# -*- coding: utf-8 -*-
"""THE DIRECTINPUT8 EMPIRICAL TEST (32-bit python): replicate the client's exact init:
  hr1 = DirectInput8Create(hInst, 0x0800, IID_IDirectInput8A, &di, NULL);
  if (hr1 >= 0) hr2 = di->EnumDevices(...)   [the vtable+0xC path]
If hr1 or hr2 < 0 on this machine => THE PREDICATE CONFIRMED EMPIRICALLY."""
import ctypes
import ctypes.wintypes as wt

k32 = ctypes.windll.kernel32
hinst = k32.GetModuleHandleA(None)

dinput8 = ctypes.WinDLL("dinput8.dll")

# GUID IDirectInput8A = {BF798070-482A-4C4E-9D3D-D5E6BF798070... actually:
IID_IDirectInput8A = (ctypes.c_ubyte * 16)(
    0x70, 0x80, 0x79, 0xBF, 0x2A, 0x48, 0x4E, 0x4C,
    0x9D, 0x3D, 0xD5, 0xE6, 0xBF, 0x79, 0x80, 0x70)

# THE IID VERBATIM FROM THE CLIENT BINARY @0xA9BED4 (.rdata): {BF798030-483A-4DA2-AA99-5D64ED369700}
IID = (ctypes.c_ubyte * 16)(
    0x30, 0x80, 0x79, 0xBF, 0x3A, 0x48, 0xA2, 0x4D,
    0xAA, 0x99, 0x5D, 0x64, 0xED, 0x36, 0x97, 0x00)

out = ctypes.c_void_p()
hr = dinput8.DirectInput8Create(hinst, 0x0800, ctypes.byref(IID), ctypes.byref(out), None)
print("DirectInput8Create hr = 0x{:08X} ({})".format(hr & 0xFFFFFFFF, "FAILED" if hr < 0 else "OK"))
print("out ptr = {}".format(out.value))

if hr >= 0 and out.value:
    # the vtable walk: *out = the object; **out = the vtable; vtable[3] (0xC/4) = EnumDevices
    obj = ctypes.cast(out, ctypes.c_void_p)
    vtbl = ctypes.cast(ctypes.cast(obj, ctypes.POINTER(ctypes.c_void_p)).contents,
                       ctypes.POINTER(ctypes.c_void_p))
    print("vtable[0] = {}".format(hex(vtbl[0] or 0)))
    enumdevs = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_uint,
                                  ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint)(vtbl[3])
    # the enum callback: BOOL CALLBACK(LPCDIDEVICEINSTANCEA, PVREF) -> continue
    CBC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)

    def cb(inst, ref):
        print("  device enumerated (callback fired)")
        return 1  # DIENUM_CONTINUE

    # EnumDevices(dwDevType=DI8DEVCLASS_ALL(0), lpCallback, pvRef, dwFlags=0)
    hr2 = enumdevs(obj, 0, CBC(cb), None, 0)
    print("EnumDevices hr = 0x{:08X} ({})".format(hr2 & 0xFFFFFFFF, "FAILED" if hr2 < 0 else "OK"))
else:
    print("(no EnumDevices test — the create failed)")
