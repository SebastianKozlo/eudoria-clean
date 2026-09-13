# qc_region_dump.py —okiery wokol podejrzanych adresow (RUN A)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()

def dump(va, n, mark=None):
    b = pe.read_va(va, n)
    print('--- VA 0x%08X (off %s) ---' % (va, pe.va2off(va)))
    for i in range(0, len(b), 16):
        chunk = b[i:i+16]
        va_i = va + i
        marks = ''
        if mark:
            for m in mark:
                if va_i <= m < va_i + len(chunk):
                    marks += ' <-- 0x%08X tutaj' % m
        print('0x%08X  %-47s %s%s' % (va_i, ' '.join('%02x' % x for x in chunk), 
              ''.join(chr(x) if 32 <= x < 127 else '.' for x in chunk), marks))

print('===== FUN_006fa8b0 (ctor ArkModelResourceInstanceRef) 0x006FA8B0 =====')
dump(0x006FA8B0, 0x30)
print()
print('===== GetViewerStrings region 0x007C0500-0x007C0700 =====')
dump(0x007C0500, 0x60, [0x007C053A])
dump(0x007C0560, 0x80, [0x007C0580, 0x007C05B3])
dump(0x007C0600, 0x60, [0x007C0620])
dump(0x007C06A0, 0x50, [0x007C06C6])
print()
print('===== FUN_00567770 region 0x005678E0-0x00567940 =====')
dump(0x005678E0, 0x60, [0x00567906])
dump(0x00567930, 0x40)
print()
print('===== FUN_006cb6f0 new(0xC) region 0x006CB810-0x006CB830 =====')
dump(0x006CB810, 0x30, [0x006CB81B, 0x006CB819])
print()
print('===== FUN_006cb6f0 entry 0x006CB6F0 =====')
dump(0x006CB6F0, 0x40)
print()
print('===== FUN_00730f90/fb0/fd0/f60 =====')
dump(0x00730F60, 0x80)
print()
print('===== FUN_00726e70 (ctor ArkObject) =====')
dump(0x00726E70, 0x60)
print()
print('===== FUN_006b9970 entry =====')
dump(0x006B9970, 0x40)
print()
print('===== FUN_006b4c50 entry =====')
dump(0x006B4C50, 0x40)
print()
print('===== hardcode 11769 @0x00511245 =====')
dump(0x00511230, 0x40, [0x00511245, 0x00511252])
print()
print('===== pump callsite #1 @0x004C859A =====')
dump(0x004C8590, 0x20, [0x004C859A])
print()
print('===== FUN_006cb020 entry =====')
dump(0x006CB020, 0x40)
print()
print('===== FUN_006cb3c0 entry =====')
dump(0x006CB3C0, 0x40)
print()
print('===== FUN_006fa8d0 dtor =====')
dump(0x006FA8D0, 0x30)
print()
print('===== vtable heads =====')
for name, va in [('ArkObject 0x00A86B48', 0x00A86B48), ('ArkObjectClass 0x00A86850', 0x00A86850),
                 ('ArkPortalCell 0x00A91CF8', 0x00A91CF8), ('AMRIR 0x00A864B8', 0x00A864B8),
                 ('ArkSceneObject 0x00A98050', 0x00A98050), ('NiAVObject 0x00A8D534', 0x00A8D534),
                 ('NiNode 0x00A8CCF4', 0x00A8CCF4)]:
    dump(va, 0x10)
