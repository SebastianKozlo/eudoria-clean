#!/usr/bin/env python3
"""The display-enum canon gap — static byte census:
(a) the display/API-name strings in the image (runtime GetProcAddress resolution);
(b) the ExitProcess(-1) call sites (PUSH -1; call ExitProcess + variants);
(c) the LoadLibraryA("D3D8.DLL") route strings (the TMF canon)."""
import json
import struct

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000"
OUT = RUN + r"\DISPLAY_ENUM_STATIC_CENSUS.json"

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
t = pe + 24 + opt
for i in range(nsec):
    name = d[t:t + 8].rstrip(b"\x00").decode()
    vsize, va, rsize, raw = struct.unpack_from("<IIII", d, t + 8)
    secs.append((name, va, vsize, raw, rsize))
    t += 40


def off2va(off):
    for name, va, vsz, raw, rsz in secs:
        if raw <= off < raw + rsz:
            return 0x400000 + va + (off - raw)
    return None


def va2off(va):
    rva = va - 0x400000
    for name, sva, vsz, raw, rsz in secs:
        if sva <= rva < sva + vsz:
            return raw + (rva - sva)
    return None


out = {"strings": {}, "exit_minus_one": []}

# (a) the API-name strings
STRINGS = ["EnumDisplayDevices", "EnumDisplayDevicesA", "EnumDisplayDevicesExA", "EnumDisplaySettings",
           "EnumDisplaySettingsEx", "EnumDisplaySettingsA", "ChangeDisplaySettings", "ChangeDisplaySettingsA",
           "ChangeDisplaySettingsExA", "GetDeviceCaps", "CreateDCA", "CreateDCW", "GetSystemMetrics",
           "GetMonitorInfoA", "EnumDisplayMonitors", "MonitorFromWindow", "Direct3DCreate8",
           "Direct3DCreate9", "DirectDrawCreateEx", "D3D8.DLL", "d3d8.dll", "user32.dll", "USER32.DLL",
           "dxdiagn.dll", "DXDIAG", "GetAdapterIdentifier", "GetAdapterModeCount", "GetAdapterDisplayMode"]
for s in STRINGS:
    pat = s.encode()
    hits = []
    i = d.find(pat)
    while i != -1 and len(hits) < 30:
        va = off2va(i)
        if va:
            hits.append(va)
        i = d.find(pat, i + 1)
    if hits:
        out["strings"][s] = [hex(v) for v in hits]

# (b) ExitProcess(-1) call sites:
#   pattern A: 6A FF (push -1) ... E8 <rel to ExitProcess>
#   pattern B: 68 FF FF FF FF (push -1) ... E8
# first: locate ExitProcess in the import table (IAT entry address + the thunk)
imp_rva = struct.unpack_from("<I", d, pe + 24 + 96 + 8)[0]


def rva2off(rva):
    return va2off(0x400000 + rva)


o = rva2off(imp_rva)
exitprocess_iat = None
while True:
    oft, ts, fwd, nameRva, fthunk = struct.unpack_from("<IIIII", d, o)
    if nameRva == 0:
        break
    dll = d[rva2off(nameRva):rva2off(nameRva) + 32].split(b"\x00")[0].decode()
    if dll.lower().startswith("kernel32"):
        thunk = rva2off(oft if oft else fthunk)
        iat_va = 0x400000 + fthunk
        while True:
            val = struct.unpack_from("<I", d, thunk)[0]
            if val == 0:
                break
            if not (val >> 31):
                fn = d[rva2off(val) + 2:rva2off(val) + 40].split(b"\x00")[0].decode("ascii", "replace")
                if fn == "ExitProcess":
                    exitprocess_iat = iat_va
                iat_va += 4
            thunk += 4
    o += 20
out["ExitProcess_IAT_VA"] = hex(exitprocess_iat) if exitprocess_iat else None

# find CALL [ExitProcess] sites: FF 15 <iat_va> (indirect call dword ptr [addr])
if exitprocess_iat:
    pat = b"\xFF\x15" + struct.pack("<I", exitprocess_iat)
    sites = []
    i = d.find(pat)
    while i != -1 and len(sites) < 60:
        va = off2va(i)
        if va:
            # the preceding bytes: push -1?
            pre = d[i - 12:i]
            tag = None
            if pre.endswith(b"\x6A\xFF"):
                tag = "push -1 (byte) adjacent"
            elif b"\x68\xFF\xFF\xFF\xFF" in pre:
                tag = "push -1 (dword) near"
            sites.append({"call_va": hex(va), "preceding": pre.hex(), "tag": tag})
        i = d.find(pat, i + 1)
    out["call_ExitProcess_sites"] = sites

with open(OUT, "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=1))
