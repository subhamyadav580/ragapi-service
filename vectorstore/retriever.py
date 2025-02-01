from langchain_community.vectorstores import Chroma
from service import load_documents, split_documents, GetEmbeddings
from logging_config import logger
import os

VECTOR_DB_PATH = "db/chroma"  # Path to store the persistent ChromaDB

class GenerateVectorStore:
    @classmethod
    def generate_vector_store(cls):
        logger.info("Inside generating vector store")
        embeddings = GetEmbeddings()
        if not os.path.exists(VECTOR_DB_PATH):
            logger.info("Creating a new Chroma vector store")
            docs = load_documents()
            splits = split_documents(docs)[:10]
            vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=VECTOR_DB_PATH)
            vectorstore.persist()

GenerateVectorStore.generate_vector_store()

class RetrieverSingleton:
    _retriever = None
    @classmethod
    def get_retriever(cls, top_k):
        logger.info("Initializing retriever")
        if cls._retriever is None:
            logger.info("Loading vector store")
            try:
                embeddings = GetEmbeddings()
                if os.path.exists(VECTOR_DB_PATH):
                    logger.info("Loading existing Chroma vector store")
                    vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
                else:
                    logger.info("Creating a new Chroma vector store")
                    docs = load_documents()
                    splits = split_documents(docs)[:10]
                    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=VECTOR_DB_PATH)
                    vectorstore.persist()

                cls._retriever = vectorstore.as_retriever(k = top_k) # k = 5 means the system will return the top 5 most relevant contexts.
                logger.info("Retriever initialization completed")
            except Exception as e:
                logger.error(f"Failed to initialize retriever: {str(e)}")
                raise
        return cls._retriever