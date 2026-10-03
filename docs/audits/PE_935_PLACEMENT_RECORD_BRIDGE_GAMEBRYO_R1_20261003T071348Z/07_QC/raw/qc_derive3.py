#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC_DERIVE3 — oracle identity checks + emitter id2 arrays + misc probes.

P8  NiMain.lib (Gb 1.1.2 Eval) SHA256 + size vs contract/preflight pins.
P9  Gb12 source locators: NiNode.cpp line 34 (ctor) / line 52 (AttachChild),
    NiObjectNET.cpp line 112 (SetName) — read the exact lines (short derived
    quotes only; no source dumps into the repo).
P10 Emitter hardcoded id2 arrays in .rdata: DAT_00A855F0 (Z08 2x4), DAT_00A858B8,
    DAT_00A858C0 (Z09 2x1) — dump + templates id2-set membership.
P11 FUN_005B5F90 (construction driver B) callers: PUSH 0x3ED3 site check.
P12 C11 remaining keys: vtable_discovery / rtti_refs / update_world_data_window.
"""
import hashlib
import json
import os
import struct

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
NIMAIN = r"D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib"
GB12 = r"D:\gamebyroengine\extracted\Gb12_Source"
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
TEMPLATES = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
OUT = os.path.join(PKG, "07_QC", "raw", "QC_DERIVATIONS3.json")

R = {"p8_nimain": {}, "p9_gb12_locators": {}, "p10_id2_arrays": {},
     "p11_driverB": {}, "p12_c11_keys": {}, "errors": []}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()


# P8
if os.path.exists(NIMAIN):
    R["p8_nimain"] = {"path": NIMAIN, "size": os.path.getsize(NIMAIN),
                      "sha256": sha256_file(NIMAIN)}
else:
    R["errors"].append("NiMain.lib not found at pinned path")

# P9: Gb12 locator lines
def read_line(path, lineno):
    with open(path, "r", encoding="latin-1", errors="replace") as f:
        for i, line in enumerate(f, 1):
            if i == lineno:
                return line.rstrip("\r\n")
    return None

locs = {
    "NiNode_ctor_line34": os.path.join(GB12, r"CoreLibs\NiMain\NiNode.cpp"),
    "NiNode_attachchild_line52": os.path.join(GB12, r"CoreLibs\NiMain\NiNode.cpp"),
    "NiObjectNET_setname_line112": os.path.join(GB12, r"CoreLibs\NiMain\NiObjectNET.cpp"),
}
for k, p in locs.items():
    if os.path.exists(p):
        n = 34 if "ctor" in k else (52 if "attachchild" in k else 112)
        ln = read_line(p, n)
        R["p9_gb12_locators"][k] = {"path": p, "line": n, "content": ln,
                                    "sha256_file": sha256_file(p)}
    else:
        R["errors"].append("missing Gb12 source file: %s" % p)

# P10: id2 arrays from .rdata
data = open(EXE, "rb").read()
e_lfanew, = struct.unpack_from("<I", data, 0x3C)
opt_size, = struct.unpack_from("<H", data, e_lfanew + 20)
image_base, = struct.unpack_from("<I", data, e_lfanew + 24 + 28)
nsec, = struct.unpack_from("<H", data, e_lfanew + 6)
secs = []
so = e_lfanew + 24 + opt_size
for i in range(nsec):
    o = so + i * 40
    vsz, vaddr, rsz, rptr = struct.unpack_from("<4I", data, o + 8)
    secs.append((data[o:o + 8].rstrip(b"\0").decode("latin-1"), vaddr, rsz, rptr))


def va2fo(va):
    rva = va - image_base
    for (nm, vaddr, rsz, rptr) in secs:
        if vaddr <= rva < vaddr + rsz:
            return rptr + (rva - vaddr)
    return None


# id2 set from templates (independent re-walk, minimal)
tv = open(TEMPLATES, "rb").read()
id2set = set()
pos = 16
while pos + 16 <= len(tv):
    bid, = struct.unpack_from("<I", tv, pos)
    bsz, = struct.unpack_from("<I", tv, pos + 4)
    id2set.add(bid)
    pos += ((16 + bsz + 36 - 1) // 36) * 36

for arr_va, cnt in ((0x00A855F0, 8), (0x00A858B8, 2), (0x00A858C0, 2)):
    fo = va2fo(arr_va)
    vals = struct.unpack_from("<%dI" % cnt, data, fo)
    R["p10_id2_arrays"]["0x%08X" % arr_va] = {
        "values": list(vals),
        "in_templates_id2": [v in id2set for v in vals],
        "hex": data[fo:fo + 4 * cnt].hex(" "),
    }

# P11: FUN_005B5F90 callers scan (E8 to 0x005B5F90 in .text)
text = None
for s in secs:
    if s[0] == ".text":
        text = s
nm, vaddr, rsz, rptr = text
seg = data[rptr:rptr + rsz]
base_va = image_base + vaddr
sites = []
for i in range(len(seg) - 5):
    if seg[i] == 0xE8:
        rel, = struct.unpack_from("<i", seg, i + 1)
        if base_va + i + 5 + rel == 0x005B5F90:
            sites.append("0x%08X" % (base_va + i))
R["p11_driverB"]["callsites_to_FUN_005B5F90"] = sites
# PUSH 0x3ED3 anywhere (68 D3 3E 00 00)
n5 = struct.pack("<B I", 0x68, 0x3ED3)
i = seg.find(n5)
push3ed3 = []
while i >= 0 and len(push3ed3) < 20:
    push3ed3.append("0x%08X" % (base_va + i))
    i = seg.find(n5, i + 1)
R["p11_driverB"]["push_0x3ED3_sites"] = push3ed3
# also 0x3ED2 variant
n6 = struct.pack("<B I", 0x68, 0x3ED2)
i = seg.find(n6)
push3ed2 = []
while i >= 0 and len(push3ed2) < 20:
    push3ed2.append("0x%08X" % (base_va + i))
    i = seg.find(n6, i + 1)
R["p11_driverB"]["push_0x3ED2_sites"] = push3ed2

# P12: C11 remaining keys
c11 = json.load(open(os.path.join(PKG, "01_RAW", "C11_ORACLE_COUNTERPARTS.json"),
                     encoding="utf-8"))
for k in ("vtable_discovery", "rtti_refs", "update_world_data_window"):
    v = c11.get("measured", {}).get(k)
    R["p12_c11_keys"][k] = v

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, indent=2)
print("QC_DERIVE3 written:", OUT)
print("NiMain:", R["p8_nimain"].get("sha256"), R["p8_nimain"].get("size"))
for k, v in R["p9_gb12_locators"].items():
    print(k, "->", repr(v.get("content"))[:120])
for k, v in R["p10_id2_arrays"].items():
    print(k, v["values"], v["in_templates_id2"])
print("driverB callsites:", sites)
print("push 3ED3:", push3ed3)
print("push 3ED2:", push3ed2)
