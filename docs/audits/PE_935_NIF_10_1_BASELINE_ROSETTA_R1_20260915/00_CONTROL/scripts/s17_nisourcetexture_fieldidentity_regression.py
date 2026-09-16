#!/usr/bin/env python3
# s17_nisourcetexture_fieldidentity_regression.py -- C5 bounded
# structural regression for PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_
# 20260916.
#
# Regression ONLY (contract C5) -- NOT semantic science.
#
# Finds ALL physical v10.1 NiSourceTexture blocks in the PCG corpus
# (independent BNT2 walk + independent header/type-table scan; prior
# expected denominator 45 blocks / 5 files is a COMPARATOR, not an
# oracle), decodes every one with the FIELD_IDENTITY_V2 decoder (s14),
# and records: file, block_index, UseExternal, IsStatic, selected File
# Name branch, start/end/next offsets, next GroupID, closure status.
#
# Tests:
#   R1  Use External != 0 -> external texture path (File Name[UE==1]
#       consumed + Unknown Link read)
#   R2  Use External == 0 -> internal File Name path (File Name[UE==0]
#       consumed + Pixel Data ref read)
#   R3  full physical denominator: ALL v10.1 NiSourceTexture blocks
#
# Output: 01_RAW/NISOURCETEXTURE_FIELDIDENTITY_REGRESSION.csv
import csv
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s01_bnt2_walk import walk_bnt2  # noqa: E402
from s02_nif_version_scan import ARCHIVE  # noqa: E402
from s06_world_slice_validator import Cursor  # noqa: E402
from s14_world_slice_validator_fieldidentity_v2 import (  # noqa: E402
    WorldSliceValidatorV2)
from s04_nifxml_baseline import Unresolved  # noqa: E402

REPO_RAW = os.path.join(os.path.dirname(HERE), "..", "01_RAW")
WORK = (r"D:\Eudoria_Reconstruction\99_Audits"
        r"\PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916\02_WORK")
V10_1 = 0x0A010000


def scan_header(data):
    """Return header dict or None if not a NIF 10.1.0.0 payload."""
    nl = data.find(b"\n")
    if nl < 0 or nl > 256:
        return None
    pos = nl + 1
    if len(data) < pos + 12:
        return None
    ver, = struct.unpack_from("<I", data, pos)
    if ver != V10_1:
        return None
    pos += 4
    uv, = struct.unpack_from("<I", data, pos)
    pos += 4
    nb, = struct.unpack_from("<I", data, pos)
    pos += 4
    if nb > 4096:
        return None
    nbt, = struct.unpack_from("<H", data, pos)
    pos += 2
    if nbt > 256:
        return None
    names = []
    for _ in range(nbt):
        if pos + 4 > len(data):
            return None
        ln, = struct.unpack_from("<I", data, pos)
        pos += 4
        if ln > 128 or pos + ln > len(data):
            return None
        names.append(data[pos:pos + ln].decode("ascii", "replace"))
        pos += ln
    idx = []
    for _ in range(nb):
        if pos + 2 > len(data):
            return None
        ti, = struct.unpack_from("<H", data, pos)
        pos += 2
        if ti >= nbt:
            return None
        idx.append(ti)
    return {"version": ver, "user_version": uv, "num_blocks": nb,
            "types": names, "idx": idx}


# ----------------------------------------------------------------------
# ENGINE-TRANSCRIBED READERS (SRC-06 Gamebryo 1.2 source), for the
# controller/keyframe types that the frozen schema decoder cannot
# traverse (ARG tokens -> Unresolved). These readers are boundary-only
# instruments transcribed from:
#   NiTimeController.cpp LoadBinary (next ref, flags u16, freq, phase,
#     lo, hi, target ref; NiDeclareFlags(unsigned short))
#   NiInterpController/NiSingleInterpController/NiFloatInterpController
#     LoadBinary (nothing before 10.1.0.104)
#   NiTransformController.cpp (= NiKeyframeController successor; data
#     ref before 10.1.0.104)
#   NiTransformData.cpp (= NiKeyframeData successor; rot/pos/scale key
#     groups; NiRotKey/NiPosKey/NiFloatKey::LoadBinary; NiQuaternion
#     W,X,Y,Z order; NiAnimationKey.h KeyType NOINTERP=0, LIN=1,
#     BEZ=2, TCB=3, EULER=4, STEP=5)
#   NiFlipController.cpp (affected map u32, start f32, secs f32,
#     texture list before 10.1.0.104)
#   NiFloatData.cpp (key group of float keys)
#   NiTextureTransformController.cpp (bool, map index u32, enum u32,
#     float-data ref before 10.1.0.104)
# ----------------------------------------------------------------------

KEY_LIN, KEY_BEZ, KEY_TCB, KEY_EULER, KEY_STEP = 1, 2, 3, 4, 5


class EWalkFail(Exception):
    pass


def _keys_float(cur, n, ktype):
    per = {KEY_LIN: 8, KEY_BEZ: 16, KEY_TCB: 20, KEY_STEP: 8}
    if ktype not in per:
        raise EWalkFail("unsupported float key type %d" % ktype)
    cur.skip(n * per[ktype])


def _keys_pos(cur, n, ktype):
    per = {KEY_LIN: 16, KEY_BEZ: 32, KEY_TCB: 28, KEY_STEP: 16}
    if ktype not in per:
        raise EWalkFail("unsupported pos key type %d" % ktype)
    cur.skip(n * per[ktype])


def _keys_rot(cur, n, ktype):
    if ktype == KEY_LIN or ktype == KEY_BEZ:
        cur.skip(n * 20)      # time + quat WXYZ (BEZ rot: no tangents
    elif ktype == KEY_TCB:     # in this engine version)
        cur.skip(n * 32)
    elif ktype == KEY_STEP:
        cur.skip(n * 20)
    elif ktype == KEY_EULER:
        cur.u32()             # axis order enum
        for _ in range(3):
            nn = cur.u32()
            if nn > (1 << 20):
                raise EWalkFail("euler key count implausible")
            if nn > 0:
                kt = cur.u32()
                _keys_float(cur, nn, kt)
    else:
        raise EWalkFail("unsupported rot key type %d" % ktype)


def _key_group(cur, kind):
    n = cur.u32()
    if n > (1 << 20):
        raise EWalkFail("key count implausible %d" % n)
    if n > 0:
        ktype = cur.u32()
        if kind == "float":
            _keys_float(cur, n, ktype)
        elif kind == "pos":
            _keys_pos(cur, n, ktype)
        elif kind == "rot":
            _keys_rot(cur, n, ktype)


def e_nitimecontroller(cur):
    cur.u32()   # next controller ref
    cur.u16()   # flags
    cur.skip(16)  # frequency, phase, lo key time, hi key time
    cur.u32()   # target ref


def e_keyframecontroller(cur):
    e_nitimecontroller(cur)
    cur.u32()   # data ref (before 10.1.0.104)


def e_keyframedata(cur):
    _key_group(cur, "rot")
    _key_group(cur, "pos")
    _key_group(cur, "float")   # scale keys


def e_flipcontroller(cur):
    e_nitimecontroller(cur)
    cur.u32()   # affected map
    cur.skip(8)  # start time, secs per frame (before 10.1.0.104)
    nt = cur.u32()
    if nt > 4096:
        raise EWalkFail("flip texture count implausible %d" % nt)
    cur.skip(nt * 4)


def e_floatdata(cur):
    _key_group(cur, "float")


def e_texturetransformcontroller(cur):
    e_nitimecontroller(cur)
    cur.u8()    # shader map bool
    cur.u32()   # map index
    cur.u32()   # member enum
    cur.u32()   # float data ref (before 10.1.0.104)


ENGINE_READERS = {
    "NiKeyframeController": e_keyframecontroller,
    "NiTransformController": e_keyframecontroller,
    "NiKeyframeData": e_keyframedata,
    "NiTransformData": e_keyframedata,
    "NiFlipController": e_flipcontroller,
    "NiFloatData": e_floatdata,
    "NiTextureTransformController": e_texturetransformcontroller,
}


def walk_partial(v, data, targets, hdr, cur, i, max_target,
                 max_attempts=200000):
    """Recursive partial block walk with the FROZEN Ark search
    machinery (v.ark_candidates + v._decode_ark_with) and V2 schema
    blocks. Captures NiSourceTexture blocks at indices in `targets`;
    succeeds once block max_target+1's GroupID has been verified
    (i.e. when i > max_target). Returns list of target records along
    the successful path, or None (backtracking discipline identical
    in spirit to s06 _decode_blocks)."""
    if i > max_target:
        return []
    if i >= hdr["num_blocks"]:
        return None
    tname = hdr["types"][hdr["idx"][i]]
    start = cur.pos
    v._attempts += 1
    if v._attempts > max_attempts:
        return None
    gid = cur.u32()
    if gid != 0:
        return None
    if tname in ENGINE_READERS:
        save = cur.pos
        try:
            ENGINE_READERS[tname](cur)
        except (EWalkFail, struct.error, IndexError) as ex:
            cur.pos = save
            return None
        down = walk_partial(v, data, targets, hdr, cur, i + 1,
                            max_target, max_attempts)
        if down is None:
            cur.pos = save
        return down
    if tname in v.dec.s.objects and tname not in v.ARK_SEARCH:
        save = cur.pos
        try:
            if i in targets:
                blk = v.dec.decode_block(cur, tname)
            else:
                blk = v.dec.decode_block(cur, tname)
        except (Unresolved, struct.error, ValueError, IndexError,
                UnicodeDecodeError):
            cur.pos = save
            return None
        rec = None
        if i in targets:
            rec = st_record(hdr, i, tname, start, cur.pos, blk)
            # next block GroupID check
            if i + 1 < hdr["num_blocks"]:
                rec["next_block_offset"] = cur.pos
                rec["next_GroupID"] = cur.u32()
                rec["next_block_type"] = \
                    hdr["types"][hdr["idx"][i + 1]]
                cur.pos -= 4
                if rec["next_GroupID"] != 0:
                    cur.pos = save
                    return None
            else:
                rec["next_block_offset"] = ""
                rec["next_GroupID"] = ""
                rec["next_block_type"] = "END_OF_FILE"
        down = walk_partial(v, data, targets, hdr, cur, i + 1,
                            max_target, max_attempts)
        if down is None:
            cur.pos = save
            return None
        return ([rec] + down) if rec is not None else down
    # Ark search block (or unknown): candidate-driven, frozen logic
    v._current_num_blocks = hdr["num_blocks"]
    for cand in v.ark_candidates(cur, tname):
        save = cur.pos
        try:
            blk = v._decode_ark_with(cur, tname, cand)
        except (Unresolved, struct.error, ValueError, IndexError,
                UnicodeDecodeError):
            blk = None
        if blk is None:
            cur.pos = save
            continue
        down = walk_partial(v, data, targets, hdr, cur, i + 1,
                            max_target, max_attempts)
        if down is not None:
            return down
        cur.pos = save
    return None


def st_record(hdr, i, tname, start, end, blk):
    rec = {"block_index": i, "block_type": tname,
           "start_offset": start, "end_offset": end,
           "Use External": blk.get("Use External"),
           "Is Static": blk.get("Is Static"),
           "File Name": blk.get("File Name")}
    ue = blk.get("Use External")
    if ue == 1:
        rec["file_name_branch"] = "EXTERNAL (File Name[UE==1])"
        rec["link_value"] = blk.get("Unknown Link")
    elif ue == 0:
        rec["file_name_branch"] = "INTERNAL (File Name[UE==0])"
        rec["link_value"] = blk.get("Pixel Data")
    else:
        rec["file_name_branch"] = "UNKNOWN_UE_%r" % ue
        rec["link_value"] = None
    link = rec["link_value"]
    if isinstance(link, int) and 0 <= link < hdr["num_blocks"]:
        rec["link_target_type"] = hdr["types"][hdr["idx"][link]]
    return rec


def main():
    walk = walk_bnt2(ARCHIVE)
    entries = walk["entries"]
    print("bnt2 entries %d" % len(entries))
    v = WorldSliceValidatorV2()

    # PHASE 1: independent version+type-table scan over ALL entries
    files_with_st = []
    n_v101 = 0
    with open(ARCHIVE, "rb") as f:
        for e in entries:
            f.seek(e["offset"])
            head = f.read(min(e["size"], 65536))
            hdr = scan_header(head)
            if hdr is None:
                # type table may exceed the 64KB head for big files --
                # fall back to full payload
                if e["size"] > 65536:
                    f.seek(e["offset"])
                    head = f.read(e["size"])
                    hdr = scan_header(head)
                if hdr is None:
                    continue
            n_v101 += 1
            positions = [i for i, ti in enumerate(hdr["idx"])
                         if hdr["types"][ti] == "NiSourceTexture"]
            if positions:
                files_with_st.append(
                    {"name": e["name"], "size": e["size"],
                     "blocks": positions})
    total_blocks = sum(len(x["blocks"]) for x in files_with_st)
    print("v10.1 files %d; files_with_NiSourceTexture %d; blocks %d"
          % (n_v101, len(files_with_st), total_blocks))

    # PHASE 2: V2 decode of every NiSourceTexture block + file closure
    rows = []
    tally = {"TOTAL": 0, "FILES": len(files_with_st),
             "EXTERNAL_BRANCH": 0, "INTERNAL_BRANCH": 0,
             "PASS": 0, "FAIL": 0, "AMBIGUOUS": 0,
             "CLOSURE_OK": 0, "CLOSURE_FAIL": 0}
    with open(ARCHIVE, "rb") as f:
        for fw in files_with_st:
            f.seek(fw["name"] and 0 or 0)
            # locate entry payload
            payload = None
            for e in entries:
                if e["name"] == fw["name"]:
                    f.seek(e["offset"])
                    payload = f.read(e["size"])
                    break
            if payload is None:
                for bi in fw["blocks"]:
                    tally["TOTAL"] += 1
                    tally["AMBIGUOUS"] += 1
                    rows.append({
                        "file": fw["name"], "block_index": bi,
                        "status": "AMBIGUOUS",
                        "detail": "entry not found in walk"})
                continue
            # full closure attempt (search enabled; PE gid==0 invariant)
            try:
                res = v.decode_file(payload)
                closure_status = "CLOSURE_OK" if res else "NO_RESULT"
                tally["CLOSURE_OK"] += 1
            except Exception as ex:  # noqa: BLE001
                closure_status = "CLOSURE_FAIL"
                tally["CLOSURE_FAIL"] += 1
                closure_err = "%s: %s" % (type(ex).__name__,
                                          str(ex)[:120])
            else:
                closure_err = ""
            for bi in fw["blocks"]:
                tally["TOTAL"] += 1
                row = {"file": fw["name"], "block_index": bi,
                       "block_type": "NiSourceTexture",
                       "closure_status": closure_status}
                targets = set(fw["blocks"])
                max_target = max(targets)
                try:
                    cur = Cursor(payload)
                    hdr = v.parse_header(cur)
                    v._attempts = 0
                    recs = walk_partial(v, payload, targets, hdr, cur,
                                        0, max_target)
                except (Unresolved, ValueError, struct.error,
                        IndexError, UnicodeDecodeError) as ex:
                    recs = None
                    row["detail"] = "walk setup: %s: %s" % (
                        type(ex).__name__, str(ex)[:120])
                if recs is None or len(recs) != len(targets):
                    row["status"] = "FAIL"
                    row.setdefault(
                        "detail",
                        "partial walk did not reach all %d target "
                        "blocks (got %s)" % (
                            len(targets),
                            0 if recs is None else len(recs)))
                    tally["FAIL"] += 1
                    rows.append(row)
                    continue
                by_idx = {r["block_index"]: r for r in recs}
                rec = by_idx.get(bi)
                if rec is None:
                    row["status"] = "FAIL"
                    row["detail"] = "target block missing from record"
                    tally["FAIL"] += 1
                    rows.append(row)
                    continue
                row.update(rec)
                ue = rec.get("Use External")
                if ue == 1:
                    tally["EXTERNAL_BRANCH"] += 1
                elif ue == 0:
                    tally["INTERNAL_BRANCH"] += 1
                ngid = rec.get("next_GroupID")
                if ngid == "" or ngid == 0:
                    row["status"] = "PASS"
                    tally["PASS"] += 1
                else:
                    row["status"] = "FAIL"
                    row["detail"] = "next GroupID nonzero (%r)" % ngid
                    tally["FAIL"] += 1
                rows.append(row)

    out = os.path.join(REPO_RAW,
                       "NISOURCETEXTURE_FIELDIDENTITY_REGRESSION.csv")
    cols = ["file", "block_index", "block_type", "Use External",
            "Is Static", "file_name_branch", "File Name", "link_value",
            "link_target_type", "start_offset", "end_offset",
            "next_block_offset", "next_GroupID", "next_block_type",
            "closure_status", "status", "detail"]
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, restval="")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(json.dumps(tally))
    print("csv %s rows=%d" % (out, len(rows)))
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK,
                           "NISOURCETEXTURE_REGRESSION_SUMMARY.json"),
              "w", encoding="utf-8") as fh:
        json.dump({"tally": tally,
                   "files_with_st": [x["name"] for x in files_with_st],
                   "v10_1_files": n_v101}, fh, indent=2)
    # ASSERT denominators (COUNTER_ARITHMETIC per addendum E)
    assert tally["TOTAL"] == tally["PASS"] + tally["FAIL"] + \
        tally["AMBIGUOUS"], "denominator mismatch"
    assert tally["EXTERNAL_BRANCH"] + tally["INTERNAL_BRANCH"] + \
        sum(1 for r in rows if r.get("file_name_branch", "")
            .startswith("UNKNOWN")) == tally["TOTAL"], "branch mismatch"


if __name__ == "__main__":
    main()
