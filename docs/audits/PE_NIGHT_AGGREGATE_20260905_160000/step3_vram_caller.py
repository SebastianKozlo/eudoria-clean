#!/usr/bin/env python3
"""Step 3: WHO holds the VRAM-check strings? Census the sandbox DLLs for
'HardwareInformation', 'DEVICEMAP', 'Video' registry strings + their display imports."""
import os
import struct

WD = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\STEP3_VRAM_CALLER_CENSUS.txt"
lines = []
NEEDLES = [b"HardwareInformation", b"DEVICEMAP", b"HARDWARE\\DEVICEMAP", b"\\Device\\Video",
           b"EnumDisplayDevices", b"EnumDisplaySettings", b"GetDeviceCaps", b"4d36e968"]

for fn in sorted(os.listdir(WD)):
    if not fn.lower().endswith(".dll"):
        continue
    p = os.path.join(WD, fn)
    d = open(p, "rb").read()
    hits = []
    for needle in NEEDLES:
        i = d.find(needle)
        cnt = 0
        while i != -1:
            cnt += 1
            i = d.find(needle, i + 1)
        if cnt:
            hits.append(f"{needle.decode('ascii','replace')}x{cnt}")
    if hits:
        lines.append(f"  {fn} ({len(d)} B): {', '.join(hits)}")

# + the same census for the loaded system DLLs of interest
SYS = [r"C:\Windows\SysWOW64\dinput8.dll", r"C:\Windows\SysWOW64\d3dx9_30.dll",
       r"C:\Windows\SysWOW64\dsound.dll", r"C:\Windows\SysWOW64\winmm.dll"]
for p in SYS:
    d = open(p, "rb").read()
    hits = []
    for needle in NEEDLES:
        i = d.find(needle)
        cnt = 0
        while i != -1:
            cnt += 1
            i = d.find(needle, i + 1)
        if cnt:
            hits.append(f"{needle.decode('ascii','replace')}x{cnt}")
    lines.append(f"  {p.split(chr(92))[-1]} [sys] ({len(d)} B): {', '.join(hits) if hits else '(none)'}")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
