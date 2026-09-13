# 02_ANALYSIS — C. Źródło transformacji instancji (sekcja C kontraktu) + D. brak placementu

RUN: PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912 | ERA: EU 9.3.5 | Entropia.exe SHA256 E7785430...

## C.1 Co prześledzono (świeże poszukiwanie, bez transferu hipotezy PE2)

Poszukiwano ścieżki tworzenia instancji świata i miejsca ustawiania transformacji
(pozycja/obrót/skala). Zbadane wejścia:

1. **Ścieżka avatar/consumer kompletnego A** (FUN_006b4c50): po załadowaniu zasobu modelu
   encja dostaje obiekt zasobu (pole +0x1b8/+0x1bc) i woła vtable[+0xA4] na obiekcie
   [param_1+0x18] — dalsze ustawianie transformacji NIE zostało osiągnięte (vtable
   [+0xA4]/[+0xA8] na klasie encji nie zdekomponowane w tym runie).
2. **Ścieżka fabryki żądań** (FUN_00511070 → request-struct → FUN_006c0d50): utworzenie
   obiektu 0x130 = **ArkModelManagerMain** (`*obj = ArkModelManagerMain::vftable`,
   ctor-part FUN_006c8f80 = `*obj = ArkModelManager::vftable` — dziedziczenie) — menedżer
   modeli; transformacja instancji NIE tutaj.
3. **Klasy RTTI istniejące w binarium**: ArkAnimationTransform / ArkAnimationTranslation /
   ArkAnimationRotation / ArkAnimationScale (animacje!), ArkClientCameraController,
   ArkBillboardNode, ArkNode-podobne — to warstwa ANIMACJI, nie placementu instancji.
4. **Warstwa sieci**: dekoder strumienia serwera (odpowiednik PE2 FUN_005977b0 create-object
   z rekordami 0x1C + transform XYZ) NIE został zidentyfikowany w tym runie.

## C.2 Gdzie łańcuch się urywa (dokładnie) i czego brakuje

- URYWA SIĘ na: wejściu "create world instance from network message". Znane runy
  (PE_STATIC_WORLD_EU_PARSE_R1_20260903, 06_synthesis.md) wskazują: "the DYN1 server-stream
  reconstruction" = OCZEKUJĄCE (open) dla ery EU; żaden run go nie wykonał. Ten run potwierdza:
  wśród 25 call-site'ów lookupu template (S10) i 13 callery pumpu modeli (S20) żaden
  nie nosi cech dekodera pakietów sieciowych z rekordami f32 XYZ.
- BRAKUJE: (a) identyfikacji funkcji dekodującej strumień serwera (create-object message),
  (b) funkcji ustawiającej transformację instancji (odpowiednik vtable[0x50] set-position z PE2),
  (c) sprawdzenia czy rekord sieciowy EU 9.3.5 ma strukturę 0x1C + sub-rekord transformacyjny
  jak w PE2 (TO JEST NIEPRZENIESIONA HIPOTEZA — do własnej weryfikacji w dedykowanym runie).
- Status hipotezy PE2 (server-delivered placement): POZOSTAJE HIPOTEZĄ dla 9.3.5. Żadne
  twierdzenie o źródle transformacji w 9.3.5 nie jest tutaj robione.

## C.3 D. Odzyskanie historycznej lokalizacji

**NIE ZNALEZIONO (uczciwy brak)**. Ten run był misją mechanizmu (statyczny trace),
nie placementu. Żadna historyczna pozycja budynku nie została odzyskana; nie wykonano
żadnego mock-spawn/ręcznego wstrzykiwania instancji (zabronione kontraktem).

## C.4 Ogniwa pozytywne (dla przyszłego runu placementu)

- Transformacja modelu per-instancja MUSI przechodzić przez menedżer sceny/modeli
  (ArkModelManagerMain/ArkModelManager — VA: ctor 0x006c0d50/0x006c8f80;
  13 callery FUN_006c9700 = potencjalne miejsca attach modelu do encji).
- Kolejność pracy dla przyszłego runu: (1) zdekodować warstwę sieci (login/stream),
  (2) znaleźć create-object handler, (3) śledzić transformację do vtable set-position.
