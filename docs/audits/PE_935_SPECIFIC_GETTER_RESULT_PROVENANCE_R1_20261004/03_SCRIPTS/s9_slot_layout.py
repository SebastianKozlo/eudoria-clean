# s9_slot_layout.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: exact slot-payload layout: FUN_0075F5C0 (slot creator called by
# SLOT_ADD with kind/tag/traits), FUN_0075F6D0 (the +0x40 table payload-copy
# helper - 5 machine-verified call sites in FUN_0070D990), FUN_0070C980
# (slot array appender; machine-verify SLOT_ADD's 2 call targets too), and
# the int-traits factory FUN_00977A50. READ-ONLY. Own PE mapper.
# Output: 01_RAW/S9_SLOT_LAYOUT.json
import sys, os, json, struct
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004"
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

def read_window(d, image_base, secs, va, size):
    off = va_to_off(image_base, secs, va)
    if off is None:
        return None
    return d[off:off+size].hex(" ")

def verify_calls(d, image_base, secs, sites):
    out = []
    for site in sites:
        off = va_to_off(image_base, secs, site)
        if off is None or d[off] != 0xE8:
            out.append({"site": "0x%08X" % site, "error": "no E8 opcode at VA"})
            continue
        rel = struct.unpack_from("<i", d, off + 1)[0]
        tgt = site + 5 + rel
        out.append({"site": "0x%08X" % site, "target": "0x%08X" % tgt,
                    "target_bytes": read_window(d, image_base, secs, tgt, 24)})
    return out

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S9"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base
    windows = {
        "FUN_0075F5C0_slot_creator_win": (0x0075F5C0, 0x110),
        "FUN_0075F6D0_copy_helper_win": (0x0075F6D0, 0xF0),
        "FUN_0070C980_appender_win": (0x0070C980, 0xC0),
        "FUN_00977A50_int_traits_win": (0x00977A50, 0xB0),
        "FUN_00412C50_vecinit_win": (0x00412C50, 0xC0),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    out["slotadd_calls"] = verify_calls(d, image_base, secs, [
        0x0070CBFF,   # SLOT_ADD -> payload creator
        0x0070CC07,   # SLOT_ADD -> appender
        0x0070E360,   # FUN_0070E2F0 -> clone helper
        0x0070E367,   # FUN_0070E2F0 -> second call
    ])
    with open(os.path.join(RUN, "01_RAW", "S9_SLOT_LAYOUT.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S9 done.")
    for s in out["slotadd_calls"]:
        print(" ", s["site"], "->", s.get("target", s.get("error")))

if __name__ == "__main__":
    main()
