from pydantic import BaseModel, Field
from typing import Optional

class QueryRequest(BaseModel):
    query: str = Field(..., example="What is philosophy?", description="The query to ask the RAG model.")
    top_k: int = Field(5, le=10, ge=1, example=5, description="Number of contexts to retrieve (default is 5)")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is philosophy?",
                "top_k": 5
            }
        }




# class QueryResponse(BaseModel):
#     response: str = Field(..., example="Philosophy is a form of systematic, rational inquiry that critically reflects on its own methods and presuppositions. It involves attentively thinking about enduring problems central to the human condition, using various methods such as conceptual analysis, thought experiments, and critical questioning. Major branches include epistemology, ethics, logic, metaphysics, among others, and it provides an interdisciplinary perspective on fields like science, mathematics, and law. Thanks for asking!")

class StreamingChunkResponse(BaseModel):
    """Model for each chunk in the stream"""
    content: str = Field(..., description="Content of the streaming chunk")
    finished: bool = Field(default=False, description="Indicates if this is the final chunk")


    class Config:
        json_schema_extra = {
            "example": {
                "content": "Philosophy is the study of fundamental questions...",
                "finished": False
            }
        }

