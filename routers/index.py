from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from google.cloud import storage

index_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@index_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"data_files": "ok"}
    )


def list_file(bucket_name="chatbot-data-metropolia"):
    file_list = []
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        file_list.append(blob.name)
    return file_list


@index_router.get("/list_files")
def list_files():
    return JSONResponse(content={"data_files": list_file()})
