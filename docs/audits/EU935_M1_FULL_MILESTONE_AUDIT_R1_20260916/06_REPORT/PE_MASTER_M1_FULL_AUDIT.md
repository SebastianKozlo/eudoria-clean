# PE-MASTER M1 FULL MILESTONE AUDIT - FINAL REPORT
# EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916

PE-MASTER-issued adjudication text, persisted verbatim by pe-master-auditor
(bounded PERSIST_PUBLISH contract; formatting only; no scientific claim added
or altered). ALL verdicts in this report are ADVISORY_PRE_QUALIFICATION
(PE-MASTER status PROVISIONAL_UNTIL_QUALIFIED; CANONICAL_GATE_EFFECT=NONE).

## 1. REPORT METADATA / RUN CONTRACT

- RUN_ID: EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916
- ASSIGNMENT_MODE: FULL_MILESTONE_AUDIT (Gate-B pre-check over the standing
  V4.1 deliverable lineage)
- RUN_CLASS: LOAD_BEARING; RUN_TYPE: FULL_MILESTONE_AUDIT / GATE-B PRE-CHECK
- Executor-of-record: PE-MASTER in-session audit; persistence by
  pe-master-auditor; NO_NESTED_TASKS
- Execution class: STATIC-ONLY - the client never ran; zero runtime
  experiments; zero renders; no patching of any original binary
- Package: docs/audits/EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916/
- No new science: this audit re-hashes, reconciles and classifies the standing
  records; it does not produce new measurements beyond the fresh identity
  pins recorded in SOURCE_INDEX (which are hashes of existing bytes, not
  measurements of game behavior).

## 2. AUDIT TARGET

- TARGET: EU935-M1 WORLD SURFACE FIDELITY.
- AUDIT START HEAD: 0187e18455081e58fc1f38ee36d974206483093d (== origin/master
  == ls-remote at audit start; verified). BASE_SHA: 0187e18455081e58fc1f38ee36d974206483093d
  (BASE == HEAD: this audit adds a package; it does not modify any prior
  scientific artifact).
- AUDIT SCOPE: the standing V4.1 deliverable lineage (the LIVE matrix + the
  UNRESOLVED record + the P0 execution queue verdicts + the retraction canon),
  reconciled against the physical sources and the implementation tree.
- GOVERNANCE SOURCE STATE: PROJECT_STATE.json ABSENT -> recorded as
  GOVERNANCE_SOURCE_ABSENT (finding F3, P3; recorded, not invented).

## 3. SOURCE PINS AND PHYSICAL IDENTITIES

All physical source pins were re-hashed fresh by PE-MASTER in this audit
session; the three V4.1 package identities were resolved from shorthand to
full hashes and independently re-hashed at persistence (all MATCH). The full
table: 00_CONTROL/SOURCE_INDEX.md. Key pins:

- Entropia.exe PCG_9_3_5 (9.3.5.6746), 8,015,872 B:
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 - MATCH
  (all M1 static-run pins).
- The DIFFERENT-ERA Entropia.exe (8,445,952 B):
  E706C7152FB4874AB73779AC5F18E1259BB4373EFC5235E9F4FCB32FF1A6243B - recorded
  to prevent accidental cross-era use (never for 9.3.5 address claims).
- Models.bnt C950A8C2... / Textures.bnt 61ACD13B... / VegetationClimates.bnt
  7B858401... (BOTH copies byte-identical) - MATCH.
- terrain.bnt (125,064,817 B): full SHA256 NOT_PROVIDED in the prior records
  -> THIS AUDIT RECORDS THE FRESH PIN
  95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990 (finding
  F4, P3).
- The 12-byte Textures\Terrain.bnt stub: byte content verified
  (00 00 00 00 00 00 00 00 42 4E 54 32); SHA256 recomputed at persistence:
  FC0168D5B7E993098B97812B4EDAAD51B578AEEC47F0E29605B494E09540171D.
- 50.bnt (JUL): A6E59EE07A51EAC06A3E75DA5421E5928D59EDED74F096DCAD04CE80ED01DA00
  (fresh pin); JUL-era Textures.bnt: 2EAE115958D3157FA62F8CBFBAC6F4BFB5C38A820F1D05F9248C4200C0208A56
  (fresh pin, era-labeled).
- V4.1 package identities (all MATCH): M1_GATE_DELIVERABLE_MATRIX_V4.md
  EC04FC47... (68,176 B); .json 003056AC... (78,096 B);
  EVIDENCE_MANIFEST_V4.json 9944925D... (134,472 B).

## 4. V4.1 RECONCILIATION

- 19/19 rows accounted; 0 silently dropped; 0 overwritten; 0 contradictions.
- MATCH = 16; SUPERSEDED_WITH_VALID_EDGE = 3 (rows 3, 8, 14).
- STILL_OPEN rows carry their own open markers (row 9 [P-CLIMATE]; row 10
  CELL CONTENT RECONSTRUCTION-ONLY; row 11 CONDITIONAL on the x87 model; row
  19 self-regression scope).
- Full row-level record: 01_RAW/V4_1_RECONCILIATION.csv.
- PASS predicate: every standing V4.1 row is accounted for with an explicit
  relationship (MATCH or SUPERSEDED_WITH_VALID_EDGE with its edge recorded),
  zero contradiction findings. RESULT: PASS (19/19).

## 5. UNRESOLVED RECONCILIATION SUMMARY

- 39 items classified (27 known-open A1..A27 + 5 honest limits B1..B5 + the
  7-item V3 open set C1..C7).
- STILL_OPEN (honest; recorded; none blocks Gate A/B): A1..A4, A6..A12,
  A15..A20, A22..A27, A13, A14, B1, B3, B4, C4, C6 - each is either RE-era
  work, an era-bounded placeholder, or a documented bound.
- STILL_OPEN-BLOCKED-UNKNOWN: A3 + A18 (cellstream exhaustive negatives), C5,
  C7 (x87, ENVIRONMENT_BLOCKED).
- STILL_OPEN-narrowed / NARROWED (valid edge): A5, B2, C3 (georef 8b8b106).
- SUPERSEDED_WITH_VALID_EDGE (closed at queue scope): B5, C1, C2
  (RUN-C/RUN-E executed).
- A21 (clean pesource NIF path): matrix delivered at queue scope; the full
  path open.
- Full record: 01_RAW/UNRESOLVED_RECONCILIATION.csv.

## 6. WHAT M1 CLAIMS (the 19-row deliverable)

The LIVE deliverable = the V4.1 matrix (EC04FC47/003056AC + the manifest
9944925D), 19 rows, one per charter section-13 dimension: TERRAIN_HEIGHT,
TERRAIN_GRID, TERRAIN_WORLD_TRANSFORM, TERRAIN_MATERIAL_RECORDS,
TERRAIN_TEXTURE_RESOLUTION, TERRAIN_BLEND_SEMANTICS, FOLIAGE_SOURCE,
FOLIAGE_MODEL_BINDING, FOLIAGE_BIOME_RULES, FOLIAGE_DISTRIBUTION,
FOLIAGE_SEED/RNG, WATER_SOURCE, WATER_REGIONS, WATER_LEVEL, WATER_TEXTURE,
WATER_MATERIAL, WATER_ANIMATION, PESOURCE_MOUNT, RUNTIME_INTEGRATION - each
carrying 9 fields in both formats (MD + JSON), with the era-bounded registry
(19 entries) and the honest-limits section binding. Statuses per the
reconciliation (§4); the claim-level ledger with per-row measured quantities,
denominators and independence: 01_RAW/CLAIM_LEDGER.csv (M1-CL-01..20).

## 7. WHAT EXISTS (verified)

- The V4.1 package on disk at
  docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ (matrix MD + JSON +
  EVIDENCE_MANIFEST_V4.json + UNRESOLVED.md) - all re-hashed this session and
  independently re-hashed at persistence (MATCH).
- The governance canon: PROJECT_OPERATING_MODEL.md (the §13 closure hard
  gate), the PE_ARCHITECT_DECISIONS_LEDGER ENTRY #9 (r185 canonical decision,
  APPLIED, supersedes the r169 pin; eudoria-web = frozen oracle), the
  CORRECTION_LEDGER, the PE_MASTER_REVIEW.md files of all queue runs.
- The implementation tree (independently re-verified on disk at this
  persistence): terrain/ pages - p0.html (heights), materials.html,
  materials_wsum.html, materials_confirmed.html, era_divergent.html,
  water_system.html, foliage_system.html, model_witness.html (the clean pages
  + the witness page); calibration/calibration.html; src/pesource/ and
  src/peworld/ exist; package.json pins three@0.185.0 and node_modules/three
  carries version 0.185.0 (installed). Consistent with the audited claim: the
  clean pages + model_witness.html exist on disk; src/pesource + src/peworld
  exist; three@0.185.0 installed.
- The physical corpora LOCAL-ONLY (sizes re-verified at persistence; identity
  metadata in SOURCE_INDEX; payloads never committed).

## 8. CONFIRMED LIST

V4.1 rows 1, 2, 4, 5, 6, 7, 12, 13, 15, 16, 17, 18, 19 (each per its own
recorded status and denominators - see CLAIM_LEDGER) plus the CONFIRMED
mechanism parts: row 3's engine facts (world/tile/scale constants; the
world-datum pin), row 8's binding mechanism + the original-direct witness,
row 9's record structure, row 10's mechanism + byte-locked arithmetic, row
11's identity + byte-locked operands (CONDITIONAL on the x87 model), row 14's
engine constant 10.0f. The x87 CONDITIONAL model itself is CONFIRMED as a
model (M1-CL-20).

## 9. STRONGLY_SUPPORTED / PLAUSIBLE

- Row 3 TERRAIN_WORLD_TRANSFORM: STRONGLY_SUPPORTED, narrowed by the georef
  run (the world datum pinned; the engine-side keying BLOCKED-UNKNOWN).
- Row 9 FOLIAGE_BIOME_RULES: PARTIALLY CONFIRMED (the [P-CLIMATE] selection
  PLAUSIBLE-UNVERIFIED - the shared-selector hypothesis).
- Row 14 WATER_LEVEL: CONFIRMED engine 10.0f, datum narrowed (the field-vs-tile
  mapping for the page remains labeled).
- heightScale 128 u16/m = STRONGLY_SUPPORTED runtime calibration (not an
  engine-extracted constant).
- The shared-selector hypothesis (climate selection) = PLAUSIBLE-NOT-CONFIRMED.

## 10. REJECTED / OVERCLAIMED

NONE standing. The retraction/supersession ledger enumerates the superseded
and retracted items (01_RAW/RETRACTION_SUPERSESSION_LEDGER.csv): the
'sequential terrain names' premise; ORIGIN_PERMANENT_ZERO; unconditional
W*0.01; the f0906b9 '300s clean run'; the naive sequential overlay mix; the
'raw u16 height==0 = water marker'; the defective 23D7742E pin; the
EAX-residue death theory; the historical verdict-cell echo items (governance
indexes only). No standing document claims 1:1 historical foliage placement
(the overclaim trap was checked - SELF_ADVERSARIAL_PASS.md item 5).

## 11. UNKNOWN / BLOCKED (none of these waived or papered over)

- x87 actual CW (ENVIRONMENT_BLOCKED; the conditional model documented).
- Cell-stream origin ([P-CELLSTREAM]; exhaustive negatives valid).
- Climate per-location selection ([P-CLIMATE]; exhaustive negatives valid).
- Engine-side tile keying mechanism (BLOCKED-UNKNOWN; the data-level
  filename-xy key CONFIRMED).
- Patcher-delivered grids 432502/459344 (era-bounded placeholders).
- Original-client visual parity (milestone-scope limit; human-gated post-M1).
- p3 seed input ([P-RNG-P3]; labeled).
- Rotation/variant candidates (identity rotation = the RE-faithful absence).
- dim2/dim4 semantics; special-row semantics; TDF min/max source; >4-material
  reduction.
- WAVES/SKY plane textures (MISSING locally; synthetic stand-ins labeled).
- JUL-era runtime semantics (the loader-absent era fact).

## 12. RETRACTIONS

See 01_RAW/RETRACTION_SUPERSESSION_LEDGER.csv (9 rows, each with
counterexample, correction, current status, dependents, blast radius and
current evidence). Retraction compliance verified at claim AND field level;
nothing retracted is cited as standing anywhere in this package.

## 13. BLAST RADIUS OF OPEN ITEMS

Per the dependency graph (01_RAW/DEPENDENCY_GRAPH.csv): all open items are
bounded to their own rows/contracts; NO open item invalidates a CONFIRMED
row. The x87 condition touches rows 10-11 labels only (already CONDITIONAL -
it cannot flip an accepted claim because the claims are already conditional).
The georef residue touches rows 3/14 (narrowed, with the engine-side keying
honestly BLOCKED-UNKNOWN). The cellstream negatives bound rows 9/10 (honest
[BLOCKED-UNKNOWN; RECONSTRUCTION-ONLY labels carried). The parity limit bounds
row 19's claim scope (self-regression; explicitly not original-client parity).

## 14. CLOSURE GATES (exact predicates quoted VERBATIM from POM §13)

The gate text below is transcribed BYTE-FAITHFULLY from
PROJECT_OPERATING_MODEL.md lines 270-295 (including that file's own mojibake
em-dash/§ sequences - preserved verbatim; see
01_RAW/CLOSURE_GATE_MATRIX.csv for the same text in the gate matrix).

**GATE A - VERBATIM REQUIREMENT:**

## 13. MILESTONE CLOSURE HARD GATE (A/B/C/D â€” no milestone closes without ALL four)

**A â€” EXECUTION QUEUE EXHAUSTED:** every P0 from the PE-MASTER M1 execution
queue (the ordered list: x87 CW measurement -> witness matrix + scrambled-texture
falsification -> georef/P-DATUM -> P-CELLSTREAM/P-CLIMATE) is executed and
post-audited, each ending `MASTER_ACCEPTED` or an honest `BLOCKED-UNKNOWN` with
the exhaustive-negative record. No P0 silently dropped; no P0 closed by wording.

GATE A RESULT: PASS - evidence: the queue records (design 57a8d96 verdict
PENDING design-review, superseded by execution attempts; automation run
1e0976b MASTER_ACCEPTED advisory with honest blocker; night aggregate
e858a41..bc6835f display-enum canon; retraction dd68724) = honest
BLOCKED-UNKNOWN (ENVIRONMENT_BLOCKED with exhaustive negatives); witness
matrix + scrambled falsification = MASTER_ACCEPTED (8c037c0 + 59b5b63;
PE-MASTER re-execution 6/6; 5/6 + F-1); georef/P-DATUM = MASTER_PARTIAL_PASS
advisory (answered at world-datum level; the engine-side residue honestly
BLOCKED-UNKNOWN); P-CELLSTREAM/P-CLIMATE = MASTER_ACCEPTED advisory with
honest BLOCKED-UNKNOWN + exhaustive negatives (0/27, 0/8,381 independently
reproduced by PE-MASTER; 26 containers/179,774 entries; 12-B stub
byte-exact). Measured result: 4/4 P0s executed-to-bound, 0 dropped, 0 closed
by wording. Failure condition: any P0 dropped or closed by wording - NOT
triggered.

**GATE B - VERBATIM REQUIREMENT:**

## 13. MILESTONE CLOSURE HARD GATE (A/B/C/D â€” no milestone closes without ALL four)

**B â€” INTERNAL CHAIN COMPLETE:** the FULL_MILESTONE_AUDIT + the complete gate
package (the LIVE deliverable matrix carrying the contract fields physically,
the evidence manifest, the retraction/open records) pushed + remote-verified;
the PE-MASTER pre-check = `MASTER_ACCEPTED` and PE-MASTER declares
`MILESTONE_CANDIDATE_FOR_DEEP_AUDIT`. The package passes the four permanent
controls (Â§16).

GATE B RESULT: PASS (advisory; upon this package's push+verify) - evidence:
THIS audit package (the V4.1 reconciliation 19/19; the UNRESOLVED
reconciliation; the LIVE deliverable matrix = V4.1 with all identities
re-hashed; the evidence manifest present; the retraction/open records
present; pushed + remote-verified). PE-MASTER pre-check = MASTER_ACCEPTED
(advisory). The four permanent §16 controls applied to the package: the claim
matrix (CLAIM_LEDGER), the changed-code/record read (the package is
newly-written persistence of PE-MASTER's text; the §19 entrypoint touch is
the only mutation of an existing file, with PRE_EDIT evidence), the evidence
re-hash (SOURCE_INDEX/EVIDENCE_INDEX), the retraction compliance
(RETRACTION_SUPERSESSION_LEDGER).

**GATE C - VERBATIM REQUIREMENT:**

## 13. MILESTONE CLOSURE HARD GATE (A/B/C/D â€” no milestone closes without ALL four)

**C â€” CROSS-ENGINE DEEP AUDIT (MANDATORY):** the human relays the package to
ChatGPT Desktop; the deep post-audit returns `MILESTONE_POST_AUDIT_PASS`.
`PARTIAL`/`REJECTED` enter the Â§6 correction cycle â€” the milestone stays open
until a PASS. The relay is NOT optional, NOT "rare", NOT skippable on cost
grounds; only the human's `EARLY_DESKTOP_ESCALATION` inverse (a human decision
to change this contract) can alter this.

GATE C RESULT: NOT_APPLICABLE_YET (an expected future governance stage; NOT a
scientific failure). The Desktop deep post-audit is MANDATORY next; the relay
is NOT optional, NOT skippable on cost grounds.

**GATE D - VERBATIM REQUIREMENT:**

## 13. MILESTONE CLOSURE HARD GATE (A/B/C/D â€” no milestone closes without ALL four)

**D â€” HUMAN FINAL DECISION:** the human, and ONLY the human, issues
`MILESTONE_CLOSED` (or `NEXT_MILESTONE_AUTHORIZED`). No agent verdict, no
package, no concurrence closes a milestone. Between C-PASS and D the project is
CANDIDATE-CLOSED, not closed.

GATE D RESULT: NOT_APPLICABLE_YET. Only the human issues MILESTONE_CLOSED or
NEXT_MILESTONE_AUTHORIZED.

Why non-circular, per gate: A = each queue verdict from fresh QC + PE-MASTER
physical re-execution, not from executor prose; B = this audit independently
re-hashed all pins and re-derived classifications; C = cross-engine by
construction; D = human authority.

## 15. THREE COVERAGES

CLIENT_KNOWLEDGE / RECONSTRUCTION_IMPLEMENTATION / HISTORICAL_GAME_RECOVERY
are reported per dimension SEPARATELY, never merged into one percentage.
Numeric coverage is quoted ONLY with its recorded denominator: 99.8613% =
24,474/24,508 (binding chain, era 9.3.5); 80.40% = 19,705/24,508
(name-anchored, OBSERVED class); 89.45% = 2,171/2,427 morph spans is an
M2-adjacent NIF metric - CROSS-REFERENCE ONLY, NOT M1 surface. Dimensions
without a defined denominator are marked NO_DEFINED_DENOMINATOR. Full table:
02_ANALYSIS/M1_KNOWLEDGE_IMPLEMENTATION_RECOVERY_MATRIX.md.

## 16. X87 DISPOSITION

X87_CW_STATUS = UNMEASURED / ENVIRONMENT_BLOCKED; X87_CW_M1_CLOSURE_BLOCKER
= CONDITIONAL (the conditionality is documented and binding; acceptance is a
human/Desktop decision); CONTRACT_BASIS = POM §13 Gate A + the V4.1 HONEST
LIMITS. PC=24 would break 14,104/229,376 real lerp values (6.15%) - it cannot
flip an accepted claim because the claims are already CONDITIONAL. The
real-display/GPU-P/physical-console experiment is a HUMAN DECISION (paths:
(a) real display env, (b) instruction-level Ghidra predicate trace H3, (c)
conditional-PC acceptance) - NOT ordered by this audit, NOT performed. No
patching of Entropia.exe was performed; no GPU experiments started. Full
record: 02_ANALYSIS/X87_RUNTIME_AUDIT.md; ledger row M1-CL-20.

## 17. CELLSTREAM DISPOSITION

CELLSTREAM_CLIMATE_STATUS = honest BLOCKED-UNKNOWN;
EXHAUSTIVE_NEGATIVE_RECORD_VALID = YES; GATE_A_CONTRACT_SATISFIED = YES.
Raw negatives verified: Parameters 0/27; Textures 0/8,381 (PE-MASTER
independently reproduced the entry-size census); 26 local containers /
179,774 BNT entries / 70 size-coincidence hits = the expected tail, ZERO grid
data (N-8); the 12-byte stub byte-exact (re-verified + re-hashed at this
persistence); 32 .vcl decode-verified; TDF @2112=308/@2116=16 era 9.3.5.
Full record: 02_ANALYSIS/CELLSTREAM_CLIMATE_AUDIT.md.

## 18. FOLIAGE DISPOSITION

Mechanism CONFIRMED (loader registration FUN_0041dae0 + the factory
@0x00420007; 45 RTTI classes; VCL 32/492/256; the grid/cell-record/spawn-loop
/RNG arithmetic byte-locked - 76/76 bit-exact; 463,141 platform samples, 0
mismatches; exhaustive domain proofs). Historical inputs NOT recovered: the
cell byte-stream content (RECONSTRUCTION-ONLY stand-in), the per-location
climate selection ([P-CLIMATE]), the historical placement/content - FOLIAGE IS
NOT 1:1 and no standing document claims it (verified: V4 rows 10/19 carry
RECONSTRUCTION-ONLY labels). Missing historical inputs do NOT violate the M1
closure contract (the V4.1 matrix honestly bounds them; the Gate A terminal
state is satisfied by the cellstream exhaustive negatives). Full record:
02_ANALYSIS/FOLIAGE_AUDIT.md.

## 19. DOWNSTREAM CONTRACT

02_ANALYSIS/M1_DOWNSTREAM_OUTPUT_CONTRACT.md is BINDING for later milestones:
the coordinate system (the mutable S singleton - no S==0 assumption; no
unconditional W*0.01), the terrain frame (the byte-locked datum; the
BLOCKED-UNKNOWN engine-side keying never silently assumed), the scale/origin
behavior, the height decode-model variants (consumers must state which), the
texture inputs/limits, the tile/cell interface, the vegetation
mechanism/limits, and the OPEN_LIMITS list of blocked unknowns later
milestones must not silently assume.

## 20. SELF-ADVERSARIAL PASS

Executed and persisted: 02_ANALYSIS/SELF_ADVERSARIAL_PASS.md. Summary: the
five most load-bearing claims (the height decode chain; the foliage RNG/scale
byte-locks; the Terrain_14 blend semantics; the world datum (+50.0, the
height field); the foliage-historical-placement overclaim trap) each carry
CLAIM | FALSIFIER | COUNTERCHECK | RESULT | IMPACT; all stand (with the
honest PARTIAL/CONDITIONAL labels where applicable); the negative check found
NO overclaim. Also recorded: era discipline verified; BLOCKED not waived; no
retracted claim feeds the conclusions; implementation success not
masquerading as semantics; the witness/falsification executed by RUN-C/RUN-E
with PE-MASTER re-execution.

## 21. M1 READINESS RESULT

M1_READY_FOR_HUMAN_CLOSURE_DECISION.

## 22. CANONICAL POM DECLARATION

PE-MASTER_DECLARES = MILESTONE_CANDIDATE_FOR_DEEP_AUDIT (advisory
pre-qualification; NOT milestone closure; ADVISORY_PRE_QUALIFICATION;
CANONICAL_GATE_EFFECT=NONE). The ChatGPT Desktop post-audit (Gate C) is
MANDATORY next; human closure only; NOTHING AUTHORIZES M2.

## 23. MINIMUM BLOCKERS

NONE scientific. The CONDITIONAL human-decision items (the x87 GPU-P vs the
conditional-PC acceptance) are DECISIONS, not defects.

## 24. NON-BLOCKING OPEN ITEMS

The OPEN_LIMITS list (01_RAW/OPEN_LIMITS.csv, 17 binding items): cell
byte-stream origin; climate per-location selection; engine-side tile keying
mechanism; patcher-delivered grids 432502/459344; x87 actual CW;
original-client visual parity; WAVES/SKY plane textures; JUL-era runtime
semantics (loader-absent era fact); TDF min/max source; special-row tile
semantics; dim2/dim4 semantics; >4-material reduction; rotation/variant
candidates; p3 seed input; clean pesource NIF path; P-UNITS bridge; noise
seed [P4].

## 25. NEXT ACTION FOR HUMAN

Relay this package to ChatGPT Desktop for the Gate-C deep post-audit
(expected verdict vocabulary: MILESTONE_POST_AUDIT_PASS / _PARTIAL /
_REJECTED), then make the human closure decision (Gate D). Nothing else is
authorized by this package: no M2 opening, no milestone closure, no new
science.

## 26. ENTRYPOINT HOUSEKEEPING (§19)

- PRE_EDIT SHA256 of AUDIT_ENTRYPOINT.md:
  D5F61F383E80FC0C375BDA244146A918612971EC986097E488D0C0952286DA94
  (byte-identical copy preserved at
  00_CONTROL/AUDIT_ENTRYPOINT.md.pre).
- POST_EDIT SHA256 of AUDIT_ENTRYPOINT.md:
  09DA50660376ED6363282CE10549EEFCB8D872DF4C932E68892D131349C52CA7.
- Exactly ONE cell modified (the PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916
  verdict cell: PENDING -> 'MASTER_ACCEPTED (advisory; supersession R2;
  G16R/G17R/G18R PASS - AMEND-019 persistence)') and exactly ONE row added
  (this audit's LATEST RUNS top row).
- rows_added=1, rows_removed=0, rows_modified=1 - verified via
  `git diff --numstat AUDIT_ENTRYPOINT.md` = 2 insertions / 1 deletion; the
  57 untouched rows byte-identical; the 58 -> 59 row count verified.
- Findings F1 (fixed this run) and F2 (recorded; out of the authorized
  single-cell scope) in §28.

## 27. PERSISTENCE

- PUBLICATION_COMMIT (FINAL_SHA):
  `e077562ea37e161bc958ff2bca891266131ac565` (pushed; at the publication
  moment verified: HEAD == origin/master == `git ls-remote origin
  refs/heads/master`, all three read e077562ea37e161bc958ff2bca891266131ac565;
  push range 0187e18..e077562).
- BASE_SHA: `0187e18455081e58fc1f38ee36d974206483093d` (BASE == the audit
  start HEAD; the publication commit is the only new commit on the branch).
- Changed path census (publication commit): 27 paths = 26 package files under
  `docs/audits/EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916/` + `AUDIT_ENTRYPOINT.md`
  (the §19 housekeeping touch: the only modified pre-existing file; 1396
  insertions / 1 deletion; the deletion = the single authorized verdict-cell
  line replacement in the NIF-correction row; the 2 pre-existing untracked
  roots `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` and
  `experiments/` remained untracked and unstaged - verified in the staged
  index before commit).
- Manifest counts: `06_REPORT/MANIFEST_SHA256.csv` = 25 rows covering every
  package file EXCEPT the manifest itself (the L12 self-hash exclusion
  precedent, documented here; 0 stale, 0 missing, 0 .pyc, 0 __pycache__);
  package total = 26 files (25 + the manifest).
- CONSISTENCY COMMIT: this §27 finalization + the regenerated manifest row for
  this report are persisted in the immediately following path-limited commit
  (2 paths: this report + the manifest; its SHA is the repo HEAD visible via
  `git log` at the end of this persistence run) and pushed with the same
  HEAD == origin/master == ls-remote verification. After that commit the
  committed state is internally consistent: every manifest row matches the
  committed file bytes (25/25 re-verified).

## 28. FINDINGS LIST

- **F1 [P3]** - the NIF-correction row verdict cell was stale (authored
  pre-adjudication, PENDING wording; the verdict lives in gates + review).
  FIXED per §19 this run: the cell now carries the adjudicated verdict
  (MASTER_ACCEPTED advisory; supersession R2; G16R/G17R/G18R PASS; AMEND-019
  persistence). PRE/POST hashes in §26.
- **F2 [P3]** - the night-aggregate row verdict cell remains PENDING
  (governance index inconsistency; its science was consumed and re-verified
  inside the accepted georef/x87 reviews). NOT fixed here - out of the
  authorized §19 single-cell scope. RECORDED (governance index only; no
  science effect; the retraction ledger row 9 carries it).
- **F3 [P3]** - PROJECT_STATE.json absent -> GOVERNANCE_SOURCE_ABSENT
  (recorded, not invented).
- **F4 [P3]** - terrain.bnt canonical full SHA256 pin NOT_PROVIDED in prior
  records - fresh pin recorded this audit:
  95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990.
- NO P0/P1/P2 findings.

## 29. CONTRACT COMPLIANCE AND DEVIATIONS

- PERSIST_PUBLISH contract compliance: PE-MASTER's adjudication persisted
  verbatim (formatting only); NO new scientific claims; NO verdict text
  altered; no Task dispatches (NO_NESTED_TASKS); historical packages
  READ-ONLY; only the authorized persistence roots touched.
- Deviations from the bounded contract: NONE (any deviation would be
  disclosed here). Administrative notes (not deviations): (a) the §14 gate
  text preserves the POM file's own mojibake sequences verbatim (byte-faithful
  transcription, disclosed); (b) the recovery-matrix table adds the
  world-transform/georef line so that all 19 V4.1 rows are covered (content =
  the row's own fields; disclosed in the file header); (c) this report is
  persisted in TWO path-limited commits (the package publication commit, then
  the §27 finalization + manifest-regeneration consistency commit) per the
  contract's own two-step instruction.
