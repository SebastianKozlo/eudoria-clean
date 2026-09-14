# -*- coding: utf-8 -*-
# QC probe 4 — POSSIBLE_ALIAS/REJECTED sampling (own traces), scope census,
# follow-up byte checks (block ctor entry, 0x529020 site, ebp/esi redefinition,
# rep movsd targets, combined-offset rescan at container fns).
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 INTERNAL_QC
# Output: 00_CONTROL/qc_probe/out_qc4_sample_scope.txt
import csv, os, re, struct, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone

def log(s=""):
    OUT.append(s)
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode())

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
OUT = []

def log(s=""):
    OUT.append(s)
    print(s)

data = open(EXE, "rb").read()
lf = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, lf + 6)[0]
opt = lf + 24
optsize = struct.unpack_from("<H", data, lf + 20)[0]
imgbase = struct.unpack_from("<I", data, opt + 28)[0]
secoff = opt + optsize
SECS = []
for i in range(nsec):
    o = secoff + 40 * i
    nm = data[o:o+8].rstrip(b"\0").decode()
    vs, va, rs, rp = struct.unpack_from("<IIII", data, o + 8)
    SECS.append((nm, va, vs, rs, rp))
TXT = None
for nm, va, vs, rs, rp in SECS:
    if nm == ".text":
        TXT = (va, rs, rp)
tva = imgbase + TXT[0]

def off_of(va):
    rva = va - imgbase
    for nm, sva, vs, rs, rp in SECS:
        if sva <= rva < sva + rs:
            return rp + (rva - sva)
    return None

def rd(va, n):
    o = off_of(va)
    return None if o is None else data[o:o+n]

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True

def dec_at(va, n=16):
    b = rd(va, n)
    if b is None:
        return None
    try:
        i = next(md.disasm(b, va))
        return (i.address, i.size, i.bytes.hex(), i.mnemonic, i.op_str)
    except StopIteration:
        return None

def dec_range(va, n):
    out = []
    b = rd(va, n)
    if b is None:
        return out
    for i in md.disasm(b, va):
        out.append((i.address, i.size, i.bytes.hex(), i.mnemonic, i.op_str))
    return out

rows = list(csv.DictReader(open(PKG + r"\02_ANALYSIS\SF30_WRITER_CENSUS.csv")))
raw = open(PKG + r"\01_RAW\SF30_WRITER_RAW.txt", encoding="utf-8", errors="replace").read()

# ================= PART A: POSSIBLE_ALIAS sampling ==============================
poss = [r for r in rows if r["classification"] == "POSSIBLE_ALIAS"]
log("== A: POSSIBLE_ALIAS population ==")
from collections import Counter
fn_of_poss = Counter(r["function_va"] for r in poss)
log("POSSIBLE rows: %d, distinct functions: %d" % (len(poss), len(fn_of_poss)))
log("top functions by POSSIBLE count: %s" % fn_of_poss.most_common(8))
F_SF = {0x0044D590, 0x0047CCF0, 0x005090A0, 0x005090B0, 0x005090C0, 0x00509330,
        0x005094C0, 0x005094E0, 0x00509580, 0x00509670, 0x00509F00, 0x0050A050,
        0x0050A240, 0x0050A460, 0x005247C0, 0x00528E50, 0x0067B800, 0x0067C7C0, 0x006A3930}
in_fsf = [r for r in poss if r["function_va"] != "UNATTRIBUTED" and int(r["function_va"], 16) in F_SF]
log("POSSIBLE rows inside the 19 F_SF functions: %d" % len(in_fsf))
for r in in_fsf:
    log("   %s %s fn=%s recv=%r" % (r["writer_va"], r["instruction"], r["function_va"], r["receiver_provenance"]))
rej_fsf = [r for r in rows if r["classification"] == "REJECTED_ALIAS" and r["function_va"] != "UNATTRIBUTED" and int(r["function_va"], 16) in F_SF]
log("REJECTED rows inside F_SF functions: %d" % len(rej_fsf))
for r in rej_fsf:
    log("   %s %s fn=%s recv=%r" % (r["writer_va"], r["instruction"], r["function_va"], r["receiver_provenance"]))

# deterministic sample: spread across the address space + different functions
sample_fns = []
for fn, cnt in fn_of_poss.most_common():
    if fn not in ("UNATTRIBUTED",):
        sample_fns.append((fn, cnt))
picked = []
seen_fn = set()
# pick 12 rows: the first row of up to 12 distinct functions, spread across VAs
step = max(1, len(poss) // 12)
for idx in range(0, len(poss), step):
    r = poss[idx]
    if r["function_va"] not in seen_fn:
        seen_fn.add(r["function_va"])
        picked.append(r)
    if len(picked) >= 12:
        break

log("")
log("== A2: my own receiver traces for %d sampled POSSIBLE_ALIAS rows ==" % len(picked))
for r in picked:
    va = int(r["writer_va"], 16)
    i = dec_at(va)
    # extract base register from instruction
    m = re.match(r"[\w ]*\[[a-z]{3}(?: \+ 0x30)?\]", r["instruction"])
    log("-- %s fn=%s ins='%s' recv=%r" % (r["writer_va"], r["function_va"], r["instruction"], r["receiver_provenance"]))
    # decode a window before the candidate: 24 bytes, find the last def of base reg
    # use aligned linear decode backwards heuristically: decode from va-0x18 (may misalign;
    # anchor on the candidate and decode forward-only window context instead)
    ctx = dec_range(va - 0x18, 0x18 + (i[1] if i else 6))
    lastdef = []
    basereg = None
    if i:
        for opnd in md.disasm(bytes.fromhex(""), va):  # placeholder never used
            break
    # find base register by re-decoding with detail
    b = rd(va, 16)
    ins = next(md.disasm(b, va))
    for op in ins.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
            basereg = ins.reg_name(op.mem.base) if op.mem.base else None
    log("   base reg: %s" % basereg)
    # backward textual search in ctx for a def of basereg
    for c in ctx:
        if c[4].startswith((basereg + ",").upper()) or c[4].startswith(basereg + ","):
            lastdef.append("%08X %s %s" % (c[0], c[3], c[4]))
    log("   aligned-ish defs in the 24-byte window before: %s" % (lastdef if lastdef else "none seen (window may be misaligned)"))
    # cross-check with the raw block for this row
    blk = raw.split("### " + r["writer_va"] + " ", 1)[1].split("### 0x", 1)[0] if ("### " + r["writer_va"] + " ") in raw else ""
    why = re.search(r"why: (.+)", blk)
    log("   raw why: %s" % (why.group(1)[:160] if why else "NOT FOUND"))

# ================= PART B: REJECTED_ALIAS sampling across reasons ==================
log("")
log("== B: REJECTED_ALIAS reason taxonomy census (from raw 'why:' lines) ==")
reasons = Counter()
for r in rows:
    if r["classification"] != "REJECTED_ALIAS":
        continue
    blk = raw.split("### " + r["writer_va"] + " ", 1)
    why = ""
    if len(blk) > 1:
        m = re.search(r"why: (R-[A-Z-]+)", blk[1])
        if m:
            why = m.group(1)
    reasons[why or "?"] += 1
for k, v in reasons.most_common():
    log("  %-18s %d" % (k, v))

# sample 2 rows per reason and verify the rejection against my own window decode
log("")
log("== B2: my own verification of sampled REJECTED rows ==")
done = Counter()
for r in rows:
    if r["classification"] != "REJECTED_ALIAS":
        continue
    va = int(r["writer_va"], 16)
    blk = raw.split("### " + r["writer_va"] + " ", 1)
    why = ""
    if len(blk) > 1:
        m = re.search(r"why: (R-[A-Z-]+)", blk[1])
        if m:
            why = m.group(1)
    if not why or done[why] >= 2:
        continue
    done[why] += 1
    i = dec_at(va)
    b = rd(va, 16)
    ins = next(md.disasm(b, va))
    basereg = None
    for op in ins.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
            basereg = ins.reg_name(op.mem.base) if op.mem.base else None
    log("  %s %s base=%s reason=%s recv=%r" % (r["writer_va"], r["instruction"], basereg, why, r["receiver_provenance"]))
    # for R-IMM-STATIC / R-ZERO / R-LEA-STACK / R-STACK-PTR verify the defining insn near the window
    ctx = dec_range(va - 0x18, 0x30)
    for c in ctx:
        if c[4].startswith((basereg or "~~") + ","):
            log("      window def: %08X %s %s" % (c[0], c[3], c[4]))

# ================= PART C: scope census (own) =====================================
log("")
log("== C: scope census over the executor package ==")
EXE_PKG_FILES = [
    "00_CONTROL/RUN_CONTRACT.md", "00_CONTROL/SCRIPT_SHA256.csv", "00_CONTROL/SOURCE_IDENTITIES.json",
    "00_CONTROL/census.py", "00_CONTROL/census_state.json", "00_CONTROL/finalize.py", "00_CONTROL/sf30_core.py",
    "01_RAW/POSITIVE_CONTROL_0050A050.txt", "01_RAW/SF30_RTTI_RAW.txt", "01_RAW/SF30_WRITER_RAW.txt",
    "02_ANALYSIS/SF30_PROVENANCE.md", "02_ANALYSIS/SF30_WRITER_CENSUS.csv", "03_EVIDENCE/README.md",
    "06_REPORT/HANDOFF.md", "06_REPORT/MANIFEST_SHA256.csv", "06_REPORT/REPORT.md",
    "06_REPORT/STAGE_ACCEPTANCE_GATES.csv",
]
labels = ["MODEL_BRIDGE_CONFIRMED", "TRANSFORM_TO_MODEL"]
for rel in EXE_PKG_FILES:
    t = open(os.path.join(PKG, rel.replace("/", "\\")), encoding="utf-8", errors="replace").read()
    for lab in labels:
        for ln_no, line in enumerate(t.splitlines(), 1):
            if lab in line:
                # my own claim-context rule: a claim = a line asserting the outcome
                is_neg = bool(re.search(r"NOT_DEMONSTRATED|not made|no MODEL_BRIDGE|no TRANSFORM|remains|zero|forbidden|NOT claimed|not decode|no claim", line, re.I))
                log("  %-40s:%d %s neg=%s :: %s" % (rel, ln_no, lab, is_neg, line.strip()[:150]))
old_wrong = re.compile(r"26 package files|25 manifest rows|26/25")
found_old = False
for rel in EXE_PKG_FILES:
    t = open(os.path.join(PKG, rel.replace("/", "\\")), encoding="utf-8", errors="replace").read()
    for ln_no, line in enumerate(t.splitlines(), 1):
        if old_wrong.search(line):
            log("  OLD-WRONG-FIGURES %s:%d :: %s" % (rel, ln_no, line.strip()[:150]))
            found_old = True
log("old wrong 26/25 figures present: %s" % ("YES - FINDING" if found_old else "no (good)"))
# 0x437F70 / 0x82B5A0 / 0x007B5390 occurrences with contexts
log("")
log("  forbidden-VA textual occurrences:")
for rel in EXE_PKG_FILES:
    t = open(os.path.join(PKG, rel.replace("/", "\\")), encoding="utf-8", errors="replace").read()
    for ln_no, line in enumerate(t.splitlines(), 1):
        for va in ("0x437f70", "0x437F70", "0x82b5a0", "0x82B5A0", "0x7b5390", "0x007B5390", "0x7B5390"):
            if va in line:
                log("  %-40s:%d [%s] :: %s" % (rel, ln_no, va, line.strip()[:170]))
                break

# era + static-only statements
log("")
log("  era/static markers:")
for rel in ["06_REPORT/REPORT.md", "06_REPORT/HANDOFF.md", "00_CONTROL/SOURCE_IDENTITIES.json", "03_EVIDENCE/README.md"]:
    t = open(os.path.join(PKG, rel.replace("/", "\\")), encoding="utf-8", errors="replace").read()
    log("   %-40s PCG_9_3_5: %s ; STATIC-ONLY: %s" % (rel, t.count("PCG_9_3_5"), t.count("STATIC-ONLY")))

# ================= PART D: follow-up byte checks ==================================
log("")
log("== D: follow-up byte checks ==")
log(" -- D1 block ctor entry 0x007B6000..0x007B6035 (aligned) --")
va = 0x007B6000
while va < 0x007B6035:
    i = dec_at(va)
    log("   %08X  %-12s %-8s %s" % (va, i[2], i[3], i[4]))
    va += i[1]
log(" -- D2 window before 0x00529020 (find 'mov ecx,[esi+0xc0]') --")
va = 0x00529010
while va < 0x00529026:
    i = dec_at(va)
    if i is None:
        break
    log("   %08X  %-12s %-8s %s" % (va, i[2], i[3], i[4]))
    va += i[1]
log(" -- D3 receiver sites for FUN_005094C0 membership --")
for va in (0x0067B8E8, 0x0067C8A8, 0x006A3A2D):
    i = dec_at(va)
    log("   %08X  %-12s %-8s %s" % (va, i[2] if i else "?", i[3] if i else "?", i[4] if i else "?"))
    # context before
    for c in dec_range(va - 8, 14):
        if c[0] < va:
            log("      ctx %08X  %-12s %-8s %s" % (c[0], c[2], c[3], c[4]))
log(" -- D4 ebp redefinition in SF ctor 0x509357..0x5093C3 --")
va = 0x00509330
hits = []
while va < 0x005093C3:
    i = dec_at(va)
    if i is None:
        break
    if i[4] == "ebp, ecx" or i[4].startswith("ebp,"):
        hits.append("%08X %s %s" % (va, i[3], i[4]))
    va += i[1]
log("   ebp defs in 0x509330..0x5093C3: %s" % hits)
log(" -- D4b esi redefinition in SF dtor 0x50A263..0x50A2D1 --")
va = 0x0050A240
hits = []
while va < 0x0050A2D1:
    i = dec_at(va)
    if i is None:
        break
    if i[4].startswith("esi,") and not i[4].startswith("esi, ["):
        hits.append("%08X %s %s" % (va, i[3], i[4]))
    va += i[1]
log("   esi defs in 0x50A240..0x50A2D1: %s" % hits)
log(" -- D5 first rep movsd target (claim [esp+0x18]) --")
va = 0x00509430
edi_def = None
ecx_def = None
while va < 0x00509460:
    i = dec_at(va)
    if i is None:
        break
    if i[3] == "lea" and i[4].startswith("edi,"):
        edi_def = "%08X %s %s" % (va, i[3], i[4])
    if i[3] == "mov" and i[4].startswith("edi,"):
        edi_def = "%08X %s %s" % (va, i[3], i[4])
    if i[4].startswith("ecx,"):
        ecx_def = "%08X %s %s" % (va, i[3], i[4])
    va += i[1]
log("   before 0x50945D: edi_def=%s ecx_def=%s" % (edi_def, ecx_def))
log(" -- D6 second rep movsd count (claim SF+0x4C..0x70 => 9 dwords) --")
va = 0x00509460
while va < 0x00509472:
    i = dec_at(va)
    if i is None:
        break
    if i[4].startswith("ecx,"):
        log("   %08X  %-10s %-8s %s" % (va, i[2], i[3], i[4]))
    va += i[1]
log(" -- D7 combined-offset rescan at container fns (own; comb={0x34,0x3C,0x40,0x44,0x48,0xF0}, base=container reg) --")
def fn_end(entry):
    va = entry
    last = entry
    guard = 0
    while guard < 4096:
        i = dec_at(va)
        if i is None:
            break
        if i[3].startswith("ret") or i[3] == "ret":
            last = va + i[1]
            # check padding after
            b = rd(last, 2)
            if b and (b[0] in (0xCC, 0x90)):
                return last
        last = va + i[1]
        va = last
        guard += 1
    return last

COMB = {0x34, 0x3C, 0x40, 0x44, 0x48, 0xF0}
for fn, reg in ((0x0044D590, "esi"), (0x00528E50, "esi"), (0x0067B800, "esi"), (0x0067C7C0, "esi"), (0x006A3930, "esi")):
    end = fn_end(fn)
    n = 0
    va = fn
    while va < end:
        i = dec_at(va)
        if i is None:
            break
        b = rd(va, 16)
        ins = next(md.disasm(b, va))
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp in COMB and (op.access & capstone.CS_AC_WRITE):
                if ins.reg_name(op.mem.base) == reg:
                    n += 1
                    log("   HIT fn=%08X %08X %s %s disp=0x%X" % (fn, va, ins.mnemonic, ins.op_str, op.mem.disp))
        va += i[1]
    log("   fn 0x%08X (end~0x%08X): combined-disp writes via %s: %d" % (fn, end, reg, n))

open(os.path.join(PKG, "00_CONTROL/qc_probe/out_qc4_sample_scope.txt"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
log("")
log("QC4 DONE")
