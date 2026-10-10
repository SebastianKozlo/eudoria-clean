// QC2 — full CSV parse of TEXTURE_LINK_DISPOSITIONS.csv (record census, schema, four-primary rows,
// PCG935 aggregates, mojibake detection). READ-ONLY; writes under 00_CONTROL_INTERNAL_QC/.
import { readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const PKG = resolve(process.argv[2]);
const csvPath = join(PKG, 'TEXTURE_LINK_DISPOSITIONS.csv');
const raw = readFileSync(csvPath); // bytes
const text = raw.toString('utf8');

// locate non-ASCII bytes and their context
const nonAscii = [];
for (let i = 0; i < raw.length; i++) {
  if (raw[i] > 0x7f) {
    const s = Math.max(0, i - 40), e = Math.min(raw.length, i + 40);
    nonAscii.push({ offset: i, bytesHex: raw.slice(i, i + 8).toString('hex'), context: raw.slice(s, e).toString('latin1') });
    i += 40; // skip context window to avoid flooding
  }
}

// proper CSV parse with quoted fields
function parseCsv(text) {
  const rows = []; let row = [], field = '', inQ = false, i = 0;
  while (i < text.length) {
    const c = text[i];
    if (inQ) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i += 2; continue; } inQ = false; i++; continue; }
      field += c; i++; continue;
    }
    if (c === '"') { inQ = true; i++; continue; }
    if (c === ',') { row.push(field); field = ''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; i++; continue; }
    field += c; i++;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
}
const rows = parseCsv(text);
const header = rows[0];
const dataRows = rows.slice(1).filter(r => r.length > 1 || (r[0] || '') !== '');
const schemaCheck = { header, headerFieldCount: header.length };
const fieldCounts = {};
let malformed = 0;
for (const r of dataRows) { fieldCounts[r.length] = (fieldCounts[r.length] || 0) + 1; if (r.length !== header.length) malformed++; }

// census per era / model
const byEra = {};
const byModel = {};
const primaryIds = ['192374', '193207', '193313', '193684'];
for (const r of dataRows) {
  const era = r[1]; byEra[era] = (byEra[era] || 0) + 1;
  const mid = r[0]; byModel[mid] = (byModel[mid] || 0) + 1;
}

// four primaries: verify texture-chain rows + material rows
const primaries = {};
for (const r of dataRows) {
  if (primaryIds.includes(r[0])) {
    if (!primaries[r[0]]) primaries[r[0]] = [];
    primaries[r[0]].push({ edge: r[2], slot: r[3], dispositions: r[6] });
  }
}
const primaryChecks = {};
for (const id of primaryIds) {
  const rs = primaries[id] || [];
  primaryChecks[id] = {
    rowCount: rs.length,
    textureChainRows: rs.filter(x => x.edge.includes('TEXTURE_CHAIN')).length,
    allTextureChainUntexturedProxy: rs.filter(x => x.edge.includes('TEXTURE_CHAIN')).every(x => x.dispositions.includes('UNTEXTURED_PROXY_MESH')),
    materialRows: rs.filter(x => x.edge.includes('NIMATERIALPROPERTY')).length,
    materialAllAppliedYes: rs.filter(x => x.edge.includes('NIMATERIALPROPERTY')).every(x => x.dispositions.includes('MATERIAL_APPLIED=YES')),
    materialAllPixelRender: rs.filter(x => x.edge.includes('NIMATERIALPROPERTY')).every(x => x.dispositions.includes('BROWSER_OBSERVED=PIXEL_RENDER')),
    anyArkTailTransfer: rs.some(x => x.dispositions.includes('textureId') || /9.byte/i.test(x.dispositions) && !x.dispositions.includes('RAW_ONLY'))
  };
}

// PCG935 aggregate rows: NAME_NOT_FOUND sums
let nameNotFoundSum = 0, pcgAggRows = 0, modelsWithEdges = new Set();
for (const r of dataRows) {
  if (r[1] === 'PCG_9_3_5' && r[2].includes('aggregated')) {
    pcgAggRows++;
    const m = r[6].match(/NAME_NOT_FOUND=(\d+)/);
    if (m) { nameNotFoundSum += parseInt(m[1], 10); modelsWithEdges.add(r[0]); }
  }
}
// count PCG_9_3_5 texture-name edges distinct from material edges
let pcgTextureEdgeRows = 0, pcgMaterialRefRows = 0;
for (const r of dataRows) {
  if (r[1] === 'PCG_9_3_5') {
    if (r[2].includes('ARKTEXTURE_ENTRY')) pcgTextureEdgeRows++;
    if (r[2].includes('NIMATERIALPROPERTY') && !r[2].includes('aggregated')) pcgMaterialRefRows++;
  }
}

// mojibake detection: replacement char U+FFFD in decoded text
const mojibakeRows = [];
dataRows.forEach((r, idx) => { if (r.some(f => f.includes('\uFFFD'))) mojibakeRows.push({ dataRowIndex: idx + 1, model_id: r[0], era: r[1], edge: r[2] }); });

const out = {
  runId: 'PE_CITY_ASSET_MAP_R1_20261010', qcStep: 'QC2_TEXTURE_CSV_PARSE',
  totalBytes: raw.length,
  endsWithNewline: raw[raw.length - 1] === 0x0a,
  schemaCheck, fieldCounts, malformedRowCount: malformed,
  totalParsedRows: rows.length, headerRow: 1, dataRows: dataRows.length,
  byEra, distinctModels: Object.keys(byModel).length,
  primaryChecks, pcgAggregateRows: pcgAggRows, pcgAggNameNotFoundSum: nameNotFoundSum,
  pcgAggDistinctModelsWithEdges: modelsWithEdges.size,
  pcgTextureEdgeAggRowCount: pcgTextureEdgeRows,
  pcgMaterialRefRowCount: pcgMaterialRefRows,
  mojibakeRowCount: mojibakeRows.length, mojibakeRows: mojibakeRows.slice(0, 40),
  nonAsciiByteSites: nonAscii.length, nonAsciiSamples: nonAscii.slice(0, 10)
};
writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC2_TEXTURE_CSV_PARSE.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify({ dataRows: out.dataRows, byEra: out.byEra, distinctModels: out.distinctModels, malformed: malformed, primaryChecks, pcgAggRows: pcgAggRows, nameNotFoundSum, mojibakeRowCount: out.mojjibakeSafe = out.mojibakeRowCount, nonAsciiSites: nonAscii.length }, null, 1));
