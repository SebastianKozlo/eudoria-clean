# FROZEN_METHOD — PE_935_TEXANCHOR_CENSUS_R1_20260906_175500 (era PCG_9_3_5)

**STANDING SENTENCE (applies to every output of this run):** correlation/association
outputs are OBSERVED-level evidence; semantic roles remain runtime-gated; no semantic
claims.

RUN_CLASS: MATERIAL (a measurement refining the confirmed K1 claim's caveat — no new
format-field meaning). The K1 chain resolution (24,474/24,508) is NOT re-tested; it
stands. This run measures only.

Pre-registered BEFORE the census execution (see PREREG_MARKER.txt for the hash record).
Pre-freeze calibration evidence: 00_CONTROL/CALIBRATION_PROBE{,2,3}_*.py/.json (READ-ONLY
exploration; all numbers below re-derived fresh by the frozen driver).

---

## M1. Populations and denominators (explicit, fixed)

- **Entry population**: every row of the pinned K1 table
  `ARKTEXTURE_ID_TABLE.csv` (SHA256 34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9):
  expected 24,508 rows = v10 19,637 + v4 4,871; resolved 24,474 / dangling 34 (the K1
  split, UNTOUCHED); 3,767 entry-bearing files. Entry key = (nif, block_index, entry_idx).
- **Corpus**: `pcg_install\Data\Models\Models.bnt` (SHA256
  c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0), 5,596 NIF payloads,
  parsed with the frozen R61 reader (10/10 SHA pins verified in-driver BEFORE any parse;
  READ-ONLY, never modified). Parse closure must be 5,596/5,596 (HARD STOP otherwise).
- **G-CENSUS (reproduction gate)**: the driver re-derives, from the pinned corpus bytes,
  every entry (block_index, entry_idx, name, f1, f2, ref, anim_flag, frame_index,
  bnt2_id, version, grammar) — v10 from the frozen parser's `ark_tex_textures` fields,
  v4 by the R32/K1-validated raw decode — and requires row-for-row equality with the
  pinned K1 table, plus per-file entry-count equality and the 24,474/34 resolved split
  from the table. ANY mismatch = HARD STOP (exit 3, evidence written, no results).

## M2. Name-part extraction (frozen)

For entry name `name`: if "_" occurs, `mesh_part, slot_suffix = name.rsplit("_", 1)`;
else `mesh_part = name`, `slot_suffix = ""` (reason NO_UNDERSCORE). This is the
ITER-32/K1 split convention (last underscore). Calibration: all 24,508 names contain
"_" (K1/R32 convention exceptions: 0 expected).

## M3. Own-file mesh-name universe (frozen)

Per file, from the frozen R61 parser blocks:
- **U_exposed(file)** = { non-empty `fields["name"]` of every NiTriShape block } ∪
  { non-empty `fields["name"]` of every NiMaterialProperty block } — exactly the
  mesh/material names the parser exposes.
- **Colon-bridge twin (OBSERVED same-name spelling layer)**: `bridge(u) = u` with its
  LAST ":" replaced by "_" iff the substring after that last ":" is one-or-more digits,
  else `u` unchanged. Justification (OBSERVED, calibration probe 3 on the full corpus):
  20,833/21,914 non-empty NiTriShape names end in ":<digits>" (the 3ds Max
  multi-material export spelling, e.g. "CISTERN:4"), while ArkTexture entry mesh-parts
  spell the same identifier with "_" (e.g. "CISTERN_4"); exact-only membership resolves
  1,103/24,508 vs 19,705/24,508 with the bridge. The bridge adds NO fuzzy matching —
  only the observed dual spelling of the same exposed name.
- **U_f(file) = U_exposed(file) ∪ { bridge(u) : u ∈ U_exposed(file) }** — the frozen
  mesh-name set used by the census. Universe contents are shipped per file
  (01_RAW/FILE_UNIVERSES.jsonl).
- Supplementary OBSERVED universe fields (NOT part of the frozen predicate): the
  NiNode-name set per file (for a supplementary own-file resolution flag only).

## M4. The anchor predicate (EXPLICIT, frozen)

For each of the 24,508 entries:

- **Component (a) — own-file mesh-part resolution**:
  `own_file_resolution = (mesh_part ∈ U_f(own file))` — exact string equality.
  Per record also `resolution_mode ∈ {exact, bridge, none}`: "exact" iff
  mesh_part ∈ U_exposed(own file); "bridge" iff resolved only via a bridge twin;
  "none" otherwise.
- **Component (b) — slot-suffix consistency**:
  `slot_consistency = (K1 table `slot` column value == extracted slot_suffix)` — the
  pinned entry table's slot field vs this run's independent M2 extraction (direct string
  equality; zero new format-field meanings; the K1 slot column is the audited 40/40
  slot-join field).
- **anchored(entry) = own_file_resolution AND slot_consistency.**

NO PASS/FAIL is attached to any anchor fraction — this is a MEASUREMENT; the numbers,
their exact binomial 95% CIs and the OBSERVED labels are the output.

**Supplementary OBSERVED census (NOT part of the frozen predicate, recorded per record
and reported separately, era-labelled, ITER-32-confirmed mapping cited, no semantic
claims):** `f1_enum_match = (f1 == enum[slot_suffix])` with the ITER-32 enum
BASE=0, DARK=1, DETAIL=2, GLOSS=3, GLOW=4, BUMP=5, DECAL0=6, ENVIRONMENT=9,
ANIMn=11 (n=0..31); entries whose suffix is not in the enum vocabulary are excluded
from the supplementary census with an explicit denominator. The ITER-32-documented
172 ANIM exceptions (f1=0 ×142 / f1=4 ×30) are expected and reported as-is.

## M5. The seeded cross-file negative control (frozen)

`rng = random.Random(20260906)` (single instance, fixed order of consumption):
1. `sample_idx = rng.sample(range(24508), 10000)` — a simple random sample of 10,000
   entries WITHOUT replacement (deterministic; trial order = sample order).
2. For each sampled entry, in sample order: `other_file = rng.choice(sorted list of
   entry-bearing files EXCLUDING the entry's own file)` — uniform over the other
   entry-bearing files (3,766 alternatives per trial; the self-pairing case is excluded
   by construction and asserted at trial time).
3. Re-evaluate the M4 anchor predicate with the OTHER file's U_f in place of the own
   file's: `anchored_nc = (mesh_part ∈ U_f(other_file)) AND slot_consistency(entry)`.
   The slot-suffix consistency component is the entry's own (unchanged).
4. Denominators (explicit everywhere): trials = 10,000; entry population = 24,508;
   entry-bearing files = 3,767. Output: NC anchored rate + exact binomial 95% CI;
   NC other-file resolution rate + CI; per-trial records in 01_RAW/NC_TRIALS.jsonl
   (entry key, own file, other file, mesh part, other-file resolution, slot
   consistency, anchored, reason, trial index).
5. Determinism proof: the driver re-derives the full sampling/pairing sequence with a
   fresh `random.Random(20260906)` and requires identity (SELF_AUDIT).

## M6. Sub-censuses (frozen list; every fraction with denominator + exact binomial 95% CI)

1. **per-slot** — the 40-slot canon (the K1 table slot column vocabulary;
   BASE/GLOSS/DARK/ENVIRONMENT/GLOW/BUMP/DETAIL/DECAL0/ANIM0..31).
2. **per-grammar** — v10 / v4.
3. **per-version** — 10.1.0.0 / 4.1.0.12 / 4.0.0.2.
4. **per-class** — (i) K1 resolved/dangling; (ii) resolution_mode exact/bridge/none.
5. **supplementary** — f1_enum_match (global + per-slot); NiNode-universe resolution
   flag (global); both clearly labeled SUPPLEMENTARY_OBSERVED, outside the frozen
   predicate.

Each sub-census reports: population n, anchored count, own-file resolution count,
slot-consistency count, anchored fraction + CI, component fractions + CIs.

## M7. Exact binomial 95% CIs (frozen)

Clopper-Pearson exact: lower = BetaQuantile(0.025; k, n-k+1) (0 if k=0);
upper = BetaQuantile(0.975; k+1, n-k) (1 if k=n); implemented via the regularized
incomplete beta function (continued fraction) + bisection (tol 1e-13). In-driver
validation (SELF_AUDIT): closed forms for k=0/k=n at n=10 and n=24,508; definitional
brute-force tail-sum comparison on 10 (k,n) pairs including edge cases
(k=0, k=1, k=n-1, k=n, mid-range, run-scale) — worst |delta| must be < 1e-9.

## M8. The EIGHT negative fixtures (the standard list, adapted to this run's machinery; all must FAIL CLOSED)

| # | Name | Synthetic input | Expected explicit verdict |
|---|---|---|---|
| 1 | zero successes both sides | population with 0 anchored own and 0 NC hits | DEGENERATE_POPULATION (explicit non-pass; never silent success) |
| 2 | empty population | empty entry population | EMPTY_POPULATION |
| 3 | duplicate present in both groups | duplicate entry key within the population | DUPLICATE_ENTRY_KEY |
| 4 | unequal denominators | sub-census with declared denominator ≠ record count | DENOMINATOR_MISMATCH |
| 5 | a corrupted record | record missing the `name` field | CORRUPTED_RECORD |
| 6 | NC self-pairing trial | NC trial whose other_file == own_file | NC_SELF_PAIRING_REJECTED |
| 7 | a malformed manifest row | manifest row with unquoted comma (4+ fields) | MALFORMED_MANIFEST_ROW |
| 8 | a missing input file | nonexistent input path | MISSING_INPUT_FILE |

All eight are SYNTHETIC (no game data); each must produce its explicit non-pass/error
class; G-EXEC PASS requires 8/8 fail-closed.

## M9. Discipline (frozen)

- Zero size-derived validation numbers: no gate/census validation number derives from
  any file/payload size; an AST self-scan of the gate/validation functions must
  report zero len()/getsize()/stat()-derived validation assignments.
- Read-only originals (Models.bnt, K1 table, R61 source, contract) — re-hashed
  in-driver before and after; zero payload bytes written.
- All outputs inside this run dir only; every JSON carries the standing sentence and
  era label; every number carries its denominator.
- artifact_index.csv per MANIFEST_SCHEMA_SPEC.md (ordinary rows + external-source
  section; self-validation gate with the 6 spec negative tests; documented
  self-exclusions: the manifest's own row + 05_ANALYSIS/MANIFEST_VALIDATION.json —
  circular, precedent L12).
