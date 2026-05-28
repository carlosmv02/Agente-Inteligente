from ingest.chunk_pdf_ocr import chunk_pdf_with_ocr


def chunk_tema4(pdf_path: str):
    return chunk_pdf_with_ocr(
        pdf_path=pdf_path,
        tema="Tema 4",
        fuente="teoria"
    )