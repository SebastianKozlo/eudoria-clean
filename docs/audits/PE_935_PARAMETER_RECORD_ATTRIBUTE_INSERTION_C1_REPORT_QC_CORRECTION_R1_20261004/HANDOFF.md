# HANDOFF — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004

Executor: pe-reconstruction (PE-MASTER bounded worker contract; NO_NESTED_TASKS;
STATIC-ONLY — the client never ran). This is the return-to-parent handoff for the
C1/C2/P3 REPORT-QC correction of the R1 parameter-record package, driven by the
independent Desktop post-audit. Fresh full run (the previous dispatched session
returned empty with zero disk artifacts).

## Result in one paragraph

Both P2s are FIXED and all tied P3s are FIXED, with the canonical S1 result
PRESERVED: (C1) the R1 QC-7 gate's declared scope was corrected to
PAYLOAD_FIELD_DECODE_CHECK (physical payload values at fixed offsets) after the
Desktop QC counterexample proved a deliberate A/B destination-documentation swap
passes it with byte-identical output; a NEW CLIENT_DESTINATION_MAPPING_CHECK now
byte-verifies the documented payload→template destinations against the pinned-EXE
store instructions (payload[1]→+0x08 via 89 47 08 @0x00730CE6; payload[2]→+0x04 via
89 47 04 @0x00730D14; id2/C/D likewise), guarded by a two-case A/B mutation
falsifier that FAILS on the swapped mapping (both the Desktop-replica and the fully
self-consistent mutant) while the raw VFS values stay unchanged —
AB_MAPPING_MUTATION_FALSIFIER=DETECTED; the FUN_00730C90 failure-path description
now states the byte-verified ZERO-WRITE behavior (flag/bounds failures store ZERO,
do not advance the cursor; FUN_0040DE60 zeroes the cursor flag on limit exceed) and
retracts the false "another cursor mode stores the same value" sentence; the parser
instruction starts were corrected (B @0x00730D14, C @0x00730D42, FLD @0x00730D69;
FSTP @0x00730D70 was already correct). (C2) every "0x4E26-property / 20006-family
property id" wording is replaced by the byte-verified layered identity
CLASS_SELECTOR=0x4E26=20006 (pair @0x004C54C2; wrapper CALL FUN_00703B80
@0x004C54CE — NOT a property-tag fetch) vs PROPERTY_TAG=6 (PUSH 6 @0x004C551F; CALL
FUN_0070C180 @0x004C5523) → the returned RUNTIME VALUE → the FUN_0072F880 lookup
key, with the flag-0xD82 alternative preserved SEPARATE/UNKNOWN; the recommended
next experiment is reworded to the SPECIFIC getter-result provenance with the open
taxonomy PHYSICAL_RECORD_DERIVED | CONSTANT_INITIALIZATION | LOCAL_COMPUTED |
CACHE_PROVIDER | MESSAGE_DERIVED | FALLBACK_BRANCH | UNKNOWN. (P3) receiver
provenance corrected (FUN_00452490 wrapper CALL FUN_0043A550 @0x00452490 → MOV
ECX,EAX @0x00452495 → tail JMP FUN_0072FA30 @0x00452497; loader PRESERVES incoming
ECX MOV [ESP+0x38],ECX @0x0072FA6B — byte-verified, the Desktop's @0x0072FA6C is the
ModRM byte — recovers @0x0072FBD4; the loader does NOT itself call the singleton);
FUN_0072F580 default @0x0072F5A5, FUN_0072F7F0 node-size @0x0072F822, FUN_004C5480
resolver CALL @0x004C54B2 corrected; proprietary-byte census corrected (no complete
original FILES; bounded evidence excerpts present); 4508 negative reworded to the
measured scan scope. NO new placement science, NO new VFS, NO third record, NO
record value changes, NO F1-F4, NO model join, NO XYZ, NO network trace. TARGETED QC
(SELF_CHECK_REPORT_QC_HANDOFF_CORRECTION) = QC_PASS 10/10.

## Status block

```text
RUN_ID = PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004
RUN_STATUS = COMPLETE (C1+C2 corrected; P3s corrected; S1 preserved; HARD STOP)
HARD_STOP_REASON = contract terminal state — the next placement experiment
  (specific-getter-result provenance) is DESIGNED_NOT_EXECUTED and NOT authorized
BASE_SHA = 4c1205342abd1b051f72fab9932532b1f0ed86fe
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004)
REMOTE_STATE = actual remote master == 4c12053 at run start (fetch + ls-remote),
  re-verified immediately before the commit, and == local HEAD == origin/master
  after the fast-forward push
AUDIT_OUTPUT_ROOT = docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004/
FINAL_REPORT_PATH = <root>/FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS =
  <root>/01_RAW/QC_TARGETED.json                (10/10 targeted QC checks)
  <root>/01_RAW/QC_MUTATION_AB_SWAP.json        (A/B mutation falsifier, DETECTED)
  <root>/01_RAW/EXE_BYTE_PROOFS.json            (11 bounded pinned-EXE windows)
  <root>/QC_TARGETED_REPORT.md, SUPERSESSION_LEDGER.md, CORRECTED_DOC_DELTAS.md,
  INPUT_IDENTITIES.md, 03_SCRIPTS/qc_targeted.py
CANONICAL_GATE_EFFECT = NONE; M1_CLOSED = NO; NEXT_EXPERIMENT_AUTHORIZED = NO
```

## Changed paths (this publication)

1. NEW package: docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004/
   (FINAL_REPORT.md, HANDOFF.md, QC_TARGETED_REPORT.md, SUPERSESSION_LEDGER.md,
   CORRECTED_DOC_DELTAS.md, INPUT_IDENTITIES.md, COMMITTED_PACKAGE_MANIFEST_SHA256.csv,
   01_RAW/{QC_TARGETED,QC_MUTATION_AB_SWAP,EXE_BYTE_PROOFS}.json,
   03_SCRIPTS/{qc_targeted,make_manifest}.py).
2. Narrowly corrected R1 docs (only the ordered corrections; before→after in
   CORRECTED_DOC_DELTAS.md): PARSER_CHAIN.md, RECORD_A.md, QC_REPORT.md,
   RECEIVER_INSERTION_CHAIN.md, PLACEMENT_CONSUMER_EDGE.md, FINAL_REPORT.md,
   HANDOFF.md, RECORD_B.md (all under docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004/).
3. AUDIT_ENTRYPOINT.md: one new factual row (same publication commit).

## For the PE-MASTER review (suggested falsification targets)

1. Re-run `03_SCRIPTS/qc_targeted.py normal` and `... mutation` — both must
   reproduce QC_PASS 10/10 and AB_MAPPING_MUTATION_FALSIFIER=DETECTED
   deterministically (read-only; no repo mutation).
2. Re-derive the FUN_00730C90 store instructions from the pinned EXE and check the
   corrected PARSER_CHAIN.md table against them; then swap the A/B destination cells
   in any copy and confirm the CLIENT_DESTINATION_MAPPING_CHECK fails (the Desktop
   counterexample class is now closed).
3. Verify the zero-write claims directly: MOV [EDI*],EBX sites at 0x00730CC3 /
   0x00730CF0 / 0x00730D1E / 0x00730D4C with EBX=0; FLDZ+FSTP at 0x00730D7A/0x730D7C;
   FUN_0040DE60's MOV BYTE [ECX+0x11],0 @0x0040DE6F behind JBE @0x0040DE6D.
4. Verify the class-selector/tag-6 separation at the bytes: 0x4E26 imm32 at
   0x004C54C2 vs 6A 06 at 0x004C551F and the FUN_0070C180 rel32 at 0x004C5523 —
   two distinct identities at two distinct sites.
5. Check the supersession ledger against 4c12053 (git show) — every original
   statement must be quoted verbatim and still present in git history.

## Boundaries honored

STATIC_ONLY; no client launch; no runtime instrumentation; no model join; no XYZ;
no 20xxx/24xxx detailed analysis; no second VFS; no third record; no RECORD_A/B
value changes; no runtime-key producer hunt; no Gamebryo F1-F4; no network trace;
no inventory redo; no VFS repars; historical packages read-only except the ORDERED
narrow corrections (all documented in SUPERSESSION_LEDGER.md +
CORRECTED_DOC_DELTAS.md; original mistake evidence preserved); foreign untracked
groups untouched; bounded original byte windows / payload excerpts present as
forensic evidence, no complete original proprietary FILES, no NEW proprietary
payload; path-limited git add only (no `git add .`); fast-forward push, no force.
