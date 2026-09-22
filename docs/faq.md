# Frequently asked questions

## Is this a replacement for a 3D engine?

No. It is a data contract with reference tools. A 3D engine renders the resulting geometry; an authoring compiler solves intent; a player coordinates lessons and media. They are deliberately separate.

## Is it compatible with my existing FoldLab application?

Not directly. This draft uses a new `format` discriminator, explicit millimeter coordinates and a separated operation/step model. Implement the new reader or an adapter described in [migration](migration.md). Merely renaming an archive is unsafe.

## Why both readable source and JSON?

Named declarations make construction relationships easier to author. JSON gives editors, validators and other languages a portable structural form. Both preserve intent; resolved operations are what allow deterministic playback without reconstructing every decision.

## Are all seven alignment families implemented by the supplied solver?

Their constraints and witness semantics are documented. The helper enumerates four families and validates witnesses for all seven. It explicitly rejects unsupported higher-family enumeration. This is not a complete solver or source-to-motion compiler.

## Can a JSON Schema prove the crane is correct?

No. It checks structure. Additional checks cover references, material topology, selected seams, interpolation strain and sampled continuity. They do not establish a collision-free path, finite-thickness feasibility, a natural-looking render or a successful real-paper lesson.

## Is the crane example complete?

It has all 44 instructional steps and resolved data for all 40 operations in the supplied geometric demonstration. It also has documented approximations for advanced shaping. Its full text copy is not a claim of blind-user testing, and the finished crane is not a physically certified pattern.

## Does “resolved” mean “physically validated”?

No. It means the file has the motion representation it declares, with no hidden unauthored physical step in that complete sequence. Review/collision/physical usability are independent. An implementation must preserve the limitations instead of promoting the status to a stronger claim.

## Can I distribute an artistic background or narration?

Declare assets with rights, sizes and hashes. Backgrounds in packages are embedded. Remote narration requires explicit user/host policy and a matching transcript; validation does not fetch it. An external asset still needs appropriate distribution permissions. Hashes detect changed bytes, not ownership or trust.

## Why are mountain and valley lines different in printed templates?

This draft explicitly supports the requested mountain-solid/valley-dashed template convention, always with a legend. It is not labelled a universal origami diagram standard. Normal viewers can use subtle guides and stronger active emphasis without changing the intrinsic crease assignment.

## Do I need special fonts or an account?

No. Documents do not carry user accounts, credentials, analytics or font binaries. A viewer may offer locally installed fonts and accessible spacing preferences. Installed command-line tools validate offline using bundled schemas.

## Can I use the references to mirror an instruction website?

A source URL or a model being described as traditional does not grant rights to reproduce the site's wording or diagrams. Retain rights/provenance and obtain the necessary permission. This repository contains original example prose and does not bundle a site mirror.
