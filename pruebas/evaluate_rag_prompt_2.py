"""
evaluate_rag_prompt_2.py
------------------------
Evalua el RAG con la variante de prompt 2: pedagogico_con_citas.

Este script reutiliza el motor de evaluate_rag.py y solo cambia:
  - el prompt usado para generar respuestas,
  - la carpeta de salida, para no sobrescribir prompt-0 ni prompt-1.

Uso:
    python evaluate_rag_prompt_2.py

Ejemplo:
    docker compose run --rm \
      -e OLLAMA_MODEL=qwen3:4b \
      -e EVAL_REUSE_RAW_RESULTS=0 \
      rag python evaluate_rag_prompt_2.py
"""

from pathlib import Path
import os
import re

import evaluate_rag as base


PROMPT_VARIANT = "pedagogico_con_citas"
PROMPT_VERSION = "prompt-2"


def slug_model_name(model_name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", model_name.strip())
    return value.replace(":", "-").strip("-") or "modelo"


def build_rag_prompt(question: str, context: str) -> str:
    return f"""Eres un asistente experto en Diseno y Dimensionado de Redes (DDR).

Tu tarea es responder a la PREGUNTA usando el CONTEXTO como unica fuente de hechos concretos.
Esta variante prioriza respuestas pedagogicas, trazables y faciles de auditar.

REGLAS:
1) Usa el CONTEXTO como unica fuente de hechos concretos.
2) No inventes enunciados, datos, topologias, valores, resultados ni pasos que no esten en el CONTEXTO.
3) Si el CONTEXTO no contiene suficiente informacion, dilo explicitamente.
4) Si faltan datos para cerrar un resultado numerico, indicalo claramente.
5) Si la pregunta es conceptual, responde con una explicacion pedagogica: definicion, idea clave y matices importantes soportados por el CONTEXTO.
6) Si la pregunta es de ejercicio o problema, responde de forma desarrollada, estructurada y completa: datos disponibles, procedimiento soportado, resultado si se puede obtener y limites si faltan datos.
7) Termina siempre con frases cerradas y completas.
8) Ajusta la longitud a la pregunta, pero favorece explicar el razonamiento frente a una respuesta minima.
9) Si el contexto muestra varias ocurrencias del mismo ejercicio dentro de un examen, no las mezcles: indica que la consulta es ambigua y separalas.
10) Incluye una cita breve al final de cada idea principal o paso relevante.
11) El formato de cita debe ser: [Fuente: <fuente>; Tema: <tema>; PDF: <pdf>; Pag: <pag>].
12) Si algun metadato no aparece en el CONTEXTO, omitelo de la cita en vez de inventarlo.
13) Usa solo citas derivadas de las cabeceras visibles del CONTEXTO.
14) No incluyas bibliografia externa ni referencias no presentes en el CONTEXTO.
15) Responde en espanol y manten la terminologia del CONTEXTO.

FORMATO DE RESPUESTA:
- Respuesta: contesta directamente a la pregunta.
- Desarrollo: explica los conceptos, pasos o razonamiento necesarios, con citas.
- Limites del contexto: indica que informacion falta, si falta algo; si no falta nada relevante, escribe "No se aprecian limites relevantes en el contexto recuperado."

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
        "Prompt pedagogico con citas: variante del prompt de rag_answer.py que "
        "mantiene el uso exclusivo del contexto, pero fuerza una respuesta "
        "mas desarrollada, estructurada y trazable con citas por idea o paso."
    )
    return summary


def configure_prompt_2_outputs() -> None:
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
    configure_prompt_2_outputs()
    print(f"Variante de prompt: {PROMPT_VARIANT} ({PROMPT_VERSION})")
    print(f"Resultados: {base.TESTS_DIR}\n")
    base.main()


if __name__ == "__main__":
    main()
