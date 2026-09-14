# QC_AUDIT_R1.md — PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914

**QC_VERDICT: QC_FAIL (publication STOPPED before STEP 2/STEP 4 per the dispatch's explicit rule
"If you find any defect: STOP, do not publish, return QC_FAIL with the exact defect").**

QC actor: pe-master-auditor (fresh context; direct PE-MASTER dispatch 2026-09-14; NO_NESTED_TASKS).
QC method: own PE32 parser written for this QC (PowerShell byte-level; NO capstone, NO Ghidra, and
deliberately ZERO execution of the package's own scripts — independence over repeatability). All
19 package files read to EOF. The physical EXE was opened READ-ONLY.

IMPORTANT SCOPE NOTE: **every scientific claim of the run verified CONFIRMED** — all 6 dispatched
verification points PASS (44/44 independent byte checks; details below). The QC_FAIL is caused by
exactly ONE additional defect found inside the package (P2, toolchain-version provenance string,
finding below), which triggers the dispatch's binary defect rule. The run's decode layer itself is
intact; PE-MASTER adjudicates the amendment.

## 0. Identities measured by the QC (own measurements, 2026-09-14)

| Identity | Measured | Status |
|---|---|---|
| EXE SHA256 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | == pin, PASS |
| EXE size | 8,015,872 B | == pin, PASS |
| EXE PE32 identity | machine 0x014C (i386), opt_magic 0x010B (PE32), image_base 0x00400000; sections .text/.rdata/.data/.tls/.rsrc (headers parsed by my own parser; .text rva 0x1000/rsize 0x674000, .rdata rva 0x675000/rsize 0xF7000 — identical to 00_CONTROL/SOURCE_IDENTITIES.json) | PASS |
| Repo HEAD (12_WebGame/eudoria-clean) | 6465019298e66856a2fe9fa9750c047d057c97dd == BASE_SHA == origin/master (ls-remote) | PASS, no drift |
| Repo dirty set | only untracked `?? experiments/` (foreign, untouched by this QC) | PASS |
| AUDIT_ENTRYPOINT.md pre-edit SHA256 | 367BCF3CE06066E7B6833F287E8AB17A9A6ECE403AF9D508D1711EAC176D5DAA (76,562 B) — recorded for the (not performed) publication step | RECORDED |
| Package census | 19 files, 120,461 B total (own byte-sum) | == contract, PASS |
| Toolchain ground truth | `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` = Python 3.12.7, `capstone.__version__` = **5.0.7** | measured (see finding) |

## 1. Dispatch QC point 1 — vtable 0x00A7D458 + boundary + RTTI walk: PASS

Own reads from physical .rdata (my own VA->file-offset mapping from the parsed section table):

- vtable @ 0x00A7D458, six dwords (little-endian, read by me): **0x0050A460 / 0x005090A0 /
  0x005090B0 / 0x0050A050 / 0x005090C0 / 0x00509580** — exactly the six contract functions, in
  contract order (slots 0..5). The six functions ARE the complete vtable. PASS.
- 7th dword @ 0x00A7D470 = **0x53565064**; bytes 64 50 56 53 = ASCII `dPVS` — .rdata string data,
  NOT a .text pointer; vtable extent ends at slot 5. PASS.
- vtable section = .rdata (my own section mapping). PASS.
- RTTI walk (own, from physical bytes): [0x00A7D454] = **0x00AA12B8** -> COL @ 0x00AA12B8:
  signature=0, offset=0, cd_offset=0, pTypeDescriptor=**0x00B78834**, pClassHierarchy=0x00AA12CC
  -> TD @ 0x00B78834: vfptr=0x00A98110, spare=0, name (read by me at TD+8, 23 bytes, NUL-terminated)
  = **`.?AVSceneFeederObject@@`**. PASS — matches 01_RAW/VTABLE_AND_SLOTS.txt and
  01_RAW/VTABLE_SLOT_MAP.json exactly.

## 2. Dispatch QC point 2 — slot 1/2/4 bodies: PASS

Own byte reads (mine, no capstone, hand-decoded):

- Slot 1 @ 0x005090A0 = **8D 41 34 C3** = `LEA EAX,[ECX+0x34]; RET` — position-ADDRESS getter,
  no value read. PASS.
- Slot 2 @ 0x005090B0 = **8D 41 74 C3** = `LEA EAX,[ECX+0x74]; RET` — +0x74, outside window. PASS.
- Slot 4 @ 0x005090C0 = **8D 81 80 00 00 00 C3** = `LEA EAX,[ECX+0x80]; RET` — +0x80, outside
  window. PASS.

## 3. Dispatch QC point 3 — slot 3 body @0x0050A050: PASS (incl. the no-position-to-call negative)

Full 90-byte body read and verified by me against every dispatch pin:

| VA | measured bytes | check |
|---|---|---|
| 0x0050A05B | 8B 4E 30 | MOV ECX,[ESI+0x30] — the +0x30 LINK read. PASS |
| 0x0050A061 | 8B 42 44 | MOV EAX,[EDX+0x44] — vtable slot 17 load (0x44/4). PASS |
| 0x0050A064 | FF D0 | CALL EAX — the virtual call. PASS |
| 0x0050A075 | E8 F6 DE F2 FF | direct call target recomputed by me = 0x00437F70. PASS |
| 0x0050A07C | E8 1F 15 32 00 | direct call target recomputed by me = 0x0082B5A0. PASS |
| 0x0050A087 | 8B 16 | MOV EDX,[ESI] — fallback: this->vtable. PASS |
| 0x0050A089 | 8B 42 04 | MOV EAX,[EDX+4] — vtable slot 1 (= slot 1 above, proven getter). PASS |
| 0x0050A08C | 8B CE | MOV ECX,ESI. PASS |
| 0x0050A08E | FF D0 | CALL EAX — fallback self-vcall; no stack args pushed for it. PASS |
| 0x0050A090 | 8B 10 | MOV EDX,[EAX] — read X. PASS |
| 0x0050A096 | 89 11 | MOV [ECX],EDX — copy X -> caller arg1 buffer. PASS |
| 0x0050A098 | 8B 50 04 | MOV EDX,[EAX+4] — read Y. PASS |
| 0x0050A09B | 89 51 04 | MOV [ECX+4],EDX — copy Y. PASS |
| 0x0050A09E | 8B 40 08 | MOV EAX,[EAX+8] — read Z. PASS |
| 0x0050A0A1 | 89 41 08 | MOV [ECX+8],EAX — copy Z. PASS |
| 0x0050A0A7 | C2 08 00 | terminal RET 8. PASS |
| 0x0050A0AA | CC CC CC CC CC CC | CC padding completing to 16-align 0x0050A0B0 — body end evidence. PASS |

No-position-value-into-any-CALL (complete call enumeration, my own dataflow reasoning over the
measured bytes): the body contains exactly 4 calls.
1. 0x0050A064 vcall: only stack argument = EAX pushed at 0x0050A060, loaded at 0x0050A050 from
   [ESP+8] = the caller's arg2 (query flag); receiver ECX = the +0x30 link object. No position
   value involved (on this path no position read occurs at all).
2. 0x0050A075 -> 0x00437F70: arguments = (vcall result + 0x90) and ESI = arg1 (caller out
   buffer) — no position value (position reads exist only on the fallback tail).
3. 0x0050A07C -> 0x0082B5A0: thiscall on the 0x00437F70 result — no position value.
4. 0x0050A08E self-vcall of vtable slot 1: no stack arguments (the only push since entry is the
   saved ESI at 0x0050A056; ECX = this); after it the position values are only READ and COPIED
   to the caller's arg1 buffer, then RET 8 — no further call exists on this path.
CONFIRMED: position values (SF+0x34..0x3C) NEVER flow into any call. `position_to_call = N` for
every slot is correct. This is a verified NEGATIVE (the census's central claim).

## 4. Dispatch QC point 4 — positive control @0x005094C0: PASS

Own read, 28 bytes at 0x005094C0: **8B 44 24 04 8B 10 89 51 34 8B 50 04 89 51 38 8B 40 08 89 41
3C C6 41 28 01 C2 04 00** — BYTE-EXACT vs the contract-expected pattern (my comparison). Decodes as
arg-triple -> this+0x34/0x38/0x3C, flag this+0x28=1, RET 4. PASS. (The window is followed at
+0x1A by CC CC CC CC padding — consistent with the 28-byte function extent.)

## 5. Dispatch QC point 5 — census CSV, ONE_HOP_FLOW, REPORT, gates, HANDOFF: PASS

- 02_ANALYSIS/SCENEFEEDER_SLOT_CENSUS.csv: header = exactly the 19 contract columns in contract
  order; **6 data rows** (slot_index 0..5); classifications = 5x NO_RELEVANT_ACCESS + 1x MIXED —
  both from the closed vocabulary. Slot 3 row: reads_sf30/34/38/3c = Y/Y/Y/Y, writes = N/N/N,
  takes_position_address = N, position_to_call = N, call_va = 0050A064 (the vcall), receiver =
  SF+0x30 link (class unknown). Slot 1 row: takes_position_address = Y. PASS.
- 02_ANALYSIS/ONE_HOP_FLOW.md: consistent with the CSV (slot-3 Path A/B, slot-1 address getter,
  slots 0/2/4/5 negatives, NEXT_SEAM = NONE). PASS.
- 06_REPORT/REPORT.md: FINAL STATUS B; gates G1-G5 PASS with G5 explicitly vacuous; NOT_CHECKED
  section matches the contract stop-rule. PASS.
- 06_REPORT/STAGE_ACCEPTANCE_GATES.csv: G1-SOURCE/G2-VTABLE/G3-COMPLETE-SLOT-CENSUS/
  G4-POSITION-ACCESS/G5-ONE-HOP-FLOW all PASS, boundary evidence consistent with the raw files.
  PASS.
- 06_REPORT/HANDOFF.md: RUN_STATUS B; ENTRYPOINT_ROW_DRAFT present (last cell = "PENDING (the
  PE-MASTER loop audit)") — verified in full, including the byte pins quoted in the draft. PASS.

## 6. Dispatch QC point 6 — package hygiene: PASS

- No `__pycache__` or hidden/dot directories anywhere in the package (own recursive scan).
- Extensions present: .md x5, .py x4, .csv x4, .json x3, .txt x3 = 19 files, 120,461 B. No
  binaries, no proprietary payloads, the EXE is NOT in the package.
- File set = exactly the contract's small set: 12 required files + 4 scripts + SCRIPT_SHA256.csv
  + 2 machine-readable sidecars (VTABLE_SLOT_MAP.json, SLOT_ACCESS_CENSUS.json — both documented
  in 03_EVIDENCE/README.md and SCRIPT_SHA256.csv purposes). Nothing outside the contract set.
- MANIFEST_SHA256.csv (pre-QC state): 18 rows, 3 columns (path,bytes,sha256); my own re-hash of
  all 18 rows: **18/18 match, 0 failures**; 0 duplicate paths; no self-row; all 19 disk files
  covered (18 manifested + manifest itself). PASS.

## 7. Additional consistency checks performed (beyond the dispatched minimum)

- Slot 0 body (30 B @0x0050A460): my read = 56 8B F1 E8 D8 FD FF FF F6 44 24 08 01 74 09 56 E8
  B5 2F 45 00 83 C4 04 8B C6 5E C2 04 00 — scalar deleting destructor (CALL 0x0050A240 recomputed
  by me; TEST [ESP+8],1 JE; CALL 0x0095D42A recomputed; RET 4). Zero window-field (0x30/0x34/
  0x38/0x3C) displacements in the body. PASS.
- Thunk resolution verified by my OWN import-table walk: 0x0095D42A = FF 25 5C 53 A7 00 -> IAT
  slot VA 0x00A7535C -> **MSVCR80.dll.??3@YAXPAX@Z (operator delete)** — matches the run's claim.
- Slot 5 body (24 B @0x00509580): my read = 8B 44 24 04 8B 49 18 50 51 E8 62 BB F0 FF 8B C8 E8
  3B DC 3A 00 C2 04 00 — reads [ECX+0x18] (outside window), calls recomputed = 0x004150F0 and
  0x008B71D0. No window-field access. PASS.
- E8 rel32 target arithmetic recomputed by me for all 6 direct calls listed above — all exact.

## 8. FINDING (the one defect; this is what forces QC_FAIL under the dispatch rule)

**P2 — TOOLCHAIN-VERSION STRING DEFECT: the two primary raw decode evidence headers (and two
script literals + one script comment) claim "capstone 5.0.9", but the measured toolchain is
capstone 5.0.7 — the package contradicts its own identity records.**

- Exact sources (all measured/read by this QC):
  - `01_RAW\VTABLE_AND_SLOTS.txt` line 2: "(capstone 5.0.9, x86-32)"
  - `01_RAW\SLOT_DISASSEMBLY.txt` line 1: "OWN DECODE (capstone 5.0.9, x86-32)"
  - `00_CONTROL\s1_vtable_slots.py` line 28 — hard-coded literal emitting "capstone 5.0.9"
  - `00_Control\s2_slot_disasm.py` line 51 — hard-coded literal emitting "capstone 5.0.9"
  - `00_CONTROL\sf_core.py` line 3 comment — "disassembly listing via capstone 5.0.9"
- Contradicted (correct) records in the SAME package:
  - `00_CONTROL\RUN_CONTRACT.md` §INPUT_IDENTITIES: "capstone 5.0.7 (capstone.__version__)"
    (measured at run time by the executor)
  - `00_CONTROL\SOURCE_IDENTITIES.json`: "capstone_version": "5.0.7"
  - `00_CONTROL\SCRIPT_SHA256.csv` sf_core purpose: "capstone 5.0.7 x86-32"
- Physical counter-evidence (my own measurement, 2026-09-14, with the exact recorded interpreter
  `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe`): `Python 3.12.7`,
  `capstone.__version__` = **5.0.7**. The "5.0.9" strings in the two emitted raw headers are
  hard-coded literals in s1/s2 (neither script queries capstone.__version__), i.e. a stale
  editing artifact, not a measurement.
- Failure mechanism: stale literal propagated from script source into the two PRIMARY raw
  evidence files' headers at generation time.
- Affected claims/runs: ONLY the toolchain-provenance header lines of this package's raw files.
  ZERO effect on any decode claim of the run — every load-bearing byte was re-verified by this
  QC without capstone at all (sections 1-7 above all PASS). No other run is affected.
- Skutek/Effect: internal contradiction of the package's provenance records (raw evidence
  headers vs identity records); publishing the package as-is would freeze a factually wrong
  toolchain label into the repo copy.
- Narrow correction (for PE-MASTER to assign — this QC does NOT mutate the completed run's
  originals): EITHER (a) an amendment/review run that fixes the literals in s1/s2/sf_core.py
  (preferably to read `capstone.__version__` dynamically) and regenerates or errata-amends the
  two raw headers (completed-run originals must not be silently overwritten — amendment file or
  regenerated evidence inside a NEW correction run directory per project discipline), OR (b) an
  explicit PE-MASTER waiver/erratum decision recorded before publication.
- Revalidation predicate: after the fix, (1) both raw headers read the version equal to the
  measured `capstone.__version__` of the recorded interpreter, (2) the instruction listings below
  the header lines remain byte-identical to the current listings, (3) manifest re-hash OK.

## 9. QC verdict and consequences

- All 6 dispatched verification points: **PASS** (sections 1-6).
- Independent byte pins: 44/44 PASS (sections 1-4, 7).
- One P2 defect found (section 8) → per the dispatch's explicit binary rule ("If you find any
  defect: STOP, do not publish, return QC_FAIL with the exact defect"): **QC_FAIL**.
- Consequences applied: PE_MASTER_REVIEW.md NOT written (STEP 2 not reached); the repo NOT
  touched (zero git mutations; HEAD == BASE_SHA verified unchanged at QC end); publication NOT
  performed; AUDIT_ENTRYPOINT.md untouched (pre-edit SHA recorded above).
- Package mutations by this QC (disclosed): (1) this file 06_REPORT/QC_AUDIT_R1.md added;
  (2) 06_REPORT/MANIFEST_SHA256.csv regenerated to cover ALL package files now present
  (19 rows, no self-row, zero missing, zero duplicates — the package's own manifest invariant;
  the 18 pre-existing rows re-hashed and unchanged).

## 10. FULL_READ_LOG (this QC)

All 19 package files read TO EOF by this QC: 00_CONTROL\RUN_CONTRACT.md; 00_CONTROL\s1_vtable_slots.py;
00_Control\s2_slot_disasm.py; 00_CONTROL\s3_positive_control.py; 00_CONTROL\SCRIPT_SHA256.csv;
00_CONTROL\sf_core.py; 00_CONTROL\SOURCE_IDENTITIES.json; 01_RAW\POSITIVE_CONTROL_005094C0.txt;
01_RAW\SLOT_DISASSEMBLY.txt; 01_RAW\VTABLE_AND_SLOTS.txt; 01_RAW\VTABLE_SLOT_MAP.json;
02_ANALYSIS\ONE_HOP_FLOW.md; 02_ANALYSIS\SCENEFEEDER_SLOT_CENSUS.csv;
02_ANALYSIS\SLOT_ACCESS_CENSUS.json; 03_EVIDENCE\README.md; 06_REPORT\HANDOFF.md;
06_REPORT\MANIFEST_SHA256.csv; 06_REPORT\REPORT.md; 06_REPORT\STAGE_ACCEPTANCE_GATES.csv.
Package scripts were read but deliberately NOT executed (independence; no side effects on a
completed run; re-execution would prove repeatability, not independence).

## 11. NOT_CHECKED by this QC (beyond the run's declared boundaries)

- Callee bodies beyond the one-hop stop rule: 0x0050A240 (dtor body), 0x00437F70, 0x0082B5A0,
  0x004150F0, 0x008B71D0, and the dynamic link->vtable[+0x44] (slot 17) target — same
  NOT_CHECKED set as the run's own declaration.
- The SF+0x30 link object's class/RTTI (the run's declared open edge; the proposed next test).
- Slot callers, runtime overrides, engine execution (ABSENT by contract).
- Capstone-version decode equivalence between 5.0.7/5.0.9 (unnecessary: this QC's byte
  verification is capstone-free).
- The prior run PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913's own claims (out of scope;
  only its status quo was checked for consistency as recorded in RUN_CONTRACT §3).

## RESOLUTION (round 2)

Round 2 (same QC actor, fresh context, direct PE-MASTER FINAL dispatch 2026-09-14;
NO_NESTED_TASKS): re-verification of the executor amendment (task ses_f601216e) from disk with
my OWN reads. The round-1 record above is preserved verbatim (executor-untouched; its sha256 at
round-2 start = 8A8CB47F4226B333E4F4FFDEF7A5D2C1C75BCBB3344AADB2A450C7F67FA32006, re-measured
by me == the round-1 identity). BASE re-measured at round-2 start: HEAD == origin/master ==
ls-remote == 6465019298e66856a2fe9fa9750c047d057c97dd (no drift). EXE re-measured:
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, 8015872 B (unchanged).

### Amendment re-verification (dispatch points a-f, all my own measurements)

- (a) The 3 script literals fixed - CONFIRMED by my own full reads: 00_CONTROL\s1_vtable_slots.py
  line 12 `import capstone` + line 30 dynamic
  `emit("# S1: physical vtable + slot map (capstone %s, x86-32)" % capstone.__version__)`;
  00_CONTROL\s2_slot_disasm.py line 13 `import capstone` + line 53 dynamic
  `emit("# OWN DECODE (capstone %s, x86-32) - PE_935_..." % capstone.__version__)`;
  00_CONTROL\sf_core.py line 3 comment = "capstone 5.0.7 (measured)". My own whole-package scan:
  ZERO live "5.0.9" in 00_Control/*.py + 01_RAW/*.txt. PASS.
- (b) Raw headers say 5.0.7 - my own reads: 01_RAW\VTABLE_AND_SLOTS.txt line 2 and
  01_RAW\SLOT_DISASSEMBLY.txt line 1 both read "capstone 5.0.7, x86-32". PASS.
- (c) Diffs vs 00_CONTROL\PRE_EDIT\*.pre (my own line-level diff + git-minimal diff):
  sf_core.py EXACTLY 1 changed line (line 3, the version comment); VTABLE_AND_SLOTS.txt EXACTLY
  1 (line 2); SLOT_DISASSEMBLY.txt EXACTLY 1 (line 1) - the regenerated evidence is
  byte-identical modulo the version label = determinism PROVEN; s1/s2 = the version-literal line
  plus the PE-MASTER-ordered `import capstone` insertion (+2 lines each; git numstat +3/-1;
  nothing else). All 5 .pre copies still carry the old "5.0.9" (one occurrence each, my own
  scan) - defect provenance preserved. PASS.
- (d) capstone.__version__ measured by me with the recorded interpreter
  D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe: Python 3.12.7,
  capstone.__version__ = 5.0.7 - equals the new dynamic labels. PASS.
- (e) MANIFEST_SHA256.csv re-hash (my own): 25 rows, format path,bytes,sha256 (SHA = column 3);
  25/25 hash+bytes MATCH, 0 mismatches, 0 duplicate paths, no self-row; 26 disk files =
  25 manifested + the manifest itself; 0 missing. SCRIPT_SHA256.csv re-hash (my own; format
  script,bytes,sha256,purpose, SHA = column 3): 4/4 MATCH (sf_core 82655ce7..., s1 53a0682b...,
  s2 b725c244..., s3 a229ae05...). QC_AUDIT_R1.md sha 8A8CB47F... == round-1 pin - the executor
  did NOT touch my record. PASS.
- (f) AMEND_LOG_R1.md (8431 B, read to EOF by me) documents ALL required elements: the order
  (including the aborted-before-any-change first dispatch provenance), the P2 defect, the exact
  old->new line diffs for all 5 changed files, the determinism proof (regenerated raws differ
  only in the version line; JSON sidecars byte-identical 2e5c9469.../f219f78b...), the post-fix
  "5.0.9" census (0 live; remaining 13 = 8 documentation quotes in this QC record + 5 .pre
  snapshots, by design), and the __pycache__ removal. PASS.

### Round-2 QC verdict for the amendment

**QC_PASS.** The P2 is resolved exactly per the round-1 revalidation predicate (section 8):
(1) both raw headers now read the version equal to the measured capstone.__version__ of the
recorded interpreter; (2) the instruction listings below the header lines remain byte-identical
(1-line diffs vs .pre); (3) manifest re-hash OK. The amendment touched ONLY the 5 ordered files
plus the 2 control CSVs and AMEND_LOG_R1.md; zero science claims changed (the decode layer was
already independently verified in round 1: 44/44 byte checks, capstone-free). No new defect found.

Process note (for the project discipline ledger): this defect was caught ONLY by the
fresh-context INTERNAL_QC round - the executor's SELF_CHECK and the PE-MASTER pre-QC audit both
missed it; the binary defect rule (find defect -> STOP publication -> return QC_FAIL) worked
exactly as designed: publication was stopped, the finding was adjudicated ACCEPTED_FINDING, the
executor amendment was ordered, executed and now re-verified. The discipline worked.
