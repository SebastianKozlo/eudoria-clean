#!/usr/bin/env node
// PRIVATE probe: find inline v4-style type strings + structure in a file tail.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
const name = process.argv[2];
const from = parseInt(process.argv[3] ?? '0', 10);
const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const { payload } = archive.readEntry(archive.entryByName(name));
const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
const KNOWN = ['NiNode', 'NiTriShape', 'NiTriShapeData', 'NiTexturingProperty', 'NiMaterialProperty',
  'NiAlphaProperty', 'NiZBufferProperty', 'NiVertexColorProperty', 'NiStringExtraData',
  'NiArkTextureExtraData', 'NiArkImporterExtraData', 'NiArkAnimationExtraData',
  'NiArkViewportInfoExtraData', 'NiTextureEffect', 'NiParticleSystem', 'NiPSysData'];
let found = 0;
for (let p = from; p < payload.length - 8 && found < 40; p++) {
  const len = dv.getInt32(p, true);
  if (len > 0 && len < 64) {
    let ok = true; let s = '';
    for (let i = 0; i < len; i++) {
      const b = payload[p + 4 + i];
      if (b < 32 || b > 126) { ok = false; break; }
      s += String.fromCharCode(b);
    }
    if (ok && KNOWN.includes(s)) {
      console.log(`@${p}: inline type "${s}" (len ${len})`);
      found++;
    }
  }
}
// footer scan
for (let p = payload.length - 8; p < payload.length - 4; p++) {
  const n = dv.getUint32(p, true);
  if (p + 4 + 4 * n === payload.length) console.log(`FOOTER @${p}: ntop=${n}`);
}
console.log('file size', payload.length);
