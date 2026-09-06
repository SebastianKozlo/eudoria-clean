#!/usr/bin/env python3
"""The death Detail column + d3d9 in the trace + the DLL imports (whose code enumerates)."""
import csv
import struct

CSV = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_AUTOMATION_R1_20260905_140126\04_RUNTIME\live_test\entropia_death_trace.csv"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\DEATH_DETAIL_AND_DLL_IMPORTS.txt"
lines = []

rows = list(csv.DictReader(open(CSV, encoding="utf-8", errors="replace")))
T = '\ufeff"Time of Day"'
for r in rows:
    r["Time of Day"] = r.pop(T)
e = [r for r in rows if r["Process Name"] == "Entropia.exe"]

# (a) every row from the first DEVICEMAP open, WITH the Detail column
vi = next(i for i, r in enumerate(e) if "DEVICEMAP" in r["Path"])
lines.append("=== THE DEATH WINDOW WITH DETAILS ===")
for r in e[vi:vi + 40]:
    lines.append(f"{r['Time of Day'][3:21]} {r['Operation'][:20]:20} {r['Path'][:80]:80} {r['Result'][:14]:14} {(r.get('Detail') or '')[:70]}")

# (b) d3d9 in the trace
d3d9 = [r for r in e if "d3d9" in r["Path"].lower()]
lines.append(f"\n=== d3d9 rows: {len(d3d9)}")
for r in d3d9[:12]:
    lines.append(f"  {r['Operation'][:20]:20} {r['Path'][:80]:80} {r['Result'][:14]}")

# (c) what OTHER DLLs loaded (the full Load Image census of the death run)
loads = [r for r in e if r["Operation"] == "Load Image"]
lines.append(f"\n=== Load Image rows: {len(loads)}")
for r in loads:
    lines.append(f"  {r['Path'][:100]}")

# (d) the imports of the suspect DLLs (d3dx9_30 from SysWOW64; DINPUT8)
for dll in (r"C:\Windows\SysWOW64\d3dx9_30.dll", r"C:\Windows\SysWOW64\DINPUT8.dll"):
    try:
        d = open(dll, "rb").read()
    except OSError as ex:
        lines.append(f"\n{dll}: UNREADABLE {ex}")
        continue
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    imp_rva = struct.unpack_from("<I", d, pe + 24 + 96 + 8)[0]
    secs = []
    t = pe + 24 + opt
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
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
    lines.append(f"\n=== IMPORTS of {dll}")
    while True:
        oft, ts, fwd, nameRva, fthunk = struct.unpack_from("<IIIII", d, o)
        if nameRva == 0:
            break
        dllname = d[rva2off(nameRva):rva2off(nameRva) + 32].split(b"\x00")[0].decode()
        thunk = rva2off(oft if oft else fthunk)
        funcs = []
        while True:
            val = struct.unpack_from("<I", d, thunk)[0]
            if val == 0:
                break
            if not (val >> 31):
                fn = d[rva2off(val) + 2:rva2off(val) + 48].split(b"\x00")[0].decode("ascii", "replace")
                funcs.append(fn)
            thunk += 4
        disp = [f for f in funcs if any(k in f for k in ("Display", "DeviceCaps", "SystemMetrics", "Monitor", "CreateDC"))]
        lines.append(f"  {dllname}: {len(funcs)} imports; display-relevant: {disp}")
        o += 20

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
