# REPORT.md — P02_CONTINUATION (Etap B: transform continuation at 0085C130)

AUTHOR: PE-MASTER_DIRECT_ANALYST_FALLBACK (two empty worker sessions; zero disk output verified twice; contract section 10 fallback with attribution). Evidence: P02_EXTRACT (99 rows, admission A36c825b21b5c) + frozen R2 P04 + new P01_CALLER. Zero new admissions.

## 1. Findings

1. **0085C130 dispatches 0085BFA0 on the SAME receiver** (ECX unchanged from entry through 0085C13B) and on ITSELF downstream (this+0x30 = the 13-dword transform field that the P01 caller 00527AA0 fills from a previous 0085BFA0 output copy). This strengthens the single-receiver thread: 00527AA0 -> 0085BFA0 -> copy to receiver+0x30 -> 0085C130 -> 0085BFA0 again + 0096CD10(this+0x30). [CONFIRMED, dataflow]
2. **Two blend/lerp-style trios, same factor S1=arg2(float)**:
   - L1 = [ESI+0x54/0x58/0x5C] + S1*(OUT[+0x20/+0x28/+0x2C] - [ESI+0x54/0x58/0x5C]) — owner fields blended toward three floats (CORRECTED_PER_QC_F1: out-buffer slots +0x24/+0x28/+0x2C, continuous; first FLD before the PUSH shifts ESP) from the fresh 0085BFA0 output.
   - L2 = v + S1*(u-v) — a trio produced from the stored transform (this+0x30) via 0096CD10 blended toward a trio from the fresh output via the same helper.
   Working labels only. NOT named position/rotation/matrix/world transform.
3. **Critical conditional**: u and v are zeroed BY THE CALLER before each 0096CD10 call and read AFTER; if 0096CD10 does not write its out-trio, u=v=0 => w=0 => L2 = v(=possibly 0). L2 content is therefore CONDITIONAL_ON_OPAQUE_CALLEE. 0096CD10 body unopened (out of admitted window; opens would need new admission of [0096CD10..] body).
4. **0096D7C0 receives ECX=arg1 (caller-supplied pointer) with [&L2, &L1]**; 0085C130 returns arg1 itself. arg1's class and the consumer semantics are UNKNOWN.
5. ESP balanced; FPU depth 0 at RET; full push-shift re-basing done (STACK_MAP.md). Callee-cleanup for the 3 opaque CALLs is a labeled premise (no ADD ESP observed; balance collapses without it).

## 2. Answers to Etap B questions

- ORIGIN_OWNER_FIELDS [+54/+58/+5C]: read here as the "current" side of L1; writer not in window => UNKNOWN.
- TRANSFORM_SOURCE: within window, the transform data read by 0085BFA0 comes from receiver slot+0x24 data address (frozen R2 P04: 12 floats, 9 copies + 3 components + 1.0f shaped output). THIS WINDOW ADDS: the three OUT slots consumed here are +0x20, +0x28, +0x2C (non-contiguous: +0x24 skipped) — cross-check against frozen P04 layout naming (QC task). The first real data barrier remains: **who writes [receiver+0x2C] (slot+0x24 data-address holder) and where the 12 floats originate** (stream/record/cache/buffer unknown). Missing info: writer census of receiver+0x2C and of receiver+0x30; upstream storage feeding the slot+0x24 data address. Not obtainable from any currently admitted window.
- RELATIVE_VALUE_DATAFLOW: complete mechanical graph (STACK_MAP.md); write-order subtlety verified: L1 reads the S1*(C-O) trio at E-0x58/E-0x54/E-0x50 BEFORE the w=u-v block overwrites the same three slots.
- FPU/ESP: PASS (gates G01/G02/G11-claim C11).

## 3. Remaining barrier (exact missing information)

1. Writer of [receiver+0x2C] and provenance of the data-address it holds (the 12-float source).
2. Writer/first chronology of receiver+0x30 copy (P01 caller is ONE visible writer; earlier ones unknown).
3. 0096CD10 semantics (does it write u/v? what does it extract?) — body at 0x0096CD10, needs a new bounded admission to open.
4. 0096D7C0 semantics and arg1 identity.
No world-instance join established in this package; nothing here contradicts the frozen evidence.

