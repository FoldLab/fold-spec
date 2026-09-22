# 06 · Resolved geometry and motion

**Normative for `playback-1`**

`geometry.meshes` describes material topology; `geometry.operations` is the physical execution order. Each operation acts on one sheet using a named mesh. Source meshes and motion keys are required data, not disposable render caches.

## Material mesh contract

Core meshes triangulate an entire original rectangular sheet exactly once. Each triangle is counterclockwise in material XY. Edges have one boundary incident face or two oppositely directed incident faces; the only boundary is the original rectangle. There are no slits, glued seams, disconnected islands or duplicated coincident material particles in this profile.

Every vertex must be used, every face must be nondegenerate, and all material points must lie within the sheet. The material graph must be a connected manifold disk. A compiler must not confuse display tessellation edges with instructional creases. Different operations may use different conforming triangulations if their boundary states agree.

## Hinge operation

A `hinge` carries `startPositionsMm`, directed `axisMm: [A,B]`, explicit `movingFaces`, `angleDeg`, easing and duration. All vertices incident to a moving face rotate by the signed right-handed angle about A→B. A vertex shared with stationary paper must lie on the hinge within position tolerance. It receives one position, not independently computed disconnected face positions.

The core angle is a **delta from the supplied start pose**, not an intrinsic mountain/valley dihedral. Positive/negative rotation depends on the directed axis. `angleDeg` cannot be zero; a whole-sheet motion is `rigid`, not a hinge with no stationary paper.

For progress t, linear easing uses t; smoothstep uses `s=t²(3−2t)`. Apply Rodrigues’ rotation with `angleDeg*s`. The endpoint is computed directly from the start pose, never accumulated by integrating frames.

## Rigid handling operation

A `rigid` operation moves the entire named sheet/model state. It has the same axis and easing, a translation vector and nonnegative `liftMm`:

```text
p(t) = rotate(startPosition, A, B, angle*s)
       + translationMm*s + [0,0,liftMm*sin(pi*s)]
```

This distinguishes turning paper over from moving the camera. `liftMm` is an authored path parameter, not an automatic clearance guarantee; validate clearance against the current geometry when it matters. A 180-degree turn explicitly records its axis and signed direction. Quaternion shortest-path interpolation must not choose the direction on the author’s behalf.

## Sampled coupled operation

A `sampled` operation has a fixed mesh, increasing keyframes from `at:0` to `at:1`, an exact position for each shared material vertex at every key, linear interpolation, and a declared edge-error budget. The key times already encode the trajectory’s pacing. Do not apply a second global easing to a sampled clip.

Between adjacent keys, linearly interpolate shared vertices. For an edge vector `e(s)=a+s*b`, squared length is quadratic. Its interior minimum occurs at `clamp(-dot(a,b)/dot(b,b),0,1)` when b is nonzero; its maximum is at an endpoint. Checking those values against the original material edge length bounds **the complete interpolation interval**, not just a few sampled frames.

The per-operation budget cannot exceed the document’s relative-edge tolerance. Dense rigid snapshots alone do not make interpolation rigid. A writer should refine sampling or use analytic operations rather than widening the budget beyond the profile.

## Continuity and topology changes

The first operation on a sheet starts from `[u,v,0]`. Later operations start at the previous endpoint for that sheet. With a remesh, compare the old and new piecewise-linear embeddings over the material domain, including edge midpoints, centroids and changed crease lines; vertex-only equality is insufficient. No bend may vanish because a new triangulation omitted it.

At least the overlapping mesh refinement must agree within position tolerance. The reference checks vertices, midpoints and centroids in both directions; a general conforming implementation must also handle arbitrary crossing diagonals and local refinements, not assume those finite samples prove all possible embeddings equivalent.

## Partial models

Resolved operations in a `partial` document describe a prefix of its physical instructions. After the first unauthored physical operation, a core player cannot resume geometry later without a separately defined state-reconstruction extension. Show the remaining instructions in Text mode rather than pretending the unknown paper state is known.

## What this does not prove

A valid connected embedding with small edge error may still self-intersect, have incorrect layer insertion, or be impractical in real paper. Collision/contact analysis, realistic thickness, force/pressure simulation, and human folding review are separate evidence. A model’s `limitations` must retain known approximations.
