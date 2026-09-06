
---

## AMENDMENT A-1 — GOVERNANCE MODEL v2 + PE-MASTER HUMAN AUDIT CONTRACT (ADOPTED 2026-09-06)

**Status noweli:** BINDING standing record. Przyjęta decyzją człowieka (2026-09-06),
przekazaną verbatim przez PE-MASTER; zapisana runem governance-only
`PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906` (RUN_CLASS: MATERIAL, zadeklarowany przez
PE-MASTER w kontrakcie runu; BASE_SHA `8c95438245b3f75b8d90bd3f86a573dd8fab4c54`).
Nowela jest ADDYTYWNA: istniejący tekst tego pliku pozostaje nietknięty (dowód: kopia
`.pre` jest PEŁNYM byte-prefixem tego pliku po noweli — weryfikacja skryptem
bajt-po-bajcie, `docs/audits/PE_OPERATING_MODEL_AMENDMENT_A1_R2_20260906/00_CONTROL/`).
Tam, gdzie poniższe terminy pokrywają się z istniejącymi sekcjami, w warstwie
governance, którą ta nowela wprost nazywa (RUN_CLASS, głębokość audytu, tryb DAILY
Desktopu, DAILY DOSSIER, triggery, pętla poprawek, tabela ról, tryb MILESTONE,
wersjonowanie), wiążąca jest ta nowela.

**A1.1 — RUN_CLASS.** RUN_CLASS: SUPPORTING | MATERIAL | LOAD_BEARING. Klasę deklaruje
PE-MASTER w kroku FORMALIZE — obowiązkowe pole kontraktu runu, na równi z BASE_SHA.
Executor nie klasyfikuje własnej pracy. Reklasyfikacja wyłącznie W GÓRĘ i wyłącznie na
dowodzie (semantyka DEPENDENCY_GATE): jeśli wniosek runu staje się nośny, run awansuje
do LOAD_BEARING, a zaległy głęboki audyt domyka się ZANIM ktokolwiek na nim zbuduje.
Błędna klasyfikacja = finding (dyscyplinarny zapis, nie kara).

**A1.2 — Głębokość audytu wg klasy.**

- SUPPORTING → internal QC auditora + PE-MASTER reconcile (reconcile = mechanicznie:
  re-hash pinów wejściowych, census scope commitu, ENTRYPOINT_ROW_SURVIVAL, brak zapisów
  poza dozwolonymi ścieżkami, spójność raport-vs-artefakt na poziomie liczników).
- MATERIAL → internal QC + PE-MASTER targeted deep audit (dotknięte pliki +
  load-bearing claims runu).
- LOAD_BEARING → internal auditor w ŚWIEŻYM kontekście (formalizator runu nie może być
  jego internal auditorem) + PE-MASTER pełny 5-warstwowy deep audit + rekomputacja
  fizyczna surowych dowodów.

**A1.3 — Tryb DAILY Desktop (DAILY_AUDIT): namespace i asymetria.** Nowy namespace:
`DAILY_AUDIT_PASS | DAILY_AUDIT_PARTIAL | DAILY_AUDIT_REJECTED |
DAILY_AUDIT_REVALIDATION_REQUIRED`. ASYMETRIA: PASS → CANONICAL_GATE_EFFECT=NONE i
MILESTONE_CLOSURE_EFFECT=NONE (niczego nie zamyka, nie jest standing evidence dla
bramki zamknięcia); REJECTED/PARTIAL → MOŻE otworzyć blocker/retraction/revalidation,
ale wyłącznie przez weryfikację findingu przez PE-MASTER (ACCEPTED_FINDING /
PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE — Desktop też może się mylić) i dopiero
potem bounded correction run. Desktop nie steruje executorem bezpośrednio.

**A1.4 — DAILY DOSSIER.** Dossier buduje DETERMINISTYCZNY skrypt (własność:
pe-toolsmith; hash-pinned; narzędzie współdzielone, nie run-local) z mechanicznych
źródeł: ANCHOR_SHA, HEAD_SHA, git rev-list, git diff --name-status, RUN manifests,
REPORT manifests, EVIDENCE manifests, gate registry, retraction registry,
frozen-baseline registry, hash verification, PROJECT_STATE delta, Rosetta delta.
pe-master-auditor NIE kuratoruje dossieru: może wyłącznie DODAĆ AUDITOR_NOTES /
KNOWN_DISAGREEMENTS / OPEN_FINDINGS; nigdy nie filtruje runów ani dowodów (audytowany
nie kuratoruje okna, przez które jest audytowany). Każdy rekord dziennego audytu zawiera
DOSSIER_SHA256 + BUILDER_SCRIPT_SHA256 + ANCHOR_SHA + HEAD_SHA. Desktop czyta repo i
dysk bezpośrednio i może sam odtworzyć każde pole dossieru; nieodtwarzalne pole
= finding.

**A1.5 — Triggery DAILY.** (A) elapsed>=24h AND delta!=empty; OR (B)
MATERIAL_RUN_COUNT>=8; OR (C) LOAD_BEARING_RUN_COUNT>=3; OR (D) new RETRACTION; OR
(E) milestone gate package created — przy czym (E) MA PODWÓJNY ROUTING: (E1) ostatni
dzienny audyt delty PRZED zamrożeniem paczki (wejście do pre-checku PE-MASTER) oraz
(E2) otwarcie trybu MILESTONE na relayu człowieka. Dwa tryby Desktopu (DAILY i
MILESTONE) nigdy się nie mieszają — także na poziomie triggerów. Gdy przez okno
triggerów nic istotnego się nie wydarzy: status NO_MATERIAL_DELTA i NIE uruchamia się
Desktopu dla rytuału.

**A1.6 — Pętla poprawek.** finding → correction → NEW RUN_ID → świeża sesja/kontekst
bez historii argumentacji poprzedniego auditora (wejście przez artefakty) → audyt.
Nigdy ta sama sesja nie certyfikuje własnego rozkazu poprawy.

**A1.7 — Tabela ról (verbatim z decyzji człowieka).**

| Rola | Odpowiedzialność |
|---|---|
| PE-MASTER | projekt, roadmapa, dependency graph, wybór pracy, głęboki audit istotnych runów |
| PE-RECONSTRUCTION | wykonanie RE/implementacji/eksperymentów |
| PE-MASTER-AUDITOR | bezpośredni QC runów i evidence (nie executor-of-record własnych audytowanych runów; separacja sesyjna) |
| ChatGPT Desktop DAILY | niezależne badanie przyrostu + audit-of-auditors (CANONICAL_GATE_EFFECT=NONE dla PASS) |
| ChatGPT Desktop MILESTONE | pełny niezależny post-audit całego milestone (nigdy nie zastępowany sumą daily PASSów) |
| CZŁOWIEK | strategiczna autoryzacja i MILESTONE_CLOSED |

**A1.8 — Tryb MILESTONE nienaruszony.** pre-check PE-MASTER → paczka gate → HARD STOP
→ Desktop deep post-audit (pełnozakresowy) → decyzja człowieka. Suma daily PASSów
nigdy nie zamyka bramki §13 C.

**A1.9 — Wersjonowanie.** Niniejsza nowela = A-1 / governance v2.0. Dalsze zmiany
modelu idą WYŁĄCZNIE przez jawne nowele z numerami (append-only, z changelogiem), nigdy
ad hoc w promptach. Kontrakt PE-MASTER HUMAN AUDIT CONTRACT v1 = plik
`PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md` (repo root), przywołany niniejszą nowelą jako
wiążący format każdego istotnego audytu PE-MASTER od tej chwili.

*Changelog modelu: A-1 (2026-09-06) — governance v2.0 (niniejsza nowela; pierwszy wpis
changeloga).*
