# P02 — member-view 0040B070 i kwalifikacja provenance (DIRECT_ANALYST_FALLBACK)

Attribution: analiza bezpośrednio przez PE-MASTER (rodzic) w trybie DIRECT_ANALYST_FALLBACK na tym kontrakcie (§10; dwie niekompletne próby dziecka w P01). Provenance-context pliku przeczytany tekstowo; nauka ograniczona do sekcji FUN_0040b070 (linie 66–81) zgodnie z requestem; gate 00407270 NIE jest analizowany jako kierunek.

## 1. Treść dopuszczonego body (linia 66–77, CONFIRMED-jako-dekompilat)

```
int __fastcall FUN_0040b070(int param_1)
{
  return param_1 + 0x14;
}
```

Plik: GHIDRA_GATE_00407270.txt, 1269 B, SHA256 C34D2BD8995A41D34AD852316B41F603AFCFCDD4EE308727B2AB3E6B260502A5. Ekstrakt: 15 linii, pin 6AC83E27A46A027970E99CD015CAEB945493B0A39CF6F654FCEB0A0611122D84.

## 2. Kwalifikacja provenance (obowiązkowa rozdzielność)

- **Co wiąże eksport z 9.3.5:** wyłącznie deklaracja historycznego skryptu/aggregate — plik leży w tym samym folderze PE_NIGHT_AGGREGATE_20260905_160000 co listing H5 (SHA 642CC29A…); konwencja nazewnicza „@0x40b070” sugeruje ten sam program; namespace stlp_std (STLport) jest spójny z klientem PE 2003.
- **Co jest tylko deklaracją starego skryptu:** program identity (że dekompilat pochodzi z dokładnie tego samego binarium co H5). Bez oryginału (niedostępny/nieotwarty) NIE można tego zweryfikować.
- **Czego nie można zweryfikować:** zgodności bajtów instrukcji pod 0040B070 z żadnym fizycznym buildem; że dekompilat __fastcall odzwierciedla rzeczywiste ABI (etykieta __fastcall jest decompiler-assigned).
- **Poziom dowodu:** dekompilat = BYTE_OBSERVATION/STRUCTURE w medium tekstowym; promocja do instrukcyjnych faktów H5 wymagałaby fizycznego binarium. **MEMBER_VIEW_PROVENANCE = SAME-HISTORICAL-AGGREGATE-DECLARED, PROGRAM-IDENTITY-UNVERIFIED.**

## 3. Model member-view (STRONGLY_SUPPORTED, decompiler-level)

- FUN_0040b070 zwraca `param_1+0x14` — klasyczny member-view: zwraca adres składowej pod offsetem 0x14 obiektu właściciela.
- Kontekst wywołania w tym pliku (tylko jako provenance kontekstu, nie nowa nauka o gate): wynik jest rzutowany na `basic_string*` i dalej `c_str` — dowodzi, że typ składowej @+0x14 zależy od klasy właściciela; getter sam w sobie jest beztypowy.
- **Implikacja dla par:** kampanijne "dwa DWORD z wyniku 0040B070" są spójne z member-view (wynik = wskaźnik na składową 8-bajtową), ALE typ/domena składowej nie wynika z gettera — zależy od klasy konkretnego ownera w danym callsite.

## 4. Registration semantics (utrzymane wyzwanie postaudytu)

- Ciało gettera nie zawiera żadnego zapisu wskaźnika funkcji, żadnego wywołania dispatch. Etykieta __fastcall nie zmienia faktu, że jedyną operacją jest `lea/add +0x14`.
- Zatem: **callback registration przez 0040B070 = REJECTED (decompiler-level counterevidence utrzymane, spójnie z postaudytem S2).** Callback przekazywany dalej jako argument (kampanijny plumbing: EBX/EDI → 0043E5B0/006C3640) to zwykły argument synchroniczny.

## 5. Most tożsamości par (pozostaje otwarty)

- PAIR_FRAME={66h,A} przekazywana do opaque 0043C700 (z ramki wywołania w H5) i PAIR_PROJECTED=2×DWORD z [element+18h/+1Ch] (z callbacku 008BD720 → kopiowane w 006C3640) to **nadal dwa niezamknięte źródła**. Dekompilat gettera nie zamyka equality: żadna value-flow krawędź między {66h,A} a element+18h nie istnieje w dopuszczonych danych.
- Rzeczywisty 006C3640 (P01) kopiuje dokładnie 2 DWORD z wyniku callbacku — więc **jeśli** callbackiem jest 008BD720, pary pochodzą z [element+18h/+1Ch]. Ale tożsamość callbacku w konkretnym callsite oraz to, czy {66h,A} trafia do elementu przed iteracją (np. przez 0043C700), pozostaje do ustalenia u owning callera.

## 6. Liczniki actuals

- document_body: 15 linii (66–81 exclusive) = 15/1000 body-document budget.
- Instrukcje: 0 (dekompilat); CALL: 0; ciała: 1 (FUN_0040b070), kandydaci: 2 (zgodnie z planem; gate 00407270 NIE otwarty jako ciało — tylko kontekst tekstowy provenance).
- Warianty: 2/24 (kons.).

## 7. Statusy wyjściowe

- MEMBER_VIEW_MODEL = STRONGLY_SUPPORTED (decompiler-level; program-identity unverified).
- MEMBER_VIEW_PROVENANCE = SAME-AGGREGATE-DECLARED, PROGRAM-IDENTITY-UNVERIFIED.
- REGISTRATION_SEMANTICS = REJECTED (na poziomie dekompilatu i spójnie z plumbingiem H5).
- PAIR_FRAME_TO_PROJECTED = NOT_ESTABLISHED (bez zmian).