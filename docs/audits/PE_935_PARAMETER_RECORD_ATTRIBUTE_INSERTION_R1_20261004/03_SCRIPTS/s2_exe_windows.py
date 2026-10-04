# s2_exe_windows.py
# RUN: PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004
# Purpose: read raw instruction windows from the pinned Entropia.exe and enumerate
# rel32 CALL sites for target functions (caller censuses) + PUSH imm32 sites.
# Own PE mapper (section table read; no offset==RVA assumption). READ-ONLY.
# Output: 01_RAW/S2_EXE_WINDOWS.json
import sys, os, json, struct
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

def load_pe(path):
    d = open(path, "rb").read()
    e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
    assert d[e_lfanew:e_lfanew+4] == b"PE\x00\x00"
    coff = e_lfanew + 4
    nsec = struct.unpack_from("<H", d, coff + 2)[0]
    opt_size = struct.unpack_from("<H", d, coff + 16)[0]
    opt = coff + 20
    magic = struct.unpack_from("<H", d, opt)[0]
    image_base = struct.unpack_from("<I", d, opt + 28)[0]  # PE32
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
            off = s["rawptr"] + (rva - s["vaddr"])
            if off is not None and rva - s["vaddr"] < s["rawsize"]:
                return off
    return None

def read_window(d, image_base, secs, va, size):
    off = va_to_off(image_base, secs, va)
    if off is None:
        return None
    return d[off:off+size].hex(" ")

def scan_calls(d, image_base, secs, targets):
    # scan .text for E8 rel32 whose target == t
    res = {("0x%08X" % t): [] for t in targets}
    for s in secs:
        if s["name"] != ".text":
            continue
        base = s["rawptr"]; size = s["rawsize"]
        blob = d[base:base+size]
        vaddr0 = s["vaddr"]
        i = 0
        n = len(blob)
        while i < n - 5:
            if blob[i] == 0xE8:
                rel = struct.unpack_from("<i", blob, i + 1)[0]
                tgt_va = image_base + vaddr0 + i + 5 + rel
                key = "0x%08X" % tgt_va
                if key in res:
                    site_va = image_base + vaddr0 + i
                    res[key].append("0x%08X" % site_va)
                i += 1
            else:
                i += 1
    return res

def scan_push_imm32(d, image_base, secs, imm):
    # find PUSH imm32 (68 xx xx xx xx) sites with the given immediate in .text
    pat = b"\x68" + struct.pack("<I", imm)
    sites = []
    for s in secs:
        if s["name"] != ".text":
            continue
        blob = d[s["rawptr"]:s["rawptr"]+s["rawsize"]]
        start = 0
        while True:
            i = blob.find(pat, start)
            if i < 0:
                break
            sites.append("0x%08X" % (image_base + s["vaddr"] + i))
            start = i + 1
    return sites

def main():
    d, image_base, secs = load_pe(EXE)
    info = {"image_base": "0x%08X" % image_base,
            "sections": [{"name": s["name"], "vaddr": "0x%08X" % s["vaddr"],
                          "vsize": s["vsize"], "rawptr": s["rawptr"],
                          "rawsize": s["rawsize"]} for s in secs]}
    windows = {}
    # Established-function narrow re-verification windows (BRIDGE pins):
    WIN = {
        # reader path string .rdata
        "string_parameters_templates_vfs_0x00A86D30": (0x00A86D30, 24),
        # reader FUN_0072FA30 head (path build + open + loop)
        "FUN_0072FA30_head": (0x0072FA30, 160),
        # per-record read FUN_00971AD0 head
        "FUN_00971AD0_head": (0x00971AD0, 160),
        # parse FUN_00730C90 head (field parse f0,f2,f1,f3,f4)
        "FUN_00730C90_head": (0x00730C90, 176),
        # registry lazy singleton FUN_0043A550
        "FUN_0043A550_full": (0x0043A550, 96),
        # lookup FUN_0072F580 full
        "FUN_0072F580_full": (0x0072F580, 48),
        # RB-tree insert FUN_0072F8D0 head
        "FUN_0072F8D0_head": (0x0072F8D0, 160),
        # lookup family sibling FUN_0072F880 (NEW decode)
        "FUN_0072F880_full": (0x0072F880, 128),
        # FUN_004c5480 (NEW decode - id2 from 20006 property?)
        "FUN_004C5480_full": (0x004C5480, 160),
        # FUN_004c5580 head + early body (established deriver; raw re-pin)
        "FUN_004C5580_head": (0x004C5580, 224),
        # FUN_00567770 window around the FUN_004c5580 call @0x005678BA
        "FUN_00567770_around_005678BA": (0x00567880, 160),
        # FUN_00567770 head (builder)
        "FUN_00567770_head": (0x00567770, 96),
        # FUN_005670a0 (NEW decode - record<-template seam)
        "FUN_005670A0_full": (0x005670A0, 128),
        # FUN_005B5F90 head (lookup + FUN_005670a0 call)
        "FUN_005B5F90_head": (0x005B5F90, 128),
        # FUN_005B6370 region around PUSH 0x3ED3 @0x005B6597
        "FUN_region_005B6560_65D0": (0x005B6560, 128),
        # FUN_005B6370 head (identify)
        "FUN_005B6370_head": (0x005B6370, 96),
        # FUN_00567170 lookup call region (established)
        "FUN_00567170_around_0056736D": (0x00567360, 48),
        # getters (established): A=FUN_007CE1E0, B=FUN_00746550, D=FUN_0048ADA0
        "getter_A_007CE1E0": (0x007CE1E0, 16),
        "getter_B_00746550": (0x00746550, 16),
        "getter_D_0048ADA0": (0x0048ADA0, 16),
        "getter_C_006B22D0": (0x006B22D0, 16),
        # record setters (established): position/rotation
        "setter_pos_00730F90": (0x00730F90, 32),
        "setter_rot_00730FB0": (0x00730FB0, 32),
        # FUN_00797280 (record <- id2 store; established usage in constructors)
        "FUN_00797280_full": (0x00797280, 48),
        # FUN_00457930 head (named registration; established)
        "FUN_00457930_head": (0x00457930, 48),
    }
    for k, (va, size) in WIN.items():
        windows[k] = {"va": "0x%08X" % va, "size": size, "bytes": read_window(d, image_base, secs, va, size)}
    # caller censuses
    targets = [0x0072F580, 0x005670A0, 0x004C5580, 0x0072F880, 0x004C5480,
               0x005B5F90, 0x00567170, 0x0043A550, 0x00846840, 0x00854720,
               0x00730C90, 0x00971AD0, 0x0072FA30, 0x0072F8D0, 0x006C3F50,
               0x00848EA0, 0x007CE1E0, 0x00567770, 0x00567C50, 0x00797280,
               0x008492C0, 0x00567030]
    censuses = scan_calls(d, image_base, secs, targets)
    # PUSH imm32 scan for the hardcoded keys
    pushes = {}
    for imm in (0x3ED3, 0x3ED2, 0x3BD9, 0x3BDA, 0x3BDB, 0x3A47, 0x3A40, 0x119C):
        pushes["0x%08X" % imm] = scan_push_imm32(d, image_base, secs, imm)
    out = {"pe": info, "windows": windows, "call_censuses": censuses, "push_imm32": pushes}
    with open(os.path.join(RUN, "01_RAW", "S2_EXE_WINDOWS.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("windows:", len(windows), "| censuses:", {k: len(v) for k, v in censuses.items()})
    print("pushes:", pushes)

if __name__ == "__main__":
    main()
