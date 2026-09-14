/* Shared chrome + helpers for Indonesia Market Entry OS (requires i18n.js first) */
(function () {
  addI18N({
    "nav.home": ["首页", "Home", "Beranda"],
    "nav.entry": ["落地方案生成", "Entry Plan", "Rencana Masuk"],
    "nav.calc": ["计算器", "Calculators", "Kalkulator"],
    "nav.reg": ["法规情报库", "RegIntel", "Intelijen Regulasi"],
    "nav.tools": ["合同与模板", "Contracts & Templates", "Kontrak & Templat"],
    "nav.hs": ["进口许可查询", "Import Lookup", "Cek Impor"],
    "verify": ["待核实", "verify", "perlu verifikasi"],
    "verify.why": ["该数值/规则随时可能调整，执行前请核对最新法规或向主管部门确认", "This figure/rule changes by decree; confirm against the latest regulation or the authority before acting", "Angka/aturan ini dapat berubah; periksa peraturan terbaru atau konfirmasi ke instansi sebelum bertindak"],
    "fx.note": ["汇率默认 1 USD ≈ Rp16,500，1 CNY ≈ Rp2,300，可在计算器页修改。", "Default rates 1 USD ≈ Rp16,500, 1 CNY ≈ Rp2,300; editable on the Calculators page.", "Kurs default 1 USD ≈ Rp16.500, 1 CNY ≈ Rp2.300; dapat diubah di halaman Kalkulator."],
    "unit.wan": ["万", "0k", "rb"], "unit.yi": ["亿", "bn", "M"],
    "week": ["周", "wk", "mgg"],
  });
  const NAV = [["/imeos/", "nav.home"], ["/imeos/entry/", "nav.entry"], ["/imeos/calculators/", "nav.calc"], ["/imeos/regintel/", "nav.reg"], ["/imeos/tools/", "nav.tools"], ["/imeos/hs/", "nav.hs"]];
  const here = location.pathname.replace(/index\.html$/, "");
  const nav = NAV.map(([h, k]) => `<a href="${h}" class="${here === h ? "on" : ""}">${T(k)}</a>`).join("");
  const sw = LANGS.map((l) => `<button class="${l === LANG ? "on" : ""}" onclick="setLang('${l}')">${{ zh: "中文", en: "EN", id: "ID" }[l]}</button>`).join("");
  document.body.insertAdjacentHTML("afterbegin", `<header class="top"><div class="in">
    <a class="logo" href="/imeos/"><i></i>Indonesia Market Entry OS <span>· ketikyuk</span></a>
    <nav class="nav">${nav}</nav><div class="lang">${sw}</div></div></header>`);

  const W = window;
  W.$ = (s, r = document) => r.querySelector(s);
  W.$$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  W.esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  W.idr = (n, opts = {}) => {
    if (n == null || isNaN(n)) return "–";
    const a = Math.abs(n);
    if (opts.short) {
      if (LANG === "zh") {
        if (a >= 1e8) return "Rp" + (n / 1e8).toLocaleString("zh-CN", { maximumFractionDigits: 2 }) + "亿";
        if (a >= 1e4) return "Rp" + (n / 1e4).toLocaleString("zh-CN", { maximumFractionDigits: 0 }) + "万";
      } else if (LANG === "id") {
        if (a >= 1e9) return "Rp" + (n / 1e9).toLocaleString("id-ID", { maximumFractionDigits: 2 }) + " miliar";
        if (a >= 1e6) return "Rp" + (n / 1e6).toLocaleString("id-ID", { maximumFractionDigits: 1 }) + " juta";
      } else {
        if (a >= 1e9) return "Rp" + (n / 1e9).toLocaleString("en-US", { maximumFractionDigits: 2 }) + "bn";
        if (a >= 1e6) return "Rp" + (n / 1e6).toLocaleString("en-US", { maximumFractionDigits: 1 }) + "m";
      }
    }
    return "Rp" + Math.round(n).toLocaleString(LANG === "zh" ? "id-ID" : locale);
  };
  W.num = (n, d = 0) => (n == null || isNaN(n)) ? "–" : Number(n).toLocaleString(locale, { maximumFractionDigits: d, minimumFractionDigits: d });
  W.pct = (n, d = 2) => (n == null || isNaN(n)) ? "–" : (n * 100).toFixed(d) + "%";
  W.fx = () => { try { const s = JSON.parse(localStorage.getItem("imeos.fx") || "null"); if (s) return s; } catch (e) {} return { usd: 16500, cny: 2300 }; };
  W.toUSD = (n) => n / W.fx().usd;
  W.toCNY = (n) => n / W.fx().cny;
  W.store = {
    get(k, d) { try { const v = localStorage.getItem("imeos." + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem("imeos." + k, JSON.stringify(v)); } catch (e) {} },
  };
  W.regLink = (id) => { const r = (W.KB && W.KB.regs[id]) || {}; return `<a href="/imeos/regintel/?id=${encodeURIComponent(id)}" title="${esc(L(r.zh) || "")}">${esc(r.t || id)}</a>`; };
  W.verifyTag = (why) => `<span class="verify" title="${esc(why ? L(why) : T("verify.why"))}">${T("verify")}</span>`;
  W.dateISO = (d) => d.toISOString().slice(0, 10);
  W.addWeeks = (d, w) => new Date(d.getTime() + w * 7 * 864e5);
  W.download = (name, text, type = "text/plain") => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); };
  document.addEventListener("DOMContentLoaded", () => applyI18N());
})();
