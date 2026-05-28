from ingest.chunk_problemas_pdf import chunk_problemas_pdf


def chunk_problemas_tema4(pdf_path: str):
    return chunk_problemas_pdf(
        pdf_path=pdf_path,
        tema="Tema 4",
        pdf_label="problemas_tema4.pdf"
    )