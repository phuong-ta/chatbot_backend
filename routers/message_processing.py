from typing import Annotated

from fastapi import APIRouter, status, Form, HTTPException
from langchain_openai import OpenAI
from langchain_google_genai import GoogleGenerativeAI
import os
import sys
from dotenv import load_dotenv
from vertexai.preview import rag
from vertexai.preview.generative_models import GenerativeModel, Tool
import vertexai



message_router = APIRouter()
api_key = os.environ.get("OPENAI_API_KEY")


rag_retrieval_tool = Tool.from_retrieval(
    retrieval=rag.Retrieval(
        source=rag.VertexRagStore(
            rag_resources=[
                rag.RagResource(
                    rag_corpus="projects/chatbot-444605/locations/us-central1/ragCorpora/2305843009213693952",  # Currently only 1 corpus is allowed.
                    # Optional: supply IDs from `rag.list_files()`.
                    # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                )
            ],
            similarity_top_k=3,  # Optional
            vector_distance_threshold=0.5,  # Optional
        ),
    )
)

@message_router.post("/message/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(message: Annotated[str, Form()]):

    #llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    #llm = OpenAI(model_name="gpt-3.5-turbo-instruct", api_key=str(api_key))

    #

    # Create a gemini-pro model instance
    rag_model = GenerativeModel(
        model_name="gemini-1.5-flash-001", tools=[rag_retrieval_tool]
    )



    if message == "":
        # Raise an HTTP exception with a 403 status code
        raise HTTPException(status_code=403, detail="Wrong password")

    #response  = llm.invoke(str(message))
    # Generate response
    response = rag_model.generate_content(str(message))

    if response:
        return {"response": response.text}
    else:
        return {"response": "error"}
