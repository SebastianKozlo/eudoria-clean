# -*- coding: utf-8 -*-
"""The CreateDCA failure analysis (32-bit): the error code + the variants."""
import ctypes

gdi32 = ctypes.windll.gdi32
k32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

k32.SetLastError(0)
h = gdi32.CreateDCA(b"DISPLAY", None, None, None)
e = k32.GetLastError()
print("CreateDCA('DISPLAY') = {} GetLastError = {} ({:#x})".format(h, e, e & 0xFFFFFFFF))

k32.SetLastError(0)
h2 = gdi32.CreateDCA(b"DISPLAY", b"DISPLAY", None, None)
e2 = k32.GetLastError()
print("CreateDCA('DISPLAY','DISPLAY') = {} err = {}".format(h2, e2))

# the EnumDisplayDevices-based device name form:
class DISPLAY_DEVICEA(ctypes.Structure):
    _fields_ = [("cb", ctypes.c_ulong), ("DeviceName", ctypes.c_char * 32),
                ("DeviceString", ctypes.c_char * 128), ("StateFlags", ctypes.c_ulong),
                ("DeviceID", ctypes.c_char * 128), ("DeviceKey", ctypes.c_char * 128)]


dd = DISPLAY_DEVICEA()
dd.cb = ctypes.sizeof(dd)
if user32.EnumDisplayDevicesA(None, 0, ctypes.byref(dd), 0):
    dev = dd.DeviceName
    print("device0 name:", dev)
    k32.SetLastError(0)
    h3 = gdi32.CreateDCA(dev, None, None, None)
    e3 = k32.GetLastError()
    print("CreateDCA('{}') = {} err = {}".format(dev.decode(), h3, e3))

# GetDC for reference
hdc = user32.GetDC(None)
print("GetDC(NULL) = {}".format(hdc))
print("GetDeviceCaps(hdc, BITSPIXEL=12) =", gdi32.GetDeviceCaps(hdc, 12))
print("GetDeviceCaps(hdc, HORZRES=8) =", gdi32.GetDeviceCaps(hdc, 8))
user32.ReleaseDC(None, hdc)
