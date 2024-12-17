from typing import Annotated

from fastapi import APIRouter, status, Form, HTTPException
from langchain_openai import OpenAI
from langchain_google_genai import GoogleGenerativeAI
import os
import sys




message_router = APIRouter()
api_key = os.environ.get("OPENAI_API_KEY")


@message_router.post("/message/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(message: Annotated[str, Form()]):

    #llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", api_key=api_key)
    if message == "":
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")

    return {"response": llm.invoke(str(message))}
