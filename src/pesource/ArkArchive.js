// ArkArchive.js — PE MILESTONE 1 ITER 010 (PE_WORLD_SURFACE_FIDELITY_R1, RESUME R4)
// ArkVFS (.ark) archive reader — the Jan-2003 CD installer container framing
// (Textures.ark, canon 4,833 entries; pe-ark-vfs skill F-111: standard ZIP
// layout, only the magic differs: AK vs PK; all entries STORED, no encryption).
//
// FORMAT (CONFIRMED — pe-ark-vfs skill, 7-Zip + QuickBMS cross-verified):
//   Local header: 'AK\x03\x04' + [u16 ver][u16 flags][u16 comp][u16 time]
//                 [u16 date][u32 crc32][u32 comp_size][u32 uncomp_size]
//                 [u16 name_len][u16 extra_len][name][extra][data...]
//   EOCD: 'AK\x05\x06' [u32 disk_num quirk][u16 entries_disk][u16 total]
//         [u32 cd_size][u32 cd_offset][u16 comment_len]
//   Sequential local-header scan is the reliable index (central directory
//   not fully RE'd); EOCD totals cross-check the scan count.
//
// Entry names are '<numeric_texture_id>.<ext>' (case-mixed .tga/.DDS) — the
// same numeric texture-ID space as BNT2 (era comparison is per-ID).
// FORMAT KNOWLEDGE LIVES HERE (format layer) — never in the renderer.

export const ARK_LOCAL_MAGIC = 'AK\x03\x04';
export const ARK_EOCD_MAGIC = 'AK\x05\x06';

export class ArkArchive {
  constructor(wholeFile) {
    this.bytes = wholeFile;
    if (wholeFile.byteLength < 22) throw new Error('[ArkArchive] file too small');
    const dv = new DataView(wholeFile.buffer, wholeFile.byteOffset, wholeFile.byteLength);
    this._dv = dv;
    // EOCD scan (last 22 bytes + slack)
    let eocd = -1;
    const scanFloor = Math.max(0, wholeFile.byteLength - 22 - 65536);
    for (let i = wholeFile.byteLength - 22; i >= scanFloor; i--) {
      if (wholeFile[i] === 0x41 && wholeFile[i + 1] === 0x4b &&
          wholeFile[i + 2] === 0x05 && wholeFile[i + 3] === 0x06) { eocd = i; break; }
    }
    if (eocd < 0) throw new Error('[ArkArchive] EOCD AK\\x05\\x06 not found');
    this.eocdOffset = eocd;
    this.eocdDiskNum = dv.getUint32(eocd + 4, true); // u32 quirk (ZIP: u16)
    this.eocdEntriesDisk = dv.getUint16(eocd + 8, true);
    this.eocdTotalEntries = dv.getUint16(eocd + 10, true);
    this.eocdCdSize = dv.getUint32(eocd + 12, true);
    this.eocdCdOffset = dv.getUint32(eocd + 16, true);
    this._entries = null;
    this._byId = null;
  }

  entries() {
    if (this._entries) return this._entries;
    const out = [];
    let pos = 0;
    const b = this.bytes;
    while (pos + 4 <= b.length) {
      if (!(b[pos] === 0x41 && b[pos + 1] === 0x4b && b[pos + 2] === 0x03 && b[pos + 3] === 0x04)) break;
      const flags = this._dv.getUint16(pos + 6, true);
      const compression = this._dv.getUint16(pos + 8, true);
      const crc32 = this._dv.getUint32(pos + 14, true);
      const compSize = this._dv.getUint32(pos + 18, true);
      const uncompSize = this._dv.getUint32(pos + 22, true);
      const nameLen = this._dv.getUint16(pos + 26, true);
      const extraLen = this._dv.getUint16(pos + 28, true);
      const name = String.fromCharCode(...b.subarray(pos + 30, pos + 30 + nameLen));
      const dataOffset = pos + 30 + nameLen + extraLen;
      out.push({ entryIndex: out.length, name, size: uncompSize, compSize, compression, flags, crc32, dataOffset });
      pos = dataOffset + compSize;
    }
    if (this.eocdTotalEntries !== out.length) {
      throw new Error(
        `[ArkArchive] EOCD total ${this.eocdTotalEntries} != local scan ${out.length}`);
    }
    this._entries = out;
    return out;
  }

  entryByName(name) {
    const lower = name.toLowerCase();
    for (const e of this.entries()) if (e.name.toLowerCase() === lower) return e;
    return null;
  }

  /** Entry by numeric texture ID — name is '<id>.<ext>' (case-mixed). */
  entryById(textureId) {
    if (!this._byId) {
      this._byId = new Map();
      for (const e of this.entries()) {
        const m = e.name.match(/^(\d+)\.[^.]+$/i);
        if (m) {
          const id = parseInt(m[1], 10);
          if (!this._byId.has(id)) this._byId.set(id, e);
        }
      }
    }
    return this._byId.get(textureId) ?? null;
  }

  /**
   * Reads one STORED entry payload (compression must be 0 — no silent decode
   * of an unexpected compression; fail loudly instead).
   * @returns {{payload: Uint8Array, entry: object}}
   */
  readEntry(entry) {
    if (entry.compression !== 0) {
      throw new Error(`[ArkArchive] entry ${entry.name} compression=${entry.compression} (STORED expected — refusing)`);
    }
    if (entry.compSize !== entry.size) {
      throw new Error(`[ArkArchive] entry ${entry.name} compSize ${entry.compSize} != uncompSize ${entry.size}`);
    }
    if (entry.dataOffset + entry.size > this.bytes.length) {
      throw new Error(`[ArkArchive] entry ${entry.name} beyond EOF`);
    }
    const payload = this.bytes.subarray(entry.dataOffset, entry.dataOffset + entry.size);
    return { payload, entry };
  }
}
