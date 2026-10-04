# s2_producer_windows.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: bounded raw windows for the Phase B/C/D machinery discovered by s1:
# FUN_004926E0 (element accessor), FUN_00977780 (error helper), FUN_00415470
# (singleton behind class-selector resolve), FUN_00703D70 (class-selector
# machinery), FUN_004C1430 (mapfind used by FUN_0072F880), FUN_00567770 call
# region re-read, FUN_0043A550, plus imm32 push/jump-table evidence for the
# property-array writer search (Phase D). READ-ONLY. Own PE mapper.
# Output: 01_RAW/S2_PRODUCER_WINDOWS.json
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

def scan_imm32_in_text(d, image_base, secs, imm_list):
    # all occurrences of the imm32 byte patterns 68/3D/C7-displacement-insensitive:
    # record raw 4-byte little-endian occurrences of each value inside .text
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
                sites.append("0x%08X" % (image_base + s["vaddr"] + idx))
                start = idx + 1
        res["0x%08X" % imm] = sites
    return res

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S2"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base

    windows = {
        # element accessor used at the value-index step (LEA ECX,[ECX+EAX*4])
        "FUN_004926E0_win": (0x004926E0, 0x100),
        # error helper (descriptor invalid path)
        "FUN_00977780_win": (0x00977780, 0x80),
        # singleton behind FUN_00703B80
        "FUN_00415470_win": (0x00415470, 0xA0),
        # class-selector machinery (bigger window)
        "FUN_00703D70_win": (0x00703D70, 0x140),
        # mapfind used by FUN_0072F880 (key type determination)
        "FUN_004C1430_win": (0x004C1430, 0x120),
        # builder call region (re-read wider)
        "FUN_00567770_around_call2": (0x00567860, 0xB0),
        # registry singleton (narrow)
        "FUN_0043A550_win2": (0x0043A550, 0x50),
        # static default descriptor area (out-of-range getter return) + default template
        "DAT_00BA5108_win": (0x00BA5108, 0x20),
        "DAT_00BA5800_win": (0x00BA5800, 0x40),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    # call censuses for the new machinery
    targets = [0x004926E0, 0x00977780, 0x00415470, 0x00703D70, 0x004C1430,
               0x0070C180, 0x0072F880]
    out["call_census"] = scan_callers(d, image_base, secs, targets)

    with open(os.path.join(RUN, "01_RAW", "S2_PRODUCER_WINDOWS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S2 done. census=%s" % {k: len(v) for k, v in out["call_census"].items()})

if __name__ == "__main__":
    main()
