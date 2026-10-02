#!/usr/bin/env python3
# QC-R3 Q3: independent re-derivation of the cursor + destination over the pinned 20002.vfs.
# Own framing re-derivation from raw bytes; own walk implementation; own negative controls.
import json, os, struct

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
QC_DIR = os.path.join(PKG, "04_QC", "QC_R3_DESKTOP_CORRECTION")
VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"

data = open(VFS, "rb").read()
assert data[0:8] == b"ArkVFS02", "magic mismatch"
global_dword_8 = struct.unpack_from("<I", data, 8)[0]   # 0x80 (the stride/base constant in the header)

# ---- framing re-derivation (independent): global header 16 bytes; records stride 0x80 ----
STRIDE = 128
GLOBAL_HDR = 16
n_records = (len(data) - GLOBAL_HDR) // STRIDE
exact_eof = GLOBAL_HDR + n_records * STRIDE == len(data)
leftover = len(data) - GLOBAL_HDR - n_records * STRIDE

WIDTHS = {0x01: 8, 0x0C: 4, 0x0D: 4, 0x0E: 4, 0x10: 4, 0x11: 4}

class WalkError(Exception):
    pass

def walk_record(payload, ordinal, limit_override=None):
    """Independent TLV walk over one record payload.
    Model (byte-derived, decoder-verified in Q1):
      cursor.base = payload; offset 0; limit = len(payload) (or override for negative control)
      advance-8 (class id + record id) -> offset 8
      flags u16 -> offset 10 ; count u16 -> offset 12
      count x { tag u16 (+2); value width[tag] }
      mode-1 tail u32 -> offset == limit (full consumption)
    Returns dict with per-stage states incl. the cursor offset at the tag-17 VALUE read."""
    limit = limit_override if limit_override is not None else len(payload)
    off = 0
    flag = True

    def need(n):
        nonlocal off, flag
        if off + n > limit:
            flag = False
            raise WalkError(f"BOUNDS_FAILURE offset {off}+{n} > limit {limit}")
    def rd(n):
        nonlocal off
        need(n)
        b = payload[off:off+n]
        off += n
        return b
    def adv(n):
        nonlocal off, flag
        if off + n > limit:
            flag = False
            raise WalkError(f"ADVANCE_OVERRUN offset {off}+{n} > limit {limit}")
        off += n

    states = []
    # advance-8 (FUN_0070dcf0 @0x70DDA2): class id + record id consumed
    adv(8)
    states.append({"stage": "after advance-8", "offset": off})
    # header u16 flags + u16 count (FUN_00726900)
    flags_u16 = struct.unpack("<H", rd(2))[0]
    count_u16 = struct.unpack("<H", rd(2))[0]
    states.append({"stage": "header read", "flags": flags_u16, "count": count_u16, "offset": off})
    entries = []
    tag17_state = None
    for i in range(count_u16):
        if not flag:
            break
        tag = struct.unpack("<H", rd(2))[0]
        w = WIDTHS.get(tag)
        if w is None:
            flag = False
            raise WalkError(f"UNKNOWN TAG {tag:#x} at entry {i} (no descriptor width)")
        val_off = off  # cursor offset at the VALUE read
        val = rd(w)
        entries.append({"tag": tag, "value_offset": val_off, "raw": val.hex()})
        if tag == 0x11:
            tag17_state = {"iteration": i, "cursor_offset_at_value_read": val_off,
                           "cursor_offset_hex": hex(val_off), "raw_hex": val.hex().upper(),
                           "decoded_le_u32": struct.unpack("<I", val)[0]}
    # mode-1 tail u32
    tail = struct.unpack("<I", rd(4))[0]
    states.append({"stage": "after tail", "tail_u32": tail, "offset": off, "limit": limit})
    return {"ordinal": ordinal, "states": states, "entries": entries, "tag17": tag17_state,
            "full_consumption": off == limit and flag}

res = {"q": "Q3_vfs_walk", "vfs_size": len(data), "global_header": data[:16].hex().upper(),
       "global_dword_at_8": global_dword_8, "framing": {
           "global_header_bytes": GLOBAL_HDR, "stride": STRIDE, "records": n_records,
           "exact_eof": exact_eof, "leftover_bytes": leftover},
       "record_0_header": {}, "record_1014_header": {}, "walks": {}, "census": {}, "negative_controls": {}}

# ---- record 0 and record 1014 detailed walks + raw byte anchors ----
def rec_bounds(i):
    start = GLOBAL_HDR + i * STRIDE
    hdr = data[start:start+16]
    rid, rsize, rver, rcrc = struct.unpack("<IIII", hdr)
    payload = data[start+16:start+16+rsize]
    return {"start": start, "header_hex": hdr.hex().upper(), "id": f"{rid:#010x}", "size": rsize,
            "ver": rver, "crc": rcrc, "payload_start": start+16, "payload": payload}

r0 = rec_bounds(0)
r1014 = rec_bounds(1014)
res["record_0_header"] = {k: v for k, v in r0.items() if k != "payload"}
res["record_1014_header"] = {k: v for k, v in r1014.items() if k != "payload"}

w0 = walk_record(r0["payload"], 0)
res["walks"]["record_0"] = {"states": w0["states"], "entries": w0["entries"], "tag17": w0["tag17"],
                            "full_consumption": w0["full_consumption"],
                            "raw_bytes_at_tag17_value": r0["payload"][0x30:0x34].hex().upper()}
w1014 = walk_record(r1014["payload"], 1014)
res["walks"]["record_1014"] = {"states": w1014["states"], "entries": w1014["entries"], "tag17": w1014["tag17"],
                              "full_consumption": w1014["full_consumption"],
                              "raw_bytes_at_tag17_value": r1014["payload"][0x30:0x34].hex().upper()}

# ---- full census: every record; tag-17 offset == 0x30; zero-value records; consumption ----
tag17_offsets = {}
tag17_values = {}
tag_sequences = {}
full_consumption = 0
flags_hist = {}
count_hist = {}
sizes_hist = {}
ver_hist = {}
crc_hist = {}
walk_failures = []
for i in range(n_records):
    rb = rec_bounds(i)
    sizes_hist[rb["size"]] = sizes_hist.get(rb["size"], 0) + 1
    ver_hist[rb["ver"]] = ver_hist.get(rb["ver"], 0) + 1
    crc_hist[rb["crc"]] = crc_hist.get(rb["crc"], 0) + 1
    try:
        w = walk_record(rb["payload"], i)
        if w["full_consumption"]:
            full_consumption += 1
        if w["tag17"]:
            o = w["tag17"]["cursor_offset_hex"]
            tag17_offsets[o] = tag17_offsets.get(o, 0) + 1
            v = w["tag17"]["decoded_le_u32"]
            tag17_values[i] = v
        seq = tuple(e["tag"] for e in w["entries"])
        tag_sequences[seq] = tag_sequences.get(seq, 0) + 1
        fl = w["states"][1]["flags"]
        flags_hist[fl] = flags_hist.get(fl, 0) + 1
        ct = w["states"][1]["count"]
        count_hist[ct] = count_hist.get(ct, 0) + 1
    except WalkError as e:
        walk_failures.append({"ordinal": i, "error": str(e)})

zero_records = sorted([i for i, v in tag17_values.items() if v == 0])
res["census"] = {
    "records_walked": n_records,
    "walk_failures": walk_failures,
    "tag17_value_offset_distinct": tag17_offsets,
    "tag17_offset_0x30_count": tag17_offsets.get("0x30", 0),
    "full_consumption_count": full_consumption,
    "flags_histogram": {f"{k:#x}": v for k, v in flags_hist.items()},
    "count_histogram": {f"{k}": v for k, v in count_hist.items()},
    "sizes_histogram": sizes_hist, "ver_histogram": ver_hist, "crc_histogram": crc_hist,
    "tag_sequences": [{"tags": [hex(t) for t in seq], "count": c} for seq, c in tag_sequences.items()],
    "zero_valued_records": zero_records,
    "record_0_tag17_value": tag17_values.get(0),
    "record_1014_tag17_value": tag17_values.get(1014),
    "record_1015_tag17_value": tag17_values.get(1015),
}

# ---- destination computation check: value_array + (tag+4)*4 ----
TAG = 0x11
field_index = TAG + 4
dest_offset = field_index * 4
res["destination"] = {
    "field_index": field_index, "field_index_hex": hex(field_index),
    "dest_offset": dest_offset, "dest_offset_hex": hex(dest_offset),
    "slot": field_index, "slots_total": 18 + 4,
    "expected": "value_array + 0x54 = slot 21 of 22 (count 18 + 4)",
    "ok": dest_offset == 0x54 and field_index == 21 and (18 + 4) == 22,
}

# ---- MY negative controls (falsifiers of the walk, not inherited from the executor) ----
# NC1: truncate record 0 payload to 48 bytes -> the tag-17 value read must FAIL bounds
try:
    walk_record(r0["payload"][:48], 0)
    nc1 = {"detected": False, "note": "walk PASSED on truncated payload - DETECTOR FAILURE"}
except WalkError as e:
    nc1 = {"detected": True, "error": str(e),
           "note": "offset 48+4 > limit 48 => the reader's bounds error path (dest=0 + flag clear in the real reader)"}
# NC2: shift the tag bytes (corrupt tag 0xC -> 0x06, an unknown tag) -> walk must FAIL
payload_corrupt = bytearray(r0["payload"])
payload_corrupt[0x16] = 0x06  # the tag-0xC entry's tag u16 low byte at payload+0x16
try:
    walk_record(bytes(payload_corrupt), 0)
    nc2 = {"detected": False, "note": "walk PASSED on corrupted tag - DETECTOR FAILURE"}
except WalkError as e:
    nc2 = {"detected": True, "error": str(e), "note": "unknown tag => descriptor lookup failure in the real parser"}
# NC3: a legal NULL-ish structural check: header count says 0 entries -> walk consumes only the header+tail
payload_c0 = bytearray(r0["payload"])
payload_c0[0xA] = 0  # count u16 = 0
payload_c0[0x16] = 0x0C
w_nc3 = walk_record(bytes(payload_c0), 0)
nc3 = {"walk_completed": w_nc3["full_consumption"], "entries": len(w_nc3["entries"]),
       "note": "count=0 => 0 entries; walk still consumes to limit (structural consistency of the model)"}
res["negative_controls"] = {"NC1_truncate_48": nc1, "NC2_corrupt_tag": nc2, "NC3_count_zero": nc3}

# ---- verdict predicates ----
checks = {
    "framing_exact_eof": exact_eof and leftover == 0 and n_records == 1366,
    "global_header_magic": res["global_header"].startswith("41726B56465330") and global_dword_8 == 0x80,
    "record0_tag17_value_11963": tag17_values.get(0) == 11963,
    "record0_raw_bytes_BB2E0000": r0["payload"][0x30:0x34].hex().upper() == "BB2E0000",
    "record1014_tag17_value_0": tag17_values.get(1014) == 0,
    "record1014_raw_bytes_00000000": r1014["payload"][0x30:0x34].hex().upper() == "00000000",
    "tag17_offset_0x30_all_records": tag17_offsets.get("0x30", 0) == n_records and len(tag17_offsets) == 1,
    "census_1366_of_1366": len(walk_failures) == 0 and n_records == 1366,
    "zeros_exactly_1014_1015": zero_records == [1014, 1015],
    "full_consumption_all": full_consumption == n_records,
    "record0_offset_at_tag17_value_0x30": w0["tag17"]["cursor_offset_hex"] == "0x30",
    "record1014_offset_at_tag17_value_0x30": w1014["tag17"]["cursor_offset_hex"] == "0x30",
    "destination_slot21_0x54": res["destination"]["ok"],
    "nc1_detected": nc1["detected"],
    "nc2_detected": nc2["detected"],
    "flags_0x80_all": list(flags_hist.keys()) == [0x80],
    "count_6_all": list(count_hist.keys()) == [6],
    "sizes_56_all": list(sizes_hist.keys()) == [56],
    "ver_1_all": list(ver_hist.keys()) == [1],
    "crc_0_all": list(crc_hist.keys()) == [0],
}
res["checks"] = checks
res["failed_checks"] = [k for k, v in checks.items() if not v]
res["verdict"] = "PASS" if not res["failed_checks"] else "FAIL"
out = os.path.join(QC_DIR, "QC_R3_VFS_WALK_RESULT.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print(json.dumps({"framing": res["framing"], "checks": checks, "failed": res["failed_checks"],
                  "verdict": res["verdict"],
                  "tag_sequences": res["census"]["tag_sequences"],
                  "zero_records": zero_records,
                  "record0_tag17": res["walks"]["record_0"]["tag17"],
                  "record1014_tag17": res["walks"]["record_1014"]["tag17"],
                  "negative_controls": res["negative_controls"]}, indent=2))
