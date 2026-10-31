# REPORT — PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031 (RUN_CLASS: MATERIAL, STATIC-ONLY)

RUN_ID: PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031 | PARENT_LOOP: 75db9418-2d3e-4e05-9799-eeb4c3f63955
Era: PCG_9_3_5 | Executor: pe-reconstruction (bounded worker; NO_NESTED_TASKS)

## 1. Pytanie główne i odpowiedź

> Czy rekordy placementu obiektów świata (model id + pozycja [+ orientacja/skala]) są
> odzyskiwalne z Volumes.bnt / wpisów .bvi — na poziomie dowodu dual-independent decode —
> i jaką mają strukturę?

**ODPOWIEDŹ: NIE dla .bvi jako źródła placementu (klasa NOT_PLACEMENT_DATA, dowód dual
decode 4/4 próbki + census korpusu 1850/1865); STRUKTURA .bvi: dwie rodziny geometryczne —
TYPE0 (prymitywy 36 B = 9×f32 LE: 2×trójka 3D + trójka kątowa π/36-quantized) i
TYPE1 (siatka: vcount×f32×3 + tcount×3×u32 triangle-soup).** Relacja do modeli istnieje
tylko na poziomie NAZW plików (bvi_id = nif_id + 1, 1098/1865 = 58.9%), nie w payloadach
(join pól u32: 0/675). Relacja .bvi↔model jest per-model (collision volume; konsument
P5: pole B template → `<B>.bvi` 1,666/1,666), co wraz z brakiem id w payloadach wyklucza
rolę nośnika rekordów placementu. Wspólna klatka świata dla pól f1–f6 ODRZUCONA pomiarem
(klastrowanie zakresów per-plik); dokładna semantyka f1–f6 i przestrzeń per-rekord:
UNDETERMINED (V2-009 zachowane).

Werdykt era-2003 (BVI = local collision mesh) POTWIERDZONY na poziomie payloadu dla
PCG_9_3_5 — jako nowy pomiar; kanony §6 bez zmian, brak propozycji supersesji.

## 2. Startup (obowiązek kontraktu §1)

- BASE_SHA_AT_EXECUTION = dc6f1961125596dba9f3156371fb427a90881436 (`git rev-parse HEAD`
  == BASE_SHA kontraktu — zgodność). DIRTY_PATH_INVENTORY: wyłącznie
  `?? docs/audits/PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031/` (katalog tego runu — oczekiwany).
- Re-hash pinów (wszystkie PASS, fail-closed):
  - P1 6BC4DCED…84A20; P2 9014F963…6547; P3 EDC245EF…48B0; P4 5C946B94…6BA9B;
    P5-primary 6D6B9C8D…123E; P5-Z2CSV 55625900…CD7E (wszystkie == kontrakt §5).
  - Volumes.bnt: 3,746,375 B, SHA256 6AD8BA3C…BAC09 == pin §4. Models.bnt indeks: 5,596/0 duplikatów.

## 3. Wyniki Stage'ów

- **Stage A** — PRIOR_CANON_PLACEMENT_VERDICTS.md: P1–P5 wyekstrahowane z plików;
  żaden pakiet nie rozstrzygnął pytania payloadowego (P5 jawnie "nie badano payloadów
  .bvi"); brak PRIOR_CANON_ALREADY_RESOLVED. Era-2003 kanon udokumentowany jako
  NIE-bindujący dla 9.3.5 do czasu własnego pomiaru (dokonanego).
- **Stage B** — VOLUME_PIN.json: census trójstronny **1865 = 1865 = 1865** (własny parse /
  recount Z2 CSV / unikalne nazwy), round-trip do traileru PASS, 0 naruszeń granic.
  Dysputa 900-vs-1865: „900" niepoparte żadnym zmierzonym źródłem; zgodność trójstronna
  = 1865. **G2 PASS.**
- **Stage C** — 4 zróżnicowane próbki (148 B / 40 B / 2,524 B / 190,690 B). DWA dekodery
  o RÓŻNYCH liniach: A (Python, structure-first: licznik w nagłówku), B (Node.js,
  content/statistics-driven: grid-solver z dywizybilności+wzorca, vcount ze skanu f32-run).
  Zgodność: 4/4, **0 rozbieżności** (675 pól f32 + komplet checków TYPE1, w tym vcount
  scan-vs-header = 2104). Kontrole negatywne **wykonane**: wrong-endian/truncated/wrong-width
  **FAIL na obu** (4/4×3 każdy; rzeczywiste komunikaty w DECODE_A.json/DECODE_B.json).
  **G3 PASS.** (Ujawnienie: pierwsza wersja kontroli b (truncate 40 B) nie zawiodła dla
  584781 — naprawione przed finalnym pomiarem: ucięcie 24,000 B łamie blok wierzchołków;
  historia re-pinów w tools/PINS_SHA256.txt.)
- **Stage D** — BVI_STRUCTURE.md: TYPE0 = nagłówek `00 00 + u16 LE count` + count×36 B
  (9×f32 LE: f1–f6 trójki 3D UNDETERMINED, f7–f9 kąty OBSERVED π/36-quantized, pełnokorpusowo
  21,818 rekordów — TYPE0_FIELD_STATS.json); równanie 4+count×36==packed **1686/1686**.
  TYPE1 = `u32@0=1` + vc×f32×3 + u32 tricount + tricount×3×u32 (triangle-soup OBSERVED);
  **ogon 584781 (154,314 B = 80.9%) NIEZDEKODOWANY — jawny RESUME_POINT**. 15 plików (0.80%)
  nagłówków poza obiema rodzinami — UNCLASSIFIED.
- **Stage E** — PLACEMENT_CLASSIFICATION.md: klasa **NOT_PLACEMENT_DATA** (geometria
  kolizyjna per-model); 5 pomiarów dowodowych; tabela ALTERNATIVE_HYPOTHESES A1–A7
  (A2–A4 wykluczone pomiarem; A1 wykluczona jako wspólna klatka świata; A5 częściowo
  otwarta ale bez id nie nośna; A6/A7 otwarte = RESUME_POINT; denominatory jawne).
  **G4 PASS.**
- **Stage F** — MODEL_JOIN.md/MODEL_JOIN.json: nazwy: exact 0/1865, **id−1: 1098/1865
  (58.9%)**, id+1: 10, not-joined 757, ambiguous 0. Pola f32: u32 0/675; u16 5/1350 (0.37%)
  sklasyfikowane koincydencjalnie (2 unikalne wartości, powtórzenia między rekordami).
  Primary index = własny parse Models.bnt; P5 CSV tylko cross-check. **G5 PASS.**

## 4. Coverage algebra

TOTAL plików .bvi = 1865 = dual-decoded (4) + header-only (1861; w tym 15
header-unclassified). Sumy nie dublują podzbiorów: 4 + 1861 = 1865; 0 missing. Payload-level dual decode: 4/1865;
pełna struktura payloadu: 3/4 (584781 częściowo — ogon otwarty); pola TYPE1 poza joinem:
2,104 wierzchołków + 2,778 indeksów not-tested (z powodem).

## 5. Standing canon (§6 — verbatim, nietknięty)

```text
HISTORICAL_BUILDING_PLACEMENT   = NOT_ESTABLISHED
MODEL_218757_TO_WORLD_INSTANCE   = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED              = NO
HISTORICAL_WORLD_INSTANCE        = NOT_ESTABLISHED
PE_AXES_AND_UNITS                = UNVERIFIED
```
Brak propozycji supersesji. Wynik runu jest spójny z kanonem.

## 6. Intervention ledger

INTERVENTIONS: NONE (static data analysis only). Zero uruchomień klienta/frida/debuggerów;
zero zmian w compat/, src/, pcg_install, starych pakietach audytowych (READ_ONLY — weryfikacja
obecności braku zmian: ten run nigdy nie otwierał ich do zapisu); zero commitów/add/push;
serwery nietknięte (żadna komenda sieciowa).

## 7. SELF_CHECK (własny, jawny — NIE audyt PE-MASTER)

- [x] Wszystkie piny (P1–P5, Z2CSV, Volumes.bnt) re-hashowane przed analizą; zgodność fail-closed.
- [x] Census trójstronny policzony trzema niezależnymi metodami; zgoda 1865/1865/1865.
- [x] Kontrole negatywne WYKONANE (nie zadeklarowane): 24 wykonania (2 dekodery × 4 próbki × 3
      kontrole), wszystkie FAIL z zapisanym komunikatem; jedna iteracja naprawcza udokumentowana.
- [x] Lineage dekoderów rozdzielony (nagłówki plików tools/); brak wspólnej mapy pól.
- [x] Denominatory wszędzie jawne (§4); brak "fully audited" bez mianownika.
- [x] Etykiety OBSERVED/HYPOTHESIS przypisane per-pole; żadna wartość f32 nie została
      nazwana współrzędną świata (V2-009; §12 kontraktu).
- [x] Narzędzia run-local z SHA256 pinowanym PRZED użyciem (tools/PINS_SHA256.txt;
      historia re-pinów jawna — 3 iteracje naprawcze: volume_pin ścieżka, decode_a truncate,
      decode_b .cjs+kalibracja).
- [ ] NIE wykonano (granice): dekodu ogonu TYPE1 (80.9% payloadu 584781); dekodu 15 plików
      "INNE"; dekodu pozostałych 1,861 payloadów (tylko census nagłówkowy); nie badano
      konsumenta runtime .bvi w binarium (poza kanonem P5); Kaitai/hexpat jako trzecia
      implementacja — nie użyto (kontrakt wymagał dwóch; V3 byłby rozszerzeniem).

## 8. NOT_CHECKED (pełna lista jawnych granic)

1. Ogon TYPE1 w 584781.bvi (154,314 B) — struktura nieznana (zaczyna się od bloku f32 z
   powtórzeniami 4-bajtowymi); wymaga dedykowanego pomiaru.
2. 15 plików z nagłówkami `01 00 xx 00` (0.80%) — niezdekodowane.
3. Pozostałe 1,861 payloadów — tylko weryfikacja nagłówka/rodziny.
4. Semantyka dokładna pól f1–f6 TYPE0 (punkt? AABB? capsule?) — UNDETERMINED bez
   konsumenta runtime (potrzebny RE binarium: reader .bvi w Entropia.exe).
5. Przypisanie osi rotacji f7–f9 (Euler X/Y/Z) — HYPOTHESIS.
6. Nie wykonano trzeciej implementacji (Kaitai) — poza zakresem kontraktu (≥2 wymagane).

## 9. RESUME_POINT (jeśli PE-MASTER zleci kontynuację)

Kolejność wartości: (1) dekod ogona TYPE1 (największy nierozwiązany segment payloadowy);
(2) dekod 15 plików "INNE"; (3) RE binarium: zlokalizować reader .bvi (wzorzec: u32@0==1,
tri-soup) i domknąć semantykę f1–f6 per konsument (to rozstrzygnie hipotezę prymitywu
kolizyjnego vs cokolwiek innego, bez uruchamiania klienta).
