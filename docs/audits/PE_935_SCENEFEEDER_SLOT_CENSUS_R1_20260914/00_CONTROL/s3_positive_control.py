# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 - S3: positive control.
# Re-derive the FUN_005094C0 window from the PHYSICAL EXE: hexdump + own
# capstone decode + byte-exact comparison against the contract-expected
# pattern (which itself is re-derived here from the expected semantic copy:
# [arg] -> SF(this)+0x34/0x38/0x3C, flag +0x28 = 1, ret 4).
# STATIC-ONLY. Output: 01_RAW/POSITIVE_CONTROL_005094C0.txt

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_core as core

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")

lines = []
def emit(s=""):
    lines.append(s)
    print(s)

exe_sha = core.sha256_file(core.EXE_PATH)
assert exe_sha.lower() == core.EXPECTED_SHA256.lower(), "sha mismatch"
assert os.path.getsize(core.EXE_PATH) == core.EXPECTED_SIZE, "size mismatch"
pe = core.PE(core.EXE_PATH)
assert pe.machine == core.EXPECTED_MACHINE and pe.opt_magic == core.EXPECTED_OPT_MAGIC
assert pe.image_base == core.EXPECTED_IMAGE_BASE

emit("# OWN DECODE - PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914")
emit("# POSITIVE CONTROL: FUN_005094C0 window (re-derived, not trusted from listing)")
emit("# Source: PHYSICAL EXE %s" % core.EXE_PATH)
emit("# EXE SHA256 (measured): %s" % exe_sha)
emit()
emit("# === HEXDUMP window 0x%08X..0x%08X ===" % (
    core.POSITIVE_CONTROL_VA, core.POSITIVE_CONTROL_VA + core.POSITIVE_CONTROL_WINDOW - 1))
emit(core.hexdump(pe, core.POSITIVE_CONTROL_VA, core.POSITIVE_CONTROL_WINDOW))
emit()

# --- byte-exact comparison with the contract-expected pattern --------------
measured = pe.read_va(core.POSITIVE_CONTROL_VA, len(core.POSITIVE_CONTROL_EXPECTED))
emit("# === BYTE-EXACT COMPARISON vs contract-expected pattern ===")
emit("# expected (%d bytes): %s" % (
    len(core.POSITIVE_CONTROL_EXPECTED), core.POSITIVE_CONTROL_EXPECTED.hex(" ")))
emit("# measured (%d bytes): %s" % (len(measured), measured.hex(" ")))
byte_exact = (measured == core.POSITIVE_CONTROL_EXPECTED)
emit("# BYTE-EXACT MATCH: %s" % ("PASS" if byte_exact else "FAIL"))
emit()

# --- own capstone decode of the window --------------------------------------
emit("# === OWN CAPSTONE DECODE (x86-32) ===")
window = core.POSITIVE_CONTROL_WINDOW
va = core.POSITIVE_CONTROL_VA
end = va + window
sem = []
while va < end:
    ins = pe.disasm_one(va)
    if ins is None:
        emit("# DISASM_FAIL @ %08X" % va)
        break
    emit(core.render_insn(ins))
    sem.append(ins)
    if ins["mnemonic"] == "ret":
        break  # the controlled function ends at its first ret (pattern: ret 4)
    va += ins["size"]

emit()
emit("# === SEMANTIC VERDICT (executor re-derivation from the measured bytes) ===")
# Adjudicate semantics from the measured instructions (not from the contract text).
txt = " ".join("%s %s" % (i["mnemonic"], i["op_str"]) for i in sem)
checks = {
    "loads_arg_ptr_esp4":      ("mov eax, dword ptr [esp + 4]" in txt),
    "reads_src_x_arg0":        ("mov edx, dword ptr [eax]" in txt),
    "writes_dst_this_34":      ("mov dword ptr [ecx + 0x34], edx" in txt),
    "reads_src_y_arg4":        ("mov edx, dword ptr [eax + 4]" in txt),
    "writes_dst_this_38":      ("mov dword ptr [ecx + 0x38], edx" in txt),
    "reads_src_z_arg8":        ("mov eax, dword ptr [eax + 8]" in txt),
    "writes_dst_this_3c":      ("mov dword ptr [ecx + 0x3c], eax" in txt),
    "flag_this_28_set_1":      ("mov byte ptr [ecx + 0x28], 1" in txt),
    "terminal_ret_4":          (sem and sem[-1]["mnemonic"] == "ret" and sem[-1]["op_str"] == "4"),
}
all_ok = all(checks.values())
for k, v in checks.items():
    emit("#   %-26s %s" % (k, "PASS" if v else "FAIL"))
emit("# SEMANTIC COPY [arg+0/4/8] -> [ecx(this)+0x34/0x38/0x3C], flag [this+0x28]=1, ret 4:")
emit("#   -> %s" % ("PASS - the window PROVES: caller-supplied triple pointer (arg) is"
                   " copied into the this-object fields +0x34/+0x38/+0x3C" if all_ok else "FAIL"))
emit("#")
emit("# NOTE (layer honesty): the window proves arg-triple -> this+0x34/38/3C. The")
emit("# identity 'arg == instance+0x44' was established by the accepted prior run")
emit("# (PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913, caller-side); it is NOT")
emit("# re-derived in this run and is NOT needed for the control's validation purpose.")
emit("#")
emit("# POSITIVE_CONTROL VERDICT: %s" % ("PASS" if (byte_exact and all_ok) else "FAIL"))

with open(os.path.join(RAW, "POSITIVE_CONTROL_005094C0.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
print()
print("WROTE 01_RAW/POSITIVE_CONTROL_005094C0.txt")
if not (byte_exact and all_ok):
    sys.exit(5)
