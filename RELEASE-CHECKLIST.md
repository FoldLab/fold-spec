# Release checklist

## Before changing a version

- Confirm normative text, schemas, grammar and reference semantics agree.
- Explain migrations and unsupported capabilities. Keep prior versions immutable.
- Review source rights, external references and all user-tested claims.
- Add positive, negative, ambiguity, numerical-boundary and security examples.

## Build and verify

- Rebuild schemas and generated field documentation.
- Run `python tools/check.py` from a clean checkout with installed dependencies.
- Build the offline site and inspect its navigation, tables, code blocks and local links.
- Validate every example and inspect every `.foldlab` package against its readable source.
- Reproduce the crane's reported step/operation/strain measurements without claiming physical verification.
- Record Python/dependency versions, actual counts and implementation boundaries in `VERIFICATION.md`.

## Package

- Include original source, normative prose, schemas, examples, tests, generated offline documentation and licenses.
- Exclude `.venv`, `__pycache__`, arbitrary downloads, credentials and font binaries.
- Write SHA-256 hashes for included files, excluding the hash manifest itself.
- Create a real ZIP with a `fold-spec/` root directory.
- Test CRC, extract to a fresh directory, verify every file hash, and rerun the check command there.
- Confirm the exact downloadable path exists before publishing its link.

## Stable release gates beyond this draft

A full symbolic compiler, library expander, robust local overlap/contact validation, graphical reader, interoperable PDF output, and real paper/accessibility testing are separate implementation projects. Do not mark them complete because this reference draft passes its included corpus. Seek independent implementation evidence before a stable conformance claim.
