# Verification record

**Edition:** `1.0.0-draft.1` · **Executed:** 22 September 2026 · **Environment:** Python 3.13.5 on Linux, jsonschema 4.26.0, mistune 3.2.1.

The reference tools and supplied examples pass the checks below. This is an implementer-draft specification with explicitly limited reference tooling, **not** a claim of complete player conformance, physical correctness, or a deployed application. The machine-readable result is [verification-results.json](docs/verification-results.json).

## Executed checks

| Check | Result | Scope |
|---|---:|---|
| Unit and regression suite | **124 passed, 0 failures, 0 errors** | Includes seven real command-line subprocess tests, not just direct function calls |
| JSON Schemas | **4 passed** | Draft 2020-12 structural schema checks plus regeneration equality |
| Readable document examples | **10 passed** | Status, locale, references, topology and other implemented semantic checks |
| Native `.foldlab` packages | **10 passed** | CRC, declared payloads, sizes, SHA-256 and equality to readable source |
| Source/JSON example pairs | **2 passed** | Exact parsed authoring AST equality |
| Standalone scene example | **1 passed** | Structure, path ordering, camera and local raster asset checks |
| Library examples | **2 passed** | Structure, exports and parameter-binding example targets; not full expansion |
| Language-neutral fixture corpus | **12 cases** | Two accepted cases and ten deliberately rejected cases, exercised within the unit suite |
| Documentation links | **152 checked in the recorded run** | Existing local Markdown targets; additional site-link checks are recorded with the package |
| Offline documentation | **59 HTML pages; 2,058 local references passed** | File and fragment targets, unique IDs, page titles/main landmarks; zero scripts and remote resources |
| Python syntax compatibility | **Passed** | Python 3.10 grammar parse of shipped tools/tests; actual execution used Python 3.13 |

The full repository check completed in approximately 33 seconds in the recorded run. This is a test-runtime observation, not a performance guarantee. Runtime varies with machine load.

## Functional README commands

The subprocess suite validates the real crane file, parses the named source example into a new JSON file and validates it, samples the documented hinge operation, exports the crane to plain text and semantic HTML, creates and reopens a package with its actual background asset, rejects a second write to the same package path, checks the labelled schema-only mode, and verifies JSON error reporting for an unknown operation.

Outputs are created in temporary directories. The test suite does not rewrite the shipped examples. The `pack` command intentionally refuses to overwrite an existing destination; this is documented in the README.

## Crane geometry evidence

The crane has **44 instructional steps**, **40 resolved operations**, and **1,002 sampled interpolation intervals**. Its final mesh has **208 triangles**; all topology revisions together contain 2,360 triangles. The latter number is not the simultaneous render mesh size.

The maximum measured relative edge-length deviation is **0.0014848974941527038** (approximately **0.14849%**) and is below the document's 0.005 budget. Sampled intervals are checked analytically for the minimum and maximum edge lengths of the linear interpolation, not merely at a few arbitrary playback frames. Hinge samples and step subdivisions are also exercised.

This evidence checks the supplied numerical representation. It does not certify self-contact, physical folding, finite-thickness feasibility, tactile comprehension or perfect correspondence to every traditional crane variant. Model qualifications remain in the JSON and in the exported text.

## Boundaries and unexecuted checks

The reference implementation does **not** include a full symbolic construction compiler, full reusable-part expander, complete overlap-arrangement/layer-order proof, 3D viewer, PDF renderer or legacy FoldLab application adapter. Its planar helper enumerates four constraint families and validates supplied witnesses for all seven; it does not claim general solution enumeration for the remaining three.

A Chromium attempt to navigate to the locally generated documentation returned `net::ERR_BLOCKED_BY_ADMINISTRATOR` in the delivery environment. The restriction was not disabled. No browser-rendered or real-screen-reader pass is claimed. The offline documentation is instead checked for generated pages, local links/resources and script-free structure. The hosted GitHub Actions workflow is supplied but has not run on GitHub as part of this delivery.

No paid audio service, online generation API, real-paper folding session, NVDA/VoiceOver review, or physical collision solver was used to manufacture a stronger test claim. See [implementation coverage](IMPLEMENTATION-STATUS.md) for the profile-by-profile limits.

## Reproduce

```sh
python -m pip install -r requirements.txt
python tools/check.py --report build/check-results.json
python tools/build_site.py
python tools/check_site.py build/site
```

Before publishing another edition, regenerate changed schemas and examples, rerun these checks, regenerate this report, build the documentation again, and verify a freshly extracted package. Do not carry this count forward as evidence for modified files.
