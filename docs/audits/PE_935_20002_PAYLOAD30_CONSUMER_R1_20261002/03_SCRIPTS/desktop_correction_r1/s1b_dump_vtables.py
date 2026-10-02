# s1b_dump_vtables.py — vtable dwords, RTTI walk, helper functions (static context dump)
import sys, os, struct
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

pe = pe_parse.PE32()

def dump(va, length, label):
    fo = pe.va_to_fo(va, length)
    data = pe.read_va(va, length)
    print("=== %s  VA 0x%08X..0x%08X  FO 0x%08X ===" % (label, va, va + length, fo))
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        a = va + i
        print("%08X  %-48s" % (a, " ".join("%02X" % b for b in chunk)))
    print()

def u32(va):
    return pe.read_u32_va(va)

# --- type-1 object (from FUN_00977a50): object 0xBA937C, vtable stored = 0xA9C670, flag 0xBA9380
VT1 = 0x00A9C670
# --- type-2 object (from FUN_00977ad0): object 0xBA9384, vtable = 0xA9C64C
VT2 = 0x00A9C64C
# --- type-3 object (from FUN_00977ce0): object 0xBA938C, vtable = 0xA9C694
VT3 = 0x00A9C694
# --- type-4 object (from FUN_0040a290): object 0xBA101C, vtable = 0xA79A30
VT4 = 0x00A79A30

for name, vt in (("type1_vtable_region", VT1), ("type2_vtable_region", VT2),
                 ("type3_vtable_region", VT3), ("type4_vtable_region", VT4)):
    dump(vt - 16, 64, name + "_with_preceding_dwords")

print("=== vtable slot dwords (vtable+0x14) ===")
for name, vt in (("type1", VT1), ("type2", VT2), ("type3", VT3), ("type4", VT4)):
    slot_va = vt + 0x14
    target = u32(slot_va)
    pin = pe.pin(slot_va, 4)
    print("%s: vtable=0x%08X slot_va=0x%08X fo=0x%08X bytes=%s -> target VA 0x%08X" %
          (name, vt, slot_va, int(pin["file_offset"], 16), pin["original_bytes_hex"], target))
    # full vtable entries 0..0x18
    entries = []
    for off in range(0, 0x18 + 4, 4):
        entries.append("+0x%02X: 0x%08X" % (off, u32(vt + off)))
    print("   entries: %s" % " | ".join(entries))

print()
print("=== RTTI walk (vtable-4 -> COL -> TypeDescriptor -> name) ===")
for name, vt in (("type1", VT1), ("type2", VT2), ("type3", VT3), ("type4", VT4)):
    col_va = u32(vt - 4)
    print("%s: [vtable-4]@[0x%08X] = COL VA 0x%08X" % (name, vt - 4, col_va))
    col = pe.pin(col_va, 20)
    sig, off, cdoff, ptype, pclass = struct.unpack("<IIIII", bytes.fromhex(col["original_bytes_hex"]))
    print("   COL: sig=0x%X offset=0x%X cdOffset=0x%X pTypeDescriptor=0x%08X pClassDescriptor=0x%08X" %
          (sig, off, cdoff, ptype, pclass))
    td = pe.pin(ptype, 64)
    td_bytes = bytes.fromhex(td["original_bytes_hex"])
    name_z = td_bytes[8:].split(b"\x00")[0]
    print("   TypeDescriptor @0x%08X: vftable=0x%08X spare=0x%08X name=%r" %
          (ptype, struct.unpack_from("<I", td_bytes, 0)[0], struct.unpack_from("<I", td_bytes, 4)[0], name_z))
    print()

# --- helper functions context
dump(0x70C7B1, 0x60, "vector_append_helper_FUN_0070c7b1")
dump(0x7CD4D0, 0x40, "atexit_style_helper_A_0x7CD4DB_region")
dump(0x95D4D0, 0x40, "atexit_style_helper_B_0x95D4DB_region")
dump(0x70DDE0, 0x120, "payload_prep_tail_FUN_0070dcf0")
