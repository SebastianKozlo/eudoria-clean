#!/usr/bin/env python3
# gate_census.py — ERRATA G3: census fraz w 01_CORRECTED\00_RAPORT_CORRECTED.md.
# Frazy poprawione: obecne DOKŁADNIE 1× (lub obecne ≥1 dla fraz wielokrotnych — liczby zapisane).
# Frazy zakazane (zastąpowane twierdzenia): NIEOBECNE (0 wystąpień).
import json, os

ERR = r"D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912"
REPORT = os.path.join(ERR, "01_CORRECTED", "00_RAPORT_CORRECTED.md")

text = open(REPORT, encoding="utf-8").read()
low = text.lower()

# --- frazy zakazane (zastępowane twierdzenia R1 + usunięte błędy) ---
FORBIDDEN = {
    "30× -1": "F1 — literówka liczby pustych slotów dzieci korzenia",
    "0 odniesień do 296445": "C — fałszywy negatyw skryptowy",
    "127 rekordów": "F2 — błędna liczba rekordów EnvironmentZones",
    "L~463": "F3 — błędny numer linii NiStream.cpp",
    "w żadnych danych klienta": "D1 — globalny negatyw",
    "wyłącznie serwer": "D2 — nieudowodniona wyłączność",
    "VFS 2003": "A2 — błędna etykieta ery korpusu ArkVFS02",
    "[00][FFFFFFFF][u32 ID w ofs 5][00]": "E — błędna arytmetyka 9 B (10 bajtów)",
    "atlas (flipbook)": "E — interpretacja bez etykiety hipotezy",
    "warianty slum: b001_01": "F8 — niepodparte twierdzenie o wariantach",
    "b062_01": "F8 — niepodparte twierdzenie o wariantach",
    "Strings/*.bpt": "F9 — błędne rozszerzenie (poprawne: .bnt)",
    "marker?w": "F9 — mojibake '?'",
    "wpis?w ? 2": "F9 — mojibake '?'",
    "s? zamienne": "F9 — mojibake '?'",
    "To domyka empirycznie semantykę": "B4 — wycofane zdanie o semantyce 7 floatów",
    "dostarcza WYŁĄCZNIE serwer": "A1/D2 — handler PE2 przypisany klientowi 9.3.5 z wyłącznością",
}

# --- frazy poprawione: obecne dokładnie 1× ---
REQUIRED_ONCE = {
    "27× -1 (23 realne dzieci)": "F1",
    "L362": "F3",
    "382,811–592,741": "F5",
    "27 plików, 2.2 MB": "F6",
    "84 kanoniczne + 42 ogonowe": "F2",
    "[u8 0 @0][u32 -1 (0xFFFFFFFF) @1..4][u32 ID @5..8]": "E",
    "0 w pozostałych 1,933 skryptach": "C (mianownik zweryfikowany skanem erraty)",
    "interpretacja flipbook/atlas = HIPOTEZA": "E",
    "ekstrema SUROWYCH tablic wierzchołków z RÓŻNYCH układów lokalnych": "B4",
    "world[i] = parent_world ∘ local_i": "B1 (konwencja)",
    "(401,-1611,-368)": "B3 (glowsak lokalne — opis A)",
    "blok 59 ma effect 13 w tablicy effects": "F4 (effects-owner)",
}

# --- frazy poprawione: obecne ≥1 (wielokrotne dozwolone; liczby zapisane) ---
REQUIRED_PRESENT = {
    "56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650": "A1 (SHA binarium PE2)",
    "E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31": "A1 (SHA Entropia.exe 9.3.5)",
    "HIPOTEZA TRANSFERU": "A1",
    "UNVERIFIED": "A1",
    "ArkVFS02": "A2",
    "era ≠ 2003-CD": "A2",
    "NOT_FOUND_IN_SEARCHED_SCOPE": "D1 (status negatywu)",
    "nie znaleziono potwierdzonego rekordu historycznej instancji 296445 w opisanym zakresie": "D1",
    "u32BE": "F10",
    "3,885 unikalnych wg regexu audytora": "F7",
    "PE2_unpacked_out.exe": "A1 (identyfikacja binarium kanonu)",
    "FUN_005977b0": "A1 (handler — z erą PE2/2003)",
    "vtable[0x50]": "A1 (z erą PE2/2003)",
    "min (-2500.0, -2500.0, ~-1.27e-08) do max (2500.0, 2500.0, 15620.0)": "B3 (bbox bramki G1; legalnie §2.3 + §3B)",
}

results = {"forbidden": {}, "required_once": {}, "required_present": {}}
ok = True
for phrase, why in FORBIDDEN.items():
    n = text.count(phrase) + (low.count(phrase.lower()) - text.count(phrase))  # case-insensitive total
    n = low.count(phrase.lower())
    results["forbidden"][phrase] = {"count": n, "why": why}
    if n != 0:
        ok = False
for phrase, why in REQUIRED_ONCE.items():
    n = text.count(phrase)
    results["required_once"][phrase] = {"count": n, "why": why, "expected": 1}
    if n != 1:
        ok = False
for phrase, why in REQUIRED_PRESENT.items():
    n = low.count(phrase.lower())
    results["required_present"][phrase] = {"count": n, "why": why}
    if n < 1:
        ok = False

results["verdict"] = ("G3 FAIL — patrz szczegóły poniżej" if not ok else
                     "G3 PASS — frazy zakazane 0 wystąpień; poprawione obecne (1× lub ≥1 z zapisanymi liczbami)")
json.dump(results, open(os.path.join(ERR, "02_EVIDENCE", "G3_GATE_RESULTS.json"), "w"), indent=1, ensure_ascii=False)
assert ok, "G3 FAIL — szczegoly w 02_EVIDENCE\\G3_GATE_RESULTS.json"
print("G3 PASS")
for phrase, r in results["forbidden"].items():
    print(f"  FORBIDDEN 0x: {phrase!r} -> {r['count']}")
for phrase, r in results["required_once"].items():
    print(f"  ONCE 1x: {r['count']}x {phrase!r}")
for phrase, r in results["required_present"].items():
    print(f"  PRESENT {r['count']}x {phrase!r}")
