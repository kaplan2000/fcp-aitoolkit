# Website security and operations

Reviewed on 2026-09-22. This document describes the website, not the macOS application's security model. It records repository safeguards and deployment requirements; it does not claim immunity from abuse or that every Cloudflare account setting has been verified.

## Architecture and trust boundary

The site is generated HTML, CSS, JavaScript, images, RSS, Markdown and discovery files. `scripts/build.py` and `scripts/localize.py` run at build time. `wrangler.jsonc` serves the exported `dist/` directory with Workers Static Assets on `https://www.fcp-aitoolkit.com/*`. There is no request-time application script, database, login, upload endpoint, payment processor or server-held application secret. Downloads and subscriptions are handled by the linked Mac App Store service.

English lives at `/`; the other nine languages have explicit paths. Articles and navigation are readable without JavaScript. Theme choice is validated against `light`, `dark` and `system`, stored only in browser local storage, and never submitted to the site.

Repository writers and deployment credentials are trusted. Blog bodies are trusted, checked-in HTML, not a sanitizer boundary for arbitrary user submissions. Localized text and attributes are HTML-escaped; structured data escapes closing tags; RSS values are XML-escaped. Client scripts use fixed choices, `textContent` and DOM properties rather than interpreting supplied HTML. There are no advertising or third-party analytics scripts in this build.

## Browser safeguards

`_headers` defines a restrictive same-origin Content Security Policy: scripts and styles come from this origin, without `unsafe-inline` or `unsafe-eval`; object loading, base-URL changes and form submissions are disabled. Framing is denied through both `frame-ancestors 'none'` and `X-Frame-Options: DENY`. Other configured headers include MIME-sniffing protection, a restricted referrer policy, disabled camera/microphone/location/payment/USB capabilities, and one-year HSTS without subdomain or preload opt-in.

The generated HTML also contains a CSP meta element for the GitHub Pages backup. This does not reproduce every response-header safeguard: framing protection cannot be supplied through CSP meta, and HSTS and the other HTTP headers must be checked separately after a fallback. See [MDN's frame-ancestors reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors).

Cloudflare applies `_headers` to static asset responses. If a future change adds a Worker that constructs responses, attach equivalent headers there too. Confirm headers on the deployed hostname, including error pages; source configuration is not proof of a live response. See [Workers Static Assets headers](https://developers.cloudflare.com/workers/static-assets/headers/).

## Publishing and artifact hygiene

`scripts/export.py` selects public files and directories, assembles them in a fresh staging directory and replaces the dedicated repository `dist/` only after the copy succeeds. It rejects nonempty arbitrary destinations, a symlink destination, Git checkouts, symlinked source files, and hidden or unexpected file types in copied public trees. This prevents the stale-file leak possible when repeatedly merging into an existing export. Maintainer notes, source catalogs, scripts, credentials, Git metadata and graph output do not belong in the deployed artifact. Public directory trees and downloadable ZIP contents still require review; a permitted file extension is not a content audit.

From the repository root, the standard command is:

```sh
python3 scripts/export.py dist
```

For a separate export, choose a new or empty directory outside the public source directories. Do not place output within a blog, language or image source tree.

Run the build and content checks, then verify the exported artifact with the production serving configuration. Confirm representative pages in every language, one unknown path returning a real 404, CSS/JavaScript/image MIME types, security headers, and the crawler endpoints. The HTML and header CSPs should remain consistent. Avoid introducing inline scripts/styles or external assets without deliberately revisiting both policies.

The configured route covers HTTPS on `www` only. HTTP traffic retains the existing HTTPS redirect through Cloudflare/GitHub Pages instead of being intercepted by static asset routing. Cloudflare requires the matching DNS record to be proxied; an active zone alone is insufficient. Confirm the HTTP-to-HTTPS and apex-to-`www` redirects independently; the configured HSTS and CSP do not themselves create a first-visit HTTP redirect. Keep the GitHub Pages origin and custom-domain association intact while using it as backup. `workers.dev` and version preview URLs are disabled in the configuration. See [Cloudflare route prerequisites](https://developers.cloudflare.com/workers/configuration/routing/routes/).

## Abuse controls and crawler access

The 2026-09-22 access audit confirmed the active Free Website zone and OAuth access to Workers deployment and routes. Attempts to read zone settings, DNS records, WAF rulesets and bot-management settings returned HTTP 403. The current OAuth session does not provide those product permissions. This repository therefore does not claim that custom WAF rules, bot settings, AI Crawl Control policies or rate limits have been inspected, enabled or tuned. Those controls require the corresponding dashboard access or scoped API authorization.

There is no application rate limiter in this static build. Any traffic rules must be chosen from observed traffic and the zone's available features, with allowance for shared client IPs and normal asset loading. Monitor legitimate access and rollback impact before broadening a rule. Rate limits are not an exact global request ceiling, and can affect indexing. See [Cloudflare rate-limiting behavior and availability](https://developers.cloudflare.com/waf/rate-limiting-rules/).

`robots.txt` permits public crawling, while sitemap, hreflang, RSS, per-article Markdown and the `llms` files expose the content directly. These are discovery conventions, not authentication or firewall rules. They neither bypass security controls nor guarantee indexing. Check Cloudflare's managed robots and AI Crawl Control settings for conflicts with the site's intended accessibility. See [AI Crawl Control](https://developers.cloudflare.com/ai-crawl-control/).

Never exempt requests from security solely because the User-Agent contains a crawler name. Anyone can send that header. If an operational exception is needed, use verified identity signals and a narrow rule for the necessary paths and controls; do not disable all protections for every crawler. See [Cloudflare verified bots](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/).

## Rollback

1. Confirm the GitHub Pages `gh-pages` deployment contains the intended public build and its `CNAME`, and that the existing origin still serves it over HTTPS. Record the active Worker version and exact route before changing routing.
2. For a content regression, restore a known-good static deployment. To return traffic to GitHub Pages, remove only the Worker route `https://www.fcp-aitoolkit.com/*`, preserving the existing DNS record, zone, origin and GitHub Pages custom domain. This works only while that origin configuration remains valid.
3. Verify homepage, a localized article, crawler files, error status and response headers at the public hostname. Backup hosting may have a reduced header policy, as described above.
4. Update the deployment configuration or suspend its automation so the next deployment does not recreate the removed route unintentionally. Re-enable the route only after the replacement is verified.

## Reporting

Report a vulnerability privately to `help@fcp-aitoolkit.com` with the affected URL, a minimal reproduction and expected impact. Avoid sending private media, credentials or unrelated personal data. The machine-readable contact is `/.well-known/security.txt`; renew its expiry before 2027-09-22. No response-time guarantee or bounty program is implied.
