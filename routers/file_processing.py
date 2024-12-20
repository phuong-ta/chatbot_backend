import os
from typing import Annotated

import vertexai
from fastapi import APIRouter, status, UploadFile, Form, HTTPException
from vertexai.preview import rag

file_router = APIRouter()
api_key = os.environ.get("OPENAI_API_KEY")

from google.cloud import storage
import json

"""
def get_json_from_bucket(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Get the file contents as bytes
    file_contents = blob.download_as_bytes()

    # Decode the JSON data
    json_data = json.loads(file_contents.decode("utf-8"))

    return json_data


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_json_from_bucket(bucket_name="metropolia_chatobt",
                                                                    file_name="google_credentials.json")
                                                
"""


def upload_blob_from_memory(bucket_name, contents, destination_blob_name, metadata=None):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Set metadata if provided
    if metadata:
        blob.metadata = metadata

    blob.upload_from_string(contents)
    return True

"""
def store_vector_data(project_id, location, corpus_name, bucket_path):
    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location=location)

    # Import Files to the RagCorpus
    response = rag.import_files(
        corpus_name=corpus_name,
        paths=bucket_path,
        chunk_size=512,  # Optional
        chunk_overlap=100,  # Optional
        max_embedding_requests_per_min=900,  # Optional
    )

    return response.imported_rag_files_count
"""

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
    bucket_name = "metropolia_chatobt"

    upload_blob_from_memory(bucket_name=bucket_name, contents=contents,
                            destination_blob_name=f"{file.filename}", metadata=metadata)


    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename
    }
