# AUTHORIZATION — PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003

```text
RUN_ID = PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003
RUN_TYPE = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION
RUN_CLASS = LOAD_BEARING (PE-MASTER declaration per POM A1.1)
DISPATCH = PE-MASTER direct dispatch to pe-master-auditor (PHASE A: FORMALIZATION + BUDGET PREREGISTRATION); NO_NESTED_TASKS
MODE = STATIC_ONLY
DATE = 2026-10-03
CANONICAL_GATE_EFFECT = NONE
MILESTONE NAMESPACE = EU935-M1 (OPEN)
PRIMARY_TARGET = PCG_9_3_5 / Entropia Universe 9.3.5
EXPECTED_BASE_SHA = b151d428fc46818bc3b84d8ca000d92caa2cd76b
AUDITED_DESKTOP_SHA = b151d428fc46818bc3b84d8ca000d92caa2cd76b
TRANSPORT_SIZE_BYTES = 31499
TRANSPORT_SHA256 = 7FCFA68E5CCEDB1B65C08C30EB2F9054C6E73AF325E32B8F31F2DE15905D3572
```

## PROVENANCE OF THIS ORDER

- The order below was received VERBATIM from the human, directly in the PE-MASTER session (OpenCode, workspace D:\TESTAI) on 2026-10-03. No message ID exists on this channel — none was invented.
- PE-MASTER pinned the received order to a transport file OUTSIDE the repository (transport channel only, NOT project evidence):

```text
TRANSPORT_PATH = C:\Users\User\AppData\Local\Temp\opencode\PE_CORRECTION_TRANSPORT\PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_ORDER.md
TRANSPORT_SIZE_BYTES = 31499
TRANSPORT_SHA256 = 7FCFA68E5CCEDB1B65C08C30EB2F9054C6E73AF325E32B8F31F2DE15905D3572
```

- Independently verified by this formalizer before reliance (2026-10-03, measured before any other action): SIZE_BYTES = 31499 and SHA256 = 7FCFA68E5CCEDB1B65C08C30EB2F9054C6E73AF325E32B8F31F2DE15905D3572 — both MATCH the pinned values. Physical file properties: UTF-8, no BOM, no trailing newline, 2,052 lines, maximum line length 130 chars.
- This AUTHORIZATION.md persists the order verbatim as this run's authoritative contract.
- Byte-identity method: the verbatim block below was embedded by byte-exact concatenation of the physical transport file (no retyping, no transcoding, no BOM introduction). The embedded 31,499-byte block was re-hashed after assembly; the verification result is recorded in 00_CONTROL/PREFLIGHT.md section 7.
- Dispatch-metadata observation (no effect on identity): the PHASE A dispatch described the transport as "~700 lines"; the physical transport file contains 2,052 lines. Transport identity is bound by size + SHA256 — both match the pinned values exactly; the line-count note in the dispatch is a description discrepancy only, recorded here for provenance transparency.

## HUMAN AUTHORIZATION ORDER (VERBATIM)

The complete transport file content follows, byte-faithful: the Polish text, the code fences and the section numbering are preserved exactly; nothing was added, removed or "improved" inside the block. The verbatim block starts on the next line and comprises exactly 31,499 bytes (the source file has no trailing newline; the block ends with the closing triple-backtick fence of order section 22, and the line break separating it from the END marker below was added by the assembly, outside the verbatim block).

<<<VERBATIM TRANSPORT FILE CONTENT BEGINS ON THE NEXT LINE>>>
# PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1

```text
RUN_ID =
PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003

RUN_TYPE =
DESKTOP_POST_AUDIT_FOCUSED_CORRECTION

AUDITED_DESKTOP_SHA =
b151d428fc46818bc3b84d8ca000d92caa2cd76b

EXPECTED_BASE_SHA =
b151d428fc46818bc3b84d8ca000d92caa2cd76b

PRIMARY_TARGET =
PCG_9_3_5 / Entropia Universe 9.3.5

MILESTONE =
EU935-M1 — OPEN

CANONICAL_GATE_EFFECT =
NONE
```

---

# 0. HUMAN AUTHORIZATION

Wykonaj **JEDEN bounded correction/persistence cycle** dla niezależnego Desktop post-audit dokładnego commita:

```text
b151d428fc46818bc3b84d8ca000d92caa2cd76b
```

Desktop verdict dla tego SHA:

```text
POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS
SUPPORTED_RESULT_LEVEL = B
CANONICAL_GATE_EFFECT = NONE

OPEN_FINDINGS:
F-D1 = P1
F-D2 = P2
F-D3 = P2
F-D4 = P2
```

Desktop audit NIE obalił głównego record→resource chain.

Potwierdzony zakres pozostaje:

```text
physical templates record 4508
→ parser / registry
→ keyed lookup
→ A at template+0x08
→ request pair {0x66, A=296445}

SEPARATELY:
A=296445
↔ Models.bnt index entry "296445.nif"
```

Nie udowodniono:

```text
runtime physical open of the NIF
physical record → world-instance identity
world-instance transform
persistent static placement
historical world XYZ
```

## Autoryzowane

To zlecenie AUTORYZUJE wyłącznie:

- korektę F-D1..F-D4;
- niezbędne current-state supersessions/retractions wynikające z tych findingów;
- ograniczone post-audit source identity verification potrzebne dla F-D3;
- prerejestrację i pomiar nowego correction/QC budget;
- fresh targeted QC w świeżym kontekście;
- final report/review/handoff/disposition records;
- factual correction row w `AUDIT_ENTRYPOINT.md`;
- final manifest;
- commit + push;
- live remote verification.

## Nieautoryzowane

To zlecenie NIE AUTORYZUJE:

- nowego RE;
- nowej eksploracji Ghidra;
- uruchamiania klienta;
- runtime capture;
- nowego placement trace;
- śledzenia budynku/template `4057`;
- śledzenia `0x0059AB12`;
- rodziny `0x008D–0x008F`;
- szukania XYZ;
- Q1;
- zmiany kwalifikacji PE-MASTERA;
- zamknięcia M1;
- autoryzacji M2/M3;
- następnego eksperymentu;
- history rewrite;
- amend commita `b151d428...`;
- force-push;
- usuwania lub przepisywania historycznego evidence;
- promocji żadnego UNKNOWN.

Historia musi pozostać jawna:

```text
b151d428...
Desktop verdict = REQUIRE_CORRECTIONS
```

Nowy correction commit NIE może retrospektywnie zmieniać tego werdyktu na PASS.

---

# 1. BOOT — OBOWIĄZKOWE PRZED PRACĄ

Najpierw wykonaj:

```text
git fetch
```

Zweryfikuj niezależnie:

```text
HEAD
==
origin/master
==
git ls-remote origin refs/heads/master
==
b151d428fc46818bc3b84d8ca000d92caa2cd76b
```

Jeżeli którakolwiek wartość jest inna:

```text
HARD_STOP = BASE_MISMATCH
```

i nie wykonuj korekty.

Sprawdź:

- zero nieoczekiwanych tracked modifications;
- zero staged changes;
- wszystkie wcześniej znane obce/untracked grupy pozostają nietknięte;
- `AUDIT_ENTRYPOINT.md` odpowiada live HEAD;
- istnieje oryginalny pakiet:

```text
docs/audits/
PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
```

Odczytaj jako obowiązkowe minimum:

```text
PROJECT_OPERATING_MODEL.md
CHATGPT_ARCHITECT_INSTRUCTIONS.md
AUDIT_ENTRYPOINT.md

oryginalny:
00_CONTROL/
02_ANALYSIS/TRACE_EDGE_BLOCKS.md
02_ANALYSIS/CLAIM_MATRIX.csv
02_ANALYSIS/NOT_CHECKED.md
02_ANALYSIS/RETRACTIONS_SUPERSESSIONS.md
05_ORACLE/ORACLE_RECORDS.md
06_REPORT/DRAFT_FINAL_REPORT.md
06_REPORT/PE_MASTER_REVIEW.md
06_REPORT/FINAL_REPORT.md
07_QC/QC_AUDIT_R1.md
07_QC/QC_RECHECK_R1.md
```

Nie traktuj wcześniejszego:

```text
MASTER_ACCEPTED
```

jako nadrzędnego wobec późniejszego niezależnego Desktop post-audit.

Dla `b151d428...` obowiązuje:

```text
DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS
```

---

# 2. OUTPUT ROOT

Utwórz NOWY correction package:

```text
docs/audits/
PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003/
```

Nie modyfikuj historycznego package `b151d428` kosmetycznie, jeśli nie jest to absolutnie konieczne do ustanowienia current state.

Preferuj:

```text
HISTORICAL ARTIFACT
→ preserved

NEW CORRECTION RECORD
→ explicitly supersedes current meaning
```

W nowym pakiecie co najmniej:

```text
00_CONTROL/
  AUTHORIZATION.md
  PREFLIGHT.md
  CORRECTION_BUDGET.md

01_ANALYSIS/
  DESKTOP_FINDINGS.md
  CORRECTION_MATRIX.csv
  HISTORY_BUDGET_RECONCILIATION.md
  CURRENT_CLAIM_STATE.md
  DEFERRED_PLACEMENT_LEADS.md

02_QC/
  TARGETED_QC_REPORT.md
  raw/   (tylko bounded własne pomiary QC)

03_REPORT/
  FINAL_REPORT.md
  HANDOFF.md
  FINDING_DISPOSITION.md

MANIFEST_SHA256.csv   [GENEROWANY LAST]
```

Nazwy mogą zostać minimalnie dostosowane, ale semantyczny zakres musi zostać zachowany.

---

# 3. NOWE BUDŻETY TEGO CORRECTION CYCLE — PREREGISTER PRZED PRACĄ

**PRZED pierwszą edycją, pomiarem korekcyjnym lub source verification** zapisz:

```text
00_CONTROL/CORRECTION_BUDGET.md
```

Twarde limity:

```text
CORRECTION_EXECUTOR_MAX_TOOL_CALLS = 80
CORRECTION_EXECUTOR_MAX_WALL_MINUTES = 120

FRESH_TARGETED_QC_MAX_TOOL_CALLS = 70
FRESH_TARGETED_QC_MAX_WALL_MINUTES = 90

QC_REPAIR_ROUNDS_MAX = 1
```

Repair round może zostać użyty WYŁĄCZNIE do naprawy defektu wytworzonego przez tę korektę.

Nie może służyć do nowego science.

## COUNTING_RULE

Zapisz przed rozpoczęciem:

```text
1 explicit tool invocation = 1 tool call.

A single tool invocation containing multiple shell/analysis commands
still counts as 1 tool call.

Internal reasoning without a tool invocation = 0.

Failed calls count.

Retries caused by auditor/executor instrument errors count.

Subagent/nested context calls, jeśli w ogóle dozwolone,
muszą być rozliczane jawnie w budżecie właściwej fazy.

Counters start at zero independently for:
A. correction executor
B. fresh targeted QC

No silent budget expansion.

When the cap is reached:
STOP and report PARTIAL / REVALIDATION_REQUIRED honestly.
```

Te budżety są NOWE:

```text
NEW_CORRECTION_CYCLE_BUDGETS = YES
```

Nie wolno na ich podstawie dopisywać historycznie:

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED = YES
```

Historyczny stan pozostaje osobnym findingiem F-D4.

---

# 4. F-D1 — P1 — E10 SEMANTIC RETRACTION

To jest najważniejsza korekta merytoryczna.

## Co pozostaje CONFIRMED

Nie zmieniaj obserwowanej operacji:

```text
templates.vfs list2
→ 9 × u32 when the size gate permits
→ accessed/copied as three 3-component groups
→ interpreted operationally as floats
→ FUN_006C1F90 performs component-wise interpolation
→ result is written as three float components to a runtime slot
```

Zapisz:

```text
E10_OBSERVED_OPERATION = CONFIRMED
```

## Co musi zostać wycofane

Nie wolno już jako bieżącego claimu używać:

```text
positions
slot-position
payload-derived position
payload-derived transform
spatial vec3
world transform
```

dla E10.

Obecny status musi być:

```text
E10_FINAL_SEMANTIC_ROLE = UNVERIFIED

E10_SPATIAL_POSITION_OR_TRANSFORM =
NOT_ESTABLISHED

E10_SLOT_CLASS =
UNKNOWN
```

## Alternatywa kolorystyczna

Desktop wskazał fizyczny falsifier semantic certainty dla rekordu `11963`.

Trzy grupy floatów:

```text
(0.0705882, 0.2627450, 0.3529410)
(0.1137250, 0.1137250, 0.1137250)
(0.0000000, 0.5372550, 0.7176470)
```

są zgodne również z hipotezą normalized RGB-like values około:

```text
(18, 67, 90)
(29, 29, 29)
(0, 137, 183)
```

To jest WYŁĄCZNIE kontrpróba dla przestrzennej pewności.

Zapisz:

```text
COLOR_VECTOR_HYPOTHESIS =
PLAUSIBLE_ALTERNATIVE_ONLY
```

NIE zapisuj:

```text
E10 = COLOR
```

Nie buduj decoderów kolorów.

Nie wykonuj nowego consumer trace.

## Wymagane globalne statusy po F-D1

```text
WORLD_INSTANCE_IDENTITY =
NOT_ESTABLISHED

WORLD_INSTANCE_EDGE =
NOT_ESTABLISHED

PERSISTENT_PLACEMENT_EDGE =
NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED =
NO
```

## Surfaces

Zaktualizuj wszystkie AKTYWNE/current surfaces tak, aby nie propagowały starej semantyki E10.

Nie trzeba usuwać starego tekstu z historycznego `b151d428` package.

Nowy correction state ma jawnie powiedzieć:

```text
Historical E10 position/transform wording from b151d428
is SUPERSEDED by this correction.
```

---

# 5. F-D2 — P2 — E2/E3 ABI / INPUT PROVENANCE

Skoryguj calling convention i provenance argumentów.

Fizyczny flow:

```text
MOV EAX,[ESP+0x0C]   ; id2
PUSH EAX             ; id2 remains stack argument
CALL FUN_0043A550    ; registry singleton getter
MOV ECX,EAX          ; ECX = registry this
CALL FUN_0072F580    ; lookup(id2)
```

Poprawny model:

```text
registry_this.FUN_0072F580(id2)
```

gdzie:

```text
ECX = registry_this

id2 = stack argument
```

NIE wolno już pisać dla wejścia do lookupu:

```text
ECX = id2
```

Po lookupie:

```text
EAX = template pointer
EDI = template pointer

MOV ECX,EDI
→ getter A
```

pozostaje poprawne.

## Blast radius

F-D2 NIE obala:

```text
id2
→ registry lookup
→ template
→ A @ +0x08
→ A=296445
```

ani osobnego:

```text
296445
↔
"296445.nif"
```

Status:

```text
MAIN_MAPPING_IMPACT = NONE
ABI_DESCRIPTION_CORRECTED = YES
```

---

# 6. F-D3 — P2 — GAMEBRYO ORACLE #3 PROVENANCE

Mechanizm #3 wymaga poprawienia provenance.

Dotychczasowa ogólna referencja:

```text
CoreLibs\NiMain\NiAVObject.cpp
```

nie jest wystarczającym locatorem implementacji.

Desktop ustalił właściwą implementację Win32:

```text
CoreLibs/NiMain/Win32/NiAVObject_Win32.cpp:22
```

## Dozwolony bounded check

Wykonaj WYŁĄCZNIE statyczne source identity verification tego jednego pliku/mechanizmu.

Możesz zmierzyć:

```text
exact path
file size
SHA256
exact line/function locator
```

Jeżeli pomiar wykonujesz teraz, zapisz:

```text
POST_AUDIT_SOURCE_CHECK = YES
MEASURED_DURING_CORRECTION = YES
```

Nie backdate'uj tego jako wiedzy pierwotnego executora.

Rozdziel:

```text
HISTORICAL_ORACLE_REFERENCE
```

od:

```text
POST_AUDIT_SOURCE_VERIFICATION
```

Nie dodawaj nowego mechanizmu oracle.

Limit historyczny pozostaje:

```text
ORACLE_MECHANISMS = 3
```

Nie wykonuj:

- Gamebryo inventory;
- SDK build;
- runtime Gamebryo;
- nowych cross-version searches.

## Target-local evidence

Nie obniżaj target-side evidence wynikającego bezpośrednio z `Entropia.exe`.

W szczególności:

```text
NiNode slot27
m_kLocal-shaped +0x38
parent m_kWorld-shaped +0x6C
MOV ECX,13
REP MOVSD
```

pozostają niezależnymi obserwacjami target-local.

---

# 7. F-D4 — P2 — HISTORYCZNY BUDŻET / PROCESS CENSUS

Nie próbuj „naprawić historii".

Utwórz:

```text
01_ANALYSIS/HISTORY_BUDGET_RECONCILIATION.md
```

## Historyczne preregistered executor budgets

Zachowaj:

```text
EXECUTOR_ENUM_BUDGET =
PREREGISTERED_MAX_30

EXECUTOR_DEEP_TRACE_BUDGET =
PREREGISTERED_MAX_90

EXECUTOR_CONTROLS_ORACLE_BUDGET =
PREREGISTERED_MAX_30
```

## QC

Historyczny stan:

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED =
NOT_ESTABLISHED
```

Nie wolno zmienić go na YES.

## Tool-call census Desktopu

Zweryfikuj ze źródła/session store, JEŚLI jest dostępne, cztery liczby:

```text
executor initial phase = 125 tool calls
executor repair phase = 23 tool calls
fresh QC = 109 tool calls
focused re-QC = 69 tool calls
```

Dla każdej zapisz:

```text
VALUE =
SOURCE =
SESSION_ID / SOURCE_IDENTIFIER =
COUNT_SCOPE =
COUNTING_METHOD =
INDEPENDENTLY_RECOMPUTED = YES/NO
PROVENANCE_STATUS =
```

Jeżeli nie jesteś w stanie niezależnie odtworzyć liczby, NIE udawaj pomiaru.

Zapisz:

```text
INHERITED_FROM_DESKTOP_POST_AUDIT
```

z dokładnym źródłem.

## Wcześniejsze deklaracje

Zinwentaryzuj:

```text
~41 analytical invocations
```

oraz:

```text
~14 / ~27 / ~10
```

Ustal:

- gdzie zostały zapisane;
- co miały liczyć;
- czy istnieje reprodukowalna reguła liczenia;
- czy da się je uzgodnić ze store census.

Jeżeli nie:

```text
STATUS = UNVERIFIED / NON_RECONSTRUCTABLE
```

Nie wymyślaj denominatora po fakcie.

## Wymagany finalny status F-D4

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED =
NOT_ESTABLISHED

HISTORICAL_TOOL_CALL_CENSUS =
MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE

HARD_HISTORICAL_PHASE_LIMIT_BREACH =
NOT_DEMONSTRATED

FULL_HISTORICAL_BUDGET_CONFORMANCE =
NOT_PROVEN
```

Bardzo ważne:

całkowita liczba tool calls w sesji NIE pozwala sama z siebie stwierdzić:

```text
ENUM > 30
DEEP_TRACE > 90
CONTROLS+ORACLE > 30
```

bo historycznie nie zapisano reguły przypisywania wszystkich tool calls do tych faz.

F-D4 zostaje zamknięte przez:

```text
honest process record
+
retraction of full-conformance claim
+
preservation of NOT_ESTABLISHED
```

Nie przez retroaktywny PASS.

---

# 8. DODATKOWE NIEBLOKUJĄCE DOPRECYZOWANIA

Tylko jeśli występują w ACTIVE/current state.

## A. Decompilation counts

Rozróżniaj:

```text
DECOMPILATION_RECORDS = 88
```

od:

```text
UNIQUE_FUNCTION_ENTRY = 87
```

jeżeli świeży recount potwierdzi te wartości.

Nie nazywaj automatycznie:

```text
88 unique functions
```

Hard limit 120 nie jest wykazany jako przekroczony.

## B. list1

Nie przedstawiaj pełnego schema `list1` wyłącznie jako:

```text
count × strings
```

jeżeli element `0x20` obejmuje również dwa dalsze `u32`.

Status tych dwóch pól:

```text
UNKNOWN
```

Nie rozszerzaj parsera w tej korekcie.

## C. Reader census

Claim:

```text
templates reader = 1 caller
```

musi być oznaczony jako:

```text
CENSUS_BOUNDED_OBSERVATION
```

Nie:

```text
GLOBAL_PROOF_OF_ONLY_POSSIBLE_READER
```

Brak bezpośredniego file-read w danym construction chain NIE dowodzi, że dane nie zostały wcześniej załadowane do pamięci.

Zachowaj:

```text
WORLD_INSTANCE_EDGE = NOT_ESTABLISHED
```

a nie:

```text
WORLD_INSTANCE_EDGE DOES NOT EXIST
```

---

# 9. GŁÓWNY SCIENCE CHAIN — INVARIANTS

Korekta nie może bez nowego dowodu zmienić następującego wyniku:

```text
physical templates record 4508
→ parser
→ registry
→ keyed lookup
→ A @ template+0x08
→ request pair {0x66, A=296445}
```

oraz osobno:

```text
A=296445
↔
Models.bnt index entry "296445.nif"
```

## Wymagany current state

```text
MAIN_RECORD_REQUEST_INDEX_CHAIN =
SUPPORTED

RESULT_LEVEL =
B

MODEL_ID_RECOVERED =
YES

RUNTIME_NIF_OPEN =
NOT_CLOSED

WORLD_INSTANCE_IDENTITY =
NOT_ESTABLISHED

WORLD_INSTANCE_EDGE =
NOT_ESTABLISHED

PERSISTENT_PLACEMENT_EDGE =
NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED =
NO

E10_FINAL_SEMANTIC_ROLE =
UNVERIFIED

E10_SPATIAL_POSITION_OR_TRANSFORM =
NOT_ESTABLISHED

CANONICAL_GATE_EFFECT =
NONE

PE_MASTER_QUALIFICATION_CHANGE =
NO

M1_CLOSED =
NO

M2_AUTHORIZED =
NO

M3_AUTHORIZED =
NO

NEXT_EXPERIMENT_AUTHORIZED =
NO
```

---

# 10. DESKTOP VERDICT — HISTORY MUST SURVIVE

Dla commita:

```text
b151d428fc46818bc3b84d8ca000d92caa2cd76b
```

zachowaj historycznie:

```text
DESKTOP_POST_AUDIT_VERDICT =
REQUIRE_CORRECTIONS

OPEN_AT_DESKTOP_AUDIT:
F-D1 = P1
F-D2 = P2
F-D3 = P2
F-D4 = P2
```

Nowy correction commit może ustalić:

```text
F-D1 = CORRECTED
F-D2 = CORRECTED
F-D3 = CORRECTED
F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD
```

ale nie wolno zmienić historycznego verdictu dla `b151d428`.

---

# 11. DEFERRED PLACEMENT LEAD — TEMPLATE 4057 / MODEL 218757

## RECORD ONLY — DO NOT EXECUTE

Podczas wcześniejszej lokalnej diagnostyki powstał bardzo obiecujący, ale **NIEZWERYFIKOWANY** model-specific placement lead.

Zapisz go wyłącznie w:

```text
01_ANALYSIS/DEFERRED_PLACEMENT_LEADS.md
```

oraz w HANDOFF jako candidate future experiment.

NIE wykonuj jego RE podczas tej korekty.

## Dostarczony lokalny lead

```text
candidate template id2 = 4057

candidate model:
A = 218757

candidate collision:
B = 218758

candidate client immediate:
VA 0x0059AB12
PUSH 0x00000FD9 = 4057

nearby immediate:
886
```

Wcześniejsza lokalna analiza twierdziła także:

```text
218757.nif exists in Models.bnt
218758.bvi exists in Volumes.bnt
```

ale ponieważ te wyniki nie są częścią bieżącego opublikowanego kanonu tego correction runu:

**nie repinuj ich teraz i nie promuj ich.**

Zapisz je jako:

```text
LOCAL_LEAD_TO_BE_REPINNED_IN_FUTURE_AUTHORIZED_RUN
```

## Human context

Człowiek wskazuje model `218757` jako potencjalnie bardzo użyteczny probe object, ponieważ z pamięci historycznej:

```text
- był charakterystycznym statycznym budynkiem/landmarkiem;
- prawdopodobnie występował tylko w jednej lokalizacji świata.
```

Ta pamięć:

```text
HUMAN_HISTORICAL_RECOLLECTION
```

jest wyłącznie podstawą wyboru testowego obiektu.

Nie jest dowodem:

```text
instance count = 1
world position
template semantics
hardcoded placement
```

## Current epistemic status

Zapisz dokładnie:

```text
4057_EXISTS_AS_TEMPLATE_ID =
LOCAL_LEAD / TO_BE_REPINNED

4057_TO_A218757_MAPPING =
LOCAL_LEAD / TO_BE_REPINNED

B218758_COLLISION_MAPPING =
LOCAL_LEAD / TO_BE_REPINNED

IMMEDIATE_4057_AT_0x0059AB12 =
LOCAL_LEAD / TO_BE_REPINNED

IMMEDIATE_4057_IS_TEMPLATE_ID =
UNVERIFIED

HARDCODED_TEMPLATE_REFERENCE_4057 =
UNVERIFIED

CLIENT_CONSTRUCTS_MODEL_218757_HERE =
UNVERIFIED

STATIC_BUILDING_INSTANCE =
UNVERIFIED

STATIC_LANDMARK_CONSTRUCTION_PATH =
UNVERIFIED

WORLD_TRANSFORM_SOURCE =
UNKNOWN

PLACEMENT_XYZ =
UNKNOWN

IMMEDIATE_886_SEMANTIC_ROLE =
UNKNOWN
```

## Niedozwolone podczas correction cycle

Nie:

- otwieraj Ghidry wokół `0x0059AB12`;
- dekompiluj containing function;
- śledź callee;
- skanuj rodziny `0x008D–0x008F`;
- skanuj EXE ponownie dla 4057/218757;
- szukaj XYZ;
- szukaj podobnych immediate;
- zgaduj znaczenie 886;
- próbuj udowodnić, że 4057 jest template ID;
- próbuj połączyć 4057 z registry;
- próbuj połączyć 218757 z runtime instance.

To ma być WYŁĄCZNIE preservation of lead.

---

# 12. CANDIDATE NEXT EXPERIMENT — DESIGN ONLY, NOT AUTHORIZED

W `DEFERRED_PLACEMENT_LEADS.md` zapisz projekt następnego bounded experimentu, ale go NIE uruchamiaj.

```text
CANDIDATE_RUN_TITLE =
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1

AUTHORIZATION_STATUS =
NOT_AUTHORIZED
```

## Anchor

```text
VA 0x0059AB12
candidate raw immediate = 4057
```

## Primary question

```text
What semantic role does immediate 4057 have at this call-site,
and does its dataflow reach the templates registry,
model/resource construction,
or world-instance transform machinery?
```

## Mandatory falsifier

Najważniejszy test:

```text
If immediate 4057 does NOT reach FUN_0072F580
or another independently proven template-id consumer,
the numeric equality with templates.vfs id2=4057
must be treated as coincidental and the lead rejected.
```

## Future proof ladder — only after separate human authorization

```text
1. RAW BYTE PIN
   verify 0x0059AB12 physically

2. FUNCTION BOUNDARY
   identify full containing function

3. ARGUMENT ROLE
   determine exact argument position / dataflow role of 4057

4. CALLEE
   resolve immediate/direct callee(s)

5. SEMANTIC DATAFLOW
   follow 4057 WITHOUT assuming id2 semantics

6. TEMPLATE TEST
   prove or falsify:
   4057 → FUN_0072F580
   or another independently proven template consumer

7. ONLY IF STEP 6 PASSES
   re-pin:
   template id2=4057
   → A=218757
   → resource identity

8. OBJECT IDENTITY
   determine what object is created/referenced

9. TRANSFORM PRODUCER
   find first producer of transform-like values for SAME object

10. CLASSIFY TRANSFORM PROVENANCE
    - hardcoded immediate?
    - global/static table?
    - local physical data?
    - message?
    - runtime attribute?
    - parent-relative?
    - other/unknown?

11. WORLD / SCENE EDGE
    only if identity is preserved:
    object → scene insertion / world transform

12. STATIC PLACEMENT CANDIDATE
    only if a concrete transform joins the same proven instance
```

## Separate unknown: immediate 886

```text
IMMEDIATE_886 = OBSERVED_LOCAL_LEAD
FINAL_SEMANTIC_ROLE = UNKNOWN
```

Nie zgaduj:

```text
instance ID
zone ID
class
variant
location code
```

dopóki przyszły dataflow tego nie wykaże.

## Success threshold przyszłego runu

Samo:

```text
PUSH 4057
```

NIE wystarczy.

Minimalny sukces semantyczny:

```text
4057 immediate
→ proven template-id consumer
→ template 4057
```

Wyższy sukces:

```text
4057
→ template 4057
→ A=218757
→ concrete construction/resource path
```

Placement breakthrough dopiero:

```text
same proven instance
→ concrete transform producer
→ identity-preserving scene/world path
```

Bez tego:

```text
PLACEMENT_XYZ_RECOVERED = NO
```

---

# 13. FRESH TARGETED QC — ŚWIEŻY KONTEKST

Po wykonaniu F-D1..F-D4 uruchom fresh targeted QC w NOWYM kontekście.

Sesja wykonująca korektę nie certyfikuje sama siebie.

Fresh QC NIE powtarza całego placement experimentu.

Nie robi nowego RE.

Nie bada leadu 4057.

## QC scope

### Q1 — F-D1

Sprawdź wszystkie current-state surfaces.

Wymagane:

```text
active E10 position/transform semantic promotions = 0

E10_OBSERVED_OPERATION = CONFIRMED

E10_FINAL_SEMANTIC_ROLE = UNVERIFIED

E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED

COLOR_VECTOR_HYPOTHESIS =
PLAUSIBLE_ALTERNATIVE_ONLY

WORLD_INSTANCE_EDGE = NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED = NO
```

Historyczne cytaty w supersession/retraction records nie liczą się jako live residue.

### Q2 — F-D2

Zweryfikuj przeciwko istniejącym raw evidence:

```text
registry this = ECX
id2 = stack argument
lookup = registry_this.FUN_0072F580(id2)
```

Sprawdź, że:

```text
record → registry → A
```

pozostało bez zmiany.

### Q3 — F-D3

Zweryfikuj:

```text
correct Win32 locator
exact source identity
POST_AUDIT_SOURCE_CHECK label
MEASURED_DURING_CORRECTION label
no backdating
no fourth oracle
```

### Q4 — F-D4

Zweryfikuj:

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED =
NOT_ESTABLISHED
```

Sprawdź cztery census values:

```text
125
23
109
69
```

wraz z provenance status.

Sprawdź także:

```text
~41 analytical invocations
~14/~27/~10
```

i ich disposition.

Wymagane:

```text
HARD_HISTORICAL_PHASE_LIMIT_BREACH =
NOT_DEMONSTRATED

FULL_HISTORICAL_BUDGET_CONFORMANCE =
NOT_PROVEN
```

### Q5 — CURRENT CORRECTION BUDGET

Sprawdź, że:

```text
CORRECTION_BUDGET
```

został zapisany przed pracą.

Zweryfikuj planned vs used.

Tak samo dla targeted QC.

Jeśli przekroczony:

```text
CORRECTION_RE_QC_FAIL
```

lub uczciwy bounded partial — bez retroaktywnej zmiany limitu.

### Q6 — invariants

Muszą pozostać:

```text
MAIN_RECORD_REQUEST_INDEX_CHAIN = SUPPORTED
RESULT_LEVEL = B
MODEL_ID_RECOVERED = YES

WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
WORLD_INSTANCE_EDGE = NOT_ESTABLISHED
PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED
PLACEMENT_XYZ_RECOVERED = NO

CANONICAL_GATE_EFFECT = NONE
M1_CLOSED = NO
NEXT_EXPERIMENT_AUTHORIZED = NO
```

### Q7 — deferred lead

Sprawdź, że:

```text
4057/218757/0x59AB12
```

został TYLKO zachowany jako unverified future lead.

Fresh QC ma FAIL, jeśli korekta wykonała nowe RE tego tropu lub promowała jego status.

## QC verdict — exact strings

```text
CORRECTION_RE_QC_PASS
```

albo:

```text
CORRECTION_RE_QC_FAIL
```

Każdy finding:

```text
ID
P0/P1/P2/P3
exact path
claim
counter-evidence
blast radius
required disposition
```

---

# 14. FINAL REPORT / REVIEW / HANDOFF

Po PASS targeted QC przygotuj:

```text
03_REPORT/FINAL_REPORT.md
03_REPORT/HANDOFF.md
03_REPORT/FINDING_DISPOSITION.md
```

## FINDING_DISPOSITION

Musi zawierać:

```text
F-D1:
ORIGINAL = P1
DISPOSITION = CORRECTED / NOT_CORRECTED
SCIENCE_EFFECT = ...

F-D2:
ORIGINAL = P2
DISPOSITION = ...

F-D3:
ORIGINAL = P2
DISPOSITION = ...

F-D4:
ORIGINAL = P2
DISPOSITION = ...
```

F-D4 nie wymaga:

```text
QC_BUDGET_PRE_REGISTERED = YES
```

Prawidłowe zamknięcie może być:

```text
CORRECTED_BY_HONEST_PROCESS_RECORD
```

przy zachowaniu:

```text
NOT_ESTABLISHED
NOT_PROVEN
```

---

# 15. AUDIT_ENTRYPOINT — PRZED FINAL MANIFEST

Po finalnych raportach i targeted QC:

dodaj dokładnie jeden factual correction row do `AUDIT_ENTRYPOINT.md`.

Nie modyfikuj historycznych rows.

Correction row musi podać:

```text
CORRECTION_RUN_ID
BASE_SHA = b151d428...
AUDITED_DESKTOP_SHA = b151d428...
Desktop verdict = REQUIRE_CORRECTIONS
scope = F-D1..F-D4
targeted QC verdict
RESULT_LEVEL = B
PLACEMENT_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
pointer to correction FINAL_REPORT
```

Można odnotować:

```text
DEFERRED_LEAD_4057 = RECORDED_NOT_EXECUTED
```

ale nie promować go jako wynik.

`CURRENT STATE` zmieniaj wyłącznie wtedy, gdy kontrakt i fakty wymagają aktualizacji pointera/statusu.

---

# 16. FINAL MANIFEST — MUSI BYĆ LAST

Bezwzględna kolejność:

```text
CORRECTION
→ FRESH TARGETED QC
→ FINAL REPORT
→ REVIEW / DISPOSITION
→ HANDOFF
→ AUDIT_ENTRYPOINT correction row
→ FINAL MANIFEST
→ VERIFY BIJECTION
→ STAGE
→ VERIFY STAGED BLOBS
→ COMMIT
→ PUSH
→ FETCH/REMOTE VERIFY
→ HARD STOP
```

Manifest jest ostatnim generowanym/zmienianym plikiem pakietu przed stagingiem.

## Bijection

Po wygenerowaniu:

```text
MANIFEST_SHA256.csv
```

policz:

```text
PHYSICAL_FILE_COUNT
MANIFEST_ROWS
```

Manifest self-excluded.

Wymagane:

```text
physical package files minus manifest
↔
manifest rows

MISSING = 0
EXTRA = 0
DUPLICATES = 0
SIZE_MISMATCH = 0
SHA256_MISMATCH = 0
```

Wykonaj pełny rehash wszystkich wierszy, nie sample.

## Freeze rule

Jeżeli PO finalnym manifeście zmieni się dowolny covered file:

```text
FINAL MANIFEST IS INVALID
```

Wtedy obowiązkowo:

```text
UNFREEZE
→ REGENERATE MANIFEST
→ REVERIFY FULL BIJECTION
→ RESTAGE
→ REVERIFY STAGED BLOBS
```

Nie commituj starego manifestu.

---

# 17. STAGING

Stage WYŁĄCZNIE:

```text
new correction package
+
AUDIT_ENTRYPOINT.md
```

i tylko inne ścieżki, jeśli correction design jawnie ich wymaga.

Preferowane jest NIE modyfikować historycznego `b151d428` package.

Sprawdź:

```text
git diff --cached --name-only
```

Ustal:

```text
STAGED_PATH_CENSUS
OUTSIDE_SCOPE_PATHS
```

Wymagane:

```text
OUTSIDE_SCOPE_PATHS = 0
```

## Staged blob verification

Nie wystarczy working-tree rehash.

Dla KAŻDEGO manifest row sprawdź:

```text
MANIFEST SHA256
==
SHA256(staged blob bytes)
```

Wymagane:

```text
STAGED_MISSING = 0
STAGED_SIZE_MISMATCH = 0
STAGED_SHA256_MISMATCH = 0
```

Sprawdź również brak unstaged delta dla staged scope.

---

# 18. COMMIT / PUSH

Commit message musi jawnie identyfikować correction run i Desktop findings.

Przykładowo:

```text
PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003:
close Desktop F-D1..F-D4; E10 semantics reverted to UNVERIFIED;
RESULT_LEVEL B unchanged; no XYZ recovered
```

Nie amenduj `b151d428`.

Nie wykonuj force-push.

Po commit:

```text
COMMIT_PARENT
```

musi odpowiadać EXPECTED_BASE_SHA, o ile podczas correction nie pojawił się jawnie obsłużony upstream change.

Jeśli upstream się zmienił:

```text
HARD STOP
```

zamiast automatycznego merge/rebase.

---

# 19. POST-PUSH REMOTE VERIFICATION

Po push:

```text
git fetch
```

Zmierz:

```text
LOCAL_HEAD
FETCHED_ORIGIN_MASTER
LIVE_REMOTE_HEAD
```

Wymagane:

```text
LOCAL_HEAD
==
FETCHED_ORIGIN_MASTER
==
LIVE_REMOTE_HEAD
==
NEW_CORRECTION_SHA
```

Zweryfikuj również:

```text
COMMIT_PATH_CENSUS
==
AUTHORIZED_CORRECTION_SCOPE
```

oraz:

```text
FOREIGN_PATHS = 0
```

---

# 20. FINAL REPORT — REQUIRED FIELDS

`FINAL_REPORT.md` musi zawierać co najmniej:

```text
CORRECTION_RUN_ID =
PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003

AUDITED_DESKTOP_SHA =
b151d428fc46818bc3b84d8ca000d92caa2cd76b

BASE_SHA =
b151d428fc46818bc3b84d8ca000d92caa2cd76b

DESKTOP_POST_AUDIT_VERDICT =
REQUIRE_CORRECTIONS

F_D1_DISPOSITION =
...

F_D2_DISPOSITION =
...

F_D3_DISPOSITION =
...

F_D4_DISPOSITION =
...

NEW_CORRECTION_BUDGET_PREREGISTERED =
YES

CORRECTION_TOOL_CALLS_PLANNED =
80

CORRECTION_TOOL_CALLS_USED =
...

CORRECTION_WALL_MINUTES_PLANNED =
120

CORRECTION_WALL_TIME_USED =
...

TARGETED_QC_TOOL_CALLS_PLANNED =
70

TARGETED_QC_TOOL_CALLS_USED =
...

TARGETED_QC_WALL_MINUTES_PLANNED =
90

TARGETED_QC_WALL_TIME_USED =
...

HISTORICAL_EXECUTOR_INITIAL_TOOL_CALLS =
125 + provenance status

HISTORICAL_EXECUTOR_REPAIR_TOOL_CALLS =
23 + provenance status

HISTORICAL_FRESH_QC_TOOL_CALLS =
109 + provenance status

HISTORICAL_FOCUSED_RE_QC_TOOL_CALLS =
69 + provenance status

HISTORICAL_APPROX_41_ANALYTICAL_INVOCATIONS_STATUS =
...

HISTORICAL_APPROX_14_27_10_STATUS =
...

HISTORICAL_QC_BUDGET_PRE_REGISTERED =
NOT_ESTABLISHED

HARD_HISTORICAL_PHASE_LIMIT_BREACH =
NOT_DEMONSTRATED

FULL_HISTORICAL_BUDGET_CONFORMANCE =
NOT_PROVEN

MAIN_RECORD_REQUEST_INDEX_CHAIN =
SUPPORTED

RESULT_LEVEL =
B

MODEL_ID_RECOVERED =
YES

E10_OBSERVED_OPERATION =
CONFIRMED

E10_FINAL_SEMANTIC_ROLE =
UNVERIFIED

E10_SPATIAL_POSITION_OR_TRANSFORM =
NOT_ESTABLISHED

COLOR_VECTOR_HYPOTHESIS =
PLAUSIBLE_ALTERNATIVE_ONLY

RUNTIME_NIF_OPEN =
NOT_CLOSED

WORLD_INSTANCE_IDENTITY =
NOT_ESTABLISHED

WORLD_INSTANCE_EDGE =
NOT_ESTABLISHED

PERSISTENT_PLACEMENT_EDGE =
NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED =
NO

DEFERRED_LEAD_4057 =
RECORDED_NOT_EXECUTED

IMMEDIATE_4057_IS_TEMPLATE_ID =
UNVERIFIED

HARDCODED_TEMPLATE_REFERENCE_4057 =
UNVERIFIED

PLACEMENT_4057_XYZ =
UNKNOWN

NEXT_4057_EXPERIMENT_AUTHORIZED =
NO

CANONICAL_GATE_EFFECT =
NONE

PE_MASTER_QUALIFICATION_CHANGE =
NO

M1_CLOSED =
NO

M2_AUTHORIZED =
NO

M3_AUTHORIZED =
NO

NEXT_EXPERIMENT_AUTHORIZED =
NO

QC_VERDICT =
CORRECTION_RE_QC_PASS | CORRECTION_RE_QC_FAIL

PHYSICAL_FILE_COUNT =
...

MANIFEST_ROWS =
...

MANIFEST_SHA256 =
...

STAGED_PATH_CENSUS =
...

COMMIT_SHA =
...

COMMIT_PARENT =
...

LOCAL_HEAD =
...

FETCHED_ORIGIN_MASTER =
...

LIVE_REMOTE_HEAD =
...

PUSH_VERIFIED =
YES | NO

HARD_STOP =
YES
```

---

# 21. FINAL DELIVERY NOTICE

Po zakończeniu zwróć do PE-MASTER / HUMAN:

```text
CORRECTION_RUN_ID

BASE_SHA

HEAD_SHA

AUDITED_DESKTOP_SHA

DESKTOP_POST_AUDIT_VERDICT

F-D1 disposition
F-D2 disposition
F-D3 disposition
F-D4 disposition

NEW_CORRECTION_BUDGET:
planned vs used

NEW_TARGETED_QC_BUDGET:
planned vs used

HISTORICAL TOOL-CALL CENSUS:
125 / 23 / 109 / 69
+ provenance classification

HISTORICAL ~41 disposition

HISTORICAL ~14/~27/~10 disposition

HISTORICAL_QC_BUDGET_PRE_REGISTERED

HARD_HISTORICAL_PHASE_LIMIT_BREACH

FULL_HISTORICAL_BUDGET_CONFORMANCE

MAIN_RECORD_REQUEST_INDEX_CHAIN

RESULT_LEVEL

MODEL_ID_RECOVERED

E10_OBSERVED_OPERATION

E10_FINAL_SEMANTIC_ROLE

E10_SPATIAL_POSITION_OR_TRANSFORM

PLACEMENT_XYZ_RECOVERED

WORLD_INSTANCE_IDENTITY

WORLD_INSTANCE_EDGE

PERSISTENT_PLACEMENT_EDGE

DEFERRED_LEAD_4057 status

NEXT_4057_EXPERIMENT_AUTHORIZED=NO

QC_VERDICT

PHYSICAL_FILE_COUNT

MANIFEST_ROWS

MANIFEST_SHA256

STAGED_PATH_CENSUS

COMMIT_PATH_CENSUS

LOCAL_HEAD

FETCHED_ORIGIN_MASTER

LIVE_REMOTE_HEAD

PUSH_VERIFIED

CANONICAL_GATE_EFFECT=NONE

M1_CLOSED=NO

M2_AUTHORIZED=NO

M3_AUTHORIZED=NO

NEXT_EXPERIMENT_AUTHORIZED=NO

HARD_STOP=YES
```

---

# 22. TERMINAL HARD STOP

Po zweryfikowanym pushu:

```text
HARD STOP
```

Nie:

- dispatchuj kolejnego runu;
- nie zaczynaj `4057`;
- nie śledź `0x59AB12`;
- nie wykonuj kolejnego placement experiment;
- nie zamykaj M1;
- nie zmieniaj kwalifikacji;
- nie autoryzuj M2/M3.

Jedyny następny krok:

```text
HUMAN
→ focused Desktop re-audit dokładnego nowego correction SHA
```

Dopiero po focused Desktop PASS i osobnej decyzji człowieka można rozważyć przyszły:

```text
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1
```

z anchor:

```text
0x0059AB12 / candidate immediate 4057
```

i obowiązkowym falsifierem:

```text
NO PROVEN TEMPLATE-ID CONSUMER
→ NUMERIC MATCH REJECTED AS COINCIDENCE
```
<<<END OF VERBATIM TRANSPORT FILE CONTENT — exactly 31,499 bytes; SHA256 7FCFA68E5CCEDB1B65C08C30EB2F9054C6E73AF325E32B8F31F2DE15905D3572; the source file has no trailing newline, so the line break immediately before this marker was added by the assembly and is NOT part of the verbatim block>>>

---

## SCOPE (summary — the order above is authoritative)

### Authorized by this order

1. Corrections F-D1..F-D4 (order sections 4–7):
   - **F-D1 (P1) — E10 semantic retraction:** E10_OBSERVED_OPERATION stays CONFIRMED (templates.vfs list2 → 9 × u32 when the size gate permits → three 3-component groups → interpreted operationally as floats → FUN_006C1F90 component-wise interpolation → three float components written to a runtime slot); E10_FINAL_SEMANTIC_ROLE = UNVERIFIED; E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED; E10_SLOT_CLASS = UNKNOWN; the wording "positions / slot-position / payload-derived position / payload-derived transform / spatial vec3 / world transform" is retracted for E10; COLOR_VECTOR_HYPOTHESIS = PLAUSIBLE_ALTERNATIVE_ONLY (record 11963 falsifier only — no "E10 = COLOR" claim, no color decoders, no new consumer trace); required global statuses after F-D1: WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED, WORLD_INSTANCE_EDGE = NOT_ESTABLISHED, PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED, PLACEMENT_XYZ_RECOVERED = NO; all ACTIVE/current surfaces updated so they no longer propagate the old E10 semantics; explicit supersession statement: "Historical E10 position/transform wording from b151d428 is SUPERSEDED by this correction."
   - **F-D2 (P2) — E2/E3 ABI / input provenance:** correct model is registry_this.FUN_0072F580(id2) with ECX = registry_this and id2 = a stack argument (PUSH EAX of [ESP+0x0C] before CALL FUN_0043A550 registry singleton getter; MOV ECX,EAX); "ECX = id2" as the lookup entry description is retracted; after the lookup, EAX = EDI = template pointer and MOV ECX,EDI → getter A remains correct; MAIN_MAPPING_IMPACT = NONE; ABI_DESCRIPTION_CORRECTED = YES.
   - **F-D3 (P2) — Gamebryo oracle #3 provenance:** the general reference CoreLibs\NiMain\NiAVObject.cpp is not a sufficient implementation locator; the correct Win32 implementation locator is CoreLibs/NiMain/Win32/NiAVObject_Win32.cpp:22; the ONLY permitted new physical measurement for F-D3 is a static source identity verification of that one file/mechanism (exact path, file size, SHA256, exact line/function locator), labeled POST_AUDIT_SOURCE_CHECK = YES and MEASURED_DURING_CORRECTION = YES (no backdating as primary-executor knowledge); HISTORICAL_ORACLE_REFERENCE is separated from POST_AUDIT_SOURCE_VERIFICATION; no new oracle mechanism (ORACLE_MECHANISMS = 3); no Gamebryo inventory, no SDK build, no runtime Gamebryo, no new cross-version searches; target-local evidence from Entropia.exe (NiNode slot27, m_kLocal-shaped +0x38, parent m_kWorld-shaped +0x6C, MOV ECX,13 / REP MOVSD) is NOT downgraded.
   - **F-D4 (P2) — historical budget / process census:** create 01_ANALYSIS/HISTORY_BUDGET_RECONCILIATION.md; preserve historical executor budgets (EXECUTOR_ENUM_BUDGET = PREREGISTERED_MAX_30, EXECUTOR_DEEP_TRACE_BUDGET = PREREGISTERED_MAX_90, EXECUTOR_CONTROLS_ORACLE_BUDGET = PREREGISTERED_MAX_30); HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED and must NOT be changed to YES; session-store census attempt for the four values 125 / 23 / 109 / 69 (executor initial / executor repair / fresh QC / focused re-QC), each recorded with VALUE / SOURCE / SESSION_ID / COUNT_SCOPE / COUNTING_METHOD / INDEPENDENTLY_RECOMPUTED / PROVENANCE_STATUS — if not independently reproducible, record INHERITED_FROM_DESKTOP_POST_AUDIT with the exact source, never a faked measurement; inventory the earlier declarations ~41 analytical invocations and ~14 / ~27 / ~10 (where recorded, what they counted, whether a reproducible counting rule exists, whether they reconcile with the store census — otherwise STATUS = UNVERIFIED / NON_RECONSTRUCTABLE, no after-the-fact denominator); required final statuses: HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED, HISTORICAL_TOOL_CALL_CENSUS = MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE, HARD_HISTORICAL_PHASE_LIMIT_BREACH = NOT_DEMONSTRATED, FULL_HISTORICAL_BUDGET_CONFORMANCE = NOT_PROVEN; F-D4 closes by honest process record + retraction of the full-conformance claim + preservation of NOT_ESTABLISHED — NOT by a retroactive PASS; a total session tool-call count alone does not demonstrate per-phase limit breaches because no historical rule assigned all tool calls to those phases.
2. Necessary current-state supersessions/retractions arising from these findings (order sections 0, 4, 10): the historical b151d428 package text is preserved (no deletion/rewriting of historical evidence); the new correction record explicitly supersedes its current meaning where it propagated the old E10 wording.
3. Bounded post-audit source identity verification for F-D3 ONLY (order section 6).
4. Budget preregistration and measurement of the new correction/QC budgets (order section 3; 00_CONTROL/CORRECTION_BUDGET.md — written BEFORE any correction edit, correction measurement or source verification).
5. Fresh targeted QC in a fresh context (order section 13): scope Q1–Q7 (F-D1 surfaces, F-D2 raw-evidence ABI recheck, F-D3 locator/labels/no-backdating/no-fourth-oracle, F-D4 census values and dispositions, current correction budget planned-vs-used, invariants, deferred lead untouched); QC verdict strings are exactly CORRECTION_RE_QC_PASS or CORRECTION_RE_QC_FAIL; every finding reported with ID / P0-P3 / exact path / claim / counter-evidence / blast radius / required disposition.
6. Final report / review / handoff / disposition records (order sections 10, 14, 20): 03_REPORT/FINAL_REPORT.md, 03_REPORT/HANDOFF.md, 03_REPORT/FINDING_DISPOSITION.md with the full required field set; FINDING_DISPOSITION entries carry ORIGINAL severity + DISPOSITION + SCIENCE_EFFECT (F-D4 does NOT require QC_BUDGET_PRE_REGISTERED = YES; CORRECTED_BY_HONEST_PROCESS_RECORD is a valid closure).
7. Exactly one factual correction row in AUDIT_ENTRYPOINT.md (order section 15; historical rows NOT modified; row carries CORRECTION_RUN_ID, BASE_SHA = b151d428…, AUDITED_DESKTOP_SHA = b151d428…, Desktop verdict = REQUIRE_CORRECTIONS, scope = F-D1..F-D4, targeted QC verdict, RESULT_LEVEL = B, PLACEMENT_XYZ_RECOVERED = NO, CANONICAL_GATE_EFFECT = NONE, NEXT_EXPERIMENT_AUTHORIZED = NO, pointer to the correction FINAL_REPORT; optional DEFERRED_LEAD_4057 = RECORDED_NOT_EXECUTED without promotion).
8. Final manifest generated LAST (order section 16): MANIFEST_SHA256.csv with full bijection verification (physical package files minus manifest ↔ manifest rows; MISSING = 0, EXTRA = 0, DUPLICATES = 0, SIZE_MISMATCH = 0, SHA256_MISMATCH = 0; full rehash of all rows, not a sample; freeze rule with mandatory UNFREEZE → regenerate → reverify → restage → reverify staged blobs if any covered file changes afterwards).
9. Staging + staged-blob verification (order section 17): stage ONLY the new correction package + AUDIT_ENTRYPOINT.md (other paths only if the correction design explicitly requires them; prefer NOT modifying the historical b151d428 package); STAGED_PATH_CENSUS with OUTSIDE_SCOPE_PATHS = 0; for EVERY manifest row, MANIFEST SHA256 == SHA256(staged blob bytes) with STAGED_MISSING = 0, STAGED_SIZE_MISMATCH = 0, STAGED_SHA256_MISMATCH = 0; no unstaged delta for the staged scope.
10. Commit + push (order section 18): commit message explicitly identifies the correction run and Desktop findings; NO amend of b151d428; NO force-push; after commit, COMMIT_PARENT must equal EXPECTED_BASE_SHA — if upstream changed, HARD STOP instead of automatic merge/rebase.
11. Live remote verification (order section 19): LOCAL_HEAD == FETCHED_ORIGIN_MASTER == LIVE_REMOTE_HEAD == NEW_CORRECTION_SHA; COMMIT_PATH_CENSUS == authorized correction scope; FOREIGN_PATHS = 0.
12. Deferred placement lead — RECORD ONLY, DO NOT EXECUTE (order sections 11–12): candidate template id2 = 4057, candidate model A = 218757, candidate collision B = 218758, candidate client immediate VA 0x0059AB12 (PUSH 0x00000FD9 = 4057), nearby immediate 886; the earlier local claims "218757.nif exists in Models.bnt" / "218758.bvi exists in Volumes.bnt" are NOT repinned and NOT promoted (LOCAL_LEAD_TO_BE_REPINNED_IN_FUTURE_AUTHORIZED_RUN); preserved ONLY in 01_ANALYSIS/DEFERRED_PLACEMENT_LEADS.md and in HANDOFF as a candidate future experiment, with the exact epistemic statuses from order section 11 (all UNVERIFIED / UNKNOWN where specified; HUMAN_HISTORICAL_RECOLLECTION is only a test-object selection basis, not evidence); candidate next experiment PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1 recorded as DESIGN ONLY with AUTHORIZATION_STATUS = NOT_AUTHORIZED, its anchor, primary question, mandatory falsifier (no proven template-id consumer → numeric match rejected as coincidence), 12-step future proof ladder, the 886 unknown, and the success thresholds.
13. Order section 8 non-blocking precisions (ONLY where they occur in ACTIVE/current state): A. distinguish DECOMPILATION_RECORDS = 88 from UNIQUE_FUNCTION_ENTRY = 87 (fresh bounded recount of the existing C3_DECOMP.json may confirm; never call it "88 unique functions"; hard limit 120 not shown exceeded); B. do not present the full list1 schema as only count × strings if element 0x20 also covers two further u32 (their status = UNKNOWN; no parser extension in this correction); C. "templates reader = 1 caller" is marked CENSUS_BOUNDED_OBSERVATION, not GLOBAL_PROOF_OF_ONLY_POSSIBLE_READER; no direct file-read in a given construction chain does not prove the data was not previously loaded into memory; keep WORLD_INSTANCE_EDGE = NOT_ESTABLISHED (not "does not exist").

### NOT authorized by this order

- New RE; new Ghidra exploration; client launch; runtime capture; new placement trace.
- Tracing building/template 4057; tracing 0x0059AB12; scanning the family 0x008D–0x008F; XYZ search.
- Q1 (qualification vehicle); PE-MASTER qualification change; M1 closure; M2/M3 authorization; next-experiment authorization (PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1 = NOT_AUTHORIZED during this cycle; NEXT_EXPERIMENT_AUTHORIZED = NO).
- History rewrite; amend of commit b151d428…; force-push; deleting or rewriting historical evidence; promoting any UNKNOWN.
- New color decoders or new consumer traces for E10 (order section 4); Gamebryo inventory, SDK build, runtime Gamebryo, new cross-version searches (order section 6); list1 parser extension (order section 8B); a fourth oracle mechanism (ORACLE_MECHANISMS = 3).
- Backdating post-audit source verification as primary-executor knowledge (order section 6).
- Retroactive change of the historical Desktop verdict for b151d428 (order sections 0, 10); "fixing history" for F-D4 (order section 7).
- During the correction cycle, around the deferred lead: opening Ghidra at 0x0059AB12, decompiling the containing function, tracing callees, scanning 0x008D–0x008F, rescanning the EXE for 4057/218757, searching for XYZ or similar immediates, guessing the meaning of 886, trying to prove 4057 is a template ID, trying to connect 4057 to the registry, trying to connect 218757 to a runtime instance (order section 11).
- After verified push, anything beyond terminal HARD STOP: dispatching another run, starting 4057, tracing 0x59AB12, another placement experiment, closing M1, changing qualification, authorizing M2/M3 (order section 22); the only next step is HUMAN → focused Desktop re-audit of the exact new correction SHA.

## DESKTOP VERDICT HISTORY (IMMUTABLE)

For commit b151d428fc46818bc3b84d8ca000d92caa2cd76b the historical record is:

```text
DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS
SUPPORTED_RESULT_LEVEL = B
CANONICAL_GATE_EFFECT = NONE

OPEN_AT_DESKTOP_AUDIT:
F-D1 = P1
F-D2 = P2
F-D3 = P2
F-D4 = P2
```

- The historical Desktop post-audit verdict for b151d428 is IMMUTABLE. This correction cycle may set finding DISPOSITIONS for the new correction record — permitted closure forms per order section 10: F-D1 = CORRECTED, F-D2 = CORRECTED, F-D3 = CORRECTED, F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD — but it must NOT retroactively change that historical verdict (the new correction commit cannot turn "b151d428 → Desktop verdict = REQUIRE_CORRECTIONS" into a PASS or any other value). History must remain open.
- The earlier historical MASTER_ACCEPTED (advisory) does NOT outrank the later independent Desktop post-audit (order section 1: for b151d428…, DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS governs).
- The historical package docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/ is READ-ONLY for this correction cycle (NEVER MODIFY; no cosmetic changes unless absolutely necessary to establish current state — prefer HISTORICAL ARTIFACT → preserved, NEW CORRECTION RECORD → explicitly supersedes current meaning).

---

AUTHORIZATION.md was composed in PHASE A (formalization + budget preregistration) on 2026-10-03 by pe-master-auditor under PE-MASTER direct dispatch (NO_NESTED_TASKS). The verbatim human order above is the authoritative contract; the summaries in this file are navigation aids only. No correction edit, correction measurement or source verification was performed in PHASE A.
