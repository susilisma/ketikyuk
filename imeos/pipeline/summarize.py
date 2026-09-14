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

SYSTEM = """你是印尼法规合规分析师，服务对象是在印尼投资或出口到印尼的中国企业（含电子烟/HPTL 企业）。
根据提供的法规元数据、条文和（如有）新旧条文 Diff，输出严格基于原文的中文分析。
规则：
- 只陈述原文能支持的内容；原文没有写明的，写"原文未明确"，不要推测数字或日期。
- 引用条款时写明 Pasal 编号；金额保留原币种和单位。
- 印尼法律术语第一次出现时保留印尼语原词，如"营业执照（NIB）"。
- 受影响企业和行动建议要具体到企业类型与动作，避免空泛表述。"""

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["title_zh", "summary_zh", "key_points", "what_changed", "effective_dates",
                 "affected", "actions", "risk_level", "joiway_note"],
    "properties": {
        "title_zh": {"type": "string"},
        "summary_zh": {"type": "string", "description": "3-5 句概述"},
        "key_points": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                       "required": ["pasal", "point"],
                       "properties": {"pasal": {"type": "string"}, "point": {"type": "string"}}}},
        "what_changed": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                         "required": ["pasal", "before", "after"],
                         "properties": {"pasal": {"type": "string"}, "before": {"type": "string"},
                                        "after": {"type": "string"}}}},
        "effective_dates": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                            "required": ["date", "what"],
                            "properties": {"date": {"type": "string"}, "what": {"type": "string"}}}},
        "affected": {"type": "array", "items": {"type": "string"}},
        "actions": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                    "required": ["who", "action", "deadline"],
                    "properties": {"who": {"type": "string"}, "action": {"type": "string"},
                                   "deadline": {"type": "string"}}}},
        "risk_level": {"type": "string", "enum": ["high", "medium", "low", "info"]},
        "joiway_note": {"type": "string", "description": "对电子烟/HPTL 中资企业的专门提示；无关则写'无直接影响'"},
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
            max_tokens=16000,
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
