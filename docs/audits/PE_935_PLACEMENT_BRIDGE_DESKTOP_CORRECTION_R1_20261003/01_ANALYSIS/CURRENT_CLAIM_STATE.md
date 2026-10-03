# CURRENT CLAIM STATE — AUTHORITATIVE CONSOLIDATED BLOCK

```text
RUN_ID = PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003
BASE_SHA = AUDITED_DESKTOP_SHA = b151d428fc46818bc3b84d8ca000d92caa2cd76b
STATUS = CURRENT-STATE SURFACE (supersedes current meaning of historical b151d428 texts)
HISTORICAL TEXTS = PRESERVED as historical artifacts (docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/ — NEVER modified; superseded in current meaning only)
```

This block supersedes the current meaning of the historical b151d428 texts wherever they conflict with it. Historical files remain byte-preserved historical artifacts.

## 1. E10 SUPERSESSION STATEMENT (order §4)

"Historical E10 position/transform wording from b151d428 is SUPERSEDED by this correction."

## 2. E10 — CURRENT STATUS

E10_OBSERVED_OPERATION = CONFIRMED, with the observed-operation chain (order §4, verbatim):

```text
templates.vfs list2
→ 9 × u32 when the size gate permits
→ accessed/copied as three 3-component groups
→ interpreted operationally as floats
→ FUN_006C1F90 performs component-wise interpolation
→ result is written as three float components to a runtime slot
```

Current semantic statuses (exact strings):

```text
E10_OBSERVED_OPERATION = CONFIRMED
E10_FINAL_SEMANTIC_ROLE = UNVERIFIED
E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED
E10_SLOT_CLASS = UNKNOWN
COLOR_VECTOR_HYPOTHESIS = PLAUSIBLE_ALTERNATIVE_ONLY
```

Color-vector context (counter-test for spatial certainty, NOT a claim): the three float groups of record 11963 — (0.0705882, 0.2627450, 0.3529410) / (0.1137250, 0.1137250, 0.1137250) / (0.0000000, 0.5372550, 0.7176470) — are equally consistent with normalized RGB-like values ≈ (18, 67, 90) / (29, 29, 29) / (0, 137, 183). NOT recorded: E10 = COLOR. No color decoders. No new consumer trace.

FORBIDDEN-AS-CURRENT E10 VOCABULARY (do not use as current claims):

```text
positions
slot-position
payload-derived position
payload-derived transform
spatial vec3
world transform
```

## 3. F-D2 ABI — CURRENT STATUS (order §5)

```text
lookup model = registry_this.FUN_0072F580(id2)
ECX = registry_this
id2 = stack argument
```

Corrected physical flow (verbatim):

```text
MOV EAX,[ESP+0x0C]   ; id2
PUSH EAX             ; id2 remains stack argument
CALL FUN_0043A550    ; registry singleton getter
MOV ECX,EAX          ; ECX = registry this
CALL FUN_0072F580    ; lookup(id2)
```

The old wording "ECX = id2" for the lookup entry is RETRACTED (forbidden as current). Post-lookup ECX=EDI → getter A stays correct.

```text
MAIN_MAPPING_IMPACT = NONE
ABI_DESCRIPTION_CORRECTED = YES
```

## 4. F-D3 — CURRENT STATUS (order §6)

```text
HISTORICAL_ORACLE_REFERENCE (superseded locator):
  general "CoreLibs\NiMain\NiAVObject.cpp" (historical ORACLE_RECORDS.md:82-83) — INSUFFICIENT LOCATOR, superseded

POST_AUDIT_SOURCE_VERIFICATION (current locator):
  CoreLibs/NiMain/Win32/NiAVObject_Win32.cpp:22
  EXACT_PATH  = D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\Win32\NiAVObject_Win32.cpp
  FILE_SIZE   = 999 bytes
  SHA256      = 75E452680D4B52D469EC69EF33C79CF94BF0F3E334250B8FAB3892077BF23FD4
  LINE_22     = void NiAVObject::UpdateWorldData()  (sole function of the file; local→world transform propagation:
                 with parent → m_kWorld = m_pkParent->m_kWorld * m_kLocal; else → m_kWorld = m_kLocal;
                 then forwards UpdateWorldData to the collision object)

POST_AUDIT_SOURCE_CHECK = YES
MEASURED_DURING_CORRECTION = YES
  (measured 2026-10-03 by the correction executor, pe-reconstruction — explicitly NOT the historical
   executor's knowledge; no backdating)

ORACLE_MECHANISMS = 3   (UNCHANGED — no fourth mechanism)
```

Target-local evidence (independent observations from Entropia.exe — NOT downgraded, still current):

```text
NiNode slot27
m_kLocal-shaped +0x38
parent m_kWorld-shaped +0x6C
MOV ECX,13
REP MOVSD
```

## 5. F-D4 — FINAL STATUSES (exact strings)

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED
HISTORICAL_TOOL_CALL_CENSUS = MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE
HARD_HISTORICAL_PHASE_LIMIT_BREACH = NOT_DEMONSTRATED
FULL_HISTORICAL_BUDGET_CONFORMANCE = NOT_PROVEN
```

Census provenance summary (full record: 01_ANALYSIS/HISTORY_BUDGET_RECONCILIATION.md): executor initial 125 = INHERITED_FROM_DESKTOP_POST_AUDIT (+ machine sum check 148 = 125+23); executor repair 23 = INHERITED_FROM_DESKTOP_POST_AUDIT (+ same sum check); fresh QC 109 = INDEPENDENTLY_RECOMPUTED, exact match; focused re-QC 69 = INDEPENDENTLY_RECOMPUTED, exact match. A session total alone cannot demonstrate per-phase limit breaches (no historical phase-attribution rule). F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD.

## 6. §8 PRECISIONS — ACTIVE/CURRENT (order §8)

### A. Decompilation counts

```text
DECOMPILATION_RECORDS = 88
UNIQUE_FUNCTION_ENTRY = 87
```

(Both machine-recounted this correction, 2026-10-03: the 88 decompilation records span the historical 01_RAW C*.json set — C2=4, C3=17, C4=12, C5=12, C6=17, C7=12, C8=10, C11=4 — mirrored by the QC decomp_dump's 88 .c files and the QC's own recheck4_decomp_integrity.json {dump_files: 88, match: 88, all_match: true}. Exactly ONE duplicate pair: 006baa20 = C3:R10_other_006baa20 + C6:Y07_consumer_006baa20. Note: 01_RAW/C3_DECOMP.json ALONE contains 17 records / 17 unique — the 88-record census is the run-wide raw record set. It must NOT be phrased as "88 unique functions". Hard limit 120 is NOT demonstrated exceeded.)

### B. list1 schema

The full schema of list1 is NOT merely count × strings — the element at +0x20 covers two further u32. Status of those two fields:

```text
UNKNOWN
```

No parser extension was performed in this correction (and none is authorized in this cycle).

### C. Reader census

```text
templates reader "1 caller" = CENSUS_BOUNDED_OBSERVATION
```

(bounded to the censused machinery — NOT GLOBAL_PROOF_OF_ONLY_POSSIBLE_READER). Absence of a direct file-read in a given construction chain does NOT prove the data was not previously loaded into memory. And:

```text
WORLD_INSTANCE_EDGE = NOT_ESTABLISHED
```

(NOT "WORLD_INSTANCE_EDGE does not exist".)

## 7. MAIN SCIENCE CHAIN + INVARIANTS (order §9 — exact strings)

```text
MAIN_RECORD_REQUEST_INDEX_CHAIN = SUPPORTED
RESULT_LEVEL = B
MODEL_ID_RECOVERED = YES
RUNTIME_NIF_OPEN = NOT_CLOSED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
WORLD_INSTANCE_EDGE = NOT_ESTABLISHED
PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED
PLACEMENT_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
PE_MASTER_QUALIFICATION_CHANGE = NO
M1_CLOSED = NO
M2_AUTHORIZED = NO
M3_AUTHORIZED = NO
NEXT_EXPERIMENT_AUTHORIZED = NO
```

Supported chain (unchanged): physical templates record 4508 → parser → registry → keyed lookup → A @ template+0x08 → request pair {0x66, A=296445}; separately A=296445 ↔ Models.bnt index entry "296445.nif". NOT proven (unchanged): runtime physical open of the NIF; physical record → world-instance identity; world-instance transform; persistent static placement; historical world XYZ.

## 8. E10 ACTIVE-SURFACE CENSUS (measured 2026-10-03T09:21:57Z, BEFORE Phase B writes)

Method: regex `slot-position|slot position|payload-derived|payload derived` over all repo *.md files (582 files scanned, node_modules excluded; PowerShell 5.1 Select-String, case-sensitive AND case-insensitive variants measured). Results (case-sensitive: 24 matching lines / 29 matches; case-insensitive: 25 lines / 30 matches). Classification:

```text
historical package hits (5 files, 15 lines: TRACE_EDGE_BLOCKS.md 7, AMEND_LOG_R1.md 1, DRAFT_FINAL_REPORT.md 4,
  PE_MASTER_REVIEW.md 1, QC_AUDIT_R1.md 2)
  → PRESERVED historical artifacts, superseded by this correction (not live residue)
new correction package 00_CONTROL/AUTHORIZATION.md (4 lines: 393, 394, 395, 2101)
  → QUOTED ORDER TEXT (frozen control plane; verbatim human-order contract, incl. the forbidden-vocabulary list
     and F-D1 scope) — not a semantic promotion
PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914 (3 lines: ENTROPIA_SLOT17_FINGERPRINT.md:167,
  HANDOFF.md:20, REPORT.md:82 — "slot-position alignment")
  → UNRELATED_SENSE (vtable slot alignment)
PE_935_SF_ARG2_PROVENANCE_R1_20260914/06_REPORT/QC_AUDIT.md (2 lines: 260, 265 — "slot positions across its
  10 vtables" / "a single slot position")
  → UNRELATED_SENSE (vtable slot alignment; 2 lines measured vs 1 expected by the dispatch — honest deviation recorded)
PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/00_CONTROL/RUN_CONTRACT.md:105 ("slot POSITION_TO_CALL",
  case-insensitive match only)
  → UNRELATED_SENSE (vtable slot naming)
AUDIT_ENTRYPOINT.md → 0 hits
all other live docs → 0 hits
```

```text
ACTIVE E10 POSITION/TRANSFORM SEMANTIC PROMOTIONS = 0
```

(outside supersession/retraction records; order §13 Q1: historical quotes inside supersession/retraction records do not count as live residue).

## 9. DESKTOP VERDICT HISTORY (IMMUTABLE)

```text
for b151d428: DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS
OPEN_AT_DESKTOP_AUDIT: F-D1 = P1, F-D2 = P2, F-D3 = P2, F-D4 = P2
SUPPORTED_RESULT_LEVEL = B
```

This correction sets dispositions only (F-D1 = CORRECTED, F-D2 = CORRECTED, F-D3 = CORRECTED, F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD) and does NOT retroactively change the historical Desktop verdict for b151d428.
