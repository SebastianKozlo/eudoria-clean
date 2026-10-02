# s1d_dump_type4.py — type-4 reader width proof + destructor context
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

pe = pe_parse.PE32()

def dump(va, length, label):
    fo = pe.va_to_fo(va, length)
    data = pe.read_va(va, length)
    print("=== %s  VA 0x%08X  FO 0x%08X ===" % (label, va, fo))
    for i in range(0, length, 16):
        chunk = data[i:i + 16]
        print("%08X  %-48s" % (va + i, " ".join("%02X" % b for b in chunk)))
    print()

dump(0x4099C0, 0x60, "type4_inner_FUN_004099c0")
dump(0x4923D0, 0x30, "type4_outer_target_0x4923d0")
dump(0xA744B0, 0x20, "type1_destructor_0xA744B0")
dump(0x409E50, 0x20, "type4_vtable_slot4_FUN_00409e50")
dump(0x70C5A0, 0x60, "region_before_vector_append")
