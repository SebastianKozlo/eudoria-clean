# qc_correction_c1.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004
# Purpose: bounded machine re-verification of EXACTLY the byte-level statements
# this correction package re-states, plus the textual doc-gates of the
# correction QC (Q1-Q8). Two modes:
#   bytes    -> 01_RAW/QC_CORRECTION_BATTERY.json (byte battery)
#   docgates -> 01_RAW/QC_DOC_GATES.json (gates over THIS package's own docs)
#
# Bounded scope (enforced by construction - NO new science):
#   * NO decode of FUN_0070DC20, FUN_00843340, FUN_007292F0, FUN_00747970;
#     only the byte pins of ALREADY-published chain segments and the
#     dispatch-contract-stated GP2 alternative-flow call/JMP sites are read.
#   * NO factory+0x84 stream trace, NO RECORD_A analysis, NO templates.vfs
#     access, NO alias-closure/bulk-write/pointer-derived-write search. The
#     ONLY .text scan is the SAME direct-literal 4-byte-occurrence census the
#     R1 S5 instrument performed (re-measurement of the published measured
#     scope, classified store-vs-load-vs-raw), used to re-scope the census
#     claim, NOT to prove lifetime immutability.
#   * NO position/rotation/world-XYZ/network/model-join work.
# READ-ONLY vs the pinned EXE and the Desktop inputs. Writes only into this
# package's 01_RAW/.
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
DESKTOP_DIR = r"C:\Users\User\Documents\ChatGPT\PE\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_DESKTOP_POST_AUDIT_20261004"
REPORT_MD = os.path.join(DESKTOP_DIR, "REPORT.md")
REVIEW_TXT = os.path.join(DESKTOP_DIR, "PE_MASTER_REVIEW_INPUT.txt")

EXPECTED = {
    "exe_size": 8015872,
    "exe_sha256": "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31",
    "report_md_sha256": "B433828F8DF5C8EFF80A81303BD9A8CA88258E985A4ADB4760B1E6DEE3E670CD",
    "review_txt_sha256": "61A0DB5CBD4F52C806107A76811C9B13D0A83679F053556F91D2FC9781608AC9",
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
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

def locate(image_base, secs, va):
    rva = va - image_base
    for s in secs:
        if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rawsize"]):
            off_in_sec = rva - s["vaddr"]
            file_backed = off_in_sec < s["rawsize"]
            return {"section": s["name"], "rva": rva, "file_backed": file_backed,
                    "file_off": (s["rawptr"] + off_in_sec) if file_backed else None}
    return None

def read_at(d, image_base, secs, va, n):
    loc = locate(image_base, secs, va)
    if loc is None or not loc["file_backed"]:
        return None
    return d[loc["file_off"]:loc["file_off"]+n]

def text_blob(d, secs):
    for s in secs:
        if s["name"] == ".text":
            return s["rawptr"], s["rawsize"], s["vaddr"]
    raise RuntimeError("no .text")

# direct-store opcode forms over a disp32 literal: MOV [disp32], r32 (89 /r,
# mod=00 rm=101/110/111 style absolute) and MOV [disp32], imm32 (C7 05) and
# MOV [disp32], EAX (A3). The reg32 absolute forms are 89 05/0D/15/1D/25/2D/35/3D.
STORE_FORMS = {b"\x89\x05", b"\x89\x0D", b"\x89\x15", b"\x89\x1D",
               b"\x89\x25", b"\x89\x2D", b"\x89\x35", b"\x89\x3D",
               b"\xC7\x05", b"\xA3"}

def literal_census(d, image_base, secs, va):
    """SAME measured scope as R1 S5: raw 4-byte occurrences of the VA in .text,
    classified by the preceding opcode bytes. Store-classification only for
    DIRECT disp32 store forms. NOT an alias/bulk/indirect-write closure."""
    pat = struct.pack("<I", va)
    rawptr, rawsize, vaddr0 = text_blob(d, secs)
    blob = d[rawptr:rawptr+rawsize]
    hits = []
    start = 0
    while True:
        idx = blob.find(pat, start)
        if idx == -1:
            break
        site_va = image_base + vaddr0 + idx
        prev2 = blob[idx-2:idx] if idx >= 2 else b""
        prev1 = blob[idx-1:idx] if idx >= 1 else b""
        if prev2 in STORE_FORMS:
            cls = "DIRECT_STORE_FORM"
        elif prev1 == b"\xA3":
            cls = "DIRECT_STORE_FORM"
        elif prev1 in [bytes([op]) for op in range(0xB8, 0xC0)]:
            cls = "MOV_REG_IMM32_LOAD"
        else:
            cls = "RAW_BYTE_OCCURRENCE"
        hits.append({
            "va": "0x%08X" % site_va,
            "class": cls,
            "prev_bytes": blob[max(0, idx-3):idx].hex(" "),
            "window": blob[max(0, idx-8):idx+10].hex(" "),
        })
        start = idx + 1
    return hits

def check(name, measured, expected, ok):
    return {"check": name, "measured": measured, "expected": expected,
            "pass": bool(ok)}

def bytes_mode():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004",
           "mode": "bytes", "battery": "QC_CORRECTION_BATTERY"}
    checks = []

    # A. input identities (dispatch pins)
    rm_sha = sha256_file(REPORT_MD)
    checks.append(check("A1_DESKTOP_REPORT_SHA256", rm_sha,
                        EXPECTED["report_md_sha256"], rm_sha == EXPECTED["report_md_sha256"]))
    rv_sha = sha256_file(REVIEW_TXT)
    checks.append(check("A2_REVIEW_INPUT_SHA256", rv_sha,
                        EXPECTED["review_txt_sha256"], rv_sha == EXPECTED["review_txt_sha256"]))

    # B. pinned EXE identity
    exe_size = os.path.getsize(EXE)
    exe_sha = sha256_file(EXE)
    checks.append(check("B1_EXE_SIZE", exe_size, EXPECTED["exe_size"],
                        exe_size == EXPECTED["exe_size"]))
    checks.append(check("B2_EXE_SHA256", exe_sha, EXPECTED["exe_sha256"],
                        exe_sha == EXPECTED["exe_sha256"]))

    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base
    out["sections"] = secs

    def rd(va, n):
        return read_at(d, image_base, secs, va, n)

    def hx(va, n):
        b = rd(va, n)
        return None if b is None else b.hex(" ")

    # C. GP2 alternative-branch control flow (dispatch-stated pins, re-verified)
    # C1: CALL FUN_00843340 @0x004C550E (E8 rel32) -> result in EAX
    b = rd(0x004C550E, 5)
    tgt = struct.unpack_from("<i", b, 1)[0] + 0x004C550E + 5 if b and b[0] == 0xE8 else None
    checks.append(check("C1_ALT_CALL_843340_site_0x004C550E",
                        {"bytes": b.hex(" "), "resolved_target": "0x%08X" % tgt if tgt else None},
                        {"opcode": "E8", "target": "0x00843340"},
                        b[0] == 0xE8 and tgt == 0x00843340))
    # C2: JMP @0x004C5516 (EB 38) -> 0x004C5550
    b = rd(0x004C5516, 2)
    jtgt = 0x004C5516 + 2 + b[1] if b and b[0] == 0xEB else None
    checks.append(check("C2_JMP_conv_0x004C5516",
                        {"bytes": b.hex(" "), "target": "0x%08X" % jtgt if jtgt else None},
                        {"opcode": "EB 38", "target": "0x004C5550"},
                        b == b"\xEB\x38" and jtgt == 0x004C5550))
    # C3: MOV ESI,EAX @0x004C5550 (8B F0)
    b = rd(0x004C5550, 2)
    checks.append(check("C3_MOV_ESI_EAX_0x004C5550", b.hex(" "), "8B F0", b == b"\x8B\xF0"))
    # C4: cleanup CALL FUN_00703BC0 @0x004C555E (published epilogue pin)
    b = rd(0x004C555E, 5)
    tgt = struct.unpack_from("<i", b, 1)[0] + 0x004C555E + 5 if b and b[0] == 0xE8 else None
    checks.append(check("C4_CLEANUP_CALL_703BC0_0x004C555E",
                        {"bytes": b.hex(" "), "resolved_target": "0x%08X" % tgt if tgt else None},
                        {"opcode": "E8", "target": "0x00703BC0"},
                        b[0] == 0xE8 and tgt == 0x00703BC0))
    # C5: MOV EAX,ESI @0x004C5563 (8B C6)
    b = rd(0x004C5563, 2)
    checks.append(check("C5_MOV_EAX_ESI_0x004C5563", b.hex(" "), "8B C6", b == b"\x8B\xC6"))
    # C6: the return edge: FUN_004C5580 CALLs FUN_004C5480 @0x004C55B5
    b = rd(0x004C55B5, 5)
    tgt = struct.unpack_from("<i", b, 1)[0] + 0x004C55B5 + 5 if b and b[0] == 0xE8 else None
    checks.append(check("C6_CALLER_CALLS_GETTER_0x004C55B5",
                        {"bytes": b.hex(" "), "resolved_target": "0x%08X" % tgt if tgt else None},
                        {"opcode": "E8", "target": "0x004C5480"},
                        b[0] == 0xE8 and tgt == 0x004C5480))
    # C7: TEST EAX,EAX @0x004C55BD (85 C0)
    b = rd(0x004C55BD, 2)
    checks.append(check("C7_TEST_EAX_EAX_0x004C55BD", b.hex(" "), "85 C0", b == b"\x85\xC0"))
    # C8: JE 0x004C5AB6 @0x004C55C3 (0F 84 ED 04 00 00) - zero -> abort
    b = rd(0x004C55C3, 6)
    jtgt = struct.unpack_from("<i", b, 2)[0] + 0x004C55C3 + 6 if b and b[0] == 0x0F and b[1] == 0x84 else None
    checks.append(check("C8_JE_ABORT_0x004C55C3",
                        {"bytes": b.hex(" "), "target": "0x%08X" % jtgt if jtgt else None},
                        {"opcode": "0F 84 ED 04 00 00", "target": "0x004C5AB6"},
                        b == b"\x0F\x84\xED\x04\x00\x00" and jtgt == 0x004C5AB6))
    # C9: PUSH ESI @0x004C55D0 (56) + PUSH EAX @0x004C55D1 (50)
    b = rd(0x004C55D0, 2)
    checks.append(check("C9_PUSH_ESI_EAX_0x004C55D0", b.hex(" "), "56 50", b == b"\x56\x50"))
    # C10: CALL FUN_0072F880 @0x004C55D9 (E8 rel32) - the shared lookup
    b = rd(0x004C55D9, 5)
    tgt = struct.unpack_from("<i", b, 1)[0] + 0x004C55D9 + 5 if b and b[0] == 0xE8 else None
    checks.append(check("C10_SHARED_LOOKUP_CALL_0x004C55D9",
                        {"bytes": b.hex(" "), "resolved_target": "0x%08X" % tgt if tgt else None},
                        {"opcode": "E8", "target": "0x0072F880"},
                        b[0] == 0xE8 and tgt == 0x0072F880))
    # ORDER gate: abort JE (0x004C55C3) precedes key PUSH (0x004C55D1) and the
    # lookup CALL (0x004C55D9) => a ZERO result aborts BEFORE the lookup.
    checks.append(check("C11_ZERO_ABORT_PRECEDES_LOOKUP_order",
                        {"test": 0x004C55BD, "je": 0x004C55C3,
                         "push": 0x004C55D1, "call": 0x004C55D9},
                        "TEST < JE < PUSH EAX < CALL FUN_0072F880",
                        0x004C55BD < 0x004C55C3 < 0x004C55D1 < 0x004C55D9))
    out["gp2_flow_window"] = {
        "getter_conv_to_ret": hx(0x004C5550, 0x18),
        "caller_test_to_call": hx(0x004C55BD, 0x22),
        "alt_call_to_jmp": hx(0x004C550D, 0x0D),
    }

    # D. GP3 fallback statics
    statics = {}
    for name, va in (("DAT_00BA5108_default_slot", 0x00BA5108),
                     ("DAT_00BA9374_fallback_slot_object", 0x00BA9374)):
        loc = locate(image_base, secs, va)
        content = rd(va, 4)
        statics[name] = {
            "va": "0x%08X" % va,
            "section": loc["section"] if loc else None,
            "file_backed": loc["file_backed"] if loc else None,
            "initial_4bytes": content.hex(" ") if content is not None else None,
            "mapped_content": ("ZERO_AT_IMAGE_MAPPING" if (content is None or content == b"\x00\x00\x00\x00") else "NONZERO"),
        }
    out["fallback_statics"] = statics
    ok_statics = all(v["mapped_content"] == "ZERO_AT_IMAGE_MAPPING" for v in statics.values())
    checks.append(check("D1_STATICS_ZERO_AT_IMAGE_MAPPING",
                        {k: v["mapped_content"] for k, v in statics.items()},
                        "both ZERO_AT_IMAGE_MAPPING", ok_statics))
    # D2: FUN_00977780 returns the fallback static: B8 74 93 BA 00 C3 @0x00977780
    b = rd(0x00977780, 6)
    checks.append(check("D2_FUN_00977780_returns_BA9374", b.hex(" "),
                        "B8 74 93 BA 00 C3", b == b"\xB8\x74\x93\xBA\x00\xC3"))
    # D3: fallback call site @0x004C5549 (E8 -> 0x00977780) + convergence read
    b = rd(0x004C5549, 5)
    tgt = struct.unpack_from("<i", b, 1)[0] + 0x004C5549 + 5 if b and b[0] == 0xE8 else None
    checks.append(check("D3_FALLBACK_CALL_0x004C5549",
                        {"bytes": b.hex(" "), "resolved_target": "0x%08X" % tgt if tgt else None},
                        {"opcode": "E8", "target": "0x00977780"},
                        b[0] == 0xE8 and tgt == 0x00977780))
    b = rd(0x004C554E, 2)
    checks.append(check("D4_CONV_READ_0x004C554E", b.hex(" "), "8B 00", b == b"\x8B\x00"))
    # D5: FUN_0070C180 out-of-range default: MOV EAX,0x00BA5108; RET 4
    b = rd(0x0070C1DF, 8)
    checks.append(check("D5_DEFAULT_SLOT_RETURN_0x0070C1DF", b.hex(" "),
                        "B8 08 51 BA 00 C2 04 00",
                        b == b"\xB8\x08\x51\xBA\x00\xC2\x04\x00"))
    # D6: direct-literal census (SAME measured scope as R1 S5) - re-measured
    census = {}
    for name, va in (("0x00BA5108", 0x00BA5108), ("0x00BA9374", 0x00BA9374)):
        hits = literal_census(d, image_base, secs, va)
        census[name] = {"hits": hits,
                        "store_form_count": sum(1 for h in hits if h["class"] == "DIRECT_STORE_FORM")}
    out["direct_literal_census"] = census
    checks.append(check("D6_DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN",
                        {k: v["store_form_count"] for k, v in census.items()},
                        "0 direct-store-form occurrences for BOTH statics (measured scan scope)",
                        all(v["store_form_count"] == 0 for v in census.values())))

    # E. GP1 scoped default-creation-path pins (the zero-init statement this
    # correction PRESERVES with its exact scope)
    # E1: int traits vtable 0x00A9C670 slot 1 = 0x009777E0
    b = rd(0x00A9C674, 4)
    v = struct.unpack("<I", b)[0]
    checks.append(check("E1_INTTRAITS_VTABLE_SLOT1", "0x%08X" % v, "0x009777E0", v == 0x009777E0))
    # E2: FUN_009777E0 = MOV EAX,[ESP+4]; MOV DWORD [EAX],0; RET 4
    b = rd(0x009777E0, 12)
    checks.append(check("E2_INTTRAITS_SLOT1_ZERO_INIT_BYTES", b.hex(" "),
                        "8B 44 24 04 C7 00 00 00 00 00 C2 04",
                        b == b"\x8B\x44\x24\x04\xC7\x00\x00\x00\x00\x00\xC2\x04"))
    # E3: factory bind MOV [EBX+4],ESI @0x0070D9A5 (89 73 04)
    b = rd(0x0070D9A5, 3)
    checks.append(check("E3_FACTORY_BIND_0x0070D9A5", b.hex(" "), "89 73 04",
                        b == b"\x89\x73\x04"))
    # E4: slot-6 schema args @0x73758D (9-byte sequence: PUSH traits; PUSH 0;
    # PUSH 0; PUSH 1 (kind); PUSH 6 (tag))
    b = rd(0x0073758D, 9)
    checks.append(check("E4_SLOT6_SCHEMA_ARGS_0x73758D", b.hex(" "),
                        "50 6A 00 6A 00 6A 01 6A 06",
                        b == b"\x50\x6A\x00\x6A\x00\x6A\x01\x6A\x06"))
    # E5: writer idiom @0x0070DA36 (8B 44 19 08)
    b = rd(0x0070DA36, 4)
    checks.append(check("E5_TABLE_WRITER_IDIOM_0x0070DA36", b.hex(" "), "8B 44 19 08",
                        b == b"\x8B\x44\x19\x08"))
    # E6: reader idiom @0x004C5539 (8B 40 08) + LEA @0x004C553F (8D 0C 81)
    b1 = rd(0x004C5539, 3)
    b2 = rd(0x004C553F, 3)
    checks.append(check("E6_TABLE_READER_IDIOMS",
                        {"read": b1.hex(" "), "lea": b2.hex(" ")},
                        {"read": "8B 40 08", "lea": "8D 0C 81"},
                        b1 == b"\x8B\x40\x08" and b2 == b"\x8D\x0C\x81"))

    npass = sum(1 for c in checks if c["pass"])
    out["checks"] = checks
    out["summary"] = {"total": len(checks), "pass": npass, "fail": len(checks) - npass}
    out["forbidden_actions"] = [
        {"action": "decode_FUN_0070DC20", "executed": "NO"},
        {"action": "decode_FUN_00843340_beyond_call_site", "executed": "NO"},
        {"action": "trace_factory_plus_0x84_stream", "executed": "NO"},
        {"action": "analyze_RECORD_A", "executed": "NO"},
        {"action": "open_templates_vfs", "executed": "NO"},
        {"action": "alias_closure_or_bulk_write_search", "executed": "NO"},
        {"action": "model_join_position_rotation_world_xyz_network", "executed": "NO"},
        {"action": "launch_client", "executed": "NO"},
    ]
    with open(os.path.join(RUN, "01_RAW", "QC_CORRECTION_BATTERY.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("bytes battery: %d/%d PASS" % (npass, len(checks)))
    for c in checks:
        if not c["pass"]:
            print("FAIL:", c["check"], "measured=", c["measured"])

# ---------------------------------------------------------------------------
# docgates: textual gates Q1-Q8 over THIS package's own docs.
# FINAL_REPORT.md and HANDOFF.md are scanned for ACTIVE corrected claims;
# SUPERSESSION_LEDGER.md is allowed to contain the historical wording ONLY
# inside clearly-identified ORIGINAL_EXCERPT / SUPERSEDED context (keyword hit
# inside such context is not a failure), so the ledger is checked only for
# the positive presence of corrected dispositions.
DOC_REQ = {
    "FINAL_REPORT.md": [
        "IMMEDIATE_VALUE_STORAGE = PER_RECEIVER_COMPONENT_VALUE_TABLE",
        "ULTIMATE_VALUE_SOURCE = UNKNOWN",
        "FILE_DERIVED_VALUE_EXCLUDED = NO",
        "RECORD_A_RELATION = NOT_ESTABLISHED",
        "DEFAULT_CREATION_PATH_INITIAL_VALUE = 0",
        "NONZERO_VALUE_PRODUCER = UNRESOLVED",
        "NONZERO_VALUE_PRODUCER_TIMING = UNRESOLVED",
        "ALTERNATIVE_TAG6_SEGMENT = BYPASSED",
        "ALTERNATIVE_SHARED_LOOKUP = CONDITIONAL_ON_NONZERO_RESULT",
        "FUN_00843340_RESULT_SEMANTIC = UNKNOWN",
        "FUN_00843340_RESULT_TO_LOOKUP_KEY = CONFIRMED_CONDITIONAL_ON_NONZERO",
        "FALLBACK_STATIC_INITIAL_CONTENT = ZERO_AT_IMAGE_MAPPING",
        "DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN = NO",
        "FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED",
        "ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL",
        "FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED",
        "MAX_NEW_FUNCTIONS_AUTHORIZED = 20",
        "ACTUAL_DETAILED_COUNT = 28",
        "GETTER_RESULT_TO_LOOKUP_KEY = PRESERVED_CONFIRMED",
        "GETTER_RESULT_PROVENANCE = UNKNOWN",
        "PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED",
        "NEW_PLACEMENT_SCIENCE_EXECUTED = NO",
        "NEXT_EXPERIMENT_EXECUTED = NO",
    ],
    "HANDOFF.md": [
        "FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED",
        "GETTER_RESULT_PROVENANCE = UNKNOWN",
    ],
    "SUPERSESSION_LEDGER.md": [
        "GP1", "GP2", "GP3", "PROCESS_BUDGET",
        "ORIGINAL_EXCERPT",
    ],
}
DOC_FORBID = {
    # ACTIVE-claim documents must not carry the superseded wording; historical
    # wording is only allowed in SUPERSESSION_LEDGER.md inside SUPERSEDED
    # ORIGINAL_EXCERPT context (checked by positive gates above).
    "FINAL_REPORT.md": [
        "permanently-zero", "permanently zero", "permanently ZERO",
        "NEVER consults",
        "was written into table[10] after creation",
        "was written into table[10] AFTER class_obj creation",
        "honest stop", "stopped per contract", "stop per contract",
        "stopped RE at the value-writer boundary per contract",
    ],
    "HANDOFF.md": [
        "permanently-zero", "permanently zero", "permanently ZERO",
        "NEVER consults",
        "was written into table[10] after creation",
        "honest stop", "stopped per contract", "stop per contract",
    ],
}

def docgates_mode():
    gates = []
    for fname, required in DOC_REQ.items():
        p = os.path.join(RUN, fname)
        txt = open(p, "r", encoding="utf-8").read()
        missing = [s for s in required if s not in txt]
        gates.append({"gate": "REQ_%s" % fname, "missing": missing,
                      "pass": not missing})
        if fname in DOC_FORBID:
            hits = [s for s in DOC_FORBID[fname] if s in txt]
            gates.append({"gate": "FORBID_%s" % fname, "hits": hits,
                          "pass": not hits})
    # Q-mapping record
    qmap = {
        "Q1": ["FINAL_REPORT.md:IMMEDIATE_VALUE_STORAGE/ULTIMATE_VALUE_SOURCE/FILE_DERIVED_VALUE_EXCLUDED"],
        "Q2": ["FINAL_REPORT.md:DEFAULT_CREATION_PATH_INITIAL_VALUE + NONZERO_VALUE_PRODUCER_TIMING; no universal after-creation wording"],
        "Q3": ["FINAL_REPORT.md:ALTERNATIVE_* + FUN_00843340_* fields"],
        "Q4": ["FINAL_REPORT.md:FALLBACK_STATIC_INITIAL_CONTENT / DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN / FALLBACK_STATIC_LIFETIME_IMMUTABILITY"],
        "Q5": ["FINAL_REPORT.md:ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL; no permanently-zero wording"],
        "Q6": ["FINAL_REPORT.md:FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED; no 'per contract' compliance wording"],
        "Q7": ["FINAL_REPORT.md:GETTER_RESULT_TO_LOOKUP_KEY = PRESERVED_CONFIRMED / GETTER_RESULT_PROVENANCE = UNKNOWN / PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED"],
        "Q8": ["QC_CORRECTION_BATTERY.json forbidden_actions all NO + docs NEW_PLACEMENT_SCIENCE_EXECUTED = NO / NEXT_EXPERIMENT_EXECUTED = NO"],
    }
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004",
           "mode": "docgates", "qc_scope": "SELF_CHECK_GETTER_PROVENANCE_REPORT_SCOPE_CORRECTION",
           "gates": gates, "q_mapping": qmap}
    npass = sum(1 for g in gates if g["pass"])
    out["summary"] = {"total": len(gates), "pass": npass, "fail": len(gates) - npass}
    with open(os.path.join(RUN, "01_RAW", "QC_DOC_GATES.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("docgates: %d/%d PASS" % (npass, len(gates)))
    for g in gates:
        if not g["pass"]:
            print("FAIL:", g["gate"], g.get("missing", g.get("hits")))

def _norm(s):
    return " ".join(s.split())

def quotecheck_mode():
    """Every SUPERSESSION_LEDGER.md row's ORIGINAL_EXCERPT fenced blocks must
    be real (whitespace-normalized) substrings of the row's named SOURCE_FILE.
    No fabricated quotes; no quote assigned to a file where it is absent."""
    import re
    repo = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
    ledger = os.path.join(RUN, "SUPERSESSION_LEDGER.md")
    txt = open(ledger, "r", encoding="utf-8").read()
    rows = re.split(r"\n### Row ", "\n" + txt)
    checks = []
    for chunk in rows[1:]:
        title = chunk.split("\n", 1)[0].strip()
        m = re.search(r"SOURCE_FILE: `([^`]+)`", chunk)
        if not m:
            checks.append({"row": title, "error": "no SOURCE_FILE", "pass": False})
            continue
        src = m.group(1)
        path = src if re.match(r"^[A-Za-z]:\\", src) else os.path.join(repo, src)
        blocks = re.findall(r"```\n(.*?)```", chunk, flags=re.S)
        if not blocks:
            checks.append({"row": title, "source": src,
                           "error": "no ORIGINAL_EXCERPT block", "pass": False})
            continue
        content_n = _norm(open(path, "r", encoding="utf-8").read())
        missing = []
        for q in blocks:
            if _norm(q) not in content_n:
                missing.append(_norm(q)[:80] + "...")
        checks.append({"row": title, "source": src, "quotes": len(blocks),
                       "missing_in_source": missing, "pass": not missing})
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004",
           "mode": "quotecheck", "checks": checks}
    npass = sum(1 for c in checks if c["pass"])
    out["summary"] = {"total": len(checks), "pass": npass,
                      "fail": len(checks) - npass}
    with open(os.path.join(RUN, "01_RAW", "QC_LEDGER_QUOTE_CHECKS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("quotecheck: %d/%d PASS" % (npass, len(checks)))
    for c in checks:
        if not c["pass"]:
            print("FAIL:", c)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "bytes"
    if mode == "bytes":
        bytes_mode()
    elif mode == "docgates":
        docgates_mode()
    elif mode == "quotecheck":
        quotecheck_mode()
    else:
        raise SystemExit("mode must be bytes|docgates|quotecheck")
