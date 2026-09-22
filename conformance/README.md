# Conformance fixtures

`cases.json` is a language-neutral manifest. Each case identifies an input file, the affected profile, whether the input should be accepted, and the expected first reference diagnostic for an invalid case. Other implementations may report additional errors, but must not accept an invalid document as valid for that profile.

Run all checks with `python tools/check.py` from the root. `tests/test_fixtures.py` runs this manifest through the supplied reader. Other test modules cover operations, mathematical branch selection, presentation seams, parser AST equivalence, safe packages and the crane.

The manifest fixtures deliberately isolate small failures. They are not a complete conformance certification suite, and a successful run must be interpreted alongside `IMPLEMENTATION-STATUS.md`. Invalid files are not normal example packages; do not publish them as valid models.

The current corpus tests structural and semantic failures, not live attacks against external services. Never add enormous decompression bombs, secrets or copyrighted site mirrors as test inputs.
