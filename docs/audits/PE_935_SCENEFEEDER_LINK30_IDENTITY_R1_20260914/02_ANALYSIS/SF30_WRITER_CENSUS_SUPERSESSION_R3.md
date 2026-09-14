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
