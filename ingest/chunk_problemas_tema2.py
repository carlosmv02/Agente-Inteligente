from ingest.chunk_problemas_pdf import chunk_problemas_pdf


def chunk_problemas_tema2(pdf_path: str):
    return chunk_problemas_pdf(
        pdf_path=pdf_path,
        tema="Tema 2",
        pdf_label="problemas_tema2.pdf"
    )


def chunk_problemas_tema2_ii(pdf_path: str):
    return chunk_problemas_pdf(
        pdf_path=pdf_path,
        tema="Tema 2",
        pdf_label="problemas_tema2_II.pdf"
    )