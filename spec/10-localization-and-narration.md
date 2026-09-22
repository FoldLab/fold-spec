# 10 · Localization and narration

**Normative**

## Localized text

Localized fields map language tags to plain strings. `defaultLocale` MUST be present in every localized field. Tags follow BCP 47 conventions [R1]; the bundled schema checks a bounded syntax subset, not the entire IANA registry. Case-colliding tags such as `en` and `EN` in one map are rejected.

Lookup order is the requested tag, progressively less specific tags, then the default locale. Display the actual language of a fallback span; do not label English text as Japanese because the user requested Japanese. Structural IDs and geometry do not change between translations. If a physical instruction differs, it is not merely a translation and needs a new semantic revision.

Plain text is not HTML, JavaScript, SSML, or a template expression. A reader escapes strings on HTML export. Explicit narration pronunciation hints are data, not executable speech markup.

## Narration entries

A narration record names an ID, step, locale, primary/descriptive variant, status, exact transcript, and `textSha256`. Its hash is SHA-256 over the transcript’s **exact UTF-8 bytes** without silently normalizing Unicode or whitespace.

`status` values:

* `missing`: no recorded asset exists; show useful player placeholders, not fake playback.
* `ready`: exactly one local `asset` or HTTPS `url` is present.
* `stale`: the transcript/content changed and audio needs regeneration; do not auto-play it as current.

Primary ready narration must match the step body in the same locale. Descriptive narration may combine canonical copy with the step’s tactile details; an editor must maintain that correspondence and review it after changes. Optional `pronunciations` records pair written and spoken forms without injecting SSML or code.

`durationMs` is optional until measured. The reader uses actual media progress when available and must not fabricate a duration for missing media. A step can refer to its narration IDs, but all references must resolve to entries for that same step. Missing optional audio does not remove the transcript.

## Hosting and security

A local narration asset must be declared with its media type, license, size and digest. A remote narration URL is optional network content and requires user/application policy before requesting it. Do not issue HEAD, preload or analytics requests merely while validating a document. Block credentials in URLs, non-HTTPS schemes and unsafe redirect targets; server fetchers additionally enforce SSRF defenses.

The file is provider-independent. It contains no API keys, paid-generation instructions, secrets, or requirement to contact a particular generation service. Audio creation and hosting are outside the core format.

## Playback lifecycle

No audio auto-starts on open. Explicit play may load the current clip; a separately enabled follow-step option may play subsequent clips after user activation. Pause/stop/cancel must work independently of model geometry. Changing model, revision, step, language, view or transcript invalidates obsolete audio jobs. Completion events from an older generation cannot advance the current tutorial.

When following narration, finish the physical movement and available narration before beginning the reading wait. Expose a user way to continue without failed audio. Manual confirmation remains authoritative. Avoid narration and screen-reader live regions speaking identical text simultaneously.

Text export remains complete when audio is missing. A tagged accessible PDF is a separate output capability and is not proven by having transcripts in JSON.

[R1]: https://www.rfc-editor.org/rfc/rfc5646
