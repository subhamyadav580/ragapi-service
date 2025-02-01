from pydantic import BaseModel, Field, StrictInt, StrictBool
from typing import Optional

class QueryRequest(BaseModel):
    """
    Schema for user input query request to the RAG model.
    """
    query: str = Field(..., example="What is philosophy?", description="The query to ask the RAG model.")
    top_k: StrictInt = Field(5, le=10, ge=1, example=5, description="Number of contexts to retrieve (default is 5)")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is philosophy?",
                "top_k": 5
            }
        }

class StreamingChunkResponse(BaseModel):
    """
    Model for each chunk in the stream that the API will return.
    """
    content: str = Field(..., description="Content of the streaming chunk")
    finished: StrictBool = Field(default=False, description="Indicates if this is the final chunk")


    class Config:
        json_schema_extra = {
            "example": {
                "content": "Philosophy is the study of fundamental questions...",
                "finished": False
            }
        }
