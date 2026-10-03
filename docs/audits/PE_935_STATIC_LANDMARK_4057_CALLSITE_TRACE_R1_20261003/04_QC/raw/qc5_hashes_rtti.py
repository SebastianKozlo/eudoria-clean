# QC5: script hash re-verification + RTTI vtable COL walk (RVA interpretation)
import struct, hashlib, csv, os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
OUTP = PKS = os.path.join(PKG, "04_QC", "raw", "qc5_output.txt")
out = open(OUTP, "w", encoding="utf-8")
def emit(s=""):
    print(s); out.write(s + "\n")

emit("== script SHA256 re-verification (my own re-hash vs SCRIPT_SHA256.csv)")
rows = [r for r in csv.DictReader(open(os.path.join(PKG, "03_SCRIPTS", "SCRIPT_SHA256.csv"), encoding="utf-8-sig")) if r.get("script")]
emit(f"  csv rows (non-empty, BOM-tolerant): {len(rows)}")
bad = 0
for r in rows:
    p = os.path.join(PKG, "03_SCRIPTS", r["script"])
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    ok = h == r["sha256"].strip().lower()
    if not ok:
        bad += 1
        emit(f"  MISMATCH {r['script']}: csv={r['sha256']} mine={h}")
emit(f"  re-hashed {len(rows)} scripts; mismatches={bad}")
disk = sorted(f for f in os.listdir(os.path.join(PKG, "03_SCRIPTS")) if f.endswith(".py"))
csvset = set(r["script"] for r in rows)
emit(f"  scripts on disk: {len(disk)}; in csv: {len(csvset)}; disk-minus-csv={sorted(set(disk)-csvset)}; csv-minus-disk={sorted(csvset-set(disk))}")

emit("\n== RTTI vtable COL walks (retry, RVA-aware)")
data = open(r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe", "rb").read()
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
opt = e_lfanew + 4 + 20
image_base = struct.unpack_from("<I", data, opt + 28)[0]
nsec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
sizeopt = struct.unpack_from("<H", data, e_lfanew + 20)[0]
secs = []
for i in range(nsec):
    o = opt + sizeopt + i * 40
    nm = data[o:o+8].rstrip(b"\x00").decode()
    vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, o + 8)
    secs.append((nm, vaddr, vsize, rptr, rsize))
def va2off(va):
    rva = va - image_base
    for (n, vaddr, vsize, rptr, rsize) in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return rptr + (rva - vaddr)
    return None
def rd32va(va):
    return struct.unpack_from("<I", data, va2off(va))[0]
def rdstr(va, n=48):
    o = va2off(va); return data[o:o+n].split(b"\x00")[0]
for vt, label in [(0x00A80704, "claim: ArkRepairUI::vftable (stored in FUN_0059BE70 unwind local)"),
                  (0x00A7A948, "claim: ArkUI::Component::vftable (stored in FUN_008DFB70 temp)")]:
    col_field = rd32va(vt - 4)
    emit(f"  VT 0x{vt:08X} ({label}):")
    emit(f"    [VT-4] raw dword = 0x{col_field:08X}")
    o = va2off(col_field)
    if o is not None:
        b = data[o:o+24]
        emit(f"    raw bytes @0x{col_field:08X}: " + " ".join(f"{x:02X}" for x in b))
    for interp_name, col_va in [("as VA", col_field), ("as RVA+base", image_base + col_field)]:
        try:
            o = va2off(col_va)
            if o is None:
                emit(f"    {interp_name}: COL 0x{col_va:08X} unmappable")
                continue
            sig, off, cdoff, td_rva, cd_rva, self_rva = struct.unpack_from("<IIIIII", data, o)
            emit(f"    {interp_name}: COL=0x{col_va:08X} sig=0x{sig:08X} off=0x{off:08X} cdoff=0x{cdoff:08X} td_rva=0x{td_rva:08X} cd_rva=0x{cd_rva:08X} self_rva=0x{self_rva:08X}")
            for td_name, td_va in [("TD as base+rva", image_base + td_rva), ("TD as VA", td_rva)]:
                try:
                    nm = rdstr(td_va + 8)
                    emit(f"      {td_name}: TD=0x{td_va:08X} name={nm!r}")
                except Exception as e:
                    emit(f"      {td_name}: TD=0x{td_va:08X} unreadable ({e})")
        except Exception as e:
            emit(f"    {interp_name}: FAILED {e}")
emit("\n== DONE qc5")
out.close()
