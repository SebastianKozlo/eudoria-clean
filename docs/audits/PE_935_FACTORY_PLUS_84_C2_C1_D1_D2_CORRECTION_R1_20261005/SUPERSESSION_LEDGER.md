# SUPERSESSION LEDGER — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005

NEW_SUPERSESSION_RECORD_COUNT = 9

A NEW ledger for THIS correction run (the historical 9-record ledger of the
THREE-P2 package, the 13-record ledger of the C2 package and the 31-record
ledger of the C1 package remain untouched, READ ONLY). Every ORIGINAL_EXCERPT
below is machine-verified a verbatim substring of its named READ-ONLY source
(quotecheck gate Q14); the commit-message source is the verbatim copy under
01_RAW whose fidelity to the immutable git object at 9d31a82b is itself
machine-checked by Q14. Retractions are recorded here; NO historical file and
NO historical commit is edited.

## S-D1-01

- SUPERSEDED_CLAIM: the committed BASE decoder's grouped-opcode validity rule
  shared ONE legal-reg whitelist across opcodes 0F 71/72/73 in both the MMX
  and the SSE2 branch, so the reserved `0F 73 /4` sub-encoding was ACCEPTED
  with and without the 66 prefix (Desktop post-audit finding D1/P2; per the
  ISA there is no 0F 73 /4 form in either class).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/03_SCRIPTS/x86dec.py`
- ORIGINAL_EXCERPT: `# SSE2: 71/72/73 reg {2,4,6}; 73 reg {3,7} = PSRLDQ/PSLLDQ`
- ORIGINAL_EXCERPT: `return reg in (2, 4, 6) or (op2 == 0x73 and reg in (3, 7))`
- ORIGINAL_EXCERPT: `# MMX: 71/72/73 reg {2,4,6}; 0F 73 reg {3,7} reserved without 66`
- ORIGINAL_EXCERPT: `return reg in (2, 4, 6)`
- NEW_STATEMENT: the corrected decoder (this package's 03_SCRIPTS/x86dec.py)
  judges the 0F 71/72/73 immediate-shift family by PER-OPCODE legal-reg
  tables: 0F 71 {2,4,6}/{2,4,6}, 0F 72 {2,4,6}/{2,4,6},
  0F 73 {2,6}/{2,3,6,7} (without-66/with-66); `0F 73 E0 02` and
  `66 0F 73 E0 02` REJECT fail-closed; /4 stays legal for 71/72; 66 0F 73
  /3,/7 stay legal (PSRLDQ/PSLLDQ); mod=3 requirement, memory-form
  rejection, F2/F3 rejection and 0F BA behaviour unchanged. Oracle: GNU
  objdump Binutils 2.44 returns (bad) for both negative forms
  (01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json, fixtures D1_NEG_73_4_E0,
  D1_NEG_73_4_E0_66).
- EVIDENCE: 01_RAW/CQC_DECODER_UNIT_TESTS.json (D1 vectors); oracle records;
  D1 falsifier (01_RAW/D1_BOUNDARY_FALSIFIER.json).

## S-D1-02

- SUPERSEDED_CLAIM: the THREE-P2 FINAL_REPORT's correction-status list
  declared the H2 family closed as `CORRECTED_FAIL_CLOSED_VALIDITY`; the
  independent Desktop post-audit proved the family was NOT closed (0F 73 /4
  accepted). The family-level claim is superseded; the per-opcode repaired
  state is declared instead.
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/FINAL_REPORT.md`
- ORIGINAL_EXCERPT: `H2_GROUP_OPCODES = CORRECTED_FAIL_CLOSED_VALIDITY`
- NEW_STATEMENT: THIS run's family status is
  `H2_GROUP_OPCODES = CORRECTED_PER_OPCODE_VALIDITY_TABLES` (the D1 defect
  repaired; the H2 controls carried from THREE-P2 all still pass; the
  bounded-instrument honesty stays: the decoder is NOT a general-purpose x86
  decoder, and no whole-family closure beyond the oracle-verified fixture
  set is claimed).
- EVIDENCE: 01_RAW/CQC_DECODER_UNIT_TESTS.json (72 entries, all pass);
  oracle D1 fixtures; the D1 smoke battery in GENERATION_RECORD.md.

## S-D1-03

- SUPERSEDED_CLAIM: the THREE-P2 honest-limits section asserted that no
  defect remained and the repair was complete for the whole dispatched
  scope; the Desktop post-audit found the D1/D2 defects inside exactly that
  scope, so the completeness assertion is superseded (the repairs it
  described for P2-1/P2-2/P2-3/H1/H2-in-tested-scope stand - the audit
  confirmed them and did not reopen them).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/FINAL_REPORT.md`
- ORIGINAL_EXCERPT: `- No defect was found that could not be fixed within the bounded scope; the`
- ORIGINAL_EXCERPT: `  repair is COMPLETE for the three P2 + H1 + H2 as defined by the dispatch.`
- NEW_STATEMENT: THIS run's honest-limits statement is scoped to what is
  actually tested: D1/D2 repaired in the measured fixture/mutation scope;
  the 2218 unresolved census rows and every NOT_ESTABLISHED/UNVERIFIED
  state remain the honest states; NO blanket completeness claim is made
  for the machinery, and the corrected instruments are usable for dependent
  work within their measured boundary - not an unrestricted green light.
- EVIDENCE: Desktop post-audit REPORT.md (D1_H2_INVALID_73_4 = OPEN_P2,
  D2_Q2_PINSET_AND_APPLICABILITY = OPEN_P2 - the authority for this
  correction); this run's D1/D2 controls.

## S-D2-01

- SUPERSEDED_CLAIM: the committed BASE gate_q2 decided effective-address
  applicability SOLELY from the mutable JSON field `pin.kind` and trusted
  the declared fail_count as its final predicate - a relabelled kind or a
  removed EA object silently disabled EA validation, and pin
  completeness/multiplicity were never checked (Desktop finding D2/P2).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/03_SCRIPTS/cqc_battery.py`
- ORIGINAL_EXCERPT: `ea_required = (pin.get("kind") == "mem")`
- ORIGINAL_EXCERPT: `q2["ok"] = (not q2["mismatches"] and not q2["json_csv_inconsistencies"]`
- ORIGINAL_EXCERPT: `and pkg["c1"]["pin_totals"]["fail_count"] == 0)`
- NEW_STATEMENT: the corrected gate_q2 binds the expected pin universe to
  the BASE-pinned PINS roster (re-derived in-run from the BASE Git blob),
  requires the JSON claim multiset == CSV claim multiset == expected roster
  multiset with each expected claim EXACTLY ONCE, checks claim_id +
  instruction_va + declared role per claim, checks the declared totals
  against the measured rows, and derives EA applicability from the EXPECTED
  role - a mutated JSON kind FAILS the role check AND cannot disable EA
  validation; the EXE-derived EA is additionally cross-checked against the
  roster's pinned expect_ea spec.
- EVIDENCE: 01_RAW/CQC_FINAL.json gate_details.Q2 (d2_pin_universe);
  01_RAW/D2_MUTATION_RESULTS.json (D2-M1..M8 all causal).

## S-D2-02

- SUPERSEDED_CLAIM: the THREE-P2 FINAL_REPORT described the corrected Q2 as
  re-deriving the effective_address object with applicability chosen by the
  pin's own claim, and reported the 46/46 EA coverage as the Q2 closure
  measure; the coverage was real for the pins PRESENT, but the gate did not
  establish that those were ALL the required pins, nor that a pin could not
  escape EA validation by relabelling itself.
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/FINAL_REPORT.md`
- ORIGINAL_EXCERPT: `CORRECTION: gate_q2 now independently re-derives, for every JSON pin where a`
- ORIGINAL_EXCERPT: `Measured: 46 EA pins checked, 46 re-derived, 0`
- NEW_STATEMENT: THIS run's Q2 coverage statement is the
  Q2_PIN_UNIVERSE_COVERAGE enumeration (roster-bound bidirectional
  multiset + per-claim identity/role + declared-totals agreement +
  expected-role-driven EA applicability + registry tamper check) in
  ADDITION to the carried effective_address EXE re-derivation; the 46/46 EA
  coverage is reported as exactly what it is (all EXPECTED mem-role pins
  re-derived), never as a JSON-closure claim.
- EVIDENCE: 01_RAW/CQC_FINAL.json gate_details.Q2; D2-M1/D2-M3 (compound
  kind+EA removal), D2-M2/D2-M4 (whole-pin deletions), D2-M5/M6/M7
  (duplicate/extra), D2-M8 (synchronized omission) - all FAIL the gate.

## S-D2-03

- SUPERSEDED_CLAIM: the THREE-P2 internal PE-MASTER review verdict line
  endorsed the H2 and P2-3 claims with CONFIRMED status strings; the
  independent Desktop post-audit found D1 (H2 0F 73 /4) and D2 (Q2 pin
  universe/applicability) - the ENDORSED CLAIMS are superseded (the review
  itself remains a historical, advisory, pre-publication record - its
  process was never an independent post-audit and is not retroactively
  edited).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/PE_MASTER_REVIEW.md`
- ORIGINAL_EXCERPT: `P2_3_Q2_EFFECTIVE_ADDRESS = CORRECTED_RE_DERIVED_FROM_EXE (CONFIRMED: 46/46 coverage measured; M5/M6 causal)`
- ORIGINAL_EXCERPT: `H2_GROUP_OPCODES = CORRECTED_FAIL_CLOSED_VALIDITY (CONFIRMED)`
- NEW_STATEMENT: the corrected statuses of THIS run (measured by the fresh
  battery): D1_H2_0F73_4_STATUS = CORRECTED_PER_OPCODE_LEGAL_REG_TABLES;
  D2_PINSET_STATUS = CORRECTED_ROSTER_BOUND_BIDIRECTIONAL_MULTISET;
  D2_ROLE_APPLICABILITY_STATUS = CORRECTED_EXPECTED_ROLE_DRIVEN_EA. The
  M5/M6 causality remains valid and is reproduced (7/7 retained controls).
- EVIDENCE: 01_RAW/CQC_FINAL.json (gates + mutations); this ledger S-D1-01,
  S-D2-01.

## S-D2-04

- SUPERSEDED_CLAIM: the THREE-P2 QC_REPORT's Q2 summary wording presented
  the 133-pin/46-EA re-derivation as the corrected Q2 coverage; the summary
  was accurate for the per-pin EXE re-derivation but did NOT state that pin
  identity/completeness/multiplicity were unverified (they were - D2).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/QC_REPORT.md`
- ORIGINAL_EXCERPT: `Q2 (P2-3 corrected): 133 JSON pins re-derived (opcode_bytes, length,`
- NEW_STATEMENT: THIS run's QC_REPORT states the corrected Q2 coverage as
  the pin-universe binding PLUS the carried EXE re-derivation, with the
  D2 mutation evidence (8/8 causal).
- EVIDENCE: 01_RAW/D2_MUTATION_RESULTS.json; QC_REPORT.md of THIS package.

## S-CM-01

- SUPERSEDED_CLAIM: the immutable BASE (THREE-P2) commit message describes
  the published H2 rule with the shared {2,4,6} whitelist wording and the
  published Q2 as an EA-object re-derivation with `46/46 kind=mem` coverage
  - both statements encode the D1/D2 defects. History is NOT edited; this
  record supersedes the claims only.
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt`
- ORIGINAL_EXCERPT: `(H2) grouped-opcode validity fail-closed (0F BA reg 4-7 any mod; 0F 71/72/73 register-only, MMX reg {2,4,6}, SSE2 66 reg {2,4,6} + 66 0F 73 reg {3,7} legal PSRLDQ/PSLLDQ; F2/F3 rejected; reserved sub-opcodes REJECT)`
- ORIGINAL_EXCERPT: `measured coverage 46/46 kind=mem pins`
- NEW_STATEMENT: the corrected wording is THIS package's commit-message
  draft (HANDOFF.md): per-opcode 0F 73 tables with the /4 pair REJECTED;
  Q2 roster-bound pin-universe coverage with expected-role-driven EA
  applicability. The verbatim copy's fidelity to the immutable git object
  at 9d31a82b is machine-checked by gate Q14.
- EVIDENCE: Q14 commit_message_verbatim_fidelity=PASS;
  01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt.

## S-AUD-01

- SUPERSEDED_CLAIM: none superseded by a BASE claim - this record executes
  the independent Desktop post-audit's retraction list verbatim, as the
  authority for this correction: the audited state's blanket claims
  (the H2-family closure wording, the Q2 JSON-closure wording, the
  implication that no P0/P1/P2 remained open in the correction scope, and
  the implication that the machinery was free of any blocker for dependent
  reuse) are retracted in THIS package's active claim surfaces;
  the audited state's TESTED original repairs are preserved, not reopened.
- SOURCE_FILE: `C:\Users\User\Documents\ChatGPT\PE\PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005\REPORT.md`
- ORIGINAL_EXCERPT: `Retract the audited state's blanket claims:`
- ORIGINAL_EXCERPT: `D1_H2_INVALID_73_4 = OPEN_P2`
- ORIGINAL_EXCERPT: `D2_Q2_PINSET_AND_APPLICABILITY = OPEN_P2`
- NEW_STATEMENT: after THIS correction, within the measured scope:
  D1_H2_0F73_4 closed in the oracle-verified fixture set;
  D2_Q2 pinset/applicability closed in the 8-mutation control set;
  OPEN_P0_P1_P2_IN_CORRECTION_SCOPE = NONE_AFTER_D1_D2_IN_TESTED_SCOPE
  (P0/P1: none identified by the audit or this run; the census's 2218
  unresolved rows are honest UNRESOLVED states, not open defects of the
  machinery); dependent reuse stays bounded to the measured boundary
  (the decoder is a fail-closed bounded instrument, NOT a general x86
  decoder).
- EVIDENCE: Desktop post-audit REPORT.md (verbatim quotes above); this
  package's D1/D2 controls; FINAL_REPORT.md honest-limits section.
