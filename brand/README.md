# FCP AI Toolkit social assets

Created 2026-09-22. Art direction: graphite, warm white, muted chartreuse; subtle film grain and editing timeline details.

| File | Size | Intended use |
| --- | --- | --- |
| `app-icon-original.png` | 1024 × 1024 | Exact, unmodified current application icon / source logo |
| `social-profile-1024.png` | 1024 × 1024 | YouTube, Instagram, and TikTok profile image; centered for circular cropping |
| `youtube-banner-2560x1440.jpg` | 2560 × 1440; 523 KB | Upload-ready YouTube banner |
| `youtube-banner-2560x1440.png` | 2560 × 1440; 3.54 MB | Lossless banner export |

The banner's identity and text fit within the centered 1544 × 422 px area (approximately x=508–2052, y=509–931). Background details extend beyond that area. Both banner exports are below 6 MB.

The original icon is copied directly from `fcp-subtitles/Assets.xcassets/AppIcon.appiconset/icon_512x512@2x.png` in the Swift app repository. The social profile and banner are generated brand compositions based on that reference. Use the exact original when pixel-identical logo artwork is required.

Generated with the built-in `image_gen` tool using the prompts in `prompts.md`. The banner source was 1672 × 941 px; it was exported to 2560 × 1440 with macOS `sips`. The profile source was 1254 × 1254 px; it was reduced to 1024 × 1024. JPEG quality: 92. No hand-drawn or code-painted replacement artwork was used.

Visual checks: title spelling, tagline, AI-TK lettering, composition, profile centering, image dimensions, and file sizes checked after export.
