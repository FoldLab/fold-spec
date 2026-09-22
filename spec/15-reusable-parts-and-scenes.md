# 15 · Reusable parts and scenes

**Normative for `library-1`; scenes for `presentation-1`**

## Data-only construction libraries

A `.foldlib.json` declares `format: "fold-spec-library"`, version, ID, revision, license, and named `parts`. Each part has a description, `sheetSlot`, bounded parameters/bindings, an authoring graph and an export list. Export names must exist in that graph.

An importing document declares the library as a hashed local asset with role `library`. Each `authoring.imports` record names the asset, part, target sheet, numeric parameter values and any `expandedOperationIds`. The package includes the dependency bytes; an import does not initiate arbitrary network or code execution.

This core handles construction libraries beginning on an unused flat sheet. Applying a base to an arbitrary already-folded sheet requires an explicitly defined precondition/state adapter outside this draft’s library profile. Multiple sheets do not imply simulated glue or physical assembly.

## Parameters and expansion

Each parameter declares ID, minimum, maximum and default. Its bindings name a JSON pointer **inside the part’s authoring object** and a numeric `factor`. The target must be an existing numeric leaf. Expansion substitutes `parameterValue * factor` into those leaves, then validates the resulting typed graph. No expressions, string interpolation, filesystem paths, conditionals or loops are evaluated.

This permits a `sideMm` parameter to fill ±half-side material coordinates using factors 0.5 and −0.5 while retaining derived midpoint/ratio constructions. Parameter units are determined by their bound target fields; a library must not bind one parameter to incompatible dimensions. Unknown parameters, out-of-range values, missing targets, and conflicting writes to the same target are errors.

Replace the library’s declared sheetSlot with the importing target sheet. Prefix all internal typed names and references with `instanceId::`. Import IDs must be unique. Only explicitly exported names can be referenced outside the instance. This avoids capture between a caller’s `center` and a library’s `center`.

Expansion occurs during authoring/compilation, before resolved playback. A portable resolved document retains explicit resolved operations; a runtime does not need the library’s executable code because none exists. Cycles, nested imports exceeding the depth policy, and changing bytes under a supposedly pinned dependency are errors. The current example library has no parameters and demonstrates a basic exported center/alignment graph.

The supplied reference tools validate library structure but do not implement a full library expander. That limitation is explicit; `source-1` parsing must not be confused with `library-1` compilation.

## Standalone scenes

A `.foldscene` declares `format: "fold-spec-scene"`, version, ID, stage, assets and license. It contains no instructional steps, model geometry, final display state, or model-specific wing rig. Applying it changes only the scene-level presentation data.

Scene images are local assets relative to the scene file and are embedded when a model is packaged. A reusable scene file plus sibling assets is an unpacked representation, not automatically one self-contained binary file. For distribution, either include the directory or apply the scene and package the selected assets into the model. This distinction avoids claiming a filename-only style is portable.

A preset label is an editor convenience. The resolved keyframes, image bytes, material parameters where applicable, and response values determine behavior. A scene requesting flutter cannot manufacture a missing model rig; final model flourishes remain model-specific.
