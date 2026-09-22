# 17 · Interoperability and migration

**Normative conversion constraints; mappings are informative**

## Existing application documents

Legacy `.foldlab` files use `format: "foldlab"` and application-specific versioned fields. This draft uses `format: "fold-spec"` and `specVersion`. Readers must inspect the discriminator and supported version; the same suffix does not imply wire compatibility. Do not just replace the version string.

Legacy sheet geometry often uses normalized units with the longer dimension spanning two units. Convert positions, material coordinates, hinge endpoints and stage values through their documented frames. A normalized sheet position scales by `max(widthMm,heightMm)/2`; legacy camera radians must not be mistaken for degree-valued operation angles. Copying a vector without converting its coordinate system can produce a visually plausible but incorrect model.

Map an old one-action step to an operation plus one instruction run. Preserve pause semantics deliberately; old timeline-scaled holds and new real-time reading waits are not identical. Retain original step IDs where meaning is unchanged, and source labels when splitting a step.

Map old material-region selection to explicit resolved moving faces after conforming triangulation. Convert old sampled clips without dropping required keys or relaxing edge budgets. Preserve the starting pose and visible ordering across remeshes. Old numerical face ranks become coplanar **hints**, not new claims of general physical stacking correctness.

Accessibility prose, review status, limitations, source attribution, scene images and paper response must survive. A draft accessibility migration remains draft. Unsupported historical geometry or presentation must be reported in a conversion report, not replaced by a finished silhouette.

The crane example includes an adapted legacy geometric demonstration in the new resolved representation. Its limitations are written into the file and example guide. The reference repository does not include a universal legacy migration engine.

## Geometry-only interchange

The separate FOLD format describes meshes, crease patterns, states and ordering information [R1]. Do not claim its `.fold` extension or label a Fold Spec JSON document as FOLD merely because it contains vertices.

A Fold Spec exporter can create a geometry snapshot by mapping material coordinates, positions, triangle adjacency and known crease assignments into the selected FOLD frame representation. Carry provenance and an explicit warning that narration, lesson grouping, authoring constraints, accessibility, stage assets and presentation semantics may not survive that export.

FOLD has multiple-frame and layering concepts; it is not simply a crease-pattern-only format. Conversely, a geometry import containing frames does not inherently supply a complete teachable timeline. Never manufacture physical steps from disconnected snapshots without validated correspondence and motion.

## Other 3D exports

A generic mesh/scene export may preserve appearance and a baked clip while losing paper identity, crease history, tactile copy and branch intent. A conversion must state its preserved and discarded capabilities. A topology-only export cannot be round-tripped into a complete lesson with invented metadata.

## Round-trip guarantees

Lossless native round trips preserve document meaning, stable references, required assets, explicit motion and limitations. JSON member ordering and whitespace are not meaningful; exact asset hashes remain meaningful. Source-language pretty printing need not preserve comments, but the parsed authoring AST must remain equivalent.

[R1]: https://github.com/edemaine/fold/blob/main/doc/spec.md
