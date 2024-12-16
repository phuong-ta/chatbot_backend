import getpass
import os
from typing import Annotated
from fastapi import APIRouter, status, Form, HTTPException
from langchain_openai import ChatOpenAI, OpenAI


os.environ['OPENAI_KEY']

llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0,
    max_retries=2,
    # api_key="...",
    # base_url="...",
    # organization="...",
    # other params...
)


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
    return {"response": llm.invoke(message)}
