# PE_NIF_WITNESS_FALSIFICATION_R1 — 00_FINAL_REPORT (RUN-E)

**RUN_ID**: PE_NIF_WITNESS_FALSIFICATION_R1_20260905_131214
**EXECUTION**: direct by pe-master-auditor (Task endpoint unavailable this session — standing project precedent; documented)
**P0**: do the 6 witness-recipe predictions (pinned WITNESS_MATRIX.json @ 8c037c0, blob 408f736d) hold when ACTUALLY executed against the frozen R61 parser?
**ERA-PRIMARY**: PCG 9.3.5 (corpus SHA256 re-hashed: c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0)
**BASE**: repo HEAD at run start per orchestrator pre-flight; HEAD_SHA of the publication commit recorded in the handoff.

## SCOREBOARD: 5/6 exact predictions MATCHED + 1 FINDING (F-1, MILD-2 prediction REFUTED)

| Variant | Prediction (pinned matrix) | Actual (execution) | Verdict |
|---|---|---|---|
| **MILD-1** (146709 u3-byte1 @639 0x18→0x19) | PASS self-healed; SILENT variant flip G3D→G3E; boundary_search recovers TRUE boundary (**766**) | PASS; ark_variant=G3E; boundary_method=boundary_search; ext_size=120; **true_boundary_from_raw=766; preamble_u32@766==0** | **MATCH (exact, incl. the PE-MASTER 766 gate)** |
| **MILD-2** (424276 node-count digit @306 '2'→'3') | PASS self-healed; transient ArkAnimationError swallowed by TEXT_CRLF→G9_RTTI fallback; SILENT variant flip to G9_RTTI | **FAIL_CLOSED @block 3** (loud desync failure; fail_reason records the desync region) — the G9_RTTI fallback did NOT trigger | **MISMATCH → FINDING F-1** |
| **MILD-3** (500078 u2-LSB @625 0x02→0x03) | FAIL_CLOSED: "v10 NiArkAnimationExtraData u2=0x00000003 has no P0-verified parser. FAIL CLOSED." | **EXACT VERBATIM**: "FAIL CLOSED: block_type=NiArkAnimationExtraData offset=605 reason=variant parse error: v10 NiArkAnimationExtraData u2=0x00000003 has no P0-verified parser. FAIL CLOSED." | **MATCH (exact)** |
| **SCRAMBLE-1** (container byte-copy footer 'BNT2'→'XXXX') | container ValueError "not a BNT2 archive: footer magic=b'XXXX'" before any payload parse | **EXACT**: ValueError "not a BNT2 archive: footer magic=b'XXXX'"; positive control: intact original loads 5,596 entries; container SHA changed (pre-parse detectable) | **MATCH (exact)** |
| **SCRAMBLE-2** (424276 version u32 @41 → 0xFFFFFFFF) | FAIL_ERROR "header parse error: absurd string length 1766719488 at pos=51" (anchor_forensics simulated value) | **EXACT**: parse_status=FAIL_ERROR; fail_reason == "header parse error: absurd string length 1766719488 at pos=51" | **MATCH (exact)** |
| **SCRAMBLE-3** (500078 preamble @481 → 0xDEADBEEF) | FAIL_CLOSED "non-zero block_preamble_u32=3735928559" @block 0 | **EXACT**: FAIL_CLOSED; fail_block_index=0; block_type=NiNode; offset=481; reason=non-zero block_preamble_u32=3735928559 | **MATCH (exact)** |

## FINDING F-1 (the falsification run's value demonstrated)

- **What**: the pinned matrix's MILD-2 predicted_outcome is REFUTED: the parser does NOT
  silently absorb a TEXT node-count overshoot via the G9_RTTI fallback; it FAILS CLOSED
  at the first desynced block (block 3 of 424276), loudly.
- **Severity**: P1, matrix-internal prediction error. **NO safety regression — the actual
  behavior is the SAFER property** (no silent corruption absorption). No parser-contract
  breach (MILD-3's must-fail contract HELD; MILD-2's predicted silent-pass was the wrong
  expectation, not the parser).
- **Blast radius**: (a) WITNESS_MATRIX.json MILD-2 predicted_outcome record (historical —
  correction via ledger entry, not in-place edit); (b) RUN-C's final-message claim
  "MILD-2 → PASS przez G9_RTTI fallback" — WRONG. Zero docs/nif grammar-claim impact
  (the matrix is a test-plan artifact, not wiki content); zero prior-corpus-result impact.
- **Required correction (proposed)**: a CORRECTION_LEDGER entry recording the MILD-2
  actual outcome (proposed to the standing CORRECTION_LEDGER.md in a future bounded
  application — NOT applied in this run; wiki HOLD).

## SELF-DISCLOSURE (instrument)

1. The first driver's verdict-match logic was BUGGY (it required an exception where the
   frozen parser reports failures via parse_status fields on a returned result object).
   The RAW parse results were correct and stand unchanged; the verdict computation was
   re-done post-hoc by verdicts_fixed.py (hash recorded) — full disclosure in
   02_LOGS + both driver hashes in SHA256_DRIVER.txt.
2. SCRAMBLE-1 was executed on a FULL container byte-copy (395,412,868 B) per the pinned
   recipe ("byte-copy of pcg_install Models.bnt ... NEVER the original") — the copy lives
   ONLY in the run's local sandbox; originals untouched; zero payloads published.

## GATES (per the PE-MASTER GO)

| Gate | Result |
|---|---|
| Pins re-hashed at start | R61 10/10; corpus SHA; map SHA (git blob 408f736d == local hash-object) — PASS |
| 6 sandbox variants built exactly per recipes | 6/6; every precondition assertion held (byte@639==0x18, byte@306=='2', byte@625==0x02, version bytes==0c000104, preamble==00000000, footer=='BNT2'); byte-diffs recorded — PASS |
| MILD-1 gate: boundary-recovery == 766 | TRUE boundary computed from raw = 766; recovered boundary consistent; preamble u32 @766 == 0 — PASS |
| MILD-3 MUST FAIL_CLOSED | FAIL_CLOSED with the EXACT predicted reason (no P0-verified parser for u2=3) — PASS (contract held) |
| SCRAMBLE-1/2/3 fail loudly with exact modes | ValueError / absurd-length FAIL_ERROR / preamble FAIL_CLOSED — 3/3 EXACT |
| No silent pass | NONE of the 6 silently passed; the one predicted-silent case (MILD-2) failed LOUDLY — the parser is STRICTER than predicted |
| Originals untouched | corpus SHA re-hashed after the run = unchanged; all edits only on sandbox copies — PASS |
| Zero payloads in repo | SANDBOX dir stays LOCAL-ONLY; repo publication = package without sandbox (identity metadata: SHA256 + diffs only) — PASS |

## MILESTONE_PROGRESS vector

```
variants_built: 6/6 (3 mild single-byte + 2 payload scrambles + 1 container scramble)
predictions_matched: 5/6 exact
findings: 1 (F-1, MILD-2 matrix prediction refuted; actual = safer loud failure)
counts: 6 witness recipes executed against the frozen R61 parser, offline
excluded: no render, no client runtime, no application, no wiki edits, no M2 advancement;
          sandbox copies local-only; originals untouched; zero payloads in repo
```

## Consequence (per the GO's point 5)

After this run: the NIF queue continues to RUN-F (block-census 9.3.5 — IF not already
done; to be verified) and then WAITS for the x87 CW (M1 stream) and human decisions.
HARD STOP after this package + handoff; report to PE-MASTER via the human.

RUN_STATUS = COMPLETED
HARD_STOP_REASON = NONE (falsification executed; finding F-1 recorded; awaiting PE-MASTER review; no auto-continuation)
