# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 - TASK F1-P (the bounded STATIC proof)
#
# QUESTION (exactly one): is the census row 0x0040525B receiver (base register edx of
# `mov dword ptr [edx+0x30], ebx`) PROVABLY never a SceneFeederObject pointer - via
# the global pointer slot 0x00B6C3D8 - so that REJECTED_ALIAS stands with the
# corrected justification R-GLOBAL-PTR-NON-SF?
#
# METHOD: OWN minimal PE parser written for this proof (the package's historical
# sf30_core.py / census.py are NOT imported and NOT modified - only their general
# conventions are followed: DOS/COFF/section walk, VA<->offset via the section
# table, detail-mode capstone decode), capstone 5.0.7 from the pinned temp path,
# full .text linear sweep with the bad-byte restart rule: the sweep starts at the
# FIRST byte of .text; each cursor position decodes exactly one instruction and the
# cursor advances by its size; when capstone yields NO instruction at the cursor
# (bad byte), a restart is recorded and the cursor advances ONE byte. Decoded-insn
# and restart totals are recorded FACTS, not gates (they may differ +/-1 from any
# prior run by restart convention); the CENSUS ITEMS are the gates.
#
# ALL PINS ARE FAIL-CLOSED EXPECTATIONS, re-derived from the physical bytes below.
# They are never used as decode inputs. A predicate mismatch is RECORDED as a
# MISMATCH line in the raw artifact and in the verdict block; the pre-registered
# contract branches (relabel / HARD STOP / return to PE-MASTER) are decided from
# the raw artifact by the amendment executor - never by silent adaptation here.
#
# STATIC-ONLY: the client NEVER runs; no process of any game binary; byte reads
# only. Era: PCG_9_3_5. ZERO git mutations by this script (git is READ-ONLY here).
#
# Bounded decode targets (per contract, NOTHING ELSE is decoded):
#   - the full-.text census sweeps (global-slot operands, immediates, E8 calls);
#   - the 0x00405250..0x0040525B candidate window;
#   - the 0x00404C86..0x00404CA2 value chain;
#   - FUN_00409080 entry->ret;
#   - the 0x00404B60 consumer window (documented body-end rule: linear decode stops
#     at a run of >=1 int3 (CC) or nop (90) padding byte where the run end is
#     16-aligned or the run length is >=4, or right after a ret instruction that
#     lands on a 16-aligned cursor with no padding byte there - the MSVC layout
#     convention; the census over the window is PATH-INSENSITIVE, branches are
#     ignored);
#   - the FUN_005247C0 allocation window.
#
# Output: 01_RAW/F1_GLOBALPTR_PROOF_RAW.txt (UTF-8, LF, deterministic).

import hashlib
import os
import struct
import subprocess
import sys

sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone  # noqa: E402

X86 = capstone.x86

RUN_ID = "PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914"
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914")
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
RAW_OUT = os.path.join(PKG, "01_RAW", "F1_GLOBALPTR_PROOF_RAW.txt")
CSV_PATH = os.path.join(PKG, "02_ANALYSIS", "SF30_WRITER_CENSUS.csv")

# ---- pins (fail-closed expectations; never decode inputs) ----
BASE_SHA = "3644e5ac9cbf7b5445861e7f5342fb8642741346"
EXPECTED_SHA256 = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECTED_SIZE = 8015872
EXPECTED_MACHINE = 0x014C
EXPECTED_OPT_MAGIC = 0x010B
EXPECTED_IMAGE_BASE = 0x00400000

GLOBAL_SLOT = 0x00B6C3D8
STATIC_OBJ = 0x00B9FEC0
CAND_VA = 0x0040525B
LOAD_VA = 0x00405250
PUSH_VA = 0x00405256
FUN_INIT = 0x00409080
FUN_CONSUMER = 0x00404B60
FUN_ALLOC = 0x005247C0
SF_VTABLE = 0x00A7D458
SF_CTOR = 0x00509330
NEW_THUNK = 0x0095D3C4

BASELINE_UNTRACKED = {
    "?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/",
    "?? experiments/",
}
PKG_REL_PREFIX = "docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/"

EAX_FAM = {"eax", "ax", "al", "ah"}
ECX_FAM = {"ecx", "cx", "cl", "ch"}
EDX_FAM = {"edx", "dx", "dl", "dh"}
ESI_FAM = {"esi", "si"}
CALL_CLOBBERS = {"eax", "ecx", "edx"}  # cdecl/thiscall caller-saved: a call redefines eax (return) and clobbers ecx/edx


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def git(args):
    return subprocess.check_output(["git"] + args, cwd=REPO).decode().strip()


class PEX:
    """Own minimal PE parser + capstone decode wrapper. Fail-closed on identity.
    Written independently for this proof (the historical sf30_core.py is not
    imported; its conventions are followed only)."""

    def __init__(self, path):
        self.path = path
        self.sha256 = sha256_file(path)
        with open(path, "rb") as f:
            d = f.read()
        self.data = d
        self.size = len(d)
        # ---- P1 fail-closed identity asserts ----
        assert self.sha256.upper() == EXPECTED_SHA256, "SOURCE_IDENTITY_FAIL: sha256 %s" % self.sha256
        assert self.size == EXPECTED_SIZE, "SOURCE_IDENTITY_FAIL: size %d" % self.size
        assert struct.unpack_from("<H", d, 0)[0] == 0x5A4D, "bad DOS magic"
        e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
        assert struct.unpack_from("<I", d, e_lfanew)[0] == 0x00004550, "bad PE signature"
        coff = e_lfanew + 4
        self.machine, self.num_sections = struct.unpack_from("<HH", d, coff)
        opt_size = struct.unpack_from("<H", d, coff + 16)[0]
        opt = coff + 20
        self.opt_magic = struct.unpack_from("<H", d, opt)[0]
        self.image_base = struct.unpack_from("<I", d, opt + 28)[0]
        self.dll_chars = struct.unpack_from("<H", d, opt + 70)[0]
        assert self.machine == EXPECTED_MACHINE, "machine 0x%04X" % self.machine
        assert self.opt_magic == EXPECTED_OPT_MAGIC, "opt_magic 0x%04X" % self.opt_magic
        assert self.image_base == EXPECTED_IMAGE_BASE, "image_base 0x%08X" % self.image_base
        assert self.dll_chars & 0x0040 == 0, "ASLR flag set (pin says no ASLR)"
        sec_off = opt + opt_size
        self.sections = []
        for i in range(self.num_sections):
            o = sec_off + i * 40
            name = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
            vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", d, o + 8)
            self.sections.append({
                "name": name, "vsize": vsize, "vaddr": vaddr,
                "rsize": rsize, "rptr": rptr,
                "va_start": self.image_base + vaddr,
                "va_end": self.image_base + vaddr + max(vsize, rsize),
            })
        t = [s for s in self.sections if s["name"] == ".text"]
        assert len(t) == 1, "expected exactly one .text section"
        self.text = t[0]
        self.text_va = self.text["va_start"]
        self.text_end = self.text_va + self.text["rsize"]
        self.text_raw = d[self.text["rptr"]:self.text["rptr"] + self.text["rsize"]]
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        self.md.detail = True

    def va_to_off(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + s["rsize"]:
                return s["rptr"] + (rva - s["vaddr"])
        return None

    def off_to_va(self, off):
        for s in self.sections:
            if s["rptr"] <= off < s["rptr"] + s["rsize"]:
                return self.image_base + s["vaddr"] + (off - s["rptr"])
        return None

    def read_va(self, va, n):
        off = self.va_to_off(va)
        if off is None:
            return None
        return self.data[off:off + n]

    def read_va32(self, va):
        b = self.read_va(va, 4)
        if b is None or len(b) < 4:
            return None
        return struct.unpack("<I", b)[0]

    def section_of(self, va):
        rva = va - self.image_base
        for s in self.sections:
            if s["vaddr"] <= rva < s["vaddr"] + max(s["vsize"], s["rsize"]):
                return s
        return None

    def insn_at(self, va, max_bytes=16):
        n = max_bytes
        if self.text_va <= va < self.text_end:
            n = min(n, self.text_end - va)
        b = self.read_va(va, n)
        if not b:
            return None
        try:
            ins = next(self.md.disasm(b, va))
        except StopIteration:
            return None
        rec = {"va": va, "size": ins.size, "bytes": bytes(ins.bytes).hex(),
               "mnemonic": ins.mnemonic, "op_str": ins.op_str,
               "mem": [], "imm": [], "wregs": [], "rregs": []}
        for op in ins.operands:
            if op.type == X86.X86_OP_MEM:
                rec["mem"].append({
                    "base": op.mem.base, "index": op.mem.index,
                    "scale": op.mem.scale, "disp": op.mem.disp,
                    "access": op.access,
                    "base_name": ins.reg_name(op.mem.base) if op.mem.base else "",
                })
            elif op.type == X86.X86_OP_IMM:
                rec["imm"].append(op.imm)
            elif op.type == X86.X86_OP_REG:
                nm = ins.reg_name(op.reg)
                if op.access & capstone.CS_AC_WRITE:
                    rec["wregs"].append(nm)
                if op.access & capstone.CS_AC_READ:
                    rec["rregs"].append(nm)
        return rec

    def rtti_walk(self, vtable_va):
        """Contingency-only minimal MSVC RTTI walker (COL -> TypeDescriptor).
        Name at TD+0x08 (vfptr@+0, spare@+4, name@+8 - correct MSVC layout)."""
        col = self.read_va32(vtable_va - 4)
        if col is None:
            return {"error": "no COL pointer"}
        col_raw = self.read_va(col, 0x14)
        if not col_raw or len(col_raw) < 0x14:
            return {"error": "COL read fail"}
        sig, off, cd, ptd, pchd = struct.unpack("<IIIII", col_raw)
        if sig != 0:
            return {"error": "COL signature != 0"}
        td_raw = self.read_va(ptd, 0x48)
        if td_raw is None:
            return {"error": "TD read fail"}
        nf = td_raw[8:]
        z = nf.find(b"\x00")
        nb = nf[:z] if z >= 0 else nf
        return {"col_va": col, "ptd": ptd, "sig": sig,
                "name": nb.decode("ascii", "replace"), "name_hex": nb.hex()}


# ---- render / helpers ---------------------------------------------------------


def render(rec):
    return "%08X  %-24s %-6s %s" % (rec["va"], rec["bytes"], rec["mnemonic"], rec["op_str"])


def access_str(a):
    r = "R" if a & capstone.CS_AC_READ else ""
    w = "W" if a & capstone.CS_AC_WRITE else ""
    return (r + w) or "?"


def defines(rec, fam):
    """True if the instruction defines (writes) any register of the family.
    A call counts as a definition of the caller-saved set (eax/ecx/edx)."""
    if rec["mnemonic"] == "call":
        return bool(fam & CALL_CLOBBERS)
    return bool(fam & set(rec["wregs"]))


def e8_calls_to(pe, target):
    """All direct CALL rel32 (E8) byte-occurrences in .text whose target == target.
    Byte scan of the raw .text (instruction-stream membership is recorded
    separately where required)."""
    sites = []
    tr = pe.text_raw
    base = pe.text_va
    for i in range(len(tr) - 5):
        if tr[i] == 0xE8:
            rel = struct.unpack_from("<i", tr, i + 1)[0]
            if base + i + 5 + rel == target:
                sites.append(base + i)
    return sites


def dword_occurrences(pe, value):
    """Whole-FILE raw byte occurrences of the little-endian dword value."""
    pat = struct.pack("<I", value)
    d = pe.data
    out = []
    i = d.find(pat)
    while i >= 0:
        out.append(i)
        i = d.find(pat, i + 1)
    return out


def esp_delta(rec):
    """Signed esp change caused by rec (positive = esp decreases). Path-insensitive."""
    m = rec["mnemonic"]
    if m == "push":
        return 4
    if m == "pop":
        return -4
    if m == "sub" and rec["op_str"].replace(" ", "").startswith("esp,"):
        for iv in rec["imm"]:
            return iv
    if m == "add" and rec["op_str"].replace(" ", "").startswith("esp,"):
        for iv in rec["imm"]:
            return -iv
    return 0


def pad_run(pe, va, byte):
    k = 0
    while k < 16:
        b = pe.read_va(va + k, 1)
        if not b or b[0] != byte:
            break
        k += 1
    return k


def decode_to_body_end(pe, entry, max_bytes=0x3000):
    """Linear decode of the FULL window from entry to the function's end.
    Documented body-end rule: stop at a run of >=1 CC or 90 byte where
    (run_end % 16 == 0) or (run_len >= 4); or right after a ret instruction
    when the cursor is 16-aligned with no padding byte there. Restarts (bad
    bytes) are recorded and skipped by ONE byte."""
    insns = []
    restarts = []
    va = entry
    limit = entry + max_bytes
    while va < limit:
        b = pe.read_va(va, 1)
        if b and b[0] == 0xCC:
            k = pad_run(pe, va, 0xCC)
            if k >= 1 and ((va + k) % 16 == 0 or k >= 4):
                return insns, ("CC_PAD", va, k), restarts
        if b and b[0] == 0x90:
            k = pad_run(pe, va, 0x90)
            if k >= 1 and ((va + k) % 16 == 0 or k >= 4):
                return insns, ("NOP_PAD", va, k), restarts
        if insns and insns[-1]["mnemonic"] == "ret" and va % 16 == 0 and (not b or b[0] not in (0xCC, 0x90)):
            return insns, ("RET_AT_ALIGN", va, 0), restarts
        rec = pe.insn_at(va)
        if rec is None:
            restarts.append(va)
            va += 1
            continue
        insns.append(rec)
        va += rec["size"]
    return insns, ("LIMIT", va, 0), restarts


def decode_to_ret(pe, entry, max_bytes=0x2000):
    """Linear decode entry -> FIRST ret-family instruction (ret / ret imm16).
    Bad bytes are recorded (the pin expects ZERO) and skipped by ONE byte."""
    insns = []
    bad = []
    va = entry
    while va < entry + max_bytes:
        rec = pe.insn_at(va)
        if rec is None:
            bad.append(va)
            va += 1
            continue
        insns.append(rec)
        if rec["mnemonic"] == "ret":
            return insns, bad
        va += rec["size"]
    return insns, bad


# ---- P1: source + base identity (fail-closed) ----------------------------------


def check_p1(pe):
    head = git(["rev-parse", "HEAD"])
    origin = git(["rev-parse", "origin/master"])
    remote = git(["ls-remote", "origin", "master"]).split()[0]
    status = git(["status", "--short"]).splitlines()
    diff_head = git(["diff", "HEAD"])
    diff_cached = git(["diff", "--cached"])
    lines = []
    lines.append("git HEAD           = %s (pin %s) %s" % (head, BASE_SHA, "OK" if head == BASE_SHA else "DRIFT"))
    lines.append("git origin/master  = %s %s" % (origin, "OK" if origin == BASE_SHA else "DRIFT"))
    lines.append("git ls-remote      = %s %s" % (remote, "OK" if remote == BASE_SHA else "DRIFT"))
    lines.append("git status --short lines: %d" % len(status))
    for ln in status:
        ok = (ln in BASELINE_UNTRACKED or
              (ln.startswith("?? ") and ln[3:].startswith(PKG_REL_PREFIX)))
        lines.append("  %-90s %s" % (ln, "allowed" if ok else "FOREIGN-DIRTY"))
    lines.append("git diff HEAD empty      : %s" % ("YES" if diff_head == "" else "NO"))
    lines.append("git diff --cached empty  : %s" % ("YES" if diff_cached == "" else "NO"))
    lines.append("EXE sha256         = %s %s" % (pe.sha256.upper(), "OK" if pe.sha256.upper() == EXPECTED_SHA256 else "FAIL"))
    lines.append("EXE size            = %d %s" % (pe.size, "OK" if pe.size == EXPECTED_SIZE else "FAIL"))
    lines.append("machine=0x%04X opt_magic=0x%04X image_base=0x%08X dll_chars=0x%04X (no-ASLR bit clear: %s)"
                 % (pe.machine, pe.opt_magic, pe.image_base, pe.dll_chars, not (pe.dll_chars & 0x40)))
    if not (head == BASE_SHA and origin == BASE_SHA and remote == BASE_SHA):
        print("HARD STOP: BASE_DRIFT")
        sys.exit(2)
    bad_status = [ln for ln in status
                  if not (ln in BASELINE_UNTRACKED or
                          (ln.startswith("?? ") and ln[3:].startswith(PKG_REL_PREFIX)))]
    if bad_status or diff_head != "" or diff_cached != "":
        print("HARD STOP: BASE_DRIFT (foreign dirty path / tracked modification)")
        for ln in bad_status:
            print("  foreign:", ln)
        sys.exit(2)
    if not (pe.sha256.upper() == EXPECTED_SHA256 and pe.size == EXPECTED_SIZE
            and pe.machine == EXPECTED_MACHINE and pe.opt_magic == EXPECTED_OPT_MAGIC
            and pe.image_base == EXPECTED_IMAGE_BASE):
        print("HARD STOP: SOURCE_IDENTITY_FAIL")
        sys.exit(2)
    lines.append("P1 VERDICT: PASS")
    return True, lines


# ---- the full-.text sweep with inline censuses ---------------------------------


def sweep(pe):
    """Single-pass linear sweep of FULL .text (restart-at-next-byte on bad bytes).
    Inline censuses (bounded memory):
    - global_ops:  decoded insns with a mem operand base==0, index==0, disp==0x00B6C3D8;
    - global_imms: decoded insns with an imm operand == 0x00B6C3D8 (address takers);
    - sf_vt_imms:  decoded insns with an imm operand == 0x00A7D458;
    - sightings at 0x00405250 / 0x00405256 / 0x0040525B and any insn STARTING
      in the open interval (0x00405250, 0x0040525B).
    """
    stats = {"decoded": 0, "restarts": 0}
    restart_vas = []
    global_ops = []
    global_imms = []
    sf_vt_imms = []
    saw = {}
    interval = []
    va = pe.text_va
    end = pe.text_end
    while va < end:
        rec = pe.insn_at(va)
        if rec is None:
            stats["restarts"] += 1
            if len(restart_vas) < 200:
                restart_vas.append(va)
            va += 1
            continue
        stats["decoded"] += 1
        for m in rec["mem"]:
            if m["base"] == 0 and m["index"] == 0 and m["disp"] == GLOBAL_SLOT:
                global_ops.append((rec, m["access"]))
        for iv in rec["imm"]:
            if iv == GLOBAL_SLOT:
                global_imms.append(rec)
            if iv == SF_VTABLE:
                sf_vt_imms.append(rec)
        if LOAD_VA <= va <= CAND_VA:
            saw[va] = rec
            if LOAD_VA < va < CAND_VA:
                interval.append(rec)
        va += rec["size"]
    return {"stats": stats, "restart_vas": restart_vas, "global_ops": global_ops,
            "global_imms": global_imms, "sf_vt_imms": sf_vt_imms,
            "saw": saw, "interval": interval}


# ---- main measurement flow ------------------------------------------------------


def main():
    pe = PEX(EXE_PATH)  # fail-closed identity asserts (P1 phase A)
    out = []
    w = out.append
    w("# F1_GLOBALPTR_PROOF_RAW - PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914")
    w("# RUN: %s - Era: PCG_9_3_5 - STATIC-ONLY (the client NEVER ran; no process of" % RUN_ID)
    w("#   any game binary; byte-reading script only; zero git mutations).")
    w("# generator: 00_CONTROL/f1_globalptr_proof.py (own minimal PE parser; capstone")
    w("#   %s; bad-byte restart rule documented in the script header)." % capstone.__version__)
    w("# QUESTION: is census row 0x0040525B's receiver (base register edx of")
    w("#   `mov dword ptr [edx+0x30], ebx`) provably never a SceneFeederObject")
    w("#   pointer - via the global pointer slot 0x00B6C3D8 - so REJECTED_ALIAS")
    w("#   stands with the corrected justification R-GLOBAL-PTR-NON-SF?")
    w("# SWEEP: full .text 0x%08X..0x%08X (rsize 0x%X), linear, restart-at-next-byte."
      % (pe.text_va, pe.text_end, pe.text["rsize"]))
    w("")
    verdict = {}

    # ================= P1 =================
    w("== P1: source + base identity (fail-closed) ==")
    ok, lines = check_p1(pe)
    for ln in lines:
        w(ln)
    verdict["P1"] = ok
    w("")

    # ---- the sweep (recorded facts + census material) ----
    sw = sweep(pe)
    w("# sweep recorded facts (NOT gates): decoded %d instructions, %d restarts"
      % (sw["stats"]["decoded"], sw["stats"]["restarts"]))
    if sw["restart_vas"]:
        w("# restart VAs (first <=200): %s" % ", ".join("0x%08X" % v for v in sw["restart_vas"]))
    w("")

    # ================= P2 =================
    w("== P2: candidate window 0x00405250..0x0040525B (boundary-aligned decode + sweep stream) ==")
    p2 = True
    i_load = pe.insn_at(LOAD_VA)
    i_push = pe.insn_at(PUSH_VA)
    i_cand = pe.insn_at(CAND_VA)
    w("boundary-aligned decode:")
    for va, r in ((LOAD_VA, i_load), (PUSH_VA, i_push), (CAND_VA, i_cand)):
        w("  " + (render(r) if r else "0x%08X  <DECODE-FAIL>" % va))
    ok_load = (i_load is not None and i_load["va"] == LOAD_VA
               and i_load["bytes"] == "8b15d8c3b600"
               and i_load["mnemonic"] == "mov" and i_load["op_str"] == "edx, dword ptr [0xb6c3d8]"
               and i_load["wregs"] == ["edx"]
               and any(m["base"] == 0 and m["index"] == 0 and m["disp"] == GLOBAL_SLOT
                       and (m["access"] & capstone.CS_AC_READ) for m in i_load["mem"]))
    ok_push = (i_push is not None and i_push["va"] == PUSH_VA
               and i_push["bytes"] == "68304c4000"
               and i_push["mnemonic"] == "push" and i_push["imm"] == [0x404C30])
    ok_cand = (i_cand is not None and i_cand["va"] == CAND_VA
               and i_cand["bytes"] == "895a30"
               and i_cand["mnemonic"] == "mov" and i_cand["op_str"] == "dword ptr [edx + 0x30], ebx"
               and any(m["base_name"] == "edx" and m["disp"] == 0x30
                       and (m["access"] & capstone.CS_AC_WRITE) for m in i_cand["mem"]))
    w("  load  @0x00405250 == pin (8b15d8c3b600, mov edx,[0xb6c3d8], writes edx): %s" % ok_load)
    w("  push  @0x00405256 == pin (68304c4000, push 0x404c30): %s" % ok_push)
    w("  cand  @0x0040525B == pin (895a30, mov [edx+0x30],ebx, WRITE [edx+0x30]): %s" % ok_cand)
    p2 = p2 and ok_load and ok_push and ok_cand
    stream_ok = (i_load is not None and i_push is not None
                 and i_load["va"] + i_load["size"] == PUSH_VA
                 and i_push["va"] + i_push["size"] == CAND_VA)
    w("  boundary stream 0x405250+6==0x405256 and 0x405256+5==0x40525B: %s" % stream_ok)
    p2 = p2 and stream_ok
    w("sweep-stream sightings (the full sweep decoded an instruction STARTING at these VAs):")
    pins = {LOAD_VA: "8b15d8c3b600", PUSH_VA: "68304c4000", CAND_VA: "895a30"}
    for va in (LOAD_VA, PUSH_VA, CAND_VA):
        r = sw["saw"].get(va)
        same = (r is not None and r["bytes"] == pins[va])
        w("  0x%08X: %s %s" % (va, "SEEN" if r else "NOT-SEEN",
                                "(bytes match pin)" if same else "(bytes differ / absent)"))
        p2 = p2 and same
    w("instructions STARTING in the open interval (0x405250, 0x40525B) per sweep:")
    for r in sw["interval"]:
        w("  " + render(r))
    ok_interval = (len(sw["interval"]) == 1 and sw["interval"][0]["va"] == PUSH_VA
                   and not any(defines(r, EDX_FAM) for r in sw["interval"]))
    w("  count: %d (pin exactly 1 - the push; NO edx definition among them): %s"
      % (len(sw["interval"]), ok_interval))
    p2 = p2 and ok_interval
    verdict["P2"] = p2
    w("P2 VERDICT: %s" % ("PASS" if p2 else "MISMATCH"))
    w("")

    # ================= P3 =================
    w("== P3: global-writer census (full .text sweep; mem operands base==0, index==0, disp==0x00B6C3D8) ==")
    gops = sw["global_ops"]
    writes = [(r, a) for (r, a) in gops if a & capstone.CS_AC_WRITE]
    reads = [(r, a) for (r, a) in gops if a & capstone.CS_AC_READ]
    rw = [(r, a) for (r, a) in gops if (a & capstone.CS_AC_WRITE) and (a & capstone.CS_AC_READ)]
    unk = [(r, a) for (r, a) in gops if not (a & (capstone.CS_AC_READ | capstone.CS_AC_WRITE))]
    w("total occurrences: %d (pin 179)" % len(gops))
    w("WRITE (access & CS_AC_WRITE): %d (pin exactly 1) | READ: %d (pin 178) | RMW: %d (pin 0) | unknown-access: %d (pin 0)"
      % (len(writes), len(reads), len(rw), len(unk)))
    w("ALL occurrences (VA + access + bytes + rendered):")
    for (r, a) in gops:
        w("  %s %s" % (access_str(a), render(r)))
    ok_total = len(gops) == 179
    ok_write = (len(writes) == 1 and len(rw) == 0 and len(unk) == 0
                and writes[0][0]["va"] == 0x00404C9D
                and writes[0][0]["bytes"] == "a3d8c3b600"
                and writes[0][0]["mnemonic"] == "mov"
                and writes[0][0]["op_str"] == "dword ptr [0xb6c3d8], eax")
    ok_read = len(reads) == 178
    w("sole WRITE @0x00404C9D == a3d8c3b600 `mov dword ptr [0xb6c3d8], eax`: %s" % ok_write)
    w("READ count == 178: %s | total == 179: %s" % (ok_read, ok_total))
    p3 = ok_total and ok_write and ok_read
    verdict["P3"] = p3
    w("P3 VERDICT: %s" % ("PASS" if p3 else "MISMATCH"))
    w("")

    # ================= P4 =================
    w("== P4: call census (E8 rel32 -> 0x00409080; whole-file raw dword 0x00409080) ==")
    e8s = e8_calls_to(pe, FUN_INIT)
    w("E8 rel32 calls in .text targeting 0x00409080: %d (pin exactly 1, at 0x00404C8B)" % len(e8s))
    for va in e8s:
        r = pe.insn_at(va)
        w("  " + (render(r) if r else "0x%08X <no decode>" % va))
    d90 = dword_occurrences(pe, FUN_INIT)
    w("raw dword 0x00409080 occurrences in WHOLE FILE: %d (pin 0)" % len(d90))
    p4 = (len(e8s) == 1 and e8s[0] == 0x00404C8B and len(d90) == 0)
    if e8s:
        r = pe.insn_at(e8s[0])
        p4 = p4 and r is not None and r["bytes"] == "e8f0430000" and r["mnemonic"] == "call"
    verdict["P4"] = p4
    w("P4 VERDICT: %s" % ("PASS" if p4 else "MISMATCH"))
    w("")

    # ================= P5 =================
    w("== P5: the value chain 0x00404C86 -> store (all bytes re-read) ==")
    p5 = True
    chain = []
    va = 0x00404C86
    while va < 0x00404CA2:
        r = pe.insn_at(va)
        if r is None:
            chain.append(None)
            break
        chain.append(r)
        va += r["size"]
    for r in chain:
        w("  " + (render(r) if r else "<DECODE-FAIL>"))
    exp_chain = [
        (0x00404C86, "b9c0feb900", "mov", "ecx, 0xb9fec0"),
        (0x00404C8B, "e8f0430000", "call", "0x409080"),
        (0x00404C90, "68d8c3b600", "push", "0xb6c3d8"),
        (0x00404C95, "c7442414ffffffff", "mov", "dword ptr [esp + 0x14], 0xffffffff"),
        (0x00404C9D, "a3d8c3b600", "mov", "dword ptr [0xb6c3d8], eax"),
    ]
    ok_chain = len(chain) == 5
    for (eva, eb, em, eo), r in zip(exp_chain, chain):
        m = (r is not None and r["va"] == eva and r["bytes"] == eb and r["mnemonic"] == em)
        w("  0x%08X %-6s %s: %s" % (eva, em, eb, "MATCH" if m else "MISMATCH"))
        ok_chain = ok_chain and m
    p5 = p5 and ok_chain
    between = chain[2:4]
    ok_between = (len(chain) == 5 and len(between) == 2
                  and not any(defines(r, EAX_FAM) for r in between)
                  and between[0]["va"] == 0x00404C90 and between[1]["va"] == 0x00404C95)
    w("between call-end and store: exactly push@0x404C90 + mov [esp+0x14],0xffffffff@0x404C95, NEITHER defines eax: %s" % ok_between)
    p5 = p5 and ok_between
    ok_adj = (len(chain) >= 1 and chain[0] is not None
              and chain[0]["va"] + chain[0]["size"] == 0x00404C8B
              and chain[0]["imm"] == [STATIC_OBJ])
    w("mov ecx,0xb9fec0 @0x404C86 ends exactly at call@0x404C8B (imm == 0x00B9FEC0): %s" % ok_adj)
    p5 = p5 and ok_adj
    w("")
    w("-- FUN_00409080 body: linear decode entry->ret (pin: ret 4 @0x00409155, ZERO bad bytes) --")
    body, bad = decode_to_ret(pe, FUN_INIT)
    w("bad bytes in body: %d %s (pin 0)" % (len(bad), [hex(x) for x in bad] if bad else ""))
    p5 = p5 and len(bad) == 0
    w("FULL body decode (%d instructions):" % len(body))
    for r in body:
        w("  " + render(r))
    esi_defs = [r for r in body if defines(r, ESI_FAM)]
    w("esi definitions in body: %d (pin exactly 1: mov esi, ecx @0x004090A5, 8bf1)" % len(esi_defs))
    for r in esi_defs:
        w("  " + render(r))
    ok_esi = (len(esi_defs) == 1 and esi_defs[0]["va"] == 0x004090A5
              and esi_defs[0]["bytes"] == "8bf1" and esi_defs[0]["mnemonic"] == "mov"
              and esi_defs[0]["op_str"] == "esi, ecx")
    w("  esi-def pin: %s" % ok_esi)
    p5 = p5 and ok_esi
    eax_defs = [r for r in body if defines(r, EAX_FAM)]
    w("eax definitions in body (calls count as eax defs): %d" % len(eax_defs))
    for r in eax_defs:
        w("  " + render(r))
    last_eax = eax_defs[-1] if eax_defs else None
    ok_eax = (last_eax is not None and last_eax["va"] == 0x00409142
              and last_eax["bytes"] == "8bc6" and last_eax["mnemonic"] == "mov"
              and last_eax["op_str"] == "eax, esi")
    w("last eax def == mov eax, esi @0x00409142 (8bc6): %s" % ok_eax)
    p5 = p5 and ok_eax
    tail = [r for r in body if r["va"] > 0x00409142]
    w("instructions after 0x00409142 (pin: ONLY epilogue + ret 4 @0x00409155):")
    for r in tail:
        w("  " + render(r))
    ok_tail = (not any(defines(r, EAX_FAM) or defines(r, ESI_FAM) for r in tail)) and len(tail) > 0
    if tail:
        last = tail[-1]
        ok_tail = (ok_tail and last["va"] == 0x00409155 and last["bytes"] == "c20400"
                   and last["mnemonic"] == "ret" and last["op_str"] == "0x4"
                   and all(r["mnemonic"] in ("pop", "leave", "mov", "ret") for r in tail))
    w("tail: no eax/esi def, ends ret 0x4 @0x00409155 (c20400): %s" % ok_tail)
    p5 = p5 and ok_tail
    pre = [r for r in body if r["va"] < 0x004090A5]
    ok_pre = not any(defines(r, ECX_FAM) for r in pre)
    w("no ecx definition (incl. calls) between entry and 0x004090A5: %s (%d insns checked)" % (ok_pre, len(pre)))
    p5 = p5 and ok_pre
    esi_reg = X86.X86_REG_ESI
    vt_writes = []
    for r in body:
        for m in r["mem"]:
            if m["base"] == esi_reg and m["disp"] == 0 and (m["access"] & capstone.CS_AC_WRITE):
                vt_writes.append(r)
    w("writes to [esi] / [esi+0] in body: %d (pin ZERO - no vtable store; non-polymorphic)" % len(vt_writes))
    hard_stop_sf = False
    for r in vt_writes:
        w("  FOUND: " + render(r))
        for iv in r["imm"]:
            sec = pe.section_of(iv)
            if sec and sec["name"] in (".rdata", ".data"):
                w("    imm32 0x%08X points into %s - vtable-store candidate; calibrated RTTI walk:" % (iv, sec["name"]))
                cal = pe.rtti_walk(SF_VTABLE)
                w("    calibration (0x00A7D458): %s" % cal.get("name"))
                if cal.get("name") == ".?AVSceneFeederObject@@":
                    lk = pe.rtti_walk(iv)
                    w("    candidate walk: %s" % lk.get("name"))
                    if lk.get("name") == ".?AVSceneFeederObject@@":
                        hard_stop_sf = True
                        w("    *** HARD STOP CONDITION: SceneFeederObject vtable store in FUN_00409080 body ***")
    ok_vt = len(vt_writes) == 0 and not hard_stop_sf
    p5 = p5 and ok_vt
    verdict["P5"] = p5
    if hard_stop_sf:
        w("P5 VERDICT: HARD_STOP_SF_CLASS")
    else:
        w("P5 VERDICT: %s" % ("PASS" if p5 else "MISMATCH"))
    w("=> chain: FUN_00409080 return == esi == entry ecx == 0x00B9FEC0; store @0x00404C9D")
    w("   stores eax == 0x00B9FEC0 into [0x00B6C3D8].")
    w("")

    # ================= P6 =================
    w("== P6: static object + global at rest (file-backed reads; own VA->offset) ==")
    p6 = True
    sec_data = pe.section_of(STATIC_OBJ)
    sec_glob = pe.section_of(GLOBAL_SLOT)
    for s in pe.sections:
        w("  section %-8s va 0x%08X..0x%08X vsize 0x%X rsize 0x%X (file-backed end 0x%08X)"
          % (s["name"], s["va_start"], s["va_end"], s["vsize"], s["rsize"],
             s["va_start"] + s["rsize"]))
    ok_sec = (sec_data is not None and sec_data["name"] == ".data"
              and sec_data["va_start"] == 0x00B6C000
              and sec_glob is not None and sec_glob["name"] == ".data")
    w("0x00B9FEC0 in section: %s; 0x00B6C3D8 in section: %s; .data va_start == 0x00B6C000: %s"
      % (sec_data["name"] if sec_data else "NONE",
         sec_glob["name"] if sec_glob else "NONE", ok_sec))
    p6 = p6 and ok_sec
    w("at-rest dwords 0x00B9FEC0..0x00B9FF20 (file-backed; 25 dwords incl. both ends):")
    all_zero = True
    va = STATIC_OBJ
    while va <= 0x00B9FF20:
        v = pe.read_va32(va)
        w("  [0x%08X] = 0x%08X" % (va, v if v is not None else 0xDEADBEEF))
        all_zero = all_zero and v == 0
        va += 4
    w("all zero: %s (pin ALL ZERO)" % all_zero)
    p6 = p6 and all_zero
    gv = pe.read_va32(GLOBAL_SLOT)
    w("[0x00B6C3D8] at rest = 0x%08X (pin 0x00000000)" % gv)
    p6 = p6 and gv == 0
    verdict["P6"] = p6
    w("P6 VERDICT: %s" % ("PASS" if p6 else "MISMATCH"))
    w("")

    # ================= P7 =================
    w("== P7: address-taker channel closure ==")
    p7 = True
    # (a) IMM-operand census of 0x00B6C3D8 over the full sweep
    imms = sw["global_imms"]
    w("IMM-operand census of 0x00B6C3D8 in .text (sweep stream): %d (pin EXACTLY 1)" % len(imms))
    for r in imms:
        w("  " + render(r))
    ok_imm = (len(imms) == 1 and imms[0]["va"] == 0x00404C90
              and imms[0]["bytes"] == "68d8c3b600"
              and imms[0]["mnemonic"] == "push" and imms[0]["imm"] == [GLOBAL_SLOT])
    w("the sole address-taker == push 0xb6c3d8 @0x00404C90 (68d8c3b600): %s" % ok_imm)
    p7 = p7 and ok_imm
    w("")
    # (b) caller chain: from the push site to the direct call of FUN_00404B60
    e8c = e8_calls_to(pe, FUN_CONSUMER)
    w("E8 rel32 calls in .text targeting 0x00404B60 (recorded facts): %d" % len(e8c))
    for va in e8c:
        w("  call site 0x%08X" % va)
    call_site = None
    for va in e8c:
        if va > 0x00404C90:
            call_site = va
            break
    if call_site is None:
        w("NO E8 call to 0x00404B60 found after 0x00404C90 - P7 MISMATCH (consumer link open)")
        verdict["P7"] = False
        w("P7 VERDICT: MISMATCH")
        w("")
    else:
        w("caller chain decode 0x00404C95..0x%08X (linear, path-insensitive esp simulation):" % call_site)
        chain2 = []
        va = 0x00404C95
        while va < call_site:
            r = pe.insn_at(va)
            if r is None:
                chain2.append(None)
                va += 1
                continue
            chain2.append(r)
            va += r["size"]
        d = 0
        for r in chain2:
            if r is None:
                w("  <DECODE-FAIL>")
                continue
            w("  %s  (esp delta %+d)" % (render(r), esp_delta(r)))
            d += esp_delta(r)
        rcall = pe.insn_at(call_site)
        w("  " + render(rcall) + "  (call)")
        w("caller-side stack delta D (bytes pushed between the &global push and this call): %+d" % d)
        # (c) callee window: FUN_00404B60, full body, documented body-end rule
        w("")
        w("-- FUN_00404B60 window: linear decode to the function's end (path-insensitive) --")
        win, stop, restarts = decode_to_body_end(pe, FUN_CONSUMER)
        w("body-end stop: %s at 0x%08X (run %d); bad-byte restarts in window: %d %s"
          % (stop[0], stop[1], stop[2], len(restarts), [hex(x) for x in restarts] if restarts else ""))
        w("FULL window decode (%d instructions):" % len(win))
        for r in win:
            w("  " + render(r))
        esp_reg = X86.X86_REG_ESP
        # find the first [esp+0x20] access; compute the prologue esp delta P
        first_arg_idx = None
        P = 0
        for idx, r in enumerate(win):
            hit = any(m["base"] == esp_reg and m["disp"] == 0x20 for m in r["mem"])
            if hit:
                first_arg_idx = idx
                break
            P += esp_delta(r)
        w("first [esp+0x20] access at window index %s; callee esp delta P before it: %+d"
          % (first_arg_idx if first_arg_idx is not None else "NONE", P))
        ok_arith = False
        if first_arg_idx is not None:
            total = 4 + d + P
            w("stack arithmetic: 4 (retaddr) %+d (caller D) %+d (callee P) == 0x%02X (pin 0x20): %s"
              % (d, P, total, total == 0x20))
            ok_arith = total == 0x20
        p7 = p7 and ok_arith
        # arg-register census
        arg_regs = {}
        if first_arg_idx is not None:
            for r in win:
                for m in r["mem"]:
                    if m["base"] == esp_reg and m["disp"] == 0x20 and (m["access"] & capstone.CS_AC_READ):
                        for rn in r["wregs"]:
                            arg_regs[rn] = r
        w("arg-slot loads (reg := [esp+0x20]): %s" % (list(arg_regs.items()) if arg_regs else "NONE"))
        # first-level copies of arg registers (mov R2, R1)
        arg_names = set(arg_regs.keys())
        copies = []
        for r in win:
            if r["mnemonic"] == "mov" and not r["mem"] and len(r["wregs"]) == 1 and len(r["rregs"]) == 1:
                if r["rregs"][0] in arg_names and r["wregs"][0] not in arg_names:
                    copies.append(r)
        for r in copies:
            arg_names.add(r["wregs"][0])
            w("first-level copy: " + render(r))
        arg_ids = set()
        for nm in arg_names:
            rid = getattr(X86, "X86_REG_" + nm.upper(), 0)
            arg_ids.add(rid)
        # (a) WRITE mem operands [R+0]
        viol_a = []
        uses = []
        for r in win:
            for m in r["mem"]:
                if m["base"] in arg_ids:
                    uses.append((r, m))
                    if m["disp"] == 0 and (m["access"] & capstone.CS_AC_WRITE):
                        viol_a.append((r, m))
        w("census (a): WRITE mem-operands [argreg + 0]: %d (pin ZERO)" % len(viol_a))
        for (r, m) in viol_a:
            w("  VIOLATION: " + render(r))
        p7 = p7 and len(viol_a) == 0
        # (b) stores of an arg register to memory (incl. push argreg)
        viol_b = []
        for r in win:
            if r["mnemonic"] == "push" and r["rregs"] and r["rregs"][0] in arg_names:
                viol_b.append(r)
                continue
            has_wmem = any(m["access"] & capstone.CS_AC_WRITE for m in r["mem"])
            if has_wmem and any(x in arg_names for x in r["rregs"]):
                viol_b.append(r)
        w("census (b): stores of an arg register to memory (incl. push argreg): %d (pin ZERO)" % len(viol_b))
        for r in viol_b:
            w("  VIOLATION: " + render(r))
        p7 = p7 and len(viol_b) == 0
        # (c) record ALL observed uses of the arg registers as mem bases
        w("census (c): ALL observed uses of arg registers as mem-op bases (disp/access):")
        for (r, m) in uses:
            w("  %s disp=0x%X access=%s" % (render(r), m["disp"], access_str(m["access"])))
        has_r8 = any(m["disp"] == 8 and (m["access"] & capstone.CS_AC_READ) for (r, m) in uses)
        has_wc = any(m["disp"] == 0xC and (m["access"] & capstone.CS_AC_WRITE) for (r, m) in uses)
        w("expected observations present - read [arg+8]: %s, write [arg+0xc]: %s" % (has_r8, has_wc))
        p7 = p7 and has_r8 and has_wc
        verdict["P7"] = p7
        w("P7 VERDICT: %s" % ("PASS" if p7 else "MISMATCH (ALIAS_CHANNEL_OPEN if (a)/(b) nonzero)"))
        w("")

    # ================= P8 =================
    w("== P8: SF-always-heap premise re-assertion ==")
    p8 = True
    hits = dword_occurrences(pe, SF_VTABLE)
    w("whole-file raw dword 0x00A7D458 occurrences: %d (pin exactly 2)" % len(hits))
    ok_vt = len(hits) == 2
    for off in hits:
        va = pe.off_to_va(off)
        w("  file offset 0x%X -> VA %s" % (off, ("0x%08X" % va) if va else "outside sections"))
        if va is not None:
            ok_here = va in (0x00509369, 0x0050A26B)
            ok_vt = ok_vt and ok_here
            # true-start containing store (end-anchored: insn ends at hit+4)
            ins = None
            for back in range(1, 25):
                cand = pe.insn_at(va - back)
                if cand and cand["va"] <= va and cand["va"] + cand["size"] == va + 4:
                    ins = cand
                    break
            w("    imm-operand position pin (0x00509369 / 0x0050A26B): %s" % ok_here)
            w("    containing store (true start, end-anchored at imm end): "
              + (render(ins) if ins else "<none>"))
            if ins is not None:
                ok_vt = ok_vt and ins["imm"] == [SF_VTABLE] and any(
                    m["access"] & capstone.CS_AC_WRITE for m in ins["mem"])
                ok_vt = ok_vt and ins["va"] in (0x00509366, 0x0050A269)
    w("sweep census: insns with imm 0x00A7D458: %d (pin exactly 2, both WRITE stores)"
      % len(sw["sf_vt_imms"]))
    for r in sw["sf_vt_imms"]:
        w("  " + render(r))
    ok_vt = ok_vt and len(sw["sf_vt_imms"]) == 2
    p8 = p8 and ok_vt
    dctor = dword_occurrences(pe, SF_CTOR)
    w("whole-file raw dword 0x00509330 occurrences: %d (pin 0)" % len(dctor))
    p8 = p8 and len(dctor) == 0
    callers = sorted(e8_calls_to(pe, SF_CTOR))
    w("E8 rel32 calls in .text targeting 0x00509330 (SF ctor): %s (pin [0x0047D043, 0x0052480F])"
      % ["0x%08X" % v for v in callers])
    p8 = p8 and callers == [0x0047D043, 0x0052480F]
    w("")
    w("-- FUN_005247C0 allocation window (SF-block allocation: push 0x98 + new-thunk call) --")
    win2, stop2, restarts2 = decode_to_body_end(pe, FUN_ALLOC)
    w("body-end stop: %s at 0x%08X (run %d); bad-byte restarts: %d"
      % (stop2[0], stop2[1], stop2[2], len(restarts2)))
    w("window: 0x%08X..0x%08X, %d instructions decoded" % (FUN_ALLOC, stop2[1], len(win2)))
    win2_end = stop2[1]
    push98 = [r for r in win2 if r["mnemonic"] == "push" and r["imm"] == [0x98]]
    news = [r for r in win2 if r["mnemonic"] == "call" and r["op_str"] == "0x95d3c4"]
    ctors = [r for r in win2 if r["mnemonic"] == "call" and r["op_str"] == "0x509330"]
    w("push 0x98 sites in window: %d (pin exactly 1)" % len(push98))
    for r in push98:
        w("  " + render(r))
    w("operator-new thunk (call 0x95d3c4) sites in window: %d (pin exactly 1; 0x95D3C4 = the"
      % len(news) + " MSVCR80.dll operator-new thunk per the accepted run's IAT walk - not re-decoded here)")
    for r in news:
        w("  " + render(r))
    w("SF ctor call sites in window: %d (pin exactly 1, at 0x0052480F)" % len(ctors))
    for r in ctors:
        w("  " + render(r))
    ok_alloc = (len(push98) == 1 and len(news) == 1 and len(ctors) == 1
                and ctors[0]["va"] == 0x0052480F
                and push98[0]["va"] < news[0]["va"] < ctors[0]["va"])
    w("allocation pattern ok (push 0x98 BEFORE new-call BEFORE ctor call): %s" % ok_alloc)
    p8 = p8 and ok_alloc
    # bounded context around the allocation
    if news:
        nva = news[0]["va"]
        w("bounded context decode around the allocation (0x%08X..):" % (nva - 0x20))
        va = nva - 0x20
        while va < nva + 0x20:
            r = pe.insn_at(va)
            if r is None:
                va += 1
                continue
            w("  " + render(r))
            va += r["size"]
    verdict["P8"] = p8
    w("P8 VERDICT: %s" % ("PASS" if p8 else "MISMATCH"))
    w("")

    # ================= P9 =================
    w("== P9: counts recomputed from the UNCHANGED 02_ANALYSIS/SF30_WRITER_CENSUS.csv ==")
    import csv as _csv
    rows = list(_csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    from collections import Counter as _Counter
    cc = _Counter(r["classification"] for r in rows)
    counts = {"PROVEN_SF30_WRITER": cc.get("PROVEN_SF30_WRITER", 0),
              "POSSIBLE_ALIAS": cc.get("POSSIBLE_ALIAS", 0),
              "REJECTED_ALIAS": cc.get("REJECTED_ALIAS", 0),
              "UNRESOLVED": cc.get("UNRESOLVED", 0)}
    w("CSV data rows: %d (pin 3643)" % len(rows))
    w("counts: %s (pin 2/618/3023/0; UNRESOLVED via .get(k,0) - the AMEND T-2 lesson)" % counts)
    row_40525b = [r for r in rows if r["writer_va"] == "0x0040525B"]
    ok_row = (len(row_40525b) == 1 and row_40525b[0]["classification"] == "REJECTED_ALIAS")
    w("row 0x0040525B present with classification REJECTED_ALIAS: %s" % ok_row)
    if row_40525b:
        w("  row: %s" % row_40525b[0])
    p9 = (len(rows) == 3643 and counts["PROVEN_SF30_WRITER"] == 2
          and counts["POSSIBLE_ALIAS"] == 618 and counts["REJECTED_ALIAS"] == 3023
          and counts["UNRESOLVED"] == 0 and ok_row)
    verdict["P9"] = p9
    w("P9 VERDICT: %s" % ("PASS" if p9 else "MISMATCH"))
    w("")

    # ================= verdict =================
    w("== F1-P GATE VERDICT (P1..P9) ==")
    for k in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"):
        w("%s: %s" % (k, "PASS" if verdict.get(k) else "FAIL/MISMATCH"))
    overall = all(verdict.get(k) for k in ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"))
    w("F1-P: %s" % ("PASS - branch (a) applies (R-GLOBAL-PTR-NON-SF grounded; REJECTED_ALIAS stands)"
                    if overall else
                    "FAIL - branch decision per the pre-registered contract branches"))
    w("")
    w("# interpreter: %s" % sys.executable)
    w("# capstone: %s" % capstone.__version__)
    w("# END OF RAW")

    with open(RAW_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("F1-PROOF OK / verdicts:", {k: bool(v) for k, v in verdict.items()},
          "/ OVERALL:", overall)
    print("raw artifact:", RAW_OUT)
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
