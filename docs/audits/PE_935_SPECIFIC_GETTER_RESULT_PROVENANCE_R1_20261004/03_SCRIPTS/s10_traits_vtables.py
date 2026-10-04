# s10_traits_vtables.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: resolve the int-traits vtables: dump .rdata at 0x00A9C670 and
# 0x00A799E4 (first 8 slots each), resolve slot-1 (the copy/payload method
# dispatched by FUN_0075F6D0), and decode the slot-1 target bytes. Also
# identify the second vtable-writer function near 0x00A744B2 and census its
# callers. READ-ONLY. Own PE mapper. Output: 01_RAW/S10_TRAITS_VTABLES.json
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

def read_u32s(d, image_base, secs, va, count):
    off = va_to_off(image_base, secs, va)
    if off is None:
        return None
    return ["0x%08X" % struct.unpack_from("<I", d, off + 4 * i)[0] for i in range(count)]

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
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S10"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base

    # vtables (8 slots each)
    out["vtable_00A9C670"] = read_u32s(d, image_base, secs, 0x00A9C670, 8)
    out["vtable_00A799E4"] = read_u32s(d, image_base, secs, 0x00A799E4, 8)

    # slot-1 targets of both vtables: instruction windows
    for name, vt in [("00A9C670", 0x00A9C670), ("00A799E4", 0x00A799E4)]:
        slots = read_u32s(d, image_base, secs, vt, 8)
        entries = []
        for i, sva in enumerate(slots or []):
            va = int(sva, 16)
            entries.append({"slot": i, "va": sva,
                            "bytes": read_window(d, image_base, secs, va, 32)})
        out["vtable_%s_slots" % name] = entries

    # the second vtable-writer function around 0x00A744B2: find its start
    # (scan back for CC padding) and census callers
    writer_off = va_to_off(image_base, secs, 0x00A744B2)
    start = writer_off
    while start > 0 and d[start-1] == 0xCC:
        start -= 1
    start_va = 0x00A744B2 - (writer_off - start)
    out["second_writer_start_va"] = "0x%08X" % start_va
    out["second_writer_window"] = read_window(d, image_base, secs, start_va, 0x30)
    out["second_writer_callers"] = scan_callers(d, image_base, secs, [start_va])

    # also census callers of FUN_00977A50 (the 0x00A9C670 writer) - bounded
    out["FUN_00977A50_callers"] = scan_callers(d, image_base, secs, [0x00977A50])

    with open(os.path.join(RUN, "01_RAW", "S10_TRAITS_VTABLES.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S10 done.")
    print("vtable 00A9C670:", out["vtable_00A9C670"])
    print("vtable 00A799E4:", out["vtable_00A799E4"])
    print("second writer start:", out["second_writer_start_va"], "callers:", out["second_writer_callers"])

if __name__ == "__main__":
    main()
