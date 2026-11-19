# Finite selected-layer slit: research spike

Not a format change, validator, runtime feature, or completed turtle. Run
`cd research/finite-slit && python -m unittest -v`.

**Why not patch the fold guard directly:** Web `src/core/engine.ts` keys
`conformMaterialEdges` and `assertNoTear` by a hash of material coordinates.
The former even inserts matching points into unsplit edges. A scissor marker or
an exception to tearing would either re-weld slit banks or leave other
continuity checks, mesh motion and layer transport inconsistent. The reference
fold-spec validator advertises rectangular disk topology, and its operation
boundary checks compare a single material mapping. Two legitimate positions for
one slit-bank coordinate violate that assumption even though the area and
outline at the instant of cutting are unchanged.

**Smallest useful contract:** capability-gated zero-kerf edge-to-interior
straight cut in a flat state, no removal, no through-stack cuts, no intersections
with previous cuts. Resolve the chosen frontmost flap to an explicit face chain
and stable material endpoints. Require ordered contiguous coverage from an
existing free edge to an interior stop, exclude all other faces even at equal
projected positions, and reject ambiguities instead of cutting all coplanar
layers. Remesh at the segment (including stop), preserve area and the transform
on all points immediately across the cut event. Maintain source material UVs
separately from welded-corner identities. Weld incident face corners only via
uncut shared edges. Both mouth banks separate, but the terminal fan remains
connected. Generate/persist IDs deterministically. No slit segment is a crease.

The prototype checks the corner-equivalence rule on pre-conformed fixtures
only; it deliberately does not resolve selection, project a slit, validate
path shape, or remesh. The triangle fixture demonstrates a following hinge
whose moving bank would be rejected as tearing without a real cut. Another
sheet region with matching projected coverage remains internally welded.
Production acceptance still needs tests for ambiguity, overrun, no cut beyond
the finite stop, unaffected layers within the same original sheet, independent
left/right folds, area, midpoint rendering, print/accessibility description,
undo/redo and archive round-trip. For existing lessons, require unchanged
semantic checks and sampled geometry across the corpus. Unknown cut capability
must fail closed or be explicitly reported unsupported, never fall back to a
no-op `manual` step.
