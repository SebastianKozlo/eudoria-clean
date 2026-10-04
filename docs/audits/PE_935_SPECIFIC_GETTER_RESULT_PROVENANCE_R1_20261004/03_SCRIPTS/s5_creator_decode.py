# s5_creator_decode.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: Phase D producer chain: window for FUN_0070DE10 (creator of the
# per-receiver 20006 class object - the +0x40 index table / +4 property store
# holder), the static factory global 0x00BA590C content, and whole-.text
# writer scans (MOV r/m32, imm/reg forms 89/8B+C7 disp32 and A3) for:
# 0x00BA590C (factory slot), 0x00BA5108 (default descriptor),
# 0x00BA9374 (fallback slot object), 0x00BA12E4 (manager singleton slot).
# READ-ONLY. Own PE mapper. Output: 01_RAW/S5_CREATOR_DECODE.json
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

def text_blob(d, secs):
    for s in secs:
        if s["name"] == ".text":
            return s["rawptr"], s["rawsize"], s["vaddr"]
    raise RuntimeError("no .text")

def scan_writers(d, image_base, secs, target_vas):
    # direct store scans: any 4-byte occurrence of the target VA used as a
    # displacement/address in .text (covers 89 0D xx / C7 05 xx / A3 xx /
    # 8B 0D xx loads too - classify by the opcode byte preceding).
    res = {}
    for tv in target_vas:
        pat = struct.pack("<I", tv)
        sites = []
        rawptr, rawsize, vaddr0 = text_blob(d, secs)
        blob = d[rawptr:rawptr+rawsize]
        start = 0
        while True:
            idx = blob.find(pat, start)
            if idx == -1:
                break
            site_va = image_base + vaddr0 + idx
            prev = blob[idx-1] if idx >= 1 else None
            prev2 = blob[idx-2] if idx >= 2 else None
            prev3 = blob[idx-3] if idx >= 3 else None
            sites.append({
                "va": "0x%08X" % site_va,
                "prev_bytes": " ".join("%02X" % b for b in blob[max(0, idx-3):idx]),
                "window": blob[max(0, idx-8):idx+10].hex(" "),
            })
            start = idx + 1
        res["0x%08X" % tv] = sites
    return res

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S5"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base

    windows = {
        "FUN_0070DE10_creator_win": (0x0070DE10, 0x200),
        "DAT_00BA590C_factory_slot": (0x00BA590C, 0x10),
        "DAT_00BA5D8C_sel20000_slot": (0x00BA5D8C, 0x10),
        "DAT_00BA12E4_manager_slot": (0x00BA12E4, 0x10),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    # .data initial content of the factory slot + its jump-table neighborhood
    out["writer_scans"] = scan_writers(d, image_base, secs,
                                       [0x00BA590C, 0x00BA5108, 0x00BA9374,
                                        0x00BA12E4])

    with open(os.path.join(RUN, "01_RAW", "S5_CREATOR_DECODE.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S5 done.")
    for k, v in out["writer_scans"].items():
        print(k, len(v))

if __name__ == "__main__":
    main()
