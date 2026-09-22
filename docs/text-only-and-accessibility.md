# Text-only lessons and accessible instruction

**Informative authoring guide.** The normative contract is [chapter 09](../spec/09-accessibility-and-text-only.md).

A lesson does not need animation to be useful. It needs accurate actions, stable orientation and honest status. Use `status: "instructions"` with `animation: "not-authored"` on physical actions. Do not add empty geometry or a rotating completed model merely to make the file look animated.

## One action, supplementary detail

The primary `body` is the same instruction in visual playback, text mode, transcript and print. The `tactile` object adds context, not a different recipe.

| Field | Authoring question |
|---|---|
| `orientation` | Which edge or point is nearest the folder, and which side is up? |
| `locate` | How can the relevant point, crease, pocket or layer be found without seeing it? |
| `check` | What result can the learner verify by touch or alignment? |
| `recovery` | What safe previous state can the learner return to if the result does not match? |
| `landmarkIds` | Which stable named landmarks are referenced? |
| `review` | Is this draft copy, authored guidance or user-tested content? |

For example, “fold it like the picture” is insufficient. A better instruction identifies the moving layer and destination: “Bring only the upper near point to the far point; leave the lower layers on the table.” Useful checking might state that another point remains at the near edge—but only if that is true of this model.

## Stable orientation

Near/far and left/right are relative to the folder's work surface. A camera orbit does not turn the person's paper. A true turnover is a physical action and should say how to retain the intended near edge. Color names are optional aids; Side A/Side B and tactile construction features carry the instruction independently.

## Uncertainty and user testing

Do not fill all touch-check arrays with confident invented descriptions. Empty arrays plus an explicit limitation are better than false guidance. `review.status: "tested"` requires evidence text, but the parser cannot authenticate that evidence. Retest when changing the sequence or moving layer.

The examples in this repository have not been tested with blind folders, NVDA or VoiceOver. Their semantic HTML output can support assistive technologies, but is not an accessibility certification. A consumer still needs correct landmarks, focus handling, labels, keyboard access, zoom/reflow, contrast and reduced-motion behavior.

## Personal controls

A player should offer text size, spacing, readable/local dyslexia-friendly font selection, high contrast, plain backdrops, outlines and motion reduction. Keep these as personal overrides, not edits to original paper colors or exported diagrams. Never silently substitute a requested unavailable font while claiming it is active. No font binaries are distributed here.

## Audio is optional

A missing clip leaves text usable. Read-aloud begins only on explicit user choice; advancing steps cancels obsolete audio and avoids double narration from live regions. The file can record a transcript and hash before audio exists. A provider-specific generation workflow does not belong in the trusted document interpreter.

The [minimal lesson](../examples/minimal-text/first-fold.fold.json) and [crane text counterpart](../examples/crane/crane-text.fold.json) are complete structured examples. Their generated HTML is script-free and keeps actual language tags on fallback copy.
