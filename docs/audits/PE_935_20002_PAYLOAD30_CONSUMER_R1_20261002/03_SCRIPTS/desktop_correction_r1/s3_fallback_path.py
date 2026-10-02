# s3_fallback_path.py — FALLBACK_PATH_RECORD.json generator (DESKTOP_CORRECTION_R1)
# Records the OLD claimed selected-reader path (FUN_00412540) explicitly as
# BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH, with independently
# recomputed file offsets (0x12553 / 0x1255A), its reachability condition
# (descriptor+0 == NULL, the JZ target in FUN_0075f660), and the reason it is
# NOT selected for tag ID 17. Also records the old REPORT transcription error
# "READ_INSTRUCTION_FILE_OFFSET = 0x00125553" as superseded (digit-shift).
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

RUN_ID = "PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002"
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "01_RAW", "DESKTOP_CORRECTION_R1",
                                    "FALLBACK_PATH_RECORD.json"))

pe = pe_parse.PE32()

def pin(va, length, expected_hex, claim, role, extra=None):
    p = pe.pin(va, length)
    p["expected_bytes_hex"] = expected_hex.upper() if expected_hex else None
    p["match"] = (p["expected_bytes_hex"] is None) or (p["original_bytes_hex"] == p["expected_bytes_hex"])
    p["claim"] = claim
    p["role"] = role
    if extra:
        p.update(extra)
    return p

def rel32_target(va_of_e8):
    b = pe.read_va(va_of_e8, 5)
    assert b[0] in (0xE8, 0xE9), "not a CALL/JMP rel32 at 0x%08X" % va_of_e8
    rel = struct.unpack_from("<i", b, 1)[0]
    return va_of_e8 + 5 + rel

def jrel8_target(va, length):
    b = pe.read_va(va, length)
    rel = struct.unpack_from("<b", b, length - 1)[0]
    return va + length + rel

jz_target = jrel8_target(0x75F66E, 2)
scalar_jz = jrel8_target(0x75F694, 2)
t_scalar = rel32_target(0x75F6AA)
t_array = rel32_target(0x75F696)
t_case1 = rel32_target(0x4129DF)
jt_entry0 = pe.read_u32_va(0x412A68)

pins = []
pins.append(pin(0x75F66E, 2, "7417",
    "JZ -> 0x%08X - THE FALLBACK REACHABILITY CONDITION: this branch is taken ONLY when [descriptor+0] == NULL" % jz_target,
    "fallback reachability gate (inside the virtual-branch dispatch FUN_0075f660)"))
pins.append(pin(0x75F687, 4, "F6400C01",
    "TEST byte [EAX+0xC],1 - descriptor FLAGS bit0 test (fallback only; 0xC0 & 1 == 0 for tag 17)",
    "fallback: flags bit0 test"))
pins.append(pin(0x75F68B, 3, "8B4004",
    "MOV EAX,[EAX+4] - the descriptor TYPE (1)",
    "fallback: type load"))
pins.append(pin(0x75F694, 2, "7414",
    "JZ -> 0x%08X - flags bit0 clear -> the SCALAR fallback path" % scalar_jz,
    "fallback: scalar-path branch"))
pins.append(pin(0x75F696, 5, "E8E536CBFF",
    "CALL FUN_00412d80 (rel32 target computed = 0x%08X) - the ARRAY fallback (flags bit0 set; NOT the tag-17 state even on the fallback)" % t_array,
    "fallback: array-path call"))
pins.append(pin(0x75F6AA, 5, "E81133CBFF",
    "CALL FUN_004129c0 (rel32 target computed = 0x%08X) - the SCALAR fallback type switch" % t_scalar,
    "fallback: scalar-switch call"))
pins.append(pin(0x4129C0, 4, "8B442408",
    "MOV EAX,[ESP+8] - the fallback switch's TYPE argument (1)",
    "fallback switch: type load"))
pins.append(pin(0x4129C4, 3, "83C0FF",
    "ADD EAX,-1 (type-1 range normalization)",
    "fallback switch: range normalize"))
pins.append(pin(0x4129C7, 3, "83F808",
    "CMP EAX,8 (types 1..9 supported)",
    "fallback switch: range check"))
pins.append(pin(0x4129D1, 7, "FF2485682A4100",
    "JMP dword [EAX*4 + 0x00412A68] - the switch jump table",
    "fallback switch: jump table dispatch"))
pins.append(pin(0x412A68, 4, None,
    "jump-table entry 0 (type 1) = 0x%08X - the case-1 body" % jt_entry0,
    "fallback switch: jump-table entry (static .text dword)"))
pins.append(pin(0x4129D8, 4, "8B742408",
    "MOV ESI,[ESP+8] - the case-1 body: the cursor argument",
    "fallback switch case 1: cursor load"))
pins.append(pin(0x4129DC, 1, "51",
    "PUSH ECX - the dest argument (loaded by the caller at 0x75F68E)",
    "fallback switch case 1: dest push"))
pins.append(pin(0x4129DD, 2, "8BCE",
    "MOV ECX,ESI - this = the cursor",
    "fallback switch case 1: this setup"))
pins.append(pin(0x4129DF, 5, "E85CFBFFFF",
    "CALL FUN_00412540 (rel32 target computed = 0x%08X) - THE CASE-TYPE-1 DISPATCH" % t_case1,
    "fallback switch case 1: the FUN_00412540 dispatch"))
# FUN_00412540 full instruction window (the fallback type-1 reader)
pins.append(pin(0x412540, 18, "8079110074238B410C8D50043B510877188B",
    "FUN_00412540 prologue: CMP byte [ECX+0x11],0 (cursor flag); JZ error; MOV EAX,[ECX+0xC] (offset); "
    "LEA EDX,[EAX+4] (width bound); CMP EDX,[ECX+8] (limit); JA error; MOV EDX,[ECX] (base)",
    "fallback reader: full prologue window"))
pins.append(pin(0x412553, 3, "8B0410",
    "MOV EAX,[EDX+EAX*1] - THE FALLBACK READ (4-byte LE at cursor.base+offset). "
    "Independently recomputed file offset = 0x%08X (RVA 0x12553; .text raw_pointer 0x1000 == virtual_address 0x1000)"
    % int(pe.pin(0x412553, 3)["file_offset"], 16),
    "fallback reader: THE READ INSTRUCTION (BYTE-CORRECT; NON-SELECTED for tag 17)"))
pins.append(pin(0x412556, 4, "8B542404",
    "MOV EDX,[ESP+4] - the dest pointer argument",
    "fallback reader: dest load"))
pins.append(pin(0x41255A, 2, "8902",
    "MOV [EDX],EAX - THE FALLBACK STORE. Independently recomputed file offset = 0x%08X"
    % int(pe.pin(0x41255A, 2)["file_offset"], 16),
    "fallback reader: THE STORE INSTRUCTION (BYTE-CORRECT; NON-SELECTED for tag 17)"))
pins.append(pin(0x41255C, 8, "C744240404000000",
    "MOV dword [ESP+4],4 - the fallback advance width",
    "fallback reader: advance width"))
pins.append(pin(0x412564, 5, "E9F7B8FFFF",
    "JMP FUN_0040de60 (tail) - the fallback cursor advance by 4",
    "fallback reader: advance tail-jump"))
pins.append(pin(0x412569, 4, "8B442404",
    "ERROR PATH of the fallback reader: MOV EAX,[ESP+4] (dest pointer)",
    "fallback reader: error path (dest load)"))
pins.append(pin(0x41256D, 6, "C70000000000",
    "MOV dword [EAX],0 - ERROR PATH: the destination is zeroed",
    "fallback reader: error path (dest = 0)"))
pins.append(pin(0x412579, 4, "C6411100",
    "MOV byte [ECX+0x11],0 - ERROR PATH: the cursor flag is CLEARED (failure propagation; NOT the successful parse path)",
    "fallback reader: error path (cursor flag cleared)"))
pins.append(pin(0x41257D, 3, "C20400",
    "RET 4 - the fallback reader's error-path return (pops its single stack arg: the dest; contrast the SELECTED reader FUN_009777F0's RET 8 = cursor + dest)",
    "fallback reader: error path return"))

all_match = all(p["match"] for p in pins)
art = {
    "run_id": RUN_ID,
    "artifact": "FALLBACK_PATH_RECORD.json",
    "generator": "03_SCRIPTS/desktop_correction_r1/s3_fallback_path.py",
    "generator_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest().upper(),
    "exe_path": pe.path,
    "exe_sha256": pe.sha256,
    "exe_size": pe.size,
    "classification": "BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH",
    "the_old_claim_superseded": {
        "old_selected_reader": "FUN_00412540",
        "old_read": {"va": "0x00412553", "bytes": "8B 04 10"},
        "old_store": {"va": "0x0041255A", "bytes": "89 02"},
        "old_chain": "FUN_00726900 -> FUN_0075f660 @0x726A1B -> (flags bit0 test @0x75F687, 0xC0 & 1 == 0) -> FUN_004129c0 @0x75F6AA -> case type 1 @0x4129DF -> FUN_00412540",
        "what_was_wrong": "The old trace treated the flags-bit0/typed-reader path as THE selected path. The bytes show the flags-bit0 test "
                          "lives INSIDE the fallback (reachable only after the JZ @0x75F66E is TAKEN, i.e. conditional on descriptor+0 == NULL), "
                          "which is NOT the tag-ID-17 state: the registration dataflow + factory bytes prove descriptor+0 = 0x00BA937C (non-NULL), "
                          "so the JZ is NOT taken and the VIRTUAL branch is selected (see BRANCH_SELECTION_TRACE.json).",
        "lesson": "correct instruction bytes != proven selected execution/parser path",
    },
    "reachability_condition": {
        "gate": "FUN_0075f660: TEST ECX,ECX @0x75F664 (ECX = [descriptor+0]) followed by JZ @0x75F66E -> 0x75F687",
        "condition": "the fallback is selected IFF descriptor+0 == NULL",
        "tag_17_descriptor_plus_0": "0x00BA937C (the ArkRTTraitsInt static object returned by FUN_00977a50; byte-proven non-NULL on both factory paths)",
        "verdict": "FALLBACK NOT SELECTED for tag ID 17 (control-flow reachability from the proven descriptor state)",
        "note_on_the_old_reasoning": "the old 'flags bit0 test @0x75F687 -> scalar path' reasoning only holds AFTER the JZ, i.e. conditional on descriptor+0 == NULL",
    },
    "corrected_file_offsets": {
        "read_instruction": {"va": "0x00412553", "rva": "0x00012553", "file_offset": "0x00012553",
                             "recomputed_by": "this run's own PE32 section-table computation (.text: virtual_address 0x1000, raw_pointer 0x1000)"},
        "store_instruction": {"va": "0x0041255A", "rva": "0x0001255A", "file_offset": "0x0001255A"},
        "old_report_transcription": {
            "was": "READ_INSTRUCTION_FILE_OFFSET = 0x00125553 (06_REPORT/REPORT.md, superseded)",
            "problem": "digit-shift error: 0x00125553 is a 7-hex-digit value (1194067) that does not equal the correct offset 0x12553 (75173); "
                       "the run's own pin JSON (01_RAW/CLIENT_READ_BYTES.json, immutable) already recorded the correct file_offset 0x12540-region pins "
                       "with READ @ file_offset 0x12553",
            "disposition": "superseded by the corrected value 0x12553 in DESKTOP_CORRECTION_R1; the pin JSON was always correct",
        },
    },
    "historical_preservation_note": [
        "01_RAW/CLIENT_READ_BYTES.json is byte-unchanged (immutable): its pins are BYTE-CORRECT and remain valid as FALLBACK-path + routing evidence.",
        "Its 'role' fields ('READ_FUNCTION=FUN_00412540 (type-1 scalar value reader)', 'THE CLIENT READ INSTRUCTION') describe the fallback reader's bytes;",
        "the SELECTED-path correction (virtual branch -> FUN_009777F0) lives in the NEW artifacts of 01_RAW/DESKTOP_CORRECTION_R1/.",
    ],
    "pin_count": len(pins),
    "match_count": sum(1 for p in pins if p["match"]),
    "all_match": all_match,
    "pins": pins,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(art, f, indent=1)
    f.write("\n")
print("wrote", OUT)
print("pins:", len(pins), "match:", sum(1 for p in pins if p["match"]), "all_match:", all_match)
print("jz_target=0x%08X scalar_jz=0x%08X t_scalar=0x%08X t_array=0x%08X t_case1=0x%08X jt_entry0=0x%08X" %
      (jz_target, scalar_jz, t_scalar, t_array, t_case1, jt_entry0))
