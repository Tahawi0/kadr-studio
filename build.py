#!/usr/bin/env python3
"""Static generator for Kadr Studio v2: Arabic at /, English at /en/."""
import os, json

WA = "201555014697"
EMAIL = "kadr.studio6@gmail.com"
SITE = "https://tahawi0.github.io/kadr-studio"
# Fill these in when the accounts exist (leave "" to switch off)
GOATCOUNTER = ""      # e.g. "kadrstudio"  -> https://kadrstudio.goatcounter.com
META_PIXEL = ""       # e.g. "123456789012345" from Meta Events Manager
GSC_TOKEN = ""        # Google Search Console HTML-tag verification content
SAMPLE_MSG = {"ar": "أهلًا كادر، عايز أجرب الصورة المجانية.", "en": "Hi Kadr Studio, I'd like to try the free photo."}
PACKAGES = [  # product photography bundles (EGP, USD)
  dict(n=5,  egp=1250, usd=60),
  dict(n=10, egp=2250, usd=110, pick=True),
  dict(n=20, egp=4000, usd=200),
]

# ---------- services (shared by pages + estimator) ----------
SERVICES = {
  "creative": [
    dict(id="identity", ar="هوية بصرية كاملة", en="Brand identity",
         dar="لوجو بنسختين، ألوان وخطوط، ودليل استخدام، وتطبيقات على المطبوعات والسوشيال.",
         den="Bilingual logo, colours and type, a usage guide, and the identity applied to print and social.",
         egp=2500, usd=120),
    dict(id="graphics", ar="تصميم جرافيك وسوشيال", en="Graphic & social design",
         dar="باقة ١٠ تصميمات: بوستات وستوري وكاروسيل وبنرات بهوية البراند.",
         den="A set of 10 designs: posts, stories, carousels and banners in your brand's look.",
         egp=1200, usd=60),
    dict(id="photos", ar="صور منتجات بالذكاء الاصطناعي", en="AI product photography",
         dar="من صورة موبايل لصور استوديو ولايف ستايل وعلى موديل، والمنتج زي ما هو بالظبط.",
         den="From a phone photo to studio, lifestyle and on-model shots, with the product kept exactly as it is.",
         egp=300, usd=25),
    dict(id="video", ar="فيديو إعلاني بتعليق صوتي عربي", en="Video ads with Arabic voiceover",
         dar="ريلز سينمائية بتعليق مصري أو خليجي أو فصحى، وموسيقى وترجمة مكتوبة.",
         den="Cinematic reels with Egyptian, Gulf or formal Arabic voiceover, music and captions.",
         egp=500, usd=40),
  ],
  "growth": [
    dict(id="ads", ar="إدارة إعلانات ممولة", en="Paid ads management",
         dar="ميتا وتيك توك وجوجل: استراتيجية، وتصميمات، واختبار A/B، وتقرير أسبوعي. الميزانية الإعلانية منفصلة.",
         den="Meta, TikTok and Google: strategy, creatives, A/B testing and a weekly report. Ad spend is separate.",
         egp=3000, usd=150, monthly=True),
    dict(id="social", ar="إدارة السوشيال ميديا", en="Social media management",
         dar="خطة محتوى شهرية، وبوستات وريلز وكابشن بالعربي والإنجليزي، والنشر بدالك.",
         den="A monthly content plan, posts, reels and captions in Arabic and English, published for you.",
         egp=2500, usd=250, monthly=True),
  ],
  "tech": [
    dict(id="web", ar="صفحات هبوط ومواقع", en="Landing pages & websites",
         dar="سريعة على الموبايل، عربي من اليمين لليسار مظبوط، وطلب مباشر على واتساب.",
         den="Fast on mobile, proper right-to-left Arabic, and one-tap WhatsApp ordering.",
         egp=3000, usd=150),
    dict(id="systems", ar="أنظمة وأتمتة", en="Systems & automation",
         dar="متابعة عملاء وحجوزات وطلبات، وتذكير واتساب تلقائي، ولوحات أرقام — بـ n8n وشيتات وأدوات جاهزة.",
         den="Lead, booking and order tracking, automatic WhatsApp reminders and dashboards, built with n8n, sheets and ready tools.",
         egp=4000, usd=200),
    dict(id="android", ar="تطبيقات أندرويد", en="Android apps",
         dar="تطبيقات Flutter وKotlin بواجهات عربية: حجز، وكتالوج، ومخزون، وحضور وانصراف.",
         den="Flutter and Kotlin apps with Arabic-first interfaces: booking, catalogues, inventory and attendance.",
         egp=15000, usd=600),
  ],
}

PILLARS = [
  dict(key="creative", ar="كادر كرييتيف", en="Kadr Creative",
       lar="هويات وتصميم وصور وفيديو بشكل براند عالمي.", len="Identity, design, photography and video at global-brand level."),
  dict(key="growth", ar="كادر جروث", en="Kadr Growth",
       lar="إعلانات ممولة وسوشيال بتجيب رسايل وطلبات.", len="Paid ads and social that bring in messages and orders."),
  dict(key="tech", ar="كادر تِك", en="Kadr Tech",
       lar="مواقع وأنظمة وتطبيقات بتشغّل البيزنس.", len="Websites, systems and apps that run the business."),
]

def T(lang, ar, en): return ar if lang == "ar" else en

def price(lang, s):
    if lang == "ar":
        n = f"{s['egp']:,}".translate(str.maketrans("0123456789,", "٠١٢٣٤٥٦٧٨٩٬"))
        return f"تبدأ من {n} ج.م" + (" / شهر" if s.get("monthly") else "")
    return f"From ${s['usd']:,}" + ("/mo" if s.get("monthly") else "")

# ---------- layout ----------
def ar_num(n): return f"{n:,}".translate(str.maketrans("0123456789,", "٠١٢٣٤٥٦٧٨٩٬"))

def analytics():
    out = ""
    if GOATCOUNTER:
        out += f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'
    if META_PIXEL:
        out += ("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
                "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];"
                "s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
                f"fbq('init','{META_PIXEL}');fbq('track','PageView');</script>\n")
    return out

def head(lang, title, desc, page, extra="", image="nafha-hero.webp"):
    pre = "" if lang == "ar" else "../"
    alt = ("en/" if lang == "ar" else "../") + page
    slug = "" if page == "index.html" else page
    url_ar, url_en = f"{SITE}/{slug}", f"{SITE}/en/{slug}"
    canon = url_ar if lang == "ar" else url_en
    gsc = f'<meta name="google-site-verification" content="{GSC_TOKEN}">\n' if GSC_TOKEN else ""
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="ar" href="{url_ar}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="x-default" href="{url_ar}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kadr Studio — كادر">
<meta property="og:locale" content="{'ar_EG' if lang=='ar' else 'en_US'}">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/img/{image}">
<meta name="theme-color" content="#151412">
{gsc}<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500;600&family=Readex+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/site.css">
{analytics()}{extra}</head>
<body>
"""

def nav(lang, page):
    pre = "" if lang == "ar" else "../"
    other = ("en/" if lang == "ar" else "../") + page
    items = [("index.html", T(lang, "الرئيسية", "Home")), ("creative.html", T(lang, "كرييتيف", "Creative")),
             ("growth.html", T(lang, "جروث", "Growth")), ("tech.html", T(lang, "تِك", "Tech")),
             ("free-sample.html", T(lang, "صورة مجانية", "Free photo"))]
    links = "".join(f'<a href="{h}"{" class=\"hl\"" if h=="free-sample.html" else ""}{" aria-current=\"page\"" if h==page else ""}>{l}</a>' for h, l in items)
    return f"""<header class="nav">
  <a href="index.html" class="logo" aria-label="Kadr Studio"><span class="mark"><i></i><i></i><i></i><i></i>K</span><span class="word">KADR<small>{T(lang,'استوديو','studio')}</small></span></a>
  <nav class="links">{links}</nav>
  <a class="lang" href="{other}" hreflang="{'en' if lang=='ar' else 'ar'}">{T(lang,'English','العربية')}</a>
  <a class="btn small solid js-wa" href="#contact">{T(lang,'واتساب','WhatsApp')}</a>
</header>
<main>
"""

def foot(lang):
    pre = "" if lang == "ar" else "../"
    return f"""</main>
<section class="contact" id="contact">
  <div class="wrap">
    <h2 class="reveal">{T(lang,'ابعتلنا فكرتك.<br>نرد عليك النهارده.','Send us your idea.<br>We reply today.')}</h2>
    <p class="reveal">{T(lang,'اكتب لنا على واتساب أو الإيميل. الكتابة كفاية، مش محتاجين مكالمات.','Message us on WhatsApp or email. Text is enough; no calls needed.')}</p>
    <div class="cta-row reveal">
      <a class="btn solid light js-wa" href="#">{T(lang,'كلّمنا واتساب','Talk on WhatsApp')}</a>
      <a class="btn line light" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</section>
<footer class="foot">
  <div class="wrap">
    <p class="big-word">KADR<span>كادر</span></p>
    <div class="foot-row">
      <span>© 2026 Kadr Studio</span>
      <span>{T(lang,'القاهرة، مصر · بنشتغل مع مصر والخليج والعالم','Cairo, Egypt · Working with Egypt, the Gulf and beyond')}</span>
    </div>
  </div>
</footer>
<a class="wa-float js-wa" href="#contact" aria-label="{T(lang,'كلّمنا على واتساب','Chat on WhatsApp')}"><svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.3 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.1-.3-.2-.6-.3z"/></svg><span>{T(lang,'واتساب','WhatsApp')}</span></a>
<script>window.KADR={{wa:"{WA}",lang:"{lang}"}};</script>
<script src="{pre}assets/js/site.js"></script>
</body>
</html>
"""

def frame(src, alt, cls="", lang="ar"):
    pre = "" if lang == "ar" else "../"
    return f'<figure class="frame {cls}"><span class="c tl"></span><span class="c tr"></span><span class="c bl"></span><span class="c br"></span><img src="{pre}assets/img/{src}" alt="{alt}" loading="lazy"></figure>'

def svc_rows(lang, key):
    rows = ""
    for s in SERVICES[key]:
        rows += f"""<li class="svc reveal"><div><h3>{T(lang,s['ar'],s['en'])}</h3><p>{T(lang,s['dar'],s['den'])}</p></div><b>{price(lang,s)}</b></li>"""
    return f'<ul class="svc-list">{rows}</ul>'

# ---------- pages ----------
def home(lang):
    p = "" if lang == "ar" else "../"
    sheet = [("lumaa-reception.webp", "Lumaa"), ("darb-hero.webp", "Darb Motors"), ("drape-look02.webp", "Drapé Atelier"),
             ("noby-fire1.webp", "NOBY Sports"), ("taqa-site-m.webp", "Taqa"), ("dune-set.webp", "Dune & Dew")]
    sheet_html = "".join(frame(s, a, f"s{i}", lang) for i, (s, a) in enumerate(sheet))
    pill_imgs = {"creative": ["lumaa-reception.webp", "nafha-post1.webp", "drape-look04.webp"],
                 "growth": ["noby-fire2.webp", "darb-poster.webp", "nafha-poster.webp"],
                 "tech": ["lumaa-sys-d.webp", "taqa-cart.webp", "darb-site-m.webp"]}
    pillars = ""
    for i, pl in enumerate(PILLARS):
        imgs = "".join(f'<img src="{p}assets/img/{x}" alt="" loading="lazy">' for x in pill_imgs[pl["key"]])
        names = "".join(f"<li>{T(lang,s['ar'],s['en'])}</li>" for s in SERVICES[pl["key"]])
        pillars += f"""<article class="pillar p-{pl['key']}">
  <div class="wrap pillar-in">
    <div class="pillar-text reveal">
      <h2>{T(lang,pl['ar'],pl['en'])}</h2>
      <p class="lede">{T(lang,pl['lar'],pl['len'])}</p>
      <ul class="names">{names}</ul>
      <a class="btn line" href="{pl['key']}.html">{T(lang,'ادخل القسم','Explore')} <span class="arr">{T(lang,'←','→')}</span></a>
    </div>
    <div class="pillar-imgs reveal">{imgs}</div>
  </div>
</article>"""
    est = ""
    for key in ("creative", "growth", "tech"):
        for s in SERVICES[key]:
            est += f"""<label class="opt"><input type="checkbox" value="{s['id']}" data-egp="{s['egp']}" data-usd="{s['usd']}" data-name="{T(lang,s['ar'],s['en'])}"{' data-monthly="1"' if s.get('monthly') else ''}><span>{T(lang,s['ar'],s['en'])}</span><em>{price(lang,s)}</em></label>"""
    steps = [(T(lang,"الفكرة","Brief"), T(lang,"احكيلنا عن البراند والهدف في رسالة.","Tell us about the brand and the goal in a message.")),
             (T(lang,"عينة مجانية","Free sample"), T(lang,"نعدّل صورة واحدة أو نرسم شاشة واحدة ببلاش.","We redo one photo or design one screen for free.")),
             (T(lang,"التنفيذ","Production"), T(lang,"أول تسليم خلال ٤٨ ساعة، وجولتين تعديلات.","First delivery in 48 hours, with two revision rounds.")),
             (T(lang,"الإطلاق","Launch"), T(lang,"ملفات جاهزة، أو صفحة شغالة، أو حملة منطلقة.","Ready files, a live page or a running campaign."))]
    steps_html = "".join(f'<li class="reveal"><b>{a}</b><span>{b}</span></li>' for a, b in steps)
    return head(lang, T(lang,"كادر استوديو — تصوير منتجات وتصميم وإعلانات ممولة في القاهرة","Kadr Studio — product photography, design and paid ads, Cairo"),
                T(lang,"استوديو إبداعي في القاهرة: تصوير منتجات بالذكاء الاصطناعي، وهويات وتصميم، وفيديو إعلاني، وإعلانات ممولة، ومواقع وأنظمة.","Cairo studio for AI product photography, identity and design, video ads, paid ads, and websites, systems and Android apps."), "index.html", extra=biz_jsonld(lang) + faq_jsonld(lang)) + nav(lang, "index.html") + f"""
<section class="hero wrap">
  <div class="hero-text">
    <h1 class="reveal">{T(lang,'استوديو واحد.<br>من الفكرة للنظام.','One studio.<br>Idea to system.')}</h1>
    <p class="lede reveal">{T(lang,'نصمم البراند، ونطلق إعلاناته، ونبني الموقع والنظام والتطبيق اللي بيشغّله، كله من مكان واحد.','We design the brand, launch its ads, and build the website, system and app that run it, all under one roof.')}</p>
    <div class="cta-row reveal"><a class="btn solid js-wa" href="#contact">{T(lang,'ابدأ مشروعك','Start a project')}</a><a class="btn line" href="#pillars">{T(lang,'شوف الأقسام','See what we do')}</a></div>
  </div>
  <div class="sheet">{sheet_html}</div>
</section>
<section class="offer-band"><div class="wrap offer-in">
  <p class="reveal"><b>{T(lang,'جرّبنا ببلاش:','Try us free:')}</b> {T(lang,'ابعت صورة منتج واحدة من الموبايل، وخدها صورة احترافية خلال ٤٨ ساعة.','send one phone photo of a product and get a professional shot within 48 hours.')}</p>
  <a class="btn solid light reveal" href="free-sample.html">{T(lang,'تفاصيل العرض','See the offer')} <span class="arr">{T(lang,'←','→')}</span></a>
</div></section>
<section id="pillars" class="pillars">{pillars}</section>
<section class="estimator wrap" id="estimate">
  <div class="est-head reveal"><h2>{T(lang,'احسب باقتك','Build your package')}</h2><p class="lede">{T(lang,'اختار اللي محتاجه، وشوف السعر المبدئي، وابعته لنا على واتساب في ضغطة.','Pick what you need, see a starting price, and send it to us on WhatsApp in one tap.')}</p></div>
  <form class="est-form reveal" id="est">{est}</form>
  <div class="est-out reveal"><p>{T(lang,'السعر المبدئي','Starting price')}</p><output id="estTotal">—</output><small id="estNote">{T(lang,'السعر النهائي بيتحدد بعد ما نفهم المشروع.','Final price is set after we understand the project.')}</small><a class="btn solid light" id="estSend" href="#">{T(lang,'ابعت الباقة على واتساب','Send on WhatsApp')}</a></div>
</section>
<section class="process wrap">
  <h2 class="reveal">{T(lang,'من أول رسالة للإطلاق','From first message to launch')}</h2>
  <ol class="steps">{steps_html}</ol>
</section>
""" + faq(lang) + foot(lang)

def page_head(lang, key, title_ar, title_en, lede_ar, lede_en, img, page):
    pl = next(p for p in PILLARS if p["key"] == key)
    return head(lang, T(lang, f"{pl['ar']} — Kadr Studio", f"{pl['en']} — Kadr Studio"), T(lang, lede_ar, lede_en), page) + nav(lang, page) + f"""
<section class="page-hero p-{key}">
  <div class="wrap page-hero-in">
    <div><p class="kicker">{T(lang,pl['ar'],pl['en'])}</p><h1 class="reveal">{T(lang,title_ar,title_en)}</h1><p class="lede reveal">{T(lang,lede_ar,lede_en)}</p></div>
    {frame(img, '', 'hero-img', lang)}
  </div>
</section>
<section class="wrap block"><h2 class="reveal">{T(lang,'الخدمات والأسعار','Services & pricing')}</h2>{svc_rows(lang,key)}</section>
"""

def case(lang, title, tag_ar, tag_en, d_ar, d_en, media, dark=False, note=None, link=None):
    nt = f'<p class="note">{T(lang,*note)}</p>' if note else ""
    ln = f'<a class="btn line{" light" if dark else ""}" href="{link[0]}" target="_blank" rel="noopener">{T(lang,link[1],link[2])} <span class="arr">↗</span></a>' if link else ""
    return f"""<article class="case{' dark' if dark else ''}"><div class="wrap case-in">
  <div class="case-text reveal"><p class="tag">{T(lang,tag_ar,tag_en)}</p><h3>{title}</h3><p>{T(lang,d_ar,d_en)}</p>{nt}{ln}</div>
  <div class="case-media reveal">{media}</div></div></article>"""

def imgs(lang, files, cls):
    p = "" if lang == "ar" else "../"
    return f'<div class="grid {cls}">' + "".join(f'<img src="{p}assets/img/{f}" alt="" loading="lazy">' for f in files) + "</div>"

def creative(lang):
    p = "" if lang == "ar" else "../"
    spec = ("مشروع مفاهيمي — الاسم والمنتج من تصميمنا.", "Concept project — name and product designed by us.")
    reels = f"""<div class="grid g-reels"><video src="{p}assets/video/nafha-reel.mp4" poster="{p}assets/img/nafha-poster.webp" controls muted loop playsinline preload="none"></video><video src="{p}assets/video/darb-reel.mp4" poster="{p}assets/img/darb-poster.webp" controls muted loop playsinline preload="none"></video><video src="{p}assets/video/sedan-reel.mp4" poster="{p}assets/img/sedan-poster.webp" controls muted loop playsinline preload="none"></video></div>"""
    return page_head(lang, "creative", "براندك بشكل<br>براند عالمي.", "Your brand,<br>world-class.",
        "هويات بصرية، وتصميم جرافيك وسوشيال، وصور منتجات، وفيديو إعلاني بتعليق صوتي عربي.",
        "Brand identity, graphic and social design, product photography, and video ads with Arabic voiceover.",
        "nafha-hero.webp", "creative.html") + packages(lang, dark=True) + '<section class="cases">' + \
      case(lang, T(lang,"لُمعة Lumaa","Lumaa"), "هوية بصرية كاملة · عيادة أسنان وتجميل", "Full identity · Dental & aesthetics clinic",
           "هوية لعيادة أسنان وتجميل في التجمع الخامس: قوس ذهبي يمثل باب العيادة وإطار الابتسامة، وألوان الزيتون والعاج والذهب، ومطبوعات، ولافتات، ويونيفورم، و٦ بوستات إطلاق.",
           "Identity for a dental and aesthetics clinic in New Cairo: a gold arch for the clinic door and the smile's frame, an olive, ivory and gold palette, stationery, signage, uniform and 6 launch posts.",
           imgs(lang, ["lumaa-reception.webp","lumaa-guide.webp","lumaa-dentist.webp","lumaa-exterior.webp","lumaa-post-launch.webp","lumaa-stationery.webp","lumaa-post-smile.webp","lumaa-post-room.webp","lumaa-post-offer.webp"], "g-lumaa"), note=spec) + \
      case(lang, "Drapé Atelier", "هوية بصرية · صور بالذكاء الاصطناعي · إطلاق", "Identity · AI photography · Launch",
           "براند أزياء محتشمة من الصفر: الاسم، ونظام اللوجو، وألوان ترابية بلمسة نبيتي، و١٠ لوكات حملة من صور فلات لاي، من غير سيشن تصوير.",
           "A modest-fashion label from zero: name, logo system, earthy palette with a wine accent, and 10 campaign looks made from flat lays, with no photoshoot.",
           imgs(lang, ["drape-look01.webp","drape-flatlay.webp","drape-look04.webp","drape-logos.webp","drape-post08.webp","drape-detail.webp"], "g-3")) + \
      case(lang, "NOBY Sports", "إعادة براندينج · حملة إطلاق", "Rebrand · Launch campaign",
           "محل ملابس رياضية اتعمله هوية الأسد وستايل حملة سينمائي داكن، وتصميمات إطلاق جاهزة للفيد والستوري.",
           "A sportswear store relaunched with a lion identity, a dark cinematic campaign style, and launch creatives for feed and stories.",
           imgs(lang, ["noby-banner.webp","noby-fire1.webp","noby-fire2.webp","noby-fire3.webp"], "g-noby"), dark=True) + \
      case(lang, "نَفحة Nafha", "هوية · بوستات · فيديو إعلاني", "Identity · Posts · Video ad",
           "عطر عود خليجي: لوجو بالخط العربي، وصور منتج فاخرة، و٤ بوستات إطلاق، وريل بتعليق صوتي خليجي وموسيقى أصلية.",
           "A Gulf oud perfume: Arabic calligraphic logo, luxury product shots, 4 launch posts, and a reel with Gulf voiceover and original music.",
           imgs(lang, ["nafha-post1.webp","nafha-post2.webp","nafha-post3.webp","nafha-post4.webp"], "g-4"), note=spec) + \
      case(lang, "Dune & Dew", "صور منتجات · تجميل", "Product photography · Skincare",
           "خط عناية بالبشرة اتصوّر بالكامل بالذكاء الاصطناعي: استوديو، ورمال، وأبيض نقي، بنفس العبوة والليبل في كل لقطة.",
           "A skincare line shot entirely with AI: studio, sand and pure white, with the same bottle and label in every frame.",
           imgs(lang, ["dune-set.webp"], "g-1"), note=spec) + \
      case(lang, T(lang,"ريلز إعلانية","Ad reels"), "فيديو · تعليق صوتي عربي", "Video · Arabic voiceover",
           "٣ إعلانات طولية: نفحة بتعليق خليجي، ودرب موتورز بتعليق مصري، وإعلان سيدان فاخرة نفّذناه لوكيل سيارات ومعروض هنا من غير علامات تجارية.",
           "Three vertical ads: Nafha with Gulf voiceover, Darb Motors with Egyptian voiceover, and a luxury sedan spot made for a car dealer, shown here without trademarks.",
           reels, dark=True, note=("نفحة ودرب براندات مفاهيمية.", "Nafha and Darb are concept brands.")) + "</section>" + foot(lang)

def growth(lang):
    phases = [(T(lang,"الفهم","Research"), T(lang,"المنتج والمنافسين والجمهور، وهدف واحد قابل للقياس.","Product, competitors and audience, and one measurable goal.")),
              (T(lang,"الإبداع","Creatives"), T(lang,"٣–٥ زوايا إعلانية، كل زاوية بنسختين صورة وفيديو.","3–5 ad angles, each in an image and a video version.")),
              (T(lang,"الاختبار","Testing"), T(lang,"ميزانية صغيرة على كل زاوية، ونوقف الضعيف بسرعة.","A small budget on each angle; weak ones stop fast.")),
              (T(lang,"التوسيع","Scaling"), T(lang,"نزوّد الميزانية على اللي جاب رسايل وطلبات بأقل تكلفة.","We scale what brings messages and orders at the lowest cost."))]
    ph = "".join(f'<li class="reveal"><b>{a}</b><span>{b}</span></li>' for a, b in phases)
    metrics = [(T(lang,"تكلفة الرسالة","Cost per message"), T(lang,"كام بندفع عشان عميل يكلمنا واتساب أو ماسنجر.","What we pay for each WhatsApp or Messenger conversation.")),
               (T(lang,"تكلفة الطلب","Cost per order"), T(lang,"الرقم اللي بيقول الإعلان كسبان ولا لأ.","The number that says whether the ad is profitable.")),
               (T(lang,"نسبة الضغط","Click-through rate"), T(lang,"هل الإعلان بيوقّف الناس فعلًا.","Whether the ad actually stops the scroll.")),
               (T(lang,"تقرير كل أسبوع","Weekly report"), T(lang,"صفحة واحدة: صرفنا كام، وجاب إيه، وهنعمل إيه بعدها.","One page: what we spent, what it brought, what we do next."))]
    mt = "".join(f'<li class="reveal"><b>{a}</b><span>{b}</span></li>' for a, b in metrics)
    p = "" if lang == "ar" else "../"
    return page_head(lang, "growth", "إعلانات بتجيب<br>رسايل وطلبات.", "Ads that bring<br>messages and orders.",
        "ندير حملاتك على ميتا وتيك توك وجوجل، من الفكرة والتصميم للاختبار والتقرير.",
        "We run your campaigns on Meta, TikTok and Google, from idea and creative to testing and reporting.",
        "noby-fire2.webp", "growth.html") + f"""
<section class="method p-growth"><div class="wrap"><h2 class="reveal">{T(lang,'إزاي بنشغّل الحملة','How we run a campaign')}</h2><ol class="steps light">{ph}</ol></div></section>
<section class="wrap block"><h2 class="reveal">{T(lang,'بنتابع إيه','What we track')}</h2><ul class="metrics">{mt}</ul></section>
<section class="cases">""" + \
      case(lang, T(lang,"درب موتورز — حملة «عربيتك الجاية»","Darb Motors — “Your next car” campaign"), "استراتيجية · خطة ميديا · تصميمات A/B", "Strategy · Media plan · A/B creatives",
           "حملة شهرية لمعرض عربيات هدفها حجوزات تجربة قيادة مؤهلة على واتساب: الحساب بالعكس من هدف المبيعات، و٣ جماهير بـ٣ زوايا، و٥ حملات بأسماء موحّدة على ميتا وجوجل، و٥ بوستات و٣ ستوري بنسخ A/B.",
           "A monthly campaign for a car showroom aimed at qualified test-drive bookings on WhatsApp: budget worked back from the sales target, 3 audiences with 3 angles, 5 consistently named campaigns on Meta and Google, and 5 posts and 3 stories with A/B versions.",
           imgs(lang, ["darbc-strategy.webp","darbc-feed1_a.webp","darbc-feed1_b.webp","darbc-audiences.webp","darbc-feed2.webp","darbc-feed3.webp","darbc-mediaplan.webp","darbc-story1.webp","darbc-story2.webp","darbc-story3.webp","darbc-feed4.webp"], "g-camp"),
           note=("حملة مفاهيمية — الأرقام فرضيات تخطيط مش نتايج.", "Concept campaign — figures are planning assumptions, not results.")) + \
      case(lang, T(lang,"تصميمات إعلانية","Ad creatives"), "فيد · ستوري · ريلز", "Feed · Stories · Reels",
           "نماذج من تصميماتنا الإعلانية: حملة NOBY الداكنة، وريلز نفحة ودرب. كل حملة بنطلقها بأكتر من زاوية ونسيب الأرقام تختار.",
           "Samples of our ad creative: the dark NOBY campaign and the Nafha and Darb reels. Every campaign launches with several angles and lets the numbers choose.",
           imgs(lang, ["noby-fire1.webp","noby-fire3.webp","nafha-post2.webp","darb-poster.webp"], "g-4")) + "</section>" + foot(lang)

def tech(lang):
    p = "" if lang == "ar" else "../"
    def dev(d, m):
        return f'<div class="devices"><div class="laptop"><img src="{p}assets/img/{d}" alt="" loading="lazy"></div><div class="phone"><img src="{p}assets/img/{m}" alt="" loading="lazy"></div></div>'
    caps = [(T(lang,"مواقع وصفحات هبوط","Websites & landing pages"), T(lang,"HTML وReact، استضافة مجانية أو على دومينك.","HTML and React, free hosting or your own domain.")),
            (T(lang,"أنظمة وأتمتة","Systems & automation"), T(lang,"n8n، وGoogle Sheets وExcel، وواتساب، ولوحات أرقام.","n8n, Google Sheets and Excel, WhatsApp, dashboards.")),
            (T(lang,"تطبيقات أندرويد","Android apps"), T(lang,"Flutter وKotlin، وFirebase، وواجهات عربية من الأساس.","Flutter and Kotlin, Firebase, Arabic-first interfaces."))]
    cp = "".join(f'<li class="reveal"><b>{a}</b><span>{b}</span></li>' for a, b in caps)
    return page_head(lang, "tech", "مواقع وأنظمة<br>بتشغّل البيزنس.", "Sites and systems<br>that run the business.",
        "صفحات هبوط بتبيع، وأنظمة بتوفّر وقتك، وتطبيقات أندرويد بواجهات عربية احترافية.",
        "Landing pages that sell, systems that save your time, and Android apps with polished Arabic interfaces.",
        "darb-site-m.webp", "tech.html") + f"""
<section class="method p-tech"><div class="wrap"><h2 class="reveal">{T(lang,'بنبني بإيه','What we build with')}</h2><ul class="steps light">{cp}</ul></div></section>
<section class="cases">""" + \
      case(lang, T(lang,"لُمعة — نظام الحجوزات","Lumaa — booking system"), "نظام · أتمتة واتساب · n8n", "System · WhatsApp automation · n8n",
           "لوحة استقبال لعيادة أسنان وتجميل: مواعيد اليوم والأسبوع، وملفات المرضى، ومنع تعارض المواعيد. كل حجز بيبعت تأكيد واتساب، وقبل الميعاد بـ٢٤ ساعة بيتبعت تذكير، وبعد الزيارة طلب تقييم — تلقائيًا بـ n8n.",
           "A front-desk system for a dental and aesthetics clinic: today's and the week's appointments, patient records and clash-free booking. Every booking sends a WhatsApp confirmation, a reminder goes out 24 hours before, and a review request follows the visit, all automated with n8n.",
           dev("lumaa-sys-d.webp", "lumaa-sys-m.webp"), note=("ديمو تفاعلي ببيانات وهمية — جرّب تحجز وشوف رسالة الواتساب.", "Interactive demo with dummy data: make a booking and watch the WhatsApp message."),
           link=("demos/lumaa/" if lang=="ar" else "../demos/lumaa/", "جرّب النظام", "Try the system")) + \
      case(lang, T(lang,"درب موتورز — تطبيق أندرويد","Darb Motors — Android app"), "تصميم تطبيق · نموذج تفاعلي", "App design · Interactive prototype",
           "تطبيق لمعرض العربيات بـ٦ شاشات: البداية، والموديلات بعرض الشهر، وتفاصيل العربية بالألوان والمواصفات، وحاسبة قسط حية، وحجز تجربة قيادة في المعرض أو البيت، وحسابي بالحجوزات. الواجهة عربية من الأساس والتنقل سلس.",
           "A showroom app with 6 screens: onboarding, models with the monthly offer, car details with colours and specs, a live instalment calculator, test-drive booking at the showroom or at home, and a profile with bookings. Arabic-first interface with smooth navigation.",
           f'''<div class="grid g-app"><img src="{p}assets/img/darb-app-board.webp" alt="" loading="lazy"><video src="{p}assets/video/darb-app.mp4" poster="{p}assets/img/darb-app-poster.webp" controls muted loop playsinline preload="none"></video><img src="{p}assets/img/darb-app-car.webp" alt="" loading="lazy"><img src="{p}assets/img/darb-app-calc.webp" alt="" loading="lazy"></div>''',
           dark=True, note=("نموذج تفاعلي ببيانات وهمية — جاهز للتنفيذ بـ Flutter.", "Interactive prototype with dummy data, ready to build in Flutter."),
           link=("demos/darb-app/" if lang=="ar" else "../demos/darb-app/", "جرّب التطبيق", "Try the app")) + \
      case(lang, "درب موتورز", "صفحة هبوط · حاسبة قسط", "Landing page · Instalment calculator",
           "موقع معرض عربيات بحاسبة قسط حية، وطلب تجربة قيادة يوصل واتساب برسالة جاهزة فيها الموديل والقسط.",
           "A car showroom site with a live instalment calculator and a test-drive request that lands on WhatsApp with the model and instalment filled in.",
           dev("darb-site-d.webp", "darb-site-m.webp"), note=("مشروع مفاهيمي — الاسم والعربيات والأسعار من تصميمنا.", "Concept project — name, cars and prices designed by us."),
           link=("https://tahawi0.github.io/darb-motors/", "جرّب الموقع", "Try the site")) + \
      case(lang, "طاقة كافيه", "منيو وطلبات أونلاين", "Menu & online ordering",
           "منيو كافيه بسلة طلبات بتتبعت على واتساب بالأصناف والإجمالي والعنوان، من غير تطبيق ولا عمولات.",
           "A café menu with a cart that sends the order to WhatsApp with items, total and address, with no app and no commissions.",
           dev("taqa-site-d.webp", "taqa-cart.webp"), dark=True, note=("مشروع مفاهيمي.", "Concept project."),
           link=("https://tahawi0.github.io/taqa-coffee/", "جرّب الموقع", "Try the site")) + \
      case(lang, "NOBY Sports", "كتالوج متجر", "Store catalogue",
           "كتالوج منتجات للموبايل بالمقاسات والأسعار، وطلب بضغطة على واتساب للقاهرة والجيزة.",
           "A mobile product catalogue with sizes and prices, and one-tap WhatsApp ordering for Cairo and Giza.",
           dev("noby-site-desktop.webp", "noby-site-mobile.webp")) + "</section>" + foot(lang)


# ---------- shared blocks: packages + FAQ ----------
def packages(lang, dark=False):
    cards = ""
    for k in PACKAGES:
        per = k["egp"] // k["n"]
        if lang == "ar":
            name, cost = f"{ar_num(k['n'])} صور", f"{ar_num(k['egp'])} ج.م"
            sub = f"{ar_num(per)} ج.م للصورة"
            msg = f"أهلًا كادر، حابب أطلب باقة {ar_num(k['n'])} صور منتجات ({ar_num(k['egp'])} ج.م)."
        else:
            name, cost = f"{k['n']} photos", f"${k['usd']}"
            sub = f"${k['usd']/k['n']:.0f} per photo"
            msg = f"Hi Kadr Studio, I'd like the {k['n']}-photo product package (${k['usd']})."
        badge = f'<span class="pk-badge">{T(lang,"الأوفر للمحلات","Best value for shops")}</span>' if k.get("pick") else ""
        cards += f"""<article class="pk{' pick' if k.get('pick') else ''} reveal">{badge}<h3>{name}</h3><p class="pk-price">{cost}</p><p class="pk-sub">{sub}</p>
<ul><li>{T(lang,'استوديو ولايف ستايل أو على موديل','Studio, lifestyle or on-model')}</li><li>{T(lang,'المنتج زي ما هو بالظبط','Your product kept exactly as it is')}</li><li>{T(lang,'مقاسات بوست وستوري ومتجر','Post, story and store sizes')}</li><li>{T(lang,'أول تسليم خلال ٤٨ ساعة + جولتين تعديلات','First delivery in 48h + two revision rounds')}</li></ul>
<a class="btn {'solid' if k.get('pick') else 'line'} js-wa" data-msg="{msg}" href="#contact">{T(lang,'اطلب الباقة','Order this package')}</a></article>"""
    return f"""<section class="packages{' dark' if dark else ''}" id="packages"><div class="wrap">
  <h2 class="reveal">{T(lang,'باقات صور المنتجات','Product photo packages')}</h2>
  <p class="lede reveal">{T(lang,'كل ما الكمية تزيد، سعر الصورة يقل. ابدأ بصورة مجانية الأول وبعدها اختار.','The more photos, the lower the price per photo. Start with a free one, then choose.')}</p>
  <div class="pk-grid">{cards}</div></div></section>"""

FAQ = [
  ("الصورة هتبقى شبه منتجي فعلًا؟", "Will the photo really look like my product?",
   "أيوه. شكل المنتج والليبل والألوان بيفضلوا زي ما هم، واللي بيتغير الخلفية والإضاءة والمكان أو الموديل. ولو فيه أي اختلاف بنعدّله.",
   "Yes. The product's shape, label and colours stay as they are; we change the background, light, setting or model. If anything is off, we fix it."),
  ("بتستخدموا ذكاء اصطناعي؟", "Do you use AI?",
   "أيوه، وبنقولها بوضوح. بنستخدم أدوات ذكاء اصطناعي في التصوير والفيديو، وكل صورة بتتراجع وتتظبط يدويًا قبل التسليم.",
   "Yes, and we say so openly. We use AI tools for photo and video, and every image is checked and refined by hand before delivery."),
  ("التسليم بياخد قد إيه؟", "How long does delivery take?",
   "أول تسليم خلال ٤٨ ساعة من استلام صور المنتج، وبعدها جولتين تعديلات من غير تكلفة إضافية.",
   "First delivery within 48 hours of receiving your product photos, followed by two revision rounds at no extra cost."),
  ("الدفع إزاي؟", "How do I pay?",
   "نص المبلغ مقدمًا والباقي عند التسليم. بنتفق على طريقة الدفع على واتساب. العينة المجانية من غير أي دفع.",
   "Half up front and the rest on delivery; we agree the payment method on WhatsApp. The free sample needs no payment."),
  ("الصور ملك مين؟", "Who owns the files?",
   "ملككم بالكامل بعد الدفع، بجودة عالية تنفع للسوشيال والمتجر الإلكتروني والمطبوعات.",
   "They are fully yours after payment, in high resolution for social, your online store and print."),
  ("لازم نتقابل أو نتكلم في التليفون؟", "Do we need to meet or call?",
   "لأ. كل الشغل أونلاين على واتساب: تبعتوا الصور والتفاصيل، ونبعتلكم النتيجة.",
   "No. Everything runs online on WhatsApp: you send the photos and details, we send the result."),
  ("بتشتغلوا مع عملاء من الخليج؟", "Do you work with Gulf clients?",
   "أيوه. بنشتغل مع مصر والخليج، وبنكتب ونسجّل بالمصري أو الخليجي أو الفصحى، والدفع ممكن بالدولار.",
   "Yes. We work with Egypt and the Gulf, write and record in Egyptian, Gulf or formal Arabic, and can invoice in USD."),
]

def faq(lang):
    items = "".join(f'<details class="reveal"><summary>{T(lang,qa,qe)}</summary><p>{T(lang,aa,ae)}</p></details>' for qa, qe, aa, ae in FAQ)
    return f"""<section class="faq wrap" id="faq"><h2 class="reveal">{T(lang,'أسئلة بتتسأل كتير','Frequently asked')}</h2><div class="faq-list">{items}</div></section>"""

def faq_jsonld(lang):
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": T(lang,qa,qe), "acceptedAnswer": {"@type": "Answer", "text": T(lang,aa,ae)}} for qa, qe, aa, ae in FAQ]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"

def biz_jsonld(lang):
    data = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Kadr Studio — كادر",
            "url": SITE + ("/" if lang == "ar" else "/en/"), "image": SITE + "/assets/img/nafha-hero.webp",
            "email": EMAIL, "telephone": "+" + WA, "areaServed": ["EG", "SA", "AE", "KW", "QA"],
            "address": {"@type": "PostalAddress", "addressLocality": "Cairo", "addressCountry": "EG"},
            "sameAs": ["https://www.facebook.com/profile.php?id=61595815239270"],
            "description": T(lang, "استوديو إبداعي في القاهرة: تصوير منتجات بالذكاء الاصطناعي، وهويات وتصميم، وإعلانات ممولة، ومواقع وأنظمة.",
                             "Cairo creative studio: AI product photography, brand identity and design, paid ads, websites and systems.")}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"

# ---------- free sample landing page ----------
def sample(lang):
    p = "" if lang == "ar" else "../"
    msg = SAMPLE_MSG[lang]
    steps = [(T(lang,"ابعت الصورة","Send the photo"), T(lang,"صوّر منتجك بالموبايل من الأمام في إضاءة النهار، وابعته على واتساب مع اسم النشاط.","Shoot your product on your phone, front-on in daylight, and send it on WhatsApp with your business name.")),
             (T(lang,"نشتغل عليها","We work on it"), T(lang,"نختار شكل يناسب البراند: استوديو، أو لايف ستايل، أو على موديل.","We pick a look that suits the brand: studio, lifestyle or on-model.")),
             (T(lang,"تستلمها مجانًا","You get it free"), T(lang,"خلال ٤٨ ساعة توصلك صورة احترافية جاهزة للنشر، من غير أي التزام.","Within 48 hours you get a ready-to-post professional photo, with no commitment."))]
    st = "".join(f'<li class="reveal"><b>{a}</b><span>{b}</span></li>' for a, b in steps)
    terms = [T(lang,"صورة واحدة مجانية لكل نشاط تجاري.","One free photo per business."),
             T(lang,"المنتج بيفضل زي ما هو: الشكل والليبل والألوان.","The product stays as it is: shape, label and colours."),
             T(lang,"طاقتنا حوالي ٣٠ عينة في الأسبوع، وبنرد بالترتيب.","We can take about 30 samples a week and reply in order."),
             T(lang,"لو الصورة عجبتك، تقدر تكمل بباقة. ولو لأ، خليها عندك.","If you like it, you can continue with a package. If not, keep it anyway.")]
    tm = "".join(f"<li>{t}</li>" for t in terms)
    ex = "".join(frame(f, "", "", lang) for f in ["drape-look04.webp", "nafha-post1.webp", "lumaa-post-smile.webp"])
    title = T(lang, "صورة احترافية لمنتجك مجانًا — كادر استوديو", "A professional photo of your product, free — Kadr Studio")
    desc = T(lang, "ابعت صورة منتج واحدة من الموبايل على واتساب، وخدها صورة استوديو احترافية خلال ٤٨ ساعة مجانًا. لمحلات الملابس والعطور والتجميل والمطاعم.",
             "Send one phone photo of your product on WhatsApp and get a professional studio shot back within 48 hours, free.")
    return head(lang, title, desc, "free-sample.html", extra=faq_jsonld(lang), image="drape-look02.webp") + nav(lang, "free-sample.html") + f"""
<section class="fs-hero wrap">
  <div class="fs-text">
    <p class="kicker reveal">{T(lang,'عرض العينة المجانية','Free sample offer')}</p>
    <h1 class="reveal">{T(lang,'ابعت صورة موبايل.<br>خدها صورة حملة.','Send a phone photo.<br>Get a campaign shot.')}</h1>
    <p class="lede reveal">{T(lang,'صورة منتج واحدة على واتساب، ونرجعهالك صورة احترافية خلال ٤٨ ساعة — مجانًا ومن غير أي التزام.','One product photo on WhatsApp, and we send back a professional shot within 48 hours, free and with no commitment.')}</p>
    <div class="cta-row reveal"><a class="btn solid js-wa" data-msg="{msg}" href="#contact">{T(lang,'ابعت صورتك على واتساب','Send your photo on WhatsApp')}</a><a class="btn line" href="#packages">{T(lang,'شوف الباقات','See packages')}</a></div>
  </div>
  <div class="ba reveal">
    <figure><img src="{p}assets/img/drape-flatlay.webp" alt="{T(lang,'قبل: صورة القطعة','Before: the garment photo')}"><figcaption>{T(lang,'قبل','Before')}</figcaption></figure>
    <span class="ba-arr" aria-hidden="true">{T(lang,'←','→')}</span>
    <figure><img src="{p}assets/img/drape-look02.webp" alt="{T(lang,'بعد: على موديل بإضاءة استوديو','After: on a model in studio light')}"><figcaption class="after">{T(lang,'بعد','After')}</figcaption></figure>
    <p class="ba-note">{T(lang,'نفس القطعة بالظبط، من غير سيشن تصوير — من شغلنا لبراند Drapé Atelier.','The exact same piece, with no photoshoot — our work for Drapé Atelier.')}</p>
  </div>
</section>
<section class="process wrap"><h2 class="reveal">{T(lang,'٣ خطوات بس','Just 3 steps')}</h2><ol class="steps fs-steps">{st}</ol></section>
<section class="fs-band"><div class="wrap fs-band-in">
  <div><h2 class="reveal">{T(lang,'مناسب لمين؟','Who is it for?')}</h2>
  <p class="lede reveal">{T(lang,'محلات وبراندات الملابس، والعطور ومستحضرات التجميل، والهاندميد، والمطاعم والكافيهات.','Clothing stores and labels, perfume and beauty, handmade products, restaurants and cafés.')}</p>
  <ul class="terms reveal">{tm}</ul></div>
  <div class="fs-ex reveal">{ex}</div>
</div></section>
""" + packages(lang) + faq(lang) + f"""
<section class="fs-final wrap"><h2 class="reveal">{T(lang,'جرب ببلاش الأول.','Try it free first.')}</h2>
<a class="btn solid js-wa reveal" data-msg="{msg}" href="#contact">{T(lang,'ابعت صورة منتجك دلوقتي','Send your product photo now')}</a></section>
""" + foot(lang)

def sitemap():
    pages = ["", "free-sample.html", "creative.html", "growth.html", "tech.html"]
    urls = ""
    for pg in pages:
        for pre in ("", "en/"):
            urls += f"<url><loc>{SITE}/{pre}{pg}</loc></url>\n"
    urls += f"<url><loc>{SITE}/demos/lumaa/</loc></url>\n<url><loc>{SITE}/demos/darb-app/</loc></url>\n"
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

PAGES = {"index.html": home, "free-sample.html": sample, "creative.html": creative, "growth.html": growth, "tech.html": tech}
os.makedirs("en", exist_ok=True)
for name, fn in PAGES.items():
    open(name, "w").write(fn("ar"))
    open(os.path.join("en", name), "w").write(fn("en"))
sitemap()
print("built", len(PAGES) * 2, "pages + sitemap")
