import os
from typing import Annotated

import vertexai
from fastapi import APIRouter, status, UploadFile, Form, HTTPException
from google.cloud import storage
from vertexai.preview import rag

file_router = APIRouter()
api_key = os.environ.get("OPENAI_API_KEY")


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
def store_vector_data(project_id, location, display_name, bucket_name, file_paths,
                      embedding_model="text-embedding-004"):
    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location=location)

    # Create RagCorpus
    embedding_model_config = rag.EmbeddingModelConfig(
        publisher_model=f"publishers/google/models/{embedding_model}"
    )

    rag.create_corpus(
        display_name=display_name,
        embedding_model_config=embedding_model_config,
    )
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
    original_data_path = "original"

    upload_blob_from_memory(bucket_name=bucket_name, contents=contents,
                            destination_blob_name=f"{original_data_path}/{file.filename}", metadata=metadata)

    # store_vector_data(project_id=3046579594799874048,location="europe-north1",display_name="metropolia_rag",bucket_name="metropolia_chatobt", file_paths="gs://metropolia_chatobt",embedding_model="text-embedding-004")

    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename
    }
