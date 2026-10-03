# qc_pins.py -- PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 fresh QC: pin + artifact
# verification battery (items 5c, 8, 9, 10 of the QC checklist).
import csv
import glob
import hashlib
import io
import json
import os
import re

WORK = r'D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean'
PKG = os.path.join(WORK, 'docs', 'audits', 'PE_GAMEBRYO_ORACLE_TOOL_R1_20261003')
GB = r'D:\gamebyroengine'
SBX = r'D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest().upper()


def section(name):
    print()
    print('=== ' + name + ' ===')


# ---------- P1: NiStream.cpp L42-46 ----------
section('P1: GB12 NiStream.cpp L40-48 (min/max NIF version constants)')
try:
    p = os.path.join(GB, r'extracted\Gb12_Source\CoreLibs\NiMain\NiStream.cpp')
    lines = open(p, encoding='latin-1').read().splitlines()
    for i in range(39, 48):
        print('%4d: %s' % (i + 1, lines[i]))
    print('sha256=', sha(p))
except Exception as e:
    print('ERROR', e)

# ---------- P2: NiObject.cpp L134-143 ----------
section('P2: GB12 NiObject.cpp L130-146 (per-block GroupID gate)')
try:
    p = os.path.join(GB, r'extracted\Gb12_Source\CoreLibs\NiMain\NiObject.cpp')
    lines = open(p, encoding='latin-1').read().splitlines()
    for i in range(129, 146):
        print('%4d: %s' % (i + 1, lines[i]))
    print('sha256=', sha(p), '(expect B137FE42126F496A37E7627061FF968256A6DA87D912784865609E2122FE470E)')
except Exception as e:
    print('ERROR', e)

# ---------- PostLink claim: NiObjectNET.cpp L656-693 ----------
section('PostLink: GB12 NiObjectNET.cpp L650-695 (migration-only claim)')
try:
    p = os.path.join(GB, r'extracted\Gb12_Source\CoreLibs\NiMain\NiObjectNET.cpp')
    lines = open(p, encoding='latin-1').read().splitlines()
    body = '\n'.join(lines[649:695])
    for i in range(649, 695):
        print('%4d: %s' % (i + 1, lines[i]))
    print('sha256=', sha(p), '(expect 2ADB8F89CDB40F8C114FEAA6E4A32DD7A1CC73BCE30D745F669458EE6F354190)')
except Exception as e:
    print('ERROR', e)

# ---------- P4: NiMain.lib FF4519AF ----------
section('P4: GB112 NiMain.lib re-hash (prefix FF4519AF, 3,073,590 B)')
try:
    hits = []
    for root, dirs, files in os.walk(os.path.join(GB, 'extracted')):
        for fn in files:
            if fn.lower() == 'nimain.lib':
                fp = os.path.join(root, fn)
                sz = os.path.getsize(fp)
                hits.append((fp, sz))
    for fp, sz in hits:
        h = sha(fp)
        print('lib:', fp, 'size=', sz, 'sha256=', h[:16] + '...',
              'PREFIX_OK' if h.startswith('FF4519AF') else 'PREFIX_MISMATCH',
              'SIZE_OK' if sz == 3073590 else 'SIZE_DIFF')
    if not hits:
        print('NO NiMain.lib found under extracted/')
except Exception as e:
    print('ERROR', e)

# ---------- R8: sgp_T1_dialog.txt ----------
section('R8: sgp_T1_dialog.txt (timelock message verbatim + encoding + hash)')
try:
    p = os.path.join(PKG, '04_EVIDENCE', 'sgp_T1_dialog.txt')
    raw = open(p, 'rb').read()
    print('size=', len(raw), 'BOM=', raw[:3] == b'\xef\xbb\xbf')
    txt = raw.decode('utf-8')
    print('verbatim_present=',
          'The supplied Gamebryo timelock (8469DD85B0554A49, Internal) has expired' in txt)
    print('title_present=', 'NetImmerse Evaluation Copy' in txt)
    print('sha256=', sha(p), '(E3 pin 180EB479BD87B310A946E3BBBE5876FB4D18E3E5A95735A6D497C72AF73A399A)')
    print('--- first 15 lines ---')
    for ln in txt.splitlines()[:15]:
        print(' |', ln)
except Exception as e:
    print('ERROR', e)

# ---------- R7: gui_attempts_log*.txt shader chain ----------
section('R7: gui_attempts_log*.txt (shader-library chain)')
try:
    for name in ('gui_attempts_log.txt', 'gui_attempts_log2.txt', 'gui_attempts_log3.txt'):
        p = os.path.join(PKG, '04_EVIDENCE', name)
        if not os.path.exists(p):
            print(name, 'MISSING')
            continue
        txt = open(p, encoding='utf-8', errors='replace').read()
        print('--', name, 'size=', os.path.getsize(p))
        for pat in ('EGB_SHADER_LIBRARY_PATH', 'Failed to load shader',
                    'timelock', 'Settings'):
            hits = [ln.strip() for ln in txt.splitlines() if pat in ln]
            print('   %-28s hits=%d %s' % (pat, len(hits), hits[:2]))
except Exception as e:
    print('ERROR', e)

# ---------- R6 erratum count ----------
section('R6: RETRACTIONS_SUPERSESSIONS.md erratum occurrence count')
try:
    p = os.path.join(PKG, '02_ANALYSIS', 'RETRACTIONS_SUPERSESSIONS.md')
    txt = open(p, encoding='utf-8').read()
    r6_lines = [ln.strip() for ln in txt.splitlines() if 'R6' in ln]
    tie_lines = [ln.strip() for ln in txt.splitlines() if '948' in ln]
    e2blocks = len(re.findall(r'Batch E2 additions', txt))
    print('lines containing "R6":', len(r6_lines))
    for ln in r6_lines[:6]:
        print('   R6>', ln[:150])
    print('lines containing 948:', len(tie_lines))
    for ln in tie_lines[:4]:
        print('   948>', ln[:150])
    print('"Batch E2 additions" blocks:', e2blocks, '(expect 1)')
    print('3-way tie stated:', '3-way 948 B tie' in txt or '3-way tie' in txt)
    print('sha256=', sha(p), '(E3 pin 6177511FE39D7DCEA7E3D088B5151319274003E6CADAA4810F12F808756FED3D)')
except Exception as e:
    print('ERROR', e)

# ---------- Matrix algebra ----------
section('G-MATRIX-1: blank-cell count + closed-set check')
try:
    p = os.path.join(PKG, '03_TOOL', 'GAMEBRYO_COMPATIBILITY_MATRIX.csv')
    with open(p, encoding='utf-8', newline='') as f:
        rows = list(csv.reader(f))
    header = rows[0]
    print('columns=', len(header), '(s16 example has 14; gate row says 13)')
    blanks = 0
    closed = {'PASS', 'PARTIAL', 'FAIL', 'NOT_TESTED', 'UNKNOWN'}
    outside = []
    for ri, row in enumerate(rows[1:], start=2):
        for ci, cell in enumerate(row):
            if ci >= len(header):
                print('row %d has extra cell %d: %r' % (ri, ci, cell[:40]))
                continue
            if cell.strip() == '':
                blanks += 1
                print('BLANK row %d col %s' % (ri, header[ci]))
            elif header[ci] not in ('GB_VERSION', 'TOOL', 'NOTES', 'SOURCE_AVAILABLE', 'BUILDS'):
                tok = cell.strip().split(' ')[0].split('(')[0].rstrip(',')
                if tok not in closed:
                    outside.append((ri, header[ci], tok))
    print('blank_cells=', blanks)
    print('cells_with_leading_token_outside_closed_set=', len(outside))
    for ri, colname, tok in outside:
        print('   OUTSIDE row %d col %s token=%r' % (ri, colname, tok))
    print('sha256=', sha(p), '(E2 pin 92E34E9460B371B1C8439538C25140ADF2F82DCB04924B71E1711DE49CA0BC11)')
except Exception as e:
    print('ERROR', e)

# ---------- SELECTION.md size ----------
section('SELECTION.md byte size (lock records 9954)')
try:
    p = os.path.join(PKG, '00_CONTROL', 'SELECTION.md')
    print('size=', os.path.getsize(p))
except Exception as e:
    print('ERROR', e)

# ---------- T2/T4 num_blocks + count checks ----------
section('Raw JSON: T2/T4 block counts + object_count_check')
try:
    tr = os.path.join(PKG, '04_EVIDENCE', 'T_runs')
    for name in ('inspect_T2_gb12_full.json', 'inspect_T4_gb12_full.json',
                 'inspect_T5_gb12_full.json'):
        j = json.load(open(os.path.join(tr, name), encoding='utf-8'))
        print(name, 'num_blocks=', j['input_identity'].get('num_blocks_from_header'),
              'count_check=', j.get('object_count_check'),
              'error=', j['load_result'].get('error'))
except Exception as e:
    print('ERROR', e)

# ---------- compare_T1 items (G-CMP-2) ----------
section('compare_T1.json items (MISMATCH explanations)')
try:
    p = os.path.join(PKG, '04_EVIDENCE', 'T_runs', 'compare_T1.json')
    j = json.load(open(p, encoding='utf-8'))
    print('float_policy=', json.dumps(j.get('float_policy'))[:300])
    items = j.get('items', [])
    print('item_count=', len(items))
    for it in items:
        st = it.get('status')
        name = it.get('field') or it.get('name')
        expl = it.get('explanation') or it.get('note') or it.get('detail') or ''
        if st != 'MATCH':
            print('  %-24s %-28s expl=%s' % (name, st, str(expl)[:160]))
            for extra in ('oracle_value', 'our_value', 'oracle', 'ours'):
                if extra in it:
                    print('      %s=%s' % (extra, str(it[extra])[:140]))
except Exception as e:
    print('ERROR', e)

# ---------- package drift check vs batch pins ----------
section('Package file hashes vs E2/E3 batch pins (drift check)')
try:
    pins = [
        ('02_ANALYSIS/218757_NIF_RESULT.md', '35C0E9A535EBBDCF9E07A798A35FFD26EE143066D60E5817C5C2A64C2EF155E0', 'E2'),
        ('02_ANALYSIS/NOT_CHECKED.md', 'FE2C56EC29C2E1B574D2F71E13C29DC1C507E19D4C0F6441253AE2ADE3BD7ECE', 'E3'),
        ('06_REPORT/FINAL_REPORT.md', 'DB7C9E7D03F29406A427387B94DE7470FDD73DD85E244248847423E18C82C019', 'E3'),
        ('06_REPORT/HANDOFF.md', 'B9D113FA6FA6968E606B4970EA0315D51FFFB18A2A2E978E3F962BC2C81E6727', 'E3'),
        ('00_CONTROL/STAGE_ACCEPTANCE_GATES.csv', '69540A42ADD991E81A8DF0C4E152FC9B973A2E1AAFF9AF5235EB48D6174F1F5C', 'E3'),
        ('04_EVIDENCE/T_runs/compare_T3.json', 'B810FA6A0B1DF1EC524E05BEAE109EBA3B0E5D14F956FAC8B9BD7CB44D36BFCF', 'E3'),
        ('03_TOOL/TEST_MATRIX.csv', '010F3BDAE8FED1EA6949BC593B249B1B04603F59150D0274F75763F9A69D3A85', 'E2'),
        ('03_TOOL/FAIL_CLOSED_TESTS.md', 'B42D1A92E60ED20E0D61F49F5DFA2B2F3A7C29B5619FCF4E94D53E276D3E77A3', 'E2'),
    ]
    for rel, expect, src in pins:
        p = os.path.join(PKG, rel.replace('/', os.sep))
        if not os.path.exists(p):
            print('MISSING', rel)
            continue
        h = sha(p)
        ok = 'MATCH' if h == expect.upper() else 'DRIFT'
        print('%-55s %s (%s pin)' % (rel, ok, src))
        if ok == 'DRIFT':
            print('    now=', h)
            print('    pin=', expect)
except Exception as e:
    print('ERROR', e)

# ---------- MANIFEST absence ----------
section('MANIFEST_SHA256.csv presence (persistence-phase artifact)')
print('exists=', os.path.exists(os.path.join(PKG, 'MANIFEST_SHA256.csv')))

# ---------- G-SEL-2: EXTRACT_PROVENANCE ----------
section('EXTRACT_PROVENANCE.json (G-SEL-2)')
try:
    p = os.path.join(PKG, '04_EVIDENCE', 'EXTRACT_PROVENANCE.json')
    j = json.load(open(p, encoding='utf-8'))
    print('top_keys=', sorted(j.keys()))
    txt = json.dumps(j)
    for t, h in (('218757', '3E8A22C2'), ('533021', '9CFF776D'),
                 ('496633', '4DBCC731'), ('223534', '81CB4D8D'),
                 ('547226', 'D7F2A02C')):
        print('  %s sha pin present: %s' % (t, h in txt))
    print('  Models.bnt pin present:', 'C950A8C2' in txt)
except Exception as e:
    print('ERROR', e)

# ---------- G-SIG-1 structure ----------
section('GAMEBRYO_SEMANTIC_SIGNATURES.json (G-SIG-1)')
try:
    p = os.path.join(PKG, '02_ANALYSIS', 'GAMEBRYO_SEMANTIC_SIGNATURES.json')
    j = json.load(open(p, encoding='utf-8'))
    print('top_keys=', sorted(j.keys()))
    txt = json.dumps(j)
    print('mentions Entropia.exe matching?',
          bool(re.search(r'Entropia\.exe.{0,80}match', txt, re.I)))
    sigs = j.get('signatures') or j.get('functions') or {}
    if isinstance(sigs, dict):
        print('signature_count=', len(sigs))
        for k in list(sigs)[:3]:
            v = sigs[k]
            print('  e.g.', k, '->', sorted(v.keys()) if isinstance(v, dict) else type(v))
    print('sha256=', sha(p))
except Exception as e:
    print('ERROR', e)

# ---------- sandbox: test stdout / phaseD / registry / sample / e3 files ----------
section('Sandbox: control/test evidence files (top level + selected)')
try:
    print('top-level files:')
    for fn in sorted(os.listdir(SBX)):
        fp = os.path.join(SBX, fn)
        if os.path.isfile(fp):
            print('  ', fn, os.path.getsize(fp))
    print('dirs:', sorted(d for d in os.listdir(SBX) if os.path.isdir(os.path.join(SBX, d))))
    pat = re.compile(r'(stdout|test|registry|sample|e3_|phaseD|revalid)', re.I)
    print('selected matches anywhere in sandbox:')
    n = 0
    for root, dirs, files in os.walk(SBX):
        for fn in files:
            if pat.search(fn):
                print('  ', os.path.relpath(os.path.join(root, fn), SBX))
                n += 1
                if n > 40:
                    print('   ... (truncated)')
                    break
        if n > 40:
            break
except Exception as e:
    print('ERROR', e)
print()
print('qc_pins done')
