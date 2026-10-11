// qc_recompute.mjs — INDEPENDENT mini-implementation for fresh internal QC of
// run PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011.
// PROVENANCE: authored by the separately-dispatched pe-master-auditor QC context
// (fresh internal QC). Implements the two contract §7 cases (and the §6 O3 sample
// arithmetic) DIRECTLY FROM THE CONTRACT TEXT. It does NOT import placement_probe.mjs
// or any executor analysis code — only node:crypto for fixture hashing.
// Case A: 10007-byte 0xFF buffer, maxHeader=0, strides 12..512 step 4
//   -> visited (source,header,stride) attempts, admitted layouts (divisibility+minRows).
// Case B: 80-row fixture (header 16, stride 32; u16 ID 4057/4058 alternating at +0;
//   f32 base row*3+axis*100+1 at +4/+8/+12; 8 NaN per axis in rows 0..7/8..15/16..23;
//   remaining bytes 0xFF) -> per-axis finite rates, complete finite triples, legacy
//   column mean (in-range rates, posLo=-200000/posHi=200000), ID rate.
// Case C: 4800-row table, valid IDs only at rows i%4===2; the ORIGINAL R1 sampler
//   formula floor((j+0.5)*n/rows) with n=4800, rows=1200 -> sample indices; sample ID
//   rate vs full-table ID rate.
import { createHash } from 'node:crypto';
const sha256 = b => createHash('sha256').update(b).digest('hex');
const out = { tool: 'QC_RECOMPUTE_INDEPENDENT_MINIPARSER', node: process.version, cases: {} };

// ---- Case A: LAYOUT_ATTEMPTS_VS_ADMITTED -------------------------------
{
  const buf = Buffer.alloc(10007, 0xff);
  const maxHeader = 0, minRows = 8;
  let attempts = 0, admitted = 0;
  const divisors = [];
  for (let h = 0; h <= maxHeader; h += 4) {
    for (let s = 12; s <= 512; s += 4) {
      attempts++;                                   // visited BEFORE any filter (contract §8)
      if ((buf.length - h) % s !== 0) continue;     // divisibility filter
      const N = (buf.length - h) / s;
      if (N < minRows) continue;                    // minRows filter
      admitted++; divisors.push(s);
    }
  }
  // independent primality check of 10007 (trial division, not assumed from the contract)
  let prime = true, witness = null;
  if (10007 % 2 === 0) { prime = false; witness = 2; }
  for (let d = 3; d * d <= 10007; d += 2) if (10007 % d === 0) { prime = false; witness = d; break; }
  out.cases.S7a_LAYOUT = {
    bufferBytes: buf.length, bufferSha256: sha256(buf), prime10007: { prime, witness },
    strideCount: (512 - 12) / 4 + 1, layoutAttempts: attempts, layoutsAdmitted: admitted, divisors,
  };
}

// ---- Case B: XYZ_COLUMN_MEAN_VS_ROW_TRIPLE_RATE -----------------------
{
  const rows = 80, header = 16, stride = 32;
  const b = Buffer.alloc(header + rows * stride, 0xff);
  for (let i = 0; i < rows; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(i % 2 === 0 ? 4057 : 4058, x);          // alternating ID at +0
    for (let a = 0; a < 3; a++) {
      const nanLo = a === 0 ? 0 : a === 1 ? 8 : 16, nanHi = nanLo + 7;  // rows 0..7/8..15/16..23
      if (i >= nanLo && i <= nanHi) b.writeFloatLE(NaN, x + 4 + a * 4);
      else b.writeFloatLE(i * 3 + a * 100 + 1, x + 4 + a * 4);          // base value
    }
  }
  const posLo = -200000, posHi = 200000;
  const perAxis = [], inRangeRates = [];
  for (let a = 0; a < 3; a++) {
    let finite = 0, nan = 0, inRange = 0;
    for (let i = 0; i < rows; i++) {
      const v = b.readFloatLE(header + i * stride + 4 + a * 4);
      if (Number.isNaN(v)) nan++;
      else if (Number.isFinite(v)) { finite++; if (v >= posLo && v <= posHi) inRange++; }
    }
    perAxis.push({ finite, nan, finiteRate: finite / rows, inRangeRate: inRange / rows });
    inRangeRates.push(inRange / rows);
  }
  let completeTriples = 0, completeInRange = 0;
  for (let i = 0; i < rows; i++) {
    let allFin = true, allInRange = true;
    for (let a = 0; a < 3; a++) {
      const v = b.readFloatLE(header + i * stride + 4 + a * 4);
      if (!Number.isFinite(v)) allFin = false;
      else if (!(v >= posLo && v <= posHi)) allInRange = false;
    }
    if (allFin) completeTriples++;
    if (allFin && allInRange) completeInRange++;
  }
  let idHits = 0; const idSet = new Set([4057, 4058]);
  for (let i = 0; i < rows; i++) if (idSet.has(b.readUInt16LE(header + i * stride))) idHits++;
  out.cases.S7b_XYZ = {
    fixtureSha256: sha256(b), rows, header, stride,
    perAxisFinite: perAxis.map(a => a.finite), perAxisFiniteRates: perAxis.map(a => a.finiteRate),
    perAxisNan: perAxis.map(a => a.nan),
    columnMeanInRangeRate: inRangeRates.reduce((x, y) => x + y, 0) / 3, // legacy xyzRate semantics
    completeFiniteTriples: completeTriples, tripleRate: completeTriples / rows,
    completePosConformingTriples: completeInRange, idRate: idHits / rows,
  };
}

// ---- Case C: SAMPLE_VS_CENSUS arithmetic ------------------------------
{
  const rows = 4800, header = 16, stride = 32;
  const b = Buffer.alloc(header + rows * stride, 0xff);
  const idSet = new Set([4057, 4058]);
  for (let i = 0; i < rows; i++) {
    const x = header + i * stride;
    b.writeUInt16LE(i % 4 === 2 ? (i % 8 === 2 ? 4057 : 4058) : 49281, x); // valid only at i%4===2
    b.writeFloatLE(i * 0.25 + 1, x + 4); b.writeFloatLE(i * 0.5 - 20, x + 8); b.writeFloatLE(i * 0.125 + 3, x + 12);
  }
  const n = rows, sampleRows = Math.min(n, 1200);
  const sel = []; for (let j = 0; j < sampleRows; j++) sel.push(Math.floor((j + 0.5) * n / sampleRows)); // R1 sampler formula
  const selMod = [...new Set(sel.map(i => i % 4))];
  let sampleHits = 0; for (const i of sel) if (idSet.has(b.readUInt16LE(header + i * stride))) sampleHits++;
  let fullHits = 0; for (let i = 0; i < rows; i++) if (idSet.has(b.readUInt16LE(header + i * stride))) fullHits++;
  out.cases.O3_SAMPLE_VS_CENSUS = {
    fixtureSha256: sha256(b), tableRows: rows, sampleRows, sampleIndices: [sel[0], sel[1], sel[2], sel[3]], sampleIndexMod4: selMod,
    sampleIdRate: sampleHits / sampleRows, fullCensusIdRate: fullHits / rows,
    sampleIndexEqualsValidRows: sel.every(i => i % 4 === 2),
  };
}

console.log(JSON.stringify(out, null, 2));
