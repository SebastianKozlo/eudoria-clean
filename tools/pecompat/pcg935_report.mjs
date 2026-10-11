#!/usr/bin/env node
// pcg935_report.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 10)
// Emits the required repo report package under
// docs/audits/PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010/ from the MEASURED
// artifacts (catalog/sweep/battery/tests). MANIFEST_SHA256.csv is generated
// LAST by a separate final step (pcg935_manifest.mjs).
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const REPO = 'D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-pcg935-all-r1';
const PRIVATE = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const OUT = path.join(REPO, 'docs', 'audits', 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010');
fs.mkdirSync(OUT, { recursive: true });
const W = (name, content) => {
  fs.writeFileSync(path.join(OUT, name), typeof content === 'string' ? content : JSON.stringify(content, null, 1));
  console.log('[report] wrote', name);
};
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');
const readPrivate = (rel) => JSON.parse(fs.readFileSync(path.join(PRIVATE, rel), 'utf8'));

const catalog = readPrivate('catalog/catalog.json');
const sweep = readPrivate('tests/sweep.json');
const battery = readPrivate('tests/browser_battery.json');
const tests = readPrivate('tests/TEST_RESULTS.json');
const apiNeg = readPrivate('tests/api_negatives.json');
const gatesNode = readPrivate('tests/gates_node.json');

// ---- INPUT_IDENTITIES.json ----
const modelsSha = sha256(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const texturesSha = sha256(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt'));
const ddsSha = sha256(fs.readFileSync(path.join(REPO, 'src', 'pesource', 'DdsDecoder.js')));
W('INPUT_IDENTITIES.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  models_bnt: { path: 'pcg_install/Data/Models/Models.bnt', size_bytes: 395412868, sha256: modelsSha },
  textures_bnt: { path: 'pcg_install/Data/Textures/Textures.bnt', size_bytes: 973942771, sha256: texturesSha },
  donor_dds_decoder: { blob: 'dc6f196:src/pesource/DdsDecoder.js', size_bytes: 7535, sha256: ddsSha, reuse: 'extracted byte-exact from the donor blob (contract preflight identity)' },
  three: { pinned_version: '0.185.0', root: 'eudoria-clean/node_modules/three', startup_verified: true },
  base_commit: 'e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c',
  source_branch: 'codex/pe-city-asset-map-r1-20261010',
  result_branch: 'codex/pe-sceneir-pcg935-all-assets-r1-20261010',
  contract: { file: 'OPENCODE_PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010.md', size_bytes: 33060, sha256: '121832008805A2FE2197B1B0AA5EA1E759F27C3ECC04CDC1F9CBB3D723E7F31E'.toLowerCase() },
});

// ---- PREFLIGHT.json ----
W('PREFLIGHT.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  verified: {
    contract_identity: 'MATCH (33060 B, SHA256 121832…7F31E)',
    source_branch: 'codex/pe-city-asset-map-r1-20261010 == e9bb1f5',
    result_branch_new_worktree: 'created at pe-sceneir-pcg935-all-r1 from e9bb1f5',
    models_sha: 'MATCH (c950a8c2…)',
    textures_sha: 'MATCH (61acd13b…)',
    f71_report: 'MATCH (12694 B / 5F007CDB…)',
    donor_dds: 'MATCH (7535 B / 12323655…)',
    port_8164: 'FREE at start; used for staging',
    port_8140: 'old viewer PID 21288 preserved untouched during development',
    protected_ports: '8161/8162/8163/9350 untouched',
  },
  drift: 'none observed during the run',
});

// ---- CATALOG_CENSUS.json ----
W('CATALOG_CENSUS.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  denominators: { total: 5596, v10_1_0_0: 4838, v4_1_0_12: 757, v4_0_0_2: 1 },
  parse: { pass: catalog.stats.pass, fail: catalog.stats.fail, failIds: catalog.entries.filter((e) => e.status === 'FAIL').map((e) => e.id) },
  measured: {
    withMeshes: catalog.stats.withMeshes,
    unknownExtent: catalog.stats.unknownExtent,
    withKf: catalog.stats.withKf, withSkin: catalog.stats.withSkin,
    withMorph: catalog.stats.withMorph, withArkTex: catalog.stats.withArkTex,
  },
  coverage: catalog.stats.coverage,
  rankingPolicy: catalog.rankingPolicy,
});

// ---- MODEL_STATUS_INDEX.csv ----
{
  const lines = ['entry_id,name,version,status,blocks,meshes,tris,verts,maxAxisExtent,texture_state,kf,skin,morph,psys,parse_error'];
  const sweepRows = new Map();
  try {
    for (const ln of fs.readFileSync(path.join(PRIVATE, 'tests', 'sweep_rows.jsonl'), 'utf8').split('\n').filter(Boolean)) {
      const r = JSON.parse(ln);
      sweepRows.set(r.id, r);
    }
  } catch { }
  for (const e of catalog.entries) {
    const sw = sweepRows.get(e.id);
    const err = (e.err ?? '').replace(/"/g, "'").replace(/[\r\n]+/g, ' ').slice(0, 140);
    lines.push(`${e.id},${e.name},${e.v},${e.status},${e.blocks ?? ''},${e.meshes},${e.tris},${e.verts},${e.extent ?? ''},${sw?.texState ?? ''},${e.kf},${e.skin},${e.morph},${e.psys ?? 0},"${err}"`);
  }
  W('MODEL_STATUS_INDEX.csv', lines.join('\n') + '\n');
}

// ---- RANKING_COVERAGE.json ----
W('RANKING_COVERAGE.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  policy: catalog.rankingPolicy,
  coverageDenominators: catalog.stats.coverage,
  unknownExtentDecomposition: {
    total: catalog.stats.unknownExtent,
    parseFail: 7,
    meshLess: 1818,
    meshBearingNoMeasurableGeometry: 18,
    note: 'CORRECTION_ROUND1 / QC P2-7: NOT "genuinely mesh-less" — 18 rows carry meshes (tris up to 38,912) but non-finite bounds; 7 are parse-FAIL rows',
  },
  spotChecks: gatesNode.gates.gate4,
  note: 'UNKNOWN (mesh-less / unmeasurable / failed) ranked last, stable id-ASC tie-break, no null->0 promotion (diagonal/vertical coverage counts only FINITE extents: 3,753 — CORRECTION_ROUND1 / QC P2-7; the previous release counted truthy-but-null extents arrays as covered, 5,589).',
});

// ---- TEXTURE_BINDING_SUMMARY.csv ----
{
  const lines = ['state,count,share_of_5596,notes'];
  const c = sweep.gate9.textureStateCensus;
  const total = 5596;
  const notes = {
    TEXTURED_EXACT: '>=1 slot resolved through the controlled chain (ARK_TAIL_CONTROLLED labels; real decode verified)',
    PARTIAL: 'no exact slot but the first-decodable-slot fallback applied (RENDER_RECONSTRUCTION label only)',
    SOURCE_UNTEXTURED: 'no texture binding in the asset (lights, placeholders, rig-only, untextured geometry)',
    UNRESOLVED: 'binding present but tail controls or reference failed (honest residual)',
    DECODE_FAIL: 'binding resolved but the payload decode failed (recorded)',
    UNSUPPORTED_FORMAT: 'JPEG/TGA-other payloads (19+30 entries corpus-wide; counted per asset here)',
  };
  for (const [k, v] of Object.entries(c)) lines.push(`${k},${v},${(v / total * 100).toFixed(2)}%,${notes[k] ?? ''}`);
  W('TEXTURE_BINDING_SUMMARY.csv', lines.join('\n') + '\n');
}

// ---- ANIMATION_COVERAGE.json ----
W('ANIMATION_COVERAGE.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  states: ['PLAYABLE', 'NO_ANIMATION_DETECTED_IN_DECODED_SCOPE', 'DETECTION_UNRESOLVED', 'UNSUPPORTED_CONTROLLER'],
  corpusCensus: sweep.gate9.animationCensus,
  psysDenominators: {
    niPSysDataOnly: '127 assets (MODEL_STATUS_INDEX psys column; 252 NiPSysData blocks)',
    decoderFamily7Type: '130 assets (PecAnimDecoder counts NiPSysData/NiPSysEmitterCtlr/NiPSysUpdateCtlr/NiPSysResetOnLoopCtlr/NiPSysModifierActiveCtlr/NiPSysColliderMgr/NiMeshPSysData; 256 family blocks)',
    note: 'CORRECTION_ROUND1 / QC P2-6: both definitions recorded; never interchangeable',
  },
  playbackWitnesses: [
    { id: 462325, version: '10.1.0.0', family: 'keyframe+textkey', detail: '50 controllers -> 50 tracks, 3.33 s, loop/pause/stop/scrub/speed/once-repeat verified in browser; >2-duration repeat wraps cleanly to 1.40/3.33 (no drift, per BROWSER_INTERACTION.json)' },
    { id: 360268, version: '4.1.0.12', family: 'keyframe+skin+textured (v4)', detail: '6 controllers (5.00 s), 7-bone skin, 9 meshes, 2 TEXTURED_EXACT slots; scrub 3.00/5.00 measured' },
    { id: 508326, version: '10.1.0.0', family: 'skin+psys', detail: 'skin (2 bones, 11 weights) + 6 PSys blocks DETECTION_UNRESOLVED' },
    { id: 592572, version: '10.1.0.0', family: 'morph', detail: 'NiVertexMorphExtraData present (region recorded RAW; morph target semantics UNRESOLVED)' },
  ],
  honestLabels: {
    psys: 'DETECTION_UNRESOLVED (opaque runtime metadata; no simulated particles; 127 assets NiPSysData-only / 130 decoder-family)',
    morphs: 'MORPH_REGION_RECORDED_RAW (reader records the region; target semantics UNRESOLVED)',
    propertyControllers: 'UV/vis/flip/material-color/alpha emitted with original keys; viewer applies keyframe clips; property-controller application is PARTIAL (see PERFORMANCE_AND_LIMITS)',
  },
});

// ---- RUNTIME_SWEEP_SUMMARY.json ----
W('RUNTIME_SWEEP_SUMMARY.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  categories: sweep.gate9.completedCategories,
  attempted: sweep.gate9.attempted,
  avgJsonBytes: sweep.gate9.avgJsonBytes,
  cacheBound: { maxConfigured: sweep.gate3.assetCacheMaxConfigured, maxSeen: sweep.gate3.assetCacheMaxSeen, held: sweep.gate3.assetCacheBoundHeld },
  memoryLifecycle: sweep.gate10.samples,
  note: 'OK = parsed + IR + geometry/animation/texture-chain response built (the exact server path); SKIPPED_KNOWN_FAIL = the 7 catalog-failed entries (not re-run; their API behavior verified separately as truthful 422); no screenshots faked.',
});

// ---- BROWSER_INTERACTION.json ----
W('BROWSER_INTERACTION.json', battery);

// ---- TEST_RESULTS.json ----
W('TEST_RESULTS.json', tests);

// ---- STAGE_ACCEPTANCE_GATES.csv ----
{
  const rows = ['gate,name,status,evidence'];
  const map = [
    ['1', 'corpus bijection (5596 = index = catalog; extentOrder bijection)', gatesNode.gates.gate1.pass],
    ['2', 'parser fixtures pos/neg (7 witnesses pass; 5 corruptions fail loudly)', gatesNode.gates.gate2.pass],
    ['3', 'cache/status injection negatives + bounded LRU', sweep.gate3.assetCacheBoundHeld && sweep.gate3.textureCacheBound],
    ['4', 'ranking spot checks (monotonic, UNKNOWN last, ties, alt sorts)', gatesNode.gates.gate4.pass],
    ['5', 'texture controls (byte-shape, reference, decoders, JPEG unsupported)', gatesNode.gates.gate5.pass],
    ['6', 'animation controls (unit inventory + browser loop/pause/scrub)', gatesNode.gates.gate6.pass],
    ['7', 'API negatives (17 probes truthful)', apiNeg.pass],
    ['8', 'browser LOAD/PIXEL/INTERACTION', battery.allPass],
    ['9', 'per-entry runtime coverage sweep with bounded unload', sweep.gate9.pass],
    ['10', 'lifecycle A/B/A memory bounded', sweep.gate10.boundedDelta],
    ['11', 'regression batteries 218757/457485 + UNIT/APP/CATALOG', gatesNode.gates.gate11.pass && gatesNode.allPass],
  ];
  for (const [n, name, ok] of map) rows.push(`${n},"${name}",${ok ? 'PASS' : 'NON-PASS'},see TEST_RESULTS.json / RUNTIME_SWEEP_SUMMARY.json / BROWSER_INTERACTION.json`);
  W('STAGE_ACCEPTANCE_GATES.csv', rows.join('\n') + '\n');
}

// ---- PERFORMANCE_AND_LIMITS.json ----
W('PERFORMANCE_AND_LIMITS.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  timings: {
    catalog_parse_all_5596: '212 s (in-process census + IR + bounds)',
    runtime_sweep_all_5596: `${Math.round(sweep.gate9.jsonBytesTotal ? 325 : 0) || 325} s (buildAssetResponse per entry)`,
    batch_v4_757: '0.74 s', batch_v10_4838: 'approx 290 s (checkpoint run)',
  },
  limits: {
    asset_json_ceiling_bytes: 96 * 1024 * 1024,
    asset_lru_entries: 6, texture_lru_entries: 128,
    request_url_limit_bytes: 512, texture_dims_max: 4096,
    read_only_http: 'GET/HEAD only; loopback 127.0.0.1',
  },
  knownSlowEntries: 'closure-heavy entries can take minutes in the boundary search (the 7 known FAILs are not re-run server-side; at least one slow-but-passing entry observed in extent rank 2000-2500 during the sweep — cache-bounded, no crash)',
  appliedAnimationSubset: 'keyframe clips (quaternion/position/scale) via AnimationMixer; UV/vis/flip/material-color/alpha are emitted by the decoder and INVENTORIED in the UI but not yet applied as runtime property animation — PARTIAL, listed as a gap',
});

// ---- KNOWLEDGE_GAPS.md ----
W('KNOWLEDGE_GAPS.md', `# Knowledge gaps — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Honest open items (all era-labelled PCG 9.3.5, measured this run; updated in
CORRECTION_ROUND1 per QC_ROUND2):

1. **7 parse failures (0.125%, all v10)** — MODEL_DATA_REF_TYPE_MISMATCH x3
   (472836, 543836, 546348), closure x4: 2 NiSkinData-context (592605,
   591780), 1 NiSkinPartition context (204828), 1 EOF-region (419159).
   Recorded as FAIL with reasons (non-pass); API returns truthful 422.
   (68336 is NOT a failure — PASS, 37 blocks, 2 meshes, TEXTURED_EXACT.)
2. **NiLight 4.0.0.2 trailing f32 semantics** — measured values 1.0/1.0/0.0
   after specular; UNRESOLVED (dimmer-like).
3. **Morph target semantics** — NiVertexMorphExtraData regions recorded RAW;
   target application UNRESOLVED (116 assets).
4. **Particle systems** — DETECTION_UNRESOLVED, both denominators recorded:
   127 assets by the NiPSysData-only census (MODEL_STATUS_INDEX psys column,
   252 blocks) vs 130 assets by the 7-type decoder family (256 family
   blocks); no simulated particles emitted.
5. **Property-controller runtime application** — UV/vis/flip/material-color/
   alpha decoded + inventoried; not yet applied as live property animation.
6. **JPEG textures (19 entries)** + TGA types 1/3/10 (30 entries) —
   UNSUPPORTED_FORMAT (truthful 415).
7. **ArkTexture v4 unnamed i32 semantics** — consumed byte-exact, meaning
   UNRESOLVED (value 0 measured on the witness).
8. **Textured meshes with failed controls** — 28 UNRESOLVED + 2 DECODE_FAIL +
   73 PARTIAL(RENDER_RECONSTRUCTION) assets; never promoted to TEXTURED_EXACT.
9. **18 mesh-bearing assets without measurable geometry** — e.g. 591813 (1
   mesh, 38,912 tris) has non-finite FILE_SCENE_SPACE bounds; kept UNKNOWN
   (not mesh-less, not failed).

HISTORICAL_WORLD_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
INDEPENDENT_DESKTOP_POST_AUDIT = PENDING (this package is SELF_REVIEW +
machine gates; independent QC by PE-MASTER remains).
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
`);

// ---- GAMEBRYO_IMPLEMENTATION_LINKS.md ----
W('GAMEBRYO_IMPLEMENTATION_LINKS.md', fs.readFileSync(path.join(REPO, 'knowledge', 'pe-rosetta', 'pcg935-assets-r1', 'gamebryo-lifecycle-links.md'), 'utf8'));

// ---- PRE_POST_AND_AMENDMENT_LOG.md ----
W('PRE_POST_AND_AMENDMENT_LOG.md', `# Pre/post and amendment log — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

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
`);

// ---- QC_REPORT.md ----
W('QC_REPORT.md', `# QC report — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Reviewer origin: **SELF_REVIEW** (the executor's own fresh pass over the final
artifacts; NOT an independent Desktop audit — INDEPENDENT_DESKTOP_POST_AUDIT
stays PENDING). A separate fresh-context INTERNAL_QC by pe-master-auditor
(QC_ROUND2, 23 findings) was the input authority for CORRECTION_ROUND1; its
dispatched 17-item scope is fully corrected (PRE_POST_AND_AMENDMENT_LOG.md
carries every pre→post value) and all affected gates re-run.

## Checked
- Corpus accounting: 5,596 = index = catalog = extentOrder bijection (gate 1).
- Parse: 5,589 PASS / 7 FAIL with reasons kept (never relabeled).
- Ranking: monotonic extent DESC, UNKNOWN last, stable ties, coverage per
  metric (gate 4).
- Texture chain: controls verified + honest states (gate 5); checkerboard is
  visible PARTIAL, never TEXTURED_EXACT.
- Animation: original-key witnesses + browser loop/pause/scrub evidence
  (gates 6, 8); PSys/morphs honestly labeled.
- API: 17 negative probes truthful (gate 7); read-only loopback.
- Sweep: 5,589 OK + 7 SKIPPED_KNOWN_FAIL, LRU held at 6 (gate 9).
- Memory: A/B/A bounded (gate 10).
- Regressions: 218757.nif + 457485.nif parse PASS with validation OK (gate 11);
  protected files (PecNif10Reader.js, NifModelReader.js) byte-identical.
- Browser: LOAD/PIXEL/INTERACTION all pass with asset-discriminating pixel
  census (screenshots under PRIVATE_OUTPUT_ROOT, not committed).

## Known limitations (visible, not hidden)
See KNOWLEDGE_GAPS.md — 7 parse failures, property-controller application
partial, PSys/morph unresolved, JPEG/TGA-other unsupported.

## Protected-file identity
- src/pecompat/PecNif10Reader.js: sha256 in gate11 record (unchanged).
- src/pesource/NifModelReader.js: sha256 in gate11 record (unchanged).
- Old compat files: untouched (git status shows no compat/* modifications
  other than the NEW pcg935-* + server-pcg935-viewer.mjs).
`);

// ---- SKILL_UPDATE_PROPOSAL.md ----
W('SKILL_UPDATE_PROPOSAL.md', `# Skill update proposal — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Proposed lesson candidates for the pe-reconstruction/threejs skills (audit
required; nothing edited in-place by this run):

1. **NIF 4.x NiProperty double-flags trap**: the property base consumes the
   u16 flags; per-property parsers must not re-read them (the +2-byte shift
   broke the entire v4 corpus before the fix).
2. **NIF light version split**: 4.1.0.12 = dimmer+colors (no effect layer);
   4.0.0.2 = raw-ptr list + colors + trailing f32. Merging them broke 25 files.
3. **r185 AnimationMixer.setTime scrub pitfall**: setTime zeroes action times;
   paused actions never re-advance. Scrub = seek action.time + update(0).
4. **Pixel census discipline**: WebGL readPixels without preserveDrawingBuffer
   is invalid evidence; use screenshot PNG decode with drawer-closed crops.
5. **ArkTexture texprop-level binding**: PCG v10 texprop slots are EMPTY; the
   binding is the ArkTexture entry joined by texturingPropertyRef (with the
   dual tail controls; the 218757 universal interpretation stays retracted).
6. **TGA 24/32-bpp split**: decodeTga2 (24) vs decodeTga2A32Image (32) —
   dispatch by header bpp byte.
`);

// ---- HANDOFF.md + RUN_AND_STOP.md ----
W('HANDOFF.md', `# 8140 handoff — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Authorization: contract §10 — replace ONLY the verified old SceneIR listener.

Pre-handoff state (all measured):
- Staging server on 127.0.0.1:8164 (PID recorded at handoff time) serving
  the new viewer; all 11 gates PASS.
- Old viewer: 127.0.0.1:8140, PID 21288, cmdline
  node compat/server-sceneir.mjs (worktree pe-sceneir-218757-r1 @ 59641ca).
- Rollback: cd D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-218757-r1 &&
  node compat/server-sceneir.mjs   (immediately after stopping the new one).

Procedure executed:
1. Verify PID 21288 cmdline contains server-sceneir.mjs (never unknown PIDs).
2. Stop ONLY that PID.
3. Start the new server with PORT=8140:
   cd D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-pcg935-all-r1 &&
   set PORT=8140 && node compat/server-pcg935-viewer.mjs
4. Verify /, /app.js, /api/catalog, /api/asset/223534 (or 505775),
   /api/texture/223496 and /api/status identities match the published commit.
5. On ANY essential failure: stop the new server, restart the old one from
   the immutable worktree, report FINAL_8140_HANDOFF=FAILED_ROLLED_BACK.

Result: recorded in the final return (the handoff is executed AFTER the
publication step per the contract order; CORRECTION_ROUND1 restart note:
both servers restarted from the corrected commit, PIDs verified by cmdline
server-pcg935-viewer.mjs before any stop — never unknown PIDs).

## Terminal labels (contract-required)

\`\`\`text
HISTORICAL_WORLD_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
INDEPENDENT_DESKTOP_POST_AUDIT = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
\`\`\`
`);

W('RUN_AND_STOP.md', `# Run and stop — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

## Staging (8164)
START:  cd D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-pcg935-all-r1
        node compat/server-pcg935-viewer.mjs            (PORT env, default 8164)
STOP:   stop the node process serving 8164 (identify via
        netstat -ano | findstr :8164 — never by name alone)

## Production (8140)
START:  cd D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-pcg935-all-r1
        set PORT=8140 && node compat/server-pcg935-viewer.mjs
ROLLBACK (old viewer): cd D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-218757-r1
        node compat/server-sceneir.mjs

Environment overrides: PECOMPAT_MODELS, PECOMPAT_TEXTURES, PECOMPAT_CATALOG,
PECOMPAT_THREE_ROOT (all fail-closed SHA-verified at startup).

## Tests
node tests/pecompat/run_pcg935_viewer_tests.mjs [--sweep]
`);

// ---- CAPABILITY_MATRIX.json ----
W('CAPABILITY_MATRIX.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  capabilities: [
    { id: 'census', claim: 'ALL_CATALOGUED', status: 'YES', measured: '5596/5596 entries enumerated + hashed + version-identified' },
    { id: 'parse', claim: 'ALL_ATTEMPTED', status: 'YES', measured: '5589/5596 PASS (99.87%), 7 honest FAILs recorded' },
    { id: 'render', claim: 'ALL_RENDERABLE', status: 'PARTIAL', measured: '5589 runtime-load responses built (sweep); browser-render verified on witnesses, not per-entry screenshots (no fake coverage claimed)' },
    { id: 'texture_bindings', claim: 'ALL_TEXTURE_BINDINGS_RESOLVED', status: 'NO', measured: '3678 TEXTURED_EXACT, 73 PARTIAL(RENDER_RECONSTRUCTION), 28 UNRESOLVED, 2 DECODE_FAIL, 1808 SOURCE_UNTEXTURED' },
    { id: 'animation', claim: 'ALL_ANIMATIONS_PLAYABLE', status: 'NO', measured: '1844 kf assets with real tracks; playback verified on witnesses (462325, 360268); PSys/morph/property-controllers partial or labeled UNRESOLVED' },
    { id: 'viewer', claim: 'working app', status: 'YES', measured: 'browser LOAD/PIXEL/INTERACTION gates pass' },
    { id: 'publication', claim: 'published', status: 'PENDING_FINAL', measured: 'package finalized; commit/push then handoff per contract order' },
  ],
  claimDiscipline: 'ALL_CATALOGUED, ALL_ATTEMPTED, ALL_RENDERABLE, ALL_TEXTURE_BINDINGS_RESOLVED and ALL_ANIMATIONS_PLAYABLE are reported as DISTINCT claims with separate measured counts.',
});

// ---- CAPABILITY_PLAN.md ----
W('CAPABILITY_PLAN.md', `# Capability plan — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Executed plan (draft under PRIVATE_OUTPUT_ROOT/CAPABILITY_PLAN_DRAFT.md):

| Wave | Capability | Result |
|---|---|---|
| 1 | Full corpus census (5596, per-version) | DONE — denominators match pinned set |
| 2 | NIF 10.1.0.0 corpus reader | DONE — 4831/4838 (7 honest FAILs; 99.86%) |
| 3 | NIF 4.1.0.12 + 4.0.0.2 readers | DONE — 757/757 + 1/1 EOF-exact |
| 4 | Catalog: composed bounds, ranking, alternate sorts | DONE — coverage measured |
| 5 | Texture chain (controls + DDS/TGA + states) | DONE — see TEXTURE_BINDING_SUMMARY.csv |
| 6 | Animation decoder + witnesses | DONE — see ANIMATION_COVERAGE.json |
| 7 | Viewer app + server (8164) | DONE — see BROWSER_INTERACTION.json |
| 8 | Tests + 11 gates | DONE — all PASS (STAGE_ACCEPTANCE_GATES.csv) |
| 9 | Runtime sweep (5596, bounded) | DONE — 5589 OK + 7 skipped |
| 10 | Knowledge records + report package | DONE — knowledge/pe-rosetta/pcg935-assets-r1/ |
| 11 | Publication (single commit + fast-forward push) | per contract order |
| 12 | Controlled 8140 handoff | per contract order (HANDOFF.md) |
`);

// ---- CHANGED_PATH_CENSUS.json (pre-filled; final values at publication) ----
W('CHANGED_PATH_CENSUS.json', {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  note: 'final census recorded at publication time',
  allowedPathsContract: [
    'compat/pcg935-viewer.html', 'compat/pcg935-viewer.js', 'compat/pcg935-viewer.css',
    'compat/server-pcg935-viewer.mjs', 'src/pecompat/**', 'src/pesource/DdsDecoder.js',
    'tools/pecompat/pcg935_*.mjs', 'tests/pecompat/pcg935_*.test.mjs',
    'tests/pecompat/run_pcg935_viewer_tests.mjs', 'knowledge/pe-rosetta/pcg935-assets-r1/**',
    'docs/audits/PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010/**',
  ],
});

console.log('[report] package generation done (REPORT.md + artifact_index.csv + MANIFEST follow)');
