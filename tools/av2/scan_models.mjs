// scan_models.mjs — AV-2 offline census (read-only): parse EVERY Models.ark
// member with the W09 4.1 adapter, count parse outcomes / texture joins /
// NiUV controllers, resolve textures against Textures.ark. Evidence only —
// no repo writes; output JSON to the path given as argv[2].
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel41, NIF_V4_1_0_12 } from '../../src/pesource/NifModelReader41.js';

const MODELS = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const TEXTURES = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Textures.ark';
const out = process.argv[2];

const mbuf = new Uint8Array(await fs.readFile(MODELS));
const ark = new ArkArchive(mbuf);
const entries = ark.entries();
console.log('entries', entries.length);
const tbuf = new Uint8Array(await fs.readFile(TEXTURES));
const texArk = new ArkArchive(tbuf);
texArk.entries();

function extractName(payload, rttiStart) {
  try {
    const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
    const rl = dv.getInt32(rttiStart, true);
    if (rl < 1 || rl > 256) return null;
    const np = rttiStart + 4 + rl;
    const nl = dv.getInt32(np, true);
    if (nl < 0 || nl > 1024 || np + 4 + nl > payload.length) return null;
    let s = '';
    for (let i = 0; i < nl; i++) s += String.fromCharCode(payload[np + 4 + i]);
    return s;
  } catch { return null; }
}

const census = { total: entries.length, v41: 0, unsupportedVersion: 0, parseFail: 0, stopped: 0, pass: 0, withTextures: 0, textureJoins: 0, texResolved: 0, texUnresolved: 0, uvControllers: 0, withUVController: 0, kfControllerBlocks: 0 };
const models = [];
const texCandidates = [], animCandidates = [], renderLeads = [];
for (const e of entries) {
  const rec = { id: e.name.replace(/\.nif$/i, ''), name: e.name, size: e.size };
  const { payload } = ark.readEntry(e);
  const nl = payload.indexOf(0x0a);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ver = nl >= 0 ? dv.getUint32(nl + 1, true) : null;
  if (ver !== NIF_V4_1_0_12) { census.unsupportedVersion++; rec.status = `UNSUPPORTED_VERSION_0x${ver?.toString(16)}`; models.push(rec); continue; }
  census.v41++;
  try {
    const { extraction, renderModel } = parseModel41(payload, e.name);
    rec.status = extraction.parseStatus ?? 'PASS';
    if (rec.status !== 'PASS') census.stopped++; else census.pass++;
    rec.shapes = renderModel.shapes.length;
    rec.opaque = extraction.opaqueBlocks.length;
    let joins = 0, resolved = 0, unresolved = 0;
    for (const sh of renderModel.shapes) {
      if (!sh.textureProp) continue;
      for (const slot of sh.textureProp.textures) {
        if (!slot || slot.has !== 1) continue;
        joins++;
        const blk = extraction.blocks[slot.source];
        if (blk && blk.type === 'NiSourceTexture' && !blk.fields) {
          const nm = extractName(payload, blk.rttiStart);
          const m = nm ? nm.match(/^(\d+)\.[^.]+$/i) : null;
          const tentry = m ? texArk.entryById(Number(m[1])) : (nm ? texArk.entryByName(nm) : null);
          if (tentry) resolved++; else unresolved++;
          rec.texName = nm;
        } else unresolved++;
      }
    }
    rec.texJoins = joins; rec.texResolved = resolved; rec.texUnresolved = unresolved;
    census.textureJoins += joins; census.texResolved += resolved; census.texUnresolved += unresolved;
    if (joins > 0) { census.withTextures++; if (texCandidates.length < 12) texCandidates.push({ id: rec.id, joins, resolved }); }
    const uv = renderModel.controllers.filter(c => c.type === 'NiUVController');
    rec.uvControllers = uv.length;
    census.uvControllers += uv.length;
    if (uv.length > 0) { census.withUVController++; if (animCandidates.length < 12) animCandidates.push({ id: rec.id, uv: uv.length }); }
    if (renderModel.shapes.length > 0 && rec.status === 'PASS' && renderLeads.length < 40) {
      renderLeads.push({ id: rec.id, shapes: rec.shapes, verts: renderModel.shapes.reduce((a, s) => a + s.numVertices, 0), joins, resolved, uv: uv.length, size: e.size });
    }
    const kf = (extraction.blocks ?? []).filter(b => b.type === 'NiKeyframeController').length;
    census.kfControllerBlocks += kf;
  } catch (err) {
    census.parseFail++; rec.status = `PARSE_FAIL: ${String(err.message ?? err).slice(0, 80)}`;
  }
  models.push(rec);
}
console.log(JSON.stringify(census, null, 2));
await fs.writeFile(out, JSON.stringify({ census, texCandidates, animCandidates, renderLeads, models }, null, 1));
console.log('written', out);
