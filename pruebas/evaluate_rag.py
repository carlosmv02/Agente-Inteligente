"""
evaluate_rag.py
---------------
Evalua el sistema RAG y, opcionalmente, ejecuta RAGAs.

Flujo:
  1. Lee tests/testset.json generado por generate_testset.py
  2. Para cada pregunta, ejecuta el pipeline RAG completo
  3. Evalua con RAGAs: faithfulness, answer_relevancy, context_precision, context_recall
  4. Guarda resultados en tests/ragas_results.json y muestra resumen

Uso:
    python evaluate_rag.py
"""

import json
import logging
import math
import os
import re
import sys
import time
import warnings
from pathlib import Path

import chromadb
import requests
from sentence_transformers import SentenceTransformer

try:
    import psutil
except ImportError:
    psutil = None

# Configuracion
BASE_DIR        = Path(__file__).resolve().parent
CHROMA_PATH     = os.environ.get("CHROMA_PATH", str(BASE_DIR / "chroma_ddr"))
COLLECTION_NAME = "ddr_chunks"
OLLAMA_URL      = os.environ.get("OLLAMA_URL", "http://ollama:11434")
OLLAMA_BASE_URL = OLLAMA_URL
OLLAMA_MODEL    = os.environ.get("OLLAMA_MODEL", "gemma4")
OLLAMA_JUDGE_MODEL = os.environ.get("OLLAMA_JUDGE_MODEL", OLLAMA_MODEL)
LLM_PROVIDER    = os.environ.get("LLM_PROVIDER", "ollama").lower()
OPENAI_MODEL    = os.environ.get("OPENAI_MODEL", "gpt-5-mini")
OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY", "").strip()
OPENAI_REASONING_EFFORT = os.environ.get("OPENAI_REASONING_EFFORT", "low").strip()
RAGAS_JUDGE_PROVIDER = os.environ.get("RAGAS_JUDGE_PROVIDER", "ollama").lower()
OPENAI_JUDGE_MODEL = os.environ.get("OPENAI_JUDGE_MODEL", OPENAI_MODEL)
EMBED_MODEL     = "intfloat/multilingual-e5-base"
DEFAULT_TESTS_DIR = BASE_DIR / "tests"
OUTPUT_DIR_ENV = os.environ.get("EVAL_OUTPUT_DIR")
TESTS_DIR = Path(OUTPUT_DIR_ENV) if OUTPUT_DIR_ENV else DEFAULT_TESTS_DIR
if not TESTS_DIR.is_absolute():
    TESTS_DIR = BASE_DIR / TESTS_DIR
TESTSET_FILE = Path(os.environ.get("EVAL_TESTSET_FILE", str(DEFAULT_TESTS_DIR / "testset.json")))
if not TESTSET_FILE.is_absolute():
    TESTSET_FILE = BASE_DIR / TESTSET_FILE
RESULTS_FILE    = TESTS_DIR / "ragas_results.json"
RAW_RESULTS_FILE = TESTS_DIR / "rag_pipeline_results.json"
SUMMARY_FILE    = TESTS_DIR / "evaluation_summary.json"
SUMMARY_MD_FILE = TESTS_DIR / "evaluation_summary.md"
TOP_K           = int(os.environ.get("EVAL_TOP_K", os.environ.get("TOP_K", "6")))
USE_TESTSET_HINTS = os.environ.get("EVAL_USE_TESTSET_HINTS", "1") not in {"0", "false", "False"}
ATTACH_PAGE_CONTEXT = os.environ.get("EVAL_ATTACH_PAGE_CONTEXT", "1") not in {"0", "false", "False"}
REUSE_RAW_RESULTS = os.environ.get("EVAL_REUSE_RAW_RESULTS", "1") not in {"0", "false", "False"}
RUN_RAGAS = os.environ.get("EVAL_RUN_RAGAS", "0") in {"1", "true", "True"}
DEFAULT_GENERATION_MAX_TOKENS = "2000" if LLM_PROVIDER == "openai" else "1200"
GENERATION_MAX_TOKENS = int(os.environ.get("EVAL_MAX_OUTPUT_TOKENS", DEFAULT_GENERATION_MAX_TOKENS))
OPENAI_EMPTY_RETRY_MAX_TOKENS = int(os.environ.get("EVAL_OPENAI_EMPTY_RETRY_MAX_TOKENS", "4000"))
RAGAS_TIMEOUT   = int(os.environ.get("RAGAS_TIMEOUT", "1200"))
RAGAS_MAX_WORKERS = int(os.environ.get("RAGAS_MAX_WORKERS", "2"))
RAGAS_MAX_RETRIES = int(os.environ.get("RAGAS_MAX_RETRIES", "3"))
RAGAS_SAMPLE_SIZE = int(os.environ.get("RAGAS_SAMPLE_SIZE", "0"))
RAGAS_METRICS = [
    metric.strip()
    for metric in os.environ.get(
        "RAGAS_METRICS",
        "faithfulness,answer_relevancy,context_precision,context_recall",
    ).split(",")
    if metric.strip()
]

logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"ragas\..*",
)

if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

print("Cargando modelo de embeddings...")
embed_model = SentenceTransformer(EMBED_MODEL)

print("Conectando a ChromaDB...")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_collection(COLLECTION_NAME)
PROCESS = psutil.Process(os.getpid()) if psutil else None


class LocalE5Embeddings:
    """Adaptador LangChain minimo para que RAGAs no dependa de nomic-embed-text."""

    def __init__(self, model: SentenceTransformer):
        self.model = EMBED_MODEL
        self._encoder = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._encoder.encode(
            [f"passage: {text}" for text in texts],
            normalize_embeddings=True,
        ).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self._encoder.encode(
            f"query: {text}",
            normalize_embeddings=True,
        ).tolist()


def resource_snapshot() -> dict:
    if not PROCESS:
        return {}
    info = PROCESS.memory_info()
    cpu_times = PROCESS.cpu_times()
    return {
        "rss_mb": round(info.rss / (1024 * 1024), 2),
        "vms_mb": round(info.vms / (1024 * 1024), 2),
        "cpu_user_s": round(cpu_times.user, 3),
        "cpu_system_s": round(cpu_times.system, 3),
    }


def resource_delta(start: dict, end: dict) -> dict:
    if not start or not end:
        return {}
    return {
        "rss_delta_mb": round(end.get("rss_mb", 0) - start.get("rss_mb", 0), 2),
        "rss_peak_end_mb": end.get("rss_mb"),
        "cpu_user_delta_s": round(end.get("cpu_user_s", 0) - start.get("cpu_user_s", 0), 3),
        "cpu_system_delta_s": round(end.get("cpu_system_s", 0) - start.get("cpu_system_s", 0), 3),
    }


def ollama_generate(prompt: str, num_predict: int = 1200) -> tuple[str, dict]:
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": True,
        "options": {"temperature": 0.0, "num_predict": num_predict},
    }
    r = requests.post(url, json=payload, stream=True, timeout=600)
    r.raise_for_status()
    text = ""
    last_chunk = {}
    for line in r.iter_lines():
        if line:
            chunk = json.loads(line)
            text += chunk.get("response", "")
            last_chunk = chunk

    stats = {
        "prompt_eval_count": last_chunk.get("prompt_eval_count"),
        "eval_count": last_chunk.get("eval_count"),
        "total_duration_s": ns_to_s(last_chunk.get("total_duration")),
        "load_duration_s": ns_to_s(last_chunk.get("load_duration")),
        "prompt_eval_duration_s": ns_to_s(last_chunk.get("prompt_eval_duration")),
        "eval_duration_s": ns_to_s(last_chunk.get("eval_duration")),
        "done_reason": last_chunk.get("done_reason"),
    }
    return text.strip(), stats


def _field(obj, name: str):
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _nested_field(obj, *names: str):
    current = obj
    for name in names:
        if current is None:
            return None
        current = _field(current, name)
    return current


def _is_openai_reasoning_model(model: str) -> bool:
    model_l = model.lower()
    return model_l.startswith(("gpt-5", "o"))


def _extract_openai_text(response) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()

    parts = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = _field(content, "text")
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def _openai_stats(response, requested_max_output_tokens: int) -> dict:
    usage = getattr(response, "usage", None)
    incomplete_details = getattr(response, "incomplete_details", None)
    return {
        "model": OPENAI_MODEL,
        "input_tokens": _field(usage, "input_tokens") if usage else None,
        "output_tokens": _field(usage, "output_tokens") if usage else None,
        "reasoning_tokens": _nested_field(usage, "output_tokens_details", "reasoning_tokens"),
        "total_tokens": _field(usage, "total_tokens") if usage else None,
        "status": getattr(response, "status", None),
        "incomplete_reason": _field(incomplete_details, "reason") if incomplete_details else None,
        "response_id": getattr(response, "id", None),
        "requested_max_output_tokens": requested_max_output_tokens,
        "reasoning_effort": (
            OPENAI_REASONING_EFFORT
            if _is_openai_reasoning_model(OPENAI_MODEL)
            else None
        ),
    }


def _create_openai_response(client, prompt: str, max_output_tokens: int):
    request = {
        "model": OPENAI_MODEL,
        "input": prompt,
        "max_output_tokens": max_output_tokens,
    }
    if _is_openai_reasoning_model(OPENAI_MODEL) and OPENAI_REASONING_EFFORT:
        request["reasoning"] = {"effort": OPENAI_REASONING_EFFORT}
    return client.responses.create(**request)


def openai_generate(prompt: str, num_predict: int = 1200) -> tuple[str, dict]:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "Define OPENAI_API_KEY para usar LLM_PROVIDER=openai."
        )

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "Falta la dependencia 'openai'. Reconstruye la imagen tras actualizar requirements.txt."
        ) from exc

    client = OpenAI()
    response = _create_openai_response(client, prompt, num_predict)
    text = _extract_openai_text(response)
    stats = _openai_stats(response, num_predict)

    if not text and OPENAI_EMPTY_RETRY_MAX_TOKENS > num_predict:
        retry_tokens = OPENAI_EMPTY_RETRY_MAX_TOKENS
        retry_response = _create_openai_response(client, prompt, retry_tokens)
        retry_text = _extract_openai_text(retry_response)
        retry_stats = _openai_stats(retry_response, retry_tokens)
        retry_stats["retry_after_empty_text"] = True
        retry_stats["first_attempt"] = stats
        text = retry_text
        stats = retry_stats

    if not text:
        raise RuntimeError(
            "OpenAI devolvio una respuesta sin texto visible. "
            f"status={stats.get('status')}, "
            f"incomplete_reason={stats.get('incomplete_reason')}, "
            f"output_tokens={stats.get('output_tokens')}, "
            f"reasoning_tokens={stats.get('reasoning_tokens')}, "
            f"max_output_tokens={stats.get('requested_max_output_tokens')}, "
            f"response_id={stats.get('response_id')}"
        )

    return text.strip(), stats


def generate_answer(prompt: str, num_predict: int = 1200) -> tuple[str, dict]:
    if LLM_PROVIDER == "ollama":
        return ollama_generate(prompt, num_predict=num_predict)
    if LLM_PROVIDER == "openai":
        return openai_generate(prompt, num_predict=num_predict)
    raise ValueError(f"LLM_PROVIDER no soportado: {LLM_PROVIDER}")


def ns_to_s(value) -> float | None:
    if value is None:
        return None
    return round(float(value) / 1_000_000_000, 3)


def detect_tema(query: str):
    m = re.search(r"\btema\s+(\d+)\b", query.lower())
    return f"Tema {m.group(1)}" if m else None


def query_embedding(text: str) -> list[float]:
    """Embedding compatible con la indexacion E5 usada en build_vector_db.py."""
    return embed_model.encode(f"query: {text}", normalize_embeddings=True).tolist()


def build_where_filter(query: str, item: dict | None = None):
    clauses = []

    tema = detect_tema(query)
    if USE_TESTSET_HINTS and item:
        tema = item.get("tema") or tema
        tipo = item.get("tipo")
        if tipo == "conceptual":
            clauses.append({"fuente": "teoria"})
        elif tipo == "ejercicio":
            clauses.append({"fuente": "problemas"})

    if tema:
        clauses.append({"tema": tema})

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def get_page_context(item: dict, limit: int = 4) -> tuple[list[str], list[dict]]:
    """Anade chunks de la misma pagina/PDF para no perder texto cercano a imagenes."""
    if not ATTACH_PAGE_CONTEXT:
        return [], []

    pdf = item.get("fuente_pdf")
    pagina = item.get("pagina")
    if not pdf or pagina in ("", None):
        return [], []

    where = {"$and": [{"pdf": pdf}, {"pagina": pagina}]}
    tipo = item.get("tipo")
    if tipo == "conceptual":
        where["$and"].append({"fuente": "teoria"})
    elif tipo == "ejercicio":
        where["$and"].append({"fuente": "problemas"})

    data = collection.get(where=where, include=["documents", "metadatas"])
    docs = data.get("documents") or []
    metas = data.get("metadatas") or []
    return docs[:limit], metas[:limit]


def retrieve_context_eval(query: str, item: dict | None = None) -> tuple[str, list[str], list[dict], list[float]]:
    """Devuelve (context_str, list_of_chunks) para RAGAs."""
    q_emb = query_embedding(query)
    where_filter = build_where_filter(query, item)

    res = collection.query(
        query_embeddings=[q_emb],
        n_results=TOP_K,
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    docs = res.get("documents", [[]])[0] or []
    metas = res.get("metadatas", [[]])[0] or []
    distances = res.get("distances", [[]])[0] or []

    if USE_TESTSET_HINTS and item:
        page_docs, page_metas = get_page_context(item)
        seen = set(docs)
        for doc, meta in zip(page_docs, page_metas):
            if doc not in seen:
                docs.append(doc)
                metas.append(meta)
                distances.append(None)
                seen.add(doc)

    blocks = []
    for doc, meta in zip(docs, metas):
        pagina = meta.get("pagina", meta.get("pagina_inicio", "-"))
        blocks.append(
            f"[Fuente: {meta.get('fuente')} | PDF: {meta.get('pdf')} | "
            f"Tema: {meta.get('tema')} | Pag: {pagina}]\n{doc}"
        )

    return "\n\n".join(blocks), docs, metas, distances


def build_rag_prompt(question: str, context: str) -> str:
    return f"""Eres un asistente experto en Diseno y Dimensionado de Redes (DDR).
Usa el CONTEXTO como unica fuente. No inventes datos.
Si el contexto no tiene informacion suficiente, dilo explicitamente.

CONTEXTO:
{context}

PREGUNTA:
{question}""".strip()


def run_rag(question: str, item: dict | None = None) -> tuple[str, list[str], list[dict], dict]:
    total_start = time.perf_counter()
    resources_start = resource_snapshot()

    retrieval_start = time.perf_counter()
    context_str, raw_chunks, metas, distances = retrieve_context_eval(question, item=item)
    retrieval_time_s = time.perf_counter() - retrieval_start

    prompt = build_rag_prompt(question, context_str)
    generation_start = time.perf_counter()
    answer, llm_stats = generate_answer(prompt, num_predict=GENERATION_MAX_TOKENS)
    generation_time_s = time.perf_counter() - generation_start

    resources_end = resource_snapshot()
    runtime = {
        "retrieval_time_s": round(retrieval_time_s, 3),
        "generation_time_s": round(generation_time_s, 3),
        "total_time_s": round(time.perf_counter() - total_start, 3),
        "context_count": len(raw_chunks),
        "context_chars": sum(len(chunk or "") for chunk in raw_chunks),
        "prompt_chars": len(prompt),
        "answer_chars": len(answer),
        "generation_max_tokens": GENERATION_MAX_TOKENS,
        "retrieval_distances": distances,
        "llm_provider": LLM_PROVIDER,
        "llm_model": OPENAI_MODEL if LLM_PROVIDER == "openai" else OLLAMA_MODEL,
        "ollama": llm_stats if LLM_PROVIDER == "ollama" else {},
        "openai": llm_stats if LLM_PROVIDER == "openai" else {},
        "resources": resource_delta(resources_start, resources_end),
    }
    return answer, raw_chunks, metas, runtime


def current_generator_model() -> str:
    return OPENAI_MODEL if LLM_PROVIDER == "openai" else OLLAMA_MODEL


def load_reusable_raw_results(testset: list[dict]) -> list[dict] | None:
    if not REUSE_RAW_RESULTS or not RAW_RESULTS_FILE.exists():
        return None

    with RAW_RESULTS_FILE.open(encoding="utf-8") as f:
        raw_results = json.load(f)

    if len(raw_results) != len(testset):
        return None

    for raw_item, test_item in zip(raw_results, testset):
        if raw_item.get("question") != test_item.get("question"):
            return None

    expected_model = current_generator_model()
    for raw_item in raw_results:
        runtime = raw_item.get("runtime", {})
        if runtime.get("llm_provider") != LLM_PROVIDER:
            print(
                "No se reutilizan resultados intermedios: "
                f"proveedor cache={runtime.get('llm_provider')} actual={LLM_PROVIDER}"
            )
            return None
        if runtime.get("llm_model") != expected_model:
            print(
                "No se reutilizan resultados intermedios: "
                f"modelo cache={runtime.get('llm_model')} actual={expected_model}"
            )
            return None

    return raw_results


def build_ragas_metrics(llm, emb):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness

    available_metrics = {
        "faithfulness": faithfulness,
        "answer_relevancy": answer_relevancy,
        "context_precision": context_precision,
        "context_recall": context_recall,
    }
    unknown = [name for name in RAGAS_METRICS if name not in available_metrics]
    if unknown:
        raise ValueError(
            "Metricas RAGAs no reconocidas en RAGAS_METRICS: "
            + ", ".join(unknown)
        )

    metrics = [available_metrics[name] for name in RAGAS_METRICS]
    for metric in metrics:
        metric.llm = llm
        if hasattr(metric, "embeddings"):
            metric.embeddings = emb
    return metrics


def build_openai_judge_llm(ChatOpenAI, LangchainLLMWrapper):
    """Crea el juez OpenAI para RAGAs evitando parametros no soportados."""
    is_gpt5 = OPENAI_JUDGE_MODEL.lower().startswith("gpt-5")
    kwargs = {
        "model": OPENAI_JUDGE_MODEL,
        "timeout": RAGAS_TIMEOUT,
        "max_retries": RAGAS_MAX_RETRIES,
    }

    if is_gpt5:
        kwargs["disabled_params"] = {"temperature": None}
    else:
        kwargs["temperature"] = 0

    try:
        chat_model = ChatOpenAI(**kwargs)
    except TypeError:
        kwargs.pop("disabled_params", None)
        kwargs["temperature"] = 1 if is_gpt5 else 0
        chat_model = ChatOpenAI(**kwargs)

    llm = LangchainLLMWrapper(chat_model)
    if is_gpt5:
        original_generate_text = llm.generate_text
        original_agenerate_text = llm.agenerate_text

        def force_default_temperature(args, kwargs):
            args = list(args)
            kwargs = dict(kwargs)
            if len(args) >= 3:
                args[2] = 1
                kwargs.pop("temperature", None)
            else:
                kwargs["temperature"] = 1
            return tuple(args), kwargs

        def generate_text(*args, **kwargs):
            args, kwargs = force_default_temperature(args, kwargs)
            return original_generate_text(*args, **kwargs)

        async def agenerate_text(*args, **kwargs):
            args, kwargs = force_default_temperature(args, kwargs)
            return await original_agenerate_text(*args, **kwargs)

        llm.generate_text = generate_text
        llm.agenerate_text = agenerate_text

    return llm


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def text_similarity(text_a: str, text_b: str, prefix_a: str = "passage", prefix_b: str = "passage") -> float:
    if not text_a or not text_b:
        return 0.0
    emb_a = embed_model.encode(f"{prefix_a}: {text_a}", normalize_embeddings=True).tolist()
    emb_b = embed_model.encode(f"{prefix_b}: {text_b}", normalize_embeddings=True).tolist()
    return round(cosine_similarity(emb_a, emb_b), 4)


def has_insufficient_context_answer(answer: str) -> bool:
    answer_l = (answer or "").lower()
    markers = [
        "informacion insuficiente",
        "información insuficiente",
        "no se establece",
        "no contiene suficiente",
        "no tiene informacion suficiente",
        "no tiene información suficiente",
        "no se especifica",
    ]
    return any(marker in answer_l for marker in markers)


def source_alignment(metas: list[dict], item: dict) -> dict:
    if not metas:
        return {
            "same_tema_ratio": 0.0,
            "same_pdf_ratio": 0.0,
            "same_page_hit": False,
            "retrieved_sources": [],
        }

    expected_tema = item.get("tema")
    expected_pdf = item.get("fuente_pdf")
    expected_page = item.get("pagina")
    same_tema = sum(1 for meta in metas if meta.get("tema") == expected_tema)
    same_pdf = sum(1 for meta in metas if meta.get("pdf") == expected_pdf)
    same_page_hit = any(
        meta.get("pdf") == expected_pdf
        and str(meta.get("pagina", meta.get("pagina_inicio", ""))) == str(expected_page)
        for meta in metas
    )
    sources = sorted({
        f"{meta.get('tema')}|{meta.get('pdf')}|{meta.get('pagina', meta.get('pagina_inicio', '-'))}"
        for meta in metas
    })
    return {
        "same_tema_ratio": round(same_tema / len(metas), 3),
        "same_pdf_ratio": round(same_pdf / len(metas), 3),
        "same_page_hit": same_page_hit,
        "retrieved_sources": sources,
    }


def enrich_quality_metrics(raw_results: list[dict], testset: list[dict]) -> list[dict]:
    enriched = []
    for raw_item, test_item in zip(raw_results, testset):
        answer = raw_item.get("answer", "")
        ground_truth = raw_item.get("ground_truth", "")
        contexts = raw_item.get("contexts", []) or []
        context_text = "\n\n".join(contexts)
        metas = raw_item.get("retrieved_metadatas", []) or []

        answer_gt_similarity = text_similarity(answer, ground_truth)
        answer_context_similarity = text_similarity(answer, context_text)
        gt_context_similarity = text_similarity(ground_truth, context_text)
        alignment = source_alignment(metas, test_item)

        quality = {
            "answer_ground_truth_similarity": answer_gt_similarity,
            "answer_context_similarity": answer_context_similarity,
            "ground_truth_context_similarity": gt_context_similarity,
            "insufficient_context_answer": has_insufficient_context_answer(answer),
            "answer_words": len(answer.split()),
            "ground_truth_words": len(ground_truth.split()),
            "context_count": len(contexts),
            "context_chars": sum(len(context or "") for context in contexts),
            **alignment,
        }

        item = dict(raw_item)
        item["quality"] = quality
        enriched.append(item)
    return enriched


def summarize_results(enriched_results: list[dict], wall_time_s: float) -> dict:
    count = len(enriched_results)
    runtimes = [item.get("runtime", {}) for item in enriched_results]
    qualities = [item.get("quality", {}) for item in enriched_results]
    runtime_providers = sorted({
        runtime.get("llm_provider")
        for runtime in runtimes
        if runtime.get("llm_provider")
    })
    runtime_models = sorted({
        runtime.get("llm_model")
        for runtime in runtimes
        if runtime.get("llm_model")
    })

    def avg(path: str) -> float | None:
        values = []
        for obj in runtimes + qualities:
            current = obj
            for key in path.split("."):
                if not isinstance(current, dict):
                    current = None
                    break
                current = current.get(key)
            if isinstance(current, (int, float)):
                values.append(float(current))
        if not values:
            return None
        return round(sum(values) / len(values), 4)

    total_recorded = sum(
        runtime.get("total_time_s", 0)
        for runtime in runtimes
        if isinstance(runtime.get("total_time_s"), (int, float))
    )
    insufficient = sum(1 for quality in qualities if quality.get("insufficient_context_answer"))
    same_page_hits = sum(1 for quality in qualities if quality.get("same_page_hit"))

    return {
        "num_questions": count,
        "configured_llm_provider": LLM_PROVIDER,
        "configured_llm_model": current_generator_model(),
        "top_k": TOP_K,
        "use_testset_hints": USE_TESTSET_HINTS,
        "attach_page_context": ATTACH_PAGE_CONTEXT,
        "generation_max_tokens": GENERATION_MAX_TOKENS,
        "result_llm_providers": runtime_providers,
        "result_llm_models": runtime_models,
        "wall_time_s": round(wall_time_s, 3),
        "recorded_pipeline_time_s": round(total_recorded, 3),
        "avg_time_per_response_s": round(total_recorded / count, 3) if count and total_recorded else None,
        "avg_retrieval_time_s": avg("retrieval_time_s"),
        "avg_generation_time_s": avg("generation_time_s"),
        "avg_answer_ground_truth_similarity": avg("answer_ground_truth_similarity"),
        "avg_answer_context_similarity": avg("answer_context_similarity"),
        "avg_ground_truth_context_similarity": avg("ground_truth_context_similarity"),
        "avg_same_tema_ratio": avg("same_tema_ratio"),
        "avg_same_pdf_ratio": avg("same_pdf_ratio"),
        "same_page_hit_rate": round(same_page_hits / count, 3) if count else 0.0,
        "insufficient_context_answers": insufficient,
        "insufficient_context_rate": round(insufficient / count, 3) if count else 0.0,
        "avg_context_count": avg("context_count"),
        "avg_context_chars": avg("context_chars"),
        "avg_answer_words": avg("answer_words"),
        "avg_prompt_tokens_ollama": avg("ollama.prompt_eval_count"),
        "avg_completion_tokens_ollama": avg("ollama.eval_count"),
        "avg_ollama_total_duration_s": avg("ollama.total_duration_s"),
        "avg_input_tokens_openai": avg("openai.input_tokens"),
        "avg_output_tokens_openai": avg("openai.output_tokens"),
        "avg_total_tokens_openai": avg("openai.total_tokens"),
        "avg_cpu_user_delta_s": avg("resources.cpu_user_delta_s"),
        "avg_cpu_system_delta_s": avg("resources.cpu_system_delta_s"),
        "avg_rss_peak_end_mb": avg("resources.rss_peak_end_mb"),
    }


def write_summary_markdown(summary: dict, enriched_results: list[dict]) -> None:
    lines = [
        "# Evaluacion RAG",
        "",
        "## Resumen",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- **{key}**: {value}")

    lines.extend(["", "## Peores respuestas por similitud answer-ground_truth", ""])
    ranked = sorted(
        enriched_results,
        key=lambda item: item.get("quality", {}).get("answer_ground_truth_similarity", 0),
    )
    for item in ranked[:8]:
        q = item.get("question", "").replace("\n", " ")
        quality = item.get("quality", {})
        lines.append(
            f"- {quality.get('answer_ground_truth_similarity')} | "
            f"insuficiente={quality.get('insufficient_context_answer')} | {q[:140]}"
        )

    SUMMARY_MD_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_fast_evaluation(raw_results: list[dict], testset: list[dict], wall_time_s: float) -> tuple[list[dict], dict]:
    enriched_results = enrich_quality_metrics(raw_results, testset)
    summary = summarize_results(enriched_results, wall_time_s)

    with RAW_RESULTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(enriched_results, f, ensure_ascii=False, indent=2)

    with SUMMARY_FILE.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    write_summary_markdown(summary, enriched_results)

    print("\n" + "=" * 50)
    print("RESUMEN RAPIDO")
    print("=" * 50)
    for key, value in summary.items():
        print(f"  {key:<35}: {value}")
    print(f"\nResumen guardado en {SUMMARY_FILE}")
    print(f"Resumen Markdown guardado en {SUMMARY_MD_FILE}")

    return enriched_results, summary


def main():
    run_start = time.perf_counter()
    TESTS_DIR.mkdir(parents=True, exist_ok=True)

    generator_model = OPENAI_MODEL if LLM_PROVIDER == "openai" else OLLAMA_MODEL
    judge_model = OPENAI_JUDGE_MODEL if RAGAS_JUDGE_PROVIDER == "openai" else OLLAMA_JUDGE_MODEL
    print("Configuracion de modelos:")
    print(f"  generador={LLM_PROVIDER} | modelo={generator_model}")
    print(f"  ragas_juez={RAGAS_JUDGE_PROVIDER} | modelo={judge_model}")
    print(f"  ragas_activo={RUN_RAGAS}\n")

    if not TESTSET_FILE.exists():
        print(f"ERROR: No se encontro {TESTSET_FILE}. Ejecuta primero generate_testset.py")
        sys.exit(1)

    with TESTSET_FILE.open(encoding="utf-8") as f:
        testset = json.load(f)

    print(f"Testset cargado: {len(testset)} preguntas\n")

    raw_results = load_reusable_raw_results(testset)

    if raw_results is not None:
        print(f"Reutilizando resultados intermedios de {RAW_RESULTS_FILE}\n")
    else:
        print("Generando resultados intermedios desde el pipeline RAG.\n")
        raw_results = []
        for i, item in enumerate(testset):
            question = item["question"]
            gt = item["ground_truth"]

            print(f"[{i + 1}/{len(testset)}] {question[:80]}...")
            answer, chunks, metas, runtime = run_rag(question, item=item)

            raw_results.append(
                {
                    "question": question,
                    "answer": answer,
                    "ground_truth": gt,
                    "contexts": chunks,
                    "retrieved_metadatas": metas,
                    "tema": item.get("tema"),
                    "tipo": item.get("tipo"),
                    "fuente_pdf": item.get("fuente_pdf"),
                    "pagina": item.get("pagina"),
                    "runtime": runtime,
                }
            )
            print(f"  -> Respuesta: {answer[:100]}...\n")

        with RAW_RESULTS_FILE.open("w", encoding="utf-8") as f:
            json.dump(raw_results, f, ensure_ascii=False, indent=2)
        print(f"Resultados intermedios guardados en {RAW_RESULTS_FILE}")

    raw_results, _summary = write_fast_evaluation(
        raw_results=raw_results,
        testset=testset,
        wall_time_s=time.perf_counter() - run_start,
    )

    if not RUN_RAGAS:
        print("\nRAGAs omitido. Para ejecutarlo: EVAL_RUN_RAGAS=1 python evaluate_rag.py")
        return

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from datasets import Dataset
        from langchain_ollama import ChatOllama
        from ragas import evaluate
        from ragas.embeddings import LangchainEmbeddingsWrapper
        from ragas.llms import LangchainLLMWrapper
        from ragas.run_config import RunConfig

    ragas_rows = raw_results[:RAGAS_SAMPLE_SIZE] if RAGAS_SAMPLE_SIZE > 0 else raw_results
    if RAGAS_SAMPLE_SIZE > 0:
        print(
            f"\nRAGAs se ejecutara sobre una muestra de "
            f"{len(ragas_rows)}/{len(raw_results)} ejemplos."
        )

    questions = [item["question"] for item in ragas_rows]
    answers = [item["answer"] for item in ragas_rows]
    contexts_list = [item["contexts"] for item in ragas_rows]
    ground_truths = [item["ground_truth"] for item in ragas_rows]

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts_list,
        "ground_truth": ground_truths,
    }
    dataset = Dataset.from_dict(data)

    print("Configurando RAGAs...")
    print(
        f"  judge_provider={RAGAS_JUDGE_PROVIDER} | judge_model={judge_model} | "
        f"timeout={RAGAS_TIMEOUT}s | "
        f"max_workers={RAGAS_MAX_WORKERS} | retries={RAGAS_MAX_RETRIES}"
    )
    print(f"  metrics={', '.join(RAGAS_METRICS)} | embeddings=local {EMBED_MODEL}")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        if RAGAS_JUDGE_PROVIDER == "openai":
            if not os.environ.get("OPENAI_API_KEY"):
                raise RuntimeError(
                    "Define OPENAI_API_KEY para usar RAGAS_JUDGE_PROVIDER=openai."
                )
            try:
                from langchain_openai import ChatOpenAI
            except ImportError as exc:
                raise RuntimeError(
                    "Falta 'langchain-openai'. Reconstruye la imagen tras actualizar requirements.txt."
                ) from exc

            llm = build_openai_judge_llm(ChatOpenAI, LangchainLLMWrapper)
        elif RAGAS_JUDGE_PROVIDER == "ollama":
            llm = LangchainLLMWrapper(
                ChatOllama(
                    model=OLLAMA_JUDGE_MODEL,
                    base_url=OLLAMA_BASE_URL,
                    temperature=0,
                )
            )
        else:
            raise ValueError(f"RAGAS_JUDGE_PROVIDER no soportado: {RAGAS_JUDGE_PROVIDER}")

        emb = LangchainEmbeddingsWrapper(LocalE5Embeddings(embed_model))

    metrics = build_ragas_metrics(llm, emb)

    print("\nEjecutando evaluacion RAGAs (puede tardar varios minutos)...\n")
    run_config = RunConfig(
        timeout=RAGAS_TIMEOUT,
        max_workers=RAGAS_MAX_WORKERS,
        max_retries=RAGAS_MAX_RETRIES,
    )
    results = evaluate(dataset=dataset, metrics=metrics, run_config=run_config)

    print("\n" + "=" * 50)
    print("RESULTADOS RAGAs")
    print("=" * 50)
    df = results.to_pandas()
    metric_columns = [name for name in RAGAS_METRICS if name in df.columns]
    missing_metric_columns = [name for name in RAGAS_METRICS if name not in df.columns]
    if missing_metric_columns:
        print(f"Metricas no encontradas en la salida: {', '.join(missing_metric_columns)}")
        print(f"Columnas disponibles: {', '.join(map(str, df.columns))}")
    display_columns = [name for name in ["question", "user_input"] if name in df.columns]
    display_columns += metric_columns
    if display_columns:
        print(df[display_columns].to_string(index=False))
    else:
        print(df.to_string(index=False))

    print("\n-- Medias --")
    for col in metric_columns:
        print(f"  {col:<25}: {df[col].mean():.3f}")

    df.to_json(RESULTS_FILE, orient="records", force_ascii=False, indent=2)
    print(f"\nResultados guardados en {RESULTS_FILE}")


if __name__ == "__main__":
    main()
