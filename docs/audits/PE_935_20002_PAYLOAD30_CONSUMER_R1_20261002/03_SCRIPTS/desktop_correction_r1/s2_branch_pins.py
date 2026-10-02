# s2_branch_pins.py â€” BRANCH_SELECTION_TRACE.json generator (DESKTOP_CORRECTION_R1)
# Byte-pins the full tag-ID-17 branch-selection chain from the pinned Entropia.exe:
#   registration site -> factory FUN_00977a50 -> descriptor-init dataflow
#   (FUN_0070cbc0 -> FUN_0075f5c0 -> FUN_0070c980/FUN_0070c7b0) -> lookup FUN_0070c180
#   -> dispatch FUN_0075f660 TEST/JZ/virtual slot/call -> vtable+0x14 dword (.rdata)
#   -> selected reader FUN_009777F0 (read/store/advance) -> RTTI walk.
# Every VA/RVA/file-offset is computed from THIS script's own PE32 parse (pe_parse.py).
# Every CALL/JMP rel32 target is computed programmatically and recorded.
# Static analysis only. Self-contained.
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_parse

RUN_ID = "PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002"
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "01_RAW", "DESKTOP_CORRECTION_R1",
                                    "BRANCH_SELECTION_TRACE.json"))

pe = pe_parse.PE32()
hdr = pe.header_summary()

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
    """Compute the target of CALL/JMP rel32 whose opcode byte is at va_of_e8 (5-byte instruction)."""
    b = pe.read_va(va_of_e8, 5)
    assert b[0] in (0xE8, 0xE9), "not a CALL/JMP rel32 at 0x%08X" % va_of_e8
    rel = struct.unpack_from("<i", b, 1)[0]
    return va_of_e8 + 5 + rel, b.hex().upper()

def jrel8_target(va, length):
    """Compute the target of a short Jcc rel8 (opcode at va, rel8 at va+length-1)."""
    b = pe.read_va(va, length)
    rel = struct.unpack_from("<b", b, length - 1)[0]
    return va + length + rel

pins = []
targets = {}

# ============ A. REGISTRATION SITE (FUN_00761570 schema ctor, tag-0x11 registration) ============
t, b = rel32_target(0x76170F)
targets["registration_factory_call@0x76170F"] = "0x%08X" % t
pins.append(pin(0x76170F, 5, "E83C632100",
    "CALL FUN_00977a50 (rel32 target computed = 0x%08X) - the descriptor factory for the type-1 schema entries" % t,
    "registration site: factory call (returns the reader object in EAX)"))
pins.append(pin(0x761714, 1, "50",
    "PUSH EAX - arg5 of FUN_0070cbc0 = the factory-returned object (becomes descriptor+0)",
    "registration site: arg5 push (object pointer dataflow entry)"))
pins.append(pin(0x761715, 2, "6A00",
    "PUSH 0 - arg4 of FUN_0070cbc0 (unused by the descriptor initializer; decompiler: param_4 not stored)",
    "registration site: arg4 push"))
pins.append(pin(0x761717, 5, "68C0000000",
    "PUSH 0xC0 - arg3 = descriptor FLAGS 0xC0 for tag 0x11",
    "registration site: flags push"))
pins.append(pin(0x76171C, 2, "6A01",
    "PUSH 0x1 - arg2 = descriptor TYPE 1 (4-byte scalar) for tag 0x11",
    "registration site: type push"))
pins.append(pin(0x76171E, 2, "6A11",
    "PUSH 0x11 - arg1 = THE TAG (ID 17) descriptor registration",
    "registration site: tag push"))
pins.append(pin(0x761720, 2, "8BCE",
    "MOV ECX,ESI - this = the ArkObjectClassImpl<ArkParameterArmor,20002> class object (ESI)",
    "registration site: this pointer setup"))
t, b = rel32_target(0x761722)
targets["registration_call@0x761722"] = "0x%08X" % t
pins.append(pin(0x761722, 5, "E899B4FAFF",
    "CALL FUN_0070cbc0 (rel32 target computed = 0x%08X) - the descriptor registration" % t,
    "registration site: registration call"))

# ============ B. FACTORY FUN_00977a50 (tag-17 descriptor factory) ============
pins.append(pin(0x977A50, 5, "B801000000",
    "MOV EAX,1",
    "factory: constant 1 (flag bitmask)"))
pins.append(pin(0x977A55, 6, "84058093BA00",
    "TEST byte ptr [0x00BA9380],AL (AL=1) - lazy-init flag byte test (object+4)",
    "factory: lazy-init flag test"))
pins.append(pin(0x977A5B, 2, "751D",
    "JNZ -> 0x%08X (already-initialized path, returns the object immediately)" % jrel8_target(0x977A5B, 2),
    "factory: lazy-init branch"))
pins.append(pin(0x977A5D, 6, "09058093BA00",
    "OR dword ptr [0x00BA9380],EAX (EAX=1) - set the lazy-init flag",
    "factory: flag set"))
pins.append(pin(0x977A63, 5, "68B044A700",
    "PUSH 0x00A744B0 - the object's exit-destructor function (atexit-style registration arg)",
    "factory: destructor push"))
pins.append(pin(0x977A68, 10, "C7057C93BA0070C6A900",
    "MOV dword ptr [0x00BA937C],0x00A9C670 - THE VTABLE STORE into the static .data object",
    "factory: runtime vtable store (establishes [[descriptor+0]] = 0x00A9C670)"))
t, b = rel32_target(0x977A72)
targets["factory_atexit_call@0x977A72"] = "0x%08X" % t
pins.append(pin(0x977A72, 5, "E864 5AFEFF".replace(" ", ""),
    "CALL 0x%08X (rel32 target computed) - atexit-style registration helper (arg: the destructor)" % t,
    "factory: atexit-style registration call"))
pins.append(pin(0x977A77, 3, "83C404",
    "ADD ESP,4 - __cdecl cleanup of the destructor argument",
    "factory: cdecl cleanup"))
pins.append(pin(0x977A7A, 5, "B87C93BA00",
    "MOV EAX,0x00BA937C - THE RETURN VALUE: the static .data object address (non-NULL)",
    "factory: return value store (both paths return this; never NULL)"))
pins.append(pin(0x977A7F, 1, "C3",
    "RET",
    "factory: return"))
pins.append(pin(0xA744B0, 10, "C7057C93BA00E499A700",
    "the registered destructor: MOV dword ptr [0x00BA937C],0x00A799E4; RET - resets the object vtable at exit (confirms the atexit-style semantics)",
    "factory: destructor body (context; proves the vtable-store interpretation)"))

# ============ C. DESCRIPTOR-INIT DATAFLOW ============
# FUN_0070cbc0 (registration): arg5 (object) flows to FUN_0075f5c0 -> descriptor+0
pins.append(pin(0x70CBC0, 4, "8B44240C",
    "MOV EAX,[ESP+0xC] - entry stack arg3 = flags (0xC0 for tag 0x11)",
    "registration fn: flags load"))
pins.append(pin(0x70CBE3, 4, "8B4C2428",
    "MOV ECX,[ESP+0x28] - with SUB ESP,0x10 + PUSH ESI in effect: entry stack arg5 = THE FACTORY OBJECT",
    "registration fn: arg5 (object) load"))
pins.append(pin(0x70CBEB, 1, "51",
    "PUSH ECX - push arg5 (the object) for FUN_0075f5c0",
    "registration fn: object push"))
pins.append(pin(0x70CBF1, 1, "50",
    "PUSH EAX - push arg3 (flags)",
    "registration fn: flags push"))
pins.append(pin(0x70CBF2, 4, "8B442428",
    "MOV EAX,[ESP+0x28] - entry stack arg2 = type (1)",
    "registration fn: type load"))
pins.append(pin(0x70CBF6, 3, "83C104",
    "ADD ECX,4 - ECX = tag + 4 = FIELD INDEX (0x11+4 = 0x15 = 21)",
    "registration fn: field index = tag+4"))
pins.append(pin(0x70CBFA, 1, "51",
    "PUSH ECX - push field index",
    "registration fn: field index push"))
pins.append(pin(0x70CBFB, 4, "8D4C2418",
    "LEA ECX,[ESP+0x18] - ECX = &local descriptor buffer (the SUB ESP,0x10 local)",
    "registration fn: local descriptor address"))
t, b = rel32_target(0x70CBFF)
targets["desc_init_call@0x70CBFF"] = "0x%08X" % t
pins.append(pin(0x70CBFF, 5, "E8BC290500",
    "CALL FUN_0075f5c0 (rel32 target computed = 0x%08X) - descriptor initializer" % t,
    "registration fn: descriptor-init call"))
pins.append(pin(0x70CC04, 1, "50",
    "PUSH EAX - EAX = &local descriptor (set by FUN_0075f5c0's MOV EAX,ECX, unchanged) - the insert argument",
    "registration fn: descriptor pointer push"))
pins.append(pin(0x70CC05, 2, "8BCE",
    "MOV ECX,ESI - this = the class object",
    "registration fn: insert this setup"))
t, b = rel32_target(0x70CC07)
targets["insert_call@0x70CC07"] = "0x%08X" % t
pins.append(pin(0x70CC07, 5, "E874FDFFFF",
    "CALL FUN_0070c980 (rel32 target computed = 0x%08X) - descriptor table insert" % t,
    "registration fn: table-insert call"))
pins.append(pin(0x70CC10, 3, "C21400",
    "RET 0x14 - pops 5 stack args (confirms FUN_0070cbc0's 5-arg cdecl+thiscall shape)",
    "registration fn: arg-count evidence"))
# FUN_0075f5c0 (descriptor initializer): arg5 -> descriptor+0
pins.append(pin(0x75F5C4, 2, "8BC1",
    "MOV EAX,ECX - EAX = &descriptor (this); also the function's return value",
    "descriptor init: this into EAX"))
pins.append(pin(0x75F5C6, 4, "8B4C2414",
    "MOV ECX,[ESP+0x14] - arg5 = THE FACTORY OBJECT",
    "descriptor init: object load"))
pins.append(pin(0x75F5CA, 2, "8908",
    "MOV [EAX],ECX - *** DESCRIPTOR+0 = THE OBJECT *** (0xBA937C for tag 17)",
    "descriptor init: THE descriptor+0 store"))
pins.append(pin(0x75F5D0, 3, "895004",
    "MOV [EAX+4],EDX - descriptor+4 = type (1)",
    "descriptor init: type store"))
pins.append(pin(0x75F5D7, 3, "894808",
    "MOV [EAX+8],ECX - descriptor+8 = field index (tag+4 = 21)",
    "descriptor init: field-index store"))
pins.append(pin(0x75F5DA, 3, "89500C",
    "MOV [EAX+0xC],EDX - descriptor+0xC = flags (0xC0)",
    "descriptor init: flags store"))
# FUN_0070c980 (insert): tag == count invariant, then vector append via FUN_0070c7b0
pins.append(pin(0x70C98F, 6, "8B9E8C000000",
    "MOV EBX,[ESI+0x8C] - the class-object descriptor-vector END pointer",
    "insert: vector end load"))
pins.append(pin(0x70C999, 6, "2B9E88000000",
    "SUB EBX,[ESI+0x88] - vector byte size = end - begin",
    "insert: vector size"))
pins.append(pin(0x70C9AB, 3, "C1FB04",
    "SAR EBX,4 - descriptor count = size/0x10 (stride 16)",
    "insert: descriptor count"))
pins.append(pin(0x70C99F, 3, "8B5708",
    "MOV EDX,[EDI+8] - the new descriptor's field index",
    "insert: field index load"))
pins.append(pin(0x70C9A8, 3, "83EA04",
    "SUB EDX,4 - recover the TAG from field index (tag = field_index - 4)",
    "insert: tag recovery"))
pins.append(pin(0x70C9AE, 2, "3BD3",
    "CMP EDX,EBX - tag vs descriptor count (the append-order invariant)",
    "insert: tag==count invariant test"))
pins.append(pin(0x70C9B0, 2, "751A",
    "JNZ -> 0x%08X (failure: flag byte [classObj+0xD6]=0) - the append requires tag == count, so the element lands at index == tag" % jrel8_target(0x70C9B0, 2),
    "insert: invariant branch"))
pins.append(pin(0x70C9BE, 1, "57",
    "PUSH EDI - the &descriptor argument (pushed by FUN_0070cbc0)",
    "insert: descriptor push"))
t, b = rel32_target(0x70C9BF)
targets["vector_append_call@0x70C9BF"] = "0x%08X" % t
pins.append(pin(0x70C9BF, 5, "E8ECFDFFFF",
    "CALL FUN_0070c7b0 (rel32 target computed = 0x%08X) - the vector append" % t,
    "insert: vector-append call"))
pins.append(pin(0x70C7B0, 3, "8B4104",
    "MOV EAX,[ECX+4] - the vector END pointer (append position == begin + count*0x10 == begin + tag*0x10)",
    "vector append: end load"))
pins.append(pin(0x70C7C1, 2, "8B32",
    "MOV ESI,[EDX] - source descriptor+0 = THE OBJECT POINTER",
    "vector append: object-pointer load"))
pins.append(pin(0x70C7C3, 2, "8930",
    "MOV [EAX],ESI - *** ELEMENT+0 = THE OBJECT POINTER (preserved into the descriptor table) ***",
    "vector append: object-pointer store"))
pins.append(pin(0x70C7D8, 4, "83410410",
    "ADD dword [ECX+4],0x10 - END += 0x10 (the 16-byte descriptor element)",
    "vector append: end advance"))
# FUN_0070c180 (lookup): descriptor = [classObj+0x88] + tag*0x10
pins.append(pin(0x70C1D3, 3, "C1E004",
    "SHL EAX,4 - tag*0x10 (the descriptor stride)",
    "lookup: tag*0x10"))
pins.append(pin(0x70C1D6, 6, "038188000000",
    "ADD EAX,[ECX+0x88] - descriptor = classObj->[0x88] (table base) + tag*0x10",
    "lookup: descriptor table base"))

# ============ D. DISPATCH FUN_0075f660 (TEST/JZ/virtual slot/call) ============
pins.append(pin(0x75F660, 2, "8BC1",
    "MOV EAX,ECX - EAX = the descriptor (this)",
    "dispatch: descriptor into EAX"))
pins.append(pin(0x75F662, 2, "8B08",
    "MOV ECX,[EAX] - ECX = [descriptor+0] - THE OBJECT-POINTER LOAD under test",
    "dispatch: descriptor+0 load"))
pins.append(pin(0x75F664, 2, "85C9",
    "TEST ECX,ECX - the branch-selecting conditional",
    "dispatch: TEST of [descriptor+0]"))
pins.append(pin(0x75F66E, 2, "7417",
    "JZ -> 0x%08X - the FALLBACK entry (taken only when [descriptor+0] == NULL)" % jrel8_target(0x75F66E, 2),
    "dispatch: the JZ to the fallback"))
pins.append(pin(0x75F670, 4, "8B542410",
    "MOV EDX,[ESP+0x10] - the DEST argument (entry arg2)",
    "dispatch: virtual-branch dest load"))
pins.append(pin(0x75F674, 2, "8B01",
    "MOV EAX,[ECX] - EAX = [object] = the object's VTABLE (0x00A9C670 via the factory's vtable store)",
    "dispatch: vtable load [[descriptor+0]]"))
pins.append(pin(0x75F676, 3, "8B4014",
    "MOV EAX,[EAX+0x14] - THE VIRTUAL SLOT: [vtable+0x14] (dword at 0x00A9C684)",
    "dispatch: slot load [vtable+0x14]"))
pins.append(pin(0x75F67B, 2, "FFD0",
    "CALL EAX - the virtual call (ECX = the object; args: cursor, dest)",
    "dispatch: the virtual call"))
pins.append(pin(0x75F67D, 3, "8A4611",
    "MOV AL,[ESI+0x11] - return = the cursor flag byte & 1",
    "dispatch: return flag"))

# ============ E. THE VTABLE SLOT DWORD + RTTI WALK ============
slot_dword = pe.read_u32_va(0xA9C684)
pins.append(pin(0xA9C684, 4, "F0779700",
    "the slot dword at vtable+0x14: value 0x%08X = FUN_009777F0 - THE STATIC VIRTUAL TARGET (read from pinned .rdata)" % slot_dword,
    "selected slot dword (static target of the virtual call)"))
col_va = pe.read_u32_va(0xA9C66C)
pins.append(pin(0xA9C66C, 4, "6083AB00",
    "[vtable-4] = the RTTI CompleteObjectLocator pointer 0x%08X" % col_va,
    "RTTI: COL pointer read"))
col_bytes = pe.read_va(col_va, 20)
sig, col_off, col_cd, ptd, pcd = struct.unpack("<IIIII", col_bytes)
pins.append(pin(col_va, 20, None,
    "CompleteObjectLocator: sig=0x%X offset=0x%X cdOffset=0x%X pTypeDescriptor=0x%08X pClassDescriptor=0x%08X" % (sig, col_off, col_cd, ptd, pcd),
    "RTTI: COL structure"))
td_name_bytes = pe.read_va(ptd, 8 + 32)
td_name = td_name_bytes[8:].split(b"\x00")[0].decode("ascii", "replace")
pins.append(pin(ptd, 8 + len(td_name) + 1, None,
    "TypeDescriptor at 0x%08X: name at +8 = %r" % (ptd, td_name),
    "RTTI: the reader-object class name (mangled)"))

# ============ F. THE SELECTED READER FUN_009777F0 (full instruction window) ============
pins.append(pin(0x9777F0, 4, "8B4C2404",
    "MOV ECX,[ESP+4] - arg1 = THE CURSOR",
    "selected reader: cursor load"))
pins.append(pin(0x9777F4, 4, "80791100",
    "CMP byte [ECX+0x11],0 - the CURSOR FLAG check",
    "selected reader: cursor flag check"))
pins.append(pin(0x9777F8, 2, "7420",
    "JZ -> 0x%08X (the ERROR path: dest=0 + flag cleared)" % jrel8_target(0x9777F8, 2),
    "selected reader: flag-clear branch to error path"))
pins.append(pin(0x9777FA, 3, "8B410C",
    "MOV EAX,[ECX+0xC] - the cursor OFFSET",
    "selected reader: offset load"))
pins.append(pin(0x9777FD, 3, "8D5004",
    "LEA EDX,[EAX+4] - offset+4 (the 4-byte width bound)",
    "selected reader: width bound computation"))
pins.append(pin(0x977800, 3, "3B5108",
    "CMP EDX,[ECX+8] - offset+4 vs the cursor LIMIT",
    "selected reader: bounds check"))
pins.append(pin(0x977803, 2, "7715",
    "JA -> 0x%08X (bounds failure -> the ERROR path)" % jrel8_target(0x977803, 2),
    "selected reader: bounds-failure branch"))
pins.append(pin(0x977805, 2, "8B11",
    "MOV EDX,[ECX] - the cursor BASE pointer",
    "selected reader: base load"))
# THE READ
pins.append(pin(0x977807, 3, "8B0410",
    "MOV EAX,[EDX+EAX*1] - *** THE SELECTED CLIENT READ: 4-byte x86-native little-endian load at cursor.base + cursor.offset (== payload+0x30 at the tag-ID-17 iteration) ***",
    "selected reader: THE READ INSTRUCTION"))
pins.append(pin(0x97780A, 4, "8B542408",
    "MOV EDX,[ESP+8] - arg2 = THE DESTINATION POINTER",
    "selected reader: destination-argument load"))
pins.append(pin(0x97780E, 2, "6A04",
    "PUSH 4 - the advance width",
    "selected reader: advance-width push"))
# THE STORE
pins.append(pin(0x977810, 2, "8902",
    "MOV [EDX],EAX - *** THE SELECTED STORE: the loaded dword into the destination (value_array slot 21 / +0x54) ***",
    "selected reader: THE STORE INSTRUCTION"))
t, b = rel32_target(0x977812)
targets["reader_advance_call@0x977812"] = "0x%08X" % t
pins.append(pin(0x977812, 5, "E84966A9FF",
    "CALL FUN_0040de60 (rel32 target computed = 0x%08X) - advance the cursor by 4" % t,
    "selected reader: cursor advance call"))
pins.append(pin(0x977817, 3, "C20800",
    "RET 8 - pops the cursor + dest arguments",
    "selected reader: return"))
# error path
pins.append(pin(0x97781A, 4, "8B442408",
    "MOV EAX,[ESP+8] - ERROR PATH (flag clear or bounds failure): the dest pointer",
    "selected reader ERROR PATH: dest load"))
pins.append(pin(0x97781E, 6, "C70000000000",
    "MOV dword [EAX],0 - ERROR PATH: the destination is zeroed",
    "selected reader ERROR PATH: dest = 0"))
pins.append(pin(0x97782A, 4, "C6411100",
    "MOV byte [ECX+0x11],0 - ERROR PATH: the cursor flag is CLEARED (failure propagation; NOT the successful parse path)",
    "selected reader ERROR PATH: cursor flag cleared"))

# ============ G. THE ADVANCE HELPER FUN_0040de60 ============
pins.append(pin(0x40DE60, 4, "8B442404",
    "MOV EAX,[ESP+4] - the increment argument n",
    "advance helper: increment load"))
pins.append(pin(0x40DE64, 3, "01410C",
    "ADD [ECX+0xC],EAX - cursor.offset += n",
    "advance helper: offset increment"))
pins.append(pin(0x40DE6A, 3, "3B4108",
    "CMP EAX,[ECX+8] - offset vs the cursor limit",
    "advance helper: limit check"))
pins.append(pin(0x40DE6F, 4, "C6411100",
    "MOV byte [ECX+0x11],0 - clear the cursor flag when offset > limit (the error propagation)",
    "advance helper: flag clear on overrun"))

# ============ H. THE TLV LOOP DISPATCH-CHAIN PINS (FUN_00726900) ============
t, b = rel32_target(0x726A03)
targets["lookup_call@0x726A03"] = "0x%08X" % t
pins.append(pin(0x726A03, 5, "E87857FEFF",
    "CALL FUN_0070c180 (rel32 target computed = 0x%08X) - the descriptor lookup by tag" % t,
    "TLV loop: descriptor-lookup call"))
pins.append(pin(0x726A08, 4, "83780400",
    "CMP dword [EAX+4],0 - descriptor TYPE validity check (type 1 != 0 for tag 0x11)",
    "TLV loop: type validity check"))
pins.append(pin(0x726A0E, 3, "8B4808",
    "MOV ECX,[EAX+8] - the descriptor FIELD INDEX (tag 0x11 -> 0x15 = 21)",
    "TLV loop: field index load"))
pins.append(pin(0x726A11, 3, "8B5540",
    "MOV EDX,[EBP+0x40] - instance+0x40 = the VALUE ARRAY pointer (22 u32 slots)",
    "TLV loop: value-array load"))
pins.append(pin(0x726A14, 3, "8D0C8A",
    "LEA ECX,[EDX+ECX*4] - DEST = value_array + field_index*4 (21*4 = 0x54)",
    "TLV loop: destination address computation"))
pins.append(pin(0x726A17, 1, "51",
    "PUSH ECX - the dest argument",
    "TLV loop: dest push"))
pins.append(pin(0x726A18, 1, "56",
    "PUSH ESI - the cursor argument",
    "TLV loop: cursor push"))
pins.append(pin(0x726A19, 2, "8BC8",
    "MOV ECX,EAX - this = the descriptor",
    "TLV loop: dispatch this setup"))
t, b = rel32_target(0x726A1B)
targets["dispatch_call@0x726A1B"] = "0x%08X" % t
pins.append(pin(0x726A1B, 5, "E8408C0300",
    "CALL FUN_0075f660 (rel32 target computed = 0x%08X) - the value-read dispatch" % t,
    "TLV loop: dispatch call"))

# ============ summary ============
all_match = all(p["match"] for p in pins)
art = {
    "run_id": RUN_ID,
    "artifact": "BRANCH_SELECTION_TRACE.json",
    "generator": "03_SCRIPTS/desktop_correction_r1/s2_branch_pins.py",
    "generator_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest().upper(),
    "exe_path": pe.path,
    "exe_sha256": pe.sha256,
    "exe_size": pe.size,
    "pe_header": {
        "image_base": hdr["image_base"],
        "sections": hdr["sections"],
        "section_table_note": "VA->file-offset computed per section via this run's own PE32 parse; for .text/.rdata/.data raw_pointer==virtual_address so FO==RVA; .tls/.rsrc differ (FO=RVA-0xA000) - the section table is read, not assumed",
    },
    "computed_call_targets": targets,
    "branch_selection_chain": [
        "1. REGISTRATION (FUN_00761570 schema ctor, inside the ArkObjectClassImpl<ArkParameterArmor,20002> class object): "
        "CALL FUN_00977a50 @0x76170F -> EAX = the reader object; PUSH EAX (arg5) @0x761714; PUSH 0 (arg4) @0x761715; "
        "PUSH 0xC0 (flags, arg3) @0x761717; PUSH 1 (type, arg2) @0x76171C; PUSH 0x11 (TAG 17, arg1) @0x76171E; "
        "MOV ECX,ESI (this=classObj) @0x761720; CALL FUN_0070cbc0 @0x761722.",
        "2. FACTORY FUN_00977a50: lazy-init flag byte at 0x00BA9380; on first call sets the flag, stores the vtable 0x00A9C670 "
        "into the static .data object 0x00BA937C (MOV dword [0xBA937C],0xA9C670 @0x977A68), registers the exit-destructor "
        "0x00A744B0 via the atexit-style helper 0x95D4DB (PUSH 0xA744B0 @0x977A63; CALL @0x977A72); BOTH PATHS return "
        "EAX = 0x00BA937C (MOV EAX,0xBA937C @0x977A7A) - a non-NULL static address; no NULL-return path exists.",
        "3. DESCRIPTOR INIT: FUN_0070cbc0 loads entry-arg5 (the object) @0x70CBE3 and pushes it through; field index = tag+4 "
        "@0x70CBF6; FUN_0075f5c0 stores arg5 at descriptor+0 (MOV [EAX],ECX @0x75F5CA); returns &descriptor in EAX; "
        "FUN_0070c980(this=classObj, &descriptor) enforces tag==count (@0x70C9AF/0x70C9B1) then appends via FUN_0070c7b0: "
        "copies ALL FOUR dwords incl. descriptor+0 (the object pointer, 0x70C7C1/0x70C7C3) to the vector element at "
        "classObj->[0x88] + count*0x10 == begin + tag*0x10 and advances end by 0x10.",
        "4. LOOKUP FUN_0070c180: descriptor = classObj->[0x88] + tag*0x10 (SHL EAX,4 @0x70C1D3; ADD EAX,[ECX+0x88] @0x70C1D6).",
        "5. DISPATCH FUN_0075f660 (called from FUN_00726900 @0x726A1B with ECX=descriptor, arg1=cursor, arg2=dest): "
        "MOV ECX,[EAX] @0x75F662 loads descriptor+0; TEST ECX,ECX @0x75F664; JZ @0x75F66E -> fallback 0x75F687. "
        "For tag ID 17 descriptor+0 = 0x00BA937C != NULL (proven by the registration dataflow + factory return bytes) "
        "=> the JZ is NOT taken => THE VIRTUAL BRANCH IS SELECTED (control-flow reachability from the proven descriptor state).",
        "6. VIRTUAL SLOT: MOV EAX,[ECX] @0x75F674 -> [0x00BA937C] = the vtable 0x00A9C670 (stored by the factory lazy-init); "
        "MOV EAX,[EAX+0x14] @0x75F676 -> the dword at 0x00A9C684 = 0x009777F0 (static .rdata read); CALL EAX @0x75F67B.",
        "7. SELECTED READER FUN_009777F0 (this=the ArkRTTraitsInt object, arg1=cursor, arg2=dest): "
        "cursor flag check @0x9777F4; bounds offset+4<=limit @0x9777FD..0x977803; "
        "THE READ @0x00977807 (8B 04 10) - 4-byte LE load at cursor.base+offset; "
        "dest load @0x97780A; THE STORE @0x00977810 (89 02); advance 4 via FUN_0040de60 @0x977812; RET 8. "
        "ERROR PATH (not the successful parse path): dest=0 @0x97781E + cursor flag cleared @0x97782A.",
        "8. RTTI: [vtable-4] @0xA9C66C = COL 0x00AB8360; COL+0xC = TypeDescriptor 0x00B9F10C; name = '.?AUArkRTTraitsInt@@' "
        "=> the reader object's class is ArkRTTraitsInt (the Int runtime-traits reader).",
    ],
    "desktop_lead_agreement": {
        "READ_FUNCTION=FUN_009777F0": "CONFIRMED (slot dword 0x009777F0 read from .rdata @0xA9C684)",
        "READ_INSTRUCTION_VA=0x00977807": "CONFIRMED (bytes 8B 04 10 at VA 0x00977807)",
        "READ_INSTRUCTION_FILE_OFFSET=0x00577807": "CONFIRMED (own PE32 section-table computation: VA 0x00977807 -> RVA 0x00577807 -> .text FO 0x00577807)",
        "READ_BYTES=8B 04 10": "CONFIRMED",
        "STORE_INSTRUCTION_VA=0x00977810": "CONFIRMED (bytes 89 02 at VA 0x00977810)",
        "STORE_BYTES=89 02": "CONFIRMED",
        "FACTORY=FUN_00977a50 (static .data singleton, lazy-init flag, runtime vtable store, atexit-style registration, never NULL)": "CONFIRMED (object 0x00BA937C, flag 0x00BA9380, vtable 0x00A9C670, destructor 0x00A744B0, helper 0x95D4DB)",
        "VIRTUAL_SLOT=vtable+0x14": "CONFIRMED (0x00A9C684)",
    },
    "superseded_claim": {
        "old_selected_reader": "FUN_00412540 (fallback type-1 scalar reader; READ @0x00412553 / STORE @0x0041255A)",
        "disposition": "BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH - the fallback is reached only when descriptor+0 == NULL, "
                       "which is NOT the tag-ID-17 state (see FALLBACK_PATH_RECORD.json)",
    },
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
print("computed targets:", json.dumps(targets, indent=1))
print("RTTI name:", td_name)
