# SUPERSESSION_LEDGER — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004

Governance form (per the dispatch order): **4c12053 original statement → correction
finding → corrected canonical interpretation.** The original statements below are
VERBATIM from parent commit `4c1205342abd1b051f72fab9932532b1f0ed86fe` (the R1
publication). Original evidence of every mistake is preserved in git history and in
the CORRECTED_DOC_DELTAS.md before/after quotes; nothing was silently rewritten.
The R1 raw JSON evidence (01_RAW/*), R1 scripts (03_SCRIPTS/*), and the R1 manifest
(22-row COMMITTED_PACKAGE_MANIFEST_SHA256.csv — the record of the R1 publication's
file states) are READ-ONLY history and were NOT modified by this correction.

Source of the correction findings: the independent Desktop post-audit
PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_DESKTOP_POST_AUDIT_20261004 (REPORT.md
SHA256 015F3C88...; verdict REQUIRE_CORRECTIONS_IN_REPORT_QC_AND_HANDOFF_SCOPE —
C1/P2 + C2/P2 + tied P3), re-verified independently from the pinned EXE bytes by
this run (01_RAW/QC_TARGETED.json; 01_RAW/EXE_BYTE_PROOFS.json), including the
Desktop QC counterexample (byte-identical PASS outputs under a deliberate A/B
destination-documentation swap — INPUT_IDENTITIES.md).

## C1 (P2) — QC-7 claim and destination validation

### Row S-C1-1 — QC-7's declared scope
- ORIGINAL (4c12053, QC_REPORT.md QC-7 row): "Parser raw↔decoded roundtrip: ...
  re-parsed from raw bytes **with the byte-decoded destinations**; ..."
- CORRECTION FINDING: FALSE-SCOPE claim. The qc7 gate in 03_SCRIPTS/s5_qc_checks.py
  reads the physical payload bytes at fixed file offsets via `struct.unpack_from`
  and compares against hardcoded expected values; it never reads FUN_00730C90's
  destination instructions and never reads the documented destination table. The
  Desktop counterexample (QC_COUNTEREXAMPLE_published_document.json ==
  QC_COUNTEREXAMPLE_deliberately_wrong_destination_document.json, same SHA256
  2109FEA4...) proves a deliberate A/B destination swap in PARSER_CHAIN.md leaves
  the published QC output byte-identical (8/8 PASS).
- CORRECTED INTERPRETATION (QC_REPORT.md now): the gate is renamed
  **PAYLOAD_FIELD_DECODE_CHECK** and its scope is declared as exactly that
  (physical payload values at fixed offsets). The payload→template-field mapping is
  verified by a NEW dedicated check — **CLIENT_DESTINATION_MAPPING_CHECK** (this
  package, 03_SCRIPTS/qc_targeted.py TQ2), which parses the documented destination
  table and byte-verifies every documented destination against the pinned-EXE store
  instructions, and carries a two-case **A/B mutation falsifier**
  (01_RAW/QC_MUTATION_AB_SWAP.json: both the Desktop-replica destination-cell swap
  and a fully self-consistent swap FAIL the check while the raw VFS values stay
  unchanged → AB_MAPPING_MUTATION_FALSIFIER = DETECTED).

### Row S-C1-2 — PARSER_CHAIN.md destination-table verification claim
- ORIGINAL (4c12053, PARSER_CHAIN.md): "Destinations (**verified in QC-7 by
  re-parsing** RECORD_A/RECORD_B raw bytes and matching the established historical
  anchors):"
- CORRECTION FINDING: same C1 falsification — QC-7 does not verify destinations.
- CORRECTED INTERPRETATION (PARSER_CHAIN.md now): "Destinations ([C1-corrected
  verification claim] byte-verified against the pinned-EXE store instructions by the
  correction package's CLIENT_DESTINATION_MAPPING_CHECK ... which retracts the prior
  claim that QC-7 verified the destinations)". The A→+0x08 / B→+0x04 PAIRING itself
  is UNCHANGED and remains valid — only the verification claim is retracted.

### Row S-C1-3 — QC_REPORT.md ANTI-CIRCULARITY #1 FAILURE_CASE
- ORIGINAL (4c12053, QC_REPORT.md): "FAILURE_CASE = a wrong destination pairing
  would have broken the RECORD_B anchor match (detected by QC-7 if so)."
- CORRECTION FINDING: FALSE — the Desktop counterexample is exactly this failure
  case, and QC-7 did not detect it.
- CORRECTED INTERPRETATION (QC_REPORT.md now): the FAILURE_CASE is superseded by an
  honest record of the counterexample, and the detection duty is assigned to the new
  CLIENT_DESTINATION_MAPPING_CHECK whose mutation falsifier FAILS on the swapped
  mapping (both mutants).

### Row S-C1-4 — FUN_00730C90 failure-path description
- ORIGINAL (4c12053, PARSER_CHAIN.md): "a flag-checked slow path
  (`CMP [ESI+0x11],BL`) handles the other cursor mode and **stores the same value
  to the SAME destination (both paths verified)**."
- CORRECTION FINDING: FALSE description of client behavior, byte-disproved from the
  pinned EXE: on the flag-cleared/bounds-failed paths the parser stores ZERO
  (`MOV [EDI],EBX` @0x00730CC3; `MOV [EDI+8],EBX` @0x00730CF0; `MOV [EDI+4],EBX`
  @0x00730D1E; `MOV [EDI+0xC],EBX` @0x00730D4C — EBX=0 from `XOR EBX,EBX`
  @0x00730C96; D field via `FLDZ` @0x00730D7A + `FSTP [EDI+0x10]` @0x00730D7C) and
  does NOT advance the cursor; FUN_0040DE60 (advance helper) zeroes the cursor flag
  `[cursor+0x11]` when the advanced offset exceeds the limit `[cursor+8]`
  (`ADD [ECX+0xC],EAX` @0x0040DE64; `CMP EAX,[ECX+8]` @0x0040DE6A; `JBE +4`
  @0x0040DE6D; `MOV BYTE [ECX+0x11],0` @0x0040DE6F). There is NO second cursor mode
  storing the same valid value. (Desktop-established; independently re-verified this
  run — TQ5.)
- CORRECTED INTERPRETATION (PARSER_CHAIN.md now): the zero-write failure-path
  description above; "The normal-path field mapping below is UNCHANGED and remains
  valid." Normal-path A/B mapping unaffected.

### Row S-C1-5 — FUN_00730C90 parser instruction starts
- ORIGINAL (4c12053, PARSER_CHAIN.md + RECORD_A.md): "MOV [EDI+0x04],EAX @0x00730D16"
  / "MOV [EDI+0x0C],EAX @0x00730D36" / "FLD [EDX+EAX] @0x00730D6D" and RECORD_A.md
  "FLD [EDX+EAX]; FSTP [EDI+0x10] @0x00730D6F".
- CORRECTION FINDING: the old addresses pointed at mid-instruction operand bytes
  (operand addresses are never instruction addresses). Byte-verified from the pinned
  EXE: B store `MOV [EDI+0x04],EAX` = 89 47 04 @**0x00730D14**; C store
  `MOV [EDI+0xC],EAX` = 89 47 0C @**0x00730D42**; `FLD [EDX+EAX]` = D9 04 10
  @**0x00730D69**; `FSTP [EDI+0x10]` = D9 5F 10 @**0x00730D70** (the FSTP site in
  PARSER_CHAIN.md was already correct; RECORD_A.md's "@0x00730D6F" was an operand
  byte). Negative controls: the old addresses do NOT contain the claimed instruction
  bytes (TQ6).
- CORRECTED INTERPRETATION: both docs now carry the byte-verified starts; the
  destination PAIRING (A→+0x08 / B→+0x04) is unchanged and valid.

## C2 (P2) — class selector vs property tag

### Row S-C2-1 — the "0x4E26-property" conflation (all instances)
- ORIGINAL (4c12053): PLACEMENT_CONSUMER_EDGE.md "reads the entity's 0x4E26-PROPERTY
  value = the id2", "MOV [ESP+0x1C],0x4E26 @0x004C54C2 ← the 20006-family property
  id"; FINAL_REPORT.md "FUN_004C5480: the entity's 0x4E26-property id2";
  "FUN_004C5480's 0x4E26/20006-family property value"; HANDOFF.md "the entity's
  0x4E26-property id2", "the 0x4E26-property-key provenance", "Decode the WRITERS of
  the 0x4E26 (20006-family) property value"; PLACEMENT_CONSUMER_EDGE.md "who WRITES
  the 0x4E26-property value"; QC_REPORT.md "the 0x4E26 store instruction + the
  property-machinery call targets".
- CORRECTION FINDING: conflated identity. 0x4E26 = 20006 is the **CLASS SELECTOR**
  (the pair constant at `MOV [ESP+0x1C],0x4E26` @0x004C54C2, C7 44 24 1C 26 4E 00 00,
  resolved with the exact receiver by the wrapper `CALL FUN_00703B80` @0x004C54CE —
  a class-selector resolve, NOT a property-tag fetch of 20006); the property tag on
  the audited normal branch is **6** (`PUSH 6` = 6A 06 @0x004C551F; `CALL
  FUN_0070C180` @0x004C5523 → rel32 byte-verified), invoked with the exact receiver
  (`MOV ECX,[EAX+4]` @0x004C551C), and the getter's RETURNED RUNTIME VALUE is the id2
  used as the FUN_0072F880 lookup key. Alternative/fallback branches (flag 0xD82,
  `PUSH 0xD82` @0x004C54DC → FUN_00844020) are preserved as SEPARATE/UNKNOWN; NOT all
  getter results come from the normal tag-6 branch.
- CORRECTED INTERPRETATION: layered identity **CLASS_SELECTOR = 0x4E26 = 20006**
  vs **PROPERTY_TAG = 6** now stated in PLACEMENT_CONSUMER_EDGE.md (the corrected
  chain), FINAL_REPORT.md, HANDOFF.md, QC_REPORT.md; byte-verified TQ3.

### Row S-C2-2 — next-experiment identity
- ORIGINAL (4c12053): "Recommended experiment: decode the WRITERS of the 0x4E26
  property value (the property-write counterparts of the FUN_00703B80/FUN_0042EAD0
  machinery) and determine whether that id2 is ever fed from a physical record —
  if yes ...; if network/runtime-only ..." (FINAL_REPORT.md); equivalent wording in
  HANDOFF.md and PLACEMENT_CONSUMER_EDGE.md.
- CORRECTION FINDING: the experiment identity chased the conflated "property 20006"
  level and forced a binary physical-vs-network outcome.
- CORRECTED INTERPRETATION (all three docs now): trace the producer/provenance of
  the **SPECIFIC RUNTIME VALUE returned by the class-selector-20006 / property-tag-6
  getter on the exact receiver and branch whose result is consumed as the
  FUN_0072F880 lookup key**, with the OPEN provenance taxonomy
  PHYSICAL_RECORD_DERIVED | CONSTANT_INITIALIZATION | LOCAL_COMPUTED | CACHE_PROVIDER
  | MESSAGE_DERIVED | FALLBACK_BRANCH | UNKNOWN (no forced binary). Worded identically
  in FINAL_REPORT.md, HANDOFF.md, PLACEMENT_CONSUMER_EDGE.md (TQ7).

## P3 corrections (tied to this publication)

### Row S-P3-1 — receiver provenance (the loader and the singleton)
- ORIGINAL (4c12053, RECEIVER_INSERTION_CHAIN.md): "The reader loop fetches the
  registry via FUN_0043A550 and keeps it at [ESP+0x3C] (MOV ECX,[ESP+0x3C]
  @0x0072FBD4 before the insert call @0x0072FBE5)."
- CORRECTION FINDING: the loader FUN_0072FA30 does NOT call the singleton. The
  registry pointer arrives as the loader's incoming ECX from the wrapper
  FUN_00452490: `CALL FUN_0043A550` @0x00452490 → `MOV ECX,EAX` @0x00452495 →
  tail `JMP FUN_0072FA30` @0x00452497 (all byte-verified). The loader PRESERVES the
  incoming ECX (`MOV [ESP+0x38],ECX` = 89 4C 24 38 @**0x0072FA6B** — byte-verified;
  the Desktop report's `@0x0072FA6C` is the ModRM byte, not the instruction start —
  see INPUT_IDENTITIES.md deviations) and recovers it before the insert
  (`MOV ECX,[ESP+0x3C]` @0x0072FBD4; insert call @0x0072FBE5). No FUN_0043A550 call
  site exists inside FUN_0072FA30 (bounded extent scan TQ4).
- CORRECTED INTERPRETATION: RECEIVER_INSERTION_CHAIN.md now states the wrapper→loader
  provenance with all five byte-pinned sites and the no-singleton-call census fact.

### Row S-P3-2 — instruction starts (operand bytes are not instruction starts)
- ORIGINAL (4c12053): "MOV [EBP-0x14],0x44 @0x0072F825" (RECEIVER_INSERTION_CHAIN.md,
  QC_REPORT.md QC-8 row); "MOV EAX,0x00BA5800 @0x0072F5A8" (RECEIVER_INSERTION_CHAIN.md);
  "FUN_00843DD0 @0x004C54AD" (PLACEMENT_CONSUMER_EDGE.md).
- CORRECTION FINDING: byte-verified from the pinned EXE —
  `MOV [EBP-0x14],0x44` = C7 45 EC 44 00 00 00 starts @**0x0072F822** (the R1 QC
  script's byte check already read the bytes at 0x0072F822; only the doc addresses
  were wrong); `MOV EAX,0x00BA5800` = B8 00 58 BA 00 starts @**0x0072F5A5**; the
  resolver `CALL FUN_00843DD0` starts @**0x004C54B2** (E8 19 E9 37 00 → 0x00843DD0;
  @0x004C54AD was the `PUSH EAX` mid-stream).
- CORRECTED INTERPRETATION: all three docs carry the corrected starts, each marked
  C1/P3-corrected with the old address quoted; TQ6 positive+negative byte controls.

### Row S-P3-3 — proprietary-byte census wording
- ORIGINAL (4c12053, HANDOFF.md): "no proprietary payload committed (originals
  represented by era, path, size, SHA256, offsets, bounded window hashes)".
- CORRECTION FINDING: literally false as an absolute — RECORD_A.md/RECORD_B.md carry
  the 28-byte payload hex (as forensic evidence), and 01_RAW/S2/S3 carry bounded EXE
  windows.
- CORRECTED INTERPRETATION (HANDOFF.md now): "no complete original proprietary
  binary/payload FILES were committed; bounded original byte windows / payload
  excerpts used as forensic evidence ARE present in this package ...; no NEW
  proprietary payload beyond those bounded evidence excerpts."

### Row S-P3-4 — 4508 scan wording
- ORIGINAL (4c12053): RECORD_B.md "**No static key**: ... No placement-construction
  function looks up key 4508 statically"; QC_REPORT.md QC-10 "PUSH 0x119C sites = 0 →
  no static 4508 lookup key"; FINAL_REPORT.md "NO static 4508 key exists (all 3 imm32
  hits are ESP/struct displacements; 0 PUSH sites)".
- CORRECTION FINDING: broad absence claim exceeding the measured scan class.
- CORRECTED INTERPRETATION (all three docs now): the measured scope — zero
  PUSH-imm32 0x119C sites in the performed whole-.text PUSH scan; the 3 raw imm32
  0x119C occurrences classified as displacement operands (LEA ECX,[ESP+0x119C] ×2
  @0x0053270C/@0x00532769; MOV [ESI+0x119C],EBX @0x0083427E); computed/indirect/
  runtime 4508 keys NOT excluded by this scan class; no absence claim beyond the
  measured scan. The control's discriminating contrast stands, as measured.

## What is NOT superseded (explicitly preserved)

- S1_STATIC_MECHANISM = CONFIRMED; PARSER_TO_RUNTIME_DEFINITION_SEAM = CONFIRMED;
  CONTAINER_ROLE = DEFINITION_REGISTRY; SIBLING_KEY_16083_LOOKUP =
  CONFIRMED_STATIC_CONDITIONAL_PATH; RECORD_A {id2=16083, A=410620, B=0, C=0,
  D_f32=0.49950098991394043}; RECORD_B {id2=4508, A=296445, B=296446};
  PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED (unchanged level);
  NAMED_BUILDER_RECORD_A_KEY_IDENTITY = NOT_ESTABLISHED;
  PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED;
  WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.
- All R1 raw evidence, R1 scripts, and the R1 manifest (historical record).
- The R1 commit message of 4c12053 is immutable history; its "0x4E26-property" and
  "NO static 4508 key" phrasings are superseded by this ledger's corrected
  interpretations, not rewritten.
