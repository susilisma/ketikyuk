/* Rules engine: wizard input -> structured market-entry report */
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
        const ok = pref.includes("-")
          ? (() => { const [a, b] = pref.split("-"); const n = +c.slice(0, 4); return n >= +a && n <= +b; })()
          : c.replace(".", "").startsWith(pref.replace(".", ""));
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
    const push = (key, title, items) => sections.push({ n: sections.length + 1, key, title, items });

    /* 1. Market access */
    const access = [];
    access.push({ title: `外资准入：${S.zh}`, body: [S.foreign.note, `建议 KBLI：` + S.kbli.map(([c, n, r]) => `${c} ${n}（${K().ossRisk[r]?.zh || r}）`).join("；")], refs: ["PERPRES-2021-10", "PERPRES-2021-49"], v: "KBLI 风险等级以 OSS 系统实时判定为准" });
    if (input.mode === "pma") {
      const ok = input.investment >= 10;
      access.push({ title: ok ? "投资额门槛：满足" : "投资额门槛：未满足", body: [`计划投资 Rp${num(input.investment)} 亿；要求每个 5 位 KBLI、每个地点 > Rp100 亿（不含土地建筑），实缴资本 ≥ Rp100 亿。`, ...(ok ? [] : ["选项：减少 KBLI 数量、集中在一个地点、先以代表处或分销商模式启动，或提高投资计划（投资额为计划承诺，按 LKPM 逐步落实）。"]), ...K().pma.notes.slice(1, 3)], refs: ["PERBKPM-2021-4"], tag: ok ? "ok" : "bad" });
    }
    access.push({ title: `进入模式：${mode.zh}`, body: ["优势：" + mode.pros.join("；"), "限制：" + mode.cons.join("；")], refs: input.mode === "pma" ? ["UU-2007-25", "UU-2007-40"] : input.mode === "ecom" ? ["PERMENDAG-2020-50"] : [] });
    if (acts.includes("retail")) access.push({ title: "零售环节受限", body: ["线下零售（KBLI 47xxx）多数保留给本地企业；外资仅可经营大型业态（超市 ≥1,200 m²、百货 ≥400 m² 等，有条件）。建议：PMA 持批发 KBLI，通过本地零售商/特许经营/平台完成零售。"], refs: ["PERPRES-2021-10"], tag: "warn" });
    if (acts.includes("ecommerce")) access.push({ title: "电商与平台", body: ["电商 PMA（KBLI 47919x/63122）需投资 > Rp1,000 亿；否则以批发 PMA 身份作为平台商家入驻。", "面向印尼用户的网站/APP 须 PSE 注册；社交媒体不得直接完成交易（Permendag 31/2023）。"], refs: ["PERMENDAG-2020-50", "PERMENKOMINFO-2020-5"] });
    push("access", "市场准入与结构", access);

    /* 2. Entity + NIB/KBLI/OSS */
    const ent = [];
    ent.push({ title: "设立步骤", body: mode.steps, refs: input.mode === "pma" ? ["UU-2007-40", "PP-2025-28"] : ["PP-2025-28"] });
    if (input.mode === "pma") {
      ent.push({ title: "OSS 风险分级与许可产出", body: S.kbli.map(([c, n, r]) => `${c}：${K().ossRisk[r]?.need || "按 OSS 判定"}`).concat(["NIB 同时作为进口识别号（API-U 贸易型 / API-P 生产型，二选一）、海关注册号和 SPPL 环境承诺。"]), refs: ["PP-2025-28"] });
      ent.push({ title: "设立后持续义务", body: K().pma.reporting, refs: ["PERBKPM-2021-5", "PERPRES-2018-13"] });
      if (acts.includes("import") && acts.includes("manufacture")) ent.push({ title: "API-P 与 API-U 冲突", body: ["生产型企业持 API-P 只能进口自用原料/设备，不得进口成品转售；如需同时贸易成品，需另设贸易公司（API-U）或申请 API-P 的成品进口例外（限同类互补产品）。"], tag: "warn", refs: ["PERMENDAG-2025-16"] });
    }
    push("entity", "主体设立、NIB / KBLI / OSS", ent);

    /* 3. Product compliance */
    const certs = certIds.map((id) => {
      const c = K().certs[id];
      const meta = [c.weeks[1] ? `周期约 ${c.weeks[0]}–${c.weeks[1]} 周` : "", c.cost[1] ? `费用约 ${idr(c.cost[0], { short: true })}–${idr(c.cost[1], { short: true })}` : ""].filter(Boolean).join("；");
      return { title: c.zh, body: [`主管：${c.agency}。适用：${c.who}`, ...c.how, ...(meta ? [meta] : [])], refs: c.regs, v: c.v };
    });
    if (!certs.length) certs.push({ title: "未识别到强制产品认证", body: ["仍需印尼语标签与贸易部流通规定；请用 HS 编码在“进口许可查询”页复核。"], refs: ["PERMENDAG-2021-25"] });
    push("product", "产品合规：BPOM / SNI / 清真 / 其他注册", certs);

    /* 4. Import */
    const imp = [];
    if (acts.includes("import") || input.mode !== "pma") {
      imp.push({ title: "进口资质", body: [input.mode === "pma" ? "NIB 载明 API（贸易型 API-U 或生产型 API-P）；海关注册随 NIB 自动生效；建议委托报关行 PPJK。" : "以印尼进口商（持 API-U）为进口记录人；你方为境外供应商，负责 CFS、检测报告等文件。", "通过 INSW（insw.go.id）按 HS 编码核对 Lartas（限制/禁止）清单。"], refs: ["PERMENDAG-2025-16"] });
      for (const l of lartasIds) { const x = K().lartas[l]; if (x) imp.push({ title: x.zh, body: [], refs: x.ref ? [x.ref] : [], v: x.v }); }
      for (const h of hs) imp.push(h.row ? { title: `HS ${h.code} · ${h.row[1]}`, body: [h.row[3], `参考 KBLI：${h.row[4]}`], refs: [], v: "税率与管制以 INSW/BTKI 2022 当前版本为准" } : { title: `HS ${h.code}`, body: ["知识库暂无该编码规则；请到 INSW 查询 Lartas 与税率。"], refs: [] });
      imp.push({ title: "进口税费结构", body: ["关税（MFN 或 ACFTA/RCEP 协定税率，需原产地证 Form E / RCEP）+ 增值税 11%（12%×11/12）+ 预缴所得税 PPh 22（持 API 2.5%，无 API 7.5%）+ 如适用的奢侈品税 PPnBM 与消费税。", "增值税与 PPh 22 可抵扣；反倾销/保障措施税不可抵扣。", "保税区（Kawasan Berikat）或 KITE 可暂免原料进口税费；Masterlist 可免设备关税。"], refs: ["PMK-2022-26", "PMK-2024-131"] });
    } else imp.push({ title: "本方案不涉及进口环节", body: ["如后续进口设备/原料，需在 NIB 中启用 API-P 并核对 Lartas。"], refs: [] });
    push("import", "进口许可与关税", imp);

    /* 5. Tax */
    const T = K().tax;
    const tax = [
      { title: "企业所得税与增值税", body: [`企业所得税 ${pct(T.cit, 0)}；${T.citSmallReduction}`, `增值税：${T.vatNote}`, "PKP 登记：年营收 > Rp48 亿必须登记为增值税纳税人并使用 e-Faktur。"], refs: ["UU-2021-7", "PMK-2024-131"] },
      { title: "预提税与中印税收协定", body: T.wht.map((w) => `${w[0]}｜${w[1]}｜${w[2]}`), refs: ["UU-2021-7"] },
      { title: "关联交易与转让定价", body: [T.tp, "中国母公司向印尼子公司收取的管理费/特许权使用费须有真实性证明，否则不得税前扣除且补征 PPh 26。"], refs: ["PMK-2023-172"] },
      { title: "申报节奏", body: T.compliance, refs: [] },
    ];
    if (input.mode === "pma" && input.investment >= 100) tax.push({ title: "可争取的税收优惠", body: T.incentives, refs: ["PMK-2020-130"], v: "Tax Holiday 政策 2025 年后续期情况需核实" });
    if (S.excise) tax.push({ title: "烟草制品三层税负", body: [K().excise.note, "定价倒算：HJE ≥ 最低零售价；消费税 + 9.9%×HJE 增值税 + 10%×消费税烟草税。用“计算器 → HPTL 消费税”测算。"], refs: ["PMK-2024-96", "PMK-2022-63", "PMK-2023-143"] });
    push("tax", "税务", tax);

    /* 6. Labor */
    const L = K().labor;
    const lab = [];
    if (input.staff > 0) {
      const ump = L.ump2025.find((u) => u[0].startsWith(input.province)) || L.ump2025[0];
      lab.push({ title: `最低工资参考：${ump[0]} ${idr(ump[1])}/月（2025）`, body: [L.minWage, L.umpNote, `按 ${input.staff} 名员工、平均工资 1.5 倍最低工资估算，年人力成本（含雇主 BPJS、THR）约 ${idr(input.staff * ump[1] * 1.5 * 13.6, { short: true })}`], refs: ["PP-2021-36", "PP-2023-51"], v: "2026 年最低工资以省长决定为准" });
      lab.push({ title: "合同与工时", body: [L.pkwt, L.pkwtt, L.hours, L.thr], refs: ["PP-2021-35", "PERMENAKER-2016-6"] });
      lab.push({ title: "社保 BPJS（雇主负担约工资的 10–12%）", body: [`劳动保障：JKK ${K().bpjs.tk.jkk.map((j) => (j[1] * 100).toFixed(2) + "%").join("/")}（按风险等级）+ JKM 0.30% + JHT 3.7% + JP 2%（基数上限 ${idr(K().bpjs.tk.jpCap)}）`, `健康保障：雇主 4% + 员工 1%，基数上限 ${idr(K().bpjs.kes.cap)}`, K().bpjs.tk.jkp], refs: [], v: "JP 基数上限每年调整" });
      lab.push({ title: "解雇成本", body: L.severance.flat(), refs: ["PP-2021-35"] });
      lab.push({ title: "用工合规义务", body: L.obligations, refs: ["UU-2003-13", "UU-2023-6"] });
    } else lab.push({ title: "暂无本地雇员", body: ["代表处/分销模式仍需注意：分销商员工不得受你方直接指挥，否则有劳动关系与 PE 风险。"], refs: [] });
    push("labor", "用工与社保", lab);

    /* 7. KITAS */
    const tk = [];
    if (input.expats > 0) {
      tk.push({ title: `外籍人员 ${input.expats} 名：办理路径`, body: K().tka.steps.map((s) => `${s[0]}：${s[1]}（约 ${s[2][0]}–${s[2][1]} 周）`), refs: ["PP-2021-34", "PERMENAKER-2021-8", "UU-2011-6"] });
      tk.push({ title: "注意事项", body: K().tka.notes, refs: ["KEPMENAKER-2019-349", "PERMENKUMHAM-2023-22"], v: "2025 年劳工部新 TKA 条例可能替换 Permenaker 8/2021" });
      tk.push({ title: "费用", body: [`工作 KITAS 全流程每人约 ${idr(K().tka.cost.kitasWork[0], { short: true })}–${idr(K().tka.cost.kitasWork[1], { short: true })}，另 DKP-TKA USD ${K().tka.cost.dkptkaUsdPerYear}/人/年`, "外籍人员薪酬需缴 PPh 21（税务居民）并加入 BPJS（居留 ≥ 6 个月）。"], refs: [] });
    } else tk.push({ title: "无常驻外籍人员", body: ["短期考察/技术指导使用商务签证（C1/C2 或电子签）不得从事有偿工作；超过 60 天或需工作的技术人员应办理短期 RPTKA + 工作签证。"], refs: ["UU-2011-6"] });
    push("kitas", "外籍人员签证与 KITAS", tk);

    /* 8. Site & environment */
    const site = [];
    if (acts.includes("manufacture") || input.land === "buy") {
      site.push({ title: `环境文件等级：${envLevel}`, body: K().site.env.map((e) => `${e[0]}：${e[1]} — ${e[2]}`), refs: ["PP-2021-22"] });
      site.push({ title: "土地与厂房", body: K().site.land.concat(K().site.building), refs: [] });
    } else site.push({ title: "办公/仓储场地", body: ["租赁写字楼或仓库即可；注意租金预提税（PPh 4(2) 10%，由承租方代扣）与增值税。", "仓库若存放进口货物待清关需海关保税仓许可。"], refs: [] });
    push("site", "场地、土地与环境", site);

    /* Timeline */
    const start = input.startDate ? new Date(input.startDate) : new Date();
    const base = K().timeline[input.mode] || K().timeline.pma;
    const phases = [];
    let cursor = 0;
    for (const [name, lo, hi, crit] of base) {
      if (name.startsWith("NPPBKC") && !S.excise) continue;
      if (name.startsWith("外籍") && !input.expats) continue;
      if (name.startsWith("场地") && !(acts.includes("manufacture") || input.land === "buy")) continue;
      if (name.startsWith("产品认证") && !certIds.length) continue;
      const dur = input.urgency === "fast" ? lo : Math.round((lo + hi) / 2);
      const s = crit ? cursor : Math.max(2, cursor - 2);
      phases.push({ name, start: s, end: s + dur, crit, lo, hi });
      if (crit) cursor = s + dur;
    }
    const total = Math.max(...phases.map((p) => p.end));
    const timeline = { start: dateISO(start), phases, totalWeeks: total, goLive: dateISO(addWeeks(start, total)) };

    /* Risks */
    const risks = K().risks.filter((r) => { try { return r.when(input, S); } catch (e) { return false; } });

    /* Budget */
    const budget = CALC.setupBudget(input, certIds, envLevel);

    /* Checklist */
    const checklist = [];
    const add = (g, t, m) => checklist.push({ group: g, text: t, meta: m || "" });
    if (input.mode === "pma") { ["确定 KBLI 组合与投资计划（每 KBLI > Rp100 亿）", "股东决议、章程条款（董事权限、外资比例）", "股东身份/公司文件公证认证与宣誓翻译", "公司名称预留、公证处签署 Akta", "取得 SK Kemenkumham、NPWP", "OSS 注册 NIB、勾选 API 类型", "银行开户并实缴资本", "首次 LKPM 与 BO 申报"].forEach((t) => add("公司设立", t)); }
    if (input.mode === "rep") ["总公司授权书与章程认证", "BKPM/贸易部代表处许可", "首席代表 KITAS"].forEach((t) => add("代表处", t));
    if (input.mode === "distributor") K().entryModes.distributor.steps.forEach((t) => add("分销商", t));
    certIds.forEach((c) => add("产品合规", K().certs[c].zh, `${K().certs[c].weeks[0]}–${K().certs[c].weeks[1]} 周`));
    if (acts.includes("import") || input.mode !== "pma") { add("进口", "INSW 核对每个 HS 编码的 Lartas 与税率"); lartasIds.forEach((l) => K().lartas[l] && add("进口", K().lartas[l].zh)); add("进口", "原产地证（Form E / RCEP）安排"); add("进口", "委托报关行 PPJK，测试首单"); }
    ["注册 Coretax 账户与 e-Faktur（如 PKP）", "确定会计政策与转让定价文档", "月度 PPN/PPh 申报日历"].forEach((t) => add("税务", t));
    if (input.staff > 0) ["劳动合同（PKWT/PKWTT）模板本地化", "BPJS 健康与劳动保障企业登记", "公司规章（≥10 人）报批", "WLTK 劳动力报告", "工资结构与最低工资核对"].forEach((t) => add("用工", t));
    if (input.expats > 0) K().tka.steps.forEach((s) => add("外籍人员", s[0]));
    if (acts.includes("manufacture")) ["工业园区选址与 KKPR", `环境文件 ${envLevel}`, "PBG/SLF 核对", "PLN 电力报装"].forEach((t) => add("场地", t));
    if (S.excise) ["NPPBKC 申请（场地勘验）", "商标与 HJE 核定", "税票订购与 CEISA 开通", "PP 28/2024 包装警示与销售渠道合规审查"].forEach((t) => add("消费税", t));
    risks.forEach((r) => add("风险应对", r.zh));

    return { input, sector: S, mode, sections, certIds, lartasIds, hs, envLevel, timeline, risks, budget, checklist, generated: new Date().toISOString() };
  }

  return { build, sectorOf, hsMatches };
})();
