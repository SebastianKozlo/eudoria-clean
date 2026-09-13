#!/usr/bin/env python3
# verify_manifest.py — ERRATA G4 (manifest kompletny i zgodny: re-hash) + G7 final (R1 immutable).
# G4: (a) re-hash KAŻDEGO pliku z MANIFEST_SHA256.csv i porównanie z zapisanym hashem (0 MISMATCH);
#     (b) census plików: pliki ERRATA na dysku == wiersze ERRATA manifestu + wykluczenia jawne
#         (manifest sam + G4/G7_GATE_RESULTS.json); pliki R1 na dysku == wiersze R1 manifestu;
#     (c) porównanie z baseline: wiersze R1 == G7_R1_BASELINE_SHA256.csv (hashe sprzed pracy).
# G7: hashe wszystkich plików R1 PRZED i PO pracy erraty IDENTYCZNE (0 zmian w runie R1).
import os, hashlib, csv, json

ERR = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912"
R1  = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912"
MANIFEST = os.path.join(ERR, "02_EVIDENCE", "MANIFEST_SHA256.csv")
BASELINE = os.path.join(ERR, "02_EVIDENCE", "G7_R1_BASELINE_SHA256.csv")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# --- odczyt manifestu ---
rows = []
with open(MANIFEST, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows.append(row)
mismatch = []
manifest_paths = {"ERRATA": set(), "R1": set()}
for row in rows:
    base = ERR if row["run"] == "ERRATA" else R1
    p = os.path.join(base, row["relpath"])
    if not os.path.exists(p):
        mismatch.append(("MISSING_FILE", row["run"], row["relpath"]))
        continue
    h = sha256_file(p)
    if h != row["sha256"]:
        mismatch.append(("HASH_MISMATCH", row["run"], row["relpath"], row["sha256"], h))
    if os.path.getsize(p) != int(row["size_bytes"]):
        mismatch.append(("SIZE_MISMATCH", row["run"], row["relpath"]))
    manifest_paths[row["run"]].add(row["relpath"])

# --- census plików na dysku vs manifest ---
EXPLICIT_EXCLUDE_ERRATA = {os.path.join("02_EVIDENCE", "MANIFEST_SHA256.csv"),
                           os.path.join("02_EVIDENCE", "G4_GATE_RESULTS.json"),
                           os.path.join("02_EVIDENCE", "G7_GATE_RESULTS.json")}
disk_errata = set()
for dp, dn, fns in os.walk(ERR):
    for fn in fns:
        rel = os.path.relpath(os.path.join(dp, fn), ERR)
        disk_errata.add(rel)
unlisted = disk_errata - manifest_paths["ERRATA"] - EXPLICIT_EXCLUDE_ERRATA
extra_listed = manifest_paths["ERRATA"] - disk_errata
disk_r1 = set()
for dp, dn, fns in os.walk(R1):
    for fn in fns:
        disk_r1.add(os.path.relpath(os.path.join(dp, fn), R1))
r1_missing = disk_r1 - manifest_paths["R1"]

completeness_ok = (not unlisted) and (not extra_listed) and (not r1_missing)

# --- G7: baseline vs obecne hashe R1 ---
baseline = {}
with open(BASELINE, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        baseline[row["relpath"]] = (row["sha256"], row["size_bytes"])
g7_diff = []
for row in rows:
    if row["run"] == "R1":
        bl = baseline.get(row["relpath"])
        if bl is None:
            g7_diff.append(("NOT_IN_BASELINE", row["relpath"]))
        elif bl[0] != row["sha256"]:
            g7_diff.append(("R1_CHANGED", row["relpath"], bl[0], row["sha256"]))
baseline_extra = set(baseline) - {r["relpath"] for r in rows if r["run"] == "R1"}
if baseline_extra:
    g7_diff.append(("BASELINE_EXTRA", sorted(baseline_extra)))

g7_ok = (not g7_diff) and len(baseline) == len(disk_r1)
g4_ok = (not mismatch) and completeness_ok

result_g4 = {
    "G4_manifest_verify": "PASS" if g4_ok else "FAIL",
    "manifest_rows": len(rows),
    "rehash_mismatches": mismatch,
    "errata_disk_files": len(disk_errata),
    "errata_manifest_rows": len(manifest_paths["ERRATA"]),
    "explicit_exclusions": sorted(EXPLICIT_EXCLUDE_ERRATA),
    "unlisted_errata_files": sorted(unlisted),
    "r1_disk_files": len(disk_r1),
    "r1_manifest_rows": len(manifest_paths["R1"]),
    "r1_files_missing_from_manifest": sorted(r1_missing),
}
result_g7 = {
    "G7_r1_immutable": "PASS" if g7_ok else "FAIL",
    "baseline_rows": len(baseline),
    "r1_files_now": len(disk_r1),
    "hash_changes": g7_diff,
    "note": "baseline zebrany PRZED startem pracy erraty (02_EVIDENCE/G7_R1_BASELINE_SHA256.csv); porównanie po całym runie",
}
assert g4_ok, f"G4 FAIL: {json.dumps(result_g4, indent=1)}"
assert g7_ok, f"G7 FAIL: {json.dumps(result_g7, indent=1)}"
json.dump(result_g4, open(os.path.join(ERR, "02_EVIDENCE", "G4_GATE_RESULTS.json"), "w"), indent=1)
json.dump(result_g7, open(os.path.join(ERR, "02_EVIDENCE", "G7_GATE_RESULTS.json"), "w"), indent=1)
print(f"G4 PASS: {len(rows)} manifest rows re-hashed, 0 mismatches; ERRATA {len(manifest_paths['ERRATA'])}/{len(disk_errata)-len(EXPLICIT_EXCLUDE_ERRATA)} listed; R1 {len(manifest_paths['R1'])}/{len(disk_r1)} listed")
print(f"G7 PASS: R1 hash changes: 0 (baseline {len(baseline)} files == current {len(disk_r1)} files)")
