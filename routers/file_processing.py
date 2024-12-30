import os
from typing import Annotated

from fastapi import APIRouter, status, UploadFile, Form, HTTPException

from document_handler import upload_blob_from_memory, store_vector_data

file_router = APIRouter()
upload_password = os.environ.get("UPLOAD_PASSWORD")


@file_router.post("/upload_file", status_code=status.HTTP_201_CREATED)
async def create_upload_file(description: Annotated[str, Form()], password: Annotated[str, Form()], file: UploadFile):
    # Process the file, description, and password as needed
    # Check the password
    if password != upload_password or not file:
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")
    contents = file.file.read()
    file.file.seek(0)
    # Add metadata (optional)
    metadata = {
        "name": file.filename,
        "description": description
    }

    upload_blob_from_memory(contents=contents, destination_blob_name=f"{file.filename}", metadata=metadata)

    store_vector_data(file_name=file.filename)

    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename
    }
