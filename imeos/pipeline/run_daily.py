"""Daily job: crawl current + previous year, refresh watchlist, rebuild site data.

Run by .github/workflows/regintel-daily.yml; safe to run locally.
"""
import datetime as dt
import json
from pathlib import Path

import build_site
import crawl_bpk
import seeds

HERE = Path(__file__).parent
# Business-relevant central forms. Full coverage (all BPK_JENIS) is a weekly job: pass --all.
DAILY_JENIS = [8, 9, 10, 11, 42, 67, 69, 75, 280, 105, 217, 106, 278, 46, 272, 289, 182, 230, 199, 297, 195, 196, 267, 80, 212, 78, 79, 225, 214]


def main(all_jenis=False):
    year = dt.date.today().year
    jenis = list(crawl_bpk.BPK_JENIS) if all_jenis else DAILY_JENIS
    # list pages are cheap; details are only re-fetched when new or older than refresh-days
    changes = crawl_bpk.crawl(jenis, [year, year - 1], refresh_days=14)
    seeds.run()
    log = HERE / "state" / "changes_log.jsonl"
    with log.open("a", encoding="utf8") as f:
        for ch in changes:
            f.write(json.dumps({**ch, "seen": dt.date.today().isoformat()}, ensure_ascii=False) + "\n")
    build_site.build(max_text=60)
    print(f"daily done: {len(changes)} changes")


if __name__ == "__main__":
    import sys
    main("--all" in sys.argv)
