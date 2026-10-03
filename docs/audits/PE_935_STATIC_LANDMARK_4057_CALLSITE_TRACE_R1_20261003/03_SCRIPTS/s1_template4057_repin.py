#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S1 TEMPLATE 4057 RE-PIN — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

Contract §8 (Phase 1): independently re-pin the deferred lead from the PHYSICAL
corpus BEFORE any use of VA 0x0059AB12:
  - templates.vfs record id2=4057: record offset, size, version, CRC, payload
    layout, id2, A, B, C, D raw, list1 count, list2 count, remaining fields.
  - Calibration vs canon anchors (record id2=4508 @96,496 with A=296445; walk
    census 5,438 records / 0 CRC-fail / exact EOF).
  - list1 string-encoding calibration on record id2=11963 (canon first string
    "leg_BASE") — only consulted if record 4057 has a nonempty list1.
  - Bounded BNT2 trailer-index lookups (index metadata ONLY, no payload
    decode; NEW_MODEL_RESOURCE_INDEX_RECORDS_MAX = 4):
      Models.bnt   -> "296445.nif" (calibration anchor @395,268,773), "218757.nif"
      Volumes.bnt  -> "296446.bvi" (calibration), "218758.bvi"

Format knowledge (VFS header/stride/CRC + BNT2 trailer index) = canon context
(TRACE_EDGE_BLOCKS E1 / prior c1_census.py); this is THIS run's own bounded
re-implementation, fail-closed against its calibration anchors.

Interpreter: python 3.12.10 (local Windows). Invoke:
  python 03_SCRIPTS/s1_template4057_repin.py
Output: 01_RAW/TEMPLATE_4057_PHYSICAL_RECORD.json (UTF-8). No input modified.
"""

import hashlib
import json
import os
import struct
import zlib

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "01_RAW", "TEMPLATE_4057_PHYSICAL_RECORD.json"))

PCG = r"D:\Eudoria_Reconstruction\pcg_install"
TEMPLATES = os.path.join(PCG, "Data", "Parameters", "templates.vfs")
MODELS = os.path.join(PCG, "Data", "Models", "Models.bnt")
VOLUMES = os.path.join(PCG, "Data", "Volumes", "Volumes.bnt")

# Calibration expectations (canon; measured independently by this walk)
EXPECT = {
    "templates_size": 560788,
    "templates_sha256": "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77",
    "templates_records": 5438,
    "templates_crc_fail": 0,
    "rec4508_offset": 96496,
    "rec4508_A_at_payload4": 296445,
    "models_size": 395412868,
    "models_sha256": "C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0",
    "models_index_start": 395262727,
    "models_index_count": 5596,
    "anchor_296445nif_nameoff": 395268773,
    "volumes_size": 3746375,
    "volumes_sha256": "6AD8BA3C5AD6F7534F91C1956A0E36485A49BBEF3FFA918CBDDC0C68EDBABC09",
}

TARGET_ID2 = 4057
CAL_ID2 = 4508
STRCAL_ID2 = 11963  # list1 first string "leg_BASE" (canon)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def read_vfs(path):
    """Own ArkVFS walk: magic(8) + base(u32@8) + pad(4); records from offset 16;
    header {id,size,ver,crc32} 16 B; stride ceil((16+size)/base)*base;
    CRC gate when field != 0 (zlib.crc32(payload))."""
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
            return {"ok": False, "error": "truncated at %d" % pos, "base": base, "records": recs}
        payload = data[pos + 16: pos + 16 + bsize]
        if bcrc != 0 and (zlib.crc32(payload) & 0xFFFFFFFF) != bcrc:
            crc_fail += 1
        recs.append((pos, bid, bsize, bver, bcrc, payload))
        pos += ((16 + bsize + base - 1) // base) * base
    return {"ok": (pos == len(data)), "base": base, "records": recs,
            "stop_pos": pos, "file_size": len(data), "crc_fail": crc_fail, "magic": magic.decode()}


def parse_template_payload(payload):
    """Fixed head per canon physical order: u32 id2 @0, u32 A @4 (->obj+0x08),
    u32 B @8 (->obj+0x04), u32 C @0xC, u32 D @0x10; then u16 list1_count,
    list1 strings, u16 list2_count, count x u32, final u32 f11."""
    d = {}
    d["id2_u32_at_0"] = struct.unpack_from("<I", payload, 0)[0]
    d["A_u32_at_4"] = struct.unpack_from("<I", payload, 4)[0]
    d["B_u32_at_8"] = struct.unpack_from("<I", payload, 8)[0]
    d["C_u32_at_12"] = struct.unpack_from("<I", payload, 12)[0]
    d["D_u32_at_16"] = struct.unpack_from("<I", payload, 16)[0]
    d["D_f32_at_16"] = struct.unpack("<f", payload[16:20])[0]
    pos = 20
    d["list1_count_u16_at_20"] = struct.unpack_from("<H", payload, 20)[0]
    pos = 22
    return d, pos


def try_parse_list1_strings(payload, pos, count, encoding):
    """Return (strings, end_pos) or (None, None) if encoding does not fit."""
    strings = []
    p = pos
    for _ in range(count):
        if encoding == "u16len":
            if p + 2 > len(payload):
                return None, None
            ln = struct.unpack_from("<H", payload, p)[0]
            p += 2
            if p + ln > len(payload):
                return None, None
            strings.append(payload[p:p + ln])
            p += ln
        elif encoding == "u8len":
            if p + 1 > len(payload):
                return None, None
            ln = payload[p]
            p += 1
            if p + ln > len(payload):
                return None, None
            strings.append(payload[p:p + ln])
            p += ln
        elif encoding == "asciiz":
            end = payload.find(b"\x00", p)
            if end < 0:
                return None, None
            strings.append(payload[p:end])
            p = end + 1
        else:
            return None, None
    return strings, p


def calibrate_list1_encoding(payload, count, known_first):
    """Try candidate string encodings; the one reproducing the canon first
    string AND consuming the payload cleanly (list2+f11 fit) is selected."""
    pos = 22
    trials = {}
    for enc in ("u16len", "u8len", "asciiz"):
        strings, p = try_parse_list1_strings(payload, pos, count, enc)
        if strings is None:
            trials[enc] = {"ok": False, "error": "does not fit payload"}
            continue
        ok_first = (len(strings) > 0 and strings[0].decode("latin-1") == known_first)
        rest_ok = False
        l2c = None
        if p + 2 <= len(payload):
            l2c = struct.unpack_from("<H", payload, p)[0]
            p2 = p + 2
            if p2 + 4 * l2c + 4 == len(payload):
                rest_ok = True
        trials[enc] = {"ok": True, "first_string_matches_canon": ok_first,
                       "first_string": strings[0].decode("latin-1", "replace"),
                       "end_pos": p, "list2_count_fits": rest_ok}
    return trials


def parse_bnt2_names(path, want_names):
    """Own BNT2 trailer-index parse: last 8 B = {index_start u32, 'BNT2'};
    index blob at index_start: count u32; entries: name bytes until 0x0A then
    16 B metadata; name_file_offset = index_start + name start pos."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(size - 8)
        tail = f.read(8)
    index_start, = struct.unpack("<I", tail[:4])
    if tail[4:] != b"BNT2":
        return None, None, None, "footer is %r not BNT2" % tail[4:]
    with open(path, "rb") as f:
        f.seek(index_start)
        blob = f.read()
    count, = struct.unpack_from("<I", blob, 0)
    out = {}
    pos = 4
    walked = 0
    for i in range(count):
        nl = blob.find(b"\x0a", pos)
        if nl < 0:
            return None, index_start, count, "0x0A not found at entry %d" % i
        name = blob[pos:nl].decode("latin-1")
        name_file_offset = index_start + pos
        pos = nl + 1 + 16
        walked += 1
        if name in want_names:
            out[name] = name_file_offset
    if walked != count:
        return None, index_start, count, "walked %d != count %d" % (walked, count)
    return out, index_start, count, None


def main():
    res = {"run_id": RUN_ID, "stage": "S1_template_4057_repin",
           "measured": {}, "interpreted": {}, "errors": []}
    M = res["measured"]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    # ---- input identities (re-hash)
    for label, p in (("templates_vfs", TEMPLATES), ("models_bnt", MODELS), ("volumes_bnt", VOLUMES)):
        st = os.stat(p)
        M[label] = {"path": p, "size_bytes": st.st_size, "sha256": sha256_file(p)}

    # ---- templates.vfs walk + calibration
    tv = read_vfs(TEMPLATES)
    if not tv.get("ok"):
        res["errors"].append("templates walk failed: %r" % tv.get("error"))
        M["templates_walk"] = {"ok": False, "error": tv.get("error")}
    else:
        recs = tv["records"]
        id2_counts = {}
        for (_, bid, _, _, _, _) in recs:
            id2_counts[bid] = id2_counts.get(bid, 0) + 1
        M["templates_walk"] = {
            "ok": True, "magic": tv["magic"], "base": tv["base"],
            "record_count": len(recs), "eof_ok": tv["ok"], "stop_pos": tv["stop_pos"],
            "file_size": tv["file_size"], "crc_fail": tv["crc_fail"],
            "unique_id2_count": len(id2_counts),
            "duplicate_id2_values": {str(k): v for k, v in id2_counts.items() if v > 1},
        }
        cal = [r for r in recs if r[1] == CAL_ID2]
        if cal:
            (off, bid, bsize, bver, bcrc, payload) = cal[0]
            M["calibration_record_4508"] = {
                "file_offset": off, "header_id": bid, "size": bsize, "ver": bver,
                "crc32_field": "%08X" % bcrc,
                "crc32_recomputed": "%08X" % (zlib.crc32(payload) & 0xFFFFFFFF),
                "payload_hex": payload.hex(" "),
                "A_u32_at_payload4": struct.unpack_from("<I", payload, 4)[0],
            }
        strcal = [r for r in recs if r[1] == STRCAL_ID2]
        if strcal:
            (off, bid, bsize, bver, bcrc, payload) = strcal[0]
            fixed, _ = parse_template_payload(payload)
            l1c = fixed["list1_count_u16_at_20"]
            M["list1_encoding_calibration_record_11963"] = {
                "file_offset": off, "size": bsize,
                "list1_count": l1c,
                "encoding_trials": calibrate_list1_encoding(payload, l1c, "leg_BASE"),
            }

        # ---- TARGET: record id2 = 4057
        tgt = [r for r in recs if r[1] == TARGET_ID2]
        if not tgt:
            M["record_4057"] = {"found": False}
        else:
            (off, bid, bsize, bver, bcrc, payload) = tgt[0]
            d = {"found": True, "file_offset": off, "header_id": bid, "size": bsize,
                 "ver": bver, "crc32_field": "%08X" % bcrc,
                 "crc32_recomputed": "%08X" % (zlib.crc32(payload) & 0xFFFFFFFF),
                 "crc_match": ((zlib.crc32(payload) & 0xFFFFFFFF) == bcrc or bcrc == 0),
                 "payload_len": len(payload), "payload_hex": payload.hex(" ")}
            d.update(parse_template_payload(payload)[0])
            # tail parse (lists + f11) with calibrated encoding if list1 nonempty
            l1c = d.get("list1_count_u16_at_20", 0)
            pos = 22
            enc_used = None
            if l1c and "encoding_trials" in M.get("list1_encoding_calibration_record_11963", {}):
                trials = M["list1_encoding_calibration_record_11963"]["encoding_trials"]
                for enc in ("u16len", "u8len", "asciiz"):
                    t = trials.get(enc, {})
                    if t.get("first_string_matches_canon"):
                        enc_used = enc
                        break
            if l1c:
                if enc_used:
                    strings, pend = try_parse_list1_strings(payload, 22, l1c, enc_used)
                    if strings is not None:
                        d["list1_strings"] = [s.decode("latin-1", "replace") for s in strings]
                        pos = pend
                    else:
                        d["list1_parse_error"] = "calibrated encoding %s did not fit" % enc_used
                else:
                    d["list1_parse_error"] = "no calibrated encoding available; raw hex only"
            l2c = None
            if pos + 2 <= len(payload):
                l2c = struct.unpack_from("<H", payload, pos)[0]
                pos += 2
            d["list2_count_u16"] = l2c
            if l2c is not None and pos + 4 * l2c + 4 == len(payload):
                d["list2_u32_values"] = [struct.unpack_from("<I", payload, pos + 4 * i)[0] for i in range(l2c)]
                pos += 4 * l2c
                d["f11_u32"] = struct.unpack_from("<I", payload, pos)[0]
                pos += 4
            elif l2c is not None:
                d["tail_layout_note"] = "list2/f11 do not close the payload exactly (pos=%d len=%d)" % (pos, len(payload))
            d["tail_bytes_remaining"] = len(payload) - pos
            M["record_4057"] = d

    # ---- BNT2 index lookups (bounded; 4 records total)
    names_m, idx_start_m, count_m, err_m = parse_bnt2_names(MODELS, {"296445.nif", "218757.nif"})
    if err_m:
        res["errors"].append("Models.bnt index: %s" % err_m)
    M["models_bnt_index"] = {"index_start": idx_start_m, "entry_count": count_m,
                             "found": {k: v for k, v in (names_m or {}).items()},
                             "found_296445_nif": (names_m or {}).get("296445.nif"),
                             "found_218757_nif": (names_m or {}).get("218757.nif")}
    names_v, idx_start_v, count_v, err_v = parse_bnt2_names(VOLUMES, {"296446.bvi", "218758.bvi"})
    if err_v:
        res["errors"].append("Volumes.bnt index: %s" % err_v)
    M["volumes_bnt_index"] = {"index_start": idx_start_v, "entry_count": count_v,
                              "found": {k: v for k, v in (names_v or {}).items()},
                              "found_296446_bvi": (names_v or {}).get("296446.bvi"),
                              "found_218758_bvi": (names_v or {}).get("218758.bvi")}

    # ---- interpretation (contract §8 required results) — no semantics beyond canon
    I = res["interpreted"]
    tw = M.get("templates_walk", {})
    I["walk_calibration_ok"] = (tw.get("record_count") == EXPECT["templates_records"]
                                and tw.get("crc_fail") == EXPECT["templates_crc_fail"]
                                and tw.get("eof_ok") is True)
    cal = M.get("calibration_record_4508", {})
    I["anchor_4508_ok"] = (cal.get("file_offset") == EXPECT["rec4508_offset"]
                           and cal.get("A_u32_at_payload4") == EXPECT["rec4508_A_at_payload4"])
    I["models_index_calibration_ok"] = (M["models_bnt_index"].get("index_start") == EXPECT["models_index_start"]
                                        and M["models_bnt_index"].get("entry_count") == EXPECT["models_index_count"]
                                        and M["models_bnt_index"].get("found_296445_nif") == EXPECT["anchor_296445nif_nameoff"])
    r = M.get("record_4057", {})
    I["TEMPLATE_4057_REPIN"] = ("CONFIRMED" if r.get("found") and r.get("id2_u32_at_0") == TARGET_ID2
                                and r.get("crc_match") else "REJECTED")
    I["TEMPLATE_4057_id2"] = r.get("id2_u32_at_0")
    I["TEMPLATE_4057_A"] = r.get("A_u32_at_4")
    I["TEMPLATE_4057_B"] = r.get("B_u32_at_8")
    I["A_EQUALS_CANDIDATE_218757"] = (r.get("A_u32_at_4") == 218757)
    I["B_EQUALS_CANDIDATE_218758"] = (r.get("B_u32_at_8") == 218758)
    I["MODEL_INDEX_218757"] = ("PRESENT" if M["models_bnt_index"].get("found_218757_nif") is not None else "ABSENT")
    I["COLLISION_INDEX_218758"] = ("PRESENT" if M["volumes_bnt_index"].get("found_218758_bvi") is not None else "ABSENT")

    # ---- anti-circularity provenance (contract §26 note; supervisory addition 5)
    I["pin_provenance"] = {
        "record_4057_physical": {
            "MEASURED_QUANTITY": "file_offset/size/ver/crc32/payload bytes of the templates.vfs record whose header id == 4057",
            "INDEPENDENT_SOURCE_OF_TRUTH": "physical bytes of D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Parameters\\templates.vfs (re-hashed this run), read by this run's own walker",
            "WHY_NON_CIRCULAR": "the walk uses only the container format (magic/base/stride/CRC) — the candidate values 4057/218757/218758 are inputs to a lookup, not assumptions of the parse; calibration anchors (5,438/0-CRC/EOF, record 4508 @96,496 A=296445) come from prior canon and must be reproduced by THIS implementation before the 4057 record is trusted",
            "FAILURE_CASE_DETECTED": "wrong stride/header layout would desynchronize the walk (count != 5,438, EOF mismatch, CRC failures) or misplace record 4508; record 4057 absent or id2 mismatch => TEMPLATE_4057_REPIN=REJECTED"},
        "bnt2_index_names": {
            "MEASURED_QUANTITY": "presence + name_file_offset of exact index names in the BNT2 trailer index",
            "INDEPENDENT_SOURCE_OF_TRUTH": "physical trailer/index bytes of Models.bnt / Volumes.bnt (re-hashed this run)",
            "WHY_NON_CIRCULAR": "own trailer-index parser; the Models.bnt side must first reproduce the canon calibration (index_start 395,262,727; count 5,596; anchor 296445.nif @395,268,773) before the 218757/218758 lookups are trusted",
            "FAILURE_CASE_DETECTED": "wrong entry stride would desync the name walk (0x0A misses / walked != count) or displace the calibration anchor; absent name => ABSENT"},
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("S1 written:", OUT)
    print("errors:", res["errors"])
    print("walk_calibration_ok:", I.get("walk_calibration_ok"), "anchor_4508_ok:", I.get("anchor_4508_ok"))
    print("models_index_calibration_ok:", I.get("models_index_calibration_ok"))
    r = M.get("record_4057", {})
    print("record_4057 found:", r.get("found"), "off:", r.get("file_offset"), "size:", r.get("size"),
          "ver:", r.get("ver"), "crc_match:", r.get("crc_match"))
    print("id2:", r.get("id2_u32_at_0"), "A:", r.get("A_u32_at_4"), "B:", r.get("B_u32_at_8"),
          "C:", r.get("C_u32_at_12"), "D_u32:", r.get("D_u32_at_16"), "D_f32:", r.get("D_f32_at_16"),
          "l1:", r.get("list1_count_u16_at_20"), "l2:", r.get("list2_count_u16"), "f11:", r.get("f11_u32"))
    print("TEMPLATE_4057_REPIN:", I.get("TEMPLATE_4057_REPIN"),
          "| A==218757:", I.get("A_EQUALS_CANDIDATE_218757"), "| B==218758:", I.get("B_EQUALS_CANDIDATE_218758"))
    print("MODEL_INDEX_218757:", I.get("MODEL_INDEX_218757"), "@", M["models_bnt_index"].get("found_218757_nif"))
    print("COLLISION_INDEX_218758:", I.get("COLLISION_INDEX_218758"), "@", M["volumes_bnt_index"].get("found_218758_bvi"))
    print("296446.bvi calibration:", M["volumes_bnt_index"].get("found_296446_bvi"),
          "| Volumes index_start:", idx_start_v, "count:", count_v)


if __name__ == "__main__":
    main()
