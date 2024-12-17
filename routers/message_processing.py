from typing import Annotated

from fastapi import APIRouter, status, Form, HTTPException
from langchain_openai import OpenAI
from langchain_google_genai import GoogleGenerativeAI
import os

api_key = "AIzaSyD0AbJ8GiYWiFCdYdFZSDDPa2jhWb7oc8E"

message_router = APIRouter()


@message_router.post("/message/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(message: Annotated[str, Form()]):
    # Process the file, description, and password as needed
    # Check the password
    # llm = OpenAI( api_key=api_key)
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    if message == "":
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")

    # If the password is correct, return the file information
    #return {"response": message + " from backend"}

    return {"response": llm.invoke(str(message))}
