from flask import Flask, render_template, request, jsonify
import os
from main import query  # Import your query function from main.py

app = Flask(__name__)

# Set the upload folder path
UPLOAD_FOLDER = 'C:\Users\KIIT0001\Desktop\Hyperthon'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML page

@app.route('/upload', methods=['POST'])
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
        return jsonify({"result": result})  # Return the result as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
