// phase3_pcg935_name_batch.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 3 (W4, contract §4)
// Bounded NAME_FOUND batch for the PCG_9_3_5 models that phase 2 already
// decoded with the era-validated reader: the 1,551 DECODED entries (incl.
// 218757) from PHASE2_EXTENT state. NO NEW DECODE: the existing
// PecNif10Reader is used as-is; failures are recorded per model and skipped.
//
// EDGE EXTRACTION (verified refs only, never order):
//   shape → propertyRefs → NiTexturingProperty → ArkTexture entries whose
//   texturingPropertyRef == that block (slot f1 kept RAW + lineage label
//   0=BASE 1=DARK 3=GLOSS 4=GLOW — labeled as the historical lineage reading)
//   shape → propertyRefs → NiTexturingProperty → slot.sourceRef →
//   NiSourceTexture → filename (when present)
// The per-entry 9-byte Ark tail is recorded RAW ONLY — NO textureId
// interpretation (the 218757 retraction stands; no new derivation here).
//
// NAME CATALOG: the PCG_9_3_5 Textures.bnt 8,381-entry catalog hashed in
// phase 2 (metadata only — names + SHAs from the phase-2 catalog CSV; no
// payloads). Cross-era discipline: this catalog resolves ONLY PCG_9_3_5
// references; dispositions are controlled and visible:
//   NAME_FOUND_EXACT              — name exactly equals a catalog entry name
//   NAME_BASE_MATCH_EXTENSION_DIFF — name base equals a catalog base with a
//                                    different extension (VISIBLE observation,
//                                    NOT a resolution)
//   NAME_NOT_FOUND                — no catalog match
// BROWSER_OBSERVED stays 0 until phase 4 (no browser render in this phase).
//
// OUTPUT: per-edge JSONL + summary → PRIVATE_OUTPUT only.

import fs from 'node:fs';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10 } from '../../src/pecompat/PecNif10Reader.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) args[key] = true;
      else { args[key] = next; i++; }
    }
  }
  return args;
}

const SLOT_LINEAGE_LABEL = (f1) => ({ 0: 'BASE', 1: 'DARK', 3: 'GLOSS', 4: 'GLOW' }[f1] ?? `F1_${f1}`);

async function main() {
  const args = parseArgs(process.argv);
  const bntPath = args.models;
  const statePath = args.state;
  const catalogCsv = args.catalog;
  const outJsonl = args['out-jsonl'];
  const outSummary = args['out-summary'];
  const expectSha = args['expect-sha'];
  const limit = args.limit ? parseInt(args.limit, 10) : Infinity;
  if (!bntPath || !statePath || !catalogCsv || !outJsonl || !outSummary) {
    throw new Error('--models <Models.bnt> --state <jsonl> --catalog <csv> --out-jsonl <f> --out-summary <f> required');
  }

  // catalog (metadata only)
  const catalogExact = new Set();
  const catalogBase = new Set(); // base (no extension) → true
  for (const line of fs.readFileSync(catalogCsv, 'utf8').split(/\r?\n/).slice(1)) {
    if (!line.trim()) continue;
    const cols = line.split(',');
    if (cols.length < 3) continue;
    const name = cols[2];
    catalogExact.add(name);
    const dot = name.lastIndexOf('.');
    catalogBase.add(dot >= 0 ? name.slice(0, dot) : name);
  }

  // the DECODED model list from phase 2 (1551, includes 218757)
  const decoded = [];
  for (const line of fs.readFileSync(statePath, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try {
      const r = JSON.parse(line);
      if (r.status === 'DECODED') decoded.push({ name: r.name, entryIndex: r.entryIndex });
    } catch { /* torn tail — skip */ }
  }
  const todo = decoded.slice(0, limit);
  console.log(JSON.stringify({ catalogEntries: catalogExact.size, decodedModels: decoded.length, has218757: decoded.some((d) => d.name === '218757.nif') }));

  const bytes = new Uint8Array(fs.readFileSync(bntPath));
  const containerSha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (expectSha && containerSha !== expectSha.toLowerCase()) {
    throw new Error('[phase3_pcg935_name_batch] container SHA mismatch — BLOCKED');
  }
  const arch = new Bnt2Archive(bytes);
  const entries = arch.entries();
  const byName = new Map(entries.map((e) => [e.name, e]));

  const stats = {
    modelsProcessed: 0, modelsWithArkTexture: 0, modelsWithSourceTexture: 0,
    parseErrors: 0, edges: 0, nameFoundExact: 0, nameBaseMatch: 0, nameNotFound: 0,
    distinctNames: new Set(),
    parseErrorSamples: [],
  };
  const out = fs.createWriteStream(outJsonl, { flags: 'w' });
  for (const d of todo) {
    const e = byName.get(d.name);
    if (!e) { stats.parseErrors++; continue; }
    let r;
    try {
      const { payload } = arch.readEntry(e);
      r = readNif10(payload, { sourceName: d.name });
    } catch (err) {
      stats.parseErrors++;
      if (stats.parseErrorSamples.length < 5) {
        stats.parseErrorSamples.push({ model: d.name, error: String(err?.message ?? err).slice(0, 200) });
      }
      continue;
    }
    stats.modelsProcessed++;
    const byIndex = new Map(r.blocks.map((b) => [b.index, b]));
    const arkTexByTexprop = new Map(); // texpropRef -> [{entryName, f1, bytes9Hex}]
    let modelHasArk = false;
    for (const b of r.blocks) {
      if (b.type !== 'NiArkTextureExtraData') continue;
      modelHasArk = true;
      for (const en of b.fields?.entries ?? []) {
        const list = arkTexByTexprop.get(en.texturingPropertyRef) ?? [];
        list.push({ entryName: en.entryName, f1: en.f1, bytes9Hex: en.bytes9Hex });
        arkTexByTexprop.set(en.texturingPropertyRef, list);
      }
    }
    if (modelHasArk) stats.modelsWithArkTexture++;
    let modelHasSource = false;
    // per-shape edges
    for (const b of r.blocks) {
      if (b.type !== 'NiTriShape') continue;
      for (const pref of b.propertyRefs ?? []) {
        if (pref == null || pref < 0) continue;
        const prop = byIndex.get(pref);
        if (!prop) continue;
        if (prop.type === 'NiTexturingProperty') {
          for (const [entryName, f1, bytes9Hex] of (arkTexByTexprop.get(pref) ?? []).map((x) => [x.entryName, x.f1, x.bytes9Hex])) {
            let disposition = 'NAME_NOT_FOUND';
            if (catalogExact.has(entryName)) { disposition = 'NAME_FOUND_EXACT'; stats.nameFoundExact++; }
            else {
              const base = entryName.includes('.') ? entryName.slice(0, entryName.lastIndexOf('.')) : entryName;
              if (catalogBase.has(base)) { disposition = 'NAME_BASE_MATCH_EXTENSION_DIFF'; stats.nameBaseMatch++; }
              else stats.nameNotFound++;
            }
            stats.edges++;
            stats.distinctNames.add(entryName);
            out.write(JSON.stringify({
              era: 'PCG_9_3_5', model: d.name, sceneBlock: b.index, sceneBlockName: b.name,
              edge: 'SHAPE->NITEXTURINGPROPERTY->ARKTEXTURE_ENTRY',
              texturingPropertyBlock: pref, slotF1: f1, slotLineageLabel: SLOT_LINEAGE_LABEL(f1),
              textureName: entryName, containerEntry: null, disposition,
              bytes9Hex, bytes9Semantics: 'RAW_ONLY (218757 retraction stands; no interpretation)',
              materialApplied: false, browserObserved: false,
            }) + '\n');
          }
          // slot.sourceRef → NiSourceTexture filename edges
          for (const slot of prop.fields?.slots ?? []) {
            if (!slot.has || slot.sourceRef == null || slot.sourceRef < 0) continue;
            const src = byIndex.get(slot.sourceRef);
            if (src?.type === 'NiSourceTexture') {
              modelHasSource = true;
              const fname = src.fields?.filename ?? null;
              let disposition = 'NAME_NOT_FOUND';
              if (fname && catalogExact.has(fname)) { disposition = 'NAME_FOUND_EXACT'; stats.nameFoundExact++; }
              else if (fname) {
                const base = fname.includes('.') ? fname.slice(0, fname.lastIndexOf('.')) : fname;
                if (catalogBase.has(base)) { disposition = 'NAME_BASE_MATCH_EXTENSION_DIFF'; stats.nameBaseMatch++; }
                else stats.nameNotFound++;
              } else stats.nameNotFound++;
              stats.edges++;
              out.write(JSON.stringify({
                era: 'PCG_9_3_5', model: d.name, sceneBlock: b.index, sceneBlockName: b.name,
                edge: 'SHAPE->NITEXTURINGPROPERTY->SLOT->NISOURCETEXTURE',
                texturingPropertyBlock: pref, slotName: slot.slotName, uvSet: slot.uvSet ?? null,
                textureName: fname, containerEntry: null, disposition,
                materialApplied: false, browserObserved: false,
              }) + '\n');
            }
          }
        } else if (prop.type === 'NiMaterialProperty') {
          // material reference (REFERENCE_CONFIRMED) — no texture name here
          stats.edges++;
          out.write(JSON.stringify({
            era: 'PCG_9_3_5', model: d.name, sceneBlock: b.index, sceneBlockName: b.name,
            edge: 'SHAPE->NIMATERIALPROPERTY', materialBlock: pref,
            materialApplied: false, browserObserved: false,
            note: 'material reference verified (colors on the material block); texture chain NOT claimed',
          }) + '\n');
        }
      }
    }
    if (modelHasSource) stats.modelsWithSourceTexture++;
  }
  out.end();
  stats.distinctNames = stats.distinctNames.size;
  const summary = {
    artifact: 'PCG935_NAME_FOUND_BATCH_SUMMARY',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'FOUR_MODELS_DEEP_ANALYSIS (phase 3)',
    era: 'PCG_9_3_5',
    container: { path: bntPath, sha256: containerSha },
    catalog: { source: catalogCsv, entries: catalogExact.size },
    modelsFromPhase2Decoded: decoded.length,
    modelsProcessed: stats.modelsProcessed,
    parseErrors: stats.parseErrors,
    parseErrorSamples: stats.parseErrorSamples,
    modelsWithArkTextureNames: stats.modelsWithArkTexture,
    modelsWithNiSourceTexture: stats.modelsWithSourceTexture,
    edges: stats.edges,
    dispositionCounts: {
      NAME_FOUND_EXACT: stats.nameFoundExact,
      NAME_BASE_MATCH_EXTENSION_DIFF: stats.nameBaseMatch,
      NAME_NOT_FOUND: stats.nameNotFound,
    },
    distinctTextureNames: stats.distinctNames,
    honestNote: 'The 8,381-entry Textures.bnt catalog is named NNNNNN.dat (numeric); the model-side ArkTexture names are descriptive (e.g. B_Outpost_me01_Ext_main_0_BASE). No name-based resolution is therefore expected to succeed; the 9-byte Ark tail is NOT interpreted (218757 retraction stands). MATERIAL_APPLIED and BROWSER_OBSERVED stay false/0 until a real browser render (phase 4).',
    outJsonl,
  };
  fs.writeFileSync(outSummary, JSON.stringify(summary, null, 1), 'utf8');
  process.stdout.write(JSON.stringify(summary, null, 1) + '\n');
}

main().catch((err) => {
  console.error('[phase3_pcg935_name_batch] FATAL:', err?.stack ?? err);
  process.exitCode = 1;
});
