# Handoff — PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913

Audited: 24d7669 → 5d0edde → 78cd153. Desktop verdict: Phase A corrections supported in checked scope; Phase B PARTIAL_PASS / REQUIRE_CORRECTIONS. No milestone promotion.

- F1 P1: 007343E0 returns the input cursor and reads a mask-controlled float structure into rec+0x0C; the subcursor claim is false. Field semantics remain unresolved.
- F2 P2: creator 004C46C0 adjusts the third position component via 00853A80 before constructing variants 3–7. This branch already existed in executor analysis but disappeared from the final provenance summary.
- F3 P2 in the human summary: static buildings were not demonstrated in the channel; they were not excluded from it.
- Minor: actual EXISTING position call 004C488A; byte table 38 indices; current gate interpretations must supersede stale GB4 fields.

Preserved evidence: class registration 54+1; mangling 36/36; RTTI MovableObject/ClientMovableObject; four processor call sites; insert/key trace; T6 64/64; VFS 5438/0 CRC; manifests 129+210 files; historical local corpus 1385/1385 matches snapshots.

Next: PROMPT_OPENCODE.txt. Correct grammar/provenance first; trace the provider behind 00853A80 to determine whether it reads terrain/collision data; bounded same-instance model bridge +0xC0. Network upstream and historical coordinates remain open. Runtime requires a separate GO.

Read AUDYT.md and probe.json for scope and limitations. Synthetic arithmetic witnesses are not target execution. Do not rerun the snapshot-locked probe by resetting the active repository.
