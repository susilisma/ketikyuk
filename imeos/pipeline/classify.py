"""Topic classification and business-relevance scoring.

Rule-based on purpose: every tag must be explainable to a client ("matched
'cukai' in the title"). An LLM pass (summarize.py) can refine later, but the
index never depends on it.
"""
import re

# topic key -> (Chinese label, regex over title + subject + abstract)
TOPICS = {
    "investment": ("投资与营业许可", r"penanaman modal|investasi|perizinan berusaha|\boss\b|kbli|berbasis risiko|daftar bidang usaha|bidang usaha"),
    "tax": ("税务", r"pajak|pph|ppn|perpajakan|coretax|faktur|bea meterai|tax"),
    "customs": ("海关与进出口", r"kepabeanan|bea masuk|impor|ekspor|pabean|tarif|harmonized|\bhs\b|kawasan berikat|tempat penimbunan"),
    "excise_tobacco": ("消费税·烟草/HPTL/电子烟", r"cukai|hasil tembakau|tembakau|rokok|hptl|pengolahan tembakau lainnya|rokok elektrik|vape|nikotin"),
    "trade": ("贸易与流通", r"perdagangan|distribusi|waralaba|perdagangan melalui sistem elektronik|pmse|e-commerce|barang beredar|label"),
    "industry_sni": ("工业与SNI标准", r"perindustrian|industri|\bsni\b|standar nasional|tkdn|tingkat komponen dalam negeri|sertifikasi produk"),
    "halal": ("清真认证", r"halal|bpjph|jaminan produk"),
    "health_bpom": ("卫生/BPOM/产品注册", r"kesehatan|obat|makanan|kosmetik|bpom|pangan olahan|izin edar|alat kesehatan|suplemen"),
    "labor": ("劳动用工", r"ketenagakerjaan|tenaga kerja|pekerja|upah|pesangon|perjanjian kerja|outsourcing|alih daya|pemutusan hubungan kerja"),
    "immigration_tka": ("外籍劳工/签证/KITAS", r"imigrasi|visa|izin tinggal|kitas|kitap|tenaga kerja asing|\btka\b|rptka"),
    "social_security": ("社保BPJS", r"jaminan sosial|bpjs|jaminan kesehatan|jaminan hari tua|jaminan pensiun|jaminan kecelakaan kerja|jaminan kehilangan pekerjaan"),
    "digital": ("数字经济/数据/PSE", r"sistem elektronik|data pribadi|telekomunikasi|informatika|digital|siber|pse\b|transaksi elektronik"),
    "finance": ("金融/外汇/支付", r"bank indonesia|otoritas jasa keuangan|valuta asing|devisa|pembayaran|perbankan|fintech|lembaga keuangan|devisa hasil ekspor"),
    "environment": ("环境与AMDAL", r"lingkungan hidup|amdal|limbah|emisi|persetujuan lingkungan|ukl-upl"),
    "land_zoning": ("土地与空间规划", r"pertanahan|tata ruang|kkpr|hak guna|bangunan gedung|\bpbg\b"),
    "company_law": ("公司法与治理", r"perseroan terbatas|badan hukum|pemilik manfaat|beneficial owner|notaris|ahu"),
}
_TOPIC_RE = {k: re.compile(v[1], re.I) for k, v in TOPICS.items()}

# Weight per topic for the default "Chinese manufacturer / importer, tobacco-HPTL" profile.
PROFILES = {
    "cn_hptl_importer": {
        "label": "中国电子烟/HPTL 企业（JOIWAY 类）",
        "weights": {"excise_tobacco": 5, "customs": 4, "investment": 3, "health_bpom": 3, "trade": 3,
                    "industry_sni": 2, "tax": 3, "halal": 1, "labor": 2, "immigration_tka": 2,
                    "social_security": 1, "digital": 2, "finance": 1, "environment": 1,
                    "land_zoning": 1, "company_law": 2},
    },
    "cn_general_pma": {
        "label": "一般中资 PMA 企业",
        "weights": {"investment": 5, "tax": 4, "customs": 4, "labor": 4, "immigration_tka": 4,
                    "social_security": 3, "industry_sni": 3, "trade": 3, "halal": 2, "health_bpom": 2,
                    "company_law": 3, "environment": 2, "land_zoning": 2, "digital": 2, "finance": 2,
                    "excise_tobacco": 1},
    },
}

LOW_VALUE = re.compile(
    r"dana bagi hasil|dana alokasi|apbn|apbd|anggaran|organisasi dan tata kerja|struktur organisasi|"
    r"kedudukan protokoler|hibah daerah|tunjangan kinerja|pakaian dinas|barang milik negara", re.I)


def classify(title, subject="", abstract=""):
    text = " ".join([title or "", subject or "", (abstract or "")[:3000]])
    topics = [k for k, rx in _TOPIC_RE.items() if rx.search(text)]
    return topics


def relevance(topics, form, title, profile="cn_hptl_importer"):
    w = PROFILES[profile]["weights"]
    score = max([w.get(t, 0) for t in topics] or [0]) * 15 + min(len(topics), 4) * 5
    score += {"UU": 15, "PERPPU": 15, "PP": 12, "PERPRES": 10, "PMK": 10, "PERMENDAG": 10,
              "PERMENPERIN": 8, "PERBKPM": 10, "PERBPOM": 8, "PERMENAKER": 8}.get(form, 4)
    if LOW_VALUE.search(title or ""):
        score = min(score, 20)
    return min(score, 100)


if __name__ == "__main__":
    t = classify("Perubahan atas PMK Nomor 192/PMK.010/2021 tentang Tarif Cukai Hasil Tembakau berupa Rokok dan Hasil Pengolahan Tembakau Lainnya")
    print(t, relevance(t, "PMK", "tarif cukai"))
