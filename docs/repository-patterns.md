# Specification repository patterns

**Informative research notes · reviewed 22 September 2026.**

This repository's organization follows practices visible in established specification projects. No external parser or specification implementation is copied into the reference tools. These references describe repository conventions, not endorsement or interoperability claims.

| Repository | Useful pattern | Applied here |
|---|---|---|
| [Khronos glTF](https://github.com/KhronosGroup/glTF) | Separate specification, versioned schema material, extension registry, examples, and contributor documentation | `spec/`, `schemas/`, explicit capability boundaries and contribution templates |
| [CommonMark specification](https://github.com/commonmark/commonmark-spec) | Executable examples and documentation-build tools alongside normative prose | Source/JSON paired examples, executable fixtures, local site builder |
| [TOML test suite](https://github.com/toml-lang/toml-test) | Language-neutral valid/invalid fixture corpus with expected results | `conformance/cases.json`, positive/negative JSON and diagnostics |
| [AsyncAPI JSON Schemas](https://github.com/asyncapi/spec-json-schemas) | Generated versioned schemas plus separate semantic validation; schema alone is not the full standard | Source-owned schema generator, structural versus semantic/geometric reports |
| [OpenAPI specification](https://github.com/OAI/OpenAPI-Specification) | Navigable versioned specification and documented change/proposal process | `SPEC.md`, changelog, release checklist and issue/PR templates |

## What is deliberately not copied

A badge claiming a certified standard, a deployed schema URL, a registered MIME type, a live maintainer service or a broad solver implementation would overstate this project's status. The README identifies an implementer draft, reserved identifiers, runnable reference utilities, and precise coverage limits instead.

## Practical conventions

Each normative chapter states its scope. Complete examples are separate from abbreviated fragments. Schema generation is reproducible. Invalid examples are isolated from normal package discovery and declare their expected error class. Every release should update prose, schema, example, regression test and migration note together.

## Other technical references

- [JSON — RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12)
- [BCP 14 clarification — RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [BCP 47 language tags — RFC 5646](https://www.rfc-editor.org/rfc/rfc5646)
- [JSON canonicalization — RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) — intentionally not claimed by the reference readable writer
- [Origami single-crease construction scope](https://langorigami.com/article/huzita-justin-axioms/)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [FOLD geometry specification](https://github.com/edemaine/fold/blob/main/doc/spec.md)
