# qc_pe.py — WLASNY parser PE dla QC (PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913)
# Audytor wewnetrzny QC: niezalezne od narzedzi executora odczyty surowych bajtow.
# READ-ONLY wobec binarium. Zero zaleznosci zewnetrznych (sama stdlib).

import struct, sys

class PE:
    def __init__(self, path):
        self.path = path
        with open(path, 'rb') as f:
            self.data = f.read()
        d = self.data
        # DOS header
        if d[0:2] != b'MZ':
            raise ValueError('brak MZ')
        e_lfanew = struct.unpack_from('<I', d, 0x3C)[0]
        if d[e_lfanew:e_lfanew+4] != b'PE\x00\x00':
            raise ValueError('brak PE\\0\\0')
        coff = e_lfanew + 4
        machine, nsec, tdstamp, symptr, nsym, optsz, chars = struct.unpack_from('<HHIIIHH', d, coff)
        self.machine = machine
        self.nsec = nsec
        self.chars = chars
        opt = coff + 20
        magic = struct.unpack_from('<H', d, opt)[0]
        if magic != 0x10B:
            raise ValueError('to nie PE32 (magic=0x%X)' % magic)
        self.magic = magic
        (self.majlinker, self.minlinker, sizeofcode, sizeofinitdata, sizeofuninit,
         self.entry_rva, baseofcode, baseofdata) = struct.unpack_from('<BBIIIIII', d, opt+2)
        self.image_base = struct.unpack_from('<I', d, opt+28)[0]
        self.secalign = struct.unpack_from('<I', d, opt+32)[0]
        self.filealign = struct.unpack_from('<I', d, opt+36)[0]
        self.subsys = struct.unpack_from('<I', d, opt+44+16)[0]
        self.sizeofimage = struct.unpack_from('<I', d, opt+56)[0]
        self.sizeofheaders = struct.unpack_from('<I', d, opt+60)[0]
        self.dllchars = struct.unpack_from('<H', d, opt+70)[0]
        # data directories (16)
        ddoff = opt + 96
        self.datadirs = []
        for i in range(16):
            rva, size = struct.unpack_from('<II', d, ddoff + i*8)
            self.datadirs.append((rva, size))
        # sections
        self.sections = []
        secoff = opt + struct.unpack_from('<H', d, coff+16+2)[0] + 4  # hmm, standard: SizeOfOptionalHeader at coff+16
        # actually SizeOfOptionalHeader is at coff+16 (H)
        optsize = struct.unpack_from('<H', d, coff+16)[0]
        secoff = opt + optsize
        for i in range(nsec):
            name = d[secoff:secoff+8].rstrip(b'\x00').decode('ascii', 'replace')
            vsize, vaddr, rawsize, rawptr, relptr, lineptr, nreloc, nlineno, schars = struct.unpack_from('<IIIIIIHHI', d, secoff+8)
            self.sections.append(dict(name=name, vsize=vsize, vaddr=vaddr, rawsize=rawsize, rawptr=rawptr, chars=schars))
            secoff += 40
        self.size = len(d)

    def va2off(self, va):
        rva = va - self.image_base
        return self.rva2off(rva)

    def rva2off(self, rva):
        for s in self.sections:
            if s['vaddr'] <= rva < s['vaddr'] + max(s['vsize'], s['rawsize']):
                if s['rawsize'] == 0:
                    return None
                off = s['rawptr'] + (rva - s['vaddr'])
                if off - s['rawptr'] >= s['rawsize']:
                    return None  # w .bss poza raw
                return off
        return None

    def sec_of_va(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s['vaddr'] <= rva < s['vaddr'] + max(s['vsize'], s['rawsize']):
                return s['name']
        return None

    def read_va(self, va, n):
        off = self.va2off(va)
        if off is None:
            return None
        return self.data[off:off+n]

    def read_off(self, off, n):
        return self.data[off:off+n]

    def section_bytes(self, name):
        for s in self.sections:
            if s['name'] == name:
                return self.data[s['rawptr']:s['rawptr']+s['rawsize']], s
        return None, None

    def hexdump(self, va, n):
        b = self.read_va(va, n)
        if b is None:
            return '<POZA OBRAZEM VA=0x%08X>' % va
        return ' '.join('%02x' % x for x in b)

def load(exe=r'D:\Eudoria_Reconstruction\pcg_install\Entropia.exe'):
    return PE(exe)

if __name__ == '__main__':
    pe = load()
    print('rozmiar pliku :', pe.size)
    print('image base    : 0x%08X' % pe.image_base)
    print('entry RVA     : 0x%08X  (VA 0x%08X)' % (pe.entry_rva, pe.image_base + pe.entry_rva))
    print('dll chars     : 0x%04X (ASLR bit 0x40 = %s)' % (pe.dllchars, 'ON' if pe.dllchars & 0x40 else 'OFF'))
    print('sekcje:')
    for s in pe.sections:
        print('  %-8s VA 0x%08X-0x%08X  vsize 0x%X  raw 0x%X..0x%X  chars 0x%08X' % (
            s['name'], pe.image_base+s['vaddr'], pe.image_base+s['vaddr']+s['vsize'], s['vsize'], s['rawptr'], s['rawptr']+s['rawsize'], s['chars']))
    for i,(rva,size) in enumerate(pe.datadirs[:6]):
        if rva:
            print('datadir[%d] rva 0x%X size 0x%X' % (i, rva, size))
