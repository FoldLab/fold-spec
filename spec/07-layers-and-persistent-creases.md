# 07 · Layers, sides and persistent creases

**Normative for `playback-1` and `print-1`**

## Physical ordering versus display tie-breaking

A global face rank cannot describe every folded configuration. Ordering can be local to an overlap patch, can change over time, and must not be inferred merely from triangle draw order.

An operation MAY supply `layers` relations. Each relation names two faces, progress `at`, a unit `normal`, `planeOffsetMm`, and an `overlapMm` polygon. The first face lies above the second along +normal within that coplanar patch. No relation is implied outside the patch or at another progress.

The patch plane is `normal·p = planeOffsetMm`. Its origin is `planeOffsetMm*normal`. Choose the projected +X direction as u unless `abs(normal.x)>0.9`, in which case use projected +Y; normalize it. Let v=`normal×u`. `overlapMm` coordinates use this u/v basis. This deterministic basis prevents two readers interpreting the same local polygon in different planes.

A validator for local layers checks the face references, unit normal, planar overlap, patch containment, no self-relations and no contradictory cycles within the same patch/state. It must not reject legitimate relationships in distinct spatial patches merely because a global graph cycles. The current reference tool checks references and normals, not a complete planar arrangement proof; see implementation status.

## Optional coplanar hints

`layerHint` is explicitly **rendering-only**: a unit axis and ranks matching mesh-face order. It gives tie-breaking priorities only for nearly coplanar overlapping surfaces whose normals are compatible with that axis. Larger rank means nearer +axis. Viewing from the opposite side reverses the tie-break. Equal ranks require a stable face-ID tie-break.

Hints MUST NOT override an actual geometric depth difference larger than the declared coplanar tolerance, move vertices, authorize a tuck, or replace local physical relationships. They are useful for legacy demonstration meshes, including the crane example, but are not a contact certificate.

For a hinge with start/end hints, the reader uses the start hint before normalized eased progress 0.5 and the end hint from 0.5 onward. This discrete hint handoff must occur away from ambiguous coplanar contact; the physical geometry is unchanged. For sampled operations use the preceding key’s hint for an interval, the final key’s hint at the endpoint. Writers must ensure state-boundary hints remain consistent; full-surface color swaps are defects.

## Persistent crease events

`creases` records material segments, an ID, original-face assignment and `establishedAt` in operation progress. Once established, a crease remains in material history after unfolding. A fold being inspected before its endpoint may show its active hinge as a preview; that is not a completed historical crease yet.

An event reusing a crease ID updates its assignment only for the same sheet/material segment. It cannot repurpose the identity for another location. A later inversion may change a crease’s mountain/valley assignment. Readers should distinguish historical assignment from its current flat/nonflat state.

The active guide is more prominent than historical guides. Guides are mapped through the current material embedding and split at every intersected face boundary. Ordinary views hide occluded portions; X-ray may expose them. They do not remain as unmoving screen-space lines when the paper turns.

## Mountain/valley semantics

Assignment is relative to the **original material front**, not the camera or whichever side currently faces the folder. At a consistently oriented mesh edge A→B, let left/right refer to material XY. With current hinge tangent t and oriented face normals nL/nR, a compatible signed bend is:

```text
phi = atan2(t · (nR × nL), nL · nR)
```

With these conventions positive bend is valley and negative bend is mountain. At exact zero or 180 degrees, the cross product alone does not identify the branch; preserve the authored transition/sign. This is different from a hinge’s directed rotation parameter, which also depends on which side moves.

For guide export, do not treat every triangulation diagonal as a crease. Printed mountain/valley styling is defined in chapter 13 and must include its legend.
