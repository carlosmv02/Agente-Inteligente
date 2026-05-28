# Dockerfile
FROM python:3.11-slim

# install minimal system packages for building wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy and install dependencies first for cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project sources
COPY . .

# environment defaults (can override when running)
ENV CHROMA_PATH=/app/chroma_ddr
ENV COLLECTION_NAME=ddr_chunks
ENV OLLAMA_URL=http://ollama:11434
ENV OLLAMA_MODEL=gemma4
ENV LLM_PROVIDER=ollama
ENV OPENAI_MODEL=gpt-5-mini

CMD ["python", "rag_answer.py"]
