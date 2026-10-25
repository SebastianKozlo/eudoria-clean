# FRONTIER — PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025

RUN_ID: PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025 | BUILD: ISO2003NOV_PE_5_1_0_0 | DATE: 2026-10-25
PROVENANCE: sekcje "next edge" wszystkich RESULT jobów + QC findings + MODEL_BINDING_CERTIFICATE_J03_CORRECTED/J05. Companion strict: RESEARCH_BACKLOG.json.

## Ranking residualnych krawędzi (kolejność wg siły dowodowej × kosztu)

1. **Residual-14 witryn `call [reg+0x3C]` + inner wrappera 0x498B80.** Jedyny pozostały slot+0x3C lane w section1. Najsilniejsza witryna 0x498C50 (wrapper 0x498B80, ret 8, (arg1,arg2) verbatim, retval pass-through); inner = [svc_result+0x38] z serwisu [0x6C4F20], keyed 0x19A — klasa inner = runtime → wymaga danych runtime (np. rozszerzenia corpusu o sekcje PE z vtable wrappera) albo ścieżki dynamicznej (poza zakresem STATIC_ONLY). Druga witryna: 0x56FA46 (ramię default/case-1 switch-dispatchera @0x56F9F0; receiver wybierany runtime przez [command+8]).

2. **Post-52A130 flow 0x526AE0 (0x526CFA+).** Najbliższy zmierzony styk lane (d) ze stroną SFO: co konsumuje entry zwrócony przez 52A130 @0x526CC9 w funkcji operującej na per-name obj + member +0x18; czy wartość trafia do [SFO+0x10] przez 5257C0. Statycznie mierzalne w section1 (bounded decode ogona 526AE0).

3. **Registry [0x6C62F4] consumer surface.** Kto iteruje/query-uje registry i dispatchuje które sloty z jakimi argumentami: callery 5077C0/5072C0 (query/register API), 468010-tree archetype-B surface (51C930), niezbierane formy jmp [reg]. Ta powierzchnia niesie ZARÓWNO kontrmodel caller-a fabryki (slot-0 na M+0x08 z 6 pushami), jak i proweniencję wartości czytelników M-cell (nośnik 0x19A). Pozostałe sloty nośnika 0x19A (0x5D6900-family, 0x5DD9E0/0x5DD9F0, 0x5DDD50..0x5DE260) niedekodowane.

4. **Sekcje PE poza section1.bin.** Vtable wrappera 0x498B80, rejestracje RTTI 0x6C3898/0x6C3A0C (deskryptory runtime-init), import [0x65A1A8], serwis [0x6C4F20], cell vector +0x1004C/50/54 (VA 0x6D6340+ — poza obrazem). Wymaga decyzji o rozszerzeniu corpusu (sekcja .data/IDT późniejszych sekcji PE.exe) — nowy pin, nowa fala.

5. **Realny caller fabryki (slot-0 na M+0x08).** Nieznaleziony w CAŁYM zmierzonym zakresie statycznym (D01 global/escape; D02 registry; D03 slot-22; D04 [M+0x8C] + M-cell readers). Residual forms jawnie wyliczone (CLAIMS C12). Jeśli kolejna fala statyczna (1-3 powyżej) nie domknie — wymagane dane runtime (poza zakazem tego runu; projekt przyszłego testu, nie wykonanie).

6. **a1..a6 upstream.** TO SAMO co 5: dowiązanie źródła argumentów = dowiązanie caller-a fabryki. Kandydackie klasy źródeł (parser/VM/tabela/proceduralne/default/cache/wiadomość) — wszystkie pozostają UNKNOWN w zmierzonym zakresie.

7. **468010 deeper nodes (>36 message ids)** + singleton first-field object (500BB6 teardown path) — pokrycie message-id dispatch (niży priorytet; nie niesie mostu modelowego bez registry-consumer surface).

8. **Waves pomocnicze (niewykonane w R5, wymagają osobnej decyzji):** gałąź T (anomalia 417BE7→414C9E/414C9F w packheader obrazu — nie analizowana w R5, bez heurystycznych napraw, R4-A08 upheld); gałąź C (cache/persistence 5.1 — brak uzasadnienia z nauki źródła wartości; notatki 180 plaintext cache-records / 3949 decrypted strings pozostają referencyjne, nie dowodzą placementu).

9. **EmulationReadiness 46F0A0/46F0C0** — macierz pozostaje MATERIAŁEM PROJEKTOWYM przyszłych testów; R5 nie autoryzował emulacji oryginalnych funkcji; brak wykonania.

## Granice wiedzy runu (explicit)

- STATYCZNE section1.bin TYLKO; wszystkie "brak" = SCOPED_NEGATIVE w zmierzonych formach, nie globalna nieobecność (LOCAL_SOURCE_EXHAUSTED=NO).
- BARRIER-y runtime: klasy inner/receivery/deskryptory RTTI/serwisy — niewyznaczalne z bajtów obrazu bez danych runtime lub sekcji poza section1.
- Kontrmodel wspólnego runtime namespace nazw (message-name == open-by-name key) pozostaje UNREFUTED; połowa tworzenia potwierdzona (J03), połowa konsumpcji otwarta.
- Historyczne położenie obu modeli: NOT_ESTABLISHED; autentyczne położenie wymaga modelu, konkretnej instancji, oryginalnych wartości i ramy (kontrakt §14) — żadnego z tych dowodów ten run nie dostarczył.
