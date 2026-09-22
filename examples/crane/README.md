# Paper crane — complete format example

This directory demonstrates a substantial origami document, not just a finished-model mesh. The primary example begins with a 150 × 150 mm square, stores every operation in its instructional sequence, and finishes with a three-dimensional crane display.

**Status: resolved geometric demonstration; physical and accessibility-user review not performed.** The head/neck/tail and body shaping are explicitly qualified approximations, not a universal physically accurate crane solver.

## Files

| File | What it contains |
|---|---|
| [crane.fold.json](crane.fold.json) | Complete structured lesson and executable resolved data |
| [crane.foldlab](crane.foldlab) | The same document in the verified native archive |
| [crane-text.fold.json](crane-text.fold.json) | The same primary instruction copy without claiming animation |
| [crane-text.foldlab](crane-text.foldlab) | Portable text-only counterpart |
| [crane-authoring.foldsrc](crane-authoring.foldsrc) | Full text recipe plus two named diagonal-crease intents |
| [crane-authoring.fold.json](crane-authoring.fold.json) | Exact parsed AST of the authoring study |
| [crane-instructions.md](crane-instructions.md) | Clean Markdown instructions with tactile guidance |
| [crane-instructions.txt](crane-instructions.txt) | Plain text export |
| [crane-instructions.html](crane-instructions.html) | Script-free, semantic reading view |

The authoring study intentionally leaves complex operations unresolved symbolically. The full geometric document already carries those paths numerically, but that does not mean the reference parser can infer them from prose or constraint syntax.

## Structure

There are **44 teaching steps and 40 ordered geometric operations**. Each step maps to its operation range; a check may have no movement. Topology revisions sum to 2,360 triangles across the entire sequence. The **final mesh contains 208 triangles**. Do not confuse the summed revision count with simultaneous render complexity.

| Step range | Teaching purpose |
|---|---|
| 1–11 | Prepare the square; make/open two diagonals; turn over; make/open straight creases; return to Side A |
| 12–16 | Guide and flatten the square base in four physical phases, then check it |
| 17–23 | Front guide creases, top hinge and coupled petal fold |
| 24–30 | Work on the reverse face, prepare the second petal and orient the bird base |
| 31–36 | Narrow both sides of the two lower points |
| 37–39 | Raise neck and tail; form the beak with qualified paired-layer motion |
| 40–44 | Spread wings, orient for display, ease open the body and check the result |

The primary instruction is shared by the text counterpart. Tactile sections identify orientation, relevant layers and review limits. Empty locating/check arrays are not padded with made-up tactile facts.

## The square-base subdivision

All four ranges reference `op-12`:

| Step | Operation interval | Purpose |
|---|---:|---|
| `begin-base` | 0.00–0.18 | Begin bending along existing precreases |
| `guide-pockets` | 0.18–0.55 | Guide connected side pockets inward |
| `lower-panel` | 0.55–0.88 | Lower the outer panel while retaining the nested sides |
| `flatten-base` | 0.88–1.00 | Close the square base |
| `check-base` | No operation | Confirm orientation and layer arrangement |

These are ranges of one coupled movement. They do not claim that every panel can move independently or that a pause introduces another physical crease. Endpoint comparisons check the exact shared range boundaries.

## Geometric verification

The reference validator checks disk topology, material coordinates, winding, shared hinge seams, first-state flatness, operation-to-operation material continuity, and sampled-edge interpolation budgets. The supplied crane has 1,002 sampled interpolation intervals. Its measured maximum relative edge error is approximately **0.0014848975**, or **0.14849%**, below the declared maximum of 0.005.

That error measures edge-length deviation in the particular interpolation representation. It is not an accuracy percentage for the model's entire physical behavior. No real-paper review, self-collision certification, finite-thickness contact solver, or perfect remesh-arrangement proof is supplied.

The continuously sampled paths are authored geometry. The neck/tail/head motions simplify inside reverse folds as paired-layer hinges. The central opening is faceted and does not simulate air pressure, fingertip forces or paper spring-back. These limitations travel in the document and its text exports.

## Appearance, display and context

The example has a modern cobalt front, off-white reverse, restrained washi texture, explicit physical dimensions and visual thickness. Text directions do not rely on those colors. The material stays attached to the same original sheet coordinates through every operation.

The final display refers to the last physical operation and has an orthographic camera. A short decorative bow returns to that pose. Printing uses the static completed crane, never a mid-bow frame. The print configuration includes all teaching panels and a 152.4 mm cut-out square (six inches) with the explicitly labelled guide convention.

The historical note is scoped to the crane as a **symbol**. Its source is the [City of Hiroshima's paper-crane information](https://www.city.hiroshima.lg.jp/english/peace/1033408/1009685.html). It is not a claim that this particular geometric demonstration is an authenticated historical pattern or that its exact construction dates to a particular period.

## Reproduce

From the repository root:

```sh
python tools/foldspec.py validate examples/crane/crane.fold.json
python tools/foldspec.py inspect examples/crane/crane.foldlab
python tools/foldspec.py sample examples/crane/crane.fold.json --operation op-12 --progress 0.55 -o build/crane-pocket-phase.json
python tools/foldspec.py text examples/crane/crane.fold.json --descriptive --html -o build/crane-reading.html
```

The sampler produces millimeter geometry for a renderer; it does not output an image. The full example is in the new Fold Spec dialect and needs its reader, not the earlier FoldLab v0.8 loader.
