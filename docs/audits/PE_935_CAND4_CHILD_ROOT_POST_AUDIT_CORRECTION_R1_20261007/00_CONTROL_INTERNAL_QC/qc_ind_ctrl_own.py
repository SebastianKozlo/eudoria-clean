"""qc_ind_ctrl_own.py — INDEPENDENT internal QC engine, part 2 (controls), for
PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007.

Author: pe-master-auditor (fresh-context internal QC under PE-MASTER dispatch).
RECORDS/QC-MACHINERY ONLY: zero EXE access; every buffer is an in-memory byte
constant re-derived from the PUBLISHED records (SOURCE 01_RAW/
JOIN_WINDOW_50A3B7_REPIN.txt, BASE-blob-verified). All mutants are SYNTHETIC /
IN-MEMORY ONLY; nothing is written to any file except THIS QC's own results
under 00_CONTROL_INTERNAL_QC/.

What this part does (C-checks):
  C1  the CTRL_4 clean window re-derived MY OWN way from the published
      per-instruction record: first VA 0x0050A3B7, 22 instructions, contiguous
      decode boundaries, total 0x42; byte-identical to the executor's declared
      fixture (extracted from the executor's script as TEXT — no execution for
      the comparison source)
  C2  MY OWN independent x86-32 decoder + MY OWN exact-endpoint checker (P1..P4),
      structurally different from the executor's implementation
  C3  the mandatory 4-case matrix on MY checker: REAL CLEAN = PASS; historical
      EDI-clobber = FAIL; 57->56 = FAIL; 57->90 = FAIL
  C4  the EXECUTOR's rebuilt checker (03_SCRIPTS/ctrl4_exact_endpoint.py, imported
      read-only) executed BY THIS QC on the same four buffers — must equal both
      MY results and the persisted CONTROL_RESULTS.json and the Desktop
      own_exact_endpoint_predicate
  C5  the executor's OLD-logic reproduction: clean PASS, clobber FAIL, FALSE PASS
      on ESI/NOP (the two Desktop false PASS — the defect being superseded)
  C6  MY adversarial mutants through BOTH checkers (all must FAIL the new one):
      A1a head displaced (nop at 0x0050A3B7, chain otherwise intact)         -> P1
      A1b head alternative byte form 89 C7 (mov edi,eax, non-canonical form)  -> P1
      A2  push edi real at 0x0050A3F4/0x0050A3F5 but NOT at the exact site    -> P3
      A3a join call shifted to 0x0050A3F8 (push edi at F7, call edx at F8)     -> P3+P4
      A3b call truncated at the window end (FF at F8 without modrm)            -> fail-closed
      A4a pop edi injected at 0x0050A3E3 (EDI write in range)                 -> P2
      A4b pop edi injected at 0x0050A3D6                                      -> P2
      A5  push edi in the 2-byte FF F7 form at 0x0050A3F6                     -> P3 (exact byte form)
      A6  final push removed, earlier push edi @0x0050A3D7 survives           -> P3
        (A6 == the mandatory NOP mutant; the OLD logic FALSE-PASSES it — documented)
  C7  CTRL_3: MY OWN checker + the executor's rebuilt checker on clean/mutated
      fixtures + MY adversarial fixtures ([ecx+0x69] FAIL; [esi+0x68] FAIL;
      disp32 form of [ecx+0x68] PASS — semantically identical must NOT false-fail)
  C8  window arithmetic: all four call rel32 targets + both rel8 branch targets
      recompute on MY decoder
"""
import hashlib
import importlib.util
import json
import os
import re
import sys

REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
PKG = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007")
QC_DIR = os.path.join(PKG, "00_CONTROL_INTERNAL_QC")
SRC_PKG = os.path.join(REPO, "docs", "audits", "PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007")
DESKTOP = r"C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_DESKTOP_POST_AUDIT_790E837_20261007"

results = {}


def rec(cid, ok, detail):
    results[cid] = {"ok": bool(ok), "detail": detail}
    print(("PASS  " if ok else "FAIL  ") + cid + ": " + detail)


WIN_VA = 0x0050A3B7
HEAD_VA = 0x0050A3B7
FINAL_PUSH_VA = 0x0050A3F6
JOIN_CALL_VA = 0x0050A3F7
CLOBBER_VA = 0x0050A3DD

# ---------------------------------------------------------------- C1: window re-derivation (MY parser)
win_txt = open(os.path.join(SRC_PKG, "01_RAW", "JOIN_WINDOW_50A3B7_REPIN.txt"), encoding="utf-8").read()
pat = re.compile(r"^  0x([0-9a-f]{8})  ((?:[0-9A-F]{2} )*[0-9A-F]{2})", re.M)
pieces = [(int(va, 16), bytes.fromhex(bx)) for va, bx in pat.findall(win_txt)]
pieces.sort()
MY_WINDOW = b"".join(p[1] for p in pieces)
contig = all(pieces[i][0] + len(pieces[i][1]) == pieces[i + 1][0] for i in range(len(pieces) - 1))
first_ok = pieces and pieces[0][0] == WIN_VA
# executor fixture extracted as TEXT (no execution for this comparison)
exec_src = open(os.path.join(PKG, "03_SCRIPTS", "ctrl4_exact_endpoint.py"), encoding="utf-8").read()
m = re.search(r"CLEAN_WINDOW_HEX = \((.*?)\n\)", exec_src, re.S)
quoted = re.findall(r'"([^"]*)"', m.group(1))       # the per-line hex strings (comments dropped)
EXEC_WINDOW = bytes.fromhex("".join(quoted))
rec("C1_window_rederivation", first_ok and contig and len(MY_WINDOW) == 0x42
    and MY_WINDOW == EXEC_WINDOW,
    f"clean window re-derived MY OWN way from the published record: first VA 0x0050A3B7, "
    f"{len(pieces)} instructions, contiguous boundaries, total 0x{len(MY_WINDOW):X}; byte-identical to the "
    f"executor's declared fixture (extracted from its script as text)")

CLEAN = MY_WINDOW


def clobber_mutant():
    b = bytearray(CLEAN)
    off = CLOBBER_VA - WIN_VA
    assert b[off:off + 6] == bytes.fromhex("8B 8E 8C 00 00 00")
    b[off:off + 6] = bytes.fromhex("8B 3D D0 D8 B9 00")
    return bytes(b)


def byte_mutant(va, old, new):
    b = bytearray(CLEAN)
    off = va - WIN_VA
    assert b[off] == old, f"{va:#x}: expected {old:#x}, got {b[off]:#x}"
    b[off] = new
    return bytes(b)


def tail_mutant(repl):
    """Replace the window tail from 0x0050A3F4 with repl (keeps total length flexible)."""
    off = 0x0050A3F4 - WIN_VA
    return bytes(CLEAN[:off]) + repl


M_CASES = [
    ("real_clean", CLEAN, "PASS"),
    ("historical_edi_clobber", clobber_mutant(), "FAIL"),
    ("final_push_esi", byte_mutant(FINAL_PUSH_VA, 0x57, 0x56), "FAIL"),
    ("final_push_nop", byte_mutant(FINAL_PUSH_VA, 0x57, 0x90), "FAIL"),
]

# ---------------------------------------------------------------- C2: MY OWN decoder + checker
REG = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
GRP1 = ["add", "or", "adc", "sbb", "and", "sub", "xor", "cmp"]


class Insn:
    __slots__ = ("va", "size", "mn", "ops", "writes_edi", "raw")

    def __init__(self, va, size, mn, ops, writes_edi, raw):
        self.va, self.size, self.mn, self.ops = va, size, mn, ops
        self.writes_edi = writes_edi
        self.raw = raw


def modrm(b, i):
    m = b[i]
    return (m >> 6) & 3, (m >> 3) & 7, m & 7


def modrm_len(mod, rm):
    """length of the modrm displacement field (mod=10 -> disp32; mod=00 rm=101 -> disp32 moffs)."""
    if mod == 0b01:
        return 1
    if mod == 0b10 or (mod == 0b00 and rm == 0b101):
        return 4
    return 0


def my_decode(buf, base_va):
    """Table-driven linear decode; raises on any uncovered form (fail-closed)."""
    out = {}
    i, va = 0, base_va
    while i < len(buf):
        start, op = i, buf[i]
        wedi = False
        if op in (0x8B, 0x89, 0x8D):                       # mov r,r/m | mov r/m,r | lea
            mod, reg, rm = modrm(buf, i + 1)
            dlen = modrm_len(mod, rm)
            disp = int.from_bytes(buf[i + 2:i + 2 + dlen], "little") if dlen else 0
            if mod == 0b11:
                ops = f"{REG[reg]}, {REG[rm]}" if op != 0x89 else f"{REG[rm]}, {REG[reg]}"
                wedi = (op == 0x8B or op == 0x8D) and reg == 7 or (op == 0x89 and rm == 7)
            else:
                base = f"0x{disp:08x}" if (mod == 0b00 and rm == 0b101) else (
                    f"{REG[rm]} + 0x{disp:x}" if disp else REG[rm])
                ops = f"{REG[reg]}, dword ptr [{base}]" if op != 0x89 else f"dword ptr [{base}], {REG[reg]}"
                wedi = (op == 0x8B or op == 0x8D) and reg == 7
            size = 2 + dlen
            mn = {0x8B: "mov", 0x89: "mov", 0x8D: "lea"}[op]
        elif op == 0x84:                                   # test r/m8, r8
            mod, reg, rm = modrm(buf, i + 1)
            if mod != 0b11:
                raise ValueError(f"uncovered test mod={mod:02b}")
            size, mn, ops = 2, "test", f"{['al','cl','dl','bl','ah','ch','dh','bh'][rm]}, " \
                f"{['al','cl','dl','bl','ah','ch','dh','bh'][reg]}"
        elif op in (0x74, 0xEB):                            # je/jmp rel8
            rel = buf[i + 1] - 0x100 if buf[i + 1] >= 0x80 else buf[i + 1]
            size, mn, ops = 2, ("je" if op == 0x74 else "jmp"), f"0x{va + 2 + rel:08x}"
        elif op == 0x83:                                   # grp1 r/m32, imm8
            mod, reg, rm = modrm(buf, i + 1)
            if mod not in (0b01, 0b11):
                raise ValueError(f"uncovered 0x83 mod={mod:02b}")
            dlen = modrm_len(mod, rm)
            imm = buf[i + 2 + dlen]
            if mod == 0b11:
                ops, wedi = f"{REG[rm]}, {imm:#x}", (rm == 7)
            else:
                ops = f"dword ptr [{REG[rm]} + 0x{buf[i + 2]:x}], {imm & 0xFFFFFFFF:#x}"
            size, mn = 3 + dlen, GRP1[reg]
        elif op == 0x6A:                                   # push imm8
            size, mn, ops = 2, "push", f"{buf[i + 1]}"
        elif 0x50 <= op <= 0x57:                           # push r32
            size, mn, ops = 1, "push", REG[op - 0x50]
        elif 0x58 <= op <= 0x5F:                           # pop r32 (writes reg)
            size, mn, ops = 1, "pop", REG[op - 0x58]
            wedi = (op == 0x5F)
        elif op == 0xBF:                                    # mov edi, imm32
            size, mn, ops = 5, "mov", f"edi, 0x{int.from_bytes(buf[i+1:i+5],'little'):08x}"
            wedi = True
        elif op == 0xE8:                                   # call rel32
            rel = int.from_bytes(buf[i + 1:i + 5], "little", signed=True)
            size, mn, ops = 5, "call", f"0x{va + 5 + rel:08x}"
        elif op == 0xFF:                                    # grp5; /2 = call r/m32 (reg form only here)
            mod, reg, rm = modrm(buf, i + 1)
            if reg == 0b011 and mod == 0b11:                # /3 = push r/m32 (FF F7 = push edi)
                size, mn, ops, wedi = 2, "push", REG[rm], False
            elif reg == 0b010 and mod == 0b11:
                size, mn, ops = 2, "call", REG[rm]
            else:
                raise ValueError(f"uncovered FF /{reg} mod={mod:02b}")
        elif op == 0x90:
            size, mn, ops = 1, "nop", ""
        elif op == 0xF8:                                    # clc
            size, mn, ops = 1, "clc", ""
        else:
            raise ValueError(f"uncovered opcode {op:02X} @0x{va:08X}")
        out[va] = Insn(va, size, mn, ops, wedi, bytes(buf[start:start + size]))
        i += size
        va += size
    return out


def my_ctrl4(buf, base_va=WIN_VA):
    """MY OWN exact-endpoint checker: P1..P4 simultaneous, exact addresses, exact byte forms."""
    try:
        ins = my_decode(buf, base_va)
    except (ValueError, IndexError) as e:
        return False, f"window not boundary-decodable ({e}) — FAIL closed"
    h = ins.get(HEAD_VA)
    if not h or h.raw != b"\x8B\xF8" or h.mn != "mov" or h.ops != "edi, eax":
        got = f"{h.mn} {h.ops} [{h.raw.hex(' ').upper()}]" if h else "none"
        return False, f"P1 FAIL: exact head mov edi,eax @0x0050A3B7 (8B F8) not found (got {got})"
    for va in sorted(ins):
        if HEAD_VA < va < FINAL_PUSH_VA and ins[va].writes_edi:
            return False, f"P2 FAIL: caller-side EDI write @0x{va:08X} ({ins[va].mn} {ins[va].ops})"
    f = ins.get(FINAL_PUSH_VA)
    if not f or f.raw != b"\x57" or f.mn != "push" or f.ops != "edi":
        got = f"{f.mn} {f.ops} [{f.raw.hex(' ').upper()}]" if f else "none"
        return False, f"P3 FAIL: exact final child argument push edi @0x0050A3F6 (57) not found (got {got})"
    j = ins.get(JOIN_CALL_VA)
    if not j or j.raw != b"\xFF\xD2" or j.mn != "call" or j.ops != "edx":
        got = f"{j.mn} {j.ops} [{j.raw.hex(' ').upper()}]" if j else "none"
        return False, f"P4 FAIL: exact join call endpoint call edx @0x0050A3F7 (FF D2) not found (got {got})"
    return True, "PASS: P1+P2+P3+P4 all hold at exact addresses on verified decode boundaries"


# ---------------------------------------------------------------- C3: mandatory matrix on MY checker
mine = {}
for name, buf, expected in M_CASES:
    ok, det = my_ctrl4(buf)
    mine[name] = (ok, det)
    print(f"    [mine] {name}: {'PASS' if ok else 'FAIL'} — {det}")
ok3 = (mine["real_clean"][0] and not mine["historical_edi_clobber"][0]
       and not mine["final_push_esi"][0] and not mine["final_push_nop"][0])
rec("C3_my_checker_mandatory_matrix", ok3,
    "MY OWN exact-endpoint checker: REAL CLEAN = PASS; historical EDI-clobber = FAIL (P2); "
    "57->56 = FAIL; 57->90 = FAIL (P3) — the mandatory contract §3 matrix")

# ---------------------------------------------------------------- C4: executor's checker re-executed
spec = importlib.util.spec_from_file_location(
    "exec_ctrl4", os.path.join(PKG, "03_SCRIPTS", "ctrl4_exact_endpoint.py"))
X4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(X4)                                # inert at import (full-read verified)
exe_res = {name: X4.ctrl4_exact_endpoint(buf) for name, buf, _ in M_CASES}
persisted = json.load(open(os.path.join(PKG, "CONTROL_RESULTS.json"), encoding="utf-8"))
desk = json.load(open(os.path.join(DESKTOP, "CONTROL_COUNTERCHECKS.json"), encoding="utf-8"))["CTRL_4"]
ok4 = (exe_res["real_clean"][0] and not exe_res["historical_edi_clobber"][0]
       and not exe_res["final_push_esi"][0] and not exe_res["final_push_nop"][0]
       and all(mine[n][0] == exe_res[n][0] for n in mine)
       and persisted["CTRL_4_EXACT_ENDPOINT_REBUILT"]["matrix"]["real_clean"]["new_exact_endpoint_checker"]["result"] == "PASS"
       and persisted["CTRL_4_EXACT_ENDPOINT_REBUILT"]["matrix"]["historical_edi_clobber"]["new_exact_endpoint_checker"]["result"] == "FAIL"
       and persisted["CTRL_4_EXACT_ENDPOINT_REBUILT"]["matrix"]["final_push_esi"]["new_exact_endpoint_checker"]["result"] == "FAIL"
       and persisted["CTRL_4_EXACT_ENDPOINT_REBUILT"]["matrix"]["final_push_nop"]["new_exact_endpoint_checker"]["result"] == "FAIL"
       and desk["own_exact_endpoint_predicate"] == {"clean": True, "recorded_mutant": False,
                                                     "wrong_final_push_ESI": False,
                                                     "missing_final_push_NOP": False})
rec("C4_executor_checker_and_matrix", ok4,
    "the EXECUTOR's rebuilt checker executed BY THIS QC on the same four buffers: identical results to MY "
    "checker (clean PASS; clobber FAIL; esi FAIL; nop FAIL); equals the persisted CONTROL_RESULTS.json matrix; "
    "equals the Desktop own_exact_endpoint_predicate (clean=true, recorded_mutant=false, ESI=false, NOP=false)")

# ---------------------------------------------------------------- C5: old-logic reproduction (the superseded defect)
old = {name: X4.ctrl4_OLD_logic(buf) for name, buf, _ in M_CASES}
ok5 = (old["real_clean"][0] and not old["historical_edi_clobber"][0]
       and old["final_push_esi"][0] and old["final_push_nop"][0])
rec("C5_old_logic_false_pass_reproduced", ok5,
    "the old checker's logic reproduction: clean PASS; clobber FAIL; FALSE PASS on ESI and NOP — "
    "exactly the two Desktop false PASS (the superseded any-push-edi defect), reproduced over in-memory buffers")

# ---------------------------------------------------------------- C6: MY adversarial mutants through BOTH
A = [
    ("A1a_head_displaced_nop@B7", byte_mutant(HEAD_VA, 0x8B, 0x90), "P1"),
    ("A1b_head_alt_form_89C7", bytes([0x89, 0xC7]) + CLEAN[2:], "P1"),
    ("A2_push_edi_at_F4F5_not_F6", tail_mutant(bytes([0x57, 0x57, 0x90, 0xFF, 0xD2])), "P3"),
    ("A3a_call_shifted_to_F8", tail_mutant(bytes([0x6A, 0x00, 0x90, 0x57, 0xFF, 0xD2])), "P3+P4"),
    ("A3b_call_truncated_at_F8", tail_mutant(bytes([0x6A, 0x00, 0x90, 0x90, 0xFF])), "fail-closed"),
    ("A4a_pop_edi@E3", byte_mutant(0x0050A3E3, 0x56, 0x5F), "P2"),
    ("A4b_pop_edi@D6", byte_mutant(0x0050A3D6, 0x50, 0x5F), "P2"),
    ("A5_push_edi_FFF7_form@F6", tail_mutant(bytes([0x6A, 0x00, 0xFF, 0xF7, 0x90])), "P3+P4"),
    ("A6_final_removed_earlier_survives", byte_mutant(FINAL_PUSH_VA, 0x57, 0x90), "P3"),
]
adv_rows = []
ok6 = True
for name, buf, expect in A:
    okm, detm = my_ctrl4(buf)
    oke, dete = X4.ctrl4_exact_endpoint(buf)
    old_pass = X4.ctrl4_OLD_logic(buf)[0]
    agree = (okm == oke) and (not okm)
    if not agree:
        ok6 = False
    adv_rows.append({"mutant": name, "expected_fail_leg": expect,
                     "my_checker": "PASS" if okm else "FAIL", "my_detail": detm,
                     "executor_checker": "PASS" if oke else "FAIL", "executor_detail": dete,
                     "old_logic_result": "PASS" if old_pass else "FAIL"})
    print(f"    [adv] {name}: mine={'PASS' if okm else 'FAIL'} exec={'PASS' if oke else 'FAIL'} "
          f"old={'PASS' if old_pass else 'FAIL'} — {detm}")
rec("C6_adversarial_mutants", ok6,
    f"all {len(A)} adversarial mutants FAIL BOTH checkers (mine == executor's on every buffer; zero "
    f"false PASS on the rebuilt predicate): head displacement (P1), alternative head byte-form 89 C7 (P1), "
    f"real push edi at F4/F5 but not at the exact site (P3), join call shifted to F8 (P3+P4), truncated call "
    f"(fail-closed), pop-edi EDI writes at E3 and D6 (P2), 2-byte FF F7 push form (P3 exact byte form), "
    f"final removed with the earlier push surviving (P3; the OLD logic FALSE-PASSES it — the closed hole)")

# ---------------------------------------------------------------- C7: CTRL_3 — my checker + executor's + adversarial
def my_ctrl3(fixture):
    """PASS iff the accessor instruction reads [ecx + 0x68] (any encoding form)."""
    try:
        if fixture[0] != 0x8B:
            return False, "not the 8B mov r32,r/m32 accessor form"
        mod, reg, rm = modrm(fixture, 1)
        dlen = modrm_len(mod, rm)
        disp = int.from_bytes(fixture[2:2 + dlen], "little") if dlen else 0
        if mod == 0b11:
            return False, "register form does not read a field"
        reads = (rm == 1) and disp == 0x68
        return reads, (f"reads {'[ecx + 0x%x]' % disp if rm == 1 else '[%s + 0x%x]' % (REG[rm], disp)}"
                       f"{' == the producer-written field' if reads else ' != [ecx+0x68]'}")
    except (ValueError, IndexError) as e:
        return False, f"fixture not decodable ({e})"


C3F = [
    ("clean_getter_pin", bytes.fromhex("8B 41 68 C3 CC CC CC CC"), "PASS"),
    ("foreign_accessor_0x120", bytes.fromhex("8B 81 20 01 00 00 C3 CC"), "FAIL"),
    ("adv_wrong_offset_0x69", bytes.fromhex("8B 41 69 C3 CC CC CC CC"), "FAIL"),
    ("adv_wrong_base_esi_0x68", bytes.fromhex("8B 46 68 C3 CC CC CC CC"), "FAIL"),
    ("adv_same_field_disp32_form", bytes.fromhex("8B 81 68 00 00 00 C3 CC"), "PASS"),
]
spec3 = importlib.util.spec_from_file_location("exec_ctrl3", os.path.join(PKG, "03_SCRIPTS", "ctrl3_rebuilt.py"))
X3 = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(X3)
ok7 = True
c3rows = []
for name, fx, expected in C3F:
    oka, deta = my_ctrl3(fx)
    okb, detb = X3.ctrl3_provenance(fx)
    if ("PASS" if oka else "FAIL") != expected or oka != okb:
        ok7 = False
    c3rows.append({"fixture": name, "expected": expected, "mine": "PASS" if oka else "FAIL",
                   "executor": "PASS" if okb else "FAIL"})
    print(f"    [c3] {name}: mine={'PASS' if oka else 'FAIL'} exec={'PASS' if okb else 'FAIL'} (expected {expected})")
rec("C7_ctrl3", ok7,
    "CTRL_3 rebuilt verified on MY OWN checker AND the executor's (same fixtures): clean getter pin "
    "8B 41 68 C3 = PASS; the recorded historical probe constant 8B 81 20 01 00 00 = FAIL ([ecx+0x120]); "
    "MY adversarial fixtures: [ecx+0x69] FAIL, [esi+0x68] FAIL (offset and base-register specificity), "
    "disp32 form of [ecx+0x68] PASS (semantically identical encoding must NOT false-fail); both checkers "
    "agree on every fixture; ZERO EXE access (synthetic/persisted-prior-pin only)")

# ---------------------------------------------------------------- C8: window arithmetic on MY decoder
ins = my_decode(CLEAN, WIN_VA)
calls = {va: i.ops for va, i in ins.items() if i.mn == "call"}
ok8 = (calls.get(0x0050A3B9) == "0x006c0f90" and calls.get(0x0050A3CF) == "0x006c10b0"
       and calls.get(0x0050A3D8) == "0x0050a1e0" and calls.get(0x0050A3E4) == "0x005246e0"
       and calls.get(0x0050A3F7) == "edx"
       and ins[0x0050A3C0].ops == "0x0050a3c8" and ins[0x0050A3C6].ops == "0x0050a3cc")
rec("C8_window_arithmetic", ok8,
    "MY decoder recomputes the window arithmetic: call rel32 targets 0x006C0F90 / 0x006C10B0 / 0x0050A1E0 / "
    "0x005246E0 and the je/jmp rel8 targets 0x0050A3C8 / 0x0050A3CC — all exact; the join endpoint decodes "
    "as call edx @0x0050A3F7 (FF D2)")

# ---------------------------------------------------------------- save
out = {"C_results": results, "adversarial_mutant_matrix": adv_rows, "ctrl3_matrix": c3rows,
       "mandatory_matrix": {n: {"my_checker": "PASS" if mine[n][0] else "FAIL",
                                "executor_checker": "PASS" if exe_res[n][0] else "FAIL",
                                "old_logic": "PASS" if old[n][0] else "FAIL",
                                "expected": e} for n, _, e in M_CASES}}
path = os.path.join(QC_DIR, "QC_IND_PART2_RESULTS.json")
with open(path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"\npart2: {sum(1 for v in results.values() if v['ok'])}/{len(results)} PASS -> {path}")
sys.exit(0 if all(v['ok'] for v in results.values()) else 1)
