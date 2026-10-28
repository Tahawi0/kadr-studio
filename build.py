#!/usr/bin/env python3
"""Static generator for Kadr Studio v2: Arabic at /, English at /en/."""
import os, json

WA = "201555014697"
EMAIL = "kadr.studio6@gmail.com"
SITE = "https://tahawi0.github.io/kadr-studio"
# Fill these in when the accounts exist (leave "" to switch off)
GOATCOUNTER = "kadrstudio"      # e.g. "kadrstudio"  -> https://kadrstudio.goatcounter.com
META_PIXEL = ""       # e.g. "123456789012345" from Meta Events Manager
GSC_TOKEN = "6-PiXOCklsRUEXaHXwVfm2oIPjcwCfjL655V1HjhYuI"        # Google Search Console HTML-tag verification content
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
             ("free-sample.html", T(lang, "صورة مجانية", "Free photo")), ("index.html#tools", T(lang, "أدوات مجانية", "Free tools"))]
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
    <nav class="foot-links">{''.join(f'<a href="for-{x["key"]}.html">{T(lang,x["ar"],x["en"])}</a>' for x in SECTORS)}<a href="free-sample.html">{T(lang,'صورة مجانية','Free photo')}</a><a href="order.html">{T(lang,'اطلب صورك','Order photos')}</a><a href="photo-guide.html">{T(lang,'دليل التصوير بالموبايل','Phone photo guide')}</a><a href="audit.html">{T(lang,'قيّم صفحتك','Rate your page')}</a></nav>
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
             ("nafha-post1.webp", "Nafha"), ("taqa-site-m.webp", "Taqa"), ("dune-set.webp", "Dune & Dew")]
    sheet_html = "".join(frame(s, a, f"s{i}", lang) for i, (s, a) in enumerate(sheet))
    pill_imgs = {"creative": ["lumaa-reception.webp", "nafha-post1.webp", "drape-look04.webp"],
                 "growth": ["darbc-feed1_a.webp", "darb-poster.webp", "nafha-poster.webp"],
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
""" + tools_section(lang) + f"""
<section id="pillars" class="pillars">{pillars}</section>
""" + sector_cards(lang) + f"""
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
           "براند أزياء محتشمة من الصفر: الاسم، ونظام اللوجو، وألوان ترابية بلمسة نبيتي، و١٠ لوكات حملة من صور موبايل للقطع على الشماعة، من غير سيشن تصوير.",
           "A modest-fashion label from zero: name, logo system, earthy palette with a wine accent, and 10 campaign looks made from phone photos of the pieces on hangers, with no photoshoot.",
           imgs(lang, ["drape-look02.webp","drape-before.webp","drape-look04.webp","drape-logos.webp","drape-post08.webp","drape-detail.webp"], "g-3")) + \
      case(lang, "نَفحة Nafha", "هوية · بوستات · فيديو إعلاني", "Identity · Posts · Video ad",
           "عطر عود خليجي: لوجو بالخط العربي، وصور منتج فاخرة، و٤ بوستات إطلاق، وريل بتعليق صوتي خليجي وموسيقى أصلية.",
           "A Gulf oud perfume: Arabic calligraphic logo, luxury product shots, 4 launch posts, and a reel with Gulf voiceover and original music.",
           imgs(lang, ["nafha-post1.webp","nafha-post2.webp","nafha-post3.webp","nafha-post4.webp"], "g-4"), dark=True, note=spec) + \
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
        "darbc-feed1_a.webp", "growth.html") + f"""
<section class="method p-growth"><div class="wrap"><h2 class="reveal">{T(lang,'إزاي بنشغّل الحملة','How we run a campaign')}</h2><ol class="steps light">{ph}</ol></div></section>
<section class="wrap block"><h2 class="reveal">{T(lang,'بنتابع إيه','What we track')}</h2><ul class="metrics">{mt}</ul></section>
<section class="cases">""" + \
      case(lang, T(lang,"درب موتورز — حملة «عربيتك الجاية»","Darb Motors — “Your next car” campaign"), "استراتيجية · خطة ميديا · تصميمات A/B", "Strategy · Media plan · A/B creatives",
           "حملة شهرية لمعرض عربيات هدفها حجوزات تجربة قيادة مؤهلة على واتساب: الحساب بالعكس من هدف المبيعات، و٣ جماهير بـ٣ زوايا، و٥ حملات بأسماء موحّدة على ميتا وجوجل، و٥ بوستات و٣ ستوري بنسخ A/B.",
           "A monthly campaign for a car showroom aimed at qualified test-drive bookings on WhatsApp: budget worked back from the sales target, 3 audiences with 3 angles, 5 consistently named campaigns on Meta and Google, and 5 posts and 3 stories with A/B versions.",
           imgs(lang, ["darbc-strategy.webp","darbc-feed1_a.webp","darbc-feed1_b.webp","darbc-audiences.webp","darbc-feed2.webp","darbc-feed3.webp","darbc-mediaplan.webp","darbc-story1.webp","darbc-story2.webp","darbc-story3.webp","darbc-feed4.webp"], "g-camp"),
           note=("حملة مفاهيمية — الأرقام فرضيات تخطيط مش نتايج.", "Concept campaign — figures are planning assumptions, not results.")) + \
      case(lang, T(lang,"تصميمات إعلانية","Ad creatives"), "فيد · ستوري · ريلز", "Feed · Stories · Reels",
           "نماذج من تصميماتنا الإعلانية: بوستات درب موتورز، وبوستات وريلز نفحة. كل حملة بنطلقها بأكتر من زاوية ونسيب الأرقام تختار.",
           "Samples of our ad creative: Darb Motors posts, and Nafha posts and reels. Every campaign launches with several angles and lets the numbers choose.",
           imgs(lang, ["darbc-feed3.webp","nafha-post2.webp","darbc-feed2.webp","nafha-post3.webp"], "g-4")) + "</section>" + foot(lang)

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
           link=("https://tahawi0.github.io/taqa-coffee/", "جرّب الموقع", "Try the site")) + "</section>" + foot(lang)


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


# ---------- sector pages ----------
SECTORS = [
 dict(key="fashion", ar="ملابس وأزياء", en="Fashion & clothing", img="drape-look02.webp",
  h_ar="صور تبيع القطعة<br>قبل ما تتلمس.", h_en="Photos that sell the piece<br>before it's touched.",
  l_ar="لمحلات وبراندات الملابس: صور على موديل بإضاءة استوديو من صورة موبايل، وهوية وإعلانات بتجيب رسايل.",
  l_en="For clothing stores and labels: on-model studio shots from a phone photo, plus identity and ads that bring in messages.",
  pains=[("صور الشماعة مش بتبيع","Hanger photos don't sell","العميلة عايزة تشوف القطعة لابسها حد، مش متعلقة على الحيطة.","Customers want to see the piece worn, not hanging on a wall."),
         ("سيشن التصوير غالي ومتعب","Photoshoots are costly and slow","موديل واستوديو ومصور لكل كولكشن، ولسه فيه قطع جديدة كل أسبوع.","A model, studio and photographer for every drop, with new pieces every week."),
         ("الصفحة شكلها مش موحّد","The page looks inconsistent","كل بوست بلون وإضاءة مختلفة، فالبراند مش بيتحفظ.","Every post has different light and colour, so the brand doesn't stick.")],
  svcs=["photos","graphics","identity","ads"], work=["drape-before.webp","drape-look02.webp","drape-look04.webp","drape-look03.webp","drape-post08.webp","drape-look05.webp"],
  links=[("creative.html","شوف شغل Drapé كامل","See the full Drapé work")], offer="sample"),
 dict(key="beauty", ar="تجميل وعطور", en="Beauty & perfume", img="nafha-hero.webp",
  h_ar="منتجك يستاهل<br>صورة أفخم.", h_en="Your product deserves<br>a richer shot.",
  l_ar="للعطور ومستحضرات التجميل والعناية: صور منتج فاخرة، وريلز بتعليق صوتي عربي، وبوستات بهوية واحدة.",
  l_en="For perfume, beauty and skincare: luxury product shots, reels with Arabic voiceover, and posts in one consistent look.",
  pains=[("العبوة حلوة والصورة لأ","Great bottle, flat photo","صورة الموبايل بتطفي اللمعة والتفاصيل اللي دفعت فيها.","Phone photos flatten the shine and details you paid for."),
         ("المنافسين شكلهم أغلى","Competitors look pricier","العميل بيحكم على السعر من شكل الصورة قبل ما يقرأ أي حاجة.","Buyers judge the price from the photo before reading anything."),
         ("الريلز محتاجة إنتاج","Reels need production","فيديو بتعليق صوتي وموسيقى بياخد وقت وفلوس لو اتعمل تقليدي.","A reel with voiceover and music takes time and money the usual way.")],
  svcs=["photos","video","identity","graphics"], work=["nafha-post1.webp","dune-set.webp","nafha-post2.webp","nafha-gift.webp","nafha-post3.webp","nafha-majlis.webp"],
  links=[("creative.html","شوف شغل نفحة وDune & Dew","See Nafha and Dune & Dew")], offer="sample"),
 dict(key="food", ar="مطاعم وكافيهات", en="Restaurants & cafés", img="taqa-hero.webp",
  h_ar="منيو يفتح النفس،<br>وطلب يوصل واتساب.", h_en="A menu that tempts,<br>orders that land on WhatsApp.",
  l_ar="للمطاعم والكافيهات: صور أصناف بتفتح النفس، ومنيو أونلاين بيبعت الطلب على واتساب من غير عمولات تطبيقات.",
  l_en="For restaurants and cafés: dish photos that make people hungry, and an online menu that sends orders to WhatsApp with no app commissions.",
  pains=[("عمولات التطبيقات بتاكل الربح","App commissions eat the margin","٢٠–٣٠٪ من كل طلب بتروح لتطبيقات التوصيل.","20–30% of every order goes to delivery apps."),
         ("صور الأكل مش بتشهّي","Food photos don't tempt","إضاءة المطبخ بتخلي أحلى صنف شكله عادي.","Kitchen light makes the best dish look ordinary."),
         ("الطلبات بتضيع في الرسايل","Orders get lost in chats","العميل يسأل عن المنيو والأسعار والتوصيل في ١٠ رسايل.","Customers ask about the menu, prices and delivery over 10 messages.")],
  svcs=["photos","web","graphics","social"], work=["taqa-hero.webp","taqa-site-m.webp","taqa-cart.webp","taqa-spanish.webp"],
  links=[("https://tahawi0.github.io/taqa-coffee/","جرّب منيو طاقة","Try the Taqa menu")], offer="sample"),
 dict(key="clinics", ar="عيادات ومراكز", en="Clinics & centres", img="lumaa-reception.webp",
  h_ar="عيادة شكلها يطمّن،<br>ومواعيد بتتنظم لوحدها.", h_en="A clinic that reassures,<br>bookings that run themselves.",
  l_ar="لعيادات الأسنان والتجميل والمراكز الطبية: هوية بتبني ثقة، ونظام حجوزات بتأكيد وتذكير واتساب تلقائي.",
  l_en="For dental, aesthetics and medical clinics: an identity that builds trust, and a booking system with automatic WhatsApp confirmations and reminders.",
  pains=[("مرضى بيحجزوا ومش بييجوا","No-shows","من غير تذكير، نسبة الغياب بتاكل جدول اليوم.","Without reminders, no-shows eat the day's schedule."),
         ("الاستقبال غرقان في المكالمات","Reception drowns in calls","تأكيد وتغيير وإلغاء مواعيد طول اليوم بالتليفون.","Confirming, moving and cancelling appointments by phone all day."),
         ("الشكل مش بيعكس المستوى","The look undersells the care","لوجو قديم وبوستات عشوائية بتخلي العيادة شكلها أقل من مستواها.","An old logo and random posts make the clinic look below its level.")],
  svcs=["identity","systems","graphics","ads"], work=["lumaa-reception.webp","lumaa-sys-d.webp","lumaa-post-smile.webp","lumaa-stationery.webp","lumaa-exterior.webp","lumaa-post-offer.webp"],
  links=[("demos/lumaa/","جرّب نظام الحجوزات","Try the booking system")], offer="screen"),
 dict(key="cars", ar="معارض وتوكيلات عربيات", en="Car showrooms & dealers", img="darb-hero.webp",
  h_ar="حجوزات تجربة قيادة،<br>مش لايكات.", h_en="Test-drive bookings,<br>not likes.",
  l_ar="لمعارض ووكلاء العربيات: حملات ممولة بهدف حجوزات مؤهلة على واتساب، وريلز بتعليق صوتي، وصفحات وتطبيقات بحاسبة قسط.",
  l_en="For showrooms and dealers: paid campaigns aimed at qualified WhatsApp bookings, voiceover reels, and pages and apps with an instalment calculator.",
  pains=[("رسايل كتير وحجوزات قليلة","Lots of messages, few bookings","«بكام؟» و«فيه قسط؟» من ناس مش جاهزة تشتري.","“How much?” and “Instalments?” from people not ready to buy."),
         ("الإعلان مش متقاس","Ads aren't measured","مفيش رقم واضح لتكلفة الحجز أو العميل الجاد.","No clear cost per booking or per serious lead."),
         ("المحتوى شبه بعضه","Content all looks the same","نفس صور التوكيل اللي عند كل المعارض التانية.","The same factory photos every other showroom posts.")],
  svcs=["ads","video","web","android"], work=["darbc-strategy.webp","darb-poster.webp","darbc-feed1_a.webp","darb-app-car.webp","darbc-feed2.webp","darb-site-m.webp"],
  links=[("growth.html","شوف حملة درب موتورز","See the Darb Motors campaign"),("demos/darb-app/","جرّب تطبيق درب","Try the Darb app")], offer="screen"),
]
ALL_SVCS = {x["id"]: x for k in SERVICES for x in SERVICES[k]}

def sector_cards(lang):
    p = "" if lang == "ar" else "../"
    cards = "".join(f'<a class="sec-card reveal" href="for-{sc["key"]}.html"><img src="{p}assets/img/{sc["img"]}" alt="" loading="lazy"><span>{T(lang,sc["ar"],sc["en"])} <b class="arr">{T(lang,"←","→")}</b></span></a>' for sc in SECTORS)
    return f'<section class="sectors wrap" id="sectors"><h2 class="reveal">{T(lang,"شغلنا لمجالك","Work for your field")}</h2><p class="lede reveal">{T(lang,"اختار مجالك وشوف بنحل مشاكله إزاي، وبأمثلة من شغلنا.","Pick your field and see how we solve its problems, with examples of our work.")}</p><div class="sec-grid">{cards}</div></section>'

def sector_page(sc):
    def build(lang):
        p = "" if lang == "ar" else "../"
        page = f"for-{sc['key']}.html"
        pains = "".join(f'<li class="reveal"><b>{T(lang,a,b)}</b><span>{T(lang,c,d)}</span></li>' for a, b, c, d in sc["pains"])
        rows = "".join(f'<li class="svc reveal"><div><h3>{T(lang,ALL_SVCS[i]["ar"],ALL_SVCS[i]["en"])}</h3><p>{T(lang,ALL_SVCS[i]["dar"],ALL_SVCS[i]["den"])}</p></div><b>{price(lang,ALL_SVCS[i])}</b></li>' for i in sc["svcs"])
        work = "".join(f'<img src="{p}assets/img/{w}" alt="" loading="lazy">' for w in sc["work"])
        lk = ""
        for href, a, b in sc["links"]:
            ext = href.startswith("http")
            h = href if ext or lang == "ar" else "../" + href
            lk += f'<a class="btn line" href="{h}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{T(lang,a,b)} <span class="arr">{T(lang,"←","→")}</span></a>'
        if sc["offer"] == "sample":
            msg = T(lang, f"أهلًا كادر، عندي نشاط في مجال {sc['ar']} وعايز أجرب الصورة المجانية.", f"Hi Kadr Studio, I run a {sc['en'].lower()} business and I'd like to try the free photo.")
            offer = f"""<section class="offer-band"><div class="wrap offer-in"><p class="reveal"><b>{T(lang,'جرّبنا ببلاش:','Try us free:')}</b> {T(lang,'ابعت صورة منتج واحدة من الموبايل، وخدها صورة احترافية خلال ٤٨ ساعة.','send one phone photo of a product and get a professional shot within 48 hours.')}</p><a class="btn solid light js-wa reveal" data-msg="{msg}" href="#contact">{T(lang,'ابعت صورتك','Send your photo')}</a></div></section>""" + packages(lang)
        else:
            msg = T(lang, f"أهلًا كادر، عندي {sc['ar']} وحابب أعرف تفاصيل أكتر.", f"Hi Kadr Studio, I run a {sc['en'].lower()} business and I'd like to know more.")
            offer = f"""<section class="offer-band"><div class="wrap offer-in"><p class="reveal"><b>{T(lang,'خطوة أولى مجانية:','Free first step:')}</b> {T(lang,'احكيلنا عن نشاطك، ونرسملك شاشة واحدة أو تصميم إعلان واحد ببلاش عشان تشوف الشكل قبل ما تقرر.','tell us about your business and we design one screen or one ad for free, so you see it before you decide.')}</p><a class="btn solid light js-wa reveal" data-msg="{msg}" href="#contact">{T(lang,'كلّمنا واتساب','Talk on WhatsApp')}</a></div></section>"""
        title = T(lang, f"{sc['ar']} — كادر استوديو", f"{sc['en']} — Kadr Studio")
        return head(lang, title, T(lang, sc["l_ar"], sc["l_en"]), page, image=sc["img"]) + nav(lang, page) + f"""
<section class="page-hero">
  <div class="wrap page-hero-in">
    <div><p class="kicker">{T(lang,'لـ','For ')}{T(lang,sc['ar'],sc['en'].lower())}</p><h1 class="reveal">{T(lang,sc['h_ar'],sc['h_en'])}</h1><p class="lede reveal">{T(lang,sc['l_ar'],sc['l_en'])}</p>
    <div class="cta-row reveal"><a class="btn solid js-wa" data-msg="{msg}" href="#contact">{T(lang,'كلّمنا واتساب','Talk on WhatsApp')}</a><a class="btn line" href="#work">{T(lang,'شوف الشغل','See the work')}</a></div></div>
    {frame(sc['img'], '', 'hero-img', lang)}
  </div>
</section>
<section class="method p-growth"><div class="wrap"><h2 class="reveal">{T(lang,'مشاكل نعرفها كويس','Problems we know well')}</h2><ul class="steps light">{pains}</ul></div></section>
<section class="wrap block"><h2 class="reveal">{T(lang,'اللي نقدر نعمله لك','What we can do for you')}</h2><ul class="svc-list">{rows}</ul></section>
<section class="wrap block sec-work" id="work"><h2 class="reveal">{T(lang,'من شغلنا','From our work')}</h2><div class="grid g-3 reveal">{work}</div><div class="cta-row reveal">{lk}</div></section>
""" + offer + (faq(lang) if sc["offer"] == "sample" else "") + foot(lang)
    return build


def tools_section(lang):
    items = [("audit.html", T(lang,"قيّم صفحتك في دقيقة","Rate your page in a minute"), T(lang,"٨ أسئلة عن صفحتك على فيسبوك وانستجرام، وتاخد درجة ونصايح تطبقها النهارده.","8 questions about your page, with a score and tips you can apply today."), T(lang,"ابدأ التقييم","Start"), "audit"),
             ("photo-guide.html", T(lang,"دليل التصوير بالموبايل","Phone photo guide"), T(lang,"٧ نصايح بسيطة تخلّي صورة منتجك أحسن من غير أي معدات.","7 simple tips for better product photos with no gear."), T(lang,"اقرا الدليل","Read the guide"), "guide"),
             ("order.html", T(lang,"جهّز طلب صورك","Build your photo order"), T(lang,"اختار المنتج والستايل والعدد، وشوف السعر قبل ما تكلمنا.","Pick product, style and quantity, and see the price before you message us."), T(lang,"جهّز الطلب","Build order"), "order")]
    icons = {"audit": '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="3"/><path d="M24 24 L24 10" stroke="#d9481f" stroke-width="4" stroke-linecap="round"/><path d="M24 24 L34 30" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>',
             "guide": '<svg viewBox="0 0 48 48"><rect x="14" y="4" width="20" height="40" rx="4" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="24" cy="12" r="3" fill="#d9481f"/><path d="M4 30 l8 -4 M4 22 l8 0 M4 14 l8 4" stroke="#d9481f" stroke-width="3" stroke-linecap="round"/></svg>',
             "order": '<svg viewBox="0 0 48 48"><rect x="8" y="6" width="32" height="38" rx="4" fill="none" stroke="currentColor" stroke-width="3"/><path d="M16 18 h16 M16 26 h16 M16 34 h9" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><circle cx="36" cy="36" r="8" fill="#d9481f"/></svg>'}
    cards = "".join(f'<a class="tool reveal" href="{h}"><span class="tool-ic">{icons[k]}</span><h3>{t}</h3><p>{d}</p><b>{c} <span class="arr">{T(lang,"←","→")}</span></b></a>' for h, t, d, c, k in items)
    return f'<section class="tools wrap" id="tools"><p class="kicker reveal">{T(lang,"ببلاش","Free")}</p><h2 class="reveal">{T(lang,"أدوات مجانية لنشاطك","Free tools for your business")}</h2><div class="tool-grid">{cards}</div></section>'

# ---------- page audit quiz ----------
AUDIT = [
 ("صورة البروفايل لوجو واضح يتقري في الدايرة الصغيرة؟","Is your profile picture a clear logo that reads in a small circle?","استخدم لوجو مبسّط على خلفية سادة، من غير كلام صغير.","Use a simplified logo on a plain background, with no small text.",10),
 ("صورة الغلاف بتقول بتبيع إيه في ثانية؟","Does your cover say what you sell in one second?","حط منتجك الأساسي وجملة واحدة بتقول بتعمل إيه ولمين.","Show your main product and one line on what you do and for whom.",10),
 ("صور المنتجات بإضاءة وخلفية موحّدة؟","Do product photos share the same light and background?","وحّد الخلفية والإضاءة، أو خلي كل الصور بنفس الستايل.","Unify background and light, or keep every photo in one style.",20),
 ("بتنزل بوست أو ريل ٣ مرات في الأسبوع على الأقل؟","Do you post at least 3 times a week?","اعمل جدول بسيط: ٣ بوستات ثابتة في الأسبوع أحسن من ١٠ مرة واحدة.","Keep a simple schedule: 3 steady posts a week beat 10 at once.",10),
 ("الأسعار واضحة في البوست أو الهايلايت؟","Are prices clear in posts or highlights?","«السعر في الخاص» بيطفّش ناس كتير. اكتب السعر أو «يبدأ من».","“Price in DM” drives people away. Show the price or a “from” price.",15),
 ("فيه زرار واتساب أو طريقة طلب واضحة؟","Is there a WhatsApp button or a clear way to order?","ضيف زرار واتساب للصفحة ولينك طلب مباشر في البايو.","Add a WhatsApp button and a direct order link in your bio.",15),
 ("بترد على الرسايل في أقل من ساعة؟","Do you reply to messages within an hour?","فعّل رد تلقائي ورسايل جاهزة. أول ساعة هي اللي بتقفل البيعة.","Turn on auto-replies and saved answers; the first hour closes the sale.",10),
 ("عندك تقييمات أو صور من عملاء حقيقيين؟","Do you show real customer reviews or photos?","اطلب من كل عميل راضي صورة أو جملة، وحطها في هايلايت «آراء العملاء».","Ask every happy customer for a photo or a line and pin them in a highlight.",10),
]

def audit(lang):
    qs = ""
    for i, (qa, qe, ta, te, w) in enumerate(AUDIT):
        qs += f"""<fieldset class="aq reveal" data-w="{w}" data-tip="{T(lang,ta,te)}" data-q="{T(lang,qa,qe)}"><legend><span>{i+1}</span>{T(lang,qa,qe)}</legend>
<label><input type="radio" name="q{i}" value="1"> {T(lang,'أيوه','Yes')}</label><label><input type="radio" name="q{i}" value="0.5"> {T(lang,'نص نص','Partly')}</label><label><input type="radio" name="q{i}" value="0"> {T(lang,'لأ','No')}</label></fieldset>"""
    title = T(lang, "قيّم صفحتك في دقيقة — كادر استوديو", "Rate your page in a minute — Kadr Studio")
    desc = T(lang, "٨ أسئلة سريعة عن صفحة نشاطك على فيسبوك وانستجرام، وتاخد درجة ونصايح عملية تطبقها النهارده.", "8 quick questions about your business page on Facebook and Instagram, with a score and practical tips.")
    return head(lang, title, desc, "audit.html") + nav(lang, "audit.html") + f"""
<section class="page-hero"><div class="wrap"><p class="kicker">{T(lang,'أداة مجانية','Free tool')}</p><h1 class="reveal">{T(lang,'قيّم صفحتك<br>في دقيقة.','Rate your page<br>in a minute.')}</h1><p class="lede reveal">{T(lang,'٨ أسئلة عن صفحة نشاطك على فيسبوك وانستجرام. جاوب بصراحة، وخد درجة ونصايح تقدر تطبقها النهارده بنفسك.','8 questions about your business page. Answer honestly and get a score plus tips you can apply yourself today.')}</p></div></section>
<section class="wrap audit-wrap"><form id="audit" class="audit">{qs}<button type="submit" class="btn solid">{T(lang,'اطلع النتيجة','Show my score')}</button></form>
<div id="auditOut" class="audit-out" hidden><p class="kicker">{T(lang,'نتيجتك','Your score')}</p><output id="auditScore"></output><h3 id="auditLevel"></h3><ul id="auditTips"></ul>
<a class="btn solid light" id="auditSend" href="#">{T(lang,'ابعت النتيجة واتساب وخد رأينا','Send the result on WhatsApp for our view')}</a><p class="note">{T(lang,'الإجابات بتفضل على جهازك. مش بنحفظ أي حاجة غير لو بعتّها إنت.','Your answers stay on your device; nothing is saved unless you send it.')}</p></div></section>
""" + foot(lang)

# ---------- phone photo guide ----------
def guide_svg(kind):
    ink, acc, paper = "#151412", "#d9481f", "#e8e1d3"
    base = f'<rect width="320" height="220" rx="6" fill="{paper}"/>'
    phone = lambda x, y, r=0: f'<g transform="translate({x} {y}) rotate({r})"><rect x="-22" y="-40" width="44" height="80" rx="8" fill="{ink}"/><circle cx="0" cy="-30" r="4" fill="{paper}"/></g>'
    prod = lambda x, y, s=1: f'<g transform="translate({x} {y}) scale({s})"><rect x="-18" y="-30" width="36" height="60" rx="6" fill="#b89b5e"/><rect x="-9" y="-44" width="18" height="16" rx="3" fill="{ink}"/><rect x="-12" y="-6" width="24" height="14" fill="{paper}"/></g>'
    if kind == "light":
        return base + f'<rect x="20" y="30" width="80" height="110" fill="#fff" stroke="{ink}" stroke-width="3"/><line x1="60" y1="30" x2="60" y2="140" stroke="{ink}" stroke-width="2"/><line x1="20" y1="85" x2="100" y2="85" stroke="{ink}" stroke-width="2"/>' + \
            "".join(f'<line x1="105" y1="{60+i*18}" x2="165" y2="{80+i*14}" stroke="{acc}" stroke-width="3" stroke-dasharray="6 6"/>' for i in range(4)) + prod(200, 150) + phone(275, 140)
    if kind == "bg":
        return base + f'<rect x="110" y="30" width="180" height="160" fill="#fff"/><path d="M110 150 Q200 140 290 150 L290 190 L110 190Z" fill="#f4f1ea"/>' + prod(200, 150) + \
            f'<g opacity=".5"><rect x="20" y="60" width="60" height="40" fill="{ink}" opacity=".25"/><circle cx="50" cy="150" r="22" fill="{acc}" opacity=".35"/></g><line x1="15" y1="40" x2="90" y2="190" stroke="{acc}" stroke-width="5"/>'
    if kind == "angle":
        return base + f'<line x1="20" y1="180" x2="300" y2="180" stroke="{ink}" stroke-width="2"/>' + prod(90, 150) + phone(240, 140) + \
            f'<line x1="200" y1="128" x2="112" y2="128" stroke="{acc}" stroke-width="3" stroke-dasharray="6 5"/><text x="160" y="118" font-size="14" text-anchor="middle" fill="{ink}" font-family="sans-serif">90°</text>'
    if kind == "frame":
        return base + f'<rect x="80" y="20" width="160" height="180" rx="10" fill="none" stroke="{ink}" stroke-width="4"/>' + prod(160, 115, 1.9) + \
            "".join(f'<path d="{d}" stroke="{acc}" stroke-width="4" fill="none"/>' for d in ["M95 50 V35 H110","M225 50 V35 H210","M95 170 V185 H110","M225 170 V185 H210"])
    if kind == "clean":
        return base + phone(110, 110) + f'<circle cx="110" cy="80" r="14" fill="none" stroke="{acc}" stroke-width="3"/>' + \
            f'<path d="M150 70 q30 -20 50 10" stroke="{ink}" stroke-width="3" fill="none"/>' + prod(240, 130) + \
            "".join(f'<path d="M{x} {y} l6 -10 l6 10 l-6 10z" fill="{acc}"/>' for x, y in [(268, 80), (205, 92), (275, 150)])
    if kind == "sides":
        return base + prod(60, 120, .9) + prod(130, 120, .9) + f'<g transform="translate(200 120) scale(.9)"><rect x="-18" y="-30" width="36" height="60" rx="6" fill="#a88b50"/></g>' + \
            f'<circle cx="270" cy="115" r="32" fill="#fff" stroke="{acc}" stroke-width="3"/><rect x="254" y="104" width="32" height="20" fill="#b89b5e"/><rect x="258" y="109" width="24" height="9" fill="{paper}"/>'
    if kind == "file":
        return base + f'<rect x="40" y="40" width="110" height="140" rx="8" fill="#fff" stroke="{ink}" stroke-width="3"/><path d="M120 40 v28 h30" fill="none" stroke="{ink}" stroke-width="3"/><text x="95" y="130" font-size="22" text-anchor="middle" fill="{ink}" font-family="sans-serif" font-weight="700">JPG</text>' + \
            f'<path d="M170 110 h60" stroke="{acc}" stroke-width="4" marker-end="url(#a)"/><defs><marker id="a" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{acc}"/></marker></defs>' + \
            f'<circle cx="270" cy="110" r="34" fill="#1f8f4e"/><path d="M256 110 l10 10 l18 -20" stroke="#fff" stroke-width="5" fill="none"/>'
    return base

GUIDE = [
 ("light","صوّر جنب شباك","Shoot next to a window","ضوء النهار الجانبي هو أحسن إضاءة ببلاش. اقفل الفلاش وأنوار السقف عشان الألوان متتلخبطش.","Side daylight is the best free light. Turn off the flash and ceiling lights so colours stay true."),
 ("bg","خلفية سادة ونضيفة","A plain, clean background","ورقة كرتون بيضا أو حيطة سادة أو ملاية من غير نقشة. شيل أي حاجة تانية من الكادر.","White card, a plain wall or a pattern-free sheet. Remove everything else from the frame."),
 ("angle","الموبايل في مستوى المنتج","Phone at product height","صوّر من قدام والموبايل في نفس ارتفاع المنتج، مش من فوق ولا من تحت، عشان الشكل ميتشوّهش.","Shoot front-on with the phone at the product's height, not from above or below, so the shape isn't distorted."),
 ("frame","المنتج يملا الكادر","Fill the frame","قرّب لحد ما المنتج ياخد معظم الصورة، وسيب مسافة صغيرة حواليه. متستخدمش الزووم، قرّب بإيدك.","Move closer until the product fills most of the shot with a little space around it. Don't zoom; move your hand."),
 ("clean","امسح العدسة والمنتج","Wipe the lens and the product","مسحة واحدة للعدسة بتفرق جدًا في الوضوح. وشيل التراب والبصمات من المنتج.","One wipe of the lens makes a big difference to sharpness. Clean dust and fingerprints off the product."),
 ("sides","صوّر كل الجوانب","Shoot every side","من قدام، ومن ورا، ومن الجنب، وصورة قريبة للّيبل أو أي تفصيلة مهمة.","Front, back, side, and a close-up of the label or any key detail."),
 ("file","ابعتها كملف على واتساب","Send it as a file on WhatsApp","ابعت الصورة «مستند» مش «صورة»، عشان واتساب ميضغطهاش وتوصلنا بجودتها الكاملة.","Send the photo as a Document, not a Photo, so WhatsApp doesn't compress it."),
]

def guide(lang):
    tips = "".join(f'<article class="tip reveal"><svg viewBox="0 0 320 220" role="img" aria-label="{T(lang,ta,te)}">{guide_svg(k)}</svg><p class="tip-n">{T(lang,"نصيحة","Tip")} {i+1}</p><h3>{T(lang,ta,te)}</h3><p>{T(lang,da,de)}</p></article>' for i, (k, ta, te, da, de) in enumerate(GUIDE))
    title = T(lang, "إزاي تصوّر منتجك بالموبايل — ٧ نصايح | كادر استوديو", "How to photograph your product with a phone — 7 tips | Kadr Studio")
    desc = T(lang, "دليل بسيط لتصوير المنتجات بالموبايل: الإضاءة والخلفية والزاوية وإرسال الصورة بجودة كاملة.", "A simple guide to phone product photography: light, background, angle and sending at full quality.")
    msg = SAMPLE_MSG[lang]
    return head(lang, title, desc, "photo-guide.html") + nav(lang, "photo-guide.html") + f"""
<section class="page-hero"><div class="wrap"><p class="kicker">{T(lang,'دليل مجاني','Free guide')}</p><h1 class="reveal">{T(lang,'صوّر منتجك بالموبايل<br>صح من أول مرة.','Shoot your product<br>right the first time.')}</h1><p class="lede reveal">{T(lang,'٧ نصايح بسيطة من غير أي معدات. الصورة الكويسة من الأول بتخلي النتيجة النهائية أحسن، سواء صورتها لنفسك أو بعتهالنا.','7 simple tips with no gear. A good starting photo makes the final result better, whether you use it yourself or send it to us.')}</p></div></section>
<section class="wrap tips">{tips}</section>
<section class="fs-final wrap"><h2 class="reveal">{T(lang,'صوّرت؟ ابعتهالنا.','Done? Send it over.')}</h2><p class="lede reveal" style="margin-inline:auto">{T(lang,'ونرجعهالك صورة احترافية خلال ٤٨ ساعة، مجانًا.','We send back a professional shot within 48 hours, free.')}</p>
<a class="btn solid js-wa reveal" data-msg="{msg}" href="#contact">{T(lang,'ابعت صورتك على واتساب','Send your photo on WhatsApp')}</a></section>
""" + foot(lang)

# ---------- order builder ----------
def order(lang):
    p = "" if lang == "ar" else "../"
    types = [("clothes","ملابس","Clothing"),("beauty","عطور وتجميل","Perfume & beauty"),("food","أكل ومشروبات","Food & drinks"),("acc","إكسسوارات وهاندميد","Accessories & handmade"),("other","حاجة تانية","Something else")]
    styles = [("studio","استوديو","Studio","خلفية سادة وإضاءة استوديو، للمتجر والكتالوج.","Plain background, studio light, for store and catalogue.","dune-set.webp"),
              ("life","لايف ستايل","Lifestyle","المنتج في مكان حقيقي بيحكي قصة، للسوشيال والإعلانات.","The product in a real setting that tells a story, for social and ads.","nafha-hero.webp"),
              ("model","على موديل","On model","القطعة متلبسة على موديل، للملابس والإكسسوارات.","The piece worn by a model, for clothing and accessories.","drape-look02.webp")]
    t_html = "".join(f'<label class="chip"><input type="radio" name="type" value="{T(lang,a,b)}" data-k="{k}"{" checked" if i==0 else ""}><span>{T(lang,a,b)}</span></label>' for i, (k, a, b) in enumerate(types))
    s_html = "".join(f'<label class="style-card" data-style="{k}"><input type="checkbox" name="style" value="{T(lang,a,b)}"{" checked" if k=="studio" else ""}><img src="{p}assets/img/{img}" alt="" loading="lazy"><b>{T(lang,a,b)}</b><span>{T(lang,da,de)}</span></label>' for k, a, b, da, de, img in styles)
    q_html = "".join(f'<label class="chip"><input type="radio" name="qty" value="{k["n"]}" data-egp="{k["egp"]}" data-usd="{k["usd"]}"{" checked" if k.get("pick") else ""}><span>{ar_num(k["n"]) if lang=="ar" else k["n"]} {T(lang,"صور","photos")}</span></label>' for k in PACKAGES)
    u_opts = [("بوست ٤:٥","4:5 post"),("ستوري وريلز ٩:١٦","9:16 story & reel"),("متجر مربع ١:١","1:1 store")]
    u_html = "".join(f'<label class="chip"><input type="checkbox" name="use" value="{T(lang,a,b)}"{" checked" if i==0 else ""}><span>{T(lang,a,b)}</span></label>' for i, (a, b) in enumerate(u_opts))
    title = T(lang, "اطلب صور منتجاتك — كادر استوديو", "Order your product photos — Kadr Studio")
    desc = T(lang, "اختار نوع المنتج والستايل والعدد، وشوف السعر، وابعت طلبك مرتب على واتساب في ضغطة.", "Pick your product type, style and quantity, see the price, and send a tidy order on WhatsApp in one tap.")
    return head(lang, title, desc, "order.html") + nav(lang, "order.html") + f"""
<section class="page-hero"><div class="wrap"><p class="kicker">{T(lang,'اطلب في دقيقة','Order in a minute')}</p><h1 class="reveal">{T(lang,'جهّز طلب صورك.','Build your photo order.')}</h1><p class="lede reveal">{T(lang,'اختار اللي محتاجه، وشوف السعر قبل ما تكلمنا، وابعت الطلب مرتب على واتساب.','Choose what you need, see the price before you message us, and send a tidy order on WhatsApp.')}</p></div></section>
<section class="wrap order-wrap"><form id="order" class="order">
  <div class="ostep reveal"><h3><span>١</span>{T(lang,'نوع المنتج','Product type')}</h3><div class="chips">{t_html}</div></div>
  <div class="ostep reveal"><h3><span>٢</span>{T(lang,'الستايل (تقدر تختار أكتر من واحد)','Style (pick one or more)')}</h3><div class="styles">{s_html}</div><p class="note" id="modelNote" hidden>{T(lang,'«على موديل» متاح للملابس والإكسسوارات بس.','“On model” is for clothing and accessories only.')}</p></div>
  <div class="ostep reveal"><h3><span>٣</span>{T(lang,'عدد الصور','Number of photos')}</h3><div class="chips">{q_html}</div></div>
  <div class="ostep reveal"><h3><span>٤</span>{T(lang,'المقاسات اللي محتاجها','Sizes you need')}</h3><div class="chips">{u_html}</div></div>
  <div class="ostep reveal"><h3><span>٥</span>{T(lang,'ملاحظات (اختياري)','Notes (optional)')}</h3><textarea name="notes" rows="3" placeholder="{T(lang,'مثلًا: اسم البراند، ألوان معينة، مرجع عاجبك…','e.g. brand name, colours, a reference you like…')}"></textarea></div>
</form>
<aside class="order-out reveal"><p>{T(lang,'السعر','Price')}</p><output id="orderTotal">—</output><small id="orderPer"></small><ul id="orderSum"></ul>
<a class="btn solid light" id="orderSend" href="#">{T(lang,'ابعت الطلب على واتساب','Send order on WhatsApp')}</a>
<small>{T(lang,'مش متأكد؟ ابدأ بصورة مجانية الأول.','Not sure? Start with a free photo.')} <a href="free-sample.html">{T(lang,'العرض','The offer')}</a></small></aside></section>
""" + foot(lang)

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
    <figure><img src="{p}assets/img/drape-before.webp" alt="{T(lang,'قبل: صور موبايل للقطع على الشماعة','Before: phone photos of the pieces on hangers')}"><figcaption>{T(lang,'قبل','Before')}</figcaption></figure>
    <span class="ba-arr" aria-hidden="true">{T(lang,'←','→')}</span>
    <figure><img src="{p}assets/img/drape-look02.webp" alt="{T(lang,'بعد: على موديل بإضاءة استوديو','After: on a model in studio light')}"><figcaption class="after">{T(lang,'بعد','After')}</figcaption></figure>
    <p class="ba-note">{T(lang,'نفس القطعة بالظبط، من غير سيشن تصوير — من شغلنا لبراند Drapé Atelier.','The exact same piece, with no photoshoot — our work for Drapé Atelier.')}</p>
  </div>
</section>
<section class="process wrap"><h2 class="reveal">{T(lang,'٣ خطوات بس','Just 3 steps')}</h2><ol class="steps fs-steps">{st}</ol>
<p class="reveal fs-help">{T(lang,'محتاج تعرف تصوّر صح؟','Want to shoot it right?')} <a href="photo-guide.html">{T(lang,'شوف دليل التصوير بالموبايل','See the phone photo guide')}</a> · {T(lang,'جاهز تطلب؟','Ready to order?')} <a href="order.html">{T(lang,'جهّز طلبك','Build your order')}</a></p></section>
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
    pages = ["", "free-sample.html", "order.html", "photo-guide.html", "audit.html", "creative.html", "growth.html", "tech.html"] + [f"for-{x['key']}.html" for x in SECTORS]
    urls = ""
    for pg in pages:
        for pre in ("", "en/"):
            urls += f"<url><loc>{SITE}/{pre}{pg}</loc></url>\n"
    urls += f"<url><loc>{SITE}/demos/lumaa/</loc></url>\n<url><loc>{SITE}/demos/darb-app/</loc></url>\n"
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

PAGES = {"index.html": home, "free-sample.html": sample, "creative.html": creative, "growth.html": growth, "tech.html": tech,
         "audit.html": audit, "photo-guide.html": guide, "order.html": order}
for _sc in SECTORS: PAGES[f"for-{_sc['key']}.html"] = sector_page(_sc)
os.makedirs("en", exist_ok=True)
for name, fn in PAGES.items():
    open(name, "w").write(fn("ar"))
    open(os.path.join("en", name), "w").write(fn("en"))
sitemap()
print("built", len(PAGES) * 2, "pages + sitemap")
