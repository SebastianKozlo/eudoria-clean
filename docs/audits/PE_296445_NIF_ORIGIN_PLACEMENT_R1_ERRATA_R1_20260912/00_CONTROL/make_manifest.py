#!/usr/bin/env python3
# make_manifest.py — ERRATA G1 (pakiet): MANIFEST_SHA256.csv + artifact_index.csv.
#
# MANIFEST_SHA256.csv (02_EVIDENCE): WSZYSTKIE pliki ERRATA + WSZYSTKIE pliki R1.
#   Wykluczenie własne: manifest nie zawiera własnego hasha (precedens L12).
#   Pliki weryfikacyjne powstające PO manifeście (G4_GATE_RESULTS.json, G7_GATE_RESULTS.json)
#   są ŚWIADOMIE wykluczone z listowania (auto-weryfikacja nie może listować siebie) — wykluczenie
#   jawne, udokumentowane tutaj i w G4_GATE_RESULTS.json.
# artifact_index.csv (03_REPORT): pliki PAKIETU REPO (schema projektu: standing-sentence
#   + relpath,kind,sha256) — wyklucza artifact_index.csv/MANIFEST_SHA256.csv (auto-referencja).
import os, hashlib, csv, json

ERR = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912"
R1  = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

MANIFEST_NAME = "MANIFEST_SHA256.csv"

# --- artifact_index.csv: pliki pakietu REPO (dokładnie lista dozwolona commitu G5) ---
# KOLEJNOŚĆ: artifact_index PRZED manifestem (manifest listuje wszystkie pliki ERRATA poza sobą).
# artifact_index NIE listuje artifact_index.csv ani MANIFEST_SHA256.csv (wzajemna auto-referencja
# niemożliwa — oba pliki są w commicie; hash manifestu weryfikowalny przez git/G5).
PACKAGE = [
    ("03_REPORT/ERRATA.md", "errata report"),
    ("03_REPORT/PE_MASTER_REVIEW.md", "verbatim PE-MASTER review"),
    ("03_REPORT/HANDOFF.md", "handoff"),
    ("01_CORRECTED/00_RAPORT_CORRECTED.md", "corrected report"),
    ("01_CORRECTED/TRANSFORM_TABLE_CORRECTED.csv", "recomputed artifact"),
    ("01_CORRECTED/TREE_MESHES_CORRECTED.json", "recomputed artifact"),
    ("01_CORRECTED/TREE_ANALYSIS_CORRECTED.txt", "recomputed artifact"),
    ("00_CONTROL/analyze_tree_v2.py", "generator"),
    ("00_CONTROL/rawscan.py", "generator"),
    ("00_CONTROL/script_scan.py", "generator"),
    ("00_CONTROL/gate_census.py", "generator"),
    ("00_CONTROL/make_manifest.py", "generator"),
    ("00_CONTROL/verify_manifest.py", "generator"),
]
standing = ("# Standing sentence: ERRATA R1 to PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912 — documentation "
            "errata + mechanical recompute (G1 transform gate 14/30 + bbox + glowsak; G2 rawscan offset-exact; "
            "G3 phrase census; A–F corrections per adjudicated list; ZERO new forensics). "
            "artifact_index.csv nie listuje artifact_index.csv ani MANIFEST_SHA256.csv (wzajemna auto-referencja "
            "niemożliwa; oba w commicie; hash manifestu weryfikowalny przez git). Pelny manifest lokalny: "
            "02_EVIDENCE/MANIFEST_SHA256.csv (ERRATA+R1, bez wlasnego hasha — L12). Payloady (296445.nif, 296446.bvi) "
            "LOCAL-ONLY z metadanymi w manifeście.")
apath = os.path.join(ERR, "03_REPORT", "artifact_index.csv")
with open(apath, "w", newline="", encoding="utf-8") as f:
    f.write('"' + standing + '"\n')
    w = csv.writer(f)
    for rel, kind in PACKAGE:
        p = os.path.join(ERR, *rel.split("/"))
        w.writerow([rel, kind, sha256_file(p)])
print(f"artifact_index.csv: {len(PACKAGE)} rows (+ standing sentence) — written BEFORE manifest")

# --- MANIFEST: ERRATA + R1 ---
rows = []
for dp, dn, fns in os.walk(ERR):
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, ERR)
        if rel == os.path.join("02_EVIDENCE", MANIFEST_NAME):
            continue  # własne wykluczenie (L12)
        rows.append(("ERRATA", rel, os.path.getsize(p), sha256_file(p)))
r1_rows = []
for dp, dn, fns in os.walk(R1):
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, R1)
        r1_rows.append(("R1", rel, os.path.getsize(p), sha256_file(p)))
all_rows = sorted(rows + r1_rows, key=lambda r: (r[0], r[1].lower()))

mpath = os.path.join(ERR, "02_EVIDENCE", MANIFEST_NAME)
with open(mpath, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["run", "relpath", "size_bytes", "sha256"])
    w.writerows(all_rows)
print(f"MANIFEST_SHA256.csv: {len(all_rows)} rows (ERRATA: {len(rows)}, R1: {len(r1_rows)})")
# UWAGA: G4_GATE_RESULTS.json / G7_GATE_RESULTS.json powstają PO manifeście (verify_manifest.py)
# i są świadomie wykluczone z listowania (auto-weryfikacja nie może listować siebie — patrz verify_manifest.py).
