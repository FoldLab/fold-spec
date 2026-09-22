# Wing-rig calibration

`wing-rig.fold.json` contains the analytic center-fold lesson with a bilateral final hinge. The final state is an opened, flat sheet, split along the center axis. The declared rig flutters the two sides with opposite signed angles and returns exactly to rest.

This is a **calibration sheet**, not a claimed butterfly model. It isolates seam and amplitude behavior so implementations can test decorative wing motion without introducing an unverified folding pattern.

The reference function `presentation.sample_flourish(document, progress, reduced_motion=False)` expects a validated document. It samples only the model flourish; it does not render a stage or infer wings from a silhouette. The test suite checks endpoints, unchanged shared-axis vertices, material edge lengths, bounds and source immutability.
