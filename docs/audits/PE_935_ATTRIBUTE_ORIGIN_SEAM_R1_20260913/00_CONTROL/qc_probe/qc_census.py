"""qc_census.py — own caller/edge censuses (E8 direct calls + E9 tail jumps) for the seam chain.
Independent of executor censuses (own scan loop over .text raw bytes).
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import PE

PKG = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(PKG, "00_CONTROL", "qc_probe", "QC_CENSUS.json")

TARGETS = {
    # --- chain: message -> insert ---
    "FUN_004B18D0_dispatcher": 0x004B18D0,
    "FUN_005B72C0_handler_B9": 0x005B72C0,
    "FUN_004574F0_handler_B0": 0x004574F0,
    "FUN_004B0AB0_handler_C6": 0x004B0AB0,
    "FUN_004B1670_handler_C7": 0x004B1670,
    "FUN_004C47F0_processor": 0x004C47F0,
    "FUN_007453D0_deserializer": 0x007453D0,
    "FUN_00745360_init": 0x00745360,
    "FUN_00752700_readcursor": 0x00752700,
    "FUN_00752640_readcursor": 0x00752640,
    "FUN_007527F0_readsubtype": 0x007527F0,
    "FUN_0040DE60_advance": 0x0040DE60,
    "FUN_004C46C0_creator": 0x004C46C0,
    "FUN_00856190_insert": 0x00856190,
    "FUN_00414130_getkey": 0x00414130,
    "FUN_004123D0_deref": 0x004123D0,
    "FUN_00730F60_setf60": 0x00730F60,
    "FUN_00730F90_setf90": 0x00730F90,
    "FUN_00730FB0_setfb0": 0x00730FB0,
    "FUN_00730FD0_setfd0": 0x00730FD0,
    "FUN_0085B1B0_ctor_MovableObject": 0x0085B1B0,
    "FUN_00528E50_ctor_ClientMovableObject": 0x00528E50,
    "FUN_008544D0_resolver": 0x008544D0,
    "FUN_004154F0_mgr_getter": 0x004154F0,
    "FUN_00854D90_findorcreate": 0x00854D90,
    "FUN_00567770_builder": 0x00567770,
    "FUN_00567C50_driver": 0x00567C50,
    "FUN_00457930_keyproducer": 0x00457930,
    "FUN_00845F70_attr_writer": 0x00845F70,
    "FUN_0094BD30_vfs_parser": 0x0094BD30,
    "FUN_0094F350_vfs_parser": 0x0094F350,
    "FUN_0072FA30_registry_builder": 0x0072FA30,
    "FUN_00730C90_def_parser": 0x00730C90,
    "FUN_006CB6F0_candidate": 0x006CB6F0,
    "FUN_00567170_candidate": 0x00567170,
    "FUN_005B5F90_candidate": 0x005B5F90,
    "FUN_005B6890": 0x005B6890,
    "FUN_005B6370": 0x005B6370,
    "FUN_004641F0": 0x004641F0,
    "FUN_004C4A10": 0x004C4A10,
    "FUN_008553D0_composer": 0x008553D0,
    "FUN_0085B840_walker": 0x0085B840,
    "FUN_00856090_rehash": 0x00856090,
    "FUN_00854260_nodeinit": 0x00854260,
    "FUN_00971780_hashfind": 0x00971780,
    "FUN_007CE1E0_getterA": 0x007CE1E0,
    "FUN_0048ADA0_getterD": 0x0048ADA0,
    "FUN_00752640b": None,
}


def main():
    pe = PE(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
    res = {"exe_sha256": pe.sha256(), "note": "own E8/E9 census over .text raw bytes; each site = instruction VA"}
    for name, va in sorted(TARGETS.items()):
        if va is None:
            continue
        e8 = pe.scan_call_e8(va)
        e9 = pe.scan_jmp_e9(va)
        res[name] = {
            "target_va": "0x%08X" % va,
            "e8_direct_callsites": ["0x%08X" % x for x in e8],
            "e8_count": len(e8),
            "e9_tailjumps": ["0x%08X" % x for x in e9],
            "e9_count": len(e9),
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    # compact stdout
    for name in sorted(TARGETS):
        if TARGETS[name] is None:
            continue
        r = res[name]
        print("%-38s E8=%d %s  E9=%d" % (name, r["e8_count"], " ".join(r["e8_direct_callsites"]), r["e9_count"]))
    print("->", OUT)


if __name__ == "__main__":
    main()
