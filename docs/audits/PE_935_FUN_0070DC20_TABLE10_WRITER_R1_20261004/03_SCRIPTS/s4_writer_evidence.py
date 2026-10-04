# s4_writer_evidence.py
# RUN: PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004
# Purpose (bounded, READ-ONLY): complete the writer-chain evidence with the
# machine-anchored (S3-probe-corrected) pins:
#  (1) FUN_009777F0 window (canon int-traits reader/writer; reverify READ
#      @0x00977807 + STORE @0x00977810 pins);
#  (2) FUN_0070CBC0 (SLOT_ADD canon) window - narrow reverification of the
#      id=tag+4 computation + slot field stores;
#  (3) FUN_0075F6D0 (canon traits default dispatcher) window;
#  (4) FUN_0092B660 (cache map insert canon) window + FUN_0070E100 mapfind
#      call target verification;
#  (5) getter-side reader idiom window (0x004C5520..0x004C5560) + pins;
#  (6) FULL corrected machine battery for FUN_00726900 (probe-anchored VAs)
#      and FUN_0075F660 internals;
#  (7) corrected canon reverification pins (FUN_0070D990 writer idiom bytes,
#      FUN_007374C0 vtable store @0x007374DC, FUN_00977A68 vtable store,
#      FUN_0070C180 array pins, FUN_0040DE60 pins);
#  (8) IAT direct read for the guard pair (read the dword at 0x00A75064 /
#      0x00A7506C and resolve the hint/name entry).
# Output: 01_RAW/S4_WRITER_EVIDENCE.json
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
    sec0 = opt + opt_size
    secs = []
    for i in range(nsec):
        s = sec0 + 40 * i
        name = d[s:s+8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", d, s + 8)
        secs.append({"name": name, "vaddr": vaddr, "vsize": vsize,
                     "rawptr": rawptr, "rawsize": rawsize})
    return d, image_base, secs

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
    elif b0 == 0xEB:
        raw = d[off:off+2]
        rel = struct.unpack_from("<b", raw, 1)[0]
        tgt = va + 2 + rel
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

def iat_direct(d, image_base, secs, iat_va):
    """Read the IAT slot dword and resolve it as hint/name RVA (or bound VA)."""
    off = va_to_off(image_base, secs, iat_va)
    val = struct.unpack_from("<I", d, off)[0]
    res = {"iat_va": "0x%08X" % iat_va, "raw_dword": "0x%08X" % val}
    # At image mapping an unbound IAT slot holds the RVA of the hint/name entry.
    hn_off = va_to_off(image_base, secs, image_base + val) if val < image_base else None
    if hn_off is None and val >= image_base:
        hn_off = va_to_off(image_base, secs, val)
    if hn_off is not None:
        res["hint"] = struct.unpack_from("<H", d, hn_off)[0]
        res["resolved_name"] = read_cstr(d, hn_off + 2)
    return res

def main():
    out = {"run": "PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004", "stage": "S4"}
    d, image_base, secs = load_pe(EXE)

    out["windows"] = {}
    out["windows"]["FUN_009777F0"] = {
        "va": "0x%08X" % 0x009777F0, "size": 0x60,
        "hex": read_window(d, image_base, secs, 0x009777F0, 0x60)}
    out["windows"]["FUN_0070CBC0_slotadd"] = {
        "va": "0x%08X" % 0x0070CBC0, "size": 0x120,
        "hex": read_window(d, image_base, secs, 0x0070CBC0, 0x120)}
    out["windows"]["FUN_0075F6D0_canon"] = {
        "va": "0x%08X" % 0x0075F6D0, "size": 0x50,
        "hex": read_window(d, image_base, secs, 0x0075F6D0, 0x50)}
    out["windows"]["FUN_0092B660_canon"] = {
        "va": "0x%08X" % 0x0092B660, "size": 0x60,
        "hex": read_window(d, image_base, secs, 0x0092B660, 0x60)}
    out["windows"]["getter_reader_idiom_0x004C5520"] = {
        "va": "0x%08X" % 0x004C5520, "size": 0x48,
        "hex": read_window(d, image_base, secs, 0x004C5520, 0x48)}

    # (6) FULL corrected battery for FUN_00726900 (probe-anchored)
    out["verify_calls"] = {
        # FUN_00726900 (apply loop) - corrected anchors
        "loop_guard_enter_0x00726912": verify_call(d, image_base, secs, 0x00726912, 0x00413440),
        "loop_read1_advance_0x00726937": verify_call(d, image_base, secs, 0x00726937, 0x0040DE60),
        "loop_read2_advance_0x00726972": verify_call(d, image_base, secs, 0x00726972, 0x0040DE60),
        "loop_read3_advance_0x007269A6": verify_call(d, image_base, secs, 0x007269A6, 0x0040DE60),
        "loop_tagread_advance_0x007269EF": verify_call(d, image_base, secs, 0x007269EF, 0x0040DE60),
        "loop_slotget_0x00726A03": verify_call(d, image_base, secs, 0x00726A03, 0x0070C180),
        "loop_traits_dispatch_0x00726A1B": verify_call(d, image_base, secs, 0x00726A1B, 0x0075F660),
        "loop_tail_advance4_0x00726A76": verify_call(d, image_base, secs, 0x00726A76, 0x0040DE60),
        "loop_guard_leave_0x00726AB7": verify_call(d, image_base, secs, 0x00726AB7, 0x00413450),
        # FUN_0075F660 (traits dispatcher)
        "disp_nullfallback_a_0x0075F696": verify_call(d, image_base, secs, 0x0075F696, 0x0040BF80),
        "disp_nullfallback_b_0x0075F6AA": verify_call(d, image_base, secs, 0x0075F6AA, 0x0040C7C0),
        # FUN_0070E100 (getter-side cache lookup) guard pair + mapfind
        "lookup_guard_enter_0x0070E110": verify_call(d, image_base, secs, 0x0070E110, 0x00413440),
        "lookup_mapfind_0x0070E124": verify_call(d, image_base, secs, 0x0070E124, 0x004D1430),
        "lookup_guard_leave_0x0070E136": verify_call(d, image_base, secs, 0x0070E136, 0x00413450),
        # FUN_0070D990 (canon creator) internal calls
        "d990_valuevector_ctor_0x0070D9C9": verify_call(d, image_base, secs, 0x0070D9C9, 0x00412C50),
        "d990_default_dispatch_0x0070DA42": verify_call(d, image_base, secs, 0x0070DA42, 0x0075F6D0),
    }

    out["verify_byte_pins"] = {
        # apply loop - corrected anchors (probe-derived)
        "loop_ecx_factory_classobj4_0x007269FC": verify_bytes(d, image_base, secs, 0x007269FC, "8b 4d 04"),
        "loop_movzx_tag_0x007269FF": verify_bytes(d, image_base, secs, 0x007269FF, "0f b7 d7"),
        "loop_push_tag_0x00726A02": verify_bytes(d, image_base, secs, 0x00726A02, "52"),
        "loop_cmp_slot_kind_0x00726A08": verify_bytes(d, image_base, secs, 0x00726A08, "83 78 04 00"),
        "loop_load_slot_id_0x00726A0E": verify_bytes(d, image_base, secs, 0x00726A0E, "8b 48 08"),
        "loop_load_tableptr_0x00726A11": verify_bytes(d, image_base, secs, 0x00726A11, "8b 55 40"),
        "loop_lea_dest_0x00726A14": verify_bytes(d, image_base, secs, 0x00726A14, "8d 0c 8a"),
        "loop_push_dest_0x00726A17": verify_bytes(d, image_base, secs, 0x00726A17, "51"),
        "loop_push_cursor_0x00726A18": verify_bytes(d, image_base, secs, 0x00726A18, "56"),
        "loop_mov_ecx_slot_0x00726A19": verify_bytes(d, image_base, secs, 0x00726A19, "8b c8"),
        "loop_result_bl_0x00726A20": verify_bytes(d, image_base, secs, 0x00726A20, "8a d8"),
        "loop_kind0_bl0_0x00726A24": verify_bytes(d, image_base, secs, 0x00726A24, "32 db"),
        "loop_i_inc_0x00726A26": verify_bytes(d, image_base, secs, 0x00726A26, "8b 44 24 14 83 c0 01 3b 44 24 18 89 44 24 14"),
        "loop_post_and_0x00726A37": verify_bytes(d, image_base, secs, 0x00726A37, "22 5e 11"),
        "tail_value1_or_classobj30_0x00726A50": verify_bytes(d, image_base, secs, 0x00726A50, "09 45 30"),
        "tail_value2_or_classobj30_0x00726A4B": verify_bytes(d, image_base, secs, 0x00726A4B, "09 55 30"),
        "tail_mode_cmp_word_0x00726A53": verify_bytes(d, image_base, secs, 0x00726A53, "66 83 7c 24 24 01"),
        "tail_read_u32_0x00726A6F": verify_bytes(d, image_base, secs, 0x00726A6F, "8b 3c 08"),
        "tail_vtable_slot3_0x00726A98": verify_bytes(d, image_base, secs, 0x00726A98, "8b 52 0c"),
        "tail_virtual_call_0x00726A9D": verify_bytes(d, image_base, secs, 0x00726A9D, "ff d2"),
        # FUN_0075F660 dispatcher internals
        "disp_mov_eax_ecx_0x0075F660": verify_bytes(d, image_base, secs, 0x0075F660, "8b c1"),
        "disp_load_traits_0x0075F662": verify_bytes(d, image_base, secs, 0x0075F662, "8b 08"),
        "disp_test_traits_0x0075F664": verify_bytes(d, image_base, secs, 0x0075F664, "85 c9"),
        "disp_mov_esi_cursor_0x0075F668": verify_bytes(d, image_base, secs, 0x0075F668, "8b 74 24 0c"),
        "disp_load_vtable_0x0075F674": verify_bytes(d, image_base, secs, 0x0075F674, "8b 01"),
        "disp_vtable_slot5_0x0075F676": verify_bytes(d, image_base, secs, 0x0075F676, "8b 40 14"),
        "disp_push_dest_0x0075F679": verify_bytes(d, image_base, secs, 0x0075F679, "52"),
        "disp_push_cursor_0x0075F67A": verify_bytes(d, image_base, secs, 0x0075F67A, "56"),
        "disp_virtual_call_0x0075F67B": verify_bytes(d, image_base, secs, 0x0075F67B, "ff d0"),
        "disp_ret8_0x0075F684": verify_bytes(d, image_base, secs, 0x0075F684, "c2 08 00"),
        # FUN_009777F0 canon reverify (the exact writer)
        "writer_read_0x00977807": verify_bytes(d, image_base, secs, 0x00977807, "8b 04 10"),
        "writer_store_0x00977810": verify_bytes(d, image_base, secs, 0x00977810, "89 02"),
        # getter-side reader idiom (canon reverify)
        "getter_reader_idiom_0x004C5539": verify_bytes(d, image_base, secs, 0x004C5539, "8b 44 19 08"),
        "getter_lea_0x004C5541": verify_bytes(d, image_base, secs, 0x004C5541, "8d 04 82"),
        "getter_load_0x004C554E": verify_bytes(d, image_base, secs, 0x004C554E, "8b 00"),
        # corrected canon reverification pins
        "d990_writer_idiom_id_0x0070DA36": verify_bytes(d, image_base, secs, 0x0070DA36, "8b 44 19 08"),
        "d990_writer_idiom_lea_0x0070DA3E": verify_bytes(d, image_base, secs, 0x0070DA3E, "8d 04 82"),
        "d990_writer_idiom_push_0x0070DA41": verify_bytes(d, image_base, secs, 0x0070DA41, "50"),
        "d990_factory_into_classobj4_0x0070D9A5": verify_bytes(d, image_base, secs, 0x0070D9A5, "89 73 04"),
        "d990_valuevector_args_0x0070D9BE": verify_bytes(d, image_base, secs, 0x0070D9BE, "50 8d 7b 40 51 8b cf"),
        "d990_table12_count_0x0070D9BB": verify_bytes(d, image_base, secs, 0x0070D9BB, "83 c1 04"),
        "ctor_vtable_store_0x007374DC": verify_bytes(d, image_base, secs, 0x007374DC, "c7 06 2c 6f a8 00"),
        "traits_vtable_store_0x00977A68": verify_bytes(d, image_base, secs, 0x00977A68, "c7 05 7c 93 ba 00 70 c6 a9 00"),
        # FUN_0070C180 (slot getter) pins
        "slotget_inrange_array_0x0070C1C0": verify_bytes(d, image_base, secs, 0x0070C1C0, "8b 91 8c 00 00 00 2b 91 88 00 00 00 c1 fa 04"),
        "slotget_lea_slot_0x0070C1D3": verify_bytes(d, image_base, secs, 0x0070C1D3, "c1 e0 04 03 81 88 00 00 00"),
        "slotget_default_0x0070C1E0": verify_bytes(d, image_base, secs, 0x0070C1E0, "b8 08 51 ba 00"),
        # FUN_0040DE60 cursor advance pins
        "cursor_add_pos_0x0040DE63": verify_bytes(d, image_base, secs, 0x0040DE63, "01 41 0c"),
        "cursor_bounds_flag_0x0040DE69": verify_bytes(d, image_base, secs, 0x0040DE69, "c6 41 11 00"),
        # FUN_0070E100 lookup pins
        "lookup_lea_map_0x0070E121": verify_bytes(d, image_base, secs, 0x0070E121, "8d 7e 0c"),
        "lookup_node_value_0x0070E131": verify_bytes(d, image_base, secs, 0x0070E131, "8b 68 14"),
        # schema SLOT_ADD call-site pins (canon FUN_007374F0)
        "schema_slot6_args_0x0073758D": verify_bytes(d, image_base, secs, 0x0073758D, "50 6a 00 6a 00 6a 01 6a 06 8b ce"),
        "schema_slot6_call_0x0073759A": verify_call(d, image_base, secs, 0x0073759A, 0x0070CBC0),
        # int traits vtable slot 5 = FUN_009777F0 (the writer) + slot 1 default
        "int_traits_vtable_slot5": verify_bytes(d, image_base, secs, 0x00A9C684, "f0 77 97 00"),
        "int_traits_vtable_slot1": verify_bytes(d, image_base, secs, 0x00A9C674, "e0 77 97 00"),
    }

    out["verify_branch_pins"] = {
        # corrected loop branch anchors
        "loop_entry_jbe_0x007269C8": verify_jcc(d, image_base, secs, 0x007269C8, 0x00726A37),
        "loop_cond_je_0x007269D4": verify_jcc(d, image_base, secs, 0x007269D4, 0x00726A37),
        "loop_bl_je_0x007269D8": verify_jcc(d, image_base, secs, 0x007269D8, 0x00726A37),
        "loop_read_ja_0x007269E3": verify_jcc(d, image_base, secs, 0x007269E3, 0x007269F6),
        "loop_back_jb_0x00726A35": verify_jcc(d, image_base, secs, 0x00726A35, 0x007269D0),
        "loop_post_je_0x00726A3A": verify_jcc(d, image_base, secs, 0x00726A3A, 0x00726AB4),
        "tail_mode_jne_0x00726A59": verify_jcc(d, image_base, secs, 0x00726A59, 0x00726AB4),
        "value1_ffff_jne_0x00726A45": verify_jcc(d, image_base, secs, 0x00726A45, 0x00726A50),
        "tail_zero_je_0x00726A8C": verify_jcc(d, image_base, secs, 0x00726A8C, 0x00726AB0),
        # dispatcher branches
        "disp_traits_je_0x0075F66E": verify_jcc(d, image_base, secs, 0x0075F66E, 0x0075F687),
        "disp_flags_je_0x0075F694": verify_jcc(d, image_base, secs, 0x0075F694, 0x0075F6AA),
    }

    # (8) IAT direct read for guard pair
    out["guard_iat_direct"] = {
        "slot_0x00A75064": iat_direct(d, image_base, secs, 0x00A75064),
        "slot_0x00A7506C": iat_direct(d, image_base, secs, 0x00A7506C),
    }

    with open(os.path.join(RUN, "01_RAW", "S4_WRITER_EVIDENCE.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S4 done.")
    bad_calls = [k for k, v in out["verify_calls"].items() if not v["match"]]
    bad_pins = [k for k, v in out["verify_byte_pins"].items() if not v["match"]]
    bad_br = [k for k, v in out["verify_branch_pins"].items() if not v["match"]]
    print("call fails: %s" % bad_calls)
    print("byte pin fails: %s" % bad_pins)
    print("branch fails: %s" % bad_br)
    print("guard IAT direct:", out["guard_iat_direct"])

if __name__ == "__main__":
    main()
