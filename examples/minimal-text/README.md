# Minimal text lesson

`first-fold.fold.json` contains three steps: place the square, fold it in half, and open it again. Primary instructions, orientation and tactile checks are separate fields. One partial French title demonstrates actual language fallback rather than a claim of a complete French translation.

`instructions.md`, `instructions.txt` and `instructions.html` are readable views of the same copy. `first-fold.foldlab` is the portable package. The model has no authored animation and cannot be used as a geometry fixture.

```sh
python tools/foldspec.py validate examples/minimal-text/first-fold.fold.json
python tools/foldspec.py text examples/minimal-text/first-fold.fold.json --descriptive
```

Run commands from the repository root. No real assistive-technology or physical folding review is claimed by these example files.
