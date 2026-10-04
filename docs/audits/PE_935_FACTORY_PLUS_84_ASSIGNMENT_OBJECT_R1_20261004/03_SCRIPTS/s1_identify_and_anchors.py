# s1_identify_and_anchors.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
# Purpose: input identity verification + the canonical anchor/pin battery:
# consumer-side re-pins (FUN_0070DCF0 +0x84 reads), the factory ctor/init chain pins,
# the singleton-reference censuses, the setter-chain call-target machine verification,
# the registration chain, the driver, the stream ctor, and the bounded string reads.
# READ-ONLY vs the pinned EXE. Own PE mapper (section-table driven). No Ghidra.
# Output: 01_RAW/S1_ANCHORS.json
import sys, os, json, struct, hashlib

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004"
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

def read_window(d, ib, secs, va, size):
    off = va_to_off(ib, secs, va)
    if off is None:
        return None
    return d[off:off+size].hex(" ")

def read_u8(d, ib, secs, va):
    off = va_to_off(ib, secs, va)
    return None if off is None else d[off]

def read_u32(d, ib, secs, va):
    off = va_to_off(ib, secs, va)
    return None if off is None else struct.unpack_from("<I", d, off)[0]

def read_i32_at(d, ib, secs, va):
    """read the signed rel32 located at va (the 4 operand bytes of an E8/E9 at va-1)."""
    off = va_to_off(ib, secs, va)
    return None if off is None else struct.unpack_from("<i", d, off)[0]

def call_target(d, ib, secs, call_va):
    """given a CALL/JMP instruction VA (opcode E8/E9 at call_va), machine-compute the target."""
    rel = read_i32_at(d, ib, secs, call_va + 1)
    if rel is None:
        return None
    return call_va + 5 + rel

def find_all(blob, pat, start=0):
    res = []
    while True:
        i = blob.find(pat, start)
        if i == -1:
            return res
        res.append(i)
        start = i + 1

def text_blob(d, secs):
    for s in secs:
        if s["name"] == ".text":
            return s["rawptr"], s["rawsize"], s["vaddr"]
    raise SystemExit("no .text")

def main():
    out = {"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004", "stage": "S1"}
    # ---- input identity ----
    raw = open(EXE, "rb").read()
    out["exe"] = {
        "path": EXE,
        "size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "pinned_sha256": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
        "pinned_size": 8015872,
        "identity_pass": (hashlib.sha256(raw).hexdigest()
                           == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
                           and len(raw) == 8015872),
    }
    d, ib, secs = load_pe(EXE)
    out["pe"] = {"image_base": "0x%08X" % ib,
                 "sections": [{"name": s["name"], "vaddr": "0x%08X" % s["vaddr"],
                               "vsize": s["vsize"], "rawsize": s["rawsize"]} for s in secs]}
    tp, ts, tv = text_blob(d, secs)
    TEXT = d[tp:tp+ts]
    TVA = ib + tv
    out["text"] = {"vaddr_start": "0x%08X" % TVA, "raw_size": ts}

    pins = {}

    # ---- A. consumer-side re-pins (FUN_0070DCF0) ----
    pins["consumer"] = {
        "FUN_0070DCF0_entry_bytes": {"va": 0x0070DCF0, "expect": "6A FF 68 28 C7 A0 00",
                                     "hex": read_window(d, ib, secs, 0x0070DCF0, 7)},
        "MOV_ESI_ECX_this": {"va": 0x0070DD16, "expect": "8B F1",
                             "hex": read_window(d, ib, secs, 0x0070DD16, 2)},
        "XOR_EBX_EBX": {"va": 0x0070DD18, "expect": "33 DB",
                        "hex": read_window(d, ib, secs, 0x0070DD18, 2)},
        "CMP_factory_plus_84": {"va": 0x0070DD1A, "expect": "39 9E 84 00 00 00",
                                "hex": read_window(d, ib, secs, 0x0070DD1A, 6)},
        "JE_fail_on_null": {"va": 0x0070DD20, "expect": "0F 84 C5 00 00 00",
                            "hex": read_window(d, ib, secs, 0x0070DD20, 6)},
        "MOV_ECX_stream_for_record_read": {"va": 0x0070DD6A, "expect": "8B 8E 84 00 00 00",
                                           "hex": read_window(d, ib, secs, 0x0070DD6A, 6)},
        "CALL_FUN_00971AD0": {"va": 0x0070DD75, "expect_target": "0x00971AD0",
                              "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0070DD75)},
        "MOV_ECX_stream_for_advance": {"va": 0x0070DD7E, "expect": "8B 8E 84 00 00 00",
                                       "hex": read_window(d, ib, secs, 0x0070DD7E, 6)},
        "CALL_FUN_00971650": {"va": 0x0070DD84, "expect_target": "0x00971650",
                              "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0070DD84)},
        "CALL_FUN_0070DC20_apply": {"va": 0x0070DDBD, "expect_target": "0x0070DC20",
                                    "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0070DDBD)},
    }
    # ---- B. the factory ctor/init chain pins ----
    pins["factory_init"] = {
        "base_ctor_entry": {"va": 0x0070CF80, "expect": "6A FF 68 6F C5 A0 00",
                            "hex": read_window(d, ib, secs, 0x0070CF80, 7)},
        "base_ctor_this_ESI": {"va": 0x0070CFA5, "expect": "8B F1",
                               "hex": read_window(d, ib, secs, 0x0070CFA5, 2)},
        "base_ctor_EBX_zero": {"va": 0x0070CFBC, "expect": "33 DB",
                               "hex": read_window(d, ib, secs, 0x0070CFBC, 2)},
        "NULL_INIT_store_plus_84": {"va": 0x0070D013, "expect": "89 9E 84 00 00 00",
                                    "hex": read_window(d, ib, secs, 0x0070D013, 6)},
        "derived_ctor_entry_20006": {"va": 0x0073B820, "expect": "6A FF 68 6A 3E A1 00",
                                     "hex": read_window(d, ib, secs, 0x0073B820, 7)},
        "derived_ctor_PUSH_classid": {"va": 0x0073B871, "expect": "68 26 4E 00 00",
                                      "hex": read_window(d, ib, secs, 0x0073B871, 5),
                                      "imm32_value": "0x%08X" % read_u32(d, ib, secs, 0x0073B872)},
        "derived_ctor_MOV_ECX_this": {"va": 0x0073B876, "expect": "8B CE",
                                       "hex": read_window(d, ib, secs, 0x0073B876, 2)},
        "derived_ctor_CALL_base_ctor": {"va": 0x0073B87D,
                                        "expect_target": "0x0070CF80",
                                        "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0073B87D)},
        "derived_ctor_vtable_store": {"va": 0x0073B89B, "expect": "C7 06 C4 70 A8 00",
                                      "hex": read_window(d, ib, secs, 0x0073B89B, 6),
                                      "imm32_value": "0x%08X" % read_u32(d, ib, secs, 0x0073B89D)},
        "lazyinit_guard_CMP_singleton": {"va": 0x0073E2B1, "expect": "83 3D 0C 59 BA 00 00",
                                         "hex": read_window(d, ib, secs, 0x0073E2B1, 7)},
        "lazyinit_PUSH_0x118": {"va": 0x0073E2CC, "expect": "68 18 01 00 00",
                                "hex": read_window(d, ib, secs, 0x0073E2CC, 5)},
        "lazyinit_CALL_ctor": {"va": 0x0073E2EB, "expect_target": "0x0073B820",
                               "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0073E2EB)},
        "lazyinit_store_singleton": {"va": 0x0073E302, "expect": "A3 0C 59 BA 00",
                                     "hex": read_window(d, ib, secs, 0x0073E302, 5),
                                     "imm32_value": "0x%08X" % read_u32(d, ib, secs, 0x0073E303)},
        "lazyinit_CALL_vecinit": {"va": 0x0073E307, "expect_target": "0x0070E2F0",
                                  "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0073E307)},
        "lazyinit_CALL_schema": {"va": 0x0073E312, "expect_target": "0x007374F0",
                                 "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0073E312)},
        "lazyinit_CALL_finalize": {"va": 0x0073E320, "expect_target": "0x0070C150",
                                   "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0073E320)},
        "lazyinit_CALL_readyflag": {"va": 0x0073E32B, "expect_target": "0x0070BF10",
                                    "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0073E32B)},
        "lazyinit_zero_on_fail": {"va": 0x0073E346, "expect": "C7 05 0C 59 BA 00 00 00 00 00",
                                  "hex": read_window(d, ib, secs, 0x0073E346, 10)},
        "selector_getter_20006": {"va": 0x0073C8D8, "expect": "A1 0C 59 BA 00 C3",
                                  "hex": read_window(d, ib, secs, 0x0073C8D8, 6)},
        "selector_dispatcher_entry": {"va": 0x0073C870, "expect": "8B 4C 24 04 33 C0",
                                      "hex": read_window(d, ib, secs, 0x0073C870, 6)},
        "dispatcher_jmptbl": {"va": 0x0073C8B4, "expect": "FF 24 8D FC C9 73 00",
                              "hex": read_window(d, ib, secs, 0x0073C8B4, 7),
                              "table_va": "0x%08X" % read_u32(d, ib, secs, 0x0073C8B7)},
        "dispatcher_entry5_selector_20006": {
            "note": "jump table at 0x0073C9FC, entry idx 5 (selector 0x4E26); measured target",
            "table_entry5_va": 0x0073C9FC + 5 * 4,
            "entry5_value": "0x%08X" % read_u32(d, ib, secs, 0x0073C9FC + 5 * 4)},
    }
    # ---- C. singleton/global reference censuses (the only static storage sites) ----
    refs590c = find_all(TEXT, struct.pack("<I", 0x00BA590C))
    pins["singleton_00BA590C_refs"] = {
        "count": len(refs590c),
        "sites": ["0x%08X" % (TVA + i) for i in refs590c],
        "ctx": {("0x%08X" % (TVA + i)): read_window(d, ib, secs, TVA + i - 6, 16)
                for i in refs590c},
    }
    refs12e4 = find_all(TEXT, struct.pack("<I", 0x00BA12E4))
    pins["manager_00BA12E4_refs"] = {
        "count": len(refs12e4),
        "sites": ["0x%08X" % (TVA + i) for i in refs12e4],
    }
    # ---- D. the setter chain pins (FUN_0070C680 + the loop + driver + registration) ----
    pins["setter_chain"] = {
        "setter_entry": {"va": 0x0070C680, "expect": "6A FF 68 75 C4 A0 00",
                         "hex": read_window(d, ib, secs, 0x0070C680, 7)},
        "setter_this_ESI": {"va": 0x0070C6BA, "expect": "8B F1",
                            "hex": read_window(d, ib, secs, 0x0070C6BA, 2)},
        "setter_EDI_zero": {"va": 0x0070C6BC, "expect": "33 FF",
                            "hex": read_window(d, ib, secs, 0x0070C6BC, 2)},
        "setter_guard_CMP_plus_84": {"va": 0x0070C6BE, "expect": "39 BE 84 00 00 00",
                                     "hex": read_window(d, ib, secs, 0x0070C6BE, 6)},
        "setter_guard_JE_already_attached": {"va": 0x0070C6C4, "expect": "74 07",
                                             "hex": read_window(d, ib, secs, 0x0070C6C4, 2)},
        "setter_PUSH_0xA4": {"va": 0x0070C6F9, "expect": "68 A4 00 00 00",
                             "hex": read_window(d, ib, secs, 0x0070C6F9, 5)},
        "setter_alloc_fail_JE": {"va": 0x0070C711, "expect": "74 09",
                                 "hex": read_window(d, ib, secs, 0x0070C711, 2)},
        "setter_fail_XOR_EAX": {"va": 0x0070C71C, "expect": "33 C0",
                                "hex": read_window(d, ib, secs, 0x0070C71C, 2)},
        "setter_MOV_ECX_newobj": {"va": 0x0070C713, "expect": "8B C8",
                                  "hex": read_window(d, ib, secs, 0x0070C713, 2)},
        "setter_CALL_stream_ctor": {"va": 0x0070C715, "expect_target": "0x00972380",
                                    "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0070C715)},
        "THE_STORE_plus_84": {"va": 0x0070C71E, "expect": "89 86 84 00 00 00",
                              "hex": read_window(d, ib, secs, 0x0070C71E, 6)},
        "setter_post_store_ecx_stream": {"va": 0x0070C73B, "expect": "8B C8",
                                         "hex": read_window(d, ib, secs, 0x0070C73B, 2)},
        "setter_post_store_CALL": {"va": 0x0070C742,
                                   "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0070C742)},
        "loop_entry_FUN_00703E80": {"va": 0x00703E80, "expect": "83 EC 08",
                                    "hex": read_window(d, ib, secs, 0x00703E80, 3)},
        "loop_MOV_EDI_elem": {"va": 0x00703EA7, "expect": "8B 3E",
                              "hex": read_window(d, ib, secs, 0x00703EA7, 2)},
        "loop_MOV_ECX_elem": {"va": 0x00703EB0, "expect": "8B CF",
                              "hex": read_window(d, ib, secs, 0x00703EB0, 2)},
        "loop_CALL_modecond": {"va": 0x00703EA9, "expect_target": "0x00703CD0",
                               "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00703EA9)},
        "loop_PUSH_0x40_slotpred": {"va": 0x00703EB4, "expect": "6A 40",
                                    "hex": read_window(d, ib, secs, 0x00703EB4, 2)},
        "loop_CALL_slotpred": {"va": 0x00703EB6, "expect_target": "0x0070CC80",
                               "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00703EB6)},
        "loop_PUSH_0x20": {"va": 0x00703EC3, "expect": "6A 20",
                           "hex": read_window(d, ib, secs, 0x00703EC3, 2)},
        "loop_CALL_flagtest_0x20": {"va": 0x00703EC5, "expect_target": "0x0070BF40",
                                    "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00703EC5)},
        "loop_PUSH_0x2000": {"va": 0x00703EDE, "expect": "68 00 20 00 00",
                             "hex": read_window(d, ib, secs, 0x00703EDE, 5)},
        "loop_CALL_flagtest_0x2000": {"va": 0x00703EE3, "expect_target": "0x0070BF40",
                                      "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00703EE3)},
        "loop_MOV_ECX_elem_before_setter": {"va": 0x00703EEC, "expect": "8B 0E",
                                            "hex": read_window(d, ib, secs, 0x00703EEC, 2)},
        "loop_PUSH_EBX_arg": {"va": 0x00703EEE, "expect": "53",
                              "hex": read_window(d, ib, secs, 0x00703EEE, 1)},
        "loop_PUSH_EBP_arg": {"va": 0x00703EEF, "expect": "55",
                              "hex": read_window(d, ib, secs, 0x00703EEF, 1)},
        "loop_CALL_setter": {"va": 0x00703EF0, "expect_target": "0x0070C680",
                             "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00703EF0)},
        "driver_entry_FUN_004B0980": {"va": 0x004B0980, "expect": "6A FF 68 4B C9 9A 00",
                                      "hex": read_window(d, ib, secs, 0x004B0980, 7)},
        "driver_local_0x80": {"va": 0x004B0A46, "expect": "C7 44 24 1C 80 00 00 00",
                               "hex": read_window(d, ib, secs, 0x004B0A46, 8)},
        "driver_local_8": {"va": 0x004B0A4E, "expect": "C7 44 24 20 08 00 00 00",
                           "hex": read_window(d, ib, secs, 0x004B0A4E, 8)},
        "driver_CALL_manager_getter": {"va": 0x004B0A56, "expect_target": "0x00415470",
                                       "measured_target": "0x%08X" % call_target(d, ib, secs, 0x004B0A56)},
        "driver_MOV_ECX_manager": {"va": 0x004B0A5B, "expect": "8B C8",
                                   "hex": read_window(d, ib, secs, 0x004B0A5B, 2)},
        "driver_CALL_bulk_attach": {"va": 0x004B0A5D, "expect_target": "0x00703E80",
                                    "measured_target": "0x%08X" % call_target(d, ib, secs, 0x004B0A5D)},
        "driver_string_cache": {"va": 0x00A7A83C, "string": "Cache\\"},
        "driver_string_parameters": {"va": 0x00A7A258, "string": "Parameters\\"},
        "driver_PUSH_cache_str": {"va": 0x004B09CD, "expect": "68 3C A8 A7 00",
                                  "hex": read_window(d, ib, secs, 0x004B09CD, 5),
                                  "imm32_value": "0x%08X" % read_u32(d, ib, secs, 0x004B09CE)},
        "driver_PUSH_parameters_str": {"va": 0x004B09F3, "expect": "68 58 A2 A7 00",
                                        "hex": read_window(d, ib, secs, 0x004B09F3, 5),
                                        "imm32_value": "0x%08X" % read_u32(d, ib, secs, 0x004B09F4)},
        "driver_call1": {"va": 0x004B09AF, "measured_target": "0x%08X" % call_target(d, ib, secs, 0x004B09AF)},
        "driver_call2": {"va": 0x004B09B6, "measured_target": "0x%08X" % call_target(d, ib, secs, 0x004B09B6)},
        "driver_call3": {"va": 0x004B09BD, "measured_target": "0x%08X" % call_target(d, ib, secs, 0x004B09BD)},
    }
    # ---- E. the registration chain (manager mode + list population) ----
    pins["registration_chain"] = {
        "modeinit_entry_FUN_007080C0": {"va": 0x007080C0, "expect": "8B 44 24 04",
                                        "hex": read_window(d, ib, secs, 0x007080C0, 4)},
        "modeinit_MOV_EDI_this": {"va": 0x007080C6, "expect": "8B F9",
                                  "hex": read_window(d, ib, secs, 0x007080C6, 2)},
        "modeinit_store_mode": {"va": 0x007080CA, "expect": "89 07",
                                "hex": read_window(d, ib, secs, 0x007080CA, 2)},
        "modeinit_first_loop_start": {"va": 0x007080D6, "expect": "BE 20 4E 00 00",
                                      "hex": read_window(d, ib, secs, 0x007080D6, 5),
                                      "esi_init": "0x%08X" % read_u32(d, ib, secs, 0x007080D7),
                                      "note": "ESI = 0x4E20 = 20000 (first class id)"},
        "modeinit_loop_CMP_0x4E4C": {"va": 0x007080EB, "expect": "81 FE 4C 4E 00 00",
                                     "hex": read_window(d, ib, secs, 0x007080EB, 6),
                                     "bound_imm": "0x%08X" % read_u32(d, ib, secs, 0x007080ED),
                                     "note": "loop while class_id < 0x4E4C (20044)"},
        "modeinit_loop_CALL_register": {"va": 0x007080E3, "expect_target": "0x00707FB0",
                                        "measured_target": "0x%08X" % call_target(d, ib, secs, 0x007080E3)},
        "modeinit_second_range_start": {"va": 0x007080F3, "expect": "BE C1 5D 00 00",
                                        "hex": read_window(d, ib, secs, 0x007080F3, 5),
                                        "esi_init": "0x%08X" % read_u32(d, ib, secs, 0x007080F4),
                                        "note": "ESI = 0x5DC1 = 24001"},
        "modeinit_second_CMP": {"va": 0x00708103, "expect": "81 FE D2 5D 00 00",
                                "hex": read_window(d, ib, secs, 0x00708103, 6),
                                "bound_imm": "0x%08X" % read_u32(d, ib, secs, 0x00708105)},
        "modeinit_second_CALL_register": {"va": 0x007080FB, "expect_target": "0x00707FB0",
                                          "measured_target": "0x%08X" % call_target(d, ib, secs, 0x007080FB)},
        "modeinit_caller": {"va": 0x00417524, "expect_target": "0x007080C0",
                            "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00417524)},
        "modeinit_caller_PUSH_2": {"va": 0x0041751B, "expect": "6A 02",
                                   "hex": read_window(d, ib, secs, 0x0041751B, 2)},
        "modeinit_caller_MOV_ECX_mgr": {"va": 0x00417522, "expect": "8B C8",
                                        "hex": read_window(d, ib, secs, 0x00417522, 2)},
        "register_entry_FUN_00707FB0": {"va": 0x00707FB0, "expect": "6A FF 68 F8 C0 A0 00",
                                        "hex": read_window(d, ib, secs, 0x00707FB0, 7)},
        "register_MOV_EBX_this": {"va": 0x00707FD6, "expect": "8B D9",
                                  "hex": read_window(d, ib, secs, 0x00707FD6, 2)},
        "register_PUSH_classid_arg": {"va": 0x00707FDE, "expect": "50",
                                      "hex": read_window(d, ib, secs, 0x00707FDE, 1)},
        "register_CALL_dispatcher": {"va": 0x00707FDF, "expect_target": "0x0073C870",
                                     "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00707FDF)},
        "register_MOV_EDI_factory": {"va": 0x00707FE4, "expect": "8B F8",
                                     "hex": read_window(d, ib, secs, 0x00707FE4, 2)},
        "append_MOV_EAX_list_end": {"va": 0x00708065, "expect": "8B 43 7C",
                                   "hex": read_window(d, ib, secs, 0x00708065, 3)},
        "append_CMP_capacity": {"va": 0x00708068, "expect": "3B 83 80 00 00 00",
                                "hex": read_window(d, ib, secs, 0x00708068, 6)},
        "append_LEA_list_begin": {"va": 0x0070806E, "expect": "8D 4B 78",
                                  "hex": read_window(d, ib, secs, 0x0070806E, 3)},
        "append_store_elem": {"va": 0x00708077, "expect": "89 38",
                              "hex": read_window(d, ib, secs, 0x00708077, 2)},
        "append_end_plus_4": {"va": 0x00708079, "expect": "83 41 04 04",
                              "hex": read_window(d, ib, secs, 0x00708079, 4)},
        "manager_ctor_entry_FUN_00707E50": {"va": 0x00707E50, "expect": "6A FF 68 D4 C0 A0 00",
                                            "hex": read_window(d, ib, secs, 0x00707E50, 7)},
        "manager_ctor_list_zero": {"va": 0x00707EB0, "expect": "89 5E 78 89 5E 7C",
                                   "hex": read_window(d, ib, secs, 0x00707EB0, 6)},
        "manager_ctor_cap_zero": {"va": 0x00707EB6, "expect": "89 9E 80 00 00 00",
                                  "hex": read_window(d, ib, secs, 0x00707EB6, 6)},
        "manager_getter_entry": {"va": 0x00415470, "expect": "6A FF 68 CB 62 99 00",
                                 "hex": read_window(d, ib, secs, 0x00415470, 7)},
        "manager_getter_PUSH_0x100": {"va": 0x0041549A, "expect": "68 00 01 00 00",
                                      "hex": read_window(d, ib, secs, 0x0041549A, 5)},
        "manager_getter_CALL_ctor": {"va": 0x004154B9, "expect_target": "0x00707E50",
                                     "measured_target": "0x%08X" % call_target(d, ib, secs, 0x004154B9)},
        "manager_getter_store_global": {"va": 0x004154BE, "expect": "A3 E4 12 BA 00",
                                         "hex": read_window(d, ib, secs, 0x004154BE, 5)},
    }
    # ---- F. the mode condition + slot predicate + flag test (condition battery) ----
    pins["condition_battery"] = {
        "modecond_FUN_00703CD0": {"va": 0x00703CD0,
                                  "hex": read_window(d, ib, secs, 0x00703CD0, 0x14),
                                  "note": "MOV EAX,[ECX]; CMP EAX,1; JE+8; CMP EAX,3; JE+3; XOR EAX,EAX; RET; MOV EAX,1; RET"},
        "slotpred_FUN_0070CC80_entry": {"va": 0x0070CC80, "expect": "53 56 57 8B F1",
                                        "hex": read_window(d, ib, secs, 0x0070CC80, 5)},
        "slotpred_slot_begin_plus_88": {"va": 0x0070CC8F, "expect": "8B BE 88 00 00 00",
                                        "hex": read_window(d, ib, secs, 0x0070CC8F, 6)},
        "slotpred_slot_end_plus_8C": {"va": 0x0070CC89, "expect": "8B 96 8C 00 00 00",
                                      "hex": read_window(d, ib, secs, 0x0070CC89, 6)},
        "slotpred_callback_ptr": {"va": 0x0070CC9A, "expect": "B8 F0 BE 70 00",
                                  "hex": read_window(d, ib, secs, 0x0070CC9B, 5),
                                  "imm32_value": "0x%08X" % read_u32(d, ib, secs, 0x0070CC9B)},
        "slotpred_CALL_scan": {"va": 0x0070CCA3,
                               "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0070CCA3)},
        "flagtest_FUN_0070BF40_body_transcription": {"va": 0x0070BF40,
            "hex": read_window(d, ib, secs, 0x0070BF40, 14),
            "note": "14-byte body, transcription-level only, NOT counted in the function ledger"},
    }
    # ---- G. the stream object ctor (Phase D) ----
    pins["stream_ctor"] = {
        "entry": {"va": 0x00972380, "expect": "6A FF 68 F5 A2 A4 00",
                  "hex": read_window(d, ib, secs, 0x00972380, 7)},
        "this_ESI": {"va": 0x009723A6, "expect": "8B F1",
                     "hex": read_window(d, ib, secs, 0x009723A6, 2)},
        "member_18_minus1": {"va": 0x009723D3, "expect": "C7 46 18 FF FF FF FF",
                             "hex": read_window(d, ib, secs, 0x009723D3, 7)},
        "cursor_at_3C_PUSH_1": {"va": 0x0097242A, "expect": "6A 01",
                                "hex": read_window(d, ib, secs, 0x0097242A, 2)},
        "cursor_at_3C_PUSH_0x80": {"va": 0x0097242C, "expect": "68 80 00 00 00",
                                   "hex": read_window(d, ib, secs, 0x0097242C, 5)},
        "cursor_at_3C_size_store": {"va": 0x00972443, "expect": "C7 47 04 80 00 00 00",
                                    "hex": read_window(d, ib, secs, 0x00972443, 7)},
        "cursor_at_3C_buffer_new": {"va": 0x00972449, "expect": "E8",
                                    "measured_target": "0x%08X" % call_target(d, ib, secs, 0x00972449)},
        "cursor_at_3C_buffer_store": {"va": 0x00972452, "expect": "89 07",
                                      "hex": read_window(d, ib, secs, 0x00972452, 2)},
        "cursor_at_3C_flag": {"va": 0x00972454, "expect": "C6 47 11 01",
                              "hex": read_window(d, ib, secs, 0x00972454, 4)},
        "tail_88_flag_1": {"va": 0x00972499, "expect": "89 86 88 00 00 00",
                           "hex": read_window(d, ib, secs, 0x00972499, 6)},
        "tail_8C_size_0x80": {"va": 0x0097249F, "expect": "C7 86 8C 00 00 00 80 00 00 00",
                              "hex": read_window(d, ib, secs, 0x0097249F, 10)},
        "tail_94_flag_1": {"va": 0x009724AF, "expect": "89 86 94 00 00 00",
                           "hex": read_window(d, ib, secs, 0x009724AF, 6)},
        "tail_98_size_0x80": {"va": 0x009724B5, "expect": "C7 86 98 00 00 00 80 00 00 00",
                              "hex": read_window(d, ib, secs, 0x009724B5, 10)},
        "return_this": {"va": 0x009724C5, "expect": "8B C6",
                        "hex": read_window(d, ib, secs, 0x009724C5, 2)},
        "vtable_store_search": {
            "note": "no C7 06/89 0E/89 07-style vtable store exists in the ctor extent 0x00972380..0x009724D9 (first CC pair at 0x009724DA); the object is non-polymorphic (direct-call method family)",
            "extent_first_cc_pair": "0x009724DA"},
        "ctor_call_site_in_templates_reader_region": {
            "va": 0x0072FA76, "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0072FA76),
            "note": "LEAD ONLY: the same ctor is called inside the region of the templates.vfs reader chain (FUN_0072FA30, R1 canon); reader-family class coincidence, NOT a backing-provenance bridge"},
    }
    # ---- H. reader-bridge + manager-list re-pin in the small-method region ----
    pins["small_method_region"] = {
        "bridge_read_plus_84": {"va": 0x0070BFD0, "expect": "8B 89 84 00 00 00",
                                "hex": read_window(d, ib, secs, 0x0070BFD0, 6),
                                "note": "transcription-level window: MOV ECX,[ECX+0x84]; TEST ECX,ECX; JE ret0; MOV EAX,[ESP+4]; PUSH EAX; CALL 0x009724DF; MOV AL,1; RET 4 / XOR AL,AL; RET 4"},
        "bridge_CALL_target": {"va": 0x0070BFDF,
                               "measured_target": "0x%08X" % call_target(d, ib, secs, 0x0070BFDF)},
    }
    # ---- I. caller censuses (call-target counts for the chain functions) ----
    def callers_of(target):
        res = []
        i = 0
        n = len(TEXT)
        while i < n - 5:
            if TEXT[i] in (0xE8, 0xE9):
                rel = struct.unpack_from("<i", TEXT, i + 1)[0]
                if TVA + i + 5 + rel == target:
                    res.append("0x%08X/%s" % (TVA + i, "CALL" if TEXT[i] == 0xE8 else "JMP"))
            i += 1
        return res
    pins["caller_censuses"] = {
        "FUN_0070C680_setter": callers_of(0x0070C680),
        "FUN_00703E80_bulk_attach": callers_of(0x00703E80),
        "FUN_004B0980_driver": callers_of(0x004B0980),
        "FUN_00707FB0_register": callers_of(0x00707FB0),
        "FUN_007080C0_modeinit": callers_of(0x007080C0),
        "FUN_00972380_stream_ctor": callers_of(0x00972380),
        "FUN_00415470_manager_getter_count": len(callers_of(0x00415470)),
        "FUN_0073C870_dispatcher_count": len(callers_of(0x0073C870)),
    }

    # pin evaluation
    out["pins"] = pins
    fails = []
    def check(name, expect, measured):
        ok = (str(expect).lower() == str(measured).lower())
        if not ok:
            fails.append({"pin": name, "expect": expect, "measured": measured})
        return ok
    # byte-pin checks
    for grp, items in pins.items():
        if not isinstance(items, dict):
            continue
        for k, v in items.items():
            if isinstance(v, dict) and "expect" in v and "hex" in v:
                check("%s.%s" % (grp, k), v["expect"], v["hex"])
    # target checks
    for grp, items in pins.items():
        if not isinstance(items, dict):
            continue
        for k, v in items.items():
            if isinstance(v, dict) and "expect_target" in v and "measured_target" in v:
                check("%s.%s" % (grp, k), v["expect_target"], v["measured_target"])
    # string checks
    def rstring(va):
        off = va_to_off(ib, secs, va)
        return d[off:d.find(b"\x00", off)].decode("ascii")
    check("driver_string_cache", "Cache\\", rstring(0x00A7A83C))
    check("driver_string_parameters", "Parameters\\", rstring(0x00A7A258))
    # dispatcher entry-5 check
    check("dispatcher_entry5", "0x0073C8D8",
          "0x%08X" % read_u32(d, ib, secs, 0x0073C9FC + 5 * 4))
    # singleton ref count checks (measured facts used by the chain)
    check("singleton_00BA590C_ref_count", 9, len(refs590c))
    check("manager_00BA12E4_ref_count", 3, len(refs12e4))
    out["pin_checks"] = {"total_expected_checked": True, "failures": fails,
                         "fail_count": len(fails)}

    with open(os.path.join(RUN, "01_RAW", "S1_ANCHORS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S1 done. pin_failures=%d; singleton_refs=%d; manager_refs=%d"
          % (len(fails), len(refs590c), len(refs12e4)))

if __name__ == "__main__":
    main()
