# QC REPORT — P12_QC_R1 (independent internal QC of package P12_EXEC_R1)

QC run: PE935_CAMPAIGN_P12_QC_R1_20261018T234830Z | Campaign: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
Target admission: Abff4b58618ac (CONTROL/EVENTS/000015_ADMIT.json) | Region 0x006C27A0-0x006C2830 (end-exclusive)
QC mode: fresh independent reviewer, no delegation, NO_NESTED_TASKS | Deadline 2026-10-19T00:45:00Z respected
Pinned source re-hashed at QC start: 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB (50,780,146 B) — MATCH.

## Verdict: **QC_PASS_WITH_MINOR_CORRECTIONS** (process verdict: PASS_WITH_CORRECTIONS)

All load-bearing P12 claims independently re-derived and accepted; zero rejected overclaims; one P2 counter-notation
correction and two P3 citation/framing nuances recorded below. No semantic correction is required; no claim is
demoted or rejected.

## Accepted claims (independently verified; evidence levels as graded by the worker, re-checked by QC)

| Claim | Worker grade | QC re-derivation (see RECHECK_NOTES.json) | QC status |
|---|---|---|---|
| P12-C1 five-call chain shape, both bodies | CONFIRMED | RDER-01/02/08/09: full instruction trace of both bodies from the parity-verified extract | ACCEPTED |
| P12-C2 return = ret(0x0072F580); body 1 CONFIRMED / body 2 STRONGLY_SUPPORTED | CONFIRMED/SS | RDER-05/06: no EAX writer between CALL 72F580 and body-1 RET; body-2 grading honestly withheld from CONFIRMED because the unread tail could legally write EAX (stack balance constrains slots, not opcodes) | ACCEPTED (grading correct — parent's key question about the return register: EAX holds the 72F580 product at body 1's in-window RET; body 2's EAX at the window cut is the 72F580 product and the stack-forced tail must consume exactly [saved ESI][retaddr]) |
| P12-C3 key = global table DWORD, never the return | CONFIRMED | RDER-01/02 + RDER-05: EDX=table DWORD is consumed by PUSH→0x0043A550; EAX at RET is the 72F580 product, not EDX | ACCEPTED |
| P12-C4 body-1 fail arm returns 0xBA5800; body-2 fail arm NOT claimed | CONFIRMED/NOT_ESTABLISHED | RDER-05 fail-arm trace; body-2 target 0x006C2832 out-of-window, no value claimed | ACCEPTED |
| P12-C5 stack-balance ABI (callee-pops single args) | STRONGLY_SUPPORTED | RDER-07: forcing argument re-derived independently (fixed epilogues on both body-1 arms + body-2 in-window POP EDI); valid given a working client | ACCEPTED |
| P12-C6 scoped negative (no 7CE1E0/72FCE0/43C700/40B070/43E5B0/6C3640/8BD720/6B6C9D refs in-window) | CONFIRMED | OP census: all 10 CALLs are the 4 named targets; no other call/branch/memory form can hide a reference; window-bounded | ACCEPTED (bounds preserved) |
| P12-C7 dead first 0x006B22D0 call in both bodies | CONFIRMED def-use / UNKNOWN side effects | RDER-04: def-use scan of intervening rows; correct split | ACCEPTED |
| P12-C8a resolution idiom (43A550→72F580) in-window | CONFIRMED | RDER-10: citations verified (P06 L103; P04 L35 with a compression nuance; bridge standing accurate) | ACCEPTED |
| P12-C8b composite REGISTRY-FED verdict | STRONGLY_SUPPORTED (conditional on bridge) | RDER-10(a): bridge files attribute FUN_0072F580 = templates.vfs RB-tree lookup; worker correctly keeps the registry label conditional and the call-chain facts unconditional | ACCEPTED |
| P12-C9 table geometry (10/15 strides; base delta 0x3C) | CONFIRMED arithmetic / NOT_ESTABLISHED relationship | RDER-01/02: 5×2=10, 16−1=15, 0xA85804−0xA857C8=0x3C=60 B=15 DWORDs (recomputed) | ACCEPTED |
| P12-C10 MOVSX sign-extend + unsigned JNC bound | CONFIRMED | RDER-03: negative word → huge unsigned → fail arm; ranges [0,10)/[0,15) | ACCEPTED |
| P12-C11 receiver plumbing (ECX=this at 70ED80) | CONFIRMED plumbing / UNKNOWN ABI use | RDER-08 | ACCEPTED |
| P12-C12 window discipline + over-display incident | CONFIRMED census / incident DISCLOSED | RDER-12: all claim citations in L648033-L648080; zero claims from out-of-window rows | ACCEPTED |

Source parity (common check): extract = 48/48 rows verbatim vs pinned source L648033-L648080, contiguous, 0 mismatches
(independent PowerShell slice comparison; first failure of my own first parity script was a QC-script parsing bug,
corrected and re-run — the pack was never at fault).

## Corrections (documentation-grade; no semantic effect)

- **P2 — P12-QC-F1: push_count counter semantics underspecified.** COUNTERS.json `push_count_body1=5` /
  `push_count_body2_in_window=5` count frame slots including the implicit caller return-address push; the explicit
  PUSH-instruction census is 4 per body (8 total, QC-verified: PUSH ESI/EDI/imm/EDX per body). `pop_count_body1_per_arm=3`
  is consistent only under the same accounting. No claim depends on these counters (P12-C5 cites rows directly).
  Correction for any future corrigendum: define or restate. (COUNTERS_RECHECK.json, P12-QC-F1.)
- **P3 — citation compression in P12-C8a:** P04's callsite row reads `arg2 → [arg2] → 43a550 → 72F580 → 72fce0`;
  P12 quotes it without the `[arg2]` deref step. Idiom identity unaffected; no claim depends on the omitted step.
- **P3 — MEMORY_AND_IDENTITY body 2 "22 of 24 rows":** the 24 is a stack-forced estimate (exactly one further pop +
  RET); honest in substance, could be phrased as "≥2 rows out (stack-forced exactly 1 pop + RET)".

## Rejected overclaims

None. The worker's own grading already withholds: body-2 return (SS, not CONFIRMED), body-2 fail value (not claimed),
table relationship (NOT_ESTABLISHED — the 0x3C coincidence is explicitly called numerology), iterator hypothesis
(UNVERIFIED), registry label (conditional on bridge standing), all callee internals (UNKNOWN). QC found no place where
the pack asserts more than its rows support.

## Precise remaining edge (after P12)

Unchanged from the pack's BARRIER_BACKLOG, QC-endorsed: P12-B1 (0x0043A550 key transform — smallest decisive next
admission), P12-B3/B4 (0x0070ED80 column object; 0x006B22D0 row-index/state), P12-B7 (0x006C2830-0x006C2839 ~10-byte
window completes body 2's return contract), P12-B5/B6 (permanent data barrier under campaign rules; parent catalog check
is the only non-admission option), P12-B9 (P11 leftovers). Priority for MODEL_INSTANCE_BINDING remains the consumer
side (0x006B4120, 0x006B6CB9+/0x006B6C9F+, 0x0043E5B0/0x006C3640, 0x008BD720).

## Common checks (parent instruction, per CONTRACT section 12)

- Manifest re-hash + bijection: 12/12 hashes and sizes recomputed = manifest values; 13 files on disk = 12 artifacts +
  self-excluded MANIFEST.json; CONTROL contract hash matches the package's byte-identical copy. PASS.
- Extract line parity vs pinned source: 48/48 verbatim, 0 mismatches. PASS.
- Semantic read ONLY inside admitted region (plus zero authorized exceptions for P12): all claim citations in-window;
  denied front-A region 0x007B6C4B-0x007B6E4B not read (RDER-P12-13). PASS.
- Scoped negatives keep bounds: P12-C6 and the "first globals in the C1 chain" note are window-scoped. PASS.
- Premises: shape-identity not used for semantic transfer (body-2 facts derived from body-2 rows; body-1 fail value
  NOT transferred); definition-registry ≠ instance-source preserved in C8b; inherited bridge claims cited, not
  re-derived, and citation accuracy verified (RDER-10). PASS.
- Actual vs reserved counters: 2/2, 48/48, 10/10, 2/2 — all independently recomputed. PASS.
- Chronology vs CONTROL/EVENTS: 000015 ADMIT 23:42:00Z → contract 23:42:04Z → start 23:42:40Z → extract 23:45:30Z →
  manifest 23:47:20Z; monotonic, before hard stop. Events 000011/000012 verified as the DENIED front-A admits
  (BAD_FRONT for the A+C merge attempt; FRONT_A_TIME_CAP for the 0x007B6C4B continuation) — the denied region was not
  read by P12. PASS.
- Honest attribution: P12 = single attempt; the one navigation over-display incident is disclosed in REPORT (Incidents
  section), GATES (G04 PASS_WITH_DISCLOSED_INCIDENT), and HANDOFF (over-display disclosure with VA list); zero claims
  derive from displayed out-of-window rows (RDER-12). PASS.

## Process verdict: **PASS_WITH_CORRECTIONS** (corrections = P12-QC-F1 counter notation + P3 nuances; no gate fails, no claim changes)

## QC artifacts

- RECHECK_NOTES.json — 13 line-numbered re-derivations with verdicts + FULL_READ_LOG.
- COUNTERS_RECHECK.json — independent counter recomputation, chronology, manifest re-hash.
- MANIFEST.json — sealed LAST, self-excluded.
