from service import GetEmbeddings, GetLLMModel, format_docs, custom_rag_prompt
from vectorstore.retriever import RetrieverSingleton
from models import QueryRequest, StreamingChunkResponse
from logging_config import logger

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json

# Initialize LLM and embeddings
llm = GetLLMModel()
embeddings = GetEmbeddings()

# Router for handling API requests
router = APIRouter()

async def generate_response(query: str, top_k: int):
    """
    Generates a response stream for a given query using RAG model.
    Args:
        query (str): The user query to be answered.
        top_k (int): Number of relevant contexts to retrieve.
    Yields:
        StreamingChunkResponse: The streaming content with 'finished' flag for each chunk.
    """
    try:
        retriever = RetrieverSingleton.get_retriever(top_k)
        rag_chain = (
            {"context": retriever | format_docs, "query": RunnablePassthrough()}
            | custom_rag_prompt
            | llm
            | StrOutputParser()
        )
        
        response_stream = rag_chain.stream(query)
        logger.info("Starting chunk generation")
        for chunk in response_stream:
            chunk_data = StreamingChunkResponse(
                content=chunk,
                finished=False
            )
            yield f"data: {json.dumps(chunk_data.model_dump())}\n\n".encode('utf-8')
            await asyncio.sleep(0.1)

        # Send final chunk
        final_chunk = StreamingChunkResponse(content="", finished=True)
        yield f"data: {json.dumps(final_chunk.model_dump())}\n\n".encode('utf-8')
        logger.info("Chunk generation completed")
            
    except Exception as e:
        logger.error(f"Error in chunk generation: {str(e)}")
        error_chunk = StreamingChunkResponse(
            content=f"Error: {str(e)}",
            finished=True
        )
        yield f"data: {json.dumps(error_chunk.model_dump())}\n\n".encode('utf-8')


@router.post("/query", response_model=StreamingChunkResponse, response_class=StreamingResponse, responses={
        200: {
            "description": "Successful response with streaming content",
            "content": {
                "text/event-stream": {
                    "schema": {
                        "type": "string",
                        "format": "binary",
                        "example": 'data: {"content": "Philosophy is", "finished": false}\n\n'
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "missing",
                                "loc": [
                                    "body",
                                    "query"
                                ],
                                "msg": "Field required",
                                "input": {
                                    "top_k": 5
                                }
                            }
                        ]
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "text/event-stream": {
                    "schema": {
                        "type": "string",
                        "example": 'data: {"content": "Error: Internal server error", "finished": true}\n\n'
                    }
                }
            }
        }
    }
)
async def query_rag(request: QueryRequest) -> StreamingResponse:
    """
    Handles the user query and streams results from the RAG Service.
    
    Args:
        request (QueryRequest): User's `query` and `top_k` parameter.
    
    Returns:
        StreamingResponse: Streamed chunks of context and answers from the RAG Service.
    """
    logger.info(f"Processing User Query: {request.query} with Top_k: {request.top_k}")
    return StreamingResponse(
        generate_response(request.query, request.top_k),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/event-stream'
        }
    )
