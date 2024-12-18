from typing import Annotated

from fastapi import APIRouter, status, UploadFile, Form, HTTPException
from google.cloud import storage

file_router = APIRouter()


def upload_blob_from_memory(bucket_name, contents, destination_blob_name, metadata=None):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Set metadata if provided
    if metadata:
        blob.metadata = metadata

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
    # Add metadata (optional)
    metadata = {
        "name": file.filename,
        "description": description
    }
    bucket_name = "chatbot-data-metropolia"
    original_data_path = "original"
    vector_data_path = "original"

    upload_blob_from_memory(bucket_name=bucket_name, contents=contents,
                            destination_blob_name=f"{original_data_path}/{file.filename}", metadata=metadata)

    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename
    }