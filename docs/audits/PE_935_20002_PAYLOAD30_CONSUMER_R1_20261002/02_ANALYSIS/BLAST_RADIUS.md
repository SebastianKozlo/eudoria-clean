# BLAST_RADIUS — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Comparison of this run's results against the prior claims enumerated in contract §15.
No historical report was rewritten; all edges below are in-package.
Correction state: DESKTOP_CORRECTION_R1 (the branch-selection supersession added as
item 7; items 1-6 stand as corrected by AMEND-R1; the JOIN R1 claim-5 advisory
supersession already recorded stays; do NOT edit any historical JOIN R1 file).

## Prior claims checked

### 1. The id2-domain membership observation (AMEND_R2_ID2_MEMBERSHIP_20002_48.json)
- PRIOR CLAIM: "At 20002.vfs field/offset candidate +48, 1364/1366 observed values are
  members of the tested id2 domain, with the remaining 2 observed values equal to zero
  (records 1014/1015). This is a membership count." semantic_reference=UNVERIFIED.
- THIS RUN: the raw basis is re-derived in-run and agrees: 1,366 records; the zero
  values occur exactly at records 1014 and 1015 (01_RAW\RECORD_FRAMING_SUMMARY.json,
  value_facts.zero_record_indexes = [1014, 1015]); the +48-decimal == +0x30-hex field
  identity matches (48 = 0x30). The correction re-derivation
  (01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json) independently
  reproduces the same zero-record set [1014, 1015].
- The run does NOT confirm any id2/template semantics for the value: the traced
  destination is a property slot inside the ArkParameterArmor instance (a pure copy),
  with no lookup, no template-map probe, and no comparison at the traced instructions.
  id2-domain correlation stays CANDIDATE / UNVERIFIED (numeric-domain overlap is not
  semantic proof).
- VERDICT: PRIOR_CLAIMS_UNCHANGED (the prior claim carried semantic_reference=UNVERIFIED
  and no significance language; nothing to retract or narrow). CONTEXT ONLY — no new
  membership-style comparison was performed in this run (per §A S7, the AMEND-R2
  Appendix A control apparatus was not invoked because no membership claim was made).

### 2. The §B prior-evidence lead "record layout FUN_00959090 (0x58-byte elements)"
- LEAD (not a claim): FUN_00959090's family as the candidate 20002.vfs record-layout
  parser with "+0x2C/+0x30-class cursor reads".
- THIS RUN: the lead is CORRECTED (narrowed to its actual file): the
  FUN_0094dfc0/FUN_0094e1d0/FUN_0094bd30/FUN_00959090 family's filename chain builds
  "Data\Parameters\" + "EnvironmentZones" + ".vfs" (FUN_00958d90 string byte-proven)
  with its own singletons (DAT_00ba8df4/DAT_00ba8df8); its element consumption profile
  (84 cursor bytes) is incompatible with 20002.vfs's 56-byte records. The actual
  20002.vfs parse is the class-property TLV machinery (FUN_00726900 family).
- VERDICT: PRIOR_CLAIMS_NARROWED — the lead was explicitly LEADS_TO_REVERIFY in the
  contract and was never asserted as truth; this run replaces it with the verified
  chain (02_ANALYSIS\VFS_TO_PARSER_TRACE.md §6). No historical text changes; the
  correction lives in this package.

### 3. WORLD_INSTANCE_TO_MODEL_LINK = NOT_DEMONSTRATED (§3 baseline)
- THIS RUN: unchanged. The trace found a property-storage mechanism; no
  world-instance->model edge was claimed, tested, or demonstrated. The value is not
  shown to reference any model/resource/world object.

### 4. PLACEMENT_SOURCE = NOT_RECOVERED (§3 baseline)
- THIS RUN: unchanged. No placement data was sought or recovered; no coordinate
  interpretation was applied to the value (the traced operation is a copy into a
  property slot).

### 5. JOIN R1 UNRESOLVED §2 (consumers of the parsed parameter arrays NOT decoded)
- THIS RUN (DESKTOP_CORRECTION_R1 state): the consumer gap REMAINS OPEN, honestly
  stated: the 20002.vfs parse path is decoded end-to-end INCLUDING the corrected
  branch selection (routing + the SELECTED reader + store byte-confirmed; the virtual
  branch to the ArkRTTraitsInt reader FUN_009777F0 is the proven selected path), the
  parse-side write path into the destination slot is proven unique WITHIN the
  censused machinery, and the read side is bounded-censused (202 descriptor-lookup
  sites; 0 static tag-0x11 readers identified; reads are runtime-tag-driven).
  DOWNSTREAM_CONSUMER_IDENTIFIED = NO; RUN_STATUS = CONSUMER_UNREACHED. What remains
  open is the downstream gameplay consumption — documented in
  02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json.
  (The pre-correction "PARTIALLY closed" phrasing rested on the superseded
  selected-reader trace; the corrected statement above does not.)

### 6. Loader-chain VAs from JOIN R1 PE_MASTER_REVIEW claim 5 (CONFIRMED there at code level)
- The class-ID→"<classID>.vfs" open mechanism is CONFIRMED but lives in FUN_0070c680
  (byte-pinned in-run: 0x70C3FC MOV EAX,[ECX+8]; itoa FUN_0040e900; 0x70C40E
  PUSH ".vfs"; 0x70C742 CALL FUN_00972df0; reader stored at classObj+0x84 @0x70C71E).
- JOIN R1 PE_MASTER_REVIEW claim 5's FUNCTION-LEVEL attribution of that mechanism to
  FUN_0070E810 is CONTRADICTED by the physical bytes (three independent measurements:
  this run's DECOMP/DISASM_FUN_0070e810.txt, the QC byte probes, and PE-MASTER's own
  countercheck): FUN_0070E810 builds a "textures"+".vfs" filename (string "textures"
  @0xA86858; the PUSH imm32 0xA86858 is at 0x70E4AD (0x70E4AC holds 50 = PUSH EAX —
  the QC report's probe VA 0x70E4AC was one byte early; PE-MASTER correction); CALL
  FUN_0070e470 @0x70E866; open CALL FUN_00972df0 @0x70E8B6) and contains NO call to
  the itoa function FUN_0040e900 (PE-MASTER whole-.text census: exactly 5 call sites
  of FUN_0040e900 exist, NONE inside FUN_0070E810's window; QC census agrees).
- Additionally the FUN_0094BD30/FUN_00959090/FUN_0094D9B0 "0x58-B array" family cited
  by the same historical claim is the EnvironmentZones.vfs loader (84-byte cursor
  grammar matching EnvironmentZones.vfs's 84-byte payloads — REC0 size field = 84
  measured; string "EnvironmentZones" @0xA9808C, sole code ref @0x958DCE), NOT the
  20xxx parameter channel; the 0x58-byte ArkParameterArmor INSTANCES of this run are
  a different machinery (a size coincidence).
- VERDICT: PRIOR_CLAIMS_NARROWED (mechanism confirmed; JOIN R1 claim 5's function
  attribution corrected in-package; the second lead-correction alongside item 2). No
  historical file is rewritten; the supersession of the historical attribution is
  recorded here and in 06_REPORT\PE_MASTER_REVIEW.md (PE-MASTER verdict) — a future
  amendment of the JOIN R1 package itself requires separate human authorization.

### 7. DESKTOP P1 (added by DESKTOP_CORRECTION_R1): THE SELECTED-READER TRACE — BRANCH SELECTION
- PRIOR CLAIM (this run's own pre-correction state, superseded): the value read for
  tag 0x11 is performed by FUN_00412540 (READ @ VA 0x00412553 / STORE @ VA
  0x0041255A), reached via "FUN_0075f660 -> flags bit0 test @0x75F687 -> scalar path
  -> FUN_004129c0 -> case type 1"; REPORT RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED;
  the QC rounds 1/2 verified that trace's BYTES (all correct) and accepted it.
- DESKTOP COUNTEREXAMPLE (human-side ChatGPT Desktop post-audit verdict
  REQUIRE_CORRECTIONS): the dispatch FUN_0075f660 tests [descriptor+0] FIRST; a
  non-NULL descriptor+0 selects the VIRTUAL branch, and the flags-bit0/typed-reader
  path is only a FALLBACK (requires descriptor+0 == NULL).
- THIS CORRECTION (DESKTOP_CORRECTION_R1, byte-proven; full chain in
  01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json, 96/96 pins):
  the tag-0x11 descriptor's +0 field holds the static ArkRTTraitsInt reader object
  0x00BA937C (returned by the factory FUN_00977a50 on both paths — never NULL), so the
  VIRTUAL BRANCH IS SELECTED: the read/store pair is FUN_009777F0 @ VA 0x00977807
  (8B 04 10) / @ VA 0x00977810 (89 02); the reader object's RTTI class is
  ArkRTTraitsInt (`.?AUArkRTTraitsInt@@`); the fallback FUN_00412540 pins are
  re-classified BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH
  (01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json).
- SUPERSEDED ITEMS: the active selected-reader trace (FUN_00412540 @0x00412553 /
  0x0041255A) — superseded; the REPORT transcription
  "READ_INSTRUCTION_FILE_OFFSET = 0x00125553" — superseded (digit-shift error; the
  correct fallback offsets are 0x12553/0x1255A, and the SELECTED reader's offset is
  0x00577807); the QC rounds 1/2 selected-reader CONCLUSION — superseded (their
  reports are immutable historical records; their byte verifications remain correct);
  the REPORT/HANDOFF RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED —
  superseded by CONSUMER_UNREACHED (the destination slot is not a downstream
  consumer; the downstream-consumer axis is honestly NO).
- VERDICT: SELF-CORRECTION ISSUED BY THIS PACKAGE (the active artifacts were corrected
  in-place with BEFORE copies preserved; no historical JOIN R1 / QC / control file was
  rewritten). LESSON recorded (contract §8): **"correct instruction bytes != proven
  selected execution/parser path"** — byte-correct pins of an instruction do not prove
  that the instruction's path is selected; path selection must be proven by
  control-flow reachability from the proven dataflow state (here: descriptor+0 != NULL).
- Reconciliation with items 2/6: this item is the THIRD correction of the same class
  family (a reader/parser attribution corrected by physical bytes): item 2
  (FUN_00959090 -> EnvironmentZones.vfs) and item 6 (FUN_0070E810 -> textures) each
  corrected a FUNCTION-LEVEL attribution; item 7 corrects a PATH-SELECTION
  attribution. All three live in-package; none rewrites historical JOIN R1 or QC text.

## Retractions/supersessions issued by this run
- NONE against any prior REPORT outside this package (nothing prior was contradicted
  at claim level beyond the items above).
- ONE lead-correction (item 2) and ONE historical-attribution narrowing (item 6),
  both recorded in-package per the LEADS_TO_REVERIFY discipline.
- ONE self-supersession (item 7, DESKTOP_CORRECTION_R1): this package's own
  pre-correction selected-reader trace and RUN_STATUS — corrected in-place with the
  BEFORE copies preserved; the QC1/QC2 selected-reader conclusions are recorded as
  SUPERSEDED (their reports immutable; see 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md).

## Governance fields (unchanged by this run)
Q1_STATUS_CHANGED=NO; PE_MASTER_QUALIFICATION_CHANGED=NO; GATE_B_CHANGED=NO;
M1_CHANGED=NO; M2_CHANGED=NO; M3_CHANGED=NO (this run is a bounded EU935-M3-contribution
workstream; NO milestone crossing/closure).
