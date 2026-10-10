# ROSETTA_RUNTIME_PROVENANCE — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Kontrakt §7: „Zachowaj działającą ścieżkę oryginalne pliki PE → nasze
czytniki/Rosetta → resolver → scena → Three.js… Nie zamień aplikacji w
ręcznie poukładaną scenę z hardcoded mapą albo wyłącznie eksportowany GLB
bez traceability.” Niniejszy dokument potwierdza, że R2 utrzymuje TĘ SAMĄ
wykonywalną Rosettę (rozszerzoną, nie przepisaną).

## Ścieżka danych (production, bez side-decoder)

```text
oryginalne archiwa (piny SHA256, fail-closed):
  Terrain\terrain.bnt            125 064 817 B  95841761CE4EA074…
  VegetationClimates\…bnt            25 346 B  7B858401C3EEBDA5…
  Models\Models.bnt             395 412 868 B  C950A8C26F2063F4…
  Textures\Textures.bnt          973 942 771 B  61ACD13B140E1306…
  (Asset Lab controls) Models.ark 128 742 137 B  F660D055B4B9471B…  [era CD_JAN_2003]
        │
        ▼ PESourceMount (era PCG_9_3_5; BNT2_TERRAIN/BNT2 framing; era gate ?era=)
  getTerrainTile        → TDF offset 64, RAW uint16 32×32/kafel (nigdy offset 52)
  getTerrainMaterials   → named records, mask@record+56, RAW wagi
  resolveTexture        → id@+16 → „<id>.dat” (chain potwierdzony silnikowo)
  getVegetationClimate → strict .vcl (25 UNSUPPORTED — bez konwersji)
  LazyModelArchive/LazyTextureArchive → bounded single-entry reads (nigdy cały kontener)
        │
        ▼ serwer loopback 127.0.0.1:8163 (allowlist statics; bounded APIs)
  /api/world/tile/<g>/<g>[+/meta+/materials] /texture/<id> /model/<id>
  /climate/<0..31> /climates /status /overview[/progress] /gaps
  R2: /far /lod8/<bx>/<by> /asset/cd/<pinned proxy>[+/wire]
        │
        ▼ klient (ten sam produkcjny kod co serwer dla dekoderów)
  TerrainTile → PETerrainRegion (near 8×8 RAW) + PEHeightField (halo 10×10,
  triangle-exact, jedyna wysokość dla renderingu/drzew/spaceru)
  PEFoliageLabSeed v2 (wrapper; PEFoliageCore BYTE-LOCKED) → WorldVegetation
  (fair cap, statusy instancji, slot-order texture chain)
  NifModelReader (witness v10.1.0.0) → buildShapeRenderables → Three.js
  DdsDecoder (DXT1/DXT5 strict subset — kwalifikowane na payloadach runu)
  WorldLod (mid/far decymowane RZECZYWISTE próbki; policy renderera)
        │
        ▼ Three.js r185 (0.185.0 pinned; node_modules THIS worktree)
  WebGLRenderer (logarithmicDepthBuffer) — scena /world + /assetlab
```

## Traceability (co jest CZYM)

- Kafel: era+container SHA+wpis (X-PE headers + makeProvenance) —
  identyczność cache CAM-C3 sprawdzana przy KAŻDYM hicie (odmowa przy
  mismatch, nie ciche użycie).
- Model: entryName `<id>.nif` + payload SHA (X-PE-Payload-Sha256) + SHA
  kontenera — reader kwalifikowany odmawia GŁOŚNO (UNSUPPORTED, nigdy
  zamiennik).
- Tekstura: numeric id → „<id>.dat” (era gate: PCG_9_3_5 ONLY; próby
  cross-era odrzucane PRZED dostępem do danych).
- Punk debug (klik w /world, orbit): era + containerSHA + wpis (+payload
  dostępny przez /meta/route headers) → dekoder/schema → obiekt sceny →
  zastosowana polityka (LOD/kalibracja/mostki rekonstrukcji) — w drawerze.
- Slot tekstury modelu: pierwsza rozwiązywalna w kolejności wpisów Ark =
  RENDER_RECONSTRUCTION (albedo historycznego materiału — UNRESOLVED;
  żadna użytą teksturą TGA nie „odzyskuje” materiału).
- Regional preview: mapa NASZA (REGIONAL_PREVIEW v1; profile 0/2/7/19);
  oryginalne profile same nie determinują lokalizacji —
  ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED.
- Oryginalne bajty ≠ dowód przypisania: rozdział zachowany (ground albedo
  pozostaje RENDER_RECONSTRUCTION dla roli/UV/cell sampling; brakujące
  wejście palety = brak konkretnej zależności, nigdy losowy fallback).

## Czego ta Rosetta NIE twierdzi

- Nie odtwarza historycznych XYZ/osi/jednostek (CURRENT_RUNTIME_
  CALIBRATION = preset z provenance; pozycje = jednostki adaptera).
- Nie jest placementem budynków (HISTORICAL_BUILDING_PLACEMENT =
  NOT_ESTABLISHED; model 218757 nigdzie nie postawiony).
- Nie jest stock-PE pagingiem (LOD near/mid/far = polityka renderera).
- Nie twierdzi pełnej obsługi NIF (witness scope; ALL_NIFS_SUPPORTED =
  NOT_ESTABLISHED).
- Cache są odtwarzalne z pełną identycznością wejść (era+SHA+wpis+wersja
  polityki) — brak „ręcznie poukładanej sceny”; żaden GLB-export nie
  zastępuje łańcucha.
