#!/usr/bin/env python3
"""QC DUTY 2 (part 2) — INDEPENDENT BNT2 index relation derivation for model 218757.

Fresh internal QC (pe-master-auditor, fresh session). This is my OWN reader,
written from the physical footer/index structure of the pinned Models.bnt,
NOT a copy of the executor's s01 walker. Read-only against Models.bnt.

Method:
  1. Read the last 8 bytes: u32 dir_offset + magic 'BNT2' (validate magic).
  2. Seek dir_offset, read u32 count.
  3. For each entry: ASCII name up to 0x0A terminator, then 16-byte record
     (u32 size, u32 offset, u32 f3, u32 f4).
  4. Fail-closed validation: bounds, duplicates, EOF-exactness, overlaps.
  5. Find every entry whose name matches ^218757$ and every entry whose
     payload SHA256 equals the pin — AMBIGUITY CHECK (is the relation unique?).
  6. Cross-check historical values: ordinal 781, payload offset 116223520,
     length 57316, name byte offset 395283797 (cross-checks, not authority).
  7. Fresh-extract the winning range to the QC sandbox (LOCAL_ONLY copy under
     00_CONTROL_INTERNAL_QC), hash it, and byte-compare against the pinned
     218757.nif.
"""
import hashlib
import json
import struct
import sys

BNT = "D:/Eudoria_Reconstruction/pcg_install/Data/Models/Models.bnt"
PIN = ("D:/Eudoria_Reconstruction/99_Audits/"
       "PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/sandbox/payloads/218757.nif")
OUT = ("D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/"
       "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/"
       "00_CONTROL_INTERNAL_QC/q2_218757_relation.json")

PIN_SIZE = 57316
PIN_SHA = "3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36"
XCHECK = {"ordinal": 781, "offset": 116223520, "length": 57316,
          "name_offset": 395283797}


class QCError(Exception):
    pass


def u32(buf, off):
    return struct.unpack_from("<I", buf, off)[0]


def derive():
    f = open(BNT, "rb")
    try:
        f.seek(0, 2)
        fsize = f.tell()
        f.seek(fsize - 8)
        tail = f.read(8)
        if tail[4:8] != b"BNT2":
            raise QCError(f"magic mismatch: {tail[4:8]!r}")
        dir_off = u32(tail, 0)
        if not (0 < dir_off < fsize - 8):
            raise QCError(f"dir_off out of range: {dir_off}")
        f.seek(dir_off)
        count = u32(f.read(4), 0)
        if not (0 < count < 10_000_000):
            raise QCError(f"count insane: {count}")

        entries = []
        names = {}
        while True:
            name_off_in_file = f.tell()          # byte offset of THIS name
            name = bytearray()
            while True:
                c = f.read(1)
                if not c:
                    raise QCError("EOF inside name")
                if c == b"\x0A":
                    break
                name += c
                if len(name) > 300:
                    raise QCError("name too long")
            rec = f.read(16)
            if len(rec) != 16:
                raise QCError("short entry record")
            size, off, f3, f4 = struct.unpack("<IIII", rec)
            nm = name.decode("ascii")
            entries.append({
                "ordinal": len(entries), "name": nm,
                "file_byte_offset_of_name": name_off_in_file,
                "size": size, "offset": off, "f3": f3, "f4": f4,
            })
            if nm in names:
                raise QCError(f"duplicate name {nm!r}")
            names[nm] = len(entries) - 1
            if len(entries) == count:
                break

        # EOF-exactness: index must end exactly at fsize-8
        if f.tell() != fsize - 8:
            raise QCError(f"index end {f.tell()} != {fsize-8}")

        # bounds + overlap
        order = sorted(entries, key=lambda e: e["offset"])
        prev_end = 0
        for e in order:
            if e["size"] == 0:
                raise QCError(f"zero size {e['name']}")
            if e["offset"] + e["size"] > dir_off:
                raise QCError(f"OOB {e['name']}")
            if e["offset"] < prev_end:
                raise QCError(f"overlap {e['name']}")
            prev_end = e["offset"] + e["size"]

        # ambiguity check A: name stem matches 218757 (file name is
        # '218757.nif' per physical bytes; sweep ANY name containing 218757)
        by_name = [e for e in entries if "218757" in e["name"]]
        # ambiguity check B: any OTHER entry sharing the same payload range
        by_range = [e for e in entries
                    if e["offset"] == XCHECK["offset"]
                    and e["size"] == XCHECK["length"]]
        # ambiguity check C: payload SHA equality across a name-suffix sweep
        # (only hash candidates whose declared size == PIN_SIZE; hashing all
        # 5596 payloads would be slow, same-size is a sound ambiguity filter)
        same_size_hits = []
        for e in entries:
            if e["size"] == PIN_SIZE:
                f.seek(e["offset"])
                blob = f.read(e["size"])
                if hashlib.sha256(blob).hexdigest() == PIN_SHA:
                    same_size_hits.append(e["ordinal"])

        return f, entries, by_name, by_range, same_size_hits, dir_off, fsize
    except Exception:
        f.close()
        raise


def main():
    (f, entries, by_name, by_range,
     same_size_hits, dir_off, fsize) = derive()
    try:
        res = {
            "qc_tool": "qc2_218757_index_derivation.py (independent "
                       "pe-master-auditor reader)",
            "bnt": BNT,
            "bnt_size": fsize,
            "bnt_sha_declared": "c950a8c26f2063f4dd748d88"
                                "c95bd769aac77a2f5f76face7e969be0b3d3bee0",
            "dir_offset": dir_off,
            "num_entries": len(entries),
            "crosschecks": XCHECK,
            "by_name_218757": [
                {"ordinal": e["ordinal"], "name": e["name"],
                 "size": e["size"], "offset": e["offset"],
                 "f3": e["f3"], "f4": e["f4"],
                 "name_file_offset": e["file_byte_offset_of_name"]}
                for e in by_name],
            "same_range_as_xcheck": [e["ordinal"] for e in by_range],
            "same_size_sha_pin_hits": same_size_hits,
        }
        if len(by_name) != 1:
            res["verdict"] = "AMBIGUOUS_NAME"
            print(json.dumps(res, indent=2))
            return 1
        win = by_name[0]

        # fresh extraction
        f.seek(win["offset"])
        blob = f.read(win["size"])
        res["extracted_size"] = len(blob)
        res["extracted_sha256"] = hashlib.sha256(blob).hexdigest()

        # byte identity with pin
        with open(PIN, "rb") as pf:
            pin_blob = pf.read()
        res["pin_size_actual"] = len(pin_blob)
        res["byte_identical_to_pin"] = blob == pin_blob
        res["pin_sha_declared"] = PIN_SHA

        # cross-check verdicts
        res["xcheck_ordinal_match"] = win["ordinal"] == XCHECK["ordinal"]
        res["xcheck_offset_match"] = win["offset"] == XCHECK["offset"]
        res["xcheck_length_match"] = win["size"] == XCHECK["length"]
        res["xcheck_name_offset_match"] = (
            win["file_byte_offset_of_name"] == XCHECK["name_offset"])
        res["ambiguity"] = {
            "distinct_entries_with_218757_in_name": len(by_name),
            "entries_sharing_declared_range": len(by_range),
            "same_size_payloads_with_pin_sha": len(same_size_hits),
        }
        res["verdict"] = "UNIQUE_DERIVATION_OK" if (
            res["byte_identical_to_pin"]
            and res["xcheck_ordinal_match"]
            and res["xcheck_offset_match"]
            and res["xcheck_length_match"]
            and res["xcheck_name_offset_match"]
            and len(same_size_hits) == 1
        ) else "MISMATCH"
        print(json.dumps(res, indent=2))
        with open(OUT, "w", encoding="utf-8") as o:
            json.dump(res, o, indent=2)
        return 0
    finally:
        f.close()


if __name__ == "__main__":
    sys.exit(main())
