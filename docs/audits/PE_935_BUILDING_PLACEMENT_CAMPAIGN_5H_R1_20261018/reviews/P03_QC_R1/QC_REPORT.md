# QC REPORT — P03_EXEC_R1 independent internal review (P03_QC_R1)

RUN_ID: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_P03_QC_R1_20261018 | ASSIGNMENT_MODE: INTERNAL_QC | OPERATOR: pe-master-auditor (fresh session, no delegation, NO_NESTED_TASKS)
TARGET (immutable): packages\P03_EXEC_R1 (admission A6963eee83a5f, region 0x007B6C30–0x007B6C4B end-exclusive, 14 rows = source lines 959600–959613)
PARENT LOOP: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | REVIEW WRITES: ONLY this directory | DEADLINE respected.
QC_VERDICT: **QC_PASS_WITH_CORRECTIONS** → PROCESS_VERDICT: **PASS_WITH_CORRECTIONS** (1 P2 wording/evidence-level correction; zero claim retractions; zero rejected overclaims).

## Method (independence statement)

Re-derived every load-bearing claim from the pinned saved source re-read directly by this reviewer (SHA256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB — re-hashed, matches pin, 50,780,146 B). The 14 region rows were re-read from source lines 959600–959613 and compared row-for-row with the worker's extract. Address searches outside the region were navigation only. All 13 package files, both package contracts, parent CONTRACT (§5, §6, §12), EVENTS 000004/000005 and the event hash chain were read/verified in full. Reviewer's own incidental-exposure disclosure: the navigation grep for `007b6c4b` returned one out-of-region match line (959614, `007b6c4b TEST EDI,EDI`); NO semantic analysis was performed on it and no claim in this review depends on its content — same incident class the worker disclosed.

## Accepted claims (independently re-derived; evidence_level = reviewer status)

| # | Claim (worker) | Reviewer re-derivation | Status |
|---|---|---|---|
| 1 | 14 rows / 1 entry / 0 CALL / 2 edges / 3 reg-saves / ZERO memory writes | Source lines 959600–959613 re-read: byte-identical parity; full decode-length continuity check of all 14 rows PASSES and shows RET 0x4 ending exactly at the end-exclusive boundary 0x007B6C4B; no CALL instruction; no memory-destination store (only the 3 register-save PUSHes as stack traffic, disclosed) | CONFIRMED |
| 2 | thiscall; key at [ESP+0x10] by value; RET 0x4 balanced | Re-derived stack arithmetic: 3 PUSHes (−0xC) ⇒ [ESP+0x10] = entry [ESP+4] = ARG1 = the single key DWORD; RET 0x4 pops retaddr+4 ⇒ balanced. CROSS-CHECK from the P02 caller (independently verified by reviewer in P02's region): `PUSH 0x00A85460; MOV ECX,EBX; CALL 0x007b6c30` with NO ADD ESP after the call ⇒ caller pushes exactly 1 arg and requires callee cleanup — caller-side and callee-side agree. Hidden-second-arg countermodel refuted | CONFIRMED |
| 3 | Unconditional read [this+0x18] BEFORE key test; register-decrement −1; NO store back | Row 959604 (`MOV EDI,[EBP+0x18]`) precedes the test row 959607 in a single straight-line block; `SUB EDI,0x1` (row 959606) is register-only; no store to [this+0x18] anywhere in the 14 rows | CONFIRMED |
| 4 | JNZ continuation at 0x007B6C4B; target recorded, not read | In-region operand (row 959608) + decode arithmetic (007b6c43+8=007b6c4b); reviewer confirms the target row was NOT semantically read by the worker (extract = exactly 14 in-range rows; G6 PASS) | CONFIRMED (edge fact; target semantics NOT_ESTABLISHED) |
| 5 | Both candidates (CAND-P3a lookup vs CAND-P3b get-or-create/register) remain NOT_ESTABLISHED | The 14 in-region rows contain no table access at all (only [this+0x18] read + key null test) — no in-region predicate discriminates the candidates; decision lives entirely in the continuation | CONFIRMED (as properly NOT_ESTABLISHED) |
| 6 | Key 0x00A85460 ≠ 0 ⇒ JNZ always taken at both P02 callsites; in-region fast path dead for them | Arithmetic + P02 callsite constants verified by reviewer in P02's region (rows 626560/626567) | CONFIRMED |
| 7 | P03-C9: 32 direct CALL rows reference 0x007b6c30 (navigation census) | Reviewer grep: 33 matches = 32 CALL rows + 1 entry row | CONFIRMED (count only; no semantic weight) |
| 8 | Counters 1/1 body, 14/14 rows, 2/2 edges, 0 CALL actual, 2/2 candidates; Front A after P03: 6/16, 386/1800, 42/64, 8/12 | Reviewer recount identical; Front A arithmetic MATCH (5+1, 372+14, 42+0, 6+2) | CONFIRMED |

## CONTRACT §12 checks

- **Full manifest re-hash + bijection: PASS.** All 12 censused entries match this reviewer's independent SHA256 re-hash; 12 censused + self-excluded MANIFEST = 13 disk files, no strays, no missing. Package CONTRACT.json is hash-identical to CONTROL\CONTRACTS\P03.json (BFF9E307…7D171).
- **Line parity vs pinned source: PASS** (14/14, byte-identical; decode continuity additionally confirms the region boundary is instruction-exact).
- **Alias/lifetime/vtable-boundary premise challenge: PASS.** No virtual-dispatch claim (P03-C9 navigation only); vtable-derived key ≠ receiver identity (applied — key treated as by-value constant, receiver class UNKNOWN); explicit store ≠ final value after opaque continuation (no store in-region, no final-value claim); scoped negatives keep bounds ("cannot write" = in-region explicit-store level; get-or-create countermodel live as P03-B1).
- **Actual vs reserved counters incl. no-refund handling: PASS.** Actual 0 CALL vs the reserve field "edges: 2" (rendered as "2 CALL" in the parent cap-note — a parent-side framing artifact; the contract main_question itself states "0 CALL"). The worker kept the 2-slot reservation un-refunded per §6, reported actual CALL = 0, kept Front A CALL at 42/64 (actual-based) with the encumbrance disclosed. Handling ASSESSED CORRECT.
- **Chronology vs EVENTS: PASS.** ADMIT 000005 (21:37:21.668Z) → contract (21:37:26) → RUN_STARTED (21:37:39) → source re-verify (21:37:49) → extract (21:39:20) → MANIFEST (21:40:27–43, honestly bounded); event hash chain 000003→000004→000005 re-hashed by reviewer — both links MATCH.
- **No semantic read beyond admitted regions: PASS** (see boundary incident below).

## Boundary-incident assessment (worker disclosure)

The worker disclosed that the region-locating Grep (pattern `007b6c3|007b6c4`) returned 49 rows: 32 direct-CALL reference rows, the 14 in-region rows, and 3 boundary/continuation rows (0x007b6c4b, 0x007b6c4d, 0x007b6c4e) that sit at/just past the end-exclusive boundary. Reviewer verification: **no claim depends on them.** Checked individually: the jump-target VA 0x007B6C4B derives from the in-region JNZ operand (row 959608), not from the exposed rows; continuation size is explicitly declared unknown ("the 3 incidentally-exposed navigation rows do not bound it and were not analyzed" — BARRIER_BACKLOG P03-B1); P03-C9 uses only the CALL-row count. The incident is properly classified as a disclosed side effect of permitted address-search navigation (COUNTERS/REPORT/GATES G4 PASS_WITH_DISCLOSURE/MANIFEST disclosures). No refund or retraction needed.

## Corrections

- **[P2] QC-P03-D1 — evidence-level tightening for the "same body" assertion.** COUNTERS.json (bodies note), HANDOFF.md and MEMORY_AND_IDENTITY E1 state "continuation 0x007B6C4B is the SAME logical function" flatly. Reviewer grade: **STRONGLY_SUPPORTED inference, not a byte-verified fact** — the supporting facts are excellent (the 3 pushed callee-saved registers are balanced only within this function's frame; live-in EBP=this/EDI/EBX; guard-jump-over-early-return shape; the JNZ target is exactly the next instruction boundary per decode arithmetic), but the target itself is unread and the worker's own CLAIMS already hedge the unread-continuation parts (P03-C4 PLAUSIBLE, P03-C6b UNVERIFIED). Effect: none on counters (1 body correct either way); the wording should keep the inference graded so the parent's future continuation admission does not inherit an unearned CONFIRMED. This is a documentation-grade correction for a future corrigendum — the frozen package was NOT modified by this review.

## Rejected overclaims

None. All claims carry correct evidence levels, countermodels and premises-preserved checks; "the 14 admitted rows CANNOT themselves write a binding" is correctly scoped to the in-region explicit-store level; lookup-vs-register is correctly NOT_ESTABLISHED with the decision localized to 0x007B6C4B.

## Precise remaining edge (P03-B1, sharpening P02-B1)

Admission of the continuation **0x007B6C4B+** (same source, same logical body per the STRONGLY_SUPPORTED frame-ownership inference — do not double-count the body per §6): decide by the continuation's miss-path store census — insert/write (+ possible count update at M[this+0x18]) ⇒ CAND-P3b register (the P02 leaf action would then WRITE the binding through this call); return NULL with no stores ⇒ CAND-P3a pure lookup. Also record: matched-entry structure, further jump/call targets (report, do not read), exit paths, return-value provenance. Continuation size is unknown from the admitted window (reserve conservatively).

## FULL_READ_LOG / NOT_CHECKED

See RECHECK_NOTES.json `full_read_log` / `not_checked`. No load-bearing component was left unchecked; NOT_CHECKED items are opaque-by-design (continuation 0x007B6C4B+), parent-owned (EVENTS 000001–000003 contents, REQUESTS/CHECKPOINTS) or cited-context.

## Sealed outputs of this review

RUN_STARTED.json (first write), RECHECK_NOTES.json, COUNTERS_RECHECK.json, QC_REPORT.md, MANIFEST.json (LAST, self-excluded — SHA256 recorded in the parent return, not here).
