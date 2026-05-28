"""
evaluate_rag_sin_pistas.py
--------------------------
Ejecuta las pruebas sin pistas del testset.

Equivale a desactivar EVAL_USE_TESTSET_HINTS para comprobar la recuperacion
en un escenario mas cercano a preguntas libres.

Pruebas:
  - gemma4:e2b + prompt-0
  - mistral:7b + prompt-0
  - gemma4:e2b + prompt-2
  - mistral:7b + prompt-2

Uso:
    python evaluate_rag_sin_pistas.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "resultados" / "sin-pistas"


RUNS = [
    ("gemma4:e2b", "prompt-0", "evaluate_rag.py"),
    ("mistral:7b", "prompt-0", "evaluate_rag.py"),
    ("gemma4:e2b", "prompt-2", "evaluate_rag_prompt_2.py"),
    ("mistral:7b", "prompt-2", "evaluate_rag_prompt_2.py"),
]


def slug_model_name(model_name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", model_name.strip())
    return value.replace(":", "-").strip("-") or "modelo"


def build_env(model: str, prompt_version: str) -> tuple[dict[str, str], Path]:
    env = os.environ.copy()
    env["LLM_PROVIDER"] = "ollama"
    env["OLLAMA_MODEL"] = model
    env["EVAL_USE_TESTSET_HINTS"] = "0"
    env["EVAL_ATTACH_PAGE_CONTEXT"] = env.get("EVAL_ATTACH_PAGE_CONTEXT", "1")
    env["EVAL_TOP_K"] = env.get("EVAL_TOP_K", "6")
    env["EVAL_REUSE_RAW_RESULTS"] = "0"
    env["EVAL_RUN_RAGAS"] = "1"
    env["RAGAS_JUDGE_PROVIDER"] = "openai"
    env["OPENAI_JUDGE_MODEL"] = env.get("OPENAI_JUDGE_MODEL", "gpt-5-mini")

    output_dir = RESULTS_DIR / f"{slug_model_name(model)}-{prompt_version}"
    env["EVAL_OUTPUT_DIR"] = str(output_dir)
    return env, output_dir


def run_one(model: str, prompt_version: str, script: str) -> None:
    env, output_dir = build_env(model, prompt_version)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 72)
    print(f"Prueba sin pistas: {model} | {prompt_version}")
    print(f"Script: {script}")
    print(f"Resultados: {output_dir}")
    print("=" * 72 + "\n")

    subprocess.run([sys.executable, script], cwd=BASE_DIR, env=env, check=True)


def main() -> int:
    for model, prompt_version, script in RUNS:
        run_one(model, prompt_version, script)
    print(f"\nPruebas sin pistas completadas en: {RESULTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
