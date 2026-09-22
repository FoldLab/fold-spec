# Data-only construction library

`basics.foldlib.json` declares one reusable part and its exports. The part starts on an unused flat `sheetSlot`; it exposes an alignment and selected region without executing imports or arbitrary code.

This smallest library uses no numeric parameters or bindings. The normative parameter/pointer expansion contract is in [chapter 15](../../spec/15-reusable-parts-and-scenes.md). The reference check validates its schema and exported reference names; it does not claim to expand a complete library hierarchy or generate motion from it.

`parameterized.foldlib.json` adds a bounded `sideMm` parameter and four numeric bindings for the corner coordinates. It is a complete structural example of the expansion input, not evidence that the supplied tools implement a full library expander.
