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
    docker run -p 8000:8000 --name rag-api-container rag-api-service


### Vector Store Initialization

At the start of the service, the vector store for Philosophy is created using the Wikipedia data and is stored in a Chroma vector store. The vectors of the documents are stored in a folder named `db` within the container, specifically in the `db/chroma` directory. These vector store will persist across requests, allowing the API to quickly retrieve the most relevant information for any given query.

#### Accessing the Vector Store Inside the Docker Container

1. Access the container
    ```bash
    docker exec -it rag-api-container /bin/bash

2. Navigate to the db/chroma directory
    ```bash
    cd db/chroma


### Test the API

#### Sample Request
```
    curl --location 'http://127.0.0.1:8000/query' \
    --header 'Content-Type: application/json' \
    --data '{
        "query": "What is philosophy?"
    }'
```

#### Sample Response 
```
    data: {"content": "Ph", "finished": false}

    data: {"content": "il", "finished": false}

    data: {"content": "osoph", "finished": false}

    data: {"content": "y", "finished": false}

    data: {"content": " is", "finished": false}

    data: {"content": " a", "finished": false}

    data: {"content": " system", "finished": false}

    data: {"content": "atic", "finished": false}

    data: {"content": " study", "finished": false}

    data: {"content": " of", "finished": false}

    data: {"content": " general", "finished": false}

    data: {"content": " and", "finished": false}

    data: {"content": " fundamental", "finished": false}

    data: {"content": " questions", "finished": false}

    data: {"content": " concerning", "finished": false}

    data: {"content": " topics", "finished": false}

    data: {"content": " like", "finished": false}

    data: {"content": " existence", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " reason", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " knowledge", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " value", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " mind", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " and", "finished": false}

    data: {"content": " language", "finished": false}

    data: {"content": ".", "finished": false}

    data: {"content": " It", "finished": false}

    data: {"content": " is", "finished": false}

    data: {"content": " a", "finished": false}

    data: {"content": " rational", "finished": false}

    data: {"content": " and", "finished": false}

    data: {"content": " critical", "finished": false}

    data: {"content": " inqu", "finished": false}

    data: {"content": "iry", "finished": false}

    data: {"content": " that", "finished": false}

    data: {"content": " reflect", "finished": false}

    data: {"content": "s", "finished": false}

    data: {"content": " on", "finished": false}

    data: {"content": " its", "finished": false}

    data: {"content": " methods", "finished": false}

    data: {"content": " and", "finished": false}

    data: {"content": " assumptions", "finished": false}

    data: {"content": ".", "finished": false}

    data: {"content": " Philosoph", "finished": false}

    data: {"content": "y", "finished": false}

    data: {"content": " origin", "finished": false}

    data: {"content": "ated", "finished": false}

    data: {"content": " in", "finished": false}

    data: {"content": " An", "finished": false}

    data: {"content": "cient", "finished": false}

    data: {"content": " Greece", "finished": false}

    data: {"content": " and", "finished": false}

    data: {"content": " covers", "finished": false}

    data: {"content": " a", "finished": false}

    data: {"content": " wide", "finished": false}

    data: {"content": " area", "finished": false}

    data: {"content": " of", "finished": false}

    data: {"content": " philosoph", "finished": false}

    data: {"content": "ical", "finished": false}

    data: {"content": " sub", "finished": false}

    data: {"content": "fields", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " including", "finished": false}

    data: {"content": " Western", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " Arab", "finished": false}

    data: {"content": "ic", "finished": false}

    data: {"content": "\u2013", "finished": false}

    data: {"content": "Pers", "finished": false}

    data: {"content": "ian", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " Indian", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " and", "finished": false}

    data: {"content": " Chinese", "finished": false}

    data: {"content": " philosophy", "finished": false}

    data: {"content": ".", "finished": false}

    data: {"content": " The", "finished": false}

    data: {"content": " modern", "finished": false}

    data: {"content": " period", "finished": false}

    data: {"content": " of", "finished": false}

    data: {"content": " philosophy", "finished": false}

    data: {"content": " began", "finished": false}

    data: {"content": " with", "finished": false}

    data: {"content": " the", "finished": false}

    data: {"content": " emer", "finished": false}

    data: {"content": "gence", "finished": false}

    data: {"content": " of", "finished": false}

    data: {"content": " the", "finished": false}

    data: {"content": " empir", "finished": false}

    data: {"content": "ical", "finished": false}

    data: {"content": " sciences", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " such", "finished": false}

    data: {"content": " as", "finished": false}

    data: {"content": " physics", "finished": false}

    data: {"content": " and", "finished": false}

    data: {"content": " psych", "finished": false}

    data: {"content": "ology", "finished": false}

    data: {"content": ",", "finished": false}

    data: {"content": " which", "finished": false}

    data: {"content": " are", "finished": false}

    data: {"content": " considered", "finished": false}

    data: {"content": " separate", "finished": false}

    data: {"content": " academic", "finished": false}

    data: {"content": " discipl", "finished": false}

    data: {"content": "ines", "finished": false}

    data: {"content": " in", "finished": false}

    data: {"content": " the", "finished": false}

    data: {"content": " modern", "finished": false}

    data: {"content": " sense", "finished": false}

    data: {"content": " of", "finished": false}

    data: {"content": " the", "finished": false}

    data: {"content": " term", "finished": false}

    data: {"content": ".", "finished": false}

    data: {"content": "", "finished": false}

    data: {"content": "", "finished": true}

```


### Swagger API Documentation
URL (`http://localhost:8000/docs`) to access FastAPI's interactive Swagger UI for testing and documentation.


### Logs

Log files are stored in the `logs` folder, which they can monitor for activity and debugging. These logs are generated during service runtime, capturing request and error details. To view the logs, you can access them from within the container while it is running.

#### Accessing the Logs Inside the Docker Container

1. Access the container:
    ```bash
    docker exec -it rag-api-container /bin/bash

2. Navigate to the db/chroma directory:
    ```bash
    cd logs