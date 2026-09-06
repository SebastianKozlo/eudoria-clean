#!/usr/bin/env python3
"""Step 2: (a) the TIME-ORDERED death sequence (the loads + reads + exits interleaved);
(b) the UTF-16 string census for the display APIs + the runtime-resolution strings."""
import csv
import struct

CSV = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test\entropia_death_trace.csv"
EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\STEP2_TIMEORDER_AND_UTF16.txt"
lines = []

rows = list(csv.DictReader(open(CSV, encoding="utf-8", errors="replace")))
T = '\ufeff"Time of Day"'
for r in rows:
    r["Time of Day"] = r.pop(T)
e = [r for r in rows if r["Process Name"] == "Entropia.exe"]

# (a) the ordered events: loads of interest + all display/registry-video reads + exits
INTEREST_LOADS = ("dinput8", "InputHost", "CoreMessaging", "imm32", "umpdc", "d3dx9_30", "dsound")
events = []
for r in e:
    op = r["Operation"]
    p = r["Path"]
    if op == "Load Image" and any(s.lower() in p.lower() for s in INTEREST_LOADS):
        events.append(("LOAD", r))
    elif op in ("RegOpenKey", "RegQueryValue", "RegCloseKey") and ("DEVICEMAP" in p or "4d36e968" in p or "53C87C01" in p or "Control\\Video" in p):
        events.append(("VIDREG", r))
    elif op in ("Thread Exit", "Process Exit"):
        events.append(("EXIT", r))
    elif op == "CreateFile" and "wd\\" in p.lower() and r["Result"] == "NAME NOT FOUND":
        events.append(("MISS", r))
events.sort(key=lambda x: x[1]["Time of Day"])
lines.append(f"time-ordered events: {len(events)}")
for kind, r in events:
    p = r["Path"]
    short = p.split("\\")[-1] if p else ""
    lines.append(f"{r['Time of Day'][3:21]} {kind:6} {r['Operation'][:18]:18} {short[:60]:60} {r['Result'][:12]}")

# (b) UTF-16 + ANSI string census for the resolution strings
d = open(EXE, "rb").read()
STRINGS = ["EnumDisplayDevices", "EnumDisplayDevicesA", "EnumDisplaySettings", "EnumDisplaySettingsA",
           "EnumDisplaySettingsExA", "ChangeDisplaySettings", "ChangeDisplaySettingsA",
           "GetSystemMetrics", "GetDeviceCaps", "user32", "USER32", "d3d9", "D3D9",
           "Direct3DCreate9", "GetClientRect", "CreateWindowExA", "FindWindowA"]
lines.append("\n=== string census (ANSI + UTF16LE) ===")


def off2va(off):
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    t = pe + 24 + opt
    for i in range(nsec):
        name = d[t:t + 8].rstrip(b"\x00").decode()
        vsize, va, rsize, raw = struct.unpack_from("<IIII", d, t + 8)
        if raw <= off < raw + rsize:
            return 0x400000 + va + (off - raw)
        t += 40
    return None


for s in STRINGS:
    hits = []
    a = s.encode()
    u = s.encode("utf-16-le")
    for pat, form in ((a, "ansi"), (u, "utf16")):
        i = d.find(pat)
        while i != -1 and len(hits) < 12:
            va = off2va(i)
            if va:
                hits.append(f"{va:#x}({form})")
            i = d.find(pat, i + 1)
    if hits:
        lines.append(f"  {s}: {' '.join(hits)}")
    else:
        lines.append(f"  {s}: ABSENT")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
