#!/usr/bin/env python3
"""PE_M1_P_CELLSTREAM_CLIMATE_R1 — the bounded offline census for queue item #4.
THE QUESTION (P-CELLSTREAM/P-CLIMATE): are the climate/cell-stream data local?
Canon (iter028): the 65x65 climate grid + the 129x129 detail grids are
patcher-delivered (non-local); the cell-content stream = server-delivered.
This run RE-VERIFIES the negatives fresh + documents the LOCAL anchors:
  (a) VegetationClimates.bnt (the .vcl climate DEFINITIONS — local);
  (b) the TDF 16x16 weight maps (the LOCAL per-tile climate-ish data);
  (c) the Parameters/*.vfs grid-absence divisibility scan;
  (d) the Textures\Terrain.bnt stub + the container-entry size negatives."""
import json
import struct
import zlib

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_P_CELLSTREAM_CLIMATE_R1_20260905_155533"
VC = r"D:\Eudoria_Reconstruction\pcg_install\Data\VegetationClimates\VegetationClimates.bnt"
PAR = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters"
TER = r"D:\Eudoria_Reconstruction\pcg_install\Data\Terrain\terrain.bnt"
STUB = r"D:\Eudoria_Reconstruction\pcg_install\Data\Textures\Terrain.bnt"


def main():
    out = {}

    # (d) the stub
    sb = open(STUB, "rb").read()
    out["stub_terrain_bnt"] = {"size": len(sb), "bytes": sb.hex(),
                               "trailer_BNT2": sb[-4:] == b"BNT2"}

    # (a) the .vcl decode
    d = open(VC, "rb").read()
    fs = len(d)
    istart = struct.unpack_from("<I", d, fs - 8)[0]
    count = struct.unpack_from("<I", d, istart)[0]
    pos = istart + 4
    entries = []
    for _ in range(count):
        ne = pos
        while d[ne] != 0x0A:
            ne += 1
        nm = d[pos:ne].decode("ascii", "replace")
        sz, off = struct.unpack_from("<II", d, ne + 1)
        entries.append((nm, sz, off))
        pos = ne + 17
    out["vcl_index"] = {"count": count, "sample": [e[0] for e in entries[:6]]}
    # the TSV structure: read the first .vcl payload (BNT2 raw entries, no zlib)
    nm, sz, off = entries[0]
    raw = d[off:off + sz]
    try:
        txt = raw.decode("ascii")
    except UnicodeDecodeError:
        try:
            txt = zlib.decompress(raw).decode("ascii")
        except Exception:
            txt = None
    if txt:
        lines = [l for l in txt.splitlines() if l.strip()]
        cols = [len(l.split("\t")) for l in lines]
        models = {l.split("\t")[0] for l in lines}
        out["vcl_first_entry"] = {
            "name": nm, "lines": len(lines),
            "columns_set": sorted(set(cols)),
            "unique_model_ids": len(models),
            "first_line": lines[0][:160],
        }
    # all entries: line counts
    all_txt = []
    for nm, sz, off in entries:
        raw = d[off:off + sz]
        try:
            t = raw.decode("ascii")
        except UnicodeDecodeError:
            try:
                t = zlib.decompress(raw).decode("ascii")
            except Exception:
                t = None
        all_txt.append((nm, len([l for l in t.splitlines() if l.strip()]) if t else None))

    # (c) the grid-absence scan: 65x65=4225, 129x129=16641 (+16B header variants)
    import os
    grid_hits = []
    for fn in sorted(os.listdir(PAR)):
        p = os.path.join(PAR, fn)
        n = os.path.getsize(p)
        for grid, label in ((4225, "65x65"), (16641, "129x129")):
            if n == grid or n == grid + 16 or (n - 16) % grid == 0:
                grid_hits.append({"file": fn, "size": n, "grid": label})
    out["parameters_grid_scan"] = {"files": len(os.listdir(PAR)), "hits": grid_hits}

    # Textures.bnt entry-size census for the grids (bounded: the index only)
    tex = open(r"D:\Eudoria_Reconstruction\pcg_install\Data\Textures\Textures.bnt", "rb").read()
    tfs = len(tex)
    tistart = struct.unpack_from("<I", tex, tfs - 8)[0]
    tcount = struct.unpack_from("<I", tex, tistart)[0]
    pos = tistart + 4
    tex_hits = []
    for _ in range(tcount):
        ne = pos
        while tex[ne] != 0x0A:
            ne += 1
        nm = tex[pos:ne].decode("ascii", "replace")
        sz, off = struct.unpack_from("<II", tex, ne + 1)
        if sz in (4225, 16641, 4225 + 18, 16641 + 18):
            tex_hits.append({"name": nm, "size": sz})
        pos = ne + 17
    out["textures_entry_grid_scan"] = {"count": tcount, "hits": tex_hits}

    # (b) the TDF weight maps: 3 sample tiles
    t = open(TER, "rb").read()
    tfs2 = len(t)
    ist2 = struct.unpack_from("<I", t, tfs2 - 8)[0]
    cnt2 = struct.unpack_from("<I", t, ist2)[0]
    pos = ist2 + 4
    e0 = None
    for _ in range(3):
        ne = pos
        while t[ne] != 0x0A:
            ne += 1
        nm = t[pos:ne].decode("ascii", "replace")
        sz, off = struct.unpack_from("<II", t, ne + 1)
        if e0 is None:
            e0 = (nm, sz, off)
        pos = ne + 17
    nm, sz, off = e0
    dsize = struct.unpack_from("<I", t, off + 4)[0]
    tile = zlib.decompress(t[off + 8:off + 8 + sz])
    w1 = struct.unpack_from("<I", tile, 2112)[0]
    w2 = struct.unpack_from("<I", tile, 2116)[0]
    wm = tile[2120:2120 + 256]
    out["tdf_weight_map"] = {"tile": nm, "decompressed": len(tile),
                             "field_2112": w1, "field_2116": w2,
                             "weightmap_16x16_first16": list(wm[:16]),
                             "structure_matches_M1": (w1 == 308 and w2 == 16)}

    with open(f"{RUN}\\01_RAW\\CELLSTREAM_CLIMATE_CENSUS.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=1)[:2200])


if __name__ == "__main__":
    main()
