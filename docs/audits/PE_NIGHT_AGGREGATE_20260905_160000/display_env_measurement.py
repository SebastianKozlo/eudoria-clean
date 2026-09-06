#!/usr/bin/env python3
"""THE DISPLAY ENVIRONMENT MEASUREMENT (read-only, zero game client).
What does the display enumeration return on THIS machine (the Hyper-V/Remote-Display VM)?
(a) EnumDisplayDevicesA for iDev 0..5 (the adapter identity + state flags);
(b) EnumDisplaySettingsExA per device (the mode list);
(c) the registry Class\\{4d36e968...}\\00NN keys + their value names;
(d) HKLM\\HARDWARE\\DEVICEMAP\\VIDEO values.
This closes the ENVIRONMENT side of the display-enum canon gap."""
import ctypes
import winreg

out = []
user32 = ctypes.windll.user32


class DISPLAY_DEVICEA(ctypes.Structure):
    _fields_ = [("cb", ctypes.c_ulong),
                ("DeviceName", ctypes.c_char * 32),
                ("DeviceString", ctypes.c_char * 128),
                ("StateFlags", ctypes.c_ulong),
                ("DeviceID", ctypes.c_char * 128),
                ("DeviceKey", ctypes.c_char * 128)]


class DEVMODEA(ctypes.Structure):
    _fields_ = [("dmDeviceName", ctypes.c_char * 32),
                ("dmSpecVersion", ctypes.c_ushort),
                ("dmDriverVersion", ctypes.c_ushort),
                ("dmSize", ctypes.c_ushort),
                ("dmDriverExtra", ctypes.c_ushort),
                ("dmFields", ctypes.c_ulong),
                ("dmPositionX", ctypes.c_long),
                ("dmPositionY", ctypes.c_long),
                ("dmScreenOrientation", ctypes.c_ulong),
                ("dmDisplayFixedOutput", ctypes.c_ulong),
                ("dmColor", ctypes.c_ushort),
                ("dmDuplex", ctypes.c_ushort),
                ("dmYResolution", ctypes.c_ushort),
                ("dmTTOption", ctypes.c_ushort),
                ("dmCollate", ctypes.c_ushort),
                ("dmFormName", ctypes.c_char * 32),
                ("dmLogPixels", ctypes.c_ushort),
                ("dmBitsPerPel", ctypes.c_ulong),
                ("dmPelsWidth", ctypes.c_ulong),
                ("dmPelsHeight", ctypes.c_ulong),
                ("dmDisplayFlags", ctypes.c_ulong),
                ("dmDisplayFrequency", ctypes.c_ulong),
                ("dmICMMethod", ctypes.c_ulong),
                ("dmICMIntent", ctypes.c_ulong),
                ("dmMediaType", ctypes.c_ulong),
                ("dmDisplayType", ctypes.c_ulong),
                ("dmReserved1", ctypes.c_ulong),
                ("dmReserved2", ctypes.c_ulong),
                ("dmPanningWidth", ctypes.c_ulong),
                ("dmPanningHeight", ctypes.c_ulong)]


user32.EnumDisplaySettingsExA.argtypes = [ctypes.c_char_p, ctypes.c_uint,
                                          ctypes.POINTER(DEVMODEA), ctypes.c_uint]

out.append("=== EnumDisplayDevicesA(NULL, iDev, 0) — the adapters ===")
for i in range(6):
    dd = DISPLAY_DEVICEA()
    dd.cb = ctypes.sizeof(dd)
    ok = user32.EnumDisplayDevicesA(None, i, ctypes.byref(dd), 0)
    if not ok:
        out.append(f"  iDev={i}: EnumDisplayDevicesA returned FALSE (enumeration end)")
        break
    out.append(f"  iDev={i}: ok={ok}")
    out.append(f"    DeviceName  = {dd.DeviceName.decode('ascii', 'replace')}")
    out.append(f"    DeviceString= {dd.DeviceString.decode('ascii', 'replace')}")
    out.append(f"    StateFlags  = {dd.StateFlags:#010x} (ATTACHED={bool(dd.StateFlags & 1)}, "
               f"PRIMARY={bool(dd.StateFlags & 2)}, MIRRORING={bool(dd.StateFlags & 8)}, "
               f"VGA_COMPATIBLE={bool(dd.StateFlags & 16)}, REMOVABLE={bool(dd.StateFlags & 32)}, "
               f"MODESPRUNED={bool(dd.StateFlags & 0x8000000)})")
    out.append(f"    DeviceID    = {dd.DeviceID.decode('ascii', 'replace')}")
    out.append(f"    DeviceKey   = {dd.DeviceKey.decode('ascii', 'replace')}")
    j = 0
    cnt = 0
    modes = []
    while True:
        dm = DEVMODEA()
        dm.dmSize = ctypes.sizeof(DEVMODEA)
        okm = user32.EnumDisplaySettingsExA(dd.DeviceName, j, ctypes.byref(dm), 0)
        if not okm:
            break
        if j == 0:
            modes.append(f"current: {dm.dmPelsWidth}x{dm.dmPelsHeight}@{dm.dmDisplayFrequency}Hz {dm.dmBitsPerPel}bpp")
        cnt += 1
        j += 1
    out.append(f"    modes(EnumDisplaySettingsExA j={j}): {cnt}; {modes}")

out.append("\n=== EnumDisplayDevicesA(NULL, iDev, 1) — the monitors ===")
for i in range(4):
    dd = DISPLAY_DEVICEA()
    dd.cb = ctypes.sizeof(dd)
    ok = user32.EnumDisplayDevicesA(None, i, ctypes.byref(dd), 1)
    if not ok:
        out.append(f"  iDev={i}: FALSE")
        break
    out.append(f"  iDev={i}: {dd.DeviceName.decode('ascii', 'replace')} | "
               f"{dd.DeviceString.decode('ascii', 'replace')[:40]} | flags {dd.StateFlags:#x}")

out.append("\n=== The registry display-class keys (the Class GUID 4d36e968...) ===")
CLS = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
try:
    root = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, CLS)
    i = 0
    while True:
        try:
            sub = winreg.EnumKey(root, i)
        except OSError:
            break
        if sub.isdigit():
            try:
                k = winreg.OpenKey(root, sub)
                vals = []
                vi = 0
                while True:
                    try:
                        vals.append(winreg.EnumValue(k, vi)[0])
                    except OSError:
                        break
                    vi += 1
                out.append(f"  {sub}: values={vals[:16]}")
                out.append(f"      has MatchingDeviceID: {'MatchingDeviceID' in vals}")
                k.Close()
            except OSError as ex:
                out.append(f"  {sub}: open error {ex}")
        i += 1
    root.Close()
except OSError as ex:
    out.append(f"  class key error: {ex}")

out.append("\n=== HKLM\\HARDWARE\\DEVICEMAP\\VIDEO values ===")
try:
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DEVICEMAP\VIDEO")
    i = 0
    while True:
        try:
            name, data, typ = winreg.EnumValue(k, i)
        except OSError:
            break
        out.append(f"  {name} = {str(data)[:110]}")
        i += 1
except OSError as ex:
    out.append(f"  error: {ex}")

OUTP = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\DISPLAY_ENV_MEASUREMENT.txt"
open(OUTP, "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
