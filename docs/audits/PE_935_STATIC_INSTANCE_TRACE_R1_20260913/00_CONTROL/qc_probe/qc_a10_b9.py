# qc_a10_b9.py — poprawiony skan RTTI (bez terminatora, wszystkie sekcje) + census 20006
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
data = pe.data

print('=== A10 (poprawka): surowe substringy w CALYM pliku (bez terminatorego wymogu) ===')
for pat in [b'Sector', b'Region', b'Entity', b'ArkPortalCell', b'Sectors.xbc', b'Objects.pak', b'Planets.pak',
            b'ArkPortal', b'Portal']:
    hits = []
    start = 0
    while True:
        i = data.find(pat, start)
        if i < 0: break
        va = None
        for s_ in pe.sections:
            if s_['rawptr'] <= i < s_['rawptr'] + s_['rawsize']:
                va = pe.image_base + s_['vaddr'] + (i - s_['rawptr']); break
        ctx = data[max(0,i-12):i+len(pat)+30].split(b'\x00')[0]
        hits.append((va, i, ctx))
        start = i + 1
        if len(hits) > 25: break
    print('%-14s: %d trafien' % (pat.decode(), len(hits)))
    for va, off, ctx in hits[:25]:
        print('   @%s (off %d): %r' % (('0x%08X' % va) if va else 'RAW', off, ctx[:64]))

print()
print('=== B9: census 20006 (0x4E26 LE: 26 4e 00 00) w .text ===')
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']
pats = {bytes.fromhex('264e0000'): 'imm32 0x4E26 (LE)',
        bytes.fromhex('264e000000'): 'imm32+pad',
        }
for p, name in pats.items():
    start = 0
    hits = []
    while True:
        i = text.find(p, start)
        if i < 0: break
        hits.append(text_va + i)
        start = i + 1
    print('%s: %d' % (name, len(hits)))
    for h in hits[:35]:
        off = pe.va2off(h)
        prev = text[off-1]
        prev2 = text[off-2]
        desc = {0x68: 'PUSH', 0x3D: 'CMP EAX', 0x81: 'CMP r32?', 0xB8: 'MOV EAX', 0xB9: 'MOV ECX', 0xBA: 'MOV EDX', 0xBB: 'MOV EBX'}.get(prev, 'prev=%02x' % prev)
        print('   @0x%08X (%s) ctx=%s' % (h, desc, data[off-8:off+12].hex()))

# tez jako push imm8? 20006 nie miesci sie w imm8. PUSH imm32 = 68 26 4E 00 00
print()
print('PUSH imm32 20006 (68 26 4e 00 00):')
p = bytes.fromhex('68264e0000')
start = 0
cnt = 0
while True:
    i = text.find(p, start)
    if i < 0: break
    print('   @0x%08X' % (text_va + i))
    cnt += 1
    start = i + 1
print('   liczba PUSH 20006: %d' % cnt)
