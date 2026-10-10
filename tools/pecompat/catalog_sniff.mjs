// catalog_sniff.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 2 (W2)
// Bounded, header-only payload sniff shared by ark_index.mjs / bnt_index.mjs.
// This is a HEURISTIC CLASSIFICATION from the first bytes ONLY — it is never
// presented as a decode, and UNKNOWN is recorded as UNKNOWN (never zeroed).
//
// Sniff classes:
//   NIF            — ASCII header line matches /^(NetImmerse|Gamebryo) File
//                    Format, Version \d+\.\d+\.\d+\.\d+/ (version captured)
//   DDS            — 'DDS ' magic (0x44 0x44 0x53 0x20)
//   TGA_HEADER     — bytes[0]<=0xFF idlen, bytes[1] in {0,1}, bytes[2] in
//                    {0,1,2,3,9,10,11,32,33}, plausible u16 dims at 12..16
//                    (width/height each in 1..8192) — recorded with dims+bpp
//   OTHER/UNKNOWN  — recorded with first8 hex
//
// Era labels are attached by the CALLER (sniff itself is era-neutral).

export function sniffPayload(bytes) {
  const first8 = Buffer.from(bytes.subarray(0, 8)).toString('hex');
  const rec = { sniffClass: 'UNKNOWN', first8Hex: first8, nifVersion: null, tgaWidth: null, tgaHeight: null, tgaBpp: null, note: null };
  // NIF: ASCII header line
  let ascii = '';
  for (let i = 0; i < Math.min(bytes.length, 80); i++) {
    const c = bytes[i];
    if (c === 0x0a || c === 0x00) break;
    if (c < 0x20 || c > 0x7e) { ascii = null; break; }
    ascii += String.fromCharCode(c);
  }
  if (ascii) {
    const m = ascii.match(/^(NetImmerse|Gamebryo) File Format, Version (\d+)\.(\d+)\.(\d+)\.(\d+)/);
    if (m) {
      rec.sniffClass = 'NIF';
      rec.nifEngine = m[1];
      rec.nifVersion = `${m[2]}.${m[3]}.${m[4]}.${m[5]}`;
      return rec;
    }
  }
  // DDS magic
  if (bytes[0] === 0x44 && bytes[1] === 0x44 && bytes[2] === 0x53 && bytes[3] === 0x20) {
    rec.sniffClass = 'DDS';
    return rec;
  }
  // TGA header plausibility (uncompressed/mapped/RLT variants)
  const imageType = bytes[2];
  const cmapType = bytes[1];
  if (cmapType <= 1 && [0, 1, 2, 3, 9, 10, 11, 32, 33].includes(imageType)) {
    const w = bytes[12] | (bytes[13] << 8);
    const h = bytes[14] | (bytes[15] << 8);
    const bpp = bytes[16];
    if (w >= 1 && w <= 8192 && h >= 1 && h <= 8192 && [8, 15, 16, 24, 32].includes(bpp)) {
      rec.sniffClass = 'TGA_HEADER';
      rec.tgaWidth = w;
      rec.tgaHeight = h;
      rec.tgaBpp = bpp;
      return rec;
    }
  }
  rec.sniffClass = 'OTHER';
  rec.note = 'no NIF/DDS/TGA header pattern in first bytes — NOT decoded in this phase';
  return rec;
}
