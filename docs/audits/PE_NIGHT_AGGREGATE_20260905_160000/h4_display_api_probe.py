# -*- coding: utf-8 -*-
"""THE DISPLAY-API PROBE (32-bit): call each display API SEQUENTIALLY with long
sleeps + stdout markers, under ProcMon -> the CSV correlates WHICH API performs
the DEVICEMAP/HardwareInformation.MemorySize registry reads on THIS machine."""
import ctypes
import time

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
ms = lambda: time.strftime("%H:%M:%S") + ".{:03d}".format(int(time.time() % 1 * 1000))


def mark(label):
    print("MARK {} {}".format(ms(), label), flush=True)


class DISPLAY_DEVICEA(ctypes.Structure):
    _fields_ = [("cb", ctypes.c_ulong), ("DeviceName", ctypes.c_char * 32),
                ("DeviceString", ctypes.c_char * 128), ("StateFlags", ctypes.c_ulong),
                ("DeviceID", ctypes.c_char * 128), ("DeviceKey", ctypes.c_char * 128)]


mark("A_GETDC_BEGIN")
hdc = user32.GetDC(None)
mark("A_GETDC_END hdc={}".format(hdc))
time.sleep(2.0)

for idx, cap in ((4, "DRIVERVERSION"), (2, "ASPECTX"), (8, "BITSPIXEL"), (88, "HORZRES")):
    mark("B_GETDEVICECAPS_{}_BEGIN".format(cap))
    v = gdi32.GetDeviceCaps(hdc, idx)
    mark("B_GETDEVICECAPS_{}_END v={}".format(cap, v))
    time.sleep(1.5)

mark("C_GETSYSTEMMETRICS_BEGIN")
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)
mark("C_GETSYSTEMMETRICS_END {}x{}".format(w, h))
time.sleep(1.5)

mark("D_ENUMDISPLAYDEVICES_BEGIN")
dd = DISPLAY_DEVICEA()
dd.cb = ctypes.sizeof(dd)
ok = user32.EnumDisplayDevicesA(None, 0, ctypes.byref(dd), 0)
mark("D_ENUMDISPLAYDEVICES_END ok={} flags={:#x}".format(ok, dd.StateFlags))
time.sleep(1.5)

mark("E_CREATEDCA_BEGIN")
hdc2 = gdi32.CreateDCA("DISPLAY", None, None, None)
mark("E_CREATEDCA_END hdc={}".format(hdc2))
time.sleep(1.5)

mark("F_RELEASEDC")
user32.ReleaseDC(None, hdc)
mark("DONE")
