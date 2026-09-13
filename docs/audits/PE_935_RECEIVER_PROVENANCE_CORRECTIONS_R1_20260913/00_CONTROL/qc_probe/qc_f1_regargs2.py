# -*- coding: utf-8 -*-
# QC F1-KEY part 2: per-registration arg decode. For each of the 55 ctor-class call
# sites: identify the LAST push before the CALL (= arg1) and the push before it
# (= arg2 candidate: 68 7B 95 A7 00 empty-string / 50 PUSH EAX after LEA = &local /
# other). Pins exact VAs. pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}
CT_CLASS = 0x0070CF80
calls = b.calls(CT_CLASS, 0xE8)

# Minimal backward instruction walker for the push-run directly preceding the call:
# decode pushes (68 imm32 / 6A imm8 / 50-57 reg) walking BACK from the call site.
def back_pushes(site_va, maxback=24):
    """Walk bytes immediately before call; collect pushes until a non-push byte.
    Returns list of (at_va, kind, value) in REVERSE order (nearest first)."""
    out = []
    va = site_va
    steps = 0
    while steps < maxback:
        steps += 1
        # opcode candidates ending at va
        found = False
        for plen, kind in ((5, "imm32"), (2, "imm8"), (1, "reg")):
            start = va - plen
            byte = b.rd(start, 1)
            if byte is None:
                continue
            op = byte[0]
            ok = (kind == "imm32" and op == 0x68) or \
                 (kind == "imm8" and op == 0x6A) or \
                 (kind == "reg" and 0x50 <= op <= 0x57)
            if not ok:
                continue
            if kind == "imm32":
                val = struct.unpack("<I", b.rd(start + 1, 4))[0]
            elif kind == "imm8":
                val = struct.unpack("<b", b.rd(start + 1, 1))[0]
            else:
                val = op - 0x50  # EAX=0..EDI=7
            out.append(dict(at=hex(start), kind=kind, value=val,
                            value_hex=hex(val) if isinstance(val, int) else val))
            va = start
            found = True
            break
        if not found:
            break
    return out  # nearest-to-call first

sites = []
for c in calls:
    site = c["site_va"]
    pushes = back_pushes(site)
    arg1 = pushes[0] if pushes else None
    arg2 = pushes[1] if len(pushes) > 1 else None
    # arg1 classification
    a1_kind = arg1["kind"] if arg1 else None
    a1_val = arg1["value"] if arg1 else None
    a2_kind = arg2["kind"] if arg2 else None
    a2_val = arg2["value_hex"] if arg2 else None
    sites.append(dict(call_site=hex(site), arg1_kind=a1_kind, arg1=a1_val,
                      arg1_hex=hex(a1_val) if isinstance(a1_val, int) else None,
                      arg1_push_at=arg1["at"] if arg1 else None,
                      arg2_kind=a2_kind, arg2=a2_val,
                      arg2_push_at=arg2["at"] if arg2 else None,
                      n_pushes=len(pushes)))

imm_sites = [s for s in sites if s["arg1_kind"] == "imm32"]
zero_sites = [s for s in sites if s["arg1_kind"] == "imm8" and s["arg1"] == 0]
other_sites = [s for s in sites if s not in imm_sites and s not in zero_sites]
R["sites"] = sites
R["summary"] = dict(total_calls=len(calls),
                    arg1_imm32=len(imm_sites),
                    arg1_push0=len(zero_sites),
                    arg1_other=len(other_sites),
                    arg2_emptystring=len([s for s in imm_sites if s["arg2"] == "0xa7957b"]),
                    arg2_other=len([s for s in imm_sites if s["arg2"] != "0xa7957b"]))
R["zero_arg1_sites"] = zero_sites
R["other_arg1_sites"] = other_sites

# the 4 required pairs with exact pins
pairs = {}
for s in sites:
    if s["arg1"] == 0x4E43:
        pairs["surgeon_20035"] = s
    if s["arg1"] == 0x4E3E:
        pairs["container_20030"] = s
    if s["arg1"] == 0x4E42:
        pairs["realworlditem_20034"] = s
    if s["arg1"] == 0x4E26:
        pairs["unknown_20006"] = s
R["required_pairs_pins"] = pairs

p = save_json("QC_F1_REGARGS2.json", R)
print("saved", p)
print(json.dumps(R["summary"], indent=1) if False else R["summary"])
import json
print(json.dumps(pairs, indent=1))
print("zero sites:", json.dumps(zero_sites, indent=1))
print("other:", json.dumps(other_sites, indent=1))
a2o = [s for s in imm_sites if s["arg2"] != "0xa7957b"]
print("arg2 != empty-string count:", len(a2o))
for s in a2o[:8]:
    print("  ", s["call_site"], "arg1", s["arg1_hex"], "arg2", s["arg2"], s["arg2_kind"], "push_at", s["arg2_push_at"])
