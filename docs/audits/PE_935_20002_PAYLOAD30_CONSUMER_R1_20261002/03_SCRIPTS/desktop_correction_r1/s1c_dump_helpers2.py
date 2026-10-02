# s1c_dump_helpers2.py — second helper context dump (alignment check + reader widths)
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

pe = pe_parse.PE32()

def dump(va, length, label):
    fo = pe.va_to_fo(va, length)
    data = pe.read_va(va, length)
    print("=== %s  VA 0x%08X  FO 0x%08X ===" % (label, va, fo))
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        a = va + i
        print("%08X  %-48s" % (a, " ".join("%02X" % b for b in chunk)))
    print()

dump(0x70C780, 0x60, "vector_append_region_wide")     # alignment context for the CALL target 0x70C7B1
dump(0x7CD4DB, 0x30, "atexit_helper_A_entry")          # exact entry 0x7CD4DB
dump(0x95D336, 0x30, "atexit_helper_B_inner")          # the helper B inner target 0x95D336
dump(0x409ED0, 0x50, "type4_reader_FUN_00409ed0")       # slot target for type-4 (tag 1)
dump(0x9778A0, 0x50, "type3_reader_FUN_009778a0")      # slot target for type-3 (tag 2 schema)
dump(0xA98110, 0x20, "type_descriptor_vftable_region") # RTTI type_info vftable region (context)
