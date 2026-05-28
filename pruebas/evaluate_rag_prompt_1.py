"""
evaluate_rag_prompt_1.py
------------------------
Evalua el RAG con la variante de prompt 1: estricto.

Este script reutiliza el motor de evaluate_rag.py y solo cambia:
  - el prompt usado para generar respuestas,
  - la carpeta de salida, para no sobrescribir prompt-0.

Uso:
    python evaluate_rag_prompt_1.py

Ejemplo:
    docker compose run --rm \
      -e OLLAMA_MODEL=qwen3:4b \
      -e EVAL_REUSE_RAW_RESULTS=0 \
      rag python evaluate_rag_prompt_1.py
"""

from pathlib import Path
import os
import re

import evaluate_rag as base


PROMPT_VARIANT = "estricto"
PROMPT_VERSION = "prompt-1"


def slug_model_name(model_name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", model_name.strip())
    return value.replace(":", "-").strip("-") or "modelo"


def build_rag_prompt(question: str, context: str) -> str:
    return f"""Eres un asistente experto en Diseno y Dimensionado de Redes (DDR).

Debes responder a la PREGUNTA usando exclusivamente la informacion del CONTEXTO.

REGLAS ESTRICTAS:
1) No uses conocimiento externo, aunque conozcas la respuesta.
2) No inventes datos, topologias, formulas, valores numericos, resultados, pasos intermedios ni conclusiones.
3) Si el CONTEXTO no permite responder con seguridad, responde exactamente: "No hay informacion suficiente en el contexto para responder."
4) Si el CONTEXTO contiene informacion parcial, explica solo lo que si esta soportado e indica claramente que falta informacion para completar la respuesta.
5) Si faltan datos para resolver un ejercicio o cerrar un calculo numerico, no calcules por aproximacion ni supongas valores.
6) Si hay varias interpretaciones posibles o varias ocurrencias similares, senala la ambiguedad y separa las alternativas soportadas por el CONTEXTO.
7) Mantente fiel a la terminologia del CONTEXTO.
8) Responde en espanol, de forma clara y directa.
9) Para preguntas conceptuales, da una respuesta breve y precisa.
10) Para ejercicios o problemas, estructura la respuesta en pasos solo si esos pasos estan justificados por el CONTEXTO.
11) No incluyas citas bibliograficas inventadas. Si mencionas una fuente, usa solo los metadatos visibles del CONTEXTO.

CONTEXTO:
{context}

PREGUNTA:
{question}

RESPUESTA:""".strip()


_original_run_rag = base.run_rag
_original_summarize_results = base.summarize_results


def run_rag(question: str, item: dict | None = None):
    answer, chunks, metas, runtime = _original_run_rag(question, item=item)
    runtime["prompt_variant"] = PROMPT_VARIANT
    runtime["prompt_version"] = PROMPT_VERSION
    return answer, chunks, metas, runtime


def summarize_results(enriched_results: list[dict], wall_time_s: float) -> dict:
    summary = _original_summarize_results(enriched_results, wall_time_s)
    summary["prompt_variant"] = PROMPT_VARIANT
    summary["prompt_version"] = PROMPT_VERSION
    summary["prompt_description"] = (
        "Prompt estricto: responde solo con informacion presente en el contexto "
        "y declara insuficiencia cuando no haya soporte suficiente."
    )
    return summary


def configure_prompt_1_outputs() -> None:
    custom_output_dir = os.environ.get("EVAL_OUTPUT_DIR")
    if custom_output_dir:
        result_dir = Path(custom_output_dir)
        if not result_dir.is_absolute():
            result_dir = Path(base.BASE_DIR) / result_dir
    else:
        model_slug = slug_model_name(base.current_generator_model())
        result_dir = Path(base.BASE_DIR) / "resultados" / f"{model_slug}-{PROMPT_VERSION}"
    result_dir.mkdir(parents=True, exist_ok=True)

    base.TESTS_DIR = result_dir
    base.TESTSET_FILE = Path(base.BASE_DIR) / "tests" / "testset.json"
    base.RAW_RESULTS_FILE = result_dir / "rag_pipeline_results.json"
    base.RESULTS_FILE = result_dir / "ragas_results.json"
    base.SUMMARY_FILE = result_dir / "evaluation_summary.json"
    base.SUMMARY_MD_FILE = result_dir / "evaluation_summary.md"


def main() -> None:
    base.build_rag_prompt = build_rag_prompt
    base.run_rag = run_rag
    base.summarize_results = summarize_results
    configure_prompt_1_outputs()
    print(f"Variante de prompt: {PROMPT_VARIANT} ({PROMPT_VERSION})")
    print(f"Resultados: {base.TESTS_DIR}\n")
    base.main()


if __name__ == "__main__":
    main()
