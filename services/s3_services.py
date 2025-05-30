from fastapi import UploadFile, Form
from dependencies.aws import get_s3_client
from config import settings
import uuid
import os
import logging
from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)




def generate_s3_key_by_type(file: UploadFile, emp_id: str, org: str, doc_type: str) -> str:
    """
    Generate S3 key based on organization, employee, and document type.

    Example key: org1/emp123/passport.pdf
    """
    ext = file.filename.split(".")[-1]
    return f"{org}/{emp_id}/{doc_type.lower()}.{ext}"


def upload_file_to_s3(file: UploadFile, emp_id: str, org:str,doc_type: str) -> str:
    """
    Uploads a file to an S3 bucket under a specific folder with a unique filename.

    Args:
        file (UploadFile): The file to be uploaded, provided by FastAPI's UploadFile.
        folder (str): The name (prefix) under which the file should be stored in the S3 bucket.
        org (str): The name of organisation

    Returns:
        str: The unique key (path) of the uploaded file in the S3 bucket.

    """
    
    try:
        s3 = get_s3_client()
        unique_filename = generate_s3_key_by_type(file, emp_id, org, doc_type)
        s3.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET,
            unique_filename
        )
        logging.info(f"Uploaded '{file.filename}' to S3 as '{unique_filename}'")
        return unique_filename
    except Exception as e:
        raise RuntimeError(f"Failed to upload to S3: {e}")



def download_file_from_s3(file_key:str, name: str ) -> str:
    s3 = get_s3_client()
    return s3.download_file(settings.AWS_S3_BUCKET, f"{name}/{file_key}", file_key)
   

def download_from_s3(s3_key: str) -> str:
    """
    Downloads a file from S3 using its key.

    Args:
        s3_key (str): S3 object key (path in bucket).
        local_filename (str): Local filename to save the file.

    Returns:
        str: Full path to the downloaded file.
    """
    s3 = get_s3_client()
    try:
        response = s3.get_object(Bucket=settings.AWS_S3_BUCKET, Key=s3_key)
        file_content = response["Body"].read()
        logging.info(f"Fetched '{s3_key}' from S3 into memory.")
        return file_content
    except Exception as e:
        raise RuntimeError(f"Failed to fetch from S3: {e}")