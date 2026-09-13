# -*- coding: utf-8 -*-
# Quick check of the class-id token bytes in MSVC mangling.
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
data = open(EXE, "rb").read()
for label, va in [("ParameterTransformation", 0x00B8DA28), ("RealWorldItem", 0x00B8DD18),
                  ("ParameterContainer", 0x00B8DAF0), ("SetObject", 0x00B8DEB0)]:
    off = 7782400 + (va - 0x00B6C000)
    z = data[off:off+90].split(b"\x00")[0]
    tok_start = z.find(b"$0")
    tok = z[tok_start+2:].split(b"@")[0]
    print(label)
    print("  full :", z.decode())
    print("  token:", [hex(b) for b in tok], "chars:", tok.decode())
    # MSVC: $0<hex>@ ; try hex interpretation if valid
    try:
        v = int(tok.decode(), 16)
        print("  hex-interpretation: 0x%X = %d" % (v, v))
    except ValueError:
        print("  hex-interpretation: INVALID (contains non-hex chars)")
