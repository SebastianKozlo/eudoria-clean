# PLACEMENT_CLASSIFICATION — Stage E (PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031)

## Klasa przypisana (dokładnie jedna z taksonomii kontraktu)

**NOT_PLACEMENT_DATA** — payloady .bvi służą innej roli: **geometria kolizyjna per-model**
(prymitywy objętościowe z rotacją + siatki trójkątowe), dedykowana pojedynczemu modelowi
NIF wskazywanemu przez relację nazw `bvi_id = nif_id + 1`.

Denominatory (jawne):
- Payload-level dual decode: **4/1865** plików (506044, 105624, 506237, 584781) — klasa
  dla ZDEKODOWANEJ PRÓBKI jest CAŁKOWICIE udowodniona poniższymi pomiarami.
- Header-level census (pełny korpus): **1850/1865 = 99.2%** plików potwierdza rodzinę
  TYPE0 (1686) lub TYPE1 (164); **15/1865 = 0.80%** (nagłówki `01 00 xx 00`) —
  NIE sklasyfikowane w tym runie (jawne ograniczenie; classification korpusowa opiera
  się na 99.2% + identyczności roli archiwum jako całości — patrz dowód 2).

## Dowody roli (1–5; każdy = pomiar, nie proza)

1. **Brak pola id modelu w payloadach** — placement-record potrzebuje identyfikatora
   modelu/instancji; w 675 polach f32 (3 próbki TYPE0) reinterpretacja u32: **0 trafień**
   w indeksie Models.bnt (5,596 nazw, 0 duplikatów); u16-połówki: 5/1350 (0.37%) —
   koincydencje (2 unikalne wartości powtórzone między rekordami; patrz MODEL_JOIN.md).
   Przy braku id, rekord placementu musiałby dziedziczyć id z nazwy pliku — ale wtedy
   wszystkie rekordy jednego pliku wskazywałyby TEN SAM model (patrz dowód 3).
2. **Rodzina TYPE1 = siatki trójkątowe** (584781: 2,104 wierzchołków f32×3 + 926 trójkątów
   u32×3, indeksy < vcount, wzorce triangle-soup 0,1,2…71,71,72,69…) — archiwum zawiera
   jawnie GEOMETRIĘ; nośnik placementów nie potrzebuje siatek trójkątnych per-model.
   Rodziny TYPE0/TYPE1 współdzielą kontener, konwencję nazw i relację do NIF — jedna rola.
3. **Konsumencki join P5 (STANDING)**: pole B templates.vfs (per-REKORD template, pojedyncza
   wartość) odwzorowuje się 1,666/1,666 na nazwę `<B>.bvi` — każdy template wskazuje JEDEN
   plik .bvi = zasób per-model (collision volume), nie listę placementów instancji.
4. **Niespójność ze współdzieloną klatką świata (pomiar dyskryminujący)**: zakresy pól f1–f6
   klastrowane per-plik (506044: [−526, +1265]; 506237: [−25, +33]; 105624: [−0.55, +1.73]) —
   gdyby rekordy były pozycjami świata, wszystkie pliki dzieliłyby tę samą klatkę i zakresy
   rozkładałyby się porównywalnie (świat PE: 0..524,287 / runtime 14,336×15,360).
   Klastrowanie per-plik = przestrzeń LOKALNA per-model (PE_AXES_AND_UNITS = UNVERIFIED
   pozostaje kanonem — twierdzimy tylko "nie jest to jedna wspólna klatka placementu").
5. **f7–f9 = kąty (OBSERVED wartości π/36-quantized)** — per-prymitywowa orientacja
   (HYPOTHESIS Euler) — spójne ze zbiorem brył kolizyjnych danego modelu, nie z
   orientacją instancji świata (placement instancji wymagałby id+pozycji+orientacji
   RAZEM; mamy orientację prymitywu BEZ id i BEZ udowodnionej pozycji świata).

## ALTERNATIVE_HYPOTHESES (obowiązkowa tabela; rozstrzygnięcia POMIAREM)

| Hipoteza alternatywna (dla interpretacji nośnej) | Pomiar dyskryminujący | Wynik |
|---|---|---|
| A1: rekordy TYPE0 to POZYCJE ŚWIATA instancji (f1–f3 = world XYZ) | zakresy f1–f6 per-plik (dowód 4) + brak id (dowód 1) + join per-template B (dowód 3) | WYKLUCZONA jako wspólna klatka świata; per-rekord pozycja świata pozostaje UNDETERMINED, ale bez id modelu nie może być rekordem placementu — klasa *_YES_* niemożliwa |
| A2: artifact wyrównania (pola z niezestrojonych bajtów) | równanie strukturalne 4+count×36 == packed dla 1686/1686 TYPE0; dual decode A/B 0 rozbieżności na 675 polach; kontrole negatywne (wrong-endian/truncated/wrong-width) FAIL na obu dekoderach (4/4×3) | WYKLUCZONA |
| A3: struktura zagnieżdżona/błędnie odczytana jako pola (np. stride 12, nie 36) | solver grid B rozstrzygnął 36 przez spójność wzorca intra=24 + kalibrację korpusową; pod-grid 12 B istnieje arytmetycznie (12 | 36) i jest JAWNIE zapisany jako stride_solutions w DECODE_B.json; negatyw: wartości kątowe f9 pojawiają się sensownie tylko w siatce 36 | WYKLUCZONA dla próbek; dwuznaczność solvera udokumentowana |
| A4: zera w f7/f8 to padding, nie kąty | 6,040 rekordów z f8 ≠ 0 (π, ±π/4, π/36) i 6,058 z f7 ≠ 0 (do π/2) — pole przenosi rzeczywiste wartości kątowe; padding nie przyjmuje ±π/36 | WYKLUCZONA |
| A5: odniesienie pośrednie do modelu (schemat/obliczenie zamiast prostego id) | reinterpretacje u32/u16 = 0/675 (u32) + koincydencje 0.37% (u16) — brak dowodu na JAKIKOLWIEK mechanizm pośredni; konsument z P5 (dowód 3) wskazuje rolę zasobu per-model | NIEROZSTRZYGNIĘTA statycznie w pełni (nie można wykluczyć każdego schematu pośredniego), ale bez konsumenta-placementu hipoteza nie ma nośności; klasa *_YES_* nie wymaga jej wykluczenia — id jest NIEOBECNE (dowód 1), a to wystarcza: placement-record bez id nie spełnia definicji z §2 kontraktu |
| A6: 15 plików INNE (0.80%) może być placementami | nagłówki `01 00 xx 00` — NIE zdekodowane w tym runie | OTWARTA dla 15/1865 (0.80%) — RESUME_POINT; nie wpływa na klasę próbki 4/4 ani na 99.2% korpusu |
| A7: ogon TYPE1 (154,314 B = 80.9% w 584781) może zawierać placementy | NIE zdekodowany (budget) | OTWARTA dla tego segmentu — RESUME_POINT; jawnie niesklasyfikowana część payloadu 584781 |

## Statusy kanoniczne (§6 kontraktu — przytoczone werbatim, NIETYKANE)

```text
HISTORICAL_BUILDING_PLACEMENT   = NOT_ESTABLISHED
MODEL_218757_TO_WORLD_INSTANCE   = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED              = NO
HISTORICAL_WORLD_INSTANCE        = NOT_ESTABLISHED
PE_AXES_AND_UNITS                = UNVERIFIED
```

Ten run NIE proponuje supersesji żadnego z powyższych (wynik NOT_PLACEMENT_DATA jest
spójny z kanonem; era-2003 BVI=collision zostaje potwierdzona dla PCG_9_3_5 na poziomie
payloadu — jako nowy pomiar, bez zmiany kanonu §6).
