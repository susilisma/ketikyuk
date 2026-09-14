/* Shared chrome + helpers for Indonesia Market Entry OS */
(function () {
  const NAV = [
    ["/imeos/", "首页"],
    ["/imeos/entry/", "落地方案生成"],
    ["/imeos/calculators/", "计算器"],
    ["/imeos/regintel/", "法规情报库"],
    ["/imeos/tools/", "合同与模板"],
    ["/imeos/hs/", "进口许可查询"],
  ];
  const here = location.pathname.replace(/index\.html$/, "");
  const nav = NAV.map(([h, t]) => `<a href="${h}" class="${here === h ? "on" : ""}">${t}</a>`).join("");
  document.body.insertAdjacentHTML("afterbegin", `<header class="top"><div class="in">
    <a class="logo" href="/imeos/"><i></i>Indonesia Market Entry OS <span>· ketikyuk</span></a>
    <nav class="nav">${nav}</nav></div></header>`);

  const W = window;
  W.$ = (s, r = document) => r.querySelector(s);
  W.$$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  W.esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  W.idr = (n, opts = {}) => {
    if (n == null || isNaN(n)) return "–";
    const a = Math.abs(n);
    // Chinese readers think in 万/亿; keep Indonesian thousands separators for exact figures.
    if (opts.short && a >= 1e8) return "Rp" + (n / 1e8).toLocaleString("zh-CN", { maximumFractionDigits: 2 }) + "亿";
    if (opts.short && a >= 1e4) return "Rp" + (n / 1e4).toLocaleString("zh-CN", { maximumFractionDigits: 0 }) + "万";
    return "Rp" + Math.round(n).toLocaleString("id-ID");
  };
  W.num = (n, d = 0) => (n == null || isNaN(n)) ? "–" : Number(n).toLocaleString("zh-CN", { maximumFractionDigits: d, minimumFractionDigits: d });
  W.pct = (n, d = 2) => (n == null || isNaN(n)) ? "–" : (n * 100).toFixed(d) + "%";
  W.fx = () => {
    try { const s = JSON.parse(localStorage.getItem("imeos.fx") || "null"); if (s) return s; } catch (e) {}
    return { usd: 16500, cny: 2300 };
  };
  W.toUSD = (n) => n / W.fx().usd;
  W.toCNY = (n) => n / W.fx().cny;
  W.money3 = (n) => `${idr(n, { short: true })} <small class="mute">≈ ¥${num(toCNY(n))} / $${num(toUSD(n))}</small>`;
  W.store = {
    get(k, d) { try { const v = localStorage.getItem("imeos." + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem("imeos." + k, JSON.stringify(v)); } catch (e) {} },
  };
  W.regLink = (id) => {
    const r = (W.KB && W.KB.regs[id]) || {};
    const t = r.t || id;
    return `<a href="/imeos/regintel/?id=${encodeURIComponent(id)}" title="${esc(r.zh || "")}">${esc(t)}</a>`;
  };
  W.verifyTag = (why) => `<span class="verify" title="${esc(why || "该数值/规则随时可能调整，执行前请核对最新法规或向主管部门确认")}">待核实</span>`;
  W.dateISO = (d) => d.toISOString().slice(0, 10);
  W.addWeeks = (d, w) => new Date(d.getTime() + w * 7 * 864e5);
  W.download = (name, text, type = "text/plain") => {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type }));
    a.download = name; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  };
})();
