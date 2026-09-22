# 11 · Final presentation and artistic stage

**Normative for `presentation-1`**

## Three separate concepts

**Finishing** is physical construction: opening a cup, setting a wing, closing a flap, or gently shaping a body. Required finishing actions must already occur in the instructional sequence, with geometry when the document claims them resolved.

**Display** is the stable final pose and camera. `presentation.display.afterOperation` names the last resolved physical operation. Its orientation and checks describe the completed object. A printout uses this pose, never the current animation frame.

**Flourish** is a short decorative animation after construction. It is not a new fold, does not change the saved final state, and must return to that exact rest pose. Text-only/planned records may describe a proposed flourish without claiming geometry exists.

## Root flourishes

Core root kinds are `none`, `tip`, `bow`, and `turn`. A resolved nonempty root flourish records a nonzero directed `axisMm`, amplitude, integer cycle count, and duration. For normalized t and N cycles:

```text
envelope(t) = sin(pi*t)^2
angle(t)    = amplitudeDeg * envelope(t) * sin(2*pi*N*t)
```

Apply this right-handed rotation to the completed model about the declared axis. The named kind communicates intent to the author/UI; the numerical motion is the same bounded formula. `turn` in this core is a restrained swivel, not an implicit 360-degree spin. A different motion curve requires an extension or explicit stage path.

At t=0 and t=1 both angle and endpoint velocity are zero. The exact stored final state is selected at either endpoint to avoid floating-point accumulation. Pause/scrub sample this same function. Reduced-motion mode shows the static display pose without the flourish.

## Bilateral wing rig

A `bilateral-hinge` rig names the sheet/final operation, axis, and unit partition normal perpendicular to the axis. No face may cross the partition plane away from the hinge. Shared vertices belonging to both sides must lie on the hinge. There must be paper on both sides.

For `flutter`, the two sides rotate with opposite signs about that one axis using the bounded flourish function. A shared material vertex receives one position regardless of its incident faces. No centroid-based independent triangle motion is allowed. The calibration example is intentionally a two-panel sheet, not a fabricated butterfly design.

A style cannot invent wings on an unrigged cup. Runtime missing-rig handling must disable the flutter with an explicit status, not silently use root rotation as if it were the intended local motion.

## Stage and composition order

The optional `stage` contains a declared background asset, root path keys, camera, model scale and paper response. Its key coordinates are **millimeters in the fixed stage frame**, not camera-dependent CSS offsets. Key rotations are degrees about X then Y then Z, composed as `Rz*Ry*Rx`. Interpolate each Euler component with smoothstep between keys, preserving the written rotation branch; the core limits values to prevent unbounded spins.

Composition order is:

1. Sample canonical instruction geometry (or the completed display state).
2. Apply eligible hinge paper response during instruction playback only.
3. Apply a final local rig flourish when in the presentation phase.
4. Apply final root flourish once.
5. Apply stage root rotation, uniform scale about the origin, then stage translation.
6. Project through the active presentation/inspection camera.

Only one model flourish runs: Artistic mode must not apply a second wing oscillation on top of the final-presentation flutter. A static background does not rotate with paper inspection. The base image is optional; omission uses the reader’s neutral backdrop. Preset names are not required resources.

## User experience and printing

Offer show-final, play/replay flourish, pause, skip and return-to-instructions controls. A playthrough may run its final flourish once, subject to the user’s motion preference. A text reader never has to wait through it. End-of-lesson looping is explicit, not automatic forever.

Printing excludes decorative root travel and flourishes. It includes all required physical finishing steps and, by default, one static final-presentation panel. The final panel can be disabled through an output preference. Proposed presentation text may be printed when geometry is unavailable, but no unrelated model image may be substituted.
