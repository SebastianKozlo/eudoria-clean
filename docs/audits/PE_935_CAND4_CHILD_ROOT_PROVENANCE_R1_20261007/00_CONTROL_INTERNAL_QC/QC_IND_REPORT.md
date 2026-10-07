# QC_IND_REPORT — INDEPENDENT INTERNAL QC of PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

- QC_RUN_ID = PE_935_CAND4_CHILD_ROOT_PROVENANCE_INTERNAL_QC_R2_20261007 (this independent QC)
- ASSIGNMENT_MODE = INTERNAL_QC (PE-MASTER direct dispatch to pe-master-auditor; NO_NESTED_TASKS; STATIC-ONLY)
- QC_SCOPE = INDEPENDENT_INTERNAL_QC_CAND4_CHILD_ROOT (LOAD_BEARING depth, fresh context)
- AUDITED_PACKAGE = docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/ (28 physical files)
- REPO = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean; BASE_SHA = HEAD = d65fa12e5bae4e9aab291c3cc7815b1822e41cff (re-verified by me at QC start and QC end; zero tracked modifications; AUDIT_ENTRYPOINT.md untouched vs BASE)
- EXE = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe — MY OWN measurement: 8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH the pin.
- CONTRACT = C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_PROMPT_REVIEW_20261007\OPENCODE_CAND4_CHILD_ROOT_REVIEWED.md — MY OWN measurement: 18,159 B / SHA256 57249511611ADFA68161D9F2363DCB9831BFF36C9C913B59C83251B5D8C17568 — MATCH. Read in full (375 lines) before this QC.
- METHOD: ALL measurements below are MY OWN: my own PE mapper (parsed from the raw PE headers — image base 0x400000, sections .text/.rdata/.data/.tls/.rsrc; no executor tooling imported), my own x86-32 sequential decoder (table-driven, written in this QC; NO capstone), my own rel32 arithmetic, my own .NET/PowerShell SHA-256 re-hash of the manifest (implementation independent of the executor's Python hashlib), my own git blob-identity method for the historical packages. My four QC scripts + this record set live under 00_CONTROL_INTERNAL_QC/.

## QC_VERDICT

**QC_PASS_WITH_FINDINGS** — 5 findings, ALL P3 (records-precision / census-note class); ZERO P1/P2. Every
load-bearing byte claim, the edge census, the budget ledger, the four §9 controls, the §8 status algebra,
the PREREGISTRATION timing, the manifest bijection and the governance boundaries were independently
re-verified and PASS. The findings are annotation/cross-reference precision defects and one
records-transparency note; none falsifies a load-bearing claim; none requires reopening science. The
edge-budget exceedance (24 > MAX 8) is a PROCESS finding honestly disclosed by the run itself
(ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION = NO) — verified as disclosed,
not re-adjudicated here.

## 1. Own byte re-pins (dispatch item 2a–f) — ALL PASS

- (a) FUN_006C66D0 body: MY OWN read @0x006C66D0 = `8B 41 68 C3`; MY OWN ModRM decode: 0x41 = mod01 /
  reg=000(EAX) / rm=001(ECX) -> **mov eax,[ecx+0x68]; ret** (thiscall, ECX = this). It is NOT
  `8B 46 68` (mov eax,[esi+0x68] would require ModRM 0x46). Extent 0x006C66D0..0x006C66D4 RESOLVED:
  terminal C3 + 12× CC padding 0x006C66D4..0x006C66DF + aligned next entry 0x006C66E0 = `56` (push esi).
  All three callers re-verified by my own rel32 arithmetic: 0x0050A34B/0x0050A39D/0x0050A3AF -> 0x006C66D0.
  GETTER_OPERATION = DIRECT_FIELD_GETTER; ARKMODELMANAGER_CHILD_FIELD_OFFSET = 0x68 — CONFIRMED.
- (b) RTTI (my own walker, vtable[-1]->COL->TD+8): 0x00A855D0 -> COL 0x00AA6C58 ->
  `.?AVArkModelManagerMain@@`; 0x00A85A08 -> COL 0x00AA6CD8 -> `.?AVArkModelManager@@`;
  0x00A864B8 -> COL 0x00AA7770 -> `.?AVArkModelResourceInstanceRef@@` — all MATCH (incl. the claimed
  COL VAs). Vtable data reads: derived slot2 = 0x006C0FD0, slot3 = 0x006C19B0; base slot2/3 = 0x008E0110
  (both) — MATCH. Ctor vtable stores 0x00A855D0 @0x006C0D9B / 0x00A85A08 @0x006C8FAB — MATCH.
- (c) producer chain — every pin re-verified from EXE by my own reads:
  base-ctor NULL write `89 5E 68` @0x006C8FD3; [+0x6C]=0 @0x006C8FE3; flag [+0xEC]=0 @0x006C9014;
  lazy `cmp [esi+0x68],0` @0x006C8B34; trigger `E8` @0x006C8B3A -> 0x006C6F60; producer guard
  `cmp [esi+0x6C],0` @0x006C6F88; validity E8 @0x006C6F97 -> 0x0072FCE0; both empty-string-key pushes
  `68 7B 95 A7 00` @0x006C6FB5/@0x006C6FD3 (key 0x00A7957B = 0x00; "Entropia" @0x00A7957C — verified);
  getter-A E8 @0x006C6FF6 -> 0x007CE1E0; pump E8 @0x006C6FFC -> 0x006C9700 (cdecl cleanup
  `83 C4 10` @0x006C7001); store `89 46 6C` @0x006C7008; installer call E8 @0x006C7049 -> 0x006C6780;
  writer read `8B 78 04` @0x006C67BE; THE WRITER `89 7E 68` @0x006C67E2; incref `01 5F 04` @0x006C67E7;
  decref `01 69 04` @0x006C67D4; zero-destroy dispatch `8B 01 / 8B 50 04 / FF D2` @0x006C67D9..DE —
  ALL MATCH. All 56 byte pins and all 23 rel32 recomputes of 01_RAW/PINS_AND_REL32.txt re-verified by my
  own mapper/arithmetic: 56/56 + 23/23, ZERO mismatches.
- (d) named-lookup roots: receiver `8B 4E 68` @0x006C67EA + `push 0x00A859F8` @0x006C67ED + call
  0x007B6C30 @0x006C67F2; receiver again @0x006C6833 + `push 0x00A8547C` @0x006C6836 + call
  0x007B6C30 @0x006C683B; strings "ArkTexture\0" @0x00A859F8 and "ArkAnimation\0" @0x00A8547C verified —
  the stored child IS used as a named-lookup root for both constants. CONFIRMED (conditional lookups;
  existence not guaranteed — honestly stated by the run).
- (e) join window 0x0050A3B7..0x0050A3F8 — MY OWN per-instruction decode: the ONLY EDI-writing
  instruction in the window is the head `mov EDI, EAX` @0x0050A3B7; `push EDI` present @0x0050A3D7
  (arg of FUN_0050A1E0) and @0x0050A3F6 (THE join child argument); the four intervening calls
  (0x0050A3B9->0x006C0F90, 0x0050A3CF->0x006C10B0, 0x0050A3D8->0x0050A1E0, 0x0050A3E4->0x005246E0)
  and the slot-41 dispatch `FF D2` @0x0050A3F7 verified. CALLER SIDE IS CLEAN — CONFIRMED. The four
  callee bodies remain unopened (STRONGLY_SUPPORTED, ABI = support not proof — the honest §7 fallback
  stands).
- (f) my own sequential decode of all 6 opened extents reproduces every raw-record listing address
  (subset verification: 100% of within-extent listing addresses are instruction starts in MY walk);
  extents verified by terminal RET + CC padding + aligned next entries (12/2/10/6/14 CC bytes
  respectively; FUN_006C6780 window ends mid-instruction at 0x006C6844 with tail bytes
  `0F 84 BE 00` — exactly the honest PARTIAL/UNRESOLVED claim).

## 2. EDGE ACCOUNTING — independent reconstruction (dispatch item 3)

- MY OWN boundary-safe CALL walk of the 6 analyzed extents: getter 0 + ctor 1 + base-ctor 2 + lazy 5 +
  producer 13 + installer-window 5 = **26 CALL instructions** — EQUALS the executor's "26 CALL
  instructions in the 6 analyzed extents, 100% covered".
- Ledger census (my independent CSV parse): 24 ANALYZED_NEW + 7 RAW_VISIBLE_ONLY + 7 REPIN_PRIOR_SCOPE +
  27 OUT_OF_ANALYZED_EXTENT = 65 rows — EQUALS the declared census.
- Exact bijection: the 26 in-body ledger rows (19 ANALYZED_NEW + 7 RV) biject 1:1 with my 26 walked
  CALLs — zero missing, zero extra.
- **INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24** (5 caller-side units E-01..E-05 with new callee/gate
  semantics + 19 in-body non-RV calls) == ACCOUNTED_EDGE_COUNT = 24. **MATCH.**
- No semantic analysis hidden under RAW_VISIBLE (lesson J2): all 7 RV rows have an EMPTY
  NEW_INTERPRETATION field and an explicit NOT_COUNTED_REASON; the reports rely on NO pure
  never-analyzed RV/NEIGH target outside NOT_CHECKED/NEIGH/GAP/census/negation contexts (my sweep,
  with manual adjudication of the 4 raw-text hits: all benign census/NOT_CHECKED enumerations).
- The exceedance is EXACTLY 24 (not more): 24 > MAX 8, 16 past the stop line, as disclosed. The
  stop-before-exceeding rule was factually NOT honored in execution (process FAIL) and
  RETROACTIVE_PRIOR_AUTHORIZATION = NO is recorded verbatim in the ledger header, FINAL_REPORT §4,
  CLAIM_MATRIX CL-14 and HANDOFF. SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET.
- Unit-key uniqueness verified: zero duplicate (caller_start_VA, callsite_VA) among the 24 counted rows.

## 3. Budget census (dispatch item 4) — verified within/over as declared

- bodies 6/6 (the 6th = FUN_006C6780 PARTIAL: the partial opening honestly consumes a body unit — the
  preregistration declared that rule upfront; extent UNRESOLVED past the window, nothing claimed past it);
- writers 2/6 (W1 NULL reset + W2 value producer) + 3 explicit gaps (GAP-1 creation-chain internals;
  GAP-2 FUN_006C8BB0; GAP-3 off-path writers out of scope by governance) — the achieved-in-scope rule
  honored, NO global census (verified: no writer-search artifacts exist beyond the two);
- hops 2/3 (H-1 WRAPPER_CONTAINS; H-2 UNRESOLVED relation; H-3/H-4 SAME_OBJECT moves correctly NOT hops);
- candidates 3/3 (ctor reset; producer chain; FUN_006C8BB0 alternative — declared NOT_CHECKED gap);
- PREREGISTRATION timing VERIFIED by physical mtimes: PREREGISTRATION.md 11:02:49Z < first raw decode
  11:12:10Z < ledgers 11:15–11:16Z < controls 11:19Z < QC 11:24–11:28Z < HANDOFF 11:28:22Z <
  MANIFEST_SHA256.csv 11:28:59Z (manifest LAST — the every-write-after rule physically honored at
  package time).

## 4. Controls CTRL_1..4 (dispatch item 5)

qc_controls.py read to EOF (216 lines). Each control is ONE checker, clean PASS -> mutated FAIL, same
code path, correct cause (verified by reading AND by MY OWN INDEPENDENT REPLICAS on my own byte reads):

- CTRL_1 PASS (my replica PASS): the adjacency-only (NiControllerSequence) mutation trips the checker's
  REJECT_MODEL_ADJACENCY_ONLY branch — adjacency-only rejection is genuinely tested; the REAL child
  input is honestly classified POLICY_ONLY (evidence-absence of the §6 legs, no detection claim).
- CTRL_2 PASS (my replica PASS): clean = the real writer pair (store [esi+0x68] + read [eax+4]);
  mutated = the REAL foreign-field store `89 46 6C` (+0x6C instance cache) -> store_ok = False —
  the containment predicate fires on the correct cause.
- CTRL_3 PASS (my replica PASS): clean = the real getter `8B 41 68` ([ecx+0x68]); mutated = the REAL
  foreign accessor `8B 81 20 01 00 00` ([ecx+0x120], verified by my own read) -> FAIL — correct bytes
  of a foreign field do not qualify as provenance of THIS getter.
- CTRL_4 PASS (my replica PASS): clean = the real window (chain intact); mutated = the synthetic EDI
  clobber `8B 3D D0 D8 B9 00` @0x0050A3DD -> "EDI clobbered" FAIL — the child-identity predicate breaks
  as required; the record honestly notes the checker covers the CALLER side only (the real chain stays
  STRONGLY_SUPPORTED, NOT CONFIRMED).
- Fixtures are marked SYNTHETIC_MACHINERY_TEST_ONLY; synthetic PASS is not claimed as PCG science.

## 5. §8 status algebra (dispatch item 6) — literal, no promotion

CHILD_EVIDENCE_COMPLETE = FALSE is CORRECT: CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
(≠ CONFIRMED_MODEL_DERIVED — GAP-1 [instance+4] identity + GAP-2 alternative producer honestly cap it);
CHILD_VISUAL_ROLE = UNRESOLVED (no positive §6 proof); CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED
(≠ CONFIRMED — four intervening bodies unopened; ABI is support, not proof); EXACT_PARENT =
CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried, scoped to EXAMINED_ACLD_PLUS_18_SF_INSTANCE).
=> CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND — the chain never advances past its weakest
required edge. JOIN_OPERATION = STRONGLY_SUPPORTED remains the ceiling: FUN_007BF470 NOT opened (all
mentions are prohibition/ceiling contexts — verified by my sweep). Zero CMO↔ACLD transfer (all CMO
mentions are no-transfer/scoping contexts — verified). MY OWN sweep: no active
SCIENCE_PASS/CONFIRMED-overclaim tokens anywhere (all 8 SCIENCE_PASS mentions are negation/policy/
machinery contexts).

## 6. §11 prohibitions (dispatch item 7) — honored

No runtime (STATIC-ONLY throughout), no payloads opened, no ExtraData/FUN_007B68B0 work (mentions are
prohibitions + one prior-canon string-confirmation read of "ArkSceneFeeder" @0x00A7D444 — a string
constant, not an ExtraData structure analysis), no FUN_007BF470, no transform semantics, no XYZ/paging/
network, no global atlas. Oracles honestly NOT_USED: my bounded search CONFIRMS no OpenMW tree on the
local disk; the Gb12 identities re-measured by me MATCH (NiNode.cpp 33,897 B / 38C7A1DE…, NiAVObject.cpp
33,215 B / 72E08371…); NO oracle-based mechanism claim exists anywhere in the package (see F-QC-C for the
one inaccurate availability-justification sentence).

## 7. Manifest, encoding, historical packages (dispatch item 8) — verified

- 28 physical package files; MANIFEST_SHA256.csv self-excluded = 27 data rows; AUDIT_ENTRYPOINT.md
  explicitly OUT of this phase's scope, noted in the manifest header (persistence regenerates).
- MY OWN re-hash by the .NET SHA-256 implementation: 27/27 size+SHA256 MATCH — zero mismatch.
- Bijection exact (zero missing/extra/duplicate); ROW_COUNT = 27 header matches.
- Encoding: ALL files UTF-8 no-BOM, LF-only, strict-decodable — zero violations.
- Historical packages read-only — MY OWN method: P1 = 49/49 and P2 = 27/27 tracked-at-BASE files present
  and git-blob-identical to d65fa12e (zero mismatches); BOTH aggregate SHA-256 claims of
  INPUT_IDENTITIES §3 INDEPENDENTLY REPRODUCED by me (recipe: sorted "repo-relative-path lowercase-sha256"
  lines, LF + trailing LF): P1 = AB21CBC3…BE65B5B ✓, P2 = 80AB81F5…AE21A164 ✓.

## 8. Governance (dispatch item 9) — consistent

GOVERNANCE_DECISION.md §1 preserves the verbatim human authorization of 2026-10-07: exactly ONE run per
the reviewed contract file, RUN_ID and EXPECTED_BASE_SHA matching, full bounded scope + the contract's
internal QC/persistence/commit/push, explicit NON-authorization of every §11 extension, producer/writer
coverage = achieved-in-scope-only with explicit gaps (no global census), BLOCKED on preflight failure,
HARD STOP after execution+publication, NEXT_EXPERIMENT_AUTHORIZED = NO — all elements present and
consistent with the parent's characterization of the authorization. The phase-boundary adjudication
(ORCHESTRATOR_PHASE_SPLIT: this executor = science + controls + internal QC + package; NO entrypoint
edit, NO commit/push this phase; proposed entrypoint row in HANDOFF only) is recorded from the dispatch
text as received and matches the physical state I verified: AUDIT_ENTRYPOINT.md unmodified vs BASE,
HEAD unchanged at BASE, no staged/committed paths, 6 foreign untracked roots untouched. RESULTING_SHA =
NONE (this phase) is correct. PE_MASTER_REVIEW.md is an honestly-marked PLACEHOLDER
(NOT_PERFORMED-do-persistence).

## FINDINGS (all P3; no P1/P2)

**[F-QC-A | P3] NEIGH row-range annotation defects in three raw files + one ledger evidence cell.**
- Sources: 01_RAW/FUN_006C8F80_BASECTOR_DECODE.txt:71 ("EDGE_ACCOUNTING_LEDGER rows NEIGH-12..NEIGH-21" —
  actual rows for that window: NEIGH-12..NEIGH-20; NEIGH-21 belongs to the lazy-init window);
  01_RAW/FUN_006C8B20_LAZYINIT_DECODE.txt:85 ("rows NEIGH-22..NEIGH-27" — actual: NEIGH-21..NEIGH-24;
  NEIGH-25..27 belong to the producer window); 01_RAW/FUN_006C6F60_PRODUCER_DECODE.txt:99 ("ledger rows
  NEIGH-28..NEIGH-31" — THOSE ROW IDS DO NOT EXIST; actual: NEIGH-25..NEIGH-27);
  FIELD_PRODUCER_LEDGER.csv:11 (GAP-2 EVIDENCE cell cites "EDGE_ACCOUNTING_LEDGER NEIGH-22..NEIGH-27" —
  actual FUN_006C8BB0-window rows: NEIGH-21..NEIGH-24).
- Effect/skutek: cross-reference imprecision only. Every referenced row EXISTS in the ledger with correct
  caller/VA/reason; I byte-verified the underlying callsites myself (0x006C8C02/0F/34/52, 0x006C907E..
  0x006C90F0, 0x006C70CE/DE/EA — all PASS in my QC-G series). No load-bearing claim depends on the range
  annotations; the GAP-2 declaration (FUN_006C8BB0 unopened) stands.
- Poprawka: regenerate the four annotation strings with the actual row IDs (NEIGH-12..NEIGH-20;
  NEIGH-21..NEIGH-24; NEIGH-25..NEIGH-27; NEIGH-21..NEIGH-24) at the next records-correction opportunity.
- Test rewalidacji: grep the corrected files for the row IDs; each cited range must equal the ledger's
  rows enumerated for that evidence window.

**[F-QC-B | P3] Garbled window-end sentence in the producer raw record.**
- Source: 01_RAW/FUN_006C6F60_PRODUCER_DECODE.txt:101 — "Window ends 0x006C7088+0xC8 = 0x006C7088?
  (LEN 400 from 0x006C6F60 = 0x006C70F0; the instruction listing cut at the window end)". The leading
  fragment "0x006C7088+0xC8 = 0x006C7088?" is a malformed leftover draft; the correct arithmetic
  (LEN 400 -> window end 0x006C70F0) appears later in the same line.
- Effect: cosmetic/records blemish; the physical window (0x006C6F60..0x006C70F0) and every byte in the
  record are correct (verified by my own reads/decode).
- Poprawka: rewrite the line as one clear statement ("Window ends at 0x006C70F0 (LEN 400).").
- Test rewalidacji: the corrected line must contain exactly one window-end arithmetic, equal to 0x006C70F0.

**[F-QC-C | P3] Inaccurate directory-contents statement in the oracle availability ruling.**
- Source: INPUT_IDENTITIES.md:104-107 — "D:\gamebyroengine contains only the extracted Gb12_Source and
  the Gamebryo 1.1.2 Evaluation SDK" — MY OWN listing shows the directory ALSO contains GameBryo2.6.7z,
  Gamebryo 1.2 Source.rar, gamebryo_1.2.7z, GB_2.3.iso, Gamebryo_Version_1.1.2_Gamebryo_2004.iso
  (plus the .zip).
- Effect: the justification sentence is wrong, but the OPERATIVE ruling stands: a .7z archive is not the
  sigmaco/gamebryo-v2.6 git mirror at commit 329cd25…; no file identity against that commit can be
  measured without extraction (out of scope); the mirror therefore remains NOT_PRESENT-as-identity /
  NOT_USED, and NO oracle-based claim exists anywhere in the package. OpenMW absence is independently
  confirmed by my bounded search (no openmw tree under D:\ or C:\Users\User).
- Poprawka: restate the directory census accurately; keep the NOT_USED ruling.
- Test rewalidacji: directory listing quoted in the record must equal the physical listing.

**[F-QC-D | P3] Unpersisted independent manifest re-hash claim.**
- Source: HANDOFF.md:145-155 — claims an "INDEPENDENT post-generation re-hash by a separate
  implementation", with the record "reported in the terminal response and QC_REPORT.md (not persisted as
  a package file)". QC_REPORT.md contains no such record (its checks predate the manifest; the manifest
  is generated LAST at 11:28:59Z).
- Effect: the claim's "and QC_REPORT.md" part is inaccurate as written; the physical manifest state is
  nonetheless now INDEPENDENTLY confirmed by MY QC (27/27 .NET re-hash, zero mismatch).
- Poprawka: at persistence, attribute the independent re-hash to the persisted QC record(s) of the final
  package; drop the QC_REPORT.md citation.
- Test rewalidacji: the final package's manifest-verification note must cite a persisted record.

**[F-QC-E | P3] Census-note: the four §7 intervening callsites carry no ledger row.**
- Source: the four prior-scope callsites FUN_0050A310 @0x0050A3B9->FUN_006C0F90, @0x0050A3CF->FUN_006C10B0,
  @0x0050A3D8->FUN_0050A1E0, @0x0050A3E4->FUN_005246E0 are re-pinned inside
  01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt (prior-recorded "intervening call #1..#4" roles; prior record cited)
  and in PINS_AND_REL32.txt (pins + rel32 with "(intervening callee #N; body NOT opened)"), but have NO
  EDGE_ACCOUNTING_LEDGER row (neither REPIN_PRIOR_SCOPE nor RAW_VISIBLE_ONLY), while the same window's
  join call DOES have one (RP-07) and the FUN_006A3930 prior-scope re-pins DO have rows (RP-01..RP-06).
- Effect: no budget or claim impact — their interpretations are prior-recorded (the source run's QC S4
  window + the F-QC-6 residue named exactly these four undecoded callees), so they are correctly NOT
  counted; but EVIDENCE_INDEX's "the FULL callsite census" wording is slightly overbroad: a reader
  reconstructing the census from the ledger alone would miss these four callsites.
- Poprawka: add four REPIN_PRIOR_SCOPE rows (free, prior record cited) at the next records-regeneration,
  or scope the "full census" wording to "every analyzed/interpreted callsite unit of this run".
- Test rewalidacji: the ledger must enumerate every callsite touched by the run's records, with a class
  and reason for each.

## OBSERVATIONS (non-findings, recorded for transparency)

- O-1: the executor's S6_independent_reconstructed_edge_count check is partially circular ("both from
  the ledger") — the executor DISCLOSES this in its own detail string; the genuinely independent part of
  its QC is the 26-call completeness bijection, and MY QC now supplies the fully independent count (24).
- O-2: QC_REPORT.md (11:27:08Z) was written before the final execution of qc_internal.py that produced
  the persisted QC_INTERNAL_RESULTS.json (11:28:56Z); the script bytes were unchanged between (mtime
  11:24:11Z) and the two records are content-consistent (23/23 checks, all ok). No discrepancy.
- O-3: my QC records under 00_CONTROL_INTERNAL_QC/ (7+ files) are OUT of the executor-phase manifest
  scope by design; per the established precedent the PERSISTENCE PHASE must regenerate the manifest over
  the final physical package (including these QC records) and re-verify the bijection.

## NOT_CHECKED by this QC (explicit)

- The four §7 intervening callee BODIES (FUN_006C0F90/FUN_006C10B0/FUN_0050A1E0/FUN_005246E0) — EDI
  preservation inside them remains physically unverified (STATIC-ONLY; opening them would be new
  science; the STRONGLY_SUPPORTED cap is correct).
- FUN_006C9700 and the creation chain (GAP-1); FUN_006C8BB0 (GAP-2); FUN_007B6C30; FUN_006C7740;
  FUN_006C7B40; FUN_006D3570; the manager slot-2/slot-3 bodies (0x006C0FD0/0x006C19B0); all NEIGH bodies;
  the FUN_006C6780 continuation past 0x006C6844 — all correctly NOT_CHECKED by the run and NOT checked
  here (QC opens no new science branches).
- The 0x110 NiControllerSequence object's own bytes (CTRL_1's mutated fixture is the synthetic input
  built from the prior canon's classification, per contract §9.1 — no new real EXE objects were
  searched; consistent).
- Any runtime behavior (the client never ran); any payload/VFS/BNT/NIF content; remote state of
  origin/master beyond the BASE pin (no push occurred in this phase; local HEAD == BASE re-verified by
  me before and after my QC work).

## Files of this QC (all under 00_CONTROL_INTERNAL_QC/)

- qc_ind_byte_pins.py + qc_ind_byte_pins_results.json (part 1: own PE mapper + identity + pins)
- qc_ind_decoder.py + qc_ind_decoder_results.json (part 2: own sequential decoder + extents + CALL walk)
- qc_ind_census.py (part 3: ledger census + independent edge reconstruction + J2 sweeps)
- qc_ind_controls_replica.py (part 4: my own CTRL_1..4 replicas)
- qc_ind_manifest_rehash.ps1 (part 5: .NET manifest re-hash + encoding + blob identity)
- QC_IND_REPORT.md (this report) + FULL_READ_LOG.md + QC_IND_RESULTS.json
