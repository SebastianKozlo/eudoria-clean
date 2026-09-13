# qc_b3_sample.py — probki B3 (FUN_00845f70 callers), granice funkcji, A3 sample #13/#pump13
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']
data = pe.data

def func_start(va):
    """przeszukaj wstecz za padding cc cc cc lub poprzednia funkcja: heurystyka - najblizszy 'cc cc' przed va"""
    off = pe.va2off(va)
    i = off
    while i > 0x1000:
        if data[i-1] == 0xCC and data[i] != 0xCC:
            start = i
            # pomin wiecej cc
            while data[start-1] == 0xCC:
                start -= 1
            va_s = None
            for s in pe.sections:
                if s['rawptr'] <= start < s['rawptr'] + s['rawsize']:
                    va_s = pe.image_base + s['vaddr'] + (start - s['rawptr'])
                    break
            return va_s
        i -= 1
    return None

print('=== B3: funkcje zawierajace call-site FUN_00845f70 (probka 8 + outliery) ===')
sites = [0x004387E4, 0x0043F77D, 0x004B534A, 0x0048FA06, 0x00510684, 0x00514381, 0x00514926, 0x00515B44, 0x0084738C, 0x0084739F, 0x004C5FCF, 0x004F7127, 0x005044B9, 0x0056984B, 0x005B6F95, 0x0044045A]
for s in sites:
    fs = func_start(s)
    print('  call-site 0x%08X -> funkcja ~0x%08X (offset +%X)' % (s, fs, s - fs))

print()
print('=== A3 sample #13: FUN_006e2610 (0x006E28E4 lookup) - czyta avatar-id? ===')
# cialo funkcji: 0x006E2610..do najblizszego cc-cc
off = pe.va2off(0x006E2610)
end = off
while not (data[end] == 0xCC and data[end+1] == 0xCC):
    end += 1
    if end - off > 0x3000: break
body = data[off:end]
body_va = 0x006E2610
print('FUN_006e2610 body: 0x%08X-0x%08X (%d B)' % (body_va, body_va + len(body), len(body)))
for tgt_name, tgt in [('FUN_004926e0 (avatar-id)', 0x004926E0), ('FUN_00977780 (avatar-id)', 0x00977780),
                      ('FUN_0072f580 (lookup)', 0x0072F580), ('FUN_005670a0 (copy)', 0x005670A0)]:
    n = 0
    for i in range(len(body) - 5):
        if body[i] == 0xE8:
            rel = struct.unpack_from('<i', body, i + 1)[0]
            t = body_va + i + 5 + rel
            if t == tgt:
                n += 1
                print('   CALL %s @0x%08X' % (tgt_name, body_va + i))
    if n == 0:
        print('   %s: 0 wywolan w body' % tgt_name)

print()
print('=== A3 pump #13: FUN_0094b1d0 - stringi wegetacji ===')
off = pe.va2off(0x0094B1D0)
end = off
while not (data[end] == 0xCC and data[end+1] == 0xCC):
    end += 1
    if end - off > 0x2000: break
body = data[off:end]
body_va = 0x0094B1D0
print('FUN_0094b1d0 body: 0x%08X-0x%08X (%d B)' % (body_va, body_va + len(body), len(body)))
for strva, name in [(0x00A97DF4, 'ArkVegetationClient::GetModel'), (0x00A97D8C, '~ArkVegetationModelClient?')]:
    pat = struct.pack('<I', strva)
    i = body.find(pat)
    if i >= 0:
        print('   ref do 0x%08X (%s) @0x%08X' % (strva, name, body_va + i))
    else:
        print('   brak refu do 0x%08X (%s) w body' % (strva, name))
# jakie stringi w ogole pushuje
for i in range(len(body) - 5):
    if body[i] == 0x68:
        imm = struct.unpack_from('<I', body, i + 1)[0]
        if 0x00A75000 <= imm < 0x00B6C000:
            o2 = pe.va2off(imm)
            s = data[o2:o2+48]
            s = s.split(b'\x00')[0].decode('ascii', 'replace')
            print('   PUSH 0x%08X @0x%08X = %r' % (imm, body_va + i, s))

print()
print('=== A7: FUN_006cb020 — stringi i format "<id>__<name>" ===')
off = pe.va2off(0x006CB020)
end = off
while not (data[end] == 0xCC and data[end+1] == 0xCC):
    end += 1
    if end - off > 0x3000: break
body = data[off:end]
body_va = 0x006CB020
print('FUN_006cb020 body: 0x%08X-0x%08X (%d B)' % (body_va, body_va + len(body), len(body)))
for i in range(len(body) - 5):
    if body[i] == 0x68:
        imm = struct.unpack_from('<I', body, i + 1)[0]
        if 0x00A75000 <= imm < 0x00B6C000:
            o2 = pe.va2off(imm)
            s = data[o2:o2+48]
            s = s.split(b'\x00')[0].decode('ascii', 'replace')
            print('   PUSH 0x%08X @0x%08X = %r' % (imm, body_va + i, s))
# wywolania w body
for i in range(len(body) - 5):
    if body[i] == 0xE8:
        rel = struct.unpack_from('<i', body, i + 1)[0]
        t = body_va + i + 5 + rel
        if t in (0x007B6C30, 0x006CB3C0, 0x006F33A0):
            print('   CALL 0x%08X @0x%08X' % (t, body_va + i))

print()
print('=== A7: FUN_006cb3c0 — stringi (pending-attach) ===')
off = pe.va2off(0x006CB3C0)
end = off
while not (data[end] == 0xCC and data[end+1] == 0xCC):
    end += 1
    if end - off > 0x2000: break
body = data[off:end]
body_va = 0x006CB3C0
print('FUN_006cb3c0 body: 0x%08X-0x%08X (%d B)' % (body_va, body_va + len(body), len(body)))
for i in range(len(body) - 5):
    if body[i] == 0x68:
        imm = struct.unpack_from('<I', body, i + 1)[0]
        if 0x00A75000 <= imm < 0x00B6C000:
            o2 = pe.va2off(imm)
            s = data[o2:o2+48]
            s = s.split(b'\x00')[0].decode('ascii', 'replace')
            print('   PUSH 0x%08X @0x%08X = %r' % (imm, body_va + i, s))

print()
print('=== granica: czy 0x0058E0B7 jest w FUN_0058db50? ===')
fs = func_start(0x0058E0B7)
print('func_start(0x0058E0B7) = 0x%08X (offset wewnatrz: %X)' % (fs, 0x0058E0B7 - fs))
fs2 = func_start(0x00515345)
print('func_start(0x00515345) = 0x%08X (offset: %X)' % (fs2, 0x00515345 - fs2))
fs3 = func_start(0x005B7567)
print('func_start(0x005B7567) = 0x%08X (offset: %X)' % (fs3, 0x005B7567 - fs3))
fs4 = func_start(0x004B534A)
print('func_start(0x004B534A) = 0x%08X (offset: %X)' % (fs4, 0x004B534A - fs4))
fs5 = func_start(0x0084738C)
print('func_start(0x0084738C) = 0x%08X (offset: %X)' % (fs5, 0x0084738C - fs5))
