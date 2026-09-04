// era_probe.js — raw, assumption-free probe of pcg terrain.bnt footer/index
// ERA-VALIDATION ITER 019 (M1-E CLEAN_RUNTIME_FOUNDATION START R2)
// Read-only. No decoder assumptions: dump bytes, hex, structure candidates.
'use strict';
const fs = require('fs');

const PATH = process.argv[2] || 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';
const buf = fs.readFileSync(PATH);
const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
const len = buf.byteLength;
console.log('file:', PATH);
console.log('size:', len);

// last 32 bytes hex
const tail = buf.subarray(len - 32);
console.log('tail32:', tail.toString('hex').match(/../g).join(' '));

// ASCII of tail
console.log('tail32 ascii:', JSON.stringify(tail.toString('latin1')));

// candidate magics in last 16 bytes
for (let i = len - 16; i < len - 3; i++) {
  const m = dv.getUint32(i, true);
  const tag = buf.toString('latin1', i, i + 4);
  console.log(`  u32@${i} (LE): 0x${m.toString(16).padStart(8, '0')}  "${tag.replace(/[^\x20-\x7e]/g, '.')}"`);
}

// Look for 'BUNT' anywhere in the last 4096 bytes
const w = buf.subarray(Math.max(0, len - 4096));
for (let i = 0; i + 4 <= w.length; i++) {
  if (w[i] === 0x42 && w[i+1] === 0x55 && w[i+2] === 0x4e && w[i+3] === 0x54) {
    console.log('BUNT found at absolute offset:', (len - 4096 + i));
  }
}
// First 64 bytes (record framing?)
console.log('head64:', buf.subarray(0, 64).toString('hex').match(/../g).join(' '));
// u32 at 0..15
for (let i = 0; i < 12; i += 4) console.log(`  head u32@${i} LE:`, dv.getUint32(i, true));
