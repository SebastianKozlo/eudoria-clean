# CAMERA_UI_AND_ASSET_LAB — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Kontrakt §5 + §7. Pomiary przeglądarkowe w raw/BROWSER/INTERACTION_SCENARIOS.json
(izolowana instancja Edge headless + CDP; surowe PNG prywatnie; 0 błędów stron).

## 1. Kamera (§5)

- **Preset referencji** (faktycznie serwowany viewer 9350, pin
  LIVE_REFERENCE_CAMERA.json): FOV 45, enableDamping, dampingFactor 0.08,
  minDistance 10, maxDistance 50000, far 200000. ZASTOSOWANE. Near: 0.5 +
  `logarithmicDepthBuffer: true` — uzasadniona zmiana dla skali świata
  (bliskie drzewa i 14-kilometrowy LOD w jednej frustumie bez z-collapse;
  wybór renderera, NIE twierdzenie o jednostkach PE).
- **Streaming za fokusem** (WL-4): orbit → controls.target; fly/walk →
  camera.position. Pomiar S2: trzy F z rzędu — origin okna 3× IDENTYCZNY
  (PRE: dryf (53,114)→(68,129)). R analogicznie (spawn focus; settle na
  realną powierzchnię — brak y=0).
- **Przejścia trybów**: S3 — orbit→fly→walk→orbit: max przesunięcie XY
  kamery **0** („nie skacze do innego miejsca”); orbit pivot prze-celowuje
  na oglądany punkt (_lastFlyFocus), oryginalne wierzchołki nietknięte.
- **Interaktywna referencja 9350**: porównanie interaktywne „feels” z
  referencją NIE było wykonywane (standing 9350 dostępny tylko HTTP w tej
  sesji; nie przejmujemy cudzych sesji) → **REFERENCE_INTERACTION_NOT_
  VERIFIED** — nie twierdzimy identycznego feelingu z samego współczynnika;
  preset cyfrowy + struktura fit (center+maxDim×1.8+kierunek 0.7/0.6/0.7)
  są przejęte z faktycznie serwowanego kodu (pin SHA 6CA4D619…).

## 2. UI (§5)

- **Canvas ≥85%/80%**: S1 zmierzył canvasFrac (width/height vs viewport
  1280×720): PASS (full-bleed layout; drawer to overlay).
- **Drawer „Szczegóły”**: domyślnie zwinięty, stan w localStorage; sekcje:
  ładowanie/błędy + spójność sceny, profil/seed/gęstość (aplikacja =
  forceNew scene request), teleport, census (renderer info + LOD + cache),
  punkt debug, sterowanie, dowody, diagnostyka. Usunięty stały sidebar
  480px; action-bar jest jedną pozycjonowaną belką (bez nakładania headera).
- **Klawisze**: pola drawer nie przechwytują ruchu (S6: podczas pisania W
  nie porusza; po blur porusza — isTypingTarget gate); resize NIE resetuje
  kamery; drawing buffer podąża (S9: buffer 1280→960 szer. inny, kamera
  stała).

## 3. Asset Lab (§7)

- **Widok**: `/assetlab` — duży viewport, ten sam orbit preset + fit
  (AABB center, maxDim×1.8, kierunek 0.7/0.6/0.7, tło 0x1a1a2e, Hemisphere
  0xb0d0ff/0x806040 0.8 + Directional 1.2 — VIEWER SETTINGS za referencją
  9350, nie dane PE), drawer ze statusem witnessa, łańcuchem provenance,
  diagnostyką slotów i mapą wyświetlania.
- **Witness PCG 519316** (startowy, zgodnie z kontraktem): pełny łańcuch
  LIVE: `/api/world/model/519316` (bounded ORIGINAL payload 540 469 B z
  przypiętego PCG_9_3_5 Models.bnt) → parseWitnessModel (v10.1.0.0, 22
  bloków; production reader — żaden nowy loader) → 3 kształty
  bridge_02:0/1/2 → NiTexturingProperty → NiArkTextureExtraData (6 wpisów)
  → sloty W KOLEJNOŚCI przez decodeModelTextureStrict → **3/3 kształty
  TEKSTUROWANE** (S10: „teksturowane 3, bez tekstur 0”; sloty pominięte 0).
  Sześć nazw tekstur rozwiązywanych do RZECZYWISTYCH wpisów tej samej ery:
  518860/518862 (DXT1), 516807 (DXT1), 519227 (TGA A32 512×512 — DARK/
  DETAIL). Status DECODED katalogu NIE był założeniem — łańcuch zmierzony
  na żywo (provenance w drawerze: era/kontener SHA/wpis/payload SHA).
- **4 proxy CD jako KONTROLA** (192374/193207/193313/193684): z przypiętego
  `Models.ark` (SHA F660D055…, era CD_JAN_2003 — ODRĘBNA tożsamość
  mount/cache; PCG route nadal odrzuca era=CD). Parse przez bounded nif41
  reader SERVER-side (importuje node:fs — nie jest modułem klienckim);
  przeglądarka renderuje **wire** z `/api/world/asset/cd/<id>/wire`
  (FILE_SCENE: BEZ konwersji jednostek i osi; odwracalny CENTERED offset
  pokazany w drawerze). Status SOURCE-UNTEXTURED per ustalenie katalogowe
  (brak UV/texture bindings w zbadanych payloadach) — jawny neutralny
  materiał, ZERO wymyślonych bindingów. S10: wszystkie 4 wybrane
  interaktywnie, każdy ze statusem (np. 193313: NIF 4.1.0.12, 5 kształtów,
  SOURCE-UNTEXTURED).
- **Eras nie mieszane**: PCG witness i CD controls to ODRĘBNE pozycje
  selektora z osobną erą w statusach; żadne cross-era resolution.

Kontrola world vs Asset Lab RAPORTOWANA OSOBNO: świat (S1–S9) wyżej; Asset
Lab = S10 + pixel captures assetlab_*.png (nontrivial; BROWSER_INTERACTION).

ALL_NIFS_SUPPORTED = NOT_ESTABLISHED (Asset Lab to kontrola jednego
witnessa + 4 proxy; nie „wszystkie NIF-y”; 225492 i kontrolery tekstur —
poza zakresem, bez nowych rodzin loaderów w tym runie).
