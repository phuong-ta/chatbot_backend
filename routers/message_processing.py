import getpass
import os
from typing import Annotated
from fastapi import APIRouter, status, Form, HTTPException
from langchain_openai import ChatOpenAI, OpenAI

openai_key = os.environ['OPENAI_KEY']


message_router = APIRouter()


@message_router.post("/message/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(message: Annotated[str, Form()]):
    # Process the file, description, and password as needed
    # Check the password
    if message == "":
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")

    # response = llm.invoke(message)
    # If the password is correct, return the file information
    return {"response": openai_key}
