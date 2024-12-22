import os
from typing import Annotated

import vertexai
from fastapi import APIRouter, status, UploadFile, Form, HTTPException
from vertexai.preview import rag
import json

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

""""
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


def store_vector_data(project_id, location, corpus_name, file_name):
    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location=location)
    bucket_path = [f"gs://metropolia_chatobt/{file_name}"]

    # Import Files to the RagCorpus
    response = rag.import_files(
        corpus_name=corpus_name,
        paths=bucket_path,
        chunk_size=512,  # Optional
        chunk_overlap=100,  # Optional
        max_embedding_requests_per_min=900,  # Optional
    )

    return response.imported_rag_files_count


@web_router.post("/upload_website", status_code=status.HTTP_201_CREATED)
async def create_upload_file(website: Annotated[str, Form()],description: Annotated[str, Form()], password: Annotated[str, Form()]):
    # Process the file, description, and password as needed
    # Check the password
    if password != "metropolia_pepe":
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")
    web_link = website
    # Add metadata (optional)
    metadata = {
        "name": web_link,
        "description": description
    }

    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": web_link
    }
