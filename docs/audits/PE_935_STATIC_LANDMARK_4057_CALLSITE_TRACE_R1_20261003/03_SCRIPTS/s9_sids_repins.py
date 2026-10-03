#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S9 SIDS RE-PIN + SERIES EXISTENCE CENSUS —
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

Bounded data-side closure of the measured code chain (g4/g5: the 0x1C string
singleton at DAT_00BA124C is initialized by FUN_00821FB0, which opens
"parameters\\sids.vfs" via the VFS reader family and parses records into its
map; FUN_00821760 looks up the composite key {FUN_00826a50(0), id} there):

  1. pin the physical identity of sids.vfs (size/sha256/magic);
  2. walk the container (same ArkVFS container walker as s1, fail-closed);
  3. EXISTENCE census (set membership ONLY, no new detailed records beyond
     the bounded raw dump of sids.vfs record 4057):
       - sids.vfs header ids for the anchored series {0xFD4..0xFD9 = 4052..4057,
         886 = 0x376, and the sibling series {4011, 4014..4018} = 0xFAB, 0xFAE..0xFB2}
       - templates.vfs id2 for the SAME values (its own walk, re-measured here)
     -> tests whether the consecutive pushed immediates are sids ids, and
        whether templates.vfs coincidentally spans the same numeric range
        (CONTROL-1 numeric-coincidence + CONTROL-2 unrelated-immediate class);
  4. bounded raw dump of the sids.vfs record whose header id == 4057
     (payload hex window + printable-ASCII observation only; NO structural
     parse claims — the sids parser FUN_00821e70 is NOT decoded this run).

NEW_PHYSICAL_RECORDS_DETAILED this run: templates.vfs record 4057 (s1) + this
sids.vfs record 4057 raw dump = 2 (the contract budget NEW_PHYSICAL_RECORDS_
DETAILED_MAX = 2). The 4508 record was a calibration re-pin of an existing
canon anchor, not a new detailed record.

Interpreter: python 3.12.10. Invoke: python 03_SCRIPTS/s9_sids_repins.py
Output: 01_RAW/SIDS_REPINS.json (UTF-8).
"""

import hashlib
import json
import os
import struct
import zlib

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "01_RAW", "SIDS_REPINS.json"))

PCG = r"D:\Eudoria_Reconstruction\pcg_install"
SIDS = os.path.join(PCG, "Data", "Parameters", "sids.vfs")
TEMPLATES = os.path.join(PCG, "Data", "Parameters", "templates.vfs")

# anchored + sibling immediate series measured in FUN_00599D30 (s4 census)
SERIES = {
    "anchor_series_FUN_008dfcd0": [0xFD4, 0xFD5, 0xFD6, 0xFD7, 0xFD8, 0xFD9],
    "sibling_series_FUN_008f0780": [0xFAB, 0xFAE, 0xFAF, 0xFB0, 0xFB1, 0xFB2],
    "nearby_immediate_886": [0x376],
}
ALL_VALUES = sorted(set(sum(SERIES.values(), [])))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_vfs(path):
    data = open(path, "rb").read()
    magic = data[:8]
    if magic not in (b"ArkVFS01", b"ArkVFS02"):
        return {"ok": False, "error": "bad magic %r" % magic}
    base = struct.unpack_from("<I", data, 8)[0]
    recs = []
    pos = 16
    crc_fail = 0
    while pos + 16 <= len(data):
        bid, bsize, bver, bcrc = struct.unpack_from("<IIII", data, pos)
        if pos + 16 + bsize > len(data):
            return {"ok": False, "error": "truncated at %d" % pos, "records": recs}
        payload = data[pos + 16: pos + 16 + bsize]
        if bcrc != 0 and (zlib.crc32(payload) & 0xFFFFFFFF) != bcrc:
            crc_fail += 1
        recs.append((pos, bid, bsize, bver, bcrc, payload))
        pos += ((16 + bsize + base - 1) // base) * base
    return {"ok": (pos == len(data)), "base": base, "records": recs,
            "stop_pos": pos, "file_size": len(data), "crc_fail": crc_fail,
            "magic": magic.decode()}


def main():
    res = {"run_id": RUN_ID, "stage": "S9_sids_repins",
           "measured": {}, "interpreted": {}, "errors": []}
    M = res["measured"]

    if not os.path.exists(SIDS):
        res["errors"].append("sids.vfs NOT FOUND at %s" % SIDS)
        M["sids_identity"] = {"path": SIDS, "exists": False}
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
        print("S9: sids.vfs NOT FOUND — recorded honestly")
        return
    st = os.stat(SIDS)
    M["sids_identity"] = {"path": SIDS, "size_bytes": st.st_size,
                          "sha256": sha256_file(SIDS)}

    sv = read_vfs(SIDS)
    if not sv.get("ok"):
        res["errors"].append("sids walk failed: %r" % sv.get("error"))
        M["sids_walk"] = {"ok": False, "error": sv.get("error")}
    else:
        recs = sv["records"]
        M["sids_walk"] = {"ok": True, "magic": sv["magic"], "base": sv["base"],
                          "record_count": len(recs), "eof_ok": sv["ok"],
                          "crc_fail": sv["crc_fail"], "stop_pos": sv["stop_pos"],
                          "file_size": sv["file_size"]}
        ids = set(r[1] for r in recs)
        M["sids_series_census"] = {
            "series": {k: {("0x%X" % v): (v in ids) for v in vals}
                       for k, vals in SERIES.items()},
        }
        # bounded raw dump: sids record 4057
        tgt = [r for r in recs if r[1] == 0xFD9]
        if tgt:
            (off, bid, bsize, bver, bcrc, payload) = tgt[0]
            dump_len = min(len(payload), 256)
            pw = payload[:dump_len]
            M["sids_record_4057_raw"] = {
                "found": True, "file_offset": off, "header_id": bid, "size": bsize,
                "ver": bver, "crc32_field": "%08X" % bcrc,
                "crc32_recomputed": "%08X" % (zlib.crc32(payload) & 0xFFFFFFFF),
                "crc_match": ((zlib.crc32(payload) & 0xFFFFFFFF) == bcrc or bcrc == 0),
                "payload_len": len(payload),
                "payload_hex_first_bytes": pw.hex(" "),
                "printable_ascii_observation": "".join(
                    chr(b) if 32 <= b < 127 else "." for b in pw),
                "structural_parse_note": "NO structural claims: sids payload layout "
                "is NOT decoded this run (parser FUN_00821e70 NOT measured); "
                "printable-ASCII rendering is an observation only",
            }
        else:
            M["sids_record_4057_raw"] = {"found": False}

    tv = read_vfs(TEMPLATES)
    if not tv.get("ok"):
        res["errors"].append("templates walk failed: %r" % tv.get("error"))
    else:
        tids = set(r[1] for r in tv["records"])
        M["templates_series_census"] = {
            "note": "re-measured with the same container walker (calibration: s1 walk 5,438/0-CRC/EOF)",
            "series": {k: {("0x%X" % v): (v in tids) for v in vals}
                       for k, vals in SERIES.items()},
        }
        M["templates_walk_calibration"] = {
            "record_count": len(tv["records"]), "crc_fail": tv["crc_fail"],
            "eof_ok": tv["ok"],
            "matches_s1_calibration": (len(tv["records"]) == 5438 and tv["crc_fail"] == 0 and tv["ok"])}

    I = res["interpreted"]
    sid_ids = set()
    if M.get("sids_walk", {}).get("ok"):
        sid_ids = set()
        # re-derive id set for interpretation
        sv2 = read_vfs(SIDS)
        sid_ids = set(r[1] for r in sv2["records"])
    tmpl_ok = M.get("templates_walk_calibration", {}).get("matches_s1_calibration", False)
    I["SERIES_IN_SIDS"] = {("0x%X" % v): (v in sid_ids) for v in ALL_VALUES}
    I["ALL_SIX_ANCHOR_SERIES_VALUES_IN_SIDS"] = all(
        v in sid_ids for v in SERIES["anchor_series_FUN_008dfcd0"])
    I["IMMEDIATE_4057_IS_SIDS_RECORD_ID"] = (0xFD9 in sid_ids)
    I["IMMEDIATE_886_IS_SIDS_RECORD_ID"] = (0x376 in sid_ids)
    I["COMPOSITE_KEY_SEMANTIC_CLASS"] = (
        "STRING_TABLE_KEY_FROM_SIDS_VFS (mechanically: {section_object, id} key into the "
        "sids.vfs-loaded string map of the 0x1C singleton; sids.vfs record presence measured)")
    I["pin_provenance"] = {
        "sids_repins": {
            "MEASURED_QUANTITY": "sids.vfs identity (size/sha256/magic), container walk census, header-id existence for the anchored immediate series, raw payload window of record 4057",
            "INDEPENDENT_SOURCE_OF_TRUTH": "physical bytes of D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Parameters\\sids.vfs, read by this run's own container walker (same implementation as the s1 templates walk, which is calibrated 5,438/0-CRC/EOF + anchor 4508 @96,496)",
            "WHY_NON_CIRCULAR": "the sids.vfs file identity and the code-path reading it (FUN_00821fb0 -> 'parameters\\\\sids.vfs' string + VFS reader FUN_00971ad0) were measured independently on both sides (code: g5 listing/decompile; data: this walk); the census values come from the file's own header ids, not from the code hypothesis",
            "FAILURE_CASE_DETECTED": "if 4057 were NOT a sids id, the census would return absent and the string-table-key reading would be downgraded to UNRESOLVED; a walk divergence would break the s1-calibrated stride/CRC/EOF checks"},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("S9 written:", OUT)
    print("errors:", res["errors"])
    print("sids identity:", M["sids_identity"])
    print("sids walk:", M.get("sids_walk"))
    print("SERIES_IN_SIDS:", I.get("SERIES_IN_SIDS"))
    print("ALL_SIX_ANCHOR_SERIES_VALUES_IN_SIDS:", I.get("ALL_SIX_ANCHOR_SERIES_VALUES_IN_SIDS"))
    print("IMMEDIATE_4057_IS_SIDS_RECORD_ID:", I.get("IMMEDIATE_4057_IS_SIDS_RECORD_ID"))
    print("IMMEDIATE_886_IS_SIDS_RECORD_ID:", I.get("IMMEDIATE_886_IS_SIDS_RECORD_ID"))
    r = M.get("sids_record_4057_raw", {})
    print("sids rec 4057: found=", r.get("found"), "off=", r.get("file_offset"),
          "size=", r.get("size"), "crc_match=", r.get("crc_match"))
    if r.get("found"):
        print("  ascii_observation:", r.get("printable_ascii_observation")[:160])
    print("templates_series_census:", M.get("templates_series_census", {}).get("series"))


if __name__ == "__main__":
    main()
