# Glossary

| Term | Meaning in Fold Spec |
|---|---|
| Material space | Original two-dimensional position on a sheet, measured in millimeters |
| Pose space | Three-dimensional position of that material at a particular operation time |
| Folder-table frame | Near/far/left/right relative to the person's work surface, not the camera |
| Construction frame | An explicitly identified plane and source state for symbolic geometry |
| Landmark | A stable descriptive reference; optional material location does not make it a solver variable |
| Point / line / region | Typed authoring entities used to express geometric intention |
| Constraint | A relationship a candidate crease must satisfy |
| Witness | An explicit crease solution that still must satisfy its constraints |
| Intent | A crease plus selected material region, direction, duration and optional resolved-operation bindings |
| Operation | An executable hinge, rigid handling transform or sampled trajectory |
| Step | A learner-facing instruction, possibly covering part of an operation |
| Run | A normalized increasing range of one operation assigned to a step |
| Group | An ordered collection of related instructional step IDs |
| Persistent crease | A material-space line event retained when paper is unfolded |
| Layer relation | Local geometric ordering over an explicit overlap patch |
| Layer hint | A rendering tie-break for coplanar surfaces, not physical contact proof |
| Remesh | A topology representation change preserving the same material-to-pose mapping |
| Final display | Static completed pose used by printing and reduced-motion presentation |
| Flourish | Decorative motion that starts and ends at that display pose |
| Paper response | A bounded visual bend/settle approximation, not calibrated elasticity |
| Resolved | Motion is present for the declared complete sequence; not a physical certificate |
| Partial | Motion covers only a declared contiguous prefix before an unresolved physical instruction |
| Text-ready | Actual instructional copy without claimed resolved geometry |
| Planned | Metadata/proposed guidance without a completed tutorial |
| Schema check | Structural JSON validation |
| Semantic check | References, status combinations, chronology and other interpretation rules |
| Geometric check | Material topology, seams, trajectories, residuals and defined error budgets |
| User-tested | A review claim requiring evidence, not something a parser authenticates |
