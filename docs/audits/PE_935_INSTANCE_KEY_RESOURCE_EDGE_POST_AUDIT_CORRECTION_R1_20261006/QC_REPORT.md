# QC_REPORT — PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006

**QC scope:** SELF_CHECK (targeted, run-local; performed by the executor that
produced the correction — NOT an independent QC; no fresh-context internal QC
and no external Desktop re-audit of THIS package were performed in this phase;
PE-MASTER audits this package before persistence).

**QC time window:** 2026-10-06 04:27–04:40 local (preflight measurements
04:1x–04:27; Q15 final re-hash after the last package write). Instrument:
03_SCRIPTS/ledger_schema_qc.py (fail-closed; CSV schema + artifact-existence
layer only — it does NOT prove PCG semantics or physical provenance).

---

## Q1 — Identity and baseline: PASS (measured)

- LOCAL_HEAD = f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 — MATCH EXPECTED_BASE_SHA.
- origin/master (after `git fetch origin`, exit 0) = f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 — MATCH.
- Actual remote master (`git ls-remote origin refs/heads/master`) = f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 — MATCH.
- Working tree: zero tracked changes; 6 foreign untracked paths inventoried and
  preserved untouched (INPUT_IDENTITIES.md).
- Contract: 24,218 B / SHA256 EA86AA0897695C100D89BD68438318F6DDC9BD50DE28C7A6EDCC59ACF4ED61ED — MATCH.
- OUTPUT_ROOT did not exist at preflight (no collision).

## Q2 — Desktop post-audit identity: PASS (measured)

- REPORT.md = 14,545 B / SHA256 664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572 — MATCH.
- DESKTOP_POST_AUDIT = REQUIRE_CORRECTIONS; audited target f129fd5... == Q1 base.

## Q3 — Source package read-only: PASS (measured)

- Full re-hash census of all 36 source-package files taken BEFORE any work
  (INPUT_IDENTITIES.md baseline table).
- Re-hash after all correction work: ZERO diffs (see Q15).

## Q4 — FUNCTION_LEDGER_SCHEMA: PASS (measured)

`FUNCTION_LEDGER_CORRECTED.csv`: 1 header + 8 data rows, every row exactly 10
cells; header exactly the ten contract §6 columns in order; no STATUS column
(FUNCTION_NO_STATUS_COLUMN = PASS); ORD unique (1..8); zero DictReader
extra/null/missing cells; identity/evidence/cited separated; all prose fields
non-empty; every CITED_PHYSICAL_SOURCE cites >=1 existing source-package
artifact (traceability check on disk). Checker verdict PASS, exit 0.

## Q5 — EDGE_LEDGER_SCHEMA: PASS (measured)

`EDGE_LEDGER_CORRECTED.csv`: 1 header + 22 data rows, every row exactly 11
cells; header exactly the eleven contract §6 columns in order; EDGE_ID unique;
zero DictReader extra/null/missing cells; STATUS != CITED_PHYSICAL_SOURCE on
every row. Checker verdict PASS, exit 0.

## Q6 — DictReader extra/null cells: ZERO (measured)

DICTREADER_NO_EXTRA_NO_MISSING = PASS on both tables (restkey sentinel
`__EXTRA__` produced zero hits; zero None-valued fields).

## Q7 — STATUS/source separation: PASS (measured)

EDGE-only semantic gates (LEDGER_SCHEMA_QC.json):
- STATUS_VOCABULARY = PASS — every STATUS starts with a declared token
  (CONFIRMED / UNRESOLVED_IN_BUDGET / UNRESOLVED / EDGE RECORDED /
  NON-CANONICAL LEAD / UNKNOWN / NOT_CHECKED).
- STATUS_NOT_EVIDENCE_PATH = PASS — no evidence path can pass as STATUS.
- CITED_NOT_STATUS_TOKEN = PASS — no STATUS token can pass as
  CITED_PHYSICAL_SOURCE (swap-detection gate).
- IDENTITY_SOURCE_SEPARATION = PASS; CITED_EXISTING_ARTIFACT = PASS.
- FUNCTION ledger: its own declared identity/operation/role/availability
  checks PASS; the edge STATUS enum was NOT applied to prose fields
  (FUNCTION_PROSE_FIELDS_NONEMPTY = PASS).

## Q8 — MUT-A (extra cell): CAUSAL_FAIL (measured)

- MUT_A_FUNCTION (row ORD=1, extra cell appended): production SCHEMA_GATE
  REJECTED — exact failed predicates: ROW_WIDTH_EXACT, DICTREADER_NO_EXTRA_CELLS.
- MUT_A_EDGE (row E-GETTER, extra cell appended): production SCHEMA_GATE
  REJECTED — exact failed predicates: ROW_WIDTH_EXACT, DICTREADER_NO_EXTRA_CELLS.
- Clean baselines: PASS for both tables; the SAME production validator that
  accepts the clean tables rejected the mutants; the rejection is caused only
  by the schema predicates (the checker never consults manifest or Git state).
- Verdict: CAUSAL_FAIL (both table-specific mutants rejected).

## Q9 — MUT-B (missing cell): CAUSAL_FAIL (measured)

- MUT_B_FUNCTION (row ORD=1, last cell removed): REJECTED — ROW_WIDTH_EXACT,
  DICTREADER_NO_MISSING_CELLS.
- MUT_B_EDGE (row E-GETTER, last cell removed): REJECTED — ROW_WIDTH_EXACT,
  DICTREADER_NO_MISSING_CELLS.
- Verdict: CAUSAL_FAIL (both table-specific mutants rejected).

## Q10 — MUT-C (EDGE STATUS/CITED swap): CAUSAL_FAIL (measured)

- MUT_C_EDGE (row E-GETTER, STATUS <-> CITED_PHYSICAL_SOURCE swapped, width
  preserved): production SEMANTIC_SCHEMA_GATE REJECTED — exact failed
  predicates: STATUS_VOCABULARY, STATUS_NOT_EVIDENCE_PATH,
  CITED_NOT_STATUS_TOKEN, CITED_EXISTING_ARTIFACT.
- MUT-C was NOT applied to the FUNCTION ledger (no STATUS column).
- Verdict: CAUSAL_FAIL.

All mutations ran on TEMP COPIES (system temp dir, deleted after each
measurement); the clean corrected ledgers were never modified
(MUTATION_RESULTS.json). No unexpected mutant PASS occurred; had one occurred
it would have been recorded as UNEXPECTED_MUTANT_PASS, not CAUSAL_FAIL.

## Q11 — DPA2 history preserved: PASS (measured)

- Historical truth recorded: TOTAL_DETAILED_FUNCTIONS_MAX = 6;
  FUN_0064B1E0 = FUNCTION #7 FULL 27-BYTE BODY OBSERVED;
  ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL.
- Present decision recorded separately: PROCESS_EXCEPTION_AUTHORIZATION =
  HUMAN_ADJUDICATED_NOW; RETROACTIVE_PRIOR_AUTHORIZATION = NO;
  HISTORICAL_BREACH_PRESERVED = YES; SCIENTIFIC_CORE_EFFECT = NONE.
- The string "BUDGET RESPECTED" does NOT occur for the original run anywhere in
  this package; the historical sequence was NOT rewritten as if authorization
  preceded the breach; the historical labels
  ("PASS WITH ONE DISCLOSED DEVIATION" / QC_PASS / MASTER_ACCEPTED) are
  superseded as process-compliance statements (SUPERSESSION.md) while their
  byte-level technical QC results stay valid within their actual tested scope.
- TECHNICAL_QC and PROCESS_COMPLIANCE are recorded separately (DPA2).

## Q12 — DPA3 provenance: PASS (measured)

- PERSISTENCE_PHASE_SPLIT_SOURCE = NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE
  (no already-preserved source with time/identity exists in the authorized
  evidence set; none was fabricated; the chronology was not back-filled).
- PHASE_SPLIT_BEHAVIOR_CLASSIFICATION = ORCHESTRATOR_PHASE_SPLIT (the executed
  split is orchestration behavior on the recorded evidence, NOT
  DIRECT_HUMAN_INSTRUCTION).
- FINAL_PUBLICATION_AUTHORIZATION = PRESENT (the preserved verbatim human
  instruction DID authorize commit/push; commit f129fd5... remains authorized).
- Historical GOVERNANCE_DECISION.md NOT modified (read-only source package,
  Q15 zero diff).

## Q13 — P3 precision: PASS (measured, per-item)

- P3-1: measured 61-char State-A SHA string in the historical AMENDMENT 1
  (missing `239`) vs the full 64-char SHA in 01_RAW/GovernanceWriteTime.txt;
  transcription corrected in this package's GOVERNANCE_DECISION.md; NO claim of
  recovery of State-A bytes or the +25 B delta.
- P3-2: source row 2 FUNCTION_IDENTITY said vtable store @0x00528EA8; the same
  row's IDENTITY_EVIDENCE and BYTE_WINDOWS F00528E50_ctor_prologue (C7 06 B0 DC
  A7 00 @0x00528EA2; 89 9E A4 00 00 00 @0x00528EA8) plus Desktop P3-2 give the
  authoritative store VA 0x00528EA2; corrected in
  FUNCTION_LEDGER_CORRECTED.csv row 2.
- P3-3: source row 5 EXTENT ended at 0x0085620F; RET 4 = C2 04 00 occupies
  0x0085620E..0x00856210 (source QC_REPORT Q5 already used body
  0x00856190..0x00856210); corrected to inclusive 0x00856190..0x00856210 =
  129 B with the window limitation disclosed (BYTE_WINDOWS
  F00856190_mapinsert_full ends at 0x0085620F, omitting the final RET byte).
- P3-4: ">=3 different receiver kinds proven" replaced by the authoritative
  receiver wording (ClientMovableObject CONFIRMED / GameClient CONFIRMED /
  additional [EBX] form UNRESOLVED); allowed conclusion
  `SHARED +0x74 OFFSET READER — STRONGLY_SUPPORTED in examined census scope`
  (FUNCTION_LEDGER_CORRECTED.csv row 1).
- P3-5: the broad "No resource edge exists anywhere in the examined path"
  formulation is superseded by "No resource/template/model consumer was
  established in the examined bounded path."; the direct E8 negative is scoped
  to the measured five-address direct-E8 predicate
  {FUN_0072F580, FUN_006C9700, FUN_006CB6F0, FUN_006CB020, FUN_0043A550} in the
  decoded insert body (FUNCTION_LEDGER_CORRECTED row 5; EDGE E-M1-INSERT).
- P3-6: historical QC_GATES.csv G2 row width limitation recorded (8 naive
  cells vs 6 declared columns, caused by unquoted commas in "8,015,872 B");
  previous QC did NOT establish generic CSV schema validity; the artifact was
  NOT rewritten; its valid physical-byte results stay valid within their
  actual tested scope.

## Q14 — No unintended science diff: PASS (measured, item by item)

Required-unchanged conclusions vs the source run — all preserved:
1. Getter bytes `8B 41 74 C3` @0x00414130 = `mov eax,[ecx+0x74]; ret` —
   preserved verbatim (FUNCTION row 1; EDGE E-GETTER).
2. Six direct E8 census in the stated scope (0x004569D3, 0x00456BEB,
   0x0045723E, 0x0045A08B, 0x00528FD9, 0x008561AC; 0 E9, 0 dwords, 0 outside
   .text; indirect/inlined readers NOT claimed) — preserved verbatim
   (EDGE E-N1..E-N4, E-C1, E-M1; E8_CENSUS.json untouched).
3. Selected ClientMovableObject receiver (SAME_MOVABLE_OBJECT_PROVEN, 4-edge
   byte-pinned chain) — preserved verbatim (EDGE E-C1; FUNCTION rows 1-2).
4. GameClient different-object result (DIFFERENT_OBJECT for the three census
   sites) — preserved verbatim (EDGE E-N1..E-N3, E-GB1, E-GB2).
5. Map-identity role in the examined path (mgr1+0x10 hash_map, key=[value+0x74],
   value = the same instance) — preserved (EDGE E-M1, E-M1-PAIR, E-M1-INSERT;
   only the P3-5 scoping wording of the same measured negative changed).
6. SceneFeeder key pass-through evidence (no lookup in FUN_005247C0;
   [SF+0x14]=key; key -> FUN_0064B1E0 at the boundary) — preserved (EDGE
   E-C1-PUSH, E-E1-ABI, E-E1-CALL, E-E2-KEYSTORE, E-E2-EXTRADATA; FUNCTION
   rows 3-4).
7. resource/model edge NOT_ESTABLISHED (not converted to CONFIRMED nor
   REJECTED_GLOBAL) — preserved (SUPERSESSION.md status block).
8. WORLD_XYZ_RECOVERED = NO — preserved.
9. STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED — preserved.
10. HISTORICAL_INSTANCE_DATA_RECOVERED = NO — preserved.

Allowed changes used (contract §15 exhaustive list): schema repair (the two
corrected ledgers + all reconstructed fields), corrected metadata (P3-3
extent), corrected provenance (DPA3), corrected addresses/sizes/wording (P3-1,
P3-2, P3-4, P3-5), process-budget adjudication (DPA2), supersession/status
routing (SUPERSESSION.md). No new science claim appears in this package.

## Q15 — Source package hash diff: ZERO (measured)

Full re-hash of all 36 source-package files AFTER all correction work equals
the pre-work baseline census byte-for-byte (zero size/SHA diffs). The source
package is untouched by this run.

## Q16 — Forbidden work: ZERO (measured)

- No new PCG RE, Ghidra, disassembly, xref, function tracing, decoder,
  Gamebryo/OpenMW/NIF research, oracle execution, SceneFeeder research,
  FUN_007B68B0/FUN_007B6A80 analysis, ExtraData consumer research,
  resource/model tracing, AttachChild search, 0xA4 work, client runtime,
  network, VFS/BNT/NIF/ARK payload opening, XYZ recovery, static-building
  experiment, PE-MASTER qualification or milestone change was performed.
- No EXE byte reads were performed by this correction (records-only; EXE
  identity carried from the source package and the Desktop post-audit).
- No file outside OUTPUT_ROOT was written; AUDIT_ENTRYPOINT.md was NOT edited
  (proposed row in HANDOFF.md); foreign untracked paths untouched.
- Scratch/builder scripts live outside the repo (system temp), not in the
  package; no __pycache__ inside the package (verified in the final census).

---

## RECONSTRUCTION_MAP (DPA1 — how every corrected field was derived)

Rule applied: raw cell texts of the malformed source rows are PRESERVED
EVIDENCE; each logical field was assigned from (a) verbatim cells, (b) joined
cells where the un-quoted embedded comma split one logical field, or (c)
existing persisted evidence (FINAL_REPORT §7 status algebra = the
authoritative per-field table; FINAL_REPORT §6; BYTE_WINDOWS.txt windows;
sibling ledger rows) for cells ABSENT from the source serialization. No
invented provenance; every reconstruction cites its evidence below.

### FUNCTION_LEDGER_CORRECTED.csv (8 rows)

| Row | Field | Derivation |
|---|---|---|
| ORD 1 | EXTENT | join of raw C2+C3 (embedded comma in "[[00414130,00414133]]") |
| ORD 1 | IDENTITY_EVIDENCE | join of raw C6+C7 (embedded comma in "mov eax,[ecx+0x74]") |
| ORD 1 | OBSERVED_OPERATION | join of raw C8+C9 (embedded comma) — equals FINAL_REPORT §7 row 1 verbatim |
| ORD 1 | FINAL_SEMANTIC_ROLE | raw C10 with P3-4 wording correction (CONFIRMED/CONFIRMED/UNRESOLVED) |
| ORD 1 | other fields | raw cells verbatim |
| ORD 2 | all 10 fields | raw cells verbatim; FUNCTION_IDENTITY VA corrected per P3-2 (@0x00528EA2; source's own IDENTITY_EVIDENCE cell already said EA2; BYTE_WINDOWS F00528E50_ctor_prologue) |
| ORD 3-7 | OBSERVED_OPERATION | ABSENT from the 9-cell source rows (missing-cell defect class confirmed by the naive-parse shift the Desktop audit described); reconstructed VERBATIM from FINAL_REPORT §7 status algebra (the per-field table assigns exactly these OBSERVED_OPERATION values; consistent with the rows' own IDENTITY_EVIDENCE byte decodes and BYTE_WINDOWS windows) |
| ORD 3-7 | FINAL_SEMANTIC_ROLE | raw C6 (the "opis semantic role" cell; anchored by C7 = HISTORICAL_INPUT_AVAILABILITY and C8 = CITED_PHYSICAL_SOURCE right-alignment) |
| ORD 3-8 | HISTORICAL_INPUT_AVAILABILITY, CITED_PHYSICAL_SOURCE, EXTENT, BUDGET_ROLE, FUNCTION_IDENTITY, IDENTITY_EVIDENCE | raw cells verbatim (ORD 5 EXTENT corrected per P3-3; ORD 5 FINAL_SEMANTIC_ROLE scoped per P3-5) |
| ORD 8 | OBSERVED_OPERATION | ABSENT from the 9-cell source row; reconstructed from FINAL_REPORT §6 ("FUN_004157B0 (0x30-B head read only: the vtable store, for the GameClient classification)") + BYTE_WINDOWS F004157B0_head (C7 06 18 9F A7 00 @0x004157B8; 8B F1 @0x004157B2) + the row's own FUNCTION_IDENTITY cell |
| ORD 8 | FINAL_SEMANTIC_ROLE | raw C6 verbatim ("GameClient constructor (classification probe only)") |

### EDGE_LEDGER_CORRECTED.csv (22 rows)

| Row | Field | Derivation |
|---|---|---|
| 17 verbatim rows (E-GETTER, E-C1, E-C1-CALL, E-C1-STORE, E-E1-ABI, E-E2-KEYSTORE, E-E2-HOLDERSTORE, E-E2-NINODE, E-E2-EXTRADATA, E-E2-REG, E-M1, E-M1-PAIR, E-N1..E-N4) | all 11 fields | raw cells verbatim (well-formed 11-cell rows) |
| E-M1-INSERT | STATUS | raw STATUS with the P3-5 scoping of the same measured negative (five-address direct-E8 predicate; source FINAL_REPORT §1.2 lists the five addresses) |
| E-C1-PUSH (12 raw cells = 11 fields + 1 embedded comma) | TARGET_OR_DESTINATION_ARITHMETIC | raw C5 verbatim (push effect + callee arg order; mirrors sibling E-E1-ABI TARGET) |
| E-C1-PUSH | FIELD_REGISTER_VALUE | raw C6 verbatim (arg1=KEY arg2=&string; mirrors E-E1-ABI FIELD "arg1=KEY arg2=string") |
| E-C1-PUSH | RECEIVER_PROOF | join of raw C7+C8 (the one embedded comma; value identity + provenance of the pushed EAX) |
| E-C1-PUSH | PATH_CONDITIONS / STATUS / CITED | raw C9 / C10 / C11 verbatim |
| E-E1-CALL (10 raw cells; one field absent) | PATH_CONDITIONS | ABSENT from the source row (C8=STATUS, C9=CITED right-alignment confirmed the gap); reconstructed from existing evidence: FUNCTION_LEDGER ORD 3 IDENTITY_EVIDENCE ("alloc-fail JZ 0x00524816"), sibling E-E1-ABI RECEIVER_PROOF ("new-block alloc result (EAX) != 0 (JZ 0x00524816 skips ctor...)"), GHIDRA_DECOMPILES FUN_005247c0 conditional call |
| E-GB1 (10 raw cells; one field absent) | RECEIVER_PROOF | raw C6 verbatim ("return value = the receiver of census sites E-N1..N3" — receiver-flavored cell; C7=PATH/C8=STATUS/C9=CITED right-alignment) |
| E-GB1 | FIELD_REGISTER_VALUE | ABSENT from the source row; reconstructed from existing evidence: BYTE_WINDOWS F00401360_receiver_getter (A1 5C FE B9 00 @0x00401381 reads the slot), FUNCTION_LEDGER ORD 6 ("returns the object at [0x00B9FE5C]", 0x88 B, vtable 0x00A79F18), E-GB2/RTTI_PROBES.json (class proof) |
| E-GB2 (10 raw cells; one field absent) | RECEIVER_PROOF | ABSENT from the source row (C6=FIELD, C7=PATH, C8=STATUS, C9=CITED); reconstructed from existing evidence: BYTE_WINDOWS F004157B0_head (8B F1 MOV ESI,ECX @0x004157B2; C7 06 18 9F A7 00 @0x004157B8) + FUNCTION_LEDGER ORD 6 miss-path decode (PUSH 0x88; new @0x0040138F; ctor call FUN_004157B0 @0x004013A9) |
| E-XD (10 raw cells; one field absent) | RECEIVER_PROOF | ABSENT from the source row (C6=FIELD, C7=PATH, C8=STATUS, C9=CITED); reconstructed from existing evidence: BYTE_WINDOWS F0064B1E0_head (56 PUSH ESI; 8B F1 MOV ESI,ECX @0x0064B1E1) + E-E2-EXTRADATA (ECX=new(0x14) block, alloc non-NULL JZ 0x00509492) + FUNCTION_LEDGER ORD 7 |

Residual honesty note: for the four reconstructed cells (E-E1-CALL
PATH_CONDITIONS, E-GB1 FIELD_REGISTER_VALUE, E-GB2 RECEIVER_PROOF, E-XD
RECEIVER_PROOF) and the six reconstructed OBSERVED_OPERATION values, the
original per-cell serialization did not persist a distinct value; the
correction uses the existing persisted evidence cited above rather than
silent shifts of neighbouring cells, and flags this mapping here explicitly.
The E-C1-PUSH embedded-comma join position (C7+C8 -> RECEIVER_PROOF) was
determined by structural analogy with the well-formed sibling rows E-E1-ABI /
E-C1-STORE (TARGET = effect+arg order; FIELD = arg values; RECEIVER = value/
receiver identity+provenance; PATH = branch condition); all raw cell texts of
that row are preserved verbatim inside the corrected row.

---

## Raw measurement artifacts of this run

- LEDGER_SCHEMA_QC.json — machine results for Q4-Q7 (checker output).
- MUTATION_RESULTS.json — machine results for Q8-Q10 (temp-copy mutations;
  exact failed predicates per mutant).
- INPUT_IDENTITIES.md — Q1-Q3 baseline census (36 rows) and identities.

## Overall correction QC verdict

QC_OUTCOME = PASS (Q1–Q16 all PASS as measured above; both corrected ledgers
PASS the fail-closed schema QC; all five mutants CAUSAL_FAIL).
PUBLICATION INTEGRITY (separate from QC outcome): no blocker encountered in
this phase (base/remote identity stable, allowlist respected, source package
byte-identical, no unauthorized writes/staged paths, no new science, no
payload publication). Persistence (entrypoint row + manifest regeneration
including it + path-limited commit/push + remote verification) is NOT executed
in this phase — it belongs to PE-MASTER after its own audit of this package.
A QC PASS does not convert the superseded process-compliance verdicts of the
source run; ORIGINAL_PROCESS_BUDGET_COMPLIANCE stays FAIL (historical) with
PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW.
