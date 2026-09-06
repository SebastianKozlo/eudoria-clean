#!/usr/bin/env python3
"""Pre-freeze calibration probe for PE_935_TEXANCHOR_CENSUS_R1 (era PCG_9_3_5).

READ-ONLY exploration BEFORE the frozen method is written. Purpose:
 1. Confirm the frozen R61 parser API surface used by the census driver
    (block_type strings, fields["name"] on NiTriShape / NiMaterialProperty,
    res fields) on the pinned corpus.
 2. Sample the per-file mesh-name universe on entry-bearing K1 files and
    measure the OBSERVED own-file mesh-part resolution rate on a small
    sample (calibration only - NOT the run measurement).
 3. Record everything machine-readable for the audit trail.

This probe writes ONLY inside this run package (00_CONTROL). It parses the
read-only corpus with the frozen R61 parser (10/10 SHA pins verified first).
NO census outputs are produced here; the frozen method + PREREG_MARKER are
written AFTER this probe and BEFORE the census driver executes.
"""
import sys
import os
import csv
import json
import struct
import hashlib
import random

sys.dont_write_bytecode = True

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEXANCHOR_CENSUS_R1_20260906_175500"
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_SHA256 = "c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0"
K1_TABLE = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\01_RAW"
            r"\ARKTEXTURE_ID_TABLE.csv")
K1_SHA256 = "34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9"
R61_SRC = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = (r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828"
                r"\03_validation\SHA256_SOURCE.json")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out = {"probe": "calibration_probe_r1", "era": "PCG_9_3_5",
           "read_only": True}
    # pins
    with open(R61_SHA_JSON, "r", encoding="utf-8-sig") as f:
        locked = json.load(f)
    r61_ok = 0
    for name, sha in locked.items():
        if name.endswith(".py"):
            actual = sha256_file(os.path.join(R61_SRC, name))
            assert actual.lower() == str(sha).lower(), name
            r61_ok += 1
    models_sha = sha256_file(MODELS_BNT)
    k1_sha = sha256_file(K1_TABLE)
    assert models_sha.lower() == MODELS_SHA256
    assert k1_sha.lower() == K1_SHA256
    out["pins"] = {"r61_source_files": r61_ok, "models_bnt_sha256": models_sha,
                   "k1_table_sha256": k1_sha}

    # K1 table quick structure
    rows = list(csv.DictReader(open(K1_TABLE, encoding="utf-8")))
    out["k1_rows"] = len(rows)

    # parse index
    sys.path.insert(0, R61_SRC)
    from pe_nif_reader import PENifReader  # noqa: E402

    def parse_bnt2_index(path, expected_count):
        fs = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(fs - 8)
            footer = f.read(8)
        istart = struct.unpack_from("<I", footer, 0)[0]
        assert footer[4:8] == b"BNT2"
        with open(path, "rb") as f:
            f.seek(istart)
            idx = f.read(fs - 8 - istart)
        count = struct.unpack_from("<I", idx, 0)[0]
        assert count == expected_count, count
        pos = 4
        entries = []
        for i in range(count):
            ne = pos
            while idx[ne] != 0x0A:
                ne += 1
            name = idx[pos:ne].decode("ascii", errors="replace")
            size, off = struct.unpack_from("<II", idx, ne + 1)
            entries.append((name, size, off))
            pos = ne + 17
        assert pos == len(idx)
        return entries

    models_entries = parse_bnt2_index(MODELS_BNT, 5596)
    out["models_bnt_entries"] = len(models_entries)
    entry_map = {n: (s, o) for n, s, o in models_entries}

    # pick a calibration sample: the first 40 entry-bearing K1 files + a few
    # specific ones
    from collections import Counter
    per_file = Counter(r["nif"] for r in rows)
    sample_files = sorted(per_file)[:40]
    rng = random.Random(20260906)
    extra = rng.sample(sorted(per_file), 40)
    sample_files = sorted(set(sample_files) | set(extra))

    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    reader = PENifReader()

    universes = {}
    block_type_census = Counter()
    name_field_types = Counter()
    for name in sample_files:
        size, off = entry_map[name]
        payload = data[off:off + size]
        res = reader.parse_bytes(payload, source_name=name)
        assert res.parse_status == "PASS", (name, res.parse_status)
        uni = set()
        for b in res.blocks:
            block_type_census[b.block_type] += 1
            if b.block_type in ("NiTriShape", "NiMaterialProperty"):
                nm = (b.fields or {}).get("name")
                name_field_types[(b.block_type, type(nm).__name__)] += 1
                if isinstance(nm, str) and nm:
                    uni.add(nm)
        universes[name] = uni

    # measure own-file resolution on the sample entries
    n_ent = 0
    n_res = 0
    n_slot_ok = 0
    per_src = Counter()
    examples = []
    for r in rows:
        if r["nif"] not in universes:
            continue
        n_ent += 1
        nm = r["name"]
        if "_" in nm:
            mesh_part, suffix = nm.rsplit("_", 1)
        else:
            mesh_part, suffix = nm, ""
        hit = mesh_part in universes[r["nif"]]
        per_src["hit" if hit else "miss"] += 1
        if hit:
            n_res += 1
        if suffix == r["slot"]:
            n_slot_ok += 1
        if len(examples) < 12:
            examples.append({"nif": r["nif"], "name": nm, "mesh_part": mesh_part,
                             "suffix": suffix, "table_slot": r["slot"],
                             "own_file_resolution": hit,
                             "universe_size": len(universes[r["nif"]]),
                             "universe_head": sorted(universes[r["nif"]])[:6]})

    out["sample"] = {
        "files": len(sample_files),
        "entries_in_sample": n_ent,
        "own_file_mesh_part_resolutions": n_res,
        "table_slot_vs_suffix_agreements": n_slot_ok,
        "per_outcome": dict(per_src),
        "resolution_rate_sample": (n_res / n_ent) if n_ent else None,
    }
    out["examples"] = examples
    out["block_type_census_on_sample"] = dict(block_type_census)
    out["name_field_types"] = {"%s/%s" % k: v for k, v in name_field_types.items()}
    out["universe_sizes_head"] = {f: len(universes[f])
                                  for f in list(sample_files)[:10]}

    with open(os.path.join(RUN, "00_CONTROL", "CALIBRATION_PROBE.json"),
              "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in
                      ("pins", "k1_rows", "sample", "name_field_types")},
                     indent=1)[:2600])
    print("examples:")
    for e in examples[:6]:
        print(" ", json.dumps(e)[:240])


if __name__ == "__main__":
    main()
