# SUPERSESSION_LEDGER — PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004

Governance form: **superseded statement → supersession finding → corrected
canonical interpretation.** The superseded statements are from the C1-correction
package (PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_
R1_20261004, published at BASE 97bdf959cb742490a0e974bddf5a2dd25f93f5f7) and the
R1 package docs it corrected. Historical files were NOT edited (READ-ONLY;
git history preserves every published state; `git status` at this run's start
confirmed zero tracked-file modifications). This ledger IS the supersession
record — nothing was silently rewritten.

QUOTING DISCIPLINE (P3, this run — and the correction of row S-P3-1 below):
**"VERBATIM"** is reserved for actual byte-for-byte reproduction: every quote
below marked VERBATIM is a contiguous substring of the named file — every
character, line fold and indentation preserved (a quote may start mid-line; it
contains NO omissions and NO editorial changes). **"ORIGINAL_EXCERPT"** is used
where a quote contains abbreviations, ellipses, or editorial restructure.

Source of the supersession findings: the Desktop C1-C1 mutant C counterexample
(each destination row pointed at the OTHER payload field's REAL store with a
MATCHING displacement), reproduced on the PRISTINE BASE historical verifier by
this run (01_RAW/BASE_MUTANT_C_REPRODUCTION.json: BASE canonical QC_PASS 10/10,
BASE A/B falsifier DETECTED, BASE mutant C FALSE PASS — PAYLOAD_FIELD_DECODE_
CHECK=PASS, CLIENT_DESTINATION_MAPPING_CHECK=PASS, FULL_QC=QC_PASS) and closed
by the corrected gate (01_RAW/QC_MUTATION_BATTERY_POST_FIX.json: mutants A, B,
C all FAIL with FULL_QC=QC_FAIL; canonical copy passes).

## C1-C1 (P2) — the detection-scope claims of the published CLIENT_DESTINATION_MAPPING_CHECK

### Row S-C1C1-1 — "The Desktop-counterexample blind spot is closed"
- SUPERSEDED (C1-correction FINAL_REPORT.md, "C1 — what was fixed", item 2,
  published at 97bdf95) — VERBATIM (byte-exact contiguous excerpt, original
  line folds preserved):
  ```
  CLIENT_DESTINATION_MAPPING_CHECK **FAILS** — both mutants DETECTED. The
     Desktop-counterexample blind spot is closed.
  ```
- SUPERSESSION FINDING: the claim was OVERBROAD as a completeness statement.
  The two published mutants (destination-cell swap; destination+displacement
  swap with old VAs) are detected, but the mutant class "each row pointed at
  the OTHER payload field's REAL store VA with a MATCHING displacement"
  (Desktop mutant C) passes the published verifier UNDETECTED — reproduced on
  the pristine historical verifier by this run (false PASS, 10/10, with every
  historical per-row verdict `dest_eq_disp=True`, `bytes_match=True`,
  `pass=True`).
- CORRECTED INTERPRETATION: the blind spot class "a real MOV to the right
  displacement somewhere else" is closed by the corrected gate of THIS package
  (03_SCRIPTS/qc_targeted_c1c1.py TQ2): three simultaneous identities (payload
  field identity → store instruction identity → destination field identity)
  against a hard-coded, byte-backed parser-sequence oracle; the A/B/C battery
  plus canonical negative control is the operative falsifier set
  (MUTANT_C_POST_FIX_DETECTED = YES). C1_C1_PAYLOAD_INDEX_TO_STORE_IDENTITY =
  FIXED_AND_VERIFIED; C1 = CLOSED_FOR_AUDITED_STATE (audited scope).

### Row S-C1C1-2 — detection duty assigned to the A/B falsifier (ledger wording)
- SUPERSEDED (C1-correction SUPERSESSION_LEDGER.md, row S-C1-3, "CORRECTED
  INTERPRETATION", published at 97bdf95) — VERBATIM (byte-exact contiguous
  excerpt, original line folds preserved):
  ```
  honest record of the counterexample, and the detection duty is assigned to the new
    CLIENT_DESTINATION_MAPPING_CHECK whose mutation falsifier FAILS on the swapped
    mapping (both mutants).
  ```
- SUPERSESSION FINDING: "(both mutants)" understates the detection duty — a
  third mutant class in the SAME counterexample family passed that falsifier.
- CORRECTED INTERPRETATION: the detection duty is now assigned to the corrected
  CLIENT_DESTINATION_MAPPING_CHECK of THIS package (identity oracle + A/B/C
  battery). The C1-correction package's verifier and its 01_RAW records remain
  historical measurement records (untouched); its verdict on the CANONICAL
  table (PASS) remains valid — the canonical table also passes the corrected
  gate.

### Row S-C1C1-3 — R1 QC_REPORT.md QC-7 scope-limit parenthetical
- SUPERSEDED (R1 QC_REPORT.md, QC-7 row, published at 97bdf95) — VERBATIM
  (byte-exact contiguous excerpt):
  ```
  it is verified by the correction package's CLIENT_DESTINATION_MAPPING_CHECK (pinned-EXE store instructions + A/B mutation falsifier)
  ```
- SUPERSESSION FINDING: the parenthetical credits the then-published verifier
  with the destination verification; that verifier proved only
  displacement-consistency + bytes-at-VA, not the payload-index → store-VA
  identity (mutant C passed it).
- CORRECTED INTERPRETATION: the destination mapping is verified by the
  corrected CLIENT_DESTINATION_MAPPING_CHECK of THIS package (three identities
  vs the hard-coded byte-backed parser-sequence oracle + A/B/C falsifier +
  canonical negative control). The R1 file is READ-ONLY history — the
  corrected reading lives here and in this package's FINAL_REPORT/QC records.

### Row S-C1C1-4 — R1 QC_REPORT.md ANTI-CIRCULARITY #1 wording
- SUPERSEDED (R1 QC_REPORT.md, ANTI-CIRCULARITY statement 1, published at
  97bdf95) — VERBATIM (byte-exact contiguous excerpt, original line folds
  preserved):
  ```
  The payload→destination mapping is now guarded by the correction
     package's CLIENT_DESTINATION_MAPPING_CHECK, whose A/B mutation falsifier FAILS on
     the swapped documentation mapping (both the Desktop-style destination-only swap
     and a fully self-consistent swap) while the raw VFS values stay unchanged.
  ```
- SUPERSESSION FINDING: same class as S-C1C1-1 — the guard as then implemented
  accepted mutant C.
- CORRECTED INTERPRETATION: the mapping is guarded by the corrected gate of
  THIS package; its anti-circularity statement is recorded in
  01_RAW/QC_TARGETED.json (tq2 anti_circularity), 01_RAW/ORACLE_EVIDENCE.json,
  and this package's FINAL_REPORT section 3.

### Row S-C1C1-5 — R1 PARSER_CHAIN.md destination-table verification claim
- SUPERSEDED (R1 PARSER_CHAIN.md, "Destinations" intro, published at 97bdf95) —
  VERBATIM (byte-exact contiguous excerpt, original line folds preserved):
  ```
  byte-verified against the pinned-EXE
  store instructions by the correction package's CLIENT_DESTINATION_MAPPING_CHECK
  (PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004,
  including an A/B-swap mutation falsifier).
  ```
- SUPERSESSION FINDING: "byte-verified" + the A/B falsifier credit is the same
  overbroad detection-scope claim (the table itself and every destination
  pairing remain correct; what failed was only the VERIFIER's ability to
  reject a swapped-identity table).
- CORRECTED INTERPRETATION: the destination table is verified at IDENTITY
  level by this package's corrected gate; the canonical table passes it, and
  the A/B/C falsifier proves swapped-identity tables FAIL.

## P3 (bounded) — ORIGINAL_EXCERPT vs VERBATIM labeling

### Row S-P3-1 — blanket "VERBATIM" claim of the C1-correction supersession ledger
- SUPERSEDED WORDING (C1-correction SUPERSESSION_LEDGER.md header, published at
  97bdf95) — VERBATIM (byte-exact contiguous excerpt, original line folds
  preserved):
  ```
  The original statements below are
  VERBATIM from parent commit `4c1205342abd1b051f72fab9932532b1f0ed86fe` (the R1
  publication).
  ```
- FINDING: over-broad as a blanket label. Several quoted entries in that
  ledger are abbreviated excerpts with ellipses and/or editorial Markdown, not
  byte-for-byte reproduction — e.g. its row S-C1-1 ORIGINAL quote
  `"Parser raw↔decoded roundtrip: ... re-parsed from raw bytes **with the
  byte-decoded destinations**; ..."` (the "..." are the ledger author's
  omissions and the `**...**` is editorial emphasis inside the quote), and its
  S-C2-1 quote folds multiple doc locations into one editorially restructured
  list. Those entries are ORIGINAL_EXCERPTs.
- CORRECTED INTERPRETATION: reserve "verbatim" for actual byte-for-byte
  reproduction (as this ledger does); use ORIGINAL_EXCERPT where entries
  contain abbreviated excerpts/ellipses/editorial Markdown. The historical
  file was NOT edited (READ-ONLY); this row IS the correction record.

## What is NOT superseded (explicitly preserved)

- The canonical destination mapping itself: payload[0]/id2→template+0x00,
  payload[1]/A→template+0x08, payload[2]/B→template+0x04, payload[3]/C→
  template+0x0C, payload[4]/D_f32→template+0x10 — UNCHANGED and now verified
  at identity level (the canonical table passes the corrected gate).
- C2_CLASS_SELECTOR_PROPERTY_TAG = CLOSED_FOR_AUDITED_STATE (CLASS_SELECTOR
  0x4E26 = 20006 vs PROPERTY_TAG 6 — the layered identity, its byte pins, and
  the fallback-branch SEPARATE/UNKNOWN boundary).
- S1_STATIC_MECHANISM = PRESERVED_CONFIRMED; PARSER_TO_RUNTIME_VALUE_SEAM =
  CONFIRMED; CONTAINER_ROLE = DEFINITION_REGISTRY;
  SIBLING_KEY_16083_LOOKUP = CONFIRMED_STATIC_CONDITIONAL_PATH.
- RECORD_A {id2=16083, A=410620, B=0, C=0, D_f32=0.49950098991394043};
  RECORD_B {id2=4508, A=296445, B=296446} — values UNCHANGED (TQ1 re-verified).
- The narrowed QC-7 scope (PAYLOAD_FIELD_DECODE_CHECK = physical payload
  values at fixed file offsets — all it ever did).
- The FUN_00730C90 failure-path ZERO-WRITE description; FUN_0040DE60
  cursor-advance/flag-zero semantics; all instruction-start corrections
  (0x00730D14 / 0x00730D42 / 0x00730D69 / 0x00730D70 / 0x0072F5A5 / 0x0072F822 /
  0x004C54B2 / 0x0072FA6B) and their negative controls.
- The receiver-provenance chain (FUN_00452490 wrapper → FUN_0072FA30 loader,
  ECX preserve @0x0072FA6B / recover @0x0072FBD4; no singleton call in the
  loader extent).
- All historical packages, raw JSON evidence, scripts, and manifests (READ-ONLY
  measurement records of their publications), including the C1-correction
  package's own published records and the R1 package.
- The next-experiment identity (SPECIFIC_GETTER_RESULT_PROVENANCE with the
  OPEN taxonomy) — designed-not-executed, wording intact (TQ7 re-verified).
- PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED (level unchanged);
  PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED;
  WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.
