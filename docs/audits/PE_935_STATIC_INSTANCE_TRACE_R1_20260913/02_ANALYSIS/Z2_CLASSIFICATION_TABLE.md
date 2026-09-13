# Z2 — KLASYFIKACJA 25 LOOKUP + 13 PUMP CALL-SITE'ÓW (GA-CLASSIFY)

RUN: PE_935_STATIC_INSTANCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)
Binarium SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
Klasy: STATIC_WORLD / AVATAR_EQUIPMENT / PREVIEW_UI / VEGETATION / MODEL_MACHINERY / OTHER / UNKNOWN.
Dowód = dekompilacja callera (S10/S20 poprzedniego runu — to samo binarium, ten sam SHA,
re-weryfikacja bajtowa S9: 38/38 call-site'ów zgodnych bajtowo, 0 mismatch) + własne dekompilacje GA4-GA8.

## A. 25 call-site'ów lookupu FUN_0072f580 (rejestr template'ów)

| # | call-site VA | caller | klasyfikacja | dowód (1-3 zdania + stałe/klasy) | pewność |
|---|---|---|---|---|---|
| 1 | 0x00511252 | FUN_00511070 | AVATAR_EQUIPMENT | Hardcode 11769=0x2DF9 @0x00511245 (slot template'u); lookup→getter A→żądanie modelu slotu; wywoływany z łańcucha 005F6990 (avatar visual setup) i z FUN_004c5bd0-chain. | WYSOKA |
| 2 | 0x006BAB46 | FUN_006baa20 | OTHER (ctor obiektu z template'em) | Ctor (vft DAT_00ba4618): param-sety 0x4E26=20006/0x4E48=20040 + atrybut 0x3D1C ("face" wg FUN_004c5580); czyta avatar-id (FUN_00977780/FUN_004926e0); lookup→walidacja→template@[+0xC]. | ŚREDNIA (avatar-adjacent, ale sam ctor generyczny) |
| 3 | 0x00733517 | FUN_00733490 | OTHER (system atrybutów) | Iteruje 3 rekordy (stride 6×4): jeśli id@+0x0C≠0 a tpl@+0x14==0 → FUN_00976770(0x3D35) → param-set 0x4E26 → lookup → zapis tpl. Rezolwer referencji template'owych w rekordach parametrów. | WYSOKA |
| 4-8 | 0x006C26EB/0x006C2736/0x006C2787/0x006C27D7/0x006C282A | FUN_006c26b0/2700/2750/27a0/27f0 | OTHER (rodzina getterów tabelarycznych) | FUN_006c26b0: tabela DAT_00A85608 (34 sloty: `sVar1<0x22`), indeks [slot+row*0x22] → id → lookup. Tabela "ClickTargetNode" (symbol Ghidra @0x00A85608-obszar). Getter-y służą avatar/UI/body-set (FUN_006c2840/2870 używane przez FUN_006b4c50). | WYSOKA (rodzina; aucun placement) |
| 9 | 0x006C3F62 | FUN_006c3f50 | MODEL_MACHINERY (emiter pary) | lookup(param_1) → `local_8=0x66; local_4=FUN_007ce1e0()` → buduje parę {typ=MODEL, A} → wkłada do listy żądań (wektor @param_2). Most lookup→pump. | WYSOKA |
| 10 | 0x0056736D | FUN_00567170 | OTHER (rejestracja derived-record z transformem) | Czyta atrybuty (floats, FUN_008492c0-class); lookup→FUN_005670a0 (copy do węzła); buduje rekord POCHODNY z pozycją@+0x08 (FUN_00730f90 @0x0056739B) i rotacją@+0x14 (FUN_00730fb0 @0x005673BA) — maszyna placementu runtime. | WYSOKA (mechanizm), NISKA (czy obsługuje statyki — NIEROZSTRZYGNIĘTE) |
| 11-12 | 0x006C285E/0x006C288E | FUN_006c2840/006c2870 | OTHER (gettery slotów body-set) | Używane przez FUN_006b4c50 (avatar body-set ×2 → A ×2 → pump ×2). | WYSOKA |
| 13 | 0x006E28E4 | FUN_006e2610 | AVATAR_EQUIPMENT (adjacent) | Czyta avatar-id (FUN_004926e0/FUN_00977780 → [this+0x28]); lookup(param_2)→FUN_005670a0→walidacja — rejestracja template'u avatara. | ŚREDNIA |
| 14 | 0x00848F26 | FUN_00848ea0 | OTHER (atrybutowo-pędzone) | FUN_00745bf0→FUN_00843d60→FUN_00844660(uVar3)→lookup — czytnik atrybutów 0x0084xxxx decyduje o id; brak placementu. | WYSOKA |
| 15 | 0x004E6979 | FUN_004e68a0 | OTHER (atrybutowo-pędzone) | FUN_008493f0(...,&DAT_00ba27e0)→FUN_00745840→FUN_00844660→lookup→walidacja→FUN_007ad080. | WYSOKA |
| 16 | 0x0043EAF3 | FUN_0043eae0 | AVATAR_EQUIPMENT (fabryka) | lookup(param_2)→walidacja→FUN_0040b070→FUN_0043e5b0(&local_10, ..., FUN_008bd720) — builder pary {0x66,A} (poprzedni run: pair-insert FUN_0043c700); sloty avatara. | WYSOKA |
| 17 | 0x0067B915 | FUN_0067b800 | PREVIEW_UI | UI-helpers FUN_005094c0/0085c0f0/00509510/00509190 przed lookup; po walidacji operator_new(0x130) — obiekt UI z template'em. | WYSOKA |
| 18 | 0x006A3994 | FUN_006a3930 | OTHER (ctor) | Ctor (pola [this+..]); lookup(param_2)→walidacja→[this+0x18]=tpl lub 0. Generyczny. | ŚREDNIA |
| 19 | 0x0067C8D5 | FUN_0067c7c0 | PREVIEW_UI | Bliźniak FUN_0067b800 (identyczny kształt kodu, ta sama sekwencja UI-helperów). | WYSOKA |
| 20 | 0x005B5FEF | FUN_005b5f90 | OTHER (rejestracja derived z transformem) | lookup→FUN_005670a0→FUN_00730f60; f90/fb0 @0x005B601A/@0x005B6032 — jak #10: rekord placementu z pozycją+rotacją z atrybutów. | WYSOKA (mechanizm), NISKA (rola) |
| 21 | 0x006C236B | FUN_006c2350 | OTHER/UI | `uVar2 = *("ClickTargetNode" + (param_1+iVar1*4)*4+4)` — tabela klikalnych węzłów UI. | WYSOKA |
| 22-23 | 0x006C2BC2/0x006C2C15 | FUN_006c2bb0 | OTHER (łańcuch getterów) | tpl z [param+0x14] lub fallback do FUN_006c2700 (rodzina tabelaryczna). | WYSOKA |
| 24-25 | 0x006B2903/0x006B2931 | FUN_006b28e0 | AVATAR_EQUIPMENT | Hardcode 0x2D88=11656 (param==4 && stan==2); rodzina 11655/11656/(11657 wyliczany) — sloty ciała avatara (poprzedni run F1). | WYSOKA |

## B. 13 call-site'ów pumpu FUN_006c9700 (żądanie {0x66=MODEL, id})

| # | call-site VA | caller | klasyfikacja | dowód | pewność |
|---|---|---|---|---|---|
| 1 | 0x004C859A | FUN_004c83c0 | MODEL_MACHINERY | pump(id, "","",0) — generyczny wrapper pobrania modelu (użyty też w łańcuchu 004C5BD0→005F6990). | ŚREDNIA |
| 2 | 0x005F5B01 | FUN_005f5a80 | MODEL_MACHINERY (avatar-chain) | pump(param_1, ..., uVar2) — pobranie modelu w łańcuchu avatar (005F6850/005F6990 wywołują). | ŚREDNIA |
| 3 | 0x006C6FFC | FUN_006c6f60 | MODEL_MACHINERY | getter A → pump → [this+0x6C]=model — zapis referencji modelu w obiekcie. | ŚREDNIA |
| 4 | 0x006CB7CF | FUN_006cb6f0 | **MODEL_MACHINERY — TWÓRCA INSTANCJI** | Cache-lookup(A) w mapie [store+0x3C] (FUN_00971780) → check FUN_006cb370 → pump {0x66,A} → new(12)+ctor ArkModelResourceInstanceRef FUN_006fa8b0 → FUN_006cb020 (nazwana instancja 0x110B "<id>__<name>", check "ArkAnimation") → FUN_006f33a0 (rejestracja). | WYSOKA |
| 5 | 0x0093BEBC | FUN_0093be20 | OTHER/UNKNOWN (hardcode) | pump(0x70D17=460563,...) — hardcoded id; NEGATYW: "460563.nif" NIE istnieje w Models.bnt (0 hitów; Portals/TEZ/Volumes/VegetationClimates też 0) → żądanie bez zasobu lokalnego (inny typ/fail-download). | ŚREDNIA |
| 6 | 0x0094DB31 | FUN_0094da20 | MODEL_MACHINERY | pump(iVar3) → [obj+0x44] — zapis modelu. | ŚREDNIA |
| 7-8 | 0x006B4D3A/0x006B4DCB | FUN_006b4c50 | **AVATAR_EQUIPMENT (body-set)** | FUN_006c2840()/FUN_006c2870() (sloty tabelaryczne) → A×2 (FUN_007ce1e0) → pump×2 → attach do węzła [param_1+0x18] (detach starego vtable+0xA8). Jedyny caller: FUN_006b9970 = update postaci (string "CharacterPosition" @0x006B9B — odczyt węzła pozycji). | WYSOKA |
| 9 | 0x004413D7 | FUN_00441200 | MODEL_MACHINERY | pump(arg-stack) z 0x4413dc — generyczne pobranie. | ŚREDNIA |
| 10-11 | 0x006BCA46/0x006BCAFA | FUN_006bc8e0 | AVATAR_EQUIPMENT | Region 006b (avatar): chained FUN_006c2840 + getter A → pump ×2 — sloty wyposażenia. | ŚREDNIA |
| 12 | 0x006B749D | FUN_006b73d0 | MODEL_MACHINERY | pump(param_1,"","",0) — generyczny getter modelu. | ŚREDNIA |
| 13 | 0x0094B25F | FUN_0094b1d0 | **VEGETATION** | Stringi verbatim: "ArkVegetationModelClient::~ArkVegetationModelClient" i "ArkVegetationClient::GetModel" — pump {MODEL, id} dla modeli wegetacji (proceduralnych). | WYSOKA |

## C. WNIOSKI (GA-CLASSIFY)

1. **0/38 call-site'ów jest typu STATIC_WORLD** — wynik negatywny NO_STATIC_CONSUMER_FOUND dla
   powierzchni lookupu-template'ów + pumpu-modeli: żaden konsument nie jest napędzany
   placementem (brak generyczności-placement: wszystkie mają avatar-sloty, tabele UI,
   atrybuty, vegetation albo są maszyną sama w sobie).
2. **Kwalifikacja FUN_006b4c50 (Z2a) ROZSTRZYGNIĘTA**: to konsument **AVATAR_EQUIPMENT**
   (body-set/clothes): dual slot-table-getter → A → pump ×2 → attach do węzła postaci;
   jedyny caller FUN_006b9970 = update postaci z odczytem węzła "CharacterPosition";
   a upstream FUN_00489810 = setup lokalnego avatara (płeć: FUN_006c1f60(2-(stan!=1))).
   Stałe 11769/11655/11656/11657 = sloty ciała/wyposażenia avatara (NIE budynki).
3. Kontrola negatywna klasyfikacji: brak jakiejkolwiek stałej 296445/4508/4752/2249
   w .text (skan S3: 296445=0 hitów; 4508=3 hity=disp32, patrz Z3) — ścieżki są generyczne
   wobec ID zasobów; jedyny hardcode-model to 0x70D17 (FUN_0093be20) bez zasobu lokalnego.
4. Redirect: jeżeli statyki ładują modele, to NIE przez te 38 call-site'ów — kandydatem
   jest system ArkObject (ctor pobiera A z obiektu template → +0x28) + podsystem wizualny
   0x006Cxxxx (FUN_006cd850/cd820/cdd80) + system atrybutów (Z4).
