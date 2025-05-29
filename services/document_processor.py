import os
import logging
from services.s3_services import download_from_s3
from llm.qwen_client import analyze_document
from logging_config import setup_logging
from templates.extractor import extract_document_fields

setup_logging()
logger = logging.getLogger(__name__)


def process_document_task(data: dict):
    """
    Handles the document processing pipeline:
    - Downloads the document from S3 in memory.
    - Sends to Qwen2.5-VL model to classify and extract.
    - Post-processes the result using a template-based extractor.

    Args:
        data (dict): Should include 'file_url' and 'uploaded_by'.
    """
    file_url = data.get('file_url')
    uploaded_by = data.get('uploaded_by')

    if not file_url or not uploaded_by:
        logger.error("Missing required keys in data")
        return

    filename = os.path.basename(file_url)

    # Step 1: Download file from S3 as bytes
    try:
        image_bytes = download_from_s3(file_url)
        logger.info(f"Downloaded file {filename} for user {uploaded_by}")
    except Exception as e:
        logger.error(f"Failed to download file from S3: {e}")
        return

    # Step 2: Run multimodal document analysis
    try:
        raw_response = analyze_document(image_bytes)
        logger.info(f"Model response received for {filename}")
    except Exception as e:
        logger.error(f"Qwen document analysis failed: {e}")
        return

    # Step 3: Template-based structured field extraction
    try:
        structured_data = extract_document_fields(raw_response)
        logger.info(f"Structured extraction for {filename}: {structured_data}")
    except Exception as e:
        logger.error(f"Failed during template-based extraction: {e}")
        return
