from flask import Flask, request, jsonify, abort
import requests
import os

app = Flask(__name__)

# 환경변수에서 키 로드 (절대 코드에 하드코딩하지 않음)
GOOGLE_VISION_API_KEY = os.environ.get("GOOGLE_VISION_API_KEY")
GPT_INTERNAL_TOKEN = os.environ.get("GPT_INTERNAL_TOKEN")

@app.route('/api/ocr', methods=['POST'])
def ocr():
    # 요청 헤더에서 토큰 확인
    token = request.headers.get("x-api-token")
    if token != GPT_INTERNAL_TOKEN:
        abort(403, description="Invalid API token")

    # JSON 입력 확인
    data = request.get_json()
    image_url = data.get("image_url")

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    # Google Vision API 호출
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
        return jsonify({ "text": text })
    except:
        return jsonify({ "text": "" })
