# AMEND_LOG_R1.md — PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (pre-publication amendment)

- **Amendment order**: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914, AMENDMENT ORDER
  of 2026-09-14 (PE-MASTER, after MASTER_AUDIT + INTERNAL_QC QC_PASS; adjudicated
  findings QC_AUDIT_R1.md §4). Executor: pe-reconstruction. NO NESTED TASKS. NO HUMAN
  PROMPTS.
- **Amend class**: documentation/render-layer precision corrections — P2-1, P2-2,
  P3-4, P3-5, P3-6, P3-7, P3-8, P3-9, P3-10. NO new science, NO scope expansion, NO
  new claims, NO census-data semantic change (classification rows, counts, candidate
  VAs, RTTI dwords/bytes, positive-control bytes all unchanged — script-asserted below).
- **Git**: ZERO git mutations by this amendment (publication remains a separate later
  step by pe-master-auditor). BASE_SHA re-verified before any change:
  HEAD == origin/master == ls-remote == 1a490eed4ca2b295e78cd3cf851a08ac9c93930b.
- **Physical source pin re-verified (fail-closed asserts in every regenerated run)**:
  Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31,
  size 8015872 (measured by the probe and re-asserted inside census.py and finalize.py).
- **NO `.pre` files** (human budget rule; this log's SHA pairs replace the byte-prefix
  convention for THIS pre-publication amendment). The determinism diff used transient
  before-copies OUTSIDE the package in the opencode temp dir
  (`C:\Users\User\AppData\Local\Temp\opencode\pe935_amend\before\`), never inside it.
- **Untouched per order**: 00_CONTROL/RUN_CONTRACT.md, 00_CONTROL/qc_probe/ (all 12
  files), 06_REPORT/QC_AUDIT_R1.md, prior-run packages, experiments/, every repo file
  outside this package. Before==after hash verification listed in section 9.

## 0. Pre-edit physical verification (adjudicated findings re-measured BEFORE editing)

Probe: `C:\Users\User\AppData\Local\Temp\opencode\pe935_amend\probe_pre_edit.py`
(SHA256 9E5ED5EE3B0FF8F016D2FCC3254B67EEF5B3398ED4BE98231F6C454D4C05425F, read-only
on the EXE, interpreter `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe`,
Python 3.12.7, capstone 5.0.7 from the census.py-pinned path). Measured:

- **P2-1 load/call split** — all four receiver sites decoded from physical bytes:
  load @0x0052901A `8b8ec0000000 mov ecx,[esi+0xc0]` ends exactly at call
  @0x00529020 `e89b04feff call 0x5094c0`; load @0x0067B8E4 `8b4e04 mov ecx,[esi+4]`;
  load @0x0067C8A4 `8b4e04 mov ecx,[esi+4]`; load @0x006A3A29 `8b4e18 mov
  ecx,[esi+0x18]`; calls @0x0067B8E8 / @0x0067C8A8 / @0x006A3A2D all
  `call 0x5094c0`. The three non-adjacent sites carry exactly one intervening
  instruction `push eax` (0x50) between load and call — an argument push, no ECX
  redefinition; the receiver claim is unaffected (QC P2-1's split confirmed).
- **P3-8** — `lea ecx,[esi+0xc8]` @0x007B6037 (bytes `8d8ec8000000`) preceding
  `call 0x788480` @0x007B6047: address-of, not dereference (confirmed).
- **P3-6 true containing stores** — for every pattern-scan hit, the TRUE store
  instruction from its true start (end-anchored: the imm32 is the trailing operand, so
  the true instruction ends at hit+4; asserted to contain the imm in its rendered
  operand): 0x00509369→0x00509366 `c7450058d4a700 mov [ebp],0xa7d458`;
  0x0050A26B→0x0050A269 `c70658d4a700 mov [esi],0xa7d458`;
  0x00509002→0x00509000 `c7012cd4a700 mov [ecx],0xa7d42c`;
  0x0050904A→0x00509048 `c7062cd4a700 mov [esi],0xa7d42c`;
  0x0050A2EE→0x0050A2EC `c7062cd4a700 mov [esi],0xa7d42c`;
  0x008B92F9→0x008B92F7 `c7002cd4a700 mov [eax],0xa7d42c`;
  0x008B9519→0x008B9517 `c7002cd4a700 mov [eax],0xa7d42c`.
- **P3-4 reason census** — derived BY SCRIPT from 01_RAW/SF30_WRITER_RAW.txt why-lines
  (`...\pe935_amend\reason_census.py`, SHA256
  3D360B62CBC5C5EC7F9689124EA64FEF9D5CCE07D755CB142641D34199DDAF92; asserts 3643
  blocks, 3023 REJECTED, 0 R-tags on non-REJECTED rows):
  R-ESP 2765 / R-STACK-PTR 129 / R-CTOR-OTHER 104 / R-ZERO 18 / R-LEA-STACK 3 /
  R-EBP-INHERITED 2 / R-IMM-STATIC 1 / R-CONT-FIELD 1 = 3023; **R-EBP-FRAME = 0 rows**.
  Matches the twice-independently-verified expectation (QC §4 P3-4 + PE-MASTER).
- **G5-trip measurement** — the executor's own G5 substring detector applied to the
  QC additions measures **7 trip lines** (bare forbidden-label quotes inside the
  QC's own census artifacts: out_qc4b_scope_bytes.txt lines 5-6,
  out_qc4_sample_scope.txt lines 95-97, QC_AUDIT_R1.md lines 117 and 234) — foreign
  content with zero negative marker on those same lines. This is the measured reason
  the finalize.py re-run must keep the gate census and manifest to the EXECUTOR SET
  (see finalize.py amendment in section 2.2 and note 8.2).

## 1. Amendments to 00_CONTROL/census.py (edited, then the outputs regenerated)

Before-SHA256 F19756A90550CB68D2937271D9DBC955590196F325629ACDDFBFC33895EACFA1
(1087 lines) → After-SHA256
7c4d705575238ddc4a27d01dcc1ea92bade8fa0ee42d400eb2697f1d75b4723f (1099 lines).
Changed lines ONLY (all others byte-identical):

**1a. P3-6 — section 2.1 vtable-store scan (render bug + true-start decode).**
OLD (the `C.hexdump(pe, h, 0) and ...` falsy short-circuit never printed the hit VA;
first-covering-wins accepted misaligned decodes):
```python
    for back in range(1, 9):
        cand = pe.disasm_one(h - back)
        if cand and cand["va"] < h < cand["va"] + cand["size"]:
            ins = cand
            break
    w("#   hit %s -> store insn: %s" % (C.hexdump(pe, h, 0) and ("0x%08X" % h), C.render(ins) if ins else "?"))
```
NEW (hit VA printed explicitly; containing instruction rendered from its TRUE start
— end-anchored at h+4 — with a fail-closed assert that the rendered store carries
the scanned imm32):
```python
    for back in range(1, 17):
        cand = pe.disasm_one(h - back)
        if cand and cand["va"] <= h and cand["va"] + cand["size"] == h + 4:
            ins = cand
            break
    assert ins is not None and "0xa7d458" in ins["op_str"], (h, ins)
    w("#   hit 0x%08X -> store insn: %s" % (h, C.render(ins)))
```
(plus explanatory comment lines; the subsequent `if ins:` raw-bytes line unchanged).

**1b. P2-1 — F_SF evidence string for FUN_005094C0 (line 196 → 201).**
OLD: `"SF method: called with ecx=SF loaded from proven SF slots: 0x00529020 mov ecx,[esi+0xc0]; 0x0067B8E8 mov ecx,[esi+4]; 0x0067C8A8; 0x006A3A2D"`
NEW: `"SF method: called with ecx=SF loaded from proven SF slots: load @0x0052901A mov ecx,[esi+0xc0] + call @0x00529020; load @0x0067B8E4 mov ecx,[esi+4] + call @0x0067B8E8; load @0x0067C8A4 + call @0x0067C8A8; load @0x006A3A29 mov ecx,[esi+0x18] + call @0x006A3A2D"`

**1c. P3-6 — section 03 fam42c render loop (lines 263-268 → 268-278).**
OLD:
```python
for h in fam42c:
    for back in range(1, 9):
        cand = pe.disasm_one(h - back)
        if cand and cand["va"] < h < cand["va"] + cand["size"]:
            w("#   -> %s" % C.render(cand))
            break
```
NEW (same true-start rule + assert; hit VA explicit):
```python
for h in fam42c:
    ins = None
    for back in range(1, 17):
        cand = pe.disasm_one(h - back)
        if cand and cand["va"] <= h and cand["va"] + cand["size"] == h + 4:
            ins = cand
            break
    assert ins is not None and "0xa7d42c" in ins["op_str"], (h, ins)
    w("#   hit 0x%08X -> store insn: %s" % (h, C.render(ins)))
```

**1d. P3-5 — SF30_PROVENANCE.md RUN header line (inserted after the title line).**
NEW: `prov_md.append("RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")`

**1e. P3-8 — block-ctor hop note for 0x007B6047 (line 818 → 829).**
OLD: `"call 0x788480 with ecx=[block+0xC8] (callee NOT analyzed)"`
NEW: `"call 0x788480 with ecx = &block[+0xC8] (lea ecx,[esi+0xC8] @0x007B6037 — address-of, not dereference) (callee NOT analyzed)"`

**1f. P3-5 — POSITIVE_CONTROL RUN header line (inserted as pc_lines line 2).**
NEW: `pc_lines.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")`

**1g. P3-5 — SF30_WRITER_RAW.txt RUN header (line 959 → 971).**
OLD: `raw.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (STATIC-ONLY)")`
NEW: `raw.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")`

**1h. P3-5 + P2-2 — SF30_RTTI_RAW.txt headers (lines 1007-1008 → 1018-1020).**
OLD line 1007: `rt.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (STATIC-ONLY)")`
NEW line 1019: `rt.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")`
OLD line 1008: `rt.append("# walker: object -> vtable -> [vtable-4]=COL -> COL.pTypeDescriptor -> TD -> TD+0x0C name")`
NEW line 1020: `rt.append("# walker: object -> vtable -> [vtable-4]=COL -> COL.pTypeDescriptor -> TD -> TD+0x08 name")`

**1i. P2-2 — TD name-offset label, calibration + link render lines.**
OLD line 1019: `rt.append("# TD+0x0C name bytes (raw) = %s" % cal["td"]["name_raw_hex"])`
NEW line 1031: `rt.append("# TD+0x08 name bytes (raw) = %s" % cal["td"]["name_raw_hex"])`
OLD line 1037: `rt.append("# TD+0x0C name bytes (raw) = %s" % lk["td"]["name_raw_hex"])`
NEW line 1049: `rt.append("# TD+0x08 name bytes (raw) = %s" % lk["td"]["name_raw_hex"])`

**1j. Writer encoding — the four evidence writers now write UTF-8 explicitly**
(`open(..., "w", encoding="utf-8")` for SF30_PROVENANCE.md, POSITIVE_CONTROL_0050A050.txt,
SF30_WRITER_RAW.txt, SF30_RTTI_RAW.txt). Reason: the mandated header/correction text
contains non-ASCII characters (· U+00B7, — U+2014); the host locale default is cp1252,
while the package's .md documents (REPORT.md, HANDOFF.md) are UTF-8 — the explicit
UTF-8 keeps the whole package encoding-consistent. Pure-ASCII content bytes are
unaffected by this change; the CSV writer (newline="" csv) was left untouched.

## 2. Amendments to 00_CONTROL/finalize.py

Before-SHA256 027C8FDC6FF0C1E77542CEDBC524842559E3E8C3CC03FAFD368A5CA32BF2CF84
(286 lines) → After-SHA256
4df58fbf8132168976554189ef4b758a4554d29698f72f32f5bc1cfe46c0b868 (302 lines).
Changed lines ONLY:

**2a. P2-2 — G4 expected string (line 101).**
OLD: `and "TD+0x0C name bytes (raw) = 2e3f41564e694e6f64654040" in rtti_txt`
NEW: `and "TD+0x08 name bytes (raw) = 2e3f41564e694e6f64654040" in rtti_txt`
(kept in sync with 1i — the gate re-passes against the regenerated RTTI raw.)

**2b. Executor-set filter for the G5 census + manifest (lines 112-115 → 112-131).**
OLD:
```python
package_files = []
for root, _dirs, files in os.walk(BASE):
    for f in files:
        package_files.append(os.path.join(root, f))
```
NEW: same walk, but skipping `00_CONTROL\qc_probe\*` and `06_REPORT\QC_AUDIT_R1.md`
(with an in-code comment giving the reason; see note 8.2). No gate predicate, no
forbidden-label detector logic, no negative-marker set was modified (the QC P2-3
detector finding is NOT amended here — it is a next-gate-template fix per the QC
verdict).

**2c. UTF-8 reads of the four amended evidence artifacts** (G1 pc_txt, G2 raw_txt,
G3 prov, G4 rtti_txt now `encoding="utf-8"`), matching 1j so the gate reads the
regenerated artifacts correctly.

## 3. Regeneration commands (exact; interpreter D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe, `-B` so no __pycache__ is created inside the package)

1. `python.exe -B <pkg>\00_CONTROL\census.py` → exit 0, stdout:
   `CENSUS OK / raw candidates: 3643 / classification: {'REJECTED_ALIAS': 3023,
   'POSSIBLE_ALIAS': 618, 'PROVEN_SF30_WRITER': 2} / proven: ['0x005093C3',
   '0x0050A2D1'] / link RTTI: .?AVNiNode@@ vtable 0x00A8CCF4 slots=47
   slot17=0x007B5390 / combined hits: 0 bulk hits: 2`
   (all fail-closed asserts passed; EXE pin re-asserted inside the run).
2. `python.exe -B <pkg>\00_CONTROL\finalize.py` — pass 1 (this AMEND_LOG not yet on
   disk) → exit 0, stdout: `FINALIZE OK / G0..G5: [G0-SOURCE-BASE, G1-POSITIVE-
   CONTROL, G2-CENSUS-COMPLETENESS, G3-PROVENANCE, G4-TYPE-IDENTITY, G5-SCOPE-HELD]
   = [True, True, True, True, True, True] / denominator: 3643 / counts
   {'REJECTED_ALIAS': 3023, 'POSSIBLE_ALIAS': 618, 'PROVEN_SF30_WRITER': 2} /
   manifest rows: 16 / claim_hits: [] / candidates inside forbidden fn ranges: 0`.
3. Pass 2 (after this log was written; identical command) → identical verdicts
   (`[True, True, True, True, True, True]`, claim_hits [], 0 rows inside forbidden
   ranges), manifest rows: 17 (this log included in the executor set). A final
   finalize re-run after this log's last wording edits refreshed the manifest's
   AMEND_LOG row to the final log hash (still 17 rows; every other output
   byte-identical — same hashes as listed in section 6). STAGE_ACCEPTANCE_GATES.csv,
   SOURCE_IDENTITIES.json and SCRIPT_SHA256.csv are byte-identical across all passes
   (hashes in section 6); only MANIFEST_SHA256.csv differs from pass 1 (17th row =
   this log) and from each log-editing pass (its AMEND_LOG row). The manifest's own
   SHA256 is not self-recordable (same regress as its L12 self-exclusion); its final
   on-disk hash is reported in the executor's delivery notice to PE-MASTER.

## 4. Regenerated evidence files (old line → new line; before → after SHA256)

**4a. 00_CONTROL/census_state.json**
778F92F1316757D4A7E74F349B665C7FECE6B30AC14434045886C0BFDDE10739 →
d175e7919c8fa662b089e1e4ee5569ea4a606f6d315bb101af0f7e568add87a3.
Exactly 1 line changed (line 72, the f_sf entry for FUN_005094C0 — the P2-1 string
of 1b). 142 lines before and after.

**4b. 01_RAW/SF30_WRITER_RAW.txt**
E7C7491AC7CD96AD370CD99AF995103396925B06E95BD5F61DDDC75AE9B6C740 →
64402a73013b52943e10ae17bb115f466a0d3bef98aa3835915cf3c1cd572248.
35086 lines before and after; exactly 4 line-regions differ (10 old lines → 10 new
lines; NOTHING else differs in the 2.4 MB file):
- lines 19-21 (§2.1 hit lines, P3-6):
  OLD L19: `#   hit  -> store insn: 00509368  0058d4                   add      byte ptr [eax - 0x2c], bl`
  NEW L19: `#   hit 0x00509369 -> store insn: 00509366  c7450058d4a700           mov      dword ptr [ebp], 0xa7d458`
  OLD L20: `#     raw bytes at 00509368: 0058d4`
  NEW L20: `#     raw bytes at 00509366: c7450058d4a700`
  OLD L21: `#   hit  -> store insn: 0050A269  c70658d4a700             mov      dword ptr [esi], 0xa7d458`
  NEW L21: `#   hit 0x0050A26B -> store insn: 0050A269  c70658d4a700             mov      dword ptr [esi], 0xa7d458`
- line 62 (§2.6, P2-1): the FUN_005094C0 string of 1b.
- lines 83-87 (§03 fam42c, P3-6), OLD misaligned renders →
  NEW: `#   hit 0x00509002 -> store insn: 00509000  c7012cd4a700             mov      dword ptr [ecx], 0xa7d42c` /
  `#   hit 0x0050904A -> store insn: 00509048  c7062cd4a700             mov      dword ptr [esi], 0xa7d42c` /
  `#   hit 0x0050A2EE -> store insn: 0050A2EC  c7062cd4a700             mov      dword ptr [esi], 0xa7d42c` /
  `#   hit 0x008B92F9 -> store insn: 008B92F7  c7002cd4a700             mov      dword ptr [eax], 0xa7d42c` /
  `#   hit 0x008B9519 -> store insn: 008B9517  c7002cd4a700             mov      dword ptr [eax], 0xa7d42c`.
- line 150 (P3-5): `# RUN: ... (STATIC-ONLY)` → `# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY`.
The authoritative `#   classified:` lines (23-24) are UNCHANGED (asserted by the
regenerated run; they were already correct).

**4c. 01_RAW/SF30_RTTI_RAW.txt**
0F3227F605180600BB0CD57035A0822F8379B790E7AD2BE9B4C51FEAD04783C2 →
399c4cfb5a83728b019d51de805bff2fdc2f5d753e87c909f8e0a43e8326aee5.
33 lines before and after; exactly 3 line-regions differ:
- line 2 (P3-5): as 4b's RUN line.
- line 3 (P2-2): `... -> TD -> TD+0x0C name` → `... -> TD -> TD+0x08 name`.
- lines 10 and 23 (P2-2): `# TD+0x0C name bytes (raw) = ...` →
  `# TD+0x08 name bytes (raw) = ...` (the hex byte strings themselves UNCHANGED —
  `2e3f41565363656e654665656465724f626a6563744040` and `2e3f41564e694e6f64654040`).

**4d. 01_RAW/POSITIVE_CONTROL_0050A050.txt**
45305F21A39D95DA0CB0E0C7EE7B9D9B951E3E1C8D3ED0D510EA8E6E09AAF922 →
4bfd3bb14bc815bd8b2b1b4d150430a40df4e848c54ec1214c3898342cfa8d18.
38 → 39 lines; exactly 1 line ADDED (line 2, the P3-5 RUN header). All measured
window bytes/assertion lines UNCHANGED (G1 re-passed).

**4e. 02_ANALYSIS/SF30_PROVENANCE.md**
213A176B44DB84A8E6283421E6AB27583040A08C0B807BE363B187741A6C006A →
a2f48326ce7b795b8b4067c6e719cbdbf0a082627a1c2b660c36d980a296452c.
71 → 72 lines; 2 line-regions differ:
- line 2 ADDED (P3-5): `RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY`
- line 41 → 42 (P3-8):
  OLD: `- 007B6047 `call 0x788480` call 0x788480 with ecx=[block+0xC8] (callee NOT analyzed)`
  NEW: `- 007B6047 `call 0x788480` call 0x788480 with ecx = &block[+0xC8] (lea ecx,[esi+0xC8] @0x007B6037 — address-of, not dereference) (callee NOT analyzed)`

**4f. 02_ANALYSIS/SF30_WRITER_CENSUS.csv — BYTE-IDENTICAL (determinism assert).**
71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0 → same
(hash-compare of the regenerated file vs the before-copy: 0 differing lines of
3644; its 6 data columns carry none of the amended strings). Counts recomputed by
finalize.py from the CSV rows: **3643 total / 2 PROVEN_SF30_WRITER / 618
POSSIBLE_ALIAS / 3023 REJECTED_ALIAS / 0 UNRESOLVED — UNCHANGED.**

## 5. 06_REPORT/REPORT.md amendments

A6F8335F7D0350C44B92F53A95B4D44B04AB79CCC0FB25563678BC755188BAF2 →
e08a5875790f5a3fdca539c5a3be4c717515d08abbe5937f73cd33ceece5436d.
Five changed regions (all other lines byte-identical):

**5a. P3-10 + P3-9(a) — section 2 BEFORE/AFTER bullets.** BEFORE gains the
canon-completeness note ("the accepted PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_
20260913 had ALREADY established (own decode, its REPORT §4.1 FUN_00509330 line) that
the SF ctor performs new(0x118) → FUN_007B6000 → stores at SF+0x30, with refcount at
block+4, characterized as a 'scene object' with NO class name"). AFTER: "the field's
proven lifecycle transitions (create in ctor / release+null in dtor) are byte-locked
(mid-life writers bounded by the census residue, §3/§7)" + "THIS run independently
CONFIRMS that prior-run chain byte-level and adds: the complete writer census (incl.
the dtor nulling), the calibrated RTTI class identity .?AVNiNode@@ (newly published),
the slot-17 value, and the census bound. P1 provenance chain: byte-confirmed
(consistent with the prior-run association; class identity NEW)."

**5b. P2-1 — C9 row example.**
OLD: `(e.g. 0x00529020 `mov ecx,[esi+0xc0]; call 0x5094c0`)`
NEW: `(e.g. load @0x0052901A `mov ecx,[esi+0xc0]`; call 0x5094c0 @0x00529020)`
(rest of C9 unchanged.)

**5c. P3-9(b) — C8 row.**
OLD: `at the 7 proven container callsites → ZERO hits (see C10);`
NEW: `at the 5 proven container functions (7 store sites) → ZERO hits (see C10);`

**5d. P3-7 — C11 row.**
OLD: `— the positive-control window re-read (allowed) is the only touch. |`
NEW: `— the positive-control window re-read (allowed) is the only touch of forbidden
callees IN THE PACKAGE CONTENT; the gate machinery derived the forbidden functions'
extents by in-memory boundary-only decode (no semantics extracted, nothing
persisted). |`

**5e. P3-4 — section 3 POSSIBLE_ALIAS bound paragraph.**
OLD: `with per-row reasons (R-ESP stack slots; R-EBP-FRAME / R-EBP-INHERITED frames;
R-LEA-STACK; R-IMM-STATIC — ...; R-CTOR-OTHER — ...; R-CONT-FIELD — ...; R-ZERO null base).`
NEW: `with per-row reasons; fired-reason census recomputed by script from the raw
why-lines of 01_RAW/SF30_WRITER_RAW.txt: **R-ESP 2765 / R-STACK-PTR 129 /
R-CTOR-OTHER 104 / R-ZERO 18 / R-LEA-STACK 3 / R-EBP-INHERITED 2 / R-IMM-STATIC 1 /
R-CONT-FIELD 1 = 3023**; **R-EBP-FRAME: rule present, never fired (0 rows)**.`
(numbers are the verbatim output of reason_census.py, never hand-typed.)

## 6. Control/report files regenerated by finalize.py

- **06_REPORT/STAGE_ACCEPTANCE_GATES.csv — BYTE-IDENTICAL to the pre-amend file**
  (375798E82C80E7ED4EC388DB486A22856C9409A5A397FF10582E1D0188121968 both before and
  after; all six rows PASS with the same raw-evidence text; byte-identical across
  all finalize passes).
- **00_CONTROL/SOURCE_IDENTITIES.json — BYTE-IDENTICAL to the pre-amend file**
  (0F6A72721168222619BDA4BC3913D7F71E9AAC151919986E831D0015E57BB1FF).
- **00_CONTROL/SCRIPT_SHA256.csv**
  9A038D997DC43CDE99712A24523F07E99D6AE735855F922AC94D70E4A199277F →
  0C2DE0B2C7DB5FDDE7D71D883351A8FE540A49C8B7AA9D809312561BE2228B61. Three rows
  updated (census.py 7c4d7055…, finalize.py 4df58fbf…, census_state.json d175e791…);
  the sf30_core.py row is UNCHANGED (cd6bc11f… — that script was not amended;
  its rtti_walk already reads TD+0x08, `td_raw[8:]`).
- **06_REPORT/MANIFEST_SHA256.csv** — regenerated after each finalize pass
  (deterministic): pass 1 (this log absent) = 16 rows, SHA256
  850AFABB42F8C94126D06AD307BA9A18F27E5D74F915BD5F91703A91C437FB40; the pass after
  this log first existed = 17 rows = the executor set + this log (self-excluded as
  always); the FINAL pass (after this log's last wording edits) keeps 17 rows with
  the AMEND_LOG row updated to this log's final hash — that final manifest's own
  SHA256 is reported in the executor's delivery notice to PE-MASTER (not
  self-recordable here, same regress as its L12 self-exclusion). Rows for unchanged
  files (RUN_CONTRACT.md, SOURCE_IDENTITIES.json, sf30_core.py,
  SF30_WRITER_CENSUS.csv, 03_EVIDENCE/README.md, HANDOFF.md,
  STAGE_ACCEPTANCE_GATES.csv) keep their pre-amend hashes; the manifest
  still covers the EXECUTOR SET only — the QC additions stay outside it by the
  QC_AUDIT_R1.md §9 convention (see 8.2).

## 7. Determinism + counts asserts (all script-asserted, not hand-checked)

- SF30_WRITER_CENSUS.csv: **BYTE-IDENTICAL** (SHA 71552E2A… unchanged).
- SF30_WRITER_RAW.txt: differs in **exactly 4 line-regions (10 lines replaced by 10
  lines; line count unchanged at 35086)** — listed in 4b; zero other byte differs.
- SF30_RTTI_RAW.txt: 3 line-regions; POSITIVE_CONTROL: +1 line;
  SF30_PROVENANCE.md: +1 line + 1 replaced line; census_state.json: 1 line.
- Counts: **3643 total / 2 PROVEN / 618 POSSIBLE / 3023 REJECTED / 0 UNRESOLVED** —
  recomputed by finalize.py from the CSV rows and cross-checked against the raw
  blocks and census_state.json (all three agree; sweep stats 2,266,698 decoded / 64
  restarts unchanged). No classification row, candidate VA, RTTI dword/byte or
  positive-control byte changed anywhere.
- **All gates G0–G5 re-run PASS** (every finalize pass: True ×6, claim_hits [],
  0 rows inside forbidden ranges; STAGE_ACCEPTANCE_GATES.csv regenerated
  byte-identical to the pre-amend file).

## 8. Disclosure notes

**8.1. P2-2 label origin (contract text NOT edited, per order).** The "TD+0x0C" label
originated in the contract's formalization text (RUN_CONTRACT.md line 59, "TypeDescriptor
-> TD+0x0C name string") — a PE-MASTER dispatch defect carried verbatim into the
contract. The executed walker always read +0x08 (sf30_core.py `td_raw[8:]`), the
mandatory known-answer calibration PASSED, and INTERNAL_QC + PE-MASTER byte checks
confirm TD+0x08 = `2e3f4156…` (".?AV…" prefix present) is the correct MSVC
TypeDescriptor layout (vfptr@+0, spare@+4, name@+8). RUN_CONTRACT.md is a verbatim
contract record and stays untouched; this log is the required statement of the
defect's origin.

**8.2. finalize.py executor-set filter (gate-input stability, not a gate change).**
At the original finalize run the QC additions did not exist, so os.walk(BASE) WAS the
executor set. The INTERNAL_QC round then added 00_CONTROL/qc_probe/ (12 files) and
06_REPORT/QC_AUDIT_R1.md. The re-run MUST NOT silently absorb foreign content into
the gate census or the manifest: (a) QC_AUDIT_R1.md §9 itself declares the probe
inventory "outside the executor's manifest by convention"; (b) my measured trip
check (section 0) shows 7 lines in the QC additions that would trip the executor's
G5 substring detector as bare label-quotes — QC census-artifact lines, not this
run's claims. The filter restores the gate's input universe to exactly the executor
package (original semantics); no detector/predicate logic was touched, and the
QC's P2-3 detector-permissiveness finding is deliberately NOT fixed here (it is a
next-gate-template fix per the QC verdict).

**8.3. Encoding.** The four regenerated evidence files are now UTF-8 (see 1j); all
are valid UTF-8 with the mandated header line; pure-ASCII lines are byte-identical
to the pre-amend files.

**8.4. Hygiene.** Both re-runs used `-B` (no __pycache__ created; verified absent
inside the package). No file was created inside the package except this log. The
temp-dir scripts (probe_pre_edit.py, reason_census.py, diff_regenerated.py) and
before-copies live OUTSIDE the package under
C:\Users\User\AppData\Local\Temp\opencode\pe935_amend\ and are not package content.

## 9. Untouched verification (before == after SHA256, measured after all edits)

- 00_CONTROL/RUN_CONTRACT.md 7416A3C9642D4E088ABBFB5548242E1511E966C63468E12839842270810D6609 (== pre-amend)
- 00_CONTROL/sf30_core.py CD6BC11F2AF482FD587BF24D6291242CAF652FB0189CEBB83B7A18A2EE42907E (== pre-amend; NOT amended)
- 06_REPORT/QC_AUDIT_R1.md B80DD10B42F9A40EC1E211CF3DD508D4206B35017B3E3F64370AAC338EF6040A (== pre-amend; the QC's own record)
- 00_CONTROL/qc_probe/ all 12 files — hashes equal to QC_AUDIT_R1.md §9's inventory
  (qc1_counters.py BB7FF3AD…, qc2_bytes.py DCE9091A…, qc3_sweep.py 9AF5B188…,
  qc4_sample_scope.py 22E9AC4C…, qc4b_scope_bytes.py 430B80CE…, qc5_final.py
  2DDAD0CB…, out_qc1_counters.txt DFE4B37D…, out_qc2_bytes.txt DB3BC4CF…,
  out_qc3_sweep.txt 05509B77…, out_qc4_sample_scope.txt 6786160F…,
  out_qc4b_scope_bytes.txt 741CFF60…, out_qc5_final.txt 71B99BC7…).
- 03_EVIDENCE/README.md FDBE55B810583EC33833B16A8DA48553BDB207A4A14474D087445004F64BC360 (== pre-amend)
- 06_REPORT/HANDOFF.md 71A2B1C127ECF4F7191BB9D8E3B3B769B2E41EAAF38137C8D6CA45610E943BC8 (== pre-amend)
- Repo state: HEAD == BASE_SHA 1a490eed4ca2b295e78cd3cf851a08ac9c93930b; zero git
  mutations (status shows only this untracked package + the foreign untracked
  experiments/, untouched).

## 10. Amendment tooling inventory (outside the package, temp dir)

- probe_pre_edit.py — SHA256 9E5ED5EE3B0FF8F016D2FCC3254B67EEF5B3398ED4BE98231F6C454D4C05425F
- reason_census.py — SHA256 3D360B62CBC5C5EC7F9689124EA64FEF9D5CCE07D755CB142641D34199DDAF92
- diff_regenerated.py — SHA256 B0116068FBFB42DAE94004AC66A938A1E1ADE65D23BD3F0B972A4B938217264A
- before\ (8 transient before-copies used for the determinism diff; never inside the package)

— pe-reconstruction, amendment executor, 2026-09-14. RUN_STATUS: COMPLETE.
