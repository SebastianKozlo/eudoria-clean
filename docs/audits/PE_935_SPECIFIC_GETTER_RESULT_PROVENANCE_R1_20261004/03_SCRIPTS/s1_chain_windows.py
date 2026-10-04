# s1_chain_windows.py
# RUN: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
# Purpose: identity verification + bounded raw instruction windows for the audited
# getter chain (FUN_004C5480 receiver/class-selector/tag-6) + rel32 CALL censuses
# (callers of each chain function). Own PE mapper (section-table read; no
# offset==RVA assumption). READ-ONLY vs the pinned EXE. sys.dont_write_bytecode.
# Output: 01_RAW/S1_CHAIN_WINDOWS.json
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SHA256_EXPECT = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest().upper()

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
            if rva - s["vaddr"] < s["rawsize"]:
                return s["rawptr"] + (rva - s["vaddr"])
    return None

def read_window(d, image_base, secs, va, size):
    off = va_to_off(image_base, secs, va)
    if off is None:
        return None
    return d[off:off+size].hex(" ")

# call census: E8 rel32 sites in .text whose target == t (target VA, image-based)
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

def scan_jmp_thunks(d, image_base, secs, targets):
    # E9 rel32 direct JMP thunks to target (helper relocation pattern)
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
            if blob[i] == 0xE9:
                rel = struct.unpack_from("<i", blob, i + 1)[0]
                tgt_va = image_base + vaddr0 + i + 5 + rel
                key = "0x%08X" % tgt_va
                if key in tset:
                    res.setdefault(key, []).append("0x%08X" % (image_base + vaddr0 + i))
            i += 1
    return res

def main():
    out = {"run": "PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004", "stage": "S1"}
    # identity
    exe_sha = sha256_file(EXE)
    d, image_base, secs = load_pe(EXE)
    out["identity"] = {
        "exe": EXE,
        "exe_size": os.path.getsize(EXE),
        "exe_sha256": exe_sha,
        "exe_sha256_expected": EXE_SHA256_EXPECT,
        "exe_sha256_match": exe_sha == EXE_SHA256_EXPECT,
        "image_base": "0x%08X" % image_base,
        "sections": [{"name": s["name"], "vaddr": "0x%08X" % s["vaddr"],
                      "vsize": "0x%X" % s["vsize"], "rawsize": "0x%X" % s["rawsize"],
                      "rawptr": "0x%X" % s["rawptr"]} for s in secs],
    }
    assert exe_sha == EXE_SHA256_EXPECT, "EXE identity FAILED"

    # ---- bounded windows for the audited chain ----
    windows = {
        # audited getter core (full function body window)
        "FUN_004C5480_full": (0x004C5480, 0x1A0),
        # the wrapper that calls it (per predecessor: call @0x004C55B5)
        "FUN_004C5580_win": (0x004C5580, 0x90),
        # builder call region (FUN_00567770, call site @0x005678BA per predecessor)
        "FUN_00567770_around_call": (0x00567880, 0x60),
        # class-selector resolve wrapper
        "FUN_00703B80_win": (0x00703B80, 0x200),
        # the property/tag getter core (this run's main decode target)
        "FUN_0070C180_win": (0x0070C180, 0x400),
        # receiver tree resolve
        "FUN_00843DD0_win": (0x00843DD0, 0x180),
        # attribute-flag reader (established; narrow recheck)
        "FUN_00844020_win": (0x00844020, 0x180),
        # registry singleton (established; narrow recheck)
        "FUN_0043A550_win": (0x0043A550, 0x60),
        # lookup-with-copy (established; narrow recheck)
        "FUN_0072F880_win": (0x0072F880, 0x100),
    }
    out["windows"] = {}
    for name, (va, size) in windows.items():
        out["windows"][name] = {"va": "0x%08X" % va, "size": size,
                                "hex": read_window(d, image_base, secs, va, size)}

    # ---- rel32 call censuses ----
    targets = [0x004C5480, 0x004C5580, 0x00703B80, 0x0070C180, 0x00843DD0,
               0x00844020, 0x0043A550, 0x0072F880, 0x0072F580, 0x00567770]
    out["call_census"] = scan_callers(d, image_base, secs, targets)
    out["jmp_thunk_census"] = scan_jmp_thunks(d, image_base, secs, targets)

    os.makedirs(os.path.join(RUN, "01_RAW"), exist_ok=True)
    with open(os.path.join(RUN, "01_RAW", "S1_CHAIN_WINDOWS.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S1 done. windows=%d call_census=%s" %
          (len(windows), {k: len(v) for k, v in out["call_census"].items()}))

if __name__ == "__main__":
    main()
