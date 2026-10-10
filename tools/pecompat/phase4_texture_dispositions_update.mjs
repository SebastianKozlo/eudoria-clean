// phase4_texture_dispositions_update.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4.
// Updates TEXTURE_LINK_DISPOSITIONS.csv (report package) for the FOUR CD_2003
// primaries' MATERIAL edges after the REAL browser PIXEL_RENDER of their
// /catalog previews (contract §4 + task 3 MATERIAL_APPLIED/BROWSER_OBSERVED):
//   - MATERIAL edges (SHAPE#N->NIMATERIALPROPERTY): MATERIAL_APPLIED=YES (the
//     verified NiMaterialProperty diffuse color IS applied to that shape's
//     material in the preview) + BROWSER_OBSERVED=PIXEL_RENDER (the preview was
//     rendered by a real headless Edge and captured as a verified non-trivial
//     PNG — per-model PNG SHA256 recorded).
//   - TEXTURE_CHAIN edges: UNCHANGED — UNTEXTURED_PROXY_MESH stays the measured
//     fact (0 texture bindings, 0 UV sets, numTex=0; texture classes stay 0;
//     NO textured PASS is claimed anywhere).
// The per-model PNG SHA256s come from the PIXEL_RENDER raw record (never from
// memory); the update FAILS CLOSED if the record does not verify (all 4
// previews present, status PASS, per-shot sha256 recorded).
import fs from 'node:fs';

const CSV = process.argv[2];
const PIXEL_RAW = process.argv[3];
if (!CSV || !PIXEL_RAW) throw new Error('usage: node phase4_texture_dispositions_update.mjs <TEXTURE_LINK_DISPOSITIONS.csv> <CATALOG_PIXEL_RUN.json>');

const pixel = JSON.parse(fs.readFileSync(PIXEL_RAW, 'utf8'));

// verify the evidence BEFORE writing anything (fail-closed)
if (pixel.status !== 'PASS') throw new Error(`pixel record status != PASS (${pixel.status}) — refusing to update dispositions`);
const shots = new Map(pixel.shots.map((s) => [s.label, s]));
const needed = ['PREVIEW_192374', 'PREVIEW_193207', 'PREVIEW_193313', 'PREVIEW_193684'];
for (const label of needed) {
  const s = shots.get(label);
  if (!s || !s.png?.sha256) throw new Error(`pixel record missing shot ${label} — refusing`);
  if (!s.checks.every((c) => c.ok)) throw new Error(`shot ${label} has failed checks — refusing`);
}
const pngSha = (id) => shots.get(`PREVIEW_${id}`).png.sha256;

const lines = fs.readFileSync(CSV, 'utf8').split(/\r?\n/).filter((l) => l.length > 0);
const out = [];
let updatedMaterialRows = 0, textureChainRows = 0;
for (const line of lines) {
  if (line.startsWith('model_id,')) { out.push(line); continue; }
  const isMaterialEdge = /->NIMATERIALPROPERTY,/.test(line);
  const isCd2003Primary = /^(192374|193207|193313|193684),CD_2003,/.test(line);
  if (isMaterialEdge && isCd2003Primary) {
    const model = line.split(',')[0];
    const before = line;
    const after = line.replace(
      /"REFERENCE_CONFIRMED \(block (\d+)\); MATERIAL_APPLIED=NOT_YET \(no render this phase\); BROWSER_OBSERVED=0"/,
      `"REFERENCE_CONFIRMED (block $1); MATERIAL_APPLIED=YES (NiMaterialProperty diffuse color APPLIED to this shape's material in the /catalog preview — real-browser PIXEL_RENDER observed; per-model PNG SHA256 ${pngSha(model)}); BROWSER_OBSERVED=PIXEL_RENDER (headless Edge screenshot, non-triviality gate PASS)"`,
    );
    if (after === before) throw new Error(`row not updated (unexpected format): ${line.slice(0, 120)} — refusing`);
    out.push(after);
    updatedMaterialRows++;
  } else {
    if (/->TEXTURE_CHAIN/.test(line) && isCd2003Primary) textureChainRows++;
    out.push(line); // UNCHANGED — UNTEXTURED_PROXY_MESH stays the measured fact
  }
}
fs.writeFileSync(CSV, out.join('\r\n') + '\r\n', 'utf8');
process.stdout.write(JSON.stringify({
  artifact: 'TEXTURE_LINK_DISPOSITIONS_PHASE4_UPDATE',
  csv: CSV,
  materialRowsUpdated: updatedMaterialRows,
  textureChainRowsUnchanged: textureChainRows,
  modelsRenderedByRealBrowser: needed.map((n) => ({ label: n, pngSha256: pngSha(n.replace('PREVIEW_', '')) })),
  policy: 'MATERIAL_APPLIED only where a REAL browser render applied + observed the material; texture classes stay 0 (UNTEXTURED_PROXY_MESH unchanged — measured fact); fail-closed on any evidence gap',
}, null, 1) + '\n');
