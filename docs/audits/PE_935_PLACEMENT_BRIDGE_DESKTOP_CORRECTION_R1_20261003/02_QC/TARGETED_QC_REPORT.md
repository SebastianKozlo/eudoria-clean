# TARGETED QC REPORT — PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003

```text
QC_RUN_ID = PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_TARGETED_QC_20261003
QC_PHASE = FRESH TARGETED QC (order §13, scope Q1–Q7)
FRESH_CONTEXT = YES — this QC session did NOT author the correction; entry through artifacts only
               (the correction was authored by pe-reconstruction, Phase B, under PE-MASTER dispatch)
AUDITED_PACKAGE = docs/audits/PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003/
AUDITED_BASE_SHA = AUDITED_DESKTOP_SHA = b151d428fc46818bc3b84d8ca000d92caa2cd76b (verified at QC start AND at QC end)
HISTORICAL_PACKAGE (READ-ONLY) = docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
DATE = 2026-10-03 (UTC; measurements 09:29Z–09:38Z)
NO_NESTED_TASKS = YES (no Task dispatched by this QC)
RE_PERFORMED_BY_QC = NONE (no new RE, no new placement trace, no 4057/0x0059AB12 work, no EXE byte read —
  the single binary-adjacent touch was the order-authorized F-D3 re-hash + read of NiAVObject_Win32.cpp,
  a SOURCE FILE, and re-hashing/reading repo files for identity checks)
```

## EXECUTIVE SUMMARY

All four corrections (F-D1..F-D4) verified against physical evidence with my own instruments. The corrected
E10 semantics are byte-and-package consistent; the F-D2 ABI correction is confirmed by raw EXE-window
evidence (the old "ECX = id2" wording is physically impossible); the F-D3 locator/identity claims match my
own re-hash; the F-D4 census values 109 and 69 are EXACTLY reproduced by my independent store recount, with
125/23 honestly inherited and machine-sum-checked; the correction budget was written before all correction
work; all §9 invariants are exact; the deferred lead is preserved-only with no RE performed. No P0/P1/P2
defect was introduced by the correction. Two P3 documentation nuances recorded (non-blocking).

```text
QC_VERDICT = CORRECTION_RE_QC_PASS
```

---

## Q1 — F-D1 (E10 semantic retraction) — PASS

- Claim (package): ACTIVE E10 POSITION/TRANSFORM SEMANTIC PROMOTIONS = 0; required statuses present;
  historical package preserved.
- My own census (raw: 02_QC/raw/q1_e10_census.md): case-sensitive grep `slot-position|slot position|
  payload-derived|payload derived|spatial vec3` over ALL repo *.md + *.csv; separate censuses for
  `world transform` and `positions`; case-insensitive check of the SCENEFEEDER hit.
  - Historical package hits: 5 files / 15 lines — MY COUNT EXACTLY MATCHES the executor's census
    (TRACE 7, AMEND 1, DRAFT 4, PE_MASTER_REVIEW 1, QC_AUDIT 2) → preserved historical artifacts,
    superseded by the correction record — NOT live residue.
  - New-package hits: ALL are supersession/census/contract text (forbidden-vocabulary lists, historical
    quotes, retraction statements) — NOT promotions. AUTHORIZATION.md hits are the verbatim human order
    (frozen contract), including the order's own forbidden-vocabulary list — contract text, not promotion.
  - UNRELATED_SENSE (verified individually): NINODE_SLOT17 ×3 ("slot-position alignment" — vtable slot
    alignment), SF_ARG2 ×2 ("slot positions across its 10 vtables" — vtable slots), SCENEFEEDER ×1
    (case-insensitive only: "slot POSITION_TO_CALL" @RUN_CONTRACT.md:105 — vtable-slot naming; my own
    case-insensitive grep confirms exactly this 1 hit).
  - AUDIT_ENTRYPOINT.md: my own substring extraction shows ALL its "positions" occurrences are inside
    "dispositions" or the negative statements "the 296445 positions NOT recovered" → 0 E10 promotions.
  - `world transform` hits outside the packages: all UNRELATED_SENSE (SF position-consumer family,
    external-sources packet grammar, REJECTED NIF notes, transform-discipline contract rules) or
    historical/contract text → no live E10 promotion.
- Required statuses verified by full reads of CURRENT_CLAIM_STATE.md + DESKTOP_FINDINGS.md:
  E10_OBSERVED_OPERATION = CONFIRMED (with the order §4 observed-operation chain verbatim, unchanged);
  E10_FINAL_SEMANTIC_ROLE = UNVERIFIED; E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED;
  E10_SLOT_CLASS = UNKNOWN; COLOR_VECTOR_HYPOTHESIS = PLAUSIBLE_ALTERNATIVE_ONLY;
  WORLD_INSTANCE_IDENTITY/WORLD_INSTANCE_EDGE = NOT_ESTABLISHED; PERSISTENT_PLACEMENT_EDGE =
  NOT_ESTABLISHED; PLACEMENT_XYZ_RECOVERED = NO; supersession statement present VERBATIM
  ("Historical E10 position/transform wording from b151d428 is SUPERSEDED by this correction.");
  NO "E10 = COLOR" assertion (package-wide grep: only negatives/prohibition text); no color decoders
  (package tree = 9 md/csv files); no consumer trace added.
- Historical package integrity (my re-hash): 06_REPORT/FINAL_REPORT.md = 27,690 B /
  SHA256 EDC245EFE76CB774FA2F65863AF9E14531BCBC9AFAB9EA8B84EB251764E048B0; 06_REPORT/PE_MASTER_REVIEW.md =
  12,901 B / SHA256 4BE5A85497EB2BFB9083A02BDC0080DEC5E946691B8FD9E3D758BE6835836E2D — both MATCH the
  Phase-A pins; git status on the historical path = clean.
- Result: **ACTIVE E10 POSITION/TRANSFORM SEMANTIC PROMOTIONS = 0 (CONFIRMED by my own census).**

## Q2 — F-D2 (ABI correction) — PASS (verified from existing raw evidence; EXE not touched)

- Claim (package): registry_this.FUN_0072F580(id2); ECX = registry_this; id2 = stack argument; old
  "ECX = id2" retracted; MAIN_MAPPING_IMPACT = NONE; ABI_DESCRIPTION_CORRECTED = YES.
- My verification (raw: 02_QC/raw/q2_abi_evidence.md):
  - C9_LISTING_WINDOWS.json window L01 (emitter FUN_006C3F50, start 0x006C3F50) COVERS the pre-call bytes:
    `8B 44 24 0C` MOV EAX,[ESP+0x0C] @0x006C3F53; PUSH EBX/ESI/EDI (prologue saves); `50` PUSH EAX
    @0x006C3F5A; `E8 F0 65 D7 FF` CALL 0x0043A550 @0x006C3F5B (rel32 recomputed by me → 0x0043A550 ✓);
    `8B C8` MOV ECX,EAX @0x006C3F60 ✓ (the pinned instruction); `E8 19 B6 06 00` CALL 0x0072F580
    @0x006C3F62 ✓ (rel32 recomputed by me → 0x0072F580 ✓). **The pre-call bytes showed exactly the
    corrected flow: id2 loaded from [ESP+0x0C] and PUSHed as the stack argument before the getter call.**
    Because the window covers 0x006C3F50..0x006C3F5A, the bounded physical EXE re-read was NOT needed and
    was NOT performed (zero EXE bytes read by this QC). C10V2 (exe SHA E7785430…; 962/962 windows bytes
    identical; 113/113 targets) corroborates the windows against the pinned EXE.
  - Window L02: `C2 04 00` RET 0x4 @0x0072F5A2 (one 4-byte stack argument; both return paths) ✓;
    body decodes as thiscall over the container (MOV ESI,ECX; mapfind called with ECX=ESI; tree walk from
    [ESI+4]/[ESI+8]; sentinel CMP EAX,ESI; key read via LEA EAX,[ESP+0xC] → &arg1 → mapfind arg2 →
    MOV ESI,[ESI] deref) → ECX at the lookup entry = the registry, NOT id2 (if ECX were id2≈4508 the walk
    would read absolute address 0x1194 — physically impossible).
  - E1/X11 (TRACE_EDGE_BLOCKS.md:46-52): FUN_0043A550 = lazy registry-singleton getter (root
    DAT_00BA1824; if 0 → new(0x18) → FUN_0052A260) — returns the registry in EAX ⇒ MOV ECX,EAX sets
    ECX = registry_this ✓. Parallel caller L08 (FUN_00567170: PUSH ESI; CALL FUN_0043A550; MOV ECX,EAX;
    CALL FUN_0072F580) confirms the family-wide ABI ✓.
  - Post-lookup unchanged: MOV EDI,EAX @0x006C3F67; MOV ECX,EDI @0x006C3F6E; CALL FUN_007CE1E0 @0x006C3F74 ✓.
  - Package-wide "ECX = id2" grep: ONLY quote/retraction/contract contexts (AUTHORIZATION §5 prohibition
    text; CORRECTION_MATRIX historical-wording column; the explicit RETRACTED statements) — NOT a current
    claim anywhere. Main mapping chain (record → registry → lookup → A @ template+0x08 → {0x66, A=296445};
    separately A=296445 ↔ "296445.nif") unchanged in CURRENT_CLAIM_STATE.md §7 ✓.
- Precision finding QC-P3-2 below (prologue pushes omitted from the order's own flow block) — non-blocking.

## Q3 — F-D3 (oracle provenance) — PASS

- My own re-hash + full read (raw: 02_QC/raw/q3_source_identity.txt): EXACT PATH
  D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\Win32\NiAVObject_Win32.cpp EXISTS; SIZE = 999 B ✓;
  SHA256 = 75E452680D4B52D469EC69EF33C79CF94BF0F3E334250B8FAB3892077BF23FD4 ✓ (MATCHES the claimed value);
  MTIME_UTC = 2007-07-05T11:52:25Z; line 22 = `void NiAVObject::UpdateWorldData()` — the file's SOLE
  function (32 lines), body = parent-compose (m_kWorld = m_pkParent->m_kWorld * m_kLocal) / else
  (m_kWorld = m_kLocal) / forward to collision object — exactly as the package describes.
- Labels: POST_AUDIT_SOURCE_CHECK = YES; MEASURED_DURING_CORRECTION = YES; measured 2026-10-03 by the
  correction executor, explicitly NOT backdated ✓. HISTORICAL_ORACLE_REFERENCE (general
  CoreLibs\NiMain\NiAVObject.cpp, ORACLE_RECORDS.md:82-85 — read intact) is separated from
  POST_AUDIT_SOURCE_VERIFICATION ✓. ORACLE_MECHANISMS = 3 UNCHANGED — no fourth mechanism anywhere ✓.
- No Gamebryo inventory / SDK build / runtime Gamebryo / cross-version searches: package tree contains
  exactly the 9 md/csv files (no such artifacts); EXECUTION_LOG §3 records the negatives ✓.
- Target-local evidence NOT downgraded: NiNode slot27 (0x007E4820), m_kLocal-shaped +0x38, parent
  m_kWorld-shaped +0x6C, MOV ECX,13 / REP MOVSD preserved verbatim as independent target-local
  observations (CURRENT_CLAIM_STATE.md §4; historical ORACLE_RECORDS.md intact) ✓.
- Historical 05_ORACLE/ORACLE_RECORDS.md NOT modified (git clean; read confirms intact MECHANISM 3) ✓.

## Q4 — F-D4 (budget/census honest record) — PASS

- HISTORY_BUDGET_RECONCILIATION.md verified against the historical sources (my reads):
  - Preserved executor budgets verbatim from RUN_PLAN.md:28-32 ("## Budget (fixed BEFORE analysis; NOT
    expandable after results)": ENUM max 30 / DEEP_TRACE max 90 / CONTROLS+ORACLE max 30) ✓.
  - HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED — and NOTHING in the new package writes YES:
    my package-wide grep found the ONLY "= YES" occurrence inside AUTHORIZATION.md:357 = the verbatim
    order §3 PROHIBITION text ("Nie wolno na ich podstawie dopisywać historycznie:
    HISTORICAL_QC_BUDGET_PRE_REGISTERED = YES") — contract text, not a status ✓.
  - Four census values each with VALUE / SOURCE / SESSION_ID / COUNT_SCOPE / COUNTING_METHOD /
    INDEPENDENTLY_RECOMPUTED / PROVENANCE_STATUS ✓ (§3.1–3.4).
  - ~41 and ~14/~27/~10 inventory with locations, claimed meaning, no reproducible rule, non-reconcilable
    with the store, STATUS = UNVERIFIED / NON_RECONSTRUCTABLE ✓ (NOT_CHECKED.md:57-61 verified verbatim —
    the ~41 total and the ~14+~27+~10 ≈ 51 per-phase sum coexist in the SAME section; the arithmetic
    tension is recorded honestly WITHOUT an invented resolution) ✓.
  - Required final statuses present: HARD_HISTORICAL_PHASE_LIMIT_BREACH = NOT_DEMONSTRATED;
    FULL_HISTORICAL_BUDGET_CONFORMANCE = NOT_PROVEN; HISTORICAL_TOOL_CALL_CENSUS =
    MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE; the explicit statement that a session total alone
    cannot establish per-phase overruns (no historical phase-attribution rule) ✓; closure =
    CORRECTED_BY_HONEST_PROCESS_RECORD (never a retroactive PASS) ✓.
  - Historical QC's own verdicts verified verbatim: QC_AUDIT_R1.md:322-324 ("declared usage ~14/~27/~10 —
    QC cannot re-count tool invocations from artifacts (noted as UNVERIFIED, not contradicted)") and
    :390 ("Budget usage counts (~14/~27/~10): UNVERIFIED") — the reconciliation's citations are EXACT.
    (Note: my single-line Select-String first missed the quote because it wraps across lines 323/324;
    the citation "323-324" is accurate — instrument limitation, documented in 02_QC/raw.)
- MY OWN STORE RECOUNT (raw: 02_QC/raw/q4_store_census.py + q4_store_census_output.txt; read-only SQLite
  URI mode; my method: part rows with data JSON type == 'tool' per session_id):
  - executor ses_eff63660cffeJE8ariHPxOW4KQ ("Execute bounded placement bridge run", 2026-10-03T07:13:45Z,
    parent ses_eff65ce0dffehQR2H4VAoaJOIv): TOOL_PARTS = **148** → machine sum check 148 = 125 + 23 ✓.
  - fresh QC ses_eff4f9ba2ffe54l7YQDmBq294P ("Fresh internal QC of bridge run", 07:35:22Z):
    TOOL_PARTS = **109** — EXACT MATCH with the Desktop census value and the executor's
    INDEPENDENTLY_RECOMPUTED claim ✓ (total parts 316 ✓ matches §3.3).
  - focused re-QC ses_eff40a7ffffex6TtoVQEAWrKmX ("Focused re-QC of repair round", 07:51:42Z):
    TOOL_PARTS = **69** — EXACT MATCH ✓ (total parts 224 ✓ matches §3.4).
  - Side identifications match: persistence session 55 tool parts; service-restore session 112; parent
    title "Eksperyment PE_935 Placement Record Bridge" (07:11:07Z) — all as the executor recorded ✓.
  - The 125/23 SPLIT remains inherited (no phase boundary in the store) — the executor's
    INDEPENDENTLY_RECOMPUTED = NO for those values is honest and my recount confirms its consistency ✓.
  → The executor's store provenance claims are SUPPORTED BY MY OWN RECOUNT; no fabricated measurement.

## Q5 — CURRENT CORRECTION BUDGET — PASS

- Budget-before-work (raw: 02_QC/raw/q5_mtimes.txt): CORRECTION_BUDGET.md physical mtime =
  2026-10-03T09:17:50Z — PREDATES all six 01_ANALYSIS files (earliest DESKTOP_FINDINGS.md 09:26:31Z;
  latest EXECUTION_LOG.md 09:28:19Z) and all recorded Phase B measurements (first UTC-stamped call
  09:21:08Z; F-D3 source measurement 09:21:53Z; §8A recount 09:21:56Z; E10 census 09:21:57Z; store
  census ~09:22–09:25Z). The banner timestamp 09:16:45Z is DISCLOSED in the file as the AUTHORIZATION.md
  byte-identity verification time (AUTHORIZATION.md mtime = 09:16:45Z — matches), i.e. the last verified
  measurement preceding the budget write — honest provenance, not a backdated write.
- Planned vs used: Phase A 10/15 (+ wall ~5 min ≤ 25); Phase B 26/65 (+ wall ~12 min ≤ 95); executor-phase
  total 36/80 — no cap exceeded; A+B ≤ 80 holds; EXECUTION_LOG self-reports (25 as of write, planned final
  26/65) match the handoff numbers; no retroactive limit change.
- QC-P3-1 (below) records the ≈14-vs-~12 wall-minute self-report nuance (non-blocking).
- Honest limitation recorded: mtimes alone do not prove absence of pre-budget work, but every
  correction-produced artifact/measurement is post-budget and no contradicting evidence exists.

## Q6 — INVARIANTS (order §9) + §8 PRECISIONS — PASS

- CURRENT_CLAIM_STATE.md §7 carries EXACTLY (full read, character-checked):
  MAIN_RECORD_REQUEST_INDEX_CHAIN = SUPPORTED; RESULT_LEVEL = B; MODEL_ID_RECOVERED = YES;
  RUNTIME_NIF_OPEN = NOT_CLOSED; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED;
  WORLD_INSTANCE_EDGE = NOT_ESTABLISHED; PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED;
  PLACEMENT_XYZ_RECOVERED = NO; E10_FINAL_SEMANTIC_ROLE = UNVERIFIED;
  E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED; CANONICAL_GATE_EFFECT = NONE;
  PE_MASTER_QUALIFICATION_CHANGE = NO; M1_CLOSED = NO; M2_AUTHORIZED = NO; M3_AUTHORIZED = NO;
  NEXT_EXPERIMENT_AUTHORIZED = NO. The main chain and the separate 296445 ↔ "296445.nif" join unchanged ✓.
- §8A: DECOMPILATION_RECORDS = 88 vs UNIQUE_FUNCTION_ENTRY = 87 — **MY OWN RECOUNT CONFIRMS EXACTLY**
  (raw: 02_QC/raw/q6_decomp_recount.py + output): TOTAL = 88, UNIQUE = 87, exactly ONE duplicate pair
  0x6baa20 = C3:R10_other_006baa20 + C6:Y07_consumer_006baa20; per-file C2=4, C3=17, C4=12, C5=12,
  C6=17, C7=12, C8=10, C11=4 (C1/C9/C10/C10V2/C12 = 0); three independent extraction routes (field,
  key, code signature) agree on every record (0 mismatches). Corroborated: historical QC decomp_dump =
  88 .c files; recheck4_decomp_integrity.json {dump_files: 88, match: 88, mismatch: [], all_match: true}
  — matches the package's citation. "88 unique functions" is NOT used as a current claim (package-wide
  grep: only the order's prohibition text and the retraction/negative statements). Hard limit 120 NOT
  demonstrated exceeded ✓.
- §8B list1: full schema NOT presented as only count × strings; element +0x20 covers two further u32 =
  UNKNOWN; NO parser extension (git status: ZERO tracked modifications anywhere — only the new package
  untracked; no parser/code file touched) ✓.
- §8C reader census: "1 caller" = CENSUS_BOUNDED_OBSERVATION, NOT GLOBAL_PROOF_OF_ONLY_POSSIBLE_READER
  (grep confirms only the NOT-label usages); WORLD_INSTANCE_EDGE = NOT_ESTABLISHED, never "does not exist"
  (grep: only negative/retraction contexts) ✓.

## Q7 — DEFERRED LEAD (4057/218757/0x0059AB12/886) — PASS (preserved only)

- DEFERRED_PLACEMENT_LEADS.md preserves the lead ONLY as an unverified future lead: the exact order §11
  epistemic status block (all LOCAL_LEAD / TO_BE_REPINNED, UNVERIFIED, UNKNOWN — verbatim, none
  promoted); the §12 candidate experiment PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1 with
  AUTHORIZATION_STATUS = NOT_AUTHORIZED, anchor, primary question, MANDATORY FALSIFIER verbatim
  ("If immediate 4057 does NOT reach FUN_0072F580 … must be treated as coincidental and the lead
  rejected."), the 12-step ladder, the 886 unknown, the success thresholds ✓.
- NO RE performed: package tree = 9 md/csv files (no Ghidra artifacts, no EXE scans, no decompilations, no
  XYZ work); package-wide 4057/218757/59AB12/0x008D/886 grep shows hits ONLY in the order contract text
  (AUTHORIZATION.md), the authorized preservation record (DEFERRED_PLACEMENT_LEADS.md), and the
  EXECUTION_LOG negatives/handoff; "218757.nif/218758.bvi exist" claims recorded ONLY as
  LOCAL_LEAD_TO_BE_REPINNED_IN_FUTURE_AUTHORIZED_RUN (not repinned, not promoted) ✓.
- IMMEDIATE_4057_IS_TEMPLATE_ID = UNVERIFIED etc. are NOT promoted; the candidate run is NOT executed;
  NEXT_4057_EXPERIMENT_AUTHORIZED = NO ✓.

---

## FINDINGS

**QC-P3-1 — P3 — EXECUTION_LOG.md §1 wall-minute self-report nuance (non-blocking).**
- PATH: docs/audits/PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003/01_ANALYSIS/EXECUTION_LOG.md
  (§1: "WALL_MINUTES_AS_OF_THIS_WRITE ≈ 14 of MAX 95").
- CLAIM: ~14 wall minutes elapsed as of the EXECUTION_LOG write (Phase B).
- COUNTER-EVIDENCE (my measurement): EXECUTION_LOG mtime 09:28:19Z; stated Phase B start ≈09:17Z →
  elapsed ≈11.3 min; the final handoff wall number (~12) matches the physical window (09:17Z→~09:28:35Z).
  The ≈14 figure corresponds to the elapsed time since the PHASE A start (~09:14Z), not the Phase B start.
- BLAST RADIUS: none material — both values are disclosed approximations ("≈"), both far below the 95-min
  cap; no budget conclusion changes.
- REQUIRED DISPOSITION: optional one-line clarification in the Phase D report; no repair round required.

**QC-P3-2 — P3 — order §5 flow block omits the prologue register saves (precision note, non-blocking).**
- PATH: 00_CONTROL/AUTHORIZATION.md order §5 flow block; quoted verbatim in 01_ANALYSIS/
  CURRENT_CLAIM_STATE.md §3 and DESKTOP_FINDINGS.md F-D2.
- CLAIM (as quoted): MOV EAX,[ESP+0x0C] directly followed by PUSH EAX then CALL FUN_0043A550.
- COUNTER-EVIDENCE (my decode of C9 L01): physically PUSH EBX/ESI/EDI (@0x006C3F57-59) intervene between
  MOV EAX,[ESP+0x0C] @0x006C3F53 and PUSH EAX @0x006C3F5A.
- BLAST RADIUS: none — the simplification is the human order's own verbatim text (the package quotes it
  faithfully as required); the id2 stack-argument analysis is unaffected (the pushed value is still the
  [ESP+0x0C] load, i.e. the emitter's incoming arg1).
- REQUIRED DISPOSITION: none for this cycle (order text is frozen); optional precision footnote in the
  Phase D FINAL_REPORT when quoting the flow.

**Verified non-findings (recorded for transparency):**
- Budget banner 09:16:45Z vs budget file mtime 09:17:50Z: the relationship is explicitly disclosed in the
  file (09:16:45Z = the AUTHORIZATION byte-identity verification preceding the write); preregistration
  physically completed 09:17:50Z, still before all correction work — NOT a defect.
- AUTHORIZATION.md "HISTORICAL_QC_BUDGET_PRE_REGISTERED = YES" @line 357 and "E10 = COLOR" @line 446 /
  "ECX = id2" @line 515: verbatim order PROHIBITION text — contract, not status writes (classified).
- QC_AUDIT_R1.md "re-count tool invocations" citation: accurate (spans lines 323-324); my first
  single-line search missed it — instrument limitation, documented, not a package defect.

---

## COVERAGE

FULL_READ (complete, to EOF): all 9 package files (AUTHORIZATION.md 2152 lines, CORRECTION_BUDGET.md,
PREFLIGHT.md, six 01_ANALYSIS files); NiAVObject_Win32.cpp (32 lines); historical TRACE_EDGE_BLOCKS.md
lines 28-134 (E1/E2/E3 blocks); historical ORACLE_RECORDS.md lines 75-99; historical RUN_PLAN.md lines
24-53; historical NOT_CHECKED.md lines 52-68; historical QC_AUDIT_R1.md lines 318-331 + 385-394;
C10V2_BYTE_CROSSCHECK.json (815 lines); C9_LISTING_WINDOWS.json lines 1-2590 (windows L01, L02, L03, L08,
L11, L14-L19 headers); C3_DECOMP.json + C2_CALLER_CENSUS.json heads (structure determination).

RECOMPUTED / CENSUS (my own instruments): full-repo E10-vocabulary censuses (*.md + *.csv, case-sensitive
+ targeted case-insensitive); "world transform"/"positions" censuses; 4057-family package census;
"88 unique"/"does not exist"/"GLOBAL_PROOF"/"ECX = id2"/"E10 = COLOR" package greps; my own SQLite store
recount (109/69 exact, 148 sum check, session identifications); my own decompilation recount (88/87, 3
extraction routes, 0 route mismatches); my own byte decode of C9 L01/L02 incl. rel32 recomputation;
re-hash of the 2 historical anchor files + NiAVObject_Win32.cpp; package tree census (9 files + QC raw);
physical mtimes of all package files; HEAD/porcelain verification at QC start AND end.

BOUNDED_INSPECTION: AUDIT_ENTRYPOINT.md via targeted substring extraction (all "positions" occurrences
classified; full row re-audit outside this QC's scope).

NOT_CHECKED (explicit; none load-bearing for the verdict):
- No placement experiment re-run; no new RE of any kind (per contract — absence verified instead).
- C9_LISTING_WINDOWS.json lines 2591-4940 (remaining windows) not read — not load-bearing for F-D2;
  C10V2's 962/962 byte-identity covers their integrity.
- Historical C1/C4/C5/C6/C7/C8/C11/C12 raw contents beyond the decompilation-record structure (the
  decompilation records of ALL C-files were machine-recounted; their code content was not re-read).
- Historical 07_QC/QC_RECHECK_R1.md not read in full (its F-D4-relevant role is recount-method references;
  the load-bearing QC_AUDIT_R1 citations were verified verbatim).
- The external Desktop post-audit session itself (off-machine): the 125/23 split remains INHERITED —
  unverifiable here, exactly as the executor recorded (INHERITED_FROM_DESKTOP_POST_AUDIT; my machine
  sum check 148 = 125+23 confirms consistency).
- Executor per-call ledgers for Phases A/B (10/15, 26/65) accepted as self-reports consistent with
  artifacts and PREFLIGHT/EXECUTION_LOG internal accounts (the QC/QC-repair historical values WERE
  independently recomputed).

---

## BUDGET (this QC)

```text
QC_TOOL_CALLS_PLANNED = 70 (preregistered, 00_CONTROL/CORRECTION_BUDGET.md)
QC_TOOL_CALLS_USED = 56 (including failed call #32 [PowerShell quoting] and instrument-retry call #35,
  counted per the COUNTING_RULE; 2 store-recount calls within the ≤6 Q4 bound; QC-owned writes included)
QC_WALL_MINUTES_PLANNED = 90
QC_WALL_MINUTES_USED ≈ 9 (QC start ≈09:29Z → report write ≈09:38Z; all QC artifacts timestamped
  09:33:47Z–09:36:58Z)
NO_CAP_EXCEEDED = YES (56/70 calls; ~9/90 min)
```

## FINAL VERIFICATION (at QC end)

```text
HEAD = b151d428fc46818bc3b84d8ca000d92caa2cd76b  (UNCHANGED; no stage/commit/push by this QC)
PORCELAIN = exactly the 6 expected untracked groups: the 5 preexisting foreign dirs + experiments/ +
            this new correction package (02_QC/raw additions are inside the new package — QC-owned paths)
TRACKED_MODIFICATIONS = 0 anywhere; AUDIT_ENTRYPOINT.md = untouched
HISTORICAL_PACKAGE_UNTOUCHED = YES (re-hashed anchors match; git clean)
ENTRYPOINT_UNTOUCHED = YES
DEFERRED_LEAD_4057 = RECORDED_NOT_EXECUTED (QC-confirmed)
```

## VERDICT

```text
QC_VERDICT = CORRECTION_RE_QC_PASS
```

Rationale: zero active E10 promotions (my census); all §9 invariants exact; no unauthorized RE (including
no 4057/0x0059AB12 work — Q7-verified absence); no budget cap exceeded (correction 36/80; this QC 56/70);
census provenance verified by my own recount (109/69 exact matches; 148 = 125+23; no fabrication); no
fourth oracle; historical package and entrypoint untouched; HEAD unchanged; no P0/P1/P2 defect introduced
by the correction. The two P3 findings (QC-P3-1, QC-P3-2) are documentation nuances with dispositions and
do not force FAIL per the order §13 verdict rule.

NEXT: per the order §§14–22, PE-MASTER proceeds (03_REPORT + disposition + entrypoint row + manifest +
staging + commit/push belong to the authorized later phases; this QC performed none of them).
