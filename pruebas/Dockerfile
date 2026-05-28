FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag_answer.py .
COPY genera_examen.py .
COPY generate_testset.py .
COPY evaluate_rag.py .
COPY evaluate_rag_openai.py .
COPY evaluate_rag_prompt_1.py .
COPY evaluate_rag_prompt_2.py .
COPY evaluate_rag_sin_pistas.py .
COPY evaluate_rag_sin_contexto_pagina.py .
COPY evaluate_rag_top_k.py .
COPY evaluate_rag_conjunto.py .
COPY chroma_ddr ./chroma_ddr

ENV TOKENIZERS_PARALLELISM=false
ENV TRANSFORMERS_VERBOSITY=error
ENV CHROMA_PATH=/app/chroma_ddr
ENV OLLAMA_URL=http://ollama:11434
ENV OLLAMA_MODEL=gemma4
ENV LLM_PROVIDER=ollama
ENV OPENAI_MODEL=gpt-5-mini

CMD ["python", "rag_answer.py"]
