import json
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "chunks_ddr.jsonl"
DB_DIR = "chroma_ddr"
COLLECTION_NAME = "ddr_chunks"

MODEL_NAME = "intfloat/multilingual-e5-base"


def load_chunks(path: str):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def sanitize_metadata(md: dict) -> dict:
    """
    Convierte metadata a tipos compatibles con Chroma:
    str, int, float, bool.
    Elimina None y convierte listas/dicts a string.
    """
    clean = {}

    for k, v in md.items():
        if v is None:
            continue

        if isinstance(v, (str, int, float, bool)):
            clean[k] = v

        elif isinstance(v, list):
            if len(v) == 0:
                continue
            clean[k] = ",".join(map(str, v))

        elif isinstance(v, dict):
            clean[k] = json.dumps(v, ensure_ascii=False)

        else:
            clean[k] = str(v)

    return clean


def main():
    if not os.path.exists(CHUNKS_PATH):
        raise FileNotFoundError(f"No existe {CHUNKS_PATH}. Ejecuta primero main_ingest.py")

    chunks = load_chunks(CHUNKS_PATH)
    print(f"Cargados {len(chunks)} chunks")

    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(
        path=DB_DIR,
        settings=Settings(anonymized_telemetry=False)
    )

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    col = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    docs = []
    metadatas = []
    ids = []

    for idx, ch in enumerate(chunks):
        content = ch.get("content", "")
        metadata = sanitize_metadata(ch.get("metadata", {}))

        if not content.strip():
            continue

        docs.append(content)
        metadatas.append(metadata)
        ids.append(f"chunk-{idx:05d}")

    print("Generando embeddings (local)...")
    embeddings = model.encode(
        [f"passage: {d}" for d in docs],
        normalize_embeddings=True
    )

    print("Guardando en Chroma...")
    col.add(
        ids=ids,
        documents=docs,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    print(f"Vector DB creada en ./{DB_DIR} con colección '{COLLECTION_NAME}'")


if __name__ == "__main__":
    main()