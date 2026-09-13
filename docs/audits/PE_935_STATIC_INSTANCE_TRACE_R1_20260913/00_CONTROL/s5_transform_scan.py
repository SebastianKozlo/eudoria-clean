# -*- coding: utf-8 -*-
# PE_935_STATIC_INSTANCE_TRACE_R1_20260913 — S5 TRANSFORM-WRITE PATTERN SCAN
# STATIC-ONLY raw scan of .text for NiAVObject transform write patterns
# (offsets from VA-locked oracle FUN_007c04f0 = NiAVObject::GetViewerStrings):
#   m_kLocal.m_Translate @ +0x5C,+0x60,+0x64   (SetTranslate)
#   m_kWorld.m_Translate @ +0x90,+0x94,+0x98   (SetWorldTranslate)
#   m_kLocal.m_Rotate   @ +0x38..+0x58 (9f)    (SetRotate)
#   m_kLocal.m_fScale   @ +0x68                 (SetScale)
# Scan for:
#   A) three consecutive dword stores [reg+0x5C],[reg+0x60],[reg+0x64]
#      forms: 89 /r with disp8 (89 4X YY) and disp32 (89 8X YY 00 00 00),
#             FSTP (D9 5X YY / D9 9X YY 00 00 00), MOVSS (F3 0F 11 /r)
#   B) same for +0x90/+0x94/+0x98
#   C) 9-store runs to +0x38..+0x58 (rotate)
# Output: 01_RAW/S5_TRANSFORM_WRITES.json with VA + hex context.

import json
import os
import re
import struct

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913"
OUT = os.path.join(RUN_ROOT, "01_RAW")
EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"

def main():
    data = open(EXE, "rb").read()
    text_off, text_len = 4096, 6766592
    text = data[text_off:text_off + text_len]

    def va(off_in_text):
        return 0x00401000 + off_in_text

    results = {"local_translate_triples": [], "world_translate_triples": [],
               "rotate_runs": [], "scale_writes": []}

    # ---- A/B: triple stores ----
    # mov [reg+disp8], reg : 89 4X disp8  (mod=01, rm=reg base)
    def find_triples(base_disp, label, bucket):
        # we look for three stores with disp8 base_disp, +4, +8 whose bytes
        # appear within a window of 24 bytes, sharing the same rm (base reg)
        for i in range(len(text) - 24):
            w = text[i:i+24]
            # find pattern 89 4X d1 ... 89 4Y d2 ... 89 4Z d3 with d1=base d2=+4 d3=+8
            # and rm bits of 4X/4Y/4Z equal (mod=01 => rm 0-7, disp8)
            # simple regexes over the window with same rm:
            found = None
            for rm in range(8):
                p1 = bytes([0x89, 0x40 | rm, base_disp & 0xFF])
                j = w.find(p1)
                if j < 0:
                    continue
                w2 = w[j:j+24-j]
                p2 = bytes([0x89, 0x40 | rm, (base_disp + 4) & 0xFF])
                k = w.find(p2, j + 3)
                if k < 0:
                    continue
                p3 = bytes([0x89, 0x40 | rm, (base_disp + 8) & 0xFF])
                m = w.find(p3, k + 3)
                if m < 0:
                    continue
                found = (j, k, m, rm)
                break
            if found:
                j, k, m, rm = found
                results[bucket].append({
                    "va": "0x%08X" % va(i),
                    "first_store_va": "0x%08X" % va(i + j),
                    "rm": rm,
                    "window_hex": " ".join("%02x" % b for b in w[:24]),
                })
        # dedupe overlapping (keep first of each cluster)
        dedup = []
        last = -100
        for r in results[bucket]:
            o = int(r["va"], 16)
            if o - last < 24:
                continue
            dedup.append(r)
            last = o
        results[bucket] = dedup

    find_triples(0x5C, "local", "local_translate_triples")
    find_triples(0x90, "world", "world_translate_triples")

    # ---- D: FSTP triple to +0x5C (D9 5X disp8) ----
    fstp_hits = []
    for i in range(len(text) - 3):
        b = text[i]
        if b == 0xD9 and (text[i+1] & 0xF8) == 0x50:  # FSTP [reg+disp8]
            disp = text[i+2]
            if disp in (0x5C, 0x90):
                fstp_hits.append({"va": "0x%08X" % va(i), "disp": disp,
                                   "hex": " ".join("%02x" % x for x in text[i:i+6])})
    results["fstp_store_hits"] = fstp_hits

    # ---- C: rotate runs: 9 consecutive disp8 stores +0x38..+0x58 with stride 4 ----
    # quick heuristic: functions containing >= 5 stores of the form 89 4X disp with
    # disp in {0x38..0x58 step 4} same rm; scan windows of 64 bytes
    rot = []
    for i in range(0, len(text) - 64, 1):
        w = text[i:i+64]
        for rm in range(8):
            cnt = 0
            for d in range(0x38, 0x5C, 4):
                if bytes([0x89, 0x40 | rm, d]) in w:
                    cnt += 1
            if cnt >= 5:
                rot.append({"va": "0x%08X" % va(i), "rm": rm, "count": cnt,
                            "window_hex": " ".join("%02x" % b for b in w[:64])})
                break
        if len(rot) > 400:
            break
    # dedupe
    dedup = []
    last = -100
    for r in rot:
        o = int(r["va"], 16)
        if o - last < 64:
            continue
        dedup.append(r)
        last = o
    results["rotate_runs"] = dedup

    with open(os.path.join(OUT, "S5_TRANSFORM_WRITES.json"), "w") as f:
        json.dump({"run_id": "PE_935_STATIC_INSTANCE_TRACE_R1_20260913",
                   "stage": "S5_transform_write_scan",
                   "note": "offsets from VA-locked NiAVObject oracle (FUN_007c04f0 GetViewerStrings)",
                   "results": results}, f, indent=2)

    print("S5_DONE local_triples=%d world_triples=%d fstp=%d rotate_runs=%d" % (
        len(results["local_translate_triples"]), len(results["world_translate_triples"]),
        len(results["fstp_store_hits"]), len(results["rotate_runs"])))
    for r in results["local_translate_triples"][:20]:
        print("  LOC %s rm=%d %s" % (r["first_store_va"], r["rm"], r["window_hex"][:47]))
    for r in results["world_translate_triples"][:20]:
        print("  WLD %s rm=%d %s" % (r["first_store_va"], r["rm"], r["window_hex"][:47]))

if __name__ == "__main__":
    main()
