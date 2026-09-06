# INTERNAL_QC_R1 — RUN D: PE_935_TEXANCHOR_CENSUS_R1_20260906_175500

- **QC context**: FRESH independent internal QC (pe-master-auditor, new session; the QC
  author did NOT execute the run). Assignment mode INTERNAL_QC, MATERIAL depth (targeted).
- **Scope discipline**: READ-ONLY over the whole tree except this one file
  (`00_CONTROL/INTERNAL_QC_R1.md`). No run outputs re-executed in place, no manifest
  amendment, no commit, NO_NESTED_TASKS. QC scripts were kept OUTSIDE the package in
  `C:\Users\User\AppData\Local\Temp\opencode\` (texanchor_qc_rederive.py,
  texanchor_qc_ci.py, texanchor_qc_blockcensus.py, texanchor_qc_claims.py,
  texanchor_qc_completeness.py).
- **Independent re-derivation basis** (no trust in the executor's aggregates): the pinned
  K1 CSV + Models.bnt bytes + the contract-pinned frozen R61 reader (10/10 SHA pins —
  the frozen method defines U_exposed as what that parser exposes), combined with MY OWN
  BNT2 index parser, MY OWN v10/v4 raw struct decoders, MY OWN bridge/mesh-part logic,
  MY OWN census/NC replay, and MY OWN definitional Clopper-Pearson CIs (brute-force
  binomial tail sums in log space + bisection — a different implementation family from
  the driver's incomplete-beta continued fraction).
- **Note**: this QC record postdates artifact_index.csv (manifest untouched by design;
  manifest amendment is PE-MASTER's decision).

---

## Q1. Contract + driver hashes — PASS

- `Get-FileHash 00_CONTROL/CONTRACT.md` →
  `4ba68d73fbc8551caad87b73d33a68ef156d54c259e2ffbb8ff482f58bcf215f` — equals the
  expected contract SHA in the QC assignment.
- `Get-FileHash 00_CONTROL/texanchor_census_r1.py` →
  `be22fae22383b66ee9dc3ffda33b0fadad1fc9dec42342663333eff191aa3f8c` — equals the
  expected driver SHA. `SHA256_DRIVER.txt` records the same value; PREREG_MARKER.txt
  records the same value; PIN_RESULTS.json records the executed driver hash (in-driver
  G-PINS check) — the audited bytes are the executed bytes.
- Driver read to EOF (1,459 lines) by the QC; no unexplained logic found.

## Q2. Freeze / G-METHOD — PASS

- FROZEN_METHOD.md present, `Get-FileHash` →
  `823bf9fd12367271a55a7c614681faf28b1b6eac9ed7ec6b77c967fe7a1347ff` — equals the hash
  recorded in PREREG_MARKER.txt (which also records the driver + contract hashes).
- Ordering (UTC mtimes): CONTRACT 17:53 → calibration probes 17:58–17:59 (declared
  pre-freeze in PREREG; not census results) → FROZEN_METHOD 18:02:13 → driver last edit
  18:04:21 → PREREG_MARKER 18:04:30 → PIN_RESULTS 18:04:34 → outputs 18:04:58+.
  The frozen method and marker precede all outputs; the driver was final before the
  marker was written.
- **Anchor predicate — code vs frozen text, EXACT match** (QC's own line-by-line read):
  M2 `name.rsplit("_", 1)` (else `("", no underscore)`) = driver `split_mesh_part`;
  M3 colon-bridge `last ":" → "_" iff tail is all digits` = driver `bridge` +
  `U_f = U_exposed | twins` (twins never replace exposed names); M4
  `own_file_resolution = mesh_part ∈ U_f(OWN file)` (= driver `universes[r['nif']]`),
  `slot_consistency = K1 slot column == extracted suffix` (= driver
  `r['slot'] == slot_suffix`), `anchored = own AND slot`, mode exact/bridge/none —
  all match the frozen text exactly.
- **NC procedure matches**: `random.Random(20260906)` single instance;
  `rng.sample(range(24508), 10000)` without replacement; per trial
  `rng.choice(sorted entry-bearing files EXCLUDING own file)` (uniform over 3,766
  alternatives); self-pairing excluded by construction + asserted per trial
  (counter `nc_self_pairing`, observed 0). Verified in code and by my own replay.

## Q3. Raw re-derivation — PASS

(a) **Row counts (my own count)**: ANCHOR_OUTCOMES.jsonl = **24,508**; NC_TRIALS.jsonl =
**10,000** (trial idx 0..9,999 unique); FILE_UNIVERSES.jsonl = **3,767**.

(b) **Re-derived from raw records (my own recount)**: anchored = **19,705**;
own_file_resolution = **19,705**; slot_consistency = **24,508/24,508**; resolution modes
exact **1,103** / bridge **18,602** / none **4,803** (1,103+18,602 = 19,705;
19,705+4,803 = 24,508). 0 duplicate entry keys; stored `anchored` equals recomputed
`own AND slot` on every record (0 mismatches).
Stronger: I re-derived the census itself from the pinned inputs (own code): all 24,508
stored outcomes match my recomputation row-for-row (outcome_mismatch = 0), and per-file
universes match my corpus-built universes exactly (0 mismatches over tri/mat/twins/sizes).

(c) **NC hits re-derived = 67** (my recount of NC_TRIALS anchored=true; other-file
resolution also 67; self-pairing 0; per-trial denominators correct on all 10,000:
10,000 / 24,508 / 3,767 / 3,766). My full replay of the frozen RNG procedure
(seed 20260906) reproduced every trial's entry, other_file, resolution, slot and
anchored value row-for-row (nc_mismatch = 0 over 10,000) — determinism and procedure
conformance confirmed by an independent implementation.

(d) **Exact binomial CI verified with MY OWN definitional implementation** (binomial
tail sums + bisection, no incomplete beta): anchored 19,705/24,508 →
CP95 = **[0.7989971, 0.8089770]** — matches the reported [79.8997%, 80.8977%].
Also independently confirmed: NC 67/10,000 → [0.0051961, 0.0085011] vs reported
[0.5196%, 0.8501%]; slot 24,508/24,508 → lower bound 0.9998495 = closed form
0.025^(1/24508) vs reported [99.9849%, 100%]; ENVIRONMENT 0/1,694 → upper 0.0021752 =
closed form 1 − 0.025^(1/1694).

(e) **Per-slot extremes verified from raw (my recount, all 40 slots)**: ENVIRONMENT
**0/1,694**; static families GLOW 1,330/1,524 = 0.872703 (87.27%), BASE 12,867/14,307,
GLOSS 2,571/2,791, DARK 1,750/1,816, DETAIL 192/199, BUMP 946/970, DECAL0 49/50 = 0.98
(98.00%) → static range **87.27%–98.00%** confirmed; every ANIM0–31 slot = 0 anchored
(ANIM total n = 1,157). All per-slot n/anchored equal the ANCHOR_RESULTS.json values.

## Q4. G-CENSUS reproduction — PASS (verified stronger than the 3-row spot check)

My own re-derivation (texanchor_qc_rederive.py): my BNT2 index parse (5,596 entries,
exact consumption), all 5,596 payloads parsed (5,596/5,596 PASS), every
NiArkTextureExtraData block decoded with MY OWN struct code (v10: 4,838 blocks;
v4: 758 blocks; 0 decode failures; exact cursor consumption), then compared field-for-field
against the pinned K1 CSV: **24,508/24,508 rows checked, 0 mismatches** on all 11 fields
(block_index, entry_idx, name, f1, f2, ref, anim_flag, frame_index, bnt2_id, version,
grammar); **per-file entry counts exact on 3,767/3,767** files; v10 19,637 / v4 4,871;
resolved split **24,474/34** untouched. CENSUS_REPRODUCTION.json is consistent with all
of this (rows_checked 24,508, mismatch_count 0, raw decode 4,838 + 758, 0 failures).
Population completeness additionally verified: total ark entries across ALL 5,596 files
= 24,508 (no entries exist outside the 3,767 table files); the one 4.0.0.2 file
(52555.nif) carries 0 entries — the report's version-census note is true.

## Q5. Fixtures / SELF_AUDIT — PASS

- NEGATIVE_FIXTURES_GEXEC.json: **8/8 fail-closed**, each with the expected explicit
  non-pass class (DEGENERATE_POPULATION, EMPTY_POPULATION, DUPLICATE_ENTRY_KEY,
  DENOMINATOR_MISMATCH, CORRUPTED_RECORD, NC_SELF_PAIRING_REJECTED,
  MALFORMED_MANIFEST_ROW, MISSING_INPUT_FILE).
- QC EXECUTED the gate validators itself (imported the pinned driver module WITHOUT
  running main; own synthetic inputs): every validator fails closed with the correct
  class; positive control (a fully valid manifest row) PASSES — the suite is not
  vacuously failing.
- MANIFEST_NEGATIVE_TESTS.json: **6/6** negatives fail-closed with the correct classes
  (also independently reproduced by my own validator executions).
- SELF_AUDIT zero size-derived claim: QC grep over the driver for
  `len(|getsize|.stat(` — 69 hits, **0 inside the eleven gate/validation functions**
  (hits are the BNT2 index parser's footer seek — extraction geometry, the raw decoders'
  cursor bounds, and record-COUNT assertions in main; no validation number anywhere
  derives from a file/payload size). AST scan scope is consistent with the frozen M9
  wording; the claim holds even beyond the scanned set.
- SELF_AUDIT CI validation (16 definitional pairs, worst delta 2.8e-14; closed forms)
  consistent with my own definitional CI implementation results.

## Q6. Manifest — PASS

- MANIFEST_SCHEMA_SPEC.md read; artifact_index.csv parsed with the standard csv parser
  by my own re-run: **27 ordinary rows** + "# external sources" + **14 external rows**.
  Assertions on EVERY ordinary row: exactly 3 fields; sha256 64-hex; relative
  forward-slash path; file exists in the package; physical hash equals the row;
  **no duplicates (27/27 unique)**; external rows: 5 fields, kind=external_source, era
  non-empty, physical path exists, hash matches. **Findings: 0.**
- Coverage cross-check: 29 files on disk = 27 covered + exactly the two DOCUMENTED
  circular self-exclusions (artifact_index.csv, 05_ANALYSIS/MANIFEST_VALIDATION.json);
  no manifest row points to a non-existent file. Writer (write_manifest_r1.py, read to
  EOF) uses a proper RFC-4180 csv writer and the spec's fail-closed gate;
  MANIFEST_VALIDATION.json (27/14 verified, 6/6 negatives, PASS) matches my re-run.

## Q7. Scope / originals untouched — PASS

- `Get-FileHash Models.bnt` → `c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0`
  (== pin); `Get-FileHash ARKTEXTURE_ID_TABLE.csv` →
  `34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9` (== pin);
  R61 source re-hashed by QC: **10/10** == SHA256_SOURCE.json.
- K1 table mtime 2026-09-06 10:15 UTC (predates this run, 17:53+); Models.bnt mtime
  2008-09-17 (original media). Content identity to the pins is hash-proven.
- eudoria-clean repo: `git status --porcelain` **clean**; HEAD `b7c85a5` == contract
  BASE_SHA `b7c85a5a1aad8b6c69a642c4f44e9b469a4f50da` (run executed, NOT committed —
  consistent; the run package lives outside that repo).
- Zero payloads: the 29 package files are .py/.json/.jsonl/.md/.csv/.txt only (largest
  are the JSONL evidence files). No file outside the run dir was modified by this run
  (hash pins + clean git + pre-run mtimes; the pre-existing `__pycache__` in R61
  01_source dates from 2026-08-25/29, not from this run — the driver sets
  `sys.dont_write_bytecode = True`).

## Q8. Report honesty (every number vs QC's own Q2–Q7 results) — PASS

- 06_REPORT/00_FINAL_REPORT.md read in full. Every numeric claim matched my
  independent results: 19,705/24,508 = 80.4023% [79.8997%, 80.8977%]; components
  1,103/18,602/4,803 (4.4998%/75.9025%/19.5977%); slot 24,508/24,508 [99.9849%,
  100%]; NC 67/10,000 = 0.6700% [0.5196%, 0.8501%]; ratio 120.0x; per-slot table
  (all rows); per-grammar v10 15,721/19,637, v4 3,984/4,871; per-class resolved
  19,690/24,474, dangling 15/34; miss decomposition 1,694 + 1,157 + 1,952 = 4,803 with
  per-slot misses BASE 1,440 / GLOSS 220 / GLOW 194 / DARK 66 / BUMP 24 / DETAIL 7 /
  DECAL0 1; f1 enum 24,336/24,508 with the 172 disagreements = f1=0 ×142 + f1=4 ×30
  (my recount); NiNode variant 21/24,508; colon-tail 20,833/21,914 and materials
  8,034/3,529 (my block-level census); version census 4,838/757/1 with 52555.nif the
  sole 4.0.0.2 file (0 entries).
- Miss-structure examples verified from raw: "Nameless0" ×583 and "Nameless12" ×224
  among ENVIRONMENT misses; "Geo_Flame_0_NONE" ×200 among ANIM misses; the
  **84-record space-variant residue** verified exactly: 84 unresolved "Editable_Mesh"
  entries across 72 files, and ALL 72 files' universes contain the space spelling
  "Editable Mesh" — documented, not bridged (NOT_CHECKED item 4), exactly as reported.
- OBSERVED labels present on every measured section; the standing sentence present at
  the top and bottom of the report, in HANDOFF, in STAGE_ACCEPTANCE_GATES.csv and in
  every JSON/JSONL artifact.
- Documented-not-done disclosures verified present: the 84-record space-variant
  residue (NOT bridged; report §6 + §9.4); the slot-column predicate choice (§4
  predicate) with the f1 census explicitly SUPPLEMENTARY_OBSERVED and NOT part of the
  frozen predicate (§7 + §9.3); the K1 resolution explicitly NOT re-tested and
  Textures.bnt not parsed (§9.2); no era-2003 leg; NC samples entries not files.
- No semantic claims found: runtime meaning is consistently gated (standing sentence;
  §8 closes with "what the anchor MEANS at runtime remains runtime-gated"); the
  NAMELESS_N / "_NONE" attributions are spelling observations citing R32-documented
  canon.
- STAGE_ACCEPTANCE_GATES.csv (proper RFC-4180 CSV) and HANDOFF.md numbers all match
  my results; the handoff follows the contract's final schema.

## Q9. K1-caveat paragraph — PASS

Report §8 states the association measurement with explicit denominators (24,508 census;
2,851 env+anim = 11.63%; 1,952 static-slot misses) and the **120x** separation vs the
0.67% cross-file chance rate — all verified above. The OBSERVED label is intact
("(OBSERVED, era PCG_9_3_5)"), the K1 99.8613% ID-membership figure is correctly
ATTRIBUTED to the K1 run (not re-tested here), there is no "the chain is proven"
wording anywhere (the paragraph claims coexistence of ID-membership with strong
per-file anchoring for static families and zero anchoring for env/anim — a measured
statement), and it closes runtime-gated. Meets the contract's one-paragraph refinement
requirement without overclaiming.

---

## DISCREPANCIES

**D1 (P2 — report prose count error; no number affected):** 00_FINAL_REPORT.md line 26
("the 8 static slot families anchor at 87.27–98.00%") and line 144 ("strong per-file
name anchoring for the eight static slot families"). Only **7** static slot families
(BASE, GLOSS, DARK, GLOW, BUMP, DETAIL, DECAL0) anchor in 87.27–98.00%; the 8th
non-ANIM family is ENVIRONMENT, which anchors at 0/1,694 and is explicitly contrasted
in the same sentences. All underlying per-slot numbers, rates and CIs are correct (QC
re-derived every one); the family COUNT in prose is off by one. Correction: "seven
static slot families". Revalidation: grep the corrected report for "eight static" →
0 hits. Does not affect gates, measurements, evidence or the K1-caveat content —
documentation-only, for PE-MASTER to route (existing completed files stay immutable;
amendment per project rules).

**D2 (P3 — denominator wording, value correct):** "20,833/21,914 non-empty NiTriShape
names end in ':<digits>'" (FROZEN_METHOD M3 calibration + report §4): the denominator is
BLOCK-level name occurrences (NiTriShape blocks carrying a non-empty name — QC's own
block census reproduces 21,914 / 20,833 / 1,081 exactly), not unique name strings
(unique: 20,911 names, 20,273 colon-tail, per QC's recount of FILE_UNIVERSES). The
number is correct on its actual basis and used consistently; wording "names" could
mislead a unique-name reading. No result affected.

**D3 (P3 — disclosure depth, not an error):** component (b) slot-consistency =
24,508/24,508 (100%) is an identity-by-construction (the K1 slot column was derived
under the same last-underscore convention as this run's M2 extraction). The caveat is
present in 05_ANALYSIS/ANCHOR_RESULTS.json ("K1's own derivation convention; the
expected identity is itself the reproduction evidence") and the report quotes the
predicate accurately (§4), but the report prose does not spell out the
by-construction nature of the 100%. Disclosure-depth note only.

Observations (not discrepancies): the K1 table's mtime (2026-09-06 10:15 UTC) precedes
this run and its hash matches every pin — its own package history is outside this run's
scope. DRIVER_LOG.txt is UTF-16 text (hash-pinned in the manifest; content consistent
with GATES_RESULTS/ANCHOR_RESULTS). The NC self-pairing "assertion" is a counter
(0 observed) — the frozen construction already excludes self-pairing, and QC's replay
confirms 0/10,000.

## FULL_READ_LOG (QC)

Contract.md (46); FROZEN_METHOD.md (159); PREREG_MARKER.txt (35); DRIVER_LOG.txt;
texanchor_census_r1.py (1,459, to EOF); write_manifest_r1.py (299, to EOF);
00_FINAL_REPORT.md (203); HANDOFF.md; STAGE_ACCEPTANCE_GATES.csv; PIN_RESULTS.json;
GATES_RESULTS.json; CENSUS_REPRODUCTION.json; SCOPE_CHECK.json; NEGATIVE_FIXTURES_GEXEC.json;
MANIFEST_NEGATIVE_TESTS.json; SELF_AUDIT.json (293); MANIFEST_VALIDATION.json;
ANCHOR_RESULTS.json (1,211); MANIFEST_SCHEMA_SPEC.md (22); K1 CSV (24,508 rows parsed);
ANCHOR_OUTCOMES.jsonl / NC_TRIALS.jsonl / FILE_UNIVERSES.jsonl (programmatically
full-parsed, every record); artifact_index.csv (all 41 data rows). Hash computations
and corpus parses per the commands quoted in Q1–Q7 above.

## NOT_CHECKED (explicit)

- CALIBRATION_PROBE{,2,3} scripts/JSONs: role/pins/manifest coverage verified, declared
  pre-freeze and NOT census results; their two load-bearing calibration figures
  (20,833/21,914 colon-tail; 1,103 exact-only resolution) were independently re-derived
  from the corpus by this QC. Full-text logic read not required by any checklist item.
- R61 parser internals: treated as the contract-pinned frozen tool (10/10 SHA pins
  re-verified by QC); its behavior was exercised over all 5,596 payloads and its
  outputs cross-checked against MY independent raw-byte decoders (0 disagreements).
- Textures.bnt / K1 bnt2_id resolution: out of scope by contract (the K1 resolution
  stands; explicitly not re-tested — report §9.2).
- No runtime/D3D8 evidence: out of scope by design (OBSERVED-level structural
  measurement; runtime meaning gated).

No unchecked LOAD-BEARING component remains.

---

**Per-item verdicts: Q1 PASS · Q2 PASS · Q3 PASS · Q4 PASS · Q5 PASS · Q6 PASS ·
Q7 PASS · Q8 PASS (D1/D2/D3 recorded) · Q9 PASS.**

QC_VERDICT = QC_PASS
