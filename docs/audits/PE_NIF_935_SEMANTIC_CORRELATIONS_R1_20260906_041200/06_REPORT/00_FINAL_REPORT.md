# PE_NIF_935_SEMANTIC_CORRELATIONS_R1 — FINAL REPORT (EU935-M1, RUN_CLASS MATERIAL)

**Run**: PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200
**Date**: 2026-09-04..06 era-window, executed 2026-09-06 04:12-04:40. **Agent**: pe-reconstruction.
**Parent**: PE-MASTER loop 0132d23c-2f0f-42f2-bb07-fb74f637488b (KROK 3 of 3). **Era**: PCG 9.3.5 (era-primary). **Milestone**: EU935-M1 bounded contribution, NO milestone crossing.

**ONE_PRIMARY_QUESTION**: What do four pre-registered offline statistical probes OBSERVE about the four open NiArk/semantic fields (the importer 3-byte flags; the ArkTexture field1/field2-low8 two-class joint; the event-registry u32 values; the viewport float families) — with every result labeled OBSERVED and any correlation tested against a permuted/base-rate control so nothing masquerades as semantic proof?

**STANDING SENTENCE: correlation outputs are OBSERVED-level evidence; semantic roles remain runtime-gated (KROK 4 class).**

No "means"/"proves"/"the semantic role is" appears in any verdict. Every correlation claim below carries its permutation-control numbers.

---

## 1. Inputs, pins, integrity (G1)

| Item | Value |
|---|---|
| Corpus | `pcg_install\Data\Models\Models.bnt`, SHA256 `c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0` (pin MATCH, re-hashed in-driver before any parse) |
| BNT2 index | 5,596 entries (footer-index pattern, R10/R28/R29-established) |
| Frozen parser | R61 `PE_R61_FROZEN_BASELINE_20260828\01_source` — **10/10 SHA256 verified in-driver BEFORE any parse, READ-ONLY, never modified** |
| Era-mirror manifest | `FULL_5426_RESULTS_R61.csv` (5,426 filenames, READ-ONLY) |
| Prior census artifacts | R29/R32/R30/R8/R28 read as RECONCILIATION TARGETS ONLY (read-only); all numbers below re-derived fresh from the pinned bytes |
| Driver | `00_Control\semantic_correlations_r1.py`, SHA256 `927b256679e28dfc1e1e2284ceebd680d9ee52f1b5b8e53f3ed48b3397d1f4a7` == SHA256_DRIVER.txt (hash-after-last-edit provenance verified at every phase start) |
| Parse closure | **5,596/5,596 PASS** (HARD STOP not triggered) |
| Payload writes | ZERO (only census rows / hex / floats into JSON/CSV) |

## 2. G2 — canon reconciliation (all contract numbers EXACT; zero drift)

| Canon (contract) | This run (fresh re-derivation) | Verdict |
|---|---|---|
| Importer v4 flag states 558/128/72 (000000/0000ff/00ffff) | 558/128/72 | MATCH |
| ArkTexture field1 classes 3,042/1,796 | (field1=1, low8=0)=3,042; (field1=-256, low8=255)=1,796; no other combination | MATCH |
| Event registry 263 strings / 136 string-bearing records / 113 zeros | 263 / 136 / 113 | MATCH |
| Viewport classes 2,304/752/592/79/11 (13B/21B/85B/121B/43B) | 2,304/752/592/79/11 | MATCH |
| Importer block split 4,838 v10 / 758 v4 (secondary) | 4,838 / 758 | MATCH |
| R29 exporter×version matrix 8 cells (secondary) | all 8 cells exact (4004/606/507/212/139/115/12/1) | MATCH |
| Viewport block total 4,095 (registry) with 1 block/file | 4,095 blocks, per-file histogram {1: 4,095} | MATCH |

Reconciliation notes (era-labeled, nothing silently superseded):
- **Viewport length classes 39→18 and 47→4** in this run's R28-consistent slicing (`ext = raw[4+nl:]`, R61-derived) correspond to the R8-era inline census rows 35→18 / 43→4; the contract's 43B×11 is the R28 number and matches exactly here. The five contract classes reconcile exactly; the extra classes (35/39/45/47/49) are documented in RECONCILIATION.json (`viewport_extra`).
- The 3 walk-anomalies are the R30-documented text-degenerate 7 B blocks (424512/424791/424793.nif, u4=0x00030100, no strings) — expected, out of binary-grammar scope.
- 43B subclass census 3 all-zero-default / 8 parametric reproduces R28's own data exactly under the pre-registered |f|>1e-6 rule (verified independently against `VIEWPORT_43B.json`).

## 3. Method (pre-registered in the driver docstring before the final run)

For every A×B pair: Pearson chi-square on the observed contingency table (zero-marginal rows/columns dropped, documented), null distribution = **10,000 uniform label permutations** of A across the fixed B partition (items pre-grouped by B, per-replicate C-level slice recount; `random.Random(20260906)` with independent seed offsets per test). Verdict: **"OBSERVED correlation" iff observed chi² > 95th percentile of the permutation distribution**, else "NO OBSERVED correlation". p_perm = (1+#{perm≥obs})/(N+1). Constant variables (no variance) are documented **"NO TEST (constant)"** without a permutation run. 42 test rows total: **33 executed with permutation controls; 9 constants documented**. Raw machine-readable data: `01_RAW/PROBE{1-4}_RAW.csv` + `EXTRACTION.json`; analysis: `05_ANALYSIS/*.json` (G5).

## 4. PROBE-1 — importer v4 3-byte flags (758 v4 files; A = flag state 000000/0000ff/00ffff)

| B variable | Verdict | obs chi² | perm p95 | p_perm |
|---|---|---|---|---|
| B1 nif version (4.0.0.0/4.0.0.2/4.1.0.12) | **NO OBSERVED correlation** | 0.359 | 9.540 | 1.0000 |
| B2 exporter string class | **OBSERVED correlation** | 61.605 | 9.535 | 0.0001 |
| B3 mesh-bearing | NO TEST (constant: yes in all 758) | - | - | - |
| B4 morph-bearing | NO TEST (constant: no in all 758; R29-consistent) | - | - | - |
| B5 block count class | **OBSERVED correlation** | 21.102 | 12.541 | 0.0022 |
| B6 geometry size (total triangles) | **OBSERVED correlation** | 55.539 | 12.970 | 0.0001 |
| B7 texture entry count | **OBSERVED correlation** | 19.686 | 12.901 | 0.0057 |
| B8 era-mirror | NO TEST (constant: yes in all 758) | - | - | - |

OBSERVED-level reading (no semantics claimed): 00ffff occurs only in 4.1.0.12-exporter files (72/72); 0000ff is 126/128 4.1.0.12-exporter; 000000 spreads over all exporter classes (408/138/12). The flag state tracks the **exporter string**, not the file version (B2 OBSERVED while B1 is not — 139 v4 files carry exporter strings older than their own version, R29 F4-consistent). Descriptives (OBSERVED): block-count medians 19/27/21; triangle medians 208/650/134; entry medians 3/4/2 for 000000/0000ff/00ffff; 00ffff files are the smallest (tri median 134) and 0000ff the largest (650).

## 5. PROBE-2 — ArkTexture field1/field2-low8 two-class joint (4,838 v10 files)

| B variable | Verdict | obs chi² | perm p95 | p_perm |
|---|---|---|---|---|
| B1 entry count class | **OBSERVED correlation** | 4,728.2 | 9.383 | 0.0001 |
| has BASE / GLOSS / DARK / DETAIL / GLOW / BUMP / DECAL0 / ENVIRONMENT | **OBSERVED** each | 4,703.3 / 313.2 / 149.1 / 40.7 / 240.7 / 283.6 / 27.4 / 316.8 | 3.71 / 3.80 / 3.73 / 3.84 / 4.19 / 3.80 / 3.47 / 3.82 | 0.0001 each |
| has ANIM slot | **OBSERVED** | 38.292 | 4.084 | 0.0001 |
| NiTextureEffect present | **OBSERVED** | 316.790 | 3.823 | 0.0001 |
| mesh-bearing | **OBSERVED** | 4,736.4 | 3.892 | 0.0001 |
| era-mirror | **OBSERVED** | 25.493 | 3.931 | 0.0001 |
| num_tex | NO TEST (constant: 3 in 4,838/4,838) | - | - | - |
| field2 raw packing | documented: deterministic function of B1×A (tested via B1, not separately) | - | - | - |

**Structural fact behind the associations (OBSERVED)**: the field1=-256/low8=255 class (1,796 files) has **entry_count = 0 in 1,796/1,796 files and carries no slot entries of any kind** (mean slot counts all 0); the field1=1/low8=0 class (3,042) carries all 19,637 v10 entries. All slot/effect/mesh correlations above are therefore correlates of this one underlying zero-entry structure — NOT independent lines of semantic evidence. (26 zero-entry files sit in the field1=1 class: entry_count 0 ×26, consistent with R32's field2_raw=0 census.) The ENVIRONMENT-slot and NiTextureEffect tests return the same table (obs 316.790 both) — an OBSERVED-level echo of the R32 count-equivalence (1,694 == 1,694). Class MEANING remains unknown (runtime-gated).

## 6. PROBE-3 — event-registry per-string u32 values (263 strings / 136 blocks)

Families (pre-registered classifier; 263/263 classified, OTHER = 0):

| Family | n | zero-rate | non-zero value distribution (OBSERVED) |
|---|---|---|---|
| MORPH_LR (left/right + variants incl. typo 'rifgt') | 213 | 0.4883 | top: 0.3375×12, 0.6667×12, 1.3333×12, 0.3667×8, 0.5×6 |
| SOUND_HIT (hit_01..03) | 20 | 0.0000 | top: 1.6×4, 0.4667×2, 1.3667×2, 1.5×2, 0.6667×2 — never zero |
| START_USETOOL (effect/sound; 15 single + 2 multi-line combined) | 17 | 0.4706 | top: 0.0667×3, 0.3333×3, 0.0333, 0.6667, 0.4333 |
| ANIMCMD_500078 (start -name … -loop set) | 11 | 0.0909 | 1.6667, 3.3333, 10.167, 20.0, 15.167, … (large values) |
| END_MORPH1 ('end', 'morph: 1') | 2 | 0.0000 | 21.2667, 4.2333 |

Zero/non-zero × family chi-square: **OBSERVED correlation** — obs 24.826, perm p95 8.993, p_perm 0.0001 (10,000 label shuffles). OBSERVED-level reading (no semantics): the u32 is non-zero whenever SOUND_HIT and END_MORPH1 strings appear (20/20 and 2/2), near-always non-zero for the 500078 animation commands (10/11), and zero for ~49% of morph-left/right strings. All 263 values remain float-interpretable (0 non-finite); max 21.2667 (R30-consistent). Semantic role of the u32: UNVERIFIED (runtime-gated).

## 7. PROBE-4 — viewport float families (85B×592, 121B×79, 43B×11)

**POSITION-STATISTICS (labeled, NOT semantics)** — f32 at 4-aligned ext offsets (R8/R28 convention): position 1 decodes to **exactly 2.0 in 592/592 (85B) and 79/79 (121B)** files (distinct=1; the canon "fov-like ~2.0" constant). 43B: positions 2+ carry 1.0 / -0.2083 / -0.2710 / -16.32 / -48.65 / 0.747 in the 8 parametric files (R28-consistent). Other positions are heterogeneous across files (medians 0.0, hundreds of distinct values); **27/592 (85B) and 4/79 (121B) vectors contain non-finite 4-aligned bit patterns** (censused per position, n_nonfinite; excluded from min/max; sanitized to 0.0 for clustering — pre-registered amendment, see process note). Full tables: PROBE4_POSITION_STATS.json.

**43B subclass census**: all_zero_default ×3, parametric ×8 (pre-registered |f|>1e-6 rule; reproduces R28's own data exactly). Subclass × mesh: NO TEST (constant); subclass × block-count: NO OBSERVED (obs 5.958 = p95 5.958, p_perm 0.0583).

**k-means (pre-registered: raw vectors, Euclidean, restarts=5, max_iter=20, seed 20260906, empty-cluster re-seeding, elbow 0.80)**:
- 85B: k tested 2..5, inertia curve 1.088e78 / 8.592e77 / 8.762e77 / 6.705e77 → chosen **k=3, sizes {587, 2, 3}**.
- 121B: k tested 2..4, curve 2.444e77 / 1.768e77 / 1.047e77 → chosen **k=4, sizes {76, 1, 1, 1}**.
- Honest caveat: with the pre-registered unstandardized metric, distances are dominated by the large-magnitude positions (±1e38-scale reads); the clusters are one dominant group plus a few outliers — reported as-is.

**Cluster × file-class tests (each with its 10,000-label control):**

| Test | Verdict | obs chi² | perm p95 | p_perm |
|---|---|---|---|---|
| 85B cluster × skinned | **OBSERVED correlation** | 54.032 | 12.567 | 0.0014 |
| 85B cluster × block-count class | **OBSERVED correlation** | 29.858 | 17.119 | 0.0114 |
| 85B cluster × mesh / morph / particle / era-mirror | NO OBSERVED / NO TEST (mesh constant) | 0.043-0.465 | - | - |
| 121B cluster × all content classes | NO OBSERVED (skin 0.123/p95 25.695; blocks 5.675/42.863; …) | - | - | - |
| pooled ext-length class (85/121/43) × block-count | **OBSERVED correlation** | 98.933 | 19.224 | 0.0004 |
| pooled ext-length class × era-mirror | **OBSERVED correlation** (weak) | 8.203 | 6.590 | 0.0199 |
| pooled ext-length class × morph / skin / particle | NO OBSERVED (particle 5.593 = p95 5.593, p_perm 0.0633) | - | - | - |

OBSERVED-level reading (no semantics): the 2+3 85B outlier-cluster files are skinned/more-block-heavy files; ext-length class tracks block-count class strongly and era-mirror weakly. Per-field camera semantics remain PLAUSIBLE-not-CONFIRMED (ITER-8/28 status unchanged).

## 8. Process note (honesty; driver fixed 3× before the final run, re-hashed each time)

1. First analyze execution: reconciliation-code type bug (joint-tuple destructuring) fired the G2 HARD STOP — investigated: MY bug, not data drift; manual cross-check had already shown exact canon numbers. Fixed.
2. First PROBE-1 B6 used raw_bytes byte-size: fully-parsed blocks carry no raw_bytes in the frozen parser (discovered in-run) — pre-registered replacement: parser fields num_triangles/num_vertices (documented in the docstring amendment).
3. First k-means collapsed to a single cluster: (a) empty-centroid pathology — fixed by pre-registered farthest-point re-seeding; (b) NaN poisoning — 27/592 and 4/79 vectors carry non-finite 4-aligned bit patterns — fixed by the pre-registered non-finite→0.0 sanitization + n_nonfinite census. All amendments recorded in the driver docstring BEFORE the final run; every execution re-verified pins (R61 10/10 + corpus SHA + driver-hash provenance). The final driver hash (927b2566…) matches SHA256_DRIVER.txt; all shipped artifacts are from the final execution only.

## 9. SELF_CHECK (executor self-check, not independent MASTER audit)

- [x] Full raw census: 5,596/5,596 parsed; populations 758/4,838/263/682 as contracted; every number re-derived from pinned bytes.
- [x] All gates evaluated: G1-G6 (below); G3 = 33 permutation controls executed + 9 constants documented (42 rows).
- [x] Negative controls present: permutation p95/p_perm reported for EVERY executed test, including the no-correlation ones (e.g., PROBE-1 B1 obs 0.359 vs p95 9.540; 121B cluster tests; 43B-sub blocks obs == p95 → correctly NOT claimed).
- [x] Source/generator hashes: corpus c950a8c2… (pin), R61 10/10, driver 927b2566… == SHA256_DRIVER.txt, artifacts hashed in-driver in artifact_index.csv.
- [x] No default-success fallback: CENSUS_MISMATCH HARD STOP fired and was investigated when triggered (execution #2); constants produce NO TEST, never PASS.
- [x] Scope: read-only originals; zero payloads; no R61/source/wiki/AUDIT_ENTRYPOINT/CORRECTION_LEDGER writes; no milestone crossing; no nested tasks.

## 10. STAGE ACCEPTANCE GATES

G1 pins PASS · G2 canon reconciliation PASS (all contract numbers EXACT) · G3 every executed probe carries its 10,000-label permutation control (33 executed; 9 constants documented) PASS · G4 all outputs OBSERVED-labeled + standing no-semantic-proof sentence present (this report + every 05_ANALYSIS JSON) PASS · G5 machine-readable per-probe JSON/CSV PASS · G6 discipline (read-only originals; run dir + 99_Audits byte-identical mirror; zero payloads; path-limited commit; push; origin==HEAD) PASS — see STAGE_ACCEPTANCE_GATES.csv.

## 11. FINAL HANDOFF BLOCK

RUN_ID = PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200
AUDIT_OUTPUT_ROOT = docs/audits/PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200 (repo) + 99_Audits mirror
FINAL_REPORT_PATH = 06_Report/00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = 01_RAW/EXTRACTION.json; 01_RAW/PROBE1_RAW.csv; 01_RAW/PROBE2_RAW.csv; 01_RAW/PROBE3_RAW.csv; 01_RAW/PROBE4_RAW.csv; 05_ANALYSIS/RECONCILIATION.json; 05_ANALYSIS/PROBE1_CONTINGENCY.json; 05_ANALYSIS/PROBE2_CONTINGENCY.json; 05_ANALYSIS/PROBE3_FAMILIES.json; 05_ANALYSIS/PROBE4_POSITION_STATS.json; 05_ANALYSIS/PROBE4_CLUSTERS.json; 00_Control/semantic_correlations_r1.py; STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv
RUN_STATUS = COMPLETED (all 4 probes executed with controls; 0 census mismatches; no HARD STOP)
HARD_STOP_REASON = NONE (one transient CENSUS_MISMATCH HARD STOP during development execution #2 was a reconciliation-code bug, fixed before the final run; final run G2 = 0 mismatches)
