"""Turn crawl state into the static JSON the website reads.

    python build_site.py                 # full rebuild from state/
    python build_site.py --max-text 40   # download/parse at most 40 new PDFs this run

Outputs (imeos/data/regintel/):
  index.json            compact list of every regulation
  meta.json             counts, sources, generated_at
  alerts.json           recent, relevant changes with diff headlines
  docs/<ID>.json        parsed articles (+ consolidated text when amended)
  diffs/<ID>.json       old-vs-new for amending regulations
"""
import argparse
import datetime as dt
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

import articles as A
import classify as C
import diff as D
import parse_pdf as P
from normalize import extract_citations
from sources import AGENCIES, BPK_JENIS, MINISTRY_SOURCES

HERE = Path(__file__).parent
STATE = HERE / "state"
OUT = HERE.parent / "data" / "regintel"
CURATED = HERE / "curated"
TODAY = dt.date.today().isoformat()

ISSUER_AGENCY = [
    (r"keuangan", "kemenkeu"), (r"perdagangan", "kemendag"), (r"perindustrian", "kemenperin"),
    (r"investasi|penanaman modal", "bkpm"), (r"ketenagakerjaan|tenaga kerja", "kemnaker"),
    (r"kesehatan", "kemenkes"), (r"pengawas obat", "bpom"), (r"hukum", "kemenkumham"),
    (r"komunikasi|digital|informatika", "komdigi"), (r"bank indonesia", "bi"),
    (r"otoritas jasa keuangan", "ojk"), (r"standardisasi", "bsn"), (r"pertanian", "kementan"),
    (r"pemerintah pusat|presiden|dewan perwakilan|sekretariat negara", "presiden"),
]


def agency_of(issuer, form):
    if form in ("UU", "PERPPU", "PP", "PERPRES", "KEPPRES", "INPRES"):
        return "presiden" if form != "UU" else "dpr_presiden"
    for rx, key in ISSUER_AGENCY:
        if re.search(rx, issuer or "", re.I):
            return key
    return "various"


def load_records():
    recs = {}
    for f in (STATE / "bpk").glob("*.json"):
        r = json.loads(f.read_text("utf8"))
        if not r.get("year"):
            continue
        prev = recs.get(r["id"])
        if prev is None or r["fetched_at"] > prev["fetched_at"]:
            recs[r["id"]] = r
    return recs


def compute_status(recs):
    """Merge forward relations (from each record) with reverse edges (from others)."""
    inbound = defaultdict(list)
    for r in recs.values():
        for rel in r.get("relations", []):
            if rel.get("target"):
                inbound[rel["target"]].append((rel["type"], r["id"]))
    for rid, r in recs.items():
        types = {t for t, _ in inbound.get(rid, [])} | {x["type"] for x in r.get("relations", [])}
        amended_by = sorted({x["target"] for x in r["relations"] if x["type"] == "Diubah dengan" and x.get("target")}
                            | {src for t, src in inbound.get(rid, []) if t == "Mengubah"})
        revoked_by = sorted({x["target"] for x in r["relations"] if x["type"] == "Dicabut dengan" and x.get("target")}
                            | {src for t, src in inbound.get(rid, []) if t == "Mencabut"})
        partial = "Dicabut sebagian dengan" in types or any(t == "Mencabut sebagian" for t, _ in inbound.get(rid, []))
        if revoked_by or r.get("status_bpk") == "Tidak Berlaku":
            status = "revoked"
        elif r.get("date_effective") and r["date_effective"] > TODAY:
            status = "not_yet_effective"
        elif partial:
            status = "partially_revoked"
        elif amended_by:
            status = "amended"
        else:
            status = "in_force" if r.get("status_bpk") == "Berlaku" else "unknown"
        r["status"], r["amended_by"], r["revoked_by"] = status, amended_by, revoked_by


def text_for(rec, budget):
    """Parsed text, cached per PDF URL. Returns (payload, downloaded?)."""
    if not rec.get("pdf"):
        return None, False
    cache = STATE / "text" / f"{rec['id']}.json"
    key = hashlib.sha1(rec["pdf"][0].encode()).hexdigest()
    if cache.exists():
        c = json.loads(cache.read_text("utf8"))
        if c.get("pdf_key") == key:
            return c, False
    if budget <= 0:
        return None, False
    try:
        ex = P.extract(P.download(rec["pdf"][0]))
    except Exception as e:  # network / corrupt PDF: skip, retry next run
        print(f"  pdf fail {rec['id']}: {e}")
        return None, True
    split = A.split_articles(ex["text"])
    payload = {"id": rec["id"], "pdf_key": key, "sha1": ex["sha1"], "pages": ex["pages"],
               "ocr_pages": ex["ocr_pages"], "needs_ocr": ex["needs_ocr"], "text": ex["text"],
               "articles": split["articles"], "preamble": split["preamble"][:6000],
               "amendment": A.parse_amendment(ex["text"])}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(payload, ensure_ascii=False), "utf8")
    return payload, True


def amendment_target(texts_rec, rec):
    am = texts_rec.get("amendment") if texts_rec else None
    if am:
        cites = extract_citations(am["target_text"])
        if cites:
            return cites[0]
    for rel in rec.get("relations", []):
        if rel["type"] == "Mengubah" and rel.get("target"):
            return rel["target"]
    m = re.search(r"Perubahan\s+(?:\w+\s+)?atas\s+(.+)", rec.get("title", ""), re.I)
    if m:
        cites = extract_citations(m.group(1))
        if cites:
            return cites[0]
    return None


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), "utf8")


def build(max_text=40, min_relevance=55, summarize_docs=True):
    recs = load_records()
    compute_status(recs)
    seeds = set(json.loads((CURATED / "watchlist.json").read_text("utf8"))["ids"])

    for r in recs.values():
        r["topics"] = C.classify(r["title"], r.get("subject"), r.get("abstract"))
        r["relevance"] = C.relevance(r["topics"], r["form"], r["title"])
        r["agency"] = agency_of(r.get("issuer"), r["form"])
        if r["id"] in seeds:
            r["relevance"] = max(r["relevance"], 90)

    # ---- text: seeds and relevant documents first, then amendment chains they touch
    budget = max_text
    texts = {}
    order = sorted(recs.values(), key=lambda r: (r["id"] not in seeds, -r["relevance"], r.get("date_enacted") or ""))
    for r in order:
        if r["id"] not in seeds and r["relevance"] < min_relevance:
            continue
        t, downloaded = text_for(r, budget)
        budget -= downloaded
        if t:
            texts[r["id"]] = t
    # amended bases of relevant amendments need text too, regardless of their own score
    for rid in list(texts):
        tgt = amendment_target(texts[rid], recs[rid])
        if tgt and tgt in recs and tgt not in texts:
            t, downloaded = text_for(recs[tgt], max(budget, 1))
            budget -= downloaded
            if t:
                texts[tgt] = t

    # ---- diffs along amendment chains
    chains = defaultdict(list)
    for rid, t in texts.items():
        tgt = amendment_target(t, recs[rid])
        if t.get("amendment") and tgt:
            chains[tgt].append(rid)
            recs[rid]["amends"] = tgt
    diffs = {}
    for base, amends in chains.items():
        if base not in texts:
            continue
        amends.sort(key=lambda i: recs[i].get("date_enacted") or "")
        cur_articles, prior_text, prior_id = texts[base]["articles"], texts[base]["text"], base
        for aid in amends:
            d = D.diff_amendment_texts(cur_articles, prior_text, texts[aid]["text"])
            if not d:
                continue
            consolidated = d.pop("consolidated")
            d.update({"id": aid, "base": base, "prior_version": prior_id,
                      "base_title": recs[base]["title"], "title": recs[aid]["title"],
                      "missing_prior_amendments": [x for x in recs[base].get("amended_by", [])
                                                   if x not in amends and
                                                   (recs.get(x, {}).get("date_enacted") or "") < (recs[aid].get("date_enacted") or "")]})
            if d["missing_prior_amendments"]:
                d["confidence"] = "low"
            diffs[aid] = d
            write(OUT / "diffs" / f"{aid}.json", d)
            cur_articles, prior_text, prior_id = consolidated, texts[aid]["text"], aid
        write(OUT / "docs" / f"{base}.consolidated.json",
              {"id": base, "as_of": prior_id, "articles": cur_articles})
        recs[base]["consolidated_as_of"] = prior_id

    for rid, t in texts.items():
        write(OUT / "docs" / f"{rid}.json", {
            "id": rid, "pages": t["pages"], "needs_ocr": t["needs_ocr"], "ocr_pages": t["ocr_pages"],
            "articles": t["articles"], "effective": D.effective_dates(t["text"]),
            "amendment_ops": [{k: o.get(k) for k in ("op", "pasal", "instruction")}
                              for o in (t.get("amendment") or {}).get("ops", [])]})

    # ---- summaries: curated (human-reviewed) beats LLM
    summaries = {}
    for f in (CURATED / "summaries").glob("*.json"):
        s = json.loads(f.read_text("utf8"))
        s["_generated"] = "curated"
        summaries[f.stem] = s
    if summarize_docs:
        import summarize as S
        if S.available():
            todo = [rid for rid in texts if rid not in summaries and recs[rid]["relevance"] >= 70]
            todo.sort(key=lambda i: recs[i].get("date_promulgated") or "", reverse=True)
            for rid in todo[:int(__import__("os").environ.get("REGINTEL_MAX_DOCS", 15))]:
                s = S.summarize(recs[rid], texts[rid], diffs.get(rid), texts[rid]["sha1"])
                if s:
                    summaries[rid] = s
        cache = STATE / "summaries"
        for f in cache.glob("*.json") if cache.exists() else []:
            summaries.setdefault(f.stem, json.loads(f.read_text("utf8")))
    for rid, s in summaries.items():
        write(OUT / "summaries" / f"{rid}.json", s)

    # ---- index
    index = []
    for r in sorted(recs.values(), key=lambda r: (r.get("date_enacted") or "", r["id"]), reverse=True):
        index.append({
            "id": r["id"], "f": r["form"], "n": r["number_raw"], "y": r["year"], "t": r["about"],
            "ag": r["agency"], "de": r.get("date_enacted"), "dp": r.get("date_promulgated"),
            "dv": r.get("date_effective"), "st": r["status"], "tp": r["topics"], "rv": r["relevance"],
            "ab": r["amended_by"], "rb": r["revoked_by"], "am": r.get("amends"),
            "rel": [[x["type"], x["target"], x["label"]] for x in r["relations"] if x.get("target")],
            "u": r["url"], "pdf": (r.get("pdf") or [None])[0],
            "tx": r["id"] in texts, "df": r["id"] in diffs, "sm": r["id"] in summaries,
            "ca": r.get("consolidated_as_of"),
        })
    write(OUT / "index.json", index)

    # ---- alerts: recent + relevant, newest first
    horizon = (dt.date.today() - dt.timedelta(days=120)).isoformat()
    alerts = []
    for r in recs.values():
        d = r.get("date_promulgated") or r.get("date_enacted") or ""
        if d < horizon or r["relevance"] < 50:
            continue
        a = {"id": r["id"], "date": d, "title": r["title"], "status": r["status"], "relevance": r["relevance"],
             "topics": r["topics"], "agency": r["agency"], "effective": r.get("date_effective"),
             "kind": "amendment" if r.get("amends") else ("revocation" if any(
                 x["type"] == "Mencabut" for x in r["relations"]) else "new")}
        if r["id"] in diffs:
            dd = diffs[r["id"]]
            a["diff_headline"] = {
                "modified": sum(c["kind"] == "modified" for c in dd["changes"]),
                "added": sum(c["kind"] == "added" for c in dd["changes"]),
                "deleted": sum(c["kind"] == "deleted" for c in dd["changes"]),
                "annex_rows_changed": sum(1 for x in (dd.get("annex") or {}).get("rows", []) if x["old"] != x["new"]),
            }
        if r["id"] in summaries:
            a["summary_zh"] = summaries[r["id"]].get("summary_zh")
            a["risk_level"] = summaries[r["id"]].get("risk_level")
        alerts.append(a)
    alerts.sort(key=lambda a: (a["date"], a["relevance"]), reverse=True)
    write(OUT / "alerts.json", alerts)

    counts = defaultdict(int)
    for r in recs.values():
        counts[r["status"]] += 1
    write(OUT / "meta.json", {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "total": len(recs), "with_text": len(texts), "diffs": len(diffs), "summaries": len(summaries),
        "status_counts": counts, "agencies": AGENCIES,
        "topics": {k: v[0] for k, v in C.TOPICS.items()},
        "forms": sorted({r["form"] for r in recs.values()}),
        "sources": [{"name": "Database Peraturan BPK", "url": "https://peraturan.bpk.go.id/", "adapter": "live"}]
                   + MINISTRY_SOURCES,
        "bpk_jenis_crawled": [v[0] for v in BPK_JENIS.values()],
    })
    print(f"index {len(index)} | text {len(texts)} | diffs {len(diffs)} | summaries {len(summaries)} | alerts {len(alerts)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-text", type=int, default=40)
    ap.add_argument("--min-relevance", type=int, default=55)
    ap.add_argument("--no-summarize", action="store_true")
    a = ap.parse_args()
    build(a.max_text, a.min_relevance, not a.no_summarize)
