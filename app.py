from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

API_KEY = 'your_api_key'
URL = 'https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image'
IMAGE_URL = "https://example.com/reference-image.jpg"

@app.route('/generate-images', methods=['POST'])
def generate_images():
    data = request.json
    prompts = data['prompts']
    responses = []

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }

    for prompt in prompts:
        payload = {
            'prompt': prompt,
            'steps': 30,
            'guidance': 7.5,
            'width': 1024,
            'height': 1024,
            'response_format': 'url',
            'image_url': IMAGE_URL
        }
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        responses.append(response.json())

    return jsonify(responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
