# Quick start

**Informative; commands use the repository root.**

## 1. Install and check

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python tools/check.py
```

PowerShell activation: `.venv\Scripts\Activate.ps1`. The reference tools require Python 3.10+. They do not need your application project, a renderer, a GPU, or an API key. Install dependencies before going offline.

`check.py` checks schema syntax, complete examples, source-to-JSON equivalence, local documentation links, shipped package integrity, fixtures, and the unit suite. It exits nonzero on failure and prints an explicit summary. It does not claim the unresolved authoring graphs have been compiled into geometry.

## 2. Read a text-only model

```sh
python tools/foldspec.py validate examples/minimal-text/first-fold.fold.json
python tools/foldspec.py text examples/minimal-text/first-fold.fold.json --descriptive
python tools/foldspec.py text examples/minimal-text/first-fold.fold.json --locale fr-CA --html -o build/lesson-fr.html
```

The partial French translation demonstrates fallback. Translated and fallback spans retain their actual language. Text-only content has no phantom mesh or canned animation.

## 3. Inspect actual motion

```sh
python tools/foldspec.py sample examples/hinge/center-fold.fold.json --operation fold-center --progress 0.5 -o build/hinge-state.json
```

The output contains the referenced triangle topology and current millimeter positions. It is suitable input to a renderer. It is not a screenshot or an image file. To see the exact operation IDs in any document, inspect its `geometry.operations` array.

## 4. Use the crane

```sh
python tools/foldspec.py validate examples/crane/crane.fold.json
python tools/foldspec.py sample examples/crane/crane.fold.json --operation op-12 --progress 0.55 -o build/collapse-state.json
python tools/foldspec.py text examples/crane/crane.fold.json --html --descriptive -o build/crane.html
```

Read [the crane notes](../examples/crane/README.md) before treating it as a physical reference. Its resolved geometry has deliberately documented approximations and measured strain bounds.

## 5. Package and inspect

```sh
python tools/foldspec.py pack examples/scene/staged-fold.fold.json -o build/staged.foldlab
python tools/foldspec.py inspect build/staged.foldlab
```

The packer copies the declared local background bytes and creates their manifest hashes. It rejects missing assets, invalid paths, symlinks, duplicate names, and an existing destination. It does not fetch remote audio. Archives and file suffixes in this repository use the new Fold Spec discriminator; they are not directly loadable by legacy FoldLab readers.

## 6. Parse authoring source

```sh
python tools/foldspec.py parse-source examples/authoring/named-fold.foldsrc -o build/named.fold.json
python tools/foldspec.py validate build/named.fold.json
```

This produces a typed authoring graph, not a completed fold animation. The example retains `status: "instructions"` until a compiler binds and validates executable operations.

## Errors

CLI failures return nonzero and write JSON containing `error`, `message` and, where available, `path` to stderr. Examples include `E_SCHEMA`, `E_REFERENCE`, `E_STRAIN`, `E_TEAR`, `E_PACKAGE_HASH` and `E_SOLVER_UNSUPPORTED`. Read [diagnostics](../spec/19-diagnostics-and-conformance-tests.md).

`--schema-only` checks the document structure and deliberately skips references, geometry and assets. Do not use that flag to claim complete validity.
