# s3_apply_loop_deep.py
# RUN: PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004
# Purpose (bounded, READ-ONLY): (1) dump the FULL FUN_00726900 record-apply
# loop body incl. the tail beyond the S2 window; (2) dump the traits dispatch
# target FUN_0075F65C; (3) dump the int-traits vtable 0x00A9C670 (16 dwords);
# (4) canon re-verification windows: FUN_0070C180 (slot getter), FUN_0070D990
# (default creator), FUN_007374C0 (component ctor), FUN_0070E100 (cache
# lookup), FUN_00977A50 region (traits static init), FUN_0040DE60 (cursor
# advance); (5) machine-verify the apply-loop call targets + key byte pins;
# (6) name the two IAT slots used by the guard pair FUN_00413440/0x00413450
# via a minimal import-directory walk (bounded, read-only).
# Output: 01_RAW/S3_APPLY_LOOP_DEEP.json
import sys, os, json, struct
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

def load_pe(path):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    assert d[e_lfanew:e_lfanew+4] == b"PE\x00\x00"
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", d, coff + 2)[0]
    opt_size = struct.unpack_from("<H", d, coff + 16)[0]
    opt = coff + 20
    image_base = struct.unpack_from("<I", d, opt + 28)[0]
    # data directories: import = index 1
    num_dirs = struct.unpack_from("<I", d, opt + 92)[0]
    dirs = []
    for i in range(num_dirs):
        rva, size = struct.unpack_from("<II", d, opt + 96 + 8 * i)
        dirs.append((rva, size))
    sec0 = opt + opt_size
    secs = []
    for i in range(nsec):
        s = sec0 + 40 * i
        name = d[s:s+8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, s + 8)
        secs.append({"name": name, "vaddr": vaddr, "vsize": vsize,
                     "rawptr": rawptr, "rawsize": rawsize})
    return d, image_base, secs, dirs

def va_to_off(image_base, secs, va):
    rva = va - image_base
    for s in secs:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rawsize"]):
            if rva - s["vaddr"] < s["rawsize"]:
                return s["rawptr"] + (rva - s["vaddr"])
    return None

def read_window(d, image_base, secs, va, size):
    off = va_to_off(image_base, secs, va)
    if off is None:
        return None
    return d[off:off+size].hex(" ")

def verify_call(d, image_base, secs, va, expected_target):
    off = va_to_off(image_base, secs, va)
    raw = d[off:off+5]
    if raw[0] != 0xE8:
        return {"va": "0x%08X" % va, "opcode": raw.hex(" "),
                "is_E8": False, "computed_target": None,
                "expected": "0x%08X" % expected_target, "match": False}
    rel = struct.unpack_from("<i", raw, 1)[0]
    tgt = va + 5 + rel
    return {"va": "0x%08X" % va, "opcode": raw.hex(" "),
            "is_E8": True, "computed_target": "0x%08X" % tgt,
            "expected": "0x%08X" % expected_target, "match": tgt == expected_target}

def verify_bytes(d, image_base, secs, va, expected_hex):
    expected = bytes.fromhex(expected_hex.replace(" ", ""))
    off = va_to_off(image_base, secs, va)
    raw = d[off:off+len(expected)]
    got = raw.hex(" ")
    return {"va": "0x%08X" % va, "expected": expected_hex, "actual": got,
            "match": got == expected_hex}

def verify_jcc(d, image_base, secs, va, expected_target):
    off = va_to_off(image_base, secs, va)
    b0 = d[off]
    if b0 == 0x0F:
        raw = d[off:off+6]
        rel = struct.unpack_from("<i", raw, 2)[0]
        tgt = va + 6 + rel
    else:
        raw = d[off:off+2]
        rel = struct.unpack_from("<b", raw, 1)[0]
        tgt = va + 2 + rel
    return {"va": "0x%08X" % va, "opcode": raw.hex(" "),
            "computed_target": "0x%08X" % tgt,
            "expected": "0x%08X" % expected_target, "match": tgt == expected_target}

def read_cstr(d, off, maxlen=64):
    end = d.find(b"\x00", off, off + maxlen)
    if end == -1:
        return d[off:off+maxlen].decode("ascii", "replace")
    return d[off:end].decode("ascii", "replace")

def iat_slot_name(d, image_base, secs, dirs, iat_va):
    """Resolve the import name for the IAT slot at iat_va (VA)."""
    iat_rva = iat_va - image_base
    imp_rva, imp_size = dirs[1]
    if imp_rva == 0:
        return {"iat_va": "0x%08X" % iat_va, "name": None, "note": "no import dir"}
    off = va_to_off(image_base, secs, image_base + imp_rva)
    if off is None:
        return {"iat_va": "0x%08X" % iat_va, "name": None, "note": "import dir not mapped"}
    idx = 0
    while True:
        desc = d[off + 20 * idx: off + 20 * idx + 20]
        orig_first, ts, fc, name_rva, first = struct.unpack("<IIIII", desc)
        if orig_first == 0 and first == 0:
            break
        # walk thunks
        thunk_rva = orig_first if orig_first else first
        t = 0
        while True:
            toff = va_to_off(image_base, secs, image_base + thunk_rva + 8 * t)
            val = struct.unpack_from("<I", d, toff)[0]
            if val == 0:
                break
            if first + 8 * t == iat_rva:
                if val & 0x80000000:
                    return {"iat_va": "0x%08X" % iat_va, "ordinal": val & 0xFFFF}
                hn_off = va_to_off(image_base, secs, image_base + val)
                return {"iat_va": "0x%08X" % iat_va,
                        "dll": read_cstr(d, va_to_off(image_base, secs, image_base + name_rva)),
                        "hint": struct.unpack_from("<H", d, hn_off)[0],
                        "name": read_cstr(d, hn_off + 2)}
            t += 1
        idx += 1
    return {"iat_va": "0x%08X" % iat_va, "name": None, "note": "not found"}

def main():
    out = {"run": "PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004", "stage": "S3"}
    d, image_base, secs, dirs = load_pe(EXE)

    out["windows"] = {}
    # (1) FULL FUN_00726900 (covers through 0x00726AB0+)
    out["windows"]["FUN_00726900_full"] = {
        "va": "0x%08X" % 0x00726900, "size": 0x1C0,
        "hex": read_window(d, image_base, secs, 0x00726900, 0x1C0)}
    # (2) traits dispatch target
    out["windows"]["FUN_0075F65C"] = {
        "va": "0x%08X" % 0x0075F65C, "size": 0x60,
        "hex": read_window(d, image_base, secs, 0x0075F65C, 0x60)}
    # (3) int traits vtable (16 dwords)
    vt_off = va_to_off(image_base, secs, 0x00A9C670)
    vt_bytes = d[vt_off:vt_off+0x40]
    out["int_traits_vtable_0x00A9C670_dwords"] = [
        "0x%08X" % struct.unpack_from("<I", vt_bytes, 4*i)[0] for i in range(16)]
    out["int_traits_vtable_raw_hex"] = vt_bytes.hex(" ")
    # (4) canon re-verification windows
    out["windows"]["FUN_0070C180_canon"] = {
        "va": "0x%08X" % 0x0070C180, "size": 0x70,
        "hex": read_window(d, image_base, secs, 0x0070C180, 0x70)}
    out["windows"]["FUN_0070D990_canon"] = {
        "va": "0x%08X" % 0x0070D990, "size": 0x110,
        "hex": read_window(d, image_base, secs, 0x0070D990, 0x110)}
    out["windows"]["FUN_007374C0_canon"] = {
        "va": "0x%08X" % 0x007374C0, "size": 0x40,
        "hex": read_window(d, image_base, secs, 0x007374C0, 0x40)}
    out["windows"]["FUN_0070E100_canon"] = {
        "va": "0x%08X" % 0x0070E100, "size": 0x80,
        "hex": read_window(d, image_base, secs, 0x0070E100, 0x80)}
    out["windows"]["FUN_00977A50_region"] = {
        "va": "0x%08X" % 0x00977A50, "size": 0x40,
        "hex": read_window(d, image_base, secs, 0x00977A50, 0x40)}
    out["windows"]["FUN_0040DE60_canon"] = {
        "va": "0x%08X" % 0x0040DE60, "size": 0x40,
        "hex": read_window(d, image_base, secs, 0x0040DE60, 0x40)}
    # factory lazy singleton + schema-init region pins (canon)
    out["windows"]["FUN_007374F0_schema_pin_region"] = {
        "va": "0x%08X" % 0x00737580, "size": 0x40,
        "hex": read_window(d, image_base, secs, 0x00737580, 0x40)}

    # (5) machine-verify apply-loop pins
    out["verify_calls"] = {
        "FUN_00726900_to_FUN_00413440_guard": verify_call(d, image_base, secs, 0x00726912, 0x00413440),
        "FUN_00726900_to_FUN_0040DE60_read1": verify_call(d, image_base, secs, 0x00726937, 0x0040DE60),
        "FUN_00726900_to_FUN_0040DE60_read2": verify_call(d, image_base, secs, 0x00726972, 0x0040DE60),
        "FUN_00726900_to_FUN_0040DE60_read3": verify_call(d, image_base, secs, 0x007269A6, 0x0040DE60),
        "FUN_00726900_to_FUN_0040DE60_loopread": verify_call(d, image_base, secs, 0x007269EB, 0x0040DE60),
        "FUN_00726900_to_FUN_0070C180": verify_call(d, image_base, secs, 0x007269FF, 0x0070C180),
        "FUN_00726900_to_FUN_0075F65C": verify_call(d, image_base, secs, 0x00726A17, 0x0075F65C),
    }
    out["verify_byte_pins"] = {
        "loop_mov_ecx_factory_from_classobj4": verify_bytes(d, image_base, secs, 0x007269F8, "8b 4d 04"),
        "loop_movzx_edx_tag": verify_bytes(d, image_base, secs, 0x007269FB, "0f b7 d7"),
        "loop_cmp_slot_kind_zero": verify_bytes(d, image_base, secs, 0x00726A04, "83 78 04 00"),
        "loop_mov_ecx_slot_id": verify_bytes(d, image_base, secs, 0x00726A0A, "8b 48 08"),
        "loop_mov_edx_table_ptr_classobj40": verify_bytes(d, image_base, secs, 0x00726A0D, "8b 55 40"),
        "loop_lea_dest_table_plus_id4": verify_bytes(d, image_base, secs, 0x00726A10, "8d 0c 8a"),
        "loop_push_dest_push_cursor": verify_bytes(d, image_base, secs, 0x00726A13, "51 56"),
        "loop_mov_ecx_slot": verify_bytes(d, image_base, secs, 0x00726A15, "8b c8"),
        "read1_movzx_ax": verify_bytes(d, image_base, secs, 0x00726948, "0f b7 c7"),
        "read1_cmp_ffff": verify_bytes(d, image_base, secs, 0x0072694B, "3d ff ff 00 00"),
        "loop_counter_init": verify_bytes(d, image_base, secs, 0x007269BC, "c7 44 24 14 00 00 00 00"),
        "loop_i_increment_cmp": verify_bytes(d, image_base, secs, 0x00726A22, "8b 44 24 14 83 c0 01 3b 44 24 18"),
        "loop_jb_back": verify_jcc(d, image_base, secs, 0x00726A31, 0x007269CC),
        "postloop_and_flag": verify_bytes(d, image_base, secs, 0x00726A33, "22 5e 11"),
        # canon re-verification pins
        "FUN_0070D990_writer_idiom_0x0070DA36": verify_bytes(d, image_base, secs, 0x0070DA36, "8b 46 08"),
        "FUN_0070D990_writer_idiom_0x0070DA3E": verify_bytes(d, image_base, secs, 0x0070DA3E, "8d 04 98"),
        "FUN_0070D990_factory_into_classobj4_0x0070D9A5": verify_bytes(d, image_base, secs, 0x0070D9A5, "89 73 04") ,
        "FUN_00977A50_vtable_store_0x00977A68": verify_bytes(d, image_base, secs, 0x00977A68, "a3 7c 93 ba 00"),
        "FUN_007374C0_component_vtable_store": verify_bytes(d, image_base, secs, 0x007374C6, "c7 07 2c 6f a8 00"),
    }
    out["verify_branch_pins"] = {
        "read1_je_flag_off": verify_jcc(d, image_base, secs, 0x00726920, 0x0072693E),
        "read1_ja_bounds": verify_jcc(d, image_base, secs, 0x0072692B, 0x0072693E),
        "read1_jmp_after": verify_jcc(d, image_base, secs, 0x0072693C, 0x00726948),
        "read2_je_flag_off": verify_jcc(d, image_base, secs, 0x0072695B, 0x00726979),
        "read3_je_flag_off": verify_jcc(d, image_base, secs, 0x0072698F, 0x007269AD),
        "count_loop_entry_jmp": verify_jcc(d, image_base, secs, 0x007269C4, 0x00726A33),
        "loop_cond_je_exit": verify_jcc(d, image_base, secs, 0x007269D0, 0x00726A33),
        "loop_bl_je_exit": verify_jcc(d, image_base, secs, 0x007269D4, 0x00726A33),
        "loop_read_ja_skip": verify_jcc(d, image_base, secs, 0x007269DF, 0x007269F2),
        "slot_kind_je_skip": verify_jcc(d, image_base, secs, 0x00726A08, 0x00726A20),
        "postloop_je_tail": verify_jcc(d, image_base, secs, 0x00726A36, 0x00726AB0),
    }

    # (6) IAT slot names for the guard pair
    out["guard_iat_resolution"] = {
        "slot_0x00A75064": iat_slot_name(d, image_base, secs, dirs, 0x00A75064),
        "slot_0x00A7506C": iat_slot_name(d, image_base, secs, dirs, 0x00A7506C),
    }

    with open(os.path.join(RUN, "01_RAW", "S3_APPLY_LOOP_DEEP.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S3 done.")
    bad_calls = [k for k, v in out["verify_calls"].items() if not v["match"]]
    bad_pins = [k for k, v in out["verify_byte_pins"].items() if not v["match"]]
    bad_br = [k for k, v in out["verify_branch_pins"].items() if not v["match"]]
    print("call fails: %s" % bad_calls)
    print("byte pin fails: %s" % bad_pins)
    print("branch fails: %s" % bad_br)
    print("guard IAT:", out["guard_iat_resolution"])

if __name__ == "__main__":
    main()
