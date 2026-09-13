# qc_b2_b12.py — B2: ctor rekordu FUN_00730700 census; B12: tabele .rdata
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

print('=== B2: callerzy ctora rekordu FUN_00730700 ===')
cs = callers_of(0x00730700)
print('liczba: %d -> %s' % (len(cs), ['0x%08X' % h for h in cs]))
b = pe.read_va(0x00730700, 48)
print('FUN_00730700 bajty:', b.hex())

print()
print('=== B2: FUN_00730f60 vs FUN_00730700 (czy 730700 zawiera init 11 dwordow?) ===')
# czy FUN_00730700 woła FUN_00730f60?
off = pe.va2off(0x00730700)
end = off
while not (data[end] == 0xCC and data[end+1] == 0xCC and data[end+2] == 0xCC):
    end += 1
    if end - off > 0x600: break
body = data[off:end]
bv = 0x00730700
print('FUN_00730700 body: 0x%08X-0x%08X (%d B)' % (bv, bv+len(body), len(body)))
for i in range(len(body)-5):
    if body[i] == 0xE8:
        rel = struct.unpack_from('<i', body, i+1)[0]
        t = bv + i + 5 + rel
        print('  CALL @0x%08X -> 0x%08X' % (bv+i, t))

print()
print('=== B12: struktura tabel .rdata ===')
def dump_ptr_table(va, max_entries, label):
    print('%s @0x%08X:' % (label, va))
    vals = []
    for k in range(max_entries):
        b = pe.read_va(va + k*4, 4)
        if b is None: break
        v = struct.unpack('<I', b)[0]
        vals.append(v)
    # wypisz az dojdziemy do wartoci niskich (nie-pointerw)
    for k, v in enumerate(vals):
        is_code = 0x00401000 <= v < 0x00A745E5
        print('  [%2d] +0x%03X: 0x%08X %s' % (k, k*4, v, '(kod)' if is_code else ''))
        if k > 80: break

# tabela 0x00A7D764 (16 wpisow)
dump_ptr_table(0x00A7D764, 24, 'Tabela CWO-Logic #1')
# tabela 0x00A7D8EC (74)
dump_ptr_table(0x00A7D8EC, 10, 'Tabela #2 @0x00A7D8EC (head)')
# tabela 0x00A7DA34 (72)
dump_ptr_table(0x00A7DA34, 10, 'Tabela #3 @0x00A7DA34 (head)')
# sasiedztwo: co jest przed 0x00A7D764? czy to kontynuacja wiekszej tabeli?
dump_ptr_table(0x00A7D6FC, 24, 'Przed 0x00A7D764 (0x00A7D6FC..)')
