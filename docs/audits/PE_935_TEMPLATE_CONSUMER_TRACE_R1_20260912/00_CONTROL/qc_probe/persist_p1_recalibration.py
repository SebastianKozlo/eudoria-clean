#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PERSIST probe (pe-master-auditor, RUN_ID: PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_PERSIST):
P1 RECALIBRATION SCAN of Entropia.exe (EU 9.3.5) — the F1 avatar-hardcode constants.

Own PE parse (DOS->e_lfanew->COFF->Optional->sections), fail-closed SHA assert.
Scans (record every hit with VA + file offset):
  .text:  f9 2d 00 00        imm32 0x2DF9 = 11769   EXPECT: exactly 1 (gate P1)
          b8 f9 2d 00 00     MOV EAX,0x2DF9         EXPECT: 1 @0x00511245 (F1 text)
          b9 2d 00 00        imm32 0x2DB9 = 11705   EXPECT: 0 in .text (negative control)
          ba 2d 00 00        imm32 0x2DBA = 11706   EXPECT: 0 in .text (negative control)
          b8 88 2d 00 00     MOV EAX,0x2D88 = 11656 EXPECT: present @0x006B28F6 (family)
          05 87 2d 00 00     ADD EAX,0x2D87         EXPECT: present @0x006B2922 (computed {11655|11657})
  .rdata: b9 2d 00 00 / ba 2d 00 00 (the u32 table rows for 11705/11706, EXPECT @0x00A85838/0x00A8583C)
  supplementary (INFORMATIONAL ONLY, NOT the GATE-NC predicate — that is chain-scoped
  per qc_D CHAIN dict): whole-.text scan of the 5 template constants imm32.

READ-ONLY on the binary. Writes only:
  00_CONTROL\qc_probe\persist_p1_recalibration_result.json
"""
import hashlib
import json
import os
import struct
import sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\00_CONTROL\qc_probe\persist_p1_recalibration_result.json"
EXPECT_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"

res = {"probe": "persist_p1_recalibration", "errors": []}

with open(EXE, "rb") as f:
    blob = f.read()
sha = hashlib.sha256(blob).hexdigest().upper()
res["exe_sha256"] = sha
res["exe_size"] = len(blob)
if sha != EXPECT_SHA:
    res["errors"].append("SHA256 MISMATCH: %s != %s" % (sha, EXPECT_SHA))
    print("FATAL: SHA mismatch"); print(sha)
    with open(OUT, "w", encoding="utf-8") as f: json.dump(res, f, indent=2)
    sys.exit(2)

e_lfanew = struct.unpack_from("<I", blob, 0x3C)[0]
coff = e_lfanew + 4
n_sec = struct.unpack_from("<H", blob, coff + 2)[0]
size_opt = struct.unpack_from("<H", blob, coff + 16)[0]
opt = coff + 20
image_base = struct.unpack_from("<I", blob, opt + 28)[0]
sections = []
for i in range(n_sec):
    off = opt + size_opt + 40 * i
    name = blob[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", blob, off + 8)
    sections.append({"name": name, "vsize": vsize, "vaddr": vaddr, "rsize": rsize, "rptr": rptr})
res["image_base"] = "0x%08X" % image_base
res["sections"] = [{**s, "vaddr": "0x%08X" % s["vaddr"], "rptr": "0x%X" % s["rptr"]} for s in sections]

text = [s for s in sections if s["name"] == ".text"][0]
rdata = [s for s in sections if s["name"] == ".rdata"][0]


def scan(sec, pattern, label):
    lo = sec["rptr"]
    hi = sec["rptr"] + sec["rsize"]
    body = blob[lo:hi]
    hits = []
    i = body.find(pattern)
    while i >= 0:
        file_off = lo + i
        va = image_base + sec["vaddr"] + i
        ctx = blob[file_off - 4:file_off + 8].hex()
        hits.append({"file_offset": file_off, "va": "0x%08X" % va, "context_hex": ctx})
        i = body.find(pattern, i + 1)
    res.setdefault(label, [])
    res[label] = hits
    return hits


pats = [
    (text, bytes.fromhex("f92d0000"), "text_imm32_0x2DF9_11769"),
    (text, bytes.fromhex("b8f92d0000"), "text_mov_eax_0x2DF9"),
    (text, bytes.fromhex("b92d0000"), "text_imm32_0x2DB9_11705"),
    (text, bytes.fromhex("ba2d0000"), "text_imm32_0x2DBA_11706"),
    (text, bytes.fromhex("b8882d0000"), "text_mov_eax_0x2D88_11656"),
    (text, bytes.fromhex("05872d0000"), "text_add_eax_0x2D87"),
    (rdata, bytes.fromhex("b92d0000"), "rdata_imm32_0x2DB9_11705"),
    (rdata, bytes.fromhex("ba2d0000"), "rdata_imm32_0x2DBA_11706"),
]
for sec, pat, label in pats:
    hits = scan(sec, pat, label)
    print("%-32s hits=%d %s" % (label, len(hits), [h["va"] for h in hits]))

# supplementary informational scan (NOT the gate predicate)
info = {}
for cval, cname in [(296445, "A_4508"), (4508, "id_4508"), (296446, "B_4508"), (126740, "A_4752"), (278453, "A_2249")]:
    hits = scan(text, struct.pack("<I", cval), "info_text_imm32_%d_%s" % (cval, cname))
    info["%d(%s)" % (cval, cname)] = [h["va"] for h in hits]
res["info_whole_text_constants_scan"] = {
    "note": "INFORMATIONAL whole-.text scan; the GATE-NC predicate is chain-scoped (qc_D CHAIN dict, 29 functions, span 0x2000)",
    "hits": info,
}

# gate assertions (fail-closed)
gate = {}
gate["imm32_0x2DF9_exactly_1"] = len(res["text_imm32_0x2DF9_11769"]) == 1
gate["mov_eax_0x2DF9_present"] = len(res["text_mov_eax_0x2DF9"]) == 1
gate["imm32_0x2DB9_text_0"] = len(res["text_imm32_0x2DB9_11705"]) == 0
gate["imm32_0x2DBA_text_0"] = len(res["text_imm32_0x2DBA_11706"]) == 0
gate["family_11656_present"] = len(res["text_mov_eax_0x2D88_11656"]) >= 1
gate["family_add_0x2D87_present"] = len(res["text_add_eax_0x2D87"]) >= 1
gate["rdata_11705_11706_table"] = (
    any(h["va"] == "0x00A85838" for h in res["rdata_imm32_0x2DB9_11705"])
    and any(h["va"] == "0x00A8583C" for h in res["rdata_imm32_0x2DBA_11706"])
)
res["gate"] = gate
for k, v in gate.items():
    print("GATE %-32s %s" % (k, "PASS" if v else "FAIL"))
    if not v:
        res["errors"].append("gate assertion failed: %s" % k)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print("result -> %s" % OUT)
sys.exit(1 if res["errors"] else 0)
