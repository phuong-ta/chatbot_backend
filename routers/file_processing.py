from typing import Annotated

from fastapi import APIRouter, status, UploadFile, Form, HTTPException
from google.cloud import storage
file_router = APIRouter()

def upload_blob_from_memory(bucket_name, contents, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    return True




@file_router.post("/upload_file", status_code=status.HTTP_201_CREATED)
async def create_upload_file(description: Annotated[str, Form()], password: Annotated[str, Form()], file: UploadFile):
    # Process the file, description, and password as needed
    # Check the password
    if password != "metropolia_pepe" or not file:
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")
    contents = file.file.read()
    file.file.seek(0)
    upload_blob_from_memory("chatbot-data-metropolia",contents=contents,destination_blob_name=file.filename )
    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename,
        "description": description,
    }
