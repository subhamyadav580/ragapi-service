# Streaming RAG API Service

This repository contains a **Streaming Retrieval-Augmented Generation (RAG)** API service using **TinyLlama** and Wikipedia data on **Philosophy**. The API, built with **FastAPI** and served by **Uvicorn**, generates real-time text based on the Wikipedia knowledge base.

## Features

- Real-time text generation from [Wikipedia (Philosophy)](https://en.wikipedia.org/wiki/Philosophy)
- **TinyLlama** for RAG tasks
- **FastAPI** & **Uvicorn** for API framework
- **Ollama** for model execution

## Installation

### Prerequisites

Ensure Docker is installed. Get it [here](https://docs.docker.com/get-docker/).

### Build & Run the Service

1. Clone the repository:

   ```bash
   git clone https://github.com/subhamyadav580/ragapi-service
   cd ragapi-service

2. Build the Docker Image
    ```bash
    docker build -t rag-api-service .

3. Run the Docker Container
    ```bash
    docker run -d -p 8000:8000 --name rag-api-container rag-api-service

### Test the API
```bash 

    curl --location 'http://127.0.0.1:8000/query' \
    --header 'Content-Type: application/json' \
    --data '{
        "query": "What is philosophy?"
    }'
