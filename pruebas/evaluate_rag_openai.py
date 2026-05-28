"""
evaluate_rag_openai.py
----------------------
Ejecuta de forma secuencial la evaluacion del RAG con OpenAI para los tres
prompts disponibles:

  - prompt-0: prompt base              -> evaluate_rag.py
  - prompt-1: prompt estricto          -> evaluate_rag_prompt_1.py
  - prompt-2: prompt pedagogico/citas  -> evaluate_rag_prompt_2.py

Uso recomendado dentro del contenedor:

    python evaluate_rag_openai.py

Uso recomendado con docker compose:

    docker compose run --rm \
      -e OPENAI_MODEL=gpt-5-mini \
      -e EVAL_REUSE_RAW_RESULTS=0 \
      rag python evaluate_rag_openai.py

Para calcular tambien RAGAS con juez OpenAI:

    docker compose run --rm \
      -e OPENAI_MODEL=gpt-5-mini \
      -e EVAL_REUSE_RAW_RESULTS=0 \
      -e EVAL_RUN_RAGAS=1 \
      -e RAGAS_JUDGE_PROVIDER=openai \
      -e OPENAI_JUDGE_MODEL=gpt-5-mini \
      rag python evaluate_rag_openai.py
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "resultados"
TESTS_DIR = BASE_DIR / "tests"

PROMPT_RUNS = [
    {
        "version": "prompt-0",
        "name": "base",
        "script": "evaluate_rag.py",
        "outputs_in_tests": True,
    },
    {
        "version": "prompt-1",
        "name": "estricto",
        "script": "evaluate_rag_prompt_1.py",
        "outputs_in_tests": False,
    },
    {
        "version": "prompt-2",
        "name": "pedagogico_con_citas",
        "script": "evaluate_rag_prompt_2.py",
        "outputs_in_tests": False,
    },
]

OUTPUT_FILES = [
    "rag_pipeline_results.json",
    "evaluation_summary.json",
    "evaluation_summary.md",
]
RAGAS_RESULTS_FILE = "ragas_results.json"


def slug_model_name(model_name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", model_name.strip())
    return value.replace(":", "-").strip("-") or "modelo-openai"


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    env["LLM_PROVIDER"] = "openai"
    if not env.get("OPENAI_MODEL"):
        env["OPENAI_MODEL"] = "gpt-5-mini"

    # Fuerza nuevas respuestas salvo que el usuario indique lo contrario.
    if not env.get("EVAL_REUSE_RAW_RESULTS"):
        env["EVAL_REUSE_RAW_RESULTS"] = "0"

    # Si se activa RAGAS y no se indica juez, se usa OpenAI para evitar mezclar
    # un generador OpenAI con un juez local por accidente.
    if env.get("EVAL_RUN_RAGAS", "0") in {"1", "true", "True"}:
        if not env.get("RAGAS_JUDGE_PROVIDER"):
            env["RAGAS_JUDGE_PROVIDER"] = "openai"
        if not env.get("OPENAI_JUDGE_MODEL"):
            env["OPENAI_JUDGE_MODEL"] = env.get("OPENAI_MODEL", "gpt-5-mini")

    return env


def ragas_enabled(env: dict[str, str]) -> bool:
    return env.get("EVAL_RUN_RAGAS", "0") in {"1", "true", "True"}


def result_dir_for(openai_model: str, prompt_version: str) -> Path:
    return RESULTS_DIR / f"{slug_model_name(openai_model)}-{prompt_version}"


def remove_file_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def cleanup_stale_ragas(env: dict[str, str], prompt_version: str, openai_model: str) -> None:
    if ragas_enabled(env):
        return

    if prompt_version == "prompt-0":
        remove_file_if_exists(TESTS_DIR / RAGAS_RESULTS_FILE)

    remove_file_if_exists(result_dir_for(openai_model, prompt_version) / RAGAS_RESULTS_FILE)


def copy_prompt_0_outputs(openai_model: str, env: dict[str, str]) -> Path:
    result_dir = result_dir_for(openai_model, "prompt-0")
    result_dir.mkdir(parents=True, exist_ok=True)

    missing = []
    for filename in OUTPUT_FILES:
        source = TESTS_DIR / filename
        if not source.exists():
            missing.append(str(source))
            continue
        shutil.copy2(source, result_dir / filename)

    ragas_source = TESTS_DIR / RAGAS_RESULTS_FILE
    ragas_target = result_dir / RAGAS_RESULTS_FILE
    if ragas_enabled(env):
        if not ragas_source.exists():
            missing.append(str(ragas_source))
        else:
            shutil.copy2(ragas_source, ragas_target)
    else:
        remove_file_if_exists(ragas_target)

    if missing:
        raise FileNotFoundError(
            "No se han encontrado todos los resultados esperados del prompt base:\n"
            + "\n".join(f"  - {path}" for path in missing)
        )

    return result_dir


def run_prompt(prompt_run: dict[str, object], env: dict[str, str]) -> Path:
    script = str(prompt_run["script"])
    prompt_name = str(prompt_run["name"])
    prompt_version = str(prompt_run["version"])
    openai_model = env.get("OPENAI_MODEL", "gpt-5-mini")
    cleanup_stale_ragas(env, prompt_version, openai_model)

    print("\n" + "=" * 72)
    print(f"Ejecutando {prompt_version} ({prompt_name}) con OpenAI")
    print(f"Modelo generador: {openai_model}")
    print(f"Script: {script}")
    print("=" * 72 + "\n")

    subprocess.run(
        [sys.executable, script],
        cwd=BASE_DIR,
        env=env,
        check=True,
    )

    if bool(prompt_run["outputs_in_tests"]):
        result_dir = copy_prompt_0_outputs(openai_model, env)
    else:
        result_dir = result_dir_for(openai_model, prompt_version)

    print(f"\nResultados de {prompt_version}: {result_dir}")
    return result_dir


def main() -> int:
    env = build_env()
    openai_model = env.get("OPENAI_MODEL", "gpt-5-mini")

    print("Evaluacion RAG con OpenAI")
    print(f"Modelo generador: {openai_model}")
    print(f"EVAL_REUSE_RAW_RESULTS={env.get('EVAL_REUSE_RAW_RESULTS')}")
    print(f"EVAL_RUN_RAGAS={env.get('EVAL_RUN_RAGAS', '0')}")
    if env.get("EVAL_RUN_RAGAS", "0") in {"1", "true", "True"}:
        print(f"RAGAS_JUDGE_PROVIDER={env.get('RAGAS_JUDGE_PROVIDER')}")
        print(f"OPENAI_JUDGE_MODEL={env.get('OPENAI_JUDGE_MODEL')}")

    result_dirs = []
    for prompt_run in PROMPT_RUNS:
        result_dirs.append(run_prompt(prompt_run, env))

    print("\n" + "=" * 72)
    print("Evaluacion OpenAI completada")
    print("Carpetas generadas:")
    for result_dir in result_dirs:
        print(f"  - {result_dir}")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
