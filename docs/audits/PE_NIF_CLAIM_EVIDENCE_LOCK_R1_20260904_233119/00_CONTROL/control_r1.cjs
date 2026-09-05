// control_r1.cjs — PE-NIF-CLAIM-EVIDENCE-LOCK-R1 one-time control instrumentation.
// READ-ONLY on all sources. Writes ONLY to this run dir (01_RAW, 05_ANALYSIS).
// Verifies the external auditor's allegations F1-F6 from RAW evidence (not from probe.json).
// Hash-after-last-edit rule: SHA256 of this file recorded in SHA256_CONTROL.txt BEFORE execution.
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto'), { execFileSync } = require('child_process');
const PROJECT = 'D:/Eudoria_Reconstruction';
const AUDITS = PROJECT + '/99_Audits';
const RUN = AUDITS + '/PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119';
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const OUT = {};

// ---------- helpers ----------
function readJSON(p) { return JSON.parse(fs.readFileSync(p, 'utf8').replace(/^\uFEFF/, '')); }
function csvParse(line) { // RFC4180-style state machine (same standard as probe.cjs)
  const fields = []; let s = '', quoted = false;
  for (let i = 0; i < line.length; i++) { const c = line[i];
    if (c === '"') { if (quoted && line[i+1] === '"') { s += '"'; i++; } else quoted = !quoted; }
    else if (c === ',' && !quoted) { fields.push(s); s = ''; } else s += c; }
  fields.push(s); return { fields, unclosed: quoted };
}

// ---------- CONTROL 1 (R32): independent f1 recount ----------
(function control1() {
  const afc = readJSON(AUDITS + '/PE_NIF_MATERIAL_CENSUS_R32_20260904_160538/02_results/ANIM_FRAME_CHECK.json');
  const f1 = {}, framePrefix = {}; let total = 0, slots = 0;
  for (const [slot, d] of Object.entries(afc.per_slot)) {
    slots++; total += d.count;
    for (const [v, n] of Object.entries(d.f1)) f1[v] = (f1[v] || 0) + n;
    for (const [k, n] of Object.entries(d.frame_prefix)) framePrefix[k] = (framePrefix[k] || 0) + n;
  }
  let sumF1 = 0; for (const n of Object.values(f1)) sumF1 += n;
  // late slots ANIM16..31: how many carry f1=11?
  let late16_31_count = 0, late16_31_f11 = 0, late16_31_f0 = 0, late16_31_f4 = 0;
  for (let i = 16; i <= 31; i++) { const d = afc.per_slot['ANIM' + i]; if (!d) continue;
    late16_31_count += d.count; late16_31_f11 += d.f1['11'] || 0; late16_31_f0 += d.f1['0'] || 0; late16_31_f4 += d.f1['4'] || 0; }
  OUT.control1_r32 = {
    source: 'R32/02_results/ANIM_FRAME_CHECK.json (raw, independent recount)',
    anim_entries_total_field: afc.anim_entries_total,
    recount_total: total, per_slot_count_sum: slots,
    f1_distribution: f1, f1_distribution_sum: sumF1,
    frame_index_equals_slot_number_field: afc.frame_index_equals_slot_number,
    frame_prefix_values: Object.values(framePrefix).reduce((a,b)=>a+b,0),
    regular_00ffffffff_prefix: afc.regular_00ffffffff_prefix, mismatches: afc.mismatches.length,
    allegation_985_142_30: (f1['11'] === 985 && f1['0'] === 142 && f1['4'] === 30),
    exceptions_172: ((f1['0'] || 0) + (f1['4'] || 0)),
    ANIM16_31: { count: late16_31_count, f1_11: late16_31_f11, f1_0: late16_31_f0, f1_4: late16_31_f4 },
    r32_report_claims_10_of_45_carry_11: late16_31_f11 === 10,
    r32_report_actual_value: late16_31_f11
  };
})();

// ---------- CONTROL 2 (R33/R34): denominators + k=1 counterexamples ----------
(function control2() {
  const rsg = readJSON(AUDITS + '/PE_NIF_MORPH_QUANT_R34_20260904_164538/02_results/REAL_SPARSE_GRAMMAR.json');
  const ex = rsg.VARIABLE_K.exact_examples_cap50;
  const k1 = ex.filter(e => e[4] && e[4]['1']);
  const si14 = ex.find(e => e[0] === '574845.nif' && e[1] === 69 && e[2] === 14);
  const si27 = ex.find(e => e[0] === '574845.nif' && e[1] === 69 && e[2] === 27);
  const perSpan574845 = rsg.per_span.filter(p => p.file === '574845.nif');
  const kHistAll = {};
  for (const e of ex) for (const [k, n] of Object.entries(e[4])) kHistAll[k] = (kHistAll[k] || 0) + n;
  OUT.control2_r33r34 = {
    denominators: {
      fit_spans_tested: rsg.meta.fit_spans_tested,
      real_record_spans: rsg.meta.real_record_spans,
      real_record_spans_def: rsg.meta.real_record_spans_def,
      g1_exact: rsg.G1_prompt_W_from_block.spans_exact, g1_rr: rsg.G1_prompt_W_from_block.spans_exact_of_real_record,
      g2_exact: rsg.G2_variant_W_plus_1.spans_exact, g2_rr: rsg.G2_variant_W_plus_1.spans_exact_of_real_record,
      mscan: rsg.M_SCAN.spans_with_any_valid_m, mscan_rr: rsg.M_SCAN.spans_with_any_valid_m_of_real_record,
      var_exact: rsg.VARIABLE_K.spans_exact, var_rr: rsg.VARIABLE_K.spans_exact_of_real_record,
      var_files: rsg.VARIABLE_K.files_exact,
      rr_pct: +(100 * rsg.VARIABLE_K.spans_exact_of_real_record / rsg.meta.real_record_spans).toFixed(2),
      var_pct_of_all_fit: +(100 * rsg.VARIABLE_K.spans_exact / rsg.meta.fit_spans_tested).toFixed(2),
      mscan_odd_m: { m1: (rsg.M_SCAN.m_histogram.find(x => x[0] === 1) || [])[1], m3: (rsg.M_SCAN.m_histogram.find(x => x[0] === 3) || [])[1] }
    },
    k1_counterexamples: {
      count_examples_with_k1: k1.length,
      file_574845_bi69_si14: si14 ? { records: si14[3], k_hist: si14[4] } : null,
      file_574845_bi69_si27: si27 ? { records: si27[3], k_hist: si27[4] } : null,
      per_span_var_ok_spans_574845: perSpan574845.filter(p => p.var_ok).length,
      per_span_total_574845: perSpan574845.length
    },
    k_hist_in_exact_examples_cap50: kHistAll,
    driver_facts: {
      parse_variable_rule: 'for k in range(1, VAR_MAX_K+1): break on FIRST match (morph_quant_r34.py L825-838)',
      VAR_MAX_K: 8, WP_TOL: 1e-4, VAR_NDELTA: 9,
      REAL_def: 'entry, id!=0, id<N, all-4 floats clean, pos%4==0 (prompt criteria; R33-derived)',
      uniqueness_proof_present: false
    },
    k_range_2003_r35: readJSON(AUDITS + '/PE_NIF_CROSS_ERA_R35_20260904_170224/02_results/GRAMMAR_VALIDATION.json').morph_real_sparse_and_quant['2003'].grammar.k_histogram
  };
})();

// ---------- CONTROL 3+4 (R35/R36): direct BNT2 re-read, era join, d analysis ----------
function parseBnt(p) {
  const b = fs.readFileSync(p);
  const start = b.readUInt32LE(b.length - 8);
  const count = b.readUInt32LE(start);
  let pos = start + 4;
  const entries = new Map(); const order = [];
  for (let i = 0; i < count; i++) {
    const end = b.indexOf(10, pos);
    const name = b.subarray(pos, end).toString('ascii');
    const size = b.readUInt32LE(end + 1), offset = b.readUInt32LE(end + 5), c = b.readUInt32LE(end + 9), d = b.readUInt32LE(end + 13);
    entries.set(name, { size, offset, c, d, bytes: b.subarray(offset, offset + size) });
    order.push(name); pos = end + 17;
  }
  return { sha256: hash(b), size: b.length, count, indexEnd: pos, indexExpectedEnd: b.length - 8, entries, order };
}
const CRC_TABLE = Uint32Array.from({ length: 256 }, (_, v) => { for (let k = 0; k < 8; k++) v = (v >>> 1) ^ ((v & 1) ? 0xedb88320 : 0); return v >>> 0; });
function crc32(b) { let c = 0xffffffff; for (const x of b) c = (c >>> 8) ^ CRC_TABLE[(c ^ x) & 255]; return (c ^ 0xffffffff) >>> 0; }
const pcg = parseBnt(PROJECT + '/pcg_install/Data/Models/Models.bnt');
const old = parseBnt(PROJECT + '/01_Original_Files/BNT_Models/Models.bnt');
(function control3_4() {
  const cMism = [];
  for (const [n, e] of pcg.entries) if (crc32(e.bytes) !== e.c) cMism.push('953:' + n);
  for (const [n, e] of old.entries) if (crc32(e.bytes) !== e.c) cMism.push('2003:' + n);
  let dEqC953 = 0, dEqC03 = 0;
  for (const e of pcg.entries.values()) if (e.d === e.c) dEqC953++;
  for (const e of old.entries.values()) if (e.d === e.c) dEqC03++;
  const names953 = new Set(pcg.order), names03 = new Set(old.order);
  const shared = [...names03].filter(n => names953.has(n));
  const oldOnly = [...names03].filter(n => !names953.has(n));
  const newOnly = [...names953].filter(n => !names03.has(n));
  let identical = 0, changedSameVer = 0, flips = 0, dStable = 0; const changedNames = [], dChangedOnIdentical = [];
  for (const n of shared) {
    const a = old.entries.get(n), b = pcg.entries.get(n);
    const same = a.bytes.equals(b.bytes);
    if (same) { identical++; if (a.d === b.d) dStable++; else dChangedOnIdentical.push(n); }
    else { changedNames.push(n); }
  }
  OUT.control3_4_bnt = {
    pcg: { sha256: pcg.sha256, entries: pcg.count, index_exact: pcg.indexEnd === pcg.indexExpectedEnd },
    old2003: { sha256: old.sha256, entries: old.count, index_exact: old.indexEnd === old.indexExpectedEnd },
    c_eq_crc32_payload: { checked: pcg.count + old.count, mismatches: cMism.length, mismatch_names: cMism },
    d_eq_c: { e953: dEqC953 + '/' + pcg.count, e2003: dEqC03 + '/' + old.count },
    era_join: {
      shared_names: shared.length, byte_identical: identical, changed: changedNames.length,
      old_only_2003: oldOnly, new_only_953_count: newOnly.length,
      d_stable_among_identical: dStable, d_changed_on_identical: dChangedOnIdentical
    }
  };
  // family witnesses in changed / old-only 2003 payloads (block-name scan + diff-region intersection)
  const FAMS = ['NiArkAnimationExtraData', 'NiArkShaderExtraData', 'NiArkTextureExtraData', 'NiVertexMorphExtraData', 'NiArkImporterExtraData'];
  function blockRanges(payload) {
    const ranges = [];
    for (const fam of FAMS) {
      let i = 0;
      while ((i = payload.indexOf(Buffer.from(fam, 'ascii'), i)) !== -1) { ranges.push({ fam, start: i, end: i + fam.length }); i += fam.length; }
    }
    ranges.sort((a, b) => a.start - b.start);
    // approximate block payload region = [name_start, next name start]
    return ranges.map((r, i) => ({ ...r, regionEnd: i + 1 < ranges.length ? ranges[i + 1].start : payload.length }));
  }
  function diffRegions(a, b) {
    if (a.length !== b.length) return [{ start: 0, end: Math.max(a.length, b.length), sizeChange: true }];
    let i = 0; while (i < a.length && a[i] === b[i]) i++;
    if (i >= a.length) return [];
    let j = 0; while (j < a.length - i && a[a.length - 1 - j] === b[b.length - 1 - j]) j++;
    return [{ start: i, end: a.length - j }];
  }
  const witness = {}; for (const f of FAMS) witness[f] = { changed_files_with_block: 0, changed_files_with_diff_inside_block_region: 0, old_only_files_with_block: 0 };
  const detail = [];
  for (const n of changedNames.concat(oldOnly)) {
    const p03 = old.entries.get(n).bytes;
    const p953 = pcg.entries.get(n) ? pcg.entries.get(n).bytes : null;
    const ranges = blockRanges(p03);
    const drs = p953 ? diffRegions(p953, p03) : [{ start: 0, end: p03.length }];
    for (const r of ranges) {
      if (!witness[r.fam]) continue;
      if (p953) witness[r.fam].changed_files_with_block++;
      else witness[r.fam].old_only_files_with_block++;
      for (const d of drs) if (d.start < r.regionEnd && d.end > r.start) {
        if (p953) witness[r.fam].changed_files_with_diff_inside_block_region++; else witness[r.fam].old_only_files_with_block++;
        detail.push({ file: n, family: r.fam, diffStart: d.start, diffEnd: d.end, blockNameAt: r.start, region: [r.start, r.regionEnd] });
        break;
      }
    }
  }
  OUT.control3_4_bnt.family_witness_2003_nonidentical = {
    method: 'block-name ASCII scan of the 2003 payload; block payload region approximated as [name_start, next block-name start); diff regions by common-prefix/suffix trim vs the 953 payload (size-change = whole-file diff). APPROXIMATE locality heuristic, honest label.',
    changed_files: changedNames.length, old_only_files: oldOnly.length,
    witness: witness, first_40_bytelevel_witnesses: detail.slice(0, 40), bytelevel_witness_total: detail.length
  };
})();

// ---------- CONTROL 5 (R29/R37/R38): spot re-reads ----------
(function control5() {
  const pat = readJSON(AUDITS + '/PE_NIF_IMPORTER_HEADER_R29_20260904_150900/02_results/PATTERNS.json');
  const v10_4x = pat.era_matrix_nifver_x_exporter.filter(r => r.nif_version === '10.1.0.0' && r.exporter_string !== 'Gamebryo_1_1').reduce((a, r) => a + r.count, 0);
  const cs = readJSON(AUDITS + '/PE_NIF_G3D_CLASS_ROLE_R37_20260904_173625/02_results/CLASS_SEQUENCES.json');
  const srt = cs.a2_position.scene_root_target;
  const ma = readJSON(AUDITS + '/PE_NIF_TEXT_MODES_R38_20260904_175053/02_results/MODE_ANALYSIS.json');
  OUT.control5_r29_r37_r38 = {
    r29: { exact_patterns: pat.patterns.length, masked_patterns: pat.masked_patterns.length, v10_with_4x_strings: v10_4x, gamebryo_1_1_v10: (pat.era_matrix_nifver_x_exporter.find(r => r.exporter_string === 'Gamebryo_1_1') || {}).count },
    r37: { class_histogram: cs.class_histogram, scene_root_target_bucket: srt.bucket_census, relpos_min: srt.relpos.min, relpos_max: srt.relpos.max, n_records: srt.n_scene_root_target_records, plus_single_record_file: 1, root_last_total: srt.n_scene_root_target_records + 1 },
    r38: { mode_census: ma.M1_cross_tables.mode_census, twin_pair_41076: ma.M3_mode_vs_mode.identical_param_pairs_diff_mode.map(x => ({ file: x.file, mode: x.mode })), verdicts: ma.verdicts || null }
  };
})();

// ---------- CONTROL 6 (R39/R40): proposals, applied state, manifest validation ----------
(function control6() {
  const repo = PROJECT + '/12_WebGame/eudoria-clean';
  const gitShow = ref => Buffer.from(execFileSync('git', ['-c', 'safe.directory=*', 'show', ref], { cwd: repo, maxBuffer: 1e7 }));
  const sem = readJSON(AUDITS + '/PE_NIF_SEMANTICS_ENRICH_R40_20260904_182016/02_results/SEMANTICS_PROPOSALS.json');
  const rem = readJSON(AUDITS + '/PE_NIF_SEMANTICS_ENRICH_R40_20260904_182016/02_results/README_PROPOSALS.json');
  const ed = readJSON(AUDITS + '/PE_NIF_WIKI_AUDIT_R39_20260904_180213/02_results/EDIT_PROPOSALS.json');
  const applySim = (preB, props) => { let s = preB.toString('utf8'); for (const p of props) s = s.replace(p.old_text, p.new_text); return Buffer.from(s, 'utf8'); };
  const semSim = applySim(gitShow('077b8a4^:docs/nif/09-semantics.md'), sem.proposals);
  const remSim = applySim(gitShow('077b8a4^:docs/nif/README.md'), rem.proposals);
  const semPost = gitShow('077b8a4:docs/nif/09-semantics.md');
  const remPost = gitShow('077b8a4:docs/nif/README.md');
  const numstat = f => execFileSync('git', ['-c', 'safe.directory=*', 'diff', '077b8a4^', '077b8a4', '--numstat', '--', 'docs/nif/' + f], { cwd: repo, encoding: 'utf8' }).trim();
  const editCount = Array.isArray(ed.proposals) ? ed.proposals.length : (ed.proposal_count || Object.keys(ed).length);
  OUT.control6_r39_r40 = {
    r39_edit_proposals_count: editCount,
    r40_proposals: { readme: rem.proposals.length, semantics: sem.proposals.length },
    r40_apply_byte_exact: {
      '09-semantics.md': { sim_sha: hash(semSim), actual_sha: hash(semPost), equal: semSim.equals(semPost), sim_bytes: semSim.length, actual_bytes: semPost.length },
      'README.md': { sim_sha: hash(remSim), actual_sha: hash(remPost), equal: remSim.equals(remPost), sim_bytes: remSim.length, actual_bytes: remPost.length }
    },
    r40_report_size_figures: {
      report_claimed: { 'README.md': '4573 -> 9182 bytes', '09-semantics.md': '3705 -> 13214 bytes' },
      verified_true_byte_sizes: { 'README.md': [gitShow('077b8a4^:docs/nif/README.md').length, remPost.length], '09-semantics.md': [gitShow('077b8a4^:docs/nif/09-semantics.md').length, semPost.length] },
      verdict: 'unit-mix: report adds a CHAR delta to a BYTE pre-size; true byte sizes 9213 / 13326'
    },
    plus_236_lines_claim: { source: 'PE_AUTO_LOOP.json last_completed (ITER-40)', numstat: { 'README.md': numstat('README.md'), '09-semantics.md': numstat('09-semantics.md') }, combined_added: null }
  };
  const ns = s => s ? parseInt(s) : 0;
  const rns = OUT.control6_r39_r40.plus_236_lines_claim.numstat;
  OUT.control6_r39_r40.plus_236_lines_claim.combined_added = ns((rns['README.md']||'').split(/\s/)[0]) + ns((rns['09-semantics.md']||'').split(/\s/)[0]);
})();

// ---------- MANIFEST validation + normalized sidecars (12 runs) ----------
(function manifests() {
  const runs = fs.readdirSync(AUDITS).filter(n => /^PE_NIF_.*_R(29|30|31|32|33|34|35|36|37|38|39|40)_/.test(n)).sort();
  OUT.manifests = [];
  for (const run of runs) {
    const dir = AUDITS + '/' + run;
    const raw = fs.readFileSync(dir + '/artifact_index.csv', 'utf8');
    const origSha = hash(fs.readFileSync(dir + '/artifact_index.csv'));
    const lines = raw.replace(/\r\n/g, '\n').trim().split('\n'); // trim = trailing blank lines are NOT data rows (probe.cjs standard)
    const head = csvParse(lines[0]).fields;
    const shaCol = head.indexOf('sha256');
    const pathCol = head.indexOf('artifact') >= 0 ? head.indexOf('artifact') : head.indexOf('path');
    const rows = []; const strictErrors = [];
    for (let i = 1; i < lines.length; i++) {
      const c = csvParse(lines[i]);
      if (c.fields.length !== head.length || c.unclosed) strictErrors.push({ line: i + 1, expectedColumns: head.length, actualColumns: c.fields.length, text: lines[i] });
    }
    // resolve + verify hashes, classify rows
    for (let i = 1; i < lines.length; i++) {
      const cells = csvParse(lines[i]).fields; // permissive recovery of the row
      const digest = cells.find(x => /^[a-fA-F0-9]{64}$/.test(x)) || '';
      const art = (cells[pathCol] || '').trim();
      let resolved = null, hashStatus = 'NO_HASH_FIELD';
      if (digest) {
        const cand = [...new Set([path.resolve(dir, art), path.resolve(PROJECT, art), path.resolve(AUDITS, art), path.resolve(PROJECT, art.replace(/^\.\.\//, ''))].filter(x => fs.existsSync(x) && fs.statSync(x).isFile()))];
        if (cand.length === 1) { resolved = cand[0]; hashStatus = (hash(fs.readFileSync(resolved)).toLowerCase() === digest.toLowerCase()) ? 'MATCH' : 'MISMATCH'; }
        else hashStatus = cand.length === 0 ? 'UNRESOLVED_POINTER' : 'AMBIGUOUS_POINTER(' + cand.length + ')';
      }
      rows.push({ row: i + 1, raw_text: lines[i], cells, artifact_field: art, sha256_field: digest, hash_status: hashStatus, resolved_path: resolved });
    }
    OUT.manifests.push({ run, orig_sha256: origSha, header: head, row_count: lines.length - 1, strict_errors: strictErrors });
    // normalized sidecar (strict valid CSV)
    const esc = s => '"' + String(s).replace(/"/g, '""') + '"';
    const side = [ ['run','original_manifest','original_manifest_sha256','original_row','artifact','role','sha256','hash_status','resolved_full_path','path_status','scope_class'].join(',') ];
    for (const r of rows) {
      const role = (r.cells[head.indexOf('role')] || '').trim();
      const computedBy = head.indexOf('computed_by') >= 0 ? (r.cells[head.indexOf('computed_by')] || '').trim() : '';
      let scope = 'IMMUTABLE_SNAPSHOT'; // default: inside a completed run dir
      const a = r.artifact_field.toLowerCase(); const rp = (r.resolved_path || '').replace(/\\/g, '/').toLowerCase();
      if (/readme\.md$/.test(rp) && rp.includes('docs/nif')) scope = 'PRE_EDIT_INPUT';           // R40 recorded pre-apply wiki state
      else if (/09-semantics\.md$/.test(rp) && rp.includes('docs/nif')) scope = 'PRE_EDIT_INPUT';
      else if (rp.includes('pe_auto_loop.json')) scope = 'MUTABLE_POINTER';                       // live loop state
      else if (/report\.md$/.test(rp) || /stage_acceptance_gates\.csv$/.test(rp) || /handoff\.md$/.test(rp) || /sha256_driver\.txt$/.test(rp)) scope = 'POST_EDIT_OUTPUT';
      else if (r.hash_status === 'UNRESOLVED_POINTER' || r.hash_status.startsWith('AMBIGUOUS')) scope = 'UNRESOLVED_ALIAS';
      else if (a === 'source_of_truth_corpus' || a.startsWith('frozen_parser_r61_manifest')) scope = 'UNRESOLVED_ALIAS';
      const pathStatus = r.resolved_path ? 'RESOLVED' : 'UNRESOLVED_ALIAS';
      side.push([run, '99_Audits/' + run + '/artifact_index.csv', origSha, r.row, r.artifact_field, role + (computedBy ? ' [' + computedBy + ']' : ''), r.sha256_field, r.hash_status, r.resolved_path ? r.resolved_path.replace(/\//g, '\\') : '', pathStatus, scope].map(esc).join(','));
    }
    fs.writeFileSync(RUN + '/05_ANALYSIS/NORMALIZED_MANIFESTS/' + run + '.artifact_index.normalized.csv', side.join('\r\n') + '\r\n');
  }
})();

// ---------- write outputs ----------
OUT.provenance = {
  control_script: '00_CONTROL/control_r1.cjs',
  written_by: 'pe-reconstruction, PE-NIF-CLAIM-EVIDENCE-LOCK-R1',
  read_only_on_sources: true,
  sources_read: ['pcg_install/Data/Models/Models.bnt', '01_Original_Files/BNT_Models/Models.bnt', 'R29-R40 run dirs', 'docs/nif @ git 077b8a4 (+HEAD 8cd0bc3 unchanged)'],
  note: 'This file is CONTROL OUTPUT, not a re-run of any historical driver.'
};
fs.writeFileSync(RUN + '/01_RAW/CONTROL_R1_RESULTS.json', JSON.stringify(OUT, null, 2));
console.log('control_r1 OK. strictCsvErrors total: ' + OUT.manifests.reduce((a, m) => a + m.strict_errors.length, 0));
console.log(JSON.stringify({ c1: { f1: OUT.control1_r32.f1_distribution, ANIM16_31_f11: OUT.control1_r32.ANIM16_31.f1_11 }, c2: { den: OUT.control2_r33r34.denominators, k1: OUT.control2_r33r34.k1_counterexamples.file_574845_bi69_si14 }, c34: { join: OUT.control3_4_bnt.era_join, deq: OUT.control3_4_bnt.d_eq_c, cmm: OUT.control3_4_bnt.c_eq_crc32_payload.mismatches.length }, witness: OUT.control3_4_bnt.family_witness_2003_nonidentical.witness, c6: { apply: OUT.control6_r39_r40.r40_apply_byte_exact, lines236: OUT.control6_r39_r40.plus_236_lines_claim } }, null, 1));
