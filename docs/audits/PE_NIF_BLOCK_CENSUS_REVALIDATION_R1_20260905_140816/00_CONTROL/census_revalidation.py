#!/usr/bin/env python3
"""
PE_NIF_BLOCK_CENSUS_REVALIDATION_R1 — RUN-F (L21 denominator-falsification honored:
the R1 census EXISTS and is complete; this run = INDEPENDENT REVALIDATION + completion,
NOT a duplicate).

P0: does the R1 per-block-type census (77 types, 392,061 blocks, 5,596 files) reproduce
EXACTLY under a fresh independent execution of the frozen R61 parser on the same
hash-pinned corpus — and are the wiki registry counts consistent with it?

Completion items: explicit denominators everywhere; block-per-file sum cross-check;
era-labeled 9.3.5; per-type diff vs R1 (any mismatch = finding).
"""
import sys
import os
import json
import hashlib
import struct
from collections import Counter

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_BLOCK_CENSUS_REVALIDATION_R1_20260905_140816"
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
R61 = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json"
R1_CENSUS = r"D:\Eudoria_Reconstruction\99_Audits\PE_PCG935_NIF_CORPUS_AUDIT_R1_20260904_113907\02_results\BLOCK_TYPE_CENSUS.csv"
REGISTRY = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\nif\02-block-registry.md"

LOG = []
def log(m):
    LOG.append(str(m))
    print(m, flush=True)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    # pins
    locked = json.load(open(R61_SHA, encoding="utf-8-sig"))
    n_ok = 0
    for name, sha in locked.items():
        if name.endswith(".py"):
            if sha256_file(os.path.join(R61, name)).lower() == str(sha).lower():
                n_ok += 1
            else:
                raise RuntimeError(f"R61 HASH MISMATCH: {name}")
    log(f"[pins] R61 {n_ok}/10")
    corpus_sha = sha256_file(MODELS_BNT)
    log(f"[pins] corpus {corpus_sha}")
    r1_census_sha = sha256_file(R1_CENSUS)
    log(f"[pins] R1 census sha {r1_census_sha}")

    # R1 census load
    r1 = {}
    with open(R1_CENSUS, encoding="utf-8") as f:
        next(f)
        for line in f:
            t, c = line.strip().split(",")
            r1[t] = int(c)
    log(f"[R1] {len(r1)} types; total blocks {sum(r1.values())}")

    # corpus index
    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    fs = len(data)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    entries = []
    pos = istart + 4
    for _ in range(count):
        ne = pos
        while data[ne] != 0x0A:
            ne += 1
        nm = data[pos:ne].decode("ascii")
        sz = struct.unpack_from("<IIII", data, ne + 1)[0]
        off = struct.unpack_from("<IIII", data, ne + 1)[1]
        entries.append((nm, sz, off))
        pos = ne + 17
    log(f"[corpus] {len(entries)} entries (denominator: 5,596 files expected)")

    sys.path.insert(0, R61)
    from pe_nif_reader import PENifReader  # noqa: E402

    census = Counter()
    files_pass = 0
    per_file_blocks = {}
    statuses = Counter()
    for nm, sz, off in entries:
        payload = data[off:off + sz]
        res = PENifReader().parse_bytes(payload, source_name=nm)
        st = str(getattr(res, "parse_status", None) or getattr(res, "status", None) or "?")
        statuses[st] += 1
        nb = 0
        for b in (getattr(res, "blocks", None) or []):
            census[b.block_type] += 1
            nb += 1
        per_file_blocks[nm] = nb
        if st == "PASS":
            files_pass += 1
    total_blocks = sum(census.values())
    log(f"[fresh] statuses={dict(statuses)}; types={len(census)}; total={total_blocks}")
    log(f"[fresh] files PASS {files_pass}/{len(entries)}")

    # diff vs R1
    diff = {}
    for t in sorted(set(r1) | set(census)):
        a, b = r1.get(t, 0), census.get(t, 0)
        if a != b:
            diff[t] = {"R1": a, "fresh": b}
    log(f"[diff] vs R1: {len(diff)} type-count mismatches")

    # block-per-file sum cross-check
    spf = sum(per_file_blocks.values())
    log(f"[sum] sum(blocks-per-file)={spf} == census total {total_blocks}: {spf == total_blocks}")

    # registry cross-check (wiki 02-block-registry.md "Count 9.3.5" column)
    reg_rows = []
    with open(REGISTRY, encoding="utf-8") as f:
        for line in f:
            if line.startswith("| ") and "Count" not in line and "---" not in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[0] and cells[1]:
                    reg_rows.append((cells[0], cells[1]))
    reg_mismatch = []
    reg_checked = 0
    for t, cnt_txt in reg_rows:
        # handle "21,914 / 21,190" style (take the first number) and commas
        first = cnt_txt.split("/")[0].strip().replace(",", "")
        if not first.isdigit():
            continue
        reg_checked += 1
        if census.get(t) != int(first):
            reg_mismatch.append({"type": t, "registry": int(first), "census": census.get(t)})
    log(f"[registry] checked {reg_checked} rows; mismatches {len(reg_mismatch)}")

    out = {
        "run": "PE_NIF_BLOCK_CENSUS_REVALIDATION_R1",
        "denominators": {
            "files_declared": len(entries),
            "files_expected": 5596,
            "files_pass": files_pass,
            "parse_statuses": dict(statuses),
            "total_blocks_fresh": total_blocks,
            "total_blocks_R1": sum(r1.values()),
            "types_fresh": len(census),
            "types_R1": len(r1),
        },
        "pins": {"r61": f"{n_ok}/10", "corpus_sha256": corpus_sha,
                 "r1_census_sha256": r1_census_sha},
        "revalidation": {
            "census_identical_to_R1": len(diff) == 0,
            "type_diffs": diff,
        },
        "sum_cross_check": {"sum_blocks_per_file": spf,
                            "equals_census_total": spf == total_blocks},
        "registry_cross_check": {"rows_checked": reg_checked,
                                 "mismatches": reg_mismatch},
        "era": "PCG 9.3.5 (pcg_install Models.bnt)",
        "milestone_progress": {
            "counts": "fresh census 5,596 files / 392,061 blocks / 77 types (expected); diff vs R1 + registry cross-check",
            "excluded": "no 2003-era re-census (era-labeled 9.3.5 per the GO); no render; no wiki edits; no payloads",
        },
    }
    with open(os.path.join(RUN, "01_RAW", "REVALIDATION_RESULTS.json"), "w") as f:
        json.dump(out, f, indent=2)
    with open(os.path.join(RUN, "05_ANALYSIS", "SUMMARY.json"), "w") as f:
        json.dump({k: out[k] for k in ("denominators", "revalidation",
                                       "sum_cross_check", "registry_cross_check")},
                  f, indent=2)
    with open(os.path.join(RUN, "02_LOGS", "LOGS.md"), "w") as f:
        f.write("\n".join(LOG))
    log(f"[done] census_identical_to_R1={len(diff) == 0}")


if __name__ == "__main__":
    main()
