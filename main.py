from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.index import index_router
from routers.message_processing import message_router
from routers.file_processing import file_router
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(index_router)
app.include_router(message_router)
app.include_router(file_router)
