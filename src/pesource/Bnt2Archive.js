// Bnt2Archive.js — PE MILESTONE 1 ITER 010 (PE_WORLD_SURFACE_FIDELITY_R1, RESUME R4)
// BNT2 archive reader — the framing used by Textures.bnt (EU-runtime corpus,
// 8,095 entries; canon: M3-2-R1 extracted 8,095/8,095 raw payloads 1:1 with
// SHA256, source SHA256 2EAE1159...).
//
// FORMAT (CONFIRMED — pe-bnt-tdf skill + M3-2-R1 extraction code):
//   Footer (last 8 bytes): [uint32 LE dir_offset]['BNT2' magic]
//   Directory @dir_offset: [uint32 LE count][count × entries]
//   Entry: [name bytes, 0x0A-terminated][uint32 LE size][uint32 LE offset]
//                           [uint32 LE crc32][uint32 LE pad]
//   Payload @offset: RAW bytes (NO zlib in Textures.bnt), size = entry size.
//
// Entries are named '<numeric_texture_id>.dat' — the BNT2 texture resource ID
// space (M3-4-R2B CONFIRMED: ArkTexture bytes[5:8] u32 LE = this ID).
// FORMAT KNOWLEDGE LIVES HERE (format layer) — never in the renderer.

export const BNT2_MAGIC = 'BNT2';

export class Bnt2Archive {
  /**
   * @param {Uint8Array} wholeFile raw bytes of the .bnt file
   */
  constructor(wholeFile) {
    this.bytes = wholeFile;
    if (wholeFile.byteLength < 8) throw new Error('[Bnt2Archive] file too small');
    const dv = new DataView(wholeFile.buffer, wholeFile.byteOffset, wholeFile.byteLength);
    const magic = String.fromCharCode(...wholeFile.subarray(wholeFile.byteLength - 4));
    if (magic !== BNT2_MAGIC) {
      throw new Error(`[Bnt2Archive] bad footer magic ${magic} (expected BNT2)`);
    }
    this.dirOffset = dv.getUint32(wholeFile.byteLength - 8, true);
    this.count = dv.getUint32(this.dirOffset, true);
    this._dv = dv;
    this._entries = null;
    this._byName = null;
    this._byId = null;
  }

  entries() {
    if (this._entries) return this._entries;
    const out = [];
    let p = this.dirOffset + 4;
    for (let i = 0; i < this.count; i++) {
      const nameStart = p;
      while (p < this.bytes.length && this.bytes[p] !== 0x0a) p++;
      if (p >= this.bytes.length) throw new Error(`[Bnt2Archive] entry ${i}: unterminated name`);
      const name = String.fromCharCode(...this.bytes.subarray(nameStart, p));
      p++; // skip 0x0A terminator
      const size = this._dv.getUint32(p, true);
      const offset = this._dv.getUint32(p + 4, true);
      const crc32 = this._dv.getUint32(p + 8, true);
      p += 16; // size, offset, crc32, pad
      out.push({ entryIndex: i, name, size, offset, crc32 });
    }
    if (p !== this.bytes.length - 8) {
      throw new Error(
        `[Bnt2Archive] directory end ${p} != footer-8 ${this.bytes.length - 8} (count=${this.count})`);
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

  /** Entry by numeric texture ID — name is '<id>.dat'. */
  entryById(textureId) {
    if (!this._byId) {
      this._byId = new Map();
      for (const e of this.entries()) {
        const m = e.name.match(/^(\d+)\.dat$/i);
        if (m) this._byId.set(parseInt(m[1], 10), e);
      }
    }
    return this._byId.get(textureId) ?? null;
  }

  /**
   * Reads one RAW entry payload (NO decompression — Textures.bnt payloads are
   * stored 1:1; validated against the directory size).
   * @returns {{payload: Uint8Array, entry: object}}
   */
  readEntry(entry) {
    if (entry.offset + entry.size > this.bytes.length) {
      throw new Error(`[Bnt2Archive] entry ${entry.name} beyond EOF`);
    }
    const payload = this.bytes.subarray(entry.offset, entry.offset + entry.size);
    return { payload, entry };
  }
}
