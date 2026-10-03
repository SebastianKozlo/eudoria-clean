#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S10 SIDS ENTRY PARSE (measured layout) + G6 CURATION —
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

1. Curates the LOCAL-ONLY g6 dump (FUN_00821e70, the sids payload->map parser)
   into 01_RAW/G6_SIDS_PARSER.json + 01_RAW/G6_DECOMPILE_I01_sids_parser_00821e70_00821E70.c.
2. Data-side parse of the sids.vfs single record payload using the LAYOUT
   MEASURED FROM CODE (g6): u16 entry-count at payload+0; then per entry a
   string (encoding auto-calibrated: u16len / u8len / asciiz — the candidate
   that closes the payload exactly with the header count wins) followed by a
   u32 id (g6: FUN_0040de60(4) read into the map key).
3. Census of the anchored immediate series among the parsed entry ids
   (0xFD4..0xFD9, 0x376, 0xFAB, 0xFAE..0xFB2) and bounded dump of the matching
   entries (id + string). NO claims beyond the measured layout.

Interpreter: python 3.12.10. Invoke: python 03_SCRIPTS/s10_sids_entry_parse.py
Output: 01_RAW/SIDS_ENTRY_PARSE.json + 01_RAW/G6_SIDS_PARSER.json (+ .c)
"""

import json
import os
import struct
import zlib

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
SCRATCH = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003"
SIDS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\sids.vfs"

CENSUS = [0xFD4, 0xFD5, 0xFD6, 0xFD7, 0xFD8, 0xFD9, 0x376, 0xFAB,
          0xFAE, 0xFAF, 0xFB0, 0xFB1, 0xFB2]


def read_sids_record():
    data = open(SIDS, "rb").read()
    assert data[:8] == b"ArkVFS02"
    base = struct.unpack_from("<I", data, 8)[0]
    bid, bsize, bver, bcrc = struct.unpack_from("<IIII", data, 16)
    payload = data[32: 32 + bsize]
    crc_ok = (zlib.crc32(payload) & 0xFFFFFFFF) == bcrc
    return {"container_record_id": bid, "size": bsize, "ver": bver,
            "crc_ok": crc_ok, "payload": payload, "file_size": len(data)}


def parse_entries(payload, encoding):
    """u16 count; then count x (string(encoding), u32 id). Returns entries or None."""
    if len(payload) < 2:
        return None
    count = struct.unpack_from("<H", payload, 0)[0]
    pos = 2
    entries = []
    for i in range(count):
        if encoding == "u16len":
            if pos + 2 > len(payload):
                return None
            ln = struct.unpack_from("<H", payload, pos)[0]
            pos += 2
            if pos + ln + 4 > len(payload):
                return None
            s = payload[pos:pos + ln]
            pos += ln
        elif encoding == "u8len":
            if pos + 1 > len(payload):
                return None
            ln = payload[pos]
            pos += 1
            if pos + ln + 4 > len(payload):
                return None
            s = payload[pos:pos + ln]
            pos += ln
        elif encoding == "asciiz":
            end = payload.find(b"\x00", pos)
            if end < 0 or end + 1 + 4 > len(payload):
                return None
            s = payload[pos:end]
            pos = end + 1
        else:
            return None
        sid = struct.unpack_from("<I", payload, pos)[0]
        pos += 4
        entries.append((sid, s))
    if pos != len(payload):
        return None
    return count, entries


def main():
    res = {"run_id": RUN_ID, "stage": "S10_sids_entry_parse",
           "measured": {}, "interpreted": {}, "errors": []}
    M = res["measured"]

    # ---- g6 curation
    with open(os.path.join(SCRATCH, "g6_sids_parser.json"), "r") as f:
        g6 = json.load(f)
    with open(os.path.join(RAWDIR, "G6_SIDS_PARSER.json"), "w", encoding="utf-8") as f:
        json.dump({"run_id": RUN_ID, "stage": "G6_curated_sids_parser",
                   "source": {
                       "ghidra": "11.2.1 PUBLIC (analyzeHeadless; fresh project LANDMARK4057)",
                       "target": "sandbox copy of D:\\Eudoria_Reconstruction\\pcg_install\\Entropia.exe (SHA256 E7785430... pinned)",
                       "postscript": "03_SCRIPTS/g6_sids_parser.py (hash in 03_SCRIPTS/SCRIPT_SHA256.csv)"},
                   "measured": g6.get("measured", {}),
                   "errors": g6.get("errors", [])}, f, indent=2)
    d = g6["measured"]["functions"]["I01_sids_parser_00821e70"]
    with open(os.path.join(RAWDIR, "G6_DECOMPILE_I01_sids_parser_00821e70_00821E70.c"),
              "w", encoding="utf-8") as f:
        f.write("// I01_sids_parser_00821e70 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)\n")
        f.write("// listing + callers + callees: 01_RAW/G6_SIDS_PARSER.json\n")
        f.write(d.get("decompile_c") or "")

    # ---- sids.vfs record + payload parse (measured layout)
    rec = read_sids_record()
    M["sids_container_record"] = {k: rec[k] for k in ("container_record_id", "size", "ver", "crc_ok", "file_size")}
    M["parse_trials"] = {}
    chosen = None
    for enc in ("u16len", "u8len", "asciiz"):
        r = parse_entries(rec["payload"], enc)
        M["parse_trials"][enc] = {"ok": r is not None,
                                  "count": (r[0] if r else None),
                                  "entries": (len(r[1]) if r else None)}
        if r is not None and chosen is None:
            chosen = (enc, r[0], r[1])
    if chosen is None:
        res["errors"].append("no candidate string encoding closes the sids payload exactly — layout NOT confirmed")
        M["parse_result"] = {"ok": False}
    else:
        enc, count, entries = chosen
        ids = {}
        for (sid, s) in entries:
            ids.setdefault(sid, s)
        M["parse_result"] = {"ok": True, "encoding": enc, "count": count,
                            "entries": len(entries), "unique_ids": len(ids)}
        M["series_census_in_parsed_ids"] = {("0x%X" % v): (v in ids) for v in CENSUS}
        dumps = {}
        for v in CENSUS:
            if v in ids:
                dumps["0x%X" % v] = ids[v].decode("latin-1", "replace")[:160]
        M["series_entries_dump"] = dumps

    I = res["interpreted"]
    if M.get("parse_result", {}).get("ok"):
        I["MEASURED_LAYOUT"] = ("u16 count; count x (string[%s], u32 id) — from g6 code "
                               "(FUN_00821e70: FUN_0040de60(2)/FUN_0040de60(4) cursor reads; "
                               "FUN_00413da0 insert), calibrated on the physical payload by "
                               "exact-consumption" % M["parse_result"]["encoding"])
        I["IMMEDIATE_4057_IS_SIDS_ENTRY_ID"] = M["series_census_in_parsed_ids"].get("0xFD9", False)
        I["IMMEDIATE_886_IS_SIDS_ENTRY_ID"] = M["series_census_in_parsed_ids"].get("0x376", False)
        I["SUPERSEDES"] = ("SIDS_REPINS.json's container-level census (record ids): the sids.vfs "
                          "container holds ONE record; the string-table ids are PAYLOAD entries, "
                          "parsed per the measured layout here")
    I["pin_provenance"] = {
        "sids_entry_parse": {
            "MEASURED_QUANTITY": "sids.vfs single-record header + payload entry ids/strings parsed with the code-measured layout (u16 count; string; u32 id)",
            "INDEPENDENT_SOURCE_OF_TRUTH": "physical bytes of sids.vfs (identity pinned in SIDS_REPINS.json); layout from the g6 decompile of the client's own parser FUN_00821e70 (byte-anchored listing, zero template-machinery hits)",
            "WHY_NON_CIRCULAR": "two independent sides: the CODE (parser reads u16 count, string, u32 id) and the DATA (the payload closes exactly under that layout with the header count) — neither derives from the other; the 4057 hypothesis enters only as a census needle",
            "FAILURE_CASE_DETECTED": "a wrong layout would not close the payload exactly (parse_trials recorded for all candidates); if 0xFD9 were absent from the parsed ids, IMMEDIATE_4057_IS_SIDS_ENTRY_ID would be False and the string-table reading would be downgraded to UNRESOLVED"},
    }

    with open(os.path.join(RAWDIR, "SIDS_ENTRY_PARSE.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("S10 written: 01_RAW/SIDS_ENTRY_PARSE.json")
    print("errors:", res["errors"])
    print("container record:", M["sids_container_record"])
    print("parse trials:", M["parse_trials"])
    print("parse result:", M.get("parse_result"))
    print("series census:", M.get("series_census_in_parsed_ids"))
    print("series entries:")
    for k, v in (M.get("series_entries_dump") or {}).items():
        print("   %s -> %r" % (k, v))


if __name__ == "__main__":
    main()
