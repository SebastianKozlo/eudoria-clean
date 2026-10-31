// skin_probe.mjs — AV-5: byte-level layout discovery for NiSkinInstance /
// NiSkinData / NiSkinPartition in NIF 4.1.0.12 Models.ark members (era
// ISO_5_1_0_0). Read-only. Hypotheses verified against block spans (opaque
// anchored boundaries from the R1 4.1 reader) — closure-exact only.
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel41 } from '../../src/pesource/NifModelReader41.js';

const MODELS = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const mbuf = new Uint8Array(await fs.readFile(MODELS));
const ark = new ArkArchive(mbuf);

function hexAt(dv, u8, p, n) {
  let h = '';
  for (let i = 0; i < n; i++) h += u8[p + i].toString(16).padStart(2, '0') + (i % 4 === 3 ? ' ' : '');
  return h;
}

let found = 0;
const LIMIT = 6;
for (const e of ark.entries()) {
  if (!/\.nif$/i.test(e.name)) continue;
  const { payload } = ark.readEntry(e);
  const nl = payload.indexOf(0x0a);
  if (nl < 0) continue;
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  if (dv.getUint32(nl + 1, true) !== 0x0401000C) continue;
  let ex;
  try { ex = parseModel41(payload, e.name); } catch { continue; }
  const inst = ex.extraction.blocks.filter(b => b.type === 'NiSkinInstance');
  if (!inst.length) continue;
  found++;
  console.log(`\n=== ${e.name} (id ${e.name.match(/\d+/)[0]}) — ${inst.length} NiSkinInstance`);
  for (const b of ex.extraction.blocks.filter(x => x.type.startsWith('NiSkin'))) {
    console.log(`  ${b.type} #${b.index} rttiStart=${b.rttiStart} span=${b.span}`);
    // dump first 160 bytes after the RTTI string
    const dvB = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
    const rttiLen = dvB.getInt32(b.rttiStart, true);
    const p0 = b.rttiStart + 4 + rttiLen;
    console.log('    head: ' + hexAt(dvB, payload, p0, Math.min(160, b.rttiStart + b.span - p0)));
  }
  // shapes with skinRef
  for (const sh of ex.renderModel.shapes) {
    if (sh.skinRef >= 0) console.log(`  shape ${sh.shapeName} skinRef=${sh.skinRef} verts=${sh.numVertices}`);
  }
  if (found >= LIMIT) break;
}
console.log(`\nscanned, found ${found} skinned models (limit ${LIMIT})`);
