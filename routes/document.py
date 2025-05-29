from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
from services.s3_services import upload_file_to_s3, download_file_from_s3
from kafka.producer import publish_document_event

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/upload/")
async def upload_document(org:str= Form(...),emp_id: str = Form(...), files: List[UploadFile] = File(...)):
    """
    Upload multiple documents to S3 and publish metadata to Kafka.

    Args:
        org (str): Name of the Organisation
        name (str): Name or identifier of the uploader.
        files (List[UploadFile]): List of files to be uploaded.

    Returns:
        dict: A dictionary containing a list of URLs for the successfully uploaded files.

    """
    upload_urls = []
    try:
        for file in files:
            file_url = upload_file_to_s3(file, emp_id, org)
            filename = file_url.split("/")[-1]
            publish_document_event({
                "filename": filename,
                "file_url": file_url,
                "uploaded_by": emp_id
            })
            upload_urls.append(file_url)
        return {"urls": upload_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/download/")
def download_document(file_key: str = Form(...), name: str = Form(...)):
    """
    Download a document from S3 storage.

    Args:
        file_key (str): The unique key (filename) of the file stored in S3.
        name (str): Name or identifier of the requester or the download target path.

    Returns:
        dict: A message indicating successful download.
    """
    try:
        download_file_from_s3(file_key, name)
        return {"message": "file downloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
