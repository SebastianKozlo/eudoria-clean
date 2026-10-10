// QC5 — proper BNT2 payload boundary analysis (sorted-by-offset gap/overlap census),
// census artifact row counts, and PHASE3 block-dump integrity (re-hash + parse).
import { readFileSync, writeFileSync, statSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';

const PRIV = process.argv[2];
const OUT = resolve(process.argv[3]);
const res = { runId: 'PE_CITY_ASSET_MAP_R1_20261010', qcStep: 'QC5_BOUNDARIES_CENSUS_BLOCKDUMPS' };

// --- BNT2 proper boundary analysis (payload order, not directory order) ---
const bntBytes = readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt');
const dv = new DataView(bntBytes.buffer, bntBytes.byteOffset, bntBytes.byteLength);
const dirOffset = dv.getUint32(bntBytes.length - 8, true);
const count = dv.getUint32(dirOffset, true);
let p = dirOffset + 4; const entries = [];
for (let i = 0; i < count; i++) {
  const s = p; while (bntBytes[p] !== 0x0a) p++;
  const name = bntBytes.subarray(s, p).toString('latin1'); p++;
  entries.push({ i, name, size: dv.getUint32(p, true), offset: dv.getUint32(p + 4, true), crc: dv.getUint32(p + 8, true) });
  p += 16;
}
const sorted = [...entries].sort((a, b) => a.offset - b.offset);
let overlaps = 0, gaps = [], cursor = 0;
for (const e of sorted) {
  if (e.offset < cursor) overlaps++;
  else if (e.offset > cursor) gaps.push({ from: cursor, to: e.offset, bytes: e.offset - cursor });
  cursor = Math.max(cursor, e.offset + e.size);
}
const bntFooterStart = bntBytes.length - 8;
const maxEnd = sorted[sorted.length - 1].offset + sorted[sorted.length - 1].size;
const dirMonotonic = entries.every((e, i) => i === 0 || e.offset >= entries[i - 1].offset);
res.bnt2Boundaries = {
  count, dirEnd: p, dirEndEqualsFooterStart: p === bntFooterStart,
  payloadOverlaps: overlaps, payloadGaps: gaps.length, gapTotalBytes: gaps.reduce((a, g) => a + g.bytes, 0),
  gapsSample: gaps.slice(0, 5),
  firstPayloadOffset: sorted[0].offset,
  lastPayloadEnd: maxEnd, footerStart: bntFooterStart, tailGapBytes: bntFooterStart - maxEnd,
  directoryOrderMonotonicOffsets: dirMonotonic
};

// --- census artifact row counts ---
function parseCsv(text) { const rows = []; let row = [], f = '', q = false, i = 0;
  while (i < text.length) { const c = text[i];
    if (q) { if (c === '"') { if (text[i+1]==='"'){f+='"';i+=2;continue;} q=false;i++;continue;} f+=c;i++;continue; }
    if (c === '"') { q = true; i++; continue; }
    if (c === ',') { row.push(f); f=''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(f); rows.push(row); row=[]; f=''; i++; continue; }
    f += c; i++; }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  return rows; }
const cdCensus = parseCsv(readFileSync(join(PRIV, 'PHASE2_CENSUS', 'CD_2003_FILE_CENSUS.csv'), 'utf8'));
const pcgCensus = parseCsv(readFileSync(join(PRIV, 'PHASE2_CENSUS', 'PCG_9_3_5_FILE_CENSUS.csv'), 'utf8'));
res.census = {
  cd_rows: cdCensus.length - 1, pcg_rows: pcgCensus.length - 1,
  cd_header: cdCensus[0], pcg_header: pcgCensus[0],
  claimed: { cd: 4, pcg: 1818 },
  cd_total_bytes: cdCensus.slice(1).reduce((a, r) => a + (+r[2] || 0), 0),
  pcg_total_bytes: pcgCensus.slice(1).reduce((a, r) => a + (+r[2] || 0), 0)
};

// --- PHASE3 block dumps + parts CSVs: identity + parse ---
res.phase3BlockDumps = {};
for (const id of ['192374', '193207', '193313', '193684']) {
  const bj = join(PRIV, 'PHASE3_BlockDumps', `${id}_blocks.json`);
  const pj = join(PRIV, 'PHASE3_BlockDumps', `${id}_parts.csv`);
  const bBytes = readFileSync(bj);
  const b = JSON.parse(bBytes.toString('utf8'));
  const parts = parseCsv(readFileSync(pj, 'utf8'));
  res.phase3BlockDumps[id] = {
    blocks_json_bytes: bBytes.length, blocks_json_sha256: createHash('sha256').update(bBytes).digest('hex'),
    topKeys: Object.keys(b),
    numBlocks: b.numBlocks ?? b.blockCount ?? (Array.isArray(b.blocks) ? b.blocks.length : null),
    status: b.status ?? b.statusClass ?? null,
    names: b.names ? Object.keys(b.names).length : (b.hierarchy?.names ?? null),
    parts_csv_rows: parts.length - 1, parts_csv_header: parts[0]
  };
}

// --- PHASE3_MODELS extracted payloads: re-hash (vs phase-2 catalog) ---
const prim = {};
for (const id of ['192374', '193207', '193313', '193684']) {
  const mp = join(PRIV, 'PHASE3_MODELS', `${id}.nif`);
  const bytes = readFileSync(mp);
  prim[id] = { size: bytes.length, sha256: createHash('sha256').update(bytes).digest('hex'), first_bytes: bytes.subarray(0, 8).toString('hex') };
}
res.phase3ModelPayloads = prim;

// --- PHASE3_NativeControl raw outputs re-read (verbatim) ---
res.nativeControl = {};
for (const id of ['192374', '193207', '193313', '193684']) {
  const so = readFileSync(join(PRIV, 'PHASE3_NativeControl', `${id}.stdout.txt`));
  const se = readFileSync(join(PRIV, 'PHASE3_NativeControl', `${id}.stderr.txt`));
  res.nativeControl[id] = { stdout_bytes: so.length, stdout_text: so.toString('utf8'), stderr_bytes: se.length, stderr_text: se.toString('utf8') };
}
const rrRaw = readFileSync(join(PRIV, 'PHASE3_NativeControl', 'run_records.json'));
const rrHasBom = rrRaw[0] === 0xef && rrRaw[1] === 0xbb && rrRaw[2] === 0xbf;
res.nativeControlRunRecords = { hasUtf8Bom: rrHasBom, bytes: rrRaw.length, sha256: createHash('sha256').update(rrRaw).digest('hex'), strictJsonParse: (() => { try { JSON.parse(rrRaw.toString('utf8')); return 'OK'; } catch (e) { return 'FAIL: ' + String(e.message).slice(0, 80); } })() };
const rr = rrRaw.toString('utf8').replace(/^\uFEFF/, '');
res.nativeControl.run_records = JSON.parse(rr).runs ?? JSON.parse(rr);

// --- BOM census over ALL private-output JSON artifacts (machine-readability check) ---
function bomCensus(dir) { const out = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...bomCensus(p));
    else if (e.name.toLowerCase().endsWith('.json')) {
      const b = readFileSync(p);
      const hasBom = b[0] === 0xef && b[1] === 0xbb && b[2] === 0xbf;
      let strict = 'OK'; try { JSON.parse(b.toString('utf8')); } catch (err) { strict = 'FAIL'; }
      out.push({ file: p, hasBom, strictJsonParse: strict });
    }
  }
  return out; }
const bomList = bomCensus(PRIV);
res.privateJsonBomCensus = { totalJson: bomList.length, withBom: bomList.filter(x => x.hasBom).map(x => x.file), strictParseFailures: bomList.filter(x => x.strictJsonParse !== 'OK').map(x => x.file) };

writeFileSync(join(OUT, 'QC5_BOUNDARIES_CENSUS_BLOCKDUMPS.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify({ bnt2Boundaries: res.bnt2Boundaries, census: { cd_rows: res.census.cd_rows, pcg_rows: res.census.pcg_rows, cd_total_bytes: res.census.cd_total_bytes, pcg_total_bytes: res.census.pcg_total_bytes }, nativeControl: Object.fromEntries(Object.entries(res.nativeControl).filter(([k]) => k !== 'run_records').map(([k, v]) => [k, { stdout_bytes: v.stdout_bytes, stderr: v.stderr_text }])), prim: res.phase3ModelPayloads }, null, 1));
