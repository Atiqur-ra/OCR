from fastapi import UploadFile, Form
from dependencies.aws import get_s3_client
from config import settings
import uuid
from botocore.exceptions import ClientError
import os


def upload_file_to_s3(file: UploadFile, name: str, org:str) -> str:
    """
    Uploads a file to an S3 bucket under a specific folder with a unique filename.

    Args:
        file (UploadFile): The file to be uploaded, provided by FastAPI's UploadFile.
        folder (str): The name (prefix) under which the file should be stored in the S3 bucket.
        org (str): The name of organisation

    Returns:
        str: The unique key (path) of the uploaded file in the S3 bucket.

    """
    s3 = get_s3_client()
    unique_filename = f"{org}/{name}/{uuid.uuid4()}_{file.filename}"
    s3.upload_fileobj(
        file.file,
        settings.AWS_S3_BUCKET,
        unique_filename
    )

    # file_url = f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{unique_filename}"
    return unique_filename



def download_file_from_s3(file_key:str, name: str ) -> str:
    s3 = get_s3_client()
    return s3.download_file(settings.AWS_S3_BUCKET, f"{name}/{file_key}", file_key)
   

def download_from_s3(s3_key: str, local_filename: str) -> str:
    """
    Downloads a file from S3 using its key.

    Args:
        s3_key (str): S3 object key (path in bucket).
        local_filename (str): Local filename to save the file.

    Returns:
        str: Full path to the downloaded file.
    """
    s3 = get_s3_client()
    local_dir = "temp_docs"
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, local_filename)

    try:
        s3.download_file(settings.AWS_S3_BUCKET, s3_key, local_path)
        print(f"Downloaded '{s3_key}' from S3 to '{local_path}'")
        return local_path
    except Exception as e:
        raise RuntimeError(f"Failed to download from S3: {e}")