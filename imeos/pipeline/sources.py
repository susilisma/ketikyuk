"""Source registry for Indonesia Regulatory Intelligence.

Two layers:
  1. BPK_JENIS  -- peraturan.bpk.go.id aggregates most central-government
     regulations with structured metadata (status, amend/revoke relations,
     PDF). This is the primary crawl backbone.
  2. MINISTRY_SOURCES -- ministry JDIH portals. Used for documents BPK lags on
     (Surat Edaran, Keputusan Dirjen, technical guides) and as the
     authoritative copy for verification. Each entry carries `adapter`:
     "bpk" means covered through layer 1; "todo" means an adapter still has to
     be written for that portal.
"""

# jenis id on peraturan.bpk.go.id -> (short form, issuing body key)
BPK_JENIS = {
    8: ("UU", "dpr_presiden"),
    9: ("PERPPU", "presiden"),
    10: ("PP", "presiden"),
    11: ("PERPRES", "presiden"),
    12: ("KEPPRES", "presiden"),
    13: ("INPRES", "presiden"),
    42: ("PMK", "kemenkeu"),
    66: ("KMK", "kemenkeu"),
    67: ("PERMENDAG", "kemendag"),
    68: ("KEPMENDAG", "kemendag"),
    69: ("PERMENPERIN", "kemenperin"),
    70: ("KEPMENPERIN", "kemenperin"),
    75: ("PERBKPM", "bkpm"),          # Kementerian Investasi/BKPM (until Oct 2024)
    280: ("PERBKPM", "bkpm"),         # Kementerian Investasi dan Hilirisasi/BKPM (from Oct 2024)
    105: ("PERMENAKER", "kemnaker"),
    217: ("KEPMENAKER", "kemnaker"),
    106: ("PERMENKOMINFO", "komdigi"),  # Kominfo (until Oct 2024)
    278: ("PERMENKOMDIGI", "komdigi"),  # Komunikasi dan Digital
    46: ("PERMENKUMHAM", "kemenkumham"),
    272: ("PERMENKUM", "kemenkumham"),  # Kementerian Hukum (from Oct 2024)
    289: ("PERMENIMIPAS", "imigrasi"),  # Imigrasi dan Pemasyarakatan
    182: ("PERMENKES", "kemenkes"),
    183: ("KEPMENKES", "kemenkes"),
    230: ("PERBPOM", "bpom"),
    199: ("PERBPOM", "bpom"),          # older "Peraturan Kepala BPOM"
    297: ("PERBPJPH", "bpjph"),
    195: ("PERBPJSKES", "bpjs"),
    196: ("PERBPJSTK", "bpjs"),
    267: ("PERBPJSTK", "bpjs"),
    78: ("PBI", "bi"),
    79: ("SEBI", "bi"),
    80: ("POJK", "ojk"),
    212: ("SEOJK", "ojk"),
    225: ("PERBSN", "bsn"),
    134: ("PERMENTAN", "kementan"),
    89: ("PERKPPU", "kppu"),
    178: ("PERBPBATAM", "various"),    # BP Batam free-trade zone
    214: ("SE", "various"),
    15: ("PERMEN", "various"),
    14: ("PERLEMBAGA", "various"),
}

AGENCIES = {
    "dpr_presiden": {"zh": "国会与总统", "en": "Parliament & President", "id": "DPR & Presiden"},
    "presiden": {"zh": "总统", "en": "President", "id": "Presiden"},
    "kemenkeu": {"zh": "财政部", "en": "Ministry of Finance", "id": "Kementerian Keuangan"},
    "djp": {"zh": "税务总局", "en": "Directorate General of Taxes", "id": "Direktorat Jenderal Pajak"},
    "djbc": {"zh": "海关与消费税总局", "en": "Customs & Excise", "id": "Direktorat Jenderal Bea dan Cukai"},
    "kemendag": {"zh": "贸易部", "en": "Ministry of Trade", "id": "Kementerian Perdagangan"},
    "kemenperin": {"zh": "工业部", "en": "Ministry of Industry", "id": "Kementerian Perindustrian"},
    "bkpm": {"zh": "投资部/BKPM", "en": "Ministry of Investment/BKPM", "id": "Kementerian Investasi/BKPM"},
    "kemenkes": {"zh": "卫生部", "en": "Ministry of Health", "id": "Kementerian Kesehatan"},
    "bpom": {"zh": "食品药品监督管理局 BPOM", "en": "BPOM (Food & Drug Authority)", "id": "BPOM"},
    "kemnaker": {"zh": "劳工部", "en": "Ministry of Manpower", "id": "Kementerian Ketenagakerjaan"},
    "imigrasi": {"zh": "移民总局", "en": "Immigration", "id": "Direktorat Jenderal Imigrasi"},
    "kemenkumham": {"zh": "法律部", "en": "Ministry of Law", "id": "Kementerian Hukum"},
    "bpjs": {"zh": "社保 BPJS", "en": "BPJS (social security)", "id": "BPJS"},
    "komdigi": {"zh": "通信与数字部", "en": "Ministry of Communication & Digital", "id": "Kementerian Komunikasi dan Digital"},
    "bi": {"zh": "印尼央行", "en": "Bank Indonesia", "id": "Bank Indonesia"},
    "ojk": {"zh": "金融服务管理局 OJK", "en": "OJK (Financial Services Authority)", "id": "Otoritas Jasa Keuangan"},
    "bsn": {"zh": "国家标准局 BSN", "en": "BSN (National Standards)", "id": "Badan Standardisasi Nasional"},
    "bpjph": {"zh": "清真产品认证机构 BPJPH", "en": "BPJPH (Halal Agency)", "id": "BPJPH"},
    "kementan": {"zh": "农业部", "en": "Ministry of Agriculture", "id": "Kementerian Pertanian"},
    "kppu": {"zh": "商业竞争监督委员会 KPPU", "en": "KPPU (Competition Commission)", "id": "KPPU"},
    "various": {"zh": "其他部门", "en": "Other agencies", "id": "Instansi lain"},
}

MINISTRY_SOURCES = [
    {"agency": "jdihn", "name": "JDIH Nasional", "url": "https://jdihn.go.id/", "adapter": "todo"},
    {"agency": "setneg", "name": "peraturan.go.id (Kemenkum)", "url": "https://peraturan.go.id/", "adapter": "todo"},
    {"agency": "kemenkeu", "name": "JDIH Kemenkeu", "url": "https://jdih.kemenkeu.go.id/", "adapter": "bpk"},
    {"agency": "djp", "name": "Peraturan Pajak DJP", "url": "https://pajak.go.id/id/peraturan", "adapter": "todo"},
    {"agency": "djbc", "name": "JDIH Bea Cukai", "url": "https://jdih.beacukai.go.id/", "adapter": "todo"},
    {"agency": "kemendag", "name": "JDIH Kemendag", "url": "https://jdih.kemendag.go.id/", "adapter": "bpk"},
    {"agency": "kemenperin", "name": "JDIH Kemenperin", "url": "https://jdih.kemenperin.go.id/", "adapter": "bpk"},
    {"agency": "bkpm", "name": "JDIH BKPM", "url": "https://jdih.bkpm.go.id/", "adapter": "bpk"},
    {"agency": "kemenkes", "name": "JDIH Kemenkes", "url": "https://jdih.kemkes.go.id/", "adapter": "todo"},
    {"agency": "bpom", "name": "JDIH BPOM", "url": "https://jdih.pom.go.id/", "adapter": "todo"},
    {"agency": "kemnaker", "name": "JDIH Kemnaker", "url": "https://jdih.kemnaker.go.id/", "adapter": "bpk"},
    {"agency": "imigrasi", "name": "JDIH Imigrasi", "url": "https://jdih.imigrasi.go.id/", "adapter": "todo"},
    {"agency": "bpjs", "name": "BPJS Ketenagakerjaan Regulasi", "url": "https://www.bpjsketenagakerjaan.go.id/", "adapter": "todo"},
    {"agency": "komdigi", "name": "JDIH Komdigi", "url": "https://jdih.komdigi.go.id/", "adapter": "bpk"},
    {"agency": "bi", "name": "Peraturan BI", "url": "https://www.bi.go.id/id/publikasi/peraturan/", "adapter": "bpk"},
    {"agency": "ojk", "name": "Regulasi OJK", "url": "https://www.ojk.go.id/id/regulasi/", "adapter": "bpk"},
    {"agency": "bpjph", "name": "JDIH BPJPH", "url": "https://jdih.halal.go.id/", "adapter": "todo"},
]
