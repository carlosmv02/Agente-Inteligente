import io
import os
import re
from typing import List, Dict, Any, Tuple

import fitz
from PIL import Image
import pytesseract

# Si en Windows no encuentra Tesseract, descomenta y ajusta:
# pytesseract.pytesseract.tesseract_cmd = r"D:\carlo\Tesseract-OCR\tesseract.exe"


def _clean_text(s: str) -> str:
    if not s:
        return ""
    s = s.replace("\x00", " ")
    s = s.replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


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


def _ocr_image(image: Image.Image, lang: str = "spa+eng") -> str:
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return _clean_text(text)
    except Exception as e:
        print(f"[WARN] Error OCR: {e}")
        return ""


def _is_meaningful_ocr_text(text: str, min_len: int = 12) -> bool:
    if not text:
        return False

    alnum_count = sum(ch.isalnum() for ch in text)
    if alnum_count < min_len:
        return False

    weird_ratio = sum(
        not (ch.isalnum() or ch.isspace() or ch in ".,;:()[]-%+/=<>")
        for ch in text
    ) / max(len(text), 1)

    return weird_ratio <= 0.40


def _extract_page_images_ocr(
    doc,
    page,
    page_num: int,
    ocr_lang: str = "spa+eng",
    min_image_width: int = 120,
    min_image_height: int = 120
) -> List[str]:
    image_texts = []
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

            ocr_text = _ocr_image(image, lang=ocr_lang)
            if _is_meaningful_ocr_text(ocr_text):
                image_texts.append(
                    f"[OCR imagen página {page_num}, figura {img_index}]\n{ocr_text}"
                )

        except Exception as e:
            print(f"[WARN] No se pudo procesar imagen página {page_num}, imagen {img_index}: {e}")

    return image_texts


def _join_pages_with_markers(
    pdf_path: str,
    ocr_lang: str = "spa+eng"
) -> str:
    """
    Devuelve un texto único con marcadores de página para luego poder
    estimar en qué páginas aparece cada ejercicio.
    """
    doc = fitz.open(pdf_path)
    parts = []

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_num = page_idx + 1

        page_text = _extract_page_text_blocks(page)
        image_ocr_texts = _extract_page_images_ocr(doc, page, page_num, ocr_lang=ocr_lang)

        section_parts = [f"\n[[PAGE:{page_num}]]\n"]
        if page_text:
            section_parts.append(page_text)
        if image_ocr_texts:
            section_parts.append("\n\n".join(image_ocr_texts))

        parts.append("\n\n".join(section_parts))

    return "\n\n".join(parts)


def _find_exercise_spans(text: str) -> List[Tuple[str, int, int]]:
    """
    Detecta ejercicios por patrones tipo:
    1. ...
    11. ...
    11.Calcule ...
    """
    pattern = re.compile(r'(?m)^\s*(\d+)\s*\.\s*')
    matches = list(pattern.finditer(text))

    spans = []
    for i, m in enumerate(matches):
        ej = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        spans.append((ej, start, end))

    return spans


def _pages_in_fragment(fragment: str) -> List[int]:
    pages = re.findall(r"\[\[PAGE:(\d+)\]\]", fragment)
    pages = [int(p) for p in pages]
    seen = set()
    ordered = []
    for p in pages:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    return ordered


def _remove_page_markers(text: str) -> str:
    text = re.sub(r'\[\[PAGE:\d+\]\]', '', text)
    return _clean_text(text)


def _split_long_exercise(text: str, max_chars: int = 2200, overlap: int = 250) -> List[str]:
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


def chunk_problemas_pdf(
    pdf_path: str,
    tema: str,
    pdf_label: str = None,
    ocr_lang: str = "spa+eng"
) -> List[Dict[str, Any]]:
    """
    Chunking por ejercicio para boletines de problemas.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No existe el PDF: {pdf_path}")

    merged_text = _join_pages_with_markers(pdf_path, ocr_lang=ocr_lang)
    spans = _find_exercise_spans(merged_text)

    chunks: List[Dict[str, Any]] = []
    pdf_name = pdf_label or os.path.basename(pdf_path)

    if not spans:
        # fallback: un chunk único si no detecta ejercicios
        clean = _remove_page_markers(merged_text)
        if clean:
            chunks.append({
                "content": clean,
                "metadata": {
                    "tema": tema,
                    "fuente": "problemas",
                    "pdf": pdf_name,
                    "tipo": "problema",
                    "ejercicio": "general",
                    "pagina_inicio": 0,
                    "pagina_fin": 0,
                    "paginas_str": ""
                }
            })
        return chunks

    for ejercicio, start, end in spans:
        fragment = merged_text[start:end]
        paginas = _pages_in_fragment(fragment)
        clean_fragment = _remove_page_markers(fragment)

        if not clean_fragment:
            continue

        subchunks = _split_long_exercise(clean_fragment, max_chars=2200, overlap=250)

        for sub_idx, subchunk in enumerate(subchunks):
            chunks.append({
                "content": subchunk,
                "metadata": {
                    "tema": tema,
                    "fuente": "problemas",
                    "pdf": pdf_name,
                    "tipo": "problema",
                    "ejercicio": ejercicio,
                    "pagina_inicio": paginas[0] if paginas else None,
                    "pagina_fin": paginas[-1] if paginas else None,
                    "paginas_str": ",".join(map(str, paginas)) if paginas else "",
                    "subchunk_index": sub_idx,
                    "total_subchunks": len(subchunks)
                }
            })

    return chunks
