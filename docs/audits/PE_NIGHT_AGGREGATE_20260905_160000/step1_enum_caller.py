#!/usr/bin/env python3
"""Step 1 of the -1 predicate hunt: (a) the exe's per-DLL imports for DINPUT8/d3dx9_30;
(b) which of the loaded modules import EnumDisplayDevices/EnumDisplaySettings
(the in-process enum caller identification). Read-only."""
import struct

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\STEP1_ENUM_CALLER_CENSUS.txt"
lines = []

d = open(EXE, "rb").read()


def parse_imports(path, tag):
    try:
        b = open(path, "rb").read()
    except OSError as ex:
        return [(f"{tag}: unreadable {ex}")]
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if b[:2] != b"MZ":
        return [(f"{tag}: not MZ")]
    nsec = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    imp_rva = struct.unpack_from("<I", b, pe + 24 + 96 + 8)[0]
    secs = []
    t = pe + 24 + opt
    for i in range(nsec):
        name = b[t:t + 8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, va, rsize, raw = struct.unpack_from("<IIII", b, t + 8)
        secs.append((name, va, vsize, raw, rsize))
        t += 40

    def rva2off(rva):
        for name, va, vsz, raw, rsz in secs:
            if va <= rva < va + vsz:
                return raw + (rva - va)
        return None

    res = []
    o = rva2off(imp_rva)
    if o is None:
        return [(f"{tag}: no import dir")]
    while True:
        oft, ts, fwd, nameRva, fthunk = struct.unpack_from("<IIIII", b, o)
        if nameRva == 0:
            break
        no = rva2off(nameRva)
        dll = b[no:no + 32].split(b"\x00")[0].decode("ascii", "replace") if no else "?"
        thunk = rva2off(oft if oft else fthunk)
        funcs = []
        while thunk:
            val = struct.unpack_from("<I", b, thunk)[0]
            if val == 0:
                break
            if not (val >> 31):
                fo = rva2off(val)
                if fo:
                    fn = b[fo + 2:fo + 48].split(b"\x00")[0].decode("ascii", "replace")
                    funcs.append(fn)
            thunk += 4
        res.append((dll, funcs))
        o += 20
    return res


# (a) the exe's imports for DINPUT8 + d3dx9_30
lines.append("=== THE EXE's imports (DINPUT8 / d3dx9_30 focus) ===")
for dll, funcs in parse_imports(EXE, "exe"):
    if dll.lower().startswith(("dinput8", "d3dx9")):
        lines.append(f"  {dll}: {len(funcs)} imports:")
        for fn in funcs:
            lines.append(f"    {fn}")

# (b) which loaded modules import the display-enum APIs
MODS = [r"C:\Windows\SysWOW64\dinput8.dll", r"C:\Windows\SysWOW64\d3dx9_30.dll",
        r"C:\Windows\SysWOW64\dsound.dll", r"C:\Windows\SysWOW64\winmm.dll",
        r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\dpvs.dll",
        r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\mac3r.dll",
        r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\wmvcore.dll"]
lines.append("\n=== The display-enum API importers among the loaded modules ===")
for m in MODS:
    try:
        imps = parse_imports(m, m.split("\\")[-1])
    except Exception as ex:
        lines.append(f"  {m}: ERROR {ex}")
        continue
    tag = m.split("\\")[-1]
    for dll, funcs in imps:
        disp = [f for f in funcs if "Display" in f or f.startswith(("GetSystemMetrics", "GetDeviceCaps", "CreateDC"))]
        if disp:
            lines.append(f"  {tag} -> {dll}: {disp}")
    # the module's exports of interest (DirectInput8Create etc.)
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
