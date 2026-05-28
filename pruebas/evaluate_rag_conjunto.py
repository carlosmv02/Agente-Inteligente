"""
evaluate_rag_conjunto.py
------------------------
Ejecuta en secuencia las tres pruebas nuevas para poder dejarlas corriendo
en el servidor, por ejemplo dentro de screen.

Pruebas incluidas:
  1. evaluate_rag_sin_pistas.py
  2. evaluate_rag_sin_contexto_pagina.py
  3. evaluate_rag_top_k.py

Uso recomendado con docker compose:
    docker compose run --rm rag python evaluate_rag_conjunto.py

Para reanudar desde una prueba concreta:
    docker compose run --rm rag python evaluate_rag_conjunto.py --desde top-k
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "resultados" / "conjunto"

RUNS = [
    ("sin-pistas", "evaluate_rag_sin_pistas.py"),
    ("sin-contexto-pagina", "evaluate_rag_sin_contexto_pagina.py"),
    ("top-k", "evaluate_rag_top_k.py"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ejecuta las tres pruebas nuevas de RAG en secuencia."
    )
    parser.add_argument(
        "--desde",
        choices=[name for name, _ in RUNS],
        help="Empieza desde esta prueba y omite las anteriores.",
    )
    parser.add_argument(
        "--solo",
        choices=[name for name, _ in RUNS],
        action="append",
        help="Ejecuta solo esta prueba. Se puede repetir varias veces.",
    )
    parser.add_argument(
        "--continuar-si-falla",
        action="store_true",
        help="Continua con la siguiente prueba aunque una falle.",
    )
    return parser.parse_args()


def selected_runs(args: argparse.Namespace) -> list[tuple[str, str]]:
    runs = RUNS
    if args.desde:
        start = next(index for index, (name, _) in enumerate(runs) if name == args.desde)
        runs = runs[start:]
    if args.solo:
        selected = set(args.solo)
        runs = [(name, script) for name, script in runs if name in selected]
    return runs


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["RAGAS_JUDGE_PROVIDER"] = "openai"
    env["OPENAI_JUDGE_MODEL"] = env.get("OPENAI_JUDGE_MODEL", "gpt-5-mini")
    env["RAGAS_TIMEOUT"] = env.get("RAGAS_TIMEOUT", "1200")
    env["RAGAS_MAX_WORKERS"] = env.get("RAGAS_MAX_WORKERS", "1")
    return env


def write_line(log_file, line: str = "") -> None:
    print(line, flush=True)
    log_file.write(line + "\n")
    log_file.flush()


def run_script(name: str, script: str, env: dict[str, str], log_file) -> dict:
    started_at = datetime.now().isoformat(timespec="seconds")
    cmd = [sys.executable, "-u", script]

    write_line(log_file)
    write_line(log_file, "=" * 80)
    write_line(log_file, f"[{started_at}] Iniciando prueba: {name}")
    write_line(log_file, f"Script: {script}")
    write_line(log_file, f"Comando: {' '.join(cmd)}")
    write_line(
        log_file,
        "Juez RAGAS: "
        f"{env.get('RAGAS_JUDGE_PROVIDER')} | {env.get('OPENAI_JUDGE_MODEL')}",
    )
    write_line(log_file, "=" * 80)

    process = subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
        log_file.write(line)
        log_file.flush()

    exit_code = process.wait()
    finished_at = datetime.now().isoformat(timespec="seconds")
    status = "ok" if exit_code == 0 else "error"

    write_line(log_file)
    write_line(
        log_file,
        f"[{finished_at}] Prueba {name} terminada con estado={status} "
        f"exit_code={exit_code}",
    )

    return {
        "name": name,
        "script": script,
        "started_at": started_at,
        "finished_at": finished_at,
        "exit_code": exit_code,
        "status": status,
    }


def main() -> int:
    args = parse_args()
    runs = selected_runs(args)
    if not runs:
        print("No hay pruebas seleccionadas.")
        return 1

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = RESULTS_DIR / f"evaluate_rag_conjunto_{timestamp}.log"
    summary_path = RESULTS_DIR / f"evaluate_rag_conjunto_{timestamp}.json"

    env = build_env()
    results = []
    exit_code = 0

    with log_path.open("w", encoding="utf-8") as log_file:
        write_line(log_file, "Ejecucion conjunta de pruebas RAG")
        write_line(log_file, f"Inicio: {datetime.now().isoformat(timespec='seconds')}")
        write_line(log_file, f"Directorio base: {BASE_DIR}")
        write_line(log_file, f"Log: {log_path}")
        write_line(log_file, "Pruebas seleccionadas:")
        for name, script in runs:
            write_line(log_file, f"  - {name}: {script}")

        for name, script in runs:
            result = run_script(name, script, env, log_file)
            results.append(result)

            if result["exit_code"] != 0:
                exit_code = result["exit_code"]
                if not args.continuar_si_falla:
                    write_line(
                        log_file,
                        "Se detiene la ejecucion. Usa --continuar-si-falla "
                        "si quieres seguir con el resto.",
                    )
                    break

        write_line(log_file)
        write_line(log_file, f"Fin: {datetime.now().isoformat(timespec='seconds')}")
        write_line(log_file, f"Resumen JSON: {summary_path}")

    summary = {
        "started_at": timestamp,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "base_dir": str(BASE_DIR),
        "log_path": str(log_path),
        "ragas_judge_provider": env.get("RAGAS_JUDGE_PROVIDER"),
        "openai_judge_model": env.get("OPENAI_JUDGE_MODEL"),
        "continue_on_error": args.continuar_si_falla,
        "runs": results,
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    if exit_code == 0:
        print(f"\nTodas las pruebas seleccionadas han terminado. Log: {log_path}")
    else:
        print(f"\nLa ejecucion termino con errores. Log: {log_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
