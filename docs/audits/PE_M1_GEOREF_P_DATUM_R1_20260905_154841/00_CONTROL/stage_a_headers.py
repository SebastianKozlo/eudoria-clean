#!/usr/bin/env python3
"""PE_M1_GEOREF_P_DATUM_R1 stage A — the 9.3.5 terrain.bnt TDF-header census.
THE P-DATUM question: where does the runtime take the world georeference from
(datum/origin/anchoring)? The 9.3.5 terrain.bnt entries are SEQUENTIALLY named
(00000000.tdf..) -> unlike the 2003 50.bnt (filename-XY placement), the 9.3.5
tile placement MUST come from the TDF header fields. This census measures:
  @0-3 u32 x | @4-7 u32 y | @8-11 data_size | @12-15 dim
over ALL entries (bounded decompression: header-only via decompressobj).
Era: PCG 9.3.5. Read-only on the original file."""
import json
import os
import struct
import zlib
from collections import Counter

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GEOREF_P_DATUM_R1_20260905_154841"
SRC = r"D:\Eudoria_Reconstruction\pcg_install\Data\Terrain\terrain.bnt"
OUT = os.path.join(RUN, "01_RAW", "TERRAIN_935_HEADER_CENSUS.json")


def main():
    data = open(SRC, "rb").read()
    fs = len(data)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    # entries: 13-byte name + u32 packed + u32 offset (21 bytes)
    entries = []
    pos = istart + 4
    for _ in range(count):
        ne = pos
        while data[ne] != 0x0A:
            ne += 1
        nm = data[pos:ne].decode("ascii", "replace")
        sz, off = struct.unpack_from("<II", data, ne + 1)
        entries.append((nm, sz, off))
        pos = ne + 17
    print(f"entries: {len(entries)}")

    # trailer magic check (the BNT2 signature bytes at fs-4)
    trailer_magic = data[fs - 4: fs]
    print(f"trailer magic: {trailer_magic!r}")

    hdr = []
    bad = 0
    for i, (nm, sz, off) in enumerate(entries):
        marker = data[off:off + 4]
        if marker != b"\x02\x00\x00\xff":
            bad += 1
            if bad <= 5:
                print(f"  BAD MARKER @entry {i} {nm}: {marker.hex()}")
            continue
        dsize = struct.unpack_from("<I", data, off + 4)[0]
        d = zlib.decompressobj()
        h = d.decompress(data[off + 8: off + 8 + sz], 64)
        # h = up to 64 decompressed bytes
        if len(h) < 16:
            bad += 1
            continue
        x, y, dsz, dim = struct.unpack_from("<IIII", h, 0)
        hdr.append({"i": i, "name": nm, "x": x, "y": y, "data_size": dsz, "dim": dim})
        if (i + 1) % 10000 == 0:
            print(f"  {i+1}/{len(entries)}")

    xs = Counter(e["x"] for e in hdr)
    ys = Counter(e["y"] for e in hdr)
    dims = Counter((e["data_size"], e["dim"]) for e in hdr)
    out = {
        "file": SRC,
        "size": fs,
        "trailer_magic": trailer_magic.hex(),
        "count": count,
        "entries_parsed": len(hdr),
        "bad_entries": bad,
        "x": {"unique": len(xs), "min": min(xs) if xs else None,
              "max": max(xs) if xs else None},
        "y": {"unique": len(ys), "min": min(ys) if ys else None,
              "max": max(ys) if ys else None},
        "dim_size_classes": {f"dsz={k[0]},dim={k[1]}": v for k, v in dims.most_common(10)},
        "sample_first8": hdr[:8],
        "sample_last4": hdr[-4:],
        "grid_full": (len(xs) - 1) * (len(ys) - 1) if xs and ys else 0,
    }
    # pair-census: are (x,y) unique? duplicates?
    pairs = Counter((e["x"], e["y"]) for e in hdr)
    dups = {str(k): v for k, v in pairs.items() if v > 1}
    out["pair_duplicates"] = {"count": len(dups), "examples": dict(list(dups.items())[:5])}
    # cross-check: does header x/y correlate with the sequential name index?
    # sample: name-index vs header x/y for the first 12
    out["name_vs_header"] = [{"name": e["name"], "i": e["i"], "x": e["x"], "y": e["y"]}
                             for e in hdr[:12]]
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    # raw dump for stage D
    with open(os.path.join(RUN, "01_RAW", "TERRAIN_935_HEADERS.jsonl"), "w") as f:
        for e in hdr:
            f.write(json.dumps(e) + "\n")
    print(json.dumps({k: out[k] for k in ("count", "entries_parsed", "bad_entries",
                                         "x", "y", "dim_size_classes")}, indent=1))
    print(f"pair dups: {len(dups)}")
    print("written:", OUT)


if __name__ == "__main__":
    main()
