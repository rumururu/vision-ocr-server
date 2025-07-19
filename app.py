from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
GOOGLE_VISION_API_KEY = os.environ.get("GOOGLE_VISION_API_KEY")

@app.route('/api/ocr', methods=['POST'])
def ocr():
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    vision_api_url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
    payload = {
        "requests": [{
            "image": { "source": { "imageUri": image_url } },
            "features": [{ "type": "TEXT_DETECTION" }]
        }]
    }

    response = requests.post(vision_api_url, json=payload)
    result = response.json()

    try:
        text = result["responses"][0]["textAnnotations"][0]["description"]
        return jsonify({"text": text})
    except:
        return jsonify({"text": ""})
