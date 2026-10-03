# AUTHORIZATION — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

```text
RUN_ID = PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
BASE_SHA = a4992788982f8ff7f59866fa46aad1176897c69d
DISPATCH_TIME = 2026-10-03 (PE-MASTER preflight verified 2026-10-03)
DISPATCHED_BY = PE-MASTER (loop 18e522c6)
EXECUTOR = pe-reconstruction
NO_NESTED_TASKS = YES (mandatory)
RUN_CLASS = LOAD_BEARING
MODE = STATIC_ONLY
PRIMARY_TARGET = PCG_9_3_5 / Entropia Universe 9.3.5
MILESTONE = EU935-M1 — OPEN
EXPECTED_BASE_SHA = a4992788982f8ff7f59866fa46aad1176897c69d
CANONICAL_GATE_EFFECT = NONE
```

**VERBATIM HUMAN ORDER — FROZEN CONTROL PLANE**

The text between the BEGIN/END markers below is the verbatim human contract as
dispatched by PE-MASTER. It is frozen: no edits, no paraphrase, no backdating.
Section-0 human authorization (Polish original) authorizes exactly ONE bounded
static RE experiment for the local lead (immediate 4057 / VA 0x0059AB12 /
candidate template id2=4057 / candidate model A=218757 / candidate collision
B=218758 / nearby immediate 886), including Ghidra use bounded to this
call-site, raw-byte pinning, call/xref/dataflow analysis, bounded physical
corpus re-pin, bounded Models.bnt/Volumes.bnt index inspection, analysis of
functions directly dependent on 0x0059AB12, fresh independent QC, one
commit+push (persistence phase — SEPARATE, by pe-master-auditor), and a final
manifest/evidence package. It does NOT authorize client launch, dynamic
instrumentation, network capture, runtime packet analysis, wide placement
subsystem sweeps, all-buildings search, automatic map reconstruction, M1
closure, M2/M3, Q1, PE-MASTER qualification changes, another experiment after
this run, history rewrite, force-push, proprietary payload publication,
guessing 886, or accepting 4057 as template ID merely because the number
matches. Pasting this prompt by the human authorizes THIS ONE RUN. After
publication: HARD STOP → ChatGPT/Desktop independent post-audit of exact pushed
SHA → HUMAN decision.

Executor note (outside the frozen text): per the PE-MASTER dispatch supervisory
additions, this executor (science phase) does NOT commit, push, stage, or
create any git state; 04_QC is produced by the fresh QC child; 05_REPORT
contains DRAFT_FINAL_REPORT.md only from this executor; FINAL_REPORT.md,
HANDOFF.md, PE_MASTER_REVIEW.md and MANIFEST_SHA256.csv are persistence-phase
artifacts of pe-master-auditor.

=== BEGIN VERBATIM CONTRACT ===

# PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1

```text
RUN_ID =
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

RUN_TYPE =
BOUNDED_STATIC_LANDMARK_CALLSITE_TRACE

RUN_CLASS =
LOAD_BEARING

PRIMARY_TARGET =
PCG_9_3_5 / Entropia Universe 9.3.5

MILESTONE =
EU935-M1 — OPEN

EXPECTED_BASE_SHA =
a4992788982f8ff7f59866fa46aad1176897c69d

MODE =
STATIC_ONLY

CANONICAL_GATE_EFFECT =
NONE
```

---

# 0. HUMAN AUTHORIZATION

Człowiek AUTORYZUJE dokładnie **JEDEN bounded static RE experiment** dotyczący lokalnego leada:

```text
candidate immediate = 4057
candidate call-site anchor = VA 0x0059AB12
candidate template id2 = 4057
candidate model A = 218757
candidate collision B = 218758
nearby immediate = 886
```

Celem jest ustalenie:

> **jaką semantyczną rolę ma immediate `4057` w kodzie klienta PCG 9.3.5 i czy jego identity-preserving dataflow prowadzi do template registry → model/resource construction → konkretnej runtime instance → transform source?**

To zlecenie AUTORYZUJE:

- statyczną analizę `Entropia.exe`;
- użycie Ghidry dla ograniczonego zakresu tego call-site'u;
- raw-byte pinning;
- call/xref/dataflow analysis;
- bounded inspection lokalnego physical corpus PCG 9.3.5 potrzebnego do re-pinu `4057 → A/B`;
- bounded inspection `Models.bnt` / `Volumes.bnt` indexu;
- analizę niezbędnych funkcji bezpośrednio zależnych od `0x0059AB12`;
- świeży niezależny QC;
- jeden commit + push po zakończeniu;
- finalny manifest i evidence package.

To zlecenie NIE AUTORYZUJE:

- uruchomienia klienta;
- dynamic instrumentation;
- network capture;
- runtime packet analysis;
- szerokiego sweepu całego placement subsystemu;
- szukania wszystkich budynków;
- automatycznej rekonstrukcji mapy;
- M1 closure;
- M2/M3;
- Q1;
- zmiany PE-MASTER qualification;
- kolejnego eksperymentu po tym runie;
- history rewrite;
- force-push;
- publikacji proprietary original payloadów;
- zgadywania znaczenia `886`;
- uznania `4057` za template ID wyłącznie dlatego, że liczba pasuje.

Wklejenie tego promptu przez człowieka jest autoryzacją **tego jednego runu**.

Po publikacji:

```text
HARD STOP
→ ChatGPT/Desktop independent post-audit exact pushed SHA
→ HUMAN decision
```

---

# 1. STAN WEJŚCIOWY — NIE PRZEPISUJ HISTORII

Aktualny canonical repo HEAD przed startem powinien być:

```text
a4992788982f8ff7f59866fa46aad1176897c69d
```

Poprzedni correction cycle ustalił i zachował:

```text
MAIN_RECORD_REQUEST_INDEX_CHAIN = SUPPORTED
RESULT_LEVEL = B
MODEL_ID_RECOVERED = YES

RUNTIME_NIF_OPEN = NOT_CLOSED

WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
WORLD_INSTANCE_EDGE = NOT_ESTABLISHED
PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED
PLACEMENT_XYZ_RECOVERED = NO

E10_OBSERVED_OPERATION = CONFIRMED
E10_FINAL_SEMANTIC_ROLE = UNVERIFIED
E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED

NEXT_EXPERIMENT_AUTHORIZED = NO
```

Ten run jest nową, odrębnie autoryzowaną pracą.

Nie cofaj ani nie zmieniaj correction cycle `a499278`.

---

# 2. DEFERRED LEAD — STARTOWY STATUS EPISTEMICZNY

Poniższe dane są WYŁĄCZNIE leadem wejściowym.

Nie są automatycznie dowodem.

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

Human historical recollection:

```text
model 218757 był charakterystycznym statycznym budynkiem/landmarkiem
i prawdopodobnie występował tylko w jednej lokalizacji świata
```

ma status:

```text
HUMAN_HISTORICAL_RECOLLECTION
```

i służy WYŁĄCZNIE do wyboru dobrego probe object.

Nie jest dowodem:

```text
instance_count = 1
static role
world coordinates
template semantics
hardcoded placement
```

---

# 3. PRIMARY QUESTION

Główne pytanie runu:

```text
What semantic role does immediate 4057 have at/around VA 0x0059AB12,
and does its identity-preserving dataflow reach:

4057
→ independently proven template-id consumer
→ template 4057
→ model/resource A=218757
→ concrete runtime object identity
→ transform producer
→ scene/world insertion?
```

Najważniejsze jest **identity-preserving dataflow**.

Nie wystarczy znaleźć osobno:

```text
4057
218757
XYZ-like floats
NiNode
```

Muszą być połączone tym samym, udowodnionym łańcuchem.

---

# 4. MANDATORY FALSIFIER — NAJWAŻNIEJSZA BRAMKA

Pierwszym celem nie jest potwierdzenie hipotezy.

Pierwszym celem jest możliwość jej ODRZUCENIA.

```text
MANDATORY_FALSIFIER:

If immediate 4057 at/around 0x0059AB12 does NOT reach
FUN_0072F580 or another independently proven template-id consumer,

then:

IMMEDIATE_4057_IS_TEMPLATE_ID = REJECTED_FOR_THIS_CALLSITE
HARDCODED_TEMPLATE_REFERENCE_4057 = NOT_ESTABLISHED
NUMERIC_MATCH_4057 = COINCIDENCE_OR_UNRESOLVED

and the run MUST NOT continue pretending that
0x0059AB12 constructs template 4057.
```

Jeżeli falsifier zadziała, run może zakończyć się wartościowym wynikiem negatywnym.

Nie szukaj wtedy na siłę innego sposobu na „uratowanie" 4057.

---

# 5. BOOT / PREFLIGHT

Przed analizą:

1. `git fetch`
2. zweryfikuj:

```text
HEAD
==
origin/master
==
live remote master
==
a4992788982f8ff7f59866fa46aad1176897c69d
```

3. Jeżeli nie:

```text
HARD_STOP = BASE_MISMATCH
```

4. Sprawdź working tree:
   - brak tracked modifications;
   - brak staged changes;
   - znane obce untracked groups pozostają nietknięte.

5. Zweryfikuj input EXE:

```text
Entropia.exe
size = 8,015,872 B
SHA256 =
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
```

Jeżeli hash/size się nie zgadza:

```text
HARD_STOP = WRONG_TARGET_BUILD
```

6. Odczytaj jako canon/context minimum:

```text
AUDIT_ENTRYPOINT.md

docs/audits/
PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003/
  01_ANALYSIS/CURRENT_CLAIM_STATE.md
  01_ANALYSIS/DEFERRED_PLACEMENT_LEADS.md
  03_REPORT/FINAL_REPORT.md
  03_REPORT/PE_MASTER_REVIEW.md

docs/audits/
PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
  02_ANALYSIS/TRACE_EDGE_BLOCKS.md
  02_ANALYSIS/CLAIM_MATRIX.csv
  05_ORACLE/ORACLE_RECORDS.md
  06_REPORT/FINAL_REPORT.md
```

Poprzednie pakiety są LEADS/CANON CONTEXT zgodnie z ich statusem.

Nie są automatycznie dowodem nowego call-site'u.

---

# 6. NOWY BUDŻET — PREREGISTER BEFORE SCIENCE

Utwórz przed nowym RE:

```text
00_CONTROL/RUN_BUDGET.md
```

Twarde limity:

```text
EXECUTOR_MAX_TOOL_CALLS = 120
EXECUTOR_MAX_WALL_MINUTES = 180

FRESH_QC_MAX_TOOL_CALLS = 80
FRESH_QC_MAX_WALL_MINUTES = 120

QC_REPAIR_ROUNDS_MAX = 1

NEW_PCG_FUNCTIONS_DETAILED_MAX = 60

NEW_PHYSICAL_RECORDS_DETAILED_MAX = 2

NEW_MODEL_RESOURCE_INDEX_RECORDS_MAX = 4

NEW_GAMEBRYO_ORACLE_MECHANISMS_MAX = 0
```

Istniejące Gamebryo/canon można czytać jako kontekst.

Nie rozpoczynaj nowego Gamebryo research.

## Scope expansion forbidden

Jeżeli do odpowiedzi potrzeba >60 nowych funkcji albo zaczynasz śledzić wiele niezależnych subsystemów:

```text
STOP
RESULT = PARTIAL_COVERAGE
```

Nie rozszerzaj limitu po zobaczeniu wyników.

---

# 7. OUTPUT PACKAGE

Utwórz:

```text
docs/audits/
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003/
```

Minimalna struktura:

```text
00_CONTROL/
  AUTHORIZATION.md
  PREFLIGHT.md
  RUN_BUDGET.md
  SELECTION.md

01_RAW/
  RAW_BYTE_PINS.json
  CALLSITE_WINDOW.json
  CALL_XREF_CENSUS.json
  TEMPLATE_4057_PHYSICAL_RECORD.json
  RESOURCE_INDEX_PINS.json

02_ANALYSIS/
  CALLSITE_DATAFLOW.md
  TEMPLATE_ROLE_TEST.md
  OBJECT_IDENTITY_TRACE.md
  TRANSFORM_PROVENANCE.md
  NEGATIVE_CONTROLS.md
  CLAIM_MATRIX.csv
  NOT_CHECKED.md
  RETRACTIONS_SUPERSESSIONS.md

03_SCRIPTS/
  własne bounded reproducible scripts

04_QC/
  TARGETED_QC_REPORT.md
  raw/

05_REPORT/
  DRAFT_FINAL_REPORT.md
  FINAL_REPORT.md
  HANDOFF.md
  PE_MASTER_REVIEW.md

MANIFEST_SHA256.csv
```

Oryginalne payloady:

```text
Entropia.exe
templates.vfs
Models.bnt
Volumes.bnt
NIF/BVI
```

pozostają LOCAL_ONLY.

Do repo trafiają tylko:

- identity metadata;
- hash;
- size;
- offsets;
- bounded byte windows;
- własne scripts;
- reports;
- manifests;
- derived evidence.

---

# 8. PHASE 1 — RE-PIN LEAD BEFORE USING IT

Zanim zbadasz `0x0059AB12`, niezależnie od wcześniejszej rozmowy potwierdź lub odrzuć:

## 8.1 Template 4057

Z fizycznego `templates.vfs`:

```text
record id2 = 4057
```

Zmierz:

```text
physical file identity
record offset
record size
record version
record CRC
payload layout
id2
A
B
C
D raw
list1 count
list2 count
remaining fields
```

Nie przypisuj semantyki D/listom poza istniejącym kanonem.

Wymagany rezultat:

```text
TEMPLATE_4057_REPIN =
CONFIRMED | REJECTED
```

Jeżeli CONFIRMED, dopiero wtedy podaj:

```text
id2 = 4057
A = ?
B = ?
```

Nie dziedzicz automatycznie `218757/218758`.

## 8.2 Model index

Jeżeli A faktycznie = `218757`, sprawdź WYŁĄCZNIE index:

```text
Models.bnt
→ "218757.nif"
```

Nie musisz dekodować całego NIF.

Zapisz:

```text
MODEL_INDEX_218757 =
PRESENT | ABSENT
```

## 8.3 Collision index

Jeżeli B faktycznie = `218758`, sprawdź WYŁĄCZNIE index:

```text
Volumes.bnt
→ "218758.bvi"
```

Zapisz:

```text
COLLISION_INDEX_218758 =
PRESENT | ABSENT
```

Nie rozszerzaj tego do collision semantics.

---

# 9. PHASE 2 — RAW REPIN CALL-SITE 0x0059AB12

Dopiero po Phase 1:

odczytaj fizyczne bajty `Entropia.exe` wokół:

```text
VA 0x0059AB12
```

Zweryfikuj:

```text
instruction boundary
opcode
immediate value
file offset
containing executable section
```

Wymagane:

```text
IMMEDIATE_4057_RAW_PIN =
CONFIRMED | REJECTED
```

Jeżeli instrukcja NIE jest rzeczywiście:

```text
PUSH 0x00000FD9
```

albo `4057` nie jest pełnym immediate tej instrukcji:

```text
HYPOTHESIS_4057_CALLSITE = REJECTED
```

i zakończ science branch.

## Context window

Zachowaj bounded raw window wystarczające do:

- prologu/epilogu containing function;
- wszystkich push/store dotyczących tego immediate;
- bezpośredniego call target;
- warunków branchujących prowadzących do site'u.

Nie skanuj całego EXE „na wszelki wypadek".

---

# 10. PHASE 3 — CONTAINING FUNCTION

Ustal pełną granicę funkcji zawierającej `0x0059AB12`.

Wymagane:

```text
FUNCTION_START
FUNCTION_END
SIZE
CALLERS
CALLEES
calling convention evidence
object/this pointer evidence if present
```

Nie nadawaj funkcji nazwy semantycznej przed dataflow.

Używaj np.:

```text
FUN_XXXXXXXX
```

dopóki rola nie jest dowiedziona.

---

# 11. PHASE 4 — CO DOKŁADNIE OZNACZA PUSH 4057?

To najważniejsza część.

Zidentyfikuj:

```text
PUSH 4057
```

jako:

- który argument?
- do którego CALL?
- czy jest konsumowany bezpośrednio?
- czy kopiowany do local?
- czy przechodzi przez wrapper?
- czy używany jako index/enum/flag/size/value?
- czy zachowuje wartość 4057?

Zbuduj dokładny dataflow:

```text
4057 immediate
→ instruction
→ stack/local/register
→ call argument / store
→ callee
→ use
```

Każdy etap musi mieć:

```text
VA
instruction
raw bytes
source object/value
destination
```

Nie wystarcza decompiler prose.

---

# 12. PHASE 5 — TEMPLATE-ID CONSUMER TEST

Sprawdź, czy ten sam `4057` dochodzi do:

```text
FUN_0072F580
```

w poprawnym ABI:

```text
registry_this.FUN_0072F580(id2)

ECX = registry_this
id2 = stack argument
```

albo do innego consumer'a, którego rola `template id2` zostanie **niezależnie udowodniona**.

## PASS

```text
4057
→ proven template-id consumer
```

wtedy:

```text
IMMEDIATE_4057_IS_TEMPLATE_ID =
CONFIRMED
```

## FAIL

Jeżeli `4057` trafia np. do:

```text
UI enum
effect ID
animation state
array size
message code
resource subtype
unrelated manager
```

albo dataflow urywa się przed jakimkolwiek proven template consumer:

```text
IMMEDIATE_4057_IS_TEMPLATE_ID =
REJECTED_FOR_THIS_CALLSITE
```

Nie kontynuuj wtedy jako „landmark construction path".

---

# 13. PHASE 6 — TEMPLATE → MODEL BRIDGE

Wykonuj TYLKO jeśli Phase 5 PASS.

Udowodnij identity-preserving:

```text
4057 immediate
→ lookup key 4057
→ template object
→ field A @ +0x08
→ measured A
```

Jeżeli measured A = `218757`:

```text
HARDCODED_TEMPLATE_REFERENCE_4057 =
CONFIRMED

IMMEDIATE_4057_TO_MODEL_218757 =
CONFIRMED
```

pod warunkiem zachowania tego samego dataflow.

Nie wystarcza:

```text
4057 exists somewhere
+
218757 exists somewhere
```

---

# 14. PHASE 7 — RESOURCE REQUEST / CONSTRUCTION

Jeżeli 4057→template→A=218757 przejdzie:

śledź WYŁĄCZNIE bezpośredni dalszy path tego samego obiektu/wartości.

Pytania:

```text
Czy A=218757 trafia do:
- {0x66, A} resource request?
- resource manager?
- model provider?
- instance creator?
- visual object constructor?
- wrapper?
```

Rozdziel:

```text
RESOURCE_REFERENCE
RESOURCE_REQUEST
RESOURCE_RESOLUTION
RUNTIME_OPEN
INSTANCE_CREATION
```

Nie łącz ich w jeden claim.

Dopuszczalne statusy:

```text
CONFIRMED
STRONGLY_SUPPORTED
UNVERIFIED
REJECTED
```

---

# 15. PHASE 8 — OBJECT IDENTITY

Najważniejszy krok po resource bridge.

Ustal, czy powstaje lub jest wybierana konkretna runtime object instance.

Wymagaj dowodu:

```text
OBJECT_BASE_POINTER
OBJECT_CLASS / RTTI if available
constructor/factory provenance
template/resource identity
```

Nie wystarczy:

```text
NiNode exists
model exists
function creates something
```

Aby przejść dalej:

```text
SAME_RUNTIME_OBJECT_IDENTITY =
ESTABLISHED
```

musi istnieć zachowany pointer/handle/identity z construction path do transform path.

---

# 16. PHASE 9 — TRANSFORM SOURCE

Tylko jeśli runtime-object identity jest zachowane.

Znajdź pierwszy producer danych transformu TEJ SAMEJ instancji.

Klasyfikuj źródło jako:

```text
HARDCODED_CONSTANT
GLOBAL_STATIC_TABLE
LOCAL_PHYSICAL_FILE
CELL/WORLD_DATA
MESSAGE
RUNTIME_ATTRIBUTE
PARENT_RELATIVE
DERIVED_PROCEDURALLY
UNKNOWN
```

Nie wybieraj kategorii na podstawie wyglądu danych.

## Bardzo ważne — lekcja E10

Trzy floaty NIE oznaczają automatycznie pozycji.

Aby nazwać coś position/translation, wymagaj co najmniej jednego niezależnego semantic discriminatora, np.:

- trafienie do znanego target-local position setter;
- zapis do re-pinned NiTransform translation field;
- use przez target-local transform multiplication jako translation;
- późniejszy use przez world-coordinate consumer;
- niezależny ABI/field-role proof.

Bez tego:

```text
THREE_FLOAT_OPERATION = CONFIRMED
FINAL_SEMANTIC_ROLE = UNVERIFIED
```

---

# 17. PHASE 10 — SCENE / WORLD EDGE

Jeżeli istnieje konkretna instance + transform:

sprawdź, czy ten sam obiekt dochodzi do:

```text
NiAVObject/NiNode scene structure
parent/world transform propagation
scene insertion
world root / cell root
```

Nie używaj samego faktu istnienia `NetImmerseScene::Root` jako dowodu insertion.

Wymagane:

```text
INSTANCE_TO_SCENE_EDGE =
CONFIRMED | STRONGLY_SUPPORTED | NOT_ESTABLISHED
```

---

# 18. PHASE 11 — XYZ RECOVERY

`PLACEMENT_XYZ_RECOVERED = YES` wolno ustawić WYŁĄCZNIE, jeżeli jednocześnie:

```text
1. concrete template/resource identity is proven;

2. concrete runtime instance identity is preserved;

3. transform producer belongs to the SAME instance;

4. three translation components have independently proven spatial semantics;

5. raw/source provenance of values is known;

6. coordinate values are reproducible independently;

7. rotation/orientation is separately classified if claimed.
```

Jeżeli któregokolwiek brakuje:

```text
PLACEMENT_XYZ_RECOVERED = NO
```

Nie używaj:

```text
looks plausible
near known map coordinate
roughly matches memory
```

jako dowodu.

---

# 19. IMMEDIATE 886

`886` pozostaje:

```text
IMMEDIATE_886_SEMANTIC_ROLE = UNKNOWN
```

Możesz ustalić tylko jego mechaniczny dataflow, JEŻELI znajduje się w tej samej funkcji/call sequence i jest konieczny do zrozumienia 4057.

Nie rozpoczynaj osobnego trace 886.

Nie klasyfikuj go jako:

```text
zone id
instance id
location id
class id
variant
```

bez dowodu.

Jeżeli nie jest potrzebny:

```text
886 = NOT_CHECKED_FURTHER
```

---

# 20. NEGATIVE CONTROLS

Run musi zawierać co najmniej następujące kontrole.

## CONTROL-1 — numeric coincidence

Pytanie:

```text
Czy 4057 rzeczywiście dochodzi do template consumer?
```

Failure case:

```text
nie dochodzi
```

→ lead rejected.

## CONTROL-2 — unrelated-immediate control

Sprawdź bounded kontekst call-site'u pod kątem tego, czy inne natychmiastowe liczby podobnej klasy są traktowane jako zwykłe enum/flags/constants.

Cel:

nie nadawać 4057 specjalnej semantyki tylko dlatego, że pasuje do `templates.vfs`.

## CONTROL-3 — identity continuity

Jeżeli po template/resource path przechodzisz do transform:

udowodnij, że to TEN SAM runtime object.

Failure:

```text
different pointer / different instance / generic global transform
```

→ world-instance bridge nieustanowiony.

## CONTROL-4 — spatial semantics

Jeżeli znajdziesz 3 floaty:

spróbuj obalić „position" alternatywą:

```text
color
direction
scale
parameter vector
interpolation coefficients
effect data
```

Tylko target-local consumer może zamknąć semantykę.

## CONTROL-5 — scene insertion

Generic:

```text
NiNode ctor
SetName
UpdateWorldData
```

nie wystarczą.

Musi istnieć identity-preserving edge z badanego obiektu.

---

# 21. LANDMARK TRACE LEVELS

Nie używaj poprzedniego `RESULT_LEVEL=B` jako wyniku tego nowego eksperymentu.

Poprzedni:

```text
PRIOR_PLACEMENT_BRIDGE_RESULT_LEVEL = B
```

pozostaje historycznie bez zmian.

Dla tego runu użyj:

## LANDMARK_LEVEL_0 — FALSIFIED / UNRESOLVED

```text
4057 immediate exists
but template semantics not established
```

lub call-site nie jest związany z template 4057.

## LANDMARK_LEVEL_1 — TEMPLATE BRIDGE

Udowodniono:

```text
0x0059AB12 immediate 4057
→ proven template-id consumer
→ template 4057
→ A=218757
```

ale nie concrete instance.

## LANDMARK_LEVEL_2 — INSTANCE BRIDGE

Poziom 1 +

```text
→ concrete runtime instance identity
```

ale transform producer/world placement niedomknięty.

## LANDMARK_LEVEL_3 — TRANSFORM BRIDGE

Poziom 2 +

```text
→ same-instance transform producer
→ spatial semantics independently established
```

ale scene/world insertion może być jeszcze niepełne.

## LANDMARK_LEVEL_4 — STATIC PLACEMENT BRIDGE

Wymaga:

```text
4057
→ template 4057
→ model 218757
→ concrete static runtime instance
→ concrete spatial transform
→ identity-preserving scene/world edge
→ reproducible XYZ
```

To jest jedyny poziom pozwalający:

```text
PLACEMENT_XYZ_RECOVERED = YES
```

Nie przyznawaj najwyższego osiągniętego levelu „na oko".

Każdy level wymaga wszystkich poprzednich krawędzi.

---

# 22. CLAIM MATRIX — WYMAGANE ROZDZIELENIE

Każdy ważny claim musi mieć osobny wiersz:

```text
CLAIM_ID
CLAIM_TEXT
STATUS
SOURCE
METHOD
INDEPENDENT_COUNTERCHECK
WHY_NON_CIRCULAR
FALSIFIER
FAILURE_CASE_DETECTED
BLAST_RADIUS
```

Minimalne claims:

```text
C4057-01 physical templates record 4057
C4057-02 A/B mapping
C4057-03 model index 218757.nif
C4057-04 collision index 218758.bvi
C4057-05 raw PUSH 4057 @0x0059AB12
C4057-06 containing function
C4057-07 immediate argument/dataflow role
C4057-08 proven/not-proven template consumer
C4057-09 template→A identity continuity
C4057-10 resource request
C4057-11 runtime object identity
C4057-12 transform producer
C4057-13 transform semantic role
C4057-14 scene/world insertion
C4057-15 placement XYZ
C4057-16 immediate 886 role
```

---

# 23. STATUS DISCIPLINE

Stosuj:

```text
CONFIRMED
STRONGLY_SUPPORTED
PLAUSIBLE
UNVERIFIED
REJECTED
```

Rozdziel:

```text
FUNCTION_IDENTITY
OBSERVED_OPERATION
FINAL_SEMANTIC_ROLE
```

Przykład:

```text
function copies 3 floats =
OBSERVED_OPERATION CONFIRMED

those floats are position =
FINAL_SEMANTIC_ROLE UNVERIFIED
```

Nie promuj UNKNOWN przez podobieństwo nazwy, liczby lub struktury.

---

# 24. STOP CONDITIONS

Natychmiast STOP science branch, jeżeli:

### S1

`0x0059AB12` nie zawiera fizycznie immediate `4057`.

### S2

4057 nie dochodzi do proven template consumer.

### S3

template 4057 nie mapuje fizycznie do `A=218757`.

### S4

path rozchodzi się na więcej niż pozwala bounded budget i nie ma dominującego identity-preserving branch.

### S5

osiągnięto tool/function/time budget.

### S6

potrzebny jest runtime/client launch.

Wtedy:

```text
honest bounded result
→ NOT_ESTABLISHED / PARTIAL_COVERAGE
→ HARD STOP
```

Nie rozszerzaj eksperymentu.

---

# 25. FRESH TARGETED QC — ŚWIEŻY KONTEKST

Po science executorze uruchom fresh QC.

[PE-MASTER NOTE: This QC is NOT your work — a separate fresh pe-master-auditor child performs it. You produce the evidence that Q1-Q16 will verify. Design your raw evidence so that each of the following is independently verifiable from bytes, not from your prose: input EXE identity; physical template 4057 record; A/B mapping; 218757.nif/218758.bvi index presence if claimed; raw immediate at 0x0059AB12; containing-function boundaries; exact argument/dataflow role of 4057; whether 4057 truly reaches a proven template consumer (the mandatory falsifier); any claimed 4057→A218757 identity-preserving bridge; object identity if claimed; transform source if claimed; spatial-semantic discriminator if XYZ claimed; scene/world edge if claimed; 886 bounded treatment; budget compliance; no unauthorized client/runtime/network work.]

# 26. QC ANTI-CIRCULARITY

Każdy PASS load-bearing ma podać:

```text
MEASURED_QUANTITY
INDEPENDENT_SOURCE_OF_TRUTH
WHY_NON_CIRCULAR
FAILURE_CASE_DETECTED
```

[PE-MASTER NOTE: apply this to your own raw evidence records too — every load-bearing raw pin must state its measured quantity, the independent source of truth it was derived from, why the check is non-circular, and the failure case it would detect.]

# 27. PE-MASTER FULL AUDIT

[PE-MASTER NOTE: performed by the parent after fresh QC. Not your work. Your DRAFT_FINAL_REPORT.md must answer the 18 questions of contract section 28 explicitly.]

# 28. REPORT — OBOWIĄZKOWE PYTANIA

FINAL_REPORT musi odpowiedzieć osobno:

```text
1. Czy 0x0059AB12 naprawdę zawiera PUSH 4057?

2. Czy ten 4057 jest argumentem do konkretnego calla?

3. Jaka jest jego dokładna rola ABI/dataflow?

4. Czy dochodzi do proven template-id consumer?

5. Czy immediate 4057 jest semantycznie template id?

6. Czy template 4057 fizycznie mapuje się do A=218757?

7. Czy 218757.nif jest obecny w Models.bnt index?

8. Czy B=218758 i 218758.bvi są potwierdzone?

9. Czy ten path wykonuje tylko resource request,
   czy tworzy concrete runtime instance?

10. Jeżeli instance istnieje — jaka jest jej identity?

11. Skąd bierze transform?

12. Czy transform ma independently proven spatial semantics?

13. Czy jest połączony z tą samą instancją?

14. Czy dochodzi do scene/world structure?

15. Czy XYZ zostało odzyskane?

16. Jaka jest rola 886?

17. Jaki LANDMARK_TRACE_LEVEL osiągnięto?

18. Co pozostało UNKNOWN?
```

---

# 29. REQUIRED FINAL STATUS BLOCK

FINAL_REPORT ma zakończyć się blokiem:

```text
RUN_ID =
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

BASE_SHA =
a4992788982f8ff7f59866fa46aad1176897c69d

INPUT_BUILD_SHA256 =
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31

TEMPLATE_4057_REPIN =
CONFIRMED | REJECTED

TEMPLATE_4057_A =
<value | UNKNOWN>

TEMPLATE_4057_B =
<value | UNKNOWN>

MODEL_INDEX_218757 =
PRESENT | ABSENT | NOT_APPLICABLE

COLLISION_INDEX_218758 =
PRESENT | ABSENT | NOT_APPLICABLE

IMMEDIATE_4057_RAW_PIN =
CONFIRMED | REJECTED

IMMEDIATE_4057_AT_0x0059AB12 =
CONFIRMED | REJECTED

IMMEDIATE_4057_IS_TEMPLATE_ID =
CONFIRMED | REJECTED_FOR_THIS_CALLSITE | UNVERIFIED

HARDCODED_TEMPLATE_REFERENCE_4057 =
CONFIRMED | NOT_ESTABLISHED

IMMEDIATE_4057_TO_MODEL_218757 =
CONFIRMED | NOT_ESTABLISHED

MODEL_218757_RESOURCE_REQUEST =
CONFIRMED | STRONGLY_SUPPORTED | NOT_ESTABLISHED

RUNTIME_NIF_OPEN_218757 =
CONFIRMED | STRONGLY_SUPPORTED | NOT_ESTABLISHED

CONCRETE_RUNTIME_INSTANCE =
CONFIRMED | STRONGLY_SUPPORTED | NOT_ESTABLISHED

STATIC_BUILDING_INSTANCE =
CONFIRMED | STRONGLY_SUPPORTED | UNVERIFIED

WORLD_TRANSFORM_SOURCE =
HARDCODED_CONSTANT |
GLOBAL_STATIC_TABLE |
LOCAL_PHYSICAL_FILE |
CELL_WORLD_DATA |
MESSAGE |
RUNTIME_ATTRIBUTE |
PARENT_RELATIVE |
DERIVED_PROCEDURALLY |
UNKNOWN

TRANSFORM_SEMANTIC_ROLE =
CONFIRMED_SPATIAL |
STRONGLY_SUPPORTED_SPATIAL |
UNVERIFIED

INSTANCE_TO_SCENE_EDGE =
CONFIRMED | STRONGLY_SUPPORTED | NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED =
YES | NO

PLACEMENT_X =
<value | UNKNOWN>

PLACEMENT_Y =
<value | UNKNOWN>

PLACEMENT_Z =
<value | UNKNOWN>

ROTATION_RECOVERED =
YES | NO

IMMEDIATE_886_SEMANTIC_ROLE =
<role | UNKNOWN | NOT_CHECKED_FURTHER>

LANDMARK_TRACE_LEVEL =
0 | 1 | 2 | 3 | 4

MANDATORY_FALSIFIER_RESULT =
PASS_TEMPLATE_CONNECTION |
FAIL_NUMERIC_COINCIDENCE |
UNRESOLVED

PRIOR_RESULT_LEVEL =
B (UNCHANGED)

CANONICAL_GATE_EFFECT =
NONE

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

# 30. SUCCESS THEATER PROHIBITED

Niedozwolone przykłady:

```text
"4057 is hardcoded, therefore it is the building"
```

```text
"218757 exists, therefore the call-site loads it"
```

```text
"three floats look like coordinates"
```

```text
"NiNode machinery exists nearby, therefore this object is inserted into scene"
```

```text
"the building existed in one location historically, therefore this is its position"
```

```text
"no position was seen in the scanned window, therefore the client does not know it"
```

Wszystkie takie skróty mają być oznaczone jako:

```text
INVALID_INFERENCE
```

jeśli pojawią się podczas runu.

---

# 31. IMPORTANT NEGATIVE RESULT

Jeżeli run zakończy się:

```text
4057 immediate = unrelated constant
```

to jest PEŁNOPRAWNY wynik.

Final report powinien wtedy powiedzieć:

```text
LANDMARK_TRACE_LEVEL = 0

MANDATORY_FALSIFIER_RESULT =
FAIL_NUMERIC_COINCIDENCE

HARDCODED_TEMPLATE_REFERENCE_4057 =
NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED =
NO
```

Nie szukaj natychmiast innego call-site'u dla 4057.

To byłby osobny przyszły eksperyment.

---

# 32. PERSISTENCE ORDER

Po science + fresh QC + PE-MASTER audit:

```text
SCIENCE
→ FRESH QC
→ PE-MASTER FULL AUDIT
→ FINAL REPORT
→ REVIEW / HANDOFF / CLAIM MATRIX
→ AUDIT_ENTRYPOINT factual row
→ FINAL MANIFEST LAST
→ VERIFY FULL BIJECTION
→ STAGE
→ VERIFY STAGED BLOBS
→ COMMIT
→ PUSH
→ FETCH / LIVE REMOTE VERIFY
→ HARD STOP
```

[PE-MASTER NOTE: Steps from FINAL REPORT onward are the persistence phase — NOT your work. You deliver DRAFT_FINAL_REPORT.md ending with the section-29 status block (filled with your measured values), CLAIM_MATRIX.csv, NOT_CHECKED.md, RETRACTIONS_SUPERSESSIONS.md, and all raw evidence. The persistence phase (executed later by pe-master-auditor) will finalize FINAL_REPORT.md, HANDOFF.md, PE_MASTER_REVIEW.md, the AUDIT_ENTRYPOINT row, MANIFEST_SHA256.csv, the bijection verification, the single commit (parent a499278) and the push.]

Manifest:

```text
physical package files minus manifest
↔ manifest rows
```

Wymagane:

```text
MISSING = 0
EXTRA = 0
DUPLICATES = 0
SIZE_MISMATCH = 0
SHA256_MISMATCH = 0
```

Pełny rehash, nie sampling.

Po stage:

```text
manifest SHA
==
staged blob SHA
```

dla każdego covered file.

---

# 33. AUDIT_ENTRYPOINT

Dodaj jeden factual row.

Nie zmieniaj `CURRENT STATE`, jeśli run nie ma governance effect.

[PE-MASTER NOTE: entrypoint row is persistence-phase work, not yours.]

# 34. COMMIT / PUSH

[PE-MASTER NOTE: persistence-phase work, not yours. You create NO git state.]

# 35. FINAL DELIVERY NOTICE

Finalny handoff ma podać:

```text
RUN_ID
BASE_SHA
HEAD_SHA

INPUT_BUILD_SHA256

EXECUTOR_BUDGET planned/used
QC_BUDGET planned/used

TEMPLATE_4057_REPIN

TEMPLATE_4057_A
TEMPLATE_4057_B

MODEL_INDEX_218757
COLLISION_INDEX_218758

IMMEDIATE_4057_RAW_PIN

CONTAINING_FUNCTION

4057_ARGUMENT_ROLE

IMMEDIATE_4057_IS_TEMPLATE_ID

MANDATORY_FALSIFIER_RESULT

HARDCODED_TEMPLATE_REFERENCE_4057

IMMEDIATE_4057_TO_MODEL_218757

MODEL_RESOURCE_REQUEST_STATUS

RUNTIME_NIF_OPEN_218757

CONCRETE_RUNTIME_INSTANCE

STATIC_BUILDING_INSTANCE

WORLD_TRANSFORM_SOURCE

TRANSFORM_SEMANTIC_ROLE

INSTANCE_TO_SCENE_EDGE

PLACEMENT_XYZ_RECOVERED

PLACEMENT_X
PLACEMENT_Y
PLACEMENT_Z

ROTATION_RECOVERED

IMMEDIATE_886_SEMANTIC_ROLE

LANDMARK_TRACE_LEVEL

QC_VERDICT
PE_MASTER_VERDICT

NOT_CHECKED summary

MANIFEST_ROWS
PHYSICAL_FILE_COUNT
MANIFEST_SHA256

COMMIT_PATH_CENSUS

LOCAL_HEAD
FETCHED_ORIGIN_MASTER
LIVE_REMOTE_HEAD

PUSH_VERIFIED

CANONICAL_GATE_EFFECT = NONE
M1_CLOSED = NO
M2_AUTHORIZED = NO
M3_AUTHORIZED = NO
NEXT_EXPERIMENT_AUTHORIZED = NO

HARD_STOP = YES
```

# 36. TERMINAL HARD STOP

Po pushu:

```text
HARD STOP
```

[PE-MASTER NOTE: the terminal HARD STOP is the parent's terminal condition. For you: when your science phases are complete (or a STOP condition S1-S6 fires), write your draft report + evidence and RETURN to the parent. Do not start any other experiment.]

Jeżeli ten run osiągnie `LANDMARK_TRACE_LEVEL=4`, nadal NIE oznacza automatycznie:

```text
ALL_STATIC_PLACEMENTS_SOLVED
```

Oznacza tylko:

```text
ONE MODEL-SPECIFIC STATIC PLACEMENT BRIDGE
```

=== END VERBATIM CONTRACT ===
