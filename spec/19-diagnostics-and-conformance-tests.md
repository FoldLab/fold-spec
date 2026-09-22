# 19 · Diagnostics and conformance tests

**Normative diagnostic categories; informative reference tooling**

Diagnostics have a stable code, readable message and optional path/identifier. JSON Pointer-style paths identify document members; Fold Source diagnostics identify source lines. Readers may provide additional context, but must not hide an unsupported capability behind “success.”

| Code family | Meaning |
|---|---|
| `E_JSON`, `E_ENCODING`, `E_UNICODE`, `E_DUPLICATE_KEY`, `E_NUMBER` | Input cannot be interpreted as strict bounded JSON/text. |
| `E_SCHEMA`, `E_VERSION` | Structural shape or required version unsupported. |
| `E_REFERENCE`, `E_DUPLICATE_ID`, `E_FRAME`, `E_CYCLE` | Broken identity, type, frame or dependency graph. |
| `E_STATUS`, `E_RUN_COVERAGE` | Availability claims and instructional motion coverage disagree. |
| `E_DEGENERATE`, `E_AMBIGUOUS`, `E_NO_SOLUTION`, `E_CONSTRAINT` | Crease construction cannot be resolved as requested. |
| `E_SOLVER_UNSUPPORTED` | This implementation cannot enumerate the requested family; it did not guess. |
| `E_TOPOLOGY`, `E_MATERIAL`, `E_COVERAGE`, `E_TEAR` | Invalid material mesh or disconnected hinge selection. |
| `E_CONTINUITY`, `E_STRAIN` | State mismatch or motion outside declared numerical budgets. |
| `E_LAYER`, `E_CAMERA`, `E_RIG`, `E_PRESENTATION` | Invalid view/contact/rig/display relationship. |
| `E_NARRATION`, `E_NARRATION_HASH`, `E_NARRATION_STALE` | Audio state or transcript binding invalid. |
| `E_LOCALE`, `E_REVIEW` | Missing copy locale or unsupported review claim. |
| `E_PATH`, `E_ASSET`, `E_ASSET_HASH`, `E_PACKAGE_HASH`, `E_MANIFEST`, `E_ZIP`, `E_IMAGE` | Packaging or media integrity issue. |
| `E_LIMIT`, `E_UNSUPPORTED`, `E_DEPENDENCY`, `E_IO` | Resource/capability/environment failure, not necessarily invalid origami. |

Different validators may detect different first failures when one fixture violates several requirements. Negative fixtures should isolate one defect. Compare acceptance/rejection and relevant category, not an entire implementation-specific prose error string.

## Test layers

1. **Structure:** every positive JSON example passes the pinned schema and every negative fixture fails its intended layer.
2. **Semantics:** typed references, locales, statuses, range coverage and resource roles are coherent.
3. **Geometry:** material topology, hinge seams, endpoint continuity, remesh matching and interpolation error are checked.
4. **Packaging:** hashes, CRCs, size bounds, paths and asset equality survive pack/unpack.
5. **Language:** valid Fold Source produces the expected AST; invalid syntax/types are rejected without execution.
6. **Behavior:** player timing, waits, narration lifecycle, focus, reduced motion and printing agree with their contracts.
7. **Human/physical:** actual paper folding and assistive-technology/user testing validate claims that data checks cannot prove.

The repository includes layers 1–5 with explicit implementation limits. It does not ship a production browser simulator or PDF runtime. Tests for those belong to implementing applications.

## Test manifest and deterministic examples

`conformance/cases.json` lists language-independent fixture intent and expected validity. `tests/` exercises numeric and package behaviors in Python. `tools/check.py` validates all examples, schemas, source AST equality, local Markdown links and package contents, then runs the test suite.

The crane report distinguishes triangle counts summed across mesh revisions from the final model’s face count. A positive edge-strain check is not a collision-free certificate. Current measured results appear in [verification](../VERIFICATION.md), never inherited from an older application report.
