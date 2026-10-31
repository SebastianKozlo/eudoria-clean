// inspector.js — JOB W07_NIF_INSPECTOR (attempt W07_a1, 2026-10-30).
// W09_a1 UPDATE (2026-10-30, additive): the page now dispatches the NIF
// FORMAT from the payload header version bytes BEFORE parsing:
//   0x0A010000 -> NifModelReader.parseWitnessModel (v10 witness, UNTOUCHED)
//   0x0401000C -> NifModelReader41.parseModel41   (the NEW dedicated
//                 NIF 4.1.0.12 adapter — a SEPARATE format module; the v10
//                 reader's version gate stays in place and still 4.1-LOUD-
//                 FAILs inside itself by design; the unit test N1 re-proves
//                 that gate). 218757/296445 now render as REAL IR through
//                 the shared typed IR contract (same field names + the same
//                 FILE-ORDER hex f32 convention), REFERENCE ASSET STAGE.
//
// PURPOSE: a NEW browser page that inspects NIF/source assets through THE
// SAME Rosetta pipeline (NOT a second parser): the raw NIF bytes go through
// src/pesource/NifModelReader.js (THE clean v10.1.0.0 witness reader — its
// version gate is UNTOUCHED; NIF 4.1 LOUD-FAILS by design) into the IR
// (the canonical extraction), and the page DISPLAYS:
//   (a) the block graph tree (type/name/children/depth, from children refs),
//   (b) per-node LOCAL TRS + WORLD TRS (parent-composed, NiTransform
//       operator* semantics: world = parent o child, row-dot rotate,
//       NO transpose — mirroring the repo's own corrected
//       src/pe2003/rosetta/bridges/gamebryoReference/niTransformAdapter.mjs
//       compose(): (P o C).s = P.s*C.s, .R = P.R*C.R,
//       .t = P.t + P.R(P.s * C.t)),
//   (c) materials (NiMaterialProperty colors, NiTexturingProperty slots,
//       the era Ark texture binding),
//   (d) controllers (v10: refs only — OPAQUE, honestly; 4.1 via reader41:
//       DECODED NiUVController/NiUVData blocks where implemented),
//   (e) a 3D viewport (Three r187, OrbitControls, axes helper — REFERENCE
//       ASSET STAGE: this is NOT a world placement, NOT world instance
//       positions; cm->m x0.01 + Z-up->Y-up (x,z,-y) bridges as the
//       model_witness.js CURRENT_RUNTIME_CALIBRATION),
//   (f) badges: era label, format version, unsupported/opaque blocks
//       (offset + span), provenance SHA256.
//
// HONESTY CONTRACT (loud failures are DISPLAYED, never faked):
//   - 457485.nif (ORIGINAL witness): FULL IR + render.
//   - other PCG_9_3_5 climate-0 model ids: ORIGINAL-DIRECT via PESourceMount
//     (the same chain as model_witness.js: mount Models.bnt SHA-verified ->
//     getModelResource -> NifModelReader).
//   - 457485_adapted.nif: the engine-oracle ADAPTED copy (NiArk-stripped) —
//     parseWitnessModel LOUD-FAILs at the witness-chain derivation (the
//     NiArkTextureExtraData is stripped); displayed VERBATIM + the W08
//     engine-oracle census as REFERENCE (fetched live, labeled).
//   - BABYLENGUIN.NIF (10.1.0.0): NifModelReader LOUD-FAILs at the first
//     block type outside the witness scope — displayed VERBATIM + the W08
//     engine-oracle L3b census as REFERENCE. NO fake partial parse.
//   - 218757/296445 (NIF 4.1.0.12): W09 — REAL IR via the dedicated
//     NifModelReader41 adapter (engine-oracle cross-checked 22/22 + census
//     on both fixtures in the W09 unit test); rendered as REFERENCE asset
//     stage. The W08 engine-oracle censuses remain shown as REFERENCE.
//
// All SHA pins verified in-session (W07_a1) before use; the page re-verifies
// every fetched payload against its pin and REFUSES on mismatch.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { parseWitnessModel } from '../src/pesource/NifModelReader.js';
import { parseModel41 } from '../src/pesource/NifModelReader41.js';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';

// ---------- fatal-error census (before anything can fail) ----------
window.__W07_ERRORS__ = [];
window.addEventListener('error', (e) => {
  window.__W07_ERRORS__.push({ kind: 'error', text: String(e.message ?? e), source: e.filename });
});
window.addEventListener('unhandledrejection', (e) => {
  window.__W07_ERRORS__.push({ kind: 'unhandledrejection', text: String(e.reason ?? e) });
});

// ---------- browser I/O adapter (the world_iso injection pattern) ----------
async function fetchBytes(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url}: HTTP ${res.status}`);
  return new Uint8Array(await res.arrayBuffer());
}
async function strictInflate(zlibBytes) {
  const ds = new DecompressionStream('deflate');
  const stream = new Blob([zlibBytes]).stream().pipeThrough(ds);
  const buf = await new Response(stream).arrayBuffer();
  return new Uint8Array(buf);
}
async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}
const io = { readFile: fetchBytes, inflate: strictInflate, sha256: sha256Hex };

// ---------- asset registry (SHA pins verified in-session W07_a1; see header) ----------
// source=fixture  : pinned NIF bytes over HTTP (fixtures live under the
//                   server root: WORK_ROOT/oracle_helper/fixtures + the
//                   allowlisted /assets/... exact routes in server.mjs).
// source=models_bnt: ORIGINAL-DIRECT — PESourceMount PCG_9_3_5 Models.bnt
//                   (SHA-verified mount) -> getModelResource(id) -> reader.
const ASSETS = {
  '457485': {
    source: 'fixture', url: '/oracle_helper/fixtures/457485.nif',
    sha256: '72479A7F4EEBE93401708FC539D153B6F865DD29D04490C8E1243C0BA72B2239',
    era: ERAS.PCG_9_3_5,
    label: '457485.nif — ORIGINAL witness (v10.1.0.0, NiArk era binding)',
    note: 'THE witness model. Fixture bytes are the extracted Models.bnt entry '
      + '<457485.nif> — byte-identity verified against the PCG_9_3_5 Models.bnt '
      + 'entry in-session (same SHA256) and re-verified at load.',
  },
  '457485_adapted': {
    source: 'fixture', url: '/oracle_helper/fixtures/457485_adapted.nif',
    sha256: '1014238EB5F156A977676223E84A7A4674C89CE3097BDC8F0459824A944C9623',
    era: ERAS.PCG_9_3_5,
    label: '457485_adapted.nif — engine-oracle ADAPTED copy (NiArk-stripped)',
    note: 'NiArk blocks stripped (W08 lossmap sidecar) so the stock Gamebryo '
      + 'NiStream can load it. The witness reader parses the 11 blocks but '
      + 'LOUD-FAILs at the render-model derivation (NiArkTextureExtraData '
      + 'absent) — displayed verbatim; W08 engine census shown as REFERENCE.',
  },
  'BABYLENGUIN': {
    source: 'fixture', url: '/assets/BABYLENGUIN.NIF',
    sha256: 'A86C49384E62DF41339101B62E48BE6DCAE10E06B5F7CAC39DC627CF89635EA9',
    era: 'GBR_SDK_10_1 (Gamebryo SDK control sample — REFERENCE, not a PE asset)',
    label: 'BABYLENGUIN.NIF — SDK control sample (v10.1.0.0)',
    note: 'Loads DIRECTLY in the stock engine (W08 L3b) but is OUTSIDE the '
      + 'NifModelReader witness scope (NiSourceTexture/NiSkin*/NiPSys*/'
      + 'NiBoneLODController... block types are not implemented) — the reader '
      + 'LOUD-FAILs at the first unknown block; displayed verbatim. The W08 '
      + 'engine-oracle census is shown as REFERENCE (fetched live).',
  },
  '218757': {
    source: 'fixture', url: '/assets/218757_stripped.nif',
    sha256: '13807FC14BDD45095043B3563F400E0B7B980220D070BDD5F082683DD6ADB947',
    era: 'PE42_CORPUS (reference stage — outpost)',
    label: '218757 — NIF 4.1.0.12 (W09: real IR via NifModelReader41)',
    note: 'NIF 4.1.0.12 — parsed by the DEDICATED adapter NifModelReader41 '
      + '(W09; R61-frozen-method semantics port, per-fixture boundary-'
      + 'validated; engine-oracle cross-check 22/22 + census in the W09 '
      + 'unit test). The v10 witness reader version gate stays untouched '
      + '(4.1 still LOUD-FAILs there BY DESIGN — negative control).',
  },
  '296445': {
    source: 'fixture', url: '/assets/296445_stripped.nif',
    sha256: '23EC7FF06C27F871AFE004113060DC6DA6C93D9D5FAF0CAAE7EAA81EF403C656',
    era: 'PE42_CORPUS (reference stage — slum building)',
    label: '296445 — NIF 4.1.0.12 (W09: real IR via NifModelReader41)',
    note: 'NIF 4.1.0.12 — parsed by the DEDICATED adapter NifModelReader41 '
      + '(W09). Carries the era controller pair NiUVController + NiUVData '
      + '(DECODED in the 4.1 IR — target "GeoTexanim01:0"). The W08 '
      + 'engine-oracle census (L4) is shown as REFERENCE alongside.',
  },
  // ORIGINAL-DIRECT climate-0 witnesses (all 10 parse FULL-OK — W07 unit test).
  '166878': bntAsset(166878), '166897': bntAsset(166897), '436223': bntAsset(436223),
  '436293': bntAsset(436293), '436300': bntAsset(436300), '457523': bntAsset(457523),
  '457532': bntAsset(457532), '457579': bntAsset(457579), '457699': bntAsset(457699),
};
function bntAsset(id) {
  return {
    source: 'models_bnt', modelId: id, era: ERAS.PCG_9_3_5,
    label: `${id}.nif — ORIGINAL-DIRECT (PCG_9_3_5 Models.bnt -> NifModelReader)`,
    note: 'The 10 VCL climate-0 (0.vcl) col0 model ids (foliage manifest scope). '
      + 'Loaded through the SAME Rosetta pipeline as model_witness.js: '
      + 'PESourceMount mount (SHA-verified) -> getModelResource -> NifModelReader.',
  };
}

// ---------- URL params ----------
const params = new URLSearchParams(location.search);
let assetKey = params.get('asset') || '457485';
if (!ASSETS[assetKey]) {
  if (/^\d+$/.test(assetKey)) { ASSETS[assetKey] = bntAsset(Number(assetKey)); }
  else assetKey = '457485';
}
const asset = ASSETS[assetKey];
const eraParam = params.get('era') || asset.era; // era label (validated for models_bnt below)

// ---------- DOM ----------
const el = (id) => document.getElementById(id);
const graphEl = el('graph'), detailsEl = el('details');
const badges = {
  era: el('b-era'), version: el('b-version'), revision: el('b-revision'),
  sha: el('b-sha'), status: el('b-status'), blocks: el('b-blocks'),
};
const sel = el('assetSelect');
for (const [k, a] of Object.entries(ASSETS)) {
  const o = document.createElement('option');
  o.value = k; o.textContent = a.label;
  sel.appendChild(o);
}
sel.value = assetKey;
sel.addEventListener('change', () => {
  const u = new URL(location.href);
  u.searchParams.set('asset', sel.value);
  location.href = u.href;
});

const state = {
  job: 'W07_NIF_INSPECTOR', attempt: 'W07_a1', asset: assetKey,
  source: asset.source, era: eraParam, label: asset.label,
  revision: THREE.REVISION, pipeline: 'NifModelReader.parseWitnessModel (src/pesource — THE Rosetta v10.1.0.0 witness reader; version gate UNTOUCHED)',
  payloadSha256: null, shaVerified: false, mountHashVerified: null,
  formatVersion: null, status: 'LOADING', fatalErrors: window.__W07_ERRORS__,
  numBlocks: null, typeCounts: null, graphNodeCount: null, maxDepth: null,
  controllerRefs: null, opaqueBlocks: null, loudFail: null,
};
window.__W07__ = state;

function setBadge(which, text, cls) {
  badges[which].innerHTML = text;
  badges[which].className = 'badge' + (cls ? ' ' + cls : '');
}

setBadge('revision', `three: <b>r${THREE.REVISION}</b>`);
setBadge('era', `era: <b>${state.era}</b>`);

// ---------- f32 bit helpers (the reader's FILE-ORDER hex convention) ----------
const bitsToF32 = (hex) => {
  const u = new Uint32Array(1);
  const b = new Uint8Array(u.buffer);
  for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
  return new Float32Array(u.buffer)[0];
};
const bitsVec = (v) => v.map(bitsToF32);
const bitsMat = (rows) => rows.map(bitsVec);
const fmt = (v, d = 6) => Number(v.toFixed(d));

// ---------- NiTransform compose (mirrors niTransformAdapter.mjs compose()) ----------
function composeTRS(P, C) {
  const R = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
    R[i][j] = P.rotation[i][0] * C.rotation[0][j] +
              P.rotation[i][1] * C.rotation[1][j] +
              P.rotation[i][2] * C.rotation[2][j];
  }
  const ct = C.translation;
  const t = [
    P.translation[0] + P.scale * (P.rotation[0][0] * ct[0] + P.rotation[0][1] * ct[1] + P.rotation[0][2] * ct[2]),
    P.translation[1] + P.scale * (P.rotation[1][0] * ct[0] + P.rotation[1][1] * ct[1] + P.rotation[1][2] * ct[2]),
    P.translation[2] + P.scale * (P.rotation[2][0] * ct[0] + P.rotation[2][1] * ct[1] + P.rotation[2][2] * ct[2]),
  ];
  return { translation: t, rotation: R, scale: P.scale * C.scale };
}

// ---------- load the asset ----------
let bytes = null, sourceNote = '';
async function loadAsset() {
  if (asset.source === 'fixture') {
    bytes = await fetchBytes(asset.url);
    const sha = await sha256Hex(bytes);
    state.payloadSha256 = sha;
    if (sha !== asset.sha256) {
      throw new Error(`[W07] SHA256 MISMATCH for ${asset.url}: got ${sha}, pinned ${asset.sha256} — REFUSING to display (provenance gate)`);
    }
    state.shaVerified = true;
    sourceNote = `fixture route ${asset.url} (SHA-pinned, verified at load)`;
  } else {
    if (eraParam !== ERAS.PCG_9_3_5) {
      throw new Error(`[W07] models_bnt source requires era PCG_9_3_5 (got '${eraParam}') — NO silent era substitution`);
    }
    const mount = new PESourceMount(io);
    const rec = await mount.mountEra({
      era: ERAS.PCG_9_3_5, container: 'Models/Models.bnt',
      path: '/pcg/Data/Models/Models.bnt', format: 'BNT2', verifyHash: true,
    });
    state.mountHashVerified = rec.hashVerified;
    const res = await mount.getModelResource({ era: ERAS.PCG_9_3_5, modelId: asset.modelId });
    bytes = res.payload;
    state.payloadSha256 = await sha256Hex(bytes);
    state.shaVerified = true; // container SHA-verified at mount; entry SHA recorded
    state.modelEntry = { name: `${asset.modelId}.nif`, size: res.entry.size, offset: res.entry.offset, crc32: res.entry.crc32 };
    sourceNote = `ORIGINAL-DIRECT: PCG_9_3_5 Models.bnt (mount SHA-verified) -> getModelResource(${asset.modelId}) [entry ${res.entry.size} B @${res.entry.offset}]`;
  }
}

// ---------- the pipeline (format dispatch -> THE reader; no second parser per format) ----------
let extraction = null, renderModel = null, loudFail = null, is41 = false;
function peekVersion(bytes) {
  // Minimal FORMAT sniff (dispatch only — both readers re-gate internally):
  // header text up to first \n, then the u32 version.
  const nl = bytes.indexOf(0x0a);
  if (nl < 0 || nl + 5 > bytes.length) return null;
  return (bytes[nl + 1]) | (bytes[nl + 2] << 8) | (bytes[nl + 3] << 16) | (bytes[nl + 4] << 24);
}
async function runPipeline() {
  try {
    const v = peekVersion(bytes) >>> 0;
    if (v === 0x0401000C) {
      // NIF 4.1.0.12 -> the DEDICATED adapter (W09). Same typed IR contract.
      const r = parseModel41(bytes, `${assetKey}.nif`);
      extraction = r.extraction; renderModel = r.renderModel; is41 = true;
      state.pipeline = 'NifModelReader41.parseModel41 (src/pesource — THE dedicated NIF 4.1.0.12 adapter, W09)';
    } else {
      // v10 witness path — UNTOUCHED (its own gate re-verifies the version).
      const r = parseWitnessModel(bytes, `${assetKey}.nif`);
      extraction = r.extraction; renderModel = r.renderModel; is41 = false;
    }
    state.status = 'IR_READY';
  } catch (e) {
    loudFail = { message: String(e.message ?? e), name: e.name ?? 'Error' };
    const m = loudFail.message;
    if (m.includes('NOT implemented') && m.includes('version')) state.status = 'ERA_GATE_LOUD_FAIL';
    else if (m.includes('UNKNOWN type')) state.status = 'WITNESS_SCOPE_LOUD_FAIL';
    else if (m.includes('witness chain incomplete')) state.status = 'WITNESS_CHAIN_LOUD_FAIL';
    else state.status = 'LOUD_FAIL';
    state.loudFail = loudFail;
  }
}

// ---------- graph (AVObject hierarchy from children refs) ----------
const AV_TYPES = new Set(['NiNode', 'NiTriShape']);
function buildGraph() {
  const blocks = extraction.blocks;
  const byIndex = new Map(blocks.map(b => [b.index, b]));
  const childOf = new Map(); // childIdx -> parentIdx
  for (const b of blocks) {
    if (b.type === 'NiNode' && Array.isArray(b.fields.children)) {
      // NULL child refs (-1) are legal NIF data — skipped, never graph edges.
      for (const c of b.fields.children) if (c >= 0) childOf.set(c, b.index);
    }
  }
  const roots = blocks.filter(b => AV_TYPES.has(b.type) && !childOf.has(b.index)).map(b => b.index);
  const nodes = [];
  let maxDepth = 0;
  function walk(idx, depth, worldTRS) {
    const b = byIndex.get(idx);
    if (!b) throw new Error(`[inspector] graph walk: block #${idx} not in IR (bad ref)`);
    const local = {
      translation: bitsVec(b.fields.translation),
      rotation: bitsMat(b.fields.rotation),
      scale: bitsToF32(b.fields.scale),
    };
    const world = composeTRS(worldTRS, local);
    nodes.push({ index: idx, type: b.type, name: b.fields.name, depth, local, world });
    if (depth > maxDepth) maxDepth = depth;
    if (b.type === 'NiNode' && Array.isArray(b.fields.children)) {
      for (const c of b.fields.children) if (c >= 0) walk(c, depth + 1, world);
    }
  }
  const identity = { translation: [0, 0, 0], rotation: [[1, 0, 0], [0, 1, 0], [0, 0, 1]], scale: 1 };
  for (const r of roots) walk(r, 0, identity);
  return { nodes, roots, childOf, byIndex, maxDepth };
}

function renderGraphPanel(g) {
  graphEl.innerHTML = '';
  const title = document.createElement('div');
  title.innerHTML = `<h3>BLOCK GRAPH — ${g.nodes.length} AVObject nodes, maxDepth ${g.maxDepth}, roots [${g.roots.join(',')}]</h3>`;
  graphEl.appendChild(title);
  for (const n of g.nodes) {
    const div = document.createElement('div');
    div.className = 'node';
    div.style.paddingLeft = (8 + n.depth * 14) + 'px';
    div.textContent = `#${n.index} ${n.type}`;
    if (n.name) div.textContent += ` "${n.name}"`;
    div.innerHTML += ` <span class="nodedepth">d${n.depth}</span>`;
    div.addEventListener('click', () => selectNode(n, g));
    div.dataset.idx = String(n.index);
    graphEl.appendChild(div);
    // ref lines (extraData / properties / controller / dataRef / effects)
    const b = g.byIndex.get(n.index);
    const refs = [];
    if (b.fields.extraData !== undefined) {
      // v10: array of refs; 4.1: SINGLE int ref (documented difference)
      if (Array.isArray(b.fields.extraData) && b.fields.extraData.length) refs.push(`extraData: [${b.fields.extraData.join(',')}]`);
      else if (!Array.isArray(b.fields.extraData) && b.fields.extraData !== -1) refs.push(`extraData: ${b.fields.extraData} (v4 single link)`);
    }
    if (b.fields.properties && b.fields.properties.length) refs.push(`properties: [${b.fields.properties.join(',')}]`);
    if (b.fields.controller !== undefined && b.fields.controller !== -1) refs.push(`controller: ${b.fields.controller}`);
    if (b.fields.dataRef !== undefined && b.fields.dataRef !== -1) refs.push(`data: ${b.fields.dataRef}`);
    if (b.fields.effects && b.fields.effects.length) refs.push(`effects: [${b.fields.effects.join(',')}]`);
    if (refs.length) {
      const rl = document.createElement('div');
      rl.className = 'refline';
      rl.style.paddingLeft = (20 + n.depth * 14) + 'px';
      rl.textContent = refs.join('  ');
      graphEl.appendChild(rl);
    }
  }
  // unreferenced / non-AV blocks census line
  const avSet = new Set(g.nodes.map(n => n.index));
  const others = extraction.blocks.filter(b => !avSet.has(b.index)).map(b => `#${b.index} ${b.type}`);
  const foot = document.createElement('div');
  foot.innerHTML = `<h3>NON-GRAPH BLOCKS (${others.length}) — properties/extra-data/data (referenced, not children)</h3>
    <div class="refline">${others.join(', ') || 'none'}</div>`;
  graphEl.appendChild(foot);
}

// ---------- details panels ----------
let selectedNode = null;
function selectNode(n, g) {
  selectedNode = n;
  document.querySelectorAll('.node').forEach(d => d.classList.toggle('sel', d.dataset.idx === String(n.index)));
  renderDetails(g);
}

function trsTable(label, trs) {
  const t = trs.translation, r = trs.rotation;
  return `<table><tr><td class="k">${label} translate</td><td>[${t.map(v => fmt(v, 4)).join(', ')}]</td></tr>
    <tr><td class="k">${label} rotate</td><td>[${r[0].map(v => fmt(v, 4)).join(', ')}]<br>[${r[1].map(v => fmt(v, 4)).join(', ')}]<br>[${r[2].map(v => fmt(v, 4)).join(', ')}]</td></tr>
    <tr><td class="k">${label} scale</td><td>${fmt(trs.scale, 6)}</td></tr></table>`;
}

function renderDetails(g) {
  const parts = [];
  parts.push(`<h3>SOURCE</h3><div>${sourceNote}<br>payload sha256: <b>${state.payloadSha256}</b> (verified ${state.shaVerified ? 'Y' : 'N'})</div>`);
  if (state.status === 'IR_READY') {
    parts.push(`<h3>HEADER</h3><table>
      <tr><td class="k">header text</td><td>${extraction.header.text}</td></tr>
      <tr><td class="k">version</td><td>${extraction.header.versionRaw} (${extraction.header.versionString})</td></tr>
      <tr><td class="k">userVersion</td><td>${extraction.header.userVersion ?? '— (none — v4 header)'}</td></tr>
      <tr><td class="k">numBlocks</td><td>${extraction.header.numBlocks}</td></tr>
      <tr><td class="k">blockTypes</td><td>${extraction.header.blockTypes ? extraction.header.blockTypes.join(', ') : '— (inline RTTI per block — no type table in 4.1)'}</td></tr>
      <tr><td class="k">dataStartOffset</td><td>${extraction.header.dataStartOffset}</td></tr>
      <tr><td class="k">file tail</td><td>${extraction.fileTailBytesLen} B — <span class="hex">${extraction.fileTailBytesHex.slice(0, 64)}${extraction.fileTailBytesLen > 32 ? '…' : ''}</span> (semantics UNKNOWN — recorded raw${extraction.fileTailBytesHex === '0100000000000000' ? '; NOTE: identical 8 B trailing pattern in both 4.1 fixtures (era observation, UNVERIFIED)' : ''})</td></tr>
    </table>`);
    if (selectedNode) {
      parts.push(`<h3>NODE #${selectedNode.index} ${selectedNode.type}${selectedNode.name ? ' "' + selectedNode.name + '"' : ''} (depth ${selectedNode.depth})</h3>`);
      parts.push(trsTable('local', selectedNode.local));
      parts.push(trsTable('world', selectedNode.world));
      parts.push('<div class="refline">world = parent ∘ child (NiTransform operator*: (P∘C).s=Ps·Cs, .R=P·C, .t=Pt+P.R(Ps·Ct) — niTransformAdapter compose parity)</div>');
    } else {
      parts.push('<div class="refline">select a graph node for local/world TRS</div>');
    }
    // materials
    const mats = extraction.blocks.filter(b => b.type === 'NiMaterialProperty');
    parts.push(`<h3>MATERIALS (${mats.length} NiMaterialProperty)</h3>`);
    for (const m of mats) {
      const f = m.fields;
      parts.push(`<table>
        <tr><td class="k">#${m.index} name</td><td>"${f.name}"${f.materialFlags !== undefined ? ` (materialFlags=0x${f.materialFlags.toString(16)} — 4.1-ONLY field)` : ''}</td></tr>
        <tr><td class="k">ambient</td><td>[${bitsVec(f.ambient).map(v => fmt(v, 4)).join(', ')}]</td></tr>
        <tr><td class="k">diffuse</td><td>[${bitsVec(f.diffuse).map(v => fmt(v, 4)).join(', ')}]</td></tr>
        <tr><td class="k">specular</td><td>[${bitsVec(f.specular).map(v => fmt(v, 4)).join(', ')}]</td></tr>
        <tr><td class="k">emissive</td><td>[${bitsVec(f.emissive).map(v => fmt(v, 4)).join(', ')}]</td></tr>
        <tr><td class="k">glossiness</td><td>${fmt(bitsToF32(f.glossiness), 4)}</td></tr>
        <tr><td class="k">alpha</td><td>${fmt(bitsToF32(f.alpha), 4)}</td></tr>
      </table>`);
    }
    // texture slots + era Ark binding
    const texprops = extraction.blocks.filter(b => b.type === 'NiTexturingProperty');
    const arks = extraction.blocks.filter(b => b.type === 'NiArkTextureExtraData');
    parts.push(`<h3>TEXTURE PROPERTIES (${texprops.length}) / ARK BINDING (${arks.length})</h3>`);
    for (const tp of texprops) {
      const rows = tp.fields.textures.map((s, i) => {
        if (!s.has) return `<tr><td class="k">slot ${i}</td><td>has=0</td></tr>`;
        // shared: has/source/clamp/filter/uv_set; 4.1-ONLY: ps2_l/ps2_k/unk1; v10-ONLY: tail_A/tail_B/transform_present
        const shared = `has=1 source=${s.source} clamp=${s.clamp} filter=${s.filter} uv_set=${s.uv_set}`;
        const era = s.ps2_l !== undefined
          ? ` ps2_l=${s.ps2_l} ps2_k=${s.ps2_k} unk1=${s.unk1} (4.1 TexDesc)`
          : (s.transform_present !== undefined ? ` transform=${s.transform_present}` : '');
        return `<tr><td class="k">slot ${i}</td><td>${shared}${era}</td></tr>`;
      }).join('');
      const flagsNote = tp.fields.texFlags !== undefined
        ? ` (texFlags=0x${tp.fields.texFlags.toString(16)}, applyMode=${tp.fields.applyMode} — 4.1 field names)`
        : ` (fieldA=${tp.fields.fieldA}, fieldB=${tp.fields.fieldB})`;
      parts.push(`<table><tr><td class="k">#${tp.index}</td><td>NiTexturingProperty (count ${tp.fields.textureCount})${flagsNote}</td></tr>${rows}</table>`);
    }
    for (const ak of arks) {
      for (const e of ak.fields.entries) {
        parts.push(`<table>
          <tr><td class="k">#${ak.index} entry</td><td>"${e.name}" slotType=${e.f1} ref=${e.ref} (-> NiTexturingProperty block)</td></tr>
          <tr><td class="k">textureId</td><td><b>${e.textureId}</b> (era Textures.bnt entry id; unk[1..4]=FFFFFFFF, unk[5..8]=u32 LE id — canon rule)</td></tr>
        </table>`);
      }
    }
    const alphas = extraction.blocks.filter(b => b.type === 'NiAlphaProperty');
    for (const a of alphas) {
      parts.push(`<table><tr><td class="k">#${a.index} alpha</td><td>flags=0x${a.fields.alphaFlags.toString(16)} threshold=${a.fields.alphaThreshold}</td></tr></table>`);
    }
    // controllers
    const ctrl = [];
    for (const b of extraction.blocks) {
      if (b.fields && b.fields.controller !== undefined) ctrl.push({ i: b.index, t: b.type, n: b.fields.name, c: b.fields.controller });
    }
    const active = ctrl.filter(c => c.c !== -1 && c.c !== undefined);
    parts.push(`<h3>CONTROLLERS (${active.length} active refs / ${ctrl.length} blocks with controller field)</h3>`);
    if (is41 && renderModel.controllers && renderModel.controllers.length) {
      // 4.1: DECODED controller blocks (the implemented types) — real fields,
      // cross-checked against the engine oracle (W09 unit gates B8a-e).
      for (const c of renderModel.controllers) {
        if (c.type === 'NiUVController') {
          parts.push(`<table>
            <tr><td class="k">#${c.blockIndex} NiUVController</td><td>DECODED (4.1 adapter)</td></tr>
            <tr><td class="k">target</td><td>#${c.targetIndex} ${c.targetType} "${c.targetName}"</td></tr>
            <tr><td class="k">freq / phase</td><td>${fmt(c.frequency, 6)} / ${fmt(c.phase, 6)}</td></tr>
            <tr><td class="k">begin / end</td><td>${fmt(c.startTime, 6)} / ${fmt(c.stopTime, 6)}</td></tr>
            <tr><td class="k">data</td><td>#${c.dataRef} (NiUVData)</td></tr>
          </table>`);
        } else if (c.type === 'NiUVData') {
          parts.push(`<table>
            <tr><td class="k">#${c.blockIndex} NiUVData</td><td>DECODED (4.1 adapter)</td></tr>
            <tr><td class="k">key groups</td><td>${c.uvGroups.map(g => `${g.numKeys} keys (interp ${g.interpolation})`).join(' | ')}</td></tr>
          </table>`);
        }
      }
      parts.push('<div class="refline">4.1 controller payloads NiUVController/NiUVData are DECODED in the reader41 IR (the two era controller types these fixtures carry); other controller block types remain opaque.</div>');
    } else if (active.length) {
      for (const c of active) parts.push(`<div>#${c.i} ${c.t}${c.n ? ' "' + c.n + '"' : ''} -> controller ref <b>${c.c}</b> (OPAQUE — no controller block type implemented in the v10 witness scope)</div>`);
    } else {
      parts.push('<div class="refline">all controller refs are -1 (none) in this asset</div>');
    }
    if (!is41) parts.push('<div class="refline">controller PAYLOADS are outside the v10 witness scope — refs are recorded opaque; the W08 engine oracle provides controller censuses (type/target/freq/phase) for reference assets.</div>');
    // unsupported / opaque blocks
    const opaque = [];
    if (is41 && extraction.opaqueBlocks) {
      for (const o of extraction.opaqueBlocks) {
        opaque.push(`#${o.index} ${o.type} — OPAQUE @${o.offset} span ${o.span} B (boundary=${o.boundaryMethod}; known-RTTI-anchored, no printable-string guessing)`);
      }
    }
    for (const b of extraction.blocks) {
      if (b.type === 'NiArkViewportInfoExtraData') {
        opaque.push(`#${b.index} NiArkViewportInfoExtraData — opaque ext @${b.fields.extStart}..${b.fields.extEnd} (${b.fields.extSize} B, boundary=${b.fields.boundaryMethod})`);
      } else if (b.type === 'NiArkAnimationExtraData' && b.fields.extSize > 0) {
        opaque.push(`#${b.index} NiArkAnimationExtraData — opaque ext ${b.fields.extSize} B @${b.payloadStart}..${b.blockEnd} (variant ${b.fields.variant}, boundary=${b.fields.boundaryMethod})`);
      } else if (b.type === 'NiArkImporterExtraData') {
        opaque.push(`#${b.index} NiArkImporterExtraData — opaque trailing 38 B @${b.payloadStart}..${b.blockEnd}`);
      }
    }
    if (extraction.fileTailBytesLen > 0) opaque.push(`file tail — ${extraction.fileTailBytesLen} B opaque after last block (semantics UNKNOWN)`);
    state.opaqueBlocks = opaque;
    parts.push(`<h3>UNSUPPORTED / OPAQUE (${opaque.length})</h3>`);
    for (const o of opaque) parts.push(`<div class="refline">${o}</div>`);
  } else {
    // LOUD FAIL display — verbatim, no fake IR
    parts.push(`<div class="failbox">Reader LOUD FAIL (${state.status}):
${loudFail.message}

NO partial IR is displayed: each format's reader either returns the FULL canonical extraction or fails LOUDLY (fail-closed parity with the R61 oracle). This page does not fake a partial parse; per-version readers are dispatched by the header version (one reader per FORMAT, never two for the same format).</div>`);
    if (state.status === 'ERA_GATE_LOUD_FAIL') {
      parts.push(`<div class="refbox">Unsupported NIF version for BOTH readers (the format dispatch found neither 0x0401000C (NifModelReader41) nor 0x0A010000 (NifModelReader witness)). The witness-reader version gate is INTENTIONAL and stays untouched. NIF 4.1.0.12 assets (218757/296445) now dispatch to the W09 dedicated adapter and parse as real IR; this box appears only for other unsupported versions. REFERENCE data below (if any) is engine-oracle campaign output (W08), labeled REFERENCE, not parsed here.</div>`);
    }
    if (state.status === 'WITNESS_CHAIN_LOUD_FAIL') {
      parts.push(`<div class="refbox">This is the ADAPTED copy (NiArk blocks stripped so the stock engine NiStream could load it — W08). All 11 blocks parse internally, but the witness RENDER-MODEL derivation requires the NiArkTextureExtraData era binding, which was stripped — the reader fails LOUDLY at that derivation and withholds the IR by design. The W08 engine census below is REFERENCE data.</div>`);
    }
    if (state.status === 'WITNESS_SCOPE_LOUD_FAIL') {
      parts.push(`<div class="refbox">BABYLENGUIN.NIF is a Gamebryo SDK control sample (v10.1.0.0, loads in the stock engine — W08 L3b) but carries block types OUTSIDE the witness scope (NiSourceTexture, NiSkinInstance, NiParticleSystem, NiBoneLODController, lights...). The v10 witness reader implements ONLY the 14 witness chain types; it fails closed at the first unknown block. The W08 engine census below is REFERENCE data (not a JS parse).</div>`);
    }
  }
  detailsEl.innerHTML = parts.join('');
}

// ---------- REFERENCE oracle data (fetched live, labeled; never a parse) ----------
const REFERENCE_BY_ASSET = {
  '457485_adapted': { url: '/oracle_helper/out/L1b_457485_adapted.json', label: 'W08 engine oracle — L1b census (stock Gamebryo 1.2 on the ADAPTED copy)' },
  'BABYLENGUIN': { url: '/oracle_helper/out/L3b_babylnguin.json', label: 'W08 engine oracle — L3b census (stock Gamebryo 1.2, loads DIRECTLY)' },
  '218757': { url: '/oracle_helper/compare/COMPARE_218757.json', label: 'W08 comparison — R61 peReader (4.1 JS lineage) vs engine oracle, 22/22 MATCH (REFERENCE)' },
  '296445': { url: '/oracle_helper/out/L4_296445_stripped.json', label: 'W08 engine oracle — L4 census (REFERENCE)' },
};
async function showReference() {
  const ref = REFERENCE_BY_ASSET[assetKey];
  if (!ref) return;
  try {
    const j = await (await fetch(ref.url)).json();
    const box = document.createElement('div');
    box.className = 'refbox';
    const summary = j.typeCounts
      ? `census ${j.blockCensus} blocks; typeCounts ${JSON.stringify(j.typeCounts)}; version ${j.nifVersion}; topObjects ${j.topObjects}; controllerBlocks ${j.controllerBlockCount ?? j.controllerBlocks ?? '?'}`
      : JSON.stringify(j).slice(0, 600) + '…';
    box.innerHTML = `<b>REFERENCE (not parsed by NifModelReader):</b><br>${ref.label}<br>${ref.url}<br>${summary}`;
    detailsEl.appendChild(box);
    state.referenceOracle = { url: ref.url, label: ref.label, blockCensus: j.blockCensus ?? null, typeCounts: j.typeCounts ?? null, nifVersion: j.nifVersion ?? null };
  } catch (e) {
    const box = document.createElement('div');
    box.className = 'refbox';
    box.textContent = `REFERENCE fetch FAILED (${ref.url}): ${e.message} — no reference shown (non-fatal)`;
    detailsEl.appendChild(box);
  }
}

// ---------- 3D viewport (REFERENCE ASSET STAGE — Three r187) ----------
let renderer = null, scene = null, camera = null, controls = null;
function initViewport() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x14141c);
  const w = el('viewwrap').clientWidth || 640, h = el('viewwrap').clientHeight || 480;
  camera = new THREE.PerspectiveCamera(50, w / h, 0.01, 1000);
  renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(w, h);
  el('view').appendChild(renderer.domElement);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  // REFERENCE STAGE helpers (explicitly diagnostic, not the PE environment):
  const axes = new THREE.AxesHelper(1.0); // 1 m axes at origin
  scene.add(axes);
  const grid = new THREE.GridHelper(4, 8, 0x334155, 0x1e293b);
  scene.add(grid);
  window.addEventListener('resize', onResize);
  renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
}
function onResize() {
  const w = el('viewwrap').clientWidth || 640, h = el('viewwrap').clientHeight || 480;
  camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h);
}

function addRenderModel() {
  // [P-UNITS]/[P-AXIS] CURRENT_RUNTIME_CALIBRATION (model_witness.js parity):
  // NIF cm -> m x0.01; NIF Z-up -> Three Y-up via (x, z, -y).
  const UNIT = 0.01;
  const n = renderModel.numVertices;
  const positions = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    positions[i * 3] = renderModel.positions[i * 3] * UNIT;
    positions[i * 3 + 1] = renderModel.positions[i * 3 + 2] * UNIT;
    positions[i * 3 + 2] = -renderModel.positions[i * 3 + 1] * UNIT;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  if (renderModel.normals) {
    const normals = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      normals[i * 3] = renderModel.normals[i * 3];
      normals[i * 3 + 1] = renderModel.normals[i * 3 + 2];
      normals[i * 3 + 2] = -renderModel.normals[i * 3 + 1];
    }
    geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
  }
  if (renderModel.uvSets && renderModel.uvSets[0]) {
    geometry.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(renderModel.uvSets[0]), 2));
  }
  if (renderModel.colors) {
    geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(renderModel.colors), 4));
  }
  geometry.setIndex(new THREE.BufferAttribute(renderModel.index, 1));
  const alphaThreshold = renderModel.alpha ? renderModel.alpha.threshold : 0;
  const alphaBlendOn = renderModel.alpha ? (renderModel.alpha.flags & 1) === 1 : false;
  const material = new THREE.MeshBasicMaterial({
    vertexColors: !!renderModel.colors,
    transparent: alphaBlendOn,
    alphaTest: alphaThreshold / 255.0,
    side: THREE.DoubleSide,
  });
  material.color.set(0xffffff);
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = `witness:${renderModel.shapeName}`;
  scene.add(mesh);
  // NOTE (honest): the era TEXTURE is not fetched here (reference stage —
  // resolveTexture would mount the 974 MB era Textures.bnt); the Ark
  // textureId is displayed in the materials panel instead.
  const center = renderModel.center.map(v => v * UNIT);
  const camDist = Math.max(renderModel.radius * UNIT * 2.6, 0.5);
  camera.position.set(center[0] + camDist * 0.55, center[1] + camDist * 0.42, center[2] + camDist * 0.72);
  camera.near = Math.max(camDist / 1000, 0.001);
  camera.far = camDist * 50;
  camera.updateProjectionMatrix();
  controls.target.set(center[0], center[1], center[2]);
  el('viewmsg').textContent = '';
}

/** W09: multi-shape render for the NIF 4.1.0.12 reference stage (the 4.1
 * fixtures carry 14..30 shapes). SAME calibration as the witness render:
 * [P-UNITS]/[P-AXIS] CURRENT_RUNTIME_CALIBRATION (model_witness.js parity):
 * NIF cm -> m x0.01; NIF Z-up -> Three Y-up via (x, z, -y). Per-shape WORLD
 * TRS from the reader41 IR (NiTransform compose parity) applied as the mesh
 * transform — REFERENCE ASSET STAGE, NOT world instance positions. */
function addRenderModel41() {
  const UNIT = 0.01;
  let boundsCenter = [0, 0, 0], boundsRadius = 1;
  const all = renderModel.shapes;
  // overall bounds from per-shape center/radius (meters, Y-up bridged)
  const centers = all.map(sh => [sh.center[0] * UNIT, sh.center[2] * UNIT, -sh.center[1] * UNIT]);
  let cx = 0, cy = 0, cz = 0;
  for (const c of centers) { cx += c[0]; cy += c[1]; cz += c[2]; }
  if (centers.length) { cx /= centers.length; cy /= centers.length; cz /= centers.length; }
  let maxR = 0;
  for (let i = 0; i < all.length; i++) {
    const d = Math.hypot(centers[i][0] - cx, centers[i][1] - cy, centers[i][2] - cz) + all[i].radius * UNIT;
    if (d > maxR) maxR = d;
  }
  boundsCenter = [cx, cy, cz];
  boundsRadius = Math.max(maxR, 0.1);
  for (const sh of all) {
    const n = sh.numVertices;
    const positions = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      positions[i * 3] = sh.positions[i * 3] * UNIT;
      positions[i * 3 + 1] = sh.positions[i * 3 + 2] * UNIT;
      positions[i * 3 + 2] = -sh.positions[i * 3 + 1] * UNIT;
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    if (sh.normals) {
      const normals = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) {
        normals[i * 3] = sh.normals[i * 3];
        normals[i * 3 + 1] = sh.normals[i * 3 + 2];
        normals[i * 3 + 2] = -sh.normals[i * 3 + 1];
      }
      geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
    }
    if (sh.uvSets && sh.uvSets[0]) geometry.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(sh.uvSets[0]), 2));
    if (sh.colors) geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(sh.colors), 4));
    geometry.setIndex(new THREE.BufferAttribute(sh.index, 1));
    const alphaThreshold = sh.alphaProp ? sh.alphaProp.threshold : 0;
    const alphaBlendOn = sh.alphaProp ? (sh.alphaProp.flags & 1) === 1 : false;
    const material = new THREE.MeshBasicMaterial({
      vertexColors: !!sh.colors,
      transparent: alphaBlendOn,
      alphaTest: alphaThreshold / 255.0,
      side: THREE.DoubleSide,
    });
    if (sh.material) {
      // NiMaterialProperty diffuse as the flat-color tint (reference stage —
      // the era TEXTURES are not mounted; the W08 finding applies: an era
      // BASE slot with source=-1 binds NO texture file here)
      material.color.setRGB(sh.material.diffuse[0], sh.material.diffuse[1], sh.material.diffuse[2]);
    } else {
      material.color.set(0x9aa3b0);
    }
    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = `nif41:${sh.shapeName}`;
    // world TRS (row-vector NiTransform convention) -> THREE matrix
    // (column-vector): rotation transposed; translation bridged (x, z, -y).
    const w = sh.worldTRS;
    const m = new THREE.Matrix4();
    m.set(
      w.rotation[0][0], w.rotation[1][0], w.rotation[2][0], w.translation[0] * UNIT,
      w.rotation[0][2], w.rotation[1][2], w.rotation[2][2], w.translation[2] * UNIT,
      -w.rotation[0][1], -w.rotation[1][1], -w.rotation[2][1], -w.translation[1] * UNIT,
      0, 0, 0, w.scale,
    );
    mesh.matrixAutoUpdate = false;
    mesh.matrix.copy(m);
    scene.add(mesh);
  }
  const camDist = Math.max(boundsRadius * 2.6, 0.5);
  camera.position.set(boundsCenter[0] + camDist * 0.55, boundsCenter[1] + camDist * 0.42, boundsCenter[2] + camDist * 0.72);
  camera.near = Math.max(camDist / 1000, 0.001);
  camera.far = camDist * 50;
  camera.updateProjectionMatrix();
  controls.target.set(boundsCenter[0], boundsCenter[1], boundsCenter[2]);
  el('viewmsg').textContent = '';
}

// ---------- badges + state publication ----------
function publishBadges() {
  setBadge('sha', `sha256: <b>${state.payloadSha256 ? state.payloadSha256.slice(0, 12) + '…' : '—'}</b> verified=${state.shaVerified ? 'Y' : 'N'}`);
  setBadge('version', `format: <b>${state.formatVersion ?? '—'}</b>`);
  const stCls = state.status === 'IR_READY' ? 'ok' : 'fail';
  setBadge('status', `status: <b>${state.status}</b>`, stCls);
  setBadge('blocks', `blocks: <b>${state.numBlocks ?? '—'}</b> graphNodes: <b>${state.graphNodeCount ?? '—'}</b>`);
  const eraCls = String(state.era).includes('REFERENCE') || String(state.era).includes('SDK') || String(state.era).includes('PE42') ? 'ref' : '';
  setBadge('era', `era: <b>${state.era}</b>`, eraCls);
}

// ---------- main ----------
(async function main() {
  initViewport();
  try {
    await loadAsset();
    await runPipeline();
    if (state.status === 'IR_READY') {
      const counts = {};
      for (const b of extraction.blocks) counts[b.type] = (counts[b.type] || 0) + 1;
      state.numBlocks = extraction.blocks.length;
      state.typeCounts = counts;
      state.formatVersion = extraction.header.versionString;
      const g = buildGraph();
      state.graphNodeCount = g.nodes.length;
      state.maxDepth = g.maxDepth;
      const ctrl = extraction.blocks.filter(b => b.fields && b.fields.controller !== undefined && b.fields.controller !== -1);
      state.controllerRefs = ctrl.map(b => ({ block: b.index, type: b.type, ref: b.fields.controller }));
      renderGraphPanel(g);
      selectedNode = g.nodes[0] || null;
      renderDetails(g);
      if (is41) addRenderModel41();
      else addRenderModel();
    } else {
      // fail assets: header version is known only for the era-gate case (from
      // the verbatim error) — honest, no header peek, no second parser.
      if (state.status === 'ERA_GATE_LOUD_FAIL') state.formatVersion = '4.1.0.12 (version-gate LOUD FAIL — header version from the gate error, no parse)';
      else state.formatVersion = '10.1.0.0 (gate passed; parse failed later — see status)';
      graphEl.innerHTML = `<div class="failbox">GRAPH UNAVAILABLE — ${state.status}.
The block graph is derived from the IR; the IR is withheld on LOUD FAIL (fail-closed). No second parser is used and no partial structure is invented.</div>`;
      renderDetails(null);
      el('viewmsg').textContent = 'NO RENDER MODEL — parse LOUD FAIL (honest: nothing is rendered for a failed parse)';
    }
    await showReference();
    publishBadges();
    state.doneAt = new Date().toISOString();
  } catch (e) {
    state.status = 'ERROR';
    state.error = String(e.message ?? e);
    window.__W07_ERRORS__.push({ kind: 'fatal', text: state.error });
    graphEl.innerHTML = `<div class="failbox">FATAL: ${state.error}</div>`;
    detailsEl.innerHTML = `<div class="failbox">${state.error}</div>`;
    publishBadges();
  }
})();
