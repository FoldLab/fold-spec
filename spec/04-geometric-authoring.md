# 04 · Typed geometric authoring

**Normative for `construction-1`**

`authoring` preserves why a fold exists. `geometry` preserves the resolved operation used for playback. They are complementary, not interchangeable. Playback uses resolved data; changing authoring geometry invalidates its compiled bindings until they are recomputed and checked.

## Construction frames

A frame names a sheet, an `afterOperation` (or `null` for the initial flat state), an `originMm`, and perpendicular unit vectors `u` and `v`. Its positive normal is `u × v`. Coordinates in a frame are millimeters projected onto this plane.

A material point is mapped through the named sheet state before projection. It must lie in the construction plane within the document position tolerance. A folded material line that has become a bent polyline cannot be treated as one straight line unless its complete mapped segment is straight within tolerance. A solver MUST reject nonplanar inputs rather than flatten them silently.

A frame does not mutate paper orientation. Repositioning the model is a separate physical operation; moving a camera changes neither frame nor material identity.

## Points

Every point has `id`, `frame`, and a typed `definition`:

| Kind | Meaning |
|---|---|
| `material` | A named position `uvMm` on an original sheet, evaluated in the frame’s named state. |
| `literal` | Explicit `xyMm` in this construction plane; not automatically a point on the paper. |
| `midpoint` | `(a+b)/2` for two points in this frame. |
| `ratio` | `a + (numerator/denominator)*(b-a)`; denominator positive and numerator between 0 and denominator. |
| `intersection` | The unique intersection of two nonparallel lines in the frame. |

Keep rational intent as numerator/denominator; implementations may resolve it numerically under the tolerance policy. A ratio representation alone does not turn every downstream floating-point computation into exact arithmetic.

## Lines

Line definitions are `through`, `perpendicular`, `angle`, or `alignment`. All dependencies use the same construction frame. `angle` rotates an existing line’s direction by `angleDeg` in the positive frame orientation, then passes it through a named point.

Resolved lines use a unit normal and offset: `n · x = d`. Canonical orientation chooses `n.y > 0`, or when n.y is zero, `n.x >= 0`. A canonical normal only normalizes naming; it does not decide which paper moves or whether the fold is a mountain or valley.

An `alignment` uses one of the seven constraint families in chapter 05 plus a branch-selection policy. The solver must preserve the selected solution and provide diagnostics when it ceases to satisfy the construction.

## Regions and layer selection

A region is a polygon, a half-plane chosen by a point strictly off its boundary, or a finite union/intersection/difference/xor of prior regions. Region operations apply to sets in the stated construction plane; boundary points are retained as shared boundaries. To select paper, map each original material location through the frame's named pose and test its planar membership. This is a preimage in the material domain, not a direct comparison between original UVs and unrelated plane coordinates. Selected material must lie in the construction plane within tolerance; the core planar authoring compiler must not flatten an out-of-plane selection.

Where several coplanar layers occupy the same region, plane membership selects all of them by default. An intent may supply `materialFilter`: an array of simple polygons in **original material millimeters**. Their union intersects the plane-region preimage, allowing a specific original flap to be selected even when it overlaps another layer. Filter polygons must lie inside the sheet and must not self-intersect. Omitting the filter means no additional material restriction.

Region selection is not an instruction to duplicate paper or detach a flap. The compiler freezes the resulting `movingFaces` in the resolved mesh and checks every shared moving/stationary vertex against the actual hinge. A geometric region may identify material that currently lies below another layer; screen-space clicking must not replace that identity.

If an intended region divides an existing face, the compiler must create a conforming mesh revision before the motion begins and prove the starting pose is unchanged. A display-layer rank does not define selection. General pocket insertion between named surfaces requires an explicit operation/constraint extension; a half-plane expression alone does not solve it.

## Intents and dependency checking

An intent records sheet, crease line, moving region, signed rotation, duration, and `resolvedOperations`. The crease normal is canonicalized as described above. In plane coordinates its directed tangent is `(-n.y,n.x)`. The 3D axis passes through `origin + u*(d*n.x) + v*(d*n.y)` and points along `u*(-n.y) + v*n.x`. `rotationDeg` is right-handed about **that** direction. This rule prevents two compilers choosing opposite fold paths from the same undirected line. A resolved hinge may use a reversed numerical axis only when its angle is also negated.

Empty bindings mean not compiled. Nonempty bindings are promises that the associated operations implement that intent; a construction-conforming writer must check the residuals and selections.

Cycles, cross-type references, dangling names and accidental frame crossings are errors. Forward references are allowed if the complete graph is acyclic. The compiler topologically orders dependencies; the serialized `geometry.operations` still defines physical execution order.

The crane example binds the first two diagonal precreases to explicit authoring relationships; it does not pretend that the rest of its complex 3D demonstration is already expressed as a symbolic constraint program.
