# qc_xref.py — xrefy stringow i call-rel32 (RUN A: A2, A3, A6)
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']

def call_rel32_targets(target_va):
    """znajdz wszystkie CALL rel32 (e8) w .text w kierunku target_va"""
    hits = []
    n = len(text)
    for i in range(n - 5):
        if text[i] == 0xE8:
            rel = struct.unpack_from('<i', text, i + 1)[0]
            t = text_va + i + 5 + rel
            if t == target_va:
                hits.append(text_va + i)
    return hits

def imm32_refs(va):
    """znajdz odwolania imm32 do va (push/mov/dword literal) w .text: szukaj 4-bajtowego LE"""
    pat = struct.pack('<I', va)
    hits = []
    start = 0
    while True:
        i = text.find(pat, start)
        if i < 0: break
        # poprzedni bajt: 68 (push imm), b8+ (mov reg), 3d, itp.
        prev = text[i-1] if i > 0 else 0
        hits.append((text_va + i, prev))
        start = i + 1
    return hits

print('=== A2: xrefy do "CharacterPosition" @0x00A8548C ===')
for va, prev in imm32_refs(0x00A8548C):
    prev_desc = {0x68: 'PUSH imm', 0xB8: 'MOV EAX', 0xB9: 'MOV ECX', 0xBA: 'MOV EDX', 0xBB: 'MOV EBX', 0xBE: 'MOV ESI', 0xBF: 'MOV EDI', 0x05: 'ADD EAX', 0x3D: 'CMP EAX'}.get(prev, 'prev=0x%02x' % prev)
    print('  0x%08X (%s)' % (va, prev_desc))
    # kontekst 32 bajty przed i po
    off = pe.va2off(va) 
    ctx = pe.data[off-24:off+12]
    print('    ctx: %s' % ' '.join('%02x' % x for x in ctx))

print()
print('=== A2: callerzy FUN_006b4c50 (body ~0x006B4C50..0x006B5???). CALL rel32 do 0x006B4C50 ===')
for h in call_rel32_targets(0x006B4C50):
    print('  CALL @0x%08X -> 0x006B4C50' % h)
    off = pe.va2off(h)
    ctx = pe.data[off-16:off+8]
    print('    ctx: %s' % ' '.join('%02x' % x for x in ctx))

print()
print('=== A3: callerzy lookupu FUN_0072f580 (CALL rel32) ===')
lut = call_rel32_targets(0x0072F580)
print('  liczba CALL rel32 -> 0x0072F580: %d' % len(lut))
for h in lut:
    print('   0x%08X' % h)

print()
print('=== A3: callerzy pumpu FUN_006c9700 (CALL rel32) ===')
pmp = call_rel32_targets(0x006C9700)
print('  liczba CALL rel32 -> 0x006C9700: %d' % len(pmp))
for h in pmp:
    print('   0x%08X' % h)

print()
print('=== A6: FUN_00846840 body — immediate 0x6A4/0x6A5/0x6A8/0x6A9 ===')
body = pe.read_va(0x00846840, 0x350)
for imm in (0x6A4, 0x6A5, 0x6A8, 0x6A9, 0x6AC, 0x23):
    pat = struct.pack('<I', imm)
    hits = []
    start = 0
    while True:
        i = body.find(pat, start)
        if i < 0: break
        hits.append(0x00846840 + i)
        start = i + 1
    print('  imm 0x%04X: %d trafien w body 0x00846840-0x00846B8F' % (imm, len(hits)))
    for h in hits[:8]:
        off = pe.va2off(h)
        prev = pe.data[off-1]
        print('     @0x%08X prev=0x%02x ctx=%s' % (h, prev, pe.data[off-6:off+8].hex()))
