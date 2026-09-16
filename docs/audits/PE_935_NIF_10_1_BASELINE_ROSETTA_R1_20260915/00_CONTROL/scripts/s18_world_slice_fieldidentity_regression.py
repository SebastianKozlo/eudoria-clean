#!/usr/bin/env python3
# s18_world_slice_fieldidentity_regression.py -- C6 correction
# regression for PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916.
#
# Bounded regression of the FIELD_IDENTITY_V2 decoder (s14) against the
# FROZEN decoder (s06) over the existing 2363 world-slice files.
# This is correction regression -- NOT a new holdout (contract C6).
#
# For each slice file (deterministic sorted order):
#   OLD = s06 WorldSliceValidator.decode_file (frozen instrument,
#         executed read-only; hypothesis sha unchanged)
#   V2  = s14 WorldSliceValidatorV2.decode_file (field-identity fix)
# recorded: closure status both, per-block boundary arrays both,
# canonical per-block value fingerprints, duration.
#
# Comparison outputs:
#   files_same_closure / files_newly_closing / files_newly_failing /
#   files_ambiguous / changed_field_interpretations /
#   changed_boundaries / INFRA classes.
# Final algebra: PASS + FAIL + AMBIGUOUS + INFRA_UNRESOLVED = 2363.
#
# Chunking (contract C11 execution rule): deterministic sorted order;
# --chunk K of N; partial results persisted to 02_WORK
# WORLD_SLICE_V2_CHUNK_K.json; aggregate only after all chunks complete.
# An infrastructure timeout is NOT a NIF failure (separate INFRA_
# classes; never counted as parse failure).
#
# Output (aggregate): 01_RAW/WORLD_SLICE_FIELDIDENTITY_REGRESSION.csv
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_bnt2_walk import walk_bnt2  # noqa: E402
from s02_nif_version_scan import ARCHIVE  # noqa: E402
from s06_world_slice_validator import (  # noqa: E402
    WorldSliceValidator, ArkBlockError)
from s14_world_slice_validator_fieldidentity_v2 import (  # noqa: E402
    WorldSliceValidatorV2)
from s04_nifxml_baseline import Unresolved  # noqa: E402
import struct  # noqa: E402

VALIDATION = (r"D:\Eudoria_Reconstruction\99_Audits"
              r"\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\02_WORK"
              r"\WORLD_SLICE_VALIDATION.json")
WORK = (r"D:\Eudoria_Reconstruction\99_Audits"
        r"\PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916\02_WORK")
REPO_RAW = os.path.join(os.path.dirname(HERE), "..", "01_RAW")

CATCH = (Unresolved, ValueError, IndexError, TypeError, KeyError,
         UnicodeDecodeError)


def canon(obj):
    """Canonical fingerprint of a decoded block (sorted, deterministic).
    __start__/__end__/__decision__ fields are stripped (boundary
    comparison is separate)."""
    def rec(o):
        if isinstance(o, dict):
            return sorted((str(k), rec(v)) for k, v in o.items()
                          if not str(k).startswith("__"))
        if isinstance(o, list):
            return [rec(x) for x in o]
        if isinstance(o, float):
            return round(o, 6)
        return repr(o)
    import hashlib
    s = json.dumps(rec(obj), sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def run_one(v, payload):
    """decode_file with per-class error translation.
    Returns (status, info) where status in
    {OK, FAIL, AMBIGUOUS_LAYOUT, TOOL_EXCEPTION}."""
    t0 = time.time()
    try:
        res = v.decode_file(payload)
        dur = time.time() - t0
        if res is None:
            return "FAIL", {"err": "closure search exhausted",
                            "dur": dur}
        blocks = res["blocks"]
        return "OK", {
            "bounds": [[b.get("__start__"), b.get("__end__")]
                       for b in blocks],
            "types": [b.get("__type__") for b in blocks],
            "fps": [canon(b) for b in blocks],
            "tops": res["top_objects"],
            "search": res["search_used"],
            "dur": dur}
    except Unresolved as ex:
        return "FAIL", {"err": "Unresolved: %s" % str(ex)[:120],
                        "dur": time.time() - t0}
    except ArkBlockError as ex:
        return "FAIL", {"err": "ArkBlockError: %s" % str(ex)[:120],
                        "dur": time.time() - t0}
    except struct.error as ex:
        return "FAIL", {"err": "struct.error: %s" % str(ex)[:120],
                        "dur": time.time() - t0}
    except (ValueError, IndexError, KeyError, TypeError,
            UnicodeDecodeError) as ex:
        return "FAIL", {"err": "%s: %s" % (type(ex).__name__,
                                           str(ex)[:120]),
                        "dur": time.time() - t0}
    except MemoryError as ex:
        return "INFRA_RESOURCE_LIMIT", {"err": "MemoryError",
                                        "dur": time.time() - t0}
    except RecursionError:
        return "INFRA_RESOURCE_LIMIT", {"err": "RecursionError",
                                        "dur": time.time() - t0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", type=int, default=0,
                    help="run chunk K (0-based) of N")
    ap.add_argument("--nchunks", type=int, default=1)
    ap.add_argument("--max-seconds", type=float, default=1e9,
                    help="stop before starting a new file once chunk "
                         "wall-clock exceeds this (resume = next chunk "
                         "run with same boundaries minus done)")
    args = ap.parse_args()

    val = json.load(open(VALIDATION, encoding="utf-8"))
    names = []
    for subset in ("train", "hold"):
        for r in val["results"][subset]:
            names.append((r["name"], r["subset"], r["closure"]))
    names.sort()
    total = len(names)
    k, n = args.chunk, args.nchunks
    mine = [x for idx, x in enumerate(names) if idx % n == k]
    print("slice files %d; chunk %d/%d -> %d files"
          % (total, k, n, len(mine)))

    # resume support: previously completed files in this chunk
    out_path = os.path.join(WORK, "WORLD_SLICE_V2_CHUNK_%d.json" % k)
    done = {}
    if os.path.exists(out_path):
        done = json.load(open(out_path, encoding="utf-8"))
        print("resuming: %d files already done" % len(done))

    walk = walk_bnt2(ARCHIVE)
    ents = {e["name"]: e for e in walk["entries"]}
    v_old = WorldSliceValidator()
    v_v2 = WorldSliceValidatorV2()
    t_start = time.time()
    n_infra_stop = 0

    with open(ARCHIVE, "rb") as f:
        for name, subset, old_frozen_closure in mine:
            if name in done:
                continue
            if time.time() - t_start > args.max_seconds:
                n_infra_stop += 1
                break
            e = ents.get(name)
            if e is None:
                done[name] = {"subset": subset, "err": "ENTRY_MISSING",
                              "status": "AMBIGUOUS"}
                continue
            f.seek(e["offset"])
            payload = f.read(e["size"])
            st_old, info_old = run_one(v_old, payload)
            st_v2, info_v2 = run_one(v_v2, payload)
            rec = {"subset": subset,
                   "frozen_closure": old_frozen_closure,
                   "old_now": st_old, "v2": st_v2}
            if st_old == "OK" and st_v2 == "OK":
                rec["same_closure"] = (
                    info_old["bounds"] == info_v2["bounds"] and
                    info_old["fps"] == info_v2["fps"])
                rec["changed_boundaries"] = (
                    info_old["bounds"] != info_v2["bounds"])
                rec["changed_field_interpretations"] = (
                    info_old["fps"] != info_v2["fps"])
            else:
                rec["same_closure"] = st_old == st_v2
            if st_old != "OK":
                rec["old_err"] = info_old.get("err")
            if st_v2 != "OK":
                rec["v2_err"] = info_v2.get("err")
            rec["dur_old"] = round(info_old.get("dur", 0), 3)
            rec["dur_v2"] = round(info_v2.get("dur", 0), 3)
            done[name] = rec
            if len(done) % 100 == 0:
                json.dump(done, open(out_path, "w", encoding="utf-8"))
                print("... %d done (%.1fs)" % (len(done),
                                              time.time() - t_start))
    json.dump(done, open(out_path, "w", encoding="utf-8"))
    print("chunk %d complete: %d files (infra_stop=%d)"
          % (k, len(done), n_infra_stop))


if __name__ == "__main__":
    main()
