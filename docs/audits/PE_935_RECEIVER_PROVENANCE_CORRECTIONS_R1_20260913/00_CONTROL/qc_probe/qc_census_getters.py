# -*- coding: utf-8 -*-
# QC census: own raw E8+E9 census for getterA FUN_007CE1E0, getterD FUN_0048ADA0,
# getterDf32 FUN_00861240; cross-tab vs Ghidra isCall lists (GHIDRA_REFCOUNTS.json).
# Explains 808 vs 817 and 116 vs 117.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys, json
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
G = json.load(open(r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\01_RAW\GHIDRA_REFCOUNTS.json"))["measured"]
R = {}

def census(target):
    e8 = b.calls(target, 0xE8)
    e9 = b.calls(target, 0xE9)
    return [s["site_va"] for s in e8], [s["site_va"] for s in e9]

def ghidra_sites(label):
    return [int(s, 16) for s in G[label]["sites"]]

for name, target, glabel in (
        ("getterA", 0x007CE1E0, "getterA_007CE1E0"),
        ("getterD", 0x0048ADA0, "getterD_0048ADA0"),
        ("getterDf32", 0x00861240, "getterDf32_00861240"),
        ("ctor_record_00730700", 0x00730700, "ctor_record_00730700"),
        ("ctor_ArkObjectClass", 0x0070CF80, "ctor_ArkObjectClass_0070CF80"),
        ("ctor_ArkObject", 0x00726E70, "ctor_ArkObject_00726E70"),
        ("factory", 0x0070BF50, "factory_0070BF50")):
    e8, e9 = census(target)
    g = ghidra_sites(glabel)
    e8s, e9s, gs = set(e8), set(e9), set(g)
    R[name] = dict(
        raw_e8=len(e8), raw_e9=len(e9),
        ghidra_isCall=G[glabel]["isCall_count"],
        e8_only=sorted(hex(x) for x in (e8s - gs)),
        e9_only=sorted(hex(x) for x in (e9s - gs)),
        ghidra_only_not_raw=sorted(hex(x) for x in (gs - e8s - e9s)),
        in_both=sorted(hex(x) for x in (e8s & gs)),
        e8_not_in_ghidra=sorted(hex(x) for x in (e8s - gs)),
    )
    print(name, "E8:", len(e8), "E9:", len(e9), "Ghidra:", G[glabel]["isCall_count"])
    if e9:
        print("   E9 sites (in Ghidra?):", [hex(x) for x in e9], "in_ghidra:", [x in gs for x in e9])
    if R[name]["ghidra_only_not_raw"]:
        print("   Ghidra-only sites:", R[name]["ghidra_only_not_raw"])
    if R[name]["e8_not_in_ghidra"]:
        print("   raw-E8-not-in-Ghidra sites:", R[name]["e8_not_in_ghidra"])

p = save_json("QC_CENSUS_GETTERS.json", R)
print("saved", p)
