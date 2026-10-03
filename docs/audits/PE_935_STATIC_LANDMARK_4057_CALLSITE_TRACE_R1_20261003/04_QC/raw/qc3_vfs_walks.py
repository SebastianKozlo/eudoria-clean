# QC3: independent full walks: templates.vfs (5,438-record census + record 4057/4508 + CRC recompute
# + id2 census 4052..4057), sids.vfs (3,887-entry closure + 0xFD9/0x376 extraction)
import struct, zlib

TVFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
SVFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\sids.vfs"
OUTP = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003\04_QC\raw\qc3_output.txt"
out = open(OUTP, "w", encoding="utf-8")
def emit(s=""):
    print(s); out.write(s + "\n")

td = open(TVFS, "rb").read()
emit(f"== templates.vfs walk (size={len(td)}) magic={td[:8]!r}")
emit(f"  container header fields: @8={struct.unpack_from('<I', td, 8)[0]} @12={struct.unpack_from('<I', td, 12)[0]}")
STRIDE = 72
pos = 16
records = []
crc_fail = 0
crc_checked = 0
while pos < len(td):
    if pos + 16 > len(td):
        emit(f"  TRUNCATED HEADER at {pos}"); break
    rid, size, ver, crc = struct.unpack_from("<IIII", td, pos)
    if size > len(td) - pos - 16:
        emit(f"  BAD SIZE at {pos}: id={rid} size={size} -> desync"); break
    payload = td[pos+16 : pos+16+size]
    crc_checked += 1
    if zlib.crc32(payload) & 0xFFFFFFFF != crc:
        crc_fail += 1
        if crc_fail <= 5:
            emit(f"  CRC MISMATCH rec id={rid} @ {pos}: field={crc:08X} recomputed={zlib.crc32(payload)&0xFFFFFFFF:08X}")
    records.append((pos, rid, size, ver, crc, payload))
    total = 16 + size
    advance = ((total + STRIDE - 1) // STRIDE) * STRIDE
    pos += advance
emit(f"  WALK RESULT: records={len(records)} end_pos={pos} file_size={len(td)} eof_exact={pos==len(td)}")
emit(f"  crc recomputed over {crc_checked} records; failures={crc_fail} (claim: 5438 records, 0 CRC fail, EOF exact)")
ids = [r[1] for r in records]
emit(f"  unique ids: {len(set(ids))} (claim 5438 unique, no duplicates); duplicates: {[i for i in set(ids) if ids.count(i)>1][:10]}")
# record anchors
for want, label in [(4057, "record_4057"), (4508, "record_4508")]:
    hit = [r for r in records if r[1] == want]
    if hit:
        p, rid, size, ver, crc, pl = hit[0]
        emit(f"  {label}: offset={p} (claim {88792 if want==4057 else 96496}) size={size} ver={ver} crc={crc:08X} MATCH_OFFSET={p==(88792 if want==4057 else 96496)}")
        emit(f"    payload_hex={pl.hex(' ')}")
        f = struct.unpack_from("<7I", pl) if len(pl) >= 28 else ()
        if len(pl) >= 28:
            import struct as s2
            d_f32 = s2.unpack_from("<f", pl, 16)[0]
            emit(f"    id2={f[0]} A={f[1]} B={f[2]} C={f[3]} D_u32={f[4]} D_f32={d_f32:.6f} l1={f[5]} l2_or_f11={f[6]}")
    else:
        emit(f"  {label}: NOT FOUND")
# id2 census for the series 0xFD4..0xFD9 = 4052..4057
emit("  id2-existence census for series 4052..4057 (claim: only 4054 & 4057 PRESENT):")
idset = set(ids)
for v in range(4052, 4058):
    emit(f"    id2={v} (0x{v:04X}): {'PRESENT' if v in idset else 'ABSENT'}")
# sanity: dump next-record header after 4057
emit(f"  record after 4057 (pos {88792+72}): {struct.unpack_from('<II', td, 88792+72)[:4]}")

sd = open(SVFS, "rb").read()
emit(f"\n== sids.vfs parse (size={len(sd)}) magic={sd[:8]!r}")
rid, size, ver, crc = struct.unpack_from("<IIII", sd, 16)
emit(f"  container record @16: id={rid} size={size} ver={ver} crc={crc:08X} (claim: id=1, size=128996, ver=1, crc field=0)")
payload = sd[32:32+size]
emit(f"  payload [{32}..{32+size}) len={len(payload)}")

def parse_entries(start, count, label):
    p = start
    ents = []
    ok = True
    for i in range(count):
        if p + 2 > len(payload): ok = False; break
        ln = struct.unpack_from("<H", payload, p)[0]
        p += 2
        if p + ln + 4 > len(payload): ok = False; break
        s = payload[p:p+ln]; p += ln
        eid = struct.unpack_from("<I", payload, p)[0]; p += 4
        ents.append((eid, s.decode("ascii", "replace")))
    emit(f"  [{label}] start={start} parsed={len(ents)} end_pos={p} (payload len {len(payload)}) closure_exact={p==len(payload)}")
    return ents, p == len(payload)

cnt32 = struct.unpack_from("<I", payload, 0)[0]
cnt16 = struct.unpack_from("<H", payload, 0)[0]
emit(f"  count u32@0={cnt32} u16@0={cnt16} (claim 3887)")
eA, cA = parse_entries(8, cnt32, "LayoutA: u32 count + u32 X(2021) + entries")
eB, cB = parse_entries(2, cnt16, "LayoutB: u16 count + entries (claimed wording)")
best = eA if cA and not cB else (eB if cB and not cA else (eA if cA else eB))
emit(f"  LayoutA closes={cA} LayoutB closes={cB}")
ents = best
emit(f"  chosen entries={len(ents)} unique ids={len(set(e[0] for e in ents))} (claim: 3887/3887 unique)")
want = {0xFD9: "S_REPAIR_UI_CLEAR_TOOLTIP", 0x376: "S_GENERIC_CLEAR", 0xFD4: "S_REPAIR_UI_ADD_EQUIPPED_TOOLTIP",
        0xFD5: "S_REPAIR_UI_ADD_WEAPONS_TOOLTIP", 0xFD6: "S_REPAIR_UI_ADD_ARMOR_TOOLTIP",
        0xFD7: "S_REPAIR_UI_ADD_TOOLS_TOOLTIP", 0xFD8: "S_REPAIR_UI_ADD_ALL_TOOLTIP",
        0xFAB: "S_REPAIR_UI_ADD_EQUIPPED", 0xFAE: "S_REPAIR_UI_ADD_WEAPONS", 0xFAF: "S_REPAIR_UI_ADD_ARMOR",
        0xFB0: "S_REPAIR_UI_ADD_TOOLS", 0xFB1: "S_REPAIR_UI_ADD_ALL", 0xFB2: "S_REPAIR_UI_DRAG_ITEMS_HERE"}
d = dict(ents)
for k, exp in sorted(want.items()):
    got = d.get(k)
    emit(f"    id 0x{k:04X} ({k}): {got!r} MATCH={got==exp}")
emit(f"  first 3 entries: {ents[:3]}")
emit(f"  last entry: {ents[-1]}")
emit("\n== DONE qc3")
out.close()
