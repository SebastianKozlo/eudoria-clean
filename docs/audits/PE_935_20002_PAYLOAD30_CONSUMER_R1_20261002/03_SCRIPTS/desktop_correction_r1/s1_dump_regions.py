# s1_dump_regions.py — raw-byte dumps of the DESKTOP_CORRECTION_R1 scope windows
# Static analysis only. Self-contained; imports only the sibling pe_parse module.
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

pe = pe_parse.PE32()

REGIONS = [
    ("reg_site_ctx",      0x761540, 0x761760),  # ArkParameterArmor schema ctor region incl. tag-0x11 registration
    ("factory_type1",     0x977a50, 0x977b40),  # FUN_00977a50 (lead: type-1 factory)
    ("reader_type1_lead", 0x9777f0, 0x9778a0),  # FUN_009777F0 (lead: selected type-1 reader)
    ("dispatch",          0x75f660, 0x75f6c0),  # FUN_0075f660 value-read dispatch
    ("desc_init",         0x75f5c0, 0x75f5e0),  # FUN_0075f5c0 descriptor initializer
    ("register",          0x70cbc0, 0x70cc14),  # FUN_0070cbc0 registration
    ("insert",            0x70c980, 0x70ca50),  # FUN_0070c980 descriptor-table insert
    ("lookup",            0x70c180, 0x70c210),   # FUN_0070c180 descriptor lookup
    ("advance_helper",    0x40de60, 0x40dea0),  # FUN_0040de60 cursor advance helper
    ("payload_prep",      0x70dcf0, 0x70dd40),  # FUN_0070dcf0 (advance 8 lead)
    ("factory_type2",     0x977ad0, 0x977bc0),  # FUN_00977ad0 (type-2 factory lead)
    ("factory_type4",     0x40a290, 0x40a340),  # FUN_0040a290 (type-4 factory lead)
    ("factory_type3",     0x977ce0, 0x977d80),  # FUN_00977ce0 (type-3 factory lead)
    ("fallback_reader",   0x412540, 0x412570),  # FUN_00412540 fallback type-1 reader
    ("fallback_switch",   0x4129c0, 0x412a30),  # FUN_004129c0 fallback scalar switch
    ("tlv_loop",          0x726900, 0x726b40),  # FUN_00726900 TLV loop
]

out = []
for name, lo, hi in REGIONS:
    fo = pe.va_to_fo(lo, hi - lo)
    data = pe.read_va(lo, hi - lo)
    out.append("=== %s  VA 0x%08X..0x%08X  FO 0x%08X..0x%08X ===" % (name, lo, hi, fo, fo + (hi - lo)))
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        va = lo + i
        hexs = " ".join("%02X" % b for b in chunk)
        out.append("%08X  %-48s  %s" % (va, hexs, "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)))
    out.append("")

print("\n".join(out))
