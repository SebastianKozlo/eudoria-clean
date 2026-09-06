#!/usr/bin/env python3
"""Read the VT2-referenced strings + dump them to a file (avoiding the console cp1252 issue)."""
import struct

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\VT2_STRINGS.txt"
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
t = pe + 24 + opt
for i in range(nsec):
    name = d[t:t + 8].rstrip(b"\x00").decode()
    vsize, sva, rsize, praw = struct.unpack_from("<IIII", d, t + 8)
    secs.append((name, sva, vsize, praw))
    t += 40

lines = []
for va in (0x9A6408, 0x9A6438, 0x9A6468, 0x9A6498, 0x9A64E9, 0x9A6500, 0x9A6540, 0x9A6580):
    rva = va - 0x400000
    for name, sva, vsz, praw in secs:
        if sva <= rva < sva + vsz:
            o = praw + (rva - sva)
            s = d[o:o + 128].split(b"\x00")[0]
            lines.append("0x{:X} = {!r}".format(va, s))
            break
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("written " + OUT)
