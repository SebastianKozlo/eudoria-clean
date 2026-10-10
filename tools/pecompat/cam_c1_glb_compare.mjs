#!/usr/bin/env node
// cam_c1_glb_compare.mjs — PE_WORLD_LAUNCHER_R1_20261010, Etap A, CAM-C1
// (contract §2a; Desktop post-audit CITY_ASSET_MAP_F71_POST_AUDIT §3 CAM-C1/P2).
//
// RETRACTION REPRODUCED HERE AS CODE: the standing claim
// NO_GLB_PRESENT_FOR_THESE_IDS (f71eb30 package: DEEP_ANALYSIS.md §5,
// REPORT.md, LIMITATIONS.md — historical, read-only) is FALSE. The four GLB
// comparison inputs physically exist under
// D:\Eudoria_Reconstruction\12_WebGame\tools\pe_asset_viewer_v4\assets\
// converted\static\<id>_complete_textured.glb (READ_ONLY comparison inputs;
// size+SHA256 pins re-verified by this tool at every run — fail-closed).
//
// WHAT THIS TOOL DOES (method, registered in PREREGISTRATION.md §1):
//   1. Re-decodes the four CD_2003 primaries from the pinned READ_ONLY
//      Models.ark payloads with the EXISTING production phase-3 reader
//      (tools/pecompat/nif41_deep.mjs readNif41/analyzeNif41Model — the same
//      reader the catalog server uses), after fail-closed container + payload
//      pin verification. (The alternative — reusing the prior run's stored
//      decoded arrays — was not taken: a fresh decode keeps this package
//      independent of historical private artifacts.)
//   2. Parses the GLB binary (glTF 2.0 container: JSON chunk + BIN chunk;
//      no Draco — extension checked and refused loudly if present) and extracts
//      each mesh primitive's POSITION (float32 VEC3) and indices (uint16/uint32).
//   3. Applies the EXPLICIT conversion (x,y,z) -> (x,z,-y) to the ORIGINAL
//      NIF vertex positions — ONCE, no scaling, no further axis arithmetic —
//      then compares:
//        - the multiset of vertex positions (bit-exact float32 keys);
//        - the multiset of UNORIENTED geometric triangles (each triangle =
//          its 3 position keys, sorted — winding/orientation DELIBERATELY
//          ignored).
//   4. Records per model: counts, per-geometry tables, bounds, GLB images
//      census, TEXCOORD presence, UV sets of the ORIGINAL NIF, local-TRS
//      identity check.
//
// COMPARISON UNIT: original file units, float32. TOLERANCE: bit-exact equality
// is EXPECTED for a pure axis shuffle (no arithmetic); any mismatch is
// reported with its measured count and max abs delta — never massaged.
//
// EXPLICIT LIMITS (must accompany any use of these results):
//   - Unoriented triangle agreement does NOT confirm winding, materials, or
//     the converter execution lineage (which script produced the GLBs is NOT
//     established by agreement).
//   - The `_textured.glb` FILENAME is NOT proof of textures: the ORIGINAL
//     NIFs have 0 UV sets and 0 texture bindings; the four models remain
//     UNTEXTURED_PROXY; NO random textures may be attached. The GLBs' own
//     TEXCOORD_0/NORMAL attributes are exporter-side artifacts, not evidence
//     of original-texture binding. The GLB `images` census is expected 0.
//
// Usage: node tools/pecompat/cam_c1_glb_compare.mjs [--json-out <path>]
// Output: JSON report on stdout (+ optional file).

'use strict';
import crypto from 'node:crypto';
import { promises as fsp } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { readNif41, analyzeNif41Model } from './nif41_deep.mjs';
import { CATALOG_PINS, PRIMARY_IDS, PRIMARY_PINS } from './catalog_data.mjs';

const GLB_DIR = 'D:\\Eudoria_Reconstruction\\12_WebGame\\tools\\pe_asset_viewer_v4\\assets\\converted\\static';
const GLB_PINS = Object.freeze({
  '192374': { sizeBytes: 94484, sha256: '8af713e0af150b3edab69affbb0121c55685f883054a0db692c4838d0982e3ea' },
  '193207': { sizeBytes: 66476, sha256: '4f8c7c5ba652fbcca6c01a02f4ac76a3cdc56eed5314aa1044f4fcf870c19b85' },
  '193313': { sizeBytes: 94644, sha256: 'da1a15bf8d7a04be006b5804b12dff2c282123562cd00189561b0d160e6c1243' },
  '193684': { sizeBytes: 108192, sha256: '6b96c12763c80bc693361924e1eaa1bab16b5bd2daba7908e3fcb86c62ec2efc' },
});

const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');

// ---- float32 key helpers (bit-exact multiset comparison) ----
const hex8 = (u32) => u32.toString(16).padStart(8, '0');

/** Position key: the three little-endian float32 bit patterns, '|'-joined. */
function posKeyFromBits(bx, by, bz) { return `${hex8(bx)}|${hex8(by)}|${hex8(bz)}`; }

/** Read the i-th position key of a Float32Array-backed position buffer. */
function nifPosKey(f32, i) {
  const dv = new DataView(f32.buffer, f32.byteOffset, f32.byteLength);
  return posKeyFromBits(dv.getUint32(i * 12, true), dv.getUint32(i * 12 + 4, true), dv.getUint32(i * 12 + 8, true));
}

/** The EXPLICIT conversion (x,y,z) -> (x,z,-y): ONE application, on the
 *  ORIGINAL NIF position. Returns the converted position key (bit-exact) and
 *  the numeric converted triple. new_y = z (original), new_z = -y (original,
 *  negated in FLOAT space so -0.0/+0.0 behave exactly as the conversion
 *  arithmetic does). NOTE (recorded in the intervention ledger): the first
 *  execution of this tool transposed the target slots ((x, y, -z) — a
 *  variable-naming bug), produced a 4/4 MISMATCH, and was caught by the
 *  preregistered expectation of exact agreement; fixed to the contract
 *  conversion (x, z, -y) and re-run. */
function convertXyzToXzNegY(dv, i) {
  const x = dv.getFloat32(i * 12, true);
  const y = dv.getFloat32(i * 12 + 4, true);
  const z = dv.getFloat32(i * 12 + 8, true);
  const nx = x, ny = z, nz = -y; // (x, z, -y) — new_x=x, new_y=z, new_z=-y
  const nb = new DataView(new ArrayBuffer(12));
  nb.setFloat32(0, nx, true); nb.setFloat32(4, ny, true); nb.setFloat32(8, nz, true);
  return {
    key: posKeyFromBits(nb.getUint32(0, true), nb.getUint32(4, true), nb.getUint32(8, true)),
    value: [nx, ny, nz],
    original: [x, y, z],
  };
}

// ---- GLB (binary glTF 2.0) bounded reader ----
function readGlbGeometry(bytes, label) {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  if (bytes.length < 12 || dv.getUint32(0, true) !== 0x46546c67) throw new Error(`[${label}] not a GLB (magic mismatch)`);
  const version = dv.getUint32(4, true);
  const totalLen = dv.getUint32(8, true);
  if (version !== 2) throw new Error(`[${label}] GLB version ${version} != 2`);
  if (totalLen !== bytes.length) throw new Error(`[${label}] GLB total length ${totalLen} != file size ${bytes.length}`);
  let p = 12;
  let json = null, bin = null, binStart = -1;
  while (p + 8 <= bytes.length) {
    const chunkLen = dv.getUint32(p, true);
    const chunkType = dv.getUint32(p + 4, true);
    const start = p + 8;
    if (start + chunkLen > bytes.length) throw new Error(`[${label}] GLB chunk overruns the file`);
    const chunk = bytes.subarray(start, start + chunkLen);
    if (chunkType === 0x4e4f534a) json = JSON.parse(new TextDecoder().decode(chunk)); // 'JSON'
    else if (chunkType === 0x004e4942) { bin = chunk; binStart = start; } // 'BIN'
    p = start + chunkLen;
  }
  if (!json || !bin) throw new Error(`[${label}] GLB missing JSON or BIN chunk`);
  if (json.extensionsUsed?.includes('KHR_draco_mesh_compression')) {
    throw new Error(`[${label}] Draco-compressed GLB refused by this bounded comparison reader (no Draco decode is authorized here)`);
  }
  const images = Array.isArray(json.images) ? json.images.length : 0;
  const bufferViews = json.bufferViews ?? [];
  const accessors = json.accessors ?? [];
  // glTF bufferView.byteOffset is RELATIVE to the start of the BIN chunk;
  // accessor.byteOffset is relative to the bufferView start.
  const accBase = (ai) => {
    const acc = accessors[ai];
    const bv = bufferViews[acc.bufferView];
    return binStart + (bv?.byteOffset ?? 0) + (acc.byteOffset ?? 0);
  };
  const readAccessorF32Vec3 = (ai) => {
    const acc = accessors[ai];
    if (!acc || acc.componentType !== 5126 || acc.type !== 'VEC3') throw new Error(`[${label}] accessor ${ai} is not float32 VEC3`);
    const base = accBase(ai);
    const n = acc.count;
    const out = new Float32Array(n * 3);
    for (let i = 0; i < n * 3; i++) out[i] = dv.getFloat32(base + i * 4, true);
    return out;
  };
  const readAccessorIdx = (ai) => {
    const acc = accessors[ai];
    if (!acc) throw new Error(`[${label}] missing indices accessor ${ai}`);
    if (acc.componentType !== 5123 && acc.componentType !== 5125) {
      throw new Error(`[${label}] indices accessor ${ai} componentType ${acc.componentType} not u16/u32`);
    }
    const base = accBase(ai);
    const n = acc.count;
    const out = new Uint32Array(n);
    if (acc.componentType === 5123) { for (let i = 0; i < n; i++) out[i] = dv.getUint16(base + i * 2, true); }
    else { for (let i = 0; i < n; i++) out[i] = dv.getUint32(base + i * 4, true); }
    return out;
  };
  const primitives = [];
  for (const mesh of json.meshes ?? []) {
    for (const prim of mesh.primitives ?? []) {
      const posAi = prim.attributes?.POSITION;
      if (posAi == null) throw new Error(`[${label}] a primitive without POSITION`);
      const positions = readAccessorF32Vec3(posAi);
      let indices = null;
      if (prim.indices != null) indices = readAccessorIdx(prim.indices);
      primitives.push({
        positions,
        indices,
        hasTexcoord: prim.attributes?.TEXCOORD_0 != null,
        hasNormal: prim.attributes?.NORMAL != null,
        material: prim.material ?? null,
        numVertices: positions.length / 3,
        numTriangles: indices ? indices.length / 3 : positions.length / 3 / 3, // non-indexed TRIANGLES soup — measured, not assumed
      });
    }
  }
  return { json, images, generator: json.asset?.generator ?? null, primitives };
}

/** Multiset equality of two Map<key,count>; returns matched keys count + diffs. */
function multisetDiff(a, b) {
  let matchedKeys = 0, matchedCount = 0;
  const onlyInA = [], onlyInB = [];
  for (const [k, ca] of a) {
    const cb = b.get(k) ?? 0;
    if (cb === ca) { matchedKeys++; matchedCount += ca; }
    else if (cb === 0) onlyInA.push({ key: k, count: ca });
    else onlyInA.push({ key: k, countA: ca, countB: cb });
  }
  for (const [k, cb] of b) {
    if (!a.has(k)) onlyInB.push({ key: k, count: cb });
  }
  return { matchedKeys, matchedCount, onlyInA: onlyInA.slice(0, 4), onlyInB: onlyInB.slice(0, 4), onlyInACount: onlyInA.length, onlyInBCount: onlyInB.length };
}

function parseKeyNumeric(key) {
  const parts = key.split('|');
  const dv = new DataView(new ArrayBuffer(4));
  const out = [];
  for (const part of parts) {
    dv.setUint32(0, parseInt(part, 16), true);
    out.push(dv.getFloat32(0, true));
  }
  return out;
}

async function main() {
  const args = process.argv.slice(2);
  let jsonOut = null;
  for (let i = 0; i < args.length; i++) if (args[i] === '--json-out') jsonOut = args[++i];

  const t0 = Date.now();
  const report = {
    runId: 'PE_WORLD_LAUNCHER_R1_20261010',
    phase: 'ETAP_A_CAM_C1',
    retraction: 'NO_GLB_PRESENT_FOR_THESE_IDS is RETRACTED — the four GLB comparison inputs exist at the pinned paths and are verified below (fail-closed).',
    method: {
      originalSide: 'fresh decode of the four CD_2003 primaries from the pinned READ_ONLY Models.ark with the EXISTING production reader (tools/pecompat/nif41_deep.mjs readNif41/analyzeNif41Model; container + payload pins fail-closed at load)',
      glbSide: 'bounded glTF 2.0 binary parse (JSON+BIN chunks; Draco refused loudly; POSITION float32 VEC3 + u16/u32 indices per primitive)',
      conversion: 'EXPLICIT (x,y,z) -> (x,z,-y) applied ONCE to the ORIGINAL NIF vertex positions (no scaling, no further axis arithmetic; -y negated in float space)',
      comparisonUnit: 'multiset of float32 vertex positions (bit-exact keys) + multiset of UNORIENTED geometric triangles (3 position keys, sorted — winding/orientation deliberately ignored); ORIGINAL file units everywhere (never meters)',
      tolerance: 'bit-exact float32 equality expected for a pure axis shuffle; measured mismatch counts + max abs delta reported as measured (never massaged)',
    },
    explicitLimits: [
      'Unoriented triangle agreement does NOT confirm winding, materials, or the converter execution lineage (which script produced the GLBs is NOT established by agreement).',
      'The _textured.glb FILENAME is NOT proof of textures: the ORIGINAL NIFs have 0 UV sets and 0 texture bindings; the four models remain UNTEXTURED_PROXY; NO random textures may be attached.',
      'GLB-side TEXCOORD_0/NORMAL attributes are exporter-side artifacts, not evidence of original-texture binding.',
    ],
    models: [],
    elapsedMs: null,
  };

  // ---- pinned container (READ_ONLY) ----
  const arkBytes = new Uint8Array(await fsp.readFile(CATALOG_PINS.modelsArk.path));
  const arkSha = sha256(arkBytes);
  if (arkBytes.length !== CATALOG_PINS.modelsArk.sizeBytes || arkSha !== CATALOG_PINS.modelsArk.sha256) {
    throw new Error(`CAM-C1: Models.ark identity mismatch (size ${arkBytes.length}, sha ${arkSha}) — BLOCKED`);
  }
  const ark = new ArkArchive(arkBytes);
  const entries = ark.entries();
  const byName = new Map(entries.map((e) => [e.name, e]));

  for (const id of PRIMARY_IDS) {
    const entry = byName.get(`${id}.nif`);
    if (!entry) throw new Error(`CAM-C1: ${id}.nif not found in the pinned Models.ark — BLOCKED`);
    const { payload } = ark.readEntry(entry);
    const pin = PRIMARY_PINS[id];
    const psha = sha256(payload);
    if (payload.length !== pin.sizeBytes || psha !== pin.sha256) {
      throw new Error(`CAM-C1: primary ${id} payload pin mismatch (size ${payload.length}/${pin.sizeBytes}, sha ${psha}) — BLOCKED`);
    }
    const r = readNif41(payload, { sourceName: `${id}.nif` });
    const analysis = analyzeNif41Model(r, {
      assetId: Number(id), era: 'CD_2003', build: 'CAM_C1_REDECODE',
      container: CATALOG_PINS.modelsArk.container, entryName: `${id}.nif`,
      payloadSha256: psha, sizeBytes: payload.length, adapterVersion: 'cam-c1-compare-v1',
      physicalSource: `Models.ark entry ${pin.entryIndex} (READ_ONLY original)`,
    });

    // ---- GLB side (READ_ONLY comparison input; pin fail-closed) ----
    const glbPath = `${GLB_DIR}\\${id}_complete_textured.glb`;
    const glbBytes = new Uint8Array(await fsp.readFile(glbPath));
    const glbSha = sha256(glbBytes);
    const glbPinOk = glbBytes.length === GLB_PINS[id].sizeBytes && glbSha === GLB_PINS[id].sha256;
    if (!glbPinOk) throw new Error(`CAM-C1: GLB ${id} pin mismatch (size ${glbBytes.length}, sha ${glbSha}) — BLOCKED`);
    const glb = readGlbGeometry(glbBytes, `GLB ${id}`);

    // ---- NIF geometry (per block with real geometry) ----
    const nifGeoms = [];
    for (const b of r.blocks) {
      const g = b.geometry;
      if (!g || !g.positions) continue;
      nifGeoms.push({ block: b.index, type: b.type, name: b.name, numVertices: g.numVertices, numTriangles: g.numTriangles, uvSets: (g.uvSets ?? []).length, hasNormals: !!g.normals });
    }
    // local TRS identity check (measured, not assumed)
    let trsTotal = 0, trsIdentity = 0;
    for (const b of r.blocks) {
      if (!b.localTrs) continue;
      trsTotal++;
      const t = b.localTrs.translate, R = b.localTrs.rotate;
      const isIdent = t[0] === 0 && t[1] === 0 && t[2] === 0 && b.localTrs.scale === 1 &&
        R[0][0] === 1 && R[1][1] === 1 && R[2][2] === 1 &&
        R[0][1] === 0 && R[0][2] === 0 && R[1][0] === 0 && R[1][2] === 0 &&
        R[2][0] === 0 && R[2][1] === 0;
      if (isIdent) trsIdentity++;
    }

    // ---- build the converted NIF multisets ----
    const nifPosMultiset = new Map();
    const nifTriMultiset = new Map();
    let nifVertexTotal = 0, nifTriangleTotal = 0;
    const nifBounds = { min: [Infinity, Infinity, Infinity], max: [-Infinity, -Infinity, -Infinity] };
    const geoKeys = []; // per-geometry converted position keys, for the per-geometry table
    for (const b of r.blocks) {
      const g = b.geometry;
      if (!g || !g.positions) continue;
      const dv = new DataView(g.positions.buffer, g.positions.byteOffset, g.positions.byteLength);
      const keys = new Array(g.numVertices);
      for (let i = 0; i < g.numVertices; i++) {
        const conv = convertXyzToXzNegY(dv, i);
        keys[i] = conv.key;
        nifPosMultiset.set(conv.key, (nifPosMultiset.get(conv.key) ?? 0) + 1);
        for (let k = 0; k < 3; k++) {
          const v = conv.value[k];
          if (v < nifBounds.min[k]) nifBounds.min[k] = v;
          if (v > nifBounds.max[k]) nifBounds.max[k] = v;
        }
      }
      geoKeys.push({ block: b.index, keys });
      nifVertexTotal += g.numVertices;
      if (g.indices) {
        for (let t = 0; t < g.indices.length; t += 3) {
          const tri = [keys[g.indices[t]], keys[g.indices[t + 1]], keys[g.indices[t + 2]]].sort();
          const k = tri.join('~');
          nifTriMultiset.set(k, (nifTriMultiset.get(k) ?? 0) + 1);
          nifTriangleTotal++;
        }
      }
    }

    // ---- build the GLB multisets ----
    const glbPosMultiset = new Map();
    const glbTriMultiset = new Map();
    let glbVertexTotal = 0, glbTriangleTotal = 0;
    const glbBounds = { min: [Infinity, Infinity, Infinity], max: [-Infinity, -Infinity, -Infinity] };
    for (const prim of glb.primitives) {
      const dv = new DataView(prim.positions.buffer, prim.positions.byteOffset, prim.positions.byteLength);
      const n = prim.positions.length / 3;
      const keys = new Array(n);
      for (let i = 0; i < n; i++) {
        const key = posKeyFromBits(dv.getUint32(i * 12, true), dv.getUint32(i * 12 + 4, true), dv.getUint32(i * 12 + 8, true));
        keys[i] = key;
        glbPosMultiset.set(key, (glbPosMultiset.get(key) ?? 0) + 1);
        for (let k = 0; k < 3; k++) {
          const v = dv.getFloat32(i * 12 + k * 4, true);
          if (v < glbBounds.min[k]) glbBounds.min[k] = v;
          if (v > glbBounds.max[k]) glbBounds.max[k] = v;
        }
      }
      glbVertexTotal += n;
      if (prim.indices) {
        for (let t = 0; t < prim.indices.length; t += 3) {
          const tri = [keys[prim.indices[t]], keys[prim.indices[t + 1]], keys[prim.indices[t + 2]]].sort();
          const k = tri.join('~');
          glbTriMultiset.set(k, (glbTriMultiset.get(k) ?? 0) + 1);
          glbTriangleTotal++;
        }
      } else {
        for (let t = 0; t + 2 < n; t += 3) {
          const tri = [keys[t], keys[t + 1], keys[t + 2]].sort();
          const k = tri.join('~');
          glbTriMultiset.set(k, (glbTriMultiset.get(k) ?? 0) + 1);
          glbTriangleTotal++;
        }
      }
    }

    // ---- compare ----
    const posDiff = multisetDiff(nifPosMultiset, glbPosMultiset);
    const triDiff = multisetDiff(nifTriMultiset, glbTriMultiset);
    const positionsExact = posDiff.onlyInACount === 0 && posDiff.onlyInBCount === 0;
    const trianglesExact = triDiff.onlyInACount === 0 && triDiff.onlyInBCount === 0;
    // max abs delta over the unmatched GLB keys vs the converted NIF bounds — measured diagnostic
    let maxDelta = null;
    if (!positionsExact) {
      let m = 0;
      for (const d of [...posDiff.onlyInA, ...posDiff.onlyInB]) {
        const v = parseKeyNumeric(d.key);
        for (let k = 0; k < 3; k++) {
          const cands = [Math.abs(v[k] - nifBounds.min[k]), Math.abs(v[k] - nifBounds.max[k])];
          m = Math.max(m, ...cands);
        }
      }
      maxDelta = m;
    }

    report.models.push({
      id,
      nif: {
        payloadPin: { sizeBytes: payload.length, sha256: psha, contractPin: 'MATCH' },
        geometries: nifGeoms.length,
        vertices: nifVertexTotal,
        triangles: nifTriangleTotal,
        complexityFromAnalyze: analysis.complexity,
        trsIdentity: `${trsIdentity}/${trsTotal} local TRS identity`,
        uvSetsTotal: nifGeoms.reduce((n, g) => n + g.uvSets, 0),
        perGeometry: nifGeoms,
      },
      glb: {
        path: glbPath,
        pin: { sizeBytes: glbBytes.length, sha256: glbSha, contractPin: glbPinOk ? 'MATCH' : 'MISMATCH' },
        generator: glb.generator,
        primitives: glb.primitives.length,
        vertices: glbVertexTotal,
        triangles: glbTriangleTotal,
        images: glb.images,
        allPrimitivesHaveTexcoord: glb.primitives.every((p) => p.hasTexcoord),
        allPrimitivesHaveNormal: glb.primitives.every((p) => p.hasNormal),
        perPrimitive: glb.primitives.map((p, i) => ({ primitive: i, numVertices: p.numVertices, numTriangles: p.numTriangles, hasTexcoord: p.hasTexcoord, material: p.material })),
      },
      comparison: {
        conversion: '(x,y,z) -> (x,z,-y) applied ONCE to the original NIF positions',
        positionsMultisetExact: positionsExact,
        trianglesUnorientedMultisetExact: trianglesExact,
        vertexCountAgreement: nifVertexTotal === glbVertexTotal,
        triangleCountAgreement: nifTriangleTotal === glbTriangleTotal,
        positionMismatch: { keysOnlyInNif: posDiff.onlyInACount, keysOnlyInGlb: posDiff.onlyInBCount, sampleOnlyInNif: posDiff.onlyInA, sampleOnlyInGlb: posDiff.onlyInB, maxAbsDeltaDiagnostic: maxDelta },
        triangleMismatch: { keysOnlyInNif: triDiff.onlyInACount, keysOnlyInGlb: triDiff.onlyInBCount, sample: triDiff.onlyInA.slice(0, 2) },
        convertedNifBounds: Number.isFinite(nifBounds.min[0]) ? { min: nifBounds.min, max: nifBounds.max } : null,
        glbPositionBounds: Number.isFinite(glbBounds.min[0]) ? { min: glbBounds.min, max: glbBounds.max } : null,
      },
      verdict: positionsExact && trianglesExact
        ? 'EXACT_AGREEMENT (multiset positions + unoriented triangles, after the explicit (x,z,-y) conversion)'
        : 'MISMATCH (see comparison.positionMismatch / triangleMismatch — reported as measured, never massaged)',
    });
  }

  report.summary = {
    models: report.models.length,
    positionsExact: report.models.filter((m) => m.comparison.positionsMultisetExact).length,
    trianglesUnorientedExact: report.models.filter((m) => m.comparison.trianglesUnorientedMultisetExact).length,
    allGlbPinsMatch: report.models.every((m) => m.glb.pin.contractPin === 'MATCH'),
    glbImagesTotal: report.models.reduce((n, m) => n + m.glb.images, 0),
    originalUvSetsTotal: report.models.reduce((n, m) => n + m.nif.uvSetsTotal, 0),
    standing: 'NO_GLB_PRESENT_FOR_THESE_IDS RETRACTED. Unoriented agreement does NOT confirm winding/materials/converter lineage; the models remain UNTEXTURED_PROXY (no UV/bindings in the originals; GLB images total 0).',
  };
  report.elapsedMs = Date.now() - t0;

  const text = JSON.stringify(report, null, 1) + '\n';
  if (jsonOut) {
    await fsp.writeFile(jsonOut, text, 'utf8');
    console.error(`[cam_c1_glb_compare] JSON -> ${jsonOut}`);
  }
  console.log(text);
}

main().catch((e) => {
  console.error(`[cam_c1_glb_compare] LOUD FAIL: ${e?.stack ?? e}`);
  process.exit(1);
});
