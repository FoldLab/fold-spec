# 16 · Extensions and versioning

**Normative**

This draft uses explicit named extensions instead of accepting arbitrary unknown members throughout core objects. A declaration has an ID such as `org.example:assembly`, a three-part extension version, scoped `requiredFor` profiles, and `data`. The identifier is a namespace convention, not an automatic claim that the named domain endorses or serves the extension.

The root core objects are closed. Extension data is opaque to an unaware reader and must remain bounded, non-executing JSON. Extensions cannot redefine the meaning of a core field, weaken validation, or disguise an unsupported physical operation as optional decoration.

## Required capabilities

`requiredFor` can name text, authoring, playback, presentation or print. An empty array declares supplemental data that an unaware reader may ignore, while preserving it on round trip. Supplemental data must not be necessary to reconstruct physical geometry. A reader that does not support a required extension for a requested view must decline that conformance claim and explain the missing capability. It may still offer another unaffected view. Merely retaining unknown JSON bytes is not equivalent to implementing the extension.

Writers preserve unknown extension data on non-destructive round trips unless the user explicitly chooses a lossy conversion. Editing geometry in an unaware tool must invalidate dependent extension claims rather than silently keep stale animation or history metadata.

## Feature lifecycle

New normative features require a written proposal, schema, positive/negative examples, safety/privacy analysis, compatibility description and tests. An extension should have a clear scope and at least one implementation before promotion to a stable core feature. Evidence of two independent interoperable implementations is a release goal, not something this repository claims to have already achieved.

A future stable major version can make breaking semantic changes. Minor stable versions add compatible capabilities only through explicit negotiation rules. Patch versions clarify prose or fix nonsemantic errors. Draft editions use exact support, since semantics can still change during review.

The document revision is separate from specification version. A copy edit increments the document revision without requiring a new standard version. A new required operation changes capability requirements even when the rest of the tutorial is identical.

## Out of core scope

Cryptographic author signatures, arbitrary executable plugins, dynamic network imports, remote code/shaders, kirigami cuts, glue joints, material-calibrated cloth physics, general multi-sheet contact, and binary mesh compression are not silently implied. They require explicit future contracts. Discussing an extension idea in this repository does not make it implemented.
