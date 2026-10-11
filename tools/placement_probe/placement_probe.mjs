#!/usr/bin/env node
/*
 * PE935 placement candidate reconnaissance - CORRECTION R1 (2026-10-11)
 * Corrected per contract PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011:
 *  - fail-closed numeric configuration validation (INVALID_CONFIGURATION, exit!=0, SCAN_STARTED=NO)
 *  - exclusion census: every declared archive entry has exactly one disposition
 *  - LAYOUT_ATTEMPTS counted for every visited (source, header, stride) BEFORE the
 *    divisibility/minRows filters; LAYOUTS_ADMITTED reported separately
 *  - joint XYZ_FINITE_RATE (complete finite triples / examined rows) reported for
 *    the sample AND (for finalists) as a real FULL_CENSUS over all table rows;
 *    the legacy xyzRate (mean of per-axis column in-range rates) is kept under its
 *    original name and meaning and is NOT renamed to the joint rate
 *  - f32 diagnostics per candidate field: FINITE_RATE with explicit denominator,
 *    NAN/INFINITY/SUBNORMAL/ZERO counts, magnitude summary, ALTERNATIVE_U32_INTERPRETATION
 *  - per-invocation budgets (shared across all inputs/entries): SYNTHETIC_INPUTS,
 *    SCANNED_BYTES (reserved before payload read), LAYOUT_EVALUATIONS,
 *    FULL_CENSUS_ROWS, RETAINED_CANDIDATES (peak across all structures)
 * Read-only input. NEVER labels a candidate as a historical placement.
 * No external dependencies. Node.js >= 20.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL, fileURLToPath } from 'node:url';

const DEFAULTS = Object.freeze({
  maxStride: 512, maxHeader: 64, minRows: 8, maxSampleRows: 1200,
  posLo: -200000, posHi: 200000, minPosRate: 0.88,
  minIdRate: 0.35, minDistinctId: 2, minPosDistinct: 4,
  maxPayloadMiB: 4, maxInputMiB: 650, top: 100,
  seed: 0x13572468,
});
// Canonical execution ceilings - thresholds may be LOWERED per invocation (CLI --budget-*),
// never raised. These are tool-execution budgets, not scientific claims.
export const BUDGET_CEILINGS = Object.freeze({
  syntheticInputs: 32, scannedBytes: 67108864, layoutEvaluations: 100000,
  fullCensusRows: 50000, retainedCandidates: 256,
});
const MAGIC_SKIP_EXTS = new Set(['.nif','.dds','.tga','.png','.jpg','.jpeg','.bmp','.glb','.wav','.ogg','.mp3','.mp4','.bvi']);
const sha256 = b => createHash('sha256').update(b).digest('hex');
const inRange = (x, min, max) => Number.isFinite(x) && x >= min && x <= max;
function rng(seed) { let x = seed >>> 0; return () => { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return (x >>> 0) / 4294967296; }; }
function shuffleCopy(arr, seed) { const a = Array.from(arr), rand = rng(seed); for (let j = a.length - 1; j > 0; j--) { const k = Math.floor(rand() * (j + 1)); [a[j], a[k]] = [a[k], a[j]]; } return a; }
function csvEscape(v) { const x = String(v ?? ''); return /[",\n\r]/.test(x) ? '"' + x.replaceAll('"', '""') + '"' : x; }
function writeCsv(to, objects, cols) { const out = [cols.join(','), ...objects.map(v => cols.map(k => csvEscape(v[k])).join(','))].join('\n') + '\n'; fs.writeFileSync(to, out, 'utf8'); }

// ---------------- configuration validation (fail-closed) ----------------
const INT_RULES = {
  maxStride: { min: 12, max: 4096 },
  maxHeader: { min: 0, max: 1 << 20 },      // legal zero (search from offset 0)
  minRows: { min: 1, max: 1 << 24 },
  maxSampleRows: { min: 1, max: 1 << 24 },
  minDistinctId: { min: 1, max: 0xffffffff },
  minPosDistinct: { min: 0, max: 1 << 24 }, // legal zero
  top: { min: 0, max: 1 << 24 },            // legal zero
  seed: { min: 0, max: 0xffffffff },
};
const RATE_KEYS = ['minPosRate', 'minIdRate'];      // proportions: [0,1]
const SIZE_KEYS = ['maxPayloadMiB', 'maxInputMiB']; // sizes: >= 0 (legal zero excludes everything)
const POS_KEYS = ['posLo', 'posHi'];               // finite, posLo < posHi, negatives allowed
const BUDGET_RULES = {
  syntheticInputs: { min: 1, max: BUDGET_CEILINGS.syntheticInputs },
  scannedBytes: { min: 1, max: BUDGET_CEILINGS.scannedBytes },
  layoutEvaluations: { min: 1, max: BUDGET_CEILINGS.layoutEvaluations },
  fullCensusRows: { min: 1, max: BUDGET_CEILINGS.fullCensusRows },
  retainedCandidates: { min: 1, max: BUDGET_CEILINGS.retainedCandidates },
};
export function validateOptions(cfg) {
  const bad = [];
  for (const [k, r] of Object.entries(INT_RULES)) {
    const v = cfg[k];
    if (!Number.isSafeInteger(v)) bad.push(k + ' must be an integer (got ' + (v === undefined ? 'MISSING_VALUE_AFTER_FLAG' : JSON.stringify(v)) + ')');
    else if (v < r.min || v > r.max) bad.push(k + ' out of range [' + r.min + ', ' + r.max + ']: ' + v);
  }
  for (const k of RATE_KEYS) {
    const v = cfg[k];
    if (!Number.isFinite(v)) bad.push(k + ' must be finite (got ' + (v === undefined ? 'MISSING_VALUE_AFTER_FLAG' : JSON.stringify(v)) + ')');
    else if (v < 0 || v > 1) bad.push(k + ' out of range [0,1]: ' + v);
  }
  for (const k of SIZE_KEYS) {
    const v = cfg[k];
    if (!Number.isFinite(v)) bad.push(k + ' must be finite (got ' + (v === undefined ? 'MISSING_VALUE_AFTER_FLAG' : JSON.stringify(v)) + ')');
    else if (v < 0) bad.push(k + ' must be >= 0: ' + v);
  }
  for (const k of POS_KEYS) {
    const v = cfg[k];
    if (!Number.isFinite(v)) bad.push(k + ' must be finite (got ' + (v === undefined ? 'MISSING_VALUE_AFTER_FLAG' : JSON.stringify(v)) + ')');
  }
  if (Number.isFinite(cfg.posLo) && Number.isFinite(cfg.posHi) && !(cfg.posLo < cfg.posHi)) bad.push('posLo must be < posHi (got ' + cfg.posLo + ' >= ' + cfg.posHi + ')');
  const budgets = { ...BUDGET_CEILINGS, ...(cfg.budgetThresholds || {}) };
  for (const [k, r] of Object.entries(BUDGET_RULES)) {
    const v = budgets[k];
    if (!Number.isSafeInteger(v)) bad.push('budgetThresholds.' + k + ' must be an integer (got ' + JSON.stringify(v) + ')');
    else if (v < r.min || v > r.max) bad.push('budgetThresholds.' + k + ' out of range [' + r.min + ', ' + r.max + '] (ceiling ' + BUDGET_CEILINGS[k] + '): ' + v);
  }
  return { ok: bad.length === 0, errors: bad, budgets };
}
function assertValidConfig(cfg) { const v = validateOptions(cfg); if (!v.ok) throw new Error('INVALID_CONFIGURATION: ' + v.errors.join('; ')); return v.budgets; }

// ---------------- budget tracker (per invocation, shared across inputs) --------
export class Budget {
  constructor(thresholds) {
    this.limits = Object.freeze({ ...BUDGET_CEILINGS, ...thresholds });
    this.layoutAttempts = 0; this.scannedBytes = 0; this.syntheticInputs = 0;
    this.fullCensusRows = 0; this.peakRetained = 0; this.sampleRowsExamined = 0;
    this.containerReadBytes = 0; this.controlWorkBytes = 0;
    this.exhausted = []; this.refusals = []; this.externalRetained = 0;
  }
  markExhausted(kind, detail) { if (!this.exhausted.includes(kind)) this.exhausted.push(kind); this.refusals.push({ kind, detail, layoutAttempts: this.layoutAttempts, scannedBytes: this.scannedBytes, syntheticInputs: this.syntheticInputs, fullCensusRows: this.fullCensusRows, retainedPeak: this.peakRetained, externalRetained: this.externalRetained }); }
  refundPayload(size) { this.scannedBytes -= size; this.syntheticInputs--; } // reservation released when a reserved payload is never scanned (parse failure / pre-exhaustion skip)
  admitPayload(size, label) {
    if (this.syntheticInputs + 1 > this.limits.syntheticInputs) { this.markExhausted('SYNTHETIC_INPUTS', 'refused payload admission: ' + label); return false; }
    if (this.scannedBytes + size > this.limits.scannedBytes) { this.markExhausted('SCANNED_BYTES', 'refused payload ' + label + ': ' + size + 'B would exceed ' + this.limits.scannedBytes); return false; }
    this.syntheticInputs++; this.scannedBytes += size; return true; // reservation BEFORE read, using verified size
  }
  tryLayoutAttempt() {
    this.layoutAttempts++;
    if (this.layoutAttempts > this.limits.layoutEvaluations) { this.markExhausted('LAYOUT_EVALUATIONS', 'layout attempt ' + this.layoutAttempts + ' exceeds ' + this.limits.layoutEvaluations); return false; }
    return true;
  }
  tryRetain(localCount) {
    const total = this.externalRetained + localCount; // peak across ALL structures (main rows + local lists)
    if (total + 1 > this.limits.retainedCandidates) { this.markExhausted('RETAINED_CANDIDATES', 'candidate retention ' + (total + 1) + ' exceeds ' + this.limits.retainedCandidates); return false; }
    return true;
  }
  trackTotalHeld(localCount) { this.trackPeak(this.externalRetained + localCount); }
  trackPeak(n) { if (n > this.peakRetained) this.peakRetained = n; }
  tryFullCensus(rows) {
    if (this.fullCensusRows + rows > this.limits.fullCensusRows) { this.markExhausted('FULL_CENSUS_ROWS', 'census ' + this.fullCensusRows + '+' + rows + ' exceeds ' + this.limits.fullCensusRows); return false; }
    this.fullCensusRows += rows; return true;
  }
  get coverage() { return this.exhausted.length ? 'PARTIAL' : 'FULL'; }
  summary() { return { limits: this.limits, used: { layoutAttempts: this.layoutAttempts, scannedBytes: this.scannedBytes, syntheticInputs: this.syntheticInputs, fullCensusRows: this.fullCensusRows, peakRetainedCandidates: this.peakRetained, sampleRowsExamined: this.sampleRowsExamined }, containerReadBytes: this.containerReadBytes, controlWorkBytes: this.controlWorkBytes, exhausted: this.exhausted, refusals: this.refusals, coverage: this.coverage }; }
}
// ---------------- ids / helpers (unchanged discovery semantics) ----------------
function readIds(jsonPath) {
  const obj = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const sets = {}; for (const [key, v] of Object.entries(obj)) {
    if (!Array.isArray(v) || !/^S_(tpl|model|bvi)$/.test(key)) continue;
    const ints = v.map(i => Number(i)); if (ints.some(i => !Number.isSafeInteger(i) || i < 0 || i > 0xffffffff)) throw Error('bad ID in ' + key);
    sets[key] = new Set(ints.filter(x => x !== 0 && x !== 0xffff && x !== 0xffffffff));
  }
  if (!sets.S_tpl?.size) throw Error('--ids JSON must include nonempty S_tpl array from verified templates.vfs parser; cannot infer it from a file name');
  return sets;
}
function optionsFrom(argv) {
  const cfg = { ...DEFAULTS, inputs: [], repo: null, ids: null, out: null, anchors: null, includeAssets: false, includeAllEntries: false, entryRegex: null, budgetThresholds: {} };
  const str = { '--repo': 'repo', '--ids': 'ids', '--out': 'out', '--anchors': 'anchors', '--entry-regex': 'entryRegex' };
  const num = { '--max-stride': 'maxStride', '--max-header': 'maxHeader', '--min-rows': 'minRows', '--max-sample-rows': 'maxSampleRows', '--pos-lo': 'posLo', '--pos-hi': 'posHi', '--min-pos-rate': 'minPosRate', '--min-id-rate': 'minIdRate', '--min-distinct-id': 'minDistinctId', '--max-payload-mib': 'maxPayloadMiB', '--max-input-mib': 'maxInputMiB', '--top': 'top', '--seed': 'seed' };
  const budget = { '--budget-max-inputs': 'syntheticInputs', '--budget-scanned-bytes': 'scannedBytes', '--budget-layout-evals': 'layoutEvaluations', '--budget-census-rows': 'fullCensusRows', '--budget-retained-candidates': 'retainedCandidates' };
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--input') { if (i + 1 >= argv.length) throw Error('INVALID_CONFIGURATION: missing value after --input'); cfg.inputs.push(argv[++i]); continue; }
    if (key === '--include-assets') { cfg.includeAssets = true; continue; }
    if (key === '--all-entries') { cfg.includeAllEntries = true; continue; }
    if (key === '--help' || key === '-h') { cfg.help = true; continue; }
    if (str[key]) { if (i + 1 >= argv.length) throw Error('INVALID_CONFIGURATION: missing value after ' + key); cfg[str[key]] = argv[++i]; continue; }
    if (budget[key]) { const raw = argv[++i]; if (raw === undefined || raw === '') throw Error('INVALID_CONFIGURATION: missing value after ' + key); const n = Number(raw); if (!Number.isSafeInteger(n)) throw Error('INVALID_CONFIGURATION: ' + key + ' must be an integer, got ' + JSON.stringify(raw)); cfg.budgetThresholds[budget[key]] = n; continue; }
    if (num[key]) { const raw = argv[++i]; if (raw === undefined || raw === '') throw Error('INVALID_CONFIGURATION: missing value after ' + key); const n = Number(raw); if (typeof n !== 'number' || !Number.isFinite(n)) throw Error('INVALID_CONFIGURATION: ' + key + ' must be a finite number, got ' + JSON.stringify(raw)); cfg[num[key]] = n; continue; }
    throw Error('INVALID_CONFIGURATION: unknown option ' + key);
  }
  return cfg;
}
function usage() { return 'PE placement candidate probe, correction R1 (READ ONLY, never CONFIRMED by heuristics)\nnode placement_probe.mjs --repo <eudoria-clean repo> --ids <id_sets.json> --out <dir> --input <file> [--input ...]\nOptional: --entry-regex <regex>, --include-assets, --max-stride 512 --max-payload-mib 4\n  --min-id-rate .35 --pos-lo -200000 --pos-hi 200000 --min-distinct-id 1|2 (default 2; 1 enables\n  single-definition tables at the cost of a broader candidate net), --anchors <aligned_positions.json>\nBudget thresholds (per invocation; may only LOWER the canonical ceilings):\n  --budget-max-inputs N (<=32) --budget-scanned-bytes N (<=67108864) --budget-layout-evals N (<=100000)\n  --budget-census-rows N (<=50000) --budget-retained-candidates N (<=256)\nInvalid numeric configuration => INVALID_CONFIGURATION, nonzero exit, SCAN_STARTED=NO.\nSchema ids JSON: {"S_tpl":[4057,...], "S_model":[218757,...], "S_bvi":[]}\nAnchors JSON: [{"definitionId":4057,"position":[1,2,3],"tolerance":20}, ...]\n'; }
function distinctValueCount(a, cap = 50) { const s = new Set(); for (let v of a) { s.add(v); if (s.size > cap) return s.size; } return s.size; }
function readNum(buf, base, width) { return width === 2 ? buf.readUInt16LE(base) : buf.readUInt32LE(base); }
function posColumn(buf, h, s, n, o, opts) {
  let ok = 0, distinct = new Set(), nonzero = 0;
  for (let j = 0; j < n; j++) { const v = buf.readFloatLE(h + j * s + o); if (inRange(v, opts.posLo, opts.posHi)) ok++; if (v !== 0) nonzero++; if (distinct.size <= 100) distinct.add(v); }
  return { rate: ok / n, distinct: distinct.size, nonzero: nonzero / n };
}
function idColumn(buf, h, s, n, o, width, set) { let hits = 0; const vals = [], recognized = [];
  for (let j = 0; j < n; j++) { const v = readNum(buf, h + j * s + o, width); vals.push(v); if (set.has(v)) { hits++; recognized.push(v); } }
  return { rate: hits / n, hits, matchedDistinct: distinctValueCount(recognized), values: vals };
}
/** INVARIANT: shuffling ONLY the ID column does NOT change its set-membership rate.
 * Don't pretend that it is a negative control. Use wrong-ID-set/byte-scramble;
 * with independent spatial anchors, evaluate ROW-LEVEL JOINT associations. */
function jointAnchorMatches(ids, coords, anchors) {
  let total = 0, close = 0, distances = [];
  for (const a of anchors) {
    if (!Number.isInteger(a.definitionId) || !Array.isArray(a.position) || a.position.length !== 3 || !Number.isFinite(a.tolerance) || a.tolerance < 0) throw Error('invalid aligned anchor');
    total++; let d = Infinity;
    for (let i = 0; i < ids.length; i++) if (ids[i] === a.definitionId) { let dd = Math.hypot(...coords[i].map((v, j) => v - a.position[j])); if (dd < d) d = dd; }
    distances.push(Number.isFinite(d) ? d : null); if (d <= a.tolerance) close++;
  }
  return { total, close, distances };
}
function wrongIdSet(set, width, seed) { const max = width === 2 ? 65536 : 4294967296; let out = new Set(), rand = rng(seed ^ max), attempts = 0;
  while (out.size < set.size && attempts < set.size * 60 + 200) { let v = Math.floor(rand() * max); attempts++; if (v !== 0 && !set.has(v)) out.add(v); }
  return out;
}
function evaluateRows(buf, h, s, subset, opts) {
  const n = Math.floor((buf.length - h) / s); const rows = Math.min(n, opts.maxSampleRows), sel = [];
  for (let i = 0; i < rows; i++) sel.push(Math.floor((i + 0.5) * n / rows));
  return sel;
}
// joint row-triple finite rate + per-axis finite/in-range/subnormal/u32 diagnostics
function tripleStats(buf, header, stride, xyzOff, indices, opts) {
  const perAxis = [0, 1, 2].map(() => ({ finite: 0, inRange: 0, nan: 0, inf: 0, subnormal: 0, zero: 0, u32: { min: Infinity, max: -Infinity, zero: 0, distinct: new Set() }, absMin: Infinity, absMax: 0 }));
  let completeFiniteTriples = 0, posConformingTriples = 0;
  for (const i of indices) {
    let allFin = true, allInRange = true;
    for (let a = 0; a < 3; a++) {
      const off = header + i * stride + xyzOff + a * 4;
      const u32 = buf.readUInt32LE(off); const v = buf.readFloatLE(off);
      const st = perAxis[a];
      st.u32.min = Math.min(st.u32.min, u32); st.u32.max = Math.max(st.u32.max, u32); st.u32.distinct.add(u32); if (u32 === 0) st.u32.zero++;
      if (Number.isNaN(v)) st.nan++;
      else if (!Number.isFinite(v)) st.inf++;
      else {
        st.finite++; if (v === 0) st.zero++;
        const av = Math.abs(v); st.absMin = Math.min(st.absMin, av); st.absMax = Math.max(st.absMax, av);
        if (((u32 >>> 23) & 0xff) === 0 && (u32 & 0x7fffff) !== 0) st.subnormal++;
        if (inRange(v, opts.posLo, opts.posHi)) st.inRange++; else allInRange = false;
      }
      if (!Number.isFinite(v)) allFin = false;
    }
    if (allFin) completeFiniteTriples++;
    if (allFin && allInRange) posConformingTriples++;
  }
  const n = indices.length;
  const axisOut = perAxis.map(st => ({
    finiteRate: n ? st.finite / n : null, finiteCount: st.finite, examinedRows: n,
    posRangeRate: n ? st.inRange / n : null, posRangeCount: st.inRange,
    nanCount: st.nan, infinityCount: st.inf, subnormalCount: st.subnormal, zeroCount: st.zero,
    magnitudeSummary: { minAbsFinite: st.absMin === Infinity ? null : st.absMin, maxAbsFinite: st.finite === 0 ? null : st.absMax },
    alternativeU32Interpretation: { min: st.u32.min === Infinity ? null : st.u32.min, max: st.u32.max === -Infinity ? null : st.u32.max, zeroCount: st.u32.zero, distinctCount: st.u32.distinct.size },
  }));
  return {
    examinedRows: n,
    xyzFiniteRate: n ? completeFiniteTriples / n : null, // joint triple rate; null (NOT_EVALUATED) at zero denominator
    completeFiniteTriples, denominator: n,
    posConformingTripleRate: n ? posConformingTriples / n : null,
    perAxis: axisOut,
  };
}
function evaluateCandidateControls(buf, candidate, set, opts, anchors, budget) {
  const { header: h, stride: s, idOffset: idOff, idWidth: width, xyzOffset: xyzOff, sampleIndices: indices } = candidate;
  const ids = indices.map(i => readNum(buf, h + i * s + idOff, width));
  const coords = indices.map(i => [0, 4, 8].map(k => buf.readFloatLE(h + i * s + xyzOff + k)));
  const observedHits = ids.filter(i => set.has(i)).length;
  const randomSet = wrongIdSet(set, width, opts.seed + 31);
  const wrongSetHits = ids.filter(i => randomSet.has(i)).length;
  // Fixed-layout byte permutation null - DOES NOT constitute a general statistical proof.
  const rand = rng(opts.seed ^ s ^ h); const flat = Buffer.from(buf.subarray(h, h + Math.min(buf.length - h, Math.max(512, Math.min(512 * 1024, indices.length * s)))));
  budget.controlWorkBytes += flat.length;
  for (let i = flat.length - 1; i > 0; i--) { let j = Math.floor(rand() * (i + 1)); let tmp = flat[i]; flat[i] = flat[j]; flat[j] = tmp; }
  const byteN = Math.min(indices.length, Math.floor(flat.length / s)); let byteHits = 0;
  for (let i = 0; i < byteN; i++) if (set.has(readNum(flat, i * s + idOff, width))) byteHits++;
  // Stride +/-4 as a diagnostic: not a validity oracle; nested records can have aliases.
  const neighbor = {}; for (const other of [s - 4, s + 4]) { if (other < 12 || other > opts.maxStride + 4 || h + other > buf.length) continue;
    const rows = Math.min(indices.length, Math.floor((buf.length - h) / other)); let hit = 0; for (let i = 0; i < rows; i++) if (set.has(readNum(buf, h + i * other + idOff, width))) hit++;
    neighbor[other] = rows ? hit / rows : null;
  }
  const joint = anchors?.length ? jointAnchorMatches(ids, coords, anchors) : null;
  const shuffled = anchors?.length ? jointAnchorMatches(shuffleCopy(ids, opts.seed ^ 0x5a5a), coords, anchors) : null;
  return { wrongSetHitRate: wrongSetHits / ids.length, byteShuffleIdRate: byteN ? byteHits / byteN : null, neighborStrideIdRates: neighbor,
    idShuffleMembershipRate: observedHits / ids.length, permutationMembershipInvariant: true,
    independentAnchorJoint: joint, shuffledIdAnchorJoint: shuffled };
}export function analyzeBlob(buffer, sets, opts = {}) {
  const cfg = { ...DEFAULTS, ...opts };
  assertValidConfig(cfg); // exported function path validates too - no bypass of option checks
  const budget = cfg.budget instanceof Budget ? cfg.budget : new Budget(cfg.budgetThresholds || {});
  const buf = Buffer.isBuffer(buffer) ? buffer : Buffer.from(buffer);
  if (!sets?.S_tpl?.size) throw Error('non-empty template ID set required');
  const found = []; let layoutsAdmitted = 0, positionTriples = 0, idColumnsFound = 0;
  let budgetExhausted = false;
  outer:
  for (let h = 0; h <= Math.min(cfg.maxHeader, buf.length - 8 * cfg.minRows); h += 4) {
    for (let s = 12; s <= cfg.maxStride; s += 4) {
      if (!budget.tryLayoutAttempt()) { budgetExhausted = true; break outer; } // counted BEFORE divisibility/minRows/early-outs
      if ((buf.length - h) % s !== 0) continue; const N = (buf.length - h) / s; if (N < cfg.minRows) continue;
      layoutsAdmitted++;
      const inds = evaluateRows(buf, h, s, N, cfg), n = inds.length;
      budget.sampleRowsExamined += n;
      const sampled = Buffer.allocUnsafe(n * s); for (let j = 0; j < n; j++) buf.copy(sampled, j * s, h + inds[j] * s, h + (inds[j] + 1) * s);
      let triples = [];
      for (let o = 0; o + 12 <= s; o += 4) {
        const cs = [0, 4, 8].map(k => posColumn(sampled, 0, s, n, o + k, cfg));
        if (cs.every(x => x.rate >= cfg.minPosRate && x.distinct >= cfg.minPosDistinct)) triples.push({ offset: o, cs, meanRate: cs.reduce((a, c) => a + c.rate, 0) / 3 });
      }
      if (!triples.length) continue; positionTriples += triples.length;
      const candidates = [];
      for (let o = 0; o < s; o += 2) { for (let width of [2, 4]) {
        if (o + width > s) continue;
        for (const [setName, baseSet] of Object.entries(sets)) {
          const S = width === 2 ? new Set([...baseSet].filter(x => x < 65536)) : baseSet;
          if (!S.size) continue;
          let v = idColumn(sampled, 0, s, n, o, width, S); if (v.rate >= cfg.minIdRate && v.matchedDistinct >= cfg.minDistinctId) { idColumnsFound++; candidates.push({ offset: o, width, setName, set: S, stats: v }); }
        }
      } }
      for (const tri of triples) for (const ic of candidates) {
        if (ic.offset + ic.width > tri.offset && ic.offset < tri.offset + 12) continue; // do not interpret same bytes simultaneously as XYZ and ID
        if (!budget.tryRetain(found.length)) { budgetExhausted = true; break outer; }
        budget.trackTotalHeld(found.length + 1);
        const score = (ic.stats.rate + tri.meanRate) / 2;
        const item = { header: h, stride: s, rowCount: N, sampleCount: n, idOffset: ic.offset, idWidth: ic.width, idSetName: ic.setName, idRate: ic.stats.rate, idHits: ic.stats.hits, idDistinct: ic.stats.matchedDistinct, xyzOffset: tri.offset, xyzRate: tri.meanRate, score,
          sampleIndices: inds, idValues: ic.stats.values, _set: ic.set };
        found.push(item);
      }
    }
  }
  budget.trackTotalHeld(found.length);
  found.sort((a, b) => b.score - a.score || b.idRate - a.idRate || a.stride - b.stride);
  const selected = found.slice(0, cfg.top);
  // finalist diagnostics: sample stats + (budget-permitting) FULL census over ALL rows
  for (const c of selected) {
    c.sampleStats = tripleStats(buf, c.header, c.stride, c.xyzOffset, c.sampleIndices, cfg);
    c.sampleXyzFiniteRate = c.sampleStats.xyzFiniteRate; // joint triple rate on the sample
    if (budget.tryFullCensus(c.rowCount)) {
      const all = []; for (let i = 0; i < c.rowCount; i++) all.push(i);
      c.fullCensus = tripleStats(buf, c.header, c.stride, c.xyzOffset, all, cfg);
      c.fullCensusRowCount = c.rowCount;
      c.fullCensusXyzFiniteRate = c.fullCensus.xyzFiniteRate;
      let fullIdHits = 0; for (let i = 0; i < c.rowCount; i++) if (c._set.has(readNum(buf, c.header + i * c.stride + c.idOffset, c.idWidth))) fullIdHits++;
      c.fullCensusIdRate = c.rowCount ? fullIdHits / c.rowCount : null;
      c.censusStatus = 'FULL_CENSUS';
    } else {
      c.fullCensusRowCount = null; c.fullCensusXyzFiniteRate = null; c.fullCensusIdRate = null;
      c.censusStatus = 'PARTIAL_BUDGET_EXHAUSTED'; c.censusReason = 'FULL_CENSUS_ROWS budget exhausted';
    }
    c.tableRowCount = c.rowCount; c.sampledRowCount = c.sampleCount;
    c.controls = evaluateCandidateControls(buf, c, c._set, cfg, cfg.anchors, budget);
  }
  for (const c of selected) delete c._set; // sets are not JSON-serializable; controls retained
  const stats = {
    layoutAttempts: budget.layoutAttempts, // every visited (source,header,stride) BEFORE filters
    layoutsTested: layoutsAdmitted,        // LEGACY field (post-filter), kept for API compatibility
    layoutsAdmitted, positionTriples, idColumns: idColumnsFound,
    candidatesBeforeCap: found.length, candidatesEmitted: selected.length,
    capTruncated: found.length > selected.length,
    budgetExhausted, coverage: budget.coverage, exhaustedKinds: budget.exhausted,
  };
  return { candidates: selected, stats, config: cfg, budget: budget.summary() };
}
function normalizeCandidate(c) { const { sampleIndices, idValues, controls, ...rest } = c; return { ...rest, controls }; }
function verifyDirectoryInputs(inputs) { const o = []; for (let item of inputs) { if (!item || !fs.existsSync(item)) throw Error('input not found: ' + item); if (!fs.statSync(item).isFile()) throw Error('input must be regular file: ' + item); o.push(path.resolve(item)); } return o; }

// ---------------- container scan with exclusion census ----------------
async function scanInput(file, opts, sets, adapters, allRows, allSources, skips, budget) {
  const size = fs.statSync(file).size;
  const containerRecord = { input: file, sizeBytes: size, containerKind: null, parseStatus: null, declaredEntryCount: null, dispositions: [], scannedPayloadCount: 0, scanExceptions: 0 };
  if (size > opts.maxInputMiB * 1024 * 1024) {
    containerRecord.containerKind = path.extname(file).toLowerCase() || 'RAW_BLOB_UNFRAMED';
    containerRecord.parseStatus = 'INPUT_TOO_LARGE';
    skips.push({ file, entry: '', reason: 'INPUT_TOO_LARGE', size, message: '' });
    allSources.push(containerRecord); return;
  }
  budget.containerReadBytes += size;
  const ext = path.extname(file).toLowerCase();
  let sources = [];
  if (ext === '.bnt' || ext === '.ark') {
    containerRecord.containerKind = ext;
    const bytes = fs.readFileSync(file), containerSha = sha256(bytes);
    containerRecord.sha256 = containerSha;
    let entries = null, arch = null;
    try {
      arch = ext === '.bnt' ? new adapters.Bnt2Archive(bytes) : new adapters.ArkArchive(bytes);
      entries = arch.entries();
      containerRecord.declaredEntryCount = entries.length;
      containerRecord.parseStatus = 'OK';
    } catch (ex) {
      containerRecord.parseStatus = 'UNSUPPORTED'; // container-level framing failure - no invented entry count
      containerRecord.declaredEntryCount = null;
      skips.push({ file, entry: '', reason: 'CONTAINER_PARSE_FAILED', size, message: String(ex) });
      allSources.push(containerRecord); return;
    }
    for (const e of entries) {
      // exactly one disposition per declared entry, in fixed filter order:
      // FILTERED_REGEX -> FILTERED_EXTENSION -> ENTRY_TOO_LARGE -> TOO_SMALL -> PARSE_FAILED -> OVER_BUDGET -> SCANNED
      if (opts.entryRegex && !opts.entryRegex.test(e.name)) { containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'FILTERED_REGEX' }); continue; }
      const extE = path.extname(e.name).toLowerCase();
      if (!opts.includeAssets && !opts.includeAllEntries && MAGIC_SKIP_EXTS.has(extE)) { containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'FILTERED_EXTENSION' }); continue; }
      if (e.size > opts.maxPayloadMiB * 1024 * 1024) { containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'ENTRY_TOO_LARGE', detail: 'size ' + e.size + ' > cap' }); skips.push({ file, entry: e.name, reason: 'ENTRY_TOO_LARGE', size: e.size, message: '' }); continue; }
      if (e.size < opts.minRows * 12) { containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'TOO_SMALL', detail: 'size ' + e.size + ' < minRows*12' }); continue; }
      // budget reservation BEFORE the payload read, using the declared (directory) size;
      // the read result is verified below and the reservation is refunded if the payload is never scanned
      if (!budget.admitPayload(e.size, file + '!' + e.name)) { containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'OVER_BUDGET', detail: budget.exhausted[budget.exhausted.length - 1] }); continue; }
      let p = null;
      try { p = arch.readEntry(e).payload; } catch (ex) { budget.refundPayload(e.size); containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'PARSE_FAILED', message: String(ex) }); skips.push({ file, entry: e.name, reason: 'READER_FAILURE', size: e.size, message: String(ex) }); continue; }
      const payload = Buffer.from(p.buffer, p.byteOffset, p.byteLength);
      if (payload.length !== e.size) { budget.refundPayload(e.size); containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'PARSE_FAILED', message: 'payload size mismatch: declared ' + e.size + ', actual ' + payload.length }); skips.push({ file, entry: e.name, reason: 'PAYLOAD_SIZE_MISMATCH', size: e.size, message: 'actual ' + payload.length }); continue; }
      containerRecord.dispositions.push({ entryIndex: e.entryIndex, name: e.name, disposition: 'SCANNED' });
      sources.push({ bytes: payload, entry: e.name, index: e.entryIndex, offset: e.offset ?? e.dataOffset });
    }
    containerRecord.scannedPayloadCount = sources.length;
  } else {
    // RAW input: budget reservation BEFORE the payload read, using the verified on-disk size
    containerRecord.containerKind = 'RAW_BLOB_UNFRAMED';
    containerRecord.parseStatus = 'OK';
    containerRecord.declaredEntryCount = 1; // the raw file itself is one declared unit
    if (!budget.admitPayload(size, file)) {
      containerRecord.dispositions.push({ entryIndex: 0, name: '[whole file]', disposition: 'OVER_BUDGET', detail: budget.exhausted[budget.exhausted.length - 1] });
      allSources.push(containerRecord); return; // refused BEFORE the read
    }
    const bytes = fs.readFileSync(file);
    containerRecord.sha256 = sha256(bytes);
    containerRecord.dispositions.push({ entryIndex: 0, name: '[whole file]', disposition: 'SCANNED' });
    sources.push({ bytes, entry: '[whole file]', index: -1, offset: 0 });
    containerRecord.scannedPayloadCount = sources.length;
  }
  allSources.push(containerRecord);
  for (const src of sources) {
    if (budget.exhausted.length && (budget.exhausted.includes('LAYOUT_EVALUATIONS') || budget.exhausted.includes('RETAINED_CANDIDATES'))) {
      // a shared per-invocation budget was exhausted by an earlier payload: this admitted
      // payload is NOT analyzed - its admission-level disposition is corrected to OVER_BUDGET
      // (it was admitted, but no scan work was performed on it), recorded honestly,
      // and no double-charged layout attempt is burned.
      const d = containerRecord.dispositions.find(x => x.name === src.entry && x.disposition === 'SCANNED');
      if (d) { d.disposition = 'OVER_BUDGET'; d.detail = 'budget exhausted before analysis: ' + budget.exhausted.join(','); }
      skips.push({ file, entry: src.entry, reason: 'BUDGET_EXHAUSTED', total: '', emitted: '', message: budget.exhausted.join(',') });
      break;
    }
    try {
      const data = analyzeBlob(src.bytes, sets, { ...opts, budget });
      const meta = { input: file, containerSha256: containerRecord.sha256, entry: src.entry, entryIndex: src.index, entryOffset: src.offset, payloadSize: src.bytes.length, payloadSha256: sha256(src.bytes) };
      const rank = data.candidates;
      for (let k = 0; k < rank.length; k++) {
        // RETAINED_CANDIDATES applies to the GLOBAL peak across ALL structures:
        // main allRows + any per-call lists. Enforce before each retained row push.
        if (!budget.tryRetain(0)) { // total = externalRetained(rows) + 0 + 1(new row) vs limit
          skips.push({ file, entry: src.entry, reason: 'BUDGET_EXHAUSTED', total: '', emitted: '', message: 'RETAINED_CANDIDATES' });
          break;
        }
        budget.externalRetained++;
        budget.trackTotalHeld(0);
        const c = rank[k], coords = []; for (let j = 0; j < Math.min(16, c.sampleIndices.length); j++) {
          const i = c.sampleIndices[j], base = c.header + i * c.stride;
          coords.push({ row: i, sourceOffset: src.offset + base, ID: readNum(src.bytes, base + c.idOffset, c.idWidth), xyz: [0, 4, 8].map(v => src.bytes.readFloatLE(base + c.xyzOffset + v)) });
        }
        allRows.push({ ...meta, ...normalizeCandidate(c), sampleRows: coords, scanStats: data.stats });
      }
      if (data.stats.capTruncated) skips.push({ file, entry: src.entry, reason: 'PER_SOURCE_CANDIDATE_CAP', total: data.stats.candidatesBeforeCap, emitted: data.stats.candidatesEmitted, message: '' });
      if (data.stats.budgetExhausted) skips.push({ file, entry: src.entry, reason: 'BUDGET_EXHAUSTED', total: '', emitted: '', message: data.stats.exhaustedKinds.join(',') });
    } catch (ex) { containerRecord.scanExceptions++; skips.push({ file, entry: src.entry, reason: 'SCAN_EXCEPTION', message: String(ex) }); }
  }
}
async function main(argv) {
  let opts;
  try { opts = optionsFrom(argv); } catch (e) {
    process.stderr.write(String(e?.message || e) + '\n');
    process.stderr.write('SCAN_STARTED=NO\n');
    process.exitCode = 3; return; // fail-closed: no output dir, no scan
  }
  const v = validateOptions(opts);
  if (!v.ok) { process.stderr.write('INVALID_CONFIGURATION: ' + v.errors.join('; ') + '\n'); process.stderr.write('SCAN_STARTED=NO\n'); process.exitCode = 3; return; }
  const budget = new Budget(opts.budgetThresholds);
  if (opts.help) { process.stdout.write(usage()); return; }
  if (!opts.repo || !opts.ids || !opts.out || !opts.inputs.length) { process.stderr.write('INVALID_CONFIGURATION: required --repo --ids --out --input; run --help\n'); process.stderr.write('SCAN_STARTED=NO\n'); process.exitCode = 3; return; }
  const dir = path.resolve(opts.repo); const set = readIds(opts.ids); const files = verifyDirectoryInputs(opts.inputs); const root = path.resolve(opts.out);
  if (files.some(f => path.resolve(f).startsWith(root + path.sep)) || dir === root) { process.stderr.write('INVALID_CONFIGURATION: OUT must be separate from original input files\n'); process.stderr.write('SCAN_STARTED=NO\n'); process.exitCode = 3; return; }
  if (opts.anchors) { opts.anchors = JSON.parse(fs.readFileSync(opts.anchors, 'utf8')); if (!Array.isArray(opts.anchors)) throw Error('anchors JSON must be array'); }
  if (opts.entryRegex) opts.entryRegex = new RegExp(opts.entryRegex, 'i');
  const [x, y] = await Promise.all(['src/pesource/Bnt2Archive.js', 'src/pesource/ArkArchive.js'].map(s => import(pathToFileURL(path.join(dir, s)).href)));
  const adapters = { Bnt2Archive: x.Bnt2Archive, ArkArchive: y.ArkArchive };
  fs.mkdirSync(root, { recursive: true });
  let rows = [], sources = [], skips = [];
  for (const f of files) {
    await scanInput(f, opts, set, adapters, rows, sources, skips, budget);
    budget.trackPeak(rows.length);
    if (rows.length >= budget.limits.retainedCandidates) { budget.markExhausted('RETAINED_CANDIDATES', 'global rows retention at ' + rows.length); break; }
  }
  rows.sort((a, b) => b.score - a.score || b.idRate - a.idRate);
  const cols = ['input','entry','entryIndex','entryOffset','containerSha256','payloadSha256','payloadSize','header','stride','rowCount','sampleCount','tableRowCount','sampledRowCount','sampleXyzFiniteRate','fullCensusRowCount','fullCensusXyzFiniteRate','fullCensusIdRate','censusStatus','idOffset','idWidth','idSetName','idRate','idHits','idDistinct','xyzOffset','xyzRate','score','control_wrongSet','control_byteShuffle','control_neighbor','control_idShuffleInvariance','control_anchorMatches','control_shuffledAnchorMatches','status'];
  const csvRows = rows.map(x => ({ ...x, control_wrongSet: x.controls.wrongSetHitRate, control_byteShuffle: x.controls.byteShuffleIdRate, control_neighbor: JSON.stringify(x.controls.neighborStrideIdRates), control_idShuffleInvariance: x.controls.permutationMembershipInvariant, control_anchorMatches: x.controls.independentAnchorJoint?.close ?? 'NOT_PERFORMED', control_shuffledAnchorMatches: x.controls.shuffledIdAnchorJoint?.close ?? 'NOT_PERFORMED', status: 'CANDIDATE_ONLY_NOT_PLACEMENT_PROOF' }));
  writeCsv(path.join(root, 'placement_candidates.csv'), csvRows, cols);
  writeCsv(path.join(root, 'scan_skips.csv'), skips, ['file','entry','reason','size','message','total','emitted']);
  fs.writeFileSync(path.join(root, 'candidates_top.json'), JSON.stringify(rows.slice(0, Math.min(20, rows.length)), null, 2) + '\n');
  fs.writeFileSync(path.join(root, 'sources.json'), JSON.stringify(sources, null, 2) + '\n');
  // exclusion census reconciliation: every declared entry accounted exactly once
  const census = sources.map(c => ({ input: c.input, containerKind: c.containerKind, parseStatus: c.parseStatus, declaredEntryCount: c.declaredEntryCount, scannedPayloadCount: c.scannedPayloadCount, scanExceptions: c.scanExceptions, dispositions: c.dispositions, dispositionCounts: c.dispositions.reduce((m, d) => (m[d.disposition] = (m[d.disposition] || 0) + 1, m), {}), dispositionTotal: c.dispositions.length, censusOk: c.parseStatus === 'OK' ? (c.dispositions.length === c.declaredEntryCount) : null }));
  const safeOpts = Object.fromEntries(Object.entries(opts).filter(([key]) => !['entryRegex', 'anchors', 'budget'].includes(key)));
  const record = {
    tool: 'PE935_PLACEMENT_PROBE_R1_CORRECTION', timeUtc: new Date().toISOString(), mode: 'READ_ONLY_INPUTS__CANDIDATES_NOT_PROOF',
    scanStarted: 'YES', config: safeOpts, budgetThresholds: opts.budgetThresholds,
    inputFiles: files, idSetCounts: Object.fromEntries(Object.entries(set).map(([k, v]) => [k, v.size])),
    sourceCount: sources.length, candidateCount: rows.length, skippedCount: skips.length,
    exclusionCensus: census,
    budgets: budget.summary(),
    controls: { idShuffleMembershipRate: 'MATHEMATICALLY_INVARIANT__NOT_A_NEGATIVE_CONTROL', wrongIdSet: 'MEASURES_BASE_RATE_ONLY', byteScramble: 'STRUCTURAL_NEGATIVE_NOT_SCIENCE_PROOF', jointAnchors: opts.anchors?.length ? 'ALIGNED_REFERENCES_USER_SUPPLIED' : 'NOT_PERFORMED' },
    status: budget.coverage === 'PARTIAL' ? 'BUDGET_EXHAUSTED_COVERAGE_PARTIAL' : 'NO_PLACEMENT_CONFIRMED',
    warning: 'No graph/consumer join, no world XYZ; do not push raw rows or snippets to public repo. sampleXyzFiniteRate is a SAMPLE quantity; fullCensusXyzFiniteRate is only meaningful with censusStatus=FULL_CENSUS. xyzRate remains the legacy per-axis column-mean in-range rate.',
  };
  fs.writeFileSync(path.join(root, 'SUMMARY.json'), JSON.stringify(record, null, 2) + '\n');
  console.log('CANDIDATE_ONLY sources=' + sources.length + ' candidates=' + rows.length + ' skipped=' + skips.length + ' coverage=' + budget.coverage + ' output=' + root);
  if (skips.some(s => s.reason === 'SCAN_EXCEPTION' || s.reason === 'READER_FAILURE' || s.reason === 'CONTAINER_PARSE_FAILED')) process.exitCode = 2;
}
if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) { main(process.argv.slice(2)).catch(e => { console.error('FATAL: ' + (e?.stack || e)); process.exitCode = 1; }); }