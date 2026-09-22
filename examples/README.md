# Example catalogue

All documents are original examples for this draft. Use `python tools/check.py` from the repository root to validate the complete examples and paired source files.

| Directory | Purpose | Availability |
|---|---|---|
| [minimal-text](minimal-text/README.md) | Localized primary copy, tactile checks and fallback language | Instructions only; no fabricated geometry |
| [authoring](authoring/README.md) | Named points, alignment, region and intent; `.foldsrc` → JSON AST | Authoring graph; no compiled animation |
| [hinge](hinge/README.md) | Explicit analytic fold and reverse, crease history and layer hints | Complete small geometric lesson |
| [crane](crane/README.md) | 44 teaching steps, 40 resolved operations, static display, flourish, history and parallel text/source examples | Complete geometric demonstration with explicit approximations |
| [partial](partial/README.md) | Resolved prefix followed by an unauthored physical action | Partial; playback must stop at the gap |
| [planned](planned/README.md) | Cup finishing/display requirements before construction is authored | Metadata/proposed presentation only |
| [presentation](presentation/README.md) | Validated bilateral hinge and bounded flutter | Calibration sheet, not a butterfly pattern |
| [scene](scene/README.md) | Raster asset, reusable stage data and a packaged lesson | Runnable validation and asset round trip; no graphical stage player |
| [library](library/README.md) | Data-only base declarations with exports | Structural example; full expansion not implemented by the helper |

Readable `.fold.json` documents are the source for the corresponding shipped `.foldlab` archives. Every archive has a new-format manifest; it is not a legacy application file. No optional artwork, physics or accessibility test is implied merely by a field or filename existing.
