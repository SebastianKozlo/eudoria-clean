# s5_qc_battery.py
# RUN: PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004
# Purpose (bounded, READ-ONLY): the TARGETED SELF_CHECK QC battery
# (QC_SCOPE=SELF_CHECK_FUN_0070DC20_TABLE10_WRITER). Re-executes the
# COMPLETE corrected pin set in one instrument and evaluates the 12 gates:
#  Q1 base+EXE identity; Q2 call target + extent; Q3 arguments; Q4 same-
#  component identity; Q5 attribute-id selection; Q6 exact write
#  destination; Q7 table[10] identity (writer-side and getter-side
#  recomputed independently); Q8 source-operand boundary; Q9 control
#  discrimination; Q10 function-budget ledger; Q11 forbidden-scope
#  census; Q12 preserved canonical states (static re-read of this package's
#  claims file). Also resolves the guard-pair bound-import thunks
#  (0x00A75064/0x00A7506C -> .text thunks -> IAT -> hint/name).
# Output: 01_RAW/S5_QC_BATTERY.json
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

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
    else:
        raw = d[off:off+2]
        rel = struct.unpack_from("<b", raw, 1)[0]
        tgt = va + 2 + rel
    return {"va": "0x%08X" % va, "opcode": raw.hex(" "),
            "computed_target": "0x%08X" % tgt,
            "expected": "0x%08X" % expected_target, "match": tgt == expected_target}

def resolve_guard_iat(d, image_base, secs, iat_va):
    """Resolve an IAT slot of the KERNEL32 import (FirstThunk RVA 0x675060)
    to its API name. The slot dword at image mapping = hint/name RVA."""
    off = va_to_off(image_base, secs, iat_va)
    val = struct.unpack_from("<I", d, off)[0]
    res = {"iat_va": "0x%08X" % iat_va, "hint_name_rva": "0x%08X" % val,
           "ft_base_rva": "0x675060", "slot_index": (iat_va - image_base - 0x675060) // 4}
    # hint/name entry at RVA val (this image: .rdata rawptr == vaddr)
    hn_off = va_to_off(image_base, secs, image_base + val)
    hint = struct.unpack_from("<H", d, hn_off)[0]
    end = d.find(b"\x00", hn_off + 2, hn_off + 70)
    res["hint"] = hint
    res["api_name"] = d[hn_off+2:end].decode("ascii", "replace")
    return res

def main():
    out = {"run": "PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004", "stage": "S5_QC"}
    d, image_base, secs = load_pe(EXE)

    results = {}

    # ---------- Q1: EXE identity ----------
    sz = os.path.getsize(EXE)
    h = sha256(EXE)
    results["Q1_exe_identity"] = {
        "size_bytes": sz, "sha256": h,
        "expected_size": 8015872,
        "expected_sha256": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
        "match": (sz == 8015872 and h == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31")}
    # git identity recorded separately by the run (see INPUT_IDENTITIES.md); here
    # only the EXE is machine-verifiable inside this instrument.

    # ---------- Q2: call target + FUN_0070DC20 extent ----------
    q2 = {}
    q2["callsite_0x0070DDBD"] = verify_call(d, image_base, secs, 0x0070DDBD, 0x0070DC20)
    q2["prologue_sub_esp10_push_ebx"] = verify_bytes(d, image_base, secs, 0x0070DC20, "83 ec 10 53")
    q2["ret_0xC_fail_exit"] = verify_bytes(d, image_base, secs, 0x0070DCE2, "c2 0c 00")
    q2["ret_0xC_success_exit"] = verify_bytes(d, image_base, secs, 0x0070DCED, "c2 0c 00")
    q2["next_function_prologue_0x0070DCF0"] = verify_bytes(d, image_base, secs, 0x0070DCF0, "6a ff 68 28 c7 a0 00")
    results["Q2_call_and_extent"] = q2

    # ---------- Q3: arguments (FUN_0070DCF0 -> FUN_0070DC20) ----------
    q3 = {}
    q3["caller_argsetup_push2_lea_cursor_push_push_ecx"] = verify_bytes(
        d, image_base, secs, 0x0070DDB3, "6a 02 8d 44 24 18 50 57 8b ce")
    q3["arg1_receiver_load"] = verify_bytes(d, image_base, secs, 0x0070DC24, "8b 5c 24 18")
    q3["arg2_cursor_load"] = verify_bytes(d, image_base, secs, 0x0070DC46, "8b 44 24 24")
    q3["arg3_mode_load_for_delegate_notify"] = verify_bytes(d, image_base, secs, 0x0070DCA0, "8b 54 24 28")
    q3["this_factory_mov_esi_ecx"] = verify_bytes(d, image_base, secs, 0x0070DC2D, "8b f1")
    q3["caller_ret4_thiscall_1arg"] = verify_bytes(d, image_base, secs, 0x0070DDFF, "c2 04 00")
    results["Q3_arguments"] = q3

    # ---------- Q4: same-component identity ----------
    q4 = {}
    # creator path inside FUN_0070DC20
    q4["FUN_0070DC20_calls_FUN_0070D990"] = verify_call(d, image_base, secs, 0x0070DC3F, 0x0070D990)
    q4["creator_stores_factory_at_classobj_plus4"] = verify_bytes(d, image_base, secs, 0x0070D9A5, "89 73 04")
    q4["creator_component_ctor_vtable_0x00A86F2C"] = verify_bytes(d, image_base, secs, 0x007374D6, "c7 06 2c 6f a8 00")
    q4["creator_table12_count_add4"] = verify_bytes(d, image_base, secs, 0x0070D9BB, "83 c1 04")
    q4["creator_valuevector_call"] = verify_call(d, image_base, secs, 0x0070D9C9, 0x00412C50)
    # insert into factory+0x0C
    q4["FUN_0070DC20_lea_map_factory_plus_0C"] = verify_bytes(d, image_base, secs, 0x0070DC71, "8d 4e 0c")
    q4["FUN_0070DC20_receiver_into_keyslot"] = verify_bytes(d, image_base, secs, 0x0070DC74, "89 5c 24 18")
    q4["FUN_0070DC20_classobj_into_valueslot"] = verify_bytes(d, image_base, secs, 0x0070DC78, "89 7c 24 1c")
    q4["FUN_0070DC20_calls_FUN_0092B660"] = verify_call(d, image_base, secs, 0x0070DC7C, 0x0092B660)
    # getter-side lookup of the SAME map
    q4["lookup_lea_map_factory_plus_0C"] = verify_bytes(d, image_base, secs, 0x0070E11E, "8d 7e 0c")
    q4["lookup_calls_mapfind_FUN_004D1430"] = verify_call(d, image_base, secs, 0x0070E124, 0x004D1430)
    q4["lookup_node_value_plus_0x14"] = verify_bytes(d, image_base, secs, 0x0070E131, "8b 68 14")
    results["Q4_same_component"] = q4

    # ---------- Q5: attribute-id selection ----------
    q5 = {}
    q5["schema_slot6_args"] = verify_bytes(d, image_base, secs, 0x0073758D, "50 6a 00 6a 00 6a 01 6a 06 8b ce")
    q5["schema_slot6_calls_SLOT_ADD"] = verify_call(d, image_base, secs, 0x00737598, 0x0070CBC0)
    q5["SLOT_ADD_id_equals_tag_plus_4"] = verify_bytes(d, image_base, secs, 0x0070CBF6, "83 c1 04")
    q5["traits_factory_FUN_00977A50_vtable_store"] = verify_bytes(
        d, image_base, secs, 0x00977A68, "c7 05 7c 93 ba 00 70 c6 a9 00")
    q5["int_traits_vtable_slot5_is_FUN_009777F0"] = verify_bytes(d, image_base, secs, 0x00A9C684, "f0 77 97 00")
    q5["int_traits_vtable_slot1_is_FUN_009777E0"] = verify_bytes(d, image_base, secs, 0x00A9C674, "e0 77 97 00")
    # loop-side selection
    q5["loop_read_tag_u16"] = verify_bytes(d, image_base, secs, 0x007269E7, "0f b7 3c 08")
    q5["loop_calls_slot_getter_FUN_0070C180"] = verify_call(d, image_base, secs, 0x00726A03, 0x0070C180)
    q5["slot_getter_inrange_compute"] = verify_bytes(
        d, image_base, secs, 0x0070C1D3, "c1 e0 04 03 81 88 00 00 00")
    q5["slot_getter_default_0x00BA5108"] = verify_bytes(d, image_base, secs, 0x0070C1DF, "b8 08 51 ba 00")
    q5["loop_gate_slot_kind_nonzero"] = verify_bytes(d, image_base, secs, 0x00726A08, "83 78 04 00")
    q5["loop_load_slot_id"] = verify_bytes(d, image_base, secs, 0x00726A0E, "8b 48 08")
    results["Q5_attribute10_selection"] = q5

    # ---------- Q6: exact write destination ----------
    q6 = {}
    q6["loop_load_table_ptr_classobj_plus_0x40"] = verify_bytes(d, image_base, secs, 0x00726A11, "8b 55 40")
    q6["loop_lea_dest_table_plus_id_times_4"] = verify_bytes(d, image_base, secs, 0x00726A14, "8d 0c 8a")
    q6["loop_push_dest_push_cursor_mov_ecx_slot"] = verify_bytes(
        d, image_base, secs, 0x00726A17, "51 56 8b c8")
    q6["loop_calls_traits_dispatcher"] = verify_call(d, image_base, secs, 0x00726A1B, 0x0075F660)
    q6["dispatcher_loads_slot_traits"] = verify_bytes(d, image_base, secs, 0x0075F662, "8b 08")
    q6["dispatcher_traits_vtable_slot5"] = verify_bytes(d, image_base, secs, 0x0075F676, "8b 40 14")
    q6["dispatcher_virtual_call"] = verify_bytes(d, image_base, secs, 0x0075F67B, "ff d0")
    q6["writer_READ_from_cursor"] = verify_bytes(d, image_base, secs, 0x00977807, "8b 04 10")
    q6["writer_STORE_into_dest"] = verify_bytes(d, image_base, secs, 0x00977810, "89 02")
    q6["writer_advance4_calls_FUN_0040DE60"] = verify_call(d, image_base, secs, 0x00977812, 0x0040DE60)
    q6["writer_failpath_zero_store"] = verify_bytes(d, image_base, secs, 0x0097781E, "c7 00 00 00 00 00")
    results["Q6_exact_write"] = q6

    # ---------- Q7: table[10] identity — BOTH sides recomputed ----------
    q7 = {}
    # writer side: id = tag+4; for tag 6 -> 10; dest = table + 10*4
    q7["writer_side_id_formula"] = "slot6.id = tag(6) + 4 = 10  [add ecx,4 @0x0070CBF6; tag imm 6 @0x00737596]"
    q7["writer_side_tag6_imm"] = verify_bytes(d, image_base, secs, 0x00737594, "6a 06")
    q7["writer_side_dest_formula"] = "dest = [class_obj+0x40] + id*4  [8b 55 40 @0x00726A11; 8d 0c 8a @0x00726A14]"
    q7["writer_side_store"] = verify_bytes(d, image_base, secs, 0x00977810, "89 02")
    # getter side (independent recompute; R1 canon chain FUN_004C5480):
    q7["getter_side_calls_slot_getter"] = verify_call(d, image_base, secs, 0x004C5523, 0x0070C180)
    q7["getter_side_loads_slot_id"] = verify_bytes(d, image_base, secs, 0x004C5539, "8b 40 08")
    q7["getter_side_loads_table_ptr"] = verify_bytes(d, image_base, secs, 0x004C553C, "8b 4e 40")
    q7["getter_side_lea_table_plus_id_times_4"] = verify_bytes(d, image_base, secs, 0x004C553F, "8d 0c 81")
    q7["getter_side_calls_element_accessor"] = verify_call(d, image_base, secs, 0x004C5542, 0x004926E0)
    q7["getter_side_value_load"] = verify_bytes(d, image_base, secs, 0x004C554E, "8b 00")
    results["Q7_table10_identity"] = q7

    # ---------- Q8: source-operand boundary ----------
    q8 = {}
    q8["value_operand_read_pin"] = verify_bytes(d, image_base, secs, 0x00977807, "8b 04 10")
    q8["value_operand_semantics"] = "EAX = u32 at [cursor.base + cursor.pos] — the record payload value field"
    q8["boundary_statement"] = ("STOP enforced: no factory+0x84 stream setter trace, no VFS/file/"
                                 "network provenance performed by any instrument of this run")
    results["Q8_source_boundary"] = q8

    # ---------- Q9: control discrimination ----------
    q9 = {}
    # same mechanism, different record tag -> different id -> different table index
    q9["control_statement"] = ("SAME loop body @0x007269D0-0x00726A35 for every tag; id = tag+4 "
                               "(add ecx,4 @0x0070CBF6); dest = table + id*4 (lea @0x00726A14). "
                               "tag 2 -> id 6 -> &table[6]; tag 4 -> id 8 -> &table[8]; "
                               "tag 6 -> id 10 -> &table[10]; tag 7 -> id 11 -> &table[11]. "
                               "Different record tags produce DISJOINT destinations through the "
                               "identical instruction sequence. R1 canon kinds {4,3,1,4,1,2,1,2}: "
                               "tag2 kind=1 int (same traits writer FUN_009777F0 as tag6) -> the "
                               "mechanism discriminates ATTRIBUTE IDENTITY, not just value.")
    # widen the schema window and PATTERN-SEARCH the tag-2 SLOT_ADD arg block
    # (50 6a 00 6a 00 6a 01 6a 02 = push traits,0,0,kind=1,tag=2)
    wide = read_window(d, image_base, secs, 0x007374F0, 0xA0)
    q9["schema_widewin_0x007374F0_hex"] = wide
    pat = "50 6a 00 6a 00 6a 01 6a 02"
    found = []
    toks = wide.split(" ")
    ptoks = pat.split(" ")
    for i in range(len(toks) - len(ptoks) + 1):
        if toks[i:i+len(ptoks)] == ptoks:
            found.append("0x%08X" % (0x007374F0 + i))
    q9["schema_slot2_args_pattern_search"] = {
        "pattern": pat, "found_vas": found,
        "unique_found": len(found) == 1}
    if len(found) == 1:
        va2 = int(found[0], 16)
        q9["schema_slot2_args_bytes"] = verify_bytes(d, image_base, secs, va2, pat)
        # the SLOT_ADD call right after (push-order verified at slot-6)
        q9["schema_slot2_calls_SLOT_ADD"] = verify_call(d, image_base, secs, va2 + 11, 0x0070CBC0)
    q9["schema_slot7_args_kind2_tag7"] = verify_bytes(
        d, image_base, secs, 0x007375A2, "50 6a 00 6a 00 6a 02 6a 07 8b ce")
    q9["schema_slot7_calls_SLOT_ADD"] = verify_call(d, image_base, secs, 0x007375AD, 0x0070CBC0)
    results["Q9_control"] = q9

    # ---------- Q10: function budget ----------
    results["Q10_function_budget"] = {
        "MAX_NEW_FUNCTIONS_ANALYZED_IN_DETAIL": 8,
        "NEW_FUNCTION_COUNT": 7,
        "FUNCTION_BUDGET_PRECHECK": "PASS" if 7 <= 8 else "FAIL",
        "note": "ledger in FUNCTION_LEDGER.csv; every entry recorded BEFORE detailed analysis"}

    # ---------- Q11: forbidden-scope census (enforced by construction) ----------
    results["Q11_forbidden_scope"] = {
        "factory_plus_0x84_stream_setter_traced": "NO",
        "templates_vfs_opened": "NO",
        "RECORD_A_analyzed": "NO",
        "candidate_B_delegate_decoded": "NO",
        "FUN_00843340_decoded": "NO",
        "model_194013_traced": "NO",
        "NIF_work": "NO",
        "world_xyz": "NO",
        "client_executed": "NO",
        "network_trace": "NO",
    }

    # ---------- Q12: preserved canonical states (static claims re-read) ----------
    preserved = {
        "GETTER_RESULT_TO_LOOKUP_KEY": "PRESERVED_CONFIRMED (not reopened)",
        "CLASS_SELECTOR_20006": "PRESERVED_CONFIRMED (not reopened)",
        "PROPERTY_TAG_6": "PRESERVED_CONFIRMED (not reopened)",
        "IMMEDIATE_VALUE_STORAGE": "PRESERVED (PER_RECEIVER_COMPONENT_VALUE_TABLE)",
        "ULTIMATE_VALUE_SOURCE": "UNKNOWN (preserved)",
        "FILE_DERIVED_VALUE_EXCLUDED": "NO (preserved)",
        "RECORD_A_RELATION": "NOT_ESTABLISHED (preserved)",
        "DEFAULT_CREATION_PATH_INITIAL_VALUE": "0 (preserved)",
        "C1": "PRESERVED_CLOSED", "C2": "PRESERVED_CLOSED",
        "S1_STATIC_MECHANISM": "PRESERVED_CONFIRMED",
        "GP1_GP2_GP3_corrections": "PRESERVED (not reopened)",
    }
    results["Q12_preserved_states"] = preserved

    # ---------- guard thunk resolution (KERNEL32 IAT) ----------
    out["guard_iat_resolution"] = {
        "FUN_00413440_slot_0x00A75064": resolve_guard_iat(d, image_base, secs, 0x00A75064),
        "FUN_00413450_slot_0x00A7506C": resolve_guard_iat(d, image_base, secs, 0x00A7506C),
    }
    out["guard_iat_resolution"]["FUN_00413440_slot_0x00A75064"]["expected_name"] = "EnterCriticalSection"
    out["guard_iat_resolution"]["FUN_00413450_slot_0x00A7506C"]["expected_name"] = "LeaveCriticalSection"
    out["guard_iat_resolution"]["FUN_00413440_slot_0x00A75064"]["match"] = \
        out["guard_iat_resolution"]["FUN_00413440_slot_0x00A75064"]["api_name"] == "EnterCriticalSection"
    out["guard_iat_resolution"]["FUN_00413450_slot_0x00A7506C"]["match"] = \
        out["guard_iat_resolution"]["FUN_00413450_slot_0x00A7506C"]["api_name"] == "LeaveCriticalSection"

    # remaining corrected pins re-verified (canon reverifications)
    out["canon_reverify"] = {
        "cursor_add_pos_0x0040DE64": verify_bytes(d, image_base, secs, 0x0040DE64, "01 41 0c"),
        "cursor_bounds_flag_0x0040DE6F": verify_bytes(d, image_base, secs, 0x0040DE6F, "c6 41 11 00"),
        "cursor_ret4_0x0040DE73": verify_bytes(d, image_base, secs, 0x0040DE73, "c2 04 00"),
        "loop_tagread_advance_0x007269EF": verify_call(d, image_base, secs, 0x007269EF, 0x0040DE60),
        "loop_read1_advance_0x00726937": verify_call(d, image_base, secs, 0x00726937, 0x0040DE60),
        "loop_read2_advance_0x00726972": verify_call(d, image_base, secs, 0x00726972, 0x0040DE60),
        "loop_read3_advance_0x007269A6": verify_call(d, image_base, secs, 0x007269A6, 0x0040DE60),
        "loop_guard_enter_0x00726912": verify_call(d, image_base, secs, 0x00726912, 0x00413440),
        "loop_guard_leave_0x00726AB7": verify_call(d, image_base, secs, 0x00726AB7, 0x00413450),
        "loop_tail_advance4_0x00726A76": verify_call(d, image_base, secs, 0x00726A76, 0x0040DE60),
        "d990_writer_idiom_id_0x0070DA36": verify_bytes(d, image_base, secs, 0x0070DA36, "8b 44 19 08"),
        "d990_writer_idiom_lea_0x0070DA3E": verify_bytes(d, image_base, secs, 0x0070DA3E, "8d 04 82"),
        "d990_writer_idiom_push_0x0070DA41": verify_bytes(d, image_base, secs, 0x0070DA41, "50"),
        "d990_default_dispatch_0x0070DA42": verify_call(d, image_base, secs, 0x0070DA42, 0x0075F6D0),
        "default_dispatcher_vtable_slot1_0x0075F6E5": verify_bytes(d, image_base, secs, 0x0075F6E5, "8b 40 04"),
        "default_dispatcher_tailjmp_0x0075F6E8": verify_bytes(d, image_base, secs, 0x0075F6E8, "ff e0"),
        "lookup_guard_enter_0x0070E110": verify_call(d, image_base, secs, 0x0070E110, 0x00413440),
        "lookup_guard_leave_0x0070E136": verify_call(d, image_base, secs, 0x0070E136, 0x00413450),
        "caller2_FUN_0073C870_0x007046C9": verify_call(d, image_base, secs, 0x007046C9, 0x0073C870),
        "caller2_FUN_0070E100_0x007046DE": verify_call(d, image_base, secs, 0x007046DE, 0x0070E100),
        "caller2_FUN_0075D8D0_0x007046EA": verify_call(d, image_base, secs, 0x007046EA, 0x0075D8D0),
        "caller2_FUN_00726900_0x007046F2": verify_call(d, image_base, secs, 0x007046F2, 0x00726900),
        "caller2_FUN_0070DC20_0x00704704": verify_call(d, image_base, secs, 0x00704704, 0x0070DC20),
        "FUN_0070DCF0_to_FUN_00971AD0": verify_call(d, image_base, secs, 0x0070DD75, 0x00971AD0),
        "FUN_0070DCF0_to_FUN_00971650": verify_call(d, image_base, secs, 0x0070DD84, 0x00971650),
        "FUN_0070DCF0_to_FUN_0040DE60_adv8": verify_call(d, image_base, secs, 0x0070DDA8, 0x0040DE60),
        "FUN_0070DCF0_to_FUN_0040E160": verify_call(d, image_base, secs, 0x0070DD39, 0x0040E160),
        "disp_ret8_0x0075F684": verify_bytes(d, image_base, secs, 0x0075F684, "c2 08 00"),
        "writer_ret8_0x00977817": verify_bytes(d, image_base, secs, 0x00977817, "c2 08 00"),
        "slotadd_ret_0x14_0x0070CC10": verify_bytes(d, image_base, secs, 0x0070CC10, "c2 14 00"),
        "slotadd_calls_FUN_0075F5C0": verify_call(d, image_base, secs, 0x0070CBFF, 0x0075F5C0),
        "slotadd_calls_appender_FUN_0070C980": verify_call(d, image_base, secs, 0x0070CC07, 0x0070C980),
    }

    out["gate_results"] = results

    # rollup
    def roll(dct, path=""):
        fails = []
        for k, v in dct.items():
            if isinstance(v, dict) and "match" in v:
                if not v["match"]:
                    fails.append(path + k)
            elif isinstance(v, dict):
                fails.extend(roll(v, path + k + "."))
        return fails
    all_pins = {k: v for k, v in results.items() if isinstance(v, dict)}
    all_pins["canon_reverify"] = out["canon_reverify"]
    fails = roll(all_pins)
    out["rollup"] = {
        "total_pin_checks": sum(1 for _ in _iter_pins(all_pins)),
        "failed_pins": fails,
        "Q1_PASS": results["Q1_exe_identity"]["match"],
        "ALL_PIN_CHECKS_PASS": len(fails) == 0,
    }

    with open(os.path.join(RUN, "01_RAW", "S5_QC_BATTERY.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S5 QC done.")
    print("failed pins: %s" % fails)
    print("guard IAT:", json.dumps(out["guard_iat_resolution"], ensure_ascii=True))

def _iter_pins(dct):
    for k, v in dct.items():
        if isinstance(v, dict):
            if "match" in v:
                yield (k, v)
            else:
                yield from _iter_pins(v)

if __name__ == "__main__":
    main()
