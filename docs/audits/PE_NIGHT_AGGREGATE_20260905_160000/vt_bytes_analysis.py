#!/usr/bin/env python3
"""The byte-level analysis of the DisplaySubsystem VT1 (0x48B520) + VT2 (0x48B0E0):
the call census (E8 rel32), the immediate constants, the strings referenced."""
import struct

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\VT_BYTES_ANALYSIS.txt"

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
t = pe + 24 + opt
for i in range(nsec):
    name = d[t:t + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, va, rsize, raw = struct.unpack_from("<IIII", d, t + 8)
    secs.append((name, va, vsize, raw))
    t += 40


def va2off(tva):
    rva = tva - 0x400000
    for name, va, vsz, raw in secs:
        if va <= rva < va + vsz:
            return raw + (rva - va)
    return None


lines = []
for fva, label, size in ((0x0048B520, "VT1_0048b520", 0x300), (0x0048B0E0, "VT2_0048b0e0", 0x440)):
    off = va2off(fva)
    code = d[off:off + size]
    lines.append("=== {} (bytes at the entry: {})".format(label, code[:16].hex(" ")))
    # find the function end (ret + CC padding or ret far)
    end = 0
    for j in range(len(code) - 6):
        if code[j] in (0xC3,) and code[j + 1:j + 5] in (b"\xcc\xcc\xcc\xcc", b"\x90\x90\x90\x90", b"\xcc\xcc\xcc\x90"):
            end = j
            break
        if code[j:j + 3] == b"\xc2\x10\x00" or code[j:j + 2] == b"\xc2\x08":
            end = j
            break
    if end == 0:
        end = size
    lines.append("function end scan: {} bytes".format(end))
    body = code[:end]
    # the call census
    calls = []
    j = 0
    while j < len(body) - 5:
        if body[j] == 0xE8:
            rel = struct.unpack_from("<i", body, j + 1)[0]
            tgt = fva + j + 5 + rel
            calls.append((fva + j, tgt))
        j += 1
    lines.append("calls ({}):".format(len(calls)))
    for site, tgt in calls:
        lines.append("  call @0x{:08X} -> 0x{:08X}".format(site, tgt))
    # the referenced constants: mov dword ptr [imm],imm / push imm
    j = 0
    while j < len(body) - 6:
        if body[j] == 0x68:  # PUSH imm32
            v = struct.unpack_from("<I", body, j + 1)[0]
            if v > 0x3FFFF and v < 0x1000000:
                lines.append("  push imm @0x{:08X} = 0x{:08X}".format(fva + j, v))
            j += 5
        else:
            j += 1
    lines.append("")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
