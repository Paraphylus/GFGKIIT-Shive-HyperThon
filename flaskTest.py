import requests
from flask import Flask, render_template, request, jsonify
import os
from main import query  # Import your query function from main.py
from allergy_foods import allergy_foods  # Import allergy_foods list
API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer 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"}

app = Flask(__name__)

# Set the upload folder path
UPLOAD_FOLDER = '/Hyperthon'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML page

@app.route('/Hyperthon', methods=['POST'])
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Process the image using the query function in main.py
    try:
        result = query(filepath)  # Use your existing function to process the image
        food = result[0]['label']

        # Check if the food label matches any allergens
        allergens_detected = []
        for allergen in allergy_foods:
            if food.lower() == allergen.lower():
                allergens_detected.append(food)

        if allergens_detected:
            result_message = f"Food detected: {food}. Potential allergens found!"
        else:
            result_message = f"Food detected: {food}. No allergens found."

        # Pass the result message to the HTML page
        return render_template('index.html', result=result_message)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
