# 03 · Paper, coordinates and appearance

**Normative**

## Units and frames

All physical lengths and resolved positions are **millimeters**. All operation angles are **degrees**. All durations are integer **milliseconds**. Progress `at`, `from` and `to` is dimensionless in [0,1]. Do not mix these with legacy normalized sheet units, radians, CSS pixels or animation frames.

A sheet starts as a rectangle centered at the origin in its material XY plane:

* `u` / X increases to the folder’s right.
* `v` / Y increases away from the folder.
* +Z is above the work surface and is the original material front, called Side A.
* Side B is the reverse of the same material sheet.

A 150 × 150 mm sheet therefore occupies [-75,75] × [-75,75]. Every mesh vertex stores a fixed `uvMm` identity on that original sheet and a current 3D position. Folding changes position, not material identity. A material point on a crease can be incident to several faces without becoming several independent particles.

Each sheet has its own initial material/pose frame. Core playback leaves unrelated sheets still while an operation names another sheet. Physical contact or assembly between sheets requires a separately supported assembly extension. Listing multiple sheets is not an assembly solver.

## Dimensions and thickness

`widthMm`, `heightMm` and `thicknessMm` are explicit. The canonical core is a zero-thickness material mid-surface. Thickness informs rendering and future physical models; it does not authorize disconnecting faces or changing hinge locations.

The suggested display default is 0.18 mm. Rendered boundary rims MAY show that thickness, but MUST remain attached to shared geometry. Readers SHOULD avoid making the paper look like a thick block when stacked. Collision-aware thickness is outside core conformance.

## Front/back materials

Each face declares `color`, `roughness` and `texture`. Suggested defaults are a flat modern accent such as `#DA453E`, an off-white reverse such as `#F7F2E8`, roughness 0.88, and restrained washi texture. These are appearance presets, not measured material properties.

Colors are six-digit sRGB values. Realistic paper is opaque. Front/back selection follows the consistently wound material faces and current orientation; two coplanar transparent planes are not an acceptable substitute. X-ray transparency is a viewer mode and MUST NOT overwrite source opacity.

`texture.kind` is `smooth`, `washi`, or `kraft`; `strength`, `seed`, and `scaleMm` provide stable artistic parameters. Pixel-exact fiber appearance is deliberately not standardized. Readers must preserve the original seed/data on round trip even when their shading implementation differs.

## Patterns and raster images

Optional patterns are `none`, `waves`, `hemp-leaf`, `checks`, or `linked-circles`. `tileMm`, `ink`, and `opacity` define their scale and contrast. These are generic geometric appearance families, not reproductions of a named artist’s fabric or paper.

An optional `imageAsset` refers to a declared `paper-image` asset. The default front-anchored UV mapping is:

```text
s = (u + widthMm / 2) / widthMm
t = (heightMm / 2 - v) / heightMm
```

`uvTransform` is `[a,b,c,d,tx,ty]` with `s' = a*s + c*t + tx` and `t' = b*s + d*t + ty`. Default is identity. Both material faces use original material identity; viewing Side B physically reverses orientation. An author who wants a back image authored from a back-facing viewpoint must explicitly use the appropriate image transform, commonly `[-1,0,0,1,1,0]`. A renderer MUST NOT add a second undocumented mirror.

Apply base color, then an optional raster image as a replacement printed appearance over its coverage, then the procedural pattern, then subtle surface texture. Shading acts last. Readers that cannot show an optional appearance asset disclose the approximation while retaining the asset.

## Viewer and output overrides

A high-contrast palette, strong outline, plain stage, UI theme, or export ink-saving palette is a reversible overlay. None changes the actual paper’s dimensions, creases, saved colors, or layer membership. The effective order is explicit model data, then deliberately selected export/view overrides. Global defaults fill newly created or unspecified authoring choices; they do not silently replace imported materials.

## Camera records and interpolation

A camera records its `positionMm`, `targetMm`, unit `up`, and projection. Position must differ from target, and the view direction must not be parallel to up. An orthographic camera requires `verticalSpanMm` and must not contain `verticalFovDeg`; perspective does the reverse. The vertical field of view is in degrees. A missing `transitionMs` means an immediate authored view change.

For a stable camera basis, let `back = normalize(position-target)`, `right = normalize(up × back)`, and `trueUp = back × right`. These form a right-handed orientation matrix with columns right/trueUp/back. `up` is an orientation hint; the resulting trueUp is used for projection. A top-down initial view may use position [0,0,200], target [0,0,0], up [0,1,0].

When transitioning within a physical instruction, derive source and destination unit quaternions from those bases. Normalize quaternion sign to positive w; when w is zero, the first nonzero x/y/z component is positive. If their dot product is negative, negate the destination to choose the shorter arc. At the exact equal-length 180-degree tie, retain the canonical destination sign. Use shortest-path slerp with clamped quintic ease `e(t)=t³(10−15t+6t²)`.

Interpolate target coordinates, positive camera-to-target distance, and orthographic span or perspective field of view using the same eased parameter. Reconstruct position as interpolated target plus rotated +Z times the interpolated distance; this avoids a linear camera path passing through its target. Cap transition duration at the step's active physical-run duration. For steps with no physical duration, use the authored view immediately. Different projection types switch at the boundary instead of blending incompatible matrices.

If a step omits a camera, retain the preceding authored camera; the reader chooses a neutral initial fit when none has been supplied. Explicit camera records must not be silently refit independently each frame. Viewport aspect ratio changes horizontal framing, not the stored vertical span or field of view. Clipping planes are renderer policy and must contain the relevant model geometry.

Free inspection may override the authored view without changing instructions or material coordinates. Returning to the authored camera can use a local UI transition unless reduced motion requests an immediate change. That local inspection bridge is not a physical fold or a portable timing claim. Text mode and printed diagrams never require the user to replay the bridge.
