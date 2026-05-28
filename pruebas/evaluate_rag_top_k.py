"""
evaluate_rag_top_k.py
---------------------
Ejecuta pruebas variando el numero de chunks recuperados.

Usa EVAL_TOP_K para comparar TOP_K=3, TOP_K=6 y TOP_K=10 en las
configuraciones finalistas locales con prompt base.

Pruebas:
  - gemma4:e2b + prompt-0 + TOP_K in {3, 6, 10}
  - mistral:7b + prompt-0 + TOP_K in {3, 6, 10}

Uso:
    python evaluate_rag_top_k.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "resultados" / "top-k"
MODELS = ["gemma4:e2b", "mistral:7b"]
TOP_K_VALUES = [3, 10]


def slug_model_name(model_name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", model_name.strip())
    return value.replace(":", "-").strip("-") or "modelo"


def build_env(model: str, top_k: int) -> tuple[dict[str, str], Path]:
    env = os.environ.copy()
    env["LLM_PROVIDER"] = "ollama"
    env["OLLAMA_MODEL"] = model
    env["EVAL_USE_TESTSET_HINTS"] = env.get("EVAL_USE_TESTSET_HINTS", "1")
    env["EVAL_ATTACH_PAGE_CONTEXT"] = env.get("EVAL_ATTACH_PAGE_CONTEXT", "1")
    env["EVAL_TOP_K"] = str(top_k)
    env["EVAL_REUSE_RAW_RESULTS"] = "0"
    env["EVAL_RUN_RAGAS"] = "1"
    env["RAGAS_JUDGE_PROVIDER"] = "openai"
    env["OPENAI_JUDGE_MODEL"] = env.get("OPENAI_JUDGE_MODEL", "gpt-5-mini")

    output_dir = RESULTS_DIR / f"top-k-{top_k}" / f"{slug_model_name(model)}-prompt-0"
    env["EVAL_OUTPUT_DIR"] = str(output_dir)
    return env, output_dir


def run_one(model: str, top_k: int) -> None:
    env, output_dir = build_env(model, top_k)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 72)
    print(f"Prueba TOP_K={top_k}: {model} | prompt-0")
    print(f"Resultados: {output_dir}")
    print("=" * 72 + "\n")

    subprocess.run([sys.executable, "evaluate_rag.py"], cwd=BASE_DIR, env=env, check=True)


def main() -> int:
    for top_k in TOP_K_VALUES:
        for model in MODELS:
            run_one(model, top_k)
    print(f"\nPruebas TOP_K completadas en: {RESULTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
