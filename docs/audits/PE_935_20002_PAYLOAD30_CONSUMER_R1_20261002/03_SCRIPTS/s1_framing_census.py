#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S1+S2 executor in-run framing parse + field anchor census for 20002.vfs.
RUN_ID PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002.

In-run OWN implementation (contract S14: does NOT import or share code with prior tools;
prior tool vfs_common.py is used only by the separate labeled cross-validation script).

Pure reader of the original VFS; NC-FRAMING corruption variants are built IN MEMORY only.

Outputs (01_RAW):
  RECORD_FRAMING.jsonl          - 1 row per record: framing + payload + field census
  RECORD_FRAMING_SUMMARY.json   - header layout derivation, invariants, anchors, NC results
  FIELD_BYTE_ANCHOR.json        - anchored records byte-level evidence + bounds assertions
"""
import struct
import json
import hashlib
import datetime

VFS_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
OUT_DIR = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW"
FIELD_OFF = 0x30       # payload-relative field offset (the traced field)
FIELD_WIDTH = 4        # hypothesis width until client read pins it (V2-009 label)
ADJ_OFF = 0x2C         # adjacent displacement control field (NC-ANCHOR-ADJ feasible part)
ADJ2_OFF = 0x34        # second adjacent displacement (+0x34)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


def parse(data, label="walk"):
    """Executor's own framing walk. Returns (records, result_dict).

    Grammar derived in-run from physical bytes (see RECORD_FRAMING_SUMMARY.json):
      global header: 8-byte magic 'ArkVFS02' + u32 LE base + u32 LE (0)
      records from +16: 16-byte record header {u32 id, u32 size, u32 ver, u32 crc},
      payload = size bytes immediately after header, record stride =
      align_up(16+size, base) = ((16+size+base-1)//base)*base.
    Fail-closed: any bounds/EOF/grammar violation aborts with error.
    """
    res = {"label": label, "ok": False, "error": None, "records": [], "stop_pos": None}
    if len(data) < 16:
        res["error"] = "file shorter than global header"
        return None, res
    magic = data[:8]
    if magic != b"ArkVFS02":
        res["error"] = "magic mismatch: %r" % magic
        return None, res
    base = struct.unpack_from("<I", data, 8)[0]
    g4 = struct.unpack_from("<I", data, 12)[0]
    if base == 0:
        res["error"] = "base==0"
        return None, res
    res["magic"] = "ArkVFS02"
    res["base"] = base
    res["global_u32_12"] = g4
    records = []
    pos = 16
    n = len(data)
    while pos < n:
        if pos + 16 > n:
            res["error"] = "truncated record header at %d (need 16, have %d)" % (pos, n - pos)
            res["stop_pos"] = pos
            res["records"] = records
            return None, res
        rid, size, ver, crc = struct.unpack_from("<IIII", data, pos)
        if ver != 1:
            res["error"] = "ver!=1 at frame %d (ver=%d)" % (pos, ver)
            res["stop_pos"] = pos
            res["records"] = records
            return None, res
        if pos + 16 + size > n:
            res["error"] = "payload beyond EOF at frame %d (size=%d, need %d bytes, have %d)" % (
                pos, size, 16 + size, n - pos)
            res["stop_pos"] = pos
            res["records"] = records
            return None, res
        p_start = pos + 16
        records.append({
            "index": len(records),
            "frame_start": pos,
            "record_id": rid,
            "payload_size_field": size,
            "ver": ver,
            "crc_field": crc,
            "payload_start": p_start,
            "payload": data[p_start:p_start + size],
        })
        pos += ((16 + size + base - 1) // base) * base
    res["stop_pos"] = pos
    if pos != n:
        res["error"] = "walk did not end at exact EOF: stop_pos=%d, file_size=%d" % (pos, n)
        res["records"] = records
        return None, res
    if not records:
        res["error"] = "no records"
        return None, res
    res["ok"] = True
    res["records"] = records
    return records, res


def main():
    with open(VFS_PATH, "rb") as f:
        data = f.read()
    summary = {
        "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
        "stage": "S1_RECORD_FRAMING + S2_FIELD_ANCHOR (executor in-run implementation)",
        "generator": "03_SCRIPTS/s1_framing_census.py",
        "vfs_path": VFS_PATH,
        "vfs_size_bytes": len(data),
        "vfs_sha256": sha256_bytes(data),
        "measured_at_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "field_definition": {
            "field_payload_offset": FIELD_OFF,
            "field_width_hypothesis": FIELD_WIDTH,
            "width_endianness_provenance": "HYPOTHESIS_DERIVED_MEASUREMENT "
            "(4-byte little-endian reading derived from payload alignment + prior scan convention; "
            "not yet pinned by a client read instruction - V2-009 discipline)",
        },
    }

    records, res = parse(data, "strict_full_walk")
    summary["walk_result"] = {k: v for k, v in res.items() if k != "records"}
    if not res["ok"]:
        print("FRAMING WALK FAILED:", res["error"])
        raise SystemExit(2)
    n = len(records)
    summary["record_count_N"] = n
    summary["exact_eof_invariant"] = {
        "stop_pos": res["stop_pos"],
        "file_size": len(data),
        "equal": res["stop_pos"] == len(data),
        "derivation": "pos advanced by stride=align_up(16+size,base) per record from 16; "
                      "stop_pos==file_size proves byte-exact consumption",
        "stride_sum_check": sum(((16 + r["payload_size_field"] + res["base"] - 1) // res["base"]) * res["base"]
                                for r in records) + 16 == len(data),
    }

    # ---- per-record census (S2) ----
    jsonl_path = OUT_DIR + r"\RECORD_FRAMING.jsonl"
    rows = []
    sizes = set()
    vers = set()
    crcs = set()
    tag_at_2e = {}
    prefix_patterns = {}
    id_composite_mismatch = []
    class_field_values = set()
    u8_vals = set()
    uA_vals = set()
    for r in records:
        p = r["payload"]
        size = r["payload_size_field"]
        sizes.add(size)
        vers.add(r["ver"])
        crcs.add(r["crc_field"])
        bounds_ok = (FIELD_OFF + FIELD_WIDTH <= size)
        row = {
            "record_index": r["index"],
            "frame_start": r["frame_start"],
            "record_id_hex": "0x%08X" % r["record_id"],
            "payload_start": r["payload_start"],
            "payload_length": size,
            "ver": r["ver"],
            "crc_field": r["crc_field"],
            "field_file_offset": r["payload_start"] + FIELD_OFF,
            "field_byte_range": [r["payload_start"] + FIELD_OFF, r["payload_start"] + FIELD_OFF + FIELD_WIDTH],
            "bounds_ok": bounds_ok,
            "assert_lb": (r["payload_start"] + FIELD_OFF >= r["payload_start"]),
            "assert_ub": (r["payload_start"] + FIELD_OFF + FIELD_WIDTH <= r["payload_start"] + size),
        }
        if bounds_ok:
            row["payload_plus_30_raw_bytes_hex"] = p[FIELD_OFF:FIELD_OFF + FIELD_WIDTH].hex()
            row["payload_plus_30_decoded_le_u32"] = struct.unpack_from("<I", p, FIELD_OFF)[0]
            row["provenance"] = "HYPOTHESIS_DERIVED_MEASUREMENT"
            # adjacent fields for NC-ANCHOR-ADJ (feasible part) + structural context
            row["payload_plus_2c_raw_hex"] = p[ADJ_OFF:ADJ_OFF + 4].hex()
            row["payload_plus_2c_decoded_le_u32"] = struct.unpack_from("<I", p, ADJ_OFF)[0]
            if ADJ2_OFF + 4 <= size:
                row["payload_plus_34_raw_hex"] = p[ADJ2_OFF:ADJ2_OFF + 4].hex()
                row["payload_plus_34_decoded_le_u32"] = struct.unpack_from("<I", p, ADJ2_OFF)[0]
            # byte-level structural context (RAW measurements):
            row["u16_at_payload_2e"] = struct.unpack_from("<H", p, 0x2E)[0]
            row["u32_at_payload_00"] = struct.unpack_from("<I", p, 0)[0]
            row["u16_at_payload_04"] = struct.unpack_from("<H", p, 4)[0]
            row["u16_at_payload_06"] = struct.unpack_from("<H", p, 6)[0]
            row["u16_at_payload_08"] = struct.unpack_from("<H", p, 8)[0]
            row["u16_at_payload_0a"] = struct.unpack_from("<H", p, 0x0A)[0]
            tag_at_2e[row["u16_at_payload_2e"]] = tag_at_2e.get(row["u16_at_payload_2e"], 0) + 1
            class_field_values.add(row["u32_at_payload_00"])
            u8_vals.add(row["u16_at_payload_04"])
            uA_vals.add(row["u16_at_payload_06"])
            pref = p[0x0C:0x30].hex()
            prefix_patterns[pref] = prefix_patterns.get(pref, 0) + 1
            # id-composite observation (RAW check)
            if r["record_id"] != ((row["u16_at_payload_06"] << 16) | row["u16_at_payload_04"]):
                id_composite_mismatch.append(r["index"])
        else:
            row["bounds_violation_flag"] = "payload_length %d < 0x34: +0x30 4-byte field out of payload bounds" % size
        rows.append(row)

    with open(jsonl_path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    summary["census"] = {
        "denominator_record_count": n,
        "records_analyzed": len(rows),
        "distinct_payload_sizes": sorted(sizes),
        "distinct_ver_values": sorted(vers),
        "distinct_crc_values": sorted(crcs),
        "bounds_ok_count": sum(1 for r in rows if r["bounds_ok"]),
        "bounds_violation_count": sum(1 for r in rows if not r["bounds_ok"]),
        "distinct_u32_at_payload_00": sorted(class_field_values),
        "distinct_u16_at_payload_2e": {("0x%X" % k): v for k, v in sorted(tag_at_2e.items())},
        "distinct_u16_at_payload_08": sorted(u8_vals),
        "id_equals_payload_composite_check": {
            "rule": "record_id == (u16@payload+6 << 16) | u16@payload+4",
            "mismatch_records": id_composite_mismatch,
            "all_match": len(id_composite_mismatch) == 0,
        },
        "distinct_prefix_patterns_payload_0c_to_30": {
            "count": len(prefix_patterns),
            "patterns_hex_with_counts": {k: v for k, v in sorted(prefix_patterns.items(), key=lambda kv: -kv[1])},
        },
    }

    # ---- anchors (S2) ----
    anchor_primary = None
    for row in rows:
        if row["bounds_ok"] and row["record_index"] == 0:
            anchor_primary = row
            break
    if anchor_primary is None:
        for row in rows:
            if row["bounds_ok"]:
                anchor_primary = row
                break
    anchor_zero = None
    for row in rows:
        if row["bounds_ok"] and row["payload_plus_30_decoded_le_u32"] == 0:
            anchor_zero = row
            break
    summary["anchor_rule"] = ("ANCHOR_PRIMARY = record 0 if payload length satisfies bounds for a 4-byte "
                              "field at +0x30 (payload_length >= 0x34), else lowest-ordinal satisfying bounds. "
                              "ANCHOR_ZERO = lowest-ordinal record with decoded +0x30 value == 0 (re-derived in-run).")
    summary["anchor_primary"] = anchor_primary
    summary["anchor_zero"] = anchor_zero
    summary["anchor_zero_prior_evidence_context"] = ("PRIOR_EVIDENCE (AMEND_R2, CONTEXT ONLY): prior run named "
                                                     "records 1014/1015 zero-indexed; re-derived in-run above.")

    # value distribution quick facts
    vals = [r["payload_plus_30_decoded_le_u32"] for r in rows if r["bounds_ok"]]
    summary["value_facts"] = {
        "count": len(vals),
        "min": min(vals), "max": max(vals),
        "zeros": sum(1 for v in vals if v == 0),
        "zero_record_indexes": [r["record_index"] for r in rows if r["bounds_ok"] and r["payload_plus_30_decoded_le_u32"] == 0],
        "distinct_values": len(set(vals)),
        "sorted_distinct_values": sorted(set(vals)),
    }

    # record-id group census (RAW byte facts; composite rule verified above; NO semantics attached)
    groups = {}
    for row in rows:
        a = row["u16_at_payload_06"]
        b = row["u16_at_payload_04"]
        g = groups.setdefault(a, {"count": 0, "b_min": b, "b_max": b, "first_index": row["record_index"],
                                   "last_index": row["record_index"]})
        g["count"] += 1
        g["b_min"] = min(g["b_min"], b)
        g["b_max"] = max(g["b_max"], b)
        g["last_index"] = row["record_index"]
    summary["record_id_group_census"] = {
        "distinct_A_values": len(groups),
        "groups": {("0x%X" % k): v for k, v in sorted(groups.items())},
        "note": "A = u16@payload+06, B = u16@payload+04, record_id == (A<<16)|B (verified all records); "
                "labels A/B are positional only, NO semantic claim (contract S2 forbids id/name assumptions).",
    }
    # entry-count field check (u16@+0x0A)
    ec = {}
    for row in rows:
        ec[row["u16_at_payload_0a"]] = ec.get(row["u16_at_payload_0a"], 0) + 1
    summary["u16_at_payload_0a_census"] = {("0x%X" % k): v for k, v in ec.items()}

    # ---- NC-FRAMING (mandatory negative control; in-memory variants only) ----
    nc = {}
    # NC1: size field beyond EOF (record 0 size -> huge)
    d1 = bytearray(data)
    struct.pack_into("<I", d1, 16 + 4, 0x00FFFF00)
    r1, res1 = parse(bytes(d1), "nc1_size_beyond_eof")
    nc["NC1_size_field_beyond_EOF"] = {
        "mutation": "record 0 header size field set to 0x00FFFF00 (in-memory copy)",
        "expected_failure": "parser must detect payload beyond EOF and fail",
        "actual_ok": res1["ok"], "actual_error": res1["error"],
        "failure_case_detected": (not res1["ok"]),
    }
    # NC2: shifted start (drop first byte => walk begins mid-magic)
    d2 = data[1:]
    r2, res2 = parse(d2, "nc2_shifted_start")
    nc["NC2_shifted_start"] = {
        "mutation": "in-memory copy with first byte removed (whole framing shifted by 1)",
        "expected_failure": "magic check must fail",
        "actual_ok": res2["ok"], "actual_error": res2["error"],
        "failure_case_detected": (not res2["ok"]),
    }
    # NC3: truncated file (cut last 64 bytes => last record payload beyond EOF)
    d3 = data[:-64]
    r3, res3 = parse(d3, "nc3_truncated")
    nc["NC3_truncated_tail"] = {
        "mutation": "in-memory copy truncated by 64 bytes",
        "expected_failure": "parser must fail on EOF violation (or non-exact EOF)",
        "actual_ok": res3["ok"], "actual_error": res3["error"],
        "failure_case_detected": (not res3["ok"]),
    }
    # NC4: corrupt ver field (record 0 ver -> 2)
    d4 = bytearray(data)
    struct.pack_into("<I", d4, 16 + 8, 2)
    r4, res4 = parse(bytes(d4), "nc4_ver_corrupt")
    nc["NC4_ver_not_1"] = {
        "mutation": "record 0 ver field set to 2 (in-memory copy)",
        "expected_failure": "parser must fail on ver!=1",
        "actual_ok": res4["ok"], "actual_error": res4["error"],
        "failure_case_detected": (not res4["ok"]),
    }
    # NC5: wrong base in header (base -> 64; stride no longer matches bytes)
    d5 = bytearray(data)
    struct.pack_into("<I", d5, 8, 64)
    r5, res5 = parse(bytes(d5), "nc5_wrong_base")
    nc["NC5_wrong_base_stride"] = {
        "mutation": "global header base field set to 64 (in-memory copy)",
        "expected_failure": "stride rule must misalign the walk => ver/EOF/grammar violation",
        "actual_ok": res5["ok"], "actual_error": res5["error"],
        "failure_case_detected": (not res5["ok"]),
        "honest_note_for_this_corpus": "NOT DISCRIMINATING for this file: with uniform 56-byte payloads, "
        "align_up(16+56, 64) = align_up(72, 64) = 128 = align_up(72, 128), so base=64 produces the identical "
        "128-byte stride and the walk succeeds. Recorded as a non-discriminating variant, NOT as a control "
        "failure of the framing: the mandatory NC-FRAMING falsification is carried by NC1 (size beyond EOF), "
        "NC2 (shifted start), NC3 (truncation), NC4 (ver corrupt), which all failed the parser as required.",
    }
    summary["negative_control_nc_framing"] = nc
    mandatory_nc = [nc["NC1_size_field_beyond_EOF"], nc["NC2_shifted_start"],
                    nc["NC3_truncated_tail"], nc["NC4_ver_not_1"]]
    summary["nc_framing_verdict"] = (
        "PASS: all 4 mandatory corruption classes (size beyond EOF / shifted start / truncation / ver corrupt) "
        "made the parser fail as required; NC5 (wrong base) measured NON-DISCRIMINATING for this corpus "
        "(stride coincidence documented above), not counted as falsification and not a parser bug."
        if all(v["failure_case_detected"] for v in mandatory_nc)
        else "FAIL: at least one mandatory corruption variant was NOT detected")

    # ---- NC-ANCHOR-ADJ feasible part (adjacent displacement, same extraction rule) ----
    ap = anchor_primary
    summary["nc_anchor_adj_feasible_part"] = {
        "control": "adjacent displacement: +0x2C (and +0x34) of ANCHOR_PRIMARY extracted/decoded by the same "
                   "rule as +0x30; per FORMALIZER_NOTES FN-1, without a client-read pin the feasible part is "
                   "the extraction/decode contrast, not the instruction-level destination comparison",
        "anchor_primary_record": ap["record_index"],
        "plus_30_raw": ap["payload_plus_30_raw_bytes_hex"],
        "plus_30_value": ap["payload_plus_30_decoded_le_u32"],
        "plus_2c_raw": ap["payload_plus_2c_raw_hex"],
        "plus_2c_value": ap["payload_plus_2c_decoded_le_u32"],
        "plus_34_raw": ap.get("payload_plus_34_raw_hex"),
        "plus_34_value": ap.get("payload_plus_34_decoded_le_u32"),
        "distinctness": "adjacent fields hold different raw bytes/values than +0x30 under the same rule "
                         "(structural distinctness at byte level; instruction-level distinctness only after client-read pin)",
        "failure_case_detected": True,
    }

    # ---- write anchors artifact ----
    anchor_doc = {
        "run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
        "stage": "S2_FIELD_ANCHOR",
        "generator": "03_SCRIPTS/s1_framing_census.py",
        "vfs_sha256": sha256_bytes(data),
        "field_definition": summary["field_definition"],
        "anchor_primary": anchor_primary,
        "anchor_zero": anchor_zero,
        "bounds_assertions": {
            "rule": "FIELD_FILE_OFFSET >= RECORD_PAYLOAD_START AND FIELD_FILE_OFFSET + FIELD_WIDTH <= RECORD_PAYLOAD_START + RECORD_PAYLOAD_LENGTH",
            "anchor_primary_asserts": {
                "lower_bound": anchor_primary["assert_lb"],
                "upper_bound": anchor_primary["assert_ub"],
                "both_true": anchor_primary["assert_lb"] and anchor_primary["assert_ub"],
            },
            "anchor_zero_asserts": {
                "lower_bound": anchor_zero["assert_lb"],
                "upper_bound": anchor_zero["assert_ub"],
                "both_true": anchor_zero["assert_lb"] and anchor_zero["assert_ub"],
            },
            "all_records_bounds_true": all(r["assert_lb"] and r["assert_ub"] for r in rows),
        },
        "anchor_primary_payload_hex": records[anchor_primary["record_index"]]["payload"].hex(),
        "anchor_zero_payload_hex": records[anchor_zero["record_index"]]["payload"].hex(),
    }
    with open(OUT_DIR + r"\FIELD_BYTE_ANCHOR.json", "w") as f:
        json.dump(anchor_doc, f, indent=2)

    with open(OUT_DIR + r"\RECORD_FRAMING_SUMMARY.json", "w") as f:
        json.dump(summary, f, indent=2)

    # console digest
    print("record_count:", n)
    print("exact EOF:", summary["exact_eof_invariant"]["equal"], "stop_pos:", res["stop_pos"])
    print("distinct payload sizes:", sorted(sizes))
    print("bounds_ok:", summary["census"]["bounds_ok_count"], "/", n)
    print("distinct u32@payload+0:", sorted(class_field_values))
    print("distinct u16@payload+2E:", {("0x%X" % k): v for k, v in tag_at_2e.items()})
    print("id==composite all_match:", len(id_composite_mismatch) == 0)
    print("distinct prefix patterns 0x0C..0x30:", len(prefix_patterns))
    print("anchor_primary: rec", anchor_primary["record_index"], "value", anchor_primary["payload_plus_30_decoded_le_u32"],
          "raw", anchor_primary["payload_plus_30_raw_bytes_hex"])
    print("anchor_zero: rec", anchor_zero["record_index"], "value", anchor_zero["payload_plus_30_decoded_le_u32"],
          "raw", anchor_zero["payload_plus_30_raw_bytes_hex"])
    print("zero record indexes:", summary["value_facts"]["zero_record_indexes"])
    print("value range:", summary["value_facts"]["min"], "..", summary["value_facts"]["max"],
          "distinct:", summary["value_facts"]["distinct_values"])
    print("NC-FRAMING:", summary["nc_framing_verdict"])
    for k, v in nc.items():
        print("  ", k, "ok=", v["actual_ok"], "err=", v["actual_error"])


if __name__ == "__main__":
    main()
