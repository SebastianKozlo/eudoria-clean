#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RE-QC 9 (physical truth revalidation of C9 listing windows + C10V2 pins):
independent of QC round-1 (which verified the PRE-repair data) and of the
executor's instruments. With THIS QC's own PE mapper:
 1. Every instruction of every C9 window: signed-hex normalized 'bytes' string
    must equal the physical EXE bytes at its VA. Expect 962/962.
 2. Every CALL/imm record: re-derive target from raw EXE bytes (rel32 / imm32)
    and compare with the listing 'text' / C10V2 record. Expect 113/113.
 3. C10V2 byte-pin records (windows, call_targets, string_pin) re-checked
    against physical EXE bytes/offsets.
"""
import hashlib
import json
import os
import re
import struct

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
OUT = os.path.join(PKG, "07_QC", "raw", "recheck", "recheck9_physical.json")

data = open(EXE, "rb").read()
assert hashlib.sha256(data).hexdigest().upper() == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
coff = e_lfanew + 4
nsec = struct.unpack_from("<H", data, coff + 2)[0]
opt_size = struct.unpack_from("<H", data, coff + 16)[0]
opt = coff + 20
image_base = struct.unpack_from("<I", data, opt + 28)[0]
sections = []
for i in range(nsec):
    off = opt + opt_size + 40 * i
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", data, off + 8)
    sections.append((vaddr, max(vsize, rsize), raddr))

def va_to_fo(va):
    rva = va - image_base
    for vaddr, size, raddr in sections:
        if vaddr <= rva < vaddr + size:
            return raddr + (rva - vaddr)
    return None

def norm_bytes(s):
    """Ghidra-Jython signed hex ('-7D 44 24 0C') -> physical bytes ('83 EC 24 0C')."""
    out = []
    for tok in s.split():
        v = int(tok, 16)
        if v < 0:
            v += 256
        out.append("%02X" % (v & 0xFF))
    return out

with open(os.path.join(PKG, "01_RAW", "C9_LISTING_WINDOWS.json"), encoding="utf-8-sig") as f:
    c9 = json.load(f)

total = 0
byte_match = 0
byte_mism = []
call_checks = 0
call_match = 0
call_mism = []
for wname, w in c9["measured"]["windows"].items():
    for ins in w["instructions"]:
        va = int(ins["addr"], 16)
        fo = va_to_fo(va)
        got = norm_bytes(ins["bytes"])
        phys = ["%02X" % b for b in data[fo:fo + len(got)]]
        total += 1
        if got == phys:
            byte_match += 1
        else:
            byte_mism.append({"window": wname, "addr": ins["addr"],
                               "listing": " ".join(got), "physical": " ".join(phys)})
        # CALL rel32 / MOV imm32 re-derivation
        txt = ins["text"]
        if phys[0] == "E8" and len(phys) >= 5:
            rel = struct.unpack_from("<i", data, fo + 1)[0]
            tgt = "0x%08X" % (va + 5 + rel)
            m = re.search(r"CALL (0x[0-9A-Fa-f]+)", txt)
            call_checks += 1
            if m and m.group(1).lower() == tgt.lower():
                call_match += 1
            else:
                call_mism.append({"kind": "call", "addr": ins["addr"], "text": txt,
                                  "derived": tgt})
        if (phys[0] == "68" or (phys[0] == "B8" and False)) and len(phys) >= 5:
            imm = struct.unpack_from("<I", data, fo + 1)[0]
            m = re.search(r"0x([0-9A-Fa-f]+)", txt)
            call_checks += 1
            if m and int(m.group(1), 16) == imm:
                call_match += 1
            else:
                call_mism.append({"kind": "imm32", "addr": ins["addr"], "text": txt,
                                  "derived": "0x%08X" % imm})

res = {"c9_instructions": total, "c9_byte_identical": byte_match,
       "c9_byte_mismatches": len(byte_mism),
       "call_imm_checks": call_checks, "call_imm_matches": call_match,
       "call_imm_mismatches": call_mism[:10], "n_call_mism": len(call_mism)}

# --- C10V2 pins re-check ---
with open(os.path.join(PKG, "01_RAW", "C10V2_BYTE_CROSSCHECK.json"), encoding="utf-8-sig") as f:
    v2 = json.load(f)
meas = v2["measured"]
pin_ok = 0
pin_bad = []
n_pin = 0
for kind in ("windows", "call_targets", "string_pin"):
    obj = meas.get(kind)
    if isinstance(obj, dict):
        items = obj.items()
    elif isinstance(obj, list):
        items = [("<%s[%d]>" % (kind, i), o) for i, o in enumerate(obj)]
    else:
        continue
    for key, rec in items:
        if not isinstance(rec, dict):
            continue
        va = rec.get("addr") or rec.get("va")
        if not va:
            continue
        n_pin += 1
        vaint = int(va, 16)
        fo = va_to_fo(vaint)
        raw = " ".join("%02X" % b for b in data[fo:fo + 8])
        ok_fields = []
        bad_fields = []
        for fld, expect in rec.items():
            if fld in ("addr", "va", "window", "label", "source", "note", "kind"):
                continue
            ev = str(expect)
            em = re.fullmatch(r"0x([0-9A-Fa-f]+)", ev)
            if em and len(em.group(1)) <= 8:
                # numeric value pin
                want = int(em.group(1), 16)
                if fld.startswith("raw_") or True:
                    # compare against physical derivation where applicable
                    if "imm32" in fld:
                        got = struct.unpack_from("<I", data, fo + 1)[0]
                        (ok_fields if got == want else bad_fields).append((fld, ev, "0x%08X" % got))
                    elif "rel32" in fld or "target" in fld:
                        rel = struct.unpack_from("<i", data, fo + 1)[0]
                        got = vaint + 5 + rel
                        (ok_fields if got == want else bad_fields).append((fld, ev, "0x%08X" % got))
                    elif "bytes" in fld:
                        gotn = norm_bytes(ev) if ev.startswith("-") or "-" in ev else ev.replace(" ", "").upper()
                        gotn = " ".join(gotn[i:i + 2] for i in range(0, len(gotn), 2))
                        physn = " ".join("%02X" % b for b in data[fo:fo + len(gotn.split())])
                        (ok_fields if gotn == physn else bad_fields).append((fld, ev, physn))
        if bad_fields:
            pin_bad.append({"key": key, "addr": va, "bad": bad_fields[:4]})
        else:
            pin_ok += 1

res["c10v2_pin_records_checked"] = n_pin
res["c10v2_pin_ok"] = pin_ok
res["c10v2_pin_bad_count"] = len(pin_bad)
res["c10v2_pin_bad_sample"] = pin_bad[:5]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res, indent=1))
