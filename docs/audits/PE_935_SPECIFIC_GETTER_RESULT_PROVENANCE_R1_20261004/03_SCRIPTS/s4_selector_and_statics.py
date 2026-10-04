# s4_selector_and_statics.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: windows at the machine-verified corrected targets of the
# class-selector machinery: FUN_0073C870 (selector->factory; the s3 dict name
# "FUN_0073C8D0" was the pre-correction label — VA now corrected),
# FUN_0070E100 (factory+receiver -> class object), plus the singleton
# constructor FUN_00707E50, the builder call region, static objects, and
# caller censuses of the corrected targets. READ-ONLY. Own PE mapper.
# Output: 01_RAW/S4_SELECTOR_AND_STATICS.json
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

def scan_callers(d, image_base, secs, targets):
    res = {}
    tset = {("0x%08X" % t): t for t in targets}
    for s in secs:
        if s["name"] != ".text":
            continue
        blob = d[s["rawptr"]:s["rawptr"]+s["rawsize"]]
        vaddr0 = s["vaddr"]
        n = len(blob)
        i = 0
        while i < n - 5:
            if blob[i] == 0xE8:
                rel = struct.unpack_from("<i", blob, i + 1)[0]
                tgt_va = image_base + vaddr0 + i + 5 + rel
                key = "0x%08X" % tgt_va
                if key in tset:
                    res.setdefault(key, []).append("0x%08X" % (image_base + vaddr0 + i))
            i += 1
    return res

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S4"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base

    windows = {
        "FUN_0073C870_selector_factory_win": (0x0073C870, 0x120),
        "FUN_0070E100_factory_receiver_win": (0x0070E100, 0x180),
        "FUN_00707E50_singleton_ctor_win": (0x00707E50, 0x200),
        "FUN_00567770_builder_callsite_win": (0x00567860, 0xB0),
        "DAT_00BA5108_staticdesc": (0x00BA5108, 0x20),
        "DAT_00BA9374_staticfallback": (0x00BA9374, 0x20),
        "DAT_00BA5800_deftemplate": (0x00BA5800, 0x40),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    targets = [0x0073C870, 0x0070E100, 0x00707E50]
    out["call_census"] = scan_callers(d, image_base, secs, targets)

    with open(os.path.join(RUN, "01_RAW", "S4_SELECTOR_AND_STATICS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S4 done. census=%s" % {k: len(v) for k, v in out["call_census"].items()})

if __name__ == "__main__":
    main()
