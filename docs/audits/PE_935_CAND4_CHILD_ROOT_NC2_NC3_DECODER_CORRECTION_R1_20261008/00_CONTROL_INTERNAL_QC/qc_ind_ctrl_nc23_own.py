"""qc_ind_ctrl_nc23_own.py — FRESH INDEPENDENT INTERNAL QC of the NC2+NC3 correction run
PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008
(RECORDS_AND_QC_MACHINERY_CORRECTION; frozen human-authorized dispatch contract
OPENCODE_NC2_NC3_CORRECTION.md, SIZE 14069, SHA256
3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F — verified
in full before any work; executor phase already performed by pe-reconstruction).

Author/origin: pe-master-auditor, FRESH-CONTEXT independent internal QC under direct
PE-MASTER dispatch. This is NOT the executor's self-review, NOT a Desktop post-audit
and NOT the future Desktop post-audit of the eventual published correction SHA.
RECORDS/QC-MACHINERY ONLY: ZERO EXE access; every buffer is a SYNTHETIC IN-MEMORY
byte string re-derived BY THIS QC from the PUBLISHED record
(docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/01_RAW/
JOIN_WINDOW_50A3B7_REPIN.txt — SHA256-pinned below). Nothing is written except THIS
QC's own QC_RESULTS.json in this directory (plus QC_REPORT.md authored in the same
QC session, outside this script).

INDEPENDENCE STATEMENT:
- This engine is the CORRECTED SUCCESSOR of the historical internal-QC implementation
  (SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py, pe-master-auditor
  lineage, READ-ONLY, SHA256-pinned). It keeps the historical internal-QC
  implementation style (own mem_dlen displacement helper, own Insn class, own
  fail-closed linear decode, own P1-P4 checker) and applies the three NC2/NC3
  corrections to the QC side:
    NC2  (kept from the historical engine — it was already correct there): the 0x84
         branch rejects EVERY memory TEST form (mod != 0b11) BEFORE any length
         computation; register TEST (84 C0) stays supported.
    NC3-A (CORRECTED HERE — the historical engine's defect): the FF /3 acceptance
         branch is REMOVED (FF D8 is the invalid register encoding of far CALL, not a
         PUSH); only FF /2 (call r/m32) with mod=11 remains (the FF D2 endpoint);
         FF /6 and no other forms are added.
    NC3-B (CORRECTED HERE): LEA with mod=11 (invalid x86 encoding, e.g. 8D C0) is
         rejected EXPLICITLY, BEFORE any operand formatting and before any verdict
         computation — the checker returns (False, diagnostic), never TypeError.
  NC1 is PRESERVED: every memory-ModRM branch rejects mod != 0b11 with rm == 0b100
  (SIB) before any displacement/length computation (mem_dlen for 0x8B/0x89/0x8D and
  0x83; the register-only fail-closed raises for 0x84 and 0xFF cover their SIB
  subcases before any length arithmetic as well).
- It does NOT import the production decoder into its verdict path, shares NO decoder
  helper with production and does NOT copy production's _reject_sib/decode structure
  (production: standalone _reject_sib helper + inline size/memoff table; this engine:
  mem_dlen fused guard + own formatting paths — structurally different code, same
  contract-mandated predicates).
- The ACTUAL corrected production checker (03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py)
  IS executed separately, via importlib, ONLY for comparison on the same in-memory
  buffers (module import-inert — verified by THIS QC's FULL READ of all 377 lines:
  no file I/O, no writers, only a fixture-length assert at module level).
- DISCLOSED SHARED ASSUMPTION (by design, contract-mandated): both this checker and
  production implement the SAME contract-mandated P1-P4 exact-endpoint predicate and
  the SAME eight-case matrix definitions. The predicate and case set are fixed by the
  frozen contract; the IMPLEMENTATIONS are independent. Their agreement on the matrix
  is a same-predicate cross-check of two independent decoders, NOT a universal
  x86-decoder correctness proof (never claimed: GENERAL_X86_DECODER_PROVEN).

QC scope (dispatch terminal gate, all conditions recorded individually):
  G1  16/16 required matrix rows match (8 cases x [this QC's own checker, the ACTUAL
      corrected production checker executed via importlib]).
  G2  production authenticity: measured script SHA256 equals the pinned/declared SHA
      AND case-by-case equality of this QC's own re-execution with every
      CONTROL_RESULTS_POST.json matrix row.
  G3  clean-window decode boundary regression: this QC's own decode produces the
      published 22-instruction VA/size map (total 0x42), exact P1/P3/P4 endpoints.
  G4  the nine historical SIB negative cases (re-derived SAFELY from the historical
      QC script via ast.parse + ast.literal_eval — the historical top level is NEVER
      executed/imported; it writes QC_RESULTS.json) are rejected by BOTH decoders 9/9.
  G5  the 144-form Desktop sweep (6 opcode branches 8B/89/8D/84/83/FF x 3 memory mod
      00/01/10 x 8 reg, always rm=4) is rejected at DECODER level by BOTH decoders,
      with the form set identical to the cited Desktop sweep.
  G6  explicit NC2/NC3 rejection mechanisms recorded for cases 6-8 (both engines)
      AND zero unexpected exceptions in all 16 matrix rows.
  QC_PASS = G1..G6 all PASS. Any FAIL/ERROR/NOT_PERFORMED forbids QC_PASS.
  One targeted repair round (NC2/NC3 only) is allowed by the contract; any other
  material finding stays OPEN.

Deterministic: NO timestamps anywhere in QC_RESULTS.json.
"""

import sys
sys.dont_write_bytecode = True   # FIRST: never write __pycache__/.pyc anywhere

import ast
import hashlib
import importlib.util
import json
import os
import re

# ---------------------------------------------------------------- paths (READ-ONLY inputs)
HERE = os.path.dirname(os.path.abspath(__file__))            # OUTPUT_ROOT/00_CONTROL_INTERNAL_QC
PKG = os.path.dirname(HERE)                                   # OUTPUT_ROOT
REPO = os.path.dirname(os.path.dirname(os.path.dirname(PKG)))  # eudoria-clean repo root

RUN_ID = "PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008"

CONTRACT = (r"C:\Users\User\Documents\ChatGPT\PE\PE_935_NC2_NC3_CORRECTION_PROMPT_20261008"
            r"\OPENCODE_NC2_NC3_CORRECTION.md")
DESKTOP_CC = (r"C:\Users\User\Documents\ChatGPT\PE\PE_935_NC1_DESKTOP_POST_AUDIT_91598A98_20261007"
              r"\CONTROL_COUNTERCHECKS.json")
HIST_QC = os.path.join(REPO, "docs", "audits",
                       "PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007",
                       "00_CONTROL_INTERNAL_QC", "qc_ind_ctrl_sib_own.py")
HIST_PROD = os.path.join(REPO, "docs", "audits",
                         "PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007",
                         "03_SCRIPTS", "ctrl4_exact_endpoint_sibfixed.py")
WIN_RECORD = os.path.join(REPO, "docs", "audits",
                          "PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007", "01_RAW",
                          "JOIN_WINDOW_50A3B7_REPIN.txt")
NEW_PROD = os.path.join(PKG, "03_SCRIPTS", "ctrl4_exact_endpoint_nc23fixed.py")
POST_JSON = os.path.join(PKG, "CONTROL_RESULTS_POST.json")
PRE_JSON = os.path.join(PKG, "CONTROL_RESULTS_PRE.json")

RESULTS = {}


def rec(cid, ok, detail):
    RESULTS[cid] = {"ok": bool(ok), "detail": detail}
    print(("PASS  " if ok else "FAIL  ") + cid + ": " + detail)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def sha256_file(path):
    with open(path, "rb") as f:
        return sha256_bytes(f.read())


def size_file(path):
    return os.path.getsize(path)


def hexsp(b):
    return " ".join(f"{x:02X}" for x in b)


# ================================================================ Q0: pinned input identities
PINS = {
    "dispatch_contract": {"path": CONTRACT, "size": 14069,
                          "sha256": "3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F"},
    "published_window_record": {"path": WIN_RECORD, "size": 4043,
                                "sha256": "A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3"},
    "historical_internal_qc_READ_ONLY": {"path": HIST_QC, "size": 51943,
                                         "sha256": "529B61DB312AEC338221425B12F2D94DE2BE351B5C62F68DDBA6BF915B007B25"},
    "historical_production_sibfixed_READ_ONLY": {"path": HIST_PROD, "size": 17740,
                                                 "sha256": "44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405"},
    "corrected_production_nc23fixed": {"path": NEW_PROD, "size": 21069,
                                       "sha256": "68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13"},
    "control_results_pre_json": {"path": PRE_JSON, "size": 51477,
                                 "sha256": "00A90A837E08E1FE7661C0C1E184417200E494587F1FB3A4E098A93B3D7E08B1"},
    "control_results_post_json": {"path": POST_JSON, "size": 71311,
                                  "sha256": "5E09A5126672F63D2F6C1E19543505597FF80B2C55C13259139DB78C3E12E49D"},
    "desktop_control_counterchecks_CITED": {"path": DESKTOP_CC, "size": 132471,
                                            "sha256": "AD8DC2052F714439497A277512944EF729F53BDC94B436CB20EE09FEE6BCC28D"},
}

INPUTS = {}
pins_ok = True
for key, pin in PINS.items():
    size = size_file(pin["path"])
    sha = sha256_file(pin["path"])
    match = (size == pin["size"] and sha == pin["sha256"])
    pins_ok = pins_ok and match
    INPUTS[key] = {"path": pin["path"], "size_bytes": size, "size_pin": pin["size"],
                   "sha256": sha, "sha256_pin": pin["sha256"], "match": match}
rec("Q0_input_identities", pins_ok,
    "all 8 pinned inputs physically re-measured by THIS QC (contract, published window record, "
    "historical QC script, historical sibfixed production, corrected nc23fixed production, "
    "CONTROL_RESULTS_PRE.json, CONTROL_RESULTS_POST.json, Desktop CONTROL_COUNTERCHECKS.json): "
    + ("ALL MATCH" if pins_ok else "MISMATCH — BLOCKED_INPUT_IDENTITY"))
if not pins_ok:
    out = {"RUN_ID": RUN_ID, "QC_ORIGIN": "FRESH_INDEPENDENT_INTERNAL_QC_BY_PE_MASTER_AUDITOR",
           "QC_VERDICT": "BLOCKED_INPUT_IDENTITY", "inputs": INPUTS}
    with open(os.path.join(HERE, "QC_RESULTS.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    sys.exit(3)

# ================================================================ Q1: window re-derivation (MY OWN parser)
WIN_VA = 0x0050A3B7
HEAD_VA = 0x0050A3B7
FINAL_PUSH_VA = 0x0050A3F6
JOIN_CALL_VA = 0x0050A3F7
NC23_SPAN_VA = 0x0050A3DD
NC23_SPAN_LEN = 12

with open(WIN_RECORD, encoding="utf-8") as f:
    win_txt = f.read()
pat = re.compile(r"^  0x([0-9a-f]{8})  ((?:[0-9A-F]{2} )*[0-9A-F]{2})", re.M)
pieces = sorted((int(v, 16), bytes.fromhex(bx)) for v, bx in pat.findall(win_txt))
MY_WINDOW = b"".join(bx for _, bx in pieces)
PUB_VA_SIZES = {va: len(bx) for va, bx in pieces}
first_ok = bool(pieces) and pieces[0][0] == WIN_VA
contig = all(pieces[i][0] + len(pieces[i][1]) == pieces[i + 1][0] for i in range(len(pieces) - 1))
rec("Q1_window_rederivation", first_ok and contig and len(pieces) == 22 and len(MY_WINDOW) == 0x42,
    f"clean window re-derived MY OWN way from the published record: {len(pieces)} instructions, "
    f"first VA 0x0050A3B7, contiguous boundaries, total 0x{len(MY_WINDOW):X}; "
    f"buffer SHA256 {sha256_bytes(MY_WINDOW)}")

# ================================================================ Q2: MY OWN corrected decoder + checker
# Successor of the historical internal-QC engine (qc_ind_ctrl_sib_own.py) with the
# NC2 (kept), NC3-A (removed /3) and NC3-B (LEA mod=11 rejected) corrections.
REG = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
GRP1 = ["add", "or", "adc", "sbb", "and", "sub", "xor", "cmp"]


class Insn:
    __slots__ = ("va", "size", "mn", "ops", "wedi", "raw")

    def __init__(self, va, size, mn, ops, wedi, raw):
        self.va, self.size, self.mn, self.ops = va, size, mn, ops
        self.wedi = wedi
        self.raw = raw


def mrm_split(buf, i):
    mb = buf[i]
    return (mb & 0b11000000) >> 6, (mb & 0b00111000) >> 3, mb & 0b00000111


def mem_dlen(mod, rm):
    """Displacement length helper — NC1 guard fused BEFORE any length arithmetic:
    a memory form (mod != 0b11) with rm == 0b100 carries a SIB byte this engine does
    not decode; it is rejected here, before any displacement or instruction-length
    computation (the historical shared false-pass defect). Register forms carry no
    displacement (length 0)."""
    if mod != 0b11 and rm == 0b100:
        raise ValueError(f"SIB memory form rejected fail-closed (mod={mod:02b}, rm=100) "
                         f"before any displacement/length computation — NC1 guard")
    if mod == 0b01:
        return 1
    if mod == 0b10 or (mod == 0b00 and rm == 0b101):
        return 4
    return 0


def my_decode(buf, base_va):
    """My own linear fail-closed decode. Raises on any uncovered form; a SIB memory
    form raises via mem_dlen BEFORE any length arithmetic; every memory TEST form
    (mod != 11) raises BEFORE any length computation (NC2); LEA mod=11 raises BEFORE
    operand formatting (NC3-B); the FF branch accepts ONLY /2 mod=11 (NC3-A: the
    historical erroneous /3 acceptance is removed; /6 and other forms NOT added).
    Bytes are never skipped and decode never continues past a rejected form."""
    out = {}
    i, va = 0, base_va
    while i < len(buf):
        start, op = i, buf[i]
        wedi = False
        if op in (0x8B, 0x89, 0x8D):                      # mov r32,r/m32 | mov r/m32,r32 | lea
            mod, reg, rm = mrm_split(buf, i + 1)
            dlen = mem_dlen(mod, rm)                      # NC1 guard (memory forms); reg form -> 0
            if op == 0x8D and mod == 0b11:                # NC3-B: LEA register form is INVALID x86 —
                raise ValueError("unsupported LEA register form (mod=11) — fail-closed (NC3-B)")  # reject BEFORE formatting
            disp = int.from_bytes(buf[i + 2:i + 2 + dlen], "little") if dlen else 0
            if mod == 0b11:
                if op == 0x89:                           # mov rm, reg — writes rm
                    ops, wedi = f"{REG[rm]}, {REG[reg]}", (rm == 7)
                else:                                    # mov reg, rm — writes reg
                    ops, wedi = f"{REG[reg]}, {REG[rm]}", (reg == 7)
            elif mod == 0b00 and rm == 0b101:            # moffs disp32
                ops = (f"{REG[reg]}, dword ptr [0x{disp:08x}]" if op != 0x89
                       else f"dword ptr [0x{disp:08x}], {REG[reg]}")
                wedi = (op != 0x89) and (reg == 7)       # e.g. 8B 3D ... = mov edi,[moffs]: EDI write
            else:
                base = f"{REG[rm]} + 0x{disp:x}" if disp else REG[rm]
                ops = (f"{REG[reg]}, dword ptr [{base}]" if op != 0x89
                       else f"dword ptr [{base}], {REG[reg]}")
                wedi = (op != 0x89) and (reg == 7)       # memory writes never write a register
            size, mn = 2 + dlen, {0x8B: "mov", 0x89: "mov", 0x8D: "lea"}[op]
        elif op == 0x84:                                  # test r/m8, r8 — REGISTER FORMS ONLY
            mod, reg, rm = mrm_split(buf, i + 1)
            if mod != 0b11:                              # NC2: EVERY memory TEST form (incl. SIB)
                raise ValueError(f"uncovered test memory form (mod={mod:02b}) — fail-closed (NC2)")
            r8 = ("al", "cl", "dl", "bl", "ah", "ch", "dh", "bh")
            size, mn, ops = 2, "test", f"{r8[rm]}, {r8[reg]}"
        elif op in (0x74, 0xEB):                          # je/jmp rel8
            rel = buf[i + 1] - 0x100 if buf[i + 1] >= 0x80 else buf[i + 1]
            size, mn = 2, ("je" if op == 0x74 else "jmp")
            ops = f"0x{va + 2 + rel:08x}"
        elif op == 0x83:                                  # grp1 r/m32, imm8 (sign-extended)
            mod, reg, rm = mrm_split(buf, i + 1)
            if mod not in (0b01, 0b11):                   # fail-closed BEFORE mem_dlen
                raise ValueError(f"uncovered 0x83 mod={mod:02b} — fail-closed")
            dlen = mem_dlen(mod, rm)                      # NC1 guard (mod=01 rm=100 SIB); reg form -> 0
            imm = buf[i + 2 + dlen]
            imm = imm - 0x100 if imm >= 0x80 else imm     # sign-extend imm8 before masking
            if mod == 0b11:
                ops, wedi = f"{REG[rm]}, {imm:#x}", (rm == 7)
            else:
                ops = f"dword ptr [{REG[rm]} + 0x{buf[i + 2]:x}], {imm & 0xFFFFFFFF:#x}"
            size, mn = 3 + dlen, GRP1[reg]
        elif op == 0x6A:                                  # push imm8
            size, mn, ops = 2, "push", f"{buf[i + 1]}"
        elif 0x50 <= op <= 0x57:                          # push r32 (reads the register)
            size, mn, ops = 1, "push", REG[op - 0x50]
        elif 0x58 <= op <= 0x5F:                          # pop r32 (writes the register)
            size, mn, ops = 1, "pop", REG[op - 0x58]
            wedi = (op == 0x5F)
        elif op == 0xBF:                                  # mov edi, imm32 — writes EDI
            size, mn, ops = 5, "mov", f"edi, 0x{int.from_bytes(buf[i + 1:i + 5], 'little'):08x}"
            wedi = True
        elif op == 0xE8:                                  # call rel32
            rel = int.from_bytes(buf[i + 1:i + 5], "little", signed=True)
            size, mn, ops = 5, "call", f"0x{va + 5 + rel:08x}"
        elif op == 0xFF:                                  # grp5 — ONLY /2 (call r/m32) mod=11
            mod, reg, rm = mrm_split(buf, i + 1)
            if mod != 0b11:                              # every memory form (incl. SIB) fail-closed
                raise ValueError(f"uncovered FF memory form (reg={reg:03b} mod={mod:02b}) — fail-closed")
            if reg == 0b010:                             # /2 call r/m32 (FF D2 = call edx)
                size, mn, ops = 2, "call", REG[rm]
            else:
                # NC3-A: the historical erroneous /3 acceptance is REMOVED (FF D8 is the
                # invalid register encoding of far CALL, not a PUSH); FF /6 and no other
                # forms are added — only the required FF D2 endpoint stays supported
                raise ValueError(f"uncovered FF /{reg} mod=11 — fail-closed (NC3-A: only /2 call supported)")
        elif op == 0x90:
            size, mn, ops = 1, "nop", ""
        else:
            raise ValueError(f"uncovered opcode {op:02X} @0x{va:08X} — fail-closed")
        out[va] = Insn(va, size, mn, ops, wedi, bytes(buf[start:start + size]))
        i += size
        va += size
    return out


def my_ctrl4(buf, base_va=WIN_VA):
    """MY OWN exact-endpoint checker: P1..P4 simultaneous, exact addresses, exact byte
    forms. Any decode failure (ValueError/IndexError only — NO blanket catch; an
    unexpected exception PROPAGATES and would be recorded as ERROR) FAILS the window
    closed — never skip-and-continue."""
    try:
        ins = my_decode(buf, base_va)
    except (ValueError, IndexError) as e:
        return False, f"window not boundary-decodable ({e}) — FAIL closed"
    h = ins.get(HEAD_VA)
    if not h or h.raw != b"\x8B\xF8" or h.mn != "mov" or h.ops != "edi, eax":
        got = f"{h.mn} {h.ops} [{hexsp(h.raw)}]" if h else "none"
        return False, f"P1 FAIL: exact head mov edi,eax @0x0050A3B7 (8B F8) not found (got: {got})"
    for va in sorted(ins):
        if HEAD_VA < va < FINAL_PUSH_VA and ins[va].wedi:
            return False, f"P2 FAIL: caller-side EDI write @0x{va:08X} in the required range ({ins[va].mn} {ins[va].ops})"
    f = ins.get(FINAL_PUSH_VA)
    if not f or f.raw != b"\x57" or f.mn != "push" or f.ops != "edi":
        got = f"{f.mn} {f.ops} [{hexsp(f.raw)}]" if f else "none"
        return False, f"P3 FAIL: exact final child argument push edi @0x0050A3F6 (57) not found (got: {got})"
    j = ins.get(JOIN_CALL_VA)
    if not j or j.raw != b"\xFF\xD2" or j.mn != "call" or j.ops != "edx":
        got = f"{j.mn} {j.ops} [{hexsp(j.raw)}]" if j else "none"
        return False, f"P4 FAIL: exact join call endpoint call edx @0x0050A3F7 (FF D2) not found (got: {got})"
    return True, ("PASS: P1 head mov edi,eax @0x0050A3B7 (8B F8) exact; P2 no caller-side EDI write inside "
                  "(0x0050A3B7, 0x0050A3F6); P3 final push edi @0x0050A3F6 (57) exact; P4 join call edx "
                  "@0x0050A3F7 (FF D2) exact — on MY OWN verified decode boundaries")


# ================================================================ Q3: the eight buffers (MY OWN builders)
def build_span(window, va, orig_hex, repl_hex):
    b = bytearray(window)
    off = va - WIN_VA
    orig = bytes.fromhex(orig_hex)
    repl = bytes.fromhex(repl_hex)
    assert len(orig) == len(repl), "span replacement length mismatch"
    assert bytes(b[off:off + len(orig)]) == orig, f"original span mismatch at 0x{va:08X}"
    b[off:off + len(orig)] = repl
    return bytes(b)


def build_byteflip(window, va, old, new):
    b = bytearray(window)
    off = va - WIN_VA
    assert b[off] == old, f"byteflip site mismatch at 0x{va:08X}"
    b[off] = new
    return bytes(b)


def outside_preserved(buf, clean, va, ln):
    off = va - WIN_VA
    return bytes(buf[:off]) == bytes(clean[:off]) and bytes(buf[off + ln:]) == bytes(clean[off + ln:])


def p1_p3_p4_bytes(buf):
    return (bytes(buf[HEAD_VA - WIN_VA:HEAD_VA - WIN_VA + 2]) == b"\x8B\xF8"
            and buf[FINAL_PUSH_VA - WIN_VA] == 0x57
            and bytes(buf[JOIN_CALL_VA - WIN_VA:JOIN_CALL_VA - WIN_VA + 2]) == b"\xFF\xD2")


CLEAN = MY_WINDOW
NC23_ORIG12 = "8B 8E 8C 00 00 00 56 E8 F7 A2 01 00"          # the clean span @0x0050A3DD..0x0050A3E8
BUF = {
    "REAL_RECORDED_CLEAN": CLEAN,
    "HISTORICAL_EDI_CLOBBER": build_span(CLEAN, 0x0050A3DD, "8B 8E 8C 00 00 00", "8B 3D D0 D8 B9 00"),
    "FINAL_PUSH_ESI": build_byteflip(CLEAN, FINAL_PUSH_VA, 0x57, 0x56),
    "FINAL_PUSH_NOP": build_byteflip(CLEAN, FINAL_PUSH_VA, 0x57, 0x90),
    "NC1_SIB_HIDDEN_EDI_WRITE": build_span(CLEAN, NC23_SPAN_VA, NC23_ORIG12,
                                           "8B 8C 24 8C 00 00 E8 BF AA BB CC 90"),
    "NC2_NON_SIB_TEST_HIDDEN_EDI": build_span(CLEAN, NC23_SPAN_VA, NC23_ORIG12,
                                              "84 06 BF AA BB CC E8 90 90 90 90 90"),
    "NC3_INVALID_FF_FAR_CALL_REGISTER": build_span(CLEAN, NC23_SPAN_VA, NC23_ORIG12,
                                                   "FF D8 90 90 90 90 90 90 90 90 90 90"),
    "NC3_INVALID_LEA_REGISTER": build_span(CLEAN, NC23_SPAN_VA, NC23_ORIG12,
                                            "8D C0 90 90 90 90 90 90 90 90 90 90"),
}
CASE_ORDER = [
    "REAL_RECORDED_CLEAN", "HISTORICAL_EDI_CLOBBER", "FINAL_PUSH_ESI", "FINAL_PUSH_NOP",
    "NC1_SIB_HIDDEN_EDI_WRITE", "NC2_NON_SIB_TEST_HIDDEN_EDI", "NC3_INVALID_FF_FAR_CALL_REGISTER",
    "NC3_INVALID_LEA_REGISTER",
]
# (col1 = MY checker, col2 = ACTUAL corrected production checker) — dispatch matrix
REQUIRED_16 = {
    "REAL_RECORDED_CLEAN": ("PASS", "PASS"),
    "HISTORICAL_EDI_CLOBBER": ("FAIL", "FAIL"),
    "FINAL_PUSH_ESI": ("FAIL", "FAIL"),
    "FINAL_PUSH_NOP": ("FAIL", "FAIL"),
    "NC1_SIB_HIDDEN_EDI_WRITE": ("FAIL", "FAIL"),
    "NC2_NON_SIB_TEST_HIDDEN_EDI": ("FAIL", "FAIL"),
    "NC3_INVALID_FF_FAR_CALL_REGISTER": ("FAIL", "FAIL"),
    "NC3_INVALID_LEA_REGISTER": ("FAIL", "FAIL"),
}

buffer_records = {}
for name in CASE_ORDER:
    buf = BUF[name]
    if name == "REAL_RECORDED_CLEAN":
        span_va, span_len = None, 0
    elif name in ("FINAL_PUSH_ESI", "FINAL_PUSH_NOP"):
        span_va, span_len = FINAL_PUSH_VA, 1
    elif name == "HISTORICAL_EDI_CLOBBER":
        span_va, span_len = 0x0050A3DD, 6
    else:
        span_va, span_len = NC23_SPAN_VA, NC23_SPAN_LEN
    outside = True if span_va is None else outside_preserved(buf, CLEAN, span_va, span_len)
    assert len(buf) == 0x42, f"{name}: window must stay 0x42"
    assert outside, f"{name}: bytes outside the mutation span must be identical to clean"
    if name not in ("FINAL_PUSH_ESI", "FINAL_PUSH_NOP"):
        assert p1_p3_p4_bytes(buf), f"{name}: P1/P3/P4 bytes must be preserved"
    else:
        assert not p1_p3_p4_bytes(buf), f"{name}: P3 must be broken by design"
    buffer_records[name] = {
        "buffer_len_bytes": len(buf),
        "buffer_hex": hexsp(buf),
        "buffer_sha256": sha256_bytes(buf),
        "mutation_span_va": (f"0x{span_va:08X}" if span_va else None),
        "mutation_span_len": span_len,
        "bytes_outside_span_preserved_vs_clean": outside,
        "p1_p3_p4_bytes_preserved": p1_p3_p4_bytes(buf),
    }

# cross-check: MY NC2/NC3 buffers byte-identical to the cited Desktop residual cases
desktop_cc = json.load(open(DESKTOP_CC, encoding="utf-8"))
desktop_residual = desktop_cc["residual_tests"]
DESKTOP_CASE_FOR = {
    "NC2_NON_SIB_TEST_HIDDEN_EDI": "NON_SIB_TEST_HIDDEN_EDI",
    "NC3_INVALID_FF_FAR_CALL_REGISTER": "INVALID_FF_FAR_CALL_REGISTER",
    "NC3_INVALID_LEA_REGISTER": "INVALID_LEA_REGISTER",
}
desktop_buffer_identity = {}
for case_name, desk_name in DESKTOP_CASE_FOR.items():
    desk_buf = bytes.fromhex(desktop_residual[desk_name]["buffer"])
    desktop_buffer_identity[case_name] = {
        "desktop_case": desk_name,
        "byte_identical_to_my_buffer": bytes(BUF[case_name]) == desk_buf,
    }
desk_buf_ok = all(v["byte_identical_to_my_buffer"] for v in desktop_buffer_identity.values())
rec("Q3_buffer_construction", desk_buf_ok,
    "all eight buffers re-derived MY OWN way (clean via my parser; cases 2-5 same definitions as the "
    "NC1 package; cases 6-8 replace EXACTLY the 12 bytes @0x0050A3DD..0x0050A3E8, window stays 0x42, "
    "bytes outside the span verified identical, P1/P3/P4 preserved); MY NC2/NC3 buffers are "
    "byte-identical to the cited Desktop residual case buffers 3/3: " + str(desk_buf_ok))

# ================================================================ Q4: 16-row matrix (mine + ACTUAL production via importlib)
spec = importlib.util.spec_from_file_location("ctrl4_exact_endpoint_nc23fixed_QC", NEW_PROD)
PROD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PROD)          # import-inert (full-read verified: no file I/O, no writer)
prod_fixture_identity = bytes(PROD.CLEAN_WINDOW) == MY_WINDOW


def run_one(fn, buf):
    """Run ONE checker call. Classification catch at the HARNESS boundary only (an
    unexpected exception escaping a checker is recorded as ERROR — never as FAIL and
    never silently swallowed); the checkers themselves catch only (ValueError, IndexError)."""
    try:
        ok, detail = fn(buf)
    except Exception as exc:            # harness classification only — NOT inside any checker
        return {"result": "ERROR", "exception": type(exc).__name__, "detail": f"{type(exc).__name__}: {exc}"}
    return {"result": "PASS" if ok else "FAIL", "exception": None, "detail": detail}


MATRIX = {}
rows_ok = True
unexpected_exceptions = 0
for name in CASE_ORDER:
    mine = run_one(my_ctrl4, BUF[name])
    prod = run_one(PROD.ctrl4_exact_endpoint, BUF[name])
    req_mine, req_prod = REQUIRED_16[name]
    row_ok = (mine["result"] == req_mine and prod["result"] == req_prod)
    rows_ok = rows_ok and row_ok
    unexpected_exceptions += (1 if mine["result"] == "ERROR" else 0) + (1 if prod["result"] == "ERROR" else 0)
    MATRIX[name] = {
        "required": {"independent_qc_own": req_mine, "production": req_prod},
        "independent_qc_own": mine,
        "production_reexecution": prod,
        "row_ok": row_ok,
    }
    print(f"    [row] {name:34s} mine={mine['result']:4s} (req {req_mine:4s})  "
          f"prod={prod['result']:4s} (req {req_prod:4s})")
g1_pass = rows_ok and prod_fixture_identity
rec("Q4_g1_16_row_matrix", g1_pass,
    f"16/16 required rows match (8 cases x 2 independent implementations): clean PASS/PASS; "
    f"clobber, esi, nop, NC1 SIB, NC2 TEST, NC3 FF D8, NC3 LEA all FAIL/FAIL; production fixture "
    f"byte-identical to MY re-derived window: {prod_fixture_identity}")

# ================================================================ Q5 (G2): production authenticity vs CONTROL_RESULTS_POST.json
post = json.load(open(POST_JSON, encoding="utf-8"))
post_rows = post["nc23_matrix_post"]
prod_sha = sha256_file(NEW_PROD)
sha_match = (prod_sha == PINS["corrected_production_nc23fixed"]["sha256"]
             and prod_sha == post["production_checker"]["script_sha256"])
row_agreement = {}
for name in CASE_ORDER:
    prow = post_rows[name]
    row_agreement[name] = {
        "post_actual": prow["actual"],
        "my_production_reexecution": MATRIX[name]["production_reexecution"]["result"],
        "actual_equal": prow["actual"] == MATRIX[name]["production_reexecution"]["result"],
        "detail_equal": prow["checker_detail"] == MATRIX[name]["production_reexecution"]["detail"],
        "buffer_sha256_equal": prow["buffer_sha256"] == sha256_bytes(BUF[name]),
        "buffer_hex_equal": prow["buffer_hex"] == hexsp(BUF[name]),
        "buffer_len_equal": prow["buffer_len_bytes"] == len(BUF[name]),
        "expected_equal": prow["expected"] == REQUIRED_16[name][1],
        "post_match_flag": prow["match"] is True,
    }
rows_equal = all(v["actual_equal"] and v["detail_equal"] and v["buffer_sha256_equal"]
                 and v["buffer_hex_equal"] and v["buffer_len_equal"]
                 and v["expected_equal"] and v["post_match_flag"] for v in row_agreement.values())

# static structural verification of the corrected production source (complements THIS QC's
# FULL READ of all 377 lines). REPAIRED AFTER THE FIRST QC RUN (disclosed repair round 1/1,
# NC2/NC3-scoped, on THIS QC's own check — NOT on the audited production code): the first
# run's predicates were modeled on the sibfixed layout and (a) matched the module DOCSTRING's
# verbatim quotes of the NC2/NC3 raise statements instead of the real code lines, and
# (b) searched for the sibfixed 0x84 memory length table that the NC2 correction REMOVED BY
# DESIGN. The repaired check anchors on actual code: module docstring excluded via its ast
# end_lineno; the 0x84 branch scanned as header -> _modrm -> NC1 guard -> NC2 raise -> length
# assignment; the LEA operand-formatting line anchored to ITS OWN "mn = \"lea\"" sub-branch.
prod_src = open(NEW_PROD, encoding="utf-8").read()
prod_lines = prod_src.split("\n")
prod_tree = ast.parse(prod_src)
_doc_end = (prod_tree.body[0].end_lineno
            if prod_tree.body and isinstance(prod_tree.body[0], ast.Expr)
            and isinstance(prod_tree.body[0].value, ast.Constant)
            and isinstance(prod_tree.body[0].value.value, str) else 0)


def code_line_of(pred):
    """First CODE line (after the module docstring) matching pred — the docstring quotes
    the NC2/NC3 raise statements verbatim, so plain substring search hits prose, not code."""
    for idx, ln in enumerate(prod_lines, start=1):
        if idx <= _doc_end:
            continue
        if pred(ln):
            return idx
    return None


sib_guard_def = code_line_of(lambda l: l.startswith("def _reject_sib(mod, rm):"))
sib_call_lines = [i for i, l in enumerate(prod_lines, start=1)
                  if i > _doc_end and "_reject_sib(mod, rm)" in l and not l.startswith("def")]
nc3b_line = code_line_of(lambda l: "unsupported LEA register form" in l and "raise" in l)
catch_line = code_line_of(lambda l: "except (ValueError, IndexError)" in l)

# 0x84 branch scan (code only): in the CORRECTED module the memory-TEST length table NO
# LONGER EXISTS (that removal IS the NC2 correction); the branch's only length computation
# is the register-form "size = 2", and the NC2 raise must precede it.
test84_header = code_line_of(lambda l: l.strip().startswith("elif op == 0x84:"))
test84_modrm = test84_guard = test84_nc2 = test84_size = None
if test84_header:
    for i in range(test84_header + 1, len(prod_lines) + 1):
        ln = prod_lines[i - 1]
        if i > _doc_end and ln.strip().startswith("elif op =="):
            break
        s = ln.strip()
        if test84_modrm is None and "_modrm(buf, i + 1)" in ln:
            test84_modrm = i
        elif test84_guard is None and "_reject_sib(mod, rm)" in ln:
            test84_guard = i
        elif test84_nc2 is None and "unsupported memory TEST form" in ln:
            test84_nc2 = i
        elif test84_size is None and s == "size = 2":
            test84_size = i
# LEA operand-formating line: anchored to the "mn = \"lea\"" sub-branch (distinct from the
# 0x8B branch's own op_str assignments that a bare substring search would hit first).
mn_lea_line = code_line_of(lambda l: l.strip() == 'mn = "lea"')
lea_format_line = None
if mn_lea_line:
    for i in range(mn_lea_line - 1, _doc_end, -1):
        if prod_lines[i - 1].strip().startswith("op_str ="):
            lea_format_line = i
            break

structural = {
    "docstring_end_line": _doc_end,
    "sib_guard_def_line": sib_guard_def,
    "sib_guard_call_lines": sib_call_lines,
    "sib_guard_call_site_count": len(sib_call_lines),
    "test84_branch_header_line": test84_header,
    "test84_modrm_line": test84_modrm,
    "test84_nc1_guard_line": test84_guard,
    "nc2_reject_line": test84_nc2,
    "test84_size_line": test84_size,
    "test84_memory_length_table_removed": code_line_of(
        lambda l: "size = 2 if mod == 0b11 else" in l) is None,
    "nc2_raise_before_any_length_computation": (test84_nc2 is not None and test84_size is not None
                                                and test84_nc2 < test84_size),
    "nc1_guard_before_nc2_raise_in_84_branch": (test84_guard is not None and test84_nc2 is not None
                                               and test84_guard < test84_nc2),
    "nc3b_reject_line": nc3b_line,
    "lea_operand_format_line": lea_format_line,
    "nc3b_before_lea_formatting": (nc3b_line is not None and lea_format_line is not None
                                   and nc3b_line < lea_format_line),
    "checker_catch_line": catch_line,
    "four_memory_modrm_branches_guarded": len(sib_call_lines) == 4,
    "catch_only_valueerror_indexerror": catch_line is not None and "except Exception" not in prod_src,
}
structural_ok = (structural["nc2_raise_before_any_length_computation"]
                 and structural["nc1_guard_before_nc2_raise_in_84_branch"]
                 and structural["test84_memory_length_table_removed"]
                 and structural["nc3b_before_lea_formatting"]
                 and structural["four_memory_modrm_branches_guarded"]
                 and structural["catch_only_valueerror_indexerror"])

# my own engine mirror SELF-CHECK (honestly labeled: my verification of my own engine;
# PE-MASTER audits it independently) — functional falsifiers of the NC3-A/NC3-B/NC2 corrections
def _decode_raises(fn, b):
    try:
        fn(b, 0x00400000)
        return False, "NO RAISE — DECODED (DEFECT)"
    except (ValueError, IndexError) as exc:
        return True, f"{type(exc).__name__}: {exc}"


self_falsifiers = {
    "NC3A_FF_F7_must_raise (/3 removed)": _decode_raises(my_decode, bytes.fromhex("FF F7 90")),
    "NC3A_FF_D8_must_raise (/3 removed)": _decode_raises(my_decode, bytes.fromhex("FF D8 90")),
    "NC3A_FF_F0_must_raise (/6 NOT added)": _decode_raises(my_decode, bytes.fromhex("FF F0 90")),
    "NC3A_FF_D2_must_decode (/2 kept)": (True, "call edx") if
        (lambda ins: ins[0x00400000].mn == "call" and ins[0x00400000].ops == "edx")(my_decode(bytes.fromhex("FF D2 90"), 0x00400000))
        else (False, "FF D2 did not decode as call edx"),
    "NC3B_LEA_8D_C0_must_raise": _decode_raises(my_decode, bytes.fromhex("8D C0 90")),
    "NC3B_LEA_8D_06_must_decode": (True, "lea mem") if
        (lambda ins: ins[0x00400000].mn == "lea")(my_decode(bytes.fromhex("8D 06 90"), 0x00400000))
        else (False, "8D 06 did not decode as memory LEA"),
    "NC2_TEST_84_06_must_raise": _decode_raises(my_decode, bytes.fromhex("84 06 90")),
    "NC2_TEST_84_C0_must_decode": (True, "test al, al") if
        (lambda ins: ins[0x00400000].mn == "test" and ins[0x00400000].ops == "al, al")(my_decode(bytes.fromhex("84 C0 90"), 0x00400000))
        else (False, "84 C0 did not decode as register TEST"),
}
self_structural_ok = all(v[0] for v in self_falsifiers.values())

g2_pass = sha_match and rows_equal and structural_ok and self_structural_ok
rec("Q5_g2_production_authenticity", g2_pass,
    "measured production script SHA256 " + prod_sha[:12] + "... equals the pin AND the POST.json "
    "production_checker.script_sha256; every CONTROL_RESULTS_POST.json matrix row equals MY OWN "
    "re-execution case-by-case (actual/detail/buffer identity/expected/match-flag all equal, 8/8); "
    "static structure verified ON CODE LINES (docstring excluded via ast): NC1 guard x4 memory-ModRM "
    "branches before any length math; NC2 raise precedes the 0x84 branch's length assignment and the "
    "sibfixed memory length table is REMOVED (the NC2 correction itself); NC1 guard precedes the NC2 "
    "raise inside the 0x84 branch; NC3-B raise precedes LEA operand formatting; checker catch only "
    "(ValueError, IndexError); MY engine self-falsifiers: /3 removed (FF F7, FF D8 raise), /6 NOT "
    "added (FF F0 raises), /2 kept (FF D2 decodes call edx), LEA mod=11 raises, memory LEA decodes, "
    "memory TEST raises, register TEST decodes — all as required")

# ================================================================ Q6 (G3): clean-window boundary regression (MY decode)
my_ins = my_decode(CLEAN, WIN_VA)
my_map = {va: ins.size for va, ins in my_ins.items()}
maps_identical = (my_map == PUB_VA_SIZES and len(my_map) == 22)
total_bytes = sum(my_map.values())
head_ok = (my_ins[HEAD_VA].raw == b"\x8B\xF8" and my_ins[HEAD_VA].mn == "mov"
           and my_ins[HEAD_VA].ops == "edi, eax")
fin_ok = (my_ins[FINAL_PUSH_VA].raw == b"\x57" and my_ins[FINAL_PUSH_VA].mn == "push"
          and my_ins[FINAL_PUSH_VA].ops == "edi")
call_ok = (my_ins[JOIN_CALL_VA].raw == b"\xFF\xD2" and my_ins[JOIN_CALL_VA].mn == "call"
           and my_ins[JOIN_CALL_VA].ops == "edx")
post_meas_map = {int(k, 16): v for k, v in
                 post["clean_window_full_decode_listing"]["boundary_regression_A"]["measured_va_size_map"].items()}
post_map_identical = (my_map == post_meas_map)
calls = {va: ins.ops for va, ins in my_ins.items() if ins.mn == "call"}
arith_ok = (calls.get(0x0050A3B9) == "0x006c0f90" and calls.get(0x0050A3CF) == "0x006c10b0"
            and calls.get(0x0050A3D8) == "0x0050a1e0" and calls.get(0x0050A3E4) == "0x005246e0"
            and calls.get(0x0050A3F7) == "edx"
            and my_ins[0x0050A3C0].ops == "0x0050a3c8" and my_ins[0x0050A3C6].ops == "0x0050a3cc")
g3_pass = (maps_identical and total_bytes == 0x42 and head_ok and fin_ok and call_ok
           and post_map_identical and arith_ok)
rec("Q6_g3_clean_map_regression", g3_pass,
    f"MY independent decode of the clean window produces the SAME 22-instruction VA/size map as the "
    f"published record (identical: {maps_identical}; total 0x{total_bytes:X}): head 8B F8 mov edi,eax "
    f"@0x0050A3B7, final push 57 @0x0050A3F6, join call FF D2 edx @0x0050A3F7 all exact; map also "
    f"identical to the POST.json measured map; window arithmetic recomputed on MY decoder (call rel32 "
    f"targets 0x006C0F90/0x006C10B0/0x0050A1E0/0x005246E0, je/jmp rel8 targets 0x0050A3C8/0x0050A3CC)")

# ================================================================ Q7 (G4): nine historical SIB negative cases (SAFE re-derivation)
# SAFE METHOD: ast.parse of the READ-ONLY historical QC script + ast.literal_eval of the
# SIB_BATTERY assignment node — CONSTANT-ONLY evaluation, ZERO code execution; the
# historical top level (which writes QC_RESULTS.json) is NEVER executed/imported.
with open(HIST_QC, encoding="utf-8") as f:
    hist_src = f.read()
hist_tree = ast.parse(hist_src)                     # parse only — no execution
battery_node = None
for node in hist_tree.body:
    if (isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "SIB_BATTERY"):
        battery_node = node
        break
assert battery_node is not None, "SIB_BATTERY assignment not found in the historical QC script"
SIB_BATTERY = ast.literal_eval(battery_node.value)  # literal-only evaluation — never runs code
assert len(SIB_BATTERY) == 9 and all(len(r) == 3 for r in SIB_BATTERY)

battery_rows = []
battery_ok = True
for form_name, bhex, declared_mech in SIB_BATTERY:
    b = bytes.fromhex(bhex)
    my_raise, my_msg = _decode_raises(my_decode, b)
    prod_raise, prod_msg = _decode_raises(PROD.decode, b)
    both = my_raise and prod_raise
    battery_ok = battery_ok and both
    battery_rows.append({"form": form_name, "bytes": bhex,
                         "historical_declared_mechanism": declared_mech,
                         "my_raises": my_raise, "my_rejection": my_msg,
                         "production_raises": prod_raise, "production_rejection": prod_msg})
    print(f"    [sib] {form_name}: mine={'RAISE' if my_raise else 'NO-RAISE'} "
          f"prod={'RAISE' if prod_raise else 'NO-RAISE'}")
g4_pass = battery_ok and len(battery_rows) == 9
rec("Q7_g4_sib_9_battery", g4_pass,
    "the nine historical SIB negative cases re-derived SAFELY from the READ-ONLY historical QC script "
    "(ast.parse + ast.literal_eval of the SIB_BATTERY constant — the historical top level NEVER "
    "executed/imported) are ALL rejected fail-closed BY BOTH decoders at the DECODER level 9/9 "
    "(mine via the mem_dlen NC1 guard and the register-only non-11 fail-closed raises; production "
    "via its _reject_sib guard in every memory-ModRM branch)")

# ================================================================ Q8 (G5): 144-form Desktop sweep, both decoders
sweep_rows = []
sweep_ok = True
for opcode in (0x8B, 0x89, 0x8D, 0x84, 0x83, 0xFF):
    for mod in (0b00, 0b01, 0b10):
        for reg in range(8):
            modrm = (mod << 6) | (reg << 3) | 0b100          # always rm=4 (SIB)
            form = bytes([opcode, modrm, 0x24])               # SIB byte 0x24 (base=esp, index=none)
            if mod == 0b01:
                form += b"\x00"                               # disp8 (full bytes: a missing guard would DECODE)
            elif mod == 0b10:
                form += b"\x00\x00\x00\x00"                   # disp32 (full bytes: a missing guard would DECODE)
            if opcode == 0x83:
                form += b"\x01"                               # imm8
            my_raise, my_msg = _decode_raises(my_decode, form)
            prod_raise, prod_msg = _decode_raises(PROD.decode, form)
            both = my_raise and prod_raise
            sweep_ok = sweep_ok and both
            sweep_rows.append({"opcode": f"0x{opcode:02X}", "mod": mod, "reg": reg, "bytes": hexsp(form),
                               "my_rejected_at_decoder_level": my_raise, "my_rejection": my_msg,
                               "production_rejected_at_decoder_level": prod_raise,
                               "production_rejection": prod_msg})
assert len(sweep_rows) == 144
per_branch = {}
for opcode in (0x8B, 0x89, 0x8D, 0x84, 0x83, 0xFF):
    rows = [r for r in sweep_rows if r["opcode"] == f"0x{opcode:02X}"]
    per_branch[f"0x{opcode:02X}"] = {
        "forms": len(rows),
        "my_rejected": sum(1 for r in rows if r["my_rejected_at_decoder_level"]),
        "production_rejected": sum(1 for r in rows if r["production_rejected_at_decoder_level"]),
        "all_rejected_by_both": all(r["my_rejected_at_decoder_level"] and r["production_rejected_at_decoder_level"]
                                   for r in rows),
        "my_mechanisms": sorted({r["my_rejection"] for r in rows}),
        "production_mechanisms": sorted({r["production_rejection"] for r in rows}),
    }


def _norm_hexlist(s):
    return " ".join(f"{int(x, 16):02x}" for x in s.split())


desk_sweep_prod = [r for r in desktop_cc["sib_branch_sweep"] if r["engine"] == "production"]
desk_forms = sorted(_norm_hexlist(r["bytes"]) for r in desk_sweep_prod)
my_sweep_forms = sorted(_norm_hexlist(r["bytes"]) for r in sweep_rows)
sweep_form_set_identical_to_desktop = (my_sweep_forms == desk_forms and len(desk_forms) == 144)
post_raw_forms = post["regression_C_144_form_sweep"]["raw_forms"]
post_forms = sorted(_norm_hexlist(r["bytes"]) for r in post_raw_forms)
sweep_form_set_identical_to_post = (my_sweep_forms == post_forms and len(post_forms) == 144)
g5_pass = (sweep_ok and sweep_form_set_identical_to_desktop and sweep_form_set_identical_to_post
           and len(sweep_rows) == 144)
rec("Q8_g5_sweep_144", g5_pass,
    f"the 144-form Desktop sweep (6 opcode branches 8B/89/8D/84/83/FF x 3 memory mod 00/01/10 x 8 reg, "
    f"always rm=4) is rejected AT THE DECODER LEVEL by BOTH independent decoders 144/144 (mine "
    f"{sum(1 for r in sweep_rows if r['my_rejected_at_decoder_level'])}/144, production "
    f"{sum(1 for r in sweep_rows if r['production_rejected_at_decoder_level'])}/144); my form set is "
    f"identical to the cited Desktop production-engine sweep (144 forms) AND to the POST.json raw_forms")

# ================================================================ Q9 (G6): NC2/NC3 mechanisms + zero unexpected exceptions
PREFIX_LEN = NC23_SPAN_VA - WIN_VA        # 38 bytes: everything before the mutation span


def rejection_at_span(engine_name, decode_fn, buf):
    """Decoder-level rejection evidence: the exact exception on the full buffer, plus
    prefix proof that decode succeeds up to exactly the mutation-span VA (so the
    rejection happens AT the span, not by an accidental earlier/parse error)."""
    try:
        decode_fn(buf, WIN_VA)
        return {"decode_status": "DECODED (DEFECT)", "rejection": None, "prefix_decodes": None}
    except (ValueError, IndexError) as exc:
        try:
            decode_fn(buf[:PREFIX_LEN], WIN_VA)
            prefix_ok = True
        except Exception:
            prefix_ok = False
        return {"decode_status": "REJECTED_FAIL_CLOSED",
                "rejection": f"{type(exc).__name__}: {exc}",
                "prefix_decodes_before_span": prefix_ok,
                "rejected_at_va": f"0x{NC23_SPAN_VA:08X}" if prefix_ok else "UNKNOWN"}


mechanisms = {}
for name in ("NC1_SIB_HIDDEN_EDI_WRITE", "NC2_NON_SIB_TEST_HIDDEN_EDI",
             "NC3_INVALID_FF_FAR_CALL_REGISTER", "NC3_INVALID_LEA_REGISTER"):
    mechanisms[name] = {
        "my_engine": rejection_at_span("mine", my_decode, BUF[name]),
        "production": rejection_at_span("production", PROD.decode, BUF[name]),
        "my_checker_verdict": MATRIX[name]["independent_qc_own"]["result"],
        "production_checker_verdict": MATRIX[name]["production_reexecution"]["result"],
    }
mech_ok = all(
    mechanisms[n][e]["decode_status"] == "REJECTED_FAIL_CLOSED"
    and mechanisms[n][e]["prefix_decodes_before_span"] is True
    for n in mechanisms for e in ("my_engine", "production"))
nc23_mech_recorded = all(
    ("memory TEST" in mechanisms["NC2_NON_SIB_TEST_HIDDEN_EDI"][e]["rejection"]
     or "test memory form" in mechanisms["NC2_NON_SIB_TEST_HIDDEN_EDI"][e]["rejection"])
    and ("FF /3" in mechanisms["NC3_INVALID_FF_FAR_CALL_REGISTER"][e]["rejection"])
    and ("LEA register form" in mechanisms["NC3_INVALID_LEA_REGISTER"][e]["rejection"])
    for e in ("my_engine", "production"))
zero_unexpected = (unexpected_exceptions == 0)
no_typeerror_escape = all("TypeError" not in json.dumps(MATRIX[name]) for name in CASE_ORDER)
g6_pass = mech_ok and nc23_mech_recorded and zero_unexpected and no_typeerror_escape
rec("Q9_g6_nc23_mechanisms_zero_unexpected", g6_pass,
    "explicit decoder-level rejection mechanisms recorded for cases 5-8 on BOTH engines, each "
    "rejection pinpointed at 0x0050A3DD by prefix decode (NC2: memory TEST form rejected before any "
    "length computation; NC3-A: FF /3 register form rejected, no /6 added; NC3-B: LEA mod=11 rejected "
    "before operand formatting -> checker (False, diagnostic), never TypeError); zero unexpected "
    "exceptions in all 16 matrix rows (" + str(unexpected_exceptions) + " ERROR rows); no TypeError "
    "escaped any checker")

# ================================================================ Q10: supplementary controls (recorded, NOT gate conditions)
# (a) register-form support battery re-executed by THIS QC on the ACTUAL production module
reg_support = {}
for label, bhex, want_mn, want_ops in [
    ("mov_reg_8B_F8", "8B F8", "mov", "edi, eax"),
    ("mov_reg_8B_C0", "8B C0", "mov", "eax, eax"),
    ("mov_reg_89_C8", "89 C8", "mov", "eax, ecx"),
    ("test_reg_84_C0", "84 C0", "test", "al, al"),
    ("lea_mem_8D_06", "8D 06", "lea", "eax, dword ptr [esi + 0x0]"),
    ("call_reg_FF_D2", "FF D2", "call", "edx"),
]:
    b = bytes.fromhex(bhex)
    try:
        ins = PROD.decode(b, 0x00400000)
        got = ins[0x00400000]
        ok = got.mnemonic == want_mn and got.op_str == want_ops
        reg_support[label] = {"bytes": bhex, "decoded": True, "mnemonic": got.mnemonic,
                              "operands": got.op_str, "supported_as_before": ok}
    except (ValueError, IndexError) as exc:
        reg_support[label] = {"bytes": bhex, "decoded": False,
                              "error": f"{type(exc).__name__}: {exc}", "supported_as_before": False}
prod_negative = {}
for label, bhex, want_mech in [
    ("NC2_test_mem_84_06", "84 06", "unsupported memory TEST form"),
    ("NC2_test_mem_84_44_24_00_SIB_first", "84 44 24 00", "unsupported SIB form"),
    ("NC3B_lea_reg_8D_C0", "8D C0", "unsupported LEA register form"),
    ("NC3A_ff_3_FF_D8", "FF D8", "uncovered FF /3"),
]:
    raised, msg = _decode_raises(PROD.decode, bytes.fromhex(bhex))
    prod_negative[label] = {"bytes": bhex, "raised": raised, "rejection": msg,
                            "mechanism_as_expected": raised and want_mech in msg}
supp_reg_ok = (all(v["supported_as_before"] for v in reg_support.values())
               and all(v["mechanism_as_expected"] for v in prod_negative.values()))

# (b) PRE transcription fidelity: the executor's SOURCE_DESKTOP_MEASUREMENT must be a
#     VERBATIM transcription of the pinned Desktop CC residual_tests (deep equality)
pre = json.load(open(PRE_JSON, encoding="utf-8"))
pre_transcription = {}
for case_name, desk_name in DESKTOP_CASE_FOR.items():
    pre_copy = pre["SOURCE_DESKTOP_MEASUREMENT"]["residual_tests"][desk_name]
    desk_copy = desktop_residual[desk_name]
    pre_transcription[case_name] = {"desktop_case": desk_name,
                                    "verbatim_deep_equal": pre_copy == desk_copy}
pre_transcription_ok = all(v["verbatim_deep_equal"] for v in pre_transcription.values())

# (c) PRE internal consistency: every per-case PRE_REPRODUCED flag true and every actual
#     equal to its expectation in the persisted PRE record (read-only verification of the
#     executor's PRE claim; the historical behavior itself is the executor's measurement,
#     its mechanism statically confirmed by THIS QC's full read of both historical scripts)
pre_flags_ok = all(
    pre["EXECUTOR_REPRODUCTION"]["PRE_REPRODUCED"]["per_case"][n][k] is True
    for n in CASE_ORDER for k in ("production", "internal_qc"))
pre_actuals_ok = all(
    pre["EXECUTOR_REPRODUCTION"]["matrix_8_cases"][n]["actual"]["production"]
    == pre["EXECUTOR_REPRODUCTION"]["matrix_8_cases"][n]["expected"]["production"]
    and pre["EXECUTOR_REPRODUCTION"]["matrix_8_cases"][n]["actual"]["internal_qc"]
    == pre["EXECUTOR_REPRODUCTION"]["matrix_8_cases"][n]["expected"]["internal_qc"]
    for n in CASE_ORDER)

# (d) cited Desktop reference decode for the instruction-level diagnosis (CITED, not new
#     measurement; nothing installed) — extracted from the pinned Desktop CC file
nc2_ref = desktop_residual["NON_SIB_TEST_HIDDEN_EDI"]["reference"]
nc2_span_rows = [e for e in nc2_ref["listing"] if 0x0050A3DD <= int(e["va"], 16) <= 0x0050A3E8]
desktop_citation = {
    "citation": {
        "file": DESKTOP_CC,
        "size_bytes": size_file(DESKTOP_CC),
        "sha256": sha256_file(DESKTOP_CC),
        "label": ("SOURCE_DESKTOP_MEASUREMENT (Desktop post-audit of 91598a98) — cited reference "
                  "decode, NOT a new measurement by this QC; nothing installed"),
    },
    "NC2_NON_SIB_TEST_HIDDEN_EDI": {
        "reference_library": nc2_ref["library"], "reference_version": nc2_ref["version"],
        "reference_decoded_bytes": nc2_ref["decoded_bytes"],
        "reference_edi_writes_in_required_interval": nc2_ref["edi_writes_in_required_interval"],
        "reference_span_decode": nc2_span_rows,
        "desktop_production_verdict_on_nc2_buffer": desktop_residual["NON_SIB_TEST_HIDDEN_EDI"]["production"],
        "desktop_independent_qc_verdict_on_nc2_buffer": desktop_residual["NON_SIB_TEST_HIDDEN_EDI"]["independent_internal"],
    },
    "NC3_INVALID_FF_FAR_CALL_REGISTER": {
        "reference_library": desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["library"],
        "reference_version": desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["version"],
        "reference_decoded_bytes": desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["decoded_bytes"],
        "reference_edi_writes_in_required_interval":
            desktop_residual["INVALID_FF_FAR_CALL_REGISTER"]["reference"]["edi_writes_in_required_interval"],
        "desktop_production_exception_on_lea_case":
            desktop_residual["INVALID_LEA_REGISTER"]["production"].get("exception"),
    },
    "NC3_INVALID_LEA_REGISTER": {
        "reference_library": desktop_residual["INVALID_LEA_REGISTER"]["reference"]["library"],
        "reference_version": desktop_residual["INVALID_LEA_REGISTER"]["reference"]["version"],
        "reference_decoded_bytes": desktop_residual["INVALID_LEA_REGISTER"]["reference"]["decoded_bytes"],
        "desktop_production_exception_on_lea_case":
            desktop_residual["INVALID_LEA_REGISTER"]["production"].get("exception"),
    },
}
rec("Q10_supplementary_controls", supp_reg_ok and pre_transcription_ok and pre_flags_ok and pre_actuals_ok,
    f"supplementary (NOT gate) controls all hold: production register-form battery re-executed by THIS "
    f"QC (6/6 positives decode incl. 84 C0/8D 06/FF D2; 4/4 negative controls raise with the expected "
    f"mechanisms); PRE SOURCE_DESKTOP_MEASUREMENT is a VERBATIM transcription of the pinned Desktop "
    f"residual_tests 3/3 (deep equality); PRE per-case reproduction flags all true and actuals equal "
    f"expectations 16/16; Desktop reference decode cited for the instruction-level diagnosis "
    f"(capstone 5.0.7, cited — NC2 span: test byte ptr [esi], al 2B @0x0050A3DD then mov edi, "
    f"0xe8ccbbaa 5B @0x0050A3DF = EDI WRITE inside (0x0050A3B7, 0x0050A3F6); capstone stops at 38 "
    f"bytes for FF D8 and 8D C0: invalid register encodings)")

# ================================================================ Q11: terminal gate
gates = {
    "G1_16_row_matrix_match": {
        "pass": g1_pass,
        "rows_total": 16,
        "rows_matching": sum(1 for n in CASE_ORDER if MATRIX[n]["row_ok"]),
        "required": {n: {"own": REQUIRED_16[n][0], "production": REQUIRED_16[n][1]} for n in CASE_ORDER},
        "production_fixture_byte_identical_to_my_window": prod_fixture_identity,
    },
    "G2_production_authenticity": {
        "pass": g2_pass,
        "script_sha256_measured": prod_sha,
        "script_sha256_pin": PINS["corrected_production_nc23fixed"]["sha256"],
        "script_sha256_post_json": post["production_checker"]["script_sha256"],
        "sha256_match": sha_match,
        "post_rows_equal_to_my_reexecution_case_by_case": rows_equal,
        "per_case_row_agreement": row_agreement,
        "production_static_structure": structural,
        "my_engine_self_falsifiers": {k: {"ok": v[0], "evidence": v[1]} for k, v in self_falsifiers.items()},
    },
    "G3_clean_map_regression": {
        "pass": g3_pass,
        "my_va_size_map": {f"0x{va:08X}": sz for va, sz in sorted(my_map.items())},
        "published_va_size_map": {f"0x{va:08X}": sz for va, sz in sorted(PUB_VA_SIZES.items())},
        "maps_identical": maps_identical,
        "instruction_count": len(my_map),
        "total_bytes": total_bytes,
        "p1_head_exact": head_ok, "p3_final_push_exact": fin_ok, "p4_join_call_exact": call_ok,
        "post_json_measured_map_identical": post_map_identical,
        "window_arithmetic_recomputed_ok": arith_ok,
    },
    "G4_sib_9_case_battery_both_decoders": {
        "pass": g4_pass,
        "battery_size": len(battery_rows),
        "my_rejected": sum(1 for r in battery_rows if r["my_raises"]),
        "production_rejected": sum(1 for r in battery_rows if r["production_raises"]),
        "derivation_method": ("ast.parse + ast.literal_eval of the SIB_BATTERY constant from the READ-ONLY "
                              "historical 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py — ZERO code "
                              "execution; the historical top level (which writes QC_RESULTS.json) was "
                              "NEVER executed or imported"),
        "rows": battery_rows,
    },
    "G5_sweep_144_forms_both_decoders": {
        "pass": g5_pass,
        "forms_total": len(sweep_rows),
        "my_rejected": sum(1 for r in sweep_rows if r["my_rejected_at_decoder_level"]),
        "production_rejected": sum(1 for r in sweep_rows if r["production_rejected_at_decoder_level"]),
        "form_set_identical_to_cited_desktop_sweep": sweep_form_set_identical_to_desktop,
        "form_set_identical_to_post_json_raw_forms": sweep_form_set_identical_to_post,
        "per_branch": per_branch,
        "raw_forms": sweep_rows,
    },
    "G6_nc23_mechanisms_zero_unexpected": {
        "pass": g6_pass,
        "mechanisms_cases_5_to_8": mechanisms,
        "nc23_rejection_mechanisms_explicitly_recorded": nc23_mech_recorded,
        "unexpected_exceptions_in_16_rows": unexpected_exceptions,
        "typeerror_escape_anywhere": (not no_typeerror_escape),
    },
}
qc_pass = all(g["pass"] for g in gates.values())
verdict = "PASS" if qc_pass else "FAIL"

rec("Q11_terminal_gate", qc_pass,
    "TERMINAL GATE: G1=" + ("PASS" if gates["G1_16_row_matrix_match"]["pass"] else "FAIL")
    + " G2=" + ("PASS" if gates["G2_production_authenticity"]["pass"] else "FAIL")
    + " G3=" + ("PASS" if gates["G3_clean_map_regression"]["pass"] else "FAIL")
    + " G4=" + ("PASS" if gates["G4_sib_9_case_battery_both_decoders"]["pass"] else "FAIL")
    + " G5=" + ("PASS" if gates["G5_sweep_144_forms_both_decoders"]["pass"] else "FAIL")
    + " G6=" + ("PASS" if gates["G6_nc23_mechanisms_zero_unexpected"]["pass"] else "FAIL")
    + " => QC_VERDICT = " + verdict)

# ================================================================ persist QC_RESULTS.json
out = {
    "RUN_ID": RUN_ID,
    "RUN_CLASS": "RECORDS_AND_QC_MACHINERY_CORRECTION",
    "QC_ORIGIN": ("FRESH_INDEPENDENT_INTERNAL_QC_BY_PE_MASTER_AUDITOR (fresh-context internal QC under "
                  "direct PE-MASTER dispatch; NOT a Desktop post-audit; NOT the executor's self-review — "
                  "the executor phase was pe-reconstruction)"),
    "AUDITED_EXECUTOR": "pe-reconstruction (executor phase of the NC2+NC3 correction run)",
    "DETERMINISM": "no timestamps; all rows machine-measured in this QC run",
    "inputs": INPUTS,
    "window_rederivation": {
        "source": ("docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/01_RAW/"
                   "JOIN_WINDOW_50A3B7_REPIN.txt"),
        "method": "MY OWN regex parser over the published per-instruction record (no import of any executor buffer)",
        "instruction_count": len(pieces), "first_va": f"0x{pieces[0][0]:08X}",
        "contiguous": contig, "total_bytes": len(MY_WINDOW),
        "my_window_sha256": sha256_bytes(MY_WINDOW),
    },
    "independence_statement": {
        "my_decoder_lineage": ("corrected successor of the historical internal-QC implementation "
                               "00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py (pe-master-auditor lineage; "
                               "READ-ONLY historical source, SHA256-pinned): own mem_dlen with the fused NC1 "
                               "SIB rejection, own Insn class, own fail-closed linear decode, own P1-P4 "
                               "checker; NC2 kept (0x84 memory TEST rejected before length); NC3-A corrected "
                               "(FF /3 acceptance REMOVED, /6 NOT added, only FF /2 mod=11); NC3-B corrected "
                               "(LEA mod=11 rejected before operand formatting)"),
        "production_lineage": ("03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py (pe-reconstruction lineage; "
                               "corrected successor of ctrl4_exact_endpoint_sibfixed.py): standalone "
                               "_reject_sib helper + NC2 memory-TEST rejection + NC3-B LEA register-form "
                               "rejection; FF branch unchanged (only /2 mod=11)"),
        "no_import_of_production_in_verdict_path": True,
        "no_shared_decoder_helper_with_production": True,
        "production_executed_separately_via_importlib_for_comparison": True,
        "disclosed_shared_assumption": ("BOTH checkers implement the SAME contract-mandated P1-P4 "
                                        "exact-endpoint predicate and the SAME eight-case matrix definitions "
                                        "(frozen dispatch contract). By design: the predicate and case set are "
                                        "contract-fixed; the implementations are independent. Matrix agreement "
                                        "is a same-predicate cross-check of two independent decoders, NOT a "
                                        "universal x86-decoder correctness proof."),
    },
    "eight_case_matrix_16_rows": {
        "buffer_provenance": ("all eight buffers re-derived MY OWN way from the published record + my own "
                              "mutation builders with fail-closed asserts on the replaced original bytes; "
                              "synthetic/in-memory only; EXE never accessed"),
        "buffer_records": buffer_records,
        "desktop_residual_case_buffer_identity": desktop_buffer_identity,
        "rows": MATRIX,
    },
    "production_static_structure_and_self_falsifiers": {
        "production_structure": structural,
        "my_engine_self_falsifiers": {k: {"ok": v[0], "evidence": v[1]} for k, v in self_falsifiers.items()},
        "self_check_label": ("SELF-CHECK (honestly labeled: my verification of my own engine; PE-MASTER "
                             "audits it independently) — functional falsifiers, not text assertions"),
    },
    "supplementary_controls_not_gate_conditions": {
        "production_register_form_battery_reexecuted": {"positives": reg_support,
                                                        "negatives": prod_negative,
                                                        "result": supp_reg_ok},
        "pre_transcription_fidelity_vs_desktop_cc": {"rows": pre_transcription,
                                                     "result": pre_transcription_ok},
        "pre_internal_consistency": {"per_case_flags_all_true": pre_flags_ok,
                                     "actuals_equal_expectations_16": pre_actuals_ok},
        "desktop_reference_citation": desktop_citation,
    },
    "gates": gates,
    "verdict": {
        "QC_VERDICT": verdict,
        "gate_wording": ("QC_PASS = G1..G6 all PASS: 16/16 required matrix rows match + production "
                         "authenticity (SHA + case-by-case POST equality) + clean 22-instruction/0x42 map "
                         "regression + nine SIB controls rejected by both decoders + 144-form sweep rejected "
                         "at decoder level by both + explicit NC2/NC3 mechanisms with zero unexpected "
                         "exceptions. Any FAIL/ERROR/NOT_PERFORMED forbids QC_PASS. One targeted repair "
                         "round (NC2/NC3 only) is allowed; other material findings stay OPEN."),
        "NC2_NC3_DISPOSITION": ("CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE (only after this positive gate; "
                                "scoped to the eight-case matrix, the nine-form battery and the "
                                "144-form sweep)") if qc_pass else "NOT_ESTABLISHED_BY_THIS_QC",
        "NC1_PRESERVED": "YES (CLOSED_FOR_AUDITED_STATE for 91598a98 — unchanged historical status)",
        "NOT_CLAIMED": ("GENERAL_X86_DECODER_PROVEN (never claimed; both engines cover only the window's "
                        "opcode universe and reject everything else fail-closed)"),
    },
    "status_preservation": {
        "NC1": "CLOSED_FOR_AUDITED_STATE for 91598a98 (historical results remain authentic and unchanged)",
        "NC2_NC3": ("CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE (only after a positive gate; never "
                    "GENERAL_X86_DECODER_PROVEN)") if qc_pass else "NOT_ESTABLISHED_WITHIN_THIS_QC",
        "MINIMUM_NEW_ANALYZED_EDGE_COUNT": ">=32 (MIN preserved); EXACT = UNRESOLVED",
        "MINIMUM_NEW_FUNCTION_BODIES_OPENED": ">=7 (MIN preserved); EXACT = UNRESOLVED",
        "ORIGINAL_SCOPE_BUDGET_COMPLIANCE": "FAIL",
        "RETROACTIVE_PRIOR_AUTHORIZATION": "NO",
        "WRAPPER_DEPTH": "UNRESOLVED",
        "HISTORICAL_LINEAGE_BUDGET_CHARGE": "2/3",
        "CHILD_RESOURCE_PROVENANCE": "STRONGLY_SUPPORTED_MODEL_DERIVED",
        "MODEL_ROOT_RELATION": "UNKNOWN",
        "CHILD_VISUAL_ROLE": "UNRESOLVED",
        "CHILD_TO_JOIN_IDENTITY": "STRONGLY_SUPPORTED",
        "EXACT_PARENT": "CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (scoped to examined ACLD+0x18 SF instance)",
        "JOIN_OPERATION": "STRONGLY_SUPPORTED",
        "CAND4_CHILD_ROOT_CLOSURE": "NOT_ESTABLISHED_WITHIN_BOUND",
        "WORLD_INSTANCE": "NOT_ESTABLISHED",
        "WORLD_XYZ_RECOVERED": "NO",
        "SOURCE_DESKTOP_POST_AUDIT": "PERFORMED_FOR_91598a98",
        "NEW_CORRECTION_DESKTOP_POST_AUDIT": "NOT_PERFORMED (this fresh internal QC is NOT the future "
                                              "Desktop post-audit of the new correction SHA)",
        "CANONICAL_GATE_EFFECT": "NONE",
    },
    "coverage": {
        "FULL_READ_LOG": [
            "03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py — ALL 377 lines (corrected production; "
            "import-inertness verified: no file I/O, only a fixture-length assert at module level)",
            "03_SCRIPTS/run_nc23_matrix.py — ALL 1032 lines (executor matrix runner)",
            "CONTROL_RESULTS_POST.json — ALL 1977 lines",
            "CONTROL_RESULTS_PRE.json — ALL 1483 lines",
            "SOURCE_STATE.md — ALL 130 lines; INPUT_IDENTITIES.md — ALL 120 lines",
            "SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py — ALL 851 lines (READ-ONLY "
            "historical QC; SIB_BATTERY re-derived via ast.parse + literal_eval, top level NEVER executed)",
            "SOURCE_PACKAGE 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py — ALL 318 lines (READ-ONLY "
            "historical production; NC2 length defect and LEA TypeError path confirmed at source level)",
            "PRIOR_SCIENCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt — ALL 53 lines",
            "Desktop CONTROL_COUNTERCHECKS.json — residual_tests (3 cases) + sib_branch_sweep (288 rows) "
            "verified programmatically against the SHA-pinned file (cited reference; full-file prose "
            "sections not re-read — citation only)",
        ],
        "read_mode": "FULL_READ for every load-bearing executor artifact and historical decoder source",
    },
    "not_checked": [
        "FUN_006C9700, FUN_006C8BB0 and any new function bodies/windows (forbidden by the contract)",
        "callee bodies of the four intervening calls (EDI preservation across them rests on the MSVC "
        "callee-saved ABI — SUPPORT, NOT PROOF; unchanged historical limitation)",
        "model/root semantics, transform writers, CMO/ACLD joins, VFS/BNT/NIF, game payloads, runtime, "
        "network channel (out of scope)",
        "Desktop CONTROL_COUNTERCHECKS.json prose sections beyond residual_tests/sib_branch_sweep "
        "(cited reference only — not a new measurement source for this QC)",
        "git commit/push/manifest/AUDIT_ENTRYPOINT publication — parent (PE-MASTER) phase; this QC "
        "performed NO git operations",
    ],
    "open_findings": [],
    "qc_repair_rounds": {
        "rounds_used": 1,
        "max_allowed": 1,
        "scope": ("THIS QC's own static structural check (NC2/NC3 QC machinery) — NOT the audited "
                  "production code, which was never modified"),
        "first_run_defect": ("the first-run structural predicate was modeled on the sibfixed layout: "
                             "(a) plain substring search matched the production module DOCSTRING's "
                             "verbatim quotes of the NC2/NC3 raise statements (line 33/46 prose) "
                             "instead of the real code lines (289/247), and (b) it searched for the "
                             "sibfixed 0x84 memory length table ('size = 2 if mod == 0b11 else ...') "
                             "which the NC2 correction REMOVED BY DESIGN — so G2's structural "
                             "sub-flag was a false FAIL of MY check, not a defect of the audited "
                             "production module"),
        "repair": ("docstring excluded via its ast end_lineno; 0x84 branch anchored and scanned as "
                   "header -> _modrm -> NC1 guard -> NC2 raise -> 'size = 2' length assignment; "
                   "explicit 'memory length table removed' sub-check added; LEA operand-formatting "
                   "line anchored to its own 'mn = \"lea\"' sub-branch; the check remains falsifiable "
                   "(a re-added length computation before the raise, or a formatting before the "
                   "NC3-B raise, would still FAIL it) — no guard weakened"),
        "revalidation": ("after the repair the ENTIRE QC was re-executed from scratch: all 8 input "
                         "identities re-measured, the 16-row matrix, G2-G6 and every supplementary "
                         "control re-measured; no stale PASS was copied from the first run"),
    },
    "historical_top_level_never_executed": True,
    "historical_qc_results_json_writer_invoked": False,
    "exe_accessed": False,
    "buffers_synthetic_in_memory_only": True,
    "files_written_by_this_qc": [
        "00_CONTROL_INTERNAL_QC/qc_ind_ctrl_nc23_own.py (this script; NEW)",
        "00_CONTROL_INTERNAL_QC/QC_RESULTS.json (NEW; written by this script)",
        "QC_REPORT.md (NEW; authored in the same fresh QC session, outside this script)",
    ],
}

out_path = os.path.join(HERE, "QC_RESULTS.json")
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"\nQC_RESULTS.json -> {out_path}")
print(f"QC_VERDICT = {verdict}")
sys.exit(0 if verdict == "PASS" else 1)
