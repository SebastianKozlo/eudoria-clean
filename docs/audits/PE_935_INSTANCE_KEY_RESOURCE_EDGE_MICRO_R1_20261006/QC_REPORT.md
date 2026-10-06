# QC_REPORT — PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006

**QC scope:** SELF_CHECK (targeted, run-local; performed by the executor that produced
the evidence — NOT an independent QC; external Desktop post-audit NOT_PERFORMED and
NOT_CHECKED). Internal review origin: none beyond this SELF_CHECK (no fresh-context
internal QC was run this phase; PE-MASTER review is a later separate step).

**QC time window:** 2026-10-06 00:04–00:20 local. Instrument: 03_SCRIPTS/qc_controls.py
(run-local; SHA256 recorded in the manifest). All gates re-derive from the pinned EXE.

---

## Q1 — Identity and baseline (PASS)

- EXE re-read at QC time: size 8,015,872 B (match); SHA256
  `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (match).
- PE spot checks (own walk): image_base 0x00400000, ASLR OFF, .text RVA 0x1000 — all match.
- BASE: LOCAL_HEAD == origin/master == actual remote master == 3921dbe2a43a9181f8a50fa5242d8586c85896b6
  (ls-remote 2026-10-05 23:53:49, exit 0); no relevant tracked changes; foreign untracked
  paths untouched (5× PE_935_* packages + experiments/).
- OUTPUT_ROOT did not exist before the run (preflight Test-Path = False).
- Getter boundary re-read: bytes `8B 41 74 C3` @0x00414130; RET = C3; after-RET padding
  `CC`×8+ confirmed (function boundary).

## Q2 — Census recount (PASS)

- Independent re-enumeration inside the QC script: **6** E8 hits in .text targeting
  0x00414130 == the census artifact's 6 (0x004569D3, 0x00456BEB, 0x0045723E,
  0x0045A08B, 0x00528FD9, 0x008561AC).
- 0 E8-pattern hits outside .text; 0 E9 JMP-thunks; 0 absolute dwords of 0x00414130.
- Independent tool cross-check: Ghidra 11.2.1 `getReferencesTo(0x00414130)` = exactly
  6 references, all UNCONDITIONAL_CALL, all 6 candidates PROVEN_EXACT instruction
  starts (GHIDRA_VERIFY.json). No divergence between own census and Ghidra.
- NOT covered (disclosed): indirect calls (call reg / call [mem]), inlined reads of
  [x+0x74], alias forms other than E9 — NOT claimed enumerated.

## Q3 — Control (a) MANDATORY: getter offset +0x74 → +0x78 without changing the EXE (PASS)

- MEASURED_QUANTITY: the EXE bytes at VA 0x00414130.
- INDEPENDENT_SOURCE_OF_TRUTH: the physical EXE file re-read by the gate.
- Clean run: byte-pin `8B 41 74 C3` PASS + semantic decode `mov eax,[ecx+0x74]; ret` PASS.
- Mutated expectation (+0x78, EXE untouched): byte-pin **FAIL** (physical byte is 0x74)
  + semantic decode **FAIL** ("disp8 mismatch: claimed 0x78, physical 0x74").
- WHY_NON_CIRCULAR: the mutation changes only the expectation, never the file; the
  gate must compare an independent expectation against physical bytes.
- FAILURE_CASE_DETECTED: if the physical byte at 0x00414132 were 0x78 (or the pin wrong),
  the CLEAN gate would already FAIL — the clean gate is falsifiable.
- Coverage limit: the 4-byte getter pin only; not every consumer instruction.
- VERDICT: clean PASS → mutated FAIL = **PASS** (QC_CONTROLS.json CTRL_A).

## Q4 — Control (b): receiver/identity edge removal (PASS)

- The selected receiver-proven claim ("ECX at 0x00528FD9 == the ClientMovableObject
  ctor this") depends on four byte-pinned identity edges: E1 `8B F1` @0x00528E76
  (MOV ESI,ECX), E2 `C7 06 B0 DC A7 00` @0x00528EA2 (CMO vtable store; RTTI
  `.?AVClientMovableObject@@` calibration PASS), E3 `8B CE` @0x00528FD2
  (MOV ECX,ESI), E4 `E8 52 B1 EE FF` @0x00528FD9 (the call).
- Clean run: all four edges hold → receiver gate PASS.
- Mutated copy (E3 removed: `8B CE`→`8B CD` in-memory, EXE untouched): the gate
  **FAILS** — the essential receiver edge is demonstrably load-bearing.
- VERDICT: clean PASS → mutated FAIL = **PASS** (CTRL_B).

## Q5 — Control (c): resource-join negative on the real examined key-to-map operation (PASS)

- The REAL examined key-to-map operation: FUN_00856190 (mgr1 hash_map insert), body
  0x00856190..0x00856210.
- Map-destination pins: `8D 73 10` @0x008561B8 (map = this+0x10) and
  `89 7C 24 14` @0x008561C1 (pair value = the instance) — both hold.
- Resource-family E8 census inside the decoded insert body: **ZERO** calls to
  FUN_0072F580 (template lookup) / FUN_006C9700 (model pump) / FUN_006CB6F0
  (instance creator) / FUN_006CB020 (named-instance builder) / FUN_0043A550
  (registry getter). The key-to-map join is an IDENTITY join (instance-key → the
  same instance object; duplicate → deleting dtor), byte-distinct from the
  templates.vfs RB-tree registry (root 0x00BA1824).
- Falsifier: a fake `E8 → FUN_0072F580` injected into an in-memory copy of the body
  at 0x0085620B is DETECTED (1 found) — the detector demonstrably FAILs on a real
  resource join. Clean PASS → falsifier-detected = **PASS** (CTRL_C).

## Q6 — RTTI walker discipline (PASS)

- Calibration FIRST, fail-closed: vtable 0x00A7D458 → `.?AVSceneFeederObject@@`,
  0x00A7DCB0 → `.?AVClientMovableObject@@`, 0x00A91E4C → `.?AVMovableObject@@` —
  all three BASE-canon names reproduced (3/3) before any new probe was trusted.
- New probes (post-calibration): 0x00A79F18 → `.?AVGameClient@@` (the 0x88-B
  singleton at [0x00B9FE5C]); 0x00A83274 → `.?AVSceneFeederObjectExtraData@@`
  (the 0x14-B key-carrying object); 0x00A7D444 → NOT-A-CLASS-VTABLE (TD
  0xCCCCCCCC = padding) — the honest negative recorded.

## Q7 — Budget discipline (PASS WITH ONE DISCLOSED DEVIATION)

- TOTAL_DETAILED_FUNCTIONS_MAX = 6. Counted budgeted detailed functions:
  FUN_00414130, FUN_00528E50 (selected caller), FUN_005247C0 (edge 1),
  FUN_00509330 (edge 2), FUN_00856190, FUN_00401360 (receiver classification).
- **Disclosed deviation:** a "head probe" of FUN_0064B1E0 (0x30 bytes dumped as an
  identity probe at the budget boundary) covered the function's ENTIRE 27-byte body
  (0x0064B1E0..0x0064B1FA) — i.e., a 7th function's semantics were extracted
  (key→[obj+0x10], vtable 0x00A83274 → SceneFeederObjectExtraData, RET 4). This
  exceeded the 6-function budget. DISPOSITION: disclosed as an over-budget probe;
  recorded in FUNCTION_LEDGER.csv row 7 as DISCLOSED_OVER_BUDGET_PROBE; its content
  is a NON-CANONICAL LEAD and is NOT load-bearing for the outcome; NO further
  analysis was performed after recognition; the outcome (BOUND_REACHED) does not
  depend on the probe. The complementary bounded probe of FUN_004157B0 (0x30-byte
  head; vtable read only, for the GameClient receiver classification) is disclosed
  in row 8 as BOUNDED_CLASSIFICATION_PROBE.
- Two further call edges were respected on the selected branch (FUN_005247C0,
  FUN_00509330); the third edge (FUN_0064B1E0) was recorded as the budget-boundary
  stop; no fourth shortlisted site, no second deep branch, no function #8 analysis.

## Q8 — Honest-negative and coverage disclosures

- NOT_CHECKED (explicit): consumers of SceneFeederObjectExtraData+0x10; FUN_007C8780
  (the ExtraData base ctor); FUN_007B6A80 registration semantics; FUN_004A9850
  (GameClient-branch consumer); FUN_00853D00 (the mgr1-family query at the
  UNRESOLVED shortlisted site 3); FUN_009789C0 (the param-set pair check); the
  FUN_00456770/FUN_00456a10/FUN_00456f40/FUN_00459fd0 containing-function bodies;
  any indirect/virtual/inlined reader of any +0x74 anywhere; every runtime behavior
  (STATIC-ONLY — the client never ran).
- WORLD_XYZ_RECOVERED = NO; STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED;
  HISTORICAL_INSTANCE_DATA_RECOVERED = NO.
- Persistence phase (per the human dispatch): commit/push NOT performed by this run;
  AUDIT_ENTRYPOINT.md NOT edited (the proposed row is in HANDOFF.md; the manifest was
  computed WITHOUT the entrypoint row — final regeneration including the entrypoint
  belongs to the persistence phase).

## Q9 — Overall verdict

**QC_PASS** (Q1–Q6, Q8 PASS; Q7 PASS WITH ONE DISCLOSED DEVIATION — the FUN_0064B1E0
over-budget probe, disclosed, non-load-bearing; no default-success fallback: every
verdict was derived from the on-disk evidence of this package).

---

## RECORD-REPAIR (post-internal-QC; executed 2026-10-06 ~00:55–01:05 local)

**Origin:** the independent internal QC run
PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_QC_INTERNAL_R1_20261006 (fresh-context
pe-master-auditor worker; verdict **QC_PASS_WITH_FINDINGS**; report:
00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md, READ-ONLY for the repair) found
F1/F2 (P1, pre-persistence repair required) and F3–F6 (P3) plus F7/O1 (observations).
PE-MASTER dispatched this record-repair continuation of THIS run to apply F1–F6.
F7 (predicted-vs-executed FAILURE_CASE) and O1 (ArkSceneFeeder string context)
require no action per the QC. NO scientific result was changed by the repair:
OUTCOME = `BOUND_REACHED` unchanged, all PASS records, the budget/hops/shortlist
accounting, the census, the RTTI identities and every load-bearing byte claim are
exactly as verified by the internal QC. This is a routine evidence-persistence /
display-precision repair per contract §5, not new science.

Applied repairs (all pinned to the CURRENT post-repair bytes; the repair touched
nothing in 00_CONTROL_INTERNAL_QC and no file outside this package):

- **F1 (P1)** — GOVERNANCE_DECISION.md: an undisclosed +25 B edit of the file between
  the KROK-0 measurement (6,299 B / A9531075... @23:54:05.874, measured 23:54:08.342)
  and 23:54:12 (6,324 B / 96B80022...), still before science (23:56:13), is now
  DISCLOSED in an append-only "AMENDMENT 1" section (both states pinned with
  size/SHA/time; cause not determinable — stated honestly; VERBATIM-block/contract
  consistency re-verified by this repair run: contract re-hashed 11,823 B /
  57A731683EE32E6FC43CCEC42664B03D4DC7FBA2138009B8BF7A0A8E634BABB6 — MATCH; no
  byte-identity claim against the KROK-0 state; GovernanceWriteTime.txt left
  unaltered — it is a single-record measurement, not a log). Append-only PROVEN:
  the first 6,324 B of the amended file hash to
  96B80022C5819AE0781B978053CB076C12B918C9E377D4CDB8569BBADD808E3A == the QC-pinned State B. Post-repair (State C):
  10,155 B / 0E135D427C05C326C02AD7DC36CB2326F1B1272A2741231BAEFBC9826FEF9F96.
- **F2 (P1)** — the three cited own-byte windows are NOW PERSISTED:
  03_SCRIPTS/byte_windows.py WINDOWS extended with SF_ctor_tail (0x00509470, 0x50),
  F0064B1E0_head (0x0064B1E0, 0x30), F004157B0_head (0x004157B0, 0x30);
  01_RAW/BYTE_WINDOWS.txt regenerated from the pinned EXE (EXE identity re-verified
  before the read: 8,015,872 B /
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH). Regeneration is APPEND-ONLY: the previous 5,474-B content
  is a byte-prefix of the new file (verified); the first 7 windows are unchanged.
  The 3 new windows are byte-identical to the internal QC's independent M6 dumps
  (3/3 region equality, different engine), and every ledger byte-content claim they
  back was re-verified TRUE from the EXE: E8 @0x0050948B → 0x0064B1E0 (recomputed
  MATCH), E8 @0x005094A2 → 0x007B6A80 (MATCH), E8 @0x0064B1E3 → 0x007C8780 (MATCH),
  8B 55 14/52/8B C8 @0x00509485..89, 8B 4D 30/50/68 44 D4 A7 00 @0x00509494..9C,
  89 46 10 @0x0064B1EC, C7 06 74 32 A8 00 @0x0064B1EF, C7 06 18 9F A7 00
  @0x004157B8. New: BYTE_WINDOWS.txt 6,514 B /
  CB94BA0F3A227B8C192BD51F2174D1E0ED0A3E30E2F8AB1A38EC1832429CA361; byte_windows.py 1,850 B /
  8230A96BE57C44E00B984612435691D38FDB9CB03F802E747F04EA814EB508D6. EVIDENCE_INDEX.md artifact description
  corrected accordingly (the superseded "boundary probe" wording is gone).
- **F3 (P3)** — 03_SCRIPTS/qc_controls.py: the CTRL_C falsifier-site comment no
  longer claims a "padding-safe" overwrite that "keeps the body intact"; it now
  states the truth: the injection at fake_at = len(body)-5 → VA 0x0085620B
  OVERWRITES the live epilogue bytes 83 C4 10 C2 04 (ADD ESP,0x10; RET 4) of the
  in-memory copy (copy exists solely to exercise the detector; EXE untouched).
  Gate logic and all QC output texts unchanged. New: 13,010 B /
  94D79BF946BD0EF4F34F911113BC5F46AC2AE26728CFB8808BA300EB72D873BF.
- **F4 (P3)** — EDGE_LEDGER E-GB2: RTTI name transcription corrected
  `.?AVGameClient@` → `.?AVGameClient@@` (matches RTTI_PROBES.json and the QC's
  own walk). New: 10,087 B /
  53EDDB73127C59728084565AEA24A6B49175CB82D5BF32071740C6262DBC42E7.
- **F5 (P3)** — FINAL_REPORT §1.2 wording precision: "ZERO calls to the resource
  family" → "ZERO DIRECT (E8) calls to the resource family" (the CTRL_C predicate
  is the direct-E8 target census; the body's indirect FF D2 dtor dispatch is outside
  it and the pair-build bytes prove its target is the value's own vtable slot 0).
  New: 14,656 B / 294C8CC244A1B68CA993E995B7A10E4998D0CCC97C60F376F2D132D2A203FD83.
- **F6 (P3)** — FUNCTION_LEDGER row 4: the RET 0xC citation now names the
  instruction START VA (C2 0C 00 @0x005094BC; 0x005094BE is its last byte — the
  extent 0x00509330..0x005094BE stays, consistent as an inclusive end). New:
  8,431 B / 4F78D05828E1B63D320B1125597020F4AB4B3D053FBDD2653CBE08864EAE32B2.
- EVIDENCE_INDEX.md (part of F2): 5,157 B /
  F75E485CFDC7EE4AF2FBA2463B16BDDAB187AEE2E397CF02057EAAD05A772910. This QC_REPORT.md record-repair section is the only
  other edit; its own post-repair hash cannot be self-pinned and is left to the
  persistence phase's manifest (regenerated LAST).

**New observations recorded during the F2 verification (NOT repaired — outside the
dispatched F1–F6 set; PE-MASTER adjudication required; none falsifies a
load-bearing claim):**

- EDGE_LEDGER E-GB2 INSTRUCTION_VA `0x004157B7` is off by one: the physical
  `C7 06 18 9F A7 00` store starts at **0x004157B8** (0x004157B7 = `50` PUSH EAX);
  byte-verified from the EXE twice (own reader + PowerShell/.NET re-read). The
  internal QC's M6 narrative repeats the same VA (inside the read-only
  00_CONTROL_INTERNAL_QC). Same defect class as F6, not covered by the dispatched
  findings.
- FUNCTION_LEDGER row 7 says the FUN_0064B1E0 body is "26 B"; physically it is
  **27 B** (0x0064B1E0..0x0064B1FA inclusive; RET 4 = C2 04 00 at 0x0064B1F8..FA;
  CC padding from 0x0064B1FB; the extent END itself is correct-inclusive). The same
  "26-byte body" wording appears in FINAL_REPORT §5 and in this report's Q7, and in
  the QC's M6 narrative/§2 row 11 (read-only). The probe's content claims (vtable
  0x00A83274, key→[obj+0x10], RET 4) are TRUE as verified; the miscount is a display
  defect only.

**Persistence state after the repair:** COMMITTED_PACKAGE_MANIFEST_SHA256.csv was
NOT regenerated (per the two-phase flow the persistence phase regenerates the
manifest LAST with the full scope: every physical file under this package minus
the manifest, including 00_CONTROL_INTERNAL_QC and the future AUDIT_ENTRYPOINT.md
row / PE_MASTER_REVIEW.md, per the 3921dbe precedent). Until then the manifest's
pins for the 9 files listed above are stale by design; the pins in this section are
the current truth. No commit/push was performed; HEAD == BASE
3921dbe2a43a9181f8a50fa5242d8586c85896b6; foreign untracked paths untouched.

---
## RECORD-REPAIR ROUND 2 (two residual P3 observations; executed 2026-10-06 ~01:24-01:28 local)

**Origin:** the two P3-class observations recorded under "New observations recorded
during the F2 verification" in the round-1 section above (found by this executor
during the round-1 repair; left for PE-MASTER adjudication). **PE-MASTER adjudication:
CORRECT for both** (same defect class as the already-repaired F6 — publishing a
residual of the same class would be inconsistent) -> dispatched as this FINAL
micro-repair. NO scientific result changed: OUTCOME = `BOUND_REACHED` unchanged; all
PASS records, the census, the RTTI identities, the budget accounting and every
load-bearing byte claim are exactly as previously verified. Display-precision repair
only; nothing outside the four authorized files (EDGE_LEDGER.csv, FUNCTION_LEDGER.csv,
FINAL_REPORT.md, QC_REPORT.md) was touched.

Pre-write re-verification (fresh reads from the pinned EXE
`D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`; identity re-verified BEFORE the
reads: 8,015,872 B / SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH; read via
this package's own 03_SCRIPTS/pe935k_core.py, fail-closed ALL_PASS before any write):

- **R2-1 (EDGE_LEDGER E-GB2 INSTRUCTION_VA):** physical byte @0x004157B7 = `50`
  (PUSH EAX); the store `C7 06 18 9F A7 00` (MOV dword [ESI], 0x00A79F18) starts at
  0x004157B8 -> INSTRUCTION_VA corrected 0x004157B7 -> 0x004157B8. E-GB2 is NOT
  quoted in FINAL_REPORT.md (package grep: the defective VA occurs only in this
  ledger row and in the read-only 00_CONTROL_INTERNAL_QC materials) -> no
  FINAL_REPORT edit for R2-1.
- **R2-2 (FUN_0064B1E0 body size):** body 0x0064B1E0..0x0064B1FA inclusive = 27 B
  (`56 8B F1 E8 98 D5 17 00 8B 44 24 08 89 46 10 C7 06 74 32 A8 00 8B C6 5E C2 04 00`;
  RET 4 = `C2 04 00` @0x0064B1F8..FA; CC padding 0x0064B1FB..FF — the next function
  starts at 0x0064B200; CALL @0x0064B1E3 -> 0x007C8780 recomputed MATCH). The extent
  END was already correct-inclusive; only the size label 26 -> 27, fixed at every
  place the four authorized files state it: FUNCTION_LEDGER row 7 (both "(26 B; RET
  4)" and "ENTIRE 26-byte function"), FINAL_REPORT s5 ("entire 26-byte body"), this
  report's Q7 ("ENTIRE 26-byte body") — plus, as occurrences of the SAME adjudicated
  fact inside the same authorized files (leaving them would republish a same-class
  self-contradiction inside the very files being repaired): FINAL_REPORT s6 ("26-B
  body fully read") and EDGE_LEDGER E-E2-EXTRADATA ("disclosed 26-byte probe", a
  cross-reference to FUNCTION_LEDGER row 7).

Applied edits (byte-precise binary replacements via Python — no PowerShell
transcoding; every pattern verified unique pre-edit; UTF-8 no-BOM and LF line
endings preserved; post-edit files re-read, re-verified and re-hashed):

- EDGE_LEDGER.csv (R2-1 + the E-E2-EXTRADATA cross-reference): 10087 B / SHA256 B8376E36B4295CB520D92D7E96C96D9968BB816C0B0039E966D2FFD484A4EA19.
- FUNCTION_LEDGER.csv (row 7 size label + "ENTIRE 26-byte function"): 8431 B / SHA256 870522063FAD9ECFFF20DCD8C210E64B6639F0D16EF524990EA92CB7FB585434.
- FINAL_REPORT.md (s5 + s6): 14656 B / SHA256 39DA4D869400D43F3675280EA38B6314618EAD10F3FD1DB1E839DE5989BEEA7A.
- QC_REPORT.md (Q7 + this entry; pre-round-2 baseline 14,978 B /
  C8B6AE322C1C1F99C5C6358BD5716FAF9A906C9B6D1349F80B9F6DCAEDB4503E; its own
  post-repair hash cannot be self-pinned — left to the persistence phase's manifest,
  per the round-1 convention).

Known same-class residuals OUTSIDE the authorized 4-file set (left untouched, flagged
for PE-MASTER): HANDOFF.md "26-B body" (line 36) and "disclosed over-budget 26-byte
probe" (line 85) — HANDOFF.md is not in the authorized set; the read-only
00_CONTROL_INTERNAL_QC materials (QC_REPORT_INTERNAL.md s2 rows 11/12 + M6 narrative;
QC_MEASUREMENTS.txt lines 119/120/127) repeat both the 26-B claim and the 0x004157B7
VA — read-only by contract. No other package file states either defective claim
(package-wide grep). Post-repair full-package UTF-8 scan: 35/35 files decode as
strict UTF-8 — zero mojibake; the package's single UTF-8 BOM sits on the
untouched 01_RAW/GovernanceWriteTime.txt (223 B, current SHA256 == its
original-run manifest pin E24D2BDC... — pre-existing state, not written by any
repair round). One transient artifact was created AND removed by this round's own
verification tooling: 03_SCRIPTS/__pycache__/pe935k_core.cpython-312.pyc (Python
bytecode cache from importing the run's own core for the re-verification reads);
detected by the post-repair scan and DELETED, restoring 03_SCRIPTS to exactly
its 8 manifest-pinned .py files. Manifest cross-check: every other pinned file
is byte-identical to the original-run manifest; the only pinned files differing
are the 9 by-design stale ones (round-1-only edits: 01_RAW/BYTE_WINDOWS.txt, 03_SCRIPTS/byte_windows.py, 03_SCRIPTS/qc_controls.py, EVIDENCE_INDEX.md, GOVERNANCE_DECISION.md;
EDGE_LEDGER.csv, FUNCTION_LEDGER.csv, FINAL_REPORT.md, QC_REPORT.md edited by
round 1 AND this round); 00_CONTROL_INTERNAL_QC/* was never pinned (added by the
internal QC phase after the manifest was generated). No package file outside the
four authorized files differs from its pre-round-2 state.

Persistence state after round 2: COMMITTED_PACKAGE_MANIFEST_SHA256.csv still NOT
regenerated (the persistence phase regenerates it LAST; the round-1 pins for the
three files edited here are superseded by the pins above). No commit/push performed;
HEAD == BASE 3921dbe2a43a9181f8a50fa5242d8586c85896b6; the package remains
untracked; foreign untracked paths untouched.
