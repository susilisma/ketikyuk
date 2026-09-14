"""Regulation number normalisation and citation extraction.

Canonical id:  <FORM>-<YEAR>-<NUMBER>      e.g. PMK-2022-204, PP-2025-28, UU-2023-6
The numbering of most forms restarts every year, so (form, year, number) is
unique. Old-style numbers such as "204/PMK.07/2022" keep the echelon code in
`number_raw` for display but collapse to the leading integer for the id.
"""
import re

# Long Indonesian names -> short form. Order matters: longest/most specific first.
FORM_NAMES = [
    (r"undang[- ]undang dasar", "UUD"),
    (r"peraturan pemerintah pengganti undang[- ]undang|perppu|perpu", "PERPPU"),
    (r"undang[- ]undang|\buu\b", "UU"),
    (r"peraturan pemerintah|\bpp\b", "PP"),
    (r"peraturan presiden|perpres", "PERPRES"),
    (r"keputusan presiden|keppres", "KEPPRES"),
    (r"instruksi presiden|inpres", "INPRES"),
    (r"peraturan menteri keuangan|\bpmk\b", "PMK"),
    (r"keputusan menteri keuangan|\bkmk\b", "KMK"),
    (r"peraturan menteri perdagangan|permendag", "PERMENDAG"),
    (r"peraturan menteri perindustrian|permenperin", "PERMENPERIN"),
    (r"peraturan menteri ketenagakerjaan|permenaker", "PERMENAKER"),
    (r"peraturan menteri kesehatan|permenkes", "PERMENKES"),
    (r"peraturan menteri hukum dan hak asasi manusia|peraturan menteri hukum dan ham|permenkumham", "PERMENKUMHAM"),
    (r"peraturan menteri komunikasi dan (?:informatika|digital)|permenkominfo|permenkomdigi", "PERMENKOMINFO"),
    (r"peraturan menteri investasi(?:/kepala badan koordinasi penanaman modal)?|peraturan badan koordinasi penanaman modal|peraturan bkpm", "PERBKPM"),
    (r"peraturan (?:kepala )?badan pengawas obat dan makanan|peraturan bpom|perbpom", "PERBPOM"),
    (r"peraturan menteri hukum(?! dan)", "PERMENKUM"),
    (r"peraturan menteri imigrasi", "PERMENIMIPAS"),
    (r"peraturan badan penyelenggara jaminan produk halal|peraturan bpjph", "PERBPJPH"),
    (r"peraturan badan penyelenggara jaminan sosial kesehatan|peraturan bpjs kesehatan", "PERBPJSKES"),
    (r"peraturan (?:badan penyelenggara jaminan sosial|bpjs) ketenagakerjaan", "PERBPJSTK"),
    (r"peraturan otoritas jasa keuangan|peraturan ojk|pojk", "POJK"),
    (r"surat edaran otoritas jasa keuangan|surat edaran ojk|seojk", "SEOJK"),
    (r"peraturan bank indonesia|\bpbi\b", "PBI"),
    (r"peraturan direktur jenderal pajak|per[- ]?dirjen pajak", "PERDIRJENPAJAK"),
    (r"peraturan direktur jenderal bea dan cukai|perdirjen bea", "PERDIRJENBC"),
    (r"surat edaran", "SE"),
]

_FORM_RE = [(re.compile(p, re.I), f) for p, f in FORM_NAMES]

BPK_SHORT = {  # "Bentuk Singkat" values seen on BPK -> our form
    "UU": "UU", "PERPU": "PERPPU", "PERPPU": "PERPPU", "PP": "PP", "PERPRES": "PERPRES",
    "KEPPRES": "KEPPRES", "INPRES": "INPRES", "PMK": "PMK", "KMK": "KMK",
    "PERMENDAG": "PERMENDAG", "PERMENPERIN": "PERMENPERIN", "PERMENAKER": "PERMENAKER",
    "PERMENKES": "PERMENKES", "POJK": "POJK", "PBI": "PBI",
}


def form_from_text(text):
    t = (text or "").strip()
    up = t.upper().replace(" ", "")
    if up in BPK_SHORT:
        return BPK_SHORT[up]
    for rx, form in _FORM_RE:
        if rx.search(t):
            return form
    return re.sub(r"[^A-Z]", "", t.upper())[:16] or "OTHER"


def number_int(number_raw):
    m = re.match(r"\s*(\d+)", number_raw or "")
    return str(int(m.group(1))) if m else re.sub(r"\W+", "", number_raw or "")


def make_id(form, year, number_raw):
    return f"{form}-{year}-{number_int(number_raw)}"


# Citations inside text: "Peraturan Menteri Keuangan Nomor 67 Tahun 2024",
# "PMK No. 119/PMK.07/2021", "Undang-Undang Nomor 6 Tahun 2023".
_CITE = re.compile(
    r"(?P<form>undang[- ]undang|peraturan pemerintah pengganti undang[- ]undang|peraturan pemerintah|"
    r"peraturan presiden|keputusan presiden|peraturan menteri [a-z ,/]+?|peraturan badan [a-z ,/]+?|"
    r"peraturan otoritas jasa keuangan|peraturan bank indonesia|"
    r"\b(?:uu|pp|perpres|pmk|permendag|permenperin|permenaker|permenkes|pojk|pbi|perppu)\b)"
    r"\s*(?:\([A-Za-z]+\)\s*)?(?:nomor|no\.?)\s*"
    r"(?P<num>\d+[A-Z]?(?:/[A-Z0-9.\-]+)*)"
    r"(?:\s*tahun\s*(?P<year>\d{4}))?",
    re.I,
)


def extract_citations(text):
    out = []
    seen = set()
    for m in _CITE.finditer(text or ""):
        num = m.group("num")
        year = m.group("year")
        if not year:
            ym = re.search(r"/(\d{4})$", num)
            if not ym:
                continue
            year = ym.group(1)
        form = form_from_text(m.group("form"))
        rid = make_id(form, year, num)
        if rid not in seen:
            seen.add(rid)
            out.append(rid)
    return out


if __name__ == "__main__":
    assert make_id("PMK", 2022, "204/PMK.07/2022") == "PMK-2022-204"
    assert extract_citations("Peraturan Menteri Keuangan Nomor 67 Tahun 2024 dan PMK No. 119/PMK.07/2021") == [
        "PMK-2024-67", "PMK-2021-119"]
    assert extract_citations("Undang-Undang Nomor 6 Tahun 2023 tentang Penetapan Perppu") == ["UU-2023-6"]
    print("normalize ok")
