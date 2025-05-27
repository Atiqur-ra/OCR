import requests
import base64

import datetime

# Encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Image path
image_path = "passport.png"

# Base64 encoded image
image_base64 = encode_image(image_path)

# Ollama API endpoint
url = "http://localhost:11434/api/generate"

# Payload for multimodal inference
payload = {
    "model": "qwen2.5vl:7b",
    "prompt": "classifiy the document and based on the document summerize it and extract the text related to that",
    "images": [image_base64],
    "stream": False
}

headers = {"Content-Type": "application/json"}

# Make the request
try:
    time = datetime.datetime.now()
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        print("\nExtracted Text:")
        print("=" * 60)
        print(result["response"])
        print("=" * 60)
    else:
        print(f"HTTP {response.status_code} Error")
        print(response.text)
    print("completed time",datetime.datetime.now() - time)

except requests.exceptions.ConnectionError:
    print("Connection error: Could not reach Ollama. Is it running?")
    print("Run 'ollama serve' in another terminal if not started.")
except Exception as e:
    print(f"Unexpected error: {e}")
