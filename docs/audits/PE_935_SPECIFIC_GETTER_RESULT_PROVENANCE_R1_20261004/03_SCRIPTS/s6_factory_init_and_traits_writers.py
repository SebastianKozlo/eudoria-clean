# s6_factory_init_and_traits_writers.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: decode the 20006-factory lazy initializer (site cluster 0x0073E2B3/
# 0x0073E303/0x0073E348) + scan writers of the ArkRTTraitsInt static object
# 0x00BA937C (descriptor+0 for kind-1 int slots; from the 20002_PAYLOAD30
# canon) to locate the INT-DESCRIPTOR SETTER family. Also dump the 0x00977700
# region (traits factory area) and the other factory consumer at 0x007374C9.
# READ-ONLY. Own PE mapper. Output: 01_RAW/S6_FACTORY_AND_TRAITS.json
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

def scan_imm32(d, image_base, secs, imm_list):
    res = {}
    for imm in imm_list:
        pat = struct.pack("<I", imm)
        sites = []
        for s in secs:
            if s["name"] != ".text":
                continue
            blob = d[s["rawptr"]:s["rawptr"]+s["rawsize"]]
            start = 0
            while True:
                idx = blob.find(pat, start)
                if idx == -1:
                    break
                site_va = image_base + s["vaddr"] + idx
                sites.append({
                    "va": "0x%08X" % site_va,
                    "window": blob[max(0, idx-8):idx+10].hex(" "),
                })
                start = idx + 1
        res["0x%08X" % imm] = sites
    return res

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S6"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base

    windows = {
        "FACTORY_INIT_0073E2A0_win": (0x0073E2A0, 0x120),
        "TRAITS_AREA_00977700_win": (0x00977700, 0x100),
        "FACTORY_CONSUMER_007374C9_win": (0x007374C0, 0xA0),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    out["imm32_scans"] = scan_imm32(d, image_base, secs, [0x00BA937C, 0x00BA9378, 0x00BA9370])

    with open(os.path.join(RUN, "01_RAW", "S6_FACTORY_AND_TRAITS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    for k, v in out["imm32_scans"].items():
        print(k, len(v), "sites")

if __name__ == "__main__":
    main()
