# Pre/post and amendment log — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

## Preflight (pre)
- Contract identity verified (33060 B / 12183200…7F31E).
- Worktree pe-sceneir-pcg935-all-r1 created from e9bb1f5; branch
  codex/pe-sceneir-pcg935-all-assets-r1-20261010.
- Inputs SHA-verified (Models c950a8c2…, Textures 61acd13b…).
- Donor DdsDecoder.js extracted byte-exact (7535 B / 12323655…).
- 8164 free; 8140 (PID 21288) + 8161/8162/8163/9350 untouched throughout.

## Execution (in-run amendments, all recorded)
1. v4 reader layout corrections (double-flags fix, ArkTexture i32,
   4.0.0.2 gates, lights version-split) — measured on-corpus, 757/757+1/1.
2. Mesh/tri counting fix for v10 (geometry lives on the dataRef target).
3. Texture chain v10 extension (texprop-level ArkTexture binding) after the
   probe showed empty texprop slots in the PCG corpus.
4. TGA 24-bpp dispatch added (decodeTga2) after the A32-only call failed.
5. Scrub bug found in browser testing (r185 mixer.setTime zeroing) — fixed
   and re-verified (3.00/5.00).
6. Sweep made resumable + SKIPPED_KNOWN_FAIL category after a crash near the
   rank-2000 slow entry; end-of-run stale-reference bug fixed; re-run clean.
7. Camera-up/space conventions follow the old viewer (default Y-up, raw
   FILE_SCENE_SPACE rendering, AABB fit on updateMatrixWorld(true)).

## Post (first publication)
- All 11 gates PASS (STAGE_ACCEPTANCE_GATES.csv; TEST_RESULTS.json).
- Commit 0940a89 pushed (fast-forward); 8140 handoff COMPLETED_VERIFIED.

## CORRECTION_ROUND1 (QC_ROUND2 findings; every pre→post below)

Input authority: QC_ROUND2/QC_FINDINGS.md (23 findings; this round corrects
the dispatched 17-item scope). Pre values are the 0940a89 publication.

- **P1-1 v10 PASS count**: REPORT.md/corpus-coverage.md/CAPABILITY_PLAN.md
  "4,832/4,838 (99.88%)" → **"4,831/4,838 (99.86%)"** (4,838−7; the
  aggregate 5,589/5,596 = 99.87% was already correct).
- **P1-2 phantom failure id**: failure lists in KNOWLEDGE_GAPS.md /
  corpus-coverage.md / REPORT.md "MODEL_DATA_REF ×4 (…, 68336) + closure ×4"
  (8 instances over 7 fails) → **MISMATCH ×3 (472836, 543836, 546348) +
  closure ×4 (592605, 591780 NiSkinData; 204828 NiSkinPartition; 419159
  EOF)**. 68336 is a PASS asset (37 blocks, 2 meshes, TEXTURED_EXACT).
- **P1-3 gate-3 stub**: pcg935_sweep.mjs gate3.negativeEntryCached
  (hard-coded assetCacheValid:true, valid-id call, unused idsInCache) →
  **REAL injection negatives** through the actual buildAssetResponse path:
  missing-identity / wrong-entry-identity / wrong-era / wrong-payload-SHA
  cache entries each DROPPED with a counted reason
  (cache_dropped_missing_identity / _entry_identity_mismatch /
  _era_version_mismatch / _payload_sha_mismatch), wrong container SHA
  refused via the extracted verifyInputSha guard (throws, counted
  input_sha_mismatch; boot wraps into a fatal exit), negative-cache repeat
  re-serves the recorded reason, foreign id → null. Cache entries now store
  identity meta (entryName, version, payloadSha256, container).
- **P2-4 negative-cache degradation**: repeated GET on a fail-id returned
  422 with a Buffer.from(null) TypeError text instead of the parse reason
  → the route stores {failed, failStatus, failCode, failMessage} and
  re-serves the RECORDED denial; regression added to the API battery
  (GET /api/asset/592605 twice — second response asserts the recorded
  reason, no TypeError/Buffer.from text).
- **P2-7 ranking null→0**: rank tool + viewer diagonal/vertical treated
  truthy-but-null extents arrays as covered (Math.hypot(null,null,null)=0)
  → finite-extent gate added (all-finite check); diagonal/vertical coverage
  5,589 → **3,753** (= extent coverage); catalog.json regenerated; gate 4
  extended with the coverageConsistent assertion.
- **P2-8 contract labels**: HISTORICAL_WORLD_PLACEMENT=NOT_ESTABLISHED,
  WORLD_XYZ_RECOVERED=NO, CANONICAL_GATE_EFFECT=NONE,
  INDEPENDENT_DESKTOP_POST_AUDIT=PENDING, NEXT_EXPERIMENT_AUTHORIZED=NO,
  HARD_STOP=YES — added to REPORT.md + HANDOFF.md + KNOWLEDGE_GAPS.md
  terminal blocks and the viewer header comment.
- **P2-9 validator nested loop**: PecSceneIR.validateSceneGraph null-slot
  census was nested INSIDE the per-block loop (duplicate warnings up to N
  per block, O(N²)) → dedented to ONE top-level pass; verdicts unchanged
  (duplicate warnings never flipped ok); re-validated on the witness set.
- **P2-10 changed-path census**: 69 paths (missing MANIFEST_SHA256.csv) →
  **70 paths** after manifest staging (set-equals git diff base..HEAD).
- **P3-11 loop-drift value**: REPORT.md/animation-decoder.md/
  viewer-runtime-lessons.md "1.44/3.33" → **"1.40/3.33"** (= the recorded
  BROWSER_INTERACTION.json interaction.loopDrift.timeTextAfter2x).
- **MM psys definitions**: "130 assets" used without definition → both
  denominators recorded everywhere (127 assets NiPSysData-only census vs
  130 assets 7-type decoder family; 252 vs 256 blocks).
- **MM textkeys card count**: animation-decoder.md "textkeys 1038 blocks"
  → **"textkeys 1031 assets / 1039 blocks"** (re-derived from the catalog).
- **MM UNKNOWN descriptor**: "1,843 genuinely mesh-less (measured ZERO)"
  → **"1,843 UNKNOWN extent = 7 FAIL + 1,818 mesh-less + 18 mesh-bearing
  without measurable geometry"** (tris up to 38,912 in the 18).

Re-runs after corrections: gate 3 (real injections), gate 4 (coverage
consistency), API battery (repeat-fetch regression), node gate battery,
browser battery (viewer comparator change), sweep. Manifest regenerated
LAST. Second single-parent commit on the same branch (parent 0940a89).
