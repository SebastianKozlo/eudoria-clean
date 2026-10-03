# qc_compare.py -- PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 fresh QC comparison harness.
# Compares the QC worker's independent oracle re-runs against the executor's
# published raw JSONs, verifies the executor's determinism pairs, and greps
# the oracle JSON bodies for wall-clock date patterns (G-TOOL-2).
import hashlib
import json
import os
import re
import glob

QC = r'C:\Users\User\AppData\Local\Temp\opencode\qc_gb_oracle_r1'
TRF = os.path.join(r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean',
                   r'docs\audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003'
                   r'\04_EVIDENCE\T_runs')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest().upper()


print('=== MINE vs EXECUTOR (field-level if differ) ===')
pairs = [
    ('probe_T1_gb12.json', 'probe_T1_gb12_mine.json'),
    ('probe_T4_gb12.json', 'probe_T4_gb12_mine.json'),
    ('probe_T1_gb26.json', 'probe_T1_gb26_mine.json'),
    ('inspect_T1_gb12_full.json', 'inspect_T1_gb12_full_mine.json'),
    ('inspect_T1_gb12_orig.json', 'inspect_T1_gb12_orig_mine.json'),
    ('inspect_T4_gb12_full.json', 'inspect_T4_gb12_full_mine.json'),
    ('inspect_T2_gb12_full.json', 'inspect_T2_gb12_full_mine.json'),
]
for ex, mine in pairs:
    p1 = os.path.join(TRF, ex)
    p2 = os.path.join(QC, mine)
    if not os.path.exists(p1):
        print('MISSING_EXECUTOR_FILE', ex)
        continue
    if not os.path.exists(p2):
        print('MISSING_MINE_FILE', mine)
        continue
    h1, h2 = sha(p1), sha(p2)
    if h1 == h2:
        print('BYTE_IDENTICAL', ex, h1)
    else:
        print('DIFFER', ex, 'exec=', h1, 'mine=', h2)
        with open(p1, encoding='utf-8') as f:
            a = json.load(f)
        with open(p2, encoding='utf-8') as f:
            b = json.load(f)
        keys = sorted(set(a) | set(b))
        for k in keys:
            if a.get(k) != b.get(k):
                sa = json.dumps(a.get(k), sort_keys=True)[:400]
                sb = json.dumps(b.get(k), sort_keys=True)[:400]
                print('  FIELD_DIFF', k)
                print('    executor:', sa)
                print('    mine    :', sb)

print('=== EXECUTOR DETERMINISM PAIRS (published) ===')
dets = [
    ('inspect_T1_gb12_full.json', 'inspect_T1_gb12_full_run2.json'),
    ('inspect_T2_gb12_full.json', 'inspect_T2_gb12_full_run2.json'),
    ('inspect_T3_gb12_full.json', 'inspect_T3_gb12_full_run2.json'),
    ('inspect_T4_gb12_full.json', 'inspect_T4_gb12_full_run2.json'),
    ('inspect_T5_gb12_full.json', 'inspect_T5_gb12_full_run2.json'),
]
for a_, b_ in dets:
    p1 = os.path.join(TRF, a_)
    p2 = os.path.join(TRF, b_)
    if os.path.exists(p1) and os.path.exists(p2):
        same = sha(p1) == sha(p2)
        print('PAIR', a_, 'vs', b_,
              'BYTE_IDENTICAL' if same else 'DIFFER',
              sha(p1), sha(p2))
    else:
        print('PAIR_INCOMPLETE', a_, 'vs', b_,
              os.path.exists(p1), os.path.exists(p2))

print('=== MY OWN DETERMINISM (T4 gb12 full-decode x2) ===')
p1 = os.path.join(QC, 'inspect_T4_gb12_full_mine.json')
p2 = os.path.join(QC, 'inspect_T4_gb12_full_mine_run2.json')
if os.path.exists(p1) and os.path.exists(p2):
    same = sha(p1) == sha(p2)
    print('MINE_T4_PAIR', 'BYTE_IDENTICAL' if same else 'DIFFER',
          sha(p1), sha(p2))
else:
    print('MINE_T4_PAIR_INCOMPLETE')

print('=== DATE-PATTERN GREP over oracle JSON bodies (04_EVIDENCE/T_runs) ===')
hits_total = 0
for p in sorted(glob.glob(os.path.join(TRF, '*.json'))):
    with open(p, encoding='utf-8', errors='replace') as f:
        txt = f.read()
    hits = re.findall(r'20\d\d-[01]\d-[0-3]\d', txt)
    if hits:
        hits_total += len(hits)
        print('DATE_HITS', os.path.basename(p), hits[:8])
print('date_grep_total_hits=%d' % hits_total)
print('qc_compare done')
