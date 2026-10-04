# FINAL_REPORT — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004

RUN_ID: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004
RUN_CLASS: LOAD_BEARING | MODE: STATIC-ONLY (client never launched; raw byte reads +
independent x86 byte verification only) | Executor: pe-reconstruction (PE-MASTER
bounded worker contract; NO_NESTED_TASKS; fresh dispatch — the previous session
returned empty with zero disk artifacts, so this session performed the full run).

## MISSION AND RESULT

Fix EXACTLY the two P2 findings (C1: QC-7 claim/validation; C2: class-selector vs
property-tag conflation) and the tied P3 wordings of the R1 package
(PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004, published at 4c12053),
driven by the independent Desktop post-audit
(PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_DESKTOP_POST_AUDIT_20261004, REPORT.md
SHA256 015F3C88...; its QC_COUNTEREXAMPLE files prove a deliberate A/B-documentation
swap PASSED the published QC-7 with byte-identical PASS output — falsifying the
gate's declared scope).

**COMPLETE. Both P2s corrected; all tied P3s corrected; the canonical S1 result
preserved unchanged; NO new placement science executed; one bounded targeted QC
(QC_SCOPE=SELF_CHECK_REPORT_QC_HANDOFF_CORRECTION, 10/10 PASS) plus a two-case A/B
mutation falsifier (DETECTED) now guard the corrected claims.**

## C1 — what was fixed

1. **Concept split**: the R1 QC-7 gate is now named and scoped
   **PAYLOAD_FIELD_DECODE_CHECK** (physical payload values at fixed file offsets —
   all it ever did); the payload→template-field mapping is guarded by a NEW
   **CLIENT_DESTINATION_MAPPING_CHECK** (03_SCRIPTS/qc_targeted.py TQ2) that parses
   the documented destination table and byte-verifies every documented destination
   against the pinned-EXE store instructions:
   payload[1]→template+0x08 (MOV [EDI+0x08],EAX = 89 47 08 @0x00730CE6) and
   payload[2]→template+0x04 (MOV [EDI+0x04],EAX = 89 47 04 @0x00730D14), plus
   id2 (89 07 @0x00730CB6), C (89 47 0C @0x00730D42), D (FLD D9 04 10 @0x00730D69 +
   FSTP D9 5F 10 @0x00730D70). "Payload value == expected value" is no longer
   claimed as destination proof.
2. **Mutation falsifier** (01_RAW/QC_MUTATION_AB_SWAP.json): with the documented A/B
   destination mapping intentionally swapped (Desktop-replica destination-cell swap
   AND a fully self-consistent swap) while the raw VFS values stay unchanged, the
   CLIENT_DESTINATION_MAPPING_CHECK **FAILS** — both mutants DETECTED. The
   Desktop-counterexample blind spot is closed.
3. **Instruction starts corrected** (each byte-verified from the pinned EXE this
   run; negative controls prove the old addresses hold operand bytes, not
   instructions): MOV [EDI+4],EAX @0x00730D14 (NOT D16); MOV [EDI+C],EAX @0x00730D42
   (NOT D36); FLD [EDX+EAX] @0x00730D69 (NOT D6D; the FSTP site @0x00730D70 was
   already correct). The A→+0x08 / B→+0x04 mapping itself is UNCHANGED and valid —
   only the false "verified automatically by QC-7" claim is retracted.
4. **Failure-path description corrected**: FUN_00730C90's flag-cleared/bounds-failed
   paths write **ZERO** to the destination and do not advance the cursor
   (MOV [EDI],EBX @0x00730CC3; MOV [EDI+8],EBX @0x00730CF0; MOV [EDI+4],EBX
   @0x00730D1E; MOV [EDI+0xC],EBX @0x00730D4C; D via FLDZ @0x00730D7A + FSTP
   @0x00730D7C; EBX=0 from XOR EBX,EBX @0x00730C96). FUN_0040DE60 byte-decoded:
   ADD [ECX+0xC],EAX; CMP EAX,[ECX+8]; JBE +4; else MOV BYTE [ECX+0x11],0 — it
   ZEROES the cursor flag after exceeding the limit. The prior "another cursor mode
   stores the same valid value / both paths verified" claim is retracted as FALSE.
   Normal-path A/B mapping remains valid.

## C2 — what was fixed

All wording equivalent to "0x4E26 property" / "20006-family property id" is replaced
by the layered identity, byte-verified this run:
**CLASS_SELECTOR = 0x4E26 = 20006** (pair constant at MOV [ESP+0x1C],0x4E26
@0x004C54C2, resolved with the exact receiver by the wrapper CALL FUN_00703B80
@0x004C54CE — a class-selector resolve, NOT a property-tag fetch of 20006) vs
**PROPERTY_TAG = 6** (audited normal branch: exact receiver MOV ECX,[EAX+4]
@0x004C551C; PUSH 6 `6A 06` @0x004C551F; CALL FUN_0070C180 @0x004C5523 → returned
descriptor/variant, null-checked @0x004C552B, predicate CMP ECX,1 @0x004C552F, value
read MOV EAX,[EAX+8] @0x004C5539 on the measured branch) → the returned RUNTIME
VALUE is consumed as the FUN_0072F880 lookup key. The alternative flag-0xD82 branch
(PUSH 0xD82 @0x004C54DC → FUN_00844020 @0x004C54E4) is preserved SEPARATE/UNKNOWN;
no claim is made that all getter results come from the normal tag-6 branch.

## NEXT EXPERIMENT (corrected wording, DESIGNED NOT EXECUTED)

Trace the producer/provenance of the SPECIFIC RUNTIME VALUE returned by the
class-selector-20006 / property-tag-6 getter on the exact receiver and branch whose
result is consumed as the FUN_0072F880 lookup key. Allowed provenance outcomes
(OPEN taxonomy, no forced physical-vs-network binary): PHYSICAL_RECORD_DERIVED |
CONSTANT_INITIALIZATION | LOCAL_COMPUTED | CACHE_PROVIDER | MESSAGE_DERIVED |
FALLBACK_BRANCH | UNKNOWN. Now identically worded in FINAL_REPORT.md, HANDOFF.md and
PLACEMENT_CONSUMER_EDGE.md of the R1 package.

## P3 corrections (all in the R1 docs + this ledger)

- Receiver provenance (S-P3-1): FUN_00452490 wrapper (CALL FUN_0043A550 @0x00452490
  → MOV ECX,EAX @0x00452495 → tail JMP FUN_0072FA30 @0x00452497) delivers the
  registry pointer; the loader PRESERVES the incoming ECX (MOV [ESP+0x38],ECX
  **@0x0072FA6B**, bytes 89 4C 24 38 — the Desktop report's @0x0072FA6C is the
  ModRM byte, not the instruction start; recorded as a run deviation with byte
  evidence) and recovers it before the insert (MOV ECX,[ESP+0x3C] @0x0072FBD4;
  insert @0x0072FBE5). The loader does NOT itself call the singleton (0
  FUN_0043A550 call sites in the loader extent).
- Instruction starts (S-P3-2): FUN_0072F580 default MOV EAX,00BA5800 @0x0072F5A5
  (not F5A8); FUN_0072F7F0 node-size MOV [EBP-0x14],0x44 @0x0072F822 (not F825);
  FUN_004C5480 resolver CALL @0x004C54B2 (not 54AD); plus the parser A/B/C/D starts
  above. Operand addresses are never instruction addresses.
- Proprietary-byte census (S-P3-3): no complete original proprietary
  binary/payload FILES were committed; bounded original byte windows / payload
  excerpts used as forensic evidence ARE present (RECORD_A/B payload hex, bounded
  EXE windows in 01_RAW); no NEW proprietary payload beyond those bounded excerpts.
- 4508 scan wording (S-P3-4): zero PUSH-imm32 0x119C in the performed whole-.text
  PUSH scan; the three raw imm32 0x119C occurrences classified as displacement
  operands; computed/indirect/runtime uses NOT excluded — no absence claim beyond
  the measured scan class.

## TERMINAL FIELDS (exact)

```text
BASE_SHA = 4c1205342abd1b051f72fab9932532b1f0ed86fe
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004)
S1_STATIC_MECHANISM = PRESERVED_CONFIRMED
PAYLOAD_FIELD_DECODE_CHECK = PASS
CLIENT_DESTINATION_MAPPING_CHECK = PASS
AB_MAPPING_MUTATION_FALSIFIER = DETECTED
PARSER_FAILURE_PATH_WORDING = CORRECTED
CLASS_SELECTOR_20006_IDENTITY = CONFIRMED
PROPERTY_TAG_6_IDENTITY = CONFIRMED
CLASS_SELECTOR_PROPERTY_TAG_SEPARATION = CORRECTED
NEXT_EXPERIMENT_IDENTITY = SPECIFIC_GETTER_RESULT_PROVENANCE
RECEIVER_PROVENANCE_WORDING = CORRECTED
INSTRUCTION_ADDRESS_CORRECTIONS = COMPLETE
PROPRIETARY_BYTE_WORDING = CORRECTED
STATIC_4508_SCAN_WORDING = CORRECTED
PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
NEW_PLACEMENT_SCIENCE_EXECUTED = NO
NEXT_EXPERIMENT_EXECUTED = NO
CANONICAL_GATE_EFFECT = NONE
```

## Not-superseded canonical result (explicitly preserved, no upgrades)

S1_STATIC_MECHANISM=CONFIRMED; PARSER_TO_RUNTIME_DEFINITION_SEAM=CONFIRMED;
CONTAINER_ROLE=DEFINITION_REGISTRY; RECORD_A {id2=16083, A=410620, B=0, C=0,
D_f32=0.49950098991394043}; RECORD_B {id2=4508, A=296445, B=296446};
SIBLING_KEY_16083_LOOKUP=CONFIRMED_STATIC_CONDITIONAL_PATH;
PLACEMENT_CONSUMER_EDGE=STRONGLY_SUPPORTED (level unchanged);
NAMED_BUILDER_RECORD_A_KEY_IDENTITY=NOT_ESTABLISHED (not upgraded);
PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE=NOT_ESTABLISHED;
WORLD_INSTANCE_SEMANTIC=NOT_ESTABLISHED; WORLD_XYZ_RECOVERED=NO.

## Evidence index (this package)

- `QC_TARGETED_REPORT.md` — the targeted QC records (TQ0..TQ9 + mutation falsifier).
- `01_RAW/QC_TARGETED.json` — 10/10 checks PASS raw record.
- `01_RAW/QC_MUTATION_AB_SWAP.json` — the A/B mutation falsifier (both mutants FAIL,
  raw VFS values unchanged, mutated rows recorded).
- `01_RAW/EXE_BYTE_PROOFS.json` — 11 bounded pinned-EXE instruction windows.
- `03_SCRIPTS/qc_targeted.py` — the bounded instrument (read-only vs originals;
  normal + mutation modes).
- `03_SCRIPTS/make_manifest.py` — the manifest generator (self-excluded manifest;
  scope = committed files minus manifest).
- `SUPERSESSION_LEDGER.md` — the explicit 4c12053-statement → correction-finding →
  corrected-interpretation ledger (S-C1-1..S-C1-5, S-C2-1..S-C2-2, S-P3-1..S-P3-4).
- `CORRECTED_DOC_DELTAS.md` — per-file before→after deltas of the 8 corrected R1 docs.
- `INPUT_IDENTITIES.md` — corpus + mandatory-input identities (incl. the Desktop
  QC_COUNTEREXAMPLE pair — byte-identical SHA256s — and the run's byte-verification
  deviations vs the Desktop report).
- `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` — generated LAST; self-excluded; covers
  every file committed by this run (the new package + the 8 corrected R1 docs +
  AUDIT_ENTRYPOINT.md).

## Honest boundaries

1. SELF_CHECK only (QC_SCOPE=SELF_CHECK_REPORT_QC_HANDOFF_CORRECTION) — no
   independent-QC claim; the PE-MASTER review of this package is pending.
2. STATIC-ONLY: no client launch, no runtime observation, no Ghidra; all instruction
   identities are byte reads from the pinned Entropia.exe with this run's own PE
   mapper (section-table-driven; no offset==RVA assumption).
3. One deviation vs the dispatch text: the loader ECX-preserve site is byte-verified
   at **0x0072FA6B** (89 4C 24 38), not the dispatch/Desktop-cited 0x0072FA6C (the
   ModRM byte). The semantic claim is unaffected; the correction is documented in
   INPUT_IDENTITIES.md and SUPERSESSION_LEDGER.md row S-P3-1.
4. The R1 commit message of 4c12053 is immutable history; its superseded phrasings
   ("0x4E26-property", "NO static 4508 key") are documented in the ledger, not rewritten.
5. The R1 raw JSON evidence (01_RAW/S5_QC_CHECKS.json etc.) is the historical
   measurement record and was NOT altered; the R1 manifest remains the record of the
   R1 publication's file states.
6. Next placement experiment NOT executed (terminal HARD STOP per contract).
