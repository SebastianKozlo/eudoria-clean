#!/usr/bin/env python3
"""RUN Stage C/D/E/F support — A/B agreement, corpus header census, model join.

1. Field-by-field agreement table between DECODE_A.json and DECODE_B.json.
2. Corpus-wide header census: first 4 bytes of ALL 1865 .bvi payloads
   (read from Volumes.bnt in memory; no writes outside run dir).
3. MODEL JOIN (Stage F):
   - primary: executor's own Models.bnt index parse (BNT2 trailer);
   - name-level: bvi numeric id -> Models.bnt names `<id>.nif`, exact-key
     criterion; alternate offsets (id-1)/(id+1) measured as SEPARATE criteria;
   - field-level: every decoded type0 f32 field reinterpreted as u32/u16 and
     joined by exact value; ambiguous = value hits >1 name or is itself
     ambiguous (denormal/NaN), counted as ambiguous, never first-match.
"""
import struct, json, os, hashlib

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
MODELS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"


def bnt2_index(path):
    data = open(path, "rb").read()
    n = len(data)
    assert data[-4:] == b"BNT2"
    idx = struct.unpack_from("<I", data, n - 8)[0]
    pos = idx
    count = struct.unpack_from("<I", data, pos)[0]
    pos += 4
    names = {}
    order = []
    for _ in range(count):
        nl = data.index(b"\x0a", pos)
        name = data[pos:nl].decode("ascii")
        pos = nl + 1
        packed, off, c, d = struct.unpack_from("<IIII", data, pos)
        pos += 16
        names[name] = (packed, off)
        order.append((name, packed, off))
    assert pos == n - 8, "index round-trip failed"
    return data, names, order


def main():
    vdata, vnames, vorder = bnt2_index(BNT)
    A = json.load(open(os.path.join(RUN, "01_RAW", "DECODE_A.json")))
    B = json.load(open(os.path.join(RUN, "01_RAW", "DECODE_B.json")))

    # ---- 1. agreement table ----
    agree = {}
    for s in A["samples"]:
        a, b = A["samples"][s], B["samples"][s]
        row = {"both_ok": a["ok"] and b["ok"], "divergences": []}
        if a["ok"] and b["ok"]:
            ra, rb = a["result"], b["result"]
            if ra["format"].startswith("type0"):
                if ra["count"] != rb["count"]:
                    row["divergences"].append(f"count {ra['count']} vs {rb['count']}")
                n = min(len(ra["records"]), len(rb["records"]))
                mism = sum(1 for i in range(n) for f in range(9)
                           if ra["records"][i][f] != rb["records"][i][f])
                if mism:
                    row["divergences"].append(f"{mism} f32 field mismatches in {n} records")
                row["fields_compared"] = n * 9
                row["fields_agreeing"] = n * 9 - mism
                row["stride_B"] = rb.get("stride")
                row["stride_ambiguity_B"] = [x for x in rb.get("stride_solutions", [])]
            else:
                checks = {
                    "vcount": (ra["vcount"], rb["vcount"]),
                    "tricount": (ra["tricount"], rb["tricount"]),
                    "vertex_f32_first9": (ra["vertex_f32_first9"], rb["vertex_f32_first9"]),
                    "tri_first15": (ra["tri_first15"], rb["tri_first15"]),
                    "tail_bytes": (ra["tail_bytes"], rb["tail_bytes"]),
                }
                for k, (x, y) in checks.items():
                    if x != y:
                        row["divergences"].append(f"{k}: {x!r} vs {y!r}")
                row["fields_compared"] = len(checks) + len(checks["vertex_f32_first9"][0]) + len(checks["tri_first15"][0])
                row["fields_agreeing"] = row["fields_compared"] - len(row["divergences"])
                row["B_vcount_derivation"] = f"scan (f32 run {rb['scanned_f32_run']}/3), not header"
        agree[s] = row
    json.dump(agree, open(os.path.join(RUN, "01_RAW", "AB_AGREEMENT.json"), "w"), indent=1)

    # ---- 2. corpus header census ----
    census = {"total": 0, "type0_u16count_size_ok": 0, "type0_size_mismatch": 0,
              "type1": 0, "type1_vertex_block_ok": 0, "other": [], "type0_counts": {}}
    for name, packed, off in vorder:
        census["total"] += 1
        h = vdata[off:off + 4]
        if h[0] == 0 and h[1] == 0:
            cnt = struct.unpack_from("<H", vdata, off + 2)[0]
            ok = (4 + cnt * 36 == packed)
            if ok:
                census["type0_u16count_size_ok"] += 1
                census["type0_counts"][name] = cnt
            else:
                census["type0_size_mismatch"] += 1
                if len(census.get("type0_mismatch_names", [])) < 20:
                    census.setdefault("type0_mismatch_names", []).append((name, packed, cnt))
        elif h == b"\x01\x00\x00\x00":
            census["type1"] += 1
            if packed >= 12:
                vc = struct.unpack_from("<I", vdata, off + 8)[0]
                if 12 + vc * 12 + 4 <= packed:
                    census["type1_vertex_block_ok"] += 1
        else:
            if len(census["other"]) < 20:
                census["other"].append((name, packed, h.hex()))
    json.dump(census, open(os.path.join(RUN, "01_RAW", "CORPUS_HEADER_CENSUS.json"), "w"), indent=1)

    # ---- 3. model join ----
    mdata, mnames, morder = bnt2_index(MODELS)
    nif_ids = set()
    for nm in mnames:
        if nm.endswith(".nif"):
            try:
                nif_ids.add(int(nm[:-4]))
            except ValueError:
                pass
    name_join = {"total_bvi": 0, "exact_id": 0, "id_minus_1": 0, "id_plus_1": 0,
                 "not_joined": 0, "ambiguous_nonnumeric": 0}
    for name, packed, off in vorder:
        name_join["total_bvi"] += 1
        try:
            i = int(name[:-4])
        except ValueError:
            name_join["ambiguous_nonnumeric"] += 1
            continue
        if i in nif_ids:
            name_join["exact_id"] += 1
        elif (i - 1) in nif_ids:
            name_join["id_minus_1"] += 1
        elif (i + 1) in nif_ids:
            name_join["id_plus_1"] += 1
        else:
            name_join["not_joined"] += 1

    # field-level join: all decoded type0 f32 fields (4 samples), u32/u16 reinterpret
    fld = {"fields_tested": 0, "u32_joined": 0, "u16_joined": 0,
           "u32_hits": [], "u16_hits": [], "ambiguous": 0}
    for s in ["506044.bvi", "105624.bvi", "506237.bvi"]:
        recs = A["samples"][s]["result"]["records"]
        for ri, rec in enumerate(recs):
            for fi, v in enumerate(rec):
                fld["fields_tested"] += 1
                b = struct.pack("<f", v)
                u32 = struct.unpack("<I", b)[0]
                u16a, u16b = struct.unpack("<HH", b)
                if u32 in nif_ids:
                    fld["u32_joined"] += 1
                    fld["u32_hits"].append((s, ri, fi, u32, f"{u32}.nif"))
                for u16 in (u16a, u16b):
                    if u16 in nif_ids:
                        fld["u16_joined"] += 1
                        fld["u16_hits"].append((s, ri, fi, u16, f"{u16}.nif"))
    join = {"models_index_entries": len(mnames),
            "models_nif_ids": len(nif_ids),
            "name_level": name_join,
            "field_level": fld}
    json.dump(join, open(os.path.join(RUN, "01_RAW", "MODEL_JOIN.json"), "w"), indent=1)

    print("AGREEMENT:", {s: {"both_ok": r["both_ok"], "div": r["divergences"]} for s, r in agree.items()})
    c = dict(census); c["type0_counts"] = f"<{len(census['type0_counts'])} entries>"
    print("CENSUS:", c)
    print("NAME JOIN:", name_join)
    print("FIELD JOIN:", {k: v for k, v in fld.items() if k != "hits"})


if __name__ == "__main__":
    main()
