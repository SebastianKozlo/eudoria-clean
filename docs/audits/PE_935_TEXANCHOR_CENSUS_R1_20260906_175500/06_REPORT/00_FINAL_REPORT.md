# PE_935_TEXANCHOR_CENSUS_R1 — FINAL REPORT (era PCG_9_3_5, RUN_CLASS MATERIAL)

**RUN_ID**: PE_935_TEXANCHOR_CENSUS_R1_20260906_175500
**Parent**: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 4) | **Milestone**: EU935-M1 (NO crossing)
**Executor**: pe-reconstruction | **Contract**: 00_CONTROL/CONTRACT.md (SHA256 4ba68d73fbc8551caad87b73d33a68ef156d54c259e2ffbb8ff482f58bcf215f, verified in-driver)
**Driver**: 00_CONTROL/texanchor_census_r1.py, SHA256 be22fae22383b66ee9dc3ffda33b0fadad1fc9dec42342663333eff191aa3f8c (hash-after-last-edit, verified in-driver) | **Frozen method**: 00_CONTROL/FROZEN_METHOD.md (SHA256 823bf9fd12367271a55a7c614681faf28b1b6eac9ed7ec6b77c967fe7a1347ff), pre-registered with PREREG_MARKER.txt BEFORE the run

**STANDING SENTENCE: correlation/association outputs are OBSERVED-level evidence; semantic roles remain runtime-gated; no semantic claims.**

The K1 chain resolution (24,474/24,508) is NOT re-tested — it stands. This run is a
MEASUREMENT (KROK-3 pattern): no PASS/FAIL is attached to any anchor fraction.

---

## 1. P0 ANSWER

**OBSERVED (era PCG_9_3_5, denominator 24,508 K1 ArkTexture entries):** 19,705/24,508 =
**80.4023%** of entries are structurally name-anchored to their OWN file (exact binomial 95%
CI [79.8997%, 80.8977%]) — the mesh-part resolves to a mesh/material name present in the same
file AND the slot field equals the name's slot suffix — versus the seeded cross-file negative
control at **67/10,000 = 0.6700%** (CI [0.5196%, 0.8501%]; seed 20260906): a **120.0x**
file-specific association strength. Component (a) own-file mesh-part resolution =
19,705/24,508 = 80.4023% (exact-spelling 1,103 = 4.4998%; colon-bridge-only 18,602 =
75.9025%; unresolved 4,803 = 19.5977%); component (b) slot-field/suffix consistency =
24,508/24,508 = 100.0000% (CI [99.9849%, 100.0000%]). The anchoring is not uniform:
the 7 static slot families anchor at 87.27–98.00% while ENVIRONMENT (0/1,694) and every
ANIM0–31 slot (0/1,157) anchor at 0.0000% (ENVIRONMENT CI [0.0000%, 0.2175%]).

## 2. Inputs and pins (G-PINS: PASS)

| Item | Value |
|---|---|
| K1 table | `PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\01_RAW\ARKTEXTURE_ID_TABLE.csv` — SHA256 34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9 re-hashed in-driver |
| Corpus | `pcg_install\Data\Models\Models.bnt` — SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0 re-hashed in-driver; BNT2 index 5,596 entries, exact consumption, 0 anomalies |
| Frozen parser | R61 (`PE_R61_FROZEN_BASELINE_20260828\01_source`) — 10/10 SHA pins verified in-driver BEFORE any parse; READ-ONLY; never modified; re-hashed 10/10 after the run |
| Parse closure | 5,596/5,596 PASS (HARD STOP not triggered) |
| Pre-registration | FROZEN_METHOD.md + PREREG_MARKER.txt written BEFORE the execution; the driver verifies the marker records the physical method+driver hashes at start |

## 3. G-CENSUS: the K1 table reproduces from the pinned corpus (PASS)

The driver re-derived every entry from the corpus bytes (v10 from the frozen parser's
`ark_tex_textures` + trailing decode; v4 by the R32/K1-validated raw decode) and compared
row-for-row against the pinned table: **24,508/24,508 rows checked, 0 mismatches** on all of
block_index, entry_idx, name, f1, f2, ref, anim_flag, frame_index, bnt2_id, version, grammar;
v10 19,637 / v4 4,871 exact; per-file counts exact on all 3,767 entry-bearing files; the
24,474/34 resolved split untouched (table-pinned property). Validation layers: v10 raw
re-decode 4,838/4,838 (0 failures), v4 exact consumption 758/758 (0 failures).

## 4. Frozen method (pre-registered; 00_CONTROL/FROZEN_METHOD.md)

- **Name-part extraction**: split at the LAST underscore (ITER-32/K1 convention).
- **Own-file universe U_f**: the mesh/material names the frozen R61 parser exposes
  (NiTriShape + NiMaterialProperty `fields["name"]`, non-empty) plus the colon-bridge twin
  of each name (last ":" → "_" iff the tail is digits). Pre-freeze calibration (full corpus,
  READ-ONLY probes): 20,833/21,914 non-empty NiTriShape names end in ":<digits>" (3ds Max
  multi-material export spelling, e.g. "CISTERN:4") while entry mesh-parts spell the same
  identifier with "_" ("CISTERN_4"); exact-only membership would resolve 1,103/24,508 —
  the bridge is the OBSERVED dual spelling of the same exposed names, not fuzzy matching.
  Bridge collisions: 0.
- **Predicate**: anchored = (mesh_part ∈ U_f(own file)) AND (K1 table slot column == extracted
  suffix); components reported separately.
- **NC**: random.Random(20260906); 10,000-entry simple random sample without replacement;
  per trial a uniformly-chosen OTHER entry-bearing file; self-pairing excluded by construction
  (0 observed; asserted per trial); determinism re-proven in-driver (sample sequence and all
  pairings identical on re-derivation).
- **CIs**: exact binomial (Clopper-Pearson) via regularized incomplete beta; validated
  in-driver against definitional brute-force tail sums on 16 (k,n) pairs including edges
  (worst delta 2.8e-14) and closed forms.

## 5. The measurement (all OBSERVED; every number with its denominator)

| Metric | Count / denominator | Rate | Exact binomial 95% CI |
|---|---|---|---|
| **Anchored (own-file resolution AND slot consistency)** | **19,705 / 24,508** | **0.804023** | **[0.798997, 0.808977]** |
| Component (a): own-file mesh-part resolution | 19,705 / 24,508 | 0.804023 | [0.798997, 0.808977] |
| — resolution mode exact spelling | 1,103 / 24,508 | 0.044998 | — |
| — resolution mode colon-bridge only | 18,602 / 24,508 | 0.759025 | — |
| — unresolved (none) | 4,803 / 24,508 | 0.195977 | — |
| Component (b): slot field == slot suffix | 24,508 / 24,508 | 1.000000 | [0.999849, 1.000000] |
| **NC anchored (cross-file, seed 20260906)** | **67 / 10,000 trials** | **0.006700** | **[0.005196, 0.008501]** |
| NC other-file mesh-part resolution | 67 / 10,000 | 0.006700 | [0.005196, 0.008501] |
| Anchored / NC ratio | — | **120.00x** | — |

## 6. Sub-censuses (each group: n, anchored, rate, CI — full tables in 05_ANALYSIS/ANCHOR_RESULTS.json)

**Per-slot (the 40-slot canon; 40/40 slots present, population sum 24,508):**

| Slot | n | anchored | rate | CI95 |
|---|---|---|---|---|
| BASE | 14,307 | 12,867 | 0.89935 | [0.894304, 0.904233] |
| GLOSS | 2,791 | 2,571 | 0.921175 | [0.910551, 0.930906] |
| DARK | 1,816 | 1,750 | 0.963656 | [0.953992, 0.971783] |
| ENVIRONMENT | 1,694 | **0** | **0.000000** | [0.000000, 0.002175] |
| GLOW | 1,524 | 1,330 | 0.872703 | [0.854921, 0.889035] |
| BUMP | 970 | 946 | 0.975258 | [0.963408, 0.984084] |
| DETAIL | 199 | 192 | 0.964824 | [0.928870, 0.985743] |
| DECAL0 | 50 | 49 | 0.980000 | [0.893530, 0.999494] |
| ANIM0–ANIM31 (32 slots) | 1,157 | **0** | **0.000000 each** | per-slot CIs in ANCHOR_RESULTS.json |

**Per-grammar / per-version / per-class:**

| Group | n | anchored | rate | CI95 |
|---|---|---|---|---|
| v10 (10.1.0.0) | 19,637 | 15,721 | 0.800581 | [0.794922, 0.806150] |
| v4 (4.1.0.12) | 4,871 | 3,984 | 0.817902 | [0.806772, 0.828649] |
| K1-resolved class | 24,474 | 19,690 | 0.804527 | [0.799502, 0.809480] |
| K1-dangling class | 34 | 15 | 0.441176 | [0.271850, 0.621142] |

(The one 4.0.0.2 file, 52555.nif, bears no ArkTexture entries, so the per-entry version
census has exactly two groups; the identity sum 19,637 + 4,871 = 24,508 is asserted.)

**Unresolved structure (OBSERVED, 4,803 misses):** ENVIRONMENT 1,694 (100% of that
population; mesh-parts are the R32-documented NAMELESS_N materials, e.g. "Nameless0" x583,
"Nameless12" x224) + all ANIM slots 1,157 (100%; "_NONE" effect materials, e.g.
"Geo_Flame_0_NONE" x200) + static-slot misses 1,952 (BASE 1,440, GLOSS 220, GLOW 194,
DARK 66, BUMP 24, DETAIL 7, DECAL0 1). The miss evidence also shows a space-vs-underscore
spelling residue (e.g. mesh-part "Editable_Mesh" x84 vs NiTriShape names spelled
"Editable Mesh" in some v4 files) — unresolved under the frozen colon-bridge rule and
reported as-is; the per-record JSONL carries every case.

## 7. Supplementary OBSERVED censuses (NOT part of the frozen predicate; no semantic claims)

- **f1 enum agreement**: 24,336/24,508 = 0.992982 (CI [0.991856, 0.993989]) against the
  ITER-32-confirmed mapping (BASE=0, DARK=1, DETAIL=2, GLOSS=3, GLOW=4, BUMP=5, DECAL0=6,
  ENVIRONMENT=9, ANIMn=11; excluded suffixes not in the enum: 0). The 172 disagreements are
  exactly the ITER-32-documented ANIM exceptions (f1=0 x142 / f1=4 x30) — reproduced, not
  reinterpreted. Recorded per record (`sup_f1_enum_match`).
- **NiNode-universe variant**: mesh_part ∈ the file's NiNode-name set resolves only
  21/24,508 = 0.000857 — the anchoring surface is the NiTriShape/material names, not the
  NiNode names (recorded per record, `sup_ninode_resolution`).

## 8. K1-caveat refinement (one paragraph, as contracted)

The K1 chain physically verified ID-membership — 24,474/24,508 = 99.8613% of ArkTexture
bnt2_ids exist in Textures.bnt — while explicitly caveating that ID-membership is not
automatically proof of every mesh→texture association. This run measures that gap's
structure (OBSERVED, era PCG_9_3_5): the association between an ArkTexture entry and its OWN
file is strong and file-specific — 80.40% of entries name-anchor to a mesh/material name in
their own file at 120x the cross-file chance rate (0.67%) — but it is NOT universal: the
ENVIRONMENT and ANIM slot families (2,851 entries = 11.63% of the census) anchor at exactly
0% (their mesh-parts are the R32-documented NAMELESS_N / "_NONE" material spellings, absent
from their files' NiTriShape/material names), and 1,952 static-slot entries also lack own-file
name matches. ID-membership therefore coexists with strong per-file name anchoring for the
seven static slot families and with zero name-anchoring for env/anim families; what the
anchor MEANS at runtime remains runtime-gated.

## 9. Honest NOT_CHECKED list

1. **Runtime meaning**: what name-anchoring (or its absence) MEANS for runtime texture
   binding is runtime-gated — this run makes no semantic claims (the standing sentence).
2. **The K1 bnt2_id resolution was not re-derived**: the 24,474/34 split is taken as the
   pinned K1 property; Textures.bnt was not parsed this run (out of scope).
3. **f1 semantics**: reported only as the OBSERVED enum-agreement census; not used in the
   frozen predicate; the 172 ANIM exceptions are the ITER-32-documented ones.
4. **The space-variant spelling residue** ("Editable_Mesh" vs "Editable Mesh") is
   documented from the miss evidence but NOT bridged — the frozen predicate ran as
   pre-registered; any follow-up is PE-MASTER's decision.
5. **No era-2003 leg**: PCG_9_3_5 only; the 2003 corpus was not touched.
6. **The NC samples entries, not files**: the contract's NC design (10,000 sampled entries,
   uniform over the other entry-bearing files) was executed exactly as frozen; no
   file-stratified variant was run.

## 10. SELF_CHECK (executor self-check; not independent MASTER audit)

- [x] Full raw census: 24,508 per-record outcomes + 10,000 NC trial records + 3,767 file
  universes written and line-counted (ANCHOR_OUTCOMES.jsonl 24,508 lines; NC_TRIALS.jsonl
  10,000; FILE_UNIVERSES.jsonl 3,767); G-CENSUS re-derivation 24,508/24,508, 0 mismatches.
- [x] All gates evaluated: G-PINS PASS, G-CENSUS PASS, G-METHOD PASS (marker + hashes),
  G-EXEC PASS (8/8 fixtures fail-closed + 6/6 manifest negative tests + self-audit), G-SCOPE
  PASS; the anchor fractions themselves carry NO PASS/FAIL (measurement, per contract).
- [x] Meaningful negative controls: seeded cross-file NC 67/10,000 with explicit
  denominators + determinism re-proof; 8 fail-closed fixtures; 6 manifest negative tests.
- [x] Correct source/generator hashes: every pin re-hashed in-driver before and after;
  driver hash == SHA256_DRIVER.txt; prereg marker records the physical method+driver hashes.
- [x] No default-success fallbacks: every pin/census path is HARD-STOP armed; degenerate
  populations yield explicit non-pass (fixture 1 proof); empty/duplicate/corrupt inputs
  rejected (fixtures 2/3/5).
- [x] Zero size-derived validation numbers (AST self-scan of the gate functions: 0 findings);
  read-only originals untouched (re-hashed after); zero payloads; outputs only in this run
  dir; NO commit (per contract).

## 11. STAGE ACCEPTANCE GATES

G-PINS PASS · G-CENSUS PASS (24,508/24,508 row-for-row; 0 mismatches) · G-METHOD PASS
(pre-registered + hash-recorded) · G-EXEC PASS (per-record outcomes; 8/8 fixtures fail-closed;
6/6 manifest negative tests; zero size-derived scan) · G-SCOPE PASS (read-only originals;
zero payloads; run-local tooling in 00_CONTROL only; artifact_index per spec +
self-validation PASS) — see STAGE_ACCEPTANCE_GATES.csv.

## 12. Artifacts (REAL SHA-256 in artifact_index.csv)

- `00_CONTROL/`: CONTRACT.md, FROZEN_METHOD.md, PREREG_MARKER.txt, SHA256_DRIVER.txt,
  texanchor_census_r1.py, write_manifest_r1.py, PIN_RESULTS.json, GATES_RESULTS.json,
  DRIVER_LOG.txt, CALIBRATION_PROBE{,2,3} (pre-freeze READ-ONLY calibration evidence).
- `01_RAW/`: ANCHOR_OUTCOMES.jsonl (24,508), NC_TRIALS.jsonl (10,000),
  FILE_UNIVERSES.jsonl (3,767), CENSUS_REPRODUCTION.json, NEGATIVE_FIXTURES_GEXEC.json,
  MANIFEST_NEGATIVE_TESTS.json, SELF_AUDIT.json, SCOPE_CHECK.json.
- `05_ANALYSIS/`: ANCHOR_RESULTS.json, MANIFEST_VALIDATION.json.
- `06_REPORT/`: this report + HANDOFF.md. Run root: STAGE_ACCEPTANCE_GATES.csv,
  artifact_index.csv.

**Every number above is OBSERVED-level evidence, era PCG_9_3_5, with its denominator.
Semantic roles remain runtime-gated; no semantic claims.**

Component (b) slot-suffix consistency 24,508/24,508 = 100% is a definitional identity under the same last-underscore convention the K1 table used (caveat per INTERNAL_QC_R1 D3); the substantive association signal is component (a) + the 120x cross-file separation.
