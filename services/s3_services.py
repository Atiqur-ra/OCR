from fastapi import UploadFile, Form
from dependencies.aws import get_s3_client
from config import settings
import uuid
from botocore.exceptions import ClientError


def upload_file_to_s3(file: UploadFile, folder: str) -> str:
    s3 = get_s3_client()
    file_ext = file.filename.split('.')[-1]
    unique_filename = f"{folder}/{uuid.uuid4()}.{file_ext}"
    s3.upload_fileobj(
        file.file,
        settings.AWS_S3_BUCKET,
        unique_filename
    )

    file_url = f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{unique_filename}"
    return unique_filename


def download_file_from_s3(file_key:str, name: str ) -> str:
    s3 = get_s3_client()
    return s3.download_file(settings.AWS_S3_BUCKET, f"{name}/{file_key}", file_key)
   