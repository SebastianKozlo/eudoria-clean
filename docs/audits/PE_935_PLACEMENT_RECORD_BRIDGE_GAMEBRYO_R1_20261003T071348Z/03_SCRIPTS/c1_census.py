#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C1 CENSUS — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

Purpose (contract S3 enumeration + S6 physical-record pinning):
  1. Pin physical identities: templates.vfs, 20002.vfs, Models.bnt (read-only).
  2. Walk templates.vfs to exact EOF (ArkVFS02); count records; dump record id2=4508
     (the FAMILY-T physical-record candidate: A=296445) and record id2=11963
     (the FAMILY-P cross-check: value of 20002.vfs record 0 field payload+0x30).
  3. Re-pin the byte-level identity of the 20002.vfs record 0 field payload+0x30
     (BB 2E 00 00 = 11963) from this run's own read.
  4. Models.bnt BNT2 index: anchor 296445.nif @ name_file_offset 395,268,773 (E.7
     re-pin) + existence of 551661.nif and 296446.bvi-domain checks.
  5. id2-set membership census for the 20002.vfs payload+0x30 column (1366 records)
     — own measurement of the JOIN R1 lead (1,364/1,366 claim).

No original file is modified. Output: 01_RAW/C1_CENSUS.json (UTF-8).
"""

import hashlib
import json
import os
import struct
import zlib

RUN_ID = "PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z"
PCG = r"D:\Eudoria_Reconstruction\pcg_install"
PARAM = os.path.join(PCG, "Data", "Parameters")
TEMPLATES = os.path.join(PARAM, "templates.vfs")
V20002 = os.path.join(PARAM, "20002.vfs")
MODELS = os.path.join(PCG, "Data", "Models", "Models.bnt")
OUT = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + "01_RAW" + os.sep + "C1_CENSUS.json"

EXPECTED = {
    "templates_vfs_size": None,          # pinned by this census
    "v20002_size": 174864,
    "v20002_sha256": "C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4",
    "models_size": 395412868,
    "models_sha256": "C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0",
    "templates_records": 5438,
    "anchor_296445nif_nameoff": 395268773,
    "v20002_records": 1366,
    "v20002_rec0_off48": 11963,
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_vfs_permissive(path):
    """Permissive ArkVFS01/02 family walk (any ver; CRC gate only when field != 0).
    Returns dict; payload bytes kept only for requested ids (keeps memory sane)."""
    data = open(path, "rb").read()
    magic = data[:8]
    assert magic in (b"ArkVFS01", b"ArkVFS02"), magic
    base = struct.unpack_from("<I", data, 8)[0]
    recs = []
    pos = 16
    crc_fail = 0
    while pos + 16 <= len(data):
        bid, bsize, bver, bcrc = struct.unpack_from("<IIII", data, pos)
        if pos + 16 + bsize > len(data):
            return {"ok": False, "error": "truncated at %d" % pos, "base": base}
        payload = data[pos + 16: pos + 16 + bsize]
        if bcrc != 0:
            if (zlib.crc32(payload) & 0xFFFFFFFF) != bcrc:
                crc_fail += 1
        recs.append((len(recs), pos, bid, bsize, bver, bcrc, payload))
        pos += ((16 + bsize + base - 1) // base) * base
    eof_ok = (pos == len(data))
    return {"ok": eof_ok, "base": base, "records": recs, "stop_pos": pos,
            "eof_ok": eof_ok, "crc_fail": crc_fail, "size": len(data)}


def parse_bnt2_names(path, want_names):
    """Return {name: name_file_offset} for wanted names (index metadata only)."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(size - 8)
        tail = f.read(8)
    index_start, = struct.unpack("<I", tail[:4])
    assert tail[4:] == b"BNT2"
    with open(path, "rb") as f:
        f.seek(index_start)
        blob = f.read()
    count, = struct.unpack_from("<I", blob, 0)
    out = {}
    pos = 4
    for i in range(count):
        nl = blob.find(b"\x0a", pos)
        if nl < 0:
            break
        name = blob[pos:nl].decode("latin-1")
        name_file_offset = index_start + pos
        pos = nl + 1
        if name in want_names:
            out[name] = name_file_offset
        pos += 16
    return out, count, index_start


def main():
    res = {"run_id": RUN_ID, "stage": "C1_census", "measured": {}, "interpreted": {}, "errors": []}

    # --- identity pins
    for label, p in (("templates_vfs", TEMPLATES), ("v20002", V20002), ("models_bnt", MODELS)):
        st = os.stat(p)
        res["measured"][label] = {
            "path": p, "size_bytes": st.st_size, "sha256": sha256_file(p),
        }
    m = res["measured"]
    # pin checks
    res["interpreted"]["v20002_pin_match"] = (m["v20002"]["sha256"] == EXPECTED["v20002_sha256"]
                                              and m["v20002"]["size_bytes"] == EXPECTED["v20002_size"])
    res["interpreted"]["models_pin_match"] = (m["models_bnt"]["sha256"] == EXPECTED["models_sha256"]
                                              and m["models_bnt"]["size_bytes"] == EXPECTED["models_size"])

    # --- templates.vfs walk
    tv = read_vfs_permissive(TEMPLATES)
    if not tv["ok"]:
        res["errors"].append("templates walk failed: %r" % tv.get("error"))
    recs = tv["records"]
    res["measured"]["templates_walk"] = {
        "base": tv["base"], "record_count": len(recs), "eof_ok": tv["eof_ok"],
        "stop_pos": tv["stop_pos"], "file_size": tv["size"], "crc_fail": tv["crc_fail"],
        "magic": "ArkVFS02" if open(TEMPLATES, "rb").read(8) == b"ArkVFS02" else "other",
    }
    res["interpreted"]["templates_count_match_5438"] = (len(recs) == EXPECTED["templates_records"])

    # size distribution of template payloads
    sizes = {}
    for (_, _, _, bs, _, _, _) in recs:
        sizes[bs] = sizes.get(bs, 0) + 1
    res["measured"]["templates_payload_size_hist_top"] = sorted(sizes.items(), key=lambda kv: -kv[1])[:8]

    # --- dump target records
    def dump_record_by_id2(want_id2):
        for (idx, off, bid, bs, bver, bcrc, payload) in recs:
            if bid == want_id2:
                return {
                    "index": idx, "file_offset": off, "header_id": bid, "size": bs,
                    "ver": bver, "crc32_field": "%08X" % bcrc,
                    "payload_hex_first32": payload[:32].hex(" "),
                    "payload_len": len(payload),
                    "u32_at": {str(o): struct.unpack_from("<I", payload, o)[0] for o in range(0, min(28, len(payload)), 4)},
                    "f32_at": {str(o): struct.unpack_from("<f", payload, o)[0] for o in range(16, min(24, len(payload)), 4)},
                }
        return None

    r4508 = dump_record_by_id2(4508)
    r11963 = dump_record_by_id2(11963)
    res["measured"]["templates_record_id2_4508"] = r4508
    res["measured"]["templates_record_id2_11963"] = r11963

    # byte re-pin: A field @ file 96516 == fd 85 04 00 (from lead); verify from file bytes
    with open(TEMPLATES, "rb") as f:
        f.seek(96516)
        abytes = f.read(4)
    res["measured"]["templates_file_bytes_at_96516"] = abytes.hex(" ")
    res["interpreted"]["a_field_4508_equals_296445"] = (struct.unpack("<I", abytes)[0] == 296445)
    if r4508 is not None:
        payload = None
        for (idx, off, bid, bs, bver, bcrc, pl) in recs:
            if bid == 4508:
                payload = pl
                break
        a_in_payload = struct.unpack_from("<I", payload, 4)[0] if len(payload) >= 8 else None
        res["measured"]["templates_4508_payload_u32_at_4"] = a_in_payload
        res["interpreted"]["a_at_payload_plus4_consistent"] = (a_in_payload == 296445)

    # --- 20002.vfs walk + record 0 + offset-48 column census
    v = read_vfs_permissive(V20002)
    if not v["ok"]:
        res["errors"].append("20002 walk failed: %r" % v.get("error"))
    vrecs = v["records"]
    res["measured"]["v20002_walk"] = {
        "base": v["base"], "record_count": len(vrecs), "eof_ok": v["eof_ok"],
        "stop_pos": v["stop_pos"], "file_size": v["size"], "crc_fail": v["crc_fail"],
    }
    res["interpreted"]["v20002_count_match_1366"] = (len(vrecs) == EXPECTED["v20002_records"])

    # id2 set from templates
    id2set = set(bid for (_, _, bid, _, _, _, _) in recs)

    # record 0 dump + re-pin
    (idx0, off0, bid0, bs0, bv0, bc0, p0) = vrecs[0]
    res["measured"]["v20002_record0"] = {
        "index": idx0, "file_offset": off0, "header_id": bid0, "size": bs0,
        "payload_hex_full": p0.hex(" "),
        "payload_len": len(p0),
        "u32_at_48": struct.unpack_from("<I", p0, 48)[0],
    }
    res["interpreted"]["v20002_rec0_off48_is_11963"] = (struct.unpack_from("<I", p0, 48)[0] == EXPECTED["v20002_rec0_off48"])

    # offset-48 column membership census (1366 records)
    hits = 0
    miss_vals = []
    for (idx, off, bid, bs, bver, bcrc, pl) in vrecs:
        if len(pl) >= 52:
            val = struct.unpack_from("<I", pl, 48)[0]
            if val in id2set:
                hits += 1
            else:
                miss_vals.append(val)
    res["measured"]["v20002_off48_column"] = {
        "records_scanned": len(vrecs),
        "id2_set_size": len(id2set),
        "hits_in_templates_id2": hits,
        "misses": len(miss_vals),
        "miss_values": miss_vals[:20],
    }

    # --- Models.bnt anchors
    names, count, idx_start = parse_bnt2_names(MODELS, {"296445.nif", "551661.nif", "296446.nif", "460563.nif"})
    res["measured"]["models_bnt_index"] = {
        "entry_count": count, "index_start": idx_start, "wanted_name_offsets": names,
    }
    res["interpreted"]["anchor_296445nif_ok"] = (names.get("296445.nif") == EXPECTED["anchor_296445nif_nameoff"])
    res["interpreted"]["nif_551661_present"] = ("551661.nif" in names)
    res["interpreted"]["nif_296446_present"] = ("296446.nif" in names)
    res["interpreted"]["nif_460563_absent_expected"] = ("460563.nif" not in names)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("C1 census written:", OUT)
    print("errors:", res["errors"])
    print("templates records:", res["measured"]["templates_walk"]["record_count"])
    print("20002 records:", res["measured"]["v20002_walk"]["record_count"])
    print("off48 hits/misses:", hits, "/", len(miss_vals))


if __name__ == "__main__":
    main()
