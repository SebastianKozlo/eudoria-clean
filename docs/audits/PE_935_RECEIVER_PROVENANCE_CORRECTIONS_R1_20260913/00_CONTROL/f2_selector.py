# -*- coding: utf-8 -*-
# F2 — selector 0x4E38 reconstruction from raw bytes.
# (1) branch region dump 0x008557C0-0x00855830 (CMP EAX,0x4E38, walker, getter, selector);
# (2) jump table @0x00855BB4 (4 entries) dump + targets decode;
# (3) walker family bodies: FUN_0085B840, FUN_0085B860;
# (4) FUN_008553D0 full body hexdump for Ghidra cross-check;
# (5) getter D FUN_0048ADA0 + call site @0x008556DF context (QC B10 claim);
# (6) templates.vfs record 4508: D field read (file offset 96528, payload +0x10).
# Output: 01_RAW/F2_SELECTOR.json + F2_CTX_*.txt

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump, f32bits

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"

pe = PE(EXE)
res = {"stage": "F2_selector", "measured": {}, "errors": []}


def dump(name, va, n):
    b = pe.read_va(va, n)
    with open(os.path.join(OUT, "F2_CTX_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")
    return b


# 1. branch region
dump("BRANCH_008557C0", 0x008557C0, 0xC0)

# 2. jump table @0x00855BB4
jt = []
for i in range(4):
    v = pe.read_va32(0x00855BB4 + i * 4)
    jt.append({"index": i, "va": "0x%08X" % (0x00855BB4 + i * 4), "target": ("0x%08X" % v) if v else None})
res["measured"]["jump_table_00855BB4"] = jt
dump("JUMPTABLE_00855BB4", 0x00855BB4, 0x20)

# 3. walkers
for va in (0x0085B840, 0x0085B860):
    fend, fbody = pe.func_body(va, 0x200)
    res["measured"]["walker_%08X" % va] = {"entry": "0x%08X" % va, "size": len(fbody)}
    dump("WALKER_%08X" % va, va, min(len(fbody), 0x200))

# 4. FUN_008553D0 body (large; dump first 0x800 + locate branch)
fend, fbody = pe.func_body(0x008553D0, 0x2000)
res["measured"]["FUN_008553D0"] = {"entry": "0x008553D0", "size": len(fbody),
                                    "end": ("0x%08X" % fend) if fend else None}
dump("FUN_008553D0", 0x008553D0, min(len(fbody), 0xA00))

# 5. getter D call site @0x008556DF context
dump("GETTERD_SITE_008556C0", 0x008556C0, 0x60)

# 6. templates.vfs record 4508 D field
vfs = open(VFS, "rb").read()
rec_off = 96528
payload = vfs[rec_off:rec_off + 64]
res["measured"]["template_4508"] = {
    "record_file_offset": rec_off,
    "raw_hex_first_64": payload.hex(),
    "id_u32_at_0": struct.unpack_from("<I", vfs, rec_off)[0],
    "B_u32_at_4": struct.unpack_from("<I", vfs, rec_off + 4)[0],
    "A_u32_at_8": struct.unpack_from("<I", vfs, rec_off + 8)[0],
    "C_u32_at_C": struct.unpack_from("<I", vfs, rec_off + 0xC)[0],
    "D_bits_u32_at_10": struct.unpack_from("<I", vfs, rec_off + 0x10)[0],
    "D_bits_hex": "0x%08X" % struct.unpack_from("<I", vfs, rec_off + 0x10)[0],
    "D_f32": f32bits(struct.unpack_from("<I", vfs, rec_off + 0x10)[0]),
    "expected_D_bits": 0x42F9E1CB,
    "expected_D_f32": 124.94100189208984,
}

with open(os.path.join(OUT, "F2_SELECTOR.json"), "w") as f:
    json.dump(res, f, indent=2)

print("done")
print("jump table:", json.dumps(jt))
print("FUN_008553D0 size:", len(fbody), "end:", res["measured"]["FUN_008553D0"]["end"])
t = res["measured"]["template_4508"]
print("4508: id=%d B=%d A=%d C=%s D_bits=0x%08X D_f32=%r" % (
    t["id_u32_at_0"], t["B_u32_at_4"], t["A_u32_at_8"], t["C_u32_at_C"],
    t["D_bits_u32_at_10"], t["D_f32"]))
