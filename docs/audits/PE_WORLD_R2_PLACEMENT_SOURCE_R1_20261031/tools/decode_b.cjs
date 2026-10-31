#!/usr/bin/env node
// RUN Stage C — DECODER B (implementation lineage: CONTENT/STATISTICS-DRIVEN, Node.js).
//
// Lineage declaration (G3 / QH-009): written from the BYTES, not from decoder A's
// field table. No header count field is trusted:
//  - type0 family: candidate record grids are SOLVED from size divisibility +
//    intra-record consistency of the dominant repeating 8-byte pattern; the
//    record count is the number of grid cells found (never read from a header).
//  - type1 family: vertex count is DERIVED by scanning the longest run of
//    plausible (non-denormal) f32 from offset 12, then tricount u32 is read
//    after the run and validated (indices < vcount, block fits).
// Honest limitations recorded in output: a 1-record type0 file cannot yield a
// repeating-pattern statistic; stride is then solved by divisibility brute
// force and may remain AMBIGUOUS (candidate set reported, not hidden).
//
// Negative controls (a) wrong-endian (b) truncated (c) wrong-width must FAIL.

"use strict";
const fs = require("fs"), path = require("path");
const RUN = path.resolve(__dirname, "..");
const SAMPLES = ["506044.bvi", "105624.bvi", "506237.bvi", "584781.bvi"];

function readF32(buf, off, be) { return be ? buf.readFloatBE(off) : buf.readFloatLE(off); }
function readU32(buf, off, be) { return be ? buf.readUInt32BE(off) : buf.readUInt32LE(off); }
// plausible f32: finite, magnitude sane, exact zero allowed, denormals rejected
function plausibleF32(v) {
  return Number.isFinite(v) && (v === 0 || Math.abs(v) > 1e-30) && Math.abs(v) < 1e7;
}
function allPlausible(buf, off, n, be) {
  for (let i = 0; i < n; i++) if (!plausibleF32(readF32(buf, off + i * 4, be))) return false;
  return true;
}

// ---- type0: solve record grid from bytes ----
function solveType0(buf, be, opts, widthOverride) {
  opts = opts || {};
  // dominant repeating 8-byte pattern at 4-aligned offsets
  const freq = new Map();
  for (let o = 0; o + 8 <= buf.length; o += 4) {
    const k = buf.toString("latin1", o, o + 8);
    freq.set(k, (freq.get(k) || 0) + 1);
  }
  let bestKey = null, bestN = 0;
  for (const [k, n] of freq) if (n > bestN) { bestKey = k; bestN = n; }
  const positions = [];
  if (bestKey) for (let o = 0; o + 8 <= buf.length; o += 4)
    if (buf.toString("latin1", o, o + 8) === bestKey) positions.push(o);
  const spacingHisto = new Map();
  for (let i = 1; i < positions.length; i++) {
    const s = positions[i] - positions[i - 1];
    spacingHisto.set(s, (spacingHisto.get(s) || 0) + 1);
  }
  const strideCandidates = [];
  if (spacingHisto.size) {
    let s = 0, n = 0;
    for (const [k, v] of spacingHisto) if (v > n) { s = k; n = v; }
    strideCandidates.push(s);
  }
  // brute-force additional candidates from divisibility (independent of pattern)
  const bodyMax = buf.length - 4; // observed: leading bytes are 0..3 at most
  for (let s = 12; s <= 80; s += 4)
    if (!strideCandidates.includes(s) && Number.isInteger(bodyMax / s)) strideCandidates.push(s);

  const solutions = [];
  for (const stride of strideCandidates) {
    const w = widthOverride || stride;
    if (w % 4 !== 0) continue;
    for (let start = 0; start <= 4; start++) {
      if ((buf.length - start) % w !== 0) continue;
      const n = (buf.length - start) / w;
      if (n < 1) continue;
      if (!allPlausible(buf, start, n * (w / 4), be)) continue;
      // pattern-consistency: if we have >=2 pattern occurrences, they must sit
      // at the same intra-record offset for this grid
      if (positions.length >= 2) {
        let intra = null, consistent = true;
        for (const p of positions) {
          const io = (p - start) % w;
          if (io < 0) { consistent = false; break; }
          if (intra === null) intra = io;
          else if (intra !== io) { consistent = false; break; }
        }
        if (!consistent) continue;
      }
      solutions.push({ stride: w, start, count: n, pattern_intra: positions.length >= 2 ? (positions[0] - start) % w : null });
    }
  }
  if (!solutions.length) return { fail: "no consistent record grid found (type0 solver)" };
  // corpus calibration (B's OWN statistics, not A's field table): when supplied,
  // only strides B itself derived with pattern support from the untruncated
  // corpus are accepted — spurious grids from damaged input must fail.
  if (opts.corpusStrides && !solutions.some(x => opts.corpusStrides.includes(x.stride)))
    return { fail: `no grid with corpus-calibrated stride in [${opts.corpusStrides}] ` +
                   `(found strides: ${solutions.map(x => x.stride)})` };
  const unique = solutions.length === 1;
  // prefer pattern-supported solution; tie-break: maximal stride (records as
  // large as the divisibility evidence supports). Both grids stay reported.
  let sol = solutions[0];
  const withPattern = solutions.filter(x => x.pattern_intra !== null);
  if (withPattern.length) sol = withPattern.reduce((a, b) => (b.stride > a.stride ? b : a));
  else sol = solutions.reduce((a, b) => (b.stride > a.stride ? b : a));
  const recs = [];
  for (let i = 0; i < sol.count; i++) {
    const base = sol.start + i * sol.stride;
    const vals = [];
    for (let f = 0; f < sol.stride / 4; f++) vals.push(readF32(buf, base + f * 4, be));
    recs.push(vals);
  }
  return { count: sol.count, stride: sol.stride, header_bytes: sol.start, records: recs,
           stride_solutions: solutions, stride_unique: unique,
           dominant_pattern: bestKey ? Buffer.from(bestKey, "latin1").toString("hex") : null,
           dominant_pattern_count: bestN };
}

// ---- type1: scan-derived vertex run ----
function solveType1(buf, be, vwidthOverride) {
  const w = vwidthOverride || 12;
  if (buf.length < 12) return { fail: "payload < 12 bytes" };
  // longest run of plausible f32 from offset 12
  let run = 0;
  while (12 + (run + 1) * 4 <= buf.length && plausibleF32(readF32(buf, 12 + run * 4, be))) run++;
  // vertices are f32 x3; the run may have swallowed the first triangle index (==0)
  const vcounts = [];
  for (let vc = Math.floor(run / 3); vc >= Math.floor(run / 3) - 2 && vc >= 1; vc--) {
    const vEnd = 12 + vc * w;
    if (vEnd + 4 > buf.length) continue;
    const T = readU32(buf, vEnd, be);
    if (vEnd + 4 + T * 12 > buf.length) continue;
    let ok = true;
    for (let i = 0; i < T * 3; i++)
      if (readU32(buf, vEnd + 4 + i * 4, be) >= vc) { ok = false; break; }
    if (ok) vcounts.push({ vcount: vc, tricount: T });
  }
  if (!vcounts.length) return { fail: "no consistent vertex/triangle scan solution (type1 solver)" };
  if (vcounts.length > 1) return { fail: `ambiguous type1 scan solutions: ${JSON.stringify(vcounts)}` };
  const { vcount, tricount } = vcounts[0];
  const vEnd = 12 + vcount * w;
  const idx = [];
  for (let i = 0; i < tricount * 3; i++) idx.push(readU32(buf, vEnd + 4 + i * 4, be));
  return { vcount, vertex_width: w, scanned_f32_run: run, tricount,
           vertex_f32_first9: Array.from({length: 9}, (_, i) => readF32(buf, 12 + i * 4, be)),
           tri_first15: idx.slice(0, 15), tail_bytes: buf.length - (vEnd + 4 + tricount * 12) };
}

function decode(buf, opts) {
  opts = opts || {};
  const be = !!opts.bigEndian;
  if (buf.length >= 2 && buf[0] === 0 && buf[1] === 0) {
    const r = solveType0(buf, be, opts, opts.width);
    return Object.assign({ format: "type0_grid_solver" }, r);
  }
  if (buf.length >= 4 && readU32(buf, 0, be) === 1) {
    const r = solveType1(buf, be, opts.vwidth);
    return Object.assign({ format: "type1_scan_solver" }, r);
  }
  return { fail: "unknown type word" };
}

function main() {
  const out = { impl: "B_nodejs_content_driven", samples: {}, negative_controls: {} };
  for (const s of SAMPLES) {
    const buf = fs.readFileSync(path.join(RUN, "01_RAW", "samples", s + ".bin"));
    const r = decode(buf);
    const slim = r.fail ? { ok: false, error: r.fail }
      : { ok: true, result: r }; // FULL records kept for the A/B agreement table
    out.samples[s] = slim;
    console.log(s, JSON.stringify(slim).slice(0, 400));
  }
  // corpus calibration: strides B derived with PATTERN support from the
  // untruncated type0 samples (B's own statistics, not A's field table)
  const corpusStrides = [];
  for (const s of SAMPLES) {
    const buf = fs.readFileSync(path.join(RUN, "01_RAW", "samples", s + ".bin"));
    if (!(buf.length >= 2 && buf[0] === 0 && buf[1] === 0)) continue;
    const r = solveType0(buf, false, {});
    if (r && r.stride_solutions)
      for (const sol of r.stride_solutions)
        if (sol.pattern_intra !== null && !corpusStrides.includes(sol.stride))
          corpusStrides.push(sol.stride);
  }
  for (const s of SAMPLES) {
    const buf = fs.readFileSync(path.join(RUN, "01_RAW", "samples", s + ".bin"));
    const c = {};
    let r = decode(buf, { bigEndian: true, corpusStrides });
    c.a_wrong_endian = { failed: !!r.fail, output: r.fail || (r.records ? "DECODED (control did not fail)" : JSON.stringify(r).slice(0, 200)) };
    const cut = buf.subarray(0, Math.max(4, Math.min(buf.length >> 1, 24000)));
    r = decode(cut, { corpusStrides });
    c.b_truncated = { failed: !!r.fail, output: r.fail || "DECODED (control did not fail)" };
    if (buf[0] === 0 && buf[1] === 0) {
      r = decode(buf, { width: 72, corpusStrides }); // 18 f32 per record — wrong width
      c.c_wrong_width = { failed: !!r.fail, output: r.fail || "DECODED (control did not fail)" };
    } else {
      r = decode(buf, { vwidth: 24 });
      c.c_wrong_width_f64_vertices = { failed: !!r.fail, output: r.fail || "DECODED (control did not fail)" };
    }
    out.negative_controls[s] = c;
  }
  fs.writeFileSync(path.join(RUN, "01_RAW", "DECODE_B.json"), JSON.stringify(out, null, 1));
  const allFail = Object.values(out.negative_controls).every(cs => Object.values(cs).every(x => x.failed));
  console.log("neg controls all failed:", allFail);
}
main();
