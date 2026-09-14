/* Calculators: payroll (PPh 21 + BPJS), HPTL excise, setup cost aggregation */
window.CALC = (() => {
  const K = () => window.KB;

  function pph21Annual(taxable) {
    let tax = 0, prev = 0;
    for (const [cap, rate] of K().pph21.brackets) {
      if (taxable <= prev) break;
      tax += (Math.min(taxable, cap) - prev) * rate;
      prev = cap;
    }
    return tax;
  }

  /** gross: monthly base wage + fixed allowances. Returns full breakdown (monthly). */
  function payroll({ gross, married = false, dependents = 0, jkkClass = 0, thrMonths = 1, hasNpwp = true, resident = true }) {
    const b = K().bpjs;
    const jkk = b.tk.jkk[jkkClass][1];
    const jpBase = Math.min(gross, b.tk.jpCap), kesBase = Math.min(gross, b.kes.cap);
    const emp = {
      jkk: gross * jkk, jkm: gross * b.tk.jkm, jht: gross * b.tk.jhtEmp, jp: jpBase * b.tk.jpEmp, kes: kesBase * b.kes.emp,
    };
    const ee = { jht: gross * b.tk.jhtEe, jp: jpBase * b.tk.jpEe, kes: kesBase * b.kes.ee };
    emp.total = Object.values(emp).reduce((a, c) => a + c, 0);
    ee.total = ee.jht + ee.jp + ee.kes;
    // Taxable income: gross + employer-paid JKK/JKM/BPJS-Kes premiums are taxable benefits; JHT/JP employer parts are not.
    const thr = gross * thrMonths;
    const annualGross = gross * 12 + thr + (emp.jkk + emp.jkm + emp.kes) * 12;
    const jobCost = Math.min(annualGross * K().pph21.jobCost.rate, K().pph21.jobCost.max);
    const pension = (ee.jht + ee.jp) * 12;
    const net = annualGross - jobCost - pension;
    const p = K().pph21.ptkp;
    const ptkp = p.base + (married ? p.married : 0) + Math.min(dependents, p.maxDep) * p.dependent;
    const pkp = Math.max(0, Math.floor((net - ptkp) / 1000) * 1000);
    let annualTax = resident ? pph21Annual(pkp) : annualGross * 0.20;
    if (resident && !hasNpwp) annualTax *= 1.2;
    const monthlyTax = annualTax / 12;
    const takeHome = gross - ee.total - monthlyTax;
    const employerCost = gross + emp.total + thr / 12;
    return { gross, emp, ee, thr, annualGross, jobCost, pension, ptkp, pkp, annualTax, monthlyTax, takeHome, employerCost };
  }

  /** HPTL excise per unit and per batch */
  function excise({ type, year = 2026, volume, hje, units = 1 }) {
    const y = K().excise.years[year], t = y[type];
    const [rate, minHje] = t;
    const perUnitVolume = volume; // ml or g per retail unit; for cartridge products, minHje is per cartridge
    const hjeUsed = Math.max(hje || 0, type === "tertutup" ? minHje : minHje * perUnitVolume);
    const cukai = rate * perUnitVolume;
    const ppn = K().excise.ppnRate * hjeUsed;
    const pajakRokok = K().excise.pajakRokok * cukai;
    const totalTax = cukai + ppn + pajakRokok;
    return { rate, minHje, hjeUsed, cukai, ppn, pajakRokok, totalTax, share: totalTax / hjeUsed, batch: { cukai: cukai * units, ppn: ppn * units, pajakRokok: pajakRokok * units, total: totalTax * units }, src: y.src, note: y.note };
  }

  /** import landed cost */
  function landed({ cif, dutyRate, addRate = 0, vat = 0.11, pph22 = 0.025, luxury = 0 }) {
    const duty = cif * dutyRate, add = cif * addRate;
    const base = cif + duty + add;
    const ppn = base * vat, ppnbm = base * luxury, pph = base * pph22;
    return { duty, add, ppn, ppnbm, pph, total: base + ppn + ppnbm + pph, cashOut: duty + add + ppn + ppnbm + pph, creditable: ppn + pph };
  }

  function setupBudget(input, certIds = [], envLevel = "SPPL") {
    const fx = window.fx();
    const on = {
      pma: input.mode === "pma", rep: input.mode === "rep", staff: input.staff > 0, office: input.mode !== "distributor" && input.mode !== "ecom",
      factory: input.activities.includes("manufacture"), warehouse: input.activities.includes("import") && !input.activities.includes("manufacture") && input.mode === "pma",
      audit: input.mode === "pma" && input.investment >= 50, expat: input.expats > 0, excise: input.sector === "hptl", certs: certIds.length > 0,
      uklupl: envLevel === "UKL-UPL", amdal: envLevel === "AMDAL", always: true,
    };
    const rows = [];
    for (const c of K().costs) {
      if (!on[c.cond]) continue;
      let lo = c.lo, hi = c.hi, mult = 1;
      if (c.usd) { lo *= fx.usd; hi *= fx.usd; }
      if (c.phase === "perExpat") mult = input.expats;
      if (c.id === "cert") { lo = certIds.reduce((a, id) => a + (K().certs[id]?.cost[0] || 0), 0); hi = certIds.reduce((a, id) => a + (K().certs[id]?.cost[1] || 0), 0); }
      rows.push({ ...c, lo: lo * mult, hi: hi * mult, mult });
    }
    const sum = (ph) => rows.filter((r) => ph.includes(r.phase)).reduce((a, r) => ({ lo: a.lo + r.lo, hi: a.hi + r.hi }), { lo: 0, hi: 0 });
    return { rows, oneOff: sum(["setup", "perExpat"]), annual: sum(["annual"]) };
  }

  return { payroll, pph21Annual, excise, landed, setupBudget };
})();
