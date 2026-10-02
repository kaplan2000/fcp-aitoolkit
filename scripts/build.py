#!/usr/bin/env python3
"""Build the dependency-free, GitHub Pages-compatible FCP AI Toolkit site."""
import json
import hashlib
import re
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://www.fcp-aitoolkit.com'
STORE = 'https://apps.apple.com/app/id6775619373'
TODAY = '2026-10-02'
VERSION = '1.1.1'
RELEASE_POST = '/blog/fcp-ai-toolkit-1-1-1/'
SOCIAL = [('YouTube', 'https://www.youtube.com/@FCPAIToolkit'), ('Instagram', 'https://www.instagram.com/fcpaitoolkit/'), ('TikTok', 'https://www.tiktok.com/@fcpaitoolkit')]
HOME = json.loads((ROOT / 'content/home.json').read_text())
POSTS = sorted(json.loads((ROOT / 'content/posts.json').read_text()), key=lambda p: p['date'], reverse=True)

def write(path, text):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text.rstrip() + '\n')

def asset(path):
    """Invalidate an earlier host's browser cache when an asset changes."""
    digest = hashlib.sha256((ROOT / path.lstrip('/')).read_bytes()).hexdigest()[:12]
    return path + '?v=' + digest

def human_date(date):
    return datetime.fromisoformat(date).strftime('%B %d, %Y').replace(' 0', ' ')

def arrow():
    return '<span aria-hidden="true">↗</span>'

def header(active=''):
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="shell nav-wrap">
<a class="brand" href="/" aria-label="FCP AI Toolkit home"><img src="/images/brand/logo-purple-256.png" width="38" height="38" alt=""><span>FCP AI <b>Toolkit</b></span></a>
<button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" hidden>Menu <span aria-hidden="true">+</span></button>
<nav id="site-nav" aria-label="Main navigation"><a href="/#workflow">Workflow</a><a href="/#styles">Caption styles</a><a href="/blog/" {'aria-current="page"' if active == 'blog' else ''}>Blog <span class="nav-new">NEW</span></a><a class="nav-download" href="{STORE}">Get the app {arrow()}</a></nav>
</div></header>'''

def footer():
    links = ''.join(f'<a href="{escape(url)}">{name} {arrow()}</a>' for name, url in SOCIAL)
    return f'''<footer class="site-footer"><div class="shell"><div class="footer-top"><a class="brand" href="/"><img src="/images/brand/logo-purple-256.png" width="40" height="40" alt=""><span>FCP AI <b>Toolkit</b></span></a><p>Less busywork. More storytelling.</p><div class="social-links" aria-label="Social channels">{links}</div></div><div class="footer-bottom"><span>© 2026 FCP AI Toolkit</span><div><a href="/privacy/">Privacy</a><a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Terms</a><a href="mailto:help@fcp-aitoolkit.com">Contact</a><a href="/feed.rss">RSS</a></div><a class="soleach" href="https://soleach.com/">Powered by <strong>Soleach Digital Agency</strong> {arrow()}</a></div><p class="legal-note">An independent workflow extension. Final Cut Pro is a trademark of Apple Inc.</p></div></footer>'''

def page(title, description, path, body, active='', schema=None, article=None):
    canonical = SITE + path
    graph = [{'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'FCP AI Toolkit', 'url': SITE, 'logo': SITE + '/images/brand/logo-purple-1024.png', 'sameAs': [u for _, u in SOCIAL]}, {'@type': 'WebSite', '@id': SITE + '/#website', 'name': 'FCP AI Toolkit', 'url': SITE, 'publisher': {'@id': SITE + '/#organization'}, 'inLanguage': 'en'}]
    if schema:
        graph.extend(schema)
    jsonld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    article_meta = f'<meta property="article:published_time" content="{article["date"]}T00:00:00+03:00"><meta property="article:modified_time" content="{TODAY}T00:00:00+03:00"><link rel="alternate" type="text/markdown" href="{path}index.md" title="Markdown version">' if article else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}"><meta name="theme-color" content="#17121f"><meta name="robots" content="index, follow, max-image-preview:large"><meta name="author" content="FCP AI Toolkit">
<link rel="canonical" href="{canonical}"><link rel="icon" href="/images/brand/favicon-purple.png" type="image/png" sizes="32x32"><link rel="apple-touch-icon" href="/images/brand/apple-touch-icon-purple.png"><link rel="manifest" href="/site.webmanifest?v=purple"><link rel="alternate" type="application/rss+xml" title="FCP AI Toolkit updates" href="/feed.rss">
<meta property="og:site_name" content="FCP AI Toolkit"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/images/brand/social-card-purple.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="FCP AI Toolkit — Your words. In motion."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title, quote=True)}"><meta name="twitter:description" content="{escape(description, quote=True)}"><meta name="twitter:image" content="{SITE}/images/brand/social-card-purple.jpg"><meta name="apple-itunes-app" content="app-id=6775619373">
{article_meta}<link rel="stylesheet" href="{asset('/css/site.css')}"><script src="{asset('/js/site.js')}" defer></script><script type="application/ld+json">{jsonld}</script></head>
<body>{header(active)}{body}{footer()}</body></html>'''

CARD_ART = {
    '1.0': ('release-art', 'THE FIRST FRAME', 'Your words. In motion.'),
    '1.1': ('preview-art', 'THE NEXT CHAPTER', 'A smarter way to keep editing.'),
    '1.1.1': ('update-art', HOME['card_label'], HOME['card_bottom']),
}

def post_card(post):
    art, label, bottom = CARD_ART[post['version']]
    return f'''<a class="post-card" href="/blog/{post['slug']}/"><div class="post-art {art}"><span class="art-label">{escape(label)}</span><span class="art-version">{post['version']}<span class="art-star" aria-hidden="true">✳</span></span><span class="art-bottom">{escape(bottom)}</span></div><div class="post-meta"><span class="tag {'tag-lime' if post['version'] == VERSION else ''}">{post['label']}</span><time datetime="{post['date']}">{human_date(post['date'])}</time></div><h3>{escape(post['title'])} {arrow()}</h3><p>{escape(post['excerpt'])}</p></a>'''

TRASH_ICON = '<svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true"><path d="M3 4.5h10M6.5 4.5V3h3v1.5M4.5 4.5l.6 8.5h5.8l.6-8.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SEARCH_ICON = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><circle cx="7" cy="7" r="4.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10.5 10.5 14 14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'
# Native names, shown as-is in every language edition.
LANGUAGE_NAMES = ['Türkçe', 'English', 'Español', '日本語', 'Deutsch', 'العربية', 'हिन्दी', 'Português', '한국어', 'Français', 'Русский', 'Italiano', 'Polski', 'Tiếng Việt', 'Nederlands', 'Svenska', 'Ελληνικά', 'Українська', 'Bahasa Indonesia', 'বাংলা', '中文', 'Kiswahili']

def whats_new():
    """The 1.1.1 section: Smart Cache demo, edit/search/language cards and the two fixes.

    Every visible string lives in the HTML so the localizer can translate it;
    js/site.js only switches states and filters the sample captions."""
    h = lambda key: escape(HOME[key])
    statuses = ''.join(f'<span data-msg="{state}"{"" if state == "idle" else " hidden"}>{h("cache_status_" + state.replace("-", "_"))}</span>' for state in ('idle', 'working-full', 'done-full', 'cached', 'extended', 'working-part', 'done-part'))
    ticks = ''.join(f'<i class="cache-bar-{n}"></i>' for n in [40, 70, 55, 85, 35, 60, 90, 50, 30, 75, 65, 45, 80, 55, 35, 70, 95, 60, 40, 75, 50, 85, 45, 65])
    samples = ''.join(f'<li><span class="result-text">{escape(s["text"])}</span><span class="result-meta"><span>{escape(s["file"])}</span><span>{escape(s["tc"])}</span></span></li>' for s in HOME['search_samples'])
    languages = ''.join(f'<span>{escape(name)}</span>' for name in LANGUAGE_NAMES)
    return f'''<section class="whats-new" id="whats-new"><div class="shell"><div class="section-heading"><div><p class="eyebrow"><span class="status-dot"></span> {h("new_eyebrow")}</p><h2>{h("new_h2_line1")}<br><span class="serif">{h("new_h2_line2")}</span></h2></div><p>{h("new_intro")}</p></div>
<div class="new-grid"><article class="cache-demo" data-state="idle"><div class="demo-top"><span>{h("cache_label")}</span><span>{VERSION}</span></div><h3>{h("cache_title")}</h3><p class="demo-body">{h("cache_body")}</p>
<div class="cache-stage" aria-hidden="true"><div class="cache-ruler"><span>00:00</span><span>00:06</span><span>00:12</span><span class="ruler-ext">00:18</span></div><div class="cache-track"><div class="cache-clip"><span class="clip-name">{h("cache_clip_name")}</span><span class="clip-fill"></span></div><div class="cache-ext"><span class="clip-fill"></span><span class="ext-tag">{h("cache_new_part")}</span></div><span class="cache-playhead"></span></div><div class="cache-wave">{ticks}</div></div>
<p class="cache-status" role="status" aria-live="polite">{statuses}</p>
<div class="cache-controls"><button type="button" class="button button-lime cache-run" data-cache="run"><span class="run-first">{h("cache_btn_run")}</span><span class="run-again" hidden>{h("cache_btn_again")}</span></button><button type="button" class="cache-button" data-cache="extend" disabled>{h("cache_btn_extend")}</button><button type="button" class="cache-button cache-reset" data-cache="reset" disabled>{h("cache_btn_reset")}</button></div>
<p class="demo-label">{h("cache_note")}</p></article>
<div class="new-cards"><article class="new-card edit-card"><div class="edit-demo" aria-hidden="true"><div class="edit-times"><span>0:02.5</span><i>→</i><span>0:05.0</span><span class="edit-trash">{TRASH_ICON}</span></div><div class="edit-field"><span class="edit-wrong">{h("edit_sample_wrong")}</span><span class="edit-right">{h("edit_sample_right")}</span><span class="edit-badge">✓ {h("edit_badge")}</span></div></div><h3>{h("edit_title")}</h3><p>{h("edit_body")}</p></article>
<article class="new-card search-card"><h3>{h("search_title")}</h3><p>{h("search_body")}</p><label class="search-field">{SEARCH_ICON}<input type="search" class="caption-search" placeholder="{h("search_placeholder")}" aria-label="{h("search_placeholder")}" autocomplete="off" spellcheck="false"></label><p class="search-hint">{h("search_hint")}</p><ul class="search-results">{samples}</ul><p class="search-empty" hidden>{h("search_empty")}</p></article>
<article class="new-card lang-card"><div class="lang-head"><span class="lang-count">~100</span><span class="lang-chip"><span class="status-dot"></span> {h("lang_auto")}</span></div><div class="lang-marquee" aria-hidden="true"><div>{languages}{languages}</div></div><h3>{h("lang_title")}</h3><p>{h("lang_body")}</p></article></div></div>
<div class="fixes-row"><p class="eyebrow">{h("fixes_label")}</p><p><span>01</span> {h("fix1")}</p><p><span>02</span> {h("fix2")}</p><a class="text-link" href="{RELEASE_POST}">{h("fixes_link")} ↗</a></div></div></section>'''

def home():
    body = '''<main id="main">
<section class="hero shell"><div class="hero-copy"><a class="release-link" href="RELEASE_POST"><span class="status-dot"></span> [[h:hero_release_link]] <span aria-hidden="true">↗</span></a><h1>Your words.<br><span class="serif">In motion.</span><span class="hero-asterisk" aria-hidden="true">✳</span></h1><div class="hero-bottom"><p>Turn speech into expressive, editable captions.<br class="desktop-only"> Right inside Final Cut Pro. Right on your Mac.</p><a class="button button-lime" href="STORE">Get FCP AI Toolkit <span aria-hidden="true">↗</span></a><span class="microcopy">Free Motion templates · AI captions with a subscription</span></div></div>
<div class="hero-art" aria-label="Interactive caption style illustration"><div class="preview-top"><span><span class="status-dot"></span> THE CAPTION STUDIO</span><span>02 / 05</span></div><div class="caption-canvas" data-style="highlight"><span class="corner corner-tl"></span><span class="corner corner-tr"></span><span class="corner corner-bl"></span><span class="corner corner-br"></span><div class="canvas-orbit" aria-hidden="true"></div><div class="canvas-label">GOOD STORIES DESERVE TO BE SEEN.</div><p class="sample-caption">Make every<br><span class="caption-word">word</span> count.</p><span class="canvas-note">YOUR FOOTAGE. YOUR VOICE.</span></div><div class="preview-controls"><span class="mono">STYLE PREVIEW</span><button type="button" class="next-style">Change style <span aria-hidden="true">↗</span></button></div><div class="mini-timeline" aria-hidden="true"><div class="timeline-ruler"><span>00:00:01:00</span><span>00:00:02:00</span><span>00:00:03:00</span></div><div class="caption-track"><span>Make</span><span>every</span><span>word</span><span>count.</span></div><div class="audio-track">WAVE</div><div class="playhead"></div></div><p class="demo-label">Illustrative preview · Five Motion templates included</p></div></section>
<div class="spec-strip"><div class="shell"><span>BUILT FOR YOUR EDIT.</span><span><i aria-hidden="true">↳</i> Native Final Cut Pro extension</span><span><i aria-hidden="true">◈</i> On-device transcription</span><span><i aria-hidden="true">⌘</i> Made for Apple silicon</span><span><i aria-hidden="true">◎</i> [[h:spec_languages]]</span></div></div>
<section class="section shell" id="workflow"><div class="section-heading"><div><p class="eyebrow">01 / STAY IN YOUR FLOW</p><h2>From spoken words<br>to the <span class="serif">final frame.</span></h2></div><p>Your timeline is where the story comes together.<br>That’s where your captions should be, too.</p></div><div class="workflow-grid"><article><span class="step-num">01</span><div class="step-graphic import-graphic" aria-hidden="true"><span class="mini-project">▤<small>Your project.fcpxml</small></span><span class="import-arrow">↘</span><img src="/images/brand/logo-purple-256.png" alt="" width="68" height="68" loading="lazy"></div><h3>Drop in your project.</h3><p>Open the workflow extension in Final Cut Pro and bring in your project. Choose the dialogue you want to work with.</p></article><article><span class="step-num">02</span><div class="step-graphic transcribe-graphic" aria-hidden="true"><div class="waveform">WAVE</div><span class="transcribed-text">A good story starts here<span>│</span></span></div><h3>Let your Mac listen.</h3><p>Generate word-timed captions with local speech recognition. Your audio is processed on your Mac, without a cloud transcription service.</p></article><article><span class="step-num">03</span><div class="step-graphic arrange-graphic" aria-hidden="true"><span class="compound-label">⌑ Captions</span><div><i>Your</i><i>next</i><i>great</i><i>story.</i></div></div><h3>Make it your own.</h3><p>Pick a Motion template, tune the look and bring your captions back into a tidy compound clip in your timeline.</p></article></div></section>
WHATS_NEW
<section class="styles-section" id="styles"><div class="shell"><div class="section-heading"><div><p class="eyebrow">02 / GIVE YOUR WORDS SOME CHARACTER</p><h2>Same words.<br><span class="serif">Different energy.</span></h2></div><p>Five built-in Motion templates.<br>A style for the story you’re telling.</p></div><div class="style-selector" role="group" aria-label="Choose a caption style"><button type="button" data-caption-style="basic" aria-pressed="false">Basic</button><button type="button" data-caption-style="highlight" aria-pressed="true">Highlighted</button><button type="button" data-caption-style="background" aria-pressed="false">Highlighted + Background</button><button type="button" data-caption-style="pop" aria-pressed="false">Pop</button><button type="button" data-caption-style="beast" aria-pressed="false">Beast Pop</button></div><div class="large-preview" data-style="highlight"><span class="preview-frame-label">CAPTION STYLE STUDY / <span class="active-style-name">Highlighted</span></span><p class="sample-caption">A little <span class="caption-word">motion.</span><br>A lot of meaning.</p><span class="preview-frame-footer">FONT, COLOUR & POSITION — MAKE THEM YOURS.</span><span class="preview-index" aria-hidden="true">Aa</span></div><p class="style-note">Interactive style illustration. Fine-tune the actual Motion templates in the app and Final Cut Pro.</p></div></section>
<section class="section shell product-section"><div class="product-copy"><p class="eyebrow">03 / SMALL TOOL. THOUGHTFUL DETAILS.</p><h2>Made to feel<br><span class="serif">right at home.</span></h2><p class="lead">A native workflow extension built around the way you already edit.</p><ul class="feature-list"><li><span>01</span><div><h3>Your footage stays yours.</h3><p>Speech recognition runs locally after the model download. No uploading your edit for transcription.</p></div></li><li><span>02</span><div><h3>A timeline that stays tidy.</h3><p>Generated titles are grouped in a compound clip inside a secondary storyline.</p></div></li><li><span>03</span><div><h3>Start with free templates.</h3><p>Install and use the included Motion templates. Add an active subscription when you want automatic AI captions.</p></div></li><li><span>04</span><div><h3>[[h:feature4_title]]</h3><p>[[h:feature4_body]]</p></div></li></ul></div><figure class="product-figure"><div class="workspace-shot"><img src="/images/product/workspace-1-1-1.webp" alt="[[h:figure_alt]]" loading="lazy" width="456" height="300"></div><figcaption><span class="status-dot"></span> [[h:figure_caption]] <span>[[h:figure_tagline]]</span></figcaption></figure></section>
<section class="journal-section"><div class="shell"><div class="section-heading"><div><p class="eyebrow">FROM THE EDIT ROOM</p><h2>What’s new.<br><span class="serif">What’s next.</span></h2></div><a class="text-link" href="/blog/">Visit the blog ↗</a></div><div class="post-grid">POSTS</div></div></section>
<section class="section shell faq-section" id="faq"><div><p class="eyebrow">A FEW USEFUL ANSWERS</p><h2>Before you<br><span class="serif">press play.</span></h2><a class="text-link" href="mailto:help@fcp-aitoolkit.com">Talk to us ↗</a></div><div class="faq-list"><details><summary>What do I need to run it?<span aria-hidden="true">+</span></summary><p>Built for Apple silicon. Requires macOS 26.4 or later and Final Cut Pro. Check the current <a href="STORE">Mac App Store listing</a> for compatibility before downloading.</p></details><details><summary>What’s free, and what’s paid?<span aria-hidden="true">+</span></summary><p>The app is free to download, with Motion templates you can install and use independently in Final Cut Pro. Automatic AI caption generation requires an active monthly subscription. Current pricing and any trial eligibility are shown in the App Store.</p></details><details><summary>Does my audio leave my Mac?<span aria-hidden="true">+</span></summary><p>Transcription is processed locally. An internet connection is needed to download models and for App Store purchases or subscription checks. Read our <a href="/privacy/">privacy policy</a> for details.</p></details><details><summary>Can I change how the captions look?<span aria-hidden="true">+</span></summary><p>Yes. Choose from Basic, Highlighted, Highlighted with Background, Pop and Beast Pop, then adjust styling such as the font, colours and position.</p></details><details><summary>[[h:faq_new_q]]<span aria-hidden="true">+</span></summary><p>[[r:faq_new_a]]</p></details><details><summary>[[h:faq_why_q]]<span aria-hidden="true">+</span></summary><p>[[r:faq_why_a]]</p></details><details><summary>[[h:faq_lang_q]]<span aria-hidden="true">+</span></summary><p>[[r:faq_lang_a]]</p></details></div></section>
<section class="download-section shell" id="download"><div class="download-mark" aria-hidden="true">✳</div><p class="eyebrow">LESS CAPTIONING. MORE CREATING.</p><h2>Your next story.<br><span class="serif">With every word.</span></h2><a class="button button-dark" href="STORE">Get FCP AI Toolkit <span aria-hidden="true">↗</span></a><p>[[h:download_meta]]</p></section>
<section class="community shell"><div><p class="eyebrow">LET’S BUILD THIS TOGETHER</p><h2>[[h:community_h2_line1]] <span class="serif">[[h:community_h2_line2]]</span></h2><p>[[h:community_body]]</p></div><div class="community-links">SOCIAL</div></section>
</main>'''
    waves = ''.join(f'<i class="wave-{h}"></i>' for h in [20,35,65,42,80,53,30,92,70,45,25,60,85,50,35,75,95,55,30,70,42,88,60,33,50,79,40,20,65,45,82,50,35,74,95,64,32,55,82,40])
    body = body.replace('WHATS_NEW', whats_new()).replace('RELEASE_POST', RELEASE_POST)
    body = re.sub(r'\[\[h:(\w+)\]\]', lambda m: escape(HOME[m.group(1)]), body)
    body = re.sub(r'\[\[r:(\w+)\]\]', lambda m: HOME[m.group(1)], body)
    body = body.replace('WAVE', waves).replace('STORE', STORE).replace('POSTS', ''.join(post_card(p) for p in POSTS)).replace('SOCIAL', ''.join(f'<a href="{escape(url)}">{name} {arrow()}</a>' for name,url in SOCIAL))
    schema = [{'@type': 'SoftwareApplication', '@id': SITE + '/#app', 'name': 'FCP AI Toolkit', 'applicationCategory': 'MultimediaApplication', 'operatingSystem': 'macOS 26.4 or later', 'softwareVersion': VERSION, 'downloadUrl': STORE, 'description': 'A native Final Cut Pro workflow extension for on-device AI captions and Motion title templates. Free template features; automatic AI captions require a subscription.', 'image': SITE + '/images/brand/logo-purple-1024.png', 'datePublished': '2026-06-21', 'publisher': {'@id': SITE + '/#organization'}}]
    write('index.html', page('FCP AI Toolkit — Your words. In motion.', 'Create expressive, editable captions right inside Final Cut Pro with on-device AI. Free Motion templates. Made for Apple silicon.', '/', body, schema=schema))

def blog():
    body = '<main id="main" class="shell blog-main"><div class="blog-heading"><p class="eyebrow">THE FCP AI TOOLKIT JOURNAL</p><h1>Notes from<br><span class="serif">the edit room.</span></h1><p>New releases, work in progress, and the thinking behind the toolkit.</p><a class="text-link" href="/feed.rss">Follow the RSS feed ↗</a></div><div class="post-grid">' + ''.join(post_card(p) for p in POSTS) + '</div></main>'
    write('blog/index.html', page('Blog — FCP AI Toolkit', 'Product updates, release notes and a look at what is coming next for FCP AI Toolkit.', '/blog/', body, 'blog', [{'@type': 'Blog', 'name': 'The FCP AI Toolkit Journal', 'url': SITE + '/blog/', 'blogPost': [{'@id': SITE + '/blog/' + p['slug'] + '/#article'} for p in POSTS]}]))
    for post in POSTS:
        path = f'/blog/{post["slug"]}/'
        next_post = next(p for p in POSTS if p != post)
        body = f'''<main id="main"><article><header class="article-header shell"><a class="text-link" href="/blog/">← The edit room</a><div class="post-meta"><span class="tag {'tag-lime' if post['version'] == VERSION else ''}">{post['label']}</span><time datetime="{post['date']}">{human_date(post['date'])}</time><span>FCP AI Toolkit</span></div><h1>{escape(post['title'])}</h1><p class="article-deck">{escape(post['excerpt'])}</p></header><div class="article-layout shell"><aside class="article-aside"><span class="eyebrow">VERSION {post['version']}</span><span class="aside-version">{post['version']}</span><span>{post['label']}</span><a href="{STORE}">View on the App Store ↗</a><a href="{path}index.md">Read as Markdown ↗</a></aside><div class="prose">{post['body']}<div class="article-end"><img src="/images/brand/logo-purple-256.png" width="44" height="44" alt=""><div><strong>FCP AI Toolkit</strong><p>Powered by <a href="https://soleach.com/">Soleach Digital Agency</a></p></div></div></div></div></article><section class="related shell"><p class="eyebrow">KEEP READING</p><a href="/blog/{next_post['slug']}/">{escape(next_post['title'])} ↗</a></section></main>'''
        schema = [{'@type': 'BlogPosting', '@id': SITE + path + '#article', 'headline': post['title'], 'description': post['excerpt'], 'datePublished': post['date'] + 'T00:00:00+03:00', 'dateModified': TODAY + 'T00:00:00+03:00', 'mainEntityOfPage': SITE + path, 'image': SITE + '/images/brand/social-card-purple.jpg', 'author': {'@type': 'Organization', 'name': 'FCP AI Toolkit', 'url': SITE}, 'publisher': {'@id': SITE + '/#organization'}, 'inLanguage': 'en'}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':SITE+'/'},{'@type':'ListItem','position':2,'name':'Blog','item':SITE+'/blog/'},{'@type':'ListItem','position':3,'name':post['title'],'item':SITE+path}]}]
        write(path.strip('/') + '/index.html', page(post['title'] + ' — FCP AI Toolkit', post['excerpt'], path, body, 'blog', schema, post))
        text = post['body']
        text = re.sub(r'<h2>(.*?)</h2>', r'\n## \1\n', text)
        text = re.sub(r'<h3>(.*?)</h3>', r'\n### \1\n', text)
        text = re.sub(r'<a href="(.*?)"[^>]*>(.*?)</a>', r'[\2](\1)', text)
        text = text.replace('<li>', '\n- ').replace('</p>', '\n\n')
        text = re.sub('<[^>]+>', '', text)
        from html import unescape
        write(path.strip('/') + '/index.md', f'# {post["title"]}\n\nDate: {post["date"]}\nStatus: {post["label"]}\nCanonical: {SITE}{path}\n\n{post["excerpt"]}\n\n' + unescape(text).strip())

def privacy():
    body = '''<main id="main" class="shell legal-page"><p class="eyebrow">YOUR WORK, YOUR MAC</p><h1>Privacy <span class="serif">policy.</span></h1><p class="muted">Updated October 2, 2026</p><div class="prose"><h2>Who we are</h2><p>FCP AI Toolkit is operated by Mustafa Kaplan. This page explains how the macOS app and this website handle information. For questions, contact <a href="mailto:help@fcp-aitoolkit.com">help@fcp-aitoolkit.com</a>.</p><h2>Your media and AI processing</h2><p>The app processes your project audio and generates transcriptions locally on your Mac. Your media and transcripts are not uploaded to a cloud AI transcription service. The app needs access to the project and media files you choose to use.</p><h2>Model downloads and local files</h2><p>Speech recognition requires a model to be downloaded before use. Model downloads use an internet connection. Downloaded models and the app’s working data are stored locally. Your source media remains under your control.</p><p>PRIVACY_CACHE</p><h2>Purchases and subscriptions</h2><p>In-app purchases and subscriptions are handled by Apple through StoreKit. Apple processes payment and account information under its own privacy policy. The app checks purchase and subscription status to provide the features you have purchased. We do not receive your payment card details.</p><h2>This website</h2><p>This website is served by Cloudflare, with a backup copy on GitHub Pages. Hosting providers may process technical request information, such as IP addresses, to deliver and secure the site. This site does not embed advertising or third-party analytics scripts, and does not set analytics cookies. Links to the App Store, Soleach and our social channels take you to services with their own privacy practices.</p><p>Your appearance preference is stored only in your browser, so the site can remember light, dark or system mode. It is not sent to us. You can clear it by removing this site’s browser data.</p><h2>When you contact us</h2><p>If you email support, we receive the email address and information you choose to share. We use that information to respond to your request. Please avoid sending private footage or sensitive project information unless it is necessary for the support you are requesting.</p><h2>Contact and changes</h2><p>You can contact <a href="mailto:help@fcp-aitoolkit.com">help@fcp-aitoolkit.com</a> about your information or this policy. We will update this page when our practices change.</p></div></main>'''
    body = body.replace('PRIVACY_CACHE', escape(HOME['privacy_cache']))
    write('privacy/index.html', page('Privacy policy — FCP AI Toolkit', 'How FCP AI Toolkit handles local transcription, model downloads, subscriptions and website information.', '/privacy/', body))

def discovery():
    paths = ['/', '/blog/', '/privacy/'] + [f'/blog/{p["slug"]}/' for p in POSTS]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(f'  <url><loc>{SITE}{path}</loc><lastmod>{TODAY}</lastmod></url>' for path in paths) + '\n</urlset>')
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n\n# Human-readable product context for language models: /llms.txt\n')
    llms = f'''# FCP AI Toolkit

> A native Final Cut Pro workflow extension for on-device speech-to-text captions and editable Motion titles on Apple silicon Macs.

## Product facts
- Official website: {SITE}/
- Available version: 1.1.1, released on the Mac App Store on September 30, 2026. Version 1.0 was first released June 21, 2026. There was no public 1.1: it shipped as 1.1.1, which adds two bug fixes to the features previewed for 1.1.
- Built for Apple silicon. Requirements: macOS 26.4 or later and Final Cut Pro; consult the App Store for current hardware compatibility.
- The app is free to download. Included Motion templates can be used for free. Automatic AI caption generation requires an active monthly subscription; consult the App Store for current pricing and trial eligibility.
- Transcription runs on the Mac after downloading a speech model. Model downloads and Apple StoreKit purchases/subscription checks use the internet.
- Templates: Basic, Highlighted, Highlighted with Background, Pop, Beast Pop.
- New in 1.1.1: Smart Cache (reuses earlier transcriptions of the same media, language and model; only new parts of an extended clip are transcribed; on by default, can be turned off); caption text and start/end time editing inside the extension, saved locally, with a remove button per caption; Smart Search across locally cached captions (text, source file name, timecode; no jump to the clip); about 100 Whisper-model languages plus local Auto Detect; the extension fits smaller Final Cut Pro windows.
- Fixed in 1.1.1: overlapping duplicate captions that could lock the caption editor; caption timing for detached and connected audio.
- About 100 languages describes the Whisper model catalog; quality has not been separately tested in every language.
- Do not infer SRT export, text-to-speech, visual search, direct YouTube upload, or direct Final Cut Pro playhead control.

## Pages
- [Home]({SITE}/): Product overview, workflow, styles and FAQ.
- [Blog]({SITE}/blog/): Product updates and release notes.
- [Privacy]({SITE}/privacy/): Data handling and local processing.
- [App Store]({STORE}): Current availability, requirements and pricing.
'''
    llms += '\n## Release notes\n' + '\n'.join(f'- [{p["title"]}]({SITE}/blog/{p["slug"]}/index.md): {p["date"]}; {p["label"]}.' for p in POSTS)
    llms += '\n\n## Organization and contact\n- Powered by [Soleach Digital Agency](https://soleach.com/).\n- Support: help@fcp-aitoolkit.com\n' + '\n'.join(f'- [{name}]({url})' for name,url in SOCIAL) + '\n\n## Optional\n- [Full product and release context](' + SITE + '/llms-full.txt)\n- [RSS](' + SITE + '/feed.rss)\n- [Sitemap](' + SITE + '/sitemap.xml)'
    write('llms.txt', llms)
    write('llms-full.txt', llms + '\n\n---\n\n' + '\n\n---\n\n'.join((ROOT / f'blog/{p["slug"]}/index.md').read_text() for p in POSTS))
    def rssdate(date):
        return format_datetime(datetime.fromisoformat(date).replace(tzinfo=timezone.utc))
    items = '\n'.join(f'<item><title>{xml_escape(p["title"])}</title><link>{SITE}/blog/{p["slug"]}/</link><guid isPermaLink="true">{SITE}/blog/{p["slug"]}/</guid><pubDate>{rssdate(p["date"])}</pubDate><description>{xml_escape(p["excerpt"])}</description><category>{p["label"]}</category></item>' for p in POSTS)
    write('feed.rss', f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>FCP AI Toolkit — The Edit Room</title><link>{SITE}/blog/</link><description>Product updates and release notes from FCP AI Toolkit.</description><language>en</language><lastBuildDate>{rssdate(TODAY)}</lastBuildDate><atom:link href="{SITE}/feed.rss" rel="self" type="application/rss+xml"/>{items}</channel></rss>')
    write('site.webmanifest', json.dumps({'name':'FCP AI Toolkit','short_name':'FCP AI Toolkit','start_url':'/','display':'browser','background_color':'#17121f','theme_color':'#17121f','icons':[{'src':'/images/brand/logo-purple-256.png','sizes':'256x256','type':'image/png'},{'src':'/images/brand/logo-purple-1024.png','sizes':'1024x1024','type':'image/png'}]}, indent=2))
    write('.nojekyll', '')
    write('404.html', page('Page not found — FCP AI Toolkit', 'Return to FCP AI Toolkit.', '/404.html', '<main id="main" class="shell not-found"><p class="eyebrow">404 / OUT OF FRAME</p><h1>Let’s get you<br><span class="serif">back on track.</span></h1><a class="button button-lime" href="/">Back to the homepage ↗</a></main>').replace('index, follow, max-image-preview:large', 'noindex, follow'))

if __name__ == '__main__':
    home()
    blog()
    privacy()
    discovery()
    from localize import build_locales
    build_locales()
    print(f'Built homepage, blog index, {len(POSTS)} posts, privacy, 404 and discovery files.')
