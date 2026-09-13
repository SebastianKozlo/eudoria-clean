#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 - Z2c: INDEPENDENT spot-check of the join
by RAW BYTE-SCAN (not via the BNT2 parser).

RUN_ID: PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913
PURPOSE: Kontrola niezależności (QC control: independent counter-check). Z2_JOIN_RESULT.json
         pochodzi z własnego parsera BNT2; ten skrypt weryfikuje RDZENIE twierdzenia C
         (członkostwo nazwy "<A>.nif" w Models.bnt) metodą FUNDAMENTALNIE inną: surowym
         skanem bajtów całego pliku (ta sama klasa metody, której użył QC runu R1 §4).

CHECKS:
  1. 8 pozytywnych próbek A (3 kotwice R1 + 5 losowych hitów z detail-CSV, seed 20260913):
     surowy skan Models.bnt musi znalezc string "<A>.nif" co najmniej 1 raz (region indeksu).
  2. 5 próbek B (3 kotwice R1 + 2 losowe hity): surowy skan Volumes.bnt dla "<B>.bvi".
  3. Negatywy: 3 syntetyczne A+1,000,000 (z Z2_NEGATIVE_CONTROL_A.csv) -> 0 wystapien w
     Models.bnt; cross-absent 296446.nif (Models.bnt) i 296445.bvi (Volumes.bnt) -> 0;
     999999999.nif/.bvi -> 0.
  4. Census surowy: liczba wystapien ".nif\n" w calym Models.bnt (raport, bez asercji
     dokladnej liczby - payloady moga teoretycznie zawierac sekwencje) oraz liczba nazw
     indeksowych z parsera (kontekst).
READ-ONLY na oryginale. Zapis: 03_EVIDENCE\Z2C_INDEPENDENT_SPOTCHECK.json.
"""

import csv
import hashlib
import json
import os
import random
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"
OUT_EV = os.path.join(RUN_ROOT, "03_EVIDENCE")
MODELS_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
VOLUMES_PATH = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
DETAIL_A = os.path.join(RUN_ROOT, "01_RAW", "Z2_JOIN_A_TO_NIF_DETAIL.csv")
DETAIL_B = os.path.join(RUN_ROOT, "01_RAW", "Z2_JOIN_B_TO_BVI_DETAIL.csv")
NEGCTRL = os.path.join(RUN_ROOT, "01_RAW", "Z2_NEGATIVE_CONTROL_A.csv")

SEED = 20260913

ERRORS = []


def die(msg):
    ERRORS.append(msg)
    sys.stderr.write("[FAIL] " + msg + "\n")


def count_occurrences(blob, needle):
    n = 0
    start = 0
    while True:
        i = blob.find(needle, start)
        if i < 0:
            return n
        n += 1
        start = i + 1


def main():
    with open(MODELS_PATH, "rb") as f:
        models = f.read()
    with open(VOLUMES_PATH, "rb") as f:
        volumes = f.read()

    with open(DETAIL_A, "r", encoding="utf-8", newline="") as f:
        rows_a = [r for r in csv.DictReader(f)]
    with open(DETAIL_B, "r", encoding="utf-8", newline="") as f:
        rows_b = [r for r in csv.DictReader(f)]
    with open(NEGCTRL, "r", encoding="utf-8", newline="") as f:
        rows_neg = [r for r in csv.DictReader(f)]

    rnd = random.Random(SEED)
    random_hits_a = rnd.sample([r for r in rows_a if r["hit"] == "True"], 5)
    random_hits_b = rnd.sample([r for r in rows_b if r["hit"] == "True"], 2)

    # (1) positives A (raw byte-scan, independent of the parser)
    pos_a = {}
    for a in [296445, 126740, 278453] + [int(r["a_value"]) for r in random_hits_a]:
        needle = b"%d.nif" % a
        c = count_occurrences(models, needle)
        pos_a[str(a)] = c
        if c < 1:
            die("raw-scan positive A=%d: 0 occurrences in Models.bnt (join said HIT)" % a)

    # (2) positives B
    pos_b = {}
    for b in [296446, 126741, 278454] + [int(r["b_value"]) for r in random_hits_b]:
        needle = b"%d.bvi" % b
        c = count_occurrences(volumes, needle)
        pos_b[str(b)] = c
        if c < 1:
            die("raw-scan positive B=%d: 0 occurrences in Volumes.bnt (join said HIT)" % b)

    # (3) negatives
    neg = {}
    for r in rows_neg[:3]:
        needle = r["name"].encode("ascii")
        c = count_occurrences(models, needle)
        neg[r["name"]] = c
        if c != 0:
            die("raw-scan synthetic negative %s: %d occurrences (expected 0)" % (r["name"], c))
    for name, blob, label in [("296446.nif", models, "Models.bnt"),
                              ("999999999.nif", models, "Models.bnt"),
                              ("296445.bvi", volumes, "Volumes.bnt"),
                              ("999999999.bvi", volumes, "Volumes.bnt")]:
        c = count_occurrences(blob, name.encode("ascii"))
        neg[name] = c
        if c != 0:
            die("raw-scan negative %s in %s: %d occurrences (expected 0)" % (name, label, c))

    # (4) raw census context (report only, no exact-count assertion)
    raw_nif_newline = count_occurrences(models, b".nif\n")
    raw_bvi_newline = count_occurrences(volumes, b".bvi\n")

    if ERRORS:
        sys.stderr.write("FAIL-CLOSED: %d error(s)\n" % len(ERRORS))
        sys.exit(1)

    result = {
        "run_id": "PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
        "stage": "Z2c_independent_raw_scan_spotcheck",
        "driver": "z2c_independent_spotcheck.py",
        "driver_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest().upper(),
        "method": "raw byte-scan of the whole archive files (independent of the BNT2 parser)",
        "models_bnt_sha256": hashlib.sha256(models).hexdigest().upper(),
        "volumes_bnt_sha256": hashlib.sha256(volumes).hexdigest().upper(),
        "positive_A_occurrences": pos_a,
        "positive_B_occurrences": pos_b,
        "negative_occurrences_expected_zero": neg,
        "raw_census_context": {
            "models_bnt_dotnif_newline_occurrences": raw_nif_newline,
            "volumes_bnt_dotbvi_newline_occurrences": raw_bvi_newline,
            "parser_entry_counts": {"models": 5596, "volumes": 1865},
            "note": "wystąpienia '.nif\\n' w calym pliku >= liczba wpisów indeksu (region indeksu; "
                    "payloady mogą teoretycznie zawierać sekwencję - bez asercji równości)",
        },
        "verdict": "PASS: wszystkie pozytywy potwierdzone surowym skanem, wszystkie negatywy 0",
        "errors": [],
    }
    with open(os.path.join(OUT_EV, "Z2C_INDEPENDENT_SPOTCHECK.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({"positive_A": pos_a, "positive_B": pos_b,
                      "negatives_all_zero": all(v == 0 for v in neg.values()),
                      "raw_nif_newline": raw_nif_newline,
                      "raw_bvi_newline": raw_bvi_newline}, indent=2))
    print("[Z2C] INDEPENDENT SPOTCHECK PASS")


if __name__ == "__main__":
    main()
