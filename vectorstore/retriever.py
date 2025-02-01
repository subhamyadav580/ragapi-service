from langchain_community.vectorstores import Chroma
from service import load_documents, split_documents, GetEmbeddings
from logging_config import logger
import os

VECTOR_DB_PATH = "db/chroma"  # Path to store the persistent ChromaDB


class GenerateVectorStore:
    """
    This class handles the creation and persistence of the Chroma vector store.
    It ensures that documents are loaded, split into chunks, and then embedded 
    into a vector store for efficient similarity search.
    """
    @classmethod
    def generate_vector_store(cls):
        """
        Generates the Chroma vector store if it does not already exist. 
        Loads documents, splits them, and stores the embeddings.
        """
        logger.info("Starting the generation of the vector store")
        embeddings = GetEmbeddings()
        # Check if the vector store directory exists, create if it doesn't
        if not os.path.exists(VECTOR_DB_PATH):
            logger.info("Vector store not found. Creating a new Chroma vector store.")
            # Load documents, split them, and create the vector store
            docs = load_documents()
            splits = split_documents(docs)[:10]  # Limit the number of documents for initial testing
            vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=VECTOR_DB_PATH)
            vectorstore.persist()
            logger.info("Vector store creation completed.")
        else:
            logger.info("Vector store already exists. Skipping creation.")

# Run the vector store creation at startup
GenerateVectorStore.generate_vector_store()

class RetrieverSingleton:
    """
    Singleton class to ensure only one retriever instance is created.
    This is used to retrieve the most relevant contexts based on a user's query.
    """
    _retriever = None
    @classmethod
    def get_retriever(cls, top_k: int):
        """
        Returns the retriever object that fetches the top_k relevant contexts.
        
        Args:
            top_k (int): The number of most relevant contexts to retrieve.
        
        Returns:
            retriever (Chroma): The retriever for querying the vector store.
        """
        logger.info("Initializing the retriever")

        # Only create the retriever if it doesn't exist already
        if cls._retriever is None:
            try:
                embeddings = GetEmbeddings()

                # Load the existing vector store if it exists
                if os.path.exists(VECTOR_DB_PATH):
                    logger.info("Loading the existing Chroma vector store")
                    vectorstore = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
                else:
                    logger.error("Vector store does not exist.")
                    raise FileNotFoundError("Chroma vector store not found.")

                # Initialize the retriever with the desired number of top results
                cls._retriever = vectorstore.as_retriever(k=top_k)
                logger.info("Retriever initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize retriever: {str(e)}")
                raise
        return cls._retriever
