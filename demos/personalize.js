/* Kadr Studio — تخصيص الديمو باسم العميل ولونه: ?n=اسم&c=hex */
(function () {
  "use strict";
  var q = new URLSearchParams(location.search);
  var name = (q.get("n") || "").replace(/[<>{}]/g, "").trim().slice(0, 40);
  var col = (q.get("c") || "").replace(/[^0-9a-fA-F]/g, "");
  if (col.length === 3) col = col.split("").map(function (x) { return x + x; }).join("");
  col = col.length === 6 ? "#" + col : "";
  var cfg = window.KADR_DEMO || {};
  window.KADR_NAME = name || cfg.brand;
  if (!name && !col) return;
  var root = document.documentElement;
  function lum(h) { var r = parseInt(h.substr(1, 2), 16), g = parseInt(h.substr(3, 2), 16), b = parseInt(h.substr(5, 2), 16); return (0.299 * r + 0.587 * g + 0.114 * b) / 255; }
  if (col) (cfg.colorVars || []).forEach(function (v) { root.style.setProperty(v, col); });
  if (col && cfg.inkVar) root.style.setProperty(cfg.inkVar, lum(col) > 0.6 ? "#141210" : "#ffffff");
  if (col && cfg.onColor) cfg.onColor(col, lum(col));
  function run() {
    if (name) {
      var pairs = (cfg.replace || []).map(function (s) { return [s, name]; });
      var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), n;
      while ((n = w.nextNode())) { var t = n.nodeValue; pairs.forEach(function (p) { t = t.split(p[0]).join(p[1]); }); if (t !== n.nodeValue) n.nodeValue = t; }
      pairs.forEach(function (p) { document.title = document.title.split(p[0]).join(p[1]); });
      var first = name.replace(/^((عيادة|عيادات|مركز|معرض|د\.|دكتور)\s*)+/, "").charAt(0) || name.charAt(0);
      (cfg.initials || []).forEach(function (sel) { document.querySelectorAll(sel).forEach(function (e) { e.textContent = first; }); });
      if (cfg.onName) cfg.onName(name, first);
    }
    var bar = document.querySelector(cfg.bar || ".demo-bar");
    if (bar && name) { var s = document.createElement("strong"); s.textContent = "مجهّزة لـ «" + name + "»" + (bar.tagName === "DIV" && bar.classList.contains("note") ? "" : " · "); if (bar.classList.contains("note")) s.style.display = "block"; bar.insertBefore(s, bar.firstChild); }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
