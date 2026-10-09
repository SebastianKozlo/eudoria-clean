#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""qc_remeasure.py — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009
INDEPENDENT fresh-context internal QC re-measurement (pe-master-auditor).

Method independence from the executor:
  * OWN minimal PE parser (PE header -> section table -> VA->file offset).
    Source B (checker_plus4_successor_v2.py) is NOT imported here.
  * OWN x86-32 boundary decoder, written independently of the executor's
    x86_minidec (different structure: opcode-class table + ModRM/SIB
    split, writes/reads sets derived per opcode class).
  * OWN byte pins, clobber scans, mutants (in-memory copies only),
    RTTI chain walk, rel32 recomputation, token-gate scans (own regexes),
    budget byte recount from the executor's own script logic.

The EXE file is NEVER modified (all mutations run on in-memory copies).
python -B; stdlib only; output = stdout (JSON at the end).
"""
import hashlib
import json
import os
import re
import struct
import sys

RUN_ID = "PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009"
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # package dir
REPO = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
EXE_SIZE_EXPECTED = 8015872
EXE_SHA_EXPECTED = ("E7785430E81DFFE648CE8F5312414B17"
                    "BC9FCE61389689A22F753765D5280F31")  # 64 hex chars


# ---------------------------------------------------------------- own PE parser
class MyPE:
    def __init__(self, data):
        self.data = data
        if data[:2] != b"MZ":
            raise SystemExit("FAIL: no MZ")
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise SystemExit("FAIL: no PE sig")
        coff = e_lfanew + 4
        self.num_sections = struct.unpack_from("<H", data, coff + 2)[0]
        opt_size = struct.unpack_from("<H", data, coff + 16)[0]
        opt = coff + 20
        magic = struct.unpack_from("<H", data, opt)[0]
        if magic != 0x10B:
            raise SystemExit("FAIL: not PE32 (magic=%#x)" % magic)
        self.image_base = struct.unpack_from("<I", data, opt + 28)[0]
        self.section_alignment = struct.unpack_from("<I", data, opt + 32)[0]
        self.file_alignment = struct.unpack_from("<I", data, opt + 36)[0]
        sec_tbl = opt + opt_size
        self.sections = []
        for i in range(self.num_sections):
            s = sec_tbl + 40 * i
            name = data[s:s + 8].rstrip(b"\x00").decode("ascii", "replace")
            vsize = struct.unpack_from("<I", data, s + 8)[0]
            vaddr = struct.unpack_from("<I", data, s + 12)[0]
            rsize = struct.unpack_from("<I", data, s + 16)[0]
            rptr = struct.unpack_from("<I", data, s + 20)[0]
            self.sections.append({
                "name": name, "vsize": vsize, "vaddr": vaddr,
                "rsize": rsize, "rptr": rptr})

    def off(self, va, n=1):
        """VA -> file offset, fail-closed, range-checked."""
        rva = va - self.image_base
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rsize"]):
                fo = rva - s["vaddr"] + s["rptr"]
                if fo + n > len(self.data) or fo < 0:
                    raise SystemExit(
                        "FAIL: range outside file for VA %#x" % va)
                return fo
        raise SystemExit("FAIL: VA %#x not in any section" % va)

    def read(self, va, n):
        fo = self.off(va, n)
        return self.data[fo:fo + n]

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]


# ------------------------------------------------------------ own x86 decoder
GPR = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
GPR8 = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]
GPR16 = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"]


class QcDecodeError(Exception):
    pass


def my_modrm(buf, i):
    """Return (mod, reg, rm, base, index, scale, disp_bytes_len, disp, mem)."""
    m = buf[i]
    mod = (m >> 6) & 3
    reg = (m >> 3) & 7
    rm = m & 7
    n = 1
    base = None
    index = None
    scale = 1
    disp = None
    if mod == 3:
        return {"mod": mod, "reg": reg, "rm": rm, "size": n, "base": None,
                "index": None, "scale": 0, "disp": None, "mem": False}
    if rm == 4:  # SIB
        sib = buf[i + 1]
        n += 1
        scale = 1 << ((sib >> 6) & 3)
        index = ((sib >> 3) & 7)
        base = sib & 7
        if index == 4:
            index = None
        if mod == 0 and base == 5:
            base = None
            disp = struct.unpack_from("<I", buf, i + 2)[0]
            n += 4
        elif mod == 1:
            disp = struct.unpack_from("<b", buf, i + 2)[0]
            n += 1
        elif mod == 2:
            disp = struct.unpack_from("<i", buf, i + 2)[0]
            n += 4
    elif mod == 0 and rm == 5:
        disp = struct.unpack_from("<I", buf, i + 1)[0]
        n += 4
    else:
        base = rm
        if mod == 1:
            disp = struct.unpack_from("<b", buf, i + 1)[0]
            n += 1
        elif mod == 2:
            disp = struct.unpack_from("<i", buf, i + 1)[0]
            n += 4
    return {"mod": mod, "reg": reg, "rm": rm, "size": n, "base": base,
            "index": index, "scale": scale, "disp": disp, "mem": True}


def _mem_str(mr, width_tag=""):
    if mr["base"] is None and mr["index"] is None:
        return "[0x%08x]" % (mr["disp"] & 0xffffffff)
    parts = []
    if mr["base"] is not None:
        parts.append(GPR[mr["base"]])
    if mr["index"] is not None:
        parts.append("%s*%d" % (GPR[mr["index"]], mr["scale"]))
    s = "[" + "+".join(parts)
    if mr["disp"]:
        s += "%+#x" % mr["disp"]
    s += "]"
    return s


def my_decode(buf, off, va):
    """Decode one instruction; returns dict. Independent implementation."""
    start = off
    b0 = buf[off]
    pre66 = False
    if b0 == 0x66:
        pre66 = True
        off += 1
        b0 = buf[off]
    out = {"va": va, "writes": set(), "reads": set(), "width": 16 if pre66
           else 32, "is_call": False, "is_jump": False, "mem_dst": None,
           "prefix66": pre66}
    # ---- single-byte push ----
    if 0x50 <= b0 <= 0x57:
        out["mnemonic"] = "push"
        out["length"] = off + 1 - start
        out["bytes"] = bytes(buf[start:off + 1])
        out["reads"].add(GPR[b0 - 0x50])
        out["writes"].add("esp")  # implicit
        return out
    if b0 in (0x88, 0x89, 0x8A, 0x8B, 0x8D, 0x33, 0x3B):
        mr = my_modrm(buf, off + 1)
        off += 1 + mr["size"]
        reg32 = GPR[mr["reg"]]
        if b0 == 0x89:      # mov r/m, r
            if mr["mem"]:
                out["mnemonic"] = "mov"
                out["dst"] = _mem_str(mr)
                out["src"] = (GPR16[mr["reg"]] if pre66
                              else reg32)
                if mr["base"] is not None:
                    out["reads"].add(GPR[mr["base"]])
                out["mem_dst"] = {"base": (GPR[mr["base"]]
                                           if mr["base"] is not None else None),
                                  "disp": mr["disp"] or 0}
            else:
                out["mnemonic"] = "mov"
                out["dst"] = (GPR16[mr["rm"]] if pre66
                             else GPR[mr["rm"]])
                out["src"] = (GPR16[mr["reg"]] if pre66
                              else reg32)
                out["writes"].add(GPR[mr["rm"]])
                out["reads"].add(GPR[mr["reg"]])
        elif b0 == 0x88:     # mov r/m8, r8
            out["mnemonic"] = "mov"
            out["width"] = 8
            if mr["mem"]:
                out["dst"] = _mem_str(mr)
                if mr["base"] is not None:
                    out["reads"].add(GPR[mr["base"]])
                out["mem_dst"] = {"base": (GPR[mr["base"]]
                                           if mr["base"] is not None else None),
                                  "disp": mr["disp"] or 0}
            else:
                out["dst"] = GPR8[mr["rm"]]
                out["writes"].add(GPR[mr["rm"]] if mr["rm"] < 4
                                  else GPR[mr["rm"]])
            out["src"] = GPR8[mr["reg"]]
        elif b0 == 0x8B:     # mov r, r/m
            out["mnemonic"] = "mov"
            out["dst"] = (GPR16[mr["reg"]] if pre66 else reg32)
            out["src"] = _mem_str(mr) if mr["mem"] else (
                GPR16[mr["rm"]] if pre66 else GPR[mr["rm"]])
            out["writes"].add(reg32)
            if mr["mem"]:
                if mr["base"] is not None:
                    out["reads"].add(GPR[mr["base"]])
            else:
                out["reads"].add(GPR[mr["rm"]])
        elif b0 == 0x8D:     # lea r, m
            if not mr["mem"]:
                raise QcDecodeError("lea reg,reg @%#x" % va)
            out["mnemonic"] = "lea"
            out["dst"] = reg32
            out["src"] = _mem_str(mr)
            out["writes"].add(reg32)
            if mr["base"] is not None:
                out["reads"].add(GPR[mr["base"]])
        elif b0 == 0x33:     # xor r, r/m
            out["mnemonic"] = "xor"
            out["dst"] = reg32
            out["src"] = _mem_str(mr) if mr["mem"] else GPR[mr["rm"]]
            out["writes"].add(reg32)
            if not mr["mem"]:
                out["reads"].add(GPR[mr["rm"]])
        else:                # 0x3B cmp — not expected in window
            raise QcDecodeError("cmp @%#x" % va)
    elif b0 == 0xC7:
        mr = my_modrm(buf, off + 1)
        if mr["reg"] != 0:
            raise QcDecodeError("C7 reg!=0 @%#x" % va)
        off += 1 + mr["size"]
        imm = struct.unpack_from("<I", buf, off)[0]
        off += 4
        out["mnemonic"] = "mov"
        out["imm32"] = imm
        if mr["mem"]:
            out["dst"] = _mem_str(mr)
            out["mem_dst"] = {"base": (GPR[mr["base"]]
                                       if mr["base"] is not None else None),
                              "disp": mr["disp"] or 0}
            if mr["base"] is not None:
                out["reads"].add(GPR[mr["base"]])
        else:
            out["dst"] = GPR[mr["rm"]]
            out["writes"].add(GPR[mr["rm"]])
        out["src"] = "0x%08x" % imm
    elif b0 == 0xD9:
        sub = buf[off + 1]
        if (sub >> 6) & 3 == 3:   # x87 register form
            if sub == 0xEE:
                out["mnemonic"] = "fldz"
            elif sub == 0xE8:
                out["mnemonic"] = "fld1"
            else:
                raise QcDecodeError("D9 /r mod3 @%#x" % va)
            off += 2
        else:
            mr = my_modrm(buf, off + 1)
            off += 1 + mr["size"]
            if mr["reg"] == 2:
                out["mnemonic"] = "fst"
            elif mr["reg"] == 3:
                out["mnemonic"] = "fstp"
            else:
                raise QcDecodeError("D9 mem reg=%d @%#x"
                                    % (mr["reg"], va))
            out["dst"] = _mem_str(mr)
            out["src"] = "st0"
            out["mem_dst"] = {"base": (GPR[mr["base"]]
                                       if mr["base"] is not None else None),
                              "disp": mr["disp"] or 0}
            if mr["base"] is not None:
                out["reads"].add(GPR[mr["base"]])
    elif b0 == 0xE8:
        rel = struct.unpack_from("<i", buf, off + 1)[0]
        off += 5
        out["mnemonic"] = "call"
        out["is_call"] = True
        out["call_target"] = (va + 5 + rel) & 0xffffffff
    else:
        raise QcDecodeError("unsupported opcode %#04x @%#x" % (b0, va))
    out["length"] = off - start
    out["bytes"] = bytes(buf[start:off])
    return out


def linear_decode(pe, va_from, va_to):
    ins = []
    va = va_from
    while va < va_to:
        fo = pe.off(va)
        d = my_decode(pe.data, fo, va)
        d["text"] = "%s %s, %s" % (d["mnemonic"], d.get("dst", ""),
                                   d.get("src", "")) if d.get("dst") is not \
            None else d["mnemonic"]
        ins.append(d)
        va += d["length"]
    return ins


def hx(b):
    return " ".join("%02X" % c for c in b)


# ------------------------------------------------------------------- main
def main():
    R = {"run_id": RUN_ID, "qc_agent": "pe-master-auditor fresh-context"}

    # -- identity (own hash) --
    with open(EXE, "rb") as f:
        data = f.read()
    sha = hashlib.sha256(data).hexdigest().upper()
    R["exe"] = {"size": len(data), "sha256": sha,
                "size_match": len(data) == EXE_SIZE_EXPECTED,
                "sha_match": sha == EXE_SHA_EXPECTED}
    if not R["exe"]["size_match"] or not R["exe"]["sha_match"]:
        print(json.dumps(R))
        return 1

    pe = MyPE(data)
    R["pe"] = {"image_base": pe.image_base,
               "section_alignment": pe.section_alignment,
               "file_alignment": pe.file_alignment,
               "sections": pe.sections}

    # -- VA->offset mapping check (own) --
    store_va = 0x0085B281
    store_off = pe.off(store_va, 3)
    R["va_offset_check"] = {
        "va": store_va, "my_file_offset": store_off,
        "executor_claimed_offset": 4567681,
        "match": store_off == 4567681,
        "hex": hx(pe.read(store_va, 3))}

    # ================= DUTY 1: byte re-measurements =================
    pins = {
        "store_0x0085B281": (0x0085B281, "89 4E 44"),
        "boundary_ret_0x0085B1AC": (0x0085B1AC, "C3"),
        "boundary_pad_0x0085B1AD_AF": (0x0085B1AD, "CC CC CC"),
        "entry_0x0085B1B0": (0x0085B1B0, "8B 44 24 08"),
        "vbase_stamp_0x0085B1C1": (0x0085B1C1, "C7 06 4C 1E A9 00"),
        "arg1_load_0x0085B1DA": (0x0085B1DA, "8B 7C 24 14"),
        "zeroinit_0x0085B1E4": (0x0085B1E4, "D9 56 44"),
        "zeroinit_0x0085B1E7": (0x0085B1E7, "D9 56 48"),
        "zeroinit_0x0085B1EC": (0x0085B1EC, "D9 56 4C"),
        "ecx_from_edi_0x0085B24B": (0x0085B24B, "8B CF"),
        "call_0x0085B27A": (0x0085B27A, "E8 E1 B2 EE FF"),
        "load_ecx_eax_0x0085B27F": (0x0085B27F, "8B 08"),
        "copy48_0x0085B287": (0x0085B287, "89 56 48"),
        "copy4C_0x0085B28D": (0x0085B28D, "89 46 4C"),
        "caller_esi_0x00528E76": (0x00528E76, "8B F1"),
        "caller_ecx_0x00528E8B": (0x00528E8B, "8B CE"),
        "caller_call_0x00528E8D": (0x00528E8D, "E8 1E 23 33 00"),
        "derived_vtable_0x00528EA2": (0x00528EA2, "C7 06 B0 DC A7 00"),
        "accessor_0x00746560": (0x00746560, "8D 41 08 C3"),
        # exclusion-record pins (census verification, duty 5)
        "excl_CG_rep_0x00509557": (0x00509557, "F3 A5"),
        "excl_CG_lea_0x0050954D": (0x0050954D, "8D 7B 4C"),
        "excl_CG_movbx_0x00509518": (0x00509518, "8B D9"),
        "excl_CG_sf_receipt_0x00529025": (0x00529025, "8B 8E C0 00 00 00"),
        "excl_CH_cmo0xC0_0x00528FEA": (0x00528FEA, "89 86 C0 00 00 00"),
        "excl_CI_cmo0xB4_0x00529058": (0x00529058, "D9 9E B4 00 00 00"),
        "excl_CJ_0x0074539B": (0x0074539B, "89 46 44"),
        "excl_CJ_0x007453A4": (0x007453A4, "89 4E 48"),
        "excl_CJ_0x007453AD": (0x007453AD, "89 56 4C"),
        "excl_CK_0x008551CA": (0x008551CA, "89 46 44"),
        "excl_CL_fst_0x005093E9": (0x005093E9, "D9 55 44"),
        "excl_CL_fst_0x005093F1": (0x005093F1, "D9 55 48"),
        "excl_CL_mov_0x0050944C": (0x0050944C, "89 45 44"),
        "excl_CL_mov_0x00509455": (0x00509455, "89 4D 48"),
        "excl_CM_0x008BD750": (0x008BD750, "89 46 44"),
        "excl_CN_0x006C8FBB": (0x006C8FBB, "89 5E 48"),
        "excl_CN_0x006C8FBE": (0x006C8FBE, "89 5E 4C"),
        "excl_CO_0x006C94FF": (0x006C94FF, "89 46 44"),
        "excl_CP_vtable_0x005D48B6": (0x005D48B6, "C7 06 A4 14 A8 00"),
    }
    R["pins"] = {}
    for name, (va, expect) in pins.items():
        n = len(expect.split())
        got = hx(pe.read(va, n))
        R["pins"][name] = {"va": va, "expected": expect, "measured": got,
                           "match": got == expect}
    # extra: census C-K secondary claim "+0x48/+0x4C stores @0x00855260 region"
    R["excl_CK_region_0x00855260_hex"] = hx(pe.read(0x00855260, 12))

    # rel32 recomputation (own arithmetic)
    rel_store_call = struct.unpack("<i", pe.read(0x0085B27B, 4))[0]
    rel_caller_call = struct.unpack("<i", pe.read(0x00528E8E, 4))[0]
    R["rel32"] = {
        "call_0x0085B27A": {"rel32_signed": rel_store_call,
                            "target": (0x0085B27A + 5 + rel_store_call)
                            & 0xffffffff,
                            "expected": 0x00746560,
                            "match": (0x0085B27A + 5 + rel_store_call)
                            == 0x00746560},
        "call_0x00528E8D": {"rel32_signed": rel_caller_call,
                            "target": (0x00528E8D + 5 + rel_caller_call)
                            & 0xffffffff,
                            "expected": 0x0085B1B0,
                            "match": (0x00528E8D + 5 + rel_caller_call)
                            == 0x0085B1B0}}

    # RTTI chains (own walk, MSVC RTTI: vtable[-1]=COL; COL+12=TD; TD+8=name)
    def rtti(vtable, exp_col, exp_td, exp_name):
        col_ptr = pe.u32(vtable - 4)
        col = pe.read(col_ptr, 20)
        sig, off, cd, ptd, pcd = struct.unpack("<5I", col)
        namelen = len(exp_name) + 1
        name_bytes = pe.read(ptd + 8, namelen)
        name = name_bytes[:-1].decode("ascii", "replace")
        null_ok = name_bytes[-1] == 0
        return {"vtable": vtable, "col_ptr": col_ptr, "col_sig": sig,
                "col_offset": off, "col_cd": cd, "td": ptd, "pcd": pcd,
                "name": name, "null_terminated": null_ok,
                "bytes_read": 4 + 20 + namelen,
                "match": (sig == 0 and col_ptr == exp_col and ptd == exp_td
                          and name == exp_name and null_ok)}
    R["rtti"] = {
        "vtable_0x00A91E4C": rtti(0x00A91E4C, 0x00AB33D0, 0x00B7997C,
                                  ".?AVMovableObject@@"),
        "vtable_0x00A7DCB0": rtti(0x00A7DCB0, 0x00AA17CC, 0x00B79958,
                                  ".?AVClientMovableObject@@")}

    # ================= DUTY 2: own boundary decode =================
    W1_VA, W1_LEN = 0x0085B1A8, 0xE8
    w1 = pe.read(W1_VA, W1_LEN)
    R["w1_hex_own"] = hx(w1)
    ins_list = linear_decode(pe, 0x0085B1B0, 0x0085B290)
    R["decode"] = {
        "instruction_count": len(ins_list),
        "total_bytes": sum(i["length"] for i in ins_list),
        "ends_at": ins_list[-1]["va"] + ins_list[-1]["length"],
        "ends_exact_0x0085B290":
            ins_list[-1]["va"] + ins_list[-1]["length"] == 0x0085B290,
        "any_jump_or_unknown": any(i.get("is_jump") for i in ins_list),
        "calls": [i["va"] for i in ins_list if i["is_call"]],
        "instructions": [
            {"va": i["va"], "len": i["length"], "bytes": hx(i["bytes"]),
             "text": i["text"], "writes": sorted(i["writes"])}
            for i in ins_list]}
    # key boundary starts
    key = [0x0085B1B7, 0x0085B1C1, 0x0085B1DA, 0x0085B1E4, 0x0085B1E7,
           0x0085B1EC, 0x0085B24B, 0x0085B27A, 0x0085B27F, 0x0085B281,
           0x0085B284, 0x0085B287, 0x0085B28A, 0x0085B28D]
    by_va = {i["va"]: i for i in ins_list}
    R["boundary_starts"] = {
        ("%08x" % va): (hx(by_va[va]["bytes"]) if va in by_va else None)
        for va in key}
    sel = by_va.get(0x0085B281)
    R["selected_store_own_decode"] = {
        "va": 0x0085B281, "bytes": hx(sel["bytes"]),
        "len": sel["length"], "mnemonic": sel["mnemonic"],
        "dst": sel["dst"], "src": sel["src"], "width": sel["width"],
        "mem_dst": sel["mem_dst"], "writes": sorted(sel["writes"]),
        "reads": sorted(sel["reads"]),
        "file_offset": pe.off(0x0085B281, 3)}
    # zero-init triple + copy triple mnemonics from MY decode
    R["triple_check"] = {
        "copy_triple": {
            "0x0085B281": {"bytes": hx(by_va[0x0085B281]["bytes"]),
                           "text": by_va[0x0085B281]["text"]},
            "0x0085B287": {"bytes": hx(by_va[0x0085B287]["bytes"]),
                           "text": by_va[0x0085B287]["text"]},
            "0x0085B28D": {"bytes": hx(by_va[0x0085B28D]["bytes"]),
                           "text": by_va[0x0085B28D]["text"]}},
        "zero_init_triple": {
            "0x0085B1E4": {"bytes": hx(by_va[0x0085B1E4]["bytes"]),
                           "text": by_va[0x0085B1E4]["text"],
                           "mnemonic": by_va[0x0085B1E4]["mnemonic"]},
            "0x0085B1E7": {"bytes": hx(by_va[0x0085B1E7]["bytes"]),
                           "text": by_va[0x0085B1E7]["text"],
                           "mnemonic": by_va[0x0085B1E7]["mnemonic"]},
            "0x0085B1EC": {"bytes": hx(by_va[0x0085B1EC]["bytes"]),
                           "text": by_va[0x0085B1EC]["text"],
                           "mnemonic": by_va[0x0085B1EC]["mnemonic"]}}}

    # ================= DUTY 4: clobber scans (own) =================
    def writers_between(lo_excl, hi_incl, reg):
        return [i["va"] for i in ins_list
                if lo_excl < i["va"] <= hi_incl and reg in i["writes"]]
    def calls_between(lo_excl, hi_excl):
        return [i["va"] for i in ins_list
                if lo_excl < i["va"] < hi_excl and i["is_call"]]
    R["clobber_scan"] = {
        "esi_writers_(0x0085B1B7,0x0085B281]":
            writers_between(0x0085B1B7, 0x0085B281, "esi"),
        "edi_writers_(0x0085B1DA,0x0085B24B]":
            writers_between(0x0085B1DA, 0x0085B24B, "edi"),
        "ecx_writers_(0x0085B24B,0x0085B27A)":
            writers_between(0x0085B24B, 0x0085B27A - 1, "ecx"),
        "ecx_writers_(0x0085B27F,0x0085B281)":
            writers_between(0x0085B27F, 0x0085B281 - 1, "ecx"),
        "calls_(0x0085B24B,0x0085B27A)": calls_between(0x0085B24B,
                                                      0x0085B27A),
        "calls_(0x0085B27F,0x0085B281)": calls_between(0x0085B27F,
                                                      0x0085B281),
        "esi_def_sites": [i["va"] for i in ins_list if "esi" in i["writes"]],
        "edi_def_sites": [i["va"] for i in ins_list if "edi" in i["writes"]],
        "ecx_def_sites": [i["va"] for i in ins_list if "ecx" in i["writes"]],
        "esi_writers_(0x0085B1B7,0x0085B28D]":
            writers_between(0x0085B1B7, 0x0085B28D, "esi")}
    # stack proof for arg1 = [esp+0x14]
    pro = ins_list[0]
    R["arg1_stack_proof"] = {
        "first_insn": {"va": pro["va"], "bytes": hx(pro["bytes"]),
                       "text": pro["text"]},
        "pushes_before_0x0085B1DA": [
            {"va": i["va"], "text": i["text"]} for i in ins_list
            if 0x0085B1B0 <= i["va"] < 0x0085B1DA
            and i["mnemonic"] == "push"],
        "arg1_slot_after_4_pushes": "[esp+0x14]",
        "note": "entry [esp+4] (arg1) + 0x10 (4 pushes) = [esp+0x14]"}

    # ================= DUTY 7a: own mutation controls =================
    def pin_ok(buffer_, va, expect_hex):
        n = len(expect_hex.split())
        fo = pe.off(va, n)
        return hx(bytes(buffer_[fo:fo + n])) == expect_hex

    m1 = bytearray(data)
    m1[store_off] = 0x8B                      # opcode 89 -> 8B (load)
    m3 = bytearray(data)
    m3[store_off + 2] = 0x48                   # disp 0x44 -> 0x48
    m5 = bytearray(data)
    acc_off = pe.off(0x00746560, 4)
    m5[acc_off] ^= 0xFF                        # corrupt accessor byte 0
    R["own_mutants"] = {
        "M1_opcode": {"real_pass": pin_ok(data, store_va, "89 4E 44"),
                      "mutant_fail": not pin_ok(m1, store_va, "89 4E 44")},
        "M3_offset": {"real_pass": pin_ok(data, store_va, "89 4E 44"),
                      "mutant_fail": not pin_ok(m3, store_va, "89 4E 44")},
        "M2_va_shift": {"shifted_fail":
                        not pin_ok(data, 0x0085B282, "89 4E 44")},
        "M5_accessor": {"real_pass": pin_ok(data, 0x00746560, "8D 41 08 C3"),
                        "mutant_fail":
                        not pin_ok(m5, 0x00746560, "8D 41 08 C3")},
        "M6_sf_conflation": {
            "selected_store_va": store_va,
            "sf_store_va_committed": 0x00509557,
            "sf_receiver_reg": "ebx (mov ebx,ecx @0x00509518) with "
                               "edi=[ebx+0x4C] (lea @0x0050954D), "
                               "SF received via ecx=[CMO+0xC0] @0x00529025",
            "selected_receiver": "esi = base-ctor this (mov esi,ecx "
                                  "@0x0085B1B7)",
            "distinct": (store_va != 0x00509557
                         and R["pins"]["excl_CG_rep_0x00509557"]["match"]
                         and R["pins"]["excl_CG_lea_0x0050954D"]["match"]
                         and R["pins"]["excl_CG_movbx_0x00509518"]["match"]
                         and
                         R["pins"]["excl_CG_sf_receipt_0x00529025"]["match"])}}

    # ================= DUTY 6: budget byte recount =================
    # Executor windows: W1 232, W2 4, W3 52; RTTI reads per executor's own
    # script: u32(vtable-4)=4 + read(col,20) + read(ptd+8, len(name)+1)
    mo_name = ".?AVMovableObject@@"
    cmo_name = ".?AVClientMovableObject@@"
    rtti_mo_bytes = 4 + 20 + len(mo_name) + 1
    rtti_cmo_bytes = 4 + 20 + len(cmo_name) + 1
    total = 232 + 4 + 52 + rtti_mo_bytes + rtti_cmo_bytes
    R["budget_recount"] = {
        "W1": 232, "W2": 4, "W3": 52,
        "rtti_0x00A91E4C_bytes": rtti_mo_bytes,
        "rtti_0x00A7DCB0_bytes": rtti_cmo_bytes,
        "len_movableobject_name": len(mo_name),
        "len_clientmovableobject_name": len(cmo_name),
        "my_total_bytes_read_by_executor_script": total,
        "executor_declared_total": 381,
        "executor_declared_rtti_cmo_component": 49,
        "match": total == 381}

    # ============ DUTY 7b: own token-gate scans (ALL package files) ========
    forbidden = {
        "WORLD_XYZ_RECOVERED=YES":
            re.compile(r"WORLD_XYZ_RECOVERED\s*=\s*YES", re.I),
        "GLOBAL_COORDINATE_FRAME=ESTABLISHED/YES":
            re.compile(r"GLOBAL_COORDINATE_FRAME\s*=\s*(ESTABLISHED|YES)",
                       re.I),
        "HISTORICAL_PLACEMENT(_RECORD)=ESTABLISHED/YES/RECOVERED":
            re.compile(r"HISTORICAL_PLACEMENT(?:_RECORD)?\s*=\s*"
                       r"(ESTABLISHED|YES|RECOVERED)", re.I),
        "INSTANCE_MODEL_JOIN=ESTABLISHED/YES/CONFIRMED":
            re.compile(r"INSTANCE_MODEL_JOIN\s*=\s*"
                       r"(ESTABLISHED|YES|CONFIRMED)", re.I),
        "STORES THE WORLD/GLOBAL POSITION":
            re.compile(r"STORES?\s+THE\s+(WORLD|GLOBAL|HISTORICAL)\s+"
                       r"(POSITION|XYZ|COORDINATE)", re.I),
        "equality conflation CMO+0x4C":
            re.compile(r"CMO\+0x4C\s*(?:==|is|=)\s*"
                       r"(?:SF\+0x4C|NiNode\+0x5C|m_kLocal|m_kWorld)",
                       re.I),
        "equality conflation general":
            re.compile(r"(?:CMO\+0x4[48C])\s*(?:==|is)\s*"
                       r"(?:SF\+0x4[48C]|NiNode\+0x5C|m_kLocal|m_kWorld)",
                       re.I),
    }
    transform_active = re.compile(
        r"SAME_INSTANCE_TRANSFORM_RELATION\s*=\s*CONFIRMED_STATIC", re.I)
    transform_ctx_markers = ("supersede", "supersession", "superseded",
                             "historical", "not qualified", "not_qualified",
                             "must not", "j3", "s-5", "earlier",
                             "prior", "was", "pre-registered")
    promo = re.compile(r"\+0x4[48c].{0,80}position|"
                       r"position.{0,80}\+0x4[48c]", re.I)
    promo_ctx = ("historical", "superseded", "prior", "unverified",
                 "not promoted", "ceiling", "label", "context", "pozcja",
                 "must not", "no promotion", "forbidden", "if this run",
                 "falsifier", "process control", "would fail", "gate",
                 "no claim", "does not", "run makes no")

    hits = {"forbidden": [], "transform_static_mentions": [],
           "promotion_probe_hits": [], "files_scanned": []}
    for root, _dirs, files in os.walk(PKG):
        for fn in files:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, PKG)
            if rel.startswith("03_SCRIPTS" + os.sep) and \
                    fn.startswith("qc_"):
                continue  # my own QC scripts excluded from this scan
            hits["files_scanned"].append(rel)
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                prev = []
                for lineno, line in enumerate(f, 1):
                    for tag, rx in forbidden.items():
                        if rx.search(line):
                            hits["forbidden"].append(
                                {"file": rel, "line": lineno,
                                 "tag": tag,
                                 "text": line.strip()[:200]})
                    if transform_active.search(line):
                        low = line.lower()
                        marked = any(m in low
                                     for m in transform_ctx_markers)
                        hits["transform_static_mentions"].append(
                            {"file": rel, "line": lineno,
                             "supersession_marked": marked,
                             "text": line.strip()[:200]})
                    if promo.search(line):
                        ctx = " ".join(prev[-2:] + [line]).lower()
                        if not any(m in ctx for m in promo_ctx):
                            hits["promotion_probe_hits"].append(
                                {"file": rel, "line": lineno,
                                 "text": line.strip()[:200]})
                    prev.append(line)
                    if len(prev) > 2:
                        prev.pop(0)
    R["token_scan"] = {
        "files_scanned_count": len(hits["files_scanned"]),
        "files_scanned": sorted(hits["files_scanned"]),
        "forbidden_hits": hits["forbidden"],
        "transform_CONFIRMED_STATIC_mentions":
            hits["transform_static_mentions"],
        "unmarked_transform_mentions": [
            h for h in hits["transform_static_mentions"]
            if not h["supersession_marked"]],
        "promotion_probe_hits": hits["promotion_probe_hits"]}

    # ================= status-epistemology token presence =================
    def grep_pkg(pattern):
        rx = re.compile(pattern)
        found = []
        for root, _d, fl in os.walk(PKG):
            for fn in fl:
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, PKG)
                if rel.startswith("03_SCRIPTS" + os.sep) and \
                        fn.startswith("qc_"):
                    continue
                with open(p, "r", encoding="utf-8",
                          errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        if rx.search(line):
                            found.append("%s:%d" % (rel, i))
        return found
    R["epistemology_tokens"] = {
        "FIELD_SEMANTICS_UNVERIFIED":
            grep_pkg(r"FIELD_SEMANTICS\s*=\s*UNVERIFIED"),
        "WORLD_XYZ_RECOVERED_NO":
            grep_pkg(r"WORLD_XYZ_RECOVERED\s*=\s*NO"),
        "WORLD_INSTANCE_IDENTITY_NOT_ESTABLISHED":
            grep_pkg(r"WORLD_INSTANCE_IDENTITY\s*=\s*NOT_ESTABLISHED"),
        "HISTORICAL_PLACEMENT_NOT_ESTABLISHED":
            grep_pkg(r"HISTORICAL_PLACEMENT\s*=\s*NOT_ESTABLISHED"),
        "coverage_split_ CLIENT/RECON/HISTORICAL":
            grep_pkg(r"CLIENT_KNOWLEDGE_COVERAGE"),
        "J3_standing_NOT_QUALIFIED":
            grep_pkg(r"SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN"
                     r"\s*=\s*NOT_QUALIFIED_BY_ORIGINAL_SCOPE"),
        "J3_edge_FAIL_preserved":
            grep_pkg(r"ORIGINAL_EDGE_BUDGET_COMPLIANCE\s*=\s*FAIL")}

    print(json.dumps(R, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
