#!/usr/bin/env python3
# FRESH INTERNAL QC - debug extraction: compare sec_for_fo and verify_pin bodies
# precisely (exact line ranges from the full source reads).
import sys
sys.dont_write_bytecode = True

import difflib
import json

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC3 = PKG + r"\04_QC\QC_R3_DESKTOP_CORRECTION\qc_tools\qc3_q1_pinverify.py"
QC4 = PKG + r"\04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_q1_pinverify.py"

with open(QC3, encoding="utf-8") as f:
    l3 = f.read().splitlines()
with open(QC4, encoding="utf-8") as f:
    l4 = f.read().splitlines()

# sec_for_fo: qc3 L18-22 (1-based); qc4 L90-95 (1-based)
s3 = l3[17:22]
s4 = l4[89:95]
print("sec_for_fo qc3 (L18-22):", json.dumps(s3))
print("sec_for_fo qc4 (L90-95):", json.dumps(s4))
print("sec_for_fo IDENTICAL (line-slice):", s3 == s4)
print()
# verify_pin: qc3 L24-45 (1-based); qc4 L97-118 (1-based)
v3 = l3[23:45]
v4 = l4[96:118]
print("verify_pin qc3 L24-45 == qc4 L97-118:", v3 == v4)
if v3 != v4:
    for d in difflib.unified_diff(v3, v4, "qc3", "qc4", lineterm=""):
        print(d)
print()
# also dump what the naive body() extraction produced, to explain the earlier false
def body(src, marker):
    i = src.index(marker)
    j = src.index("def ", i + len(marker))
    return src[i:j]
qc3src = "\n".join(l3)
qc4src = "\n".join(l4)
s3n = body(qc3src, "def sec_for_fo(fo):")
s4n = body(qc4src, "def sec_for_fo(fo):")
print("naive sec_for_fo qc3 len:", len(s3n), "tail-40:", json.dumps(s3n[-40:]))
print("naive sec_for_fo qc4 len:", len(s4n), "tail-40:", json.dumps(s4n[-40:]))
