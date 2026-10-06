# pin_getter.py - re-pin FUN_00414130 from the physical EXE and dump its window.
# Also dumps the boundary context (bytes before/after the function) and the
# published-canon cross-check inputs. Output: 01_RAW/GETTER_PIN.txt + JSON.

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe935k_core import Exe, hexs, EXE_PATH

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_RAW")
os.makedirs(OUT, exist_ok=True)

GETTER_VA = 0x00414130

ex = Exe()
hdr = {
    "exe_path": EXE_PATH,
    "size_bytes": len(ex.raw),
    "image_base": "0x%08X" % ex.image_base,
    "aslr": ex.aslr,
    "size_of_image": "0x%08X" % ex.size_of_image,
    "sections": [
        {"name": s["name"], "va": "0x%08X" % (ex.image_base + s["virtual_address"]),
         "vsize": "0x%X" % s["virtual_size"], "raw_size": "0x%X" % s["raw_size"],
         "raw_ptr": "0x%X" % s["raw_pointer"]} for s in ex.sections
    ],
}

# PE header spot checks (era pins: base 0x00400000, ASLR OFF, .text RVA 0x1000)
spot = {
    "image_base_expected": "0x00400000",
    "image_base_match": ex.image_base == 0x00400000,
    "aslr_expected": False,
    "aslr_match": ex.aslr is False,
    "text_rva_expected": 0x1000,
    "text_rva_match": any(s["name"] == ".text" and s["virtual_address"] == 0x1000 for s in ex.sections),
}

# getter bytes at VA 0x00414130
gb = ex.read(GETTER_VA, 16)
window_before = ex.read(GETTER_VA - 16, 16)

# manual decode of the 4-byte candidate: 8B 41 74 C3 = mov eax,[ecx+0x74]; ret
def decode_getter(b):
    if b is None or len(b) < 4:
        return {"decoded": False, "reason": "short read"}
    d = {}
    d["b0_8B"] = (b[0] == 0x8B)
    d["b1_41_modrm"] = (b[1] == 0x41)  # mod=01 reg=000 eax rm=001 ecx
    if b[1] == 0x41:
        mod = (b[1] >> 6) & 3
        reg = (b[1] >> 3) & 7
        rm = b[1] & 7
        d["modrm_mod"] = mod
        d["modrm_reg"] = reg  # 000 = EAX
        d["modrm_rm"] = rm   # 001 = ECX
        d["disp8"] = b[2]
        d["disp8_hex"] = "0x%02X" % b[2]
    d["b3_C3_ret"] = (b[3] == 0xC3)
    d["decoded"] = bool(d["b0_8B"] and d["b1_41_modrm"] and d["b3_C3_ret"])
    d["text"] = ("mov eax,[ecx+0x%02X]; ret" % b[2]) if d["decoded"] else "NO-DECODE"
    return d

dec = decode_getter(gb)

# VA->file offset resolution for the getter
off = ex.va_to_off(GETTER_VA)

result = {
    "measurement": "FUN_00414130 byte pin from physical EXE",
    "exe_identity": hdr,
    "pe_spot_checks": spot,
    "getter": {
        "va": "0x%08X" % GETTER_VA,
        "file_offset": "0x%X" % off if off is not None else None,
        "bytes_hex": hexs(gb),
        "decode": dec,
        "window_before_va_0x00414120": hexs(window_before),
    },
}

with open(os.path.join(OUT, "GETTER_PIN.json"), "w") as f:
    json.dump(result, f, indent=1)

# text report
lines = []
lines.append("FUN_00414130 GETTER PIN (physical EXE: %s)" % EXE_PATH)
lines.append("image_base=0x%08X ASLR=%s" % (ex.image_base, ex.aslr))
lines.append("PE spot checks: %s" % json.dumps(spot))
lines.append(".text range: 0x%08X..0x%08X" % ex.text_range())
lines.append("getter VA 0x%08X -> file offset 0x%X" % (GETTER_VA, off))
lines.append("bytes @0x00414130: %s" % hexs(gb))
lines.append("decode: %s" % dec["text"])
lines.append("bytes @0x00414120 (before): %s" % hexs(window_before))
with open(os.path.join(OUT, "GETTER_PIN.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")

print("\n".join(lines))
