# CANONICAL STATE RECONCILIATION — W4 (census recomputation layer)

RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 · Era: PCG_9_3_5 · MODE: STATIC-ONLY
(the client NEVER ran; own byte reads + own capstone disassembly of the pinned Entropia.exe,
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, fail-closed).

## 1. The starting canonical layer (independently re-derived in this run)

- The historical CSV `PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/02_ANALYSIS/SF30_WRITER_CENSUS.csv`
  (READ-ONLY, byte-identity asserted before and after this run; SHA256
  71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0) was parsed by this
  run's own script: **3643 rows, unique writer_va 3643**, classification counts
  PROVEN_SF30_WRITER=2 / POSSIBLE_ALIAS=618 / REJECTED_ALIAS=3023. This is the R1 layer.
- The AMEND_R2 sidecar (`02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md`, commit
  a7a6c756) superseded exactly one row (0x0040525B REJECTED_ALIAS -> POSSIBLE_ALIAS)
  WITHOUT regenerating the CSV (CSV/RAW byte-identical by design).
- Canonical layer BEFORE this cleanup (CSV + AMEND_R2 delta, the B.7 pin — re-derived):
  **3643 = 2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED.**

## 2. The two rows revalidated in this run (W1/W2)

Derived from this run's own evidence (01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt,
01_RAW/E2_CALLER_PROVENANCE_CENSUS.txt, 01_RAW/E1_FUN_007EAC00_DISASM.txt,
01_RAW/E2_FUN_0082DAC0_DISASM.txt):

### Row E1 — writer 0x007EB1B3

- CSV row 2385 (verbatim): `0x007EB1B3,0x007EAC00,"mov dword ptr [ebp + 0x30], esi",esi,caller stack (inherited ebp),REJECTED_ALIAS`
- OLD_CLASS: REJECTED_ALIAS (historical reason R-EBP-INHERITED — UNSOUND; additionally the
  historical function attribution 0x007EAC00 is DISPROVEN: bytes at the claimed entry start
  `00 00` (mid-stream), and ZERO references exist via E8/E9/EB/whole-file-imm32; no
  entry fallthrough).
- NEW_CLASS: **POSSIBLE_ALIAS**
- PROOF (case proven): **NONE_PROVEN.** The REAL containing function is 0x007EA740
  (SEH-frame FPO, entry-closed: sole E8 caller 0x007EB284, zero indirect channels); EBP
  is REDEFINED at 0x007EA76D `mov ebp, dword ptr [esp + 0x1a0]` = ARG3 — an argument
  pointer, not a frame pointer. Level-2 caller closure (wrapper FUN_007EB210, three call
  sites 0x007C198F / 0x007EB2FF / 0x007EB410): arg3 = an ECX `this` pointer / an incoming
  stack-argument VALUE / a caller EBP register respectively — NONE proven to be a stack
  address or a non-SF object on every writer-reaching path within the declared two-level
  bound.
- STATUS: **REJECTED_SUPERSEDED_TO_POSSIBLE.** Reason superseded: R-EBP-INHERITED is
  unsound as a rule, and its factual premise ("fn never redefines ebp") is false for the
  real containing function (EBP redefined from an argument at 0x007EA76D).

### Row E2 — writer 0x0082DB61

- CSV row 2577 (verbatim): `0x0082DB61,0x0082DAC0,"mov word ptr [ebp + 0x30], cx",cx,caller stack (inherited ebp),REJECTED_ALIAS`
- OLD_CLASS: REJECTED_ALIAS (historical reason R-EBP-INHERITED — UNSOUND; the historical
  function attribution 0x0082DAC0 is likewise DISPROVEN — `00 00` leading bytes, zero
  E8/E9/EB/imm32 references, no fallthrough).
- NEW_CLASS: **REJECTED_ALIAS (unchanged)** — now standing on a SOUND proof.
- PROOF (case proven): **B (with class corroboration).** The REAL containing function is
  0x0082DA80 (sole E8 caller 0x0082E057, zero indirect channels); EBP is REDEFINED at
  0x0082DA82 `mov ebp, ecx` (= the reader `this`). Level-2 closure: FUN_0082DFF0 (the
  caller; exactly two E8 call sites 0x006B0C63 / 0x006B0F38, zero indirect channels)
  constructs the reader IN PLACE as a STACK LOCAL on BOTH paths — `lea ecx, [esp + 0x9c]`;
  `call 0x82d920` (constructor thunk storing vtable 0x00A9189C) — and passes the SAME slot
  (`lea ecx, [esp + 0xac]` after the four intervening pushes) to FUN_0082DFF0, where
  `mov esi, ecx` (0x0082E017) forwards it to FUN_0082DA80. The EBP value at the writer is
  therefore a STACK ADDRESS on every writer-reaching path (case B), and the object's class
  is ArkNiTGAReader (vtable 0x00A9189C -> COL 0x00AB25E8 -> TypeDescriptor 0x00B96D3C ->
  `.?AVArkNiTGAReader@@`) — a class distinct from SceneFeederObject. SF is always-heap
  (accepted census), so a stack address can never alias SF+0x30. (16-bit write note: a
  16-bit store can alias the low half of a 32-bit field; the base-register analysis is
  unchanged.)
- STATUS: **REJECTED_STANDS_SOUND.** Reason superseded: R-EBP-INHERITED (unsound, wrong
  function attribution) is replaced by the case-B stack-derivation proof + class identity.

## 3. Derived canonical counts (NOT hard-coded — derived from the W1/W2 evidence)

- Start: 2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED.
- E1: REJECTED -> POSSIBLE (one row): REJECTED 3022 -> 3021, POSSIBLE 619 -> 620.
- E2: unchanged (REJECTED, now soundly proven).

**DERIVED CANONICAL LAYER: 3643 = 2 PROVEN / 620 POSSIBLE / 3021 REJECTED / 0 UNRESOLVED.**
TOTAL == 3643 asserted (2 + 620 + 3021 + 0 = 3643). ✓

## 4. Rows that do NOT change

All 3641 other rows keep their standing canonical classes (3643 rows total; the two
revalidated rows are dispositioned above; every other row's class is untouched by this
cleanup). The CSV and RAW historical artifacts are byte-identical before == after
(hash asserted in 01_RAW/IDENTITY_VERIFICATION_AT_START.txt and re-asserted at run end).

## 5. DRAFT — future append-only sidecar for the LINK30 package

The persistence worker will create (after PE-MASTER adjudication)
`docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R3.md`
with EXACTLY the content between the DRAFT-BEGIN/DRAFT-END markers below. It is an
ANNOTATION of the historical census artifacts — it does not modify them.

--- DRAFT-BEGIN ---
# SF30_WRITER_CENSUS supersession (R3, PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914) — census row 0x007EB1B3

RUN: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 · Era: PCG_9_3_5 · MODE: STATIC-ONLY
(the client NEVER ran). RUN_CLASS: MATERIAL (process/persistence/revalidation).
This sidecar is an ANNOTATION of the historical census artifacts — it does not modify them.

## The superseded row (CSV row 2385, quoted verbatim from 02_ANALYSIS/SF30_WRITER_CENSUS.csv)

`0x007EB1B3,0x007EAC00,"mov dword ptr [ebp + 0x30], esi",esi,caller stack (inherited ebp),REJECTED_ALIAS`

## Canonical supersession statement

The historical rejection reason R-EBP-INHERITED ("fn never redefines ebp (FPO, ebp
untouched); ebp = ancestor frame pointer = stack address") is SUPERSEDED on two grounds,
both proven from the physical bytes (fail-closed SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31):

1. The rule is UNSOUND (EBP is callee-saved and may carry arbitrary caller state).
2. Its factual premise is FALSE for the real containing function, and the historical
   function attribution itself is DISPROVEN: 0x007EAC00 is not a function entry (leading
   bytes 00 00 = mid-stream; ZERO references via full-.text E8/E9/EB census and
   whole-file imm32 census; no entry fallthrough).

The REAL containing function is 0x007EA740 (MSVC SEH-frame FPO; entry-closed: sole E8
caller 0x007EB284 inside the NiNode-RTTI-guarded dispatch wrapper FUN_007EB210; zero
E9/EB/imm32 channels; CC-padding boundary). Inside it, EBP is REDEFINED at 0x007EA76D
(`mov ebp, dword ptr [esp + 0x1a0]` = ARG3). Level-2 caller closure over the wrapper's
three call sites (0x007C198F / 0x007EB2FF / 0x007EB410) finds arg3 = an ECX `this`
pointer / an incoming stack-argument VALUE / a caller EBP register — no case A/B/C proof
that the EBP value is a stack address or a non-SF object on every writer-reaching path
(declared two-level bound; provenance UNKNOWN beyond).

CANONICAL CLASSIFICATION CHANGE: row 0x007EB1B3 REJECTED_ALIAS -> **POSSIBLE_ALIAS**.
This does NOT assert the write IS SF+0x30; it asserts the historical rejection was never
proven.

Companion row 0x0082DB61 (`mov word ptr [ebp + 0x30], cx`), revalidated in the same run,
KEEPS REJECTED_ALIAS — now SOUNDLY: real function 0x0082DA80 (EBP := ECX at 0x0082DA82);
both entry paths construct the reader as a STACK LOCAL ArkNiTGAReader
(`lea ecx, [esp + 0x9c]`; ctor 0x82d920 stores vtable 0x00A9189C ->
`.?AVArkNiTGAReader@@`) — case B + class proof.

CANONICAL COUNTS: 3643 = 2 PROVEN / 620 POSSIBLE / 3021 REJECTED / 0 UNRESOLVED
(was 2/619/3022/0; the E1 row is the sole change; TOTAL == 3643 invariant).

Evidence: 01_RAW/E1_FUN_007EAC00_DISASM.txt, 01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt,
01_RAW/E2_FUN_0082DAC0_DISASM.txt, 01_RAW/E2_CALLER_PROVENANCE_CENSUS.txt,
02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md in
docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/.
--- DRAFT-END ---
