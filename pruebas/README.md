# Pruebas del sistema RAG

Esta carpeta contiene el entorno de evaluacion del asistente RAG de DDR:
scripts, testset, base vectorial, configuracion Docker y resultados.

La documentacion completa esta en:

```text
pruebas.md
```

Comando basico:

```bash
docker compose up -d --build
docker compose run --rm rag python evaluate_rag.py
```

Para las pruebas adicionales:

```bash
docker compose run --rm -e OPENAI_API_KEY rag python evaluate_rag_conjunto.py
```
