#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 - Z4: GATES G1-G4 (machine verification).

G1-JOIN: liczby join rekomputowalne z ZAPISANYCH artefaktów (detail CSV) i zgodne z
         Z2_JOIN_RESULT.json; round-trip endianness wykonany (pola w JSON); negative-control
         wykonany (20/20 absent w CSV); niezależny byte-scan PASS (Z2C JSON).
G2-CENSUS: pełny wynik census zapisany maszynowo (plik, linia, fraza, ocena) —
         Z3_QUANTIFIER_CENSUS.csv: 32 wierszy, kolumna verdict bez UNASSIGNED, zgodność
         ze Z3_CENSUS_SUMMARY.json.
G3-ERRATA: każda fraza zastępowana obecna DOKŁADNIE 1x w ERRATA_R2.md (jako cytat);
         nieobecna w narracji poprawionej (predykat: count==1); poprawki [E-1..E-6] oznaczone;
         poprawiona kopia nagłówka (GŁÓWNE PYTANIE P0) obecna 1x.
G4-IMMUTABLE: pełny re-hash obu kopii pakietu PE_935_TEMPLATE_CONSUMER_TRACE_R1 i porównanie
         z baseline zapisanym PRZED startem pracy (674 plików) — muszą być identyczne.

Zapis: 06_REPORT\GATE_CHECKS.json + stdout. FAIL-CLOSED (exit 1 przy każdej niezgodności).
"""

import csv
import hashlib
import json
import os
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"
R1_LOCAL = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
R1_REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
BASELINE = r"C:\Users\User\AppData\Local\Temp\opencode\pe935_join_r1_baseline_20260913.txt"

ERRORS = []


def die(gate, msg):
    ERRORS.append("[%s] %s" % (gate, msg))
    sys.stderr.write("[FAIL][%s] %s\n" % (gate, msg))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    out = {}

    # ---------------- G1 ----------------
    with open(os.path.join(RUN_ROOT, "01_RAW", "Z2_JOIN_RESULT.json"), encoding="utf-8") as f:
        j = json.load(f)
    with open(os.path.join(RUN_ROOT, "01_RAW", "Z2_JOIN_A_TO_NIF_DETAIL.csv"), encoding="utf-8", newline="") as f:
        rows_a = list(csv.DictReader(f))
    with open(os.path.join(RUN_ROOT, "01_RAW", "Z2_JOIN_B_TO_BVI_DETAIL.csv"), encoding="utf-8", newline="") as f:
        rows_b = list(csv.DictReader(f))
    with open(os.path.join(RUN_ROOT, "01_RAW", "Z2_NEGATIVE_CONTROL_A.csv"), encoding="utf-8", newline="") as f:
        rows_neg = list(csv.DictReader(f))
    with open(os.path.join(RUN_ROOT, "03_EVIDENCE", "Z2C_INDEPENDENT_SPOTCHECK.json"), encoding="utf-8") as f:
        j2c = json.load(f)

    hits_a = sum(1 for r in rows_a if r["hit"] == "True")
    miss_a = sum(1 for r in rows_a if r["hit"] != "True")
    hits_b = sum(1 for r in rows_b if r["hit"] == "True")
    uniq_a = len(rows_a)
    uniq_b = len(rows_b)
    rec_hits = sum(int(r["template_count"]) for r in rows_a if r["hit"] == "True")
    rec_hits_b = sum(int(r["template_count"]) for r in rows_b if r["hit"] == "True")

    g1 = {
        "detail_csv_rows_A": uniq_a,
        "detail_csv_hits_A": hits_a,
        "detail_csv_misses_A": miss_a,
        "detail_csv_rows_B": uniq_b,
        "detail_csv_hits_B": hits_b,
        "per_record_hits_A_from_template_counts": rec_hits,
        "per_record_hits_B_from_template_counts": rec_hits_b,
        "json_hits": j["join_A_to_nif"]["hits"],
        "json_misses": j["join_A_to_nif"]["misses"],
        "json_unique_A": j["join_A_to_nif"]["unique_nonzero_A"],
        "json_per_record_hits": j["join_A_to_nif"]["per_record"]["record_hits"],
        "json_bonus_hits": j["bonus_join_B_to_bvi"]["hits"],
        "json_bonus_per_record_hits": j["bonus_join_B_to_bvi"]["per_record"]["record_hits"],
        "json_B_zero_records": j["denominators"]["B_zero_record_count"],
        "json_A_zero_records": j["denominators"]["A_zero_record_count"],
        "negative_control_rows": len(rows_neg),
        "negative_control_all_absent": all(r["present_in_models_bnt"] == "False" for r in rows_neg),
        "endianness_round_trip_failures": j["endianness_control"]["round_trip_pack_unpack_failures"],
        "raw_byte_anchor_pack_identical": j["endianness_control"]["raw_byte_anchor_4508"]["pack_round_trip_identical"],
        "recompute_g1_identical": j["join_A_to_nif"]["recompute_g1"]["identical"],
        "independent_spotcheck_verdict": j2c["verdict"],
        "raw_nif_newline_equals_parser": (
            j2c["raw_census_context"]["models_bnt_dotnif_newline_occurrences"] == j2c["raw_census_context"]["parser_entry_counts"]["models"]),
        "raw_bvi_newline_equals_parser": (
            j2c["raw_census_context"]["volumes_bnt_dotbvi_newline_occurrences"] == j2c["raw_census_context"]["parser_entry_counts"]["volumes"]),
    }
    # arithmetic identities recomputed FROM SAVED ARTIFACTS
    if not (g1["detail_csv_hits_A"] == g1["json_hits"] == g1["json_unique_A"] == 3618):
        die("G1", "hits A: detail=%d json=%d uniq=%d (expected 3618)" %
            (g1["detail_csv_hits_A"], g1["json_hits"], g1["json_unique_A"]))
    if g1["detail_csv_misses_A"] != 0 or g1["json_misses"] != 0:
        die("G1", "misses A nonzero")
    if g1["per_record_hits_A_from_template_counts"] != g1["json_per_record_hits"] or g1["json_per_record_hits"] != 5438:
        die("G1", "per-record A: recomputed=%d json=%d" %
            (g1["per_record_hits_A_from_template_counts"], g1["json_per_record_hits"]))
    if not (g1["detail_csv_hits_B"] == g1["json_bonus_hits"] == 1666):
        die("G1", "hits B mismatch")
    if g1["per_record_hits_B_from_template_counts"] != g1["json_bonus_per_record_hits"]:
        die("G1", "per-record B mismatch")
    if g1["json_A_zero_records"] != 0:
        die("G1", "A==0 records nonzero")
    if g1["negative_control_rows"] != 20 or not g1["negative_control_all_absent"]:
        die("G1", "negative control: rows=%d all_absent=%r" %
            (g1["negative_control_rows"], g1["negative_control_all_absent"]))
    if g1["endianness_round_trip_failures"] != 0 or not g1["raw_byte_anchor_pack_identical"]:
        die("G1", "endianness controls failed")
    if not g1["recompute_g1_identical"]:
        die("G1", "Z2 internal double-recompute flag false")
    if "PASS" not in g1["independent_spotcheck_verdict"]:
        die("G1", "independent spotcheck not PASS")
    if not (g1["raw_nif_newline_equals_parser"] and g1["raw_bvi_newline_equals_parser"]):
        die("G1", "raw-scan census != parser census")
    # B==0 + per-record B == total records identity
    if g1["json_B_zero_records"] + g1["json_bonus_per_record_hits"] != 5438:
        die("G1", "B_zero(%d) + B_per_record_hits(%d) != 5438" %
            (g1["json_B_zero_records"], g1["json_bonus_per_record_hits"]))
    out["G1"] = {"PASS": len(ERRORS) == 0, "recomputed": g1}

    # ---------------- G2 ----------------
    with open(os.path.join(RUN_ROOT, "03_EVIDENCE", "Z3_QUANTIFIER_CENSUS.csv"), encoding="utf-8", newline="") as f:
        rows_c = list(csv.DictReader(f))
    with open(os.path.join(RUN_ROOT, "03_EVIDENCE", "Z3_CENSUS_SUMMARY.json"), encoding="utf-8") as f:
        jc = json.load(f)
    g2 = {
        "census_rows": len(rows_c),
        "summary_total_hits": jc["total_hits"],
        "unassigned_verdicts": sum(1 for r in rows_c if r["verdict"] in ("", "UNASSIGNED")),
        "rows_missing_verdict_column": sum(1 for r in rows_c if not r.get("verdict")),
        "verdict_counts_csv": {},
        "verdict_counts_json": jc["verdict_counts"],
    }
    for r in rows_c:
        g2["verdict_counts_csv"][r["verdict"]] = g2["verdict_counts_csv"].get(r["verdict"], 0) + 1
    if g2["census_rows"] != 32 or g2["census_rows"] != g2["summary_total_hits"]:
        die("G2", "census rows=%d summary=%d (expected 32)" % (g2["census_rows"], g2["summary_total_hits"]))
    if g2["unassigned_verdicts"] != 0 or g2["rows_missing_verdict_column"] != 0:
        die("G2", "unassigned verdicts present")
    if g2["verdict_counts_csv"] != g2["verdict_counts_json"]:
        die("G2", "verdict counts CSV vs JSON mismatch: %r vs %r" %
            (g2["verdict_counts_csv"], g2["verdict_counts_json"]))
    # required columns present
    for col in ("file", "line_no", "phrase_label", "matched_text", "verdict"):
        if col not in rows_c[0]:
            die("G2", "census missing column %s" % col)
    out["G2"] = {"PASS": not any(e.startswith("[G2]") for e in ERRORS), "measured": g2}

    # ---------------- G3 ----------------
    errata_path = os.path.join(RUN_ROOT, "06_REPORT", "ERRATA_R2.md")
    with open(errata_path, encoding="utf-8") as f:
        errata = f.read()
    replaced_phrases = [
        "Mechanizm jest w pełni zakotwiczony w kodzie",
        "wykonuje reader",
        "Kolejność pracy dla przyszłego runu: (1) zdekodować warstwę sieci",
        "A dosłownie nazywa wpis",
        "GWNE PYTANIE",
        "Łańcuch kompletny do otworzenia zasobu modelu",
    ]
    g3 = {p: errata.count(p) for p in replaced_phrases}
    for p, c in g3.items():
        if c != 1:
            die("G3", "replaced phrase count=%d (expected 1): %s" % (c, p))
    markers = ["[E-1]", "[E-2]", "[E-3]", "[E-4]", "[E-5]", "[E-6]"]
    for m in markers:
        if errata.count(m) < 1:
            die("G3", "missing errata marker %s" % m)
    if errata.count("## GŁÓWNE PYTANIE P0 — ODPOWIEDŹ") != 1:
        die("G3", "corrected quote-line count != 1")
    # corrected narrative phrases present (kanoniczne brzmienia)
    for must in ("ZAWIERA i MOŻE WYKONAĆ reader", "STRONGLY_SUPPORTED", "H_CLIENT", "FULL_MAPPING"):
        if errata.count(must) < 1:
            die("G3", "corrected narrative missing phrase: %s" % must)
    # typo must NOT appear in corrected narrative outside its single quote line: covered by count==1
    # corrected narrative must NOT contain the replaced phrases (count==0)
    final_report_path = os.path.join(RUN_ROOT, "06_REPORT", "00_FINAL_REPORT.md")
    with open(final_report_path, encoding="utf-8") as f:
        narrative = f.read()
    g3_narrative = {p: narrative.count(p) for p in replaced_phrases}
    for p, c in g3_narrative.items():
        if c != 0:
            die("G3", "replaced phrase present in corrected narrative (count=%d, expected 0): %s" % (c, p))
    # corrected canonical phrases present
    for must in ("ZAWIERA i MOŻE WYKONAĆ reader", "STRONGLY_SUPPORTED", "H_CLIENT", "FULL_MAPPING",
                 "3,618/3,618", "1,666/1,666"):
        if narrative.count(must) < 1:
            die("G3", "final report missing canonical phrase: %s" % must)
    out["G3"] = {"PASS": not any(e.startswith("[G3]") for e in ERRORS),
                 "phrase_counts_errata": g3,
                 "phrase_counts_corrected_narrative": g3_narrative}

    # ---------------- G4 ----------------
    with open(BASELINE, encoding="utf-8-sig") as f:
        baseline = {}
        for line in f:
            line = line.rstrip("\r\n")
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 4:
                continue
            root, rel, size, sha = parts
            baseline[(root, rel)] = (int(size), sha)
    current = {}
    for root in (R1_LOCAL, R1_REPO):
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                current[(root, rel)] = (os.path.getsize(full), sha256_file(full))
    g4 = {
        "baseline_files": len(baseline),
        "current_files": len(current),
        "missing": sorted([k for k in baseline if k not in current])[:20],
        "added": sorted([k for k in current if k not in baseline])[:20],
        "changed": sorted([k for k in baseline if k in current and baseline[k] != current[k]])[:20],
    }
    if len(baseline) != 674:
        die("G4", "baseline file count=%d (expected 674)" % len(baseline))
    if g4["missing"] or g4["added"] or g4["changed"]:
        die("G4", "package drift: missing=%d added=%d changed=%d (first 20 each in 'measured')"
            % (len(g4["missing"]), len(g4["added"]), len(g4["changed"])))
    out["G4"] = {"PASS": not any(e.startswith("[G4]") for e in ERRORS), "measured": g4}

    # ---------------- result ----------------
    overall_pass = all(out[g]["PASS"] for g in ("G1", "G2", "G3", "G4"))
    result = {
        "run_id": "PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
        "stage": "Z4_gate_checks_G1_G4",
        "driver": "z4_gates.py",
        "driver_sha256": sha256_file(os.path.abspath(__file__)),
        "gates": out,
        "overall_G1_G4": "PASS" if overall_pass else "FAIL",
        "note": "G5 (git path census / push / HEAD==origin) i G6 (entrypoint +1/-0) weryfikowane "
                "procedurą publikacji (git) — patrz 06_REPORT\\00_FINAL_REPORT.md §5 i HANDOFF.",
        "errors": ERRORS,
    }
    with open(os.path.join(RUN_ROOT, "06_REPORT", "GATE_CHECKS.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(result, indent=2, ensure_ascii=False).encode("ascii", "backslashreplace").decode())
    if not overall_pass or ERRORS:
        sys.exit(1)
    print("[Z4] GATES G1-G4 PASS")


if __name__ == "__main__":
    main()
