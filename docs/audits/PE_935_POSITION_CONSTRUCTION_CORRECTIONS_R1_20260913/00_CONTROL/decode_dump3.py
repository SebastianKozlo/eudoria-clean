# -*- coding: utf-8 -*-
# decode_dump3.py - third wave: extended manager ctor, lock family, imports,
# short-function raw bytes, Phase-3 ctor chain.
# STATIC-ONLY. Own capstone decode from the physical EXE.

import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe935_core as core

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")
pe = core.PE(core.EXE_PATH)

FUNCTIONS = [
    ("F008550C0_MANAGER_CTOR_FULL", 0x008550C0, 0x500),
    ("F00413590_LOCK_INIT", 0x00413590, 0x100),
    ("F00413560_LOCK_FAMILY2", 0x00413560, 0x60),
    ("F004134F0_LOCK_FAMILY1", 0x004134F0, 0x100),
    ("F00413360_REALFN", 0x00413360, 0x100),
    ("F008552C0_REGION_AFTER", 0x008552C0, 0x300),
]

for label, va, mx in FUNCTIONS:
    end_va, body = pe.func_body(va, maxb=mx)
    txt = pe.disasm_lines(va, len(body)) if body else "NO BYTES"
    out_path = os.path.join(RAW, label + ".txt")
    with open(out_path, "w") as f:
        f.write("# OWN DECODE (capstone x86-32) from physical EXE\n")
        f.write("# entry=%08X end_detected=%s size=%d\n" %
                (va, hex(end_va) if end_va else "None", len(body)))
        f.write("# file=%s\n" % core.EXE_PATH)
        f.write(txt + "\n")
    print("%-28s entry=%08X end=%s size=%d" %
          (label, va, hex(end_va) if end_va else "-", len(body)))

# --- import table parse -------------------------------------------------
print("\n--- IMPORT TABLE ---")
d = pe.data
imp_rva = struct.unpack_from("<I", d, pe.e_lfanew + 4 + 20 + 96 + 8)[0]  # opt+96 data dir[1]
sec = None
for s in pe.sections:
    if s["vaddr"] <= imp_rva < s["vaddr"] + s["rsize"]:
        sec = s
        break
imp_off = sec["rptr"] + (imp_rva - sec["vaddr"])
imports = {}
i = 0
while True:
    ilt, ts, fc, name_rva, iat_rva = struct.unpack_from("<IIIII", d, imp_off + i * 20)
    if ilt == 0 and name_rva == 0 and iat_rva == 0:
        break
    name_off = sec["rptr"] + (name_rva - sec["vaddr"])
    dll_name = d[name_off:d.index(b"\x00", name_off)].decode("ascii", "replace")
    # walk IAT entries (via the FirstThunk address)
    iat_sec = None
    for s in pe.sections:
        if s["vaddr"] <= iat_rva < s["vaddr"] + s["rsize"]:
            iat_sec = s
            break
    iat_off = iat_sec["rptr"] + (iat_rva - iat_sec["vaddr"])
    ilt_off = None
    if ilt:
        for s in pe.sections:
            if s["vaddr"] <= ilt < s["vaddr"] + s["rsize"]:
                ilt_off = s["rptr"] + (ilt - s["vaddr"])
                break
    j = 0
    funcs = []
    while True:
        entry_rva = iat_rva + j * 4
        if ilt_off is not None:
            v = struct.unpack_from("<I", d, ilt_off + j * 4)[0]
        else:
            v = struct.unpack_from("<I", d, iat_off + j * 4)[0]
        if v == 0:
            break
        if v & 0x80000000:
            fname = "ordinal_%d" % (v & 0xFFFF)
        else:
            hn_off = None
            for s in pe.sections:
                if s["vaddr"] <= v < s["vaddr"] + s["rsize"]:
                    hn_off = s["rptr"] + (v - s["vaddr"])
                    break
            if hn_off is None:
                fname = "?"
            else:
                fname = d[hn_off + 2:d.index(b"\x00", hn_off + 2)].decode("ascii", "replace")
        funcs.append((pe.image_base + entry_rva, fname))
        j += 1
    imports[dll_name] = funcs
    print("DLL %s: %d imports" % (dll_name, len(funcs)))
    i += 1

# resolve the IAT slots of interest
SLOTS = [0x00A75064, 0x00A7506C, 0x00A75A38, 0x00A75A40, 0x00A75A44,
         0x00A75A5C, 0x00A759E4, 0x00A759AC, 0x00A759B4, 0x00A759B8]
with open(os.path.join(RAW, "IMPORT_RESOLUTION.json"), "w") as f:
    out = {}
    for slot in SLOTS:
        found = None
        for dll, funcs in imports.items():
            for va, fname in funcs:
                if va == slot:
                    found = (dll, fname)
                    break
            if found:
                break
        print("IAT %08X = %s" % (slot, "%s!%s" % found if found else "UNRESOLVED"))
        out[hex(slot)] = found
    struct_out = {k: v for k, v in out.items()}
    import json
    json.dump(struct_out, f, indent=1)
print("DONE")
