"""Resolve watchlist ids (FORM-YEAR-NUMBER) to BPK records and fetch them.

Also follows one hop of amend/revoke relations so every watched regulation
has its full amendment chain available for diffing.
"""
import json
import re
from pathlib import Path

import crawl_bpk as c
from sources import BPK_JENIS

HERE = Path(__file__).parent
FORM_JENIS = {}
for jid, (form, _) in BPK_JENIS.items():
    FORM_JENIS.setdefault(form, jid)


def known_ids():
    out = {}
    for f in (HERE / "state" / "bpk").glob("*.json"):
        r = json.loads(f.read_text("utf8"))
        out[r["id"]] = r
    return out


def resolve(rid):
    form, year, number = rid.split("-", 2)
    for jenis in (FORM_JENIS.get(form), ""):
        r = c.get(f"{c.BASE}/Search", params={"keywords": "", "tentang": "", "nomor": number,
                                               "jenis": jenis or "", "tahun": year})
        if r is None:
            continue
        for bpk_id, slug in dict.fromkeys(re.findall(r'href="/Details/(\d+)/([^"]+)"', r.text)):
            rec = c.fetch_detail(bpk_id, slug)
            if rec and rec["id"] == rid:
                return rec
    return None


def run(follow=True, log=print):
    watch = json.loads((HERE / "curated" / "watchlist.json").read_text("utf8"))["ids"]
    have = known_ids()
    fetched = []
    for rid in watch:
        if rid in have:
            continue
        rec = resolve(rid)
        if rec:
            c.save(rec)
            have[rid] = rec
            fetched.append(rid)
            log(f"seed {rid}: bpk {rec['bpk_id']}")
        else:
            log(f"seed {rid}: NOT FOUND on BPK")
    if follow:
        for rid in watch:
            for rel in (have.get(rid) or {}).get("relations", []):
                tid = rel.get("target_bpk_id")
                if rel.get("target") and rel["target"] not in have and tid:
                    rec = c.fetch_detail(tid, "x")
                    if rec:
                        c.save(rec)
                        have[rec["id"]] = rec
                        fetched.append(rec["id"])
                        log(f"  follow {rid} -{rel['type']}-> {rec['id']}")
    return fetched


if __name__ == "__main__":
    run()
