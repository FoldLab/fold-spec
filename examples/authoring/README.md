# Named construction example

`named-fold.foldsrc` and `named-fold.fold.json` are exactly equivalent source and AST forms. Their declared work frame is the initial paper plane. Two far corners define a point-to-point alignment crease; a named material region selects the left half.

The `far-midpoint` reference is the midpoint of the far edge, not the center of the full sheet. This distinction is deliberate: meaningful references should preserve what they actually construct.

```sh
python tools/foldspec.py parse-source examples/authoring/named-fold.foldsrc -o build/named.fold.json
python tools/foldspec.py validate build/named.fold.json
```

The parser does not invent a resolved motion. The explicit `resolvedOperations: []` field says this intent is not yet bound to an animation. See the hinge example for independently authored executable geometry.
