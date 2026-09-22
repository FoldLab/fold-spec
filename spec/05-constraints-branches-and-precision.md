# 05 · Crease constraints, branches and precision

**Normative for `construction-1`**

The core construction families specify a single straight crease in a common plane. They are geometric constraints, not a universal language for all possible three-dimensional paper manipulation [R1]. In particular, pocket opening, curling and simultaneous coupled operations need additional resolved motion or a separately defined solver.

## Mathematical definition

Represent a candidate crease by a unit normal `n` and offset `d`, so `n·x = d`. Reflection of point p is:

```text
R(p) = p - 2 * (n·p - d) * n
```

A target line has unit normal m and offset c. Its point residual is `|m·p-c|` in millimeters.

| Constraint kind | Required relations |
|---|---|
| `through-points` | `n·a=d` and `n·b=d`. Distinct points determine one line. |
| `point-to-point` | `R(a)=b`. For distinct points the crease is their perpendicular bisector. |
| `line-to-line` | Reflection maps the complete first line onto the second line. Intersecting distinct lines generally admit two angle bisectors. |
| `perpendicular-through` | Crease passes through p and is perpendicular to line l. Thus `n·p=d` and `n·l.normal=0`. |
| `point-to-line-through` | `R(p)` lies on l and the crease passes through q. Zero, one, or multiple solutions can occur. |
| `two-points-to-lines` | `R(a)` lies on line A and `R(b)` on line B. Multiple solutions and degeneracies are possible. |
| `point-to-line-perpendicular` | `R(p)` lies on l and the crease is perpendicular to r. Feasibility depends on the input configuration. |

A solver MUST NOT assert universal uniqueness for these families. Coincident points/lines, parallel relationships and identity mappings can underdetermine a crease. Degenerate or nonisolated solutions must be reported distinctly from “no solution.”

## Choosing a branch

`branch.mode: "unique"` succeeds only when exactly one admissible distinct solution remains after the declared constraints. Zero solutions produce `E_NO_SOLUTION`; multiple solutions produce `E_AMBIGUOUS`; a continuum produces `E_DEGENERATE`. An arbitrary “first solver result” is never an interoperable branch rule.

`branch.mode: "witness"` supplies the intended crease’s unit normal and offset. A compiler validates that candidate against the constraints and the stated tolerance, then retains the explicit solution. A witness is a solution selector, not permission to ignore a failed constraint. Canonicalizing the sign of a witness must not change the geometric line.

Example: mapping X=0 to Y=0 permits both diagonal bisectors. A witness can distinguish them without depending on enumeration order:

```json
{"mode":"witness","normal":[0.7071067811865476,0.7071067811865476],"offsetMm":0}
```

This is a branch fragment; see [construction tests](../tests/test_construction.py) for complete operands and expected solutions.

## Movement remains explicit

Selecting a crease does not select the moving layer, amount of rotation, or final contact relationship. Those are explicit fields in the intent and resolved operation. A line-to-line construction can be meaningful even where a naïve whole-sheet fold would collide with already stacked paper.

## Numerical contracts

Resolved geometry uses finite numbers interpreted at least with binary64 precision by the reference model. A renderer may upload float32 buffers but may not change canonical source data to match its display precision. Comparison uses declared positional, angular and relative-edge tolerances, not string equality of decimals.

Document tolerances are bounded: position up to 0.01 mm, angle up to 0.01 degree, and relative-edge error up to 0.005. Exact requirements such as increasing times and matching IDs are not softened by these tolerances. A writer must not increase a tolerance silently to rescue an invalid model.

Angular residuals should be measured as angles or normalized directional residuals, not mixed with millimeter errors in a dimensionally ambiguous score. Report each family’s residuals separately. Near-degenerate roots should be isolated/refined or rejected as unresolved; do not snap distinct solutions together because their decimal strings look similar.

Precision has several dimensions: symbolic intent, numerical residual, repeatable motion, material strain and physical feasibility. Passing one does not prove the others. The reference helper enumerates the first four families and checks supplied witnesses for all seven; it deliberately errors for unsupported higher-family enumeration.

[R1]: https://langorigami.com/article/huzita-justin-axioms/
