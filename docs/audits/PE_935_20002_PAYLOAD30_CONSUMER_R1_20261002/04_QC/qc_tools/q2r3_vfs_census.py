#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QC-R2 TOOL 3 (fresh QC worker, round 2; own walk; shares NO code with the
executor's 03_SCRIPTS, with round-1's qc_tools, or with JOIN R1's vfs_common):

INDEPENDENT RE-DERIVATION of the 20002.vfs framing walk and the
u16@payload+0x08 census from the raw pinned VFS bytes
(C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4, 174,864 B).

Grammar derivation is from the physical bytes (observed in this session's own
hexdump): 16-byte global header {magic "ArkVFS02"(8) + u32 base + pad}, then
records of 16-byte framing header {u32 id, u32 size, u16 ver, u32 crc, u16 pad}
followed by `size` payload bytes; record stride = base * ceil((16+size)/base);
walk terminates at EXACT EOF.

Checks:
  V1. magic ArkVFS02; base == 0x80
  V2. exact-EOF walk; record count == 1366
  V3. per-record sanity: size==56, ver==1, crc==0 for ALL records
  V4. u16@payload+0x08 histogram == {"0x80": 1366}   <- dispatch duty 5 census
  V5. u16@payload+0x04 distinct values == exactly 1..190 (190 values)
      (cross-check of the AMEND-R1 C5 renamed key's "original value set")
  V6. u32@payload+0x00 == 20002 for all; u16@payload+0x2E == 0x11 for all
  V7. id == (u16@payload+6 << 16) | u16@payload+4 for all records
  V8. anchors: rec0 payload+0x30 == 11963 (BB 2E 00 00) @file offset 80;
      rec1014 == 0 @129872; zeros exactly at {1014, 1015}
  V9. field distinct-count == 142, min 0, max 16409 (round-1 figures)
  V10. comparison vs the AMENDED RECORD_FRAMING_SUMMARY.json keys
      (distinct_u16_at_payload_04 array; distinct_u16_at_payload_08 aggregate)
"""
import hashlib
import json
import os
import struct

VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
ROOT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"


def u16(data, off):
    return struct.unpack_from("<H", data, off)[0]


def u32(data, off):
    return struct.unpack_from("<I", data, off)[0]


def main():
    with open(VFS, "rb") as fh:
        data = fh.read()
    res = {"tool": "q2r3_vfs_census.py", "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
           "qc_round": 2,
           "vfs_identity": {"size": len(data), "sha256": hashlib.sha256(data).hexdigest().upper()},
           "checks": {}}
    ck = res["checks"]

    # V1: global header
    ck["V1_global_header"] = {
        "magic": data[0:8].decode("ascii", "replace"),
        "base": "%#x" % u32(data, 8),
        "magic_ok": data[0:8] == b"ArkVFS02", "base_ok": u32(data, 8) == 0x80,
        "pass": data[0:8] == b"ArkVFS02" and u32(data, 8) == 0x80}
    base = u32(data, 8)

    # V2/V3: the walk
    records = []
    pos = 0x10
    problems = []
    while pos < len(data):
        if pos + 16 > len(data):
            problems.append("truncated header at %#x" % pos)
            break
        rid = u32(data, pos)
        size = u32(data, pos + 4)
        ver = u16(data, pos + 8)
        crc = u32(data, pos + 10)
        pad = u16(data, pos + 14)
        pstart = pos + 16
        if pstart + size > len(data):
            problems.append("payload overruns EOF at record frame %#x (size=%d)" % (pos, size))
            break
        records.append({"frame": pos, "payload_start": pstart, "size": size,
                        "ver": ver, "crc": crc, "pad": pad, "rid": rid})
        stride = base * ((16 + size + base - 1) // base)
        pos = pos + stride
    exact_eof = (pos == len(data) and not problems)
    ck["V2_exact_eof_walk"] = {
        "final_pos": pos, "file_size": len(data), "record_count": len(records),
        "expected_record_count": 1366,
        "problems": problems,
        "pass": exact_eof and len(records) == 1366}

    # V3: per-record sanity
    sizes = {r["size"] for r in records}
    vers = {r["ver"] for r in records}
    crcs = {r["crc"] for r in records}
    ck["V3_record_header_sanity"] = {
        "distinct_sizes": sorted(sizes), "distinct_vers": sorted(vers),
        "distinct_crcs": sorted(crcs),
        "pass": sizes == {56} and vers == {1} and crcs == {0}}

    # V4/V5/V6: payload censuses
    hist08 = {}
    vals04 = set()
    u32_00_all_20002 = True
    u16_2e_all_11 = True
    for r in records:
        ps = r["payload_start"]
        v08 = u16(data, ps + 0x08)
        hist08["%#x" % v08] = hist08.get("%#x" % v08, 0) + 1
        vals04.add(u16(data, ps + 0x04))
        if u32(data, ps + 0x00) != 20002:
            u32_00_all_20002 = False
        if u16(data, ps + 0x2E) != 0x11:
            u16_2e_all_11 = False
    ck["V4_u16_at_payload_08_census"] = {
        "histogram": hist08, "expected": {"0x80": 1366},
        "pass": hist08 == {"0x80": 1366}}
    ck["V5_u16_at_payload_04_distinct"] = {
        "count": len(vals04), "min": min(vals04), "max": max(vals04),
        "is_exactly_1_to_190": vals04 == set(range(1, 191)),
        "pass": vals04 == set(range(1, 191))}
    ck["V6_payload_censuses"] = {
        "u32_at_payload_00_all_20002": u32_00_all_20002,
        "u16_at_payload_2e_all_0x11": u16_2e_all_11,
        "pass": u32_00_all_20002 and u16_2e_all_11}

    # V7: id composite
    comp_ok = all(r["rid"] == ((u16(data, r["payload_start"] + 6) << 16) | u16(data, r["payload_start"] + 4))
                  for r in records)
    ck["V7_id_composite"] = {"all_match": comp_ok, "pass": comp_ok}

    # V8/V9: the payload+0x30 field census
    field_vals = {}
    zeros = []
    for i, r in enumerate(records):
        fo = r["payload_start"] + 0x30
        raw = data[fo:fo + 4]
        val = struct.unpack("<I", raw)[0]
        field_vals[i] = (val, raw)
        if val == 0:
            zeros.append(i)
    r0 = field_vals[0]
    r1014 = field_vals[1014]
    distinct = {v for v, _ in field_vals.values()}
    ck["V8_anchors"] = {
        "rec0_field": {"value": r0[0], "raw": r0[1].hex().upper(),
                       "file_offset": records[0]["payload_start"] + 0x30},
        "rec0_expected": {"value": 11963, "raw": "BB2E0000", "file_offset": 80},
        "rec1014_field": {"value": r1014[0], "file_offset": records[1014]["payload_start"] + 0x30},
        "rec1014_expected": {"value": 0, "file_offset": 129872},
        "zero_records": zeros, "expected_zero_records": [1014, 1015],
        "pass": (r0[0] == 11963 and r0[1] == bytes.fromhex("BB2E0000")
                 and records[0]["payload_start"] + 0x30 == 80
                 and r1014[0] == 0 and records[1014]["payload_start"] + 0x30 == 129872
                 and zeros == [1014, 1015])}
    ck["V9_field_census"] = {
        "distinct_count": len(distinct), "min": min(distinct), "max": max(distinct),
        "expected": {"distinct": 142, "min": 0, "max": 16409},
        "pass": len(distinct) == 142 and min(distinct) == 0 and max(distinct) == 16409}

    # V10: comparison vs the AMENDED RECORD_FRAMING_SUMMARY.json
    with open(os.path.join(ROOT, "01_RAW", "RECORD_FRAMING_SUMMARY.json"), "r", encoding="utf-8") as fh:
        summary = json.load(fh)  # also proves the edited JSON still parses
    arr04 = summary["census"]["distinct_u16_at_payload_04"] if "census" in summary else None
    if arr04 is None:
        # locate the key wherever it lives
        def find_key(obj, key):
            if isinstance(obj, dict):
                if key in obj:
                    return obj[key]
                for v in obj.values():
                    r = find_key(v, key)
                    if r is not None:
                        return r
            return None
        arr04 = find_key(summary, "distinct_u16_at_payload_04")
        agg08 = find_key(summary, "distinct_u16_at_payload_08")
    else:
        agg08 = summary["census"]["distinct_u16_at_payload_08"]
    ck["V10_vs_amended_summary"] = {
        "json_parses": True,
        "distinct_u16_at_payload_04_type": type(arr04).__name__,
        "distinct_u16_at_payload_04_count": len(arr04) if isinstance(arr04, list) else None,
        "array_equals_1_to_190": isinstance(arr04, list) and arr04 == list(range(1, 191)),
        "distinct_u16_at_payload_08": agg08,
        "aggregate_equals_expected": agg08 == {"0x80": 1366},
        "my_walk_u16_08_histogram": hist08,
        "my_walk_u16_04_count": len(vals04),
        "pass": isinstance(arr04, list) and arr04 == list(range(1, 191))
                and agg08 == {"0x80": 1366}}

    res["OVERALL_PASS"] = all(c.get("pass", False) for c in ck.values())

    path = os.path.join(ROOT, "04_QC", "QC_R2_VFS_WALK_RESULT.json")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=1)[:6000])
    print("OVERALL_PASS =", res["OVERALL_PASS"])


if __name__ == "__main__":
    main()
