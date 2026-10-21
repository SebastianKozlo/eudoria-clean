# CALLER TRANSFORM BUFFER PRODUCERS - OPENCODE SAVED R1 (2026-10-20/21)

RUN_ID: PE_935_CALLER_TRANSFORM_BUFFER_PRODUCER_OPENCODE_SAVED_R1_20261020
RUN_STATUS: SEALED_SCIENCE_PENDING_PUBLICATION (see HANDOFF for final)
SCIENCE_VERDICT: PASS_WITH_EXPLICIT_LIMITATIONS (primary P0 answered; bounded negatives; QC_PARTIAL with coverage map)
PROCESS_VERDICT: WITHIN_NUMERIC_CAPS_WITH_RECORDED_DENIES (2 failed admission attempts recorded as DENY events; 0 incidents)

## 1. Question and answer

P0: which instructions/callees define the 13 dwords passed from the caller stack buffer via CALL@85A429 and where do the values come from?

ANSWER (admitted literals, continuous coverage 85A1B0..85A432 plus fully-covered callee bodies):

- Caller function entry: 0x0085A1B0 (MSVC SEH prolog, AND ESP,-8 alignment; frame base F = post-cookie-push ESP; this spilled to [F+0x14]).
- S := ESP before PUSH EDI@85A421 = F on both admitted paths (push balance literal-verified, incl. callee cleanups 7C3BB0 RET 0x4 and 857830 RET 0x14 on both exits). LEA EAX,[ESP+0x64] at ESP=S-4 yields S+0x60. Source buffer = [S+0x60,S+0x94) = [F+0x60,F+0x94), 13 dwords, last word [F+0x90].
- CALLEE CORRECTION: the CALL@85A429 target is 0x00857F90 (prior label "F858" rebound; complete literal CALL census: exactly 1 direct caller of 857F90 = this site; 0 direct callers of 85F858 in the pinned H5). ABI: ECX=this, arg1=buffer pointer, arg2=[F+0x10] (95D3C4 allocation or 0).
- Slot writers (all 13 explicit, single literal census over the continuous range):
  - i0..i8: REP MOVSD@85A228 copies the 9-dword block built by 7C3BB0(this=F+0xA0, arg=float const [0xA7AE30]): i0=1.0, i1=i2=i3=0.0, i4=H1(c), i5=H2(c), i6=0.0, i7=-H2(c), i8=H1(c). H1/H2 are IAT-thunked CRT FPU imports ([0xA75390]/[0xA75398]) - exact values UNKNOWN; the store structure [[1,0,0],[0,H1,H2],[0,-H2,H1]] (rotation-about-X-shaped) is CONFIRMED at store level, cos/sin identity only PLAUSIBLE.
  - i9 = raw M32[EBX+0x00], i10 = raw M32[EBX+0x10] (EBX=[EBP+0xC], the caller's stack arg2), i11 = 0x00000000, i12 = float 1.0.
- The double loop 85A331..85A413 (bounded by [F+0x18] outer / [F+0x38] inner, both = 1-ftol products, both data-dependent) is SKIPPABLE entirely by JBE@85A32B when [F+0x18]==0. The loop writes only through ESI (=95D3BE import result, stride [EDX+0xC]) - NOT tied to the source buffer (NOT_ESTABLISHED; positive exclusion blocked by opaque import).
- Callee 857830 receives pointers bracketing the buffer (F+0x3C/F+0x50/F+0x94/F+0x5C + const float arg2 overwritten at 85A3C3) but its fully-covered literal body (both exits RET 0x14) writes only [F+0x50],[F+0x54],[F+0x58],[F+0x94] (one-past-end) and [result2..+8] (opaque destination via 853BD0/4154F0). 857830_DIRECT_WRITES_SOURCE = REJECTED within proven premises; result2 chain remains UNKNOWN_MODREF.
- Bounded negatives: no other literal in-buffer write exists in the admitted denominator. Opaque chains carried as UNKNOWN_MODREF: 413440 (head absent from listing), 95D3C4/95D3BE (IAT thunk chain [0xA75354]), 857830 result2, import helpers. No-writer statements are scoped to the denominator.

## 2. Upstream (ETAP C) and frontier

12 of 13 words are constant-derived (const angle via imports, FLDZ, FLD1). The only data-dependent words (i9,i10) trace to the EBX object = stack arg2 of 85A1B0. 85A1B0 has ZERO literal direct callers in the pinned H5 (complete literal CALL census) - the provenance frontier is the virtual/indirect dispatch of 85A1B0. FIRST_MISSING_EDGE: caller/dispatch identity of 85A1B0 (would join the buffer to a concrete structure and could settle AABB-vs-transform). Resource-instance relation: UNKNOWN/NOT_ESTABLISHED; prior open edges unchanged (A==X UNKNOWN; X_store=X_entry CONDITIONAL; X<->R UNKNOWN).

Schema: 9+3+1 with scale-like 1.0 fits a transform-like record; i9/i10 asymmetric raw field copies ([EBX+0],[EBX+0x10]) and hardcoded i11=0 weaken a translation-vector reading; AABB-derived hypothesis (fields +0/+4/+0xC/+0x10 with subtractions) equally plausible. NOT established as NiTransform/world-space.

## 3. Model gate and sessions

OpenCode CLI 1.18.18 (runtime_version from DB session.version of all roles, per correction 6 - not a desktop label). Model gate PASS before science (saved_guard start --proof; MODEL_GATE.json pins coordinator ses_ea2b25e55ffezodvaQqzQ6N1B6, smoke ses_ea2b03266ffeDwZI0OdP0UDO2Y with SMOKE_INPUT SHA256 9B4B0060662446225170243011C8FAFE3038FCAE4DCD4CCBCF08DDF8E528B5F5 and micro-qualification T1-T4, probe ses_ea2afd518ffeyHCpyX8Q71RLyf). Effective client effort medium (merged scoped registry verified: glm-5-3 and glm-5-3-default both reasoningEffort=medium); REQUEST_EFFORT=NOT_OBSERVED; SERVER_EFFECTIVE_EFFORT=UNKNOWN. Same-model fresh contexts give separate review, not model independence.

## 4. Budget (from guard status, not hand-counted)

Charged (no refunds): 21 body reservations / 313 listing rows / 13 CALL / 10 candidate reservations. Union: 311 rows / 13 CALL (shared rows 1168622, 1165475). Caps 64/10000/400/64 respected. Events: 1 START, 10 ADMIT, 7 NAV, 2 DENY (failed admission attempts: J005-v1 plan missing; J007 NO_ROWS), 0 INCIDENT. J007 probe proved NO instruction rows exist in [85A414,85A419) - the JC@85A413 is the 6-byte long form ending at 85A419; coverage 85A1B0..85A432 is continuous.

## 5. Workers and QC

- W001 (pe-reconstruction, ses_ea29f40beffeCJAbu3N1hkrf4h): packets J001/J002/J005 (43 rows). Confirmed frame/ABI/7C3BB0/MOVSD with packet-limited conditional on the (separately covered) gap; its f1==f2 statement rejected (distinct thunked helpers), store structure accepted.
- W002 (pe-reconstruction, ses_ea29e89fbffe6DaQ3UkuCc5RBq): packet J003 (75 rows). Confirmed i9/i10/i11 raw copies, [F+0x38] write (correcting the coordinator - NC2), JBE condition, full write census of the window.
- QC001 (pe-master-auditor): first attempt EMPTY (finish=length, 0-byte text; saved WORKERS/QC001_EMPTY_ATTEMPT.md). One retry per contract with a smaller packet: ses_ea291867affe7JG5IPye0hPYpO, verdict QC_PARTIAL: L2 CONFIRMED (independent arg-map recount), P1 CONFIRMED, C1 STRONGLY_SUPPORTED (result2 not excluded - identical to claim caveat), L1 ESI-origin leg UNREVIEWED in-packet (covered by W002-delivered row; mapped in PACKET_COVERAGE.csv).
- INTERNAL_INDEPENDENT_REVIEW only (same model family); external Desktop post-audit PENDING.

## 6. Corrections (prior + new)

Corrections 1-6 from the START_PROMPT applied (see CORRECTIONS_APPLIED.json). New: NC1 label rebind F858->857F90 (census evidence); NC2 [F+0x38] write correction (worker W002); NC3 worker f1==f2 statement rejected.

## 7. Statuses

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. No original EXE/assets/runtime/memory were opened; saved listing only. Prior XSI statuses retained unchanged (A==X UNKNOWN; X_store=X_entry and C3B0 preservation CONDITIONAL).

## 8. Publication

Sanitized additive publication per CONTRACT section 11 is executed after seal (receipt root): new result + additive predecessor postaudit revalidation (PUBLISHED_DIFF_REHASH.csv + scope). Mandatory pub_manifest.py create + verify before push; no PASS = PUBLICATION_NOT_READY. Historical REPORTs untouched; 8f80190 never pushed. See RECEIPT_ROOT/PUBLICATION_RESULT.md for the outcome.
