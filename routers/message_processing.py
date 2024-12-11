from typing import Annotated

from fastapi import APIRouter, status, Form

message_router = APIRouter()


@message_router.post("/message/", status_code=status.HTTP_201_CREATED)
async def create_item(message: Annotated[str, Form()]):
    return {"response": message + " server"}
