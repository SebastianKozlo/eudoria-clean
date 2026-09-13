# -*- coding: utf-8 -*-
# QC F1-KEY: class-ID = [class+8]. Independent census:
#  (1) all direct E8 calls to ctor ArkObjectClass 0x0070CF80; extract PUSH imm32 arg
#  (2) all E8 calls to ctor ArkObject 0x00726E70 (count)
#  (3) for each registration function: find the vtable written (C7 .. imm32 = vtable VA),
#      resolve vtable-4 -> COL -> TD -> RTTI name; decode $0-suffix (A=0..P=15 nibbles)
#      and cross-check against the imm32 (mangling <-> imm32 correlation)
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys, re
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import Bin, save_json

b = Bin(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe")
R = {}

NIBBLE = {chr(ord('A') + i): i for i in range(16)}  # A=0 .. P=15
def dec_dollar0(s):
    """MSVC $0<value>@ — each char is a nibble A..P (A=0..P=15)."""
    v = 0
    for ch in s:
        if ch not in NIBBLE:
            return None
        v = (v << 4) | NIBBLE[ch]
    return v

CT_CLASS = 0x0070CF80
CT_OBJ = 0x00726E70

calls_class = b.calls(CT_CLASS, 0xE8)
calls_obj = b.calls(CT_OBJ, 0xE8)
R["counts"] = dict(calls_to_0070CF80=len(calls_class), calls_to_00726E70=len(calls_obj))

# --- extract imm32 arg per registration call site ---
# expected pattern: 68 xx xx xx xx (PUSH imm32) somewhere in the ~32 bytes before the
# call, typically: PUSH imm32; PUSH <empty-string-ptr>; MOV ECX,ESI/ESX; CALL
regs = []
for c in calls_class:
    site = c["site_va"]
    window = b.rd(site - 40, 40)
    # find LAST 68 imm32 before call (closest to call)
    best = None
    for i in range(len(window) - 5, -1, -1):
        if window[i] == 0x68:
            imm = struct.unpack_from("<I", window, i + 1)[0]
            best = imm
            push_at = site - 40 + i
            break
    # check the empty-string arg2 pattern too: PUSH 0x00A7957B expected as the OTHER push
    regs.append(dict(call_site=hex(site), imm32_arg1=best, imm32_hex=(hex(best) if best else None),
                     push_at=hex(push_at) if best else None))

R["registrations"] = regs
imm_values = [r["imm32_arg1"] for r in regs if r["imm32_arg1"] is not None]
R["imm_census"] = {hex(v): imm_values.count(v) for v in sorted(set(imm_values))}
R["n_with_imm32"] = len(imm_values)

# --- function starts (walk back to prologue 6A FF / 55 8B EC / sub) — heuristic:
# find nearest preceding 'CC CC CC' padding or RET-run; function start = padding+1 ---
def func_start(va):
    off = b.va2off(va)
    lo = max(0, off - 0x8000)
    # search backwards for CC CC CC (inter-function padding)
    o = off
    while o > lo:
        if b.raw[o - 1] == 0xCC and b.raw[o - 2] == 0xCC and b.raw[o - 3] == 0xCC:
            return b.off2va(o)
        o -= 1
    return None

# --- vtable written inside each registration function ---
# scan function body [start, next CC-run] for C7 06/07/05/46/47/4E... imm32 patterns where
# imm32 is a VA in .rdata and [imm32-4] points to a COL; resolve the RTTI name.
def vtables_in_body(start_va, end_off):
    res = []
    off0 = b.va2off(start_va)
    o = off0
    while o < end_off:
        if b.raw[o] == 0xC7 and b.raw[o + 1] in (0x05, 0x06, 0x07, 0x46, 0x47, 0x4E, 0x86, 0x87):
            # C7 /0: MOV r/m32, imm32 -> modrm 0x05 (disp32), 06/07 (r/m), 46/47/4E/86/87...
            # decode disp: for simplicity accept C7 06/07 (MOV [ESI]/[EDI], imm32)
            if b.raw[o + 1] in (0x06, 0x07):
                imm = struct.unpack_from("<I", b.raw, o + 2)[0]
                col = b.u32va(imm - 4) if imm else None
                if col and 0x00A00000 <= col < 0x00C00000:
                    td = b.u32va(col + 0xC) if col else None
                    if td:
                        nm = b.cstr(td + 8, 160)
                        if nm and nm.startswith(".?AV"):
                            res.append(dict(vtable=hex(imm), rtti=nm, at=hex(b.off2va(o))))
                        o += 6
                        continue
        o += 1
    return res

# --- census of .?AV?$ArkObjectClassImpl@ strings in the whole image ---
impl_names = {}
pat = b".?AV?$ArkObjectClassImpl@"
i = b.raw.find(pat)
while i >= 0:
    end = b.raw.find(b"\x00", i)
    nm = b.raw[i:end].decode("ascii", "replace")
    va = b.off2va(i)
    m = re.match(r"\.\?AV\?\$ArkObjectClassImpl@V(\w+)@@\$0([A-P0-9]+)@", nm)
    decoded = dec_dollar0(m.group(2)) if m else None
    impl_names[hex(va)] = dict(rtti=nm, inner_class=m.group(1) if m else None,
                               suffix=m.group(2) if m else None, decoded_id=decoded)
    i = b.raw.find(pat, i + 1)
R["arkobjectclassimpl_rtti_census"] = impl_names
R["impl_count"] = len(impl_names)

# --- correlate: for each registration, find vtable+RTTI in its function ---
corr = []
for r in regs:
    site = int(r["call_site"], 16)
    fs = func_start(site)
    entry = dict(call_site=r["call_site"], imm32=r["imm32_arg1"], imm32_hex=r["imm32_hex"],
                 func_start=hex(fs) if fs else None)
    if fs:
        # body: from fs to next CC CC CC
        o0 = b.va2off(fs)
        o = o0
        end = o0
        while end + 3 < b.size:
            if b.raw[end] == 0xCC and b.raw[end + 1] == 0xCC and b.raw[end + 2] == 0xCC:
                break
            end += 1
        vts = vtables_in_body(fs, end)
        # pick vtables whose RTTI is an ArkObjectClassImpl
        impls = [v for v in vts if "ArkObjectClassImpl" in v["rtti"]]
        entry["vtables_all"] = vts
        entry["impl_rtti"] = impls[0] if impls else None
        if impls:
            nm = impls[0]["rtti"]
            m = re.match(r"\.\?AV\?\$ArkObjectClassImpl@V(\w+)@@\$0([A-P0-9]+)@", nm)
            entry["inner_class"] = m.group(1) if m else None
            entry["mangling_decoded"] = dec_dollar0(m.group(2)) if m else None
            entry["mangling_matches_imm32"] = (entry["mangling_decoded"] == r["imm32_arg1"]) if m and entry["mangling_decoded"] is not None else None
    corr.append(entry)
R["correlation"] = corr

match = [c for c in corr if c.get("mangling_matches_imm32") is True]
mismatch = [c for c in corr if c.get("mangling_matches_imm32") is False]
R["correlation_summary"] = dict(total=len(corr), with_impl_rtti=len([c for c in corr if c.get("impl_rtti")]),
                                match=len(match), mismatch=len(mismatch))

# --- the 4 required pairs ---
def pair_for(classname):
    for c in corr:
        if c.get("inner_class") == classname:
            return c
    return None
required = {}
for cn in ("ArkSurgeonObject", "ArkParameterContainer", "ArkRealWorldItemObject", None):
    pass
# find class for imm32 0x4E26 (20006):
c4e26 = [c for c in corr if c["imm32"] == 0x4E26]
R["pair_0x4E26"] = c4e26
R["required_pairs"] = dict(
    surgeon=pair_for("ArkSurgeonObject"),
    container=pair_for("ArkParameterContainer"),
)
# realworld item: search impl census for the name
rwi = {k: v for k, v in impl_names.items() if v["inner_class"] and "RealWorld" in v["inner_class"]}
R["realworld_impls"] = rwi
rwi_reg = [c for c in corr if c.get("inner_class") and "RealWorld" in c["inner_class"]]
R["pair_realworld"] = rwi_reg

p = save_json("QC_F1_CLASSID.json", R)
print("saved", p)
print("counts:", R["counts"], "with imm32:", R["n_with_imm32"])
print("imm census:", R["imm_census"])
print("impl count:", R["impl_count"])
print("correlation:", R["correlation_summary"])
print("pair surgeon:", R["required_pairs"]["surgeon"])
print("pair container:", R["required_pairs"]["container"])
print("pair 0x4E26:", R["pair_0x4E26"])
print("pair realworld:", R["pair_realworld"])
