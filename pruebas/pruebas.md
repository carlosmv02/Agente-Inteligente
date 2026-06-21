# Carpeta `pruebas`

Esta carpeta contiene el entorno usado para probar, comparar y documentar el
comportamiento del sistema RAG de Diseno y Dimensionado de Redes (DDR). La idea
es que se pueda ejecutar en otra maquina sin reconstruir todo el corpus desde
cero cuando ya se dispone de la base vectorial `chroma_ddr`. En esta carpeta se
incluyen los scripts de evaluacion, el testset y los resultados generados. La
base `chroma_ddr/` es un artefacto generado y puede no estar versionada porque
esta ignorada por git.

El objetivo de estas pruebas es medir tres partes del sistema:

1. La recuperacion de contexto desde ChromaDB.
2. La calidad de la respuesta generada por distintos modelos y prompts.
3. El coste practico de cada configuracion: tiempo, longitud de contexto,
   longitud de respuesta y, opcionalmente, metricas RAGAS.

## Estructura

| Ruta | Contenido |
|---|---|
| `rag_answer.py` | Asistente interactivo RAG. Permite preguntar al sistema y generar examenes nuevos. |
| `genera_examen.py` | Logica auxiliar para generar examenes y solucionarios controlados. |
| `generate_testset.py` | Genera `tests/testset.json` a partir de la base vectorial. |
| `evaluate_rag.py` | Evaluacion base del pipeline RAG. |
| `evaluate_rag_prompt_1.py` | Evaluacion con prompt estricto. |
| `evaluate_rag_prompt_2.py` | Evaluacion con prompt pedagogico y citas. |
| `evaluate_rag_openai.py` | Ejecuta los tres prompts usando OpenAI como generador. |
| `evaluate_rag_sin_pistas.py` | Prueba de recuperacion sin usar pistas del testset. |
| `evaluate_rag_sin_contexto_pagina.py` | Ablacion del contexto adicional de pagina. |
| `evaluate_rag_top_k.py` | Comparacion de valores de `TOP_K`. |
| `evaluate_rag_conjunto.py` | Orquestador que ejecuta las tres pruebas adicionales anteriores. |
| `tests/testset.json` | Conjunto de preguntas y respuestas de referencia. |
| `resultados/` | Resultados de evaluaciones ya ejecutadas. |
| `chroma_ddr/` | Base de datos vectorial persistente usada por las pruebas. Es requerida para ejecutar, pero es un artefacto generado/no versionado. |
| `pruebas-adicionales/` | Carpeta opcional montada por Docker Compose para artefactos auxiliares locales. Puede no existir hasta que se use. |
| `Dockerfile` | Imagen del servicio RAG. |
| `docker-compose.yml` | Levanta Ollama y el contenedor de pruebas. |
| `requirements.txt` | Dependencias Python del entorno de pruebas. |

## Base Vectorial Requerida

Los scripts de evaluacion cargan siempre la coleccion `ddr_chunks` desde
`CHROMA_PATH`. Aunque se reutilicen resultados intermedios, `evaluate_rag.py`
inicializa ChromaDB al arrancar, asi que `chroma_ddr/` debe existir.

El `Dockerfile` de esta carpeta hace:

```dockerfile
COPY chroma_ddr ./chroma_ddr
```

Por tanto, antes de construir la imagen de pruebas debe existir
`pruebas/chroma_ddr/`. Si no existe, hay que regenerar o copiar la base desde la
raiz del repositorio.

Desde la raiz del repositorio, si `chunks_ddr.jsonl` ya existe:

```bash
python build_vector_db.py
```

Si se han cambiado materiales o no existe `chunks_ddr.jsonl`:

```bash
python main_ingest.py
python build_vector_db.py
```

Despues copia la base a la carpeta de pruebas.

En PowerShell, desde la raiz:

```powershell
New-Item -ItemType Directory -Force .\pruebas\chroma_ddr
Copy-Item -Recurse -Force .\chroma_ddr\* .\pruebas\chroma_ddr\
```

En Bash, desde la raiz:

```bash
mkdir -p pruebas/chroma_ddr
cp -r chroma_ddr/. pruebas/chroma_ddr/
```

Si se actualiza `pruebas/chroma_ddr/`, reconstruye la imagen `rag` para que el
contenedor use la nueva base:

```bash
cd pruebas
docker compose build rag
```


## Preparar El Entorno

Ejecutar los comandos desde esta carpeta:

```bash
cd pruebas
```

Construir y levantar los servicios:

```bash
docker compose up -d --build
```

Comprobar que los contenedores estan activos:

```bash
docker compose ps
```

Descargar los modelos locales que se usen:

```bash
docker compose exec ollama ollama pull gemma4
docker compose exec ollama ollama pull gemma4:e2b
docker compose exec ollama ollama pull mistral:7b
```

Descarga solo los modelos que vayas a ejecutar. Los resultados historicos de
`resultados/` incluyen ejecuciones con `gemma4:e2b`, `gemma4:e4b`,
`gemma4:latest`, `mistral:7b`, `qwen3:4b`, `qwen3:8b`, `llama3.1:8b` y
`gpt-5-mini`.

Si se van a ejecutar pruebas con OpenAI o RAGAS con juez OpenAI, hay que definir
la clave por variable de entorno. No debe guardarse ninguna clave real en el
repositorio.

En Bash:

```bash
export OPENAI_API_KEY="..."
```

En PowerShell:

```powershell
$env:OPENAI_API_KEY="..."
```

## Ejecutar El Asistente

Para usar el RAG de forma interactiva:

```bash
docker compose run --rm -it rag python rag_answer.py
```

Por defecto el contenedor usa:

| Variable | Valor por defecto |
|---|---|
| `LLM_PROVIDER` | `ollama` |
| `OLLAMA_MODEL` | `gemma4` |
| `OLLAMA_URL` | `http://ollama:11434` |
| `CHROMA_PATH` | `/app/chroma_ddr` |
| `OPENAI_MODEL` | `gpt-5-mini` |

Para usar OpenAI como generador:

```bash
docker compose run --rm \
  -e LLM_PROVIDER=openai \
  -e OPENAI_API_KEY \
  -e OPENAI_MODEL=gpt-5-mini \
  -it rag python rag_answer.py
```

El asistente tambien reconoce peticiones de generacion de examenes, por ejemplo:

```text
genera un examen nuevo con solucionario
```

Algunas variables utiles para controlar esa generacion son:

| Variable | Uso |
|---|---|
| `RAG_EXAM_SEED` | Fija una semilla para repetir el mismo examen. |
| `RAG_EXAM_PROFILE` | Selecciona un perfil teorico. |
| `RAG_EXAM_VARIANT` / `RAG_EXAM_SCENARIO` | Selecciona una variante de topologia para la pregunta 4. |
| `RAG_EXAM_DIMENSION` / `RAG_EXAM_DIMENSIONING` / `RAG_EXAM_DIMENSION_OPTION` | Selecciona la opcion de dimensionamiento de la pregunta 4. |
| `RAG_EXAM_FORCE_PROFILE` | Si vale `1`/`true`, fuerza las preguntas teoricas del banco interno. |
| `RAG_EXAM_ONLY_MAX_TOKENS` | Limite de tokens para examen sin solucionario. |
| `RAG_EXAM_SOLUTION_MAX_TOKENS` | Limite de tokens para solucionario. |
| `RAG_EXAM_WITH_SOLUTION_MAX_TOKENS` | Alias heredado para el limite del solucionario. |

## Testset

El testset principal esta en:

```text
tests/testset.json
```

Contiene preguntas, respuestas de referencia, contexto original y metadatos como
tema, tipo, PDF y pagina. Es importante no regenerarlo si se quieren comparar
resultados antiguos y nuevos, porque cambiar el testset cambia la base de la
comparacion.

Para regenerarlo desde ChromaDB:

```bash
docker compose run --rm \
  -e OLLAMA_MODEL=gemma4 \
  rag python generate_testset.py
```

Salida:

```text
tests/testset.json
```

## Evaluacion Base

La evaluacion base se lanza con:

```bash
docker compose run --rm rag python evaluate_rag.py
```

Por defecto:

- Usa `LLM_PROVIDER=ollama`.
- Usa `OLLAMA_MODEL=gemma4`, salvo que se indique otro.
- Lee `tests/testset.json`.
- Guarda resultados en `tests/`.
- No ejecuta RAGAS, porque `EVAL_RUN_RAGAS=0` por defecto.
- Reutiliza `tests/rag_pipeline_results.json` si ya existe y coincide con el
  modelo configurado.

Para forzar respuestas nuevas:

```bash
docker compose run --rm \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag.py
```

Para cambiar el modelo local:

```bash
docker compose run --rm \
  -e OLLAMA_MODEL=gemma4:e2b \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag.py
```

Para ejecutar tambien RAGAS con juez OpenAI:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  -e EVAL_RUN_RAGAS=1 \
  -e RAGAS_JUDGE_PROVIDER=openai \
  -e OPENAI_JUDGE_MODEL=gpt-5-mini \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag.py
```

## Ficheros De Resultado

Cada evaluacion genera, como minimo, estos ficheros:

| Fichero | Contenido |
|---|---|
| `rag_pipeline_results.json` | Resultado por pregunta: pregunta, respuesta, referencia, contextos recuperados, metadatos y tiempos. |
| `evaluation_summary.json` | Resumen numerico agregado. |
| `evaluation_summary.md` | Resumen legible y lista de peores respuestas por similitud. |
| `ragas_results.json` | Resultados RAGAS, solo si `EVAL_RUN_RAGAS=1`. |

Metricas rapidas incluidas en `evaluation_summary.json`:

| Campo | Significado |
|---|---|
| `avg_answer_ground_truth_similarity` | Similitud semantica media entre respuesta y referencia. |
| `avg_answer_context_similarity` | Similitud entre respuesta y contexto recuperado. |
| `avg_same_tema_ratio` | Proporcion media de chunks recuperados del tema esperado. |
| `avg_same_pdf_ratio` | Proporcion media de chunks del PDF esperado. |
| `same_page_hit_rate` | Frecuencia con la que se recupera la pagina esperada. |
| `avg_time_per_response_s` | Tiempo medio registrado por respuesta. |
| `avg_context_chars` | Longitud media del contexto usado. |
| `avg_answer_words` | Longitud media de las respuestas. |

Metricas RAGAS usadas cuando se activa RAGAS:

| Metrica | Que mide |
|---|---|
| `faithfulness` | Si la respuesta esta apoyada por el contexto. |
| `answer_relevancy` | Si la respuesta responde a la pregunta. |
| `context_precision` | Si los fragmentos recuperados son relevantes. |
| `context_recall` | Si el contexto contiene la informacion necesaria. |

## Prompts

Hay tres variantes de prompt:

| Prompt | Script | Descripcion | Salida por defecto |
|---|---|---|---|
| `prompt-0` | `evaluate_rag.py` | Prompt base. | `tests/` |
| `prompt-1` | `evaluate_rag_prompt_1.py` | Prompt estricto: responde solo si el contexto lo permite. | `resultados/<modelo>-prompt-1/` |
| `prompt-2` | `evaluate_rag_prompt_2.py` | Prompt pedagogico con citas. | `resultados/<modelo>-prompt-2/` |

Ejemplo con `prompt-2`:

```bash
docker compose run --rm \
  -e OLLAMA_MODEL=gemma4:e2b \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag_prompt_2.py
```

Para ejecutar los tres prompts con OpenAI:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  -e OPENAI_MODEL=gpt-5-mini \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag_openai.py
```

`evaluate_rag_openai.py` ejecuta `prompt-0` en `tests/` y despues copia esos
ficheros a `resultados/<modelo>-prompt-0/`. Los prompts 1 y 2 escriben
directamente en `resultados/<modelo>-prompt-1/` y
`resultados/<modelo>-prompt-2/`.

Con RAGAS:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  -e OPENAI_MODEL=gpt-5-mini \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  -e EVAL_RUN_RAGAS=1 \
  -e RAGAS_JUDGE_PROVIDER=openai \
  -e OPENAI_JUDGE_MODEL=gpt-5-mini \
  rag python evaluate_rag_openai.py
```

## Pruebas Adicionales

### Sin Pistas

Script:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_sin_pistas.py
```

Que hace:

- Desactiva `EVAL_USE_TESTSET_HINTS`.
- Evalua un escenario mas parecido a preguntas libres.
- Ejecuta:
  - `gemma4:e2b` + `prompt-0`
  - `mistral:7b` + `prompt-0`
  - `gemma4:e2b` + `prompt-2`
  - `mistral:7b` + `prompt-2`
- Activa RAGAS con juez OpenAI.

Salida:

```text
resultados/sin-pistas/gemma4-e2b-prompt-0/
resultados/sin-pistas/mistral-7b-prompt-0/
resultados/sin-pistas/gemma4-e2b-prompt-2/
resultados/sin-pistas/mistral-7b-prompt-2/
```

### Sin Contexto De Pagina

Script:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_sin_contexto_pagina.py
```

Que hace:

- Desactiva `EVAL_ATTACH_PAGE_CONTEXT`.
- Comprueba si anadir chunks de la misma pagina mejora realmente la respuesta.
- Ejecuta:
  - `gemma4:e2b` + `prompt-0`
  - `mistral:7b` + `prompt-0`
- Activa RAGAS con juez OpenAI.

Salida:

```text
resultados/sin-contexto-pagina/gemma4-e2b-prompt-0/
resultados/sin-contexto-pagina/mistral-7b-prompt-0/
```

### TOP_K

Script:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_top_k.py
```

Que hace:

- Cambia el numero de chunks recuperados con `EVAL_TOP_K`.
- Ejecuta `TOP_K=3` y `TOP_K=10`.
- Usa `gemma4:e2b` y `mistral:7b` con `prompt-0`.
- El caso `TOP_K=6` corresponde a la configuracion base.
- Activa RAGAS con juez OpenAI.

Salida:

```text
resultados/top-k/top-k-3/gemma4-e2b-prompt-0/
resultados/top-k/top-k-3/mistral-7b-prompt-0/
resultados/top-k/top-k-10/gemma4-e2b-prompt-0/
resultados/top-k/top-k-10/mistral-7b-prompt-0/
```

### Ejecucion Conjunta

Para lanzar las tres pruebas adicionales en secuencia:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_conjunto.py
```

Ejecuta, en orden:

1. `evaluate_rag_sin_pistas.py`
2. `evaluate_rag_sin_contexto_pagina.py`
3. `evaluate_rag_top_k.py`

El orquestador guarda un log y un resumen JSON en:

```text
resultados/conjunto/
```

Opciones utiles del orquestador:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_conjunto.py --desde top-k

docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_conjunto.py --solo sin-pistas --solo top-k

docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_conjunto.py --continuar-si-falla
```

## Variables De Entorno Utiles

| Variable | Valor habitual | Uso |
|---|---|---|
| `CHROMA_PATH` | `/app/chroma_ddr` | Ruta de la base ChromaDB con la coleccion `ddr_chunks`. |
| `LLM_PROVIDER` | `ollama` u `openai` | Selecciona proveedor del generador. |
| `OLLAMA_URL` | `http://ollama:11434` | URL del servidor Ollama. |
| `OLLAMA_MODEL` | `gemma4`, `gemma4:e2b`, `mistral:7b` | Modelo local. |
| `OPENAI_MODEL` | `gpt-5-mini` | Modelo OpenAI generador. |
| `OPENAI_API_KEY` | secreto local | Clave para OpenAI. No se guarda en git. |
| `OPENAI_REASONING_EFFORT` | `low` | Esfuerzo de razonamiento para modelos OpenAI que lo soportan. |
| `EVAL_TESTSET_FILE` | `tests/testset.json` | Testset a evaluar. |
| `EVAL_OUTPUT_DIR` | ruta | Carpeta de salida personalizada. |
| `EVAL_REUSE_RAW_RESULTS` | `1` o `0` | Reutiliza o regenera respuestas. |
| `EVAL_RUN_RAGAS` | `0` o `1` | Activa metricas RAGAS. |
| `EVAL_OPENAI_EMPTY_RETRY_MAX_TOKENS` | `4000` | Segundo intento si OpenAI devuelve respuesta sin texto visible. |
| `RAGAS_JUDGE_PROVIDER` | `ollama` u `openai` | Proveedor del juez RAGAS. |
| `OPENAI_JUDGE_MODEL` | `gpt-5-mini` | Modelo OpenAI usado como juez. |
| `OLLAMA_JUDGE_MODEL` | modelo local | Modelo Ollama usado como juez. |
| `RAGAS_METRICS` | lista separada por comas | Metricas RAGAS a ejecutar. |
| `RAGAS_TIMEOUT` | `1200` | Timeout por llamada RAGAS. |
| `RAGAS_MAX_WORKERS` | `1` o `2` | Paralelismo de RAGAS. |
| `RAGAS_MAX_RETRIES` | `3` | Reintentos maximos de RAGAS. |
| `RAGAS_SAMPLE_SIZE` | `0` | Si es mayor que 0, evalua RAGAS solo en una muestra. |
| `EVAL_TOP_K` / `TOP_K` | `6` | Numero de chunks recuperados. |
| `EVAL_USE_TESTSET_HINTS` | `1` | Usa metadatos del testset para filtrar recuperacion. |
| `EVAL_ATTACH_PAGE_CONTEXT` | `1` | Anade contexto adicional de la misma pagina. |
| `EVAL_MAX_OUTPUT_TOKENS` | `1200` o `2000` | Limite de generacion. |
| `TESTSET_MAX_RETRIES` | `3` | Reintentos al generar cada ejemplo del testset. |
| `TOKENIZERS_PARALLELISM` | `false` | Evita avisos de paralelismo de Transformers. |
| `TRANSFORMERS_VERBOSITY` | `error` | Reduce ruido de logs de Transformers. |

## Problemas Habituales

### Falla `COPY chroma_ddr`

Si `docker compose build` falla porque no encuentra `chroma_ddr`, crea o copia
primero `pruebas/chroma_ddr/` siguiendo la seccion **Base Vectorial Requerida**.

### No Existe La Coleccion `ddr_chunks`

Significa que `CHROMA_PATH` apunta a una carpeta vacia o a una base incorrecta.
Regenera la base, copiala a `pruebas/chroma_ddr/` y reconstruye la imagen.

### Falta `OPENAI_API_KEY`

Las pruebas con generador OpenAI o RAGAS con juez OpenAI necesitan pasar la clave
al contenedor:

```bash
docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag.py
```

### Se Reutilizan Resultados Antiguos

`evaluate_rag.py` reutiliza `rag_pipeline_results.json` si coincide el proveedor,
el modelo y el testset. Para regenerar respuestas, usa:

```bash
docker compose run --rm \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag.py
```

## Ejecutar Pruebas Largas

En un servidor remoto conviene usar `screen` o `tmux` para no perder la ejecucion
si se corta la conexion SSH.

Ejemplo con `screen`:

```bash
screen -S rag_eval
cd /ruta/al/repositorio/pruebas
docker compose run --rm -e OPENAI_API_KEY rag python evaluate_rag_conjunto.py
```

Para desconectarse sin parar la prueba:

```text
Ctrl + A
D
```

Para volver:

```bash
screen -r rag_eval
```

## Orden Recomendado

Para reproducir las pruebas principales desde cero:

1. Levantar entorno y descargar modelos.
2. Comprobar que existe `tests/testset.json`.
3. Ejecutar evaluaciones base de los modelos finalistas.
4. Ejecutar `prompt-1` y `prompt-2` si se quieren comparar prompts.
5. Ejecutar `evaluate_rag_conjunto.py` para las pruebas adicionales.
6. Revisar `evaluation_summary.json`, `evaluation_summary.md` y `ragas_results.json`.
7. Comparar calidad, tiempo y recuperacion antes de seleccionar configuracion final.

Comandos resumidos:

```bash
docker compose up -d --build
docker compose exec ollama ollama pull gemma4:e2b
docker compose exec ollama ollama pull mistral:7b

docker compose run --rm \
  -e OLLAMA_MODEL=gemma4:e2b \
  -e EVAL_OUTPUT_DIR=resultados/gemma4-e2b-prompt-0 \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag.py

docker compose run --rm \
  -e OLLAMA_MODEL=mistral:7b \
  -e EVAL_OUTPUT_DIR=resultados/mistral-7b-prompt-0 \
  -e EVAL_REUSE_RAW_RESULTS=0 \
  rag python evaluate_rag.py

docker compose run --rm \
  -e OPENAI_API_KEY \
  rag python evaluate_rag_conjunto.py
```
