from fastapi import FastAPI, Request
from handlers import router
from logging_config import logger

app = FastAPI(
    title="Streaming RAG API Service",
    description="This API allows querying a Retrieval-Augmented Generation (RAG) system to answer questions based on provided context.",
)

app.include_router(router=router, prefix="")



@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    logger.info(f"Start of the request: {request.base_url}")
    response = await call_next(request)
    logger.info(f"End of the request: {request.base_url}")
    logger.info(f"Response for url: {response}")
    return response
