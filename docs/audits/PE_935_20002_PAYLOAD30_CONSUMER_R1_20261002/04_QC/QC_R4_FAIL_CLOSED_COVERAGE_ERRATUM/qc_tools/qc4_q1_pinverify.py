#!/usr/bin/env python3
# QC-R4 Q1: FAIL-CLOSED repair of the QC-R3 Q1 pin verifier.
# Source lineage: 04_QC\QC_R3_DESKTOP_CORRECTION\qc_tools\qc3_q1_pinverify.py
#   (SHA256 C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F, 18199 B, 308 lines)
#   copied to qc_tools\qc4_q1_pinverify.py and repaired per RUN_CONTRACT §2 (R1-R12) of
#   PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002.
# The F1 defect being repaired (confirmed fail-open, RUN_CONTRACT §1): verification
# exceptions were appended to res["errors"] WITHOUT a pin result row, the failed pin
# vanished from the denominator (len(res["pins"])), and overall_ok ignored errors and
# the original input-pin count - so a malformed/unmapped pin could silently disappear
# (Desktop counterexample: 185 input pins, 1 bad VA -> claimed denominator 184,
# overall_ok=true, exit 0).
# The ONLY behavioral changes vs qc3_q1_pinverify.py (RUN_CONTRACT R11 enumerates them):
#   R1  ORIGINAL_INPUT_PIN_COUNT captured before verification (census.input_pin_count);
#   R2  every input pin stays represented as a result row (no pin may vanish);
#   R3  a verification exception produces an explicit FAILED row (pin_id + source +
#       original VA string + error retained) that STAYS in the denominator;
#   R4  census.overall_ok requires processed_count == input_pin_count AND
#       verified_ok == input_pin_count AND mismatch_count == 0 AND error_count == 0
#       AND all semantic assertions PASS AND all required extra checks PASS
#       (plus the R8 bijection_ok and the R10 exe-identity / run-error conditions);
#   R5  process exit code 0 iff overall_ok true, else nonzero (1);
#   R8  stable pin_id "<artifact-name>::<array_path>[<index>]" over pins[] /
#       entry_pins[] / width_sources.<key>.width_pins[], preserved even when the VA is
#       malformed; identity-set bijection input pins <-> result rows (no dups, no drops);
#   R9  explicit --inputs / --output CLI paths (directory of the four canonical artifact
#       names, or the four explicit file paths); NO hard-coded QC-R3 output path;
#   R10 fail-closed at every level: pinned-EXE identity hash checked at start
#       (expected E7785430...F31); missing input file / unparsable JSON -> run-level
#       error + overall_ok=false + nonzero exit; a pin without a parseable "va" (or any
#       other per-pin failure) is a FAILED row with the error retained - never skipped;
#   R12 sys.dont_write_bytecode = True as the first statements.
# Everything else is semantically IDENTICAL to qc3_q1_pinverify.py: same four-artifact
# pin loading (pins[] + entry_pins fallback + width_sources width_pins), same
# verify_pin field semantics, same extra checks (incl. the BSS-tail factory note),
# same 19 semantic windows, same 51 semantic assertions.
import sys
sys.dont_write_bytecode = True

import argparse, hashlib, json, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc4_pe32_x86 import PE32, disasm_range, find_func_end, decode_one, DecodeError

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXPECTED_EXE_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
ARTIFACTS = ["BRANCH_SELECTION_TRACE.json", "FALLBACK_PATH_RECORD.json",
             "DESTINATION_PROOF_CORRECTION_R1.json", "CURSOR_PROOF_CORRECTION_R1.json"]

pe = None  # set after the R10 EXE identity check passes


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def parse_args():
    ap = argparse.ArgumentParser(
        description="QC-R4 fail-closed pin verifier (repaired copy of qc3_q1_pinverify.py).")
    ap.add_argument("--inputs", nargs="+", required=True,
                    help="a directory containing the four canonical artifact files, "
                         "OR the four explicit artifact file paths")
    ap.add_argument("--output", required=True,
                    help="path of the result JSON to write")
    return ap.parse_args()


def resolve_inputs(raw):
    """R9: map --inputs to the four artifact paths in canonical order.
    Fail-closed: anything that is not (one directory containing all four canonical
    names) or (exactly the four canonical file paths) raises ValueError."""
    if len(raw) == 1 and os.path.isdir(raw[0]):
        d = raw[0]
        missing = [a for a in ARTIFACTS if not os.path.isfile(os.path.join(d, a))]
        if missing:
            raise ValueError(f"input directory {d!r} missing canonical artifacts: {missing}")
        return [os.path.join(d, a) for a in ARTIFACTS]
    if len(raw) == 4:
        names = [os.path.basename(p) for p in raw]
        if sorted(names) == sorted(ARTIFACTS):
            by_name = {os.path.basename(p): p for p in raw}
            return [by_name[a] for a in ARTIFACTS]
        raise ValueError(f"--inputs file set is not the four canonical artifact names: {names}")
    raise ValueError("--inputs must be one directory or exactly the four artifact file paths")


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


def enumerate_artifact_pins(d, name):
    """R8: enumerate this artifact's pins with stable identities, using the SAME
    loading semantics as qc3_q1_pinverify.py (pins[] with entry_pins fallback, then
    width_sources.<key>.width_pins[]). Returns [(pin_id, pin_dict), ...]."""
    out = []
    pins = d.get("pins", [])
    array_path = "pins"
    if not pins and "entry_pins" in d:
        pins = d["entry_pins"]
        array_path = "entry_pins"
    for idx, p in enumerate(pins):
        out.append((f"{name}::{array_path}[{idx}]", p))
    for wsrc_key, wsrc in d.get("width_sources", {}).items():
        for idx, wp in enumerate(wsrc.get("width_pins", [])):
            out.append((f"{name}::width_sources.{wsrc_key}.width_pins[{idx}]", wp))
    return out


def main():
    global pe
    args = parse_args()
    res = {"q": "Q1_pinverify_QC_R4_fail_closed",
           "run_id": "PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002",
           "inputs": [], "exe_identity": {}, "run_errors": [],
           "pins": [], "errors": [], "census": {},
           "semantic_windows": {}, "semantic_assertions": {}, "extra_checks": {}}

    # ---- R10: pinned-EXE identity check at start (static read only; never executed)
    exe_ok = False
    exe_sha = None
    exe_err = None
    try:
        exe_sha = sha256_file(EXE)
        exe_ok = (exe_sha == EXPECTED_EXE_SHA256)
        if not exe_ok:
            exe_err = f"EXE identity mismatch: expected {EXPECTED_EXE_SHA256}, measured {exe_sha}"
    except Exception as e:
        exe_err = f"{type(e).__name__}: {e}"
    res["exe_identity"] = {"path": EXE, "expected_sha256": EXPECTED_EXE_SHA256,
                           "measured_sha256": exe_sha, "ok": exe_ok, "error": exe_err}
    if exe_ok:
        try:
            pe = PE32(EXE)
        except Exception as e:
            res["run_errors"].append({"stage": "exe_parse",
                                      "error": f"{type(e).__name__}: {e}"})
    else:
        res["run_errors"].append({"stage": "exe_identity", "error": exe_err})

    # ---- R9: resolve explicit input paths
    input_paths = None
    try:
        input_paths = resolve_inputs(args.inputs)
    except Exception as e:
        res["run_errors"].append({"stage": "input_resolution",
                                  "error": f"{type(e).__name__}: {e}"})
    res["inputs"] = input_paths if input_paths else []

    # ---- load artifacts + R1: enumerate ALL input pins BEFORE any verification
    enumerated = []  # [(pin_id, artifact_name, pin_dict), ...]
    if input_paths:
        for path in input_paths:
            name = os.path.basename(path)
            if not os.path.isfile(path):
                res["run_errors"].append({"stage": "artifact_load", "artifact": name,
                                          "error": "missing input file"})
                continue
            try:
                with open(path, "r", encoding="utf-8-sig") as f:
                    d = json.load(f)
            except Exception as e:
                res["run_errors"].append({"stage": "artifact_load", "artifact": name,
                                          "error": f"{type(e).__name__}: {e}"})
                continue
            enumerated.extend((pid, name, p) for (pid, p) in enumerate_artifact_pins(d, name))
    original_input_pin_count = len(enumerated)  # R1

    # ---- verification: R2/R3 - every input pin gets a result row, FAILED rows stay
    rows = res["pins"]
    per_art = {a: {"claimed": 0, "processed": 0, "verified_ok": 0,
                   "failed": 0, "mismatch": 0, "error": 0} for a in ARTIFACTS}
    verified_ok = 0
    mismatch_count = 0
    error_count = 0
    mismatch_list = []
    for (pin_id, art, p) in enumerated:
        per_art[art]["claimed"] += 1
        if pe is None:
            # R10 fail-closed: no verified pinned EXE -> no pin is verified
            va_val = p.get("va") if isinstance(p, dict) else None
            err = "EXE unavailable or identity mismatch: pin verification not performed"
            rec = {"pin_id": pin_id, "source": art, "va": va_val, "status": "FAILED",
                   "ok": False, "error": err}
            rows.append(rec)
            per_art[art]["processed"] += 1
            res["errors"].append({"pin_id": pin_id, "source": art, "va": va_val,
                                   "error": err})
            error_count += 1
            per_art[art]["error"] += 1
            continue
        try:
            rec = verify_pin(p, art)
            rec["pin_id"] = pin_id
            rec["status"] = "VERIFIED_OK" if rec["ok"] else "MISMATCH"
            rows.append(rec)
            per_art[art]["processed"] += 1
            if rec["ok"]:
                verified_ok += 1
                per_art[art]["verified_ok"] += 1
            else:
                mismatch_count += 1
                per_art[art]["mismatch"] += 1
                mismatch_list.append(f"{rec['source']}:{rec['va']}")
        except Exception as e:
            # R3: explicit FAILED row; the pin STAYS in the denominator
            va_val = p.get("va") if isinstance(p, dict) else None
            err = f"{type(e).__name__}: {e}"
            rec = {"pin_id": pin_id, "source": art, "va": va_val, "status": "FAILED",
                   "ok": False, "error": err}
            rows.append(rec)
            per_art[art]["processed"] += 1
            res["errors"].append({"pin_id": pin_id, "source": art, "va": va_val,
                                   "error": err})
            error_count += 1
            per_art[art]["error"] += 1

    processed_count = len(rows)
    denominator = len(rows)  # R2/R3: FAILED rows are IN the denominator
    failed_count = mismatch_count + error_count

    # ---- R8: identity-set bijection input pins <-> result rows (counters are not enough)
    input_ids = [t[0] for t in enumerated]
    row_ids = [r["pin_id"] for r in rows]
    bijection_ok = (len(input_ids) == len(set(input_ids))
                    and len(row_ids) == len(set(row_ids))
                    and len(input_ids) == len(row_ids)
                    and set(input_ids) == set(row_ids))

    # ---- extra pin-level claims not in the pins[] arrays (identical to qc3)
    extra = {}
    if pe is not None:
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

    # ---- SEMANTIC re-derivation with my own decoder (load-bearing windows; identical to qc3)
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

    if pe is not None:
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

    # ---- semantic assertions (the load-bearing chain; identical to qc3)
    sem = {}
    def assert_sem(name, cond, detail=""):
        sem[name] = {"ok": bool(cond), "detail": detail}

    if pe is not None:
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
    extra_required_ok = all(v["ok"] for v in extra.values()
                            if isinstance(v, dict) and "ok" in v)
    extra_required_count = sum(1 for v in extra.values()
                              if isinstance(v, dict) and "ok" in v)
    extra_failed_list = [k for k, v in extra.items()
                         if isinstance(v, dict) and "ok" in v and v["ok"] is False]

    # ---- R4: overall_ok predicate (plus the R8 bijection and R10 identity conditions)
    overall_ok = (
        exe_ok
        and pe is not None
        and not res["run_errors"]
        and processed_count == original_input_pin_count
        and verified_ok == original_input_pin_count
        and mismatch_count == 0
        and error_count == 0
        and bijection_ok
        and sem_ok == sem_total
        and extra_required_ok
    )

    res["census"] = {
        "input_pin_count": original_input_pin_count,          # R1
        "processed_count": processed_count,
        "verified_ok": verified_ok,
        "failed_count": failed_count,
        "mismatch_count": mismatch_count,
        "error_count": error_count,
        "denominator": denominator,                          # R2/R3: FAILED rows included
        "result_row_count": len(rows),
        "bijection_ok": bijection_ok,                        # R8
        "mismatch_list": mismatch_list,
        "per_artifact": per_art,
        "semantic_assertions": {"total": sem_total, "ok": sem_ok,
                                "failed": sem_total - sem_ok,
                                "failed_list": [k for k, v in sem.items() if not v["ok"]]},
        "extra_checks": {"all_required_ok": extra_required_ok,
                         "required_count": extra_required_count,
                         "failed_list": extra_failed_list},
        "overall_ok": overall_ok,                            # R4
    }

    out = args.output
    out_dir = os.path.dirname(os.path.abspath(out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(json.dumps({
        "input_pin_count": original_input_pin_count,
        "processed_count": processed_count,
        "my_verified_ok": verified_ok,
        "failed_count": failed_count,
        "mismatched": mismatch_count,
        "errors": error_count,
        "denominator": denominator,
        "result_row_count": len(rows),
        "bijection_ok": bijection_ok,
        "semantic_assertions": f"{sem_ok}/{sem_total}",
        "semantic_failed": [k for k, v in sem.items() if not v["ok"]],
        "extra_checks_failed": extra_failed_list,
        "exe_identity_ok": exe_ok,
        "run_errors": res["run_errors"],
        "overall_ok": overall_ok}, indent=2))
    # R5: exit code 0 iff overall_ok true, else nonzero
    sys.exit(0 if overall_ok else 1)


if __name__ == "__main__":
    main()
