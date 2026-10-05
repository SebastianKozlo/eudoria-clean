# QC REPORT — PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005

QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION
Author/origin: pe-reconstruction worker session (executor self-QC), run under
the PE-MASTER two-phase dispatch of 2026-10-05. This is NOT an independent
audit; the independent Desktop post-audit of the eventually published commit
remains a separate human-relayed step, and the PE-MASTER internal
pre-publication review is the phase-2 gate (advisory/pre-qualification;
CANONICAL_GATE_EFFECT = NONE).

## Battery

Instrument: 03_SCRIPTS/cqc_battery.py (the corrected battery; every status
derived from measured inputs on disk, no hard-coded PASS).
Executions: `--mode data` then `--mode docs` (the committed record is the
LAST full run; both runs re-hash the pinned EXE
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 /
8,015,872 B).

## Data-mode result (01_RAW/CQC_FINAL.json)

- Gates Q1-Q13: 13/13 PASS.
  - Q1 baseline: EXE pinned-match + LOCAL_HEAD == origin/master ==
    actual-remote == c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd (pre-commit
    phase-1 state; after the eventual phase-2 commit the HEAD moves BY
    DESIGN - the Q1 scope note records this).
  - Q2 (P2-3 corrected): 133 JSON pins re-derived (opcode_bytes, length,
    boundary status/source) + the effective_address object for all 46 mem
    pins (46 checked, 46 re-derived, 0 mismatches, 0 JSON<->CSV EA
    inconsistencies) + pin_totals.fail_count == 0.
  - Q3: all 133 CSV rows re-derived full-row (measured_operand /
    measured_target / boundary fields / status classes).
  - Q4: decoder unit battery 64/64 vectors (measured count), census
    re-decode 2612/2612 rows clean, coverage windows sane.
  - Q5: boundary matrix 13/13 cases (A1, A2, B, C, D, E, NEW-F incl. 106
    order-permutation proofs, NEW-G, 2x REAL-REFUTE, 3x REAL positive
    controls) + non-E8 control + census discipline sweep + anchor registry
    complete.
  - Q6: all 2227 positive census rows boundary-re-derived; 0 mismatches
    (negative disp8 controls boundary-free by design).
  - Q7: AF3 discipline (manager PROVEN chain physically re-verified; the
    four downgraded layout controls stay UNRESOLVED); ledger<->census
    consistent.
  - Q8: C3 store collection re-derived (3 stores, 2 FS:[0] segment stores
    excluded from this+0 eligibility); DIRECT_VPTR status match.
  - Q9: census arithmetic re-summed from the emitted CSV - all
    consistency predicates true; RAW_PATTERN_ROWS regression 2612 MATCH.
  - Q10: both known stores re-pinned (bytes + CONFIRMED boundary +
    THIS_OF_KNOWN_FUNCTION provenance).
  - Q11: enumeration membership derived from measured bounds; CONTROL B
    mutant fails.
  - Q12: object structural identity checks.
  - Q13: declared family count agreement (9, derived from len(FAMILIES)).
- Mutations: 7/7 CAUSAL_PASS (MUTATION_TOTAL = 7; M1, M2, M3, M4,
  AF3/Q8 compound, M5, M6 - each UNMUTATED=PASS -> MUTATED=FAIL through
  the SAME production gate function object, with exact BEFORE/AFTER values
  and the exact failing predicates recorded).
- QC_VERDICT (data): QC_PASS.

## Docs-mode result

- Q14: required-string battery over FINAL_REPORT.md (all preserved-core and
  correction-status strings present); forbidden/overclaim phrase sweep over
  the active claim surfaces (0 hits; the supersession ledger quotes are
  confined to ORIGINAL_EXCERPT lines); supersession quotecheck 10/10
  excerpts verbatim in their named READ-ONLY sources, 9 records = declared
  NEW_SUPERSESSION_RECORD_COUNT; P3-C identity hygiene (C1 historical typo
  count 1; new identity present; typo absent from this package);
  commit-message verbatim fidelity (01_RAW/C2_COMMIT_MESSAGE_VERBATIM.txt
  == git log -1 --format=%B c4cb60f...); forbidden-input census over the
  instruments (no .vfs/.bnt/.nif/.ark opened; no http literals).
- QC_VERDICT (full, data+docs): QC_PASS.

## In-run repair disclosure (single authorized pass)

The battery's FIRST data-mode execution failed Q2 with 70 false-positive
JSON<->CSV EA inconsistencies on ten mem+imm pins (e.g. driver_local_0x80,
`C7 44 24 1C 80 00 00 00`): those pins serialize the IMMEDIATE form in the
CSV measured_operand by the generator's design, so the CSV provides no EA
representation for them. The check was corrected to participate only where
the CSV row actually carries the EA pipe representation; the JSON EA of
those pins remains fully validated against the EXE by the primary
re-derivation. The committed records are from the final pass (the standard
two-pass battery discipline; disclosed here honestly, as in the source
run).

## Mutation records (exact values in 01_RAW/CQC_MUTATION_RESULTS.json)

| ID | Gate | Before | After | Failing predicates |
|---|---|---|---|---|
| M1 | Q2 | stream_ctor_entry.opcode_bytes = '6A FF' | 'EB FF' | 1 (opcode_bytes vs EXE-derived) |
| M2 | Q3 | slotpred measured_operand = '0x70BEF0 (7388912)' | '0x70BEF0B8 (118482808)' | 1 |
| M3 | Q8 | offset_zero_stores = [3 measured stores] | [] | 2 (count + derived status) |
| M4 | Q6 | census[0x0070DD1A].containing_function = 'FUN_0070DCF0_consumer_record_reader' | 'entry~0xDEADBEEF' | 1 |
| AF3/Q8 | Q7 | manager row: IDENTITY_EDGE/IDENTIFIED_OBJECT/IDENTITY_EVIDENCE/ADDRESS_PROVENANCE_STATUS all populated | all four emptied (COMPOUND; candidate bytes unchanged) | 5 |
| M5 | Q2 | THE_STORE_plus_84 EA base_register = 'ESI' | 'EAX' | 1 (base_register vs EXE-derived ESI) |
| M6 | Q2 | THE_STORE_plus_84 EA provenance = 'THIS_OF_KNOWN_FUNCTION:FUN_0070C680_stream_attach_setter' | 'THIS_OF_KNOWN_FUNCTION:FUN_00000000_FAKE' | 1 (provenance vs EXE+thisflow-derived) |

Every mutated copy lived in a temporary tree OUTSIDE the repo and was
deleted after its run; no corrupted copy is persisted anywhere; unrelated
artifacts were copied byte-identical into each temp package so the mutated
package differs from the production package ONLY in the mutated field.

## Outcome-conditional statement

QC PASS means the corrected claims accurately match evidence and stated
uncertainty; it does NOT mean all census candidates were solved (the 2218
unresolved census rows and every NOT_ESTABLISHED/UNVERIFIED state in
FINAL_REPORT.md are the corrected honest states, not failures).
