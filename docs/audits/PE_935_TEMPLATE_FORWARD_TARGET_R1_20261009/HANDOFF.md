# HANDOFF — PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009

## MANDATORY HANDOFF BLOCK

- **AUDIT_OUTPUT_ROOT**:
  `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009\`
- **FINAL_REPORT_PATH**:
  `docs\audits\PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009\FINAL_REPORT.md`
- **PRIMARY_EVIDENCE_PATHS**:
  - `POINTER_DATAFLOW.json` (per-edge register traces, anchor body pins, classifications)
  - `CALLEE_FIELD_ACCESS_CENSUS.json` (every template-derived memory access, 11-field rows)
  - `CALL_EDGE_PROVENANCE.json` (all subject + anchor callsites, recomputed rel32 targets)
  - `FALSIFIER_RESULTS.json` (8/8 falsifiers, 4-part requirement each)
  - `INPUT_IDENTITIES.json` (all identity measurements before/after)
  - `01_RAW\OWN_DECODER_WINDOWS.json` (own decoder output, all windows incl. sentinel dump)
  - `01_RAW\F8_BODY_CROSSCHECK.json` (dual-decoder agreement: 451 insns, 0 disagreements)
  - `01_RAW\KEY_REGION_LISTINGS.md` (dual-verified listings of every decision region)
  - `01_RAW\OBJDUMP_LISTINGS\` (independent GNU objdump 2.44 listings)
  - `01_RAW\GHIDRA_HYPOTHESIS_EXPORT.json` (quarantined hypotheses only)
- **RUN_STATUS**: **COMPLETE** (all pre-registered windows decoded within budget; all 7 gates PASS; the 2 primary subject bodies and both bounded anchors fully analyzed; no scope expansion)
- **HARD_STOP_REASON**: NONE (no EXE SHA mismatch — identical before and after; no anchor identity mismatch — all callsites re-pinned at exact VAs; no budget exhaustion)
- **EXE SHA256 before**: E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
- **EXE SHA256 after**: E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (identical; size 8,015,872 B unchanged)

## PER-PHASE RESULTS

- **Phase 0 preflight**: PASS — git HEAD == origin/master == live ls-remote == BASE cea10e9;
  output roots created fresh (verified non-existent before); predecessor package reopened
  READ-ONLY and re-verified 25/25 rows against its manifest BEFORE and AFTER (0 mismatches);
  PREREGISTRATION.md written BEFORE all science; EXE + Ghidra-sandbox hashes verified.
- **Phase 1 calling convention + pointer identity**: PASS — caller conventions byte-derived
  (FUN_00511070 cdecl ≥3 params, ESI=param_1, EBP=param_3; FUN_006C3F50 cdecl 2 params;
  both subject callees receiver-only thiscalls, ZERO stack arguments, proven by their
  4-byte bodies); all three ECX provenance chains byte-traced with exhaustive
  writer/intervening-call censuses.
- **Phase 2 bounded callee analysis**: PASS — FUN_007CE1E0 = 4-byte getter `MOV EAX,[ECX+8]; RET`;
  FUN_0040B070 = 4-byte interior-pointer thunk `LEA EAX,[ECX+0x14]; RET` (NO memory access);
   complete field-access census with 4 direct rows + 7 store/forward rows + 11 rejection
   classes (class split per QC finding P2-1, records correction 2026-10-09: the corrected
   classifier re-run over all 135 memory-form operands yields unclassified=[] — see
   CALLEE_FIELD_ACCESS_CENSUS.json census_completeness_revalidation);
   NO field named; all semantics UNKNOWN preserved.
- **Phase 3 derived object test**: PASS (honest outcome) — the FUN_0040B070 result is
  P+0x14, an interior pointer of the SAME object; the reads 0x006C3FBE ([EAX+4]) and
  0x006C3FC1 ([EAX]) are actual field reads at [P+0x18] and [P+0x14]; no wrapper/handle;
  P's pointee-vs-node identity UNRESOLVED at window level (FUN_004D1430 body CLOSED).
- **Phase 4 adversarial validation**: PASS — 8/8 falsifiers executed (below).
- **Phase 5 output**: this package — 9 top-level documents + 14 files under 01_RAW/ = 23
  physical files; no MANIFEST/QC_REPORT —
  later phases; no AUDIT_ENTRYPOINT.md touch; no commit/push.

## PER-CALLSITE POINTER_IDENTITY CLASSIFICATION

| Callsite | Classification | Basis |
|---|---|---|
| 0x00511259 (FUN_00511070 → FUN_007CE1E0) | **POINTER_IDENTITY_CONFIRMED** | single writer MOV ECX,EAX @0x00511257; 0 intervening calls; branch-selected id 0x2DFA/0x2DF9; sentinel/NULL conditions recorded |
| 0x006C3F74 (FUN_006C3F50 → FUN_007CE1E0) | **POINTER_IDENTITY_CONFIRMED** | single writer MOV ECX,EDI @0x006C3F6E; EDI's only body writer = MOV EDI,EAX @0x006C3F67; 0 intervening calls |
| 0x006C3FB5 (FUN_006C3F50 → FUN_0040B070) | **POINTER_IDENTITY_CONFIRMED_CONDITIONAL** | direct path byte-confirmed (MOV ECX,EDI @0x006C3FAE; both paths cross CALL 0x006C3F74 first — byte-proven EDI-safe, the callee's open 4-byte body never writes EDI); vector-growth path additionally crosses CALL 0x006C2E00 @0x006C3FA9 (body CLOSED) — EDI survival across THAT call rests on standard callee-saved discipline, recorded as the condition [crossings census completed per QC finding P3-2, records correction 2026-10-09 — classification and condition unchanged] |

## DERIVED_OBJECT_IDENTITY + TRANSFORM_SEMANTICS

- **DERIVED_OBJECT_IDENTITY** = **INTERIOR_POINTER_SAME_OBJECT**: the FUN_0040B070 return at
  CALL 0x006C3FB5 is EAX = P + 0x14 (byte-proven LEA) — an interior pointer into the same
  object the lookup returned, NOT a new/wrapper/handle object. The reads at 0x006C3FBE/0x006C3FC1
  are therefore direct field reads of P at +0x18/+0x14 (resolves the predecessor's
  UNKNOWN-identity note).
- **TRANSFORM_SEMANTICS** = **UNVERIFIED**: zero FPU/SSE instructions in all six bodies
  (machine-measured); the consecutive dword pair [P+0x14],[P+0x18] and the dword [P+8]
  keep semantics UNKNOWN; NO coordinate/vector/transform claim made (falsifier F4 discipline).

## ALL EIGHT FALSIFIERS — OUTCOMES

1. **F1 (ECX ≠ lookup result at CALL)**: EXECUTED, PASS — E1/E2 single-writer chains;
   E3 growth-path condition honestly down-graded E3 to _CONDITIONAL.
2. **F2 (pointer = not-found sentinel)**: EXECUTED, PASS — sentinel path byte-pinned
   (JE @0x0072F59C → MOV EAX,0x00BA5800); sentinel = static-zero .data tail; callers
   never test it; all classifications conditional on it.
3. **F3 (field access belongs to another object)**: EXECUTED, PASS — full provenance census;
   5-dword struct-copy near-miss (base = 0x50CAF0/0x50D8C0 results) caught and rejected;
   the second FUN_007CE1E0 use @0x0051115B (non-template receiver) identified.
4. **F4 (float misclassified as coordinate)**: EXECUTED, PASS by demonstrated discipline —
   0 FPU/SSE in all six bodies; pair-shape NOT promoted; all field semantics UNKNOWN.
5. **F5 (call destroys assumed-preserved register)**: EXECUTED, PASS with E3 condition —
   in-window compiler corroboration: the save/reload pair 89 44 24 10 @0x006C3F83 /
   8B 4C 24 10 @0x006C3FBA proves the shipped code treats EAX as volatile across the
   growth-path call.
6. **F6 (return value misattributed)**: EXECUTED, PASS — last-writer attribution
   machine-verified; CAUGHT and CORRECTED the inherited "FUN_0040b070(0x8BD720)" reading:
   FUN_0040B070 takes NO stack argument; 0x8BD720 is prepared for the LATER 0x006C3640 call.
7. **F7 (claim rests only on Ghidra type)**: EXECUTED, PASS — zero load-bearing claims from
   Ghidra; concrete catches: getter signature artifact (the getter NEVER reads its stack
   arg), "FUN_008bd720" name artifact, and the corroborating (non-load-bearing) agreement
   of the 4-byte-body decompiles.
8. **F8 (boundary/target incorrect)**: EXECUTED, PASS — dual-decoder agreement over 451
   body instructions: 0 boundary + 0 call-target disagreements; 3 defects in MY OWN decoder
   caught by the objdump cross-check during calibration, fixed, and the entire pipeline
   re-run and re-measured BEFORE analysis.

## EVERY NOT_CHECKED ITEM (with reason)

- FUN_004D1430 body (would settle what the lookup's +0x14 arithmetic lands on — node vs
  object): NOT_CHECKED — outside pre-registered windows; no recursive opening (new bounded
  contract needed).
- FUN_006C2E00 body (would byte-verify EDI preservation on the E3 growth path):
  NOT_CHECKED — outside windows; recorded as E3's condition.
- FUN_006C3640 body (final consumer of [P+0x14],[P+0x18],[P+8]): NOT_CHECKED — outside
  windows; edge + exact argument mapping recorded.
- FUN_00414670 body (W_A consumer of [P+8]): NOT_CHECKED — outside windows.
- 0x0085B1B0 / 0x0095D3C4 bodies: NOT_CHECKED — contract-FORBIDDEN; edges/adjacent bytes only.
- Runtime object identity / any runtime behavior: NOT_CHECKED — STATIC_ONLY.
- Pointee contents of P / registry population path: NOT_CHECKED — UNRESOLVED_UPSTREAM
  (out of scope as in the predecessor).
- Whether FUN_00511070's param_2 is used inside the body: NOT directly referenced by any
  [ESP+0x16C]-class offset in the decode; its Ghidra-typed usage is a hypothesis only.

## INTERVENTION LEDGER (expected NONE — STATIC_ONLY)

- **Ghidra project reuse**: pre-declared in PREREGISTRATION §6 (LANDMARK4057 project,
  -noanalysis processing; its sandbox Entropia.exe re-hashed this run = physical hash,
  PASS). Counted as declared method, NOT an intervention. No re-import; no project state
  changed by this run beyond the headless read-only postScript execution (Ghidra saved
  the processed file state — its project timestamps may advance; no program bytes or
  analysis changed).
- **Decoder repair loop (disclosed under falsifier F8)**: 3 defects in my own fresh decoder
  were caught by the pre-registered independent objdump cross-check during calibration
  (before any analysis conclusion was drawn): (1) modrm wrapper tuple unwinding, (2)
  incomplete ALU-family table, (3) SIB index=4 "no index" meaning (+ a FS-prefix display
  fix). All were fixed and the ENTIRE pipeline re-run and re-measured; final state =
  0 disagreements. No analysis was based on defective decodes.
- **objdump slice extraction**: raw byte slices of the physical EXE written to SCRATCH
  only (never inside the package; the package contains text listings only).
- **No other interventions**: no runtime/network experiments; no package installations
  (capstone checked-absent, none installed); no tracked-file modification; no commits;
  no foreign untracked paths touched; python -B throughout, zero .pyc residue (verified
  by scan in this run's locations).
- **In-run script failures (honest)**: 3 trivial script crashes during tooling bring-up
  (JSON key name 'length' vs 'len'; an f-string quoting error; an instruction-before
  lookup keyed wrongly) — all fixed immediately, no analysis impact, scripts re-run clean.

## CLAIM LIMITS (verbatim, unchanged)

- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
- WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED
- WORLD_XYZ_RECOVERED = NO
- A negative result is acceptable and is reported without optimization toward a positive finding.

## 12-LINE SCIENTIFIC SUMMARY (what the template pointer actually is at each subject)

1. FUN_007CE1E0 @0x007CE1E0 is a 4-byte getter: `MOV EAX,[ECX+8]; RET` — the template pointer is DEREFERENCED at +0x8 by it (E1@0x00511259, E2@0x006C3F74).
2. FUN_0040B070 @0x0040B070 is a 4-byte interior-pointer thunk: `LEA EAX,[ECX+0x14]; RET` — NO dereference inside it; the template pointer is only address-shifted (E3@0x006C3FB5).
3. At E3 the caller immediately dereferences the returned interior pointer: [P+0x18] @0x006C3FBE and [P+0x14] @0x006C3FC1 — so the template pointer is dereferenced at +0x14 and +0x18 by the CALLER.
4. NO conversion: neither callee allocates, wraps, or indirections the template pointer into another object; the "derived object" of Phase 3 is P+0x14 — the same object.
5. NO key/handle use: P is never compared, hashed, or looked up in-window (the registry key is the id — the input side).
6. NOT stored: P itself is never written to memory anywhere in the windows — receiver-only, register-resident.
7. P's FIELDS are forwarded: [P+8] → vector pair (0x66,·) into the caller-owned vector + FUN_006C3640 arg6 (W_B); [P+8] → FUN_00414670 (arg2 @0x0051129C, arg3 @0x005112E4; W_A, path-conditional); [P+0x14]/[P+0x18] → FUN_006C3640 args 2/3.
8. RUNTIME OBJECT IDENTITY: NOT_ESTABLISHED (STATIC_ONLY — the client never ran).
9. TRANSFORM-RELEVANCE: NOT_ESTABLISHED — zero FPU/SSE instructions in all six bodies; the dword pair [P+0x14],[P+0x18] keeps UNKNOWN semantics; no promotion.
10. The lookup itself (FUN_0072F580, re-pinned) returns mapfind_result+0x14 on the found path (`83 C0 14` @0x0072F59E) and the sentinel 0x00BA5800 (static-zero .data tail) on not-found — callers never test the sentinel.
11. The getter (FUN_0043A550, re-pinned) NEVER reads its stack argument — the key stays on the stack and is consumed by the lookup's RET 0x4; Ghidra's param signature is an artifact (F7).
12. All of this is dual-verified (own decoder + GNU objdump 2.44, 0 disagreements over 451 body instructions; every CALL target recomputed from opcode bytes); claim limits preserved; nothing promoted.
