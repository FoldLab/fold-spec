# Fold Spec · specification index

**Version:** `1.0.0-draft.1`  
**Status:** implementer draft; no standards-body ratification or universal compatibility is claimed.

Read the normative chapters below in numerical order for a complete implementation. Examples and guides explain usage; the schemas constrain structure. If a schema and normative statement disagree, report a defect and do not silently rely on the more permissive interpretation. See [conformance](spec/00-status-and-conformance.md).

## Normative chapters

- [00 · Status and conformance](spec/00-status-and-conformance.md)
- [01 · Files and packages](spec/01-files-and-packages.md)
- [02 · Document model and identities](spec/02-document-and-identities.md)
- [03 · Paper, coordinates and appearance](spec/03-paper-coordinates-and-appearance.md)
- [04 · Typed geometric authoring](spec/04-geometric-authoring.md)
- [05 · Crease constraints, branches and precision](spec/05-constraints-branches-and-precision.md)
- [06 · Resolved geometry and motion](spec/06-resolved-geometry.md)
- [07 · Layers, sides and persistent creases](spec/07-layers-and-persistent-creases.md)
- [08 · Instructions, substeps and playback](spec/08-instructions-timing-and-playback.md)
- [09 · Accessibility and text-only copy](spec/09-accessibility-and-text-only.md)
- [10 · Localization and narration](spec/10-localization-and-narration.md)
- [11 · Final presentation and artistic stage](spec/11-final-presentation-and-artistic-stage.md)
- [12 · Paper response and rendering fidelity](spec/12-paper-response-and-rendering.md)
- [13 · Diagrams, print and cut-out templates](spec/13-diagrams-print-and-templates.md)
- [14 · History, provenance and rights](spec/14-history-provenance-and-rights.md)
- [15 · Reusable parts and scenes](spec/15-reusable-parts-and-scenes.md)
- [16 · Extensions and versioning](spec/16-extensions-and-versioning.md)
- [17 · Interoperability and migration](spec/17-interoperability-and-migration.md)
- [18 · Security, resource policy and privacy](spec/18-security-resource-policy-and-privacy.md)
- [19 · Diagnostics and conformance tests](spec/19-diagnostics-and-conformance-tests.md)
- [20 · Design boundaries and future work](spec/20-future-work-and-design-boundaries.md)

## Normative syntax and data contracts

- [Fold Source grammar](grammar/fold-source.ebnf)
- [Document schema](schemas/1.0.0-draft.1/document.schema.json)
- [Package manifest schema](schemas/1.0.0-draft.1/manifest.schema.json)
- [Construction library schema](schemas/1.0.0-draft.1/library.schema.json)
- [Reusable scene schema](schemas/1.0.0-draft.1/scene.schema.json)

## Informative guidance

[Architecture](docs/architecture.md) · [Authoring](docs/authoring-guide.md) · [Player implementation](docs/implementing-a-player.md) · [Accessibility](docs/text-only-and-accessibility.md) · [Crane](examples/crane/README.md) · [Field reference](docs/field-reference.md) · [FAQ](docs/faq.md) · [Glossary](docs/glossary.md)

## External references

References are linked at their point of use. The core uses JSON (RFC 8259), JSON Schema 2020-12, SHA-256, BCP 14 terminology and BCP 47 language tags. The implementation does not claim RFC 8785 canonical output, registered MIME types, or a registered `.foldlab` suffix. Research into established specification repository layouts is recorded in [repository patterns](docs/repository-patterns.md).
