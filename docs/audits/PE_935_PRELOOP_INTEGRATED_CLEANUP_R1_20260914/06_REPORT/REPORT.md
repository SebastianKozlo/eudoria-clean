# REPORT — PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914

- RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
- RUN_CLASS: MATERIAL · RUN_TYPE: PROCESS / PERSISTENCE / REVALIDATION
- MILESTONE: EU935-M1 (no milestone action in this run) · ERA: PCG_9_3_5
- MODE: **STATIC-ONLY** — Entropia.exe was NEVER executed; all analysis = own byte reads +
  own capstone 5.0.7 disassembly (measured provenance; the 5.0.9 dist-info label is a
  KNOWN FALSE LABEL) of the pinned physical file (SHA256
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, SIZE 8015872,
  fail-closed asserted before any byte read in every probing script).
- EXECUTOR: pe-reconstruction (direct PE-MASTER dispatch; NO_NESTED_TASKS).
- PARENT LOOP: 2ed038db-5d2e-4e7e-b679-2d29bf57501a (4h auto loop; Phase 1 = this cleanup).
- BASE_SHA: a7a6c756bc35a5b28220236e9ac649131206aeb3 (observed HEAD == BASE_SHA at start
  and end; ZERO git mutations by this run).
- GIT MUTATIONS: **NONE** (read-only observations only; all outputs are new untracked
  files inside this package).
- TIMEBOX NOTE (honest): the 40-minute soft timebox was exceeded (~70 minutes of work).
  The overrun came from the W1/W2 chain depth required by the evidence (the historical
  function attributions turned out to be wrong and had to be disproven + re-discovered +
  closed over two caller levels). No work item was abandoned; every item W1-W9 completed.

## 1. E1/E2 revalidation — the load-bearing result

Both census rows were historically rejected under R-EBP-INHERITED ("fn never redefines
ebp (FPO, ebp untouched); ebp = ancestor frame pointer = stack address") — an UNSOUND
rule. This run revalidated both from physical bytes:

**The historical function attributions are DISPROVEN.** 0x007EAC00 and 0x0082DAC0 are
not function entries: bytes at both start `00 00` (a mid-stream misaligned decode), and
NEITHER VA is referenced anywhere (full-.text E8/E9/EB census = 0; whole-file imm32
census = 0; no entry fallthrough — CC/ret+CC padding precedes the REAL entries). The
"FPO, ebp untouched" premise was evaluated at non-function VAs.

**E1 (writer 0x007EB1B3, `mov dword ptr [ebp+0x30], esi`, bytes 89 75 30 — verified):**
the REAL containing function is **0x007EA740** (MSVC SEH-frame FPO; entry-closed: sole E8
caller 0x007EB284; zero indirect channels). EBP is **REDEFINED at 0x007EA76D
`mov ebp, dword ptr [esp + 0x1a0]`** = ARG3 — an argument pointer, NOT a frame pointer.
Its sole caller is the NiNode-RTTI-guarded dispatch wrapper FUN_007EB210 (virtual
GetRTTI call on esi + base-chain walk against the immediate 0x00BA7218 — the NiNode
NiRTTI — then a pass-through of the wrapper's four args). Level-2 closure over the
wrapper's three call sites (0x007C198F / 0x007EB2FF / 0x007EB410): arg3 = an ECX `this` /
an incoming stack-argument VALUE / a caller EBP register — NO case A/B/C proven.
**E1 FINAL CLASS: POSSIBLE_ALIAS (case NONE_PROVEN).** REJECTED was never proven.

**E2 (writer 0x0082DB61, `mov word ptr [ebp+0x30], cx`, bytes 66 89 4D 30 — verified):**
the REAL containing function is **0x0082DA80** (a bounds-checked u16 cursor reader:
[ebp+0x90] cursor / [ebp+0x8C] end). EBP is **REDEFINED at 0x0082DA82 `mov ebp, ecx`**
= the reader `this`. Its sole caller FUN_0082DFF0 (two entry sites, zero indirect
channels) constructs the reader IN PLACE as a **STACK LOCAL on BOTH paths** —
`lea ecx, [esp + 0x9c]`; `call 0x82d920` (constructor storing vtable 0x00A9189C) — and
passes the same slot to FUN_0082DA80. RTTI resolution of vtable 0x00A9189C → COL
0x00AB25E8 → TypeDescriptor 0x00B96D3C → **`.?AVArkNiTGAReader@@`**. The EBP value at
the writer is therefore a stack address of an object of a class distinct from
SceneFeederObject on every writer-reaching path. **E2 FINAL CLASS: REJECTED_ALIAS
(REJECTED_STANDS_SOUND; case B + class corroboration).**

## 2. Derived census recomputation (W4)

- Canonical layer before: 3643 = 2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED
  (re-derived: CSV self-count 2/618/3023 + the AMEND_R2 sidecar delta for row 0x0040525B).
- E1: REJECTED -> POSSIBLE. E2: unchanged (sound).
- **DERIVED CANONICAL LAYER: 3643 = 2 PROVEN / 620 POSSIBLE / 3021 REJECTED / 0 UNRESOLVED.**
  TOTAL == 3643 asserted. Historical CSV/RAW byte-identical before == after.
- The drafted append-only sidecar text for a future
  `SF30_WRITER_CENSUS_SUPERSESSION_R3.md` (LINK30 package) is INSIDE
  02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §5 (drafted only; the persistence worker
  applies it after adjudication).

## 3. Classifier rule V2 + mandatory tests (W3)

- Rule: 02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md; implementation:
  00_Control/ebp_alias_classifier.py (deterministic, -B).
- Negative test (SYNTHETIC_FIXTURE: unknown live-in EBP; no redefinition; write
  [ebp+0x30],reg) → **POSSIBLE_ALIAS** (REQUIRED; PASS).
- Positive control (push ebp; mov ebp,esp; mov [ebp+0x30],eax) → **REJECTED_ALIAS**
  (sound case A; PASS).
- Raw outputs: 01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt (verbatim program output).

## 4. SLOT17 audit findings (W5) — dispositions

AUD-F1 ACCEPTED (temporal-scope erratum: RUN_START vs PUBLICATION; reflog: master
3644e5ac -> a7a6c756 at 14:40:54 before the 15:11:43 branch commit; REMOTE_HEAD_CHRONOLOGY
= UNRESOLVED; branch validity unaffected — parent pin 3644e5ac verified). AUD-F2 ACCEPTED
(commit-tree census: 03_EVIDENCE=16, 06_REPORT=4; TOTAL 35 stands). AUD-F3
PARTIALLY_ACCEPTED (5 control/locator files carried <14:31:34; all evidence/raw/analysis
files >=14:39:07; REPORT line overstates; mtime = corroboration only — content correctness
stands on the completing session's re-measurements; no science downgrade). AUD-F4
REJECTED_WITH_EVIDENCE (standard IMAGE_OPTIONAL_HEADER32 layout confirmed: ImageBase @
opt+0x1C = 0x00400000; the "+4 shifted" docstring claim is wrong; standard wording
mandatory for future scripts). AUD-F5 REJECTED_WITH_EVIDENCE (Gb112_eval = Documentation
only; the NiMain.lib used = the installed Evaluation SDK path, pins re-verified: SIZE
3073590, SHA256 FF4519AF...6597). AUD-F6 ACCEPTED (corrected temporal scoping recorded;
no verbatim chat reconstruction). AUD-F7 ACCEPTED (same temporal-scope erratum as F1).
Full document: 02_ANALYSIS/SLOT17_AUDIT_FINDINGS_DISPOSITION.md.

## 5. GB12 vtable erratum + NiRTTI precision (W6)

- Raw JSON re-verified: GB12 NiNode slots 13=GetGroup, 14=SetGroup, 15=UpdateControllers,
  16=UpdateNodeBound, 17=ApplyTransform, 18=GetObjectByName, 19=SetSelectiveUpdateFlags.
  The prose-table rows 13-16 (NiAVObject/NiNode columns) duplicate UpdateControllers at
  13 AND 15 and UpdateNodeBound at 14 AND 16 — erratum recorded; headline results
  (17/18/19) CORRECT and unchanged.
- NiRTTI three-part statement: 0x00BA7218 = NiNode NiRTTI CONFIRMED; base pointer VALUE
  0x00BA7270 CONFIRMED; **semantic identity 0x00BA7270 = NiAVObject NiRTTI CONFIRMED —
  UPGRADED from STRONGLY_SUPPORTED** by the bounded probe (single whole-file hit of
  `B9 70 72 BA 00` at 0x00A6C33A; the initializer thunk at 0x00A6C330 pushes the
  'NiAVObject' literal 0x00A8D8BC and base 0x00BA7224, sets ecx=0x00BA7270, calls the
  same NiRTTI ctor 0x007199E0; bound respected: one pattern + one context window).
  Corroboration: 0x00BA7218 also appears as the NiNode-kind comparison immediate in the
  E1 dispatch wrapper (`cmp eax, 0xba7218` @0x007EB260).
- Document: 02_ANALYSIS/SLOT17_ERRATA.md; raw: 01_RAW/NIRTTI_BOUNDED_PROBE_0xBA7270.txt.

## 6. F5 disposition (W7)

**F5_PROCESS_STATUS = PARKED_UNAUTHORIZED_ATTEMPT** (human OPTION C): the FIRSTCALL run
started before the authorization gate; the violation history stands; the package is never
completed, never retro-authorized, never deleted, its science never adopted, never
published; it stays untracked on disk untouched (7/7 hashes unchanged, re-verified
before == after; 3 empty dirs verified). Supersession QC comparison (FIRSTCALL facts vs
SLOT17's independent re-measurements): **6/6 consistent, 6/6 strictly subsumed** →
**F5_SCIENCE_STATUS = SUPERSEDED_SCIENTIFICALLY_BY
PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914 (commit
5290e79e0dc469c70605f35c125d7b727f9f7a6b).** Document: 02_ANALYSIS/F5_DISPOSITION.md.

## 7. Science status matrix (W8)

All 15 standing statuses preserved (no invention, no downgrade; identity
STRONGLY_SUPPORTED NOT raised — the locked B->A criterion held). Changed/new rows: E1
(POSSIBLE_ALIAS), E2 (REJECTED sound), 0x00BA7270 semantic identity (CONFIRMED via the
bounded probe), 0x00BA7218 second-static-use corroboration row, canonical counts
(2/620/3021/0). Document: 02_ANALYSIS/SCIENCE_STATUS_MATRIX.csv.

## 8. Gates

G0-G12 self-assessed **PASS** (G0-G11 all PASS; G8 both tests returned the REQUIRED
classes). G13 in-scope part (package-internal consistency + R3 sidecar draft consistency)
PASS; the cherry-pick/commits/push are explicitly post-adjudication. G14 (fresh QC) and
G15 (persistence) are **PENDING** — closed by others. Matrix:
06_REPORT/STAGE_ACCEPTANCE_GATES.csv.

## 9. Findings (honest register)

- **P2 FINDING (science-material)**: the historical LINK30 function-attribution layer
  produced WRONG function boundaries for at least the E1/E2 rows (non-function VAs with
  zero references). E1/E2 are now corrected, but the SAME attribution method may have
  mislabeled other rows' function_va values (classes derived from in-function EBP/ESP
  analysis at wrong entries would be unreliable). Scope of exposure UNKNOWN from this
  run; a future census-wide attribution re-derivation is RECOMMENDED (proposed for
  PE-MASTER adjudication, not executed here).
- **P3 FINDING (timebox)**: soft timebox exceeded (~70 min; honest disclosure in §0).
- **P3 FINDING (provenance)**: 01_RAW/IDENTITY_VERIFICATION_AT_START.txt was generated by
  an earlier revision of the verification script (SHA 83B392E3... recorded in that file);
  the END record used the current revision (1E28AF12...). Measurements identical
  (disclosed in 03_EVIDENCE/README.md).
- **AUD-F4/F5 confirmations** are corrections of SLOT17-package-adjacent documentation,
  not science defects (the SLOT17 science itself stands).

## 10. Cleanup-level outcome

**PRELOOP_CLEANUP_PROPOSAL_READY** — all self-assessed gates G0-G12 PASS with consistent
evidence; the derived canonical counts (2/620/3021/0, TOTAL 3643) and the drafted R3
sidecar are ready for PE-MASTER adjudication. The SLOT17 package can be integrated
verbatim via the future cherry-pick of 5290e79 (persistence worker, after adjudication).

## 11. PENDING (closed by others — placeholders)

- FRESH_QC_VERDICT = QC_PASS_WITH_FINDINGS (G14; 06_REPORT/QC_AUDIT.md)
- PE_MASTER_VERDICT = MASTER_ACCEPTED (advisory; PRELOOP_CLEANUP_STATUS = ACCEPTED;
  06_REPORT/PE_MASTER_REVIEW.md)
- PERSISTENCE_STATUS = EXECUTED (G15; commits + push recorded in
  00_CONTROL/PERSISTENCE_COMPLETION_LOG.md and the repo git history)
