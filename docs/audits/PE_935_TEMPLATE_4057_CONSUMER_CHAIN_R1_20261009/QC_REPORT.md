# QC REPORT — PE_935_TEMPLATE_4057_CONSUMER_CHAIN_INTERNAL_QC_R1_20261009

- **QC OF**: `PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009` (RUN_CLASS BOUNDED_STATIC_CONSUMER_CENSUS; executor pe-reconstruction)
- **QC ORIGIN**: pe-master-auditor **fresh context**, dispatched directly by PE-MASTER (`NO_NESTED_TASKS`). This is **internal QC inside PE-MASTER — NOT an independent Desktop post-audit, NOT executor self-review**. No executor artifact was modified; no commit/push performed; AUDIT_ENTRYPOINT.md untouched.
- **QC VERDICT**: **QC_PASS_WITH_FINDINGS** — in the dispatch's binary frame: **QC_PASS for the audited science**, with **4×P2 records corrections REQUIRED BEFORE PERSISTENCE** (F-QC-1..F-QC-4) and 6×P3 minor records defects (F-QC-5..F-QC-10). It is **not QC_FAIL**: no load-bearing claim was rejected; every core census claim was independently re-measured and CONFIRMED.
- **QC measurement label**: `AUDITOR_RECHECK` (own PE parser, own scan implementations, own byte reads from the physical EXE; scratch outputs under `SCRATCH\QC_FRESH\` only).

---

## 1. Per-duty results

| Duty | Result | Basis (auditor's own measurements) |
|---|---|---|
| D1 IDENTITY | **PASS** | EXE re-hashed by QC: 8,015,872 B / `E7785430…D5280F31` — MATCH. Landmark package `PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003`: **full 84/84 SHA256 census** (not a sample) = executor pre-work baseline, **0 diffs**; cited files verified (`SIDS_ENTRY_PARSE.json` 58F7258A…, `FALSIFIER_REACH_CHECK.json` 09F5989C…); corroborated by empty `git diff 9124e8e` (package is tracked). Reused-project sandbox EXE re-hashed = expected. |
| D2 CENSUS VERACITY | **PASS** (findings F-QC-2, F-QC-4 inside verified windows) | See §2 — all counts, pins, sets, tables and no-4057 independently reproduced. |
| D3 GATE PREDICATES | **PASS_WITH_FINDINGS** | G1 substance PASS but the stated count "12/12 classes" is wrong (F-QC-3); G2 PASS (two index-formula notes wrong — F-QC-2); G3 PASS (.pyc wording over-broad — F-QC-5); G4 PASS (0 promotion violations; preserved distinctions present verbatim; sids-4057 namespace UNRECONCILED, neither label cited as resolved). |
| D4 SCOPE HYGIENE | **PASS** | HEAD = BASE 9124e8e; tracked tree unchanged (`git diff` empty; repo-root AUDIT_ENTRYPOINT.md byte-unchanged); only the new package untracked + 6 pre-existing foreign untracked groups untouched; zero `.pyc` in run scratch/package/historical package; no NIF/GLB/ARK/VFS/BNT physical reads (scripts read only the EXE; "templates.vfs" is an in-EXE string anchor, not a file); both disclosed interventions adjudicated HONEST (c2 bugfix cycle; Ghidra project reuse — the DB re-save disclosed, historical packages byte-verified unchanged). |
| D5 HANDOFF/RECORD QUALITY | **PASS_WITH_FINDINGS** | Census numbers cross-check everywhere (25/23, 35/32, union 32, 12 analyzed, 20 not analyzed = 11+9); EVIDENCE_INDEX §3 hashes 21/21 MATCH; SCRATCH↔package copies byte-identical; records defects F-QC-6..F-QC-10. |

## 2. D2 — the core census, independently re-measured (AUDITOR_RECHECK)

**Subject pins — all MATCH against the physical EXE** (own byte reads + rel32 arithmetic):
- `FUN_0072F580` @0x0072F580: 46 B body (0x0072F580–0x0072F5AD); `E8 9B 1E DA FF` @0x0072F590 → 0x004D1430 (recomputed); `83 C0 14` @0x0072F59E; sentinel `B8 00 58 BA 00` @0x0072F5A5. 19-instruction listing byte-identical.
- `FUN_0043A550` @0x0043A550: 119 B body (0x0043A550–0x0043A5C6); read `A1 24 18 BA 00` @0x0043A571; store `A3 24 18 BA 00` @0x0043A59B; fail-path `33 C0` + store @0x0043A5B2; operator_new call → 0x0095D3C4; ctor call → 0x0052A260 (both rel32 recomputed). 35-instruction listing byte-identical.
- `DAT_00BA1824`: own mapping → within-.data offset 219,172 ≥ raw_size 212,992 → **zero-initialized tail (BSS-like)** ✓; **exactly 3** absolute 4-byte-LE occurrences in the whole file, at operand VAs 0x0043A572 / 0x0043A59C / 0x0043A5B3 = the 3 instruction refs inside FUN_0043A550 (1 READ + 2 WRITE per the raw Ghidra op_types).

**Census counts — my own scans (independent implementation):**

| Measurement | Auditor | Executor | Agreement |
|---|---|---|---|
| E8 rel32 → 0x0072F580 over .text | **25** | 25 | **VA sets IDENTICAL** (0 disagreements) |
| E8 rel32 → 0x0043A550 | **35** | 35 | **VA sets IDENTICAL** (0 disagreements) |
| E9 → either target | **0 / 0** | 0 / 0 | identical |
| Absolute VA occurrences (whole file) | **0 / 0** (targets), **3** (datum) | 0 / 0 / 3 | identical |
| Unique callers (from raw Ghidra) | 23 / 32 (union 32) | 23 / 32 | identical |
| Pair pattern (all 23 lookup callers also call getter) | **confirmed** from raw caller list | claimed | confirmed |

Three-way agreement confirmed: **my raw scan == executor raw scan == Ghidra call refs** (raw `c2_census.json`, all op_type `UNCONDITIONAL_CALL`, non-call refs 0), and **every raw candidate is a defined Ghidra instruction** (60/60, 0 undefined, read from the raw output).

**Window selection rule — VERIFIED against the RAW Ghidra output:** the recorded (non-address-sorted) reference iteration order in the un-curated `SCRATCH\ghidra_out\c2_census.json` lists exactly the 12 chosen windows as its first 12 lookup references; the c2 script's selection logic (first 12 unique callers of the lookup target in `getReferencesTo` order) reproduces the chosen set exactly. The FINAL_REPORT's "first 12 in reference order" claim is honest per the recorded raw order. (The QC did not re-run Ghidra to reproduce the iteration order — that would re-save the reused project DB outside the QC scratch allowance; see NOT_CHECKED.)

**Window content — byte-level verification:**
- **1169/1169** listing instructions across all 12 window files byte-identical to the physical EXE (0 mismatches); + 54 subject-listing instructions; + **656/656** callsite-context-slice instructions — **1879/1879 total, 0 mismatches**.
- Body-end rule 12/12: last instruction RET/RET-imm; following-function content present in `body_end_context` after body_end.
- Four load-bearing windows re-derived in full (see QC_RESULTS.json D2 for the byte traces): FUN_006baa20 (store `89 7E 0C` @0x006BAB60 → **[ESI+0xC] = caller-owned field**; template only receiver of FUN_0072fce0 then stored), FUN_00733490 (`89 37` @0x00733529 → **[EDI] = 3×0x18 record slots at this+0x14**, loop `ADD EDI,0x18` @0x00733542), FUN_006c3f50 (`89 19`/`89 41 04` @0x006C3F8D/F → **vector insert slot**, pair (0x66, FUN_007ce1e0 result); FUN_0040b070(0x8BD720) @0x006C3FB5), FUN_00567170 (immediates 0x3BDA/0x3BDB/0x3BD9/0x3A40/0x3A47 all byte-verified; FLD constants target **stack locals**, never the template; template pushed to FUN_005670a0). **Store targets are caller-owned fields, NOT template fields — confirmed in every case; zero [template+off] operands in all 12 windows.**
- Accessor windows verified incl. table-index formulas: FUN_006c26b0 **A+34B** (CMP EDI,0x22; LEA EDX,[EDI+ECX*2] with ECX=17B) ✓, FUN_006c2700 **16B+A** ✓, FUN_006c27f0 **15B+A** ✓, FUN_006c2840/70 **B*4** ✓ — but FUN_006c2750/70 **physically A+10B** (`8D 04 80` → 5B; `8D 0C 47` → A+2·5B), **claimed A+40B → F-QC-2**. The 10-dword dumps align with stride 10 (= the A-bound), corroborating the correction.
- **No in-window id equals 4057 — CONFIRMED AND STRENGTHENED**: all cited immediates verified ≠ 0xFD9; full dword-0xFD9 sweep of **all 12 window ranges: 0 hits**; and a full **whole-.rdata-section** dword-0xFD9 sweep: **0 hits** — covering all rows of all 7 cited tables, beyond the executor's dumped first-n dwords.
- ID tables 7/7 value-diff MATCH (own reads vs ID_TABLE_DUMPS.json).
- 3 UNKNOWN-provenance windows verified genuinely UNKNOWN (id sources byte-level confirmed to leave the window; no guessed provenance).

## 3. Findings ledger

Severity scale P0–P3. **All four P2s are records/provenance defects requiring correction BEFORE the persistence phase** (otherwise the MANIFEST/entrypoint row would propagate false records). None invalidates the run's science; the valid layers of the run are preserved.

### **F-QC-1 (P2) — EVIDENCE_INDEX c2 script SHA256 field is a 62-character transcription**
- **Where**: `EVIDENCE_INDEX.md` §2, row "c2_ghidra_census.py (EXECUTED version)".
- **Claimed**: `D073EC73994FA3B2A64898CFA6482CFF4FBB111203893C63D59E009AD16091` — **62 hex chars (invalid SHA256 length)**.
- **Actual (AUDITOR_RECHECK)**: `D073EC73994FA3B2A64898CFA6482CFF4FFBBB111203893C63D59E009AD16091` (64 chars). The on-disk file (mtime 09:52:03, before the run outputs 09:52:20–24) is the executed version; s1/s3 recorded hashes both match exactly.
- **Mechanism**: transcription slip ("FFBBB"→"FBB"). **Impact**: manifest-identity defect (source file unchanged ≠ manifest identity correct); the persistence MANIFEST would conflict with this field.
- **Correction**: replace with the actual 64-char hash. **Revalidation**: recompute + assert 64 hex + equality.

### **F-QC-2 (P2) — Wrong table-index formula for windows FUN_006c2750 / FUN_006c27a0 (claimed A+40B; physical A+10B)**
- **Where**: FINAL_REPORT §3 rows 6–7; CALLER_CENSUS.json classification notes ("index = A + 40*B") for both windows.
- **Counter-evidence**: window 05 @0x006C2772 `8D 04 80` LEA EAX,[EAX+EAX*4] → 5B; @0x006C2775 `8D 0C 47` LEA ECX,[EDI+EAX*2] → **A + 10B**; load @0x006C2778 `8B 14 8D 78 57 A8 00`. Window 06 identical at 0x006C27C2/C5/C8 (+0xE variant). The 10-dword table dumps = the A-bound → stride 10 is the coherent reading.
- **Impact**: id-source class, table VAs, load VAs, bounds, question (a)=YES and no-4057 **unaffected**; the recorded stride arithmetic is wrong by 4× in two summary docs + the machine census. Windows 03/04/07/10/11 formulas verified CORRECT.
- **Correction**: (A+40B)→(A+10B) in both documents. **Revalidation**: byte re-read + arithmetic.

### **F-QC-3 (P2) — G1 gate statement "12/12 classes" is wrong (the class universe is C1..C10 = 10)**
- **Where**: FINAL_REPORT §6 G1; HANDOFF G1 ("12/12 reference classes (C1..C10)" — self-contradictory); repeated in the executor's final message.
- **Counter-evidence**: PREREGISTRATION §4 = 10 classes; FINAL_REPORT §2 table = 10 rows; CALLER_CENSUS reference_classes = 10 keys per target; the census's own gates_self_check says "all 10". "12" is the window-budget number.
- **Impact**: G1 substance PASSES (all classes enumerated with method+result; no silent skip; the single NOT_CHECKED sub-class explicitly listed with reason — the executor itself offers "PASS_WITH_ONE_DECLARED_LIMITATION"); the stated denominator is false and inconsistent across the summary layer.
- **Correction**: 10/10 classes × 2 functions. **Revalidation**: count the class keys.

### **F-QC-4 (P2) — Question (b) answer's consumption enumeration omits window 8's in-window derived-object field reads**
- **Where**: FINAL_REPORT §4(b) + CALLER_CENSUS question_answers.b ("Zero direct field accesses … on the returned template object … All consumption is: pointer STORE … and pointer FORWARD").
- **Counter-evidence**: FUN_006c3f50: after `CALL 0x0040b070` @0x006C3FB5 (receiver = template; body CLOSED), the window reads `8B 50 04` MOV EDX,[EAX+0x4] @0x006C3FBE and `8B 00` MOV EAX,[EAX] @0x006C3FC1 — **in-window field reads of the FUN_0040b070 result** (an object derived from the template by method call; identity UNKNOWN while the callee is closed) — forwarded as a pair into FUN_006c3640.
- **Adjudication**: the template POINTER itself is never field-accessed in any window (verified — that sub-claim is TRUE); but the pre-registered (b) asks about objects **derived** from the template, and this in-window read pattern with UNKNOWN semantics is not disclosed in the (b) enumeration. The honest form: "NO transform-relevant access ESTABLISHED; one derived-result read pattern (window 8, byte-pinned) with UNKNOWN semantics". Material for the follow-up list (FUN_0040b070 belongs there alongside FUN_0072fce0 / the FUN_007ce1e0 family).
- **Correction**: add the two byte-pinned reads to the (b) detail + window-8 note. **Revalidation**: byte re-read @0x006C3FBE/C1.

### **F-QC-5 (P3) — G3 ".pyc residue anywhere … cwd" over-broad**
0 in run scratch/package/historical package ✓ (auditor scans), but the repo tree holds 19 pre-existing **foreign untracked** .pyc/__pycache__ artifacts (mtimes 2026-09-14 / 10-03/04: `tools/gamebryo_oracle/**`, foreign NINODE_SLOT17 package) — none from this run. Scope the claim to the run's own locations.

### **F-QC-6 (P3) — Getter "Both paths RET with EAX = the singleton" wrong for the alloc-fail path**
Alloc-fail: JE @0x0043A592 → `33 C0` @0x0043A5B0 → store 0 @0x0043A5B2 → RET @0x0043A5C6 with **EAX = 0**, not a singleton (the package's own decompile shows the three-path structure). Success + already-exists paths do return the singleton. No load-bearing claim depends on it.

### **F-QC-7 (P3) — HANDOFF "AUDIT_ENTRYPOINT.md … (it does not exist yet)" misleading**
The repo-root AUDIT_ENTRYPOINT.md exists (tracked, byte-unchanged — git-verified); only `docs/audits/AUDIT_ENTRYPOINT.md` does not exist (per PREREGISTRATION §8, accurate). Reword.

### **F-QC-8 (P3) — ID_TABLE_DUMPS notes imprecision**
(i) A-family dumps cover only the B=0 row (stride = A-bound; rows B≥1 undumped); (ii) the 37-B twins have **no bounds check on B** (the report's bounds list is A-family only), so "consumed range" is an assumption there — B≥5 reads code VAs/zeros as keys; (iii) "all 7 accessor tables contain id-ranged small integers at the bounds-checked positions" overgeneralizes for 0x00A855D0 whose row-0 dwords 0–7 are code VAs + a string tail (ids start at dword 8). **NO_4057 survives at FULL scope via the auditor's whole-.rdata sweep (0 hits)** — stronger than the executor's dumped-subset claim.

### **F-QC-9 (P3) — "All callee bodies involved (16 names)" is a subset**
The 12 windows contain **92 distinct** non-subject call targets; all stayed closed (fact TRUE — nothing was opened); the 16-name list is the classification-relevant subset. Reword to avoid implying only 16 callees were touched.

### **F-QC-10 (P3) — No dedicated FULL_READ_LOG artifact**
The read/closed discipline is distributed (PREREGISTRATION §5.1/5.2, FINAL_REPORT §3, census) and honest (verified against the window call-edge inventory); a dedicated log file is absent. Optional records improvement at persistence.

## 4. Scope hygiene & intervention adjudication (D4)

- **Git**: HEAD = BASE 9124e8e; `git diff` empty (tracked tree byte-unchanged incl. repo-root AUDIT_ENTRYPOINT.md); only the new package untracked + 6 pre-existing foreign untracked groups (5× PE_935_* + experiments/) untouched.
- **Forbidden reads**: none — all three scripts read only the physical EXE (plus their own JSON outputs). "templates.vfs" appears only as the in-EXE string calibration anchor (auditor re-read both calibration anchors physically: string @0x00A86D30 → off 6,843,696 ✓; `68 D3 3E 00 00` @0x005B6597 ✓).
- **Interventions**: (1) c2 postscript bugfix cycle — **HONEST** (disclosed; failed log overwritten — disclosed; failed first-draft bytes superseded in place, its pre-fix hash unverifiable — disclosed as such; no scientific result depends on it) with the F-QC-1 hash-transcription defect; (2) Ghidra project reuse — **HONEST** (pre-disclosed §6; DB re-save disclosed; scratch ≠ historical package; historical packages byte-verified unchanged by the auditor). No other interventions; no input file modified; STATIC_ONLY held.

## 5. Files created by this QC

- **Package root** (expected QC additions; EVIDENCE_INDEX §3 predates them — the persistence MANIFEST must include them or record their exclusion): `QC_RESULTS.json`, `QC_REPORT.md` (this file).
- **QC scratch only** (`SCRATCH\QC_FRESH\`): `auditor_recheck.py`, `auditor_window_verify.py`, `auditor_pkg_checks.py`, `auditor_stage4.py` + result JSONs (`AUDITOR_recheck_results.json`, `AUDITOR_window_verify.json`, `AUDITOR_pkg_checks.json`, `AUDITOR_stage4.json`) + `AUDITOR_landmark_census_after.txt`. **No executor artifact was modified.**

## 6. FULL_READ_LOG / NOT_CHECKED

Recorded verbatim in `QC_RESULTS.json` (`full_read_log`, `not_checked`). Key NOT_CHECKED items: the executor's final message (not available in this context — every dispatch-restated claim was verified against artifacts); the failed c2 attempt's bytes (no longer on disk, disclosed); Ghidra's internal reference-iteration order not independently re-produced by re-running Ghidra (would re-save the reused project DB outside QC scratch allowance — verified instead against the RAW un-curated output order + script logic, which reproduce the chosen 12 exactly); the 20 IDENTIFIED_NOT_ANALYZED callers' bodies; landmark package content beyond the hash census. **No unchecked load-bearing component of the audited claims remains** — every load-bearing census claim was independently re-measured.

---

**NEXT_PARENT_ACTION (for PE-MASTER's decision, not executed by this QC)**: dispatch a bounded records correction (F-QC-1..F-QC-4 required; F-QC-5..F-QC-10 recommended) BEFORE the persistence phase, then persist (MANIFEST over the final scope including or explicitly excluding the two QC artifacts). The audited science needs no re-measurement — every load-bearing census claim was independently reproduced by this QC.
