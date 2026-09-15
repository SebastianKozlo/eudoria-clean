# AMEND_LOG_R1.md — PE_935_SF_ARG2_PROVENANCE_R1_20260914 — R1 CORRECTION BATCH

Executor: pe-reconstruction, executing the bounded correction batch dispatched by
PE-MASTER for loop `2ed038db-5d2e-4e7e-b679-2d29bf57501a` (EU935-M1). Batch date:
2026-09-14. MODE: STATIC-ONLY (Entropia.exe never executed; byte reads only).
ZERO git mutations (HEAD `f239eb85cd0f56ae10cee52d57833a49f225965c` unchanged
start→end; zero staged paths; no commits; untracked set unchanged). All outputs
stay inside this package. Canonical interpreter
`D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (Python 3.12.7),
`-B`, no pycache (verified: no `__pycache__`/`.pyc` created).

This record documents the adjudicated corrections applied to the run package after
the fresh QC (`QC_PASS_WITH_FINDINGS`) and PE-MASTER's adjudication audit. The
immutable inputs (RUN_CONTRACT.md, SOURCE_IDENTITIES.json,
GIT_OBSERVATIONS_AT_FORMALIZE.md) and 06_REPORT/QC_AUDIT.md are untouched;
QC_AUDIT.md stays verbatim (its verification gap is recorded by PE-MASTER, not
edited into the QC file).

---

## 1. The PE-MASTER adjudication finding (the P1 defect both executor and QC missed)

The run claimed (REPORT/HANDOFF/ANALYSIS/SCIENCE_STATUS_DELTA + the generator's
embedded text + the ARG2_PRODUCER_TRACE.txt raw): *"the SF primary-vtable
functions FUN_0050A460/0x5090A0/0x5090B0/0x50A050/0x5090C0 are ALSO slots 11..15
of the .?AVArkAudioObjectInterface@@ vtable — SceneFeederObject shares its slot
functions with ArkAudioObjectInterface (inheritance family)."*

**This is FALSE — a VTABLE-BOUNDARY OVERRUN ARTIFACT.** Every pin below was
re-derived in this batch from the pinned Entropia.exe (SHA256
`E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`, size
8015872, fail-closed S0; raw evidence: `01_RAW/AMEND_R1_PIN_REVERIFICATION.txt`,
all pins MATCH):

**The TRUE .rdata layout (re-derived; the adjudicated truth):**

| VA | content | value |
|---|---|---|
| 0x00A7D428 | ArkAudio vtable[-1] COL pointer | 0x00AA1270 |
| 0x00AA1270 | ArkAudio COL: sig 0, ptd | ptd 0x00B7880C → TD name `.?AVArkAudioObjectInterface@@` |
| 0x00A7D42C | ArkAudio vtable slot 0 | 0x00509040 |
| 0x00A7D430 | ArkAudio vtable slot 1 | 0x0096B960 |
| 0x00A7D434 | ArkAudio vtable slot 2 | 0x0096B960 |
| 0x00A7D438 | ArkAudio vtable slot 3 | 0x00509010 |
| 0x00A7D43C | ArkAudio vtable slot 4 | 0x0096B960 |
| 0x00A7D440 | ArkAudio vtable slot 5 | 0x007E19D0 — **the vtable ENDS here (exactly 6 slots)** |
| 0x00A7D444..0x00A7D452 | the ASCII string `ArkSceneFeeder\0` | `41 72 6B 53 63 65 6E 65 46 65 65 64 65 72 00` (+pad 00 @0x00A7D453) |
| 0x00A7D454 | SF vtable[-1] COL pointer | 0x00AA12B8 |
| 0x00AA12B8 | SF COL: sig 0, ptd | ptd 0x00B78834 → TD name `.?AVSceneFeederObject@@` |
| 0x00A7D458 | SF vtable slot 0 | 0x0050A460 |
| 0x00A7D45C | SF vtable slot 1 | 0x5090A0 |
| 0x00A7D460 | SF vtable slot 2 | 0x5090B0 |
| 0x00A7D464 | SF vtable slot 3 | 0x0050A050 (the imm32-census exactly-one dword) |
| 0x00A7D468 | SF vtable slot 4 | 0x5090C0 |
| 0x00A7D46C | SF vtable slot 5 | 0x509580 — **the SF vtable ends here (exactly 6 slots)** |
| 0x00A7D470 | first non-code dword past the SF vtable | 0x53565064 (not in .text — extent ends) |

**Why the memberships were artifacts:** the pre-fix generator enumerated a FIXED
16 slots from each COL-derived vtable start with a loose plausibility check
(`0x00400000 <= fv < 0x10400000`, no break on a non-hit). Reading 16 dwords from
0x00A7D42C reads through the 6 real slots, the `ArkSceneFeeder` string bytes
(slots 6–9 — all rejected by the loose check too: slots 6–8 exceed 0x10400000,
slot 9 = 0x00007265 falls below 0x00400000), the SF COL pointer (slot 10,
ACCEPTED as a junk "function"), and the SF vtable slots 0–4 (slots 11–15,
ACCEPTED). The "(ArkAudioObjectInterface, 11..15)" memberships for the SF slot
functions are exactly those overrun dwords: `(0x00A7D458 - 0x00A7D42C)/4 = 11` …
`(0x00A7D468 - 0x00A7D42C)/4 = 15` (re-derived).

**Function-pointer sharing is EXCLUDED by the run's own evidence:** the
whole-file imm32 census of 0x0050A050 (re-derived in this batch: hit count = 1,
VA 0x00A7D464, .rdata) — the address occurs EXACTLY ONCE in the entire file, at
the SF vtable slot-3 dword. NO function is shared; NO inheritance relationship
between SceneFeederObject and ArkAudioObjectInterface is established by this
adjacency (any such claim stays UNVERIFIED).

## 2. The QC findings and their fixes (06_REPORT/QC_AUDIT.md stays verbatim)

- **P1-QC-1 (aggregate error):** the method-1 aggregate "23,671 holder reads" was
  arithmetically wrong; the package's own raw enumerates +0x04: 12,535;
  +0x0C: 5,957; +0x10: 2,615; +0x14: 2,841; +0x18: 1,761; +0xC0: 196.
  **Re-derived in this batch by script from the raw: SUM = 25,905 (MATCH).**
  Fixed in: 06_REPORT/REPORT.md (ARG2_PROVENANCE row), 06_REPORT/HANDOFF.md (W2
  line), 06_REPORT/STAGE_ACCEPTANCE_GATES.csv (G2 MEASURED_QUANTITY),
  02_ANALYSIS/ARG2_ANALYSIS.md (§1.2 method-1). Error direction was conservative
  (more reads occurred than claimed); the results (18 flows, 0 PROVEN, 17+1 ABI)
  are unaffected.
- **P3-QC-1 (off-by-one):** EVIDENCE_INDEX.csv's CENSUS_IMM32 row cited the
  CAL-1 ctor-store hit as "0x00509368"; the raw and the bytes give the imm32
  operand position 0x00509369 (inside `C7 45 00 58 D4 A7 00` @0x00509366).
  Fixed in 03_EVIDENCE/EVIDENCE_INDEX.csv (0x00509369).
- **P3-QC-3 (paraphrase; FIX-5):** ARG2_ANALYSIS.md §1.2 described the held-object
  refcount increment as `add [ecx+4],1`; the actual instruction is
  `mov edx,1` (`BA 01 00 00 00`) then `add [ecx+4],edx` (`01 51 04`) —
  re-derived in this batch from the bytes @0x006FABA0 region (MATCH).
  Found in exactly ONE analysis-layer location (02_ANALYSIS/ARG2_ANALYSIS.md
  §1.2); NOT present in any raw (the raw decode carries the true bytes). Fixed
  there; no raw touched.
- **P2-QC-1 (latent +0xC0 disp8 sign-extension defect): RECORDED, NOT FIXED** —
  not in this batch's assigned fix list; latent with zero outcome impact this
  run (per the QC's own measurement: 78 true disp32 reads + 118 `[base−0x40]`
  reads; none flows into a slot-3 vcall). Left for PE-MASTER's disposition.
- **P3-QC-2 / P3-QC-4:** no action required per the QC (P3-QC-2's high-slot
  membership positions are now further contextualized by the extent fix — see §5).

## 3. Every before/after SHA256 pair (script-computed; the reverify raw carries the measured after-values)

| File | Before (pre-batch) | After (post-batch) | Change |
|---|---|---|---|
| 00_CONTROL/w2c_w3_virtual_census.py | AB84C09F9E67E16A08A9FEB87BEB96DB7BD2636F8BB2E2C400C25234A4D404C4 | 576A37D09C18958BD5CB841AB22CE6D8B1CCC807CD8A678DEF7525E4CF94B40B | FIX-1 (extent rule + corrected statement) |
| 01_RAW/ARG2_PRODUCER_TRACE.txt | FD10AABD5294987F0386402671DBE118098515C4606E1F0B97C8FFB68FCFDBC6 | 10AA922952A0A8AE3280EED55BBB48F928A39A44DD153FC39B442DBD6455655F | FIX-2 (regenerated by the fixed generator) |
| 06_REPORT/REPORT.md | 1C2FA523C0CC4AE5B09F1F96101F6CB308EC7377FD73AFFFD5B1AA50047D6DD8 | 99CDC3A8FD740CFCA1EEC481A8B092C99E1E6C6CDE6E5ED2D2383FA708C1B453 | FIX-3/4 (aggregate 25,905; adjacency correction; P1 item-2 retraction) |
| 06_REPORT/HANDOFF.md | 181FA60C38CE74C15D231E13FF3B1AC01F90E62DA7601CCA16AC169B1DCE1096 | E9DB229D1155A0508CE361E5B3E0D1654C6150438C83452533FA9DB5492D7FF1 | FIX-3/4 (aggregate; shared-slots P1 retracted, corrected adjacency) |
| 02_ANALYSIS/ARG2_ANALYSIS.md | A3084985EC9501C88DBEAD6A203495218F109F315B0EFE322360BE362FA0EF4A | EFA11922A0247F0879B3B43280155785CE2795854B43D38B7A791BF7D19DB5B9 | FIX-3/4/5 (aggregate; §1.4 + §3 corrections; `mov edx,1; add [ecx+4],edx`) |
| 02_ANALYSIS/SCIENCE_STATUS_DELTA.csv | BE226BFB9C463B062B459B738168CED6E99F63EC5C10623098FF11EAEBB93422 | 320D2916BC57B7E00164AD0229C1A08A5F236EA12609E24932BE72BF4221CEC0 | FIX-3 (arg2-semantic-role evidence note; status UNVERIFIED unchanged) |
| 03_EVIDENCE/EVIDENCE_INDEX.csv | C0A6E41F34D7252FB9721B141209751CC9D176FBE05BCF0FE7B739979417344C | 901D2FAB8B154CC229A67842FA18CFA4589CFA844B4B9DA204E2B0674F2278E8 | FIX-3 (trace row: post-fix generator SHA + regeneration record; 0x00509369; two new amendment rows) |
| 06_REPORT/STAGE_ACCEPTANCE_GATES.csv | 8CABF14AC4C2C1D7FE2F516A87341EA3F9C6B596EF702077EBFC57FFD362F3C4 | 1A04E6311FBFF63D2DF15AC9B3A6A3BFDD62C8661E146356BEE62CF24E971093 | FIX-4 (G2 aggregate 23,671→25,905; no vtable-membership numbers appear in the G2 row, so no extent note was added there) |
| 00_CONTROL/SCRIPT_SHA256.csv | D4E09661FC8FE786E7FE4D7DD44714F8B91624F7767532823C4E6AE49A794C8A | C2A092CFAD5D9CF032837BB5EC99EDE33E382668AB887066190BF18C675C1C1E | registry update (w2c row → post-fix hash; new amend_r1_reverify.py row) |
| 06_REPORT/MANIFEST_SHA256.csv | 45A874B7A9C9CCF98E701C813689084B228328B2E10EB7B38EC73C8248DA988E | (regenerated last, after this record; no self-row convention — its post-batch identity is verified by the final verification pass recorded in the delivery notice) | registry update (changed rows + 3 new files) |
| 01_RAW/VIRTUAL_CALLSITE_CENSUS.csv | 7B74CB5D04E13D692207760A6DA40AD3FB3840AAB7502B457685AB2DF9EE8009 | **UNCHANGED (byte-identical, by batch design — see §5)** | — |
| 06_REPORT/QC_AUDIT.md | 216FA97D6EF19C361BA2EC68D7EBE91A06E59C6B0710E7EEE59907ACF3CEA87A | **UNCHANGED (verbatim per the batch constants)** | — |
| 00_CONTROL/amend_r1_reverify.py | (NEW) | 3CFC93E5790F32818D522CE0CB31FFCA36EA357AE8A0A92D8882DDAD93517CE8 | NEW (batch: pin re-derivation, fail-closed) |
| 01_RAW/AMEND_R1_PIN_REVERIFICATION.txt | (NEW) | 06051DC1DAA65A2FC928AAF60357665520B910165D3822CC0A29CBEEFA933B30 | NEW (its output; deterministic ×2) |

All other package files: byte-identical to their pre-batch MANIFEST_SHA256.csv
rows (asserted by `amend_r1_reverify.py` against the PRE-BATCH manifest —
**IMMUTABILITY ASSERT: PASS, 0 fails**; see the raw).

## 4. The regeneration record — 01_RAW/ARG2_PRODUCER_TRACE.txt (FIX-2)

- **Rationale:** the raw carried a PE-MASTER-adjudicated false "STRUCTURAL
  FINDING (measured)" claim (the shared-slots statement). A raw carrying a
  proven-false 'measured' claim cannot be published; this is the ONE case where
  a raw is regenerated. The regeneration is DISCLOSED here, was performed by the
  FIXED (post-FIX-1) generator, and is deterministic (re-run twice,
  byte-identical — §9).
- **Exact regeneration command** (canonical interpreter, `-B`, workdir = this
  package's 00_Control):
  `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe -B w2c_w3_virtual_census.py`
  (executed twice; both runs byte-identical for both outputs).
- **Old SHA256:** FD10AABD5294987F0386402671DBE118098515C4606E1F0B97C8FFB68FCFDBC6.
- **New SHA256:** 10AA922952A0A8AE3280EED55BBB48F928A39A44DD153FC39B442DBD6455655F.
- **Corrected content summary (the complete diff, script-measured):**
  1. L10: "vtable-slot function map: 6713 functions" → **4843** (the
     extent-rule count; the pre-fix map carried 3,270 overrun-fabricated entries).
  2. The memberships line: each SF primary-vtable function now has EXACTLY ONE
     membership (the SF vtable itself, slots 0..5) — the false
     "(ArkAudioObjectInterface, 11..15)" entries are gone.
  3. The false "STRUCTURAL FINDING (measured)" line is REPLACED by three
     measured lines: STRUCTURAL CONTEXT (exactly-one membership + the imm32
     census bound), ADJACENCY FACT (the ArkAudio vtable @0x00A7D42C, exactly 6
     slots + slot values; the SF vtable @0x00A7D458, 6 slots; the
     `ArkSceneFeeder\0` string @0x00A7D444; the SF COL 0x00AA12B8 @0x00A7D454),
     and the adjacency-is-not-sharing statement (vtable-boundary overrun
     correction; no semantic promotion).
  4. The REJECTED_NOT_SF demo line for 0x007f1d73: the enclosing-method class
     list shrinks to the extent-verified single class
     (`.?AVNiBoundingVolume@@`, slot 1) — see §5.
  5. The closest-candidate section: FUN_006FAB80's vtable membership list is
     now extent-verified (5 classes, down from the pre-fix 10 — see §5); the
     section's class focus consequently shifts
     (`.?AVArkAnimationAlpha@@` → `.?AVArkAnimationCyclic@@`) with the
     corresponding vtable-store context disassembly.
  6. ALL census outcomes are UNCHANGED: CAL-3 PASS; 218 candidates;
     211 INSUFFICIENT_PROOF / 5 REJECTED_NOT_SF / 2 NOT_A_VTABLE_CALL;
     0 verified SF slot-3 sites; the 18 method-1 flows (identical read sites
     and offsets); 17 ABI-incompatible + 1 ABI-compatible; the six method-1
     per-offset buckets (12,535 / 5,957 / 2,615 / 2,841 / 1,761 / 196; aggregate
     25,905).
- The generator co-writes `01_RAW/VIRTUAL_CALLSITE_CENSUS.csv`; its post-fix
  regeneration differs from the frozen raw in EXACTLY ONE row (see §5) and was
  NOT applied — the raw stays byte-identical per the batch constants.

## 5. NEW_FINDING (correction-batch discovery; NOT adjudicated) — CORRECTION_REQUEST to PE-MASTER

The mandated vtable-extent fix (FIX-1) has two downstream consequences on
membership lists that were NOT in the adjudicated defect list. They are
re-derived in `01_RAW/AMEND_R1_PIN_REVERIFICATION.txt` (PIN SET 5) and recorded
here for PE-MASTER's adjudication. Per the batch scope rule ("fix EXACTLY the
listed items"), no additional document edits were made for them.

1. **VIRTUAL_CALLSITE_CENSUS.csv, row for VA 0x008046070 (candidate 0x007f1d73):**
   the fixed generator's regeneration produces a byte-identical CSV EXCEPT this
   one row's evidence string:
   - before (frozen raw, kept): `... = vtable slot function of classes
     ['.?AVNiBMPReader@@', '.?AVNiBoundingVolume@@', '.?AVNiSGIReader@@'] (all
     non-SF) ...`
   - post-fix (NOT applied): `... = vtable slot 1 of RTTI class
     .?AVNiBoundingVolume@@ (its this is a .?AVNiBoundingVolume@@, not an SF) ...`
   The NiBMPReader/NiSGIReader memberships were overrun artifacts of the same
   class as the adjudicated ArkAudio case; the genuine (extent-verified)
   membership is `.?AVNiBoundingVolume@@` slot 1. **Classification
   REJECTED_NOT_SF and all counts are UNCHANGED either way.** The frozen raw was
   retained byte-identical (batch constant: all other raws stay byte-identical);
   a regeneration of this row would need PE-MASTER authorization.
2. **FUN_006FAB80 (the ABI-compatible forwarding-thunk family):** its pre-fix
   10-class membership list shrinks to 5 extent-verified classes
   (ArkAnimationCyclic / CyclicLinear / CyclicSin / Derivatives / Predefined;
   the Alpha / AnimatedTexture / Color / ArkModelResourceInstanceRef /
   ArkRefObject memberships were overrun artifacts). Consequently the
   documents' phrase "shared slot function of 10 RTTI classes" (REPORT.md
   ARG2_PROVENANCE row; HANDOFF.md W3 line; ARG2_ANALYSIS.md §1.2 closest-
   candidate paragraph; EVIDENCE_INDEX.csv rows 13–14) now disagrees with the
   regenerated raw's 5-class measurement. Those statements were NOT edited in
   this batch (outside the listed items) and are flagged for PE-MASTER's
   adjudication. The run's conclusions do not depend on the count (the thunk's
   receiver class was and remains UNPROVEN within the declared bound; the
   ABI-compatibility finding stands).
3. **QC cross-reference:** QC_AUDIT.md §4–§5 verified the pre-fix memberships
   ("0x007F1D70 of NiBMPReader/NiBoundingVolume/NiSGIReader"; "EXACTLY the 10
   claimed classes") with the same overreading method, and QC §5 confirmed the
   shared-slots P1 — all superseded by the adjudication/extent rule. The QC file
   stays verbatim; this section is the correction of record.

## 6. The corrected structural statement (canonical text)

Each SF primary-vtable function has EXACTLY ONE vtable membership — the SF
vtable itself (slots 0..5); the run's whole-file imm32 census independently
bounds FUN_0050A050 to EXACTLY ONE address occurrence in the file (the SF
vtable slot-3 dword 0x00A7D464). The `.?AVArkAudioObjectInterface@@` vtable
(0x00A7D42C, exactly 6 slots, RTTI-verified:
0x00509040/0x0096B960/0x0096B960/0x00509010/0x0096B960/0x007E19D0) is ADJACENT
to the SF vtable (0x00A7D458, 6 slots) in .rdata, separated by the
"ArkSceneFeeder" string literal (@0x00A7D444) and the SF COL pointer
(0x00AA12B8 @0x00A7D454). **Adjacency is NOT function sharing and NOT
inheritance evidence.** No SF slot function is shared with
ArkAudioObjectInterface; any SceneFeederObject↔ArkAudioObjectInterface
inheritance relationship is UNVERIFIED.

## 7. Standing statuses unchanged

- ARG2_ABI: **CONFIRMED** (untouched by this batch).
- ARG2_PROVENANCE: **UNVERIFIED (measured-and-bounded)** — the aggregate
  correction (25,905) strengthens the exhaustion bound; all census outcomes
  unchanged.
- ARG2_VALUE_CLASS: **UNVERIFIED (zero values identified)** — unchanged.
- ARG2_FINAL_SEMANTIC_ROLE: **UNVERIFIED** — unchanged; the corrected adjacency
  fact replaces the false structural context; no promotion.

## 8. The new lesson (recorded)

**Vtable-extent rule:** a COL-derived vtable ends at the first non-code dword;
reading past it overruns into adjacent .rdata (the FNMAP lesson's data-array
analog) — membership claims require extent-verified reads. Implemented in
`00_Control/w2c_w3_virtual_census.py` (`build_rtti_maps`): slot enumeration
terminates at the first dword outside the .text VA range
([0x00401000, 0x00401000+0x6735E5) — vsize-based, measured from the section
table); the same rule is applied in the measured adjacency disclosure.

## 9. Determinism proof (the affected generator paths, re-executed)

- `w2c_w3_virtual_census.py` (post-fix): executed TWICE; both outputs
  byte-identical between the runs (ARG2_PRODUCER_TRACE.txt:
  10AA922952A0A8AE3280EED55BBB48F928A39A44DD153FC39B442DBD6455655F both runs;
  the co-written CSV 8C58419342636ECAC492A516DCF1D7BFFA6375117195181A9A13B38E55738A23
  both runs — not applied, §5).
- `amend_r1_reverify.py`: executed TWICE; output byte-identical both runs
  (06051DC1DAA65A2FC928AAF60357665520B910165D3822CC0A29CBEEFA933B30).
- Sequence note: the reverify script ran BEFORE the registry updates so its
  immutability assert compares against the PRE-BATCH manifest rows (the frozen
  before-record). The registries were updated after (below).

## 10. Immutability asserts (re-asserted by this batch, script-computed)

- FIRSTCALL package: **7/7 pinned file hashes MATCH** (+ 3 empty dirs + no
  extra files) — re-hashed in-batch.
- LINK30: SF30_WRITER_CENSUS.csv SHA256 **MATCH**
  (71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0, compared
  against the SOURCE_IDENTITIES.json pin); SF30_WRITER_RAW.txt present and
  untouched.
- experiments/: untracked, foreign, untouched; never inventoried.
- QC_AUDIT.md: byte-identical to its pre-batch state
  (216FA97D6EF19C361BA2EC68D7EBE91A06E59C6B0710E7EEE59907ACF3CEA87A); NOT in
  MANIFEST_SHA256.csv (the QC session's intentional exclusion is preserved).
- Git: HEAD `f239eb85cd0f56ae10cee52d57833a49f225965c` at batch start AND end;
  zero staged paths; no commits; the untracked set is exactly the three expected
  directories (FIRSTCALL pkg / this package / experiments/). ZERO git mutations
  by this batch.

## 11. Registry updates (after this record's hashes above)

- `00_CONTROL/SCRIPT_SHA256.csv`: the w2c_w3_virtual_census.py row updated to
  the post-fix hash; the new `00_CONTROL/amend_r1_reverify.py` row added;
  unchanged rows preserved (casing and values byte-faithful).
- `06_REPORT/MANIFEST_SHA256.csv`: rows updated for the changed files; 3 new
  rows added (the two 00_CONTROL amendment files + the reverify raw);
  QC_AUDIT.md intentionally NOT added (per the QC session's note); no self-row.
  Its own post-batch identity is asserted in the final verification pass
  (delivery notice).

---

## 12. SECOND CORRECTION BATCH (FIX-7/FIX-8/FIX-9) — 2026-09-14

Executor: pe-reconstruction, executing the SECOND bounded correction batch
dispatched by PE-MASTER for loop `2ed038db-5d2e-4e7e-b679-2d29bf57501a`
(EU935-M1) — the adjudication of §5 of this record. MODE: STATIC-ONLY
(Entropia.exe never executed; byte reads only). ZERO git mutations (HEAD
`f239eb85cd0f56ae10cee52d57833a49f225965c` unchanged start→end; zero staged
paths; no commits; untracked set unchanged). All verification/refresh tooling
of this batch lives OUTSIDE the package (temp), so no package script changed
and `SCRIPT_SHA256.csv` is byte-identical. Canonical interpreter
`D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (Python 3.12.7),
`-B` everywhere; no `__pycache__`/`.pyc` created (asserted in-batch).

Numbering note: the dispatching instruction said "append as section 6"; the
first batch's record already occupies sections 6–11 (append-only; existing
sections untouched), so this record is section 12.

### FIX-7 — the one-row CSV regeneration (01_RAW/VIRTUAL_CALLSITE_CENSUS.csv)

- Rationale (PE-MASTER adjudicated): the frozen raw carried the proven-false
  'measured' annotation in the 0x007F1D73 row's evidence (the pre-fix 3-class
  membership list ['.?AVNiBMPReader@@', '.?AVNiBoundingVolume@@',
  '.?AVNiSGIReader@@'] — an extent artifact; only .?AVNiBoundingVolume@@ slot 1
  is extent-verified). A published raw must not carry a proven-false 'measured'
  annotation — the same principle as the ARG2_PRODUCER_TRACE regeneration (§4);
  this section records the CSV regeneration.
- VA-label resolution (honesty note): the dispatching instruction labels the
  row "VA 0x008046070" — a decimal/hex conflation of the CSV's decimal va
  column (a row with va=8046070 = candidate 0x007AC5F6 exists and is
  UNCHANGED: its NiD3DHLSLPixelShader/NiD3DPixelShader list is extent-stable,
  pre==post per AMEND_R1_PIN_REVERIFICATION.txt PIN SET 5). The instruction's
  content description (the NiBMPReader/NiSGIReader class list,
  REJECTED_NOT_SF) uniquely identifies the changed row, and the programmatic
  diff confirms it: the ONE changed line is the row va=8330611 = candidate
  0x007F1D73 (enclosing method 0x007F1D70).
- Regeneration command (the FIXED generator, executed TWICE — determinism):
  `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe -B
  w2c_w3_virtual_census.py` (workdir = this package's 00_Control; the
  generator co-writes the trace — byte-identical before/run1/run2, SHA256
  10AA922952A0A8AE3280EED55BBB48F928A39A44DD153FC39B442DBD6455655F: the trace
  raw is NOT mutated by this batch).
- Before SHA256: `7B74CB5D04E13D692207760A6DA40AD3FB3840AAB7502B457685AB2DF9EE8009`
- After SHA256: `8C58419342636ECAC492A516DCF1D7BFFA6375117195181A9A13B38E55738A23`
  — EXACTLY the hash the first batch's determinism proof predicted (§9).
- The complete diff (script-measured; line 132; the ONLY change; all other
  236 data rows + header byte-identical; reconstruction check PASS):
  - before: `8330611,P3,"007F1D73  8B 50 0C                  mov edx, dword ptr [eax + 0xc]",eax,0x007f1d71,ecx,REJECTED_NOT_SF,"receiver = `this` of enclosing method 0x007f1d70 = vtable slot function of classes ['.?AVNiBMPReader@@', '.?AVNiBoundingVolume@@', '.?AVNiSGIReader@@'] (all non-SF) (no def of ecx in window — incoming this)",,,`
  - after: `8330611,P3,"007F1D73  8B 50 0C                  mov edx, dword ptr [eax + 0xc]",eax,0x007f1d71,ecx,REJECTED_NOT_SF,"receiver = `this` of enclosing method 0x007f1d70 = vtable slot 1 of RTTI class .?AVNiBoundingVolume@@ (its this is a .?AVNiBoundingVolume@@, not an SF) (no def of ecx in window — incoming this)",,,`
  - Changed columns within the row: the evidence field ONLY (8th of 11
    columns); classification REJECTED_NOT_SF unchanged; row count 237 lines
    (header + 236) unchanged; classification distribution unchanged (211
    INSUFFICIENT_PROOF / 5 REJECTED_NOT_SF / 2 NOT_A_VTABLE_CALL + 18
    M1_FLOW rows); the census denominators (218 candidates; the method-1
    buckets 12,535 / 5,957 / 2,615 / 2,841 / 1,761 / 196 = 25,905; 18 flows;
    17 ABI-incompatible + 1 ABI-compatible) unchanged — the co-written trace
    raw is byte-identical.

### FIX-8 — the 5-class truth in the documents

The regenerated raw measures FUN_006FAB80's vtable memberships as 5
EXTENT-VERIFIED classes (read from the regenerated raw, closest-candidate
section; cross-checked against AMEND_R1_PIN_REVERIFICATION.txt PIN SET 5 —
MATCH; never hand-copied): `.?AVArkAnimationCyclic@@`,
`.?AVArkAnimationCyclicLinear@@`, `.?AVArkAnimationCyclicSin@@`,
`.?AVArkAnimationDerivatives@@`, `.?AVArkAnimationPredefined@@` (all
ArkAnimation family). The pre-fix 10-class list carried 5 vtable-boundary
overrun artifacts (.?AVArkAnimationAlpha@@, .?AVArkAnimationAnimatedTexture@@,
.?AVArkAnimationColor@@, .?AVArkModelResourceInstanceRef@@,
.?AVArkRefObject@@). Document hits fixed (each verified by grep
before/after):

| Document | Before SHA256 | After SHA256 | Hit fixed |
|---|---|---|---|
| 06_REPORT/REPORT.md | 99CDC3A8FD740CFCA1EEC481A8B092C99E1E6C6CDE6E5ED2D2383FA708C1B453 | 62D6C797F02F17F30EE2191560299AFC7C64551A3D2B58CDA8002B0776AF3598 | ARG2_PROVENANCE row: "shared slot function of 10 RTTI classes incl. the ArkAnimation family" → "shared slot function of 5 vtable-extent-verified RTTI classes — the ArkAnimation family: [the exact 5-class list]; list read from the regenerated raw, corrected per the R1 amendment 2026-09-14" |
| 02_ANALYSIS/ARG2_ANALYSIS.md | EFA11922A0247F0879B3B43280155785CE2795854B43D38B7A791BF7D19DB5B9 | B5D8EB82561A851927A5AE85E5B190519CE9A9E8B380B0E7177B23B6EC4E947D | (1) §1.2 closest-candidate paragraph: "shared vtable slot function of 10 RTTI classes (pre-fix list incl. artifact names)" → "of 5 RTTI classes (vtable-extent-verified per the R1 amendment 2026-09-14 — the list read from the regenerated raw: [the 5])"; (2) §1.2 REJECTED_NOT_SF sentence: the artifact list `.?AVNiBMPReader@@`/`.?AVNiSGIReader@@` → `.?AVNiBoundingVolume@@` only (extent-verified; the enclosing method 0x007F1D70 is vtable slot 1) — under the "same class-list wording anywhere else" clause |
| 06_REPORT/STAGE_ACCEPTANCE_GATES.csv | 1A04E6311FBFF63D2DF15AC9B3A6A3BFDD62C8661E146356BEE62CF24E971093 | 225FEB8D7743188D4D18495707F38A9A2B2D94FF27503A5657FB56C5E4A251C7 | G2 row FAILURE_CASE_DETECTED fragment: "(NiD3DPixelShader / NiBMPReader-family this-receivers)" → "(NiD3DPixelShader / NiBoundingVolume this-receivers)" — same clause (the G5 row is FIX-9, below) |

Negative findings (grep-complete; no edit needed — the §5 item-2 location
list overstated these): 06_REPORT/HANDOFF.md carries NO "10"/artifact-class
wording (its W3 line says "ArkAnimation-family shared slot function" —
count-free and family-level, TRUE under the 5-class measurement;
byte-identical, E9DB229D1155A0508CE361E5B3E0D1654C6150438C83452533FA9DB5492D7FF1);
03_EVIDENCE/EVIDENCE_INDEX.csv rows 13–14 carry no such wording (their counts
remain TRUE post-regeneration;
901D2FAB8B154CC229A67842FA18CFA4589CFA844B4B9DA204E2B0674F2278E8);
02_ANALYSIS/SCIENCE_STATUS_DELTA.csv likewise
(320D2916BC57B7E00164AD0229C1A08A5F236EA12609E24932BE72BF4221CEC0). The
forwarding-structure claim (forwards (arg1,arg2) to slot 3 of [this+0x14]) is
byte-verified and unchanged everywhere it appears.

Post-fix grep census (patterns: "10 RTTI", "10-class", "10 classes",
"10 claimed", "10 vtables", the 5 ArkAnimation artifact names, "NiBMPReader",
"NiSGIReader"): remaining hits are EXACTLY the allowed set — this record
(append-only history), 01_RAW/AMEND_R1_PIN_REVERIFICATION.txt (the
pre-fix-as-pre-fix raw record), 06_REPORT/QC_AUDIT.md (the protected
historical QC record), and the two 00_CONTROL scripts' own comment strings
(unchanged scripts). ZERO hits in any other document; the regenerated
CSV/trace raws now carry the extent-verified text only.

### FIX-9 — the G5 gate-row context (06_REPORT/STAGE_ACCEPTANCE_GATES.csv)

The G5_HYPOTHESIS_DISCIPLINE row's WHY_NON_CIRCULAR column carried the
retracted-artifact phrase "structural context (ArkAudioObjectInterface
membership; ArkAnimation forwarding family) recorded as context only".
Replaced (ONLY that fragment) with the corrected adjacency fact:

> structural context (the .?AVArkAudioObjectInterface@@ vtable @0x00A7D42C is
> ADJACENT to the SF vtable in .rdata — separated by the 'ArkSceneFeeder'
> literal and the SF COL; no function sharing — the imm32 census bound; no
> inheritance claim — UNVERIFIED; ArkAnimation forwarding family) recorded as
> context only

The G5 STATUS column is UNCHANGED: PASS. The gates CSV parses 12 rows × 6
columns (asserted in-batch). QC_AUDIT.md stays byte-identical (the historical
QC record; this record is the correction of record).

### End-of-batch asserts (all script-computed, in-batch)

- FIRSTCALL package: 7/7 pinned file hashes MATCH (+ 3 empty dirs + no extra
  files) — re-hashed at batch start AND batch end.
- experiments/: untracked, foreign, untouched; never inventoried, never
  written (zero batch operations targeted it; the untracked set is unchanged).
- 06_REPORT/QC_AUDIT.md: byte-identical
  (216FA97D6EF19C361BA2EC68D7EBE91A06E59C6B0710E7EEE59907ACF3CEA87A) —
  batch start AND end.
- 00_CONTROL/SCRIPT_SHA256.csv: byte-identical
  (C2A092CFAD5D9CF032837BB5EC99EDE33E382668AB887066190BF18C675C1C1E) — no
  script edited this batch.
- All raws other than the authorized CSV regeneration byte-identical to
  their batch-start state (full-file before/after census; the trace
  byte-identical across before/run1/run2).
- Determinism: the fixed generator executed TWICE; the CSV byte-identical
  both runs (8C58419342636ECAC492A516DCF1D7BFFA6375117195181A9A13B38E55738A23
  both runs); the trace byte-identical both runs.
- No `__pycache__`/`.pyc` anywhere in this package (the FIRSTCALL package's
  pinned pycache is pre-existing and hash-verified).
- Git: HEAD `f239eb85cd0f56ae10cee52d57833a49f225965c` at batch start AND
  end; zero staged paths; no commits; the untracked set exactly the three
  expected directories. ZERO git mutations by this batch.

### Registry updates (this section's hashes above)

- `06_REPORT/MANIFEST_SHA256.csv`: REFRESHED (after this record — regenerated
  last, family convention) for the files changed by this batch:
  00_CONTROL/AMEND_LOG_R1.md (this append), 01_RAW/VIRTUAL_CALLSITE_CENSUS.csv,
  02_ANALYSIS/ARG2_ANALYSIS.md, 06_REPORT/REPORT.md and
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv. Before SHA256:
  `6D72CDE4274ECBE632B7CAF4B18D3D830CF654224CDE3FE19A5E318AD1F8A660`.
  Row count unchanged: 32 data rows (every package file except the manifest
  itself and QC_AUDIT.md — both intentionally excluded, the same
  self-exclusion convention). All non-changed rows re-verified byte-identical
  against their pre-batch values during the refresh; the manifest's own
  post-batch identity is asserted in the final verification pass (delivery
  notice).
- `00_CONTROL/SCRIPT_SHA256.csv`: NOT touched (no script changed this batch).
