# s2_decode_support.py
# RUN: PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004
# Purpose (bounded, READ-ONLY): (1) dump windows of the two candidate
# write-path subordinates FUN_0075D8D0 and FUN_00726900 called inside
# FUN_0070DC20; (2) dump bounded context around the SECOND E8 caller of
# FUN_0070DC20 @0x00704704; (3) surface windows of the guard pair
# FUN_0040D440/FUN_0040D450; (4) MACHINE-VERIFY every call/branch pin of the
# FUN_0070DCF0 + FUN_0070DC20 manual decodes (opcode bytes at exact VA +
# rel32 target recomputation); (5) xref censuses (E8 callers) for the
# subordinate functions. Own PE mapper, byte reads only.
# Output: 01_RAW/S2_DECODE_SUPPORT.json
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

def scan_callers(d, image_base, secs, target):
    res = []
    for s in secs:
        if s["name"] != ".text":
            continue
        blob = d[s["rawptr"]:s["rawptr"]+s["rawsize"]]
        vaddr0 = s["vaddr"]
        n = len(blob)
        i = 0
        while i < n - 5:
            if blob[i] == 0xE8:
                rel = struct.unpack_from("<i", blob, i + 1)[0]
                tgt_va = image_base + vaddr0 + i + 5 + rel
                if tgt_va == target:
                    res.append("0x%08X" % (image_base + vaddr0 + i))
            i += 1
    return res

def verify_call(d, image_base, secs, va, expected_target):
    off = va_to_off(image_base, secs, va)
    raw = d[off:off+5]
    if raw[0] != 0xE8:
        return {"va": "0x%08X" % va, "opcode": raw[0:5].hex(" "),
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
    """short jcc (74/75/EB...) or 0F 8x long jcc; verifies opcode bytes at VA
    and recomputes the branch target."""
    off = va_to_off(image_base, secs, va)
    b0 = d[off]
    if b0 == 0x0F:
        raw = d[off:off+6]
        rel = struct.unpack_from("<i", raw, 2)[0]
        tgt = va + 6 + rel
        return {"va": "0x%08X" % va, "opcode": raw.hex(" "),
                "computed_target": "0x%08X" % tgt,
                "expected": "0x%08X" % expected_target, "match": tgt == expected_target}
    raw = d[off:off+2]
    rel = struct.unpack_from("<b", raw, 1)[0]
    tgt = va + 2 + rel
    return {"va": "0x%08X" % va, "opcode": raw.hex(" "),
            "computed_target": "0x%08X" % tgt,
            "expected": "0x%08X" % expected_target, "match": tgt == expected_target}

def main():
    out = {"run": "PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004", "stage": "S2"}
    d, image_base, secs = load_pe(EXE)

    # (1) subordinate function windows
    out["windows"] = {}
    out["windows"]["FUN_0075D8D0"] = {
        "va": "0x%08X" % 0x0075D8D0, "size": 0x100,
        "hex": read_window(d, image_base, secs, 0x0075D8D0, 0x100)}
    out["windows"]["FUN_00726900"] = {
        "va": "0x%08X" % 0x00726900, "size": 0x140,
        "hex": read_window(d, image_base, secs, 0x00726900, 0x140)}
    # (2) second caller context @0x00704704
    out["windows"]["caller2_context_0x00704704"] = {
        "va": "0x%08X" % 0x007046C0, "size": 0x84,
        "hex": read_window(d, image_base, secs, 0x007046C0, 0x84)}
    # (3) guard pair surface windows (machine-corrected targets: 0x00413440 /
    # 0x00413450; the executor's first hand rel32 computation 0x0040D440/
    # 0x0040D450 was WRONG and was corrected by this battery)
    out["windows"]["FUN_00413440_surface"] = {
        "va": "0x%08X" % 0x00413440, "size": 0x40,
        "hex": read_window(d, image_base, secs, 0x00413440, 0x40)}
    out["windows"]["FUN_00413450_surface"] = {
        "va": "0x%08X" % 0x00413450, "size": 0x40,
        "hex": read_window(d, image_base, secs, 0x00413450, 0x40)}

    # (4) machine verification of the manual FUN_0070DCF0 decode pins
    out["verify_calls"] = {}
    cf = [
        ("FUN_0070DCF0_to_FUN_0040E160", 0x0070DD39, 0x0040E160),
        ("FUN_0070DCF0_to_alloc_0x0095D3BE", 0x0070DD4B, 0x0095D3BE),
        ("FUN_0070DCF0_to_FUN_00971AD0", 0x0070DD75, 0x00971AD0),
        ("FUN_0070DCF0_to_FUN_00971650", 0x0070DD84, 0x00971650),
        ("FUN_0070DCF0_to_FUN_0040DE60", 0x0070DDA8, 0x0040DE60),
        ("FUN_0070DCF0_to_FUN_0070DC20", 0x0070DDBD, 0x0070DC20),
        ("FUN_0070DCF0_to_delete_0x0095DB40", 0x0070DDE3, 0x0095DB40),
    ]
    for name, va, tgt in cf:
        out["verify_calls"][name] = verify_call(d, image_base, secs, va, tgt)

    dc = [
        ("FUN_0070DC20_to_FUN_0070D990", 0x0070DC3F, 0x0070D990),
        ("FUN_0070DC20_to_FUN_0075D8D0", 0x0070DC4B, 0x0075D8D0),
        ("FUN_0070DC20_to_FUN_00726900", 0x0070DC53, 0x00726900),
        ("FUN_0070DC20_to_FUN_00413440", 0x0070DC62, 0x00413440),
        ("FUN_0070DC20_to_FUN_0092B660", 0x0070DC7C, 0x0092B660),
        ("FUN_0070DC20_to_FUN_00413450", 0x0070DC87, 0x00413450),
    ]
    for name, va, tgt in dc:
        out["verify_calls"][name] = verify_call(d, image_base, secs, va, tgt)

    # byte pins of the decode (opcodes at exact VAs)
    out["verify_byte_pins"] = {}
    pins = [
        ("FUN_0070DCF0_prologue_mov_esi_ecx", 0x0070DD16, "8b f1"),
        ("FUN_0070DCF0_cmp_factory84", 0x0070DD1A, "39 9e 84 00 00 00"),
        ("FUN_0070DCF0_mov_edi_receiver_esp38", 0x0070DD5C, "8b 7c 24 38"),
        ("FUN_0070DCF0_push2_cursor_receiver_ecx", 0x0070DDB3, "6a 02 8d 44 24 18 50 57 8b ce"),
        ("FUN_0070DCF0_ret4", 0x0070DDFF, "c2 04 00"),
        ("FUN_0070DC20_prologue", 0x0070DC20, "83 ec 10 53"),
        ("FUN_0070DC20_mov_ebx_arg1", 0x0070DC24, "8b 5c 24 18"),
        ("FUN_0070DC20_mov_esi_ecx_this", 0x0070DC2D, "8b f1"),
        ("FUN_0070DC20_pushes_then_mov_ecx_esi", 0x0070DC3B, "50 53 8b ce"),
        ("FUN_0070DC20_mov_edi_classobj", 0x0070DC44, "8b f8"),
        ("FUN_0070DC20_mov_eax_esp24_cursor_arg", 0x0070DC46, "8b 44 24 24"),
        ("FUN_0070DC20_mov_ecx_edi_push_eax", 0x0070DC50, "8b cf 50"),
        ("FUN_0070DC20_lea_ebp_esi24", 0x0070DC5D, "8d 6e 24"),
        ("FUN_0070DC20_lea_ecx_esi0C_factory_cache", 0x0070DC71, "8d 4e 0c"),
        ("FUN_0070DC20_mov_receiver_into_keyslot", 0x0070DC74, "89 5c 24 18"),
        ("FUN_0070DC20_mov_classobj_into_valueslot", 0x0070DC78, "89 7c 24 1c"),
        ("FUN_0070DC20_mov_edx_esp28_arg3", 0x0070DCA0, "8b 54 24 28"),
        ("FUN_0070DC20_vtable_slot9", 0x0070DCA6, "8b 40 24"),
        ("FUN_0070DC20_vtable_slot10", 0x0070DCC8, "8b 42 28"),
        ("FUN_0070DC20_classobj_vt0_push1", 0x0070DCD0, "8b 17 8b 02 6a 01 8b cf ff d0"),
        ("FUN_0070DC20_ret_0xC_fail", 0x0070DCE2, "c2 0c 00"),
        ("FUN_0070DC20_ret_0xC_success", 0x0070DCED, "c2 0c 00"),
    ]
    for name, va, hx in pins:
        out["verify_byte_pins"][name] = verify_bytes(d, image_base, secs, va, hx)

    # branch target pins
    out["verify_branch_pins"] = {}
    brs = [
        ("FUN_0070DC20_je_receiver_null_to_pop_esi", 0x0070DC34, 0x0070DCE8),
        ("FUN_0070DC20_je_applyfail_to_cleanup", 0x0070DC5A, 0x0070DCB3),
        ("FUN_0070DC20_je_insertfail_to_cleanup", 0x0070DC8F, 0x0070DCB3),
        ("FUN_0070DC20_je_nodelegate_skip", 0x0070DC98, 0x0070DCAF),
        ("FUN_0070DC20_jne_success", 0x0070DCB1, 0x0070DCE5),
        ("FUN_0070DC20_je_classobj_null_success_null", 0x0070DCB5, 0x0070DCE5),
        ("FUN_0070DC20_je_nodelegate_skip2", 0x0070DCBE, 0x0070DCD0),
        ("FUN_0070DCF0_je_no_stream_return0", 0x0070DD20, 0x0070DDEB),
        ("FUN_0070DCF0_je_readfail", 0x0070DD7C, 0x0070DDC4),
        ("FUN_0070DCF0_jne_sizemismatch", 0x0070DD8D, 0x0070DDC4),
        ("FUN_0070DCF0_ja_cursorbounds", 0x0070DDA0, 0x0070DE02),
    ]
    for name, va, tgt in brs:
        out["verify_branch_pins"][name] = verify_jcc(d, image_base, secs, va, tgt)

    # (5) xref censuses
    out["xref_census"] = {
        "FUN_0075D8D0_E8_callers": scan_callers(d, image_base, secs, 0x0075D8D0),
        "FUN_00726900_E8_callers": scan_callers(d, image_base, secs, 0x00726900),
        "FUN_0070D990_E8_callers": scan_callers(d, image_base, secs, 0x0070D990),
        "FUN_0092B660_E8_callers": scan_callers(d, image_base, secs, 0x0092B660),
    }

    with open(os.path.join(RUN, "01_RAW", "S2_DECODE_SUPPORT.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S2 done.")
    bad_calls = [k for k, v in out["verify_calls"].items() if not v["match"]]
    bad_pins = [k for k, v in out["verify_byte_pins"].items() if not v["match"]]
    bad_br = [k for k, v in out["verify_branch_pins"].items() if not v["match"]]
    print("call verify fails: %s" % bad_calls)
    print("byte pin fails: %s" % bad_pins)
    print("branch pin fails: %s" % bad_br)
    print("xrefs:", {k: len(v) for k, v in out["xref_census"].items()})

if __name__ == "__main__":
    main()
