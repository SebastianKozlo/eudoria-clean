# qc_a6_switch.py — rozstrzygniecie switch 0x6A4 w FUN_00846840 + Models.bnt name check
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()

body = pe.read_va(0x00846840, 0x350)
print('=== poszukiwanie roznych form immediate 1700/1701/1704/1705 w body FUN_00846840 ===')
pats = {
    'a4 06 00 00 (0x6A4)': bytes.fromhex('a4060000'),
    'a5 06 00 00 (0x6A5)': bytes.fromhex('a5060000'),
    'a8 06 00 00 (0x6A8)': bytes.fromhex('a8060000'),
    'a9 06 00 00 (0x6A9)': bytes.fromhex('a9060000'),
    '5c f9 ff ff (-0x6A4)': bytes.fromhex('5cf9ffff'),
    '2c f9 ff ff (0x6A4 w LEA sub?)': bytes.fromhex('2cf9ffff'),
}
for name, p in pats.items():
    hits = []
    start = 0
    while True:
        i = body.find(p, start)
        if i < 0: break
        hits.append(0x00846840 + i)
        start = i + 1
    print('%-28s: %d' % (name, len(hits)))
    for h in hits:
        off = pe.va2off(h)
        print('    @0x%08X ctx: %s' % (h, pe.data[off-8:off+12].hex()))

# caly .text — gdzie wystepuja 0x6A4..0x6A9 jako imm32 (dla A6: "jako imm w call-site'ach")
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']
print()
print('=== .text: imm32 0x6A4/0x6A5/0x6A8/0x6A9 (wszystkie) ===')
for imm in (0x6A4, 0x6A5, 0x6A8, 0x6A9):
    p = struct.pack('<I', imm)
    hits = []
    start = 0
    while True:
        i = text.find(p, start)
        if i < 0: break
        va = text_va + i
        prev = text[i-1]
        prev2 = text[i-2]
        hits.append((va, prev, prev2))
        start = i + 1
    print('imm 0x%04X: %d trafien w .text' % (imm, len(hits)))
    for va, prev, prev2 in hits:
        off = pe.va2off(va)
        ctx = pe.data[off-6:off+8].hex()
        print('    @0x%08X prev=0x%02x,prev2=0x%02x ctx=%s' % (va, prev, prev2, ctx))

print()
print('=== Models.bnt: nazwy plikow (A4/E.7 rozstrzygniecie) ===')
import glob
cands = glob.glob(r'D:\Eudoria_Reconstruction\pcg_install\**\Models.bnt', recursive=True)
print('znalezione Models.bnt:', cands)
for path in cands:
    with open(path, 'rb') as f:
        data = f.read()
    print('rozmiar:', len(data))
    for name in [b'296445.nif', b'460563.nif', b'126740.nif', b'278453.nif']:
        for term, tname in [(b'', 'bez termin'), (b'\n', 'LF'), (b'\x00', 'NUL')]:
            p = name + term
            cnt = data.count(p)
            first = data.find(p)
            print('  %-12s term=%-4s: count=%d first=%d' % (name.decode(), tname, cnt, first))
