# -*- coding: utf-8 -*-
# Ghidra postScript: authoritative isCall() reference counts for key functions.
# rc1_refcounts.py

import json

OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\01_RAW\GHIDRA_REFCOUNTS.json"

prog = currentProgram
af = prog.getAddressFactory()
space = af.getDefaultAddressSpace()
fm = prog.getFunctionManager()

def addr(va):
    return space.getAddress(va)

res = {"stage": "ghidra_refcounts", "measured": {}, "errors": []}

for label, va in (("ctor_ArkObject_00726E70", 0x00726E70),
                  ("ctor_ArkObjectClass_0070CF80", 0x0070CF80),
                  ("factory_0070BF50", 0x0070BF50),
                  ("ctor_ArkSurgeonObject_007351E0", 0x007351E0),
                  ("getterA_007CE1E0", 0x007CE1E0),
                  ("getterD_0048ADA0", 0x0048ADA0),
                  ("getterDf32_00861240", 0x00861240),
                  ("ctor_record_00730700", 0x00730700)):
    refs = getReferencesTo(addr(va))
    call_sites = []
    for r in refs:
        if r.getReferenceType().isCall():
            call_sites.append("0x%08X" % r.getFromAddress().getOffset())
    res["measured"][label] = {"isCall_count": len(call_sites), "sites": call_sites}

with open(OUT, "w") as f:
    json.dump(res, f, indent=2)

print("REFCOUNTS done")
for k, v in res["measured"].items():
    print("%s = %d" % (k, v["isCall_count"]))
