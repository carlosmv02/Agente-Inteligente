import io
import os
import re
from typing import List, Dict, Any

import fitz
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\carlo\tesseract.exe"

# Si en Windows no encuentra Tesseract, descomenta esta línea y ajusta la ruta:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def _clean_text(s: str) -> str:
    if not s:
        return ""
    s = s.replace("\x00", " ")
    s = s.replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _split_text(text: str, max_chars: int = 1200, overlap: int = 200) -> List[str]:
    text = _clean_text(text)
    if not text:
        return []

    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]

        if end < n:
            cut_candidates = [
                chunk.rfind("\n\n"),
                chunk.rfind("\n"),
                chunk.rfind(". "),
                chunk.rfind("; "),
                chunk.rfind(": "),
            ]
            cut = max(cut_candidates)
            if cut > int(max_chars * 0.6):
                chunk = chunk[:cut + 1]
                end = start + len(chunk)

        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

        if end >= n:
            break

        next_start = max(end - overlap, start + 1)
        if next_start <= start:
            break
        start = next_start

    return chunks


def _extract_page_text_blocks(page) -> str:
    blocks = page.get_text("blocks")
    blocks = sorted(blocks, key=lambda b: (b[1], b[0]))

    texts = []
    for block in blocks:
        txt = block[4] if len(block) > 4 else ""
        txt = _clean_text(txt)
        if txt:
            texts.append(txt)

    return "\n\n".join(texts)


def _extract_nearby_text(page_text: str, max_chars: int = 500) -> str:
    page_text = _clean_text(page_text)
    if not page_text:
        return ""
    return page_text[:max_chars]


def _describe_image_basic(image: Image.Image, page_num: int, img_index: int) -> str:
    width, height = image.size

    if width > height:
        orientation = "horizontal"
    elif height > width:
        orientation = "vertical"
    else:
        orientation = "cuadrada"

    return (
        f"Imagen extraída de la página {page_num}, figura {img_index}. "
        f"Dimensiones aproximadas: {width}x{height} píxeles. "
        f"Orientación: {orientation}. "
        f"Posible recurso visual del tema, como diagrama, esquema, gráfica, tabla o ilustración."
    )


def _ocr_image(image: Image.Image, lang: str = "spa+eng") -> str:
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return _clean_text(text)
    except Exception as e:
        print(f"[WARN] Error OCR: {e}")
        return ""


def _is_meaningful_ocr_text(text: str, min_len: int = 15) -> bool:
    if not text:
        return False

    alnum_count = sum(ch.isalnum() for ch in text)
    if alnum_count < min_len:
        return False

    weird_ratio = sum(
        not (ch.isalnum() or ch.isspace() or ch in ".,;:()[]-%+/")
        for ch in text
    ) / max(len(text), 1)

    if weird_ratio > 0.35:
        return False

    return True


def chunk_pdf_with_ocr(
    pdf_path: str,
    tema: str,
    fuente: str = "teoria",
    max_chars: int = 1200,
    overlap: int = 200,
    ocr_lang: str = "spa+eng",
    min_image_width: int = 120,
    min_image_height: int = 120
) -> List[Dict[str, Any]]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No existe el PDF: {pdf_path}")

    doc = fitz.open(pdf_path)
    chunks: List[Dict[str, Any]] = []
    pdf_name = os.path.basename(pdf_path)

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_num = page_idx + 1

        # 1) TEXTO
        page_text = _extract_page_text_blocks(page)

        if page_text:
            text_chunks = _split_text(page_text, max_chars=max_chars, overlap=overlap)

            for chunk_idx, chunk_text in enumerate(text_chunks):
                chunks.append({
                    "content": chunk_text,
                    "metadata": {
                        "tema": tema,
                        "fuente": fuente,
                        "pdf": pdf_name,
                        "pagina": page_num,
                        "tipo": "teoria",
                        "chunk_index": chunk_idx,
                        "total_chunks_pagina": len(text_chunks)
                    }
                })

        # 2) IMÁGENES + OCR
        image_list = page.get_images(full=True)

        for img_index, img_info in enumerate(image_list, start=1):
            xref = img_info[0]

            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

                width, height = image.size
                if width < min_image_width or height < min_image_height:
                    continue

                basic_desc = _describe_image_basic(image, page_num, img_index)
                ocr_text = _ocr_image(image, lang=ocr_lang)
                nearby_text = _extract_nearby_text(page_text, max_chars=500)

                parts = [basic_desc]

                if _is_meaningful_ocr_text(ocr_text):
                    parts.append("Texto detectado en la imagen:\n" + ocr_text)

                if nearby_text:
                    parts.append("Texto cercano en la misma página:\n" + nearby_text)

                content = "\n\n".join(parts).strip()

                chunks.append({
                    "content": content,
                    "metadata": {
                        "tema": tema,
                        "fuente": fuente,
                        "pdf": pdf_name,
                        "pagina": page_num,
                        "tipo": "imagen",
                        "imagen_index": img_index,
                        "image_width": width,
                        "image_height": height
                    }
                })

            except Exception as e:
                print(f"[WARN] No se pudo procesar imagen página {page_num}, imagen {img_index}: {e}")

    return chunks