# Design decision register

**Informative.** Decisions are part of the draft's engineering rationale, not evidence that a complete engine exists.

| ID | Decision | Reason / tradeoff |
|---|---|---|
| D01 | Keep intent separate from resolved motion | Retains meaningful construction relationships without forcing runtime solvers into playback |
| D02 | Distinguish teaching steps from operations | Allows understandable collapse substeps without detaching connected panels |
| D03 | Use original material coordinates and explicit pose coordinates | Stable textures/creases, consistent shared seams, unambiguous units |
| D04 | Require explicit branch selection | Multiple valid alignment solutions must not depend on parser/solver enumeration order |
| D05 | Keep text as first-class content | Unanimated lessons remain useful without fake geometry |
| D06 | Add tactile detail to shared primary copy | Avoids maintaining contradictory visual and nonvisual recipes |
| D07 | Separate final still from flourish | Correct print result and reduced-motion behavior |
| D08 | Use local declared assets with hashes | Portable delivery and corruption checks without code execution |
| D09 | Keep a strict bounded core | Unknown required behavior fails visibly instead of being silently guessed |
| D10 | Name physical-review limitations | Geometry checks, rendering quality and physical feasibility are not equivalent |
| D11 | Draft new discriminator and explicit adapters | Avoids silently breaking older application file semantics |
| D12 | Keep personal settings outside source data | Theme, contrast and accessibility preferences must not rewrite model or print colors |

Before changing one of these decisions, include a minimal example, compatibility impact, updated schema/semantics and both positive and negative tests. A future extension should define its fallback and resource policy, not merely add an arbitrary object to JSON.
