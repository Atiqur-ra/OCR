# import requests
# import base64

# import datetime

# # Encode image to base64
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# # Image path
# image_path = "passport.png"

# # Base64 encoded image
# image_base64 = encode_image(image_path)

# # Ollama API endpoint
# url = "http://localhost:11434/api/generate"

# # Payload for multimodal inference
# payload = {
#     "model": "qwen2.5vl:7b",
#     "prompt": "classifiy the document and based on the document summerize it and extract the text related to that",
#     "images": [image_base64],
#     "stream": False
# }

# headers = {"Content-Type": "application/json"}

# # Make the request
# try:
#     time = datetime.datetime.now()
#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code == 200:
#         result = response.json()
#         print("\nExtracted Text:")
#         print("=" * 60)
#         print(result["response"])
#         print("=" * 60)
#     else:
#         print(f"HTTP {response.status_code} Error")
#         print(response.text)
#     print("completed time",datetime.datetime.now() - time)

# except requests.exceptions.ConnectionError:
#     print("Connection error: Could not reach Ollama. Is it running?")
#     print("Run 'ollama serve' in another terminal if not started.")
# except Exception as e:
#     print(f"Unexpected error: {e}")


import spacy
from llm.qwen_client import analyze_document

nlp = spacy.load("en_core_web_trf")

def extract_passport_fields(llm_output: str) -> dict:
    passport_schema = {
    "Surname": "",
    "Given Names": "",
    "Nationality": "",
    "Place of Birth": "",
    "Date of Birth": "",
    "Date of Issue": "",
    "Date of Expiration": "",
    "Passport Number": ""
    }
    
    # Split lines and process key-value pairs
    for line in llm_output.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)  # Split only at first occurrence
            
            # Clean the key by removing any leading '-'
            key = key.lstrip("- ").strip()
            if key in passport_schema:
                passport_schema[key] = value.strip()
    
    return passport_schema

# Example text
# text = """Passport Number: 910239248
# Name: DE LA PAZ
# Nationality: UNITED STATES
# Date of Birth: 07/12/1992
# Expiry Date: 15-09-2032"""

with open("driving license.jpeg", "rb") as file:
    f = file.read()

text = analyze_document(f)

print(text)
