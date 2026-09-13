#!/usr/bin/env python3
# script_scan.py — ERRATA, weryfikacja reprodukcyjna korekty C (retraction negatywu skryptowego).
# Cel: niezależne potwierdzenie adjudykowanych faktów audytu zewnętrznego F3 (offsety trafień
# w zdekodowanym korpusie .obj.dec) + zweryfikowanie mianownika "pozostałych" plików.
# ZERO nowej forensyki — reprodukcja faktów podwójnie zweryfikowanych (audyt + PE-MASTER);
# pełny wynik zapisywany do 02_EVIDENCE\SCRIPT_SCAN_REPRO.json.
import os, struct, json

ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_DYN1_INGEST_PARSER_GHIDRA_R1_20260903_120000\03_EVIDENCE\decoded"
ERR = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912"

U32_IDS = [296445, 296446, 126740, 126741, 278453, 278454]
patterns = {}
for i in U32_IDS:
    p = struct.pack("<I", i)
    assert struct.unpack("<I", p)[0] == i, f"reverse-conversion assertion FAILED for {i}"
    patterns[str(i)] = p
ascii_patterns = {"296445": b"296445"}

files = sorted(fn for fn in os.listdir(ROOT) if fn.endswith(".obj.dec"))
hits = {}
files_with_hits = set()
for fn in files:
    data = open(os.path.join(ROOT, fn), "rb").read()
    for k, p in patterns.items():
        off = data.find(p)
        while off != -1:
            hits.setdefault(k, []).append({"file": fn, "offset": off})
            files_with_hits.add(fn)
            off = data.find(p, off + 1)
    for k, p in ascii_patterns.items():
        off = data.find(p)
        while off != -1:
            hits.setdefault(f"ascii:{k}", []).append({"file": fn, "offset": off})
            files_with_hits.add(fn)
            off = data.find(p, off + 1)

# Wartości adjudykowane (audyt zewnętrzny F3 + PE-MASTER) — bramka zgodności:
EXPECTED = {
    ("296445", "4508.obj.dec"): 664,
    ("296446", "4508.obj.dec"): 580,
    ("126740", "4752.obj.dec"): 520,
    ("278453", "2249.obj.dec"): 664,
}
gate_ok = True
for (pid, fn), exp_off in EXPECTED.items():
    got = [(h["file"], h["offset"]) for h in hits.get(pid, [])]
    if (fn, exp_off) not in got:
        gate_ok = False
        print(f"MISMATCH: {pid} in {fn} @ {exp_off} NOT found (got {got})")

result = {
    "purpose": "reprodukcja korekty C (retraction '0 odniesień do 296445'); weryfikacja mianownika",
    "corpus": ROOT, "corpus_files": len(files),
    "files_with_hits": sorted(files_with_hits), "files_without_hits": len(files) - len(files_with_hits),
    "hits": hits,
    "adjudicated_offsets_gate": {"expected": {f"{k[0]}@{k[1]}": v for k, v in EXPECTED.items()},
                                  "pass": gate_ok},
    "notes": ("Mianownik plikowy bez trafień = 1,936 - 3 = 1,933 (kontrakt erraty podawał '1,932' = "
              "1,936 - 4 trafienia — artefakt arytmetyczny, poprawka udokumentowana w ERRATA.md). "
              "Skan pełny (6 wzorców u32LE + ASCII 296445) wykrywa dodatkowo kompani +1 "
              "(126741 @4752.obj.dec@436; 278454 @2249.obj.dec@580) — spójne z parowaniem B=A+1; "
              "zapisane jako pełny wynik reprodukcji, nie część adjudykowanego tekstu korekty."),
}
assert gate_ok, "SCRIPT SCAN GATE FAIL — adjudykowane offsety nieodtworzone"
json.dump(result, open(os.path.join(ERR, "02_EVIDENCE", "SCRIPT_SCAN_REPRO.json"), "w"), indent=1)
print(f"files: {len(files)}; with hits: {len(files_with_hits)} ({sorted(files_with_hits)}); without: {len(files)-len(files_with_hits)}")
print("adjudicated offsets gate: PASS")
for k in sorted(hits):
    print(f"  {k}: {[(h['file'], h['offset']) for h in hits[k]]}")
