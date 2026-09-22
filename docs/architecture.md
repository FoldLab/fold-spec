# Architecture and design goals

**Informative**

Fold Spec is a publication format with an optional authoring layer. Its job is to preserve an origami lesson as useful data, not to prescribe one UI framework or one real-time physics engine.

## Four questions, four layers

**What does the author intend?** Named geometry expresses relationships: align a point to another point, construct a midpoint, choose a line intersection, or use an explicitly selected crease solution. These relationships remain meaningful when a diagram is viewed from a different camera.

**How is the paper moved?** Resolved operations identify original material, hinges and trajectories. They define a reproducible path that can be sampled directly. A renderer must not guess how an unspecified pocket opens merely because the next picture is a cup.

**What does the learner do?** Instruction steps refer to ranges of operations. One coupled collapse can have several teachable phases without making its connected panels independent. Primary copy is shared by the visual viewer, text mode, narration transcript and exports.

**How is the result shown?** The final still pose and theatrical flourish are different things. A printed crane must be the finished crane, not a sample captured halfway through a decorative bow. A camera move cannot substitute for turning the real paper over.

## The compiler boundary

```text
named geometric intent + selected branches + material regions
                         ↓
                 authoring compiler
                         ↓
resolved geometry + source-to-operation bindings + diagnostics
                         ↓
       instruction runs / text / playback / diagrams
```

A resolved operation can be authored without a symbolic recipe. Conversely, a symbolic recipe can exist before its geometry has been authored. Explicit status describes that difference. Keep both when possible, but never let conflicting representations silently override each other.

The reference parser implements a finite declarative syntax and produces the JSON AST. The planar helper demonstrates candidate enumeration for four constraint families and witness checking for seven. No complete construction compiler, general library expander, contact solver, PDF engine, or 3D viewer is included.

## Source versus cache

Material identities, required motion samples, translated copy, selected image assets, narrative references and authored final display are source. Renderer tessellation, thumbnails, decoded texture objects, browser preferences and current progress are derived or personal data.

A thumbnail cache should include model revision, relevant appearance, chosen static pose/camera, output size and renderer version. It should not cause a large document to be reserialized on every frame. Cache misses may be regenerated; missing required motion cannot.

## A modular implementation

A practical application can separate format/validation, authoring, geometry, renderer, instruction state, accessibility, media playback and export packages. React/Next.js, a native application, or a server-side exporter can consume the same documents. The normative spec does not require a particular UI or PDF library. A FoldLab adapter can continue using its existing pdfcn/Forme integration while following the print semantics here.

## Scope boundaries

The core sheet is a rectangular, connected manifold disk. Cuts, curved creases, holes, arbitrary inelastic materials, glue, collision-certified pockets and unrestricted multisheet assembly require a separately specified extension. Multiple declared sheets alone do not prove that their assembly has been simulated. Visual thickness is a display surface, not a physical contact shell.
