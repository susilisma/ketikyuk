/* Rules engine: wizard input -> structured market-entry report (trilingual via L/T) */
addI18N({
  "e.access": ["市场准入与结构", "Market access & structure", "Akses pasar & struktur"],
  "e.entity": ["主体设立、NIB / KBLI / OSS", "Entity, NIB / KBLI / OSS", "Badan usaha, NIB / KBLI / OSS"],
  "e.product": ["产品合规：BPOM / SNI / 清真 / 其他注册", "Product compliance: BPOM / SNI / halal / other", "Kepatuhan produk: BPOM / SNI / halal / lainnya"],
  "e.import": ["进口许可与关税", "Import licensing & duties", "Perizinan impor & bea masuk"],
  "e.tax": ["税务", "Tax", "Perpajakan"],
  "e.labor": ["用工与社保", "Employment & social security", "Ketenagakerjaan & BPJS"],
  "e.kitas": ["外籍人员签证与 KITAS", "Expat visas & KITAS", "Visa & KITAS tenaga kerja asing"],
  "e.site": ["场地、土地与环境", "Site, land & environment", "Lokasi, tanah & lingkungan"],
  "e.foreignAccess": ["外资准入：{s}", "Foreign access: {s}", "Akses asing: {s}"],
  "e.kbliSuggest": ["建议 KBLI：", "Suggested KBLI: ", "KBLI yang disarankan: "],
  "e.kbliRisk": ["KBLI 风险等级以 OSS 系统实时判定为准", "KBLI risk levels are determined live by OSS", "Tingkat risiko KBLI ditentukan OSS secara langsung"],
  "e.threshOk": ["投资额门槛：满足", "Investment threshold: met", "Ambang investasi: terpenuhi"],
  "e.threshNo": ["投资额门槛：未满足", "Investment threshold: not met", "Ambang investasi: belum terpenuhi"],
  "e.threshBody": ["计划投资 Rp{n} 亿；要求每个 5 位 KBLI、每个地点 > Rp100 亿（不含土地建筑），实缴资本 ≥ Rp100 亿。", "Planned investment Rp{n}bn; required > Rp10bn per 5-digit KBLI per location (excl. land & buildings), paid-up capital ≥ Rp10bn.", "Rencana investasi Rp{n} miliar; wajib > Rp10 miliar per KBLI 5 digit per lokasi (di luar tanah & bangunan), modal disetor ≥ Rp10 miliar."],
  "e.threshFix": ["选项：减少 KBLI 数量、集中在一个地点、先以代表处或分销商模式启动，或提高投资计划（投资额为承诺，按 LKPM 逐步落实）。", "Options: fewer KBLIs, one location, start with a rep office or distributor, or raise the plan (the figure is a commitment realised via LKPM).", "Opsi: kurangi KBLI, satu lokasi, mulai dengan kantor perwakilan/distributor, atau naikkan rencana (angka adalah komitmen yang direalisasikan lewat LKPM)."],
  "e.mode": ["进入模式：{m}", "Entry mode: {m}", "Mode masuk: {m}"],
  "e.pros": ["优势：", "Advantages: ", "Keunggulan: "], "e.cons": ["限制：", "Limits: ", "Keterbatasan: "],
  "e.retail": ["零售环节受限", "Retail is restricted", "Ritel dibatasi"],
  "e.retailBody": ["线下零售（KBLI 47xxx）多数保留给本地企业；外资仅可经营大型业态（超市 ≥1,200 m²、百货 ≥400 m²）。建议 PMA 持批发 KBLI，通过本地零售商/特许经营/平台完成零售。", "Offline retail (KBLI 47xxx) is mostly reserved for locals; foreigners may only run large formats (supermarkets ≥1,200 m², department stores ≥400 m²). Hold wholesale KBLIs in the PMA and retail through local retailers, franchising or marketplaces.", "Ritel luring (KBLI 47xxx) sebagian besar untuk lokal; asing hanya format besar (supermarket ≥1.200 m², department store ≥400 m²). PMA memegang KBLI perdagangan besar dan ritel lewat peritel lokal, waralaba, atau marketplace."],
  "e.ecom": ["电商与平台", "E-commerce & platforms", "E-commerce & platform"],
  "e.ecomBody1": ["电商 PMA（KBLI 47919x/63122）需投资 > Rp1,000 亿；否则以批发 PMA 身份作为平台商家入驻。", "An e-commerce PMA (KBLI 47919x/63122) needs > Rp100bn; otherwise sell on marketplaces as a wholesale PMA.", "PMA e-commerce (KBLI 47919x/63122) perlu > Rp100 miliar; jika tidak, berjualan di marketplace sebagai PMA perdagangan besar."],
  "e.ecomBody2": ["面向印尼用户的网站/APP 须 PSE 注册；社交媒体不得直接完成交易（Permendag 31/2023）。", "Sites/apps for Indonesian users need PSE registration; no direct transactions on social media (Permendag 31/2023).", "Situs/aplikasi untuk pengguna Indonesia wajib PSE; tidak boleh transaksi langsung di media sosial (Permendag 31/2023)."],
  "e.steps": ["设立步骤", "Set-up steps", "Langkah pendirian"],
  "e.ossOut": ["OSS 风险分级与许可产出", "OSS risk levels & licence outputs", "Tingkat risiko OSS & keluaran izin"],
  "e.ossNib": ["NIB 同时作为进口识别号（API-U 贸易型 / API-P 生产型，二选一）、海关注册号和 SPPL 环境承诺。", "The NIB doubles as importer ID (API-U trading / API-P producer, one only), customs registration and SPPL undertaking.", "NIB sekaligus API (API-U dagang / API-P produsen, pilih satu), registrasi kepabeanan, dan SPPL."],
  "e.ongoing": ["设立后持续义务", "Ongoing obligations", "Kewajiban berkelanjutan"],
  "e.apiClash": ["API-P 与 API-U 冲突", "API-P vs API-U conflict", "Konflik API-P dan API-U"],
  "e.apiClashBody": ["生产型企业持 API-P 只能进口自用原料/设备，不得进口成品转售；如需贸易成品，需另设贸易公司或申请 API-P 成品进口例外。", "An API-P producer may only import inputs/equipment for its own use, not finished goods for resale; trading finished goods needs a separate trading company or the API-P exception for complementary goods.", "Produsen API-P hanya boleh mengimpor bahan/mesin untuk kebutuhan sendiri, bukan barang jadi untuk dijual; perlu perusahaan dagang terpisah atau pengecualian barang komplementer."],
  "e.noCert": ["未识别到强制产品认证", "No mandatory product certification identified", "Tidak ada sertifikasi produk wajib yang teridentifikasi"],
  "e.noCertBody": ["仍需印尼语标签与流通规定；请用 HS 编码在“进口许可查询”页复核。", "Indonesian labelling and distribution rules still apply; re-check by HS code on the Import Lookup page.", "Label berbahasa Indonesia dan ketentuan peredaran tetap berlaku; periksa ulang kode HS di halaman Cek Impor."],
  "e.weeksCost": ["周期约 {a}–{b} 周", "About {a}–{b} weeks", "Sekitar {a}–{b} minggu"], "e.cost": ["费用约 {a}–{b}", "Cost about {a}–{b}", "Biaya sekitar {a}–{b}"],
  "e.agency": ["主管：{a}。适用：{w}", "Authority: {a}. Applies to: {w}", "Instansi: {a}. Berlaku untuk: {w}"],
  "e.impQual": ["进口资质", "Importer status", "Status importir"],
  "e.impPma": ["NIB 载明 API（API-U 或 API-P）；海关注册随 NIB 生效；建议委托报关行 PPJK。", "The NIB carries the API (API-U or API-P); customs registration is automatic; use a customs broker (PPJK).", "NIB memuat API (API-U atau API-P); registrasi kepabeanan otomatis; gunakan PPJK."],
  "e.impLocal": ["以印尼进口商（持 API-U）为进口记录人；你方为境外供应商，负责 CFS、检测报告等文件。", "The Indonesian importer (API-U) is importer of record; you supply CFS, test reports and other documents.", "Importir Indonesia (API-U) sebagai importir tercatat; Anda menyediakan CFS, hasil uji, dan dokumen lain."],
  "e.insw": ["通过 INSW（insw.go.id）按 HS 编码核对 Lartas 清单。", "Check restrictions (lartas) by HS code on INSW (insw.go.id).", "Periksa lartas per kode HS di INSW (insw.go.id)."],
  "e.hsRef": ["参考 KBLI：{k}", "Reference KBLI: {k}", "KBLI rujukan: {k}"],
  "e.hsVerify": ["税率与管制以 INSW/BTKI 2022 当前版本为准", "Rates and controls per the current INSW/BTKI 2022", "Tarif dan kendali sesuai INSW/BTKI 2022 terkini"],
  "e.hsUnknown": ["知识库暂无该编码规则；请到 INSW 查询。", "No rule for this code yet; check INSW.", "Belum ada aturan untuk kode ini; periksa INSW."],
  "e.impTax": ["进口税费结构", "Import tax stack", "Struktur pungutan impor"],
  "e.impTax1": ["关税（MFN 或 ACFTA/RCEP 协定税率，需原产地证）+ 增值税 11% + PPh 22（持 API 2.5%，无 API 7.5%）+ 如适用的奢侈品税与消费税。", "Duty (MFN or ACFTA/RCEP with certificate of origin) + VAT 11% + PPh 22 (2.5% with API, 7.5% without) + luxury tax and excise where applicable.", "Bea masuk (MFN atau ACFTA/RCEP dengan SKA) + PPN 11% + PPh 22 (2,5% dengan API, 7,5% tanpa) + PPnBM dan cukai bila berlaku."],
  "e.impTax2": ["增值税与 PPh 22 可抵扣；反倾销/保障措施税不可抵扣。", "VAT and PPh 22 are creditable; anti-dumping/safeguard duties are not.", "PPN dan PPh 22 dapat dikreditkan; BMAD/BMTP tidak."],
  "e.impTax3": ["保税区或 KITE 可暂免原料税费；Masterlist 可免设备关税。", "Bonded zones or KITE suspend duties on inputs; Masterlist exempts capital goods.", "Kawasan Berikat atau KITE menangguhkan pungutan bahan baku; Masterlist membebaskan bea masuk mesin."],
  "e.noImport": ["本方案不涉及进口环节", "No import step in this plan", "Rencana ini tidak mencakup impor"],
  "e.noImportBody": ["如后续进口设备/原料，需在 NIB 中启用 API-P 并核对 Lartas。", "If you later import equipment/inputs, enable API-P on the NIB and check lartas.", "Jika nanti mengimpor mesin/bahan, aktifkan API-P pada NIB dan periksa lartas."],
  "e.citVat": ["企业所得税与增值税", "Corporate income tax & VAT", "PPh Badan & PPN"],
  "e.cit": ["企业所得税 {r}；{s}", "Corporate income tax {r}; {s}", "PPh Badan {r}; {s}"], "e.vat": ["增值税：{s}", "VAT: {s}", "PPN: {s}"],
  "e.pkp": ["年营收 > Rp48 亿必须登记 PKP 并使用 e-Faktur。", "Revenue > Rp4.8bn must register as PKP and use e-Faktur.", "Omzet > Rp4,8 miliar wajib PKP dan e-Faktur."],
  "e.wht": ["预提税与中印税收协定", "Withholding tax & the China–Indonesia treaty", "Pemotongan pajak & P3B Tiongkok–Indonesia"],
  "e.tp": ["关联交易与转让定价", "Related-party transactions & transfer pricing", "Transaksi afiliasi & transfer pricing"],
  "e.tpBody": ["母公司收取的管理费/特许权使用费须有真实性证明，否则不得扣除且补征 PPh 26。", "Management fees/royalties charged by the parent need substance evidence or they are non-deductible with PPh 26 assessed.", "Biaya manajemen/royalti dari induk wajib dibuktikan substansinya, jika tidak, tidak dapat dibiayakan dan dikenai PPh 26."],
  "e.filing": ["申报节奏", "Filing calendar", "Kalender pelaporan"],
  "e.incent": ["可争取的税收优惠", "Available tax incentives", "Insentif pajak yang dapat diupayakan"],
  "e.incentV": ["Tax Holiday 2025 年后续期情况需核实", "Confirm the tax-holiday extension after 2025", "Konfirmasi perpanjangan tax holiday setelah 2025"],
  "e.tobTax": ["烟草制品三层税负", "Three-layer tobacco tax burden", "Tiga lapis pungutan hasil tembakau"],
  "e.tobTaxBody": ["定价倒算：HJE ≥ 最低零售价；消费税 + 9.9%×HJE 增值税 + 10%×消费税烟草税。用“计算器 → HPTL 消费税”测算。", "Price backwards: HJE ≥ minimum; excise + VAT 9.9%×HJE + cigarette tax 10%×excise. Use Calculators → HPTL excise.", "Hitung mundur: HJE ≥ minimum; cukai + PPN 9,9%×HJE + Pajak Rokok 10%×cukai. Gunakan Kalkulator → Cukai HPTL."],
  "e.minWage": ["最低工资参考：{r} {v}/月（2025）", "Minimum wage reference: {r} {v}/month (2025)", "Acuan upah minimum: {r} {v}/bulan (2025)"],
  "e.laborCost": ["按 {n} 名员工、平均工资 1.5 倍最低工资估算，年人力成本（含雇主 BPJS、THR）约 {v}", "For {n} staff at 1.5× minimum wage, annual labour cost (incl. employer BPJS, THR) ≈ {v}", "Untuk {n} pekerja dengan 1,5× upah minimum, biaya tenaga kerja tahunan (termasuk BPJS pemberi kerja, THR) ≈ {v}"],
  "e.umpV": ["2026 年最低工资以省长决定为准", "2026 minimum wages per governor decrees", "Upah minimum 2026 sesuai keputusan gubernur"],
  "e.contracts": ["合同与工时", "Contracts & working hours", "Kontrak & waktu kerja"],
  "e.bpjs": ["社保 BPJS（雇主负担约工资的 10–12%）", "BPJS (employer share ≈ 10–12% of wages)", "BPJS (beban pemberi kerja ≈ 10–12% upah)"],
  "e.bpjsTk": ["劳动保障：JKK {j}（按风险等级）+ JKM 0.30% + JHT 3.7% + JP 2%（基数上限 {c}）", "Employment: JKK {j} (by risk class) + JKM 0.30% + JHT 3.7% + JP 2% (cap {c})", "Ketenagakerjaan: JKK {j} (per kelas risiko) + JKM 0,30% + JHT 3,7% + JP 2% (batas {c})"],
  "e.bpjsKes": ["健康保障：雇主 4% + 员工 1%，基数上限 {c}", "Health: employer 4% + employee 1%, cap {c}", "Kesehatan: pemberi kerja 4% + pekerja 1%, batas {c}"],
  "e.jpV": ["JP 基数上限每年调整", "The JP cap is adjusted yearly", "Batas JP disesuaikan tiap tahun"],
  "e.sever": ["解雇成本", "Termination cost", "Biaya PHK"], "e.oblig": ["用工合规义务", "Employment compliance", "Kepatuhan ketenagakerjaan"],
  "e.noStaff": ["暂无本地雇员", "No local employees yet", "Belum ada pekerja lokal"],
  "e.noStaffBody": ["分销商员工不得受你方直接指挥，否则有劳动关系与 PE 风险。", "Do not direct the distributor's staff, or employment and PE risks arise.", "Jangan mengarahkan pekerja distributor secara langsung, agar tidak timbul risiko hubungan kerja dan BUT."],
  "e.expats": ["外籍人员 {n} 名：办理路径", "{n} expatriates: process", "{n} TKA: alur"], "e.expatStep": ["{a}：{b}（约 {w1}–{w2} 周）", "{a}: {b} (~{w1}–{w2} weeks)", "{a}: {b} (±{w1}–{w2} minggu)"],
  "e.notes": ["注意事项", "Notes", "Catatan"], "e.tkaV": ["劳工部新 TKA 条例可能替换 Permenaker 8/2021", "A new Manpower TKA regulation may replace Permenaker 8/2021", "Permenaker TKA baru dapat menggantikan Permenaker 8/2021"],
  "e.fees": ["费用", "Fees", "Biaya"], "e.kitasFee": ["工作 KITAS 每人约 {a}–{b}，另 DKP-TKA USD {d}/人/年", "Work KITAS ≈ {a}–{b} per person, plus DKP-TKA USD {d} per person per year", "KITAS kerja ≈ {a}–{b} per orang, ditambah DKP-TKA USD {d}/orang/tahun"],
  "e.expatTax": ["外籍人员薪酬缴 PPh 21（税务居民）并加入 BPJS（居留 ≥ 6 个月）。", "Expat pay is subject to PPh 21 (residents) and BPJS (stay ≥ 6 months).", "Gaji TKA dikenai PPh 21 (SPDN) dan BPJS (tinggal ≥ 6 bulan)."],
  "e.noExpat": ["无常驻外籍人员", "No resident expatriates", "Tanpa TKA menetap"],
  "e.noExpatBody": ["短期考察使用商务签证不得从事有偿工作；超过 60 天或需工作的技术人员应办理短期 RPTKA + 工作签证。", "Business visas do not allow paid work; technicians beyond 60 days or doing work need a short-term RPTKA + work visa.", "Visa bisnis tidak mengizinkan bekerja; teknisi lebih dari 60 hari atau yang bekerja perlu RPTKA jangka pendek + visa kerja."],
  "e.envLevel": ["环境文件等级：{l}", "Environmental document: {l}", "Dokumen lingkungan: {l}"],
  "e.landBld": ["土地与厂房", "Land & buildings", "Tanah & bangunan"],
  "e.officeSite": ["办公/仓储场地", "Office / warehouse premises", "Kantor / gudang"],
  "e.officeBody1": ["租赁写字楼或仓库即可；注意租金预提税（PPh 4(2) 10%）与增值税。", "Lease an office or warehouse; note rent withholding (PPh 4(2) 10%) and VAT.", "Sewa kantor atau gudang; perhatikan PPh 4(2) 10% atas sewa dan PPN."],
  "e.officeBody2": ["仓库若存放待清关进口货物需海关保税仓许可。", "Storing uncleared imports needs a bonded-warehouse licence.", "Menyimpan barang impor belum diselesaikan perlu izin gudang berikat."],
  /* checklist groups & items */
  "c.inc": ["公司设立", "Incorporation", "Pendirian"], "c.rep": ["代表处", "Rep office", "Kantor perwakilan"], "c.dist": ["分销商", "Distributor", "Distributor"], "c.prod": ["产品合规", "Product compliance", "Kepatuhan produk"], "c.imp": ["进口", "Import", "Impor"], "c.tax": ["税务", "Tax", "Pajak"], "c.lab": ["用工", "Employment", "Ketenagakerjaan"], "c.exp": ["外籍人员", "Expatriates", "TKA"], "c.site": ["场地", "Site", "Lokasi"], "c.exc": ["消费税", "Excise", "Cukai"], "c.risk": ["风险应对", "Risk actions", "Mitigasi risiko"],
  "c.i1": ["确定 KBLI 组合与投资计划（每 KBLI > Rp100 亿）", "Fix KBLI set and investment plan (> Rp10bn per KBLI)", "Tetapkan KBLI dan rencana investasi (> Rp10 miliar per KBLI)"],
  "c.i2": ["股东决议、章程条款", "Shareholder resolutions, articles", "Keputusan pemegang saham, anggaran dasar"],
  "c.i3": ["股东文件公证认证与宣誓翻译", "Legalised, sworn-translated shareholder documents", "Dokumen pemegang saham dilegalisasi dan diterjemahkan tersumpah"],
  "c.i4": ["名称预留、公证处签署 Akta", "Name reservation, sign the deed", "Pemesanan nama, tanda tangan akta"],
  "c.i5": ["取得 SK Kemenkumham、NPWP", "Obtain SK and NPWP", "Peroleh SK dan NPWP"],
  "c.i6": ["OSS 注册 NIB、勾选 API 类型", "Register NIB on OSS, choose API type", "Daftar NIB di OSS, pilih jenis API"],
  "c.i7": ["银行开户并实缴资本", "Open bank account, inject capital", "Buka rekening, setor modal"],
  "c.i8": ["首次 LKPM 与 BO 申报", "First LKPM and BO filing", "LKPM pertama dan pelaporan BO"],
  "c.r1": ["总公司授权书与章程认证", "Parent's appointment letter and articles legalised", "Surat penunjukan dan anggaran dasar dilegalisasi"], "c.r2": ["BKPM/贸易部代表处许可", "BKPM/Trade rep-office licence", "Izin kantor perwakilan BKPM/Kemendag"], "c.r3": ["首席代表 KITAS", "Chief representative KITAS", "KITAS kepala perwakilan"],
  "c.m1": ["INSW 核对每个 HS 编码", "Check every HS code on INSW", "Periksa setiap kode HS di INSW"], "c.m2": ["原产地证（Form E / RCEP）安排", "Arrange certificates of origin (Form E / RCEP)", "Siapkan SKA (Form E / RCEP)"], "c.m3": ["委托报关行，测试首单", "Appoint a broker, run a test shipment", "Tunjuk PPJK, uji pengiriman pertama"],
  "c.t1": ["注册 Coretax 与 e-Faktur", "Register on Coretax and e-Faktur", "Daftar Coretax dan e-Faktur"], "c.t2": ["确定会计政策与转让定价文档", "Set accounting policy and TP documentation", "Tetapkan kebijakan akuntansi dan dokumen TP"], "c.t3": ["月度申报日历", "Monthly filing calendar", "Kalender pelaporan bulanan"],
  "c.l1": ["劳动合同模板本地化", "Localise employment contracts", "Lokalisasi kontrak kerja"], "c.l2": ["BPJS 企业登记", "BPJS company registration", "Registrasi BPJS perusahaan"], "c.l3": ["公司规章（≥10 人）报批", "Company regulation (≥10 staff) ratified", "Peraturan Perusahaan (≥10 pekerja) disahkan"], "c.l4": ["WLTK 劳动力报告", "WLTK manpower report", "WLTK"], "c.l5": ["工资结构与最低工资核对", "Wage scale vs minimum wage", "Struktur upah vs upah minimum"],
  "c.s1": ["工业园区选址与 KKPR", "Industrial-estate site and KKPR", "Lokasi kawasan industri dan KKPR"], "c.s2": ["环境文件 {l}", "Environmental document {l}", "Dokumen lingkungan {l}"], "c.s3": ["PBG/SLF 核对", "Check PBG/SLF", "Periksa PBG/SLF"], "c.s4": ["PLN 电力报装", "PLN power connection", "Sambungan listrik PLN"],
  "c.e1": ["NPPBKC 申请", "NPPBKC application", "Permohonan NPPBKC"], "c.e2": ["商标与 HJE 核定", "Brand and HJE determination", "Penetapan merek dan HJE"], "c.e3": ["税票订购与 CEISA 开通", "Stamp ordering and CEISA activation", "Pemesanan pita cukai dan aktivasi CEISA"], "c.e4": ["PP 28/2024 包装与渠道合规审查", "PP 28/2024 packaging and channel review", "Kajian kemasan dan saluran sesuai PP 28/2024"],
});

window.ENGINE = (() => {
  const K = () => window.KB;
  const sectorOf = (id) => K().sectors.find((s) => s.id === id) || K().sectors.find((s) => s.id === "other");

  function hsMatches(codes) {
    const out = [];
    for (const raw of codes) {
      const c = raw.replace(/[^0-9.]/g, "");
      if (c.length < 4) continue;
      let best = null;
      for (const row of K().hs) {
        const [pref] = row;
        const ok = pref.includes("-") ? (() => { const [a, b] = pref.split("-"); const n = +c.slice(0, 4); return n >= +a && n <= +b; })() : c.replace(".", "").startsWith(pref.replace(".", ""));
        if (ok && (!best || pref.length > best[0].length)) best = row;
      }
      out.push({ code: raw, row: best });
    }
    return out;
  }

  function build(input) {
    const S = sectorOf(input.sector);
    const mode = K().entryModes[input.mode];
    const acts = input.activities;
    const hs = hsMatches(input.hs);
    const certIds = [...new Set([...S.certs, ...(acts.includes("ecommerce") ? ["pse"] : [])])].filter((c) => K().certs[c]);
    const lartasIds = [...new Set([...S.lartas, ...hs.flatMap((h) => h.row ? h.row[2] : [])])];
    const envLevel = acts.includes("manufacture") ? (input.investment >= 200 || ["steel", "energy", "auto"].includes(S.id) ? "AMDAL" : "UKL-UPL") : "SPPL";
    const sections = [];
    const push = (key, items) => sections.push({ n: sections.length + 1, key, title: T("e." + key), items });
    const Ls = (arr) => arr.map(L);

    const access = [];
    access.push({ title: T("e.foreignAccess", { s: L(S.zh) }), body: [L(S.foreign.note), T("e.kbliSuggest") + S.kbli.map(([c, n, r]) => `${c} ${L(n)} (${L(K().ossRisk[r]?.zh) || r})`).join("; ")], refs: ["PERPRES-2021-10", "PERPRES-2021-49"], v: T("e.kbliRisk") });
    if (input.mode === "pma") {
      const ok = input.investment >= 10;
      access.push({ title: ok ? T("e.threshOk") : T("e.threshNo"), body: [T("e.threshBody", { n: num(input.investment) }), ...(ok ? [] : [T("e.threshFix")]), ...Ls(K().pma.notes.slice(1, 3))], refs: ["PERBKPM-2021-4"], tag: ok ? "ok" : "bad" });
    }
    access.push({ title: T("e.mode", { m: L(mode.zh) }), body: [T("e.pros") + Ls(mode.pros).join("; "), T("e.cons") + Ls(mode.cons).join("; ")], refs: input.mode === "pma" ? ["UU-2007-25", "UU-2007-40"] : input.mode === "ecom" ? ["PERMENDAG-2020-50"] : [] });
    if (acts.includes("retail")) access.push({ title: T("e.retail"), body: [T("e.retailBody")], refs: ["PERPRES-2021-10"], tag: "warn" });
    if (acts.includes("ecommerce")) access.push({ title: T("e.ecom"), body: [T("e.ecomBody1"), T("e.ecomBody2")], refs: ["PERMENDAG-2020-50", "PERMENKOMINFO-2020-5"] });
    push("access", access);

    const ent = [];
    ent.push({ title: T("e.steps"), body: Ls(mode.steps), refs: input.mode === "pma" ? ["UU-2007-40", "PP-2025-28"] : ["PP-2025-28"] });
    if (input.mode === "pma") {
      ent.push({ title: T("e.ossOut"), body: S.kbli.map(([c, n, r]) => `${c}: ${L(K().ossRisk[r]?.need) || "OSS"}`).concat([T("e.ossNib")]), refs: ["PP-2025-28"] });
      ent.push({ title: T("e.ongoing"), body: Ls(K().pma.reporting), refs: ["PERBKPM-2021-5", "PERPRES-2018-13"] });
      if (acts.includes("import") && acts.includes("manufacture")) ent.push({ title: T("e.apiClash"), body: [T("e.apiClashBody")], tag: "warn", refs: ["PERMENDAG-2025-16"] });
    }
    push("entity", ent);

    const certs = certIds.map((id) => {
      const c = K().certs[id];
      const meta = [c.weeks[1] ? T("e.weeksCost", { a: c.weeks[0], b: c.weeks[1] }) : "", c.cost[1] ? T("e.cost", { a: idr(c.cost[0], { short: true }), b: idr(c.cost[1], { short: true }) }) : ""].filter(Boolean).join("; ");
      return { title: L(c.zh), body: [T("e.agency", { a: L(c.agency), w: L(c.who) }), ...Ls(c.how), ...(meta ? [meta] : [])], refs: c.regs, v: c.v ? L(c.v) : null };
    });
    if (!certs.length) certs.push({ title: T("e.noCert"), body: [T("e.noCertBody")], refs: ["PERMENDAG-2021-25"] });
    push("product", certs);

    const imp = [];
    if (acts.includes("import") || input.mode !== "pma") {
      imp.push({ title: T("e.impQual"), body: [input.mode === "pma" ? T("e.impPma") : T("e.impLocal"), T("e.insw")], refs: ["PERMENDAG-2025-16"] });
      for (const l of lartasIds) { const x = K().lartas[l]; if (x) imp.push({ title: L(x.zh), body: [], refs: x.ref ? [x.ref] : [], v: x.v ? L(x.v) : null }); }
      for (const h of hs) imp.push(h.row ? { title: `HS ${h.code} · ${L(h.row[1])}`, body: [L(h.row[3]), T("e.hsRef", { k: h.row[4] })], refs: [], v: T("e.hsVerify") } : { title: `HS ${h.code}`, body: [T("e.hsUnknown")], refs: [] });
      imp.push({ title: T("e.impTax"), body: [T("e.impTax1"), T("e.impTax2"), T("e.impTax3")], refs: ["PMK-2022-26", "PMK-2024-131"] });
    } else imp.push({ title: T("e.noImport"), body: [T("e.noImportBody")], refs: [] });
    push("import", imp);

    const X = K().tax;
    const tax = [
      { title: T("e.citVat"), body: [T("e.cit", { r: pct(X.cit, 0), s: L(X.citSmallReduction) }), T("e.vat", { s: L(X.vatNote) }), T("e.pkp")], refs: ["UU-2021-7", "PMK-2024-131"] },
      { title: T("e.wht"), body: X.wht.map((w) => `${w[0]} | ${L(w[1])} | ${L(w[2])}`), refs: ["UU-2021-7"] },
      { title: T("e.tp"), body: [L(X.tp), T("e.tpBody")], refs: ["PMK-2023-172"] },
      { title: T("e.filing"), body: Ls(X.compliance), refs: [] },
    ];
    if (input.mode === "pma" && input.investment >= 100) tax.push({ title: T("e.incent"), body: Ls(X.incentives), refs: ["PMK-2020-130"], v: T("e.incentV") });
    if (S.excise) tax.push({ title: T("e.tobTax"), body: [L(K().excise.note), T("e.tobTaxBody")], refs: ["PMK-2024-96", "PMK-2022-63", "PMK-2023-143"] });
    push("tax", tax);

    const Lb = K().labor, lab = [];
    if (input.staff > 0) {
      const ump = Lb.ump2025.find((u) => u[0] === input.province) || Lb.ump2025[0];
      lab.push({ title: T("e.minWage", { r: ump[0], v: idr(ump[1]) }), body: [L(Lb.minWage), L(Lb.umpNote), T("e.laborCost", { n: input.staff, v: idr(input.staff * ump[1] * 1.5 * 13.6, { short: true }) })], refs: ["PP-2021-36", "PP-2023-51"], v: T("e.umpV") });
      lab.push({ title: T("e.contracts"), body: Ls([Lb.pkwt, Lb.pkwtt, Lb.hours, Lb.thr]), refs: ["PP-2021-35", "PERMENAKER-2016-6"] });
      lab.push({ title: T("e.bpjs"), body: [T("e.bpjsTk", { j: K().bpjs.tk.jkk.map((j) => (j[1] * 100).toFixed(2) + "%").join("/"), c: idr(K().bpjs.tk.jpCap) }), T("e.bpjsKes", { c: idr(K().bpjs.kes.cap) }), L(K().bpjs.tk.jkp)], refs: [], v: T("e.jpV") });
      lab.push({ title: T("e.sever"), body: Ls(Lb.severance), refs: ["PP-2021-35"] });
      lab.push({ title: T("e.oblig"), body: Ls(Lb.obligations), refs: ["UU-2003-13", "UU-2023-6"] });
    } else lab.push({ title: T("e.noStaff"), body: [T("e.noStaffBody")], refs: [] });
    push("labor", lab);

    const tk = [];
    if (input.expats > 0) {
      tk.push({ title: T("e.expats", { n: input.expats }), body: K().tka.steps.map((s) => T("e.expatStep", { a: L(s[0]), b: L(s[1]), w1: s[2][0], w2: s[2][1] })), refs: ["PP-2021-34", "PERMENAKER-2021-8", "UU-2011-6"] });
      tk.push({ title: T("e.notes"), body: Ls(K().tka.notes), refs: ["KEPMENAKER-2019-349", "PERMENKUMHAM-2023-22"], v: T("e.tkaV") });
      tk.push({ title: T("e.fees"), body: [T("e.kitasFee", { a: idr(K().tka.cost.kitasWork[0], { short: true }), b: idr(K().tka.cost.kitasWork[1], { short: true }), d: K().tka.cost.dkptkaUsdPerYear }), T("e.expatTax")], refs: [] });
    } else tk.push({ title: T("e.noExpat"), body: [T("e.noExpatBody")], refs: ["UU-2011-6"] });
    push("kitas", tk);

    const site = [];
    if (acts.includes("manufacture") || input.land === "buy") {
      site.push({ title: T("e.envLevel", { l: envLevel }), body: K().site.env.map((e) => `${e[0]}: ${L(e[1])} — ${L(e[2])}`), refs: ["PP-2021-22"] });
      site.push({ title: T("e.landBld"), body: Ls(K().site.land).concat(Ls(K().site.building)), refs: [] });
    } else site.push({ title: T("e.officeSite"), body: [T("e.officeBody1"), T("e.officeBody2")], refs: [] });
    push("site", site);

    const start = input.startDate ? new Date(input.startDate) : new Date();
    const base = K().timeline[input.mode] || K().timeline.pma;
    const phases = [];
    let cursor = 0;
    base.forEach(([name, lo, hi, crit], idx) => {
      const zh = name[0];
      if (zh.startsWith("NPPBKC") && !S.excise) return;
      if (zh.startsWith("外籍") && !input.expats) return;
      if (zh.startsWith("场地") && !(acts.includes("manufacture") || input.land === "buy")) return;
      if (zh.startsWith("产品认证") && !certIds.length) return;
      const dur = input.urgency === "fast" ? lo : Math.round((lo + hi) / 2);
      const s = crit ? cursor : Math.max(2, cursor - 2);
      phases.push({ name: L(name), start: s, end: s + dur, crit, lo, hi });
      if (crit) cursor = s + dur;
    });
    const total = Math.max(...phases.map((p) => p.end));
    const timeline = { start: dateISO(start), phases, totalWeeks: total, goLive: dateISO(addWeeks(start, total)) };

    const risks = K().risks.filter((r) => { try { return r.when(input, S); } catch (e) { return false; } }).map((r) => ({ ...r, zh: L(r.zh), detail: L(r.detail) }));
    const budget = CALC.setupBudget(input, certIds, envLevel);

    const checklist = [];
    const add = (g, t, m) => checklist.push({ group: T(g), text: t, meta: m || "" });
    if (input.mode === "pma") ["c.i1", "c.i2", "c.i3", "c.i4", "c.i5", "c.i6", "c.i7", "c.i8"].forEach((k) => add("c.inc", T(k)));
    if (input.mode === "rep") ["c.r1", "c.r2", "c.r3"].forEach((k) => add("c.rep", T(k)));
    if (input.mode === "distributor") K().entryModes.distributor.steps.forEach((t) => add("c.dist", L(t)));
    certIds.forEach((c) => add("c.prod", L(K().certs[c].zh), K().certs[c].weeks[1] ? `${K().certs[c].weeks[0]}–${K().certs[c].weeks[1]} ${T("week")}` : ""));
    if (acts.includes("import") || input.mode !== "pma") { add("c.imp", T("c.m1")); lartasIds.forEach((l) => K().lartas[l] && add("c.imp", L(K().lartas[l].zh))); add("c.imp", T("c.m2")); add("c.imp", T("c.m3")); }
    ["c.t1", "c.t2", "c.t3"].forEach((k) => add("c.tax", T(k)));
    if (input.staff > 0) ["c.l1", "c.l2", "c.l3", "c.l4", "c.l5"].forEach((k) => add("c.lab", T(k)));
    if (input.expats > 0) K().tka.steps.forEach((s) => add("c.exp", L(s[0])));
    if (acts.includes("manufacture")) [T("c.s1"), T("c.s2", { l: envLevel }), T("c.s3"), T("c.s4")].forEach((t) => add("c.site", t));
    if (S.excise) ["c.e1", "c.e2", "c.e3", "c.e4"].forEach((k) => add("c.exc", T(k)));
    risks.forEach((r) => add("c.risk", r.zh));

    return { input, sector: S, mode, sections, certIds, lartasIds, hs, envLevel, timeline, risks, budget, checklist, generated: new Date().toISOString() };
  }

  return { build, sectorOf, hsMatches };
})();
