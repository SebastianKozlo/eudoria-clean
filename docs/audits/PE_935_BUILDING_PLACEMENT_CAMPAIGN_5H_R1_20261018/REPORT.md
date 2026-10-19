# PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 — FINAL CAMPAIGN REPORT

- RUN_ID: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
- OUTPUT_ROOT: D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
- FINAL_REPORT_PATH: this file (REPORT.md)
- MODE: SAVED_EVIDENCE_RESEARCH_WITH_AGENTS_AND_SANITIZED_REPORT_PUBLICATION
- Authoring contract: D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_5H_AUTHORING_R1_20261018\CONTRACT.md (§13, §15, §16 govern closing; §14 publication)
- Materialized by: pe-master-auditor worker under direct PE-MASTER dispatch (closing materialization package, NO_NESTED_TASKS). Science synthesis content: verified this night by PE-MASTER (parent) and fresh pe-master-auditor QC sessions; this report cites the package reports and QC packs and does NOT re-derive the science (per dispatch instruction). Counters, gates and integrity facts below were independently recomputed from the on-disk artifacts by this materialization.
- Parent question (contract §1): how does the original 9.3.5 client join a concrete model resource to a world instance, and where does the instance transform come from? Anchor example: definition 4508 / resource 296445 / entry 296445.nif (scoped; not a claim that every scene object is this model or a static building).

## 0. Clock, control and stop facts (tool-derived; no manual times)

- T0 = 2026-10-18T21:13:23.544925Z (CONTROL/EVENTS/000001_START.json; wall_epoch 1792358003.5449252; monotonic 216672.437 s).
- Authorized window: total_seconds=18000 (300 min), science_seconds=16200 (270 min). Science cutoff = T0+16200 s = 2026-10-19T01:43:23.544925Z. HARD deadline = T0+18000 s = 2026-10-19T02:13:23.544925Z.
- The last science artifact sealed: P12_EXEC_R1 MANIFEST finalized 2026-10-18T23:47:20Z (reviews/P12_QC_R1 chronology recheck, MONOTONIC and CONSISTENT); the final joint QC session (P10+P11+P12) started 23:48:30Z. Science phase (execution + internal QC) therefore completed well before the 270-min cutoff.
- Control state at materialization (campaign_control.py status, read-only): 15 events (1 START + 12 ADMIT + 2 DENY); reserved 32 bodies / 1260 instruction rows / 153 edges / 32 candidates vs limits 96 / 12000 / 320 / 48; stopped=false (STOP executed after this report was finalized; the definitive final clock snapshot is the tool-written FINAL_STOP.json at the campaign root).
- Event chain integrity: all 14 previous_event_sha256 links independently re-verified by this materialization (14/14 MATCH); SHA256 of the last event 000015_ADMIT.json = 691BE254CF1B96CF219179E5EE7D729114CAA5E51E5C3A2D686DA2772BE04E67, equal to the tool status previous_sha. Ledger exports: BODY_ADMISSION_EVENTS.jsonl (17188 B, 14 lines = 12 ADMIT + 2 DENY; START not an admission event), BODY_ADMISSION_LEDGER.json (37243 B); both exported from CONTROL/EVENTS, not independent time attestation (their own origin note).
- STOP reason: SCIENCE_QUEUE_EXHAUSTED (meaningful authorized data/budget edges exhausted within the closed corpus; remaining sharp edges are corpus-coverage barriers or front-cap-denied; see §7 edge map and §8 next experiments).

## 1. MECHANISM — what the client statically does (per front)

### Front A — CAND4 closure (45-minute wall; capped as contracted)

Status: CLOSED_AT_FRONT_CAP. No factory/resource→actualS identity bridge exists in the admitted windows.

- 0x006B1C60 = factory class-bootstrap: [ECX]=0xA85454 vtable install + [0x00BA7220]=1 flag. Not a registration key/receiver map (P01; QC-passed).
- 0x006B1C80 = type-directed worklist walker: virtual vtable+8 typeinfo-style dispatch calls, static type nodes 0x00BA7218/0x00BA7210, children via +CC/+D4 (NiTArray layout). Its [EDI]=EAX store is pinned to a stack-local deque insert cursor — it cannot reach the outslot/V at the explicit-store level (P01, P02).
- Walker tail (P02): full store census over all 136 rows — NO [elem+8] store, NO receiver-pointer store, NO registration-key store, NO global store, NO ID values (no 0x42/66, no 296445 in either encoding). Leaf action = constant class-keyed SELECTION via 0x007B6C30 with key 0x00A85460 (= factory vtable 0xA85454+0xC) against the leaf elem and, on empty, its [+0x24] member. The key is a compile-time constant, not a per-resource ID.
- 0x007B6C30 (P03): entry guard + in-function dispatch (JNZ 0x007B6C4B continuation), ZERO writes in-region. Lookup-vs-register semantics: NOT_ESTABLISHED — the continuation 0x007B6C4B was DENIED (event 000011_DENY reason BAD_FRONT on a combined A+C request; event 000012_DENY reason FRONT_A_TIME_CAP on the A-only resubmission) → BACKLOG.
- 0x007D27B0 (A2b): NiStream teardown installing vptr 0xA8EC24; this-relative stores only; cannot write outslot/V. Instruction fact: it FREES the [this+0x148] holder → premise refinement for Q/V preservation: survival depends on retain/refcount, not holder liveness (P01).
- Type66+ID A → 296445: NOT_ESTABLISHED (scoped).

### Front B — SceneFeeder position producer

- Writer 0x005094C0 CONFIRMED: thiscall, one 4-byte argument = pointer to a 3-DWORD record, writes SF+34/+38/+3C, sets SF+28:=1 (dirty). No ID/parent/scale/rotation logic in the writer (P04; independently re-derived at QC).
- Callers (P04): R1/R2/R3 are update mechanisms (rotation constant {0,0,0} — NOT historical restores); R5 is a copy-initializer on a fresh receiver (rotation via getter 85C0F0 = real data); the AFTER-writer ID chain 43A550→72F580→72FCE0→6C0D50 was recorded and NOT admitted (out-of-window by design).
- Producers (P05): dominant route is COMPUTED — 0x0085BFA0 = affine-matrix getter (virtual slot +0x24 of [this+0x2C]; helpers 96cb20/96cf80; out-record = 3×3 + translation + 1.0), 0x0085C0C0 = slot +0x28 pass-through, 0x0085C0F0 = rotation derived, 0x0085C280 = gated slot +0xdc. Alternate route: 0x00862850 = RAW FIELD COPY [this+0x3C..0x44] (field semantics unknown).
- 0x00509070 REJECTED as an SF+30 link-setter: it is a 3-DWORD setter to [this+0x80..0x88]. The SF+30 node-role edge (root-instance vs internal NIF node) remains UNRESOLVED.
- Boundary result: update mechanism ≠ recovered data source. The transform-data boundary MOVED to the virtual slots of [this+0x2C] and to the 0x00862850 receiver class.

### Front C — definition→instance join (producer side CONFIRMED; consumer edge = corpus barrier)

- Standing bridge assimilated: record 4508 → A=296445 → 296445.nif CONFIRMED as a DEFINITION chain; world-instance identity NOT_ESTABLISHED.
- NEW this night — the {0x66,A} MODEL request formation chain is CONFIRMED end-to-end on the producer side (P11, P12, P07, P09, P06; all QC-passed):
  1. Keyed-table producers 0x006C27A0 / 0x006C27F0: keys from global tables M32[0xA857C8 + (w1+idx1*10)*4] / M32[0xA85804 + (w2+idx2*15)*4]; column word MOVSX-bounded (<10 / <15) from 0x0070ED80(0x1F/0x20)+0x0E/+0x0C; row index via 0x006B22D0 (P12).
  2. CALL 0x0043A550 (RB-tree registry lazy singleton) → CALL 0x0072F580 (templates.vfs RB-tree lookup) → registry record returned (body 1 CONFIRMED at in-window RET; body 2 STRONGLY_SUPPORTED — stack-forced tail out-of-window) (P12).
  3. Worklist: stack-local append buffer; producers reached via container field [EDI+8] (P11).
  4. Pump 0x006B6C9D = overflow/fallback arm (entered at JZ 0x006B6C88 when cursor==bound): per element valid-check 0x0072FCE0 → A-read getter 0x007CE1E0 ([ECX+0x08]) → constant 0x66 pair build via 0x0043C700 → callback 0x008BD720 registered via 0x0040B070 → enqueue via 0x0043E5B0 (P07).
  5. Parallel sites 0x006C3F98 / 0x006D44A4 register the same callback via 0x0040B070 + 0x006C3640 — the second enqueue path: queue object [+4]=tail cursor (+=8 per entry), [+8]=limit, 8-byte entries = the 2 DWORDs of the callback's returned pair (the projection callback reads elem+0x18/+0x1C) (P07, P09).
- 0x008BD720 (P06) = `LEA EAX,[ECX+0x18]; RET` — a side-effect-free leaf. The bridge-era "dispatching callback" premise is REJECTED_WITH_EVIDENCE.
- CONSUMER/DISPATCHER of the queue: NOT_FOUND — corpus-coverage data barrier: 0x0040B070, 0x0043E5B0, 0x0043C700 have ZERO body rows in the saved listing (CALL operands only; 17/1/10 sites; independently re-verified twice this night).
- The id2/class-20006-tag-6 composite-key property hypothesis is REJECTED_WITH_EVIDENCE at 0x00745A70: single-byte linear scan over 8-byte entries; any key component >255 (e.g. 20006) = guaranteed always-fail; key[3] — 0x00745BF0's first stack argument — is what reaches the byte-compare; the cursor is an absolute entry pointer (P10; B1/B4 settled at QC).
- No VFS-record-fed channel into the slot consumer was found in any admitted window (scoped negatives) — the FAMILY-P/T merge question is NOT_DECIDABLE at available levels (array populator unknown).

### Front D — historical values

Status: SCOPED_NEGATIVE_WITH_BOUNDS (P08; QC_PASS).

- NO historical world-instance placement values exist in the corpus.
- TRANSFORM_TABLE_CORRECTED.csv values are model-internal NIF node transforms of 296445.nif (tool-composed; own-parser block-map + errata recompute provenance; 30 rows, 16 default-zero rows). The 218757 scene-inspection transforms are composed FILE_SCENE_SPACE, cross-checked — not placement.
- Historical placement values would be server-session-delivered; the PE2/2003 network-handler f32 XYZ mechanism is UNVERIFIED for 9.3.5; session records do not exist in the corpus (FIRST_PEINST 0/6).
- Unsearched value-carrier classes (Strings/*.bnt encrypted interiors, .prt, media) remain data barriers — none is a known placement carrier for 296445.

## 2. INSTANCE_RESOURCE_JOIN

MODEL_INSTANCE_BINDING (campaign synthesis):

- Definition-side chain (registry → model resource id → MODEL request formation): CONFIRMED statically (§1 Front C). This is the strongest positive movement of the night: the {0x66,A} MODEL-request transport is now bounded from the keyed-table producers down to the enqueue sites, with the callback leaf pinned as a side-effect-free projection (elem+0x18/+0x1C → 8-byte queue entry).
- Instance-side chain (world instance identity, transform origin): NOT_ESTABLISHED. No evidence in any admitted window identifies which world instance consumes a {0x66,A} request or where its transform originates.
- Concrete proof behind the movement: P12 (producers + registry lookup RET), P11 (worklist append), P07 (pump arm + registration sites), P09 (second enqueue path), P06 (callback leaf semantics), all with fresh independent QC; plus the corpus-coverage census for the three zero-row transport callees.

## 3. HISTORICAL_VALUES

- No source transform values for any historical 296445 world instance exist in the saved corpus (Front D, SCOPED_NEGATIVE_WITH_BOUNDS; QC_PASS).
- The only float triplets found are (a) model-internal NIF node transforms of 296445.nif (definition-side, tool-composed) and (b) composed FILE_SCENE_SPACE inspection transforms — neither is placement.
- CURSOR_SOURCE_MEDIUM = UNKNOWN (unchanged; contract §9 requires a source-proven channel before any change).
- Session-scoped negatives are honest bounds, not absence proofs beyond the corpus: the unsearched carrier classes are data barriers, and none is a known placement carrier for 296445.

## 4. RECONSTRUCTION_VALIDATION

- No independent confirmation exists that any current reconstruction output reproduces a correct historical placement of 296445. WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT = NOT_ESTABLISHED.
- What the night DID validate is mechanism-level: the SceneFeeder writer semantics, the producer routes (COMPUTED via virtual-slot affine getters vs RAW FIELD COPY), and the {0x66,A} request transport producer side — usable as working dependencies for reconstruction engineering, not as historical truth.
- Per contract §12: publication is not a science gate; the final independent Desktop postaudit of the whole campaign remains PENDING.

## 5. Known/open edge map

| # | Edge | Front | State | Blocking class |
|---|------|-------|-------|----------------|
| K1 | factory/resource→actualS identity bridge (registration key, receiver, [elem+8] store) | A | REJECTED in admitted windows (P01, P02) | none — closed negative |
| K2 | 0x007B6C4B continuation: register-vs-lookup for the model-loader walker leaf | A | NOT_ESTABLISHED; DENIED (events 000011/000012) | front cap (BACKLOG) |
| K3 | Q/V survival premise: retain/refcount vs holder liveness | A | refined (0x007D27B0 frees [this+0x148]) | premise update, closed at instruction level |
| K4 | SF+30 writer / node-role (root vs internal NIF node) | B | UNRESOLVED (509070 rejected as link-setter) | next census needed |
| K5 | transform-data origin: virtual slots of [this+0x2C]; 862850 receiver class field semantics | B | boundary MOVED, not resolved | receiver-class census |
| K6 | {0x66,A} queue CONSUMER/DISPATCHER | C | NOT_FOUND | corpus barrier (40B070/43E5B0/43C700 zero body rows; saved decompiled FUN_0040b070 exists OUTSIDE the 967-file closed catalog in GHIDRA_GATE_00407270.txt — needs the human corpus-boundary decision) |
| K7 | class-20006 property writer census / 745A70 array populator | C | NOT_DECIDABLE at available levels | writer-side census design |
| K8 | FAMILY-P/T merge (file-fed property → slot consumer) | C | NOT_DECIDABLE | depends on K7 |
| K9 | historical placement value carriers (Strings/*.bnt encrypted interiors, .prt, media) | D | UNSEARCHED data barriers | corpus boundary; none a known 296445 carrier |
| K10 | world-instance identity for 296445 (instance-record channel) | C/A | NOT_ESTABLISHED | depends on K6/K7 |

## 6. Hypothesis table (resolved this campaign)

Positive (CONFIRMED unless noted):
- H-B1: 0x005094C0 is the SF local-translation writer with dirty flag — CONFIRMED (P04).
- H-B2: dominant SF position record producer route is COMPUTED (virtual-slot affine-matrix getter chain) — CONFIRMED (P05).
- H-C1: {0x66,A} MODEL request formation chain end-to-end on the producer side — CONFIRMED (body 2 of the registry pair STRONGLY_SUPPORTED; P06–P12).
- H-C2: 4508 → A=296445 → 296445.nif as DEFINITION chain — CONFIRMED (standing, assimilated).
- H-A1: 0x007D27B0 cannot write outslot/V at explicit-store level; premise refinement: frees the [this+0x148] holder → V/Q survival depends on retain/refcount — CONFIRMED (P01).

Negative / rejected:
- H-A2: registration area contains a factory/resource→actualS identity bridge — REJECTED in admitted windows (P01, P02; scoped negative).
- H-A3: 0x007B6C30 is get-or-create/register — NOT_ESTABLISHED (entry guard + in-function dispatch; continuation unread, cap-denied → BACKLOG) (P03).
- H-C3: bridge-era premise "0x008BD720 is a dispatching callback/thunk" — REJECTED_WITH_EVIDENCE (side-effect-free leaf) (P06).
- H-C4: id2/class-20006-tag-6 composite-key property hypothesis at 0x00745A70 — REJECTED_WITH_EVIDENCE (single-byte scan; >255 components always-fail) (P10).
- H-B3: 0x00509070 as SF+30 link-setter — REJECTED (3-DWORD setter to [this+0x80..0x88]) (P05).
- H-B4: 0x006B1C80's [EDI]=EAX store reaches outslot/V — REJECTED at explicit-store level (stack-local deque insert cursor) (P01/P02).
- H-D1: historical placement values exist in the saved corpus — REJECTED within scope (SCOPED_NEGATIVE_WITH_BOUNDS; session records absent; unsearched carrier classes are data barriers, not evidence of absence) (P08).

## 7. FIRST_MISSING_EDGE per front

- Front A: 0x007B6C4B miss-path store census (register-vs-lookup for the model-loader walker leaf — the A1 missing link; ~167 rows; denied by FRONT_A_TIME_CAP, event 000012 → BACKLOG).
- Front B: SF+30 writer/node-role + the 0x00862850 receiver-class field semantics ([this+0x3C..0x44] raw copy) — the transform-data boundary is now there.
- Front C: the queue CONSUMER/DISPATCHER of the 8BD720-registered {0x66,A} requests — corpus barrier (saved decompiled FUN_0040b070 exists outside the closed catalog; reading requires the human corpus-boundary decision, then admission).
- Front D: unsearched value-carrier classes (Strings/*.bnt encrypted interiors, .prt, media) — data barriers; none a known placement carrier for 296445.

## 8. Three best next experiments (DESIGNED_NOT_EXECUTED)

1. Corpus-boundary decision + admission: decode the saved FUN_0040b070 (GHIDRA_GATE_00407270.txt) → queue object → consumer census of the 8BD720-registered requests. Closes the {0x66,A} transport consumer edge (K6). Required input: the human's corpus-boundary decision, then admission of that file + listing windows.
2. 0x007B6C4B continuation (0x007B6C4B–0x007B6E4B): miss-path store census decides register-vs-lookup for the model-loader walker leaf — the A1 missing link (K2). Required input: front-A budget in a fresh campaign; admission ~167 rows, 1 body, ~12 edges.
3. Class-20006 property writer census + 0x00745A70 array populator: decides whether any file-fed property reaches the slot consumer — the FAMILY-P/T merge (K7/K8). Required input: writer-side census design; larger package (multiple bodies; needs its own admission plan).

## 9. Budgets — actual vs reserved vs limits

Campaign limits (contract §6): 96 bodies / 12000 instruction rows / 320 CALL sites (reserved as edges) / 48 candidate variants. Package limits: 20 / 2400 / 64 / 12.

Reserved (tool ledger, 12 admissions): 32 bodies / 1260 rows / 153 edges / 32 candidates — ALL within limits.

Actual (per-package counters, QC-rechecked; sums independently recomputed by this materialization):

| Package | bodies | rows | CALL | candidates | note |
|---|---|---|---|---|---|
| P01 | 3 | 236 | 19 | 4 | contract body entries were branch targets, not entries (P01-C8) |
| P02 | 2 | 136 | 23 | 2 | completes 006B1C80 |
| P03 | 1 | 14 | 0 | 2 | edges reserve 2 → actual CALL 0 (disclosed) |
| P04 | 5 | 291 | 47 | 4 | R5 window ends mid-body (disclosed) |
| P05 | 6 | 164 | 8 | 4 | DIRECT_ANALYST_FALLBACK |
| P06 | 3 | 92 | 11 | 4 | includes 1 disclosed unforeseen in-window body (0x008BD730), NOT used for claims |
| P07 | 4 | 148 | 10 | 4 | +15 rows vs reserve (148 vs 133), ALL inside admitted window (QC adjudication) |
| P08 | 0 | 0 | 0 | 0 | document assimilation (front D) — no body admission |
| P09 | 1 | 23 | 1 | 2 | edges reserve 4 → actual CALL 1 (disclosed) |
| P10 | 1 | 57 | 0 | 2 | edges reserve 4 → actual CALL 0 |
| P11 | 2 | 45 | 4 | 2 | retry 1; under reserve, honest |
| P12 | 2 | 48 | 10 | 2 | exact |
| **SUM** | **30** | **1254** | **133** | **32** | vs limits 96/12000/320/48 — ALL WITHIN |

- No refund sought for under-reserve packages (contract §6); the P07 overshoot is actual-vs-reserve row accounting only, adjudicated as no admission breach (reviews/P07_QC_R1, QC-P07-3: all 54 SR2 rows inside the admitted window ending 0x006B6D3E end-exclusive).
- The P06 bodies deviation (3 in-window vs 2 declared) is the disclosed INCIDENT-P06-I1: window-contained, no claims built on the unforeseen body, adjudicated compliant (reviews/P06_QC_R1).

**P2 FINDING (this materialization) — dispatch-prose counter discrepancy.** The closing dispatch prose stated actual totals "1254 rows, 136 CALL sites, 30 candidates". The per-package QC-rechecked counters sum to 1254 rows (match), **133 CALL sites** and **32 candidate variants** (both differ). Sources: packages/P0x_EXEC_R1/COUNTERS.json + reviews/P0x_QC_Rx/COUNTERS_RECHECK.json (all 12 packages re-summed independently by this materialization; P09's own COUNTERS disclose the exact "4 CALL vs 1 CALL" prose-rendering discrepancy — plausible mechanism for the 136 figure, PLAUSIBLE not CONFIRMED; no single mechanism identified for the 30-vs-32 candidates figure). Effect: NONE on any gate — under either reading all totals are inside the campaign limits (133 and 136 ≤ 320; 30 and 32 ≤ 48) — and no science claim depends on these aggregates. Correction applied in THIS report and in GATES.json: the ledger carries 133 CALL / 32 candidates as the counter-verified actuals. Revalidation predicate: re-sum packages/*/COUNTERS.json actual fields; expected 30/1254/133/32.

## 10. Dispatch/QC attribution

- Executor: pe-reconstruction executed P01–P04, P06, P08, P09 (first attempt), P10, P11 (retry 1; attempt 1 incomplete), P12.
- DIRECT_ANALYST_FALLBACK (parent, disclosed, §4-authorized emergency exception): P05 and P07 — two incomplete child attempts each, artifacts preserved, attribution recorded in the packages (P05/P07 COUNTERS "attribution" field).
- Fresh pe-master-auditor QC for every package: P01_QC_R1; P02_QC_R1 + P03_QC_R1 (joint session); P04_QC_R1; P05_QC_R2 (the R1 QC session was unavailable — recorded honestly; reviews/P05_QC_R1 contains only the attempt marker, left untouched); P06_QC_R1 + P05_QC_R2 (joint); P07_QC_R1; P08_QC_R1 + P09_QC_R1 (joint); P10_QC_R1 + P11_QC_R1 + P12_QC_R1 (joint).
- All QC verdicts: QC_PASS or QC_PASS_WITH_CORRECTIONS (process verdicts PASS or PASS_WITH_CORRECTIONS; P08 process PASS). Zero rejected overclaims across the campaign. Zero claims promoted to canonical standing.

## 11. Incidents and their adjudications

1. **INCIDENT-P06-I1** — unforeseen in-window body 0x008BD730 (3 bodies in window vs 2 declared). Adjudicated compliant: window-contained, disclosed at execution, NOT used for claims; QC_PASS with corrections registered (reviews/P06_QC_R1).
2. **P05/P07 child session failures** — two incomplete child attempts each; DIRECT_ANALYST_FALLBACK executed by the parent on the same saved-only contract with the same admission and limits (§4); honest attribution in package COUNTERS; QC recheck of retry/fallback attribution = HONEST.
3. **P11 attempt 1 incomplete** — session died after 2 files; retry 1 completed in a fresh session; prior-session CONTRACT/RUN_STARTED preserved byte-identical, retry marker RUN_STARTED_RETRY1.json added (reviews/P11_QC_R1 attribution recheck: HONEST).
4. **P12 navigation overdisplay** — disclosed; zero claims depend on it.
5. **QC-INC-1 (P01_QC_R1)** — one intermediate reviewer manifest write went to a typo'd path ('D:\Eudoria_Reconstruction\99_Audoria_Reconstruction_placeholder'); removed immediately, removal verified; no worker-pack/CONTROL/canonical/repo path touched; disclosed in reviews/P01_QC_R1/MANIFEST.json. An unrelated pre-existing placeholder file (created 2026-09-05) was observed and left untouched (UNRELATED_WORK_EXCLUDED).
6. **Estimated-timestamp defects** in several worker/QC docs — caught and repaired to the real clock before sealing, disclosed (e.g. P01 COUNTERS stamp correction; P09 worker's own disclosed-and-repaired timestamp-discipline defect, final state verified consistent; P11-QC-F1 stamp-ordering anomaly recorded as a finding for any future corrigendum). None load-bearing; no claim depends on the stamps.
7. **P07 row overshoot (148 vs 133 reserved)** — adjudicated as reserve-accounting overshoot with ALL rows inside the admitted window; no admission violation, no retroactive authorization needed (reviews/P07_QC_R1, QC-P07-3 wording correction registered).
8. **Dispatch-prose counter discrepancy (this materialization)** — see the P2 finding in §9; reported here as an incident of the closing synthesis, not of any sealed package.

## 12. Standing labels (unchanged by this campaign)

- WORLD_XYZ_RECOVERED = NO
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED
- CURSOR_SOURCE_MEDIUM = UNKNOWN
- CANONICAL_GATE_EFFECT = NONE
- MODEL_INSTANCE_BINDING = DEFINITION_SIDE_CONFIRMED_STATIC / INSTANCE_SIDE_NOT_ESTABLISHED (scoped; no global promotion — no STATIC_BUILDING_ROLE, no milestone claim)
- Per contract §16: even a strong XYZ candidate would require independent identity/provenance/coordinate-frame closure before any global promotion; none arose.

## 13. PROCESS/QC/PUBLICATION

- Integrity: 15 control events, hash chain 14/14 verified; 12 packages sealed with manifests (each QC re-hash + bijection PASS); every package has fresh independent QC; ledger exports present at the campaign root (identities in CAMPAIGN_ARTIFACT_INDEX.csv).
- ADMIT/DENY compliance: 12 ADMITs, each extraction within its admitted region (deviations: P06 incident and P07 overshoot, both adjudicated in-window); 2 DENYs respected and NOT converted (000011 BAD_FRONT; 000012 FRONT_A_TIME_CAP → BACKLOG).
- Boundaries: EXE_READ_BYTES=0; RUNTIME_ACTIONS=0; CONFIG_CHANGES=0; no game payload/VFS/BNT/NIF opened; frozen roots untouched; repo untouched by this campaign; no agent/skill/config mutations.
- Publication: **PUBLICATION_PENDING** — variant (b) of contract §15 (local seal first, then publication of the sanitized frozen projection). The publication package (PUBLICATION_ALLOWLIST.csv, EXCLUDED_ARTIFACTS.csv, redaction/provenance mapping, separate publication manifest, per §14) is a separate sequential action AFTER this seal; its receipt will be recorded OUTSIDE the sealed root in 99_Audits\PE_935_BUILDING_PLACEMENT_5H_PUBLICATION_RECEIPT_R1_20261018. No publication SHA may be appended into this sealed REPORT.
- Final independent Desktop postaudit of the whole campaign: PENDING (contract §12).

## 14. Terminal block (contract §16)

```
RUN_ID = PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018
RUN_STATUS = COMPLETED_SCIENCE_SEALED_STOP_EXECUTED
STOP_REASON = SCIENCE_QUEUE_EXHAUSTED (meaningful authorized data/budget edges exhausted within the closed corpus; remaining sharp edges are corpus-coverage barriers or front-cap-denied)
SCIENCE_VERDICT = PARTIAL_POSITIVE: producer-side {0x66,A} MODEL request formation chain CONFIRMED (definition side); world-instance join and historical transform origin NOT_ESTABLISHED (scoped negatives with exact bounds)
PROCESS_VERDICT = PASS (all 12 packages QC-passed; budgets within limits; incidents adjudicated and disclosed)
QC_ORIGIN = FRESH_INDEPENDENT_pe-master-auditor_FOR_EVERY_PACKAGE (P05: R1 session unavailable, recorded; R2 completed)
FRONT_A = CLOSED_AT_FRONT_CAP (no identity bridge; 007B6C4B continuation cap-denied → BACKLOG)
FRONT_B = WRITER_AND_PRODUCER_ROUTES_CONFIRMED; SF+30 NODE-ROLE UNRESOLVED; data boundary moved to [this+0x2C] virtual slots + 862850 receiver class
FRONT_C = PRODUCER_SIDE_CONFIRMED; CONSUMER/DISPATCHER NOT_FOUND (corpus barrier: 40B070/43E5B0/43C700 zero body rows; saved FUN_0040b070 outside closed catalog — human corpus-boundary decision required)
FRONT_D = SCOPED_NEGATIVE_WITH_BOUNDS (no historical placement values in corpus; data barriers documented)
WORLD_XYZ_RECOVERED = NO
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM = UNKNOWN
MODEL_INSTANCE_BINDING = DEFINITION_SIDE_CONFIRMED_STATIC / INSTANCE_SIDE_NOT_ESTABLISHED
CANONICAL_GATE_EFFECT = NONE
BUDGETS: reserved 32 bodies / 1260 rows / 153 edges / 32 candidates (limits 96/12000/320/48 — respected);
         actual 30 bodies / 1254 rows / 133 CALL sites / 32 candidate variants (per-package QC-rechecked counters, re-summed; P2 discrepancy vs dispatch prose 136/30 disclosed in §9)
CLOCK: T0 = 2026-10-18T21:13:23.544925Z; science complete ~23:47-23:55Z (P12 seal 23:47:20Z) << science cutoff 01:43:23.544Z; STOP within the 300-min window (final tool snapshot: FINAL_STOP.json)
TASK_DISPATCHES = 12 science packages (pe-reconstruction; P05/P07 DIRECT_ANALYST_FALLBACK disclosed) + 12 fresh QC sessions (joint where noted) + this closing materialization
CONFIG_CHANGES = 0
EXE_READ_BYTES = 0
RUNTIME_ACTIONS = 0
INCIDENTS = 8 (all adjudicated/disclosed; §11)
MANIFEST_IDENTITY = parent MANIFEST.json is written LAST by PE-MASTER after this seal, self-excluded; campaign artifact identities: CAMPAIGN_ARTIFACT_INDEX.csv (this materialization)
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018\REPORT.md
PUBLICATION = PUBLICATION_PENDING (variant (b) §15; receipt dir PE_935_BUILDING_PLACEMENT_5H_PUBLICATION_RECEIPT_R1_20261018 outside the sealed root)
```

## 15. Are we closer to building-placement, and on what concrete evidence?

Yes — on the producer side of the definition→instance transport. Concrete evidence: the keyed-table producers and their global key tables (P12, CONFIRMED at in-window RET), the worklist append path (P11), the overflow/fallback pump arm with its const-0x66 pair build and callback registration (P07), the second enqueue path and queue object layout (P09), the callback leaf pinned as a side-effect-free elem+0x18 projection (P06), plus the corpus census that locates the next missing edge exactly (queue consumer; saved FUN_0040b070 outside the closed catalog). What is NOT established: any world-instance identity, any historical transform value, and any coordinate-frame proof — the three things the human's question still needs (§2–§4). The remaining sharp edges are corpus barriers or cap-denied continuations, not unexplored in-corpus territory: the science queue was exhausted honestly.

— Materialized 2026-10-19T00:0xZ (real clock; final exact clock facts are the tool-written FINAL_STOP.json). pe-master-auditor, closing materialization package under PE-MASTER dispatch.
