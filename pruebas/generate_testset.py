"""
generate_testset.py
-------------------
Genera un dataset de preguntas+respuestas de referencia a partir de los chunks
almacenados en ChromaDB, usando Ollama como LLM generador.

Uso:
    python generate_testset.py

Salida:
    tests/testset.json  -- lista de {question, ground_truth, context, tema}
"""

import json
import os
import random
import re
import unicodedata
from pathlib import Path

import chromadb
import requests

# Configuracion
BASE_DIR        = Path(__file__).resolve().parent
CHROMA_PATH     = os.environ.get("CHROMA_PATH", str(BASE_DIR / "chroma_ddr"))
COLLECTION_NAME = "ddr_chunks"
OLLAMA_URL      = os.environ.get("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL    = os.environ.get("OLLAMA_MODEL", "gemma4")
TESTS_DIR       = BASE_DIR / "tests"
OUTPUT_FILE     = TESTS_DIR / "testset.json"
MAX_RETRIES     = int(os.environ.get("TESTSET_MAX_RETRIES", "3"))

# Cuantas preguntas generar por tema y tipo
N_PER_TEMA      = 4   # preguntas conceptuales por tema
N_EJERCICIOS    = 6   # preguntas sobre ejercicios (total)
TEMAS           = ["Tema 1", "Tema 2", "Tema 3", "Tema 4", "Tema 5"]


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_for_match(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def is_low_quality_chunk(text: str, fuente: str) -> bool:
    """Descarta chunks demasiado pobres para generar preguntas fiables."""
    if not text:
        return True

    cleaned = normalize_spaces(text)
    cleaned_match = normalize_for_match(cleaned)
    if len(cleaned) < 160:
        return True

    alpha_chars = sum(ch.isalpha() for ch in cleaned)
    digit_chars = sum(ch.isdigit() for ch in cleaned)
    if alpha_chars < 80:
        return True

    # Evita fragmentos casi vacios, mascaras, listas de numeros o OCR muy roto.
    if alpha_chars < digit_chars * 2 and fuente == "problemas":
        return True

    is_image_chunk = "imagen extra" in cleaned_match or "posible recurso visual del tema" in cleaned_match
    if is_image_chunk:
        has_near_text = "texto cercano en la misma pagina:" in cleaned_match
        has_detected_text = "texto detectado en la imagen:" in cleaned_match
        if not has_near_text:
            return True
        if has_detected_text and alpha_chars < 180:
            return True

        # Evita preguntas generadas desde logos, portadas o descripciones genericas
        # del extractor ("recurso visual"), que luego no tienen una respuesta DDR real.
        useful_terms = [
            "objetivos", "requisitos", "restricciones", "top-down", "dimensionado",
            "formulacion", "optimizacion", "trafico", "demanda", "colas",
            "routing", "enrutamiento", "capacidad", "coste", "congestion",
            "robusto", "autonomas", "telemetry", "intent-based",
        ]
        generic_visual_only = (
            "posible recurso visual del tema" in cleaned_match
            and "texto detectado en la imagen:" in cleaned_match
            and "universidad degranada" in cleaned_match
            and not any(term in cleaned_match for term in useful_terms)
        )
        if generic_visual_only:
            return True

        if any(marker in cleaned_match for marker in ["prof. jose camacho", "josecamacho@ugr.es", "https://prado.ugr.es/"]):
            topic_terms = sum(term in cleaned_match for term in useful_terms)
            if topic_terms < 2:
                return True

    noisy_markers = [
        "universidad degranada",
        "texto detectado en la imagen:",
        "dimensiones aproximadas:",
        "orientacion:",
    ]
    marker_hits = sum(marker in cleaned_match for marker in noisy_markers)
    if marker_hits >= 2 and alpha_chars < 220:
        return True

    return False


def ollama_generate(prompt: str, num_predict: int = 800) -> str:
    url = f"{OLLAMA_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en Diseno y Dimensionado de Redes (DDR). "
                    "Debes seguir el formato pedido y responder de forma completa."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "think": False,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": num_predict,
            "num_thread": 12,
            "num_ctx": 8192,
            "num_batch": 512,
        },
    }
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    message = data.get("message") or {}
    content = (message.get("content") or "").strip()
    if not content:
        done_reason = data.get("done_reason", "")
        eval_count = data.get("eval_count", "")
        prompt_eval_count = data.get("prompt_eval_count", "")
        raise ValueError(
            f"respuesta vacia del modelo (done_reason={done_reason}, "
            f"prompt_eval_count={prompt_eval_count}, eval_count={eval_count})"
        )
    return content


def generate_with_retries(prompt: str, num_predict: int, label: str) -> str:
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw = ollama_generate(prompt, num_predict=num_predict)
            if raw.strip():
                return raw
            last_error = ValueError("respuesta vacia del modelo")
            print(f"  [WARN] {label}: intento {attempt}/{MAX_RETRIES} con respuesta vacia")
        except Exception as e:
            last_error = e
            print(f"  [WARN] {label}: intento {attempt}/{MAX_RETRIES} fallo: {e}")
    if last_error:
        raise last_error
    raise ValueError("no se pudo obtener respuesta del modelo")


def try_parse_labeled_question_answer(raw: str):
    """Fallback para salidas tipo 'PREGUNTA: ... RESPUESTA: ...'."""
    raw_clean = raw.strip()
    if not raw_clean:
        raise ValueError("respuesta vacia del modelo")

    pregunta_match = re.search(
        r"(?:^|\n)\s*PREGUNTA\s*:\s*(.+?)(?:\n\s*RESPUESTA\s*:|$)",
        raw_clean,
        flags=re.DOTALL | re.IGNORECASE,
    )
    respuesta_match = re.search(
        r"(?:^|\n)\s*RESPUESTA\s*:\s*(.+)$",
        raw_clean,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if not pregunta_match or not respuesta_match:
        raise ValueError(f"salida etiquetada no parseable. Raw: {raw_clean[:200]}")

    pregunta = pregunta_match.group(1).strip()
    respuesta = respuesta_match.group(1).strip()
    if not pregunta or not respuesta:
        raise ValueError("pregunta o respuesta vacia en salida etiquetada")

    return {"pregunta": pregunta, "respuesta": respuesta}


def try_parse_question_answer_json(raw: str):
    """Intenta extraer {"pregunta", "respuesta"} incluso si el modelo mete ruido."""
    raw_clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    if not raw_clean:
        raise ValueError("respuesta vacia del modelo")

    # Caso ideal: JSON valido completo.
    try:
        obj = json.loads(raw_clean)
        if obj.get("pregunta") and obj.get("respuesta"):
            return obj
    except Exception:
        pass

    # Intento 2: recortar al primer objeto JSON reconocible.
    match = re.search(r"\{.*\}", raw_clean, flags=re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            obj = json.loads(candidate)
            if obj.get("pregunta") and obj.get("respuesta"):
                return obj
        except Exception:
            pass

    # Intento 3: extraer manualmente los campos, tolerando comillas/cierres rotos.
    pregunta_match = re.search(r'"pregunta"\s*:\s*"(.+?)"\s*,\s*"respuesta"\s*:', raw_clean, flags=re.DOTALL)
    respuesta_match = re.search(r'"respuesta"\s*:\s*"(.+?)(?:"\s*\}|$)', raw_clean, flags=re.DOTALL)
    if pregunta_match and respuesta_match:
        pregunta = pregunta_match.group(1).strip()
        respuesta = respuesta_match.group(1).strip()
        pregunta = pregunta.replace('\\"', '"')
        respuesta = respuesta.replace('\\"', '"')
        if pregunta and respuesta:
            return {"pregunta": pregunta, "respuesta": respuesta}

    raise ValueError(f"JSON no parseable. Raw: {raw_clean[:200]}")


def build_conceptual_prompt(context_snippet: str, json_mode: bool = True) -> str:
    if json_mode:
        return f"""A partir del siguiente fragmento de teoria de redes (DDR), genera UNA sola pregunta conceptual clara y su respuesta correcta y completa.

La respuesta debe ser pedagogica, natural y breve.
Evita formulas, notacion matematica o variables salvo que sean imprescindibles.
Prioriza una explicacion intuitiva antes que una formulacion formal.
No uses saltos de linea dentro de los valores JSON.
Devuelve una sola linea de JSON valida.

FRAGMENTO:
{context_snippet}

Responde UNICAMENTE en este formato JSON (sin markdown, sin texto extra):
{{"pregunta": "...", "respuesta": "..."}}"""

    return f"""A partir del siguiente fragmento de teoria de redes (DDR), genera UNA sola pregunta conceptual clara y su respuesta correcta y completa.

La respuesta debe ser pedagogica, natural y breve.
Evita formulas innecesarias.

FRAGMENTO:
{context_snippet}

Devuelve SOLO este formato, sin markdown ni comentarios:
PREGUNTA: ...
RESPUESTA: ..."""


def build_exercise_prompt(context_snippet: str, json_mode: bool = True) -> str:
    if json_mode:
        return f"""A partir del siguiente enunciado o solucion de un ejercicio de redes (DDR), genera UNA pregunta sobre ese ejercicio y su respuesta correcta.

La respuesta debe ser clara y fiel al fragmento.
Si el contenido es muy formal, explica primero la idea general y despues, si hace falta, menciona la formulacion.
No uses saltos de linea dentro de los valores JSON.
Devuelve una sola linea de JSON valida.

FRAGMENTO:
{context_snippet}

Responde UNICAMENTE en este formato JSON (sin markdown, sin texto extra):
{{"pregunta": "...", "respuesta": "..."}}"""

    return f"""A partir del siguiente enunciado o solucion de un ejercicio de redes (DDR), genera UNA pregunta sobre ese ejercicio y su respuesta correcta.

La respuesta debe ser clara y fiel al fragmento.

FRAGMENTO:
{context_snippet}

Devuelve SOLO este formato, sin markdown ni comentarios:
PREGUNTA: ...
RESPUESTA: ..."""


def get_chunks_by_tema_fuente(collection, tema: str, fuente: str, limit: int = 60):
    data = collection.get(
        where={"$and": [{"tema": tema}, {"fuente": fuente}]},
        include=["documents", "metadatas"],
    )
    docs = data.get("documents") or []
    metas = data.get("metadatas") or []
    paired = [
        (doc, meta)
        for doc, meta in zip(docs, metas)
        if not is_low_quality_chunk(doc, fuente)
    ]
    random.shuffle(paired)
    return paired[:limit]


def generate_conceptual_questions(collection, tema: str, n: int) -> list:
    """Genera n preguntas conceptuales sobre un tema."""
    chunks = get_chunks_by_tema_fuente(collection, tema, "teoria", limit=40)
    if not chunks:
        print(f"  [WARN] Sin chunks de teoria para {tema}")
        return []

    selected = chunks[: min(n * 4, len(chunks))]
    results = []

    for doc, meta in selected:
        if len(results) >= n:
            break
        context_snippet = doc[:600]
        prompt = build_conceptual_prompt(context_snippet, json_mode=True)

        try:
            raw = generate_with_retries(prompt, num_predict=600, label=f"{tema} conceptual")
        except Exception as e:
            print(f"  [WARN] No se pudo generar salida JSON para {tema}: {e}")
            fallback_prompt = build_conceptual_prompt(context_snippet, json_mode=False)
            try:
                raw = generate_with_retries(
                    fallback_prompt,
                    num_predict=600,
                    label=f"{tema} conceptual fallback",
                )
            except Exception as inner_e:
                print(f"  [WARN] No se pudo generar salida para {tema}: {inner_e}")
                continue

        try:
            obj = try_parse_question_answer_json(raw)
        except Exception as e:
            try:
                obj = try_parse_labeled_question_answer(raw)
            except Exception:
                print(f"  [WARN] No se pudo parsear JSON para {tema}: {e}\n  Raw: {raw[:200]}")
                continue

        if obj.get("pregunta") and obj.get("respuesta"):
            results.append(
                {
                    "question": obj["pregunta"],
                    "ground_truth": obj["respuesta"],
                    "context": doc,
                    "tema": tema,
                    "tipo": "conceptual",
                    "fuente_pdf": meta.get("pdf", ""),
                    "pagina": meta.get("pagina", ""),
                }
            )
            print(f"  [OK] {tema} conceptual: {obj['pregunta'][:70]}...")

    return results


def generate_exercise_questions(collection, n: int) -> list:
    """Genera n preguntas sobre ejercicios/problemas de cualquier tema."""
    results = []

    for tema in TEMAS:
        chunks = get_chunks_by_tema_fuente(collection, tema, "problemas", limit=20)
        if not chunks:
            continue

        per_tema = max(1, n // len(TEMAS))
        selected = chunks[: min(per_tema * 4, len(chunks))]

        for doc, meta in selected:
            if len([item for item in results if item["tema"] == tema]) >= per_tema:
                break
            context_snippet = doc[:700]
            prompt = build_exercise_prompt(context_snippet, json_mode=True)

            try:
                raw = generate_with_retries(prompt, num_predict=800, label=f"{tema} ejercicio")
            except Exception as e:
                print(f"  [WARN] No se pudo generar salida JSON para ejercicio {tema}: {e}")
                fallback_prompt = build_exercise_prompt(context_snippet, json_mode=False)
                try:
                    raw = generate_with_retries(
                        fallback_prompt,
                        num_predict=800,
                        label=f"{tema} ejercicio fallback",
                    )
                except Exception as inner_e:
                    print(f"  [WARN] No se pudo generar salida para ejercicio {tema}: {inner_e}")
                    continue

            try:
                obj = try_parse_question_answer_json(raw)
            except Exception as e:
                try:
                    obj = try_parse_labeled_question_answer(raw)
                except Exception:
                    print(
                        f"  [WARN] No se pudo parsear JSON para ejercicio {tema}: {e}\n  Raw: {raw[:200]}"
                    )
                    continue

            if obj.get("pregunta") and obj.get("respuesta"):
                results.append(
                    {
                        "question": obj["pregunta"],
                        "ground_truth": obj["respuesta"],
                        "context": doc,
                        "tema": tema,
                        "tipo": "ejercicio",
                        "fuente_pdf": meta.get("pdf", ""),
                        "pagina": meta.get("pagina", ""),
                    }
                )
                print(f"  [OK] {tema} ejercicio: {obj['pregunta'][:70]}...")

    return results


def main():
    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Conectando a ChromaDB en {CHROMA_PATH}...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    print(f"Coleccion: {collection.count()} chunks\n")

    all_items = []

    for tema in TEMAS:
        print(f"[*] Generando preguntas conceptuales para {tema}...")
        items = generate_conceptual_questions(collection, tema, N_PER_TEMA)
        all_items += items
        print(f"    -> {len(items)} preguntas generadas\n")

    print("[*] Generando preguntas sobre ejercicios...")
    items = generate_exercise_questions(collection, N_EJERCICIOS)
    all_items += items
    print(f"    -> {len(items)} preguntas generadas\n")

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"\nDataset guardado en {OUTPUT_FILE}")
    print(f"Total preguntas: {len(all_items)}")
    tipos = {}
    for item in all_items:
        tipos[item["tipo"]] = tipos.get(item["tipo"], 0) + 1
    for tipo, count in tipos.items():
        print(f"  - {tipo}: {count}")


if __name__ == "__main__":
    main()
