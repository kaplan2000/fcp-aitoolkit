#!/usr/bin/env python3
"""Export only the public site; never deploy maintainer notes or graph output."""
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ['index.html', '404.html', 'CNAME', '.nojekyll', 'feed.rss', 'robots.txt', 'sitemap.xml', 'llms.txt', 'llms-full.txt', 'site.webmanifest', 'css/site.css', 'js/site.js', 'js/theme.js', '_headers', '.well-known/security.txt', 'images/favicon.png', 'images/product/workspace.webp']
DIRS = ['blog', 'privacy', 'images/brand', 'tr', 'es', 'fr', 'pt', 'ru', 'ar', 'hi', 'bn', 'zh']
ASSETS = ['app-icon-original.png', 'fcp-ai-toolkit-icon.png', 'logo-purple-transparent.png', 'youtube-banner-purple-2560x1440.jpg', 'youtube-banner-purple-2560x1440.png', 'social-profile-1024.png', 'youtube-banner-2560x1440.jpg', 'youtube-banner-2560x1440.png', 'fcp-ai-toolkit-social-kit.zip', 'fcp-ai-toolkit-purple-social-kit.zip']

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 scripts/export.py OUTPUT_DIRECTORY')
requested = Path(sys.argv[1])
if requested.is_symlink():
    raise SystemExit('Export directory must not be a symlink.')
dest = requested.resolve()
if dest == ROOT or ROOT.is_relative_to(dest):
    raise SystemExit('Export directory must not be the source repository or its parent.')
# Only our dedicated generated dist folder may be replaced. A worktree or an
# arbitrary nonempty user directory must never be wiped or silently merged.
if dest.exists() and any(dest.iterdir()) and dest != ROOT / 'dist':
    raise SystemExit('Choose an empty export directory; existing files are not merged.')
source_files = [ROOT / name for name in FILES + ['brand/' + name for name in ASSETS]]
for name in DIRS:
    for source in (ROOT / name).rglob('*'):
        if source.is_symlink():
            raise SystemExit(f'Refusing symlink in public output: {source.relative_to(ROOT)}')
        if source.is_file():
            if any(part.startswith('.') for part in source.relative_to(ROOT).parts):
                raise SystemExit(f'Refusing hidden file in public output: {source.relative_to(ROOT)}')
            if source.suffix not in {'.html', '.md', '.rss', '.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico'}:
                raise SystemExit(f'Unexpected public asset type: {source.relative_to(ROOT)}')
            source_files.append(source)
for source in source_files:
    if source.is_symlink() or not source.is_file():
        raise SystemExit(f'Missing file or unsafe symlink: {source.relative_to(ROOT)}')
dest.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='.fcp-site-build-', dir=dest.parent) as staging:
    stage = Path(staging) / 'public'
    stage.mkdir()
    for source in source_files:
        target = stage / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    # Assemble first so a failed copy leaves the previous export intact.
    if dest.exists():
        if (dest / '.git').exists():
            raise SystemExit('Refusing to replace a Git checkout.')
        dest.rename(Path(staging) / 'previous')
    stage.rename(dest)
print(f'Exported {len(source_files)} public website files to {dest}')
