# s8_slotadd_verify.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: machine-verify every E8 call target in FUN_007374F0 (slot array
# builder), the 20006 factory lazy-init function, FUN_0070D990 (class_obj
# creator incl. the +0x40 table copy helper targets), and decode windows for
# SLOT_ADD (target of the tag-6 add call), FUN_0070E2F0 (factory init call
# with args (8,0)), and the payload-copy helper family ~0x75F7C0.
# READ-ONLY. Own PE mapper. Output: 01_RAW/S8_SLOTADD_VERIFY.json
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
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S8"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base

    # every E8 in FUN_007374F0 (0x7374F0..0x7375B3) - walk 5-byte steps where
    # E8 is expected; safer: scan the range for E8 and verify each candidate
    range_sites = []
    for va in range(0x007374F0, 0x007375B3):
        off = va_to_off(image_base, secs, va)
        if off is not None and d[off] == 0xE8:
            rel = struct.unpack_from("<i", d, off + 1)[0]
            range_sites.append({"site": "0x%08X" % va,
                                "target": "0x%08X" % (va + 5 + rel)})
    out["FUN_007374F0_calls"] = range_sites

    # factory lazy-init (0x73E2C7..0x73E355) calls
    init_sites = []
    for va in range(0x0073E2C0, 0x0073E355):
        off = va_to_off(image_base, secs, va)
        if off is not None and d[off] == 0xE8:
            rel = struct.unpack_from("<i", d, off + 1)[0]
            init_sites.append({"site": "0x%08X" % va,
                               "target": "0x%08X" % (va + 5 + rel)})
    out["FACTORY_INIT_calls"] = init_sites

    # FUN_0070D990 (class_obj creator) calls
    creator_sites = []
    for va in range(0x0070D990, 0x0070DA7A):
        off = va_to_off(image_base, secs, va)
        if off is not None and d[off] == 0xE8:
            rel = struct.unpack_from("<i", d, off + 1)[0]
            creator_sites.append({"site": "0x%08X" % va,
                                  "target": "0x%08X" % (va + 5 + rel)})
    out["FUN_0070D990_calls"] = creator_sites

    # specific verifications
    out["specific"] = verify_calls(d, image_base, secs, [
        0x0073B87E,   # factory ctor register call
        0x005678BA,   # builder -> FUN_004C5580
    ])

    windows = {
        "SLOTADD_0070CBC0_win": (0x0070CBC0, 0x160),
        "FUN_0070E2F0_win": (0x0070E2F0, 0x100),
        "COPYHELPER_0075F7C0_win": (0x0075F7C0, 0x100),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    with open(os.path.join(RUN, "01_RAW", "S8_SLOTADD_VERIFY.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S8 done.")
    print("FUN_007374F0_calls:")
    for s in range_sites: print(" ", s["site"], "->", s["target"])
    print("FACTORY_INIT_calls:")
    for s in init_sites: print(" ", s["site"], "->", s["target"])
    print("FUN_0070D990_calls:")
    for s in creator_sites: print(" ", s["site"], "->", s["target"])

if __name__ == "__main__":
    main()
