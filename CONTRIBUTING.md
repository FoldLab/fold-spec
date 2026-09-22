# Contributing

Changes should make independent implementations more predictable, not merely make one example pass. Start by identifying whether the change affects normative semantics, a schema, authoring syntax, a reference-tool defect, or only explanatory prose.

A normative change needs: the problem and minimal document; proposed behavior and rejected alternatives; compatibility/version impact; security and accessibility implications; a valid example; at least one invalid or boundary example; and updated tests. Edit `tools/schema_source.py`, regenerate schema output, and regenerate `docs/field-reference.md`. Do not edit generated schemas independently.

Run `python tools/check.py` and `python tools/build_site.py`. Cite actual evidence for review claims. Never loosen geometry tolerances, skip a failing fixture, or replace unsupported motion with a static object merely to get a green test run.

New examples should be original or have clear reuse permission. Keep model-design credit, instruction credit and asset licenses distinct. Do not add remote dependencies, scripts, executable macros, credentials or font files to example packages.

Use the issue templates for contradictions and feature proposals. Submit related prose/schema/example/tests together in one reviewable change. The publishing owner should assign a maintainer and stable release host before any external conformance or registry claim is made.
