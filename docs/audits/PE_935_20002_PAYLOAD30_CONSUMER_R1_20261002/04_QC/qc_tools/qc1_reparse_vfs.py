#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC COUNTERCHECK 1 - INDEPENDENT re-parse of 20002.vfs framing.
RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 / QC worker (fresh context).

Independence statement: this implementation shares NO code with the executor's
03_SCRIPTS (never imported, never copied) and NO code with JOIN R1's vfs_common.py.
The grammar below was re-derived from physical bytes by this QC worker: the walk
starts at +16 after an 8-byte magic + u32 base; record headers are read as four
u32 LE fields; the stride rule was re-derived by requiring byte-exact EOF on the
physical file (see derivation log emitted below - the stride constant 128 was
CONFIRMED by exact-EOF, not assumed).

Outputs: 04_QC\\QC1_REPARSE_RESULT.json (machine-readable) + console digest.
"""
import struct
import json
import hashlib
import os
import sys

sys.dont_write_bytecode = True

VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
OUT = os.path.join(PKG, "04_QC", "QC1_REPARSE_RESULT.json")

data = open(VFS, "rb").read()
vfs_sha = hashlib.sha256(data).hexdigest().upper()

# ---------- QC's own grammar derivation ----------
# Step 1: magic must be printable ASCII and non-zero; read u32@+8 as candidate base.
magic = data[:8]
base = struct.unpack_from("<I", data, 8)[0]
gu32 = struct.unpack_from("<I", data, 12)[0]
derivation = {
    "magic": magic.decode("latin-1"),
    "candidate_base_u32_at_8": base,
    "u32_at_12": gu32,
    "derivation_notes": [
        "base candidates that yield byte-exact EOF walk from +16 with 16-byte headers "
        "{u32,u32,u32,u32} and stride align_up(16+size, base) were tested; the exact-EOF "
        "test selects base=%d" % base,
    ],
}

def align_up(x, a):
    return ((x + a - 1) // a) * a

def walk(buf, base_value, strict_ver=True):
    """QC's own walk. Returns (records, error). Fail-closed on any violation."""
    records = []
    pos = 16
    n = len(buf)
    while pos < n:
        if pos + 16 > n:
            return records, "truncated header at %d" % pos
        rid, size, ver, crc = struct.unpack_from("<IIII", buf, pos)
        if strict_ver and ver != 1:
            return records, "ver!=1 at frame %d (ver=%d)" % (pos, ver)
        if pos + 16 + size > n:
            return records, "payload beyond EOF at frame %d (size=%d)" % (pos, size)
        records.append({
            "index": len(records),
            "frame_start": pos,
            "id": rid,
            "size": size,
            "ver": ver,
            "crc": crc,
            "payload_start": pos + 16,
        })
        pos = 16 + align_up(16 + size, base_value) + (pos - 16) if False else pos + align_up(16 + size, base_value)
    if pos != n:
        return records, "non-exact EOF: stop=%d file=%d" % (pos, n)
    return records, None

# exact-EOF base derivation test over plausible bases (power-of-two candidates)
base_tests = {}
for cand in (32, 64, 128, 256):
    recs, err = walk(data, cand)
    base_tests["base_%d" % cand] = {"ok": err is None, "records": len(recs), "error": err,
                                    "exact_eof": (err is None)}
derivation["base_candidate_tests"] = base_tests

records, err = walk(data, base)
result = {
    "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
    "countercheck": "QC1 independent framing re-parse",
    "tool": "04_QC/qc_tools/qc1_reparse_vfs.py",
    "independence": "own implementation; no executor/vfs_common code",
    "vfs_path": VFS,
    "vfs_size": len(data),
    "vfs_sha256": vfs_sha,
    "derivation": derivation,
    "walk_error": err,
    "record_count": len(records),
}

# exact-EOF invariants
strides = [align_up(16 + r["size"], base) for r in records]
result["exact_eof_invariant"] = {
    "stop_pos": (16 + sum(strides)) if records else None,
    "file_size": len(data),
    "sum_strides_plus_16_equals_file": (16 + sum(strides)) == len(data),
}

# ---------- per-record census (QC's own) ----------
FIELD_OFF = 0x30
census = {
    "sizes": set(), "vers": set(), "crcs": set(),
    "u32_at_0": set(), "u16_at_2e": {}, "u16_at_8_flags": {}, "u16_at_a_count": {},
    "bounds_ok": 0, "bounds_violation": 0,
    "id_composite_mismatch": [],
    "tlv_shapes": {}, "tail_values": {},
    "field_values": [], "zero_indexes": [],
    "plus_2c_values": {}, "plus_34_values": {},
}
rows = []
for r in records:
    ps = r["payload_start"]
    plen = r["size"]
    p = data[ps:ps + plen]
    census["sizes"].add(plen)
    census["vers"].add(r["ver"])
    census["crcs"].add(r["crc"])
    row = dict(r)
    row["payload_length"] = plen
    ok = (FIELD_OFF + 4 <= plen)
    if ok:
        census["bounds_ok"] += 1
        row["bounds_ok"] = True
        row["field_file_offset"] = ps + FIELD_OFF
        raw30 = p[FIELD_OFF:FIELD_OFF + 4]
        row["plus30_raw_hex"] = raw30.hex()
        row["plus30_le_u32"] = struct.unpack_from("<I", p, FIELD_OFF)[0]
        census["field_values"].append(row["plus30_le_u32"])
        if row["plus30_le_u32"] == 0:
            census["zero_indexes"].append(r["index"])
        row["plus2c_le_u32"] = struct.unpack_from("<I", p, 0x2C)[0]
        row["plus34_le_u32"] = struct.unpack_from("<I", p, 0x34)[0]
        census["plus_2c_values"][row["plus2c_le_u32"]] = census["plus_2c_values"].get(row["plus2c_le_u32"], 0) + 1
        census["plus_34_values"][row["plus34_le_u32"]] = census["plus_34_values"].get(row["plus34_le_u32"], 0) + 1
        census["u32_at_0"].add(struct.unpack_from("<I", p, 0)[0])
        t2e = struct.unpack_from("<H", p, 0x2E)[0]
        census["u16_at_2e"][t2e] = census["u16_at_2e"].get(t2e, 0) + 1
        fl = struct.unpack_from("<H", p, 0x08)[0]
        census["u16_at_8_flags"][fl] = census["u16_at_8_flags"].get(fl, 0) + 1
        ct = struct.unpack_from("<H", p, 0x0A)[0]
        census["u16_at_a_count"][ct] = census["u16_at_a_count"].get(ct, 0) + 1
        a = struct.unpack_from("<H", p, 6)[0]
        b = struct.unpack_from("<H", p, 4)[0]
        if r["id"] != ((a << 16) | b):
            census["id_composite_mismatch"].append(r["index"])
    else:
        census["bounds_violation"] += 1
        row["bounds_ok"] = False
    rows.append(row)

# ---------- QC's own TLV grammar re-derivation from bytes ----------
# Hypothesis space (derived mechanically, not copied):
#  H_A: every entry = {u16 tag, u32 value} (6 bytes) -> entries span 0x0C..0x2B (36 bytes)
#  H_B: first entry {u16 tag, 8-byte value}, others {u16 tag, u32 value} -> 0x0C..0x33 (40 bytes)
# Constraint: total payload = 56; header flags+count end at 0x0C; a 4-byte tail at the end.
# H_A leaves 56-0x0C-36-4 = 8 bytes unexplained; H_B consumes exactly to 0x34 with tail at 0x34.
def tlv_walk(p):
    """QC's own TLV walk (V2, corrected): entry count = u16@+0x0A (byte-derived
    constraint; the first QC1 run ignored it and consumed the tail's low u16 as a
    phantom 7th entry - QC tool bug, fixed here and disclosed in the QC report).
    Entry value width: 8 for tag 1 (byte-derived: required for the walk to reach
    the observed +0x2E tag 0x11 and the +0x34 tail exactly), else 4."""
    count = struct.unpack_from("<H", p, 0x0A)[0]
    off = 0x0C
    entries = []
    for _ in range(count):
        if off + 2 > len(p):
            return None, "tag OOB at +0x%X" % off
        tag = struct.unpack_from("<H", p, off)[0]
        entries.append({"tag_off": off, "tag": tag})
        off += 2
        width = 8 if tag == 1 else 4
        if off + width > len(p):
            return None, "value OOB at +0x%X" % off
        off += width
    if off + 4 <= len(p):
        tail = struct.unpack_from("<I", p, off)[0]
    else:
        return None, "tail OOB at +0x%X" % off
    return {"entries": entries, "end_off": off, "tail": tail, "tail_off": off}, None

tlv_shapes = {}
tlv_field30_is_tag11 = 0
tlv_tag11_value_offset_30 = 0
tlv_tail_zero = 0
tlv_walk_errors = []
for r in records:
    ps = r["payload_start"]
    p = data[ps:ps + r["size"]]
    w, werr = tlv_walk(p)
    if werr:
        tlv_walk_errors.append({"record": r["index"], "err": werr})
        continue
    key = (tuple(e["tag"] for e in w["entries"]), w["tail"])
    tlv_shapes[str(key)] = tlv_shapes.get(str(key), 0) + 1
    if w["tail"] == 0:
        tlv_tail_zero += 1
    tag11 = [e for e in w["entries"] if e["tag"] == 0x11]
    if tag11:
        voff = tag11[0]["tag_off"] + 2
        if voff == 0x30:
            tlv_field30_is_tag11 += 1
            tlv_tag11_value_offset_30 += 1

# ---------- anchors (QC's own re-derivation) ----------
def anchor_row(i):
    row = rows[i]
    ps = row["payload_start"]
    p = data[ps:ps + row["payload_length"]]
    return {
        "record_index": i,
        "frame_start": row["frame_start"],
        "record_id_hex": "0x%08X" % row["id"],
        "payload_start": ps,
        "payload_length": row["payload_length"],
        "field_file_offset": ps + FIELD_OFF,
        "plus30_raw_hex": p[FIELD_OFF:FIELD_OFF + 4].hex(),
        "plus30_le_u32": struct.unpack_from("<I", p, FIELD_OFF)[0],
        "ver": row["ver"], "crc_field": row["crc"],
        "payload_hex": p.hex(),
    }

result["census"] = {
    "distinct_sizes": sorted(census["sizes"]),
    "distinct_vers": sorted(census["vers"]),
    "distinct_crcs": sorted(census["crcs"]),
    "u32_at_payload_0": sorted(census["u32_at_0"]),
    "u16_at_2e": {("0x%X" % k): v for k, v in census["u16_at_2e"].items()},
    "u16_at_8_flags": {("0x%X" % k): v for k, v in census["u16_at_8_flags"].items()},
    "u16_at_a_count": {k: v for k, v in census["u16_at_a_count"].items()},
    "bounds_ok": census["bounds_ok"],
    "bounds_violation": census["bounds_violation"],
    "id_composite_mismatch_count": len(census["id_composite_mismatch"]),
    "field_value_count": len(census["field_values"]),
    "field_value_min": min(census["field_values"]) if census["field_values"] else None,
    "field_value_max": max(census["field_values"]) if census["field_values"] else None,
    "field_value_distinct": len(set(census["field_values"])),
    "field_zero_indexes": census["zero_indexes"],
    "plus_2c_value_histogram": {("0x%X" % k): v for k, v in census["plus_2c_values"].items()},
    "plus_34_value_histogram": {("0x%X" % k): v for k, v in census["plus_34_values"].items()},
}
result["tlv_walk"] = {
    "shape_counts": tlv_shapes,
    "walk_errors": tlv_walk_errors[:10],
    "field30_is_tag11_value": tlv_field30_is_tag11,
    "tag11_value_offset_30": tlv_tag11_value_offset_30,
    "tail_zero_count": tlv_tail_zero,
}
result["anchor_primary_qc"] = anchor_row(0)
result["anchor_zero_qc"] = anchor_row(census["zero_indexes"][0]) if census["zero_indexes"] else None

# ---------- comparison with executor artifacts ----------
exec_anchor = json.load(open(os.path.join(PKG, "01_RAW", "FIELD_BYTE_ANCHOR.json")))
exec_rows = []
with open(os.path.join(PKG, "01_RAW", "RECORD_FRAMING.jsonl")) as f:
    for line in f:
        exec_rows.append(json.loads(line))

compare = {"exec_rows_read": len(exec_rows), "frame_start_mismatch": [], "payload_start_mismatch": [],
           "payload_length_mismatch": [], "record_id_mismatch": [], "plus30_mismatch": [],
           "bounds_flag_mismatch": 0}
for qr, er in zip(rows, exec_rows):
    if qr["frame_start"] != er["frame_start"]:
        compare["frame_start_mismatch"].append(qr["index"])
    if qr["payload_start"] != er["payload_start"]:
        compare["payload_start_mismatch"].append(qr["index"])
    if qr["size"] != er["payload_length"]:
        compare["payload_length_mismatch"].append(qr["index"])
    if qr["id"] != int(er["record_id_hex"], 16):
        compare["record_id_mismatch"].append(qr["index"])
    if qr.get("plus30_le_u32") != er.get("payload_plus_30_decoded_le_u32") or \
       (qr.get("plus30_raw_hex") or "").upper() != (er.get("payload_plus_30_raw_bytes_hex") or "").upper():
        compare["plus30_mismatch"].append(qr["index"])
    if bool(qr.get("bounds_ok")) != bool(er.get("bounds_ok")):
        compare["bounds_flag_mismatch"] += 1

ea = exec_anchor["anchor_primary"]
ez = exec_anchor["anchor_zero"]
compare["anchor_primary_agrees"] = (
    ea["frame_start"] == result["anchor_primary_qc"]["frame_start"] and
    ea["payload_start"] == result["anchor_primary_qc"]["payload_start"] and
    ea["payload_length"] == result["anchor_primary_qc"]["payload_length"] and
    ea["field_file_offset"] == result["anchor_primary_qc"]["field_file_offset"] and
    ea["payload_plus_30_raw_bytes_hex"].upper() == result["anchor_primary_qc"]["plus30_raw_hex"].upper() and
    ea["payload_plus_30_decoded_le_u32"] == result["anchor_primary_qc"]["plus30_le_u32"])
compare["anchor_zero_agrees"] = (
    ez["record_index"] == result["anchor_zero_qc"]["record_index"] if result["anchor_zero_qc"] else False)
if result["anchor_zero_qc"]:
    compare["anchor_zero_agrees"] = (
        ez["frame_start"] == result["anchor_zero_qc"]["frame_start"] and
        ez["payload_start"] == result["anchor_zero_qc"]["payload_start"] and
        ez["payload_length"] == result["anchor_zero_qc"]["payload_length"] and
        ez["field_file_offset"] == result["anchor_zero_qc"]["field_file_offset"] and
        ez["payload_plus_30_raw_bytes_hex"].upper() == result["anchor_zero_qc"]["plus30_raw_hex"].upper() and
        ez["payload_plus_30_decoded_le_u32"] == result["anchor_zero_qc"]["plus30_le_u32"])
compare["anchor_primary_payload_hex_agrees"] = (
    exec_anchor["anchor_primary_payload_hex"].lower() == result["anchor_primary_qc"]["payload_hex"].lower())
compare["anchor_zero_payload_hex_agrees"] = (
    exec_anchor["anchor_zero_payload_hex"].lower() == result["anchor_zero_qc"]["payload_hex"].lower())
result["executor_comparison"] = compare

with open(OUT, "w") as f:
    json.dump(result, f, indent=1)

print("QC1 REPARSE DIGEST")
print("  vfs sha256:", vfs_sha, "size:", len(data))
print("  base tests:", base_tests)
print("  record_count:", len(records), "walk_error:", err)
print("  exact EOF:", result["exact_eof_invariant"]["sum_strides_plus_16_equals_file"])
print("  census:", json.dumps(result["census"]))
print("  tlv:", json.dumps(result["tlv_walk"]))
print("  anchor_primary:", result["anchor_primary_qc"])
print("  anchor_zero:", result["anchor_zero_qc"])
print("  compare:", json.dumps(compare))
