// PESourceMount.js — PE MILESTONE 1 ITER 001 (PE_WORLD_SURFACE_FIDELITY_R1)
// The era-aware source/compatibility layer (charter §7). The ORIGINAL PE
// installation is mounted; the runtime consumes original bytes through this
// layer. NO renderer semantics. NO silent cross-era substitution.
//
// Interface (charter):
//   mountEra(...) / enumerate(...) / openResource(...)
//   getTerrainTile(...) / resolveTexture(...) / getVegetationClimate(...)
//   getWaterResource(...)  [NOT_RECOVERED — explicit, see charter §6]
//
// I/O is injected (NodeSourceAdapter for audits/tests, BrowserSourceAdapter
// for the runtime) so this module is environment-neutral.
//
// Gate scope (M1-A): terrain (50.bnt BUNT). resolveTexture /
// getVegetationClimate / getWaterResource exist as EXPLICIT stubs with
// evidence status — they are implemented in their own gates (B/C/D) and must
// fail loudly, never silently fall back to a derived cache.

import { BuntArchive } from './BuntArchive.js';
import { Bnt2Archive } from './Bnt2Archive.js';
import { ArkArchive } from './ArkArchive.js';
import { decodeTdfPayload, gridFromName, isSentinelName, TDF_SENTINEL_NAME } from './TdfDecoder.js';
import { TerrainTile, HEIGHT_SCALE_CALIBRATION } from './TerrainTile.js';
import { makeProvenance, EVIDENCE_STATUS, ERAS, KNOWN_HASHES } from './PEProvenance.js';

export const PESOURCE_DECODER_VERSION = 'pesource-m1-v1';

export class PESourceMount {
  /**
   * @param {object} io — { readFile(path): Promise<Uint8Array>,
   *                         inflate(bytes): Promise<Uint8Array>,
   *                         sha256(bytes): Promise<string> (optional, for mount verification) }
   */
  constructor(io) {
    if (!io || typeof io.readFile !== 'function' || typeof io.inflate !== 'function') {
      throw new Error('[PESourceMount] io adapter (readFile, inflate) required');
    }
    this.io = io;
    this.mounts = new Map(); // era:containerKey -> mount record
    this.archives = new Map(); // era:containerKey -> BuntArchive (lazy)
  }

  /**
   * mountEra — register a source container for an era.
   * @param {object} opts { era, container, path, expectedSha256?, verifyHash? }
   * The era is part of the identity: JUL_2003 is the primary historical target;
   * other eras mount for comparison/RE only and are never silently mixed.
   */
  async mountEra({ era, container, path, expectedSha256 = null, verifyHash = false, format = 'BUNT' }) {
    if (!Object.values(ERAS).includes(era)) throw new Error(`[PESourceMount] unknown era ${era}`);
    if (!['BUNT', 'BNT2', 'ARKVFS'].includes(format)) {
      throw new Error(`[PESourceMount] unknown container format ${format}`);
    }
    const key = `${era}:${container}`;
    if (this.mounts.has(key)) throw new Error(`[PESourceMount] ${key} already mounted`);
    const known = KNOWN_HASHES[key];
    const expect = expectedSha256 ?? known ?? null;
    const bytes = await this.io.readFile(path);
    let actualSha256 = null;
    if (expect || verifyHash) {
      if (typeof this.io.sha256 !== 'function') {
        throw new Error('[PESourceMount] hash verification requested but io.sha256 unavailable');
      }
      actualSha256 = await this.io.sha256(bytes);
      if (expect && actualSha256.toLowerCase() !== expect.toLowerCase()) {
        throw new Error(
          `[PESourceMount] ${key} SHA256 MISMATCH: got ${actualSha256}, expected ${expect} — REFUSING to mount (era integrity)`);
      }
    }
    const mount = {
      era, container, path, bytes, format,
      expectedSha256: expect, actualSha256,
      hashVerified: actualSha256 !== null && (expect === null || actualSha256.toLowerCase() === expect.toLowerCase()),
    };
    this.mounts.set(key, mount);
    return mount;
  }

  _mount(era, container) {
    const key = `${era}:${container}`;
    const m = this.mounts.get(key);
    if (!m) throw new Error(`[PESourceMount] ${key} not mounted`);
    return m;
  }

  _archive(era, container) {
    const key = `${era}:${container}`;
    let arch = this.archives.get(key);
    if (!arch) {
      const m = this._mount(era, container);
      arch = new BuntArchive(m.bytes, this.io);
      this.archives.set(key, arch);
    }
    return arch;
  }

  /**
   * Texture-container reader (ITER_010, Gate B). The container format is part
   * of the mount record ('BNT2' -> Textures.bnt, 'ARKVFS' -> Textures.ark).
   * Format knowledge stays in the format layer (Bnt2Archive / ArkArchive).
   */
  _textureReader(era, container) {
    const key = `${era}:${container}`;
    let reader = this.textureReaders?.get(key);
    if (!reader) {
      const m = this._mount(era, container);
      const format = m.format;
      if (format === 'BNT2') reader = new Bnt2Archive(m.bytes);
      else if (format === 'ARKVFS') reader = new ArkArchive(m.bytes);
      else throw new Error(`[PESourceMount] ${key} is not a texture container (format=${format})`);
      if (!this.textureReaders) this.textureReaders = new Map();
      this.textureReaders.set(key, reader);
    }
    return reader;
  }

  /** enumerate — list entries of a mounted container, with provenance. */
  async enumerate({ era, container }) {
    const arch = this._archive(era, container);
    const m = this._mount(era, container);
    return arch.entries().map((e) => ({
      entryIndex: e.entryIndex, // NOTE: index order is an archive artifact — NOT grid order
      name: e.name,
      packedSize: e.packedSize,
      offset: e.offset,
      provenance: makeProvenance({
        era, container, entry: e.name, physicalSource: m.path, offset: e.offset,
        decoderVersion: PESOURCE_DECODER_VERSION,
        evidenceStatus: EVIDENCE_STATUS.CONFIRMED,
        extra: { hashVerified: m.hashVerified },
      }),
    }));
  }

  /** openResource — raw entry payload + provenance (no decode). */
  async openResource({ era, container, entryName }) {
    const arch = this._archive(era, container);
    const m = this._mount(era, container);
    const entry = arch.entryByName(entryName);
    if (!entry) throw new Error(`[PESourceMount] entry ${entryName} not found in ${era}:${container}`);
    const { payload } = await arch.readEntry(entry);
    return {
      payload,
      provenance: makeProvenance({
        era, container, entry: entryName, physicalSource: m.path, offset: entry.offset,
        decoderVersion: PESOURCE_DECODER_VERSION,
        evidenceStatus: EVIDENCE_STATUS.CONFIRMED,
        extra: { packedSize: entry.packedSize, hashVerified: m.hashVerified },
      }),
    };
  }

  /**
   * getTerrainTile — canonical TerrainTile from ORIGINAL bytes.
   * Grid addressing is FILENAME-XY ONLY (entry-index ordering is REJECTED —
   * it caused horizontal bands; superseded 2026-07-28).
   * The sentinel tile (7ffe7ffe.tdf) is handled EXPLICITLY and never returned
   * as a regular tile.
   */
  async getTerrainTile({ era, gridX, gridY }) {
    if (era !== ERAS.JUL_2003) {
      // Only the JUL-2003 50.bnt terrain is decoded by this gate. Other eras
      // must not be silently substituted for historical truth.
      throw new Error(
        `[PESourceMount] getTerrainTile: era ${era} is not the canonical JUL_2003 terrain (NO silent era substitution)`);
    }
    if (!Number.isInteger(gridX) || !Number.isInteger(gridY) ||
        gridX < 0 || gridX > 219 || gridY < 0 || gridY > 235) {
      throw new Error(`[PESourceMount] grid out of range 0..219/0..235: ${gridX},${gridY}`);
    }
    const name = gridX.toString(16).padStart(4, '0') + gridY.toString(16).padStart(4, '0') + '.tdf';
    if (isSentinelName(name)) {
      throw new Error('[PESourceMount] sentinel tile requested — use getSentinel()');
    }
    const container = 'Terrain/50.bnt';
    const m = this._mount(era, container);
    const arch = this._archive(era, container);
    const entry = arch.entryByName(name);
    if (!entry) throw new Error(`[PESourceMount] tile ${name} not found in ${container}`);
    const { payload } = await arch.readEntry(entry);
    const decoded = decodeTdfPayload(payload, { name, gridX, gridY });
    return new TerrainTile({
      gridX, gridY, name,
      heights: decoded.heights,
      header: decoded.header,
      subheader: decoded.subheader,
      tail: decoded.tail,
      provenance: makeProvenance({
        era, container, entry: name, physicalSource: m.path, offset: entry.offset,
        decoderVersion: PESOURCE_DECODER_VERSION,
        evidenceStatus: EVIDENCE_STATUS.CONFIRMED,
        extra: {
          packedSize: entry.packedSize,
          decompressedSize: payload.byteLength,
          heightDataOffsetPayloadRelative: 64, // explicit: heights @64..2111 payload-relative
          mask16OffsetRecordRelative: 52,     // explicit: material mask @52..307 RECORD-relative
          offsetSpacesSeparated: true,
          hashVerified: m.hashVerified,
        },
      }),
    });
  }

  /** The sentinel/overview tile, explicit (charter §3: handled explicitly). */
  async getSentinelInfo({ era }) {
    const container = 'Terrain/50.bnt';
    const m = this._mount(era, container);
    const arch = this._archive(era, container);
    const entry = arch.entryByName(TDF_SENTINEL_NAME);
    if (!entry) throw new Error('[PESourceMount] sentinel tile missing (expected 7ffe7ffe.tdf)');
    const { payload } = await arch.readEntry(entry);
    const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
    return {
      name: TDF_SENTINEL_NAME,
      decompressedSize: payload.byteLength,
      dataSize: dv.getUint32(8, true),
      tileDim: dv.getUint32(12, true),
      provenance: makeProvenance({
        era, container, entry: TDF_SENTINEL_NAME, physicalSource: m.path, offset: entry.offset,
        decoderVersion: PESOURCE_DECODER_VERSION,
        evidenceStatus: EVIDENCE_STATUS.CONFIRMED,
        extra: { role: 'SENTINEL_OVERVIEW_NOT_REGULAR_TILE' },
      }),
    };
  }

  /**
   * resolveTexture — Gate B (ITER_010). Resolves a numeric texture resource ID
   * against a MOUNTED, ERA-EXPLICIT texture container (BNT2 'Textures.bnt' or
   * ArkVFS 'Textures.ark'). The ID space is the canon BNT2 texture resource ID
   * (M3-4-R2B CONFIRMED: u32 LE embedded in ArkTexture records; entry name =
   * '<id>.dat' / '<id>.<ext>').
   *
   * NO silent cross-era substitution: the era+container must be mounted
   * explicitly by the caller; a JUL_2003 texture container does NOT exist in
   * the original installation (auditor-verified 2026-09-04) — every era used
   * here is a CROSS-ERA dependency and the provenance records it.
   *
   * @returns {{payload: Uint8Array, provenance: object}}
   * @throws if not mounted / not a texture container / ID not found (NOT_FOUND
   *   is LOUD — callers record unresolved IDs explicitly, never fall back).
   */
  async resolveTexture({ era, container, textureId }) {
    if (!Number.isInteger(textureId) || textureId < 0) {
      throw new Error(`[PESourceMount] invalid textureId ${textureId}`);
    }
    const m = this._mount(era, container); // throws LOUDLY if not mounted
    const reader = this._textureReader(era, container); // throws if not a texture container
    const entry = reader.entryById(textureId);
    if (!entry) {
      throw new Error(`[PESourceMount] textureId ${textureId} NOT_FOUND in ${era}:${container}`);
    }
    const { payload } = reader.readEntry(entry);
    return {
      payload,
      entry,
      provenance: makeProvenance({
        era, container, entry: entry.name, physicalSource: m.path, offset: entry.offset ?? entry.dataOffset ?? null,
        decoderVersion: PESOURCE_DECODER_VERSION,
        evidenceStatus: EVIDENCE_STATUS.CONFIRMED,
        extra: {
          textureId, containerFormat: m.format, payloadSize: payload.byteLength,
          hashVerified: m.hashVerified,
          crossEra: era !== 'JUL_2003', // explicit cross-era tag (always true for texture containers)
        },
      }),
    };
  }

  /** getVegetationClimate — Gate C scope. NOT IMPLEMENTED in M1-A. */
  async getVegetationClimate() {
    throw new Error(
      '[PESourceMount] getVegetationClimate: NOT_IMPLEMENTED_IN_THIS_GATE (Gate C — foliage/biome origin)');
  }

  /** getWaterResource — Gate D scope. The original water system is NOT_RECOVERED. */
  async getWaterResource() {
    throw new Error(
      '[PESourceMount] getWaterResource: NOT_RECOVERED (Gate D — original water system forensics pending)');
  }

  get heightScaleCalibration() { return HEIGHT_SCALE_CALIBRATION; }
}
