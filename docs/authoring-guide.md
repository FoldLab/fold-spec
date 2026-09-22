# Authoring with named geometry

**Informative**

Begin with the [complete named-fold source](../examples/authoring/named-fold.foldsrc). Its `document` block contains ordinary JSON for identity, paper, copy and statuses. Typed declarations add the construction graph; they never execute arbitrary expressions.

## A small geometric recipe

```text
point nw in work = material(paper, -75mm, 75mm);
point ne in work = material(paper, 75mm, 75mm);
point far-midpoint in work = midpoint(nw, ne);
line center-crease in work = align-points(nw, ne);
region left on paper in work = half-plane(center-crease, nw);
```

This is a fragment inside a complete `.foldsrc` file. The midpoint lies on the **far edge**, because both endpoints are far corners. Calling that point the sheet center would be misleading. Names should express the actual construction, not merely an attractive label.

A point-to-point alignment gives a crease halfway between the source points. A region specifies which side of it moves. The intent still supplies direction/angle and links to resolved operations. No language can infer the intended paper layers safely from a point alignment alone.

## Frame first

Every construction names an explicit planar frame. It identifies a sheet and either the initial state or a state after an existing operation. Geometry in different frames cannot be combined by silently discarding Z. The frame's `u` and `v` vectors must be orthonormal. If the required material lies off that plane, the planar construction is not applicable.

A material point identifies a location on the original sheet. It moves with that material after folds. A literal point is a coordinate in the specified construction plane. An accessibility landmark is descriptive metadata and is not automatically a symbolic point.

## More than one valid crease

For `align-lines`, two angle bisectors can satisfy the same alignment. Requesting a unique solution is a check, not an instruction to pick the first one. Supply an explicit witness when the intended branch must be retained:

```text
line chosen in work = align-lines(edge-x, edge-y,
  witness(0.7071067811865476, 0.7071067811865476, 0mm));
```

This fragment assumes `edge-x` and `edge-y` exist. The witness uses a **unit normal and offset**, not two arbitrary screen pixels. A compiler must check the reflection constraints before accepting it. See [the seven families](../spec/05-constraints-branches-and-precision.md).

## Reusable bases

A `.foldlib.json` is pinned, local data. It can export named geometric results under an instance namespace. Numeric parameter bindings target defined leaves; no JavaScript, code import, interpolation string, or network call is part of expansion. The reference repository documents this contract but does not implement the full expander.

## Teach one action at a time

Map a continuous geometric operation to meaningful instructional ranges. For a square-base collapse, useful boundaries correspond to guiding side pockets, lowering the outer panel and flattening it. Do not pretend connected panels can move independently, or split a motion at arbitrary fractions merely to increase the displayed step count.

Keep source-step labels when splitting a tutorial. Update captions, tactile checkpoints, narration transcripts, bookmarks and print panels together. The [crane authoring study](../examples/crane/crane-authoring.foldsrc) illustrates a full text recipe with two named diagonal intents; it does not falsely claim all advanced folds are symbolically compiled.

## Working loop

Write primary copy and tactile context; define references and branches; produce resolved motion; validate source continuity and edge behavior; inspect intermediate samples and final display; review with real paper and assistive technology. Store the actual review status. A mathematical invariant passing is not a substitute for a human being able to complete the fold.
