"""PDF -> clean text, with OCR fallback for scanned documents.

Text layer via pypdf. Pages with almost no extractable text are treated as
scans and sent to Tesseract (lang "ind") when PyMuPDF + pytesseract are
installed; otherwise the document is flagged `needs_ocr` so it shows up in the
work queue instead of silently producing an empty article list.
"""
import hashlib
import re
from pathlib import Path

import requests
from pypdf import PdfReader

HERE = Path(__file__).parent
CACHE = HERE / "cache" / "pdf"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"

NOISE = [
    re.compile(r"^\s*-\s*\d+\s*-\s*$"),                      # "- 3 -"
    re.compile(r"^\s*\d+\s*/\s*\d+\s*$"),                    # "3 / 60"
    re.compile(r"^\s*(www\.)?(peraturan|jdih)[\w.]*\.go\.id\S*\s*$", re.I),
    re.compile(r"^\s*(jdih\.)?[\w.-]+\.go\.id\s*$", re.I),
    re.compile(r"^\s*PRESIDEN\s*$|^\s*REPUBLIK INDONESIA\s*$"),  # running header on PP/Perpres pages
    re.compile(r"^\s*SK No\s*\d+\s*[A-Z]?\s*$"),             # Setneg sheet numbers
]


def download(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".pdf")
    if not path.exists() or path.stat().st_size < 1000:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=120)
        r.raise_for_status()
        path.write_bytes(r.content)
    return path


def _ocr_page(pdf_path, index):
    try:
        import fitz  # PyMuPDF
        import pytesseract
        from PIL import Image
    except ImportError:
        return None
    doc = fitz.open(pdf_path)
    pix = doc[index].get_pixmap(dpi=300)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return pytesseract.image_to_string(img, lang="ind")


def extract(pdf_path):
    reader = PdfReader(str(pdf_path))
    pages, ocr_pages, missing = [], 0, 0
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        if len(t.strip()) < 80:
            o = _ocr_page(pdf_path, i)
            if o:
                t, ocr_pages = o, ocr_pages + 1
            else:
                missing += 1
        pages.append(t)
    text = clean("\n".join(pages))
    return {
        "text": text,
        "pages": len(pages),
        "ocr_pages": ocr_pages,
        "needs_ocr": missing > max(1, len(pages) // 4),
        "sha1": hashlib.sha1(text.encode()).hexdigest(),
    }


def clean(text):
    lines = []
    for line in text.replace("\r", "").split("\n"):
        if any(rx.match(line) for rx in NOISE):
            continue
        line = re.sub(r"[ \t]+", " ", line).strip()
        # OCR-layer artefacts on scanned copies: "Pasal6", "Pasa!I", "Pa sal 12"
        line = re.sub(r"^Pa\s?sa\s?[l!1I|]\s*(\d+[A-Z]?|[IVX]+)$", r"Pasal \1", line)
        line = re.sub(r"^BAB\s*([IVXL]+)$", r"BAB \1", line)
        line = line.replace("MENTER!", "MENTERI")
        lines.append(line)
    t = "\n".join(lines)
    t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)          # hyphenated line breaks
    t = re.sub(r"dan/\s*a\s*tau", "dan/atau", t)       # frequent pypdf artefact
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()
