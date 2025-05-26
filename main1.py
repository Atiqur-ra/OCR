# from model.ocr_model import OCR
# ocr = OCR()                 # auto-select backend
# text = ocr.extract_text("passport.png")
# print(text)

# from dotenv import load_dotenv
# load_dotenv()
# from langchain_huggingface import HuggingFaceEndpoint

# # Use a hosted model (without downloading)
# llm = HuggingFaceEndpoint(
#     model="Qwen/Qwen2-VL-7B-Instruct",
#     task="image-text-to-text"
# )

# prompt = "Extract structured text from this document"
# result = llm.invoke(prompt)
# print(result)

# from huggingface_hub import InferenceClient
# import base64

# client = InferenceClient(
#     model="Qwen/Qwen2-VL-7B-Instruct",
#     provider="nebius",
#     token="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",
# )

# # Encode image to base64 data URL
# with open("passport.png", "rb") as f:
#     image_bytes = f.read()
#     base64_image = base64.b64encode(image_bytes).decode("utf-8")
#     data_url = f"data:image/png;base64,{base64_image}"

# # Send request
# response = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Extract structured text from this image. like,name date_of_birth, passport_number, country, date_of_expiry"},
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": data_url}
#                 }
#             ]
#         }
#     ]
# )

# print(response.choices[0].message["content"])


# from transformers import AutoProcessor, AutoModelForVision2Seq
# from PIL import Image
# import torch

# # Load model and processor
# model_id = "Qwen/Qwen2-VL-7B-Instruct"
# processor = AutoProcessor.from_pretrained(model_id)
# model = AutoModelForVision2Seq.from_pretrained(
#     model_id,
#     torch_dtype=torch.float32,
#     device_map={"": "cpu"}
# )
# # Load image
# image = Image.open("passport.png").convert("RGB")


# prompt = "<img> Extract structured text from this document."

# # Prepare input
# inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)

# # Generate output
# generated_ids = model.generate(**inputs, max_new_tokens=1024)
# output = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

# print(output)



from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

# Load model and processor
model_id = "Qwen/Qwen2-VL-7B-Instruct"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForVision2Seq.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    device_map={"": "cpu"}  # or "auto" if using GPU
)

# Load image
image = Image.open("passport.png").convert("RGB")

# Use proper image token
prompt = "<|image|> Extract structured text from this document."

# Prepare input
inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)

# Generate output
generated_ids = model.generate(**inputs, max_new_tokens=1024)
output = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(output)

