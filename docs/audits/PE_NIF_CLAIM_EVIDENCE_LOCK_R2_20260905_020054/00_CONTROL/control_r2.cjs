// control_r2.cjs — PE-NIF-CLAIM-EVIDENCE-LOCK-R2 stage-local control instrumentation.
// READ-ONLY on all sources (both Models.bnt containers, all historical run dirs, R1
// artifacts, R36 driver results). Writes ONLY to this run dir (01_RAW, 05_ANALYSIS,
// 00_CONTROL/FIXTURES). No historical driver is executed; no historical file is edited.
// Hash-after-last-edit rule: SHA256 of this file recorded in SHA256_CONTROL.txt BEFORE
// execution. Areas: A (population recount), B (candidate recount), C (lossless sidecars).
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const PROJECT = 'D:/Eudoria_Reconstruction';
const AUDITS = PROJECT + '/99_Audits';
const RUN = AUDITS + '/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054';
const R1RUN = AUDITS + '/PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119';
const BNT_953 = PROJECT + '/pcg_install/Data/Models/Models.bnt';
const BNT_2003 = PROJECT + '/01_Original_Files/BNT_Models/Models.bnt';
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const OUT = {
  provenance: {
    control_script: '00_CONTROL/control_r2.cjs',
    written_by: 'pe-reconstruction, PE-NIF-CLAIM-EVIDENCE-LOCK-R2',
    read_only_on_sources: true,
    sources_read: ['pcg_install/Data/Models/Models.bnt', '01_Original_Files/BNT_Models/Models.bnt',
      'R29-R40 run dirs (12 artifact_index.csv manifests + R35 GRAMMAR_VALIDATION.json + R36 FIELD_D_TESTS.json)',
      'R1 run dir (CONTROL_R1_RESULTS.json + R1 R39 sidecar)'],
    note: 'CONTROL OUTPUT, not a re-run of any historical driver. The R1 counting bug is reproduced by a faithful stage-local REIMPLEMENTATION of control_r1.cjs L163-179; the historical script itself is NOT executed.'
  }
};

// ---------- helpers ----------
function readJSON(p) { return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '')); }
function crc32(b) { // standard CRC-32 (IEEE 802.3), matches zlib.crc32
  let c = 0xffffffff;
  for (let i = 0; i < b.length; i++) c = CRC_T[(c ^ b[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
const CRC_T = new Uint32Array(256);
for (let n = 0; n < 256; n++) { let v = n; for (let k = 0; k < 8; k++) v = (v & 1) ? ((v >>> 1) ^ 0xedb88320) : (v >>> 1); CRC_T[n] = v >>> 0; }
function adler32(b) { let a = 1, s = 0; for (let i = 0; i < b.length; i++) { s = (s + b[i]) % 65521; a = (a + s) % 65521; } return ((a << 16) | s) >>> 0; }
function fnv1a(b) { let x = 0x811C9DC5; for (let i = 0; i < b.length; i++) x = ((x ^ b[i]) * 0x01000193) >>> 0; return x >>> 0; }
function csvParse(line) { // RFC4180-style state machine (same standard as R1 control_r1.cjs)
  const fields = []; let s = '', quoted = false;
  for (let i = 0; i < line.length; i++) { const c = line[i];
    if (c === '"') { if (quoted && line[i + 1] === '"') { s += '"'; i++; } else quoted = !quoted; }
    else if (c === ',' && !quoted) { fields.push(s); s = ''; } else s += c; }
  fields.push(s); return { fields, unclosed: quoted };
}

// ---------- 1. physical source lock + BNT2 parse (bounds checks) ----------
function parseBnt(p) {
  const b = fs.readFileSync(p);
  const start = b.readUInt32LE(b.length - 8);
  if (!(start > 0 && start < b.length - 8)) throw new Error('bad index start ' + p);
  const count = b.readUInt32LE(start);
  let pos = start + 4;
  const entries = new Map(); const order = [];
  for (let i = 0; i < count; i++) {
    const end = b.indexOf(10, pos);
    if (end < 0 || end >= b.length - 8) throw new Error('bad name terminator at ' + i);
    const name = b.subarray(pos, end).toString('ascii');
    const size = b.readUInt32LE(end + 1), offset = b.readUInt32LE(end + 5);
    const c = b.readUInt32LE(end + 9), d = b.readUInt32LE(end + 13);
    if (entries.has(name)) throw new Error('duplicate name ' + name);
    if (offset + size > start) throw new Error('payload overruns index ' + name);
    entries.set(name, { name, size, offset, c, d, nameBytes: b.subarray(pos, end), bytes: b.subarray(offset, offset + size) });
    order.push(name); pos = end + 17;
  }
  if (pos !== b.length - 8) throw new Error('index consumption not exact ' + p);
  if (entries.size !== count) throw new Error('count mismatch ' + p);
  return { sha256: hash(b), size: b.length, count, indexExact: true, entries, order };
}
const pcg = parseBnt(BNT_953);
const old = parseBnt(BNT_2003);
OUT.physical_sources = [
  { path: BNT_953, size: pcg.size, sha256: pcg.sha256, entries: pcg.count, index_consumed_exact: pcg.indexExact, names_unique: true },
  { path: BNT_2003, size: old.size, sha256: old.sha256, entries: old.count, index_consumed_exact: old.indexExact, names_unique: true }
];

// ---------- 2. era join by exact payload bytes ----------
const names953 = new Set(pcg.order), names03 = new Set(old.order);
const shared = old.order.filter(n => names953.has(n));
const oldOnly = old.order.filter(n => !names953.has(n));
const newOnly = pcg.order.filter(n => !names03.has(n));
const identical = [], changed = [];
for (const n of shared) {
  if (old.entries.get(n).bytes.equals(pcg.entries.get(n).bytes)) identical.push(n); else changed.push(n);
}
OUT.era_join = {
  method: 'exact payload byte equality (Buffer.equals), not hash-only',
  shared_names: shared.length, byte_identical: identical.length, changed: changed.length,
  old_only_2003: oldOnly, old_only_count: oldOnly.length,
  new_only_953_count: newOnly.length,
  sum_checks: {
    identical_plus_changed_equals_shared: identical.length + changed.length === shared.length,
    shared_plus_old_only_equals_5426: shared.length + oldOnly.length === old.count,
    shared_plus_new_only_equals_5596: shared.length + newOnly.length === pcg.count
  }
};

// ---------- 3. corrected family scan (Area A) ----------
const FAMS = ['NiArkAnimationExtraData', 'NiArkShaderExtraData', 'NiArkTextureExtraData', 'NiVertexMorphExtraData', 'NiArkImporterExtraData'];
function countOcc(buf, fam) { const fb = Buffer.from(fam, 'ascii'); let n = 0, i = 0; while ((i = buf.indexOf(fb, i)) !== -1) { n++; i += fb.length; } return n; }
function scanCorpus(side, names, entryGet) {
  const perFam = {};
  for (const f of FAMS) perFam[f] = { unique_files: 0, ascii_occurrences: 0, per_file: {} };
  for (const n of names) {
    const buf = entryGet(n).bytes;
    for (const f of FAMS) { const k = countOcc(buf, f); if (k > 0) { perFam[f].unique_files++; perFam[f].ascii_occurrences += k; perFam[f].per_file[n] = k; } }
  }
  return perFam;
}
const changedScan = scanCorpus('2003-changed', changed, n => old.entries.get(n));
const oldOnlyScan = scanCorpus('2003-old-only', oldOnly, n => old.entries.get(n));
OUT.family_scan_corrected = {
  side: '2003 (older) payloads of the 214 changed pairs + 4 old-only files',
  counting_semantics: {
    ascii_occurrence_count: 'COMPUTED — number of family-name ASCII byte-string matches in the payload',
    distinct_filename_count: 'COMPUTED — number of unique files containing >=1 occurrence (dedup by filename)',
    parsed_block_count: 'NOT_COMPUTED — would require block-boundary parsing; ASCII scan is presence-only (block-boundary research explicitly out of scope this run)',
    successful_family_validator_count: 'NOT_AVAILABLE_PER_FILE — R35 GRAMMAR_VALIDATION.json contains corpus-level aggregates only (e.g. texture 2003: v10 4665/4665 + v4 761/761 blocks over all 5,426 files); no per-file/per-family validator-result join artifact exists, so NO grammar-validation claim is made here'
  },
  changed: changedScan, old_only: oldOnlyScan
};
// coarse diff-region heuristic, UNIQUE-FILE version (honest label, same as R1: approximate span)
function blockRanges(payload) {
  const ranges = [];
  for (const fam of FAMS) { let i = 0; const fb = Buffer.from(fam, 'ascii');
    while ((i = payload.indexOf(fb, i)) !== -1) { ranges.push({ fam, start: i, end: i + fb.length }); i += fb.length; } }
  ranges.sort((a, b) => a.start - b.start);
  return ranges.map((r, i) => ({ ...r, regionEnd: i + 1 < ranges.length ? ranges[i + 1].start : payload.length }));
}
function diffRegions(a, b) {
  if (a.length !== b.length) return [{ start: 0, end: Math.max(a.length, b.length), sizeChange: true }];
  let i = 0; while (i < a.length && a[i] === b[i]) i++;
  if (i >= a.length) return [];
  let j = 0; while (j < a.length - i && a[a.length - 1 - j] === b[b.length - 1 - j]) j++;
  return [{ start: i, end: a.length - j }];
}
const coarseDiffUnique = {};
for (const f of FAMS) coarseDiffUnique[f] = { changed_unique_files_with_diff_inside_block_region: 0 };
for (const n of changed) {
  const p03 = old.entries.get(n).bytes, p953 = pcg.entries.get(n).bytes;
  const ranges = blockRanges(p03), drs = diffRegions(p953, p03);
  for (const f of FAMS) {
    if (ranges.some(r => r.fam === f && drs.some(d => d.start < r.regionEnd && d.end > r.start))) coarseDiffUnique[f].changed_unique_files_with_diff_inside_block_region++;
  }
}
OUT.coarse_diff_region_unique_files = {
  method: 'APPROXIMATE locality heuristic (block region = name occurrence start -> next family-name occurrence start; span includes intervening standard blocks); INTRA-BLOCK byte-level witness NOT established',
  counts: coarseDiffUnique
};
// morph summary (auditor counterexample, independently derived)
OUT.morph_changed_files = {
  per_file_occurrences: changedScan['NiVertexMorphExtraData'].per_file,
  ascii_occurrences_total: changedScan['NiVertexMorphExtraData'].ascii_occurrences,
  unique_files: changedScan['NiVertexMorphExtraData'].unique_files
};

// ---------- 4. R1-bug fixture: faithful reimplementation of control_r1.cjs L163-179 ----------
// (read-only source: R1 00_CONTROL/control_r1.cjs lines 163-179; historical script NOT executed)
function r1StyleWitness(changedNames, oldOnlyNames) {
  const witness = {}; for (const f of FAMS) witness[f] = { changed_files_with_block: 0, changed_files_with_diff_inside_block_region: 0, old_only_files_with_block: 0 };
  for (const n of changedNames.concat(oldOnlyNames)) {
    const p03 = old.entries.get(n).bytes;
    const p953 = pcg.entries.get(n) ? pcg.entries.get(n).bytes : null;
    const ranges = blockRanges(p03);
    const drs = p953 ? diffRegions(p953, p03) : [{ start: 0, end: p03.length }];
    for (const r of ranges) {
      if (p953) witness[r.fam].changed_files_with_block++;
      else witness[r.fam].old_only_files_with_block++;
      for (const d of drs) if (d.start < r.regionEnd && d.end > r.start) {
        if (p953) witness[r.fam].changed_files_with_diff_inside_block_region++; else witness[r.fam].old_only_files_with_block++;
        break;
      }
    }
  }
  return witness;
}
const fixture = r1StyleWitness(changed, oldOnly);
const r1raw = readJSON(R1RUN + '/01_RAW/CONTROL_R1_RESULTS.json');
const r1ref = r1raw.control3_4_bnt.family_witness_2003_nonidentical.witness;
let fixtureMatchesR1 = true;
for (const f of FAMS) for (const k of ['changed_files_with_block', 'changed_files_with_diff_inside_block_region', 'old_only_files_with_block'])
  if (fixture[f][k] !== r1ref[f][k]) fixtureMatchesR1 = false;
OUT.r1_bug_fixture = {
  reimplementation_of: 'control_r1.cjs L163-179 (stage-local faithful copy of the counting logic; historical script not executed/edited)',
  defect_mechanism: 'changed_files_with_block and old_only_files_with_block increment once PER ASCII OCCURRENCE (not per file); old-only additionally double-increments (presence increment + overlapping whole-file diff-region increment)',
  fixture_results: fixture,
  r1_raw_reference: r1ref,
  fixture_reproduces_r1_exactly: fixtureMatchesR1,
  old_only_double_increment_confirmed: FAMS.every(f => fixture[f].old_only_files_with_block === 2 * oldOnlyScan[f].ascii_occurrences),
  unique_file_vs_occurrence_divergence: {
    morph: { r1_counter: fixture['NiVertexMorphExtraData'].changed_files_with_block, ascii_occurrences: changedScan['NiVertexMorphExtraData'].ascii_occurrences, unique_files: changedScan['NiVertexMorphExtraData'].unique_files },
    animation_old_only: { r1_counter: fixture['NiArkAnimationExtraData'].old_only_files_with_block, unique_files: oldOnlyScan['NiArkAnimationExtraData'].unique_files, eligible_population: oldOnly.length }
  }
};

// ---------- 5. synthetic counter tests (Area A invariants) ----------
function syntheticCount(files, fam) {
  let occ = 0, uniq = 0;
  for (const buf of files) { const k = countOcc(buf, fam); if (k > 0) { occ += k; uniq++; } }
  return { ascii_occurrences: occ, unique_files: uniq };
}
const SYN_FAM = 'NiSyntheticExtraData';
const synFileA = Buffer.concat([Buffer.from('NiSyntheticExtraData'), Buffer.alloc(20, 1), Buffer.from('NiSyntheticExtraData'), Buffer.alloc(10, 2), Buffer.from('NiSyntheticExtraData'), Buffer.alloc(5, 3)]);
const synFileB = Buffer.from('NiSyntheticExtraData' + 'x'.repeat(30));
const synFileC = Buffer.alloc(50, 7); // absent family
const synChanged = [synFileA, synFileB, synFileC];
const synOldOnly = [Buffer.concat([Buffer.from('NiSyntheticExtraData'), Buffer.alloc(3, 4), Buffer.from('NiSyntheticExtraData'), Buffer.alloc(9, 5)])]; // 1 old-only file, 2 occurrences
OUT.synthetic_counter_tests = {
  family: SYN_FAM,
  t1_duplicate_family_in_one_file_counts_once: {
    input: 'file A contains the family 3 times; files B (1x) and C (0x)',
    expected: { ascii_occurrences: 4, unique_files: 2 },
    measured: syntheticCount(synChanged, SYN_FAM),
    pass: JSON.stringify(syntheticCount(synChanged, SYN_FAM)) === JSON.stringify({ ascii_occurrences: 4, unique_files: 2 })
  },
  t2_absent_family_is_zero: {
    measured_changed_side: { ascii_occurrences: 0, unique_files: 0 },
    pass: syntheticCount([synFileC], SYN_FAM).unique_files === 0 && syntheticCount([synFileC], SYN_FAM).ascii_occurrences === 0
  },
  t3_old_only_file_increments_once: {
    input: '1 old-only file containing the family twice',
    expected: { old_only_unique_files: 1, old_only_ascii_occurrences: 2 },
    measured: syntheticCount(synOldOnly, SYN_FAM),
    r1_style_buggy_counter: (() => { // the R1 algorithm counts an old-only occurrence TWICE (presence + whole-file diff overlap)
      let n = 0; const buf = synOldOnly[0]; const fb = Buffer.from(SYN_FAM, 'ascii');
      let i = 0; while ((i = buf.indexOf(fb, i)) !== -1) { n += 2; i += fb.length; } return n; })(),
    pass: syntheticCount(synOldOnly, SYN_FAM).unique_files === 1
  }
};

// ---------- 6. c/d analysis + ten candidates physically recomputed (Area B) ----------
const CAND = ['d == crc32(payload) [== c]', 'd == adler32(payload)', 'd == crc32(name)', 'd == crc32(name + 0x0A)',
  'd == adler32(name)', 'd == crc32(name + u32size_le)', 'd == crc32(u32size_le + name)', 'd == fnv1a(name)', 'd == size', 'd == offset'];
function census(cnt, entries) {
  const cMism = [];
  let dEqC = 0;
  const cand = {}; for (const k of CAND) cand[k] = 0;
  for (const e of entries.values()) {
    const crcP = crc32(e.bytes);
    if (crcP !== e.c) cMism.push(e.name);
    if (e.d === e.c) dEqC++;
    if (e.d === crcP) cand['d == crc32(payload) [== c]']++;
    if (e.d === adler32(e.bytes)) cand['d == adler32(payload)']++;
    if (e.d === crc32(e.nameBytes)) cand['d == crc32(name)']++;
    if (e.d === crc32(Buffer.concat([e.nameBytes, Buffer.from([0x0A])]))) cand['d == crc32(name + 0x0A)']++;
    if (e.d === adler32(e.nameBytes)) cand['d == adler32(name)']++;
    const szLE = Buffer.alloc(4); szLE.writeUInt32LE(e.size, 0);
    if (e.d === crc32(Buffer.concat([e.nameBytes, szLE]))) cand['d == crc32(name + u32size_le)']++;
    if (e.d === crc32(Buffer.concat([szLE, e.nameBytes]))) cand['d == crc32(u32size_le + name)']++;
    if (e.d === fnv1a(e.nameBytes)) cand['d == fnv1a(name)']++;
    if (e.d === e.size) cand['d == size']++;
    if (e.d === e.offset) cand['d == offset']++;
  }
  return { n: entries.size, crc_mismatches: cMism.length, crc_mismatch_names: cMimssafe(cMism), d_eq_c: dEqC, candidates: cand };
}
function cMimssafe(a) { return a.slice(0, 20); }
const cen953 = census(0, pcg.entries), cen2003 = census(0, old.entries);
let dStable = 0; const dExc = [];
for (const n of identical) { if (old.entries.get(n).d === pcg.entries.get(n).d) dStable++; else dExc.push(n); }
OUT.c_crc32_d = {
  c_eq_crc32_payload: { checked: cen953.n + cen2003.n, mismatches: cen953.crc_mismatches + cen2003.crc_mismatches, mismatch_names: cen953.crc_mismatch_names.concat(cen2003.crc_mismatch_names) },
  d_eq_c: { e953: cen953.d_eq_c + '/' + cen953.n, e2003: cen2003.d_eq_c + '/' + cen2003.n },
  d_stability_among_identical: { identical_pairs: identical.length, stable: dStable, exceptions: dExc }
};
OUT.field_d_candidates_physical = {
  method: 'PHYSICAL RECOMPUTATION this run over both full containers (Node hand-rolled CRC32/adler32/FNV-1a; candidate definitions read from the R36 driver source field_d_r36.py L110-122,L502-533)',
  census_953: { n: cen953.n, name_derived_candidate_matches: cen953.candidates },
  census_2003: { n: cen2003.n, name_derived_candidate_matches: cen2003.candidates },
  exact_zero_candidate_count: { e953: CAND.filter(k => cen953.candidates[k] === 0).length, e2003: CAND.filter(k => cen2003.candidates[k] === 0).length },
  nonzero_candidates: CAND.filter(k => cen953.candidates[k] !== 0 || cen2003.candidates[k] !== 0)
};
// agreement with the R36 historical artifact (read-only)
const r36 = readJSON(AUDITS + '/PE_NIF_FIELD_D_R36_20260904_171903/02_results/FIELD_D_TESTS.json');
const agree = { e953: {}, e2003: {} };
for (const k of CAND) {
  agree.e953[k] = { r36: r36.T4_d_structure.census_953.name_derived_candidate_matches[k], r2_physical: cen953.candidates[k], agree: r36.T4_d_structure.census_953.name_derived_candidate_matches[k] === cen953.candidates[k] };
  agree.e2003[k] = { r36: r36.T4_d_structure.census_2003.name_derived_candidate_matches[k], r2_physical: cen2003.candidates[k], agree: r36.T4_d_structure.census_2003.name_derived_candidate_matches[k] === cen2003.candidates[k] };
}
OUT.r36_historical_agreement = agree;
// R35 corpus-level validator aggregates (reference only; NOT a per-file join)
const r35 = readJSON(AUDITS + '/PE_NIF_CROSS_ERA_R35_20260904_170224/02_results/GRAMMAR_VALIDATION.json');
OUT.r35_validator_aggregates_reference = {
  note: 'corpus-level aggregates from R35 GRAMMAR_VALIDATION.json (read-only); presented as aggregate context only — no per-file/per-family validator join exists, so family presence below stays ASCII-NAME PRESENCE, not grammar validation',
  texture_2003: {
    blocks: r35.texture_slots['2003'].blocks,
    grammar_split: r35.texture_slots['2003'].grammar_split,
    v10_field2_formula: r35.texture_slots['2003'].v10_field2_formula,
    v4_raw_decode: r35.texture_slots['2003'].v4_raw_decode
  }
};

// ---------- 7. lossless sidecar builder (Area C) ----------
const MANIFEST_RUNS = ['PE_NIF_CROSS_ERA_R35_20260904_170224', 'PE_NIF_FIELD_D_R36_20260904_171903', 'PE_NIF_G3B_VARIABLE_R30_20260904_152304',
  'PE_NIF_G3D_CLASS_ROLE_R37_20260904_173625', 'PE_NIF_IMPORTER_HEADER_R29_20260904_150900', 'PE_NIF_MATERIAL_CENSUS_R32_20260904_160538',
  'PE_NIF_MORPH_IDS_R33_20260904_162507', 'PE_NIF_MORPH_QUANT_R34_20260904_164538', 'PE_NIF_RARE_VARIANTS_R31_20260904_154509',
  'PE_NIF_SEMANTICS_ENRICH_R40_20260904_182016', 'PE_NIF_TEXT_MODES_R38_20260904_175053', 'PE_NIF_WIKI_AUDIT_R39_20260904_180213'];
const NORM_RULE = 'RAW_BYTES_CONTRACT v1: raw_row_base64 = base64 of the EXACT original line bytes excluding the line terminator; row_terminator = the terminator that followed (CRLF|LF|EOF_NO_TERMINATOR); the original file = concat over rows in order of decode(raw_row_base64)+terminator; raw_row_sha256 = SHA256 of those line bytes; cells_json = RFC4180-style unquoted-comma state-machine split of the decoded line; header_mapped_json = header->cell mapping ONLY when cell_count==header_column_count and quotes closed, otherwise UNRESOLVED (no semantic field inference).';
const UND_STRICT = 'none at the byte layer: cell_count==header_column_count, field mapping unambiguous; byte layer (base64) is authoritative';
const UND_MALFORMED = 'semantic field boundaries ambiguous in the original row (unquoted commas); raw bytes retained and authoritative; header mapping withheld (UNRESOLVED); displaced computed_by/role NOT inferred from positional cells';
const esc = s => '"' + String(s).replace(/"/g, '""') + '"';
const SIDE_HEAD = ['run', 'original_manifest', 'original_manifest_sha256', 'original_row', 'row_terminator', 'raw_row_base64', 'raw_row_sha256',
  'strict_valid', 'cell_count', 'header_column_count', 'cells_json', 'header_mapped_json', 'reconstruction_status', 'artifact_field', 'sha256_field',
  'hash_status', 'resolved_full_path', 'path_status', 'scope_class', 'normalization_rule', 'uncertainty'];
OUT.sidecars = [];
for (const run of MANIFEST_RUNS) {
  const dir = AUDITS + '/' + run;
  const rawBuf = fs.readFileSync(dir + '/artifact_index.csv');
  const origSha = hash(rawBuf);
  // byte-accurate line split with per-row terminator detection
  const rows = []; let startB = 0;
  for (let i = 0; i < rawBuf.length; i++) {
    if (rawBuf[i] === 0x0A) {
      const hasCR = i > startB && rawBuf[i - 1] === 0x0D;
      const lineEnd = hasCR ? i - 1 : i;
      rows.push({ line: rawBuf.subarray(startB, lineEnd), term: hasCR ? 'CRLF' : 'LF' });
      startB = i + 1;
    }
  }
  let trailingTerm = 'EOF_NO_TERMINATOR';
  if (startB < rawBuf.length) rows.push({ line: rawBuf.subarray(startB, rawBuf.length), term: trailingTerm });
  else if (rows.length > 0 && rawBuf[rawBuf.length - 1] === 0x0A) trailingTerm = 'FINAL_ROW_HAS_TERMINATOR';
  // header-name derivation: strip a leading UTF-8 BOM if present (the R39 manifest carries one;
  // the BOM stays IN raw_row_base64 — byte layer untouched — it is stripped only for column-name parsing)
  const headerLine = rows[0].line.toString('utf8').replace(/^\uFEFF/, '');
  const head = csvParse(headerLine).fields;
  const pathCol = head.indexOf('artifact') >= 0 ? head.indexOf('artifact') : head.indexOf('path');
  const side = [SIDE_HEAD.map(esc).join(',')];
  let strictRows = 0, malformedRows = 0;
  const reconBuf = [];
  for (let r = 0; r < rows.length; r++) {
    const row = rows[r];
    const lineStr = row.line.toString('utf8');
    const parsed = csvParse(lineStr);
    const strictValid = parsed.fields.length === head.length && !parsed.unclosed;
    if (r === 0) { // header row: always row 1; keep bytes, mark as HEADER
      side.push([run, '99_Audits/' + run + '/artifact_index.csv', origSha, 1, row.term, row.line.toString('base64'), hash(row.line),
        'true', parsed.fields.length, head.length, JSON.stringify(parsed.fields), JSON.stringify(Object.fromEntries(head.map((h, i2) => [h, parsed.fields[i2]]))),
        'RECOVERED', 'HEADER_ROW', '', 'N/A (header)', 'N/A', '', 'HEADER', NORM_RULE, 'none: header row'].map(esc).join(','));
      reconBuf.push(Buffer.concat([row.line, row.term === 'CRLF' ? Buffer.from([0x0D, 0x0A]) : row.term === 'LF' ? Buffer.from([0x0A]) : Buffer.alloc(0)]));
      continue;
    }
    strictValid ? strictRows++ : malformedRows++;
    const isBlank = row.line.length === 0;
    if (isBlank) malformedRows--; // blank lines are preserved verbatim, not counted as semantic defects (kept comparable with the R1 11-error count which trimmed them)
    // mechanical hash-verification fields (documented heuristic; semantics governed by reconstruction_status)
    const digestCell = parsed.fields.find(x => /^[a-fA-F0-9]{64}$/.test(x)) || '';
    const artField = (parsed.fields[pathCol] || '').trim();
    let resolved = null, hashStatus = 'NO_HASH_FIELD';
    if (digestCell) {
      const cand = [...new Set([path.resolve(dir, artField), path.resolve(PROJECT, artField), path.resolve(AUDITS, artField), path.resolve(PROJECT, artField.replace(/^\.\.\//, ''))].filter(x => fs.existsSync(x) && fs.statSync(x).isFile()))];
      if (cand.length === 1) { resolved = cand[0]; hashStatus = (hash(fs.readFileSync(resolved)).toLowerCase() === digestCell.toLowerCase()) ? 'MATCH' : 'MISMATCH'; }
      else hashStatus = cand.length === 0 ? 'UNRESOLVED_POINTER' : 'AMBIGUOUS_POINTER(' + cand.length + ')';
    }
    // scope classification (same documented rules as the R1 sidecars)
    let scope = 'IMMUTABLE_SNAPSHOT';
    const rp = (resolved || '').replace(/\\/g, '/').toLowerCase();
    if (/readme\.md$/.test(rp) && rp.includes('docs/nif')) scope = 'PRE_EDIT_INPUT';
    else if (/09-semantics\.md$/.test(rp) && rp.includes('docs/nif')) scope = 'PRE_EDIT_INPUT';
    else if (rp.includes('pe_auto_loop.json')) scope = 'MUTABLE_POINTER';
    else if (/report\.md$/.test(rp) || /stage_acceptance_gates\.csv$/.test(rp) || /handoff\.md$/.test(rp) || /sha256_driver\.txt$/.test(rp)) scope = 'POST_EDIT_OUTPUT';
    else if (hashStatus === 'UNRESOLVED_POINTER' || hashStatus.startsWith('AMBIGUOUS')) scope = 'UNRESOLVED_ALIAS';
    else if (artField === 'source_of_truth_corpus' || artField.startsWith('frozen_parser_r61_manifest')) scope = 'UNRESOLVED_ALIAS';
    let headerMapped, reconStatus, uncertainty;
    if (isBlank) { headerMapped = 'UNRESOLVED'; reconStatus = 'EMPTY_LINE_PRESERVED'; uncertainty = 'zero-byte line preserved verbatim (part of the original file bytes; required for byte-exact reconstruction)'; }
    else if (strictValid) { headerMapped = JSON.stringify(Object.fromEntries(head.map((h, i2) => [h, parsed.fields[i2]]))); reconStatus = 'RECOVERED'; uncertainty = UND_STRICT; }
    else { headerMapped = 'UNRESOLVED'; reconStatus = 'UNRESOLVED'; uncertainty = UND_MALFORMED; }
    const termBytes = row.term === 'CRLF' ? Buffer.from([0x0D, 0x0A]) : row.term === 'LF' ? Buffer.from([0x0A]) : Buffer.alloc(0);
    reconBuf.push(Buffer.concat([row.line, termBytes]));
    side.push([run, '99_Audits/' + run + '/artifact_index.csv', origSha, r + 1, row.term, row.line.toString('base64'), hash(row.line),
      String(strictValid), parsed.fields.length, head.length, JSON.stringify(parsed.fields), headerMapped, reconStatus,
      artField, digestCell, hashStatus, (resolved || '').replace(/\//g, '\\'), resolved ? 'RESOLVED' : 'UNRESOLVED_ALIAS', scope, NORM_RULE, uncertainty].map(esc).join(','));
  }
  const recon = Buffer.concat(reconBuf);
  const reconEqual = recon.equals(rawBuf);
  const reconStatusCounts = {};
  for (const line of side.slice(1)) { const st = csvParse(line).fields[12]; reconStatusCounts[st] = (reconStatusCounts[st] || 0) + 1; }
  fs.writeFileSync(RUN + '/05_ANALYSIS/NORMALIZED_MANIFESTS/' + run + '.artifact_index.lossless.csv', side.join('\r\n') + '\r\n');
  OUT.sidecars.push({
    run: run, original_manifest: '99_Audits/' + run + '/artifact_index.csv', original_manifest_sha256: origSha,
    rows_total_including_header: rows.length, data_rows: rows.length - 1, strict_rows: strictRows, malformed_rows: malformedRows,
    reconstruction_statuses: reconStatusCounts,
    full_file_reconstruction_sha256_equal: reconEqual,
    reconstruction_sha256: hash(recon), newline_style: rows[0].term
  });
}

// ---------- 8. R39 GAP_ANALYSIS round-trip test (Area C explicit requirement) ----------
const r39SidecarPath = RUN + '/05_ANALYSIS/NORMALIZED_MANIFESTS/PE_NIF_WIKI_AUDIT_R39_20260904_180213.artifact_index.lossless.csv';
const r39Rows = fs.readFileSync(r39SidecarPath, 'utf8').replace(/^\uFEFF/, '').split('\r\n').filter(l => l.length > 0);
const r39Parsed = r39Rows.map(l => csvParse(l).fields);
const r39Gap = r39Parsed.filter(f => f[13] === '02_results/GAP_ANALYSIS.json')[0];
const gapDecoded = Buffer.from(r39Gap[5], 'base64');
const gapFullRoleText = 'per-file gaps, priorities, orphan/ambiguous-label classification';
// byte-exact comparison against the ORIGINAL manifest line (independent of the base64 round-trip)
const r39Orig = fs.readFileSync(AUDITS + '/PE_NIF_WIKI_AUDIT_R39_20260904_180213/artifact_index.csv');
let r39OrigLine = null, cursor = 0, lineNo = 0;
while (cursor <= r39Orig.length) {
  const nl = r39Orig.indexOf(0x0A, cursor);
  const hasCR = nl > cursor && r39Orig[nl - 1] === 0x0D;
  const end = nl < 0 ? r39Orig.length : (hasCR ? nl - 1 : nl);
  const line = r39Orig.subarray(cursor, end);
  lineNo++;
  if (lineNo === Number(r39Gap[3])) { r39OrigLine = line; break; }
  if (nl < 0) break;
  cursor = nl + 1;
}
// R1 sidecar (read-only) for comparison
const r1Side = fs.readFileSync(R1RUN + '/05_ANALYSIS/NORMALIZED_MANIFESTS/PE_NIF_WIKI_AUDIT_R39_20260904_180213.artifact_index.normalized.csv', 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/).filter(l => l.length > 0).map(l => csvParse(l).fields);
const r1Gap = r1Side.filter(f => f[4] === '02_results/GAP_ANALYSIS.json')[0];
OUT.r39_gap_row_test = {
  original_row_number: r39Gap[3], row_terminator: r39Gap[4],
  decoded_line: gapDecoded.toString('utf8'),
  decoded_contains_full_role_text: gapDecoded.toString('utf8').includes(gapFullRoleText),
  decoded_bytes_equal_original_manifest_line_bytes: r39OrigLine !== null && gapDecoded.equals(r39OrigLine),
  original_line_sha256: r39OrigLine ? hash(r39OrigLine) : null,
  r2_reconstruction_status: r39Gap[12],
  r2_header_mapped: r39Gap[11],
  r2_no_silent_truncation: r39Gap[12] === 'UNRESOLVED' && !JSON.stringify(r39Gap).includes('per-file gaps [priorities]'),
  r1_sidecar_role_value: r1Gap ? r1Gap[5] : 'NOT_FOUND',
  r1_sidecar_role_preserves_original: r1Gap ? r1Gap[5].includes(gapFullRoleText) : false,
  r1_sidecar_lost_text_confirmed: r1Gap ? (r1Gap[5] === 'per-file gaps [priorities]') : false
};

// ---------- 9. synthetic quoting/escaping fixture (Area C; for the independent checker) ----------
// mixed newline policy: rows 1-3 CRLF, row 4 LF (byte-accurate construction)
const synOriginal = Buffer.concat([
  Buffer.from('artifact,role,sha256\r\n', 'utf8'),
  Buffer.from('a,b"quoted, with comma",c\r\n', 'utf8'),
  Buffer.from('x,"line with ""escaped"" quotes",y\r\n', 'utf8'),
  Buffer.from('z,trailing\n', 'utf8')]);
const synRows = [{ l: Buffer.from('artifact,role,sha256', 'utf8'), t: 'CRLF' }, { l: Buffer.from('a,b"quoted, with comma",c', 'utf8'), t: 'CRLF' },
  { l: Buffer.from('x,"line with ""escaped"" quotes",y', 'utf8'), t: 'CRLF' }, { l: Buffer.from('z,trailing', 'utf8'), t: 'LF' }];
const synSide = [SIDE_HEAD.map(esc).join(',')];
const synRecon = [];
for (let r = 0; r < synRows.length; r++) {
  const lineStr = synRows[r].l.toString('utf8'); const parsed = csvParse(lineStr);
  const strictValid = parsed.fields.length === 3 && !parsed.unclosed && r > 0;
  const isHeader = r === 0;
  synSide.push(['SYNTHETIC', '00_CONTROL/FIXTURES/synthetic_original.csv', hash(synOriginal), r + 1, synRows[r].t, synRows[r].l.toString('base64'), hash(synRows[r].l),
    String(isHeader || strictValid), parsed.fields.length, 3, JSON.stringify(parsed.fields),
    (isHeader || strictValid) ? JSON.stringify(Object.fromEntries(['artifact', 'role', 'sha256'].map((h, i2) => [h, parsed.fields[i2]]))) : 'UNRESOLVED',
    'RECOVERED', parsed.fields[0], '', 'NO_HASH_FIELD', '', 'FIXTURE', 'SYNTHETIC_FIXTURE', NORM_RULE,
    'synthetic quoting/escaping fixture row'].map(esc).join(','));
  synRecon.push(Buffer.concat([synRows[r].l, synRows[r].t === 'CRLF' ? Buffer.from([0x0D, 0x0A]) : synRows[r].t === 'LF' ? Buffer.from([0x0A]) : Buffer.alloc(0)]));
}
fs.writeFileSync(RUN + '/00_CONTROL/FIXTURES/synthetic_sidecar.csv', synSide.join('\r\n') + '\r\n');
fs.writeFileSync(RUN + '/00_CONTROL/FIXTURES/synthetic_original.csv', synOriginal);
OUT.synthetic_quoting_fixture = {
  note: 'quoting/escaping/newline-policy round-trip fixture for the independent Python checker (mixed CRLF/LF, embedded quotes, quoted commas)',
  original_sha256: hash(synOriginal), sidecar_reconstruction_sha256_equal: Buffer.concat(synRecon).equals(synOriginal)
};

// ---------- write output ----------
fs.writeFileSync(RUN + '/01_RAW/RECOUNTS.json', JSON.stringify(OUT, null, 2) + '\n');
const brief = {
  era_join: { shared: OUT.era_join.shared_names, identical: OUT.era_join.byte_identical, changed: OUT.era_join.changed, old_only: OUT.era_join.old_only_count, new_only: OUT.era_join.new_only_953_count, sums_ok: OUT.era_join.sum_checks },
  family_unique_files: Object.fromEntries(FAMS.map(f => [f, [changedScan[f].unique_files, changedScan[f].ascii_occurrences, oldOnlyScan[f].unique_files, oldOnlyScan[f].ascii_occurrences]])),
  morph: OUT.morph_changed_files,
  r1_fixture_reproduces: OUT.r1_bug_fixture.fixture_reproduces_r1_exactly,
  old_only_double_increment_confirmed: OUT.r1_bug_fixture.old_only_double_increment_confirmed,
  synthetic: OUT.synthetic_counter_tests,
  d: OUT.c_crc32_d,
  candidates: { exact_zero: OUT.field_d_candidates_physical.exact_zero_candidate_count, nonzero: OUT.field_d_candidates_physical.nonzero_candidates,
    e953: OUT.field_d_candidates_physical.census_953.name_derived_candidate_matches, e2003: OUT.field_d_candidates_physical.census_2003.name_derived_candidate_matches },
  r36_agreement_all: Object.values(OUT.r36_historical_agreement.e953).every(x => x.agree) && Object.values(OUT.r36_historical_agreement.e2003).every(x => x.agree),
  sidecars_reconstruction_equal: OUT.sidecars.map(s => s.full_file_reconstruction_sha256_equal),
  r39_gap: { full_role_text: OUT.r39_gap_row_test.decoded_contains_full_role_text, r1_role: OUT.r39_gap_row_test.r1_sidecar_role_value, r1_lost: OUT.r39_gap_row_test.r1_sidecar_lost_text_confirmed }
};
console.log('control_r2 OK');
console.log(JSON.stringify(brief, null, 1));
