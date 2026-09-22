# Implementing a player

**Informative integration guide.** This repository supplies data contracts and a limited reference toolchain, not a complete UI renderer.

## Load in stages

Validate bytes/JSON first, then schema, identities and references, supported capabilities, assets, material topology, operation boundaries, and trajectory strain. Decode images/media in a bounded platform subsystem only after preflight. Never fetch an imported URL simply because it exists in metadata.

Discover the status before opening a canvas. Planned content shows metadata. Text-ready content shows instructions. Partial geometry can play only its declared resolved prefix. Fully resolved geometry still carries independent accessibility and physical-review limitations.

## Compile once, sample many times

Create immutable operation and mesh indexes. For an instruction run, map its local progress into the referenced operation range. Multiple runs are weighted by their active durations. Holds and user waiting are separate. The reference `presentation.sample_step` demonstrates this physical-time mapping.

Use the resolved hinge axis/direction, not the decorative valley/mountain label, to rotate vertices. Move a shared material vertex consistently across all incident faces. An unfold can use a reverse hinge or an explicit path; it retains crease history. A sampled operation interpolates its supplied positions linearly with no second undocumented ease.

## Timing controller

Use a single state machine: idle, folding, narration-wait, inter-step-wait, manual-confirmation, paused, final-display and flourish. Author durations scale with animation speed. A custom five-second reading wait stays five wall-clock seconds. Pause freezes it; replacing the selected model or seeking invalidates stale completion tokens.

A selected operation is a stable ID, not an array index remembered forever. When a step is subdivided, maintain a documented mapping for progress/bookmarks and invalidate narration whose transcript no longer matches. Automatic playback does not take focus away from a user typing in a control.

## Material and layer identity

UVs derive from original millimeter coordinates, not triangle-local positions. Determine front/back from oriented geometry. Opaque realistic rendering is distinct from an explicit X-ray view. Resolve coincident faces with region-aware order; do not shift each face arbitrarily in global Z to conceal a priority bug.

Crease guides live in material space, mapped to the current mesh. Separate established creases from active emphasis and unmade future lines. Clip guides behind real layers in normal views; X-ray may reveal them. Preserve parent priorities at remesh boundaries and curved-strip subdivisions.

## Final presentation

First complete physical finishing operations. Then obtain the static completed pose. Apply a decorative rig/root flourish only during its optional phase and return exactly to the static pose. `tools/presentation.py` demonstrates deterministic final and flourish sampling; it does not implement scene travel, rendering or paper response.

For print and thumbnails, use the static pose, not the viewer's current animation time. Do not hide an unauthored cup opening by replacing the final mesh. A text-only model may contain proposed display guidance without a simulated object.

## Rendering and interaction

A practical client can use Three.js or another 3D engine, native renderers, or a CPU fallback. Update geometry outside the framework's state-diff path, render on demand when paused, and limit concurrent thumbnail contexts. Cache by relevant geometry/material/static-camera revisions and renderer version, not just model title.

Expose keyboard inspection alternatives, reset-to-best-view, text/animation switching with a shared selected step, contrast/font controls and explicit narration controls. Keep model colors, viewer overrides and print overrides separate.

## Testing boundaries

Test beginning, intermediate, near-end, exact-end and next-start states in both directions. Check complex remeshing, turnovers and folds after rigid transforms. Compare ordinary rendering and printed diagrams, camera motion and fixed-view geometry, text transcripts and final stills. Use actual browser/download/media tests in addition to mathematical sampling. Test self-contact and real paper separately; the reference validator does not certify them.
