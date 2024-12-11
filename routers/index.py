from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

index_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@index_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"data_files": "ok"}
    )


@index_router.get("/list_files")
def list_files():
    fruit_list = ["apple", "banana", "cherry"]
    return JSONResponse(content={"data_files": fruit_list})


@index_router.post("/upload_file")
async def upload_file():
    return {"message": "Admin getting schwifty"}