#!/usr/bin/env python3
"""PE_M1_GEOREF_P_DATUM_R1 — the geo-source census (offline, read-only).
Files: Volumes.bnt / TerrainEditZones.bnt / terrain.bnt / Textures.bnt(height tex 429259)
Era: PCG 9.3.5 (primary) + the D:\Entropia Universe 2008-era comparison copies.
Every read read-only; every claim hash-backed."""
import hashlib
import json
import struct
import os

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_GEOREF_P_DATUM_R1_20260905_154841"
OUT = os.path.join(RUN, "01_RAW", "GEO_SOURCE_CENSUS.json")

FILES = {
    "volumes_935": r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt",
    "terraineditzones_935": r"D:\Eudoria_Reconstruction\pcg_install\Data\TerrainEditZones\TerrainEditZones.bnt",
    "terrain_935": r"D:\Eudoria_Reconstruction\pcg_install\Data\Terrain\terrain.bnt",
    "textures_935": r"D:\Eudoria_Reconstruction\pcg_install\Data\Textures\Textures.bnt",
    "volumes_eu": r"D:\Entropia Universe\Data\volumes\Volumes.bnt",
    "terraineditzones_eu": r"D:\Entropia Universe\Data\terraineditzones\TerrainEditZones.bnt",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest().upper()


def bnt2_index(data, max_entries=200):
    """Read the BNT2 trailer index (the verified PE BNT2 layout: u32 count @trailer)."""
    fs = len(data)
    magic = data[:8]
    trailer = data[-16:]
    # PE BNT2: trailer = index_start(u32) at fs-8 (the verified pattern from prior runs)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    entries = []
    pos = istart + 4
    for i in range(min(count, max_entries)):
        ne = pos
        while ne < fs and data[ne] != 0x0A:
            ne += 1
        nm = data[pos:ne].decode("ascii", "replace")
        sz, off = struct.unpack_from("<II", data, ne + 1)
        entries.append({"name": nm, "packed_size": sz, "offset": off})
        pos = ne + 17
    return {"magic": magic.hex(), "trailer": trailer.hex(), "index_start": istart,
            "count": count, "entries": entries}


def main():
    out = {"run": "PE_M1_GEOREF_P_DATUM_R1", "era_primary": "PCG 9.3.5", "files": {}}
    for key, path in FILES.items():
        if not os.path.isfile(path):
            out["files"][key] = {"status": "MISSING"}
            continue
        d = open(path, "rb").read()
        rec = {"size": len(d), "sha256": sha256_file(path)}
        try:
            rec.update(bnt2_index(d, max_entries=60))
            # entry-name census: any geo-coordinate-like names?
            names = [e["name"] for e in rec["entries"]]
            rec["name_patterns"] = {
                "numeric_named": sum(1 for n in names if n.replace(".", "").isdigit()),
                "sample": names[:24],
            }
        except Exception as ex:
            rec["parse_error"] = f"{type(ex).__name__}: {ex}"
        out["files"][key] = rec
        print(f"{key}: {len(d)} B, sha {rec['sha256'][:12]}, magic {rec.get('magic','?')}, count {rec.get('count','?')}")
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"census written: {OUT}")


if __name__ == "__main__":
    main()
