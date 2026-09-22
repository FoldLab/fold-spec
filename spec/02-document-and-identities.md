# 02 · Document model and identities

**Normative**

## Root members

| Member | Meaning |
|---|---|
| `format`, `specVersion` | Exact wire discriminator and edition. |
| `id`, `revision` | Stable document identity and positive, monotonically increasing author revision. |
| `defaultLocale` | Required primary copy locale. |
| `status` | Planned, instructions, partial geometry, or resolved geometry. |
| `metadata` | Title, summary, authors, licensing, taxonomy and sources. |
| `sheets` | Original material dimensions and both paper faces. |
| `accessibility` | Nonvisual setup, landmarks, limitations and review. |
| `instructions` | One canonical ordered lesson, independently grouped for teaching. |
| `geometry` | Optional resolved meshes and ordered operations. |
| `authoring` | Optional typed construction graph and explicit links to resolved operations. |
| `assets` | Local packaged resources with exact hashes. |
| `presentation` | Final state and optional playthrough-only staging/flourish. |
| `narration` | Optional per-step transcripts and audio availability. |
| `history` | Optional sourced model/symbol/tradition context. |
| `print` | Portable publication defaults, not mandatory personal settings. |
| `extensions` | Versioned, scoped extension declarations. |

See the [field reference](../docs/field-reference.md) for exact required members and schemas.

## Stable names, not rendering indices

Document, sheet, step, operation, mesh, landmark, source, asset and narration identifiers are case-sensitive ASCII strings matching the schema. They MUST remain stable when their semantic identity remains stable. A renderer’s GPU buffer index is not a persistent identity.

Each named collection has a separate namespace, except authoring points, lines, regions and intents, which share a typed name namespace. Thus a step and operation can both be `fold-center`, but two points cannot share an ID or collide with a line name. A mesh’s face and vertex IDs are local to that mesh. Cross-mesh continuity is determined by material coordinates, not accidentally equal local names.

Revisions are not timestamps. The core does not require embedding a complete edit history. Applications MAY keep an append-only revision store outside the document. On splitting a step, retain the original mapping in authoring/source records and update progress/audio links deliberately; do not silently reuse an old ID for a different physical action.

## Metadata and licensing

Titles and summaries are localized plain text. Authors declare roles such as design, instructions, geometry, translation, review and assets. A design being traditional does not establish the rights to another author’s prose, photographs or diagrams. Document licensing and each asset’s license are distinct. An application’s open-source license does not overwrite imported content restrictions.

Categories are broad labels; tags are concise search terms. The spec does not prescribe a global category taxonomy. Applications SHOULD deduplicate obvious aliases and keep source IDs so two procedures sharing a title are not accidentally merged.

## Planned entries and derived UI status

A planned entry has valid identity and useful known metadata, but zero lesson steps. It MAY include proposed display guidance, provided that the absence of authored construction remains explicit. Applications MUST NOT generate empty paper animations, completed-model images, or fake progress counts to fill missing data.

Status counters should be derived from actual validated content. A Markdown work record is not an imported lesson. A lesson with a required manual pocket opening is not a fully resolved cup. Background assignment, custom artwork generation, narration availability, geometry authoring, accessibility testing and real-paper testing are separate accomplishments.

## Local user state

Current step, elapsed wait, selected theme, text sizing, font preference, temporary camera orbit and high-contrast overlays are not source geometry. They belong in per-user state keyed to document ID/revision. Model paper changes and authored cameras are source changes. Export-only recoloring stays in export preferences unless the author explicitly applies it to the model.
