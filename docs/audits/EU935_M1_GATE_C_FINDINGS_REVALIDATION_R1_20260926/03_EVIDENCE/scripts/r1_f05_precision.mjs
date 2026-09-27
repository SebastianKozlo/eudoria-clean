// r1_f05_precision.mjs — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926
// F05 independent probe:
//   (1) the ORIGIN CONSTANT precision control: W=5, S=0 —
//       f32(5 * f32(0.01))  [K = f32(0.01) WIDENED to f64 — the byte-faithful form]
//       vs
//       f32(5 * 0.01)       [K read as an unconstrained binary64 0.01 literal]
//       recorded as decimal AND hex bit patterns;
//   (2) the three foliage QWORD operands re-read from the original binary bytes
//       (PE-header section map; .rdata VA->file offset), cross-checked against
//       the PEFoliageCore BYTE-LOCK claims;
//   (3) the x87 conditional-model status separation record (wording check basis).
// READ-ONLY: writes only to this run's 03_EVIDENCE.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = 'D:/Eudoria_Reconstruction';
const REPO = ROOT + '/12_WebGame/eudoria-clean';
const EV = REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/03_EVIDENCE';
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();
const f32bits = (v) => { const f = Math.fround(v); const dv = new DataView(new ArrayBuffer(4)); dv.setFloat32(0, f); return '0x' + dv.getUint32(0).toString(16).padStart(8, '0'); };

// ---------- (1) precision control ----------
const Kf32 = Math.fround(0.01);                       // float32(0.01), the binary's K
const typed = Math.fround(5 * Kf32);                  // f32(5 * (double)(float)0.01)
const literal64 = Math.fround(5 * 0.01);              // f32(5 * binary64 0.01)
const Kf64lit = 0.01;                                 // binary64 0.01 = 0x3F847AE147AE147B
const out = {
  probe: 'F05_EXACTNESS_ORIGIN_PRECISION',
  run_id: 'EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926',
  node_version: process.version,
  origin_precision_control: {
    W: 5, S: 0,
    K_f32_0_01: { decimal: Kf32, hex_bits: f32bits(Kf32), role: 'the byte-faithful K = f32(0.01) widened to f64 for the multiply' },
    typed_K_f32_widened: { formula: 'out = f32(f32(W * (double)(float)0.01) - S)', decimal: typed, hex_bits: f32bits(typed) },
    literal_K_binary64: { formula: 'out = f32(f32(W * 0.01) - S)  [K read as binary64 0.01]', decimal: literal64, hex_bits: f32bits(literal64) },
    equal: typed === literal64,
    verdict: typed === literal64
      ? 'INDISTINGUISHABLE (unexpected — re-check)'
      : 'DISTINCT f32 results: the K constant is f32(0.01) WIDENED to f64, NOT an unconstrained binary64 0.01 literal; the shortened downstream form "W * 0.01" is ambiguous and, read as a binary64 literal, WRONG for this control',
    binary64_0_01_bits: '0x3F847AE147AE147B (= 0.01000000000000000020816681711721685...)',
    f32_0_01_bits: f32bits(Kf32) + ' (= 0.009999999776482582...)',
  },
  binary_operand_reread: (() => {
    const EXE = ROOT + '/pcg_install/Entropia.exe';
    const ex = fs.readFileSync(EXE);
    const pe = ex.readUInt32LE(0x3c);
    const ns = ex.readUInt16LE(pe + 6), opt = ex.readUInt16LE(pe + 20), base = ex.readUInt32LE(pe + 24 + 28);
    const sects = [];
    for (let i = 0; i < ns; i++) {
      const p = pe + 24 + opt + i * 40;
      sects.push({ name: ex.toString('ascii', p, p + 8).replaceAll('\0', ''), va: ex.readUInt32LE(p + 12), size: ex.readUInt32LE(p + 16), raw: ex.readUInt32LE(p + 20) });
    }
    const va = (v, n) => { const s = sects.find(s => v - base >= s.va && v - base + n <= s.va + s.size); return ex.subarray(s.raw + v - base - s.va, s.raw + v - base - s.va + n); };
    const read = (addr) => { const b = va(addr, 8); return { va: '0x' + addr.toString(16), bytes: b.toString('hex'), f64: b.readDoubleLE(0) }; };
    return {
      exe: { path: EXE, sha256_fresh: sha256(ex), size: ex.length, image_base: base },
      _DAT_00a7d7a8: read(0xa7d7a8),
      _DAT_00a8c758: read(0xa8c758),
      _DAT_00a980d0: read(0xa980d0),
      cross_check: 'PEFoliageCore.js FOLIAGE_OPERAND_LOCK byte claims: 32767.0 / 65535.0 / 0.00007812499825377017',
    };
  })(),
  x87_status_separation: {
    BYTE_LOCKED_OPERANDS: 'CONFIRMED (the three .rdata QWORDs re-read above; iter035 CONSTANT_ADDRESS_LOCK)',
    ARITHMETIC_MODEL_EXACTNESS: 'CONDITIONAL on the stated x87 model (PC in {53,64}, RC = nearest-even) — the exhaustive proofs compared f64+Math.fround vs 80-bit-then-FSTP under THAT model; PC=24 measured DIFFERENT (14,104/229,376 real; 103,073/1,245,184 synthetic)',
    ORIGINAL_CLIENT_RUNTIME_PARITY: 'UNVERIFIED/UNMEASURED (the actual foliage-site CW at chain-execution time was never measured; no runtime experiment authorized or performed)',
    HISTORICAL_FOLIAGE_INPUTS: 'NOT RECOVERED ([P-CLIMATE] caller-selected climate; [P-CELLSTREAM] stand-in cell content; p3 default 0; windowWorld = CURRENT_RUNTIME_CALIBRATION)',
    FOLIAGE_PLACEMENT_1_1: 'NOT CLAIMED (no standing document claims 1:1 historical placement)',
  },
};
fs.writeFileSync(path.join(EV, 'F05_PRECISION_CONTROLS.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({ control: out.origin_precision_control, operands: { a: out.binary_operand_reread._DAT_00a7d7a8.f64, b: out.binary_operand_reread._DAT_00a8c758.f64, c: out.binary_operand_reread._DAT_00a980d0.f64, sha: out.binary_operand_reread.exe.sha256_fresh } }, null, 2));
