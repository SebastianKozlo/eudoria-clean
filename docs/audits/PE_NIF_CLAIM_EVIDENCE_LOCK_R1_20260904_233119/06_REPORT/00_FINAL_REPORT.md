# PE-NIF-CLAIM-EVIDENCE-LOCK-R1 — FINAL REPORT (CLAIM–EVIDENCE SCOPE LOCK)

RUN_ID = PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119
AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\06_REPORT\00_FINAL_REPORT.md
EXECUTED BY = pe-reconstruction (method per pe-re-analyst; single bounded round; no nested agents)
DATE = 2026-09-05 (run dir timestamped 20260904_233119 per prompt)

## 0. P0 = CLAIM–EVIDENCE SCOPE LOCK — achieved

This round reconciled the NIF ITER-29–40 claims with their actual test scope.
Every auditor allegation (F1–F6 + context) was re-verified FROM RAW EVIDENCE
(never copied from the auditor's probe.json), each receiving
ACCEPTED / REFUTED / UNRESOLVED; every atomic claim received exactly ONE
knowledge status from {CONFIRMED, STRONGLY_SUPPORTED, PLAUSIBLE, UNVERIFIED,
REJECTED}. No historical run, wiki file, PE_AUTO_LOOP.json, frozen parser or
original game file was modified. All doc changes are PROPOSALS
(06_REPORT/PROPOSED_DOC_CORRECTIONS.md). No new discoveries were made and no
new semantics work was started.

## 1. Inputs and integrity chain

- Prompt SHA256 verified before execution:
  BFDB1D23E42904FB29CBDB5995D072B8C793AB5D4E241E28BF7F3EFA8EEBA562 (match).
- Mandatory reading completed: AGENTS.md + the six 00_PROJECT_CONTEXT files;
  the external audit 06_REPORT/00_FINAL_REPORT.md; 01_RAW/probe.json;
  00_CONTROL/probe.cjs; all 12 referenced run dirs (REPORT + gates +
  artifact_index + the raw result JSONs cited by F1–F6).
- docs/nif reference state: commit 077b8a4; local HEAD 8cd0bc3 with
  `git diff 077b8a4..HEAD -- docs/nif` EMPTY and the working tree clean —
  reference snapshot == current state; current file SHA256s equal the
  auditor's post-apply SHAs (README 4f976581..., 09-semantics bb22d518...).
- ACTIVE_WRITER.lock v2 (heartbeat 2026-09-04T10:25:00) scopes the writer to
  PE_AUTO_LOOP.json / PE_MILESTONE_1_WORLD_SURFACE_R1 / eudoria-web / canon.
  This round writes ONLY to its own new run dir and reads every writer-scope
  path read-only → NO writer conflict; no dependent work stopped; the lock
  was NOT taken over (stale heartbeat irrelevant — no writer-scope write).
- Control instrumentation: 00_CONTROL/control_r1.cjs (one-time; read-only on
  sources; executed twice — exec-1 counted a trailing blank line as a 12th
  CSV error, fixed to the probe.cjs .trim() standard and re-executed; both
  hashes recorded in 00_CONTROL/SHA256_CONTROL.txt BEFORE each execution;
  all other results identical between executions). Generator:
  00_CONTROL/generate_claim_matrix.cjs (CLAIM_MATRIX emitter, iterated for
  column/status hygiene — final output validated 43 rows / 0 bad).

## 2. The six controls — verdicts

### CONTROL 1 — R32 (f1 recount; allegations F1)
INDEPENDENT RECOUNT from R32's own ANIM_FRAME_CHECK.json (raw artifact, not
probe.json): total 1,157; f1 = {11: 985, 0: 142, 4: 30}; sum 1,157 ✓;
frame-index == slot-number 1,157/1,157, mismatches [], regular prefixes 0 ✓.
- Auditor's "985/142/30, hence 172 without f1=11" → ACCEPTED (exact).
- Separation performed: vocabulary size (40 slots) ≠ distinct f1 values
  (9 type-codes; ANIM0–31 share 11); frame/slot equality (CONFIRMED) is a
  different invariant from f1==11 (REJECTED as unqualified; CONFIRMED only
  for the 8 named slots + 985/1,157 ANIM); "f1 IS the slot-type code"
  semantics stays STRONGLY_SUPPORTED (R32's own S7), engine meaning open.
- Exception-omission sites found (all in-scope of F1): R32 REPORT.md S1
  ("perfect f1↔slot enum mapping" while S4.3 carries the exceptions);
  README.md L82 ("f1 = slot enum", no exception); 09-semantics.md L55
  ("perfect f1 enum"), L70-73 ("a perfect 1:1 enum ... ANIM=11"), L84-86
  (ANIM bullet without the 172). The omitting wording ORIGINATES in the
  worker's own R40-SP2 proposal text (S18).
- NEW FINDING (beyond the auditor): R32 REPORT S4.3 says "10 of 45" late
  ANIM16–31 entries carry f1=11 — the raw says **9 of 45** (3+3+1+1+1; f1=0
  x22, f1=4 x14). Report arithmetic slip; proposal P5-1.

### CONTROL 2 — R33/R34 (morph denominators, k=1 counterexamples; allegation F2)
Reconstructed from REAL_SPARSE_GRAMMAR.json (raw):
- 6,167 fit spans; 2,427 "real-record" spans (definition read VERBATIM:
  "has_real(>=1 REAL entry) AND n_wp_inrange>0" — REAL = id!=0 & id<N & clean
  floats & 4-aligned, i.e. R33-hypothesis criteria; the weight-pair condition
  is ITER-4-hypothesis-aligned → the classifier IS model-dependent) →
  auditor's selection-dependence allegation ACCEPTED.
- variable-k exact: 3,186/6,167 (51.66%) and 2,093/2,427 (86.24%) — the
  auditor's "86.2%, nie 100%, and do not mix with 3,186 or R21 denominators"
  ACCEPTED (all four now carried together with definitions; 334 real-record
  spans fit no tested grammar).
- k=1 counterexample VERIFIED from raw exact_examples_cap50:
  574845.nif bi=69 si=14 → 14 records ALL k=1; si=27 → 5 records all k=1
  (27 of the 50 example spans are 574845.nif bi=69, predominantly k=1);
  R35's 2003 k-histogram = {1:1884, 2:3135, 3:829, 4:215, 5:108}; driver
  VAR_MAX_K=8. → "k per-record in {2,3,4}" (R34 verdict + wiki ch09 L191)
  REJECTED; scope correction proposed.
- Model selection vs validation: parse_variable (morph_quant_r34.py
  L809-841) takes the SMALLEST k whose prefix sums ≈1.0 (tol 1e-4) and
  breaks on first match — segmentation uniqueness is NOT proven anywhere
  in R34 (caveat 2 admits the k=1/k=2 ambiguity) → ACCEPTED. The nine-float
  "3 delta triples" meaning (3 states × XYZ?) remains UNVERIFIED; the wiki's
  "position deltas" wording is an unproven interpretation → proposal P1-5.
- "Morph payload SOLVED" (global): REJECTED; the scoped byte-fit claim is
  CONFIRMED with its denominators. No new grammar was built this round
  (explicitly out of scope).

### CONTROL 3 — R35 (era separation, witnesses; allegation F3)
Direct BNT2 re-read of BOTH original containers (independent of probe.json):
- 5,422 shared names = 5,208 byte-identical (96.05%) + 214 changed (211
  same-version + 3 flips per R36) + 4 old-only-2003 + 174 new-only-953 →
  auditor's "5208/5422 identical → conformance test, weaker era-generalization
  test" ACCEPTED; identical/changed/unique now reported separately.
- Witness question ANSWERED with new evidence (control_r1.cjs scan):
  FILE-LEVEL witnesses on genuinely changed payloads EXIST for all five
  families — all 214 changed + 4 old-only 2003 files were parsed by the R35
  validators; family blocks present in changed files: animation/texture/
  importer 214/214, shader 9, morph 29; all 4 old-only files contain
  animation/texture/importer blocks (0 shader/morph). INTRA-BLOCK
  byte-level witnesses were NOT established (coarse name-to-next-ark-name
  span heuristic; the span includes intervening standard blocks) — an honest
  evidence-scope limit, NOT a falsification; block-by-block diff listed as
  missing-for-stronger.
- 21 claims → 19 ERA-STABLE / 2 EVOLVED / 0 ABSENT / 0 falsifications
  re-derived from FORMAT_EVOLUTION.json → the count is real but covers the
  TESTED claims only → "never GRAMMAR" (ch10 L121-125) REJECTED as a
  universal; scoped replacement proposed (P2-2). "Lack of witness does not
  falsify; it limits evidence scope" — applied exactly as instructed.

### CONTROL 4 — R36 (c vs d, iff; allegation F4)
- c == CRC32(payload): RE-DERIVED over both containers — 11,022/11,022,
  0 mismatches → CONFIRMED (auditor's independent confirmation reproduced).
- d stable 5,205/5,208 identical; the three same-payload-different-d files
  re-derived by name: exactly 524071.nif, 524077.nif, 524083.nif →
  ACCEPTED. d==c 3,435/5,596 (61.42%) and 3,299/5,426 (60.80%) re-derived.
- Tested-formula range read from FIELD_D_TESTS.json T4: 10 candidate
  families per era (adler32(payload), CRC32(name), CRC32(name+0x0A),
  adler32(name), CRC32(name+size), CRC32(size+name), fnv1a(name), size,
  offset — all exact-0; crc32(payload) only at the d==c subsets) → exclusion
  of the TESTED list ≠ exclusion of all deterministic functions → ACCEPTED.
- Writer/registration evidence searched in the EXISTING evidence: ABSENT —
  all 12 REPORTs state value-pattern inference; R36 itself: "packer
  write-path semantics inferred from value patterns, not from packer code".
  → mechanism hypothesis stays STRONGLY_SUPPORTED; the "registration CRC"
  origin story is NOT converted into established history.
- The iff (ch09 L208, ch10 L23, ch11 L24): REJECTED — CRC collisions,
  return-to-old-bytes, the 3 T1 exceptions (d-rewrites on unchanged payloads)
  explainable only by an unobserved "registering event" (unfalsifiability
  risk), and no demonstrated registration history. Correlation wording
  proposed instead (P1-6/P2-1/P3-1).

### CONTROL 5 — R29/R37/R38 (metadata vs era; invariant vs role; label vs behavior; allegation F5)
- R29: 14 exact / 10 masked patterns re-derived; 834 = 507+212+115 re-summed;
  exporter-string census CONFIRMED, "original toolchain version / survives
  up-conversion" is R29's own STRONGLY_SUPPORTED (no re-export event ever
  observed) → ACCEPTED: it is a metadata/provenance HINT; wiki presents it
  ungraded (ch09 L219-228) → grading proposal P1-7.
- R37: Scene-Root-last re-derived 348/348 (347 TAIL + 1 single-record file,
  relpos min=max=1.0) — a CONFIRMED corpus label/order invariant; the engine
  class-role stays UNVERIFIED (R37's own verdict) and the wiki ALREADY
  preserves that caution (README L94-97, ch09 L162-169) → ACCEPTED with
  "no wiki correction needed on this point".
- R38: mode census {996/253/20/4/1} re-derived; 41076.nif twin pair re-read
  (identical non-mode fields) — a CONFIRMED corpus fact proving
  params-do-not-determine-mode; state-binding STRONGLY_SUPPORTED; one-shot
  PLAUSIBLE; activation-time/persistence/one-shot runtime NOT proven →
  ACCEPTED. Wiki flattening found (README L80 "SEMANTICS decoded", ch09
  L146-155 ungraded "Readings") → grading proposals P4-2/P1-4.
  G3C_BOUNDARY = parser route (CONFIRMED, already correctly scoped in wiki
  ch08); it does not close the contaminated-records' format semantics
  (residual noted).
- One evidential status per atomic claim enforced (the R34-style mixed
  "CONFIRMED (STRONGLY_SUPPORTED)" pattern was replaced by split rows).

### CONTROL 6 — R39/R40 + manifests (allegation F6)
- R39: 45 proposals re-counted (EDIT_PROPOSALS.json); apply state confirmed
  via git (077b8a4^ = post-R39 pre-R40; commit 3e383ce per README L64).
  "Execution of the update ≠ independent validation of 45 claims" →
  ACCEPTED (claims keep their run-derived statuses).
- R40: NEW EVIDENCE — exact re-application of the 9 proposals onto git
  077b8a4^ reproduces the applied files BYTE-EXACT (README sha 4f976581...,
  09-semantics sha bb22d518...) → the master's apply is CONFIRMED
  byte-exact. NEW FINDING: R40 report's size figures are unit-mixed
  ("4,573→9,182 bytes" / "3,705→13,214 bytes" = pre BYTES + CHAR delta;
  true byte sizes 9,213 / 13,326) → proposal P5-2.
- "+236 lines" (PE_AUTO_LOOP.json L298) re-derived via git numstat: README
  +70/-9, 09-semantics +166/-2 → 236 = COMBINED added lines (net +225) →
  ACCEPTED (proposal P5-3; the loop file is WRITER-scope — NOT written).
- Manifests: 11 strict CSV errors re-derived in exactly the 8 manifests the
  auditor named (R30/R31/R32/R33/R35/R36/R38/R39). 12 normalized sidecars
  created (05_ANALYSIS/NORMALIZED_MANIFESTS/), each strict-CSV-valid, with
  original manifest path + original SHA256 + per-row hash re-verification +
  resolved full path + explicit scope classes (PRE_EDIT_INPUT for the wiki
  pre-apply rows, POST_EDIT_OUTPUT for package files, IMMUTABLE_SNAPSHOT for
  in-run artifacts/evidence pointers, MUTABLE_POINTER for PE_AUTO_LOOP.json,
  UNRESOLVED_ALIAS explicitly marked — no invented paths or hashes; the R40
  manifest's 3 expected-vs-current hash differences are classified as
  provenance-state differences: pre-apply snapshot vs post-apply state vs
  mutable live file, NOT tampering).
- README "complete" (L3-5) + ch11 "nothing outside that list is open"
  (L80-81): unbounded → REJECTED as wording; scoped replacements proposed
  (P4-3/P3-2). Coverage / raw-byte behavior / parser support / engine
  semantics separation: already largely present (README state table +
  ch11 honest-100% section) and refined by the proposals.

## 3. Results summary

- CLAIM_MATRIX.csv: 43 atomic claims; statuses: CONFIRMED 24, REJECTED 9,
  STRONGLY_SUPPORTED 7, UNVERIFIED 2, PLAUSIBLE 1 (single status per row).
- ALLEGATION_DISPOSITIONS.csv: 23 rows; every auditor allegation
  ACCEPTED with concrete re-derived evidence; 0 REFUTED, 0 UNRESOLVED
  (the auditor's allegations survived verification; two NEW findings were
  added beyond them: R32 "10 of 45"→9, R40 unit-mixed sizes).
- DENOMINATORS.json: 21 explicit denominators with definitions and
  non-interchangeability warnings.
- COUNTEREXAMPLES.json: 12 bounding counterexamples (CE-1..CE-12).
- 12 normalized manifest sidecars; CONTROL_R1_RESULTS.json (raw control
  output); SOURCE_QUOTES.md (19 quote blocks, all with file+lines+SHA).
- Runtime: NOT RUN (out of scope) — runtime-gated claims stay at their
  non-CONFIRMED levels BY DESIGN; executing a test is not conflated with
  proving a hypothesis anywhere in this report.

## 4. What this round deliberately did NOT do

- No wiki/canon/Obsidian edit; no commit/push; no PE_AUTO_LOOP.json write;
  no old driver re-run; no new flags/morph/TEXT semantics work; no WORLD XYZ;
  no milestone promotion; no MAPRE change; no game execution. The corrected
  wordings live ONLY as proposals in 06_REPORT/PROPOSED_DOC_CORRECTIONS.md.

## 5. Acceptance-gates self-check

| Gate | Result |
|---|---|
| Every auditor allegation has ACCEPTED/REFUTED/UNRESOLVED with evidence | PASS (23/23 in ALLEGATION_DISPOSITIONS.csv; all ACCEPTED, evidence re-derived) |
| CLAIM_MATRIX columns complete (claim/source+line+SHA/corpus/denominator/method/independence/counterexample/status/wording/missing) | PASS (43 rows, 14 columns) |
| Knowledge statuses exclusively from the 5-value taxonomy, one per atomic claim | PASS ({CONFIRMED 24, REJECTED 9, STRONGLY_SUPPORTED 7, UNVERIFIED 2, PLAUSIBLE 1}) |
| No unbounded 100%/fully decoded/never/iff without exact scope | PASS (all such instances located, marked REJECTED with scoped replacements) |
| Raw bytes/correlations do not lose validity from open semantics | PASS (correlation claims kept CONFIRMED; semantics separated) |
| All new JSON/CSV syntax+column validated; hashes recomputed; no placeholders | PASS (validated: CLAIM_MATRIX, ALLEGATION_DISPOSITIONS, 12 sidecars, DENOMINATORS, COUNTEREXAMPLES, CONTROL_R1_RESULTS; manifest excludes itself from its own hash list — documented) |
| Docs-to-change are proposals only in 06_REPORT; repo/runs unchanged | PASS (PROPOSED_DOC_CORRECTIONS.md; git tree clean vs HEAD; no historical write) |

RUN_STATUS = COMPLETED (all six controls executed; PASS = correct
reconciliation and explicit claim limiting, NOT full NIF solution)

HARD_STOP_REASON = stage complete; corrections are PROPOSALS pending
independent post-audit; no next stage auto-continuation.

## FINAL HANDOFF BLOCK

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\01_RAW\CONTROL_R1_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\05_ANALYSIS\CLAIM_MATRIX.csv; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\05_ANALYSIS\ALLEGATION_DISPOSITIONS.csv; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\05_ANALYSIS\DENOMINATORS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\05_ANALYSIS\COUNTEREXAMPLES.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\05_ANALYSIS\NORMALIZED_MANIFESTS; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\03_STATIC\SOURCE_QUOTES.md; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119\02_LOGS\LOGS.md
RUN_STATUS = COMPLETED
HARD_STOP_REASON = etap zakończony, oczekuje niezależnego post-audytu (stage complete; doc corrections are proposals pending independent post-audit; no auto-continuation)
