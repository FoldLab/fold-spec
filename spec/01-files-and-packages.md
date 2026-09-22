# 01 · Files and packages

**Normative**

## Encodings and filenames

| Filename | Representation | Purpose |
|---|---|---|
| `name.fold.json` | UTF-8 JSON document | Readable, diffable interchange. |
| `name.foldlab` | ZIP package | One document plus exactly its declared local assets. |
| `name.foldsrc` | UTF-8 Fold Source | Optional readable typed authoring form. |
| `name.foldlib.json` | UTF-8 JSON library | Data-only reusable construction parts. |
| `name.foldscene` | UTF-8 JSON scene | Reusable presentation styling, without model geometry. |

The project/repository name is `fold-spec`. A `.foldlab` suffix is retained for the existing application family, but the root discriminator `format: "fold-spec"` identifies this new contract. Merely changing a filename does not migrate an old file. The `.fold` suffix is **not** claimed: it belongs to the separate geometry interchange described in chapter 17.

Use `application/json` for JSON and `application/zip` for packages when serving files. No new IANA media type is registered by this draft. The example schema URLs under `fold-spec.example` are reserved documentation identifiers, not a deployed service. Tooling MUST resolve bundled schemas offline rather than fetch that domain.

JSON MUST satisfy RFC 8259 [R1], be UTF-8 without a BOM, and have no duplicate object members, lone surrogates, NUL strings, NaN, infinity, or numeric overflow. Object-member order is not semantic; array order generally is. Unknown core fields are rejected rather than treated as misspelled optional settings.

## Archive layout

```text
paper-crane.foldlab
├── manifest.json
├── document.json
└── assets/
    ├── stage.png             # only when declared
    └── narration-01.mp3      # only when declared
```

`manifest.json` has `format: "fold-spec-package"`, the same `specVersion` as the document, `document: "document.json"`, and an `entries` array. Every entry has `path`, `byteLength`, and a lowercase hexadecimal `sha256`. The manifest lists **every payload except itself** exactly once. `document.json` is mandatory. Directory entries are unnecessary and excluded by the core package profile.

A document asset record repeats the asset’s byte length and hash. Both declarations MUST match the actual bytes. No unlisted, unreferenced, or missing payload is allowed in a complete package, including optional assets that were explicitly declared. A hosted optional narration URL is different: it is not a fictitious local asset and is not in the package manifest.

Hashes cover exact stored uncompressed bytes. They detect corruption, not authorship or trust. There is no signature mechanism in the core draft. A signature extension must specify its canonicalization and trust model independently.

## Paths and compression

Paths are ASCII relative POSIX paths with the restricted characters and length defined by the schema. Reject leading slash, backslash, colon, percent-encoded paths, empty segments, `.` or `..`, trailing dots/spaces, platform device names, duplicates and case-folding collisions. `document.json` and `manifest.json` cannot be used as asset paths. Readers MUST NOT extract symlinks, devices, or executable files from a package.

Only stored and DEFLATE compression are supported. Encryption, multi-volume archives and ZIP64 are not part of this bounded profile. Readers enforce limits on declared sizes and actual streamed expansion. Do not allocate a full advertised buffer before checking limits.

The reference policy is 64 MiB compressed, 32 MiB per expanded entry, 128 MiB total expanded, and 258 entries. A document may contain at most 256 assets. These limits are conservative interoperability targets, not hard physical limits on origami complexity.

## Deterministic writing

Writers SHOULD emit manifest first, remaining entries in path order, fixed timestamps, ordinary file permissions, and deterministic JSON serialization. Identical compressed bytes are not required across DEFLATE implementations. The provided writer uses deterministic readable JSON; it is **not** RFC 8785 canonical JSON [R2]. Never describe `sort_keys=True` or a pretty printer as JCS.

The essential equivalence test is decoded document meaning plus exact required asset bytes. A verified round trip may change whitespace without changing the tutorial.

[R1]: https://www.rfc-editor.org/rfc/rfc8259
[R2]: https://www.rfc-editor.org/rfc/rfc8785
