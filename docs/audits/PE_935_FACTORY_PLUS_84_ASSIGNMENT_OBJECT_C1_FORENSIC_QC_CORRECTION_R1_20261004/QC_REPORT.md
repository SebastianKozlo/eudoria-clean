# QC_REPORT — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004

QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C1_FORENSIC_QC_CORRECTION (executor
self-check, explicitly NOT an independent PE-MASTER audit). Raw machine
records: 01_RAW/CQC_FINAL.json (gates Q1-Q14 + AUX), 01_RAW/
CQC_NEGATIVE_CONTROLS.json (controls A-F), 01_RAW/CQC_DECODER_UNIT_TESTS.json
(03_SCRIPTS/cqc_battery.py). Every gate status is DERIVED from measured inputs
on disk — no hard-coded PASS. Outcome-conditional: QC PASS means the
corrected claims accurately match evidence and uncertainty, NOT that all
census candidates were solved (828 unresolved write candidates and the
NOT_ESTABLISHED invariants are the corrected honest states, not failures).
FAIL is reserved for unsupported/contradicted positive claims, missing
claimed-outcome evidence, or scope/governance violations.

## Verdict

**QC_VERDICT = QC_PASS (14/14 gates PASS + AUX quotecheck 42/42 PASS, 0
failures).**

## Gate table

| Gate | Checks | Result | Key measured values |
|---|---|---|---|
| Q1 | baseline + EXE identity | PASS | local HEAD = origin/master = actual remote master = a0e176803aed23b19040d4310de1668efec4511f (BASE_SHA); EXE 8,015,872 B / SHA256 E7785430...F31 exact pin match |
| Q2 | authoritative same-VA pin integrity | PASS | 133 ledger records re-derived from disk+EXE: opcode_bytes == EXE[va:va+len] for every record; every promoted rel32 target re-computed as va+5+signed_rel32 from the SAME VA; every operand raw byte block re-read at va+operand_offset; the 2 declassified records re-verified (byte != E8); C1 battery fail_count=0; 0 same-VA violations, 0 field mismatches |
| Q3 | pin negative-control battery A-F | PASS | A: corrupted ctor-entry mutant FAILS the raw-evidence gate while the canonical bytes PASS; B: the mutated enumeration range (bound excluding 20006) FAILS the membership gate while membership is derived from the MEASURED values (never literal-only); C: non-CALL VA -> CALL_VALIDATION=FAIL, NO accepted target; D: corrupted callback immediate FAILS the pin/immediate gate while the canonical immediate (0x0070BEF0) passes; E: the E8-inside-immediate synthetic (B8 E8 01 00 00 00 C0 C3, candidate offset 1) -> NO target promoted (opcode-byte coincidence + in-range apparent target insufficient); F: the synthetic ESP+SIB row (89 84 2C 84 00 00 00, EA = ESP+EBP*1+132) -> ADDRESS_PROVENANCE=UNRESOLVED, CLASSIFICATION=UNRESOLVED (NOT rejected as wrong object from the base name) |
| Q4 | signed displacement semantics | PASS | every NEGATIVE_DISP8_MINUS_0x7C_CONTROL row (385) has signed displacement -124; every other row has effective +132; both known stores re-measured at +132; 0 bad rows |
| Q5 | decoder unit battery + re-decode consistency | PASS | mandated controls: 8B 04 85 00 00 00 00 -> 7; 8B 04 24 -> 3; 66 B8 01 00 -> 4; 89 86 truncated -> REJECT (no length fabricated); every one of the 2,612 census rows re-decodes identically (0 bad rows); decoder coverage over the 8 historical counted-function windows: no aborts |
| Q6 | trusted boundary policy | PASS | every BOUNDARY_CONFIRMED census row names a declared trusted source (KNOWN_FUNCTION_ENTRY / CC_PADDING_DELIMITED_START / RET_DELIMITED_START); zero forbidden not-an-instruction/immediate-data assertions in any census reason; CONTROL E passes |
| Q7 | full EA/SIB provenance handling | PASS | every decoded census row carries the full effective-address field set (operand_width, base, index, scale, raw/signed/effective displacement, provenance status); CONTROL F passes; the 0x00812944 spot-check: census fields == a fresh machine decode of the same bytes (base=ESP, index=NONE — SIB index 100b means NO INDEX; the historical census displayed the impossible [ESP+ESP*1+0x84], SUPERSESSION_LEDGER S-31) |
| Q8 | EBP/ESP provenance discipline | PASS | every REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE row documents its provenance_basis (window-verified layout evidence or machine-checked manager-this flow) — zero register-name rejections; zero ESP/EBP-based write rows resolved to any rejection (all UNRESOLVED with ADDRESS_PROVENANCE=UNRESOLVED) |
| Q9 | regenerated census arithmetic + distinct denominators | PASS | classification tally re-summed from the CSV = 2,612 rows exactly (1003 + 1217 + 385 + 5 + 2); derived CENSUS_UNRESOLVED_ROWS = 1217 == summary; derived FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES = 828 == summary; the distinct denominators verified: 1217 = 828 write candidates + 389 boundary-unresolved read/LEA rows; all other quantities cross-match the summary |
| Q10 | known stores physical re-pin | PASS | 0x0070D013 = 89 9E 84 00 00 00 + boundary CONFIRMED + census classification KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE + store class INITIALIZATION_NULL in the row; 0x0070C71E = 89 86 84 00 00 00 + CONFIRMED + KNOWN_CONFIRMED + store class CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE |
| Q11 | factory identity/enumeration from measured evidence | PASS | membership 0x4E26 in [0x4E20, 0x4E4C) derived from the MEASURED pin immediates (0x4E20 from the ESI init @0x007080D6, 0x4E4C from the CMP bound @0x007080EB); CONTROL B mutant fails; dispatcher entry-5 table value measured 0x0073C8D8; second range measured 0x5DC1..0x5DD2 |
| Q12 | object structural identity | PASS | 0xA4 == 164 (machine-measured imm32) with the FACTORY size 0x118 == 280 recorded separately; ctor call target 0x00972380 VALIDATED in the ledger; extent 0x00972380..0x009724DA measured; cursor pin VALIDATED (0x00972427); all 7 tail/return pins VALIDATED; the corrected terminology strings present in FINAL_REPORT |
| Q13 | vtable/polymorphism scope + phrase sweep | PASS | C3 machine search DIRECT_VPTR_STORE_IN_EXAMINED_CTOR=NOT_OBSERVED (decode completed, 1 offset-0 store found, base EDI not the this-register); ASSIGNED_OBJECT_VTABLE = UNVERIFIED + OBJECT_POLYMORPHISM = NOT_ESTABLISHED present; KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES measured (3 examined callsites); superseded-phrase absence sweep over FINAL_REPORT.md, HANDOFF.md, INPUT_IDENTITIES.md and both CSVs: ZERO hits (SUPERSESSION_LEDGER.md is the designated old-claim record, verified by the AUX quotecheck instead) |
| Q14 | nonclaims + forbidden scope + predecessor preservation | PASS | all 30 required corrected/preserved strings verified in FINAL_REPORT (runtime-value nonclaims, closure invariants, the forbidden-scope NO block, the preserved predecessor chain incl. WRITER_FUNCTION = FUN_009777F0 / WRITER_VA = 0x00977810 / TAG6_TO_ID10 = PRESERVED_CONFIRMED / SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED / TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD, and the function-ledger hygiene strings); instrument open()-argument census: the only opened files are the pinned EXE + package artifacts + the READ-ONLY historical package files for the quotecheck — zero .vfs/.bnt/.nif/.ark literals in any open() call, zero http markers |
| AUX | supersession quotecheck | PASS | 42 verbatim excerpts across 31 records (S-01..S-31) machine-verified as real substrings of their named READ-ONLY historical source files; 0 failures |

## QC hygiene notes (honest record)

1. The battery's FIRST execution caught real defects and forced their
   correction in the single targeted repair pass (per the correction execution
   limit, no further iteration): (a) six verbatim-excerpt transcription
   errors in SUPERSESSION_LEDGER.md (the historical S1/S3 JSON records are
   pretty-printed multi-line — single-line reconstructions were not
   substrings; one em-dash vs hyphen; one line-wrapped quote) — all replaced
   with exact single-line excerpts, now quotecheck-verified 42/42; (b) the
   active-claim-surface sweep (Q13) found this package's own FINAL_REPORT/
   HANDOFF quoting the superseded historical phrases while DESCRIBING the
   supersession — the quotes were moved to SUPERSESSION_LEDGER.md (the
   designated old-claim record) and the active surfaces now reference them by
   record ID, restoring a zero-tolerance sweep; (c) the Q7 spot-check had been
   built from the historical census's impossible "[ESP+ESP*1+0x84]" display —
   the fresh machine decode proved SIB index 100b means NO INDEX, which
   became the new SUPERSESSION_LEDGER record S-31 (a genuine F84-C2 discovery
   of the historical SIB-display defect); (d) the Q14 open-path census
   over-matched prose mentions of extensions in comments (now extracts only
   actual open() call arguments) and the http-marker check self-matched its
   own literal (now built from split literals). The committed 01_RAW records
   are the final pass.
2. The QC sweeps active claim surfaces (FINAL_REPORT.md, HANDOFF.md,
   INPUT_IDENTITIES.md, both CSVs); QC_REPORT.md itself is written after the
   battery and is not swept by it (same discipline as the historical
   packages; the AUX quotecheck independently verifies every historical
   excerpt against the READ-ONLY historical files).
3. QC re-execution hygiene: every instrument accepts --out/--csv overrides;
   re-running with defaults overwrites only THIS package's 01_RAW JSON/CSV —
   the committed record in git is the authoritative one for this run.
4. Q1's git components are run-time measurements (recorded in
   01_RAW/CQC_FINAL.json); the EXE identity component remains byte-exact on
   any re-run.

## Not applicable / unresolved states (outcome-conditional, legitimate)

- QC PASS does NOT resolve the 828 FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES
  or the 389 boundary-unresolved read/LEA rows — they are the corrected
  honest bounds within the examined encodings.
- EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED (invariant);
  EXAMINED_ENCODING_CANDIDATE_CLOSURE = CLOSED is scoped to the declared
  encodings/effective-address forms/trusted-boundary coverage.
- ASSIGNED_OBJECT_VTABLE = UNVERIFIED and OBJECT_POLYMORPHISM =
  NOT_ESTABLISHED are the honest global states; only the direct observation
  DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED is claimed.
- ULTIMATE_VALUE_SOURCE = UNKNOWN; the runtime-value nonclaims
  (ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED,
  WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED,
  FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT = NOT_ESTABLISHED) stand.
- No gate required positive evidence for a claim this correction does not
  make: UNRESOLVED/NOT_VERIFIED/NOT_ESTABLISHED are legitimate measured
  states, not QC failures.
