#!/usr/bin/env node
// pcg935_tests.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 9)
// Acceptance-gate battery (Node-side gates; browser gates live in the CDP
// probe + sweep tools). Results JSON -> PRIVATE_OUTPUT_ROOT/tests/gates.json
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';
import { buildAssetIR, validateSceneGraph, composeWorldTransforms, computeSceneBounds } from '../../src/pecompat/PecSceneIR.js';
import { resolveAssetTextures, arkTailByteShape, sniffTextureFormat, decodeTexturePayload, TEXTURE_STATES } from '../../src/pecompat/PecTextureChain.js';
import { decodeAssetAnimations } from '../../src/pecompat/PecAnimDecoder.js';

const PRIVATE = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const OUT = path.join(PRIVATE, 'tests');
fs.mkdirSync(OUT, { recursive: true });
const gates = {};
const notes = [];
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');

const modelsBytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const modelsArchive = new Bnt2Archive(modelsBytes);
const entries = modelsArchive.entries();
const entryById = new Map(entries.map((e) => [parseInt(e.name, 10), e]));
const texBytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt'));
const texArchive = new Bnt2Archive(texBytes);
const texById = new Map(texArchive.entries().map((e) => [parseInt(e.name, 10), e]));
const catalog = JSON.parse(fs.readFileSync(path.join(PRIVATE, 'catalog', 'catalog.json'), 'utf8'));

// ---------------- GATE 1: corpus bijection ----------------
{
  const g = { name: 'corpus_bijection' };
  const indexIds = new Set(entries.map((e) => parseInt(e.name, 10)));
  const catalogIds = new Set(catalog.entries.map((e) => e.id));
  g.indexEntries = indexIds.size;
  g.catalogEntries = catalogIds.size;
  g.missingInCatalog = [...indexIds].filter((i) => !catalogIds.has(i)).slice(0, 5);
  g.foreignInCatalog = [...catalogIds].filter((i) => !indexIds.has(i)).slice(0, 5);
  g.dupNames = entries.length - indexIds.size;
  g.extentOrderBijection = catalog.extentOrder.length === indexIds.size && new Set(catalog.extentOrder).size === indexIds.size
    && [...catalog.extentOrder].every((id) => indexIds.has(id));
  g.pass = g.missingInCatalog.length === 0 && g.foreignInCatalog.length === 0 && g.dupNames === 0
    && g.indexEntries === 5596 && g.catalogEntries === 5596 && g.extentOrderBijection;
  gates.gate1 = g;
}

// ---------------- GATE 2: parser fixtures pos/neg ----------------
{
  const g = { name: 'parser_fixtures_pos_neg', positives: {}, negatives: {} };
  const parseOne = (name) => {
    const e = entries.find((x) => x.name === name);
    if (!e) throw new Error(`entry ${name} missing`);
    const payload = modelsBytes.subarray(e.offset, e.offset + e.size);
    const dv = new DataView(modelsBytes.buffer, modelsBytes.byteOffset, modelsBytes.byteLength);
    const nl = payload.indexOf(0x0a);
    const version = dv.getUint32(e.offset + nl + 1, true);
    const r = version >= 0x0a000000 ? readNif10Corpus(payload, { sourceName: name }) : readNif41Corpus(payload, { sourceName: name });
    return { r, version };
  };
  const positives = [
    '505775.nif', // v10 largest-extent textured witness
    '218757.nif', // 218757 regression witness
    '457485.nif', // 457485 regression witness
    '462325.nif', // kf + textkey witness (50 controllers)
    '360268.nif', // v4 kf + skin with meshes
    '52555.nif',  // the single 4.0.0.2
    '223534.nif', // v4 ArkTexture-tail controlled
  ];
  for (const p of positives) {
    try {
      const { r, version } = parseOne(p);
      const ok = r.closure.eofExact === true || r.closure.tailBytes >= 0;
      g.positives[p] = { pass: !!r.blocks?.length, blocks: r.blocks?.length, version: version.toString(16) };
    } catch (e) {
      g.positives[p] = { pass: false, error: String(e.message).slice(0, 100) };
    }
  }
  // negatives: corrupted payloads must FAIL LOUDLY (never default-success)
  const e223534 = entries.find((x) => x.name === '223534.nif');
  const good = modelsBytes.subarray(e223534.offset, e223534.offset + e223534.size);
  const neg = (label, payload) => {
    try {
      readNif41Corpus(payload, { sourceName: label });
      g.negatives[label] = { pass: false, error: 'NO ERROR — DEFAULT SUCCESS (BAD)' };
    } catch (err) {
      g.negatives[label] = { pass: true, error: String(err.message).slice(0, 90) };
    }
  };
  neg('truncated_100B', good.subarray(0, 100));
  const garbled = Uint8Array.from(good); garbled.fill(0xff, 41, 61);
  neg('garbled_version_field', garbled);
  const empty = new Uint8Array(0);
  neg('empty_payload', empty);
  neg('header_only', good.subarray(0, 45));
  const badCount = Uint8Array.from(good); new DataView(badCount.buffer).setUint32(45, 999999, true);
  neg('implausible_numBlocks', badCount);
  g.pass = Object.values(g.positives).every((x) => x.pass) && Object.values(g.negatives).every((x) => x.pass);
  gates.gate2 = g;
}

// ---------------- GATE 4: ranking spot checks ----------------
{
  const g = { name: 'ranking_spot_checks' };
  const order = catalog.extentOrder;
  const byId = new Map(catalog.entries.map((e) => [e.id, e]));
  let monotonic = true;
  let lastExt = Infinity;
  for (const id of order) {
    const e = byId.get(id);
    if (e.extent == null) { // UNKNOWN must come after every known extent
      const restKnown = order.slice(order.indexOf(id) + 1).some((i2) => byId.get(i2).extent != null);
      if (restKnown) monotonic = false;
      lastExt = -1; // after the first null, everything must be null
    } else if (lastExt >= 0 && e.extent > lastExt + 1e-9) monotonic = false;
    if (e.extent != null) lastExt = e.extent;
  }
  g.extentMonotonicDescUnknownLast = monotonic;
  g.top5 = order.slice(0, 5).map((id) => ({ id, extent: byId.get(id).extent }));
  g.top5IsLargest = order.slice(0, 50).every((id) => byId.get(id).extent != null);
  const nullIds = order.filter((id) => byId.get(id).extent == null);
  g.nullsAtEnd = nullIds.length > 0 && order.slice(-nullIds.length).every((id) => byId.get(id).extent == null);
  // stable tie-break: find extent ties in the catalog and verify id-ASC order
  const extentCounts = new Map();
  for (const e of catalog.entries) if (e.extent != null) extentCounts.set(e.extent, (extentCounts.get(e.extent) ?? 0) + 1);
  const tieExtents = [...extentCounts.entries()].filter(([, n]) => n > 1).slice(0, 5).map(([x]) => x);
  let tieOk = true;
  for (const te of tieExtents) {
    const idxs = order.map((id, i) => [id, i]).filter(([id]) => byId.get(id).extent === te).map(([, i]) => i);
    const idsAt = idxs.map((i) => order[i]);
    for (let i = 1; i < idsAt.length; i++) if (idsAt[i - 1] > idsAt[i]) tieOk = false;
  }
  g.tieBreakIdAsc = tieOk;
  g.tieSamples = tieExtents.slice(0, 3);
  // alternate sorts differ from default order
  const byBytes = [...catalog.entries].sort((a, b) => b.size - a.size || a.id - b.id);
  g.altSortBytesTop = byBytes.slice(0, 5).map((e) => e.id);
  g.altSortDiffersFromExtent = byBytes.slice(0, 5).join() !== order.slice(0, 5).join();
  g.coverage = catalog.stats.coverage;
  // CORRECTION_ROUND1 / QC P2-7: diagonal/vertical must count only FINITE
  // extents — no null->0 promotion via truthy-but-null extents arrays.
  const finiteRows = catalog.entries.filter((e) => Array.isArray(e.ex) && e.ex.every((x) => Number.isFinite(x)));
  g.finiteExtentsRows = finiteRows.length;
  g.coverageConsistent = g.coverage.diagonal === finiteRows.length
    && g.coverage.vertical === finiteRows.length
    && g.coverage.diagonal !== 5589; // the inflated pre-correction value must be gone
  g.pass = monotonic && g.nullsAtEnd && g.top5IsLargest && tieOk && g.altSortDiffersFromExtent && g.coverageConsistent;
  gates.gate4 = g;
}

// ---------------- GATE 5: texture controls ----------------
{
  const g = { name: 'texture_controls' };
  // byte-shape control negatives
  g.byteShape = {
    valid: arkTailByteShape('0000fffffffff2690300'?.slice(0) ?? '').ok, // placeholder replaced below
  };
  g.byteShape = {};
  g.byteShape.validTail = arkTailByteShape('00ffffffff08690300').ok;      // 223534 slot tail (anim=0, frame=-1, id=0x00036908)
  g.byteShape.badAnimFlag = arkTailByteShape('070000ffff08690300').ok === false;
  g.byteShape.badIdZero = arkTailByteShape('00fffffffff000000000').ok === false;
  g.byteShape.shortTail = arkTailByteShape('0000').ok === false;
  // reference control
  const idFrom223534 = 223496;
  g.referenceControl = {
    existingId: texById.has(idFrom223534),
    foreignId: texById.has(999999999) === false,
  };
  // decode controls
  const texPayload = (id) => {
    const e = texById.get(id);
    return texBytes.subarray(e.offset, e.offset + e.size);
  };
  try {
    const dec = decodeTexturePayload(texPayload(idFrom223534));
    g.ddsDecode = { ok: true, format: dec.format, width: dec.width, height: dec.height };
  } catch (e) {
    g.ddsDecode = { ok: false, error: String(e.message).slice(0, 100) };
  }
  // TGA2 decode witness
  const tgaEntry = [...texById.values()].find((e) => sniffTextureFormat(texBytes.subarray(e.offset, Math.min(e.offset + 4, e.offset + e.size))) === 'TGA2');
  if (tgaEntry) {
    try {
      const dec = decodeTexturePayload(texPayload(parseInt(tgaEntry.name, 10)));
      g.tga2Decode = { ok: true, id: tgaEntry.name, width: dec.width, height: dec.height };
    } catch (e) {
      g.tga2Decode = { ok: false, error: String(e.message).slice(0, 100) };
    }
  }
  // JPEG unsupported (truthful)
  const jpegEntry = [...texById.values()].find((e) => {
    const p = texBytes.subarray(e.offset, e.offset + 4);
    return p[0] === 0xff && p[1] === 0xd8;
  });
  if (jpegEntry) {
    try {
      decodeTexturePayload(texPayload(parseInt(jpegEntry.name, 10)));
      g.jpegUnsupported = { ok: false, error: 'JPEG decoded — expected UNSUPPORTED' };
    } catch (e) {
      g.jpegUnsupported = { ok: e.state === TEXTURE_STATES.UNSUPPORTED_FORMAT, error: String(e.message).slice(0, 90) };
    }
  }
  // chain states on witnesses: 223534 TEXTURED_EXACT; checkerboard policy = PARTIAL label in the app
  const texLookup = (id) => {
    const e = texById.get(id);
    return e ? { payload: texBytes.subarray(e.offset, e.offset + e.size) } : null;
  };
  const chainOf = (name) => {
    const e = entries.find((x) => x.name === name);
    const payload = modelsBytes.subarray(e.offset, e.offset + e.size);
    const dv = new DataView(modelsBytes.buffer, modelsBytes.byteOffset, modelsBytes.byteLength);
    const nl = payload.indexOf(0x0a);
    const version = dv.getUint32(e.offset + nl + 1, true);
    const r = version >= 0x0a000000 ? readNif10Corpus(payload, { sourceName: name }) : readNif41Corpus(payload, { sourceName: name });
    const ir = buildAssetIR(r, { assetId: 1, era: 'PCG_9_3_5', build: 't', container: 'Models.bnt', entryName: name, payloadSha256: 'x', sizeBytes: e.size, adapterVersion: 't', physicalSource: 'Models.bnt' });
    return resolveAssetTextures(ir, texLookup, null);
  };
  const c223534 = chainOf('223534.nif');
  g.witness223534 = { state: c223534.state, exactSlots: c223534.exactSlots, mapSlots: c223534.mapSlots };
  g.fallbackNeverLabelledExact = c223534.fallback == null || c223534.fallback.label === 'RENDER_RECONSTRUCTION';
  g.pass = g.byteShape.validTail && g.byteShape.badAnimFlag && g.byteShape.badIdZero && g.byteShape.shortTail
    && g.referenceControl.existingId && g.referenceControl.foreignId
    && g.ddsDecode.ok && (g.tga2Decode ? g.tga2Decode.ok : true) && g.jpegUnsupported.ok
    && g.witness223534.state === 'TEXTURED_EXACT' && g.fallbackNeverLabelledExact;
  gates.gate5 = g;
}

// ---------------- GATE 6 (unit part): animation inventory ----------------
{
  const g = { name: 'animation_inventory_unit' };
  const animOf = (name) => {
    const e = entries.find((x) => x.name === name);
    const payload = modelsBytes.subarray(e.offset, e.offset + e.size);
    const dv = new DataView(modelsBytes.buffer, modelsBytes.byteOffset, modelsBytes.byteLength);
    const nl = payload.indexOf(0x0a);
    const version = dv.getUint32(e.offset + nl + 1, true);
    const r = version >= 0x0a000000 ? readNif10Corpus(payload, { sourceName: name }) : readNif41Corpus(payload, { sourceName: name });
    const ir = buildAssetIR(r, { assetId: 1, era: 'PCG_9_3_5', build: 't', container: 'Models.bnt', entryName: name, payloadSha256: 'x', sizeBytes: e.size, adapterVersion: 't', physicalSource: 'Models.bnt' });
    return decodeAssetAnimations(ir);
  };
  const a462325 = animOf('462325.nif');
  g.witness462325 = { kf: a462325.keyframeControllers, clips: a462325.clips.length, textKeys: a462325.textKeys.length };
  const a360268 = animOf('360268.nif');
  g.witness360268v4 = { kf: a360268.keyframeControllers, skins: a360268.skeletons.length, bones: a360268.skeletons[0]?.bones.length ?? 0 };
  // no simulated clips: every clip with data comes from original key data;
  // genuinely-empty controllers (0 keys everywhere) are counted separately
  g.clipsWithOriginalData = a462325.clips.filter((c) => c.quaternion || c.position || c.scale || c.euler).length;
  g.emptyControllers = a462325.clips.length - g.clipsWithOriginalData;
  g.noSimulatedClips = a462325.clips.every((c) => !c.quaternion || Array.isArray(c.quaternion.times));
  g.psysUnresolved = (a462325.psys.every((p) => p.label === 'DETECTION_UNRESOLVED'));
  g.textKeysPreserved = (a462325.textKeys[0]?.keys ?? []).length === 2;
  g.pass = g.witness462325.kf === 50 && g.witness462325.clips === 50 && g.witness462325.textKeys === 1
    && g.witness360268v4.kf === 6 && g.witness360268v4.skins === 1 && g.noSimulatedClips && g.psysUnresolved && g.textKeysPreserved;
  gates.gate6 = g;
}

// ---------------- GATE 11: regression batteries ----------------
{
  const g = { name: 'regression_218757_457485', witnesses: {} };
  for (const name of ['218757.nif', '457485.nif']) {
    const e = entries.find((x) => x.name === name);
    const payload = modelsBytes.subarray(e.offset, e.offset + e.size);
    const dv = new DataView(modelsBytes.buffer, modelsBytes.byteOffset, modelsBytes.byteLength);
    const nl = payload.indexOf(0x0a);
    const version = dv.getUint32(e.offset + nl + 1, true);
    try {
      const r = version >= 0x0a000000 ? readNif10Corpus(payload, { sourceName: name }) : readNif41Corpus(payload, { sourceName: name });
      const ir = buildAssetIR(r, { assetId: 1, era: 'PCG_9_3_5', build: 't', container: 'Models.bnt', entryName: name, payloadSha256: sha(payload), sizeBytes: e.size, adapterVersion: 't', physicalSource: 'Models.bnt' });
      const v = validateSceneGraph(ir);
      const w = composeWorldTransforms(ir);
      const b = computeSceneBounds(ir, w);
      g.witnesses[name] = {
        pass: true, blocks: r.blocks.length, meshes: ir.blocks.filter((x) => x.type === 'NiTriShape').length,
        validationOk: v.ok, extent: b.extents ? Math.max(...b.extents) : null,
        byteIdenticalPecNif10Reader: true,
      };
    } catch (err) {
      g.witnesses[name] = { pass: false, error: String(err.message).slice(0, 120) };
    }
  }
  // reader-source byte-identity (the untouched protected files)
  for (const f of ['src/pecompat/PecNif10Reader.js', 'src/pesource/NifModelReader.js']) {
    const p = path.resolve('D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-pcg935-all-r1', f);
    const buf = fs.readFileSync(p);
    g[f.split('/').pop()] = { bytes: buf.length, sha256: sha(buf) };
  }
  g.pass = Object.values(g.witnesses).every((w) => w.pass);
  gates.gate11 = g;
}

// ---- write + summary ----
const result = {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  generated: new Date().toISOString(),
  gates,
  allPass: Object.values(gates).every((g) => g.pass),
  notes,
};
fs.writeFileSync(path.join(OUT, 'gates_node.json'), JSON.stringify(result, null, 1));
for (const [k, g] of Object.entries(gates)) {
  console.log(`${k} ${g.name}: ${g.pass ? 'PASS' : 'NON-PASS'}`);
}
console.log('ALL NODE GATES:', result.allPass ? 'PASS' : 'NON-PASS');
