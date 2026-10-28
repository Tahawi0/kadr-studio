// ===== Settings: edit these two lines =====
const WHATSAPP = "201555014697";          // international format, no + (e.g. 201012345678)
const EMAIL = "hello@kadr.studio";          // contact email
// ==========================================

const AR = {
  logo_sub: "استوديو",
  nav_services: "الخدمات", nav_work: "أعمالنا", nav_process: "طريقة العمل", nav_contact: "تواصل",
  hero_eyebrow: "استوديو إبداعي بالذكاء الاصطناعي · القاهرة",
  hero_title: "براندك…<br><em>في أحسن كادر.</em>",
  hero_lede: "نحوّل صور الموبايل لصور حملات احترافية، ونخطط وندير صفحاتك، وننتج إعلانات فيديو بتعليق صوتي عربي، ونبني صفحات هبوط بتبيع — في أيام، مش أسابيع.",
  cta_wa: "كلّمنا واتساب", cta_work: "شوف أعمالنا", cta_mail: "راسلنا بالإيميل",
  fact1_n: "٤٨ ساعة", fact1_t: "أول تسليم",
  fact2_n: "عربي · إنجليزي", fact2_t: "بلغتين من الأساس",
  fact3_n: "مصر · الخليج", fact3_t: "فاهمين السوق",
  hero_cap: "Drapé Atelier — حملة الإطلاق",
  svc_eyebrow: "بنعمل إيه", svc_title: "أربع خدمات. استوديو واحد.",
  s1_t: "صور منتجات بالذكاء الاصطناعي",
  s1_d: "ابعت صورة المنتج من موبايلك، واستلم صور استوديو ولايف ستايل وعلى موديل — والمنتج نفسه زي ما هو بالظبط.",
  s1_p: "تبدأ من ٣٠٠ ج.م · ٢٥$",
  s2_t: "إدارة السوشيال ميديا",
  s2_d: "شكل موحد للبراند، خطة محتوى شهرية، بوستات وريلز وكابشن بالعربي والإنجليزي — ونجدولها وننشرها بدالك.",
  s2_p: "تبدأ من ٢,٥٠٠ ج.م شهريًا · ٢٥٠$",
  s3_t: "إعلانات فيديو + تعليق صوتي عربي",
  s3_d: "إعلانات قصيرة سينمائية للريلز والستوري، بتعليق صوتي عربي (مصري أو خليجي أو فصحى) وكوبي بيبيع. تخصصنا: إعلانات السيارات.",
  s3_p: "تبدأ من ٥٠٠ ج.م · ٤٠$",
  s4_t: "صفحات هبوط ومواقع",
  s4_d: "صفحات سريعة ومناسبة للموبايل، بطلب مباشر على واتساب وكتالوج منتجات، والعربي من اليمين لليسار مظبوط. جاهزة في أيام.",
  s4_p: "تبدأ من ٣,٠٠٠ ج.م · ١٥٠$",
  work_eyebrow: "مختارات من شغلنا", work_title: "براندات حقيقية. إطلاقات حقيقية.",
  c1_tag: "هوية بصرية · صور بالذكاء الاصطناعي · إطلاق سوشيال",
  c1_d: "براند أزياء محتشمة اتبنى من الصفر: الاسم، ونظام اللوجو، وألوان ترابية بلمسة نبيتي، وفيد إطلاق كامل. كل لوك اتصور فلات لاي، وبعدها اتلبس على موديل بدون وش بالذكاء الاصطناعي — من غير سيشن تصوير ولا استوديو.",
  c1_l1: "الاسم ونظام اللوجو", c1_l2: "١٠ لوكات للحملة + فلات لاي", c1_l3: "بوستات الإطلاق وريلز متحركة",
  c2_tag: "إعادة براندينج · موقع · حملة",
  c2_d: "محل ملابس رياضية محلي اتعمله إطلاق جديد: هوية الأسد، وستايل حملة سينمائي داكن، وموقع كتالوج للموبايل بطلب بضغطة واحدة على واتساب للقاهرة والجيزة.",
  c2_l1: "لوجو الأسد وهوية الصفحة", c2_l2: "موقع كتالوج بطلبات واتساب", c2_l3: "تصميمات حملة الإطلاق",
  c3_tag: "إعلانات فيديو · تعليق صوتي عربي · إنتاج بالذكاء الاصطناعي",
  c3_h: "ريلز إعلانية",
  c3_d: "إعلانين طوليين لبراندات مفاهيمية من تصميمنا: «نَفحة» عطر عود خليجي، و«درب موتورز» معرض عربيات مصري. كل لقطة والتعليق الصوتي والموسيقى والترجمة العربية اتعملوا بالذكاء الاصطناعي وخلّصناهم إحنا — جاهزين للريلز والتيك توك.",
  c3_l1: "لقطات منتج بالذكاء الاصطناعي", c3_l2: "تعليق صوتي خليجي ومصري + موسيقى أصلية", c3_l3: "ترجمة عربية وكارت عرض في النهاية",
  c3_note: "شغل مفاهيمي — أسماء البراندات والعروض وهمية.",
  c3_v1: "نَفحة — عطر عود · ١٩ ثانية", c3_v2: "درب موتورز — عرض تقسيط · ٢٢ ثانية",
  proc_eyebrow: "طريقة الشغل", proc_title: "من أول رسالة لحد ما تنزل — بسرعة.",
  p1_t: "الفكرة", p1_d: "احكيلنا عن البراند على واتساب أو الإيميل. الكتابة كفاية — مش محتاجين مكالمات.",
  p2_t: "عينة مجانية", p2_d: "نعدّل صورة واحدة من منتجاتك ببلاش، عشان تشوف الجودة الأول.",
  p3_t: "التنفيذ", p3_d: "أول تسليم خلال ٤٨ ساعة، ومعاه جولتين تعديلات.",
  p4_t: "النشر", p4_d: "ملفات أو بوستات أو صفحتك شغالة — جاهزة للنشر وبمقاسات كل المنصات.",
  ct_eyebrow: "ابدأ مشروعك",
  ct_title: "ابعتلنا صورة منتج واحدة. وهنوريك ممكن تبقى إيه.",
  foot_note: "القاهرة، مصر · بنشتغل مع العالم كله"
};

const EN = {};
document.querySelectorAll("[data-i18n]").forEach(el => EN[el.dataset.i18n] = el.textContent);
document.querySelectorAll("[data-i18n-html]").forEach(el => EN[el.dataset.i18nHtml] = el.innerHTML);

function setLang(lang) {
  const dict = lang === "ar" ? AR : EN;
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  document.querySelectorAll("[data-i18n]").forEach(el => { const v = dict[el.dataset.i18n]; if (v) el.textContent = v; });
  document.querySelectorAll("[data-i18n-html]").forEach(el => { const v = dict[el.dataset.i18nHtml]; if (v) el.innerHTML = v; });
  document.getElementById("langBtn").textContent = lang === "ar" ? "English" : "العربية";
  try { localStorage.setItem("kadr-lang", lang); } catch (e) {}
  setLinks(lang);
}

function setLinks(lang) {
  const msg = lang === "ar"
    ? "أهلاً Kadr Studio، عايز أعرف تفاصيل أكتر عن خدماتكم."
    : "Hi Kadr Studio, I'd like to know more about your services.";
  document.querySelectorAll(".js-wa").forEach(a => {
    a.href = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(msg);
    a.target = "_blank"; a.rel = "noopener";
  });
  document.querySelectorAll(".js-mail").forEach(a => {
    a.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(lang === "ar" ? "مشروع جديد" : "New project");
  });
}

let saved = null;
try { saved = localStorage.getItem("kadr-lang"); } catch (e) {}
const params = new URLSearchParams(location.search);
const initial = params.get("lang") || saved || ((navigator.language || "").startsWith("ar") ? "ar" : "en");
setLang(initial);

document.getElementById("langBtn").addEventListener("click", () =>
  setLang(document.documentElement.lang === "ar" ? "en" : "ar"));
document.getElementById("yr").textContent = new Date().getFullYear();
