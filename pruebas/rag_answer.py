import os
import re
import json
import sys
import logging
import unicodedata
import requests
import chromadb
from sentence_transformers import SentenceTransformer, util

import genera_examen

try:
    import termios
    import tty
except ImportError:
    termios = None
    tty = None

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)


CHROMA_PATH     = os.environ.get("CHROMA_PATH", "./chroma_ddr")
COLLECTION_NAME = "ddr_chunks"
EMBED_MODEL_NAME = "intfloat/multilingual-e5-base"
OLLAMA_MODEL    = os.environ.get("OLLAMA_MODEL", "gemma4")
OLLAMA_URL      = os.environ.get("OLLAMA_URL", "http://ollama:11434")
LLM_PROVIDER    = os.environ.get("LLM_PROVIDER", "openai").lower()
OPENAI_MODEL    = os.environ.get("OPENAI_MODEL", "gpt-5-mini")
OPENAI_REASONING_EFFORT = os.environ.get("OPENAI_REASONING_EFFORT", "low").strip()
EXAM_WITH_SOLUTION_MAX_TOKENS = int(os.environ.get("RAG_EXAM_WITH_SOLUTION_MAX_TOKENS", "6000"))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
DEBUG_PRINT_CONTEXT = False

print("Cargando modelo de embeddings...")
embed_model = SentenceTransformer(EMBED_MODEL_NAME)

client     = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(COLLECTION_NAME)

print("RAG listo")
print("- Vector DB:", CHROMA_PATH)
print("- Embeddings:", EMBED_MODEL_NAME)
print("- LLM provider:", LLM_PROVIDER)
if LLM_PROVIDER == "openai":
    print("- OpenAI model:", OPENAI_MODEL)
else:
    print("- Ollama model:", OLLAMA_MODEL)
print("Escribe una pregunta y pulsa Enter. Escribe 'exit' para salir.\n")


def infer_response_budget(question: str, context: str) -> int:
    q = question.lower()

    exam_budget = genera_examen.response_budget(question)
    if exam_budget is not None:
        return exam_budget

    if is_exam_generation_request(question):
        return 3000

    if re.search(r"\b(\d+\.\d+)\b", q):
        return 2000
    if re.search(r"(?:ejercicio|problema)\s+\d+", q):
        return 2000
    if any(w in q for w in [
        "resuelve", "resolver", "calcula", "calcular", "dimensiona",
        "dimensionar", "diseña", "diseñar", "justifica", "desarrolla",
        "explica paso a paso", "paso a paso", "problema", "ejercicio"
    ]):
        return 2000
    if any(w in q for w in [
        "compara", "diferencia", "relaciona", "ventajas", "inconvenientes",
        "analiza", "razona"
    ]):
        return 1200
    if any(w in q for w in [
        "resume", "resumen", "explica", "descripción", "descripcion"
    ]):
        return 1200
    if any(w in q for w in [
        "qué es", "que es", "define", "definición", "definicion",
        "enumera", "lista"
    ]):
        return 500

    context_len = len(context.split())
    if context_len > 1200:
        return 1400
    if context_len > 700:
        return 1000
    return 800


def is_conceptual_question(question: str) -> bool:
    q = _normalize_text(question)

    if is_exam_generation_request(question):
        return False

    if any(token in q for token in [
        "resuelve", "resolver", "calcula", "calcular", "dimensiona", "dimensionar",
        "disena", "disenar", "problema", "ejercicio", "paso a paso", "formulacion",
        "matriz de trafico", "octave", "matlab", "script"
    ]):
        return False

    return any(token in q for token in [
        "que es", "explica", "explicame", "define", "definicion",
        "diferencia", "compara", "ventajas", "inconvenientes",
        "por que", "para que"
    ])


def looks_incomplete(text: str) -> bool:
    if not text:
        return True
    stripped = text.rstrip()
    if stripped.count("```") % 2 == 1:
        return True
    if stripped.endswith((":", ",", ";", "(", "[", "{", "-")):
        return True
    return stripped[-1] not in ".!?»\"'"


def build_prompt(question: str, context: str, continuation: bool = False, partial_answer: str = "") -> str:
    if not continuation:
        if is_exam_generation_request(question):
            return genera_examen.build_exam_prompt(
                question,
                context,
                include_solution=is_exam_generation_with_solution_request(question),
            )

        if is_exam_generation_request(question):
            return f"""
Eres un asistente experto en Diseno y Dimensionado de Redes (DDR).

Tu tarea es redactar un examen nuevo a partir del CONTEXTO.

REGLAS:
1) Devuelve solo el enunciado del examen, nunca la solucion.
2) El examen debe tener exactamente 4 preguntas numeradas del 1 al 4.
3) Las preguntas 1, 2 y 3 deben ser teoricas o de razonamiento breve, con estilo similar al de los examenes reales.
4) La pregunta 4 debe ser el ejercicio practico largo del examen y debe requerir entregar un archivo `.m`.
5) La pregunta 4 NO puede ser genérica: debe incluir una topologia concreta, una matriz de trafico o datos de entrada equivalentes, varias opciones tipo OPC y la referencia a entregar un `.m`, como en los examenes reales.
6) La pregunta 4 debe pedir formulacion matematica abstracta y solucion programada, no simplemente "simular una red".
7) No escribas el codigo `.m` ni una solucion ejemplo.
8) Reparte la puntuacion de forma verosimil.
9) No uses bloques de codigo.
10) No expliques tus decisiones ni anadas comentarios fuera del examen.
11) Termina el examen completamente, sin dejar frases a medias.
12) La pregunta 4 debe seguir exactamente la plantilla obligatoria incluida abajo.
13) No generes examenes personalizados por DNI ni variantes dependientes del alumno.

CONTEXTO:
{context}

{exam_question_4_template()}

PETICION:
{question}
""".strip()
        return f"""
Eres un asistente experto en Diseño y Dimensionado de Redes (DDR).

REGLAS:
1) Usa el CONTEXTO como única fuente de hechos concretos.
2) No inventes enunciados, datos, topologías, valores, resultados ni pasos que no estén en el CONTEXTO.
3) Si el CONTEXTO no contiene suficiente información, dilo explícitamente.
4) Si faltan datos para cerrar un resultado numérico, indícalo claramente.
5) Si la pregunta es conceptual, responde de forma concisa y clara.
6) Si la pregunta es de ejercicio o problema, responde de forma desarrollada, estructurada y completa.
7) Termina siempre con frases cerradas y completas.
8) Ajusta la longitud a la pregunta: breve si es una definición; amplia si es un ejercicio o razonamiento.

9) Si el contexto muestra varias ocurrencias del mismo ejercicio dentro de un examen, no las mezcles: indica que la consulta es ambigua y separalas.

CONTEXTO:
{context}

PREGUNTA:
{question}
""".strip()

    return f"""Continúa la siguiente respuesta incompleta.
NO repitas lo ya escrito. Retoma desde la última frase incompleta y cierra la explicación.

CONTEXTO:
{context}

RESPUESTA INCOMPLETA:
{partial_answer}

CONTINUACIÓN:""".strip()


def call_ollama_stream(prompt: str, num_predict: int, print_tokens: bool = False) -> dict:
    """Llama a Ollama en modo stream. Si print_tokens=True imprime cada token en tiempo real."""
    url     = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.0,
            "num_predict": num_predict,
            "num_thread": 12,
            "num_ctx": 8192,
            "num_batch": 512,
        }
    }

    r = requests.post(url, json=payload, stream=True, timeout=600)
    if not r.ok:
        raise RuntimeError(f"ERROR llamando a Ollama: {r.status_code} {r.reason}: {r.text}")

    full_response = ""
    last_data     = {}

    for line in r.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        token = chunk.get("response", "")
        full_response += token

        if print_tokens and token:
            print(token, end="", flush=True)

        last_data = chunk

    last_data["response"] = full_response
    return last_data


def _extract_openai_text(response) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()

    parts = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def call_openai(prompt: str, num_predict: int, print_tokens: bool = False) -> dict:
    """Llama a OpenAI usando la API key definida en OPENAI_API_KEY."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Define OPENAI_API_KEY para usar LLM_PROVIDER=openai.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "Falta la dependencia 'openai'. Reconstruye la imagen Docker con: docker compose build rag"
        ) from exc

    client = OpenAI()
    request = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "max_output_tokens": num_predict,
    }
    if OPENAI_MODEL.startswith(("gpt-5", "o")) and OPENAI_REASONING_EFFORT:
        request["reasoning"] = {"effort": OPENAI_REASONING_EFFORT}

    response = client.responses.create(**request)
    text = _extract_openai_text(response)

    if not text:
        status = getattr(response, "status", None)
        incomplete_details = getattr(response, "incomplete_details", None)
        raise RuntimeError(
            "OpenAI devolvio una respuesta sin texto. "
            f"status={status}, incomplete_details={incomplete_details}, "
            f"response_id={getattr(response, 'id', None)}"
        )

    if print_tokens and text:
        print(text, end="", flush=True)

    return {
        "response": text,
        "done_reason": "stop",
        "model": OPENAI_MODEL,
    }


def call_llm(prompt: str, num_predict: int, print_tokens: bool = False) -> dict:
    if LLM_PROVIDER == "ollama":
        return call_ollama_stream(prompt, num_predict, print_tokens=print_tokens)
    if LLM_PROVIDER == "openai":
        return call_openai(prompt, num_predict, print_tokens=print_tokens)
    raise ValueError(f"LLM_PROVIDER no soportado: {LLM_PROVIDER}")


def ask_llm_streaming(question: str, context: str) -> str:
    """Genera la respuesta con streaming visible. Las continuaciones no se imprimen token a token
    para evitar confusión, pero sí se acumulan correctamente."""
    base_budget = infer_response_budget(question, context)

    try:
        if is_exam_generation_request(question):
            print("\nRESPUESTA:\n", flush=True)
            answer = genera_examen.generate_exam_answer(
                question=question,
                context=context,
                call_llm=call_llm,
                print_tokens=True,
            )
            print("\n", flush=True)
            return answer

        prompt = build_prompt(question, context)

        print("\nRESPUESTA:\n", flush=True)
        data = call_llm(prompt, base_budget, print_tokens=True)

        answer      = (data.get("response") or "").strip()
        done_reason = data.get("done_reason", "")

        max_continuations = 1 if is_exam_generation_request(question) else 2
        continuation_budget = max(300, base_budget // 2)

        for _ in range(max_continuations):
            if done_reason not in ("length", "max_tokens"):
                break
            if not looks_incomplete(answer):
                break

            # Continuación: imprime también en streaming
            cont_prompt = build_prompt(
                question=question,
                context=context,
                continuation=True,
                partial_answer=answer
            )
            data_cont   = call_llm(cont_prompt, continuation_budget, print_tokens=True)
            extra       = (data_cont.get("response") or "").strip()
            done_reason = data_cont.get("done_reason", "")

            if not extra:
                break

            answer = (answer.rstrip() + "\n" + extra.lstrip()).strip()

            if done_reason not in ("length", "max_tokens") and not looks_incomplete(answer):
                break

        # Salto de línea final tras el stream
        print("\n", flush=True)
        return answer

    except Exception as e:
        print(flush=True)
        return f"ERROR llamando al modelo {LLM_PROVIDER}: {e}"


def _format_blocks(docs, metas) -> str:
    blocks = []
    for doc, meta in zip(docs, metas):
        pagina    = meta.get("pagina", meta.get("pagina_inicio", "-"))
        ejercicio = meta.get("ejercicio", "-")
        ocurrencia = meta.get("ejercicio_ocurrencia")
        ocurrencia_str = f" ({ocurrencia})" if ocurrencia else ""
        blocks.append(
            f"[Fuente: {meta.get('fuente')} | PDF: {meta.get('pdf')} | "
            f"Tema: {meta.get('tema')} | Página: {pagina} | Ej: {ejercicio}]"
            f" | Occ: {ocurrencia_str.strip(' ()') if ocurrencia else '-'}]"
            f"\n{doc}"
        )
    return "\n\n".join(blocks)


def _normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def is_exam_generation_request(question: str) -> bool:
    return genera_examen.is_exam_generation_request(question)


def is_exam_generation_with_solution_request(question: str) -> bool:
    return genera_examen.is_exam_generation_with_solution_request(question)


def exam_question_4_template(include_solution: bool = False) -> str:
    return genera_examen.exam_question_4_template(include_solution=include_solution)


def _apply_backspaces(text: str) -> str:
    cleaned = []
    for ch in text:
        if ch in ("\b", "\x7f"):
            if cleaned:
                cleaned.pop()
        else:
            cleaned.append(ch)
    return "".join(cleaned)


def _read_question(prompt: str = "PREGUNTA: ") -> str:
    if not sys.stdin.isatty() or termios is None or tty is None:
        return _apply_backspaces(input(prompt))

    sys.stdout.write(prompt)
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    chars = []

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)

            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                break

            if ch in ("\x03",):
                sys.stdout.write("^C\n")
                sys.stdout.flush()
                raise KeyboardInterrupt

            if ch in ("\x04",):
                sys.stdout.write("\n")
                sys.stdout.flush()
                return "exit"

            if ch in ("\b", "\x7f"):
                if chars:
                    chars.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            if ch.isprintable() or ch == " ":
                chars.append(ch)
                sys.stdout.write(ch)
                sys.stdout.flush()

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return "".join(chars)


def _detect_query_filters(query: str):
    q              = _normalize_text(query)
    tema           = None
    ejercicio      = None
    prefer_pdf     = None
    convocatoria   = None
    curso_academico = None
    es_examen      = False

    m_tema = re.search(r"\btema\s+(\d+)\b", q)
    if m_tema:
        tema = f"Tema {m_tema.group(1)}"

    m_decimal = re.search(r"\b(\d+\.\d+)\b", q)
    if m_decimal:
        ejercicio = m_decimal.group(1)

    m_simple = re.search(r"\b(?:ejercicio|problema)\s+(\d+)\b", q)
    if ejercicio is None and m_simple:
        ejercicio = m_simple.group(1)

    m_conv = re.search(r"\b(enero|febrero)\b", q)
    if m_conv:
        convocatoria = m_conv.group(1)

    m_curso = re.search(r"\b(20\d{2})\s*[-/]\s*(20\d{2})\b", q)
    if m_curso:
        curso_academico = f"{m_curso.group(1)}-{m_curso.group(2)}"

    if re.search(r"\bexamen(?:es)?\b", q) or convocatoria or curso_academico:
        es_examen = True

    if re.search(r"\bii\b", q, flags=re.IGNORECASE):
        prefer_pdf = "problemas_tema2_II.pdf"

    return {
        "ejercicio": ejercicio,
        "tema": tema,
        "prefer_pdf": prefer_pdf,
        "es_examen": es_examen,
        "convocatoria": convocatoria,
        "curso_academico": curso_academico,
    }


def _query_problem_chunks(ejercicio: str, tema: str = None, prefer_pdf: str = None):
    where_clauses = [{"fuente": "problemas"}, {"ejercicio": ejercicio}]
    if tema:
        where_clauses.append({"tema": tema})

    data  = collection.get(where={"$and": where_clauses})
    docs  = data.get("documents", []) or []
    metas = data.get("metadatas", []) or []

    if not docs:
        return [], []

    paired = list(zip(docs, metas))

    if prefer_pdf:
        preferred = [(d, me) for d, me in paired if me.get("pdf") == prefer_pdf]
        if preferred:
            paired = preferred

    paired.sort(key=lambda x: (
        x[1].get("subchunk_index", 0),
        x[1].get("pagina_inicio", x[1].get("pagina", 0))
    ))

    return [d for d, _ in paired], [m for _, m in paired]


def _query_exam_chunks(
    query: str,
    ejercicio: str = None,
    convocatoria: str = None,
    curso_academico: str = None,
    top_k_code: int = 2,
):
    q_norm = _normalize_text(query)
    wants_code = any(word in q_norm for word in ["matlab", "octave", "codigo", "script", ".m"])

    base_where = {"$and": [{"fuente": "examenes"}, {"tipo": "examen"}]}
    if convocatoria and curso_academico:
        base_where = {
            "$and": [
                {"fuente": "examenes"},
                {"tipo": "examen"},
                {"convocatoria": convocatoria},
                {"curso_academico": curso_academico},
            ]
        }
    elif convocatoria:
        base_where = {
            "$and": [
                {"fuente": "examenes"},
                {"tipo": "examen"},
                {"convocatoria": convocatoria},
            ]
        }
    elif curso_academico:
        base_where = {
            "$and": [
                {"fuente": "examenes"},
                {"tipo": "examen"},
                {"curso_academico": curso_academico},
            ]
        }

    q_emb = embed_model.encode(query).tolist()
    res = collection.query(query_embeddings=[q_emb], n_results=24, where=base_where)
    docs = res.get("documents", [[]])[0] or []
    metas = res.get("metadatas", [[]])[0] or []

    if not docs:
        return [], []

    paired = list(zip(docs, metas))

    if ejercicio:
        exact_ex = [(d, m) for d, m in paired if str(m.get("ejercicio", "")) == str(ejercicio)]
        if exact_ex:
            paired = exact_ex

    paired.sort(key=lambda x: (
        x[1].get("pagina_inicio", x[1].get("pagina", 0) or 0),
        x[1].get("subchunk_index", 0)
    ))

    exam_id = None
    if paired:
        exam_id = paired[0][1].get("examen_id")
    if not exam_id and convocatoria and curso_academico:
        exam_id = f"{convocatoria}-{curso_academico}"

    code_docs = []
    code_metas = []

    if exam_id and (wants_code or ejercicio):
        code_res = collection.query(
            query_embeddings=[q_emb],
            n_results=top_k_code * 3,
            where={
                "$and": [
                    {"fuente": "examenes"},
                    {"tipo": "codigo_examen"},
                    {"examen_id": exam_id},
                ]
            }
        )
        raw_code_docs = code_res.get("documents", [[]])[0] or []
        raw_code_metas = code_res.get("metadatas", [[]])[0] or []

        if raw_code_docs:
            filtered_code = list(zip(raw_code_docs, raw_code_metas))
            if ejercicio:
                exact_code = [
                    (d, m) for d, m in filtered_code
                    if str(m.get("ejercicio_relacionado", "")) == str(ejercicio)
                ]
                if exact_code:
                    filtered_code = exact_code
                elif not wants_code:
                    filtered_code = []
            elif not wants_code:
                filtered_code = []

            raw_code_docs = [d for d, _ in filtered_code]
            raw_code_metas = [m for _, m in filtered_code]

        if raw_code_docs:
            d_embs = embed_model.encode(raw_code_docs, normalize_embeddings=True)
            q_emb_norm = embed_model.encode(query, normalize_embeddings=True)
            scores = util.cos_sim(q_emb_norm, d_embs)[0].tolist()
            ranked = sorted(zip(scores, raw_code_docs, raw_code_metas), key=lambda x: x[0], reverse=True)
            code_docs = [d for _, d, _ in ranked[:top_k_code]]
            code_metas = [m for _, _, m in ranked[:top_k_code]]

    return [d for d, _ in paired] + code_docs, [m for _, m in paired] + code_metas


def _query_related_theory(query: str, tema: str = None, top_k: int = 3):
    if is_conceptual_question(query):
        print("[DEBUG] Consulta conceptual detectada. Priorizando teoria.", flush=True)
        docs_c, metas_c = _query_conceptual_context(query=query, tema=tema, top_k=min(top_k, 4))
        if docs_c:
            return _format_blocks(docs_c, metas_c)

    q_emb        = embed_model.encode(query).tolist()
    where_filter = {"fuente": "teoria"}
    if tema:
        where_filter = {"$and": [{"fuente": "teoria"}, {"tema": tema}]}

    res     = collection.query(query_embeddings=[q_emb], n_results=top_k * 4, where=where_filter)
    docs_t  = res["documents"][0][:top_k]
    metas_t = res["metadatas"][0][:top_k]
    return docs_t, metas_t


def _conceptual_noise_score(doc: str) -> tuple[int, int, int]:
    text = (doc or "").lower()
    symbol_count = sum(text.count(token) for token in ["\\", "=", "<=", ">=", "x_{", "arg min", "s.a.", "min "])
    digit_count = sum(ch.isdigit() for ch in text)
    explanatory_hits = sum(
        token in text for token in [
            "se define", "consiste", "es un", "permite", "objetivo",
            "ventaja", "inconveniente", "caracterizacion", "dimensionado",
            "redundancia", "encaminamiento", "topologia"
        ]
    )
    return (symbol_count, digit_count, -explanatory_hits)


def _query_conceptual_context(query: str, tema: str = None, top_k: int = 4):
    q_emb = embed_model.encode(query, normalize_embeddings=True)

    where_filter = {"fuente": "teoria"}
    if tema:
        where_filter = {"$and": [{"fuente": "teoria"}, {"tema": tema}]}

    res = collection.query(
        query_embeddings=[q_emb.tolist()],
        n_results=max(top_k * 4, 12),
        where=where_filter
    )
    docs = res.get("documents", [[]])[0] or []
    metas = res.get("metadatas", [[]])[0] or []
    if not docs:
        return [], []

    d_embs = embed_model.encode(docs, normalize_embeddings=True)
    scores = util.cos_sim(q_emb, d_embs)[0].tolist()
    ranked = sorted(
        zip(scores, docs, metas),
        key=lambda x: (-x[0],) + _conceptual_noise_score(x[1])
    )

    selected = ranked[:top_k]
    return [d for _, d, _ in selected], [m for _, _, m in selected]


def _looks_too_symbolic(text: str) -> bool:
    if not text:
        return False
    markers = ["\\(", "\\)", "\\[", "\\]", "x_{", "<=", ">=", "arg min"]
    hits = sum(text.count(token) for token in markers)
    return hits >= 3


def _refine_conceptual_answer(question: str, context: str, answer: str) -> str:
    if not is_conceptual_question(question):
        return _refine_conceptual_answer(question, context, answer)
    if not _looks_too_symbolic(answer):
        return answer

    prompt = f"""Reescribe la siguiente RESPUESTA para que sea mas pedagogica y natural.

REGLAS:
1) Mantén el contenido fiel al CONTEXTO.
2) Empieza con una definicion breve.
3) Explica la idea intuitiva con lenguaje natural.
4) Evita formulas, notacion matematica y variables salvo una mencion muy breve si aporta valor.
5) No anadas informacion nueva.
6) Mantén la respuesta clara y compacta.

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA ORIGINAL:
{answer}
""".strip()

    refined = call_llm(prompt, num_predict=700, print_tokens=False).get("response", "").strip()
    return refined or answer


def _query_exam_generation_context() -> str:
    where_filter = {"$and": [{"fuente": "examenes"}, {"tipo": "examen"}]}

    q_theory = "pregunta teorica breve de examen de ddr"
    q_practical = "ejercicio practico de examen ddr topologia matriz de trafico OPC script octave m"

    res_theory = collection.query(
        query_embeddings=[embed_model.encode(q_theory).tolist()],
        n_results=20,
        where=where_filter,
    )
    theory_docs = res_theory.get("documents", [[]])[0] or []
    theory_metas = res_theory.get("metadatas", [[]])[0] or []

    theory_pairs = []
    for doc, meta in zip(theory_docs, theory_metas):
        text = (doc or "").lower()
        if any(token in text for token in ["opc 1", "opc 2", "usar ej", "ver solución", "ver solucion", "octave", "matriz de tráfico", "matriz de trafico"]):
            continue
        if len((doc or "").split()) > 220:
            continue
        theory_pairs.append((doc, meta))
        if len(theory_pairs) >= 6:
            break

    res_practical = collection.query(
        query_embeddings=[embed_model.encode(q_practical).tolist()],
        n_results=20,
        where=where_filter,
    )
    practical_docs = res_practical.get("documents", [[]])[0] or []
    practical_metas = res_practical.get("metadatas", [[]])[0] or []

    practical_pairs = []
    for doc, meta in zip(practical_docs, practical_metas):
        text = (doc or "").lower()
        if any(token in text for token in ["opc 1", "opc 2", "usar ej", "ver solución", "ver solucion", "octave", "matriz de tráfico", "matriz de trafico"]):
            practical_pairs.append((doc, meta))
        if len(practical_pairs) >= 4:
            break

    parts = []
    if theory_pairs:
        parts.append("[PATRON PREGUNTAS BREVES]\n" + _format_blocks(
            [d for d, _ in theory_pairs],
            [m for _, m in theory_pairs]
        ))
    if practical_pairs:
        parts.append("[PATRON EJERCICIO FINAL]\n" + _format_blocks(
            [d for d, _ in practical_pairs],
            [m for _, m in practical_pairs]
        ))

    return "\n\n".join(parts)


def retrieve_context(query: str, top_k: int = 6) -> str:
    print("[DEBUG] Iniciando retrieve_context...", flush=True)

    top_k_ej     = 4
    top_k_teoria = 2

    filters = _detect_query_filters(query)
    ejercicio = filters["ejercicio"]
    tema = filters["tema"]
    prefer_pdf = filters["prefer_pdf"]
    es_examen = filters["es_examen"]
    convocatoria = filters["convocatoria"]
    curso_academico = filters["curso_academico"]

    if tema:
        print(f"[DEBUG] Tema detectado: {tema}", flush=True)

    if es_examen:
        print(f"[DEBUG] Consulta de examen detectada: True", flush=True)
    if convocatoria:
        print(f"[DEBUG] Convocatoria detectada: {convocatoria}", flush=True)
    if curso_academico:
        print(f"[DEBUG] Curso detectado: {curso_academico}", flush=True)

    if es_examen:
        if is_exam_generation_request(query):
            return _query_exam_generation_context()

        docs, metas = _query_exam_chunks(
            query=query,
            ejercicio=ejercicio,
            convocatoria=convocatoria,
            curso_academico=curso_academico,
        )

        if docs:
            ambiguity_note = ""
            if ejercicio:
                occurrences = sorted({
                    m.get("ejercicio_ocurrencia")
                    for m in metas
                    if str(m.get("ejercicio", "")) == str(ejercicio) and m.get("ejercicio_ocurrencia")
                })
                if len(occurrences) > 1:
                    ambiguity_note = (
                        "[AVISO]\n"
                        f"En este examen hay varias ocurrencias del ejercicio {ejercicio}: "
                        f"{', '.join(map(str, occurrences))}. "
                        "No deben mezclarse en una sola respuesta. "
                        "Si la pregunta no especifica cual, primero indica la ambiguedad y "
                        "resume cada ocurrencia por separado.\n\n"
                    )

            q_emb = embed_model.encode(query, normalize_embeddings=True)
            d_embs = embed_model.encode(docs, normalize_embeddings=True)
            scores = util.cos_sim(q_emb, d_embs)[0].tolist()
            ranked = sorted(
                zip(scores, docs, metas),
                key=lambda x: (
                    0 if (ejercicio and str(x[2].get("ejercicio", "")) == str(ejercicio)) else 1,
                    x[2].get("ejercicio_ocurrencia", 0),
                    x[2].get("pagina_inicio", x[2].get("pagina", 0) or 0),
                    -x[0],
                )
            )

            docs_e = [d for _, d, _ in ranked[:top_k]]
            metas_e = [me for _, _, me in ranked[:top_k]]
            return ambiguity_note + _format_blocks(docs_e, metas_e)

        print("[DEBUG] No se encontraron chunks de examen exactos. Busqueda general.", flush=True)

    if ejercicio:
        print(f"[DEBUG] Ejercicio detectado: {ejercicio}", flush=True)
        print(f"[DEBUG] PDF preferido: {prefer_pdf}", flush=True)

        docs, metas = _query_problem_chunks(ejercicio=ejercicio, tema=tema, prefer_pdf=prefer_pdf)

        if docs:
            q_emb  = embed_model.encode(query, normalize_embeddings=True)
            d_embs = embed_model.encode(docs, normalize_embeddings=True)
            scores = util.cos_sim(q_emb, d_embs)[0].tolist()
            ranked = sorted(zip(scores, docs, metas), key=lambda x: x[0], reverse=True)

            docs_p  = [d for _, d, _ in ranked[:top_k_ej]]
            metas_p = [me for _, _, me in ranked[:top_k_ej]]

            docs_t, metas_t = _query_related_theory(query=query, tema=tema, top_k=top_k_teoria)

            context = _format_blocks(docs_p, metas_p)
            if docs_t:
                context += "\n\n" + _format_blocks(docs_t, metas_t)
            return context

        print("[DEBUG] No se encontraron chunks exactos. Búsqueda general.", flush=True)

    print("[DEBUG] Búsqueda semántica normal", flush=True)
    q_emb        = embed_model.encode(query).tolist()
    where_filter = {"tema": tema} if tema else None

    if tema:
        print(f"[DEBUG] Filtrando semánticamente por tema: {tema}", flush=True)

    res   = collection.query(query_embeddings=[q_emb], n_results=top_k, where=where_filter)
    docs  = res["documents"][0]
    metas = res["metadatas"][0]
    return _format_blocks(docs, metas)


# ── Bucle principal ────────────────────────────────────────────────────────────
while True:
    try:
        question = _read_question("PREGUNTA: ").strip()
    except KeyboardInterrupt:
        print("Saliendo...")
        break

    if question.lower() == "exit":
        break

    print("[*] Recuperando contexto de la base de datos...", flush=True)
    context = retrieve_context(question)
    print("[+] Contexto recuperado", flush=True)

    if DEBUG_PRINT_CONTEXT:
        print("\n===== CONTEXTO RECUPERADO =====\n")
        print(context)
        print("\n===============================\n")

    print("[*] Generando respuesta...", flush=True)
    answer = ask_llm_streaming(question, context)

    print("=" * 60 + "\n")
