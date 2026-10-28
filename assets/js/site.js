(function () {
  const K = window.KADR || {}, ar = K.lang === "ar";
  const wa = (msg) => "https://wa.me/" + K.wa + "?text=" + encodeURIComponent(msg);

  // WhatsApp buttons
  const hello = ar ? "أهلًا كادر، عايز أعرف تفاصيل أكتر عن خدماتكم." : "Hi Kadr Studio, I'd like to know more about your services.";
  document.querySelectorAll(".js-wa").forEach((a) => { a.href = wa(a.dataset.msg || hello); a.target = "_blank"; a.rel = "noopener"; });

  // Count WhatsApp clicks (only if GoatCounter / Meta Pixel are switched on)
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href*="wa.me"]');
    if (!a) return;
    const where = location.pathname.split("/").pop() || "index.html";
    if (window.goatcounter && window.goatcounter.count)
      window.goatcounter.count({ path: "wa-click/" + (ar ? "ar/" : "en/") + where, title: "WhatsApp click", event: true });
    if (window.fbq) window.fbq("track", "Contact");
  });

  // Reveal on scroll (staggered within each parent)
  const els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const sibs = [...e.target.parentElement.querySelectorAll(":scope > .reveal")];
        e.target.style.transitionDelay = Math.max(0, sibs.indexOf(e.target)) * 80 + "ms";
        e.target.classList.add("in"); io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach((el) => io.observe(el));
  } else els.forEach((el) => el.classList.add("in"));

  // Package estimator
  const form = document.getElementById("est");
  if (!form) return;
  const out = document.getElementById("estTotal"), send = document.getElementById("estSend");
  const fmt = (n) => ar ? n.toLocaleString("ar-EG") + " ج.م" : "$" + n.toLocaleString("en-US");
  function update() {
    const picked = [...form.querySelectorAll("input:checked")];
    let once = 0, monthly = 0;
    picked.forEach((i) => { const v = +(ar ? i.dataset.egp : i.dataset.usd); i.dataset.monthly ? (monthly += v) : (once += v); });
    if (!picked.length) out.textContent = "—";
    else {
      const parts = [];
      if (once) parts.push(fmt(once));
      if (monthly) parts.push(fmt(monthly) + (ar ? " / شهر" : "/mo"));
      out.textContent = parts.join(" + ");
    }
    const list = picked.map((i) => "• " + i.dataset.name).join("\n");
    const msg = ar
      ? "أهلًا كادر، حابب أعرف تفاصيل الباقة دي:\n" + (list || "—") + "\nالسعر المبدئي: " + out.textContent
      : "Hi Kadr Studio, I'm interested in this package:\n" + (list || "—") + "\nStarting price: " + out.textContent;
    send.href = wa(msg); send.target = "_blank"; send.rel = "noopener";
  }
  form.addEventListener("change", update);
  update();
})();

/* ---- audit quiz + order builder ---- */
(function () {
  const K = window.KADR || {}, ar = K.lang === "ar";
  const wa = (msg) => "https://wa.me/" + K.wa + "?text=" + encodeURIComponent(msg);
  const num = (n) => ar ? n.toLocaleString("ar-EG") : n.toLocaleString("en-US");

  const audit = document.getElementById("audit");
  if (audit) audit.addEventListener("submit", (e) => {
    e.preventDefault();
    let score = 0, missing = 0; const tips = [], lines = [];
    audit.querySelectorAll(".aq").forEach((f) => {
      const c = f.querySelector("input:checked"), w = +f.dataset.w;
      if (!c) { missing++; return; }
      score += w * +c.value;
      if (+c.value < 1) tips.push(f.dataset.tip);
      lines.push("• " + f.dataset.q + " " + (c.value === "1" ? (ar ? "أيوه" : "Yes") : c.value === "0" ? (ar ? "لأ" : "No") : (ar ? "نص نص" : "Partly")));
    });
    if (missing) { alertBox(ar ? "جاوب على كل الأسئلة الأول (" + num(missing) + " فاضلين)." : "Please answer every question first (" + missing + " left)."); return; }
    score = Math.round(score);
    const lvl = score >= 80 ? (ar ? "صفحتك في حالة كويسة جدًا" : "Your page is in great shape")
              : score >= 50 ? (ar ? "أساس كويس، وفيه مكسب سهل" : "A good base, with easy wins")
              : (ar ? "فيه فرص كبيرة ضايعة" : "Big opportunities are being missed");
    const out = document.getElementById("auditOut");
    document.getElementById("auditScore").textContent = ar ? num(score) + " من " + num(100) : score + "/100";
    document.getElementById("auditLevel").textContent = lvl;
    document.getElementById("auditTips").innerHTML = (tips.length ? tips : [ar ? "استمر كده، وجرب تزوّد الريلز." : "Keep it up, and try more reels."]).map((t) => "<li>" + t + "</li>").join("");
    const msg = (ar ? "أهلًا كادر، عملت تقييم الصفحة وطلعت " + num(score) + "/" + num(100) + ". حابب أعرف رأيكم.\n" : "Hi Kadr Studio, I scored " + score + "/100 on the page check. I'd like your view.\n") + lines.join("\n");
    const send = document.getElementById("auditSend"); send.href = wa(msg); send.target = "_blank"; send.rel = "noopener";
    out.hidden = false; out.scrollIntoView({ behavior: "smooth", block: "start" });
    if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: "audit-score/" + (score >= 80 ? "high" : score >= 50 ? "mid" : "low"), title: "Audit", event: true });
  });
  function alertBox(t) { let b = document.getElementById("auditMsg"); if (!b) { b = document.createElement("p"); b.id = "auditMsg"; b.className = "note"; b.style.color = "#d9481f"; audit.appendChild(b); } b.textContent = t; }

  const order = document.getElementById("order");
  if (!order) return;
  const out = document.getElementById("orderTotal"), per = document.getElementById("orderPer"), sum = document.getElementById("orderSum"), send = document.getElementById("orderSend");
  const modelCard = order.querySelector('[data-style="model"]'), note = document.getElementById("modelNote");
  function update() {
    const type = order.querySelector('input[name="type"]:checked');
    const canModel = ["clothes", "acc"].includes(type.dataset.k);
    modelCard.classList.toggle("off", !canModel); note.hidden = canModel;
    if (!canModel) modelCard.querySelector("input").checked = false;
    const styles = [...order.querySelectorAll('input[name="style"]:checked')].map((i) => i.value);
    const q = order.querySelector('input[name="qty"]:checked');
    const uses = [...order.querySelectorAll('input[name="use"]:checked')].map((i) => i.value);
    const notes = order.notes.value.trim();
    const price = +(ar ? q.dataset.egp : q.dataset.usd), n = +q.value;
    out.textContent = ar ? num(price) + " ج.م" : "$" + num(price);
    per.textContent = ar ? num(Math.round(price / n)) + " ج.م للصورة" : "$" + Math.round(price / n) + " per photo";
    const L = ar ? ["المنتج", "الستايل", "العدد", "المقاسات"] : ["Product", "Style", "Photos", "Sizes"];
    const rows = [[L[0], type.value], [L[1], styles.join("، ") || "—"], [L[2], num(n)], [L[3], uses.join("، ") || "—"]];
    sum.innerHTML = rows.map(([a, b]) => "<li>" + a + ": " + b + "</li>").join("");
    const msg = (ar ? "أهلًا كادر، حابب أطلب صور منتجات:\n" : "Hi Kadr Studio, I'd like to order product photos:\n") +
      rows.map(([a, b]) => "• " + a + ": " + b).join("\n") + "\n" + (ar ? "• السعر: " : "• Price: ") + out.textContent +
      (notes ? "\n" + (ar ? "• ملاحظات: " : "• Notes: ") + notes : "");
    send.href = wa(msg); send.target = "_blank"; send.rel = "noopener";
  }
  order.addEventListener("input", update); order.addEventListener("change", update); update();
})();
