// QC4 — INDEPENDENT catalog re-verification (pe-master-auditor fresh internal QC).
// My OWN minimal raw-byte ARK (ZIP-like, AK magic) and BNT2 readers — imports NOTHING
// from the executor's tools (no nif41_deep, no PecSceneIR, no ArkArchive/Bnt2Archive).
// Re-hash bounded samples of entries against the phase-2 catalogs in PRIVATE_OUTPUT,
// verify the four primary pins, catalog row counts, and coverage arithmetic.
// READ-ONLY against originals; writes under 00_CONTROL_INTERNAL_QC/.
import { readFileSync, writeFileSync, openSync, readSync, closeSync, statSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';

const PRIV = process.argv[2];
const OUT = resolve(process.argv[3]);
const MODELS_ARK = 'D:\\Eudoria_Reconstruction\\pcg2003_install\\Data\\Models\\Models.ark';
const MODELS_BNT = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt';
const res = { runId: 'PE_CITY_ASSET_MAP_R1_20261010', qcStep: 'QC4_CATALOG_REHASH', method: 'own minimal raw-byte readers; no executor tool imports' };

// --- container identity re-verification (streamed SHA256 of whole files) ---
function sha256File(p) { const fd = openSync(p, 'r'); const h = createHash('sha256'); const buf = Buffer.alloc(1 << 24); let pos = 0; for (;;) { const n = readSync(fd, buf, 0, buf.length, pos); if (n <= 0) break; h.update(buf.subarray(0, n)); pos += n; } closeSync(fd); return h.digest('hex'); }
res.containerIdentity = {
  models_ark: { path: MODELS_ARK, size: statSync(MODELS_ARK).size, sha256: sha256File(MODELS_ARK) },
  models_bnt: { path: MODELS_BNT, size: statSync(MODELS_BNT).size, sha256: sha256File(MODELS_BNT) }
};
res.containerIdentity.pinsCheck = {
  models_ark_expected: { size: 128742137, sha256: 'f660d055b4b9471b3b6e16b07f5368dbd6f2208dab6b51bb9bdb9942bd73ea62' },
  models_bnt_expected: { size: 395412868, sha256: 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0' },
  ark_ok: res.containerIdentity.models_ark.size === 128742137 && res.containerIdentity.models_ark.sha256 === 'f660d055b4b9471b3b6e16b07f5368dbd6f2208dab6b51bb9bdb9942bd73ea62',
  bnt_ok: res.containerIdentity.models_bnt.size === 395412868 && res.containerIdentity.models_bnt.sha256 === 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0'
};

// --- MY minimal ARK reader: sequential local-header walk ---
const arkBytes = readFileSync(MODELS_ARK);
function myArkWalk(bytes) {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const entries = []; let pos = 0; let stop = null;
  while (pos + 4 <= bytes.length) {
    if (!(bytes[pos] === 0x41 && bytes[pos + 1] === 0x4b && bytes[pos + 2] === 0x03 && bytes[pos + 3] === 0x04)) { stop = pos; break; }
    const method = dv.getUint16(pos + 8, true);
    const crc = dv.getUint32(pos + 14, true);
    const compSize = dv.getUint32(pos + 18, true);
    const uncompSize = dv.getUint32(pos + 22, true);
    const nameLen = dv.getUint16(pos + 26, true);
    const extraLen = dv.getUint16(pos + 28, true);
    const name = bytes.subarray(pos + 30, pos + 30 + nameLen).toString('latin1');
    const dataOffset = pos + 30 + nameLen + extraLen;
    entries.push({ i: entries.length, name, method, crc, compSize, uncompSize, dataOffset });
    pos = dataOffset + compSize;
  }
  return { entries, chainEnd: stop, eocd: findEocd(bytes, dv) };
}
function findEocd(bytes, dv) {
  for (let i = bytes.length - 22; i >= Math.max(0, bytes.length - 22 - 65536); i--) {
    if (bytes[i] === 0x41 && bytes[i + 1] === 0x4b && bytes[i + 2] === 0x05 && bytes[i + 3] === 0x06) {
      return { offset: i, cdSize: dv.getUint32(i + 12, true), cdOffset: dv.getUint32(i + 16, true), total: dv.getUint16(i + 10, true), eocdPlus22: i + 22 };
    }
  }
  return null;
}
const arkWalk = myArkWalk(arkBytes);
res.arkWalk = {
  entriesWalked: arkWalk.entries.length,
  chainEndsAtCdOffset: arkWalk.chainEnd === arkWalk.eocd.cdOffset,
  chainEnd: arkWalk.chainEnd, cdOffset: arkWalk.eocd.cdOffset,
  eocdTotal: arkWalk.eocd.total,
  eocdPlus22EqualsFileSize: arkWalk.eocd.eocdPlus22 === arkBytes.length,
  duplicateNames: arkWalk.entries.length - new Set(arkWalk.entries.map(e => e.name.toLowerCase())).size
};

// --- MY minimal BNT2 reader: footer + directory ---
const bntBytes = readFileSync(MODELS_BNT);
function myBntWalk(bytes) {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const magic = bytes.subarray(bytes.length - 4).toString('latin1');
  if (magic !== 'BNT2') throw new Error('bad BNT2 magic: ' + magic);
  const dirOffset = dv.getUint32(bytes.length - 8, true);
  const count = dv.getUint32(dirOffset, true);
  const entries = []; let p = dirOffset + 4;
  for (let i = 0; i < count; i++) {
    const nameStart = p;
    while (p < bytes.length && bytes[p] !== 0x0a) p++;
    const name = bytes.subarray(nameStart, p).toString('latin1');
    p++;
    const size = dv.getUint32(p, true), offset = dv.getUint32(p + 4, true), crc = dv.getUint32(p + 8, true);
    p += 16;
    entries.push({ i, name, size, offset, crc });
  }
  return { magic, dirOffset, count, entries, dirEnd: p, footerStart: bytes.length - 8 };
}
const bntWalk = myBntWalk(bntBytes);
let overlaps = 0, gaps = 0;
for (let i = 1; i < bntWalk.entries.length; i++) { if (bntWalk.entries[i].offset < bntWalk.entries[i - 1].offset + bntWalk.entries[i - 1].size) overlaps++; }
res.bntWalk = {
  magic: bntWalk.magic, count: bntWalk.count, dirEndEqualsFooterStart: bntWalk.dirEnd === bntWalk.footerStart,
  duplicateNames: bntWalk.entries.length - new Set(bntWalk.entries.map(e => e.name.toLowerCase())).size,
  overlapsDetected: overlaps,
  lastEntryEndsAtFooter: (() => { const last = bntWalk.entries[bntWalk.entries.length - 1]; return last.offset + last.size === bntWalk.footerStart; })()
};

// --- load phase-2 catalogs (executor artifacts, for COMPARISON) ---
function parseCsv(text) {
  const rows = []; let row = [], f = '', q = false, i = 0;
  while (i < text.length) { const c = text[i];
    if (q) { if (c === '"') { if (text[i+1]==='"'){f+='"';i+=2;continue;} q=false;i++;continue;} f+=c;i++;continue; }
    if (c === '"') { q = true; i++; continue; }
    if (c === ',') { row.push(f); f=''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(f); rows.push(row); row=[]; f=''; i++; continue; }
    f += c; i++; }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  return rows;
}
function loadCatalog(file) {
  const rows = parseCsv(readFileSync(join(PRIV, 'PHASE2_CATALOGS', file), 'utf8'));
  const hdr = rows[0];
  return rows.slice(1).filter(r => r.length > 1 || r[0] !== '').map(r => Object.fromEntries(hdr.map((h, i) => [h, r[i]])));
}
const arkCatalog = loadCatalog('CD2003_MODELS_ARK_ENTRIES.csv');
const bntCatalog = loadCatalog('PCG935_MODELS_BNT_ENTRIES.csv');
res.catalogArtifactRowCounts = {
  ark_csv_rows: arkCatalog.length, bnt_csv_rows: bntCatalog.length,
  claimed: { ark: 2492, bnt: 5596 }
};

// --- re-hash bounded samples: ARK 15 entries incl. 4 primaries; BNT 15 incl. entry 781/218757 ---
const arkByName = new Map(arkWalk.entries.map(e => [e.name.toLowerCase(), e]));
const bntByName = new Map(bntWalk.entries.map(e => [e.name.toLowerCase(), e]));
const catalogByName = (cat, nameCol) => new Map(cat.map(r => [r[nameCol].toLowerCase(), r]));

function hashArkEntry(e) { return createHash('sha256').update(arkBytes.subarray(e.dataOffset, e.dataOffset + e.uncompSize)).digest('hex'); }
function hashBntEntry(e) { return createHash('sha256').update(bntBytes.subarray(e.offset, e.offset + e.size)).digest('hex'); }
function crc32(buf) { let c, crc = 0xFFFFFFFF; for (let i = 0; i < buf.length; i++) { c = (crc ^ buf[i]) & 0xff; for (let k = 0; k < 8; k++) c = c & 1 ? (c >>> 1) ^ 0xEDB88320 : c >>> 1; crc = (crc >>> 8) ^ c; } return (crc ^ 0xFFFFFFFF) >>> 0; }

const primaries = ['192374.nif', '193207.nif', '193313.nif', '193684.nif'];
const arkSampleNames = [...primaries, '101411.nif', '212124.nif', '218524.nif', '206197.nif', '284804.nif', '17764.nif', '33281.nif', '127427.nif', '797.nif', '141921.nif', '128877.nif', '208597.nif'];
const arkCat = catalogByName(arkCatalog, 'name');
res.arkSampleRehash = [];
for (const nm of arkSampleNames) {
  const e = arkByName.get(nm), c = arkCat.get(nm);
  if (!e || !c) { res.arkSampleRehash.push({ name: nm, error: !e ? 'not found by MY walk' : 'not in catalog' }); continue; }
  const payload = arkBytes.subarray(e.dataOffset, e.dataOffset + e.uncompSize);
  const my = { sha256: createHash('sha256').update(payload).digest('hex'), crc: crc32(payload) };
  res.arkSampleRehash.push({
    name: nm, my_offset: e.dataOffset, my_size: e.uncompSize, my_sha256: my.sha256, my_crc32: my.crc,
    catalog: { offset: +c.data_offset, size: +c.uncompressed_size, sha256: c.payload_sha256, crc32: c.crc32_stored, match_crc: c.crc32_match },
    verdict_sha: my.sha256 === c.payload_sha256 ? 'MATCH' : 'MISMATCH',
    verdict_size: e.uncompSize === +c.uncompressed_size && (+c.stored_size) === e.compSize ? 'MATCH' : 'MISMATCH',
    verdict_crc: my.crc === e.crc && my.crc === (+c.crc32_computed) ? 'MATCH' : 'MISMATCH',
    verdict_offset: e.dataOffset === +c.data_offset ? 'MATCH' : 'MISMATCH'
  });
}

const bntCat = catalogByName(bntCatalog, 'name');
const bntSampleNames = ['218757.nif', '505775.nif', '505813.nif', '333375.nif', '131688.nif', '129311.nif', '65678.nif', '129375.nif', '192811.nif', '129281.nif', '335388.nif', '311193.nif', '218524.nif', '212124.nif', '423020.nif'];
res.bntSampleRehash = [];
for (const nm of bntSampleNames) {
  const e = bntByName.get(nm), c = bntCat.get(nm);
  if (!e || !c) { res.bntSampleRehash.push({ name: nm, error: !e ? 'not found by MY walk' : 'not in catalog' }); continue; }
  const payload = bntBytes.subarray(e.offset, e.offset + e.size);
  const my = { sha256: createHash('sha256').update(payload).digest('hex'), crc: crc32(payload) };
  res.bntSampleRehash.push({
    name: nm, my_entry_index: e.i, my_offset: e.offset, my_size: e.size, my_sha256: my.sha256, my_crc32: my.crc,
    catalog: { entry_index: +c.entry_index, offset: +c.offset, size: +c.size_bytes, sha256: c.payload_sha256, crc32: c.crc32_stored },
    verdict_sha: my.sha256 === c.payload_sha256 ? 'MATCH' : 'MISMATCH',
    verdict_size: e.size === +c.size_bytes ? 'MATCH' : 'MISMATCH',
    verdict_crc: my.crc === e.crc && my.crc === (+c.crc32_computed) ? 'MATCH' : 'MISMATCH',
    verdict_offset: e.offset === +c.offset && e.i === +c.entry_index ? 'MATCH' : 'MISMATCH'
  });
}
// entry 781 pin (218757.nif): the SceneIR-run pinned payload SHA
const e781 = bntWalk.entries[781];
res.entry781Check = { my_index: 781, name: e781.name, my_offset: e781.offset, my_size: e781.size, my_sha256: hashBntEntry(e781), catalog_sha256: (bntCat.get(e781.name.toLowerCase()) || {}).payload_sha256 };

// --- four primary pins vs phase-2 catalog values (sizes/SHA from catalog) ---
res.primaryPins = primaries.map(nm => {
  const e = arkByName.get(nm), c = arkCat.get(nm);
  return { name: nm, my_size: e.uncompSize, my_sha256: hashArkEntry(e), catalog_size: +c.uncompressed_size, catalog_sha256: c.payload_sha256, sha_match: hashArkEntry(e) === c.payload_sha256, size_match: e.uncompSize === +c.uncompressed_size };
});

// --- coverage arithmetic + counts verification against catalog artifacts ---
const arkVer = {}; for (const r of arkCatalog) arkVer[r.nif_version] = (arkVer[r.nif_version] || 0) + 1;
const bntVer = {}; for (const r of bntCatalog) { const k = (r.nif_engine + ' ' + r.nif_version).trim(); bntVer[k] = (bntVer[k] || 0) + 1; }
const texBntRows = parseCsv(readFileSync(join(PRIV, 'PHASE2_CATALOGS', 'PCG935_TEXTURES_BNT_ENTRIES.csv'), 'utf8')).slice(1).filter(r => r.length > 1 || r[0] !== '').length;
const texArkRows = parseCsv(readFileSync(join(PRIV, 'PHASE2_CATALOGS', 'CD2003_TEXTURES_ARK_ENTRIES.csv'), 'utf8')).slice(1).filter(r => r.length > 1 || r[0] !== '').length;
res.countsAndArithmetic = {
  ark_version_distribution_from_catalog: arkVer,
  bnt_version_distribution_from_catalog: bntVer,
  cd_arithmetic_1815_440_237: (arkVer['4.1.0.12'] || 0) + (arkVer['4.0.0.2'] || 0) + (arkVer['4.0.0.0'] || 0),
  pcg_arithmetic_4838_757_1: (bntVer['Gamebryo 10.1.0.0'] || 0) + (bntVer['NetImmerse 4.1.0.12'] || 0) + (bntVer['NetImmerse 4.0.0.2'] || 0),
  phase3_extension_1551_17_3270_758: 1551 + 17 + 3270 + 758,
  texture_ark_csv_rows: texArkRows, texture_bnt_csv_rows: texBntRows
};

writeFileSync(join(OUT, 'QC4_CATALOG_REHASH.json'), JSON.stringify(res, null, 1));
// console digest
const arkBad = res.arkSampleRehash.filter(r => r.verdict_sha !== 'MATCH' || r.verdict_crc !== 'MISMATCH-not-defined' && r.verdict_crc !== 'MATCH' || r.verdict_offset !== 'MATCH' || r.verdict_size !== 'MATCH');
const bntBad = res.bntSampleRehash.filter(r => r.verdict_sha !== 'MATCH' || r.verdict_crc !== 'MATCH' || r.verdict_offset !== 'MATCH' || r.verdict_size !== 'MATCH');
console.log(JSON.stringify({
  containerPins: res.containerIdentity.pinsCheck,
  arkWalk: res.arkWalk, bntWalk: res.bntWalk,
  arkSamples: res.arkSampleRehash.length, arkBad: arkBad.length,
  bntSamples: res.bntSampleRehash.length, bntBad: bntBad.length,
  entry781: res.entry781Check,
  primaryPins: res.primaryPins.map(p => ({ n: p.name, sha_match: p.sha_match, size_match: p.size_match })),
  counts: res.countsAndArithmetic
}, null, 1));
