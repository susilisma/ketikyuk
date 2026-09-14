# RegIntel pipeline — 印尼法规情报流水线

```
crawl_bpk.py   peraturan.bpk.go.id 列表 → 详情元数据（编号/日期/状态/修订与废止关系/PDF 链接）→ state/bpk/<bpk_id>.json
seeds.py       curated/watchlist.json 里的核心法规（FORM-YEAR-NUMBER）按编号解析并抓取，顺带抓一跳修订/废止关系
parse_pdf.py   下载 PDF → pypdf 文本层；扫描件走 PyMuPDF + Tesseract(ind) OCR；清洗页眉页脚与 OCR 伪影
articles.py    BAB/Pasal 拆分；解析 "Perubahan atas ..." 的 Pasal I 修订指令（modify/insert/delete/annex）
diff.py        把修订指令应用到旧版条文 → 合并版本；词级 Diff；附件（Lampiran）数值表对比；生效日期提取
classify.py    主题分类（规则）+ 面向中资/HPTL 企业的相关度评分
summarize.py   Claude 生成中文摘要/影响/行动项（需 ANTHROPIC_API_KEY；curated/summaries/ 里的人工版本优先）
build_site.py  汇总为静态 JSON → ../data/regintel/{index,meta,alerts}.json, docs/, diffs/, summaries/
run_daily.py   每日任务：抓当年+上年 → 刷新 watchlist → 重建站点数据（GitHub Actions: .github/workflows/regintel-daily.yml）
```

## 本地运行

```bash
pip install -r requirements.txt          # OCR 可选：另装 tesseract + tesseract-ocr-ind
python crawl_bpk.py --years 2025 2026    # 首次全量（默认所有 BPK_JENIS，按需 --jenis 42 67 ...）
python seeds.py                          # 核心法规与修订链
python build_site.py --max-text 60       # 每次最多下载解析 60 份新 PDF
```

## 维护点

- `sources.py` — BPK 的 jenis id；部委改名后 id 会变（2024-10 后 BKPM=280、Komdigi=278、Kemenkum=272、Imigrasi=289）。
- `curated/watchlist.json` — 必抓必解析的核心法规。
- `curated/summaries/<ID>.json` — 人工审核过的中文摘要，字段同 `summarize.SCHEMA`，会覆盖 AI 版本。
- `classify.py` — 主题正则与行业权重；`PROFILES` 可加新的客户画像。
- `state/` 进入 git（元数据小），`state/text/` 与 `cache/` 不进 git（由 Actions cache 保存）。

## 已知限制

- BPK 汇聚有滞后；部委 JDIH、税务局、海关、BPOM 的直连适配器（`MINISTRY_SOURCES` 中 `adapter: todo`）尚未实现。
- 扫描件 OCR 质量影响条文拆分与 Diff；`needs_ocr` 会标记。
- 修订链若缺中间版本，`diff.confidence` 降为 low 并在页面提示。
