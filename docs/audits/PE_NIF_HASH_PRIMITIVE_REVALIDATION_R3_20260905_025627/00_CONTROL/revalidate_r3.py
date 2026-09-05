"""revalidate_r3.py — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3 main driver.

Executes the nine work items of the R3 revalidation prompt with deterministic
assertions and nonzero failure exit. WRITES ONLY inside this run dir
(01_RAW, 02_LOGS). READ-ONLY on: original game files, R2 package, historical
runs (R34/R35/R36/R39), shared tools. The historical R2 script is NOT
executed; only its extracted literal helper declarations run (inside
00_CONTROL/probe_r2_helpers.cjs, hash-pinned source, pure vm context).

Phase ordering is enforced: the KNOWN-ANSWER phase (prompt item 3) must PASS
before any corpus aggregation (item 4) happens; the process aborts nonzero
otherwise. Method classes are kept separate in every record:
  PHYSICAL_RECOMPUTATION / STAGE_LOCAL_REPRODUCTION / SOURCE_INSPECTION /
  HISTORICAL_RESUM / HISTORICAL_TRANSCRIPTION.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import re
import struct
import subprocess
import sys
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r3_primitives as rp  # noqa: E402

B = Path('D:/Eudoria_Reconstruction')
RUN = B / '99_Audits/PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627'
R2 = B / '99_Audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054'
R2SRC = R2 / '00_CONTROL/control_r2.cjs'
R2SRC_SHA = '666c378da43dd23b961252bdc091baf9b2c7df6b32268d002ed916b20018b59e'
PROMPT = B / '99_Audits/PE_NIF_R2_POST_AUDIT_20260905_025627/00_CONTROL/OPENCODE_REVALIDATION_PROMPT.md'
PROMPT_SHA = '662D4C522A570D210549618BFEE7D27ACBC0253F39034C005C2678BDE389D35C'
BNT_953 = B / 'pcg_install/Data/Models/Models.bnt'
BNT_2003 = B / '01_Original_Files/BNT_Models/Models.bnt'
BNT_953_SHA = 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0'
BNT_2003_SHA = '1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353f1cefd3524a6'
R34 = B / '99_Audits/PE_NIF_MORPH_QUANT_R34_20260904_164538/02_results/REAL_SPARSE_GRAMMAR.json'
R34_SHA = '2c26ba86db44ad7a58322c136112fec36e23efab1db1fafea1c976311eba007e'
R35_REPORT = B / '99_Audits/PE_NIF_CROSS_ERA_R35_20260904_170224/REPORT.md'
R36_TESTS = B / '99_Audits/PE_NIF_FIELD_D_R36_20260904_171903/02_results/FIELD_D_TESTS.json'
SIDE_DIR = R2 / '05_ANALYSIS/NORMALIZED_MANIFESTS'
PY = str(B / '10_Scripts/python_env/python.exe')
NODE = r'C:/Program Files/nodejs/node.exe'

RAW = RUN / '01_RAW'
LOG = RUN / '02_LOGS'
GATES: list = []
T0 = time.time()
LOG_LINES: list = []


def log(msg):
    line = time.strftime('%H:%M:%S') + ' ' + msg
    print(line, flush=True)
    LOG_LINES.append(line)


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def jload(p: Path):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def jwrite(rel: str, obj) -> Path:
    p = RUN / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1) + '\n', encoding='utf-8')
    log('WROTE ' + rel + ' (' + str(p.stat().st_size) + ' B)')
    return p


def gate(gid, name, measured, denominator, truth, noncirc, failure, method_class, ok):
    """Three-state gate (R3 repair of R2's bool(None)->false/FAIL defect)."""
    state = rp.three_state(ok)
    GATES.append({
        'gate_id': gid, 'gate_name': name,
        'gate_type': 'HUMAN_REVIEWED' if ok is None else 'EXECUTABLE',
        'measured_quantity': measured, 'denominator': denominator,
        'independent_source_of_truth': truth, 'why_non_circular': noncirc,
        'failure_case_detected': failure, 'method_class': method_class,
        'state': state, 'pass': None if ok is None else bool(ok),
    })
    return ok


def custom_parse(text: str):
    """RFC4180-style state machine under the CUSTOM PHYSICAL-LINE contract:
    the record is the given raw row bytes; a bare CR inside them is an
    ordinary character (same semantics as the R2 builder's csvParse,
    control_r2.cjs L39-45)."""
    fields = []
    s = []
    quoted = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '"':
            if quoted and i + 1 < n and text[i + 1] == '"':
                s.append('"')
                i += 1
            else:
                quoted = not quoted
        elif ch == ',' and not quoted:
            fields.append(''.join(s))
            s = []
        else:
            s.append(ch)
        i += 1
    fields.append(''.join(s))
    return fields


# =========================================================================
# Phase 0 — identity pins
# =========================================================================
log('PHASE 0 identity pins')
ok_prompt = sha_file(PROMPT).lower() == PROMPT_SHA.lower()
gate('R3G1', 'execution prompt SHA256 verified', 'SHA256 of OPENCODE_REVALIDATION_PROMPT.md',
     '1 prompt file', 'the prompt file itself (physical)', 'hash recomputation, not a stored value',
     'any byte change in the prompt fails the gate', 'PHYSICAL_RECOMPUTATION', ok_prompt)
if not ok_prompt:
    log('FATAL: prompt hash mismatch')
    sys.exit(3)

ok_r2src = sha_file(R2SRC) == R2SRC_SHA
gate('R3G3a', 'R2 source hash-pin verified before literal extraction',
     'SHA256 of R2 00_CONTROL/control_r2.cjs', '1 source file',
     'the pinned R2 artifact + the external post-audit record of the same pin',
     'independent recomputation; the pin is asserted, not trusted',
     'a modified R2 control source fails extraction and the gate', 'PHYSICAL_RECOMPUTATION', ok_r2src)
if not ok_r2src:
    log('FATAL: R2 source hash-pin mismatch')
    sys.exit(3)

ok34 = sha_file(R34) == R34_SHA
gate('R3G12pin', 'R34 per_span source hash-pin', 'SHA256 of R34 REAL_SPARSE_GRAMMAR.json',
     '1 source file', 'the external post-audit record of the same pin',
     'recomputation', 'a modified R34 result file fails the re-sum gate', 'PHYSICAL_RECOMPUTATION', ok34)


# =========================================================================
# Phase 1 — KNOWN-ANSWER tests BEFORE corpus aggregation (prompt item 3)
# =========================================================================
log('PHASE 1 known-answer tests (before any corpus aggregation)')

KAT_SETS = ['corrected', 'oracle_self_vectors', 'r2_literal_python',
            'wrong_value_controls', 'three_state_corrected', 'three_state_r2_coercion']
kat_runs = {}
for s in KAT_SETS:
    outp = LOG / ('kat_' + s + '.json')
    proc = subprocess.run([PY, str(RUN / '00_CONTROL/run_kats.py'), '--set', s,
                           '--out', str(outp)], capture_output=True, text=True)
    body = jload(outp) if outp.is_file() else {}
    kat_runs[s] = {'exit_code': proc.returncode, 'all_pass': body.get('all_pass'), 'body': body}
    log('KAT set %s exit=%s all_pass=%s' % (s, proc.returncode, body.get('all_pass')))

ok_kat = kat_runs['corrected']['exit_code'] == 0 and kat_runs['corrected']['all_pass'] is True
gate('R3G4', 'corrected-primitive KAT suite PASSES before corpus aggregation',
     '14 KAT vectors (empty/single/multi/binary/zero-high-byte/overflow-sensitive/repeated/'
     'incremental) + 4 streaming-carry identity checks',
     '14 vectors / 4 incremental checks', 'zlib (C library) + published constants (RFC1950 init=1, '
     'CRC-32 check value 0xCBF43926, FNV vectors 0x811C9DC5/0xE40C292C/0xBF9CF968/0x4F9F2CAB)',
     'own spec implementation vs C oracle vs published constants: three independent sources',
     'any single vector mismatch aborts the run BEFORE aggregation (nonzero exit)',
     'EXECUTABLE', ok_kat)

ok_oracle = kat_runs['oracle_self_vectors']['exit_code'] == 0 and \
    kat_runs['oracle_self_vectors']['all_pass'] is True
gate('R3G5', 'oracles validated against their own published vectors',
     'zlib.adler32("Wikipedia")==0x11E60398; zlib.crc32("123456789")==0xCBF43926; '
     'fnv exact-int("")/("a")/("foobar")/("hello") == published vectors',
     '8 oracle self-vector checks', 'published constants (RFC + canonical CRC check value)',
     'the oracle is compared to constants written independently of the oracle',
     'an oracle disagreeing with its published constant fails the gate (and aborts aggregation)',
     'EXECUTABLE', ok_oracle)

nc_r2py = kat_runs['r2_literal_python']
ok_nc_r2py = nc_r2py['exit_code'] != 0 and nc_r2py['all_pass'] is False
gate('R3G6a', 'negative control: unchanged R2 adler32 semantics FAIL the KAT predicates',
     'exit_code=%s; failed predicates: %s' % (nc_r2py['exit_code'],
        sorted({p for v in nc_r2py['body'].get('vectors', []) for p in v['failed_predicates']})),
     '14 KAT vectors', 'zlib oracle + published constants (the same predicates the corrected set passes)',
     'the control runs the SAME predicates; detection is the required outcome',
     'adler32("")=0x00010000!=1, adler32("a")=0x00620061!=0x00620062 (reproduced)',
     'STAGE_LOCAL_REPRODUCTION', ok_nc_r2py)
# characterization: the exact-int transcription of R2 fnv PASSES the fnv KATs —
# the fnv defect is arithmetic (float64), not formula-shape; the float defect is
# reproduced only by the executed Node literal (R3G6b).

nc_wrong = kat_runs['wrong_value_controls']
ok_nc_wrong = nc_wrong['exit_code'] != 0 and nc_wrong['all_pass'] is False
gate('R3G7a', 'negative control: deliberately wrong-value primitives FAIL the KAT predicates',
     'exit_code=%s; failed predicates: %s' % (nc_wrong['exit_code'],
        sorted({p for v in nc_wrong['body'].get('vectors', []) for p in v['failed_predicates']})),
     '14 KAT vectors', 'zlib oracle + published constants',
     'wrong values cannot pass value identity even when aggregate counts are preserved (R3G7b)',
     'adler32_wrong_xor("")=0x5A5A5A5B!=1; fnv1a_wrong_basis("a")!=0xE40C292C',
     'EXECUTABLE', ok_nc_wrong)

nc_ts = kat_runs['three_state_r2_coercion']
ok_nc_ts = nc_ts['exit_code'] != 0 and nc_ts['all_pass'] is False
failed_pred = [c['predicate'] for c in nc_ts['body'].get('cases', []) if not c['pass']]
gate('R3G8a', 'negative control: pending-as-false serialization DETECTED (R2 bool(ok) coercion)',
     'exit_code=%s; failed predicates: %s; serialize(None) actually returned %r' % (
         nc_ts['exit_code'], failed_pred, rp.bool_coerce(None)),
     '3 predicates (None/True/False)', "the R2 run_gates.py L50 behavior 'pass': bool(ok)",
     'the control applies the corrected predicates to the historical coercion',
     "bool(None)->False serializes PENDING human review as FAIL (R2 TEST_RESULTS.json HR-1..4=false, CSV FAIL)",
     'STAGE_LOCAL_REPRODUCTION', ok_nc_ts)

ok_ts = kat_runs['three_state_corrected']['exit_code'] == 0 and \
    kat_runs['three_state_corrected']['all_pass'] is True
gate('R3G8b', 'corrected three-state serializer passes the same predicates',
     "three_state(None)='PENDING', three_state(True)='PASS', three_state(False)='FAIL'",
     '3 predicates', 'the predicate set itself (None/True/False distinct states)',
     'same predicates as the failed control; only the serializer differs',
     'any state collapse (pending->fail) fails the gate',
     'EXECUTABLE', ok_ts)

# ---------- Node probe: execute the ACTUAL extracted R2 literals ----------
log('PHASE 1b Node probe (actual R2 literal declarations executed, hash-pinned source)')
probe_path = RAW / 'R2_HELPER_PROBE.json'
proc = subprocess.run([NODE, str(RUN / '00_CONTROL/probe_r2_helpers.cjs'), str(probe_path)],
                      capture_output=True, text=True)
log('probe exit=%s' % proc.returncode)
if proc.returncode != 0 or not probe_path.is_file():
    log('FATAL: probe failed: ' + (proc.stderr or '')[:400])
    sys.exit(3)
probe = jload(probe_path)

ok_probe_pin = probe['provenance']['r2_source_sha_pin_verified'] is True
declarations = probe['provenance']['extraction']
DECL_ADLER = ('function adler32(b) { let a = 1, s = 0; for (let i = 0; i < b.length; i++) '
              '{ s = (s + b[i]) % 65521; a = (a + s) % 65521; } return ((a << 16) | s) >>> 0; }')
DECL_FNV = ('function fnv1a(b) { let x = 0x811C9DC5; for (let i = 0; i < b.length; i++) '
            'x = ((x ^ b[i]) * 0x01000193) >>> 0; return x >>> 0; }')
ok_decl = (len(declarations) == 5
           and declarations[3] == DECL_ADLER and declarations[4] == DECL_FNV
           and declarations[0].startswith('function crc32(')
           and declarations[1].startswith('const CRC_T')
           and declarations[2].startswith('for (let n'))
gate('R3G3b', 'literal extraction from the hash-pinned R2 source (declarations recorded byte-exact)',
     '5 unique line-prefix extractions incl. both defect-relevant declarations',
     '5 snippets', 'the hash-pinned source + the external post-audit verification.json record '
     'of the same two declarations',
     'extraction is prefix-unique on the pinned bytes; the executed code is quoted in the evidence',
     'non-unique or altered extraction fails the gate',
     'STAGE_LOCAL_REPRODUCTION', ok_probe_pin and ok_decl)

# defect reproduction against the ACTUAL executed bytes (prompt item 1):
# counterexamples TESTED, not accepted blindly.
pk = {v['id']: v for v in probe['kat_vectors']}
defect = {
    'adler_empty_r2': '%08x' % pk['V01_empty']['r2_adler'],
    'adler_a_r2': '%08x' % pk['V02_a']['r2_adler'],
    'adler_hello_r2': '%08x' % pk['V03_hello']['r2_adler'],
    'fnv_hello_r2': '%08x' % (pk['V03_hello']['r2_fnv'] & 0xFFFFFFFF),
    'fnv_548296_r2': '%08x' % (pk['V07_name_548296']['r2_fnv'] & 0xFFFFFFFF),
    'adler_empty_correct': '%08x' % pk['V01_empty']['corrected_adler'],
    'adler_a_correct': '%08x' % pk['V02_a']['corrected_adler'],
    'adler_hello_correct': '%08x' % pk['V03_hello']['corrected_adler'],
    'fnv_hello_correct': '%08x' % pk['V03_hello']['corrected_fnv'],
    'fnv_548296_correct': '%08x' % pk['V07_name_548296']['corrected_fnv'],
}
expected_defect = {
    'adler_empty_r2': '00010000', 'adler_a_r2': '00620061', 'adler_hello_r2': '06280214',
    'fnv_hello_r2': 'a82fb4a1', 'fnv_548296_r2': '200d96de',
    'adler_empty_correct': '00000001', 'adler_a_correct': '00620062',
    'adler_hello_correct': '062c0215', 'fnv_hello_correct': '4f9f2cab',
    'fnv_548296_correct': '4e2b6736',
}
ok_defect = defect == expected_defect
gate('R3G6b', 'DEFECT REPRODUCED from the executed R2 literals (counterexamples tested, not assumed)',
     json.dumps(defect), '5 R2-value counterexamples + 5 corrected-reference values',
     'zlib + exact-int/BigInt references + published vectors (all independent of the R2 code)',
     'the R2 literals are executed from the hash-pinned bytes; expected values come from the oracles',
     'if the R2 literals produced the CORRECT values the prompt counterexamples would be falsified (gate fails)',
     'STAGE_LOCAL_REPRODUCTION', ok_defect)

ok_r2crc = all(v['r2_crc32'] == (zlib.crc32(bytes.fromhex(vec[1])) & 0xFFFFFFFF)
               for vec, v in zip(rp.KAT_VECTORS, probe['kat_vectors']) if vec[1])
gate('R3G6c', 'positive control: the R2 crc32 literal is NOT defective (defect census bounded)',
     'R2 crc32 == zlib.crc32 on all %d KAT vectors' % len(probe['kat_vectors']),
     '%d KAT vectors' % len(probe['kat_vectors']), 'zlib.crc32 (C oracle)',
     'the same executed-literal method that reproduced the adler/fnv defects',
     'a crc32 mismatch would widen the defect census and fail this gate',
     'STAGE_LOCAL_REPRODUCTION', ok_r2crc)

phase1_ok = all(g['state'] == 'PASS' for g in GATES if g['gate_type'] == 'EXECUTABLE')
if not phase1_ok:
    log('FATAL: PHASE 1 failed — corpus aggregation NOT executed')
    jwrite('02_LOGS/TEST_RESULTS_ABORT.json', {'phase': '1', 'gates': GATES})
    sys.exit(3)
log('PHASE 1 PASS — aggregation authorized')


# =========================================================================
# Phase 2 — corpus aggregation (prompt item 4) — physical recomputation
# =========================================================================
log('PHASE 2 corpus parse + per-entry value comparison')


def parse_bnt(p: Path):
    b = p.read_bytes()
    mv = memoryview(b)
    start = struct.unpack_from('<I', b, len(b) - 8)[0]
    assert 0 < start < len(b) - 8, 'bad index start'
    count = struct.unpack_from('<I', b, start)[0]
    pos = start + 4
    entries = {}
    order = []
    for _ in range(count):
        end = b.index(b'\n', pos)
        assert end < len(b) - 8, 'bad name terminator'
        name = b[pos:end].decode('ascii')
        size, off, c, d = struct.unpack_from('<IIII', b, end + 1)
        assert name not in entries, 'duplicate name'
        assert off + size <= start, 'payload overruns index'
        entries[name] = {'size': size, 'off': off, 'c': c, 'd': d,
                         'name_bytes': b[pos:end], 'payload': mv[off:off + size]}
        order.append(name)
        pos = end + 17
    assert pos == len(b) - 8, 'index consumption not exact'
    assert len(entries) == count, 'count mismatch'
    return {'sha256': hashlib.sha256(b).hexdigest(), 'size': len(b),
            'entries': entries, 'order': order}


t = time.time()
c953 = parse_bnt(BNT_953)
c2003 = parse_bnt(BNT_2003)
log('parsed both containers in %.1fs' % (time.time() - t))

ok_src = c953['sha256'] == BNT_953_SHA and c2003['sha256'] == BNT_2003_SHA
gate('R3G2', 'physical source identity (both Models.bnt SHA256)',
     'SHA256 of both containers (Python parser + Node probe agree)', '2 containers',
     'the physical game files', 'fresh recomputation in two independent parsers',
     'a modified/replaced container fails the gate', 'PHYSICAL_RECOMPUTATION', ok_src)
if not ok_src:
    sys.exit(3)

ERAS = [('pcg_953', c953, probe['census']['pcg_953']),
        ('era_2003', c2003, probe['census']['era_2003'])]

join_ok = True
join_checked = 0
for era, cont, pc in ERAS:
    if pc['n'] != len(cont['entries']):
        join_ok = False
        break
    for row in pc['rows']:
        e = cont['entries'].get(row[0])
        if e is None or (e['size'], e['off'], e['c'], e['d']) != tuple(row[12:16]):
            join_ok = False
            break
        join_checked += 1
gate('R3G9join', 'probe/Python corpus join identity (era+file+fields)',
     'per-entry (size,off,c,d) equality: %d/%d checked' % (join_checked, 5596 + 5426),
     '11,022 entries (5,596 + 5,426)', 'two independent parsers of the same physical containers',
     'the join is verified before any value comparison; keyed by era+file',
     'any field mismatch fails the comparison keying', 'PHYSICAL_RECOMPUTATION',
     join_ok and join_checked == 11022)
if not join_ok:
    sys.exit(3)

# ---------- per-entry computation (Python corrected/oracle legs) ----------
t = time.time()
per_entry = {}
sample_iter_adler = {'n': 0, 'bytes': 0, 'matches': 0}
sample_iter_crc = {'n': 0, 'bytes': 0, 'matches': 0}
big_names = set()
for cont in (c953, c2003):
    for n, _ in sorted(cont['entries'].items(), key=lambda kv: -kv[1]['size'])[:50]:
        big_names.add(n)
for era, cont, pc in ERAS:
    for idx, row in enumerate(pc['rows']):
        name = row[0]
        e = cont['entries'][name]
        nb = e['name_bytes']
        payload = e['payload']
        sz = struct.pack('<I', e['size'])
        vals = {
            'adler_name_zlib': zlib.adler32(nb) & 0xFFFFFFFF,
            'adler_name_iter': rp.adler32_rfc1950(nb),
            'adler_payload_zlib': zlib.adler32(payload) & 0xFFFFFFFF,
            'adler_payload_closed': rp.adler32_closed_form(payload),
            'crc_name_zlib': zlib.crc32(nb) & 0xFFFFFFFF,
            'crc_name_lf_zlib': zlib.crc32(nb + b'\n') & 0xFFFFFFFF,
            'crc_name_sz_zlib': zlib.crc32(nb + sz) & 0xFFFFFFFF,
            'crc_sz_name_zlib': zlib.crc32(sz + nb) & 0xFFFFFFFF,
            'crc_payload_zlib': zlib.crc32(payload) & 0xFFFFFFFF,
            'fnv_name_exact': rp.fnv1a_rfc9923(nb),
            'payload_sha256': hashlib.sha256(payload).hexdigest(),
            'size': e['size'], 'off': e['off'], 'c': e['c'], 'd': e['d'],
            'crc_name_own': rp.crc32_ieee(nb),
            'adler_name_r2_node': row[1], 'fnv_name_r2_node': row[2], 'crc_name_r2_node': row[3],
            'adler_payload_r2_node': row[4], 'crc_payload_r2_node': row[5],
            'crc_name_lf_r2_node': row[6], 'crc_name_sz_r2_node': row[7],
            'crc_sz_name_r2_node': row[8],
            'adler_name_node_corrected': row[9], 'adler_payload_node_corrected': row[10],
            'fnv_name_node_bigint': row[11],
        }
        per_entry[(era, name)] = vals
        # bounded iterative-spec validation sample (payloads)
        if e['size'] <= 32768 or name in big_names or idx % 97 == 0:
            sample_iter_adler['n'] += 1
            sample_iter_adler['bytes'] += e['size']
            if rp.adler32_rfc1950(payload) == vals['adler_payload_zlib']:
                sample_iter_adler['matches'] += 1
            sample_iter_crc['n'] += 1
            sample_iter_crc['bytes'] += e['size']
            if rp.crc32_ieee(payload) == vals['crc_payload_zlib']:
                sample_iter_crc['matches'] += 1
log('per-entry python legs computed in %.1fs (iterative sample: %d entries / %.1f MB)'
    % (time.time() - t, sample_iter_adler['n'], sample_iter_adler['bytes'] / 1e6))

DEN = len(per_entry)

# ---------- identity pass (corrected primitive == independent oracle, per entry) ----------
IDENT_KEYS = ['adler32(name)', 'adler32(payload)', 'fnv1a(name)', 'crc32(name)',
              'crc32(name+0x0A)', 'crc32(name+u32size_le)', 'crc32(u32size_le+name)',
              'crc32(payload)']
identity = {k: {'denominator': DEN, 'matches': 0, 'first_mismatches': []} for k in IDENT_KEYS}
for (era, name), v in per_entry.items():
    checks = {
        'adler32(name)': (v['adler_name_iter'] == v['adler_name_zlib']
                          and v['adler_name_node_corrected'] == v['adler_name_zlib']),
        'adler32(payload)': (v['adler_payload_closed'] == v['adler_payload_zlib']
                             and v['adler_payload_node_corrected'] == v['adler_payload_zlib']),
        'fnv1a(name)': v['fnv_name_exact'] == v['fnv_name_node_bigint'],
        'crc32(name)': (v['crc_name_r2_node'] == v['crc_name_zlib']
                        and v['crc_name_own'] == v['crc_name_zlib']),
        'crc32(name+0x0A)': v['crc_name_lf_r2_node'] == v['crc_name_lf_zlib'],
        'crc32(name+u32size_le)': v['crc_name_sz_r2_node'] == v['crc_name_sz_zlib'],
        'crc32(u32size_le+name)': v['crc_sz_name_r2_node'] == v['crc_sz_name_zlib'],
        'crc32(payload)': v['crc_payload_r2_node'] == v['crc_payload_zlib'],
    }
    for k, okv in checks.items():
        if okv:
            identity[k]['matches'] += 1
        elif len(identity[k]['first_mismatches']) < 5:
            identity[k]['first_mismatches'].append({'era': era, 'file': name})
identity['adler32(payload)_iterative_spec_sample'] = dict(sample_iter_adler)
identity['crc32(payload)_own_table_sample'] = dict(sample_iter_crc)

ok_identity = (all(identity[k]['matches'] == DEN for k in IDENT_KEYS)
               and sample_iter_adler['matches'] == sample_iter_adler['n']
               and sample_iter_crc['matches'] == sample_iter_crc['n'])
measured_identity = ('adler(name) %d/%d; adler(payload) closed==zlib==Node %d/%d '
                     '(iterative-spec sample %d/%d, %d bytes); fnv(name) exact==BigInt %d/%d; '
                     'crc32 candidates Node-literal==zlib+own-table %d/%d each '
                     '(name/lf/sz/szrev/payload)'
                     % (identity['adler32(name)']['matches'], DEN,
                        identity['adler32(payload)']['matches'], DEN,
                        sample_iter_adler['matches'], sample_iter_adler['n'],
                        sample_iter_adler['bytes'],
                        identity['fnv1a(name)']['matches'], DEN,
                        identity['crc32(payload)']['matches'], DEN))
gate('R3G9', 'per-entry primitive/input identity pass (corrected == oracle, every input)',
     measured_identity,
     '11,022 entries x 8 candidate input classes',
     'zlib (C), numpy closed form, Node Number/BigInt, own CRC table — independent implementations',
     'four independent implementations per defect-affected input class; none shares code with another',
     'any single-entry value mismatch fails the gate and blocks match-count derivation',
     'PHYSICAL_RECOMPUTATION', ok_identity)
if not ok_identity:
    sys.exit(3)

# ---------- R2-vs-corrected per-entry value comparison (complete mismatch census) ----------
r2_vs = {}
for cand, r2k, corrk in [
    ('adler32(name)', 'adler_name_r2_node', 'adler_name_zlib'),
    ('adler32(payload)', 'adler_payload_r2_node', 'adler_payload_zlib'),
    ('fnv1a(name)', 'fnv_name_r2_node', 'fnv_name_exact'),
    ('crc32(name)', 'crc_name_r2_node', 'crc_name_zlib'),
    ('crc32(name+0x0A)', 'crc_name_lf_r2_node', 'crc_name_lf_zlib'),
    ('crc32(name+u32size_le)', 'crc_name_sz_r2_node', 'crc_name_sz_zlib'),
    ('crc32(u32size_le+name)', 'crc_sz_name_r2_node', 'crc_sz_name_zlib'),
    ('crc32(payload)', 'crc_payload_r2_node', 'crc_payload_zlib'),
]:
    mism, coinc, examples = [], [], []
    for (era, name), v in per_entry.items():
        if v[r2k] != v[corrk]:
            mism.append(era + '|' + name)
            if len(examples) < 25:
                examples.append({'era': era, 'file': name, 'r2_value': '%08x' % v[r2k],
                                 'corrected_value': '%08x' % v[corrk]})
        else:
            coinc.append({'era': era, 'file': name, 'value': '%08x' % v[corrk]})
    r2_vs[cand] = {'denominator': DEN, 'r2_node_matches_corrected': DEN - len(mism),
                   'mismatches': len(mism), 'mismatch_census_keys': mism,
                   'bounded_examples': examples}
    if cand == 'fnv1a(name)':
        r2_vs[cand]['coincidence_census'] = coinc
    log('R2-vs-corrected %-24s mismatches %d/%d' % (cand, len(mism), DEN))

ok_census = (r2_vs['adler32(name)']['mismatches'] == DEN
             and r2_vs['adler32(name)']['r2_node_matches_corrected'] == 0
             and all(r2_vs[c]['mismatches'] == 0 for c in
                     ['crc32(name)', 'crc32(name+0x0A)', 'crc32(name+u32size_le)',
                      'crc32(u32size_le+name)', 'crc32(payload)']))
gate('R3G10', 'R2-vs-corrected per-entry value comparison recorded (complete mismatch census)',
     'adler32(name) %d/%d mismatches; adler32(payload) %d/%d; fnv1a(name) %d/%d mismatches '
     '(%d coincidences); all five crc32 candidates 0 mismatches (R2 crc32 correct)'
     % (r2_vs['adler32(name)']['mismatches'], DEN, r2_vs['adler32(payload)']['mismatches'], DEN,
        r2_vs['fnv1a(name)']['mismatches'], DEN, r2_vs['fnv1a(name)']['r2_node_matches_corrected']),
     '11,022 entries x 8 candidate input classes',
     'the executed R2 literals vs the corrected implementations (both recorded per entry)',
     'value comparison happens per entry BEFORE any match-count table is derived',
     'aggregate-only comparison would conceal these value mismatches — the P0 mechanism',
     'PHYSICAL_RECOMPUTATION', ok_census)

# ---------- match-count tables (ONLY AFTER identity pass) ----------
KEYS = ['d == crc32(payload) [== c]', 'd == adler32(payload)', 'd == crc32(name)',
        'd == crc32(name + 0x0A)', 'd == adler32(name)', 'd == crc32(name + u32size_le)',
        'd == crc32(u32size_le + name)', 'd == fnv1a(name)', 'd == size', 'd == offset']
census = {}
crc_dir_mismatch = {}
for era, cont, pc in ERAS:
    counts = dict.fromkeys(KEYS, 0)
    mism = 0
    for name, e in cont['entries'].items():
        v = per_entry[(era, name)]
        d = e['d']
        vals = {KEYS[0]: v['crc_payload_zlib'], KEYS[1]: v['adler_payload_zlib'],
                KEYS[2]: v['crc_name_zlib'], KEYS[3]: v['crc_name_lf_zlib'],
                KEYS[4]: v['adler_name_zlib'], KEYS[5]: v['crc_name_sz_zlib'],
                KEYS[6]: v['crc_sz_name_zlib'], KEYS[7]: v['fnv_name_exact'],
                KEYS[8]: e['size'], KEYS[9]: e['off']}
        for k in KEYS:
            if vals[k] == d:
                counts[k] += 1
        if v['crc_payload_zlib'] != e['c']:
            mism += 1
    census[era] = {'n': len(cont['entries']), 'name_derived_candidate_matches': counts}
    crc_dir_mismatch[era] = mism

# wrong-value aggregate preservation (negative control completion: R3G7b)
wrong_agg = {}
for era, cont, pc in ERAS:
    wc = {'d == adler32_wrong_xor(name)': 0, 'd == adler32_wrong_xor(payload)': 0,
          'd == fnv1a_wrong_basis(name)': 0}
    for name, e in cont['entries'].items():
        v = per_entry[(era, name)]
        if (v['adler_name_zlib'] ^ 0x5A5A5A5A) == e['d']:
            wc['d == adler32_wrong_xor(name)'] += 1
        if (v['adler_payload_zlib'] ^ 0x5A5A5A5A) == e['d']:
            wc['d == adler32_wrong_xor(payload)'] += 1
        if rp.fnv1a_wrong_basis(e['name_bytes']) == e['d']:
            wc['d == fnv1a_wrong_basis(name)'] += 1
    wrong_agg[era] = wc
agg_preserved = all(wrong_agg[era][k] == 0 for era in wrong_agg for k in wrong_agg[era])
ok_nc_agg = nc_wrong['exit_code'] != 0 and agg_preserved
gate('R3G7b', 'wrong-value controls PRESERVE the aggregate zero-match counts on the full corpora',
     'wrong-adler(name)/wrong-adler(payload)/wrong-fnv(name) d-match counts all zero: %s'
     % json.dumps(wrong_agg),
     '11,022 entries x 3 wrong candidates x 2 eras',
     'the physically recomputed d values of both containers',
     'the KAT predicates (R3G7a) FAIL for the same wrong primitives that keep the aggregates at zero',
     'this is the P0 demonstration: aggregate acceptance alone CANNOT detect value errors; '
     'value-identity gates (R3G4/R3G9) are required and DO detect them',
     'PHYSICAL_RECOMPUTATION', ok_nc_agg)

# agreement with R2 aggregates + R36 historical
r2_recounts = jload(R2 / '01_RAW/RECOUNTS.json')
r36 = jload(R36_TESTS)
agree_r2 = agree_r36 = True
for era in census:
    key = 'census_953' if era == 'pcg_953' else 'census_2003'
    agree_r2 &= census[era]['name_derived_candidate_matches'] == \
        r2_recounts['field_d_candidates_physical'][key]['name_derived_candidate_matches']
    agree_r36 &= census[era]['name_derived_candidate_matches'] == \
        r36['T4_d_structure'][key]['name_derived_candidate_matches']
nine_zero = all(census[era]['name_derived_candidate_matches'][k] == 0
               for era in census for k in KEYS if k != KEYS[0])
crc_subset = {era: census[era]['name_derived_candidate_matches'][KEYS[0]] for era in census}
c_eq_crc = {era: census[era]['n'] - crc_dir_mismatch[era] for era in census}

ok_recount = (bool(agree_r2) and bool(agree_r36) and nine_zero
              and crc_subset['pcg_953'] == 3435 and crc_subset['era_2003'] == 3299
              and c_eq_crc['pcg_953'] == 5596 and c_eq_crc['era_2003'] == 5426)
gate('R3G11', 'corrected census reproduces the physical result UNCHANGED (nine-zero + CRC subset)',
     'nine exact-zero candidates on both corpora; d==crc32(payload)=3,435/5,596 and 3,299/5,426; '
     'c==CRC32(payload)=11,022/11,022 (0 directory mismatches); agreement with R2 aggregates AND '
     'R36 historical: 20/20 candidate-era pairs',
     '10 candidates x 2 corpora', 'the physical containers + immutable R36 FIELD_D_TESTS.json + '
     'R2 RECOUNTS.json (all hashed)',
     'recomputed with CORRECTED primitives after the value-identity pass; three sources compared; '
     'the independent Python (zlib/exact-int) already agreed — the R2 Node leg was computing '
     'different functions',
     'any count change vs the historical aggregates would indicate value-level sensitivity (would be '
     'investigated, not accepted)',
     'PHYSICAL_RECOMPUTATION', ok_recount)

# ---------- write census artifacts ----------
full_rows = []
FIELDS = ('adler_name_zlib', 'adler_name_iter', 'adler_payload_zlib', 'adler_payload_closed',
          'crc_name_zlib', 'crc_name_lf_zlib', 'crc_name_sz_zlib', 'crc_sz_name_zlib',
          'crc_payload_zlib', 'fnv_name_exact', 'payload_sha256', 'size', 'off', 'c', 'd',
          'adler_name_r2_node', 'fnv_name_r2_node', 'crc_name_r2_node', 'adler_payload_r2_node',
          'crc_payload_r2_node', 'crc_name_lf_r2_node', 'crc_name_sz_r2_node',
          'crc_sz_name_r2_node', 'adler_name_node_corrected', 'adler_payload_node_corrected',
          'fnv_name_node_bigint')
for (era, name), v in sorted(per_entry.items()):
    full_rows.append({'era': era, 'file': name, **{k: v[k] for k in FIELDS}})
full_census_path = jwrite('01_RAW/PRIMITIVE_VALUE_CENSUS_FULL.json', {
    'provenance': {'note': 'LOCAL-ONLY full per-entry value census (NOT part of the published '
                           'package); hash values only, no payload bytes',
                   'sources': [str(BNT_953), str(BNT_2003)],
                   'source_sha256': [c953['sha256'], c2003['sha256']]},
    'rows': full_rows})

comparison = {
    'provenance': {
        'run': 'PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627',
        'method': 'per-entry function VALUE comparison keyed by era+file+candidate input identity; '
                  'match-count tables derived ONLY AFTER the primitive/input identity pass',
        'r2_values': 'literal helper declarations extracted from the hash-pinned R2 source '
                     '(SHA256 ' + R2SRC_SHA + ') and executed as pure functions (Node vm); the '
                     'historical R2 script was NOT executed',
        'corrected_values': 'r3_primitives.py (RFC1950 adler s1=1/s2=0 mod 65521; RFC9923 fnv '
                            'exact multiply mod 2^32) cross-checked against zlib, numpy closed '
                            'form and Node Number/BigInt implementations',
        'sources': [{'era': 'pcg_953', 'path': str(BNT_953), 'sha256': c953['sha256'], 'entries': 5596},
                    {'era': 'era_2003', 'path': str(BNT_2003), 'sha256': c2003['sha256'],
                     'entries': 5426}],
        'payload_publication_policy': 'NO original payload bytes published; per-entry input '
                                      'identity via name + size + SHA256 kept in the local-only '
                                      'full census file',
    },
    'identity_pass': identity,
    'r2_vs_corrected': r2_vs,
    'match_counts_after_identity_pass': census,
    'crc_directory_check': {'c_eq_crc32_payload': c_eq_crc,
                            'crc_directory_mismatches': crc_dir_mismatch},
    'aggregate_zero_match_preservation_of_wrong_value_controls': wrong_agg,
    'full_census_local': {'path': str(full_census_path), 'sha256': sha_file(full_census_path)},
}
jwrite('01_RAW/PRIMITIVE_VALUE_COMPARISON.json', comparison)
jwrite('01_RAW/CENSUS_RECOUNT_R3.json', {
    'method': 'PHYSICAL RECOMPUTATION with corrected primitives (after identity pass)',
    'census': census, 'crc_directory': c_eq_crc,
    'agreement': {'r2_aggregates': bool(agree_r2), 'r36_historical': bool(agree_r36),
                  'r36_source': str(R36_TESTS), 'r36_source_sha256': sha_file(R36_TESTS),
                  'r2_source': str(R2 / '01_RAW/RECOUNTS.json'),
                  'r2_source_sha256': sha_file(R2 / '01_RAW/RECOUNTS.json')},
})

# =========================================================================
# Phase 3 — historical re-sums (kept separate from physical recomputation)
# =========================================================================
log('PHASE 3 historical re-sums (R34 / R35 / R2 state)')

g = jload(R34)
ps = g['per_span']
residual = [s for s in ps if s.get('has_real') and s.get('n_wp_inrange', 0) > 0 and not s.get('var_ok')]
other_fit = [s for s in residual if s.get('g1_ok') or s.get('g2_ok') or s.get('mscan_ok_m')]
none_fit = [s for s in residual if not (s.get('g1_ok') or s.get('g2_ok') or s.get('mscan_ok_m'))]
classifier_real = [s for s in ps if s.get('has_real') and s.get('n_wp_inrange', 0) > 0]
var_ok_all = sum(1 for s in ps if s.get('var_ok'))
var_ok_classifier = sum(1 for s in classifier_real if s.get('var_ok'))
r34_resum = {
    'method': 'HISTORICAL RESUM of prior per-span results (R34 REAL_SPARSE_GRAMMAR.json); NOT a '
              'new physical grammar execution',
    'source': str(R34), 'source_sha256': sha_file(R34),
    'per_span_total': len(ps),
    'classifier_real_spans': len(classifier_real),
    'variable_k_residual_among_classifier_real': len(residual),
    'residual_with_another_recorded_fit': len(other_fit),
    'residual_with_none_of_the_recorded_alternatives': len(none_fit),
    'scoped_denominators': {'var_ok among classifier-real': var_ok_classifier,
                            'classifier-real denominator': len(classifier_real),
                            'var_ok all spans': var_ok_all, 'all spans denominator': len(ps)},
    'counterexamples': [s for s in other_fit if s['file'] in
                        ('592572.nif', '579739.nif', '574751.nif')],
    'interpretation_limits': [
        '334 is the VARIABLE-K residual among classifier-real spans, NOT "fit no tested grammar"',
        'alternative-model fits (g1/g2/mscan) are recorded fits, NOT promoted to true segmentation',
        'the classifier ("real-record" class) is hypothesis-aligned, not established truth',
    ],
}
jwrite('01_RAW/R34_RESUM.json', r34_resum)
ok34sum = (len(residual) == 334 and len(other_fit) == 62 and len(none_fit) == 272
           and var_ok_classifier == 2093 and len(classifier_real) == 2427
           and var_ok_all == 3186 and len(ps) == 6167
           and len(r34_resum['counterexamples']) == 3)
gate('R3G12', 'R34 per-span re-sum: 334 is the VARIABLE-K residual (not "no tested grammar")',
     'classifier-real 2,427; variable-k ok 2,093 (86.2%%); residual 334; of residual: 62 another '
     'recorded fit, 272 none among the recorded alternatives; all-span fit 3,186/6,167; 3 concrete '
     'counterexamples (592572.nif / 579739.nif / 574751.nif)',
     '6,167 per-span records', 'the R34 REAL_SPARSE_GRAMMAR.json per_span raw records (hash-pinned)',
     'independent re-filter with the exact R34 classifier condition; raw rows, not prose',
     'the wording "334 real-record spans fit no tested grammar" is contradicted by the 62 recorded '
     'alternative fits (counterexample 592572.nif bi=65 si=45 mscan_ok_m=[30])',
     'HISTORICAL_RESUM', ok34sum)

# R35 claim table preservation (historical transcription, source inspection)
rep35 = R35_REPORT.read_text(encoding='utf-8')
claims35 = []
for line in rep35.splitlines():
    if not line.startswith('| C-'):
        continue
    cells = [c.strip() for c in line.split('|')]
    if len(cells) >= 8 and cells[5].startswith('**') and \
            ('ERA-STABLE' in cells[5] or 'EVOLVED' in cells[5]):
        claims35.append({'claim_id': cells[1], 'claim_text': cells[2][:200],
                         'measured_953': cells[3][:200], 'measured_2003': cells[4][:200],
                         'verdict': cells[5], 'status': cells[6]})
verdicts = {}
for c in claims35:
    v = 'EVOLVED' if 'EVOLVED' in c['verdict'] else 'ERA-STABLE'
    c['verdict_class'] = v
    verdicts[v] = verdicts.get(v, 0) + 1
morph1 = next((c for c in claims35 if c['claim_id'] == 'C-MORPH-1'), None)
ok35 = (len(claims35) == 21 and verdicts.get('ERA-STABLE') == 19 and verdicts.get('EVOLVED') == 2
        and morph1 is not None and '86.2%' in morph1['measured_953']
        and '81.0%' in morph1['measured_2003'])
jwrite('01_RAW/R35_CLAIM_TABLE_PRESERVED.json', {
    'method': 'HISTORICAL TRANSCRIPTION of the R35 REPORT.md 21-claim evolution table '
              '(source inspection)',
    'source': str(R35_REPORT), 'source_sha256': sha_file(R35_REPORT),
    'claims': claims35, 'verdict_counts': verdicts,
    'notes': ['C-MORPH-1 is a PARTIAL-FIT claim (rr 2,093/2,427 = 86.2% on 9.3.5; 1,180/1,457 = '
              '81.0% on 2003), NOT a 100% fit',
              '2 claims are EVOLVED (content-profile deltas), so "all 21 claims reproduced at '
              '100%" is NOT a valid summary',
              'exact claim IDs, denominators and evidence statuses retained; nothing promoted'],
})
gate('R3G13', 'R35 21-claim table preserved with exact IDs/denominators/verdicts (no 100% overstatement)',
     '21 claims transcribed; verdicts ERA-STABLE %d / EVOLVED %d; C-MORPH-1 partial-fit '
     '(86.2%%/81.0%%) recorded; sample/denominator limits retained'
     % (verdicts.get('ERA-STABLE', 0), verdicts.get('EVOLVED', 0)),
     '21 claims', 'the R35 REPORT.md table (hash recorded)',
     'verbatim transcription, not a summary; the overstatement is explicitly corrected',
     'presenting all 21 claims as 100% fits would contradict the C-MORPH-1 row and the 2 EVOLVED '
     'verdicts',
     'HISTORICAL_TRANSCRIPTION', ok35)

# R2 state re-sum (tally + three-state evidence from the actual R2 artifacts)
cm = list(csv.DictReader(open(R2 / '05_ANALYSIS/CLAIM_MATRIX.csv', encoding='utf-8-sig', newline='')))
tally = {}
for r in cm:
    tally[r['knowledge_status']] = tally.get(r['knowledge_status'], 0) + 1
tr2 = jload(R2 / '02_LOGS/TEST_RESULTS.json')
g13 = next(x for x in tr2['gates'] if x['gate_id'] == 'R2G13')
hr_json = {x['gate_id']: x['pass'] for x in tr2['gates'] if x['gate_type'] == 'HUMAN_REVIEWED'}
gates_csv = list(csv.DictReader(open(R2 / 'STAGE_ACCEPTANCE_GATES.csv', encoding='utf-8-sig', newline='')))
hr_csv = {x['gate_id']: x['result'] for x in gates_csv if x['gate_type'] == 'HUMAN_REVIEWED'}
r2_state = {
    'method': 'HISTORICAL RESUM / SOURCE INSPECTION of the actual R2 artifacts (not a rerun)',
    'r2_claim_matrix_tally_from_rows': tally,
    'r2g13_gate_name_recorded': g13['gate_name'],
    'r2g13_label_stale': '{CONFIRMED 17, REJECTED 7}' in g13['gate_name'],
    'hr_gates_json_pass_values': hr_json,
    'hr_gates_csv_results': hr_csv,
    'serialization_defect': 'run_gates.py L50 stores bool(ok): HR-1..HR-4 were called with ok=None '
                            '-> pass=false in TEST_RESULTS.json and FAIL in the CSV, '
                            'misrepresenting pending human review as failed review',
    'r2_test_results_sha256': sha_file(R2 / '02_LOGS/TEST_RESULTS.json'),
    'r2_gates_csv_sha256': sha_file(R2 / 'STAGE_ACCEPTANCE_GATES.csv'),
    'r2_claim_matrix_sha256': sha_file(R2 / '05_ANALYSIS/CLAIM_MATRIX.csv'),
}
jwrite('01_RAW/R2_STATE_RESUM.json', r2_state)
ok_r2state = (tally.get('CONFIRMED') == 16 and tally.get('REJECTED') == 8
              and r2_state['r2g13_label_stale']
              and hr_json == {'HR-1': False, 'HR-2': False, 'HR-3': False, 'HR-4': False}
              and set(hr_csv.values()) == {'FAIL'})
gate('R3G16', 'R2G13-equivalent tally derived from ACTUAL rows (stale 17/7 label detected)',
     'actual R2 CLAIM_MATRIX tally: CONFIRMED %d, REJECTED %d (the R2G13 gate label said 17/7); '
     'R2 HR-1..4 serialized pass=false / CSV=FAIL although no human reviewed them'
     % (tally.get('CONFIRMED', 0), tally.get('REJECTED', 0)),
     '24 R2 claim rows + 4 R2 HR gates', 'the actual R2 artifacts (CLAIM_MATRIX.csv, '
     'TEST_RESULTS.json, STAGE_ACCEPTANCE_GATES.csv — all hashed)',
     'labels are derived from parsing the emitted rows, never copied from gate names',
     'the stale {17,7} label and the pending-as-FAIL serialization are both detected',
     'HISTORICAL_RESUM', ok_r2state)

# =========================================================================
# Phase 4 — sidecar byte-losslessness + R39 bare-CR dual-policy (item 8)
# =========================================================================
log('PHASE 4 sidecars')
TERM = {'CRLF': b'\r\n', 'LF': b'\n', 'EOF_NO_TERMINATOR': b''}
sidecars = []
for p in sorted(SIDE_DIR.glob('*.csv')):
    rows = list(csv.DictReader(open(p, encoding='utf-8-sig', newline='')))
    orig = B / rows[0]['original_manifest']  # sidecar records a project-root-relative path
    buf = orig.read_bytes()
    orig_sha = hashlib.sha256(buf).hexdigest()
    recon = b''
    header = None
    errors = []
    strict_compared = 0
    unresolved = 0
    for index, row in enumerate(rows, 1):
        raw = base64.b64decode(row['raw_row_base64'], validate=True)
        assert hashlib.sha256(raw).hexdigest() == row['raw_row_sha256']
        assert row['original_manifest_sha256'] == orig_sha and int(row['original_row']) == index
        assert row['row_terminator'] in TERM, 'unknown terminator ' + row['row_terminator']
        recon += raw + TERM[row['row_terminator']]
        if index == 1:
            fields1 = custom_parse(raw.decode('utf-8'))  # BOM retained as data
            header = [f.lstrip('\ufeff') for f in fields1]  # keys: BOM-stripped
            if row['strict_valid'] == 'true':
                strict_compared += 1
                if dict(zip(header, fields1)) != json.loads(row['header_mapped_json']):
                    errors.append(index)
            continue
        if row['strict_valid'] == 'true':
            strict_compared += 1
            parsed = custom_parse(raw.decode('utf-8'))
            if len(parsed) != len(header) or dict(zip(header, parsed)) != \
                    json.loads(row['header_mapped_json']):
                errors.append(index)
        else:
            unresolved += 1
    sidecars.append({'path': str(p), 'original': str(orig), 'byte_exact': recon == buf,
                     'rows': len(rows), 'strict_rows_compared': strict_compared,
                     'unresolved_rows': unresolved,
                     'semantic_mapping_errors_under_custom_contract': errors})

# R39 final row dual-policy analysis
r39_side_path = next(s['path'] for s in sidecars if 'WIKI_AUDIT_R39' in s['path'])
r39_rows = list(csv.DictReader(open(r39_side_path, encoding='utf-8-sig', newline='')))
last = r39_rows[-1]
raw_last = base64.b64decode(last['raw_row_base64'])
custom_fields = custom_parse(raw_last.decode('utf-8'))
csv_records = list(csv.reader(io.StringIO(raw_last.decode('utf-8'), newline=None), strict=True))
r39_header_row = r39_rows[0]
header_keys = [f.lstrip('\ufeff') for f in
               custom_parse(base64.b64decode(r39_header_row['raw_row_base64']).decode('utf-8'))]
dual = {
    'row': last['original_row'],
    'raw_row_bytes_hex': raw_last.hex(),
    'raw_row_shape': 'final field value ends with a bare CR (0x0d); the recorded row terminator is CRLF',
    'custom_line_contract': {
        'policy': 'bare CR is an ordinary character within the physical row (the R2 builder '
                  'csvParse semantics, control_r2.cjs L39-45)',
        'computed_by_value': repr(custom_fields[-1]),
        'matches_sidecar_header_mapped_json':
            dict(zip(header_keys, custom_fields)) == json.loads(last['header_mapped_json']),
    },
    'csv_record_semantics': {
        'policy': 'Python csv with universal newlines: a lone CR terminates the record',
        'computed_by_value': repr(csv_records[0][-1]) if csv_records else None,
        'records_emitted': len(csv_records),
    },
    'conclusion': 'Both policies preserve the original bytes exactly (byte-lossless sidecar, 12/12). '
                  'The final-row computed_by value differs BY INTERPRETATION ("n/a\\r" vs "n/a"); '
                  'this is NOT raw-byte loss and NOT permission for a manifest migration. The '
                  'sidecar mapping follows the custom physical-line contract and is internally '
                  'consistent under it.',
}
side_out = {
    'method': 'PHYSICAL RECOMPUTATION (full-file byte reconstruction) + independent field-level '
              'comparison under the EXPLICIT custom physical-line contract',
    'sidecars': sidecars,
    'byte_exact_count': sum(1 for s in sidecars if s['byte_exact']),
    'sidecar_count': len(sidecars),
    'r39_final_row_dual_policy': dual,
    'bare_cr_policy_statement': 'Semantic header normalization, where restated, follows the custom '
                                'physical-line contract (bare CR = data). Standard CSV record '
                                'parsing yields a different computed_by for exactly one row (R39 '
                                'row 10) — recorded as an interpretive difference, not byte loss.',
}
jwrite('01_RAW/SIDECAR_BARE_CR_ANALYSIS.json', side_out)

ok_side = (sum(1 for s in sidecars if s['byte_exact']) == 12 and len(sidecars) == 12
           and all(not s['semantic_mapping_errors_under_custom_contract'] for s in sidecars)
           and dual['custom_line_contract']['matches_sidecar_header_mapped_json'] is True
           and dual['csv_record_semantics']['computed_by_value'] == "'n/a'")
gate('R3G14', '12/12 sidecars byte-lossless re-verified; bare-CR policy explicit + dual-policy compared',
     'byte reconstruction 12/12 SHA-equal; field-level mapping under the custom contract: %d '
     'strict rows compared, 0 errors (incl. R39 row 10 = "n/a\\r"); CSV-record-semantics parse of '
     'R39 row 10 yields "n/a" (interpretive difference, not byte loss)'
     % sum(s['strict_rows_compared'] for s in sidecars),
     '12 sidecar files / %d strict rows' % sum(s['strict_rows_compared'] for s in sidecars),
     'the original manifests (bytes) + the sidecar records (SHA-pinned per row)',
     'reassembly is byte-level; the field comparison uses an independently written state machine '
     'with the same semantics as the R2 builder',
     'any reconstruction byte difference or mapping mismatch fails the gate',
     'PHYSICAL_RECOMPUTATION', ok_side)

# =========================================================================
# Phase 5 — three-state preservation + TEST_RESULTS emission
# =========================================================================
log('PHASE 5 gates assembly (three-state)')
for hr in [
    ('HR-R3-1', 'Semantic adequacy of the corrected wordings (P1R2-5-R3, P2R2-2-R3, method provenance)'),
    ('HR-R3-2', 'Acceptance of the R3 finding dispositions and supersession map'),
    ('HR-R3-3', 'Proposal application decision (all corrections remain PROPOSALS; nothing applied)'),
    ('HR-R3-4', 'Scope discipline: no morph research, no wiki application, no canonical update, '
                'no milestone promotion'),
]:
    gate(hr[0], hr[1], 'reviewer judgment', 'independent post-audit', 'independent post-audit',
         'human review cannot be machine-proved; mechanical gates check only structure',
         'n/a (human review)', 'HUMAN_REVIEWED', None)

states_present = sorted({g['state'] for g in GATES})
three_state_ok = ('PENDING' in states_present and 'PASS' in states_present
                  and 'FAIL' not in states_present
                  and all(g['pass'] is None for g in GATES if g['gate_type'] == 'HUMAN_REVIEWED'))
gate('R3G15', 'three-state preservation through the gate function/JSON (PENDING distinct from FAIL/PASS)',
     "states present in this run's gate set: %s; HR gates carry pass=null/state=PENDING (R2 stored "
     'false/FAIL for the same situation)' % states_present,
     '%d gates' % len(GATES), 'the emitted gate records themselves',
     'the R3 gate function serializes None as PENDING; the negative control (R3G8a) proves the R2 '
     'coercion fails these predicates',
     'any pending gate serialized as FAIL/PASS fails this gate',
     'EXECUTABLE', three_state_ok)

executable_pass = all(g['state'] == 'PASS' for g in GATES if g['gate_type'] == 'EXECUTABLE')
overall = {
    'run': 'PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627',
    'overall_executable_pass': executable_pass,
    'executable_gates': sum(1 for g in GATES if g['gate_type'] == 'EXECUTABLE'),
    'human_reviewed_gates_pending': sum(1 for g in GATES if g['gate_type'] == 'HUMAN_REVIEWED'),
    'failed_gates': [g['gate_id'] for g in GATES if g['state'] == 'FAIL'],
    'human_acceptance': 'PENDING_HUMAN_REVIEW — OVERALL EXECUTABLE PASS IS NOT HUMAN ACCEPTANCE',
    'provenance': {
        'driver': '00_CONTROL/revalidate_r3.py',
        'driver_sha256_at_execution': sha_file(Path(__file__)),
        'primitives': '00_CONTROL/r3_primitives.py',
        'primitives_sha256_at_execution': sha_file(RUN / '00_CONTROL/r3_primitives.py'),
        'probe': '00_CONTROL/probe_r2_helpers.cjs (Node) — executed the literal R2 declarations',
        'probe_output_sha256': sha_file(probe_path),
        'duration_s': round(time.time() - T0, 1),
    },
    'kat_subprocess_exit_codes': {s: kat_runs[s]['exit_code'] for s in kat_runs},
}
jwrite('02_LOGS/TEST_RESULTS.json', {'overall': overall, 'gates': GATES})

(RUN / '02_LOGS/LOGS.md').write_text(
    '# LOGS — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3\n\n'
    'Generated ' + time.strftime('%Y-%m-%d %H:%M:%S') + ' by 00_CONTROL/revalidate_r3.py.\n\n'
    '## Execution order (enforced)\n\n'
    '1. Phase 0 identity pins (prompt SHA, R2 source pin, R34 pin).\n'
    '2. Phase 1 KAT suites via `run_kats.py` subprocesses (corrected / oracle self-vectors /\n'
    '   R2-literal / wrong-value / three-state controls) — the corrected set MUST pass before\n'
    '   aggregation; negative controls MUST exit nonzero (actual exit codes recorded in\n'
    '   02_LOGS/kat_*.json and TEST_RESULTS.json).\n'
    '3. Phase 1b Node probe (literal R2 declarations executed from the hash-pinned source;\n'
    '   counterexamples tested against actual executed bytes).\n'
    '4. Phase 2 corpus aggregation (only after Phase 1 PASS): per-entry identity pass,\n'
    '   R2-vs-corrected value census, match-count tables, R2/R36 agreement.\n'
    '5. Phase 3 historical re-sums (R34 / R35 / R2 state) — kept separate from physical\n'
    '   recomputation.\n'
    '6. Phase 4 sidecar byte reconstruction + R39 bare-CR dual-policy comparison.\n'
    '7. Phase 5 gate assembly (three-state) + TEST_RESULTS.json emission.\n\n'
    '## Command log\n\n```\n' + '\n'.join(LOG_LINES) + '\n```\n\n'
    '## Invocations\n\n```\n'
    'python 00_CONTROL/run_kats.py --set <set> --out 02_LOGS/kat_<set>.json   (x6 sets)\n'
    'node   00_CONTROL/probe_r2_helpers.cjs 01_RAW/R2_HELPER_PROBE.json\n'
    'python 00_CONTROL/revalidate_r3.py\n'
    'python 00_CONTROL/emit_r3_outputs.py\n'
    '```\n', encoding='utf-8')
log('WROTE 02_LOGS/LOGS.md')

print(json.dumps({'overall_executable_pass': executable_pass,
                  'failed_gates': overall['failed_gates'],
                  'defect_reproduction': defect,
                  'r2_vs_corrected_mismatches': {k: r2_vs[k]['mismatches'] for k in r2_vs},
                  'census_953': census['pcg_953']['name_derived_candidate_matches'],
                  'census_2003': census['era_2003']['name_derived_candidate_matches'],
                  'r34_resum': [len(residual), len(other_fit), len(none_fit)],
                  'duration_s': round(time.time() - T0, 1)}, indent=1))
sys.exit(0 if executable_pass else 1)
