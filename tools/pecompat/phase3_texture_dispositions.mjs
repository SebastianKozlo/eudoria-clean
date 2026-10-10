// phase3_texture_dispositions.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 3 (W4, contract §4)
// Builds TEXTURE_LINK_DISPOSITIONS.csv (report package; metadata only, no payloads):
//   - CD_2003 four primaries: per-shape rows (texture chain disposition +
//     material REFERENCE_CONFIRMED edges) with the explicit UNTEXTURED_PROXY_MESH
//     visual-fallback label (never a false textured PASS).
//   - PCG_9_3_5 bounded batch (218757 + the phase-2-decoded set): per-model
//     aggregate rows from the private per-edge JSONL (full lists stay in
//     PRIVATE_OUTPUT).
// Columns: model_id, era, edge, slot, texture_name, container_entry, dispositions.

import fs from 'node:fs';

const PRIV = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_CITY_ASSET_MAP_R1_20261010';
const DUMPS = `${PRIV}\\PHASE3_BlockDumps`;
const PCG_JSONL = `${PRIV}\\PHASE3_PCG935_BATCH\\PCG935_NAME_EDGES.jsonl`;
const OUT = process.argv[2];

const MODELS = ['192374', '193207', '193313', '193684'];
const lines = ['model_id,era,edge,slot,texture_name,container_entry,dispositions'];

for (const m of MODELS) {
  const d = JSON.parse(fs.readFileSync(`${DUMPS}\\${m}_blocks.json`, 'utf8'));
  for (const s of d.meshRows) {
    // texture chain edge (the honest terminating chain)
    lines.push([
      m, 'CD_2003',
      `SHAPE#${s.shapeBlock}(${s.shapeName})->TEXTURE_CHAIN`,
      'ANY', '', '',
      '"UNTEXTURED_PROXY_MESH: 0 NiTexturingProperty, 0 NiSourceTexture, NiArkTextureExtraData numTex=0, 0 UV sets — explicit visual fallback, NOT a textured PASS"',
    ].join(','));
    // material edge (REFERENCE_CONFIRMED, verified block ref)
    const matBlock = (s.propertyRefs ?? [])[0] ?? null;
    lines.push([
      m, 'CD_2003',
      `SHAPE#${s.shapeBlock}(${s.shapeName})->NIMATERIALPROPERTY`,
      'MATERIAL', '', '',
      `"REFERENCE_CONFIRMED (block ${matBlock}); MATERIAL_APPLIED=NOT_YET (no render this phase); BROWSER_OBSERVED=0"`,
    ].join(','));
  }
  // root state properties (verified refs, not texture edges)
  const root = d.blocks?.[0];
  if (root && root.propertyRefs) {
    lines.push([
      m, 'CD_2003', 'ROOT->STATE_PROPERTIES', 'STATE', '', '',
      `"REFERENCE_CONFIRMED (${root.propertyRefs.join('|')}: NiVertexColorProperty + NiZBufferProperty — state properties, no texture chain)"`,
    ].join(','));
  }
}

// PCG935 aggregate rows from the private per-edge JSONL
const agg = new Map();
for (const lineRaw of fs.readFileSync(PCG_JSONL, 'utf8').split('\n')) {
  if (!lineRaw.trim()) continue;
  const e = JSON.parse(lineRaw);
  const a = agg.get(e.model) ?? { nameEdges: 0, nameFound: 0, nameBase: 0, nameNotFound: 0, matEdges: 0 };
  if (e.edge === 'SHAPE->NIMATERIALPROPERTY') a.matEdges++;
  else {
    a.nameEdges++;
    if (e.disposition === 'NAME_FOUND_EXACT') a.nameFound++;
    else if (e.disposition === 'NAME_BASE_MATCH_EXTENSION_DIFF') a.nameBase++;
    else if (e.disposition === 'NAME_NOT_FOUND') a.nameNotFound++;
  }
  agg.set(e.model, a);
}
for (const [model, a] of [...agg.entries()].sort()) {
  const id = model.replace(/\.nif$/, '');
  const dispositions = [];
  dispositions.push(`NAME_FOUND_EXACT=${a.nameFound}`);
  dispositions.push(`NAME_BASE_MATCH_EXTENSION_DIFF=${a.nameBase}`);
  dispositions.push(`NAME_NOT_FOUND=${a.nameNotFound}`);
  dispositions.push(`MATERIAL_REFERENCE_CONFIRMED=${a.matEdges}`);
  dispositions.push('MATERIAL_APPLIED=0;BROWSER_OBSERVED=0');
  dispositions.push('CONTAINER_ENTRY_RESOLVED=0;IMAGE_DECODED=0');
  dispositions.push('ARK_TAIL=RAW_ONLY(218757 retraction stands)');
  lines.push([
    id, 'PCG_9_3_5', 'SHAPE->NITEXTURINGPROPERTY->ARKTEXTURE_ENTRY (aggregated)', 'BASE/DARK/etc', 'see private JSONL', 'Textures.bnt (8,381 entries)',
    `"${dispositions.join('; ')}"`,
  ].join(','));
}

// ASCII-only output (repo hygiene: no em-dashes / non-ASCII in persisted records)
const ascii = (s) => s.replace(/\u2014/g, '-').replace(/[^\x00-\x7F]/g, (c) => `\\u${c.charCodeAt(0).toString(16).padStart(4, '0')}`);
fs.writeFileSync(OUT, ascii(lines.join('\r\n')) + '\r\n', 'utf8');process.stdout.write(JSON.stringify({ artifact: 'TEXTURE_LINK_DISPOSITIONS', written: OUT, cd2003Models: MODELS.length, pcg935AggregateRows: agg.size }, null, 1) + '\n');
