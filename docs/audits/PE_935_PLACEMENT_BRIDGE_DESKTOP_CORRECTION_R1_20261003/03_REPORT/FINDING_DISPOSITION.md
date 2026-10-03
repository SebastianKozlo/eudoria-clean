# FINDING DISPOSITION — PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003

Order §14 disposition record for the Desktop post-audit findings of
b151d428fc46818bc3b84d8ca000d92caa2cd76b (order: 00_CONTROL/AUTHORIZATION.md §14).

## HISTORICAL DESKTOP VERDICT (PRESERVED — IMMUTABLE)

```text
for b151d428: DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS
OPEN_AT_DESKTOP_AUDIT: F-D1 = P1, F-D2 = P2, F-D3 = P2, F-D4 = P2
SUPPORTED_RESULT_LEVEL = B
```

The dispositions below are records of the NEW correction cycle only. They do NOT retroactively
change the historical Desktop verdict for b151d428 (order §§0, 10: "Nowy correction commit NIE
może retrospektywnie zmieniać tego werdyktu na PASS."). History remains open.

---

## F-D1 — E10 SEMANTIC RETRACTION

```text
ORIGINAL = P1
DISPOSITION = CORRECTED
```

SCIENCE_EFFECT: no science result retracted except the E10 semantic wording — the observed
operation stays CONFIRMED (E10_OBSERVED_OPERATION = CONFIRMED with the order §4 chain verbatim:
templates.vfs list2 → 9 × u32 when the size gate permits → three 3-component groups →
interpreted operationally as floats → FUN_006C1F90 component-wise interpolation → three float
components written to a runtime slot); the semantics are now UNVERIFIED / NOT_ESTABLISHED
(E10_FINAL_SEMANTIC_ROLE = UNVERIFIED; E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED;
E10_SLOT_CLASS = UNKNOWN; COLOR_VECTOR_HYPOTHESIS = PLAUSIBLE_ALTERNATIVE_ONLY — counter-test
only, no "E10 = COLOR" claim). PLACEMENT_XYZ_RECOVERED stays NO. Required global statuses hold
(WORLD_INSTANCE_IDENTITY / WORLD_INSTANCE_EDGE / PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED).
The historical E10 position/transform wording from b151d428 is SUPERSEDED by this correction
(supersession statement: 01_ANALYSIS/CURRENT_CLAIM_STATE.md §1; historical texts preserved as
historical artifacts). Fresh-QC-measured active E10 position/transform semantic promotions = 0
(02_QC/TARGETED_QC_REPORT.md Q1). No science layer beyond the E10 semantic wording was affected:
the main record→resource chain (§9 invariants) is untouched.

## F-D2 — E2/E3 ABI / INPUT PROVENANCE

```text
ORIGINAL = P2
DISPOSITION = CORRECTED
```

SCIENCE_EFFECT: MAIN_MAPPING_IMPACT = NONE — the mapping chain (record 4508 → parser →
registry → keyed lookup → A @ template+0x08 → request pair {0x66, A=296445}; separately
A=296445 ↔ "296445.nif") is UNCHANGED; only the ABI description was corrected:
registry_this.FUN_0072F580(id2) with ECX = registry_this and id2 = stack argument; the old
"ECX = id2" lookup-entry wording is RETRACTED; ABI_DESCRIPTION_CORRECTED = YES. Post-lookup
EAX = EDI = template pointer; MOV ECX,EDI → getter A remains correct. Fresh-QC verification from
existing raw evidence (02_QC/raw/q2_abi_evidence.md): pre-call bytes show exactly the corrected
flow; "ECX = id2" is physically impossible. QC-P3-2 precision note recorded (see below).

## F-D3 — GAMEBRYO ORACLE #3 PROVENANCE

```text
ORIGINAL = P2
DISPOSITION = CORRECTED
```

SCIENCE_EFFECT: locator provenance corrected, NO science status change — the general reference
CoreLibs\NiMain\NiAVObject.cpp (HISTORICAL_ORACLE_REFERENCE) is superseded as a locator by the
POST_AUDIT_SOURCE_VERIFICATION CoreLibs/NiMain/Win32/NiAVObject_Win32.cpp:22 (999 B; SHA256
75E452680D4B52D469EC69EF33C79CF94BF0F3E334250B8FAB3892077BF23FD4; line 22 =
void NiAVObject::UpdateWorldData(); POST_AUDIT_SOURCE_CHECK = YES; MEASURED_DURING_CORRECTION =
YES — measured 2026-10-03 by the correction executor, no backdating; independently re-hashed by
the fresh QC). ORACLE_MECHANISMS = 3 (UNCHANGED — no fourth mechanism). Target-local evidence
from Entropia.exe (NiNode slot27; m_kLocal-shaped +0x38; parent m_kWorld-shaped +0x6C;
MOV ECX,13; REP MOVSD) is NOT downgraded. No Gamebryo inventory, no SDK build, no runtime
Gamebryo, no cross-version searches.

## F-D4 — HISTORICAL BUDGET / PROCESS CENSUS

```text
ORIGINAL = P2
DISPOSITION = CORRECTED_BY_HONEST_PROCESS_RECORD
```

SCIENCE_EFFECT: process record only — no historical budget value was invented. The four census
values are recorded with provenance (01_ANALYSIS/HISTORY_BUDGET_RECONCILIATION.md): executor
initial 125 / executor repair 23 = INHERITED_FROM_DESKTOP_POST_AUDIT (+ machine sum check
148 = 125+23); fresh QC 109 / focused re-QC 69 = RECOMPUTED_FROM_LOCAL_SESSION_STORE, exact —
independently reproduced by the fresh targeted QC AND PE-MASTER. The earlier declarations ~41
and ~14/~27/~10 = UNVERIFIED / NON_RECONSTRUCTABLE (no reproducible counting rule; no
after-the-fact denominator). Final statuses preserved exactly: HISTORICAL_QC_BUDGET_PRE_REGISTERED
= NOT_ESTABLISHED; HISTORICAL_TOOL_CALL_CENSUS =
MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE; HARD_HISTORICAL_PHASE_LIMIT_BREACH =
NOT_DEMONSTRATED; FULL_HISTORICAL_BUDGET_CONFORMANCE = NOT_PROVEN. F-D4 does NOT require
QC_BUDGET_PRE_REGISTERED = YES (order §14: "F-D4 nie wymaga: QC_BUDGET_PRE_REGISTERED = YES";
CORRECTED_BY_HONEST_PROCESS_RECORD is a valid closure) — closure is by honest process record +
retraction of the full-conformance claim + preservation of NOT_ESTABLISHED / NOT_PROVEN, never
by a retroactive PASS.

---

## FRESH TARGETED QC FINDINGS (order §13 record; 02_QC/TARGETED_QC_REPORT.md)

```text
QC-P3-1 — P3 — EXECUTION_LOG wall-minute self-report nuance: ACCEPTED; closed by the
  FINAL_REPORT wall-time clarification (03_REPORT/FINAL_REPORT.md §3: the "≈14" figure measured
  from the Phase A start ~09:14Z rather than Phase B ~09:17Z; the final ~12 min matches the
  physical window 09:17Z→09:28:35Z; no budget conclusion changes). Non-blocking; no repair
  round required.
QC-P3-2 — P3 — order §5 flow block omits the prologue register saves: ACCEPTED; closed by the
  FINAL_REPORT precision footnote (03_REPORT/FINAL_REPORT.md §2/F_D2, quoted directly after the
  order §5 flow quote: the physical window C9 L01 contains three prologue register saves PUSH
  EBX/ESI/EDI @0x006C3F57-59 between MOV EAX,[ESP+0x0C] @0x006C3F53 and PUSH EAX @0x006C3F5A;
  the id2 stack-argument conclusion is unaffected). The order text itself is frozen contract
  text and is NOT modified (order-quoted blocks stay verbatim per the AUTHORIZATION contract).

QC_REPAIR_ROUNDS_MAX = 1 — UNCONSUMED (no repair round was needed; both P3 findings are
  non-blocking documentation nuances closed inside the Phase D reports)
```

---

## CLOSURE SUMMARY

```text
F-D1 = CORRECTED
F-D2 = CORRECTED
F-D3 = CORRECTED
F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD
TARGETED_QC_VERDICT = CORRECTION_RE_QC_PASS (fresh context, scope Q1–Q7)
PE-MASTER ADVISORY = MASTER_ACCEPTED (ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE)
HISTORICAL DESKTOP VERDICT for b151d428 = REQUIRE_CORRECTIONS — PRESERVED IMMUTABLE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES (order §22; single next action: HUMAN → focused Desktop re-audit of the exact
pushed correction SHA)
```

END OF FINDING DISPOSITION.
