#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""corrected_qc_decoder.py — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

CORRECTED QC DECODER — the fresh-QC-worker successor of the HISTORICAL QC
decoder of PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009
(03_SCRIPTS/qc_remeasure.py, 31970 B /
4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B3E2F2E71B3EB5B3F3F8DDE1A — immutable).

EXPLICIT MAPPING (contract section 3):

  OLD_QC_SCRIPT:
    docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/qc_remeasure.py
    (historical, IMMUTABLE, not edited — its behavior stays documented there)

  CORRECTED_QC_SCRIPT:
    docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/03_SCRIPTS/corrected_qc_decoder.py
    (this file — written by the fresh-QC worker phase, NOT by the executor
    phase; SIZE/SHA256 recorded in QC_RESULTS.json)

IMPLEMENTATION LINEAGE AND INDEPENDENCE (contract section 7):

  This successor continues the historical QC decoder's STYLE (my_modrm /
  _mem_str / my_decode / linear_decode structure over a PE image object,
  GPR/GPR8/GPR16 tables, QcDecodeError), with the CMO-C1/P2 alias defect
  FIXED. It is an INDEPENDENT implementation with respect to the PRODUCTION
  corrected executor decoder (03_SCRIPTS/corrected_executor_decoder.py):

    * the production decoder's mapping helper (BYTE8_PARENT /
      BYTE8_BIT_RANGE dict literals) is NOT imported, NOT copied and NOT
      transcribed here;
    * the parent attribution is implemented ARITHMETICALLY from the x86-32
      byte-register encoding: byte-register index i in 0..7 names
      GPR8[i]; in 32-bit mode (no REX prefixes exist in this window) the
      byte registers 0..3 are the LOW bytes of GPRs 0..3 and 4..7 are the
      HIGH bytes of GPRs 0..3, so parent(i) = GPR[i & 3] and the bit range
      is [0,8) for i < 4 and [8,16) for i >= 4.

THE FIX (contract section 4; CMO-C1/P2) — two historical defect facets:

  1. Historical writes-set defect: the historical register-direct 0x88
     branch added GPR[rm] unconditionally (the `if mr["rm"] < 4 else`
     conditional was a NO-OP — both arms GPR[mr["rm"]]), filing CH (rm=5)
     under EBP. FIXED: the writes-set now carries the correct parent for
     ALL EIGHT destination aliases (AL/CL/DL/BL/AH/CH/DH/BH -> parents
     EAX/ECX/EDX/EBX/EAX/ECX/EDX/EBX) via the arithmetic helper.
  2. Historical reads-set defect: the register-direct 0x88 byte SOURCE
     parent was never recorded at all (only the src string). FIXED: the
     reads-set now records the byte source's parent in BOTH forms
     (register-direct AND memory), so a CH source reads ECX — never EBP,
     and never nothing.

THREE PROPERTIES distinguished per byte operand (contract section 4):
  1. exact byte-register operand NAME — the dst/src strings (unchanged);
  2. PARENT general-purpose register — the writes/reads sets (fixed);
  3. WIDTH / bit-range actually written or read — width=8; low aliases
     [0,8), high aliases [8,16). A partial-byte write CLOBBERS the parent
     for reaching-definition purposes but is NOT a full 32-bit overwrite;
     recorded via partial_gpr_write / gpr_bits_written, never asserted as
     a 32-bit overwrite.

  Additive per-0x88 fields (my own field names, distinct from the
  production decoder's): op8_dst_name / op8_dst_parent / op8_dst_bits,
  op8_src_name / op8_src_parent / op8_src_bits, partial_gpr_write,
  gpr_bits_written (register form only for the last two pairs).

PRESERVED UNCHANGED from the historical QC decoder: instruction lengths,
ModRM/SIB interpretation, destination/source strings, text rendering,
the supported opcode set (0x50-0x57 push, 0x88, 0x89 incl. 66-prefix
16-bit, 0x8A/0x8B, 0x8D, 0x33, 0x3B-class fail-closed, 0xC7, 0xD9, 0xE8),
fail-closed QcDecodeError on unsupported opcodes. NOT a general x86
emulator/disassembler. This correction does NOT establish
GENERAL_X86_DECODER_CORRECTNESS or GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED.

QC SCAN + QC PROVENANCE GATE (successor of the historical QC
writers_between scan, qc_remeasure.py main() nested def, source lines
497-499; and the same production value-provenance PREDICATE semantics the
executor's clean analysis uses — byte pins at 0x0085B1DA / 0x0085B24B /
0x0085B27A / 0x0085B27F / 0x0085B281, rel32 recomputation of the accessor
call to 0x00746560, the accessor bytes, the EDI and ECX reaching-definition
scans; conclusion CORE_VALUE_SOURCE=[arg1+8] / COPY_FROM_MEMORY). The
gate contains NO hard-coded mutant expectation: identical checks run for
the clean window and for every mutant; a mutant differing from clean ONLY
in the two bytes at 0x0085B24D fails the gate through the ECX
reaching-definition scan alone.

python -B; stdlib only; this module performs NO file I/O and NO writes.
"""
import struct

# ---------------------------------------------------------------- tables
GPR = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
GPR8 = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]
GPR16 = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"]


class QcDecodeError(Exception):
    pass


# ------------------------------------------------- CMO-C1 alias correction
def byte_parent(idx):
    """Parent 32-bit GPR of byte-register index idx (x86-32, no REX).

    Hardware encoding: byte regs 0..3 (al,cl,dl,bl) are the low bytes of
    GPRs 0..3 (eax,ecx,edx,ebx); byte regs 4..7 (ah,ch,dh,bh) are the HIGH
    bytes of the SAME four GPRs. Implemented arithmetically — this is the
    independent successor implementation of the corrected alias mapping
    (NOT a copy of the production BYTE8_PARENT dict).
    """
    return GPR[idx & 3]


def byte_bits(idx):
    """Bit range of byte-register idx within its parent: low [0,8) / high
    [8,16) (x86-32, no REX)."""
    return (8, 16) if idx >= 4 else (0, 8)


# ------------------------------------------------------------ own PE mapper
class QcPE:
    """Minimal fail-closed PE32 section mapper (QC lineage: MyPE successor).

    Whole-range checks; a VA+n request must lie fully inside one section's
    mapped span and inside the physical file.
    """

    def __init__(self, data):
        self.data = data
        if len(data) < 0x40 or data[:2] != b"MZ":
            raise SystemExit("QC FAIL: no MZ")
        e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
        if data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
            raise SystemExit("QC FAIL: no PE sig")
        coff = e_lfanew + 4
        nsec = struct.unpack_from("<H", data, coff + 2)[0]
        opt_size = struct.unpack_from("<H", data, coff + 16)[0]
        opt = coff + 20
        if struct.unpack_from("<H", data, opt)[0] != 0x10B:
            raise SystemExit("QC FAIL: not PE32")
        self.image_base = struct.unpack_from("<I", data, opt + 28)[0]
        self.sections = []
        tbl = opt + opt_size
        for i in range(nsec):
            s = tbl + 40 * i
            vsize = struct.unpack_from("<I", data, s + 8)[0]
            vaddr = struct.unpack_from("<I", data, s + 12)[0]
            rsize = struct.unpack_from("<I", data, s + 16)[0]
            rptr = struct.unpack_from("<I", data, s + 20)[0]
            self.sections.append((vaddr, max(vsize, rsize), rptr))

    def off(self, va, n=1):
        rva = va - self.image_base
        for vaddr, span, rptr in self.sections:
            if vaddr <= rva < vaddr + span:
                fo = rva - vaddr + rptr
                if fo < 0 or fo + n > len(self.data):
                    raise SystemExit(
                        "QC FAIL: range outside file for VA %#x" % va)
                return fo
        raise SystemExit("QC FAIL: VA %#x not in any section" % va)

    def read(self, va, n):
        fo = self.off(va, n)
        return self.data[fo:fo + n]

    def u32(self, va):
        return struct.unpack("<I", self.read(va, 4))[0]


# ------------------------------------------------------------------- ModRM
def my_modrm(buf, i):
    """Decode ModRM at buf[i] (historical QC structure, unchanged)."""
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
        index = (sib >> 3) & 7
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


def _mem_str(mr):
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


# ----------------------------------------------------------------- decoder
def my_decode(buf, off, va):
    """Decode one instruction at buf[off] (file offset off, VA va).

    Historical QC structure, with the CMO-C1 0x88 alias correction applied
    (see module docstring). Fail-closed QcDecodeError on unsupported
    opcodes; controlled failure, never silent acceptance.
    """
    start = off
    b0 = buf[off]
    pre66 = False
    if b0 == 0x66:
        pre66 = True
        off += 1
        b0 = buf[off]
    out = {"va": va, "writes": set(), "reads": set(),
           "width": 16 if pre66 else 32, "is_call": False, "is_jump": False,
           "mem_dst": None, "prefix66": pre66}
    if 0x50 <= b0 <= 0x57:
        out["mnemonic"] = "push"
        out["length"] = off + 1 - start
        out["bytes"] = bytes(buf[start:off + 1])
        out["reads"].add(GPR[b0 - 0x50])
        out["writes"].add("esp")  # implicit (unchanged historical QC fact)
        return out
    if b0 in (0x88, 0x89, 0x8A, 0x8B, 0x8D, 0x33, 0x3B):
        mr = my_modrm(buf, off + 1)
        off += 1 + mr["size"]
        reg32 = GPR[mr["reg"]]
        if b0 == 0x89:      # mov r/m, r (32/16-bit; prefix66 handled)
            if mr["mem"]:
                out["mnemonic"] = "mov"
                out["dst"] = _mem_str(mr)
                out["src"] = GPR16[mr["reg"]] if pre66 else reg32
                if mr["base"] is not None:
                    out["reads"].add(GPR[mr["base"]])
                out["mem_dst"] = {
                    "base": GPR[mr["base"]]
                            if mr["base"] is not None else None,
                    "disp": mr["disp"] or 0}
            else:
                out["mnemonic"] = "mov"
                out["dst"] = GPR16[mr["rm"]] if pre66 else GPR[mr["rm"]]
                out["src"] = GPR16[mr["reg"]] if pre66 else reg32
                out["writes"].add(GPR[mr["rm"]])
                out["reads"].add(GPR[mr["reg"]])
        elif b0 == 0x88:     # mov r/m8, r8 — THE CMO-C1 CORRECTED BRANCH
            out["mnemonic"] = "mov"
            out["width"] = 8
            src_i = mr["reg"]
            dst_i = mr["rm"]
            # three properties of the byte SOURCE (name / parent / bits)
            out["op8_src_name"] = GPR8[src_i]
            out["op8_src_parent"] = byte_parent(src_i)
            out["op8_src_bits"] = list(byte_bits(src_i))
            if mr["mem"]:
                out["dst"] = _mem_str(mr)
                if mr["base"] is not None:
                    out["reads"].add(GPR[mr["base"]])
                out["mem_dst"] = {
                    "base": GPR[mr["base"]]
                            if mr["base"] is not None else None,
                    "disp": mr["disp"] or 0}
                out["partial_gpr_write"] = False
                out["gpr_bits_written"] = None
            else:
                out["dst"] = GPR8[dst_i]
                out["op8_dst_name"] = GPR8[dst_i]
                out["op8_dst_parent"] = byte_parent(dst_i)
                out["op8_dst_bits"] = list(byte_bits(dst_i))
                # FIXED parent attribution for ALL EIGHT destination
                # aliases (historical bug: GPR[rm] unconditionally, with a
                # NO-OP conditional; CH (rm=5) was filed under EBP):
                out["writes"].add(byte_parent(dst_i))
                # partial-byte write: clobbers the parent for
                # reaching-definition purposes, NOT a full 32-bit write:
                out["partial_gpr_write"] = True
                out["gpr_bits_written"] = list(byte_bits(dst_i))
            out["src"] = GPR8[src_i]
            # FIXED byte-SOURCE parent in the reads-set, BOTH forms
            # (historical bug: never recorded at all):
            out["reads"].add(byte_parent(src_i))
        elif b0 == 0x8B:     # mov r, r/m
            out["mnemonic"] = "mov"
            out["dst"] = GPR16[mr["reg"]] if pre66 else reg32
            out["src"] = _mem_str(mr) if mr["mem"] else (
                GPR16[mr["rm"]] if pre66 else GPR[mr["rm"]])
            out["writes"].add(reg32)
            if mr["mem"]:
                if mr["base"] is not None:
                    out["reads"].add(GPR[mr["base"]])
            else:
                out["reads"].add(GPR[mr["rm"]])
        elif b0 == 0x8A:     # mov r8, r/m8 (byte load; symmetric alias fix)
            out["mnemonic"] = "mov"
            out["width"] = 8
            out["dst"] = GPR8[mr["reg"]]
            out["op8_dst_name"] = GPR8[mr["reg"]]
            out["op8_dst_parent"] = byte_parent(mr["reg"])
            out["op8_dst_bits"] = list(byte_bits(mr["reg"]))
            out["writes"].add(byte_parent(mr["reg"]))
            out["partial_gpr_write"] = True
            out["gpr_bits_written"] = list(byte_bits(mr["reg"]))
            if mr["mem"]:
                out["src"] = _mem_str(mr)
                if mr["base"] is not None:
                    out["reads"].add(GPR[mr["base"]])
                out["op8_src_name"] = None
                out["op8_src_parent"] = None
                out["op8_src_bits"] = None
            else:
                out["src"] = GPR8[mr["rm"]]
                out["op8_src_name"] = GPR8[mr["rm"]]
                out["op8_src_parent"] = byte_parent(mr["rm"])
                out["op8_src_bits"] = list(byte_bits(mr["rm"]))
                out["reads"].add(byte_parent(mr["rm"]))
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
            out["mem_dst"] = {
                "base": GPR[mr["base"]]
                        if mr["base"] is not None else None,
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
                raise QcDecodeError("D9 mem reg=%d @%#x" % (mr["reg"], va))
            out["dst"] = _mem_str(mr)
            out["src"] = "st0"
            out["mem_dst"] = {
                "base": GPR[mr["base"]]
                        if mr["base"] is not None else None,
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
    """Linear fail-closed decode of [va_from, va_to) from the PE image."""
    ins = []
    va = va_from
    while va < va_to:
        fo = pe.off(va)
        d = my_decode(pe.data, fo, va)
        d["text"] = ("%s %s, %s" % (d["mnemonic"], d.get("dst", ""),
                                    d.get("src", ""))
                     if d.get("dst") is not None else d["mnemonic"])
        ins.append(d)
        va += d["length"]
    return ins


def hx(b):
    return " ".join("%02X" % c for c in b)


# ------------------------------------------------------- QC scan successor
def writers_between(ins_list, lo_excl, hi_incl, reg):
    """Register-writer scan, historical QC lineage (lo_excl < va <= hi_incl).

    Successor of the historical qc_remeasure.py main() nested def
    writers_between (source lines 497-499), same interval semantics.
    """
    return [i["va"] for i in ins_list
            if lo_excl < i["va"] <= hi_incl and reg in i["writes"]]


def writers_scan(ins_list, reg, lo_excl, hi_excl):
    """Exclusive-upper variant (the executor ECX-scan integer semantics:
    lo_excl < va < hi_excl — over integer VAs equivalent to the historical
    QC call writers_between(lo, hi-1, reg))."""
    return [i["va"] for i in ins_list
            if lo_excl < i["va"] < hi_excl and reg in i["writes"]]


# --------------------------------------------------- QC provenance gate
VALUE_CHAIN_VAS = {
    "edi_def": 0x0085B1DA,        # 8B 7C 24 14  mov edi, [esp+0x14]
    "ecx_def": 0x0085B24B,        # 8B CF         mov ecx, edi
    "accessor_call": 0x0085B27A,  # E8 ...       call 0x00746560
    "value_load": 0x0085B27F,     # 8B 08         mov ecx, [eax]
    "selected_store": 0x0085B281,  # 89 4E 44      mov [esi+0x44], ecx
}
ACCESSOR_VA = 0x00746560
ACCESSOR_HEX = "8D 41 08 C3"


def qc_value_provenance_gate(ins_list, accessor_bytes_hex):
    """The QC value-provenance predicate (same production semantics as the
    clean analysis; NO hard-coded mutant expectation).

    Checks: byte pins at the five chain VAs; the rel32 recomputation of the
    call at 0x0085B27A to 0x00746560; the accessor bytes (passed in from a
    physical read); the EDI reaching definition (0x0085B1DA, 0x0085B24B];
    the ECX reaching definition (0x0085B24B, 0x0085B27A). Conclusion
    CORE_VALUE_SOURCE=[arg1+8] / CONFIRMED_COPY_FROM_MEMORY iff all checks
    hold. Every mutant is evaluated by the IDENTICAL checks.
    """
    by_va = {}
    for i in ins_list:
        by_va.setdefault(i["va"], i)

    def pin(va, expected_hex):
        i = by_va.get(va)
        return i is not None and hx(i["bytes"]) == expected_hex

    edi_clobbers = writers_between(
        ins_list, VALUE_CHAIN_VAS["edi_def"], VALUE_CHAIN_VAS["ecx_def"],
        "edi")
    ecx_clobbers = writers_scan(
        ins_list, "ecx", VALUE_CHAIN_VAS["ecx_def"],
        VALUE_CHAIN_VAS["accessor_call"])

    checks = {
        "pin_0x0085B1DA_8B7C2414":
            pin(VALUE_CHAIN_VAS["edi_def"], "8B 7C 24 14"),
        "pin_0x0085B24B_8BCF":
            pin(VALUE_CHAIN_VAS["ecx_def"], "8B CF"),
        "pin_0x0085B27A_E8E1B2EEFF":
            pin(VALUE_CHAIN_VAS["accessor_call"], "E8 E1 B2 EE FF"),
        "rel32_target_0x00746560": False,
        "accessor_0x00746560_8D4108C3":
            accessor_bytes_hex == ACCESSOR_HEX,
        "pin_0x0085B27F_8B08":
            pin(VALUE_CHAIN_VAS["value_load"], "8B 08"),
        "pin_0x0085B281_894E44":
            pin(VALUE_CHAIN_VAS["selected_store"], "89 4E 44"),
        "edi_reaching_definition_intact": edi_clobbers == [],
        "ecx_reaching_definition_intact": ecx_clobbers == [],
    }
    call_ins = by_va.get(VALUE_CHAIN_VAS["accessor_call"])
    if call_ins is not None and call_ins["bytes"][:1] == b"\xE8":
        rel = struct.unpack("<i", call_ins["bytes"][1:5])[0]
        checks["rel32_target_0x00746560"] = (
            (VALUE_CHAIN_VAS["accessor_call"] + 5 + rel) & 0xffffffff
            == ACCESSOR_VA)

    failure_reasons = []
    if not checks["pin_0x0085B1DA_8B7C2414"]:
        failure_reasons.append("PIN_85B1DA_MISMATCH")
    if not checks["pin_0x0085B24B_8BCF"]:
        failure_reasons.append("PIN_85B24B_MISMATCH")
    if not (checks["pin_0x0085B27A_E8E1B2EEFF"]
            and checks["rel32_target_0x00746560"]):
        failure_reasons.append("ACCESSOR_CALL_PIN_OR_TARGET_MISMATCH")
    if not checks["accessor_0x00746560_8D4108C3"]:
        failure_reasons.append("ACCESSOR_BYTES_MISMATCH")
    if not checks["pin_0x0085B27F_8B08"]:
        failure_reasons.append("PIN_85B27F_MISMATCH")
    if not checks["pin_0x0085B281_894E44"]:
        failure_reasons.append("PIN_85B281_MISMATCH")
    if not checks["edi_reaching_definition_intact"]:
        failure_reasons.append("EDI_REACHING_DEF_BROKEN")
    if not checks["ecx_reaching_definition_intact"]:
        failure_reasons.append("ECX_REACHING_DEF_BROKEN")

    ok = failure_reasons == []
    return {
        "gate": "PASS" if ok else "FAIL",
        "checks": checks,
        "edi_clobber_vas": ["0x%08X" % v for v in edi_clobbers],
        "ecx_clobber_vas": ["0x%08X" % v for v in ecx_clobbers],
        "failure_reasons": failure_reasons,
        "core_value_source": "[arg1+8]" if ok else None,
        "value_provenance": ("CONFIRMED_COPY_FROM_MEMORY" if ok
                             else "BROKEN"),
    }
