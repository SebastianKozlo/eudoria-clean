# -*- coding: utf-8 -*-
# QC probe 3 — INDEPENDENT SWEEP REPRODUCTION + full CSV-vs-bytes cross-check
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 INTERNAL_QC
# Own implementation of the DOCUMENTED enumeration rule (raw header):
#   linear capstone sweep of full .text; candidate = any decoded insn with a
#   WRITE mem-operand disp==0x30; bad-byte restart = last_end+1.
# Output: 00_CONTROL/qc_probe/out_qc3_sweep.txt
import csv, struct, sys, hashlib

sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
OUT = []

def log(s=""):
    OUT.append(s)
    print(s)

data = open(EXE, "rb").read()
assert hashlib.sha256(data).hexdigest().upper() == "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
lf = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, lf + 6)[0]
opt = lf + 24
optsize = struct.unpack_from("<H", data, lf + 20)[0]
imgbase = struct.unpack_from("<I", data, opt + 28)[0]
secoff = opt + optsize
TEXT = None
for i in range(nsec):
    o = secoff + 40 * i
    nm = data[o:o+8].rstrip(b"\0").decode()
    vs, va, rs, rp = struct.unpack_from("<IIII", data, o + 8)
    if nm == ".text":
        TEXT = (va, vs, rs, rp)
va0, vs0, rs0, rp0 = TEXT
tva = imgbase + va0
tbytes = data[rp0:rp0 + rs0]
log("== QC3 own sweep ==")
log(".text va=0x%08X rsize=0x%X (%d bytes)" % (tva, rs0, len(tbytes)))

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True

pos = 0
n = len(tbytes)
decoded = 0
restarts = 0
cands = []  # (va, base_reg, access_str)
mv = memoryview(tbytes)
while pos < n:
    last_end = pos
    for ins in md.disasm(mv[pos:], tva + pos):
        decoded += 1
        last_end = pos + (ins.address - (tva + pos)) + ins.size
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
                cands.append((ins.address, ins.mnemonic, ins.op_str))
                break
    if last_end >= n:
        break
    pos = last_end + 1
    restarts += 1

log("sweep: instructions decoded=%d restarts=%d" % (decoded, restarts))
log("raw candidates (write-mem disp==0x30): %d" % len(cands))
log("claim (raw header): decoded=2266698 restarts=64 candidates=3643")
log("reproduction: decoded %s, restarts %s, candidates %s"
    % (decoded == 2266698, restarts == 64, len(cands) == 3643))

# --- full CSV-vs-bytes cross-check -------------------------------------------
rows = list(csv.DictReader(open(PKG + r"\02_ANALYSIS\SF30_WRITER_CENSUS.csv")))
log("")
log("== full CSV vs own decode of every candidate row ==")
csv_by_va = {r["writer_va"]: r for r in rows}
mism_ins = []
mism_form = []
forms = {}
for va, mn, ops in cands:
    key = "0x%08X" % va
    r = csv_by_va.get(key)
    if r is None:
        mism_form.append(("CSV row missing for candidate %s" % key))
        continue
    if (r["instruction"] != "%s %s" % (mn, ops)):
        mism_ins.append((key, r["instruction"], "%s %s" % (mn, ops)))
extra = [r["writer_va"] for r in rows if r["writer_va"] not in {"0x%08X" % v for v, _m, _o in cands}]
log("rows whose instruction text differs from my own decode: %d %s"
    % (len(mism_ins), mism_ins[:5] if mism_ins else ""))
log("CSV rows that are NOT in my candidate set: %d %s" % (len(extra), extra[:5]))
log("my candidates missing a CSV row: %d" % len(mism_form))

# form census over my candidates
md2 = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md2.detail = True
from collections import Counter
formc = Counter()
bregc = Counter()
for va, mn, ops in cands:
    b = data[rp0 + (va - tva):rp0 + (va - tva) + 16]
    ins = next(md2.disasm(b, va))
    for op in ins.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
            bregc[ins.reg_name(op.mem.base) if op.mem.base else "(none)"] += 1
            formc["%s+%s" % (ins.mnemonic, "idx" if op.mem.index else ("disp%d" % (8 if ins.size <= 4 else 32)))] += 1
            break
log("")
log("== my candidate base-register distribution ==")
log(", ".join("%s=%d" % (k, v) for k, v in sorted(bregc.items())))
log("claim: eax=80, ebp=25, ebx=24, ecx=30, edi=76, edx=6, esi=637, esp=2765 (sum 3643)")
log("== my candidate mnemonic-form distribution ==")
for k, v in sorted(formc.items(), key=lambda x: -x[1]):
    log("  %-28s %d" % (k, v))
# forms with no base register?
log("candidates with no base register: %d" % bregc.get("(none)", 0))

# UNATTRIBUTED rows check
log("")
log("== UNATTRIBUTED rows (15 per QC1) ==")
for r in rows:
    if r["function_va"] == "UNATTRIBUTED":
        log("  %s %s class=%s srcval=%r recv=%r" % (r["writer_va"], r["instruction"], r["classification"], r["source_register_value"], r["receiver_provenance"]))

open(PKG + r"\00_CONTROL\qc_probe\out_qc3_sweep.txt", "w").write("\n".join(OUT) + "\n")
log("")
log("QC3 DONE")
