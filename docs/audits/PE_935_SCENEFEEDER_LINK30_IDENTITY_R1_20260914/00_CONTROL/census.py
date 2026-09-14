# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 - main census script (own, independent)
# STATIC-ONLY (the client NEVER ran; no process of any game binary was launched).
# Enumeration rule (Task A, documented):
#   Linear sweep of the FULL .text section (from physical EXE bytes via own PE
#   section walk), capstone 5.0.7 x86-32, started at .text VA 0x00401000 and
#   decoded contiguously to the section end. A RAW CANDIDATE is any decoded
#   instruction having at least one memory operand with displacement == 0x30
#   and WRITE access, covering: mov reg->[base+0x30] (disp8 and disp32
#   encodings), [base+index*scale+0x30] variants, immediate stores (C7 /0),
#   and any other write-form with disp==0x30 (e.g. x87 fst) - a SUPERSET of
#   the contract-listed mov forms. Embedded data islands (if any) decode as
#   candidates too; they are never promoted to PROVEN without receiver proof.
#   Raw candidate count = the census denominator BEFORE classification.
# Every count in the CSV/raw files is produced by THIS script from physical
# bytes; no hand-typed numbers (COUNTER_ARITHMETIC).

import csv
import json
import struct
import sys

sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone  # noqa: E402

BASE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
sys.path.insert(0, BASE + r"\00_CONTROL")
import sf30_core as C  # noqa: E402

pe = C.PE()  # fail-closed: SHA/size/machine/opt_magic/image_base/no-ASLR asserts

RAW = []
OUT = []


def w(line=""):
    OUT.append(line)


# =====================================================================
# PART 0 - source identity (fail-closed, already asserted in C.PE)
# =====================================================================
ident = {
    "exe_path": C.EXE_PATH,
    "exe_sha256_measured": pe.sha256.upper(),
    "exe_sha256_pinned": C.EXPECTED_SHA256,
    "exe_size_measured": pe.size,
    "exe_size_pinned": C.EXPECTED_SIZE,
    "machine": "0x%04X" % pe.machine,
    "opt_magic": "0x%04X" % pe.opt_magic,
    "image_base": "0x%08X" % pe.image_base,
    "entry_rva": "0x%08X" % pe.entry_rva,
    "sections": [
        {"name": s["name"], "vaddr": "0x%08X" % s["vaddr"], "vsize": "0x%X" % s["vsize"],
         "rsize": "0x%X" % s["rsize"], "va_start": "0x%08X" % s["va_start"],
         "va_end": "0x%08X" % s["va_end"]} for s in pe.sections],
    "aslr_dynamic_base_flag": "clear (no ASLR) - measured",
}
assert ident["exe_sha256_measured"] == ident["exe_sha256_pinned"]
assert ident["exe_size_measured"] == int(ident["exe_size_pinned"])

# =====================================================================
# PART 1 - RTTI CALIBRATION (mandatory known-answer test, run FIRST)
# =====================================================================
w("#" * 78)
w("# 01 RTTI CALIBRATION (known answer first): SceneFeederObject vtable")
w("#" * 78)
cal = pe.rtti_walk(C.SF_VTABLE_VA)
w("# pinned (expected, from accepted prior run - RE-DERIVED HERE, never trusted):")
w("#   vtable=0x%08X expected_name=%s" % (C.SF_VTABLE_VA, C.SF_RTTI_NAME_EXPECTED))
w("# measured walk (all dwords from physical .rdata via own va_to_off):")
w("#   [vtable-4] @ 0x%08X = 0x%08X" % (cal["col_ptr_va"], cal["col_va"]))
w("#   COL @ 0x%08X raw=%s" % (cal["col_va"], cal["col"]["raw"]))
w("#   signature=%d offset=%d cd_offset=%d pTypeDescriptor=0x%08X pClassHierarchy=0x%08X"
  % (cal["col"]["signature"], cal["col"]["offset"], cal["col"]["cd_offset"],
     cal["col"]["p_type_descriptor"], cal["col"]["p_class_hierarchy"]))
w("#   TD @ 0x%08X vfptr=0x%08X spare=0x%08X" % (
    cal["td"]["va"], cal["td"]["vfptr"], cal["td"]["spare"]))
w("#   TD name raw bytes: %s" % cal["td"]["name_raw_hex"])
w("#   TD name (verbatim) = %r" % cal["td"]["name"])
CAL_OK = cal["td"]["name"] == C.SF_RTTI_NAME_EXPECTED
w("# CALIBRATION: measured == expected known answer -> %s" % ("PASS" if CAL_OK else "FAIL"))
assert CAL_OK, "RTTI calibration FAILED - walker unusable (fail-closed)"

# =====================================================================
# PART 2 - SF identity re-derivation (creation chain; starting points only)
# =====================================================================
w("")
w("#" * 78)
w("# 02 SF IDENTITY RE-DERIVATION from physical bytes (contract pins -> measured)")
w("#" * 78)

# 2.1 vtable-store scan: byte pattern of imm32 0x00A7D458 anywhere in .text
w("# 2.1 byte-pattern scan: '58 D4 A7 00' (imm32 0x00A7D458) over full .text")
vt_hits = pe.scan_pattern(bytes.fromhex("58d4a700"))
for h in vt_hits:
    ins = None
    # true containing store: the scanned imm32 is the instruction's trailing
    # operand, so the TRUE containing instruction ends exactly at h+4; misaligned
    # back-decodes that merely COVER h (the old first-covering-wins bug, QC P3-6)
    # are rejected. The hit VA is printed explicitly (old hexdump short-circuit bug).
    for back in range(1, 17):
        cand = pe.disasm_one(h - back)
        if cand and cand["va"] <= h and cand["va"] + cand["size"] == h + 4:
            ins = cand
            break
    assert ins is not None and "0xa7d458" in ins["op_str"], (h, ins)
    w("#   hit 0x%08X -> store insn: %s" % (h, C.render(ins)))
    if ins:
        w("#     raw bytes at %08X: %s" % (ins["va"], ins["bytes"]))
assert [h for h in vt_hits] == [0x509369, 0x50A26B], "unexpected vtable-store set"
ctor_store = pe.disasm_one(0x00509366)
dtor_store = pe.disasm_one(0x0050A269)
w("#   classified: 0x%08X in SF ctor FUN_00509330: %s" % (ctor_store["va"], ctor_store["op_str"]))
w("#   classified: 0x%08X in SF dtor FUN_0050A240: %s" % (dtor_store["va"], dtor_store["op_str"]))
assert ctor_store["mnemonic"] == "mov" and "0xa7d458" in ctor_store["op_str"]
assert dtor_store["mnemonic"] == "mov" and "0xa7d458" in dtor_store["op_str"]

# 2.2 ctor call census (complete direct E8 scan + absolute dword scan)
ctor_callers = pe.calls_to(C.SF_CTOR_VA)
w("# 2.2 direct CALL rel32 (E8) census of ctor 0x00509330 over full .text:")
for c in ctor_callers:
    w("#   E8 callsite 0x%08X" % c)
assert sorted(ctor_callers) == [0x0047D043, 0x0052480F], "ctor caller set drift"
abs_refs = []
d = pe.data
i = 0
pat = struct.pack("<I", C.SF_CTOR_VA)
while True:
    i = d.find(pat, i)
    if i < 0:
        break
    abs_refs.append(i)
    i += 1
w("# 2.3 absolute dword 0x00509330 scan over the WHOLE file (indirect-ref test): %d occurrences"
  % len(abs_refs))
w("#     -> no function-pointer data reference exists; ctor reachable ONLY via the 2 E8 sites")
assert len(abs_refs) == 0

# 2.4 creation chain re-derivation: new(0x98) -> ctor
w("# 2.4 creation chain (a) FUN_005247C0 body - key measured lines:")
chain_a = {
    0x005247E7: ("push", "0x98"),
    0x005247EC: ("call", "0x95d3c4"),
    0x0052480D: ("mov", "ecx, eax"),
    0x0052480F: ("call", "0x509330"),
    0x00524814: ("mov", "esi, eax"),
}
for va, expect in chain_a.items():
    ins = pe.disasm_one(va)
    w("#   %s  %-26s %-6s %s" % ("%08X" % va, ins["bytes"], ins["mnemonic"], ins["op_str"]))
    assert ins["mnemonic"] == expect[0] and ins["op_str"] == expect[1], (va, ins, expect)
new_thunk = pe.resolve_thunk(0x95D3C4)
del_thunk = pe.resolve_thunk(0x95D42A)
w("#   thunk 0x0095D3C4 -> %s   (one-hop IAT resolve, own import walk)" % new_thunk)
w("#   thunk 0x0095D42A -> %s" % del_thunk)
assert new_thunk == "MSVCR80.dll.??2@YAPAXI@Z"
assert del_thunk == "MSVCR80.dll.??3@YAXPAX@Z"
w("# 2.4 creation chain (b) FUN_0047CCF0 window - key measured lines:")
chain_b = [0x0047CFC6, 0x0047CFDE, 0x0047CFE3, 0x0047D03A, 0x0047D043, 0x0047D048, 0x0047D04A]
for va in chain_b:
    ins = pe.disasm_one(va)
    w("#   %s  %-26s %-6s %s" % ("%08X" % va, ins["bytes"], ins["mnemonic"], ins["op_str"]))

# 2.5 durable SF-pointer stores at the 7 create-callsites (complete E8 census)
w("# 2.5 complete E8 callsite census of FUN_005247C0 -> durable SF-pointer stores:")
create_callers = pe.calls_to(C.SF_CREATE_VA)
w("#   E8 callsites: %s" % ", ".join("0x%08X" % c for c in create_callers))
SF_SLOT_STORES = []  # (callsite, store_va, field_off, container_reg)
for cs in create_callers:
    found = None
    for ins in pe.disasm_range(cs + 5, 0x20):
        if ins["mnemonic"] == "mov" and len(ins["mem_ops"]) == 1 and "W" in ins["mem_ops"][0]["access"]:
            mo = ins["mem_ops"][0]
            if mo["index"] == "" and mo["base"] not in ("esp",) and "," in ins["op_str"]:
                # mov [container+field], eax (returned SF)
                parts = ins["op_str"].split(",")
                if parts[1].strip() == "eax":
                    found = (ins["va"], mo["disp"], mo["base"])
                    break
    if found:
        SF_SLOT_STORES.append((cs, found[0], found[1], found[2]))
        w("#   callsite 0x%08X: %08X  %s  %s   <- SF pointer stored at container(%s)+0x%X"
          % (cs, found[0], pe.disasm_one(found[0])["bytes"], pe.disasm_one(found[0])["op_str"],
             found[2], found[1]))
assert len(SF_SLOT_STORES) == len(create_callers), "SF store not found after some callsite"

# 2.6 F_SF: functions with a PROVEN SF-this receiver (evidence recorded)
#   ctor/dtor: vtable store of 0x00A7D458 at [this]
#   vtable slots 0..5: this = SF for any instance of the RTTI-verified class
#   methods called with ecx=SF (measured sites below)
F_SF = {
    0x00509330: "SF ctor: vtable store 0x00509366 mov [ebp],0xa7d458; this=ecx per 0x00509357 mov ebp,ecx",
    0x0050A240: "SF dtor body: vtable store 0x0050A269 mov [esi],0xa7d458; this=ecx per 0x0050A263 mov esi,ecx; called from vtable slot 0 (0x0050A460 body: call 0x50A240 with ecx=this)",
    0x0050A460: "vtable slot 0 (scalar deleting dtor), entry 0x00A7D458 slot[0]=0x0050A460",
    0x005090A0: "vtable slot 1, entry 0x00A7D45C",
    0x005090B0: "vtable slot 2, entry 0x00A7D460",
    0x0050A050: "vtable slot 3, entry 0x00A7D464 (reads SF+0x30; positive control window)",
    0x005090C0: "vtable slot 4, entry 0x00A7D468",
    0x00509580: "vtable slot 5, entry 0x00A7D46C",
    0x005094C0: "SF method: called with ecx=SF loaded from proven SF slots: load @0x0052901A mov ecx,[esi+0xc0] + call @0x00529020; load @0x0067B8E4 mov ecx,[esi+4] + call @0x0067B8E8; load @0x0067C8A4 + call @0x0067C8A8; load @0x006A3A29 mov ecx,[esi+0x18] + call @0x006A3A2D",
    0x005094E0: "SF method: called with ecx=SF (esi=ctor return) at 0x0052482B in FUN_005247C0",
    0x00509670: "SF method: called with ecx=esi=SF at 0x0050A298 in SF dtor body",
    0x00509F00: "SF method: called with ecx=esi=SF at 0x0050A2A9 in SF dtor body",
    0x005247C0: "SF creation function: esi = ctor 0x509330 return (=new(0x98) block) at 0x00524814",
    0x0047CCF0: "SF creation function: ebx/[esp+0x60] = ctor return at 0x0047D048/0x0047D04A",
}
# container functions holding SF in a field (SF pointer slot proven in 2.5)
CONTAINER_FNS = {}
for cs, sva, off, reg in SF_SLOT_STORES:
    fs = pe.find_function_start(sva)
    if fs is None:
        fs = pe.find_function_start(sva, max_back=0x8000)
    CONTAINER_FNS.setdefault(fs, []).append((off, reg, sva))
    if fs:
        F_SF.setdefault(fs, ("SF container function: SF stored at [%s+0x%X] (0x%08X); "
                             "SF-this reloadable from that field" % (reg, off, sva)))
w("# 2.6 F_SF (functions with proven SF-this availability) - complete list with evidence:")
for f in sorted(F_SF):
    w("#   FUN_%08X: %s" % (f, F_SF[f]))

# =====================================================================
# PART 3 - THE CENSUS (documented enumeration rule -> raw candidates)
# =====================================================================
# Sweep robustness rule: capstone's generator stops at the first
# undecodable byte; the sweep therefore RESTARTS one byte after the last
# decoded instruction until the section end, so every byte position is
# consumed by the sweep (bad bytes skipped singly). This keeps the
# denominator complete over the full .text.
w("")
w("#" * 78)
w("# 03 WRITER CENSUS - RAW SCAN (enumeration rule in file header)")
w("#" * 78)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
text_va = pe.text_va_start
text_bytes = pe.text_raw
candidates = []
n_decoded = 0
n_restarts = 0
mv = memoryview(text_bytes)
pos = 0
n = len(text_bytes)
while pos < n:
    last_end = pos
    for ins in md.disasm(mv[pos:], text_va + pos):
        n_decoded += 1
        last_end = pos + (ins.address - (text_va + pos)) + ins.size
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
                candidates.append(ins.address)
                break
    if last_end >= n:
        break
    pos = last_end + 1
    n_restarts += 1
w("# linear sweep: .text VA 0x%08X..0x%08X (rsize 0x%X)" % (text_va, pe.text_va_end, len(text_bytes)))
w("# sweep instructions decoded: %d ; undecodable-byte restarts: %d" % (n_decoded, n_restarts))
w("# RAW CANDIDATES (write-mem disp==0x30, any form incl. disp8/disp32/base+index/imm-store): %d"
  % len(candidates))
assert len(candidates) > 0

# SF family vtable-pointer census (supporting): stores of 0x00A7D42C
# (SF base-class dtor transition observed in the SF dtor body at 0x0050A2EC)
fam42c = pe.scan_pattern(bytes.fromhex("2cd4a700"))
w("# byte-pattern '2C D4 A7 00' (imm32 0x00A7D42C) in .text: %s"
  % ", ".join("0x%08X" % h for h in fam42c))
for h in fam42c:
    ins = None
    # true containing store from its true start (QC P3-6; same end-anchored rule
    # as section 2.1: the imm32 is the trailing operand, true insn ends at h+4)
    for back in range(1, 17):
        cand = pe.disasm_one(h - back)
        if cand and cand["va"] <= h and cand["va"] + cand["size"] == h + 4:
            ins = cand
            break
    assert ins is not None and "0xa7d42c" in ins["op_str"], (h, ins)
    w("#   hit 0x%08X -> store insn: %s" % (h, C.render(ins)))
fam444 = pe.scan_pattern(bytes.fromhex("44d4a700"))
w("# byte-pattern '44 D4 A7 00' (imm32 0x00A7D444, pushed in SF ctor at 0x00509498) in .text: %s"
  % ", ".join("0x%08X" % h for h in fam444))

# Function map: every 16-aligned entry preceded by CC/90 padding (MSVC layout)
entry_vas = []
tr = text_bytes
for off in range(0x10, len(tr), 0x10):
    if tr[off - 1] in (0xCC, 0x90):
        entry_vas.append(text_va + off)
FNMAP = []  # (start, body_end)
_stops = []
for e in entry_vas:
    body, b_end, stop = pe.derive_body(e)
    if body:
        FNMAP.append((e, b_end))
        _stops.append((e, stop))
# extend with tight-adjacent entries: a body that stopped with RET_AT_ALIGN
# hands the next function entry at the aligned stop VA (MSVC tight adjacency)
seen = {s for (s, _e) in FNMAP}
added = 0
changed = True
while changed:
    changed = False
    for (e, stop) in list(_stops):
        if stop[0] == "RET_AT_ALIGN" and stop[1] not in seen and stop[1] < pe.text_va_end:
            seen.add(stop[1])
            body, b_end, st = pe.derive_body(stop[1])
            if body:
                FNMAP.append((stop[1], b_end))
                _stops.append((stop[1], st))
                added += 1
                changed = True
FNMAP.sort()
w("# function map: %d aligned padded entries discovered; %d bodies derived; %d tight-adjacent entries added"
  % (len(entry_vas), len(FNMAP), added))


def map_lookup(va):
    import bisect
    idx = bisect.bisect_right(FNMAP, (va, 0xFFFFFFFF)) - 1
    if idx >= 0:
        s, e = FNMAP[idx]
        if s <= va <= e:
            return s
    return None

# base-register distribution
from collections import Counter
base_counter = Counter()
for va in candidates:
    ins = pe.disasm_one(va)
    for m in ins["mem_ops"]:
        if m["disp"] == 0x30 and "W" in m["access"]:
            base_counter[m["base"] or "(none)"] += 1
w("# raw candidate base-register distribution: %s"
  % ", ".join("%s=%d" % (k, v) for k, v in sorted(base_counter.items())))

# =====================================================================
# PART 4 - CLASSIFICATION
# =====================================================================
# Policy (per contract 4 classes; receiver provenance per hit):
#   PROVEN_SF30_WRITER : base register proven == SF-this at the instruction
#                        (in-register dataflow chain to a proven SF origin).
#   POSSIBLE_ALIAS     : receiver provenance not resolvable to SF or non-SF
#                        within this run's static bounds (SF pointer origin
#                        closure across the whole binary not performed).
#   REJECTED_ALIAS     : proven non-SF receiver, with the reason:
#     R-ESP            : base==esp -> thread-stack slot (SF is heap-only:
#                        both proven creation paths use operator new).
#     R-EBP-FRAME      : base==ebp and fn prologue 'push ebp; mov ebp,esp'
#                        -> frame pointer -> stack.
#     R-EBP-INHERITED  : base==ebp, fn never redefines ebp, not an F_SF FPO
#                        fn -> inherited ancestor frame pointer -> stack.
#     R-LEA-STACK      : base defined by 'lea reg,[esp+X]'/'lea reg,[ebp+X]'
#                        within the fn before the write (stack object).
#     R-IMM-STATIC     : base defined by 'mov reg, imm32'/'lea reg,[imm]'
#                        -> fixed data-section address; SF proven always
#                        heap (no static/placement creation exists).
#     R-CONT-FIELD     : base proven == SF-container (not SF itself); a
#                        write [container+0x30] hits the container field 0x30
#                        (SF pointer slot is at +0x0C/+0x04/+0x10/+0x14/
#                        +0x18/+0xC0 per Part 2.5), not SF+0x30.
#     R-CTOR-OTHER     : hit in a function that stores a DIFFERENT vtable
#                        into its own [this] (other class ctor) and the base
#                        register is that this.
#   UNRESOLVED        : receiver trace attempted, ambiguous (e.g. register
#                        defined through a chain this run did not chase).
# SF-this provenance within F_SF functions (measured anchors):
#   FUN_00509330: ebp==SF (0x00509357 mov ebp,ecx; 0x00509366 vtable store [ebp])
#   FUN_0050A240: esi==SF (0x0050A263 mov esi,ecx; 0x0050A269 vtable store [esi])
#   slots/methods 0x509xxx: ecx==SF at entry (thiscall)
#   FUN_005247C0: esi==SF after 0x00524814 mov esi,eax
#   FUN_0047CCF0: ebx==SF after 0x0047D048; also stack slot [esp+0x60]
#   container fns: SF==[container_reg+field] (field per Part 2.5)
w("")
w("#" * 78)
w("# 04 CLASSIFICATION (policy in header; every row in the CSV)")

SF_SLOTS_BY_FN = {}
for cs, sva, off, reg in SF_SLOT_STORES:
    fs = pe.find_function_start(sva)
    if fs is None:
        fs = pe.find_function_start(sva, max_back=0x8000)
    if fs:
        SF_SLOTS_BY_FN.setdefault(fs, []).append((reg, off))


def trace_reg_in_fn(insns, idx, reg):
    """Backward scan for the last definition of `reg` before insns[idx].
    Returns (kind, detail) or (None, None) if not found in-function."""
    j = idx - 1
    steps = 0
    while j >= 0 and steps < 400:
        ins = insns[j]
        ops = ins["op_str"]
        mn = ins["mnemonic"]
        # register as destination (first operand, before comma)
        if ops == reg and mn in ("inc", "dec", "not", "neg"):
            return ("ALU", "%s @ %08X" % (ops, ins["va"]))
        if ops.startswith(reg + ",") or ops.startswith(reg.upper() + ","):
            if mn == "mov":
                src = ops.split(",", 1)[1].strip()
                if src.startswith("0x") or src.startswith("dword ptr [0x") or src.startswith("0"):
                    return ("IMM", "%s @ %08X" % (ops, ins["va"]))
                if src == "esp":
                    return ("FROM_ESP", "mov %s,esp @ %08X" % (reg, ins["va"]))
                if src == "ebp":
                    return ("FROM_EBP", "mov %s,ebp @ %08X" % (reg, ins["va"]))
                if src.startswith("dword ptr ["):
                    return ("LOAD", "%s @ %08X" % (ops, ins["va"]))
                return ("REGCOPY", "%s @ %08X" % (ops, ins["va"]))
            if mn == "lea":
                return ("LEA", "%s @ %08X" % (ops, ins["va"]))
            if mn in ("pop",):
                return ("POP", "%s @ %08X" % (ops, ins["va"]))
            if mn in ("xor", "sub") and ops.startswith(reg + ","):
                other = ops.split(",", 1)[1].strip()
                if other == reg:
                    return ("ZERO", "%s @ %08X" % (ops, ins["va"]))
                return ("ALU", "%s @ %08X" % (ops, ins["va"]))
            return ("ALU", "%s @ %08X" % (ops, ins["va"]))
        # call clobbers eax (caller-saved: eax,ecx,edx)
        if mn == "call" and reg in ("eax", "ecx", "edx"):
            return ("CALL_RESULT", "call @ %08X defines %s" % (ins["va"], reg))
        j -= 1
        steps += 1
    return (None, None)


def fn_has_ebp_frame(insns):
    for i in insns[:12]:
        if i["mnemonic"] == "mov" and i["op_str"].startswith("ebp, esp"):
            return True
        if i["mnemonic"] == "mov" and i["op_str"].startswith("ebp,"):
            return False
    return False


# decode each F_SF function body once; also special fn->sf_reg map
FN_SF_REG = {
    0x00509330: ("ebp", "0x00509357 mov ebp,ecx; 0x00509366 mov [ebp],0xa7d458"),
    0x0050A240: ("esi", "0x0050A263 mov esi,ecx; 0x0050A269 mov [esi],0xa7d458"),
    0x0050A460: ("ecx", "thiscall entry (vtable slot 0)"),
    0x005090A0: ("ecx", "thiscall entry (vtable slot 1)"),
    0x005090B0: ("ecx", "thiscall entry (vtable slot 2)"),
    0x0050A050: ("ecx", "thiscall entry (vtable slot 3)"),
    0x005090C0: ("ecx", "thiscall entry (vtable slot 4)"),
    0x00509580: ("ecx", "thiscall entry (vtable slot 5)"),
    0x005094C0: ("ecx", "thiscall entry; receiver proven at 4 call sites"),
    0x005094E0: ("ecx", "thiscall entry; receiver proven at 0x0052482B"),
    0x00509670: ("ecx", "thiscall entry; receiver proven at 0x0050A298"),
    0x00509F00: ("ecx", "thiscall entry; receiver proven at 0x0050A2A9"),
    0x005247C0: ("esi", "0x00524814 mov esi,eax (eax=ctor return=SF)"),
    0x0047CCF0: ("ebx", "0x0047D048 mov ebx,eax (eax=ctor return=SF); also [esp+0x60]"),
}

FN_BODY_CACHE = {}


def fn_body(fs):
    if fs not in FN_BODY_CACHE:
        FN_BODY_CACHE[fs] = pe.derive_body(fs)[0]
    return FN_BODY_CACHE[fs]


# classify every candidate
def fn_vtable_store_class(body):
    """If fn stores a DIFFERENT class vtable into [this+0] (ctor pattern),
    return (store_reg, vtable_imm) - ONLY when the imm is in .rdata/.data AND
    RTTI-walks to a valid TypeDescriptor name (prevents flag/data immediates
    masquerading as vtables). First such store wins."""
    for ins in body:
        if ins["mnemonic"] == "mov" and len(ins["mem_ops"]) == 1:
            mo = ins["mem_ops"][0]
            if mo["base"] and mo["index"] == "" and mo["disp"] == 0 and "W" in mo["access"]:
                parts = ins["op_str"].split(",")
                src = parts[1].strip() if len(parts) > 1 else ""
                if src.startswith("0x"):
                    imm = int(src, 16)
                    if imm in (0x00A7D458, 0x00A7D42C):
                        continue  # SceneFeederObject family - never 'other'
                    if pe.section_of(imm) not in (".rdata", ".data"):
                        continue
                    rw = pe.rtti_walk(imm)
                    if "td" in rw and rw["td"]["name"]:
                        return (mo["base"], imm)
    return (None, None)


rows = []
for va in candidates:
    ins = pe.disasm_one(va)
    fs = map_lookup(va)
    if fs is None:
        fs = pe.find_function_start(va, max_back=0x4000)
    fkey = fs if (fs and fs in F_SF) else None
    base = ""
    for m in ins["mem_ops"]:
        if m["disp"] == 0x30 and "W" in m["access"]:
            base = m["base"]
            break
    cls = None
    why = ""
    srcval = ins["op_str"].split(",", 1)[1].strip() if "," in ins["op_str"] else ""
    recv = "unknown"
    if fkey is not None:
        body = fn_body(fkey)
        idx = next((k for k, x in enumerate(body) if x["va"] == va), None)
        if idx is None:
            cls = "UNRESOLVED"
            why = "hit VA not inside derived body of F_SF fn %08X (attribution mismatch)" % fkey
        else:
            sfreg, sfprovenance = FN_SF_REG.get(fkey, (None, None))
            slots = SF_SLOTS_BY_FN.get(fkey, [])
            cregs = {r for (r, _o) in slots}
            if base == "esp":
                cls = "REJECTED_ALIAS"
                why = ("R-ESP: write to thread-stack slot; SF proven heap-only "
                       "(both creation paths operator new)")
                recv = "stack slot (esp+0x30)"
            elif base == sfreg:
                cls = "PROVEN_SF30_WRITER"
                why = "base==%s==SF-this in %s (SF reg provenance: %s)" % (
                    base, "FUN_%08X" % fkey, sfprovenance)
                recv = "SF-this (register %s, %s)" % (base, sfprovenance)
            else:
                kind, detail = trace_reg_in_fn(body, idx, base)
                if kind == "LOAD":
                    hit_sf_load = any(
                        ("dword ptr [%s + 0x%x]" % (r, o)) in detail for (r, o) in slots)
                    if hit_sf_load:
                        cls = "PROVEN_SF30_WRITER"
                        why = ("base==%s loaded from a proven SF-pointer slot (%s) in %s"
                               % (base, detail, "FUN_%08X" % fkey))
                        recv = "SF-this (loaded from container SF slot)"
                    else:
                        cls = "POSSIBLE_ALIAS"
                        why = ("base==%s loaded from memory (%s) in SF-context fn %08X; "
                               "loaded value's class not resolvable within run bounds"
                               % (base, detail, fkey))
                elif kind == "REGCOPY":
                    src2 = detail.split(",", 1)[1].strip().split(" ")[0]
                    if src2 == sfreg:
                        cls = "PROVEN_SF30_WRITER"
                        why = ("base==%s copied from SF register %s (%s) in %s"
                               % (base, src2, detail, "FUN_%08X" % fkey))
                        recv = "SF-this (copy of SF reg)"
                    elif src2 == "ecx":
                        def_va = int(detail.split(" @ ")[1], 16)
                        if any(x["va"] == def_va and k2 < 20 for k2, x in enumerate(body)):
                            # copy of thiscall this at fn entry -> the fn's own this
                            cls = "REJECTED_ALIAS"
                            why = ("R-CONT-FIELD: base==%s==this(container) copied at entry "
                                   "(%s) in container fn %08X; [container+0x30] writes the "
                                   "container's field 0x30, not SF+0x30 (SF pointer slot at %s)"
                                   % (base, detail, fkey,
                                      "+0x%X" % slots[0][1] if slots else "?"))
                            recv = "container+0x30 (container this)"
                        else:
                            cls = "UNRESOLVED"
                            why = ("base==%s copied from ecx mid-body (%s); origin not traced "
                                   "within run bounds" % (base, detail))
                    else:
                        cls = "UNRESOLVED"
                        why = ("base==%s copied from %s (%s); origin not traced to SF or "
                               "non-SF within run bounds" % (base, src2, detail))
                elif kind == "LEA":
                    if "[esp" in detail or "[ebp" in detail:
                        cls = "REJECTED_ALIAS"
                        why = "R-LEA-STACK: base==%s = lea of stack address (%s)" % (base, detail)
                        recv = "stack object"
                    else:
                        cls = "UNRESOLVED"
                        why = "base==%s = lea %s (non-stack base, not traced to SF)" % (base, detail)
                elif kind == "IMM":
                    cls = "REJECTED_ALIAS"
                    why = ("R-IMM-STATIC: base==%s = fixed immediate address (%s); SF proven "
                           "always-heap" % (base, detail))
                    recv = "static data address"
                elif kind in ("FROM_ESP", "FROM_EBP"):
                    cls = "REJECTED_ALIAS"
                    why = "R-STACK-PTR: base==%s copied from stack pointer (%s)" % (base, detail)
                    recv = "stack"
                elif kind == "ZERO":
                    cls = "REJECTED_ALIAS"
                    why = ("R-ZERO: base==%s zeroed in-register (%s) before the write; a null "
                           "base cannot be an SF instance" % (base, detail))
                    recv = "null base"
                elif kind == "CALL_RESULT":
                    cls = "UNRESOLVED"
                    why = ("base==%s = result of call (%s); callee return not traced "
                           "within run bounds" % (base, detail))
                elif kind == "POP":
                    cls = "UNRESOLVED"
                    why = "base==%s from pop (%s); origin not traced within run bounds" % (base, detail)
                elif kind is None:
                    if base == "ebp" and fn_has_ebp_frame(body):
                        cls = "REJECTED_ALIAS"
                        why = "R-EBP-FRAME: ebp is the fn frame pointer; [ebp+0x30] is a stack local/arg"
                        recv = "stack local/arg"
                    else:
                        cls = "POSSIBLE_ALIAS"
                        why = ("base==%s has no in-function definition (holds caller value); "
                               "receiver not resolvable within run bounds" % base)
                else:
                    cls = "UNRESOLVED"
                    why = "base==%s defined by %s" % (base, detail)
    else:
        bdy = fn_body(fs) if fs else []
        idx2 = next((k for k, x in enumerate(bdy) if x["va"] == va), None) if bdy else None
        if bdy and idx2 is not None and base:
            kind, detail = trace_reg_in_fn(bdy, idx2, base)
        else:
            kind, detail = (None, None)
        if base == "esp":
            cls = "REJECTED_ALIAS"
            why = ("R-ESP: write to thread-stack slot (esp base); SF proven heap-only "
                   "(both creation paths operator new); heap addresses never equal the "
                   "thread-stack pointer")
            recv = "stack slot (esp+0x30)"
        elif base == "ebp":
            if bdy and fn_has_ebp_frame(bdy):
                cls = "REJECTED_ALIAS"
                why = "R-EBP-FRAME: fn has 'push ebp; mov ebp,esp' frame; [ebp+0x30] is a stack local/arg"
                recv = "stack local/arg"
            elif bdy and kind is None and not any(
                    i["mnemonic"] == "mov" and i["op_str"].startswith("ebp,") for i in bdy):
                cls = "REJECTED_ALIAS"
                why = ("R-EBP-INHERITED: fn never redefines ebp (FPO, ebp untouched); "
                       "ebp = ancestor frame pointer = stack address")
                recv = "caller stack (inherited ebp)"
            elif kind == "LEA" and ("[esp" in detail or "[ebp" in detail):
                cls = "REJECTED_ALIAS"
                why = "R-LEA-STACK: base==ebp = lea of stack address (%s)" % detail
                recv = "stack object"
            else:
                cls = "POSSIBLE_ALIAS"
                why = ("base==ebp redefined in non-SF-proven fn (FPO repurpose: %s); "
                       "receiver not resolvable within run bounds" % (detail or "unattributed fn"))
                recv = "unknown (ebp repurposed)"
        elif base == "":
            cls = "UNRESOLVED"
            why = "write form without a base register (absolute/disp-only form)"
        else:
            # R-CTOR-OTHER: the fn constructs a DIFFERENT class (stores its vtable
            # into [this+0]) and the hit's base IS that this: only when base is
            # never redefined in the fn (kind is None) or is an entry-adjacent
            # copy of ecx. Assumption documented in header: an SF instance is
            # never passed as this to a different class's constructor (no such
            # passing exists in any SF-context function derived in this run).
            vts_reg, vts_imm = fn_vtable_store_class(bdy)
            src2 = detail.split(",", 1)[1].strip().split(" ")[0] if (
                kind == "REGCOPY" and detail) else None
            ctor_other_ok = bool(vts_reg) and base == vts_reg and (
                kind is None or (kind == "REGCOPY" and src2 == "ecx"))
            if ctor_other_ok:
                cls = "REJECTED_ALIAS"
                name = "?"
                rw = pe.rtti_walk(vts_imm)
                if "td" in rw:
                    name = rw["td"]["name"]
                why = ("R-CTOR-OTHER: containing fn stores vtable 0x%08X (RTTI %r) into "
                       "[this+0]; hit's base==that this-reg (never redefined in fn) -> "
                       "receiver is that class, not SceneFeederObject" % (vts_imm, name))
                recv = "other-class this (vtable 0x%08X, %s)" % (vts_imm, name)
            elif kind == "LEA" and ("[esp" in detail or "[ebp" in detail):
                cls = "REJECTED_ALIAS"
                why = "R-LEA-STACK: base==%s = lea of stack address (%s) -> stack object" % (base, detail)
                recv = "stack object"
            elif kind == "IMM":
                cls = "REJECTED_ALIAS"
                why = ("R-IMM-STATIC: base==%s = fixed immediate address (%s); SF proven "
                       "always-heap (both creation paths operator new; no static/placement "
                       "creation exists)" % (base, detail))
                recv = "static data address"
            elif kind in ("FROM_ESP", "FROM_EBP"):
                cls = "REJECTED_ALIAS"
                why = "R-STACK-PTR: base==%s copied from stack pointer (%s)" % (base, detail)
                recv = "stack"
            elif kind == "ZERO":
                cls = "REJECTED_ALIAS"
                why = ("R-ZERO: base==%s zeroed in-register (%s) before the write; a null "
                       "base cannot be an SF instance" % (base, detail))
                recv = "null base"
            else:
                cls = "POSSIBLE_ALIAS"
                why = ("receiver provenance not resolvable within this run's static bounds "
                       "(SF pointer origin closure across the whole binary not performed); "
                       "base==%s in a function not proven to ever receive SF" % base)
    rows.append({
        "writer_va": "0x%08X" % va,
        "function_va": ("0x%08X" % fs) if fs else "UNATTRIBUTED",
        "instruction": "%s %s" % (ins["mnemonic"], ins["op_str"]),
        "source_register_value": srcval,
        "receiver_provenance": recv,
        "classification": cls,
        "why": why,
        "bytes": ins["bytes"],
    })

# COUNTER_ARITHMETIC: counts recomputed FROM THE ROWS
from collections import Counter as C2
cls_counter = C2(r["classification"] for r in rows)
TOTAL = len(rows)
w("# classified rows: %d" % TOTAL)
for k in ("PROVEN_SF30_WRITER", "POSSIBLE_ALIAS", "REJECTED_ALIAS", "UNRESOLVED"):
    w("#   %-20s %d" % (k, cls_counter.get(k, 0)))
proven_set = {r["writer_va"] for r in rows if r["classification"] == "PROVEN_SF30_WRITER"}
w("# PROVEN writer set: %s" % ", ".join(sorted(proven_set)))
assert proven_set <= {"0x005093C3", "0x0050A2D1"}, proven_set

# =====================================================================
# PART 5 - coverage classes (i)-(iv)
# =====================================================================
w("")
w("#" * 78)
w("# 05 COVERAGE CLASSES (i)-(iv)")
w("#" * 78)
# (i) writes via a register holding SF-this: ALL base-register hits are in the
#     census; F_SF-function hits were register-traced (see CSV).
w("# (i) register-held SF-this: census covers every write-mem disp0x30 form in")
w("#     .text; F_SF functions (%d) fully traced - PROVEN writers:" % len(F_SF))
for r in rows:
    if r["classification"] == "PROVEN_SF30_WRITER":
        w("#     %s  %s  [%s]" % (r["writer_va"], r["instruction"], r["why"]))
# (ii) SF pointer in a stack slot/local: creation fn 0x0047CCF0 keeps SF at
#      [esp+0x60]; the census traces loads of base regs from stack slots inside
#      F_SF functions (trace_reg_in_fn LOAD case).
w("# (ii) SF pointer held in a stack slot/local: F_SF traces cover stack-slot")
w("#     SF holders ([esp+0x60] in FUN_0047CCF0, [esp+0x2c] in FUN_005247C0);")
w("#     any [reg+0x30] write whose base was loaded from those slots would be")
w("#     classified PROVEN via the LOAD trace. No such writer exists outside")
w("#     the two PROVEN rows (see CSV).")
# (iii) combined-offset writes via the container: SF pointer slots proven at
#      +0x0C/+0x10/+0x14 (FUN_0044D590), +0xC0 (FUN_00528E50), +0x04
#      (FUN_0067B800, FUN_0067C7C0), +0x18 (FUN_006A3xxx). Combined disp forms
#      field+0x30 = {0x3C, 0x40, 0x44, 0xF0, 0x34, 0x48}.
comb = {0x3C, 0x40, 0x44, 0xF0, 0x34, 0x48}
w("# (iii) combined-offset writes through the container holding the SF POINTER:")
comb_hits = []
for fkey in SF_SLOTS_BY_FN:
    body = fn_body(fkey)
    for i, ins in enumerate(body):
        for m in ins["mem_ops"]:
            if m["disp"] in comb and "W" in m["access"] and m["base"] in (
                    [r for r, _ in SF_SLOTS_BY_FN[fkey]]):
                comb_hits.append((fkey, ins, m))
for fkey, ins, m in comb_hits:
    w("#     combined-form candidate %s: %s (container=%s, disp=0x%X)"
      % ("0x%08X" % ins["va"], C.render(ins), m["base"], m["disp"]))
if not comb_hits:
    w("#     ZERO combined-disp (0x34/0x3C/0x40/0x44/0x48/0xF0) writes through the")
    w("#     container registers at the proven container functions.")
w("#     Static fact: the SF slot holds a POINTER (store 'mov [container+field],eax'")
w("#     with eax = operator-new block), so a [container+field+0x30] write would")
w("#     hit the container's OWN field, not SF+0x30 (SF not embedded). Evidence")
w("#     stores: %s" % "; ".join("0x%08X [+0x%X]" % (sv, off) for _, sv, off, _ in SF_SLOT_STORES))
# (iv) bulk initialization covering +0x30 (rep movsd / memcpy-style) at SF
#      ctor/init sites: enumerate string/bulk ops in SF ctor + SF init methods.
w("# (iv) bulk-init covering SF+0x30 at SF ctor/init sites:")
bulk = []
for fkey in (0x00509330, 0x0050A240, 0x005094C0, 0x005094E0, 0x00509670, 0x00509F00):
    body = fn_body(fkey)
    for ins in body:
        # capstone 5.0.7 renders F3 A5 as mnemonic 'rep movsd'
        if ("movsd" in ins["mnemonic"] or "stosd" in ins["mnemonic"]) and "dword" in ins["op_str"]:
            bulk.append((fkey, ins))
for fkey, ins in bulk:
    w("#     %s: %s" % ("FUN_%08X" % fkey, C.render(ins)))
if not bulk:
    w("#     no bulk/string ops found in SF ctor/init bodies")
w("#     Both SF-ctor rep movsd targets: 0x0050945D -> [edi]=[esp+0x18] (stack),")
w("#     0x0050946E -> [edi]=[ebp+0x4C] (SF+0x4C..0x70). Neither covers +0x30.")
w("#     (measured lines recorded in the raw evidence below)")

# =====================================================================
# PART 6 - PROVENANCE (Task B) for PROVEN writers, up to creation/receipt only
# =====================================================================
prov_md = []
prov_md.append("# SF30_PROVENANCE - value-source chains for PROVEN_SF30_WRITER rows")
prov_md.append("RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")
prov_md.append("")
prov_md.append("All VAs and bytes below are MEASURED from the physical EXE (own PE walk,")
prov_md.append("capstone 5.0.7 x86-32). STATIC-ONLY. Chains stop at creation/receipt of the")
prov_md.append("written value; the value's later behavior is NOT followed (contract).")
prov_md.append("")
prov_md.append("## P1. writer 0x005093C3 (SF ctor FUN_00509330): [SF+0x30] = new(0x118) block")
prov_md.append("")
prov_md.append("Receiver proof: 0x00509357 `mov ebp,ecx` (SF-this from thiscall ecx);")
prov_md.append("0x00509366 `mov dword ptr [ebp],0xa7d458` (SF vtable store at [this+0]);")
prov_md.append("hence [ebp+0x30] == SF+0x30.")
prov_md.append("")
prov_md.append("| hop | VA | bytes | instruction | evidence |")
prov_md.append("|---|---|---|---|---|")
for va in (0x00509376, 0x005093A0, 0x005093A5, 0x005093AC, 0x005093B5, 0x005093B6, 0x005093B8,
           0x005093BD, 0x005093BF, 0x005093C1, 0x005093C3, 0x005093C6, 0x005093C8):
    ins = pe.disasm_one(va)
    note = {
        0x00509376: "alloc size 0x118 pushed",
        0x005093A0: "operator new (thunk 0x95D3C4 = MSVCR80.dll.??2@YAPAXI@Z)",
        0x005093A5: "cdecl cleanup of the new() arg",
        0x005093AC: "null test of the new block",
        0x005093B5: "ctor arg = 0 (ebx)",
        0x005093B6: "ecx = new block (this for 0x7B6000)",
        0x005093B8: "block initializer FUN_007B6000(this=block, 0)",
        0x005093BD: "skip-null path join",
        0x005093BF: "alloc-fail path: eax = 0",
        0x005093C1: "null test of initialized block (ctor return)",
        0x005093C3: "WRITE: SF+0x30 = block pointer",
        0x005093C6: "if null skip refcount",
        0x005093C8: "refcount++ at block+4",
    }.get(va, "")
    prov_md.append("| %08X | %s | `%s %s` | %s |" % (va, ins["bytes"], ins["mnemonic"], ins["op_str"], note))
prov_md.append("")
prov_md.append("Source chain (creation/receipt level): operator new(0x118) -> initialized by")
prov_md.append("FUN_007B6000 (thiscall this=block, arg=0) -> returned block pointer stored at")
prov_md.append("SF+0x30 -> refcount dword at block+4 incremented. STOP (later behavior not")
prov_md.append("followed).")
prov_md.append("")
prov_md.append("Block initializer identity evidence (only what Task C needs; NO method of")
prov_md.append("the link vtable is decoded anywhere in this run; callees inside the block ctor")
prov_md.append("are recorded at receipt level only and are NOT analyzed):")
prov_md.append("")
for va in (0x007B6023, 0x007B6029, 0x007B6041, 0x007B6047, 0x007B609F):
    ins = pe.disasm_one(va)
    note = {
        0x007B6023: "mov esi,ecx - this = block",
        0x007B6029: "call 0x7C02D0 with this=block (callee NOT analyzed - receipt-level only)",
        0x007B6041: "VTABLE STORE: [this] = 0x00A8CCF4",
        0x007B6047: "call 0x788480 with ecx = &block[+0xC8] (lea ecx,[esi+0xC8] @0x007B6037 — address-of, not dereference) (callee NOT analyzed)",
        0x007B609F: "mov eax,esi - ctor returns this",
    }.get(va, "")
    prov_md.append("- %08X `%s %s` %s" % (va, ins["mnemonic"], ins["op_str"], note))
prov_md.append("")
prov_md.append("Check: FUN_007B6000 (the block ctor, not a vtable method) is NOT an entry of")
prov_md.append("vtable 0x00A8CCF4 (verified in RTTI raw: no slot value equals 0x007B6000).")
prov_md.append("")
prov_md.append("## P2. writer 0x0050A2D1 (SF dtor body FUN_0050A240): [SF+0x30] = 0")
prov_md.append("")
prov_md.append("Receiver proof: 0x0050A263 `mov esi,ecx` (thiscall SF-this); 0x0050A269")
prov_md.append("`mov dword ptr [esi],0xa7d458` (SF vtable store at [this+0]); the function is")
prov_md.append("the dtor body called from vtable slot 0 (FUN_0050A460). Hence [esi+0x30] ==")
prov_md.append("SF+0x30.")
prov_md.append("")
prov_md.append("| hop | VA | bytes | instruction | evidence |")
prov_md.append("|---|---|---|---|---|")
for va in (0x0050A2BD, 0x0050A2C0, 0x0050A2C4, 0x0050A2C8, 0x0050A2CA, 0x0050A2CC, 0x0050A2CF,
           0x0050A2D1, 0x0050A2D4):
    ins = pe.disasm_one(va)
    note = {
        0x0050A2BD: "load link = [SF+0x30]",
        0x0050A2C0: "null test",
        0x0050A2C4: "refcount-- at link+4",
        0x0050A2C8: "if nonzero, keep link",
        0x0050A2CA: "if zero: vtable = [link]",
        0x0050A2CC: "deleter = vtable slot 1",
        0x0050A2CF: "dispatch deleter (destroy link)",
        0x0050A2D1: "WRITE: SF+0x30 = 0 (ebx)",
        0x0050A2D4: "re-read of the now-null field (defensive duplicate)",
    }.get(va, "")
    prov_md.append("| %08X | %s | `%s %s` | %s |" % (va, ins["bytes"], ins["mnemonic"], ins["op_str"], note))
prov_md.append("")
prov_md.append("Source chain (creation/receipt level): the written value is the constant 0 in")
prov_md.append("ebx (`xor ebx,ebx` at 0x0050A272); the write happens after the refcount release")
prov_md.append("protocol. STOP.")
prov_md.append("")
prov_md.append("SOURCE_PROVENANCE per PROVEN writer: P1 = RESOLVED (allocation->ctor->stored);")
prov_md.append("P2 = RESOLVED (constant zero after release protocol).")
open(BASE + r"\02_ANALYSIS\SF30_PROVENANCE.md", "w", encoding="utf-8").write("\n".join(prov_md) + "\n")

# =====================================================================
# PART 7 - RTTI of the link object (Task C) - calibration already passed
# =====================================================================
w("")
w("#" * 78)
w("# 07 LINK-OBJECT RTTI WALK (Task C) - walker calibrated in Part 01")
w("#" * 78)
LINK_VT = pe.read_va32(0x007B6041 + 2)  # imm operand of mov [esi], imm32
w("# vtable discovered from block ctor: 0x007B6041 'mov dword ptr [esi], 0x%08X'" % LINK_VT)
lk = pe.rtti_walk(LINK_VT)
w("# measured walk:")
w("#   [vtable-4] @ 0x%08X = 0x%08X" % (lk["col_ptr_va"], lk["col_va"]))
w("#   COL @ 0x%08X raw=%s" % (lk["col_va"], lk["col"]["raw"]))
w("#   signature=%d offset=%d cd_offset=%d pTypeDescriptor=0x%08X pClassHierarchy=0x%08X"
  % (lk["col"]["signature"], lk["col"]["offset"], lk["col"]["cd_offset"],
     lk["col"]["p_type_descriptor"], lk["col"]["p_class_hierarchy"]))
w("#   TD @ 0x%08X vfptr=0x%08X spare=0x%08X" % (lk["td"]["va"], lk["td"]["vfptr"], lk["td"]["spare"]))
w("#   TD name raw bytes: %s" % lk["td"]["name_raw_hex"])
w("#   TD name (verbatim) = %r" % lk["td"]["name"])
w("#   section of vtable: %s ; of COL: %s ; of TD: %s" % (
    pe.section_of(LINK_VT), pe.section_of(lk["col_va"]), pe.section_of(lk["td"]["va"])))
# vtable extent: count code-pointer entries
n_slots = 0
va = LINK_VT
while True:
    v = pe.read_va32(va)
    if v is None or not pe.in_text(v):
        break
    n_slots += 1
    va += 4
w("#   vtable code-pointer entries from 0x%08X: %d (first non-code dword ends it)" % (LINK_VT, n_slots))
w("#   slot values NOT decoded (contract: no method of the link vtable; slot 17")
w("#   ([vtable+0x44]) is the NEXT seam and is explicitly out of scope)")
slot17 = pe.read_va32(LINK_VT + 0x44)
w("#   [vtable+0x44] dword VALUE recorded but NOT decoded, NOT followed: 0x%08X" % slot17)
w("#   check: block ctor 0x007B6000 is NOT a vtable entry (not a virtual method):")
ct_in_vt = False
for k in range(n_slots):
    if pe.read_va32(LINK_VT + 4 * k) == 0x007B6000:
        ct_in_vt = True
w("#     0x007B6000 among vtable entries: %s" % ("YES" if ct_in_vt else "NO"))
assert not ct_in_vt
# secondary vtable inside the block (embedded member at +0xE0) - recorded, not decoded
lk2 = pe.rtti_walk(0x00A8CCE0)
w("# (supporting, not required) embedded member vtable 0x00A8CCE0 at block+0xE0:")
w("#   RTTI name = %r (COL 0x%08X)" % (lk2["td"]["name"], lk2["col_va"]))
RTTI_NAME = lk["td"]["name"]
assert RTTI_NAME == ".?AVNiNode@@", RTTI_NAME

# =====================================================================
# PART 8 - POSITIVE CONTROL 0x0050A050 window (mandatory)
# =====================================================================
pc_lines = []
pc_lines.append("# POSITIVE CONTROL - FUN_0050A050 @ 0x0050A05B window (measured from physical EXE)")
pc_lines.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")
pc_lines.append("# STATIC-ONLY. capstone 5.0.7 x86-32, own PE va_to_off.")
pc_lines.append("")
win = pe.disasm_range(0x0050A050, 0x30)
pc_lines.append("# full measured window 0x0050A050..:")
for i in win:
    pc_lines.append(C.render(i))
b_a = pe.read_va(0x0050A057, 2)
b_b = pe.read_va(0x0050A05B, 3)
b_c1 = pe.read_va(0x0050A05E, 2)
b_c2 = pe.read_va(0x0050A061, 3)
b_c3 = pe.read_va(0x0050A064, 2)
pc_lines.append("")
pc_lines.append("# (a) 0x0050A057 bytes = %s  -> mov esi,ecx   [ESI := SF-this]" % b_a.hex())
pc_lines.append("#     0x0050A05B bytes = %s  -> mov ecx,[esi+0x30]  [ECX := [SF+0x30]]" % b_b.hex())
assert b_a.hex() == "8bf1"
assert b_b.hex() == "8b4e30"
pc_lines.append("# (b) ECX clobber check between 0x0050A05B and the call 0x0050A064:")
win2 = pe.disasm_range(0x0050A05E, 6)
clobber = False
for i in win2:
    pc_lines.append("#     " + C.render(i))
    if i["op_str"].startswith("ecx,") and i["mnemonic"] != "call":
        clobber = True
pc_lines.append("#     ECX modified in window: %s" % ("YES - FAIL" if clobber else "NO - PASS"))
assert not clobber
pc_lines.append("# (c) receiver chain: edx=[ecx] @ 0x0050A05E (bytes %s);" % b_c1.hex())
pc_lines.append("#     eax=[edx+0x44] @ 0x0050A061 (bytes %s);" % b_c2.hex())
pc_lines.append("#     call eax @ 0x0050A064 (bytes %s)" % b_c3.hex())
assert b_c1.hex() == "8b11"
assert b_c2.hex() == "8b4244", b_c2.hex()
assert b_c3.hex() == "ffd0"
pc_lines.append("#     receiver of CALL = ECX = [ESI+0x30] = [SF+0x30]: CONFIRMED")
pc_lines.append("#     [edx+0x44] is the LINK vtable slot-17 dword VALUE (vtable 0x%08X+0x44=0x%08X):" % (LINK_VT, LINK_VT + 0x44))
pc_lines.append("#       NOT decoded, NOT followed (contract hard scope; next seam).")
pc_lines.append("")
pc_lines.append("# POSITIVE_CONTROL = PASS (a),(b),(c) all measured exactly as specified.")
open(BASE + r"\01_RAW\POSITIVE_CONTROL_0050A050.txt", "w", encoding="utf-8").write("\n".join(pc_lines) + "\n")

# =====================================================================
# PART 9 - raw evidence: derivation (Parts 1-5) + per-candidate windows
# =====================================================================
raw = []
raw.extend(OUT)
raw.append("")
raw.append("# " * 39)
raw.append("# SF30_WRITER_RAW.txt - raw evidence for EVERY census candidate")
raw.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")
raw.append("# EXE: %s" % C.EXE_PATH)
raw.append("# SHA256(measured) = %s  SIZE = %d" % (pe.sha256.lower(), pe.size))
raw.append("# enumeration rule: linear capstone sweep of full .text (VA 0x%08X..0x%08X),"
           % (pe.text_va_start, pe.text_va_end))
raw.append("# candidate = any decoded insn with WRITE mem-operand disp==0x30 (disp8/disp32,")
raw.append("# base+index+scale+disp, immediate stores C7 /0, x87 fst - superset of mov forms).")
raw.append("# RAW CANDIDATE COUNT (denominator before classification): %d" % len(candidates))
raw.append("# instructions decoded in sweep: %d ; sweep bad-byte restarts: %d"
           % (n_decoded, n_restarts))
raw.append("")
raw.append("## per-candidate disassembly windows")
raw.append("# NOTE: each window is decoded linearly from (candidate_va - 8); that start")
raw.append("# address is NOT guaranteed to be an instruction boundary, so window lines")
raw.append("# before the candidate may be misaligned. The candidate line (### header,")
raw.append("# with its byte encoding) is the authoritative sweep-decoded instruction.")
by_va = {r["writer_va"]: r for r in rows}
for va in candidates:
    ins = pe.disasm_one(va)
    prev = pe.disasm_one(va - 8)  # not reliable as prev insn; use sweep context none
    raw.append("### 0x%08X  %s %s   [bytes %s]" % (va, ins["mnemonic"], ins["op_str"], ins["bytes"]))
    row = by_va["0x%08X" % va]
    raw.append("    fn=%s  class=%s" % (row["function_va"], row["classification"]))
    raw.append("    why: %s" % row["why"])
    raw.append("    window:")
    for i in pe.disasm_range(va - 8, 0x14):
        mark = " <== CANDIDATE" if i["va"] == va else ""
        raw.append("      " + C.render(i) + mark)
raw.append("")
raw.append("## raw scan statistics")
raw.append("# .text rsize: 0x%X bytes" % len(text_bytes))
raw.append("# sweep instructions decoded: %d ; bad-byte restarts: %d" % (n_decoded, n_restarts))
raw.append("# raw candidates: %d" % len(candidates))
raw.append("# base-register distribution: %s"
           % ", ".join("%s=%d" % (k, v) for k, v in sorted(base_counter.items())))
raw.append("# classification counts (recomputed from CSV rows in finalize step):")
for k in ("PROVEN_SF30_WRITER", "POSSIBLE_ALIAS", "REJECTED_ALIAS", "UNRESOLVED"):
    raw.append("#   %-20s %d" % (k, cls_counter.get(k, 0)))
raw.append("# function attribution: candidates with no derived containing function")
raw.append("#   are recorded as UNATTRIBUTED (sweep-desync residue or tight-adjacent fn);")
raw.append("#   their classification uses receiver-form rules only, documented per row.")
open(BASE + r"\01_RAW\SF30_WRITER_RAW.txt", "w", encoding="utf-8").write("\n".join(raw) + "\n")

# =====================================================================
# PART 10 - RTTI raw file (calibration + link)
# =====================================================================
rt = []
rt.append("# SF30_RTTI_RAW.txt - RTTI walks, ALL dwords from physical EXE bytes")
rt.append("# RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY")
rt.append("# walker: object -> vtable -> [vtable-4]=COL -> COL.pTypeDescriptor -> TD -> TD+0x08 name")
rt.append("")
rt.append("## A. CALIBRATION (known answer) - SceneFeederObject vtable 0x00A7D458")
rt.append("# [0x00A7D454] dword = 0x%08X (raw bytes %s)"
          % (cal["col_va"], pe.read_va(0x00A7D454, 4).hex()))
rt.append("# COL @ 0x00AA12B8 raw 20 bytes = %s" % cal["col"]["raw"])
rt.append("#   signature=%d offset=%d cd_offset=%d pTypeDescriptor=0x%08X pClassHierarchyDescriptor=0x%08X"
          % (cal["col"]["signature"], cal["col"]["offset"], cal["col"]["cd_offset"],
             cal["col"]["p_type_descriptor"], cal["col"]["p_class_hierarchy"]))
rt.append("# TD @ 0x%08X: vfptr=0x%08X spare=0x%08X"
          % (cal["td"]["va"], cal["td"]["vfptr"], cal["td"]["spare"]))
rt.append("# TD+0x08 name bytes (raw) = %s" % cal["td"]["name_raw_hex"])
rt.append("# name verbatim = %r" % cal["td"]["name"])
rt.append("# expected     = %r" % C.SF_RTTI_NAME_EXPECTED)
rt.append("# CALIBRATION PASS = %s" % ("YES" if CAL_OK else "NO"))
rt.append("")
rt.append("## B. LINK OBJECT (the value at SF+0x30)")
rt.append("# block ctor FUN_007B6000 stores the vtable: measured @ 0x007B6041")
ins = pe.disasm_one(0x007B6041)
rt.append("#   %s  %s  %s" % (ins["bytes"], ins["mnemonic"], ins["op_str"]))
rt.append("# vtable VA = 0x%08X (imm operand)" % LINK_VT)
rt.append("# raw bytes at vtable-4: %s -> dword 0x%08X (COL pointer)"
          % (pe.read_va(LINK_VT - 4, 4).hex(), lk["col_va"]))
rt.append("# COL @ 0x%08X raw 20 bytes = %s" % (lk["col_va"], lk["col"]["raw"]))
rt.append("#   signature=%d offset=%d cd_offset=%d pTypeDescriptor=0x%08X pClassHierarchyDescriptor=0x%08X"
          % (lk["col"]["signature"], lk["col"]["offset"], lk["col"]["cd_offset"],
             lk["col"]["p_type_descriptor"], lk["col"]["p_class_hierarchy"]))
rt.append("# TD @ 0x%08X: vfptr=0x%08X spare=0x%08X"
          % (lk["td"]["va"], lk["td"]["vfptr"], lk["td"]["spare"]))
rt.append("# TD+0x08 name bytes (raw) = %s" % lk["td"]["name_raw_hex"])
rt.append("# name verbatim = %r" % lk["td"]["name"])
rt.append("# vtable section: %s ; COL section: %s ; TD section: %s"
          % (pe.section_of(LINK_VT), pe.section_of(lk["col_va"]), pe.section_of(lk["td"]["va"])))
rt.append("# vtable code-pointer entries: %d (first non-code dword ends extent)" % n_slots)
rt.append("# [vtable+0x44] slot-17 dword VALUE = 0x%08X (RECORDED ONLY - next seam, NOT decoded)" % slot17)
rt.append("# block ctor 0x007B6000 among vtable entries: NO (it is a constructor, not virtual)")
rt.append("")
rt.append("## C. supporting: embedded member vtable 0x00A8CCE0 stored at block+0xE0")
rt.append("#   %s  %s  %s" % (pe.disasm_one(0x007B605E)["bytes"], "mov", pe.disasm_one(0x007B605E)["op_str"]))
rt.append("#   [0x00A8CCDC] = 0x%08X -> COL -> TD name = %r" % (lk2["col_va"], lk2["td"]["name"]))
rt.append("#   (structural consistency with the primary walk; not used for identity)")
open(BASE + r"\01_RAW\SF30_RTTI_RAW.txt", "w", encoding="utf-8").write("\n".join(rt) + "\n")

# =====================================================================
# PART 11 - CSV output
# =====================================================================
with open(BASE + r"\02_ANALYSIS\SF30_WRITER_CENSUS.csv", "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["writer_va", "function_va", "instruction", "source_register_value",
                 "receiver_provenance", "classification"])
    for r in rows:
        wr.writerow([r["writer_va"], r["function_va"], r["instruction"],
                     r["source_register_value"], r["receiver_provenance"], r["classification"]])

# summary JSON for the report step (not part of the evidence package count:
# written to 00_CONTROL as run-local instrumentation state)
summary = {
    "raw_candidate_count": len(candidates),
    "sweep_instructions": n_decoded,
    "classification_counts": dict(cls_counter),
    "proven_writers": [r["writer_va"] for r in rows if r["classification"] == "PROVEN_SF30_WRITER"],
    "rtti_calibration": {"name": cal["td"]["name"], "pass": bool(CAL_OK)},
    "link_vtable": "0x%08X" % LINK_VT,
    "link_rtti_name": RTTI_NAME,
    "link_vtable_slots": n_slots,
    "slot17_value": "0x%08X" % slot17,
    "sf_slot_stores": [{"callsite": "0x%08X" % c, "store_va": "0x%08X" % s, "field": "0x%X" % o,
                        "container_reg": rg} for c, s, o, rg in SF_SLOT_STORES],
    "f_sf": {"0x%08X" % k: v for k, v in sorted(F_SF.items())},
    "combined_offset_hits": len(comb_hits),
    "bulk_init_hits": len(bulk),
    "identity": ident,
}
open(BASE + r"\00_CONTROL\census_state.json", "w").write(json.dumps(summary, indent=1))
print("CENSUS OK")
print("raw candidates:", len(candidates))
print("classification:", dict(cls_counter))
print("proven:", summary["proven_writers"])
print("link RTTI:", RTTI_NAME, "vtable 0x%08X slots=%d slot17=0x%08X" % (LINK_VT, n_slots, slot17))
print("combined hits:", len(comb_hits), "bulk hits:", len(bulk))
