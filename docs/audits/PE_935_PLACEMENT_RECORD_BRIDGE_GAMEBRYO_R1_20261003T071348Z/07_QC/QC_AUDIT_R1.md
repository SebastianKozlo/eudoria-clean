# QC_AUDIT_R1 — INDEPENDENT FRESH-CONTEXT INTERNAL QC — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

- QC_RUN_ID: PE_935_PLACEMENT_RECORD_BRIDGE_QC_R1_20261003 (fresh-context, this document)
- AUDITED_RUN: PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
- RUN_CLASS (audited): LOAD_BEARING (per POM A1.2 → fresh deep QC)
- QC EXECUTOR: pe-master-auditor (fresh context; not the run's executor; no Task nesting)
- MODE: STATIC_ONLY (no client launch, no dynamic instrumentation, no Ghidra project
  touch — QC re-derives from raw bytes with its own independent python tooling)
- CONTRACT_VERIFIED: SHA256 AB192885E28B989522CB7B62658D2BAD0A693096CDEE94D0313B638F7ECA4C76,
  17211 B — MATCH (re-measured by QC at start).
- INPUT_BUILD_VERIFIED: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31,
  8,015,872 B — MATCH (re-measured by QC).

## QC_VERDICT: **QC_PASS_WITH_FINDINGS**

Reason: every load-bearing claim of the audited run was independently re-derived
and CONFIRMED (byte-level, with QC's own PE mapper / VFS walker / BNT2 index
parser / call-site scanner / RTTI chain walker — no executor code reused); all
five controls were executed as declared; all hard limits honored; no claim is
downgraded or retracted by QC evidence. Three documentation-level findings
remain (1 × P2 internal-consistency drift in the final report's COVERAGE
number; 2 × P3 textual defects in TRACE_EDGE_BLOCKS). None affects
RESULT_LEVEL, any E1–E12 claim, any control status, or the honest
Level-B outcome. They fit the contract's one bounded repair round
(QC_REPAIR_ROUNDS_MAX = 1) as textual corrections before publication.

---

## 1. FINDINGS

### P2-1 — COVERAGE census denominator in DRAFT_FINAL_REPORT.md is inconsistent with the package's own raw data (69 vs 45)

- FILE/LINE: `06_REPORT/DRAFT_FINAL_REPORT.md`, line 29–31 ("COVERAGE = own
  machine census: 19+10+8+4+4+8+4+12 = 69 census-target caller enumerations").
- CLAIM CONTRADICTED: the census-coverage number of the run.
- PHYSICAL COUNTER-EVIDENCE (QC's own count from the package's RAW JSONs):
  `C2_CALLER_CENSUS.json` targets = 19; `C4_CONSTRUCTION_TRACE.json` census = 10;
  `C5_LAYOUT_AND_DRIVERS.json` census = 4; `C6_DRIVER_SOURCES.json` census = 8;
  `C8_TOP_SOURCES.json` census = 4. Sum = **45**, not 69. The arithmetic
  "19+10+8+4+4+8+4+12" does not reconstruct from any countable census in the
  package. `02_ANALYSIS/NOT_CHECKED.md` line 65 itself states the correct
  number: "45 census target lookups with caller enumeration" — so two
  different totals for the same coverage coexist in one package.
- BLAST RADIUS: metadata field COVERAGE in the final report only. No E-claim,
  control, RESULT_LEVEL, or count used elsewhere depends on "69" (the
  per-target denominators cited in TRACE/SELECTION/CONTROLS are all correct and
  independently confirmed: T01 25/23, T04 55, T05 13/11, T06 2, T07 1, T09 2,
  T02 1, T11 1, T12 4, T13 7/6, T15/T16/T17 15/11/7, T03 0+1 noncall,
  T19 0+1; K/M/N/P census chains all confirmed).
- EXACT CORRECTION: in the repair round, change the DRAFT_FINAL COVERAGE census
  sentence to the reconstructable total: "own machine census: 19+10+4+8+4 = 45
  census-target caller enumerations (denominators per target in the
  C2/C4/C5/C6/C8 JSONs)". (Keep the 962/962, 113/113 and 88-detailed counts —
  all confirmed below.)
- REVALIDATION PREDICATE: `sum(len(targets) for C2) + sum(census keys in
  C4,C5,C6,C8) == 45` AND the string "69 census-target" no longer appears in
  06_REPORT.

### P3-1 — Wrong instruction-byte string for PUSH 0x3ED3 in TRACE_EDGE_BLOCKS.md E9(a)

- FILE/LINE: `02_ANALYSIS/TRACE_EDGE_BLOCKS.md`, E9 block, bullet (a):
  "FUN_005B6597: 68 2D 3E 00 00  PUSH 0x3ED3".
- PHYSICAL COUNTER-EVIDENCE (QC byte read at VA 0x005B6597 via own PE mapper):
  `68 D3 3E 00 00 E8 EF F9 FF FF` = PUSH 0x3ED3; CALL → 0x005B5F90 (rel32
  re-derived by QC). "2D" is a leftover of the c10-v1 signed-hex transcription
  (−0x2D → 0xD3) that the run's own CONTROL-4/c10v2 fixed in the data
  (`C10V2_BYTE_CROSSCHECK.json`: "0x005B6597 raw_imm32 0x00003ED3 … match"):
  true) — but the corrected byte value did not propagate into the prose of
  TRACE_EDGE_BLOCKS.
- BLAST RADIUS: cosmetic — the opcode (68), imm32 (0x3ED3 = 16083), call
  target, and E9(a) conclusion are all correct; the machine pin cited
  (L16/c10v2) is correct. But the string is a load-bearing document quoting a
  byte it does not contain.
- EXACT CORRECTION: replace "68 2D 3E 00 00" with "68 D3 3E 00 00" in E9(a).
- REVALIDATION PREDICATE: grep TRACE_EDGE_BLOCKS.md for "2D 3E" → 0 hits;
  own byte read at 0x005B6597 still "68 D3 3E 00 00".

### P3-2 — Slot-flag numbering inverted in E9(c)/TRACE vs the R08 decompilation

- FILE/LINE: `02_ANALYSIS/TRACE_EDGE_BLOCKS.md` E9(c) ("for flag-2 slots: id2
  from property machinery …") — same phrasing echoed in DRAFT_FINAL
  OBSERVED_OPERATION ("runtime attributes (class-20006 property tag 6)") is
  fine; only the flag number is at issue.
- EVIDENCE (QC read of R08 `FUN_00848EA0` in C3_DECOMP.json): the id2 →
  lookup → FUN_0072FE30 → lerp path executes when `FUN_00745540(1)` returns
  TRUE (flag 1); the per-slot {u16@+0xC, float@+0x10} copy executes under
  `FUN_00745540(2)` (flag 2). The TRACE text swaps the two numbers.
- BLAST RADIUS: none on mechanics — the structure, offsets, consumer chain
  (Q05 0x4E26=20006, FUN_007376A0, FUN_0070C180(6), W04 0x24 gate, W03 lerp
  out=a+t*(b−a), Q04 0x18 stride, Q06 +0x1C+slot*4) are all confirmed by QC
  decompilation reads; E10's "slot object class UNKNOWN" honesty is unaffected.
- EXACT CORRECTION: "for flag-1 slots: id2 from property machinery…"
  (and, if touched, the matching phrase "reads per-slot {u16@+0xC,
  float@+0x10}" → flag-2).
- REVALIDATION PREDICATE: R08 branch test re-read: id2 path under
  FUN_00745540(1).

### P3-3 — NOTE (no correction required): getter census 817 (Ghidra) vs 808 (raw-byte scan)

- C2 T10 reports "817 CALL callsites / 367 unique callers" (Ghidra xref census).
  QC's independent raw scan of `.text` (every `E8 rel32` → 0x007CE1E0) yields
  808. The delta (~9) is consistent with Ghidra counting references from
  decoded-but-non-instruction areas (e.g. thunks/aligned slack) — it does not
  affect CONTROL-1, which uses T10 only qualitatively ("generic field-getter
  with hundreds of call sites" — confirmed either way). Recording method
  note: for future load-bearing uses of T10-style counts, state the census
  method or re-count from raw bytes.

---

## 2. QC INDEPENDENT RE-DERIVATIONS (what QC recomputed, from where, with what result)

All re-derivations used QC's own python (in `07_QC/raw/`), an independent PE
section mapper, independent VFS container walk, independent BNT2 trailer-index
parser, independent rel32 decoding, and an independent MSVC RTTI chain walk.
No executor script was executed or reused.

1. **Byte cross-check of every cited instruction (CONTROL-4 re-run):**
   compared all instruction records of `C9_LISTING_WINDOWS.json` (20 windows,
   L01–L20) against the physical EXE via QC's own VA→FO mapping with signed-hex
   normalization → **962/962 byte-identical, 0 mismatches**; independent rel32
   re-decode of CALL/imm32 records → **113/113 targets match**. Matches
   C10V2_BYTE_CROSSCHECK.json exactly.
2. **Record 4508 identity (E1/CONTROL-5):** own ArkVFS walk of templates.vfs
   (magic `ArkVFS02`, base 36 from file header, stride from file's own format):
   **5,438 records, stop_pos == file_size 560,788 (EOF-exact), 0 CRC fails,
   5,438 unique ids**. Record id2=4508 at file_offset **96,496**: header
   {id=4508, size=28, ver=1, crc32=AFF5797C}; payload 28 B =
   `9C 11 00 00 FD 85 04 00 FE 85 04 00 00 00 00 00 CB E1 F9 42 00 00 00 00 00 00 00 00`;
   QC re-computed crc32(payload) = AFF5797C = header field (matches).
   Parse: u32@0=4508, u32@4=**296445**, u32@8=296446, u32@12=0,
   f32@16 = **0x42F9E1CB = 124.94100189208984**, u16@20=0, u16@22=0, u32@24=0.
   Direct byte reads: @96,516 = `FD 85 04 00` (A=296445) ✓. Cross-records:
   id2=11963 @315,916, size 382, A=551661, list1_count=16, first string
   "leg_BASE" (`6C 65 67 5F 42 41 53 45`) ✓.
3. **20002.vfs (E12b):** own walk (base 128): **1,366 records, EOF-exact,
   0 CRC fail**; record 0 @16, payload 56 B with tag-0x11 value at payload+0x30
   = `BB 2E 00 00` = 11963 ✓; off48 column membership in the templates id2 set:
   **1,364 hits / 2 misses = [0, 0]** ✓.
4. **Models.bnt anchor (E4/E12c):** own trailer parser: tail `BNT2`,
   index_start 395,262,727; **5,596 entries**; name offsets found:
   `296445.nif` @ **395,268,773** (direct read: "296445.nif\n") ✓;
   `551661.nif` @ 395,323,507 ✓; `296446.nif` ABSENT ✓; `460563.nif` ABSENT ✓;
   **`4508.nif` ABSENT** — this is the E3 falsifier working: a wrong
   ECX-provenance at the getter would have produced id2 (4508) as the model
   id and the join would have missed; instead A=296445 hits.
5. **Call-site census (denominators of SELECTION/E2/E5/E9):** QC scanned all
   `E8 rel32` in `.text` with its own decoder: FUN_0072F580 lookup =
   **25 sites**; FUN_00726E70 ctor = **55**; FUN_006C9700 pump = **13**;
   FUN_006CB6F0 = **2**; FUN_006CB020 = **1**; FUN_006CB3C0 = **2**;
   FUN_007453D0 deserA = **1** (site 0x004C483D); FUN_00730C90 parse = **1**
   (0x0072FBA5); FUN_0072F8D0 insert = **1** (0x0072FBE5); FUN_007CE1E0
   getter = 808 (see P3-3). Reader FUN_0072FA30: **0 CALL sites, exactly one
   JMP (E9) at 0x00452497, 0 imm32 refs** — QC decoded the caller thunk:
   `CALL FUN_0043A550` (registry lazy-init) + `MOV ECX,EAX` + `JMP
   FUN_0072FA30` → the single caller IS the registry loader, confirming census
   T02 = 1 caller.
6. **Emitter chain E3 byte-by-byte (QC VA→FO decode of 0x006C3F50–0x006C3FD2):**
   `E8…` CALL FUN_0043A550 (lazy-init) → `8B C8` MOV ECX,EAX @0x006C3F60 →
   `E8 19 B6 06 00` CALL FUN_0072F580 @0x006C3F62 (rel32 re-derived → 0x0072F580
   ✓) → `8B F8` → `BB 66 00 00 00` MOV EBX,0x66 @0x006C3F69 → `8B CF`
   MOV ECX,EDI @0x006C3F6E → `E8 67 A2 10 00` CALL FUN_007CE1E0 @0x006C3F74
   (rel32 → 0x007CE1E0 ✓) → `89 19` @0x006C3F8D / `89 41 04` @0x006C3F8F
   (pair stores) → queue-grow `E8 52 EE FF FF` → `BB 20 D7 8B 00`
   **MOV EBX,0x008BD720 @0x006C3FB0** (the scheduler callback IS byte-pinned
   inside window L01, within the 962-verified set) → `E8 B6 70 D4 FF` CALL
   FUN_0040B070 @0x006C3FB5 (rel32 ✓) → … → `E8 6E F6 FF FF` @0x006C3FCD
   (rel32 re-derived → **FUN_006C3640** ✓ = the scheduler entry of R04).
   Getter body FUN_007CE1E0 read directly: `8B 41 08 C3` = MOV EAX,[ECX+0x08];
   RET — the [ECX+0x08] A-read claim is exact.
7. **Parse order (E1 core):** C9 L06 listing store order re-derived from the
   window bytes: stores at [EDI+0x00], then [EDI+0x08], then [EDI+0x04],
   then [EDI+0x0C], then [EDI+0x10] — i.e. payload fields f0,f2,f1,f3,f4 map
   to object +0x00,+0x08,+0x04,+0x0C,+0x10, exactly as X01/E1 claim; combined
   with the physical payload (A=296445 at payload+4) the A value lands in
   template+0x08, which the [ECX+0x08] getter reads. Chain closed without
   Ghidra on QC's side.
8. **RB-tree mechanics (E1/E2):** X03 insert compares `*(uint*)(node+0x10)`
   vs key (R02 mapfind: key@node+0x10, left@+8, right@+0xC; D01 returns
   node+0x14, default DAT_00BA5800; X11 lazy singleton `if DAT_00BA1824==0 →
   new(0x18) → FUN_0052A260`). QC verified the listing bytes for lookup
   (window L02/L03) against raw EXE (962 set) and the decompilation logic is
   consistent with the raw instruction bytes QC read directly at
   0x0072F580: `51 56 8B F1 … E8 9B 1E DA FF … 83 C0 14 … C2 04 00 … B8 00 58
   BA 00`.
9. **Scene root (E8):** QC's own scan: string "NetImmerseScene::Root" at file
   offset 6,910,716 → VA 0x00A972FC; `PUSH 0xA972FC` at **0x0093338A**
   immediately before `CALL FUN_007B67E0` @**0x0093338F** (SetName) — byte-level
   proof of the scene-root naming; second SetName site 0x009331CD pushes
   0x00A972E4 ("NetImmerseScene::Scene"). NiNode ctor vtable store
   `C7 06 F4 CC A8 00` @0x007B6041 (MOV [ESI], 0x00A8CCF4) confirmed from raw
   bytes; SetName shape confirmed by own byte read of the prolog
   (`56 8B F1 8B 46 0C 57 50 E8 …` = delete [this+0xC] first).
10. **RTTI identities (E5/R-1, E8) — independent of Ghidra:** QC walked the
    MSVC RTTI chain from raw bytes: vftable 0x00A889C8 (stored by
    `C7 45 00 C8 89 A8 00` in FUN_007796D0, QC byte read @~0x00779702) →
    COL 0x00AAB5DC → TypeDescriptor 0x00B90174 → name
    **".?AVNiControllerSequence@@"** — the R-1 correction
    (0x110 B object = NiControllerSequence) is CONFIRMED from the binary's own
    RTTI, not from a decompiler label. Same chain for **0x00A8CCF4 →
    ".?AVNiNode@@"** and ArkObject ctor store @0x00726EA1 → 0x00A86B48 →
    **".?AVArkObject@@"**.
11. **NiNode vtable re-pin (E12a/E12d):** from the ctor imm32: vtable
    0x00A8CCF4, 47 slots; slot 17 (+0x44) = **0x007B5390** ✓ (historical
    anchor MATCH); slot 27 = **0x007E4820**; QC probed slot 27's first 512 B:
    prolog `83 EC 34 53 8B D9 8B 43 24 85 C0 56 57 74 15 8D 4B 38 …`
    (SUB ESP,0x34; PUSH EBX; MOV EBX,ECX; MOV EAX,[EBX+0x24]; TEST;
    … LEA ECX,[EBX+0x38] = m_kLocal) — UpdateWorldData shape confirmed;
    **rep movsd count in 512 B = 1, max consecutive = 1** — the disclosed
    probe-window discrepancy vs the historical "rep movsd x13" description is
    exactly as the run reported (honest discretion, not a retraction; QC
    reproduced the same 1-rep result, so the discrepancy statement itself is
    CONFIRMED).
12. **Dispatcher (E9b):** Q02 decompilation shows switch cases 0xA2..0xC6 +
    199 with 0xB0 → FUN_004574F0, 0xB9 → FUN_005B72C0, 0xC6 → FUN_004B0AB0,
    199 (0xC7) → FUN_004B1670 — QC notes the case dispatch is a jump-table
    switch (QC's immediate scan of 0x004B18D0+0x2000 finds no 0xA2..0xC7
    compare-immediates — consistent with a jump-table, and the Q02 case bodies
    match the census caller chains: FUN_005B72C0 ← FUN_004B18D0 (N06, 1
    caller), deserB FUN_004C47F0 ← {FUN_004574F0, FUN_004B0AB0, FUN_004B1670,
    FUN_004B1C70} (T12)).
13. **Hardcoded id2 drivers (E9a):** own byte scans: `PUSH 0x3ED3` exactly once
    @0x005B6597 → CALL FUN_005B5F90; `PUSH 0x3ED2` @0x005B6692 and @0x005B67D8
    → two more CALLs to FUN_005B5F90 (3 call sites total, 1 unique caller
    FUN_005B6370 — census K02 confirmed); the emitter id2 arrays in .rdata:
    0x00A855F0 = [11513,11599,11603,11604,11542,11600,11602,11601],
    0x00A858B8 = [11519,11543], 0x00A858C0 = [15025,15024] — **all 12 values
    are members of the templates.vfs id2 set** (QC's own membership check).
14. **Oracle identity (era governance):** QC re-hashed
    `NiMain.lib` (Gb 1.1.2 Eval VC71 ReleaseLib) = 3,073,590 B,
    SHA256 **FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597**
    — MATCH with contract/preflight pins. QC read the exact oracle lines from
    the Gb12 tree: `NiNode.cpp:34` = `NiNode::NiNode(unsigned int uiNumChildren)
    : m_kChildren(uiNumChildren)`, `NiNode.cpp:52` =
    `void NiNode::AttachChild(NiAVObject* pkChild, bool bFirstAvail)`,
    `NiObjectNET.cpp:112` = `void NiObjectNET::SetName(const char* pcName)` —
    all three locators are physically real and quoted accurately in
    ORACLE_RECORDS.md. The claimed transfer discipline is verifiable in the
    data: Entropia SetName stores the name member at +0x0C (Entropia-local
    layout, per NINODE_SLOT17 canon) while GB12 uses +0x08 — ORACLE_RECORDS
    explicitly separates this and no GB12/GB112 offset/slot/ABI was carried
    into any E-claim (all target-side constants re-measured: +0x38/+0x6C from
    the Entropia vtable probe, key@node+0x10 from raw bytes, etc.).
15. **Git baseline (PREFLIGHT):** QC re-measured: HEAD =
    743f9fac2dd5c9e94eaba074b46903b4d3686b46; origin/master = same;
    `git ls-remote --exit-code origin refs/heads/master` = same — all three
    MATCH EXPECTED_BASE_SHA (PREFLIGHT.md PASS confirmed; note: the delivery
    notice's "7439fac" typo does NOT occur in PREFLIGHT.md — the file contains
    the correct full SHA; no finding against the package). Working tree: zero
    tracked changes; foreign untracked groups exactly as listed in PREFLIGHT;
    AUDIT_ENTRYPOINT.md untouched.
16. **artifact_index.csv (manifest precursor):** QC re-hashed ALL 38 rows:
    **38/38 size+SHA256 match**, zero duplicates, zero missing files; the only
    physical file not in the index is `artifact_index.csv` itself
    (self-exclusion per contract §9) → 38+self = 39 physical package files ✓.
    (Index file carries a UTF-8 BOM — cosmetic, parses fine with utf-8-sig.)
17. **Counts re-derivations:** FUNCTIONS_DETAILED = 4 (C2 D) + 17 (C3 R) +
    12 (C4 W) + 12 (C5 X) + 17 (C6 Y) + 12 (C7 Z) + 10 (C8 Q) + 4 (C11 O) =
    **88** ✓ (< 120 limit). RECORDS_DETAILED = 3/3 ✓ (4508; 11963; 20002-rec0).
    ORACLE mechanisms = 3/3 ✓ (SetName/NiNode-ctor; AttachChild as negative
    matcher; UpdateWorldData shape). SHORTLIST = 3 ✓ (T/P/A), DEEP_TRACE = 1 ✓
    (FAMILY-T only; no candidate substitution — SELECTION.md records the
    decision BEFORE the deep trace and the run stayed on FAMILY-T after the
    unfavorable CONTROL-2 outcome).

---

## 3. CONTROLS 1–5 VERIFICATION (each declared control was actually executed)

| Control | Tested claim (QC read) | Discriminator | QC independent check | Status agreement |
|---|---|---|---|---|
| CONTROL-1 | [ECX+0x08] getter reads A only via ECX-provenance | same displacement, different meanings elsewhere | QC confirmed: mapfind walks `*(node+8)` as LEFT-child while comparing key@node+0x10 (L03 bytes verified in 962-set); Z10 shows the same getter called on a FILE object (output → record slot, not a model id); ArkObject ctor (D03) uses it on the template; census 808 raw sites (vs 817 Ghidra — P3-3 note) | PASS — agreed |
| CONTROL-2 | placement record is a world instance of the templates record | (a) driver reading VFS; (b) template id2 at identity slot; (c) record being NiAVObject | QC confirmed all three fail: the only reader is FUN_0072FA30 via one JMP-thunk caller (registry loader: CALL FUN_0043A550 + JMP); record key comes from the message cursor (W08 deserA reads key u32 first); setters store +0x08/+0x14/+0x20 vs m_kLocal@+0x38/m_kWorld@+0x6C (setter bytes + vtable probe verified) | **FAIL for the world-instance claim → UNKNOWN** — agreed; this is exactly why RESULT_LEVEL is not A |
| CONTROL-3 | pending-attach thunks are NiNode::AttachChild | oracle operation set (NULL guard, Inc/DecRef pair, AttachParent, children-array add) | QC read Z03–Z07 bodies: state machine (state@+0x60 ∈ 0..4, partner@+0x90, transition floats @+0x68/+0x6C, index/flag @+0x98/+0x9C, array@+0x30 count@+0x38, gates @+0xAC/@+0x5C) — NONE of the four oracle operations present; oracle line NiNode.cpp:52 physically verified; HISTORICAL_CONTROL_REUSED (NC2 slot-17 matcher) correctly labeled separately | PASS — agreed (REJECTED-as-AttachChild, CONFIRMED-as-LOD-state-machine) |
| CONTROL-4 | every cited instruction exists verbatim in the EXE | byte drift between listing and file | QC re-ran the whole comparison with its own mapper: 962/962 identical; 113/113 call/imm re-derived; the c10-v1 signed-hex transcription artifact is visible in C10_BYTE_PINS.json (18/28) and was corrected in C10V2 — as described | PASS — agreed |
| CONTROL-5 | record bytes belong to the pinned files | SHA + independent walk + EOF + CRC | QC re-hashed all three files (templates BE57818C…; 20002 C3899C3E…; Models C950A8C2… — all MATCH), re-walked containers to EOF, re-computed crc32(payload 4508) = AFF5797C = header field | PASS — agreed |

No declared-but-not-executed control was found. "Controls NOT established"
(slot-object class semantics; no runtime controls) matches the evidence.

---

## 4. SELECTION / PROVENANCE / TEMPLATE-VS-INSTANCE / ORACLE-TRANSFER / ERA CHECKS

- **SELECTION:** ranking rests on QC-confirmed dataflow density (25/23 lookup,
  55 ctor, 13/11 pump — all re-counted from raw bytes) and on the physical
  record pin (C1) — not on names, numeric overlap, or building promise.
  Shortlist = 3 (T/P/A); decision written in SELECTION.md before the deep
  trace; no candidate substitution after the unfavorable CONTROL-2 result;
  no second deep trace. FAMILY-P/FAMILY-A rejections are data-grounded
  (leg_BASE body-part endpoint; no pinned physical record).
- **TEMPLATE-VS-INSTANCE:** the world-instance claim stayed UNKNOWN everywhere
  (CONTROL-2 FAIL → INSTANCE_IDENTITY (world) NOT ESTABLISHED in TRACE, CLAIM
  MATRIX, DRAFT_FINAL). No drift toward "instance from the record": the run
  explicitly separates definition-source use (templates.vfs consumed as a
  DEFINITION registry) from instance identity (message/attribute/hardcoded
  id2+transform). The placement-record vs NiAVObject distinction is byte-real
  (+0x08/+0x14/+0x20/+0x24 stores vs +0x38/+0x6C). E10's payload-derived vec3
  is honestly scoped to a slot-position computation with UNKNOWN slot class
  and is NOT conflated with a placement record (PLACEMENT_XYZ_RECOVERED = NO).
- **ORACLE TRANSFER / ERA:** no GB12/GB112 offset, slot number, layout constant
  or ABI was transferred into any target claim (QC checked every target-side
  constant against Entropia-local raw re-measurements; the SetName member
  offset case is explicitly handled as Entropia-local +0x0C vs GB12 +0x08).
  The attach-thunk negative matcher has its own target-local proof (Z03–Z07 +
  L13 bytes). The slot-27 "rep movsd x13" non-reproduction is recorded as a
  probe-window discrepancy — QC reproduced the same 1-rep result — honest
  discretion, not a silent contradiction and not an unsupported retraction.
  Era separation is maintained at input level (9.3.5 EXE pinned; PE2-era
  binary explicitly excluded), at oracle level (Gb12 source vs Gb112 lib vs
  Entropia RTTI all separately identified), and in the NINODE_SLOT17 reuse
  (labeled HISTORICAL_CONTROL_REUSED).

---

## 5. COMPLIANCE SUMMARY

- Limits: SHORTLIST_FAMILIES_MAX=3 → 3 ✓; DEEP_TRACE_FAMILIES_MAX=1 → 1 ✓;
  ORACLE_MECHANISMS_MAX=3 → 3 ✓; NEW_PCG_FUNCTIONS_DETAILED_MAX=120 → 88 ✓;
  NEW_PHYSICAL_RECORDS_DETAILED_MAX=3 → 3 ✓; QC_REPAIR_ROUNDS_MAX=1 (not yet
  consumed — see recommendation).
- Budget: pre-registered in RUN_PLAN.md (ENUM ≤30 / TRACE ≤90 / CONTROLS+ORACLE
  ≤30) before analysis ✓; declared usage ~14/~27/~10 — QC cannot re-count tool
  invocations from artifacts (noted as UNVERIFIED, not contradicted); no sign
  of post-hoc expansion; hard limits unambiguous.
- Payload discipline: package contains only derived evidence (hashes,
  instruction listings, decompilation text, small hex dumps, scripts); no
  original EXE/VFS/BNT/ARK/NIF payload or Gamebryo source dump is committed;
  oracle records are locators + hashes + short quotes (QC verified the
  originals physically exist at the quoted lines). 39 physical files, all
  small text/JSON.
- Retractions: R-1 disclosed with blast radius (this-run wording only; no
  historical claim retracted); no retracted-as-standing text found;
  supersessions S-1..S-4 are re-pins/reproductions, all consistent with QC's
  own re-measurements. R-1's RTTI basis independently CONFIRMED (see
  re-derivation 10).
- NOT_CHECKED.md: complete and honest (10 not-checked items incl. NiStream
  bodies, slot-object classes, GB 2.3/2.6/3.2 oracles, provider chain, runtime
  anything; not-established list covers the LEVEL-A blocker, slot semantics,
  scene insertion, H1/H3/H4, D_f32 role, engine generation). QC's own
  not-checked items (below) do not reveal any hole the executor should have
  covered inside this run's scope.
- PREFLIGHT.md: QC re-verified every git row and physical identity pin —
  PASS stands. (The "7439fac" typo exists only in the delivery notice, not
  in PREFLIGHT.md — no package finding.)
- AUDIT_ENTRYPOINT.md: untouched by executor and by QC ✓. No staging/commit/
  push occurred (HEAD == BASE_SHA) ✓.

---

## 6. COVERAGE OF THIS QC (explicit)

FULL_READ (complete, to EOF):
- All 39 executor package files (00_CONTROL 3, 01_RAW 13, 02_ANALYSIS 5,
  03_SCRIPTS 13, 04_CONTROLS 1, 05_ORACLE 1, 06_REPORT 3), plus full-text
  reads of the contract file and (via QC dump tooling) all decompilation
  bodies relevant to load-bearing claims: R01–R09, R11–R17; D01–D04;
  X01, X03, X06–X09, X11; Z01–Z11; W01, W03, W04, W06, W08, W09;
  Q02, Q04, Q05, Q06; O01–O04; Y01, Y06.
- All 962 C9 listing instructions (machine-compared), all 113 call/imm
  targets (re-derived), all 38 artifact_index rows (re-hashed).

BOUNDED_INSPECTION:
- C2 T10 caller_list (367 entries): metadata + head sample (the 817/367 count
  is not load-bearing — see P3-3).
- C11 vtable_discovery candidate tables (6 candidates): inspected; final
  selection (0x00A8CCF4) independently confirmed from the ctor imm32.

NOT_CHECKED BY QC (with reason):
- No re-run of Ghidra decompilation by QC (STATIC constraint + no independent
  decompiler): Method-A decompilations were verified by (a) full byte
  agreement of their underlying listing windows with the physical EXE (962/962
  re-checked by QC), (b) QC's own raw-byte decodes of the same instructions at
  every load-bearing step, and (c) the independent RTTI chain for class
  identities. Residual risk: a decompiler-only semantic assertion with no
  byte/RTTI counterpart — QC found none among the load-bearing claims.
- Full JOIN R1 re-run (Models.bnt 3,618/3,618): bounded reuse per contract §2;
  QC re-pinned the load-bearing anchor (296445.nif @395,268,773) instead.
- Q01 (FUN_00468910, 1,336 lines) full body: the run itself records it as not
  decomposed (NOT_CHECKED item 4); only its census role (P03, 9 callers) was
  used, which QC confirmed from the census data.
- Remaining non-load-bearing decompilation bodies (W02, W05, W07, W10–W12,
  X02, X04, X05, X10, X12, Q01, Q03, Q07–Q10, Y02–Y05, Y07–Y17, Z12):
  read at structure level only; none is cited as sole evidence for any
  E1–E12 claim.
- Volumes.bnt/.bvi side, NiStream/provider bodies, callback FUN_008BD720
  internals (QC read its prolog only: `8D 41 18 C3` = LEA EAX,[ECX+0x18]; RET),
  GB 2.3/2.6/3.2 oracles, runtime behavior of any kind: out of run scope by
  contract; consistent with NOT_CHECKED.md.
- Budget usage counts (~14/~27/~10): UNVERIFIED (not re-countable from
  artifacts; hard limits all independently confirmed unexceeded).

QC RAW EVIDENCE: all QC instruments and outputs are in `07_QC/raw/`
(qc_derive*.py, QC_DERIVATIONS*.json 1–5, C2_STRUCTURE_DUMP.txt,
C2_TARGETS_DUMP.txt, CENSUS_TARGETS_DUMP.txt, ARTIFACT_INDEX_CHECK.json,
decomp_dump/*.c work copies).

---

## 7. RECOMMENDATION TO PE-MASTER

**Proceed to persistence after one bounded textual repair round** (contract
QC_REPAIR_ROUNDS_MAX=1, not yet consumed):

1. Fix P2-1 (DRAFT_FINAL COVERAGE: 69 → reconstructable 45 = 19+10+4+8+4).
2. Fix P3-1 (TRACE E9a byte string "68 2D 3E 00 00" → "68 D3 3E 00 00").
3. Fix P3-2 (TRACE E9c flag numbering: id2 path is flag-1, not flag-2).
4. Optionally add the P3-3 method note (T10 census 817 Ghidra vs 808 raw) —
   not required for closure.

None of these touches raw evidence, gate results, claim statuses, or the
science outcome; after the textual repair the package is fit for the
publication phase (fresh QC → this report stands as the fresh-QC record;
PE-MASTER advisory review → entrypoint row → final manifest → commit/push
per contract §9). If PE-MASTER prefers zero-touch persistence instead, the
three findings can ship as an erratum note in the publication commit — but
the in-repo inconsistency (P2-1: two different census totals in one package)
is better fixed in the one allowed repair round while the package is still
open.

```text
QC_VERDICT = QC_PASS_WITH_FINDINGS
OPEN FINDINGS = P2-1 (report COVERAGE denominator 69 vs raw-reconstructable 45);
  P3-1 (byte-string typo in TRACE E9a); P3-2 (flag-number inversion TRACE E9c);
  P3-3 note (census method delta 817/808, no action required)
RESULT_LEVEL AGREEMENT = B (partial resource/scene chain) — agreed and honest
MODEL_RESOURCE_EDGE = CONFIRMED (static record→…→{0x66,A}→nif-name chain) —
  independently re-derived, not contradicted; runtime physical open correctly
  capped at STRONGLY_SUPPORTED by the executor itself
CONTROL-2 = FAIL → UNKNOWN — agreed (the honest core of Level B)
CANONICAL GATE EFFECT = NONE; no historical claim damaged; R-1 CONFIRMED via
  independent RTTI walk
NEXT_PARENT_ACTION = authorize the one bounded repair round (textual only),
  then persistence per contract §9 (entrypoint row → final manifest → commit →
  push → live remote verify → desktop post-audit of the exact pushed SHA)
```
