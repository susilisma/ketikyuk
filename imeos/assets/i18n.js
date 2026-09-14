/* Trilingual core. Every human-readable string in the OS is a triple [zh, en, id];
   L(triple) picks the active language. Load before common.js. */
(function () {
  const LANGS = ["zh", "en", "id"];
  const q = new URL(location.href).searchParams.get("lang");
  let lang = q && LANGS.includes(q) ? q : null;
  if (!lang) { try { lang = localStorage.getItem("imeos.lang"); } catch (e) {} }
  if (!LANGS.includes(lang)) lang = (navigator.language || "zh").startsWith("id") ? "id" : (navigator.language || "zh").startsWith("en") ? "en" : "zh";
  try { localStorage.setItem("imeos.lang", lang); } catch (e) {}
  const IDX = LANGS.indexOf(lang);
  document.documentElement.lang = { zh: "zh-CN", en: "en", id: "id" }[lang];

  window.LANG = lang;
  window.LANGS = LANGS;
  window.L = (v) => {
    if (v == null) return "";
    if (Array.isArray(v)) return v[IDX] ?? v[0] ?? "";
    if (typeof v === "object" && ("zh" in v || "en" in v || "id" in v)) return v[lang] ?? v.zh ?? v.en ?? v.id ?? "";
    return v;
  };
  /* T(key, vars) reads window.I18N (merged page dictionaries); {name} placeholders. */
  window.I18N = window.I18N || {};
  window.T = (key, vars) => {
    let s = window.I18N[key];
    s = s == null ? key : window.L(s);
    if (vars) for (const k in vars) s = s.split("{" + k + "}").join(vars[k]);
    return s;
  };
  window.addI18N = (dict) => Object.assign(window.I18N, dict);
  /* Apply data-t / data-t-ph / data-t-title attributes on the page. */
  window.applyI18N = (root = document) => {
    root.querySelectorAll("[data-t]").forEach((el) => { el.innerHTML = window.T(el.dataset.t); });
    root.querySelectorAll("[data-t-ph]").forEach((el) => { el.placeholder = window.T(el.dataset.tPh); });
    root.querySelectorAll("[data-t-title]").forEach((el) => { el.title = window.T(el.dataset.tTitle); });
    const t = root.querySelector && root.querySelector("title[data-t]");
    if (t) document.title = window.T(t.dataset.t);
  };
  window.setLang = (l) => { try { localStorage.setItem("imeos.lang", l); } catch (e) {} const u = new URL(location.href); u.searchParams.delete("lang"); location.href = u.toString(); };
  window.locale = { zh: "zh-CN", en: "en-US", id: "id-ID" }[lang];
})();
