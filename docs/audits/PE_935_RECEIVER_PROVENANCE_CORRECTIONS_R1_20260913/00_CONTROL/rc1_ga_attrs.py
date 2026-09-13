# -*- coding: utf-8 -*-
# Ghidra postScript (Jython): function attribution for F5 lists + program identity.
# rc1_ga_attrs.py - run via analyzeHeadless on the copied PE935_DISPLAY_ENUM_R1 project.

import json
from ghidra.program.model.address import AddressFactory

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\01_RAW\GHIDRA_FUNC_ATTR.json"

CTOR_SITES = [0x00456770, 0x00457C00, 0x00457E30, 0x0046AA90, 0x004B9960, 0x004C5AE0,
              0x004E3B70, 0x004FF620, 0x0050BAF0, 0x0050C0C0, 0x0050CC70, 0x0050D480,
              0x0050E490, 0x0050FCF0, 0x005106A0, 0x00511070, 0x006C8000, 0x006C80C0,
              0x0072FA30]
# note: ctor sites census (26) - heuristic func starts listed; we also anchor the raw sites:
CTOR_RAW = [0x0043E5B0, 0x00447630, 0x004C5580, 0x0048ADA0]
F90_SITES = [0x0043A253, 0x00442298, 0x0044AAFD, 0x00457D67, 0x004592EC, 0x0046E7E1,
             0x00488958, 0x004B3B26, 0x004C48F4, 0x0050BFEF, 0x0056739B, 0x00567906,
             0x005B601A, 0x0067BD0E, 0x0067CD4E]

res = {"stage": "ghidra_func_attr", "measured": {}, "errors": []}

prog = currentProgram
af = prog.getAddressFactory()
space = af.getDefaultAddressSpace()
fm = prog.getFunctionManager()

def addr(va):
    return space.getAddress(va)

def get_func(va):
    f = fm.getFunctionContaining(addr(va))
    if f is None:
        return None
    return {"entry": "0x%08X" % f.getEntryPoint().getOffset(),
            "name": f.getName(),
            "body_size": f.getBody().getNumAddresses()}

res["measured"]["program"] = {
    "name": prog.getName(),
    "executable_path": None,
    "md5_of_binary": None,
}
try:
    import hashlib
    exe_path = None
    try:
        # Ghidra 11: executable info via program options
        opts = prog.getOptions(Program._PROGRAM_INFO)
        if opts is not None:
            exe_path = opts.getString("Executable Location", None)
    except:
        pass
    if exe_path is not None:
        res["measured"]["program"]["executable_path"] = exe_path
        h = hashlib.md5()
        h2 = hashlib.sha256()
        with open(exe_path, "rb") as fh:
            for blk in iter(lambda: fh.read(1 << 20), b""):
                h.update(blk)
                h2.update(blk)
        res["measured"]["program"]["md5_of_binary"] = h.hexdigest().upper()
        res["measured"]["program"]["sha256_of_binary"] = h2.hexdigest().upper()
except Exception as e:
    res["errors"].append("hash error: %s" % e)

attr = {}
for va in F90_SITES:
    attr["f90_site_0x%08X" % va] = get_func(va)
for i, va in enumerate(CTOR_SITES):
    attr["ctor_heur_start_0x%08X" % va] = get_func(va)
res["measured"]["function_attribution"] = attr

# full list of ctor caller sites: recompute inside Ghidra via reference scan
target = addr(0x00730700)
refs = getReferencesTo(target)
sites = []
for r in refs:
    if r.getReferenceType().isCall():
        f = fm.getFunctionContaining(r.getFromAddress())
        sites.append({
            "call_site": "0x%08X" % r.getFromAddress().getOffset(),
            "func": (f.getName() if f is not None else None),
            "entry": ("0x%08X" % f.getEntryPoint().getOffset()) if f is not None else None})
res["measured"]["ctor_FUN_00730700_call_sites"] = sites

f90refs = getReferencesTo(addr(0x00730F90))
f90sites = []
for r in f90refs:
    if r.getReferenceType().isCall():
        f = fm.getFunctionContaining(r.getFromAddress())
        f90sites.append({
            "call_site": "0x%08X" % r.getFromAddress().getOffset(),
            "func": (f.getName() if f is not None else None),
            "entry": ("0x%08X" % f.getEntryPoint().getOffset()) if f is not None else None})
res["measured"]["f90_FUN_00730F90_call_sites"] = f90sites

with open(OUT, "w") as f:
    json.dump(res, f, indent=2)

print("GHIDRA_FUNC_ATTR done; ctor sites=%d f90 sites=%d" % (len(sites), len(f90sites)))
