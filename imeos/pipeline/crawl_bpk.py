"""Crawler for peraturan.bpk.go.id.

    python crawl_bpk.py --years 2024 2025 2026 --jenis 42 67 10
    python crawl_bpk.py --since-days 3          # daily incremental mode

Writes one JSON per regulation to state/bpk/<bpk_id>.json. A record is
re-fetched when it is new, or when its detail page is older than
--refresh-days (status/relations change after publication, e.g. when a later
regulation revokes it).
"""
import argparse
import datetime as dt
import html
import json
import re
import time
from pathlib import Path

import requests

from normalize import form_from_text, make_id, number_int, extract_citations
from sources import BPK_JENIS

BASE = "https://peraturan.bpk.go.id"
HERE = Path(__file__).parent
STATE = HERE / "state" / "bpk"
# The WAF rejects self-identifying bot UAs with 403; stay polite via DELAY instead.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
DELAY = 1.0

MONTHS = {"januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7,
          "agustus": 8, "september": 9, "oktober": 10, "november": 11, "desember": 12}

session = requests.Session()
session.headers["User-Agent"] = UA


def get(url, **kw):
    for attempt in range(4):
        try:
            r = session.get(url, timeout=45, **kw)
            if r.status_code == 200:
                time.sleep(DELAY)
                return r
            if r.status_code == 404:
                return None
        except requests.RequestException:
            pass
        time.sleep(5 * (attempt + 1))
    return None


def id_date(s):
    m = re.match(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", (s or "").strip())
    if not m or m.group(2).lower() not in MONTHS:
        return None
    return dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1))).isoformat()


def text_lines(fragment):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", fragment, flags=re.S)
    t = re.sub(r"<br\s*/?>|</(?:div|p|li|h\d|a|span)>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return [re.sub(r"\s+", " ", l).strip() for l in t.split("\n") if l.strip()]


def list_ids(jenis, year):
    ids, page = [], 1
    while True:
        r = get(f"{BASE}/Search", params={"keywords": "", "tentang": "", "nomor": "", "jenis": jenis,
                                         "tahun": year, "p": page})
        if r is None:
            break
        found = re.findall(r'href="/Details/(\d+)/([^"]+)"', r.text)
        new = [f for f in dict.fromkeys(found) if f not in ids]
        if not new:
            break
        ids.extend(new)
        total = re.search(r"Menemukan ([\d.]+) peraturan", r.text)
        if total and len(ids) >= int(total.group(1).replace(".", "")):
            break
        page += 1
    return ids


META_KEYS = ["Tipe Dokumen", "Judul", "T.E.U.", "Nomor", "Bentuk", "Bentuk Singkat", "Tahun",
             "Tempat Penetapan", "Tanggal Penetapan", "Tanggal Pengundangan", "Tanggal Berlaku",
             "Sumber", "Subjek", "Status", "Bahasa", "Lokasi", "Bidang"]
REL_KEYS = ["Mengubah", "Diubah dengan", "Mencabut", "Dicabut dengan", "Mencabut sebagian",
            "Dicabut sebagian dengan", "Menetapkan", "Ditetapkan dengan", "Uji materi"]


def parse_detail(bpk_id, slug, page):
    lines = text_lines(page)
    meta = {}
    try:
        start = lines.index("METADATA")
    except ValueError:
        start = 0
    i = start
    while i < len(lines) - 1 and lines[i] != "UJI MATERI":
        if lines[i] in META_KEYS and lines[i + 1] not in META_KEYS and not lines[i + 1].startswith("Halaman ini"):
            meta[lines[i]] = lines[i + 1]
            i += 2
        else:
            i += 1

    # STATUS block: "Dicabut dengan :" / "PMK No. 119 Tahun 2025" / "tentang" / "<title>"
    relations = []
    s = page.find("STATUS <span")
    e = page.find("ABSTRAK PERATURAN", s)
    if s > 0:
        parts = re.split(r'bg-light-primary p-4">\s*([^<:]+?)\s*:\s*</div>', page[s:e])
        for label, body in zip(parts[1::2], parts[2::2]):
            for li in re.findall(r"<li.*?</li>", body, re.S):
                a = re.search(r'href="/Details/(\d+)/[^"]*">([^<]+)</a>', li)
                if not a:
                    continue
                name = html.unescape(a.group(2)).strip()
                cites = extract_citations(name.replace("No.", "Nomor"))
                about = re.search(r"tentang</span>\s*([^<]+)", li)
                relations.append({"type": label.strip(), "target": cites[0] if cites else None,
                                  "target_bpk_id": int(a.group(1)), "label": name,
                                  "about": html.unescape(about.group(1)).strip() if about else ""})

    abstract = ""
    m = re.search(r"ABSTRAK:(.*?)CATATAN:", "\n".join(lines), re.S)
    if m:
        abstract = m.group(1).strip()
    note = ""
    m = re.search(r"CATATAN:\n(.*?)\n(?:Tutup|\d+ hlm)", "\n".join(lines), re.S)
    if m:
        note = m.group(1).strip()

    downloads = [BASE + u for u in dict.fromkeys(re.findall(r'href="(/Download/\d+/[^"]+)"', page))]
    short = meta.get("Bentuk Singkat") or meta.get("Bentuk", "")
    form = form_from_text(short) if short else form_from_text(meta.get("Bentuk", ""))
    if form in ("PERMEN", "OTHER") or len(form) > 14:
        form = form_from_text(meta.get("Bentuk", "")) or form
    year = meta.get("Tahun") or ""
    number_raw = meta.get("Nomor", "")
    title = meta.get("Judul", "")
    about = re.split(r"\btentang\b", title, maxsplit=1, flags=re.I)
    return {
        "id": make_id(form, year, number_raw),
        "source": "bpk",
        "bpk_id": int(bpk_id),
        "url": f"{BASE}/Details/{bpk_id}/{slug}",
        "form": form,
        "form_long": meta.get("Bentuk", ""),
        "number": number_int(number_raw),
        "number_raw": number_raw,
        "year": int(year) if year.isdigit() else None,
        "title": title,
        "about": about[1].strip() if len(about) > 1 else title,
        "issuer": meta.get("T.E.U.", "").replace("Indonesia, ", ""),
        "subject": meta.get("Subjek", ""),
        "field": meta.get("Bidang", ""),
        "date_enacted": id_date(meta.get("Tanggal Penetapan")),
        "date_promulgated": id_date(meta.get("Tanggal Pengundangan")),
        "date_effective": id_date(meta.get("Tanggal Berlaku")),
        "gazette": meta.get("Sumber", ""),
        "status_bpk": meta.get("Status", ""),
        "relations": relations,
        "abstract": abstract,
        "note": note,
        "citations": extract_citations(abstract),
        "pdf": downloads,
        "fetched_at": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }


def fetch_detail(bpk_id, slug):
    r = get(f"{BASE}/Details/{bpk_id}/{slug}")
    return parse_detail(bpk_id, slug, r.text) if r else None


def save(rec):
    STATE.mkdir(parents=True, exist_ok=True)
    path = STATE / f"{rec['bpk_id']}.json"
    old = json.loads(path.read_text("utf8")) if path.exists() else None
    path.write_text(json.dumps(rec, ensure_ascii=False, indent=1), "utf8")
    return old


def crawl(jenis_list, years, refresh_days=30, log=print):
    changes = []
    for jenis in jenis_list:
        for year in years:
            ids = list_ids(jenis, year)
            log(f"jenis={jenis} ({BPK_JENIS.get(jenis, ('?',))[0]}) year={year}: {len(ids)} listed")
            for bpk_id, slug in ids:
                path = STATE / f"{bpk_id}.json"
                if path.exists():
                    old = json.loads(path.read_text("utf8"))
                    age = dt.datetime.utcnow() - dt.datetime.fromisoformat(old["fetched_at"].rstrip("Z"))
                    if age.days < refresh_days:
                        continue
                rec = fetch_detail(bpk_id, slug)
                if not rec:
                    continue
                old = save(rec)
                if old is None:
                    changes.append({"kind": "new", "id": rec["id"], "bpk_id": rec["bpk_id"]})
                elif old.get("status_bpk") != rec["status_bpk"] or old.get("relations") != rec["relations"]:
                    changes.append({"kind": "status_changed", "id": rec["id"], "bpk_id": rec["bpk_id"],
                                    "from": old.get("status_bpk"), "to": rec["status_bpk"]})
    return changes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--jenis", type=int, nargs="*", default=list(BPK_JENIS))
    ap.add_argument("--years", type=int, nargs="*")
    ap.add_argument("--refresh-days", type=int, default=30)
    a = ap.parse_args()
    years = a.years or [dt.date.today().year]
    ch = crawl(a.jenis, years, a.refresh_days)
    out = HERE / "state" / "last_changes.json"
    out.write_text(json.dumps(ch, ensure_ascii=False, indent=1), "utf8")
    print(f"{len(ch)} changes")
