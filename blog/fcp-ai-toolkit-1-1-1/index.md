# FCP AI-Toolkit 1.1.1 is out: 1.1, plus two fixes

Date: 2026-10-02
Status: Release
Language: en
Canonical: https://www.fcp-aitoolkit.com/blog/fcp-ai-toolkit-1-1-1/

1.1.1 is on the Mac App Store with Smart Cache, caption editing, Smart Search and about 100 languages. The extra “.1” is for two bugs we fixed just in time.

FCP AI-Toolkit 1.1.1 has been on the Mac App Store since September 30. If you are on version 1.0, this is your update. Open the Mac App Store and update as you always do.


This release is about one thing: coming back to an edit without starting over. You try another style, trim the intro, fix a name, extend a clip. The captions keep up with you, instead of beginning from zero each time.



## Wait, what happened to 1.1?

Fair question. On September 22 we published a preview called [Coming in 1.1](/blog/fcp-ai-toolkit-1-1-preview/). Version 1.1 was finished and checked. It was only waiting for its launch video.


Then, on September 25, we did one last round of testing on real Final Cut Pro projects. Several clips, detached audio, the kind of mess a real edit has. Two bugs showed up. We fixed both the same day.


We could have released 1.1 and patched it later. We preferred to fix the build first and give it a new number. So 1.1.1 is simply 1.1 plus two fixes. The features are exactly the ones the preview described, and the extra “.1” stands for the two bugs we caught before you could meet them.


We sent 1.1.1 to Apple on September 27, and it went live on September 30. Nobody missed a version: there never was a public 1.1. If you are on 1.0, you go straight to 1.1.1.


- June 21, 2026Version 1.0 is releasedSeptember 22, 20261.1 is previewed and waits for its launch videoSeptember 25, 2026Last test finds two bugs; both fixed that day
- September 27, 20261.1.1 goes to Apple for reviewSeptember 30, 20261.1.1 is live on the Mac App Store

## The first fix: captions that sat on top of each other

When you press Analyze, the extension transcribes each dialogue clip on your timeline on its own, then joins the results. In some projects, that could give you the same line twice, or captions sitting on top of each other. We found three ways it could happen:




- A trimmed clip. You cut the start of a clip on the timeline, but speech from the hidden, trimmed-away part could still come through as captions.

- Two clips with the same speech. Think of camera audio plus a separate microphone, both marked as dialogue. The same words could show up twice.

- The speech model itself. Whisper sometimes returns lines that overlap a little.

On its own, that is annoying. But 1.1.1 also brings a caption editor, and the editor does something sensible: it refuses any timing change that would make a caption overlap its neighbour. With duplicates already overlapping, every fix you tried would have been refused. You would have been stuck, with an editor that felt locked.


Here is what happens now:




- Each clip’s captions are cut to the part of the clip you actually see on the timeline, without cutting words in half.

- Duplicate speech is merged into one caption.

- Any overlap that is left gets split cleanly.

- Captions saved before the fix are repaired automatically when they load.

And there is a new remove button on every caption. If there is a line you simply do not want, delete it. It stays deleted next time.



## The second fix: audio that was not where we thought

This one is about audio that is detached from its video, or that sits on a connected clip. A common case is sound from a separate recorder, attached to your main clip.


In those projects, the extension could read the positions on your timeline wrongly. In one of our test projects, the detached audio was longer than its video. Only the length of the video was transcribed, and the two sources sat 1.6 seconds apart. The captions drifted out of sync.


Now the positions of nested and connected clips are calculated correctly. A connected clip is measured on its own storyline, instead of being cut to the length of the clip it hangs from. The picture of a video clip is no longer mistaken for an audio source. And audio roles, disabled clips and switched-off audio channels are respected.


Both fixes came from the same place: real projects. We are glad we tested on them one more time.



## Smart Cache: do not start over

Smart Cache remembers, on your Mac, what has already been transcribed.


Picture this. You caption an interview, and you are happy with it. Then the client asks for ten more seconds at the end. You extend the clip on the timeline and hit Analyze again. Only the new, not-yet-transcribed part goes through Whisper. The rest is already there.


Run the same clip again, with the same language and the same model, and the captions come back instantly. That helps while an edit is still changing: try another style, re-run, trim, extend, without starting the caption pass from scratch.


Smart Cache is on by default. There is a switch in the extension if you want it off. The first run of a clip still takes as long as it takes, and that depends on your Mac, your clip and the model. Smart Cache helps with the second run, not the first.



## Fix a caption before it reaches the timeline

Even a good speech model can spell your guest’s name its own way. Now you can correct a name, a punctuation mark or a whole phrase right inside the extension, before the titles land on the timeline.


You can also change each caption’s start and end time. The editor checks your timing as you go. It refuses an invalid range and a caption that overlaps its neighbour, so a small change cannot quietly break the sequence.


Your edits are saved on your Mac. They come back when you open the extension again, or when you analyse the same media again. And, new in 1.1.1, you can remove a caption you do not want.



## Smart Search: where did I say that?

You remember saying something about a lens, but not in which video. Smart Search looks through every caption you have generated, across all your clips. Each result shows the matching text, the file name and the timecode.


Search also sees your corrections. If you fixed a name, the fixed name is the one you can find.


One honest limit: clicking a result does not jump to the clip in Final Cut Pro. You get the file name and the timecode, and you go there yourself.



## About 100 languages, and Auto Detect

Version 1.0 had a picker with 20 languages. The language menu now lists all of the roughly 100 languages in the Whisper model catalogue. At the top there is a new option, Auto Detect. If you are not sure which language is in a clip, or you mix languages across clips, let it decide. Auto Detect runs on your Mac too, after the model download.


Please read this part carefully. That number is the model’s language coverage. We did not test caption quality separately in every language. How accurate the captions are depends on the language, the recording, the speaker and the model. So reviewing your captions stays part of the job, in every language. With the new editor, it is also quicker to do.



## Smaller windows

The extension now fits smaller Final Cut Pro windows, for example on a laptop screen. The project drop area, search and template choices stay reachable.



## What stays the same



- Transcription still runs on your Mac. We use WhisperKit, which is built on OpenAI’s Whisper. Your footage is not uploaded to a cloud transcription service. The speech model is downloaded once, and that needs internet. App Store purchases and subscription checks use the internet too.

- The same five templates. Basic, Highlighted, Highlighted with Background, Pop and Beast Pop. Font, colour and position are still adjustable.

- The same tidy result. Your titles come back grouped in one compound clip in a secondary storyline.

- The same pricing model. The app is free to download and the templates are free. Automatic AI captions need an active monthly subscription. For current pricing, please look at the [Mac App Store page](https://apps.apple.com/app/id6775619373).


## What is not in this update

So you do not have to wonder: 1.1.1 has no SRT or other subtitle-file export, no text-to-speech and no automatic YouTube upload. Search finds words, not pictures or ideas, so there is no visual or semantic search. And, as said above, a search result does not jump to the clip.


We are already working on the next update. We will not promise anything about it here. We would rather tell you when it is ready.



## Get it, watch it, tell us what you think

To update, open the [Mac App Store](https://apps.apple.com/app/id6775619373) and install FCP AI-Toolkit 1.1.1. The App Store page is now available in 10 languages, and it has a short preview video.


To see it at work, watch the [launch video on YouTube](https://www.youtube.com/watch?v=ZvGX2RwCvH8). Our first videos, a launch video and Shorts, are on [YouTube](https://www.youtube.com/@FCPAIToolkit) and on [Instagram](https://www.instagram.com/fcpaitoolkit/) as Reels. We are also on [TikTok](https://www.tiktok.com/@fcpaitoolkit). If you want to read how we got here, the [1.0 post](/blog/fcp-ai-toolkit-1-0/) and the [1.1 preview](/blog/fcp-ai-toolkit-1-1-preview/) are still online.


If something does not work in your project, or you have an idea, write to us at help@fcp-aitoolkit.com. A real project with a real problem is the best test we can get. It is how we found these two bugs.


Thank you for using FCP AI-Toolkit.
