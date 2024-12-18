from typing import Annotated

from fastapi import APIRouter, status, UploadFile, Form, HTTPException
from google.cloud import storage
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


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


def load_file_from_cloud(bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    loader = PyPDFLoader(blob.download_as_string().decode("utf-8"))
    docs = loader.load()
    return docs






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

    data = PyPDFLoader((file.file.read()).decode("utf-8"))
    documents = data.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(), metadata=metadata)

    upload_blob_from_memory(bucket_name=bucket_name, contents=vectorstore,
                            destination_blob_name=f"{vector_data_path}/{file.filename}")




    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename
    }