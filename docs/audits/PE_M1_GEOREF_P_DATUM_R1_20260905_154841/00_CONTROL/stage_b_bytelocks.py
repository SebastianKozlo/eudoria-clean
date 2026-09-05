#!/usr/bin/env python3
"""PE_M1_GEOREF_P_DATUM_R1 stage B — the datum-constant byte-locks (read-only).
Targets in the sandbox Entropia.exe (9.3.5, SHA E7785430...):
  1. The slot packer FUN_00991a20 (iter028: '{value, format 50.0}') — read its
     instruction bytes + locate the 50.0 constant (f64 0x4049000000000000 /
     f32 0x42480000) it references.
  2. The water level 10.0f @0x00A7B128 (iter036 byte-locked) — re-verify + find
     its consumers' instruction form (FLD/FMUL/FADD operand width).
  3. The census of ALL 50.0/10.0 float constants in the image + their VAs.
Method: read-only file reads; VA->file offset via the PE section map."""
import json
import struct

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GEOREF_P_DATUM_R1_20260905_154841"


def sections(d):
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<I", d, pe + 24 + 28)[0]  # ImageBase @opt+28
    secs = []
    t = pe + 24 + opt
    for i in range(nsec):
        name = d[t:t + 8].rstrip(b"\x00").decode()
        vsize, va, rsize, raw = struct.unpack_from("<IIII", d, t + 8)
        secs.append({"name": name, "va": va, "vsize": vsize, "raw": raw, "rsize": rsize})
        t += 40
    return base, secs


def va2off(base, secs, va):
    rva = va - base
    for s in secs:
        if s["va"] <= rva < s["va"] + s["vsize"]:
            return s["raw"] + (rva - s["va"])
    return None


def main():
    d = open(EXE, "rb").read()
    base, secs = sections(d)
    print(f"ImageBase {base:#x}; sections: " + ", ".join(f"{s['name']}@{s['va']:#x}+{s['vsize']:#x}" for s in secs))

    out = {"exe": EXE, "image_base": base, "sections": secs}

    # 1. FUN_00991a20 bytes (the slot packer)
    fva = 0x00991A20
    off = va2off(base, secs, fva)
    code = d[off:off + 96]
    out["packer_fun_00991a20"] = {"va": fva, "file_offset": off,
                                  "bytes": code.hex()}
    print(f"\nFUN_00991a20 @{fva:#x} (off {off:#x}):")
    for i in range(0, 96, 16):
        print("  " + code[i:i+16].hex(" "))

    # 2. The float-constant census: all f64/f32 50.0 and 10.0 in the image
    pats = {
        "f64_50.0": bytes.fromhex("0000000000004940"),
        "f32_50.0": bytes.fromhex("00004842"),
        "f64_10.0": bytes.fromhex("0000000000002440"),
        "f32_10.0": bytes.fromhex("00002042"),
    }
    census = {}
    for label, pat in pats.items():
        hits = []
        i = d.find(pat)
        while i != -1 and len(hits) < 400:
            hits.append(i)
            i = d.find(pat, i + 1)
        # file offset -> VA
        vas = []
        for h in hits:
            for s in secs:
                if s["raw"] <= h < s["raw"] + s["rsize"]:
                    vas.append(base + s["va"] + (h - s["raw"]))
                    break
        census[label] = {"count": len(hits), "vas": vas}
        print(f"\n{label}: {len(hits)} file hits -> {len(vas)} VA hits")
        print("  VAs: " + " ".join(f"{v:#x}" for v in vas[:16]))
    out["constant_census"] = census

    # 3. The known water 10.0f @0x00A7B128 — re-verify the bytes + width class
    wva = 0x00A7B128
    woff = va2off(base, secs, wva)
    wbytes = d[woff:woff + 8]
    out["water_10f_00A7B128"] = {"va": wva, "file_offset": woff,
                                 "bytes": wbytes.hex(),
                                 "as_f32": struct.unpack_from("<f", d, woff)[0],
                                 "as_f64_low": struct.unpack_from("<d", d, woff)[0]}
    print(f"\n@0x00A7B128: {wbytes.hex(' ')} | f32={struct.unpack_from('<f', d, woff)[0]}")

    with open(f"{RUN}\\01_RAW\\DATUM_CONSTANT_BYTELOCKS.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwritten: 01_RAW\\DATUM_CONSTANT_BYTELOCKS.json")


if __name__ == "__main__":
    main()
