# AUTHORIZATION — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

| Field | Value |
|---|---|
| RUN_ID | PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 |
| RUN_CLASS | LOAD_BEARING (human-declared) |
| RUN_TYPE | GAMEBRYO_TOOLCHAIN_FORENSICS_AND_ORACLE_TOOL_BUILD |
| MODE | **STATIC / LOCAL TOOL EXECUTION ONLY — the game client is NEVER launched; no dynamic instrumentation; no network** |
| PARENT | PE-MASTER supervisory loop `8f0ef23a-964b-4767-ac59-1ec593a1b118` (owner session win32:16328); PE-MASTER direct dispatch; **NO_NESTED_TASKS** (no agent may launch another agent; every worker returns to PE-MASTER) |
| BASE_SHA | `f33c7b9c201b02b8e0f8c7010275b6217475b5a4` (== HEAD == origin/master == live remote; re-verified fail-closed by the formalizer on 2026-10-03, see PREFLIGHT.md) |
| WORKDIR | `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` |
| EXECUTOR | pe-reconstruction |
| FRESH-CONTEXT QC | pe-master-auditor (**a fresh session — NOT the formalizer of this run**; A1.2 separation: the formalizer may not be its own run's internal auditor) |
| PERSISTENCE | pe-master-auditor (separate persistence phase, separately dispatched by PE-MASTER; no git operations before that phase) |
| CONTRIBUTES_TO | EU935-M2, EU935-M3, EU935-M10, EU935-M11 (NO advancement) |
| MILESTONE_ADVANCEMENT | NONE; NEXT_MILESTONE_AUTHORIZED = NO; CANONICAL_GATE_EFFECT = NONE; Q1 absent → **all verdicts ADVISORY_PRE_QUALIFICATION** |

## TRANSFER_NOTE (read before trusting the block below)

The block between the markers below is the human order transferred by PE-MASTER
verbatim from the human message (order-transfer artifact GB_ORACLE_R1_ORDER_TRANSFER.md,
SHA256 86AE80B9F4742A9FA0CC12461BD922657671F443D957369C67B3BE9937859382, 20545 B).
PE-MASTER verified the transfer section-by-section for fidelity before release.
The scientific operationalization (gates/budgets/selection rules) remains normative
in RUN_CONTRACT.md / RUN_BUDGET.md / SELECTION.md / PREFLIGHT.md.

---8<--- HUMAN ORDER VERBATIM ---8<---

# PE_GAMEBRYO_ORACLE_TOOL_R1

```text
RUN_ID =
PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

RUN_TYPE =
GAMEBRYO_TOOLCHAIN_FORENSICS_AND_ORACLE_TOOL_BUILD

RUN_CLASS =
LOAD_BEARING

PRIMARY_TARGET =
PCG_9_3_5 / Entropia Universe 9.3.5

CONTRIBUTES_TO =
EU935-M2
EU935-M3
EU935-M10
EU935-M11

PRIMARY_REPO =
SebastianKozlo/eudoria-clean

DEFAULT_BRANCH =
master

LOCAL_GAMEBRYO_CORPUS =
D:\gamebyroengine

LOCAL_PCG_CORPUS =
D:\Eudoria_Reconstruction\pcg_install

MODE =
STATIC / LOCAL TOOL EXECUTION ONLY

CANONICAL_GATE_EFFECT =
NONE

MILESTONE_ADVANCEMENT =
NONE

NEXT_MILESTONE_AUTHORIZED =
NO
```

---

# 0. HUMAN AUTHORIZATION

Człowiek autoryzuje jeden bounded run mający dwa cele:

1. przeprowadzić forensic inventory lokalnego korpusu Gamebryo:
   `D:\gamebyroengine`;
2. zbudować lokalne narzędzie:

```text
GAMEBRYO_ORACLE_TOOL
```

które pozwoli używać oryginalnych źródeł / narzędzi / loaderów Gamebryo jako niezależnego oracle do analizy NIF-ów PCG 9.3.5.

To NIE jest run placementowy.

Nie wolno w tym runie automatycznie kontynuować do:

```text
- world placement reconstruction;
- EXE-wide scan 218757;
- search for all buildings;
- runtime/network analysis;
- M1 closure;
- M2/M3 advancement;
- Q1;
- gameplay/runtime implementation.
```

Po publikacji:

```text
HARD STOP
→ ChatGPT/Desktop independent post-audit
→ HUMAN decision
```

---

# 1. PRE-FLIGHT — LIVE REPOSITORY FIRST

Zanim zrobisz cokolwiek lokalnie:

```text
git fetch
git rev-parse HEAD
git rev-parse origin/master
git ls-remote origin refs/heads/master
```

Sprawdź live repo:

```text
AUDIT_ENTRYPOINT.md
PROJECT_STATE.json          jeśli istnieje
PROJECT_OPERATING_MODEL.md  jeśli istnieje
```

Nie zakładaj stanu z poprzedniej sesji.

Zapisz:

```text
BASE_SHA
LIVE_MASTER_SHA
WORKTREE_STATE
FOREIGN_UNTRACKED_GROUPS
```

Nie modyfikuj istniejących historycznych runów.

---

# 2. PRIMARY SCIENTIFIC QUESTION

Odpowiedz:

> Jakie oryginalne wersje Gamebryo, źródła, toolsy i loadery rzeczywiście znajdują się w `D:\gamebyroengine`, jakie wersje NIF potrafią czytać i w jaki sposób możemy użyć ich jako niezależnego oracle wobec naszego PCG 9.3.5 parsera?

Najważniejszy wynik ma być praktyczny:

> stworzyć powtarzalne narzędzie, które bierze NIF z lokalnego korpusu PCG 9.3.5 i produkuje audytowalny, machine-readable opis tego, co ORYGINALNY / HISTORYCZNY Gamebryo loader rozpoznaje.

---

# 3. ABSOLUTNA ZASADA: ERA SEPARATION

Nie mieszaj automatycznie wersji Gamebryo.

Każdy source/tool/SDK oznacz:

```text
GAMEBRYO_VERSION
SOURCE_IDENTITY
SOURCE_PATH
FILE_HASH / ARCHIVE_HASH
COMPILER ERA
NIF_VERSION_SUPPORT_EVIDENCE
```

Kategorie:

```text
GB_1_1_2
GB_1_2
GB_2_3
GB_2_6
UNKNOWN_GAMEBRYO
THIRD_PARTY
OUR_TOOL
```

Nigdy nie pisz:

```text
"Gamebryo robi X"
```

jeśli dowód dotyczy tylko jednej konkretnej wersji.

Pisz:

```text
"Gamebryo 2.6 source X does Y"
```

albo:

```text
"GB 1.2 implementation observed operation = ..."
```

---

# 4. PHASE A — FORENSIC INVENTORY `D:\gamebyroengine`

Zrób pełne, read-only inventory.

Nie rozpakowuj bez potrzeby całych archiwów do repo.

Dla każdego:

```text
directory
ISO
7z
source tree
tool project
prebuilt executable
library
documentation
sample
```

zapisz:

```text
relative/local path
size
SHA256
probable version
evidence for version
source/binary/docs classification
```

Szczególnie znajdź i zinwentaryzuj:

```text
SceneViewer
NifViewer
SceneGraphPrinter
NifConvert
AnimationTool
DeveloperTools
NiStream
NiBinaryStream
NiObject
NiObjectNET
NiAVObject
NiNode
NiGeometry
NiGeometryData
NiTexturingProperty
NiSourceTexture
NiPixelData
NiTimeController
NiControllerSequence
NiKeyframeController
NiTransformController
NiBound
NiBoxBV
NiSphereBV
NiMain
```

oraz wszystkie:

```text
LoadBinary
SaveBinary
RegisterLoader
RegisterStreamables
CreateObject
LinkObject
PostLinkObject
Load
Link
Stream
Read
```

---

# 5. PHASE B — VERSION SUPPORT: NIE ZGADUJ

Dla każdej wersji Gamebryo ustal:

```text
MIN_NIF_VERSION_SUPPORTED
MAX_NIF_VERSION_SUPPORTED
SUPPORTED VERSION TABLE
VERSION COMPARISON LOGIC
FAILURE BEHAVIOR
```

Źródła dowodu, w kolejności:

```text
1. original Gamebryo source
2. original Gamebryo tool source
3. original Gamebryo docs
4. actual loader execution against controlled test files
5. third-party docs only as context
```

Nie uznawaj:

```text
"GB 2.6 should support 10.1"
```

za dowód.

Ma być:

```text
SUPPORTED
REJECTED
PARTIAL
UNKNOWN
```

z physical evidence.

---

# 6. PHASE C — IDENTIFY ORIGINAL NIF LOAD PIPELINE

Zrekonstruuj z source dokładny pipeline:

```text
NIF bytes
→ header/version
→ object type string / type id
→ factory registration
→ object allocation
→ LoadBinary
→ link phase
→ PostLink
→ runtime scene graph
```

Dla każdego kroku wskaż:

```text
class
function
source file
line number
version
```

Jeżeli mechanizm różni się między 1.x i 2.x, pokaż różnicę.

Docelowo chcemy mapę:

```text
ORIGINAL BYTE
→ GAMEBRYO LOADER
→ RUNTIME FIELD
→ RUNTIME OBJECT
→ CONSUMER
```

To jest nowy GAMEBRYO ROSETTA oracle.

---

# 7. PHASE D — ZBUDUJ `GAMEBRYO_ORACLE_TOOL`

Stwórz nasze własne narzędzie/wrapper.

Preferowana architektura:

```text
tools/gamebryo_oracle/
```

ale przed dodaniem sprawdź strukturę repo i dostosuj się do istniejącej konwencji.

Tool musi być:

```text
LOCAL_FIRST
READ_ONLY względem original assets
DETERMINISTIC
FAIL_CLOSED
MACHINE_READABLE
CLI
```

Przykładowy interfejs:

```text
gamebryo-oracle inspect <path-to-nif>

gamebryo-oracle compare <path-to-nif> \
    --our-parser <our-output>

gamebryo-oracle capabilities

gamebryo-oracle probe-version <path-to-nif>
```

Jeżeli technicznie lepiej zrobić kilka wrapperów, jest to dozwolone, ale jeden nadrzędny entrypoint jest wymagany.

---

# 8. MINIMALNY OUTPUT `inspect`

Tool MUSI generować JSON.

Minimum:

```json
{
  "input_identity": {
    "size": "...",
    "sha256": "...",
    "header": "...",
    "nif_version": "..."
  },

  "oracle": {
    "gamebryo_version": "...",
    "loader_identity": "...",
    "loader_source_identity": "...",
    "tool_version": "..."
  },

  "load_result": {
    "accepted": true,
    "partial": false,
    "error": null
  },

  "objects": [],
  "scene_graph": {},
  "type_histogram": {},
  "controllers": [],
  "properties": [],
  "textures": [],
  "bounds": [],
  "warnings": [],
  "unknowns": []
}
```

---

# 9. OBJECT-LEVEL OUTPUT

Dla każdego obiektu, jeśli Gamebryo to udostępnia:

```text
stream index
runtime class
RTTI class
name
parent
children
local translation
local rotation
local scale
world translation
world rotation
world scale
bounding volume
properties
controllers
references
```

Rozdziel:

```text
SERIALIZED_LOCAL_TRANSFORM
COMPUTED_WORLD_TRANSFORM
```

Nie nazywaj `computed world transform` pozycją w Eudorii bez dowodu.

---

# 10. CRITICAL WORLD-PLACEMENT SAFETY RULE

Dla każdego NIF-a klasyfikuj najwyższy scene-graph level:

```text
MODEL_LOCAL
MULTI_OBJECT_LOCAL_SCENE
CELL_LIKE
WORLD_LIKE
UNKNOWN
```

Nie wolno automatycznie zakładać:

```text
root transform = world placement
```

Dla `218757.nif` odpowiedz jawnie:

```text
IS_ROOT_TRANSFORM_ZERO?
IS_ROOT_TRANSFORM_NONZERO?
DOES_FILE_CONTAIN_PARENT ABOVE BUILDING?
DO_NODE_NAMES_SUGGEST_CELL/WORLD CONTEXT?
IS_THIS CLEARLY A STANDALONE ASSET?
```

Statusy:

```text
CONFIRMED
STRONGLY_SUPPORTED
PLAUSIBLE
UNVERIFIED
REJECTED
```

---

# 11. ORIGINAL VS OUR DECODER — COMPARISON MODE

Najważniejsza funkcja toola:

```text
ORIGINAL/HISTORICAL GAMEBRYO OUTPUT
vs
OUR CURRENT NIF DECODER OUTPUT
```

Porównaj minimum:

```text
block count
object count
type histogram
object ordering
names
parent-child edges
local transforms
world transforms
geometry count
vertex counts
triangle counts
UV sets
normals
bounding volumes
controllers
properties
texture references
unknown blocks
parse failures
```

Output:

```text
MATCH
MISMATCH
NOT_AVAILABLE_IN_ORACLE
NOT_AVAILABLE_IN_OUR_DECODER
SEMANTICALLY_UNRESOLVED
```

Nie wymuszaj fake equality dla reprezentacji float.

Zdefiniuj tolerancję tylko tam, gdzie jest potrzebna, i jawnie ją zapisz.

---

# 12. TEST CORPUS

Nie zaczynaj tylko od `218757.nif`.

Wybierz mały, prerejestrowany corpus:

```text
T1 = 218757.nif
T2 = representative PCG 9.3.5 NIF 10.1.0.0
T3 = second structurally different NIF 10.1.0.0
T4 = representative NIF 4.1.0.12
T5 = minimal/simple NIF if one exists
```

Selection musi nastąpić PRZED wynikami.

Nie wybieraj plików po tym, które najładniej przechodzą.

Dla każdego zapisz:

```text
source container
asset name/id
SHA256 extracted local copy
NIF version
selection reason
```

Original payload pozostaje LOCAL_ONLY.

---

# 13. TEST `218757.nif`

To jest ważny probe-object, ale NIE pozwól, żeby zdominował science.

Dla `218757.nif` chcemy:

```text
LOAD SUCCESS / FAIL
NIF VERSION
ROOT CLASS
OBJECT COUNT
NODE COUNT
GEOMETRY COUNT
MESH COUNT
TYPE HISTOGRAM
NODE NAMES
ROOT LOCAL TRANSFORM
ALL NONZERO NODE TRANSLATIONS
BOUNDING BOX / BOUNDING SPHERE
APPROX DIMENSIONS
CONTROLLERS
TEXTURE REFERENCES
CUSTOM/UNKNOWN TYPES
```

Odpowiedz:

> Czy z samego NIF-a da się powiedzieć coś więcej niż „asset budynku"?

oraz:

> Czy w pliku jest jakikolwiek evidence wskazujący na world/cell placement?

Dozwolony wynik:

```text
NO WORLD PLACEMENT EVIDENCE FOUND
```

Nie jest to porażka.

---

# 14. GAMEBRYO SOURCE AS RE ORACLE

To jest bardzo ważna część runu.

Zbuduj katalog semantycznych oracle signatures dla:

```text
NiAVObject::SetTranslate
NiAVObject::SetRotate
NiAVObject::SetScale
NiAVObject::UpdateWorldData
NiNode::AttachChild
NiNode::DetachChild
NiNode::SetAt
NiStream load/link/postlink
```

Dla każdej:

```text
GAMEBRYO_VERSION
SOURCE FILE
SOURCE LINE
FUNCTION CONTRACT
INPUT
OUTPUT
STATE MUTATED
CALLING SHAPE
IMPORTANT OFFSETS if determinable
```

Jeżeli masz historyczną bibliotekę/binary i możesz bezpiecznie skorelować source z kodem:

```text
SOURCE
→ COMPILED FUNCTION
→ MACHINE SHAPE
```

zrób to.

ALE:

Nie próbuj jeszcze automatycznie dopasowywać całego `Entropia.exe`.

Do repo trafia oracle/signature knowledge, nie szeroki nowy RE placementu.

---

# 15. BOUNDING VOLUME / DIMENSIONS

Sprawdź oryginalne Gamebryo semantics:

```text
NiBound
NiBoundingVolume
NiBoxBV
NiSphereBV
```

Ustal:

```text
czy bound jest serializowany;
czy jest recomputed;
na którym etapie;
w jakim układzie współrzędnych;
czy root bound reprezentuje cały asset.
```

Dopiero potem raportuj wymiary `218757.nif`.

Nie przeliczaj automatycznie jednostek na metry bez dowodu.

Raportuj:

```text
GAME_UNITS
```

dopóki skala świata nie jest CONFIRMED.

---

# 16. COMPATIBILITY MATRIX

Finalny artifact:

```text
GAMEBRYO_COMPATIBILITY_MATRIX.csv
```

Przykład:

```text
GB_VERSION
TOOL
SOURCE_AVAILABLE
BUILDS
RUNS
NIF_4_1_0_12
NIF_10_1_0_0
CUSTOM_ARK_BLOCKS
SCENE_GRAPH
TRANSFORMS
BOUNDS
CONTROLLERS
TEXTURES
NOTES
```

Każde pole:

```text
PASS
PARTIAL
FAIL
NOT_TESTED
UNKNOWN
```

---

# 17. FAIL-CLOSED REQUIREMENTS

Tool nie może powiedzieć:

```text
success
```

jeżeli silently skipped unknown classes.

Musisz wykrywać:

```text
unknown type
missing factory
unsupported block
link failure
PostLink failure
partial scene
exception
object-count mismatch
```

Jeśli loader otworzy plik, ale pominie część obiektów:

```text
LOAD_RESULT = PARTIAL
```

nie PASS.

---

# 18. POSITIVE AND NEGATIVE CONTROLS

Każdy kluczowy PASS musi mieć:

```text
MEASURED_QUANTITY
INDEPENDENT_SOURCE_OF_TRUTH
WHY_NON_CIRCULAR
FAILURE_CASE_DETECTED
```

Minimum:

### Positive control

NIF znany jako kompatybilny z danym historycznym toolchainem musi przejść.

### Wrong-version negative control

NIF o wersji poza deklarowanym zakresem musi zostać:

```text
REJECTED
```

lub jawnie oznaczony jako:

```text
UNSUPPORTED
```

### Corrupted-file negative control

Na kopii testowej zmień lokalnie kilka krytycznych bajtów/header version.

Tool musi FAIL.

### Unknown-class control

Jeśli można stworzyć syntetyczny lub zmodyfikowany test z niezarejestrowanym typem:

Tool musi zgłosić unknown class, nie silent PASS.

Nie publikuj zmodyfikowanego proprietary payloadu.

---

# 19. SCENEGRAPH PRINTER

Jeżeli oryginalny `SceneGraphPrinter` można zbudować lub uruchomić:

użyj go jako niezależnego oracle.

Nie patchuj go na początku.

Najpierw:

```text
ORIGINAL UNMODIFIED TOOL RESULT
```

Potem dopiero ewentualnie wrapper.

Zachowaj lokalnie:

```text
stdout
stderr
exit code
tool SHA256
input SHA256
```

Nasz wrapper może przeparsować jego output do JSON.

Jeżeli nie da się go zbudować:

ustal dokładną przyczynę:

```text
compiler incompatibility
missing SDK
missing library
missing platform target
source incompatibility
```

Nie pisz po prostu „tool broken".

---

# 20. SCENEVIEWER / NIFVIEWER

Są wtórne wobec machine-readable oracle.

Jeśli działają:

dla małego corpusu zrób:

```text
LOAD RESULT
runtime object count if accessible
warnings/errors
visual screenshot LOCAL evidence
```

Screenshot nie jest źródłem prawdy dla parser semantics.

„Looks correct" ≠ PASS.

---

# 21. NIFCONVERT

Nie używaj converted NIF jako dowodu o oryginalnych bytes.

Jeśli NifConvert będzie testowany:

```text
ORIGINAL
→ CONVERTER
→ DERIVATIVE
```

Derivative oznacz:

```text
GENERATED_DIAGNOSTIC_ARTIFACT
```

Nigdy:

```text
RECOVERED_ORIGINAL
```

---

# 22. TOOL IMPLEMENTATION POLICY

Do repo można dodać wyłącznie:

```text
nasz wrapper
nasze parsery
nasze build scripts
nasze test harnesses
naszą dokumentację
nasze JSON schema
nasze tests
hash/provenance manifests
```

Nie pushuj:

```text
Gamebryo proprietary source
Gamebryo ISO
Gamebryo libs/binaries
Entropia original NIF
Entropia.exe
BNT/VFS original payload
screenshots zawierających proprietary assety, jeśli repo policy tego nie dopuszcza
```

External/original dependencies reprezentuj przez:

```text
LOCAL_PATH_DESCRIPTION
VERSION
SIZE
SHA256
REPRODUCTION_METHOD
```

---

# 23. PROPOSED TOOL STRUCTURE

Jeżeli pasuje do repo:

```text
tools/gamebryo_oracle/
    README.md
    oracle.py / oracle.ps1 / suitable launcher
    schemas/
        oracle_result.schema.json
        comparison_result.schema.json
    adapters/
        gb112/
        gb12/
        gb23/
        gb26/
    compare/
        compare_scene_graph.py
    tests/
        ...
```

Adapters nie mogą zawierać proprietary source.

Mogą zawierać:

```text
build instructions
local path discovery
command invocation
output parser
hash verification
```

---

# 24. OUTPUT ARTIFACTS

Stwórz run package, np.:

```text
docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/
```

Minimum:

```text
00_CONTROL/
    AUTHORIZATION.md
    PREFLIGHT.md
    SELECTION.md
    RUN_BUDGET.md

01_INVENTORY/
    GAMEBRYO_CORPUS_INVENTORY.csv
    TOOLCHAIN_MATRIX.csv
    SOURCE_ORACLE_INDEX.csv

02_ANALYSIS/
    NIF_LOAD_PIPELINE.md
    VERSION_SUPPORT.md
    GAMEBRYO_ROSETTA.md
    TRANSFORM_SEMANTICS.md
    BOUNDING_VOLUME_SEMANTICS.md
    218757_NIF_RESULT.md
    NOT_CHECKED.md
    RETRACTIONS_SUPERSESSIONS.md

03_TOOL/
    TOOL_IMPLEMENTATION_REPORT.md
    TEST_MATRIX.csv
    FAIL_CLOSED_TESTS.md

04_EVIDENCE/
    machine-readable generated metadata
    hashes
    outputs
    comparison summaries

05_QC/
    independent QC
    raw QC outputs

06_REPORT/
    FINAL_REPORT.md
    HANDOFF.md
    PE_MASTER_REVIEW.md

MANIFEST_SHA256.csv
```

---

# 25. REQUIRED FINAL QUESTIONS

FINAL_REPORT musi odpowiedzieć osobno:

1. Jakie wersje Gamebryo fizycznie posiadamy?
2. Jakie wersje posiadają source?
3. Jakie oryginalne narzędzia fizycznie posiadamy?
4. Które można zbudować?
5. Które można uruchomić?
6. Które potrafią czytać NIF 4.1.0.12?
7. Które potrafią czytać NIF 10.1.0.0?
8. Czy odczyt 10.1 jest FULL czy PARTIAL?
9. Jak original Gamebryo streamuje NIF?
10. Jak działa object factory?
11. Jak działa link/PostLink?
12. Jak przechowywana jest local transform?
13. Jak wyliczana jest world transform?
14. Jak działa AttachChild?
15. Jak działa bounding volume?
16. Czy zbudowano GAMEBRYO_ORACLE_TOOL?
17. Czy tool działa deterministycznie?
18. Czy jest fail-closed?
19. Czy `218757.nif` został poprawnie odczytany?
20. Jak wygląda jego scene graph?
21. Jakie ma wymiary w GAME_UNITS?
22. Czy zawiera world/cell placement evidence?
23. Czy wynik oryginalnego Gamebryo zgadza się z naszym parserem?
24. Jakie różnice znaleziono?
25. Które nasze dotychczasowe NIF assumptions mogą zostać podniesione/obniżone?
26. Co pozostaje UNKNOWN?
27. Jakie nowe Rosetta edges uzyskaliśmy?
28. Czy powstało cokolwiek, co realnie pomoże przyszłemu placement RE?
29. Czy jakikolwiek proprietary payload/source trafił do repo?
30. Czy milestone/governance pozostały bez zmian?

---

# 26. CLAIM DISCIPLINE

Rozdziel:

```text
FUNCTION_IDENTITY
OBSERVED_OPERATION
FINAL_SEMANTIC_ROLE
```

oraz:

```text
CLIENT_KNOWLEDGE_COVERAGE
RECONSTRUCTION_IMPLEMENTATION_COVERAGE
HISTORICAL_GAME_RECOVERY_COVERAGE
```

Original Gamebryo source może CONFIRM:

```text
engine semantics
NIF field semantics
runtime structure
transform algorithm
```

ale NIE może sam CONFIRM:

```text
MindArk placement source
historical world coordinates
server-sent values
Ark custom semantics
```

bez osobnego dowodu.

---

# 27. IMPORTANT ANTI-OVERCLAIM

Nie wolno uznać:

```text
Gamebryo root transform
=
Eudoria world position
```

bez independent evidence.

Nie wolno uznać:

```text
SceneViewer successfully rendered
=
our parser fully correct
```

Nie wolno uznać:

```text
loader accepted file
=
all objects understood
```

Nie wolno uznać:

```text
source exists
=
Entropia uses that exact implementation
```

chyba że zostanie ustanowiona FUNCTION_IDENTITY / build correspondence.

---

# 28. OPTIONAL HIGH-VALUE RESULT

Jeśli w bounded scope da się bez rozszerzania misji przygotować historyczne semantic signatures:

```text
NiAVObject::SetTranslate
NiAVObject::UpdateWorldData
NiNode::AttachChild
```

to wygeneruj osobny:

```text
GAMEBRYO_SEMANTIC_SIGNATURES.json
```

z:

```text
version
source identity
function contract
relevant structure offsets
compiled signature if independently established
confidence
```

Ale NIE rozpoczynaj jeszcze EXE-wide Entropia matching.

To będzie materiał dla przyszłego osobno autoryzowanego runu.

---

# 29. FRESH QC

Po implementacji uruchom fresh independent QC.

QC musi przynajmniej:

- niezależnie sprawdzić hashes toolchainów;
- niezależnie potwierdzić wersję NIF test corpusu;
- re-run minimum 3 testów oracle;
- porównać raw Gamebryo output z wrapper JSON;
- przeprowadzić corrupted-input negative control;
- sprawdzić unknown/unsupported fail-closed behavior;
- sprawdzić, że żadnego proprietary source/payload nie ma w staged files;
- sprawdzić deterministic repeatability.

Jeśli tool silently pomija obiekty:

```text
QC_FAIL
```

dopóki wynik nie zostanie oznaczony PARTIAL.

---

# 30. PERSISTENCE

Po science + fresh QC + PE-MASTER review:

```text
FINAL REPORT
→ HANDOFF
→ AUDIT_ENTRYPOINT factual row
→ MANIFEST LAST
→ VERIFY BIJECTION
→ STAGE
→ VERIFY STAGED STATE
→ ONE COMMIT
→ PUSH
```

Bez force push.

Po push:

```text
HEAD
origin/master
live remote
```

muszą być identyczne.

---

# 31. TERMINAL

Po publikacji:

```text
GAMEBRYO_ORACLE_TOOL_BUILT =
YES / PARTIAL / NO

GB_NIF_10_1_SUPPORT =
CONFIRMED / PARTIAL / REJECTED / UNKNOWN

218757_ORACLE_RESULT =
...

WORLD_PLACEMENT_RECOVERED =
NO
```

Ostatnie pole pozostaje `NO`, chyba że w samym NIF-ie pojawi się jednoznaczny, niezależnie zweryfikowany world/cell placement record. Nie promuj zwykłego local transform.

Następnie:

```text
HARD STOP
NEXT_EXPERIMENT_AUTHORIZED = NO
→ ChatGPT/Desktop independent post-audit exact pushed SHA
→ HUMAN strategic decision
```

Nie rozpoczynaj automatycznie:

```text
218757 EXE scan
placement tracing
Ark insertion-edge RE
```

nawet jeśli tool ujawni ciekawy lead.

---8<--- END HUMAN ORDER ---8<---

## AUTHORIZATION RECORD (formalizer)

- This file was created by the pe-master-auditor FORMALIZER-1 worker under
  direct PE-MASTER dispatch (loop `8f0ef23a-964b-4767-ac59-1ec593a1b118`,
  checkpoint phase FORMALIZE, iteration 1). The formalizer did NO science,
  NO corpus analysis, NO tool building and NO git mutations.
- The human authorization quote in section 0 is byte-exact from
  `PE_MASTER_LOOP_STATE.json` (`authorization_quote`, revision 2,
  SHA256 93DE11B540F8C8F485C7278C63045EE3299E886CA7DDE4B2A38030A55DA347BC).
- The order text block between the markers is the PE-MASTER-verified
  verbatim transfer of the human order (order-transfer artifact SHA256
  86AE80B9F4742A9FA0CC12461BD922657671F443D957369C67B3BE9937859382,
  20545 B).
