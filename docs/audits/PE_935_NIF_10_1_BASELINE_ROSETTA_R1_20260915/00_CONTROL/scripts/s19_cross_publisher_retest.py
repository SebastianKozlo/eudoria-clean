#!/usr/bin/env python3
# s19_cross_publisher_retest.py -- C7 re-adjudication of the
# cross-publisher GroupID evidence for PE_935_NIF_10_1_WORKAUDIT_
# CORRECTION_R1_20260916.
#
# Re-runs the s08 cross-publisher sample set (EE2 + Gamebryo SDK
# samples) with BOTH the frozen decoder (OLD) and FIELD_IDENTITY_V2
# (s14), recording per-file status and the exact failure point.
# Expected changes (derived independently by the s15 engine walker):
#   BABYLENGUIN.NIF: OLD fails "block 7 GroupID=479309" (FALSE read,
#   mechanism reproduced by s16); V2 passes blocks 0-6 with the
#   correct File Name[UE==0] consumption (block6 end=1517, block7
#   GroupID=0@1517) and fails only later at genuinely unsupported
#   types. The "nonzero GroupID in a non-PE 10.1 file" positive-realism
#   witness is RETRACTED.
#   EE2 samples contain no NiSourceTexture -> outcomes must be
#   IDENTICAL between OLD and V2 (defect could not contribute).
#
# Output: 01_RAW/CROSS_PUBLISHER_RETEST_FIELDIDENTITY.csv
import csv
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s06_world_slice_validator import (  # noqa: E402
    WorldSliceValidator, Cursor, ArkBlockError)
from s14_world_slice_validator_fieldidentity_v2 import (  # noqa: E402
    WorldSliceValidatorV2)
from s04_nifxml_baseline import Unresolved  # noqa: E402

SAMPLES = [
    r"D:\Eudoria_Reconstruction\04_External_References\reference_only"
    r"\blender_niftools\todo\old_nifs\ee2\lodtest.nif",
    r"D:\Eudoria_Reconstruction\04_External_References\reference_only"
    r"\blender_niftools\todo\old_nifs\ee2\lodtest-skinned.nif",
    r"D:\gamebyroengine\extracted\gb112_known_good\BABYLENGUIN.NIF",
    r"D:\gamebyroengine\extracted\gb112_known_good\DESTROYERBOT.NIF",
    r"D:\gamebyroengine\extracted\gb112_known_good\ROCKY.NIF",
]
REPO_RAW = os.path.join(os.path.dirname(HERE), "..", "01_RAW")


def sequential(v, data):
    """s08-style sequential decode with per-block tracing. Returns
    (status, last_ok_block_index, detail)."""
    cur = Cursor(data)
    try:
        hdr = v.parse_header(cur)
    except Exception as ex:  # noqa: BLE001
        return "FAIL", -1, "header: %s: %s" % (type(ex).__name__, ex)
    for i in range(hdr["num_blocks"]):
        tname = hdr["types"][hdr["idx"][i]]
        start = cur.pos
        gid = cur.u32()
        if gid != 0:
            return ("FAIL", i - 1,
                    "block %d GroupID=%d at offset %d (%s)"
                    % (i, gid, start, tname))
        if tname not in v.dec.s.objects:
            return ("FAIL", i - 1,
                    "unsupported type %s at block %d" % (tname, i))
        try:
            v.dec.decode_block(cur, tname)
        except (Unresolved, struct.error, ValueError, IndexError,
                TypeError, UnicodeDecodeError) as ex:
            return ("FAIL", i - 1,
                    "block %d %s: %s: %s" % (i, tname,
                                             type(ex).__name__,
                                             str(ex)[:100]))
    try:
        ntop = cur.u32()
        cur.skip(ntop * 4)
        eof_ok = cur.pos == len(data)
    except (struct.error, ValueError) as ex:
        return ("FAIL", hdr["num_blocks"] - 1,
                "footer: %s" % str(ex)[:100])
    return ("CLOSURE_OK" if eof_ok else "EOF_MISMATCH",
            hdr["num_blocks"] - 1, "")


def main():
    v_old = WorldSliceValidator()
    v_v2 = WorldSliceValidatorV2()
    rows = []
    for path in SAMPLES:
        if not os.path.exists(path):
            rows.append({"file": os.path.basename(path),
                         "old_status": "MISSING",
                         "v2_status": "MISSING"})
            continue
        data = open(path, "rb").read()
        st_old, last_old, det_old = sequential(v_old, data)
        st_v2, last_v2, det_v2 = sequential(v_v2, data)
        rows.append({
            "file": os.path.basename(path),
            "old_status": st_old,
            "old_last_ok_block": last_old,
            "old_detail": det_old,
            "v2_status": st_v2,
            "v2_last_ok_block": last_v2,
            "v2_detail": det_v2,
        })
    out = os.path.join(REPO_RAW, "CROSS_PUBLISHER_RETEST_FIELDIDENTITY"
                      ".csv")
    cols = ["file", "old_status", "old_last_ok_block", "old_detail",
            "v2_status", "v2_last_ok_block", "v2_detail"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, restval="")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    for r in rows:
        print("%s OLD=%s(%s) V2=%s(%s)"
              % (r["file"], r.get("old_status"),
                 r.get("old_detail", "")[:60],
                 r.get("v2_status"), r.get("v2_detail", "")[:60]))
    print("csv", out, len(rows))


if __name__ == "__main__":
    main()
