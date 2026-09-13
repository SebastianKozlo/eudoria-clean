# qc_final_bytes.py — pozostale weryfikacje bajtowe B4/B5/B6/B10/A2/A8
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
data = pe.data
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']

def body_of(va, maxb=0x9000):
    off = pe.va2off(va)
    end = off
    while not (data[end] == 0xCC and data[end+1] == 0xCC and data[end+2] == 0xCC):
        end += 1
        if end - off > maxb: break
    return va, data[off:end]

def func_start_strict(va):
    off = pe.va2off(va)
    i = off
    while i > 0x1000:
        if data[i-3:i] == b'\xcc\xcc\xcc' and data[i] != 0xCC:
            for s in pe.sections:
                if s['rawptr'] <= i < s['rawptr'] + s['rawsize']:
                    return pe.image_base + s['vaddr'] + (i - s['rawptr'])
        i -= 1
    return None

def calls_in_body(bv, body, targets):
    out = []
    for i in range(len(body)-5):
        if body[i] == 0xE8:
            rel = struct.unpack_from('<i', body, i+1)[0]
            t = bv + i + 5 + rel
            if t in targets:
                out.append((bv+i, t))
    return out

print('=== A2: FUN_006b9970 — zapis [obj+0x1DC]? ===')
bv, body = body_of(0x006B9970, 0x4000)
print('body 0x%08X-0x%08X (%d B)' % (bv, bv+len(body), len(body)))
# szukaj bajtow dc 01 00 00 (disp +0x1DC) i d8 01 00 00 (+0x1D8)
for pat, name in [(bytes.fromhex('dc010000'), 'disp +0x1DC'), (bytes.fromhex('d8010000'), 'disp +0x1D8')]:
    start = 0
    while True:
        i = body.find(pat, start)
        if i < 0: break
        print('  %s @0x%08X ctx=%s' % (name, bv+i, body[max(0,i-8):i+12].hex()))
        start = i + 1
# string CharacterPosition usage
for t in calls_in_body(bv, body, [0x006B4C50]):
    print('  CALL FUN_006b4c50 @0x%08X' % t[0])

print()
print('=== A8: FUN_0070bf50 (ArkObjectClass::create) — new(0x58) -> ctor? ===')
bv, body = body_of(0x0070BF50, 0x200)
print('body 0x%08X (%d B): %s' % (bv, len(body), body[:64].hex()))
hits = calls_in_body(bv, body, [0x00726E70])
for h in hits:
    print('  CALL FUN_00726e70 @0x%08X' % h[0])
# push 0x58
i = body.find(bytes.fromhex('6a58'))
if i >= 0:
    print('  PUSH 0x58 @0x%08X' % (bv+i))
i = body.find(bytes.fromhex('6858000000'))
if i >= 0:
    print('  PUSH imm32 0x58 @0x%08X' % (bv+i))

print()
print('=== B4: FUN_00514ef0 — pisanie attr 0x2B/0x2C przez FUN_00845f70 ===')
bv, body = body_of(0x00514EF0, 0x4000)
print('body 0x%08X-0x%08X (%d B)' % (bv, bv+len(body), len(body)))
for i in range(len(body)-5):
    if body[i] == 0xE8:
        rel = struct.unpack_from('<i', body, i+1)[0]
        t = bv + i + 5 + rel
        if t == 0x00845F70:
            ctx = body[max(0,i-24):i+6]
            print('  CALL FUN_00845f70 @0x%08X  prev-24B: %s' % (bv+i, ctx.hex()))
# imm 0x2b / 0x2c jako push imm8 (6a 2b / 6a 2c) lub push imm32
for pat, name in [(bytes.fromhex('6a2b'), 'PUSH 0x2B (imm8)'), (bytes.fromhex('6a2c'), 'PUSH 0x2C (imm8)'),
                  (bytes.fromhex('682b000000'), 'PUSH 0x2B (imm32)'), (bytes.fromhex('682c000000'), 'PUSH 0x2C (imm32)')]:
    start = 0
    while True:
        i = body.find(pat, start)
        if i < 0: break
        print('  %s @0x%08X ctx=%s' % (name, bv+i, body[max(0,i-12):i+14].hex()))
        start = i + 1

print()
print('=== B5: FUN_00419dd0 (CommunicationSubsystem ctor) — executor @+0x28 ===')
bv, body = body_of(0x00419DD0, 0x2000)
print('body 0x%08X-0x%08X (%d B)' % (bv, bv+len(body), len(body)))
hits = calls_in_body(bv, body, [0x004B15F0])
for h in hits:
    ctx = body[h[0]-bv-16:h[0]-bv+20]
    print('  CALL FUN_004b15f0 (executor ctor) @0x%08X ctx=%s' % (h[0], ctx.hex()))
# new(0x34)
i = body.find(bytes.fromhex('6a34'))
if i >= 0:
    print('  PUSH 0x34 @0x%08X ctx=%s' % (bv+i, body[max(0,i-12):i+16].hex()))
# zapis [reg+0x28] po callu: 89 47 28 / 89 46 28 / 89 41 28 / 89 4e 28 / 89 5x 28
for pat, name in [(bytes.fromhex('894728'),'MOV [EDI+0x28],EAX'),(bytes.fromhex('894628'),'MOV [ESI+0x28],EAX'),
                  (bytes.fromhex('894128'),'MOV [ECX+0x28],EAX'),(bytes.fromhex('894e28'),'MOV [ESI+0x28],ECX'),
                  (bytes.fromhex('895e28'),'MOV [ESI+0x28],EBX'),(bytes.fromhex('897e28'),'MOV [EDI+0x28],EBX'),
                  (bytes.fromhex('897f28'),'MOV [EDI+0x28],EDI'),(bytes.fromhex('894f28'),'MOV [EDI+0x28],ECX')]:
    start = 0
    while True:
        j = body.find(pat, start)
        if j < 0: break
        print('  %s @0x%08X ctx=%s' % (name, bv+j, body[max(0,j-16):j+10].hex()))
        start = j + 1

print()
print('=== B5: FUN_004b2950 (Execute) — dispatch do FUN_004b18d0; callerzy Execute ===')
bv, body = body_of(0x004B2950, 0x1000)
print('body 0x%08X-0x%08X (%d B): %s' % (bv, bv+len(body), len(body), body[:48].hex()))
hits = calls_in_body(bv, body, [0x004B18D0, 0x004B1890])
for h in hits:
    print('  CALL 0x%08X @0x%08X' % (h[1], h[0]))
# census callerow FUN_004b2950 (bezposrednich)
n = 0
for i in range(len(text)-5):
    if text[i] == 0xE8:
        rel = struct.unpack_from('<i', text, i+1)[0]
        t = text_va + i + 5 + rel
        if t == 0x004B2950:
            n += 1
            print('  bezposredni CALL Execute @0x%08X' % (text_va + i))
print('  bezposrednich call-site\'ow FUN_004b2950 w .text: %d' % n)
# oraz callerzy FUN_004b18d0
n = 0
for i in range(len(text)-5):
    if text[i] == 0xE8:
        rel = struct.unpack_from('<i', text, i+1)[0]
        t = text_va + i + 5 + rel
        if t == 0x004B18D0:
            n += 1
            print('  bezposredni CALL dispatch @0x%08X' % (text_va + i))
print('  bezposrednich call-site\'ow FUN_004b18d0 w .text: %d' % n)

print()
print('=== B5: FUN_004b1890 (enqueue) — ring push {type,x,payload}? ===')
bv, body = body_of(0x004B1890, 0x200)
print('body: %s' % body[:96].hex())

print()
print('=== B5: jump table dispatchera FUN_004b18d0 — gdzie? ===')
bv, body = body_of(0x004B18D0, 0x800)
# znajdz ff 24 85 (JMP [EAX*4+disp32]) lub ff 24 85/ff 24 95
for pat, name in [(bytes.fromhex('ff2485'), 'JMP [EAX*4+disp32]'), (bytes.fromhex('ff2495'), 'JMP [EDX*4+disp32]')]:
    i = body.find(pat)
    if i >= 0:
        disp = struct.unpack_from('<I', body, i+3)[0]
        table_va = bv + i + 3 - 1 + 1 - 3 + 4 + disp  # disp relatywny do konca instrukcji
        # poprawka: koniec instrukcji = bv+i+3+4
        end_ins = bv + i + 3 + 4
        table_va = end_ins + disp
        print('  %s @0x%08X -> tabela @0x%08X' % (name, bv+i, table_va))
        # odczytaj 38 wpisow
        entries = []
        for k in range(0x26):
            e = pe.read_va(table_va + k*4, 4)
            if e:
                v = struct.unpack('<I', e)[0]
                entries.append(v)
        print('  wpisy 0..37:', ' '.join('%08X' % v for v in entries))
        print('  wpis #23 (case 0xB9 = 0xB9-0xA2=0x17=23): 0x%08X' % entries[0x17] if len(entries) > 0x17 else 'brak')

print()
print('=== B10: census callerow FUN_0048ada0 / FUN_00861240 ===')
for name, va in [('FUN_0048ada0 (getter D dword)', 0x0048ADA0), ('FUN_00861240 (getter D f32)', 0x00861240)]:
    n = 0
    for i in range(len(text)-5):
        if text[i] == 0xE8:
            rel = struct.unpack_from('<i', text, i+1)[0]
            t = text_va + i + 5 + rel
            if t == va:
                n += 1
    print('  %s: %d bezposrednich call-site\'ow w .text' % (name, n))

print()
print('=== B3: funkcja zawierajaca site 0x0044AAFD (f90 caller) ===')
fs = func_start_strict(0x0044AAFD)
print('  func_start_strict(0x0044AAFD) = %s' % ('0x%08X' % fs) if fs else 'brak')
fs2 = func_start_strict(0x0044AB0E)
print('  func_start_strict(0x0044AB0E) = %s' % ('0x%08X' % fs2) if fs2 else 'brak')
# czy FUN_00447630 istnieje jako poczatek bloku? sprawdz jej poczatek
b = pe.read_va(0x00447630, 16)
print('  bajty @0x00447630: %s' % (b.hex() if b else 'poza'))
