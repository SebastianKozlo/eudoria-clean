# PE-NIF-CLAIM-EVIDENCE-LOCK-R2 — FINAL REPORT (CORRECTION PACKAGE)

RUN_ID = PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054
ITERATION = R2 (correction run following the independent post-audit of R1
PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119)
MILESTONE MAPPING = EU935-M2 contribution only; NO milestone advancement
SCOPE = repair the R1 correction package's own evidence defects (Areas A-E) and
publish the bounded package; proposals remain proposals; no wiki application
BASE_SHA (repo, captured; never reset) = c0c2f2fca328366364928aeee3c6249c24025446
HEAD_SHA = the publication commit that adds this package directory (reported in the
final chat handoff; a commit cannot embed its own hash — the run-dir copy of this
report is byte-identical to the committed one)
PRIMARY_TARGET = PCG 9.3.5 Models.bnt (5,596 entries) + 2003-era Models.bnt (5,426
entries; separately hash-pinned comparison corpus, NOT interchangeable target
evidence)
SOURCE ERA/BUILD = PCG 9.3.5 (Entropia Universe 9.3.5, pcg_install) and the
2003-era container (01_Original_Files/BNT_Models; era label inherited provenance)
EXECUTED BY = pe-reconstruction (single bounded round; no nested agents)
DATE = 2026-09-05

## 0. P0 = CORRECTION_PACKAGE_EVIDENCE_SELF_CONSISTENCY — addressed

Every correction demanded by the independent post-audit was re-derived FROM RAW
PHYSICAL EVIDENCE, never copied from the auditor: all counts recomputed in Node
(control_r2.cjs) AND independently in Python (run_gates.py) from the two containers;
sidecars validated against the ORIGINAL manifest bytes; the auditor's findings were
themselves independently checked (FINDING_DISPOSITIONS.csv — 7 ACCEPTED with
re-derived evidence, including one NEW R2 finding beyond the auditor list: the R39
manifest UTF-8 BOM that R1's .trim() silently stripped). One status per atomic
claim; a supersession map replaces the defective R1 representations without editing
any historical file. No wiki/canonical/loop/shared-tool write; no runtime work.

## 1. Inputs and integrity chain

- Prompt SHA256 verified before execution (R2G1): 46A2A99A9F1D03B4FE33F2FBFCA89D2440FD702188A3D020E9BF29A7A370E5ED.
- Mandatory reading completed: AGENTS.md + six 00_PROJECT_CONTEXT files; the external
  audit contract; the post-audit report + verification.json + verify.py (read-only,
  independently reproduced — not copied); the full R1 package (report, claim matrix,
  proposals, raw JSON, control source, gates, sidecars, logs, manifest) and its
  cited historical evidence (R32/R34/R35/R36 raw JSONs, R36 driver source, R39/R40
  results); docs/audits/README.md.
- Physical sources hash-locked (R2G2): PCG Models.bnt 395,412,868 B =
  c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0; 2003 Models.bnt
  375,322,581 B = 1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353f1cefd3524a6.
  Both BNT2 indexes parsed with bounds checks and exact consumption (5,596 / 5,426
  unique names).
- R1 immutability during this run re-verified (R2G17): 10 key R1 artifact hashes match
  the post-audit record exactly.
- Repo state: HEAD c0c2f2fc; untracked docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/
  (another writer) — untouched and excluded from the R2 commit.

## 2. Area A — population mismatch reproduced and fixed

Independent reclassification of both corpora by EXACT payload bytes (Buffer.equals /
bytes equality; not hash-only): 5,422 shared names = 5,208 byte-identical + 214
changed; 4 old-only (13563.nif, 261922.nif, 38579.nif, 524174.nif); 174 new-only;
sum invariants hold (R2G3, Python == Node).

FOUR counters kept distinct (never substituted):
1. ASCII occurrence count — COMPUTED.
2. distinct filename count — COMPUTED.
3. parsed block count — NOT_COMPUTED (ASCII scan is presence-only; block-boundary
   research is explicitly out of scope for this correction run).
4. successful family-validator count — NOT_AVAILABLE per-file: R35
   GRAMMAR_VALIDATION.json contains corpus-level aggregates only (texture 2003:
   v10 4,665/4,665 + v4 761/761 blocks over ALL 5,426 files); no per-file/per-family
   validator-result join artifact exists. Therefore NO grammar-validation claim is
   attached to family presence.

Corrected family presence (2003 side of the 214 changed pairs; ASCII-name presence):
- animation: 214 unique files (214 occurrences)
- texture: 214 unique files (214 occurrences)
- importer: 214 unique files (214 occurrences)
- shader: 9 unique files (9 occurrences)
- morph: 3 unique files (29 occurrences — 548296.nif=13, 548808.nif=13, 566482.nif=3)
Old-only (4 files): animation 4, texture 4, importer 4 unique files (1 occurrence
per file each); shader 0; morph 0.

Auditor counterexamples — REPRODUCED, not assumed:
- The R1 counting bug was reproduced EXACTLY by a stage-local faithful
  reimplementation of control_r1.cjs L163-179 over the same physical data
  (fixture_reproduces_r1_exactly = true): old-only counters double-increment
  (presence + whole-file diff overlap → 8 for the population of 4) and both
  counters increment per ASCII occurrence (morph "changed_files_with_block" = 29).
  The historical script itself was NOT executed or edited.
- NiVertexMorphExtraData = 29 occurrences in THREE changed files (13/13/3) —
  independently derived from the physical payloads in both implementations.
Synthetic invariants verified (R2G7): a family occurring 3x in one file counts as
ONE file (4 occurrences / 2 files across the synthetic corpus); absent family = 0;
an old-only file increments ONCE (the R1-style buggy counter yields 4 for one
file — DETECTED).

Affected R1 representations corrected: CLAIM_MATRIX C-R35-04 (→ C2-A-02/03/05),
gate G7, R1 final report Control 3, P2-2 NOTE, DENOMINATORS family-witness entry
(→ C2-A-06 four-counter taxonomy). Full list in SUPERSESSION_MAP.csv (18 rows,
each defect quote verified present in its R1 artifact — R2G15).

## 3. Area B — candidate-formula wording repaired

The TEN named candidates were PHYSICALLY recomputed over both full containers this
run (definitions read from the R36 driver source; Node hand-rolled CRC32/adler32/
FNV-1a cross-checked against Python zlib):
- NINE candidates exact-0 on BOTH corpora: adler32(payload), crc32(name),
  crc32(name+0x0A), adler32(name), crc32(name+size_le), crc32(size_le+name),
  fnv1a(name), size, offset (each 0/5,596 and 0/5,426).
- The tenth, d == crc32(payload): 3,435/5,596 (61.42%) and 3,299/5,426 (60.80%) —
  NOT universal, NOT exact-zero (this is exactly the d==c subset; c==CRC32(payload)
  re-verified 11,022/11,022 with 0 mismatches first).
- Three-way agreement: R2 Node == R2 Python == R36 historical FIELD_D_TESTS.json
  (20/20 candidate-era pairs, R2G8).
- d stability: 5,205/5,208 byte-identical pairs; exceptions exactly 524071.nif,
  524077.nif, 524083.nif (R2G9).

Superseded: R1 C-R36-05's "All 10 TESTED ... exact 0 counts on both full corpora"
and gate G8's "10 tested formula families (exact-0)" and COUNTEREXAMPLES CE-5(c) —
all REJECTED as worded (C2-B-03); corrected canonical wording in P7R2. KEPT
unchanged: the rejection of the universal registration biconditional (d==c iff
unchanged) and the rejection of "all deterministic functions excluded" (C2-B-04).
Claim-status tally recomputed for the R2 matrix: 24 rows = CONFIRMED 16, REJECTED 8
(R2G13); R1's own matrix is a historical artifact and was not edited.

## 4. Area C — genuinely lossless sidecars

12 new sidecars (05_ANALYSIS/NORMALIZED_MANIFESTS/*.artifact_index.lossless.csv)
under RAW_BYTES_CONTRACT v1: every original row preserved as EXACT raw bytes
(base64 of the line without terminator + per-row SHA256 + per-row terminator),
original manifest path + SHA256, row position, all recoverable original fields
(header mapping ONLY for strict rows; cell arrays always), normalization rule and
uncertainty per row. VERIFIED LOSSLESS by full-file byte reconstruction: the
reassembly of all rows (decode + terminators, in order) equals the original file
byte-for-byte — 12/12 SHA256 equality (R2G10, verified by BOTH the Node builder and
the independent Python checker using the strict csv module).

- Malformed rows (11 across 8 manifests — R30/R31/R32/R33/R35/R36/R38/R39):
  semantic reconstruction withheld as UNRESOLVED with bytes retained; displaced
  computed_by/role NOT inferred from positional cells. The R35 manifest's trailing
  blank line is preserved as EMPTY_LINE_PRESERVED (part of the original bytes).
- R39 GAP_ANALYSIS explicit test (R2G11): the original role text "per-file gaps,
  priorities, orphan/ambiguous-label classification" round-trips byte-exactly
  (decoded row == original line bytes; SHA a427edfc69522dc976297c983af9db75548cc9f295760d045dd770fe147799d4);
  reconstruction_status = UNRESOLVED (no silent truncation). R1's sidecar role was
  "per-file gaps [priorities]" — the loss is CONFIRMED (the same positional-merge
  mechanism also produced "…edit [before execution)]" on the R39 SHA256_DRIVER row).
- Quoting/escaping/newline policy validated on a synthetic fixture (mixed CRLF/LF,
  embedded quotes, quoted commas) plus the real sidecars (R2G12).
- Original manifests IMMUTABLE (R2G17 covers R1-side; the 12 historical manifests
  are re-hashed inside the sidecar source-identity checks). PE_AUTO_LOOP.json is a
  MUTABLE POINTER (live loop state; hash valid at read time only) — NOT written,
  NOT "restored".

## 5. Area D — proposals repaired WITHOUT applying

PROPOSED_DOC_CORRECTIONS_R2.md (PROPOSALS ONLY — nothing applied):
- P1R2-5: "[9 × f32 trailing values; grouping and semantic role UNVERIFIED]" (was
  "delta triples"); first-match/uniqueness limits and the classifier-conditioned
  denominators (2,093/2,427; 3,186/6,167) preserved.
- P4R2-3: "byte-complete" replaced by evidence-graded documentation FOR THE TESTED
  CORPORA with four separated metrics (parser file-consumption 100% on both corpora;
  field coverage partial; segmentation uniqueness not proven — morph first-match;
  semantics per-family graded).
- P1R2-6 / P2R2-1 / P3R2-1: measured-first d/c wording; registration = separately
  labeled hypothesis; writer not observed.
- P2R2-2: R1's scoped era-conclusion kept, its NOTE corrected to ASCII-name presence
  with the exact per-file numbers and no validator claim.
- P5R2-4 (execution history, resolved honestly): the recorded control_r1.cjs history
  is TWO executions (two pre-execution hashes in SHA256_CONTROL.txt); the three
  iterations in R1 LOGS.md belong to generate_claim_matrix.cjs — a different
  instrument. The chat "3-execution history" is a handoff/record mismatch; no third
  execution is recorded and none is invented (chat-side origin UNRESOLVED — no chat
  access; recorded side CONFIRMED at two).
- P5R2-5 (45 vs 9): R39's 45 proposals were COUNTED/READ (apply state evidenced via
  git); R40's 9 proposals were REPLAYED byte-exact. "45+9 applied byte-exact (replay)"
  is NOT evidenced by R1 and is not claimed; a full 45-proposal replay was neither
  performed nor recorded (and is not performed this run either).
- "Every grammar"/"all"/"100%" restricted to explicit measured populations; the
  prior justified f1/morph/era/semantic retractions of R1 are preserved.
- Finding disposition matrix: 7 rows, all ACCEPTED with independently re-derived
  evidence (F1-F5, F-PUB, R2-NEW-1); R1→R2 supersession map: 18 rows.

## 6. Area E — gates that DETECT failures

18 EXECUTABLE gates computed from fresh results by run_gates.py (independent
Python implementation; stdlib only), each recording MEASURED_QUANTITY / DENOMINATOR /
INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED
(02_LOGS/TEST_RESULTS.json; STAGE_ACCEPTANCE_GATES.csv). 4 HUMAN_REVIEWED wording
gates are separated (HR-1..4, pass=null by design). The suite EXITS NONZERO on any
violation and demonstrably FAILS on real defects: during this run it caught (a)
the exec-1 BOM crash (R39), (b) a 22-field sidecar row, (c) coverage-math and
assertion defects in its own intermediate state — all documented in 02_LOGS/LOGS.md.
Negative controls demonstrated on the immutable R1 artifacts (read-only fixtures):
- R1 old-only counter 8 → FAILS unique-file ≤ 4 (R2G4/R2G6);
- R1 morph "changed_files_with_block" 29 → FAILS the 3-unique-file invariant (R2G5);
- R1 C-R36-05 ten-exact-zero wording → FAILS the nine/ten invariant (R2G8);
- R1 sidecar role "per-file gaps [priorities]" → FAILS lossless round-trip (R2G11);
- R1 P6 "raw_text column" claim → FAILS structural inspection (no such column).
Corrected R2 outputs PASS all of these. Synthetic counter fixtures stored under
00_CONTROL/FIXTURES/. Human-reviewed wording gates are separate from the executable
suite (gate_type column) — R1's fixed-description gate ledger (generate_gates.cjs
static array, quote S11) is itself superseded as a presentation pattern; the R2
ledger is GENERATED from TEST_RESULTS.json by generate_gates_r2.cjs.

## 7. Claims summary (R2 CLAIM_MATRIX — 24 atomic rows, one status each)

- CONFIRMED 16 (era join; family presence as presence; four-counter taxonomy; nine
  exact-zero; payload-CRC subset; tested-list scope; c/d measured facts; 12/12
  lossless sidecars; R39 round-trip; malformed-row withholding; trailing-values
  scoped; measured-first registration presentation; two-execution record; 45/9
  distinction; R2 gate-suite detection).
- REJECTED 8 (R1 occurrence/double-increment counters AS file counts; R1
  validated-on-changed-payloads claim; R1 ten-exact-zero wording; R1 raw_text/lossy
  sidecar claim; "delta triples" grouping wording; "byte-complete" wording; the
  chat "3-execution history"; the chat "45+9 byte-exact replay").
- Tally verified by R2G13; full matrix with sources, denominators, counterexamples,
  independence and proposed wording: 05_ANALYSIS/CLAIM_MATRIX.csv.

## 8. Retractions / supersessions

All supersessions are recorded as NEW evidence (SUPERSESSION_MAP.csv, 18 rows);
no historical file was edited. Headline retractions (R1 representations, now
superseded): occurrence-as-file counters; the "validated on changed payloads"
witness claim; ten-exact-zero; the sidecar losslessness claim; "delta triples";
"byte-complete"; registration-foregrounded wording; the chat-only execution-count
and replay claims. R1 items that REMAIN VALID and are preserved: the f1 exception
wording (P1-1..P1-4), exporter-string grading (P1-7), era-scoped conclusion
(P2R2-2 main), open-problems scoping (P3R2-2), mode-semantics grading (P4-1/P4-2),
ledger entries (P5R2-1..3), vocabulary-census scoping (P8R2 keeps R1 P7's
justified retractions).

## 9. Known limitations / open questions

- Family presence is ASCII-NAME PRESENCE; parsed block counts were not computed and
  per-file validator joins do not exist in R35's artifacts (block-boundary research
  was deliberately NOT started — that would be a new research project, out of scope).
- Intra-block byte-level witnesses on the 214 changed files remain NOT established
  (the coarse span heuristic is unchanged; deferred as future bounded work).
- The chat-side origin of the "3-execution" and "45+9" statements is UNRESOLVED
  (no chat access); only the recorded side is asserted.
- The 45 R39 proposals were NOT re-derived byte-exact this run (no such replay is
  claimed; performing one is a separate authorized task).
- Era labels: PCG 9.3.5 is the primary target; the 2003-era container is a
  hash-pinned comparison corpus (inherited-provenance label, not newly dated).
- Morph trailing-value semantics remain UNVERIFIED (position vs other; 3×XYZ
  hypothesis open); segmentation uniqueness remains unproven.

## 10. Dependent prior claims / blast radius

- The R1 package remains PUBLISHED and immutable at c0c2f2fc; this R2 package
  supersedes its defective representations going forward. Auditors should read
  R1's CLAIM_MATRIX/gates/report THROUGH this supersession map.
- No downstream claim depends on the corrected counters being the OLD values; the
  corrections NARROW claims (presence vs validation; occurrence vs file; nine vs
  ten) — every affected consumer (wiki proposals, correction ledger) is itself a
  proposal pending post-audit, so no applied canon is affected. Blast radius is
  confined to the audit/documentation layer.
- Physical-evidence claims (c==CRC32 11,022/11,022; d==c subsets; d-stability;
  era join; f1 distribution; morph byte-fit denominators; k examples) were
  RE-VERIFIED unchanged — the correction package does not alter any byte-level
  measurement.

## 11. Gates and publication

- Content gate pass: 17/17 EXECUTABLE PASS (exit 0). Final package pass (adds R2G18
  artifact integrity): recorded in 02_LOGS/TEST_RESULTS.json; the ledger
  STAGE_ACCEPTANCE_GATES.csv is GENERATED from that file (no hand-written results).
- Publication (the ONLY authorized repo write): the complete R2 package copied
  byte-identically to docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/
  in SebastianKozlo/eudoria-clean (master), per-file SHA256 parity verified, staged
  as that single path (never git add -A), committed with RUN+subsystem+result, pushed
  origin master WITHOUT force (per-command -c http.sslBackend=openssl; TLS
  verification retained; no global config change), remote SHA verified. docs/nif,
  historical audit packages, canonical state and runtime code remain READ-ONLY; the
  untracked docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ (another writer's) is
  excluded. Execution/source SHA (BASE c0c2f2fc) is reported separately from the
  package-publication SHA (final HEAD, reported in the handoff).
- If any publication step could not be completed safely, the status would be
  EXTERNAL_AUDIT_INCOMPLETE with the exact blocker (see HANDOFF.md for the actual
  outcome).

## 12. What this run deliberately did NOT do

No wiki/canonical/Obsidian/INDEX application; no PE_AUTO_LOOP write or relaunch; no
shared-tool edit; no historical run/driver/manifest edit; no runtime/game/Ghidra
execution; no new morph semantics, world placement, XYZ, MAPRE or milestone
promotion; no block-boundary/uniqueness research project; no 45-proposal replay.
Independent post-audit is required before applying ANY proposal.

## FINAL HANDOFF BLOCK

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\01_RAW\RECOUNTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\05_ANALYSIS\CLAIM_MATRIX.csv; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\05_ANALYSIS\NORMALIZED_MANIFESTS; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\02_LOGS\TEST_RESULTS.json
RUN_STATUS = <final: COMPLETED after the final package pass + publication attempt — see HANDOFF.md>
HARD_STOP_REASON = correction package complete; all doc changes remain PROPOSALS
pending the next independent post-audit; no auto-continuation.
