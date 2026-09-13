#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 - Z3b: merge semantic verdicts into the
quantifier census (final machine-readable census for gate G2).

RUN_ID: PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913
INPUT:  03_EVIDENCE\Z3_QUANTIFIER_HITS_RAW.csv (mechanical scan, 32 hits)
OUTPUT: 03_EVIDENCE\Z3_QUANTIFIER_CENSUS.csv (hits + verdict + rationale + errata ref)

Verdict taxonomy (audytor):
  OK_FACTUAL              — kwantyfikator opisuje zmierzony/zrealizowany obiekt (tabela, procedura).
  OK_SCOPED               — kwantyfikator ograniczony w tym samym zdaniu do zakresu faktycznie
                            kompletnego (np. "od pliku do rejestru", "(A→request)"); zgodny z
                            PARTIAL_TO_RESOURCE.
  OK_STATIC_CODE_DESC     — czasownik opisuje statyczne rozkazy kodu (byte-locked), nie przebieg
                            runtime.
  OK_FACTUAL_NEGATIVE     — uczciwa negacja ("NIE wykonano").
  NEEDS_QUALIFICATION     — fraza indykatywna brzmiąca runtime'owo w runie STATIC-ONLY
                            (klient nigdy nie uruchomiony); errata [E-2].
  OVERCLAIM_AS_WORDED     — jako słowo przekracza klasyfikację PARTIAL_TO_RESOURCE lub
                            twierdzi nieudowodnioną konieczność; errata [E-1]/[E-3]/[E-4].
Warstwa AUX (PE_MASTER_REVIEW.md) jest poza predykatem Z3 (kierunek erraty: adnotacja (e)/(E-4),
bez modyfikacji oryginału).
"""

import csv
import hashlib
import json
import os
import sys

RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913"
OUT_EV = os.path.join(RUN_ROOT, "03_EVIDENCE")

# key = (file, line_no, phrase_label, matched_text) -> (verdict, rationale, errata_ref)
V = {}

FR = r"06_REPORT\00_FINAL_REPORT.md"
HO = r"06_REPORT\HANDOFF.md"
GA = r"06_REPORT\STAGE_ACCEPTANCE_GATES.csv"
BA = r"02_ANALYSIS\B_template_loading_chain.md"
CA = r"02_ANALYSIS\C_transform_source_and_D_placement.md"
PM = r"06_REPORT\PE_MASTER_REVIEW.md"

# --- FINAL_REPORT -----------------------------------------------------------
V[(FR, 15, "static_runtime_phrasing", "czyta")] = (
    "NEEDS_QUALIFICATION",
    "Fraza indykatywna o brzmieniu wykonaniowym („klient czyta i konsumuje”) w runie STATIC-ONLY "
    "(klient nigdy nie uruchomiony). Poprawne brzmienie: klient ZAWIERA i MOŻE wykonać reader "
    "(statycznie wykazany przepływ; brak runtime-observation).",
    "E-2")
V[(FR, 15, "static_runtime_phrasing", "konsumuje")] = V[(FR, 15, "static_runtime_phrasing", "czyta")]
V[(FR, 16, "w_pelni", "w pełni")] = (
    "OVERCLAIM_AS_WORDED",
    "„Mechanizm jest w pełni zakotwiczony w kodzie” — jako słowo przekracza GATE-A = "
    "PARTIAL_TO_RESOURCE: ciała metod wirtualnych providera/fabryki (node+0x24 → vtable[+4]/"
    "[+0x38]) NIE są zdekomponowane; ciąg create→store-read w fabryce nie jest VA-locked. "
    "Uczciwość ratowana natychmiastowym residuum w §2, ale zdanie otwierające §0 nie przenosi "
    "kwalifikacji. Finding A audytu zewnętrznego (Desktop): „o pół kroku za mocny”.",
    "E-1")
V[(FR, 17, "static_runtime_phrasing", "czyta")] = (
    "NEEDS_QUALIFICATION",
    "„rekordy czyta generyczny reader VFS” — opis kodu w trybie wykonaniowym; run STATIC-ONLY.",
    "E-2")
V[(FR, 19, "static_runtime_phrasing", "konsumenci pobierają")] = (
    "NEEDS_QUALIFICATION",
    "Czasownik wykonaniowy dla obiektów kodu; run STATIC-ONLY (przepływ statyczny, nie runtime).",
    "E-2")
V[(FR, 20, "static_runtime_phrasing", "wołają")] = (
    "NEEDS_QUALIFICATION",
    "Czasownik wykonaniowy dla obiektów kodu; run STATIC-ONLY.",
    "E-2")
V[(FR, 41, "kompletn*", "Kompletn")] = (
    "OK_FACTUAL",
    "„Kompletna tabela 20 ogniw” — tabela 20 ogniw istnieje i jest kompletna jako tabela "
    "(rejestr VA ma 20 wierszy); zgodne z bramką.",
    "")
V[(FR, 69, "kompletn*", "kompletn")] = (
    "OK_SCOPED",
    "„PARTIAL_TO_RESOURCE (z resztą łańcucha kompletną)” — residuum jawnie wykluczone w tym samym "
    "zdaniu; „reszta” = łańcuch minus jawne residuum. Zgodne z klasyfikacją bramki.",
    "")
V[(FR, 79, "static_runtime_phrasing", "czyta")] = (
    "OK_STATIC_CODE_DESC",
    "„konsument A czyta WYŁĄCZNIE +0x08” — opis statycznych rozkazów (byte-locked, QC §2), "
    "nie przebiegu runtime.",
    "")
V[(FR, 102, "kompletn*", "kompletn")] = (
    "OK_SCOPED",
    "Wiersz bramki: „łańcuch L1–L7 kompletny VA-locked; residuum: …” — jawne residuum "
    "w tej samej komórce; zgodne z PARTIAL_TO_RESOURCE.",
    "")
V[(FR, 113, "wszystk*", "Wszystkie")] = (
    "OK_FACTUAL",
    "Self-check o 4 bramkach własnych — fakt proceduralny.",
    "")
V[(FR, 117, "wykonan*", "wykonaniem")] = (
    "OK_FACTUAL",
    "Procedura hashowania skryptów — fakt proceduralny.",
    "")
V[(FR, 123, "wykonan*", "wykonano")] = (
    "OK_FACTUAL_NEGATIVE",
    "Uczciwa negacja residuum („NIE wykonano: dekompilacja ciał metod wirtualnych providera”).",
    "")

# --- HANDOFF ----------------------------------------------------------------
V[(HO, 15, "kompletn*", "kompletn")] = (
    "OK_SCOPED",
    "„konsument kompletny: get A → {0x66,A}” — scope jawny (ścieżka do żądania); nie twierdzi "
    "fizycznego otwarcia; zgodne z PARTIAL_TO_RESOURCE.",
    "")
V[(HO, 21, "static_runtime_phrasing", "czyta")] = (
    "NEEDS_QUALIFICATION",
    "„EU 9.3.5 czyta rekordy templates.vfs” — brzmienie wykonaniowe; run STATIC-ONLY.",
    "E-2")
V[(HO, 24, "static_runtime_phrasing", "konsumuje")] = (
    "NEEDS_QUALIFICATION",
    "„konsumuje A do załadowania modelu” — brzmienie wykonaniowe; run STATIC-ONLY.",
    "E-2")
V[(HO, 34, "static_runtime_phrasing", "czyta")] = (
    "OK_STATIC_CODE_DESC",
    "„ścieżka modelu czyta WYŁĄCZNIE +0x08” — opis statyczny, byte-locked (separacja instrukcyjna).",
    "")
V[(HO, 40, "wszystk*", "wszystkie")] = (
    "OK_FACTUAL",
    "„wszystkie [VA] własne, z binarium E7785430…” — fakt provenance (QC potwierdził).",
    "")
V[(HO, 47, "kompletn*", "kompletn")] = (
    "OK_SCOPED",
    "„konsument kompletny:” — kontekst listy VA (ścieżka do żądania {0x66,A}).",
    "")
V[(HO, 67, "wykonan*", "wykonaniem")] = (
    "OK_FACTUAL",
    "Procedura hashowania — fakt proceduralny.",
    "")

# --- STAGE_ACCEPTANCE_GATES ---------------------------------------------------
V[(GA, 3, "static_runtime_phrasing", "czyta")] = (
    "OK_STATIC_CODE_DESC",
    "„scieyka modelu czyta WYLACZNIE +0x08” — opis statyczny, byte-locked.",
    "")

# --- B_template_loading_chain -------------------------------------------------
V[(BA, 5, "wszystk*", "wszystkie")] = (
    "OK_FACTUAL",
    "„wszystkie dekompilacje własne, w TYM binarium” — fakt provenance (QC §2 weryfikował).",
    "")
V[(BA, 8, "w_pelni", "W pełni")] = (
    "OK_SCOPED",
    "„W pełni zablokowany bajtowo łańcuch wczytyania rekordu (od pliku do rejestru)” — jawny "
    "scope (od pliku do rejestru = ogniwa 1–11), ta część faktycznie w pełni byte-locked "
    "(QC 6/6 + ~40); NIE obejmuje providera/fabryki.",
    "")
V[(BA, 28, "kompletn*", "kompletn")] = (
    "OK_SCOPED",
    "„konsument kompletny (A→request)” — scope jawny w nawiasie.",
    "")

# --- C_transform_source_and_D_placement ---------------------------------------
V[(CA, 10, "kompletn*", "kompletn")] = (
    "OK_SCOPED",
    "„Ścieżka avatar/consumer kompletnego A” — ścieżka konsumenta A (nie cały mechanizm).",
    "")
V[(CA, 41, "wykonan*", "wykonano")] = (
    "OK_FACTUAL_NEGATIVE",
    "Uczciwa negacja („nie wykonano żadnego mock-spawn”).",
    "")
V[(CA, 46, "MUSI_upper", "MUSI")] = (
    "OVERCLAIM_AS_WORDED",
    "„Transformacja modelu per-instancja MUSI przechodzić przez menedżer sceny/modeli” — "
    "nieudowodniona konieczność modalna: wniosek architektoniczny bez instruction-lock "
    "(brak zdekompilowanego transform-set). Kontekst Finding B audytu zewnętrznego (C.4 "
    "network-first + MUSI = zbyt wąska ramka kolejnego kierunku).",
    "E-3")
V[(CA, 46, "musi_lower", "MUSI")] = V[(CA, 46, "MUSI_upper", "MUSI")]

# --- PE_MASTER_REVIEW (AUX — poza predykatem Z3) --------------------------------
V[(PM, 6, "static_runtime_phrasing", "czyta")] = (
    "NEEDS_QUALIFICATION",
    "[AUX] Warstwa PE-MASTER (advisory): fraza indykatywna jak w FINAL_REPORT §0; run STATIC-ONLY.",
    "E-2-aux")
V[(PM, 6, "static_runtime_phrasing", "konsumuje")] = V[(PM, 6, "static_runtime_phrasing", "czyta")]
V[(PM, 9, "kompletn*", "kompletn")] = (
    "OVERCLAIM_AS_WORDED",
    "[AUX] „Łańcuch kompletny do otworzenia zasobu modelu” — fraza cytowana wprost przez audyt "
    "zewnętrzny (Finding A: „o pół kroku za mocny”); poprawne warstwowanie: do ŻĄDANIA zasobu = "
    "CONFIRMED (VA-locked); fizyczne OTWARCIE = STRONGLY_SUPPORTED (RTTI + rejestracja .nif + "
    "BNT2 reader + data-binding), NIE instruction-closed. Warstwa PE-MASTER — pakiet immutable; "
    "adnotacja erraty E-6 (nie modyfikacja oryginału).",
    "E-6")
V[(PM, 10, "static_runtime_phrasing", "czyta")] = (
    "OK_STATIC_CODE_DESC",
    "[AUX] „czyta wyłącznie +0x08” — opis statyczny, byte-locked.",
    "")


def main():
    raw_path = os.path.join(OUT_EV, "Z3_QUANTIFIER_HITS_RAW.csv")
    with open(raw_path, "r", encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f)]

    missing_keys = []
    out_rows = []
    for r in rows:
        key = (r["file"], int(r["line_no"]), r["phrase_label"], r["matched_text"])
        if key not in V:
            missing_keys.append(key)
            verdict = rationale = errata = "UNASSIGNED"
        else:
            verdict, rationale, errata = V[key]
        out = dict(r)
        out["verdict"] = verdict
        out["verdict_rationale"] = rationale
        out["errata_ref"] = errata
        out_rows.append(out)

    if missing_keys:
        sys.stderr.write("FAIL-CLOSED: %d hits without assigned verdict:\n" % len(missing_keys))
        for k in missing_keys:
            sys.stderr.write("  %r\n" % (k,))
        sys.exit(1)

    out_csv = os.path.join(OUT_EV, "Z3_QUANTIFIER_CENSUS.csv")
    fields = ["file", "layer", "line_no", "phrase_label", "matched_text", "line_text",
              "verdict", "verdict_rationale", "errata_ref"]
    with open(out_csv, "w", encoding="utf-8", newline="\n") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    counts = {}
    for r in out_rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    by_layer = {}
    for r in out_rows:
        by_layer.setdefault(r["layer"], {}).setdefault(r["verdict"], 0)
        by_layer[r["layer"]][r["verdict"]] += 1

    result = {
        "run_id": "PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913",
        "stage": "Z3b_census_verdict_merge",
        "driver": "z3b_merge_verdicts.py",
        "driver_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest().upper(),
        "total_hits": len(out_rows),
        "verdict_counts": counts,
        "by_layer": by_layer,
        "overclaim_sites_unique": [
            {"file": FR, "line": 16, "errata_ref": "E-1",
             "site": "„Mechanizm jest w pełni zakotwiczony w kodzie”"},
            {"file": CA, "line": 46, "errata_ref": "E-3",
             "site": "„MUSI przechodzić przez menedżer sceny/modeli” (C.4 + kolejność network-first)"},
            {"file": PM, "line": 9, "errata_ref": "E-4", "layer": "AUX",
             "site": "„Łańcuch kompletny do otworzenia zasobu modelu” (PE-MASTER layer, immutable)"},
        ],
        "note": "Klucz (file, line, phrase_label, matched_text) unikalny dla wszystkich 32 trafień; "
                "warstwa AUX poza predykatem Z3 (kierunek erraty, nie modyfikacja).",
        "errors": [],
    }
    with open(os.path.join(OUT_EV, "Z3_CENSUS_SUMMARY.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({"total_hits": len(out_rows), "verdict_counts": counts,
                      "by_layer": by_layer}, indent=2, ensure_ascii=False))
    print("[Z3B] CENSUS MERGE DONE")


if __name__ == "__main__":
    main()
