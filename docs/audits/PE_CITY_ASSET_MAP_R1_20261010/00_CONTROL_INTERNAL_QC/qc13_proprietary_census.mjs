// QC13 — proprietary census (duty 6) + private artifact identity verification.
// Scans ALL changed/new text files for embedded proprietary payloads; verifies EVERY
// privateArtifactReferences entry (path+size+SHA256) from CATALOG_COVERAGE.json.
import { readFileSync, writeFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import { resolve, join, relative } from 'node:path';
import { createHash } from 'node:crypto';
import { execSync } from 'node:child_process';

const WT = 'D:\\Eudoria_Reconstruction\\12_WebGame\\pe-city-asset-map-r1';
const PKG = resolve(process.argv[2]);
const PRIV = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_CITY_ASSET_MAP_R1_20261010';
const res = { qcStep: 'QC13_PROPRIETARY_CENSUS', scanned: [], violations: [], privateArtifactCheck: [] };

// ---- enumerate changed/new files (git status --porcelain -uall) ----
const statusOut = execSync('git status --porcelain=v1 --untracked-files=all', { cwd: WT, encoding: 'utf8' });
const files = statusOut.split(/\r?\n/).filter(Boolean).map((l) => l.slice(3).trim()).filter(f => !f.startsWith('docs/audits/PE_CITY_ASSET_MAP_R1_20261010/00_CONTROL_INTERNAL_QC/'));
// plus the whole report package (mine + executor's)
function walk(dir) { const out = []; for (const e of readdirSync(dir, { withFileTypes: true })) { const p = join(dir, e.name); if (e.isDirectory()) out.push(...walk(p)); else out.push(p); } return out; }
const pkgFiles = walk(PKG).filter(p => !p.includes('00_CONTROL_INTERNAL_QC'));
const allFiles = [...new Set([...files.map(f => join(WT, f)), ...pkgFiles])];

// ---- payload scans ----
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47]);
function looksBinary(buf) { let suspicious = 0; const n = Math.min(buf.length, 8192); for (let i = 0; i < n; i++) { if (buf[i] === 0) { if (!(buf.length > 1 && (buf[0] === 0xff && buf[1] === 0xfe || buf[0] === 0xfe && buf[1] === 0xff))) { return true; } } if (buf[i] < 9 && buf[i] !== 0x09 && buf[i] !== 0x0a && buf[i] !== 0x0d) suspicious++; } return suspicious > n * 0.02; }

for (const p of allFiles) {
  if (!existsSync(p)) continue;
  const buf = readFileSync(p);
  const rel = relative(WT, p);
  const rec = { file: rel, bytes: buf.length };
  // encoding classes
  const isUtf16 = buf.length >= 2 && ((buf[0] === 0xff && buf[1] === 0xfe) || (buf[0] === 0xfe && buf[1] === 0xff));
  rec.encoding = isUtf16 ? 'utf16le/bom' : (looksBinary(buf) ? 'BINARY-ish' : 'text');
  if (rec.encoding === 'BINARY-ish') res.violations.push({ file: rel, kind: 'NON_TEXT_FILE_IN_CHANGED_SET', bytes: buf.length });
  // PNG bytes embedded?
  if (buf.includes(PNG_SIG)) res.violations.push({ file: rel, kind: 'PNG_BYTES_EMBEDDED' });
  const text = isUtf16 ? buf.toString('utf16le') : buf.toString('utf8');
  // DDS / TGA markers as binary magic in text: 'DDS ' at plausible data positions — count
  const ddsCount = (text.match(/\u0044\u0044\u0053\u0020/g) || []).length; // literal "DDS " also appears in words? count occurrences of "DDS" word separately
  // bulk NIF headers (data context)
  const nifHeaders = (text.match(/NetImmerse File Format/g) || []).length;
  const gbHeaders = (text.match(/Gamebryo File Format/g) || []).length;
  rec.nifHeaderStringCount = nifHeaders; rec.gamebryoHeaderStringCount = gbHeaders;
  if (nifHeaders > 5 || gbHeaders > 5) res.violations.push({ file: rel, kind: 'BULK_NIF_HEADERS', nifHeaders, gbHeaders });
  // long base64 runs
  const b64 = text.match(/[A-Za-z0-9+/]{300,}={0,2}/g) || [];
  rec.longBase64Runs = b64.length;
  if (b64.length) res.violations.push({ file: rel, kind: 'LONG_BASE64_RUN', count: b64.length, sample: b64[0].slice(0, 40) });
  // long hex runs (> 256 hex chars = > 128 bytes of raw payload)
  const hexRuns = text.match(/\b[0-9a-fA-F]{256,}\b/g) || [];
  rec.longHexRuns = hexRuns.length;
  if (hexRuns.length) res.violations.push({ file: rel, kind: 'LONG_HEX_RUN', count: hexRuns.length, sample: hexRuns[0].slice(0, 40) });
  // BNT2 magic as payload data (string constant mention is OK; count > 2 flags data context)
  const bnt2 = (text.match(/BNT2/g) || []).length;
  rec.bnt2StringCount = bnt2;
  if (bnt2 > 3) res.violations.push({ file: rel, kind: 'BNT2_MAGIC_REPEATED', count: bnt2 });
  res.scanned.push(rec);
}

// ---- private artifact identity verification (ALL referenced artifacts) ----
const cov = JSON.parse(readFileSync(join(PKG, 'CATALOG_COVERAGE.json'), 'utf8'));
const refs = cov.privateArtifactReferences?.artifacts ?? [];
for (const a of refs) {
  const exists = existsSync(a.path);
  let ok = false, detail = null;
  if (exists) {
    const st = statSync(a.path);
    const sha = createHash('sha256').update(readFileSync(a.path)).digest('hex');
    ok = st.size === a.sizeBytes && sha === a.sha256;
    detail = { sizeOk: st.size === a.sizeBytes, shaOk: sha === a.sha256 };
  }
  res.privateArtifactCheck.push({ path: a.path, exists, identityOk: ok, ...detail });
}
// also verify the phase-3/4 private artifacts referenced in DEEP_ANALYSIS/TEST_RESULTS (renders, models, native control)
const extraPriv = [
  join(PRIV, 'PHASE3_MODELS', '193313.nif'),
  join(PRIV, 'PHASE3_Renders', '193313_topdown_xz_filled.png'),
  join(PRIV, 'PHASE3_NativeControl', 'run_records.json'),
  join(PRIV, 'PHASE3_PCG935_BATCH', 'PCG935_NAME_EDGES.jsonl'),
  join(PRIV, 'PIXEL_RENDER', 'T9_PIXEL_RENDER_ASSET_MODE.png'),
  join(PRIV, 'PIXEL_RENDER_CATALOG', 'CATALOG_PIXEL_PREVIEW_193313.png'),
];
res.extraPrivateSpotChecks = extraPriv.map(p => ({ path: p, exists: existsSync(p), bytes: existsSync(p) ? statSync(p).size : null, sha256: existsSync(p) ? createHash('sha256').update(readFileSync(p)).digest('hex') : null }));

// one render non-triviality spot-check (private artifact usability)
if (existsSync(join(PRIV, 'PHASE3_Renders', '193313_topdown_xz_filled.png'))) {
  const { analyzePng } = await import('file:///' + join(WT, 'tools', 'pecompat', 'png_nontrivial.mjs').replace(/\\/g, '/'));
  const r = analyzePng(readFileSync(join(PRIV, 'PHASE3_Renders', '193313_topdown_xz_filled.png')), {});
  res.renderSpotCheck = { file: join(PRIV, 'PHASE3_Renders', '193313_topdown_xz_filled.png'), decodeOk: r.decodeOk, uniqueColors: r.stats?.full?.uniqueColors, lumaStdDev: r.stats?.full?.lumaStdDev, dims: r.dimensions };
}

res.summary = {
  filesScanned: res.scanned.length,
  violations: res.violations.length,
  privateRefs: refs.length,
  privateRefsOk: res.privateArtifactCheck.filter(x => x.identityOk).length,
  privateRefsMissing: res.privateArtifactCheck.filter(x => !x.exists).map(x => x.path),
  privateRefsMismatch: res.privateArtifactCheck.filter(x => x.exists && !x.identityOk).map(x => x.path)
};
writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC13_PROPRIETARY_CENSUS.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify(res.summary, null, 1));
console.log('VIOLATIONS:', JSON.stringify(res.violations.slice(0, 20), null, 1));
console.log('RENDER SPOT:', JSON.stringify(res.renderSpotCheck));
