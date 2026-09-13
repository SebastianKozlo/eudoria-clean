# Desktop audit handoff

RUN_ID: PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913
Audited snapshot: 2a2ba8ddc864d16b0b31e6ef7928e0e2af922633
Base: 7053654aa227b913f47ac8b3d6be664f4f302954
Verdict: PARTIAL_PASS / REQUIRE_CORRECTIONS; advisory, no canonical milestone change.

- F1 P1: ArkObjectClass factory receiver was misidentified as templates.vfs record A.
- F2 P2: switch at 008557FD uses getter +8, not template field D +10.
- F3 P1: raw-ID absence cannot exclude FILE/placement semantics.
- F4 P2: 0 labels STATIC_WORLD cannot exclude generic machinery from building loading.
- F5 P2: call-presence predicate does not establish exclusive transform provenance.

Physical checks: 5438 templates, 0 CRC failures; 3618/3618 A/NIF, 1666/1666 B/BVI; 276 portal entries and CRCs, 13 zero raw-pattern counts; S14 64/64; independent PE RTTI/factory and selector witnesses; closure manifest 49/49.
No client execution, new Ghidra run, production changes, original-file writes, or exhaustive external-source recheck.

Read REPORT.md, probe.json and PROMPT_OPENCODE.txt. Local authoring copy: AUDYT.md in the Desktop workspace, identical to published REPORT.md.
Replay probe.mjs on an isolated checkout at the audited snapshot, setting EU935_AUDIT_REPO if needed. Its snapshot assertion deliberately rejects a newer live checkout. Do not reset a shared checkout to replay it.

Next: correct receiver provenance and conclusion scopes, then trace one attribute-origin/model-instance seam. Original runs remain immutable. Separate new run IDs and explicit GitHub publication are included in the prompt. Unknown historical building coordinates remain UNKNOWN.
