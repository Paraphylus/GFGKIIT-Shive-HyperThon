import requests
from allergy_foods import allergy_foods

API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("download.jpg")
food = output[0]['label']
for i in range(len(allergy_foods)):
    if food.lower() == allergy_foods[i].lower():
        print("Food has potential allergen: " + food)