# -*- coding: utf-8 -*-
# F1 follow-up: decode registration functions' ctor args (EBP -> [class+8]) and
# class-name strings; dump strings referenced; decode REG dispatcher; check
# FUN_0070E2F1 (registrar), FUN_0073AB61 (derived ctor called by writer).
# Output: 01_RAW/F1_REG_ARGS.json + F1_CTX2_*.txt

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

pe = PE(EXE)
res = {"stage": "F1_reg_args", "measured": {}, "errors": []}


def func_start(va):
    off = pe.va_to_off(va)
    d = pe.data
    i = off
    while i > 0x1000:
        if d[i - 1] == 0xCC and d[i - 2] == 0xCC and d[i - 3] == 0xCC:
            return pe.off_to_va(i)
        i -= 1
    return None


def read_cstr(va, maxlen=96):
    b = pe.read_va(va, maxlen)
    if b is None:
        return None
    z = b.find(b"\x00")
    return b[:z if z >= 0 else maxlen].decode("ascii", "replace")


def decode_push_imm_before_call(call_va, back=0x40):
    """Scan back from CALL site for PUSH imm32 (68 xx xx xx xx) nearest preceding."""
    off = pe.va_to_off(call_va)
    d = pe.data
    imms = []
    i = off - 1
    lo = max(0, off - back)
    while i >= lo:
        if d[i] == 0x68:
            imm = struct.unpack_from("<I", d, i + 1)[0]
            imms.append(("0x%08X" % (pe.off_to_va(i)), "0x%08X" % imm, imm))
            if len(imms) >= 2:
                break
        i -= 1
    return imms


sites = json.load(open(os.path.join(OUT, "F1_CENSUS.json")))["measured"]["callers_ctor_ArkObjectClass_0070CF80"]["call_sites"]
reg = []
for site_hex in sites:
    site = int(site_hex, 16)
    st = func_start(site)
    imms = decode_push_imm_before_call(site)
    reg.append({"call_site": site_hex, "func_start": ("0x%08X" % st) if st else None,
                "push_imm32_before_call": imms})
res["measured"]["ctor_callers_with_push_imm"] = reg

# For each caller, also grab the PUSH 0x00xxxxxx string-ref (class name candidate):
# find PUSH imm32 whose value is in .rdata and looks like a string pointer
def string_pushes_before_call(call_va, back=0x60):
    off = pe.va_to_off(call_va)
    d = pe.data
    out = []
    i = off - 1
    lo = max(0, off - back)
    while i >= lo:
        if d[i] == 0x68:
            imm = struct.unpack_from("<I", d, i + 1)[0]
            if 0x00A75000 <= imm < 0x00B6C000:  # .rdata range
                s = read_cstr(imm)
                out.append({"push_at": "0x%08X" % pe.off_to_va(i), "ptr": "0x%08X" % imm,
                            "string": s})
        i -= 1
    return out

regs2 = []
for site_hex in sites:
    site = int(site_hex, 16)
    sp = string_pushes_before_call(site)
    if sp:
        regs2.append({"call_site": site_hex, "string_pushes": sp})
res["measured"]["string_refs_before_ctor_calls"] = regs2

# decode: what are the imm args at each ctor call site? classify arg1 pattern:
# PUSH imm32 (68) directly before PUSH <local> + CALL — take the two nearest pushes
summary = []
for r in reg:
    site = r["call_site"]
    immvals = [x[2] for x in r["push_imm32_before_call"]]
    summary.append({"call_site": site, "func_start": r["func_start"],
                    "imm_values": ["0x%08X" % v for v in immvals]})
res["measured"]["summary_imm_per_caller"] = summary

# region dumps
def dump(name, va, n):
    with open(os.path.join(OUT, "F1_CTX2_%s.txt" % name), "w") as f:
        f.write("region %s VA=0x%08X len=%d\n" % (name, va, n))
        f.write(hexdump(pe, va, n) + "\n")

dump("REG_00739BCD_WIDE", 0x00739B70, 0xA0)
dump("FUN_0070E2F1", 0x0070E2F1, 0x80)
dump("FUN_0073AB61", 0x0073AB61, 0xA0)
dump("VTSTORE2_0070D19A_WIDE", 0x0070D160, 0xC0)
dump("HIT_00516F0E_WIDE", 0x00516EA0, 0x100)

with open(os.path.join(OUT, "F1_REG_ARGS.json"), "w") as f:
    json.dump(res, f, indent=2)

print("done")
print("callers with string pushes:", len(regs2))
for r in regs2[:8]:
    print(r["call_site"], [s["string"] for s in r["string_pushes"]])
print("--- imm summary (first 20):")
for s in summary[:20]:
    print(s["call_site"], s["func_start"], s["imm_values"])
