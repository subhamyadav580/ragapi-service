from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import bs4

from config import Config
from logging_config import logger

config = Config()

# Define the RAG prompt template
RAG_TEMPLATE = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer.

    {context}

    Question: {query}

    Helpful Answer:
"""
custom_rag_prompt = PromptTemplate.from_template(RAG_TEMPLATE)

def GetLLMModel():
    """
    Returns an initialized LLM model for generating answers.
    Returns:
        ChatOllama: The initialized LLM model.
    """
    return ChatOllama(model=config.MODEL_NAME, temperature=0)

def GetEmbeddings():
    """
    Returns an initialized embeddings model.
    Returns:
        OllamaEmbeddings: The initialized embeddings model.
    """
    return OllamaEmbeddings(model=config.MODEL_NAME)

def format_docs(docs):
    """
    Formats the documents by extracting their content.
    Args:
        docs (list): List of documents.
    Returns:
        str: Formatted string of document contents.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def load_documents():
    """
    Loads documents from a specified URL path.
    Returns:
        list: List of loaded documents.
    """
    loader = WebBaseLoader(
        web_paths=(config.WEB_PATH,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("mw-page-title-main", "mw-body-content"),
            )
        ),
    )
    return loader.load()

def split_documents(docs):
    """
    Splits documents into smaller chunks based on configuration.
    Args:
        docs (list): List of documents to be split.
    Returns:
        list: List of split document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        add_start_index=True,
    )
    return text_splitter.split_documents(docs)

