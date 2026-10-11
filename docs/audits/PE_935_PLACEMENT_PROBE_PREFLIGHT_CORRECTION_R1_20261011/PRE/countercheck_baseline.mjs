// countercheck_baseline.mjs — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011
// AUDITOR_COUNTERCHECK (run-local, executor-side): INDEPENDENT mini-parser that
// recomputes the §6/§7 expected quantities DIRECTLY from the synthetic fixture
// bytes, WITHOUT importing either the original kit or the corrected kit.
// Lineage: separate implementation; reads only fixture builders (byte identity,
// not parsing logic). Writes PRE/COUNTERCHECK_BASELINE.json.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as FX from '../../../../tools/placement_probe/tests/fixtures.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const out = { tool: 'COUNTERCHECK_BASELINE_INDEPENDENT_MINIPARSER', cases: {} };

// §7 LAYOUT: strides 12..512 step 4, headers 0..0 → visited attempts
{
  const strides = []; for (let s = 12; s <= 512; s += 4) strides.push(s);
  const buf = FX.layoutBuffer10007();
  const divisible = strides.filter(s => buf.length % s === 0);
  out.cases.LAYOUT = {
    strideCountVisited: strides.length, headerCountVisited: 1,
    layoutAttemptsExpected: strides.length * 1, layoutsAdmittedExpected: divisible.length,
    bufferLength: buf.length, primalityNote: '10007 % s != 0 for all s in 12..512 (10007 is prime)',
  };
}

// §7 XYZ: recompute per-axis finite rates and joint triple rate from bytes
{
  const b = FX.xyzFixture80(); const header = 16, stride = 32, rows = 80;
  const axisFinite = [0, 0, 0]; let completeTriples = 0;
  for (let i = 0; i < rows; i++) {
    let allFin = true;
    for (let a = 0; a < 3; a++) {
      const v = b.readFloatLE(header + i * stride + 4 + a * 4);
      if (Number.isFinite(v)) axisFinite[a]++; else allFin = false;
    }
    if (allFin) completeTriples++;
  }
  const idOk = []; for (let i = 0; i < rows; i++) idOk.push([4057, 4058].includes(b.readUInt16LE(header + i * stride)) ? 1 : 0);
  out.cases.XYZ = {
    rowsExamined: rows, perAxisFinite: axisFinite.map(c => `${c}/80`), perAxisFiniteRate: axisFinite.map(c => c / rows),
    columnMeanRateExpected: axisFinite.reduce((a, c) => a + c / rows, 0) / 3,
    completeFiniteTriples: completeTriples, tripleRateExpected: `${completeTriples}/80`, tripleRateValue: completeTriples / rows,
    idColumnRateExpected: idOk.reduce((a, b) => a + b, 0) / rows,
  };
}

// O3 SAMPLE_VS_CENSUS: recompute sample (1200 evenly spread) vs full (4800) ID rate
{
  const b = FX.poisoned4800(); const header = 16, stride = 32, n = 4800;
  const ids = []; for (let i = 0; i < n; i++) ids.push(b.readUInt16LE(header + i * stride));
  const valid = v => v === 4057 || v === 4058;
  const full = ids.filter(valid).length;
  const rows = Math.min(n, 1200); const sel = [];
  for (let i = 0; i < rows; i++) sel.push(Math.floor((i + 0.5) * n / rows));
  const sample = sel.map(i => ids[i]).filter(valid).length;
  out.cases.SAMPLE_VS_CENSUS = {
    tableRows: n, sampleRows: sel.length, fullIdRateExpected: `${full}/${n}`, fullIdRateValue: full / n,
    sampleIdRateExpected: `${sample}/${sel.length}`, sampleIdRateValue: sample / sel.length,
    note: 'fixture: valid IDs only at rows i%4===2; original sample indices are 4j+2 (all valid) — sample rate 1.0 hides the 0.25 table quality',
  };
}
// O5 COUNTERS: recompute f32 subnormality of the u32 counters
{
  const b = FX.countersAsFloats(); const header = 16, stride = 32, rows = 80;
  let subnormal = 0, finite = 0, zero = 0; const firstVals = [];
  for (let i = 0; i < rows; i++) for (let a = 0; a < 3; a++) {
    const off = header + i * stride + 4 + a * 4;
    const u32 = b.readUInt32LE(off); const f = b.readFloatLE(off);
    const expBits = (u32 >>> 23) & 0xff; const mantissa = u32 & 0x7fffff;
    if (expBits === 0 && mantissa !== 0) subnormal++;
    if (Number.isFinite(f)) finite++; if (f === 0) zero++;
    if (i < 2 && a < 3) firstVals.push({ u32, asFloat: f });
  }
  out.cases.COUNTERS_AS_FLOATS = { examined: rows * 3, subnormalF32: subnormal, finiteF32: finite, zeroF32: zero, sample: firstVals, alternativeU32: [1, 1000, 5000] };
}

// FIX: huge.rec is only 2576 bytes — under the 4 MiB cap, so config A expectation:
// SCANNED: scan.rec + huge.rec = 2? No: huge.rec data IS good records (2576B) → scanned.
out.cases.CENSUS = {
  declaredEntries: 4,
  expectedByConstruction_configA: { SCANNED: 2, FILTERED_EXTENSION: 1, TOO_SMALL: 1, recordedByOriginal_skipRows: 0 },
  regexConfigB: { FILTERED_REGEX: 3, SCANNED: 1 },
  note: 'entries scan.rec(2576B,records) tex.nif(2576B,records,ext-skip) tiny.rec(8B,too-small) huge.rec(2576B,records); original records zero skip rows here — all four dispositions are silent except none; ENTRY_TOO_LARGE only if size > 4 MiB',
};

fs.writeFileSync(path.join(HERE, 'COUNTERCHECK_BASELINE.json'), JSON.stringify(out, null, 2) + '\n');
console.log('COUNTERCHECK_BASELINE.json written');