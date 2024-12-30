from typing import Annotated

from fastapi import APIRouter, status, Form, HTTPException

from document_handler import process_url, upload_blob_from_memory, store_vector_data
import os
web_router = APIRouter()

upload_password = os.environ.get("UPLOAD_PASSWORD")

@web_router.post("/upload_website", status_code=status.HTTP_201_CREATED)
async def create_upload_file(website: Annotated[str, Form()], web_name: Annotated[str, Form()],
                             description: Annotated[str, Form()], password: Annotated[str, Form()]):
    # Process the file, description, and password as needed
    # Check the password
    if password != upload_password:
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")

    metadata = {
        "name": web_name,
        "description": description
    }


    destination_blob_name = f"{website.replace('/', '_')}.txt"
    contents = process_url(url=website)
    upload_blob_from_memory(contents=contents, destination_blob_name=destination_blob_name, metadata=metadata)
    store_vector_data(website)

    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": web_name
    }
