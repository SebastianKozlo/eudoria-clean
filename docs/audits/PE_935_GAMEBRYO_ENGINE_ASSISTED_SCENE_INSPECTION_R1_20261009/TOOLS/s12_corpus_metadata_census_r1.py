#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s12_corpus_metadata_census_r1.py — PE corpus metadata census (Work Package C,
contract section 8) for RUN_ID PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009.

LINEAGE DISCLOSURE — REUSED CODE (adapted copy), NOT an independent implementation:
  - BNT2 index structure + fail-closed walk: VERBATIM COPY of the documented
    s01_bnt2_walk.py (PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915,
    canonical SHA256 60EBC604F3645C839F56D163E6DA6C873DC7CF2E5BE1CA2D2955D430C39FF65F,
    byte-identical copy at TOOLS/s01_bnt2_walk_r1.py). READ_ONLY canonical.
  - NIF header line/version/zlib handling: adapted from s02_nif_version_scan.py
    (same Rosetta run).
  - NIF 10.1.0.0 type-table scan: adapted from s03_type_census.py
    (scan_101_header, same fail-closed bounds).
  - Calibration anchors + 218757 index cross-checks: from the s1_extract.py canon
    (PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20260903), used as CALIBRATION
    ONLY (historical values are NOT extraction authority; this run re-derives
    everything from the pinned BNT bytes).
  - 4.1.0.12 num_blocks header field: layout per the demonstrated
    nif_parser_v2.py lineage (header line + version u32 + num_blocks u32;
    BE04C79EB37FF982AD66EDC43034C8486630CA7227A7CCDDE8F0B8C35307ABCD).
    4.x type histograms are HEADER_UNSUPPORTED (inline per-block type names =
    block-body decoding, beyond a metadata census).

Scope (bounded): the pinned Models.bnt ONLY. No other container, no whole-
installation scan, no arbitrary byte scanning for fake headers.

Outputs:
  02_PE/CORPUS_METADATA_CENSUS.csv      (all indexed entries, one row each)
  02_PE/CENSUS_SUMMARY.json            (denominators, calibration, controls)
  LOCAL_ONLY 02_PE_work/per_entry_full.json  (full per-file type histograms)
"""
import csv
import hashlib
import json
import os
import struct
import sys
import zlib
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s01_bnt2_walk_r1 as s01  # noqa: E402  (verbatim documented walker)

RUN_ID = "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009"
ARCHIVE = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
OUT_ROOT = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PE_OUT = os.path.join(OUT_ROOT, "02_PE")
LOCAL_ROOT = (r"D:\Eudoria_Reconstruction\99_Audits"
              r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
LOCAL_WORK = os.path.join(LOCAL_ROOT, "02_PE_work")

EXPECT = {
    "models_size": 395412868,
    "models_sha256": "C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0",
    "index_start": 395262727,
    "index_count": 5596,
    "anchor_296445_nif_nameoff": 395268773,
    "target_218757": {"index": 781, "size": 57316, "offset": 116223520,
                      "name_off": 395283797},
}

KNOWN = {0x0A010000: "10.1.0.0", 0x0401000C: "4.1.0.12", 0x04000002: "4.0.0.2"}
V10 = 0x0A010000
ZLIB_MAGICS = (b"\x78\x01", b"\x78\x5E", b"\x78\x9C", b"\x78\xDA")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def index_name_offsets(path, index_start, count):
    """Supplementary walk of the documented index blob recording each entry's
    name file-offset (the layout is identical to the documented walker; used
    only for the name-offset CALIBRATION anchors)."""
    with open(path, "rb") as f:
        f.seek(index_start)
        blob = f.read()
    pos = 4
    offs = {}
    for i in range(count):
        nl = blob.find(b"\x0A", pos)
        if nl < 0:
            raise SystemExit("E_NAME_EOF at entry %d (offset walk)" % i)
        name = blob[pos:nl].decode("latin-1")
        offs[name] = index_start + pos
        pos = nl + 1 + 16
    if pos + 8 != len(blob):
        raise SystemExit("E_OFFSET_WALK_CLOSURE pos=%d len=%d" % (pos, len(blob)))
    return offs


def parse_header_line(data):
    """Documented s02 header parse: line + version u32. Returns
    (header_string, version, cursor_pos_after_version, err). The returned
    position is AFTER the version u32 (the s03 scan expects to start at the
    user-version field). Executor defect disclosure: the first execution of
    this script passed the position AT the version u32 into scan_101_header,
    producing a 4-byte shift and 5,595 E_TYPE_SCAN failures; caught from the
    failure reasons, fixed here, and re-run BEFORE any use of the outputs."""
    if len(data) < 8:
        return None, None, None, "E_TOO_SMALL"
    nl = data.find(b"\x0A")
    if nl < 0 or nl > 256:
        return None, None, None, "E_NO_HEADER_NEWLINE"
    try:
        hs = data[:nl].decode("ascii")
    except UnicodeDecodeError:
        return None, None, None, "E_HEADER_ASCII"
    pos = nl + 1
    if pos + 4 > len(data):
        return None, None, None, "E_SHORT_VERSION"
    version = struct.unpack("<I", data[pos:pos + 4])[0]
    pos += 4
    return hs, version, pos, None


def scan_101_header(data, pos):
    """Adapted VERBATIM-logic copy of s03_type_census.scan_101_header from the
    already-parsed version position. Same fail-closed bounds. Returns dict or
    raises ValueError."""
    if pos + 4 > len(data):
        raise ValueError("E_SHORT_USERVER")
    user_version = struct.unpack("<I", data[pos:pos + 4])[0]
    pos += 4
    if pos + 4 > len(data):
        raise ValueError("E_SHORT_NUMBLOCKS")
    num_blocks = struct.unpack("<I", data[pos:pos + 4])[0]
    pos += 4
    if num_blocks > 1_000_000:
        raise ValueError(f"E_NUMBLOCKS_SANITY:{num_blocks}")
    if pos + 2 > len(data):
        raise ValueError("E_SHORT_NUMBLOCKTYPES")
    num_block_types = struct.unpack("<H", data[pos:pos + 2])[0]
    pos += 2
    if num_block_types == 0 or num_block_types > 4096:
        raise ValueError(f"E_NUMBLOCKTYPES_SANITY:{num_block_types}")
    names = []
    for i in range(num_block_types):
        if pos + 4 > len(data):
            raise ValueError(f"E_SHORT_TYPELEN:{i}")
        ln = struct.unpack("<I", data[pos:pos + 4])[0]
        pos += 4
        if not 1 <= ln <= 256:
            raise ValueError(f"E_TYPELEN_RANGE:{i}:{ln}")
        if pos + ln > len(data):
            raise ValueError(f"E_SHORT_TYPE:{i}")
        names.append(data[pos:pos + ln].decode("ascii"))
        pos += ln
    idx = []
    for i in range(num_blocks):
        if pos + 2 > len(data):
            raise ValueError(f"E_SHORT_IDX:{i}")
        t = struct.unpack("<H", data[pos:pos + 2])[0]
        pos += 2
        if t >= num_block_types:
            raise ValueError(f"E_IDX_OOB:{i}:{t}>={num_block_types}")
        idx.append(t)
    if pos + 4 > len(data):
        raise ValueError("E_SHORT_NUMGROUPS")
    num_groups = struct.unpack("<I", data[pos:pos + 4])[0]
    pos += 4
    if num_groups > 1_000_000:
        raise ValueError(f"E_NUMGROUPS_SANITY:{num_groups}")
    group_sizes = []
    for i in range(num_groups):
        if pos + 4 > len(data):
            raise ValueError(f"E_SHORT_GROUPSIZE:{i}")
        group_sizes.append(struct.unpack("<I", data[pos:pos + 4])[0])
        pos += 4
    first_group_id = None
    if num_blocks > 0:
        if pos + 4 > len(data):
            raise ValueError("E_SHORT_GROUPID0")
        first_group_id = struct.unpack("<I", data[pos:pos + 4])[0]
        pos += 4
    return {
        "user_version": user_version, "num_blocks": num_blocks,
        "num_block_types": num_block_types, "block_types": names,
        "block_type_index": idx, "num_groups": num_groups,
        "group_sizes": group_sizes, "first_block_group_id": first_group_id,
        "blocks_start": pos,
    }


def compact_hist(counts):
    return ";".join("%s=%d" % (k, counts[k])
                    for k in sorted(counts, key=lambda k: (-counts[k], k)))


def main():
    os.makedirs(PE_OUT, exist_ok=True)
    os.makedirs(LOCAL_WORK, exist_ok=True)
    summary = {"run_id": RUN_ID, "stage": "S12_corpus_metadata_census",
               "measured": {}, "failures": []}
    M = summary["measured"]

    # ---- input identity (fail-closed vs pin)
    st = os.stat(ARCHIVE)
    sha = sha256_file(ARCHIVE)
    M["models_bnt"] = {"path": ARCHIVE, "size_bytes": st.st_size,
                       "sha256": sha,
                       "pin_match": (st.st_size == EXPECT["models_size"]
                                     and sha == EXPECT["models_sha256"])}
    if not M["models_bnt"]["pin_match"]:
        raise SystemExit("E_INPUT_HASH: Models.bnt changed vs pin")

    # ---- documented walker negative controls (synthetic archives only)
    ok, controls = s01.run_negative_controls()
    M["walker_negative_controls"] = {"results": controls, "all_ok": ok}
    if not ok:
        raise SystemExit("E_WALKER_CONTROLS: negative control battery failed")

    # ---- documented fail-closed walk of the pinned archive
    walk = s01.walk_bnt2(ARCHIVE)
    entries = walk["entries"]
    M["walk"] = {k: walk[k] for k in
                 ("file_size", "dir_offset", "num_entries", "coverage_bytes",
                  "interior_gap_bytes", "interior_gap_count", "trailing_gap_bytes")}
    # ---- calibration (fail-closed; historical values are cross-checks)
    cal = {
        "index_start": walk["dir_offset"] == EXPECT["index_start"],
        "index_count": walk["num_entries"] == EXPECT["index_count"],
        "anchor_296445_nif_nameoff": None,
        "target_218757_index": None,
        "target_218757_size_offset": None,
        "target_218757_nameoff": None,
    }
    name_offs = index_name_offsets(ARCHIVE, walk["dir_offset"],
                                   walk["num_entries"])
    cal["anchor_296445_nif_nameoff"] = (
        name_offs.get("296445.nif") == EXPECT["anchor_296445_nif_nameoff"])
    t = None
    for e in entries:
        if e["name"] == "218757.nif":
            t = e
            break
    if t is None:
        raise SystemExit("E_CAL: 218757.nif not found in index")
    cal["target_218757_index"] = t["index"] == EXPECT["target_218757"]["index"]
    cal["target_218757_size_offset"] = (
        t["size"] == EXPECT["target_218757"]["size"]
        and t["offset"] == EXPECT["target_218757"]["offset"])
    cal["target_218757_nameoff"] = (
        name_offs.get("218757.nif") == EXPECT["target_218757"]["name_off"])
    M["calibration"] = {"checks": cal, "calibration_ok": all(cal.values()),
                        "target_218757_entry": t}
    if not all(cal.values()):
        raise SystemExit("E_CAL: calibration mismatch: %r" % cal)

    # ---- per-entry census
    rows = []
    full_histos = {}
    counts_status = Counter()
    version_counts = Counter()
    compression_counts = Counter()
    ext_counts = Counter()
    text_mismatch = 0
    failures = []
    with open(ARCHIVE, "rb") as f:
        for e in entries:
            f.seek(e["offset"])
            raw = f.read(e["size"])
            if len(raw) != e["size"]:
                failures.append({"entry_index": e["index"], "name": e["name"],
                                 "reason": "E_PAYLOAD_READ",
                                 "detail": "%d/%d" % (len(raw), e["size"])})
                continue
            sha_raw = hashlib.sha256(raw).hexdigest().upper()
            compression = "raw"
            data = raw
            if raw[:2] in ZLIB_MAGICS:
                try:
                    data = zlib.decompress(raw)
                    compression = "zlib"
                except zlib.error as zerr:
                    hs, ver, pos, err = parse_header_line(raw)
                    if err is None and ver in KNOWN:
                        compression = "raw(suspicious-zlib-magic:%s)" % zerr
                    else:
                        failures.append({"entry_index": e["index"],
                                         "name": e["name"],
                                         "reason": "E_ZLIB_DECOMPRESS",
                                         "detail": str(zerr)})
                        continue
            compression_counts[compression] += 1
            ext = e["name"].rsplit(".", 1)[-1].lower() if "." in e["name"] else ""
            ext_counts[ext] += 1
            hs, ver, pos, err = parse_header_line(data)
            if err is not None:
                failures.append({"entry_index": e["index"], "name": e["name"],
                                 "reason": err, "detail": "comp=%s" % compression})
                continue
            label = KNOWN.get(ver, "OTHER")
            version_counts["%s(0x%08X)" % (label, ver)] += 1
            tv = ""
            if "Version " in hs:
                tv = hs.split("Version ", 1)[1].strip()
            tv_ok = ""
            if label != "OTHER" and tv:
                tv_ok = "MATCH" if tv == label else "MISMATCH"
            if tv_ok == "MISMATCH":
                text_mismatch += 1

            row = {
                "entry_index": e["index"], "name": e["name"],
                "ext": ext, "size_stored": e["size"], "offset": e["offset"],
                "compression": compression, "sha256_stored": sha_raw,
                "header_string": hs,
                "version_hex": "0x%08X" % ver,
                "version_label": label,
                "header_version_text": tv, "text_version_match": tv_ok,
                "user_version": "", "num_blocks": "", "num_block_types": "",
                "type_histogram": "", "histogram_status": "",
                "field_c": "0x%08X" % e["field_c"],
                "field_d": "0x%08X" % e["field_d"],
                "scan_status": "SCANNED",
            }
            if ver == V10:
                try:
                    h = scan_101_header(data, pos)
                except ValueError as ex:
                    failures.append({"entry_index": e["index"], "name": e["name"],
                                    "reason": "E_TYPE_SCAN:" + str(ex),
                                    "detail": "v=0x%08X" % ver})
                    continue
                cnt = Counter(h["block_types"][i] for i in h["block_type_index"])
                row["user_version"] = h["user_version"]
                row["num_blocks"] = h["num_blocks"]
                row["num_block_types"] = h["num_block_types"]
                row["type_histogram"] = compact_hist(cnt)
                row["histogram_status"] = "SCANNED"
                counts_status["SCANNED_10_1"] += 1
                full_histos[e["name"]] = {
                    "entry_index": e["index"], "size": e["size"],
                    "offset": e["offset"], "sha256_stored": sha_raw,
                    "header_string": hs, "version": "0x%08X" % ver,
                    "user_version": h["user_version"],
                    "num_blocks": h["num_blocks"],
                    "num_block_types": h["num_block_types"],
                    "block_types": h["block_types"],
                    "type_counts": dict(cnt),
                    "num_groups": h["num_groups"],
                    "first_block_group_id": h["first_block_group_id"],
                    "blocks_start": h["blocks_start"],
                }
            elif ver == 0x0401000C:
                # 4.1.0.12: num_blocks u32 directly after version (demonstrated
                # nif_parser_v2 layout). Type histogram HEADER_UNSUPPORTED
                # (inline per-block type names = block-body decode).
                if pos + 4 > len(data):
                    failures.append({"entry_index": e["index"],
                                     "name": e["name"],
                                     "reason": "E_SHORT_NUMBLOCKS_4X",
                                     "detail": "comp=%s" % compression})
                    continue
                nb = struct.unpack("<I", data[pos:pos + 4])[0]
                if nb > 1_000_000:
                    failures.append({"entry_index": e["index"],
                                     "name": e["name"],
                                     "reason": "E_NUMBLOCKS_SANITY_4X:%d" % nb,
                                     "detail": ""})
                    continue
                row["num_blocks"] = nb
                row["histogram_status"] = "HEADER_UNSUPPORTED_INLINE_BLOCK_TYPES"
                counts_status["HEADER_UNSUPPORTED_4_1_0_12"] += 1
                full_histos[e["name"]] = {
                    "entry_index": e["index"], "size": e["size"],
                    "offset": e["offset"], "sha256_stored": sha_raw,
                    "header_string": hs, "version": "0x%08X" % ver,
                    "num_blocks": nb,
                    "type_counts": None,
                    "note": "inline per-block type names; header-level type "
                            "table not present in this NIF version",
                }
            else:
                # 4.0.0.2 / OTHER: version readable; table layout NOT
                # demonstrated for these headers -> HEADER_UNSUPPORTED.
                row["histogram_status"] = "HEADER_UNSUPPORTED"
                counts_status["HEADER_UNSUPPORTED_OTHER_VERSION"] += 1
                full_histos[e["name"]] = {
                    "entry_index": e["index"], "size": e["size"],
                    "offset": e["offset"], "sha256_stored": sha_raw,
                    "header_string": hs, "version": "0x%08X" % ver,
                    "type_counts": None,
                }
            rows.append(row)

    counts_status["FAILED"] = len(failures)
    denom = (counts_status["SCANNED_10_1"]
             + counts_status["HEADER_UNSUPPORTED_4_1_0_12"]
             + counts_status["HEADER_UNSUPPORTED_OTHER_VERSION"]
             + counts_status["FAILED"])
    M["denominators"] = {
        "entries": walk["num_entries"], "census_rows": len(rows),
        "status_counts": dict(counts_status),
        "census_rows_plus_failures": denom,
        "integrity_ok": denom == walk["num_entries"],
    }
    M["version_counts"] = dict(version_counts)
    M["compression_counts"] = dict(compression_counts)
    M["extension_counts"] = dict(ext_counts)
    M["text_version_mismatches"] = text_mismatch
    summary["failures"] = failures

    # ---- CSV
    cols = ["entry_index", "name", "ext", "size_stored", "offset", "compression",
            "sha256_stored", "header_string", "version_hex", "version_label",
            "header_version_text", "text_version_match", "user_version",
            "num_blocks", "num_block_types", "type_histogram",
            "histogram_status", "field_c", "field_d", "scan_status"]
    csv_path = os.path.join(PE_OUT, "CORPUS_METADATA_CENSUS.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})

    # ---- LOCAL_ONLY full histograms
    with open(os.path.join(LOCAL_WORK, "per_entry_full.json"), "w",
              encoding="utf-8") as f:
        json.dump(full_histos, f, indent=1)

    # ---- failures CSV (if any)
    if failures:
        with open(os.path.join(PE_OUT, "CENSUS_FAILURES.csv"), "w",
                  newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["entry_index", "name", "reason",
                                              "detail"])
            w.writeheader()
            for r in failures:
                w.writerow(r)

    with open(os.path.join(PE_OUT, "CENSUS_SUMMARY.json"), "w",
              encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({
        "entries": walk["num_entries"], "rows": len(rows),
        "status": dict(counts_status),
        "integrity_ok": denom == walk["num_entries"],
        "versions": dict(version_counts),
        "compression": dict(compression_counts),
        "extensions": dict(ext_counts),
        "text_version_mismatches": text_mismatch,
        "failures": len(failures),
    }, indent=2))


if __name__ == "__main__":
    main()
