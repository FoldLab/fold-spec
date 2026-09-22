# 08 · Instructions, substeps and playback

**Normative for `text-1` and `playback-1`**

## One canonical lesson

`instructions.steps` is the ordered user lesson. Every step has a stable ID, localized title/body, semantic kind, animation availability, zero or more `runs`, a reading pause, and tactile guidance. The body is the primary action in Animation, Text, narration and print views. Supplementary descriptions must not define an incompatible second recipe.

A `run` names one geometric operation and an increasing `[from,to]` interval. Flattening runs across steps must cover every resolved operation, in operation order, from 0 to 1 exactly once with no gaps, overlap, or accidental repeat. A check/setup step can have no run. Multiple successive runs in a teaching step are allowed, but a novice-oriented writer SHOULD keep each physical instruction focused.

Groups provide headings and related `stepIds`; they do not change playback order. Group membership is not an implicit loop or a command to repeat a fold.

## Subdividing a coupled operation

A square-base collapse can remain one mechanically coupled trajectory while several teaching steps cover `[0,0.18]`, `[0.18,0.55]`, `[0.55,0.88]`, and `[0.88,1]`. A separate check follows with no motion. This is the crane example’s deliberate teaching decomposition, not a claim that the panels fold independently.

Boundary choices should correspond to meaningful paper landmarks and states. Splitting a clip into equal time slices alone does not improve instructions. After subdivision, source mappings, narration references, progress bookmarks and print panels must be updated. Re-running a generator must not subdivide already segmented steps again.

## Canonical time and elapsed time

Geometry time is deterministic and seekable. Human waiting and audio loading are not extra geometric motion. A run’s nominal movement duration is its normalized range length multiplied by the operation duration. Playback speed scales advancement through that range, not the model’s dimensions or positions.

After a step’s motion (and any opted-in available narration), its `pauseAfterMs` is a real-time reading wait. A user override replaces, rather than adds to, this default. At 2× folding speed a 5,000 ms reading wait remains five seconds. A pressing movement that is part of the physical operation must not be deleted because the reader sets waiting to zero.

## Controller states

The minimum conceptual states are ready, moving, awaiting-narration, timed-wait, awaiting-confirmation, presenting, paused, complete and error. Applications may implement them differently, but must preserve these effects:

1. Pause freezes the current motion, wait countdown or presentation progress.
2. A user action to continue skips only the current wait/confirmation, not a required fold.
3. Manual progression takes precedence over automatic advancement.
4. Seeking, changing model/revision, or replaying a step cancels obsolete waits/audio callbacks.
5. Failed or absent optional audio never deadlocks the lesson.
6. At the last required instruction, no phantom next step is created.
7. A final flourish is a separate optional phase, not another construction step.

Use an epoch/generation token or equivalent cancellation mechanism so a completed timeout from a previous step cannot advance the current lesson. Zero-duration waits must transition immediately and clear their state. Do not implement waits through accumulating render-frame counts.

## Text mode and accessibility

Switching between Animation and Text preserves the selected step and any meaningful within-step progress. The text remains usable when geometry is unsupported. Manual navigation can focus the newly committed heading; automatic playback must not steal keyboard focus on every frame.

Announce step changes and waiting state selectively, not every countdown tick. An implementation may expose an explicit “read each step” feature, but no audio or decorative animation starts just because a file is opened.
