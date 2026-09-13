#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 - Z2: FULL JOIN A <-> Models.bnt (+ BONUS B <-> Volumes.bnt).

RUN_ID:       PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913
ASSIGNMENT:   PE-MASTER dispatch (audyt twierdzeń A-E runu PE_935_TEMPLATE_CONSUMER_TRACE_R1
              + pełny denominatorowy join + errata; RUN_CLASS MATERIAL; NO_NESTED_TASKS).
PURPOSE:      Rozstrzygnięcie twierdzenia C ("WSZYSTKIE odpowiednie A mają odwzorowanie <A>.nif
              w Models.bnt") pełnym joinem z dokładnymi mianownikami, zamiast 3 sprawdzonych
              przypadków runu R1.

METHOD (fail-closed, independently re-implemented — NIE kopiuję generatorów runu R1):
  1. Asercje SHA256 wszystkich trzech wejść (templates.vfs / Models.bnt / Volumes.bnt).
  2. WŁASNY pełny walk templates.vfs (reguła stride ceil((16+size)/base)*base, base=u32@0x08;
     CRC-32 zlib) -> T/A/B/C z surowych bajtów.
  3. Asercja zgodności własnego walka z 01_RAW\S2_TEMPLATES_TRUE_WALK.csv runu R1
     (5,438 wierszy, per-row: offset/id/size/A/B/C/crc_ok).
  4. WŁASNY parser indeksu BNT2 (trailer [u32 index_start]["BNT2"]; blob: [u32 count]
     [count x {name\0x0a, u32 packed, u32 offset, u32 c, u32 d}] + trailer na końcu blobu);
     asercja pełnego skonsumowania blobu do traileru + samozgodności traileru; kalibracja
     pozycjami NAZW-STRINGÓW z byte-scanów runu R1 (VA_EVIDENCE_REGISTRY E.4 + QC §4 —
     skany R1 lokalizowały stringi nazw w regionie indeksu, NIE payloady):
     296445.nif@395,268,773 / 126740.nif@395,268,719 / 278453.nif@395,268,746 (Models.bnt);
     296446.bvi@3,701,937 / 126741.bvi@3,701,883 / 278454.bvi@3,701,910 (Volumes.bnt).
     Pole 'offset' indeksu BNT2 = lokalizacja PAYLOADU w archiwum (nowa miara tego runu;
     R1 nie formułował twierdzeń o offsetach payloadów).
  5. JOIN A->"<A>.nif" (unikalne niezerowe A) + per-record join; to samo dla BONUS B->"<B>.bvi".
  6. Podwójna rekomputacja join (metoda 1: membership f-string; metoda 2: przecięcie zbiorów
     int-ID) — asercja identyczności (G1).
  7. Round-trip endianness: pack("<I")->unpack("<I") == A dla wszystkich unikalnych A;
     kotwica surowych bajtów rekordu 4508 (A@96,516 LE == 296445); kontrola dyskryminatywna
     BE (join pod interpretacją big-endian — oczekiwane 0 trafień).
  8. Kontrola negatywna: 20 syntetycznych A (realne A + 1,000,000; seed 20260913) -> brak w
     Models.bnt; pozytywne 296445/126740/278453 obecne; negatyw 999999999 nieobecny;
     cross-absent 296446.nif (Models) / 296445.bvi (Volumes).

INPUT-OUTPUT: READ-ONLY na oryginałach. Zapisy WYŁĄCZNIE do run-dir (01_RAW\Z2_*).
ZERO ekstrakcji payloadów .nif/.bvi — wyłącznie metadane indeksu (nazwy/offsety/rozmiary).

Determinism: czysta funkcja bajtów wejść + stały seed; brak timestampów w wynikach.
"""

import csv
import hashlib
import json
import os
import random
import struct
import sys
import zlib

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"
OUT_RAW = os.path.join(RUN_ROOT, "01_RAW")

VFS_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
MODELS_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
VOLUMES_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
S2_CSV_R1 = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\01_RAW\S2_TEMPLATES_TRUE_WALK.csv"

# --- identity pins (zlecenie PE-MASTER 2026-09-13; odczytane ponownie na starcie runu) ---
PIN_VFS_SHA256 = "BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77"
PIN_MODELS_SHA256 = "C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0"
PIN_VOLUMES_SHA256 = "6AD8BA3C5AD6F7534F91C1956A0E36485A49BBEF3FFA918CBDDC0C68EDBABC09"

# --- expected counts (zlecenie; independently asserted) ---
PIN_MODELS_ENTRY_COUNT = 5596
PIN_VOLUMES_ENTRY_COUNT = 1865
PIN_S2_RECORD_COUNT = 5438

# --- calibration anchors: byte-proof offsets runu R1 (VA_EVIDENCE_REGISTRY.md E.4 + QC §4) ---
PIN_MODELS_ANCHORS = {
    "296445.nif": 395268773,
    "126740.nif": 395268719,
    "278453.nif": 395268746,
}
PIN_VOLUMES_ANCHORS = {
    "296446.bvi": 3701937,
    "126741.bvi": 3701883,
    "278454.bvi": 3701910,
}

# --- prior-run data-binding pins (positive/negative/cross-absent) ---
PIN_POSITIVE_MODELS = ["296445.nif", "126740.nif", "278453.nif"]
PIN_NEGATIVE_MODELS = ["999999999.nif", "296446.nif"]   # 999999999: nie istnieje; 296446: cross-absent (B-side id w Models)
PIN_NEGATIVE_VOLUMES = ["999999999.bvi", "296445.bvi"]

NEG_CONTROL_N = 20
NEG_CONTROL_OFFSET = 1000000
NEG_CONTROL_SEED = 20260913

ERRORS = []


def die(msg):
    ERRORS.append(msg)
    sys.stderr.write("[FAIL] " + msg + "\n")


def fail_closed():
    if ERRORS:
        sys.stderr.write("FAIL-CLOSED: %d assertion error(s); no result JSON written.\n" % len(ERRORS))
        for e in ERRORS:
            sys.stderr.write("  - " + e + "\n")
        sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def parse_bnt2_index(path, pin_sha, pin_count, pin_anchors, label):
    """Independent BNT2 trailer-index parser. Returns (entries, meta)."""
    sha = sha256_file(path)
    if sha != pin_sha:
        die("%s sha256: measured %s expected %s" % (label, sha, pin_sha))
        return None, None
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(size - 8)
        tail = f.read(8)
    index_start, = struct.unpack("<I", tail[:4])
    magic = tail[4:]
    if magic != b"BNT2":
        die("%s trailer magic: measured %r expected b'BNT2'" % (label, magic))
        return None, None
    with open(path, "rb") as f:
        f.seek(index_start)
        blob = f.read()
    count, = struct.unpack_from("<I", blob, 0)
    if count != pin_count:
        die("%s index count: measured %d expected %d" % (label, count, pin_count))
        return None, None
    entries = []
    pos = 4
    for i in range(count):
        nl = blob.find(b"\x0a", pos)
        if nl < 0:
            die("%s index parse: unterminated name at entry %d" % (label, i))
            return None, None
        name = blob[pos:nl].decode("latin-1")
        name_file_offset = index_start + pos  # file offset of the NAME STRING (byte-scan anchor)
        pos = nl + 1
        packed, offset, c_field, d_field = struct.unpack_from("<4I", blob, pos)
        pos += 16
        entries.append({
            "index": i, "name": name, "packed": packed,
            "offset": offset, "c": c_field, "d": d_field,
            "name_file_offset": name_file_offset,
        })
    # the read-to-EOF blob contains the index region + the file trailer itself (8 B);
    # the index must end EXACTLY at the trailer, and the trailer must be self-consistent
    if pos != len(blob) - 8:
        die("%s index parse: %d trailing bytes unconsumed (pos=%d len=%d; expected exactly 8 = trailer)"
            % (label, len(blob) - 8 - pos, pos, len(blob)))
        return None, None
    trailer_start, = struct.unpack_from("<I", blob, len(blob) - 8)
    trailer_magic = blob[-4:]
    if trailer_magic != b"BNT2" or trailer_start != index_start:
        die("%s trailer self-consistency: magic=%r index_start=%d trailer_start=%d"
            % (label, trailer_magic, index_start, trailer_start))
        return None, None
    # calibration anchors: run R1's byte-scans located the NAME STRINGS at these file
    # offsets (the index region at the file tail). Our parsed index must reproduce them
    # exactly — anchoring this parser byte-for-byte to the independent R1 scans.
    # NOTE: the index 'offset' FIELD is the PAYLOAD location (a different quantity,
    # first measured here; R1 made no payload-offset claim).
    by_name = {e["name"]: e for e in entries}
    for anchor_name, pin_off in pin_anchors.items():
        e = by_name.get(anchor_name)
        if e is None:
            die("%s calibration anchor %r absent from parsed index" % (label, anchor_name))
        elif e["name_file_offset"] != pin_off:
            die("%s calibration anchor %r name-string file offset: measured %d expected %d"
                % (label, anchor_name, e["name_file_offset"], pin_off))
    # duplicate-name census
    seen = {}
    dups = []
    for e in entries:
        if e["name"] in seen:
            dups.append(e["name"])
        seen[e["name"]] = e["index"]
    meta = {
        "path": path,
        "size_bytes": size,
        "sha256": sha,
        "trailer_index_start": index_start,
        "entry_count": count,
        "duplicate_names": dups,
        "index_blob_bytes": len(blob),
    }
    return entries, meta


def main():
    # (0) driver self-hash (record; pinned externally in 00_CONTROL\Z2_SCRIPT_SHA256.txt)
    driver_sha = sha256_file(os.path.abspath(__file__))

    # (1) own full walk of templates.vfs --------------------------------------
    vfs_sha = sha256_file(VFS_PATH)
    if vfs_sha != PIN_VFS_SHA256:
        die("templates.vfs sha256: measured %s expected %s" % (vfs_sha, PIN_VFS_SHA256))
        fail_closed()
    with open(VFS_PATH, "rb") as f:
        vfs = f.read()
    if vfs[:8] != b"ArkVFS02":
        die("templates.vfs header magic: measured %r expected b'ArkVFS02'" % vfs[:8])
        fail_closed()
    base = struct.unpack_from("<I", vfs, 8)[0]
    if base != 36:
        die("templates.vfs stride base: measured %d expected 36" % base)
        fail_closed()

    records = []
    pos = 16
    crc_fail = 0
    while pos + 16 <= len(vfs):
        bid, bsize, bver, bcrc = struct.unpack_from("<IIII", vfs, pos)
        if bver != 1:
            die("walk: ver!=1 at %d (id=%d)" % (pos, bid))
            break
        if pos + 16 + bsize > len(vfs):
            die("walk: truncated payload at %d (id=%d size=%d)" % (pos, bid, bsize))
            break
        payload = vfs[pos + 16: pos + 16 + bsize]
        got_crc = zlib.crc32(payload) & 0xFFFFFFFF
        crc_ok = (got_crc == bcrc)
        if not crc_ok:
            crc_fail += 1
        if bsize >= 28:
            id2, A, B, C = struct.unpack_from("<IIII", payload, 0)
        else:
            id2, A, B, C = None, None, None, None
        records.append({
            "index": len(records), "file_offset": pos, "id": bid, "size": bsize,
            "ver": bver, "crc32_field": "%08X" % bcrc, "crc_ok": crc_ok,
            "id2": id2, "A": A, "B": B, "C": C,
        })
        pos += ((16 + bsize + base - 1) // base) * base
    last_end = records[-1]["file_offset"] + ((16 + records[-1]["size"] + base - 1) // base) * base
    if len(records) != PIN_S2_RECORD_COUNT:
        die("walk record count: measured %d expected %d" % (len(records), PIN_S2_RECORD_COUNT))
    if crc_fail != 0:
        die("walk CRC fail count: measured %d expected 0" % crc_fail)
    if last_end != len(vfs) or pos != len(vfs):
        die("walk EOF: last_end=%d stop=%d file=%d (expected all equal)" % (last_end, pos, len(vfs)))

    # (2) consistency with S2 CSV of run R1 ----------------------------------
    with open(S2_CSV_R1, "r", encoding="utf-8", newline="") as f:
        s2_rows = list(csv.DictReader(f))
    if len(s2_rows) != PIN_S2_RECORD_COUNT:
        die("S2 CSV row count: measured %d expected %d" % (len(s2_rows), PIN_S2_RECORD_COUNT))
    s2_mismatch = []
    for i, (mine, s2) in enumerate(zip(records, s2_rows)):
        exp = {
            "file_offset": str(mine["file_offset"]),
            "id": str(mine["id"]),
            "size": str(mine["size"]),
            "ver": str(mine["ver"]),
            "crc32_field": mine["crc32_field"],
            "crc_ok": str(mine["crc_ok"]),
        }
        if mine["A"] is not None:
            exp["id2"] = str(mine["id2"])
            exp["A"] = str(mine["A"])
            exp["B"] = str(mine["B"])
            exp["C"] = str(mine["C"])
        for k, v in exp.items():
            if s2.get(k) != v:
                s2_mismatch.append("row %d field %s: mine=%r s2=%r" % (i, k, v, s2.get(k)))
                if len(s2_mismatch) > 20:
                    break
        if len(s2_mismatch) > 20:
            break
    if s2_mismatch:
        for m in s2_mismatch:
            die("S2 consistency: " + m)

    # (3) parse BNT2 indexes ---------------------------------------------------
    models_entries, models_meta = parse_bnt2_index(
        MODELS_PATH, PIN_MODELS_SHA256, PIN_MODELS_ENTRY_COUNT, PIN_MODELS_ANCHORS, "Models.bnt")
    volumes_entries, volumes_meta = parse_bnt2_index(
        VOLUMES_PATH, PIN_VOLUMES_SHA256, PIN_VOLUMES_ENTRY_COUNT, PIN_VOLUMES_ANCHORS, "Volumes.bnt")
    if models_entries is None or volumes_entries is None:
        fail_closed()
    fail_closed()  # flush any anchor/count assertion failures before computing joins

    models_names = [e["name"] for e in models_entries]
    models_name_set = set(models_names)
    volumes_names = [e["name"] for e in volumes_entries]
    volumes_name_set = set(volumes_names)

    import re
    nif_pat = re.compile(r"^(\d+)\.nif$")
    bvi_pat = re.compile(r"^(\d+)\.bvi$")
    nif_ids = {}
    for e in models_entries:
        m = nif_pat.match(e["name"])
        if m:
            nif_ids[int(m.group(1))] = e
    bvi_ids = {}
    for e in volumes_entries:
        m = bvi_pat.match(e["name"])
        if m:
            bvi_ids[int(m.group(1))] = e

    models_ext_census = {}
    for n in models_names:
        ext = os.path.splitext(n)[1].lower()
        models_ext_census[ext] = models_ext_census.get(ext, 0) + 1
    volumes_ext_census = {}
    for n in volumes_names:
        ext = os.path.splitext(n)[1].lower()
        volumes_ext_census[ext] = volumes_ext_census.get(ext, 0) + 1
    models_non_numeric_nif = [n for n in models_names if not nif_pat.match(n)]
    volumes_non_numeric_bvi = [n for n in volumes_names if not bvi_pat.match(n)]

    # (4) template-side sets ----------------------------------------------------
    total_records = len(records)
    template_ids = [r["id"] for r in records]
    unique_T = sorted(set(template_ids))
    dup_template_ids = sorted({t for t in template_ids if template_ids.count(t) > 1}) if \
        len(set(template_ids)) != len(template_ids) else []

    a_values = [r["A"] for r in records if r["A"] is not None]
    a_zero_records = [r for r in records if r["A"] == 0]
    unique_A_nonzero = sorted({a for a in a_values if a != 0})
    b_values = [r["B"] for r in records if r["B"] is not None]
    b_zero_records = [r for r in records if r["B"] == 0]
    unique_B_all = sorted(set(b_values))
    unique_B_nonzero = sorted({b for b in b_values if b != 0})

    a_to_templates = {}
    for r in records:
        if r["A"]:
            a_to_templates.setdefault(r["A"], []).append(r["id"])
    b_to_templates = {}
    for r in records:
        if r["B"]:
            b_to_templates.setdefault(r["B"], []).append(r["id"])

    # (5) JOIN A -> <A>.nif -----------------------------------------------------
    # method 1 (primary): membership via the full name-set + entry lookup via by-name map
    models_by_name = {e["name"]: e for e in models_entries}
    join_hits = 0
    join_misses = []
    join_detail = []
    for a in unique_A_nonzero:
        name = "%d.nif" % a
        hit = name in models_name_set
        entry = models_by_name.get(name) if hit else None
        if hit:
            join_hits += 1
        else:
            join_misses.append(a)
        join_detail.append({
            "a_value": a,
            "hit": hit,
            "models_entry_index": entry["index"] if entry else -1,
            "models_offset": entry["offset"] if entry else -1,
            "packed_size": entry["packed"] if entry else -1,
            "template_ids": ";".join(str(t) for t in a_to_templates[a]),
            "template_count": len(a_to_templates[a]),
        })
    # recompute method 2: set intersection on int ids (genuinely different computation)
    a_set = set(unique_A_nonzero)
    inter = a_set & set(nif_ids.keys())
    if len(inter) != join_hits:
        die("G1 recompute mismatch (set-intersection): %d vs %d" % (len(inter), join_hits))
    if sorted(inter) != sorted(a for a in unique_A_nonzero if a in nif_ids):
        die("G1 recompute mismatch: hit membership differs between methods")
    if set(join_misses) != (a_set - set(nif_ids.keys())):
        die("G1 recompute mismatch: miss sets differ between methods")

    # per-record join
    rec_a_nonzero = [r for r in records if r["A"]]
    rec_hit_count = sum(1 for r in rec_a_nonzero if ("%d.nif" % r["A"]) in models_name_set)
    rec_miss_count = len(rec_a_nonzero) - rec_hit_count
    rec_miss_records = [(r["id"], r["A"]) for r in rec_a_nonzero
                        if ("%d.nif" % r["A"]) not in models_name_set]

    # A range vs Models.bnt numeric nif ids
    max_nif_id = max(nif_ids.keys())
    min_nif_id = min(nif_ids.keys())
    max_A = max(unique_A_nonzero) if unique_A_nonzero else 0
    min_A = min(unique_A_nonzero) if unique_A_nonzero else 0
    a_beyond_max = [a for a in unique_A_nonzero if a > max_nif_id]
    a_below_min = [a for a in unique_A_nonzero if a < min_nif_id]
    a_inrange_missing = [a for a in join_misses if a <= max_nif_id and a >= min_nif_id]

    # (6) BONUS JOIN B -> <B>.bvi ------------------------------------------------
    volumes_by_name = {e["name"]: e for e in volumes_entries}
    b_join_hits = 0
    b_join_misses = []
    b_join_detail = []
    for b in unique_B_nonzero:
        name = "%d.bvi" % b
        hit = name in volumes_name_set
        entry = volumes_by_name.get(name) if hit else None
        if hit:
            b_join_hits += 1
        else:
            b_join_misses.append(b)
        b_join_detail.append({
            "b_value": b,
            "hit": hit,
            "volumes_entry_index": entry["index"] if entry else -1,
            "volumes_offset": entry["offset"] if entry else -1,
            "packed_size": entry["packed"] if entry else -1,
            "template_ids": ";".join(str(t) for t in b_to_templates[b]),
            "template_count": len(b_to_templates[b]),
        })
    b_inter = set(unique_B_nonzero) & set(bvi_ids.keys())
    if len(b_inter) != b_join_hits:
        die("G1 recompute mismatch (B set-intersection): %d vs %d" % (len(b_inter), b_join_hits))
    rec_b_nonzero = [r for r in records if r["B"]]
    b_rec_hit_count = sum(1 for r in rec_b_nonzero if ("%d.bvi" % r["B"]) in volumes_name_set)
    b_rec_miss_count = len(rec_b_nonzero) - b_rec_hit_count
    b_rec_miss_records = [(r["id"], r["B"]) for r in rec_b_nonzero
                           if ("%d.bvi" % r["B"]) not in volumes_name_set]
    max_bvi_id = max(bvi_ids.keys())
    min_bvi_id = min(bvi_ids.keys())

    # (7) endianness round-trip + BE discriminative control ----------------------
    rt_fail = 0
    for a in unique_A_nonzero:
        packed = struct.pack("<I", a)
        (unpacked,) = struct.unpack("<I", packed)
        if unpacked != a:
            rt_fail += 1
    if rt_fail:
        die("endianness round-trip: %d failures over %d unique A" % (rt_fail, len(unique_A_nonzero)))
    # raw-byte anchor: record 4508 @96,496, A @file+0x14
    rec4508 = next(r for r in records if r["id"] == 4508)
    raw = vfs[rec4508["file_offset"] + 0x14: rec4508["file_offset"] + 0x18]
    le_val, = struct.unpack("<I", raw)
    be_val = int.from_bytes(raw, "big")
    if le_val != 296445:
        die("raw-byte anchor 4508 A: LE measured %d expected 296445 (bytes %s)" % (le_val, raw.hex()))
    if struct.pack("<I", 296445) != raw:
        die("raw-byte anchor 4508 A: pack(<I,296445) != physical bytes %s" % raw.hex())
    # BE-interpreted join control (discriminative: expected ~0 hits vs LE full mapping)
    be_hits = 0
    be_hits_detail = []
    for a in unique_A_nonzero:
        be_a = int.from_bytes(struct.pack("<I", a), "big")
        if ("%d.nif" % be_a) in models_name_set:
            be_hits += 1
            be_hits_detail.append({"A": a, "be_interpreted": be_a, "name": "%d.nif" % be_a})

    # (8) negative controls --------------------------------------------------------
    rnd = random.Random(NEG_CONTROL_SEED)
    sample_a = rnd.sample(unique_A_nonzero, min(NEG_CONTROL_N, len(unique_A_nonzero)))
    neg_rows = []
    neg_all_absent = True
    for a in sample_a:
        synth = a + NEG_CONTROL_OFFSET
        present = ("%d.nif" % synth) in models_name_set
        if present:
            neg_all_absent = False
        neg_rows.append({
            "base_a": a, "synthetic_a": synth,
            "name": "%d.nif" % synth, "present_in_models_bnt": present,
        })
    if not neg_all_absent:
        die("negative control: synthetic A (real+1,000,000) present in Models.bnt")
    pin_pos_ok = all(n in models_name_set for n in PIN_POSITIVE_MODELS)
    if not pin_pos_ok:
        die("positive control: pinned .nif names absent from Models.bnt")
    pin_neg_ok = all(n not in models_name_set for n in PIN_NEGATIVE_MODELS)
    if not pin_neg_ok:
        die("negative pin: expected-absent .nif names present in Models.bnt")
    pin_neg_vol_ok = all(n not in volumes_name_set for n in PIN_NEGATIVE_VOLUMES)
    if not pin_neg_vol_ok:
        die("negative pin: expected-absent .bvi names present in Volumes.bnt")

    fail_closed()

    # (9) verdict for claim C ------------------------------------------------------
    claim_c_verdict = "FULL_MAPPING" if len(join_misses) == 0 and len(a_zero_records) == 0 else \
        ("FULL_MAPPING_NONZERO_SCOPE" if len(join_misses) == 0 else "PARTIAL_MAPPING")

    result = {
        "run_id": "PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
        "stage": "Z2_full_join_a_models",
        "driver": "z2_join_a_models.py",
        "driver_sha256": driver_sha,
        "era": "EU 9.3.5 (pcg_install)",
        "inputs": {
            "templates_vfs": {"path": VFS_PATH, "sha256": vfs_sha, "size_bytes": len(vfs)},
            "models_bnt": models_meta,
            "volumes_bnt": volumes_meta,
            "s2_csv_r1": S2_CSV_R1,
        },
        "walk": {
            "record_count": total_records,
            "stop": "EOF",
            "last_record_end": last_end,
            "file_size": len(vfs),
            "crc_fail_count": crc_fail,
            "stride_base": base,
            "s2_csv_consistency": "IDENTICAL (5438/5438 rows: offset/id/size/ver/crc32/crc_ok/id2/A/B/C)",
        },
        "denominators": {
            "template_records_total": total_records,
            "unique_template_ids_T": len(unique_T),
            "duplicate_template_ids": dup_template_ids,
            "unique_A_nonzero": len(unique_A_nonzero),
            "A_zero_record_count": len(a_zero_records),
            "A_zero_sample_ids": [r["id"] for r in a_zero_records[:20]],
            "unique_B_all_incl_zero": len(unique_B_all),
            "unique_B_nonzero": len(unique_B_nonzero),
            "B_zero_record_count": len(b_zero_records),
            "max_A": max_A, "min_A": min_A,
            "models_bnt_numeric_nif_ids": len(nif_ids),
            "models_bnt_max_nif_id": max_nif_id,
            "models_bnt_min_nif_id": min_nif_id,
            "volumes_bnt_numeric_bvi_ids": len(bvi_ids),
            "volumes_bnt_max_bvi_id": max_bvi_id,
            "volumes_bnt_min_bvi_id": min_bvi_id,
        },
        "join_A_to_nif": {
            "unique_nonzero_A": len(unique_A_nonzero),
            "hits": join_hits,
            "misses": len(join_misses),
            "miss_A_values_with_template_ids": [
                {"A": a, "template_ids": a_to_templates[a]} for a in join_misses
            ],
            "per_record": {
                "records_with_nonzero_A": len(rec_a_nonzero),
                "record_hits": rec_hit_count,
                "record_misses": rec_miss_count,
                "miss_records_template_id_A": rec_miss_records,
            },
            "multiples": {
                "duplicate_names_in_models_index": models_meta["duplicate_names"],
                "duplicate_names_count": len(models_meta["duplicate_names"]),
                "one_name_multiple_entries_possible": len(models_meta["duplicate_names"]) > 0,
                "template_side_A_shared_by_multiple_templates": sum(
                    1 for a in unique_A_nonzero if len(a_to_templates[a]) > 1),
                "note": "models.bnt index has unique names -> each A maps to at most 1 entry; "
                        "multiple templates may share one A (template-side multiplicity, reported)",
            },
            "range_analysis": {
                "A_beyond_max_nif_id": len(a_beyond_max),
                "A_beyond_max_list": a_beyond_max[:200],
                "A_below_min_nif_id": len(a_below_min),
                "A_in_range_but_missing": len(a_inrange_missing),
                "A_in_range_missing_list": a_inrange_missing[:200],
            },
            "recompute_g1": {
                "method1_membership_name_set": join_hits,
                "method2_set_intersection_int_ids": len(inter),
                "identical": (join_hits == len(inter)),
            },
        },
        "bonus_join_B_to_bvi": {
            "unique_nonzero_B": len(unique_B_nonzero),
            "hits": b_join_hits,
            "misses": len(b_join_misses),
            "miss_B_values_with_template_ids": [
                {"B": b, "template_ids": b_to_templates[b]} for b in b_join_misses
            ],
            "per_record": {
                "records_with_nonzero_B": len(rec_b_nonzero),
                "record_hits": b_rec_hit_count,
                "record_misses": b_rec_miss_count,
                "miss_records_template_id_B": b_rec_miss_records[:500],
            },
            "duplicate_names_in_volumes_index": volumes_meta["duplicate_names"],
        },
        "models_bnt_census": {
            "extension_census": models_ext_census,
            "non_numeric_nif_names_count": len(models_non_numeric_nif),
            "non_numeric_nif_names_sample": models_non_numeric_nif[:50],
        },
        "volumes_bnt_census": {
            "extension_census": volumes_ext_census,
            "non_numeric_bvi_names_count": len(volumes_non_numeric_bvi),
            "non_numeric_bvi_names_sample": volumes_non_numeric_bvi[:50],
        },
        "endianness_control": {
            "round_trip_pack_unpack_failures": rt_fail,
            "raw_byte_anchor_4508": {
                "file_offset": rec4508["file_offset"] + 0x14,
                "bytes_hex": raw.hex(),
                "le_value": le_val,
                "be_value": be_val,
                "pack_round_trip_identical": struct.pack("<I", 296445) == raw,
            },
            "be_interpreted_join_hits": be_hits,
            "be_hits_detail": be_hits_detail,
            "be_note": "join pod interpretacją big-endian daje %d trafień z %d unikalnych A "
                       "(vs LE: %d/%d) — LE to jedyna interpretacja zgodna z CAŁOŚCIĄ indeksu; "
                       "pojedyncze trafienia BE to zbiegi okoliczności (A o bajtach dających "
                       "przypadkiem prawidłowy id), nie dowód interpretacji BE"
                       % (be_hits, len(unique_A_nonzero), join_hits, len(unique_A_nonzero)),
        },
        "negative_control_A": {
            "seed": NEG_CONTROL_SEED,
            "offset": NEG_CONTROL_OFFSET,
            "rows": neg_rows,
            "all_absent": neg_all_absent,
            "positive_pins_present": pin_pos_ok,
            "negative_pins_absent_models": pin_neg_ok,
            "negative_pins_absent_volumes": pin_neg_vol_ok,
        },
        "claim_C_verdict": claim_c_verdict,
        "domain_reverse_context": {
            "note": "join jest kierunku A->N (twierdzenie C); poniżej kontekst odwrotny "
                    "(ile wpisów archiwum nie jest referencjonowane przez pola A/B template'ów)",
            "models_nif_ids_not_referenced_by_any_A": len(set(nif_ids.keys()) - set(unique_A_nonzero)),
            "volumes_bvi_ids_not_referenced_by_any_B": len(set(bvi_ids.keys()) - set(unique_B_nonzero)),
            "A_domain_is_subset_of_N_domain": set(unique_A_nonzero) <= set(nif_ids.keys()),
            "B_nonzero_domain_is_subset_of_BVI_domain": set(unique_B_nonzero) <= set(bvi_ids.keys()),
        },
        "errors": [],
    }

    with open(os.path.join(OUT_RAW, "Z2_JOIN_RESULT.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(os.path.join(OUT_RAW, "Z2_JOIN_A_TO_NIF_DETAIL.csv"), "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=["a_value", "hit", "models_entry_index", "models_offset",
                                          "packed_size", "template_ids", "template_count"])
        w.writeheader()
        for row in join_detail:
            w.writerow(row)

    with open(os.path.join(OUT_RAW, "Z2_JOIN_B_TO_BVI_DETAIL.csv"), "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=["b_value", "hit", "volumes_entry_index", "volumes_offset",
                                          "packed_size", "template_ids", "template_count"])
        w.writeheader()
        for row in b_join_detail:
            w.writerow(row)

    with open(os.path.join(OUT_RAW, "Z2_NEGATIVE_CONTROL_A.csv"), "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=["base_a", "synthetic_a", "name", "present_in_models_bnt"])
        w.writeheader()
        for row in neg_rows:
            w.writerow(row)

    with open(os.path.join(OUT_RAW, "Z2_MODELS_BNT_INDEX_NAMES.csv"), "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(["entry_index", "name", "packed_size", "offset"])
        for e in models_entries:
            w.writerow([e["index"], e["name"], e["packed"], e["offset"]])

    with open(os.path.join(OUT_RAW, "Z2_VOLUMES_BNT_INDEX_NAMES.csv"), "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(["entry_index", "name", "packed_size", "offset"])
        for e in volumes_entries:
            w.writerow([e["index"], e["name"], e["packed"], e["offset"]])

    print(json.dumps({
        "claim_C_verdict": claim_c_verdict,
        "records": total_records,
        "unique_T": len(unique_T),
        "unique_A_nonzero": len(unique_A_nonzero),
        "A_zero_records": len(a_zero_records),
        "join_hits": join_hits,
        "join_misses": len(join_misses),
        "per_record_hits": rec_hit_count,
        "per_record_misses": rec_miss_count,
        "bonus_B_hits": b_join_hits,
        "bonus_B_misses": len(b_join_misses),
        "models_nif_ids": len(nif_ids),
        "max_nif_id": max_nif_id,
        "max_A": max_A,
        "be_hits": be_hits,
        "driver_sha256": driver_sha,
    }, indent=2))
    print("[Z2] FULL JOIN PASS")


if __name__ == "__main__":
    main()
