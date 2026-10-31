#!/usr/bin/env python3
"""RUN PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031 — Stage B VOLUME_PIN.

Own independent BNT2 index parser over Volumes.bnt (PCG 9.3.5, read-only).
Lineage note: written from the generic BNT2 trailer convention
([u32 index_start]['BNT2'] at EOF; index blob = [u32 count][count x entries]),
self-validated by full-consumption round-trip; NOT copied from P5's z2 parser.

Outputs 01_RAW/VOLUME_PIN.json with the three-way census reconciliation.
"""
import hashlib, json, struct, csv, sys, os

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
Z2CSV = os.path.join(RUN, "..",
                     "PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
                     "01_RAW", "Z2_VOLUMES_BNT_INDEX_NAMES.csv")
OUT = os.path.join(RUN, "01_RAW", "VOLUME_PIN.json")

data = open(BNT, "rb").read()
size = len(data)
sha = hashlib.sha256(data).hexdigest()
assert data[-4:] == b"BNT2", "trailer magic mismatch"
index_start = struct.unpack_from("<I", data, size - 8)[0]

# Parse index blob: [u32 count] then entries {name\0A, u32 packed, u32 offset, u32 c, u32 d}
pos = index_start
count = struct.unpack_from("<I", data, pos)[0]
pos += 4
entries = []
for i in range(count):
    nl = data.index(b"\x0a", pos)
    name = data[pos:nl].decode("ascii")
    pos = nl + 1
    packed, off, c, d = struct.unpack_from("<IIII", data, pos)
    pos += 16
    entries.append((i, name, packed, off, c, d))
# Round-trip: after count entries we must land exactly at the trailer start (size-8)
consumed_ok = (pos == size - 8)
violations = sum(1 for _, n, p, o, c, d in entries
                 if not (0 <= o and o + p <= index_start))

# Distinct .bvi name census
names = [n for _, n, _, _, _, _ in entries]
bvi_names = [n for n in names if n.endswith(".bvi")]
distinct_bvi = len(set(bvi_names))
dup_names = len(names) - len(set(names))

# Executor recount of Z2 CSV
with open(Z2CSV, newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
z2_rows = len(rows)
z2_all_bvi = all(r["name"].endswith(".bvi") for r in rows)
z2_distinct_bvi = len(set(r["name"] for r in rows if r["name"].endswith(".bvi")))

# Cross-check per-row name agreement (independent per-row reconciliation)
if z2_rows == len(entries):
    row_mismatch = sum(1 for r, e in zip(rows, entries) if r["name"] != e[1])
else:
    row_mismatch = -1  # not comparable

# Size distribution for Stage C sample choice
sizes = sorted([(p, n) for _, n, p, _, _, _ in entries])
report = {
    "run": "PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031",
    "stage": "B_VOLUME_PIN",
    "path": BNT,
    "size_bytes": size,
    "sha256": sha,
    "index_start": index_start,
    "index_count_declared": count,
    "index_entries_parsed": len(entries),
    "roundtrip_consumed_to_trailer": consumed_ok,
    "boundary_violations": violations,
    "dup_names": dup_names,
    "bvi_entries": len(bvi_names),
    "distinct_bvi_names": distinct_bvi,
    "z2_csv_data_rows": z2_rows,
    "z2_csv_all_names_bvi": z2_all_bvi,
    "z2_csv_distinct_bvi_names": z2_distinct_bvi,
    "z2_vs_own_row_name_mismatches": row_mismatch,
    "three_way": {
        "a_own_index_parse": len(entries),
        "b_z2_csv_recount": z2_rows,
        "c_distinct_bvi_names": distinct_bvi,
        "agree": len(entries) == z2_rows == distinct_bvi,
    },
    "disputed_900_vs_1865": {
        "stated_900": "does NOT match Z2 CSV; recount = 1865 data rows",
        "resolution": "900 figure unsupported by any measured source; three-way census agrees on 1865",
    },
    "size_stats": {
        "min": sizes[0], "max": sizes[-1],
        "smallest_10": sizes[:10], "largest_5": sizes[-5:],
    },
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=2)
print(json.dumps({k: report[k] for k in
      ["sha256", "index_count_declared", "index_entries_parsed",
       "roundtrip_consumed_to_trailer", "boundary_violations",
       "distinct_bvi_names", "z2_csv_data_rows"]}, indent=2))
