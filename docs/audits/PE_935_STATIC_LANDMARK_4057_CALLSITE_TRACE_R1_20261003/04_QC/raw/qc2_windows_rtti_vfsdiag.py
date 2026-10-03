# QC2: machinery-in-window filter, FUN_00599D30 callee census, RTTI chain walks, VFS/BNT diagnostics
import struct

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
TVFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
SVFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\sids.vfs"
MBNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
VBNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
OUTP = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003\04_QC\raw\qc2_output.txt"
out = open(OUTP, "w", encoding="utf-8")
def emit(s=""):
    print(s); out.write(s + "\n")

data = open(EXE, "rb").read()
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
opt = e_lfanew + 4 + 20
image_base = struct.unpack_from("<I", data, opt + 28)[0]
secs = []
nsec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
sizeopt = struct.unpack_from("<H", data, e_lfanew + 20)[0]
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
def rdstr(va, n=64):
    o = va2off(va); b = data[o:o+n]; return b.split(b"\x00")[0]
tv = [s for s in secs if s[0] == ".text"][0]
tva0 = image_base + tv[1]
tbytes = data[tv[3]:tv[3] + tv[4]]

# ============ PART A: machinery-in-window filter ============
W = {
 "FUN_00599D30": (0x00599D30, 0x0059AC88),
 "FUN_008DFCD0": (0x008DFCD0, 0x008DFD63),
 "FUN_008F0780": (0x008F0780, 0x008F0814),
 "FUN_008E7B80": (0x008E7B80, 0x008E7C00),
 "FUN_008DF3F0": (0x008DF3F0, 0x008DF480),
 "FUN_008DF310": (0x008DF310, 0x008DF400),
 "FUN_00414170": (0x00414170, 0x004141E0),
 "FUN_00821BB0": (0x00821BB0, 0x00821C70),
 "FUN_008DFB70": (0x008DFB70, 0x008DFD00),
 "FUN_008F01C0": (0x008F01C0, 0x008F0300),
 "FUN_0059BE70": (0x0059BE70, 0x0059BF6D),
 "FUN_00821760": (0x00821760, 0x00821A00),
 "FUN_008221C0": (0x008221C0, 0x00822220),
 "FUN_00826A50": (0x00826A50, 0x00826A5D),
 "FUN_00415670": (0x00415670, 0x004156E0),
 "FUN_00823C10": (0x00823C10, 0x00823E10),
 "FUN_00821FB0": (0x00821FB0, 0x00822210),
 "FUN_00821E70": (0x00821E70, 0x00822210),
}
MACH = {
 0x0072F580: "registry_lookup", 0x0043A550: "registry_getter", 0x0072FA30: "templates_reader",
 0x00730C90: "template_parse", 0x007CE1E0: "A_getter", 0x006C3F50: "request_pair_emitter",
 0x008BD720: "scheduler_callback", 0x0072F8D0: "rbtree_insert", 0x0072FE30: "template_list2_out",
 0x004D1430: "generic_mapfind", 0x006CB6F0: "instance_creator",
}
emit("== PART A: machinery E8 sites falling inside ANY measured-function window (byte-level superset)")
mach_sites = {}
for tgt, nm in MACH.items():
    sites = []
    for p in range(len(tbytes) - 5):
        if tbytes[p] == 0xE8:
            rel = struct.unpack_from("<i", tbytes, p + 1)[0]
            if tva0 + p + 5 + rel == tgt:
                sites.append(tva0 + p)
    mach_sites[tgt] = sites
total_inwin = 0
for tgt, nm in MACH.items():
    inwin = []
    for s in mach_sites[tgt]:
        for fn, (a, b) in W.items():
            if a <= s < b:
                inwin.append((fn, s))
    if inwin:
        total_inwin += len(inwin)
        for fn, s in inwin:
            emit(f"  IN-WINDOW HIT: 0x{tgt:08X} {nm} called @0x{s:08X} inside {fn}")
emit(f"  machinery in-window hits total = {total_inwin} (expected: exactly 1 = FUN_004D1430 inside FUN_00823C10 @0x00823C57)")
emit("  full .text site counts per machinery VA (incl. outside windows):")
for tgt, nm in MACH.items():
    emit(f"    0x{tgt:08X} {nm}: {len(mach_sites[tgt])} sites")

# ============ PART B: FUN_00599D30 callee census ============
emit("\n== PART B: FUN_00599D30 body E8 census [0x00599D30,0x0059AC88) (byte-level superset)")
a_off = va2off(0x00599D30); b_off = va2off(0x0059AC88)
body = data[a_off:b_off + 1]
sites = []; targets = {}
for p in range(len(body) - 5):
    if body[p] == 0xE8:
        rel = struct.unpack_from("<i", body, p + 1)[0]
        t = 0x00599D30 + p + 5 + rel
        sites.append(0x00599D30 + p)
        targets.setdefault(t, []).append(0x00599D30 + p)
emit(f"  E8 byte-sites in body: {len(sites)} (claim: 177 call sites total incl. 7 indirect); unique E8 targets: {len(targets)} (claim: 49 unique direct)")
emit(f"  unique E8 targets: {sorted(hex(t) for t in targets)}")
for t in sorted(targets):
    emit(f"    0x{t:08X}: {len(targets[t])} site(s)")

# ============ PART C: RTTI chain walks (independent) ============
emit("\n== PART C: RTTI chain walks")
def td_name(td_va):
    return rdstr(td_va + 8, 48)
def vtable_class(va):
    col_va = rd32va(va - 4)
    o = va2off(col_va)
    sig, off, cdoff, td_rva, cd_rva, self_rva = struct.unpack_from("<IIIIII", data, o)
    td_va = image_base + td_rva
    return col_va, sig, td_va, rdstr(td_va + 8, 48)

emit("  [gate TD pushed in FUN_0059BE70 @0x0059BEF9 = 0x00B7DDE8]")
emit(f"  TD 0x00B7DDE8: vftable_ptr=0x{rd32va(0x00B7DDE8):08X} spare=0x{rd32va(0x00B7DDEC):08X} name={td_name(0x00B7DDE8)!r}")
emit("  [vtable stored in FUN_0059BE70 unwind local @0x0059BEC7 = 0x00A80704 (claim: ArkRepairUI::vftable)]")
try:
    col, sig, td, nm = vtable_class(0x00A80704)
    emit(f"  VT 0x00A80704: COL=0x{col:08X} sig=0x{sig:08X} TD=0x{td:08X} name={nm!r}")
except Exception as e:
    emit(f"  VT 0x00A80704 walk FAILED: {e}")
emit("  [vtable stored in FUN_008DFB70 temp @0x008DFBD0 = 0x00A7A948 (claim: ArkUI::Component::vftable)]")
try:
    col, sig, td, nm = vtable_class(0x00A7A948)
    emit(f"  VT 0x00A7A948: COL=0x{col:08X} sig=0x{sig:08X} TD=0x{td:08X} name={nm!r}")
except Exception as e:
    emit(f"  VT 0x00A7A948 walk FAILED: {e}")
emit("  [TD pushed in FUN_008F01C0 @0x008F01F4 = 0x00B73F60]")
emit(f"  TD 0x00B73F60: name={td_name(0x00B73F60)!r}")
emit(f"  [operator!= import ptr @0x00A75320 -> 0x{rd32va(0x00A75320):08X}]")
# also dump raw RTTI region file 0x77ddc0..0x77de10
o = 0x77ddc0
emit("  raw .data 0x77ddc0..0x77de0f:")
for i in range(0, 0x50, 16):
    b = data[o+i:o+i+16]
    emit(f"    +0x{i:02X}: " + " ".join(f"{x:02X}" for x in b).ljust(47) + "  " + "".join(chr(x) if 32 <= x < 127 else "." for x in b))

# ============ PART D: templates.vfs / sids.vfs / BNT diagnostics ============
def dumpfile(path, frm, to, label):
    d = open(path, "rb")
    d.seek(frm)
    b = d.read(to - frm)
    d.close()
    emit(f"  [{label}] {path.split(chr(92))[-1]} [{frm}..{to}):")
    for i in range(0, len(b), 16):
        c = b[i:i+16]
        emit(f"    {frm+i:7d}: " + " ".join(f"{x:02X}" for x in c).ljust(47) + "  " + "".join(chr(x) if 32 <= x < 127 else "." for x in c))
    return b

emit("\n== PART D1: templates.vfs diagnostics (size=%d)" % len(open(TVFS,'rb').read()))
dumpfile(TVFS, 0, 128, "header")
dumpfile(TVFS, 88776, 88848, "record-4057 area (claim: header_id=4057 @88792, size 28, ver 1, crc 79E7AC62, payload d9 0f 00 00 85 56 03 00 86 56 03 00 ...)")
dumpfile(TVFS, 96480, 96552, "record-4508 area (claim: header_id=4508 @96496, size 28, ver 1, crc AFF5797C, payload 9c 11 00 00 fd 85 04 00 fe 85 04 00 ...)")
dumpfile(TVFS, len(open(TVFS,'rb').read()) - 64, len(open(TVFS,'rb').read()), "tail")

sd = open(SVFS, "rb").read()
emit("\n== PART D2: sids.vfs diagnostics (size=%d)" % len(sd))
emit(f"  bytes[0:128]:")
for i in range(0, 128, 16):
    c = sd[i:i+16]
    emit(f"    {i:7d}: " + " ".join(f"{x:02X}" for x in c).ljust(47) + "  " + "".join(chr(x) if 32 <= x < 127 else "." for x in c))
emit(f"  u16 candidates: @36=0x{struct.unpack_from('<H', sd, 36)[0]:04X} @38=0x{struct.unpack_from('<H', sd, 38)[0]:04X} @40=0x{struct.unpack_from('<H', sd, 40)[0]:04X} @44=0x{struct.unpack_from('<H', sd, 44)[0]:04X} @48=0x{struct.unpack_from('<H', sd, 48)[0]:04X} (claim: count=3887=0x0F2F)")
emit(f"  tail 32:")
for i in range(len(sd) - 32, len(sd), 16):
    c = sd[i:i+16]
    emit(f"    {i:7d}: " + " ".join(f"{x:02X}" for x in c).ljust(47) + "  " + "".join(chr(x) if 32 <= x < 127 else "." for x in c))

def big_search(path, needle, label):
    emit(f"  [{label}] searching {path.split(chr(92))[-1]} for {needle!r} ...")
    hits = []
    with open(path, "rb") as f:
        pos = 0
        ov = b""
        while True:
            chunk = f.read(1 << 24)
            if not chunk:
                break
            buf = ov + chunk
            start = 0
            while True:
                p = buf.find(needle, start)
                if p < 0:
                    break
                hits.append(pos - len(ov) + p)
                start = p + 1
            ov = buf[-(len(needle) + 16):]
            pos += len(chunk)
    emit(f"    hits: {len(hits)}: {[h for h in hits[:10]]}")
    return hits

emit("\n== PART D3: BNT index name searches (my own, full-file)")
m1 = big_search(MBNT, b"218757.nif", "Models target")
m2 = big_search(MBNT, b"296445.nif", "Models calibration")
v1 = big_search(VBNT, b"218758.bvi", "Volumes target")
v2 = big_search(VBNT, b"296446.bvi", "Volumes calibration")
dumpfile(MBNT, 395262727 - 32, 395262727 + 96, "Models.bnt claimed index_start 395262727 area")
dumpfile(MBNT, (m1[0] if m1 else 395283797) - 16, (m1[0] if m1 else 395283797) + 48, "Models.bnt 218757.nif area")
dumpfile(VBNT, 3696320 - 32, 3696320 + 96, "Volumes.bnt claimed index_start 3696320 area")
dumpfile(VBNT, (v1[0] if v1 else 3712726) - 16, (v1[0] if v1 else 3712726) + 48, "Volumes.bnt 218758.bvi area")
emit("\n== DONE qc2")
out.close()
