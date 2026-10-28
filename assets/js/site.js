(function () {
  const K = window.KADR || {}, ar = K.lang === "ar";
  const wa = (msg) => "https://wa.me/" + K.wa + "?text=" + encodeURIComponent(msg);

  // WhatsApp buttons
  const hello = ar ? "أهلًا كادر، عايز أعرف تفاصيل أكتر عن خدماتكم." : "Hi Kadr Studio, I'd like to know more about your services.";
  document.querySelectorAll(".js-wa").forEach((a) => { a.href = wa(hello); a.target = "_blank"; a.rel = "noopener"; });

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
