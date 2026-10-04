# s3_corrected_windows.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: corrected/extended windows after s2 rel32 re-verification:
# FUN_004D1430 (the TRUE generic mapfind target of FUN_0072F880's call
# @0x0072F898 — the s2 window at 0x004C1430 was a target-arithmetic slip,
# recorded as a deviation), FUN_0073C8D0 (selector->factory), FUN_0073E100
# (factory+receiver -> class-selected object), FUN_00707E50 (singleton ctor),
# FUN_00844020 (established attribute-flag reader, narrow recheck),
# FUN_00567770 call region, static objects 0x00BA5108/0x00BA9374/0x00BA5800,
# and the call-site rel32 verification table (machine-computed targets for
# every call this run decodes). READ-ONLY. Own PE mapper.
# Output: 01_RAW/S3_CORRECTED_WINDOWS.json
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

def call_target(d, image_base, secs, site_va):
    # machine-verify: bytes at site_va must be E8; return computed target
    off = va_to_off(image_base, secs, site_va)
    if off is None or d[off] != 0xE8:
        return {"site": "0x%08X" % site_va, "error": "not an E8 at this VA"}
    rel = struct.unpack_from("<i", d, off + 1)[0]
    tgt = site_va + 5 + rel
    return {"site": "0x%08X" % site_va, "opcode_byte": "E8",
            "rel32": "0x%08X" % (rel & 0xFFFFFFFF), "target": "0x%08X" % tgt,
            "target_bytes": read_window(d, image_base, secs, tgt, 16)}

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S3"}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base

    windows = {
        "FUN_004D1430_mapfind_win": (0x004D1430, 0x200),
        "FUN_0073C8D0_win": (0x0073C8D0, 0x180),
        "FUN_0073E100_win": (0x0073E100, 0x180),
        "FUN_00707E50_win": (0x00707E50, 0x200),
        "FUN_00844020_win": (0x00844020, 0x180),
        "FUN_00567770_callsite_win": (0x00567860, 0xB0),
        "DAT_00BA5108_staticdesc": (0x00BA5108, 0x20),
        "DAT_00BA9374_staticfallback": (0x00BA9374, 0x20),
        "DAT_00BA5800_deftemplate": (0x00BA5800, 0x40),
        "DAT_00BA12E4_singleton_ptr": (0x00BA12E4, 0x8),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    # machine-computed rel32 verification for every call this run decodes
    call_sites = [
        0x004C54B2, 0x004C54CE, 0x004C54E4, 0x004C54F4, 0x004C54FA,
        0x004C5508, 0x004C550E, 0x004C5523, 0x004C5542, 0x004C5549,
        0x004C555E, 0x004C55B5, 0x004C55D2, 0x004C55D9, 0x005678BA,
        0x00703B88, 0x00703B8F, 0x00703D7D, 0x00703D8F,
        0x0072F898, 0x0072F8AF, 0x0072F8BD, 0x0041549F, 0x004154B9,
    ]
    out["call_site_verification"] = [call_target(d, image_base, secs, s) for s in call_sites]

    with open(os.path.join(RUN, "01_RAW", "S3_CORRECTED_WINDOWS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S3 done.")

if __name__ == "__main__":
    main()
