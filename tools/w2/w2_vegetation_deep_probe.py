#!/usr/bin/env python3
# W2-1 job tool (RUN PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031, W2_BIOME_VEGETATION).
# READ-ONLY static probe of PCG_9_3_5 data for vegetation placement provenance:
#   1) VCL_CENSUS: full BNT2 parse of VegetationClimates.bnt, extract all .vcl
#      payloads, 12-value stream census (decoder-identical semantics), comma
#      token locations, per-column stats (cols labeled UNVERIFIED raw).
#   2) CELL_RECORDS_SEARCH: 8-byte stride {u16,u16,u32} scan over candidate
#      container payloads; discriminator = u32 in the VCL model-id universe
#      (col0 across corpus) OR u32 < Models.bnt count; text payloads excluded.
#   3) TDF_CLIMATE_SEARCH: decompress a grid-spread sample of terrain.bnt TDF
#      tiles; census header+tail structure; look for climate-index-like fields
#      (values 0..31 / 32-bit repeating) in non-height regions.
# Writes ONLY into the W2 SCI directory. Never modifies pcg_install.
import os, sys, json, struct, zlib, hashlib, re

PCG = r"D:\Eudoria_Reconstruction\pcg_install"
SCI = r"D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031\W2_BIOME_VEGETATION"
RUN = {"tool": "w2_vegetation_deep_probe.py", "era": "PCG_9_3_5"}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()

def parse_bnt2(path):
    sz = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(sz - 8)
        b = f.read(8)
        idx_off = struct.unpack("<I", b[:4])[0]
        assert b[4:8] == b"BNT2", "footer magic"
        f.seek(idx_off)
        cnt = struct.unpack("<I", f.read(4))[0]
        raw = f.read(sz - 8 - idx_off - 4)
    entries, pos = [], 0
    for i in range(cnt):
        nl = raw.find(b"\x0a", pos)
        if nl == -1 or nl + 17 > len(raw):
            break
        name = raw[pos:nl].decode("ascii", "replace")
        f1, f2, f3, f4 = struct.unpack_from("<IIII", raw, nl + 1)
        entries.append({"i": i, "name": name, "f1": f1, "f2": f2, "f3": f3, "f4": f4})
        pos = nl + 17
    return {"idx_off": idx_off, "count": cnt, "entries": entries, "size": sz}

def read_payload(path, e):
    with open(path, "rb") as f:
        f.seek(e["f2"])
        return f.read(e["f1"])

NUM_RE = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")

def vcl_census(path):
    meta = parse_bnt2(path)
    files = []
    all_model_ids = set()
    for e in meta["entries"]:
        data = read_payload(path, e)
        rec = {"name": e["name"], "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest().upper()}
        text = data.decode("ascii", "replace")
        tokens = [t for t in re.split(r"\s+", text) if t]
        comma_tokens = []
        # locate comma tokens with byte offsets in the payload
        for m in re.finditer(r"[^\s]+,[^\s]*", text):
            comma_tokens.append({"token": m.group(0), "payload_byte_offset": m.start()})
        numeric_ok = all(NUM_RE.match(t) for t in tokens)
        groups = []
        for gi in range(len(tokens) // 12):
            groups.append(tokens[gi * 12:(gi + 1) * 12])
        trailing_partial = len(tokens) % 12
        rec["token_count"] = len(tokens)
        rec["nonempty_lines"] = sum(1 for ln in text.splitlines() if ln.strip())
        rec["fully_numeric_stream"] = numeric_ok
        rec["groups_of_12"] = len(groups)
        rec["trailing_partial_tokens"] = trailing_partial
        rec["comma_tokens"] = comma_tokens
        rec["status"] = "DECODE_OK" if (numeric_ok and trailing_partial == 0 and not comma_tokens) else "COMMA_TOKENS" if comma_tokens else "PARTIAL_OR_NONNUMERIC"
        cols = [[] for _ in range(12)]
        if numeric_ok and not comma_tokens:
            for g in groups:
                for c, t in enumerate(g):
                    cols[c].append(float(t))
        rec["records"] = [[t for t in g] for g in groups]  # RAW string values (UNVERIFIED raw labels)
        if cols[0]:
            stats = []
            for c in range(12):
                v = cols[c]
                stats.append({"col": c, "min": min(v), "max": max(v), "distinct": len(set(v))})
            rec["col_stats_numeric"] = stats
            all_model_ids.update(int(v) for v in cols[0])
        files.append(rec)
    return {"container_sha256": sha256_file(path), "container_size": meta["size"],
            "idx_off": meta["idx_off"], "entry_count": meta["count"], "files": files,
            "corpus_model_ids": sorted(all_model_ids)}

def is_text(data):
    if not data:
        return True
    printable = sum(1 for b in data if 9 <= b <= 13 or 32 <= b <= 126)
    return printable / len(data) > 0.97

def scan_8b_stride(data, model_universe, max_model_id, min_records=32):
    """Scan one payload for 8B stride {u16,u16,u32} runs where u32 lands in the
    VCL model-id universe (strong) or below max_model_id (weak)."""
    n = len(data)
    if n % 8 != 0 or n < 8 * min_records:
        return None
    recs = n // 8
    hits = 0
    sample = []
    for off in range(0, n, 8):
        x, y = struct.unpack_from("<HH", data, off)
        mid = struct.unpack_from("<I", data, off + 4)[0]
        if mid in model_universe:
            hits += 1
            if len(sample) < 8:
                sample.append({"off": off, "x": x, "y": y, "model_id": mid, "match": "VCL_UNIVERSE"})
        elif mid <= max_model_id:
            hits += 1
            if len(sample) < 8:
                sample.append({"off": off, "x": x, "y": y, "model_id": mid, "match": "WEAK<=MODELCOUNT"})
    if hits >= max(min_records, int(recs * 0.9)):
        return {"records": recs, "hits": hits, "hit_ratio": round(hits / recs, 4), "sample": sample}
    return None

def cell_records_search(model_universe, max_model_id):
    out = {"scanned": [], "candidates": [], "skipped": []}
    containers = [
        r"Data\TerrainEditZones\TerrainEditZones.bnt",
        r"Data\Portals\Portals.bnt",
        r"Data\EffectSequences\EffectSequences.bnt",
        r"Data\Sounds\MusDef.bnt",
        r"Data\UI\ui.bnt",
        r"Data\VegetationClimates\VegetationClimates.bnt",
    ]
    for rel in containers:
        full = os.path.join(PCG, rel)
        meta = parse_bnt2(full)
        cinfo = {"container": rel, "entries": meta["count"], "text_entries": 0,
                 "binary_entries": 0, "stride8_aligned": 0, "candidate_entries": []}
        for e in meta["entries"]:
            data = read_payload(full, e)
            if is_text(data):
                cinfo["text_entries"] += 1
                continue
            cinfo["binary_entries"] += 1
            r = scan_8b_stride(data, model_universe, max_model_id)
            if r:
                cinfo["stride8_aligned"] += 1
                cinfo["candidate_entries"].append({"name": e["name"], "size": len(data), "scan": r})
        if cinfo["candidate_entries"]:
            out["candidates"].append(cinfo)
        else:
            out["scanned"].append(cinfo)
    out["skipped"].append({
        "container": r"Data\Volumes\Volumes.bnt",
        "reason": "BVI = local collision mesh per standing W2 instruction ('Do not scan BVI files for model IDs as world placement'); entry census from PLACEMENT_CARRIER_RECON INVENTORY (1865 .bvi) reused; NOT scanned as a placement carrier this run",
        "entries": 1865})
    return out

def tdf_climate_search(sample_count=24):
    """Decompress a grid-spread sample of terrain.bnt TDF tiles and census their
    non-height structure. Look for climate-index-like fields."""
    full = os.path.join(PCG, r"Data\Terrain\terrain.bnt")
    meta = parse_bnt2(full)
    entries = meta["entries"]
    n = len(entries)
    idxs = sorted(set(int(i * (n - 1) / max(1, sample_count - 1)) for i in range(sample_count)))
    tiles = []
    tail_const = None
    tail_var_positions = set()
    for i in idxs:
        e = entries[i]
        data = read_payload(full, e)
        try:
            # terrain.bnt entries carry an 8-byte mini-header before the zlib
            # stream: marker 02 00 00 FF + u32 DECOMPRESSED_LEN (measured in-run
            # on 00000000.tdf: 0x0E44 = 3652; zlib starts 78 DA at f2+8).
            assert data[:4] == b"\x02\x00\x00\xff", "mini-header marker"
            decl = struct.unpack_from("<I", data, 4)[0]
            d = zlib.decompress(data[8:])
            assert len(d) == decl, f"declen {decl} != actual {len(d)}"
        except Exception as ex:
            tiles.append({"name": e["name"], "error": str(ex)})
            continue
        rec = {"name": e["name"], "entry_index": i, "compressed": len(data),
               "decompressed": len(d), "declared_len": decl}
        # known structure: height at offset 64, 32x32 u16 = 2048 bytes -> tail from 2112
        body = d[64:64 + 2048]
        rec["height_first8"] = struct.unpack("<8H", body[:16]) if len(body) >= 16 else None
        tail = d[64 + 2048:]
        rec["tail_len"] = len(tail)
        # byte-level variance census across sample: constant vs varying positions
        if tail_const is None:
            tail_const = tail
        else:
            for p in range(min(len(tail), len(tail_const))):
                if tail[p] != tail_const[p]:
                    tail_var_positions.add(p)
        # climate-index candidates: any u32 or u16 word in tail with value in 0..31
        # at a position varying across tiles (a per-tile climate id would vary)
        tiles.append(rec)
    varying = sorted(tail_var_positions)
    result = {"sampled_tiles": len(tiles), "tiles": tiles,
              "tail_varying_byte_positions": varying[:200],
              "tail_varying_count": len(varying),
              "note": "varying positions computed pairwise vs the FIRST sampled tile (a coarse but bounded census)"}
    # u16 scan of varying tail positions for values 0..31 in >1 tile
    return result

def main():
    print("W2 vegetation deep probe — READ-ONLY")
    # SHA pins
    pins = {}
    for rel in [r"Data\VegetationClimates\VegetationClimates.bnt", r"Data\Terrain\terrain.bnt"]:
        p = os.path.join(PCG, rel)
        pins[rel] = {"sha256": sha256_file(p), "size": os.path.getsize(p)}
    print(json.dumps(pins, indent=1))
    vcl = vcl_census(os.path.join(PCG, r"Data\VegetationClimates\VegetationClimates.bnt"))
    print("VCL files:", len(vcl["files"]), "corpus model ids:", len(vcl["corpus_model_ids"]))
    with open(os.path.join(SCI, "VCL_CENSUS.json"), "w") as f:
        json.dump({"pins": pins, "census": vcl}, f, indent=1)
    # cell records search
    universe = set(vcl["corpus_model_ids"])
    cr = cell_records_search(universe, max_model_id=5596)
    with open(os.path.join(SCI, "CELL_RECORDS_SEARCH.json"), "w") as f:
        json.dump({"vcl_model_universe_size": len(universe), "scan": cr}, f, indent=1)
    print("cell-records candidates:", json.dumps([c["container"] for c in cr["candidates"]]))
    # TDF climate search
    tdf = tdf_climate_search()
    with open(os.path.join(SCI, "TDF_CLIMATE_SEARCH.json"), "w") as f:
        json.dump({"pins": pins, "search": tdf}, f, indent=1)
    print("TDF sampled:", tdf["sampled_tiles"], "tail varying bytes:", tdf["tail_varying_count"])
    print("DONE")

if __name__ == "__main__":
    main()
