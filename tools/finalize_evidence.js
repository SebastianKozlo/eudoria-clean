// finalize_evidence.js — consolidates era-validation parts into the final evidence artifacts
'use strict';
const fs = require('fs');
const crypto = require('crypto');
function sha256File(p) { return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex').toUpperCase(); }

const EVID = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_MILESTONE_1_WORLD_SURFACE_R1\\03_EVIDENCE';
const tools = __dirname;

const p1 = JSON.parse(fs.readFileSync(tools + '\\era_validation_partial.json'));
const p2 = JSON.parse(fs.readFileSync(tools + '\\era_validation_partial2.json'));
const p3 = JSON.parse(fs.readFileSync(tools + '\\era_validation_partial3.json'));

const final = {
  iter: '019',
  phase: 'M1-E CLEAN_RUNTIME_FOUNDATION START R2 — DECODER ERA-VALIDATION',
  created: new Date().toISOString(),
  purpose: 'Validate BuntArchive/Bnt2Archive/TdfDecoder reuse against pcg_9_3_5 terrain.bnt BEFORE the clean pipeline touches it (NEXT_PROMPT section 2; ledger ENTRY #3 decoder versioning rule).',
  sources: p1.sources,
  verdict: 'PASS — decoders reusable with ONE era-versioned archive reader. terrain.bnt 9.3.5 is BNT2-footer framed (not BUNT), but the TDF payload semantics are byte-compatible with the JUL corpus.',
  divergence_table: p1.field_by_field_vs_50bnt,
  terrain_935_index: p1.terrain_935,
  jul_50bnt_index: p1.jul_50bnt,
  record_framing_samples: p1.record_framing_samples,
  tdf_shape: p1.tdf_shape,
  size_semantics: {
    contiguity: 'records are contiguous [offset, offset+size) across the regular region (21 breaks only at special-row region boundaries); size = 8-byte record header (02 00 00 FF + u32 decompressedSize) + zlib stream',
    strict_size_minus_8_inflation: p2.strict_size_minus_8_inflation,
    trailing_8_quirk_vs_jul: 'EQUIVALENT SEMANTICS: in both eras the index size field counts the 8-byte record header in addition to the zlib stream; the existing slice(off+8, off+8+size-8) = exact stream. iter005i BUNT_TRAILING_BYTES=8 fact HOLDS for 9.3.5 (strict 25/25 sample inflation, zero failures).',
  },
  grid: p2.grid,
  grid_refined: p3.tile_classification,
  tdf_payload_semantics: {
    standard_header_check_200: p3.standard_header_check_200,
    sentinel: p3.sentinel,
    heights: 'u16 LE at payload 64..2111, 32x32 — same as JUL (sampled range 0..26842 over 20 random regular tiles; header data_size=2100 @8, dim=32 @12 on 200/200 sampled regular tiles)',
  },
  material_tail: {
    jul_reference: 'iter008 winning walk: [u32 size][u32 dim][body]; stride = size+4; mask RAW u8 when len==dim*dim else RLE (count,value); CONFIRMED 51920/51920 on 50.bnt',
    pcg_935_full_walk: p3.record_walk_full,
    pcg_935_sample_walk_details: p3.sample_walk_details,
    result: 'CONFIRMED for era PCG_9_3_5: identical stride=size+4 record semantics consume every tail byte EXACTLY on 51920/51920 regular tiles (448,384 records, 0 failures). Record size family matches JUL (308/1076/56/84/564...). Inline material names (Stone04, Grass01, Rock03, ...) with 10,150 distinct names.',
    distinct_material_names_artifact: 'iter019_era_validation_material_names.json',
  },
  special_tiles: {
    count: 6530,
    classification: 'entries outside the regular 220x236 grid and the sentinel: y rows 65370..65535 (0xff1a..0xffff), all x within 0..219 — skirt/special rows. NOT part of regular terrain rendering; excluded from P0 scope this session; semantics UNRESOLVED (explicit label, no approximation).',
  },
  decoder_versioning_decision: {
    rule: 'ledger ENTRY #3: version the decoder rather than mutating the legacy path silently',
    action: 'eudoria-clean gets a NEW era-versioned archive reader (Bnt2TerrainArchive, era=PCG_9_3_5): BNT2 directory walk (variable 0x0A-terminated names + size/offset/crc32/pad) + BNT record framing (02 00 00 FF + u32 decompressedSize + zlib, stream = size-8). The legacy BuntArchive (JUL BUNT path) is REUSED AS-IS and never fed terrain.bnt. TdfDecoder semantics (offset 64 heights, stride=size+4 tail walk) REUSED UNCHANGED — validated above.',
  },
  scripts: [
    { path: 'eudoria-clean/tools/era_probe.js', sha256: sha256File(tools + '\\era_probe.js') },
    { path: 'eudoria-clean/tools/era_validation.js', sha256: sha256File(tools + '\\era_validation.js') },
    { path: 'eudoria-clean/tools/era_validation_2.js', sha256: sha256File(tools + '\\era_validation_2.js') },
    { path: 'eudoria-clean/tools/era_validation_3.js', sha256: sha256File(tools + '\\era_validation_3.js') },
  ],
  hard_stop_check: 'NOT TRIGGERED: terrain.bnt 9.3.5 parses without breaking the JUL path (separate era-versioned reader; legacy path untouched).',
};
fs.writeFileSync(EVID + '\\iter019_era_validation_terrain_bnt.json', JSON.stringify(final, null, 2));
console.log('final evidence written:', EVID + '\\iter019_era_validation_terrain_bnt.json');

// also write the material-names artifact into EVID
const names = fs.readFileSync(tools + '\\era_validation_material_names.json');
fs.writeFileSync(EVID + '\\iter019_era_validation_material_names.json', names);
console.log('material names artifact written');
console.log('verdict:', final.verdict);
