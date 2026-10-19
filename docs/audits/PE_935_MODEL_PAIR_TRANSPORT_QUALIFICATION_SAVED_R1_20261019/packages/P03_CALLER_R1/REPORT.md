# P03 — owning caller 006C3F50 (DIRECT_ANALYST_FALLBACK)

Wejście: extracts\WINDOW_006C3F50.txt (54 rows, [006C3F50,006C3FE0), pin 48EAA2FE58FE87B6EE2138D34B8D66E0990488981F00FCD4421624D94143740D). Attribution: parent direct per CONTRACT.md §10 (2 niekompletne próby dziecka w P01; tryb fallback dla kontraktu).

## Rekonstrukcja (CONFIRMED w oknie)

Prolog 006C3F50 SUB ESP,8; arg1=[entry+4] → 0043A550; wynik → ECX → 0072F580 → **EDI = obiekt rozwiązany z arg1** (opaque: 0043A550, 0072F580 nieotwarte).
- 006C3F69 MOV EBX,0x66; 006C3F74 CALL 007CE1E0(ECX=EDI) → **A = wynik** (opaque).
- ESI = arg2 = kontener (tail@+4/limit@+8 sprawdzone 006C3F7D-80).
- **Inline append pary {0x66, A}** do kontenera: 006C3F8D MOV [ECX],EBX; 006C3F8F MOV [ECX+4],EAX; grow przez 006C2E00 (006C3FA9) — ten sam helper co w 006C3640.
- 006C3FAE: MOV ECX,EDI; MOV EBX,0x8BD720; CALL 0040B070 → EAX = EDI+0x14 (model member-view P02).
- 006C3FBE/006C3FC1: EDX=[EAX+4]=[EDI+0x18], EAX=[EAX]=[EDI+0x14] → **para DWORD z [EDI+0x14]/[EDI+0x18] = (begin,end) zakresu**.
- CALL 006C3640 z 6 argumentami (cdecl, ADD ESP,0x18): arg1=&out-slot([ESP+0x30]), arg2=begin, arg3=end, arg4=ESI(kontener), arg5=EBX=**008BD720**, arg6=A(wynik 007CE1E0).

## Kluczowe ustalenia

1. **{66h,A} to wpis inline w TYM SAMYM kontenerze**, do którego 006C3640 dopisuje pary elementów — oba źródła par są rodzeństwem w jednej kolekcji, NIE jest to ten sam wpis (bridge equality nadal NOT_ESTABLISHED).
2. **Callback 008BD720 jest tutaj przypięty instrukcyjnie**: MOV EBX,0x008BD720 @006C3FB0 (bezpośredni immediate) — koniec spekulacji o tożsamości callbacku w tym callsite (CONFIRMED dla tego callsite).
3. Zakres elementów pochodzi z pól obiektu EDI: [EDI+0x14]=begin,[EDI+0x18]=end — para DWORD z member-view gettera 0040B070(EDI) to **wskaźniki zakresu**, nie wartość-para zasobu! W P01 kopiowane „pary" z callbacku to co innego (elem+0x18/+1C); tutaj z gettera brane są begin/end.
4. arg6=A przekazywany do 006C3640 jest **nieczytany w widocznym ciele 006C3640** (okno P01 kompletnie obejmuje funkcję) — martwy argument w tym protokole wywołania albo konwencja z szerszym ABI (premise).
5. Out-slot [ESP+0x30] lokalny; po powrocie caller nie czyta go w oknie (RET 006C3FDB zaraz po ADD ESP,0x18) — konsument wyniku jest wyżej: kontener przyszedł jako arg2 od callerów 006C3FE0/006C4020.

Actuals: 1 function-owner 006C3F50 (B5 split 006C3F98 = blok slow-path), 54 rows, 6 CALL sites (006C3F5B/62/74/ A9/B5/CD), 6 różnych targetów; 3 variants kons.

Premises: P3-P1: 0072F580 zwraca wskaźnik obiektu (wzorzec ECX=EAX po 0043A550); P3-P2: A=007CE1E0(EDI) to wartość-para (nie wskaźnik) — z zapisu bezpośredniego [ECX+4],EAX.