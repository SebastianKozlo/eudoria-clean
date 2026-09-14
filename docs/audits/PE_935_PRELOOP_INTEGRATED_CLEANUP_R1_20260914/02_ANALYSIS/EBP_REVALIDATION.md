# EBP REVALIDATION (E1/E2) — PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914

This is the §24 structure-completion document, written at persistence time by pe-master-auditor by CONSOLIDATING the executor's verified evidence. It introduces NO new science and NO new claims; the authoritative analysis records are 02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md, 02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md, 01_RAW/E1_* , 01_RAW/E2_* (all independently re-verified by the G14 fresh QC and by PE-MASTER byte-level spot checks).

RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 · Era: PCG_9_3_5 · MODE: STATIC-ONLY
(Entropia.exe was NEVER executed; every fact below derives from own byte reads + own capstone
5.0.7 disassembly of the pinned physical file, SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, SIZE 8015872, fail-closed
asserted before any byte read.)

---

## 1. The superseded rule (R-EBP-INHERITED) — statement and why it fell

The historical LINK30 census rejected writers of the form `[ebp+0x30], reg` when the
"containing function" appeared never to redefine EBP, under the rule (verbatim):

> `fn never redefines ebp (FPO, ebp untouched); ebp = ancestor frame pointer = stack address`

The rule is UNSOUND AS A RULE (02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md §1): EBP is a
callee-saved register; a function that does not redefine EBP has NO knowledge of its value
("untouched" means UNKNOWN LIVE-IN, not "stack address"), and EBP may carry arbitrary caller
state (a this/object pointer, a global, a spilled argument). The rule was replaced by
CLASSIFIER RULE V2 (02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md §2; implementation
00_CONTROL/ebp_alias_classifier.py; test evidence 01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt;
gate G8 in 06_REPORT/STAGE_ACCEPTANCE_GATES.csv): UNKNOWN LIVE-IN EBP is NEVER a structural
REJECTED solely because EBP is untouched — default POSSIBLE_ALIAS unless an explicit case
A (frame construction) / B (explicit stack derivation) / C (bounded entry/caller provenance)
is proven. The mandatory negative test (SYNTHETIC_FIXTURE: unknown live-in EBP, no EBP
redefinition, write `[ebp+0x30],reg`) returned POSSIBLE_ALIAS (PASS) and the positive
control (`push ebp; mov ebp,esp; mov [ebp+0x30],eax`) returned REJECTED_ALIAS (PASS), G8.

Additionally, BOTH rows historically rejected under that rule had WRONG historical function
attributions (the revalidation disproved the attributed function entries themselves) — the
factual premise was evaluated at non-function VAs (§2, §3 below; the attribution-defect
mechanism is byte-proven in 06_REPORT/QC_AUDIT.md §5: operand/disp `0x90`/`0xCC` bytes
misread as entry padding, e.g. the `0x90` @0x007EABFF of `fld [esp+0x90]` and the `0x90`
@0x0082DABF of `add [ebp+0x90],esi`).

## 2. E1 — writer row 0x007EB1B3: REJECTED_ALIAS -> POSSIBLE_ALIAS (case NONE_PROVEN)

CSV row 2385 (verbatim from
docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/02_ANALYSIS/SF30_WRITER_CENSUS.csv,
READ-ONLY, byte-identity asserted before == after this run):
`0x007EB1B3,0x007EAC00,"mov dword ptr [ebp + 0x30], esi",esi,caller stack (inherited ebp),REJECTED_ALIAS`

- Writer verified: `mov dword ptr [ebp+0x30], esi`, bytes `89 75 30` @0x007EB1B3
  (01_RAW/E1_FUN_007EAC00_DISASM.txt; QC byte-read 06_REPORT/QC_AUDIT.md §2).
- Historical function attribution 0x007EAC00 DISPROVEN: the bytes at the claimed entry lead
  `00 00` (a mid-stream misaligned decode), and the VA has ZERO references — full-.text
  E8/E9/EB census = 0 and whole-file imm32 census = 0; no entry fallthrough
  (01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt; QC raw-scan ref census reproduced: E8=0, E9=0,
  EB=0, imm32=0).
- The REAL containing function is 0x007EA740: MSVC SEH-frame FPO, CC-padded entry boundary,
  entry-closed — sole E8 caller 0x007EB284, zero indirect channels (E9/EB/imm32 = 0)
  (01_RAW/E1_FUN_007EAC00_DISASM.txt; 01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt; QC E8/E9/EB/
  imm32 censuses reproduced, 06_REPORT/QC_AUDIT.md §2).
- EBP is REDEFINED inside the real function @0x007EA76D: `mov ebp, dword ptr [esp+0x1a0]`
  (bytes `8B AC 24 A0 01 00 00`) = ARG3 — an argument pointer, NOT a frame pointer (the
  QC independently re-derived the ARG3 arithmetic: 8 pushes + `sub esp,0x174` ⇒
  [esp+0x1a0] = [entry_esp+0x0C] = ARG3; exactly ONE EBP-writing instruction entry→writer).
- The sole caller of 0x007EA740 is E8 call site 0x007EB284 inside the NiNode-RTTI-guarded
  dispatch wrapper FUN_007EB210 (virtual GetRTTI call + base-chain walk against the
  immediate 0x00BA7218 — the NiNode NiRTTI — then a pass-through of the wrapper's four
  args). Level-2 closure over the wrapper's three call sites (0x007C198F / 0x007EB2FF /
  0x007EB410; QC-verified complete: exactly 3 E8, zero indirect): arg3 = an ECX `this`
  pointer / an incoming stack-argument VALUE / a caller EBP register respectively.
- CASE PROVEN: **NONE_PROVEN** (within the declared two-level bound) -> **E1 FINAL CLASS:
  POSSIBLE_ALIAS.** This does NOT assert the write IS SF+0x30; it asserts the historical
  REJECTED was never proven (02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §2 row E1;
  02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md §2; QC judgment 06_REPORT/QC_AUDIT.md §2:
  "POSSIBLE_ALIAS is CORRECT"; PE-MASTER CONFIRMED — 06_REPORT/PE_MASTER_REVIEW.md
  CLAIM_MATRIX (1)).

## 3. E2 — writer row 0x0082DB61: REJECTED_STANDS_SOUND (case B + class corroboration)

CSV row 2577 (verbatim from the READ-ONLY historical CSV):
`0x0082DB61,0x0082DAC0,"mov word ptr [ebp + 0x30], cx",cx,caller stack (inherited ebp),REJECTED_ALIAS`

- Writer verified: `mov word ptr [ebp+0x30], cx`, bytes `66 89 4D 30` @0x0082DB61
  (01_RAW/E2_FUN_0082DAC0_DISASM.txt; 16-bit width note: a 16-bit write can alias the low
  half of a 32-bit field; the BASE REGISTER is what matters —
  02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §2 row E2).
- Historical function attribution 0x0082DAC0 DISPROVEN: lead `00 00` bytes, zero
  E8/E9/EB/imm32 references, no fallthrough (01_RAW/E2_CALLER_PROVENANCE_CENSUS.txt; QC
  ref census reproduced).
- The REAL containing function is 0x0082DA80 (ret+CC-padded boundary): EBP is REDEFINED at
  entry — `push ebx; push ebp; mov ebp, ecx` @0x0082DA82 = the reader `this`
  (01_RAW/E2_FUN_0082DAC0_DISASM.txt; QC entry decode + EBP-write scan reproduced).
- The caller FUN_0082DFF0 (sole caller of 0x0082DA80; exactly two entry sites 0x006B0C63 /
  0x006B0F38, zero indirect channels) constructs the reader IN PLACE as a STACK LOCAL on
  BOTH entry paths: `lea ecx, [esp+0x9c]`; `call 0x82d920` (constructor storing vtable
  0x00A9189C) — and passes the SAME stack slot to FUN_0082DA80 (QC aligned disasm at both
  call sites: `lea ecx,[esp+0xac]` after the four intervening pushes = the same slot
  0x9c+0x10=0xac; `mov esi,ecx` @0x0082E017 forwards it; 06_REPORT/QC_AUDIT.md §3).
- Class corroboration: RTTI walk of vtable 0x00A9189C -> COL 0x00AB25E8 ->
  TypeDescriptor 0x00B96D3C -> `.?AVArkNiTGAReader@@` — a class distinct from
  SceneFeederObject (QC independent RTTI walk reproduced).
- CASE PROVEN: **B (+ class corroboration)** — the EBP value at the writer is a STACK
  ADDRESS of an ArkNiTGAReader on every writer-reaching path; SF is always-heap per the
  accepted census, so a stack address can never alias SF+0x30. **E2 FINAL CLASS:
  REJECTED_ALIAS (REJECTED_STANDS_SOUND)** — a NEW sound proof, not the old rule's survival
  (02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §2 row E2; QC judgment 06_REPORT/QC_AUDIT.md
  §3; PE-MASTER CONFIRMED — 06_REPORT/PE_MASTER_REVIEW.md CLAIM_MATRIX (2)).

## 4. Canonical census counts change + the P2-1 exposure statement

- Counts: the historical canonical layer (LINK30 CSV self-count 2 PROVEN / 618 POSSIBLE /
  3023 REJECTED + the AMEND_R2 sidecar delta for row 0x0040525B) was
  **3643 = 2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED**; the E1 reclassification
  (REJECTED -> POSSIBLE, the sole change; E2 unchanged) yields the NEW canonical layer
  **3643 = 2 PROVEN / 620 POSSIBLE / 3021 REJECTED / 0 UNRESOLVED** — DERIVED, not
  hard-coded; TOTAL == 3643 invariant asserted; the historical CSV/RAW are byte-identical
  before == after (SHA256 CSV 71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0,
  RAW 64402A73013B52943E10AE17BB115F466A0D3BEF98AA3835915CF3C1CD572248; both re-verified at
  persistence STEP 0). Sources: 02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §1/§3/§4; QC
  recompute 06_REPORT/QC_AUDIT.md §6 (G9 CONFIRMED); gate rows G9 in
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv. The append-only annotation applied to the LINK30
  package: docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/02_ANALYSIS/
  SF30_WRITER_CENSUS_SUPERSESSION_R3.md (drafted verbatim in
  02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §5; applied by the persistence step).
- **P2-1 exposure statement** (CONFIRMED input-layer defect of the HISTORICAL census, not of
  this cleanup; 06_REPORT/QC_AUDIT.md §5 + FINDINGS REGISTER P2-1; PE-MASTER FINDING_DISPOSITION
  in 06_REPORT/PE_MASTER_REVIEW.md): the historical census.py function-attribution layer
  (FNMAP/find_function_start) can attribute writers to non-function VAs — the 16-aligned +
  preceded-by-0x90/0xCC heuristic misreads operand/disp bytes as entry padding (byte-proven
  at 0x007EABFF and 0x0082DABF). Rule-level scoping: the 2765 R-ESP rejections are
  FORM_ONLY (attribution-independent — the base register is read from the writer's own
  operand) and SAFE; **up to 257 attribution-dependent REJECTED rows** (R-STACK-PTR 129 /
  R-CTOR-OTHER 104 / R-ZERO 18 / R-LEA-STACK 3 / R-EBP-INHERITED 2 / R-CONT-FIELD 1;
  R-IMM-STATIC 1 already superseded) are the exposure class; the QC sample N=15 (10
  attribution-dependent + 5 form-only) found 15/15 plausible function starts — a SAMPLE,
  not a census; the per-row exposure remains UNKNOWN; false REJECTEDs can only fall to
  POSSIBLE, never silently to PROVEN (the PROVEN rows are anchor-based). The census-wide
  attribution re-derivation is QUEUED as future backlog for a future authorized run
  (06_REPORT/REPORT.md §9; 06_REPORT/PE_MASTER_REVIEW.md NEXT_EXPERIMENT).

## 5. Evidence pointer index (every raw/analysis artifact of the revalidation)

- 01_RAW/E1_FUN_007EAC00_DISASM.txt — E1 disproof + real-function disassembly (E1).
- 01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt — E1 reference/caller censuses + level-2 closure.
- 01_RAW/E2_FUN_0082DAC0_DISASM.txt — E2 disproof + real-function disassembly (E2).
- 01_RAW/E2_CALLER_PROVENANCE_CENSUS.txt — E2 caller/entry-site census + stack-local proof.
- 01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt — G8 negative test + positive control raw outputs.
- 01_RAW/IDENTITY_VERIFICATION_AT_START.txt / _AT_END.txt — fail-closed identity + hash
  records before == after (generator-revision provenance disclosed: START 83B392E3...,
  END 1E28AF12...; measurements identical).
- 01_RAW/GIT_OBSERVATIONS_AT_CLEANUP_START.md — the executor's timestamped git observation.
- 01_RAW/ENTROPIA_PE_OPTIONAL_HEADER_DUMP.txt — AUD-F4 byte derivation (standard PE32 layout).
- 01_RAW/NIRTTI_BOUNDED_PROBE_0xBA7270.txt — the bounded probe raw record (W6).
- 02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md — the authoritative E1/E2 derivation +
  counts + the R3 sidecar draft (§5).
- 02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md — the superseding rule + operational checklist +
  mandatory tests.
- 02_ANALYSIS/SCIENCE_STATUS_MATRIX.csv — standing/changed science rows.
- 00_CONTROL/ebp_alias_classifier.py — the rule V2 implementation (G8).
- 00_CONTROL/e_ebp_reval.py — the E1/E2 revalidation generator (W1/W2).
- 00_CONTROL/cleanup_verify_identities.py — the identity/hash verification generator.
- 03_EVIDENCE/EVIDENCE_INDEX.csv (+ README.md) — every artifact with generator + generator
  SHA256.
- 06_REPORT/QC_AUDIT.md — the G14 fresh QC independent reproduction of every load-bearing
  chain above.
- 06_REPORT/REPORT.md (§1-§9) + 06_REPORT/HANDOFF.md — the run report/handoff.
- 06_REPORT/STAGE_ACCEPTANCE_GATES.csv — gates G0-G15 (G6/G7/G8/G9 = the E1/E2/classifier/
  counts gates).
- 06_REPORT/PE_MASTER_REVIEW.md — the PE-MASTER adjudication record (MASTER_ACCEPTED,
  advisory; STATUS_ALGEBRA + CLAIM_MATRIX restate the CONFIRMED statuses of §2-§4).

— pe-master-auditor (persistence worker), 2026-09-14, under PE-MASTER loop
2ed038db-5d2e-4e7e-b679-2d29bf57501a, per the human's 2026-09-14 cleanup authorization.
