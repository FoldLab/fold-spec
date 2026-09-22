# 13 · Diagrams, print and cut-out templates

**Normative for `print-1`**

Instruction diagrams are views of the same physical sequence, not screenshots of controls. `print.panels` names steps and normalized sample points in each step’s movement ranges. Map the step’s concatenated run intervals proportionally to their movement durations; do not include reading waits in the sample coordinate. Samples of a non-geometric check use the preceding physical state.

## Panel content

A panel includes its ordinal, title, canonical text, meaningful paper outlines, current crease/movement indication and any necessary close-up. Before/during/after samples should be chosen to explain the action. Complex coupled movements can occupy multiple teaching panels without inventing independent physical operations.

Hide occluded lines in ordinary diagrams; show hidden edges only when deliberately styled and labelled. Suppress mesh triangulation edges that are not instructional creases. Keep vector paths and native text when the output format allows them. A bitmap preview is not a substitute for readable print typography.

`includeFinalPanel` defaults to the author’s explicit value, normally true. The final panel uses the completed static display state and orientation, independent of where the user paused playback. It includes required display/check text. Flourishes and cinematic stage travel are never additional real-world folding instructions.

For text-only content, publish the actual copy and proposed final guidance. Label a missing final illustration; do not use a blank sheet or another model to fill the space.

## Physical-size paper

An optional template provides `sizeMm`, `sides`, `includePattern`, `includeGuides`, and the guide convention. A 6 × 6 inch square is **152.4 × 152.4 mm**, not 150 × 150 mm. At 72 points per inch its cut width and height are 432 points. Printing at “fit to page” can invalidate these dimensions; include actual-size instructions and a calibration mark.

Changing template size does not rescale canonical model geometry or automatically promise that a different aspect ratio produces the same model. When preserving an authored rectangular model, preserve its aspect ratio or disclose the template mismatch. Print margins, nonprintable regions, tiling and duplex alignment remain output/device constraints.

## Guide styling and reverse side

The core template convention is `mountain-solid-valley-dashed`. Always print a legend because other diagram traditions may use different symbols. Guides are subtle enough to keep printed patterns readable but must not rely on color alone. An active instruction guide may be stronger in screen views; that preference is separate from the physical template.

For a back-side template, use the same material coordinates with the explicit viewing mirror. The visible mountain/valley interpretation reverses with the viewed side, while the stored original-front assignment does not change. Do not apply both a renderer mirror and a second layout mirror unintentionally.

Historical crease events can reverse assignment during a sequence. A static template is a location/assignment guide at a specified instructional state, not a claim that every line should be folded simultaneously. Writers SHOULD explain this limitation when a model contains reversals.

## Output settings and accessibility

Support model appearance, explicit export-only overrides, monochrome/ink-saving output and optional patterns. The preview and file output must use the same effective material settings. A light/dark application theme must not silently invert the printed page.

Semantic HTML and plain text are valid accessible alternatives. A PDF containing selectable text is not automatically a tagged accessible PDF. A reader claiming accessible PDF output must validate structure, reading order and assistive-technology behavior separately.

The format is renderer-independent. An application may implement these contracts with its existing PDF component pipeline; this repository does not bundle or certify a particular PDF runtime.
