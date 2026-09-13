# qc_b6_bound.py — test granicy 0xB9: czy producent jest statycznie osiagalny?
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']
data = pe.data

def callers_of(target):
    hits = []
    for i in range(len(text)-5):
        if text[i] == 0xE8:
            rel = struct.unpack_from('<i', text, i+1)[0]
            t = text_va + i + 5 + rel
            if t == target:
                hits.append(text_va + i)
    return hits

print('=== callerzy FUN_004b1890 (enqueue ring) ===')
for h in callers_of(0x004B1890):
    off = pe.va2off(h)
    ctx = data[off-28:off+8]
    print('  CALL @0x%08X  ctx[-28..+8]: %s' % (h, ctx.hex()))

print()
print('=== wszystkie imm 0xB9 (b9 00 00 00) w .text ===')
pat = bytes.fromhex('b9000000')
start = 0
hits = []
while True:
    i = text.find(pat, start)
    if i < 0: break
    hits.append(text_va + i)
    start = i + 1
print('liczba: %d' % len(hits))
for h in hits:
    off = pe.va2off(h)
    prev = text[pe.va2off(h)-1] if h > text_va else 0
    prev2 = text[pe.va2off(h)-2]
    prev3 = text[pe.va2off(h)-3]
    # rozpoznaj PUSH imm8: 6a b9 ; PUSH imm32: 68 b9 00 00 00; MOV reg,imm32: b8+r
    desc = '?'
    if prev == 0x68: desc = 'PUSH imm32 0xB9'
    elif prev == 0x6A: desc = 'PUSH imm8 0xB9'
    elif prev in (0xB8,0xB9,0xBA,0xBB,0xBC,0xBE,0xBF): desc = 'MOV reg32,0xB9'
    elif prev in (0x05,0x3D): desc = 'ADD/CMP EAX,0xB9'
    elif prev == 0x81 and prev2 in (0xF8,0xF9,0xFA,0xFB,0xFE,0xFF): desc = 'CMP reg,0xB9'
    print('  @0x%08X prev=%s: %s  ctx=%s' % (h, '%02x %02x' % (prev3, prev2), desc, data[off-10:off+10].hex()))

print()
print('=== PUSH imm8 0xB9 (6a b9) w .text ===')
pat2 = bytes.fromhex('6ab9')
start = 0
cnt = 0
while True:
    i = text.find(pat2, start)
    if i < 0: break
    va = text_va + i
    off = pe.va2off(va)
    print('  @0x%08X ctx=%s' % (va, data[off-10:off+14].hex()))
    cnt += 1
    start = i + 1
print('liczba: %d' % cnt)

print()
print('=== vtable executora 0x00A7C1FC — odczyty (kto czyta slot Execute)? ===')
vt = struct.pack('<I', 0x00A7C1FC)
start = 0
while True:
    i = text.find(vt, start)
    if i < 0: break
    va = text_va + i
    print('  ref @0x%08X ctx=%s' % (va, data[pe.va2off(va)-12:pe.va2off(va)+16].hex()))
    start = i + 1
# tez w .rdata/.data
for secname in ('.rdata', '.data'):
    sec, s_ = pe.section_bytes(secname)
    sva = pe.image_base + s_['vaddr']
    start = 0
    while True:
        i = sec.find(vt, start)
        if i < 0: break
        print('  ref w %s @0x%08X' % (secname, sva + i))
        start = i + 1

print()
print('=== [comm+0x28]-indirect: wywolania przez wskaznik executora (pattern call [reg+0x28]+slot)? ===')
# 8b 46 28 (MOV EAX,[ESI+0x28]) ... ff 50/51/xx (CALL [EAX+4]) — szukaj w .text korelacji
# prosty probe: wszystkie wystapienia '46 28' nastepowane w ciagu 64B przez ff 5x
pat3 = bytes.fromhex('4628')
start = 0
found = 0
while True:
    i = text.find(pat3, start)
    if i < 0: break
    window = text[i:i+96]
    j = window.find(bytes.fromhex('ff50'))
    k = window.find(bytes.fromhex('ff51'))
    if j >= 0 or k >= 0:
        va = text_va + i
        print('  kandydat @0x%08X: %s' % (va, text[i-8:i+40].hex()))
        found += 1
        if found > 12: break
    start = i + 1
print('kandydatow (limit 12): %d' % found)
