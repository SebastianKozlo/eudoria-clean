# EBP CLASSIFIER RULE V2 — corrected rule for all future censuses

RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
GENERATOR: this document was written by the cleanup executor; the operational rule is
implemented by `00_CONTROL/ebp_alias_classifier.py` (SHA256 recorded in
`01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt`); test evidence = the same raw file.

## 1. The superseded rule (R-EBP-INHERITED) and why it is unsound

The historical LINK30 census rejected writers of the form `[ebp+0x30], reg` when the
"containing function" appeared never to redefine EBP, reasoning: "fn never redefines ebp
(FPO, ebp untouched); ebp = ancestor frame pointer = stack address".

That inference is **UNSOUND AS A RULE**:

- EBP is a callee-saved register; a function that does not redefine EBP has NO knowledge
  of its value. "Untouched" means UNKNOWN LIVE-IN, not "stack address".
- EBP may carry arbitrary caller state: a `this`/object pointer, a global, a spilled
  argument — anything the caller (or an ancestor) left in it.
- The E1/E2 revalidation (W1/W2, this package) additionally found that BOTH rows
  rejected under that rule had WRONG historical function attributions: the claimed
  function entries (0x007EAC00, 0x0082DAC0) are not function entries at all (leading bytes
  `00 00`, zero E8/E9/EB/imm32 references, no fallthrough), and the REAL containing
  functions REDEFINE EBP (0x007EA76D `mov ebp, [esp+0x1a0]`; 0x0082DA82 `mov ebp, ecx`).
  The premise "ebp untouched" was false even as a factual claim about the real functions.

## 2. THE RULE (V2)

**UNKNOWN LIVE-IN EBP → NEVER structural REJECTED solely because EBP is untouched.
Default = POSSIBLE_ALIAS unless proven otherwise by an explicit case:**

- **Case A — frame construction**: explicit current-function frame construction
  (`push ebp; mov ebp,esp`) before the writer on every writer-reaching path.
  Then EBP = the function's own frame pointer = a stack address.
- **Case B — explicit stack derivation**: explicit derivation of EBP from ESP/stack
  before the writer on every writer-reaching path (`mov ebp, esp`; `lea ebp, [esp+X]`;
  or a derivation chain through argument registers PROVEN to hold a stack address on
  every entry path, e.g. EBP := ECX where ECX := `lea ecx, [esp+X]` at every reachable
  call site — as proven for E2 in this package).
- **Case C — bounded entry/caller provenance**: bounded caller closure proving the
  incoming EBP is non-SF on every entry path (e.g., every reachable caller holds a live
  standard frame pointer at its call site, so incoming EBP is a stack address; or the
  EBP-source object is proven to be of a class distinct from SceneFeederObject on every
  path). The closure must enumerate ALL entry channels: E8 rel32 census, whole-file
  imm32 address-taken census, E9/EB jump census, and entry-fallthrough check.

**For a REDEFINED EBP (the common real case) the same standard applies to the DEFINING
instruction**: REJECTED requires proof that the EBP VALUE at the writer is a stack/frame
address or an object that can never be SF (class proof); an EBP defined from an
argument/register of unbounded provenance → POSSIBLE_ALIAS, with the caller chain walked
to a DECLARED bound (two levels by default) before declaring the provenance UNKNOWN.

SF (SceneFeederObject) is always-heap per the accepted census: a stack/frame address can
never alias SF+0x30. Operand width does not change the analysis (a 16-bit write can alias
the low half of a 32-bit field; the BASE REGISTER is what matters).

**A direct E8 census alone is NOT sufficient** if the function can be reached indirectly
(address-taken / jump / fallthrough). If entry provenance remains open, the row
classification is POSSIBLE_ALIAS — which does NOT mean the target IS SF+0x30; it means
REJECTED is not proven.

## 3. Operational checklist (implemented by the checker)

1. Fail-closed binary identity (SHA256+SIZE) before any byte read.
2. Verify the writer bytes + decode at the writer VA.
3. Verify the claimed containing function: decode from the claimed entry; if the stream
   is misaligned or the VA has zero references (E8/E9/EB/imm32/fallthrough), DISPROVE the
   attribution and discover the real containing function (E8-target lattice + padding
   boundary + forward-alignment on the writer + ret-crossing check).
4. Track EBP writes from the (real) function entry to the writer.
5. Apply the case A/B/C test; record VA+bytes for every load-bearing step.
6. Record which case was proven, or NONE_PROVEN → POSSIBLE_ALIAS.

## 4. Mandatory negative test + positive control (G8)

- NEGATIVE (SYNTHETIC_FIXTURE — never claimed to be Entropia bytes): incoming EBP
  unknown; the function does not redefine EBP; a write `[ebp+0x30], reg`.
  REQUIRED classifier output: **POSSIBLE_ALIAS**. If it returns REJECTED_ALIAS the
  cleanup FAILS (G8).
- POSITIVE CONTROL: `push ebp; mov ebp,esp; mov [ebp+0x30], eax` → REQUIRED output:
  **REJECTED_ALIAS** (sound case A). If not, the checker is broken (G8).
- Both raw outputs: `01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt`.
