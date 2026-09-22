# Migration from existing FoldLab documents

**Informative.** Fold Spec is a new discriminator and representation, not a renamed release of an existing app format. No universal automatic migrator is supplied.

## Safe adapter strategy

Preserve the original file unchanged. Detect its exact format and version, validate it using its own reader, then create a new document. Carry stable model/source IDs, author/license restrictions, instruction copy and review status. Record conversion history outside claims of designer origin. Do not upgrade uncertain accessibility to user-tested status.

| Existing concept | New representation |
|---|---|
| One action per instructional step | Ordered geometric operations plus instruction `runs` |
| Normalized material and pose coordinates | Explicit millimeter material vertices and resolved positions |
| Axis-angle hinge fold | `kind: "hinge"` with directed 3D axis, selected face IDs and signed degrees |
| Turnover or model rotation | `kind: "rigid"`, or a sampled handling path when required to preserve the lift exactly |
| Dense compound motion | `kind: "sampled"` with shared topology, key times, and interval strain budget |
| Crease record | Material segment event with stable ID, assignment and establishment time |
| Original front/back colors/patterns | Two material objects anchored to material coordinates |
| Accessibility side fields | Canonical localized body plus structured tactile guidance and review |
| Stage image and choreography | Declared hashed image asset and optional presentation stage |
| Existing `.foldscene` dialect | Explicit adapter to the new scene discriminator; not a blind version rewrite |

If the original long sheet edge spans two units, the millimeter multiplier is `max(widthMm,heightMm)/2`. Apply it to **every** relevant point, axis, camera target, path and bend width according to its actual old unit. Do not multiply angles or timestamps. Older camera angles expressed in radians need explicit conversion where mapped to a degree-valued field.

## Timing and easing

If an old compound clip was sampled after an easing function, preserve the actual interpreted curve when baking. Avoid applying the old ease twice. Introducing geometric keyframes is an approximation between keys; validate the whole interpolation interval against the new declared error budget. Endpoints and source material identity remain exact within stated tolerances.

The included crane demonstrates such a resolved adaptation, but its supporting development conversion script is not a general importer. The delivered example contains all data needed by the new sampler without importing the earlier application.

## Do not manufacture intent

Numeric crease endpoints do not prove that the original author intended a named point-to-point or line-to-line alignment. Add symbolic intent only when the relationship has been verified. The crane's first two diagonal intents are explicit; the rest of its complex sequence remains resolved numerical geometry.

## Compatibility policy

A legacy reader must reject the new `fold-spec` discriminator rather than misinterpret its units or filename. A new reader may support legacy formats through explicit adapters, but must not claim byte-for-byte replay if trajectories or presentation semantics changed. Extension/capability support is checked separately from document readability.

Before releasing an adapter, test native/JSON round trips, source rights, locale fallback, material UVs, layer priorities, step ranges, final stills, and all required asset hashes. Maintain original fixtures for regression comparison.
