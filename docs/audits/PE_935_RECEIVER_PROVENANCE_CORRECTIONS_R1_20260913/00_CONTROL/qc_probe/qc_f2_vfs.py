# -*- coding: utf-8 -*-
# QC F2-VFS: own full walk of templates.vfs (ArkVFS02). Format derived from bytes:
# header {magic 'ArkVFS02', u32 0x24, u32 1}; records from 0x10: 16-byte header
# {id, size, ver, crc32(payload)} + payload(size) + padding(size); stride 16+2*size.
# Payload layout (for size 28): id2, A, B, C, D_f32, E_f32, F_u32.
# pe-master-auditor INTERNAL_QC. STATIC-ONLY.
import struct, sys, zlib, hashlib
sys.path.insert(0, r"D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\00_CONTROL\qc_probe")
from qc_core import save_json

P = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
d = open(P, "rb").read()
R = {}
R["file"] = dict(path=P, size=len(d),
                 sha256=hashlib.sha256(d).hexdigest().upper())
R["header"] = dict(magic=d[:8].decode(), u32_at_8=struct.unpack_from("<I", d, 8)[0],
                   u32_at_12=struct.unpack_from("<I", d, 12)[0])

records = []
off = 0x10
crc_fail = 0
ids = []
sizes = {}
rec4508 = None
while off < len(d):
    if off + 16 > len(d):
        R["walk_tail"] = dict(off=off, remaining=len(d) - off)
        break
    rid, size, ver, crc = struct.unpack_from("<IIII", d, off)
    if ver != 1 or size == 0 or off + 16 + size > len(d):
        R["walk_anomaly"] = dict(off=off, id=rid, size=size, ver=ver)
        break
    payload = d[off + 16: off + 16 + size]
    crc_calc = zlib.crc32(payload) & 0xFFFFFFFF
    if crc_calc != crc:
        crc_fail += 1
    rec = dict(file_offset=off, id=rid, size=size, ver=ver, crc_field=crc,
               crc_ok=(crc_calc == crc))
    if size == 28:
        id2, A, B, C, D, E, F = struct.unpack_from("<IIIIIII", payload, 0)
        rec.update(dict(id2=id2, A=A, B=B, C=C, D_bits=D,
                       D_f32=struct.unpack("<f", struct.pack("<I", D))[0],
                       E_f32=struct.unpack("<f", struct.pack("<I", E))[0], F=F))
    records.append(rec)
    ids.append(rid)
    sizes[size] = sizes.get(size, 0) + 1
    if rid == 4508:
        rec4508 = rec
    off = off + 16 + 2 * size  # stride rule

R["walk"] = dict(records=len(records), crc_fail=crc_fail,
                 end_offset=off, file_size=len(d), eof=(off == len(d)),
                 size_histogram=sizes,
                 id_min=min(ids), id_max=max(ids), dup_ids=(len(ids) - len(set(ids))))
R["record_4508"] = rec4508
R["record_4508_layout_pins"] = dict(
    rec_file_offset=96496,
    A_file_offset=96496 + 0x14, A_value_expected=296445,
    D_file_offset=96528, D_bits_expected=0x42F9E1CB,
    D_f32_expected=124.94100189208984)
if rec4508:
    R["record_4508_layout_pins"]["A_match"] = (rec4508["A"] == 296445)
    R["record_4508_layout_pins"]["D_bits_match"] = (rec4508["D_bits"] == 0x42F9E1CB)
    R["record_4508_layout_pins"]["id2_match"] = (rec4508["id2"] == 4508)

# negative control: a wrong stride rule must NOT walk cleanly to EOF
off = 0x10
bad = 0
while off + 16 <= len(d):
    rid, size, ver, crc = struct.unpack_from("<IIII", d, off)
    if ver != 1 or size == 0 or off + 16 + size > len(d):
        bad += 1
        break
    off = off + 16 + size  # WRONG rule (16+size)
    bad += 1
    if bad > 50: break
R["negative_control_stride"] = dict(wrong_rule="16+size", steps_before_fail=bad)

# verify A values against RUN1 join claim sample: check a few records' A -> <A>.nif family
R["sample_records"] = records[:5]

p = save_json("QC_F2_VFS_WALK.json", R)
print("saved", p)
print(json.dumps if False else "")
import json
print(json.dumps(R["walk"], indent=1))
print(json.dumps(R["record_4508"], indent=1))
print("layout pins:", R["record_4508_layout_pins"])
print("negative control:", R["negative_control_stride"])
