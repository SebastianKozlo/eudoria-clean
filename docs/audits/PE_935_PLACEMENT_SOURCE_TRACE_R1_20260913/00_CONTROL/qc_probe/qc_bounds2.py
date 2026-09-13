# qc_bounds2.py — poprawiona detekcja granic funkcji (>=3 x 0xCC) + droga A/B/C
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
data = pe.data
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']

def real_boundary_before(va):
    """najdalszy punkt wstecz, za ktorym jest >=3 x 0xCC padding; zwraca VA poczatku bloku kodu po paddingu"""
    off = pe.va2off(va)
    i = off
    while i > 0x1000:
        if data[i-3:i] == b'\xcc\xcc\xcc' and data[i] != 0xCC:
            return pe.image_base + (0x1000) + (i - 4096)  # RVA = off - rawptr + vaddr
        i -= 1
    return None

def va_of_off(off):
    for s in pe.sections:
        if s['rawptr'] <= off < s['rawptr'] + s['rawsize']:
            return pe.image_base + s['vaddr'] + (off - s['rawptr'])
    return None

def func_start_strict(va):
    off = pe.va2off(va)
    i = off
    while i > 0x1000:
        if data[i-3:i] == b'\xcc\xcc\xcc' and data[i] != 0xCC:
            return va_of_off(i)
        i -= 1
    return None

def call_rel32_from(va_from, va_to):
    n = 0
    off = pe.va2off(va_from)
    i = off
    end = off
    while not (data[end] == 0xCC and data[end+1] == 0xCC and data[end+2] == 0xCC):
        end += 1
        if end - off > 0x8000: break
    body = data[off:end]
    bv = va_from
    for i in range(len(body) - 5):
        if body[i] == 0xE8:
            rel = struct.unpack_from('<i', body, i + 1)[0]
            t = bv + i + 5 + rel
            if t == va_to:
                n += 1
    return n

print('=== poprawione granice ===')
for site, claim_name, claim_start in [
    (0x0058E0B7, 'droga A -> FUN_00567c50', 0x0058DB50),
    (0x005B7567, 'droga B -> FUN_00567c50', 0x005B72C0),
    (0x00515345, 'droga C -> FUN_00567c50', 0x00514EF0),
    (0x004B534A, 'FUN_00845f70 caller (B3)', None),
    (0x0084738C, 'FUN_00845f70 caller (B3)', 0x00847270),
    (0x0084739F, 'FUN_00845f70 caller (B3)', 0x00847270),
    (0x00469557, 'PUSH 0x6A4 (A6)', 0x00468910),
    (0x00438890, 'PUSH 0x6A5 (A6)', 0x004387A0),
]:
    fs = func_start_strict(site)
    inside = (fs is not None and claim_start is not None and fs <= claim_start <= site)
    print('  site 0x%08X: blok-kodu od 0x%s; claim %s -> %s' % (
        site, ('0x%08X' % fs) if fs else '?', claim_name,
        ('W SEKCIE OK (fs<=claim<=site)' if inside else 'SPRAWDZIC')))

print()
print('=== droga A: ile razy FUN_00468910 woła FUN_0058db50? ===')
n = call_rel32_from(0x00468910, 0x0058DB50)
print('FUN_00468910 -> FUN_0058db50: %d call-site(s)' % n)

print()
print('=== droga B: FUN_004b18d0 case 0xB9 -> FUN_005b72c0? ===')
# cialo FUN_004b18d0
off = pe.va2off(0x004B18D0)
end = off
while not (data[end] == 0xCC and data[end+1] == 0xCC and data[end+2] == 0xCC):
    end += 1
    if end - off > 0x8000: break
body = data[off:end]
bv = 0x004B18D0
print('FUN_004b18d0 body: 0x%08X-0x%08X (%d B)' % (bv, bv+len(body), len(body)))
# przejrzyj wszystkie CALLy i immediates 0xB9
for i in range(len(body) - 5):
    if body[i] == 0xE8:
        rel = struct.unpack_from('<i', body, i + 1)[0]
        t = bv + i + 5 + rel
        print('   CALL @0x%08X -> 0x%08X' % (bv + i, t))
# bajty b9 00 00 00 (case 0xB9 jako imm32?) i 3d b9 00 00 00 / 81 f9
for pat, name in [(bytes.fromhex('3db9000000'), 'CMP EAX,0xB9'),
                  (bytes.fromhex('81f9b9000000'), 'CMP ECX,0xB9'),
                  (bytes.fromhex('81fb b9000000'), 'CMP EBX,0xB9'),
                  (bytes.fromhex('81feb9000000'), 'CMP ESI,0xB9'),
                  (bytes.fromhex('81ffb9000000'), 'CMP EDI,0xB9'),
                  (bytes.fromhex('b9b9000000'), 'MOV ECX,0xB9')]:
    i = body.find(pat)
    if i >= 0:
        print('   %s @0x%08X' % (name, bv + i))

print()
print('=== B5: FUN_005b72c0 -> FUN_00567c50 call w body? ===')
off = pe.va2off(0x005B72C0)
end = off
while not (data[end] == 0xCC and data[end+1] == 0xCC and data[end+2] == 0xCC):
    end += 1
    if end - off > 0x8000: break
body = data[off:end]
bv = 0x005B72C0
print('FUN_005b72c0 body: 0x%08X-0x%08X (%d B)' % (bv, bv+len(body), len(body)))
for i in range(len(body) - 5):
    if body[i] == 0xE8:
        rel = struct.unpack_from('<i', body, i + 1)[0]
        t = bv + i + 5 + rel
        if t == 0x00567C50:
            print('   CALL FUN_00567c50 @0x%08X' % (bv + i))
