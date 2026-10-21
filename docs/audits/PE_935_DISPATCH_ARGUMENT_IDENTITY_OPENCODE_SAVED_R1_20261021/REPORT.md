# REPORT - PE_935_DISPATCH_ARGUMENT_IDENTITY_OPENCODE_SAVED_R1_20261021

RUN: new bounded saved-only research run, distinct clean authoring root, real direct workers, fresh same-model QC, sanitized publication phase. Launcher receipt existed legally (RECEIPT_ROOT LAUNCH_RECEIPT: PID 10916, CLI 1.18.18, scoped nask-glm medium); OUTPUT_ROOT was fresh and created by saved_guard start.

## Model gate (real, runtime-captured)

- Coordinator: ses_ea2456d4dfferKn2pZXAcTciE0, agent pe-master, model glm-5-3, provider nask-glm, version 1.18.18, PE_ROLE=SCIENCE_COORDINATOR.
- TOOL_SMOKE: ses_ea2448ae5ffedfWEn1AhWNGwLp (parent=coordinator, finish=stop, 1 completed tool), model glm-5-3-default; smoke input SHA256 independently re-measured A83C4832C3E126F2E69C6EC11DF6A050053F5B98D42A73488D5FE68A7439D629; T1-T4 expected fields all matching; nonce DAI_OC_20261021_A6F90D.
- MODEL_PROBE (auditor medium): ses_ea24419b8ffeWwYhgYHaVMETJm (finish=stop, 3 tools), model glm-5-3-default.
- Scoped merged registry verified via CLI: glm-5-3 and glm-5-3-default active with reasoningEffort=medium; glm-5-3-high/max exist but nothing selects them. REQUEST_EFFORT=NOT_OBSERVED, SERVER_EFFECTIVE_EFFORT=UNKNOWN.
- saved_guard check PASS before start (authoring 139+1 files bijection, 2297 pinned inputs). start --proof PASS -> event 000001_START.

## ETAP A - references to 0x0085A1B0

Census (metadata-only, whole pinned H5, operand format confirmed 0x-prefixed from admitted rows, so the zeros are format-valid):
- direct_callers = 0; direct_jumps = 0; address_mentions = 0 (CONTROL/NAV/NAV001-003).
- GA3 structural scan REF001 (reference_probe, REF_BEGIN before data): 0 slot targets and 0 vtable addresses equal 0x0085A1B0; census_complete=true (single saved dataset; not an exhaustive vtable census).
- 0x0085A1B0 IS a genuine function head: preceded by RET 0xc of the prior function (which does not call it); MSVC SEH prologue; epilogue RET 0x8.

DISPATCH_IDENTITY = UNRESOLVED_IN_ADMITTED_SOURCES (DATA_BARRIER). Candidate set: computed/relative pointer, dispatch/callback table outside the corpus, or no representation in the admitted sources. Per corrected postaudit CB-C2: zero direct CALLs does NOT prove virtual dispatch; no dead-code or liveness inference made.

## ETAP B - arg2 and real caller

No callsite exists in the admitted sources, so arg2 caller-frame provenance is a DATA_BARRIER (origin class: region boundary / resource / instance request / computed geometry - NOT_ESTABLISHED). In-body semantics established (CONFIRMED): arg2 = [EBP+0xC], >=36-byte structure (REP MOVSD ECX=9), float fields +0,+4,+0xC,+0x10 consumed; loop-count seeds ESI/EDI = 1 - conv(qword-constant x axis field difference); outer bound [ESP+0x18], inner bound [ESP+0x38] (written as [ESP+0x3c] under PUSH 0x20).

## ETAP C - role of the path

CONFIRMED mechanics (J001/J002): double loop over the arg2-derived extent; per-cell sample coordinates; transform CALL 0x00857830 per cell; output scaled by qword constants and quantized via 0x0095da40; dense fixed 4-byte records (u16 value at +0, byte +2 = 0, byte +3 = old AND 0x80) written with stride [desc+0xC]=4 into an ESI*EDI*4 buffer attached to a 0x20-byte descriptor (counts, stride, buffer) on the receiver; registration via 0x00857F90 lookup (result byte [+0x24] tested) + 0x006A8980 insert at receiver+0x48; temp buffer freed; arg1 dword pair consumed by 0x0093C460.

PATH_ROLE: H1 procedural region/grid buffer computation - STRONGLY_SUPPORTED (best-supported local role; falsifiers documented). H2 local resource transform and H3 world instance request transform - NOT_SUPPORTED_IN_SCOPE. No model-to-instance placement bridge. PLACEMENT_RELEVANCE: NO_FOR_NOW; priority of this path for building placement is LOWERED. Sample positions are NOT building positions. Optional modref (0x00853BD0/0x00857830) SKIPPED - the barrier is entry identity, not an opaque modref inside the admitted windows.

## Claims

CLAIMS.json DAI-01..DAI-08: 7 CONFIRMED, 1 STRONGLY_SUPPORTED (role label). QC001 (fresh pe-master-auditor, ses_ea23c214bffeIj0dYnUmdvjy55): PASS_WITH_CORRECTIONS; three packet-coverage corrections resolved by citing full-extract rows (1168759; 1168654/1168655; 1168637/1168639). Two W001 prompt row-label off-by-one transcriptions recorded in WORKERS/PROMPT_ERRATA.md and corrected in citations. All statuses PENDING_EXTERNAL_POSTAUDIT.

## Coverage

Checked fully: J001 (103 rows) + J002 (203 rows) admitted windows; census metadata for the whole pinned H5; GA3 scan; worker/QC answers byte-dumped and row-verified. NOT CHECKED (explicit): callee bodies listed in OPEN_TARGETS.json; bodies outside [0x0085A150,0x0085A560); non-literal reference representations (xref/relocation/pointer tables); any runtime behavior.

## Budgets

Charged: 24/64 bodies, 306/10000 listing rows (union 305), 19/400 calls, 8/64 candidates. Reference channel: 1/8 scans, 0/32 matches, 159410 reserved bytes. Nav: 3 metadata requests. Incidents: W001 row-label errata; W02 out-of-packet QA-fixture read (non-evidence, recorded).

## Conclusion

The main edge 0x0085A1B0 -> real references/vtable/caller -> arg2 origin is blocked exactly at entry identity: within the admitted saved sources the function has no representation of an entry mechanism. The studied path itself is a procedural grid/region buffer computation, not an established resource or instance-placement path. FIRST_MISSING_EDGE: real entry/caller of 0x0085A1B0, resolvable only by a saved non-literal reference representation (xref export covering computed references, relocation/pointer-value sweep, or dispatch-table census beyond GA3); runtime capture is out of scope this run. SEARCH_FRONTIER.json ranks the saved-only next steps.

WORLD_XYZ_RECOVERED=NO
HISTORICAL_PLACEMENT=NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM=UNKNOWN
CANONICAL_GATE_EFFECT=NONE
All statuses PENDING_EXTERNAL_POSTAUDIT. Publication (sanitized, additive) follows seal; publication is not scientific acceptance.
