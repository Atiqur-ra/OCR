from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

# Define the Hugging Face pipeline
image_text_pipeline = pipeline(
    task="image-text-to-text",
    model="Qwen/Qwen2-VL-7B-Instruct",
    max_new_tokens=100
)

# Initialize LangChain's HuggingFacePipeline wrapper
llm = HuggingFacePipeline(pipeline=image_text_pipeline)

# Example usage: process an image and text
input_data = {
    "image": "passport.png", 
    "text": "Describe what you see in this image."
}

response = llm.invoke(input_data)
print(response)
