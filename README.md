# Agente RAG para Diseno y Dimensionado de Redes

Este repositorio contiene un asistente academico basado en RAG
(`Retrieval-Augmented Generation`) para la asignatura **Diseno y
Dimensionado de Redes (DDR)**.

El sistema toma material docente de la asignatura, lo segmenta en fragmentos con
metadatos, construye una base vectorial con ChromaDB y permite hacer preguntas en
lenguaje natural usando un modelo local servido por Ollama.

Tambien incluye una carpeta de pruebas reproducibles (`pruebas/`) para comparar
modelos, prompts, estrategias de recuperacion y variantes del sistema.

## Que Hace

El proyecto cubre el flujo completo de un sistema RAG:

1. **Ingesta documental**
   - Lee PDFs de teoria.
   - Lee relaciones de problemas.
   - Lee examenes resueltos.
   - Lee scripts `.m` asociados a examenes.
   - Extrae texto, aplica OCR cuando procede y genera chunks con metadatos.

2. **Construccion de la base vectorial**
   - Carga `chunks_ddr.jsonl`.
   - Genera embeddings con `intfloat/multilingual-e5-base`.
   - Guarda documentos, metadatos y vectores en `chroma_ddr/`.

3. **Consulta**
   - Recibe una pregunta del usuario.
   - Detecta pistas como tema, ejercicio, convocatoria o curso academico.
   - Recupera contexto relevante desde ChromaDB.
   - Construye un prompt con ese contexto.
   - Genera la respuesta final con Ollama.

4. **Evaluacion**
   - La carpeta `pruebas/` contiene testset, scripts de evaluacion y resultados.
   - Permite comparar modelos, prompts, `TOP_K`, uso de pistas y contexto de
     pagina.

## Estructura Del Repositorio

```text
RAG/
|-- README.md                  # guia general del repositorio
|-- ARCHITECTURE.md            # diagrama funcional del sistema
|-- main_ingest.py             # genera chunks_ddr.jsonl desde materiales/
|-- build_vector_db.py         # reconstruye chroma_ddr/
|-- rag_answer.py              # asistente interactivo principal
|-- genera_examen.py           # logica avanzada de examenes usada en pruebas
|-- chunks_ddr.jsonl           # chunks generados por la ingesta
|-- chroma_ddr/                # base vectorial persistente
|-- materiales/
|   |-- teoria/                # PDFs de teoria
|   |-- problemas/             # relaciones de problemas
|   `-- examenes/              # examenes y scripts .m
|-- ingest/
|   |-- chunk_pdf_ocr.py
|   |-- chunk_problemas_pdf.py
|   |-- chunk_examenes.py
|   |-- chunk_tema1.py ... chunk_tema5.py
|   `-- chunk_problemas_tema2.py ... chunk_problemas_tema5.py
|-- embeddings/
|   `-- embed_chunks.py
|-- pruebas/
|   |-- pruebas.md             # guia completa de evaluacion
|   |-- evaluate_rag*.py
|   |-- tests/
|   |-- resultados/
|   `-- chroma_ddr/
|-- Dockerfile
|-- docker-compose.yml
`-- requirements.txt
```

## Materiales De Entrada

Los documentos fuente se guardan en `materiales/`:

```text
materiales/
|-- teoria/
|   |-- Tema1_2526.pdf
|   |-- Tema2_2526.pdf
|   |-- Tema3_2526.pdf
|   |-- Tema4_2526.pdf
|   `-- Tema5_2526.pdf
|-- problemas/
|   |-- problemas_tema2.pdf
|   |-- problemas_tema2_II.pdf
|   |-- problemas_tema3.pdf
|   |-- problemas_tema4.pdf
|   `-- problemas_tema5.pdf
`-- examenes/
    |-- enero-2022-2023/
    |-- febrero-2022-2023/
    |-- enero-2023-2024/
    `-- ...
```

Si se cambian, anaden o eliminan documentos en `materiales/`, hay que volver a
ejecutar la ingesta y reconstruir la base vectorial.

## Requisitos

### Opcion Recomendada: Docker

- Docker
- Docker Compose
- Espacio suficiente para los modelos de Ollama y ChromaDB

### Opcion Local Sin Docker

- Python 3.11
- Ollama instalado y ejecutandose
- Dependencias de `requirements.txt`
- Tesseract OCR si se quiere regenerar el corpus con OCR

Instalacion local:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## OCR Y Tesseract

La ingesta usa `pytesseract` para extraer texto de imagenes dentro de PDFs. Si se
ejecuta la ingesta en otra maquina, puede hacer falta ajustar la ruta de
Tesseract en los chunkers o instalarlo en el entorno.

Archivos relevantes:

- `ingest/chunk_pdf_ocr.py`
- `ingest/chunk_problemas_pdf.py`
- `ingest/chunk_examenes.py`

Si solo se consulta una base ya construida (`chroma_ddr/`), no hace falta OCR.

## Uso Rapido Con Docker Compose

Levantar servicios:

```bash
docker compose up -d --build
```

Descargar el modelo configurado por defecto:

```bash
docker compose exec ollama ollama pull gemma4
```

Lanzar el asistente:

```bash
docker compose run --rm -it rag
```

Tambien se puede indicar el script explicitamente:

```bash
docker compose run --rm -it rag python rag_answer.py
```

Para salir del asistente:

```text
exit
```

## Uso Local Sin Docker

Arrancar Ollama en una terminal:

```bash
ollama serve
```

Descargar el modelo:

```bash
ollama pull gemma4
```

Ejecutar el asistente:

```bash
LLM_PROVIDER=ollama python rag_answer.py
```

Si Ollama esta en otra URL:

```bash
LLM_PROVIDER=ollama OLLAMA_URL=http://localhost:11434 python rag_answer.py
```

En PowerShell:

```powershell
$env:LLM_PROVIDER="ollama"
$env:OLLAMA_URL="http://localhost:11434"
py rag_answer.py
```

## Regenerar El Corpus

Cuando cambian los PDFs, los examenes, los scripts `.m` o la logica de chunking,
hay que ejecutar dos pasos.

### 1. Generar Chunks

```bash
python main_ingest.py
```

Salida:

```text
chunks_ddr.jsonl
```

### 2. Reconstruir ChromaDB

```bash
python build_vector_db.py
```

Salida:

```text
chroma_ddr/
```

Despues ya se puede volver a consultar:

```bash
LLM_PROVIDER=ollama python rag_answer.py
```

Con Docker Compose:

```bash
docker compose run --rm rag python main_ingest.py
docker compose run --rm rag python build_vector_db.py
docker compose run --rm -it rag python rag_answer.py
```

## Flujo De Trabajo Habitual

### Solo Consultar El Sistema

Usar este flujo si `chroma_ddr/` ya existe y esta actualizado:

```bash
docker compose up -d --build
docker compose exec ollama ollama pull gemma4
docker compose run --rm -it rag
```

### Actualizar Materiales

Usar este flujo si se han cambiado archivos de `materiales/`:

```bash
python main_ingest.py
python build_vector_db.py
LLM_PROVIDER=ollama python rag_answer.py
```

### Ejecutar Evaluaciones

Las evaluaciones viven en `pruebas/`. Guia completa:

```text
pruebas/pruebas.md
```

Comando basico:

```bash
cd pruebas
docker compose up -d --build
docker compose run --rm rag python evaluate_rag.py
```

Para las pruebas adicionales:

```bash
docker compose run --rm -e OPENAI_API_KEY rag python evaluate_rag_conjunto.py
```

## Variables De Entorno

| Variable | Valor por defecto | Uso |
|---|---|---|
| `CHROMA_PATH` | `./chroma_ddr` | Ruta de la base vectorial. |
| `OLLAMA_URL` | `http://ollama:11434` en Compose | URL del servidor Ollama. |
| `LLM_PROVIDER` | `ollama` en Docker Compose | Proveedor de generacion: `ollama` u `openai`. |
| `OLLAMA_MODEL` | `gemma4` | Modelo generador local. |
| `OPENAI_API_KEY` | vacio | Clave para usar `LLM_PROVIDER=openai`. No se guarda en git. |
| `OPENAI_MODEL` | `gpt-5-mini` | Modelo OpenAI si se usa proveedor OpenAI. |
| `TOKENIZERS_PARALLELISM` | `false` | Evita avisos de paralelismo de Transformers. |
| `TRANSFORMERS_VERBOSITY` | `error` | Reduce ruido de logs del modelo de embeddings. |

Por defecto Docker Compose fuerza `LLM_PROVIDER=ollama` para que el asistente
funcione sin claves externas. Si quieres usar OpenAI en la raiz:

```bash
docker compose run --rm \
  -e LLM_PROVIDER=openai \
  -e OPENAI_API_KEY \
  -e OPENAI_MODEL=gpt-5-mini \
  -it rag
```

## Tipos De Preguntas Soportadas

### Preguntas Conceptuales

```text
que es el dimensionado de redes
explica la redundancia en el diseno de topologias
diferencia entre distance vector y link state
```

### Preguntas Sobre Problemas

```text
explicame el ejercicio 2.1 de la relacion de problemas del tema 2
resuelve el problema 15 del tema 2
```

### Preguntas Sobre Examenes

```text
explicame el ejercicio 2 del examen de enero de 2024-2025
resuelve el ejercicio 3 del examen de febrero de 2024-2025
dame el script matlab asociado al ejercicio 6 del examen de febrero de 2025-2026
```

### Generacion De Examenes

```text
genera un examen nuevo de DDR
```

La generacion avanzada de examenes con solucionario se documenta y evalua dentro
de `pruebas/`, donde `rag_answer.py` usa `genera_examen.py`.

## Como Recupera Contexto

El asistente no hace solo una busqueda vectorial simple. Combina embeddings con
reglas especificas del dominio:

- deteccion de `tema N`
- deteccion de `ejercicio` o `problema`
- deteccion de convocatorias como `enero` o `febrero`
- deteccion de cursos academicos como `2024-2025`
- filtro por fuente (`teoria`, `problemas`, `examenes`)
- recuperacion de scripts `.m` asociados cuando la pregunta pide codigo
- mezcla de teoria relacionada con problemas o examenes cuando ayuda a explicar

Esto permite responder mejor a consultas donde el numero de ejercicio, el PDF o
la convocatoria son tan importantes como la similitud semantica.

## Salidas Importantes

| Ruta | Descripcion |
|---|---|
| `chunks_ddr.jsonl` | Fragmentos extraidos de los materiales. |
| `chroma_ddr/` | Base vectorial persistente del asistente principal. |
| `pruebas/tests/testset.json` | Testset usado para evaluacion. |
| `pruebas/resultados/` | Resultados de evaluaciones. |

## Problemas Habituales

### El asistente no arranca

Comprueba que la base vectorial existe:

```bash
dir chroma_ddr
```

Y que Ollama esta activo:

```bash
docker compose ps
```

### Ollama No Tiene El Modelo

Descargar el modelo configurado:

```bash
docker compose exec ollama ollama pull gemma4
```

Si cambias `OLLAMA_MODEL`, descarga ese modelo exacto.

### La Base Vectorial Esta Desactualizada

Si has cambiado `materiales/`, reconstruye:

```bash
python main_ingest.py
python build_vector_db.py
```

### Falla La Ingesta Con OCR

Revisa que Tesseract esta instalado y que `pytesseract` puede encontrar el
ejecutable. En Windows puede ser necesario ajustar la ruta en los chunkers.

### Docker No Ve Los Cambios En La Base

El servicio `rag` monta `./chroma_ddr` como volumen. Si reconstruyes la base en
local, vuelve a lanzar el contenedor:

```bash
docker compose run --rm -it rag
```

## Resumen Rapido

```bash
docker compose up -d --build
docker compose exec ollama ollama pull gemma4
docker compose run --rm -it rag
```

Si cambias los materiales:

```bash
python main_ingest.py
python build_vector_db.py
LLM_PROVIDER=ollama python rag_answer.py
```
