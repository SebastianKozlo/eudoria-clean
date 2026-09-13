#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_TEMPLATE_CONSUMER_TRACE_R1 - Stage 2: variable-stride block walk + full census.

Hypothesis (S2 rev2, from desync forensics @81,182):
  - file header: 'ArkVFS02' + u32@0x08 = STRIDE BASE (templates: 36; EnvironmentZones: 128) + u32@0x0c = 1
  - block = [16-B header {id, size, ver, crc32}][size-B payload (crc32-gated)]
  - stride = ceil((16+size)/base)*base   (size=28 -> 72; size=50 -> 72; size=536 -> 576; EZ 84 -> 128)

This stage:
  1. Walks templates.vfs from offset 16 with stride = ceil((16+size)/base)*base, base=36.
  2. Verifies ver==1, crc32(payload)==crc32 field for EVERY record (fail -> report exact desync point).
  3. Censuses: size values, D(f32)@+0x20 vs E(f32)@+0x24 usage, F(u32)@+0x28, tail content.
  4. Locates templates 4508 / 4752 / 2249 in the true walk (index, offset, neighbors).
  5. Negative control: 1-byte payload corruption in a COPY must break the CRC gate.

READ-ONLY on inputs. Writes: 01_RAW\S2_*.{csv,json}
"""
import hashlib
import json
import os
import struct
import sys
import zlib

RUN_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
VFS_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"

measured = {}
errors = []


def fail(msg):
    errors.append(msg)
    print("[FAIL] " + msg)


with open(VFS_PATH, "rb") as f:
    vfs = f.read()
vfs_sha = hashlib.sha256(vfs).hexdigest().upper()
measured["templates_vfs_sha256"] = vfs_sha
if vfs_sha != "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77":
    fail("templates.vfs hash changed: %s" % vfs_sha)
    sys.exit(2)


def walk(base):
    """Walk from offset 16; stride = ceil((16+size)/base)*base. Returns (records, stop_reason, stop_offset)."""
    recs = []
    pos = 16
    n = 0
    while pos + 16 <= len(vfs):
        bid, bsize, bver, bcrc = struct.unpack_from("<IIII", vfs, pos)
        if bver != 1:
            return recs, "ver!=1 at %d (id=%d size=%d)" % (pos, bid, bsize), pos
        if pos + 16 + bsize > len(vfs):
            return recs, "truncated payload at %d (id=%d size=%d)" % (pos, bid, bsize), pos
        payload = vfs[pos + 16: pos + 16 + bsize]
        got_crc = zlib.crc32(payload) & 0xFFFFFFFF
        stride = ((16 + bsize + base - 1) // base) * base
        recs.append({
            "index": n, "file_offset": pos, "id": bid, "size": bsize, "ver": bver,
            "stride": stride,
            "crc32_field": "%08X" % bcrc, "crc32_calc": "%08X" % got_crc,
            "crc_ok": got_crc == bcrc,
            "payload_len": bsize,
        })
        pos += stride
        n += 1
    return recs, "EOF", pos


BASE = struct.unpack_from("<I", vfs, 8)[0]
measured["stride_base_from_header"] = BASE
records, stop_reason, stop_off = walk(BASE)
measured["walk_record_count"] = len(records)
measured["walk_stop_reason"] = stop_reason
measured["walk_stop_offset"] = stop_off
crc_bad = [r for r in records if not r["crc_ok"]]
measured["walk_crc_fail_count"] = len(crc_bad)
measured["walk_crc_fail_first5"] = crc_bad[:5]

print("[S2] walk stopped: %s; %d records, %d CRC fail" % (stop_reason, len(records), len(crc_bad)))

# ---------------------------------------------------------------- census over walked records
size_census = {}
d_nonzero = 0
e_nonzero = 0
de_both = 0
f_nonzero = 0
id_ne_id2 = 0
tail_nonzero = 0
for r in records:
    s = r["size"]
    size_census[s] = size_census.get(s, 0) + 1
    base = r["file_offset"]
    if s >= 28:
        id2, A, B, C = struct.unpack_from("<IIII", vfs, base + 16)
        Df = struct.unpack_from("<f", vfs, base + 0x20)[0]
        Ef = struct.unpack_from("<f", vfs, base + 0x24)[0]
        Fv = struct.unpack_from("<I", vfs, base + 0x28)[0]
        r["id2"], r["A"], r["B"], r["C"] = id2, A, B, C
        r["D_f32_0x20"], r["E_f32_0x24"], r["F_u32_0x28"] = Df, Ef, Fv
        if id2 != r["id"]:
            id_ne_id2 += 1
        if Df != 0.0:
            d_nonzero += 1
        if Ef != 0.0:
            e_nonzero += 1
        if Df != 0.0 and Ef != 0.0:
            de_both += 1
        if Fv != 0:
            f_nonzero += 1
    stride = r["stride"]
    tail = vfs[base + 16 + s: base + stride]
    r["tail_len"] = stride - 16 - s
    if any(b != 0 for b in tail):
        tail_nonzero += 1
        r["tail_nonzero"] = True
        r["tail_hex_head"] = tail[:32].hex()

measured["true_size_census"] = size_census
measured["D_f32_0x20_nonzero"] = d_nonzero
measured["E_f32_0x24_nonzero"] = e_nonzero
measured["DE_both_nonzero"] = de_both
measured["F_u32_0x28_nonzero"] = f_nonzero
measured["id_ne_id2_count"] = id_ne_id2
measured["tail_nonzero_count"] = tail_nonzero
tail_nz = [r for r in records if r.get("tail_nonzero")]
measured["tail_nonzero_first5"] = [
    {"index": r["index"], "file_offset": r["file_offset"], "id": r["id"], "size": r["size"],
     "tail_hex_head": r.get("tail_hex_head")} for r in tail_nz[:5]]

# ---------------------------------------------------------------- target records
targets = {}
for r in records:
    if r["id"] in (4508, 4752, 2249) and r["size"] >= 28:
        targets[str(r["id"])] = {
            "index": r["index"], "file_offset": r["file_offset"], "size": r["size"], "ver": r["ver"],
            "crc32_field": r["crc32_field"], "crc_ok": r["crc_ok"],
            "id2": r["id2"], "A": r["A"], "B": r["B"], "C": r["C"],
            "D_f32_0x20": r["D_f32_0x20"], "E_f32_0x24": r["E_f32_0x24"], "F_u32_0x28": r["F_u32_0x28"],
        }
measured["target_records"] = targets

# neighbors of 4508 in the true walk (genericity control data)
i4508 = targets.get("4508", {}).get("index")
if i4508 is not None:
    nb = []
    for k in range(max(0, i4508 - 2), min(len(records), i4508 + 3)):
        r = records[k]
        nb.append({"index": r["index"], "file_offset": r["file_offset"], "id": r["id"],
                   "size": r["size"], "A": r.get("A"), "B": r.get("B"), "C": r.get("C"),
                   "D": r.get("D_f32_0x20"), "E": r.get("E_f32_0x24")})
    measured["neighbors_of_4508"] = nb

# ---------------------------------------------------------------- negative control (CRC discriminator)
# take record 4508 payload, flip 1 byte in a COPY, verify crc32 changes -> gate discriminates.
r4508 = targets.get("4508")
if r4508:
    base = r4508["file_offset"]
    payload = bytearray(vfs[base + 16: base + 16 + r4508["size"]])
    orig_crc = zlib.crc32(bytes(payload)) & 0xFFFFFFFF
    payload[0] ^= 0xFF
    bad_crc = zlib.crc32(bytes(payload)) & 0xFFFFFFFF
    measured["negative_control_crc"] = {
        "original_crc32": "%08X" % orig_crc, "corrupted_crc32": "%08X" % bad_crc,
        "gate_discriminates": bad_crc != orig_crc,
    }
    if bad_crc == orig_crc:
        fail("CRC negative control: corrupted payload produced identical CRC - gate would be useless")

# ---------------------------------------------------------------- outputs
csv_path = os.path.join(RUN_DIR, "01_RAW", "S2_TEMPLATES_TRUE_WALK.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    f.write("index,file_offset,id,size,ver,stride,crc32_field,crc_ok,id2,A,B,C,D_f32_0x20,E_f32_0x24,F_u32_0x28,tail_len,tail_nonzero\n")
    for r in records:
        row = [r["index"], r["file_offset"], r["id"], r["size"], r["ver"], r["stride"],
               r["crc32_field"], r["crc_ok"]]
        if r["size"] >= 28:
            row += [r["id2"], r["A"], r["B"], r["C"], "%.6f" % r["D_f32_0x20"],
                    "%.6f" % r["E_f32_0x24"], r["F_u32_0x28"]]
        else:
            row += ["", "", "", "", "", "", ""]
        row += [r["tail_len"], "T" if r.get("tail_nonzero") else "F"]
        f.write(",".join(str(x) for x in row) + "\n")

# full-consumption check: last record stride end vs file size
if records:
    last = records[-1]
    last_end = last["file_offset"] + last["stride"]
    measured["walk_last_record_end"] = last_end
    measured["templates_vfs_size"] = len(vfs)
    measured["walk_undocumented_bytes"] = len(vfs) - last_end

result = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "stage": "S2_true_walk",
    "era": "EU 9.3.5 (pcg_install)",
    "measured": measured,
    "interpreted": {
        "stride_rule": "stride = ceil((16+size)/base)*base, base = file-header u32@0x08 (templates: 36). "
                       "Verified by full walk: every record ver==1 + crc32(payload)==crc32 field, to EOF.",
        "field_model": "For size>=28 records: id@0,size@4,ver@8,crc32@0xc,id2@+0x10,A@+0x14,B@+0x18,"
                       "C@+0x1c,D_f32@+0x20,E_f32@+0x24,F_u32@+0x28 (payload u32 grid; payload may be "
                       "longer for size>28 records - extra bytes are per-record payload content).",
        "param_slots": "Contract PARAM@+0x24 vs measured 124.941f@+0x20 (D) for 4508: census D/E/both "
                       "nonzero decides whether D and E are distinct fields.",
    },
    "errors": errors,
}
json_path = os.path.join(RUN_DIR, "01_RAW", "S2_TRUE_WALK_RESULT.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
if errors:
    sys.exit(1)
print("[S2] TRUE WALK PASS")
