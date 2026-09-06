# -*- coding: utf-8 -*-
"""THE DIRECTINPUT8 EMPIRICAL TEST v2 (32-bit): the client's EXACT calls:
- vtable[3] (offset 0xC) = IDirectInput8::CreateDevice(rguid, &pdev, NULL)
- vtable[4] (offset 0x10) = IDirectInput8::EnumDevices(dwDevType, cb, ref, flags)
With the standard device GUIDs (SysMouse/SysKeyboard) + DI8DEVCLASS_ALL."""
import ctypes

k32 = ctypes.windll.kernel32
hinst = k32.GetModuleHandleA(None)
dinput8 = ctypes.WinDLL("dinput8.dll")

# THE IID VERBATIM FROM THE CLIENT BINARY @0xA9BED4:
IID = (ctypes.c_ubyte * 16)(
    0x30, 0x80, 0x79, 0xBF, 0x3A, 0x48, 0xA2, 0x4D,
    0xAA, 0x99, 0x5D, 0x64, 0xED, 0x36, 0x97, 0x00)

GUID_SysMouse = (ctypes.c_ubyte * 16)(
    0x60, 0x2B, 0x1D, 0x6F, 0xA0, 0xD5, 0xCF, 0x11,
    0xBF, 0xC7, 0x44, 0x45, 0x53, 0x54, 0x00, 0x00)
GUID_SysKeyboard = (ctypes.c_ubyte * 16)(
    0x61, 0x2B, 0x1D, 0x6F, 0xA0, 0xD5, 0xCF, 0x11,
    0xBF, 0xC7, 0x44, 0x45, 0x53, 0x54, 0x00, 0x00)

out = ctypes.c_void_p()
hr = dinput8.DirectInput8Create(hinst, 0x0800, ctypes.byref(IID), ctypes.byref(out), None)
print("DirectInput8Create hr = 0x{:08X} ({})".format(hr & 0xFFFFFFFF, "OK" if hr >= 0 else "FAILED"))
if hr >= 0 and out.value:
    obj = ctypes.cast(out, ctypes.c_void_p)
    vtbl = ctypes.cast(ctypes.cast(obj, ctypes.POINTER(ctypes.c_void_p)).contents,
                      ctypes.POINTER(ctypes.c_void_p))

    # vtable[3] = CreateDevice(this, rguid, &pdev, punkOuter)
    createdev = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p,
                                   ctypes.c_void_p, ctypes.c_void_p,
                                   ctypes.c_void_p)(vtbl[3])
    for gname, g in (("GUID_SysMouse", GUID_SysMouse), ("GUID_SysKeyboard", GUID_SysKeyboard)):
        pdev = ctypes.c_void_p()
        hrc = createdev(obj, ctypes.byref(g), ctypes.byref(pdev), None)
        print("CreateDevice({}) hr = 0x{:08X} ({}) dev={}".format(
            gname, hrc & 0xFFFFFFFF, "OK" if hrc >= 0 else "FAILED",
            hex(pdev.value or 0)))

    # vtable[4] = EnumDevices(this, dwDevType, lpCallback, pvRef, dwFlags)
    enumdevs = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_uint,
                                  ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint)(vtbl[4])
    CBC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
    n = [0]

    def cb(inst, ref):
        n[0] += 1
        return 1  # DIENUM_CONTINUE

    hr2 = enumdevs(obj, 0, CBC(cb), None, 0)  # DI8DEVCLASS_ALL, DIEDFL_ALLDEVICES
    print("EnumDevices hr = 0x{:08X} ({}) devices={}".format(
        hr2 & 0xFFFFFFFF, "OK" if hr2 >= 0 else "FAILED", n[0]))
else:
    print("(create failed — no further tests)")
