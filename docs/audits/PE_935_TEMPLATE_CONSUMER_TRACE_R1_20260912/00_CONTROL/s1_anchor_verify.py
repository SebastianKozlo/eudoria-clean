#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_TEMPLATE_CONSUMER_TRACE_R1 - Stage 1: input anchoring.

READ-ONLY. Verifies:
  1. Entropia.exe SHA256 == E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8,015,872 B)
  2. templates.vfs identity + ArkVFS02 magic + block model on templates 4508 / 4752 / 2249
  3. Block-header model {id, size, ver, crc32} + CRC32(payload) == crc32 field (generic VFS reader gate,
     per PE_PLACEMENT_ARCH_PROBE_CONTINUATION_R1 block model, re-measured here independently)
  4. Full templates.vfs block census (stride integrity, size/ver/value census)
  5. EnvironmentZones.vfs header comparison (same-family structure check)

Outputs (run dir):
  01_RAW\S1_TEMPLATES_BLOCK_CENSUS.csv     - per-block measured values (all blocks)
  01_RAW\S1_ANCHOR_RESULT.json             - measured/interpreted/errors separation
Era: EU 9.3.5 (pcg_install). No PE2/2003 addresses used anywhere.
"""
import hashlib
import json
import os
import struct
import sys
import zlib

RUN_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
EXE_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
VFS_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
EZ_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\EnvironmentZones.vfs"

EXPECTED_EXE_SHA = "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31"
EXPECTED_EXE_SIZE = 8015872

measured = {}
errors = []


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def fail(msg):
    errors.append(msg)
    print("[FAIL] " + msg)


# ---------------------------------------------------------------- 1. binary identity
exe_sha = sha256_file(EXE_PATH)
exe_size = os.path.getsize(EXE_PATH)
measured["exe_sha256"] = exe_sha
measured["exe_size"] = exe_size
if exe_sha != EXPECTED_EXE_SHA or exe_size != EXPECTED_EXE_SIZE:
    fail("EXE identity mismatch: %s / %d B" % (exe_sha, exe_size))
    print(json.dumps({"measured": measured, "errors": errors}, indent=2))
    sys.exit(2)  # HARD STOP per contract
print("[OK] Entropia.exe SHA256 == expected E7785430...D5280F31, size %d B" % exe_size)

# ---------------------------------------------------------------- 2. templates.vfs identity
vfs_sha = sha256_file(VFS_PATH)
measured["templates_vfs_sha256"] = vfs_sha
measured["templates_vfs_size"] = os.path.getsize(VFS_PATH)
print("[OK] templates.vfs SHA256 = %s, size %d B" % (vfs_sha, measured["templates_vfs_size"]))

with open(VFS_PATH, "rb") as f:
    vfs = f.read()

magic = vfs[:8]
measured["templates_vfs_magic"] = magic.decode("ascii", "replace")
if magic != b"ArkVFS02":
    fail("templates.vfs magic mismatch: %r" % magic)

# file header: u32 @0x08, u32 @0x0c
hdr_a, hdr_b = struct.unpack_from("<II", vfs, 8)
measured["templates_vfs_hdr_u32_08"] = hdr_a
measured["templates_vfs_hdr_u32_0c"] = hdr_b

# ---------------------------------------------------------------- 3. block model
STRIDE = 72
PAYLOAD_START = 16  # block header {id@0,size@4,ver@8,crc32@12} then payload @16
records_start = 16  # first block at file offset 16
n_blocks = (len(vfs) - records_start) // STRIDE
measured["templates_vfs_block_count"] = n_blocks
resid = (len(vfs) - records_start) % STRIDE
measured["templates_vfs_residual_bytes"] = resid

crc_fail = 0
size_census = {}
ver_census = {}
blocks = []
anomalies = []
bad_stride = 0
for i in range(n_blocks):
    base = records_start + i * STRIDE
    bid, bsize, bver, bcrc = struct.unpack_from("<IIII", vfs, base)
    payload = vfs[base + PAYLOAD_START: base + PAYLOAD_START + bsize]
    got_crc = zlib.crc32(payload) & 0xFFFFFFFF
    ok_crc = (got_crc == bcrc)
    if not ok_crc:
        crc_fail += 1
    size_census[bsize] = size_census.get(bsize, 0) + 1
    ver_census[bver] = ver_census.get(bver, 0) + 1
    # payload fields (payload-relative): id2@0, A@4, B@8, C@12, f32@16 (=record+0x20), f32@20 (=record+0x24)
    anomaly = (bsize < 16) or (base + PAYLOAD_START + bsize > len(vfs))
    if anomaly:
        anomalies.append({"index": i, "file_offset": base, "id": bid, "size": bsize, "ver": bver,
                          "crc32_field": "%08X" % bcrc})
        id2 = A = B = C = 0
        param_f32 = param2_f32 = 0.0
        pad = b""
        pad_all_zero = True
    else:
        id2, A, B, C = struct.unpack_from("<IIII", vfs, base + PAYLOAD_START)
        param_f32 = struct.unpack_from("<f", vfs, base + 0x20)[0]
        param2_f32 = struct.unpack_from("<f", vfs, base + 0x24)[0]
        pad = vfs[base + PAYLOAD_START + bsize: base + STRIDE]
        pad_all_zero = all(b == 0 for b in pad)
    blocks.append({
        "index": i, "file_offset": base, "id": bid, "size": bsize, "ver": bver,
        "crc32_field": "%08X" % bcrc, "crc32_calc": "%08X" % got_crc, "crc_ok": ok_crc,
        "id2": id2, "A": A, "B": B, "C": C, "param_f32": param_f32,
        "param2_f32": param2_f32, "anomaly": anomaly,
        "pad_len": STRIDE - PAYLOAD_START - bsize, "pad_all_zero": pad_all_zero,
    })
    if bid != id2 and not anomaly:
        bad_stride += 1  # not fatal, but census it

measured["templates_vfs_crc_fail_count"] = crc_fail
measured["templates_vfs_size_census"] = size_census
measured["templates_vfs_ver_census"] = ver_census
measured["templates_vfs_id_ne_id2_count"] = bad_stride
measured["templates_vfs_pad_nonzero_count"] = sum(1 for b in blocks if not b["pad_all_zero"])
measured["param_f32_at_0x20_nonzero_count"] = sum(1 for b in blocks if b["param_f32"] != 0.0)
measured["param2_f32_at_0x24_nonzero_count"] = sum(1 for b in blocks if b["param2_f32"] != 0.0)
measured["anomaly_block_count"] = len(anomalies)
measured["anomaly_blocks_first10"] = anomalies[:10]

# ---------------------------------------------------------------- 4. target records
targets = {"4508": 96496, "4752": 97288, "2249": 93976}
parent_stated = {"4508": 96496, "4752": 97294, "2249": 93982}
anchor = {}
for tid, off in targets.items():
    b = None
    for blk in blocks:
        if blk["file_offset"] == off:
            b = blk
            break
    if b is None:
        fail("target record %s not found at measured offset %d" % (tid, off))
        continue
    anchor[tid] = {
        "measured_record_start": off,
        "parent_stated_record_start": parent_stated[tid],
        "offset_delta_vs_parent": parent_stated[tid] - off,
        "id": b["id"], "size": b["size"], "ver": b["ver"],
        "crc32_field": b["crc32_field"], "crc_ok": b["crc_ok"],
        "id2": b["id2"], "A": b["A"], "B": b["B"], "C": b["C"],
        "param_f32": b["param_f32"],
    }
measured["target_records"] = anchor

# expected values from the contract
exp = {
    "4508": dict(A=296445, B=296446, C=0, param=124.941, crc="AFF5797C"),
    "4752": dict(A=126740, B=126741, C=None, param=None, crc=None),
    "2249": dict(A=278453, B=278454, C=None, param=None, crc=None),
}
for tid, e in exp.items():
    a = anchor.get(tid)
    if not a:
        continue
    if a["A"] != e["A"]:
        fail("template %s A mismatch: got %d, contract expects %d" % (tid, a["A"], e["A"]))
    if a["B"] != e["B"]:
        fail("template %s B mismatch: got %d, contract expects %d" % (tid, a["B"], e["B"]))
    if e["crc"] and a["crc32_field"].upper() != e["crc"]:
        fail("template %s crc field mismatch: got %s, contract expects %s" % (tid, a["crc32_field"], e["crc"]))
    if tid == "4508" and abs(a["param_f32"] - e["param"]) > 0.01:
        fail("template 4508 PARAM mismatch: got %f, contract expects %f" % (a["param_f32"], e["param"]))

# ---------------------------------------------------------------- 5. EnvironmentZones comparison
ez_sha = sha256_file(EZ_PATH)
measured["environmentzones_vfs_sha256"] = ez_sha
with open(EZ_PATH, "rb") as f:
    ez = f.read(64)
ez_hdr = struct.unpack_from("<8sII", ez, 0)
measured["environmentzones_vfs_magic"] = ez_hdr[0].decode("ascii", "replace")
measured["environmentzones_vfs_hdr_u32_08"] = ez_hdr[1]
measured["environmentzones_vfs_hdr_u32_0c"] = ez_hdr[2]

# ---------------------------------------------------------------- 6. write outputs
os.makedirs(os.path.join(RUN_DIR, "01_RAW"), exist_ok=True)
csv_path = os.path.join(RUN_DIR, "01_RAW", "S1_TEMPLATES_BLOCK_CENSUS.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    f.write("index,file_offset,id,size,ver,crc32_field,crc32_calc,crc_ok,id2,A,B,C,param_f32_0x20,param2_f32_0x24,pad_len,pad_all_zero,anomaly\n")
    for b in blocks:
        f.write("%d,%d,%d,%d,%d,%s,%s,%s,%d,%d,%d,%d,%.6f,%.6f,%d,%s,%s\n" % (
            b["index"], b["file_offset"], b["id"], b["size"], b["ver"],
            b["crc32_field"], b["crc32_calc"], b["crc_ok"],
            b["id2"], b["A"], b["B"], b["C"], b["param_f32"], b["param2_f32"],
            b["pad_len"], b["pad_all_zero"], b["anomaly"]))

result = {
    "run_id": "PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912",
    "stage": "S1_anchor_verify",
    "era": "EU 9.3.5 (pcg_install)",
    "measured": measured,
    "interpreted": {
        "block_model": "templates.vfs = 'ArkVFS02' + u32@0x08(=36) + u32@0x0c(=1) + N blocks of stride 72: "
                       "[16-B header {id, size, ver, crc32}][size-B payload][pad to stride]. "
                       "Payload fields (payload-relative): id2@0, A@4, B@8, C@12, f32@16. "
                       "Record-relative (header-inclusive): id2@+0x10, A@+0x14, B@+0x18, C@+0x1c, f32@+0x20, f32@+0x24.",
        "crc_gate": "zlib.crc32 over size-B payload == crc32 field for all blocks (if crc_fail==0), "
                    "consistent with the generic VFS record-read CRC gate measured in "
                    "PE_PLACEMENT_ARCH_PROBE_CONTINUATION_R1 (FUN_00971ad0) - re-measured here on templates.vfs.",
        "param_offset": "Contract says PARAM f32 @+0x24; measured: the 124.941f value for template 4508 "
                        "sits at record+0x20 (96,528). Census of BOTH slots f32@+0x20 and f32@+0x24 across "
                        "the whole corpus decides which slot carries the value (see param*_nonzero_count).",
        "sibling_offsets": "Parent contract stated record starts 97,294 (4752) and 93,982 (2249); "
                            "measured starts are 97,288 and 93,976 (delta +6 each). Content (A/B) matches "
                            "the contract exactly. The +6 delta is recorded as PROMPT_OFFSET_DELTA (not blocking).",
    },
    "errors": errors,
}
json_path = os.path.join(RUN_DIR, "01_RAW", "S1_ANCHOR_RESULT.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
print("\n[S1] csv=%s json=%s" % (csv_path, json_path))
if errors:
    sys.exit(1)
print("[S1] ALL ANCHOR CHECKS PASS")
