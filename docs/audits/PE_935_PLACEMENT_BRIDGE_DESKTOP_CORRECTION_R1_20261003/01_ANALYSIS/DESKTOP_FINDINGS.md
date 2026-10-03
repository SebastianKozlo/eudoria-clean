# DESKTOP FINDINGS — CORRECTION OF F-D1..F-D4

```text
RUN_ID = PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003
RUN_TYPE = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION
RUN_CLASS = LOAD_BEARING
PHASE = B (CORRECTIONS)
EXECUTOR = pe-reconstruction (direct PE-MASTER dispatch; NO_NESTED_TASKS)
BASE_SHA = b151d428fc46818bc3b84d8ca000d92caa2cd76b
AUDITED_DESKTOP_SHA = b151d428fc46818bc3b84d8ca000d92caa2cd76b
MODE = STATIC_ONLY
MEASURED = 2026-10-03 (UTC)
CANONICAL_GATE_EFFECT = NONE
```

## DESKTOP VERDICT HISTORY (IMMUTABLE — this correction does not change it)

```text
for b151d428: DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS
OPEN_AT_DESKTOP_AUDIT: F-D1 = P1, F-D2 = P2, F-D3 = P2, F-D4 = P2
SUPPORTED_RESULT_LEVEL = B
```

This package sets FINDING DISPOSITIONS only (per order §10): F-D1 = CORRECTED, F-D2 = CORRECTED, F-D3 = CORRECTED, F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD. It must NOT retroactively change the historical Desktop verdict for b151d428. No historical file was modified: every historical wording below is QUOTED (preserved) and SUPERSEDED by new current-state records, never edited.

## CONFIRMED MAIN SCOPE (order §0 — unchanged by all four corrections)

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

## NOT PROVEN (order §0 — unchanged)

```text
runtime physical open of the NIF
physical record → world-instance identity
world-instance transform
persistent static placement
historical world XYZ
```

---

## F-D1 — ORIGINAL SEVERITY P1 — E10 SEMANTIC RETRACTION

### What Desktop established

The historical E10 record asserted position/transform semantics for the templates.vfs list2 payload ("positions", "payload-derived transform data", "CONFIRMED use in one runtime slot-position computation"). The OBSERVED OPERATION is real and stays CONFIRMED, but the spatial/position semantic role of the slot data is NOT established, and Desktop identified a physical falsifier for spatial certainty: the three float groups of record 11963 are equally consistent with normalized RGB-like values.

### Original historical wording (PRESERVED historical artifacts — SUPERSEDED, not modified)

All paths below are inside the historical package `docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/`:

- `02_ANALYSIS/TRACE_EDGE_BLOCKS.md:375` — "## E10 — Template payload list2 (positions) — the payload-derived transform data"
- `02_ANALYSIS/TRACE_EDGE_BLOCKS.md:378-381` — "CLAIM_ID: E10-PAYLOAD-VEC3 / STATUS: CONFIRMED as payload data + CONFIRMED use in one runtime slot-position computation (identity-preserving from the FILE to a computed position, but the SLOT object is not established as a world instance)"
- `02_ANALYSIS/TRACE_EDGE_BLOCKS.md:392` — "consumer chain FUN_00848EA0 (R08) -> slot position store (Q04 slot stride 0x18)"
- `02_ANALYSIS/TRACE_EDGE_BLOCKS.md:456-457` — "template payload list2 -> slot position lerp CONFIRMED (payload-derived transform data)"
- `02_ANALYSIS/TRACE_EDGE_BLOCKS.md:464-465` — "the only payload-derived vec3 (list2) feeds a slot-position computation whose object class is unknown"
- `02_ANALYSIS/CLAIM_MATRIX.csv:11` (row E10-PAYLOAD-VEC3) — "…feeds a runtime slot-position lerp (FUN_0072FE30 -> FUN_006C1F90) — payload-derived transform data established; slot object class UNKNOWN…"
- `06_REPORT/DRAFT_FINAL_REPORT.md:94-96` — "TRANSFORM_EDGE = placement-record setters CONFIRMED as runtime transport …; template payload list2 (3 x vec3) -> runtime slot-position lerp CONFIRMED as …"
- `06_REPORT/DRAFT_FINAL_REPORT.md:108-110` — "PLACEMENT_XYZ_RECOVERED = NO …; the only payload-derived vec3 feeds a slot-position computation of unknown class"
- `06_REPORT/PE_MASTER_REVIEW.md:79-80` — "E10 template list2 payload vec3 -> slot-position lerp: CONFIRMED as payload-derived transform data (slot class UNKNOWN — honest)"
- `07_QC/QC_AUDIT_R1.md:91` — "E10's 'slot object class UNKNOWN' honesty is unaffected"
- `07_QC/QC_AUDIT_R1.md:298-300` — "E10's payload-derived vec3 is honestly scoped to a slot-position computation with UNKNOWN slot class and is NOT conflated with a placement record (PLACEMENT_XYZ_RECOVERED = NO)"
- `06_REPORT/AMEND_LOG_R1.md:113` (AMEND-4 block; AMEND-4/5 start at :98/:123) — "id2 -> lookup -> FUN_0072FE30 -> FUN_006C1F90 lerp -> slot-position chain"

(Note: some console greps rendered "—" as mojibake; all quotes above are restored from the files' actual UTF-8 content.)

### Correction action taken

Supersession record ONLY (this package): the current meaning of the wording above is retracted; the historical files are preserved byte-for-byte. The consolidated current state is in `01_ANALYSIS/CURRENT_CLAIM_STATE.md`; the live-surface census (ACTIVE E10 POSITION/TRANSFORM SEMANTIC PROMOTIONS = 0) is recorded there and in `01_ANALYSIS/EXECUTION_LOG.md`.

### What stays CONFIRMED — E10 observed operation (order §4, verbatim)

```text
templates.vfs list2
→ 9 × u32 when the size gate permits
→ accessed/copied as three 3-component groups
→ interpreted operationally as floats
→ FUN_006C1F90 performs component-wise interpolation
→ result is written as three float components to a runtime slot
```

```text
E10_OBSERVED_OPERATION = CONFIRMED
```

(Historical observed-operation details that remain accurate as OBSERVED OPERATION, not as semantic claims: list2 = vector<u32> at template+0x20 parsed by FUN_00730970; size gate 0x24 → 9 u32 → three vec3s copied by FUN_0072FE30; lerp FUN_006C1F90 (out[i] = a[i] + t*(b[i]-a[i])); consumer FUN_00848EA0; record 4508 list2 empty (28-B payload); record id2=11963 is the 16-string list1 cross-record. Source: historical TRACE_EDGE_BLOCKS.md E10 block, lines 375-393.)

### Corrected wording/statuses (exact strings)

```text
E10_FINAL_SEMANTIC_ROLE = UNVERIFIED
E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED
E10_SLOT_CLASS = UNKNOWN
COLOR_VECTOR_HYPOTHESIS = PLAUSIBLE_ALTERNATIVE_ONLY
```

FORBIDDEN AS CURRENT E10 VOCABULARY (order §4): positions / slot-position / payload-derived position / payload-derived transform / spatial vec3 / world transform.

### Color-vector alternative (counter-test for spatial certainty — NOT a claim)

The three float groups of record 11963:

```text
(0.0705882, 0.2627450, 0.3529410)
(0.1137250, 0.1137250, 0.1137250)
(0.0000000, 0.5372550, 0.7176470)
```

are equally consistent with normalized RGB-like values of approximately:

```text
(18, 67, 90)
(29, 29, 29)
(0, 137, 183)
```

This is EXCLUSIVELY a counter-test against spatial certainty. It is NOT recorded that E10 = COLOR. NO color decoder was built. NO new consumer trace was performed (order §4 prohibitions honored).

### Required global statuses after F-D1 (exact strings)

```text
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
WORLD_INSTANCE_EDGE = NOT_ESTABLISHED
PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED
PLACEMENT_XYZ_RECOVERED = NO
```

### Supersession statement (order §4)

"Historical E10 position/transform wording from b151d428 is SUPERSEDED by this correction."

### What remains unchanged (F-D1)

The observed operation chain; the E10 payload/parse mechanics as observed operation; the WORLD_INSTANCE / PERSISTENT_PLACEMENT / PLACEMENT_XYZ statuses above; the main scope chain; historical texts (preserved, superseded only in current meaning).

---

## F-D2 — ORIGINAL SEVERITY P2 — E2/E3 ABI / INPUT PROVENANCE

### What Desktop established

The historical description of the lookup entry into FUN_0072F580 — "key = id2 in ECX (thiscall …)" and "MOV ECX, EAX (ECX = id2)" — misidentifies the calling convention and the argument provenance. Physically, at 0x006C3F60 EAX holds the registry singleton returned by FUN_0043A550; ECX therefore receives the REGISTRY this, and id2 travels as a STACK argument.

### Original historical wording (PRESERVED historical artifacts — SUPERSEDED, not modified)

- `02_ANALYSIS/TRACE_EDGE_BLOCKS.md:86-87` — "INPUT_VALUE_OR_POINTER_PROVENANCE: key = id2 in ECX (thiscall, ECX set by every caller — pinned for the emitter at 0x006C3F60 `MOV ECX,EAX` before the call)"
- `02_ANALYSIS/TRACE_EDGE_BLOCKS.md:115-117` — "0x006C3F5B  E8 …  CALL FUN_0043A550 (registry lazy-init) / 0x006C3F60  8B C8  MOV ECX, EAX  (ECX = id2) / 0x006C3F62  E8 19 B6 06 00  CALL FUN_0072F580  (lookup; raw rel32 target 0x0072F580 recomputed by c10v2)"

### Correction action taken — corrected ABI (order §5, verbatim)

```text
MOV EAX,[ESP+0x0C]   ; id2
PUSH EAX             ; id2 remains stack argument
CALL FUN_0043A550    ; registry singleton getter
MOV ECX,EAX          ; ECX = registry this
CALL FUN_0072F580    ; lookup(id2)
```

Correct model:

```text
registry_this.FUN_0072F580(id2)
```

where:

```text
ECX = registry_this
id2 = stack argument
```

The old wording "ECX = id2" for the lookup entry is RETRACTED and is forbidden as current wording.

### What stays correct (unchanged)

Post-lookup: EAX = template pointer; EDI = template pointer; MOV ECX,EDI → getter A — remains CORRECT.

Blast radius — F-D2 does NOT overturn:

```text
id2 → registry lookup → template → A @ +0x08 → A=296445
```

nor the separate:

```text
296445 ↔ "296445.nif"
```

### Corrected statuses (exact strings)

```text
MAIN_MAPPING_IMPACT = NONE
ABI_DESCRIPTION_CORRECTED = YES
```

---

## F-D3 — ORIGINAL SEVERITY P2 — GAMEBRYO ORACLE #3 PROVENANCE

### What Desktop established

The historical ORACLE reference for Mechanism 3 — the general file-level reference `CoreLibs\NiMain\NiAVObject.cpp` — is NOT a sufficient locator for the implementation actually used. The correct Win32 implementation locator is `CoreLibs/NiMain/Win32/NiAVObject_Win32.cpp:22`.

### HISTORICAL_ORACLE_REFERENCE (PRESERVED — superseded as a locator)

- `05_ORACLE/ORACLE_RECORDS.md:80` — "## MECHANISM 3 — NiAVObject UpdateWorldData (transform propagation target)"
- `05_ORACLE/ORACLE_RECORDS.md:82-85` — "- ORACLE: Gb12 source `CoreLibs\NiMain\NiAVObject.cpp` (UpdateWorldData / UpdateRgid machinery) + the NINODE_SLOT17 canon (historical, its own run's evidence): Entropia NiNode m_kLocal @+0x38, m_kWorld @+0x6C, world translate X @+0x90; slot 27 described as UpdateWorldData."

### POST_AUDIT_SOURCE_VERIFICATION (measured during THIS correction — 2026-10-03T09:21:53Z)

Measured by the correction executor (pe-reconstruction). This is explicitly NOT the historical executor's knowledge; no backdating. This is the ONLY new source measurement authorized for F-D3 (order §6).

```text
EXACT_PATH = D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\Win32\NiAVObject_Win32.cpp
FILE_SIZE_BYTES = 999
SHA256 = 75E452680D4B52D469EC69EF33C79CF94BF0F3E334250B8FAB3892077BF23FD4
FILE_MTIME_UTC (observed) = 2007-07-05T11:52:25Z
LINE_22_LOCATOR = function definition line: void NiAVObject::UpdateWorldData()
```

Line-22 derived description (locators + short derived quotes only; no source dumps): line 22 is the definition line `void NiAVObject::UpdateWorldData()` — the file's sole function (32 lines total, Win32 implementation translation unit). It implements the UpdateWorldData machinery of oracle Mechanism 3 (transform propagation target): with a parent set, the world matrix composes the parent's world with the local matrix (`m_kWorld = m_pkParent->m_kWorld * m_kLocal`); otherwise `m_kWorld = m_kLocal`; it then forwards UpdateWorldData to the attached collision object. This is the implementation-side counterpart of the historical Mechanism 3 hypothesis (local→world propagation) and of the target-local slot-27 observation.

### Labels (exact strings)

```text
POST_AUDIT_SOURCE_CHECK = YES
MEASURED_DURING_CORRECTION = YES
ORACLE_MECHANISMS = 3   (UNCHANGED — no fourth mechanism added)
```

NOT performed (order §6): no Gamebryo inventory; no SDK build; no runtime Gamebryo; no new cross-version searches.

### Target-local evidence (UNCHANGED — independent observations from Entropia.exe, NOT downgraded)

```text
NiNode slot27
m_kLocal-shaped +0x38
parent m_kWorld-shaped +0x6C
MOV ECX,13
REP MOVSD
```

---

## F-D4 — ORIGINAL SEVERITY P2 — HISTORICAL BUDGET / PROCESS CENSUS

### What Desktop established

The Desktop post-audit produced per-phase tool-call census values (executor initial 125 / executor repair 23 / fresh QC 109 / focused re-QC 69), established that the historical package contains NO preregistered QC budget, and that the earlier declarations "~41 analytical invocations" and "~14 / ~27 / ~10" are non-reconstructable approximations. Full record: `01_ANALYSIS/HISTORY_BUDGET_RECONCILIATION.md` (honest process record — NOT a history repair).

### Correction action taken

Honest process record + retraction of any full-conformance claim + preservation of NOT_ESTABLISHED. Historical artifacts preserved unmodified.

### Measurement results (bounded session-store census attempt — 5/5 preregistered calls used)

The local opencode store (`C:\Users\User\.local\share\opencode\opencode.db`, read-only SQLite query) contains the historical run's sessions (2026-10-03, workspace D:/TESTAI, parent session `ses_eff65ce0dffehQR2H4VAoaJOIv` "Eksperyment PE_935 Placement Record Bridge", created 2026-10-03T07:11:07Z):

```text
executor session ses_eff63660cffeJE8ariHPxOW4KQ ("Execute bounded placement bridge run", 2026-10-03T07:13:45Z):
  148 tool parts total = 125 + 23 EXACTLY (sum machine-verified; the 125/23 split itself is NOT independently reconstructable — one session contains both phases)
fresh QC session ses_eff4f9ba2ffe54l7YQDmBq294P ("Fresh internal QC of bridge run", 2026-10-03T07:35:22Z):
  109 tool parts — INDEPENDENTLY RECOMPUTED (exact match with the Desktop census value)
focused re-QC session ses_eff40a7ffffex6TtoVQEAWrKmX ("Focused re-QC of repair round", 2026-10-03T07:51:42Z):
  69 tool parts — INDEPENDENTLY RECOMPUTED (exact match with the Desktop census value)
```

Two further child sessions of the same parent were identified but are NOT part of the four census values: persistence session `ses_eff335334ffekauyuLGpNeRUxP` (2026-10-03T08:06:16Z, 55 tool parts) and a separate service-restore session `ses_eff20857cffeai93HfqGMdWPT8` (2026-10-03T08:26:48Z, 112 tool parts).

### Required final statuses (exact strings)

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED
HISTORICAL_TOOL_CALL_CENSUS = MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE
HARD_HISTORICAL_PHASE_LIMIT_BREACH = NOT_DEMONSTRATED
FULL_HISTORICAL_BUDGET_CONFORMANCE = NOT_PROVEN
```

### Disposition

```text
F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD
```

Closure = honest process record + retraction of any full-conformance claim + preservation of NOT_ESTABLISHED — NEVER a retroactive PASS. A session's TOTAL tool-call count alone cannot establish ENUM > 30 / DEEP_TRACE > 90 / CONTROLS+ORACLE > 30 because no historical rule assigned every tool call to those phases (order §7).

---

## WHAT REMAINS UNCHANGED GLOBALLY (order §9 invariants — exact strings)

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

No UNKNOWN was promoted; no invariant was weakened; no historical text was edited (supersede, never modify).
