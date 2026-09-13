#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 - Z3: quantifier/narrative census (Finding A, Desktop).

RUN_ID: PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913
PURPOSE: Zgodnie z zleceniem PE-MASTER (finding A audytu zewnętrznego): przeszukaj
         FINAL_REPORT + HANDOFF + STAGE_ACCEPTANCE_GATES + 02_ANALYSIS pakietu
         PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912 pod kątem kwantyfikatorów
         i narracji: „kompletny", „w pełni zakotwiczony", „MUSI", „zawsze",
         „wszystkie", „cały", „wykonuje", „pełny łańcuch".
         Pomocniczo (oznaczone jako warstwa PE-MASTER, poza predykatem Z3):
         06_REPORT\PE_MASTER_REVIEW.md (kontekst erraty (e) + fraza
         „Łańcuch kompletny do otworzenia zasobu" cytowana przez audyt zewnętrzny).

OUTPUT: 03_EVIDENCE\Z3_QUANTIFIER_HITS_RAW.csv (mechaniczny scan, bez ocen)
         + 03_EVIDENCE\Z3_QUANTIFIER_SCAN_SUMMARY.json (per-plik/per-fraza liczby)
READ-ONLY na pakiecie R1 (immutable; errata go tylko cytuje).
"""

import csv
import hashlib
import json
import os
import re
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"
OUT_EV = os.path.join(RUN_ROOT, "03_EVIDENCE")
R1_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"

PRIMARY_FILES = [
    r"06_REPORT\00_FINAL_REPORT.md",
    r"06_REPORT\HANDOFF.md",
    r"06_REPORT\STAGE_ACCEPTANCE_GATES.csv",
    r"02_ANALYSIS\A_record_definition.md",
    r"02_ANALYSIS\B_template_loading_chain.md",
    r"02_ANALYSIS\C_transform_source_and_D_placement.md",
]
AUX_FILES = [  # poza predykatem Z3; kontekst erraty (c)/(e)
    r"06_REPORT\PE_MASTER_REVIEW.md",
]

PATTERNS = [
    ("kompletn*", re.compile(r"kompletn", re.IGNORECASE)),
    ("w_pelni", re.compile(r"w\s+pełni", re.IGNORECASE)),
    ("pelny_lancuch", re.compile(r"pełn\w*\s+łańcuch\w*", re.IGNORECASE)),
    ("MUSI_upper", re.compile(r"\bMUSI\b")),
    ("musi_lower", re.compile(r"\bmusi\b", re.IGNORECASE)),
    ("zawsze", re.compile(r"\bzawsze\b", re.IGNORECASE)),
    ("wszystk*", re.compile(r"\bwszystk\w*", re.IGNORECASE)),
    ("cal*", re.compile(r"\bcał\w*", re.IGNORECASE)),
    ("wykonuj*", re.compile(r"\bwykonuj\w*", re.IGNORECASE)),
    ("wykonan*", re.compile(r"\bwykonan\w*", re.IGNORECASE)),
    # errata (b): frazy indykatywne brzmiące runtime'owo w runie STATIC-ONLY
    ("static_runtime_phrasing", re.compile(
        r"\b(czyta|czytają|konsumuje|konsumenci\b.*pobierają|pobierają|wołają|odczytuje|wysyła)\b",
        re.IGNORECASE)),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    hits = []
    summary = {"files": {}, "per_label": {}}
    file_hashes = {}
    for rel in PRIMARY_FILES + AUX_FILES:
        path = os.path.join(R1_ROOT, rel)
        layer = "PRIMARY_Z3" if rel in PRIMARY_FILES else "AUX_PE_MASTER_LAYER"
        file_hashes[rel] = sha256_file(path)
        summary["files"][rel] = {"layer": layer, "sha256": file_hashes[rel], "hit_count": 0}
        with open(path, "r", encoding="utf-8", newline="") as f:
            raw_lines = f.read().splitlines()
        for ln, line in enumerate(raw_lines, start=1):
            for label, pat in PATTERNS:
                for m in pat.finditer(line):
                    hits.append({
                        "file": rel,
                        "layer": layer,
                        "line_no": ln,
                        "phrase_label": label,
                        "matched_text": m.group(0),
                        "line_text": line.strip(),
                    })
                    summary["files"][rel]["hit_count"] += 1
                    summary["per_label"][label] = summary["per_label"].get(label, 0) + 1

    out_csv = os.path.join(OUT_EV, "Z3_QUANTIFIER_HITS_RAW.csv")
    with open(out_csv, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=["file", "layer", "line_no", "phrase_label",
                                          "matched_text", "line_text"])
        w.writeheader()
        for h in hits:
            w.writerow(h)

    result = {
        "run_id": "PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
        "stage": "Z3_quantifier_census_raw_scan",
        "driver": "z3_quantifier_census.py",
        "driver_sha256": sha256_file(os.path.abspath(__file__)),
        "target_package": R1_ROOT,
        "target_files_sha256": file_hashes,
        "patterns": [p[0] for p in PATTERNS],
        "note": "Mechaniczny scan; oceny (OK/OVERCLAIM/NEEDS_QUALIFIER) nadawane w drugim kroku "
                "przez audytora (Z3_QUANTIFIER_CENSUS.csv z kolumną verdict).",
        "total_hits": len(hits),
        "summary": summary,
    }
    with open(os.path.join(OUT_EV, "Z3_QUANTIFIER_SCAN_SUMMARY.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(json.dumps({"total_hits": len(hits), "per_label": summary["per_label"],
                      "per_file": {k: v["hit_count"] for k, v in summary["files"].items()}},
                     indent=2, ensure_ascii=False))
    print("[Z3] RAW SCAN DONE (verdicts assigned in the merge step)")


if __name__ == "__main__":
    main()
