import json
from pathlib import Path

from ingest.chunk_tema1 import chunk_tema1
from ingest.chunk_tema2 import chunk_tema2
from ingest.chunk_tema3 import chunk_tema3
from ingest.chunk_tema4 import chunk_tema4
from ingest.chunk_tema5 import chunk_tema5

from ingest.chunk_problemas_tema2 import chunk_problemas_tema2, chunk_problemas_tema2_ii
from ingest.chunk_problemas_tema3 import chunk_problemas_tema3
from ingest.chunk_problemas_tema4 import chunk_problemas_tema4
from ingest.chunk_problemas_tema5 import chunk_problemas_tema5
from ingest.chunk_examenes import chunk_examenes_dir


MATERIALES_DIR = Path("materiales")
TEORIA_DIR = MATERIALES_DIR / "teoria"
PROBLEMAS_DIR = MATERIALES_DIR / "problemas"
EXAMENES_DIR = MATERIALES_DIR / "examenes"


def save_jsonl(chunks, output_path="chunks_ddr.jsonl"):
    with open(output_path, "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")


def main():
    all_chunks = []

    # ===== TEORIA =====
    all_chunks += chunk_tema1(str(TEORIA_DIR / "Tema1_2526.pdf"))
    all_chunks += chunk_tema2(str(TEORIA_DIR / "Tema2_2526.pdf"))
    all_chunks += chunk_tema3(str(TEORIA_DIR / "Tema3_2526.pdf"))
    all_chunks += chunk_tema4(str(TEORIA_DIR / "Tema4_2526.pdf"))
    all_chunks += chunk_tema5(str(TEORIA_DIR / "Tema5_2526.pdf"))

    # ===== PROBLEMAS =====
    all_chunks += chunk_problemas_tema2(str(PROBLEMAS_DIR / "problemas_tema2.pdf"))
    all_chunks += chunk_problemas_tema2_ii(str(PROBLEMAS_DIR / "problemas_tema2_II.pdf"))
    all_chunks += chunk_problemas_tema3(str(PROBLEMAS_DIR / "problemas_tema3.pdf"))
    all_chunks += chunk_problemas_tema4(str(PROBLEMAS_DIR / "problemas_tema4.pdf"))
    all_chunks += chunk_problemas_tema5(str(PROBLEMAS_DIR / "problemas_tema5.pdf"))

    # ===== EXAMENES =====
    all_chunks += chunk_examenes_dir(str(EXAMENES_DIR))

    save_jsonl(all_chunks, "chunks_ddr.jsonl")
    print(f"Chunks totales generados: {len(all_chunks)}")


if __name__ == "__main__":
    main()
