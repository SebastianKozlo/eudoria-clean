# BLAST_RADIUS — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Comparison of this run's results against the prior claims enumerated in contract §15.
No historical report was rewritten; all edges below are in-package.

## Prior claims checked

### 1. The id2-domain membership observation (AMEND_R2_ID2_MEMBERSHIP_20002_48.json)
- PRIOR CLAIM: "At 20002.vfs field/offset candidate +48, 1364/1366 observed values are
  members of the tested id2 domain, with the remaining 2 observed values equal to zero
  (records 1014/1015). This is a membership count." semantic_reference=UNVERIFIED.
- THIS RUN: the raw basis is re-derived in-run and agrees: 1,366 records; the zero
  values occur exactly at records 1014 and 1015 (01_RAW\RECORD_FRAMING_SUMMARY.json,
  value_facts.zero_record_indexes = [1014, 1015]); the +48-decimal == +0x30-hex field
  identity matches (48 = 0x30).
- The run does NOT confirm any id2/template semantics for the value: the traced
  destination is a property slot inside the ArkParameterArmor instance (a pure copy),
  with no lookup, no template-map probe, and no comparison at the traced instructions.
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
- THIS RUN: the consumer gap is PARTIALLY closed for THIS file and THIS field: the
  20002.vfs parse path is now decoded end-to-end (routing + read + store
  byte-confirmed), the write path into the destination slot is proven UNIQUE, and the
  read side is bounded-censused (202 descriptor-lookup sites; 0 static tag-0x11
  readers; reads are runtime-tag-driven). What remains open is the downstream gameplay
  consumption — documented in 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json.

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

## Retractions/supersessions issued by this run
- NONE against any prior REPORT (nothing prior was contradicted at claim level).
- ONE lead-correction (item 2 above), recorded in-package per the LEADS_TO_REVERIFY
  discipline (the contract itself marked it NOT TRUTH).

## Governance fields (unchanged by this run)
Q1_STATUS_CHANGED=NO; PE_MASTER_QUALIFICATION_CHANGED=NO; GATE_B_CHANGED=NO;
M1_CHANGED=NO; M2_CHANGED=NO; M3_CHANGED=NO (this run is a bounded EU935-M3-contribution
workstream; NO milestone crossing/closure).
