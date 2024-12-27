import json
import os
from typing import Annotated

import vertexai

from fastapi import APIRouter, status, Form, HTTPException
from vertexai.preview import rag

web_router = APIRouter()

api_key = os.environ.get("OPENAI_API_KEY")

from google.cloud import storage


def get_json_from_bucket(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Get the file contents as bytes
    file_contents = blob.download_as_bytes()

    # Decode the JSON data
    json_data = json.loads(file_contents.decode("utf-8"))

    return json_data




@web_router.post("/upload_website", status_code=status.HTTP_201_CREATED)
async def create_upload_file(website: Annotated[str, Form()], web_name: Annotated[str, Form()],
                             description: Annotated[str, Form()], password: Annotated[str, Form()]):
    # Process the file, description, and password as needed
    # Check the password
    if password != "metropolia_pepe":
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")

    metadata = {
        "name": web_name,
        "description": description
    }
    """
    bucket_name = "metropolia_chatobt"

    upload_blob_from_memory(bucket_name=bucket_name, contents=get_html_file_content(str(web_link)),
                            destination_blob_name=web_name, metadata=metadata)


    vector_count = store_vector_data(project_id="chatbot-444605", location="us-central1",
                                     corpus_name="projects/chatbot-444605/locations/us-central1/ragCorpora/2305843009213693952",
                                     file_name=web_name)
                                     
                                     """
    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": web_name
    }
