# 00 · Status and conformance

**Normative · Fold Spec 1.0.0-draft.1 · 22 September 2026**

Fold Spec describes portable origami lessons: their words, geometric intent, resolved paper motion, presentation, and publication. This is a **complete implementer draft for review**, not a ratified industry standard or a claim that all proposed readers already exist. The reference tools implement a documented subset; see [implementation status](../IMPLEMENTATION-STATUS.md).

## Requirements language and authority

Uppercase MUST, MUST NOT, SHOULD, SHOULD NOT and MAY have their BCP 14 meanings [R1]. Lowercase usage is ordinary prose. Normative requirements are in the numbered `spec/` chapters. The JSON schemas enforce structure; prose adds cross-reference, mathematical, state-machine, and behavioral requirements. Examples and implementation guides are informative. A schema/prose disagreement is a defect to report, not permission to choose whichever behavior is easier. Until clarified, the normative prose governs.

## Representation versus capability

A valid document does not prove that an application can animate it. A reader MUST publish the capabilities it implements and the resource limits it applies. It MUST NOT skip an unsupported physical operation and continue as if the resulting paper were correct.

| Profile | Contract |
|---|---|
| `document-1` | Parse the document, validate structure, IDs, local references, statuses and required default-locale copy. |
| `package-1` | Verify the bounded archive, every declared asset and every digest before use. |
| `text-1` | Present the canonical instructions, setup, limitations and final guidance without depending on geometry. |
| `accessible-viewer-1` | Implement the nonvisual, keyboard, motion and user-control contract in chapter 09. |
| `source-1` | Parse all declared Fold Source syntax to the same JSON authoring graph. Parsing is not solving. |
| `construction-1` | Resolve the seven crease-constraint families, typed references, explicit branches and region expressions. |
| `library-1` | Expand bounded, pinned, data-only reusable parts with capture-free names. |
| `playback-1` | Interpret all core resolved operations, their continuity, instruction ranges and semantic layer data. |
| `presentation-1` | Interpret static display poses, safe root flourishes and validated bilateral rigs. |
| `print-1` | Produce equivalent static instruction panels and physical-size templates. |

Profiles are cumulative only where their contracts explicitly require another. For example, a text reader need not contain a constraint solver. A package reader needs document validation but need not decode every optional audio asset. A playback reader does not become a physical simulator by passing its profile.

## Document availability

`status` is one of `planned`, `instructions`, `partial`, or `resolved`.

* `planned`: no instructional steps and no geometry. This is a catalogue record, not an executable lesson.
* `instructions`: one or more real instructions, no resolved geometry. Symbolic authoring may be present, but is not misrepresented as compiled motion.
* `partial`: resolved geometry for an initial prefix of the physical instruction sequence; later operations remain unauthored. A reader stops 3D progression at that boundary while retaining the remaining text.
* `resolved`: all physical instructions have a resolved motion representation. Setup, check and optional decoration may be non-geometric.

A check can be a real instruction without changing geometry. A required opening cannot be relabeled as a check to evade completeness rules. `resolved` means a continuous representation exists; it does **not** mean collision-free, physically tested, mathematically exact, or accessible-user-tested.

## Honest failure and fallback

A reader MAY offer Text mode when playback is unsupported, but MUST label the unavailable capability and MUST retain the unmodified source. Unknown required `text` extensions prevent a faithful text conformance claim. Unknown required `playback` extensions do not necessarily prevent reading the base instructions.

Limits are implementation policy, not evidence that a larger document is mathematically invalid. Diagnostics SHOULD distinguish malformed data, unsupported capabilities, exceeded resource limits, unresolved construction, and failed physical validation.

## Version policy

`specVersion` is exactly `1.0.0-draft.1` in this edition. Draft revisions require exact support; no forward interpretation is implied. The stable major/minor/patch policy is described in chapter 16. Neither this spelling nor a schema passing grants a legacy application support for the new format.

[R1]: https://www.rfc-editor.org/info/bcp14/
