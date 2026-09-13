# qc_setter_census.py — census callerow setterow placementu (A6/A3-sample/B2)
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import load
pe = load()
text, tsec = pe.section_bytes('.text')
text_va = pe.image_base + tsec['vaddr']

def call_rel32_targets(target_va):
    hits = []
    n = len(text)
    for i in range(n - 5):
        if text[i] == 0xE8:
            rel = struct.unpack_from('<i', text, i + 1)[0]
            t = text_va + i + 5 + rel
            if t == target_va:
                hits.append(text_va + i)
    return hits

for name, va in [('FUN_00730f60 (init 11 dword)', 0x00730F60),
                 ('FUN_00730f90 (pozycja @+0x08)', 0x00730F90),
                 ('FUN_00730fb0 (rotacja @+0x14)', 0x00730FB0),
                 ('FUN_00730fd0 (@+0x20/+0x24)', 0x00730FD0),
                 ('FUN_006cb020 (instancja nazwana)', 0x006CB020),
                 ('FUN_006f33a0 (rejestracja)', 0x006F33A0),
                 ('FUN_00567770 (builder)', 0x00567770),
                 ('FUN_00567c50 (driver)', 0x00567C50),
                 ('FUN_006f2af0 (reset pending)', 0x006F2AF0),
                 ('FUN_006cb370 (check)', 0x006CB370),
                 ('FUN_007b6c30 (lookup klasy po nazwie)', 0x007B6C30),
                 ('FUN_00457930 (rejestracja z nazwa)', 0x00457930),
                 ('FUN_00845f70 (attr setter, B3)', 0x00845F70),
                 ('FUN_00846840 (attr fetch)', 0x00846840),
                 ('FUN_00846430 (filtr transformu)', 0x00846430),
                 ('FUN_00567b40 (push kolejki)', 0x00567B40),
                 ('FUN_004c5580 (deriver sub-obiektow)', 0x004C5580),
                 ('FUN_004148f0 (rejestracja)', 0x004148F0)]:
    hits = call_rel32_targets(va)
    print('%s -> %d call-site(s): %s' % (name, len(hits), ' '.join('0x%08X' % h for h in hits[:60])))
    print()
