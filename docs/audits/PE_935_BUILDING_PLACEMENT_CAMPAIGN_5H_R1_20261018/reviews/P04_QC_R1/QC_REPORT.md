# P04_QC_R1 — Independent Internal QC of packages/P04_EXEC_R1

RUN_ID: PE_935_P04_QC_R1_20261018 | Mode: INTERNAL_QC (pe-master-auditor, fresh session, NO_NESTED_TASKS)
Parent loop: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | Package under review: P04_EXEC_R1 (immutable, read-only for this run)
Admission audited: A0af4119f1ccf | Pinned source SHA256 re-verified independently: 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB (50,780,146 B)
QC started: 2026-10-18T21:57:45Z | QC deadline: 2026-10-18T22:20:00Z
Contract basis: CONTROL/CONTRACTS/P04.json (hash-identical copy in pack verified) + parent CONTRACT.md sections 5, 6, 8, 12.

## 0. Naming map

Dispatch naming R1–R4 (callsites) = worker naming R2–R5. Worker R1 = writer body 0x005094C0. This report uses the worker's region ids (R1 writer, R2 0x006A36F0, R3 0x0067B4F0, R4 0x0067C560, R5 0x0067C7C0).

## 1. What this QC did (same-instruction requirement, contract §12)

I analyzed the SAME instructions the worker extracted: all five extracts are **byte-identical** to the pinned saved listing at their declared line ranges (R1 145735–145743, R2 607713–607747, R3 564107–564180, R4 565392–565467, R5 565584–565680) — verified line-by-line against the pinned source, plus full 17-artifact re-hash/bijection, independent frame-arithmetic rederivation, independent counter recount, independent navigation grep of the writer's callsites, and independent reproduction of all three negative controls. Navigation grep of `CALL 0x005094c0` returned exactly 12 hit lines (addresses only); no un-admitted body was opened. My full read log and NOT_CHECKED list are in RECHECK_NOTES.json.

## 2. Accepted claims (with evidence levels)

| Claim | Worker level | QC verdict | Basis (independent) |
|---|---|---|---|
| C1 writer signature: thiscall, one 4-byte pointer arg (RET 0x4) to 3-DWORD record; writes SF+34/+38/+3C; byte SF+28:=1; no return; no ID/parent/scale/rotation logic | CONFIRMED | **ACCEPTED CONFIRMED** | R1 rows 145735–145743 re-derived instruction-by-instruction; RET 0x4 balanced against exactly one pushed arg at all four callsites (607731, 564127, 565402, 565642); single-pointer deref chain +0/+4/+8 excludes the three-scalar-args model |
| C2 callsite @0x006A3727: receiver [caller+0x18]; record &F+0x3C 12 B; no in-body producer; getters 85C280(out=&F+0xC)/85BFA0(out=&F+0x18) both fit; rotation {0,0,0} const | CONFIRMED | **ACCEPTED CONFIRMED** | frame baseline F−4 re-derived (LEA offsets 0x10→F+0xC, 0x1c→F+0x18, 0x40→F+0x3C all reconcile); no store to F+0x3C..F+0x47 in 35 rows; dual geometry +0x30/+0x24 both exact |
| C3 callsite @0x0067B52E: receiver [caller+4]; record &F+0x3C; getters 862850(arg1)/85BFA0([caller+0]); [caller+0xC]→004150F0 with f32(‖v‖·q[0x00A7AF80]) AFTER writer; ID semantics honestly UNVERIFIED | CONFIRMED | **ACCEPTED CONFIRMED** (flow claim only) | F−8 baseline (post-guard PUSH EDI) re-derived; FPU chain independently re-walked: computes v0²+v4²+v8² → sqrt → scale → 004150F0 with EAX=[ESI+0xC]; writer @564128 precedes all of it |
| C4 callsite @0x0067C584: only preceding out-callee is 85BFA0([caller+0], out=&F+0x18) — discriminating witness; stale-frame V3 not excluded | CONFIRMED | **ACCEPTED CONFIRMED** | R4 window re-read: 85bfa0@565400 → writer@565404; 862850/509070/4150F0 all post-writer; no in-body store to record slot; V3 legitimately open |
| C5 callsite @0x0067C8A8: receiver freshly created in-frame via factory [0x00A75A38]→00401360→00485050→0048CBB0→005247C0; record = RET of 85C0C0(this=arg1, out=&P+8); rotation = RET of 85C0F0 (real data); AFTER-writer ID chain arg2→[arg2]→43a550→72f580→72fce0→6C0D50 (0x130 record); window truncated mid-body | CONFIRMED | **ACCEPTED CONFIRMED for the core statement** — with frame-annotation corrections (§3.1) | factory chain, getter pair, call order, guards, cdecl ADD ESP,4, boundary JZ 0x0067C921 and JMP 0x0067C923 all verified from rows 565584–565680; no FLDZ in R5 (rotation real) |
| C6 record = bare 12-byte transform-shaped triple; NO resource-ID/instance-ID/parent/rotation channel in any admitted callsite; rotation is a separate method (509510) with separate arg; ID-shaped values flow AFTER the writer into 004150F0 / 43a550-chain, never into the record | STRONGLY_SUPPORTED | **ACCEPTED STRONGLY_SUPPORTED** | call ABI re-derived at all 4 callsites; writer reads only [arg]/[arg+4]/[arg+8]; premise "float-shaped ≠ XYZ provenance" preserved (transform-SHAPED claim only) |
| C7 dominant producer hypothesis: 85BFA0 out-tail at +0x24 (translation row of 12-float buffer); R4 discriminating witness; R2/R3 alternate 4×4-row geometry | PLAUSIBLE / CONDITIONAL | **ACCEPTED PLAUSIBLE / CONDITIONAL** (level appropriate) | slot arithmetic verified; requires un-admitted 85BFA0 extent ≥0x30 — premise explicitly flagged by worker; cannot be closed in this admission |
| C8 R2/R3/R4 = update/copy mechanisms (rotation constant zeros — cannot be historical restores); R5 = copy-initializer (fresh receiver, position+rotation copied from arg1 getters); none promoted to recovered data source | STRONGLY_SUPPORTED | **ACCEPTED STRONGLY_SUPPORTED** | FLDZ falsification scan independently reproduced (exactly one FLDZ per R2/R3/R4 writing the 509510 arg triple; none in R5); premise "update mechanism ≠ data source" preserved |
| C9 NEGATIVE (window-scoped): no attach/parent evidence in the five windows; SF+30 never written in-window; candidate link-setter 509070 un-admitted; root-vs-internal-node UNDETERMINED | CONFIRMED negative / NOT_ESTABLISHED | **ACCEPTED** (negative stands, window-scoped only) | independent grep: zero `+0x30]` stores in all 5 extracts; worker explicitly scopes the negative to the window and does not extend it program-wide |
| C10 scoped result: producer identified up to the getter boundary (85BFA0 dominant / 85C280-862850 ambiguous / 85C0C0 return); variants V1–V4 enumerated; 12 static writer callsites inventoried by navigation, 8 un-admitted NOT read | CONFIRMED | **ACCEPTED CONFIRMED** (as scoped result) | my own navigation grep returned the identical 12 addresses (4 admitted + 8 un-admitted exactly as in SOURCE_PINS.json); no out-of-admission semantic read detected anywhere in the pack |

Standing labels re-checked in MANIFEST/HANDOFF: WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN, CANONICAL_GATE_EFFECT=NONE — **unchanged, no promotion performed**. All four contract premises preserved and enforced in claim wording.

## 3. Corrections (factual errors found; none flips a claim verdict)

### 3.1 **P1 — R5 frame-map arithmetic errors in MEMORY_AND_IDENTITY.json / CLAIMS.json C5 / REPORT.md §3**

Four slot annotations in the R5 (0x0067C7C0) frame layout are arithmetically wrong. The pack's own operative baseline is ESP = P−0x14 (P = entry ESP − 0xE4, after the 5 prologue pushes EBX/EBP/ESI/EDI/EAX-cookie — this same baseline is used correctly by the worker for the arg slots, local1, local2 and the state byte, which I verified all reconcile).

- **(a) this-slot**: claimed `P+0x14: slot holding this (written 0067C80F)`. Correct: `MOV [ESP+0x34],ESI @0067C80F` at ESP=P−0x14 (deterministic — no intervening call exists between the prologue pushes and this store) → slot = **P+0x20**. The worker subtracted 0x20 (double-counting the 3 pre-SUB SEH pushes) instead of 0x14.
- **(b) 0x00733340 receiver**: claimed `0x00733340(this=&(P+0x14) slot holding this)` — i.e. the SAME slot as (a), speculated as "wrapper-object shape, +0 = this". Correct: `LEA ECX,[ESP+0x38] @0067C90A` at ESP=P−0x14 (under the pack's own stated callee-pops premise, C2 premises) → receiver = **P+0x24**, a DIFFERENT slot 4 bytes above the this-store (P+0x20); nothing is stored at P+0x24 in-window before the call. The "wrapper-object, +0 = this" speculation has a **false premise and must be withdrawn** (downgrade to UNVERIFIED). Downstream hazard if left uncorrected: the next package admitting 0x00733340 would debug the wrong slot.
- **(c) alloc-pointer slot**: labeled `P-0x14 (P+0x00): 0x130-allocation pointer`. Correct: `MOV [ESP+0x18],EBP @0067C8FA` at ESP=P−0x14 → slot = **P+4** (the label is also internally contradictory: P−0x14 and P+0x00 are different addresses).
- **(d) SEH node**: claimed `SEH node at P+0xDC` / `FS:[0] := P+0xDC`. Correct: `LEA EAX,[ESP+0xEC] @0067C7EE` at ESP=P−0x14 → node base = **P+0xD8**; P+0xDC is the handler FIELD inside the node (consistent with PUSH 0x009F9784 landing at P+0xDC and the old-FS value at P+0xD8). The worker used a 4-push baseline here (omitting the second cookie PUSH EAX @0067C7ED).

Skutek (effect): purely evidence-text/frame-map layer of the AFTER-writer chain; the load-bearing content of C5 (factory chain, 85C0C0/85C0F0 returns, ordering, guards, truncation) is verified correct from the extract rows. Poprawka (fix): the frozen worker pack stays untouched (immutable); these corrected values are authoritative for any consumer of P04 results and should be folded by the parent into the next package's context / a corrigendum note. Revalidation predicate: recompute the three slot addresses from rows 565591/565606/565629/565668/565672 at the single consistent baseline ESP=P−0x14.

### 3.2 **P2 — parent-side provenance note: EVENTS 000006 region encoding**

EVENTS/000006_ADMIT.json encodes the admitted region as a single range `va_begin 0x005094C0 / va_end_exclusive 0x0067C921`, which does **not** cover the admitted subregion 0x006A36F0–0x006A375C (0x006A36F0 > 0x0067C921). The worker's read of 0x006A36F0 IS authorized (P04.json `admitted_regions` + the event's own `body_entries` + the question text all include it) — **no worker violation** — but a future mechanical audit relying only on the event's single-range field would misfire an out-of-admission violation against R2. Poprawka: parent should note the multi-subregion encoding when exporting the admission ledger; no package change.

### 3.3 **P2 — premise refinement: aliasing sentence rigor**

MEMORY_AND_IDENTITY.json states flatly "No in-window path can pass receiver==record". This is rigorous for R2/R3/R4 (record = the callee's own fresh frame slot; a pre-existing object-field pointer cannot address a frame created after it, and no in-window instruction writes the receiver value to F+0x3C — I verified both). For R5 the record is a callee-returned pointer, so receiver==record is not provable in-window; it rests on the already-flagged V4 premise (85C0C0 returns &P+8 or an arg1-internal pointer) plus arg1≠receiver. Poprawka: treat the R5 disjointness as premise, not fact. No claim depends on it (tested counterexamples in RECHECK_NOTES.json §K).

### 3.4 **P2 — process note: per-extract metadata placement**

Contract §6 asks that each extract "podaje source SHA, numery linii, VA, package/admission ID i SHA ekstraktu". The extracts carry line numbers and VA in-content; source SHA / admission ID / extract SHA live in SOURCE_PINS.json / artifact_index.csv / MANIFEST.json (package level), not embedded in each extract file. Satisfied at package level in this run; recommend a small header line inside each extract in future packages to remove the ambiguity.

## 4. Rejected overclaims

**NONE.** Specifically checked and NOT found:
- no XYZ/world/meters/map-orientation claim (premise preserved; "transform-shaped" wording only);
- no "historical placement restored" claim (rotation-zeros falsifier documented and reproduced);
- no root-instance vs internal-node determination (C9 stays NOT_ESTABLISHED);
- no promotion of the update/copy mechanism to a recovered data source;
- no "exclusively virtual" exclusion claim (12 static callsites inventoried; 8 honestly left unread);
- no equality assertion for qword [0x00A7AF80] vs the 0.01 factor (data address explicitly not read);
- no semantic read outside admission (extract ranges map 1:1 to the five subregions; all out-of-window targets flagged unread);
- SF+30 negative correctly bounded to the window (not extended program-wide).

The only factual defects are the §3.1 frame-map arithmetic errors — evidence-text errors, not overclaims of the question's conclusions.

## 5. Precise remaining edge (verified as accurate)

1. **Byte-level producer of the position record** — read semantics/extent of 0x0085BFA0 (R2/R3/R4; R4 = discriminating witness) and the R2/R3 alternates 0x0085C280/0x00862850, plus the R5 pair 0x0085C0C0/0x0085C0F0. This closes V1/V2/V3/V4 and decides scene-graph-internal vs external-intake reading. (Requires new admission; HANDOFF priority 1–2 correct.)
2. **Node-role identity edge** — 0x00509070 (candidate SF+30/NiNode link setter, body un-admitted) and secondarily 0x00509190 / 0x006A34A0. Root vs internal NIF node remains UNDETERMINED.
3. **R5 spawn/copy path continuation** — 0x0067C7C0 continuation (JMP 0x0067C923 + epilogue), 0x006C0D50 (0x130-record ctor with lookup result), callers of 0x0067C7C0.
4. **8 un-admitted writer callsites** (0x004B335E, 0x00527BA8, 0x00527BF0, 0x00528317, 0x00529020, 0x005F62EA, 0x0067B8E8, 0x006A3A2D) — may pass an ID-bearing record to the writer; the admitted four do not.
5. **Data barriers** — qword [0x00A7AF80], constant 0xA7957B, factory slots [0x00A75A38]/44/5C/40: data addresses; code-only listing cannot resolve; corpus lookup or barrier.

## 6. Process checks (contract §12 minimum)

- **Re-hash/bijection**: 17/17 non-manifest files on disk = 17 manifest entries; all sizes+SHA256 identical (recomputed). CONTRACT.json copy == CONTROL/CONTRACTS/P04.json (A42CBDFB…232E9). PASS.
- **Key arithmetic/def-use from independent read**: re-derived for all five windows (RECHECK_NOTES.json §B–§F) including full FPU ||v|| chain and R5 SEH frame. PASS with §3.1 corrections.
- **Alias/lifetime counterexample**: provided (§3.3 + RECHECK_NOTES §K). PASS.
- **Body and CALL counts**: 5/5, 291/291, 47/47, 4/4 exact; 28 unique targets (24 direct + 4 indirect) reproduced. PASS.
- **Admission and negative-scope check**: no out-of-admission semantic read; SF+30 negative independently reproduced and confirmed window-scoped. PASS (with §3.2 parent-side encoding note).
- **Chronology**: ADMIT 000006 21:49:18Z → contract/source pin verifications 21:49:20/26Z → RUN_STARTED 21:49:38Z → MANIFEST 21:56:35Z < hard stop 22:25:00Z. Consistent; no retroactive authorization. PASS.
- **Provenance limitation (disclosed, not a defect)**: the worker session's tool-execution logs were not persisted; executed-ness of tools/extract_subregions.ps1 is evidenced by the byte-identical extract outputs against the pinned source and the pinned tool hash, not by an independent execution log.

## 7. Verdicts

- **QC_VERDICT: QC_PASS_WITH_CORRECTIONS** (process verdict: **PASS_WITH_CORRECTIONS**).
- The package is usable as a working dependency in this campaign after the §3.1 corrections are carried forward by the parent (frozen pack itself remains untouched and immutable).
- QC_ORIGIN: INDEPENDENT (fresh pe-master-auditor session; no authorship overlap with the P04 specification or execution).

## 8. Files of this review pack

RUN_STARTED.json (first filesystem action of this run) · RECHECK_NOTES.json (line-numbered rederivations, full-read log, NOT_CHECKED) · COUNTERS_RECHECK.json (independent recount) · QC_REPORT.md (this file) · MANIFEST.json (LAST, self-excluded).
