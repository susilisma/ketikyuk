"""Split regulation text into chapters (BAB) and articles (Pasal), and parse
amendment instructions of "Perubahan atas ..." regulations.
"""
import re

PASAL = re.compile(r"^Pasal\s+(\d+[A-Z]?)\s*$")
PASAL_ROMAN = re.compile(r"^Pasal\s+([IVXL]+)\s*$")
BAB = re.compile(r"^BAB\s+([IVXLC]+[A-Z]?)\s*$")
STOP = re.compile(r"^(PENJELASAN\s*$|PENJELASAN\s+ATAS|LAMPIRAN\s*$|LAMPIRAN\s+[IVX]*\s*$)")


def split_articles(text):
    """Return {"preamble": str, "articles": [{"no", "chapter", "text"}], "closing": str}."""
    lines = text.split("\n")
    # Consideranda ("Menimbang/Mengingat") cite other laws' articles on their own lines; skip past them.
    head = next((i for i, l in enumerate(lines) if l.strip().startswith("MEMUTUSKAN")), None)
    if head is not None:
        pre, lines = lines[:head], lines[head:]
    else:
        pre = []
    articles, preamble, chapter = [], pre, None
    cur, closing, pending_bab = None, [], None
    last_num = 0
    for i, raw in enumerate(lines):
        line = raw.strip()
        if STOP.match(line) and articles:
            closing = lines[i:]
            break
        m = BAB.match(line)
        if m:
            pending_bab = [m.group(1)]
            continue
        if pending_bab is not None and len(pending_bab) == 1 and line and not PASAL.match(line):
            chapter = f"BAB {pending_bab[0]} {line}"
            pending_bab = None
            continue
        m = PASAL.match(line)
        if m:
            n = int(re.match(r"\d+", m.group(1)).group(0))
            # Guard against a cross-reference wrapped onto its own line ("... dalam\nPasal 3\nayat (2)").
            nxt = next((l.strip() for l in lines[i + 1:i + 3] if l.strip()), "")
            if nxt.startswith("ayat") or (articles and n < last_num - 1 and not m.group(1)[-1].isalpha()):
                if cur is not None:
                    cur["text"].append(line)
                continue
            cur = {"no": m.group(1), "chapter": chapter, "text": []}
            articles.append(cur)
            last_num = n
            continue
        if cur is None:
            preamble.append(line)
        else:
            cur["text"].append(line)
    for a in articles:
        a["text"] = reflow("\n".join(a["text"]))
    # the closing formula ("Peraturan ... mulai berlaku ... Ditetapkan di Jakarta") trails the last article
    if articles:
        tail = re.split(r"\n(?=Agar setiap orang mengetahuinya|Ditetapkan di )", articles[-1]["text"], maxsplit=1)
        if len(tail) == 2:
            articles[-1]["text"] = tail[0].strip()
            closing = [tail[1]] + closing
    return {"preamble": reflow("\n".join(preamble)), "articles": articles, "closing": "\n".join(closing)[:4000]}


def reflow(t):
    """Join PDF line wraps but keep ayat "(1)", list "a." and "1." items on their own lines."""
    out = []
    for line in t.split("\n"):
        line = line.strip()
        if not line:
            continue
        starts_item = re.match(r"^(\(\d+[a-z]?\)|[a-z]\.|\d+\.|[a-z]\)|\d+\))\s", line)
        if out and not starts_item and not out[-1].endswith((":", ";")):
            out[-1] += " " + line
        else:
            out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------- amendments

AMEND_HEAD = re.compile(
    r"(?:Beberapa\s+)?ketentuan\s+dalam\s+(?P<target>.+?)\s+(?:diubah|diubah\s+dan\s+ditambah)\s+sebagai\s+berikut\s*:",
    re.I | re.S)
ITEM = re.compile(r"(?:^|\n)(\d{1,3})\.\s+(?=(?:Ketentuan|Di\s+antara|Pasal|BAB|Lampiran|Penjelasan|Judul|Diantara|Setelah|Ketentuan))", re.I)
OP_MODIFY = re.compile(r"Ketentuan\b.*?Pasal\s+(\d+[A-Z]?)\b.*?diubah", re.I | re.S)
OP_MODIFY_TARGET = re.compile(r"sehingga\s+Pasal\s+(\d+[A-Z]?)\s+berbunyi", re.I)
OP_INSERT = re.compile(r"(?:Di\s*antara|Setelah)\s+Pasal\s+(\d+[A-Z]?)(?:\s+dan\s+Pasal\s+(\d+[A-Z]?))?\s+disisipkan\s+(?:\d+\s*\([a-z ]+\)\s*)?pasal,?\s+yak(?:ni|itu)\s+(.+?)\s+sehingga", re.I | re.S)
OP_DELETE = re.compile(r"^Pasal\s+(\d+[A-Z]?)\s+dihapus", re.I)
OP_ANNEX = re.compile(r"Lampiran", re.I)


def parse_amendment(text):
    """Parse "Pasal I" of an amending regulation into operations.

    Returns {"target_text": str, "ops": [{"op": modify|insert|delete|other, "pasal": [..], "new_text": str, "instruction": str}]}
    """
    m = AMEND_HEAD.search(text)
    if not m:
        return None
    body = text[m.end():]
    end = re.search(r"\n\s*Pasal\s+II\s*\n", body)
    if end:
        body = body[:end.start()]
    target_text = re.sub(r"\s+", " ", m.group("target"))

    starts = [(mm.start(), mm.group(1)) for mm in ITEM.finditer("\n" + body)]
    chunks = []
    for k, (pos, num) in enumerate(starts):
        nxt = starts[k + 1][0] if k + 1 < len(starts) else len(body) + 1
        chunks.append(("\n" + body)[pos:nxt].strip())
    ops = []
    for ch in chunks:
        ch = re.sub(r"^\d{1,3}\.\s+", "", ch)
        instr, _, rest = ch.partition("\n")
        # instruction sentences can wrap across lines; they end with "berikut:" or a full stop
        ins_m = re.match(r"(.+?(?:sebagai\s+berikut\s*:|dihapus\.?|bagian\s+tidak\s+terpisahkan\s+dari\s+Peraturan[^.]*\.))\s*(.*)$", ch, re.S | re.I)
        instruction = re.sub(r"\s+", " ", ins_m.group(1)) if ins_m else re.sub(r"\s+", " ", instr)
        new_block = ins_m.group(2) if ins_m else rest
        parsed = split_articles(new_block)["articles"] if new_block else []
        if OP_DELETE.match(instruction):
            ops.append({"op": "delete", "pasal": [OP_DELETE.match(instruction).group(1)], "instruction": instruction})
        elif (mi := OP_INSERT.search(instruction)):
            names = re.findall(r"Pasal\s+(\d+[A-Z]?)", mi.group(3))
            ops.append({"op": "insert", "after": mi.group(1), "pasal": names or [a["no"] for a in parsed],
                        "articles": parsed, "instruction": instruction})
        elif (mm2 := OP_MODIFY.search(instruction)):
            tgt = OP_MODIFY_TARGET.search(instruction)
            ops.append({"op": "modify", "pasal": [tgt.group(1) if tgt else mm2.group(1)], "articles": parsed,
                        "instruction": instruction})
        elif parsed and re.search(r"disisipkan|ditambahkan", instruction, re.I):
            ops.append({"op": "insert", "after": None, "pasal": [x["no"] for x in parsed], "articles": parsed,
                        "instruction": instruction})
        else:
            kind = "annex" if OP_ANNEX.search(instruction[:40]) else "other"
            ops.append({"op": kind, "pasal": [a["no"] for a in parsed], "articles": parsed,
                        "instruction": instruction, "raw": new_block[:3000]})
    return {"target_text": target_text, "ops": ops}
