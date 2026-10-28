(function () {
  "use strict";
  const DOCTORS = [
    { id: "sara", name: "د. سارة منصور", role: "تجميل الأسنان" },
    { id: "karim", name: "د. كريم عادل", role: "تقويم الأسنان" },
    { id: "nour", name: "د. نور الهدى", role: "جلدية وتجميل" },
  ];
  const SERVICES = [
    { id: "consult", name: "كشف واستشارة", price: 300, doc: ["sara", "karim", "nour"] },
    { id: "clean", name: "تنظيف وتلميع", price: 800, doc: ["sara"] },
    { id: "white", name: "تبييض بالليزر", price: 3000, doc: ["sara"] },
    { id: "filling", name: "حشو تجميلي", price: 1200, doc: ["sara"] },
    { id: "veneer", name: "فينير (للسن)", price: 6000, doc: ["sara"] },
    { id: "aligner", name: "متابعة تقويم شفاف", price: 1500, doc: ["karim"] },
    { id: "botox", name: "بوتوكس", price: 4500, doc: ["nour"] },
    { id: "facial", name: "هيدرافيشيال", price: 1800, doc: ["nour"] },
  ];
  const NAMES = ["منة أحمد", "يوسف خالد", "سلمى حسن", "عمر طارق", "ملك إبراهيم", "آدم سامح", "نادين وليد", "كريم ياسر", "فريدة شريف", "مالك عمرو", "هنا مصطفى", "زياد محمود", "جنى رامي", "علي حازم", "ليلى أيمن", "سيف الدين نبيل", "رنا عاطف", "حمزة فؤاد"];
  const SLOTS = []; for (let h = 12; h <= 20; h++) { SLOTS.push(pad(h) + ":00"); SLOTS.push(pad(h) + ":30"); }
  const KEY = "lumaa-demo-v2";
  const ar = (n) => Number(n).toLocaleString("ar-EG");
  const DAYS = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
  const STATUS = { pending: "في انتظار التأكيد", confirmed: "مؤكد", arrived: "وصل", done: "تمت الزيارة", cancelled: "ملغي" };

  function pad(n) { return String(n).padStart(2, "0"); }
  function iso(d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function addDays(d, n) { const x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function fromIso(s) { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); }
  function dayLabel(s) { const d = fromIso(s); return DAYS[d.getDay()] + " " + ar(d.getDate()) + "/" + ar(d.getMonth() + 1); }
  function time12(t) { const [h, m] = t.split(":").map(Number); const hh = h > 12 ? h - 12 : h; return ar(hh) + ":" + ar(pad(m)).padStart(2, "٠") + (h >= 12 ? " م" : " ص"); }
  const svc = (id) => SERVICES.find((s) => s.id === id);
  const doc = (id) => DOCTORS.find((d) => d.id === id);
  function phoneFor(i) { return "01" + ["0", "1", "2", "5"][i % 4] + String(10000000 + ((i * 7919) % 89999999)).slice(0, 8); }

  // ---------- state ----------
  let S = load() || seed();
  function load() { try { const v = JSON.parse(localStorage.getItem(KEY)); return v && v.v === 1 && v.seededFor === iso(new Date()) ? v : null; } catch (e) { return null; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  function seed() {
    let r = 42; const rnd = () => (r = (r * 16807) % 2147483647) / 2147483647;
    const today = new Date(); const hh = today.getHours(); const now = (hh >= 12 && hh < 21) ? hh * 60 + today.getMinutes() : 15 * 60 + 30; // خارج مواعيد العيادة: نفترض إن اليوم شغال والساعة ٣:٣٠
    const appts = []; let id = 1;
    for (let off = -2; off <= 4; off++) {
      const d = addDays(today, off); if (d.getDay() === 5) continue; // الجمعة إجازة
      DOCTORS.forEach((dr) => {
        const count = 2 + Math.floor(rnd() * 3);
        const used = new Set();
        for (let k = 0; k < count; k++) {
          let slot; do { slot = SLOTS[Math.floor(rnd() * SLOTS.length)]; } while (used.has(slot)); used.add(slot);
          const opts = SERVICES.filter((s) => s.doc.includes(dr.id));
          const sv = opts[Math.floor(rnd() * opts.length)];
          const pi = Math.floor(rnd() * NAMES.length);
          const [h, m] = slot.split(":").map(Number), mins = h * 60 + m;
          let st;
          if (off < 0) st = rnd() < .12 ? "cancelled" : "done";
          else if (off === 0) st = mins < now - 40 ? (rnd() < .1 ? "cancelled" : "done") : mins < now ? "arrived" : (rnd() < .75 ? "confirmed" : "pending");
          else st = off === 1 ? (rnd() < .6 ? "confirmed" : "pending") : (rnd() < .4 ? "confirmed" : "pending");
          appts.push({ id: id++, name: NAMES[pi], phone: phoneFor(pi), service: sv.id, doctor: dr.id, date: iso(d), time: slot, status: st, reminded: off <= 0 || (off === 1 && st === "confirmed") });
        }
      });
    }
    const st = { v: 1, seededFor: iso(today), appts, msgs: [] };
    return st;
  }

  // ---------- messages ----------
  const T = {
    confirm: (a) => `مرحبًا ${a.name}، تم تسجيل موعدكم في عيادة لُمعة يوم ${dayLabel(a.date)} الساعة ${time12(a.time)} مع ${doc(a.doctor).name} لخدمة «${svc(a.service).name}». للتأجيل يُرجى الرد بكلمة «تأجيل».`,
    remind: (a) => `تذكير من عيادة لُمعة: موعدكم ${dayLabel(a.date)} الساعة ${time12(a.time)} مع ${doc(a.doctor).name}. يُرجى الرد بـ «تأكيد» أو «تأجيل».`,
    review: (a) => `شكرًا لزيارتكم عيادة لُمعة اليوم يا ${a.name.split(" ")[0]}. يسعدنا تقييم تجربتكم في دقيقة واحدة من خلال الرابط: [رابط التقييم]`,
    cancel: (a) => `تم إلغاء موعدكم يوم ${dayLabel(a.date)} الساعة ${time12(a.time)}. يسعدنا تحديد موعد جديد لكم في أي وقت بالرد على هذه الرسالة.`,
  };
  const KIND = { confirm: "تأكيد حجز", remind: "تذكير قبل ٢٤ ساعة", review: "طلب تقييم", cancel: "إلغاء", reply: "رد المريض" };
  function send(kind, a, inbound) {
    const text = inbound || T[kind](a);
    const now = new Date();
    S.msgs.push({ kind, to: a.name, text, inbound: !!inbound, at: pad(now.getHours()) + ":" + pad(now.getMinutes()) });
    if (S.msgs.length > 60) S.msgs.shift();
    save(); renderChat(); renderLog();
  }

  // ---------- render ----------
  const $ = (s) => document.querySelector(s);
  const todayIso = iso(new Date());
  function badge(st) { return `<span class="badge ${st}">${STATUS[st]}</span>`; }

  function renderToday() {
    const f = $("#docFilter").value;
    const list = S.appts.filter((a) => a.date === todayIso && (!f || a.doctor === f)).sort((a, b) => a.time.localeCompare(b.time));
    $("#todayDate").textContent = dayLabel(todayIso) + " · " + (new Date().getDay() === 5 ? "الجمعة إجازة العيادة" : "من ١٢ ظهرًا لـ ٩ مساءً");
    const live = list.filter((a) => a.status !== "cancelled");
    const rev = live.reduce((s, a) => s + svc(a.service).price, 0);
    const came = list.filter((a) => a.status === "arrived" || a.status === "done").length;
    $("#kpis").innerHTML = [
      [ar(list.length), "موعد اليوم"],
      [ar(list.filter((a) => a.status === "confirmed").length), "مؤكد ومستني"],
      [ar(came), "وصلوا العيادة"],
      [ar(rev) + " ج.م", "إيراد متوقع"],
    ].map(([b, s]) => `<div class="kpi"><b>${b}</b><span>${s}</span></div>`).join("");
    $("#todayList").innerHTML = list.length ? list.map(row).join("") : `<div class="empty">مفيش مواعيد النهارده${f ? " للطبيب ده" : ""}. اضغط «حجز جديد» عشان تضيف.</div>`;
  }
  function row(a) {
    const s = svc(a.service), d = doc(a.doctor);
    const acts = [];
    if (a.status === "pending") acts.push(`<button class="btn-s" data-act="remind" data-id="${a.id}">ابعت تذكير</button>`);
    if (a.status === "pending" || a.status === "confirmed") acts.push(`<button class="btn-s" data-act="arrived" data-id="${a.id}">وصل</button>`);
    if (a.status === "arrived") acts.push(`<button class="btn-s" data-act="done" data-id="${a.id}">خلصت الزيارة</button>`);
    if (["pending", "confirmed"].includes(a.status)) acts.push(`<button class="btn-s" data-act="cancel" data-id="${a.id}">إلغاء</button>`);
    return `<article class="appt s-${a.status}"><div class="time">${time12(a.time)}</div>
      <div class="who"><b>${a.name}</b><small>${s.name} · ${d.name} · ${ar(s.price)} ج.م</small></div>
      <div class="acts">${badge(a.status)}${acts.join("")}</div></article>`;
  }

  function renderWeek() {
    const start = new Date(); let html = "";
    for (let i = -1; i < 6; i++) {
      const d = addDays(start, i), di = iso(d);
      const items = S.appts.filter((a) => a.date === di).sort((a, b) => a.time.localeCompare(b.time));
      html += `<div class="day${di === todayIso ? " today" : ""}"><h3>${DAYS[d.getDay()]}<b>${ar(d.getDate())}/${ar(d.getMonth() + 1)}</b></h3>` +
        (d.getDay() === 5 ? `<p class="badge">إجازة</p>` : items.map((a) => `<button class="chip ${a.status}" data-open="${a.id}"><b>${time12(a.time)}</b> ${a.name}<br><span>${svc(a.service).name}</span></button>`).join("")) + `</div>`;
    }
    $("#week").innerHTML = html;
  }

  function renderPatients() {
    const q = ($("#pSearch").value || "").trim();
    const map = {};
    S.appts.forEach((a) => { (map[a.phone] = map[a.phone] || { name: a.name, phone: a.phone, list: [] }).list.push(a); });
    const rows = Object.values(map).filter((p) => !q || p.name.includes(q) || p.phone.includes(q)).sort((a, b) => a.name.localeCompare(b.name, "ar"));
    $("#pBody").innerHTML = rows.map((p) => {
      const done = p.list.filter((a) => a.status === "done").sort((a, b) => (b.date + b.time).localeCompare(a.date + a.time));
      const next = p.list.filter((a) => (a.date > todayIso || (a.date === todayIso && ["pending", "confirmed"].includes(a.status))) && a.status !== "cancelled").sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time))[0];
      return `<tr><td>${p.name}</td><td class="num">${p.phone}</td><td>${ar(done.length)}</td><td>${done[0] ? svc(done[0].service).name : "—"}</td><td>${next ? dayLabel(next.date) + " · " + time12(next.time) : "—"}</td></tr>`;
    }).join("") || `<tr><td colspan="5">مفيش نتايج.</td></tr>`;
  }

  function renderChat() {
    const last = S.msgs.slice(-8);
    $("#chat").innerHTML = last.length ? last.map((m) => `<div class="msg${m.inbound ? " in" : ""}">${m.inbound ? "" : `<span class="tag">${KIND[m.kind]} · إلى ${m.to}</span><br>`}${m.text}<time>${m.at}</time></div>`).join("")
      : `<div class="msg"><span class="tag">جاهز</span><br>اعمل حجز جديد أو اضغط «ابعت تذكير» وشوف الرسالة هنا.</div>`;
    const b = $("#chat"); b.scrollTop = b.scrollHeight;
  }
  function renderLog() {
    const l = S.msgs.slice().reverse().slice(0, 12);
    $("#log").innerHTML = l.length ? l.map((m) => `<div><b>${KIND[m.kind]}</b> — ${m.inbound ? "من" : "إلى"} ${m.to}<span>${m.at}</span></div>`).join("") : `<div class="empty">لسه مفيش رسائل في الجلسة دي.</div>`;
  }

  function renderFlow() {
    const node = (x, y, w, t, s, c) => `<g><rect x="${x}" y="${y}" width="${w}" height="64" rx="10" fill="${c || "#f4f0e8"}" stroke="#d9cfbf"/><text x="${x + w - 14}" y="${y + 27}" text-anchor="end" font-size="15" font-weight="600" fill="#2f3a2c">${t}</text><text x="${x + w - 14}" y="${y + 48}" text-anchor="end" font-size="12" fill="#6f6a5e">${s}</text></g>`;
    const arrow = (x1, y1, x2, y2) => `<path d="M${x1} ${y1} L${x2} ${y2}" stroke="#b89b5e" stroke-width="2" marker-end="url(#ah)"/>`;
    const lane = (y, t) => `<text x="1010" y="${y}" text-anchor="end" font-size="13" fill="#b89b5e" font-weight="600">${t}</text>`;
    $("#flow").innerHTML = `<svg viewBox="0 0 1020 400" font-family="Readex Pro" style="direction:ltr">
      <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#b89b5e"/></marker></defs>
      ${lane(22, "عند الحجز")}
      ${node(790, 34, 210, "حجز جديد", "من الاستقبال أو الموقع", "#ebe5d9")}${arrow(788, 66, 712, 66)}
      ${node(500, 34, 210, "n8n · Webhook", "يستقبل بيانات الحجز")}${arrow(498, 66, 422, 66)}
      ${node(210, 34, 210, "رسالة تأكيد واتساب", "WhatsApp Business API", "#e2ecdf")}
      ${lane(142, "كل ساعة")}
      ${node(790, 154, 210, "مؤقّت n8n", "Cron · كل ساعة", "#ebe5d9")}${arrow(788, 186, 712, 186)}
      ${node(500, 154, 210, "مواعيد بعد ٢٤ ساعة", "فلترة من جدول الحجوزات")}${arrow(498, 186, 422, 186)}
      ${node(210, 154, 210, "تذكير واتساب", "بأزرار: تأكيد / تأجيل", "#e2ecdf")}${arrow(208, 186, 132, 186)}
      ${node(10, 154, 120, "رد المريض", "تحديث الحالة", "#f3ead7")}
      ${lane(262, "بعد الزيارة")}
      ${node(790, 274, 210, "الزيارة خلصت", "الاستقبال يغيّر الحالة", "#ebe5d9")}${arrow(788, 306, 712, 306)}
      ${node(500, 274, 210, "انتظار ساعتين", "Wait node")}${arrow(498, 306, 422, 306)}
      ${node(210, 274, 210, "طلب تقييم جوجل", "رسالة شكر + رابط", "#e2ecdf")}
      <text x="1010" y="390" text-anchor="end" font-size="12" fill="#6f6a5e">في الديمو ده الرسائل بتظهر في معاينة الموبايل بدل ما تتبعت فعلًا.</text>
    </svg>`;
  }

  function renderAll() { renderToday(); renderWeek(); renderPatients(); renderChat(); renderLog(); }

  // ---------- actions ----------
  function setStatus(id, st) {
    const a = S.appts.find((x) => x.id === id); if (!a) return;
    a.status = st; save();
    if (st === "done") setTimeout(() => send("review", a), 600);
    if (st === "cancelled") send("cancel", a);
    renderAll();
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-act]");
    if (b) {
      const id = +b.dataset.id, act = b.dataset.act, a = S.appts.find((x) => x.id === id);
      if (act === "remind") { send("remind", a); a.reminded = true; save(); setTimeout(() => { send("reply", a, "تأكيد"); setStatus(id, "confirmed"); }, 1800); }
      else setStatus(id, act === "cancel" ? "cancelled" : act);
      return;
    }
    const o = e.target.closest("[data-open]");
    if (o) openDetail(+o.dataset.open);
    const t = e.target.closest(".tab");
    if (t) {
      document.querySelectorAll(".tab").forEach((x) => x.classList.toggle("on", x === t));
      document.querySelectorAll(".view").forEach((v) => v.classList.toggle("on", v.id === "view-" + t.dataset.view));
    }
  });

  function openDetail(id) {
    const a = S.appts.find((x) => x.id === id), s = svc(a.service), d = doc(a.doctor);
    $("#detailBody").innerHTML = `<header><h2>${a.name}</h2><button class="x" type="button" onclick="this.closest('dialog').close()" aria-label="إغلاق">×</button></header>
      <dl class="dl"><dt>الموعد</dt><dd>${dayLabel(a.date)} · ${time12(a.time)}</dd><dt>الخدمة</dt><dd>${s.name} · ${ar(s.price)} ج.م</dd><dt>الطبيب</dt><dd>${d.name} (${d.role})</dd><dt>الموبايل</dt><dd dir="ltr" style="text-align:right">${a.phone}</dd><dt>الحالة</dt><dd>${badge(a.status)}</dd><dt>التذكير</dt><dd>${a.reminded ? "اتبعت" : "مجدول قبل الميعاد بـ ٢٤ ساعة"}</dd></dl>
      <div class="acts" style="display:flex;gap:6px;flex-wrap:wrap">${["pending", "confirmed"].includes(a.status) ? `<button class="btn-s" data-act="remind" data-id="${a.id}">ابعت تذكير الآن</button><button class="btn-s" data-act="cancel" data-id="${a.id}">إلغاء الموعد</button>` : ""}</div>`;
    $("#detail").showModal();
  }
  $("#detail").addEventListener("click", (e) => { if (e.target.closest("[data-act]")) setTimeout(() => $("#detail").close(), 50); });

  // booking form
  const form = $("#bookForm");
  function fillServices() { const dr = $("#fDoctor").value; $("#fService").innerHTML = SERVICES.filter((s) => s.doc.includes(dr)).map((s) => `<option value="${s.id}">${s.name} — ${ar(s.price)} ج.م</option>`).join(""); }
  function fillTimes() {
    const dt = form.date.value, dr = $("#fDoctor").value;
    const taken = new Set(S.appts.filter((a) => a.date === dt && a.doctor === dr && a.status !== "cancelled").map((a) => a.time));
    $("#fTime").innerHTML = SLOTS.map((t) => `<option value="${t}"${taken.has(t) ? " disabled" : ""}>${time12(t)}${taken.has(t) ? " (محجوز)" : ""}</option>`).join("");
    const first = SLOTS.find((t) => !taken.has(t)); if (first) $("#fTime").value = first;
  }
  $("#fDoctor").innerHTML = DOCTORS.map((d) => `<option value="${d.id}">${d.name}</option>`).join("");
  $("#docFilter").innerHTML = `<option value="">كل الأطباء</option>` + DOCTORS.map((d) => `<option value="${d.id}">${d.name}</option>`).join("");
  $("#fDoctor").addEventListener("change", () => { fillServices(); fillTimes(); });
  form.date.addEventListener("change", fillTimes);
  $("#newBtn").addEventListener("click", () => {
    form.reset(); form.date.value = iso(addDays(new Date(), 1)); form.date.min = todayIso; fillServices(); fillTimes();
    $("#clash").hidden = true; $("#dlg").showModal();
  });
  form.addEventListener("submit", (e) => {
    if (e.submitter && e.submitter.value === "cancel") return;
    const fd = new FormData(form);
    if (fromIso(fd.get("date")).getDay() === 5) { e.preventDefault(); $("#clash").textContent = "يوم الجمعة إجازة العيادة، اختار يوم تاني."; $("#clash").hidden = false; return; }
    const clash = S.appts.some((a) => a.date === fd.get("date") && a.time === fd.get("time") && a.doctor === fd.get("doctor") && a.status !== "cancelled");
    if (clash) { e.preventDefault(); $("#clash").textContent = "الميعاد ده محجوز للطبيب بالفعل، اختار ساعة تانية."; $("#clash").hidden = false; return; }
    const a = { id: Math.max(0, ...S.appts.map((x) => x.id)) + 1, name: fd.get("name").trim(), phone: fd.get("phone").trim(), service: fd.get("service"), doctor: fd.get("doctor"), date: fd.get("date"), time: fd.get("time"), status: "confirmed", reminded: false };
    S.appts.push(a); save(); send("confirm", a); renderAll();
  });

  $("#docFilter").addEventListener("change", renderToday);
  $("#pSearch").addEventListener("input", renderPatients);
  $("#resetBtn").addEventListener("click", () => { try { localStorage.removeItem(KEY); } catch (e) {} S = seed(); save(); renderAll(); });

  renderFlow(); renderAll();
})();
