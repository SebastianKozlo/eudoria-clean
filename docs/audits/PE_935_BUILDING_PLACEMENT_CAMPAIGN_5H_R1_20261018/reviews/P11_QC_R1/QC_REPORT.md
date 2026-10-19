# QC REPORT — P11_QC_R1 (independent internal QC of package P11_EXEC_R1)

QC run: PE935_CAMPAIGN_P11_QC_R1_20261018T234830Z | Campaign: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
Target admission: Ae2bd704a017c (CONTROL/EVENTS/000014_ADMIT.json) | Region 0x006B6C1B-0x006B6C9D (45 rows, 4 CALL)
QC mode: fresh independent reviewer, no delegation, NO_NESTED_TASKS | Deadline 2026-10-19T00:45:00Z respected
Pinned source re-hashed at QC start: 642CC29A…C1D8DB (50,780,146 B) — MATCH.

## Verdict: **QC_PASS_WITH_MINOR_CORRECTIONS** (process verdict: PASS_WITH_CORRECTIONS)

All load-bearing P11 claims independently re-derived and accepted. The parent-assigned verifications both PASS:
the **26→16 stack-census arithmetic-slip correction is VERIFIED CORRECT** (my independent census = 16), and the
**retry attribution is honest** (prior-session CONTRACT.json + RUN_STARTED.json preserved byte-identical; retry
marker added; chronology disclosed). One P2 chronology inconsistency in the manifest stamping recorded below.
Zero rejected overclaims.

## Accepted claims (independently verified)

| Claim | Worker grade | QC re-derivation | QC status |
|---|---|---|---|
| P11-C1 stack-local DWORD-stride append buffer (cursor/bound/pending slots; equality-gated redirects) | CONFIRMED-as-instruction (mechanics); SS (bound reading) | RDER-01: full state-machine trace both stages; MOV [ESP+0x14],EAX does not touch EFLAGS so each JZ tests its CMP — verified | ACCEPTED |
| P11-C2 elements = producer returns on [EDI+0x8] (0x006C27A0 / 0x006C27F0), stash to [ESP+0x14]; [EDI+0x8] only object-field read, receiver-only | CONFIRMED-as-instruction; producer semantics UNKNOWN | RDER-02: census [EDI+0x8] exactly x2; no other EDI offset | ACCEPTED |
| P11-C3 helper 0x006B4120 (this=[ESP+0x48]; args incl. incoming ECX, &[ESP+0x20], &[ESP+0x58], 1, 1; callee-cleans shape); overflow-path ECX = stage-A cursor | CONFIRMED-as-instruction; helper role UNKNOWN | RDER-03: no ADD ESP after CALL (rows verified); ECX flow L632948→L632965 re-traced with no intervening ECX writer | ACCEPTED |
| P11-C4 pump entry = stage-B cursor==bound (JZ @L632988→0x006B6C9D); overflow/fallback arm; window last row = declared pump entry | CONFIRMED-as-instruction | RDER-04: sole in-edge verified; continuation not read | ACCEPTED |
| P11-C5 scoped negative: 0 global refs, 0 registry/pump-machinery calls in-window | SCOPED_NEGATIVE (window-bounded) | RDER-05: independent census 0 absolute refs; 4 CALLs = {6B4120×2, 6C27A0, 6C27F0} only | ACCEPTED |
| P11-C6 pump internals = STANDING_INHERITED (P07-C3 + bridge, cited not re-derived) | STANDING_INHERITED | RDER-09: citation hashes + content verified (P07 REPORT L5; bridge files) | ACCEPTED (citation accurate) |
| P11-C7 skip-slot behavior (cursor==EBP → store skipped, cursor advances); EBP role UNKNOWN | CONFIRMED-as-instruction; EBP UNKNOWN | RDER-06: both JZ→ADD paths verified | ACCEPTED |
| P11-C8 synthesis: in-window supports only "container field"; producers' internal source UNDECIDABLE; split trigger/data answer | CONFIRMED-as-instruction / UNKNOWN / STANDING_INHERITED | composition of C1-C7, all verified; NOTE: the producers were subsequently admitted and read by P12, which decided the open edge (registry-fed via CALL 0x0072F580) — P11's UNDECIDABLE-at-this-window grading remains correct for its own scope | ACCEPTED |

Hypotheses P11-H1/H2/H3 correctly recorded as unclaimed. Source parity: 45/45 rows verbatim vs L632937-632981,
0 mismatches, VA stream gapless (6c1b→6c9d).

## Corrections

- **P2 — P11-QC-F1: manifest chronology inconsistency.** MANIFEST.json declares `manifest_generated_utc =
  2026-10-18T23:41:30Z`, but COUNTERS.json is stamped 23:42:00Z and GATES.json 23:47:00Z — i.e., two artifacts
  carry stamps LATER than the manifest that should be LAST. Either the manifest stamp is mis-set or COUNTERS/GATES
  were edited after manifest generation. Content integrity is unaffected (13/13 hashes verify; the extract and all
  claims are pinned by their own hashes), and no claim depends on artifact ordering — but the stamp set is
  internally inconsistent with the declared "LAST artifact" rule. Correction for any future corrigendum: re-stamp
  or re-materialize the manifest after the last artifact edit. (COUNTERS_RECHECK.json, chronology_check.)
- **P3 — P11-QC-F2 (procedural note, no correction required in-pack):** the two boundary greps and the 15-line
  header peek are disclosed as navigation; QC verified no claim cites any row outside L632937-632981.

## Rejected overclaims

None. The pack grades its own limits honestly: producer semantics UNKNOWN, helper role UNKNOWN, EBP UNKNOWN,
loop structure UNKNOWN, pump-input P11-H1 unclaimed, PUSH-0x1 mirror P11-H2 shape-only, bound-vs-capacity
STRONGLY_SUPPORTED not CONFIRMED.

## Precise remaining edge (after P11 — as of this QC superseded in part by P12)

The producers 0x006C27A0/0x006C27F0 (P11-B1/B2) were the primary discriminator — **subsequently admitted and read by
P12** (REGISTRY-FED via CALL 0x0072F580; P12 QC verdict: QC_PASS_WITH_MINOR_CORRECTIONS). Still open from P11:
helper 0x006B4120 role (P11-B3), stage-B success exit 0x006B6CB9 / enclosing head (P11-B4/B6 — EDI identity,
buffer init, EBP role, loop structure), pump [ESP+0x14]-consumption proof (P11-B5/H1).

## Common checks (parent instruction, per CONTRACT section 12)

- Manifest re-hash + bijection: 13/13 hashes + sizes recomputed = manifest; 14 files on disk = 13 + self-excluded
  MANIFEST.json; external reference hashes (P07 REPORT, bridge draft) re-verified. PASS (with the P11-QC-F1 stamp
  inconsistency noted).
- Extract line parity vs pinned source: 45/45 verbatim, 0 mismatches. PASS.
- Semantic read ONLY inside admitted region: all citations L632937-632981; navigation disclosed; denied front-A
  region 0x007B6C4B-0x007B6E4B not read (RDER-P11-10). PASS.
- Scoped negatives keep bounds: P11-C5 strictly window-bounded. PASS.
- Premises: twin stages shape-only (no semantic transfer); definition-registry ≠ instance-source applied in C2/C6;
  inherited claims cited not re-derived, citation accuracy verified (RDER-09). PASS.
- Actual vs reserved counters: 2/2, 45/60 (UNDER, honest), 4/8 (UNDER, honest), 2/2 — all independently recomputed.
  PASS.
- Chronology vs CONTROL/EVENTS: 000014 ADMIT 23:32:39Z → first session 23:32:58Z (died; 2 files preserved) → retry
  marker 23:36:51Z → science artifacts 23:39-23:47Z → hard stop 00:55:00Z respected. Events 000011/000012 verified
  as the DENIED front-A admits (P10 story); the denied region was not read by P11. PASS (with P11-QC-F1 noted).
- Honest attribution: attempt-1 emptiness disclosed and preserved (G11); retry marked; the 26→16 in-run slip
  disclosed in SELF_CHECK and MANIFEST origin note, and the corrected value independently verified exact. PASS.

## Process verdict: **PASS_WITH_CORRECTIONS** (P2 stamp inconsistency + nothing semantic; no gate-content fails; all claims stand)

## QC artifacts

- RECHECK_NOTES.json — 10 line-numbered re-derivations incl. the slip-correction and retry-attribution verifications.
- COUNTERS_RECHECK.json — independent counter recomputation, chronology (with the F1 anomaly), manifest re-hash.
- MANIFEST.json — sealed LAST, self-excluded.
