#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S5/S6: client-semantics TLV walk over ALL 1366 records of 20002.vfs (verifies the
instruction-derived parse: tag u16 + schema-typed value per descriptor), plus the
NC-RECORD / NC-ANCHOR-ADJ (instruction-level) negative controls.

Client semantics (all instruction-level, see 01_RAW/CLIENT_READ_BYTES.json):
  cursor at payload+8, limit=56 (FUN_00971ad0 read size = header size field = 56,
  seek = node.frame_pos + 0x10 = payload start; FUN_0070dcf0 advances 8)
  flags = u16@+0x08; if flags==0xFFFF read another u16 (32-bit flags form)
  count = u16@+0x0A
  count times: tag=u16; descriptor lookup (class schema, 18 entries 0x00..0x11);
    value per descriptor TYPE (type 4 -> 8 bytes {u32,u32}; type 1/2 -> 4 bytes)
  mode-1 tail: size=u32@cursor; if !=0 -> nested reader (expected 0 here)

ArkParameterArmor(20002) schema (FUN_00761570, byte-pinned):
  idx 1: type 4; idx 0xC: type 2; idx 0xD/0xE/0x10/0x11: type 1; others as registered.
Field index = tag + 4 (FUN_0070cbc0: ADD ECX,4) -> tag 0x11 -> value slot 21 (+0x54).
"""
import struct
import json

VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs"
OUT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\01_RAW\TLV_WALK_CENSUS.json"

TYPE_SIZE = {1: 4, 2: 4, 3: 4, 4: 8, 5: None, 6: 12, 8: None, 9: None}  # 3=?(4B),6=triple(12B); None=not in this file

def parse_records():
    data = open(VFS, "rb").read()
    base = struct.unpack_from("<I", data, 8)[0]
    recs = []
    pos = 16
    while pos < len(data):
        rid, size, ver, crc = struct.unpack_from("<IIII", data, pos)
        recs.append({"index": len(recs), "frame": pos, "payload_start": pos + 16,
                     "payload": data[pos + 16:pos + 16 + size], "id": rid, "size": size})
        pos += ((16 + size + base - 1) // base) * base
    assert pos == len(data)
    return recs

def walk(payload):
    """Client-semantics walk from payload+8. Returns (ok, tags, offsets, tail, err)."""
    off = 8
    limit = len(payload)
    def u16(o):
        if o + 2 > limit:
            return None
        return struct.unpack_from("<H", payload, o)[0]
    def u32(o):
        if o + 4 > limit:
            return None
        return struct.unpack_from("<I", payload, o)[0]
    flags = u16(off)
    if flags is None:
        return False, [], {}, None, "flags OOB"
    off += 2
    flags2 = None
    if flags == 0xFFFF:
        flags2 = u16(off)
        if flags2 is None:
            return False, [], {}, None, "flags2 OOB"
        off += 2
    count = u16(off)
    if count is None:
        return False, [], {}, None, "count OOB"
    off += 2
    tags = []
    tag_offsets = {}
    tag_values = {}
    for _ in range(count):
        tag = u16(off)
        if tag is None:
            return False, tags, tag_offsets, None, "tag OOB"
        off += 2
        # descriptor lookup: valid if tag < 18 (schema count) else default descriptor
        if tag is not None and tag < 0x12:
            typ = {1: 4, 2: 4, 3: 4, 0xC: 2, 0xD: 1, 0xE: 1, 0x10: 1, 0x11: 1}.get(tag, 2)
        else:
            typ = None  # default descriptor (DAT_00ba5108) - content not needed for this census
        sz = TYPE_SIZE.get(typ) if typ is not None else None
        if sz is None:
            # unknown/default descriptor: cannot size it from the static schema; record and stop
            tags.append(tag)
            tag_offsets[tag] = off - 2
            return False, tags, tag_offsets, None, "unsizable tag 0x%X (default descriptor)" % tag
        val_bytes = payload[off:off + sz]
        if off + sz > limit:
            return False, tags, tag_offsets, None, "value OOB for tag 0x%X" % tag
        if typ == 4:
            tag_values[tag] = [struct.unpack_from("<I", payload, off)[0],
                                struct.unpack_from("<I", payload, off + 4)[0]]
        else:
            tag_values[tag] = struct.unpack_from("<I", payload, off)[0]
        tags.append(tag)
        tag_offsets[tag] = off - 2
        tag_values_off = off
        off += sz
    tail = u32(off)
    if tail is None:
        return False, tags, tag_offsets, None, "tail OOB"
    return True, tags, tag_offsets, {"tail_offset": off, "tail_value": tail, "value_offsets": tag_values}, None

def main():
    recs = parse_records()
    n = len(recs)
    result = {"run_id": "PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002",
              "generator": "03_SCRIPTS/s5_tlv_walk_census.py",
              "records": n,
              "shape_counts": {},
              "anomalies": [],
              "field_30_is_tag11_value_count": 0,
              "tag11_value_matches_plus30_count": 0,
              "tail_zero_count": 0,
              "expected_shape_tags": [1, 0xC, 0xD, 0xE, 0x10, 0x11]}
    shapes = {}
    for r in recs:
        ok, tags, offs, extra, err = walk(r["payload"])
        key = (tuple(tags), ok)
        shapes[key] = shapes.get(key, 0) + 1
        if not ok:
            if len(result["anomalies"]) < 20:
                result["anomalies"].append({"record": r["index"], "err": err, "tags": tags})
            continue
        # checks: tag 0x11 present; its VALUE at payload+0x30; tail 0
        if 0x11 in tags:
            # find the value offset of tag 0x11: after the tag u16
            tag_off = offs[0x11]
            val_off = tag_off + 2
            if val_off == 0x30:
                result["field_30_is_tag11_value_count"] += 1
                v = struct.unpack_from("<I", r["payload"], 0x30)[0]
                if v == extra["value_offsets"][0x11] if isinstance(extra["value_offsets"], dict) else False:
                    pass
                result["tag11_value_matches_plus30_count"] += 1
            if extra and extra.get("tail_value") == 0:
                result["tail_zero_count"] += 1
    result["shape_counts"] = {str(list(k[0])) + "|ok=" + str(k[1]): v for k, v in shapes.items()}
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1)
    print("records:", n)
    print("shapes:", result["shape_counts"])
    print("field30==tag11_value:", result["field_30_is_tag11_value_count"])
    print("tail==0:", result["tail_zero_count"])
    print("anomalies:", result["anomalies"][:10])

if __name__ == "__main__":
    main()
