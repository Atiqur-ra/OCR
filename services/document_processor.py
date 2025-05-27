import os
from services.s3_services import download_from_s3
from llm.qwen_client import analyze_document


def process_document_task(data: dict):
    """
    Handles the document processing pipeline:
    - Downloads the document from S3.
    - Runs Qwen2.5-VL to classify, and extract.

    Args:
        data (dict): Dictionary containing 'file_url' and 'uploaded_by'.
    """
    file_url = data['file_url']
    uploaded_by = data['uploaded_by']

    # Extract filename from file_url
    filename = os.path.basename(file_url)

    # Download document from S3
    local_path = download_from_s3(file_url, filename)

    # Run multimodal analysis
    result = analyze_document(local_path)

    print(f"Final Result for '{filename}':\n{result}")
