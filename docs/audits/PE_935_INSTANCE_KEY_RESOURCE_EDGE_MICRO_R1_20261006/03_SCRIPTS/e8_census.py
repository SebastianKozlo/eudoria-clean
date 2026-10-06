# e8_census.py - inventory of direct E8 references to FUN_00414130 (the getter).
# ENUMERATION METHOD (contract s3.1):
#   1) Linear byte scan of the raw file image of .text [0x00401000..0x00A75000)
#      (range = the pinned .text raw_size; full-section, no gaps skipped):
#      every offset o with raw[o]==0xE8 is a RAW candidate; the computed
#      target = va(o)+5+int32(raw[o+1:o+5]); a hit is a candidate whose
#      computed target == 0x00414130. NO exclusions at the raw stage - every
#      hit is recorded (candidates can be immediates/operands inside other
#      instructions; classification is separate and honest).
#   2) The same scan over the WHOLE FILE (all sections + headers) to report
#      raw E8-pattern hits outside .text (non-instruction bytes).
#   3) Absolute dword census: every file offset where the 4-byte little-endian
#      value == 0x00414130 (address-taker/alias candidates).
#   4) E9 (JMP-thunk alias) census: same method as (1) with 0xE9.
#   5) Recompute targets for the published xrefs from BASE reports
#      (0x00528FD9 in FUN_00528E50; 0x008561AC in FUN_00856190).
# NOT CLAIMED COVERED: indirect calls (call reg / call [mem]), inlined reads
# of [this+0x74], and any other alias forms - stated, not silently dropped.

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe935k_core import Exe, hexs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_RAW")
os.makedirs(OUT, exist_ok=True)

TARGET = 0x00414130
ex = Exe()
text_lo, text_hi = ex.text_range()
t_off_lo = ex.va_to_off(text_lo)
t_off_hi = t_off_lo + (text_hi - text_lo)

raw = ex.raw

def scan_pattern(byte, target, lo, hi):
    hits = []
    for o in range(lo, hi - 4):
        if raw[o] == byte:
            va = text_lo + (o - t_off_lo)
            rel = struct.unpack_from("<i", raw, o + 1)[0]
            tgt = (va + 5 + rel) & 0xFFFFFFFF
            if tgt == target:
                hits.append({
                    "file_offset": "0x%X" % o,
                    "opcode_va": "0x%08X" % va,
                    "rel32": "0x%08X" % (rel & 0xFFFFFFFF),
                    "rel32_signed": rel,
                    "computed_target": "0x%08X" % tgt,
                    "bytes_hex": hexs(raw[o:o + 5]),
                })
    return hits

e8_hits = scan_pattern(0xE8, TARGET, t_off_lo, t_off_hi)

# whole-file E8-pattern census (outside .text)
whole = []
for o in range(0, len(raw) - 4):
    if raw[o] == 0xE8:
        rel = struct.unpack_from("<i", raw, o + 1)[0]
        # absolute VA interpretation only valid for file-image bytes of .text;
        # for other sections record the raw file offset + rel32 pattern only
        if o < t_off_lo or o >= t_off_hi:
            if ((0x00401000 + 5 + rel) & 0xFFFFFFFF) == TARGET:
                sec = None
                for s in ex.sections:
                    if s["raw_pointer"] <= o < s["raw_pointer"] + s["raw_size"]:
                        sec = s["name"]
                if sec is None:
                    sec = "header/overlay"
                whole.append({"file_offset": "0x%X" % o, "section": sec,
                              "rel32": "0x%08X" % (rel & 0xFFFFFFFF)})

# absolute dword census of 0x00414130
dword_hits = []
needle = struct.pack("<I", TARGET)
i = raw.find(needle)
while i != -1:
    sec = None
    for s in ex.sections:
        if s["raw_pointer"] <= i < s["raw_pointer"] + s["raw_size"]:
            sec = s["name"]
    if sec is None:
        sec = "header/overlay"
    va = None
    for s in ex.sections:
        if s["name"] == ".text" and t_off_lo <= i < t_off_hi:
            va = text_lo + (i - t_off_lo)
    dword_hits.append({"file_offset": "0x%X" % i, "section": sec,
                       "va_if_text": ("0x%08X" % va) if va else None})
    i = raw.find(needle, i + 1)

# E9 JMP-thunk alias census in .text
e9_hits = scan_pattern(0xE9, TARGET, t_off_lo, t_off_hi)

# recompute published xref targets
published = [
    {"xref": "0x00528FD9", "claimed_in": "FUN_00528E50 (BASE PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 REPORT s4.1)"},
    {"xref": "0x008561AC", "claimed_in": "FUN_00856190 (BASE PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 REPORT S10 + RESEARCH_FINDINGS L49)"},
]
for p in published:
    va = int(p["xref"], 16)
    off = ex.va_to_off(va)
    if off is None or raw[off] != 0xE8:
        p["recomputed_target"] = None
        p["recompute_result"] = "E8-byte mismatch or unresolvable offset"
        continue
    rel = struct.unpack_from("<i", raw, off + 1)[0]
    tgt = (va + 5 + rel) & 0xFFFFFFFF
    p["recomputed_target"] = "0x%08X" % tgt
    p["recompute_result"] = "MATCH" if tgt == TARGET else "MISMATCH"
    p["bytes_hex"] = hexs(raw[off:off + 5])

result = {
    "measurement": "E8/E9/dword census for direct references to 0x00414130",
    "text_range": ["0x%08X" % text_lo, "0x%08X" % text_hi],
    "method": ("linear byte scan, every E8/E9 byte in .text raw image considered, "
               "target=va+5+rel32 signed; raw hits include non-instruction bytes; "
               "no exclusions at raw stage; indirect calls/inlining/other alias forms "
               "NOT claimed covered"),
    "e8_hits_in_text": e8_hits,
    "e8_pattern_hits_outside_text": whole,
    "e9_jmp_thunk_hits_in_text": e9_hits,
    "absolute_dword_hits_of_0x00414130": dword_hits,
    "published_xref_recompute": published,
    "counts": {
        "e8_hits_in_text": len(e8_hits),
        "e8_pattern_hits_outside_text": len(whole),
        "e9_hits_in_text": len(e9_hits),
        "absolute_dword_hits": len(dword_hits),
    },
}

with open(os.path.join(OUT, "E8_CENSUS.json"), "w") as f:
    json.dump(result, f, indent=1)

print("E8 hits in .text targeting 0x00414130: %d" % len(e8_hits))
for h in e8_hits:
    print("  opcode@%s rel32=%s bytes[%s]" % (h["opcode_va"], h["rel32"], h["bytes_hex"]))
print("E8-pattern hits outside .text: %d" % len(whole))
print("E9 JMP-thunk hits in .text: %d" % len(e9_hits))
for h in e9_hits:
    print("  opcode@%s bytes[%s]" % (h["opcode_va"], h["bytes_hex"]))
print("absolute dword 0x00414130 occurrences: %d" % len(dword_hits))
for h in dword_hits:
    print("  off=%s sec=%s va_if_text=%s" % (h["file_offset"], h["section"], h["va_if_text"]))
print("published xref recomputation:")
for p in published:
    print("  %s -> %s (%s)" % (p["xref"], p.get("recomputed_target"), p["recompute_result"]))
