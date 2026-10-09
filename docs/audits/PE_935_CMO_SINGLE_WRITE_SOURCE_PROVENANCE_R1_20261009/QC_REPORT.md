# QC_REPORT — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

Fresh-context INTERNAL QC of the bounded static RE micro-run
`PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009` (executor phase package,
12 files), against the measured contract
`OPENCODE_CMO_SINGLE_WRITE_PROVENANCE_R1_REVISED.md`
(20 158 B / SHA256 `C6599C0CCEB93DA5CD0E6B950DC3EF8AE6826FA962ABE99492F3931C7244CEB5`
— identity verified MATCH before any work).

**REAL ORIGIN:** pe-master-auditor fresh-context internal QC, internal to
PE-MASTER. This is NOT an independent Desktop post-audit, NOT
MASTER_ACCEPTED and NOT milestone closure. PE-MASTER remains advisory while
Q1 is unqualified. No publication actions were performed in this phase.

**QC_VERDICT = QC_PASS** (all nine duties hold on independent measurements;
the receiver temporal-nuance wording survives adjudication; science outcome
A stands as worded; three non-material documentation findings are recorded
below — two P2, one P3, plus one observation).

---

## 0. Input and state identity (measured)

| Item | Measured | Expected | Status |
|---|---|---|---|
| Contract SIZE/SHA256 | 20158 / C6599C0C…4CEB5 | same | MATCH |
| git HEAD (start and end of QC) | b2feef34122d2118da6ab38fc78f20f337315570 | EXPECTED_BASE_SHA | MATCH (unchanged; no commits, no push) |
| Tracked tree | clean (only untracked audit packages present, untouched) | clean | MATCH |
| Entropia.exe SIZE/SHA256 (pre-QC) | 8015872 / E7785430…5280F31 | same | MATCH |
| Entropia.exe SIZE/SHA256 (post-QC) | 8015872 / E7785430…5280F31 | same | MATCH (EXE unchanged; all QC mutations ran on in-memory copies only) |

Executor package files read **12/12 in full** (report, ledgers, CSV, JSON,
raw records, both scripts). Source packages verified unchanged (§8 below).

## 1. Method and independence

- **Own PE parser.** QC did NOT import the executor's Source B reader. The
  PE header was parsed independently (ImageBase 0x00400000, SectionAlignment
  4096, FileAlignment 4096, sections .text/.rdata/.data/.tls/.rsrc measured)
  and the VA→file-offset mapping was derived from the section table by QC:
  VA 0x0085B281 → file offset **4567681** — identical to the executor's claim.
- **Own x86-32 boundary decoder**, written independently of the executor's
  `x86_minidec_r1` (different implementation structure: opcode-class dispatch
  + ModRM/SIB split; per-class writes/reads sets). Fail-closed on unsupported
  opcodes/jumps.
- **Own byte pins, own rel32 recomputation, own RTTI chain walk, own clobber
  scans, own mutants, own token scans** (own regexes; all 12 package files,
  including the two `.py` scripts the executor's gate skipped).
- QC EXE reads: **456 B total** (W1 232 + W3 52 + W2 4 + RTTI 94 +
  exclusion-census single-instruction pins 74). Single-instruction pins
  only — **no new bodies, no xref expansion, no callee analysis** (within
  the dispatch's minimal-pin allowance for QC duty verification).
- Script: `03_SCRIPTS/qc_remeasure.py` (python -B; EXE never modified).

## 2. Duty 1 — byte re-measurements: **PASS**

All executor pins re-measured from the physical EXE with QC's own reader —
all MATCH:

- Store **0x0085B281 = `89 4E 44`** (3 B, mov dword [esi+0x44], ecx; 32-bit;
  disp8 0x44; base esi) — file offset 4567681 (own mapping).
- Function-start boundary: `C3` @0x0085B1AC + exactly `CC CC CC`
  @0x0085B1AD..AF; entry `8B 44 24 08` @0x0085B1B0 — padding-proven start
  confirmed physically.
- Value chain: `8B 7C 24 14` @0x0085B1DA; `8B CF` @0x0085B24B;
  `E8 E1 B2 EE FF` @0x0085B27A; accessor `8D 41 08 C3` @0x00746560;
  `8B 08` @0x0085B27F.
- Caller pins (W3): `8B F1` @0x00528E76; `8B CE` @0x00528E8B;
  `E8 1E 23 33 00` @0x00528E8D; `C7 06 B0 DC A7 00` @0x00528EA2.
- Base-vtable stamp `C7 06 4C 1E A9 00` @0x0085B1C1 (vtable 0x00A91E4C).
- **rel32 recomputed by QC**: 0x0085B27F + (−0x114D1F) = **0x00746560** ✓;
  0x00528E92 + 0x33231E = **0x0085B1B0** ✓.
- **RTTI chains re-walked by QC** (MSVC layout: vtable[-1]→COL, COL+12→TD,
  TD+8→name): 0x00A91E4C → COL 0x00AB33D0 (sig 0) → TD 0x00B7997C →
  **`.?AVMovableObject@@`** ✓; 0x00A7DCB0 → COL 0x00AA17CC (sig 0) →
  TD 0x00B79958 → **`.?AVClientMovableObject@@`** ✓ (both null-terminated,
  byte-verified).
- QC's own W1 read is **byte-identical** to the executor's CONTROL_RESULTS
  W1 hex (232/232 bytes), and to the committed T1_REGION raw rows.

## 3. Duty 2 — independent boundary decode: **PASS**

QC's own linear fail-closed decode from the padding-proven start
0x0085B1B0 through 0x0085B290:

- **64 instructions / 224 bytes / ends exactly at 0x0085B290** — identical
  count, sizes and boundaries to the executor's instruction table; no
  jump/unknown opcode in the window (straight-line confirmed independently).
- Every load-bearing VA lands on an instruction boundary with the expected
  bytes: 0x0085B1B7 (`8B F1`), 0x0085B1C1, 0x0085B1DA, 0x0085B1E4/E7/EC
  (zero-init **fst** triple `D9 56 44/48/4C`), 0x0085B24B (`8B CF`),
  0x0085B27A (call), 0x0085B27F (`8B 08`), 0x0085B281 (`89 4E 44`),
  0x0085B284/287/28A/28D (copy triple `89 4E 44` / `89 56 48` /
  `89 46 4C`).
- The executor's instruction table is confirmed in full by an independent
  decoder.

## 4. Duty 3 — RECEIVER temporal-nuance adjudication: **ADJUDICATED_SUPPORTED**
(receives the claim as worded; outcome A stands)

**Question:** the store executes while the object carries the BASE vtable
0x00A91E4C (.?AVMovableObject@@) — stamped in the same body at 0x0085B1C1,
linearly BEFORE the store (QC's decode: no branch in the window). The
derived vtable 0x00A7DCB0 (.?AVClientMovableObject@@) is stamped by
FUN_00528E50 at 0x00528EA2 only AFTER the base ctor returns. Is the claim
"receiver = the MovableObject-under-construction which later becomes the
ClientMovableObject on the same memory" supported and correctly worded?

**Adjudication: YES — supported by the full physical chain and correctly
worded.**

- Physical same-object chain (all pins QC-verified): caller
  `mov esi,ecx` @0x00528E76 (ESI := FUN_00528E50's entry this) →
  `mov ecx,esi` @0x00528E8B → `call 0x0085B1B0` @0x00528E8D → base ctor
  `mov esi,ecx` @0x0085B1B7 (same pointer) → store `[esi+0x44]` @0x0085B281;
  after return, the SAME ESI receives the derived vtable stamp @0x00528EA2.
  Same memory, proven by pointer identity, not class similarity.
- At store time the object is the MovableObject-under-construction (base
  vtable stamped at 0x0085B1C1 < store at 0x0085B281, straight-line).
- **Wording audit:** every claim site (PREREGISTRATION §6, CLAIM_MATRIX
  CL-02, RECEIVER_LINEAGE.txt, ANCHOR_SELECTION §4, SELECTED_WRITE_BYTES
  STATUS) states the nuance explicitly — "the MovableObject (vtable
  0x00A91E4C at store time) that FUN_00528E50 turns into a
  ClientMovableObject (vtable 0x00A7DCB0 stamped on the same memory after
  the base ctor returns)", explicitly "not as a finished CMO at store time".
  **No overstatement found; no site claims the object is already a
  ClientMovableObject at store time.**
- **Is 'CMO+0x44' honest under §3?** Yes. §3 permits "CMO where physically
  established". The ClientMovableObject identity of the examined
  construction chain is physically established in this run (same-pointer
  chain + both RTTI walks + derived-vtable stamp), so naming the final
  object's field +0x44 as "CMO+0x44" is a physically grounded label of the
  same memory — NOT a class-similarity conflation. The destination claim
  itself is worded "instance+0x44" / "that instance's +0x44 field".
- **RECEIVER_IDENTITY = CONFIRMED (scoped to the examined
  FUN_00528E50 → FUN_0085B1B0 construction path) — upheld.**
- **Disclosed assumption (limitation, not a break):** ESI/EDI preservation
  across the 5 in-window calls (FUN_007345C0, FUN_004123D0, FUN_00746550,
  FUN_00746570 — bodies not read) rests on the standard x86 MSVC thiscall
  callee-saved ABI (EBX/EBP/ESI/EDI); FUN_00746560 is physically 4 bytes
  (`lea eax,[ecx+8]; ret`) and trivially preserves ESI. The executor states
  this assumption explicitly (RECEIVER_LINEAGE R5; VALUE_PRODUCER V1). QC
  records it as a disclosed standard RE assumption about unread callee
  bodies.

## 5. Duty 4 — value provenance: **PASS**

Chain hop-by-hop, all bytes QC-verified, all arithmetic QC-recomputed:

```
[esp+0x14] -> EDI   @0x0085B1DA (mov edi,[esp+0x14])
EDI -> ECX          @0x0085B24B (mov ecx,edi)
ECX -> call         @0x0085B27A (call 0x00746560)
callee returns ECX+8 in EAX (4-byte accessor lea eax,[ecx+8]; ret @0x00746560)
[EAX] -> ECX        @0x0085B27F (mov ecx,[eax])   <-- VALUE_PRODUCER_VA
ECX -> [esi+0x44]   @0x0085B281 (the selected store)
```

- **arg1 = [esp+0x14] stack proof independently verified by QC's own
  decode**: first instruction `mov eax,[esp+8]` reads arg2 pre-push; four
  pushes (ebx/ebp/esi/edi) move entry [esp+4] (arg1) to [esp+0x14]. ✓
- **Own clobber scans (over QC's 64-instruction decode):** EDI writers in
  (0x0085B1DA, 0x0085B24B] = 0; ECX writers in (0x0085B24B, 0x0085B27A) = 0
  and in (0x0085B27F, 0x0085B281) = 0; **calls** between 0x0085B24B and
  0x0085B27A = 0 (so ECX cannot be caller-clobbered on that segment);
  ESI def sites in window = only 0x0085B1B7; EDI def sites = only
  0x0085B1DA. ✓ (matches the executor's scans).
- **VALUE_SOURCE_CLASS = COPY_FROM_MEMORY upheld**: stored value = the
  dword at [arg1+8], copied verbatim — no conversion, no arithmetic, no x87
  round-trip anywhere in the chain. VALUE_PRODUCER_VA 0x0085B27F upheld.
- **arg1 upstream honesty upheld**: the trace terminates at the ctor
  argument BY DESIGN; the upstream (placement-record corrected-copy z'
  chain) is cited ONLY as committed historical context (attribute seam
  S6–S9/ERRATA_R5) with its own axes/units-UNRESOLVED caveat; the
  representation (f32 vs u32) is explicitly NOT established
  (VALUE_PRODUCER_LINEAGE "REPRESENTATION DISCIPLINE"). The executor claims
  no representation semantics. ✓

## 6. Duty 5 — anchor census and selection: **PASS**
(with two non-material record-description findings, §12)

- **Six qualifying stores byte-exist** (QC pins): copy triple
  89 4E 44 / 89 56 48 / 89 46 4C @0x0085B281/87/8D and zero-init fst triple
  D9 56 44 / D9 56 48 / D9 56 4C @0x0085B1E4/E7/EC. ✓
- **All 10 exclusion records are genuine** — QC byte-pinned every cited
  instruction in the EXE (single-instruction pins; no new bodies):
  - **C-G** (FUN_00509510): `F3 A5` @0x00509557 with receiver
    EBX=SF (`8B D9` @0x00509518; `8D 7B 4C` lea edi,[ebx+0x4c] @0x0050954D);
    SF obtained via `mov ecx,[esi+0xC0]` @0x00529025 — **not a CMO store**
    ✓ (also matches committed source-A FUN_509x_SF_METHODS.txt).
  - **C-H** [CMO+0xC0] store `89 86 C0 00 00 00` @0x00528FEA ✓ (real CMO
    store, offset outside the lead set).
  - **C-I** [CMO+0xB4] `D9 9E B4 00 00 00` @0x00529058 ✓.
  - **C-J** placement-record ctor `89 46 44`/`89 4E 48`/`89 56 4C`
    @0x0074539B/A4/AD ✓ (receiver = record object; committed
    F00745360_REC_CTOR.txt).
  - **C-K** manager ctor `89 46 44` @0x008551CA ✓ (+ QC region probe
    @0x00855260 shows `89 46 48` — see F-QC-3).
  - **C-L** SF ctor `D9 55 44`/`D9 55 48` @0x005093E9/F1 and
    `89 45 44`/`89 4D 48` @0x0050944C/55 ✓ (receiver EBP=SF; see F-QC-2).
  - **C-M** `89 46 44` @0x008BD750 ✓; **C-N** `89 5E 48`/`89 5E 4C`
    @0x006C8FBB/BE ✓; **C-O** `89 46 44` @0x006C94FF ✓;
    **C-P** transform-family own-vtable stamp `C7 06 A4 14 A8 00`
    @0x005D48B6 ✓ (committed S5_TRANSFORM_WRITES.json families).
- **Selection rule pre-registered:** PREREGISTRATION §4 fixes the priority
  (copy family over zero-init bulk idiom; lowest VA within the family) and
  the selected store with EXPECTED bytes from committed evidence —
  BEFORE the physical re-pin; PREREGISTRATION contains no newly measured
  values (all "expected"); measurements appear only in CONTROL_RESULTS.
  Documentary consistency: PASS. (No independent timestamp evidence exists
  or is claimed; none contradicts pre-registration.)
- **Tie-break alternative honestly disclosed:** a strict lowest-VA rule
  would pick the zero-init fst @0x0085B1E4 with a CONSTANT (fldz) source;
  the pre-registration discloses and rejects it (bulk 12-field float-zero
  idiom +0x44..+0x70 = the anti-manufacturing clause; degenerate value
  provenance; unconditionally overwritten by the copy triple in the same
  straight-line sequence — QC's own decode confirms no branch in the
  window, so the overwrite is unconditional). The full census preserves all
  six store VAs for independent re-adjudication. ✓
- **No manufacturing from the CMO label:** the census is built from
  committed-evidence store records with receiver lineage; every
  reclassified record is byte-verified. ✓

## 7. Duty 6 — budget audit: **PASS** (with F-QC-1, §12)

- **Store budget:** 1/1 used; the sibling stores +0x48/+0x4C are documented
  in the census but not separately analyzed. ✓
- **Body budget (≤1, restricted to the enclosing function):** FUN_0085B1B0
  charged as 1 body in already-decoded (re-pin) status. QC verified the
  committed prior decodes exist and cover the SAME body:
  T1_REGION_0085B100_0085B900.txt (raw hex rows 0085B1B0..0085B28F —
  byte-checked against the EXE), 01_RAW/DECOMP/F0085B1B0.c (Ghidra decompile
  of the same body: param_1_00[0x11..0x13] = *puVar2..puVar2[2] with
  puVar2 = FUN_00746560()), and GHIDRA_H5_VTABLE2.txt lines 1169820-1169826
  (instruction-level, read by QC at the cited lines). **Therefore "0 new
  body semantics claimed" is TRUE**; the wording in
  FUNCTION_AND_EDGE_BUDGET.csv is honest. ✓
- **Edge budget (0 new):** both used edges are prior committed and QC-located
  in committed files: FUN_00528E50→FUN_0085B1B0 (call @0x00528E8D —
  attribute-seam REPORT S8; position corrections REPORT line 196) and
  FUN_0085B1B0→FUN_00746560 (call @0x0085B27A — Ghidra H5 line 1169820;
  position corrections line 197). Neither was followed to any new
  caller/callee. ✓
- **Callee bodies (0):** FUN_00746560 = prior 4-byte pin re-read; no other
  callee body appears in any package output. ✓
- **Byte total (F-QC-1):** the declared "TOTAL EXE BYTES READ = 381 B" is
  off by one. The executor's own script reads
  len(".?AVClientMovableObject@@")+1 = 26 name bytes for the 0x00A7DCB0
  RTTI chain (4 + 20 + 26 = 50 B), not the declared 25 (49 B). Recount:
  **232 + 4 + 52 + 44 + 50 = 382 B**. No contract limit applies to "bytes
  read"; every read byte still lies in prior-pinned scope (MICRO_R1
  RTTI_PROBES canon); the defect is numeric transparency only. Required
  correction recorded for the persistence phase (F-QC-1); QC does not edit
  executor files.

## 8. Duty 7 — controls re-verification: **PASS**

- **QC's own mutants (in-memory copies; EXE never modified):**
  - M1 opcode 89→8B at file offset 4567681: real pin PASS / mutant pin FAIL ✓
  - M3 displacement 0x44→0x48: real PASS / mutant FAIL ✓
  - M2 shifted VA 0x0085B282: pin FAIL ✓
  - M5 accessor corruption @0x00746560: real PASS / mutant FAIL ✓
  - **SF-conflation control (own):** selected store VA 0x0085B281,
    receiver ESI = base-ctor this (def @0x0085B1B7, zero clobber writers)
    vs SF store @0x00509557 (receiver EBX=SF, edi=[ebx+0x4C], SF received
    via ecx=[CMO+0xC0] @0x00529025 — all byte-verified). The conflation
    claim "selected store is an SF store" evaluates **FALSE** ✓
    (CMO/SF/NiNode kept distinct; CMO+0x4C ≠ SF+0x4C).
- **Falsifier semantics (§9):** the executor's usage
  FALSIFIER_REJECTED_HYPOTHESIS = NOT_TRIGGERED is correct — F1/F2 were
  evaluated on UNMODIFIED original-client bytes and found NO contradiction;
  synthetic mutation rejection is labeled CONTROL_PASS only, exactly as
  §9 requires. ✓
- **Token gates (own scan, ALL 12 package files — including both .py
  scripts, which the executor's gate skipped by suffix):**
  - `WORLD_XYZ_RECOVERED = YES` / `GLOBAL_COORDINATE_FRAME = ESTABLISHED` /
    `HISTORICAL_PLACEMENT( _RECORD) = ESTABLISHED/YES/RECOVERED` /
    `INSTANCE_MODEL_JOIN = ESTABLISHED/YES/CONFIRMED`: **0 hits in all
    evidence/report files**. The only regex matches are the gate script's
    own pattern DESCRIPTIONS (token_gates.py lines 8-10, 116) — not
    active claims.
  - CMO+0x4C equality conflation: 0 evidence hits (same self-description
    matches only in token_gates.py line 9).
  - `SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC`: exactly ONE
    occurrence in the package (INPUT_IDENTITIES.md line 45), explicitly
    supersession-marked ("…is SUPERSEDED by J3 S-5"). **0 unmarked
    occurrences → no J3 restoration as active.** ✓
  - Promotion probe (+0x44/48/4C ↔ position): 0 hits in evidence files
    (only the gate's self-description). FIELD_SEMANTICS = UNVERIFIED
    ceiling present in the budget ledger, the raw record and the script. ✓
  - See observation F-QC-4 (gate coverage 10/12) — QC's 12/12 scan closes
    the gap; result clean.

## 9. Duty 8 — source artifact identities and SOURCE_PACKAGE_UNCHANGED: **PASS**

All measured by QC (size + SHA256, independently recomputed):

- 7 pinned sources: source A 4 files (10650/ABC21A0D…, 5471/BAB06CEB…,
  6078/3A011632…, 13663/E62B7581…), Source B (38568/80EBEE27…), J3 2 files
  (8339/DD11137A…, 8987/00D09B0F…) — **all MATCH the contract's expected
  pairs**.
- 3 historical context files MATCH INPUT_IDENTITIES.md: MICRO_R1
  FINAL_REPORT.md (14656/39DA4D86…), source A CLAIM_MATRIX.csv
  (5232/32F81A96…), source A REPIN_ANCHOR_WINDOWS.txt (18633/5BE0AC8A…).
- Governance pinned: AUDIT_ENTRYPOINT.md (266375/9377E0FE…, NOT modified),
  PROJECT_OPERATING_MODEL.md (54413/99AE1237…), PROJECT_STATE.json ABSENT
  (recorded N/A; not invented).
- **SOURCE_PACKAGE_UNCHANGED verified:** tracked tree clean at HEAD
  b2feef34 at start and end of QC; no source file touched; the EXE is
  byte-identical after all QC work.
- J3 read COMPLETELY by QC before adjudicating any transform standing;
  S-5 applied verbatim; J3 historical ORIGINAL_EDGE_BUDGET_COMPLIANCE =
  FAIL (22 vs 6) preserved WITHOUT transfer to this run (0 new edges used).

## 10. Duty 9 — status epistemology (§10): **PASS**

| Status | Value | QC check |
|---|---|---|
| INSTRUCTION_IDENTITY | CONFIRMED | own bytes + own decode + committed cross-refs |
| RECEIVER_IDENTITY | CONFIRMED (scoped; temporal nuance adjudicated SUPPORTED) | §4 above |
| VALUE_PROVENANCE | CONFIRMED (COPY_FROM_MEMORY; producer 0x0085B27F) | §5 above |
| FIELD_SEMANTICS | UNVERIFIED (ceiling upheld) | present in ledger/raw/script; no promotion anywhere |
| WORLD_INSTANCE_IDENTITY | NOT_ESTABLISHED | CLAIM_MATRIX CL-07 |
| HISTORICAL_PLACEMENT | NOT_ESTABLISHED | CL-07 |
| WORLD_XYZ_RECOVERED | NO | CL-07 + all outputs |
| GLOBAL_COORDINATE_FRAME | NOT_ESTABLISHED | CL-07 |
| INSTANCE_MODEL_JOIN | NOT_ESTABLISHED | CL-07 |

Coverage classes are distinguished (PREREGISTRATION §6:
CLIENT_KNOWLEDGE_COVERAGE = one store's write provenance in the CMO
construction chain, bounded; RECONSTRUCTION_IMPLEMENTATION_COVERAGE = NONE;
HISTORICAL_GAME_RECOVERY_COVERAGE = NONE). No XYZ, global-frame,
instance-model-join, historical placement or runtime claim is derived from
one write plus synthetic tests. J3 standing and PLUS4 standing carried.
**SCIENCE_OUTCOME = A (WRITE_AND_IMMEDIATE_SOURCE_ESTABLISHED) is upheld.**

## 11. Verdict

**QC_VERDICT = QC_PASS.**

- All nine duties hold on QC's own independent measurements (own PE parser,
  own decoder, own pins/scans/mutants/RTTI walk/token scans).
- The receiver temporal-nuance wording survives adjudication without any
  required correction; the RECEIVER_IDENTITY claim is honest under §3.
- The executor's outcome A, all twelve ledger hops, the census/selection,
  the budget charges (1 store / 1 body as re-pin / 0 new edges / 0 callee
  bodies) and the control/token-gate results are upheld.
- Three non-material documentation findings (F-QC-1, F-QC-2, F-QC-3) and one
  observation (F-QC-4) are recorded below with exact corrections for the
  persistence phase. An honest negative is not a QC failure; none was needed:
  the positives are physically supported.

## 12. Findings (open, with required corrections)

- **P2 — F-QC-1 (budget byte-total off-by-one).**
  `FUNCTION_AND_EDGE_BUDGET.csv` (row `windows_read`) declares
  "RTTI chain 0x00A7DCB0 = 4+20+25 = 49 B … TOTAL EXE BYTES READ = 381 B".
  The executor's script reads `len(".?AVClientMovableObject@@")+1 = 26`
  name bytes → chain = 50 B; **actual total = 382 B**. No science claim,
  gate predicate or contract limit depends on this number (all read bytes
  lie in prior-pinned RTTI scope); the defect is numeric transparency.
  Required correction (persistence phase, not QC-editable): record
  "TOTAL EXE BYTES READ = 382 B (RTTI 0x00A7DCB0 chain = 4+20+26 = 50 B)"
  in the final report or an errata note.
- **P2 — F-QC-2 (census C-L mnemonic typo).**
  `ANCHOR_SELECTION.md` §3.2 row C-L says "fstp [ebp+0x44] @0x005093E9".
  The physical bytes are `D9 55 44` (ModRM reg=2 → **FST**), and the
  committed file (F00509330_SUBC0_B.txt lines 63/65) also shows `fst` for
  BOTH 0x005093E9 and 0x005093F1. Non-material (receiver EBP=SF and the
  reclassification stand; the mov pins are correct). Optional correction:
  "fst [ebp+0x44] @0x005093E9".
- **P3 — F-QC-3 (census C-K secondary-claim citation gap).**
  `ANCHOR_SELECTION.md` §3.2 row C-K claims "+0x48/+0x4C stores
  @0x00855260 region" but the cited committed file
  (T2_HEX/mgr_ctor_FUN_008550C0.txt) ends at 0x008551DF. QC's own EXE probe
  confirms `89 46 48` (mov [esi+0x48],eax) @0x00855260 — the claim is
  physically true, but the citation path does not document it. Non-material
  (the primary pin `89 46 44` @0x008551CA is in the cited file and is
  byte-verified). Optional correction: annotate the region claim with a
  QC-byte-verified marker or the actual committed source.
- **OBSERVATION — F-QC-4 (token-gate file coverage).**
  The executor's token_gates.py scanned 10/12 package files (suffix filter
  .md/.txt/.csv/.json; both .py scripts excluded). QC's own 12/12 scan
  (including both .py scripts) finds NO forbidden active standing anywhere —
  the only pattern matches are the gate script's own self-descriptions. No
  correction required for THIS package; for future runs, include .py files
  in the gate scan or record their exclusion as script-code.

**ABI assumption (disclosed limitation, not a finding against the claim):**
ESI/EDI preservation across FUN_007345C0 / FUN_004123D0 / FUN_00746550 /
FUN_00746570 (bodies unread) rests on the standard x86 MSVC thiscall
callee-saved ABI; the executor documents this explicitly; FUN_00746560 is
physically verified as the 4-byte accessor.

## 13. Coverage and NOT_CHECKED

**Coverage (algebra):**
- Executor package files: 12/12 FULL_READ (reports, ledgers, CSV, JSON, raw
  records, both scripts — to EOF).
- EXE bytes read by QC: 456 B (all windows + RTTI chains + exclusion
  single-instruction pins; no new bodies; no xref expansion; no callee
  analysis).
- Committed evidence: contract (full), J3 (full), source A pinned files
  (full), T1_REGION (full), F0085B1B0.c (full),
  F00746560_CTOR_COPY.txt (full), mgr_ctor_FUN_008550C0.txt (full), Ghidra
  H5 cited line range (1169813-1169832), position-corrections REPORT and
  ERRATA_R5 cited lines, MICRO_R1 FINAL_REPORT cited sections,
  REPIN_ANCHOR_WINDOWS PA4 sections, ORIGIN_TRIPLE_WRITE_CENSUS_RAW line
  378, S5_TRANSFORM_WRITES.json head, and the cited pins of
  F00745360_REC_CTOR.txt / F00509330_SUBC0_B.txt / FUN_008BD720_DECODE.txt /
  FUN_006C8F80_BASECTOR_DECODE.txt / RTTI_PROBES.json / source-A
  CLAIM_MATRIX.csv.

**NOT_CHECKED (explicit):**
- callee bodies FUN_007345C0 / FUN_004123D0 / FUN_00746550 / FUN_00746570
  (callee-saved ABI assumption; bodies remain undecoded);
- FUN_00528E50 entry boundary @0x00528E50 (outside the budget; W3 pins
  suffice for the receiver chain);
- FUN_0085B1B0 extent beyond 0x0085B290 (terminal RET 0xC per committed
  T1_REGION evidence; not re-decoded);
- runtime behavior (STATIC-ONLY; the client never executed);
- remote repository state (no publication actions in this phase; local HEAD
  verified == EXPECTED_BASE_SHA; no remote equality is claimed);
- no independent timestamp proof of pre-registration authorship exists
  (documentary consistency assessed; no contrary evidence found).

## 14. Outputs

- `QC_RESULTS.json` — machine-readable per-duty measured values and verdicts.
- `QC_REPORT.md` — this report.
- `03_SCRIPTS/qc_remeasure.py` — the QC re-measurement script
  (python -B; own PE parser + own decoder; read-only over the EXE;
  mutations in-memory only).

NEXT_PARENT_ACTION (for PE-MASTER, advisory context): the executor phase
package passes fresh-context internal QC with outcome A upheld; the three
documentation findings above (F-QC-1 required, F-QC-2/F-QC-3 optional)
should be carried into the finalization/persistence phase
(FINAL_REPORT / PE_MASTER_REVIEW / errata as PE-MASTER decides). QC made no
edits to any executor file and performed no publication actions.
