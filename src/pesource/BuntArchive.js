// BuntArchive.js — PE MILESTONE 1 ITER 001 (PE_WORLD_SURFACE_FIDELITY_R1)
// BUNT-footer archive reader (the 50.bnt framing, JUL-2003 Eudoria terrain).
//
// FORMAT (CONFIRMED — pe-bnt-tdf skill + FULL_SYNC §05; 51,921-entry corpus):
//   Last 8 bytes:  [uint32 LE index_offset]['BUNT' magic]
//   Index:         [uint32 LE count][count x 21-byte entries]
//   Entry:         [13-byte name 'XXXXXXXX.tdf'][uint32 LE packed_size][uint32 LE offset]
//   Record @offset:[marker 02 00 00 FF][uint32 LE decompressed_size][zlib stream]
//
// NO entry-index ordering semantics: the entry ORDER in the index is an
// artifact; grid placement comes ONLY from the entry NAME (filename-xy).

export const BUNT_ENTRY_MARKER = 0xFF000002; // little-endian read of bytes 02 00 00 FF
export const BUNT_ENTRY_NAME_LEN = 13;
export const BUNT_ENTRY_SIZE = 21;           // 13 name + 4 packed + 4 offset
export const BUNT_MAGIC = 0x544E5542;        // 'BUNT' little-endian
// BNT index quirk (CONFIRMED by M1_ITER_005i full scan, 2026-09-04): for ALL
// 51,921 entries the index `packed_size` field counts 8 bytes MORE than the
// zlib stream — the slice [offset+8, offset+8+packedSize) contains the zlib
// stream followed by the NEXT record's 8-byte header (02 00 00 FF marker +
// u32 decompressed size). TRUE compressed stream length = packedSize - 8.
// Node zlib.inflateSync tolerates the trailing bytes (why the Node oracle
// iterations passed); Chromium DecompressionStream is STRICT and rejects
// with "Junk found after end of compressed data", which the browser inflate
// surfaced as an opaque "TypeError: Failed to fetch" (iter005 root cause).
export const BUNT_TRAILING_BYTES = 8;

export class BuntArchive {
  /**
   * @param {Uint8Array} wholeFile raw bytes of the .bnt file
   * @param {object} io  { inflate(bytes: Uint8Array) -> Uint8Array }
   */
  constructor(wholeFile, io) {
    this.io = io;
    this.bytes = wholeFile;
    const dv = new DataView(wholeFile.buffer, wholeFile.byteOffset, wholeFile.byteLength);
    if (wholeFile.byteLength < 8) throw new Error('[BuntArchive] file too small');
    const magic = dv.getUint32(wholeFile.byteLength - 4, true);
    if (magic !== BUNT_MAGIC) {
      throw new Error(`[BuntArchive] bad footer magic: 0x${magic.toString(16)} (expected BUNT)`);
    }
    const indexOffset = dv.getUint32(wholeFile.byteLength - 8, true);
    if (indexOffset <= 0 || indexOffset >= wholeFile.byteLength - 8) {
      throw new Error(`[BuntArchive] implausible index offset ${indexOffset}`);
    }
    const count = dv.getUint32(indexOffset, true);
    const indexEnd = indexOffset + 4 + count * BUNT_ENTRY_SIZE;
    if (indexEnd !== wholeFile.byteLength - 8) {
      throw new Error(
        `[BuntArchive] index size mismatch: index ends at ${indexEnd}, footer at ${wholeFile.byteLength - 8}, count=${count}`);
    }
    this.count = count;
    this.indexOffset = indexOffset;
    this._dv = dv;
    this._entries = null; // lazily built: [{name, packedSize, offset, entryIndex}]
    this._byName = null;
  }

  entries() {
    if (this._entries) return this._entries;
    const out = [];
    for (let i = 0; i < this.count; i++) {
      const p = this.indexOffset + 4 + i * BUNT_ENTRY_SIZE;
      let name = '';
      for (let j = 0; j < BUNT_ENTRY_NAME_LEN; j++) {
        const c = this.bytes[p + j];
        if (c === 0) break;
        name += String.fromCharCode(c);
      }
      // The 13-byte name field is 'XXXXXXXX.tdf' + '\n' (0x0a), not NUL-padded
      // (byte-verified 2026-09-06 against the 50.bnt index; last entry
      // '7ffe7ffe.tdf\n').
      name = name.replace(/[\r\n\0]+$/, '');
      out.push({
        entryIndex: i,
        name,
        packedSize: this._dv.getUint32(p + BUNT_ENTRY_NAME_LEN, true),
        offset: this._dv.getUint32(p + BUNT_ENTRY_NAME_LEN + 4, true),
      });
    }
    this._entries = out;
    return out;
  }

  entryByName(name) {
    if (!this._byName) {
      this._byName = new Map();
      for (const e of this.entries()) {
        if (this._byName.has(e.name)) throw new Error(`[BuntArchive] duplicate entry name ${name}`);
        this._byName.set(e.name, e);
      }
    }
    return this._byName.get(name) ?? null;
  }

  /**
   * Reads + inflates one entry record. Validates the framing.
   * @returns {{payload: Uint8Array, entry: object, decompressedSize: number}}
   */
  async readEntry(entry) {
    const off = entry.offset;
    const dv = this._dv;
    if (off + 8 > this.bytes.byteLength) throw new Error(`[BuntArchive] entry ${entry.name} offset beyond EOF`);
    const marker = dv.getUint32(off, true);
    if (marker !== BUNT_ENTRY_MARKER) {
      throw new Error(`[BuntArchive] entry ${entry.name} bad marker 0x${marker.toString(16)}`);
    }
    const decompressedSize = dv.getUint32(off + 4, true);
    // packedSize spans the zlib stream + the next record's 8-byte header —
    // slice the TRUE stream length (see BUNT_TRAILING_BYTES above).
    const comp = this.bytes.subarray(off + 8, off + 8 + entry.packedSize - BUNT_TRAILING_BYTES);
    if (entry.packedSize <= BUNT_TRAILING_BYTES) {
      throw new Error(`[BuntArchive] entry ${entry.name} implausible packed size ${entry.packedSize}`);
    }
    const payload = await this.io.inflate(comp);
    if (payload.byteLength !== decompressedSize) {
      throw new Error(
        `[BuntArchive] entry ${entry.name} size mismatch: inflated ${payload.byteLength}, header says ${decompressedSize}`);
    }
    return { payload, entry, decompressedSize };
  }
}
