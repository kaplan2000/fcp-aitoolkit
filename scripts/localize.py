"""Build crawlable language editions from the shared semantic HTML and catalogs."""
import json
import re
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit
from xml.sax.saxutils import escape as xml_escape

from build import ROOT, SITE, POSTS, TODAY, write, asset

# Language paths are stable and explicit; never redirect based on IP or browser language.
LOCALES = {
    'en': ('English', 'en', 'en_US'),
    'tr': ('Türkçe', 'tr', 'tr_TR'),
    'es': ('Español', 'es', 'es_ES'),
    'fr': ('Français', 'fr', 'fr_FR'),
    'pt': ('Português', 'pt-BR', 'pt_BR'),
    'ru': ('Русский', 'ru', 'ru_RU'),
    'ar': ('العربية', 'ar', 'ar_AR'),
    'hi': ('हिन्दी', 'hi', 'hi_IN'),
    'bn': ('বাংলা', 'bn', 'bn_BD'),
    'zh': ('简体中文', 'zh-Hans', 'zh_CN'),
}
PAGES = ['index.html', 'blog/index.html', 'privacy/index.html', '404.html'] + [f'blog/{p["slug"]}/index.html' for p in POSTS]
CSP = "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; manifest-src 'self'; base-uri 'none'; object-src 'none'; form-action 'none'; upgrade-insecure-requests"

def prefix(lang):
    return '' if lang == 'en' else '/' + lang

def page_path(file):
    return '/' + file.removesuffix('index.html')

def localized_url(url, lang):
    parsed = urlsplit(url)
    if parsed.scheme and (parsed.scheme != 'https' or parsed.netloc != urlsplit(SITE).netloc):
        return url
    path = parsed.path
    if not path.startswith('/') and not (parsed.netloc and not path):
        return url
    if path in ('', '/', '/404.html', '/feed.rss') or path.startswith(('/blog/', '/privacy/')):
        path = prefix(lang) + (path or '/')
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))

class Localizer(HTMLParser):
    def __init__(self, lang, catalog, route=None):
        super().__init__(convert_charrefs=True)
        self.lang, self.catalog, self.route = lang, catalog, route
        self.output, self.script_type = [], None

    def text(self, value):
        key = value.strip()
        if key in self.catalog:
            return value[:len(value)-len(value.lstrip())] + self.catalog[key] + value[len(value.rstrip()):]
        return value

    def schema(self, value, field=''):
        if isinstance(value, dict):
            return {k: self.schema(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [self.schema(v, field) for v in value]
        if isinstance(value, str):
            if field == 'inLanguage':
                return LOCALES[self.lang][1]
            if field in ('@id', 'url', 'mainEntityOfPage', 'item'):
                return localized_url(value, self.lang)
            if field in ('name', 'description', 'headline', 'operatingSystem'):
                return self.text(value)
        return value

    def handle_decl(self, decl):
        self.output.append('<!' + decl + '>')

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'html':
            values.update(lang=LOCALES[self.lang][1], dir='rtl' if self.lang == 'ar' else 'ltr')
        if tag == 'script':
            self.script_type = values.get('type', 'text/javascript')
        for key, value in list(values.items()):
            if value is None:
                continue
            if key in ('href',) or tag == 'meta' and values.get('property') == 'og:url' and key == 'content':
                values[key] = localized_url(value, self.lang)
            elif key in ('aria-label', 'alt', 'title') or tag == 'meta' and key == 'content' and values.get('name', values.get('property')) in ('description', 'og:title', 'og:description', 'og:image:alt', 'twitter:title', 'twitter:description'):
                values[key] = self.text(value)
        self.output.append('<' + tag + ''.join(' ' + k + ('' if v is None else '="' + escape(v, quote=True) + '"') for k,v in values.items()) + '>')
        if tag == 'head' and self.route is not None:
            self.output.append('<meta http-equiv="Content-Security-Policy" content="' + escape(CSP, quote=True) + '"><meta name="referrer" content="strict-origin-when-cross-origin"><script src="' + asset('/js/theme.js') + '"></script>')

    def handle_endtag(self, tag):
        if tag == 'head' and self.route is not None:
            self.output.append(f'<meta property="og:locale" content="{LOCALES[self.lang][2]}">')
            for lang, (_, hreflang, og) in LOCALES.items():
                self.output.append(f'<link rel="alternate" hreflang="{hreflang}" href="{SITE}{prefix(lang)}{self.route}">')
                if lang != self.lang:
                    self.output.append(f'<meta property="og:locale:alternate" content="{og}">')
            self.output.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{self.route}">')
        self.output.append('</' + tag + '>')
        if tag == 'script':
            self.script_type = None
        if tag == 'nav' and self.route is not None:
            self.output.append(self.controls())

    def handle_data(self, data):
        if self.script_type == 'application/ld+json':
            self.output.append(json.dumps(self.schema(json.loads(data)), ensure_ascii=False).replace('</', '<\\/'))
        elif self.script_type:
            self.output.append(data)
        else:
            self.output.append(escape(self.text(data), quote=False))

    def controls(self):
        t = lambda key: escape(self.catalog[key], quote=True)
        links = ''.join(f'<a href="{prefix(lang)}{self.route}" lang="{tag}" hreflang="{tag}" dir="auto"{ " aria-current=\"true\"" if lang == self.lang else ""}>{name}<span aria-hidden="true">{lang.upper()}</span></a>' for lang,(name,tag,_) in LOCALES.items())
        options = ''.join(f'<option value="{value}">{t(label)}</option>' for value,label in [('system','System'),('light','Light'),('dark','Dark')])
        return f'<div class="site-preferences"><details class="language-picker"><summary aria-label="{t("Choose language")}"><span aria-hidden="true">◎</span> <span>{self.lang.upper()}</span><span aria-hidden="true">⌄</span></summary><div class="language-options"><p>{t("Available languages")}</p>{links}</div></details><label class="theme-picker"><span class="sr-only">{t("Appearance")}</span><span aria-hidden="true">◐</span><select id="theme-select" aria-label="{t("Select appearance")}" disabled>{options}</select></label></div>'

    def render(self, source):
        self.feed(source)
        self.close()
        return ''.join(self.output)


def markdown(body):
    body = re.sub(r'<h2>(.*?)</h2>', r'\n## \1\n', body)
    body = re.sub(r'<h3>(.*?)</h3>', r'\n### \1\n', body)
    body = re.sub(r'<a href="(.*?)"[^>]*>(.*?)</a>', r'[\2](\1)', body)
    body = body.replace('<li>', '\n- ').replace('</p>', '\n\n')
    return unescape(re.sub('<[^>]+>', '', body)).strip()


def build_locales():
    from datetime import datetime, timezone
    from email.utils import format_datetime
    source = {file: (ROOT / file).read_text() for file in PAGES}
    en = json.loads((ROOT / 'content/locales/en.json').read_text())
    sitemap = []
    rssdate = lambda date: format_datetime(datetime.fromisoformat(date).replace(tzinfo=timezone.utc))
    for lang, (_, tag, _) in LOCALES.items():
        catalog = json.loads((ROOT / f'content/locales/{lang}.json').read_text())
        if set(catalog) != set(en) or any(not isinstance(v,str) or not v.strip() for v in catalog.values()):
            raise ValueError(f'{lang}: catalog keys must match en.json with nonempty text. Missing: {set(en)-set(catalog)}; extra: {set(catalog)-set(en)}')
        for file, html in source.items():
            route = page_path(file)
            output = prefix(lang).lstrip('/') + ('/' if lang != 'en' else '') + file
            write(output, Localizer(lang, catalog, route).render(html))
            if file != '404.html':
                alternates = ''.join(f'<xhtml:link rel="alternate" hreflang="{l[1]}" href="{SITE}{prefix(code)}{route}"/>' for code,l in LOCALES.items()) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{route}"/>'
                sitemap.append(f'<url><loc>{SITE}{prefix(lang)}{route}</loc><lastmod>{TODAY}</lastmod>{alternates}</url>')
        for post in POSTS:
            path = prefix(lang) + f'/blog/{post["slug"]}/'
            body = Localizer(lang, catalog).render(post['body'])
            write(path.lstrip('/') + 'index.md', f'# {catalog[post["title"]]}\n\nDate: {post["date"]}\nStatus: {catalog[post["label"]]}\nLanguage: {tag}\nCanonical: {SITE}{path}\n\n{catalog[post["excerpt"]]}\n\n' + markdown(body))
        items = ''.join(f'<item><title>{xml_escape(catalog[p["title"]])}</title><link>{SITE}{prefix(lang)}/blog/{p["slug"]}/</link><guid isPermaLink="true">{SITE}{prefix(lang)}/blog/{p["slug"]}/</guid><pubDate>{rssdate(p["date"])}</pubDate><description>{xml_escape(catalog[p["excerpt"]])}</description><category>{xml_escape(catalog[p["label"]])}</category></item>' for p in POSTS)
        write(prefix(lang).lstrip('/') + ('/' if lang != 'en' else '') + 'feed.rss', f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>{xml_escape(catalog["The FCP AI Toolkit Journal"])}</title><link>{SITE}{prefix(lang)}/blog/</link><description>{xml_escape(catalog["Product updates, release notes and a look at what is coming next for FCP AI Toolkit."])}</description><language>{tag}</language><lastBuildDate>{rssdate(TODAY)}</lastBuildDate><atom:link href="{SITE}{prefix(lang)}/feed.rss" rel="self" type="application/rss+xml"/>{items}</channel></rss>')
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(sitemap) + '\n</urlset>')
    language_index = '\n\n## Website languages\n' + '\n'.join(f'- [{name}]({SITE}{prefix(lang)}/): [Blog]({SITE}{prefix(lang)}/blog/), [RSS]({SITE}{prefix(lang)}/feed.rss).' for lang,(name,_,_) in LOCALES.items())
    llms = (ROOT / 'llms.txt').read_text().rstrip() + language_index
    write('llms.txt', llms)
    write('llms-full.txt', llms + '\n\n---\n\n' + '\n\n---\n\n'.join((ROOT / f'blog/{p["slug"]}/index.md').read_text() for p in POSTS))
    print(f'Localized {len(PAGES)} pages and {len(POSTS)} articles in {len(LOCALES)} languages.')
