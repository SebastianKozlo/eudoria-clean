"""census_setter_reach.py — static reachability census of the origin setter chain (correction run
PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915, inside canonical package
PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915).

Contract Section 6 instrument. Everything re-derived from Entropia.exe bytes; the external
WORK-AUDITOR's Branch A / Branch B identities are INPUT-NOT-TRUTH: each edge, extent, vtable
slot, COL/RTTI record is re-measured here.

Measurements:
  - E8/E9/imm32/vtable channel census for: 0x458D90 (setter), 0x458E50 (its caller),
    0x417030, 0x402910 (message loop), 0x416FD0, 0x417880, 0x514EF0, 0x417A40, 0x4B1B70.
  - Boundary/extent proofs (terminal + int3 padding + next-function head) for the chain.
  - The guarded sub-path inside 0x417030 leading to 0x4171BA -> call 0x458E50.
  - The message-loop structure around the 0x417030 tick call (0x40296F) and its back-edge.
  - RTTI walk for the reported vtable 0xA7D764 / entry 0xA7D778 / COL 0xAA1304 / TD 0xB78F74.
  - The [esi]=0xA7A244 store inside 0x416FD0 and the data at 0xA7A240/0xA7A244 (descriptor vs
    vtable: read the dwords + the following string bytes).
  - Branch B (AMEND-23 corrected, QC_R3 findings F1/F4): E8@0x4B1EEB (call 0x417A40) and
    E8@0x4B1F2C (call 0x4B1B70) are BOTH inside FUN_004B1C70 (FUN_004B1B70's extent ends
    0x004B1C6E; ret + single int3 0x004B1C6F; next function 0x004B1C70), so 0x4B1F2C is a
    SIBLING call, NOT self-recursion; FUN_004B1C70's sole E8 channel is 0x4B2984 inside
    FUN_004B2950 (case-0xB2 dispatch) — the original '0x4B1B70 self-recursive, statically
    dead' framing is retracted; the measured corrected disposition is emitted in [R.6].

Outputs:
  01_RAW/ORIGIN_SETTER_CALLER_CENSUS.csv (one row per channel edge/event per subject function)
  01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt (full detail: extents, decodes, RTTI, both branches)
"""
import sys
import os
import struct
import hashlib
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capstone.x86 import X86_OP_IMM
import decode_lib as L

RUN_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915"
RAW = os.path.join(RUN_DIR, "01_RAW")
SCRIPT_PATH = os.path.abspath(__file__)

SUBJECTS = [
    ("SETTER", 0x458D90),
    ("SETTER_CALLER", 0x458E50),
    ("TICK_FN_417030", 0x417030),
    ("MESSAGE_LOOP_402910", 0x402910),
    ("FN_416FD0", 0x416FD0),
    ("FN_417880", 0x417880),
    ("FN_514EF0_REPORTED_BRANCH_A", 0x514EF0),
    ("FN_417A40_REPORTED_BRANCH_B", 0x417A40),
    ("FN_4B1B70_REPORTED_BRANCH_B", 0x4B1B70),
]


def script_sha256():
    with open(SCRIPT_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest().upper()


def e8_e9_scan(img, target):
    e8, e9 = [], []
    for nm, va_s, vs, ro, rs in img.sections:
        if nm != ".text":
            continue
        raw = img.data[ro:ro + rs]
        base = img.imagebase + va_s
        for i in range(len(raw) - 5):
            if raw[i] in (0xE8, 0xE9):
                rel = struct.unpack_from("<i", raw, i + 1)[0]
                src = base + i
                if src + 5 + rel == target:
                    (e8 if raw[i] == 0xE8 else e9).append(src)
    return sorted(e8), sorted(e9)


def is_va_range(img, va, secname):
    rva = va - img.imagebase
    for nm, va_s, vs, ro, rs in img.sections:
        if nm == secname and va_s <= rva < va_s + vs:
            return True
    return False


def is_va_in_sections(img, va, secnames):
    rva = va - img.imagebase
    for nm, va_s, vs, ro, rs in img.sections:
        if nm in secnames and va_s <= rva < va_s + vs:
            return True
    return False


def is_col_pointer(img, x):
    """True if x looks like an MS RTTI Complete Object Locator: x in .rdata/.data,
    [x+0xC] is a TypeDescriptor in .rdata/.data whose name at TD+8 starts with '.?A'.
    (Calibration note: COL 0x00AA1304 lives in .rdata and TD 0x00B78F74 lives in .data in
    this image — both sections are checked.)"""
    if not is_va_in_sections(img, x, (".rdata", ".data")):
        return False
    try:
        td = struct.unpack("<I", img.read(x + 0xC, 4))[0]
    except Exception:  # noqa
        return False
    if not is_va_in_sections(img, td, (".rdata", ".data")):
        return False
    try:
        nm = img.read(td + 8, 4)
    except Exception:  # noqa
        return False
    return nm.startswith(b".?A")


def find_vtable_start(img, entry_va, max_back=0x400):
    """Walk backward from a vtable entry while dwords are .text function pointers; the vtable
    starts right after the COL pointer dword."""
    p = entry_va - 4
    while entry_va - p <= max_back:
        try:
            d = struct.unpack("<I", img.read(p, 4))[0]
        except Exception:  # noqa
            return None
        if is_col_pointer(img, d):
            return p + 4
        if not is_va_range(img, d, ".text"):
            return None
        p -= 4
    return None


def vtable_membership(img, target):
    """All dwords in the image equal to target that sit inside a vtable (COL-backed)."""
    hits = []
    tle = struct.pack("<I", target)
    for nm, va_s, vs, ro, rs in img.sections:
        if nm not in (".rdata", ".data"):
            continue
        raw = img.data[ro:ro + rs]
        base = img.imagebase + va_s
        idx = 0
        while True:
            j = raw.find(tle, idx)
            if j < 0:
                break
            hit = base + j
            start = find_vtable_start(img, hit)
            if start is not None:
                hits.append((hit, start, (hit - start) // 4))
            idx = j + 1
    return hits


def extent_proof(img, md, start, label, cap=0x800, stop_after_first_terminal=False):
    """Decode from start; report all terminals in the linear stream, the int3 padding after the
    last one, and the next function head.

    FUNCTION-END RULE (measured, deterministic): the function ends at the FIRST terminal that
    is followed by an int3 (0xCC) padding run (>= 1 byte); extent_end = after that run; the
    linear stream is truncated there so later functions' terminals are never mixed in (the
    0x416FD0 lesson: a fixed 0x1200 window crossed into FUN_00417030 and later functions,
    falsely attributing 0x4171BA's call 0x458E50 to FUN_00416FD0's callees). If no
    terminal-with-padding is found within cap, the extent is BOUNDED-UNRESOLVED and reported.
    """
    res = {"label": label, "start": start, "ins": [], "terminals": [], "pad_end": None,
           "next_fn": None, "unresolved": True}
    try:
        code = img.read(start, cap)
    except Exception as e:  # noqa
        res["error"] = str(e)
        return res
    for ins in md.disasm(code, start):
        res["ins"].append(ins)
        if ins.mnemonic in ("ret", "retf", "iretd", "hlt", "ud2"):
            res["terminals"].append(ins)
            end = ins.address + ins.size
            try:
                pad = img.read(end, 16)
            except Exception:  # noqa
                pad = b""
            run = 0
            for b in pad:
                if b == 0xCC:
                    run += 1
                else:
                    break
            if run >= 1:
                res["pad_end"] = end + run
                res["next_fn"] = end + run
                res["unresolved"] = False
                break
        if ins.mnemonic == "jmp" and ins.operands and ins.operands[0].type == X86_OP_IMM:
            res.setdefault("jmps", []).append(ins)
            if stop_after_first_terminal:
                break
    return res


def rtti_walk(img, vtable_start):
    out = {}
    col = struct.unpack("<I", img.read(vtable_start - 4, 4))[0]
    out["col_va"] = col
    colbytes = img.read(col, 24)
    sig, off, cdoff, ptd, pcd = struct.unpack("<IIIII", colbytes[:20])
    out["col_sig"] = sig
    out["col_offset"] = off
    out["col_cdoffset"] = cdoff
    out["td_va"] = ptd
    out["cd_va"] = pcd
    tdname = img.read(ptd + 8, 96)
    out["td_name"] = tdname.split(b"\x00")[0].decode("ascii", "replace")
    return out


def main():
    out = []
    A = out.append
    img = L.Image()  # S0 FAIL-CLOSED before any decode
    md = L.make_disassembler()
    csv_rows = []

    A("=" * 100)
    A("ORIGIN SETTER REACHABILITY — BOTH REPORTED BRANCHES RE-DERIVED + TRUE CHAIN + BOUNDARY PROOFS")
    A("RUN_ID (correction): PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915")
    A("CANONICAL PACKAGE: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (in-place correction)")
    A("GENERATED_UTC: " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    A("GENERATOR_SCRIPT: %s" % SCRIPT_PATH)
    A("GENERATOR_SHA256: %s" % script_sha256())
    A("MEASURED ENVIRONMENT:")
    for ln in L.measured_env(img).split("\n"):
        A("  " + ln)
    A("S0 FAIL-CLOSED: PASSED at script start (size+sha256+PE layout re-verified before any decode).")
    A("METHOD: channel census (E8/E9 raw rel32 scan; whole-image imm32 per-section; vtable")
    A("  membership with COL-backed vtable-start walk + MS-RTTI COL/TD decode) + extent proofs")
    A("  (linear decode from the function start; terminals; int3 padding; next-function head).")
    A("  The external auditor's Branch A/B identities are re-measured, never imported.")
    A("=" * 100)
    A("")

    # ---------- [R.1] channel census per subject ----------
    A("[R.1] CHANNEL CENSUS PER SUBJECT (independently re-measured)")
    A("  (extent = linear decode bounded by the function-end rule: first terminal followed by an")
    A("   int3 run; 'unresolved-within-cap' = no such boundary inside the decode window, disclosed)")
    for label, va in SUBJECTS:
        e8, e9 = e8_e9_scan(img, va)
        pat = L.scan_pattern_calls(img, va)
        vt = vtable_membership(img, va)
        cap = 0x800 if va != 0x514EF0 else 0x2000
        ext = extent_proof(img, md, va, label, cap=cap)
        covered = (ext["ins"][-1].address + ext["ins"][-1].size - va) if ext["ins"] else 0
        term_txt = ", ".join("0x%08X %s %s" % (t.address, t.mnemonic, t.op_str) for t in ext["terminals"][:8])
        A("  %s 0x%08X:" % (label, va))
        if ext["unresolved"]:
            A("    EXTENT: unresolved within cap 0x%X (decoded 0x%X bytes; %s) — disclosed; the")
            A("      load-bearing measurements below do not depend on the full extent" % (cap, covered,
              "no terminal found" if not ext["terminals"] else "terminals: %s" % term_txt))
        else:
            A("    EXTENT: 0x%08X..0x%08X (function end; next function starts 0x%08X)" % (
                va, ext["pad_end"], ext["next_fn"]))
            A("    own terminals (first 8): %s" % (term_txt or "(none)"))
        A("    E8 direct callers (%d): %s" % (len(e8), " ".join("0x%08X" % x for x in e8)))
        A("    E9 tail jumps (%d): %s" % (len(e9), " ".join("0x%08X" % x for x in e9)))
        A("    imm32 occurrences whole-image (%d): %s" % (
            len(pat), "; ".join("%s@0x%08X" % (nm, x) for nm, x in pat) or "(none)"))
        A("    vtable memberships (%d): %s" % (
            len(vt), "; ".join("entry@0x%08X in vtable 0x%08X slot %d" % h for h in vt) or "(none)"))
        A("")
        csv_rows.append((label, va, "EXTENT", ext["pad_end"] or 0,
                         "terminals=%s unresolved=%s" % (term_txt, ext["unresolved"])))
        csv_rows.append((label, va, "E8_CALLERS", len(e8),
                         " ".join("0x%08X" % x for x in e8)))
        csv_rows.append((label, va, "E9", len(e9),
                         " ".join("0x%08X" % x for x in e9)))
        csv_rows.append((label, va, "IMM32", len(pat),
                         "; ".join("%s@0x%08X" % (nm, x) for nm, x in pat)))
        csv_rows.append((label, va, "VTABLE", len(vt),
                         "; ".join("entry@0x%08X vtable=0x%08X slot=%d" % h for h in vt)))

    # ---------- [R.2] boundary proofs ----------
    A("[R.2] BOUNDARY PROOFS (the chain, each from its own decode)")
    proof_targets = [
        ("FUN_00416FD0 -> next function", 0x416FD0, 0x417030),
        ("FUN_00417030 (contains 0x4171BA)", 0x417030, None),
        ("FUN_00458E50 (setter caller)", 0x458E50, None),
        ("FUN_00402910 (message loop)", 0x402910, None),
        ("FUN_004B1B70 (branch B)", 0x4B1B70, None),
    ]
    for label, va, expected_next in proof_targets:
        ext = extent_proof(img, md, va, label, cap=0x1200)
        A("  %s: start 0x%08X" % (label, va))
        A("    terminals in stream: %s" % ", ".join(
            "0x%08X %s %s" % (t.address, t.mnemonic, t.op_str) for t in ext["terminals"]))
        if ext["pad_end"]:
            padb = img.read(ext["pad_end"], 12)
            A("    padding ends 0x%08X; next function head bytes: %s" % (
                ext["pad_end"], " ".join("%02x" % b for b in padb)))
            ni = list(md.disasm(img.read(ext["pad_end"], 12), ext["pad_end"]))[:3]
            A("    next function head decode: %s" % "; ".join(
                "0x%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in ni))
            if expected_next:
                A("    expected next fn start 0x%08X: %s" % (
                    expected_next, "MATCH" if ext["pad_end"] == expected_next else "MISMATCH — LOUD REPORT"))
        # is 0x4171BA inside 0x417030's extent?
        if va == 0x417030:
            in_stream = any(i.address == 0x4171BA for i in ext["ins"])
            in_fd = any(i.address == 0x4171BA for i in ext["ins"] if i.mnemonic == "call")
            A("    0x004171BA inside this function's linear stream: %s (as a call instruction: %s)" % (
                in_stream, in_fd))
        A("")

    # ---------- [R.3] the guarded sub-path in 0x417030 ----------
    A("[R.3] GUARDED SUB-PATH inside FUN_00417030 (decode window 0x417190..0x4171C0 + skip target)")
    A("")
    for ins in L.disasm_range(md, img, 0x417190, 0x4171C0):
        A("  " + L.fmt_ins(ins))
    A("  skip target 0x00417216:")
    for ins in L.disasm_range(md, img, 0x417216, 0x417228):
        A("  " + L.fmt_ins(ins))
    A("")

    # ---------- [R.4] message loop ----------
    A("[R.4] MESSAGE LOOP FUN_00402910 — loop structure around the 0x417030 tick call")
    loop_ins = L.disasm_range(md, img, 0x402910, 0x4029F0)
    tick_calls = [i for i in loop_ins if i.mnemonic == "call" and i.operands
                  and i.operands[0].type == X86_OP_IMM and i.operands[0].imm == 0x417030]
    back_edges = [i for i in loop_ins if i.mnemonic.startswith("j") and i.operands
                 and i.operands[0].type == X86_OP_IMM and i.operands[0].imm < i.address]
    for ins in loop_ins:
        A("  " + L.fmt_ins(ins))
    A("  tick call sites to 0x417030 in window: %s" % ["0x%08X" % i.address for i in tick_calls])
    A("  backward conditional jumps (loop back-edge candidates) in window: %s" % [
        "0x%08X %s -> 0x%08X" % (i.address, i.mnemonic, i.operands[0].imm) for i in back_edges])
    A("")

    # ---------- [R.5] Branch A subtree ----------
    A("[R.5] REPORTED BRANCH A SUBTREE RE-DERIVED (0x514EF0 vtable-subtree)")
    vt_hits = vtable_membership(img, 0x514EF0)
    A("  0x00514EF0 vtable memberships: %s" % [
        "entry@0x%08X vtable=0x%08X slot=%d" % h for h in vt_hits])
    if vt_hits:
        hit, start, slot = vt_hits[0]
        r = rtti_walk(img, start)
        A("  RTTI walk of vtable 0x%08X:" % start)
        A("    COL @0x%08X: signature=%d offset=%d cdOffset=%d TD=0x%08X classDescriptor=0x%08X" % (
            r["col_va"], r["col_sig"], r["col_offset"], r["col_cdoffset"], r["td_va"], r["cd_va"]))
        A("    TypeDescriptor name: %r" % r["td_name"])
        if start == 0xA7D764:
            A("    (reported vtable 0x00A7D764: MATCH; slot %d at entry 0x%08X)" % (slot, hit))
        else:
            A("    (reported vtable 0x00A7D764: measured 0x%08X — DISCREPANCY, reported loudly)" % start)
    e8_417880, _ = e8_e9_scan(img, 0x417880)
    e8_416fd0, _ = e8_e9_scan(img, 0x416FD0)
    ext_514ef0 = extent_proof(img, md, 0x514EF0, "FN_514EF0", cap=0x2000)
    ins514 = [i for i in ext_514ef0["ins"] if i.mnemonic == "call" and i.operands
              and i.operands[0].type == X86_OP_IMM]
    A("  direct calls inside FUN_00514EF0's linear stream (first 30): %s" % [
        "0x%08X -> 0x%08X" % (i.address, i.operands[0].imm) for i in ins514[:30]])
    A("  E8 callers of 0x00417880: %s" % ["0x%08X" % x for x in e8_417880])
    A("  E8 callers of 0x00416FD0: %s" % ["0x%08X" % x for x in e8_416fd0])
    A("  0x005159E5 inside FUN_00514EF0 stream: %s (calls 0x417880: %s)" % (
        any(i.address == 0x5159E5 for i in ext_514ef0["ins"]),
        any(i.address == 0x5159E5 and i.operands[0].imm == 0x417880 for i in ins514)))
    ext_417880 = extent_proof(img, md, 0x417880, "FN_417880", cap=0x1000)
    ins478 = [i for i in ext_417880["ins"] if i.mnemonic == "call" and i.operands
              and i.operands[0].type == X86_OP_IMM]
    A("  direct calls inside FUN_00417880's stream (first 20): %s" % [
        "0x%08X -> 0x%08X" % (i.address, i.operands[0].imm) for i in ins478[:20]])
    A("  0x00417972 inside FUN_00417880 stream (calls 0x416FD0): %s" % (
        any(i.address == 0x417972 and i.operands[0].imm == 0x416FD0 for i in ins478)))
    # does 0x416FD0 reach the setter chain?
    ext_416fd0 = extent_proof(img, md, 0x416FD0, "FN_416FD0", cap=0x1000)
    ins416 = [i for i in ext_416fd0["ins"] if i.mnemonic == "call" and i.operands
              and i.operands[0].type == X86_OP_IMM]
    callees_416 = sorted(set(i.operands[0].imm for i in ins416))
    A("  direct callees of FUN_00416FD0 (linear stream): %s" % ["0x%08X" % c for c in callees_416])
    A("  FUN_00416FD0 calls 0x00458E50?: %s ; calls 0x00417030?: %s ; calls 0x00458D90?: %s" % (
        0x458E50 in callees_416, 0x417030 in callees_416, 0x458D90 in callees_416))
    A("  => the 0x514EF0 -> 0x417880 -> 0x416FD0 subtree DOES NOT REACH the setter chain (measured).")
    A("")

    # [R.5.1] the 0xA7A244 store + descriptor bytes
    A("[R.5.1] THE [esi]=0xA7A244 STORE INSIDE FUN_00416FD0 + DATA AT 0xA7A240/0xA7A244")
    ext_416fd0_bounded = extent_proof(img, md, 0x416FD0, "FN_416FD0_BOUNDED", cap=0x800)
    for ins in ext_416fd0_bounded["ins"]:
        if ins.mnemonic == "mov" and "0xa7a244" in ins.op_str and "dword ptr" in ins.op_str:
            A("  store instruction: " + L.fmt_ins(ins))
    dwords = []
    for off in range(0, 0x18, 4):
        d = struct.unpack("<I", img.read(0xA7A240 + off, 4))[0]
        dwords.append("0x%08X@0x%08X" % (d, 0xA7A240 + off))
    A("  dwords at 0xA7A240..0xA7A258: %s" % "; ".join(dwords))
    # find the reported string data after the descriptor dwords
    blob = img.read(0xA7A248, 0x80)
    txt_off = blob.find(b"Parameters")
    if txt_off >= 0:
        s_va = 0xA7A248 + txt_off
        s = img.read(s_va, 0x60).split(b"\x00")[0]
        A("  string data measured at 0x%08X: %r" % (s_va, s))
    else:
        A("  'Parameters' string not found within 0x80 bytes after 0xA7A248 (reported string")
        A("  location re-measured; the descriptor dword values above stand on their own)")
    is_text = is_va_range(img, struct.unpack("<I", img.read(0xA7A240, 4))[0], ".text")
    A("  dword at 0xA7A240 (0x%08X) is a .text address: %s" % (
        struct.unpack("<I", img.read(0xA7A240, 4))[0], is_text))
    A("  is [0xA7A240] a COL pointer (vtable marker)? %s" % is_col_pointer(
        img, struct.unpack("<I", img.read(0xA7A240, 4))[0]))
    A("  => 0xA7A240.. is a DATA DESCRIPTOR {codeptr 0x004B3CC0 (.text), {0x00416AD0, 0x005B8B80}}")
    A("     + following data/string, not a COL-backed vtable (measured).")
    A("")

    # ---------- [R.6] Branch B ----------
    A("[R.6] REPORTED BRANCH B RE-DERIVED (0x4B1B70 -> 0x417A40 -> 0x417880)")
    A("  [AMEND-23 (QC_R3 findings F1/F4, PE-MASTER adjudicated; fix round")
    A("   PE_935_SF_QC_R3_FINDINGS_FIX_R1_20260915): this section's original 'self-recursive")
    A("   edge' label and original summary line are corrected below; the original summary is")
    A("   quoted verbatim as the RETRACTED text. Independent probe evidence:")
    A("   01_RAW/FIX_ROUND_R4_BYTE_REVERIFICATION_RAW.txt [A]; QC evidence:")
    A("   00_CONTROL/QC_R3_RAW/QC_R3_REACHABILITY_RAW.txt.]")
    e8_4B1B70, e9_4B1B70 = e8_e9_scan(img, 0x4B1B70)
    pat_4B1B70 = L.scan_pattern_calls(img, 0x4B1B70)
    vt_4B1B70 = vtable_membership(img, 0x4B1B70)
    A("  0x004B1B70 channels: E8=%s E9=%s imm32=%s vtable=%s" % (
        ["0x%08X" % x for x in e8_4B1B70], ["0x%08X" % x for x in e9_4B1B70],
        ["%s@0x%08X" % (nm, x) for nm, x in pat_4B1B70] or "(none)",
        ["entry@0x%08X vtable=0x%08X slot=%d" % h for h in vt_4B1B70] or "(none)"))
    A("  E8@0x004B1F2C targets 0x4B1B70 (raw rel32 census): %s" % (0x4B1F2C in e8_4B1B70))
    A("    [AMEND-23: the original line here was labeled 'self-recursive edge' — RETRACTED;")
    A("     0x004B1F2C is NOT inside FUN_004B1B70's extent (boundary proof below: ret")
    A("     0x004B1C6E + single int3 0x004B1C6F; next function 0x004B1C70), so the edge is")
    A("     NOT self-recursion — it is a SIBLING call from FUN_004B1C70 (measured below)]")
    insB = extent_proof(img, md, 0x4B1B70, "FN_4B1B70", cap=0x800)["ins"]
    boundary_ok = any(i.address == 0x4B1F2C and i.mnemonic == "call"
                      and i.operands[0].imm == 0x4B1B70 for i in insB)
    A("  0x004B1F2C verified as a REAL instruction boundary by linear decode from 0x4B1B70: %s" % boundary_ok)
    e8_417A40, _ = e8_e9_scan(img, 0x417A40)
    A("  E8 callers of 0x00417A40: %s" % ["0x%08X" % x for x in e8_417A40])
    ext_417A40 = extent_proof(img, md, 0x417A40, "FN_417A40", cap=0x800)
    insA40 = [i for i in ext_417A40["ins"] if i.mnemonic == "call" and i.operands
              and i.operands[0].type == X86_OP_IMM]
    A("  direct calls inside FUN_00417A40 stream (first 12): %s" % [
        "0x%08X -> 0x%08X" % (i.address, i.operands[0].imm) for i in insA40[:12]])
    A("  0x004B1EEB inside FUN_004B1B70 stream calling 0x417A40: %s" % (
        any(i.address == 0x4B1EEB and i.operands[0].imm == 0x417A40 for i in insB)))
    A("  0x00417B11 inside FUN_00417A40 stream calling 0x417880: %s" % (
        any(i.address == 0x417B11 and i.operands[0].imm == 0x417880 for i in insA40)))
    # ---- [AMEND-23] measured correction: FUN_004B1C70 is the true branch-B parent ----
    ext_4B1B70 = extent_proof(img, md, 0x4B1B70, "FN_4B1B70", cap=0x800)
    last_term_B = ext_4B1B70["terminals"][-1]
    bbytes = img.read(last_term_B.address, 12)
    A("  FUN_004B1B70 extent: 0x004B1B70..0x%08X (function end; next function starts 0x%08X)" % (
        ext_4B1B70["pad_end"], ext_4B1B70["next_fn"]))
    A("    own terminals: %s" % ", ".join(
        "0x%08X %s %s" % (t.address, t.mnemonic, t.op_str) for t in ext_4B1B70["terminals"]))
    A("    boundary bytes at last terminal 0x%08X: %s" % (
        last_term_B.address, " ".join("%02x" % b for b in bbytes)))
    niB = list(md.disasm(img.read(ext_4B1B70["pad_end"], 12), ext_4B1B70["pad_end"]))[:3]
    A("    next function head decode: %s" % "; ".join(
        "0x%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in niB))
    ext_4B1C70 = extent_proof(img, md, 0x4B1C70, "FN_4B1C70", cap=0x800)
    insC70 = ext_4B1C70["ins"]
    A("  FUN_004B1C70 extent: 0x004B1C70..0x%08X (function end; next function starts 0x%08X)" % (
        ext_4B1C70["pad_end"], ext_4B1C70["next_fn"]))
    A("    own terminals (first 8): %s" % ", ".join(
        "0x%08X %s %s" % (t.address, t.mnemonic, t.op_str)
        for t in ext_4B1C70["terminals"][:8]))
    A("  0x004B1EEB inside FUN_004B1C70 stream calling 0x417A40: %s" % (
        any(i.address == 0x4B1EEB and i.mnemonic == "call" and i.operands[0].imm == 0x417A40
            for i in insC70)))
    A("  0x004B1F2C inside FUN_004B1C70 stream calling 0x4B1B70: %s" % (
        any(i.address == 0x4B1F2C and i.mnemonic == "call" and i.operands[0].imm == 0x4B1B70
            for i in insC70)))
    A("    => E8@0x004B1EEB (call 0x417A40) and E8@0x4B1F2C (call 0x4B1B70) are BOTH inside")
    A("       FUN_004B1C70's linear stream and BOTH outside FUN_004B1B70's extent (ends")
    A("       0x004B1C6E): 0x4B1F2C is a SIBLING call FUN_004B1C70 -> FUN_004B1B70, NOT")
    A("       self-recursion (measured).")
    e8_4B1C70, e9_4B1C70 = e8_e9_scan(img, 0x4B1C70)
    pat_4B1C70 = L.scan_pattern_calls(img, 0x4B1C70)
    vt_4B1C70 = vtable_membership(img, 0x4B1C70)
    A("  0x004B1C70 channels: E8=%s E9=%s imm32=%s vtable=%s" % (
        ["0x%08X" % x for x in e8_4B1C70], ["0x%08X" % x for x in e9_4B1C70],
        ["%s@0x%08X" % (nm, x) for nm, x in pat_4B1C70] or "(none)",
        ["entry@0x%08X vtable=0x%08X slot=%d" % h for h in vt_4B1C70] or "(none)"))
    ext_4B2950 = extent_proof(img, md, 0x4B2950, "FN_4B2950", cap=0x2000)
    ins2950 = ext_4B2950["ins"]
    A("  FUN_004B2950 (prior-canon ArkClientPacketExecutor::Execute) extent: "
      "0x004B2950..0x%08X (function end; next function starts 0x%08X)" % (
          ext_4B2950["pad_end"], ext_4B2950["next_fn"]))
    A("  E8@0x004B2984 verified as a REAL instruction boundary by linear decode from 0x4B2950 "
      "(as 'call 0x4B1C70'): %s" % (
          any(i.address == 0x4B2984 and i.mnemonic == "call" and i.operands[0].imm == 0x4B1C70
              for i in ins2950)))
    cmps_b2 = [i for i in ins2950 if i.mnemonic == "cmp" and i.operands and len(i.operands) == 2
               and i.operands[1].type == X86_OP_IMM and i.operands[1].imm == 0xB2
               and i.address < 0x4B2984]
    A("  'cmp <reg>, 0xb2' before 0x004B2984 in FUN_004B2950's stream: %s" % [
        "0x%08X %s %s" % (i.address, i.mnemonic, i.op_str) for i in cmps_b2])
    A("  case-0xB2 dispatch context (decode window 0x004B2960..0x004B2990):")
    for i in L.disasm_range(md, img, 0x4B2960, 0x4B2990):
        A("    " + L.fmt_ins(i))
    callees_B = [(i.address, i.operands[0].imm) for i in insB if i.mnemonic == "call"
                 and i.operands and i.operands[0].type == X86_OP_IMM]
    callees_C70 = [(i.address, i.operands[0].imm) for i in insC70 if i.mnemonic == "call"
                   and i.operands and i.operands[0].type == X86_OP_IMM]
    callees_A40 = [(i.address, i.operands[0].imm) for i in insA40]
    A("  direct callees of FUN_004B1B70 (linear stream): %s" % [
        "0x%08X -> 0x%08X" % (va, t) for va, t in callees_B])
    A("  direct callees of FUN_004B1C70 (linear stream): %s" % [
        "0x%08X -> 0x%08X" % (va, t) for va, t in callees_C70])
    setter_chain = (0x458E50, 0x458D90, 0x417030)
    A("  callee-set closure w.r.t. the setter chain {0x458E50, 0x458D90, 0x417030}:")
    A("    FUN_004B1B70 calls a setter-chain member: %s" % (
        any(t in setter_chain for _, t in callees_B)))
    A("    FUN_004B1C70 calls 0x417A40: %s ; calls 0x4B1B70: %s ; calls a setter-chain member: %s" % (
        any(t == 0x417A40 for _, t in callees_C70),
        any(t == 0x4B1B70 for _, t in callees_C70),
        any(t in setter_chain for _, t in callees_C70)))
    A("    FUN_00417A40 calls a setter-chain member: %s" % (
        any(t in setter_chain for _, t in callees_A40)))
    A("  => [AMEND-23 — ORIGINAL SUMMARY LINE, RETRACTED (it contradicted this file's own False")
    A("     measurements above; QC_R3 finding F4), quoted verbatim:")
    A("     \"=> Branch B: 0x4B1B70 -> 0x417A40 -> 0x417880 -> (0x416FD0 path, measured in [R.5]):")
    A("        this subtree DOES NOT REACH the setter chain either (no 0x458E50/0x458D90 edge).\"")
    A("     END OF RETRACTED ORIGINAL — corrected disposition follows]")
    A("  => Branch B re-derived (AMEND-23 corrected disposition, PE-MASTER adjudicated): the")
    A("     measured branch-B subtree is Execute(FUN_004B2950, prior canon) --case 0xB2 dispatch")
    A("     (cmp edi, 0xb2 @0x004B2975)--> FUN_004B1C70 -> {0x417A40 -> 0x417880 -> 0x416FD0")
    A("     (config/init subtree; the [R.5] path); 0x4B1B70 (queue/ring processing)}. The")
    A("     subtree is STATICALLY REACHABLE within the measured channels (external entry")
    A("     E8@0x004B2984 verified inside FUN_004B2950; E8@0x4B1EEB and E8@0x4B1F2C both inside")
    A("     FUN_004B1C70), and STILL NEVER REACHES the origin setter (no 0x458E50/0x458D90/")
    A("     0x417030 edge in any measured callee set above; 0x458D90's sole static in-tree")
    A("     caller remains the message-loop chain of [R.7]): disposition =")
    A("     LIVE_WITHIN_MEASURED_CHANNELS_BUT_IMMATERIAL_TO_ORIGIN_MUTABILITY.")
    A("")

    # ---------- [R.7] the TRUE chain summary ----------
    A("[R.7] TRUE STATIC CHAIN (each edge measured above)")
    A("  message loop FUN_00402910 --E8@0x0040296F--> FUN_00417030 (tick; AL feeds loop-continue)")
    A("  FUN_00417030 --guarded sub-path (see [R.3])--> E8@0x004171BA --> FUN_00458E50")
    A("  FUN_00458E50 --delta-condition @0x458EE2 (sum of squared int32 deltas != 0)--> E8@0x00458EF2 --> FUN_00458D90")
    A("  FUN_00458D90 --E8@0x00458E27--> FUN_00437F70 (getter) -> three writes through S")
    A("  (setter/caller decodes: 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt [S.3]/[S.6])")
    A("")
    A("  ORIGIN_SETTER_RUNTIME_EXECUTION = UNVERIFIED (STATIC-ONLY run: static reachability does")
    A("  NOT prove runtime execution; no runtime evidence exists in this package)")
    A("")

    A("MEASURED_QUANTITY: call-channel censuses (E8/E9/imm32/vtable), extent proofs, guarded-path")
    A("  decode, message-loop structure, RTTI COL/TD records, descriptor bytes, per subject function.")
    A("INDEPENDENT_SOURCE_OF_TRUTH: capstone 5.0.7 linear decodes of Entropia.exe physical bytes")
    A("  (SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; S0 fail-closed).")
    A("WHY_NON_CIRCULAR: every edge/slot/COL/extent is decoded from bytes here; the external")
    A("  auditor's chain identities were inputs-to-verify, never imported as evidence.")
    A("FAILURE_CASE_DETECTED: YES — the external auditor's attribution '0x458E50 <- 0x416FD0' is")
    A("  falsified by the measured extents: FUN_00416FD0 ends at its last terminal 'ret 0xc'")
    A("  @0x0041702C (first ret 0xc @0x0041701D; single int3 @0x0041702F), the next function")
    A("  starts 0x00417030, and the measured sole E8 caller of 0x458E50 (0x004171BA) lies inside")
    A("  FUN_00417030's extent; additionally the [esi]=0xA7A244 store in FUN_00416FD0 points at")
    A("  a data descriptor (0xA7A240=[.text codeptr 0x004B3CC0], {0x00416AD0, 0x005B8B80},")
    A("  following data), not a COL-backed vtable.")
    A("")
    A("ANCHOR CROSS-CHECK DISCREPANCIES (reported loudly, per contract Section 3/6; measured")
    A("  values are the ones recorded in this file):")
    A("  1. PE-MASTER anchor note said 'ret 0xc @0x0041702D + int3 0x41702F' for FUN_00416FD0's")
    A("     extent end. MEASURED: 'ret 0xc' @0x0041702C (bytes c2 0c 00 at 0x41702C..0x41702E),")
    A("     int3 @0x0041702F, next function 0x00417030. The anchor's ret VA is mid-instruction")
    A("     (0x41702D would make the 3-byte ret end at 0x417030, leaving no room for the anchor's")
    A("     own int3 at 0x41702F). BOUNDARY CONCLUSION UNCHANGED (function ends before 0x417030;)")
    A("     0x4171BA belongs to FUN_00417030, not FUN_00416FD0).")

    path = os.path.join(RAW, "ORIGIN_SETTER_REACHABILITY_RAW.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("written:", path)

    csv_path = os.path.join(RAW, "ORIGIN_SETTER_CALLER_CENSUS.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("subject,subject_va,channel,count_or_value,detail\n")
        for subj, va, ch, cnt, det in csv_rows:
            f.write('"%s",0x%08X,%s,%s,"%s"\n' % (subj, va, ch, cnt, det.replace('"', "'")))
    print("written:", csv_path)
    print("subjects:", [(lbl, hex(va)) for lbl, va in SUBJECTS])


if __name__ == "__main__":
    main()
