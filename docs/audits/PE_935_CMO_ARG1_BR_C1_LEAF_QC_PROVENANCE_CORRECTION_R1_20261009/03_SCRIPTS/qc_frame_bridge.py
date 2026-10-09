#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qc_frame_bridge.py — FRESH-CONTEXT INTERNAL QC (independent symbolic
implementation) for RUN_ID PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009.

QC_ORIGIN : pe-master-auditor fresh-context internal QC session (internal to
            PE-MASTER; NOT an independent Desktop post-audit; NOT executor
            self-review).
AUTHORED  : 2026-10-09. It does NOT import 03_SCRIPTS/run_frame_bridge.py and
            does NOT take the executor's ledgers or CONTROL_RESULTS.json as an
            input to any derivation; the expected discriminating results below
            were re-encoded directly from the dispatched contract section 7
            matrix by this QC session. The production artifacts are read ONLY
            for agree/disagree adjudication.

HONEST INDEPENDENCE STATEMENT:
  - window extraction / hashing / PE mapping : independent (this session)
  - disassembler : GNU objdump 2.44 via WSL PE-AI — the SAME disassembler as
    the production run; the same GNU objdump is NOT two independent
    disassemblers (stated honestly; not claimed as a cross-disassembler check)
  - objdump invocations : this session's own commands (rc recorded)
  - symbolic replay / ESP walk / derivation : this file's own implementation
  - artifact gate : this file's own implementation

EXE read scope of this QC: whole-file hash + PE header/section mapping + the
two pinned window byte ranges [0x00528E50,0x00528E92) and
[0x004C4792,0x004C47C6) ONLY. No other code is read or interpreted; callee
bodies 0x0085B1B0/0x0095D3C4 stay unopened; no upstream beyond window B; no
xrefs; no runtime; the EXE is never altered (fixtures are temp copies outside
Git, never staged).
"""

import copy
import csv
import hashlib
import json
import os
import re
import struct
import subprocess
import sys

# ------------------------------------------------------------------ pinned paths

EXE = "/mnt/d/Eudoria_Reconstruction/pcg_install/Entropia.exe"
EXE_SIZE_PIN = 8015872
EXE_SHA_PIN = ("e7785430e81dffe648ce8f5312414b17bc9fce61389689"
               "a22f753765d5280f31")

PKG = ("/mnt/d/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009")
WORK = ("/mnt/c/Users/User/AppData/Local/Temp/opencode/"
        "QC_PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009")

WIN = {
    "A": {"va": 0x00528E50, "size": 66, "raw": 1216080,
          "sha": ("f8735567340cd3be2f6b64b4bbc2be292487e97b61847"
                  "58ca408e6ff1ce78e85"),
          "raw_file": "01_RAW/WINDOW_A_OBJDUMP.txt",
          "retry_file": "01_RAW/WINDOW_A_OBJDUMP_RETRY.txt"},
    "B": {"va": 0x004C4792, "size": 52, "raw": 804754,
          "sha": ("b59e16dc116f4ce0438a1e92bc6b2cbc33fab0b19fab"
                  "c24cb3a29c911c1efb6a"),
          "raw_file": "01_RAW/WINDOW_B_OBJDUMP.txt",
          "retry_file": "01_RAW/WINDOW_B_OBJDUMP_RETRY.txt"},
}

OPAQUE_TARGET = 0x0095D3C4          # incidental opaque callsite 0x004C4797
BRIDGE_ENTRY = 0x00528E50           # window A entry (CALL 0x004C47C1 target)
TAIL_TARGET_PIN = 0x0085B1B0        # CALL 0x00528E8D target (prior pin)

# contract section 7 mutation table — re-encoded by this QC session from the
# CONTRACT text (byte positions in synthetic copies only; EXE never altered).
MUT = {
    "M1_A_FRAME":            dict(win="A", va=0x528E5E, orig="83 ec 1c", new="83 ec 18"),
    "M2_A_SLOT":             dict(win="A", va=0x528E84, orig="8b 7c 24 3c", new="8b 7c 24 38"),
    "M3_B_LEA_DISP":         dict(win="B", va=0x4C47BA, orig="8d 4c 24 14", new="8d 4c 24 18"),
    "M4_B_LAST_PUSH":        dict(win="B", va=0x4C47BE, orig="51", new="52"),
    "M5_B_EARLY_PUSH_ORDER": dict(win="B", va=0x4C47B7, orig="51 52", new="52 51"),
    "M6_B_SKIP":             dict(win="B", va=0x4C47AD, orig="74 19", new="eb 19"),
    "M7_B_RECEIVER_ONLY":    dict(win="B", va=0x4C47BF, orig="8b c8", new="8b ce"),
    "M8_B_WRONG_TARGET":     dict(win="B", va=0x4C47C1, orig="e8 8a 46 06 00", new="e8 8b 46 06 00"),
    "M9_B_LEA_TO_MOV":       dict(win="B", va=0x4C47BA, orig="8d 4c 24 14", new="8b 4c 24 14"),
}

CASE_ORDER = ["A_CLEAN", "B_CLEAN_NONNULL", "B_CLEAN_NULL", "M1_A_FRAME",
              "M2_A_SLOT", "M3_B_LEA_DISP", "M4_B_LAST_PUSH",
              "M5_B_EARLY_PUSH_ORDER", "M6_B_SKIP", "M7_B_RECEIVER_ONLY",
              "M8_B_WRONG_TARGET", "M9_B_LEA_TO_MOV"]

# Expected discriminating results — re-encoded from CONTRACT section 7.
# B-side arg exprs: (kind, offset_from_T); A-side offsets from E.
# KINDS used by THIS implementation: ADDR / MEM / OPRET / UNK / RECV.
EXP = {
    "A_CLEAN": dict(text="S=E-0x38; source [E+4]; value preserved/delivered",
                    S=-0x38, src=4, preserved=True, edi_ok=True,
                    tail=TAIL_TARGET_PIN, arg1_kind="MEM"),
    "B_CLEAN_NONNULL": dict(
        text="CALL reachable; arg1 ADDRESS(T+8); receiver = return value",
        T=0, reaches=True, arg1=("ADDR", 8), slot1=-0x10, a2="UNK",
        a3=("MEM", 0x4C), a4=("MEM", 0x50), recv="OPRET",
        target=BRIDGE_ENTRY, bvalid=True, flags_ok=True),
    "B_CLEAN_NULL": dict(
        text="JE taken; target CALL not reached; no fabricated delivery",
        je=True, call_reached=False, delivered_None=True),
    "M1_A_FRAME": dict(text="S=E-0x34; later source [E+8], not entry arg1 [E+4]",
                       S=-0x34, src=8),
    "M2_A_SLOT": dict(text="Source [E] under original frame, not [E+4]",
                      S=-0x38, src=0),
    "M3_B_LEA_DISP": dict(text="arg1 ADDRESS(T+0xC), not ADDRESS(T+8)",
                          arg1=("ADDR", 0xC)),
    "M4_B_LAST_PUSH": dict(
        text="arg1 is the earlier EDX load value MEM(T+0x4C), not the LEA address",
        arg1=("MEM", 0x4C)),
    "M5_B_EARLY_PUSH_ORDER": dict(
        text="arg1 ADDRESS(T+8) and its slot unchanged; earlier order changes",
        arg1=("ADDR", 8), slot1=-0x10, a3=("MEM", 0x50), a4=("MEM", 0x4C)),
    "M6_B_SKIP": dict(text="Unconditional exit; no delivery at the target CALL",
                      reaches=False, uncond=True),
    "M7_B_RECEIVER_ONLY": dict(
        text="Receiver becomes the T-point ESI; arg1 and its slot unchanged",
        arg1=("ADDR", 8), slot1=-0x10, recv="UNK", recv_esi=True),
    "M8_B_WRONG_TARGET": dict(
        text="Actual target 0x00528E51; no valid bridge; wrong target NOT followed",
        actual_target=0x528E51, bvalid=False),
    "M9_B_LEA_TO_MOV": dict(
        text="arg1 MEM(T+8), not ADDRESS(T+8); no pointee interpretation",
        arg1=("MEM", 8)),
}

# The EXECUTOR's claimed load-bearing facts (adjudication targets, transcribed
# from the package's WINDOW_IDENTITIES.json / BRIDGE_PROVENANCE.json / ledgers
# by this QC session BEFORE running its own derivation). The QC compares ITS
# OWN measurements against these and reports agree/disagree per field.
EXEC_CLAIMS = {
    "window_A": dict(size=66, instrs=23, first=0x528E50, last_end=0x528E92,
                     call=dict(va=0x528E8D, target=0x85B1B0)),
    "window_B": dict(size=52, instrs=16, first=0x4C4792, last_end=0x4C47C6,
                     calls=[(0x4C4797, 0x95D3C4), (0x4C47C1, 0x528E50)]),
    "phase_a": dict(
        S_delta=-56, src_slot_delta=4, src_slot="[E+0x4]",
        src_pivot="[S+0x3c]", preserved=True, edi_ok=True,
        edi_def=0x528E84, push_va=0x528E8A, push_reg="edi",
        esp_before=-0x44, callee_entry=-0x48, arg1_slot_S=-0xC,
        callee_entry_S=-0x10, arg1_kind="STACK_READ",
        stack_write_offs=[-0x38, -0x34, -0x30, -0x2C, -0x28, -0xC, -8, -4],
        seg_writes=["fs:[0x0]"], recv_kind="ENTRY_RECEIVER",
        fs_stored_off=-0xC),
    "phase_b": dict(
        T_delta=0, flags_ok=True, je_target=0x4C47C8,
        opaque=dict(push=0x128, cleanup=4, target=0x95D3C4),
        lea=dict(va=0x4C47BA, kind="ADDRESS", disp=0x14, result=8),
        arg1=dict(kind="ADDRESS", slot=-0x10, val=8, push_va=0x4C47BE,
                  push_reg="ecx"),
        args=dict(a2="ESI_UNKNOWN_T", a3=("MEM", 0x4C), a4=("MEM", 0x50)),
        recv=dict(kind="OPAQUE_RET"),
        call=dict(va=0x4C47C1, target=0x528E50, esp_before=-0x10,
                  callee_entry=-0x14, bvalid=True),
        null=dict(je=True, reached=False)),
    "bridge": dict(join="E = T-0x14", slot_T=-0x10, kind="ADDRESS", val=8,
                   intervening=[], status="POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL"),
}

DISCOVERY_SHA = {  # INPUT_IDENTITIES.md I2 records (crash-left files at discovery)
    "PREREGISTRATION_prefix_19151": ("f36de40af53cee9fe2f0f5a11a65475239"
                                     "e5035de96f2fd45d4e5669e775eacc"),
    "01_RAW/WINDOW_A_OBJDUMP.txt": ("7aaba008cfbd8baf4cdf868ba25e3e9a014"
                                    "e9f732e375402553aaa3282d2c86b"),
    "01_RAW/WINDOW_B_OBJDUMP.txt": ("b82c5532d1e10ee3116c7e74ea72471257"
                                    "fa1e3a110f7bcfea0c452b01ed99cc"),
}


class QCUnresolved(Exception):
    """Fail-closed marker for this QC implementation."""


# ------------------------------------------------------------------ utils

def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def va_s(v):
    return "0x%08X" % v


def fmt_off(d):
    """Hex offset formatting consistent with the package's ledger notation:
    4 -> '+0x4', -56 -> '-0x38', 0 -> ''."""
    if d == 0:
        return ""
    return "+0x%x" % d if d > 0 else "-0x%x" % (-d)


def expr_delta(t):
    """'E-0x38' / 'T0-0xc' / 'T0+0x4' / 'E' / 'T0' -> int (or None)."""
    m = re.match(r"^(E|T0|T|S)(?:([+-])0x([0-9a-f]+))?$", t.strip())
    if not m:
        return None
    if not m.group(2):
        return 0
    v = int(m.group(3), 16)
    return -v if m.group(2) == "-" else v


def parse_prod_expr(s):
    """'ADDRESS(T+0x8)' -> ['ADDR', 8]; 'MEM(T+0x4c)' -> ['MEM', 0x4C]."""
    if not isinstance(s, str):
        return [None, None]
    m = re.match(r"^(ADDRESS|MEM)\(T(?:([+-])0x([0-9a-f]+))?\)$", s.strip())
    if not m:
        return [None, None]
    kind = "ADDR" if m.group(1) == "ADDRESS" else "MEM"
    if not m.group(2):
        return [kind, 0]
    v = int(m.group(3), 16)
    return [kind, -v if m.group(2) == "-" else v]


# ------------------------------------------------------------------ objdump tool

def objdump_version():
    p = subprocess.run(["objdump", "--version"], capture_output=True, text=True)
    return p.stdout.splitlines()[0].strip(), p.returncode


def run_objdump(fixture, va):
    cmd = ["objdump", "-D", "-b", "binary", "-m", "i386", "-M", "intel",
           "--adjust-vma=" + hex(va), fixture]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, " ".join(cmd)


LINE_RE = re.compile(r"^\s*([0-9a-f]{1,8}):\s*(.*)$")


class In:
    __slots__ = ("va", "bytes", "n", "mn", "ops", "text")

    def __init__(self, va, blist, text):
        self.va, self.bytes, self.n = va, blist, len(blist)
        self.text = text
        parts = text.split(None, 1)
        self.mn = parts[0]
        self.ops = parts[1].strip() if len(parts) > 1 else ""


def parse_dump(raw, va_start, va_end):
    """Parse raw objdump text into a contiguous, exactly-covering instruction
    list; fail-closed on gaps/overlaps/bad coverage."""
    ins, pending = [], None
    for line in raw.splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        addr = int(m.group(1), 16)
        rest = m.group(2)
        fields = rest.split("\t")

        def hexall(L):
            return all(re.match(r"^[0-9a-f]{2}$", b) for b in L)
        if len(fields) >= 2 and fields[-1].strip() \
                and not hexall([fields[-1].strip()]):
            bstr = "\t".join(fields[:-1]).strip()
            blist = bstr.split()
            if blist and hexall(blist):
                ins.append(In(addr, blist, fields[-1].strip()))
                pending = ins[-1]
        else:
            blist = rest.split()
            if pending is not None and blist and hexall(blist):
                pending.bytes.extend(blist)
                pending.n = len(pending.bytes)
    if not ins:
        raise QCUnresolved("no instructions decoded")
    if ins[0].va != va_start:
        raise QCUnresolved("first VA 0x%X != window start 0x%X"
                           % (ins[0].va, va_start))
    for i in range(len(ins) - 1):
        if ins[i].va + ins[i].n != ins[i + 1].va:
            raise QCUnresolved("decode gap/overlap at 0x%X" % ins[i].va)
    if ins[-1].va + ins[-1].n != va_end:
        raise QCUnresolved("decode end 0x%X != window end 0x%X"
                           % (ins[-1].va + ins[-1].n, va_end))
    return ins


# ------------------------------------------------------------------ symbolic engine

class Val:
    """QC symbolic value: kind + text + optional stack offset (replay-base
    coordinates) + optional defining VA."""
    __slots__ = ("kind", "text", "off", "at")

    def __init__(self, kind, text, off=None, at=None):
        self.kind, self.text, self.off, self.at = kind, text, off, at


MEMRE = re.compile(r"^(?:DWORD PTR )?\[esp([+-]0x[0-9a-f]+)?\]$")
SEGRE = re.compile(r"^(fs|gs|ds|cs|es|ss):(0x[0-9a-f]+)$")
HEXRE = re.compile(r"^0x[0-9a-f]+$")
FLAG_MN = {"sub", "add", "xor", "test", "cmp", "or", "and", "adc", "sbb",
           "neg", "inc", "dec"}


class St:
    """One replay path's state. esp is an integer offset from the window-entry
    ESP symbol; mem maps offset -> (Val, writer_va)."""

    def __init__(self, entry_receiver=False, suffix="ENTRY"):
        self.esp = 0
        self.regs = {}
        for r in ("eax", "ebx", "ecx", "edx", "esi", "edi"):
            self.regs[r] = Val("UNK", r.upper() + "_" + suffix)
        if entry_receiver:
            self.regs["ecx"] = Val("RECV", "ECX_" + suffix)
        self.mem = {}
        self.writes = []       # (va, kind, off, val)
        self.segw = []         # (va, seg, off_text, val)
        self.reads = []        # (va, off, val, prov)
        self.flagw = []        # (va, mn)
        self.flags = None      # ("TEST", reg, va) or ("ARITH", va)
        self.steps = []        # per-instruction ledger rows
        self.defs = {}         # reg -> (va, val) latest definition
        self.reg_at = {}       # (va, reg) -> val at definition time

    def setreg(self, va, r, v):
        self.regs[r] = v
        self.defs[r] = (va, v)
        self.reg_at[(va, r)] = v

    def rd(self, va, off):
        if off in self.mem:
            v, wva = self.mem[off]
            prov = "in_window@%s" % va_s(wva)
        else:
            v = Val("MEM", "MEM([%+d])" % off, off=off, at=None)
            prov = "caller_area_unknown"
        self.reads.append((va, off, v, prov))
        return v, prov

    def wr(self, va, kind, off, v):
        self.mem[off] = (v, va)
        self.writes.append((va, kind, off, v))


def step_note(st, ins, note):
    st.steps.append(dict(va=va_s(ins.va), bytes=" ".join(ins.bytes),
                         op=ins.text, esp=st.esp, note=note))


def exec1(st, ins):
    """Interpret ONE instruction; return None (continue), a boundary dict
    (call) or a branch dict. Fail-closed on unsupported shapes."""
    mn, ops = ins.mn, ins.ops
    ol = [o.strip() for o in ops.split(",")] if ops else []

    if mn == "push":
        if len(ol) == 1 and HEXRE.match(ol[0]):
            v = Val("IMM", ol[0])
        elif len(ol) == 1 and ol[0] in st.regs:
            v = st.regs[ol[0]]
        else:
            raise QCUnresolved("unsupported push: " + ops)
        st.esp -= 4
        st.wr(ins.va, "PUSH", st.esp, v)
        step_note(st, ins, "push -> [%+d] := %s" % (st.esp, v.text))
        return None

    if mn in ("sub", "add"):
        if len(ol) == 2 and ol[0] == "esp" and HEXRE.match(ol[1]):
            d = int(ol[1], 16)
            st.esp += -d if mn == "sub" else d
            st.flagw.append((ins.va, mn))
            st.flags = ("ARITH", ins.va)
            step_note(st, ins, "%s esp,%s -> esp=%+d" % (mn, ol[1], st.esp))
            return None
        raise QCUnresolved("unsupported %s: %s" % (mn, ops))

    if mn == "mov":
        if len(ol) != 2:
            raise QCUnresolved("mov arity: " + ops)
        dst, src = ol
        mseg = SEGRE.match(src)
        if mseg:
            seg, offx = mseg.group(1), mseg.group(2)
            if seg == "fs":
                v = Val("FS0", "FS0_PREV")
            else:
                v = Val("COOKIE", "MOFFS(%s:%s)" % (seg, offx))
            st.setreg(ins.va, dst, v)
            step_note(st, ins, "seg load %s -> %s (opaque)" % (src, dst))
            return None
        msegd = SEGRE.match(dst)
        if msegd:
            if src not in st.regs:
                raise QCUnresolved("seg store from non-reg: " + ops)
            st.segw.append((ins.va, msegd.group(1), msegd.group(2),
                            st.regs[src]))
            step_note(st, ins, "SEGMENT %s := %s (NOT a stack write; AS4)"
                      % (dst, st.regs[src].text))
            return None
        msrc = MEMRE.match(src)
        if dst in st.regs and msrc:
            d = 0 if msrc.group(1) is None else int(msrc.group(1), 16)
            v, prov = st.rd(ins.va, st.esp + d)
            st.setreg(ins.va, dst, v)
            step_note(st, ins, "load %s := MEM[%+d] (%s)"
                      % (dst, st.esp + d, prov))
            return None
        mdst = MEMRE.match(dst)
        if mdst:
            d = 0 if mdst.group(1) is None else int(mdst.group(1), 16)
            if src in st.regs:
                v = st.regs[src]
            elif HEXRE.match(src):
                v = Val("IMM", src)
            else:
                raise QCUnresolved("unsupported store src: " + ops)
            st.wr(ins.va, "MOV_STORE", st.esp + d, v)
            step_note(st, ins, "store [%+d] := %s (no flag write)"
                      % (st.esp + d, v.text))
            return None
        if dst in st.regs and src in st.regs:
            st.setreg(ins.va, dst, st.regs[src])
            step_note(st, ins, "mov %s := %s (%s)"
                      % (dst, src, st.regs[src].text))
            return None
        raise QCUnresolved("unsupported mov: " + ops)

    if mn == "lea":
        if len(ol) != 2 or ol[0] not in st.regs or not MEMRE.match(ol[1]):
            raise QCUnresolved("unsupported lea: " + ops)
        if ins.bytes[0] != "8d":
            raise QCUnresolved("lea opcode byte is not 8d: %s"
                               % " ".join(ins.bytes))
        m = MEMRE.match(ol[1])
        d = 0 if m.group(1) is None else int(m.group(1), 16)
        off = st.esp + d
        v = Val("ADDR", "ADDRESS([%+d]) (lea@%s)" % (off, va_s(ins.va)),
                off=off, at=ins.va)
        st.setreg(ins.va, ol[0], v)
        step_note(st, ins, "lea %s := ADDRESS([%+d]) [kind=ADDR, opcode 8D]"
                  % (ol[0], off))
        return None

    if mn == "xor":
        if len(ol) == 2 and ol[0] in st.regs and \
                (ol[1] in st.regs or ol[1] == "esp"):
            if ol[1] == "esp":
                text = "%s XOR ESP" % st.regs[ol[0]].text
            else:
                text = "%s XOR %s" % (st.regs[ol[0]].text, ol[1].upper())
            st.setreg(ins.va, ol[0], Val("COOKIE_X", text))
            st.flagw.append((ins.va, mn))
            st.flags = ("ARITH", ins.va)
            step_note(st, ins, "opaque xor; value changes, ESP/width "
                      "unchanged")
            return None
        raise QCUnresolved("unsupported xor: " + ops)

    if mn == "test":
        if len(ol) == 2 and ol[0] == ol[1] and ol[0] in st.regs:
            st.flagw.append((ins.va, mn))
            st.flags = ("TEST", ol[0], ins.va)
            step_note(st, ins, "test %s,%s -> ZF := (%s == 0)"
                      % (ol[0], ol[0], st.regs[ol[0]].text))
            return None
        raise QCUnresolved("unsupported test: " + ops)

    if mn == "call":
        if len(ol) != 1 or not HEXRE.match(ol[0]):
            raise QCUnresolved("unsupported call: " + ops)
        if len(ins.bytes) != 5 or ins.bytes[0] != "e8":
            raise QCUnresolved("call not rel32 e8: %s" % " ".join(ins.bytes))
        rel = int.from_bytes(bytes(int(b, 16) for b in ins.bytes[1:5]),
                             "little", signed=True)
        printed = int(ol[0], 16)
        rc_t = ins.va + 5 + rel
        if rc_t != printed:
            raise QCUnresolved("call target mismatch printed 0x%X recompute 0x%X"
                               % (printed, rc_t))
        esp_before = st.esp
        st.esp -= 4
        st.wr(ins.va, "RET_PUSH", st.esp,
              Val("IMM", "RETADDR@%s" % va_s(ins.va)))
        if printed == OPAQUE_TARGET:
            st.esp += 4                 # AS3: pops exactly its return address
            st.setreg(ins.va, "eax",
                      Val("OPRET", "OPAQUE_RET(%s)" % va_s(printed), at=ins.va))
            step_note(st, ins, "OPAQUE call %s: ret-push recorded at [%+d]; "
                      "AS3 ESP restored; EAX := OPAQUE_RET"
                      % (va_s(printed), st.esp - 4))
            return None
        step_note(st, ins, "BOUNDARY call -> %s (callee not opened; hardware "
                  "ret push applied; esp_before=%+d)"
                  % (va_s(printed), esp_before))
        return dict(ev="call", va=ins.va, target=printed, target_rc=rc_t,
                    esp_before=esp_before, callee_entry=esp_before - 4)

    if mn in ("je", "jmp"):
        if len(ol) != 1 or not HEXRE.match(ol[0]):
            raise QCUnresolved("unsupported branch: " + ops)
        want = 0x74 if mn == "je" else 0xEB
        if int(ins.bytes[0], 16) != want:
            raise QCUnresolved("branch opcode mismatch: %s"
                               % " ".join(ins.bytes))
        if len(ins.bytes) != 2:
            raise QCUnresolved("branch not rel8: %s" % " ".join(ins.bytes))
        rel8 = int.from_bytes(bytes(int(b, 16) for b in ins.bytes[1:2]),
                              "little", signed=True)
        tgt = ins.va + 2 + rel8
        if tgt != int(ol[0], 16):
            raise QCUnresolved("branch target mismatch printed 0x%X recompute 0x%X"
                               % (int(ol[0], 16), tgt))
        step_note(st, ins, "%s 0x%X" % (mn, tgt))
        if mn == "jmp":
            return dict(ev="jmp", va=ins.va, target=tgt)
        if st.flags is None or st.flags[0] != "TEST":
            raise QCUnresolved("je without a TEST-defined ZF")
        return dict(ev="je", va=ins.va, target=tgt, tested_reg=st.flags[1])

    raise QCUnresolved("unsupported mnemonic: " + mn)


def clone(st):
    n = St.__new__(St)
    n.esp = st.esp
    n.regs = dict(st.regs)
    n.mem = dict(st.mem)
    n.writes = list(st.writes)
    n.segw = list(st.segw)
    n.reads = list(st.reads)
    n.flagw = list(st.flagw)
    n.flags = st.flags
    n.steps = list(st.steps)
    n.defs = dict(st.defs)
    n.reg_at = dict(st.reg_at)
    return n


def walk(ins, va_start, va_end, entry_receiver=False, suffix="ENTRY",
         max_paths=2):
    """Enumerate paths (fail-closed beyond max_paths). Returns [(name, state,
    end_event), ...]."""
    results, stack = [], [(St(entry_receiver, suffix), 0, "P")]
    while stack:
        st, idx, name = stack.pop()
        if idx >= len(ins):
            results.append((name, st, dict(ev="window_end")))
            continue
        ev = exec1(st, ins[idx])
        if ev is None:
            stack.append((st, idx + 1, name))
            continue
        if ev["ev"] == "call":
            results.append((name, st, ev))
            continue
        if ev["ev"] == "je":
            if not (va_start <= ev["target"] < va_end):
                if len(results) + len(stack) + 2 > max_paths:
                    raise QCUnresolved("path explosion")
                st_taken = clone(st)
                st_taken.steps.append(dict(va=va_s(ev["va"]), op="PATH_FORK",
                                           esp=st.esp,
                                           note="ZF=1 JE taken -> exits window "
                                                "at 0x%X (not opened)"
                                                % ev["target"]))
                results.append((name + "_NULL", st_taken,
                                dict(ev="exit", exit_va=ev["target"],
                                     kind="cond_taken", call_reached=False,
                                     delivered=None)))
                stack.append((st, idx + 1, name + "_NONNULL"))
                continue
            raise QCUnresolved("in-window conditional target unhandled")
        if ev["ev"] == "jmp":
            if not (va_start <= ev["target"] < va_end):
                results.append((name, st, dict(ev="exit", exit_va=ev["target"],
                                               kind="uncond",
                                               call_reached=False,
                                               delivered=None)))
                continue
            raise QCUnresolved("in-window jmp target unhandled")
        raise QCUnresolved("unknown event " + str(ev))
    return results


# ------------------------------------------------------------------ phase derivations

def derive_a(ins):
    """Phase A derivation on window A bytes: S chain, source slot, write
    census, EDI preservation, delivery facts. All measured, none assumed."""
    paths = walk(ins, WIN["A"]["va"], WIN["A"]["va"] + WIN["A"]["size"],
                 entry_receiver=True, suffix="ENTRY")
    if len(paths) != 1 or paths[0][2]["ev"] != "call":
        raise QCUnresolved("window A: expected single straight call boundary")
    st, ev = paths[0][1], paths[0][2]
    # pivot S = ESP when executing 0x00528E76
    s = None
    for row in st.steps:
        if int(row["va"], 16) == 0x528E76:
            s = row["esp"]
            break
    if s is None:
        raise QCUnresolved("pivot 0x528E76 not in window A")
    # delivery: last PUSH before the boundary call == arg1 writer (AS2)
    pushes = [w for w in st.writes if w[1] == "PUSH" and w[0] < ev["va"]]
    if not pushes:
        raise QCUnresolved("no delivery push")
    lp = pushes[-1]
    arg1_slot = ev["esp_before"]     # [callee_entry+4] == esp_before_call
    if lp[2] != arg1_slot:
        raise QCUnresolved("last push slot %d != arg1 slot %d"
                           % (lp[2], arg1_slot))
    val = lp[3]
    if val.kind != "MEM":
        raise QCUnresolved("A arg1 value kind %s != MEM(stack read)" % val.kind)
    # producing load: the read record that created this exact value object
    src_va = src_off = None
    for (rva, roff, rv, prov) in st.reads:
        if rv is val:
            src_va, src_off = rva, roff
    if src_va is None:
        raise QCUnresolved("producing load not found")
    # byte-level displacement cross-check of the load
    lins = next(i for i in ins if i.va == src_va)
    if not (lins.bytes[0] == "8b" and lins.bytes[1] == "7c"
            and lins.bytes[2] == "24"):
        raise QCUnresolved("source load is not mov edi,[esp+d8]: %s"
                           % " ".join(lins.bytes))
    disp = int(lins.bytes[3], 16)
    load_esp = next(r["esp"] for r in st.steps if int(r["va"], 16) == src_va)
    if load_esp + disp != src_off:
        raise QCUnresolved("disp byte 0x%X + esp %+d != src slot %+d"
                           % (disp, load_esp, src_off))
    # preservation census before the load
    wbefore = [w for w in st.writes if w[0] < src_va]
    alias = [w for w in wbefore if w[2] == src_off]
    segbefore = [g for g in st.segw if g[0] < src_va]
    preserved = len(alias) == 0
    # EDI reaching definition at the push
    push_ins = next(i for i in ins if i.va == lp[0])
    edi_def = st.defs.get("edi")
    edi_ok = (edi_def is not None and edi_def[0] == src_va
              and lp[0] > src_va and push_ins.ops.strip() == "edi")
    # the FS:[0]-stored value (the LEA-computed address) — measured
    fs_stored_off = None
    for (gva, seg, offx, gv) in segbefore:
        if gva == 0x528E70:
            fs_stored_off = gv.off
    facts = dict(
        S=s, src_va=src_va, src_off=src_off, src_disp=disp,
        src_slot_E="[E%s]" % fmt_off(src_off),
        src_slot_S="[S%s]" % fmt_off(src_off - s),
        preserved=preserved,
        alias=[(va_s(w[0]), w[1], w[2]) for w in alias],
        wbefore=[(va_s(w[0]), w[1], w[2], w[3].text) for w in wbefore],
        segbefore=[(va_s(g[0]), "%s:[%s]" % (g[1], g[2]), g[3].text)
                   for g in segbefore],
        stack_write_offs=sorted({w[2] for w in wbefore}),
        fs_stored_off=fs_stored_off,
        edi_ok=edi_ok, edi_def=edi_def[0] if edi_def else None,
        push_va=lp[0], push_reg=push_ins.ops.strip(),
        arg1_slot=arg1_slot, esp_before=ev["esp_before"],
        callee_entry=ev["callee_entry"], target=ev["target"],
        target_rc=ev["target_rc"], arg1_kind=val.kind, arg1_text=val.text,
        recv_kind=st.regs["ecx"].kind, recv_text=st.regs["ecx"].text,
        esp_before_S=ev["esp_before"] - s,
        callee_entry_S=ev["callee_entry"] - s,
        arg1_slot_S=arg1_slot - s,
        instr_count=len(ins), steps=st.steps,
        _writes=st.writes, _segw=st.segw, _reads=st.reads)
    return facts


def derive_b(ins):
    """Phase B derivation on window B bytes: T, opaque-call structure (AS3),
    flags TEST->JE, the value instruction at 0x4C47BA (kind from the OPCODE
    BYTE), arg slots at the callee entry, receiver, call target, both paths."""
    va0, va1 = WIN["B"]["va"], WIN["B"]["va"] + WIN["B"]["size"]
    paths = walk(ins, va0, va1, entry_receiver=False, suffix="UNKNOWN_T")
    nulls = [p for p in paths if p[2]["ev"] == "exit"]
    calls = [p for p in paths if p[2]["ev"] == "call"]
    if len(nulls) > 1 or len(calls) > 1:
        raise QCUnresolved("path shape unexpected in window B")
    facts = dict(path_count=len(paths), instr_count=len(ins))
    if nulls:
        ev = nulls[0][2]
        facts["null"] = dict(exit_va=ev["exit_va"],
                             in_window=va0 <= ev["exit_va"] < va1,
                             uncond=(ev["kind"] == "uncond"),
                             je=(ev["kind"] == "cond_taken"),
                             call_reached=False,
                             delivered=None)
    if calls:
        st, ev = calls[0][1], calls[0][2]
        # pivot T = ESP when executing 0x004C47AF
        t = None
        for row in st.steps:
            if int(row["va"], 16) == 0x4C47AF:
                t = row["esp"]
                break
        if t is None:
            raise QCUnresolved("pivot 0x4C47AF not in window B")
        # flags census TEST -> JE (independent mnemonic census)
        test_va = next(i.va for i in ins if i.mn == "test")
        br_ins = next(i for i in ins if i.mn in ("je", "jmp"))
        between = [i for i in ins if test_va < i.va < br_ins.va
                   and i.mn in FLAG_MN]
        flags_ok = (len(between) == 0 and br_ins.mn == "je")
        # opaque-call structure (byte-derived neighbors)
        oc = next(i for i in ins if i.mn == "call"
                  and int(i.ops.strip(), 16) == OPAQUE_TARGET)
        idx = ins.index(oc)
        before_ok = (ins[idx - 1].mn == "push"
                     and ins[idx - 1].ops.strip() == "0x128")
        after_ok = (ins[idx + 1].mn == "add"
                    and ins[idx + 1].ops.strip() == "esp,0x4")
        # value instruction at 0x4C47BA — kind from the OPCODE BYTE
        vins = next(i for i in ins if i.va == 0x4C47BA)
        if vins.bytes[0] == "8d":
            vkind = "ADDR"
        elif vins.bytes[0] == "8b":
            vkind = "MEM"
        else:
            raise QCUnresolved("unexpected value opcode at 0x4C47BA: %s"
                               % vins.bytes[0])
        vdst = vins.ops.split(",")[0].strip()
        vreg = st.reg_at.get((0x4C47BA, vdst))
        # arg1 = last push before the boundary call
        pushes = [w for w in st.writes if w[1] == "PUSH" and w[0] < ev["va"]]
        if not pushes:
            raise QCUnresolved("no arg push before bridge call")
        lp = pushes[-1]
        arg1_slot = ev["esp_before"]
        if lp[2] != arg1_slot:
            raise QCUnresolved("last push slot %d != arg1 slot %d"
                               % (lp[2], arg1_slot))
        push_ins = next(i for i in ins if i.va == lp[0])
        a1 = lp[3]
        # arg slots 1..4 at the callee entry
        aslots = {}
        for k in range(1, 5):
            off = ev["callee_entry"] + 4 * k
            if off in st.mem:
                vv = st.mem[off][0]
                aslots["a%d" % k] = (vv.kind, vv.off, vv.text)
        recv = st.regs["ecx"]
        facts["nonnull"] = dict(
            T=t, flags_ok=flags_ok,
            flag_between=[va_s(i.va) + " " + i.mn for i in between],
            br_mn=br_ins.mn, br_target=int(br_ins.ops.strip(), 16),
            opaque=dict(found=True, push128=before_ok, add_esp4=after_ok,
                        target=OPAQUE_TARGET),
            val_insn=dict(va=0x4C47BA, opcode=vins.bytes[0], kind=vkind,
                          disp=int(vins.bytes[3], 16), reg=vdst,
                          reg_off=(vreg.off if vreg else None),
                          reg_text=(vreg.text if vreg else None)),
            arg1=dict(kind=a1.kind, off=a1.off, text=a1.text,
                      slot=arg1_slot, push_va=lp[0],
                      push_reg=push_ins.ops.strip(), def_va=a1.at),
            aslots=aslots,
            recv=dict(kind=recv.kind, text=recv.text),
            call=dict(va=ev["va"], target=ev["target"],
                     target_rc=ev["target_rc"],
                     esp_before=ev["esp_before"],
                     callee_entry=ev["callee_entry"],
                     bvalid=(ev["target"] == BRIDGE_ENTRY)),
            steps=st.steps, _writes=st.writes)
    return facts


def bridge_join(a, b):
    """QC bridge join in ONE coordinate system: B-side offsets are in T0
    (window-B-entry) coords; the measured callee-entry E = callee_entry (T0
    coords); A-side offsets (E coords) map to T0 coords as off + E. All checks
    are computed, none assumed."""
    nn = b["nonnull"]
    e_off = nn["call"]["callee_entry"]      # E offset in T0 coords (-0x14)
    t = nn["T"]
    a_src_T0 = e_off + a["src_off"]
    b_arg1_T0 = nn["arg1"]["slot"]
    slot_identity = (a_src_T0 == b_arg1_T0)
    res = dict(join="E = T%s" % fmt_off(e_off), E_off=e_off,
               a_src_T0=a_src_T0, b_arg1_T0=b_arg1_T0,
               a_src_T=a_src_T0 - t, b_arg1_T=b_arg1_T0 - t,
               slot_identity=slot_identity)
    if not slot_identity:
        res["status"] = "REJECTED_SLOT_MISMATCH"
        return res
    if nn["arg1"]["kind"] != "ADDR":
        res["status"] = "REJECTED_VALUE_KIND_NOT_ADDR"
        return res
    # combined write census in T0 coords between the B final push and the
    # A source load (both path write logs, one coordinate system)
    push_va = nn["arg1"]["push_va"]
    load_va = a["src_va"]
    joined_T0 = b_arg1_T0
    interv = []
    for (wva, kind, off, v) in nn["_writes"]:
        if push_va < wva < load_va and off == joined_T0:
            interv.append(["B", va_s(wva), kind, off])
    for (wva, kind, off, v) in a["_writes"]:
        if push_va < wva < load_va and off + e_off == joined_T0:
            interv.append(["A", va_s(wva), kind, off + e_off])
    res["intervening"] = interv
    if interv:
        res["status"] = "REJECTED_SLOT_OVERWRITTEN"
        return res
    if not (a["preserved"] and a["edi_ok"]):
        res["status"] = "REJECTED_A_PRESERVATION"
        return res
    if a["arg1_kind"] != "MEM":
        res["status"] = "REJECTED_A_VALUE_KIND"
        return res
    res["status"] = "POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL"
    res["cross_value"] = ["ADDR", nn["arg1"]["off"] - t]
    res["boundaries"] = ["arg1@FUN_00528E50 entry via CALL 0x004C47C1",
                         "arg1@FUN_0085B1B0 entry via CALL 0x00528E8D"]
    res["conditions"] = ["AS1/AS2 x86 push/call + cdecl arg order",
                         "AS3 opaque 0x0095D3C4 normal ABI-compatible return",
                         "EAX != 0 at 0x004C47AD (qualified branch only)",
                         "AS4 FS/TIB disjoint from live argument stack region",
                         "AS5 straight-line window-A path from 0x00528E50"]
    return res


# ------------------------------------------------------------------ ESP walk (gate)

def esp_walk(ins):
    """Minimal independent arithmetic ESP walk (separate from the replay
    engine). Returns (per-va esp AFTER the instruction, boundary call esp)."""
    esp = 0
    per, boundary = {}, {}
    for i in ins:
        mn, ops = i.mn, i.ops
        ol = [o.strip() for o in ops.split(",")] if ops else []
        if mn == "push":
            esp -= 4
        elif mn == "sub" and ol[0] == "esp":
            esp -= int(ol[1], 16)
        elif mn == "add" and ol[0] == "esp":
            esp += int(ol[1], 16)
        elif mn == "call":
            if int(ol[0], 16) != OPAQUE_TARGET:
                boundary[i.va] = esp       # ESP BEFORE the hardware ret push
                per[i.va] = esp
                return per, boundary
        per[i.va] = esp
    return per, boundary


# ------------------------------------------------------------------ BR-C1 field
# helpers (correction PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_
# R1_20261009). QC's OWN targeted field-reading/type/expression comparison
# utilities for the four BR-C1 relations only. Not a general schema engine;
# never eval; every helper returns (ok, diagnostic, value) and never raises
# for a missing field, wrong native JSON type, malformed supported expression
# or mismatch. The QC does NOT import or delegate to the production verdict;
# all derivations below use this file's own parse/walk/opcode facts.

def field_get(container, dotted):
    cur = container
    for part in dotted.split("."):
        if type(cur) is not dict or part not in cur:
            return False, None
        cur = cur[part]
    return True, cur


def _tname(v):
    return type(v).__name__


def qc_check_str(container, dotted, expected):
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not str:
        return False, ("WRONG_TYPE:%s:expected JSON string, got %s"
                       % (dotted, _tname(v))), v
    if v != expected:
        return False, ("VALUE_MISMATCH:%s:my derivation %r, got %r"
                       % (dotted, expected, v)), v
    return True, "OK", v


def qc_check_int(container, dotted, expected):
    """Native JSON integer; JSON booleans are NOT integers here (type(True)
    is bool), so a boolean value is rejected as WRONG_TYPE."""
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not int:
        return False, ("WRONG_TYPE:%s:expected JSON integer, got %s"
                       % (dotted, _tname(v))), v
    if v != expected:
        return False, ("VALUE_MISMATCH:%s:my derivation %d, got %r"
                       % (dotted, expected, v)), v
    return True, "OK", v


def qc_check_bool(container, dotted, expected):
    """Native JSON boolean; no string->boolean coercion (JSON false is not a
    valid positive bridge predicate)."""
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not bool:
        return False, ("WRONG_TYPE:%s:expected JSON boolean, got %s"
                       % (dotted, _tname(v))), v
    if v is not expected:
        return False, ("VALUE_MISMATCH:%s:my derivation %r, got %r"
                       % (dotted, expected, v)), v
    return True, "OK", v


def qc_check_va_str(container, dotted, derived_va):
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not str:
        return False, ("WRONG_TYPE:%s:expected JSON string, got %s"
                       % (dotted, _tname(v))), v
    m = re.match(r"^0x([0-9a-fA-F]{8})$", v)
    if not m:
        return False, ("MALFORMED_EXPR:%s:not a supported 0xXXXXXXXX VA "
                       "string" % dotted), v
    if int(m.group(1), 16) != derived_va:
        return False, ("VALUE_MISMATCH:%s:my derivation %s, got %r"
                       % (dotted, va_s(derived_va), v)), v
    return True, "OK", v


def qc_slot_expr(delta):
    """QC-local '[T-0x10]' formatter from fmt_off (no production import)."""
    return "[%s%s]" % ("T", fmt_off(delta))


def qc_check_slot_expr(container, dotted, derived_delta):
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not str:
        return False, ("WRONG_TYPE:%s:expected JSON string, got %s"
                       % (dotted, _tname(v))), v
    if not re.match(r"^\[T(?:[+-]0x[0-9a-fA-F]+)?\]$", v):
        return False, ("MALFORMED_EXPR:%s:not a supported [T+0x..] slot "
                       "expression" % dotted), v
    if v != qc_slot_expr(derived_delta):
        return False, ("VALUE_MISMATCH:%s:my derivation %s, got %r"
                       % (dotted, qc_slot_expr(derived_delta), v)), v
    return True, "OK", v


def qc_eslot_expr(delta):
    """QC-local '[E+0x4]' formatter (E base, fmt_off hex notation; no
    production import). Added by the leaf-field correction run
    PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009."""
    return "[E%s]" % fmt_off(delta)


def qc_check_eslot_expr(container, dotted, derived_delta):
    """QC's OWN safe string helper for the persisted E-based source-slot
    expression leaf 'phase_a.source_slot.slot_expr_from_E'. The expected
    expression is constructed from MY independently derived source-slot
    delta (my_src), never from a copied persisted claim or the production
    verdict. Never raises: a missing field, wrong native JSON type,
    malformed supported expression or mismatch returns a named diagnostic.
    Added by the leaf-field correction run
    PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009."""
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not str:
        return False, ("WRONG_TYPE:%s:expected JSON string, got %s"
                       % (dotted, _tname(v))), v
    if not re.match(r"^\[E(?:[+-]0x[0-9a-fA-F]+)?\]$", v):
        return False, ("MALFORMED_EXPR:%s:not a supported [E+0x..] slot "
                       "expression" % dotted), v
    if v != qc_eslot_expr(derived_delta):
        return False, ("VALUE_MISMATCH:%s:my derivation %s, got %r"
                       % (dotted, qc_eslot_expr(derived_delta), v)), v
    return True, "OK", v


def qc_check_addr_expr(container, dotted, derived_delta):
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not str:
        return False, ("WRONG_TYPE:%s:expected JSON string, got %s"
                       % (dotted, _tname(v))), v
    m = re.match(r"^ADDRESS\(T(?:([+-])0x([0-9a-fA-F]+))?\)$", v)
    if not m:
        return False, ("MALFORMED_EXPR:%s:not a supported ADDRESS(T+0x..) "
                       "expression" % dotted), v
    got = 0
    if m.group(1):
        got = int(m.group(2), 16)
        if m.group(1) == "-":
            got = -got
    if got != derived_delta:
        return False, ("VALUE_MISMATCH:%s:my derivation ADDRESS(T%s0x%x), "
                       "got %r" % (dotted, "+" if derived_delta >= 0 else "-",
                                   abs(derived_delta), v)), v
    return True, "OK", v


def qc_check_arg_slot_expr(container, dotted, derived_delta):
    """Persisted arg_slots documented finite form 'T0+0x8 (computed)' vs my
    derived delta (the ' (computed)' suffix is explicitly normalized)."""
    present, v = field_get(container, dotted)
    if not present:
        return False, "MISSING_FIELD:" + dotted, None
    if type(v) is not str:
        return False, ("WRONG_TYPE:%s:expected JSON string, got %s"
                       % (dotted, _tname(v))), v
    m = re.match(r"^T0(?:([+-])0x([0-9a-fA-F]+))?(?: \(computed\))?$", v)
    if not m:
        return False, ("MALFORMED_EXPR:%s:not a supported T0+0x.. "
                       "(computed) expression" % dotted), v
    got = 0
    if m.group(1):
        got = int(m.group(2), 16)
        if m.group(1) == "-":
            got = -got
    if got != derived_delta:
        return False, ("VALUE_MISMATCH:%s:my derivation T0%s0x%x, got %r"
                       % (dotted, "+" if derived_delta >= 0 else "-",
                          abs(derived_delta), v)), v
    return True, "OK", v


# ------------------------------------------------------------------ QC artifact gate

def gate(pkg, prov_override=None):
    """QC's OWN ordinary final gate: re-derive the load-bearing facts from
    physical bytes + MY OWN objdump invocations + MY OWN ESP walk; compare
    against the persisted artifacts (or a mutated copy for AC1/AC2). Package
    hash/manifest checks are bypassed ONLY in the isolated synthetic
    artifact controls (the fact predicate itself is under test)."""
    checks = []

    def chk(cid, fact, claimed, actual, ok):
        checks.append(dict(check=cid, fact=fact, claimed=claimed,
                           actual=actual, ok=bool(ok)))

    def chk_d(cid, fact, claimed, actual, ok, diag):
        """chk + a named diagnostic for the QC's BR-C1 persisted-fact checks."""
        chk(cid, fact, claimed, actual, ok)
        checks[-1]["diagnostic"] = diag if not ok else "OK"

    # 1) physical windows vs WINDOW_IDENTITIES.json
    wids = json.load(open(os.path.join(pkg, "WINDOW_IDENTITIES.json")))
    phys = {}
    for key in ("A", "B"):
        w = WIN[key]
        with open(EXE, "rb") as fh:
            fh.seek(w["raw"])
            phys[key] = fh.read(w["size"])
        c = wids["windows"][key]
        chk("WID-%s-SHA" % key, "window SHA vs physical EXE bytes",
            c["sha256"], sha_b(phys[key]), c["sha256"] == sha_b(phys[key]))
        chk("WID-%s-SIZE" % key, "window size", c["size"], w["size"],
            c["size"] == w["size"])
        chk("WID-%s-INT" % key, "window interval", c["interval"],
            "[%s,%s)" % (va_s(w["va"]), va_s(w["va"] + w["size"])),
            c["va_start"] == va_s(w["va"])
            and c["va_end_exclusive"] == va_s(w["va"] + w["size"]))
        fx = os.path.join(WORK, "gate_window_%s.bin" % key)
        with open(fx, "wb") as fh:
            fh.write(phys[key])
        rc, out, cmd = run_objdump(fx, w["va"])
        if rc != 0:
            raise QCUnresolved("gate objdump rc=%d" % rc)

    # 2) fresh decode of the physical windows
    ins = {}
    for key in ("A", "B"):
        w = WIN[key]
        fx = os.path.join(WORK, "gate_window_%s.bin" % key)
        _rc, out, _cmd = run_objdump(fx, w["va"])
        ins[key] = parse_dump(out, w["va"], w["va"] + w["size"])

    # 3) my independent ESP walks
    walkA, boundA = esp_walk(ins["A"])
    walkB, boundB = esp_walk(ins["B"])

    # 4) ENTRY_FRAME_LEDGER.csv vs my parse + my walk
    efl = list(csv.DictReader(open(os.path.join(pkg,
                                                "ENTRY_FRAME_LEDGER.csv"))))
    by_va = {i.va: i for i in ins["A"]}
    ok_rows = (len(efl) == len(ins["A"]))
    for row in efl:
        va = int(row["VA"], 16)
        i = by_va.get(va)
        if i is None:
            ok_rows = False
            continue
        if row["BYTES"] != " ".join(i.bytes) or row["DECODED_OP"] != i.text:
            ok_rows = False
        eb = expr_delta(row["ESP_BEFORE"])
        ea = expr_delta(row["ESP_AFTER"])
        if i.mn == "call":
            if eb != boundA.get(va) or ea != boundA.get(va, 0) - 4:
                ok_rows = False
        else:
            if ea != walkA.get(va):
                ok_rows = False
    chk("EFL-ROWS", "A ledger rows vs my parse+walk", len(efl),
        len(ins["A"]), ok_rows)
    chk("EFL-S", "S = ESP at 0x00528E76 (my walk)", walkA.get(0x528E76),
        -0x38, walkA.get(0x528E76) == -0x38)
    chk("EFL-BEFCALL", "ESP before tail call 0x00528E8D (my walk)",
        boundA.get(0x528E8D), -0x44, boundA.get(0x528E8D) == -0x44)

    # 5) CALLER_STACK_LEDGER.csv (NONNULL rows) vs my parse + my walk
    csl = list(csv.DictReader(open(os.path.join(pkg,
                                                "CALLER_STACK_LEDGER.csv"))))
    by_va_b = {i.va: i for i in ins["B"]}
    nn_rows = [r for r in csl if r["PATH"] == "NONNULL"]
    ok_rows_b = True
    for row in nn_rows:
        va = int(row["VA"], 16)
        i = by_va_b.get(va)
        if i is None:
            ok_rows_b = False
            continue
        if row["BYTES"] != " ".join(i.bytes) or row["DECODED_OP"] != i.text:
            ok_rows_b = False
        eb = expr_delta(row["ESP_BEFORE"])
        ea = expr_delta(row["ESP_AFTER"])
        if i.mn == "call" and int(i.ops.strip(), 16) != OPAQUE_TARGET:
            if eb != boundB.get(va) or ea != boundB.get(va, 0) - 4:
                ok_rows_b = False
        else:
            if ea != walkB.get(va):
                ok_rows_b = False
    chk("CSL-ROWS", "B ledger NONNULL rows vs my parse+walk", len(nn_rows),
        len(ins["B"]), ok_rows_b)
    chk("CSL-T", "T = ESP at 0x004C47AF (my walk)", walkB.get(0x4C47AF),
        0, walkB.get(0x4C47AF) == 0)
    chk("CSL-BEFCALL", "ESP before bridge call 0x004C47C1 (my walk)",
        boundB.get(0x4C47C1), -0x10, boundB.get(0x4C47C1) == -0x10)

    # 6) BRIDGE_PROVENANCE.json facts vs my byte-derived facts
    prov_path = prov_override or os.path.join(pkg, "BRIDGE_PROVENANCE.json")
    prov = json.load(open(prov_path))
    pa = prov["phase_a"]
    nn = (prov["phase_b"].get("nonnull_path") or {})
    br = prov["bridge"]

    # 6a) A source slot: disp byte at 0x528E84 + my walk S
    #     (BR-C1-R1 leaf-field correction, run
    #      PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009:
    #      the two phase_a.source_slot leaves are now checked INDIVIDUALLY
    #      with QC's OWN safe typed helpers — qc_check_eslot_expr for the
    #      expression leaf (expected constructed from my independently
    #      derived my_src, never from a copied claim or the production
    #      verdict; the old hardcoded "[E+0x4]" string comparison is
    #      removed), qc_check_int for the delta leaf (native JSON integer;
    #      JSON booleans and floats rejected as WRONG_TYPE). The aggregate
    #      PROV-A-SLOT is the conjunction of BOTH typed leaf comparisons.
    #      Both leaves are evaluated even if one fails; no direct indexing
    #      of a tested leaf can raise on a missing field.)
    src_ins = by_va[0x528E84]
    disp = int(src_ins.bytes[3], 16)
    my_src = walkA[0x528E76] + disp
    ok_slot_expr, dg_slot_expr, val_slot_expr = qc_check_eslot_expr(
        prov, "phase_a.source_slot.slot_expr_from_E", my_src)
    chk_d("QC-A-SLOT-EXPR", "persisted entry source-slot expression leaf "
          "(typed; '[E+0x..]' form) vs my bytes-derived slot", val_slot_expr,
          qc_eslot_expr(my_src), ok_slot_expr, dg_slot_expr)
    ok_slot_delta, dg_slot_delta, val_slot_delta = qc_check_int(
        prov, "phase_a.source_slot.slot_delta_from_E", my_src)
    chk_d("QC-A-SLOT-DELTA", "persisted entry source-slot delta leaf "
          "(typed; native JSON integer; JSON booleans/floats rejected) vs my "
          "bytes-derived delta", val_slot_delta, my_src, ok_slot_delta,
          dg_slot_delta)
    chk("PROV-A-SLOT", "clean entry source slot (my disp byte + walk S); "
        "aggregate conjunction of BOTH typed leaf comparisons",
        (val_slot_expr, val_slot_delta), (qc_eslot_expr(my_src), my_src),
        ok_slot_expr and ok_slot_delta)
    chk("PROV-A-DELIVERY", "A delivery ESP facts (my walk)",
        [pa["delivery"]["esp_before_call"],
         pa["delivery"]["callee_entry_esp"]], ["E-0x44", "E-0x48"],
        pa["delivery"]["esp_before_call"] == "E-0x44"
        and pa["delivery"]["callee_entry_esp"] == "E-0x48")

    # 6b) B arg1 kind: OPCODE BYTE at 0x4C47BA
    #     (BR-C1.3 correction: no OR-fallback to the parallel bridge summary
    #      field; the exported arg1.value_kind is compared individually)
    lea_ins = by_va_b[0x4C47BA]
    kind_from_op = "ADDRESS" if lea_ins.bytes[0] == "8d" else "STACK_READ"
    claimed_kind = (nn.get("arg1") or {}).get("value_kind")
    chk("PROV-B-KIND", "arg1 kind vs opcode byte 0x%s at 0x4C47BA"
        % lea_ins.bytes[0], claimed_kind, kind_from_op,
        claimed_kind == kind_from_op == "ADDRESS")

    # 6c) B LEA expr: disp byte + my walk
    #     (BR-C1.3 correction: no OR-fallback to the parallel bridge summary
    #      field; the exported arg1.value_expr is compared individually)
    ldisp = int(lea_ins.bytes[3], 16)
    lea_res_T = walkB[0x4C47BA] + ldisp - walkB[0x4C47AF]
    claimed_expr = (nn.get("arg1") or {}).get("value_expr")
    my_expr = ("ADDRESS(T+0x%x)" % lea_res_T if lea_res_T > 0
               else ("ADDRESS(T)" if lea_res_T == 0
                     else "ADDRESS(T-0x%x)" % -lea_res_T))
    chk("PROV-B-LEA", "LEA result expr (my disp + walk)", claimed_expr,
        my_expr, claimed_expr == my_expr)

    # 6d) joined entry-slot identity: my walk E + src vs [T-0x10]
    #     (BR-C1.2 correction: field-presence-safe read of the persisted
    #      a_source_slot_from_T; no KeyError on a missing field)
    e_join = boundB[0x4C47C1] - 4 - walkB[0x4C47AF]
    joined = e_join + my_src
    b_slot = boundB[0x4C47C1] - walkB[0x4C47AF]
    present_asrc, claimed_asrc = field_get(prov,
                                           "bridge.a_source_slot_from_T")
    ok_asrc = (present_asrc and claimed_asrc == qc_slot_expr(joined)
               and joined == b_slot)
    chk("PROV-BRIDGE-SLOT", "joined entry-slot identity [E+4]==[T-0x10]",
        claimed_asrc if present_asrc else None, qc_slot_expr(joined), ok_asrc)

    # 6e) call targets: my rel32 recompute vs pinned roles
    for win in ("A", "B"):
        for i in ins[win]:
            if i.mn != "call":
                continue
            rel = int.from_bytes(bytes(int(b, 16) for b in i.bytes[1:5]),
                                 "little", signed=True)
            tgt = i.va + 5 + rel
            printed = int(i.ops.strip(), 16)
            pinned = {0x528E8D: TAIL_TARGET_PIN, 0x4C4797: OPAQUE_TARGET,
                      0x4C47C1: BRIDGE_ENTRY}.get(i.va)
            chk("PROV-CALL-%s-%s" % (win, va_s(i.va)),
                "call target (my rel32 recompute) at %s" % va_s(i.va),
                pinned, va_s(tgt), tgt == printed == pinned)

    # 6e-bis) BR-C1.1 persisted CALL identity (QC's OWN derivation): the
    # values ACTUALLY exported in phase_b.nonnull_path.call vs my rel32
    # recompute at the pinned callsite 0x4C47C1 and my derived bridge
    # predicate. The pinned-role checks above stay as additional checks but
    # never replace comparing the value actually read from the JSON.
    bridge_ins = by_va_b[0x4C47C1]
    if bridge_ins.mn != "call":
        raise QCUnresolved("pinned bridge callsite 0x4C47C1 is not a call")
    rel_mine = int.from_bytes(bytes(int(b, 16)
                                    for b in bridge_ins.bytes[1:5]),
                              "little", signed=True)
    target_mine = 0x4C47C1 + 5 + rel_mine
    bvalid_mine = (target_mine == BRIDGE_ENTRY)
    ok, dg, val = qc_check_va_str(prov, "phase_b.nonnull_path.call.va",
                                  0x4C47C1)
    chk_d("QC-BR11-CALL-VA", "persisted bridge callsite VA (pinned 0x004C47C1)",
          val, va_s(0x4C47C1), ok, dg)
    ok, dg, val = qc_check_va_str(prov, "phase_b.nonnull_path.call.target",
                                  target_mine)
    chk_d("QC-BR11-CALL-TARGET", "persisted exported CALL target vs my "
          "rel32-derived target", val, va_s(target_mine), ok, dg)
    ok, dg, val = qc_check_va_str(prov,
                                  "phase_b.nonnull_path.call."
                                  "target_recomputed", target_mine)
    chk_d("QC-BR11-TARGET-RECOMPUTED", "persisted recomputed CALL target vs "
          "my rel32-derived target", val, va_s(target_mine), ok, dg)
    ok, dg, val = qc_check_bool(prov, "phase_b.nonnull_path.call."
                                "bridge_valid", bvalid_mine)
    chk_d("QC-BR11-BRIDGE-VALID", "persisted bridge_valid (native JSON "
          "boolean; false is not a valid positive predicate) vs my derived "
          "predicate target==window-A entry", val, bvalid_mine, ok, dg)

    # 6e-ter) BR-C1.2 persisted argument-slot identity vs MY walk (B slot -16
    # / E delta -20 / A entry [E+4]); the relation is DERIVED (E delta + A
    # entry delta == B slot delta), not duplicate-claims-only.
    ok, dg, val = qc_check_int(prov, "phase_b.nonnull_path.arg1."
                               "slot_delta_T0", b_slot)
    chk_d("QC-BR12-ARG1-SLOT-DELTA", "persisted arg1 slot delta (B slot) vs "
          "my walk-derived slot", val, b_slot, ok, dg)
    ok, dg, val = qc_check_int(prov, "phase_b.nonnull_path."
                               "arg_slot_deltas.arg1", b_slot)
    chk_d("QC-BR12-ARG-SLOT-DELTAS-ARG1", "persisted arg_slot_deltas.arg1 vs "
          "my walk-derived slot", val, b_slot, ok, dg)
    ok, dg, val = qc_check_slot_expr(prov, "bridge.b_arg1_slot", b_slot)
    chk_d("QC-BR12-B-ARG1-SLOT", "persisted bridge.b_arg1_slot expression vs "
          "my walk-derived slot", val, qc_slot_expr(b_slot), ok, dg)
    ok, dg, val = qc_check_int(prov, "bridge.E_delta_from_T", e_join)
    chk_d("QC-BR12-E-DELTA-FROM-T", "persisted E delta (callee-entry ESP "
          "under the join) vs my walk-derived delta", val, e_join, ok, dg)
    ok, dg, val = qc_check_int(prov, "phase_b.nonnull_path.call."
                               "esp_before_call_delta_T0", b_slot)
    chk_d("QC-BR12-ESP-BEFORE-CALL-DELTA", "persisted exported ESP-before-"
          "call delta vs my walk", val, b_slot, ok, dg)
    ok, dg, val = qc_check_int(prov, "phase_b.nonnull_path.call."
                               "callee_entry_esp_delta_T0", e_join)
    chk_d("QC-BR12-CALLEE-ENTRY-DELTA", "persisted exported callee-entry ESP "
          "delta vs my walk", val, e_join, ok, dg)
    present_ed, claimed_ed = field_get(prov, "bridge.E_delta_from_T")
    present_sd, claimed_sd = field_get(prov,
                                       "phase_b.nonnull_path.arg1."
                                       "slot_delta_T0")
    relation_ok = (e_join + my_src == b_slot
                   and present_ed and present_sd
                   and type(claimed_ed) is int and type(claimed_sd) is int
                   and claimed_ed + my_src == claimed_sd)
    chk_d("QC-BR12-SLOT-RELATION", "derived entry-slot relation [E+4] == "
          "[T-0x10] (E delta + A entry delta == B slot delta), persisted "
          "claims consistent with it",
          (claimed_ed, claimed_sd) if (present_ed and present_sd) else None,
          (e_join, b_slot), relation_ok,
          "VALUE_MISMATCH:my derived relation E delta %d + A entry delta %d "
          "== B slot %d not consistent with claimed values %r / %r"
          % (e_join, my_src, b_slot, claimed_ed, claimed_sd))

    # 6e-quater) BR-C1.3 persisted pointer value + duplicate bridge summary
    # (QC's OWN derivation): every representation compared individually to my
    # LEA/opcode-derived facts (no OR-fallback hides a contradictory parallel
    # representation); the clean pointer is ADDRESS(T+8), never MEM(T+8).
    # A's STACK_READ is the argument-slot load of the joined slot [E+4] (the
    # transmitted pointer), not a B-side pointee read.
    a_delivery_expr_mine = "MEM(E%s)@%s" % (fmt_off(my_src), va_s(0x528E84))
    ok, dg, val = qc_check_int(prov, "phase_b.nonnull_path.arg1."
                               "value_delta", lea_res_T)
    chk_d("QC-BR13-ARG1-VALUE-DELTA", "persisted arg1 value delta vs my "
          "LEA-derived delta", val, lea_res_T, ok, dg)
    ok, dg, val = qc_check_str(prov, "phase_b.nonnull_path.arg_slots.arg1."
                              "kind", kind_from_op)
    chk_d("QC-BR13-ARGSLOT-ARG1-KIND", "persisted arg_slots.arg1.kind vs my "
          "opcode-derived kind", val, kind_from_op, ok, dg)
    ok, dg, val = qc_check_arg_slot_expr(prov,
                                         "phase_b.nonnull_path.arg_slots."
                                         "arg1.expr", lea_res_T)
    chk_d("QC-BR13-ARGSLOT-ARG1-EXPR", "persisted arg_slots.arg1.expr "
          "(documented 'T0+0x8 (computed)' form, suffix normalized) vs my "
          "LEA-derived delta", val, "T0%s0x%x"
          % ("+" if lea_res_T >= 0 else "-", abs(lea_res_T)), ok, dg)
    ok, dg, val = qc_check_int(prov, "phase_b.nonnull_path.arg_slots.arg1."
                               "delta", lea_res_T)
    chk_d("QC-BR13-ARGSLOT-ARG1-DELTA", "persisted arg_slots.arg1.delta vs my "
          "LEA-derived delta", val, lea_res_T, ok, dg)
    ok, dg, val = qc_check_str(prov, "bridge.b_arg1_value_kind", kind_from_op)
    chk_d("QC-BR13-B-ARG1-VALUE-KIND", "persisted bridge.b_arg1_value_kind "
          "vs my opcode-derived kind (individual, no fallback)", val,
          kind_from_op, ok, dg)
    ok, dg, val = qc_check_addr_expr(prov, "bridge.b_arg1_value_expr",
                                     lea_res_T)
    chk_d("QC-BR13-B-ARG1-VALUE-EXPR", "persisted bridge.b_arg1_value_expr "
          "vs my LEA-derived pointer value (individual, no fallback)", val,
          my_expr, ok, dg)
    ok, dg, val = qc_check_addr_expr(prov, "bridge.cross_call_value_expr",
                                     lea_res_T)
    chk_d("QC-BR13-CROSSCALL-VALUE-EXPR", "persisted "
          "bridge.cross_call_value_expr vs my LEA-derived pointer value",
          val, my_expr, ok, dg)
    ok, dg, val = qc_check_str(prov, "bridge.a_delivered_value_kind",
                               "STACK_READ")
    chk_d("QC-BR13-A-DELIVERED-KIND", "persisted A-side delivered kind = "
          "STACK_READ of the joined argument slot [E+4] (the transmitted "
          "pointer), not a B-side pointee read", val, "STACK_READ", ok, dg)
    ok, dg, val = qc_check_str(prov, "phase_a.delivery.arg1_value_kind",
                               "STACK_READ")
    chk_d("QC-BR13-A-DELIVERY-KIND", "persisted A delivery arg1 value kind "
          "(argument-slot load)", val, "STACK_READ", ok, dg)
    ok, dg, val = qc_check_str(prov, "phase_a.delivery.arg1_value_expr",
                               a_delivery_expr_mine)
    chk_d("QC-BR13-A-DELIVERY-EXPR", "persisted A delivery arg1 expression "
          "vs my derived argument-slot load expression", val,
          a_delivery_expr_mine, ok, dg)
    present_vk, claimed_vk = field_get(prov,
                                       "phase_b.nonnull_path.arg1."
                                       "value_kind")
    present_sk, claimed_sk = field_get(prov,
                                       "phase_b.nonnull_path.arg_slots.arg1."
                                       "kind")
    present_bk, claimed_bk = field_get(prov, "bridge.b_arg1_value_kind")
    present_be, claimed_be = field_get(prov, "bridge.b_arg1_value_expr")
    present_ce, claimed_ce = field_get(prov, "bridge.cross_call_value_expr")
    present_ae, claimed_ae = field_get(prov,
                                       "phase_b.nonnull_path.arg1."
                                       "value_expr")
    parallel_ok = (present_vk and present_sk and present_bk
                   and present_be and present_ce and present_ae
                   and claimed_vk == claimed_sk == claimed_bk
                   == kind_from_op
                   and claimed_be == claimed_ce == claimed_ae == my_expr)
    chk_d("QC-BR13-PARALLEL-CONSISTENCY", "the three parallel kind "
          "representations and the three parallel value expressions agree "
          "with each other AND with my derivation",
          (claimed_vk, claimed_sk, claimed_bk, claimed_be, claimed_ce,
           claimed_ae),
          (kind_from_op, kind_from_op, kind_from_op, my_expr, my_expr,
           my_expr), parallel_ok,
          "VALUE_MISMATCH:contradictory parallel bridge representations "
          "(kinds %r/%r/%r, exprs %r/%r/%r vs my derived %r/%r)"
          % (claimed_vk, claimed_sk, claimed_bk, claimed_be, claimed_ce,
             claimed_ae, kind_from_op, my_expr))

    # 6e-quinquies) BR-C1.4 persisted null-path facts vs MY B-window branch
    # derivation: for EAX==0 (TEST EAX,EAX -> ZF=1, no intervening flag
    # writer in my census), JE at 0x4C47AD is taken; the taken path transfers
    # to 0x4C47C8 OUTSIDE window B before CALL 0x4C47C1, so the CALL is not
    # reached on this path. 0x4C47C8 remains unopened; no later-behavior
    # claim.
    je_ins = by_va_b[0x4C47AD]
    if je_ins.mn != "je":
        raise QCUnresolved("conditional branch at 0x4C47AD is not a je")
    je_target_mine = int(je_ins.ops.strip(), 16)
    exit_inside_mine = (WIN["B"]["va"] <= je_target_mine
                        < WIN["B"]["va"] + WIN["B"]["size"])
    je_conditional = (je_ins.bytes[0] == "74")
    ok, dg, val = qc_check_va_str(prov, "phase_b.null_path.branch_va",
                                  0x4C47AD)
    chk_d("QC-BR14-NULL-BRANCH-VA", "persisted null-path branch VA vs my "
          "decoded branch instruction", val, va_s(0x4C47AD), ok, dg)
    ok, dg, val = qc_check_str(prov, "phase_b.null_path.branch_mnemonic",
                               je_ins.mn)
    chk_d("QC-BR14-NULL-BRANCH-MNEMONIC", "persisted branch mnemonic vs my "
          "decoded instruction", val, je_ins.mn, ok, dg)
    ok, dg, val = qc_check_va_str(prov, "phase_b.null_path.exit_va",
                                  je_target_mine)
    chk_d("QC-BR14-NULL-EXIT-VA", "persisted exit VA vs my decoded JE target "
          "(0x004C47C8; unopened, no later-behavior claim)", val,
          va_s(je_target_mine), ok, dg)
    ok, dg, val = qc_check_bool(prov, "phase_b.null_path.exit_inside_window",
                                exit_inside_mine)
    chk_d("QC-BR14-NULL-EXIT-INSIDE", "persisted exit_inside_window vs my "
          "derived window-interval fact", val, exit_inside_mine, ok, dg)
    ok, dg, val = qc_check_bool(prov, "phase_b.null_path.je_taken", True)
    chk_d("QC-BR14-NULL-JE-TAKEN", "persisted je_taken (native JSON boolean) "
          "vs my branch derivation: EAX==0 -> ZF=1 -> JE taken", val, True,
          ok, dg)
    ok, dg, val = qc_check_bool(prov, "phase_b.null_path.unconditional_exit",
                                not je_conditional)
    chk_d("QC-BR14-NULL-UNCONDITIONAL", "persisted unconditional_exit vs my "
          "opcode-derived conditionality (0x74 = conditional Jcc)", val,
          not je_conditional, ok, dg)
    ok, dg, val = qc_check_bool(prov, "phase_b.null_path.call_reached", False)
    chk_d("QC-BR14-NULL-CALL-REACHED", "persisted call_reached (native JSON "
          "boolean): taken branch exits the window before CALL 0x4C47C1",
          val, False, ok, dg)

    # 6f) flags census TEST->JE (my mnemonic census)
    between = [i for i in ins["B"]
               if 0x4C47A3 < i.va < 0x4C47AD and i.mn in FLAG_MN]
    chk("PROV-B-FLAGS", "no flag-writing insn between TEST and JE (my census)",
        [], [va_s(i.va) for i in between], len(between) == 0)

    verdict = "PASS" if all(c["ok"] for c in checks) else "REJECTED"
    return checks, verdict


# ------------------------------------------------------------------ case matrix

def build_fixture(case, orig, win_key):
    if case in ("A_CLEAN", "B_CLEAN_NONNULL", "B_CLEAN_NULL"):
        return bytes(orig), "ORIGINAL", None
    mu = MUT[case]
    data = bytearray(orig)
    idx = mu["va"] - WIN[win_key]["va"]
    ob = [int(x, 16) for x in mu["orig"].split()]
    nb = [int(x, 16) for x in mu["new"].split()]
    if list(data[idx:idx + len(ob)]) != ob:
        raise QCUnresolved("mutation precondition mismatch at %s"
                           % va_s(mu["va"]))
    if len(ob) != len(nb):
        raise QCUnresolved("mutation changes length")
    data[idx:idx + len(nb)] = bytes(nb)
    return bytes(data), "SYNTHETIC_MUTATION", \
        "%s @%s: %s -> %s (synthetic copy; EXE untouched)" \
        % (case, va_s(mu["va"]), mu["orig"], mu["new"])


def run_matrix():
    cases_dir = os.path.join(WORK, "cases")
    os.makedirs(cases_dir, exist_ok=True)
    results = []
    for case in CASE_ORDER:
        win_key = "A" if case in ("A_CLEAN", "M1_A_FRAME", "M2_A_SLOT") \
            else "B"
        w = WIN[win_key]
        with open(EXE, "rb") as fh:
            fh.seek(w["raw"])
            orig = fh.read(w["size"])
        if sha_b(orig) != w["sha"]:
            raise QCUnresolved("original window %s identity failure" % win_key)
        data, kind, note = build_fixture(case, orig, win_key)
        fx = os.path.join(cases_dir, case + ".bin")
        with open(fx, "wb") as fh:
            fh.write(data)
        rc, out, cmd = run_objdump(fx, w["va"])
        rec = dict(case=case, window=win_key, input_kind=kind, mutation=note,
                   fixture_size=len(data), fixture_sha=sha_b(data),
                   fixture_note="identity hashes qualify ORIGINAL inputs "
                                "only; synthetic fixtures are analyzed, "
                                "never rejected by hash",
                   objdump_rc=rc, objdump_cmd=cmd, raw_stdout=out)
        if rc != 0:
            rec["verdict"] = "UNRESOLVED"
            rec["reason"] = "objdump rc=%d" % rc
            results.append(rec)
            continue
        try:
            ins = parse_dump(out, w["va"], w["va"] + w["size"])
            rec["decode"] = dict(
                instrs=len(ins), first=va_s(ins[0].va),
                last_end=va_s(ins[-1].va + ins[-1].n),
                covers=(ins[0].va == w["va"]
                        and ins[-1].va + ins[-1].n == w["va"] + w["size"]))
            d = {}
            if win_key == "A":
                af = derive_a(ins)
                d = dict(S=af["S"], src=af["src_off"],
                         src_disp=af["src_disp"],
                         preserved=af["preserved"], edi_ok=af["edi_ok"],
                         tail=af["target"], tail_rc=af["target_rc"],
                         arg1_kind=af["arg1_kind"],
                         arg1_text=af["arg1_text"],
                         arg1_slot=af["arg1_slot"],
                         esp_before=af["esp_before"],
                         callee_entry=af["callee_entry"],
                         esp_before_S=af["esp_before_S"],
                         callee_entry_S=af["callee_entry_S"],
                         arg1_slot_S=af["arg1_slot_S"],
                         push_va=af["push_va"], push_reg=af["push_reg"],
                         recv_kind=af["recv_kind"],
                         fs_stored_off=af["fs_stored_off"],
                         steps=af["steps"])
            else:
                bf = derive_b(ins)
                rec["path_count"] = bf["path_count"]
                if "null" in bf:
                    d["null"] = bf["null"]
                if "nonnull" in bf:
                    nn = bf["nonnull"]
                    t = nn["T"]
                    d.update(
                        T=t, flags_ok=nn["flags_ok"], br_mn=nn["br_mn"],
                        br_target=nn["br_target"], opaque=nn["opaque"],
                        val_insn=nn["val_insn"], reaches=True,
                        arg1_kind=nn["arg1"]["kind"],
                        arg1_T=(nn["arg1"]["off"] - t
                                if nn["arg1"]["off"] is not None else None),
                        arg1_slot=nn["arg1"]["slot"] - t,
                        arg1_slot_T0=nn["arg1"]["slot"],
                        push_va=nn["arg1"]["push_va"],
                        push_reg=nn["arg1"]["push_reg"],
                        recv_kind=nn["recv"]["kind"],
                        target=nn["call"]["target"],
                        target_rc=nn["call"]["target_rc"],
                        bvalid=nn["call"]["bvalid"],
                        esp_before=nn["call"]["esp_before"],
                        callee_entry=nn["call"]["callee_entry"],
                        aslots={k: [v[0], (v[1] - t) if v[1] is not None
                                    else None] for k, v in
                                nn["aslots"].items()})
                else:
                    nl = bf.get("null", {})
                    d.update(reaches=False,
                             uncond=nl.get("uncond", False),
                             call_reached=False)
            rec["derived"] = d
            # compare against MY expected facts (contract-encoded)
            e = EXP[case]
            cmp = []

            def add(field, got, want):
                cmp.append(dict(fact=field, got=got, want=want,
                                ok=(got == want)))
            if case in ("A_CLEAN", "M1_A_FRAME", "M2_A_SLOT"):
                add("S", d.get("S"), e["S"])
                add("src", d.get("src"), e["src"])
                if "preserved" in e:
                    add("preserved", d.get("preserved"), e["preserved"])
                    add("edi_ok", d.get("edi_ok"), e["edi_ok"])
                    add("tail", d.get("tail"), e["tail"])
                    add("arg1_kind", d.get("arg1_kind"), e["arg1_kind"])
            elif case == "B_CLEAN_NULL":
                nl = d.get("null", {})
                add("je_taken", nl.get("je"), e["je"])
                add("call_reached", nl.get("call_reached"), e["call_reached"])
                add("delivered_None", nl.get("delivered") is None,
                    e["delivered_None"])
            elif case == "M6_B_SKIP":
                add("reaches", d.get("reaches"), e["reaches"])
                add("uncond", d.get("uncond"), e["uncond"])
                add("call_reached", d.get("call_reached", False), False)
            else:
                if "T" in e:
                    add("T", d.get("T"), e["T"])
                if "reaches" in e:
                    add("reaches", d.get("reaches"), e["reaches"])
                if "flags_ok" in e:
                    add("flags_ok", d.get("flags_ok"), e["flags_ok"])
                if "arg1" in e:
                    add("arg1_kind", d.get("arg1_kind"), e["arg1"][0])
                    add("arg1_off", d.get("arg1_T"), e["arg1"][1])
                if "slot1" in e:
                    add("arg1_slot", d.get("arg1_slot"), e["slot1"])
                if "a2" in e:
                    add("arg2_kind", d.get("aslots", {}).get("a2",
                                                            [None])[0],
                        e["a2"])
                if "a3" in e:
                    add("arg3", d.get("aslots", {}).get("a3",
                                                        [None, None])[:2],
                        list(e["a3"]))
                    add("arg4", d.get("aslots", {}).get("a4",
                                                        [None, None])[:2],
                        list(e["a4"]))
                if "recv" in e:
                    add("recv_kind", d.get("recv_kind"), e["recv"])
                if "actual_target" in e:
                    add("actual_target", d.get("target"), e["actual_target"])
                    add("target_rc", d.get("target_rc"), e["actual_target"])
                    add("bvalid", d.get("bvalid"), e["bvalid"])
                elif "target" in e:
                    add("target", d.get("target"), e["target"])
                    add("bvalid", d.get("bvalid"), e["bvalid"])
                if case == "M7_B_RECEIVER_ONLY":
                    add("recv_is_esi_UNK", d.get("recv_kind") == "UNK",
                        e["recv_esi"])
            rec["checks"] = cmp
            rec["verdict"] = ("CONTROL_PASS"
                              if cmp and all(c["ok"] for c in cmp)
                              else "CONTROL_FAIL")
        except QCUnresolved as ex:
            rec["verdict"] = "UNRESOLVED"
            rec["reason"] = str(ex)
            rec["note"] = "fail-closed: unsupported construct; the " \
                          "expected result was NOT filled in"
        results.append(rec)
    return results


def prod_compare(matrix):
    """Compare MY 12 case outcomes field-by-field with the PRODUCTION 12
    outcomes recorded in the package's CONTROL_RESULTS.json (the other half
    of the 24-outcome matrix). Production records are read ONLY for this
    comparison, never as a derivation input."""
    prod = json.load(open(os.path.join(PKG, "CONTROL_RESULTS.json")))
    by_case = {c["case"]: c for c in prod["cases"]}
    rows = []
    for rec in matrix:
        case = rec["case"]
        pc = by_case.get(case)
        if pc is None:
            rows.append(dict(case=case, prod_verdict="MISSING",
                             qc_verdict=rec["verdict"], agree=False))
            continue
        pf = pc.get("derived_facts") or {}
        mine = rec.get("derived") or {}
        agree = (pc.get("verdict") == rec["verdict"])
        diffs = []

        def eq(field, prod_val, my_val):
            if prod_val != my_val:
                agree = False
                diffs.append(dict(field=field, prod=prod_val, mine=my_val))
        if case in ("A_CLEAN", "M1_A_FRAME", "M2_A_SLOT"):
            eq("S", pf.get("S_delta"), mine.get("S"))
            eq("src", pf.get("source_slot_delta"), mine.get("src"))
            if "entry_slot_value_preserved" in pf:
                eq("preserved", pf.get("entry_slot_value_preserved"),
                   mine.get("preserved"))
                eq("edi_ok", pf.get("edi_preserved"), mine.get("edi_ok"))
                eq("tail", pf.get("tail_target"),
                   va_s(mine.get("tail")) if mine.get("tail") is not None
                   else None)
                eq("arg1_kind",
                   "MEM" if pf.get("arg1_kind") == "STACK_READ"
                   else pf.get("arg1_kind"), mine.get("arg1_kind"))
        else:
            nl = mine.get("null") or {}
            if "nonnull_reaches_call" in pf:
                eq("reaches", pf.get("nonnull_reaches_call"),
                   mine.get("reaches"))
            if "T_delta" in pf:
                eq("T", pf.get("T_delta"), mine.get("T"))
            if "arg1_kind" in pf:
                eq("arg1_kind",
                   "ADDR" if pf.get("arg1_kind") == "ADDRESS" else "MEM",
                   mine.get("arg1_kind"))
                eq("arg1_expr", parse_prod_expr(pf.get("arg1_expr")),
                   [mine.get("arg1_kind"), mine.get("arg1_T")])
                eq("arg1_slot", pf.get("arg1_slot_delta"),
                   mine.get("arg1_slot"))
            if "receiver_kind" in pf:
                eq("recv_kind",
                   {"OPAQUE_RET": "OPRET",
                    "UNKNOWN_REG": "UNK"}.get(pf.get("receiver_kind")),
                   mine.get("recv_kind"))
            if "bridge_target_actual" in pf:
                eq("target", pf.get("bridge_target_actual"),
                   va_s(mine.get("target")) if mine.get("target") is not None
                   else None)
                eq("bvalid", pf.get("bridge_valid"), mine.get("bvalid"))
            if "arg3_expr" in pf:
                eq("arg3", parse_prod_expr(pf.get("arg3_expr")),
                   (mine.get("aslots", {}).get("a3") or [None, None])[:2])
                eq("arg4", parse_prod_expr(pf.get("arg4_expr")),
                   (mine.get("aslots", {}).get("a4") or [None, None])[:2])
            if "null_je_taken" in pf:
                eq("null_je", pf.get("null_je_taken"), nl.get("je"))
                eq("null_call_reached", pf.get("null_call_reached"),
                   nl.get("call_reached"))
            if "unconditional_exit" in pf:
                eq("uncond", pf.get("unconditional_exit"),
                   mine.get("uncond", nl.get("uncond")))
        rows.append(dict(case=case, prod_verdict=pc.get("verdict"),
                         qc_verdict=rec["verdict"], agree=agree,
                         diffs=diffs))
    return rows


# ------------------------------------------------------------------ package scans

def raw_va_census(pkg):
    """Parse EVERY persisted raw objdump file in the package; assert all
    decoded VAs lie inside window A or window B (zero package evidence of
    any other code / callee bodies)."""
    out = []
    for root, _dirs, files in os.walk(os.path.join(pkg, "01_RAW")):
        for f in sorted(files):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, pkg).replace("\\", "/")
            raw = open(p, "r", encoding="utf-8", errors="replace").read()
            body = raw.split("--- RAW OUTPUT BELOW ---", 1)[-1]
            vas = []
            for line in body.splitlines():
                m = LINE_RE.match(line)
                if m:
                    vas.append(int(m.group(1), 16))
            uniq = sorted(set(vas))
            outside = [v for v in uniq
                       if not (0x528E50 <= v < 0x528E92
                               or 0x4C4792 <= v < 0x4C47C6)]
            out.append(dict(file=rel, va_lines=len(vas),
                            unique_vas=len(uniq),
                            outside_count=len(outside),
                            outside=[va_s(v) for v in outside[:8]]))
    return out


def standing_scan(pkg):
    """Token scan over the executor's package text files: forbidden standing
    must be absent; required fences must be present."""
    forbidden = {
        "WORLD_XYZ_RECOVERED = YES": [],
        "WORLD_XYZ_RECOVERED=YES": [],
        "FIELD_SEMANTICS = VERIFIED": [],
        "FIELD_SEMANTICS=VERIFIED": [],
        "WORLD_INSTANCE_IDENTITY = ESTABLISHED": [],
        "HISTORICAL_PLACEMENT = ESTABLISHED": [],
        "SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = CONFIRMED_STATIC": [],
    }
    required = {
        "ARG1_DIRECT_SOURCE = CONFIRMED_STATIC_CONDITIONAL": 0,
        "CMO_C1 = CLOSED_FOR_AUDITED_STATE": 0,
        "CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL": 0,
        "PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED": 0,
        "NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION": 0,
        "SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE": 0,
        "WORLD_XYZ_RECOVERED = NO": 0,
        "FIELD_SEMANTICS = UNVERIFIED": 0,
        "POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM": 0,
        "WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED": 0,
        "HISTORICAL_PLACEMENT = NOT_ESTABLISHED": 0,
    }
    files = []
    for root, _d, fs in os.walk(pkg):
        for f in fs:
            rel = os.path.relpath(os.path.join(root, f), pkg).replace("\\", "/")
            if rel in ("QC_RESULTS.json", "QC_REPORT.md",
                       "03_SCRIPTS/qc_frame_bridge.py"):
                continue
            files.append(rel)
    hits_ctx = {}
    for rel in sorted(files):
        p = os.path.join(pkg, rel)
        try:
            txt = open(p, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for tok in forbidden:
            if tok in txt:
                forbidden[tok].append(rel)
        for tok in required:
            required[tok] += txt.count(tok)
        for pat in ("NiPoint3", "ACLD", "pointee"):
            flags = re.IGNORECASE if pat == "pointee" else 0
            for m in re.finditer(re.escape(pat), txt, flags):
                s = max(0, m.start() - 60)
                hits_ctx.setdefault(pat, []).append(
                    "%s :: ...%s..." % (rel,
                                        txt[s:m.end() + 60].replace("\n", " ")))
    return dict(files_scanned=len(files),
                forbidden=forbidden,
                forbidden_clean=all(len(v) == 0 for v in forbidden.values()),
                required=required,
                required_all_present=all(v > 0 for v in required.values()),
                context_hits={k: v[:16] for k, v in hits_ctx.items()})


def crash_checks(pkg, my_raw_A, my_raw_B):
    """Verify the crash-continuation claims physically."""
    res = {}
    for rel in ("01_RAW/WINDOW_A_OBJDUMP.txt", "01_RAW/WINDOW_B_OBJDUMP.txt"):
        got = sha_file(os.path.join(pkg, rel))
        res[rel] = dict(sha=got, expect=DISCOVERY_SHA[rel],
                        unchanged_since_discovery=(got == DISCOVERY_SHA[rel]))
    pr = open(os.path.join(pkg, "PREREGISTRATION.md"), "rb").read()
    res["PREREGISTRATION.md"] = dict(
        size=len(pr), full_sha=sha_b(pr),
        prefix_19151_sha=sha_b(pr[:19151]),
        prefix_matches_discovery=(sha_b(pr[:19151])
                                  == DISCOVERY_SHA["PREREGISTRATION_prefix_19151"]),
        note="P1-P9 are byte-identical to the crashed session's "
             "preregistration (pure P10 append) iff "
             "prefix_matches_discovery is true")

    def lines_of(raw):
        return [l.rstrip() for l in raw.splitlines()
                if re.match(r"^\s+[0-9a-f]+:", l)]
    for tag, myraw in (("A", my_raw_A), ("B", my_raw_B)):
        kept = open(os.path.join(pkg, WIN[tag]["raw_file"])).read()
        retr = open(os.path.join(pkg, WIN[tag]["retry_file"])).read()
        res["ident_%s" % tag] = dict(
            mine_vs_crashkept=lines_of(myraw) == lines_of(kept),
            mine_vs_retry=lines_of(myraw) == lines_of(retr),
            crashkept_vs_retry=lines_of(kept) == lines_of(retr),
            my_line_count=len(lines_of(myraw)),
            kept_line_count=len(lines_of(kept)))
    return res


def st_defs_eax_lea(insA):
    """Cross-check: the EAX value defined by LEA at 0x528E6C (the address
    stored to FS:[0]) measured by a targeted micro-replay."""
    st = St(entry_receiver=True, suffix="ENTRY")
    for i in insA:
        if i.va == 0x528E6C:
            exec1(st, i)
            return st.regs["eax"].off
        exec1(st, i)
    return None


# ------------------------------------------------------------------ main

def main():
    os.makedirs(WORK, exist_ok=True)
    out = dict(
        run_id="PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009",
        qc_origin="pe-master-auditor fresh-context internal QC (internal to "
                  "PE-MASTER; NOT an independent Desktop post-audit; NOT "
                  "executor self-review)",
        qc_session="OpenCode pe-master-auditor session 2026-10-09, model "
                   "nask-glm/glm-5-3; python3 -B (WSL PE-AI, Debian, kernel "
                   "6.18.33.2-microsoft-standard-WSL2)",
        independence=dict(
            window_extraction_hashing_pe_mapping="INDEPENDENT (this session)",
            disassembler="SAME TOOL as production (GNU objdump 2.44 via WSL "
                         "PE-AI) - the same GNU objdump is NOT two "
                         "independent disassemblers (honest; not claimed as "
                         "a cross-disassembler check)",
            objdump_invocations="INDEPENDENT (this session's own commands; "
                                "rc recorded per invocation)",
            symbolic_replay="INDEPENDENT implementation "
                            "(03_SCRIPTS/qc_frame_bridge.py; does NOT "
                            "import run_frame_bridge.py)",
            esp_walk="INDEPENDENT minimal arithmetic walk (separate "
                     "function from the replay engine)",
            expected_facts="re-encoded from the CONTRACT section 7 matrix "
                          "by this session",
            artifact_gate="INDEPENDENT implementation (gate())",
            executor_artifacts="read ONLY for agree/disagree adjudication "
                                "(adjudication + prod_compare), never as "
                                "derivation input"))

    # 0) EXE identity before
    sha0 = sha_file(EXE)
    out["exe_before"] = dict(size=os.path.getsize(EXE), sha=sha0,
                             pin_match=(sha0 == EXE_SHA_PIN))
    if sha0 != EXE_SHA_PIN:
        print(json.dumps({"QC_BLOCKED": "EXE identity mismatch"}))
        return 2

    ver, vrc = objdump_version()
    out["tool"] = dict(name=ver, version_rc=vrc,
                      command_form="objdump -D -b binary -m i386 -M intel "
                                   "--adjust-vma=<VA> <fixture.bin>")

    # 1) my own window extraction + PE mapping (identity/mapping only)
    with open(EXE, "rb") as fh:
        blob_all = fh.read()
    e_lfanew = struct.unpack_from("<I", blob_all, 0x3C)[0]
    coff = e_lfanew + 4
    machine, nsec, _3, _4, _5, opt_size, _6 = struct.unpack_from(
        "<HHIIIHH", blob_all, coff)
    opt = coff + 20
    image_base = struct.unpack_from("<I", blob_all, opt + 28)[0]
    sections = []
    for i in range(nsec):
        off = opt + opt_size + 40 * i
        name = blob_all[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
        vsize, vaddr, rsize, raddr = struct.unpack_from(
            "<IIII", blob_all, off + 8)
        sections.append(dict(name=name, va=vaddr, vsize=vsize, raw=raddr,
                            rsize=rsize))
    win_extract = {}
    for key in ("A", "B"):
        w = WIN[key]
        rva = w["va"] - image_base
        hit = None
        for s in sections:
            if s["va"] <= rva < s["va"] + s["vsize"]:
                hit = s
        if hit is None:
            raise QCUnresolved("window %s maps to no section" % key)
        raw_off = rva - hit["va"] + hit["raw"]
        data = blob_all[w["raw"]:w["raw"] + w["size"]]
        win_extract[key] = dict(
            rva=rva, section=hit["name"], section_va=hit["va"],
            section_vsize=hit["vsize"], section_rsize=hit["rsize"],
            raw_backed=hit["rsize"] > 0,
            raw_offset_formula=raw_off, raw_offset_pinned=w["raw"],
            formula_match=(raw_off == w["raw"]),
            size=len(data), sha=sha_b(data),
            pin_match=(sha_b(data) == w["sha"]),
            inside_raw_range=(hit["raw"] <= w["raw"]
                              and w["raw"] + w["size"]
                              <= hit["raw"] + hit["rsize"]))
    out["pe_mapping"] = dict(image_base=image_base, machine=machine,
                             sections=sections, windows=win_extract)
    out["pe_disjoint"] = bool(
        WIN["A"]["raw"] + WIN["A"]["size"] <= WIN["B"]["raw"]
        or WIN["B"]["raw"] + WIN["B"]["size"] <= WIN["A"]["raw"])
    out["unique_bytes"] = WIN["A"]["size"] + WIN["B"]["size"]

    # 2) my own fresh objdump for the original windows; persist raw stdout
    raw_mine = {}
    for key in ("A", "B"):
        w = WIN[key]
        fx = os.path.join(WORK, "qc_window_%s.bin" % key)
        with open(fx, "wb") as fh:
            fh.write(blob_all[w["raw"]:w["raw"] + w["size"]])
        rc, raw, cmd = run_objdump(fx, w["va"])
        raw_mine[key] = dict(rc=rc, cmd=cmd, raw=raw)
    out["my_window_objdump"] = {k: dict(rc=v["rc"], cmd=v["cmd"],
                                        raw_stdout=v["raw"])
                                for k, v in raw_mine.items()}

    # 3) crash-continuation verification (physical)
    out["crash_verification"] = crash_checks(PKG, raw_mine["A"]["raw"],
                                             raw_mine["B"]["raw"])

    # 4) clean-window derivations (Phase A, Phase B, bridge) - MY OWN
    insA = parse_dump(raw_mine["A"]["raw"], WIN["A"]["va"],
                      WIN["A"]["va"] + WIN["A"]["size"])
    insB = parse_dump(raw_mine["B"]["raw"], WIN["B"]["va"],
                     WIN["B"]["va"] + WIN["B"]["size"])
    af = derive_a(insA)
    bf = derive_b(insB)
    join = bridge_join(af, bf)
    out["phase_a_mine"] = {k: v for k, v in af.items()
                           if not k.startswith("_")}
    out["phase_b_mine"] = dict(path_count=bf["path_count"],
                               instr_count=bf["instr_count"])
    if "null" in bf:
        out["phase_b_mine"]["null"] = bf["null"]
    if "nonnull" in bf:
        nn = bf["nonnull"]
        out["phase_b_mine"]["nonnull"] = {k: v for k, v in nn.items()
                                          if k not in ("steps", "_writes")}
        out["phase_b_mine"]["nonnull"]["steps"] = nn["steps"]
        out["phase_b_mine"]["nonnull"]["writes"] = [
            [w[0], w[1], w[2], w[3].text] for w in nn["_writes"]]
    out["bridge_mine"] = join

    # 5) adjudication: executor's claims vs my measurements (field-by-field)
    adj = []

    def adj_f(field, claimed, mine, ok=None):
        ok = (claimed == mine) if ok is None else ok
        adj.append(dict(field=field, claimed=claimed, mine=mine,
                        agree=bool(ok)))
    a = af
    bnn = bf.get("nonnull")
    bnull = bf.get("null")
    adj_f("A.window.size", EXEC_CLAIMS["window_A"]["size"], WIN["A"]["size"])
    adj_f("A.window.instrs", EXEC_CLAIMS["window_A"]["instrs"], len(insA))
    adj_f("A.window.first", EXEC_CLAIMS["window_A"]["first"], insA[0].va)
    adj_f("A.window.last_end", EXEC_CLAIMS["window_A"]["last_end"],
          insA[-1].va + insA[-1].n)
    adj_f("A.tail_target", EXEC_CLAIMS["window_A"]["call"]["target"],
          a["target"])
    adj_f("A.S_delta", EXEC_CLAIMS["phase_a"]["S_delta"], a["S"])
    adj_f("A.src_slot_delta", EXEC_CLAIMS["phase_a"]["src_slot_delta"],
          a["src_off"])
    adj_f("A.src_slot_expr", EXEC_CLAIMS["phase_a"]["src_slot"],
          a["src_slot_E"])
    adj_f("A.src_pivot_expr", EXEC_CLAIMS["phase_a"]["src_pivot"],
          a["src_slot_S"])
    adj_f("A.preserved", EXEC_CLAIMS["phase_a"]["preserved"], a["preserved"])
    adj_f("A.edi_ok", EXEC_CLAIMS["phase_a"]["edi_ok"], a["edi_ok"])
    adj_f("A.edi_def", EXEC_CLAIMS["phase_a"]["edi_def"], a["edi_def"])
    adj_f("A.push_va", EXEC_CLAIMS["phase_a"]["push_va"], a["push_va"])
    adj_f("A.push_reg", EXEC_CLAIMS["phase_a"]["push_reg"], a["push_reg"])
    adj_f("A.esp_before_call", EXEC_CLAIMS["phase_a"]["esp_before"],
          a["esp_before"])
    adj_f("A.callee_entry", EXEC_CLAIMS["phase_a"]["callee_entry"],
          a["callee_entry"])
    adj_f("A.arg1_slot_S", EXEC_CLAIMS["phase_a"]["arg1_slot_S"],
          a["arg1_slot_S"])
    adj_f("A.callee_entry_S", EXEC_CLAIMS["phase_a"]["callee_entry_S"],
          a["callee_entry_S"])
    adj_f("A.esp_before_S", EXEC_CLAIMS["phase_a"]["arg1_slot_S"],
          a["esp_before_S"])
    adj_f("A.arg1_kind", EXEC_CLAIMS["phase_a"]["arg1_kind"],
          a["arg1_kind"],
          ok=(EXEC_CLAIMS["phase_a"]["arg1_kind"] == "STACK_READ"
              and a["arg1_kind"] == "MEM"))
    adj_f("A.stack_write_offs", EXEC_CLAIMS["phase_a"]["stack_write_offs"],
          a["stack_write_offs"])
    adj_f("A.seg_writes", EXEC_CLAIMS["phase_a"]["seg_writes"],
          [g[1] for g in a["segbefore"]])
    adj_f("A.recv_kind", EXEC_CLAIMS["phase_a"]["recv_kind"], a["recv_kind"],
          ok=(EXEC_CLAIMS["phase_a"]["recv_kind"] == "ENTRY_RECEIVER"
              and a["recv_kind"] == "RECV"))
    adj_f("A.fs_stored_off", EXEC_CLAIMS["phase_a"]["fs_stored_off"],
          a["fs_stored_off"])
    adj_f("B.window.size", EXEC_CLAIMS["window_B"]["size"], WIN["B"]["size"])
    adj_f("B.window.instrs", EXEC_CLAIMS["window_B"]["instrs"], len(insB))
    adj_f("B.window.first", EXEC_CLAIMS["window_B"]["first"], insB[0].va)
    adj_f("B.window.last_end", EXEC_CLAIMS["window_B"]["last_end"],
          insB[-1].va + insB[-1].n)
    adj_f("B.calls", EXEC_CLAIMS["window_B"]["calls"],
          [(i.va, int(i.ops.strip(), 16)) for i in insB if i.mn == "call"])
    if bnn:
        adj_f("B.T_delta", EXEC_CLAIMS["phase_b"]["T_delta"], bnn["T"])
        adj_f("B.flags_ok", EXEC_CLAIMS["phase_b"]["flags_ok"],
              bnn["flags_ok"])
        adj_f("B.je_target", EXEC_CLAIMS["phase_b"]["je_target"],
              bnn["br_target"])
        adj_f("B.opaque.push128",
              EXEC_CLAIMS["phase_b"]["opaque"]["push"] == 0x128,
              bnn["opaque"]["push128"])
        adj_f("B.opaque.add_esp4",
              EXEC_CLAIMS["phase_b"]["opaque"]["cleanup"] == 4,
              bnn["opaque"]["add_esp4"])
        adj_f("B.lea.kind", EXEC_CLAIMS["phase_b"]["lea"]["kind"],
              bnn["val_insn"]["kind"],
              ok=(EXEC_CLAIMS["phase_b"]["lea"]["kind"] == "ADDRESS"
                  and bnn["val_insn"]["kind"] == "ADDR"))
        adj_f("B.lea.disp", EXEC_CLAIMS["phase_b"]["lea"]["disp"],
              bnn["val_insn"]["disp"])
        adj_f("B.arg1.kind", EXEC_CLAIMS["phase_b"]["arg1"]["kind"],
              bnn["arg1"]["kind"],
              ok=(EXEC_CLAIMS["phase_b"]["arg1"]["kind"] == "ADDRESS"
                  and bnn["arg1"]["kind"] == "ADDR"))
        adj_f("B.arg1.slot", EXEC_CLAIMS["phase_b"]["arg1"]["slot"],
              bnn["arg1"]["slot"])
        adj_f("B.arg1.val", EXEC_CLAIMS["phase_b"]["arg1"]["val"],
              bnn["arg1"]["off"])
        adj_f("B.arg1.push_va", EXEC_CLAIMS["phase_b"]["arg1"]["push_va"],
              bnn["arg1"]["push_va"])
        adj_f("B.arg1.push_reg", EXEC_CLAIMS["phase_b"]["arg1"]["push_reg"],
              bnn["arg1"]["push_reg"])
        adj_f("B.arg2", EXEC_CLAIMS["phase_b"]["args"]["a2"],
              (bnn["aslots"].get("a2") or [None, None, None])[2])
        adj_f("B.arg3", list(EXEC_CLAIMS["phase_b"]["args"]["a3"]),
              [bnn["aslots"]["a3"][0], bnn["aslots"]["a3"][1] - bnn["T"]])
        adj_f("B.arg4", list(EXEC_CLAIMS["phase_b"]["args"]["a4"]),
              [bnn["aslots"]["a4"][0], bnn["aslots"]["a4"][1] - bnn["T"]])
        adj_f("B.recv.kind", EXEC_CLAIMS["phase_b"]["recv"]["kind"],
              bnn["recv"]["kind"],
              ok=(EXEC_CLAIMS["phase_b"]["recv"]["kind"] == "OPAQUE_RET"
                  and bnn["recv"]["kind"] == "OPRET"))
        adj_f("B.call.target", EXEC_CLAIMS["phase_b"]["call"]["target"],
              bnn["call"]["target"])
        adj_f("B.call.esp_before", EXEC_CLAIMS["phase_b"]["call"]["esp_before"],
              bnn["call"]["esp_before"])
        adj_f("B.call.callee_entry",
              EXEC_CLAIMS["phase_b"]["call"]["callee_entry"],
              bnn["call"]["callee_entry"])
        adj_f("B.call.bvalid", EXEC_CLAIMS["phase_b"]["call"]["bvalid"],
              bnn["call"]["bvalid"])
    if bnull:
        adj_f("B.null.je", EXEC_CLAIMS["phase_b"]["null"]["je"], bnull["je"])
        adj_f("B.null.reached", EXEC_CLAIMS["phase_b"]["null"]["reached"],
              bnull["call_reached"])
    adj_f("BR.join", EXEC_CLAIMS["bridge"]["join"], join["join"])
    adj_f("BR.slot_identity", EXEC_CLAIMS["bridge"]["slot_T"],
          join["a_src_T"],
          ok=(join.get("slot_identity") is True
              and join.get("a_src_T") == EXEC_CLAIMS["bridge"]["slot_T"]))
    adj_f("BR.value", EXEC_CLAIMS["bridge"]["val"],
          join["cross_value"][1] if "cross_value" in join else None)
    adj_f("BR.intervening", EXEC_CLAIMS["bridge"]["intervening"],
          join.get("intervening", []))
    adj_f("BR.status", EXEC_CLAIMS["bridge"]["status"], join["status"])
    out["adjudication"] = adj
    out["adjudication_summary"] = dict(
        fields=len(adj), agree=sum(1 for r in adj if r["agree"]),
        disagree=[r["field"] for r in adj if not r["agree"]])

    # 6) 12-case matrix through MY analysis predicate
    matrix = run_matrix()
    out["matrix_qc"] = matrix
    out["matrix_qc_summary"] = dict(
        cases=len(matrix),
        control_pass=sum(1 for c in matrix if c["verdict"] == "CONTROL_PASS"),
        control_fail=sum(1 for c in matrix if c["verdict"] == "CONTROL_FAIL"),
        unresolved=sum(1 for c in matrix if c["verdict"] == "UNRESOLVED"))

    # 6b) the other half of the 24-outcome matrix: production records vs mine
    pcmp = prod_compare(matrix)
    out["prod_vs_qc"] = pcmp
    out["prod_vs_qc_summary"] = dict(
        cases=len(pcmp),
        agree=sum(1 for r in pcmp if r["agree"]),
        disagree=[r["case"] for r in pcmp if not r["agree"]])

    # 7) artifact gate: baseline + AC1/AC2 re-runs through MY gate
    base_checks, base_verdict = gate(PKG)
    out["artifact_gate_qc"] = dict(baseline=dict(
        checks=base_checks, verdict=base_verdict,
        check_count=len(base_checks),
        all_pass=all(c["ok"] for c in base_checks)))
    ac = {}
    if base_verdict == "PASS":
        prov = json.load(open(os.path.join(PKG, "BRIDGE_PROVENANCE.json")))
        acdir = os.path.join(WORK, "artifact_controls")
        os.makedirs(acdir, exist_ok=True)
        ac1 = copy.deepcopy(prov)
        ac1["phase_b"]["nonnull_path"]["arg1"]["value_kind"] = "STACK_READ"
        ac1["phase_b"]["nonnull_path"]["arg1"]["value_expr"] = "MEM(T+0x8)"
        ac1["bridge"]["b_arg1_value_kind"] = "STACK_READ"
        ac1["bridge"]["b_arg1_value_expr"] = "MEM(T+0x8)"
        if "cross_call_value_expr" in ac1["bridge"]:
            ac1["bridge"]["cross_call_value_expr"] = "MEM(T+0x8)"
        p1 = os.path.join(acdir, "BRIDGE_PROVENANCE_AC1.json")
        with open(p1, "w") as fh:
            json.dump(ac1, fh, indent=2)
        c1, v1 = gate(PKG, prov_override=p1)
        ac["AC1"] = dict(mutation="copied BRIDGE_PROVENANCE.json: clean arg1 "
                         "value kind/expression replaced ADDRESS(T+8) -> "
                         "MEM(T+8)",
                         verdict=v1,
                         result=("CONTROL_PASS" if v1 == "REJECTED"
                                 else "CONTROL_FAIL"),
                         failing=[c["check"] for c in c1 if not c["ok"]],
                         checks=c1)
        ac2 = copy.deepcopy(prov)
        ac2["phase_a"]["source_slot"]["slot_expr_from_E"] = "[E+0x8]"
        ac2["phase_a"]["source_slot"]["slot_delta_from_E"] = 8
        p2 = os.path.join(acdir, "BRIDGE_PROVENANCE_AC2.json")
        with open(p2, "w") as fh:
            json.dump(ac2, fh, indent=2)
        c2, v2 = gate(PKG, prov_override=p2)
        ac["AC2"] = dict(mutation="copied BRIDGE_PROVENANCE.json: clean "
                         "entry source [E+4] -> [E+8]",
                         verdict=v2,
                         result=("CONTROL_PASS" if v2 == "REJECTED"
                                 else "CONTROL_FAIL"),
                         failing=[c["check"] for c in c2 if not c["ok"]],
                         checks=c2)
    out["artifact_gate_qc"]["controls"] = ac
    out["artifact_gate_qc"]["overall"] = (
        "ARTIFACT_CONSISTENCY_PASS"
        if base_verdict == "PASS"
        and ac.get("AC1", {}).get("result") == "CONTROL_PASS"
        and ac.get("AC2", {}).get("result") == "CONTROL_PASS"
        else "ARTIFACT_CONTROL_FAILURE_OR_BASELINE_FAIL")

    # 8) package raw-VA census + standing scan
    out["raw_va_census"] = raw_va_census(PKG)
    out["raw_va_census_summary"] = dict(
        files=len(out["raw_va_census"]),
        outside_total=sum(r["outside_count"] for r in out["raw_va_census"]))
    out["standing_scan"] = standing_scan(PKG)

    # 9) EXE identity after
    sha1 = sha_file(EXE)
    out["exe_after"] = dict(sha=sha1, unchanged=(sha1 == sha0 == EXE_SHA_PIN))

    # verdict inputs (the QC_PASS decision is reported; the final verdict
    # text is written by the QC session in QC_RESULTS/QC_REPORT)
    m_ok = (out["matrix_qc_summary"]["control_pass"] == 12
            and out["matrix_qc_summary"]["control_fail"] == 0
            and out["matrix_qc_summary"]["unresolved"] == 0)
    a_ok = out["artifact_gate_qc"]["overall"] == "ARTIFACT_CONSISTENCY_PASS"
    d_ok = out["adjudication_summary"]["disagree"] == []
    p_ok = out["prod_vs_qc_summary"]["agree"] == 12
    crash_ok = (out["crash_verification"]
                ["01_RAW/WINDOW_A_OBJDUMP.txt"]["unchanged_since_discovery"]
                and out["crash_verification"]
                ["01_RAW/WINDOW_B_OBJDUMP.txt"]["unchanged_since_discovery"]
                and out["crash_verification"]["PREREGISTRATION.md"]
                ["prefix_matches_discovery"]
                and out["crash_verification"]["ident_A"]["mine_vs_crashkept"]
                and out["crash_verification"]["ident_B"]["mine_vs_crashkept"])
    scope_ok = (out["raw_va_census_summary"]["outside_total"] == 0
                and out["standing_scan"]["forbidden_clean"])
    prod12_ok = (out["prod_vs_qc_summary"]["agree"] == 12)
    out["verdict_inputs"] = dict(
        production_12_outcomes_all_CONTROL_PASS=prod12_ok,
        qc_matrix_12_12=m_ok, artifact_controls=a_ok,
        adjudication_zero_disagreements=d_ok,
        prod_vs_qc_12_12_agree=p_ok,
        crash_continuation_physical=crash_ok,
        scope_standing_scan=scope_ok)

    with open(os.path.join(PKG, "QC_RESULTS.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("QC_RESULTS_WRITTEN")
    print("MATRIX:", json.dumps(out["matrix_qc_summary"]))
    print("ADJ:", json.dumps(out["adjudication_summary"]))
    print("PROD_VS_QC:", json.dumps(out["prod_vs_qc_summary"]))
    print("GATE:", out["artifact_gate_qc"]["overall"])
    print("CRASH_OK:", crash_ok, "SCOPE_OK:", scope_ok)
    return 0


if __name__ == "__main__":
    sys.exit(main())
