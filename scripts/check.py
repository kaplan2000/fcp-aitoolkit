#!/usr/bin/env python3
"""Check the built site's public URLs and machine-readable publishing contract.

Run after scripts/build.py. Uses only the Python standard library, does not
contact external services, and ignores unreferenced legacy images/CSS/JS.
"""

import json
import re
import struct
import sys
from datetime import date, datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree as ET

from localize import LOCALES

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
COUNTS = {"local references": 0, "JSON-LD documents": 0}


def require(condition, message):
    if not condition:
        ERRORS.append(message)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.raw = path.read_text()
        self.ids, self.references, self.links, self.meta = set(), [], [], {}
        self.jsonld, self.text, self.times = [], [], []
        self.title, self.h1_count = "", 0
        self.in_title = False
        self.script_type = None
        self.script_text = ""
        self.script_src = None
        self.html_attrs = {}
        self.scripts = []
        self.csp = ""
        self.feed(self.raw)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.html_attrs = attrs
        require(tag != "style", f"{self.path}: inline style block violates strict CSP")
        require("style" not in attrs, f"{self.path}: inline style attribute violates strict CSP")
        require(not any(key.startswith("on") for key in attrs), f"{self.path}: inline event handler violates strict CSP")
        if attrs.get("id"):
            require(attrs["id"] not in self.ids, f"{self.path}: duplicate id {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for key in ("href", "src", "poster"):
            if key in attrs:
                self.references.append(attrs[key])
                require(not attrs[key].strip().lower().startswith("javascript:"),
                        f"{self.path}: executable javascript: URL")
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            self.references.extend(item.strip().split()[0] for item in attrs["srcset"].split(",") if item.strip())
        if tag == "link":
            self.links.append(attrs)
        if tag == "meta":
            self.meta[attrs.get("name", attrs.get("property", ""))] = attrs.get("content", "")
            if attrs.get("http-equiv", "").lower() == "content-security-policy":
                self.csp = attrs.get("content", "")
        if tag == "time":
            self.times.append(attrs.get("datetime", ""))
        if tag == "script":
            self.script_type = attrs.get("type", "text/javascript")
            self.script_text = ""
            self.script_src = attrs.get("src")
            if self.script_src:
                self.scripts.append(self.script_src)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1

    def handle_endtag(self, tag):
        if tag == "script":
            require(self.script_type in ("application/ld+json", "application/json")
                    or not self.script_text.strip(), f"{self.path}: inline executable script violates strict CSP")
            require(self.script_type in ("application/ld+json", "application/json")
                    or bool(self.script_src), f"{self.path}: executable script must use a local src")
            if self.script_type == "application/ld+json":
                try:
                    self.jsonld.append(json.loads(self.script_text))
                    COUNTS["JSON-LD documents"] += 1
                except json.JSONDecodeError as exc:
                    ERRORS.append(f"{self.path}: invalid JSON-LD: {exc}")
            self.script_type = None
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.script_type is not None:
            self.script_text += data
        else:
            self.text.append(data)
        if self.in_title:
            self.title += data

    def rel(self, name):
        return [link for link in self.links if name in link.get("rel", "").split()]


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def iso_date(value, context):
    try:
        result = datetime.fromisoformat(value).date()
        require(result <= date.today(), f"{context}: future publication/modification date {value}")
        return result
    except (TypeError, ValueError):
        ERRORS.append(f"{context}: invalid ISO date {value!r}")
        return None


def route(path):
    relative = path.relative_to(ROOT).as_posix()
    return "/" + (relative[:-10] if relative.endswith("index.html") else relative)


def locale_prefix(lang):
    return "" if lang == "en" else "/" + lang


def split_locale(path):
    first = path.strip("/").split("/")[0]
    if first in LOCALES and first != "en":
        return first, path[len(first) + 1:]
    return "en", path


def main():
    product = json.loads((ROOT / "content/product.json").read_text())
    posts = json.loads((ROOT / "content/posts.json").read_text())
    origin = product["website"].rstrip("/")
    host = urlsplit(origin).netloc
    catalogs = {lang: json.loads((ROOT / f"content/locales/{lang}.json").read_text()) for lang in LOCALES}
    source_keys = set(catalogs["en"])
    for lang, catalog in catalogs.items():
        require(set(catalog) == source_keys, f"{lang}: translation keys differ from English: {set(catalog) ^ source_keys}")
        require(all(isinstance(value, str) and value.strip() for value in catalog.values()), f"{lang}: empty translation")
        require(all(not re.search(r"<[^>]+>", value) for value in catalog.values()), f"{lang}: HTML in a text translation")
    require((ROOT / "CNAME").read_text().strip() == host, "CNAME differs from canonical domain")
    internal_dirs = {".git", "graphify-out", "node_modules", "dist"}
    pages = {route(path): Page(path) for path in ROOT.rglob("*.html")
             if not internal_dirs.intersection(path.relative_to(ROOT).parts)}
    base_routes = {"/", "/blog/", "/privacy/", "/404.html"} | {f"/blog/{post['slug']}/" for post in posts}
    expected_routes = {locale_prefix(lang) + path for lang in LOCALES for path in base_routes}
    require(set(pages) == expected_routes, f"Locale page coverage differs: {set(pages) ^ expected_routes}")
    pages_by_path = {page.path.resolve(): page for page in pages.values()}

    def local_target(value, source, anchors=True):
        require(bool(value.strip()), f"{source}: empty URL")
        absolute = urljoin(origin + source, value)
        url = urlsplit(absolute)
        if url.scheme not in ("http", "https") or url.netloc != host:
            return None
        COUNTS["local references"] += 1
        target = (ROOT / unquote(url.path).lstrip("/")).resolve()
        require(target.is_relative_to(ROOT), f"{source}: URL escapes website root: {value}")
        if not target.is_relative_to(ROOT):
            return None
        if target.is_dir():
            target /= "index.html"
        require(target.is_file(), f"{source}: missing local target {value}")
        if target.is_file() and url.fragment and anchors and target.suffix == ".html":
            page = pages_by_path.get(target)
            require(page is not None and unquote(url.fragment) in page.ids,
                    f"{source}: missing anchor {value}")
        return target

    def expected_alternates(base_path):
        return {tag: origin + locale_prefix(lang) + base_path for lang, (_, tag, _) in LOCALES.items()} | {
            "x-default": origin + base_path}

    def check_alternates(entries, base_path, context):
        require(len(entries) == len(LOCALES) + 1, f"{context}: expected {len(LOCALES) + 1} hreflang entries")
        actual = {entry.get("hreflang"): entry.get("href") for entry in entries}
        require(actual == expected_alternates(base_path), f"{context}: missing, duplicate or incorrect hreflang target")
        for target in actual.values():
            local_target(target or "", base_path)

    schemas = []
    indexable = set()
    active_stylesheets = set()
    for path, page in pages.items():
        lang, base_path = split_locale(path)
        catalog = catalogs[lang]
        language_tag = LOCALES[lang][1]
        canonical = origin + path
        require(page.html_attrs.get("lang") == language_tag, f"{path}: incorrect document language")
        require(page.html_attrs.get("dir") == ("rtl" if lang == "ar" else "ltr"), f"{path}: incorrect writing direction")
        require(page.meta.get("og:locale") == LOCALES[lang][2], f"{path}: incorrect Open Graph locale")
        check_alternates([link for link in page.rel("alternate") if "hreflang" in link], base_path, path)
        directives = {parts[0]: parts[1:] for directive in page.csp.split(";") if (parts := directive.strip().split())}
        for key, values in {"default-src": ["'none'"], "script-src": ["'self'"], "style-src": ["'self'"],
                            "base-uri": ["'none'"], "object-src": ["'none'"]}.items():
            require(directives.get(key) == values, f"{path}: missing or unsafe CSP {key}")
        for src in page.scripts:
            require(urlsplit(urljoin(origin + path, src)).netloc == host, f"{path}: external script violates self-only CSP")
        require(page.title.strip() and page.h1_count == 1, f"{path}: need a title and exactly one h1")
        require(bool(page.meta.get("description")), f"{path}: missing description")
        require([link.get("href") for link in page.rel("canonical")] == [canonical],
                f"{path}: canonical does not match public URL {canonical}")
        require(page.meta.get("og:url") == canonical, f"{path}: og:url differs from canonical")
        require(page.meta.get("og:title") == page.title, f"{path}: social title differs from page title")
        require(bool(page.meta.get("og:description")), f"{path}: missing social description")
        require(page.meta.get("twitter:card") == "summary_large_image", f"{path}: missing social image card")
        for field in ("og:image", "twitter:image"):
            require(bool(page.meta.get(field)), f"{path}: missing {field}")
            if page.meta.get(field):
                local_target(page.meta[field], path)
        for rel in ("icon", "apple-touch-icon", "manifest"):
            require(bool(page.rel(rel)), f"{path}: missing {rel}")
        require([link.get("href") for link in page.rel("alternate") if link.get("type") == "application/rss+xml"]
                == [locale_prefix(lang) + "/feed.rss"], f"{path}: incorrect language-specific RSS link")
        for value in page.references:
            local_target(value, path)
        for link in page.rel("stylesheet"):
            require(urlsplit(urljoin(origin + path, link.get("href", ""))).netloc == host,
                    f"{path}: external stylesheet violates self-only CSP")
            target = local_target(link.get("href", ""), path)
            if target and target.is_file():
                active_stylesheets.add(target)
        if "noindex" not in page.meta.get("robots", ""):
            indexable.add(canonical)
        require(bool(page.jsonld), f"{path}: missing JSON-LD")
        for document in page.jsonld:
            require(document.get("@context") == "https://schema.org", f"{path}: invalid JSON-LD context")
            schemas.extend(objects(document))
            for node in objects(document):
                if "inLanguage" in node:
                    require(node["inLanguage"] == language_tag, f"{path}: schema language differs from document")
                if "@id" in node and node["@id"].startswith(origin):
                    entity_lang, _ = split_locale(urlsplit(node["@id"]).path)
                    require(entity_lang == lang, f"{path}: schema references another language's entity")
        visible = " ".join(" ".join(page.text).split())
        require(product["attribution"] in visible, f"{path}: missing agency credit")
        require(product["agencyUrl"] in page.references, f"{path}: missing agency link")
        for social in product["social"].values():
            require(social in page.references, f"{path}: missing social link {social}")
        require(not re.search(r"example\.com|lorem ipsum|kickstart|your app name", page.raw, re.I),
                f"{path}: template placeholder remains")
    for lang in LOCALES:
        locale_pages = [page for path, page in pages.items() if split_locale(path)[0] == lang]
        require(len({page.title for page in locale_pages}) == len(locale_pages), f"{lang}: duplicate page titles")
        not_found = pages.get(locale_prefix(lang) + "/404.html")
        require(not_found is not None and "noindex" in not_found.meta.get("robots", ""), f"{lang}: 404 must be noindex")
    for stylesheet in active_stylesheets:
        # Consume quoted data URIs as a whole; inline SVG can itself contain url().
        css_urls = r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^)]*))\s*\)"
        for values in re.findall(css_urls, stylesheet.read_text()):
            value = next((value for value in values if value), "")
            local_target(value.strip(), "/" + stylesheet.relative_to(ROOT).as_posix(), anchors=False)

    # Schema entity fragments are identifiers, not DOM anchors.
    definitions = {node["@id"] for node in schemas if "@id" in node and "@type" in node}
    for node in schemas:
        if "@id" in node:
            local_target(node["@id"], "/", anchors=False)
            require(node["@id"] in definitions, f"Unresolved JSON-LD entity {node['@id']}")
        for key in ("url", "mainEntityOfPage", "image", "logo", "item"):
            if isinstance(node.get(key), str):
                value = node[key]
                require(urlsplit(value).scheme == "https", f"JSON-LD {key} is not an absolute HTTPS URL: {value}")
                local_target(value, "/", anchors=False)
        require(not any(key in node for key in ("aggregateRating", "ratingValue", "review")),
                "Unsupported review/rating claim in JSON-LD; no verified ratings in product source")
    software = [node for node in schemas if node.get("@type") == "SoftwareApplication"]
    require(len(software) == len(LOCALES), "Expected one SoftwareApplication definition per language")
    require({node.get("@id") for node in software} == {origin + locale_prefix(lang) + "/#app" for lang in LOCALES},
            "Software schema entity IDs do not cover all language editions")
    for app in software:
        require(app.get("softwareVersion") == product["availableVersion"], "Software schema advertises unreleased/stale version")
        require(app.get("datePublished") == product["releaseDate"], "Software schema release date differs from verified release")
        require(app.get("downloadUrl") == product["appStoreUrl"], "Software schema download URL differs from official app")

    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    require(sitemap.tag == "{" + ns["s"] + "}urlset", "Invalid sitemap namespace/root")
    locations = [entry.findtext("s:loc", namespaces=ns) for entry in sitemap]
    require(len(locations) == len(set(locations)), "Duplicate sitemap URLs")
    require(set(locations) == indexable, f"Sitemap differs from indexable pages: {set(locations) ^ indexable}")
    for entry in sitemap:
        location = entry.findtext("s:loc", namespaces=ns)
        local_target(location or "", "/sitemap.xml")
        iso_date(entry.findtext("s:lastmod", namespaces=ns), f"Sitemap {location}")
        _, base_path = split_locale(urlsplit(location or "").path)
        check_alternates([link.attrib for link in entry.findall("x:link", ns)], base_path, f"Sitemap {location}")
    robots = (ROOT / "robots.txt").read_text()
    require(f"Sitemap: {origin}/sitemap.xml" in robots, "robots.txt does not advertise canonical sitemap")
    require(not re.search(r"^Disallow:\s*/\s*$", robots, re.M), "robots.txt blocks the entire site")

    for lang, (_, tag, _) in LOCALES.items():
        prefix = locale_prefix(lang)
        catalog = catalogs[lang]
        feed_path = prefix + "/feed.rss"
        feed = ET.parse(ROOT / feed_path.lstrip("/")).getroot()
        require(feed.tag == "rss" and feed.get("version") == "2.0", f"{feed_path}: expected RSS 2.0")
        require(feed.findtext("channel/link") == origin + prefix + "/blog/", f"{feed_path}: incorrect channel URL")
        require(feed.findtext("channel/language") == tag, f"{feed_path}: incorrect feed language")
        require(feed.findtext("channel/title") == catalog["The FCP AI Toolkit Journal"], f"{feed_path}: untranslated journal title")
        self_link = feed.find("channel/{http://www.w3.org/2005/Atom}link")
        require(self_link is not None and self_link.get("href") == origin + feed_path
                and self_link.get("rel") == "self", f"{feed_path}: incorrect RSS self link")
        items = feed.findall("channel/item")
        expected = {origin + prefix + f"/blog/{post['slug']}/": post for post in posts}
        require(len(items) == len(posts), f"{feed_path}: item count differs from published posts")
        require({item.findtext("link") for item in items} == set(expected), f"{feed_path}: incomplete post URL coverage")
        for item in items:
            url = item.findtext("link")
            require(item.findtext("guid") == url, f"RSS {url}: GUID differs from URL")
            local_target(url or "", feed_path)
            post = expected.get(url)
            if post:
                require(parsedate_to_datetime(item.findtext("pubDate")).date().isoformat() == post["date"],
                        f"RSS {url}: publication date differs from post")
                require(item.findtext("title") == catalog[post["title"]], f"RSS {url}: title differs from translated post")
                require(item.findtext("description") == catalog[post["excerpt"]], f"RSS {url}: untranslated description")
                require(item.findtext("category") == catalog[post["label"]], f"RSS {url}: release status differs from post")

    llms = (ROOT / "llms.txt").read_text()
    full = (ROOT / "llms-full.txt").read_text()
    for name, text in (("llms.txt", llms), ("llms-full.txt", full)):
        for value in re.findall(r"\]\((https?://[^\s)]+)\)", text):
            local_target(value, "/" + name)
        require(f"Available version: {product['availableVersion']}" in text, f"{name}: stale available version")
        require(f"Version {product['upcoming']['version']}: coming soon" in text,
                f"{name}: upcoming version is not clearly labeled")
        for path in ("/", "/blog/", "/privacy/", "/feed.rss", "/sitemap.xml"):
            require(f"({origin}{path})" in text, f"{name}: missing discovery route {path}")
        for lang in LOCALES:
            for path in ("/", "/blog/", "/feed.rss"):
                require(f"({origin}{locale_prefix(lang)}{path})" in text, f"{name}: missing {lang} discovery route {path}")
    for lang, (_, tag, _) in LOCALES.items():
        catalog = catalogs[lang]
        for post in posts:
            path = locale_prefix(lang) + f"/blog/{post['slug']}/"
            published = iso_date(post["date"], post["slug"])
            require(path in pages, f"Missing generated post {path}")
            if path not in pages:
                continue
            page = pages[path]
            require(post["date"] in page.times, f"{path}: missing visible publication date")
            require(page.meta.get("article:published_time", "").startswith(post["date"]), f"{path}: article date differs from source")
            require(any(link.get("type") == "text/markdown" and link.get("href") == path + "index.md"
                        for link in page.rel("alternate")), f"{path}: missing Markdown alternate")
            articles = [node for document in page.jsonld for node in objects(document) if node.get("@type") == "BlogPosting"]
            require(len(articles) == 1, f"{path}: expected one BlogPosting schema")
            for article in articles:
                require(article.get("mainEntityOfPage") == origin + path, f"{path}: article schema canonical mismatch")
                require(article.get("headline") == catalog[post["title"]], f"{path}: article schema headline mismatch")
                require(iso_date(article.get("datePublished"), path) == published, f"{path}: schema publication date mismatch")
                modified = iso_date(article.get("dateModified"), path)
                require(modified is not None and published is not None and modified >= published, f"{path}: modification predates publication")
            markdown_path = ROOT / path.strip("/") / "index.md"
            require(markdown_path.is_file(), f"{path}: missing Markdown document")
            if not markdown_path.is_file():
                continue
            markdown = markdown_path.read_text()
            for fact in (f"# {catalog[post['title']]}", f"Date: {post['date']}", f"Status: {catalog[post['label']]}",
                         f"Language: {tag}", f"Canonical: {origin}{path}"):
                require(fact in markdown, f"{path}: Markdown metadata differs: {fact}")
            for value in re.findall(r"\]\((https?://[^\s)]+)\)", markdown):
                local_target(value, path + "index.md")
            if lang == "en":
                require(markdown.strip() in full, f"{path}: llms-full omits English article content")
                require(f"({origin}{path}index.md)" in llms, f"{path}: llms index omits English Markdown route")
            if post["version"] == product["availableVersion"]:
                require(post["date"] == product["releaseDate"] and post["label"] == "Release", f"{path}: incorrect launch date/status")
            if post["version"] == product["upcoming"]["version"]:
                require(post["date"] == product["upcoming"]["announcedOn"], f"{path}: incorrect preview announcement date")
                require(post["label"] == product["upcoming"]["status"], f"{path}: preview status differs from product facts")
                require(catalog["Coming soon"].casefold() in " ".join(page.text).casefold(), f"{path}: preview availability is unclear")

    manifest = json.loads((ROOT / "site.webmanifest").read_text())
    local_target(manifest.get("start_url", ""), "/site.webmanifest")
    require(bool(manifest.get("icons")), "Manifest has no app icons")
    for icon in manifest.get("icons", []):
        target = local_target(icon["src"], "/site.webmanifest")
        if target and target.is_file() and icon.get("type") == "image/png":
            raw = target.read_bytes()
            require(raw[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG icon: {icon['src']}")
            if len(raw) >= 24:
                width, height = struct.unpack(">II", raw[16:24])
                require(f"{width}x{height}" in icon.get("sizes", "").split(), f"Manifest icon dimensions incorrect: {icon['src']}")

    if ERRORS:
        print("Site checks failed:\n" + "\n".join(f"- {error}" for error in ERRORS))
        return 1
    print(f"PASS: {len(LOCALES)} locales, {len(pages)} HTML pages, {len(posts) * len(LOCALES)} localized posts, {len(locations)} sitemap URLs, "
          f"{COUNTS['local references']} local references and {COUNTS['JSON-LD documents']} JSON-LD documents.")
    print("Catalogs, reciprocal hreflang, lang/RTL, CSP, RSS, canonicals, schema, release dates/status, Markdown, llms and icons are consistent.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, TypeError, KeyError, ET.ParseError) as exc:
        print(f"Site checks could not complete: {exc}", file=sys.stderr)
        sys.exit(1)
