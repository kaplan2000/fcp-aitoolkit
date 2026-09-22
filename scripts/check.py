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
        self.feed(self.raw)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            require(attrs["id"] not in self.ids, f"{self.path}: duplicate id {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for key in ("href", "src", "poster"):
            if key in attrs:
                self.references.append(attrs[key])
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            self.references.extend(item.strip().split()[0] for item in attrs["srcset"].split(",") if item.strip())
        if tag == "link":
            self.links.append(attrs)
        if tag == "meta":
            self.meta[attrs.get("name", attrs.get("property", ""))] = attrs.get("content", "")
        if tag == "time":
            self.times.append(attrs.get("datetime", ""))
        if tag == "script":
            self.script_type = attrs.get("type", "text/javascript")
            self.script_text = ""
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1

    def handle_endtag(self, tag):
        if tag == "script":
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


def main():
    product = json.loads((ROOT / "content/product.json").read_text())
    posts = json.loads((ROOT / "content/posts.json").read_text())
    origin = product["website"].rstrip("/")
    host = urlsplit(origin).netloc
    require((ROOT / "CNAME").read_text().strip() == host, "CNAME differs from canonical domain")
    internal_dirs = {".git", "graphify-out", "node_modules"}
    pages = {route(path): Page(path) for path in ROOT.rglob("*.html")
             if not internal_dirs.intersection(path.relative_to(ROOT).parts)}
    require("/" in pages and "/blog/" in pages and "/404.html" in pages, "Missing homepage, blog, or 404 page")
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

    schemas = []
    indexable = set()
    active_stylesheets = set()
    for path, page in pages.items():
        canonical = origin + path
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
        require(any(link.get("type") == "application/rss+xml" for link in page.rel("alternate")),
                f"{path}: missing RSS discovery link")
        for value in page.references:
            local_target(value, path)
        for link in page.rel("stylesheet"):
            target = local_target(link.get("href", ""), path)
            if target and target.is_file():
                active_stylesheets.add(target)
        if "noindex" not in page.meta.get("robots", ""):
            indexable.add(canonical)
        require(bool(page.jsonld), f"{path}: missing JSON-LD")
        for document in page.jsonld:
            require(document.get("@context") == "https://schema.org", f"{path}: invalid JSON-LD context")
            schemas.extend(objects(document))
        visible = " ".join(" ".join(page.text).split())
        require(product["attribution"] in visible, f"{path}: missing agency credit")
        require(product["agencyUrl"] in page.references, f"{path}: missing agency link")
        for social in product["social"].values():
            require(social in page.references, f"{path}: missing social link {social}")
        require(not re.search(r"example\.com|lorem ipsum|kickstart|your app name", page.raw, re.I),
                f"{path}: template placeholder remains")
    require(len({page.title for page in pages.values()}) == len(pages), "Duplicate page titles")
    require("noindex" in pages["/404.html"].meta.get("robots", ""), "404 must be noindex")
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
    require(len(software) == 1, "Expected one SoftwareApplication definition")
    if software:
        require(software[0].get("softwareVersion") == product["availableVersion"], "Software schema advertises unreleased/stale version")
        require(software[0].get("datePublished") == product["releaseDate"], "Software schema release date differs from verified release")
        require(software[0].get("downloadUrl") == product["appStoreUrl"], "Software schema download URL differs from official app")

    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    require(sitemap.tag == "{" + ns["s"] + "}urlset", "Invalid sitemap namespace/root")
    locations = [entry.findtext("s:loc", namespaces=ns) for entry in sitemap]
    require(len(locations) == len(set(locations)), "Duplicate sitemap URLs")
    require(set(locations) == indexable, f"Sitemap differs from indexable pages: {set(locations) ^ indexable}")
    for entry in sitemap:
        location = entry.findtext("s:loc", namespaces=ns)
        local_target(location or "", "/sitemap.xml")
        iso_date(entry.findtext("s:lastmod", namespaces=ns), f"Sitemap {location}")
    robots = (ROOT / "robots.txt").read_text()
    require(f"Sitemap: {origin}/sitemap.xml" in robots, "robots.txt does not advertise canonical sitemap")
    require(not re.search(r"^Disallow:\s*/\s*$", robots, re.M), "robots.txt blocks the entire site")

    feed = ET.parse(ROOT / "feed.rss").getroot()
    require(feed.tag == "rss" and feed.get("version") == "2.0", "Expected RSS 2.0 feed")
    require(feed.findtext("channel/link") == origin + "/blog/", "RSS channel URL is incorrect")
    items = feed.findall("channel/item")
    expected = {origin + f"/blog/{post['slug']}/": post for post in posts}
    require(len(items) == len(posts), "RSS item count differs from published posts")
    require({item.findtext("link") for item in items} == set(expected), "RSS does not cover all published post URLs")
    for item in items:
        url = item.findtext("link")
        require(item.findtext("guid") == url, f"RSS {url}: GUID differs from URL")
        local_target(url or "", "/feed.rss")
        post = expected.get(url)
        if post:
            require(parsedate_to_datetime(item.findtext("pubDate")).date().isoformat() == post["date"],
                    f"RSS {url}: publication date differs from post")
            require(item.findtext("title") == post["title"], f"RSS {url}: title differs from post")
            require(item.findtext("category") == post["label"], f"RSS {url}: release status differs from post")

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
    for post in posts:
        path = f"/blog/{post['slug']}/"
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
            require(article.get("headline") == post["title"], f"{path}: article schema headline mismatch")
            require(iso_date(article.get("datePublished"), path) == published, f"{path}: schema publication date mismatch")
            modified = iso_date(article.get("dateModified"), path)
            require(modified is not None and published is not None and modified >= published, f"{path}: modification predates publication")
        markdown_path = ROOT / path.strip("/") / "index.md"
        require(markdown_path.is_file(), f"{path}: missing Markdown document")
        if not markdown_path.is_file():
            continue
        markdown = markdown_path.read_text()
        for fact in (f"# {post['title']}", f"Date: {post['date']}", f"Status: {post['label']}", f"Canonical: {origin}{path}"):
            require(fact in markdown, f"{path}: Markdown metadata differs: {fact}")
        require(markdown.strip() in full, f"{path}: llms-full omits article content")
        require(f"({origin}{path}index.md)" in llms, f"{path}: llms index omits Markdown route")
        if post["version"] == product["availableVersion"]:
            require(post["date"] == product["releaseDate"] and post["label"] == "Release", f"{path}: incorrect launch date/status")
        if post["version"] == product["upcoming"]["version"]:
            require(post["date"] == product["upcoming"]["announcedOn"], f"{path}: incorrect preview announcement date")
            require(post["label"] == product["upcoming"]["status"], f"{path}: preview status differs from product facts")
            require("coming soon" in " ".join(page.text).lower(), f"{path}: preview availability is unclear")

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
    print(f"PASS: {len(pages)} HTML pages, {len(posts)} posts, {len(locations)} sitemap URLs, "
          f"{COUNTS['local references']} local references and {COUNTS['JSON-LD documents']} JSON-LD documents.")
    print("RSS, canonical metadata, social links, release dates/status, Markdown, llms, robots and app icons are consistent.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, TypeError, KeyError, ET.ParseError) as exc:
        print(f"Site checks could not complete: {exc}", file=sys.stderr)
        sys.exit(1)
