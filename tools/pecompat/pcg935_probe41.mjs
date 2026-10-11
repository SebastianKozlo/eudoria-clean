#!/usr/bin/env node
// PRIVATE probe: walk 223534.nif block-by-block at KNOWN positions to find the
// block whose parse consumes the wrong byte count.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import * as R41 from '../../src/pecompat/PecNif41Reader.js';

const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const { payload } = archive.readEntry(archive.entryByName('223534.nif'));
const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
const RTTI = [
  [49, 'NiNode'], [172, 'NiArkAnimationExtraData'], [256, 'NiArkTextureExtraData'],
  [344, 'NiArkImporterExtraData'], [435, 'NiTexturingProperty'], [509, 'NiMaterialProperty'],
  [601, 'NiZBufferProperty'], [640, 'NiTriShape'], [765, 'NiAlphaProperty'],
  [799, 'NiTriShapeData'],
];
for (const [pos, expected] of RTTI) {
  const len = dv.getInt32(pos, true);
  const name = String.fromCharCode(...payload.subarray(pos + 4, pos + 4 + len));
  console.log(`RTTI @${pos}: "${name}" (len ${len}) expected=${expected} ${name === expected ? 'OK' : 'MISMATCH'}`);
}
// Now parse each FIXED block from its payload start and report the end position.
const FIXED = [
  [49, 'NiNode', 172], [256, 'NiArkTextureExtraData', 344], [344, 'NiArkImporterExtraData', 435],
  [435, 'NiTexturingProperty', 509], [509, 'NiMaterialProperty', 601], [601, 'NiZBufferProperty', 640],
  [640, 'NiTriShape', 765], [765, 'NiAlphaProperty', 799], [799, 'NiTriShapeData', 940],
];
// reach the private parsers via a minimal re-implementation using the exported stream class
// (the parsers are module-private; replicate the essential walk via readNif41Corpus instead).
try {
  const r = R41.readNif41Corpus(payload, { sourceName: '223534.nif', debugTrace: [] });
  console.log('FULL PARSE OK');
} catch (e) {
  console.log('full parse fails:', e.message.slice(0, 160));
}
// parse ONLY block 7 (NiTriShape) region manually: dump bytes 654..770
for (let off = 654; off < 676; off += 16) {
  let hex = '';
  for (let i = 0; i < 16 && off + i < 772; i++) hex += payload[off + i].toString(16).padStart(2, '0') + ' ';
  console.log(off + ': ' + hex);
}
