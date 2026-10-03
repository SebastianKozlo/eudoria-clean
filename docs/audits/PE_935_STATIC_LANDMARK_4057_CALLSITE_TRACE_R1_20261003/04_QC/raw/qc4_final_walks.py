# QC4: FINAL independent walks with byte-derived stride rule (advance = align_up(16+size, base), base = u32@8)
import struct, zlib

TVFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
SVFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\sids.vfs"
OUTP = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003\04_QC\raw\qc4_output.txt"
out = open(OUTP, "w", encoding="utf-8")
def emit(s=""):
    print(s); out.write(s + "\n")

td = open(TVFS, "rb").read()
base = struct.unpack_from("<I", td, 8)[0]
emit(f"== templates.vfs FINAL walk (size={len(td)}) magic={td[:8]!r} base={base} (stride = align_up(16+size, base))")
pos = 16
records = []
crc_fail = 0
while pos < len(td):
    rid, size, ver, crc = struct.unpack_from("<IIII", td, pos)
    if size > len(td) - pos - 16 or ver != 1:
        emit(f"  DESYNC at {pos}: id={rid} size={size} ver={ver}"); break
    payload = td[pos+16 : pos+16+size]
    if zlib.crc32(payload) & 0xFFFFFFFF != crc:
        crc_fail += 1
        if crc_fail <= 5:
            emit(f"  CRC MISMATCH id={rid} @{pos}: field={crc:08X} recomp={zlib.crc32(payload)&0xFFFFFFFF:08X}")
    records.append((pos, rid, size, ver, crc, payload))
    total = 16 + size
    pos += ((total + base - 1)//base)*base
emit(f"  WALK: records={len(records)} end_pos={pos} eof_exact={pos==len(td)} (claim: 5438, EOF exact)")
emit(f"  crc failures={crc_fail} (claim 0); unique ids={len(set(r[1] for r in records))} (claim 5438 unique)")
dups = [i for i in set(r[1] for r in records) if [r[1] for r in records].count(i) > 1]
emit(f"  duplicate ids: {dups[:10]}")
for want, off_claim in [(4057, 88792), (4508, 96496), (11963, 315916)]:
    hit = [r for r in records if r[1] == want]
    if hit:
        p, rid, size, ver, crc, pl = hit[0]
        d_f32 = struct.unpack_from("<f", pl, 16)[0] if len(pl) >= 20 else None
        emit(f"  record {want}: offset={p} MATCH_claim({off_claim})={p==off_claim} size={size} ver={ver} crc={crc:08X}")
        emit(f"    payload_hex={pl[:32].hex(' ')}{' ...' if len(pl)>32 else ''}")
        f = struct.unpack_from("<7I", pl)
        emit(f"    id2={f[0]} A={f[1]} B={f[2]} C={f[3]} D_u32={f[4]} D_f32={d_f32} l1={f[5]} l2/f11={f[6]}")
    else:
        emit(f"  record {want}: NOT FOUND")
idset = set(r[1] for r in records)
emit("  id2 census 4052..4057 (claim: only 4054 & 4057 PRESENT):")
for v in range(4052, 4058):
    emit(f"    {v} (0x{v:04X}): {'PRESENT' if v in idset else 'ABSENT'}")

sd = open(SVFS, "rb").read()
emit(f"\n== sids.vfs FINAL parse (size={len(sd)})")
sbase = struct.unpack_from("<I", sd, 8)[0]
rid, size, ver, crc = struct.unpack_from("<IIII", sd, 16)
emit(f"  base={sbase} container record @16: id={rid} size={size} ver={ver} crc={crc:08X} (claim: 1 / 128996 / 1 / 0)")
stride = ((16+size+sbase-1)//sbase)*sbase
emit(f"  record stride check: 16+{stride} == file? {16+stride == len(sd)}")
payload = sd[32:32+size]
cnt = struct.unpack_from("<H", payload, 0)[0]
emit(f"  payload len={len(payload)} u16 count={cnt} (claim 3887)")
p = 2
ents = []
ok = True
for i in range(cnt):
    if p + 2 > len(payload): ok = False; emit(f"  BOUNDS FAIL at entry {i}"); break
    ln = struct.unpack_from("<H", payload, p)[0]; p += 2
    if p + ln + 4 > len(payload): ok = False; emit(f"  BOUNDS FAIL at entry {i}"); break
    s = payload[p:p+ln]; p += ln
    eid = struct.unpack_from("<I", payload, p)[0]; p += 4
    ents.append((eid, s.decode("ascii", "replace")))
emit(f"  PARSE: entries={len(ents)} ok={ok} end_pos={p} exact_closure={p==len(payload)} (claim: 3887/3887, exact closure)")
ids = [e[0] for e in ents]
emit(f"  unique ids={len(set(ids))} duplicates={[i for i in set(ids) if ids.count(i)>1][:10]} (claim 3887 unique)")
emit(f"  first entry: {ents[0]!r}")
emit(f"  last entry: {ents[-1]!r}")
want = {0xFD9: "S_REPAIR_UI_CLEAR_TOOLTIP", 0x376: "S_GENERIC_CLEAR", 0xFD4: "S_REPAIR_UI_ADD_EQUIPPED_TOOLTIP",
         0xFD5: "S_REPAIR_UI_ADD_WEAPONS_TOOLTIP", 0xFD6: "S_REPAIR_UI_ADD_ARMOR_TOOLTIP",
         0xFD7: "S_REPAIR_UI_ADD_TOOLS_TOOLTIP", 0xFD8: "S_REPAIR_UI_ADD_ALL_TOOLTIP",
         0xFAB: "S_REPAIR_UI_ADD_EQUIPPED", 0xFAE: "S_REPAIR_UI_ADD_WEAPONS", 0xFAF: "S_REPAIR_UI_ADD_ARMOR",
         0xFB0: "S_REPAIR_UI_ADD_TOOLS", 0xFB1: "S_REPAIR_UI_ADD_ALL", 0xFB2: "S_REPAIR_UI_DRAG_ITEMS_HERE"}
d = dict(ents)
allmatch = True
for k, exp in sorted(want.items()):
    got = d.get(k)
    m = got == exp
    allmatch = allmatch and m
    emit(f"    0x{k:04X} ({k}): {got!r} MATCH={m}")
emit(f"  ALL 13 target entries MATCH = {allmatch}")
emit("\n== DONE qc4")
out.close()
