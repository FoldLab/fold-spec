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

## Explicit layer-resolution experiment

Material IDs identify which paper to cut, but do not encode depth. Where
the author requires the frontmost layer, use explicit IDs together with
local above/below relations evaluated from the declared cutting side.
For each positive-length ordered-path patch, the intended ID must cover
it and be provably above all other covering IDs (including transitive
relations). Reject missing coverage, hidden targets, order ties,
out-of-patch identities and contradictory order. No pixel/viewport depth
or ID-based tiebreaker. Exact overlap faces can use the existing layer
witness concepts; do not infer partial overlap from counts, display hints
or geometry sampled at only the segment midpoint.

The added resolver consumes predeclared overlap/path partitions; it does
not construct or certify those partitions, map spec face IDs to stable
material regions, or read an archive. Production integration would
first need a path/face overlay with completeness checks, positive-length
patches, a specified viewing side, and stable lineage through remeshing.
A fold can cross changing stacks, so validation must cover the whole
path, not just the slit tip or a single global face-order array.

### Geometric overlap partition (bounded fixture mode)

For strictly convex ordered polygons of integer XYZ points in one declared
plane, clip the finite segment against each polygon using rational parameters.
Split the path at all coverage and order-witness endpoints. Every positive
length interval is checked by the frontmost-layer resolver. This detects
a shorter layer hiding only the middle of a slit, and rejects unsupported
geometries (noncoplanar/invalid polygons, boundary overlap and isolated
touches), and witnesses extending outside geometric co-coverage. Transverse
boundary crossings, including an entering endpoint, delimit coverage without
making a claim about zero-length intervals. Compare supplied witness
orientation in the same view frame; the experiment does not derive order
from coplanar geometry.

Requires Python 3.10+. Fixture-only: candidate polygon list must be
complete; the experiment does not extract faces from folded documents,
certify physical witnesses, verify that the selected path is a valid
edge-to-interior cut, remesh, or implement the turtle. Turtle remains a
requirements case, not a geometry fixture.
