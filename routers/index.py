import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

index_router = APIRouter()

templates = Jinja2Templates(directory="templates")
from google.cloud import storage


def list_files_from_google(bucket_name="metropolia-rag-openai"):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    credentials_file = os.environ.get("GOOGLE_CREDENTIALS")

    if not credentials_file:
        raise ValueError("GOOGLE_CREDENTIALS environment variable is not set.")

    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # store
    file_list = []

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        file_list.append(blob.name)

    return file_list


@index_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"data_files": "ok"}
    )


@index_router.get("/list_files")
def list_files():
    return JSONResponse(content={"data_files": list_files_from_google()})
