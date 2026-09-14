# -*- coding: utf-8 -*-
# PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 - S2: own capstone decode of all
# six vtable slots from the PHYSICAL EXE. For each slot: full disassembly with
# addresses/bytes, derived body end (RET/padding/next-entry evidence), flagged
# accesses to [reg+0x30/0x34/0x38/0x3C] (script-flagged, executor-adjudicated),
# call census (direct E8 targets / indirect).
# STATIC-ONLY. Output: 01_RAW/SLOT_DISASSEMBLY.txt + 02_ANALYSIS/SLOT_ACCESS_CENSUS.json

import json
import os
import sys

import capstone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_core as core

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "01_RAW")
ANALYSIS = os.path.join(HERE, "..", "02_ANALYSIS")

lines = []
def emit(s=""):
    lines.append(s)
    print(s)

# --- S0 re-verified fail-closed inside this script too --------------------
exe_sha = core.sha256_file(core.EXE_PATH)
assert exe_sha.lower() == core.EXPECTED_SHA256.lower(), "sha mismatch"
assert os.path.getsize(core.EXE_PATH) == core.EXPECTED_SIZE, "size mismatch"
pe = core.PE(core.EXE_PATH)
assert pe.machine == core.EXPECTED_MACHINE and pe.opt_magic == core.EXPECTED_OPT_MAGIC
assert pe.image_base == core.EXPECTED_IMAGE_BASE

# --- re-derive the vtable (independent of s1; same physical source) -------
rtti = pe.rtti_walk(core.VTABLE_VA)
assert rtti["td"]["name"] == core.EXPECTED_RTTI_NAME, "RTTI name mismatch"
slots = []
i = 0
while i < 128:
    val = pe.read_va32(core.VTABLE_VA + 4 * i)
    if val is None or not pe.in_text(val):
        break
    slots.append(val)
    i += 1
assert slots == core.SIX_FUNCS or sorted(slots) == sorted(core.SIX_FUNCS), \
    "vtable content != six contract functions"

FUNCS = {0x0050A460: "FUN_0050A460", 0x005090A0: "FUN_005090A0",
         0x005090B0: "FUN_005090B0", 0x0050A050: "FUN_0050A050",
         0x005090C0: "FUN_005090C0", 0x00509580: "FUN_00509580"}

emit("# OWN DECODE (capstone %s, x86-32) - PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914" % capstone.__version__)
emit("# Source: PHYSICAL EXE %s" % core.EXE_PATH)
emit("# EXE SHA256 (measured): %s" % exe_sha)
emit("# SceneFeederObject vtable @ 0x%08X (RTTI-walk verified in 01_RAW/VTABLE_AND_SLOTS.txt)"
     % core.VTABLE_VA)
emit("# Body end derivation: linear sweep stops at CC CC CC padding / 90 90 90 padding /")
emit("#   next known vtable-entry VA / disasm failure / hard limit. body_end = end of")
emit("#   last real instruction. Terminal RET/JMP + following padding recorded per slot.")
emit("# Access flags below are SCRIPT-FLAGGED candidates ([any-reg + 0x30/0x34/0x38/0x3C]);")
emit("#   the executor adjudicates `this`-register provenance in 02_ANALYSIS.")
emit()

census = []
for slot_index, entry in enumerate(slots):
    others = [v for v in slots if v > entry]
    next_known = min(others) if others else None
    emit("=" * 78)
    emit("# SLOT %d - %s - entry 0x%08X  next_known_vtable_entry=%s"
         % (slot_index, FUNCS[entry], entry,
            ("0x%08X" % next_known) if next_known else "NONE"))
    insns, body_end, stop = pe.derive_body(entry, next_known=next_known, max_bytes=0x2000)
    emit("# body_start=0x%08X  body_end=0x%08X (inclusive end VA = last instruction end)"
         % (entry, body_end))
    emit("# stop_reason=%s @ 0x%08X  body_size=%d"
         % (stop[0], stop[1], body_end - entry))
    pad = pe.read_va(body_end, 16)
    emit("# bytes_after_body(16): %s" % (pad.hex(" ") if pad else "READ_FAIL"))
    # terminal evidence: all RET-family and unconditional JMP
    terminals = [x for x in insns
                 if x["mnemonic"].startswith("ret") or x["mnemonic"] in ("jmp", "iretd")]
    for t in terminals:
        emit("# terminal-candidate: 0x%08X  %s  %s  %s"
             % (t["va"], t["bytes"], t["mnemonic"], t["op_str"]))
    emit("-" * 78)
    slot_rec = {
        "slot_index": slot_index,
        "function": FUNCS[entry],
        "entry": "0x%08X" % entry,
        "body_start": "0x%08X" % entry,
        "body_end": "0x%08X" % body_end,
        "body_size": body_end - entry,
        "stop_reason": stop[0],
        "stop_at": "0x%08X" % stop[1],
        "bytes_after_body_hex": pad.hex(" ") if pad else None,
        "next_known": ("0x%08X" % next_known) if next_known else None,
        "instructions": [],
        "sf_field_hits": [],
        "calls": [],
    }
    for ins in insns:
        emit(core.render_insn(ins))
        rec_i = {"va": "0x%08X" % ins["va"], "bytes": ins["bytes"],
                 "mnemonic": ins["mnemonic"], "op_str": ins["op_str"]}
        if ins["mnemonic"] in ("call", "jmp"):
            rec_i["imm"] = ("0x%08X" % ins["imm"]) if "imm" in ins else None
        slot_rec["instructions"].append(rec_i)
        for m in ins["mem_ops"]:
            if m["disp"] in core.SF_FIELD_DISPS:
                hit = {
                    "va": "0x%08X" % ins["va"], "mnemonic": ins["mnemonic"],
                    "op_str": ins["op_str"], "base": m["base"], "index": m["index"],
                    "disp": "0x%X" % m["disp"], "access": m["access"],
                    "is_lea": ins["mnemonic"] == "lea",
                }
                slot_rec["sf_field_hits"].append(hit)
                emit("#    >> SF-FIELD-HIT disp=%s base=%s access=%s%s"
                     % (hit["disp"], m["base"], m["access"],
                        " (LEA - address-of, no value read)" if hit["is_lea"] else ""))
        if ins["mnemonic"] == "call":
            tgt = ("0x%08X" % ins["imm"]) if "imm" in ins else ("indirect: %s" % ins["op_str"])
            slot_rec["calls"].append({"va": "0x%08X" % ins["va"], "target": tgt})
            emit("#    >> CALL @ 0x%08X -> %s" % (ins["va"], tgt))
    emit()

    census.append(slot_rec)

# ============================ one-hop identification ======================
# Contract dataflow-stop rule: no descent into callees. Allowed one-hop
# resolution ONLY for: real target of a thunk, RTTI of a receiver, trivially
# obvious getter/setter. Below: first bytes (prologue shape), thunk-pattern
# check (FF 25 -> import), direct E8/E9 reference counts (function-start
# evidence for boundary validation). NO callee body decode is performed here.
emit("=" * 78)
emit("# ONE-HOP IDENTIFICATION (no callee body decode - stop rule honored)")
emit("# va, first-16-bytes, thunk-resolve, aligned16, direct E8 callers, direct E9 jumpers")
ONE_HOP = [
    0x0050A240,  # slot 0 callee (thiscall, ecx=this)
    0x0095D42A,  # slot 0 conditional callee (push this)
    0x00437F70,  # slot 3 path-A callee #1
    0x0082B5A0,  # slot 3 path-A callee #2 (thiscall on result)
    0x004150F0,  # slot 5 callee #1
    0x008B71D0,  # slot 5 callee #2 (thiscall on result)
    0x0050A480,  # function immediately after slot 0 true end (boundary check)
    0x0050A0B0,  # function immediately after slot 3 end (boundary check)
    0x005095A0,  # function immediately after slot 5 end (boundary check)
    0x0050A590,  # function after 0x50A480's own ret (context)
]
one_hop = {}
for va in ONE_HOP:
    fb = pe.read_va(va, 16)
    thr = pe.resolve_thunk(va)
    callers = pe.calls_to(va)
    jmps = pe.jumps_to(va)
    rec = {
        "va": "0x%08X" % va,
        "first_bytes": fb.hex(" ") if fb else None,
        "thunk": thr,
        "aligned16": (va % 16 == 0),
        "direct_e8_callers": len(callers),
        "direct_e9_jumpers": len(jmps),
        "sample_caller_vas": ["0x%08X" % c for c in callers[:6]],
    }
    one_hop["0x%08X" % va] = rec
    emit("# 0x%08X bytes=%-47s thunk=%s aligned16=%s E8callers=%d E9jmp=%d sample=%s"
         % (va, (fb.hex(" ") if fb else "?")[:47],
            (thr or "-"), rec["aligned16"], len(callers), len(jmps),
            ",".join("%08X" % c for c in callers[:4])))
emit("# NOTE: 0x50A480 / 0x50A0B0 / 0x5095A0 / 0x50A590 are NOT vtable entries;")
emit("#   their E8 caller counts are function-start evidence for the body-end")
emit("#   boundaries of slots 0/3/5 (padding runs and tight adjacency).")

with open(os.path.join(ANALYSIS, "SLOT_ACCESS_CENSUS.json"), "w") as f:
    json.dump({"census": census, "one_hop": one_hop}, f, indent=1)
with open(os.path.join(RAW, "SLOT_DISASSEMBLY.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
print()
print("WROTE 01_RAW/SLOT_DISASSEMBLY.txt + 02_ANALYSIS/SLOT_ACCESS_CENSUS.json")
