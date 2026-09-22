# 12 · Paper response and rendering fidelity

**Normative where the presentation feature is supported**

`stage.paperResponse` is an art-directed enhancement, not calibrated elasticity. It contains `enabled`, `bendWidthMm`, `settleDeg`, `damping`, and `cycles`. Suggested values are 3.4 mm, 1.8 degrees, 6 and 1.5 respectively. Geometry endpoints and source topology remain authoritative.

## Bounded settling

For a simple hinge with total nonzero angle A and normalized t, let `s=t²(3−2t)`, `a=min(settleDeg/abs(A),0.15)`, d=damping and c=cycles. A deterministic permitted settling parameter is:

```text
q(t) = clamp(s - a*sin(pi*t)^2*exp(-d*t)*sin(2*pi*c*t), 0, 1)
angle(t) = A*q(t)
```

The response stays between the authored endpoints. Disable it for reduced motion. An inverse/unfold should traverse the corresponding stored bend in reverse, not start a new artificial flat sheet. An implementation that does not implement this response may show canonical motion and disclose the missing presentation feature.

## Rounded creases

A rounded display strip may use a bounded developable bend around the existing hinge. Its width vanishes at endpoints, shared hinge points stay shared, texture coordinates stay material-attached, and displacement must not cross the declared final angle. Strip tessellation is temporary rendering geometry, never new source creases.

This draft standardizes the response parameters and invariants, not a unique shader or exact subpixel strip tessellation. A reader must not claim pixel-identical realism across renderers. Coupled sampled clips retain their authored trajectories; do not distort them indiscriminately with a global “elastic” field.

## Visibility requirements

Realistic surfaces are opaque and consistently wound. Front/back images follow the original material face. Coplanar priority is a bounded depth tie-break, not physical displacement. A completed fold must not swap visible colors simply because the reader switches from interpolated positions to the stored endpoint.

When remeshing, carry material ancestry/visibility consistently into the first state. A crease strip inherits its parent’s priority. Real geometric depth wins when surfaces are separated. X-ray is a separate inspect mode; it should offer outlines or a deliberate translucent fill while leaving the actual paper together.

Texture, restrained matte lighting, thin boundary rims and soft contact shadows provide paper cues. Bloom, glass-like transmission, rubbery overshoot, or gaps between connected faces are not substitutes for correct geometry. High contrast and a plain backdrop must remain available when scenery obscures the paper.

## Renderer audits

Test near-end and exact-end states, next-operation starts, reverse seeking, opposite viewing directions, turning over, remeshing, paper response on/off and final-presentation boundaries. Use distinctly different face colors during testing so a large layer swap is obvious. Keep canonical double-precision source separate from uploaded float32 GPU buffers.

The reference repository’s geometry validation does not test GPU materials, shadows or pixel visibility. Engine authors should add renderer-specific tests and actual browser/device checks. See [implementation guide](../docs/implementing-a-player.md).
