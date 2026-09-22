# FCP AI Toolkit website

A static, multilingual product website with a release blog, RSS and machine-readable product information. The production site at [www.fcp-aitoolkit.com](https://www.fcp-aitoolkit.com/) is served by Cloudflare Workers Static Assets through the existing proxied `https://www.fcp-aitoolkit.com/*` route. GitHub Pages, published from the `gh-pages` branch, remains the backup. Source files live on `main`.

This is an assets-only deployment: `wrangler.jsonc` points to `dist/` and has no Worker application code or `main` entry point. Cloudflare serves the generated HTML, styles, scripts and media directly.

## Build, check and preview

Use **Python 3.12 or later**. Building, checking and exporting use only the Python standard library; there are no Python packages or frontend build dependencies to install. Node.js is needed for the theme behavior check and for Wrangler deployment.

Run these commands from the repository root:

```sh
python3 scripts/build.py
python3 scripts/check.py
node scripts/check-theme.cjs
python3 scripts/export.py dist
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open [localhost:4173](http://localhost:4173/). The builder calls `scripts/localize.py` automatically; do not run the localizer separately on already translated output. `scripts/check.py` validates generated pages, local references, structured data, language metadata and discovery files. `scripts/check-theme.cjs` exercises theme preference behavior, including system changes, blocked storage and updates between tabs. It uses Node's built-in modules and does not install a browser.

The export includes only public website files. Maintainer notes, source content, scripts and knowledge-graph output are excluded. `dist/` is a replaceable generated directory and is ignored by Git; the exporter refuses to overwrite arbitrary nonempty directories or Git checkouts.

## Content and languages

- `scripts/build.py`: shared layout, homepage, privacy page, blog pages and discovery output.
- `scripts/localize.py`: translated pages, language navigation, localized URLs, metadata, RSS, Markdown and sitemap language alternates.
- `content/locales/*.json`: translation catalogs, using English phrases as stable keys.
- `content/posts.json`: original blog articles. Each needs a unique slug, title, ISO date, label, version, excerpt and trusted semantic HTML body.
- `content/product.json` and `content/SOURCES.md`: verified product facts, release boundaries and their provenance. These are maintainer records, not automatically substituted into every page.
- `css/site.css`, `js/site.js` and `js/theme.js`: responsive design, interaction and appearance preferences.
- `images/brand/`: transparent purple website logo, favicon, touch icon and social share card.
- `brand/`: the owner-supplied colour social icon, transparent purple logo, matching YouTube banner and asset package. See `brand/README.md` for the current files.

There are ten language editions, each with translated pages, both full blog articles, an RSS feed and per-article Markdown:

| Language | URL prefix |
| --- | --- |
| English | `/` |
| Turkish | `/tr/` |
| Spanish | `/es/` |
| French | `/fr/` |
| Brazilian Portuguese | `/pt/` |
| Russian | `/ru/` |
| Arabic | `/ar/` |
| Hindi | `/hi/` |
| Bengali | `/bn/` |
| Simplified Chinese | `/zh/` |

English remains at the root; there is no `/en/` edition. Arabic uses right-to-left layout. Language selection follows explicit URLs and does not redirect visitors based on IP address or browser language. The light, dark and system appearance preference is stored only in the visitor's browser and is not sent to the site operator. Core navigation, articles and FAQ work without JavaScript; scripts add theme selection, the mobile menu and illustrative caption styles.

Every catalog must contain exactly the same keys as `en.json`, with a nonempty string for every value. There are currently **237 keys per language**. When adding copy or a blog post, add each new translatable phrase to the English catalog and all nine other catalogs. When changing an English phrase key, update its source references and all catalogs together. Translate complete article paragraphs, metadata, accessibility labels and fragments around inline elements; preserve feature names and the meaning of combined fragments. The builder fails when catalog key sets differ or values are empty.

Edit the source templates and catalogs rather than generated HTML. Rebuild after content changes so blog cards, localized articles, feeds, sitemap, Markdown copies and machine-readable context remain aligned.

## Release accuracy

The current editorial baseline is **1.0, released June 21, 2026**. The **1.1 preview is dated September 22, 2026** and describes an upcoming release with no announced launch date. Do not present its planned features as available until the public App Store release has been verified.

When a release ships, update the homepage and FAQ, version metadata, relevant posts, product facts, all language catalogs and the `llms.txt`/`llms-full.txt` source copy together. Keep the distinction between free Motion templates and subscription-based automatic AI captions. `TODAY` in `scripts/build.py` is the editorial modification date; change it for substantive content changes, not on every deployment. Preserve the original publication dates of historical release posts.

## Publishing

After the build, checks and `dist/` export pass, deploy with an authenticated Cloudflare account that can update the configured Worker and route:

```sh
npx wrangler deploy --config wrangler.jsonc
```

Wrangler uploads `dist/` as static assets to `fcp-ai-toolkit-site`. The configuration uses the existing `https://www.fcp-aitoolkit.com/*` route; `workers.dev` and preview URLs are disabled. No application Worker entry point is needed. Asset routing uses trailing-slash HTML URLs and the exported 404 page. Security headers are included in the public `_headers` file.

Keep the GitHub Pages backup current by publishing the same exported files to the existing `gh-pages` branch, preserving its Git history and `CNAME`. A Cloudflare deployment does not update that branch automatically. Never publish the source repository wholesale: use the curated export for both destinations. After publishing, verify the production homepage, a translated article, language links, appearance control, RSS and sitemap.

## Discoverability

The site includes canonical URLs, descriptions, Open Graph/Twitter cards, JSON-LD, language alternates, sitemap, robots.txt, localized RSS, `llms.txt`, `llms-full.txt` and per-article Markdown. The language editions are linked explicitly for both visitors and crawlers. `llms.txt` is a useful convention, not a guarantee of inclusion in AI answers.

The site does not invent reviews, rankings, trial offers or future release dates. Social accounts are described as newly opened until actual published content supports updating that description.
