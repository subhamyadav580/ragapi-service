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

llm = GetLLMModel()
embeddings = GetEmbeddings()

router = APIRouter()

async def generate_response(query: str, top_k: int):
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


@router.post("/query", response_class=StreamingResponse, responses={
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
    Query the RAG (Retrieval-Augmented Generation) model with an optional `top_k` parameter.
    This endpoint returns a stream of results from the RAG model, where `top_k` specifies 
    the number of relevant contexts to retrieve.

    - `query`: The user's query for the RAG model.
    - `top_k`: The optional parameter to limit the number of retrieved contexts. Default is 5.
    """
    logger.info(f"Processing User Query: {request.query} and Top_k: {request.top_k}")
    return StreamingResponse(
        generate_response(request.query, request.top_k),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/event-stream'
        }
    )

