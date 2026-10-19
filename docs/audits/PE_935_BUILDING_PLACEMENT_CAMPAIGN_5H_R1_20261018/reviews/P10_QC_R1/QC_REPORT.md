# QC REPORT — P10_QC_R1 (independent internal QC of package P10_EXEC_R1)

QC run: PE935_CAMPAIGN_P10_QC_R1_20261018T234830Z | Campaign: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
Target admission: A6b8526417348 (CONTROL/EVENTS/000013_ADMIT.json) | Region 0x00745A70-0x00745B00 (end-exclusive), 57 rows, 0 calls
QC mode: fresh independent reviewer, no delegation, NO_NESTED_TASKS | Deadline 2026-10-19T00:45:00Z respected
Pinned source re-hashed at QC start: 642CC29A…C1D8DB (50,780,146 B) — MATCH. Authorized P07-extract re-check used for B1 (see below).

## Verdict: **QC_PASS_WITH_MINOR_CORRECTIONS** (process verdict: PASS_WITH_CORRECTIONS)

All load-bearing P10 claims independently re-derived and accepted, including the parent-flagged stack arithmetic
(**VERIFIED CORRECT** — see RDER-P10-01). Zero rejected overclaims. One P3 evidence-count slip and one P3
citation-source imprecision recorded below; no semantic correction required. **B1 SETTLED** by the authorized
P07-extract re-check (RECHECK_NOTES RDER-P10-06).

## B1 SETTLEMENT (parent-assigned: which key DWORD of the 4-DWORD key tuple reaches the byte-compare)

**Answer: key[3] — the FOURTH DWORD of the caller's tuple**, i.e. the value 0x00745BF0 itself received as **its own
first stack argument** (loaded at `MOV EDX,[ESP+0x4]` @0x00745bf0, stored to tuple slot +0xC @0x00745c20, landing in
callee slot **S6 = [callee_entry+0x18]** = the match value compared against each entry's zero-extended byte 0).

Full mapping, independently re-derived from the parity-verified P07 extract (authorized re-check):

| Callee slot | Content at the 0x00745C28 callsite | Role in 0x00745A70 |
|---|---|---|
| S1 = [this+4] | pushed @0x00745c27 (`PUSH EDX`, EDX=[ESI+0x4]) | scan start cursor |
| S2 = [this+8] | pushed @0x00745c26 (`PUSH ECX`, ECX=[ESI+0x8]) | scan end (post-call `CMP EAX,[ESI+0x8]` confirms) |
| S3 = key[0] | tuple slot +0x0 = EBX = read of 745BF0's never-written local block (stale value) | **dead — never read** |
| S4 = key[1] | tuple slot +0x4 = **the constant 4** (`MOV EAX,0x4; MOV EDI,EAX`) | additive base term (ESI=4) |
| S5 = key[2] | tuple slot +0x8 = read of the same never-written local block | **dead — never read** |
| S6 = key[3] | tuple slot +0xC = **745BF0's ARG1** | **match value (the byte-compare operand)** |
| (S7) | `PUSH EAX` @0x00745c09 = &ARG1 | dead — never read by the callee |

Consequences (now slot-exact):
1. The composite 4-DWORD key is **NOT consumed as a composite** — P10-5 CONFIRMED with precision: exactly one tuple
   DWORD (key[3]) reaches the compare, and only its low byte can match (usable key space 0-255; S6>255 e.g. 20006 =
   guaranteed always-fail returning S2, then `JZ 0x00745C40` fail exit).
2. **P10-8 / B4 RESOLVED**: S4 = 4 (nonzero) and the returned cursor is an **absolute entry pointer** — the caller's
   success-path `MOV EAX,[EAX]` @0x00745c35 dereferences the raw return to read the payload DWORD at entry+0, while
   the compared tag byte sits at entry+4 (= cursor+4 via ESI=4). The "+4" is a fixed intra-entry tag offset, not a
   base-pointer/offset duality. (Derived from the authorized P07-extract re-check; resolves the B4 barrier without a
   new admission.)
3. key[0]/key[2] are harmless stale reads (745BF0's own 16-byte local block, never written in-window; dead slots in
   the callee). Remaining edges unchanged: **B2 array populator** (no VA in any admitted window) and the value
   semantics of 745BF0's ARG1 (caller-of-745BF0, never admitted).

Cross-check: the prior P07_QC_R1 review recorded the same slot mapping ("callee 745A70 receives [this+4], [this+8],
&arg1 and the key by value; const 4 at +0x4") — independent agreement, slot for slot.

## Accepted claims (independently verified)

| Claim | Worker grade | QC re-derivation | QC status |
|---|---|---|---|
| P10-1 single self-contained body, 6 in-window branch targets, single RET, 0 CALL | CONFIRMED | RDER-04: VA-delta + target-set census | ACCEPTED |
| P10-2 stack-slot arithmetic S1/S2/S4/S6 consumed, S3/S5 dead | CONFIRMED | **RDER-01: push-shift arithmetic re-derived per read — all four slot attributions exactly correct** (parent-flagged check) | ACCEPTED |
| P10-3 std::find-shaped first-match scan (0x20-block 4-unroll + residual 1/2/3; match→entry start, miss→S2) | CONFIRMED | RDER-02: full control-flow re-enumeration incl. all 7 match sites and the residual dispatch table | ACCEPTED |
| P10-4 single-byte match criterion; S6>255 always-fail; immediate census {1,3,4,5,8,0x14,0x18}, no 20006/6/2 | CONFIRMED | RDER-03: independent census identical; control calculation confirms always-fail | ACCEPTED |
| P10-5 composite 4-DWORD key NOT consumed; id2/class-20006-tag-6 REJECTED at 0x00745A70 level (scoped) | REJECTED_WITH_EVIDENCE (callee level); caller variant NOT_ESTABLISHED | RDER-03 + RDER-06 (B1): slot-exact confirmation; caller-side variant correctly left open | ACCEPTED |
| P10-6 bytes 1-7 never read in-window | CONFIRMED (scoped) | RDER-02: all byte reads at 8-aligned entry-start positions | ACCEPTED |
| P10-7 no VFS-record-fed source in-window (scoped negative) | CONFIRMED (scoped); FAMILY-P/T NOT_DECIDABLE | RDER-05: operand census; bounds preserved | ACCEPTED |
| P10-8 cursor addressing duality not decidable in-window | UNVERIFIED (both models fit) | Correct AT P10's WINDOW; now RESOLVED via the authorized B1 re-check (see settlement) — no defect in the pack; the barrier is closed with evidence the worker could not have had | ACCEPTED (barrier resolved by QC) |
| P10-9 ABI (no EBP frame; 3/3 push-pop; RET no imm; EAX/ECX/EDX clobbered; 6-arg reading PLAUSIBLE) | CONFIRMED (register/RET) / PLAUSIBLE (arg count) | RDER-04 | ACCEPTED |

Source parity (common check): extract = 57/57 rows verbatim vs pinned source L809770-809826, 0 mismatches; boundary
line 809827 (0x00745B00) excluded. Authorized P07 SR1 extract = 32/32 rows verbatim vs L809928-809959, 0 mismatches.

## Corrections (minor; no semantic effect)

- **P3 — P10-QC-F1: evidence-count slip in P10-8.** P10-8's evidence string says "effective address [ESI+EAX*1] at
  all **10** byte-read sites"; the correct census is **7** MOVZX byte-read sites (4 main-loop + 3 residual). The
  claim statement ("all byte reads are [ESI + cursor]") is true for all 7 sites; the count error affects no
  conclusion. Correction for any future corrigendum: replace "10" with "7".
- **P3 — P10-QC-F2: citation-source imprecision.** SOURCE_PINS PIN-P10-CTX-1 attributes "called 745A70 with
  [this+4]/[this+8] pushes" to P07 REPORT.md; that element appears in the P07 QC review (reviews/P07_QC_R1), not in
  P07's own REPORT (the other five cited elements are literally in P07 REPORT.md L4). The FACT is true (verified
  from the parity-verified P07 extract). Correction: cite the P07 QC review for that element.

## Rejected overclaims

None. The pack's negative results (P10-5 callee-level rejection; P10-7 scoped negative; P10-8 UNVERIFIED duality)
are correctly bounded; the caller-side variant of the id2/tag-6 hypothesis is explicitly preserved as
NOT_ESTABLISHED rather than silently rejected or accepted.

## Precise remaining edge (after P10 + this QC)

- **B2 (primary)**: identity of the array populator (stores to the [this+4]/[this+8]-bounded range) — no VA visible
  in any admitted window; the FAMILY-P/T merge decision point.
- **ARG1 semantics**: what the caller-of-745BF0 feeds as 745BF0's first argument (the eventual S6 match byte
  source) — caller-of-745BF0 window never admitted.
- B4 is now RESOLVED by this QC (cursor = absolute entry pointer; S4=4 fixed tag offset); B1 is SETTLED (key[3]);
  B3 (payload bytes 1-7 semantics) narrows to the entry-payload consumer on the success path (partially visible in
  the authorized P07 extract as `MOV EAX,[EAX]` = payload DWORD read at entry+0 — a QC-level observation, not a
  worker claim).

## Common checks (parent instruction, per CONTRACT section 12)

- Manifest re-hash + bijection: 12/12 hashes + sizes recomputed = manifest values; 13 files on disk = 12 artifacts +
  self-excluded MANIFEST.json; CONTROL contract hash = package CONTRACT.json. PASS.
- Extract line parity vs pinned source: 57/57 verbatim, 0 mismatches (P10); 32/32 verbatim (authorized P07 SR1
  re-check). PASS.
- Semantic read ONLY inside admitted region: all claim citations L809770-809826; the two navigation events disclosed
  (address+mnemonic hit L809950; address-only boundary scan L809827); zero claims from out-of-window rows. PASS.
- Scoped negatives keep bounds: P10-7's no-VFS negative is window-bounded; FAMILY-P/T explicitly NOT_DECIDABLE. PASS.
- Premises: shape-identity not used for semantics ("std::find-shaped" labeled as shape, with renaming rule refusing
  PropertyMap::find canonization); definition-registry ≠ instance-source applied; inherited P07 claims cited —
  citation accuracy verified (one P3 source imprecision, facts true). PASS.
- Actual vs reserved counters: 1/1 body, 57/57 rows, 0 CALL (edges:4 reserve; prompt/contract discrepancy honestly
  disclosed), 2/2 candidates — all independently recomputed. PASS.
- Chronology vs CONTROL/EVENTS: 000011 DENY (BAD_FRONT) 23:26:19Z → 000012 DENY (FRONT_A_TIME_CAP) 23:26:25Z →
  000013 ADMIT 23:26:31Z → verify 23:26:44Z → start 23:26:50Z → extract 23:29:53Z → manifest 23:31:27Z; monotonic,
  before hard stop 00:40:00Z. Events 000011/000012 verified as the DENIED front-A admits; the denied region
  0x007B6C4B-0x007B6E4B was NOT read (RDER-P10-07). PASS.
- Honest attribution: single attempt; RUN_STARTED preceded only by the mechanical CONTRACT.json copy (disclosed in
  GATES G3 as PASS_WITH_DISCLOSURE). PASS.

## Process verdict: **PASS_WITH_CORRECTIONS** (P3-grade corrections only; no gate fails; B1 settled; B4 resolved)

## QC artifacts

- RECHECK_NOTES.json — 8 line-numbered re-derivations incl. the full B1 settlement trace + full-read log.
- COUNTERS_RECHECK.json — independent counter recomputation, chronology, manifest re-hash.
- MANIFEST.json — sealed LAST, self-excluded.
