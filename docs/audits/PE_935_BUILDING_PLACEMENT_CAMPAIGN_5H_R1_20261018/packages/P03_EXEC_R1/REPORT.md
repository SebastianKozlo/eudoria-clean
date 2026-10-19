# P03 REPORT — Front A1 final micro-package (P02-B1): lookup stub 0x007B6C30 semantics

RUN_ID: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | PACKAGE: P03 | FRONT: A
Worker: pe-reconstruction (bounded micro-package, no delegation) | Started UTC: 2026-10-18T21:37:39Z (RUN_STARTED.json, real clock)
Region: 0x007B6C30–0x007B6C4B end-exclusive (14 rows, lines 959600–959613) | Admission: A6963eee83a5f
Source: GHIDRA_H5_VTABLE2.txt, SHA256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB, 50,780,146 B — re-verified 2026-10-18T21:37:49Z (Get-FileHash), matches pin, unchanged.
Context cited (not re-analyzed): P02_EXEC_R1/REPORT.md (leaf-action callsite shape: `PUSH 0x00A85460; MOV ECX,EBX; CALL 0x007b6c30`, receivers elem/[elem+0x24], sentinel guards; key arithmetic P02-C4).

## SCOPED RESULT (headline)

**0x007B6C30 is the entry GUARD + IN-FUNCTION DISPATCH of a single larger function — the admitted 14 rows perform a null-key check and dispatch; they contain ZERO memory writes and therefore CANNOT themselves write a binding. The pure-lookup vs get-or-create/register decision is NOT decidable from the admitted region: it lives entirely in the same function's continuation at 0x007B6C4B (jump target VA — reported for parent admission, NOT read).**

Decoded body (CONFIRMED, in-region):

```
007b6c30  PUSH EBX                       ; save callee-saved regs (3)
007b6c31  PUSH EBP
007b6c32  PUSH EDI
007b6c33  MOV EBP,ECX                    ; this = ECX (thiscall receiver)
007b6c35  MOV EDI,dword ptr [EBP+0x18]   ; READ M[this+0x18] — unconditional, BEFORE key test
007b6c38  XOR EBX,EBX                    ; EBX = 0
007b6c3a  SUB EDI,0x1                    ; EDI = M[this+0x18] − 1  (register-only; NO store back)
007b6c3d  CMP dword ptr [ESP+0x10],EBX   ; key (single by-value DWORD stack arg) vs 0
007b6c41  JNZ 0x007b6c4b                 ; key != 0 → continuation (SAME function)
007b6c43  POP EDI                         ; fast path (key == 0):
007b6c44  POP EBP
007b6c45  XOR EAX,EAX                     ;   EAX = NULL
007b6c47  POP EBX
007b6c48  RET 0x4                          ;   return; callee pops the 4-byte key arg
```

With the key and receivers from the P02 leaf action (all cited from P02):

- **Key 0x00A85460** (factory vtable 0x00A85454+0xC, P02-C4): in-region it is ONLY tested against zero, then left on the stack for the continuation to consume. Because 0x00A85460 is a non-null compile-time constant, **the JNZ is ALWAYS taken at both P02 callsites (006b1e36, 006b1e49) — both lookup calls ALWAYS enter the continuation at 0x007B6C4B; the in-region fast path is dead for the P02 leaf action** (P03-C5). The vtable-derived key remains a class/type-identity constant only — no receiver identity follows from it (premise preserved).
- **Receivers [elem]/[elem+0x24]**: thiscall `this` (ECX→EBP). The receiver is dereferenced at +0x18 UNCONDITIONALLY, before the key test — so even a null-key call requires a valid receiver (consistent with P02's sentinel guards). It is read (count-shaped member, `−1` = last-index idiom, PLAUSIBLE P03-C8), NEVER written in-region. No receiver write, no global write, no table write exists in the 14 rows.
- **Pure property lookup vs get-or-create/register**: in-region facts are consistent with BOTH candidates (CAND-P3a lookup; CAND-P3b register). The guard shape (null key → NULL, no create) is orthogonal to miss-handling. A get-or-create continuation would write the binding (entry insert + possible count update at M[this+0x18]) — the P02 countermodel "the leaf action itself WRITES the binding through the callee" remains live and is decided ONLY at **0x007B6C4B** (P03-B1).

## EVIDENCE MAP

| Claim | Statement (short) | evidence_level | claim_resolution |
|---|---|---|---|
| P03-C1 | 14 rows, 1 entry, 0 CALL, 2 edges, 3 reg-saves, ZERO memory writes | CONFIRMED | factual |
| P03-C2 | thiscall: ECX=this, one by-value DWORD stack key @ [ESP+0x10], RET 0x4 (stack-balance derived) | CONFIRMED | factual |
| P03-C3 | Null-key fast path returns NULL, no table access/create; [this+0x18] read BEFORE the test | CONFIRMED | factual |
| P03-C4 | EDI = M[this+0x18]−1 register-only, live-in to continuation | CONFIRMED (rows) / PLAUSIBLE (continuation-use) | factual + CONDITIONAL |
| P03-C5 | Key 0x00A85460 ≠ 0 ⇒ JNZ always taken at P02 callsites; in-region path dead for them | CONFIRMED | factual (cited callsites) |
| P03-C6 | MAIN: in-region = pure guard+dispatch, cannot write a binding; full-function lookup-vs-register NOT_ESTABLISHED; target VA 0x007B6C4B | CONFIRMED (in-region) / UNVERIFIED (full function) | factual (a) + NOT_ESTABLISHED (b) |
| P03-C7 | CAND-P3a pure lookup (PLAUSIBLE overall) vs CAND-P3b get-or-create/register (UNVERIFIED, not excluded) | STRONGLY_SUPPORTED/PLAUSIBLE vs UNVERIFIED | CONDITIONAL (both live) |
| P03-C8 | M[this+0x18] PLAUSIBLY an entry count ({data,count}-pair shape analogy; NOT class identity) | PLAUSIBLE | CONDITIONAL |
| P03-C9 | Navigation census: 32 direct CALL rows to 0x007b6c30 in saved listing (incl. the 2 P02 callsites) | CONFIRMED (count only, navigation) | factual |

Full statements, premises, countermodels: CLAIMS.json. Register/stack identity map: MEMORY_AND_IDENTITY.json.

## COUNTERS: actual vs reserved

- Bodies: **1 actual / 1 reserved** (single logical function, entry 0x007B6C30; continuation 0x007B6C4B is the same body).
- Instruction rows: **14 actual / 14 reserved** (lines 959600–959613, line parity exact; region end-exclusive at 0x007B6C4B).
- Edges: **2 actual / 2 reserved** (E1 JNZ→0x007B6C4B recorded-not-read; E2 fall-through epilogue→RET 0x4).
- CALL sites: **0 actual** (contract main_question itself states "0 CALL"; the reserve field "edges: 2" was rendered as "2 CALL" in the dispatch prompt/cap-note — actual CALL contribution to Front A's 64-CALL budget is 0; per §6 reservations are not refunded, the conservative ledger entry stands).
- Candidates: **2 actual / 2 reserved** (CAND-P3a, CAND-P3b).
- Front A after P03: **6/16 bodies, 386/1800 rows, 42/64 CALL, 8/12 candidates**. Campaign totals: 6/96, 386/12000, 42/320, 8/48.

## GATES

See GATES.json. RUN_STATUS: COMPLETED (all contract-required outputs materialized; wall respected; no forbidden access; jump target reported not read; MANIFEST last, self-excluded).

## HONEST LIMITS

1. **Region scope:** every "cannot write" statement is scoped to the 14 admitted rows (explicit-store level). The continuation at 0x007B6C4B is opaque from here; lookup-vs-register (CAND-P3a vs CAND-P3b) is NOT resolved by this package — that is the precise remaining edge (P03-B1).
2. **Single-body note:** the JNZ target 0x007B6C4B is the continuation of the SAME logical function (entry 0x007B6C30), not a separate callee. A new admission for 0x007B6C4B+ extends this body — no second body should be counted (parent contract §6).
3. **Incidental navigation exposure (disclosed):** the Grep address search used to LOCATE the region returned 49 rows: 32 direct-CALL reference rows elsewhere (single rows, no surrounding bodies opened — reported only as navigation context P03-C9), the 14 in-region rows, and 3 boundary/continuation rows (0x007b6c4b, 0x007b6c4d, 0x007b6c4e) that matched the search pattern because the JNZ target sits exactly at the end-exclusive boundary. NO semantic analysis was performed on those 3 rows and NO claim depends on their content; the jump-target report derives from the in-region JNZ operand (row 959608). Flagged for parent QC as a disclosed side effect of permitted address-search navigation.
4. **Compiler-DCE premise:** "the continuation consumes EDI/EBX" rests on the standard optimization premise (an unused load+sub would be eliminated); this is PLAUSIBLE, not in-region fact. The count interpretation of M[this+0x18] (P03-C8) is an idiom reading, hedged; the receiver's class/layout identity is UNKNOWN.
5. **Premises preserved:** no direct-caller census claim of virtual/exclusive dispatch (P03-C9 is navigation only); vtable-derived key ≠ receiver identity (no identity inference made); explicit-store absence ≠ final-value claims after the opaque continuation (none made).
6. **Out-of-region targets:** 0x007B6C4B recorded as VA only. No other out-of-region target exists in the region (the only other exit is RET 0x4 to the caller).
7. No EXE/payload/runtime/Ghidra-export/old-script/config/skill/frozen-root/repo access in this package; EXE_READ_BYTES=0, RUNTIME_ACTIONS=0, CONFIG_CHANGES=0.
