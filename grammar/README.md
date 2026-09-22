# Fold Source grammar and AST mapping

The [EBNF](fold-source.ebnf) is normative for `source-1`. Its semantic target is the same [document schema](../schemas/1.0.0-draft.1/document.schema.json) used for readable JSON. Parsing does not certify constraints or produce a 3D animation.

| Declaration | JSON destination |
|---|---|
| `document {...};` | Root document, excluding inline `authoring` |
| `frame name {...};` | `authoring.frames[]`, outer name becomes `id` |
| `point name in frame = ...;` | `authoring.points[]` |
| `line name in frame = ...;` | `authoring.lines[]` |
| `region name on sheet in frame = ...;` | `authoring.regions[]` |
| `intent name {...};` | `authoring.intents[]` |
| `use name {...};` | `authoring.imports[]`, pinned data reference only |
| `step name {...};` | Appends to `instructions.steps[]` |

A missing optional witness becomes `branch: {"mode":"unique"}`. This requests uniqueness; it does not establish that there is only one solution. Values inside JSON blocks use their schema-defined units. Construction literals attach `mm` or `deg` to avoid accidental unit confusion.

The complete [named-fold source](../examples/authoring/named-fold.foldsrc) and [crane authoring study](../examples/crane/crane-authoring.foldsrc) have paired JSON ASTs. Tests compare the parsed trees, not merely whether the parser accepted a string.
