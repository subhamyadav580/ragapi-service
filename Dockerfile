# Use a slim Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies, including curl
RUN apt-get update && apt-get install -y \
    curl \
    git \
    libssl-dev \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama (CPU version, no sudo needed)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull the Mistral model (check Ollama docs for this step if the URL doesn't work)
RUN ollama serve & sleep 5 && ollama pull mistral  

# Copy the rest of the application files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "ollama serve & sleep 10 && uvicorn main:app --host 0.0.0.0 --port 8000"]

