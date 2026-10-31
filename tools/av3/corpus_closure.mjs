// tools/av3/corpus_closure.mjs — AV-3: run the closure-exact decoder over ALL
// NIF 4.1.0.12 files with NiKeyframeController (the 431 census members) and
// report the TRUE number of models that get KF clips at runtime (requires
// decodeKeyframeBlocks41().closureAll === true — never estimated, measured).
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel41 } from '../../src/pesource/NifModelReader41.js';
import { decodeKeyframeBlocks41 } from './kf41.mjs';

const MODELS_ARK_PATH = process.env.AV_MODELS_ARK ||
  'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const PIN = 128742137;
const SCI = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV3_ANIMATION';
const CEN = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV1_CENSUS\\ANIMATION_CENSUS.json';

const buf = await fs.readFile(MODELS_ARK_PATH);
if (buf.length !== PIN) throw new Error(`FAIL-CLOSED pin: ${buf.length} != ${PIN}`);
const ark = new ArkArchive(new Uint8Array(buf));
const anim = JSON.parse(await fs.readFile(CEN, 'utf8'));

const out = { job: 'AV3', generated: new Date().toISOString(), files: [] };
let closureOk = 0, closureFail = 0, textKeyNamed = 0, kinematic = 0;
let totalKfc = 0, totalKfd = 0, totalTextKeyBlocks = 0, totalTracks = 0;
const failureReasons = new Map();
for (const f of anim.perFileAnimated) {
  if (f.version !== '4.1.0.12') continue;
  const id = Number(f.name.replace('.nif', ''));
  let rec = { id, name: f.name };
  try {
    const entry = ark.entryById(id);
    if (!entry) throw new Error('no ark entry');
    const { payload } = ark.readEntry(entry);
    const { extraction } = parseModel41(payload, f.name);
    if (extraction.parseStatus !== 'PASS') { rec.reader = extraction.parseStatus; }
    const kf = decodeKeyframeBlocks41(payload, extraction);
    rec = { ...rec, kfc: kf.controllers.length, kfd: kf.data.length,
      textKeyBlocks: kf.textKeys.length, closureAll: kf.closureAll,
      failures: kf.failures.length };
    // count buildable tracks (controller target resolvable in hierarchy)
    const nodes = new Set(extraction.blocks.filter(b => b.type === 'NiNode' || b.type === 'NiTriShape').map(b => b.index));
    let tracks = 0;
    const dataIdx = new Set(kf.data.map(d => d.blockIndex));
    for (const c of kf.controllers) {
      if (nodes.has(c.target) && dataIdx.has(c.dataRef)) tracks++;
    }
    rec.buildableBoneTracks = tracks;
    if (kf.closureAll && kf.controllers.length && tracks > 0) {
      closureOk++;
      totalTracks += tracks;
      if (kf.textKeys.some(t => t.keys.length)) { textKeyNamed++; rec.clipNameSource = 'NiTextKeyExtraData'; }
      else { kinematic++; rec.clipNameSource = 'KINEMATIC/EMBEDDED'; }
    } else if (!kf.closureAll) {
      closureFail++;
      for (const fl of kf.failures) failureReasons.set(fl.reason.slice(0, 60), (failureReasons.get(fl.reason.slice(0, 60)) ?? 0) + 1);
    }
    totalKfc += kf.controllers.length; totalKfd += kf.data.length; totalTextKeyBlocks += kf.textKeys.length;
  } catch (e) {
    rec.error = String(e.message ?? e).slice(0, 120);
    closureFail++;
  }
  out.files.push(rec);
}
out.summary = {
  filesChecked: out.files.length,
  modelsGetClips_closureExact_measured: closureOk,
  closureFail: closureFail,
  namedClips_textKeys: textKeyNamed,
  kinematicEmbeddedClips: kinematic,
  totalKfcBlocks: totalKfc, totalKfdBlocks: totalKfd, totalTextKeyBlocks: totalTextKeyBlocks,
  totalBuildableBoneTracks: totalTracks,
  failureReasonSummary: [...failureReasons.entries()].slice(0, 10),
};
await fs.mkdir(SCI, { recursive: true });
await fs.writeFile(`${SCI}\\av3_corpus_closure.json`, JSON.stringify(out, null, 2));
console.log(JSON.stringify(out.summary, null, 2));
