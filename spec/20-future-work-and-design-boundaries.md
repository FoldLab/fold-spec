# 20 · Design boundaries and future work

**Informative**

The core deliberately separates what a file says from what a renderer can prove. It provides a useful interoperable boundary: plain instructions, explicit geometry, typed authoring, and portable presentation can improve independently.

## Candidate future extensions

| Area | Evidence needed before inclusion |
|---|---|
| General pocket insertion/contact | Local material-layer relations, continuous nonpenetration checks, example tucks and physical reviews. |
| Finite-thickness mechanics | Thickness-aware hinge/shell model, contact constraints and measured material parameters. |
| General multi-sheet assembly | Sheet identity, connection semantics, no implicit glue, disassembly and interaction tests. |
| Curved creases and wet folding | A representation preserving source curvature, surface strain bounds and authorship intent. |
| Binary/compressed motion | Typed accessors, endianness, bounds, round-trip tests and safe decompression. |
| Signature/authorship | Canonical signed payload, trust policy, revocation and privacy considerations. |
| Rich language functions | Termination/resource rules, type checking, deterministic expansion and safe module locking. |
| More exact geometry | Robust predicates, interval/root isolation and documented degeneracy handling. |

No candidate is an implied supported feature. A JSON field named `physics` cannot certify real paper behavior. An “inside reverse fold” label cannot substitute for a reproducible operation. New language syntax should preserve semantic intent rather than hide unsupported behavior behind a shorter string.

## Standardization goals

Before a stable 1.0 release, obtain independent parser and playback implementations, verify cross-renderer examples, resolve all normative contradictions, review the authoring/motion binding model, test real assistive technology and folders, and freeze extension/version negotiation. Keep a documented test matrix and release checklist.

The current draft is intentionally usable for implementing those experiments: complete examples, schemas, a safe package format, reference validators and precise limitations are provided now. It is not a declaration that the remaining engineering has already been completed.
