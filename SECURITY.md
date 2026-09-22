# Security policy

Treat every imported model, scene, media asset, library and source string as untrusted. The normative [security chapter](spec/18-security-resource-policy-and-privacy.md) defines the bounded document contract; the reference tool is not a sandbox for malicious platform codecs.

No arbitrary code, dynamic plugin import or remote schema fetch is allowed. Validate ZIP entries and expansion limits before parsing, verify all payload hashes, and never extract attacker-selected paths into an application directory. Missing audio is a content state, not permission to run a network job automatically.

For a vulnerability in a published copy, use that hosting repository's private security-reporting channel where enabled. This initial repository has no invented security email or promised response SLA. Avoid publicly attaching credentials, private source models, exploit payloads targeting live services or large decompression bombs.

Report the affected draft/tool version, a minimal safe reproducer, expected failure mode and a proposed regression test. Hash verification detects corruption and tampering relative to a manifest; it does not establish who authored the file or whether its instructions are safe.
