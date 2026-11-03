#!/usr/bin/env python3
"""Generate the bilingual home, privacy, and support pages and the sitemap. No runtime framework or dependencies."""
import json
import hashlib
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'scripts/content.json').read_text())
BASE = 'https://fortranmentis.github.io/pocket_weather_station_hp/'
REPO = 'https://github.com/fortranmentis/pocket_weather_station_hp'
STYLE_VERSION = hashlib.sha256((ROOT / 'assets/style.css').read_bytes()).hexdigest()[:12]
SCRIPT_VERSION = hashlib.sha256((ROOT / 'assets/app.js').read_bytes()).hexdigest()[:12]
PAGES = ('', 'privacy/', 'support/')

def e(value):
    return escape(str(value), quote=True)

def lines(value):
    return e(value).replace('\n', '<br>')

def arrow(direction='right'):
    path = 'm9 5 7 7-7 7' if direction == 'right' else 'm15 5-7 7 7 7'
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{path}"/></svg>'

def path_of(lang, page=''):
    """Site-root-relative directory of a page, such as 'ko/privacy/'."""
    return ('ko/' if lang == 'ko' else '') + page

def head(lang, page, title, description, prefix):
    c = DATA[lang]
    url = BASE + path_of(lang, page)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{e(title)}</title><meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#f8f9f6"><meta name="color-scheme" content="light">
  <link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{BASE}{path_of('en', page)}"><link rel="alternate" hreflang="ko" href="{BASE}{path_of('ko', page)}"><link rel="alternate" hreflang="x-default" href="{BASE}{path_of('en', page)}">
  <meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/social-preview.jpg"><meta property="og:image:alt" content="{e(c['socialAlt'])}"><meta property="og:locale" content="{'ko_KR' if lang=='ko' else 'en_US'}"><meta property="og:locale:alternate" content="{'en_US' if lang=='ko' else 'ko_KR'}"><meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="{prefix}assets/app-icon.png"><link rel="apple-touch-icon" href="{prefix}assets/app-icon.png"><link rel="stylesheet" href="{prefix}assets/style.css?v={STYLE_VERSION}">
  <script src="{prefix}assets/app.js?v={SCRIPT_VERSION}" defer></script>
</head>
<body id="top" data-asset-prefix="{prefix}">
  <a class="skip-link" href="#main">{e(c['skip'])}</a>'''

def header(lang, page, prefix):
    c = DATA[lang]
    home = '' if page == '' else prefix + path_of(lang)
    en_link, ko_link = prefix + path_of('en', page), prefix + path_of('ko', page)
    return f'''
  <header class="site-header"><div class="nav-inner">
    <a class="brand" href="{home or '#top'}"><img src="{prefix}assets/app-icon.png" width="30" height="30" alt=""><span>{e(c['name'])}</span></a>
    <nav id="main-nav" aria-label="{'주요 메뉴' if lang=='ko' else 'Main navigation'}"><a href="{home}#overview">{e(c['nav'][0])}</a><a href="{home}#experience">{e(c['nav'][1])}</a><a href="{home}#technology">{e(c['nav'][2])}</a></nav>
    <div class="nav-actions"><div class="languages" aria-label="{'언어 선택' if lang=='ko' else 'Language'}"><a href="{en_link}" lang="en" hreflang="en" {'aria-current="page"' if lang=='en' else ''}>EN</a><a href="{ko_link}" lang="ko" hreflang="ko" {'aria-current="page"' if lang=='ko' else ''}>한국어</a></div><button type="button" class="menu-toggle" aria-controls="main-nav" aria-expanded="false" aria-label="{'메뉴 열기' if lang=='ko' else 'Toggle menu'}"><span></span><span></span></button></div>
  </div></header>'''

def footer(lang, page, prefix):
    c = DATA[lang]
    home = '' if page == '' else prefix + path_of(lang)
    en_link, ko_link = prefix + path_of('en', page), prefix + path_of('ko', page)
    return f'''
  <footer class="site-footer"><div class="section-width"><div class="footer-top"><a class="brand" href="{home or '#top'}"><img src="{prefix}assets/app-icon.png" width="25" height="25" alt=""><span>{e(c['name'])}</span></a><div><a href="{prefix}{path_of(lang, 'privacy/')}">{e(c['privacyPolicy'])}</a><a href="{prefix}{path_of(lang, 'support/')}">{e(c['support'])}</a><a href="{REPO}">{e(c['sourceLink'])}</a><a href="#top">{e(c['backTop'])} ↑</a></div></div><p>{e(c['footerCaution'])}</p><p>{e(c['footerNote'])}</p><div class="footer-bottom"><span>Pocket Weather Station · 2026</span><div><a href="{en_link}" lang="en" hreflang="en">English</a><span aria-hidden="true">/</span><a href="{ko_link}" lang="ko" hreflang="ko">한국어</a></div></div></div></footer>'''

def write(lang, page, html):
    target = ROOT / path_of(lang, page) / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html)
    print(f'Generated {target.relative_to(ROOT)}')

def build(lang):
    c = DATA[lang]
    prefix = '../' if lang == 'ko' else './'
    screens = {s['id']: s for s in DATA['screens']}

    def img(sid, priority=False, cls=''):
        title = screens[sid][lang]
        return f'<img class="{cls}" src="{prefix}assets/screenshots/{sid}-600.jpg" srcset="{prefix}assets/screenshots/{sid}-600.jpg 600w, {prefix}assets/screenshots/{sid}.jpg 1206w" sizes="(max-width: 600px) 70vw, 340px" width="1206" height="2622" alt="{e(title)}" {"fetchpriority=high" if priority else "loading=lazy"} decoding="async">'

    def phone(sid, cls='', priority=False):
        return f'<div class="phone {cls}">{img(sid, priority)}<span class="island" aria-hidden="true"></span></div>'

    def zoom(sid, label, cls='text-link'):
        return f'<button class="{cls}" type="button" data-screen="{sid}" aria-haspopup="dialog">{e(label)}{arrow()}</button>'

    intro = ''.join(f'<div class="intro-item"><span class="index">{n}</span><h2>{e(t)}</h2><p>{e(b)}</p></div>' for n,t,b in c['intro'])
    tabs = ''.join(f'<button role="tab" id="tab-{x["id"]}" aria-controls="panel-{x["id"]}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}">{e(x["label"])}</button>' for i,x in enumerate(c['experiences']))
    panels = ''
    for i,x in enumerate(c['experiences']):
        points = ''.join(f'<li><h4>{e(t)}</h4><p>{e(b)}</p></li>' for t,b in x['points'])
        panels += f'''<div class="experience-panel" id="panel-{x['id']}" role="tabpanel" aria-labelledby="tab-{x['id']}" tabindex="0" {"hidden" if i else ""}>
          <div class="experience-copy"><p class="eyebrow">{e(x['tag'])}</p><h3>{lines(x['title'])}</h3><p class="body-large">{e(x['body'])}</p><ul class="feature-list">{points}</ul>{zoom(x['linkImage'],x['link'])}</div>
          <div class="experience-visual {x['id']}"><span class="orbit orbit-one" aria-hidden="true"></span><span class="orbit orbit-two" aria-hidden="true"></span>{phone(x['image'])}</div>
        </div>'''
    flow_points = ''.join(f'<li><span class="index">0{i+1}</span><div><h3>{e(t)}</h3><p>{e(b)}</p></div></li>' for i,(t,b) in enumerate(c['flowPoints']))
    ecosystem = ''.join(f'''<article class="ecosystem-card"><div class="ecosystem-copy"><p class="eyebrow">{e(x['tag'])}</p><h3>{lines(x['title'])}</h3><p>{e(x['body'])}</p></div><button class="screen-button" data-screen="{x['image']}" aria-haspopup="dialog" aria-label="{e(c['openImage'])}: {e(screens[x['image']][lang])}">{phone(x['image'])}<span class="zoom-plus" aria-hidden="true">+</span></button></article>''' for x in c['ecosystemCards'])
    ingredients = ''.join(f'<article class="ingredient ingredient-{i}"><p class="weight">{n}<span>%</span></p><h3>{e(t)}</h3><p>{e(b)}</p></article>' for i,(n,t,b) in enumerate(c['ingredients']))
    filters = ''.join(f'<button type="button" data-filter="{i}" aria-pressed="{str(i==0).lower()}">{e(x)}</button>' for i,x in enumerate(c['filters']))
    gallery = ''.join(f'''<article class="gallery-card" data-group="{s['group']}"><button class="gallery-image" type="button" data-screen="{s['id']}" aria-haspopup="dialog" aria-label="{e(c['openImage'])}: {e(s[lang])}">{img(s['id'])}<span class="zoom-plus" aria-hidden="true">+</span></button><span class="screen-index">{i+1:02d} / 14</span><h3>{e(s[lang])}</h3><p>{e(s[lang+'Body'])}</p></article>''' for i,s in enumerate(DATA['screens']))
    privacy = ''.join(f'<article><span class="privacy-symbol" aria-hidden="true">{symbol}</span><h3>{e(t)}</h3><p>{e(b)}</p></article>' for symbol,(t,b) in zip(['◉','⌁','⊕'],c['privacyCards']))
    faqs = ''.join(f'<details><summary>{e(q)}<span aria-hidden="true">+</span></summary><p>{e(a)}</p></details>' for q,a in c['faqs'])
    catalog = json.dumps([{'id':s['id'], 'title':s[lang], 'body':s[lang+'Body']} for s in DATA['screens']],ensure_ascii=False).replace('<','\\u003c')
    html = head(lang, '', c['title'], c['description'], prefix) + header(lang, '', prefix) + f'''
  <main id="main">
    <section class="hero" id="overview" aria-labelledby="hero-title">
      <div class="hero-copy"><p class="eyebrow">{e(c['eyebrow'])}</p><h1 id="hero-title">{lines(c['hero'])}</h1><p class="hero-description">{e(c['heroBody'])}</p><p class="release-badge"><span aria-hidden="true"></span>{e(c['releaseLabel'])}</p><div class="hero-actions"><a class="button" href="#experience">{e(c['heroLink'])}{arrow()}</a><a class="text-link" href="#technology">{e(c['howLink'])}{arrow()}</a></div><p class="platforms"><span class="platform-dot" aria-hidden="true"></span>{e(c['platforms'])}</p></div>
      <div class="hero-stage"><svg class="atmosphere" viewBox="0 0 1440 640" fill="none" aria-hidden="true"><path d="M-100 470C120 470 180 140 410 220S770 540 1040 320 1330 70 1540 180"/><path d="M-100 500C120 500 180 170 410 250S770 570 1040 350 1330 100 1540 210"/><path d="M-100 530C120 530 180 200 410 280S770 600 1040 380 1330 130 1540 240"/></svg><div class="hero-phones">{phone('03-chart-lcd','hero-phone-left')}{phone('01-home','hero-phone-center',True)}{phone('04-chart-forecast','hero-phone-right')}</div></div>
      <p class="image-caption">{e(c['heroCaption'])}</p>
    </section>
    <div class="intro section-width">{intro}</div>
    <section class="experience section-pad" id="experience" aria-labelledby="experience-title"><div class="section-width"><div class="section-heading"><p class="eyebrow">{e(c['experienceEyebrow'])}</p><h2 id="experience-title">{lines(c['experienceTitle'])}</h2><p>{e(c['experienceBody'])}</p></div><div class="experience-switch"><div class="tabs" role="tablist" aria-label="{e(c['tabsLabel'])}">{tabs}</div>{panels}</div></div></section>
    <section class="lcd-section" aria-labelledby="lcd-title"><div class="lcd-inner section-width"><div class="lcd-copy"><p class="eyebrow">{e(c['lcdEyebrow'])}</p><h2 id="lcd-title">{lines(c['lcdTitle'])}</h2><p class="body-large">{e(c['lcdBody'])}</p><ul class="lcd-features">{''.join(f'<li>{e(x)}</li>' for x in c['lcdFeatures'])}</ul>{zoom('03-chart-lcd',c['lcdLink'])}</div><div class="lcd-visual">{phone('12-station-display')}<span class="lcd-orbit" aria-hidden="true"></span></div></div><p class="lcd-note section-width">{e(c['lcdNote'])}</p></section>
    <section class="flow-section section-pad" aria-labelledby="flow-title"><div class="flow-inner section-width"><div class="flow-visual"><span class="map-orbit" aria-hidden="true"></span>{phone('06-pressure-flow-map')}</div><div class="flow-copy"><p class="eyebrow">{e(c['flowEyebrow'])}</p><h2 id="flow-title">{lines(c['flowTitle'])}</h2><p class="body-large">{e(c['flowBody'])}</p><ol class="flow-points">{flow_points}</ol>{zoom('06-pressure-flow-map',c['flowLink'])}</div></div></section>
    <section class="ecosystem section-pad" aria-labelledby="ecosystem-title"><div class="section-width"><div class="section-heading"><p class="eyebrow">{e(c['ecosystemEyebrow'])}</p><h2 id="ecosystem-title">{lines(c['ecosystemTitle'])}</h2><p>{e(c['ecosystemBody'])}</p></div><div class="ecosystem-grid">{ecosystem}</div></div></section>
    <section class="technology section-pad" id="technology" aria-labelledby="tech-title"><div class="section-width"><div class="section-heading centered"><p class="eyebrow">{e(c['techEyebrow'])}</p><h2 id="tech-title">{lines(c['techTitle'])}</h2><p>{e(c['techBody'])}</p></div><div class="blend-bar" aria-hidden="true"><span></span><span></span><span></span></div><div class="ingredients">{ingredients}</div><p class="footnote weight-note">{e(c['weightNote'])}</p><div class="comparison"><div class="comparison-copy"><p class="eyebrow">{e(c['compareTag'])}</p><h3>{lines(c['compareTitle'])}</h3><p>{e(c['compareBody'])}</p>{zoom('09-engine-comparison',c['compareLink'])}<p class="footnote">{e(c['compareNote'])}</p></div><div class="comparison-visual">{phone('09-engine-comparison')}{phone('10-engine-charts')}</div></div></div></section>
    <section class="gallery section-pad" id="screens" aria-labelledby="gallery-title"><div class="section-width"><div class="gallery-heading"><div><p class="eyebrow">{e(c['galleryEyebrow'])}</p><h2 id="gallery-title">{e(c['galleryTitle'])}</h2><p class="body-large">{e(c['galleryBody'])}</p></div><div class="gallery-arrows"><button type="button" data-scroll="-1" aria-label="{e(c['previous'])}">{arrow('left')}</button><button type="button" data-scroll="1" aria-label="{e(c['next'])}">{arrow()}</button></div></div><div class="gallery-controls"><div class="filters" role="group" aria-label="{e(c['filterLabel'])}">{filters}</div><span class="gallery-count" aria-live="polite" data-count-template="{e(c['screenCount'])}">{e(c['screenCount'].replace('{n}', '14'))}</span></div></div><div class="gallery-track" aria-label="{e(c['galleryLabel'])}" tabindex="0">{gallery}</div><p class="footnote section-width">{e(c['galleryNote'])}</p></section>
    <section class="privacy section-pad" id="privacy" aria-labelledby="privacy-title"><div class="section-width"><div class="section-heading"><p class="eyebrow">{e(c['privacyEyebrow'])}</p><h2 id="privacy-title">{lines(c['privacyTitle'])}</h2><p>{e(c['privacyBody'])}</p></div><div class="privacy-grid">{privacy}</div><a class="text-link" href="{prefix}{path_of(lang, 'privacy/')}">{e(c['privacyLink'])}{arrow()}</a><div class="faq"><h3>{e(c['faqTitle'])}</h3><div>{faqs}</div></div></div></section>
    <section class="closing section-pad" aria-labelledby="closing-title"><img src="{prefix}assets/app-icon.png" width="76" height="76" alt="" loading="lazy"><h2 id="closing-title">{lines(c['closing'])}</h2><p>{e(c['closingBody'])}</p><p class="release-announcement"><strong>{e(c['releaseLabel'])}</strong><span>{e(c['releaseBody'])}</span></p></section>
  </main>''' + footer(lang, '', prefix) + f'''
  <dialog class="screenshot-dialog" aria-labelledby="dialog-title" aria-describedby="dialog-description"><div class="dialog-top"><div><p id="dialog-position"></p><h2 id="dialog-title"></h2></div><div class="dialog-tools"><button type="button" class="dialog-zoom" aria-pressed="false" aria-label="{'스크린샷 더 크게 보기' if lang=='ko' else 'Zoom screenshot'}">⊕</button><button type="button" class="dialog-close" aria-label="{e(c['close'])}">×</button></div></div><div class="dialog-stage"><button type="button" class="dialog-prev" aria-label="{e(c['previousImage'])}">{arrow('left')}</button><img class="dialog-image" alt="" width="1206" height="2622"><button type="button" class="dialog-next" aria-label="{e(c['nextImage'])}">{arrow()}</button></div><p id="dialog-description"></p></dialog>
  <script type="application/json" id="screenshot-catalog">{catalog}</script>
</body></html>
'''
    write(lang, '', html)

def build_document(lang, page):
    c = DATA[lang]
    doc = c['privacyPage' if page == 'privacy/' else 'supportPage']
    prefix = '../../' if lang == 'ko' else '../'
    other = 'support/' if page == 'privacy/' else 'privacy/'
    updated = f'<p class="doc-updated">{e(doc["updated"])}</p>' if 'updated' in doc else ''
    contact = ''
    if 'contactTitle' in doc:
        contact = f'<section class="doc-contact"><h2>{e(doc["contactTitle"])}</h2><p>{e(doc["contactBody"])}</p><a class="button" href="{REPO}/issues/new">{e(doc["contactLink"])}{arrow()}</a></section>'
    sections = ''.join(f'<section><h2>{e(h)}</h2>{"".join(f"<p>{e(x)}</p>" for x in body)}</section>' for h, body in doc['sections'])
    links = f'<nav class="doc-links" aria-label="{e(c["name"])}"><a class="text-link" href="{prefix}{path_of(lang)}">{e(c["home"])}{arrow()}</a><a class="text-link" href="{prefix}{path_of(lang, other)}">{e(c["support" if other == "support/" else "privacyPolicy"])}{arrow()}</a></nav>'
    html = head(lang, page, f'{doc["title"]} — {c["name"]}', doc['description'], prefix) + header(lang, page, prefix) + f'''
  <main id="main" class="doc section-width"><p class="eyebrow">{e(c['name'])}</p><h1>{e(doc['title'])}</h1>{updated}<p class="doc-intro">{e(doc['intro'])}</p>{contact}{sections}{links}</main>''' + footer(lang, page, prefix) + '\n</body></html>\n'
    write(lang, page, html)

def build_sitemap():
    urls = ''.join(f'\n  <url><loc>{BASE}{path_of(lang, page)}</loc></url>' for page in PAGES for lang in ('en', 'ko'))
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}\n</urlset>\n')
    print('Generated sitemap.xml')

for language in ('en','ko'):
    build(language)
    build_document(language, 'privacy/')
    build_document(language, 'support/')
build_sitemap()
