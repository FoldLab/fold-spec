# 18 · Security, resource policy and privacy

**Normative**

Treat every imported file as untrusted data. A valid-looking title or checksum does not make its author trusted. Validation is layered: strict parsing, schema, references/statuses, resource bounds, mathematical checks, and safe asset decoding.

## Input handling

Reject duplicate JSON keys, invalid Unicode, excessive nesting, nonfinite/overflowed numbers, unexpected core fields, duplicate identities, path traversal and undeclared assets. Validate before allocating large arrays or creating a renderer. Schemas are bundled and resolved offline; `$ref` in untrusted documents is not a network-fetch instruction.

Never evaluate JavaScript, HTML, arbitrary expressions, SSML or shader code from a model. The optional authoring language is parsed into a bounded AST; it has no ambient filesystem, shell, network or code-import access. Extension payloads are also data.

## Archives and assets

Inspect package entries before extraction. Reject symlinks, device files, encrypted/multi-volume/unsupported archives, duplicate and case-colliding paths, central/local header inconsistencies, corrupted CRCs, hash mismatches, and expansion beyond policy. Streaming expansion must have its own byte budget, independent of claimed sizes.

Static images must have supported signatures and consistent metadata, decoded dimensions and chunk structure before display. Use a maintained sandboxed/platform decoder, decoded-pixel budgets and cancellation of superseded jobs. Audio decoders also need size/duration policies. The reference tool’s signature/PNG-CRC checks do not certify every codec implementation against malicious input.

The reference package limits are 64 MiB compressed, 32 MiB per payload, 128 MiB expanded and 258 entries; JSON nesting is capped at 96 in its parser. Raster decoding is capped at 8192 per side and 16,777,216 pixels in the reference PNG preflight. Implementations may enforce lower limits but should report `E_LIMIT`, not pretend the geometry was invalid.

## Remote resources

Core geometry, libraries and required stage resources are local assets. Optional hosted narration is HTTPS and opt-in. Do not fetch anything simply because a link appears in metadata or history. A renderer validating offline must stay offline.

Server-side audio/image helpers must reject internal/private network destinations, embedded credentials, unexpected redirects, unsupported media types and unlimited responses. Client-side fetches must not leak credentials or bypass browser origin policies. CORS errors are errors, not permission to build an unrestricted proxy.

## Privacy and caching

Local projects, generated thumbnails, audio preferences and accessibility settings can reveal personal information. Do not upload them for caching, history lookup or telemetry without permission. A document must not embed the current user’s private notes, browsing progress, access tokens or account identity by default.

A thumbnail cache should be keyed by relevant source revision/render inputs, bounded and clearable. Export checksums should not be repurposed as cross-site tracking identifiers. Per-user playback progress stays separate from shared model files.

## Review and disclosure

Security findings need minimal reproductions with secrets removed. This local repository has no published private-reporting service yet; use your deployment’s private maintainer channel rather than posting exploitable payloads publicly. A parser passing bundled fixtures is not a guarantee against all malicious files.
