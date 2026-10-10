# UNRESOLVED_AND_NEXT_SEAMS — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Co pozostaje NIEROZSTRZYGNIĘTE po tym runie (żadne z poniższych nie jest
nowym twierdzeniem science; to jawne szwy do przyszłych kontraktów).

## Otwarte ograniczenia produktu (zbadane, uczciwe)

1. **Slot tekstury modelu — ktory slot renderował 9.3.5**: UNRESOLVED.
   Adapter bierze PIERWSZY rozwiązywalny wpis Ark w kolejności (BASE→DARK/
   DETAIL) jako RENDER_RECONSTRUCTION; albedo historyczne nieodzyskane.
   Następny szew: RE ścieżki materiałów 9.3.5 (albo dowód slotu z binarium).
2. **DDS mips**: dekoder kwalifikuje TOP-LEVEL mip (łańcuch mipów pozostaje
   nieczytany w payloadzie; mipsDeclared=9 dla 166881 — podawane jawnie).
   LOD tekstur (trilinear/anisotropic) to przyszła decyzja renderera.
3. **Far LOD dostępność**: census-gated (~10–120 s po starcie serwera;
   klient pokazuje PENDING, 503 bez placeholdera). Opcjonalny przyszły
   szew: persystentny cache far po stronie serwera między startami.
4. **Mid/far wydajność**: jeden wielki mesh far (1.6M trójkątów,
   frustumCulled=false) — do profilowania FPS i ewentualnej segmentacji
   na słabszych GPU. FPS NIE był bramką tego kontraktu (czasy przebudów
   0.9–1.4 s i renderer.info zmierzone).
5. **Asset Lab scope**: witness 519316 + 4 proxy CD (kontrola).
   ALL_NIFS_SUPPORTED = NOT_ESTABLISHED. 225492.nif (NiTextureTransform-
   Controller jako pierwszy blocker) i pozostałe FAILED z katalogu —
   cel późniejszych etapów (kontrakt zabrania dodawania rodzin loaderów
   „tylko po to, by otworzyć wszystkie FAILED” w TYM runie).
6. **Regional preview**: mapa NASZA (region=tile>>5 → profile 0/2/7/19).
   ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED; profile same nie
   determinują lokalizacji. Gdy join kiedyś będzie dowiedziony — mapa
   zostanie zastąpiona dowodem, nie przez nasze domysły.
7. **Markery UNSUPPORTED_MODEL**: diagnostyka (czerwone wireframe boxy)
   — rola „wyglądu drzewa” dla modeli bez łańcucha texprop→Ark pozostaje
   UNVERIFIED (BVI/kolizja — nie renderowane jako wizualne).
8. **Woda**: NOT_RECOVERED (bez zmian). Raw u16=0 to DANE.
9. **Pointer lock w headless**: odrzucany (jak w R1) — aplikacja ma widoczny
   komunikat + działający drag-look; pełna weryfikacja pointer-lock w
   headful przeglądarce — do niezależnego post-audytu (Desktop ma headful).
10. **Pozycje**: jednostki adaptera (CURRENT_RUNTIME_CALIBRATION) —
    oryginalne osie/jednostki PE UNRESOLVED (bez zmian; nie „oryginalne XYZ”).

## Następne szwy (kandydaci do przyszłych kontraktów — NIE autoryzowane)

- RE ścieżki materiałów/albedo 9.3.5 (slot dowodu) → jeśli dowód: podmiana
  RENDER_RECONSTRUCTION na status SOURCE-CONFIRMED w splat/model chain.
- NIF family support (TextureTransformController/TextureEffect) — najpierw
  census wersji i bloków, potem kontrolowane rozszerzenia (poza tym runem).
- Persystentne cache serwera (far/decymowane bloki) między startami.
- Building placement (priorytet projektu — NIE dotknięty tym runem):
  HISTORICAL_BUILDING_PLACEMENT = NOT_ESTABLISHED; 218757 →
  MODEL_218757_TO_WORLD_INSTANCE = NOT_ESTABLISHED.

## Otwarte pytania z QC

- Żadne FAILED bramki (139/139 testów, 10/10 scenariuszy przeglądarkowych,
  7/7 wartości bramek). Otwarte nie-FAILy: REFERENCE_INTERACTION_NOT_
  VERIFIED (feel 9350) — patrz BROWSER_INTERACTION; PERFORMANCE measured
  w one-pass scenario (dłuższe profile w kolejnym runie, jeśli kontrakt
  zechce).

## Verbatim (kontynuacja §10)

```text
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```
