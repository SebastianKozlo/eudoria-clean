# QC independent byte measurement — PE parse, byte dumps, call/immediate censuses
# Author: pe-master-auditor (fresh QC), run PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
# Independent of executor scripts: own PE mapper, own census, own recomputation.
import struct, sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
OUTP = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003\04_QC\raw\qc1_exe_bytes_output.txt"
out = open(OUTP, "w", encoding="utf-8")
def emit(s=""):
    print(s)
    out.write(s + "\n")

data = open(EXE, "rb").read()
emit(f"== S0 EXE IDENTITY: size={len(data)}")

# --- own PE parse ---
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
assert data[e_lfanew:e_lfanew+4] == b"PE\x00\x00", "bad PE sig"
coff = e_lfanew + 4
machine, nsec, tstamp, psym, nsym, sizeopt, fchars = struct.unpack_from("<HHIIIHH", data, coff)
opt = coff + 20
magic = struct.unpack_from("<H", data, opt)[0]
image_base = struct.unpack_from("<I", data, opt + 28)[0]
dllchars = struct.unpack_from("<H", data, opt + 70)[0]
entry_rva = struct.unpack_from("<I", data, opt + 16)[0]
emit(f"e_lfanew=0x{e_lfanew:X} machine=0x{machine:04X} nsec={nsec} sizeopt=0x{sizeopt:X}")
emit(f"IMAGE_BASE=0x{image_base:08X} DllCharacteristics=0x{dllchars:04X} (ASLR={'ON' if dllchars & 0x40 else 'OFF'}) entry_rva=0x{entry_rva:08X}")
secs = []
for i in range(nsec):
    o = opt + sizeopt + i * 40
    name = data[o:o+8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, o + 8)
    secs.append((name, vaddr, vsize, rptr, rsize))
    emit(f"SEC {name:8s} RVA=0x{vaddr:08X} VSZ=0x{vsize:X} RAW=0x{rptr:X} RSZ=0x{rsize:X}")

def va2off(va):
    rva = va - image_base
    for (n, vaddr, vsize, rptr, rsize) in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return rptr + (rva - vaddr), n
    return None, None

def dump(va, n, label):
    off, sec = va2off(va)
    b = data[off:off+n]
    emit(f"\n-- [{label}] VA=0x{va:08X} file_off={off} sec={sec}")
    for i in range(0, len(b), 16):
        c = b[i:i+16]
        emit(f"  {va+i:08X} ({off+i:7d}): " + " ".join(f"{x:02X}" for x in c).ljust(47) + "  " +
             "".join(chr(x) if 32 <= x < 127 else "." for x in c))
    return b

def rd32va(va):
    off, _ = va2off(va)
    return struct.unpack_from("<I", data, off)[0]

def call_target(va):
    """Assume E8 at VA; return target."""
    off, _ = va2off(va)
    if data[off] != 0xE8:
        return None
    rel = struct.unpack_from("<i", data, off + 1)[0]
    return va + 5 + rel

# --- S1 (Q5): the anchor immediate ---
b = dump(0x0059AB12, 16, "Q5 bytes at anchor 0x0059AB12")
emit(f"Q5 bytes_at_anchor = {' '.join(f'{x:02X}' for x in b[0:5])}  claim=68 D9 0F 00 00  MATCH={b[0:5]==bytes.fromhex('68D90F0000')}")
if b[0] == 0x68:
    emit(f"Q5 imm32 = 0x{struct.unpack_from('<I', b, 1)[0]:08X} = {struct.unpack_from('<I', b, 1)[0]}")
dump(0x0059AAF2, 32, "Q5 32B pre-context (boundary decode)")

# --- S2 (Q14a): 886 immediate ---
b886 = dump(0x0059AB37, 16, "Q14 886 bytes at 0x0059AB37")
emit(f"Q14a bytes = {' '.join(f'{x:02X}' for x in b886[0:5])}  claim=68 76 03 00 00  MATCH={b886[0:5]==bytes.fromhex('6876030000')}")
if b886[0] == 0x68:
    emit(f"Q14a imm32 = {struct.unpack_from('<I', b886, 1)[0]}")

# --- S3 (Q6): containing function boundaries ---
dump(0x00599D20, 48, "Q6 FUN_00599D30 prologue + 16B pre-padding")
dump(0x0059AC60, 64, "Q6 end region 0x0059AC60..0x0059AC9F (claimed end 0x0059AC88)")
emit(f"Q6 body size claim: 0x0059AC88-0x00599D30 = {0x0059AC88-0x00599D30} B (claim 3929)")

# --- S4 (Q6): caller call site + RTTI gate context ---
dump(0x0059BF05, 32, "Q6 caller call site @0x0059BF11 context")
t = call_target(0x0059BF11)
emit(f"Q6 call@0x0059BF11 opcode=0x{data[va2off(0x0059BF11)[0]]:02X} target=0x{t:08X} claim=0x00599D30 MATCH={t==0x00599D30}")
dump(0x0059BE70, 272, "Q6/Q-RTTI caller FUN_0059BE70 full window 0x0059BE70..0x0059BF7F")

# --- S5: .text E8/E9 census for calls to FUN_00599D30 (single-caller claim) ---
text = None
for (n, vaddr, vsize, rptr, rsize) in secs:
    if n == ".text":
        text = (vaddr, vsize, rptr, rsize)
tvaddr, tvsize, trptr, trsize = text
tva0 = image_base + tvaddr
tbytes = data[trptr:trptr + trsize]
emit(f"\n== S5 .text census: VA range 0x{tva0:08X}..0x{tva0+trsize:08X} ({trsize} B)")

def census(targets, label):
    emit(f"\n== census {label}")
    for tgt, nm in targets.items():
        sites_e8, sites_e9 = [], []
        for p in range(len(tbytes) - 5):
            if tbytes[p] == 0xE8:
                rel = struct.unpack_from("<i", tbytes, p + 1)[0]
                if tva0 + p + 5 + rel == tgt:
                    sites_e8.append(tva0 + p)
            if tbytes[p] == 0xE9:
                rel = struct.unpack_from("<i", tbytes, p + 1)[0]
                if tva0 + p + 5 + rel == tgt:
                    sites_e9.append(tva0 + p)
        emit(f"  0x{tgt:08X} {nm}: E8 sites={[f'0x{s:08X}' for s in sites_e8]} E9(jmp) sites={[f'0x{s:08X}' for s in sites_e9]}")

MACHINERY = {
    0x0072F580: "FUN_0072F580 registry_lookup",
    0x0043A550: "FUN_0043A550 registry_singleton_getter",
    0x0072FA30: "FUN_0072FA30 templates_reader",
    0x00730C90: "FUN_00730C90 template_parse",
    0x007CE1E0: "FUN_007CE1E0 A_getter",
    0x006C3F50: "FUN_006C3F50 model_request_pair_emitter",
    0x008BD720: "FUN_008BD720 scheduler_callback",
    0x0072F8D0: "FUN_0072F8D0 rbtree_insert",
    0x0072FE30: "FUN_0072FE30 template_list2_out",
    0x004D1430: "FUN_004D1430 generic_rbtree_mapfind",
    0x006CB6F0: "FUN_006CB6F0 instance_creator",
}
census({0x00599D30: "FUN_00599D30 (containing)"}, "S5 single-caller check")
census(MACHINERY, "S6 machinery set — ALL .text direct call sites (byte-level superset)")

CHAIN = {
    0x008DFCD0: "FUN_008DFCD0 consumer4057",
    0x008F0780: "FUN_008F0780 consumer886",
    0x008E7B80: "FUN_008E7B80 subobject_producer",
    0x008DF3F0: "FUN_008DF3F0 guard_helper",
    0x008DFB70: "FUN_008DFB70 store",
    0x008F01C0: "FUN_008F01C0 store886",
    0x00414170: "FUN_00414170 stringtable_lazy_getter",
    0x00821BB0: "FUN_00821BB0 on_ret",
    0x00821760: "FUN_00821760 id_to_string",
    0x00826A50: "FUN_00826A50 key_part1_table_getter",
    0x00415670: "FUN_00415670 mgr98_lazy_getter",
    0x00823C10: "FUN_00823C10 extract_composite_key",
    0x00821FB0: "FUN_00821FB0 singleton_init_sids",
    0x00821E70: "FUN_00821E70 sids_parser",
    0x008221C0: "FUN_008221C0 stringtable_ctor",
    0x00824C70: "FUN_00824C70 mgr98_ctor(NOT_CHECKED)",
}
census(CHAIN, "S7 chain set — ALL .text direct call sites (byte-level superset; for provenance context)")

# --- S7: chain byte dumps + link recomputation ---
emit("\n== S7 chain dumps")
dump(0x008DFCD0, 160, "FUN_008DFCD0 body 0x008DFCD0..0x008DFD6F")
dump(0x00414170, 96, "FUN_00414170 lazy getter 0x00414170..+0x5F")
dump(0x00821BB0, 160, "FUN_00821BB0 window 0x00821BB0..0x00821C4F")
dump(0x00821760, 288, "FUN_00821760 window 0x00821760..0x0082187F")
dump(0x00823C10, 144, "FUN_00823C10 window 0x00823C10..0x00823C9F")
dump(0x004D1430, 64, "FUN_004D1430 generic mapfind shape 0x004D1430..+0x3F")
dump(0x008DFB70, 192, "FUN_008DFB70 store 0x008DFB70..0x008DFC2F")
dump(0x008F0780, 160, "FUN_008F0780 consumer886 0x008F0780..+0x9F")
dump(0x008F01C0, 96, "FUN_008F01C0 store886 0x008F01C0..+0x5F")
dump(0x008E7B80, 32, "FUN_008E7B80 producer 0x008E7B80..+0x1F")
dump(0x00415670, 96, "FUN_00415670 mgr getter 0x00415670..+0x5F")
dump(0x00826A50, 32, "FUN_00826A50 table getter 0x00826A50..+0x1F")
dump(0x00821FB0, 288, "FUN_00821FB0 singleton init (sids file open) 0x00821FB0..0x008220CF")
dump(0x00821E70, 176, "FUN_00821E70 sids parser 0x00821E70..+0xAF")
dump(0x008221C0, 96, "FUN_008221C0 stringtable ctor 0x008221C0..+0x5F")

emit("\n== S7 link recomputation (claimed call sites)")
for (va, claim) in [
    (0x0059AB0D, "0x008DF3F0"), (0x0059AB1E, "0x008DFCD0"), (0x0059AB32, "0x008E7B80"),
    (0x0059AB46, "0x008F0780"), (0x008DFD18, "0x00414170"), (0x008DFD1F, "0x00821BB0"),
    (0x008DFD2C, "0x008DFB70"), (0x00821C31, "0x00821760"), (0x008217CE, "0x00826A50"),
    (0x008217F3, "0x00415670"), (0x008217FA, "0x00823C10"), (0x00823C57, "0x004D1430"),
]:
    t = call_target(va)
    off, _ = va2off(va)
    op = data[off]
    emit(f"  @0x{va:08X} opcode=0x{op:02X} target=0x{t:08X} claim={claim} MATCH={('0x%08X' % t)==claim}")

# --- S8: FUN_0072F580 + FUN_0043A550 (registry consumer + getter) ---
dump(0x0072F580, 176, "S8 FUN_0072F580 registry lookup 0x0072F580..+0xAF")
dump(0x0043A550, 96, "S8 FUN_0043A550 registry singleton getter 0x0043A550..+0x5F")

# --- S9: absolute references in .text to singletons/vtables ---
emit("\n== S9 absolute 4-byte refs in .text")
for addr, nm in [(0x00BA124C, "stringtable_singleton_DAT"), (0x00BA12F4, "mgr98_DAT"),
                 (0x00BA1824, "registry_DAT"), (0x00A7A948, "ArkUI_Component_vftable")]:
    pat = struct.pack("<I", addr)
    hits = []
    start = 0
    while True:
        p = tbytes.find(pat, start)
        if p < 0:
            break
        hits.append(tva0 + p)
        start = p + 1
    emit(f"  0x{addr:08X} {nm}: {len(hits)} byte-pattern sites: {[f'0x{x:08X}' for x in hits[:40]]}")

# --- S10: string searches ---
emit("\n== S10 string searches (whole EXE)")
for s in [b"ArkRepairUI_Impl", b"ArkRepairUI", b"parameters\\sids.vfs", b"Parameters\\sids.vfs",
          b"sids.vfs", b"Parameters\\templates.vfs", b"S_REPAIR_UI_CLEAR_TOOLTIP"]:
    hits = []
    start = 0
    while True:
        p = data.find(s, start)
        if p < 0:
            break
        hits.append(p)
        start = p + 1
    emit(f"  {s!r}: {len(hits)} sites: {[hex(h) for h in hits[:20]]}")
# verify mapper anchor string claim at VA 0x00A86D30
off, sec = va2off(0x00A86D30)
emit(f"  anchor 0x00A86D30 -> file_off={off} sec={sec} bytes={data[off:off+24]!r}")

# --- S11: immediate census of FUN_00599D30 (byte-level superset) ---
emit("\n== S11 PUSH imm32 byte-census in FUN_00599D30 body [0x00599D30,0x0059AC88)")
fstart, _ = va2off(0x00599D30)
fend, _ = va2off(0x0059AC88)
body = data[fstart:fend]
imm = {}
sites = []
for p in range(len(body) - 5):
    if body[p] == 0x68:
        v = struct.unpack_from("<I", body, p + 1)[0]
        imm.setdefault(v, []).append(0x00599D30 + p)
        sites.append((0x00599D30 + p, v))
emit(f"  byte-level 68 xx xx xx xx sites: {len(sites)}, unique imm32 values: {len(imm)} (claim: 62 unique Ghidra-decoded PUSHes)")
uvals = sorted(imm.keys())
emit(f"  unique values: {[hex(v) for v in uvals]}")
emit("\n  -- series 0xFD4..0xFD9 push sites + following pattern --")
for v in [0xFD4, 0xFD5, 0xFD6, 0xFD7, 0xFD8, 0xFD9, 0xFAB, 0xFAE, 0xFAF, 0xFB0, 0xFB1, 0xFB2, 0x376]:
    for site in imm.get(v, []):
        off2, _ = va2off(site)
        nxt = data[off2:off2 + 20]
        emit(f"  PUSH 0x{v:X} @0x{site:08X} next20={' '.join(f'{x:02X}' for x in nxt)}")

# --- S12: indirect call byte-shapes census (plausibility vs '7 indirect') ---
emit("\n== S12 indirect-call byte shapes in FUN_00599D30 body (FF /2 superset)")
cnt = 0
for p in range(len(body) - 2):
    if body[p] == 0xFF:
        m = body[p + 1]
        if 0xD0 <= m <= 0xD7 or 0x10 <= m <= 0x17 or m == 0x15 or m == 0x55 or m == 0x95 or m == 0x91 or m == 0x50 or m == 0x90:
            cnt += 1
            emit(f"  candidate @0x{0x00599D30+p:08X}: FF {m:02X}")
emit(f"  total FF-call byte-shape candidates: {cnt}")

# --- S13: RTTI gate verification ---
emit("\n== S13 RTTI gate bytes")
p = data.find(b"ArkRepairUI_Impl\x00")
emit(f"  'ArkRepairUI_Impl' string at file_off=0x{p:X}" if p >= 0 else "  STRING NOT FOUND")
if p >= 0:
    td_va = image_base + 0  # placeholder; compute via reverse va2off
    # find section containing file offset p
    for (n, vaddr, vsize, rptr, rsize) in secs:
        if rptr <= p < rptr + rsize:
            td_va = image_base + vaddr + (p - rptr) - 0x0C
            emit(f"  string in section {n}; TypeDescriptor VA (name-0x0C) = 0x{td_va:08X}")
    pat = b"\x68" + struct.pack("<I", td_va)
    start = 0
    pushsites = []
    while True:
        q = tbytes.find(pat, start)
        if q < 0:
            break
        pushsites.append(tva0 + q)
        start = q + 1
    emit(f"  PUSH TD_VA(0x{td_va:08X}) byte-pattern sites in .text: {[f'0x{x:08X}' for x in pushsites]}")
    td_dump = dump(td_va, 32, "TypeDescriptor region (vftable/spare/name)")

emit("\n== DONE")
out.close()
