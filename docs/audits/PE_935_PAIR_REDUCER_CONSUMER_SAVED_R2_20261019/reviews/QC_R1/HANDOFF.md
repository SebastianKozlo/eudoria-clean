# HANDOFF — QC_R1 → PE-MASTER

RUN_ID: PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_QC_R1_20261019 | AUDITOWANY_RUN: PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019
TRYB: INTERNAL_QC (niezależny QC wewnętrzny; nie postaudyt zewnętrzny; nie MASTER_ACCEPTED; run nie zamknięty; seal i manifest należą do rodzica)

## Werdykty

- **P01_ADAPTER: PASS** — 0 findings w pakiecie; wszystkie obowiązkowe testy niezależne potwierdzone (ESP, partial-store, pointer-holder, dead args, containment, no-store-to-global). Najwyższa jakość dokumentacji w runie.
- **P02_CONSUMER: PASS_WITH_FINDINGS** — 2×P3 (F-P02-01 sloty +4 w §7; F-P02-02 forma dowodzenia B08). Wszystkie claims load-bearing potwierdzone niezależnie, w tym deferred-cleanup 0x28/0x38 byte-exact i premise 006C2C50 z 3 falsyfikatorami (falsyfikator #2 potwierdzony niezależnie).
- **P03_PUMP: PASS_WITH_FINDINGS** — 2×P2 (F-P03-01 opis przepływu PATH-NULL-B; F-P03-02 status K08 + linia upgrade GLOBAL-ELEMENT-ORIGIN), 4×P3 (target-list 00823df/00823dce; args vtable+0x3C; kolejność 004D1430; VA FS-restore). Nauka potwierdzona niezależnie: obie ścieżki zwrotu (fast vtable+0x38 / loop vtable+0x4), oba DWORD pary czytane, containment (21 skoków/16 celów, wszystkie w oknie — programowo), ABI RET 0x10 zgodny dwustronnie z P01, arg4 dead, TLS flag, EH-scope alloc/free.
- **P04_FRONTIER: PASS_WITH_FINDINGS** — 2×P2 (F-P04-01 cel zapisu trzech zer = out-arg wywołującego, nie „translation of the copied transform"; status K05 zawyżony; F-P04-02 „callee-clean NOT needed" fałszywe — model głębokości wymaga virtual RET 4 + 0096CB20 RET 0x24, potwierdzone koherencją bufora ESP0−0x54), 2×P3 („12-float block"→9-float gather; newyliczone przerwy paddingowe). Sloty +0x24/+0x28, NiTransform STRUCTURAL_ONLY (0x34=9+3+1, scale 1.0f), brak join z primary thread, live edge — potwierdzone.
- **RUN_LEVEL: QC_PARTIAL** — F-RUN-01 (P2): timestampy „(approx)" P03/P04 sprzeczne z łańcuchem guard (ADMIT 15:00:59Z/15:22:14Z); naruszenie §9 (faktyczne czasy UTC). F-RUN-02/03/04 (P3): brak P04_CONTRACT.json; „extract_dir" w P01_CONTRACT; cieńsza dokumentacja P03/P04.

## Wyniki testów obowiązkowych (skrót; pełne dane w RECHECKS.json)

1. **Re-hash/bijekcja**: 4/4 ekstrakty = sha z przydziału/admission/kontraktów; source pin 642CC29A…/50780146 B; CONTRACT.md 7494B714… = PREFLIGHT; guard chain 5/5 spójny; artifact_index P01/P02 18/18 zgodnych; **bijekcja ekstrakt↔źródło 449/449 wierszy verbatim**; seam-y P02↔prior (5B CALL rel32; 8B C7-44-24-50) dokładne; 82 wiersze prior delta-poprawne.
2. **Bilans ESP (pump 006C29D0→0x00823C10 i inne)**: pump prolog 0x3C / epilog POP×5+ADD 0x28 / RET 0x10 → ESP0+0x14 — policzone samodzielnie z surowych wierszy, zgodne z pakietem i dwustronnie z P01. Dodatkowo adapter, 006C4060, 0085BFA0, 0085C0F0/0085C130 — wszystkie zbalansowane (0085BFA0 warunkowo, patrz F-P04-02).
3. **Low-byte vs DWORD**: A13 ✓ (tylko bajt 0 ctx[5] konsumowany; slot arg3 patchowany bajtowo = (S+0x10)&~0xFF|1); C3 ✓ na surowych wierszach (byte store @006C4125, full-dword load @006C412A); nieustalone górne 24 bity nigdzie nie wpływają na admitowaną kalkulację; P03 K12 dodatkowo: pump nie czyta arg4.
4. **Pointer holder**: arg3=S+0x10, dokładnie jeden deref poziomu 1 → pair_ptr ✓; kontynuacja pair[0]/pair[1] w pumpie ✓; poziomy zgodne z C4 i P01 A05.
5. **Budżet**: 14 bodies / 449 rows / 39 calls / 12 candidates = sumy eventów = sumy pakietów; obciążenia bez refundacji (3/4/3/4 pełne); INCIDENTS puste; widoczne ciała ≤ rezerwacje wszędzie; pozycja PIVOT zgadza się co do wiersza.
6. **Chronologia**: guard spójny; P01/P02 RUN_STARTED koherentne z guard; **P03/P04 sprzeczne (F-RUN-01)**; brak jakichkolwiek śladów operacji na oryginale/runtime w plikach runu (census negatywny).

## Zgodność z korektami C1–C8 / promocja kanonu

C1–C8 zachowane we wszystkich pakietach; C6 rozwiązane body-proofem z jawnym zapisem konfliktu (nie cicho); brak promocji kanonu (CORRECTIONS canonic_promotion=false); jedyny kandydat zmiany standing między-pakietowej: linia P03 GLOBAL-ELEMENT-ORIGIN — jawna, ale z zawyżonym statusem i bez adjudykacji rodzica (F-P03-02). Dwie promocje STRUCTURE→SEMANTICS pod CONFIRMED wykryte i do re-etykietowania (F-P03-02, F-P04-01).

## Następne działanie rodzica (propozycja)

1. Corrigendum P03 (§3 PATH-NULL-B; K08/etykieta; §7 lista targetów; §2/§3 args; STACK_MAP VA) i P04 (K05 cel zapisu + status; STACK_MAP premise; §1 chain) — nowe katalogi, bez modyfikacji zamrożonych pakietów.
2. Corrigendum run-level: RUN_STARTED P03/P04 czasy → źródło guard-ledger (lub „unknown"); opcjonalnie P04_CONTRACT.json.
3. Adjudykacja standing-change GLOBAL_ELEMENT_KIND: przyjąć OBJECT_POINTER_OR_ZERO jako STRONGLY_SUPPORTED albo sfinansować admission ABI 00826760/00826840 (jeśli wymagany CONFIRMED).
4. Seal runu z MANIFEST (pierwsze exclusive-create; root self-excluded) i publikacja wg §10 kontraktu; nie publikować surowych ekstraktów.
5. QC_R1 włączyć do pieczęci jako artefakt QC (artifact_index QC_R1: REPORT/RECHECKS/HANDOFF z hashami; index self-excluded).

## Zakres i granice QC

Czytane: przydzielone pakiety (wszystkie pliki do EOF), ekstrakty, CONTROL (events/plans/requests/incidents), pliki run-root, kontrakt authoringu + szablon, kotwice z zamrożonych priorów (W1/W2/P10, anchor-level), przypięte źródło wyłącznie hashowane + bijekcja wierszowa na wierszach już admitowanych. NIE czytane/wykonane: ciała opaque callee, kod guard, semantyka 0085C130 po oknie, operacje na oryginale/runtime (zakazane; brak śladów). Nie tworzę nowych wniosków naukowych spoza admitowanego materiału; HARD STOP po review.

Artefakty QC_R1: REPORT.md (26 468 B), RECHECKS.json (77 239 B, machine-readable, z pełną mapą hashy i wynikami programowymi), HANDOFF.md, artifact_index.csv (self-excluded).
