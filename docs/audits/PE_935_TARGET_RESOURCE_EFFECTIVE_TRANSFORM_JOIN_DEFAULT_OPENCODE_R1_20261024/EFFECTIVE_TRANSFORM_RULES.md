# EFFECTIVE_TRANSFORM_RULES — reguły efektywnego transformu pierwszej trójki (run R1_20261024)

## Definicje (era: PE 9.3.5 saved-static; wszystkie adresy VA .text)
- record = 44-bajtowy factory-record (miss-path) lub parser-record objA (F+0x10, caller 004C47F0)
- def+off = pole factory-recordu (kopie w creatorze: G+off = record[off])
- v1 = trójka record+0x08/+0x0C/+0x10 (pierwszy wektor)
- v2 = trójka record+0x14.. (drugi wektor; tory hit/miss patrz B03)
- H = float z 00853A80(mgr, v1.x, v1.y, 0, 0)
- B = ClientMovableObject (new 0x128), T = M32[B+0xC0] = SceneFeederObject

## Reguła symboliczna pierwszej trójki (uwzględniając clamp H)

```
Dla selektora word[record+0x34] ∈ {3,4,5,6,7}:
    H = provider_query(mgr_singleton, (v1.x, v1.y))     # 00853A80; 0.0 przy fail walidacji
    if (H > v1.z) ordered:                               # FCOM; TEST AH,0x41; JNZ skip
        v1.z = H                                        # FSTP [ESP+0x18] @0x004C478A
# dla pozostałych selektorów oraz unordered/EQ: v1.z bez zmian
# NASTĘPNIE (ctor 00528E50):
#   base ctor 0085B1B0: B+0x44..0x4C = v1 (pierwsza trójka, z ewentualnym clampem)
#   derived: jeśli 0048CBB0(holder, 1) != 0:
#       T = new SceneFeederObject (005247C0)
#       005094C0(T, &B+0x44): T+0x34/38/3C = *(B+0x44..0x4C)   # aplikowana pierwsza trójka
#   w przeciwnym razie: T = NULL (B+0xC0 zero-init)
```

Wniosek: **aplikowana pierwsza trójka ≠ surowy rekord w ogólnym przypadku** — trzecia składowa może być podniesiona do wartości H (ordered max). Składniki 1 i 2 przechodzą bez zmian w pokazanych instrukcjach.

## Reguła drugiej trójki i bloku orientacji

```
00509510(T, &B+0x5C):
    T+0x74/78/7C = [B+0x5C..0x64]            # kopia verbatim drugiej trójki
    local = 0096CDD0(&[B+0x5C..0x64])         # builder orientacji (sin/cos; K/eps nieznane)
    S = 00437F70()                            # origin singleton (initial {0,0,0}; mutowalny - prior canon)
    block36 = 0048BAC0(S, local)              # konwersja z origin (rodzina 0x82B5A0)
    T+0x4C..0x70 = block36                    # 9 dwordów
    T+0x28 = 1                                # dirty
```

## Semantyka pól T (odczyt)
- T+0x34: stored placement (slot3 fallback zwraca surową zapisaną trójkę; slot3 primary = konwersja world-translate linka: f32(f32(W*0.01)−S), prior canon).
- T+0x74: zapasowa kopia drugiej trójki (slot2 address-of).
- T+0x80: trójka z B+0x50 (slot4 address-of).
- T+0x40: trójka z holder+0xC0 (gated [T+0x2C]>>4&1).
- T+0x30: link (new 0x118 przez 007B6000) — primary źródło pozycji live (klasa UNKNOWN).

## Granice reguł
- Wartości H w historii: NIEODZYSKANE (H z providera; provider nie uruchomiony — brak runtime).
- Krawędź model↔instancja: PARTIAL (patrz RESOURCE_INSTANCE_JOIN.csv).
- Syntetyczny przykład: selector 3, v1=(x1,y1,2), H=5 ⇒ aplikowana trójka (x1,y1,5) — ilustracja, NIE odzyskany placement.
