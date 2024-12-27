import json
import os
from typing import Annotated
import requests

import vertexai

from fastapi import APIRouter, status, Form, HTTPException
from vertexai.preview import rag
from bs4 import BeautifulSoup


web_router = APIRouter()

api_key = os.environ.get("OPENAI_API_KEY")

from google.cloud import storage


def process_url (url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    upload_to_cloud_storage(text, url)


def upload_to_cloud_storage(text, url):
    """
    Uploads text to Cloud Storage.
    """

    bucket_name = "metropolia_chatobt"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{url.replace('/', '_')}.txt")
    blob.upload_from_string(text)

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
    """
    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": web_name
    }
