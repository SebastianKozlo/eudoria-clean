# FULL_EXTERNAL_MILESTONE_POST_AUDIT — PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816
# (the M1 milestone-gate package = docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/)
#
# Persisted VERBATIM per the three-tier operating model (§22.5) by pe-master-auditor.
# The verdict was relayed by the human 2026-09-05/06 after the external (ChatGPT-class)
# deep audit of the completed M1 gate package. It SUPERSEDES the advisory PE-MASTER
# pre-check (MASTER_ACCEPTED) for gate purposes: the gate is NOT accepted.
# NOTE FOR AUDITORS: the pre-check's claim that "the divisor-candidate line disappeared
# from the live matrix" was verified against the V3 MARKDOWN, while the external audit
# shows the V3 JSON still carries it — this verification miss is processed by the
# PE-MASTER finding-verification step that follows.

## Werdykt końcowy
**AUDIT_VERDICT = RETURN_FOR_CORRECTION**

- **M1 pozostaje `PARTIAL` — bramka nieprzyjęta.**
- **M2 pozostaje zablokowany.**
- Rdzeń dowodów jest w większości solidny, ale pakiet nie jest „complete and internally consistent".
- Nie zmieniłem żadnych plików. Repo jest czyste, a `HEAD == origin/master == ea35bd8`.

### Co potwierdziłem niezależnie

- Wszystkie **38 unikalnych plików dowodowych** cytowanych przez 19 roszczeń istnieją; rozmiary i SHA są zgodne.
- Wszystkie **8 oryginalnych dużych źródeł** — m.in. `50.bnt`, `Entropia.exe`, oba `Models.bnt`, kontenery tekstur — ma zgodny SHA.
- Indeks naprawy: **57/57 artefaktów zgodnych**.
- Bezpośrednio z `Entropia.exe` potwierdziłem:
  - `32767.0` — RNG divisor,
  - `65535.0` — pozycja,
  - `0.00007812499825377017` — mnożnik skali,
  - oraz instrukcje x87 wskazujące te operandy.
- Naprawiony oracle IEEE, PE section map i 13 negatywnych kontroli fail-closed są technicznie wiarygodne.
- Niezależnie odtworzyłem:
  - PC=24: **14 104/229 376** różnic na realnej domenie,
  - PC=24: **103 073/1 245 184** na domenie syntetycznej.

## Ustalenia blokujące

### P0 — V3 nie spełnia kontraktu §13

Kontrakt wymaga dla każdego z 19 wierszy: `KNOWLEDGE`, `IMPLEMENTATION`, `VALIDATION`, `HISTORICAL_FIDELITY`, `EVIDENCE_STATUS` — [NEXT_PROMPT.md](D:/Eudoria_Reconstruction/99_Audits/PE_MASTER_HANDOFFS/PE_MILESTONE_1_WORLD_SURFACE_R1_20260906_043000/NEXT_PROMPT.md:586).

Aktywna V3 usuwa trzy z nich:

- `implementation`,
- `historical_fidelity`,
- `evidence_status`.

Generator kopiuje tylko knowledge/validation/evidence/era/bounds — [repair_06_analysis.py](D:/Eudoria_Reconstruction/99_Audits/PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439/00_CONTROL/repair_06_analysis.py:149).

Stara macierz zawierała wymagane pola, ale została formalnie oznaczona jako superseded. Nie może uzupełniać braków żywej V3.

### P0 — aktywny JSON zawiera wycofane fakty

Generator nadpisuje werdykt, lecz bezwarunkowo przenosi stare `knowledge` i `honest_bounds` — [repair_06_analysis.py](D:/Eudoria_Reconstruction/99_Audits/PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439/00_CONTROL/repair_06_analysis.py:157).

Skutki:

- ROW10 nadal mówi `pos = u16/K` i `scale = |rand*2.0| MEASURED` — [M1_GATE_DELIVERABLE_MATRIX_V3.json](D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/GATES/M1_GATE_DELIVERABLE_MATRIX_V3.json:328).
- ROW11 nadal deklaruje `32768.0 divisor candidate` — [M1_GATE_DELIVERABLE_MATRIX_V3.json](D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/GATES/M1_GATE_DELIVERABLE_MATRIX_V3.json:376).
- ROW8 nadal przedstawia clean NIF path jako „queued", bez aktualnego ograniczenia do jednego świadka — [M1_GATE_DELIVERABLE_MATRIX_V3.json](D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/GATES/M1_GATE_DELIVERABLE_MATRIX_V3.json:288).

Te same stare dane zostały następnie skopiowane do `EVIDENCE_MANIFEST.json`. Validator sprawdza jedynie obecność pól, SHA i liczniki, nie ich spójność semantyczną — [consistency_check.py](D:/Eudoria_Reconstruction/99_Audits/PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816/00_CONTROL/consistency_check.py:315).

### P1 — M1 nie spełnia warunku merytorycznego

Kontrakt zabrania PASS, jeśli kluczowy subsystem nadal ma świadomie arbitralną implementację — [NEXT_PROMPT.md](D:/Eudoria_Reconstruction/99_Audits/PE_MASTER_HANDOFFS/PE_MILESTONE_1_WORLD_SURFACE_R1_20260906_043000/NEXT_PROMPT.md:593).

Nadal otwarte są:

- źródło zawartości komórek foliage — obecny content jest `RECONSTRUCTION-ONLY`,
- wybór klimatu dla lokalizacji,
- rzeczywisty x87 control word; PC=24 zmienia 6,15% realnej domeny lerp,
- witness matrix i scrambled-texture falsification,
- georef/P-DATUM oraz brakujące gridy patchera,
- porównanie z oryginalnym klientem.

Dlatego poprawny stan to nadal `M1_PARTIAL`, ewentualnie po wyczerpaniu źródeł `MILESTONE_BLOCKED_WITH_EXHAUSTIVE_NEGATIVE` — nie PASS.

### P2 — drobniejsze defekty

- `STAGE_ACCEPTANCE_GATES.csv` podaje `463141+20000`; faktyczny podział to **443 141 testów platformowych + 20 000 f80 exactness = 463 141 łącznie**.
- Commit `b34dd76` zmieszał 24 pliki tego pakietu z dwoma plikami równoległego NIF-R3. Zostało to uczciwie opisane i nie uszkodziło treści, ale osłabia atomową proweniencję commitu.

## Ocena 19 wierszy

- **ROWS 1–7, 9, 12–18:** akceptuję w granicach jawnie opisanych statusów i ograniczeń.
- **ROW8:** dowód jednego original-direct witness jest wiarygodny; nie potwierdza szerokiej ścieżki modeli.
- **ROW10:** poprawiony dowód mechanizmu i arytmetyki akceptuję; aktywny rekord V3 odrzucam jako sprzeczny.
- **ROW11:** RNG, stałe i rounding points potwierdzone; zgodność z oryginalnym klientem pozostaje warunkowa do pomiaru x87 CW.
- **ROW19:** potwierdzona jest wyłącznie deterministyczna regresja względem własnego runtime, nie oryginalnego klienta ani pełnej mapy.

## Prompt naprawczy dla OpenCode

```text
Uruchom jeden bounded corrective run z NOWYM RUN_ID. Nie modyfikuj zakończonych
runów, nie uruchamiaj M2 i nie zmieniaj wniosków byte-level bez nowego dowodu.

1. Wygeneruj M1_GATE_DELIVERABLE_MATRIX_V4.md/.json.
2. Każdy z 19 wierszy musi fizycznie zawierać:
   KNOWLEDGE, IMPLEMENTATION, VALIDATION, HISTORICAL_FIDELITY,
   EVIDENCE_STATUS, ERA, DENOMINATOR, LIMITATIONS i EVIDENCE.
3. Nie kopiuj carried_knowledge/honest_bounds z ITER048 dla wierszy
   poprawionych w iter035/036/037.
4. ROW10: wpisz wyłącznie aktualną arytmetykę 65535.0 i
   float32(1/12800)-widened; usuń u16/K oraz rand*2.0.
5. ROW11: usuń 32768 candidate; P-RNG-DIV=32767.0 i
   P-POS-SCALE=65535.0 są SUPERSEDED-LOCKED. Zachowaj otwarte
   P-RNG-P3, view-band provenance i actual x87 CW.
6. ROW8: rozdziel SINGLE ORIGINAL-DIRECT WITNESS od nadal otwartej
   pełnej ścieżki/witness matrix.
7. Wygeneruj EVIDENCE_MANIFEST_V4 z aktualnych pól V4, nie ze starej macierzy.
8. Dodaj semantic consistency gate z negatywnymi kontrolami, zakazujący
   wycofanych fraz w polach live oraz wymagający pięciu pól kontraktu §13.
9. Popraw licznik oracle na 443141 platform + 20000 f80 = 463141 total.
10. Zmaterializuj pomiar synthetic PC24 103073/1245184 jako surowy JSON.
11. V3 zachowaj jako FROZEN/SUPERSEDED; commituj wyłącznie własne ścieżki.
12. Końcowy status pozostaje M1_PARTIAL i M2_HARD_STOP.
```

Po zaakceptowaniu V4 następny merytoryczny priorytet to pomiar rzeczywistego x87 control word, a następnie źródło `P-CELLSTREAM/P-CLIMATE`.

(End of FULL_EXTERNAL_MILESTONE_POST_AUDIT — persisted verbatim by pe-master-auditor.)
