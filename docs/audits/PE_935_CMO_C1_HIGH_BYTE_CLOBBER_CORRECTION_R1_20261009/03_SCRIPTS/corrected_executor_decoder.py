#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""corrected_executor_decoder.py — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

Corrected successor of the historical executor decoder of
PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009 (CMO-C1 / P2 fix).

EXPLICIT MAPPING (contract section 3):

  OLD_EXECUTOR_SCRIPT:
    docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/repin_write_provenance.py
    SIZE = 34043
    SHA256 = 45120C91AD6A94A79C56E9B06F1C035481FB99D3017688E7F589732BEC6EE931
    (historical, IMMUTABLE, not edited — its behavior stays documented there)

  CORRECTED_EXECUTOR_SCRIPT:
    docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/03_SCRIPTS/corrected_executor_decoder.py
    (this file; its SIZE/SHA256 are measured and recorded at POST run time in
    00_POST/POST_COUNTEREXAMPLES.json and the run handoff)

  OLD_QC_SCRIPT -> CORRECTED_QC_SCRIPT:
    docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/qc_remeasure.py
    (31970 B / 4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B3E2F2E71B3EB5B3F3F8DDE1A)
    -> 03_SCRIPTS/corrected_qc_decoder.py — WRITTEN BY THE FRESH-QC WORKER
    PHASE, NOT by this executor phase (delegation note; see PREREGISTRATION
    section 6).

THE FIX (contract section 4; CMO-C1/P2):

  Historical defect: in the opcode-0x88 (MOV r/m8, r8) branch, the byte-alias
  index (R8) was used directly as the index into the 32-bit register table
  (REGS) when building the writes/reads sets, so HIGH byte aliases were
  misfiled (CH -> EBP, BH -> EDI, ...) and the low-alias quarter was correct
  only by coincidence. The historical QC decoder additionally never recorded
  the register-direct byte source in its reads-set at all.

  This successor fixes the parent attribution for ALL EIGHT aliases on BOTH
  sides (destination writes-set, source reads-set), in BOTH forms
  (register-direct and memory), and distinguishes THREE properties per byte
  operand:

    1. exact byte-register operand NAME — the dst/src STRINGS, preserved
       unchanged from the historical decoder;
    2. PARENT general-purpose register — the writes/reads GPR sets (the
       convention the reaching-definition clobber scans consume):
         AL->EAX  CL->ECX  DL->EDX  BL->EBX
         AH->EAX  CH->ECX  DH->EDX  BH->EBX
    3. WIDTH / bit-range actually written or read — width=8; low aliases
       [0,8), high aliases [8,16). A partial-byte write CLOBBERS the parent
       register for reaching-definition purposes but is NOT a full 32-bit
       overwrite; that distinction is preserved explicitly via width /
       byte bit-range / partial-write fields, never by asserting a 32-bit
       overwrite.

  New per-0x88-instruction fields (ADDITIVE; no historical field is removed
  or renamed): byte_src, byte_src_parent, byte_src_bits; byte_dst,
  byte_dst_parent, byte_dst_bits (register form); partial_gpr_write and
  gpr_write_bits (register form only).

PRESERVED UNCHANGED (contract section 4): instruction lengths; ModRM/SIB
interpretation; destination and source strings; text rendering; all other
supported opcode behavior (0x50-0x57 push, 0x89 incl. 66-prefix 16-bit,
0x8B, 0x8D, 0x33, 0xC7, 0xD9, 0xE8); fail-closed DecodeError on any
unsupported opcode. An unsupported instruction encountered in a required
control produces a CONTROLLED failure result (the caller records the
DecodeError class/message/VA and preserves evidence) — never a silent
acceptance.

NOT a general x86 emulator/disassembler: the decoder remains a bounded
window decoder, table-driven for this window's opcode set. This correction
does NOT establish GENERAL_X86_DECODER_CORRECTNESS or
GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED.

SUCCESSOR SCAN + PROVENANCE MACHINERY (same lineage, corrected):

  scan_writers_interval() — successor of the historical executor ECX-writers
  comprehension (repin_write_provenance.py main(), source lines 444-446);
  generalized to (reg, lo_excl, hi_excl[, hi_inclusive]) with identical
  interval semantics (lo_excl < va < hi_excl; hi_inclusive reproduces the
  historical half-closed EDI/ESI scan upper bounds).

  value_provenance_gate() — the SAME production provenance predicate used for
  the clean analysis: byte pins at 0x0085B1DA / 0x0085B24B / 0x0085B27A /
  0x0085B27F / 0x0085B281, the rel32 recomputation of the accessor call,
  the accessor bytes, the EDI reaching-definition scan and the ECX
  reaching-definition scan; conclusion CORE_VALUE_SOURCE=[arg1+8]
  (COPY_FROM_MEMORY). The gate contains NO hard-coded mutant expectation:
  the clean window and every mutant are evaluated by the identical checks; a
  mutant that differs from clean ONLY in the two bytes at 0x0085B24D fails
  the gate through the ECX reaching-definition scan alone.

python -B; stdlib only; this module performs NO file I/O and NO writes.
"""
import struct

REGS = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
R8 = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]
R16 = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"]

# --- CMO-C1 correction: byte-register alias parents (contract section 4) ----
BYTE8_PARENT = {
    "al": "eax", "cl": "ecx", "dl": "edx", "bl": "ebx",
    "ah": "eax", "ch": "ecx", "dh": "edx", "bh": "ebx",
}
BYTE8_BIT_RANGE = {
    "al": (0, 8), "cl": (0, 8), "dl": (0, 8), "bl": (0, 8),
    "ah": (8, 16), "ch": (8, 16), "dh": (8, 16), "bh": (8, 16),
}


class DecodeError(Exception):
    pass


def _modrm(buf, i):
    """Decode ModRM at buf[i]. Returns dict with size advanced by caller."""
    m = buf[i]
    mod = (m >> 6) & 3
    reg = (m >> 3) & 7
    rm = m & 7
    n = 1
    base = None
    disp = None
    mem = mod != 3
    if mem:
        if rm == 4:  # SIB byte follows
            n += 1
            s = buf[i + 1]
            bas = s & 7
            idx = (s >> 3) & 7
            if mod == 0 and bas == 5:
                disp = ("disp32", struct.unpack_from("<I", buf, i + 2)[0])
                n += 4
            else:
                base = REGS[bas]
                if mod == 1:
                    disp = ("disp8", struct.unpack_from("<b", buf, i + 2)[0])
                    n += 1
                elif mod == 2:
                    disp = ("disp32", struct.unpack_from("<i", buf, i + 2)[0])
                    n += 4
        elif mod == 0 and rm == 5:
            disp = ("disp32", struct.unpack_from("<I", buf, i + 1)[0])
            n += 4
        else:
            base = REGS[rm]
            if mod == 1:
                disp = ("disp8", struct.unpack_from("<b", buf, i + 1)[0])
                n += 1
            elif mod == 2:
                disp = ("disp32", struct.unpack_from("<i", buf, i + 1)[0])
                n += 4
    return {"mod": mod, "reg": reg, "rm": rm, "size": n,
            "base": base, "disp": disp, "mem": mem}


def _fmt_mem(base, disp):
    if base is None and disp is None:
        return "[??]"
    if base is None:
        return "[0x%08x]" % (disp[1] & 0xffffffff)
    if disp is None:
        return "[%s]" % base
    d = disp[1]
    if d >= 0:
        return "[%s+0x%x]" % (base, d)
    return "[%s-0x%x]" % (base, -d)


def decode_instruction(buf, off, va):
    """Decode one instruction at buf[off] (window-relative off, VA va).

    Returns dict: va, length, bytes, text, writes/reads (parent-GPR name
    sets), dst, src, width, mnemonic, mem_dst, call_target — plus, for opcode
    0x88 only, the additive byte-alias fields (see module docstring).
    """
    start = off
    b0 = buf[off]
    prefix66 = False
    if b0 == 0x66:
        prefix66 = True
        off += 1
        b0 = buf[off]
    ins = {"va": va, "length": None, "bytes": None, "text": None,
           "writes": set(), "reads": set(), "dst": None, "src": None,
           "width": 16 if prefix66 else 32, "mnemonic": None,
           "mem_dst": None, "call_target": None, "prefix66": prefix66}

    if 0x50 <= b0 <= 0x57:
        off += 1
        ins["mnemonic"] = "push"
        ins["text"] = "push %s" % REGS[b0 - 0x50]
        ins["reads"].add(REGS[b0 - 0x50])
    elif b0 in (0x88, 0x89, 0x8B, 0x8D, 0x33):
        mr = _modrm(buf, off + 1)
        off += 1 + mr["size"]
        if b0 == 0x88:
            regname = R8[mr["reg"]]
            width = 8
        elif b0 == 0x89 and prefix66:
            regname = R16[mr["reg"]]
            width = 16
        else:
            regname = REGS[mr["reg"]]
            width = 32 if not prefix66 else 16
        if b0 == 0x89:
            ins["mnemonic"] = "mov"
            ins["dst"] = _fmt_mem(mr["base"], mr["disp"]) if mr["mem"] \
                else REGS[mr["rm"]]
            ins["src"] = regname
            if mr["mem"]:
                ins["mem_dst"] = {
                    "base": mr["base"],
                    "disp": mr["disp"][1] if mr["disp"] else 0,
                    "disp_kind": mr["disp"][0] if mr["disp"] else None}
                if mr["base"]:
                    ins["reads"].add(mr["base"])
            else:
                ins["writes"].add(REGS[mr["rm"]])
            ins["reads"].add(REGS[mr["reg"]])
        elif b0 == 0x88:
            # --- CMO-C1 corrected 0x88 (MOV r/m8, r8) ------------------------
            ins["mnemonic"] = "mov"
            ins["dst"] = _fmt_mem(mr["base"], mr["disp"]) if mr["mem"] \
                else R8[mr["rm"]]
            ins["src"] = regname
            # byte-alias operand metadata (additive; three properties:
            # exact name, parent, bit-range)
            src8 = R8[mr["reg"]]
            ins["byte_src"] = src8
            ins["byte_src_parent"] = BYTE8_PARENT[src8]
            ins["byte_src_bits"] = list(BYTE8_BIT_RANGE[src8])
            if mr["mem"]:
                ins["mem_dst"] = {
                    "base": mr["base"],
                    "disp": mr["disp"][1] if mr["disp"] else 0,
                    "disp_kind": mr["disp"][0] if mr["disp"] else None}
                if mr["base"]:
                    ins["reads"].add(mr["base"])
                ins["partial_gpr_write"] = False
                ins["gpr_write_bits"] = None
            else:
                dst8 = R8[mr["rm"]]
                ins["byte_dst"] = dst8
                ins["byte_dst_parent"] = BYTE8_PARENT[dst8]
                ins["byte_dst_bits"] = list(BYTE8_BIT_RANGE[dst8])
                # FIXED parent attribution for ALL EIGHT aliases (the
                # historical bug: writes.add(REGS[mr["rm"]]) — for rm=5 (CH)
                # this filed the write under EBP instead of ECX)
                ins["writes"].add(BYTE8_PARENT[dst8])
                # a partial-byte write CLOBBERS the parent for
                # reaching-definition purposes but is NOT a full 32-bit
                # overwrite — recorded explicitly:
                ins["partial_gpr_write"] = True
                ins["gpr_write_bits"] = list(BYTE8_BIT_RANGE[dst8])
            # FIXED source reads parent (the historical bug:
            # reads.add(REGS[mr["reg"]]) — a CH source was filed as reading
            # EBP); both forms record the byte source's PARENT:
            ins["reads"].add(BYTE8_PARENT[src8])
        elif b0 == 0x8B:
            ins["mnemonic"] = "mov"
            ins["dst"] = REGS[mr["reg"]]
            ins["src"] = _fmt_mem(mr["base"], mr["disp"]) if mr["mem"] \
                else REGS[mr["rm"]]
            ins["writes"].add(REGS[mr["reg"]])
            if mr["mem"] and mr["base"]:
                ins["reads"].add(mr["base"])
            if not mr["mem"]:
                ins["reads"].add(REGS[mr["rm"]])
        elif b0 == 0x8D:
            ins["mnemonic"] = "lea"
            ins["dst"] = REGS[mr["reg"]]
            ins["src"] = _fmt_mem(mr["base"], mr["disp"])
            ins["writes"].add(REGS[mr["reg"]])
            if mr["base"]:
                ins["reads"].add(mr["base"])
        else:  # 0x33
            ins["mnemonic"] = "xor"
            ins["dst"] = REGS[mr["reg"]]
            ins["src"] = _fmt_mem(mr["base"], mr["disp"]) if mr["mem"] \
                else REGS[mr["rm"]]
            ins["writes"].add(REGS[mr["reg"]])
            if not mr["mem"]:
                ins["reads"].add(REGS[mr["rm"]])
        ins["width"] = width
        ins["text"] = "%s %s, %s" % (ins["mnemonic"], ins["dst"], ins["src"])
    elif b0 == 0xC7:
        mr = _modrm(buf, off + 1)
        if mr["reg"] != 0:
            raise DecodeError("C7 reg!=0 unsupported @%#x" % va)
        off += 1 + mr["size"]
        imm = struct.unpack_from("<I", buf, off)[0]
        off += 4
        ins["mnemonic"] = "mov"
        ins["dst"] = _fmt_mem(mr["base"], mr["disp"]) if mr["mem"] \
            else REGS[mr["rm"]]
        ins["src"] = "0x%08x" % imm
        ins["imm32"] = imm
        if mr["mem"]:
            ins["mem_dst"] = {
                "base": mr["base"],
                "disp": mr["disp"][1] if mr["disp"] else 0,
                "disp_kind": mr["disp"][0] if mr["disp"] else None}
            if mr["base"]:
                ins["reads"].add(mr["base"])
        else:
            ins["writes"].add(REGS[mr["rm"]])
        ins["text"] = "mov %s, 0x%08x" % (ins["dst"], imm)
    elif b0 == 0xD9:
        nxt = buf[off + 1]
        if ((nxt >> 6) & 3) == 3:  # register form (x87 stack)
            if nxt == 0xEE:
                off += 2
                ins["mnemonic"] = "fldz"
                ins["text"] = "fldz"
            elif nxt == 0xE8:
                off += 2
                ins["mnemonic"] = "fld1"
                ins["text"] = "fld1"
            else:
                raise DecodeError("D9 mod3 unsupported @%#x" % va)
        else:
            mr = _modrm(buf, off + 1)
            if mr["reg"] == 2:
                ins["mnemonic"] = "fst"
            elif mr["reg"] == 3:
                ins["mnemonic"] = "fstp"
            else:
                raise DecodeError("D9 mem reg!=2/3 unsupported @%#x" % va)
            off += 1 + mr["size"]
            ins["dst"] = _fmt_mem(mr["base"], mr["disp"])
            ins["src"] = "st0"
            ins["mem_dst"] = {
                "base": mr["base"],
                "disp": mr["disp"][1] if mr["disp"] else 0,
                "disp_kind": mr["disp"][0] if mr["disp"] else None}
            if mr["base"]:
                ins["reads"].add(mr["base"])
            ins["text"] = "%s %s" % (ins["mnemonic"], ins["dst"])
    elif b0 == 0xE8:
        rel = struct.unpack_from("<i", buf, off + 1)[0]
        off += 5
        ins["mnemonic"] = "call"
        ins["call_target"] = (va + 5 + rel) & 0xffffffff
        ins["text"] = "call 0x%08x" % ins["call_target"]
    else:
        raise DecodeError("unsupported opcode %#04x @%#x" % (b0, va))

    ins["length"] = off - start
    ins["bytes"] = bytes(buf[start:off])
    return ins


def linear_decode_window(win_bytes, win_start_va, decode_from, decode_to):
    """Linear fail-closed decode of [decode_from, decode_to)."""
    out = []
    va = decode_from
    while va < decode_to:
        off = va - win_start_va
        ins = decode_instruction(win_bytes, off, va)
        out.append(ins)
        va += ins["length"]
    return out


def hexs(b):
    return " ".join("%02X" % c for c in b)


# ---------------------------------------------------------------------------
# successor scan + production provenance gate (lineage: repin_write_provenance
# main() lines 444-455; corrected successor, same interval semantics)
# ---------------------------------------------------------------------------
def scan_writers_interval(ins_list, reg, lo_excl, hi_excl,
                          hi_inclusive=False):
    """Register-writer scan between two VAs (reaching-definition guard).

    Lineage: the historical executor ECX scan
        [i["va"] for i in ins_list
         if 0x0085B24B < i["va"] < 0x0085B27A and "ecx" in i["writes"]]
    (main() source lines 444-446) — generalized; identical interval
    semantics: lo_excl < va < hi_excl, or lo_excl < va <= hi_excl when
    hi_inclusive=True (the historical EDI/ESI scan upper bounds).
    """
    if hi_inclusive:
        return [i["va"] for i in ins_list
                if lo_excl < i["va"] <= hi_excl and reg in i["writes"]]
    return [i["va"] for i in ins_list
            if lo_excl < i["va"] < hi_excl and reg in i["writes"]]


VALUE_CHAIN_VAS = {
    "edi_def": 0x0085B1DA,    # 8B 7C 24 14  mov edi, [esp+0x14]  (EDI := arg1)
    "ecx_def": 0x0085B24B,    # 8B CF         mov ecx, edi          (ECX := arg1)
    "accessor_call": 0x0085B27A,  # E8 E1 B2 EE FF  call 0x00746560
    "value_load": 0x0085B27F,     # 8B 08  mov ecx, [eax]  (stored value)
    "selected_store": 0x0085B281,  # 89 4E 44  mov [esi+0x44], ecx
}
ACCESSOR_VA = 0x00746560
ACCESSOR_BYTES = b"\x8D\x41\x08\xC3"  # lea eax, [ecx+8]; ret


def value_provenance_gate(ins_list, accessor_bytes):
    """The production value-provenance predicate (clean AND mutants alike).

    Derives the immediate value source of the selected store from the decoded
    window: EDI := [esp+0x14] (arg1) @0x0085B1DA; ECX := EDI @0x0085B24B;
    call 0x00746560 @0x0085B27A (rel32 recomputed from the instruction bytes);
    accessor lea eax,[ecx+8]; ret (returns arg1+8); mov ecx,[eax] @0x0085B27F
    (VALUE_PRODUCER); store [esi+0x44] @0x0085B281. The chain is intact iff the
    EDI and ECX reaching definitions are unbroken between their definitions
    and their uses.

    NO hard-coded mutant expectation exists in this predicate: identical
    checks run for the clean window and for any mutant; a mutant differing
    from clean ONLY in the bytes at 0x0085B24D fails exclusively through the
    ECX reaching-definition scan (every pin, the rel32 recomputation and the
    accessor check still pass) — that asymmetry is the causal proof.
    """
    by_va = {}
    for i in ins_list:
        by_va.setdefault(i["va"], i)

    def pin(va, expected_hex):
        i = by_va.get(va)
        return i is not None and hexs(i["bytes"]) == expected_hex

    edi_clobbers = scan_writers_interval(
        ins_list, "edi", VALUE_CHAIN_VAS["edi_def"],
        VALUE_CHAIN_VAS["ecx_def"], hi_inclusive=True)
    ecx_clobbers = scan_writers_interval(
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
            hexs(accessor_bytes) == "8D 41 08 C3",
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
