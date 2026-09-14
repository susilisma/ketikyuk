"""Chinese summary + business-impact analysis via the Claude API.

Only runs for regulations above a relevance threshold that have parsed text,
and only once per text hash (results cached in state/summaries/). Without an
API credential the step is skipped and the site shows rule-based metadata only.

Env:
  ANTHROPIC_API_KEY   credential (GitHub Actions secret)
  REGINTEL_MODEL      default claude-opus-5
  REGINTEL_MAX_DOCS   cap per run, default 15
"""
import json
import os
from pathlib import Path

HERE = Path(__file__).parent
CACHE = HERE / "state" / "summaries"
MODEL = os.environ.get("REGINTEL_MODEL", "claude-opus-5")

SYSTEM = """You are an Indonesian regulatory compliance analyst serving companies that invest in or export to Indonesia (including e-cigarette/HPTL businesses).
From the regulation metadata, articles and (if present) old-vs-new diff, produce an analysis strictly grounded in the text, in THREE languages: Simplified Chinese (zh), English (en), Bahasa Indonesia (id). Every text field is an object {"zh","en","id"} with equivalent content.
Rules:
- State only what the text supports; where the text is silent, say so ("原文未明确" / "not specified in the text" / "tidak diatur dalam teks"). Never invent numbers or dates.
- Cite Pasal numbers; keep amounts in the original currency and unit.
- Keep Indonesian legal terms in Indonesian on first use, e.g. "营业执照（NIB）", "business licence (NIB)".
- Affected businesses and actions must name concrete company types and steps."""

TRI = {"type": "object", "additionalProperties": False, "required": ["zh", "en", "id"],
       "properties": {"zh": {"type": "string"}, "en": {"type": "string"}, "id": {"type": "string"}}}
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["title", "summary", "key_points", "what_changed", "effective_dates",
                 "affected", "actions", "risk_level", "joiway_note"],
    "properties": {
        "title": TRI,
        "summary": {**TRI, "description": "3-5 sentence overview in each language"},
        "key_points": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                       "required": ["pasal", "point"], "properties": {"pasal": {"type": "string"}, "point": TRI}}},
        "what_changed": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                         "required": ["pasal", "before", "after"],
                         "properties": {"pasal": {"type": "string"}, "before": TRI, "after": TRI}}},
        "effective_dates": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                            "required": ["date", "what"], "properties": {"date": {"type": "string"}, "what": TRI}}},
        "affected": {"type": "array", "items": TRI},
        "actions": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                    "required": ["who", "action", "deadline"],
                    "properties": {"who": TRI, "action": TRI, "deadline": {"type": "string"}}}},
        "risk_level": {"type": "string", "enum": ["high", "medium", "low", "info"]},
        "joiway_note": {**TRI, "description": "note for e-cigarette/HPTL companies; if irrelevant say so in each language"},
    },
}


def build_prompt(rec, doc, diff):
    parts = [
        "## 元数据", json.dumps({k: rec.get(k) for k in (
            "id", "title", "form_long", "number_raw", "year", "issuer", "date_enacted", "date_promulgated",
            "date_effective", "status", "relations", "topics")}, ensure_ascii=False, indent=1),
    ]
    if diff:
        slim = {"changes": [{k: c.get(k) for k in ("kind", "pasal", "instruction", "old", "new")}
                            for c in diff.get("changes", [])],
                "annex": diff.get("annex"), "effective": diff.get("effective")}
        parts += ["## 与上一版本的 Diff（程序生成，annex.confidence=low 时需谨慎）",
                  json.dumps(slim, ensure_ascii=False, indent=1)]
    if doc:
        body = "\n\n".join(f"Pasal {a['no']}\n{a['text']}" for a in doc.get("articles", []))
        parts += ["## 条文全文", body or doc.get("text", "")]
    return "\n\n".join(parts)


def summarize(rec, doc, diff, text_hash):
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"{rec['id']}.json"
    if out.exists():
        cached = json.loads(out.read_text("utf8"))
        if cached.get("_hash") == text_hash:
            return cached
    import anthropic  # imported lazily so the rest of the pipeline runs without the SDK

    client = anthropic.Anthropic()
    try:
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=32000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
            system=SYSTEM,
            messages=[{"role": "user", "content": build_prompt(rec, doc, diff)}],
        )
    except anthropic.RateLimitError:
        return None
    except anthropic.APIStatusError as e:
        print(f"  summarize {rec['id']}: API error {e.status_code}")
        return None
    except anthropic.APIConnectionError:
        print(f"  summarize {rec['id']}: connection error")
        return None
    if response.stop_reason in ("refusal", "max_tokens"):
        print(f"  summarize {rec['id']}: stop_reason={response.stop_reason}")
        return None
    text = next((b.text for b in response.content if b.type == "text"), None)
    if not text:
        return None
    data = json.loads(text)
    data.update({"_hash": text_hash, "_model": response.model, "_generated": "llm"})
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), "utf8")
    return data


def available():
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
