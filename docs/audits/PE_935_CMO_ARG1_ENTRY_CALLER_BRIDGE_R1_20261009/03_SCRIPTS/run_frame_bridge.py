#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bounded decoder-assisted symbolic replay for one static argument-provenance question.

RUN_ID   : PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009
Contract : OPENCODE_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_REVISED_20261009.md
          (23187 B, SHA256 773C1310A2CB02B365068EE2D9C684A97765E4D416E30B415B8672D8CC09FF07)

Scope (contract section 4):
  Window A = [0x00528E50, 0x00528E92)  66 bytes  raw offset 1216080 (0x128E50)
  Window B = [0x004C4792, 0x004C47C6)  52 bytes  raw offset  804754 (0x0C4792)
  UNIQUE_ORIGINAL_CODE_BYTES_ANALYZED_MAX = 118 (A 66 + B 52)
  TARGET_CALLSITES = {0x004C47C1, 0x00528E8D}
  INCIDENTAL_OPAQUE_CALLSITE = 0x004C4797 -> 0x0095D3C4 (opaque; no body)
  0 complete function bodies opened; 0 callee bodies; no upstream beyond window B;
  no xref census; no runtime/network/model/VFS work.

Method (contract section 4): WSL GNU objdump is the ONLY x86 decoder in this run.
This script
  1) consumes objdump raw text output (never a handwritten listing),
  2) performs a bounded symbolic replay of the decoded stream,
  3) fails closed: any instruction shape outside the preregistered table, any decode
     gap/overlap, any call-target disagreement (objdump vs byte-level rel32
     recompute) or any unresolved alias makes the affected case UNRESOLVED.
     Expected results are never filled in.

Recorded assumptions (never silently applied):
  AS1 32-bit x86 stack semantics: push = ESP-=4 then store; call = ESP-=4 then
     store the return address.
  AS2 cdecl-style argument order: the LAST push before CALL occupies the first
     stack argument slot at callee entry ([ESP_at_entry+4]); the thiscall receiver
     ECX is a separate channel.
  AS3 opaque callee 0x0095D3C4 normal ABI-compatible return condition: it pops
     exactly its return address (ESP restored to the pre-call value) and conveys a
     return value in EAX. NOT verified by opening the body (it stays opaque); if
     unsupported the Phase-B result stays conditional/unresolved.
  AS4 the FS segment base (TIB) does not alias the live argument stack region: the
     FS:[0] chain-head store at 0x00528E70 writes the TIB, not the stack; the TIB
     resides at the top of the thread stack region, above any frame that passes
     arguments. Runtime FS base is not statically resolvable; recorded as an
     assumption with remaining uncertainty.
  AS5 window A is examined as a straight-line path from the entry 0x00528E50 (no
     branch exists inside window A); window B is qualified ONLY on the EAX!=0
     branch (the EAX==0 branch exits the window at 0x004C47C8, outside, unopened).

Synthetic control fixtures are byte-mutated copies in an OS temp dir OUTSIDE the
repository; the EXE is read-only and never altered. Identity hashes qualify
ORIGINAL inputs only and never reject synthetic controls before analysis.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------- pinned inputs

RUN_ID = "PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009"

EXE_PATH = "/mnt/d/Eudoria_Reconstruction/pcg_install/Entropia.exe"
EXE_SIZE = 8015872
EXE_SHA256 = "e7785430e81dffe648ce8f5312414b17bc9fce61389689a22f753765d5280f31"
IMAGE_BASE = 0x400000

WINDOWS = {
    "A": {
        "va_start": 0x00528E50,
        "size": 66,
        "raw_offset": 1216080,
        "sha256": "f8735567340cd3be2f6b64b4bbc2be292487e97b6184758ca408e6ff1ce78e85",
        "raw_text": "01_RAW/WINDOW_A_OBJDUMP.txt",
    },
    "B": {
        "va_start": 0x004C4792,
        "size": 52,
        "raw_offset": 804754,
        "sha256": "b59e16dc116f4ce0438a1e92bc6b2cbc33fab0b19fabc24cb3a29c911c1efb6a",
        "raw_text": "01_RAW/WINDOW_B_OBJDUMP.txt",
    },
}

OPAQUE_CALLEE = 0x95D3C4       # incidental opaque callsite 0x004C4797 -> 0x0095D3C4
BRIDGE_CALLEE = 0x528E50       # CALL 0x004C47C1 -> 0x00528E50 (window A entry)
TAIL_CALLEE = 0x85B1B0         # CALL 0x00528E8D -> 0x0085B1B0 (prior-pinned, not opened)

PIVOT_S_VA = 0x528E76          # S = ESP at this VA (Phase A pivot)
PIVOT_T_VA = 0x4C47AF          # T = ESP at this VA (Phase B pivot)
BRIDGE_CALL_VA = 0x4C47C1
TAIL_CALL_VA = 0x528E8D
SOURCE_LOAD_VA = 0x528E84
LEA_VA = 0x4C47BA

# contract section 7 mutation table (synthetic copies only; never the EXE)
MUTATIONS = {
    "M1_A_FRAME": {
        "window": "A", "va": 0x528E5E,
        "orig": "83 ec 1c", "new": "83 ec 18",
        "change": "sub esp,0x1c -> sub esp,0x18",
    },
    "M2_A_SLOT": {
        "window": "A", "va": 0x528E84,
        "orig": "8b 7c 24 3c", "new": "8b 7c 24 38",
        "change": "mov edi,[esp+0x3c] -> mov edi,[esp+0x38]",
    },
    "M3_B_LEA_DISP": {
        "window": "B", "va": 0x4C47BA,
        "orig": "8d 4c 24 14", "new": "8d 4c 24 18",
        "change": "lea ecx,[esp+0x14] -> lea ecx,[esp+0x18]",
    },
    "M4_B_LAST_PUSH": {
        "window": "B", "va": 0x4C47BE,
        "orig": "51", "new": "52",
        "change": "push ecx -> push edx",
    },
    "M5_B_EARLY_PUSH_ORDER": {
        "window": "B", "va": 0x4C47B7,
        "orig": "51 52", "new": "52 51",
        "change": "push ecx; push edx -> push edx; push ecx",
    },
    "M6_B_SKIP": {
        "window": "B", "va": 0x4C47AD,
        "orig": "74 19", "new": "eb 19",
        "change": "je 0x4c47c8 -> jmp 0x4c47c8",
    },
    "M7_B_RECEIVER_ONLY": {
        "window": "B", "va": 0x4C47BF,
        "orig": "8b c8", "new": "8b ce",
        "change": "mov ecx,eax -> mov ecx,esi",
    },
    "M8_B_WRONG_TARGET": {
        "window": "B", "va": 0x4C47C1,
        "orig": "e8 8a 46 06 00", "new": "e8 8b 46 06 00",
        "change": "call 0x528e50 -> call 0x528e51 (rel32 +1)",
    },
    "M9_B_LEA_TO_MOV": {
        "window": "B", "va": 0x4C47BA,
        "orig": "8d 4c 24 14", "new": "8b 4c 24 14",
        "change": "lea ecx,[esp+0x14] -> mov ecx,[esp+0x14]",
    },
}

CASE_ORDER = [
    "A_CLEAN", "B_CLEAN_NONNULL", "B_CLEAN_NULL",
    "M1_A_FRAME", "M2_A_SLOT", "M3_B_LEA_DISP", "M4_B_LAST_PUSH",
    "M5_B_EARLY_PUSH_ORDER", "M6_B_SKIP", "M7_B_RECEIVER_ONLY",
    "M8_B_WRONG_TARGET", "M9_B_LEA_TO_MOV",
]

# expected discriminating results (contract section 7 table)
EXPECTED = {
    "A_CLEAN": {
        "text": "S=E-0x38; source [E+4]; value preserved/delivered",
        "facts": {"S_delta": -0x38, "source_slot_delta": 4,
                  "entry_slot_value_preserved": True, "edi_preserved": True,
                  "tail_target": "0x0085B1B0", "arg1_kind": "STACK_READ"},
    },
    "B_CLEAN_NONNULL": {
        "text": "CALL reachable; arg1 ADDRESS(T+8); receiver = return value",
        "facts": {"T_delta": 0, "flags_preserved_test_to_je": True,
                  "nonnull_reaches_call": True, "arg1_kind": "ADDRESS",
                  "arg1_expr": "ADDRESS(T+0x8)", "receiver_kind": "OPAQUE_RET",
                  "bridge_target": "0x00528E50"},
    },
    "B_CLEAN_NULL": {
        "text": "JE taken; target CALL not reached; no fabricated delivery",
        "facts": {"null_je_taken": True, "null_call_reached": False},
    },
    "M1_A_FRAME": {
        "text": "S=E-0x34; later source [E+8], not entry arg1 [E+4]",
        "facts": {"S_delta": -0x34, "source_slot_delta": 8},
    },
    "M2_A_SLOT": {
        "text": "Source [E] under original frame, not [E+4]",
        "facts": {"S_delta": -0x38, "source_slot_delta": 0},
    },
    "M3_B_LEA_DISP": {
        "text": "arg1 ADDRESS(T+0xC), not ADDRESS(T+8)",
        "facts": {"arg1_kind": "ADDRESS", "arg1_expr": "ADDRESS(T+0xc)"},
    },
    "M4_B_LAST_PUSH": {
        "text": "arg1 is the earlier EDX load value MEM(T+0x4C), not the LEA address",
        "facts": {"arg1_kind": "STACK_READ", "arg1_expr": "MEM(T+0x4c)"},
    },
    "M5_B_EARLY_PUSH_ORDER": {
        "text": "Earlier argument order changes; final arg1 ADDRESS(T+8) and its slot remain unchanged",
        "facts": {"arg1_kind": "ADDRESS", "arg1_expr": "ADDRESS(T+0x8)",
                  "arg1_slot_delta": -0x10, "arg3_expr": "MEM(T+0x50)",
                  "arg4_expr": "MEM(T+0x4c)"},
    },
    "M6_B_SKIP": {
        "text": "Unconditional exit; no delivery at the target CALL",
        "facts": {"nonnull_reaches_call": False,
                  "unconditional_exit": True},
    },
    "M7_B_RECEIVER_ONLY": {
        "text": "Receiver becomes the T-point ESI; already pushed arg1 and its slot remain unchanged",
        "facts": {"arg1_kind": "ADDRESS", "arg1_expr": "ADDRESS(T+0x8)",
                  "arg1_slot_delta": -0x10, "receiver_kind": "UNKNOWN_REG",
                  "receiver_expr": "ESI_UNKNOWN_T"},
    },
    "M8_B_WRONG_TARGET": {
        "text": "Actual target 0x00528E51; no valid bridge to entry 0x00528E50; wrong target NOT followed",
        "facts": {"bridge_target_actual": "0x00528E51", "bridge_valid": False},
    },
    "M9_B_LEA_TO_MOV": {
        "text": "arg1 MEM(T+8), not ADDRESS(T+8); no pointee interpretation",
        "facts": {"arg1_kind": "STACK_READ", "arg1_expr": "MEM(T+0x8)"},
    },
}


class Unresolved(Exception):
    """Fail-closed marker: an unsupported shape, alias or decode problem."""


# ---------------------------------------------------------------- small helpers

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def esp_expr(base, delta):
    if delta == 0:
        return base
    return "%s%s0x%x" % (base, "-" if delta < 0 else "+", abs(delta))


def slot_expr(base, delta):
    return "[%s]" % esp_expr(base, delta)


def va_str(v):
    return "0x%08X" % v


def read_exe_window(exe_path, win):
    with open(exe_path, "rb") as fh:
        fh.seek(win["raw_offset"])
        data = fh.read(win["size"])
    if len(data) != win["size"]:
        raise Unresolved("short read at raw offset %d" % win["raw_offset"])
    return data


# ---------------------------------------------------------------- objdump tool

def objdump_version():
    p = subprocess.run(["objdump", "--version"], capture_output=True, text=True)
    first = p.stdout.splitlines()[0].strip() if p.stdout else ""
    return first, p.returncode


def run_objdump(fixture_path, vma):
    """Run WSL GNU objdump in raw-binary i386 intel mode. Returns (rc, stdout)."""
    cmd = ["objdump", "-D", "-b", "binary", "-m", "i386", "-M", "intel",
           "--adjust-vma=" + hex(vma), fixture_path]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, " ".join(cmd)


INSTR_RE = re.compile(r"^\s*([0-9a-f]+):\s*(.*)$")


class Instr(object):
    __slots__ = ("va", "nbytes", "bytes_hex", "mnemonic", "operands", "text")

    def __init__(self, va, bytes_hex, text):
        self.va = va
        self.bytes_hex = bytes_hex          # list of hex byte strings
        self.nbytes = len(bytes_hex)
        self.text = text                    # full mnemonic + operands string
        parts = text.split(None, 1)
        self.mnemonic = parts[0]
        self.operands = parts[1] if len(parts) > 1 else ""


def parse_objdump(raw_text, va_start, va_end):
    """Parse objdump raw output into a contiguous, exactly-covering instruction
    list for [va_start, va_end).  Raises Unresolved on any gap/overlap anomaly."""
    instrs = []
    pending = None
    for line in raw_text.splitlines():
        m = INSTR_RE.match(line)
        if not m:
            continue
        addr = int(m.group(1), 16)
        rest = m.group(2)
        fields = rest.split("\t")
        fields = [f for f in fields]
        if len(fields) >= 2 and fields[-1].strip():
            # instruction line: bytes field + mnemonic/operands field(s)
            bytestr = "\t".join(fields[:-1]).strip()
            text = fields[-1].strip()
            if bytestr:
                blist = bytestr.split()
                if not all(re.match(r"^[0-9a-f]{2}$", b) for b in blist):
                    continue  # header line like "00528e50 <.data>:" (no bytes)
                instrs.append(Instr(addr, blist, text))
                pending = instrs[-1]
        else:
            # continuation line: extra bytes of the previous instruction
            blist = rest.split()
            if pending is not None and all(re.match(r"^[0-9a-f]{2}$", b) for b in blist):
                pending.bytes_hex.extend(blist)
                pending.nbytes = len(pending.bytes_hex)
    if not instrs:
        raise Unresolved("no instructions decoded in window")
    if instrs[0].va != va_start:
        raise Unresolved("first decoded VA 0x%X != window start" % instrs[0].va)
    for i in range(len(instrs) - 1):
        if instrs[i].va + instrs[i].nbytes != instrs[i + 1].va:
            raise Unresolved("decode gap/overlap at 0x%X" % instrs[i].va)
    last = instrs[-1]
    if last.va + last.nbytes != va_end:
        raise Unresolved("decode ends at 0x%X, window end is 0x%X"
                         % (last.va + last.nbytes, va_end))
    return instrs


# ---------------------------------------------------------------- symbolic values
# A SymVal is a bounded symbolic value with a machine-checkable kind and a
# human-readable expression. Kinds used in this run:
#   IMM            immediate constant
#   UNKNOWN_REG    initial register value at window entry (opaque)
#   ENTRY_RECEIVER ECX at window-A entry (the thiscall receiver, opaque)
#   FS0            previous FS:[0] value (opaque)
#   COOKIE_LOAD    opaque moffs load (the security cookie)
#   COOKIE_XOR_ESP cookie value combined with ESP (opaque value change)
#   ADDR           address COMPUTED by LEA (never a memory read)
#   STACK_READ     value read from a stack slot (in-window write or caller area)
#   OPAQUE_RET     return value of the opaque callee 0x0095D3C4
#   ESI_UNKNOWN    ESI at window-B entry (unknown T-point producer)

class SymVal(object):
    __slots__ = ("kind", "expr", "delta", "provenance")

    def __init__(self, kind, expr, delta=None, provenance=None):
        self.kind = kind
        self.expr = expr
        self.delta = delta            # meaningful for ADDR / STACK_READ
        self.provenance = provenance  # e.g. "in_window@0x004C47BE"

    def to_json(self):
        return {"kind": self.kind, "expr": self.expr,
                "delta": self.delta, "provenance": self.provenance}


class State(object):
    """Symbolic machine state of one replay path, relative to a base symbol."""

    def __init__(self, base_symbol, entry_receiver=False, unknown_suffix="ENTRY"):
        self.base = base_symbol
        self.esp_delta = 0
        self.regs = {}
        for r in ("eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp"):
            if r == "esp":
                self.regs[r] = SymVal("UNKNOWN_REG", "ESP_TRACKED_SEPARATELY")
                continue
            self.regs[r] = SymVal("UNKNOWN_REG", r.upper() + "_" + unknown_suffix)
        if entry_receiver:
            self.regs["ecx"] = SymVal("ENTRY_RECEIVER", "ECX_ENTRY")
        self.mem = {}                 # delta -> (SymVal, written_at_va)
        self.writes = []              # (va, kind, delta, value)
        self.segment_writes = []      # (va, segment, offset, value)
        self.reads = []               # (va, delta, value, provenance)
        self.steps = []               # per-instruction ledger records
        self.reg_writes = []          # (va, reg, value) at-write-time snapshots
        self.flags = None            # {"zf": ..., "set_by": va}
        self.flag_writers = []       # (va, mnemonic) of flag-writing instructions
        self.reg_defs = {}            # reg -> (va, value) latest definition

    def clone(self):
        import copy
        st = State.__new__(State)
        st.base = self.base
        st.esp_delta = self.esp_delta
        st.regs = dict(self.regs)
        st.mem = dict(self.mem)
        st.writes = list(self.writes)
        st.segment_writes = list(self.segment_writes)
        st.reads = list(self.reads)
        st.steps = list(self.steps)
        st.reg_writes = list(self.reg_writes)
        st.flags = dict(self.flags) if self.flags else None
        st.flag_writers = list(self.flag_writers)
        st.reg_defs = dict(self.reg_defs)
        return st

    def set_reg(self, va, reg, val):
        self.regs[reg] = val
        self.reg_defs[reg] = (va, val)
        self.reg_writes.append((va, reg, val))

    def read_slot(self, va, delta):
        if delta in self.mem:
            val, wva = self.mem[delta]
            prov = "in_window@" + va_str(wva)
        else:
            val = SymVal("STACK_READ", slot_expr(self.base, delta),
                         delta=delta, provenance="caller_area_unknown")
            prov = "caller_area_unknown"
        self.reads.append((va, delta, val, prov))
        return val, prov

    def write_slot(self, va, kind, delta, value):
        self.mem[delta] = (value, va)
        self.writes.append((va, kind, delta, value))


# operand grammars (bounded to the shapes occurring in the two windows).
# objdump intel syntax prints "DWORD PTR [esp+0x3c]" for 32-bit MOV memory
# operands but bare "[esp+0x2c]" for LEA, so the size prefix is optional.
MEM_RE = re.compile(r"^(?:DWORD PTR )?\[esp([+-]0x[0-9a-f]+)?\]$")
SEG_RE = re.compile(r"^(fs|gs|ds|cs|es|ss):(0x[0-9a-f]+)$")
HEX_RE = re.compile(r"^0x[0-9a-f]+$")


def parse_disp(opstr):
    m = MEM_RE.match(opstr)
    if not m:
        raise Unresolved("unsupported memory operand: " + opstr)
    if m.group(1) is None:
        return 0
    return int(m.group(1), 16)


def split_operands(operands):
    return [o.strip() for o in operands.split(",")]


# ---------------------------------------------------------------- replay engine

def exec_instr(st, ins, window_end, opaque_targets, boundary_targets):
    """Interpret ONE decoded instruction on state st.
    Returns None to continue, or a dict boundary event (call/branch/exit)."""

    mn, ops_raw = ins.mnemonic, ins.operands
    ops = split_operands(ops_raw) if ops_raw else []
    note = ""
    regs = st.regs

    if mn == "push":
        esp_before = st.esp_delta
        if len(ops) == 1 and HEX_RE.match(ops[0]):
            val = SymVal("IMM", ops[0])
            note = "push immediate " + ops[0]
        elif len(ops) == 1 and ops[0] in regs:
            val = regs[ops[0]]
            note = "push " + ops[0] + " (value: " + val.expr + ")"
        else:
            raise Unresolved("unsupported push operand: " + ops_raw)
        st.esp_delta -= 4
        st.write_slot(ins.va, "PUSH", st.esp_delta, val)
        st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
        return None

    if mn == "sub" or mn == "add":
        if len(ops) == 2 and ops[0] == "esp" and HEX_RE.match(ops[1]):
            esp_before = st.esp_delta
            d = int(ops[1], 16)
            st.esp_delta = st.esp_delta - d if mn == "sub" else st.esp_delta + d
            st.flag_writers.append((ins.va, ins.text))
            st.flags = {"zf": "ARITH", "set_by": ins.va}
            note = mn + " esp," + ops[1]
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        raise Unresolved("unsupported %s: %s" % (mn, ops_raw))

    if mn == "mov":
        if len(ops) != 2:
            raise Unresolved("mov with %d operands" % len(ops))
        dst, src = ops
        esp_before = st.esp_delta
        # segment absolute forms
        mseg = SEG_RE.match(src)
        if mseg:
            seg, off = mseg.group(1), mseg.group(2)
            if seg == "fs" and dst in regs:
                st.set_reg(ins.va, dst, SymVal("FS0", "FS0"))
                note = "read previous %s:[%s] into %s (opaque)" % (seg, off, dst)
            else:
                st.set_reg(ins.va, dst, SymVal("COOKIE_LOAD",
                                               "Moffs(%s:%s)" % (seg, off)))
                note = "opaque absolute load %s:%s -> %s" % (seg, off, dst)
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        msegd = SEG_RE.match(dst)
        if msegd:
            seg, off = msegd.group(1), msegd.group(2)
            if src not in regs:
                raise Unresolved("segment store from non-register: " + ops_raw)
            st.segment_writes.append((ins.va, seg, off, regs[src]))
            note = "SEGMENT write %s:[%s] := %s (NOT a stack write; assumption AS4)" % (
                seg, off, regs[src].expr)
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        # reg <- [esp+disp]
        if dst in regs and MEM_RE.match(src):
            disp = parse_disp(src)
            val, prov = st.read_slot(ins.va, st.esp_delta + disp)
            st.set_reg(ins.va, dst, val)
            note = "load %s := MEM(%s) [slot %s, %s]" % (
                dst, esp_expr(st.base, st.esp_delta + disp),
                slot_expr(st.base, st.esp_delta + disp), prov)
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        # [esp+disp] <- reg / [esp+disp] <- imm
        if MEM_RE.match(dst):
            disp = parse_disp(dst)
            if src in regs:
                val = regs[src]
            elif HEX_RE.match(src):
                val = SymVal("IMM", src)
            else:
                raise Unresolved("unsupported store source: " + ops_raw)
            st.write_slot(ins.va, "MOV_STORE", st.esp_delta + disp, val)
            note = "store [%s] := %s (no flag write)" % (
                esp_expr(st.base, st.esp_delta + disp), val.expr)
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        # reg <- reg
        if dst in regs and src in regs:
            st.set_reg(ins.va, dst, regs[src])
            note = "transfer %s := %s (%s)" % (dst, src, regs[src].expr)
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        raise Unresolved("unsupported mov: " + ops_raw)

    if mn == "lea":
        if len(ops) != 2 or ops[0] not in regs or not MEM_RE.match(ops[1]):
            raise Unresolved("unsupported lea: " + ops_raw)
        disp = parse_disp(ops[1])
        addr_delta = st.esp_delta + disp
        st.set_reg(ins.va, ops[0], SymVal(
            "ADDRESS", esp_expr(st.base, addr_delta) + " (computed)",
            delta=addr_delta, provenance="lea@" + va_str(ins.va)))
        note = "LEA %s := ADDRESS(%s) [kind=ADDRESS, opcode 8D; computed, not a read]" % (
            ops[0], esp_expr(st.base, addr_delta))
        st.steps.append((ins, st.esp_delta, st.esp_delta, note, regs.get("edi")))
        return None

    if mn == "xor":
        if len(ops) == 2 and ops[0] in regs and ops[1] in regs:
            esp_before = st.esp_delta
            base_kind = regs[ops[0]].kind
            st.set_reg(ins.va, ops[0], SymVal(
                "COOKIE_XOR_ESP",
                "%s XOR %s" % (regs[ops[0]].expr, ops[1].upper()),
                provenance="opaque value change; no ESP change"))
            st.flag_writers.append((ins.va, ins.text))
            st.flags = {"zf": "ARITH", "set_by": ins.va}
            note = "opaque value combine (%s XOR %s); push width unchanged" % (
                base_kind, ops[1].upper())
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        raise Unresolved("unsupported xor: " + ops_raw)

    if mn == "test":
        if len(ops) == 2 and ops[0] == ops[1] and ops[0] in regs:
            esp_before = st.esp_delta
            st.flag_writers.append((ins.va, ins.text))
            st.flags = {"zf": "EQ_ZERO(%s)" % regs[ops[0]].expr,
                        "set_by": ins.va, "tested_reg": ops[0],
                        "tested_value": regs[ops[0]]}
            note = "TEST %s,%s -> ZF := (%s == 0)" % (ops[0], ops[0], regs[ops[0]].expr)
            st.steps.append((ins, esp_before, st.esp_delta, note, regs.get("edi")))
            return None
        raise Unresolved("unsupported test: " + ops_raw)

    if mn == "call":
        if len(ops) != 1 or not HEX_RE.match(ops[0]):
            raise Unresolved("unsupported call: " + ops_raw)
        if not (len(ins.bytes_hex) == 5 and ins.bytes_hex[0] == "e8"):
            raise Unresolved("call is not rel32 e8: " + " ".join(ins.bytes_hex))
        rel = int.from_bytes(bytes(int(b, 16) for b in ins.bytes_hex[1:5]),
                             "little", signed=True)
        target_rc = ins.va + 5 + rel
        target = int(ops[0], 16)
        if target_rc != target:
            raise Unresolved("call target mismatch: objdump 0x%X, rel32 recompute 0x%X"
                             % (target, target_rc))
        esp_before = st.esp_delta
        # hardware return-address push (AS1)
        st.write_slot(ins.va, "RET_PUSH", st.esp_delta - 4,
                      SymVal("IMM", "RETURN_ADDRESS@" + va_str(ins.va)))
        st.esp_delta -= 4
        if target in opaque_targets:
            # opaque callee with the recorded normal ABI-compatible return
            # condition (AS3): pops exactly its return address, ESP restored,
            # EAX conveys the return value. The callee body is NOT opened.
            st.esp_delta += 4
            st.set_reg(ins.va, "eax", SymVal(
                "OPAQUE_RET", "OPAQUE_RET(%s)" % va_str(target),
                provenance="opaque call@" + va_str(ins.va) + " under AS3"))
            note = ("INCIDENTAL OPAQUE CALL -> %s (body NOT opened; normal-return "
                    "condition AS3 applied; ESP restored; EAX := OPAQUE_RET)" % va_str(target))
            st.steps.append((ins, esp_before, st.esp_delta, note,
                             st.regs.get("edi")))
            return None
        # non-opaque call: a delivery boundary. Stop the path here.
        st.steps.append((ins, esp_before, st.esp_delta,
                         "CALL boundary -> %s (callee NOT opened; ESP before "
                         "call recorded; hardware return-address push applied)"
                         % va_str(target), st.regs.get("edi")))
        return {"event": "call_boundary", "va": ins.va, "target": target,
                "target_recomputed": target_rc, "esp_before_call": esp_before,
                "callee_entry_esp_delta": esp_before - 4}

    if mn in ("je", "jne", "jmp"):
        if len(ops) != 1 or not HEX_RE.match(ops[0]):
            raise Unresolved("unsupported branch: " + ops_raw)
        want = {"je": 0x74, "jne": 0x75, "jmp": 0xeb}[mn]
        if int(ins.bytes_hex[0], 16) != want:
            raise Unresolved("branch opcode mismatch for %s: %s"
                             % (mn, " ".join(ins.bytes_hex)))
        rel8 = int.from_bytes(bytes(int(b, 16) for b in ins.bytes_hex[1:2]),
                              "little", signed=True)
        target = ins.va + 2 + rel8
        if target != int(ops[0], 16):
            raise Unresolved("branch target mismatch: objdump 0x%X, rel8 0x%X"
                             % (int(ops[0], 16), target))
        st.steps.append((ins, st.esp_delta, st.esp_delta,
                         "%s 0x%X" % (mn, target), regs.get("edi")))
        return {"event": "branch", "va": ins.va, "mnemonic": mn,
                "target": target, "flags": st.flags}

    raise Unresolved("unsupported mnemonic: " + mn)


# ---------------------------------------------------------------- path walking

class PathResult(object):
    def __init__(self, name, state, end):
        self.name = name          # "STRAIGHT", "NONNULL", "NULL"
        self.state = state
        self.end = end            # dict: end kind + boundary/exit facts


def walk(instrs, base_symbol, va_start, va_end, entry_receiver,
         opaque_targets, boundary_targets, max_paths=2, unknown_suffix="ENTRY"):
    """Enumerate every path through the decoded window. Bounded to max_paths;
    raises Unresolved if more paths would appear (fail-closed)."""
    results = []
    stack = [(State(base_symbol, entry_receiver, unknown_suffix), 0, "STRAIGHT")]
    while stack:
        st, idx, name = stack.pop()
        if idx >= len(instrs):
            results.append(PathResult(name, st, {"event": "window_end"}))
            continue
        ev = exec_instr(st, instrs[idx], va_end, opaque_targets, boundary_targets)
        if ev is None:
            stack.append((st, idx + 1, name))
            continue
        if ev["event"] == "call_boundary":
            results.append(PathResult(name, st, ev))
            continue
        if ev["event"] == "branch":
            mn, target = ev["mnemonic"], ev["target"]
            in_window = va_start <= target < va_end
            if mn == "jmp":
                if in_window:
                    tgt_idx = next((i for i, ins in enumerate(instrs)
                                   if ins.va == target), None)
                    if tgt_idx is None:
                        raise Unresolved("in-window jmp target not decoded")
                    stack.append((st, tgt_idx, name + "+JMP"))
                    continue
                results.append(PathResult(name, st, dict(
                    ev, end="exit_window", exit_va=target,
                    exit_kind="unconditional_jump_outside")))
                continue
            # conditional branch on ZF
            if ev["flags"] is None or not str(ev["flags"].get("zf", "")).startswith("EQ_ZERO"):
                raise Unresolved("conditional branch without a TEST-defined ZF")
            if len(results) + len(stack) + 2 > max_paths:
                raise Unresolved("more than %d paths required" % max_paths)
            st_taken = st.clone()
            st_taken.steps.append((instrs[idx], st.esp_delta, st.esp_delta,
                                   "PATH FORK: ZF=1 branch taken", None))
            st_fall = st.clone()
            st_fall.steps.append((instrs[idx], st.esp_delta, st.esp_delta,
                                  "PATH FORK: ZF=0 fall-through", None))
            if in_window:
                tgt_idx = next((i for i, ins in enumerate(instrs)
                                if ins.va == target), None)
                if tgt_idx is None:
                    raise Unresolved("in-window branch target not decoded")
                stack.append((st_taken, tgt_idx, name + "_TAKEN"))
            else:
                results.append(PathResult(name + "_NULL", st_taken, dict(
                    ev, end="exit_window", exit_va=target,
                    exit_kind="conditional_jump_taken_outside")))
            stack.append((st_fall, idx + 1, name + "_FALL"))
            continue
        raise Unresolved("unknown event " + str(ev["event"]))
    return results


# ---------------------------------------------------------------- phase drivers
# All B-side deltas below are relative to T0 (ESP at window-B start).  The
# pivot T satisfies T = T0 + T_delta (measured; T_delta = 0 under AS3 for the
# audited stream).  Every fact extractor normalizes T0 deltas to T via T_delta.

def derive_a(instrs_a, base_symbol="E"):
    """Phase A: replay window A from its entry. Single straight-line path."""
    va_start = WINDOWS["A"]["va_start"]
    va_end = va_start + WINDOWS["A"]["size"]
    paths = walk(instrs_a, base_symbol, va_start, va_end,
                 entry_receiver=True, opaque_targets=set(), boundary_targets=None)
    if len(paths) != 1 or paths[0].end["event"] != "call_boundary":
        raise Unresolved("window A did not end in a single call boundary")
    st = paths[0].state
    ev = paths[0].end
    if ev["target"] != TAIL_CALLEE:
        raise Unresolved("window A tail call target is not the pinned callee")

    # pivot S: ESP after the instruction at PIVOT_S_VA
    s_delta = None
    for (ins, eb, ea, note, _x) in st.steps:
        if ins.va == PIVOT_S_VA:
            s_delta = ea
    if s_delta is None:
        raise Unresolved("pivot S VA 0x%X not found in window A" % PIVOT_S_VA)

    # delivery push = last PUSH before the tail call
    pushes = [w for w in st.writes if w[1] == "PUSH" and w[0] < ev["va"]]
    if not pushes:
        raise Unresolved("no delivery push before the tail call")
    last_push = pushes[-1]
    # callee entry ESP = esp_before_call - 4 (hardware return-address push, AS1);
    # first explicit stack argument slot = [ESP_entry + 4] (AS2) = esp_before_call
    arg1_slot_delta = ev["esp_before_call"]
    if last_push[2] != arg1_slot_delta:
        raise Unresolved("last push slot %s != expected arg1 slot %s"
                         % (last_push[2], arg1_slot_delta))
    push_ins = next((ins for ins in instrs_a if ins.va == last_push[0]), None)
    if push_ins is None or push_ins.mnemonic != "push":
        raise Unresolved("delivery push instruction not found")
    pushed_reg = push_ins.operands.strip()
    # the delivered value is the SymVal captured AT PUSH TIME (the write log
    # stores the exact pushed object); reg_defs alone would be stale after any
    # later register overwrite.
    src_val = last_push[3]
    if src_val.kind != "STACK_READ":
        raise Unresolved("A source value is not a stack read (kind=%s)" % src_val.kind)
    src_va, src_slot_delta = producing_load_va(st, src_val)
    if src_va is None:
        raise Unresolved("source load read record missing")

    # (b) entry-slot value preservation: no write to the source slot before it
    writes_before = [w for w in st.writes if w[0] < src_va]
    aliasing = [w for w in writes_before if w[2] == src_slot_delta]
    seg_before = [s for s in st.segment_writes if s[0] < src_va]
    preserved = (len(aliasing) == 0)

    # (c) EDI preservation: EDI's reaching def at the push is the source load
    edi_def = st.reg_defs.get("edi")
    edi_preserved = (edi_def is not None and edi_def[0] == src_va
                     and push_ins.va > src_va)

    facts = {
        "S_delta": s_delta,
        "source_load_va": va_str(src_va),
        "source_slot_delta": src_slot_delta,
        "source_slot_expr": slot_expr(base_symbol, src_slot_delta),
        "source_pivot_expr": slot_expr("S", src_slot_delta - s_delta),
        "entry_slot_value_preserved": preserved,
        "writes_before_source_load": [
            {"va": va_str(w[0]), "kind": w[1],
             "slot": slot_expr(base_symbol, w[2]), "value": w[3].expr}
            for w in writes_before],
        "segment_writes_before_source_load": [
            {"va": va_str(s[0]), "segment": s[1] + ":[" + s[2] + "]",
             "value": s[3].expr} for s in seg_before],
        "aliasing_writes_to_source_slot": [
            {"va": va_str(w[0]), "kind": w[1]} for w in aliasing],
        "edi_preserved": edi_preserved,
        "edi_reaching_def_at_push": va_str(edi_def[0]) if edi_def else None,
        "pushed_register": pushed_reg,
        "delivery_push_va": va_str(last_push[0]),
        "tail_call_va": va_str(ev["va"]),
        "tail_target": va_str(ev["target"]),
        "esp_before_tail_call_delta": ev["esp_before_call"],
        "callee_entry_esp_delta": ev["callee_entry_esp_delta"],
        "esp_before_tail_call": esp_expr(base_symbol, ev["esp_before_call"]),
        "esp_before_tail_call_S": esp_expr("S", ev["esp_before_call"] - s_delta),
        "callee_entry_esp": esp_expr(base_symbol, ev["callee_entry_esp_delta"]),
        "callee_entry_esp_S": esp_expr("S", ev["callee_entry_esp_delta"] - s_delta),
        "arg1_slot_delta": arg1_slot_delta,
        "arg1_slot_expr": slot_expr(base_symbol, arg1_slot_delta),
        "arg1_slot_expr_S": slot_expr("S", arg1_slot_delta - s_delta),
        "arg1_value_kind": last_push[3].kind,
        "arg1_value_delta": src_slot_delta,
        "receiver_expr": st.regs["ecx"].expr,
        "receiver_kind": st.regs["ecx"].kind,
        "instruction_count": len(instrs_a),
        "_a_state_writes": st.writes,        # raw write log for bridge_join
    }
    return facts, paths[0]


def derive_b(instrs_b, base_symbol="T0"):
    """Phase B: replay window B; enumerate NULL and NONNULL paths."""
    va_start = WINDOWS["B"]["va_start"]
    va_end = va_start + WINDOWS["B"]["size"]
    paths = walk(instrs_b, base_symbol, va_start, va_end,
                 entry_receiver=False, opaque_targets={OPAQUE_CALLEE},
                 boundary_targets=None, unknown_suffix="UNKNOWN_T")
    null_path = None
    nonnull_path = None
    for p in paths:
        if p.end.get("event") == "call_boundary":
            if nonnull_path is not None:
                raise Unresolved("multiple call-boundary paths in window B")
            nonnull_path = p
        elif p.end.get("end") == "exit_window":
            if null_path is not None:
                raise Unresolved("multiple exit paths in window B")
            null_path = p
        else:
            raise Unresolved("unexpected path end " + str(p.end.get("event")))
    facts = {"path_count": len(paths), "instruction_count": len(instrs_b)}
    if null_path is not None:
        ev = null_path.end
        br = next(ins for ins in instrs_b if ins.va == ev["va"])
        facts["null_path"] = {
            "branch_va": va_str(ev["va"]), "branch_op": br.text,
            "branch_mnemonic": br.mnemonic,
            "exit_va": va_str(ev["exit_va"]),
            "exit_inside_window": bool(va_start <= ev["exit_va"] < va_end),
            "je_taken": ev["exit_kind"] == "conditional_jump_taken_outside",
            "unconditional_exit": ev["exit_kind"] == "unconditional_jump_outside",
            "call_reached": False,
        }
    if nonnull_path is not None:
        st = nonnull_path.state
        ev = nonnull_path.end
        t_delta = None
        for (ins, eb, ea, note, _x) in st.steps:
            if ins.va == PIVOT_T_VA:
                t_delta = ea
        if t_delta is None:
            raise Unresolved("pivot T VA 0x%X not found in window B" % PIVOT_T_VA)
        # the instruction at LEA_VA (generic record: LEA or MOV after mutation);
        # value snapshot from reg_writes AT THE INSTRUCTION (reg_defs would be
        # stale after the later mov ecx,eax overwrite)
        lea_ins = next((ins for ins in instrs_b if ins.va == LEA_VA), None)
        lea_rec = None
        if lea_ins is not None:
            dst = lea_ins.operands.split(",")[0].strip()
            snap = [rw for rw in st.reg_writes
                    if rw[0] == LEA_VA and rw[1] == dst]
            v = snap[-1][2] if snap else None
            lea_rec = {"va": va_str(LEA_VA), "op": lea_ins.text,
                       "dst": dst,
                       "kind": v.kind if v else None,
                       "expr": v.expr if v else None,
                       "value_delta": v.delta if v else None,
                       "reaching_def_va": va_str(snap[-1][0]) if snap else None}
        # arg1 = last push before the call boundary
        pushes = [w for w in st.writes if w[1] == "PUSH" and w[0] < ev["va"]]
        if not pushes:
            raise Unresolved("no arg push before the bridge call")
        last_push = pushes[-1]
        arg1_slot_delta = ev["esp_before_call"]
        if last_push[2] != arg1_slot_delta:
            raise Unresolved("last push slot %s != expected arg1 slot %s"
                             % (last_push[2], arg1_slot_delta))
        push_ins = next(ins for ins in instrs_b if ins.va == last_push[0])
        pushed_reg = push_ins.operands.strip()
        # value captured at push time (write log); reg_defs would be stale
        # after the later mov ecx,eax overwrite.
        arg1_val = last_push[3]
        if arg1_val.kind == "STACK_READ":
            rd_va, _rd_slot = producing_load_va(st, arg1_val)
        elif arg1_val.kind == "ADDRESS":
            rd_va = int((arg1_val.provenance or "lea@0").split("@")[-1], 16) \
                if arg1_val.provenance else None
        else:
            rd_va = None
        recv = st.regs["ecx"]
        # flags TEST -> JE census
        br_test = next((ins for ins in instrs_b
                        if ins.mnemonic == "test" and ins.va < ev["va"]), None)
        je_ins = next(ins for ins in instrs_b
                      if ins.mnemonic in ("je", "jne", "jmp") and ins.va < ev["va"])
        if br_test is None:
            raise Unresolved("no TEST instruction before the branch in window B")
        flag_writers_between = [w for w in st.flag_writers
                                if br_test.va < w[0] < je_ins.va]
        flags_preserved = (len(flag_writers_between) == 0
                           and st.flags is not None
                           and st.flags.get("set_by") == br_test.va)
        opaque_call = next((ins for ins in instrs_b
                            if ins.mnemonic == "call"
                            and int(ins.operands.strip(), 16) == OPAQUE_CALLEE), None)
        # argument slots arg1..arg4 at the callee entry (AS2), T0 deltas
        arg_slots = {}
        for k in range(1, 5):
            dl = ev["esp_before_call"] + 4 * (k - 1)
            if dl in st.mem:
                arg_slots["arg%d" % k] = st.mem[dl][0]
        facts["nonnull_path"] = {
            "T_delta": t_delta,
            "flags": {
                "test_va": va_str(br_test.va),
                "test_op": br_test.text,
                "je_va": va_str(je_ins.va),
                "je_op": je_ins.text,
                "flag_writers_between": [va_str(w[0]) + " " + w[1]
                                         for w in flag_writers_between],
                "flags_preserved_test_to_je": flags_preserved,
                "je_condition": "EAX==0 -> taken (exit); EAX!=0 -> fall-through",
            },
            "opaque_call": {
                "va": va_str(opaque_call.va) if opaque_call else None,
                "target": va_str(OPAQUE_CALLEE),
                "preceding_push": "push 0x128",
                "following_cleanup": "add esp,0x4",
                "return_condition": "AS3 normal ABI-compatible return: pops "
                                    "exactly the return address (ESP restored), "
                                    "return value in EAX; body NOT opened",
                "callee_body_opened": False,
            },
            "lea_instruction": lea_rec,
            "arg1": {
                "final_push_va": va_str(last_push[0]),
                "pushed_register": pushed_reg,
                "slot_delta_T0": arg1_slot_delta,
                "value_kind": arg1_val.kind,
                "value_delta": arg1_val.delta,
                "value_provenance": arg1_val.provenance,
                "reaching_def_va": va_str(rd_va) if rd_va is not None else None,
            },
            "arg_slots": {k: {"kind": v.kind, "delta": v.delta, "expr": v.expr}
                          for k, v in arg_slots.items()},
            "arg_slot_deltas": {"arg%d" % k: ev["esp_before_call"] + 4 * (k - 1)
                                for k in range(1, 5)},
            "receiver": {"kind": recv.kind, "expr": recv.expr},
            "call": {
                "va": va_str(ev["va"]),
                "target": va_str(ev["target"]),
                "target_recomputed": va_str(ev["target_recomputed"]),
                "esp_before_call_delta_T0": ev["esp_before_call"],
                "callee_entry_esp_delta_T0": ev["callee_entry_esp_delta"],
                "bridge_valid": ev["target"] == BRIDGE_CALLEE,
            },
            "state": st,
        }
    return facts, paths


# ---------------------------------------------------------------- fact layer

def norm_expr_T0(kind, delta_T0, t_delta, reaching_def_va=None):
    """Normalize a T0-based value/slot delta into a T-based expression string."""
    dt = delta_T0 - t_delta if delta_T0 is not None else None
    suffix = "" if dt == 0 else ("+" if dt > 0 else "-") + "0x%x" % abs(dt)
    if kind == "ADDRESS":
        return "ADDRESS(T%s)" % suffix
    if kind == "STACK_READ":
        return "MEM(T%s)" % suffix
    return None


def producing_load_va(state, value):
    """The VA of the in-window read that created this value object
    (identity match; caller-area reads create unique objects), or None."""
    for r in state.reads:
        if r[2] is value:
            return r[0], r[1]
    return None, None


def extract_case_facts(case, a_facts, b_facts):
    """Flatten derived facts into the EXPECTED-table fact keys for one case."""
    out = {}
    if case in ("A_CLEAN", "M1_A_FRAME", "M2_A_SLOT"):
        out = {
            "S_delta": a_facts["S_delta"],
            "source_slot_delta": a_facts["source_slot_delta"],
            "entry_slot_value_preserved": a_facts["entry_slot_value_preserved"],
            "edi_preserved": a_facts["edi_preserved"],
            "tail_target": a_facts["tail_target"],
            "arg1_kind": a_facts["arg1_value_kind"],
        }
        return out
    nn = b_facts.get("nonnull_path")
    np_ = b_facts.get("null_path")
    if nn:
        t_delta = nn["T_delta"]
        out.update({
            "T_delta": t_delta,
            "flags_preserved_test_to_je": nn["flags"]["flags_preserved_test_to_je"],
            "nonnull_reaches_call": True,
            "arg1_kind": nn["arg1"]["value_kind"],
            "arg1_expr": norm_expr_T0(nn["arg1"]["value_kind"],
                                     nn["arg1"]["value_delta"], t_delta,
                                     nn["arg1"]["reaching_def_va"]),
            "arg1_slot_delta": nn["arg1"]["slot_delta_T0"] - t_delta,
            "receiver_kind": nn["receiver"]["kind"],
            "receiver_expr": nn["receiver"]["expr"],
            "bridge_target": nn["call"]["target"],
            "bridge_target_actual": nn["call"]["target"],
            "bridge_valid": nn["call"]["bridge_valid"],
        })
        for k, v in nn["arg_slots"].items():
            out[k + "_expr"] = (norm_expr_T0(v["kind"], v["delta"], t_delta)
                                if v["delta"] is not None else v["expr"])
    else:
        out.update({"nonnull_reaches_call": False,
                    "bridge_target": None, "bridge_target_actual": None,
                    "bridge_valid": False})
    if np_:
        out.update({
            "null_je_taken": np_["je_taken"],
            "null_call_reached": np_["call_reached"],
            "unconditional_exit": np_["unconditional_exit"],
        })
    return out


# ---------------------------------------------------------------- bridge join

def bridge_join(a_facts, b_facts):
    """Join Phase B to Phase A: E = the callee-entry ESP measured in B, i.e.
    E = T + (callee_entry_esp_delta_T0 - T_delta).  Checks slot-address
    identity, value preservation between the B-side write and the A-side load,
    and the pointer-value identity across both delivery boundaries.  Derived,
    never assumed."""
    nn = b_facts.get("nonnull_path")
    if nn is None:
        return {"status": "NOT_PERFORMED",
                "reason": "no nonnull path in window B"}
    t_delta = nn["T_delta"]
    e_delta = nn["call"]["callee_entry_esp_delta_T0"] - t_delta   # E = T + e_delta
    a_src = a_facts["source_slot_delta"]
    a_src_T = e_delta + a_src                                     # in T terms
    b_arg1_T = nn["arg1"]["slot_delta_T0"] - t_delta
    slot_identity = (a_src_T == b_arg1_T)
    result = {
        "join_expr": "E = T%s" % ("" if e_delta == 0 else
                                  ("+" if e_delta > 0 else "-")
                                  + "0x%x" % abs(e_delta)),
        "E_delta_from_T": e_delta,
        "a_source_slot_from_T": slot_expr("T", a_src_T),
        "b_arg1_slot": slot_expr("T", b_arg1_T),
        "slot_address_identity": slot_identity,
        "b_arg1_value_kind": nn["arg1"]["value_kind"],
        "b_arg1_value_expr": norm_expr_T0(nn["arg1"]["value_kind"],
                                        nn["arg1"]["value_delta"], t_delta,
                                        nn["arg1"]["reaching_def_va"]),
        "b_final_push_va": nn["arg1"]["final_push_va"],
        "a_source_load_va": a_facts["source_load_va"],
        "a_delivered_value_kind": a_facts["arg1_value_kind"],
    }
    if not slot_identity:
        result["status"] = "REJECTED_SLOT_MISMATCH"
        return result
    if nn["arg1"]["value_kind"] != "ADDRESS":
        result["status"] = "REJECTED_VALUE_KIND_NOT_ADDRESS"
        return result
    # value preservation: no OTHER write to the joined slot in the interval
    # (b_final_push_va, a_source_load_va).  Enumerate B and A write logs in T.
    b_writes = [(w[0], w[2] - t_delta) for w in nn["state"].writes
                if w[0] > int(nn["arg1"]["final_push_va"], 16)]
    # A write log deltas are relative to E; convert: T = E - e_delta
    a_writes = [(w[0], w[2] + e_delta) for w in a_facts["_a_state_writes"]]
    load_va = int(a_facts["source_load_va"], 16)
    push_va = int(nn["arg1"]["final_push_va"], 16)
    intervening = [(va_str(va), slot_expr("T", dl)) for va, dl in
                   (b_writes + a_writes)
                   if push_va < va < load_va and dl == b_arg1_T]
    result["intervening_writes_to_joined_slot"] = intervening
    if intervening:
        result["status"] = "REJECTED_SLOT_OVERWRITTEN"
        return result
    if a_facts["arg1_value_kind"] != "STACK_READ":
        result["status"] = "REJECTED_A_VALUE_KIND"
        return result
    if not (a_facts["entry_slot_value_preserved"] and a_facts["edi_preserved"]):
        result["status"] = "REJECTED_A_PRESERVATION"
        return result
    result["status"] = "POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL"
    result["cross_call_value_expr"] = result["b_arg1_value_expr"]
    result["delivered_boundaries"] = [
        "arg1 of FUN_00528E50 at its entry (CALL 0x004C47C1)",
        "arg1 of FUN_0085B1B0 at its entry (CALL 0x00528E8D)",
    ]
    result["conditions"] = [
        "AS3 opaque callee 0x0095D3C4 normal ABI-compatible return",
        "EAX != 0 at 0x004C47AD (qualified branch only)",
        "AS4 FS/TIB disjoint from the live argument stack region",
        "AS5 straight-line window-A path from entry 0x00528E50",
        "AS1/AS2 x86 push/call stack semantics and cdecl argument order",
    ]
    return result


# ---------------------------------------------------------------- case runner

def build_fixture(case, orig_bytes, win_key, workdir):
    """Original window bytes for clean cases; byte-mutated synthetic copies
    for M cases. Returns (fixture_bytes, input_kind, mutation_note)."""
    if case in ("A_CLEAN", "B_CLEAN_NONNULL", "B_CLEAN_NULL"):
        return bytes(orig_bytes), "ORIGINAL", None
    mu = MUTATIONS[case]
    va = mu["va"]
    start = WINDOWS[win_key]["va_start"]
    idx = va - start
    data = bytearray(orig_bytes)
    orig_b = [int(x, 16) for x in mu["orig"].split()]
    new_b = [int(x, 16) for x in mu["new"].split()]
    if list(data[idx:idx + len(orig_b)]) != orig_b:
        raise Unresolved("original bytes at %s do not match contract "
                         "mutation precondition: found %s expected %s"
                         % (va_str(va),
                            " ".join("%02x" % b for b in data[idx:idx + len(orig_b)]),
                            mu["orig"]))
    if len(orig_b) != len(new_b):
        raise Unresolved("mutation %s changes instruction length" % case)
    data[idx:idx + len(new_b)] = bytes(new_b)
    note = ("%s @%s: %s -> %s (synthetic copy; EXE untouched)"
            % (case, va_str(va), mu["orig"], mu["new"]))
    return bytes(data), "SYNTHETIC_MUTATION", note


def run_case(case, repo_out, workdir, tool_header):
    """Run the byte -> objdump -> symbolic pipeline for one control case and
    compare derived facts to the preregistered expected discriminating result."""
    if case in ("A_CLEAN", "B_CLEAN_NONNULL", "B_CLEAN_NULL"):
        win_key = "A" if case == "A_CLEAN" else "B"
    else:
        win_key = MUTATIONS[case]["window"]
    win = WINDOWS[win_key]
    orig = read_exe_window(EXE_PATH, win)
    if sha256_bytes(orig) != win["sha256"]:
        raise Unresolved("window %s physical bytes do not match the pinned "
                         "SHA256 (identity failure)" % win_key)
    data, input_kind, mutation_note = build_fixture(case, orig, win_key, workdir)
    case_dir = os.path.join(workdir, "cases")
    os.makedirs(case_dir, exist_ok=True)
    fix_path = os.path.join(case_dir, case + ".bin")
    with open(fix_path, "wb") as fh:
        fh.write(data)
    rc, out, cmd = run_objdump(fix_path, win["va_start"])
    if rc != 0:
        return {"case": case, "verdict": "UNRESOLVED",
                "reason": "objdump rc=%d" % rc}
    instrs = parse_objdump(out, win["va_start"],
                           win["va_start"] + win["size"])
    raw_rel = "01_RAW/CONTROLS/%s_OBJDUMP.txt" % case
    with open(os.path.join(repo_out, raw_rel), "w") as fh:
        fh.write(tool_header)
        fh.write("Case: %s\n" % case)
        fh.write("Command: %s\n" % cmd.replace(fix_path, os.path.basename(fix_path)))
        if mutation_note:
            fh.write("Mutation: %s\n" % mutation_note)
        fh.write("Input fixture: %s (size %d, SHA256 %s)\n"
                 % (os.path.basename(fix_path), len(data), sha256_bytes(data)))
        fh.write("Exit status: %d\n" % rc)
        fh.write("--- RAW OUTPUT BELOW ---\n\n")
        fh.write(out)

    a_facts = b_facts = None
    if win_key == "A":
        a_facts, _pa = derive_a(instrs)
    else:
        b_facts, _pb = derive_b(instrs)

    derived = extract_case_facts(case, a_facts, b_facts)
    checks = []
    all_ok = True
    for key, want in sorted(EXPECTED[case]["facts"].items()):
        got = derived.get(key, None)
        ok = (got == want)
        all_ok = all_ok and ok
        checks.append({"fact": key, "expected": want, "actual": got, "match": ok})
    verdict = "CONTROL_PASS" if all_ok else "CONTROL_FAIL"

    case_rec = {
        "case": case,
        "window": win_key,
        "input_kind": input_kind,
        "mutation": mutation_note,
        "fixture": {"name": case + ".bin", "size": len(data),
                    "sha256": sha256_bytes(data),
                    "note": "identity hashes qualify ORIGINAL inputs only; "
                            "synthetic fixtures are analyzed, never rejected "
                            "by hash"},
        "objdump": {"command": cmd, "rc": rc, "raw_output": raw_rel},
        "decode": {
            "instructions": len(instrs),
            "covers_window_exactly": True,
            "first_va": va_str(instrs[0].va),
            "last_instruction": va_str(instrs[-1].va) + " (" +
                               " ".join(instrs[-1].bytes_hex) + ")",
            "window": "[%s,%s)" % (va_str(win["va_start"]),
                                   va_str(win["va_start"] + win["size"])),
        },
        "derived_facts": derived,
        "expected_text": EXPECTED[case]["text"],
        "checks": checks,
        "verdict": verdict,
    }
    if a_facts:
        case_rec["phase_a_facts"] = {k: v for k, v in a_facts.items()
                                     if not k.startswith("_")}
    if b_facts:
        case_rec["phase_b_facts"] = jsonable_b_facts(b_facts)
    return case_rec


def jsonable_b_facts(b_facts):
    out = dict(b_facts)
    if "nonnull_path" in out:
        nn = dict(out["nonnull_path"])
        nn.pop("state", None)
        if "arg1" in nn:
            a1 = dict(nn["arg1"])
            a1["value_expr"] = norm_expr_T0(a1["value_kind"], a1["value_delta"],
                                            nn["T_delta"],
                                            a1["reaching_def_va"])
            nn["arg1"] = a1
        out["nonnull_path"] = nn
    return out


# ---------------------------------------------------------------- ledger writers

def write_entry_frame_ledger(path, a_path_result, a_facts):
    st = a_path_result.state
    writes_by_va = {}
    for w in st.writes:
        writes_by_va.setdefault(w[0], []).append(w)
    reads_by_va = {}
    for r in st.reads:
        reads_by_va.setdefault(r[0], []).append(r)
    segs_by_va = {}
    for s in st.segment_writes:
        segs_by_va.setdefault(s[0], []).append(s)
    rows = []
    seq = 0
    for (ins, eb, ea, note, _edi) in st.steps:
        seq += 1
        ws = writes_by_va.get(ins.va, [])
        rs = reads_by_va.get(ins.va, [])
        sg = segs_by_va.get(ins.va, [])
        w_txt = "; ".join("%s %s := %s" % (w[1], slot_expr("E", w[2]),
                                           w[3].expr) for w in ws)
        r_txt = "; ".join("READ %s -> %s (%s)" % (slot_expr("E", r[1]),
                                                  r[2].expr, r[3]) for r in rs)
        s_txt = "; ".join("SEGMENT %s:[%s] := %s" % (x[1], x[2], x[3].expr)
                          for x in sg)
        flag = "YES" if any(f[0] == ins.va for f in st.flag_writers) else ""
        rows.append([seq, va_str(ins.va), " ".join(ins.bytes_hex), ins.text,
                     esp_expr("E", eb), esp_expr("E", ea),
                     (("+" if ea > eb else "-") + "0x%x" % abs(ea - eb))
                     if ea != eb else "0",
                     note, w_txt, r_txt, s_txt, flag])
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["SEQ", "VA", "BYTES", "DECODED_OP", "ESP_BEFORE", "ESP_AFTER",
                    "ESP_DELTA", "NOTES", "STACK_WRITES", "STACK_READS",
                    "SEGMENT_WRITES", "FLAG_WRITER"])
        w.writerows(rows)
    return len(rows)


def write_caller_ledger(path, b_paths, b_facts):
    rows = []
    for p in b_paths:
        if p.end.get("end") == "exit_window":
            pname = "NULL"
        else:
            pname = "NONNULL"
        st = p.state
        writes_by_va = {}
        for x in st.writes:
            writes_by_va.setdefault(x[0], []).append(x)
        reads_by_va = {}
        for x in st.reads:
            reads_by_va.setdefault(x[0], []).append(x)
        seq = 0
        for (ins, eb, ea, note, _edi) in st.steps:
            seq += 1
            ws = writes_by_va.get(ins.va, [])
            rs = reads_by_va.get(ins.va, [])
            w_txt = "; ".join("%s %s := %s" % (x[1], slot_expr("T0", x[2]),
                                               x[3].expr) for x in ws)
            r_txt = "; ".join("READ %s -> %s (%s)" % (slot_expr("T0", x[1]),
                                                      x[2].expr, x[3]) for x in rs)
            flag = "YES" if any(f[0] == ins.va for f in st.flag_writers) else ""
            rows.append([pname, seq, va_str(ins.va), " ".join(ins.bytes_hex),
                         ins.text, esp_expr("T0", eb), esp_expr("T0", ea),
                         (("+" if ea > eb else "-") + "0x%x" % abs(ea - eb))
                         if ea != eb else "0",
                         note, w_txt, r_txt, flag])
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["PATH", "SEQ", "VA", "BYTES", "DECODED_OP", "ESP_BEFORE",
                    "ESP_AFTER", "ESP_DELTA", "NOTES", "STACK_WRITES",
                    "STACK_READS", "FLAG_WRITER"])
        w.writerows(rows)
    return len(rows)


# ---------------------------------------------------------------- provenance

def build_bridge_provenance(a_facts, a_path, b_facts, b_paths, join, tool_ver,
                           window_ids):
    ex = ("D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe", )
    exe_line = {"path": EXE_PATH, "size": EXE_SIZE, "sha256": EXE_SHA256}
    ev_origin = "01_RAW objdump text (GNU objdump 2.44 raw output) replayed by " \
                "03_SCRIPTS/run_frame_bridge.py; physical window bytes from the EXE"

    def claim(cid, cls, statement, va, win, op, esp_fact, status, assum, unc,
              measured=None, ist=None, circ=None, fail=None):
        c = {
            "claim_id": cid,
            "claim_class": cls,   # FUNCTION_IDENTITY / OBSERVED_STATIC_OPERATION /
                                  # ARGUMENT_DELIVERY / POINTER_VALUE_IDENTITY /
                                  # FINAL_SEMANTIC_ROLE
            "statement": statement,
            "build_exe": exe_line,
            "va": va,
            "window": win,
            "decoded_op": op,
            "esp_register_memory_fact": esp_fact,
            "path_abi_alias_assumptions": assum,
            "evidence_origin": ev_origin,
            "status": status,
            "remaining_uncertainty": unc,
        }
        if measured is not None:
            c["MEASURED_QUANTITY"] = measured
            c["INDEPENDENT_SOURCE_OF_TRUTH"] = ist
            c["WHY_NON_CIRCULAR"] = circ
            c["FAILURE_CASE_DETECTED"] = fail
        return c

    af = a_facts
    nn = b_facts["nonnull_path"]
    claims = []
    claims.append(claim(
        "A-1", "FUNCTION_IDENTITY",
        "Window A decodes as a valid 32-bit instruction stream of %d "
        "instructions starting exactly at the pinned entry VA 0x00528E50 and "
        "ending exactly at 0x00528E92; it is the entry portion of the function "
        "entered via CALL 0x004C47C1 (boundary provenance: the direct call "
        "target and the pinned historical listing F00528E50_CTOR_MOBJ.txt; the "
        "body beyond the window is NOT opened)." % af["instruction_count"],
        "0x00528E50", "A", "first=push 0xffffffff; last=call 0x85b1b0",
        "entry ESP := E (symbolic)", "QUALIFIED_AS_DECODED_ENTRY_PORTION",
        ["decode coverage check from objdump output"],
        "function identity beyond the entry boundary is NOT claimed"))
    claims.append(claim(
        "A-2", "OBSERVED_STATIC_OPERATION",
        "SEH prologue chain: push -1; push 0x9BF53F; mov eax,fs:0x0; push eax; "
        "sub esp,0x1c -> ESP = E-0x28 measured (pushes write E-4, E-8, E-0xC).",
        "0x00528E50..0x00528E5E", "A",
        "push 0xffffffff / push 0x9bf53f / mov eax,fs:0x0 / push eax / sub esp,0x1c",
        "E-0x0 -> E-0x28 (5 instructions)", "QUALIFIED", [],
        "none for this bounded operation"))
    claims.append(claim(
        "A-3", "OBSERVED_STATIC_OPERATION",
        "Register saves and security cookie: push ebx; push esi; push edi; "
        "mov eax,ds:0xB9D8D0; xor eax,esp; push eax -> ESP = E-0x38 =: S; the "
        "cookie computation changes a value, not the push width.",
        "0x00528E61..0x00528E6B", "A",
        "push ebx / push esi / push edi / mov eax,ds:0xb9d8d0 / xor eax,esp / push eax",
        "E-0x28 -> E-0x38 (6 instructions)", "QUALIFIED", [],
        "the cookie value itself is opaque and irrelevant to slot identity"))
    claims.append(claim(
        "A-4", "OBSERVED_STATIC_OPERATION",
        "mov DWORD PTR [esp+0x10],esi @0x00528E78 stores the entry receiver "
        "value at [E-0x28] (below E); mov fs:0x0,eax @0x00528E70 is a SEGMENT "
        "write of the TIB chain head (stores the address E-0xC), not a stack "
        "write.", "0x00528E70 / 0x00528E78", "A",
        "mov fs:0x0,eax / mov DWORD PTR [esp+0x10],esi",
        "store target [E-0x28]; segment target FS:[0]",
        "QUALIFIED_WITH_ASSUMPTION_AS4",
        ["AS4: FS segment base (TIB) is disjoint from the live argument stack "
         "region containing [E+4]; runtime FS base not statically resolvable"],
        "AS4 is an assumption; no runtime verification in this run"))
    claims.append(claim(
        "A-5", "ARGUMENT_DELIVERY",
        "Source load: EDI := DWORD [ESP+0x3C] @0x00528E84 with ESP = E-0x38 = "
        "S reads the slot [E+4] == [S+0x3C] (address equivalence of the old "
        "source slot and the entry first stack-argument slot, both derived).",
        "0x00528E84", "A", "mov edi,DWORD PTR [esp+0x3c] (8b 7c 24 3c)",
        "read slot [E+0x4] = [S+0x3C]", "QUALIFIED",
        ["AS2: [ESP_at_entry+4] is the first explicit stack argument slot"],
        "none for the slot-address equivalence",
        measured="[E+4] == [S+0x3C] slot-address equivalence; S=E-0x38 chain",
        ist="byte-decoded displacement 0x3C against the measured ESP chain "
            "from the physical A bytes",
        circ="the replay reads only objdump output and EXE bytes; no expected "
             "result is fed into the derivation",
        fail="control M2 (displacement 0x38) correctly yields source [E], and "
             "control M1 (SUB 0x18) correctly yields source [E+8] under the "
             "altered frame: the checker discriminates"))
    claims.append(claim(
        "A-6", "ARGUMENT_DELIVERY",
        "Entry-slot value preservation: no write touches [E+4] in "
        "[0x00528E50,0x00528E84): 8 stack writes (E-4, E-8, E-0xC, E-0x2C, "
        "E-0x30, E-0x34, E-0x38 via pushes; E-0x28 via the [esp+0x10] store) "
        "and 1 segment write (FS:[0]) are enumerated; none has delta +4; the "
        "entry-slot value therefore reaches the load unchanged.",
        "0x00528E50..0x00528E84", "A", "all writes enumerated in "
        "ENTRY_FRAME_LEDGER.csv", "writes: 8 stack (all deltas <= -4) + 1 segment",
        "QUALIFIED", ["AS4 (segment write is not a stack alias)"],
        "aliasing by unmodeled hardware events is out of static scope",
        measured="write census: zero writes to delta +4 before the load",
        ist="per-instruction write log replayed from the decoded stream",
        circ="the write log is derived from bytes, not from the hypothesis",
        fail="any write at delta +4 before 0x00528E84 would flip "
             "entry_slot_value_preserved and fail the gate"))
    claims.append(claim(
        "A-7", "ARGUMENT_DELIVERY",
        "EDI preservation: EDI's reaching definition at PUSH EDI 0x00528E8A "
        "is the load @0x00528E84; the two intervening instructions "
        "(push eax @0x00528E88, push ecx @0x00528E89) do not write EDI.",
        "0x00528E84..0x00528E8A", "A",
        "push eax / push ecx / push edi", "EDI def unchanged 0x00528E84 -> 0x00528E8A",
        "QUALIFIED", [],
        "none",
        measured="reg_defs['edi'] at the push == 0x00528E84",
        ist="register-definition tracking over the decoded stream",
        circ="derived from bytes; independent of the expected hypothesis",
        fail="any EDI write between load and push fails the gate"))
    claims.append(claim(
        "A-8", "ARGUMENT_DELIVERY",
        "Delivery at CALL 0x00528E8D: ESP before the call = E-0x44 = S-0xC "
        "(three net pushes after S); hardware return-address push -> callee "
        "entry ESP = E-0x48 = S-0x10; first explicit stack argument slot = "
        "[S-0xC] = [E-0x44], written by PUSH EDI @0x00528E8A with the value "
        "loaded from [E+4]; receiver ECX = entry ECX via ESI (separate "
        "channel).", "0x00528E8D", "A", "call 0x85b1b0 (e8 1e 23 33 00)",
        "ESP before=E-0x44=S-0xC; entry ESP=E-0x48=S-0x10; arg1 slot [S-0xC]",
        "QUALIFIED", ["AS1", "AS2"],
        "delivery at entry does not require the callee to return",
        measured="esp_before=-0x44; callee entry=-0x48; arg1 slot=[S-0xC]",
        ist="ESP chain from the decoded push sequence + hardware call push",
        circ="byte-derived; cross-checked with the prior pinned result "
             "ARG1_PROVENANCE.json (S-0xC / S-0x10 / [S-0x3C] source)",
        fail="the M4-style last-push change (control M4 in B) shows the "
             "checker rejects an arg1 that is not the last pushed value"))
    claims.append(claim(
        "B-1", "OBSERVED_STATIC_OPERATION",
        "Opaque-call sequence @0x004C4792..0x004C479F: push 0x128; CALL "
        "0x0095D3C4 (rel32 verified from bytes); add esp,0x4; "
        "mov [esp+0x44],eax. The callee 0x0095D3C4 is treated as opaque: no "
        "body, no heap-origin claim, no allocator-wide semantics. Recorded "
        "normal ABI-compatible return condition (AS3): pops exactly its "
        "return address (ESP restored), return value in EAX. Under AS3, "
        "T = ESP at 0x004C47AF equals the window-start ESP (T0).",
        "0x004C4792..0x004C47AF", "B",
        "push 0x128 / call 0x95d3c4 / add esp,0x4 / mov DWORD PTR [esp+0x44],eax",
        "T0-4 during the argument; T0 restored; T := T0 measured",
        "QUALIFIED_CONDITIONAL_ON_AS3", ["AS3"],
        "if AS3 is unsupported the Phase-B result stays conditional/unresolved; "
        "the callee is NOT opened to verify it"))
    claims.append(claim(
        "B-2", "OBSERVED_STATIC_OPERATION",
        "Flags TEST->JE: TEST EAX,EAX @0x004C47A3 defines ZF := (EAX==0); the "
        "only intervening instruction mov DWORD PTR [esp+0x3c],0x0 "
        "@0x004C47A5 writes no flags; therefore the JE @0x004C47AD branches "
        "precisely on EAX==0 (the opaque return value), and its target "
        "0x004C47C8 lies OUTSIDE window B and is not opened.",
        "0x004C47A3..0x004C47AD", "B",
        "test eax,eax / mov DWORD PTR [esp+0x3c],0x0 / je 0x4c47c8",
        "flag writers between TEST and JE: none (census)",
        "QUALIFIED", [],
        "the out-of-window branch target is not interpreted",
        measured="flag-writer census between 0x004C47A3 and 0x004C47AD = empty",
        ist="per-instruction flag-writer log from the decoded stream",
        circ="derived from decoded MOV flag semantics, not from the hypothesis",
        fail="a flag-writing instruction between TEST and JE would flip "
             "flags_preserved_test_to_je and fail the gate"))
    claims.append(claim(
        "B-3", "ARGUMENT_DELIVERY",
        "Qualified branch (EAX!=0, normal opaque return): loads ECX:=[T+0x50], "
        "EDX:=[T+0x4C]; pushes ECX, EDX, ESI -> ESP = T-0xC; LEA ECX,[ESP+0x14] "
        "@0x004C47BA computes ECX = ADDRESS(T-0xC+0x14) = ADDRESS(T+8), "
        "kind=ADDRESS (opcode 8D LEA: a computed address, not a memory read); "
        "PUSH ECX @0x004C47BE -> [T-0x10] := ADDRESS(T+8); MOV ECX,EAX "
        "@0x004C47BF -> receiver = the opaque return value.",
        "0x004C47AF..0x004C47BF", "B",
        "mov ecx,[esp+0x50] / mov edx,[esp+0x4c] / push ecx / push edx / push esi / "
        "lea ecx,[esp+0x14] / push ecx / mov ecx,eax",
        "ESP T-0x0 -> T-0x10; LEA input ESP=T-0xC",
        "QUALIFIED (EAX!=0 branch only)",
        ["AS3", "EAX!=0 at 0x004C47AD"],
        "ESI's producer is outside window B and remains unknown",
        measured="LEA result = ADDRESS(T+8); final arg slot [T-0x10]",
        ist="byte-decoded LEA displacement 0x14 against the measured ESP "
            "chain T-0xC",
        circ="replay reads only objdump output and EXE bytes; M3/M9 controls "
             "prove the checker discriminates displacement and LEA/MOV kind",
        fail="M3 (disp 0x18 -> ADDRESS(T+0xC)) and M9 (8D->8B, MEM kind) are "
             "correctly rejected as different facts"))
    claims.append(claim(
        "B-4", "ARGUMENT_DELIVERY",
        "CALL 0x00528E50 @0x004C47C1 (E8 8A 46 06 00; rel32 recompute "
        "0x004C47C6 + 0x0006468A = 0x00528E50 matches objdump): ESP before "
        "the call = T-0x10; hardware return-address push -> callee entry ESP "
        "= T-0x14 =: E; entry arg1 slot [E+4] = [T-0x10] contains "
        "ADDRESS(T+8) -- the ADDRESS value, NOT DWORD [T+8] (pointee contents "
        "not read).", "0x004C47C1", "B", "call 0x528e50",
        "ESP before=T-0x10; entry ESP=T-0x14; arg1 slot [T-0x10]",
        "QUALIFIED (EAX!=0 branch only)", ["AS1", "AS2", "AS3", "EAX!=0"],
        "no claim about [T+8] contents, type, lifetime or frame layout",
        measured="callee entry ESP = T-0x14; arg1 slot value kind=ADDRESS",
        ist="rel32 recompute from the physical bytes + ESP chain",
        circ="M8 control (rel32 +1) shows the checker computes the actual "
             "target from bytes and rejects the wrong bridge",
        fail="M8 (target 0x00528E51) correctly yields bridge_valid=False"))
    claims.append(claim(
        "B-5", "ARGUMENT_DELIVERY",
        "Null branch (EAX==0): ZF=1 -> JE taken -> control exits window B at "
        "0x004C47C8 (outside); the constructor CALL 0x004C47C1 is NOT "
        "reached on this path; NO delivery is fabricated. No claim is made "
        "about the out-of-window branch and no allocation success is "
        "asserted.", "0x004C47AD", "B", "je 0x4c47c8",
        "exit path ends outside the window; call_reached=False",
        "QUALIFIED_AS_NO_DELIVERY", [],
        "out-of-window behavior unknown and unexamined"))
    claims.append(claim(
        "BR-1", "POINTER_VALUE_IDENTITY",
        "Cross-call bridge (CROSS_CALL_IDENTITY): joining by E = T-0x14 "
        "(the callee-entry ESP measured in Phase B), the Phase-A source slot "
        "[E+4] is the SAME slot as the Phase-B prepared arg1 slot [T-0x10] "
        "(slot-address identity), and no write touches that slot between the "
        "B-side write @0x004C47BE and the A-side load @0x00528E84 (the "
        "hardware return-address push writes [T-0x14]; all A-side writes are "
        "at or below [T-0x18]; the only writes above T are the two B-side "
        "caller-frame stores at [T+0x3C] and [T+0x44]). Therefore the SAME "
        "pointer value ADDRESS(T+8) is (1) delivered as arg1 of FUN_00528E50 "
        "at CALL 0x004C47C1 and (2) loaded into EDI @0x00528E84, preserved, "
        "and delivered as arg1 of FUN_0085B1B0 at CALL 0x00528E8D.",
        "0x004C47BE / 0x00528E84", "B->A",
        "push ecx (4c47be) ... mov edi,[esp+0x3c] (528e84)",
        "joined slot [T-0x10]; value ADDRESS(T+8) both sides",
        join["status"],
        join.get("conditions", []),
        "conditional on AS1/AS2/AS3/AS4/AS5 and the EAX!=0 branch; no claim "
        "about the pointee area at [T+8], no type/lifetime/history claim, no "
        "global uniqueness across unexamined callers",
        measured="slot identity + zero intervening writes to the joined slot",
        ist="independent write-log census of both replays in T terms",
        circ="the census is byte-derived; the artifact controls AC1/AC2 "
             "prove the final gate rejects a mutated kind or slot claim",
        fail="any write to [T-0x10] between 0x004C47BE and 0x00528E84 "
             "would be enumerated and would reject the bridge"))
    claims.append(claim(
        "BR-2", "FINAL_SEMANTIC_ROLE",
        "The qualified relation is a POINTER_VALUE_IDENTITY across two "
        "delivery boundaries only. FIELD_SEMANTICS = UNVERIFIED; "
        "POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM; "
        "WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT = "
        "NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.",
        "-", "-", "no promotion performed", "n/a",
        "NOT_PERFORMED (scope fence)", [],
        "this run does not interpret the pointee, its type, or any world "
        "semantics"))

    doc = {
        "run_id": RUN_ID,
        "run_class": "BOUNDED_STATIC_ARGUMENT_PROVENANCE",
        "tool": tool_ver,
        "windows": window_ids,
        "phase_a": {
            "entry_esp_symbol": "E",
            "entry_va": "0x00528E50",
            "pivot_S": {"va": va_str(PIVOT_S_VA),
                        "esp_expr": esp_expr("E", af["S_delta"]),
                        "esp_delta_from_E": af["S_delta"]},
            "source_slot": {
                "load_va": af["source_load_va"],
                "load_expr": "mov edi,DWORD PTR [esp+0x3c]",
                "slot_expr_from_E": af["source_slot_expr"],
                "slot_expr_from_S": af["source_pivot_expr"],
                "slot_delta_from_E": af["source_slot_delta"],
            },
            "preservation": {
                "entry_slot_value_preserved_to_load":
                    af["entry_slot_value_preserved"],
                "writes_before_load": af["writes_before_source_load"],
                "segment_writes_before_load":
                    af["segment_writes_before_source_load"],
                "aliasing_writes_to_source_slot":
                    af["aliasing_writes_to_source_slot"],
                "edi_preserved_to_push": af["edi_preserved"],
                "edi_reaching_def_at_push": af["edi_reaching_def_at_push"],
            },
            "delivery": {
                "tail_call_va": af["tail_call_va"],
                "tail_target": af["tail_target"],
                "esp_before_call": af["esp_before_tail_call"],
                "esp_before_call_S": af["esp_before_tail_call_S"],
                "callee_entry_esp": af["callee_entry_esp"],
                "callee_entry_esp_S": af["callee_entry_esp_S"],
                "arg1_slot": af["arg1_slot_expr"],
                "arg1_slot_S": af["arg1_slot_expr_S"],
                "arg1_value_kind": af["arg1_value_kind"],
                "arg1_value_expr": "MEM(E+0x4)@%s" % af["source_load_va"],
            },
            "receiver": {
                "expr": af["receiver_expr"], "kind": af["receiver_kind"],
                "channel": "ECX via ESI (mov esi,ecx @0x00528E76; "
                           "mov ecx,esi @0x00528E8B); separate from arg1",
            },
        },
        "phase_b": jsonable_b_facts(b_facts),
        "bridge": join,
        "claims": claims,
    }
    return doc


# ---------------------------------------------------------------- artifact gate

def independent_esp_walk(instrs, opaque_target, va_start):
    """Independent minimal ESP arithmetic walk (separate from the replay
    engine): returns esp delta per instruction VA. Handles push (=-4),
    sub/add esp imm, opaque call (AS3 net 0), conditional branch (records and
    CONTINUES on the qualified fall-through path), stops at a boundary call or
    an unconditional jump."""
    esp = 0
    per_va = {}
    for ins in instrs:
        mn, ops = ins.mnemonic, ins.operands
        o = [x.strip() for x in ops.split(",")] if ops else []
        if mn == "push":
            esp -= 4
        elif mn == "sub" and o[0] == "esp":
            esp -= int(o[1], 16)
        elif mn == "add" and o[0] == "esp":
            esp += int(o[1], 16)
        elif mn == "call":
            tgt = int(o[0], 16)
            if tgt == opaque_target:
                pass          # AS3: ret push (-4) then pop (+4): net 0
            else:
                per_va[ins.va] = esp       # esp BEFORE the boundary call
                return per_va, esp, ins.va
        elif mn == "jmp":
            per_va[ins.va] = esp
            return per_va, esp, ins.va
        # je/jne: record and continue on the fall-through path
        per_va[ins.va] = esp
    return per_va, esp, None


def load_ledger_csv(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def esp_expr_to_delta(expr):
    """'E-0x38' / 'T0-0xc' / 'T-0x10' / 'E' / 'T0' -> signed int."""
    expr = expr.strip()
    for base in ("E", "T0", "T", "S"):
        if expr == base:
            return 0
        if expr.startswith(base):
            expr = expr[len(base):]
            break
    expr = expr.strip()
    if not expr:
        return 0
    m = re.match(r"^([+-])?0x([0-9a-f]+)$", expr)
    if not m:
        raise Unresolved("cannot parse ESP expression: " + expr)
    v = int(m.group(2), 16)
    return -v if (m.group(1) == "-") else v


def gate_artifacts(repo_out, prov_path_override=None):
    """The ordinary final gate: re-read the persisted load-bearing artifacts
    (WINDOW_IDENTITIES.json, ENTRY_FRAME_LEDGER.csv, CALLER_STACK_LEDGER.csv,
    BRIDGE_PROVENANCE.json) and compare their FACTS to independently
    re-derived evidence (physical window bytes, re-parsed persisted objdump
    text, independent ESP walk). Returns (checks, verdict)."""
    checks = []

    def chk(cid, fact, claimed, actual, ok):
        checks.append({"check": cid, "fact": fact,
                       "claimed": claimed, "actual": actual, "pass": ok})

    # 1) physical window identity vs WINDOW_IDENTITIES.json
    with open(os.path.join(repo_out, "WINDOW_IDENTITIES.json")) as fh:
        wids = json.load(fh)
    for key in ("A", "B"):
        phys = read_exe_window(EXE_PATH, WINDOWS[key])
        sh = sha256_bytes(phys)
        c = wids["windows"][key]
        chk("WID-%s-SHA" % key, "window SHA256 vs physical EXE bytes",
            c["sha256"], sh, c["sha256"] == sh)
        chk("WID-%s-SIZE" % key, "window size", c["size"], len(phys),
            c["size"] == len(phys))
        chk("WID-%s-INTERVAL" % key, "window interval",
            c["interval"], "[%s,%s)" % (va_str(WINDOWS[key]["va_start"]),
                                         va_str(WINDOWS[key]["va_start"]
                                                + WINDOWS[key]["size"])),
            c["va_start"] == va_str(WINDOWS[key]["va_start"])
            and c["va_end_exclusive"] == va_str(WINDOWS[key]["va_start"]
                                              + WINDOWS[key]["size"]))

    # 2) re-parse the persisted raw objdump text (physical evidence)
    instrs = {}
    for key in ("A", "B"):
        with open(os.path.join(repo_out, WINDOWS[key]["raw_text"])) as fh:
            raw = fh.read()
        body = raw.split("--- RAW OUTPUT BELOW ---", 1)[1]
        instrs[key] = parse_objdump(body, WINDOWS[key]["va_start"],
                                    WINDOWS[key]["va_start"]
                                    + WINDOWS[key]["size"])

    # 3) independent ESP walks
    espA, espA_end, vaA_end = independent_esp_walk(instrs["A"], OPAQUE_CALLEE,
                                                  WINDOWS["A"]["va_start"])
    espB, espB_end, vaB_end = independent_esp_walk(instrs["B"], OPAQUE_CALLEE,
                                                  WINDOWS["B"]["va_start"])

    # 4) ENTRY_FRAME_LEDGER.csv row-by-row vs re-parsed persisted objdump text
    efl = load_ledger_csv(os.path.join(repo_out, "ENTRY_FRAME_LEDGER.csv"))
    by_va = {ins.va: ins for ins in instrs["A"]}
    ok_rows = len(efl) == len(instrs["A"])
    for row in efl:
        va = int(row["VA"], 16)
        ins = by_va.get(va)
        if ins is None:
            ok_rows = False
            continue
        if row["BYTES"] != " ".join(ins.bytes_hex) or row["DECODED_OP"] != ins.text:
            ok_rows = False
        if ins.mnemonic == "call":
            # boundary call: the independent walk records ESP BEFORE the
            # hardware return-address push; the ledger ESP_AFTER includes it
            if (esp_expr_to_delta(row["ESP_BEFORE"]) != espA[va]
                    or esp_expr_to_delta(row["ESP_AFTER"]) != espA[va] - 4):
                ok_rows = False
        elif esp_expr_to_delta(row["ESP_AFTER"]) != espA[va]:
            ok_rows = False
    chk("EFL-ROWS", "ledger rows vs persisted objdump text + independent "
        "ESP walk", "%d rows" % len(efl), "%d instructions" % len(instrs["A"]),
        ok_rows)
    chk("EFL-ESP-S", "S = ESP at 0x00528E76 (independent walk)",
        espA.get(PIVOT_S_VA), -0x38, espA.get(PIVOT_S_VA) == -0x38)
    chk("EFL-ESP-BEFORE-CALL", "ESP before tail call 0x00528E8D",
        espA.get(TAIL_CALL_VA), -0x44, espA.get(TAIL_CALL_VA) == -0x44)

    # 5) CALLER_STACK_LEDGER.csv rows
    csl = load_ledger_csv(os.path.join(repo_out, "CALLER_STACK_LEDGER.csv"))
    by_va_b = {ins.va: ins for ins in instrs["B"]}
    ok_rows_b = True
    seen_nonnull = 0
    for row in csl:
        va = int(row["VA"], 16)
        ins = by_va_b.get(va)
        if ins is None:
            ok_rows_b = False
            continue
        if row["BYTES"] != " ".join(ins.bytes_hex) or row["DECODED_OP"] != ins.text:
            ok_rows_b = False
        if row["PATH"] == "NONNULL":
            seen_nonnull += 1
            is_boundary_call = (ins.mnemonic == "call"
                                and int(ins.operands.strip(), 16)
                                != OPAQUE_CALLEE)
            if is_boundary_call:
                # boundary call: walk value is ESP BEFORE the return push
                if (esp_expr_to_delta(row["ESP_BEFORE"]) != espB[va]
                        or esp_expr_to_delta(row["ESP_AFTER"]) != espB[va] - 4):
                    ok_rows_b = False
            elif esp_expr_to_delta(row["ESP_AFTER"]) != espB[va]:
                ok_rows_b = False
    chk("CSL-ROWS", "caller ledger rows vs persisted objdump text + "
        "independent ESP walk", "%d rows" % len(csl),
        "nonnull rows=%d" % seen_nonnull, ok_rows_b)
    chk("CSL-ESP-T", "T = ESP at 0x004C47AF (independent walk)",
        espB.get(PIVOT_T_VA), 0, espB.get(PIVOT_T_VA) == 0)
    chk("CSL-ESP-BEFORE-BRIDGE", "ESP before bridge call 0x004C47C1",
        espB.get(BRIDGE_CALL_VA), -0x10, espB.get(BRIDGE_CALL_VA) == -0x10)

    # 6) BRIDGE_PROVENANCE.json fact checks (independent re-derivation)
    prov_path = prov_path_override or os.path.join(repo_out,
                                                  "BRIDGE_PROVENANCE.json")
    with open(prov_path) as fh:
        prov = json.load(fh)
    pa = prov["phase_a"]
    pb = prov["phase_b"]
    nn = pb.get("nonnull_path") or {}
    br = prov["bridge"]

    # 6a) A source slot: bytes 8b 7c 24 3c at 0x00528E84 + S=-0x38 -> [E+4]
    src_ins = by_va.get(SOURCE_LOAD_VA)
    src_disp = int.from_bytes(bytes(int(b, 16) for b in src_ins.bytes_hex[3:4]),
                             "little")
    src_delta_rederived = espA[PIVOT_S_VA] + src_disp
    chk("PROV-A-SLOT", "clean entry source slot (bytes 0x3c disp + S)",
        pa["source_slot"]["slot_expr_from_E"],
        slot_expr("E", src_delta_rederived),
        pa["source_slot"]["slot_expr_from_E"]
        == slot_expr("E", src_delta_rederived)
        and pa["source_slot"]["slot_delta_from_E"] == src_delta_rederived)

    # 6b) A delivery deltas
    chk("PROV-A-DELIVERY", "tail call delivery ESP facts",
        (pa["delivery"]["esp_before_call"], pa["delivery"]["callee_entry_esp"]),
        ("E-0x44", "E-0x48"),
        pa["delivery"]["esp_before_call"] == "E-0x44"
        and pa["delivery"]["callee_entry_esp"] == "E-0x48")

    # 6c) B LEA kind: byte evidence at 0x004C47BA
    lea_ins = by_va_b.get(LEA_VA)
    lea_op = lea_ins.bytes_hex[0]
    arg1_kind_claimed = nn.get("arg1", {}).get("value_kind")
    kind_from_opcode = "ADDRESS" if lea_op == "8d" else "STACK_READ" \
        if lea_op == "8b" else "UNKNOWN"
    chk("PROV-B-ARG1-KIND", "arg1 value kind vs LEA/MOV opcode byte 0x%02X "
        "at 0x004C47BA (address-vs-MEM kind)" % int(lea_op, 16),
        arg1_kind_claimed, kind_from_opcode,
        arg1_kind_claimed == kind_from_opcode == "ADDRESS")

    # 6d) B arg1 expression: LEA disp 0x14 + ESP=T-0xC -> ADDRESS(T+8)
    lea_disp = int.from_bytes(bytes(int(b, 16) for b in lea_ins.bytes_hex[3:4]),
                             "little")
    esp_at_lea = espB[LEA_VA]
    lea_result_T = esp_at_lea + lea_disp - espB[PIVOT_T_VA]
    claimed_expr = nn.get("arg1", {}).get("value_expr") or br.get(
        "b_arg1_value_expr")
    rederived = "ADDRESS(T%s)" % ("" if lea_result_T == 0 else
                                  ("+" if lea_result_T > 0 else "-")
                                  + "0x%x" % abs(lea_result_T))
    chk("PROV-B-LEA-EXPR", "LEA result expression (bytes 0x%02x disp + "
        "independent ESP)" % lea_disp, claimed_expr, rederived,
        claimed_expr == rederived)

    # 6e) entry-slot identity: [E+4] == [T-0x10] under E=T-0x14
    e_join = espB[BRIDGE_CALL_VA] - 4 - espB[PIVOT_T_VA]   # E delta from T
    joined = e_join + src_delta_rederived
    b_slot = espB[BRIDGE_CALL_VA] - espB[PIVOT_T_VA]
    chk("PROV-BRIDGE-SLOT", "joined entry-slot identity [E+4]==[T-0x10]",
        br["a_source_slot_from_T"], slot_expr("T", joined),
        br["a_source_slot_from_T"] == slot_expr("T", joined)
        and joined == b_slot)

    # 6f) call targets from provenance vs rel32 recompute from the raw bytes
    expected_targets = {va_str(TAIL_CALL_VA): va_str(TAIL_CALLEE),
                        va_str(0x4C4797): va_str(OPAQUE_CALLEE),
                        va_str(BRIDGE_CALL_VA): va_str(BRIDGE_CALLEE)}
    for win in ("A", "B"):
        for ins in instrs[win]:
            if ins.mnemonic != "call":
                continue
            tgt = int(ins.operands.strip(), 16)
            rel = int.from_bytes(bytes(int(b, 16)
                                       for b in ins.bytes_hex[1:5]),
                                 "little", signed=True)
            ok = (ins.va + 5 + rel == tgt
                  and expected_targets.get(va_str(ins.va)) == va_str(tgt))
            chk("PROV-CALL-%s-%s" % (win, va_str(ins.va)),
                "call target at %s (rel32 recompute + pinned role)"
                % va_str(ins.va),
                expected_targets.get(va_str(ins.va)), va_str(tgt), ok)

    # 6g) flags survive TEST->JE (independent: MOV store writes no flags)
    between = [ins for ins in instrs["B"]
               if 0x4C47A3 < ins.va < 0x4C47AD and ins.mnemonic != "mov"]
    chk("PROV-B-FLAGS", "no non-MOV (flag-writing) instruction between "
        "TEST and JE", [], [i.text for i in between], len(between) == 0)

    verdict = "PASS" if all(c["pass"] for c in checks) else "REJECTED"
    return checks, verdict


# ---------------------------------------------------------------- mode mains

def mode_windows(args):
    repo_out = args.repo_out
    workdir = args.workdir
    os.makedirs(os.path.join(repo_out, "01_RAW"), exist_ok=True)
    os.makedirs(os.path.join(workdir, "retry"), exist_ok=True)
    exe_sha = sha256_file(EXE_PATH)
    if exe_sha != EXE_SHA256:
        raise Unresolved("EXE SHA256 mismatch: " + exe_sha)
    ver, rc = objdump_version()
    tool_header = ("Tool: %s\nWSL distro: PE-AI (Debian; kernel "
                   "6.18.33.2-microsoft-standard-WSL2)\n" % ver)
    window_ids = {"run_id": RUN_ID,
                  "exe": {"path": EXE_PATH, "size": EXE_SIZE,
                          "sha256": exe_sha, "image_base": va_str(IMAGE_BASE),
                          "read_scope": "whole-file hash + PE header/section "
                                        "mapping + the two pinned window byte "
                                        "ranges only"},
                  "tool": {"name": ver, "rc": rc,
                           "command_form": "objdump -D -b binary -m i386 "
                                           "-M intel --adjust-vma=<VA> "
                                           "<fixture.bin>"}}
    results = {}
    for key in ("A", "B"):
        win = WINDOWS[key]
        phys = read_exe_window(EXE_PATH, win)
        sh = sha256_bytes(phys)
        if sh != win["sha256"]:
            raise Unresolved("window %s SHA mismatch" % key)
        fix = os.path.join(workdir, "retry",
                           "window_%s_original.bin" % key)
        with open(fix, "wb") as fh:
            fh.write(phys)
        rc, out, cmd = run_objdump(fix, win["va_start"])
        retry_rel = "01_RAW/WINDOW_%s_OBJDUMP_RETRY.txt" % key
        with open(os.path.join(repo_out, retry_rel), "w") as fh:
            fh.write(tool_header)
            fh.write("Session: fresh retry verification (crash continuation; "
                     "see PREREGISTRATION.md P10)\n")
            fh.write("Command: %s\n" % cmd.replace(fix, os.path.basename(fix)))
            fh.write("Input fixture: %s (size %d, SHA256 %s)\n"
                     % (os.path.basename(fix), len(phys), sh))
            fh.write("Exit status: %d\n" % rc)
            fh.write("--- RAW OUTPUT BELOW ---\n\n")
            fh.write(out)
        instrs = parse_objdump(out, win["va_start"],
                               win["va_start"] + win["size"])
        calls = [{"va": va_str(i.va), "target": i.operands.strip(),
                  "bytes": " ".join(i.bytes_hex)}
                 for i in instrs if i.mnemonic == "call"]
        window_ids["windows"] = window_ids.get("windows", {})
        window_ids["windows"][key] = {
            "va_start": va_str(win["va_start"]),
            "va_end_exclusive": va_str(win["va_start"] + win["size"]),
            "interval": "[%s,%s)" % (va_str(win["va_start"]),
                                     va_str(win["va_start"] + win["size"])),
            "size": win["size"],
            "raw_offset": win["raw_offset"],
            "raw_offset_hex": "0x%x" % win["raw_offset"],
            "sha256": sh,
            "sha256_matches_contract_pin": True,
            "pe_mapping": {
                "section": ".text",
                "section_rva_range": "[0x1000,0x6745E5)",
                "section_raw_backed": True,
                "raw_range": "[0x1000,0x675000)",
                "unique_mapping": True,
                "note": "RVA = VA - ImageBase; raw offset = RVA for .text "
                        "(PointerToRawData == VirtualAddress == 0x1000)",
            },
            "decode": {
                "instructions": len(instrs),
                "covers_window_exactly": True,
                "first_va": va_str(instrs[0].va),
                "last_instruction_va": va_str(instrs[-1].va),
                "last_instruction_end": va_str(instrs[-1].va
                                                + instrs[-1].nbytes),
                "visible_calls": calls,
            },
            "raw_text_file": win["raw_text"],
            "retry_raw_text_file": retry_rel,
            "objdump_rc": rc,
        }
        # compare the fresh disassembly with the crashed session's persisted file
        with open(os.path.join(repo_out, win["raw_text"])) as fh:
            persisted = fh.read()
        old_body = persisted.split("--- RAW OUTPUT BELOW ---", 1)[1]
        old_lines = [l.rstrip() for l in old_body.splitlines()
                     if re.match(r"^\s+[0-9a-f]+:", l)]
        new_lines = [l.rstrip() for l in out.splitlines()
                     if re.match(r"^\s+[0-9a-f]+:", l)]
        results[key] = {
            "persisted_raw_file": win["raw_text"],
            "fresh_retry_file": retry_rel,
            "disassembly_lines_identical": old_lines == new_lines,
            "old_line_count": len(old_lines),
            "new_line_count": len(new_lines),
        }
    window_ids["crash_continuation_verification"] = results
    with open(os.path.join(repo_out, "WINDOW_IDENTITIES.json"), "w") as fh:
        json.dump(window_ids, fh, indent=2)
    return results


def mode_replay(args):
    repo_out = args.repo_out
    ver, rc = objdump_version()
    instrs = {}
    for key in ("A", "B"):
        with open(os.path.join(repo_out, WINDOWS[key]["raw_text"])) as fh:
            raw = fh.read()
        body = raw.split("--- RAW OUTPUT BELOW ---", 1)[1]
        instrs[key] = parse_objdump(body, WINDOWS[key]["va_start"],
                                   WINDOWS[key]["va_start"]
                                   + WINDOWS[key]["size"])
    a_facts, a_path = derive_a(instrs["A"])
    b_facts, b_paths = derive_b(instrs["B"])
    join = bridge_join(a_facts, b_facts)
    n1 = write_entry_frame_ledger(os.path.join(repo_out,
                                               "ENTRY_FRAME_LEDGER.csv"),
                                  a_path, a_facts)
    n2 = write_caller_ledger(os.path.join(repo_out, "CALLER_STACK_LEDGER.csv"),
                             b_paths, b_facts)
    with open(os.path.join(repo_out, "WINDOW_IDENTITIES.json")) as fh:
        wids = json.load(fh)
    prov = build_bridge_provenance(a_facts, a_path, b_facts, b_paths, join,
                                   {"name": ver, "rc": rc}, wids)
    with open(os.path.join(repo_out, "BRIDGE_PROVENANCE.json"), "w") as fh:
        json.dump(prov, fh, indent=2)
    return {"entry_frame_ledger_rows": n1, "caller_ledger_rows": n2,
            "join_status": join["status"],
            "S_delta": a_facts["S_delta"],
            "source_slot_delta": a_facts["source_slot_delta"],
            "T_delta": b_facts["nonnull_path"]["T_delta"]}


def mode_controls(args):
    repo_out = args.repo_out
    workdir = args.workdir
    os.makedirs(os.path.join(repo_out, "01_RAW", "CONTROLS"), exist_ok=True)
    ver, rc = objdump_version()
    tool_header = "Tool: %s\n" % ver
    cases = []
    for case in CASE_ORDER:
        try:
            rec = run_case(case, repo_out, workdir, tool_header)
        except Unresolved as e:
            rec = {"case": case, "verdict": "UNRESOLVED",
                   "reason": str(e),
                   "note": "fail-closed: unsupported construct; the expected "
                           "result was NOT filled in"}
        cases.append(rec)
    summary = {
        "run_id": RUN_ID,
        "produced_by": "03_SCRIPTS/run_frame_bridge.py controls (production side)",
        "tool": {"name": ver, "rc": rc},
        "matrix_total_expected": 24,
        "production_case_count": len(cases),
        "fresh_qc_side": "NOT_PERFORMED_BY_THIS_WORKER (separate fresh-QC "
                         "worker per dispatch; never invented)",
        "cases": cases,
    }
    n_pass = sum(1 for c in cases if c.get("verdict") == "CONTROL_PASS")
    n_fail = sum(1 for c in cases if c.get("verdict") == "CONTROL_FAIL")
    n_unres = sum(1 for c in cases if c.get("verdict") == "UNRESOLVED")
    summary["summary"] = {"cases": len(cases), "control_pass": n_pass,
                          "control_fail": n_fail, "unresolved": n_unres}
    with open(os.path.join(repo_out, "CONTROL_RESULTS.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    # CLAIM_MATRIX.csv: 12 production + 12 fresh-QC expected outcomes
    with open(os.path.join(repo_out, "CLAIM_MATRIX.csv"), "w",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["CASE", "SIDE", "EXPECTED_DISCRIMINATING_RESULT",
                    "ACTUAL_OUTCOME", "VERDICT", "EVIDENCE_REF"])
        for c in cases:
            w.writerow([c["case"], "PRODUCTION", EXPECTED[c["case"]]["text"],
                        json.dumps(c.get("derived_facts", c.get("reason")),
                                   sort_keys=True),
                        c.get("verdict"),
                        "01_RAW/CONTROLS/%s_OBJDUMP.txt" % c["case"]])
        for case in CASE_ORDER:
            w.writerow([case, "QC_FRESH", EXPECTED[case]["text"],
                        "NOT_PERFORMED_BY_THIS_WORKER",
                        "NOT_PERFORMED_BY_THIS_WORKER",
                        "(fresh-QC worker phase; separate session)"])
    return summary["summary"]


def mode_artifact_gate(args):
    repo_out = args.repo_out
    workdir = args.workdir
    results = {}
    checks, verdict = gate_artifacts(repo_out)
    results["baseline"] = {
        "description": "re-read of persisted load-bearing artifacts through "
                       "the ordinary final gate; facts compared to physical "
                       "bytes / persisted objdump text / independent ESP walk",
        "artifact_set": {"WINDOW_IDENTITIES.json": "persisted",
                         "ENTRY_FRAME_LEDGER.csv": "persisted",
                         "CALLER_STACK_LEDGER.csv": "persisted",
                         "BRIDGE_PROVENANCE.json": "persisted"},
        "checks": checks, "verdict": verdict,
    }
    if verdict != "PASS":
        results["overall"] = "BASELINE_FAILED_GATE_NOT_APPLIED_TO_CONTROLS"
        with open(os.path.join(repo_out, "ARTIFACT_CONTROL_RESULTS.json"),
                  "w") as fh:
            json.dump(results, fh, indent=2)
        return results
    # AC1: copied artifact with ADDRESS(T+8) -> MEM(T+8)
    import copy
    with open(os.path.join(repo_out, "BRIDGE_PROVENANCE.json")) as fh:
        prov = json.load(fh)
    ac_dir = os.path.join(workdir, "artifact_controls")
    os.makedirs(ac_dir, exist_ok=True)
    ac1 = copy.deepcopy(prov)
    ac1["phase_b"]["nonnull_path"]["arg1"]["value_kind"] = "STACK_READ"
    ac1["phase_b"]["nonnull_path"]["arg1"]["value_expr"] = "MEM(T+0x8)"
    ac1["bridge"]["b_arg1_value_kind"] = "STACK_READ"
    ac1["bridge"]["b_arg1_value_expr"] = "MEM(T+0x8)"
    if "cross_call_value_expr" in ac1["bridge"]:
        ac1["bridge"]["cross_call_value_expr"] = "MEM(T+0x8)"
    ac1_path = os.path.join(ac_dir, "BRIDGE_PROVENANCE_AC1.json")
    with open(ac1_path, "w") as fh:
        json.dump(ac1, fh, indent=2)
    c1, v1 = gate_artifacts(repo_out, prov_path_override=ac1_path)
    results["AC1"] = {
        "mutation": "copied BRIDGE_PROVENANCE.json with the clean arg1 value "
                    "kind/expression replaced: ADDRESS(T+8) -> MEM(T+8)",
        "expected": "REJECTED by the same ordinary final gate",
        "checks": c1, "verdict": v1,
        "result": "CONTROL_PASS" if v1 == "REJECTED" else "CONTROL_FAIL",
        "scope_note": "package hash/manifest checks are bypassed ONLY in "
                      "this isolated synthetic artifact control (it tests "
                      "the fact predicate itself); the persisted original is "
                      "never mutated; the mutated copy lives in the OS temp "
                      "dir outside Git",
    }
    # AC2: copied artifact with clean entry source [E+4] -> [E+8]
    ac2 = copy.deepcopy(prov)
    ac2["phase_a"]["source_slot"]["slot_expr_from_E"] = "[E+0x8]"
    ac2["phase_a"]["source_slot"]["slot_delta_from_E"] = 8
    ac2_path = os.path.join(ac_dir, "BRIDGE_PROVENANCE_AC2.json")
    with open(ac2_path, "w") as fh:
        json.dump(ac2, fh, indent=2)
    c2, v2 = gate_artifacts(repo_out, prov_path_override=ac2_path)
    results["AC2"] = {
        "mutation": "copied BRIDGE_PROVENANCE.json with the clean entry "
                    "source changed: [E+4] -> [E+8]",
        "expected": "REJECTED by the same ordinary final gate",
        "checks": c2, "verdict": v2,
        "result": "CONTROL_PASS" if v2 == "REJECTED" else "CONTROL_FAIL",
        "scope_note": "package hash/manifest checks are bypassed ONLY in "
                      "this isolated synthetic artifact control; the "
                      "persisted original is never mutated",
    }
    results["overall"] = ("ARTIFACT_CONSISTENCY_PASS"
                          if results["AC1"]["result"] == "CONTROL_PASS"
                          and results["AC2"]["result"] == "CONTROL_PASS"
                          else "ARTIFACT_CONTROL_FAILURE")
    with open(os.path.join(repo_out, "ARTIFACT_CONTROL_RESULTS.json"),
              "w") as fh:
        json.dump(results, fh, indent=2)
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("mode", choices=["windows", "replay", "controls",
                                     "artifact-gate", "all"])
    ap.add_argument("--repo-out", required=True)
    ap.add_argument("--workdir", required=True)
    args = ap.parse_args()
    args.repo_out = os.path.abspath(args.repo_out)
    args.workdir = os.path.abspath(args.workdir)
    os.makedirs(args.workdir, exist_ok=True)
    exe_sha = sha256_file(EXE_PATH)
    if exe_sha != EXE_SHA256:
        print("BLOCKED: EXE SHA256 mismatch: " + exe_sha)
        return 2
    print("EXE_SHA256_OK=%s" % exe_sha)
    if args.mode in ("windows", "all"):
        r = mode_windows(args)
        print("WINDOWS=" + json.dumps(r, sort_keys=True))
    if args.mode in ("replay", "all"):
        r = mode_replay(args)
        print("REPLAY=" + json.dumps(r, sort_keys=True))
    if args.mode in ("controls", "all"):
        r = mode_controls(args)
        print("CONTROLS=" + json.dumps(r, sort_keys=True))
    if args.mode in ("artifact-gate", "all"):
        r = mode_artifact_gate(args)
        print("ARTIFACT_GATE_OVERALL=" + str(r.get("overall")))
    exe_sha2 = sha256_file(EXE_PATH)
    print("EXE_SHA256_AFTER=%s EXE_UNCHANGED=%s" % (exe_sha2, exe_sha2 == EXE_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
