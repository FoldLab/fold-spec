# 09 · Accessibility and text-only copy

**Normative for `text-1`; additional UI requirements for `accessible-viewer-1`**

A text representation is a first-class view of the same origami, not an alternative “disabled-user library.” Users may choose words, diagrams, animation, narration, or a combination. A reader must not require a canvas to reach the primary instructions.

## Nonvisual copy model

Document-level `accessibility` defines `referenceFrame: "folder-table"`, setup statements, landmarks, review state and known limitations. Landmarks can have a stable material location `uvMm`, a name, and a nonvisual description. A name alone is insufficient when the user cannot locate it by touch.

Every step includes `tactile`:

| Member | Authoring rule |
|---|---|
| `orientation` | Identify the current near/far/left/right arrangement without relying on the camera. |
| `locate` | Explain how to find the specific edge, point, layer or pocket. |
| `check` | State what a successful result feels like or otherwise reveals. |
| `recovery` | Give a safe way to undo/reorient when the check fails. |
| `landmarkIds` | Link to existing document landmarks, never invented renderer vertices. |
| `review` | Mark draft, authored, or tested and retain evidence for tested claims. |

Lists may be empty when a truthful check is not yet known. A migration MUST NOT invent a tactile assertion merely to populate a field. “Authored” means someone supplied copy; it does not mean a blind user validated it. Tested claims require nonblank evidence, but that evidence is still an author’s claim, not a signature or platform certification.

## Example of aligned primary and detailed copy

Primary: “Lift only the upper layer at the far point and bring it to the middle of the near edge.”

Locate: “At the far corner, slide a finger between the two layers. Keep the lower layer on the table.”

Check: “One point remains at the far corner; the moved point meets the near edge’s midpoint.”

The detailed copy adds locating/checking information without instructing a different fold. Colors can reinforce a named side, but “move the red piece” is not a sufficient primary instruction. A reference like “left” is always the folder’s left in the stated orientation, not the camera’s current left.

## Text-only and planned records

An `instructions` document contains real canonical copy and no geometry. Physical steps have `animation: "not-authored"`; setup/check steps can be `not-applicable`. An `authoring` recipe alone does not make it animated. Text-only records may include **proposed** final display/flourish guidance, explicitly unavailable as animation.

A `planned` record contains no procedure. Its UI can show known metadata, sources and missing work, but must not manufacture steps or a completed illustration. The machine status remains distinguishable from an actual text lesson.

## Viewer controls

An accessible viewer provides keyboard-accessible step selection, previous/next, pause/replay, descriptive-copy toggle, high contrast, plain background, text size/spacing, reduced motion, and an understandable focus order. Controls expose accessible names and state. Pointer-only camera gestures must have keyboard/button alternatives; Text mode must not require the user to operate the camera.

Honor user/system motion and contrast preferences. A dyslexia-oriented typeface may be offered as a preference, with honest fallback when unavailable; no font is mandated by the file format and no font universally establishes reading accessibility. No font binaries are embedded by this specification repository.

UI themes, high-contrast colors and temporary outlines are user preferences, not a mutation of model materials. Narration controls remain explicit and separate from screen-reader announcements. Avoid duplicate utterances and focus stealing during automatic playback.

The WCAG 2.2 framework is a useful web implementation target [R1], but conforming data alone cannot prove an entire application conforms. Test actual assistive technology, large text/reflow, forced colors, keyboard-only operation and user comprehension. A schema test is not a substitute.

[R1]: https://www.w3.org/TR/WCAG22/
