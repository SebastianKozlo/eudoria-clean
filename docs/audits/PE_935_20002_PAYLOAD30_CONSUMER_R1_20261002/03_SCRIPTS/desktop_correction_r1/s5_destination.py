# s5_destination.py — DESTINATION_PROOF_CORRECTION_R1.json generator (DESKTOP_CORRECTION_R1)
# Byte-pins the slot-21 destination chain for the SELECTED reader (FUN_009777F0):
#   descriptor field index (tag+4) -> value array at instance+0x40 ->
#   LEA dest = value_array + field_index*4 -> slot 21 (+0x54), width 4 ->
#   the selected store @0x00977810 (89 02).
# Static analysis only. Self-contained.
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

RUN_ID = "PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002"
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "01_RAW", "DESKTOP_CORRECTION_R1",
                                    "DESTINATION_PROOF_CORRECTION_R1.json"))

pe = pe_parse.PE32()

def pin(va, length, expected_hex, claim, role):
    p = pe.pin(va, length)
    p["expected_bytes_hex"] = expected_hex.upper() if expected_hex else None
    p["match"] = (p["expected_bytes_hex"] is None) or (p["original_bytes_hex"] == p["expected_bytes_hex"])
    p["claim"] = claim
    p["role"] = role
    return p

def rel32_target(va_of_e8):
    b = pe.read_va(va_of_e8, 5)
    assert b[0] in (0xE8, 0xE9), "not a CALL/JMP rel32 at 0x%08X" % va_of_e8
    rel = struct.unpack_from("<i", b, 1)[0]
    return va_of_e8 + 5 + rel

t_dispatch = rel32_target(0x726A1B)

pins = []
# --- the descriptor field index: tag + 4 (registration side) ---
pins.append(pin(0x70CBF6, 3, "83C104",
    "ADD ECX,4 - FIELD INDEX = TAG + 4 (inside FUN_0070cbc0, feeding FUN_0075f5c0's arg1)",
    "destination: the field-index formula (registration side)"))
pins.append(pin(0x75F5CC, 4, "8B4C2404",
    "MOV ECX,[ESP+4] - FUN_0075f5c0 arg1 = the field index",
    "destination: the field-index argument load"))
pins.append(pin(0x75F5D7, 3, "894808",
    "MOV [EAX+8],ECX - descriptor+8 = FIELD INDEX (tag 0x11 -> 0x15 = 21)",
    "destination: the descriptor field-index store"))
# --- the dispatch-caller chain (FUN_00726900) ---
pins.append(pin(0x726A0E, 3, "8B4808",
    "MOV ECX,[EAX+8] - the descriptor FIELD INDEX load (ECX = 0x15 = 21 for tag 0x11)",
    "destination chain: field index load"))
pins.append(pin(0x726A11, 3, "8B5540",
    "MOV EDX,[EBP+0x40] - instance+0x40 = THE VALUE ARRAY POINTER (22 u32 slots)",
    "destination chain: the value-array load"))
pins.append(pin(0x726A14, 3, "8D0C8A",
    "LEA ECX,[EDX+ECX*4] - DEST = value_array + field_index*4 = value_array + 21*4 = value_array + 0x54 (SLOT 21)",
    "destination chain: THE destination address computation"))
pins.append(pin(0x726A17, 1, "51",
    "PUSH ECX - the dest argument (slot-21 address) pushed for FUN_0075f660",
    "destination chain: dest push (arg2 of the dispatch)"))
pins.append(pin(0x726A18, 1, "56",
    "PUSH ESI - the cursor argument (arg1 of the dispatch)",
    "destination chain: cursor push"))
pins.append(pin(0x726A19, 2, "8BC8",
    "MOV ECX,EAX - this = the descriptor",
    "destination chain: dispatch this setup"))
pins.append(pin(0x726A1B, 5, "E8408C0300",
    "CALL FUN_0075f660 (rel32 target computed = 0x%08X) - the dispatch carrying (cursor, dest)" % t_dispatch,
    "destination chain: the dispatch call"))
# --- the virtual branch passes the dest through (FUN_0075f660) ---
pins.append(pin(0x75F670, 4, "8B542410",
    "MOV EDX,[ESP+0x10] - the virtual branch loads the DEST argument (entry arg2 = the slot-21 address)",
    "destination chain: the dispatch's dest load (virtual branch)"))
pins.append(pin(0x75F679, 1, "52",
    "PUSH EDX - the dest argument pushed for the virtual call (the reader's arg2)",
    "destination chain: the virtual call's dest push"))
pins.append(pin(0x75F67A, 1, "56",
    "PUSH ESI - the cursor argument pushed for the virtual call (the reader's arg1)",
    "destination chain: the virtual call's cursor push"))
# --- the selected reader stores there ---
pins.append(pin(0x97780A, 4, "8B542408",
    "MOV EDX,[ESP+8] - the SELECTED reader FUN_009777F0 loads its arg2 = THE DEST (the slot-21 address)",
    "destination chain: the reader's destination-argument load"))
pins.append(pin(0x977810, 2, "8902",
    "MOV [EDX],EAX - THE SELECTED STORE: the 4-byte value lands at *dest = value_array[21] (width 4, dword)",
    "destination chain: THE SELECTED STORE INSTRUCTION"))
# --- the value-array allocation (FUN_0070d990; context pins) ---
pins.append(pin(0x70D9A8, 6, "8B8E8C000000",
    "MOV ECX,[ESI+0x8C] - the class-object descriptor-vector END (for the slot count)",
    "value-array allocation: vector end"))
pins.append(pin(0x70D9AE, 6, "2B8E88000000",
    "SUB ECX,[ESI+0x88] - the vector byte size (end - begin)",
    "value-array allocation: vector size"))
pins.append(pin(0x70D9B8, 3, "C1F904",
    "SAR ECX,4 - the descriptor COUNT (stride 16)",
    "value-array allocation: descriptor count"))
pins.append(pin(0x70D9BB, 3, "83C104",
    "ADD ECX,4 - SLOTS = DESCRIPTOR COUNT + 4 (18 + 4 = 22 for the ArkParameterArmor schema; tags 0x00..0x11 = 18 descriptors)",
    "value-array allocation: the count+4 slot formula"))
pins.append(pin(0x70D9BF, 3, "8D7B40",
    "LEA EDI,[EBX+0x40] - THE VALUE ARRAY LIVES AT INSTANCE+0x40 (the instance is in EBX)",
    "value-array allocation: the instance+0x40 slot"))
t_alloc = rel32_target(0x70D9C9)
pins.append(pin(0x70D9C9, 5, "E88252D0FF",
    "CALL FUN_00412c50 (rel32 target computed = 0x%08X) - the value-array allocation (this = &instance+0x40, count+4 slots)" % t_alloc,
    "value-array allocation: the allocation call"))
pins.append(pin(0x70D9A3, 2, "8BD8",
    "MOV EBX,EAX - the new instance (from the class-object factory virtual at vtable+4)",
    "value-array allocation: the instance register"))
pins.append(pin(0x70D9A5, 3, "897304",
    "MOV [EBX+4],ESI - instance+4 = THE CLASS OBJECT (the schema holder used by the TLV loop's descriptor lookup)",
    "value-array allocation: the instance+4 class-object store"))

all_match = all(p["match"] for p in pins)
art = {
    "run_id": RUN_ID,
    "artifact": "DESTINATION_PROOF_CORRECTION_R1.json",
    "generator": "03_SCRIPTS/desktop_correction_r1/s5_destination.py",
    "generator_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest().upper(),
    "exe_path": pe.path,
    "exe_sha256": pe.sha256,
    "exe_size": pe.size,
    "the_destination": {
        "dest_structure": "the ArkParameterArmor instance's value array (22 u32 slots; pointer at instance+0x40; "
                          "allocated by FUN_0070d990 as descriptor_count(18)+4 slots via FUN_00412c50)",
        "dest_field": "SLOT 21 = value_array + 0x54",
        "field_index_derivation": "descriptor+8 = field index = tag + 4 (0x11 + 4 = 0x15 = 21; formula pinned @0x70CBF6; "
                                  "stored @0x75F5D7; loaded @0x726A0E)",
        "dest_address_derivation": "LEA ECX,[EDX+ECX*4] @0x726A14: value_array + 21*4 = value_array + 0x54 (84)",
        "width": 4,
        "width_proof": "the selected reader's dword load (8B 04 10 @0x977807) and dword store (89 02 @0x977810)",
        "the_selected_store": {"va": "0x00977810", "bytes": "89 02",
                               "role": "MOV [EDX],EAX with EDX = the slot-21 address passed from FUN_00726900 -> "
                                       "FUN_0075f660's virtual branch -> the reader's arg2"},
        "scope_discipline": "DEST_FIELD_IDENTIFIED=YES is strictly separate from DOWNSTREAM_CONSUMER_IDENTIFIED=NO "
                            "(the slot is not itself the gameplay consumer; the downstream reader of slot 21 was not identified)",
    },
    "destination_chain_summary": [
        "1. FUN_00726900 loads the field index from descriptor+8 (@0x726A0E; = tag+4 = 21 for tag 0x11).",
        "2. FUN_00726900 loads the value-array pointer from instance+0x40 (@0x726A11).",
        "3. FUN_00726900 computes dest = value_array + field_index*4 (@0x726A14) = value_array + 0x54 (slot 21).",
        "4. dest is pushed as arg2 of FUN_0075f660 (@0x726A17) with the cursor as arg1 (@0x726A18).",
        "5. FUN_0075f660's VIRTUAL branch (selected for tag 17; see BRANCH_SELECTION_TRACE.json) loads the dest "
        "(@0x75F670) and pushes it for the virtual call (@0x75F679).",
        "6. The selected reader FUN_009777F0 loads the dest from its arg2 (@0x97780A) and stores the 4-byte value "
        "into it (@0x977810, 89 02) - THE SELECTED STORE.",
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
print("t_dispatch=0x%08X t_alloc=0x%08X" % (t_dispatch, t_alloc))
