// Bnt2TerrainArchive.js — MILESTONE 1-E ITER 019 (CLEAN_RUNTIME_FOUNDATION, era PCG_9_3_5)
// Era-versioned archive reader for pcg_install\Data\Terrain\terrain.bnt (9.3.5).
//
// WHY THIS CLASS EXISTS (ledger ENTRY #3 decoder versioning rule; era-validation
// evidence iter019_era_validation_terrain_bnt.json):
//   terrain.bnt 9.3.5 (SHA 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990)
//   is BNT2-footer framed (NOT the JUL 50.bnt BUNT framing). The directory entry
//   layout is variable (0x0A-terminated name + u32 size + u32 offset + u32 crc32
//   + u32 pad) while JUL 50.bnt uses fixed 21-byte entries. Record framing
//   (02 00 00 FF + u32 decompressedSize + zlib) and the trailing-8-bytes size
//   semantics are THE SAME as the JUL path (strict 25/25 sample inflation).
//   The legacy BuntArchive (JUL BUNT path) is REUSED AS-IS and is never fed
//   terrain.bnt — this class is the era-versioned variant, never a silent
//   reinterpretation of the JUL reader.
//
// INDEX FACTS (era-validated 2026-09-04, evidence JSON):
//   58,451 entries total = 51,920 regular (220x236 filename-xy grid, IDENTICAL
//   name convention to JUL: 'XXXXXXXX.tdf', 8 hex chars = grid x|y)
//   + 6,530 special-row tiles (y rows 0xff1a..0xffff — skirt rows, semantics
//   UNRESOLVED, explicitly excluded from regular terrain rendering)
//   + 1 sentinel (7ffe7ffe.tdf).

export const BNT2_TERRAIN_MAGIC = 'BNT2';
export const BNT2_TERRAIN_RECORD_MARKER = 0xFF000002; // LE read of 02 00 00 FF
export const BNT2_TERRAIN_TRAILING_BYTES = 8;          // size field = 8-byte header + zlib stream

export class Bnt2TerrainArchive {
  /**
   * @param {Uint8Array} wholeFile raw bytes of terrain.bnt (PCG_9_3_5)
   * @param {object} io { inflate(bytes: Uint8Array) -> Uint8Array }  STRICT inflate
   */
  constructor(wholeFile, io) {
    this.io = io;
    this.bytes = wholeFile;
    if (wholeFile.byteLength < 8) throw new Error('[Bnt2TerrainArchive] file too small');
    const dv = new DataView(wholeFile.buffer, wholeFile.byteOffset, wholeFile.byteLength);
    const magic = String.fromCharCode(...wholeFile.subarray(wholeFile.byteLength - 4));
    if (magic !== BNT2_TERRAIN_MAGIC) {
      throw new Error(`[Bnt2TerrainArchive] bad footer magic ${magic} (expected BNT2)`);
    }
    this.dirOffset = dv.getUint32(wholeFile.byteLength - 8, true);
    this.count = dv.getUint32(this.dirOffset, true);
    this._dv = dv;
    this._entries = null;
    this._byName = null;
  }

  entries() {
    if (this._entries) return this._entries;
    const out = [];
    let p = this.dirOffset + 4;
    for (let i = 0; i < this.count; i++) {
      const nameStart = p;
      while (p < this.bytes.length && this.bytes[p] !== 0x0a) p++;
      if (p >= this.bytes.length) throw new Error(`[Bnt2TerrainArchive] entry ${i}: unterminated name`);
      const name = String.fromCharCode(...this.bytes.subarray(nameStart, p));
      p++; // skip 0x0A
      const size = this._dv.getUint32(p, true);
      const offset = this._dv.getUint32(p + 4, true);
      const crc32 = this._dv.getUint32(p + 8, true);
      p += 16; // size, offset, crc32, pad
      out.push({ entryIndex: i, name, size, offset, crc32 });
    }
    if (p !== this.bytes.length - 8) {
      throw new Error(
        `[Bnt2TerrainArchive] directory end ${p} != footer-8 ${this.bytes.length - 8} (count=${this.count})`);
    }
    this._entries = out;
    return out;
  }

  entryByName(name) {
    if (!this._byName) {
      this._byName = new Map();
      for (const e of this.entries()) this._byName.set(e.name, e);
    }
    return this._byName.get(name) ?? null;
  }

  /**
   * Reads and decompresses one entry. Record framing (era-validated):
   *   @offset: [marker 02 00 00 FF][u32 LE decompressed_size][zlib stream]
   *   stream slice = [offset+8, offset+size)   (size = 8 + stream length)
   * @returns {{payload: Uint8Array, entry: object}}
   */
  async readEntry(entry) {
    if (entry.offset + 8 > this.bytes.length) {
      throw new Error(`[Bnt2TerrainArchive] entry ${entry.name} beyond EOF`);
    }
    const rec = this.bytes.subarray(entry.offset, entry.offset + entry.size);
    const marker = this._dv.getUint32(entry.offset, true);
    if (marker !== BNT2_TERRAIN_RECORD_MARKER) {
      throw new Error(
        `[Bnt2TerrainArchive] entry ${entry.name}: bad record marker 0x${marker.toString(16)}`);
    }
    const decompressedSize = this._dv.getUint32(entry.offset + 4, true);
    const stream = rec.subarray(8, entry.size); // size-8 stream bytes after the 8-byte header
    const payload = await this.io.inflate(stream);
    if (payload.byteLength !== decompressedSize) {
      throw new Error(
        `[Bnt2TerrainArchive] entry ${entry.name}: inflated ${payload.byteLength} != header ${decompressedSize}`);
    }
    return { payload, entry };
  }
}
