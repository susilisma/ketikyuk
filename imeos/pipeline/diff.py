"""Diff engine.

Three kinds of change a client cares about:
  1. amendment   -- "Perubahan atas X": apply Pasal I operations to the prior
                    consolidated text of X, report old vs new per article.
  2. replacement -- a new regulation revokes X and restates the topic: align
                    articles by content similarity and diff them.
  3. annex       -- tariff/threshold tables in the Lampiran: extract money,
                    percentage and unit figures and pair them in order.
Every output carries `confidence` so the UI can ask for human review instead
of presenting a guess as fact.
"""
import difflib
import re

from articles import split_articles, parse_amendment

MONTHS = {"januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7,
          "agustus": 8, "september": 9, "oktober": 10, "november": 11, "desember": 12}


def tokens(t):
    return re.findall(r"\w+[\w.,/-]*\w|\w|[^\w\s]", t or "")


def _squash(t):
    """Undo PDF extraction noise so the diff shows legal changes, not layout: "masing - masing", "ayat ( 1)"."""
    t = re.sub(r"(\w)\s+-\s*(\w)|(\w)\s*-\s+(\w)", lambda m: (m.group(1) or m.group(3)) + "-" + (m.group(2) or m.group(4)), t or "")
    t = re.sub(r"\(\s+", "(", t)
    return re.sub(r"\s+\)", ")", t)


def _heal_split_words(text, vocab):
    """Re-join "Pasa r" -> "Pasar" when the joined form exists in the other version."""
    toks = (text or "").split(" ")
    out, i = [], 0
    while i < len(toks):
        if i + 1 < len(toks) and (toks[i] + toks[i + 1]).strip(".,;:") in vocab and toks[i].strip(".,;:") not in vocab:
            out.append(toks[i] + toks[i + 1])
            i += 2
        else:
            out.append(toks[i])
            i += 1
    return " ".join(out)


def word_diff(old, new):
    """[[op, text]] with op in = - +, merged into runs for compact JSON."""
    old, new = _squash(old), _squash(new)
    va = {w.strip(".,;:") for w in old.split()}
    vb = {w.strip(".,;:") for w in new.split()}
    new, old = _heal_split_words(new, va), _heal_split_words(old, vb)
    a, b = tokens(old), tokens(new)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            out.append(["=", " ".join(a[i1:i2])])
        else:
            if i2 > i1:
                out.append(["-", " ".join(a[i1:i2])])
            if j2 > j1:
                out.append(["+", " ".join(b[j1:j2])])
    return out


def similarity(a, b):
    return difflib.SequenceMatcher(None, tokens(a), tokens(b), autojunk=False).ratio()


def _pkey(no):
    m = re.match(r"(\d+)([A-Z]?)", no)
    return (int(m.group(1)), m.group(2)) if m else (9999, no)


# ------------------------------------------------------------------ amendment

def apply_amendment(base_articles, amend):
    """Return (new_articles, changes)."""
    arts = {a["no"]: dict(a) for a in base_articles}
    changes = []
    for op in amend["ops"]:
        if op["op"] == "modify":
            for new in op["articles"] or []:
                old = arts.get(new["no"])
                changes.append({"kind": "modified" if old else "added", "pasal": new["no"],
                                "instruction": op["instruction"],
                                "old": old["text"] if old else "", "new": new["text"],
                                "diff": word_diff(old["text"] if old else "", new["text"]),
                                "similarity": round(similarity(old["text"], new["text"]), 3) if old else 0})
                arts[new["no"]] = {"no": new["no"], "chapter": (old or {}).get("chapter"), "text": new["text"]}
            if not op["articles"]:
                changes.append({"kind": "unparsed", "pasal": op["pasal"][0], "instruction": op["instruction"]})
        elif op["op"] == "insert":
            for new in op["articles"]:
                changes.append({"kind": "added", "pasal": new["no"], "instruction": op["instruction"],
                                "old": "", "new": new["text"], "diff": [["+", new["text"]]]})
                arts[new["no"]] = {"no": new["no"], "chapter": None, "text": new["text"]}
        elif op["op"] == "delete":
            for no in op["pasal"]:
                old = arts.pop(no, None)
                changes.append({"kind": "deleted", "pasal": no, "instruction": op["instruction"],
                                "old": old["text"] if old else "", "new": "",
                                "diff": [["-", old["text"]]] if old else []})
        else:
            changes.append({"kind": op["op"], "pasal": ", ".join(op["pasal"]) or "-",
                            "instruction": op["instruction"]})
    return sorted(arts.values(), key=lambda a: _pkey(a["no"])), changes


# ---------------------------------------------------------------- replacement

def diff_replacement(old_articles, new_articles, threshold=0.45):
    changes, used = [], set()
    for new in new_articles:
        best, score = None, 0
        for old in old_articles:
            if old["no"] in used:
                continue
            s = similarity(old["text"][:1500], new["text"][:1500])
            if s > score:
                best, score = old, s
        if best is not None and score >= threshold:
            used.add(best["no"])
            if score < 0.999:
                changes.append({"kind": "modified", "pasal": new["no"], "old_pasal": best["no"],
                                "old": best["text"], "new": new["text"], "similarity": round(score, 3),
                                "diff": word_diff(best["text"], new["text"])})
        else:
            changes.append({"kind": "added", "pasal": new["no"], "old": "", "new": new["text"],
                            "diff": [["+", new["text"]]]})
    for old in old_articles:
        if old["no"] not in used:
            changes.append({"kind": "deleted", "pasal": old["no"], "old": old["text"], "new": "",
                            "diff": [["-", old["text"]]]})
    return changes


# ---------------------------------------------------------------------- annex

FIG = re.compile(r"Rp\.?\s*([\d.]+)(?:,(\d+))?\s*(?:Per\s*\n?\s*(gram|mililiter|cartridge|batang|kilogram|liter|unit|kemasan))?"
                 r"|(\d+(?:,\d+)?)\s*%", re.I)


def annex_sections(text):
    i = text.find("\nLAMPIRAN")
    lamp = text[i:] if i >= 0 else ""
    parts = re.split(r"\n(?=(?:[A-H8]\.\s+)?[A-Z][A-Z ,/]{12,}TAHUN\s+\d{4}\s*\n)", lamp)
    out = []
    for p in parts:
        title = p.strip().split("\n")[0]
        year = re.search(r"TAHUN\s+(\d{4})", title)
        figs = []
        for m in FIG.finditer(p):
            if m.group(1):
                figs.append({"value": float(m.group(1).replace(".", "") + "." + (m.group(2) or "0")),
                             "unit": (m.group(3) or "").lower(), "kind": "idr",
                             "context": re.sub(r"\s+", " ", p[max(0, m.start() - 110):m.start()]).strip()[-100:]})
            else:
                figs.append({"value": float(m.group(4).replace(",", ".")), "unit": "%", "kind": "pct",
                             "context": re.sub(r"\s+", " ", p[max(0, m.start() - 110):m.start()]).strip()[-100:]})
        if figs:
            out.append({"title": title[:160], "year": int(year.group(1)) if year else None, "figures": figs})
    return out


def _row_label(ctx):
    """Last list item ("a. Rokok Elektrik Padat") preceding a figure; the figure itself is stripped."""
    ctx = re.sub(r"Rp\.?\s*[\d.,]+\s*(?:Per\s*\w+)?", " ", ctx)
    parts = re.split(r"(?=(?:^|\s)[a-z0-9]\.\s+[A-Z])", ctx)
    return re.sub(r"\s+", " ", parts[-1] if parts else ctx).strip()


def diff_annex(old_text, new_text, row_labels=None):
    """Compare the last table in force in the old text with the first table of the new text."""
    old_s, new_s = annex_sections(old_text), annex_sections(new_text)
    if not old_s or not new_s:
        return None
    o, n = old_s[-1], new_s[0]
    of, nf = o["figures"], n["figures"]
    same_shape = len(of) == len(nf) and all(
        not x["unit"] or not y["unit"] or x["unit"] == y["unit"] for x, y in zip(of, nf))
    rows = []
    for k in range(min(len(of), len(nf))):
        a, b = of[k]["value"], nf[k]["value"]
        rows.append({"idx": k, "label": (row_labels or {}).get(k, _row_label(nf[k]["context"])), "unit": nf[k]["unit"] or of[k]["unit"],
                     "old": a, "new": b, "change_pct": round((b - a) / a * 100, 2) if a else None})
    return {"old_table": o["title"], "new_table": n["title"], "rows": rows,
            "confidence": "high" if same_shape else "low",
            "note": "" if same_shape else "表格结构不一致（常见于扫描件 OCR），需人工核对原文。"}


# --------------------------------------------------------------- dates / meta

def effective_dates(text):
    out = []
    for m in re.finditer(r"mulai\s+berlaku\s+(?:sejak|pada)\s+tanggal\s+(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text, re.I):
        mon = MONTHS.get(m.group(2).lower())
        if mon:
            ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 220):m.start()])
            out.append({"date": f"{m.group(3)}-{mon:02d}-{int(m.group(1)):02d}", "context": ctx[-220:]})
    if re.search(r"mulai\s+berlaku\s+pada\s+tanggal\s+diundangkan", text, re.I):
        out.append({"date": "on_promulgation", "context": "Peraturan ini mulai berlaku pada tanggal diundangkan."})
    return out


def diff_amendment_texts(prior_consolidated_articles, prior_text, amend_text):
    amend = parse_amendment(amend_text)
    if not amend:
        return None
    new_articles, changes = apply_amendment(prior_consolidated_articles, amend)
    annex = diff_annex(prior_text, amend_text)
    parsed_ok = all(c["kind"] != "unparsed" for c in changes)
    return {"type": "amendment", "target_text": amend["target_text"], "changes": changes, "annex": annex,
            "effective": effective_dates(amend_text), "consolidated": new_articles,
            "confidence": "high" if parsed_ok else "medium"}
