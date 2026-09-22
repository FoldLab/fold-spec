# Instructions for implementation agents

Treat `SPEC.md`, normative chapters and versioned schemas as a single contract. Report contradictions; do not silently prefer the easiest interpretation. This is a new-format spec repository, not the FoldLab application.

Preserve original material IDs, exact operation/step mappings, per-side appearance, text alternatives, rights and explicit limits. Geometry, presentation and instruction are different layers. Do not substitute photos or arbitrary final meshes for missing motion. Do not declare physical validation, screen-reader certification or a full symbolic solver based on structural tests.

Edit `tools/schema_source.py` for schema changes. Run schema generation, field-reference generation, `python tools/check.py`, and the site builder after changes. Add valid/invalid fixtures for new syntax or constraints. Keep source-parser examples exactly equivalent to their JSON ASTs.

Do not include secrets, font binaries, cached third-party pages, dependencies, application build directories or speculative compatibility claims in releases. Keep authoring and library programs declarative. Package tests must reject unlisted files, tampered hashes and unsafe paths.

Maintain current verification and release records. Never fabricate test counts, a ZIP path, a public schema host or an already-published release. Missing runtime tooling should be recorded separately from failed specification checks.
