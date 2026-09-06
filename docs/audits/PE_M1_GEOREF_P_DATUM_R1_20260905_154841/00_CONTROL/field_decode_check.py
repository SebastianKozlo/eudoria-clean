#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
field_decode_check.py -- RECONSTRUCTED generator for 01_RAW/FIELD_DECODE_CHECK.json

Run:     PE_FIELD_DECODE_GENERATOR_RECONSTRUCTION_R1
Parent:  PE-MASTER loop 0ed3ca19-99c6-4af0-974b-f64fc2842c76 (iteration 2), mission item C
Package: docs/audits/PE_M1_GEOREF_P_DATUM_R1_20260905_154841 (eudoria-clean repo)

PURPOSE (F-R3 closure):
    PE-MASTER review of run PE_M1_GEOREF_P_DATUM_R1_20260905_154841 (2026-09-06) recorded
    FINDING (c) F-R3 [P2]: "01_RAW/FIELD_DECODE_CHECK.json has NO persisted generator (none
    of the 4 pinned drivers computes it) -- provenance gap; PE-MASTER's re-execution
    independently reproduces the artifact exactly; the driver reconstruction + reproduction
    proof is ORDERED as the next iteration (run-local addendum; the historical artifact
    stays byte-identical)."
    This driver is that reconstruction. It re-derives the artifact from the PHYSICAL
    429259.dat payload inside pcg_install\\Data\\Textures\\Textures.bnt: the BNT2 trailer
    index is parsed here (the payload location is READ from the parsed index, never
    hardcoded), the payload identity is pinned by SHA256, the TGA header is asserted, and
    every texel is decoded with the 16-bit model h = ((B<<8|G)/256 - 128) * 5.

DETERMINISM:
    Output is a pure function of the physical Textures.bnt bytes. No timestamps, no
    environment-dependent values. Read-only on all originals. Writes exactly two files,
    both inside this run package:
      01_RAW/FIELD_DECODE_CHECK_REPRODUCTION.json  (the reproduction proof)
      00_CONTROL/SHA256_DRIVER_ADDENDUM.md        (the run-local addendum)

FAIL-CLOSED:
    Any assert failure prints measured-vs-expected to stderr and exits nonzero WITHOUT
    writing anything. No partial PASS.
"""

import hashlib
import json
import os
import struct
import sys

RUN_ID = "PE_FIELD_DECODE_GENERATOR_RECONSTRUCTION_R1"
DRIVER_NAME = "field_decode_check.py"

BNT_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Textures\Textures.bnt"
ENTRY_NAME = "429259.dat"

# --- identity pins (PE-MASTER physical verification 2026-09-06; PE_MASTER_REVIEW.md) ---
PIN_ENTRY_INDEX = 71
PIN_ENTRY_OFFSET = 6920273
PIN_ENTRY_PACKED = 198191
PIN_PAYLOAD_SHA256 = "0BADB42EC131EE53C49E63EADEE529AA18A68A31D0CF16A57694488FF3333412"
# The physical payload hash above closes the DEFECTIVE iter029 pin
# 23D7742EBA6FFB1FDA2F8A58BD0EB95AFDBE055CE23437FF5B47C5A0163A1ED0 (CORRECTION_LEDGER entry A).

# --- TGA header pins ---
PIN_TGA_ID_LEN = 0
PIN_TGA_IMAGE_TYPE = 2
PIN_TGA_WIDTH = 257
PIN_TGA_HEIGHT = 257
PIN_TGA_BPP = 24
PIN_TGA_DESCRIPTOR = 0x00

# --- historical artifact values (01_RAW/FIELD_DECODE_CHECK.json, RUN-3) ---
PIN_LAND_PCT = 79.60605005374798
PIN_HMIN = -639.43359375
PIN_HMAX = 638.90625
LAND_PCT_TOL = 1e-9

TGA_PIXEL_START = 18
N_TEXELS = 257 * 257  # 66049


def die(message):
    sys.stderr.write("ASSERT-FAIL: " + message + "\n")
    sys.stderr.write("FAIL-CLOSED: no output written.\n")
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


ADDENDUM_TMPL = """# SHA256_DRIVER_ADDENDUM -- field_decode_check.py (F-R3 reconstruction)

field_decode_check.py sha256 {driver_sha} (after last edit, before execution; self-hashed by
the driver at startup BEFORE any decoding work; the same value is embedded in
01_RAW/FIELD_DECODE_CHECK_REPRODUCTION.json -> provenance.driver_sha256)

## Provenance note

The PE-MASTER review of run PE_M1_GEOREF_P_DATUM_R1_20260905_154841 (2026-09-06) recorded
FINDING (c) F-R3 [P2]: "01_RAW/FIELD_DECODE_CHECK.json has NO persisted generator (none of
the 4 pinned drivers computes it) -- provenance gap; PE-MASTER's re-execution independently
reproduces the artifact exactly; the driver reconstruction + reproduction proof is ORDERED as
the next iteration (run-local addendum; the historical artifact stays byte-identical)."
This file is that run-local addendum. field_decode_check.py is the RECONSTRUCTED generator,
written fresh (not recovered) in run PE_FIELD_DECODE_GENERATOR_RECONSTRUCTION_R1 under the
PE-MASTER loop 0ed3ca19-99c6-4af0-974b-f64fc2842c76 iteration-2 authorization (mission item
C). It parses the BNT2 trailer index of pcg_install\\Data\\Textures\\Textures.bnt itself,
locates entry 429259.dat from the parsed index (index 71, offset 6920273, packed 198191 B --
read from the index, not hardcoded), pins the physical payload SHA256 {payload_sha} (closing
the DEFECTIVE iter029 pin 23D7742E...; CORRECTION_LEDGER entry A), asserts the TGA header
(type 2, 257x257, 24bpp, descriptor 0x00), decodes all 66,049 texels with the 16-bit model
h = ((B<<8|G)/256 - 128) * 5, and reproduces the historical values exactly: land_pct
{land_pct} (land_count {land_count} / 66,049), hmin {hmin}, hmax {hmax} -- exit 0, all
asserts held. The reproduction proof is 01_RAW/FIELD_DECODE_CHECK_REPRODUCTION.json. The
historical 01_RAW/FIELD_DECODE_CHECK.json and the historical 00_CONTROL/SHA256_DRIVER.txt
are NOT modified by this run (the historical artifact stays byte-identical); this addendum
is a separate, NEW file next to the historical driver manifest.
"""


def main():
    # (0) driver self-hash -- PRE-EXECUTION, before any decoding work
    driver_path = os.path.abspath(__file__)
    driver_sha = sha256_file(driver_path)

    pkg_root = os.path.dirname(os.path.dirname(driver_path))  # 00_CONTROL/ -> package root
    hist_rel = os.path.join("01_RAW", "FIELD_DECODE_CHECK.json")
    repro_rel = os.path.join("01_RAW", "FIELD_DECODE_CHECK_REPRODUCTION.json")
    addendum_rel = os.path.join("00_CONTROL", "SHA256_DRIVER_ADDENDUM.md")

    # (1) parse the BNT2 trailer index OURSELVES
    bnt_sha = sha256_file(BNT_PATH)  # provenance pin: computed, recorded (not asserted)
    bnt_size = os.path.getsize(BNT_PATH)
    with open(BNT_PATH, "rb") as f:
        f.seek(bnt_size - 8)
        tail = f.read(8)
    index_start, = struct.unpack("<I", tail[:4])
    magic = tail[4:]
    if magic != b"BNT2":
        die("BNT2 trailer magic: measured %r expected b'BNT2'" % (magic,))
    with open(BNT_PATH, "rb") as f:
        f.seek(index_start)
        index_blob = f.read()
    count, = struct.unpack_from("<I", index_blob, 0)

    entry = None
    pos = 4
    for i in range(count):
        nl = index_blob.find(b"\x0a", pos)
        if nl < 0:
            die("index parse: unterminated name at entry %d" % i)
        name = index_blob[pos:nl].decode("latin-1")
        pos = nl + 1
        packed, offset, c_field, d_field = struct.unpack_from("<4I", index_blob, pos)
        pos += 16
        if name == ENTRY_NAME:
            entry = {
                "index": i,
                "name": name,
                "packed": packed,
                "offset": offset,
                "c": c_field,
                "d": d_field,
            }
            break
    if entry is None:
        die("entry %r not found in parsed BNT2 index (entry_count=%d)" % (ENTRY_NAME, count))

    # identity asserts -- values read FROM THE PARSED INDEX
    if entry["index"] != PIN_ENTRY_INDEX:
        die("entry index: measured %d expected %d" % (entry["index"], PIN_ENTRY_INDEX))
    if entry["offset"] != PIN_ENTRY_OFFSET:
        die("entry offset: measured %d expected %d" % (entry["offset"], PIN_ENTRY_OFFSET))
    if entry["packed"] != PIN_ENTRY_PACKED:
        die("entry packed size: measured %d expected %d" % (entry["packed"], PIN_ENTRY_PACKED))

    # (2) read the payload at the PARSED offset/size; pin its SHA256
    with open(BNT_PATH, "rb") as f:
        f.seek(entry["offset"])
        payload = f.read(entry["packed"])
    if len(payload) != entry["packed"]:
        die("payload read: measured %d bytes expected %d" % (len(payload), entry["packed"]))
    payload_sha = hashlib.sha256(payload).hexdigest().upper()
    if payload_sha != PIN_PAYLOAD_SHA256:
        die("payload sha256: measured %s expected %s"
            % (payload_sha, PIN_PAYLOAD_SHA256))

    # (3) TGA header asserts
    tga = {
        "id_len": payload[0],
        "cmap_type": payload[1],
        "image_type": payload[2],
        "width": struct.unpack_from("<H", payload, 12)[0],
        "height": struct.unpack_from("<H", payload, 14)[0],
        "bpp": payload[16],
        "descriptor": payload[17],
    }
    if tga["id_len"] != PIN_TGA_ID_LEN:
        die("tga id_len: measured %r expected %r" % (tga["id_len"], PIN_TGA_ID_LEN))
    if tga["image_type"] != PIN_TGA_IMAGE_TYPE:
        die("tga image_type: measured %r expected %r" % (tga["image_type"], PIN_TGA_IMAGE_TYPE))
    if tga["width"] != PIN_TGA_WIDTH:
        die("tga width: measured %r expected %r" % (tga["width"], PIN_TGA_WIDTH))
    if tga["height"] != PIN_TGA_HEIGHT:
        die("tga height: measured %r expected %r" % (tga["height"], PIN_TGA_HEIGHT))
    if tga["bpp"] != PIN_TGA_BPP:
        die("tga bpp: measured %r expected %r" % (tga["bpp"], PIN_TGA_BPP))
    if tga["descriptor"] != PIN_TGA_DESCRIPTOR:
        die("tga descriptor: measured %r expected %r" % (tga["descriptor"], PIN_TGA_DESCRIPTOR))

    # (4) decode every texel (pixel start 18, stride 3 bytes B,G,R)
    land_count = 0
    hmin = None
    hmax = None
    hsum = 0.0
    for i in range(N_TEXELS):
        b_byte = payload[TGA_PIXEL_START + 3 * i]
        g_byte = payload[TGA_PIXEL_START + 3 * i + 1]
        raw16 = (b_byte << 8) | g_byte
        h = (raw16 / 256.0 - 128.0) * 5.0
        if h > 0.0:
            land_count += 1
        if hmin is None or h < hmin:
            hmin = h
        if hmax is None or h > hmax:
            hmax = h
        hsum += h
    land_pct = land_count / N_TEXELS * 100
    mean = hsum / N_TEXELS

    # (5) value asserts vs the historical artifact (exact float64 for hmin/hmax)
    if abs(land_pct - PIN_LAND_PCT) >= LAND_PCT_TOL:
        die("land_pct: measured %r expected %r (tol %g)"
            % (land_pct, PIN_LAND_PCT, LAND_PCT_TOL))
    if hmin != PIN_HMIN:
        die("hmin: measured %r expected %r" % (hmin, PIN_HMIN))
    if hmax != PIN_HMAX:
        die("hmax: measured %r expected %r" % (hmax, PIN_HMAX))

    # (6) read the historical artifact (READ-ONLY) and quote it verbatim
    hist_path = os.path.join(pkg_root, hist_rel)
    with open(hist_path, "r", encoding="utf-8") as f:
        hist_raw = f.read()
    hist = json.loads(hist_raw)

    land_pct_diff = abs(land_pct - hist["land_pct"])
    hmin_equal = (hmin == hist["hmin"])
    hmax_equal = (hmax == hist["hmax"])
    if not (land_pct_diff < LAND_PCT_TOL and hmin_equal and hmax_equal):
        die("comparison vs historical artifact: land_pct_diff=%r hmin_equal=%r hmax_equal=%r"
            % (land_pct_diff, hmin_equal, hmax_equal))
    verdict = "EXACT_REPRODUCTION_PASS"

    out = {
        "run": RUN_ID,
        "pins": {
            "textures_bnt": {
                "path": BNT_PATH,
                "size_bytes": bnt_size,
                "sha256": bnt_sha,
            },
            "bnt2_trailer": {
                "index_start": index_start,
                "magic": "BNT2",
                "entry_count": count,
            },
            "payload": {
                "name": entry["name"],
                "index": entry["index"],
                "offset": entry["offset"],
                "packed_size": entry["packed"],
                "index_field_c": entry["c"],
                "index_field_d": entry["d"],
                "sha256": payload_sha,
            },
        },
        "tga_asserts": tga,
        "computed": {
            "land_pct": land_pct,
            "land_count": land_count,
            "n_texels": N_TEXELS,
            "hmin": hmin,
            "hmax": hmax,
            "mean": mean,
        },
        "historical": {
            "path": hist_rel.replace("\\", "/"),
            "verbatim": hist_raw,
            "parsed": hist,
        },
        "comparison": {
            "land_pct_diff": land_pct_diff,
            "hmin_equal": hmin_equal,
            "hmax_equal": hmax_equal,
        },
        "verdict": verdict,
        "provenance": {
            "driver": DRIVER_NAME,
            "driver_sha256": driver_sha,
            "generated_by": DRIVER_NAME + " (reconstructed generator, run " + RUN_ID + ")",
            "note": ("reconstructed generator closing the F-R3 provenance gap; "
                     "the historical FIELD_DECODE_CHECK.json stays byte-identical"),
        },
    }

    repro_path = os.path.join(pkg_root, repro_rel)
    with open(repro_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")

    addendum = ADDENDUM_TMPL.format(
        driver_sha=driver_sha,
        payload_sha=payload_sha,
        land_pct=repr(land_pct),
        land_count=land_count,
        hmin=repr(hmin),
        hmax=repr(hmax),
    )
    addendum_path = os.path.join(pkg_root, addendum_rel)
    with open(addendum_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(addendum)

    summary = {
        "verdict": verdict,
        "land_pct": land_pct,
        "land_count": land_count,
        "hmin": hmin,
        "hmax": hmax,
        "mean": mean,
        "land_pct_diff": land_pct_diff,
        "hmin_equal": hmin_equal,
        "hmax_equal": hmax_equal,
        "driver_sha256": driver_sha,
        "payload_sha256": payload_sha,
        "textures_bnt_sha256": bnt_sha,
        "wrote": [repro_rel, addendum_rel],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
