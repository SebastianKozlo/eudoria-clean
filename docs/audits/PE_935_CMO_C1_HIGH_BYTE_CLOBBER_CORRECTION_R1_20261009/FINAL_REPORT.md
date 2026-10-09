# FINAL_REPORT — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

## 1. Run identity

| Field | Value |
|---|---|
| RUN_ID | `PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009` |
| RUN_CLASS | `MACHINERY_AND_CONTROL_CORRECTION` (correction-only; ZERO new science) |
| BASE_SHA | `34fc34749464de3e05527088ed46be9e215f1964` |
| OUTPUT_ROOT | `docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/` |
| Finding corrected | CMO-C1 / P2, from the independent Desktop post-audit of `PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009` (AUDITED_SHA 34fc347…) |
| Target | `Entropia.exe` (PCG_9_3_5) — 8015872 B / SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`, re-hashed after all EXE-touching work: UNCHANGED (executor + QC; reads limited to the approved windows W1/W2/W3 + the two RTTI chains) |

Contract identity: `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md` — 16623 B / SHA256 `61AAA55854942A22085F3767A7D64512248EDFAE3A7B9BB54A5CBE36F36D3981` — verified MATCH before any run work (executor, QC and persistence phases independently).

Delegation: executor = pe-reconstruction (executor phase); fresh-context internal QC by pe-master-auditor (QC worker phase); PE-MASTER MASTER_AUDIT + this persistence/publication phase = PE-MASTER direct dispatch, NO_NESTED_TASKS. No EXE access in this persistence phase.

## 2. Preflight (fail-closed; all measured)

- LOCAL_HEAD == origin/master == actual remote master (live `git ls-remote`) == `34fc34749464de3e05527088ed46be9e215f1964` — MATCH.
- Tracked working tree clean; OUTPUT_ROOT absent before work (created only after preflight PASS).
- All 4 mandatory source pins MATCH: `repin_write_provenance.py` 34043 / `45120C91AD6A94A79C56E9B06F1C035481FB99D3017688E7F589732BEC6EE931`; `qc_remeasure.py` 31970 / `4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B3E2F2E71B3EB5B3F3F8DDE1A`; `CONTROL_RESULTS.json` 18509 / `9545D0D78881C29BC805EA3A05C8AA936D364256671D31A1AE907677A63DE2F8`; `QC_RESULTS.json` 31350 / `DE7DF210FAFA465E27D7A7C4410C9D9C44C9BAE1492B9FEDE2B3101F01BF0545`.
- Contextual inputs independently hashed and recorded (INPUT_IDENTITIES.md): source FINAL_REPORT.md 15589 / `FF5FDBD2…`; CLAIM_MATRIX.csv 9721 / `1D32AADE…`; MANIFEST_SHA256.csv 5368 / `5F1CAE01…`; J3 SUPERSESSION.md 8339 / `DD11137A…`; AUDIT_ENTRYPOINT.md 269640 / `E707FCB7…` (governance input, read).
- Foreign untracked paths (5× `PE_935_*` packages + `experiments/`) recorded and LEFT INTACT.

## 3. Root cause (both facets, PRE-measured)

Both bounded x86-32 decoders of the historical package index the 32-bit GPR table with the byte-alias index when building the writes/reads sets of register-direct `MOV r/m8,r8` (opcode 0x88):

- Historical executor `repin_write_provenance.py` (34043 B / 45120C91…), `elif b0 == 0x88:` branch: `ins["writes"].add(REGS[mr["rm"]])` (line 174) and `ins["reads"].add(REGS[mr["reg"]])` (line 175) — R8 indices 4–7 (AH, CH, DH, BH) misfiled onto REGS[4..7] (ESP, EBP, ESI, EDI) instead of their true parents EAX/ECX/EDX/EBX.
- Historical QC `qc_remeasure.py` (31970 B / 4E5426AE…), `my_decode` 0x88 branch: the `GPR[mr["rm"]] if mr["rm"] < 4 else GPR[mr["rm"]]` conditional is a NO-OP (both arms identical, lines 214-215) — same writes-side defect.

**Facet 1** — wrong writes-parent for high aliases: `mov ch, bl` (88 DD; ModRM DD = mod 11, reg 3 = BL source, rm 5 = CH destination) is recorded with `writes=["ebp"]` (REGS[5]) instead of ECX; the operand STRINGS stay correct ("ch"/"bl"), so the defect hides behind correct text.

**Facet 2** — the historical QC never recorded register-direct byte-source parents at all (line 216 sets the `src` string only): `reads=[]` in every register-direct 0x88 case (PRE-measured 0/64).

Downstream consumer: the historical ECX-clobber scan over the reaching-definition interval (0x0085B24B, 0x0085B27A) lists writers of "ecx"; because the CH mutant is misfiled under "ebp", the scan returns [] — the provenance guard cannot see the clobber. Supplementary PRE evidence: an EBP-writer scan over the same interval on the CH mutant returns [0x0085B24D] — the clobber exists, it is merely misfiled.

Why the historical run did not catch it (measured, not an excuse): the examined 224-byte window contains NO physical register-direct 0x88 instruction and NO high alias — only the four memory-form `88 9E 9C/9D/9E/9F 00 00 00` (`mov [esi+0x9c..0x9f], bl`) and the 16-bit `66 89 9E A0 00 00 00`; their byte source BL is a LOW alias whose parent (EBX) coincides with REGS[3]. The defect was LATENT in the historical scope; it is exposed only by the synthetic high-byte counterexample.

## 4. PRE reproduction (immutable `00_PRE/`; historical implementations, AST-extracted, top-level NEVER executed)

Method: AST extraction of the historical decoder functions/constants (free-name sets verified; the historical scripts never imported as modules, never executed at top level — their main() writes into the historical package); the historical executor ECX scan (source lines 444-446) and the QC scan call (lines 508-509) transcribed VERBATIM with programmatic byte-for-byte source-line verification. All mutants are in-memory copies; the physical EXE was never modified.

| Case | Implementation | Mutation-site decode (MEASURED) | Verbatim historical ECX scan (0x0085B24B, 0x0085B27A) |
|---|---|---|---|
| PRE-EX-CLEAN | historical executor | `D9 E8` fld1, writes=[] | [] (TRUE no-clobber) |
| PRE-QC-CLEAN | historical QC | `D9 E8` fld1, writes=[] | [] (TRUE no-clobber) |
| PRE-EX-CH (88 DD @0x0085B24D) | historical executor | dst `ch`, src `bl`, text `mov ch, bl`, **writes=["ebp"]**, reads=["ebx"] | **[] — FALSE EMPTY = FALSE PASS** |
| PRE-QC-CH (88 DD @0x0085B24D) | historical QC | dst `ch`, src `bl`, **writes=["ebp"]**, reads=[] (source parent missing — facet 2) | **[] — FALSE EMPTY = FALSE PASS** |
| PRE-EX-CL (88 D9) | historical executor | dst `cl`, writes=["ecx"] (LOW-alias coincidence) | DETECTED @0x0085B24D |
| PRE-QC-CL (88 D9) | historical QC | dst `cl`, writes=["ecx"] (coincidence) | DETECTED @0x0085B24D |

All six cases decode 64 instructions ending exactly at 0x0085B290 (2-byte mutation in a 2-byte slot — length preserved).

Historical 8×8 alias census (64 register-direct `88 /r` mod=11 cases × 2 decoders, decoded under x86-32 rules against an independent reference table):

- Historical executor: writes-parent correct 32/64 (exactly the dest 0-3 AL/CL/DL/BL cases — by coincidence), wrong 32/64 (AH→esp, CH→ebp, DH→esi, BH→edi); reads-parent correct 32/64 (source 0-3), wrong 32/64; BOTH correct in exactly 16/64.
- Historical QC: writes-parent correct 32/64 / wrong 32/64 (identical pattern); register-direct source parent recorded **0/64** (missing in all 64 — facet 2).

The false PASS is reproduced in BOTH historical decoders from this run's own measurements (not quoted Desktop values): **PRE_EXECUTOR_FALSE_PASS_REPRODUCED = TRUE; PRE_QC_FALSE_PASS_REPRODUCED = TRUE.**

## 5. Corrected successors (explicit OLD→NEW mappings; both hashes)

| Role | OLD (historical, IMMUTABLE, not edited) | NEW (this package) |
|---|---|---|
| Executor decoder | `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/repin_write_provenance.py` — 34043 B / SHA256 `45120C91AD6A94A79C56E9B06F1C035481FB99D3017688E7F589732BEC6EE931` | `03_SCRIPTS/corrected_executor_decoder.py` — 20675 B / SHA256 `C9B553AA90D449871643D27C76F96BCFEB989ABDF20B0BADD1F8530868FCD2C5` |
| QC decoder | `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/qc_remeasure.py` — 31970 B / SHA256 `4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B3E2F2E71B3EB5B3F3F8DDE1A` | `03_SCRIPTS/corrected_qc_decoder.py` — 23454 B / SHA256 `88460076843BDA7DFD51BC1182422E1F98FF13EEC493F14304BACC92FA7B0919` |

The fix (opcode 0x88 only, both implementations): the byte-alias parent map AL→EAX, CL→ECX, DL→EDX, BL→EBX, AH→EAX, CH→ECX, DH→EDX, BH→EBX applied to the writes-set (destination) and the reads-set (source), both register and memory forms. Three properties distinguished per byte operand: exact byte-register operand NAME (dst/src strings preserved unchanged); PARENT GPR (writes/reads sets); actual WIDTH/bit-range (width 8; low aliases [0,8), high aliases [8,16)). A partial-byte write CLOBBERS the parent for reaching-definition purposes but is NOT a full 32-bit overwrite — recorded explicitly, the distinction preserved. Instruction lengths, ModRM/SIB interpretation, destination strings, text rendering and all other supported opcode behavior preserved unchanged; unsupported opcodes still fail closed (DecodeError / QcDecodeError). The decoders remain BOUNDED WINDOW decoders — this correction does NOT establish GENERAL_X86_DECODER_CORRECTNESS or GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED.

The corrected QC implementation is the QC worker's OWN independent implementation (no production helper import; the parent attribution is implemented arithmetically from the x86-32 encoding `parent(idx)=GPR[idx & 3]`, and its alias-matrix reference is an explicit literal table — a different construction than the decoder's helper, so a bug in either is caught by the other).

## 6. POST controls C1–C6 + AUX-1 (expected vs measured)

| Control | Expected (contract §6) | Measured (executor decoder; QC re-measured independently) | Verdict |
|---|---|---|---|
| C1 clean baseline | DECODE PASS; 64 insns; end 0x0085B290; D9 E8 @0x0085B24D; ECX_CLOBBER_AT_MUTATION_SITE=NO; CORE_VALUE_SOURCE=[arg1+8]; gate PASS | 64 insns; end exact 0x0085B290; site `D9 E8`; scan []; gate PASS; core [arg1+8] — QC's own decoder agrees | PASS |
| C2 CH mutant 88 DD | OPERAND=CH; WRITES_PARENT=ECX; bits [8,16); CLOBBER_SCAN DETECTED @0x0085B24D; VALUE_PROVENANCE_GATE=FAIL via the broken ECX reaching-definition ALONE | dst `ch`; writes ['ecx']; reads ['ebx'] (BL parent); bits [8,16); scan DETECTED @0x0085B24D; gate FAIL with failure_reasons exactly ['ECX_REACHING_DEF_BROKEN'] — every pin, the rel32 recomputation and the accessor check still PASS on the mutant (the SAME production provenance predicate as clean; no hard-coded mutant assertion) — QC's own decoder agrees | PASS |
| C3 CL control 88 D9 | ECX clobber DETECTED; same single-cause gate FAIL | dst `cl`; writes ['ecx']; bits [0,8); scan DETECTED @0x0085B24D; gate FAIL via ECX_REACHING_DEF_BROKEN alone — QC agrees | PASS |
| C4 alias matrix 8×8 | 64 cases per decoder vs an INDEPENDENT reference table; dest 8/8, source 8/8; 2-byte register-direct cases; low [0,8) / high [8,16) bits; partial-write vs full-32-bit distinction | Executor implementation 64/64 PASS (independent REF_BYTE8 table, no production helper import); QC implementation 64/64 PASS through its own decoder + its own explicit reference table → **128/128 decoder outcomes PASS** | PASS |
| C5 unrelated-parent negatives | A mutation writing another parent must NOT report ECX modified; correct parent attribution | Executor: 88 DF `mov bh,bl`→EBX; 88 DC `mov ah,bl`→EAX; 88 CE `mov dh,cl`→EDX (reads {ecx} — a byte READ never triggers the writer-based scan); 88 FF `mov bh,bh`→EBX — scans [], gate PASS; QC's own additional: 88 D4 `mov ah,dl`→EAX; 88 FB `mov bl,bh`→EBX — **6/6 PASS** | PASS |
| C6 historical scientific regression | All pins, both rel32 targets, both RTTI identities, 64-insn clean decode + exact boundary, field-level equality with the historical decoder, original receiver and value chain | 23/23 pins MATCH; rel32 @0x00528E8D → 0x0085B1B0 (+3351326) and @0x0085B27A → 0x00746560 (−1133855); RTTI 0x00A91E4C→COL 0x00AB33D0→TD 0x00B7997C→`.?AVMovableObject@@` and 0x00A7DCB0→COL 0x00AA17CC→TD 0x00B79958→`.?AVClientMovableObject@@`; 64 insns, end exact 0x0085B290; corrected executor table field-level EQUAL to the re-executed historical executor table on ALL 64 instructions (the fix invisible on the physical window); CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL | PASS |
| AUX-1 unsupported opcode | Controlled fail-closed, never silent acceptance | In-memory `0F B0` @0x0085B24D → UNSUPPORTED_FAIL_CLOSED (DecodeError / QcDecodeError, evidence preserved) | PASS |

The QC-lineage field-level comparison (corrected QC decoder vs re-executed historical QC decoder) shows the facet-2 fix on EXACTLY the four real memory-form `88 9E` instructions @0x0085B25B/0x0085B261/0x0085B267/0x0085B26D (`mov [esi+0x9c..0x9f], bl`), where the corrected decoder gains exactly {ebx} (the BL source parent) and loses nothing — zero unexpected differences.

## 7. The 128/128 alias-matrix completion

Units kept separate per contract §6 C4: 64 distinct instruction CASES per decoder (8 destinations × 8 sources, `88 C0|src<<3|dst`, all 2-byte), 2 implementations, 128 decoder OUTCOMES total (a synthetic alias matrix, not 128 provenance-path tests):

- Executor implementation: 64 cases, 64 outcomes PASS (dest coverage 8/8, source coverage 8/8 — each alias exercised as destination AND as source; testing all destinations against only BL was NOT done).
- QC implementation (independent decoder + own explicit reference table): 64 cases, 64 outcomes PASS.
- **ALIAS_DECODER_OUTCOMES = 128/128 PASS** (executor 64 + QC 64).

Per-case checks: exact destination/source operand; correct parent; writes-set == {parent}; correct 8-bit width; no false write to an unrelated parent; correct bit ranges (low [0,8), high [8,16)); partial-write-vs-full-32-bit distinction preserved.

## 8. Historical scientific regression (C6)

CORE_RESULT preserved: **CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL** — the selected store `89 4E 44` @0x0085B281 (mov [esi+0x44], ecx), receiver ESI = the FUN_0085B1B0 ctor this (base vtable 0x00A91E4C `.?AVMovableObject@@` stamped @0x0085B1C1; FUN_00528E50 stamps 0x00A7DCB0 `.?AVClientMovableObject@@` after return), value = *(arg1+8) via the pinned accessor FUN_00746560 (`8D 41 08 C3`, lea eax,[ecx+8]; ret) reached by call rel32 @0x0085B27A, producer `8B 08` @0x0085B27F — all re-verified by executor AND QC (own RTTI walks, own rel32 recomputations, own scans). No promotion beyond the original static scope: FIELD_SEMANTICS = UNVERIFIED; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.

## 9. QC (fresh-context internal QC)

- QC_ORIGIN = pe-master-auditor fresh-context internal QC, internal to PE-MASTER — NOT an independent Desktop post-audit, NOT executor self-review. QC_RUN_ID = `PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009_INTERNAL_QC_R1`.
- **QC_VERDICT = QC_PASS** — all 11 contract acceptance gates hold with the QC's OWN measurements (own AST extraction, own corrected decoder, own reference table, own RTTI walk, own mutants):
  1. PRE false PASS reproduced in BOTH old decoders = TRUE
  2. CH → ECX in BOTH new decoders = TRUE
  3. actual clobber/provenance predicate reached = TRUE
  4. clean retains no CH-related false positive = TRUE
  5. CL + complete alias matrix pass (128/128) = TRUE
  6. unrelated-parent negatives pass (6/6 incl. 2 QC-own) = TRUE
  7. original client bytes + source chain unchanged = TRUE
  8. no new science interpretation = TRUE
  9. QC independently reproduces the decisive failure case = TRUE
  10. documentation does not overclaim = TRUE
  11. manifest/indexes/historical immutability pass = TRUE
- QC SHA-index verification: PRE index 8/8 MATCH, POST index 11/11 MATCH (own re-hash); supersession token scan over all package files present at scan time: ZERO forbidden active standing (the single `SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC` occurrence is explicitly supersession-marked); J3 statuses carried verbatim 5/5.
- Per-duty PASS records with MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED are in `QC_RESULTS.json`.

### Process disclosures and PE-MASTER adjudication

**QC's 5 disclosed bring-up repair steps of its OWN tooling** (one session; intermediate states preserved in `repair_rounds_log`; zero executor artifacts touched; zero measured values altered): (1) a mistyped constant name (NameError); (2) a duty-G premise re-scope — the reads-equality-on-all-64 premise was impossible for the QC lineage (the historical QC never recorded register byte-source parents — CMO-C1 facet 2; a false alarm of the QC's own check, the executor was not at fault); re-scoped per facet with exactly the four documented exceptions; (3) scanner self-exclusion (the duty-J token scan flagged its own regex definitions — the same self-exclusion precedent the historical qc_remeasure.py applied); (4) a computed record not persisted (one missing assignment — regenerated); (5) a duty-J equals-form regex replaced by the authoritative semantic JSON field check. **PE-MASTER ADJUDICATION: NOT a violation of QC_REPAIR_ROUNDS_MAX=1** — that budget governs rounds of repairing the correction/records after QC; no correction defect was found or repaired; the disclosure is a process fact recorded in PE_MASTER_REVIEW.md.

**Executor's 3 disclosed process repairs (QC-adjudicated HONEST)**: (1) PRE regeneration with per-case records + a file-offset consistency formula fix (no measured value changed; the QC re-measured all six PRE cases independently — every value matches); (2) C5.4 test-data repair 0xF7→0xFF — the CORRECTED DECODER CAUGHT the executor's own test-data error (88 F7 = `mov bh, dh`, reads edx, vs 88 FF = `mov bh, bh`, reads ebx — the distinction independently confirmed by the QC's own decoder; positive evidence the fix works; only test data changed); (3) CONTROL_MATRIX presentation repair (expected-column wording; presentation-only). Plus one disclosed key-name cosmetics note in QC_RESULTS.json (duty-B `ecx_scan_(...)` vs duties C/D/F `ecx_clobber_scan_(...)` naming — no measurement impact).

## 10. PE-MASTER MASTER_AUDIT

**VERDICT = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION — PE-MASTER remains PROVISIONAL_UNTIL_QUALIFIED; CANONICAL_GATE_EFFECT = NONE).** PE-MASTER independently executed the corrected production decoder on its own in-memory mutant copies through the REAL provenance gate: clean → PASS; CH 88 DD → 'mov ch, bl', writes {ecx}, byte_dst_parent 'ecx', bits [8,16), partial_gpr_write, ecx_scan [0x0085B24D], gate FAIL; CL 88 D9 → writes {ecx}, bits [0,8), gate FAIL; BH 88 DF → writes {ebx}, ecx_scan [], gate PASS (unrelated parent, no false ECX). ALL MATCH the contract's expected semantics. Persisted VERBATIM as `PE_MASTER_REVIEW.md`.

**CORRECTION_VERDICT = PASS (all 11 acceptance gates, contract §11).** Full report: PE_MASTER_REVIEW.md.

## 11. Documentary supersessions (no historical rewrite)

- **CMO-C1 / P2 — RECORDED**: historical byte-register clobber coverage was insufficient; the corrected successor version now detects the high-byte alias counterexample (all tests pass, measured). The historical source package remains IMMUTABLE.
- **DOC-1 / P3 — BACKLOG**: `C3 + CC CC CC` is useful contextual boundary evidence but not independently sufficient to identify an arbitrary function start; for the examined function supported by the actual direct-call target (rel32 @0x00528E8D → 0x0085B1B0, re-verified) and earlier disassembly.
- **DOC-2 / P3 — BACKLOG**: historical M1–M6 = three byte mutations + two expectation/address controls + one receiver comparison — not six separate semantic mutation tests; wording discipline recorded (this run's own PRE/POST counterexamples are component-level decoder controls, not semantic mutation tests).
- **J3 standing preserved VERBATIM (no restoration, no reinterpretation):**

```
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE =
  MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN =
  NOT_QUALIFIED_BY_ORIGINAL_SCOPE

ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL
WORLD_XYZ_RECOVERED = NO
```

`SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC` remains SUPERSEDED as an active standing; no J3 restoration is made by this run.

## 12. Scope compliance (contract §9 — all zeros)

```
NEW_PCG_FUNCTION_BODIES = 0
NEW_PCG_SCIENCE_EDGES = 0
NEW_FIELD_SEMANTIC_INTERPRETATIONS = 0
NEW_RUNTIME_WORK = 0
NEW_NETWORK_RE = 0
NEW_PLACEMENT_RE = 0
NEW_MODEL_RE = 0
NEW_GAMEBRYO_OPENMW_RESEARCH = 0
```

EXE unchanged (rehashed by executor + QC); sibling stores +0x48/+0x4C byte-pinned ONLY, untouched; upstream arg1 chain NOT followed; no world coordinates/position units/building identities/coordinate frames/placement messages; no Gamebryo/OpenMW research. GENERAL_X86_DECODER_CORRECTNESS and GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED = NOT ESTABLISHED (bounded window decoders only). NEW_P0_P1_P2 = 0. UNRESOLVED_FINDINGS = the disclosed process items (non-material) + DOC-1/DOC-2 P3 backlog.

## 13. Terminal governance

```
SOURCE_DESKTOP_POST_AUDIT (CMO provenance run) = PERFORMED (the CMO-C1 finding's origin)
NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

Per contract §12/§13: RESULTING_SHA and REMOTE_SHA are recorded at the terminal handoff — not embedded in any file of this commit.

**WORKS != UNDERSTOOD. STOP BEFORE SCOPE EXCEED. ONE CORRECTION RUN ONLY.**
