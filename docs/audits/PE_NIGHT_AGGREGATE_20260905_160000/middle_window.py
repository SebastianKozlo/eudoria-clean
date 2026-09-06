#!/usr/bin/env python3
"""The middle-window analysis: d3d8, DEVICEMAP, cfg files, and the display-API imports."""
import csv
import struct

CSV = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test\entropia_death_trace.csv"
EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\MIDDLE_WINDOW_AND_IMPORTS.txt"

lines = []
rows = list(csv.DictReader(open(CSV, encoding="utf-8", errors="replace")))
T = '\ufeff"Time of Day"'
for r in rows:
    r["Time of Day"] = r.pop(T)
e = [r for r in rows if r["Process Name"] == "Entropia.exe"]

for label, kw in (("d3d8.dll", ("d3d8.dll",)), ("DEVICEMAP", ("DEVICEMAP",)),
                  ("cfg/ini/log", (".cfg", ".ini", "entropia.log", "config"))):
    hits = [r for r in e if any(s in r["Path"].lower() for s in kw)]
    lines.append(f"=== {label}: {len(hits)} rows")
    for r in hits[:12]:
        lines.append(f"  {r['Time of Day'][3:21]} {r['Operation'][:20]:20} {r['Path'][:84]:84} {r['Result'][:14]} {(r.get('Detail') or '')[:50]}")

# the window between the first DEVICEMAP read and Process Exit — full dump
try:
    vi = next(i for i, r in enumerate(e) if "DEVICEMAP" in r["Path"])
    lines.append(f"\n=== FULL WINDOW from first DEVICEMAP read (idx {vi}) to exit ({len(e)}) ===")
    for r in e[vi:vi + 60]:
        lines.append(f"  {r['Time of Day'][3:21]} {r['Operation'][:22]:22} {r['Path'][:86]:86} {r['Result'][:16]}")
except StopIteration:
    lines.append("no DEVICEMAP rows")

# the display-API imports of the client (the enumeration path identification)
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
imp_rva = struct.unpack_from("<I", d, pe + 24 + 96 + 8)[0]  # DataDirectory[1] import
lines.append(f"\nimport dir RVA: {imp_rva:#x}")
# section map
secs = []
t = pe + 24 + opt
for i in range(nsec):
    name = d[t:t + 8].rstrip(b"\x00").decode()
    vsize, va, rsize, raw = struct.unpack_from("<IIII", d, t + 8)
    secs.append((name, va, vsize, raw, rsize))
    t += 40


def rva2off(rva):
    for name, va, vsz, raw, rsz in secs:
        if va <= rva < va + vsz:
            return raw + (rva - va)
    return None


o = rva2off(imp_rva)
DISPLAY_APIS = (b"EnumDisplayDevices", b"EnumDisplaySettings", b"EnumDisplaySettingsEx",
                b"ChangeDisplaySettings", b"ChangeDisplaySettingsEx", b"GetDeviceCaps",
                b"CreateDC", b"CreateDCA", b"GetSystemMetrics", b"GetMonitorInfo",
                b"EnumDisplayMonitors", b"MonitorFromWindow", b"DirectDrawCreate",
                b"Direct3DCreate8", b"Direct3DCreate9")
lines.append("\n=== DISPLAY-RELATED IMPORTS (per DLL) ===")
while True:
    oft, ts, fwd, nameRva, fthunk = struct.unpack_from("<IIIII", d, o)
    if nameRva == 0:
        break
    dll = d[rva2off(nameRva):rva2off(nameRva) + 32].split(b"\x00")[0].decode()
    thunk = rva2off(oft if oft else fthunk)
    funcs = []
    while True:
        val = struct.unpack_from("<I", d, thunk)[0]
        if val == 0:
            break
        if not (val >> 31):
            fn = d[rva2off(val) + 2:rva2off(val) + 40].split(b"\x00")[0].decode("ascii", "replace")
            if any(fn.startswith(api.decode()) for api in DISPLAY_APIS):
                funcs.append(fn)
        thunk += 4
    if funcs:
        lines.append(f"  {dll}: {', '.join(funcs)}")
    o += 20

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines[:100]))
