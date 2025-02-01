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


### Vector Store Initialization

At the start of the service, the vector store for Philosophy is created using the Wikipedia data and is stored in a Chroma vector store. This vector store will persist across requests, allowing the API to quickly retrieve the most relevant information for any given query.


### Test the API
```
    curl --location 'http://127.0.0.1:8000/query' \
    --header 'Content-Type: application/json' \
    --data '{
        "query": "What is philosophy?"
    }'
```

### Swagger API Documentation
URL (`http://localhost:8000/docs`) to access FastAPI's interactive Swagger UI for testing and documentation.


### Logs

Log files are stored in the `logs` folder, which they can monitor for activity and debugging. These logs are generated during service runtime, capturing request and error details. To view the logs, you can access them from within the container while it is running.
