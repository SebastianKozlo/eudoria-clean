# R1_RECORD_SUPERSESSION — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Data: 2026-10-10. Zlecenie: kontrakt R2 (§2). Ten plik jest NOWYM rekordem
superseding w pakiecie R2. Żaden historyczny pakiet audytowy nie został
zmieniony; nie ma retroaktywnej autoryzacji; nie ma edycji R1.

## 1. WL-6 — LITERAL_ORIGINAL_BASE_GATE_COMPLIANCE = FAIL (ujawnienie zachowane)

Zamrożony kontrakt WORLD LAUNCHER R1 (§1.2–1.3, zachowany cytat ze
zweryfikowanego wejścia Desktop REPORT.md SHA256
0E4018ECFF6107303FE5B63DE360C6CC5B95DA02257048D9BA524CBC36FF3AE3) wymagał
remote SOURCE_BRANCH == f71eb30… i worktree dokładnie z tego SHA; przy różnicy
miał nastąpić BLOCKED_BASE_CHANGED. Faktyczny commit R1:

- R1 commit (publikacja): `44ef254b8ff9ebb05bd104690181c202678c065d`
- actual parent (POMIAR ŚWIEŻY w tym runie, `git rev-parse 44ef254^`):
  `e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c`
- literalny pin kontraktu R1: f71eb30…

**LITERAL_ORIGINAL_BASE_GATE_COMPLIANCE = FAIL.**
**HUMAN_EXACT_BASE_EXCEPTION = NOT_ESTABLISHED_IN_REVIEWED_INPUTS.**

Jawne wcześniejsze zlecenie poprawki kamery (katalog, e9bb1f5 — dwa pliki
compat/catalog-app.js i compat/catalog-preview.js) nie jest dowodem osobnej
ludzkiej zmiany pinu kontraktu. Decyzja PE-MASTER i ancestry nie dowodzą
wyjątku. Poprawne pomiary bajtowe R1 (mount/readers, manifest 93/93, archiwa
4/4) pozostają zachowane i nienaruszone; to ujawnienie dotyczy zgodności
zapisu kontraktowego, nie poprawności pomiarów.

## 2. Superseding werdyktu produktu R1

R1 zakończyło się `PRODUCT_VERDICT=PASS_IN_IMPLEMENTED_SCOPE` przy jednoczesnym
ujawnieniu `INTERACTION=NOT_PERFORMED` (pointer lock odrzucony w przeglądarce
audytowej; pełny lot/spacer niezweryfikowany). Kontrakt R1 §8 wymaga rzeczywistej
interakcji; przy jej braku NOT_PERFORMED/PARTIAL, nie PASS. W nowym rekordzie
(R2) szeroki product PASS R1 zostaje cofnięty:

**R1_PRODUCT_VERDICT_SUPERSEDED = PARTIAL / REQUIRE_CORRECTIONS.**

To NIE jest retroaktywna zmiana opublikowanego pakietu R1
(docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ pozostaje READ_ONLY, byte-nietknięty)
i NIE unieważnia zachowanych wyników pomiarowych R1. Jest jawnym rekordem
korekty kwalifikacji gotowości wymaganej funkcji w nowym runie, wykonanym na
podstawie: (a) zweryfikowanego SHA-ami raportu Desktop post-audit
(REQUIRE_CORRECTIONS_IN_EXAMINED_PRODUCT_SCOPE), (b) własnej reprodukcji
WL-1..WL-5 w PRE tego runu (PRE_COUNTERCHECKS.json — wszystkie odtworzone na
rzeczywistych funkcjach produkcyjnych BASE), (c) świeżego pomiaru parenta R1.

## 3. Zachowane wyniki R1 (bez zmian)

- Ścieżka oryginalne pliki PE → PESourceMount/readers → resolver → scena →
  Three.js: potwierdzona, zachowana w R2.
- Montowanie 4/4 archiwów PCG 9.3.5 z pinami SHA256 (terrain.bnt,
  VegetationClimates.bnt, Models.bnt, Textures.bnt): zweryfikowane ponownie
  w preflight R2 (4/4 zgodne).
- Manifest pakietu R1: 93/93 bijekcja (kontrola Desktop, zachowana).
- WORLD_XYZ_RECOVERED = NO (niezmienione; jednostki adaptera, NIE oryginalne XYZ).

## 4. Nowa autoryzacja R2 nie zmienia zgodności R1

Kontrakt R2 wiąże actual BASE `44ef254b8ff9ebb05bd104690181c202678c065d`
(EXPECTED_BASE_SHA; świeży ls-remote zgodny przed startem i przed commitem).
To jest NOWE, jawne upoważnienie człowieka do runu na tym SHA — nie jest
retroaktywną autoryzacją wyboru BASE w R1 i nie zmienia oceny §1 tego pliku.

## 5. WL-1..WL-5 — rozliczenie w tym runie

PRE (odtworzone, PRE_COUNTERCHECKS.json):
- WL-1 REPRODUCED — nowsze żądanie roślinności ginie przy vegBusy/buildBusy.
- WL-2 REPRODUCED — 2304 instancje; 14 poza siatką próbek mesha (fallback y=0);
  1275 niezerowych różnic bilinear↔triangle; max 0.953125 j.a.;
  walk-nearest↔triangle max 15.8203125 j.a. (origin 53,114, profil 0, seed 0,
  gęstość 50, rzeczywiste payloady).
- WL-3 REPRODUCED — (100,10,100)→(100,10,88) przy null ground mimo bannera.
- WL-4 REPRODUCED — (53,114)→(58,119)→(63,124)→(68,129).
- WL-5 REPRODUCED — 6144→5000 usuwa 11/64 kafli wyłącznie kolejnością; 4 grupy
  nakładających się instancji 166878 (rec 8/9, brak recIndex w hashu pozycji);
  przy 50% instancjonowane tylko 3 ID.

POST (po implementacji R2): patrz POST_COUNTERCHECKS.json — każde z findings
musi wykazać naprawę na tej samej produkcyjnej ścieżce (lub uczciwe
NOT_FIXED). Bramki oddzielne: DATA_READ_PATH / PRODUCT_LOAD / PIXEL_RENDER /
INTERACTION / CONTINUOUS_WORLD / ASSET_LAB / PERFORMANCE (§8).

## 6. Zachowane frazy statusu (verbatim, kontrakt §10)

```text
HISTORICAL_TREE_DISTRIBUTION = NOT_ESTABLISHED
ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED
HISTORICAL_BUILDING_PLACEMENT = NOT_ESTABLISHED
MODEL_218757_TO_WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
ALL_NIFS_SUPPORTED = NOT_ESTABLISHED
FULL_ORIGINAL_GAME_REIMPLEMENTED = NO
CANONICAL_GATE_EFFECT = NONE
INDEPENDENT_DESKTOP_POST_AUDIT = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```
