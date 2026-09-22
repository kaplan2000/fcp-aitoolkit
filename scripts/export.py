#!/usr/bin/env python3
"""Export only the public site; never deploy maintainer notes or graph output."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ['index.html', '404.html', 'CNAME', '.nojekyll', 'feed.rss', 'robots.txt', 'sitemap.xml', 'llms.txt', 'llms-full.txt', 'site.webmanifest', 'css/site.css', 'js/site.js', 'images/favicon.png', 'images/product/workspace.webp']
DIRS = ['blog', 'privacy', 'images/brand']
ASSETS = ['app-icon-original.png', 'social-profile-1024.png', 'youtube-banner-2560x1440.jpg', 'youtube-banner-2560x1440.png', 'fcp-ai-toolkit-social-kit.zip']

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 scripts/export.py OUTPUT_DIRECTORY')
dest = Path(sys.argv[1]).resolve()
if dest == ROOT or ROOT.is_relative_to(dest):
    raise SystemExit('Export directory must not be the source repository or its parent.')
dest.mkdir(parents=True, exist_ok=True)
for name in FILES + ['brand/' + name for name in ASSETS]:
    target = dest / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, target)
for name in DIRS:
    shutil.copytree(ROOT / name, dest / name, dirs_exist_ok=True)
print(f'Exported public website to {dest}')
