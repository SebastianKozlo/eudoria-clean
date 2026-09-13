# qc_addr_lock.py — weryfikacja bajtowa cytowanych VA wlasnym parserem PE
# QC: PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913. READ-ONLY.
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load

pe = load()
OUT_A = r'D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913\00_CONTROL\qc_probe\qc_addr_lock_runA.json'
OUT_B = r'D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\00_CONTROL\qc_probe\qc_addr_lock_runB.json'

def check(label, va_hex, expected_hex, expected_off=None):
    va = int(va_hex, 16)
    exp = bytes.fromhex(expected_hex.replace(' ', ''))
    off = pe.va2off(va)
    sec = pe.sec_of_va(va)
    got = pe.read_va(va, len(exp)) if off is not None else None
    rec = dict(label=label, va=va_hex, section=sec, file_offset=off,
               expected_offset=expected_off, offset_ok=(expected_off is None or off == expected_off),
               expected_hex=expected_hex,
               measured_hex=(got.hex() if got is not None else None),
               bytes_ok=(got == exp))
    return rec

results_B = []

# ===== RUN B: wszystkie 64 wpisy S14 =====
s14 = json.load(open(r'D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\01_RAW\S14_VA_EVIDENCE.json'))
for e in s14['evidence']:
    results_B.append(check(e['label'], e['va'], e['raw_bytes_hex'], e.get('file_offset')))
n_ok = sum(1 for r in results_B if r['bytes_ok'] and r['offset_ok'])
print('RUN B S14: %d/%d zgodnych bajtowo (VA->offset + bajty)' % (n_ok, len(results_B)))
for r in results_B:
    if not (r['bytes_ok'] and r['offset_ok']):
        print('  MISMATCH:', r)
json.dump(results_B, open(OUT_B, 'w'), indent=1)

# ===== RUN A: kluczowe VA z VA_EVIDENCE_REGISTRY + raportu =====
results_A = []
def A(label, va, hexs, off=None):
    results_A.append(check(label, va, hexs, off))

# A5: wzorce 4508 (disp32!)
A('4508 LEA #1 @0x00532709', '0x00532709', '8d8c249c110000')
A('4508 LEA #2 @0x00532766', '0x00532766', '8d8c249c110000')
A('4508 MOV [ESI+0x119C] @0x0083427C', '0x0083427C', '899e9c110000')
# A6: settery placementu (wejsca funkcji)
A('FUN_00730f90 entry', '0x00730F90', '')  # filled below by dump
# A2: string CharacterPosition — najpierw znajdziemy VA skryptem stringowym; tu na razie body funkcji
A('FUN_006b9970 entry', '0x006B9970', '')
A('FUN_006b4c50 entry', '0x006B4C50', '')
# A7: tworca instancji
A('FUN_006cb6f0 entry', '0x006CB6F0', '')
A('FUN_006cb6f0 pump CALL @0x006CB7CF', '0x006CB7CF', 'e82cdfffff')
A('FUN_006fa8b0 ctor vft', '0x006FA8B0', 'c700b864a800')
A('FUN_006fa8b0 ctor [EAX+8]=ECX', '0x006FA8B3', '894808')
A('FUN_006fa8d0 dtor vft base', '0x006FA8D0', '')
A('FUN_006cb020 entry', '0x006CB020', '')
A('FUN_006cb3c0 entry', '0x006CB3C0', '')
A('FUN_006f2af0 FLD const1.0', '0x006F2AF0', 'd90534b3a700')
# A8: ArkObject ctor
A('FUN_00726e70 entry', '0x00726E70', '')
# A9: oracle NiAVObject
A('m_bAppCulled read @0x007C053A', '0x007C053A', '8a4520')
A('LEA ECX,[EBP+0x5C] @0x007C05B3 (m_localTranslate)', '0x007C05B3', '8d4d5c')
A('LEA ECX,[EBP+0x38] (m_localRotate)', '0x007C05A0', '')  # dump okolicy
A('PUSH m_worldTranslate strptr @0x007C0620', '0x007C0620', '')
A('m_kWorldBound PUSH/LEA @0x007C06C6', '0x007C06C6', '')
# E.2: builder context
A('FUN_00567770 LEA ECX,[ESP+0xB4] @0x00567906', '0x00567906', '8d8c24b4000000')
A('FUN_00846840 entry', '0x00846840', '6aff68b07ea20064a1000000005083ec')
# E.6 vtablee — sprawdzimy zawartosc (pierwszy wpis = ctor lub expected pointer)
A('ArkObject vft @0x00A86B48 head', '0x00A86B48', '40477600')
A('ArkObjectClass vft @0x00A86850 head', '0x00A86850', '')
A('ArkPortalCell vft @0x00A91CF8 head', '0x00A91CF8', '')
A('ArkModelResourceInstanceRef vft @0x00A864B8 head', '0x00A864B8', 'b064' if False else '')
A('NiAVObject vft @0x00A8D534 head', '0x00A8D534', '')
# 0x00511245 hardcode 11769 (0x2DF9) - klasyfikacja #1
A('hardcode 11769 @0x00511245', '0x00511245', '')
# 0x004C859A pump #1
A('pump callsite #1 @0x004C859A', '0x004C859A', '')
A('lookup callsite #1 @0x00511252', '0x00511252', '')
A('pump callsite #4 @0x006CB7CF dup ok', '0x006CB7CF', 'e82cdfffff')

for r in results_A:
    if r['measured_hex'] is None:
        print('A-DUMP %s @%s off=%s : %s' % (r['label'], r['va'], r['file_offset'], r['measured_hex'] if r['measured_hex'] else 'POZA'))
    else:
        print('A-DUMP %s @%s [%s] : %s%s' % (r['label'], r['va'], r['section'], r['measured_hex'],
              (' == OK' if r['expected_hex'] and r['bytes_ok'] else (' (oczekiwano %s)' % r['expected_hex'] if r['expected_hex'] else ' (dump)'))))

json.dump(results_A, open(OUT_A, 'w'), indent=1)
