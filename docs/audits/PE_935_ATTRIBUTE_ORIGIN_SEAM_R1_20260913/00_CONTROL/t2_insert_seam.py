# -*- coding: utf-8 -*-
# PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 — TASK 2: INSERT SEAM of the parameter map.
# Manager: singleton DAT_00BA12E8 (getter FUN_004154F0), ctor FUN_008550C0.
# Map head per contract hint @mgr+0x30/+0x34/+0x38. Find = FUN_00971780,
# resolver FUN_008544D0 (returns [hit+8]).
# T1 found: value ctor FUN_0085B1B0 (MovableObject) has exactly ONE raw caller
# at 0x00528E8D -> that caller is the prime INSERT-seam candidate.
# This script dumps: manager ctor, resolver, find, operator[] candidate,
# key-producer FUN_00457930, attr writer FUN_00845F70, the 0x00528E8D caller
# region, and censuses (raw E8/E9) of the key seam functions.
# STATIC-ONLY. Every VA -> pe_core mapping -> bytes.

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe_core import PE, hexdump

RUN_ID = "PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

DUMPS = [
    ("mgr_ctor_FUN_008550C0", 0x008550C0, 0x120),
    ("mgr_ctor_ctx_FUN_00855080", 0x00855080, 0x50),
    ("resolver_FUN_008544D0", 0x008544D0, 0x80),
    ("resolver_prev_FUN_00854480", 0x00854480, 0x50),
    ("find_FUN_00971780", 0x00971780, 0x100),
    ("opbracket_FUN_009719D0", 0x009719D0, 0x100),
    ("find_region_00971600_00971D00", 0x00971600, 0x700),
    ("keyproducer_FUN_00457930", 0x00457930, 0xC0),
    ("attr_writer_FUN_00845F70", 0x00845F70, 0xC0),
    ("getter_FUN_004154F0", 0x004154F0, 0x60),
    ("value_dtor_slot0_FUN_0085B7F0", 0x0085B7F0, 0x80),
    ("value_dtor_FUN_0085B3A0", 0x0085B3A0, 0x60),
    ("caller_of_ctor_region_00528C00", 0x00528C00, 0x600),
    ("walker_FUN_0085B840", 0x0085B840, 0x80),
    ("walker_FUN_0085B880", 0x0085B880, 0x60),
    ("selector_FUN_008553D0", 0x008553D0, 0x60),
]

CENSUS_TARGETS = {
    "mgr_ctor_FUN_008550C0": 0x008550C0,
    "mgr_getter_FUN_004154F0": 0x004154F0,
    "resolver_FUN_008544D0": 0x008544D0,
    "find_FUN_00971780": 0x00971780,
    "opbracket_FUN_009719D0": 0x009719D0,
    "keyproducer_FUN_00457930": 0x00457930,
    "attr_writer_FUN_00845F70": 0x00845F70,
    "selector_FUN_008553D0": 0x008553D0,
    "walker_FUN_0085B840": 0x0085B840,
    "walker_FUN_0085B860": 0x0085B860,
    "value_ctor_FUN_0085B1B0": 0x0085B1B0,
    "value_dtor_slot0_FUN_0085B7F0": 0x0085B7F0,
    "vfs_reader_FUN_00972DF0": 0x00972DF0,
    "parser_A_FUN_00730c90": 0x00730C90,
    "parser_B_FUN_0094bd30": 0x0094BD30,
    "parser_C_FUN_0094f350": 0x0094F350,
    "readcursor_FUN_00752700": 0x00752700,
    "readcursor_FUN_00752740": 0x00752740,
}

IMM_CENSUS = {
    "mgr_singleton_DAT_00BA12E8": 0x00BA12E8,
    "singleton2_DAT_00BA1260": 0x00BA1260,
    "singleton3_DAT_00BA12EC": 0x00BA12EC,
}

def calls_all(pe, target_va):
    out = []
    tr = pe.text_raw
    base = pe.text_va_start
    for i in range(len(tr) - 5):
        if tr[i] in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", tr, i + 1)[0]
            t = base + i + 5 + rel
            if t == target_va:
                out.append({"op": "E8" if tr[i] == 0xE8 else "E9",
                            "site_va": "0x%08X" % (base + i)})
    return out

def find_func_start(pe, va, back_max=0x2000):
    """Scan back from va for >=3 CC padding run; entry = first byte after."""
    off = pe.va_to_off(va)
    d = pe.data
    lo = max(off - back_max, 0)
    i = off
    while i > lo:
        if d[i] == 0xCC and d[i - 1] == 0xCC and d[i - 2] == 0xCC:
            # start of the CC run scan: walk back to its beginning
            j = i
            while d[j - 1] == 0xCC and j > lo:
                j -= 1
            # entry candidate: after the run, skipping padding/nop alignment
            k = i + 1
            while d[k] == 0xCC:
                k += 1
            return pe.off_to_va(k)
        i -= 1
    return None

def main():
    pe = PE(EXE)
    res = {"run_id": RUN_ID, "stage": "T2_insert_seam", "measured": {}, "errors": []}
    m = res["measured"]

    for name, va, ln in DUMPS:
        m["hex_" + name] = hexdump(pe, va, ln)

    # function containing the sole ctor-caller site 0x00528E8D
    fs = find_func_start(pe, 0x00528E8D)
    m["caller_of_value_ctor_func_start"] = ("0x%08X" % fs) if fs else None
    if fs:
        m["hex_caller_of_value_ctor_full"] = hexdump(pe, fs, 0x00528E8D - fs + 0x200)
        m["census_raw_calls_to_caller_of_ctor"] = calls_all(pe, fs)
        # end of body (CC CC heuristic)
        end_va, body = pe.func_body(fs, maxb=0x4000)
        m["caller_body_end_va"] = ("0x%08X" % end_va) if end_va else None
        m["caller_body_size"] = len(body)
        # all E8/E9 sites + targets within the caller body (for edge census)
        edges = []
        base = fs
        for i in range(len(body) - 5):
            if body[i] in (0xE8, 0xE9):
                rel = struct.unpack_from("<i", body, i + 1)[0]
                t = base + i + 5 + rel
                edges.append({"op": "E8" if body[i] == 0xE8 else "E9",
                              "site_va": "0x%08X" % (base + i),
                              "target": "0x%08X" % t})
        m["caller_call_edges"] = edges

    # raw E8/E9 censuses for seam functions
    cens = {}
    for name, t in sorted(CENSUS_TARGETS.items()):
        cens[name] = calls_all(pe, t)
    m["raw_call_censuses"] = cens

    # imm32 censuses for singletons (users of the manager)
    for name, val in sorted(IMM_CENSUS.items()):
        hits = pe.scan_text_imm32(val)
        ctx = []
        for off in hits:
            va = pe.text_off_to_va(off)
            ctx.append({"va": "0x%08X" % va,
                        "before6": (pe.read_va(va - 6, 6) or b"").hex(),
                        "after4": (pe.read_va(va + 4, 4) or b"").hex()})
        m["imm32_census_" + name] = {"value": "0x%08X" % val, "count": len(hits),
                                     "hits": ctx}

    with open(os.path.join(OUT, "T2_INSERT_SEAM.json"), "w") as f:
        json.dump(res, f, indent=2)

    print("T2 done.")
    print("  caller_of_value_ctor_func_start:", m.get("caller_of_value_ctor_func_start"))
    print("  caller_body_size:", m.get("caller_body_size"),
          "end:", m.get("caller_body_end_va"))
    print("  raw call counts:")
    for name, lst in sorted(cens.items()):
        print("    %-34s %d" % (name, len(lst)))
    for name in IMM_CENSUS:
        print("  imm32 %s: %d hits" % (name, m["imm32_census_" + name]["count"]))

if __name__ == "__main__":
    main()
