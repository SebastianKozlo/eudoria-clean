// server.mjs — static file server for the eudoria-clean runtime (ITER 019).
// Serves the repo root so that ES-module import maps can reference
// /node_modules/three/... directly. Read-only on originals: the runtime
// fetches original PE containers from ABSOLUTE paths exposed explicitly
// via /pcg/... aliases (see ALIASES) — never writes.
//
// Port: env PORT override, default 8140 (W03 ISO_TERRAIN_VERTICAL_SLICE
// contract; 8141 fallback if occupied — chosen port is written to the lease).
// 8130/8132 were earlier ITER session servers; 8000/8124/8126 belong to
// legacy eudoria-web servers.
//
// W03: exact route '/iso/50.bnt' serves the RECOVERED PE 5.1.0.0 ISO
// (PC Gamer Nov2003) terrain container, read-only, SHA-pinned by the page.
// This is the ONLY /iso/... route (allowlist — no directory under /iso/).
'use strict';
import http from 'node:http';
import { promises as fs, writeFileSync, mkdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { ArkArchive } from './src/pesource/ArkArchive.js';
import { parseModel41, NIF_V4_1_0_12 } from './src/pesource/NifModelReader41.js';
// AV-5 (job AV5_INTEGRATION, 2026-10-31): version-dispatch — NIF 4.0.0.0 /
// 4.0.0.2 members go to the dedicated AV-4 adapter (NifModelReader40.js,
// 638/677 renderable, layout from bytes per AV-4 census).
import { parseModel40, NIF_V4_0_0_0, NIF_V4_0_0_2 } from './src/pesource/NifModelReader40.js';
// AV-3 (job AV3_ANIMATION, 2026-10-31): closure-exact decoder for the OPAQUE
// NIF 4.1 animation blocks (NiKeyframeController/NiKeyframeData/
// NiTextKeyExtraData) — tools/av3/kf41.mjs (anchored-span closure gate inside).
import { decodeKeyframeBlocks41 } from './tools/av3/kf41.mjs';
// AV-5: closure-exact NIF 4.1 skin decoder (NiSkinInstance/NiSkinData/
// NiSkinPartition — layout FROM BYTES, tools/av5/skin41.mjs; bind law
// W_i*SkinToBone_i physically verified on the corpus, tools/av5/skin_verify.mjs).
import { decodeSkinBlocks41, buildSkinBinding } from './tools/av5/skin41.mjs';

// ---- AV-2 (PE_ISO_ASSET_VIEWER campaign, job AV2_VIEWER, 2026-10-31) ----
// Bounded /api/assets/* routes for the asset viewer page (compat/assets.html).
// Physical fail-closed pins: the two ORIGINAL era containers are opened
// READ-ONLY from the pinned paths below (env override allowed); a size
// mismatch against the pinned byte counts is a LOUD failure (500).
// No whole-container route, no arbitrary-path route: index + single-model
// parse + single-texture payload, all allowlist/index-derived.
const MODELS_ARK_PATH = process.env.AV_MODELS_ARK ||
  'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const TEXTURES_ARK_PATH = process.env.AV_TEXTURES_ARK ||
  'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Textures.ark';
const MODELS_ARK_PIN_BYTES = 128742137;   // physical pin (2026-10-31 stat)
const TEXTURES_ARK_PIN_BYTES = 289585581; // physical pin (2026-10-31 stat)
const AV_ERA = 'ISO_5_1_0_0';

let modelsArk = null, modelsArkEntries = null;
let texturesArk = null;

async function loadArk(pinnedPath, pinBytes, label) {
  const st = statSync(pinnedPath);
  if (st.size !== pinBytes) {
    throw new Error(`[AV-2] ${label} FAIL-CLOSED pin: size ${st.size} != pinned ${pinBytes} (${pinnedPath})`);
  }
  const buf = await fs.readFile(pinnedPath);
  return new ArkArchive(new Uint8Array(buf));
}
async function getModelsArk() {
  if (!modelsArk) {
    modelsArk = await loadArk(MODELS_ARK_PATH, MODELS_ARK_PIN_BYTES, 'Models.ark');
    modelsArkEntries = modelsArk.entries(); // EOCD cross-check inside
  }
  return modelsArk;
}
async function getTexturesArk() {
  if (!texturesArk) texturesArk = await loadArk(TEXTURES_ARK_PATH, TEXTURES_ARK_PIN_BYTES, 'Textures.ark');
  return texturesArk;
}
function sha256Hex(u8) {
  return createHash('sha256').update(u8).digest('hex').toUpperCase();
}

/** Structural NiSourceTexture name extraction (AV-2): for an OPAQUE
 * NiSourceTexture block the NiObjectNET base's SizedString name follows the
 * RTTI type string — two consecutive sized strings, decoded structurally
 * (NO printable-string scan). Returns null when the layout does not match. */
function extractOpaqueBlockName(payload, rttiStart) {
  try {
    const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
    const rttiLen = dv.getInt32(rttiStart, true);
    if (rttiLen < 1 || rttiLen > 256) return null;
    const namePos = rttiStart + 4 + rttiLen;
    const nameLen = dv.getInt32(namePos, true);
    if (nameLen < 0 || nameLen > 1024 || namePos + 4 + nameLen > payload.length) return null;
    let name = '';
    for (let i = 0; i < nameLen; i++) name += String.fromCharCode(payload[namePos + 4 + i]);
    return name;
  } catch { return null; }
}

/** AV-2 era-canon texture binding: in this corpus the NiTexturingProperty
 * TexDesc slots carry source=-1 (NULL) and the REAL texture binding is the
 * PE-proprietary NiArkTextureExtraData block: a SEQUENCE of records
 *   [u32 recordIndex][u32 unk][u32 nameLen][name '<shape>…<BASE|DETAIL>']
 *   [u32 0][FFFFFFFF][u32 counter][00][FFFFFFFF][u32 LE texture id]
 * (the id follows the LAST FFFFFFFF marker of the record region — the same
 * canon rule documented by inspector.js for the v10 block:
 * "unk[1..4]=FFFFFFFF, unk[5..8]=u32 LE id"; measured 2026-10-31 on Models.ark
 * members 103241 and 128816 where the id sits at the region end while an
 * earlier FFFFFFFF precedes a small per-record counter — taking the FIRST
 * marker pairs the counter as the id: VERIFIED BUG, fixed here).
 * Decoding is ANCHORED structural (sized-string + FFFFFFFF pair), never a
 * free printable-string guess. Returns [{name, textureId}]. */
function decodeArkTextureRecords(payload, block) {
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const start = block.rttiStart, end = block.rttiStart + block.span;
  const out = [];
  const printable = (b) => b >= 0x20 && b < 0x7f;
  const isMarker = (p) => p + 4 <= end &&
    payload[p] === 0xff && payload[p + 1] === 0xff && payload[p + 2] === 0xff && payload[p + 3] === 0xff;
  // skip the RTTI type string itself
  const rttiLen = dv.getInt32(start, true);
  if (rttiLen < 1 || rttiLen > 256) return out;
  // pass 1: anchor name positions (sized string + FFFFFFFF within 16 B after)
  const names = [];
  let c = start + 4 + rttiLen;
  while (c + 8 < end) {
    const len = dv.getInt32(c, true);
    if (len >= 4 && len <= 256 && c + 4 + len < end) {
      let ok = true;
      for (let i = 0; i < len; i++) if (!printable(payload[c + 4 + i])) { ok = false; break; }
      if (ok) {
        const nameEnd = c + 4 + len;
        let nearMarker = false;
        for (let m = nameEnd; m < nameEnd + 16 && m + 4 <= end; m++) if (isMarker(m)) { nearMarker = true; break; }
        if (nearMarker) {
          let name = '';
          for (let i = 0; i < len; i++) name += String.fromCharCode(payload[c + 4 + i]);
          names.push({ namePos: c, nameEnd });
          c = nameEnd + 4; // past the near marker
          continue;
        }
      }
    }
    c++;
  }
  // pass 2: per record region, id = u32 after the LAST FFFFFFFF marker
  for (let i = 0; i < names.length; i++) {
    const regionStart = names[i].nameEnd;
    const regionEnd = i + 1 < names.length ? names[i + 1].namePos : end;
    let id = null, lastMarker = -1;
    for (let m = regionStart; m + 8 <= regionEnd; m++) {
      if (isMarker(m) && m + 8 <= end) { lastMarker = m; }
    }
    if (lastMarker >= 0) id = dv.getUint32(lastMarker + 4, true);
    let name = '';
    const len = dv.getInt32(names[i].namePos, true);
    for (let k = 0; k < len; k++) name += String.fromCharCode(payload[names[i].namePos + 4 + k]);
    out.push({ name, textureId: id, region: [regionStart - start, regionEnd - start] });
  }
  return out;
}

/** AV-5: 4.0.x NiArkTextureExtraData record decode (layout from the AV-4
 * adapter notes — NiExtraData v4 base = single next link, then header ints,
 * then per-texture: [name SizedString][slotType i32][unk i32][texPropRef
 * i32][9B: 00 | FFFFFFFF | u32 LE id]). Validated by strict checks; any
 * layout mismatch returns [] (the generic anchored decoder is the fallback
 * for 4.1-shaped blocks). */
function decodeArkTextureRecordsV40(payload, block) {
  const out = [];
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const start = block.rttiStart;
  const rttiLen = dv.getInt32(start, true);
  if (rttiLen < 1 || rttiLen > 256) return out;
  let p = start + 4 + rttiLen;
  const end = start + block.span;
  const i32 = () => { if (p + 4 > end) throw new Error('v40 rec overrun'); const v = dv.getInt32(p, true); p += 4; return v; };
  const u8 = () => { if (p + 1 > end) throw new Error('v40 rec overrun'); return payload[p++]; };
  try {
    const nextExtraData = i32();
    const unk1a = i32(), unk1b = i32();
    const unkByte = u8();
    const unk2 = i32();
    const numTextures = i32();
    if (numTextures < 0 || numTextures > 64) return out;
    for (let i = 0; i < numTextures; i++) {
      const nameLen = i32();
      if (nameLen < 1 || nameLen > 256 || p + nameLen > end) return out.length ? out : [];
      let name = '';
      for (let k = 0; k < nameLen; k++) {
        const b = payload[p + k];
        if (b < 0x20 || b >= 0x7f) return out.length ? out : [];
        name += String.fromCharCode(b);
      }
      p += nameLen;
      const slotType = i32(), unk4 = i32(), texPropRef = i32();
      const idBytes = payload.subarray(p, p + 9); p += 9;
      if (p > end) return out;
      if (idBytes[1] === 0xff && idBytes[2] === 0xff && idBytes[3] === 0xff && idBytes[4] === 0xff) {
        const textureId = (idBytes[5] | (idBytes[6] << 8) | (idBytes[7] << 16) | (idBytes[8] << 24)) >>> 0;
        out.push({ name, textureId, slotType });
      }
    }
    return out;
  } catch { return out; }
}

async function handleAssetsApi(urlPath, req, res) {
  if (!urlPath.startsWith('/api/assets/')) return false;
  const send = (code, obj) => {
    const body = JSON.stringify(obj);
    res.writeHead(code, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
    res.end(body);
  };
  try {
    if (urlPath === '/api/assets/index') {
      const ark = await getModelsArk();
      const entries = modelsArkEntries.map(e => {
        const m = e.name.match(/^(\d+)\.([^.]+)$/i);
        return { id: m ? Number(m[1]) : null, name: e.name, size: e.size, ext: m ? m[2] : null };
      });
      send(200, {
        era: AV_ERA, status: 'OK',
        source: {
          container: 'Models.ark', path: MODELS_ARK_PATH,
          pinnedBytes: MODELS_ARK_PIN_BYTES, verifiedBytes: statSync(MODELS_ARK_PATH).size,
          eocdTotalEntries: ark.eocdTotalEntries,
        },
        count: entries.length, entries,
      });
      return true;
    }
    const q = new URL(req.url, 'http://127.0.0.1').searchParams;
    if (urlPath === '/api/assets/model') {
      const id = Number(q.get('id'));
      if (!Number.isInteger(id) || id < 0) { send(400, { status: 'BAD_REQUEST', reason: 'id must be an integer' }); return true; }
      const ark = await getModelsArk();
      const entry = ark.entryById(id);
      if (!entry) { send(404, { status: 'NOT_FOUND', reason: `Models.ark has no entry ${id}.nif`, era: AV_ERA }); return true; }
      const { payload } = ark.readEntry(entry);
      const sha = sha256Hex(payload);
      // minimal header sniff (inspector.js parity): version u32 after first \n
      const nl = payload.indexOf(0x0a);
      if (nl < 0) { send(200, { status: 'UNSUPPORTED', era: AV_ERA, id, name: entry.name, sha256: sha, reason: 'no newline in NIF header — not a NIF payload' }); return true; }
      const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
      const versionRaw = dv.getUint32(nl + 1, true);
      // AV-5 version-dispatch: 4.1.0.12 -> parseModel41 (W09, unchanged);
      // 4.0.0.0 / 4.0.0.2 -> parseModel40 (AV-4 dedicated adapter). Anything
      // else stays a LOUD UNSUPPORTED_VERSION (no guessing).
      let parseFn = null, versionLabel = null;
      if (versionRaw === NIF_V4_1_0_12) { parseFn = parseModel41; versionLabel = '4.1.0.12'; }
      else if (versionRaw === NIF_V4_0_0_0 || versionRaw === NIF_V4_0_0_2) { parseFn = parseModel40; versionLabel = versionRaw === NIF_V4_0_0_0 ? '4.0.0.0' : '4.0.0.2'; }
      if (!parseFn) {
        send(200, {
          status: 'UNSUPPORTED', era: AV_ERA, id, name: entry.name, sha256: sha,
          reason: `NIF version 0x${versionRaw.toString(16)} — this viewer implements NIF 4.1.0.12 (0x0401000c), 4.0.0.0 (0x04000000) and 4.0.0.2 (0x04000002); no other version, no guessing`,
        });
        return true;
      }
      const { extraction, renderModel } = parseFn(payload, entry.name);
      // texture joins (era canon): NiTexturingProperty slots carry source=-1
      // in this corpus; the REAL binding is NiArkTextureExtraData records
      // [name '<shape>_<uvSet>_<BASE|DETAIL>' + FFFFFFFF + u32 LE id]
      const texArk = await getTexturesArk();
      // collect all NiArkTextureExtraData records (may live anywhere)
      const arkRecords = [];
      const is40 = (versionRaw === NIF_V4_0_0_0 || versionRaw === NIF_V4_0_0_2);
      for (const blk of extraction.blocks) {
        if (blk.type === 'NiArkTextureExtraData' && !blk.fields) {
          // 4.0.x uses the AV-4 measured record layout (id in the 9-byte
          // tail per record); 4.1 keeps the anchored generic decoder.
          const recs = is40 ? decodeArkTextureRecordsV40(payload, blk) : decodeArkTextureRecords(payload, blk);
          if (is40 && !recs.length) {
            for (const r of decodeArkTextureRecords(payload, blk)) arkRecords.push(r);
          }
          for (const r of recs) arkRecords.push(r);
        }
      }
      const SLOT_ROLE = { 0: 'BASE', 2: 'DETAIL' };
      const textureJoins = [];
      for (const sh of renderModel.shapes) {
        const joins = [];
        if (!sh.textureProp) {
          joins.push({ slot: 0, sourceRef: null, sourceType: 'NO_TEXTURE_PROPERTY', resolved: false, reason: 'shape has no NiTexturingProperty — untextured (honest status)' });
        } else {
          const baseName = sh.shapeName.split(':')[0];
          // AV-5: 4.0.x exporters replace spaces with underscores in the
          // NiArkTextureExtraData record names (observed 2026-10-31 on
          // 103278: shape 'Editable Mesh' -> record 'Editable_Mesh_BASE')
          // — the lookup tries BOTH spellings, nothing else.
          const baseVariants = [baseName, baseName.replace(/ /g, '_')];
          const findRec = (suffix) => {
            for (const b of baseVariants) {
              const r = arkRecords.find(x => x.name === b + suffix) ??
                arkRecords.find(x => x.name.startsWith(b + '_') && x.name.endsWith(suffix));
              if (r) return r;
            }
            return null;
          };
          const recBASE = findRec('_BASE');
          const recDETAIL = findRec('_DETAIL');
          sh.textureProp.textures.forEach((slot, slotIdx) => {
            if (!slot || slot.has !== 1) return;
            const role = SLOT_ROLE[slotIdx] ?? null;
            const rec = role === 'BASE' ? recBASE : role === 'DETAIL' ? recDETAIL : null;
            const join = { slot: slotIdx, sourceRef: slot.source, sourceType: 'NiArkTextureExtraData (canon)', uvSet: slot.uv_set, role };
            if (rec) {
              join.arkRecordName = rec.name;
              join.textureId = rec.textureId;
              const tentry = texArk.entryById(rec.textureId);
              join.resolved = !!tentry;
              join.arkEntry = tentry ? { name: tentry.name, size: tentry.size } : null;
              if (!tentry) join.reason = `NiArkTextureExtraData id ${rec.textureId} NOT in Textures.ark`;
            } else {
              join.resolved = false;
              join.reason = arkRecords.length
                ? `no NiArkTextureExtraData record for '${baseName}_${role ?? '?'}' (records: ${arkRecords.slice(0, 3).map(r => r.name).join(', ')}${arkRecords.length > 3 ? '…' : ''})`
                : 'no NiArkTextureExtraData block in this model';
            }
            joins.push(join);
          });
          if (!joins.length) {
            joins.push({ slot: 0, sourceRef: null, sourceType: 'NO_ACTIVE_SLOT', resolved: false, reason: 'NiTexturingProperty present but no slot has texture=1 — untextured' });
          }
        }
        textureJoins.push({ shapeIndex: sh.shapeIndex, shapeName: sh.shapeName, joins });
      }
      // AV-5: skin decode (4.1 only — the measured layout is 4.1-era; 4.0
      // skin blocks stay OPAQUE-UNSUPPORTED, loud in the census).
      let skin = null;
      if (versionRaw === NIF_V4_1_0_12) {
        skin = decodeSkinBlocks41(payload, extraction);
      }
      // per-shape skin binding (bones + inverse-bind matrices + merged
      // per-vertex influences; NO truncation — max influences reported)
      const skinBindings = [];
      for (let si = 0; si < renderModel.shapes.length; si++) {
        const sh = renderModel.shapes[si];
        if (sh.skinRef == null || sh.skinRef < 0 || !skin) { skinBindings.push(null); continue; }
        skinBindings.push(buildSkinBinding(skin, sh));
      }
      // census (type -> count/opaque) WITHOUT raw hex payloads
      const census = {};
      for (const b of extraction.blocks) {
        if (!census[b.type]) census[b.type] = { count: 0, opaque: 0 };
        census[b.type].count++;
        if (b.opaque) census[b.type].opaque++;
      }
      // shapes: typed arrays -> plain arrays for JSON
      const shapes = renderModel.shapes.map((sh, si) => ({
        ...sh,
        positions: Array.from(sh.positions),
        normals: sh.normals ? Array.from(sh.normals) : null,
        colors: sh.colors ? Array.from(sh.colors) : null,
        uvSets: sh.uvSets.map(a => Array.from(a)),
        index: Array.from(sh.index),
        skin: skinBindings[si] ?? null,
      }));
      // AV-3 additive: decode the keyframe animation blocks (closure-exact,
      // per-block failures recorded loudly — never silent) + NiNode hierarchy
      // with NUMERIC local TRS (the client builds the Object3D/Bone tree;
      // skinned shapes bind to it — AV-5).
      const kfAnim = decodeKeyframeBlocks41(payload, extraction);
      const bitsToF32 = (hex) => {
        const u = new Uint32Array(1); const b = new Uint8Array(u.buffer);
        for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
        return new Float32Array(u.buffer)[0];
      };
      const childOfNode = new Map();
      for (const b of extraction.blocks) {
        if (b.type === 'NiNode' && b.fields) {
          for (const c of b.fields.children || []) if (c >= 0) childOfNode.set(c, b.index);
        }
      }
      const nodeHierarchy = extraction.blocks
        .filter(b => (b.type === 'NiNode' || b.type === 'NiTriShape') && b.fields)
        .map(b => ({
          index: b.index, type: b.type, name: b.fields.name,
          parent: childOfNode.has(b.index) ? childOfNode.get(b.index) : null,
          children: b.type === 'NiNode' ? b.fields.children : [],
          controller: b.fields.controller ?? null,
          localTRS: {
            translation: b.fields.translation.map(bitsToF32),
            rotation: b.fields.rotation.map(r => r.map(bitsToF32)),
            scale: bitsToF32(b.fields.scale),
          },
        }));
      send(200, {
        status: 'OK', era: AV_ERA, id, name: entry.name, size: entry.size, sha256: sha,
        header: extraction.header,
        nifVersion: versionLabel,
        adapter: versionRaw === NIF_V4_1_0_12 ? 'NifModelReader41' : 'NifModelReader40',
        parseStatus: extraction.parseStatus ?? 'PASS',
        stoppedAtBlock: extraction.stoppedAtBlock ?? null,
        tailBytes: extraction.fileTailBytesLen,
        blockCensus: census,
        opaqueCount: extraction.opaqueBlocks.length,
        shapes, controllers: renderModel.controllers, roots: renderModel.roots,
        counts: renderModel.counts, textureJoins,
        nodeHierarchy,
        keyframeAnim: {
          controllers: kfAnim.controllers,
          data: kfAnim.data,
          textKeys: kfAnim.textKeys,
          failures: kfAnim.failures,
          closureAll: kfAnim.closureAll,
          // LOOP policy label (AV-3 contract): clip looping is an ENGINEERING
          // choice of the viewer, NOT a measured NIF semantic.
          loopPolicy: 'ENGINEERING_LABEL',
        },
        // AV-5: skin payload (4.1 only). Bind law: p = SUM w_i *
        // (W_bone_i * SkinToBone_i) * v — physically verified on the corpus
        // (tools/av5/skin_verify.mjs: bind invariant M_i = W_i*STB_i is
        // constant per shape, spread < 1e-2 on the passing shapes).
        skin: skin ? {
          instances: skin.instances.map(i => ({ blockIndex: i.blockIndex, dataRef: i.dataRef, rootNodeRef: i.rootNodeRef, numBones: i.numBones })),
          data: skin.data.map(d => ({ blockIndex: d.blockIndex, numBones: d.numBones, tailLen: d.tailLen ?? null })),
          partitionBlockCount: skin.partitions.length,
          failures: skin.failures,
          closureAll: skin.closureAll,
        } : null,
      });
      return true;
    }
    if (urlPath === '/api/assets/texture') {
      const id = Number(q.get('id'));
      if (!Number.isInteger(id) || id < 0) { send(400, { status: 'BAD_REQUEST', reason: 'id must be an integer' }); return true; }
      const ark = await getTexturesArk();
      const entry = ark.entryById(id);
      if (!entry) { send(404, { status: 'NOT_FOUND', reason: `Textures.ark has no numeric entry ${id}`, era: AV_ERA }); return true; }
      const { payload } = ark.readEntry(entry);
      res.writeHead(200, {
        'Content-Type': 'application/octet-stream', 'Cache-Control': 'no-store',
        'Content-Length': payload.length, 'X-Ark-Entry': entry.name,
      });
      res.end(payload);
      return true;
    }
    send(404, { status: 'NOT_FOUND', reason: `unknown /api/assets/ route ${urlPath} (allowlist: index, model, texture)` });
    return true;
  } catch (e) {
    send(500, { status: 'ERROR', reason: String(e.message ?? e), era: AV_ERA });
    return true;
  }
}

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const BASE_PORT = Number(process.env.PORT) || 8140;
const FALLBACK_PORT = 8141;

// W03 exact-file routes: URL -> absolute original path (READ-ONLY allowlist).
// Sanitized (PATH_INCIDENT root cause fix): no hardcoded private absolute
// paths. Routes are supplied via env SERVER_EXACT_ROUTES as a JSON object
// mapping URL path -> absolute file path (read-only, exact-file semantics,
// no directory traversal). Empty default when the env var is not set.
const EXACT_ROUTES = (() => {
  try {
    return JSON.parse(process.env.SERVER_EXACT_ROUTES || '{}');
  } catch (e) {
    console.error('SERVER_EXACT_ROUTES parse failed (using empty map):', e.message);
    return {};
  }
})();
// Server lease (pid/exe/start/port/stop) — env override, default local file.
// Sanitized: no hardcoded private absolute path (PATH_INCIDENT root cause).
const LEASE_PATH = process.env.SERVER_LEASE_PATH || process.env.LEASE_PATH ||
  './server_lease.json';

// Explicit, era-labeled, read-only aliases into the original corpora.
// Sanitized: supplied via env SERVER_ALIASES as a JSON object mapping
// URL prefix -> absolute directory path. Empty default when not set.
const ALIASES = (() => {
  try {
    return JSON.parse(process.env.SERVER_ALIASES || '{}');
  } catch (e) {
    console.error('SERVER_ALIASES parse failed (using empty map):', e.message);
    return {};
  }
})();

const MIME = {
  '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.html': 'text/html', '.json': 'application/json',
  '.css': 'text/css', '.txt': 'text/plain',
  '.bnt': 'application/octet-stream', '.dat': 'application/octet-stream',
  '.tdf': 'application/octet-stream', '.tga': 'application/octet-stream',
};

const server = http.createServer(async (req, res) => {
  try {
    let urlPath = decodeURIComponent(req.url.split('?')[0]);
    if (urlPath.endsWith('/')) urlPath += 'index.html';
    // W03 exact-file allowlist FIRST (no prefix semantics, no traversal).
    if (Object.prototype.hasOwnProperty.call(EXACT_ROUTES, urlPath)) {
      const data = await fs.readFile(EXACT_ROUTES[urlPath]);
      res.writeHead(200, {
        'Content-Type': 'application/octet-stream',
        'Cache-Control': 'no-store',
        'Content-Length': data.length,
      });
      res.end(data);
      return;
    }
    // AV-2 bounded asset API FIRST (allowlist — see handleAssetsApi)
    if (await handleAssetsApi(urlPath, req, res)) return;
    let fsPath = null;
    for (const [alias, target] of Object.entries(ALIASES)) {
      if (urlPath.startsWith(alias)) {
        fsPath = target + urlPath.slice(alias.length);
        break;
      }
    }
    if (!fsPath) {
      // serve from repo root; block path traversal
      const rel = path.normalize(urlPath).replace(/^([/\\]+)*/, '');
      const abs = path.join(ROOT, rel);
      if (!abs.startsWith(ROOT)) { res.writeHead(403); res.end('forbidden'); return; }
      fsPath = abs;
    }
    const data = await fs.readFile(fsPath);
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(fsPath).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-store',
      'Content-Length': data.length,
    });
    res.end(data);
  } catch (err) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end(`not found: ${req.url}`);
  }
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE' && server.portAttempts === 0) {
    server.portAttempts = 1;
    server.listen(FALLBACK_PORT, '127.0.0.1');
  } else {
    console.error('server error:', err.message);
    process.exit(1);
  }
});

function writeLease(port) {
  const lease = {
    job: 'AV2_VIEWER (PE_ISO_ASSET_VIEWER_R1, era ISO_5_1_0_0)',
    pid: process.pid,
    exe: process.execPath,
    startedUtc: new Date().toISOString(),
    port,
    bind: '127.0.0.1',
    command: 'node server.mjs',
    stop: `Stop-Process -Id ${process.pid}`,
    route: EXACT_ROUTES,
  };
  try {
    mkdirSync(path.dirname(LEASE_PATH), { recursive: true });
    writeFileSync(LEASE_PATH, JSON.stringify(lease, null, 2) + '\n');
    console.log(`lease written: ${LEASE_PATH}`);
  } catch (e) {
    console.error('lease write FAILED (non-fatal):', e.message);
  }
}

server.portAttempts = 0;
server.listen(BASE_PORT, '127.0.0.1', () => {
  const addr = server.address();
  writeLease(addr.port);
  console.log(`eudoria-clean server http://127.0.0.1:${addr.port}/ pid=${process.pid}`);
});
