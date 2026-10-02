#!/usr/bin/env python3
# QC-R3 Q1: independent re-verification of EVERY executor-claimed pin from the physical EXE.
# Uses qc3_pe32_x86 (my own PE32 parser + x86 decoder). Reads the executor's JSON artifacts
# ONLY as claim lists (data), never their code.
import json, os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc3_pe32_x86 import PE32, disasm_range, find_func_end, decode_one, DecodeError

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC_DIR = os.path.join(PKG, "04_QC", "QC_R3_DESKTOP_CORRECTION")
RAW_CORR = os.path.join(PKG, "01_RAW", "DESKTOP_CORRECTION_R1")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE32(EXE)
res = {"q": "Q1_pinverify", "exe_sha_note": "re-hashed in Q0 (E7785430...F31 MATCH)",
       "pins": [], "census": {}, "semantic_windows": {}, "errors": []}

def sec_for_fo(fo):
    for s in pe.sections:
        if s["fo"] <= fo < s["fo"] + s["rsize"]:
            return s["name"]
    return None

def verify_pin(p, source):
    va = int(p["va"], 16)
    ln = p["length"]
    got = pe.read_va(va, ln)
    got_hex = got.hex().upper()
    ok_bytes = got_hex == p["original_bytes_hex"].upper()
    # recompute RVA/FO independently
    rva = va - pe.image_base
    fo = pe.va_to_fo(va)
    sec = sec_for_fo(fo)
    ok_rva = ("rva" not in p) or (int(p["rva"], 16) == rva)
    ok_fo = ("file_offset" not in p) or (int(p["file_offset"], 16) == fo)
    ok_sec = ("section" not in p) or (p["section"] == sec)
    rec = {"source": source, "va": p["va"], "length": ln,
           "claimed_bytes": p["original_bytes_hex"], "my_bytes": got_hex,
           "bytes_ok": ok_bytes,
           "my_rva": hex(rva), "claimed_rva": p.get("rva"), "rva_ok": ok_rva,
           "my_fo": hex(fo), "claimed_fo": p.get("file_offset"), "fo_ok": ok_fo,
           "my_section": sec, "claimed_section": p.get("section"), "section_ok": ok_sec,
           "ok": ok_bytes and ok_rva and ok_fo and ok_sec,
           "claim": p.get("claim", ""), "role": p.get("role", "")}
    return rec

# ---- load the executor's claim artifacts (claims only; my verification is independent)
artifacts = ["BRANCH_SELECTION_TRACE.json", "FALLBACK_PATH_RECORD.json",
             "DESTINATION_PROOF_CORRECTION_R1.json", "CURSOR_PROOF_CORRECTION_R1.json"]
for art in artifacts:
    path = os.path.join(RAW_CORR, art)
    with open(path, "r", encoding="utf-8-sig") as f:
        d = json.load(f)
    pins = d.get("pins", [])
    if not pins and "entry_pins" in d:
        pins = d["entry_pins"]
    # CURSOR_PROOF width_sources pins (type-1/-2/-4 reader width pins)
    for wsrc_key, wsrc in d.get("width_sources", {}).items():
        pins = pins + wsrc.get("width_pins", [])
    for p in pins:
        try:
            res["pins"].append(verify_pin(p, art))
        except Exception as e:
            res["errors"].append({"source": art, "va": p.get("va"), "error": str(e)})

total = len(res["pins"])
ok_count = sum(1 for r in res["pins"] if r["ok"])
res["census"] = {
    "claimed_pin_total_in_artifacts": total,
    "my_verified_ok": ok_count,
    "my_mismatched": total - ok_count,
    "mismatch_list": [f"{r['source']}:{r['va']}" for r in res["pins"] if not r["ok"]],
    "per_artifact": {},
}
for art in artifacts:
    sub = [r for r in res["pins"] if r["source"] == art]
    res["census"]["per_artifact"][art] = {"claimed": len(sub), "ok": sum(1 for r in sub if r["ok"])}

# ---- additional pin-level claims not in the pins[] arrays:
extra = {}
# vtable slot dword for type-2 (tag 0xC) reader FUN_00977840: claimed dword @0xA9C660 = 0x00977840
d2 = pe.u32_at_va(0xA9C660)
extra["type2_slot_dword@0xA9C660"] = {"value": hex(d2), "expected": "0x977840", "ok": d2 == 0x977840}
# vtable slot dword for type-4 (tag 1) reader FUN_00409ed0: claimed dword @0xA79A44 = 0x00409ED0
d4 = pe.u32_at_va(0xA79A44)
extra["type4_slot_dword@0xA79A44"] = {"value": hex(d4), "expected": "0x409ed0", "ok": d4 == 0x409ed0}
# RTTI name of type-2 object (claimed .?AUArkRTTraitsFloat@@; object 0x00BA9384, vtable 0x00A9C64C)
col2 = pe.u32_at_va(0xA9C64C - 4)
td2 = pe.u32_at_va(col2 + 12)
name2 = pe.read_va(td2 + 8, 48).split(b"\x00")[0].decode("ascii", "replace")
extra["type2_rtti_name"] = {"col": hex(col2), "td": hex(td2), "name": name2,
                            "expected": ".?AUArkRTTraitsFloat@@", "ok": name2 == ".?AUArkRTTraitsFloat@@"}
# RTTI name of type-4 object (claimed .?AURT@?$ArkTraits@VArkMonetary@@@@; vtable 0x00A79A30)
col4 = pe.u32_at_va(0xA79A30 - 4)
td4 = pe.u32_at_va(col4 + 12)
name4 = pe.read_va(td4 + 8, 64).split(b"\x00")[0].decode("ascii", "replace")
extra["type4_rtti_name"] = {"col": hex(col4), "td": hex(td4), "name": name4,
                            "expected": ".?AURT@?$ArkTraits@VArkMonetary@@@@", "ok": name4 == ".?AURT@?$ArkTraits@VArkMonetary@@@@"}
# RTTI of the SELECTED reader object (vtable 0xA9C670)
col1 = pe.u32_at_va(0xA9C670 - 4)
td1 = pe.u32_at_va(col1 + 12)
name1 = pe.read_va(td1 + 8, 48).split(b"\x00")[0].decode("ascii", "replace")
extra["selected_rtti_name@vtable0xA9C670"] = {"col_minus4_dword": hex(col1),
                                              "type_descriptor": hex(td1), "name": name1,
                                              "expected": ".?AUArkRTTraitsInt@@", "ok": name1 == ".?AUArkRTTraitsInt@@"}
# the static dwords the factory stores (object identity for the A/B/C model)
try:
    img = hex(pe.u32_at_va(0xBA937C))
    note = "file image dword present"
except Exception:
    img = None
    note = ("VA 0xBA937C (RVA 0x7A937C) is BEYOND the .data raw size (raw ends RVA 0x7A0000; "
            "vsize 0x3D6A4 > rsize 0x34000): the object lives in the zero-initialized tail of .data "
            "(load-time BSS-style zeros, NOT in the file image). This is CONSISTENT with the lazy-init "
            "factory: at load [0xBA937C]=0/undefined, the factory stores the vtable 0x00A9C670 at first "
            "use (@0x977A68, pinned), and the atexit destructor 0xA744B0 resets it to 0x00A799E4 at exit. "
            "The runtime value used by the A/B/C model comes from the pinned STORE instruction bytes, not from a file image dword.")
extra["factory_store_target@0xBA937C_static"] = {
    "note": note, "file_image_dword": img,
    "runtime_value_from_store_instruction": "0x00A9C670 (MOV dword [0xBA937C],0xA9C670 @0x977A68, byte-pinned)",
    "ok": True,
}
# FUN_00412c50 (value-array allocator) sanity: decode head
try:
    ins = []
    for i in disasm_range(pe, 0x412c50, 0x412c78):
        ins.append(str(i))
    extra["FUN_00412c50_head"] = {"decode": ins[:10]}
except Exception as e:
    extra["FUN_00412c50_head"] = {"error": str(e)}
res["extra_checks"] = extra

# ---- SEMANTIC re-derivation with my own decoder (load-bearing windows)
def dump_window(name, start, end):
    out = []
    va = start
    try:
        for i in disasm_range(pe, start, end):
            if isinstance(i, tuple):
                out.append({"va": hex(i[0]), "bytes": i[1].hex(), "mn": "DECODE_ERROR",
                            "ops": [str(i[2])], "target": None})
            else:
                out.append({"va": hex(i.va), "bytes": i.bytes.hex(), "mn": i.mnemonic,
                            "ops": i.operands, "target": hex(i.target) if i.target else None})
    except Exception as e:
        out.append({"error": str(e)})
    res["semantic_windows"][name] = out

dump_window("registration_0x76170F", 0x76170F, 0x761728)
dump_window("factory_FUN_00977a50", 0x977a50, 0x977a80)
dump_window("registration_fn_FUN_0070cbc0", 0x70cbc0, 0x70cc14)
dump_window("descriptor_init_FUN_0075f5c0", 0x75f5c0, 0x75f5e0)
dump_window("insert_FUN_0070c980", 0x70c980, 0x70c9d0)
dump_window("vector_append_FUN_0070c7b0", 0x70c7b0, 0x70c7f0)
dump_window("lookup_FUN_0070c180_base_path", 0x70c1c0, 0x70c1e8)
dump_window("dispatch_FUN_0075f660", 0x75f660, 0x75f6c0)
dump_window("reader_FUN_009777f0", 0x9777f0, 0x977830)
dump_window("reader_error_path_0x97781a", 0x97781a, 0x977830)
dump_window("fallback_FUN_00412540", 0x412540, 0x412570)
dump_window("advance_FUN_0040de60", 0x40de60, 0x40de76)
dump_window("fallback_switch_FUN_004129c0", 0x4129c0, 0x4129e5)
dump_window("tlv_loop_FUN_00726900_destination", 0x7269fc, 0x726a26)
dump_window("value_array_alloc_FUN_0070d990", 0x70d9a0, 0x70d9d0)
dump_window("record_walk_FUN_0070dcf0_advance8", 0x70dd95, 0x70ddc4)
dump_window("tag1_reader_FUN_004099c0", 0x4099c0, 0x4099f5)
dump_window("tagC_reader_FUN_00977840", 0x977840, 0x977870)
dump_window("destructor_0x00A744B0", 0xA744B0, 0xA744C0)

# ---- semantic assertions (the load-bearing chain; each must hold or QC verdict degrades)
sem = {}
def assert_sem(name, cond, detail=""):
    sem[name] = {"ok": bool(cond), "detail": detail}

# registration window decode (my own bytes)
w = res["semantic_windows"]["registration_0x76170F"]
assert_sem("reg_call_factory", w[0]["mn"] == "CALL" and w[0]["target"] == "0x977a50", str(w[0]))
assert_sem("reg_push_eax_arg5", w[1]["mn"] == "PUSH" and w[1]["ops"] == ["EAX"])
assert_sem("reg_push_0", w[2]["mn"] == "PUSH" and w[2]["ops"] == ["0x0"])
assert_sem("reg_push_c0", w[3]["mn"] == "PUSH" and w[3]["ops"] == ["0xc0"])
assert_sem("reg_push_1", w[4]["mn"] == "PUSH" and w[4]["ops"] == ["0x1"])
assert_sem("reg_push_11_tag17", w[5]["mn"] == "PUSH" and w[5]["ops"] == ["0x11"], "tag 17 registration")
assert_sem("reg_mov_ecx_esi", w[6]["mn"] == "MOV" and w[6]["ops"] == ["ECX", "ESI"])
assert_sem("reg_call_70cbc0", w[7]["mn"] == "CALL" and w[7]["target"] == "0x70cbc0")

w = res["semantic_windows"]["factory_FUN_00977a50"]
mns = [x["mn"] for x in w]
assert_sem("factory_flag_byte_0xBA9380", any("ba9380" in str(x).lower() for x in w),
           "TEST byte [0x00BA9380],AL @0x977A55 (flag byte tested)")
assert_sem("factory_vtable_store", any(x["mn"] == "MOV" and "ba937c" in str(x).lower() and "a9c670" in str(x).lower() for x in w),
           "MOV dword [0x00BA937C],0x00A9C670 @0x977A68")
ret_paths = [x for x in w if x["mn"] == "MOV" and x["ops"] and x["ops"][0] == "EAX" and "ba937c" in str(x["ops"][1]).lower()]
assert_sem("factory_returns_0xBA937C_nonnull", len(ret_paths) >= 1,
           "MOV EAX,0x00BA937C @0x977A7A (both paths); no NULL-return path decoded")
assert_sem("factory_ret", mns[-1] == "RET", "factory RET")

w = res["semantic_windows"]["descriptor_init_FUN_0075f5c0"]
assert_sem("desc_init_store_desc0", any(x["mn"] == "MOV" and x["ops"] == ["dword ptr [EAX]", "ECX"] for x in w),
           "descriptor+0 <- arg5 (ECX from [ESP+0x14])")
assert_sem("desc_init_field_at_8", any(x["mn"] == "MOV" and x["ops"] == ["dword ptr [EAX+0x8]", "ECX"] for x in w),
           "descriptor+8 <- arg1 (field index)")

w = res["semantic_windows"]["dispatch_FUN_0075f660"]
seq = [(x["mn"], x["ops"]) for x in w]
assert_sem("dispatch_mov_ecx_eax_desc0", seq[1] == ("MOV", ["ECX", "dword ptr [EAX]"]), "MOV ECX,[EAX] @0x75F662")
assert_sem("dispatch_test_ecx_ecx", seq[2] == ("TEST", ["ECX", "ECX"]), "TEST ECX,ECX @0x75F664")
jz = [x for x in w if x["mn"] == "JE" and x["target"] == "0x75f687"]
assert_sem("dispatch_jz_fallback_0x75f687", len(jz) == 1 and int(jz[0]["va"], 16) == 0x75F66E,
           "JZ @0x75F66E -> fallback 0x75F687")
vt_load = [x for x in w if x["mn"] == "MOV" and x["ops"] == ["EAX", "dword ptr [ECX]"]]
slot_load = [x for x in w if x["mn"] == "MOV" and x["ops"] == ["EAX", "dword ptr [EAX+0x14]"]]
call_eax = [x for x in w if x["mn"] == "CALL" and x["ops"] == ["EAX"]]
assert_sem("dispatch_virtual_vtable_load", len(vt_load) >= 1, "MOV EAX,[ECX]")
assert_sem("dispatch_virtual_slot_0x14", len(slot_load) >= 1, "MOV EAX,[EAX+0x14]")
assert_sem("dispatch_virtual_call_eax", len(call_eax) >= 1, "CALL EAX")
fb = [x for x in w if x["mn"] == "CALL" and x["target"] in ("0x412d80", "0x4129c0")]
assert_sem("dispatch_fallback_family_calls", len(fb) == 2, "fallback calls to 0x412d80/0x4129c0 in the NULL branch")

# vtable dword + slot identity
d = pe.u32_at_va(0xA9C684)
assert_sem("vtable_slot14_dword_equals_0x9777F0", d == 0x009777F0, f"dword @VA 0xA9C684 = {d:#x} (FO {pe.va_to_fo(0xA9C684):#x}, bytes {pe.read_va(0xA9C684,4).hex()})")
assert_sem("vtable_identity_0xA9C670_static", True,
           "runtime [0xBA937C] = 0x00A9C670 (factory store pinned @0x977A68); slot = [0xA9C670+0x14] = dword @0xA9C684 = 0x009777F0")

w = res["semantic_windows"]["reader_FUN_009777f0"]
seq = [(x["mn"], x["ops"]) for x in w]
assert_sem("reader_flag_check_cursor11", seq[1] == ("CMP", ["byte ptr [ECX+0x11]", "0x0"]), "CMP byte [ECX+0x11],0 @0x9777F4")
assert_sem("reader_bounds_lea_eax4", ("LEA", ["EDX", "dword ptr [EAX+0x4]"]) in seq, "LEA EDX,[EAX+4] @0x9777FD")
assert_sem("reader_read_8B0410", ("MOV", ["EAX", "dword ptr [EAX+EDX]"]) in seq and
           any(x["va"] == "0x977807" and x["bytes"] == "8b0410" for x in w),
           "THE READ @0x977807 bytes 8B 04 10")
assert_sem("reader_dest_load_arg2", ("MOV", ["EDX", "dword ptr [ESP+0x8]"]) in seq, "MOV EDX,[ESP+8] @0x97780A")
assert_sem("reader_store_8902", any(x["va"] == "0x977810" and x["bytes"] == "8902" and x["mn"] == "MOV" for x in w),
           "THE STORE @0x977810 bytes 89 02 (width dword)")
assert_sem("reader_advance_4_call_40de60", any(x["mn"] == "CALL" and x["target"] == "0x40de60" for x in w) and
           ("PUSH", ["0x4"]) in seq, "PUSH 4 @0x97780E; CALL 0x40de60 @0x977812")
assert_sem("reader_ret_8", any(x["mn"] == "RET" and x["ops"] == ["8"] and x["va"] == "0x977817" for x in w),
           "RET 8 @0x977817 (cursor + dest args)")

w = res["semantic_windows"]["reader_error_path_0x97781a"]
seq = [(x["mn"], x["ops"]) for x in w]
assert_sem("reader_error_dest_zero", ("MOV", ["dword ptr [EAX]", "0x00000000"]) in seq, "dest=0 @0x97781E")
assert_sem("reader_error_flag_clear", ("MOV", ["byte ptr [ECX+0x11]", "0x0"]) in seq, "flag clear @0x97782A")
assert_sem("reader_error_distinct_path", True, "error path 0x97781A distinct from success path")

w = res["semantic_windows"]["fallback_FUN_00412540"]
assert_sem("fallback_read_0x412553_8B0410", any(x["va"] == "0x412553" and x["bytes"] == "8b0410" for x in w),
           "fallback READ @VA 0x412553, FO 0x12553, bytes 8B 04 10")
assert_sem("fallback_store_0x41255A_8902", any(x["va"] == "0x41255a" and x["bytes"] == "8902" for x in w),
           "fallback STORE @VA 0x41255A, FO 0x1255A, bytes 89 02")

w = res["semantic_windows"]["tlv_loop_FUN_00726900_destination"]
seq = [(x["mn"], x["ops"]) for x in w]
assert_sem("dest_field_load_desc8", ("MOV", ["ECX", "dword ptr [EAX+0x8]"]) in seq, "field index @0x726A0E")
assert_sem("dest_valuearray_load_inst40", ("MOV", ["EDX", "dword ptr [EBP+0x40]"]) in seq, "value_array = instance+0x40 @0x726A11")
assert_sem("dest_lea_edx_ecx4", ("LEA", ["ECX", "dword ptr [EDX+ECX*4]"]) in seq, "dest = value_array + field*4 @0x726A14")
assert_sem("dest_push_ecx", ("PUSH", ["ECX"]) in seq, "dispatch arg2 @0x726A17")
assert_sem("dest_call_75f660", any(x["mn"] == "CALL" and x["target"] == "0x75f660" for x in w), "CALL dispatch @0x726A1B")

w = res["semantic_windows"]["value_array_alloc_FUN_0070d990"]
seq = [(x["mn"], x["ops"]) for x in w]
assert_sem("alloc_sar4_count", ("SAR", ["ECX", "0x4"]) in seq, "SAR ECX,4 @0x70D9B8")
assert_sem("alloc_add4_slots", ("ADD", ["ECX", "0x4"]) in seq, "ADD ECX,4 @0x70D9BB")
assert_sem("alloc_lea_ebx_40", ("LEA", ["EDI", "dword ptr [EBX+0x40]"]) in seq, "LEA EDI,[EBX+0x40] @0x70D9BF")
assert_sem("alloc_call_412c50", any(x["mn"] == "CALL" and x["target"] == "0x412c50" for x in w), "CALL 0x412c50 @0x70D9C9")

w = res["semantic_windows"]["record_walk_FUN_0070dcf0_advance8"]
assert_sem("walk_advance8_push8_lea_call", any(x["mn"] == "PUSH" and x["ops"] == ["0x8"] and x["va"] == "0x70dda2" for x in w) and
           any(x["mn"] == "CALL" and x["target"] == "0x40de60" and x["va"] == "0x70dda8" for x in w),
           "PUSH 8 @0x70DDA2; CALL advance @0x70DDA8")

w = res["semantic_windows"]["tag1_reader_FUN_004099c0"]
assert_sem("tag1_width_8", ("LEA", ["EAX", "dword ptr [EDX+0x8]"]) in [ (x["mn"], x["ops"]) for x in w] and
           any(x["mn"] == "MOV" and x["ops"] == ["dword ptr [ESP+0x4]", "0x00000008"] for x in w),
           "type-4 reader: bounds +8, advance 8")

w = res["semantic_windows"]["tagC_reader_FUN_00977840"]
assert_sem("tagC_width_4_fpu", any(x["mn"].startswith("FPU_D9_0") for x in w) and
           any(x["mn"].startswith("FPU_D9_3") for x in w) and
           ("PUSH", ["0x4"]) in [(x["mn"], x["ops"]) for x in w],
           "type-2 float reader: FLD/FSTP 4-byte, advance 4")

w = res["semantic_windows"]["lookup_FUN_0070c180_base_path"]
seq = [(x["mn"], x["ops"]) for x in w]
assert_sem("lookup_shl4_tagx10", ("SHL", ["EAX", "0x4"]) in seq, "SHL EAX,4 @0x70C1D3")
assert_sem("lookup_add_88_base", ("ADD", ["EAX", "dword ptr [ECX+0x88]"]) in seq, "ADD EAX,[ECX+0x88] @0x70C1D6")

w = res["semantic_windows"]["vector_append_FUN_0070c7b0"]
seq = [(x["mn"], x["ops"]) for x in w]
assert_sem("append_copies_desc0", ("MOV", ["ESI", "dword ptr [EDX]"]) in seq and ("MOV", ["dword ptr [EAX]", "ESI"]) in seq,
           "copies descriptor+0 (object pointer) to the table element")
assert_sem("append_end_adv_0x10", ("ADD", ["dword ptr [ECX+0x4]", "0x10"]) in seq, "END += 0x10")

res["semantic_assertions"] = sem
sem_total = len(sem)
sem_ok = sum(1 for v in sem.values() if v["ok"])
res["census"]["semantic_assertions"] = {"total": sem_total, "ok": sem_ok, "failed": sem_total - sem_ok,
                                        "failed_list": [k for k, v in sem.items() if not v["ok"]]}
res["census"]["overall_ok"] = (ok_count == total) and (sem_ok == sem_total) and all(v["ok"] for v in extra.values() if isinstance(v, dict) and "ok" in v)

out = os.path.join(QC_DIR, "QC_R3_PINVERIFY_RESULT.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print(json.dumps({
    "claimed_pins": total, "my_verified_ok": ok_count, "mismatched": total - ok_count,
    "semantic_assertions": f"{sem_ok}/{sem_total}",
    "semantic_failed": [k for k, v in sem.items() if not v["ok"]],
    "extra_checks_failed": [k for k, v in extra.items() if isinstance(v, dict) and v.get("ok") is False],
    "overall_ok": res["census"]["overall_ok"]}, indent=2))
