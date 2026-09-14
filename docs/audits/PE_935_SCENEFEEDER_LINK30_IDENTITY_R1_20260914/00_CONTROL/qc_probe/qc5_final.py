# -*- coding: utf-8 -*-
# QC probe 5 — final loose ends:
#  E2b full-body R-CTOR-OTHER soundness, D5b first rep movsd edi def,
#  forbidden-range membership (own extents), era labels in remaining raw files,
#  receiver-site citation precision census.
# PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 INTERNAL_QC
# Output: 00_CONTROL/qc_probe/out_qc5_final.txt
import csv, io, os, re, struct, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\opencode\capstone_lib")
import capstone

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

log("== E2b: R-CTOR-OTHER full-body soundness (4 sampled rows) ==")
rows = list(csv.DictReader(open(PKG + r"\02_ANALYSIS\SF30_WRITER_CENSUS.csv")))
raw = open(PKG + r"\01_RAW\SF30_WRITER_RAW.txt", encoding="utf-8", errors="replace").read()

def why_of(va_str):
    blk = raw.split("### " + va_str + " ", 1)
    m = re.search(r"why: (.+)", blk[1]) if len(blk) > 1 else None
    return m.group(1) if m else "?"

ctor_rows = [r for r in rows if "R-CTOR-OTHER" in why_of(r["writer_va"])]
log("R-CTOR-OTHER total: %d" % len(ctor_rows))
picked = [ctor_rows[0], ctor_rows[len(ctor_rows)//3], ctor_rows[2*len(ctor_rows)//3], ctor_rows[-1]]
for r in picked:
    va = int(r["writer_va"], 16)
    fn = int(r["function_va"], 16)
    why = why_of(r["writer_va"])
    mv_imm = re.search(r"stores vtable (0x[0-9A-Fa-f]{8})", why)
    vt_imm = int(mv_imm.group(1), 16) if mv_imm else None
    log("-- %s fn=%08X claimed_vtable=0x%08X" % (r["writer_va"], fn, vt_imm or 0))
    b = rd(va, 16)
    ins = next(md.disasm(b, va))
    base = None
    for op in ins.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.disp == 0x30 and (op.access & capstone.CS_AC_WRITE):
            base = ins.reg_name(op.mem.base)
    end = fn_end(fn)
    # full body: find the vtable store via base (before AND after the candidate)
    stores = []
    base_defs = []
    cur = fn
    while cur < end:
        i = dec_at(cur)
        if i is None:
            break
        if i[3] == "mov" and i[4] == "dword ptr [%s], 0x%x" % (base, vt_imm) and vt_imm:
            stores.append((cur, "before" if cur < va else "after"))
        if i[4].startswith(base + ","):
            base_defs.append((cur, i[3], i[4]))
        cur += i[1]
    log("   vtable store via %s (imm 0x%x): %s" % (base, vt_imm or 0, stores))
    log("   ALL %s defs in full body: %s" % (base, ["%08X %s %s" % d for d in base_defs]))
    log("   base==store reg and (no redefinition beyond entry this-copy): %s"
        % ("SOUND" if stores and all(d[1] == "mov" and d[2].split(",")[1].strip() == "ecx" for d in base_defs) else "INSPECT"))

log("")
log("== D5b: first rep movsd (0x50945D) edi/esi defs (full window 0x509440..0x509460) ==")
va = 0x00509440
while va < 0x00509460:
    i = dec_at(va)
    if i is None:
        break
    log("   %08X  %-12s %-10s %s" % (va, i[2], i[3], i[4]))
    va += i[1]
log("   (widening: 0x509435..)")
va = 0x00509435
while va < 0x00509445:
    i = dec_at(va)
    if i is None:
        break
    log("   %08X  %-12s %-10s %s" % (va, i[2], i[3], i[4]))
    va += i[1]

log("")
log("== F1: forbidden-range membership (own extents) ==")
for entry in (0x00437F70, 0x0082B5A0, 0x007B5390):
    end = fn_end(entry)
    log("   fn 0x%08X: my extent ~0x%08X (len 0x%X)" % (entry, end, end - entry))
    inside = []
    near = []
    for r in rows:
        v = int(r["writer_va"], 16)
        if entry <= v <= end:
            inside.append(r["writer_va"])
        elif entry <= v <= entry + 0x3000:
            near.append((r["writer_va"], v - entry))
    log("      census rows inside: %d %s" % (len(inside), inside))
    log("      census rows in (entry, entry+0x3000]: %s" % near)

log("")
log("== F2: era labels in remaining raw files ==")
for rel in ("01_RAW/POSITIVE_CONTROL_0050A050.txt", "01_RAW/SF30_RTTI_RAW.txt", "01_RAW/SF30_WRITER_RAW.txt", "02_ANALYSIS/SF30_PROVENANCE.md"):
    t = open(os.path.join(PKG, rel.replace("/", "\\")), encoding="utf-8", errors="replace").read()
    log("   %-38s PCG_9_3_5=%d STATIC-ONLY=%d RUN_ID=%s" % (
        rel, t.count("PCG_9_3_5"), t.count("STATIC-ONLY"),
        "yes" if "PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914" in t else "no"))

log("")
log("== F3: receiver-site citation precision (REPORT/raw/state 'mov' attached to call VAs) ==")
FILES = {
    "REPORT.md": os.path.join(PKG, "06_REPORT", "REPORT.md"),
    "SF30_WRITER_RAW.txt": os.path.join(PKG, "01_RAW", "SF30_WRITER_RAW.txt"),
    "census_state.json": os.path.join(PKG, "00_CONTROL", "census_state.json"),
}
for fname, fpath in FILES.items():
    t = open(fpath, encoding="utf-8", errors="replace").read()
    for pat in ("0x00529020 mov ecx,[esi+0xc0]", "0x0067B8E8 mov ecx,[esi+4]"):
        for ln_no, line in enumerate(t.splitlines(), 1):
            if pat in line:
                log("   %-26s :%-5d [%s] :: %s" % (fname, ln_no, pat, line.strip()[:160]))
log("   ground truth (own bytes): load @0x0052901A mov ecx,[esi+0xc0]; call 0x5094c0 @0x00529020")
log("   ground truth (own bytes): load @0x0067B8E4 mov ecx,[esi+4];   call 0x5094c0 @0x0067B8E8")
log("   ground truth (own bytes): load @0x006A3A29 mov ecx,[esi+0x18]; call 0x5094c0 @0x006A3A2D")

log("")
log("== F4: raw 2.1 'hit -> store insn' presentation artifact (misaligned render) ==")
for ln_no, line in enumerate(raw.splitlines(), 1):
    if "hit  -> store insn" in line or "hit -> store insn" in line:
        log("   raw:%d :: %s" % (ln_no, line.strip()[:150]))
log("   NOTE: census.py renders 'store insn' via a 1..8-back disasm that can land")
log("   misaligned (verified: 0x509368 'add byte ptr [eax-0x2c],bl' is a misaligned")
log("   decode of the imm bytes; the true store is at 0x00509366, stated on the")
log("   'classified:' lines). Also the hit VA itself is not printed (hexdump(h,0) bug).")

open(PKG + r"\00_CONTROL\qc_probe\out_qc5_final.txt", "w", encoding="utf-8").write("\n".join(OUT) + "\n")
log("")
log("QC5 DONE")
