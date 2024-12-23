from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from google.cloud import storage

from vertexai.preview import rag
import vertexai

index_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@index_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"data_files": "ok"}
    )


def list_file(bucket_name="chatbot-data-metropolia"):
    file_list = []
    files = rag.list_files(corpus_name="projects/chatbot-444605/locations/us-central1/ragCorpora/2305843009213693952")
    for file in files:
        file_list.append(file.display_name)

    return files


@index_router.get("/list_files")
def list_files():
    return JSONResponse(content={"data_files": list_file()})
