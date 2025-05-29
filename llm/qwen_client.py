import requests
import base64
import datetime
import logging
from logging_config import setup_logging

# Initialize logging once per app start
setup_logging()
logger = logging.getLogger(__name__)

def encode_image_base64(image_path: str) -> str:
    """
    Encodes an image file as base64.

    Args:
        image_path (str): Local image path.

    Returns:
        str: Base64-encoded string of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            logger.info(f"Encoded image '{image_path}' to base64 successfully.")
            return encoded
    except Exception as e:
        logger.error(f"Failed to encode image '{image_path}': {e}")
        raise

def analyze_document(image_bytes: bytes) -> str:
    """
    Analyzes document using Qwen2.5-VL by encoding image bytes to base64.

    Args:
        image_bytes (bytes): Raw image content.

    Returns:
        str: Model response.
    """
    try:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    except Exception as e:
        logger.error(f"Base64 encoding failed: {e}")
        raise

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5vl:7b",
        "prompt": """Classify this document as one of the following types: Passport, Driving License, Resume, I-9, SSN, Timesheet, Invoice, Educational Certificate.
                        Then extract only the relevant fields based on the document type.""",
        "images": [image_base64],
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Document analyzed successfully.")
            return result.get("response", "No response text.")
        else:
            error_msg = f"Ollama error {response.status_code}: {response.text}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    except requests.exceptions.ConnectionError:
        logger.error("Connection error: Ollama server not reachable.")
        raise RuntimeError("Ollama not reachable. Is the Ollama server running?")

    except Exception as e:
        logger.error(f"Unexpected error during document analysis: {e}")
        raise
