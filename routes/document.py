from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List
from services.s3_services import upload_file_to_s3, download_file_from_s3
router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/upload/")
async def upload_document(name:str = Form(...),files: List[UploadFile] = File(...)):
    upload_urls=[]
    try:
        for file in files:
            file_url = upload_file_to_s3(file, name)
            upload_urls.append(file_url)
        return {"urls": upload_urls} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/download/")
def download_document(file_key: str = Form(...), name:str = Form(...)):
    try:
        download_file_from_s3(file_key, name)
        return {"message":"file downloaded succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
