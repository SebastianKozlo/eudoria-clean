#!/usr/bin/env python
# m1_iter032k_vcl_columns.py
# ITER_046 / ledger ITER_032 - Gate C vector (d): the VCL column semantics
# census: cols 0-11 full census (distinct/histogram/quantiles), col1 density
# distribution, per-file (climate) structure, the special rows (cols 12-28),
# column correlations, and the 48-byte/12-value record check.
# Source: pcg_install Data\VegetationClimates\VegetationClimates.bnt
# (byte-identical to both corpus copies, SHA 7B858401..., iter017/032-verified)
import json
import struct
import hashlib
import math
from collections import Counter, defaultdict

BIN = r"D:\Eudoria_Reconstruction\pcg_install\Data\VegetationClimates\VegetationClimates.bnt"
OUT = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926\03_EVIDENCE\F02_ITER032K_RERUN_vcl_columns.json"

data = open(BIN, "rb").read()
sha = hashlib.sha256(data).hexdigest()
assert sha == "7b858401c3eebda574df4b4517e7fb2a8149c283885f27187682aa1239c745f4", sha

# ---- BNT2 parse (trailer [dir_off u32]["BNT2"]; at dir_off: [count u32]
#      + count x ([name 0x0A-terminated][size u32][offset u32][crc u32][flags u32]);
#      per the iter031e lesson: 0x0A terminator; stride name+1+16) ----
assert data[len(data)-4:len(data)] == b"BNT2", data[-4:]
dir_off = struct.unpack_from("<I", data, len(data) - 8)[0]
count = struct.unpack_from("<I", data, dir_off)[0]
entries = {}
off = dir_off + 4
for i in range(count):
    nl = data.index(b"\x0a", off)
    name = data[off:nl].decode("ascii")
    rec = nl + 1
    size, ofs, crc, flags = struct.unpack_from("<IIII", data, rec)
    entries[name] = {"size": size, "offset": ofs, "crc": crc, "flags": flags}
    off = rec + 16

# locate payloads: read each .vcl directly by (size, offset)
vcls = {}
for name, e in entries.items():
    if not name.endswith(".vcl"):
        continue
    payload = data[e["offset"]:e["offset"] + e["size"]]
    txt = payload.decode("latin-1")
    vcls[name] = {"size": e["size"], "offset": e["offset"], "text": txt}

out = {"iter": "032k", "source": {"file": BIN, "sha256": sha},
       "bnt2": {"count": count, "dir_off": dir_off, "vcl_entries": len(vcls)},
       "measured": {}, "interpreted": {}, "errors": []}
m = out["measured"]
m["vcl_files"] = sorted(vcls.keys())
assert len(vcls) == 32, len(vcls)

# ---- parse TSV rows ----
all_rows = []          # (file, [tokens])
special_rows = []      # rows with >12 columns (raw)
for name in sorted(vcls.keys(), key=lambda n: int(n.split(".")[0])):
    for line in vcls[name]["text"].splitlines():
        if not line.strip():
            continue
        toks = line.split("\t")
        if len(toks) > 12:
            special_rows.append({"file": name, "ntok": len(toks), "raw": line[:300]})
        # keep all tokens; numeric census on the first 12
        all_rows.append((name, toks))

m["total_rows_alltokens"] = len(all_rows)
m["rows_with_gt12_tokens"] = len(special_rows)
m["special_rows_raw"] = special_rows

# numeric rows (>= 12 numeric tokens)
num_rows = []
for name, toks in all_rows:
    vals = []
    ok = True
    for t in toks[:12]:
        try:
            vals.append(float(t))
        except ValueError:
            ok = False
            break
    if ok:
        num_rows.append((name, vals, len(toks)))
m["numeric_rows_12cols"] = len(num_rows)

# ---- per-column census ----
m["col_census"] = []
for c in range(12):
    vals = [v[c] for _, v, _ in num_rows]
    vs = sorted(vals)
    n = len(vs)
    def q(p):
        return vs[min(n - 1, int(p * n))]
    hist = Counter(vals)
    m["col_census"].append({
        "col": c,
        "n": n,
        "min": vs[0], "max": vs[-1],
        "mean": sum(vs) / n,
        "distinct": len(hist),
        "q10": q(0.10), "q50": q(0.50), "q90": q(0.90),
        "top_values": hist.most_common(12),
        "all_integer": all(float(v).is_integer() for v in vals),
    })

# ---- col1 density distribution ----
dvals = sorted(v[1] for _, v, _ in num_rows)
dh = Counter(v[1] for _, v, _ in num_rows)
m["col1_density"] = {
    "n": len(dvals),
    "min": dvals[0], "max": dvals[-1],
    "zero_count": dh.get(0.0, 0),
    "distinct": len(dh),
    "q25": dvals[len(dvals)//4], "q50": dvals[len(dvals)//2], "q75": dvals[3*len(dvals)//4],
    "top20": dh.most_common(20),
}

# ---- per-file structure ----
per_file = {}
for name in sorted(vcls.keys(), key=lambda n: int(n.split(".")[0])):
    rows = [(nm, v) for nm, v, _ in num_rows if nm == name]
    ids = [int(v[0]) for _, v in rows]
    d1 = [v[1] for _, v in rows]
    per_file[name] = {
        "rows": len(rows),
        "models": sorted(ids),
        "density_sum": sum(d1),
        "density_max": max(d1) if d1 else None,
        "elev_band_union": [min(v[4] for _, v in rows), max(v[5] for _, v in rows)] if rows else None,
    }
m["per_file"] = per_file

# ---- column correlations (Pearson over numeric rows) ----
def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs)/n, sum(ys)/n
    cov = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    vx = sum((x-mx)**2 for x in xs)
    vy = sum((y-my)**2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return cov / math.sqrt(vx*vy)

m["correlations"] = {}
pairs = [(0,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),
         (4,6),(5,7),(2,3),(4,5),(6,7),(8,9),(10,11),(0,4),(0,5)]
for a, b in pairs:
    xs = [v[a] for _, v, _ in num_rows]
    ys = [v[b] for _, v, _ in num_rows]
    m["correlations"]["col%d_vs_col%d" % (a, b)] = pearson(xs, ys)

# ---- model-id overlap between files (climate similarity) ----
sets = {name: set(pf["models"]) for name, pf in per_file.items()}
names = sorted(sets.keys(), key=lambda n: int(n.split(".")[0]))
m["model_overlap_matrix_top"] = []
sims = []
for i in range(len(names)):
    for j in range(i+1, len(names)):
        inter = len(sets[names[i]] & sets[names[j]])
        union = len(sets[names[i]] | sets[names[j]])
        jacc = inter / union if union else 0
        sims.append((jacc, inter, names[i], names[j]))
sims.sort(reverse=True)
m["model_overlap_matrix_top"] = [{"jaccard": s[0], "inter": s[1], "a": s[2], "b": s[3]} for s in sims[:12]]
m["model_overlap_min"] = [{"jaccard": s[0], "inter": s[1], "a": s[2], "b": s[3]} for s in sims[-6:]]
m["distinct_models_total"] = len(set().union(*sets.values()))

# ---- the 48-byte record check ----
out["interpreted"]["record_format"] = (
    "12 numeric columns per row x 4 bytes = 48 bytes = the 0x30-stride records in "
    "ArkVegetationClimate (FUN_0083acd0: vector begin/end at +0x10/+0x18, 0x30 stride "
    "deallocation) filled by the TSV parser FUN_0083a7d0 (12-value copy loop, +0x30 append). "
    "Column order preserved = the TSV order.")

with open(OUT, "w") as fh:
    json.dump(out, fh, indent=1)
print("WROTE", OUT)
print("numeric rows:", m["numeric_rows_12cols"], "special rows:", m["rows_with_gt12_tokens"])
for c in m["col_census"]:
    print("col%-2d distinct=%-5d min=%-10g max=%-10g int=%s top=%s" % (
        c["col"], c["distinct"], c["min"], c["max"], c["all_integer"], c["top_values"][:5]))
print("col1:", m["col1_density"])
