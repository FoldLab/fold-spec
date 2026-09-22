# Analytic center fold

A 150 × 150 mm square is divided into a conforming mesh. `fold-center` moves the left faces around the directed center axis through +180 degrees. `open-center` reverses that motion while retaining the material crease. The long-face area is not recomputed by blending between incompatible shapes.

```sh
python tools/foldspec.py sample examples/hinge/center-fold.fold.json --operation fold-center --progress 0.5 -o build/hinge-halfway.json
python tools/foldspec.py inspect examples/hinge/center-fold.foldlab
```

The narrative and optional missing-audio record use the same primary text. A small final tip demonstrates presentation metadata; it is not an additional folding instruction. The reference sampling functions are deterministic at the endpoints and do not mutate the source object.
