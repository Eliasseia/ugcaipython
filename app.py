from flask import Flask, request, jsonify
import requests
import json
import openai

app = Flask(__name__)

# Your API keys
API_KEY = 'your_img_api_key'
OPENAI_API_KEY = 'your_openai_api_key'

# API endpoints
IMG_URL = 'https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image'
IMAGE_URL = "https://example.com/reference-image.jpg"

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

@app.route('/generate-images', methods=['POST'])
def generate_images():
    data = request.json
    script = data.get('script')
    description = data.get('description')
    
    # Generate prompts using GPT-4
    gpt_prompt = f"Generate creative image descriptions based on the following script and description:\n\nScript: {script}\n\nDescription: {description}"
    gpt_response = openai.Completion.create(
        model="gpt-4",
        prompt=gpt_prompt,
        max_tokens=4000,
        temperature=0.7
    )
    
    # Use the GPT response directly as the prompt for image generation
    generated_prompt = gpt_response.choices[0].text.strip()

    payload = {
        'prompt': generated_prompt,
        'steps': 30,
        'guidance': 7.5,
        'width': 1024,
        'height': 1024,
        'response_format': 'url',
        'image_url': IMAGE_URL
    }

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }

    response = requests.post(IMG_URL, headers=headers, data=json.dumps(payload))
    img_response = response.json()

    return jsonify(img_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
