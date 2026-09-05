# PROPOSED_DOC_CORRECTIONS_R2 — PE-NIF-CLAIM-EVIDENCE-LOCK-R2

STATUS: PROPOSALS ONLY. Nothing below has been applied. The repo, docs/nif, wiki,
historical runs and canon are UNCHANGED by this run. An authorized applier (after the
next independent post-audit) must review, then apply. This document SUPERSEDES the
corresponding defective items of R1's 06_REPORT/PROPOSED_DOC_CORRECTIONS.md per
05_ANALYSIS/SUPERSESSION_MAP.csv; R1 items not listed here remain as proposed in R1.

Correction areas keyed to the R2 prompt: A = population counters, B = candidate-formula
wording, C = lossless sidecars, D = proposal wording/execution-provenance, E = gates.

## P1R2 — docs/nif/09-semantics.md (wiki target reference @ 077b8a4, SHA bb22d518...)

### P1R2-5 (supersedes R1 P1-5; claim C2-D-01): morph trailing-values wording
- OLD (R1 P1-5 proposed): "[9 × f32 delta triples — grouping structural; target quantity
  UNVERIFIED (position vs other; the 3-states-×-XYZ reading is an open hypothesis)]"
- NEW: "[9 × f32 trailing values; grouping and semantic role UNVERIFIED — the tested
  variable-k model consumes 9 × f32 after the weight list; grouping them into three
  triples (e.g. 3 morph states × XYZ) is an OPEN HYPOTHESIS, not an established
  structure; divisibility of nine does not establish the grouping]"
- Scope limits that MUST travel with this wording (unchanged from the justified R1
  corrections): the parser takes the SMALLEST k in 1..8 whose weight prefix sums ≈1.0
  (first-match; segmentation uniqueness NOT proven); byte-exact on 2,093/2,427
  classifier-real spans (86.2%; the 'real-record' class is a hypothesis-aligned
  classifier) and 3,186/6,167 all fit spans; 334 real-record spans fit no tested
  grammar; observed k ∈ {1,2,3,4} on 9.3.5 exact examples and k ∈ {1..5} on 2003.

### P1R2-6 (supersedes R1 P1-6; claim C2-D-03): d/c measured-first wording
- OLD (R1 P1-6 proposed): "**d==c is consistent with the file being unchanged since its
  last registration** (61.42% in 9.3.5 / 60.80% in 2003; the biconditional is not
  established — CRC collisions, byte-restoration and unobserved registering events are
  not excluded)"
- NEW: "**Measured: d==c for 3,435/5,596 entries in 9.3.5 (61.42%) and 3,299/5,426 in
  the 2003 corpus (60.80%); d is stable on 5,205/5,208 byte-identical era pairs
  (exceptions 524071.nif, 524077.nif, 524083.nif).** Hypothesis (SEPARATELY LABELED,
  not observed): d behaves as a carried-forward registration CRC — no writer, packer or
  registration event was observed in any run to date. d==c is CONSISTENT WITH the file
  being unchanged since its last registration; the biconditional is not established
  (CRC collisions, byte-restoration and unobserved registering events are not
  excluded)."
- Note: the registration history stays a hypothesis; the measured quantities lead.

## P2R2 — docs/nif/10-containers-corpus.md (reference @ 077b8a4, SHA 0b197ed4...)

### P2R2-1 (supersedes R1 P2-1; claim C2-D-03)
- OLD (R1 P2-1 proposed): "registration; d==c is consistent with unchanged-since-
  registration (biconditional not established — see ch09 note).**"
- NEW: "registration; MEASURED: d==c 3,435/5,596 (61.42%) and 3,299/5,426 (60.80%),
  d stable 5,205/5,208 byte-identical era pairs (exceptions 524071/524077/524083.nif);
  the registration reading is a separately labeled hypothesis (writer not observed);
  d==c is consistent with unchanged-since-registration, biconditional not
  established.**"

### P2R2-2 (supersedes R1 P2-2 INCLUDING its NOTE; claims C2-A-02/A-03/A-05)
- The R1 P2-2 main replacement (scoped "tested" conclusion) REMAINS VALID and is
  restated unchanged in intent: "**Conclusion (CONFIRMED at the tested scope): in the
  21 tested grammar claims on the 2003 and 9.3.5 Models.bnt corpora (5,426/5,426 +
  5,596/5,596 parse closure; note 5,208/5,422 shared files are byte-identical across
  eras), every byte-exact grammar reproduced at 100% and the rare-family and importer
  pattern censuses were count-identical. All drift observed in the tested claims was
  CONTENT; no grammar-level drift was found. No claim is made about untested claims,
  other archives, or other versions.**"
- CORRECTED NOTE (replaces the R1 NOTE; the R1 NOTE's "morph in 29" and the
  validated-on-changed-payloads reading are superseded):
  "Changed-payload ASCII-NAME PRESENCE (2003 side; this is name presence in the
  payload bytes — NOT a statement that family blocks were grammar-validated on these
  files): among the 214 changed pairs, the names appear in animation 214 unique files
  (214 occurrences), texture 214 (214), importer 214 (214), shader 9 (9), morph 3
  (29 occurrences: 548296.nif=13, 548808.nif=13, 566482.nif=3). All 4 old-only 2003
  files contain animation/texture/importer names (1 each); shader and morph names are
  absent. Intra-block byte-level witnesses were NOT established (coarse name-to-next-
  name span heuristic only)."

## P3R2 — docs/nif/11-open-problems.md (reference @ 077b8a4, SHA 5fd138f2...)

### P3R2-1 (supersedes R1 P3-1; claim C2-D-03)
- OLD (R1 P3-1 proposed): "d==c consistent with unchanged-since-registration
  (biconditional not established; c_eq_d 3,435/5,596 = 61.42%; …)"
- NEW: "MEASURED: d==c 3,435/5,596 (61.42%) and 3,299/5,426 (60.80%); d stable
  5,205/5,208 byte-identical era pairs (exceptions 524071/524077/524083.nif);
  registration = separately labeled hypothesis (writer not observed); d==c consistent
  with unchanged-since-registration (biconditional not established)"

### P3R2-2 (R1 P3-2 remains valid; unchanged)
- "SEMANTIC closure = PARTIAL — the table above is the honest list of what remains
  unknown AT THE CURRENT EVIDENCE LEVEL; claims outside this documentation's tested
  scope are neither closed nor asserted." (restated from R1 P3-2; not superseded)

## P4R2 — docs/nif/README.md (reference @ 077b8a4, SHA 4f976581...)

### P4R2-3 (supersedes R1 P4-3 / C-DOC-01; claim C2-D-02)
- OLD (R1 P4-3 proposed): "This is the byte-complete, evidence-graded documentation of
  the NIF binary format as used by Project Entropia (parse closure 100% on both
  Models.bnt eras; per-family semantic status in the state table below)"
- NEW: "This is evidence-graded documentation of the NIF binary format as used by
  Project Entropia FOR THE TESTED CORPORA (both Models.bnt eras: 5,426/5,426 +
  5,596/5,596 parse closure = parser FILE-CONSUMPTION coverage). Field coverage and
  segmentation uniqueness are PARTIAL (e.g. the morph record retains first-match
  segmentation ambiguity; several v4 fields remain open) and per-family semantic
  status is graded in the state table below. 'Complete' at any stronger level
  (byte-complete, all-fields, unique segmentation, closed semantics) is neither
  claimed nor implied."
- The four separated metrics: (1) parser file-consumption coverage: 100% on the two
  tested corpora; (2) field coverage: partial (open fields listed per family);
  (3) segmentation uniqueness: not proven (morph first-match; R34 caveat 2);
  (4) semantics: per-family graded statuses. Do not collapse these into one word.

### P4R2-1, P4R2-2 (R1 P4-1, P4-2 remain valid; unchanged — f1 type-code enum and
### graded mode-semantics wording)

## P5R2 — run REPORT texts (ledger entries only; historical files are NOT edited)

### P5R2-1 / P5R2-2 / P5R2-3 (R1 P5-1/P5-2/P5-3 remain valid; unchanged)
- R32 "10 of 45" → 9 of 45; R40 unit-mixed sizes → 9,213 / 13,326 bytes; "+236 lines"
  = combined added (net +225). All remain ledger entries; historical reports stay
  immutable.

### P5R2-4 (NEW; claims C2-D-04a/04b — execution-history record)
- Correction-ledger entry: the recorded control_r1.cjs execution history is TWO
  executions (exec-1 hash 6A296CC7…, exec-2 hash 5AD889D3…, both recorded in
  SHA256_CONTROL.txt BEFORE execution). The "three iterations" documented in R1 LOGS.md
  refer to generate_claim_matrix.cjs — a DIFFERENT instrument. The chat statement
  "3-execution history" is a handoff/record MISMATCH; no third control execution is
  recorded and none is invented. The chat-side origin of the "3" is UNRESOLVED (no
  chat access); the recorded side is CONFIRMED at two.

### P5R2-5 (NEW; claims C2-D-05a/05b — proposal-count vs replay record)
- Correction-ledger entry: R39's 45 proposals were COUNTED/READ (EDIT_PROPOSALS.json
  array length 45; apply state evidenced by git 077b8a4^ → 077b8a4 and the wiki state),
  and R40's 9 proposals were REPLAYED byte-exact (re-application reproduces the
  applied blobs 4f976581…/bb22d518…). "45+9 applied byte-exact" as a combined REPLAY
  claim is NOT evidenced by R1 and must not be stated. A full 45-proposal byte-exact
  replay was neither performed nor recorded (performing it is a separate authorized
  task, not this correction run).

## P6R2 — normalized manifests (supersedes R1 P6; claims C2-C-01..04)
- R1's 12 normalized sidecars are SUPERSEDED by the 12 LOSSLESS sidecars in
  05_ANALYSIS/NORMALIZED_MANIFESTS/*.artifact_index.lossless.csv (RAW_BYTES_CONTRACT
  v1): every original row preserved as exact raw bytes (base64 + original-row SHA256),
  original path + original manifest SHA256, row position, per-row terminator,
  recoverable original fields (header mapping ONLY for strict rows), normalization
  rule and uncertainty per row. Malformed-row semantic reconstruction is withheld as
  UNRESOLVED (bytes retained; displaced computed_by/role NOT inferred). Full-file
  byte reconstruction verified 12/12 (SHA256 equality) by the builder AND by the
  independent Python checker.
- The original manifests are IMMUTABLE and were not modified. A changing
  PE_AUTO_LOOP.json hash is a mutable pointer, not corruption; that file was not
  written or restored.
- The R39 GAP_ANALYSIS row's original role text ("per-file gaps, priorities,
  orphan/ambiguous-label classification") survives byte-exactly; R1's sidecar role
  ("per-file gaps [priorities]") is the documented lossy case.

## P7R2 — d-candidate formula wording (supersedes R1 C-R36-05/G8/CE-5(c); claims C2-B-01..03)
- Canonical replacement wording wherever the tested-formula result is stated:
  "Nine listed candidates have zero matches in each tested corpus (adler32(payload),
  CRC32(name), CRC32(name+0x0A), adler32(name), CRC32(name+size_le),
  CRC32(size_le+name), FNV-1a(name), size, offset — each 0/5,596 and 0/5,426). The
  payload CRC candidate matches 3,435/5,596 and 3,299/5,426, so it is not a universal
  formula for d either. No conclusion excludes all untested deterministic functions."
- Explicit denominators mandatory: every candidate count is stated as n/5,596 and
  n/5,426; never as a bare "all exact-0".

## P8R2 — scope-population wording rule (claims C2-D-01..03; kept from R1 where justified)
- "Every grammar", "all", "100%", "complete" must be tied to an explicit measured
  population (e.g. "the 21 tested grammar claims on the 2003 and 9.3.5 Models.bnt
  corpora"). The prior justified f1, morph, era and semantic retractions of R1
  (P1-1..P1-4, P1-7, P3-2, P4-1, P4-2, P5-1..3, P7) remain valid and are preserved;
  only the items superseded above change.
