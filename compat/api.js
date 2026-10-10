// api.js -- PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// The app's read-only SceneIR API client (PLAN ?2; pattern reviewed from
// eudoria-compat-threejs-r1/compat/api.js, rewritten for the bounded wire
// payload of this run). THREE IS NOT IMPORTED HERE -- this module is shared by
// the browser app AND the Node app-integration tests.
//
// FAIL-CLOSED CLIENT POLICY:
//   1. the served provenance must match the client-side PIN (container SHA +
//      payload SHA) -- a mismatch refuses the payload LOUDLY (no render);
//   2. the client recomposes the world transforms ITSELF (composeWorldTransforms
//      from src/pecompat/PecSceneIR.js) and cross-checks them against the
//      shipped FILE_SCENE_SPACE artifact -- a mismatch refuses the payload
//      (wire corruption cannot silently render);
//   3. geometry fingerprints are re-hashed client-side (crypto.subtle; on
//      127.0.0.1 a secure context is expected) and compared with the served
//      recomputed-from-decoded-arrays fingerprints; if subtle is unavailable
//      the check is reported NOT_PERFORMED_SUBTLE_UNAVAILABLE honestly --
//      never silently skipped.
//
// The browser never downloads the whole BNT: the ONLY data path is
// /api/sceneir/218757 (the bounded index-derived SceneIR regenerated at
// server startup from the pinned container).

// relative specifier: resolves in the browser (/compat/api.js -> /src/pecompat/...)
// AND in Node (app-integration tests import this module directly).
import {
  composeWorldTransforms, computeSceneBounds, PEC_SCENEIR_SCHEMA_VERSION,
} from '../src/pecompat/PecSceneIR.js';

export const CLIENT_PIN = Object.freeze({
  modelId: 218757,
  payloadSha256: '3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36',
  containerSha256: 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0',
});

const API_FAIL = (msg) => new Error(`[SceneIRApi] ${msg}`);

// ---------------------------------------------------------------------------
// wire -> asset reconstruction (the SAME record shape buildAssetIR produces;
// typed arrays rebuilt from plain JSON arrays)
// ---------------------------------------------------------------------------
function wireTrsToTrs(w) {
  if (!w) return null;
  return { translate: [...w.translate], rotate: w.rotate.map((r) => [...r]), scale: w.scale };
}

export function wireToAsset(wire, opts = {}) {
  const tol = opts.tolerance ?? 1e-9;
  if (!wire || wire.wireVersion !== 'pec-sceneir-wire-v1') {
    throw API_FAIL(`unsupported wire version ${wire?.wireVersion ?? '(missing)'} -- refusing`);
  }
  // 1. PIN CHECK (fail-closed; the pins travel in the app source, not the wire).
  if (wire.provenance.payloadSha256 !== CLIENT_PIN.payloadSha256 ||
      wire.provenance.containerSha256 !== CLIENT_PIN.containerSha256) {
    throw API_FAIL(
      `PIN MISMATCH -- served payload SHA ${wire.provenance.payloadSha256} / container SHA ${wire.provenance.containerSha256} ` +
      `!= client pins -- refusing (fail-closed; the pinned 218757 identity is mandatory)`);
  }
  if (wire.asset.assetId !== CLIENT_PIN.modelId) {
    throw API_FAIL(`assetId ${wire.asset.assetId} != pinned model ${CLIENT_PIN.modelId} -- refusing`);
  }
  if (wire.cacheKey !== wire.provenance.cacheKey || !wire.cacheKey.includes(wire.provenance.payloadSha256)) {
    throw API_FAIL('cacheKey inconsistent with provenance (asset SHA + adapter/schema version key rule) -- refusing');
  }

  // 2. rebuild the IR record (blocks with typed geometry arrays).
  const blocks = wire.blocks.map((b) => {
    let geometry = null;
    if (b.geometry) {
      geometry = {
        positions: Float32Array.from(b.geometry.positions),
        normals: b.geometry.normals ? Float32Array.from(b.geometry.normals) : null,
        colors: b.geometry.colors ? Float32Array.from(b.geometry.colors) : null,
        uvSets: (b.geometry.uvSets ?? []).map((s) => Float32Array.from(s)),
        indices: Uint16Array.from(b.geometry.indices),
        numVertices: b.geometry.numVertices,
        numTriangles: b.geometry.numTriangles,
        vertexPositionsF32leSha256: b.geometry.vertexPositionsF32leSha256 ?? null,
        triangleIndicesU16leSha256: b.geometry.triangleIndicesU16leSha256 ?? null,
        vertexRange: b.geometry.vertexByteRange ? { start: b.geometry.vertexByteRange[0], end: b.geometry.vertexByteRange[1] } : null,
        indexRange: b.geometry.indexByteRange ? { start: b.geometry.indexByteRange[0], end: b.geometry.indexByteRange[1] } : null,
      };
    }
    return {
      index: b.index,
      type: b.type,
      decodeStatus: b.decodeStatus,
      name: b.name,
      byteStart: b.byteRange[0],
      byteEnd: b.byteRange[1],
      localTrs: wireTrsToTrs(b.localTrs),
      children: b.children ?? null,
      effects: null,
      dataRef: b.dataRef ?? null,
      propertyRefs: b.propertyRefs ?? null,
      extraDataRefs: b.extraDataRefs ?? null,
      geometry,
      fields: null,
      opaque: b.opaqueBoundary
        ? { extStart: b.opaqueBoundary.extStart, extEnd: b.opaqueBoundary.extEnd, extLength: b.opaqueBoundary.extLength, boundaryMethod: b.opaqueBoundary.boundaryMethod }
        : null,
    };
  });
  const ir = {
    schemaVersion: PEC_SCENEIR_SCHEMA_VERSION,
    adapterVersion: wire.provenance.adapterVersion,
    cacheKey: wire.cacheKey,
    asset: {
      assetId: wire.asset.assetId,
      era: wire.asset.era,
      build: wire.asset.build,
      container: wire.asset.container,
      entryName: wire.asset.entryName,
      payloadSha256: wire.asset.payloadSha256,
      sizeBytes: wire.asset.sizeBytes,
      nifVersion: wire.asset.nifVersion,
      numBlocks: wire.asset.numBlocks,
      closure: wire.asset.closure,
    },
    blocks,
    blockTypeCensus: wire.blockTypeCensus,
    decodeCensus: wire.decodeCensus,
    meshAssociations: wire.meshAssociations,
    roots: wire.roots,
    diagnostics: {
      opaqueBlockCount: wire.decodeCensus.PARTIALLY_UNDERSTOOD + wire.decodeCensus.OPAQUE,
      supportedBlockCount: wire.decodeCensus.SUPPORTED,
      unresolvedBindings: (wire.textureBindings ?? [])
        .filter((x) => String(x.status).startsWith('UNTEXTURED'))
        .map((x) => ({ class: 'UNTEXTURED_MESH', meshBlock: x.meshBlock, meshName: x.meshName, status: x.status })),
      unsupportedFeatures: [],
      notes: wire.diagnosticsNotes ?? [],
      textureBindings: wire.textureBindings ?? [],
    },
    computed: null,
  };

  // 3. INDEPENDENT client-side composition + cross-check vs the shipped
  //    FILE_SCENE_SPACE artifact (fail-closed on mismatch).
  let worldTransforms;
  try {
    worldTransforms = composeWorldTransforms(ir);
  } catch (e) {
    throw API_FAIL(`client-side composition failed on the served wire data -- refusing: ${e.message}`);
  }
  const serverWorldByIndex = new Map(
    wire.fileSceneSpaceTransforms.filter((r) => r.worldTrs).map((r) => [r.index, r.worldTrs]));
  for (const [idx, sw] of serverWorldByIndex) {
    const cw = worldTransforms.get(idx);
    if (!cw) throw API_FAIL(`block ${idx}: server world transform present but client composition did not reach it -- refusing`);
    for (let k = 0; k < 3; k++) {
      if (Math.abs(cw.translate[k] - sw.t[k]) > tol) {
        throw API_FAIL(`WIRE CROSS-CHECK FAILED at block ${idx} translate[${k}]: client ${cw.translate[k]} vs shipped ${sw.t[k]} -- refusing`);
      }
    }
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        if (Math.abs(cw.rotate[i][j] - sw.r[i][j]) > tol) {
          throw API_FAIL(`WIRE CROSS-CHECK FAILED at block ${idx} rotate[${i}][${j}]: client ${cw.rotate[i][j]} vs shipped ${sw.r[i][j]} -- refusing`);
        }
      }
    }
    if (Math.abs(cw.scale - sw.s) > tol) {
      throw API_FAIL(`WIRE CROSS-CHECK FAILED at block ${idx} scale: client ${cw.scale} vs shipped ${sw.s} -- refusing`);
    }
  }
  // local TRS must round-trip exactly (bit-exact JSON floats).
  const serverLocalByIndex = new Map(wire.fileSceneSpaceTransforms.map((r) => [r.index, r.localTrs]));
  for (const b of blocks) {
    const sl = serverLocalByIndex.get(b.index);
    if (sl && b.localTrs) {
      for (let k = 0; k < 3; k++) {
        if (b.localTrs.translate[k] !== sl.t[k] || b.localTrs.rotate[k][0] !== sl.r[k][0] ||
            b.localTrs.rotate[k][1] !== sl.r[k][1] || b.localTrs.rotate[k][2] !== sl.r[k][2]) {
          throw API_FAIL(`local TRS round-trip mismatch at block ${b.index} row ${k} -- refusing`);
        }
      }
      if (b.localTrs.scale !== sl.s) throw API_FAIL(`local TRS scale round-trip mismatch at block ${b.index} -- refusing`);
    }
  }

  // 4. bounds cross-check (same arithmetic, independent recompute).
  const clientBounds = computeSceneBounds(ir, worldTransforms);
  const sb = wire.sceneBounds_FILE_SCENE_SPACE;
  for (let k = 0; k < 3; k++) {
    if (Math.abs(clientBounds.min[k] - sb.min[k]) > 1e-6 || Math.abs(clientBounds.max[k] - sb.max[k]) > 1e-6) {
      throw API_FAIL(`scene bounds cross-check failed (axis ${k}) -- refusing`);
    }
  }

  return { ir, worldTransforms, bounds: clientBounds, wire, provenance: wire.provenance };
}

// ---------------------------------------------------------------------------
// client-side geometry fingerprint verification (crypto.subtle; honest
// NOT_PERFORMED_SUBTLE_UNAVAILABLE when the secure-context API is missing)
// ---------------------------------------------------------------------------
async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function verifyGeometryFingerprints(asset) {
  const out = { status: 'OK', verified: 0, mismatches: [], elapsedMs: null };
  const t0 = Date.now();
  if (typeof crypto === 'undefined' || !crypto?.subtle?.digest) {
    out.status = 'NOT_PERFORMED_SUBTLE_UNAVAILABLE';
    out.note = 'crypto.subtle unavailable in this context -- the fingerprint check was NOT executed (honest NOT_PERFORMED, never a silent pass)';
    return out;
  }
  const byIndex = new Map(asset.ir.blocks.map((b) => [b.index, b]));
  for (const assoc of asset.ir.meshAssociations) {
    const g = byIndex.get(assoc.dataBlock)?.geometry;
    if (!g) { out.mismatches.push({ meshBlock: assoc.meshBlock, reason: 'geometry record missing' }); continue; }
    const vSha = await sha256Hex(new Uint8Array(g.positions.buffer, g.positions.byteOffset, g.positions.byteLength));
    const iSha = await sha256Hex(new Uint8Array(g.indices.buffer, g.indices.byteOffset, g.indices.byteLength));
    if (vSha !== assoc.vertexPositionsF32leSha256 || iSha !== assoc.triangleIndicesU16leSha256) {
      out.mismatches.push({
        meshBlock: assoc.meshBlock,
        expected: { vertex: assoc.vertexPositionsF32leSha256, index: assoc.triangleIndicesU16leSha256 },
        client: { vertex: vSha, index: iSha },
      });
    } else {
      out.verified++;
    }
  }
  out.elapsedMs = Date.now() - t0;
  if (out.mismatches.length > 0) out.status = 'FINGERPRINT_MISMATCH';
  return out;
}

// ---------------------------------------------------------------------------
// SceneIRApi -- the app's fetch client (fetch injectable for Node tests)
// ---------------------------------------------------------------------------
export class SceneIRApi {
  constructor(opts = {}) {
    this.baseUrl = opts.baseUrl ?? '';
    this.fetchImpl = opts.fetchImpl ?? ((u) => fetch(u));
    this.transferredBytes = 0;
    this.requestCount = 0;
  }

  async loadAssetIR() {
    const url = `${this.baseUrl}/api/sceneir/${CLIENT_PIN.modelId}`;
    this.requestCount++;
    const res = await this.fetchImpl(url);
    const buf = new Uint8Array(await res.arrayBuffer());
    this.transferredBytes += buf.byteLength;
    if (!res.ok) {
      let errBody = null;
      try { errBody = JSON.parse(new TextDecoder().decode(buf)); } catch { /* non-JSON */ }
      throw API_FAIL(`HTTP ${res.status} for ${url}: ${errBody?.error ?? ''} ${errBody?.message ?? ''}`);
    }
    // provenance headers cross-checked against the body (same memory on the
    // server; a mismatch still refuses the payload loudly).
    const hPayload = res.headers?.get?.('X-PE-Payload-Sha256');
    const wire = JSON.parse(new TextDecoder().decode(buf));
    if (hPayload && hPayload !== wire.provenance.payloadSha256) {
      throw API_FAIL(`X-PE-Payload-Sha256 header ${hPayload} != body ${wire.provenance.payloadSha256} -- refusing`);
    }
    const t0 = Date.now();
    const asset = wireToAsset(wire);
    const buildMs = Date.now() - t0;
    const fingerprintCheck = await verifyGeometryFingerprints(asset);
    return {
      asset,
      fingerprintCheck,
      timings: {
        fetchBytes: buf.byteLength,
        wireBuildMs: buildMs,
        adapterLoadElapsedMs: wire.provenance.elapsedMs,
      },
    };
  }
}

// ---------------------------------------------------------------------------
// buildDiagnosticsModel -- the honest, field-complete diagnostics record the
// app renders (pure function; Node-tested in T8).
// ---------------------------------------------------------------------------
export function buildDiagnosticsModel(asset, extras = {}) {
  const { ir } = asset;
  const bindings = ir.diagnostics.textureBindings ?? [];
  const bound = bindings.filter((b) => b.status === 'TEXTURE_NAME_BOUND').length;
  const untextured = bindings.filter((b) => String(b.status).startsWith('UNTEXTURED')).length;
  return {
    runId: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
    assetIdentity: {
      era: ir.asset.era,
      container: ir.asset.container,
      entryName: ir.asset.entryName,
      payloadSha256: ir.asset.payloadSha256,
      nifVersion: ir.asset.nifVersion,
      cacheKey: ir.cacheKey,
      pinVerified: ir.asset.payloadSha256 === CLIENT_PIN.payloadSha256,
    },
    blockAccounting: {
      total: ir.blocks.length,
      supported: ir.decodeCensus.SUPPORTED,
      partiallyUnderstood: ir.decodeCensus.PARTIALLY_UNDERSTOOD,
      opaque: ir.decodeCensus.OPAQUE,
      note: '62 supported + 4 Ark blocks (2 PARTIALLY_UNDERSTOOD + 2 OPAQUE) -- the 62+4=66 ceiling preserved; Ark semantics not silently decoded',
    },
    meshes: {
      imported: ir.meshAssociations.length,
      renderedClaim: 'rendered == imported unless excluded by the visible ledger below; the app never claims more rendered than visible',
      visibleLedger: extras.visibleLedger ?? null,
    },
    textureStatus: {
      nameBound: bound,
      untexturedLabeled: untextured,
      perMesh: bindings.map((b) => ({ meshBlock: b.meshBlock, meshName: b.meshName, status: b.status, textureNames: b.textureNames })),
      containerResolution: 'NOT_ESTABLISHED (name/property bindings only; no texture bytes resolved in this run)',
    },
    transforms: {
      spaces: 'serialized local TRS / composed FILE_SCENE_SPACE world / authored scene transform / render conversion -- DISTINCT quantities',
      renderConversion: asset.wire.renderAdapterChoice,
      policyLabels: asset.wire.policyLabels,
    },
    loadTimings: extras.loadTimings ?? null,
    fingerprintCheck: extras.fingerprintCheck ?? null,
    errors: extras.errors ?? [],
  };
}
