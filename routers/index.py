from typing import Annotated

from fastapi import APIRouter, Request, status, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

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


@index_router.post("/upload_file", status_code=status.HTTP_201_CREATED)
async def create_upload_file(description: Annotated[str, Form()], password: Annotated[str, Form()], file: UploadFile):
    # Process the file, description, and password as needed
    # Check the password
    if password != "metropolia_pepe":
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")

    # If the password is correct, return the file information
    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename,
        "description": description,
    }

