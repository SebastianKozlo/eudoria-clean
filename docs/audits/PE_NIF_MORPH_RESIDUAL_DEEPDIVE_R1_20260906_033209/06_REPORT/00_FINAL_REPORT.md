# PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1 — FINAL REPORT

**RUN_ID**: PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209
**Date**: 2026-09-06. **PARENT_RUN**: PE-MASTER loop 0132d23c-2f0f-42f2-bb07-fb74f637488b (KROK 2 of 3).
**MILESTONE**: EU935-M1 bounded contribution (NO milestone crossing). **ERA**: PCG 9.3.5 primary (corpus `pcg_install\Data\Models\Models.bnt`, SHA256 `c950a8c2…bee0`, verified in-driver). 2003 not used as a data source this run.
**P0 (one question)**: can the remaining NiVertexMorphExtraData segmentation ambiguity — the 334 classifier-real spans fitting no tested grammar (62 with recorded alternative fits, 272 with none) + the 325-span heterogeneous residual — be RESOLVED (higher byte-exact coverage with a validated grammar) or honestly BOUNDED?

## EXECUTIVE VERDICT: **PARTIALLY_RESOLVED** (both halves moved; nothing forced)

```
1. BASELINE (G2): reproduced EXACTLY, row-by-row — the R18 walk
   10,274/6,167/65,050/143,874; per-span agreement with the pinned R34
   REAL_SPARSE_GRAMMAR.json 6,167/6,167 (g1/g2/var/mscan/rr/wp all
   identical); rr=2,427, var-k=2,093, nofit=334 (62 alt + 272 none);
   neither=3,438, backtrack=3,105, shift=114, shift-only=8, unknown325=325
   (56 files, 551564.nif x84), r21-unknown=333; R21 probe 41/0.4197/0.8096.
   ZERO baseline drift — no CENSUS_MISMATCH.
2. PHASE 1 (the 334): coverage 2,093 -> 2,158/2,427 (86.2% -> 88.88%)
   via TWO pre-registered CONFIRMED grammars that passed their negative
   controls AND the 50/50 overfitting control:
     H5a truncated-tail:   +39 spans (var-k records + a <=41 B truncated
                            next-record head; leftover histogram 4x25,
                            18x6, 30x5, 38x2, 22x1; NC u±2 = 5;
                            OC 20/19 deterministic PASS)
     H5c idx-relaxed var-k: +26 spans (byte-exact var-k shape once the
                            idx<N bound is relaxed to idx<0x8000 (26) /
                            idx<2N (25, subset); NC = 5; OC PASS)
     -> union 65 (disjoint); REMAINING NO-FIT: 269.
   Everything else FALSIFIED with counts (below). H3/H4 were CONFIRMED
   by their pre-registered predicates and then KILLED BY THE
   OVERFITTING CONTROL exactly as designed (canonical-shift validation
   2/5 and 1/6 -> REJECTED_BY_OVERFITTING_CONTROL).
3. PHASE 2 (the 325): H7 false-tag-split CONFIRMED — 74 of the 325
   (22.8%) are join-explained: the span plus its neighbor (with the 2
   tag bytes restored as data) is Family-A-consumable end-to-end; the
   non-adjacent-join negative control reproduces only 3 (~6% of tested
   files) — a ~4x separation. Residual census: 325 -> 251 unexplained.
   H6 (phase-shift scan): REJECTED_as_coincidental — 130 of 325 fit the
   greedy walk at SOME shift, but the shift histogram is DIFFUSE
   (-52..+128, top-3 concentration 39%) and the per-start fit base rate
   is 7.9%: with a ~257-start window ~20 fitting starts per span are
   expected by coincidence. H8 (pure float array): 26 of 333 < 30 ->
   the third-family candidate is DEAD.
4. SEGMENTATION STATUS: PARTIALLY_RESOLVED. The remaining 269 rr-no-fit
   + 251 residual spans are now BOUNDED with a complete falsified-
   hypothesis list (machine-readable in 05_ANALYSIS/*.json).
```

## RUN PACKAGE (single execution, no post-hash driver edits)

- Driver `00_CONTROL/morph_residual_deepdive_r1.py`, SHA256
  `b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a`
  (SHA256_DRIVER.txt written after the last edit, BEFORE the run; the
  driver re-verifies it in-prologue). Runtime 27.9 s; exit 0.
- Post-hoc characterization probe (CLEARLY LABELED NON-COVERAGE,
  adds nothing to any coverage number):
  `00_CONTROL/h1_desync_probe_posthoc.py` -> `01_RAW/H1_DESYNC_PROBE.json`.
- BASE_SHA at start: `b4dda2e34d1f1c0d1e09836e79ac7c2dfe1deb3d`
  (eudoria-clean master, clean tree, origin==HEAD).

## G1 — INPUT PINS (all verified in-driver before any work)

| artifact | SHA256 (prefix) | status |
|---|---|---|
| R61 frozen parser manifest | 10/10 .py | PASS |
| corpus Models.bnt | c950a8c2…bee0 | PASS |
| R34 driver | 8d788a9a… | PASS (== R34 SHA256_DRIVER) |
| R34 QUANT_TESTS.json | f07b22e3… | PASS |
| R34 REAL_SPARSE_GRAMMAR.json | 2c26ba86… | PASS |
| R21 HEX_UNKNOWN.txt | c88a1a14… | PASS |
| R21 UNKNOWN325_PROBE.json | db8cafda… | PASS |
| R33 MORPH_IDS_FULL.jsonl | 90c1b8ad… | PASS |
| R20 driver | a22ff130… | PASS (matches R20 REPORT "A22FF130…") |

Full pin table: `00_CONTROL/INPUT_PIN_RESULTS.json`.

## G2 — BASELINE REPRODUCTION (EXACT; hard gate held)

- Walk (R18 run6 predicates, verbatim): big=10,274, fit=6,167,
  entries=65,050, pad_floats=143,874 — **EXACT**.
- R34 state: rr spans 2,427 (def: has_real AND n_wp_inrange>0); var-k
  2,093; no-fit 334 = 62 alt + 272 none. Corpus grammars re-derived:
  g1=132, g2=1,547, mscan-any=3,705, var=3,186 — all match R34's REPORT.
- **Row-by-row agreement vs the pinned R34 JSON: 6,167/6,167 spans**
  (file/bi/si keyed; g1_ok, g2_ok, var_ok, mscan list, has_real,
  n_wp_inrange identical; 0 disagreements).
- Residual census (R20/R21 predicates verbatim): neither=3,438;
  backtrack=3,105; shift=114; shift-only=8; unknown-325=325 (56 files;
  551564.nif x84); r21-unknown=333; r19-only=669.
- R21 probe reproduction on the 333: weight-pair 41; entry-density mean
  0.4197; f32-sanity mean 0.8096 — EXACT vs UNKNOWN325_PROBE.json.

## PHASE 1 — the 334 no-fit classifier-real spans (H1–H5)

All hypotheses were pre-registered (predicate text on disk BEFORE any
test: `00_CONTROL/PRE_REGISTERED_HYPOTHESES.json` + PREREG_MARKER.txt).
Negative control NC1 = the same grammar at deliberately-wrong starts
u+2/u−2 on the same 334 spans.

| id | grammar tested | result | counts |
|---|---|---|---|
| H1 | 62 alt grammars characterized; derived H1d weights-at-tail `[u16 idx][9×f32][k×f32 sum≈1]` | **REJECTED** | H1d fits 0/272, NC 0; characterization below |
| H2a | var-k k∈9..16, tol 1e-4 | **REJECTED** | 0 fits (NC 5) |
| H2b | var-k k∈1..8, tol 1e-3 | **REJECTED** | 1 fit (NC 5) |
| H2c | var-k k∈1..8, tol 1e-2 (0.99..1.01) | **REJECTED** | 7 fits vs NC 5 (1.4x — fails the >=5x separation) |
| H3 | start-phase shift δ∈[-15,+15] | **REJECTED_BY_OVERFITTING_CONTROL** | 10 fits, concentration 1.0 (δ: -2x5, +8x4, +12x1); canonical δ=-2 validates only 2/5 |
| H4 | W-misestimate u'∈[u-64,u+64] step 4 | **REJECTED_BY_OVERFITTING_CONTROL** | 12 fits, concentration 0.83 (δ: +8x4, +44x4, +40x2, +28x1, +12x1); canonical δ=+8 validates only 1/6 |
| H5a | truncated-tail var-k (leftover 1..41 B, head idx<N) | **CONFIRMED** | 39 fits (11.7%); leftover 4x25/18x6/30x5/38x2/22x1 (r=41 dominance 0.0); NC 5 (7.8x); OC 20/19 PASS |
| H5b | mscan extension m∈33..64 | **REJECTED** | 0 fits (NC 0) |
| H5c1 | var-k, idx<2N | **CONFIRMED** | 25 fits; NC 5; OC 13/12 PASS |
| H5c2 | var-k, idx<0x8000 | **CONFIRMED** | 26 fits (superset of H5c1 for N<16384); NC 5; OC 13/13 PASS |
| H5d | ndelta ∈ {3,6,12} | **REJECTED** | 0/0/0 fits |

**H1 characterization (what the 62 alternative grammars ARE)**: all 62
carry a fixed-m mscan fit (62/62; g2 48, g1 5); Wm/W census (42,10)x38,
(126,31)x12, (46,11)x8, (50,12)x4. Inside their fixed-m records the
weight pair lives AT THE RECORD HEAD (pair@0+1 x245; no tail-position
cluster) — same head semantics as the canon grammar; 23/62 spans have
ALL records weight-paired, 39/62 partial, 0 zero. The derived
weights-at-tail grammar therefore dies (0/272). The labeled POST-HOC
probe (`01_RAW/H1_DESYNC_PROBE.json`, NON-COVERAGE) shows the failure
mechanics: largest-k-first preference rescues 11 spans (5 of the
all-paired 23 — the R34-documented smallest-k selection ambiguity is
real but small), k2-first 10, k2-only 6, k1-only 0; the remaining
all-paired spans are WIDE-RECORD spans (dominated by Wm=126,
es_len=130, single `[u16 idx][32×f32]` records = mscan m=32 — a ~23-
weight record that exceeds even the H2a k≤16 extension). A kmax≈24
var-k test is the natural NEXT pre-registered candidate (recorded as
a lesson candidate; NOT claimed as coverage).

**Coverage accounting (the honest caveat)**: the +65 coverage comes
from grammars WEAKER than canon — H5a tolerates a bounded truncated
tail (<=41 B, head-validated), H5c drops the idx<N semantic for some
records (their idx values run 768..1536-class, median 896 — the R33
even-32 head cluster; these spans are byte-exact in SHAPE but their
vertex-index semantics is violated on some records). The two sets are
disjoint (union 65; overlap with each other 0). The remaining 269
no-fit spans fail every tested grammar including all extensions.

## PHASE 2 — the 333/325 residual spans (H6–H8)

| id | test | result | counts |
|---|---|---|---|
| H6a | Family A greedy at every start in [u-128, u+128] | **REJECTED_as_coincidental** | 136/333 spans fit at SOME shift (130 of the 325); delta histogram DIFFUSE (-52..+128; top-3 concentration 39% < 50%); per-start fit base rate 7.92% — ~20 fitting starts/span expected by chance in a ~257-start window; 5 spans skipped (dp>8192, recorded) |
| H6b | Family B unit model, start ∈ [Wm-64,Wm+64] step 2, m∈1..12 | **REJECTED_as_coincidental** | 20/333 fit (12 of 325); concentration 35% < 50% |
| H7 | false-tag-split adjacency: prev-join / next-join / full-block re-join | **CONFIRMED** | prev-join 45, next-join 50 (overlap 14; union 81/333); **74 of the 325 (22.8%) join-explained**; full-block re-join 0 (32 blocks skipped, rest>32768); NC3 non-adjacent join = 3 (~6% of tested files vs 22.8% — ~4x separation); OC PASS (structural grammar, no free parameter) |
| H8 | third family: pure fixed-stride float array | **REJECTED** | 26/333 pure arrays (< 30 threshold) — the candidate dies |

**H7 mechanism (era-labelled PCG 9.3.5 observation)**: the residual
spans are largely FRAGMENTS of Family-A streams cut by coincidental
occurrences of the block's 2-byte tag INSIDE record data — the
tag-split span model itself has a measured false-split rate. When the
fragment is re-joined with its neighbor (the 2 tag bytes restored as
data), the greedy walk consumes the joined stream end-to-end. This
explains 74 of the 325 at the join level and is consistent with H6's
diffuse shift-fits (the fragment's true walk-start lives in the
neighbor span, not at any canonical offset). Honest bound: the greedy
walk is a permissive consumption model (pads absorb); the ~4x
separation over the non-adjacent join control is the strength of the
claim, and 251 of the 325 remain unexplained at this depth.

## OVERFITTING CONTROL (G4) — applied to every coverage-increasing grammar

| grammar | mode | fit half | validation half | validation exact | verdict |
|---|---|---|---|---|---|
| H1d | — | not CONFIRMED (0 fits) | — | — | n/a |
| H5a | deterministic | 20 | 19 | 19 | **PASS** |
| H5c1 | deterministic | 13 | 12 | 12 | **PASS** |
| H5c2 | deterministic | 13 | 13 | 13 | **PASS** |
| H7 | structural (NC-based) | 37 | 37 | 37 | **PASS** |
| H3 | canonical-param (δ) | 5 | 5 | 2 | **FAIL -> REJECTED** |
| H4 | canonical-param (δ) | 6 | 6 | 1 | **FAIL -> REJECTED** |

The control did its job: H3 (10 fits) and H4 (12 fits) passed their
pre-registered population-level predicates but their canonical-shift
grammars do not generalize (per-span free shifts = overfit) — both
downgraded to REJECTED_BY_OVERFITTING_CONTROL and EXCLUDED from
coverage. No default-success: every CONFIRMED grammar carries an OC
entry; deterministic OC is a formal re-validation whose real
protection is the u±2 negative control (5.2x-7.8x separations).

## FINAL OUTPUT STATE (machine-readable: 05_ANALYSIS/COVERAGE_STATE.json)

```
REAL-RECORD COVERAGE: 2,158/2,427 = 88.88%  (canon 2,093/2,427 = 86.2%)
  +39 H5a truncated-tail; +26 H5c idx-relaxed (disjoint); remaining 269
RESIDUAL CENSUS: 325 -> 74 join-explained (H7 false-tag-split),
  251 remain unexplained; H6 shift-fits classified COINCIDENTAL
  (diffuse histogram; 7.92%/start base rate); H8 third family DEAD.
FALSIFIED (with counts, all era PCG 9.3.5):
  H1/H1d (0/272), H2a (0), H2b (1), H2c (7 vs NC5), H3 (OC 2/5),
  H4 (OC 1/6), H5b (0), H5d (0/0/0), H6a (diffuse, base 7.92%),
  H6b (diffuse), H8 (26 < 30).
SEGMENTATION STATUS: PARTIALLY_RESOLVED — the remaining 269 + 251 are
  BLOCKED at this depth with the falsification list above.
```

## Honest caveats

1. The +65 Phase-1 coverage uses grammars structurally weaker than the
   canon var-k (bounded tail exception; idx semantic relaxed) — the
   coverage number is byte-exact SHAPE coverage, and per-record vertex-
   index semantics is violated on some H5c records.
2. H7's join evidence is bounded by the greedy walk's permissiveness;
   the ~4x NC separation is the honest strength; the full-block re-join
   variant could not run on 32 blocks (rest>32,768 B, skipped +
   recorded).
3. H6a skipped 5 spans (dp>8,192 B); H4's window was pre-registered
   shrunk to ±16 for es_len>4,096 (compute bound).
4. The post-hoc probe is labeled NON-COVERAGE everywhere; its findings
   (smallest-k ambiguity rescues ~11; wide m=32 records) are lesson
   candidates for the NEXT pre-registered run (kmax≈24), not claims.
5. The R21 HEX_UNKNOWN.txt artifact contains 147 top-5-file dumps, not
   the full 333 (contract described it as "the full residual hex");
   this run re-dumped all 333 to 01_RAW/RESIDUAL333_SPANS.txt, so the
   gap is closed for any future deep dive.
6. Segmentation uniqueness remains unproven for the canon grammar
   (unchanged from R34); this run adds two more validated-but-weaker
   segmentations rather than resolving uniqueness.

## Reproduction

```
python 00_CONTROL\morph_residual_deepdive_r1.py
```
Expect: G1 pins PASS; walk 10,274/6,167/65,050/143,874 EXACT; row
agreement 6,167/6,167; rr 2,427/var 2,093/nofit 334 (62+272); neither
3,438/bt 3,105/shift 114/only 8/unknown 325 (56 files, 551564 x84)/
r21u 333; probe 41/0.4197/0.8096; H1 0/0; H2a 0; H2b 1; H2c 7;
H3 10->OC-FAIL; H4 12->OC-FAIL; H5a 39; H5b 0; H5c1 25; H5c2 26;
H5d 0; H6 130-of-325 diffuse/12-of-325 diffuse; H7 74-of-325; H8 26;
coverage 2,158/2,427; ~28 s.

## FINAL HANDOFF BLOCK

```
AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209
LOCAL_MIRROR       = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209 (byte-identical)
FINAL_REPORT_PATH  = 06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = 05_ANALYSIS\BASELINE_REPRODUCTION.json,
  05_ANALYSIS\HYPOTHESIS_RESULTS.json, 05_ANALYSIS\COVERAGE_STATE.json,
  01_RAW\NOFIT334_SPANS.txt, 01_RAW\RESIDUAL333_SPANS.txt,
  01_RAW\H1_DESYNC_PROBE.json, 00_CONTROL\PRE_REGISTERED_HYPOTHESES.json,
  STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv
RUN_STATUS = COMPLETED (PARTIALLY_RESOLVED; PARTIAL class per contract — progress documented without full closure)
HARD_STOP_REASON = NONE
```
