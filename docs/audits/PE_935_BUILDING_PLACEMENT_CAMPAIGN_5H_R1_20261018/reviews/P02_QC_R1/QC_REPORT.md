# QC REPORT — P02_EXEC_R1 independent internal review (P02_QC_R1)

RUN_ID: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_P02_QC_R1_20261018 | ASSIGNMENT_MODE: INTERNAL_QC | OPERATOR: pe-master-auditor (fresh session, no delegation, NO_NESTED_TASKS)
TARGET (immutable): packages\P02_EXEC_R1 (admission A0f2d2522b464, region 0x006B1E00–0x006B1FAC end-exclusive, 136 rows = source lines 626546–626681)
PARENT LOOP: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | REVIEW WRITES: ONLY this directory | DEADLINE respected (review window 21:42:36Z–21:58:00Z).
QC_VERDICT: **QC_PASS_WITH_CORRECTIONS** → PROCESS_VERDICT: **PASS_WITH_CORRECTIONS** (2 P2 documentation corrections; zero claim retractions; zero rejected overclaims).

## Method (independence statement)

Re-derived every load-bearing claim from the pinned saved source re-read directly by this reviewer (SHA256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB — re-hashed, matches pin, 50,780,146 B). Region rows were re-read from source lines 626546–626681 and compared row-for-row with the worker's extract. Address searches outside the region were navigation only. All 13 package files, both package contracts, the parent CONTRACT (§5, §6, §12), EVENTS 000004/000005 and the event hash chain were read/verified in full. Reviewer's own incidental-exposure disclosure: none for P02 beyond in-region parity rows (out-of-region targets were taken from in-region operands only).

## Accepted claims (independently re-derived; evidence_level = reviewer status)

| # | Claim (worker) | Reviewer re-derivation | Status |
|---|---|---|---|
| 1 | Line parity 136/136, lines 626546–626681 | Direct source re-read: byte-identical 136 rows; 136 consecutive lines; decode-length spot checks (JZ/JMP rel32 vs rel8 forms at 006b1e52/006b1e70/006b1e7f/006b1e2a) all consistent | CONFIRMED |
| 2 | Store census: exactly 7 explicit stores (deque insert @006b1e00, 4 frame stores @006b1e05/006b1ee8/006b1f07/006b1f3a, SEH restore @006b1f8d, result-flag clear @006b1faa) | Full 136-row memory-destination scan: exactly these 7, same VAs, same classes; 18 PUSH/5 POP/5 ADD ESP separately enumerated (convention disclosed by worker) | CONFIRMED |
| 3 | No [elem+8] store; only +8 access = LOAD @006b1ec8 | Verified: the only +0x8 operand is the load `MOV ESI,[EBX+0x8]` (line 626608) | CONFIRMED |
| 4 | No receiver/registration/global/ID store; no 0x42/66; no 296445 | Full immediate scan: constants present = 0xA85460(×2), 0x80, 0xFFFFFFFF, flag bytes, offsets, indirect cells, FS:[0]; no 0x42; neither 0x485FD (=296445, correct hex) nor 0x4861D occurs | CONFIRMED (with correction QC-P02-D1 on the worker's hex rendering) |
| 5 | Leaf action = constant class-keyed selection: CALL 007b6c30, key 0x00A85460 = 0x00A85454+0xC, receivers [elem] then [elem+0x24], sentinel-guarded | Rows 626560–626572 re-derived: PUSH 0x00A85460; MOV ECX,EBX; CALL; CMP ESI,EBP; fallback MOV ECX,[EBX+0x24]; same key; bail JZ 0x006b1fb4 (out-of-region, recorded not read). Arithmetic 0x00A85454+0xC PASS; vtable identity of 0x00A85454 is cited (P01/parent GA3), correctly hedged by worker (P02-C4) | CONFIRMED (mechanics) / lookup-vs-register semantics properly CONDITIONAL (CAND-P2a) |
| 6 | Sentinel guard + callee-pops frame convention (steady[0x68], M[steady+0x18]) | Re-derived per-iteration stack balance of the node loop: 4 pushes + caller ADD ESP,0xC for 006f2940's 3 args ⇒ [0x00A75A00] must callee-pop its single arg (else −4/iteration leak under the JNZ back-edge). Under this verified premise: steady[0x68] set/cleared consistently, 007b4170 receiver = M[steady+0x18] @006b1ef9, 0043ca60 byref &steady[0x18] @006B1E0B block | CONFIRMED (premise re-derived as balance-necessity; counter-convention preserved by worker) |
| 7 | RET 0x4 @006b1fa7, one by-value stack arg | RET imm16 semantics + self-consistent epilogue (5 POP + ADD ESP,0x58); caller-side consistency cited from P01 QC (not re-derivable in-region) | CONFIRMED (in-region mechanics) |
| 8 | Outbound hand-off 007b4170(ECX=M[steady+0x18]) conditional on 006f2940 result | Rows 626624–626628 verified | CONFIRMED (CAND-P2b semantics properly PLAUSIBLE/open) |
| 9 | Counters 2/2 bodies (blocks-not-functions, honest note), 136/136 rows, 23/23 CALL, 2/2 candidates; Front A 5/16, 372/1800, 42/64, 6/12 | Reviewer recount identical (18 direct + 5 indirect = 23); Front A arithmetic MATCH | CONFIRMED |

## CONTRACT §12 checks

- **Full manifest re-hash + bijection: PASS.** All 12 manifest entries match this reviewer's independent SHA256 re-hash; 12 listed + self-excluded MANIFEST = 13 disk files, no strays, no missing. Package CONTRACT.json is hash-identical to CONTROL\CONTRACTS\P02.json (A0435DB2…976D).
- **Line parity vs pinned source: PASS** (see table row 1).
- **Alias/lifetime/vtable-boundary premise challenge: PASS.** Scoped negatives keep bounds (in-region/explicit-store level everywhere; opaque callee channels enumerated); vtable match ≠ receiver identity (applied: key proximity = class/type identity only); no direct caller ≠ exclusively virtual (no caller-census claim made); explicit store ≠ final value (countermodel live); NiTArray +C8/+CC/+D4 premise consistent with [EBX+0xD4] count read; P01-C7 same-instance premise not violated (no V/Q claim).
- **Actual vs reserved counters: PASS** (2/2, 136/136, 23/23, 2/2; totals arithmetic verified).
- **Chronology vs EVENTS: PASS.** ADMIT 000004 (21:30:55Z) → contract (21:30:59) → source hash (21:31:09) → RUN_STARTED (21:31:17) → re-verify (21:34:47) → MANIFEST (21:36:36); event hash chain 000003→000004→000005 re-hashed by reviewer — both links MATCH.
- **No semantic read beyond admitted regions: PASS.** Out-of-region targets 0x006B1FB4 and 0x006B1FAF+ recorded as addresses only. Boundary observation (not a violation): end-exclusive 0x006B1FAC cuts mid-instruction — the last admitted row starts 006b1faa (5 bytes spanning to 006b1fae); row-start admission rule is documented by the worker in SOURCE_PINS; reserve 136 = extract 136 exactly; no claim depends on the straddling bytes.

## Corrections (for a future P02 corrigendum per §12 — packages are frozen; nothing was modified by this review)

- **[P2] QC-P02-D1 — incorrect hex rendering of 296445.** COUNTERS.json `store_census_negatives` (line 59) writes "no 296445/0x4861D". 296445 decimal = **0x485FD** (0x4861D = 296477). Effect: documentation-level transcription defect; the absence claim is TRUE under both encodings — neither 0x485FD nor 0x4861D appears anywhere in the 136 rows (reviewer full-immediate scan). Fix: record "296445 = 0x485FD" in the corrigendum. Revalidation predicate: grep the 136 in-region rows for `485fd|4861d` (case-insensitive) → 0 matches.
- **[P2] QC-P02-D2 — ambiguous resolution parenthetical in CLAIMS.json P02-C3.** "REJECTED_WITH_EVIDENCE (binding store present in region)" can be misread as asserting presence; P02-C1 correctly writes "(binding store absent in region)". Effect: wording inconsistency only; statement/evidence/countermodel of C3 are unambiguous (absence; hypothesis rejected). Fix: reword to "REJECTED_WITH_EVIDENCE (hypothesis 'binding store present in region' rejected — store absent)".

## Rejected overclaims

None. The headline ("NO resource-ID/element/receiver binding in the walker tail — pure processing plus ONE constant class-keyed element SELECTION") is correctly scoped to the admitted region at the explicit-store level, carries the get-or-create/register countermodel (callee-opaque channel), and does not promote the region-scoped negative to a global one; MODEL_INSTANCE_BINDING stays NOT_ESTABLISHED.

## Precise remaining edge (after P02, as sharpened by P03)

(a) lookup-vs-get-or-create/register semantics of 007b6c30 — now localized by P03 to the continuation at **0x007B6C4B** (same logical function; parent admission required; do not double-count the body per §6); (b) origin/identity of the 007b4170 receiver slot **M[steady+0x18]** (candidate channels: 0043ca60 byref, or un-itemized P01-window init); (c) low: out-of-region exit tail 0x006B1FAF+ / bail 0x006B1FB4.

## FULL_READ_LOG / NOT_CHECKED

See RECHECK_NOTES.json `full_read_log` / `not_checked`. No load-bearing component was left unchecked; NOT_CHECKED items are cited-context, opaque-by-design or parent-owned (P01 package contents, EVENTS 000001–000003 contents, REQUESTS/CHECKPOINTS, out-of-region code).

## Sealed outputs of this review

RUN_STARTED.json (first write), RECHECK_NOTES.json, COUNTERS_RECHECK.json, QC_REPORT.md, MANIFEST.json (LAST, self-excluded — SHA256 recorded in the parent return, not here).
