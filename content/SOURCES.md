# Website factual sources

Verified October 2, 2026. Version 1.1.1 is the available release.

## App Store

Primary metadata: https://itunes.apple.com/lookup?id=6775619373&country=us

- Product: FCP AI-Toolkit, ID 6775619373.
- Available version: 1.1.1, live since `2026-09-30T20:35:20Z` (lookup checked 2026-10-02; 0 ratings).
- Original release: June 21, 2026 (`2026-06-21T07:00:00Z`).
- Minimum macOS version: 26.4.
- Free download and included Motion templates; automatic AI caption generation requires an active monthly subscription.
- The App Store description confirms a native Final Cut Pro extension and titles organized into a compound clip inside a secondary storyline.
- Do not infer trial eligibility, current regional subscription price, exact minimum chip/RAM, or a minimum Final Cut Pro version.

## Version 1.1.1

Sources, checked October 2, 2026: the public App Store lookup (version, date and release notes), App Store Connect (read-only: version record and builds), and the app repository (`v1.1.1` tag, commits `677736d` and `58fe7c0`).

- 1.1 was finished on September 22, 2026 and announced as a preview the same day. It was never released publicly; 1.1 builds 19–21 were internal only.
- September 25, 2026: a final test on real projects found two bugs. Both were fixed that day and the version became 1.1.1 (build 31). Submitted September 27; live September 30.
- Features: Smart Cache, persistent caption text and timing edits with a remove button, Smart Search across cached captions, about 100 Whisper-model languages with local Auto Detect, layout for smaller Final Cut Pro windows.
- Fixes: overlapping duplicate captions that could lock the caption editor; caption timing for detached and connected audio.
- The caption editor and the window-size problem never reached a public version, so copy must not say users met them.
- The ~100-language catalog does not mean each language has been separately quality validated. Standard subtitle-file export, text-to-speech, automatic YouTube upload, visual search and direct Final Cut Pro playhead control are not claims.
- The 1.1.1 workspace image (`images/product/workspace-1-1-1.webp`) is a frame from the owner's screen recording of the 1.1.1 build in Final Cut Pro, September 25, 2026.

## Privacy and branding

Application implementation uses local WhisperKit transcription, model downloads, and Apple StoreKit purchases. Network use for downloads and purchases must remain distinct from local audio processing. A source review is not a third-party privacy audit.

Website logo: the owner requested the original transparent purple mark from `images/app-icon.png` on September 22, 2026. The favicon, header, footer and manifest now use resized versions of that mark. Social profile image: the owner supplied `fcp-ai-toolkit-icon.png`, preserved byte-for-byte in `brand/`. The purple YouTube banner uses it as an Imagegen reference. The native Swift app icon was not changed.

The production privacy page at https://www.fcp-aitoolkit.com/privacy/ listed `help@fcp-aitoolkit.com` on September 22, 2026. This address is preserved; mailbox deliverability was not tested.

Agency: https://soleach.com/ (live-verified). Attribution: “Powered by Soleach Digital Agency.”

Social URLs were supplied by the owner. YouTube’s handle is `@FCPAIToolkit` (changed from `@fcpaitoolki` on 2026-09-30); Instagram and TikTok use `@fcpaitoolkit`.

`llms.txt` is a useful convention, not a promise of AI indexing or ranking.
