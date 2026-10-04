# s1_callsite_extent.py
# RUN: PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004
# Purpose (bounded, READ-ONLY): (1) re-verify pinned EXE identity;
# (2) re-verify the pinned call site CALL FUN_0070DC20 @0x0070DDBD by
# machine call-target computation; (3) dump the caller FUN_0070DCF0 window
# (0x0070DCF0..0x0070DE10) for argument reconstruction; (4) determine the
# FUN_0070DC20 extent (function end) and dump its full body; (5) whole-.text
# E8 xref census of FUN_0070DC20. Own PE mapper, byte reads only.
# Output: 01_RAW/S1_CALLSITE_AND_EXTENT.json
import sys, os, json, struct, hashlib
sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()

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

def scan_callers(d, image_base, secs, target):
    res = []
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
                if tgt_va == target:
                    res.append("0x%08X" % (image_base + vaddr0 + i))
            i += 1
    return res

def main():
    out = {"run": "PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004", "stage": "S1"}
    # (1) EXE identity
    sz = os.path.getsize(EXE)
    out["exe_identity"] = {"path": EXE, "size_bytes": sz,
                           "sha256": sha256(EXE)}
    d, image_base, secs = load_pe(EXE)
    out["image_base"] = "0x%08X" % image_base
    out["sections"] = [{"name": s["name"], "vaddr": "0x%08X" % s["vaddr"],
                        "vsize": "0x%X" % s["vsize"], "rawsize": "0x%X" % s["rawsize"],
                        "rawptr": "0x%X" % s["rawptr"]} for s in secs]

    # (2) call-site re-verification @0x0070DDBD
    cs_va = 0x0070DDBD
    cs_bytes = read_window(d, image_base, secs, cs_va, 8)
    off = va_to_off(image_base, secs, cs_va)
    raw = d[off:off+5]
    is_e8 = raw[0] == 0xE8
    rel = struct.unpack_from("<i", raw, 1)[0]
    tgt = cs_va + 5 + rel
    out["callsite_0x0070DDBD"] = {
        "va": "0x%08X" % cs_va, "bytes": cs_bytes,
        "opcode_E8": is_e8, "rel32": "0x%08X" % (rel & 0xFFFFFFFF),
        "machine_computed_target": "0x%08X" % tgt,
        "expected_target": "0x0070DC20",
        "match": (is_e8 and tgt == 0x0070DC20)}

    # (3) caller window FUN_0070DCF0 .. 0x0070DE10 (includes the whole known
    # candidate-A frame from the R1 canon decode)
    out["windows"] = {}
    out["windows"]["FUN_0070DCF0_full"] = {
        "va": "0x%08X" % 0x0070DCF0, "size": 0x121,
        "hex": read_window(d, image_base, secs, 0x0070DCF0, 0x121)}

    # (4) FUN_0070DC20 extent: dump from start until the next function start
    # boundary. Known neighborhood: FUN_0070DCF0 starts at 0x0070DCF0, so
    # FUN_0070DC20's body lies in [0x0070DC20, 0x0070DCF0). Dump it all.
    out["windows"]["FUN_0070DC20_region"] = {
        "va": "0x%08X" % 0x0070DC20, "size": 0xD0,
        "hex": read_window(d, image_base, secs, 0x0070DC20, 0xD0)}

    # also dump a wider surrounding region to see the preceding function's
    # tail and any padding (context only)
    out["windows"]["predecessor_tail_context"] = {
        "va": "0x%08X" % 0x0070DBC0, "size": 0x60,
        "hex": read_window(d, image_base, secs, 0x0070DBC0, 0x60)}

    # (5) whole-.text E8 xref census for FUN_0070DC20
    out["xref_census_FUN_0070DC20_E8_callers"] = scan_callers(
        d, image_base, secs, 0x0070DC20)

    with open(os.path.join(RUN, "01_RAW", "S1_CALLSITE_AND_EXTENT.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("S1 done.")
    print("exe_sha256=%s size=%d" % (out["exe_identity"]["sha256"], sz))
    print("callsite match=%s target=0x%08X" % (out["callsite_0x0070DDBD"]["match"], tgt))
    print("xrefs=%s" % out["xref_census_FUN_0070DC20_E8_callers"])

if __name__ == "__main__":
    main()
