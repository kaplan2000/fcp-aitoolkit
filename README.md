# FCP AI Toolkit website

A small, static marketing site with a shared layout, release blog, RSS and machine-readable product information. Hosted on GitHub Pages at https://www.fcp-aitoolkit.com/ from the `gh-pages` branch.

## Edit and preview

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://localhost:4173. No JavaScript build tools or external packages are needed. Navigation, articles and FAQ work without JavaScript; the small script adds a mobile menu and illustrative style selector.

- `scripts/build.py`: shared layout, homepage, privacy and all generated discovery files.
- `content/posts.json`: blog articles, newest first. Each article needs a unique slug, title, ISO date, label, version, excerpt and trusted semantic HTML body.
- `content/product.json`: verified product facts and release boundaries.
- `css/site.css`, `js/site.js`: responsive styles and progressive enhancements.
- `images/brand/`: current app icon and social share card.
- `brand/`: downloadable logo, profile image and YouTube banner package.

After adding a post, run the builder and validator. The blog index, homepage cards, RSS, sitemap, Markdown copies and `llms-full.txt` are generated together. Update the current-version and upcoming-version copy when a release ships. `TODAY` in the builder is the editorial modification date; update it when making substantive content changes, not on every deployment.

## Publishing

`python3 scripts/export.py /tmp/fcp-ai-toolkit-public` exports only public website files. Maintainer notes, scripts, source content and the knowledge graph are excluded. Deploy that directory's contents to the existing `gh-pages` branch while preserving its history and `CNAME`; the source stays on `main`.

## Discoverability

The site includes canonical URLs, page descriptions, Open Graph/Twitter cards, JSON-LD, sitemap, robots.txt, RSS, llms.txt, llms-full.txt and per-article Markdown. `llms.txt` is a helpful convention; it does not guarantee inclusion in AI answers. Search Console/Bing submission and an introductory product demo are useful next steps.

The site deliberately does not show invented reviews, rankings, unverified trial offers, or a release date for the upcoming 1.1 version. External social accounts are described as newly opened.
