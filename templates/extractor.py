import yaml
from dotenv import load_dotenv
import os
load_dotenv()

def load_templates(file_path: str) -> dict:
    """Loads document templates from a YAML file."""
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: YAML file not found at {file_path}. Check your directory.")
    
def detect_document_type(raw_response: str, templates: dict) -> str:
    """Detects the document type based on keywords in the raw response."""
    for doc_type in templates:
        if doc_type.lower() in raw_response.lower():
            return doc_type
    return None

def extract_document_fields(llm_output: str) -> dict:
    """
    Extracts relevant fields based on the document type from an LLM output.

    Args:
        document_type (str): The type of document (e.g., "passport", "driving_license").
        llm_output (str): The raw extracted text from the document.
        templates (dict): Preloaded document templates from YAML.

    Returns:
        dict: Structured dictionary with required fields for storage.
    """
    if not llm_output:
        raise ValueError("LLM output is empty")
    templates = load_templates(os.getenv("TEMPLATES_FILE_PATH"))
    document_type = detect_document_type(llm_output, templates)
    if document_type not in templates:
        raise ValueError(f"Unsupported document type: {document_type}")

    
    document_schema = templates[document_type].copy()

    for line in llm_output.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            key = key.lstrip("- ").strip()

            if key in document_schema:
                document_schema[key] = value.strip()

    return document_schema



