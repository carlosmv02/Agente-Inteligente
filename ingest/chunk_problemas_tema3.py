from ingest.chunk_problemas_pdf import chunk_problemas_pdf


def chunk_problemas_tema3(pdf_path: str):
    return chunk_problemas_pdf(
        pdf_path=pdf_path,
        tema="Tema 3",
        pdf_label="problemas_tema3.pdf"
    )