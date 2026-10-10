// PecAssetAdapter.js — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// The bounded PE adapter for model 218757 (contract §7): pinned Models.bnt
// bytes -> extraction identity verification (fail-closed) -> extended v10.1
// reader (PecNif10Reader.js) -> SceneIR asset record (PecSceneIR.js).
//
// INPUT IDENTITY IS AUTHORITY: the payload is extracted EVERY load from the
// pinned container via the BNT2 index entry — never from a stale exported
// JSON. The container SHA256 and the exact payload SHA256 are verified against
// the run pins (LOUD fail-closed on mismatch); the index ordinal/offset are
// CROSS-CHECKS (loud on mismatch, but the hashes are the extraction
// authority). The SDK loader is NOT invoked; NO NiArk factories are
// fabricated; NO new 9-byte-tail semantics are derived (per-entry tails are
// recorded RAW — semantics UNRESOLVED for 218757).
//
// REUSE LABEL: the BNT2 framing reader src/pesource/Bnt2Archive.js (the base
// repo's era-validated extraction chain) is imported and used for index-derived
// extraction. src/pesource/NifModelReader.js is NOT used (457485 single-witness
// reader; stays untouched) — the NIF decode is the NEW extended reader.
//
// CACHE KEYS include the asset SHA + adapter/schema version (sceneCacheKey).
//
// TEXTURE BINDING POLICY (this run): only independently reproduced NAME /
// PROPERTY bindings — the per-part texture names + per-entry NiTexturingProperty
// refs are re-derived from the NiArkTextureExtraData bytes in THIS reader.
// Container resolution (which Textures.bnt entry a name resolves to) is
// NOT_ESTABLISHED for 218757 (predecessor verdict: RESOURCE_NAME_REFERENCES_ONLY;
// the 'BNT2 id' tail reading stays a RETRACTED prior claim). Unknown/missing
// bindings yield a labeled UNTEXTURED material status + diagnostic; geometry
// remains viewable. NO cross-era texture substitutions, no guessed IDs.

import { Bnt2Archive } from '../pesource/Bnt2Archive.js';
import { readNif10, attachGeometryFingerprints, PEC_NIF10_READER_VERSION } from './PecNif10Reader.js';
import {
  buildAssetIR, validateSceneGraph, composeWorldTransforms, computeSceneBounds,
  PEC_SCENEIR_SCHEMA_VERSION,
} from './PecSceneIR.js';

export const PEC_ADAPTER_VERSION = 'pec-nif101-adapter-v1';

/** The pinned input identities for model 218757 (contract §2 + phase-1
 * INPUT_IDENTITIES.json — re-verified by this adapter at every load). */
export const MODEL_218757_PINS = Object.freeze({
  era: 'PCG_9_3_5',
  modelsBntPath: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt',
  modelsBntSha256: 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0',
  modelsBntSize: 395412868,
  modelId: 218757,
  entryName: '218757.nif',
  entryOrdinal: 781,          // cross-check (0-based directory ordinal)
  payloadOffset: 116223520,   // cross-check
  payloadSize: 57316,
  payloadSha256: '3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36',
});

const BOUND = (msg) => new Error(`[PecAssetAdapter] ${msg}`);

export class PecAssetAdapter {
  /**
   * @param {object} io — { readFile(path): Promise<Uint8Array>,
   *                         sha256(bytes): string }  (sync hash, injected per environment)
   * @param {object} opts — { modelsBntPath?, pins? } (defaults = the run pins)
   */
  constructor(io, opts = {}) {
    if (!io || typeof io.readFile !== 'function' || typeof io.sha256 !== 'function') {
      throw BOUND('io adapter (readFile, sha256) required');
    }
    this.io = io;
    this.pins = opts.pins ?? MODEL_218757_PINS;
    this.modelsBntPath = opts.modelsBntPath ?? this.pins.modelsBntPath;
    this._archive = null; // lazy per-mount
  }

  async _loadArchive() {
    if (this._archive) return this._archive;
    const bytes = await this.io.readFile(this.modelsBntPath);
    if (this.pins.modelsBntSize && bytes.byteLength !== this.pins.modelsBntSize) {
      throw BOUND(`container size ${bytes.byteLength} != pinned ${this.pins.modelsBntSize} — REFUSING (fail-closed)`);
    }
    const containerSha = this.io.sha256(bytes).toLowerCase();
    if (containerSha !== this.pins.modelsBntSha256.toLowerCase()) {
      throw BOUND(`container SHA256 ${containerSha} != pinned ${this.pins.modelsBntSha256} — REFUSING (fail-closed era integrity)`);
    }
    this._archive = { bytes, containerSha256: containerSha, archive: new Bnt2Archive(bytes) };
    return this._archive;
  }

  /**
   * extractPinnedPayload — index-derived extraction + FULL identity
   * verification. Fail-closed on any pin mismatch.
   * @returns {{ payload: Uint8Array, entry: object, containerSha256: string,
   *             payloadSha256: string, crossChecks: object }}
   */
  async extractPinnedPayload(modelId = this.pins.modelId) {
    const { archive, containerSha256 } = await this._loadArchive();
    const entryName = `${modelId}.nif`;
    const entry = archive.entryByName(entryName);
    if (!entry) {
      throw BOUND(`entry ${entryName} NOT_FOUND in ${this.modelsBntPath} (LOUD — no fallback, no header scanning)`);
    }
    // cross-checks (loud, but the hash is the extraction authority)
    const crossChecks = {
      entryOrdinal: {
        expected: this.pins.entryOrdinal, measured: entry.entryIndex,
        match: entry.entryIndex === this.pins.entryOrdinal,
      },
      payloadOffset: {
        expected: this.pins.payloadOffset, measured: entry.offset,
        match: entry.offset === this.pins.payloadOffset,
      },
      payloadSize: {
        expected: this.pins.payloadSize, measured: entry.size,
        match: entry.size === this.pins.payloadSize,
      },
    };
    const { payload } = archive.readEntry(entry);
    if (payload.byteLength !== this.pins.payloadSize) {
      throw BOUND(`payload size ${payload.byteLength} != pinned ${this.pins.payloadSize} — REFUSING (fail-closed)`);
    }
    const payloadSha256 = this.io.sha256(payload).toLowerCase();
    if (payloadSha256 !== this.pins.payloadSha256.toLowerCase()) {
      throw BOUND(`payload SHA256 ${payloadSha256} != pinned ${this.pins.payloadSha256} — REFUSING (fail-closed; the hash is the extraction authority)`);
    }
    return { payload, entry, containerSha256, payloadSha256, crossChecks, entryName };
  }

  /**
   * loadModel — full chain: pinned extraction -> extended reader -> SceneIR
   * asset -> fingerprint recomputation -> texture binding resolution ->
   * validation. Returns { ir, worldTransforms, validation, sceneBounds,
   * meshFingerprints, provenance }.
   */
  async loadModel(modelId = this.pins.modelId) {
    const t0 = Date.now();
    const ex = await this.extractPinnedPayload(modelId);
    const readerResult = readNif10(ex.payload, { sourceName: ex.entryName });
    // Fingerprints: exact serialized f32-LE vertex / u16-LE triangle arrays,
    // recomputed from the DECODED arrays and cross-checked against the
    // serialized byte ranges (round-trip proof) — see attachGeometryFingerprints.
    const meshFingerprints = attachGeometryFingerprints(readerResult, this.io.sha256);
    for (const rec of meshFingerprints) {
      if (rec.vertexRoundtripExact === false || rec.indexRoundtripExact === false) {
        throw BOUND(`data block ${rec.dataBlock}: decoded-array fingerprint != serialized byte range (round-trip broken) — REFUSING`);
      }
    }
    const ir = buildAssetIR(readerResult, {
      assetId: modelId,
      era: this.pins.era,
      build: 'PCG_9_3_5_Models_bnt_entry',
      container: 'Models/Models.bnt',
      entryName: ex.entryName,
      payloadSha256: ex.payloadSha256,
      sizeBytes: ex.payload.byteLength,
      adapterVersion: PEC_ADAPTER_VERSION,
      physicalSource: this.modelsBntPath,
    });
    // Texture bindings: independently re-derived NAME/PROPERTY bindings only.
    resolveTextureBindings(ir);
    const validation = validateSceneGraph(ir);
    const worldTransforms = composeWorldTransforms(ir);
    const sceneBounds = computeSceneBounds(ir, worldTransforms);
    const elapsedMs = Date.now() - t0;
    return {
      ir,
      worldTransforms,
      validation,
      sceneBounds,
      meshFingerprints,
      provenance: {
        era: this.pins.era,
        container: 'Models/Models.bnt',
        physicalSource: this.modelsBntPath,
        containerSha256: ex.containerSha256,
        entryName: ex.entryName,
        entryOrdinal: ex.entry.entryIndex,
        entryOffset: ex.entry.offset,
        entrySize: ex.entry.size,
        entryCrc32: ex.entry.crc32,
        payloadSha256: ex.payloadSha256,
        payloadSize: ex.payload.byteLength,
        adapterVersion: PEC_ADAPTER_VERSION,
        readerVersion: PEC_NIF10_READER_VERSION,
        schemaVersion: PEC_SCENEIR_SCHEMA_VERSION,
        cacheKey: ir.cacheKey,
        crossChecks: ex.crossChecks,
        elapsedMs,
      },
    };
  }
}

/**
 * resolveTextureBindings — per-mesh texture binding status, derived ONLY from
 * the independently parsed NiArkTextureExtraData entries + NiTexturingProperty
 * refs. No container resolution (NOT_ESTABLISHED); no tail semantics; no
 * cross-era substitutions. Results land in ir.diagnostics.textureBindings.
 */
export function resolveTextureBindings(ir) {
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  // ArkTexture entries: { entryName, f1, f2, texturingPropertyRef, bytes9Hex }
  const arkEntries = [];
  for (const b of ir.blocks) {
    if (b.type === 'NiArkTextureExtraData') {
      for (const e of b.fields?.entries ?? []) {
        arkEntries.push({
          arkBlock: b.index,
          arkEntryName: e.entryName,
          f1: e.f1,
          f2: e.f2,
          texturingPropertyRef: e.texturingPropertyRef,
          bytes9Hex: e.bytes9Hex,
        });
      }
    }
  }
  const bindings = [];
  for (const b of ir.blocks) {
    if (b.type !== 'NiTriShape') continue;
    const texpropRefs = (b.propertyRefs ?? []).filter((r) => r != null && r >= 0 && byIndex.get(r)?.type === 'NiTexturingProperty');
    const materialRefs = (b.propertyRefs ?? []).filter((r) => r != null && r >= 0 && byIndex.get(r)?.type === 'NiMaterialProperty');
    let status;
    let names = [];
    if (texpropRefs.length === 0) {
      status = 'UNTEXTURED_NO_TEXPROP';
    } else {
      names = arkEntries
        .filter((e) => texpropRefs.includes(e.texturingPropertyRef))
        .map((e) => e.arkEntryName);
      if (names.length === 0) {
        status = texpropRefs.length > 1 ? 'UNTEXTURED_MULTI_TEXPROP_UNRESOLVED' : 'UNTEXTURED_NO_ARK_ENTRY';
      } else {
        status = 'TEXTURE_NAME_BOUND';
      }
    }
    bindings.push({
      meshBlock: b.index,
      meshName: b.name,
      texturePropertyRefs: texpropRefs,
      materialPropertyRefs: materialRefs,
      textureNames: names,
      status,
      containerResolution: 'NOT_ESTABLISHED (name/property bindings only; no texture bytes resolved in this run)',
    });
  }
  ir.diagnostics.textureBindings = bindings;
  ir.diagnostics.unresolvedBindings.push(
    ...bindings.filter((x) => x.status.startsWith('UNTEXTURED')).map((x) => ({
      class: 'UNTEXTURED_MESH', meshBlock: x.meshBlock, meshName: x.meshName, status: x.status,
    })));
  ir.diagnostics.notes.push(
    'TEXTURE_BINDING_POLICY: name/property bindings re-derived from NiArkTextureExtraData bytes in this reader; ' +
    'container resolution NOT_ESTABLISHED for 218757 (RESOURCE_NAME_REFERENCES_ONLY; per-entry 9-byte tails recorded RAW, semantics UNRESOLVED — no new tail semantics derived)',
  );
  return bindings;
}
