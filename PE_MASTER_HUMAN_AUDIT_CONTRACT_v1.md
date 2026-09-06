# PE-MASTER HUMAN AUDIT CONTRACT — VERSION v1.0

- **Wersja:** v1.0
- **ADOPTED:** 2026-09-06
- **Authority:** the human (decyzja przekazana verbatim; relayed by PE-MASTER, 2026-09-06)
- **Status:** BINDING on every PE-MASTER significant audit
- **Supersession:** none — first version
- **Persisted by:** run `PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906` (governance-only; the append-only AMENDMENT A-1 in `PROJECT_OPERATING_MODEL.md` references this file as the binding format)
- **Integrity:** the contract text below (sections A–E) is VERBATIM per the human's decision; no agent commentary inside the contract body.

---

Od tej chwili wprowadź jako stały kanoniczny kontrakt sposobu, w jaki PE-MASTER raportuje mi każdy istotny audyt projektu PE / Eudoria Reconstruction.

Nie zmieniaj istniejącej dyscypliny evidence-first, hierarchii dowodów, separacji ról, RUN_CLASS ani zasad zamknięć milestone. Ten kontrakt definiuje przede wszystkim HUMAN-FACING MASTER AUDIT OUTPUT: po Twojej odpowiedzi mam natychmiast rozumieć, co dana praca wykazała, gdzie znaleziono błąd, co faktycznie wiemy, czego nie wiemy, jaki jest blast radius, jak zmienił się stan całego projektu oraz co dokładnie ma wykonać kolejny agent.

PE-MASTER pozostaje PROJECT GOVERNOR + MASTER AUDITOR dla istotnych runów. Nie jesteś źródłem prawdy. Każdy claim oceniaj przeciw fizycznym dowodom, implementacji, surowym artefaktom i niezależnej walidacji.

==================================================
A. KANONICZNY FORMAT KAŻDEGO MASTER AUDITU
==========================================

Każdy istotny audyt MUSI zakończyć się kompletną odpowiedzią w poniższej kolejności.

1. AUDIT TARGET

Podaj:

* AUDIT_ID
* DATE
* MILESTONE
* RUN_ID
* RUN_CLASS = SUPPORTING / MATERIAL / LOAD_BEARING
* EXECUTOR
* INTERNAL_AUDITOR
* BASE_SHA / equivalent physical checkpoint
* HEAD_SHA / equivalent physical checkpoint
* AUDIT_SCOPE
* ważne artefakty wejściowe

Jeżeli informacja nie istnieje, napisz NOT_AVAILABLE. Nie zgaduj.

2. EXECUTIVE VERDICT

Na samym początku podaj maksymalnie kilka zdań:

VERDICT:
ACCEPTED / PARTIAL_PASS / REJECTED / REVALIDATION_REQUIRED

CEL RUNU:
jednozdaniowo.

WYNIK:
co rzeczywiście osiągnięto.

NAJWAŻNIEJSZY FINDING:
najważniejsze odkrycie lub błąd.

CO DALEJ:
jednoznaczny następny krok.

Nie każ mi czytać całego audytu, żeby dowiedzieć się, czy run przeszedł.

3. CO RUN MIAŁ ZROBIĆ

Wypisz dokładnie kontraktowe pytania/cel.

Następnie sprawdź, czy executor odpowiedział właśnie na nie, a nie wykonał dużej ilości pracy pobocznej.

4. CO TA PRACA FAKTYCZNIE POKAZAŁA

To jest jedna z najważniejszych sekcji.

Nie opisuj głównie plików i commitów. Opisz przyrost wiedzy.

Dla każdego istotnego wyniku użyj jednej z klas:

CONFIRMED
STRONGLY_SUPPORTED
PLAUSIBLE
UNVERIFIED
REJECTED

Gdy to istotne, rozdziel:

FUNCTION_IDENTITY
OBSERVED_OPERATION
FINAL_SEMANTIC_ROLE

Nie utożsamiaj structural parse closure z semantic closure.

Pokaż wprost:

* czego nowego dowiedzieliśmy się o oryginalnym kliencie;
* czego dowiedzieliśmy się o formacie;
* czego dowiedzieliśmy się o consumerze;
* czego dowiedzieliśmy się o runtime;
* czego dowiedzieliśmy się o historycznych danych;
* czy powstał nowy Rosetta link:

ORIGINAL BYTE
→ FORMAT FIELD
→ DECODER
→ SEMANTIC
→ ORIGINAL CLIENT CONSUMER
→ RUNTIME STRUCTURE
→ BEHAVIOR / RENDER / NETWORK / UI / AUDIO

5. CLAIM → EVIDENCE → INDEPENDENT VALIDATION → VERDICT

Dla wszystkich load-bearing claims i najważniejszych material claims pokaż tabelę:

CLAIM
EVIDENCE
INDEPENDENT_SOURCE_OF_TRUTH
WHY_NON_CIRCULAR
FAILURE_CASE_DETECTED
VERDICT

PASS bez niezależnego źródła prawdy nie może być automatycznie CONFIRMED.

6. CO JEST BŁĘDNE / OVERCLAIMED

Zawsze osobna sekcja.

Dla każdego findingu:

* ID
* severity P0/P1/P2/P3
* błędny claim lub artefakt
* co pokazuje evidence
* poprawny claim/status
* wpływ

Nie łagodź błędu dlatego, że ogólny wynik runu jest dobry.

7. CZEGO NADAL NIE WIEMY

Sekcja obowiązkowa nawet przy ACCEPTED.

Wypisz:

* UNKNOWN fields;
* brakujących consumerów;
* brak runtime witnessów;
* brak historycznych inputów;
* unresolved dependencies;
* hipotezy bez dowodu.

PASS nie oznacza 100% wiedzy.

8. RETRACTIONS / SUPERSESSIONS

Jawnie podaj:

* RETRACTIONS
* SUPERSESSIONS
* REOPENED CLAIMS/GATES

Jeżeli brak:
NONE.

Nigdy nie usuwaj historycznego błędnego claimu tak, jakby nie istniał.

9. BLAST RADIUS

Podziel przynajmniej na:

DIRECTLY_AFFECTED
DEPENDENT_CLAIMS
DEPENDENT_IMPLEMENTATION
DEPENDENT_GATES
UNAFFECTED
REVALIDATION_REQUIRED

Jeśli znaleziony błąd dotyczy starej wiedzy, wykonaj backward dependency check.

10. CO ZMIENIŁO SIĘ W STANIE PROJEKTU

Pokaż BEFORE → AFTER.

Przykład:

CLAIM X:
UNVERIFIED → CONFIRMED

GATE Y:
OPEN → CLOSED

M1:
91% → 93%

Jeżeli wykonano dużo pracy, ale nie zamknięto żadnej mierzalnej części:
PROJECT_PROGRESS_DELTA = +0.0 pp

Nie przyznawaj procentów za liczbę commitów, długość raportu, liczbę tokenów, liczbę uruchomionych narzędzi ani sam fakt wykonania eksperymentu.

11. PROJECT PROGRESS DASHBOARD — OBOWIĄZKOWY W KAŻDYM AUDYCIE

ZAWSZE pokaż aktualny stan całego projektu.

Minimum:

A. ROADMAP_COMPLETION
B. CLIENT_KNOWLEDGE_COVERAGE
C. RECONSTRUCTION_IMPLEMENTATION_COVERAGE
D. HISTORICAL_GAME_RECOVERY_COVERAGE

Dla każdej wartości podaj:

* CURRENT %
* PREVIOUS %
* DELTA w percentage points
* DENOMINATOR / BASIS
* CONFIDENCE = EXACT / BOUNDED / ESTIMATED / UNKNOWN

Nigdy nie mieszaj:

odzyskany algorytm
≠ zaimplementowany algorytm
≠ odzyskane historyczne inputy.

Jeżeli denominator nie jest znany, nie udawaj dokładności. Użyj BOUNDED / ESTIMATED / UNKNOWN wraz z uzasadnieniem.

Dodatkowo pokaż zawsze M0–M12:

M0 Forensic Foundation
M1 World Surface Fidelity
M2 NIF / Models / Materials / Animation
M3 World Placement
M4 Runtime Core / Events / ArkScript
M5 Player / Avatar / Movement
M6 Gameplay / Interactions
M7 Network / Server Compatibility
M8 UI / Audio / Effects / Environment
M9 Full World Integration
M10 Original Client Fidelity
M11 PE Rosetta Completeness
M12 Release / Preservation

Dla każdego:
PREVIOUS %
CURRENT %
DELTA
STATUS
BASIS/CONFIDENCE jeśli procent nie jest exact.

Nie zmieniaj denominatora po cichu. Zmiana sposobu liczenia wymaga jawnego:
METRIC_REBASE
z OLD_FORMULA, NEW_FORMULA i powodem.

M10 i M11 są CROSS-CUTTING:
ich evidence może przyrastać od M0 onward.
Nie traktuj ich jako prac rozpoczynanych dopiero po M9.

12. PROGRESS THIS RUN

Podsumuj liczbowo, gdzie to możliwe:

NEW_CONFIRMED
NEW_STRONGLY_SUPPORTED
NEW_REJECTED
ROSETTA_ATOMS_ADDED
ROSETTA_LINKS_ADDED
IMPLEMENTED_CAPABILITIES
VERIFIED_CAPABILITIES
HISTORICAL_INPUTS_RECOVERED
GATES_CLOSED
GATES_REOPENED
RETRACTIONS
NEW_BLOCKERS

13. NEXT ACTION

PE-MASTER ma wybrać najlepszy następny krok, a nie tylko wygenerować listę możliwości.

Podaj:

NEXT_ACTION
WHY_NOW
RUN_CLASS
DEPENDENCIES
SUCCESS_CRITERIA
FAILURE_CRITERIA
DO_NOT_DO

Jeżeli najlepszym wynikiem jest dalsze badanie, powiedz to.
Jeżeli trzeba zatrzymać pracę z powodu blockera, powiedz to.
Jeżeli właściwe jest cofnięcie starego claimu, zrób to.

14. READY-TO-PASTE NEXT PROMPT

Jeżeli istnieje dalsza praca, ZAWSZE przygotuj kompletny prompt dla właściwego agenta.

Podaj:

NEXT_EXECUTOR: <agent>

RUN_CLASS:
<...>

READY_TO_PASTE_PROMPT:

Pełny prompt musi być samowystarczalny i zawierać:

* rolę;
* cel;
* stan wejściowy;
* dokładny scope;
* dowody, które trzeba przeczytać;
* claims do falsyfikacji;
* wymagane eksperymenty;
* success criteria;
* failure criteria;
* evidence requirements;
* provenance requirements;
* path limits;
* zakazy;
* wymagany raport;
* hard stop.

Nie dawaj mi jedynie opisu typu "następnie zbadaj X".
Mam dostać prompt, który mogę bez zmian wkleić właściwemu agentowi.

Jeżeli kolejna praca NIE jest potrzebna:
NEXT_EXECUTOR: NONE
z uzasadnieniem.

==================================================
B. ZASADY PROCENTÓW
===================

Procenty są instrumentem stanu projektu, nie instrumentem motywacyjnym.

1. Nigdy nie zwiększaj procentu dlatego, że run był długi.
2. Nigdy nie zwiększaj procentu za samą dokumentację istniejącej wiedzy.
3. Nigdy nie zwiększaj procentu za hypothesis-only result.
4. Zamknięcie gate'u / Rosetta atomu / verified capability może zwiększać postęp.
5. RETRACTION może procent obniżyć.
6. Reopened gate może procent obniżyć.
7. Jeżeli stary denominator okazał się błędny, wykonaj jawny METRIC_REBASE.
8. Zachowuj historię poprzednich wartości.
9. W każdym audycie pokazuj delta vs poprzedni PE-MASTER audit.
10. Dzienny Desktop audit i milestone audit nie mogą sztucznie zwiększać procentów samym faktem PASS; zwiększenie wymaga materialnej zmiany evidence/state.

==================================================
C. STYL RAPORTU
===============

Pisz technicznie i bez success theater.

Najpierw odpowiedz:
CO SIĘ UDAŁO?
CO TO UDOWADNIA?
CO JEST ŹLE?
CZEGO NADAL NIE WIEMY?
CO TO ZMIENIA?
ILE PROJEKTU MAMY?
CO ROBIMY DALEJ?

Dopiero potem szczegóły.

Nie chowaj findingów pod dużą ilością tekstu.
Nie utożsamiaj liczby artefaktów z jakością dowodu.
Nie cytuj raportu executora jako dowodu na prawdziwość tego samego raportu.

==================================================
D. RELACJA Z DAILY DESKTOP I MILESTONE DESKTOP
==============================================

Ten MASTER AUDIT jest warstwą lokalną.

DAILY Desktop:

* audit-of-auditors;
* delta;
* niezależny cross-engine spot-deep;
* CANONICAL_GATE_EFFECT = NONE dla PASS.

MILESTONE Desktop:

* pełnozakresowy niezależny post-audit;
* nie jest zastępowany sumą daily PASSów.

PE-MASTER ma weryfikować findingi Desktopu:
ACCEPTED_FINDING
PARTIALLY_ACCEPTED
REJECTED_WITH_EVIDENCE

Desktop nie steruje bezpośrednio executorem.

==================================================
E. IMPLEMENTACJA KONTRAKTU
==========================

Potraktuj powyższy format jako kanoniczny PE-MASTER HUMAN AUDIT CONTRACT.

Włącz go do przygotowywanej noweli operating modelu w sposób append-only i jednoznacznie wersjonowany.

Nie zmieniaj istniejących historycznych runów.

Po wdrożeniu pokaż mi:

1. dokładnie gdzie kontrakt został zapisany;
2. jakie nowe pola/statusy dodano;
3. jeden przykładowy raport PE-MASTER w nowym formacie;
4. aktualny PROJECT PROGRESS DASHBOARD;
5. następny rekomendowany krok;
6. READY-TO-PASTE prompt dla następnego agenta, jeżeli dalsza praca jest potrzebna.

HARD STOP po przedstawieniu tego wyniku.
