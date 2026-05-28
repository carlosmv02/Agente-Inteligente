import io
import os
import re
from typing import Any, Dict, List, Tuple

import fitz
from PIL import Image
import pytesseract


FOLDER_PATTERN = re.compile(r"^(?P<convocatoria>[a-zA-Z]+)-(?P<inicio>\d{4})-(?P<fin>\d{4})$")


def _metadata_from_folder(folder_name: str) -> Dict[str, str]:
    match = FOLDER_PATTERN.match(folder_name)
    if not match:
        return {
            "carpeta_examen": folder_name,
            "curso_academico": folder_name,
            "convocatoria": "",
        }

    convocatoria = match.group("convocatoria").lower()
    curso = f"{match.group('inicio')}-{match.group('fin')}"
    return {
        "carpeta_examen": folder_name,
        "curso_academico": curso,
        "convocatoria": convocatoria,
        "examen_id": folder_name,
    }


def _discover_exam_pdfs(examenes_root: str) -> List[str]:
    pdfs = []
    for dirpath, _, filenames in os.walk(examenes_root):
        for filename in sorted(filenames):
            if filename.lower().endswith(".pdf"):
                pdfs.append(os.path.join(dirpath, filename))
    return sorted(pdfs)


def _discover_matlab_files(folder_path: str) -> List[str]:
    matlab_files = []
    for filename in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(".m"):
            matlab_files.append(file_path)
    return matlab_files


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
    min_image_height: int = 120,
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
                    f"[OCR imagen pagina {page_num}, figura {img_index}]\n{ocr_text}"
                )

        except Exception as e:
            print(f"[WARN] No se pudo procesar imagen pagina {page_num}, imagen {img_index}: {e}")

    return image_texts


def _join_pages_with_markers(pdf_path: str, ocr_lang: str = "spa+eng") -> str:
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
    # Algunos examenes usan formatos como "1.", "1)", "Ejercicio 1" o "Problema 1".
    # Ampliamos el patron para mantener una segmentacion mas estable entre convocatorias.
    pattern = re.compile(
        r"(?im)^\s*(?:ejercicio|problema)?\s*(\d{1,2})(?:\s*[\.\):\-])?\s+"
    )
    matches = list(pattern.finditer(text))

    spans = []
    for i, match in enumerate(matches):
        ejercicio = match.group(1)
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        spans.append((ejercicio, start, end))

    return spans


def _pages_in_fragment(fragment: str) -> List[int]:
    pages = re.findall(r"\[\[PAGE:(\d+)\]\]", fragment)
    seen = set()
    ordered = []
    for page in pages:
        page_num = int(page)
        if page_num not in seen:
            seen.add(page_num)
            ordered.append(page_num)
    return ordered


def _remove_page_markers(text: str) -> str:
    text = re.sub(r"\[\[PAGE:\d+\]\]", "", text)
    return _clean_text(text)


def _split_general_exam_by_pages(
    merged_text: str,
    max_chars: int = 2200,
    overlap: int = 250,
) -> List[Tuple[str, int]]:
    page_pattern = re.compile(r"\[\[PAGE:(\d+)\]\]")
    matches = list(page_pattern.finditer(merged_text))
    if not matches:
        clean = _remove_page_markers(merged_text)
        return [(chunk, 0) for chunk in _split_long_exercise(clean, max_chars=max_chars, overlap=overlap)]

    page_chunks: List[Tuple[str, int]] = []
    for idx, match in enumerate(matches):
        page_num = int(match.group(1))
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(merged_text)
        page_text = _clean_text(merged_text[start:end])
        if not page_text:
            continue
        for subchunk in _split_long_exercise(page_text, max_chars=max_chars, overlap=overlap):
            page_chunks.append((subchunk, page_num))

    return page_chunks


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


def _split_code_text(text: str, max_chars: int = 1800, overlap: int = 150) -> List[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
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
            cut = max(chunk.rfind("\n\n"), chunk.rfind("\n"))
            if cut > int(max_chars * 0.5):
                chunk = chunk[:cut]
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


def _chunk_matlab_file(matlab_path: str, extra_metadata: Dict[str, str]) -> List[Dict[str, Any]]:
    with open(matlab_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    code_chunks = _split_code_text(code)
    matlab_name = os.path.basename(matlab_path)
    match_ej = re.search(r"\bej\s*([0-9]+)\b", matlab_name, flags=re.IGNORECASE)
    ejercicio_relacionado = match_ej.group(1) if match_ej else ""
    all_matlab_names = ",".join(
        os.path.basename(path) for path in _discover_matlab_files(os.path.dirname(matlab_path))
    )

    chunks = []
    for chunk_idx, chunk_text in enumerate(code_chunks):
        chunks.append({
            "content": chunk_text,
            "metadata": {
                "tema": "examenes",
                "fuente": "examenes",
                "tipo": "codigo_examen",
                "pdf": "",
                "matlab_file": matlab_name,
                "ejercicio_relacionado": ejercicio_relacionado,
                "matlab_files_carpeta": all_matlab_names,
                "chunk_index": chunk_idx,
                "total_chunks_archivo": len(code_chunks),
                **extra_metadata,
            }
        })

    return chunks


def chunk_examen_pdf(pdf_path: str, ocr_lang: str = "spa+eng") -> List[Dict[str, Any]]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No existe el PDF: {pdf_path}")

    folder_name = os.path.basename(os.path.dirname(pdf_path))
    extra_metadata = _metadata_from_folder(folder_name)
    extra_metadata["matlab_files_carpeta"] = ",".join(
        os.path.basename(path) for path in _discover_matlab_files(os.path.dirname(pdf_path))
    )
    merged_text = _join_pages_with_markers(pdf_path, ocr_lang=ocr_lang)
    spans = _find_exercise_spans(merged_text)
    pdf_name = os.path.basename(pdf_path)
    chunks: List[Dict[str, Any]] = []

    if not spans:
        general_chunks = _split_general_exam_by_pages(merged_text)
        for chunk_idx, (clean, page_num) in enumerate(general_chunks):
            if not clean:
                continue
            chunks.append({
                "content": clean,
                "metadata": {
                    "tema": "examenes",
                    "fuente": "examenes",
                    "pdf": pdf_name,
                    "tipo": "examen",
                    "ejercicio": "general",
                    "pagina_inicio": page_num,
                    "pagina_fin": page_num,
                    "paginas_str": str(page_num) if page_num else "",
                    "subchunk_index": chunk_idx,
                    "total_subchunks": len(general_chunks),
                    **extra_metadata,
                }
            })
        return chunks

    exercise_counts: Dict[str, int] = {}

    for ejercicio, start, end in spans:
        exercise_counts[ejercicio] = exercise_counts.get(ejercicio, 0) + 1
        ejercicio_ocurrencia = exercise_counts[ejercicio]
        ejercicio_uid = f"{ejercicio}-{ejercicio_ocurrencia}"
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
                    "tema": "examenes",
                    "fuente": "examenes",
                    "pdf": pdf_name,
                    "tipo": "examen",
                    "ejercicio": ejercicio,
                    "ejercicio_ocurrencia": ejercicio_ocurrencia,
                    "ejercicio_uid": ejercicio_uid,
                    "pagina_inicio": paginas[0] if paginas else None,
                    "pagina_fin": paginas[-1] if paginas else None,
                    "paginas_str": ",".join(map(str, paginas)) if paginas else "",
                    "subchunk_index": sub_idx,
                    "total_subchunks": len(subchunks),
                    **extra_metadata,
                }
            })

    return chunks


def chunk_examenes_dir(examenes_root: str = "examenes") -> List[Dict]:
    if not os.path.exists(examenes_root):
        raise FileNotFoundError(f"No existe la carpeta de examenes: {examenes_root}")

    chunks = []
    pdf_paths = _discover_exam_pdfs(examenes_root)

    for pdf_path in pdf_paths:
        folder_path = os.path.dirname(pdf_path)
        folder_name = os.path.basename(folder_path)
        extra_metadata = _metadata_from_folder(folder_name)

        chunks.extend(chunk_examen_pdf(pdf_path))

        for matlab_path in _discover_matlab_files(folder_path):
            chunks.extend(_chunk_matlab_file(matlab_path, extra_metadata))

    return chunks
