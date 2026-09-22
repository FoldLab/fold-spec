# Reusable scene and local asset

`quiet.foldscene` contains stage data and a hashed local `assets/grid.png` image. The 64 × 64 grid is an original calibration raster, not generated Japanese artwork or an external photograph. The scene alone is JSON plus a sibling asset, not a self-contained single file.

`staged-fold.fold.json` applies that scene to the analytic hinge lesson. `staged-fold.foldlab` packages the actual PNG bytes and the document under a verified manifest.

```sh
python tools/foldspec.py inspect examples/scene/staged-fold.foldlab
```

The optional paper-response parameters are documented art direction, not a measured paper material. There is no stage renderer in the reference toolchain; the checks establish structural/asset consistency and the underlying fold geometry.
