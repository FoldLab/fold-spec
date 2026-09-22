# Reference implementation coverage

This table describes **the supplied tools**, not every behavior a conforming independent player must implement. Read the normative chapters for the complete draft contract.

| Area | Supplied implementation | Limits |
|---|---|---|
| JSON and structural validation | Strict UTF-8/duplicate/nonfinite/depth policy and bundled Draft 2020-12 schemas | BCP 47 syntax subset, not full IANA language registry validation |
| Cross-field semantics | IDs, references, locales, status, instruction-run partitions, narration hashes, camera vectors, review evidence, core authoring cycles | Does not authenticate evidence or review the truth of prose |
| Geometric validation | Rectangular disk topology, orientation/coverage checks, hinge seam constraints, finite positions, analytic sampled-edge bounds | No collision, finite-thickness, force simulation or physical user review |
| Operation boundaries | Bidirectional material vertex/edge-midpoint/centroid comparisons | Not a full overlay-arrangement proof for all possible remesh intersections |
| Local layer relations | Face references and unit normals | No full overlap-region order/cycle/contact validator; display hints are not physical order proof |
| Motion sampling | Analytic hinges/rigid handling, shared sampled positions, duration-weighted instruction runs | No real-time renderer, no arbitrary solver-generated complex folds |
| Fold Source | Finite parser producing the JSON AST; typed graph/reference checks | Not a complete construction compiler |
| Planar constraint helpers | Enumerates four families; checks all seven supplied witness families with separate position/angular residuals | No general enumeration for the last three families, no root conditioning certificate |
| Libraries | Versioned structural schema and fully declared example | No parameter expander, nested-library resolver or multisheet assembly engine |
| Scenes | Structural schema and example asset checks | No interactive stage renderer; image files still need safe platform decoding |
| Packages | ZIP creation/inspection, sizes/hashes/paths/regular-file checks and declared payload enforcement | Not signed author authentication; codec decoding not an image security certificate |
| Text output | Plain text and semantic, escaped, localized HTML | No actual screen-reader/voice testing or tagged PDF generation |
| Final presentation | Static state and deterministic root/hinge flourish sampler | No stage travel renderer, no calibrated spring/cloth solver |
| Print | Normative diagram/template/final-panel semantics | No PDF backend or visual layout engine shipped |
| Compatibility | New-format examples and a documented migration strategy | No complete legacy application adapter; old apps cannot load these files directly |

## Reporting a successful run

Use the validator's actual `checks` and `notChecked` fields. Do not collapse the table above into “fully conformant” or “physically correct.” Passing `--schema-only` proves less than the normal validator, and neither proves every normative semantic or UI behavior.

The [verification report](VERIFICATION.md) records executed tests for this delivery. Future maintainers must regenerate evidence after changes, rather than copying a prior count into a new release.
