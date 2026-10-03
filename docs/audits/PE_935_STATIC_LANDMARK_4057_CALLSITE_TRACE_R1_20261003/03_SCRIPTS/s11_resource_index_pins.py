#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S11 RESOURCE INDEX PINS — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
Executor: pe-reconstruction. ERA: PCG/EU 9.3.5 (pcg_install). STATIC-ONLY.

Curates the contract-required 01_RAW/RESOURCE_INDEX_PINS.json from fresh,
bounded, index-only BNT2 trailer-index lookups (same parser as s1; index
metadata only, NO payload extraction):
  Models.bnt  -> "296445.nif" (calibration anchor @395,268,773), "218757.nif"
  Volumes.bnt -> "296446.bvi" (calibration), "218758.bvi"
NEW_MODEL_RESOURCE_INDEX_RECORDS = 4 (limit respected).

Interpreter: python 3.12.10. Invoke: python 03_SCRIPTS/s11_resource_index_pins.py
"""

import hashlib
import json
import os
import struct

RUN_ID = "PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003"
HERE = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.normpath(os.path.join(HERE, "..", "01_RAW"))
OUT = os.path.join(RAWDIR, "RESOURCE_INDEX_PINS.json")

MODELS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
VOLUMES = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"

EXPECTED = {
    "models_index_start": 395262727,
    "models_index_count": 5596,
    "anchor_296445nif": 395268773,
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def parse_bnt2_names(path, want_names):
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
    res = {"run_id": RUN_ID, "stage": "S11_resource_index_pins",
           "measured": {}, "interpreted": {}, "errors": []}
    M = res["measured"]
    M["models_bnt_identity"] = {"path": MODELS, "size_bytes": os.path.getsize(MODELS),
                               "sha256": sha256_file(MODELS)}
    M["volumes_bnt_identity"] = {"path": VOLUMES, "size_bytes": os.path.getsize(VOLUMES),
                                 "sha256": sha256_file(VOLUMES)}
    names_m, idx_m, cnt_m, err_m = parse_bnt2_names(MODELS, {"296445.nif", "218757.nif"})
    if err_m:
        res["errors"].append("Models.bnt: %s" % err_m)
    M["models_bnt_index"] = {"index_start": idx_m, "entry_count": cnt_m,
                             "found": {k: v for k, v in (names_m or {}).items()},
                             "calibration_296445_nif": (names_m or {}).get("296445.nif"),
                             "target_218757_nif": (names_m or {}).get("218757.nif")}
    names_v, idx_v, cnt_v, err_v = parse_bnt2_names(VOLUMES, {"296446.bvi", "218758.bvi"})
    if err_v:
        res["errors"].append("Volumes.bnt: %s" % err_v)
    M["volumes_bnt_index"] = {"index_start": idx_v, "entry_count": cnt_v,
                              "found": {k: v for k, v in (names_v or {}).items()},
                              "calibration_296446_bvi": (names_v or {}).get("296446.bvi"),
                              "target_218758_bvi": (names_v or {}).get("218758.bvi")}
    I = res["interpreted"]
    I["models_calibration_ok"] = (idx_m == EXPECTED["models_index_start"]
                                  and cnt_m == EXPECTED["models_index_count"]
                                  and (names_m or {}).get("296445.nif") == EXPECTED["anchor_296445nif"])
    I["MODEL_INDEX_218757"] = "PRESENT" if (names_m or {}).get("218757.nif") is not None else "ABSENT"
    I["COLLISION_INDEX_218758"] = "PRESENT" if (names_v or {}).get("218758.bvi") is not None else "ABSENT"
    I["NOTE"] = ("index presence only — NO resource request/resolution claim at the "
                 "0x0059AB12 call-site (the falsifier fired; see "
                 "02_ANALYSIS/TEMPLATE_ROLE_TEST.md). These are data-side facts "
                 "about the candidate resource names.")
    I["pin_provenance"] = {
        "bnt2_index_pins": {
            "MEASURED_QUANTITY": "presence + name_file_offset of 4 exact index names (2 calibration, 2 target) in the two BNT2 trailer indexes",
            "INDEPENDENT_SOURCE_OF_TRUTH": "physical trailer/index bytes of Models.bnt / Volumes.bnt (re-hashed this run)",
            "WHY_NON_CIRCULAR": "own parser; the Models.bnt side must reproduce the canon calibration (index_start/count/anchor offset) before the target lookups are trusted",
            "FAILURE_CASE_DETECTED": "wrong entry stride desynchronizes the name walk (0x0A misses / walked != count) or displaces the calibration anchor; absent name => ABSENT"},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("S11 written:", OUT)
    print("errors:", res["errors"])
    print("models calibration ok:", I["models_calibration_ok"])
    print("MODEL_INDEX_218757:", I["MODEL_INDEX_218757"], "@", M["models_bnt_index"]["target_218757_nif"])
    print("COLLISION_INDEX_218758:", I["COLLISION_INDEX_218758"], "@", M["volumes_bnt_index"]["target_218758_bvi"])


if __name__ == "__main__":
    main()
