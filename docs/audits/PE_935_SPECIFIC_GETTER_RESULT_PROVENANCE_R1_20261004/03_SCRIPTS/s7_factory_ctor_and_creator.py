# s7_factory_ctor_and_creator.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: Phase D continuation: windows for the 20006 factory constructor
# FUN_0073B820 (reveals factory layout incl. the +0x80 bind delegate),
# the factory init calls FUN_0073DFF0 / FUN_007374F0 / FUN_0070C150 /
# FUN_0070BF10, the class_obj creator FUN_0070D990, and FUN_0070DCF0 (the
# early-path creator in FUN_0070DE10). READ-ONLY. Own PE mapper.
# Output: 01_RAW/S7_FACTORY_CTOR_AND_CREATOR.json
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

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S7"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base
    windows = {
        "FUN_0073B820_factory_ctor_win": (0x0073B820, 0x200),
        "FUN_0073DFF0_factory_init1_win": (0x0073DFF0, 0x100),
        "FUN_007374F0_factory_init2_win": (0x007374F0, 0x100),
        "FUN_0070C150_factory_init3_win": (0x0070C150, 0x100),
        "FUN_0070BF10_factory_init4_win": (0x0070BF10, 0x100),
        "FUN_0070D990_classobj_creator_win": (0x0070D990, 0x180),
        "FUN_0070DCF0_early_creator_win": (0x0070DCF0, 0x120),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}
    with open(os.path.join(RUN, "01_RAW", "S7_FACTORY_CTOR_AND_CREATOR.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S7 done.")

if __name__ == "__main__":
    main()
