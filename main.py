from fastapi import FastAPI
from handlers import router


app = FastAPI(
    title="Streaming RAG API Service",
    description="This API allows querying a Retrieval-Augmented Generation (RAG) system to answer questions based on provided context.",
)

app.include_router(router=router, prefix="")

