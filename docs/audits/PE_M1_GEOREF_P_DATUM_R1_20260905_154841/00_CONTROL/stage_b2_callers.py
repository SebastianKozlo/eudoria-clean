#!/usr/bin/env python3
"""Stage B2 — the packer callers + the 50.0 load sites (read-only).
Find: (a) all CALL sites targeting FUN_00991a20 (E8 rel32);
      (b) all FLD/FSTP dword [VA] instructions referencing the 8 f32-50.0 VAs
          and the f64-50.0 VA (DD 05 / D9 05 patterns);
      (c) the instruction context around each caller."""
import json
import struct

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GEOREF_P_DATUM_R1_20260905_154841"
TARGET = 0x00991A20


def sections(d):
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<I", d, pe + 24 + 28)[0]
    secs = []
    t = pe + 24 + opt
    for i in range(nsec):
        name = d[t:t + 8].rstrip(b"\x00").decode()
        vsize, va, rsize, raw = struct.unpack_from("<IIII", d, t + 8)
        secs.append((name, va, vsize, raw, rsize))
        t += 40
    return base, secs


def va2off(base, secs, va):
    rva = va - base
    for name, sva, vsz, raw, rsz in secs:
        if sva <= rva < sva + vsz:
            return raw + (rva - sva)
    return None


def main():
    d = open(EXE, "rb").read()
    base, secs = sections(d)
    text = next(s for s in secs if s[0] == ".text")
    traw, tva, tsize = text[3], text[1], min(text[2], text[4])

    # (a) CALL sites -> 0x00991A20
    callers = []
    for i in range(traw, traw + tsize - 5):
        if d[i] == 0xE8:
            rel = struct.unpack_from("<i", d, i + 1)[0]
            va_call = base + tva + (i - traw)
            tgt = va_call + 5 + rel
            if tgt == TARGET:
                callers.append(va_call)
    print(f"CALL sites -> FUN_00991a20: {len(callers)}: " + " ".join(f"{c:#x}" for c in callers))

    # context: 64 bytes before each call
    ctx = {}
    for c in callers:
        off = va2off(base, secs, c)
        ctx[f"{c:#x}"] = d[off - 64:off + 5].hex()
        print(f"\n@call {c:#x} (context -64..+5):")
        h = d[off - 64:off + 5].hex(" ")
        for j in range(0, len(h), 48):
            print("   " + h[j:j + 48])

    # (b) the 50.0 references: FLD/FSTP/FADD dword [VA] with VA in f32-50 set
    f32_50 = [0xA7AFA8, 0xA86E40, 0xA97EB0, 0xAC422A, 0xB04266, 0xB14266, 0xB24256, 0xB3E0B2]
    f64_50 = [0xA81D20]
    refs = {}
    for opcode, name in ((b"\xD9\x05", "fld_f32"), (b"\xD9\x3D", "fstp_f32"),
                         (b"\xD8\x05", "fadd_f32"), (b"\xD8\x0D", "fmul_f32"),
                         (b"\xD8\x25", "fsub_f32"), (b"\xD8\x35", "fsubr_f32"),
                         (b"\xD8\x2D", "fsub_f32b"), (b"\xDD\x05", "fld_f64")):
        for i in range(traw, traw + tsize - 6):
            if d[i:i + 2] == opcode:
                va = struct.unpack_from("<I", d, i + 2)[0]
                va_call = base + tva + (i - traw)
                if va in f32_50:
                    refs.setdefault(f"{va:#x}", []).append({"op": name, "site": f"{va_call:#x}"})
                if va in f64_50:
                    refs.setdefault(f"{va:#x}", []).append({"op": name, "site": f"{va_call:#x}"})
    for k, v in refs.items():
        print(f"\nrefs to {k}: {len(v)}")
        for r in v[:10]:
            print(f"   {r['op']} @ {r['site']}")

    out = {"target": hex(TARGET), "callers": [hex(c) for c in callers],
           "caller_context": ctx, "constant_refs": refs}
    with open(f"{RUN}\\01_RAW\\PACKER_CALLERS.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwritten: 01_RAW\\PACKER_CALLERS.json")


if __name__ == "__main__":
    main()
