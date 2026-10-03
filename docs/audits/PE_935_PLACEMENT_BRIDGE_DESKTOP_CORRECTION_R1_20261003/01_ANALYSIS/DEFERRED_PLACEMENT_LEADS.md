# DEFERRED PLACEMENT LEADS — RECORD ONLY, DO NOT EXECUTE

```text
RUN_ID = PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003
ORDER SECTIONS = §11 (deferred placement lead) + §12 (candidate next experiment — DESIGN ONLY, NOT AUTHORIZED)
STATUS = RECORD ONLY. This correction performed NO RE on this lead: no Ghidra was opened around 0x0059AB12,
         no containing function was decompiled, no callee was traced, no 0x008D–0x008F scan, no EXE rescan for
         4057/218757, no XYZ search, no similar-immediate search, no guessing of 886, no attempt to prove 4057 is
         a template ID, no attempt to connect 4057 to the registry, no attempt to connect 218757 to a runtime
         instance. This file is EXCLUSIVELY preservation of the lead.
```

## 1. Delivered local lead (order §11)

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

## 2. Earlier local-analysis claims — NOT repinned, NOT promoted (order §11)

Earlier local analysis also claimed:

```text
218757.nif exists in Models.bnt
218758.bvi exists in Volumes.bnt
```

but because these results are NOT part of the currently published canon of this correction run: do NOT repin them now and do NOT promote them. Recorded as:

```text
LOCAL_LEAD_TO_BE_REPINNED_IN_FUTURE_AUTHORIZED_RUN
```

## 3. Human context (order §11)

The human indicates model `218757` as a potentially very useful probe object, because from historical recollection:

```text
- był charakterystycznym statycznym budynkiem/landmarkiem;
- prawdopodobnie występował tylko w jednej lokalizacji świata.
```

(English: it was a characteristic static building/landmark; it probably occurred in only a single world location.)

This memory:

```text
HUMAN_HISTORICAL_RECOLLECTION
```

is EXCLUSIVELY a basis for choosing a test/probe object. It is NOT evidence of:

```text
instance count = 1
world position
template semantics
hardcoded placement
```

## 4. Current epistemic status (order §11 — exact strings)

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

## 5. Niedozwolone podczas correction cycle (order §11 — VERBATIM do-not-execute guard)

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

## 6. CANDIDATE NEXT EXPERIMENT — DESIGN ONLY, NOT AUTHORIZED (order §12)

```text
CANDIDATE_RUN_TITLE =
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1

AUTHORIZATION_STATUS =
NOT_AUTHORIZED
```

### Anchor

```text
VA 0x0059AB12
candidate raw immediate = 4057
```

### Primary question

```text
What semantic role does immediate 4057 have at this call-site,
and does its dataflow reach the templates registry,
model/resource construction,
or world-instance transform machinery?
```

### Mandatory falsifier

```text
If immediate 4057 does NOT reach FUN_0072F580
or another independently proven template-id consumer,
the numeric equality with templates.vfs id2=4057
must be treated as coincidental and the lead rejected.
```

### Future proof ladder — only after separate human authorization

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

### Separate unknown: immediate 886 (order §12)

```text
IMMEDIATE_886 = OBSERVED_LOCAL_LEAD
FINAL_SEMANTIC_ROLE = UNKNOWN
```

Do NOT guess:

```text
instance ID
zone ID
class
variant
location code
```

until a future dataflow demonstrates it.

### Success thresholds of the future run (order §12)

Alone:

```text
PUSH 4057
```

is NOT sufficient.

Minimal semantic success:

```text
4057 immediate
→ proven template-id consumer
→ template 4057
```

Higher success:

```text
4057
→ template 4057
→ A=218757
→ concrete construction/resource path
```

Placement breakthrough only:

```text
same proven instance
→ concrete transform producer
→ identity-preserving scene/world path
```

Without that:

```text
PLACEMENT_XYZ_RECOVERED = NO
```

## 7. Disposition inside THIS correction cycle

```text
DEFERRED_LEAD_4057 = RECORDED_NOT_EXECUTED
4057/218757/0x59AB12 preserved ONLY as an unverified future lead (order §13 Q7)
NEXT_4057_EXPERIMENT_AUTHORIZED = NO
```

Per order §11, the lead is preserved in this file and is to be carried in HANDOFF as a candidate future experiment (delivered in the Phase B handoff to PE-MASTER; 03_REPORT/HANDOFF.md is outside this phase's authorized output paths).
