import os

import requests
import vertexai
from bs4 import BeautifulSoup
from google.cloud import storage
from vertexai.preview import rag

api_key = os.environ.get("OPENAI_API_KEY")
bucket_name = os.environ.get("BUCKET_NAME")
project_id = os.environ.get("PROJECT_ID")
corpus_name = os.environ.get("CORPUS_NAME")

def process_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return text


def upload_blob_from_memory(contents, destination_blob_name, metadata=None):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Set metadata if provided
    if metadata:
        blob.metadata = metadata

    blob.upload_from_string(contents)
    return True


def store_vector_data(file_name):
    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")
    bucket_path = [f"gs://{bucket_name}/{file_name}"]

    # Import Files to the RagCorpus
    response = rag.import_files(
        corpus_name=corpus_name,
        paths=bucket_path,
        chunk_size=512,  # Optional
        chunk_overlap=100,  # Optional
        max_embedding_requests_per_min=900,  # Optional
    )

    return response.imported_rag_files_count
