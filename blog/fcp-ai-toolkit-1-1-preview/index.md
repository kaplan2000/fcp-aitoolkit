# Coming in 1.1: less repetition, more control.

Date: 2026-09-22
Status: Coming soon
Canonical: https://www.fcp-aitoolkit.com/blog/fcp-ai-toolkit-1-1-preview/

Smart Cache, lasting caption corrections, transcript search, and 100 Whisper-model languages with Auto Detect. Here is what we are preparing next.

Version 1.1 is coming soon. This update focuses on what happens when you return to an edit: running the same audio again, correcting a caption, adjusting its timing, or trying to find a line you remember hearing.

We are bringing Smart Cache, persistent caption editing, Smart Search, and a wider language selector into FCP AI-Toolkit. The release is being prepared; version 1.0 remains the version available on the Mac App Store. We have not announced a release date for 1.1.


## Transcribe once. Reuse the work.
Smart Cache will remember previously transcribed sections of your media on your Mac. When you analyze the same material again with the same language and model, the extension can reuse those results instead of asking the model to repeat the whole job.

If you extend a clip to include audio that has not been transcribed yet, only the missing sections need fresh transcription. This is especially useful while an edit is still changing: you can revisit a clip or try a different title style without starting every caption pass from scratch. Smart Cache will be enabled by default, with an option to turn it off.


## Make a correction. Keep the correction.
The new editor will let you change caption text directly inside the extension. Fix a name, adjust punctuation, or refine a phrase before generating titles. Your text corrections will be saved locally and reapplied when that cached media is used again.

Start and end time edits will also persist. You will be able to tighten a caption’s timing and keep that adjustment when you reopen the extension or analyze the material again. The editor checks for invalid time ranges and neighboring-caption overlaps so a small timing change does not silently create a broken sequence.


## Find the line you remember
Smart Search will let you search captions saved in your local cache. Results will show the matching text, source filename, and timecode, helping you identify a useful line without reading through every transcript.

The search will reflect saved text corrections, so the name you fixed in the editor is the name you can find later. In 1.1, a search result provides a reference to the relevant media and time. Clicking a result will not navigate directly to a clip in Final Cut Pro.


## 100 model languages, plus Auto Detect
The language selector will expose all 100 language codes in the Whisper model catalog, together with Auto Detect. Choose a language explicitly, or let the model identify it locally as part of transcription. After the model is downloaded, transcription and language detection stay on your Mac.

The number describes model language coverage. It does not mean we have separately tested transcription quality in every language. Accuracy still depends on the language, recording, speaker, and model, so reviewing generated captions remains part of the workflow.


## The same title workflow, with fewer interruptions
The five existing Motion templates and FCPXML handoff remain part of the experience. We are also improving how the extension fits Final Cut Pro’s saved window sizes, keeping the project drop area and template choices accessible in smaller windows.

The pricing boundary remains the same: Motion templates are free, and the AI caption workflow requires an active monthly subscription. Version 1.1 concentrates on cache, editing, search, and language coverage. SRT export, text-to-speech, and visual or semantic search are outside this update.

We will share the release announcement here when 1.1 is available. Follow our [YouTube](https://youtube.com/@fcpaitoolki?si=HdQzmtITilWRwaA-), [Instagram](https://www.instagram.com/fcpaitoolkit/), and [TikTok](https://www.tiktok.com/@fcpaitoolkit) channels for future walkthroughs and updates as we begin publishing.
