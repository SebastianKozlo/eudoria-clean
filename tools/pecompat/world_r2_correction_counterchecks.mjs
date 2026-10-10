#!/usr/bin/env node
// world_r2_correction_counterchecks.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010
// CORRECTION ROUND (PE-MASTER dispatch after INTERNAL_QC; finding [P1-2]):
//
//   The ORIGINAL run's WL-1 fix (latest-wins queue inside WorldVegetation)
//   was measured CLASS-ISOLATED. The PRODUCTION wrapper
//   compat/world-app.js#rebuildVegetation short-circuited with
//   `if (state.vegBusy) return null;` BEFORE the request could ever reach
//   the class queue — so in the production path a newer vegetation request
//   made while a build was busy was DROPPED, and even a class-queued
//   rebuild's census was never committed back to state.vegCensus /
//   state.coherence.veg.
//
// THIS tool measures the PRODUCTION WRAPPER PATH (not the class in
// isolation): the wrapper is extracted VERBATIM from compat/world-app.js
// (the exact function the browser runs) and driven through the
// A -> B-while-busy race with a SLOW synthetic provider standing in for
// the real climate+models+textures fetch chain. The provider is synthetic;
// the busy/rebuild/commit logic under test is the production wrapper.
//
//   --phase pre   measure the CURRENT worktree wrapper BEFORE the P1-2 fix
//                 (expected: the B request is LOST — dropped at the wrapper;
//                  final committed vegCensus stays stale/null; coherence.veg
//                  does not reflect B; READY not reachable for the new window).
//   --phase post  measure the SAME wrapper AFTER the P1-2 fix
//                 (expected: B is STORED at the wrapper (latest-wins) and
//                  DELIVERED to the class; the WINNING census (B) is committed
//                  gen-gated vs requestId; coherence.veg = B; READY reachable).
//
// The SAME committed tool measures both phases (no between-phase edits of the
// tool; the measured object is compat/world-app.js, whose SHA256 is pinned in
// every record). Writes (never PRE_COUNTERCHECKS.json / POST_COUNTERCHECKS.json
// — the published original evidence is immutable):
//   docs/audits/<RUN_ID>/CORRECTION_COUNTERCHECKS.json   (canonical; keyed by phase)
//   docs/audits/<RUN_ID>/raw/CORRECTION/<PHASE>_WRAPPER_RAW.json
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const RUN_ID = 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010';
const PKG = path.join(ROOT, 'docs', 'audits', RUN_ID);
const hash = (b) => crypto.createHash('sha256').update(b).digest('hex');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const args = process.argv.slice(2);
let phase = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--phase') phase = args[++i];
}
if (phase !== 'pre' && phase !== 'post') {
  console.error('usage: node tools/pecompat/world_r2_correction_counterchecks.mjs --phase pre|post');
  process.exit(2);
}

const appSource = fs.readFileSync(path.join(ROOT, 'compat/world-app.js'), 'utf8');
const worldAppSha = hash(Buffer.from(appSource, 'utf8'));
const toolSha = hash(fs.readFileSync(fileURLToPath(import.meta.url)));

// the PRODUCTION wrapper, extracted verbatim (the exact function the browser
// executes — never a reimplementation)
function extractWrapper(src) {
  const start = src.indexOf('async function rebuildVegetation(');
  if (start < 0) throw new Error('rebuildVegetation not found in compat/world-app.js');
  const end = src.indexOf('\n}', start) + 2;
  if (end <= start) throw new Error('rebuildVegetation end not found');
  return src.slice(start, end);
}
const wrapperSrc = extractWrapper(appSource);

/** The SLOW-provider fixture: a synthetic WorldVegetation stand-in whose
 *  rebuild(origin) hangs for origin A until released (standing in for the
 *  real climate fetch + model payload fetch + texture chain), then returns
 *  a census tagged with that origin. */
function makeFixture() {
  const calls = [];
  const banners = [];
  let releaseA = null;
  const gateA = new Promise((res) => { releaseA = res; });
  const veg = {
    lastCensus: null,
    async rebuild(origin, windowTiles) {
      calls.push({ gx: origin.gx, gy: origin.gy, windowTiles });
      if (origin.gx === 0) await gateA; // the SLOW provider leg (A in flight)
      const c = {
        ok: true, aborted: false, unsupportedProfile: false, error: null,
        window: { origin: { gx: origin.gx, gy: origin.gy }, windowTiles },
        counts: { requested: 1, selected: 1, placed: 1, limited: 0, cap: 5000 },
        statusCounts: { PLACED_ON_AVAILABLE_SURFACE: 1, DEFERRED_NO_SURFACE: 0, UNSUPPORTED_MODEL: 0, LOD_LIMITED: 0 },
        _tag: `origin-${origin.gx},${origin.gy}`,
      };
      veg.lastCensus = c;
      return c;
    },
  };
  const fx = {
    state: {
      vegOn: true,
      veg,
      vegCensus: null,
      vegBusy: false,
      vegPending: null,
      coherence: { terrain: { gx: 0, gy: 0 }, splat: { gx: 0, gy: 0 }, veg: null },
      sceneRequest: { id: 1, origin: { gx: 0, gy: 0 } },
    },
    calls, banners, releaseA,
    panelUpdates: 0,
  };
  const ctx = vm.createContext({
    state: fx.state,
    WINDOW_T: 8,
    banner: (m) => { banners.push(String(m)); },
    updateVegPanel: () => { fx.panelUpdates++; },
    updateEvidencePanel: () => {},
  });
  vm.runInContext(wrapperSrc, ctx, { filename: 'compat/world-app.js#rebuildVegetation(extracted)' });
  fx.ctx = ctx;
  return fx;
}

// ---- scenario 1: THE QC-required production race (A -> B while busy) ----
async function scenarioLatestWins() {
  const fx = makeFixture();
  const A = { gx: 0, gy: 0 }, B = { gx: 8, gy: 0 };
  // (1) request A with scene id 1 — the SLOW build starts (provider hangs)
  const runA = fx.ctx.rebuildVegetation(A, 1);
  await sleep(40); // A is in-flight: state.vegBusy === true
  const busyDuringA = fx.state.vegBusy;
  // (2) the streaming tick moves the scene to B: requestScene bumped the id
  //     to 2, rebuildWindow(B) rebuilt the terrain + textures for B (their
  //     coherence commits — the veg request for B ORIGINATES there), and
  //     rebuildWindow fires rebuildVegetation(B, 2) WHILE A is busy
  fx.state.sceneRequest = { id: 2, origin: { ...B } };
  fx.state.coherence.terrain = { ...B }; // rebuildWindow(B) committed the newer terrain
  fx.state.coherence.splat = { ...B };   // ...and the newer texture chain
  const runB = fx.ctx.rebuildVegetation({ ...B }, 2);
  const bReturnWhileBusy = await runB; // the busy-path return value
  // (3) A's provider resolves; the busy rebuild finishes
  fx.releaseA();
  await runA;
  await sleep(120); // let any queued/delivered newest request run
  // (4) the FINAL COMMITTED state (what the census panel + coherence line show)
  const finalCensusOrigin = fx.state.vegCensus?.window?.origin ?? null;
  const coherenceVeg = fx.state.coherence?.veg ?? null;
  // the updateCoherencePanel `same()` rule re-derived independently here
  const req = fx.state.sceneRequest;
  const same = (a) => !!(a && a.gx === req.origin.gx && a.gy === req.origin.gy);
  const terrainOk = same(fx.state.coherence.terrain);
  const splatOk = same(fx.state.coherence.splat);
  const vegOk = !!fx.state.vegOn && same(fx.state.coherence.veg);
  const allCoherent = terrainOk && splatOk && vegOk; // == the page READY condition
  return {
    scenario: 'A=(0,0) id 1 starts (slow provider) -> scene moves to B=(8,0) id 2 requested WHILE the veg rebuild is busy -> A provider resolves -> drain',
    vegBusyDuringA: busyDuringA,
    busyPathReturn: bReturnWhileBusy === null || bReturnWhileBusy === undefined ? 'null' : '(non-null census returned while busy)',
    classDeliveryOrder: fx.calls.map((c) => `(${c.gx},${c.gy})`),
    bReachedTheClass: fx.calls.some((c) => c.gx === B.gx && c.gy === B.gy),
    finalCommittedVegCensusOrigin: finalCensusOrigin,
    coherenceVeg,
    lastRequestWins: !!(finalCensusOrigin && finalCensusOrigin.gx === B.gx && finalCensusOrigin.gy === B.gy),
    coherenceVegMatchesLastRequest: !!(coherenceVeg && coherenceVeg.gx === B.gx && coherenceVeg.gy === B.gy),
    readyReachableForTheLastRequest: allCoherent,
    panelsUpdated: fx.panelUpdates,
  };
}

// ---- scenario 2: identical-repeat dedupe (the wrapper-level requestScene
// analogue; regression guard for the drain loop) ----
async function scenarioDedupe() {
  const fx = makeFixture();
  const A = { gx: 0, gy: 0 };
  const runA = fx.ctx.rebuildVegetation({ ...A }, 1);       // the running build
  await sleep(30);
  const runRepeat = fx.ctx.rebuildVegetation({ ...A }, 1);  // an IDENTICAL repeat (same origin + same request id)
  fx.releaseA();
  await runA; await runRepeat;
  await sleep(80);
  return {
    scenario: 'identical repeat (same origin + same request id) while the same request is running -> the repeat must NOT re-run the class build',
    classCalls: fx.calls.length,
    dedupeHeld: fx.calls.length === 1,
    committedOrigin: fx.state.vegCensus?.window?.origin ?? null,
  };
}

// ---- scenario 3: the stale-request gen-gate (negative control): a request
// whose id is no longer the current scene request must NOT commit its
// census (no stale overwrite of the newer scene's coherence) ----
async function scenarioStaleGate() {
  const fx = makeFixture();
  // scene id 30 is current; the veg request carries id 29 (superseded)
  fx.state.sceneRequest = { id: 30, origin: { gx: 16, gy: 0 } };
  const run = fx.ctx.rebuildVegetation({ gx: 16, gy: 0 }, 29);
  fx.releaseA(); // origin.gx===0? no — 16 runs immediately (no hang)
  await run;
  await sleep(60);
  return {
    scenario: 'a veg request with a STALE request id (29 vs current scene id 30): the census must NOT be committed',
    staleCensusCommitted: fx.state.vegCensus !== null,
    coherenceVegAfterStale: fx.state.coherence.veg ?? null,
    gateHeld: fx.state.vegCensus === null && fx.state.coherence.veg === null,
  };
}

const s1 = await scenarioLatestWins();
const s2 = await scenarioDedupe();
const s3 = await scenarioStaleGate();

const fixedPost = s1.lastRequestWins && s1.coherenceVegMatchesLastRequest && s1.readyReachableForTheLastRequest && s2.dedupeHeld && s3.gateHeld;
const brokenPre = !s1.lastRequestWins && !s1.bReachedTheClass;

const measurement = {
  measuredAt: new Date().toISOString(),
  git: {
    head: execFileSync('git', ['-C', ROOT, 'rev-parse', 'HEAD']).toString().trim(),
    status: execFileSync('git', ['-C', ROOT, 'status', '--porcelain']).toString().trim().split('\n').filter(Boolean),
  },
  productionWrapper: {
    source: 'compat/world-app.js#rebuildVegetation (extracted verbatim; executed in a controlled VM context)',
    worldAppSha256: worldAppSha,
    extractMethod: 'indexof("async function rebuildVegetation(") .. first "\\n}" — the exact function text the browser runs',
  },
  tool: { path: 'tools/pecompat/world_r2_correction_counterchecks.mjs', sha256: toolSha, sameToolBothPhases: true },
  scenarioLatestWins: s1,
  scenarioIdenticalRepeatDedupe: s2,
  scenarioStaleRequestGenGate: s3,
  expectedPre: 'BROKEN (the busy wrapper drops the newer request BEFORE the class: B never reaches the class; the final committed vegCensus/coherence do NOT reflect B; READY not reachable for the new window — stale PARTIAL persists until the next user action)',
  expectedPost: 'FIXED (the wrapper STORES the newest request while busy (latest-wins) and DELIVERS it to the class when the running build finishes; the WINNING census (the LAST request) is committed gen-gated vs requestId; coherence.veg = the last request window; READY reachable)',
  verdict: phase === 'pre' ? (brokenPre ? 'P1-2 REPRODUCED on the production wrapper path (pre-fix)' : 'NOT reproduced (unexpected — honest record)') : (fixedPost ? 'P1-2 FIXED on the production wrapper path' : 'NOT fixed (honest record)'),
};

// raw per-phase record
fs.mkdirSync(path.join(PKG, 'raw', 'CORRECTION'), { recursive: true });
fs.writeFileSync(path.join(PKG, 'raw', 'CORRECTION', `${phase.toUpperCase()}_WRAPPER_RAW.json`), JSON.stringify({ run: RUN_ID, phase, ...measurement }, null, 1) + '\n');

// canonical correction JSON: BOTH phases in one file (pre replaces only its key)
const canonical = path.join(PKG, 'CORRECTION_COUNTERCHECKS.json');
let canonicalDoc = null;
try { canonicalDoc = JSON.parse(fs.readFileSync(canonical, 'utf8')); } catch { /* first run */ }
if (!canonicalDoc) {
  canonicalDoc = {
    run: RUN_ID,
    correctionRound: 'PE_MASTER_CORRECTION_DISPATCH_20261010 (bounded correction run after INTERNAL_QC_BY_PE_MASTER_AUDITOR; QC_REPORT P1-2)',
    finding: 'P1-2 [P1 MATERIAL]: the vegetation latest-request could still be LOST in the PRODUCTION wiring — the wrapper short-circuit (if (state.vegBusy) return null) dropped newer requests before they ever reached the WorldVegetation class queue, and a class-queued rebuild census was never committed back to state.vegCensus/state.coherence.veg (the wrapper had already returned).',
    scope: 'the PRODUCTION wrapper path (compat/world-app.js#rebuildVegetation), NOT the class in isolation; the class (compat/world-vegetation.js) was NOT touched by this fix (byte-identical; only the wrapper changed).',
    noteOriginalRunOverstatement: 'REPORT §1.2 of the original run claimed "kolejka latest-wins (WorldVegetation wewnętrznie)" as the production mechanism — SUPERSEDED: the class-internal queue was never reachable from the production path in the original published code (measured here, phase pre). The production latest-wins now lives in the WRAPPER (this fix).',
    phases: {},
  };
}
canonicalDoc.phases[phase] = measurement;
fs.writeFileSync(canonical, JSON.stringify(canonicalDoc, null, 1) + '\n');

console.log(JSON.stringify({ phase, worldAppSha256: worldAppSha, verdict: measurement.verdict,
  s1: { delivery: s1.classDeliveryOrder, lastRequestWins: s1.lastRequestWins, coherenceMatches: s1.coherenceVegMatchesLastRequest, readyReachable: s1.readyReachableForTheLastRequest },
  s2: { dedupeHeld: s2.dedupeHeld }, s3: { gateHeld: s3.gateHeld } }, null, 2));
