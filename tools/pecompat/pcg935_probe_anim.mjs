#!/usr/bin/env node
// PRIVATE probe: animation decoder smoke test — pick assets with kf/skin/morph.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';
import { buildAssetIR } from '../../src/pecompat/PecSceneIR.js';
import { decodeAssetAnimations } from '../../src/pecompat/PecAnimDecoder.js';

const mBytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const mArch = new Bnt2Archive(mBytes);
const rows = fs.readFileSync('D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010\\catalog\\checkpoint.jsonl', 'utf8')
  .split('\n').filter(Boolean).map((l) => JSON.parse(l));
const pick = (pred, label) => {
  const row = rows.find(pred);
  if (!row) { console.log(`[anim-probe] no ${label} candidate`); return; }
  const { payload } = mArch.readEntry(mArch.entryByName(row.name));
  const reader = row.version >= 0x0a000000 ? readNif10Corpus : readNif41Corpus;
  const r = reader(payload, { sourceName: row.name });
  const ir = buildAssetIR(r, { assetId: row.id, era: 'PCG_9_3_5', build: 'probe', container: 'Models.bnt', entryName: row.name, payloadSha256: 'x', sizeBytes: row.sizeBytes, adapterVersion: 'probe', physicalSource: 'Models.bnt' });
  const anim = decodeAssetAnimations(ir);
  console.log(`=== ${row.name} (${row.versionString}) kf=${anim.keyframeControllers} clips=${anim.clips.length} textKeys=${anim.textKeys.length} skel=${anim.skeletons.length} morph=${anim.morphs.length} psys=${anim.psys.length} uv=${anim.uvControllers.length} vis=${anim.visControllers.length}`);
  const c = anim.clips[0];
  if (c) console.log('  clip0:', c.targetName, 'quatKeys', c.quaternion?.times?.length ?? '-', 'posKeys', c.position?.times?.length ?? '-', 'dur', c.dataDuration);
  if (anim.textKeys.length) console.log('  tk0:', JSON.stringify(anim.textKeys[0].keys.slice(0, 4)));
  if (anim.skeletons.length) console.log('  skel0 bones:', anim.skeletons[0].bones.length, 'first weights:', anim.skeletons[0].bones[0]?.vertexWeights?.length ?? 0);
};
pick((r) => r.kf > 0 && r.tk > 0, 'kf+textkey');
pick((r) => r.skin > 0, 'skinned');
pick((r) => r.morph > 0, 'morphed');
pick((r) => r.versionString === '4.1.0.12' && r.kf > 0, 'v4-keyframed');
