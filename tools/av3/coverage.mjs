// tools/av3/coverage.mjs — AV-3: how many models get KF clips after the
// integration (census intersection: has NiKeyframeController AND is
// NIF 4.1.0.12 AND was parseable by the AV-2 reader census).
'use strict';
import { promises as fs } from 'node:fs';
const CEN = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV1_CENSUS\\ANIMATION_CENSUS.json';
const AVC = 'D:\\Eudoria_Reconstruction\\12_WebGame\\pe2003-iso-assetviewer-r1\\tools\\av2\\scan_models_result.json';
const SCI = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV3_ANIMATION';
const anim = JSON.parse(await fs.readFile(CEN, 'utf8'));
const av2 = JSON.parse(await fs.readFile(AVC, 'utf8'));
const av2ById = new Map();
for (const m of av2.models ?? []) av2ById.set(Number(m.id), m);
let total41012 = 0, pass41012 = 0, passWithTextKeys = 0;
const missing = [];
for (const f of anim.perFileAnimated) {
  if (f.version !== '4.1.0.12') continue;
  total41012++;
  const m = av2ById.get(Number(f.name.replace('.nif', '')));
  if (m && m.status === 'PASS') {
    pass41012++;
    if (f.textKeys > 0) passWithTextKeys++;
  } else {
    missing.push({ name: f.name, av2: m ? m.parseStatus : 'NOT_IN_AV2_SCAN' });
  }
}
const out = {
  job: 'AV3', generated: new Date().toISOString(),
  filesWithKFCandKFD_total: anim.filesWithNiKeyframeController,
  filesWithTextKeys_total: anim.filesWithNiTextKeyExtraData,
  v4_1_0_12_withKFC: total41012,
  v4_1_0_12_withKFC_andReaderPass: pass41012,
  v4_1_0_12_withKFC_readerPass_withTextKeys: passWithTextKeys,
  excluded_opaqueUnparsed: missing.length, excludedSample: missing.slice(0, 10),
  note: 'estimate: KF clips are built client-side whenever keyframeAnim.closureAll===true; closure-exactness is enforced per block by tools/av3/kf41.mjs',
};
await fs.mkdir(SCI, { recursive: true });
await fs.writeFile(`${SCI}\\av3_coverage_estimate.json`, JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
