# PLAN — PE-NIF-CLAIM-EVIDENCE-LOCK-R2 (correction package only)

RUN_ID = PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054
P0 = CORRECTION_PACKAGE_EVIDENCE_SELF_CONSISTENCY
EXECUTED BY = pe-reconstruction (bounded correction run per the independent post-audit
prompt OPENCODE_R2_PROMPT.md, SHA256 46A2A99A9F1D03B4FE33F2FBFCA89D2440FD702188A3D020E9BF29A7A370E5ED,
verified before execution).
MILESTONE MAPPING = EU935-M2 contribution only; no milestone advancement.

## Mandate

Repair the R1 correction package's own evidence defects in a NEW immutable run, then
publish the bounded R2 package to SebastianKozlo/eudoria-clean docs/audits/. This run
does NOT apply wiki corrections, does NOT resume morph research, does NOT promote any
milestone. The external auditor's findings are re-verified from raw evidence — the
auditor is not itself a source of truth.

## Areas (from the prompt, binding)

- A. Reproduce + fix the population mismatch: independent reclassification of both
  BNT corpora (shared-identical / changed / old-only / new-only by exact bytes);
  separate ASCII occurrence count / distinct filename count / parsed block count /
  successful family-validator count; test the auditor counterexamples (old-only
  double-increment; NiVertexMorphExtraData 29 occurrences in 3 changed files) by
  independent reproduction, not assumption; synthetic counter tests (duplicate family
  in one file = one file; absent family = 0; old-only increments once); correct
  C-R35-04, gate G7, R1 final report Control 3, P2-2 NOTE, denominator inventory;
  ASCII-name presence only where no successful-validator join exists.
- B. Repair candidate-formula wording: recount the TEN named candidates with explicit
  denominators; NINE exact-zero; crc32(payload) = 3435/5596 and 3299/5426 (not
  universal, NOT exact-zero); supersede C-R36-05 + G8; keep the iff rejection and the
  "all deterministic functions excluded" rejection; recalculate the claim-status tally.
- C. Genuinely lossless sidecars: originals immutable; exact raw row bytes via base64 +
  row SHA256; original path/SHA, row position, recoverable fields, normalization rule,
  uncertainty; R39 GAP_ANALYSIS role text round-trip equality (no silent truncation);
  malformed-row semantics withheld as UNRESOLVED with bytes retained; independent CSV
  checker; PE_AUTO_LOOP hash = mutable pointer, untouched.
- D. Repair proposals WITHOUT applying: P1-5 wording; P4-3/C-DOC-01 evidence-graded
  wording; P1-6/P2-1/P3-1 measured-first; restrict every/all/100% to measured
  populations; resolve the chat "3-execution history" against the two recorded control
  hashes honestly; distinguish 45 R39 proposals COUNTED/READ vs 9 R40 edits REPLAYED;
  finding disposition matrix (ACCEPTED/REFUTED/UNRESOLVED with evidence); R1->R2
  supersession map.
- E. Gates that DETECT failures: computed from fresh results; fail on violated
  invariants; exit nonzero; human-reviewed wording gates separated from executable
  tests; OLD erroneous counter/normalization/wording fixtures FAIL and corrected
  outputs PASS; fixtures stored locally under this run; every important PASS records
  MEASURED_QUANTITY / DENOMINATOR / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR /
  FAILURE_CASE_DETECTED.

## Implementation (stage-local, read-only on all sources)

1. 00_CONTROL/control_r2.cjs (Node; hash recorded in SHA256_CONTROL.txt BEFORE
   execution): physical source lock (both Models.bnt SHA256); direct BNT2 index parse
   with bounds checks; era join by exact payload bytes; corrected family scan
   (occurrence + unique-file counters, per-file metadata, no payloads published);
   R1-bug fixture (faithful reimplementation of control_r1.cjs L163-179 counting —
   the historical script itself is NOT executed or edited); synthetic counter tests;
   c==CRC32(payload) verification; d==c recount; d-stability + 3 exceptions; the ten
   candidate formulas PHYSICALLY recomputed per era and compared with the R36
   historical T4 counts; lossless sidecar builder for the 12 manifests (base64 + row
   SHA256 + terminators + cells JSON + strict-only header mapping) with full-file
   byte reconstruction self-test; R39 GAP_ANALYSIS row round-trip test vs the R1
   sidecar. Output: 01_RAW/RECOUNTS.json + 05_ANALYSIS/NORMALIZED_MANIFESTS/*.csv.
2. 00_CONTROL/run_gates.py (Python; independent implementation): re-derives the core
   physical quantities from the two containers with Python (independent of the Node
   results), validates all 12 sidecars with the Python csv module (strict), re-runs
   the full-file reconstruction test independently, checks source identity/coverage/
   quoting/escaping, evaluates the executable gates (including old-fixture FAIL
   demonstrations read from R1's immutable artifacts), validates the R2 CSV/JSON
   outputs, writes 02_LOGS/TEST_RESULTS.json and EXITS NONZERO on any failure.
3. Table emitters (00_CONTROL/emit_r2_csvs.cjs + 00_CONTROL/r2_tables.json): emit
   CLAIM_MATRIX.csv, FINDING_DISPOSITIONS.csv, SUPERSESSION_MAP.csv and
   STAGE_ACCEPTANCE_GATES.csv with strict RFC4180 quoting (hand-written CSV is not
   trusted — R1 lesson).
4. Reports: 06_REPORT/00_FINAL_REPORT.md (authoritative),
   06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md (PROPOSALS ONLY), 03_STATIC/SOURCE_QUOTES.md,
   02_LOGS/LOGS.md, 04_RUNTIME/NOT_RUN.md, REPORT.md, HANDOFF.md, artifact_index.csv
   (real SHA256; self-exclusion documented; claim-aware claims_supported column).

## Publication (the ONLY authorized repo write)

- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (SebastianKozlo/eudoria-clean,
  branch master). BASE_SHA = c0c2f2fca328366364928aeee3c6249c24025446 (captured, never
  reset). Copy the complete R2 package byte-identically to
  docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/, verify per-file SHA256
  parity, stage ONLY that path (never git add -A), commit with RUN+subsystem+result,
  push origin master WITHOUT force using per-command -c http.sslBackend=openssl (no
  global config change, TLS verification never disabled), verify remote SHA.
- EXCLUDED: untracked docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ (another
  writer's — untouched); docs/nif, historical audit packages, canonical state, runtime
  code (READ-ONLY).
- Never push original BNT/NIF/TGA/executable/installer payloads or complete dumps.
  Sources not publishable are recorded by era/build, local path, size, SHA256 and
  reproduction method.

## Hard stops (binding)

No wiki application; no canonical/vault/index update; no PE_AUTO_LOOP modification or
relaunch; no shared-tool edit (tools/, scripts/ untouched); no historical evidence edit
(R1 run dir, R29–R40 runs, manifests read-only); no runtime/game/Ghidra execution; no
new morph semantics, world placement, XYZ, MAPRE or milestone promotion. Stop after
the corrected package, internal regression, safe publication attempt and handoff.
