# Changelog

## Unreleased — catalog, thumbnails and package index

Adds, to the `1.0.0-draft.1` edition, everything a gallery needs to list a model from its single `.foldlab` file:

- optional root `catalog` member (`slug`, `addedAt`, `thumbnails[]` with mandatory localized `alt`);
- asset role `thumbnail` (PNG/JPEG/WebP, at most 1 MiB, pixel size verified from the image header);
- optional manifest `index`: a derived browse record that `pack` writes and package inspection recomputes and rejects on any difference;
- `foldspec.py index` to list many documents or packages (duplicate IDs and slugs rejected);
- `examples/catalog`, `tests/test_catalog.py` and three conformance cases.

All additions are optional, so documents and packages that conform to beta 1 remain valid. The converse is not true: readers built against the closed beta 1 schemas reject documents that use `catalog` or the `thumbnail` role. The edition string is deliberately unchanged while this is unreleased; releasing it as beta 2 or `draft.2` is a maintainer decision (the tag `v1.0.0-draft.1-beta.1` still points at the original contract). Run the full checks and rebuild the offline site before release; `VERIFICATION.md` still records the beta 1 run only.

## 1.0.0-draft.1 (beta 1) — 2026-09-22

Initial independent Fold Spec implementer draft. Defines localized instruction documents, explicit material/pose coordinates, named geometric authoring and seven single-crease constraint families, resolved hinges and sampled motion, local layer semantics, persistent crease guides, subdivided instructional runs, accessible text-only content, narration references, final stills and flourishes, artistic scenes, print templates, source/history metadata, reusable data-only parts, versioning and security.

Includes four versioned JSON Schemas, Fold Source EBNF/parser, a limited planar-constraint helper, strict document/package validation, motion and final-presentation sampling, text/HTML export, conformance fixtures, test suite, repository guidance and an offline documentation builder. The crane example is a complete geometric demonstration with explicit advanced-shaping limitations.

This is not an already-implemented successor to the earlier application. No registered media type, deployed public schema endpoint, complete compiler, physical solver or accessibility certification is claimed.

The beta release also links the companion Fold Viewer and includes a screenshot
of that viewer rendering the byte-identical checked-in crane document. This is
presentation evidence, not an expansion of the specification's conformance
claims.
