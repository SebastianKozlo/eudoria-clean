# -*- coding: utf-8 -*-
# QC probe 4b — scope census (fixed encoding), follow-up byte checks D1-D7,
# adversarial classification checks E1-E3 (ebp rows, R-CTOR-OTHER, F_SF rows).
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 INTERNAL_QC
# Output: 00_CONTROL/qc_probe/out_qc4b_scope_bytes.txt
import csv, os, re, struct, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914"
OUT = []

def log(s=""):
    OUT.append(s)
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode())

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

# ================= PART C: scope census (own) =====================================
log("== C: scope census over the executor package (17 files) ==")
PKG_FILES = [
    "00_CONTROL/RUN_CONTRACT.md", "00_CONTROL/SCRIPT_SHA256.csv", "00_CONTROL/SOURCE_IDENTITIES.json",
    "00_CONTROL/census.py", "00_CONTROL/census_state.json", "00_CONTROL/finalize.py", "00_CONTROL/sf30_core.py",
    "01_RAW/POSITIVE_CONTROL_0050A050.txt", "01_RAW/SF30_RTTI_RAW.txt", "01_RAW/SF30_WRITER_RAW.txt",
    "02_ANALYSIS/SF30_PROVENANCE.md", "02_ANALYSIS/SF30_WRITER_CENSUS.csv", "03_EVIDENCE/README.md",
    "06_REPORT/HANDOFF.md", "06_REPORT/MANIFEST_SHA256.csv", "06_REPORT/REPORT.md",
    "06_REPORT/STAGE_ACCEPTANCE_GATES.csv",
]
def txt(rel):
    return open(os.path.join(PKG, rel.replace("/", "\\")), encoding="utf-8", errors="replace").read()

log("-- forbidden-claim labels with my own context verdict --")
CLAIMISH = re.compile(r"(MODEL_BRIDGE_CONFIRMED|TRANSFORM_TO_MODEL)", re.I)
NEG_OK = re.compile(r"NOT_DEMONSTRATED|not made|no MODEL_BRIDGE|no TRANSFORM|remains|zero|forbidden|FORBIDDEN|no claim|no slot|not decode|claim", re.I)
any_claim = []
for rel in PKG_FILES:
    for ln_no, line in enumerate(txt(rel).splitlines(), 1):
        m = CLAIMISH.search(line)
        if m:
            verdict = "negative/allowed" if NEG_OK.search(line) else "POSSIBLE CLAIM - INSPECT"
            log("  %-38s:%-4d %s :: %s" % (rel, ln_no, verdict, line.strip()[:150]))
            if verdict != "negative/allowed":
                any_claim.append((rel, ln_no, line))
log("  -> non-negative contexts: %d %s" % (len(any_claim), any_claim if any_claim else "(none: zero claim-context)"))

log("-- old wrong figures (26 package files / 25 manifest rows) --")
found_old = False
for rel in PKG_FILES:
    for ln_no, line in enumerate(txt(rel).splitlines(), 1):
        if re.search(r"26 package files|25 manifest rows", line):
            log("  OLD-FIGURE %s:%d :: %s" % (rel, ln_no, line.strip()[:150]))
            found_old = True
log("  old wrong figures present: %s" % ("YES" if found_old else "NO (correct: new package uses 27/26/28 figures only)"))

log("-- corrected figures stated --")
for rel in ("00_CONTROL/SOURCE_IDENTITIES.json", "00_CONTROL/RUN_CONTRACT.md"):
    for ln_no, line in enumerate(txt(rel).splitlines(), 1):
        if "27 package files" in line or "28 commit paths" in line:
            log("  %-38s:%-4d :: %s" % (rel, ln_no, line.strip()[:150]))

log("-- forbidden-VA textual occurrences (0x437F70 / 0x82B5A0 / 0x7B5390) --")
for rel in PKG_FILES:
    for ln_no, line in enumerate(txt(rel).splitlines(), 1):
        for va in ("0x437f70", "0x437F70", "0x82b5a0", "0x82B5A0", "0x7b5390", "0x007B5390", "0x7B5390", "0x437F70"):
            if va in line:
                log("  %-38s:%-4d [%s] :: %s" % (rel, ln_no, va, line.strip()[:170]))
                break

log("-- slot-17-decode-like listings in .txt evidence --")
for rel in [f for f in PKG_FILES if f.endswith(".txt")]:
    t = txt(rel)
    for pat in ("### 0x007B5390", "0x7B5390 ", "FUN_007B5390"):
        if pat in t:
            log("  %s contains %r" % (rel, pat))
log("  (none expected: slot 17 recorded as VALUE only)")

log("-- era + static-only markers --")
for rel in ["06_REPORT/REPORT.md", "06_REPORT/HANDOFF.md", "00_CONTROL/SOURCE_IDENTITIES.json", "03_EVIDENCE/README.md", "01_RAW/SF30_WRITER_RAW.txt"]:
    t = txt(rel)
    log("  %-40s PCG_9_3_5=%d STATIC-ONLY=%d" % (rel, t.count("PCG_9_3_5"), t.count("STATIC-ONLY")))

log("-- R-EBP-FRAME presence in raw (report lists it as a reason family) --")
n_ebpframe = len(re.findall(r"R-EBP-FRAME", raw))
log("  'R-EBP-FRAME' occurrences in SF30_WRITER_RAW.txt: %d" % n_ebpframe)

# ================= PART D: follow-up byte checks ==================================
log("")
log("== D1: block ctor entry 0x007B6000..0x007B6035 (aligned) ==")
va = 0x007B6000
while va < 0x007B6035:
    i = dec_at(va)
    log("   %08X  %-12s %-8s %s" % (va, i[2], i[3], i[4]))
    va += i[1]

log("")
log("== D2: window before 0x00529020 (locate 'mov ecx,[esi+0xc0]') ==")
va = 0x00529010
while va < 0x00529026:
    i = dec_at(va)
    if i is None:
        break
    log("   %08X  %-12s %-8s %s" % (va, i[2], i[3], i[4]))
    va += i[1]

log("")
log("== D3: receiver sites for FUN_005094C0 F_SF membership ==")
for va in (0x0067B8E8, 0x0067C8A8, 0x006A3A2D):
    i = dec_at(va)
    log("   site %08X: %s %s" % (va, i[3], i[4]))
    for c in dec_range(va - 10, 18):
        if c[0] < va:
            log("      ctx %08X  %-12s %-8s %s" % (c[0], c[2], c[3], c[4]))

log("")
log("== D4: ebp redefinition scan SF ctor 0x509330..0x5093C3 (PROVEN soundness) ==")
va = 0x00509330
defs = []
while va < 0x005093C3:
    i = dec_at(va)
    if i is None:
        break
    if i[4].startswith("ebp,"):
        defs.append("%08X %s %s" % (va, i[3], i[4]))
    va += i[1]
log("   ebp defs before WRITE1: %s" % (defs if defs else "NONE (only the entry mov ebp,ecx counted below)"))
log("   (entry def at 0x509357: %s)" % (dec_at(0x00509357)[3] + " " + dec_at(0x00509357)[4]))
log("== D4b: esi redefinition scan SF dtor 0x50A263..0x50A2D1 ==")
va = 0x0050A263
defs = []
while va < 0x0050A2D1:
    i = dec_at(va)
    if i is None:
        break
    if i[4].startswith("esi,"):
        defs.append("%08X %s %s" % (va, i[3], i[4]))
    va += i[1]
log("   esi defs before WRITE2: %s" % (defs if defs else "NONE"))

log("")
log("== D5: first rep movsd target (claim [esp+0x18]) ==")
va = 0x00509400
edi_def = None
ecx_def = None
while va < 0x0050945E:
    i = dec_at(va)
    if i is None:
        break
    if i[4].startswith("edi,"):
        edi_def = "%08X %s %s" % (va, i[3], i[4])
    if i[4].startswith("ecx,"):
        ecx_def = "%08X %s %s" % (va, i[3], i[4])
    va += i[1]
log("   last edi def before 0x50945D: %s ; last ecx def: %s" % (edi_def, ecx_def))
log("== D6: second rep movsd (0x50946E) count + range ==")
va = 0x00509460
while va < 0x00509470:
    i = dec_at(va)
    if i is None:
        break
    if i[4].startswith("ecx,") or i[4].startswith("edi,"):
        log("   %08X  %-12s %-8s %s" % (va, i[2], i[3], i[4]))
    va += i[1]

log("")
log("== D7: combined-offset rescan at the 5 proven container fns (own) ==")
COMB = {0x34, 0x3C, 0x40, 0x44, 0x48, 0xF0}
def fn_end(entry):
    va = entry
    last = entry
    guard = 0
    while guard < 8192:
        i = dec_at(va)
        if i is None:
            break
        last = va + i[1]
        if i[3].startswith("ret"):
            b = rd(last, 2)
            if b and b[0] in (0xCC, 0x90):
                return last
        va = last
        guard += 1
    return last

for fn in (0x0044D590, 0x00528E50, 0x0067B800, 0x0067C7C0, 0x006A3930):
    end = fn_end(fn)
    hits = []
    va = fn
    while va < end:
        i = dec_at(va)
        if i is None:
            break
        b = rd(va, 16)
        ins = next(md.disasm(b, va))
        for op in ins.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.disp in COMB and (op.access & capstone.CS_AC_WRITE):
                base = ins.reg_name(op.mem.base) if op.mem.base else ""
                if base == "esi":
                    hits.append("%08X %s %s disp=0x%X" % (va, ins.mnemonic, ins.op_str, op.mem.disp))
        va += i[1]
    log("   fn 0x%08X (my end ~0x%08X): esi-based combined-disp writes: %d %s" % (fn, end, len(hits), hits if hits else ""))

# ================= PART E: adversarial classification checks =====================
log("")
log("== E1: all 25 ebp-based candidates breakdown ==")
from collections import Counter
ebp_rows = [r for r in rows if "[ebp + 0x30]" in r["instruction"]]
log("   ebp-based rows: %d" % len(ebp_rows))
cc = Counter(r["classification"] for r in ebp_rows)
log("   by class: %s" % dict(cc))
for r in ebp_rows:
    if r["classification"] in ("PROVEN_SF30_WRITER", "UNRESOLVED"):
        log("   %s %s %s recv=%r" % (r["writer_va"], r["classification"], r["instruction"], r["receiver_provenance"]))

log("")
log("== E2: adversarial R-CTOR-OTHER check (4 rows deep) ==")
def why_of(va_str):
    blk = raw.split("### " + va_str + " ", 1)
    m = re.search(r"why: (.+)", blk[1]) if len(blk) > 1 else None
    return m.group(1) if m else "?"

ctor_rows = [r for r in rows if "R-CTOR-OTHER" in why_of(r["writer_va"])]
log("   R-CTOR-OTHER rows: %d" % len(ctor_rows))
picked = [ctor_rows[0], ctor_rows[len(ctor_rows)//3], ctor_rows[2*len(ctor_rows)//3], ctor_rows[-1]]
for r in picked:
    va = int(r["writer_va"], 16)
    fn = int(r["function_va"], 16)
    log("   -- %s fn=%s why: %s" % (r["writer_va"], r["function_va"], why_of(r["writer_va"])[:140]))
    # decode forward from fn to candidate, tracking base-reg defs and vtable stores
    b = rd(va, 16)
    ins = next(md.disasm(b, va))
    base = None
    for op in ins.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
            base = ins.reg_name(op.mem.base)
    vt_store = []
    base_defs = []
    cur = fn
    while cur < va:
        i = dec_at(cur)
        if i is None:
            break
        if i[3] == "mov" and re.match(r"^dword ptr \[%s\], 0x[0-9a-f]{8}$" % base, i[4].replace(" + 0]", "]").replace("dword ptr [%s]" % base, "dword ptr [%s]" % base)):
            vt_store.append("%08X %s %s" % (cur, i[3], i[4]))
        if i[4].startswith(base + ","):
            base_defs.append("%08X %s %s" % (cur, i[3], i[4]))
        cur += i[1]
    log("      base=%s ; vtable-store via base before candidate: %s" % (base, vt_store[:3]))
    log("      base defs between fn entry and candidate (last 3): %s" % (base_defs[-3:] if base_defs else "NONE"))

log("")
log("== E3: all candidates inside the 19 F_SF functions (census internal soundness) ==")
F_SF = [0x0044D590, 0x0047CCF0, 0x005090A0, 0x005090B0, 0x005090C0, 0x00509330,
        0x005094C0, 0x005094E0, 0x00509580, 0x00509670, 0x00509F00, 0x0050A050,
        0x0050A240, 0x0050A460, 0x005247C0, 0x00528E50, 0x0067B800, 0x0067C7C0, 0x006A3930]
for r in rows:
    if r["function_va"] != "UNATTRIBUTED" and int(r["function_va"], 16) in F_SF:
        log("   %s %s class=%s recv=%r" % (r["writer_va"], r["instruction"], r["classification"], r["receiver_provenance"][:90]))

open(PKG + r"\00_CONTROL\qc_probe\out_qc4b_scope_bytes.txt", "w", encoding="utf-8").write("\n".join(OUT) + "\n")
log("")
log("QC4B DONE")
