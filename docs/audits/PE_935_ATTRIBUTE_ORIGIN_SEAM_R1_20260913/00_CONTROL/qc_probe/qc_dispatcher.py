"""qc_dispatcher.py — own decode of FUN_004B18D0 dispatcher switch (byte-table + jump-table),
plus dumps of handler regions. Settles: which message types reach the placement processor
FUN_004C47F0 / FUN_007453D0, and the exact case blocks for 0xB0/0xB9/0xC6/0xC7.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qc_pe import PE

PKG = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(PKG, "00_CONTROL", "qc_probe", "QC_DISPATCHER.json")
pe = PE(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")

res = {"exe_sha256": pe.sha256()}

# 1) dispatcher prologue bytes
res["dispatcher_head_0x004B18D0"] = pe.hexdump(0x004B18D0, 0x80)
res["dispatcher_region_0x004B1900_0x004B1C70"] = pe.hexdump(0x004B1900, 0x370)

# 2) byte table at 0x004B1B3C (assume 0x25 entries = types 0xA2..0xC6) - read wide window
bt_va = 0x004B1B3C
bt = pe.read(bt_va, 0x30)
res["byte_table_va"] = "0x%08X" % bt_va
res["byte_table_bytes"] = " ".join("%02X" % b for b in bt)
res["byte_table"] = {("0x%02X" % (0xA2 + i)): bt[i] for i in range(len(bt))}

# 3) jump table at 0x004B1AE4: entries until they leave plausible .text range
jt_va = 0x004B1AE4
entries = []
for i in range(64):
    v = pe.u32(jt_va + 4 * i)
    if v is None or not (0x004B0000 <= v < 0x004B3000):
        break
    entries.append(v)
res["jump_table_va"] = "0x%08X" % jt_va
res["jump_table_entries"] = ["0x%08X" % v for v in entries]

# 4) handler regions
res["handler_B0_FUN_004574F0"] = pe.hexdump(0x004574F0, 0xC0)
res["handler_C6_FUN_004B0AB0"] = pe.hexdump(0x004B0AB0, 0xA0)
res["handler_C7_FUN_004B1670"] = pe.hexdump(0x004B1670, 0xB0)
res["handler_B9_FUN_005B72C0_head"] = pe.hexdump(0x005B72C0, 0x80)
res["case_call_FUN_004C47F0_region_0x004B1D90"] = pe.hexdump(0x004B1D90, 0x60)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print("byte_table:", res["byte_table"])
print("jump_table:", res["jump_table_entries"])
print("->", OUT)
