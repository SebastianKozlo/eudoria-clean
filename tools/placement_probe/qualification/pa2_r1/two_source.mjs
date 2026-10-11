// two_source.mjs — DA2-COV/P3 two-contributing-source measurement (contract §7)
// (RUN_ID PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011)
//
// Reproduces the externally measured cap32 case THROUGH THE ACTUAL SCAN of the
// UNCHANGED scanner (no scanner changes, no fabricated arrays): two synthetic
// records80() raw inputs with --budget-retained-candidates 32 produce, by the
// scanner's own retention semantics, exactly 29 rows from source 1 and 3 rows
// from source 2 (TOTAL_CANDIDATE_ROWS = 32; one records80() payload emits exactly
// 29 candidates, so the cap is reached only inside the second input).
//
// OBSERVER (contract §7): a bounded identity observer over the
// creation/forward/serialization collections using a WeakMap that assigns SCALAR
// ids to candidate objects — the observer stores ONLY scalar ids and counters,
// never candidate objects as its own audit roots. An alias counts once (same
// object -> same scalar id); an actual copied object counts separately (new
// object -> new scalar id). This reuses the marker-injection pattern of
// tools/placement_probe/tests/da2_retained.test.mjs (BASE) WITH ATTRIBUTION —
// the Set-of-objects audit collections are replaced by WeakMap/scalar ids.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { records80 } from '../../tests/fixtures.mjs';

const sha256 = b => createHash('sha256').update(b).digest('hex');
export const TWO_SOURCE_TARGETS = Object.freeze({
  RETAINED_CAP: 32, SOURCE_1_CONTRIBUTION: 29, SOURCE_2_CONTRIBUTION: 3, TOTAL_CANDIDATE_ROWS: 32,
  PEAK_DISTINCT_CREATION_MAX: 32, PEAK_DISTINCT_FORWARD_MAX: 32, PEAK_DISTINCT_SERIALIZATION_MAX: 32,
});

// ---- marker-injection (pattern attributed to da2_retained.test.mjs, BASE) ----
const MARK_CREATION = '  budget.trackTotalHeld(found.length);';
const MARK_FORWARD = '        allRows.push(c);';
const MARK_SERIALIZATION = "  writeCsvRows(path.join(root, 'placement_candidates.csv'), rows, cols, csvRowCells);";
const OBS_INIT = 'const T = globalThis.__tsof ??= { wm: new WeakMap(), next: 1, phases: [] };';
const OBS_IDOF = 'const __id = o => { let id = T.wm.get(o); if (id === undefined) { id = T.next++; T.wm.set(o, id); } return id; };';
const INJ_CREATION = `\n  { ${OBS_INIT} ${OBS_IDOF} T.phases.push({ stage: 'creation', distinctFound: new Set(found.map(__id)).size, trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates, auditObjectsRetained: 0 }); }`;
const INJ_FORWARD = `\n        { ${OBS_INIT} ${OBS_IDOF} T.phases.push({ stage: 'forward', input: file, entry: src.entry, rankIndex: k, retainedAfterPush: allRows.length, distinctLiveForward: new Set([...data.candidates, ...allRows].map(__id)).size, trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates, auditObjectsRetained: 0 }); }`;
const INJ_SERIALIZATION = `  { ${OBS_INIT} ${OBS_IDOF} const __serIds = new Set(); const __cells = r => { __serIds.add(__id(r)); return csvRowCells(r); }; writeCsvRows(path.join(root, 'placement_candidates.csv'), rows, cols, __cells); const __liveIds = new Set(rows.map(__id)); T.phases.push({ stage: 'serialization', liveRows: __liveIds.size, serializedIdentities: __serIds.size, combinedLiveDistinct: new Set([...__liveIds, ...__serIds]).size, allSerializedAreLiveRows: [...__serIds].every(id => __liveIds.has(id)), trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates, auditObjectsRetained: 0 }); fs.writeFileSync(path.join(root, 'TWO_SOURCE_OBSERVER.json'), JSON.stringify({ observer: 'WeakMap scalar-identity observer (DA2-COV, contract §7): scalar ids via WeakMap; phases hold only scalars/counters; no candidate objects retained as audit roots', attribution: 'marker-injection pattern reused from tools/placement_probe/tests/da2_retained.test.mjs (BASE 28e91eb) with the Set-of-objects collections replaced by WeakMap/scalar ids', phases: T.phases }, null, 2) + '\\n'); }`;

export function buildTwoSourceObservedTool(toolPath) {
  const original = fs.readFileSync(toolPath, 'utf8');
  let src = original;
  for (const [mark, inj, mode] of [[MARK_CREATION, INJ_CREATION, 'after'], [MARK_FORWARD, INJ_FORWARD, 'after'], [MARK_SERIALIZATION, INJ_SERIALIZATION, 'replace']]) {
    if (src.split(mark).length !== 2) throw Error('marker not unique: ' + mark.slice(0, 40));
    src = mode === 'replace' ? src.replace(mark, inj) : src.replace(mark, mark + inj);
  }
  return { originalSha256: sha256(Buffer.from(original)), observedSha256: sha256(Buffer.from(src)), source: src, mutation: 'none (read-only identity hooks; no predicate/limit/expectation changed)' };
}

// ---- the actual measurement through the UNCHANGED scanner ----
export function measureTwoSource({ toolPath, worktreeRoot, dir }) {
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const ids = path.join(dir, 'ids.json');
  fs.writeFileSync(ids, JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
  const raws = [];
  for (let i = 0; i < 2; i++) { const f = path.join(dir, `raw_${i}.vfs`); fs.writeFileSync(f, records80()); raws.push(f); }
  const obs = buildTwoSourceObservedTool(toolPath);
  const obsTool = path.join(dir, 'observed_tool.mjs');
  fs.writeFileSync(obsTool, obs.source);
  const run = (tool, tag) => {
    const out = path.join(dir, tag); fs.mkdirSync(out, { recursive: true });
    const res = spawnSync(process.execPath, [tool, '--repo', worktreeRoot, '--ids', ids, '--out', out, ...raws.flatMap(n => ['--input', n]), '--budget-retained-candidates', '32'], { encoding: 'utf8', timeout: 180000 });
    let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
    return { exitCode: res.status, stderr: res.stderr, stdout: res.stdout, summary, out };
  };
  const un = run(toolPath, 'un');
  const ob = run(obsTool, 'ob');
  const four = ['placement_candidates.csv', 'candidates_top.json', 'sources.json', 'scan_skips.csv'];
  const byteIdentical = Object.fromEntries(four.map(f => [f, fs.existsSync(path.join(un.out, f)) && fs.existsSync(path.join(ob.out, f)) && fs.readFileSync(path.join(un.out, f)).equals(fs.readFileSync(path.join(ob.out, f)))]));
  const budgetsIdentical = JSON.stringify(un.summary?.budgets) === JSON.stringify(ob.summary?.budgets);
  const phases = JSON.parse(fs.readFileSync(path.join(ob.out, 'TWO_SOURCE_OBSERVER.json'), 'utf8')).phases;
  // per-source provenance derived from the ordinary run's own output artifacts
  const csv = fs.readFileSync(path.join(un.out, 'placement_candidates.csv'), 'utf8').trim().split('\n');
  const perSource = {};
  for (const line of csv.slice(1)) { const input = line.split(',')[0]; perSource[input] = (perSource[input] || 0) + 1; }
  const contributions = raws.map((r, i) => ({ source: path.basename(r), path: r, rows: perSource[r] ?? 0 }));
  const sources = JSON.parse(fs.readFileSync(path.join(un.out, 'sources.json'), 'utf8'));
  const peaks = Object.fromEntries(['creation', 'forward', 'serialization'].map(st => {
    const vals = phases.filter(p => p.stage === st).map(p => (p.distinctFound ?? p.distinctLiveForward ?? p.combinedLiveDistinct ?? 0));
    return [st, vals.length ? Math.max(...vals) : null];
  }));
  const sers = phases.filter(p => p.stage === 'serialization');
  const fwdPerSource = {};
  for (const p of phases.filter(p => p.stage === 'forward')) fwdPerSource[p.input] = (fwdPerSource[p.input] ?? 0) + 1;
  return {
    tool: { ordinaryToolSha256: obs.originalSha256, observedToolSha256: obs.observedSha256, mutation: obs.mutation, observer: 'WeakMap scalar-identity observer (this module, recorded by SHA)', helperIdentity: sha256(fs.readFileSync(fileURLToPath(import.meta.url))) },
    un, ob, byteIdentical, budgetsIdentical, phases,
    perSource: { byInputPath: perSource, contributions, sourcesParseStatus: sources.map(s => ({ input: path.basename(s.input), parseStatus: s.parseStatus })) },
    peaks,
    totals: {
      candidateCount: un.summary?.candidateCount, trackedPeak: un.summary?.budgets?.used?.peakRetainedCandidates,
      coverage: un.summary?.budgets?.coverage, exhausted: un.summary?.budgets?.exhausted,
      serialization: sers[0] ?? null, forwardContributionsPerInput: fwdPerSource,
      bothInputsOpened: sources.length === 2 && sources.every(s => s.parseStatus === 'OK'),
      twoSourcesContributing: contributions.length === 2 && contributions.every(c => c.rows > 0),
    },
  };
}
