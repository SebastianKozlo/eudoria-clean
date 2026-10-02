# CORRECTION RUN CONTRACT — PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002

**Contract class:** ONE FOCUSED CORRECTION CYCLE of the existing run package
`docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002/`. No new science, no new RE question,
no scope expansion, no automatic follow-up. This document is the normative transcription of the
human decision HUMAN_DECISION_ID `PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_AUTH_R1_20261002`
(human order 2026-10-02), issued after the independent ChatGPT Desktop post-audit verdict
DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS.

| Field | Value |
|---|---|
| RUN_ID (correction) | PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002 |
| CORRECTION_TARGET | existing run package PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 (RUN_CLASS LOAD_BEARING; RUN_TYPE DESKTOP_FOCUSED_BRANCH_SELECTION_CORRECTION) — correction happens INSIDE that package |
| PARENT_AUTHORIZATION | HUMAN_DECISION_ID PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_AUTH_R1_20261002 (human order 2026-10-02; one focused correction cycle after DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS) |
| DISPATCHED_BY | PE-MASTER direct |
| BASE_SHA (AUTHORIZED_BASE_HEAD) | 9203b6d1ad5025f4158d5165863594132aaac49f (must equal current HEAD at execution start; re-verify) |
| EXECUTOR | pe-reconstruction (dispatched separately by PE-MASTER) |
| FRESH QC | a separate pe-master-auditor QC session (dispatched separately by PE-MASTER) |
| PERSISTENCE | pe-master-auditor (dispatched separately by PE-MASTER) |
| MODE | STATIC-ONLY: no client launch, no runtime execution, no hooks, no patching of any original binary/file |
| NO_NESTED_TASKS | YES — no agent dispatch by any worker under this contract; results return to PE-MASTER |
| Pre-state record | 00_CONTROL\DESKTOP_CORRECTION_R1\PRE_CORRECTION_STATE.md (formalizer-measured; re-verify at execution start) |
| Contract freeze | 00_CONTROL\DESKTOP_CORRECTION_R1\CORRECTION_CONTRACT_FREEZE.json |
| Pinned inputs | Entropia.exe = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe (8,015,872 B; SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31); 20002.vfs = D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs (174,864 B; SHA256 C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4); starting manifest 06_REPORT\MANIFEST_SHA256.csv (50,698 B; SHA256 CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF) |

## §0 IDENTITY AND GOVERNANCE

- RUN_ID: PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002. This contract authorizes ONE
  focused correction cycle of the existing package PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
  (RUN_CLASS LOAD_BEARING; RUN_TYPE DESKTOP_FOCUSED_BRANCH_SELECTION_CORRECTION).
- Roles: executor = pe-reconstruction (dispatched separately by PE-MASTER); fresh QC = a separate
  pe-master-auditor QC session (dispatched separately); persistence = pe-master-auditor (dispatched
  separately).
- STATIC-ONLY: no client launch, no runtime execution, no hooks, no patching of any original
  binary/file.
- NO_NESTED_TASKS.
- Governance unchanged: Q1_STATUS_CHANGED=NO; PE_MASTER_QUALIFICATION_CHANGED=NO;
  GATE_B_CHANGED=NO; M1_CHANGED=NO; M2_CHANGED=NO; M3_CHANGED=NO; MILESTONE_CLOSED=NO;
  NEXT_MILESTONE_AUTHORIZED=NO.
- Publication is an audit-trail action and does NOT imply scientific acceptance.

## §1 SCOPE (ONE focused correction cycle; NO further science)

**(a) Branch selection re-derivation.** Independently re-derive the branch selection for tag ID 17
in the value-read dispatch FUN_0075F660 from the physical Entropia.exe bytes. Prove or reject the
candidate chain (§2). The evidence must establish, each from pinned bytes:

1. registration of tag ID 17;
2. factory return behavior;
3. whether descriptor+0 is NULL or non-NULL for tag ID 17;
4. preservation of the descriptor object (arg dataflow FUN_0070cbc0 -> FUN_0075f5c0/param_5 ->
   descriptor+0 -> FUN_0070c980 table insert);
5. the exact conditional branch in FUN_0075F660 (TEST/JZ);
6. the selected virtual slot ([object.vtable+0x14]);
7. the virtual-function target (the static vtable dword);
8. the selected reader function.

Do not stop at matching instruction bytes — the SELECTED PATH must be proven (control-flow
reachability from the descriptor state, not just instruction presence).

**(b) Cursor provenance.** Re-prove cursor provenance for the SELECTED reader (record_i.payload +
0x30; start of record, payload start, TLV entry ordering, widths of preceding values, tag widths,
cursor increments, actual cursor at reader entry; error/failure paths distinguished from the
successful parse path).

**(c) Destination provenance.** Re-prove destination provenance for the SELECTED reader
(ArkParameterArmor value-array slot 21; instance structure source; value-array pointer; descriptor
field index tag+4; destination address; selected store instruction; width). Keep
DEST_FIELD_IDENTIFIED=YES strictly separate from DOWNSTREAM_CONSUMER_IDENTIFIED=NO (the slot is
not itself the gameplay consumer).

**(d) Active-dependency corrections.** Correct every active artifact whose truth depends on the old
selected-reader trace (dependency-aware, no blind global replacement; see §4).

**(e) Residual non-science corrections.** See §7.

## §2 DESKTOP LEADS (LEADS_TO_VERIFY — NOT truth)

- Every load-bearing use of a Desktop lead must be re-derived from the pinned EXE in-run; report
  the measured result rather than forcing the candidate.
- Candidate chain: schema(tag ID 17) registration -> nonzero descriptor factory object retained at
  descriptor+0 -> FUN_0075F660 TEST descriptor+0 -> non-NULL virtual branch ->
  [object.vtable+0x14] -> FUN_009777F0.
- Candidate reader pins: READ_FUNCTION = FUN_009777F0; READ_INSTRUCTION_VA = 0x00977807;
  READ_INSTRUCTION_FILE_OFFSET = 0x00577807; READ_BYTES = 8B 04 10; STORE_INSTRUCTION_VA =
  0x00977810; STORE_BYTES = 89 02.
- The executor MUST independently recompute VA/RVA/PE-section/file-offset/raw-bytes/decoded-instruction/destination
  behavior (own PE parse; do not copy Desktop addresses into the report until independently
  reproduced).
- Stale active claim to be retracted AS ACTIVE (preserved as historical/fallback evidence): the
  selected-reader trace READ_FUNCTION=FUN_00412540 / READ @ VA 0x00412553 / STORE @ VA 0x0041255A /
  the REPORT transcription "READ_INSTRUCTION_FILE_OFFSET = 0x00125553" (digit-shift error; the run's
  own pin JSON records the correct fallback offset 0x12553; both the wrong transcription AND the
  "selected" status must be superseded).

## §3 BEFORE-COPY / HISTORY DISCIPLINE

- Before changing ANY artifact or generator: byte-for-byte BEFORE copy + size + SHA256 into
  `00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\` (mirror the relative path, e.g.
  `BEFORE\06_REPORT\REPORT.md`).
- Preserve the starting manifest as historical evidence (already covered by the manifest being in
  the package; additionally its SHA CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF
  is recorded in PRE_CORRECTION_STATE.md).
- Historical material IMMUTABLE (no rewrite, no supersede-in-place):
  - QC round 1 report/results/tools (04_QC\QC_REPORT.md, QC1_*_RESULT.json, qc_tools\);
  - QC round 2 report/results (04_QC\QC_R2_TARGETED_REPORT.md, QC_R2_*_RESULT.json);
  - 00_CONTROL\RUN_CONTRACT.md;
  - 00_CONTROL\CONTRACT_FREEZE.json;
  - original game inputs (Entropia.exe, 20002.vfs);
  - the historical JOIN R1 package (docs\audits\PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\ —
    outside this package, untouchable);
  - previous incorrect trace evidence (01_RAW\CLIENT_READ_BYTES.json stays byte-unchanged — its
    pins are byte-correct FALLBACK-path + routing evidence; add new correction evidence in NEW files).
- New correction artifacts and new QC artifacts use NEW names / history-preserving subdirectories
  (do not overwrite prior QC rounds).
- The frozen correction control files (00_CONTROL\DESKTOP_CORRECTION_R1\PRE_CORRECTION_STATE.md,
  CORRECTION_RUN_CONTRACT.md, CORRECTION_CONTRACT_FREEZE.json) are frozen formalizer outputs: not
  editable by the executor.

## §4 ACTIVE-DEPENDENCY CORRECTION SET (inspect each; update where required; dependency-aware statements)

- 06_REPORT\REPORT.md (READ_FUNCTION/READ_VA/RVA/FILE_OFFSET/BYTES/STORE fields; the §9 chain; the
  anchor; statuses)
- 02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md (the §9 trace chain + §9 field table)
- 02_ANALYSIS\CONSUMER_TRACE.md (the answer narrative)
- 02_ANALYSIS\SEMANTIC_ASSESSMENT.md (if it asserts the selected reader)
- 02_ANALYSIS\NEGATIVE_CONTROLS.md (any selected-path claims)
- 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json + read/write census artifacts (selected-path fields)
- 02_ANALYSIS\BLAST_RADIUS.md (add the branch-selection supersession; reconcile with the Desktop
  P1; the existing items 2/6 corrections — FUN_00959090->EnvironmentZones, FUN_0070E810->textures —
  and the JOIN R1 claim-5 advisory supersession already recorded there stay; do NOT edit historical
  JOIN R1)
- 06_REPORT\EVIDENCE_INDEX.md (claim->artifact map for the corrected state + new artifacts)
- 06_REPORT\PE_MASTER_REVIEW.md (the prior verdict record: claim 5 "THE CLIENT READ @0x412553"
  and the RUN_STATUS line are superseded — update with an explicit supersession/amendment note
  preserving the historical verdict story; the BEFORE copy preserves the old text)
- 06_REPORT\HANDOFF.md (delivery notice for the corrected state)
- relevant byte-pin artifacts: ADD new pin evidence (e.g.
  01_RAW\DESKTOP_CORRECTION_R1\CLIENT_READ_BYTES_CORRECTION_R1.json) — do not overwrite
  CLIENT_READ_BYTES.json
- relevant generator scripts: run-local instrumentation/correction scripts go in NEW paths (e.g.
  03_SCRIPTS\desktop_correction_r1\); the historical scripts stay unchanged (their re-run is NOT
  required; document that regenerating old artifacts would need script fixes first — carried from
  the prior FUTURE-ADMINISTRATIVE-PASS list)
- 04_QC QC/pin generators: immutable (QC rounds 1/2 historical)
- Preserve byte-correct fallback pins explicitly labeled BYTE-CORRECT EVIDENCE OF A NON-SELECTED
  FALLBACK PATH (unless fresh physical evidence establishes otherwise).

## §5 DOWNSTREAM-CONSUMER WORDING (mandatory final state unless new bounded evidence proves otherwise)

- DOWNSTREAM_CONSUMER_IDENTIFIED = NO; RUN_STATUS = CONSUMER_UNREACHED; DEST_FIELD_IDENTIFIED =
  YES; FINAL_SEMANTIC_STATUS = UNVERIFIED; WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED;
  PLACEMENT_XYZ_RECOVERED = NO; id2-domain correlation stays CANDIDATE / UNVERIFIED
  (numeric-domain overlap is not semantic proof).
- Replace any over-broad claims ("no static reader exists"; "reads are runtime-tag-driven";
  "static-only cannot close"; "runtime is required") with bounded wording equivalent to:
  "Within the inspected 202 direct descriptor-lookup sites and the documented limited context
  window, no tag-ID-17 downstream reader was identified. Full downstream static data-flow,
  aliases, indirect calls and global writer/read completeness remain UNVERIFIED. Further static
  resolvability is NOT_ESTABLISHED."
- Write-side/read-side: do not claim unique global writer / exhaustive reader or consumer census /
  global absence of static users unless demonstrated; the existing one-caller observation for
  FUN_0075F660 is scoped explicitly (ONE_DIRECT_CALLER_FOUND within the censused machinery; NOT
  global proof that slot 21 has exactly one writer across the client).
- Use "tag ID 17" (not "17th property/descriptor") where ordinal meaning could be confused.

## §6 FRESH QC REQUIREMENTS (encoded here for the separately-dispatched QC worker)

- QC independent from the correction implementation; must test the actual branch-selection logic,
  not merely compare known expected bytes.
- Required discriminating failure detector: construct controlled in-memory models/variants of the
  already-decoded branch logic where (A) descriptor+0 = NULL; (B) descriptor+0 = NON-NULL;
  (C) virtual slot +0x14 points to another synthetic candidate target. The validator must
  demonstrate that its predicted selected path changes appropriately across A/B/C.
- NULL may legitimately select the fallback — the negative control must detect PATH-SELECTION
  CHANGE, not falsely insist that NULL is invalid input.
- QC must FAIL if: descriptor non-NULL is ignored; fallback is selected despite the proven non-NULL
  descriptor for tag ID 17; the virtual target is not proven (static vtable dword not pinned);
  reader VA/FO wrong; cursor does not reach +0x30 at the tag-ID-17 iteration for the selected
  reader; destination is not slot 21.
- QC writes ONLY in a NEW history-preserving subdirectory (e.g. 04_QC\QC_R3_DESKTOP_CORRECTION\ +
  its own qc_tools subdir); QC verdict PASS|PASS_WITH_FINDINGS|FAIL with P0/P1/P2/P3 findings.
- QC must also: re-hash EXE/VFS/HEAD; re-verify its own copy of the corrected pins; run the wording
  sweep (§5); recompute denominators; manifest spot re-hash. QC does not alter executor evidence.

## §7 RESIDUAL NON-SCIENCE CORRECTIONS (same cycle)

1. "tag ID 17" wording per §5.
2. Freshly measure the final package physical file count (do NOT hard-code 389).
3. In REPORT/HANDOFF distinguish explicitly: physical files vs manifest data rows vs manifest text
   lines vs NOTE rows vs header lines.
4. Preserve historical earlier counts where they accurately described earlier package states (e.g.
   the HANDOFF delivery-time 364/363 census is a historical delivery record — do not rewrite it as
   if wrong; add the corrected census as new state).
5. No manifest-line/file-count conflation anywhere in the corrected state.

## §8 HISTORICAL QC PRESERVATION

- QC round 1 and QC round 2 are historical evidence — do not rewrite their reports.
- The corrected state must explicitly record that their conclusion about the selected reader branch
  (the fallback-path acceptance) was superseded by the Desktop counterexample and this focused
  correction.
- The lesson must remain auditable in the amendment/correction log: "correct instruction bytes !=
  proven selected execution/parser path".

## §9 AMENDMENT / CORRECTION LOG

- New file 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md records: the Desktop finding; the
  superseded claim; BEFORE/AFTER artifacts (path + size + SHA256 pairs); the branch-selection
  correction; remaining unknowns; the exact affected dependency set.

## §10 FINAL SEQUENCE (terminal order; the executor's part ends at step 4; steps 5+ are separate dispatches)

1. CORRECTION
2. FRESH TARGETED QC
3. QC DISPOSITION
4. AMENDMENT/CORRECTION LOG
5. FINAL REPORT
6. FINAL EVIDENCE_INDEX
7. FINAL PE_MASTER_REVIEW (PE-MASTER verdict persisted by pe-master-auditor)
8. FINAL HANDOFF
9. AUDIT_ENTRYPOINT POINTER UPDATE IF APPLICABLE (factual pointer only; no governance promotion;
   no claim of Desktop PASS before the focused Desktop post-audit; BEFORE commit; in the SAME
   publication commit)
10. FINAL PACKAGE MANIFEST GENERATED LAST (MANIFEST_SHA256.csv regenerated; self-exclusion: the
    manifest is excluded from its own data rows but remains a normal committed file)
11. COMPLETE PACKAGE/MANIFEST BIJECTION VERIFICATION (every manifest row == disk size+SHA; disk
    census == manifest rows + manifest itself)
12. verify the finalized MANIFEST_SHA256.csv itself by size/SHA before staging
13. STAGED PATH AND CONTENT VERIFICATION (stage ONLY the correction package + AUDIT_ENTRYPOINT.md;
    no unrelated working-tree groups; no Entropia.exe/20002.vfs/installers/original .bnt/.ark/.vfs
    corpora/proprietary payloads/credentials/secrets; MANIFEST_SHA256.csv present in the staged
    tree; staged bytes == verified disk state)
14. COMMIT (normal new commit; no amend/squash/force-push/reset/history-rewrite; message
    identifies: RUN_ID, focused Desktop correction, actual correction/QC verdict, main superseded
    reader-path claim, confirmation that original proprietary payloads are excluded)
15. PUSH to origin/master (if remote diverged or push fails: PERSISTENCE_STATUS=PERSISTENCE_BLOCKED;
    preserve the local commit; report local SHA + push error + live remote SHA if obtainable + exact
    blocker; HARD STOP; no auto merge/rebase)
16. LIVE REMOTE VERIFICATION (git ls-remote --exit-code origin refs/heads/master; record exact
    command, UTC timestamp, exit status, returned remote SHA; require
    LOCAL_HEAD == LIVE_REMOTE_MASTER_SHA)
17. HARD STOP. NEXT_EXPERIMENT_AUTHORIZED = NO; NEXT_ACTION = FOCUSED_CHATGPT_DESKTOP_POST_AUDIT.

Post-push package immutability: no silent edit/add/delete of package files after the final manifest
verification + commit; push receipts go in the terminal response or OUTSIDE the finalized package
(no receipt files inside the package without another explicit manifest-regeneration persistence
commit).

## §11 PASS/FAIL GATES (executable; fail-closed; a gate weaker than its label is a finding)

- **C0_PRE_STATE**: HEAD == 9203b6d1ad5025f4158d5165863594132aaac49f; EXE/VFS identities
  (8,015,872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31;
  174,864 B / C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4); starting manifest
  SHA == CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF; starting bijection
  388/388 + manifest-only-on-disk delta; 5 pre-existing untracked groups byte-identical.
  FAIL => BLOCKED_INPUT_OR_PACKAGE_IDENTITY, HARD_STOP.
- **C1_BRANCH_PROVEN** (hard): each of the 8 §1(a) items pinned byte-level (VA/RVA/section/file-offset/bytes
  per pin; control-flow reachability stated; the descriptor+0 value for tag ID 17 proven non-NULL or
  NULL from the registration dataflow + factory return — not assumed); the selected slot/target
  identified statically (vtable dword read from the pinned EXE .rdata).
- **C2_READER_PINS** (hard): the selected reader's READ/STORE instructions byte-pinned with
  independently recomputed VA/RVA/file-offset; matches or falsifies the Desktop candidates (report
  measured values).
- **C3_CURSOR_PROVEN** (hard): selected-reader cursor at tag-ID-17 entry == payload+0x30 for the
  record (record 0 + ANCHOR_ZERO + census denominator 1366 per the existing framing artifacts —
  re-derive from the walk, do not inherit); error paths distinguished.
- **C4_DESTINATION_PROVEN** (hard): selected store targets value_array + (tag+4)*4 = slot 21
  (+0x54) — the same LEA chain 0x726A11/0x726A14 + dest arg pass-through in the virtual branch
  (0x75f670-0x75f67b); width 4.
- **C5_DEPENDENCIES_CORRECTED**: every active-dependency artifact updated or explicitly dispositioned
  as not-dependent; no contradictory live copy remains (repository-wide contradiction census WITHIN
  the package; entrypoint pointer per §10 if applicable); fallback pins preserved labeled.
- **C6_QC_BRANCH_SELECTION**: fresh QC executed with the A/B/C discriminating detector; QC verdict
  recorded in a NEW QC path; every QC finding dispositioned.
- **C7_WORDING**: §5 wording applied; high-risk-word audit (only/all/none/global/exhaustive/unique/proves…)
  — every occurrence evidence-anchored or weakened; "tag ID 17" convention.
- **C8_PACKAGE_FINAL**: final REPORT carries all original §18 fields (REPORT.md field list per the
  original RUN_CONTRACT §18 — preserve all keys) with corrected values; final file/row/line counts
  measured fresh and distinguished; manifest regenerated LAST with self-exclusion; bijection
  verified; manifest's own size/SHA verified separately before staging.
- **C9_PERSISTENCE** (per §10): staged census == package + AUDIT_ENTRYPOINT.md only; commit message
  per §10; push; live remote equality; receipt recorded.

Non-pass classes: BLOCKED_INPUT_OR_PACKAGE_IDENTITY; CORRECTION_PARTIAL_BRANCH_UNPROVEN (if the
selected-path proof fails — then report the measured state honestly: which link failed, what the
bytes show); QC_FAIL; PERSISTENCE_BLOCKED. If scientific revalidation fails or remains partial: do
NOT open another science question; complete the honest package state and proceed only to the
authorized persistence.

HARD_STOP: after push + live remote verification (or on any BLOCKED class). No automatic follow-up.

## §12 FORBIDDEN

- launching/instrumenting the client; runtime hooks; runtime execution;
- new placement/gameplay experiments; any new RE question outside this correction;
- editing historical JOIN R1;
- rewriting historical QC reports (rounds 1/2);
- rewriting RUN_CONTRACT.md/CONTRACT_FREEZE.json (the historical originals in 00_CONTROL\; the
  frozen DESKTOP_CORRECTION_R1 control files are likewise not editable by the executor);
- modifying original Entropia.exe/20002.vfs or any original payload;
- staging unrelated working-tree groups;
- proprietary payloads/secrets in Git;
- automatic milestone progression; automatic follow-up correction loop after publication;
- force-push; history rewrite;
- recording the commit's own SHA inside files in that same commit.

(End of contract — frozen by CORRECTION_CONTRACT_FREEZE.json)
