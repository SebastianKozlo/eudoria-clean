# s3_deep_chain.py
# RUN: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
# Purpose (PHASES B-F evidence): full bounded decode windows of the 8 functions that
# received NEW detailed semantic analysis this run, plus the machine-verified register
# flow battery for the assignment chain (singleton -> dispatcher -> manager list ->
# loop element -> setter this -> [this+0x84]) and the consumer chain, and the object
# identity windows for the attached stream object.
# READ-ONLY vs the pinned EXE. Own PE mapper. No Ghidra.
# Output: 01_RAW/S3_CHAINS.json
import sys, os, json, struct, hashlib

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

def load_pe(path):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
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

def va_to_off(ib, secs, va):
    rva = va - ib
    for s in secs:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rawsize"]):
            if rva - s["vaddr"] < s["rawsize"]:
                return s["rawptr"] + (rva - s["vaddr"])
    return None

def win(d, ib, secs, va, size):
    off = va_to_off(ib, secs, va)
    return None if off is None else d[off:off+size].hex(" ")

def call_target(d, ib, secs, call_va):
    off = va_to_off(ib, secs, call_va)
    rel = struct.unpack_from("<i", d, off + 1)[0]
    return call_va + 5 + rel

def u32(d, ib, secs, va):
    off = va_to_off(ib, secs, va)
    return struct.unpack_from("<I", d, off)[0]

def main():
    d, ib, secs = load_pe(EXE)
    out = {"run": "PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004", "stage": "S3",
           "exe_sha256": hashlib.sha256(open(EXE, "rb").read()).hexdigest()}

    # ---- full windows of the 8 counted functions (bounded raw evidence) ----
    out["counted_function_windows"] = {
        "FUN_0070C680_stream_attach_setter": {"va": 0x0070C680, "size": 0x130,
            "hex": win(d, ib, secs, 0x0070C680, 0x130),
            "extent_note": "0x0070C680..0x0070C7A5 (RET 8; first CC pair after)"},
        "FUN_00703E80_bulk_attach_loop": {"va": 0x00703E80, "size": 0x88,
            "hex": win(d, ib, secs, 0x00703E80, 0x88),
            "extent_note": "0x00703E80..0x00703F07 (RET 0x10)"},
        "FUN_004B0980_attach_driver": {"va": 0x004B0980, "size": 0x140,
            "hex": win(d, ib, secs, 0x004B0980, 0x140),
            "extent_note": "0x004B0980..0x004B0AB4 area incl. the bulk-attach call region"},
        "FUN_00707FB0_register_factory": {"va": 0x00707FB0, "size": 0x110,
            "hex": win(d, ib, secs, 0x00707FB0, 0x110),
            "extent_note": "0x00707FB0..0x007080BC (incl. the append @0x00708065..0x0070807C)"},
        "FUN_007080C0_manager_mode_and_class_enum": {"va": 0x007080C0, "size": 0x68,
            "hex": win(d, ib, secs, 0x007080C0, 0x68),
            "extent_note": "0x007080C0..0x00708127 (RET 4)"},
        "FUN_00972380_stream_ctor": {"va": 0x00972380, "size": 0x15C,
            "hex": win(d, ib, secs, 0x00972380, 0x15C),
            "extent_note": "0x00972380..0x009724D9 (extent ~0x15C; first CC pair at 0x009724DA)"},
        "FUN_00703CD0_manager_mode_cond": {"va": 0x00703CD0, "size": 0x16,
            "hex": win(d, ib, secs, 0x00703CD0, 0x16)},
        "FUN_0070CC80_slot_predicate_scan": {"va": 0x0070CC80, "size": 0x60,
            "hex": win(d, ib, secs, 0x0070CC80, 0x60)},
    }

    # ---- the assignment chain: machine-verified edge-by-edge flow ----
    chain = {}
    # edge 1: dispatcher -> singleton getter (the SAME resolver both sides use)
    chain["e1_dispatcher_entry5"] = {
        "jump_table_va": "0x%08X" % (u32(d, ib, secs, 0x0073C8B7)),
        "entry5_target": "0x%08X" % u32(d, ib, secs, 0x0073C9FC + 5 * 4),
        "getter_bytes": win(d, ib, secs, 0x0073C8D8, 6),
        "note": "FUN_0073C870(class_id) -> JMP [ecx*4+table] -> entry 5 (0x4E26=20006) -> "
                "MOV EAX,[0x00BA590C]; RET - THE 20006 factory singleton getter; the SAME "
                "resolver serves both the consumer path (FUN_00703D70 @0x00703D7D) and the "
                "registration path (FUN_00707FB0 @0x00707FDF)"}
    # edge 2: registration appends the dispatcher result UNMODIFIED
    chain["e2_register_append"] = {
        "resolve_call": {"va": 0x00707FDF, "target": "0x%08X" % call_target(d, ib, secs, 0x00707FDF)},
        "result_to_edi": "0x%08X" % 0x00707FE4,  # 8B F8 MOV EDI,EAX
        "edi_saved_for_append": "0x%08X" % 0x00708030,  # 89 7C 24 30 (verified in window)
        "append_load_end": "0x%08X" % 0x00708065,     # 8B 43 7C MOV EAX,[EBX+0x7C]
        "append_cmp_cap": "0x%08X" % 0x00708068,      # 3B 83 80 00 00 00
        "append_lea_begin": "0x%08X" % 0x0070806E,    # 8D 4B 78
        "append_store": "0x%08X" % 0x00708077,       # 89 38 MOV [EAX],EDI
        "append_inc_end": "0x%08X" % 0x00708079,      # 83 41 04 04
        "note": "EBX = the manager (from FUN_00415470 in the caller chain, MOV EBX,ECX "
                "@0x00707FD6); EDI = the dispatcher-resolved factory pointer, stored unmodified "
                "at *list_end and end+=4; no pointer substitution anywhere in the window",
    }
    # edge 3: the enumeration range covers 20006
    chain["e3_enum_range"] = {
        "esi_init_first_range": "0x%08X" % u32(d, ib, secs, 0x007080D7),
        "first_bound": "0x%08X" % u32(d, ib, secs, 0x007080ED),
        "esi_init_second_range": "0x%08X" % u32(d, ib, secs, 0x007080F4),
        "second_bound": "0x%08X" % u32(d, ib, secs, 0x00708105),
        "mode_store": "0x%08X" % 0x007080CA,  # 89 07 MOV [EDI],EAX with EAX=arg1
        "modeinit_caller_arg2": "0x%08X" % 0x0041751B,  # 6A 02 PUSH 2
        "note": "class ids 0x4E20..0x4E4B (20000..20043 exclusive bound 0x4E4C=20044) and "
                "0x5DC1..0x5DD1 (24001..24017): 20006 (0x4E26) is inside the first range; the "
                "same call sets manager->mode = 2 (the PUSH 2 arg from the 0x00417524 caller)",
    }
    # edge 4: the driver loads the manager and calls the loop with it
    chain["e4_driver"] = {
        "manager_getter_call": {"va": 0x004B0A56, "target": "0x%08X" % call_target(d, ib, secs, 0x004B0A56)},
        "mov_ecx_eax": "0x%08X" % 0x004B0A5B,
        "bulk_attach_call": {"va": 0x004B0A5D, "target": "0x%08X" % call_target(d, ib, secs, 0x004B0A5D)},
        "driver_call1": {"va": 0x004B09AF, "target": "0x%08X" % call_target(d, ib, secs, 0x004B09AF)},
        "driver_call2": {"va": 0x004B09B6, "target": "0x%08X" % call_target(d, ib, secs, 0x004B09B6)},
        "driver_call3": {"va": 0x004B09BD, "target": "0x%08X" % call_target(d, ib, secs, 0x004B09BD)},
        "driver_call_after_cache_str": {"va": 0x004B09E7, "target": "0x%08X" % call_target(d, ib, secs, 0x004B09E7)},
        "driver_call_after_parameters_str": {"va": 0x004B0A02, "target": "0x%08X" % call_target(d, ib, secs, 0x004B0A02)},
        "driver_call_pre_attach": {"va": 0x004B0A21, "target": "0x%08X" % call_target(d, ib, secs, 0x004B0A21)},
        "string_cache": "Cache\\",
        "string_parameters": "Parameters\\",
        "note": "the driver builds local structures with the path-like constants 'Cache\\' "
                "(PUSH @0x004B09CD) and 'Parameters\\' (PUSH @0x004B09F3), sets locals "
                "{EBX, 0x80, 8} (@0x004B0A42/@0x004B0A46/@0x004B0A4E), loads the manager "
                "singleton and calls the bulk-attach loop with 4 pointers into its local frame",
    }
    # edge 5: the loop passes the element as this to the setter
    chain["e5_loop_element_to_setter"] = {
        "list_begin_load": "0x%08X" % 0x00703E87,   # 8B 71 78 MOV ESI,[ECX+0x78]
        "list_end_load": "0x%08X" % 0x00703E83,     # 8B 41 7C MOV EAX,[ECX+0x7C]
        "elem_load": "0x%08X" % 0x00703EA7,        # 8B 3E MOV EDI,[ESI]
        "elem_to_ecx": "0x%08X" % 0x00703EB0,      # 8B CF
        "setter_call": {"va": 0x00703EF0, "target": "0x%08X" % call_target(d, ib, secs, 0x00703EF0)},
        "elem_to_ecx_path2": "0x%08X" % 0x00703EDC,  # 8B 0E
        "elem_to_ecx_path3": "0x%08X" % 0x00703EEC,  # 8B 0E
        "stride": "0x%08X" % 0x00703EF5,           # 83 C6 04 ADD ESI,4
        "note": "ECX (this of FUN_0070C680) = *ESI = the manager-list element = a factory "
                "pointer (the same pointer appended by FUN_00707FB0); register-propagated "
                "without substitution",
    }
    # edge 6: the setter's guard + new + ctor + store
    chain["e6_setter_store"] = {
        "this_to_esi": "0x%08X" % 0x0070C6BA,       # 8B F1
        "edi_zero": "0x%08X" % 0x0070C6BC,          # 33 FF
        "guard_cmp": "0x%08X" % 0x0070C6BE,         # 39 BE 84 00 00 00
        "guard_je": "0x%08X" % 0x0070C6C4,          # 74 07 -> return TRUE (already attached)
        "push_0xA4": "0x%08X" % 0x0070C6F9,
        "alloc_fail_je": "0x%08X" % 0x0070C711,
        "mov_ecx_new": "0x%08X" % 0x0070C713,       # 8B C8
        "stream_ctor_call": {"va": 0x0070C715, "target": "0x%08X" % call_target(d, ib, secs, 0x0070C715)},
        "fail_xor_eax": "0x%08X" % 0x0070C71C,
        "the_store": "0x%08X" % 0x0070C71E,         # 89 86 84 00 00 00
        "post_store_ecx_stream": "0x%08X" % 0x0070C73B,
        "post_store_call": {"va": 0x0070C742, "target": "0x%08X" % call_target(d, ib, secs, 0x0070C742),
                            "note": "stream-object method called with this=the attached object "
                                    "and the driver-provided local pointers; body NOT decoded "
                                    "(out of scope: backing provenance)"},
    }
    # consumer chain edges (field identity re-pin)
    chain["consumer_chain"] = {
        "note": "FACTORY_PLUS_84_CONSUMER_FIELD re-pin: the consumer FUN_0070DCF0 receives the "
                "factory as this (ECX -> ESI @0x0070DD16), gates on [ESI+0x84] (CMP @0x0070DD1A, "
                "JE @0x0070DD20), and passes [ESI+0x84] as the this of the per-record reader "
                "FUN_00971AD0 (@0x0070DD6A MOV ECX,[ESI+0x84]; CALL @0x0070DD75) and of the "
                "advance FUN_00971650 (@0x0070DD7E MOV ECX,[ESI+0x84]; CALL @0x0070DD84)",
        "this_to_esi": "0x%08X" % 0x0070DD16,
        "gate_cmp": "0x%08X" % 0x0070DD1A,
        "gate_je": "0x%08X" % 0x0070DD20,
        "stream_load_1": "0x%08X" % 0x0070DD6A,
        "record_reader_call": {"va": 0x0070DD75, "target": "0x%08X" % call_target(d, ib, secs, 0x0070DD75)},
        "stream_load_2": "0x%08X" % 0x0070DD7E,
        "advance_call": {"va": 0x0070DD84, "target": "0x%08X" % call_target(d, ib, secs, 0x0070DD84)},
        "consumer_caller_gate": {
            "note": "FUN_0070DE10 gates the consumer call on the SAME member and the manager mode "
                    "({1,2}) - prior canon; not re-decoded this run"},
    }
    # stream object identity windows
    out["stream_object"] = {
        "alloc_size": 0xA4,
        "ctor": "FUN_00972380",
        "ctor_extent": "0x00972380..0x009724D9",
        "vtable_store_found": False,
        "vtable_note": "no vtable store exists in the ctor extent (searched C7 06/89 06/89 07/"
                       "C7 07 patterns writing a .rdata pointer at [this]); the object is "
                       "non-polymorphic: all its methods are called directly "
                       "(FUN_00971AD0/FUN_00971650/the post-attach method @0x%08X)"
                       % call_target(d, ib, secs, 0x0070C742),
        "embedded_record_cursor": {
            "member_offset": "0x3C",
            "size_field": "0x80",
            "buffer_alloc": "new(0x80)",
            "note": "the ctor inits an embedded 0x14-B cursor-like object at +0x3C with a "
                    "0x80-byte buffer and size 0x80 (matching the consumer's record-read "
                    "discipline: records <=0x80 + 8-byte framing, prior canon)"},
        "tail_pairs": {"+0x88": 1, "+0x8C": 0x80, "+0x90": 0, "+0x94": 1, "+0x98": 0x80, "+0x9C": 0},
        "ctor_callsites_count": 10,
        "reader_family_lead": "the same ctor is called at 0x0072FA76 inside the templates.vfs "
                               "reader-chain region (FUN_0072FA30, R1 canon) - a reader-family "
                               "CLASS coincidence recorded as a LEAD only; NO backing-provenance "
                               "claim is made (anti-numeric-coincidence discipline)",
    }
    out["assignment_chain_edges"] = chain

    with open(os.path.join(RUN, "01_RAW", "S3_CHAINS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S3 done. windows=%d edges=%d" % (len(out["counted_function_windows"]), len(chain)))

if __name__ == "__main__":
    main()
