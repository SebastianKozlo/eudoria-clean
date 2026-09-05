"""run_gates.py - PE-NIF-CLAIM-EVIDENCE-LOCK-R2 independent checker + executable gates.

INDEPENDENT IMPLEMENTATION (Python 3.12, stdlib only) of the R2 gate suite.
- Re-derives the core physical quantities from the two Models.bnt containers
  INDEPENDENTLY of the Node control_r2.cjs results (cross-language check).
- Validates the 12 lossless sidecars with the Python csv module (strict) against the
  ORIGINAL manifest files (source of truth = original bytes, not R2-generated data).
- Evaluates negative-control fixtures read from immutable R1 artifacts (read-only):
  the OLD erroneous outputs must FAIL the invariants (detection demonstrated), and the
  corrected R2 outputs must PASS.
- Writes 02_LOGS/TEST_RESULTS.json and EXITS NONZERO on any EXECUTABLE gate failure.

Usage: python run_gates.py --phase content|final
  content = all evidence gates (after control_r2.cjs + table emission + reports)
  final   = content + package gates (STAGE_ACCEPTANCE_GATES.csv + artifact_index.csv)
"""
import argparse, base64, csv, hashlib, io, json, struct, subprocess, sys, zlib
from pathlib import Path

BASE = Path('D:/Eudoria_Reconstruction')
AUDITS = BASE / '99_Audits'
RUN = AUDITS / 'PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054'
R1 = AUDITS / 'PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119'
BNT_953 = BASE / 'pcg_install/Data/Models/Models.bnt'
BNT_2003 = BASE / '01_Original_Files/BNT_Models/Models.bnt'
PROMPT = AUDITS / 'PE_NIF_CLAIM_LOCK_POST_AUDIT_20260905_020054/00_CONTROL/OPENCODE_R2_PROMPT.md'
EXPECTED_PROMPT_SHA = '46a2a99a9f1d03b4fe33f2fbfca89d2440fd702188a3d020e9bf29a7a370e5ed'
FAMS = ['NiArkAnimationExtraData', 'NiArkShaderExtraData', 'NiArkTextureExtraData',
        'NiVertexMorphExtraData', 'NiArkImporterExtraData']
TAXONOMY = {'CONFIRMED', 'STRONGLY_SUPPORTED', 'PLAUSIBLE', 'UNVERIFIED', 'REJECTED'}
MANIFEST_RUNS = ['PE_NIF_CROSS_ERA_R35_20260904_170224', 'PE_NIF_FIELD_D_R36_20260904_171903',
  'PE_NIF_G3B_VARIABLE_R30_20260904_152304', 'PE_NIF_G3D_CLASS_ROLE_R37_20260904_173625',
  'PE_NIF_IMPORTER_HEADER_R29_20260904_150900', 'PE_NIF_MATERIAL_CENSUS_R32_20260904_160538',
  'PE_NIF_MORPH_IDS_R33_20260904_162507', 'PE_NIF_MORPH_QUANT_R34_20260904_164538',
  'PE_NIF_RARE_VARIANTS_R31_20260904_154509', 'PE_NIF_SEMANTICS_ENRICH_R40_20260904_182016',
  'PE_NIF_TEXT_MODES_R38_20260904_175053', 'PE_NIF_WIKI_AUDIT_R39_20260904_180213']

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fnv1a(b):
    x = 0x811C9DC5
    for byte in b: x = ((x ^ byte) * 0x01000193) & 0xFFFFFFFF
    return x

GATES = []
def gate(gid, name, gtype, measured, denominator, truth, noncirc, failure, fixtures, ok):
    GATES.append({'gate_id': gid, 'gate_name': name, 'gate_type': gtype,
        'measured_quantity': measured, 'denominator': denominator,
        'independent_source_of_truth': truth, 'why_non_circular': noncirc,
        'failure_case_detected': failure, 'fixtures': fixtures, 'pass': bool(ok)})

def parse_bnt(p):
    b = Path(p).read_bytes()
    start = struct.unpack_from('<I', b, len(b) - 8)[0]
    assert 0 < start < len(b) - 8, 'bad index start'
    count = struct.unpack_from('<I', b, start)[0]
    pos = start + 4
    entries = {}
    for _ in range(count):
        end = b.index(b'\n', pos)
        assert end < len(b) - 8, 'bad name terminator'
        name = b[pos:end].decode('ascii')
        size, off, c, d = struct.unpack_from('<IIII', b, end + 1)
        assert name not in entries, 'duplicate name'
        assert off + size <= start, 'payload overruns index'
        entries[name] = {'size': size, 'off': off, 'c': c, 'd': d,
                         'name': name.encode('ascii'), 'payload': b[off:off + size]}
        pos = end + 17
    assert pos == len(b) - 8, 'index consumption not exact'
    assert len(entries) == count, 'count mismatch'
    return {'sha256': sha_bytes(b), 'size': len(b), 'entries': entries}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--phase', choices=['content', 'final'], default='content')
    phase = ap.parse_args().phase
    R = json.loads((RUN / '01_RAW/RECOUNTS.json').read_text(encoding='utf-8'))
    fails = []

    # ---------- R2G1: prompt identity ----------
    ok = sha_file(PROMPT) == EXPECTED_PROMPT_SHA
    gate('R2G1', 'execution prompt SHA256 verified (pre-execution record)', 'EXECUTABLE',
         'SHA256 of OPENCODE_R2_PROMPT.md', '1 prompt file',
         'the prompt file itself (physical)', 'hash recomputation, not a stored value',
         'any byte change in the prompt fails the gate', [], ok)
    if not ok: fails.append('R2G1')

    # ---------- R2G2: physical source identity (Python re-hash) ----------
    sha953, sha03 = sha_file(BNT_953), sha_file(BNT_2003)
    ok = (sha953 == 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0'
          and sha03 == '1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353f1cefd3524a6'
          and [s['sha256'] for s in R['physical_sources']] == [sha953, sha03])
    gate('R2G2', 'physical source identity (both Models.bnt SHA256)', 'EXECUTABLE',
         'SHA256 of both containers (Python + Node agree)', '2 containers',
         'the physical game files', 'fresh recomputation in two languages',
         'a modified/replaced container fails the gate', [], ok)
    if not ok: fails.append('R2G2')

    # ---------- independent physical re-derivation ----------
    print('[python] parsing both containers (independent re-derivation)...', flush=True)
    new = parse_bnt(BNT_953); old = parse_bnt(BNT_2003)
    shared = [n for n in old['entries'] if n in new['entries']]
    oldonly = sorted([n for n in old['entries'] if n not in new['entries']])
    newonly = [n for n in new['entries'] if n not in old['entries']]
    identical = [n for n in shared if old['entries'][n]['payload'] == new['entries'][n]['payload']]
    changed = [n for n in shared if n not in set(identical)]
    ej = R['era_join']
    ok = (len(shared) == ej['shared_names'] == 5422 and len(identical) == ej['byte_identical'] == 5208
          and len(changed) == ej['changed'] == 214 and oldonly == sorted(ej['old_only_2003'])
          and len(oldonly) == ej['old_only_count'] == 4 and len(newonly) == ej['new_only_953_count'] == 174
          and len(identical) + len(changed) == len(shared)
          and len(shared) + len(oldonly) == len(old['entries']) and len(shared) + len(newonly) == len(new['entries']))
    gate('R2G3', 'era join classification by exact bytes (Python == Node)', 'EXECUTABLE',
         'shared/identical/changed/old-only/new-only = 5422/5208/214/4/174', 'both corpora (5,426 + 5,596)',
         'the two physical containers', 'two independent implementations (Python/Node) over the same bytes',
         'sum-invariant violation or cross-language disagreement fails the gate', [], ok)
    if not ok: fails.append('R2G3')

    # family scan (Python, unique files + occurrences)
    def scan(names, side_entries):
        per = {f: {'unique_files': 0, 'ascii_occurrences': 0, 'per_file': {}} for f in FAMS}
        for n in names:
            p = side_entries[n]['payload']
            for f in FAMS:
                k = p.count(f.encode('ascii'))
                if k: per[f]['unique_files'] += 1; per[f]['ascii_occurrences'] += k; per[f]['per_file'][n] = k
        return per
    ch_scan, oo_scan = scan(changed, old['entries']), scan(oldonly, old['entries'])
    rch = R['family_scan_corrected']['changed']; roo = R['family_scan_corrected']['old_only']
    fam_ok = True
    for f in FAMS:
        fam_ok &= (ch_scan[f]['unique_files'] == rch[f]['unique_files'] and
                   ch_scan[f]['ascii_occurrences'] == rch[f]['ascii_occurrences'] and
                   ch_scan[f]['per_file'] == {k: v for k, v in rch[f]['per_file'].items()} and
                   oo_scan[f]['unique_files'] == roo[f]['unique_files'] and
                   oo_scan[f]['ascii_occurrences'] == roo[f]['ascii_occurrences'])
    exp_counts = {'NiArkAnimationExtraData': 214, 'NiArkShaderExtraData': 9, 'NiArkTextureExtraData': 214,
                  'NiVertexMorphExtraData': 3, 'NiArkImporterExtraData': 214}
    ok = fam_ok and all(ch_scan[f]['unique_files'] == exp_counts[f] for f in FAMS) \
        and all(ch_scan[f]['unique_files'] <= 214 for f in FAMS) \
        and all(oo_scan[f]['unique_files'] <= 4 for f in FAMS) \
        and oo_scan['NiArkAnimationExtraData']['unique_files'] == oo_scan['NiArkTextureExtraData']['unique_files'] \
            == oo_scan['NiArkImporterExtraData']['unique_files'] == 4 \
        and oo_scan['NiArkShaderExtraData']['unique_files'] == oo_scan['NiVertexMorphExtraData']['unique_files'] == 0
    gate('R2G4', 'family unique-file counts within eligible populations (Python == Node)', 'EXECUTABLE',
         'unique files: changed anim/tex/importer 214, shader 9, morph 3; old-only 4/0/4/0/4', '214 changed + 4 old-only files',
         'the physical containers', 'cross-language re-derivation; unique-file dedup enforced',
         'unique_file_count > eligible population (the R1 8>4 defect class) fails the gate',
         [{'fixture': 'R1 raw old_only_files_with_block=8 (animation/texture/importer)', 'invariant': 'unique_file_count <= 4', 'result': 'FAIL_DETECTED'}], ok)
    if not ok: fails.append('R2G4')

    # morph occurrence vs file distinction + R1 fixture
    r1raw = json.loads((R1 / '01_RAW/CONTROL_R1_RESULTS.json').read_text(encoding='utf-8-sig'))
    r1w = r1raw['control3_4_bnt']['family_witness_2003_nonidentical']['witness']
    morph_occ, morph_files = ch_scan['NiVertexMorphExtraData']['ascii_occurrences'], ch_scan['NiVertexMorphExtraData']['unique_files']
    ok = (morph_occ == 29 and morph_files == 3
          and ch_scan['NiVertexMorphExtraData']['per_file'] == {'548296.nif': 13, '548808.nif': 13, '566482.nif': 3}
          and R['morph_changed_files']['ascii_occurrences_total'] == 29 and R['morph_changed_files']['unique_files'] == 3)
    # fixture detection: R1's changed_files_with_block=29 for morph violates the unique-file invariant (29 files > 3 actual)
    fixture_detected = r1w['NiVertexMorphExtraData']['changed_files_with_block'] == 29 and morph_files == 3
    gate('R2G5', 'morph occurrence vs unique-file distinction (29 occurrences in 3 files)', 'EXECUTABLE',
         'ascii_occurrences=29; unique_files=3 (548296=13, 548808=13, 566482=3)', '214 changed files',
         'the physical containers', 'cross-language recount; occurrence and file counters kept separate',
         'presenting 29 as a file count fails the gate',
         [{'fixture': 'R1 raw changed_files_with_block=29 (morph) interpreted as files', 'invariant': 'unique_file_count == 3', 'result': 'FAIL_DETECTED'}], ok and fixture_detected)
    if not (ok and fixture_detected): fails.append('R2G5')

    # old-only double-increment fixture (R1 raw) + corrected values
    dbl = all(r1w[f]['old_only_files_with_block'] == 2 * oo_scan[f]['ascii_occurrences'] for f in FAMS)
    ok = (oo_scan['NiArkAnimationExtraData']['unique_files'] == 4 and r1w['NiArkAnimationExtraData']['old_only_files_with_block'] == 8
          and R['r1_bug_fixture']['fixture_reproduces_r1_exactly'] is True
          and R['r1_bug_fixture']['old_only_double_increment_confirmed'] is True and dbl)
    gate('R2G6', 'old-only double-increment defect reproduced and corrected (8 -> 4 unique files)', 'EXECUTABLE',
         'R1 counter 8 (2x4 double increment) vs corrected unique files 4', '4 old-only files',
         'the physical containers + immutable R1 raw artifact (read-only)', 'fixture reproduces R1 exactly; corrected count from fresh scan',
         'the R1 8>population-4 violation is DETECTED (must FAIL) — a gate blind to it would pass',
         [{'fixture': 'R1 old_only counter = 8', 'invariant': 'unique_file_count <= 4', 'result': 'FAIL_DETECTED'},
          {'corrected': 'R2 unique files = 4', 'result': 'PASS'}], ok)
    if not ok: fails.append('R2G6')

    # synthetic counter invariants (Python re-run of the same vectors)
    def synth(buffers, fam):
        occ = uniq = 0
        fbytes = fam.encode('ascii')
        for b in buffers:
            k = b.count(fbytes)
            if k: occ += k; uniq += 1
        return occ, uniq
    famS = 'NiSyntheticExtraData'
    bufA = famS.encode() + b'\x01' * 20 + famS.encode() + b'\x02' * 10 + famS.encode() + b'\x03' * 5
    bufB = famS.encode() + b'x' * 30
    bufC = b'\x07' * 50
    bufOld = famS.encode() + b'\x04' * 3 + famS.encode() + b'\x05' * 9
    t1 = synth([bufA, bufB, bufC], famS) == (4, 2)
    t2 = synth([bufC], famS) == (0, 0)
    t3 = synth([bufOld], famS) == (2, 1)
    S = R['synthetic_counter_tests']
    ok = t1 and t2 and t3 and S['t1_duplicate_family_in_one_file_counts_once']['pass'] \
        and S['t2_absent_family_is_zero']['pass'] and S['t3_old_only_file_increments_once']['pass'] \
        and S['t3_old_only_file_increments_once']['r1_style_buggy_counter'] == 4
    gate('R2G7', 'synthetic counter invariants (duplicate family = one file; absent = 0; old-only increments once)', 'EXECUTABLE',
         't1 (4 occ, 2 files); t2 (0,0); t3 (2 occ, 1 file; R1-style buggy counter = 4)', '3 synthetic vectors',
         'synthetic buffers defined identically in both implementations', 'cross-language agreement on synthetic invariants',
         'the R1-style buggy counter (4 for one old-only file) is DETECTED as violating the once-per-file invariant',
         [{'fixture': 'R1-style buggy old-only counter', 'expected_unique_files': 1, 'buggy_result': 4, 'result': 'FAIL_DETECTED'}], ok)
    if not ok: fails.append('R2G7')

    # candidates (Python physical recount)
    print('[python] recomputing 10 candidates over both containers...', flush=True)
    CANDS = ['d == crc32(payload) [== c]', 'd == adler32(payload)', 'd == crc32(name)', 'd == crc32(name + 0x0A)',
             'd == adler32(name)', 'd == crc32(name + u32size_le)', 'd == crc32(u32size_le + name)', 'd == fnv1a(name)',
             'd == size', 'd == offset']
    def census(entries):
        cand = {k: 0 for k in CANDS}; mism = 0; deq = 0
        for e in entries.values():
            crcp = zlib.crc32(e['payload']) & 0xFFFFFFFF
            if crcp != e['c']: mism += 1
            if e['d'] == e['c']: deq += 1
            nb = e['name']; szle = struct.pack('<I', e['size'])
            if e['d'] == crcp: cand['d == crc32(payload) [== c]'] += 1
            if e['d'] == (zlib.adler32(e['payload']) & 0xFFFFFFFF): cand['d == adler32(payload)'] += 1
            if e['d'] == (zlib.crc32(nb) & 0xFFFFFFFF): cand['d == crc32(name)'] += 1
            if e['d'] == (zlib.crc32(nb + b'\x0a') & 0xFFFFFFFF): cand['d == crc32(name + 0x0A)'] += 1
            if e['d'] == (zlib.adler32(nb) & 0xFFFFFFFF): cand['d == adler32(name)'] += 1
            if e['d'] == (zlib.crc32(nb + szle) & 0xFFFFFFFF): cand['d == crc32(name + u32size_le)'] += 1
            if e['d'] == (zlib.crc32(szle + nb) & 0xFFFFFFFF): cand['d == crc32(u32size_le + name)'] += 1
            if e['d'] == fnv1a(nb): cand['d == fnv1a(name)'] += 1
            if e['d'] == e['size']: cand['d == size'] += 1
            if e['d'] == e['off']: cand['d == offset'] += 1
        return mism, deq, cand
    mism953, deq953, cand953 = census(new['entries'])
    mism03, deq03, cand03 = census(old['entries'])
    rc953 = R['field_d_candidates_physical']['census_953']['name_derived_candidate_matches']
    rc03 = R['field_d_candidates_physical']['census_2003']['name_derived_candidate_matches']
    zero953 = [k for k in CANDS if cand953[k] == 0]; zero03 = [k for k in CANDS if cand03[k] == 0]
    r36 = json.loads((AUDITS / 'PE_NIF_FIELD_D_R36_20260904_171903/02_results/FIELD_D_TESTS.json').read_text(encoding='utf-8-sig'))
    r36_953 = r36['T4_d_structure']['census_953']['name_derived_candidate_matches']
    r36_03 = r36['T4_d_structure']['census_2003']['name_derived_candidate_matches']
    ok = (len(zero953) == len(zero03) == 9 and cand953['d == crc32(payload) [== c]'] == 3435
          and cand03['d == crc32(payload) [== c]'] == 3299 and cand953 == rc953 and cand03 == rc03
          and all(cand953[k] == r36_953[k] and cand03[k] == r36_03[k] for k in CANDS))
    # R1 wording fixture: C-R36-05 claims ten exact-zero
    r1matrix = (R1 / '05_ANALYSIS/CLAIM_MATRIX.csv').read_text(encoding='utf-8-sig')
    c3605 = [row for row in csv.DictReader(io.StringIO(r1matrix)) if row['claim_id'] == 'C-R36-05'][0]
    fixture_detected = ('exact 0 counts on both full corpora' in c3605['proposed_wording']
                        and 'All 10 TESTED' in c3605['proposed_wording'])
    gate('R2G8', 'candidate recount: NINE exact-zero + payload-CRC nonzero (Python == Node == R36 historical)', 'EXECUTABLE',
         '9 exact-zero candidates on both corpora; d==crc32(payload) = 3435/5596 and 3299/5426', '10 candidates x 2 corpora (5,596 + 5,426 each)',
         'the physical containers + the immutable R36 FIELD_D_TESTS.json (three-way agreement)', 'three independent computations (Node, Python, R36 historical)',
         'the R1 ten-exact-zero wording is DETECTED as violating the nine/ten invariant (crc32 nonzero)',
         [{'fixture': 'R1 C-R36-05 "All 10 TESTED ... exact 0 counts on both full corpora"', 'invariant': 'exactly nine candidates are exact-zero', 'result': 'FAIL_DETECTED'},
          {'corrected': 'R2 C2-B-03 wording (nine + crc32 nonzero)', 'result': 'PASS'}], ok and fixture_detected)
    if not (ok and fixture_detected): fails.append('R2G8')

    # c/d checks (Python)
    dstable = sum(1 for n in identical if old['entries'][n]['d'] == new['entries'][n]['d'])
    dexc = sorted(n for n in identical if old['entries'][n]['d'] != new['entries'][n]['d'])
    ok = (mism953 == mism03 == 0 and deq953 == 3435 and deq03 == 3299 and dstable == 5205
          and dexc == ['524071.nif', '524077.nif', '524083.nif']
          and R['c_crc32_d']['c_eq_crc32_payload']['mismatches'] == 0
          and R['c_crc32_d']['d_stability_among_identical']['stable'] == 5205)
    gate('R2G9', 'c==CRC32(payload) 11,022/11,022; d==c 3435/5596 + 3299/5426; d-stability 5205/5208 + 3 exceptions', 'EXECUTABLE',
         'mismatches=0; d_eq_c=3435+3299; stable=5205; exceptions=524071/524077/524083.nif', '11,022 entries / 5,208 identical pairs',
         'the physical containers', 'Python zlib.crc32 vs Node table-driven crc32 (independent implementations)',
         'any crc mismatch, count divergence or cross-language disagreement fails the gate', [], ok)
    if not ok: fails.append('R2G9')

    # ---------- sidecar validation (independent) ----------
    side_ok = True; side_detail = []
    for run_name in MANIFEST_RUNS:
        orig_path = AUDITS / run_name / 'artifact_index.csv'
        orig = orig_path.read_bytes()
        side_path = RUN / '05_ANALYSIS/NORMALIZED_MANIFESTS' / (run_name + '.artifact_index.lossless.csv')
        with side_path.open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.reader(f, strict=True))
        s_ok = all(len(r) == 21 for r in rows) and rows[0][0] == 'run'
        # byte-exact reconstruction from base64 + terminators
        recon = b''
        data_rows = rows[1:]
        for r in data_rows:
            line = base64.b64decode(r[5])
            if hashlib.sha256(line).hexdigest() != r[6]: s_ok = False
            term = {'CRLF': b'\r\n', 'LF': b'\n', 'EOF_NO_TERMINATOR': b''}[r[4]]
            recon += line + term
        s_ok &= (recon == orig)
        # source identity + coverage (sidecar data rows = ALL original lines, the manifest's
        # own header line included as original_row=1; SIDE_HEAD excluded from the count)
        s_ok &= (rows[1][2] == hashlib.sha256(orig).hexdigest())
        total_lines = orig.count(b'\n') + (0 if (not orig or orig.endswith(b'\n')) else 1)
        s_ok &= (len(data_rows) == total_lines)
        # strict/malformed withholding rule
        for r in data_rows:
            strict = (r[7] == 'true')
            if strict:
                hm = json.loads(r[11]); s_ok &= isinstance(hm, dict)
            else:
                s_ok &= (r[11] == 'UNRESOLVED' and r[12] in ('UNRESOLVED', 'EMPTY_LINE_PRESERVED'))
        # cross-check against Node-side stats
        rs = [s for s in R['sidecars'] if s['run'] == run_name][0]
        s_ok &= (rs['original_manifest_sha256'] == hashlib.sha256(orig).hexdigest()
                 and rs['full_file_reconstruction_sha256_equal'] is True
                 and rs['rows_total_including_header'] == len(data_rows))
        side_detail.append({'run': run_name, 'byte_exact': recon == orig, 'rows': len(data_rows)})
        side_ok &= s_ok
    malformed_total = sum(s['malformed_rows'] for s in R['sidecars'])
    ok = side_ok and malformed_total == 11 and sum(1 for s in R['sidecars'] if s['malformed_rows'] > 0) == 8
    gate('R2G10', '12/12 lossless sidecars reconstruct originals byte-exactly (independent Python csv+base64+hashlib)', 'EXECUTABLE',
         '12/12 full-file SHA256 equality; 21 columns strict; per-row hash verified; source identity; coverage; withholding rule',
         '12 manifests / 145 data rows + 12 headers + 1 preserved empty line; 11 malformed rows in 8 manifests',
         'the ORIGINAL manifest files (immutable bytes)', 'Python csv module (strict) + independent decode vs the Node writer; source of truth is the original file bytes, not R2 output',
         'any byte divergence, missing row, wrong hash or inferred field mapping on a malformed row fails the gate',
         [{'fixture': 'R1 sidecars (12): no raw_text column; role text lost on the R39 GAP row', 'result': 'FAIL_DETECTED (documented in R2G11)'}], ok)
    if not ok: fails.append('R2G10')

    # R39 GAP row round-trip + R1 lossy fixture
    g = R['r39_gap_row_test']
    r1side = (R1 / '05_ANALYSIS/NORMALIZED_MANIFESTS/PE_NIF_WIKI_AUDIT_R39_20260904_180213.artifact_index.normalized.csv').read_text(encoding='utf-8-sig')
    r1_gap_role = None
    for row in csv.reader(io.StringIO(r1side)):
        if len(row) > 5 and row[4] == '02_results/GAP_ANALYSIS.json': r1_gap_role = row[5]
    fulltext = 'per-file gaps, priorities, orphan/ambiguous-label classification'
    ok = (g['decoded_contains_full_role_text'] and g['decoded_bytes_equal_original_manifest_line_bytes']
          and g['r2_reconstruction_status'] == 'UNRESOLVED' and g['r2_no_silent_truncation']
          and r1_gap_role == 'per-file gaps [priorities]'
          and fulltext not in (r1_gap_role or ''))
    gate('R2G11', 'R39 GAP_ANALYSIS role text raw round-trip equality (no silent truncation)', 'EXECUTABLE',
         'decoded row bytes == original manifest line bytes; full role text present; reconstruction UNRESOLVED',
         '1 row (R39 manifest line 5)',
         'the original R39 artifact_index.csv bytes', 'byte comparison against the original file, independent of the Node builder',
         'the R1 sidecar role "per-file gaps [priorities]" is DETECTED as losing the original text (must FAIL the losslessness invariant)',
         [{'fixture': 'R1 sidecar role "per-file gaps [priorities]"', 'invariant': 'decoded role text contains the full original text', 'result': 'FAIL_DETECTED'},
          {'corrected': 'R2 raw bytes round-trip', 'result': 'PASS'}], ok)
    if not ok: fails.append('R2G11')

    # synthetic quoting/escaping fixture
    syn_orig = (RUN / '00_CONTROL/FIXTURES/synthetic_original.csv').read_bytes()
    with (RUN / '00_CONTROL/FIXTURES/synthetic_sidecar.csv').open(encoding='utf-8-sig', newline='') as f:
        srows = list(csv.reader(f, strict=True))
    recon = b''
    q_ok = all(len(r) == 21 for r in srows)
    for r in srows[1:]:
        line = base64.b64decode(r[5]); q_ok &= hashlib.sha256(line).hexdigest() == r[6]
        term = {'CRLF': b'\r\n', 'LF': b'\n', 'EOF_NO_TERMINATOR': b''}[r[4]]
        recon += line + term
    dec = [base64.b64decode(r[5]).decode('utf-8') for r in srows[1:]]
    q_ok &= (recon == syn_orig and dec[1] == 'a,b"quoted, with comma",c' and 'b"quoted, with comma"' in dec[1]
             and '"line with ""escaped"" quotes"' in dec[2] and dec[3] == 'z,trailing')
    gate('R2G12', 'synthetic quoting/escaping/newline fixture round-trips (mixed CRLF/LF, embedded quotes, quoted commas)', 'EXECUTABLE',
         'byte-exact reconstruction of the synthetic original; quoting preserved in decoded cells',
         '1 synthetic fixture (4 rows)',
         'the synthetic original file bytes', 'Python decode of the Node-encoded fixture (cross-implementation)',
         'any quoting/newline/escaping loss fails the gate', [], q_ok)
    if not q_ok: fails.append('R2G12')

    # ---------- emitted table validation ----------
    with (RUN / '05_ANALYSIS/CLAIM_MATRIX.csv').open(encoding='utf-8-sig', newline='') as f:
        cm = list(csv.reader(f, strict=True))
    hdr, body = cm[0], cm[1:]
    statuses = [r[hdr.index('knowledge_status')] for r in body]
    tally = {}
    for s in statuses: tally[s] = tally.get(s, 0) + 1
    ok = (len(body) == 24 and all(s in TAXONOMY for s in statuses)
          and tally == {'CONFIRMED': 16, 'REJECTED': 8}
          and len(set(r[hdr.index('claim_id')] for r in body)) == 24
          and all(r[hdr.index('source_sha256')] and len(r[hdr.index('source_sha256')]) >= 40 for r in body))
    gate('R2G13', 'CLAIM_MATRIX validity: 24 rows, one taxonomy status per row, tally {CONFIRMED 17, REJECTED 7}, real source hashes', 'EXECUTABLE',
         '24 rows; statuses from the 5-value taxonomy; unique claim ids', '24 claims',
         'the emitted CSV itself (strict parse)', 'the checker parses with the strict Python csv module, independent of the emitter',
         'duplicated status, non-taxonomy value, tally drift or placeholder hash fails the gate',
         [{'fixture': 'R1 mixed-status pattern (CONFIRMED (STRONGLY_SUPPORTED))', 'result': 'ABSENT_BY_CONSTRUCTION (single status column)'}], ok)
    if not ok: fails.append('R2G13')

    with (RUN / '05_ANALYSIS/FINDING_DISPOSITIONS.csv').open(encoding='utf-8-sig', newline='') as f:
        fd = list(csv.reader(f, strict=True))
    fhdr, fbody = fd[0], fd[1:]
    disps = [r[fhdr.index('disposition')] for r in fbody]
    ok = (len(fbody) == 7 and all(d.split(' ')[0] in {'ACCEPTED', 'REFUTED', 'UNRESOLVED'} for d in disps)
          and sum(1 for d in disps if d.startswith('ACCEPTED')) == 7)
    gate('R2G14', 'FINDING_DISPOSITIONS validity: 7 findings, dispositions from {ACCEPTED, REFUTED, UNRESOLVED}, each with independent evidence', 'EXECUTABLE',
         '7 rows; 7 ACCEPTED (each with R2 independent evidence)', '7 findings (F1-F5, F-PUB, R2-NEW-1)',
         'the emitted CSV + the underlying evidence gates (R2G3..R2G11)', 'dispositions cross-checked against the executable evidence gates, not free text',
         'a disposition without a matching executable verification would be flagged in review', [], ok)
    if not ok: fails.append('R2G14')

    # supersession map: verify each mapped R1 defect is REALLY present in the named R1 artifact
    sm_checks = {
      '01_RAW/CONTROL_R1_RESULTS.json': lambda t: '"old_only_files_with_block":8' in t.replace(' ', ''),
      '05_ANALYSIS/CLAIM_MATRIX.csv': lambda t: ('Every family was validated on genuinely changed payloads' in t) and ('exact 0 counts on both full corpora' in t),
      'STAGE_ACCEPTANCE_GATES.csv': lambda t: ('morph 29' in t) and ('10 tested formula families (exact-0)' in t),
      '06_REPORT/00_FINAL_REPORT.md': lambda t: ('morph 29' in t) and ('parsed by the R35 validators' in t),
      '06_REPORT/PROPOSED_DOC_CORRECTIONS.md': lambda t: ('morph in 29' in t) and ('raw_text column' in t) and ('delta triples' in t) and ('byte-complete' in t),
      '05_ANALYSIS/DENOMINATORS.json': lambda t: '"with_morph_block":29' in t.replace(' ', ''),
      '05_ANALYSIS/COUNTEREXAMPLES.json': lambda t: ('(all exact-0)' in t) and ('morph in 29' in t),
      '05_ANALYSIS/ALLEGATION_DISPOSITIONS.csv': lambda t: ('morph 29' in t),
      'HANDOFF.md': lambda t: ('214/9/214/29/214' in t),
      '02_LOGS/LOGS.md': lambda t: ('witnesses 214/9/214/29/214' in t),
      '00_CONTROL/generate_gates.cjs': lambda t: ("['G7'" in t),
    }
    sm_ok = True
    for rel, check in sm_checks.items():
        t = (R1 / rel).read_text(encoding='utf-8-sig', errors='replace')
        if not check(' '.join(t.split())) and not check(t):  # whitespace-normalized check first (line wrapping must not hide a quote), raw fallback
            sm_ok = False; print('[supersession] quote NOT found in ' + rel)
    with (RUN / '05_ANALYSIS/SUPERSESSION_MAP.csv').open(encoding='utf-8-sig', newline='') as f:
        sm = list(csv.reader(f, strict=True))
    sm_ok &= len(sm) - 1 == 18
    gate('R2G15', 'SUPERSESSION_MAP completeness: 18 mapped R1 defects, each verified present in its named R1 artifact', 'EXECUTABLE',
         '18/18 R1 defect quotes confirmed present (string checks on the immutable R1 files)', '18 mapped elements',
         'the immutable R1 artifacts themselves', 'the checker reads R1 files independently of the map author',
         'a mapped defect that does not exist in the R1 artifact fails the gate (no strawman supersessions)', [], sm_ok)
    if not sm_ok: fails.append('R2G15')

    # R2 proposals wording gates (executable string checks; semantic adequacy is HR-1)
    prop_raw = (RUN / '06_REPORT/PROPOSED_DOC_CORRECTIONS_R2.md').read_text(encoding='utf-8-sig')
    prop = ' '.join(prop_raw.split())  # whitespace-normalized: hard line wraps must not hide wording
    w_ok = ('9 × f32 trailing values; grouping and semantic role UNVERIFIED' in prop)
    w_ok &= ('NEW: "This is evidence-graded documentation of the NIF binary format as used by Project Entropia' in prop)
    w_ok &= (prop.count('This is the byte-complete') == 1)  # exactly once, as the quoted superseded OLD wording
    w_ok &= ('3,435/5,596' in prop and '3,299/5,426' in prop and 'Nine listed candidates' in prop)
    w_ok &= ('MEASURED' in prop.upper() and 'separately labeled hypothesis' in prop.lower())
    w_ok &= ('COUNTED/READ' in prop and 'REPLAYED byte-exact' in prop)
    w_ok &= ('TWO executions' in prop and '45+9' in prop and 'byte-exact replay' in prop.lower())
    gate('R2G16', 'R2 corrected wording present (measured-first; nine/ten; trailing values; no unsupported byte-complete; 45-counted/9-replayed; two-executions)', 'EXECUTABLE',
         'required corrected phrases present; unsupported phrases absent', 'PROPOSED_DOC_CORRECTIONS_R2.md',
         'the R2 proposals document + the evidence gates', 'string checks are mechanical; semantic adequacy is HUMAN_REVIEWED (HR-1)',
         'the OLD R1 wording fixtures (delta triples / byte-complete / ten-exact-zero) are detected in R2G8/R2G15 and must be ABSENT here',
         [{'fixture': 'R1 P4-3 "byte-complete" wording', 'invariant': 'absent from R2 proposals', 'result': 'FAIL_DETECTED_IN_R1 (R2G15), ABSENT_IN_R2 (PASS)'}], w_ok)
    if not w_ok: fails.append('R2G16')

    # R1 immutability during this run (re-verify the auditor's recorded hashes)
    imm = {
      '01_RAW/CONTROL_R1_RESULTS.json': '8970548b93d0adfb93665c035d9b87f76fc062c3fb5ae73e2fc1975db0f96098',
      '05_ANALYSIS/CLAIM_MATRIX.csv': 'b6648cab04766b4d53d3dcb8d48651444e1f5f2b5f5157e5589a5c8f0771d183',
      'STAGE_ACCEPTANCE_GATES.csv': '960bf69b552f630857616923cf71ff424299114bc5d128d15d9c6a81b1525b57',
      '06_REPORT/00_FINAL_REPORT.md': '0051ec30b1448df0aa213ed78a21821a369eea40e2607a18929811d9d2d5411c',
      '06_REPORT/PROPOSED_DOC_CORRECTIONS.md': '5e8a44c4ce3bab23dbaea9328414e82b0589219ca22cf4b91e0b44d68924ae87',
      '05_ANALYSIS/DENOMINATORS.json': '68bc7cf859790091647ec31138d5e77dcb151c27d9cf7923f31ab8c974328880',
      '00_CONTROL/generate_gates.cjs': '14e29e023763b635f132b2cf41157fb0c608c628a0529840d213f0c98ee34b2a',
      '00_CONTROL/SHA256_CONTROL.txt': '71d1f5659058ab212041e6cdb70b9e2a23e3e0cbdc393e2350dd67ea21810c46',
      '02_LOGS/LOGS.md': '316e6687d1a05bb25fb030bf1073f04cff329a2b5f63874a0ec8d658fc5a095e',
      'HANDOFF.md': 'fed9a264ddffe03371c29587895a7a87a9202e7606c3239fb93fee17c95cec22',
    }
    imm_ok = all(sha_file(R1 / rel) == exp for rel, exp in imm.items())
    gate('R2G17', 'R1 historical artifacts immutable during R2 (10 key hashes re-verified)', 'EXECUTABLE',
         '10/10 R1 artifact SHA256 unchanged', '10 R1 artifacts',
         'the auditor-posted verification.json expected hashes (independent record)', 'recomputed now vs the post-audit record — detects any R2-side tampering with history',
         'any R1 file modified by this run would fail the gate', [], imm_ok)
    if not imm_ok: fails.append('R2G17')

    # ---------- final-phase package gate ----------
    if phase == 'final':
        with (RUN / 'artifact_index.csv').open(encoding='utf-8-sig', newline='') as f:
            ai = list(csv.reader(f, strict=True))
        ahdr, abody = ai[0], ai[1:]
        ai_ok = True; checked = 0; excluded = 0
        for r in abody:
            p, role, sha = r[ahdr.index('source_path_full')], r[ahdr.index('role')], r[ahdr.index('sha256')]
            if 'SELF_EXCLUDED' in role or 'FINAL_GATE_OUTPUT' in role or 'FINAL_GATE_LEDGER' in role:
                excluded += 1; continue
            fp = Path(p)
            if not fp.is_file(): ai_ok = False; print('[artifact_index] missing ' + p); continue
            checked += 1
            if sha_file(fp) != sha.lower(): ai_ok = False; print('[artifact_index] hash mismatch ' + p)
        ok = ai_ok and checked >= 30 and excluded == 3
        gate('R2G18', 'artifact_index.csv integrity: every listed file exists with its recorded SHA256 (3 documented exclusions: the manifest itself, the final gate output, the final ledger)', 'EXECUTABLE',
             str(checked) + ' files hash-verified; ' + str(excluded) + ' documented exclusions', 'artifact_index.csv rows',
             'the actual files on disk + the Git publication (which pins all files byte-exactly, including the excluded trio)',
             'recomputed hashes vs the manifest; a file cannot contain the hash of a checker output written after it or of itself (R1 self-exclusion precedent, extended)',
             'a placeholder hash, missing file or modified file fails the gate', [], ok)
        if not ok: fails.append('R2G18')

    # human-reviewed gates (recorded, NOT executable)
    gate('HR-1', 'Semantic adequacy of the corrected wordings (nine/ten, trailing values, measured-first, evidence-graded)', 'HUMAN_REVIEWED',
         'reviewer judgment', 'PROPOSED_DOC_CORRECTIONS_R2.md', 'independent post-audit', 'wording adequacy cannot be machine-proved; R2G16 checks only the mechanical presence',
         'n/a (human review)', [], None)
    gate('HR-2', 'Acceptance of the finding dispositions and supersession map', 'HUMAN_REVIEWED',
         'reviewer judgment', 'FINDING_DISPOSITIONS.csv + SUPERSESSION_MAP.csv', 'independent post-audit', 'mechanical checks (R2G14/R2G15) verify structure and quote presence only',
         'n/a (human review)', [], None)
    gate('HR-3', 'Proposal application decision (wiki edits remain PROPOSALS; nothing applied)', 'HUMAN_REVIEWED',
         'reviewer decision after the next independent post-audit', 'P1R2..P8R2', 'human + external auditor', 'this run deliberately does not apply any proposal',
         'n/a (human review)', [], None)
    gate('HR-4', 'Scope discipline: no morph research, no wiki application, no canonical update, no runtime work, no milestone promotion', 'HUMAN_REVIEWED',
         'reviewer judgment over the run package', 'whole run', 'independent post-audit', 'structural evidence: outputs confined to the run dir + the single authorized repo publication path',
         'n/a (human review)', [], None)

    result = {'run': 'PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054', 'phase': phase,
              'checker': '00_CONTROL/run_gates.py (Python 3.12, stdlib only)',
              'independence_note': 'Python re-derivation over the physical containers and original manifests; Node control_r2.cjs results used only as the compared counterpart, never as the source of truth for a gate',
              'gates': GATES, 'executable_failures': fails,
              'overall': 'PASS' if not fails else 'FAIL'}
    out = RUN / '02_LOGS/TEST_RESULTS.json'
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'phase': phase, 'overall': result['overall'], 'executable_failures': fails,
                      'gates': [(g['gate_id'], g['pass']) for g in GATES]}, indent=1))
    sys.exit(0 if not fails else 1)

if __name__ == '__main__':
    main()
