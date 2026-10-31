#!/usr/bin/env python3
"""RUN Stage C — DECODER A (implementation lineage: STRUCTURE-FIRST, Python).

Lineage declaration (G3 / QH-009): this decoder was derived from the
header-count-driven reading of the raw bytes: u16 count at offset +2 for
type-0 payloads (first u16 = 0), records of 36 bytes; and for type-1
payloads (u32@0 == 1) a vertex-block/triangle-block reading. It shares NO
field table with decoder B (Node, content/statistics-driven, independent).

Validations (fail loudly, not silently):
  type0: 4 + count*36 == payload_size  AND all 9 f32 per record finite
  type1: 12 + vcount*12 + 4 + tcount*12 <= payload_size, triangle indices
         < vcount, all vertex f32 finite

Negative controls (a) wrong-endian (b) truncated (c) wrong-width are executed
by this decoder on each sample and MUST FAIL (their failure output recorded).
"""
import struct, json, math, os, sys

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = ["506044.bvi", "105624.bvi", "506237.bvi", "584781.bvi"]


def load(name):
    return open(os.path.join(RUN, "01_RAW", "samples", name + ".bin"), "rb").read()


def finite_all(vals):
    return all(math.isfinite(v) for v in vals)


def decode_type0(payload, *, big_endian=False, width=4, truncate=None):
    """Header u16 count at +2, then count records of width*9 bytes (f32 x9)."""
    if truncate is not None:
        payload = payload[:truncate] if truncate >= 0 else payload[:len(payload) + truncate]
    en = ">" if big_endian else "<"
    if len(payload) < 4:
        return None, "FAIL truncated-header: payload < 4 bytes"
    count = struct.unpack_from(en + "H", payload, 2)[0]
    expected = 4 + count * width * 9
    if expected != len(payload):
        return None, (f"FAIL size-equation: 4 + {count}*{width}*9 = {expected} "
                      f"!= payload_size {len(payload)}")
    recs = []
    for i in range(count):
        off = 4 + i * width * 9
        vals = list(struct.unpack_from(en + "%df" % (width // 4 * 9), payload, off))
        if not finite_all(vals):
            return None, f"FAIL non-finite f32 in record {i}"
        recs.append(vals)
    return {"format": "type0", "u16_at_0": struct.unpack_from("<H", payload, 0)[0],
            "count": count, "records": recs}, None


def decode_type1(payload, *, big_endian=False, truncate=None, vwidth=12):
    """u32@0==1; u32@8 vcount; f32 verts x3; u32 tricount; u32 tri indices x3."""
    if truncate is not None:
        payload = payload[:truncate]
    en = ">" if big_endian else "<"
    if len(payload) < 12:
        return None, "FAIL truncated-header: payload < 12 bytes"
    t = struct.unpack_from(en + "I", payload, 0)[0]
    if t != 1:
        return None, f"FAIL type-word: u32@0 = {t} != 1"
    vcount = struct.unpack_from(en + "I", payload, 8)[0]
    vend = 12 + vcount * vwidth
    if vend + 4 > len(payload):
        return None, (f"FAIL vertex-block overrun: 12+{vcount}*{vwidth} = {vend} "
                      f"> payload_size {len(payload)}")
    ncomp = vwidth // 4
    raw = struct.unpack_from(en + "%df" % (vcount * ncomp), payload, 12)
    verts = list(raw)
    if not finite_all(verts):
        return None, "FAIL non-finite vertex f32"
    tcount = struct.unpack_from(en + "I", payload, vend)[0]
    tend = vend + 4 + tcount * 12
    if tend > len(payload):
        return None, (f"FAIL triangle-block overrun: {vend}+4+{tcount}*12 = {tend} "
                      f"> payload_size {len(payload)}")
    tris = list(struct.unpack_from(en + "%dI" % (tcount * 3), payload, vend + 4))
    if max(tris) >= vcount:
        return None, f"FAIL triangle index {max(tris)} >= vcount {vcount}"
    return {"format": "type1", "type_word": t, "u32_at_4": struct.unpack_from("<I", payload, 4)[0],
            "vcount": vcount, "vertex_f32_first9": verts[:9],
            "vertex_f32_min": min(verts), "vertex_f32_max": max(verts),
            "tricount": tcount, "tri_first15": tris[:15],
            "tail_bytes": len(payload) - tend}, None


def decode(payload, **kw):
    if len(payload) >= 4 and payload[0] == 0 and payload[1] == 0:
        return decode_type0(payload, **kw)
    if len(payload) >= 4 and struct.unpack_from("<I", payload, 0)[0] == 1:
        return decode_type1(payload, **kw)
    return None, "FAIL unknown-type word"


def main():
    out = {"impl": "A_python_structure_first", "samples": {}, "negative_controls": {}}
    for s in SAMPLES:
        p = load(s)
        res, err = decode(p)
        out["samples"][s] = {"ok": res is not None, "result": res, "error": err}

    # Negative controls — each must FAIL with recorded output.
    for s in SAMPLES:
        p = load(s)
        controls = {}
        r, e = decode(p, big_endian=True)
        controls["a_wrong_endian"] = {"failed": r is None, "output": e}
        r, e = decode(p, truncate=max(4, min(len(p) // 2, 24000)))
        controls["b_truncated"] = {"failed": r is None, "output": e}
        if p[:2] == b"\x00\x00":
            r, e = decode_type0(p, width=8)
            controls["c_wrong_width"] = {"failed": r is None, "output": e}
        else:
            r, e = decode_type1(p, vwidth=24)
            controls["c_wrong_width_f64_vertices"] = {"failed": r is None, "output": e}
        out["negative_controls"][s] = controls
    dest = os.path.join(RUN, "01_RAW", "DECODE_A.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({s: {"ok": v["ok"], "err": v["error"]} for s, v in out["samples"].items()}, indent=1))
    print("neg controls all failed:",
          all(c["failed"] for cs in out["negative_controls"].values() for c in cs.values()))


if __name__ == "__main__":
    main()
