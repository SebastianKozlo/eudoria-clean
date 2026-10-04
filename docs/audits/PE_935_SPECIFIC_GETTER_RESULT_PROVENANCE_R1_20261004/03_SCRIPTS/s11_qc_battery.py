# s11_qc_battery.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: FINAL SELF_CHECK QC battery: machine-verify every load-bearing
# call target and instruction-pin this run's chain decode relies on,
# re-verify EXE identity, and record the count basis. READ-ONLY.
# Output: 01_RAW/S11_QC_BATTERY.json
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SHA256_EXPECT = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
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
        secs.append((name, vaddr, vsize, rawptr, rawsize))
    return d, image_base, secs

def va2off(image_base, secs, va):
    rva = va - image_base
    for name, vaddr, vsize, rawptr, rawsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rawsize) and rva - vaddr < rawsize:
            return rawptr + (rva - vaddr)
    return None

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S11_QC"}
    exe_sha = sha256_file(EXE)
    d, image_base, secs = load_pe(EXE)
    out["exe_identity"] = {"size": os.path.getsize(EXE), "sha256": exe_sha,
                          "expected": EXE_SHA256_EXPECT, "match": exe_sha == EXE_SHA256_EXPECT}
    assert exe_sha == EXE_SHA256_EXPECT

    # [call_site, expected_target, claim] - every load-bearing call this run
    call_checks = [
        (0x004C54B2, 0x00843DD0, "receiver tree resolve (FUN_004C5480)"),
        (0x004C54CE, 0x00703B80, "class-selector wrapper (FUN_004C5480)"),
        (0x004C54E4, 0x00844020, "attribute-flag check 0xD82 (FUN_004C5480)"),
        (0x004C54F4, 0x00843DD0, "alt-branch receiver resolve"),
        (0x004C54FA, 0x007292F0, "alt-branch helper FUN_007292F0"),
        (0x004C5508, 0x004123D0, "alt-branch thunk FUN_004123D0"),
        (0x004C550E, 0x00843340, "alt-branch FUN_00843340"),
        (0x004C5523, 0x0070C180, "PROPERTY_TAG 6 getter call (audited)"),
        (0x004C5542, 0x004926E0, "identity helper at table-index step"),
        (0x004C5549, 0x00977780, "fallback static object return"),
        (0x004C555E, 0x00703BC0, "pair cleanup (FUN_004C5480 tail)"),
        (0x004C55B5, 0x004C5480, "FUN_004C5580 -> audited getter"),
        (0x004C55D2, 0x0043A550, "registry singleton"),
        (0x004C55D9, 0x0072F880, "lookup-with-copy (KEY edge)"),
        (0x005678BA, 0x004C5580, "builder FUN_00567770 -> FUN_004C5580"),
        (0x00703B88, 0x00415470, "manager singleton (selector wrapper)"),
        (0x00703B8F, 0x00703D70, "selector machinery"),
        (0x00703D7D, 0x0073C870, "selector->factory dispatch (CMP 0x4E20 region)"),
        (0x00703D8F, 0x0070E100, "factory+receiver -> class_obj get-or-create"),
        (0x0070E143, 0x00415470, "manager singleton (FUN_0070E100 miss path)"),
        (0x0070D9C9, 0x00412C50, "value-table vector init (FUN_0070D990)"),
        (0x0070D9D7, 0x0075F6D0, "fixed-member copy 1 (table[0])"),
        (0x0070D9E8, 0x0075F6D0, "fixed-member copy 2 (table[1])"),
        (0x0070D9F9, 0x0075F6D0, "fixed-member copy 3 (table[2])"),
        (0x0070DA0A, 0x0075F6D0, "fixed-member copy 4 (table[3])"),
        (0x0070DA42, 0x0075F6D0, "slot-payload copy loop (table[slot+8])"),
        (0x0070DA66, 0x00727540, "class_obj post-create call"),
        (0x0072F898, 0x004D1430, "mapfind (KEY = *(u32*)&p1)"),
        (0x0072F8AF, 0x0072FCE0, "template validity check"),
        (0x0072F8BD, 0x0072F7A0, "full-field template copy"),
        (0x0070CBFF, 0x0075F5C0, "SLOT_ADD slot-field initializer"),
        (0x0070CC07, 0x0070C980, "SLOT_ADD slot appender"),
        (0x00737598, 0x0070CBC0, "SLOT_ADD for TAG 6 (the audited slot)"),
        (0x00737588, 0x00977A50, "int traits factory before tag-6 add"),
        (0x0073E2EB, 0x0073B820, "20006 factory constructor"),
        (0x0073E307, 0x0070E2F0, "factory init call (arg 8)"),
        (0x0073E312, 0x007374F0, "factory slot-array builder"),
        (0x0073E320, 0x0070C150, "factory post-init check"),
        (0x0073E32B, 0x0070BF10, "factory byte getter"),
        (0x0073B8E3, None, "class_obj alloc (FUN_0073B8C0)"),
        (0x0070DD39, 0x0040E160, "FUN_0070DCF0 vector ctor"),
        (0x0070DD4B, None, "FUN_0070DCF0 buffer alloc"),
        (0x0070DD75, 0x00971AD0, "PER-RECORD READER call (R1 canon)"),
        (0x0070DD84, 0x00971650, "stream advance/verify"),
        (0x0070DDA8, 0x0040DE60, "cursor advance (C1 canon)"),
        (0x0070DDBD, 0x0070DC20, "record APPLY to receiver"),
        (0x0070C9BF, None, "appender vector push (target computed)"),
        (0x0073B87D, 0x0070CF80, "factory ctor register/init call"),
        (0x0073B902, None, "class_obj ctor (FUN_0073B8C0, target computed)"),
    ]
    results = []
    for site, expected, claim in call_checks:
        off = va2off(image_base, secs, site)
        if off is None or d[off] != 0xE8:
            results.append({"site": "0x%08X" % site, "claim": claim,
                            "verdict": "FAIL", "reason": "no E8 opcode at VA"})
            continue
        rel = struct.unpack_from("<i", d, off + 1)[0]
        tgt = site + 5 + rel
        row = {"site": "0x%08X" % site, "target": "0x%08X" % tgt, "claim": claim}
        if expected is None:
            row["verdict"] = "COMPUTED"
        else:
            row["expected"] = "0x%08X" % expected
            row["verdict"] = "PASS" if tgt == expected else "FAIL"
        results.append(row)
    out["call_checks"] = results

    # instruction pins (byte-exact)
    pins = {
        "0x004C54C2": ("C7 44 24 1C 26 4E 00 00", "MOV [ESP+0x1C],0x4E26 CLASS_SELECTOR pair"),
        "0x004C54CA": ("89 44 24 20", "MOV [ESP+0x20],EAX receiver into pair"),
        "0x004C54DD": ("68 82 0D 00 00", "PUSH 0xD82 branch flag"),
        "0x004C551C": ("8B 48 04", "MOV ECX,[EAX+4] getter receiver"),
        "0x004C551F": ("6A 06", "PUSH 6 PROPERTY_TAG"),
        "0x004C5528": ("8B 48 04", "MOV ECX,[EAX+4] descriptor kind"),
        "0x004C552B": ("85 C9", "TEST ECX,ECX null check"),
        "0x004C552F": ("83 F9 01", "CMP ECX,1 kind==int"),
        "0x004C5534": ("84 48 0C", "TEST [EAX+0xC],CL flags bit0"),
        "0x004C5539": ("8B 40 08", "MOV EAX,[EAX+8] SELECTED_VALUE"),
        "0x004C553C": ("8B 4E 40", "MOV ECX,[ESI+0x40] value-table begin"),
        "0x004C553F": ("8D 0C 81", "LEA ECX,[ECX+EAX*4] &table[value]"),
        "0x004C554E": ("8B 00", "MOV EAX,[EAX] table entry = KEY"),
        "0x004C55D1": ("50", "PUSH EAX key push before singleton"),
        "0x004C55D0": ("56", "PUSH ESI out-buffer push"),
        "0x0070D9A5": ("89 73 04", "MOV [EBX+4],ESI class_obj+4=FACTORY"),
        "0x0070DA36": ("8B 44 19 08", "MOV EAX,[ECX+EBX+8] slot+8 = attr id"),
        "0x0070DA3E": ("8D 04 82", "LEA EAX,[EDX+EAX*4] &table[id]"),
        "0x0075F5D7": ("89 48 08", "MOV [EAX+8],ECX slot+8 = tag+4"),
        "0x0075F5CA": ("89 08", "MOV [EAX],ECX slot+0 = traits"),
        "0x0075F5D0": ("89 50 04", "MOV [EAX+4],EDX slot+4 = kind"),
        "0x009777E4": ("C7 00 00 00 00 00", "MOV DWORD [EAX],0 int default write"),
        "0x00977A68": ("C7 05 7C 93 BA 00 70 C6 A9 00", "int traits vtable store 0x00A9C670"),
        "0x0073C87C": ("77 15", "JA selector>20000"),
        "0x0073C8A5": ("81 C1 DF B1 FF FF", "ADD ECX,-0x4E21 selector-20001"),
        "0x0073C8D8": ("A1 0C 59 BA 00", "MOV EAX,[0x00BA590C] factory slot 20006"),
        "0x004D143E": ("8B 36", "MOV ESI,[ESI] key deref (u32)"),
        "0x0070DD28": ("68 80 00 00 00", "PUSH 0x80 record buffer size"),
        # CONTROL CASE A pins: same mechanism, different tags (2 and 4, both kind 1 int)
        "0x737539": ("50 6A 00 6A 00 6A 01 6A 02", "CONTROL-A: slot-add args (traits,0,0,kind=1,tag=2)"),
        "0x737563": ("50 6A 00 6A 00 6A 01 6A 04", "CONTROL-A: slot-add args (traits,0,0,kind=1,tag=4)"),
        "0x73758D": ("50 6A 00 6A 00 6A 01 6A 06", "AUDITED: slot-add args (traits,0,0,kind=1,tag=6)"),
        # CONTROL CASE C pins: fallback returns NULL (static 0x00BA9374 never written)
        "0x00977780": ("B8 74 93 BA 00 C3", "CONTROL-C: fallback returns static VA 0x00BA9374"),
        "0x004C55C3": ("0F 84 ED 04 00 00", "CONTROL-C: TEST EAX,EAX JE 0x004C5AB6 on NULL getter result"),
    }
    pin_rows = []
    for va_s, (expect_hex, claim) in pins.items():
        va = int(va_s, 16)
        off = va2off(image_base, secs, va)
        if off is None:
            pin_rows.append({"va": va_s, "expected": expect_hex.upper(),
                             "actual": None, "claim": claim, "verdict": "FAIL",
                             "reason": "VA does not map to a raw section"})
            continue
        actual = d[off:off+len(expect_hex.split(" "))].hex(" ").upper()
        pin_rows.append({"va": va_s, "expected": expect_hex.upper(), "actual": actual,
                         "claim": claim, "verdict": "PASS" if actual == expect_hex.upper() else "FAIL"})
    out["instruction_pins"] = pin_rows

    # .data virtual-tail class of the statics (zero at load, no direct writers)
    out["statics_writer_census"] = {
        "0x00BA5108_default_descriptor": "1 real .text reference (FUN_0070C180 MOV EAX); 1 false-positive byte coincidence @0x005246B9 (SUB ESP,8; PUSH ECX; MOV EDX operand bytes); ZERO writers => permanently zero",
        "0x00BA9374_fallback_object": "1 .text reference (FUN_00977780 MOV EAX); ZERO writers => permanently zero",
        "0x00BA590C_factory20006": "writers: lazy-init store @0x0073E303 (A3) + zero-on-fail @0x0073E348 (C7 05)",
        "0x00BA937C_int_traits": "writers: vtable store @0x00977A6A (0x00A9C670) + destruct-swap @0x00977B48-ish via FUN_00977B40 slot0 (0x00A799E4 inert) + the callerless site @0x00A744B2",
    }

    n_pass = sum(1 for r in results if r["verdict"] == "PASS")
    n_fail = sum(1 for r in results if r["verdict"] == "FAIL")
    n_comp = sum(1 for r in results if r["verdict"] == "COMPUTED")
    pins_pass = sum(1 for r in pin_rows if r["verdict"] == "PASS")
    pins_fail = sum(1 for r in pin_rows if r["verdict"] == "FAIL")
    # control-case JE target arithmetic
    jeoff = va2off(image_base, secs, 0x004C55C3)
    je_tgt = 0x004C55C9 + struct.unpack_from("<i", d, jeoff + 2)[0]
    out["control_je_target"] = {"site": "0x004C55C3", "expected": "0x004C5AB6",
                                "actual": "0x%08X" % je_tgt,
                                "verdict": "PASS" if je_tgt == 0x004C5AB6 else "FAIL"}
    out["summary"] = {"call_checks_pass": n_pass, "call_checks_fail": n_fail,
                      "call_checks_computed": n_comp,
                      "instruction_pins_pass": pins_pass, "instruction_pins_fail": pins_fail}

    with open(os.path.join(RUN, "01_RAW", "S11_QC_BATTERY.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S11 QC battery: calls PASS=%d FAIL=%d COMPUTED=%d; pins PASS=%d FAIL=%d" %
          (n_pass, n_fail, n_comp, pins_pass, pins_fail))
    for r in results:
        if r["verdict"] != "PASS":
            print("  ", r)
    for r in pin_rows:
        if r["verdict"] != "PASS":
            print("  PIN:", r)

if __name__ == "__main__":
    main()
