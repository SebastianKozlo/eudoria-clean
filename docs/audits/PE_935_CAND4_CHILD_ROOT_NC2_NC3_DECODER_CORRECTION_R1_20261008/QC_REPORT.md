# QC_REPORT — Fresh Independent Internal QC
## PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008

| field | value |
|---|---|
| RUN_ID | PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008 |
| RUN_CLASS | RECORDS_AND_QC_MACHINERY_CORRECTION |
| QC_VERDICT | **PASS** (G1..G6 all PASS; executable terminal gate, every condition recorded individually in 00_CONTROL_INTERNAL_QC/QC_RESULTS.json) |
| QC_ORIGIN | **pe-master-auditor — FRESH-CONTEXT INDEPENDENT INTERNAL QC under direct PE-MASTER dispatch.** This is NOT a Desktop post-audit, NOT the future Desktop post-audit of the eventual published correction SHA, and NOT the executor's self-review — the audited executor phase was pe-reconstruction. |
| AUDITED EXECUTOR SCOPE | NC2+NC3 decoder correction (production side) + PRE/POST matrices + regressions A–D ONLY (six files; SOURCE_STATE.md §2); zero new science, zero EXE access, zero runtime |
| METHODS | own regex parser over the published record; own successor decoder/checker; importlib execution of the ACTUAL corrected production function for comparison only; ast.parse + ast.literal_eval for the historical SIB_BATTERY constant; `python -B` + `sys.dont_write_bytecode` (zero `__pycache__`/`.pyc` residue — verified); NO git operations, NO EXE, all buffers synthetic/in-memory |
| DETERMINISM | no timestamps; all rows machine-measured in this QC run |

---

## 1. Input identities (all physically re-measured by THIS QC — Q0: PASS)

| input | size / SHA256 | verdict |
|---|---|---|
| dispatch contract OPENCODE_NC2_NC3_CORRECTION.md | 14069 / 3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F | MATCH (read in FULL before any work) |
| PRIOR_SCIENCE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt | 4043 / A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3 | MATCH |
| SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py (READ-ONLY) | 51943 / 529B61DB312AEC338221425B12F2D94DE2BE351B5C62F68DDBA6BF915B007B25 | MATCH |
| SOURCE_PACKAGE 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py (READ-ONLY) | 17740 / 44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405 | MATCH |
| 03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py (audited production) | 21069 / 68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13 | MATCH |
| CONTROL_RESULTS_PRE.json | 51477 / 00A90A837E08E1FE7661C0C1E184417200E494587F1FB3A4E098A93B3D7E08B1 | MATCH |
| CONTROL_RESULTS_POST.json | 71311 / 5E09A5126672F63D2F6C1E19543505597FF80B2C55C13259139DB78C3E12E49D | MATCH |
| Desktop CONTROL_COUNTERCHECKS.json (CITED reference) | 132471 / AD8DC2052F714439497A277512944EF729F53BDC94B436CB20EE09FEE6BCC28D | MATCH |

Repo state during this QC: LOCAL_HEAD = 91598a9868037c4954e22e16c535d6a5a671771e (unchanged; this
QC created NO commit and staged NOTHING); OUTPUT_ROOT untracked as expected (publication is the
parent's phase); AUDIT_ENTRYPOINT.md READ-ONLY, not touched, still without an NC2/NC3 line —
consistent with the executor's honest scope statement (SOURCE_STATE.md §6).

## 2. Independence lineage disclosure

- **This QC's engine is its own implementation**: the corrected successor of the historical
  internal-QC implementation (SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py,
  pe-master-auditor lineage, READ-ONLY, SHA-pinned above; fully read — all 851 lines). It keeps the
  historical internal-QC style (own `mem_dlen` displacement helper with the fused NC1 SIB rejection,
  own `Insn` class, own fail-closed linear decode, own P1–P4 checker) and applies the QC-side
  corrections: **NC2 kept** (the historical 0x84 branch already rejected every memory TEST form
  before any length computation — register TEST 84 C0 stays supported); **NC3-A corrected** (the
  historical erroneous FF /3 acceptance is REMOVED — FF D8 is the invalid register encoding of far
  CALL, not a PUSH; FF /6 NOT added; only FF /2 mod=11 remains, incl. the FF D2 endpoint);
  **NC3-B corrected** (LEA mod=11 rejected explicitly BEFORE operand formatting → checker returns
  (False, diagnostic), never TypeError). NC1 guards preserved in every memory-ModRM branch.
- **No production import in the verdict path**: my_ctrl4/my_decode share no helper, no module and
  no code structure with 03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py (production: standalone
  `_reject_sib` + inline size/memoff table; mine: fused `mem_dlen` + own formatting paths).
- The ACTUAL corrected production checker WAS executed separately, via importlib, ONLY for
  comparison on the same in-memory buffers (import-inertness verified by THIS QC's full read of all
  377 lines: no file I/O, only a fixture-length assert at module level).
- **DISCLOSED SHARED ASSUMPTION (by design, contract-mandated)**: both checkers implement the SAME
  contract-mandated P1–P4 exact-endpoint predicate and the SAME eight-case matrix definitions.
  The predicate and case set are frozen by the contract; the implementations are independent.
  Matrix agreement is therefore a same-predicate cross-check of two independent decoders, NOT a
  universal x86-decoder correctness proof.
- All eight buffers were re-derived MY OWN way (clean via my own parser over the published
  per-instruction record; cases 2–5 same definitions as the NC1 package; cases 6–8 replace EXACTLY
  the 12 bytes @0x0050A3DD..0x0050A3E8 with fail-closed asserts on the original span bytes); the
  window stays 0x42 in every case and the bytes outside each mutation span were verified identical
  to clean. MY NC2/NC3 buffers are byte-identical to the cited Desktop residual case buffers 3/3.
  My re-derived clean window SHA256 = 9AC6A7529F1EB2F2424C424E6B3E3BD0BAB133C39CEC18FCC13ADCB02B349398
  — byte-identical to the production fixture (verified at import time).

## 3. The eight-case matrix — 16/16 rows match (G1: PASS)

| # | case | mutation (vs clean) | buffer SHA256 | MY checker | production (actual, importlib) | required |
|---|---|---|---|---|---|---|
| 1 | REAL_RECORDED_CLEAN | — (the published 0x42 window) | 9AC6A752…B349398 | PASS | PASS | PASS/PASS |
| 2 | HISTORICAL_EDI_CLOBBER | 6 B @0x0050A3DD → 8B 3D D0 D8 B9 00 | 1EC7B30C…C6E6847F | FAIL (P2: EDI write @0x0050A3DD) | FAIL (P2, identical site) | FAIL/FAIL |
| 3 | FINAL_PUSH_ESI | 57→56 @0x0050A3F6 | 230C6E38…E36909A1 | FAIL (P3) | FAIL (P3) | FAIL/FAIL |
| 4 | FINAL_PUSH_NOP | 57→90 @0x0050A3F6 | 6E0AAAED…8F889BA03 | FAIL (P3) | FAIL (P3) | FAIL/FAIL |
| 5 | NC1_SIB_HIDDEN_EDI_WRITE | 12 B @0x0050A3DD..E8 → 8B 8C 24 8C 00 00 E8 BF AA BB CC 90 | 257450DD…AFB3F7DAC | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject @0x0050A3DD) | FAIL/FAIL |
| 6 | NC2_NON_SIB_TEST_HIDDEN_EDI | 12 B → 84 06 BF AA BB CC E8 90 90 90 90 90 | F4C14EA9…DBA2EA9CA9 | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject @0x0050A3DD) | FAIL/FAIL |
| 7 | NC3_INVALID_FF_FAR_CALL_REGISTER | 12 B → FF D8 90×10 | 270F2EE5…CB8ADF33A3 | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject @0x0050A3DD) | FAIL/FAIL |
| 8 | NC3_INVALID_LEA_REGISTER | 12 B → 8D C0 90×10 | 978E5977…C7E5C2D5CAB | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject @0x0050A3DD) | FAIL/FAIL |

P1–P4 semantics unchanged and jointly required (exact 8B F8 @0x0050A3B7; no caller-side EDI write in
(0x0050A3B7, 0x0050A3F6); exact 57 @0x0050A3F6; exact FF D2 @0x0050A3F7 — no shift). For cases 2,
5–8 the P1/P3/P4 bytes are preserved (FAIL comes from P2 or the decoder rejection, not from breaking
the endpoints); cases 3–4 deliberately break P3. **Zero unexpected exceptions in all 16 rows**
(each engine's checker catches only (ValueError, IndexError); no TypeError anywhere — the historical
sibfixed LEA TypeError no longer occurs in the corrected production).

## 4. Production authenticity (G2: PASS)

- Measured SHA256 of the audited production script = **68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13** — equals the pin AND CONTROL_RESULTS_POST.json `production_checker.script_sha256`.
- The ACTUAL function was executed via importlib (no imitation, no hardcoded results) and **every
  CONTROL_RESULTS_POST.json matrix row equals MY OWN re-execution case-by-case 8/8**: actual
  verdict, full checker_detail string, buffer_len, buffer_hex, buffer_sha256, expected, match flag.
- Static structure verified ON CODE LINES (module docstring excluded via its ast end_lineno — the
  docstring quotes the NC2/NC3 raise statements verbatim and would otherwise masquerade as code):
  - NC1 `_reject_sib` def @line 221; guard call sites @lines [245, 287, 299, 328] — one per
    memory-ModRM branch (0x8B/0x89/0x8D, 0x84, 0x83, 0xFF), each after `_modrm` and before the
    branch's first length computation;
  - 0x84 branch: header @285, `_modrm` @286, NC1 guard @287, **NC2 raise @289 BEFORE the length
    assignment `size = 2` @291**; the sibfixed memory length table
    (`size = 2 if mod == 0b11 else (3 if mod == 0b01 else 6)`) is **REMOVED** — that removal IS the
    NC2 correction (explicit sub-check: True);
  - **NC3-B raise @247 BEFORE the LEA operand formatting @282** (anchored to the LEA's own
    `mn = "lea"` sub-branch);
  - checker catch @353 is only `(ValueError, IndexError)`; no `except Exception` anywhere.
- MY engine self-falsifiers (functional, honestly labeled SELF-CHECK — PE-MASTER audits it
  independently): FF F7 and FF D8 raise (/3 removed), FF F0 raises (/6 NOT added), FF D2 decodes as
  `call edx` (/2 kept), 8D C0 raises, 8D 06 decodes (memory LEA kept), 84 06 raises, 84 C0 decodes
  as `test al, al` (register TEST kept) — all as required.

## 5. Clean-window boundary regression (G3: PASS)

MY independent decode of the re-derived clean window produces the SAME 22-instruction VA/size map
as the published record (maps identical; total 0x42 = 66 B): head 8B F8 `mov edi, eax` @0x0050A3B7
exact, final push 57 `push edi` @0x0050A3F6 exact, join call FF D2 `call edx` @0x0050A3F7 exact;
the map is also identical to the POST.json measured map; window arithmetic recomputed on MY
decoder (call rel32 targets 0x006C0F90 / 0x006C10B0 / 0x0050A1E0 / 0x005246E0; je/jmp rel8 targets
0x0050A3C8 / 0x0050A3CC). The NC2/NC3 corrections altered NO clean boundary.

## 6. Nine historical SIB negative cases (G4: PASS)

The 9-form battery was re-derived SAFELY from the READ-ONLY historical QC script via
**ast.parse + ast.literal_eval of the SIB_BATTERY constant** — literal-only evaluation, ZERO code
execution; the historical top level (which writes QC_RESULTS.json) was NEVER executed or imported.
All nine forms are rejected fail-closed BY BOTH decoders at the DECODER level 9/9
(mine via the mem_dlen NC1 guard (0x8B/0x89/0x8D/0x83) and the register-only non-11 raises
(0x84/0xFF); production via its _reject_sib guard). Honest mechanism note: for the SIB TEST form
(84 04 24) production reports the NC1 SIB guard (it runs first) while mine reports its single
memory-form rejection — both fail-closed before any length computation; per-row messages recorded.

## 7. 144-form Desktop sweep (G5: PASS)

6 opcode branches (8B/89/8D/84/83/FF) × 3 memory mod (00/01/10) × 8 reg, always rm=4 → 144
synthetic SIB forms (full SIB/disp bytes, so a missing guard would DECODE rather than raise — the
sweep genuinely exercises the rejection predicates). **All 144 rejected AT THE DECODER LEVEL by
BOTH independent decoders (mine 144/144, production 144/144; 288 decoder calls).** My form set is
identical to the cited Desktop production-engine sweep (144 forms) AND to the POST.json raw_forms.
Honest mechanism note: for 0x83 mod=00/10 my engine raises at its uncovered-mod check while
production raises at the SIB guard — both fail-closed before any length computation; per-branch and
per-row mechanisms recorded in QC_RESULTS.json.

## 8. NC2/NC3 rejection mechanisms + instruction-level diagnosis (G6: PASS)

Decoder-level rejection evidence for the four reject cases, each pinpointed at 0x0050A3DD by
prefix decode (the 38-byte prefix before the mutation span decodes cleanly on both engines — the
rejection happens exactly AT the span, not by an accidental earlier parse error):

| case | MY engine rejection | production rejection |
|---|---|---|
| NC1_SIB_HIDDEN_EDI_WRITE | ValueError: SIB memory form rejected fail-closed (mod=10, rm=100) before any displacement/length computation — NC1 guard | ValueError: unsupported SIB form (mod=10 rm=100) — FAIL CLOSED |
| NC2_NON_SIB_TEST_HIDDEN_EDI | ValueError: uncovered test memory form (mod=00) — fail-closed (NC2) | ValueError: unsupported memory TEST form (mod=00) — FAIL CLOSED |
| NC3_INVALID_FF_FAR_CALL_REGISTER | ValueError: uncovered FF /3 mod=11 — fail-closed (NC3-A: only /2 call supported) | ValueError: uncovered FF /3 mod=11 |
| NC3_INVALID_LEA_REGISTER | ValueError: unsupported LEA register form (mod=11) — fail-closed (NC3-B) | ValueError: unsupported LEA register form (mod=11) — FAIL CLOSED |

In all four cases both checkers return the controlled (False, diagnostic) verdict — never a
TypeError, never a PASS. Zero unexpected exceptions across all 16 matrix rows.

**Instruction-level diagnosis (CITED Desktop reference decode — NOT a new measurement by this QC;
nothing installed; source: CONTROL_COUNTERCHECKS.json residual_tests, SHA256 AD8DC205…EE6BCC28D):**
- **NC2**: Desktop capstone 5.0.7 (66 decoded bytes) shows the TRUE span decode:
  `84 06` @0x0050A3DD = 2-byte `test byte ptr [esi], al`; `BF AA BB CC E8` @0x0050A3DF = 5-byte
  `mov edi, 0xe8ccbbaa` — an **EDI WRITE inside the prohibited P2 interval (0x0050A3B7, 0x0050A3F6)**
  (Desktop `edi_writes_in_required_interval = ["0x0050A3DF"]`); tail 90 ×5 nops → the TRUE expected
  verdict is FAIL. The historical sibfixed length table assigned 6 bytes to `84 06`, consumed
  `84 06 BF AA BB CC` as one TEST, then decoded `E8 90 90 90 90` as a CALL — the EDI write was never
  decoded and the checker FALSE-PASSED (Desktop residual: production ok=true on this buffer — the
  false pass; independent ok=false). I statically confirmed the defect mechanism at source level
  (sibfixed line 236: `size = 2 if mod == 0b11 else (3 if mod == 0b01 else 6)`), and the executor's
  PRE reproduced it on the AST-extracted real historical functions (production PASS / QC FAIL).
  The corrected production now rejects EVERY memory TEST form before any length computation.
- **NC3-A (FF D8)**: Desktop capstone decodes only the 38-byte prefix (stops at FF D8): FF /3 is
  CALLF m16:32 — a memory-only form; `FF D8` (mod=11) is an INVALID register encoding (undefined).
  The historical internal-QC engine accepted FF D8 via its erroneous /3 branch as a harmless
  2-byte `push eax` and FALSE-PASSED the buffer (the NC3-A defect — executor PRE: internal_qc
  PASS); the historical production already rejected it (`uncovered FF /3 mod=11`) and the
  successor keeps that behavior UNCHANGED; my successor removes the /3 branch. No FF /6 or other
  forms were added on either side (verified functionally: FF F0 raises on both engines).
- **NC3-B (8D C0)**: LEA with mod=11 is an INVALID x86 encoding (Desktop capstone likewise stops
  at 38 bytes). The historical sibfixed production crashed inside LEA operand formatting
  (`TypeError: unsupported format string passed to NoneType.__format__` — memoff None), which
  escaped the (ValueError, IndexError) catch (Desktop residual production exception; executor PRE
  reproduced it as ERROR:TypeError); the historical internal-QC engine formatted it as a harmless
  `lea eax, eax` and FALSE-PASSED (executor PRE: internal_qc PASS). Both corrected engines now
  reject it explicitly BEFORE operand formatting → controlled (False, diagnostic).

## 9. Terminal gate values (all conditions individually recorded in QC_RESULTS.json)

| gate | measured value | result |
|---|---|---|
| G1 16-row matrix | 16/16 rows match required (8 cases × 2 engines); production fixture byte-identical to my re-derived window | PASS |
| G2 production authenticity | SHA 68BEC1AE…4D9F13 == pin == POST declared; 8/8 POST rows equal my re-execution (verdict+detail+buffer identity+expected+match); static structure on code lines; 8/8 self-falsifiers | PASS |
| G3 clean map regression | my VA/size map == published map == POST measured map; 22 instructions; total 0x42 (66 B); P1/P3/P4 exact; rel32/rel8 arithmetic recomputed OK | PASS |
| G4 nine SIB cases | 9/9 rejected by BOTH decoders at decoder level (battery ast.parse+literal_eval re-derivation; historical top level never executed) | PASS |
| G5 144-form sweep | 144/144 rejected by BOTH decoders at decoder level (mine 144, production 144); form set == cited Desktop sweep == POST raw_forms | PASS |
| G6 NC2/NC3 mechanisms + exceptions | mechanisms explicitly recorded for cases 5–8 on both engines, each pinpointed @0x0050A3DD by prefix decode; 0 unexpected exceptions in 16 rows; no TypeError escape | PASS |

**QC_VERDICT = PASS** (G1..G6 all PASS). Per the frozen wording:
**NC2/NC3 = CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE** (this positive gate is the required
precondition; scope = the eight-case matrix, the nine-form battery and the 144-form sweep).
**NC1 = CLOSED_FOR_AUDITED_STATE for 91598a98** — unchanged historical status; historical results
remain authentic and unchanged. **NOT GENERAL_X86_DECODER_PROVEN** — never claimed; both engines
cover only the window's opcode universe and reject everything else fail-closed.

### QC repair round disclosure (1 of 1 allowed; on THIS QC's own tooling, NOT on the audited code)

The first QC run failed G2 on my own static structural check: (a) plain substring search matched
the production module DOCSTRING's verbatim quotes of the NC2/NC3 raise statements (prose lines 33/46)
instead of the real code lines (289/247), and (b) the predicate searched for the sibfixed 0x84
memory length table which the NC2 correction REMOVED BY DESIGN — a false FAIL of MY check, not a
defect of the audited production module (all other G2 sub-flags — SHA, 8/8 row equality,
self-falsifiers — were already PASS). Repair: docstring excluded via its ast end_lineno; 0x84
branch anchored and scanned as header → _modrm → NC1 guard → NC2 raise → `size = 2` assignment;
explicit "memory length table removed" sub-check; LEA formatting anchored to its own
`mn = "lea"` sub-branch. The check remains falsifiable (no guard weakened). **After the repair the
ENTIRE QC was re-executed from scratch** (all 8 input identities re-measured, 16-row matrix, G2–G6
and all supplementary controls re-measured; no stale PASS copied from the first run).

## 10. Supplementary controls (recorded, NOT gate conditions — all hold)

- Production register-form battery re-executed by THIS QC: 6/6 positives decode exactly as before
  (8B F8, 8B C0, 89 C8, **84 C0 register TEST**, **8D 06 memory LEA**, **FF D2 call edx**) and 4/4
  negative controls raise with the expected mechanisms (84 06 memory TEST; 84 44 24 00 → SIB guard
  first; 8D C0 LEA register; FF D8 FF /3) — the correction did not over-reject any required form.
- PRE transcription fidelity: the executor's SOURCE_DESKTOP_MEASUREMENT is a VERBATIM (deep-equal)
  transcription of the pinned Desktop residual_tests 3/3 — SOURCE_DESKTOP_MEASUREMENT and
  EXECUTOR_REPRODUCTION properly separated, no relabeling.
- PRE internal consistency: every per-case PRE_REPRODUCED flag true and every actual equals its
  expectation 16/16 (historical NC2 production false-PASS, NC3 FF D8 QC false-PASS, NC3 LEA
  production ERROR:TypeError captured as ERROR — never recorded as FAIL); the historical defect
  mechanisms were additionally confirmed statically by THIS QC's full read of both historical
  scripts (sibfixed 318 lines; qc_ind_ctrl_sib_own 851 lines).

## 11. Coverage / NOT_CHECKED

**FULL_READ_LOG** (read to EOF): ctrl4_exact_endpoint_nc23fixed.py (377), run_nc23_matrix.py (1032),
CONTROL_RESULTS_POST.json (1977), CONTROL_RESULTS_PRE.json (1483), SOURCE_STATE.md (130),
INPUT_IDENTITIES.md (120), qc_ind_ctrl_sib_own.py (851), ctrl4_exact_endpoint_sibfixed.py (318),
JOIN_WINDOW_50A3B7_REPIN.txt (53); Desktop CONTROL_COUNTERCHECKS.json — residual_tests (3 cases) +
sib_branch_sweep (288 rows) verified programmatically against the SHA-pinned file. Every
load-bearing component of this QC's gates was read or machine-verified; nothing load-bearing is
NOT_CHECKED.

**NOT_CHECKED (explicit)**: FUN_006C9700 / FUN_006C8BB0 and any new function bodies/windows
(forbidden); the four intervening callee bodies (EDI preservation across them rests on the MSVC
callee-saved-register ABI — SUPPORT, NOT PROOF; unchanged historical limitation); model/root
semantics, transform writers, CMO/ACLD joins, VFS/BNT/NIF, game payloads, runtime, network channel
(out of scope); Desktop CC prose sections beyond residual_tests/sib_branch_sweep (citation only);
git commit/push/manifest/AUDIT_ENTRYPOINT publication (parent phase — this QC performed NO git
operations).

## 12. Open findings

**NONE.** No material finding against the executor phase survives this QC: the corrected
production module, its POST matrix and regressions A–D, the PRE reproduction and the persisted
identities all revalidated independently. The only defect found during this QC was in MY OWN first
structural-check predicate (disclosed in §9; repaired within the single allowed round; the audited
code was never modified).

## 13. Status preservation (verbatim)

- NC1 = CLOSED_FOR_AUDITED_STATE for 91598a98
- NC2/NC3 = CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE (only after a positive gate; never
  GENERAL_X86_DECODER_PROVEN)
- MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32 (MIN preserved); EXACT = UNRESOLVED
- MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7 (MIN preserved); EXACT = UNRESOLVED
- ORIGINAL_SCOPE/BUDGET_COMPLIANCE = FAIL
- RETROACTIVE_PRIOR_AUTHORIZATION = NO
- WRAPPER_DEPTH = UNRESOLVED
- HISTORICAL_LINEAGE_BUDGET_CHARGE = 2/3
- CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
- MODEL_ROOT_RELATION = UNKNOWN
- CHILD_VISUAL_ROLE = UNRESOLVED
- CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED
- EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (scoped to examined ACLD+0x18 SF instance)
- JOIN_OPERATION = STRONGLY_SUPPORTED
- CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND
- WORLD_INSTANCE = NOT_ESTABLISHED
- WORLD_XYZ_RECOVERED = NO
- SOURCE_DESKTOP_POST_AUDIT = PERFORMED_FOR_91598a98
- NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED
- CANONICAL_GATE_EFFECT = NONE

This QC changes validation machinery only; it creates no science and retracts no historical
result. Publication (SUPERSESSION, FINAL_REPORT, PE_MASTER_REVIEW, HANDOFF, MANIFEST, commit/push,
live remote verify) belongs to the parent, not to this QC.

## 14. Files written by this QC (exactly 3, all inside OUTPUT_ROOT; nothing else touched)

| file | size (B) | SHA256 |
|---|---|---|
| 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_nc23_own.py (this QC's own decoder+checker+gates; executed with `python -B`) | 71164 | 31B610745AD4C991237FA36CE197BFA3AA423C9F0530D79FF1664592CA50A703 |
| 00_CONTROL_INTERNAL_QC/QC_RESULTS.json (machine-measured evidence + every gate condition) | 120193 | 900EF2273ECFA9F125106786522E24CF58C3B3881A889AA68AF10C5BC415D397 |
| QC_REPORT.md (this report) | (recorded in the handoff after write) | (recorded in the handoff after write) |

Zero `__pycache__` / `.pyc` residue under OUTPUT_ROOT and the READ-ONLY SOURCE_PACKAGE
(verified). Executor artifacts, historical packages and AUDIT_ENTRYPOINT.md untouched. No git
operations, no EXE access, all buffers synthetic/in-memory.
