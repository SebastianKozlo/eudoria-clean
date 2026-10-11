#!/usr/bin/env node
// PRIVATE probe: texture chain smoke test.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';
import { buildAssetIR } from '../../src/pecompat/PecSceneIR.js';
import { resolveAssetTextures } from '../../src/pecompat/PecTextureChain.js';

const mBytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const mArch = new Bnt2Archive(mBytes);
const tBytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt'));
const tArch = new Bnt2Archive(tBytes);
const texById = new Map(tArch.entries().map((e) => [parseInt(String(e.name), 10), e]));
const texByName = new Map(tArch.entries().map((e) => [String(e.name).toLowerCase(), e]));
const texLookup = (id) => {
  const e = texById.get(id);
  if (!e) return null;
  return { payload: tBytes.subarray(e.offset, e.offset + e.size) };
};
const nameLookup = (fn) => {
  for (const suffix of ['', '.dat', '.dds', '.tga']) {
    const e = texByName.get(String(fn).toLowerCase() + suffix);
    if (e) return { id: parseInt(String(e.name), 10), payload: tBytes.subarray(e.offset, e.offset + e.size) };
  }
  return null;
};

for (const [name, version, reader] of [
  ['223534.nif', 'v4', readNif41Corpus],
  ['505775.nif', 'v10', readNif10Corpus],
]) {
  const { payload } = mArch.readEntry(mArch.entryByName(name));
  const r = reader === readNif41Corpus ? readNif41Corpus(payload, { sourceName: name }) : readNif10Corpus(payload, { sourceName: name });
  const ir = buildAssetIR(r, { assetId: 1, era: 'PCG_9_3_5', build: 'probe', container: 'Models.bnt', entryName: name, payloadSha256: 'x', sizeBytes: payload.length, adapterVersion: 'probe', physicalSource: 'Models.bnt' });
  const t = resolveAssetTextures(ir, texLookup, nameLookup);
  console.log(`=== ${name} (${version}) state=${t.state} meshes=${t.meshCount} mapSlots=${t.mapSlots} exactSlots=${t.exactSlots} fallback=${JSON.stringify(t.fallback)}`);
  for (const mesh of t.results.slice(0, 3)) {
    console.log(`  mesh "${mesh.mesh}" state=${mesh.state}`);
    for (const s of mesh.slots.filter((x) => x.hasMap).slice(0, 3)) {
      console.log(`    slot ${s.slot}: ${s.state} method=${s.method} texId=${s.textureId} ${s.decode ? JSON.stringify(s.decode) : ''} ${s.note ? 'note=' + s.note : ''}`);
    }
  }
}
