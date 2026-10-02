# RUN_CONTRACT — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

OUTPUT_ROOT (this run package) = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\
FORMALIZED_BY = pe-master-auditor formalizer session (ASSIGNMENT_MODE = FORMALIZE; FORMALIZER ONLY — no science executed by the formalizer)
DISPATCHED_BY = PE-MASTER direct, under human authorization PE_935_20002_PAYLOAD30_CONSUMER_HUMAN_AUTH_R1_20261002
FORMALIZED_AT_UTC = 2026-10-02T18:19:08Z
CONTRACT_STATUS = FROZEN at formalization. The SHA256 + exact byte size of this file are recorded in 00_CONTROL\CONTRACT_FREEZE.json. The executor re-verifies this file's SHA256 at execution start, BEFORE any science.
Expected input identities (GATE S0 pins, transcribed as measured expected values; source: human authorization + PE-MASTER preflight 2026-10-02, re-verified by the formalizer 2026-10-02):
- EXPECTED_HEAD = 9203b6d1ad5025f4158d5165863594132aaac49f
- EXPECTED_EXE = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe — 8,015,872 B — SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
- EXPECTED_VFS = D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs — 174,864 B — SHA256 C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4
Full S0 detail: 00_CONTROL\PREFLIGHT_EXPECTED.md. Authorization transcription: 00_CONTROL\AUTHORIZATION_RECORD.md.
Section numbering §0-§19 + §A-§D follows the PE-MASTER dispatch; the normative text below is transcribed exactly.

---

## §0 RUN IDENTITY

RUN_ID = PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
PARENT = PE-MASTER direct dispatch under human authorization PE_935_20002_PAYLOAD30_CONSUMER_HUMAN_AUTH_R1_20261002
CURRENT_MILESTONE_NAMESPACE = EU935-M1 remains the current open milestone; this run is a bounded EU935-M3-contribution workstream under the human's direct order; NO milestone crossing, NO milestone closure, NO M2/M3 start.
RUN_CLASS (PE-MASTER audit-depth declaration) = LOAD_BEARING
RUN_TYPE = STATIC_RE_CONSUMER_TRACE (single science question)
BASE_SHA = 9203b6d1ad5025f4158d5165863594132aaac49f
COMMIT = FORBIDDEN; PUSH = FORBIDDEN. The package is untracked working-tree state; persistence commit/push await separate human authorization.
DIRTY_TREE_INVENTORY (pre-existing, READ-ONLY, must remain byte-identical): the 5 untracked groups measured by the PE-MASTER preflight 2026-10-02 and re-verified by the formalizer at formalization:
- docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
- docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
- docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
- docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
- experiments/
NO_NESTED_TASKS. Executor writes ONLY inside OUTPUT_ROOT (04_QC\ reserved for the fresh internal-QC worker).

## §1 ONE PRIMARY QUESTION (the ONLY science scope)

"What does the PCG 9.3.5 client do with the value located at payload+0x30 of a concrete record in 20002.vfs?"

Required trace (the complete authorized science scope):
ORIGINAL PHYSICAL BYTE / RECORD FIELD -> CLIENT READ / PARSER INSTRUCTION -> DESTINATION STRUCTURE FIELD -> DOWNSTREAM CONSUMER -> MECHANISM USING THE VALUE -> BOUNDED SEMANTIC ASSESSMENT

Everything else is supporting evidence for this trace (framing, routing, census, controls) or forbidden scope.

## §2 PROHIBITED STARTING ASSUMPTIONS

(verbatim from authorization §2; these semantic labels may NOT be applied to the payload+0x30 value unless independently re-established from in-run evidence, with each such promotion carrying its own byte-level proof):

id2; template ID; resource ID; model ID; NIF ID; object ID; instance ID; world-placement ID; network ID; foreign key; pointer; offset; coordinate; world-instance -> model edge.

Numerical equality with another identifier is not semantic evidence. A lookup returning a matching number is not automatically identity. Historical placement work may be used ONLY as search context and prior evidence. Do not silently promote old hypotheses. The search question is "where does this exact field flow?" — do NOT search by an expected answer (e.g. "find where id2 becomes model").

## §3 EPISTEMIC BASELINE (starting statuses; any change requires in-run evidence)

20002_VFS_PAYLOAD_PLUS_30_FINAL_SEMANTIC_ROLE = UNVERIFIED
WORLD_INSTANCE_TO_MODEL_LINK = NOT_DEMONSTRATED
PLACEMENT_SOURCE = NOT_RECOVERED

## §4 GOVERNANCE UNCHANGED (this run does not alter)

Q1_ATTEMPT_4_RESULT = NOT_GRADED; PE_MASTER_STATUS = PROVISIONAL_UNTIL_QUALIFIED; PE_MASTER_QUALIFIED = NO; GATE_B_CANONICAL_AUTHORITY_STATUS = BLOCKED; M1_CLOSED = NO. PE-MASTER participates only as ADVISORY_PRE_QUALIFICATION; its verdict is not a canonical gate.

## §5 INPUTS

ALLOWED (read-only): the pinned Entropia.exe; the pinned 20002.vfs; other files under D:\Eudoria_Reconstruction\pcg_install\ (identity metadata + bounded reads; e.g. templates.vfs as prior-evidence context); prior audit packages (READ-ONLY reference; especially docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\ incl. 04_TOOLS/vfs_common.py and 01_RAW\GHIDRA_OUT\* and 03_COUNTERCHECKS/AMEND_R2/AMEND_R2_ID2_MEMBERSHIP_20002_48.json); Ghidra headless (static); bounded analysis scripts created inside OUTPUT_ROOT\03_SCRIPTS\ (executor) and OUTPUT_ROOT\04_QC\ (QC worker only); local evidence artifacts inside OUTPUT_ROOT.

FORBIDDEN: launching/instrumenting the client; runtime hooks or mutations; running a second science question; broad placement recovery; searching all world-instance mechanisms as a campaign; recovering building locations generally; implementing placement in the renderer/runtime; modifying original game payloads; starting M2/M3; closing M1; qualifying PE-MASTER; Gate-B re-attestation; starting another Q1 attempt; COMMIT; PUSH; STAGING; editing any file outside OUTPUT_ROOT; editing originals.

## §6 PREFLIGHT (GATE S0)

See PREFLIGHT_EXPECTED.md. The executor re-measures HEAD + EXE + VFS identity BEFORE any science and records ACTUAL values in 00_CONTROL\PREFLIGHT.md (plus 00_CONTROL\SOURCE_IDENTITY.md with era/build/paths/SHAs). Mismatch => RUN_STATUS=BLOCKED_INPUT_IDENTITY_MISMATCH, HARD_STOP=YES.

## §7 RECORD-RELATIVE BYTE ANCHOR

"payload+0x30" means the payload of a SPECIFIC concrete record of 20002.vfs. Physical definition: FIELD_FILE_OFFSET(record_i) = RECORD_PAYLOAD_START(record_i) + 0x30. Do NOT substitute file+0x30 or a container-wide payload start.

For every analyzed record preserve: RECORD_ORDINAL_OR_PHYSICAL_ID, RECORD_FRAME_START, RECORD_PAYLOAD_START, RECORD_PAYLOAD_LENGTH, FIELD_FILE_OFFSET, FIELD_BYTE_RANGE, FIELD_WIDTH, FIELD_ENDIANNESS, RAW_BYTES, DECODED_NUMERIC_VALUE.

Prove independently (machine-checkable assertions in the artifact): FIELD_FILE_OFFSET >= RECORD_PAYLOAD_START AND FIELD_FILE_OFFSET + FIELD_WIDTH <= RECORD_PAYLOAD_START + RECORD_PAYLOAD_LENGTH.

If record framing, payload boundary, width or endianness cannot be established, preserve that uncertainty — do NOT force FIELD_IDENTITY or a numeric interpretation.

Concrete-record selection rule (deterministic, recorded BEFORE extraction): ANCHOR_PRIMARY = zero-indexed record 0 if its payload length satisfies the bounds for a 4-byte field at +0x30 (payload_length >= 0x34); otherwise the lowest-ordinal record satisfying the bounds. ANCHOR_ZERO = the lowest-ordinal record whose payload+0x30 4-byte value equals 0 (prior evidence names records 1014/1015 zero-indexed — RE-DERIVE in-run, do not inherit). FIELD_CENSUS = for EVERY record in the file: payload start, payload length, field file offset, raw 4 bytes at +0x30 (when bounds hold; else a documented bounds-violation flag), decoded value, bounds-ok flag — one CSV/JSONL artifact, 1 row per record, with the file's record count as denominator. Report the number of records analyzed and the measured coverage scope.

WIDTH/ENDIANNESS provenance discipline (V2-009): until the client read instruction is pinned, the 4-byte little-endian reading of +0x30 is a HYPOTHESIS_DERIVED_MEASUREMENT (derived from payload alignment + prior scan convention) and must be labeled as such in the artifacts; after the client read is pinned, width/endianness become RAW_MEASUREMENT from the instruction bytes.

## §8 ROUTING EDGE (separate mandatory edge before any "client read" claim)

Establish, as far as evidence allows: TARGET_PATH=20002.vfs; TARGET_OPEN_OR_LOOKUP_SITE; TARGET_ROUTING_FUNCTION; READER_OR_PARSER_FUNCTION; ROUTING_EVIDENCE.

Required distinction: GENERIC_PARSER_IDENTIFIED = YES|NO; 20002_VFS_ROUTED_TO_GENERIC_PARSER = CONFIRMED|STRONGLY_SUPPORTED|PLAUSIBLE|UNVERIFIED|REJECTED.

A matching displacement such as +0x30 inside a generic parser is NOT sufficient proof that the instruction consumes this target field. If routing cannot be demonstrated, do NOT upgrade CLIENT_READ_IDENTIFIED merely because a structurally compatible parser exists (record the generic parser as candidate context and stop the read claim at the routing bound).

## §9 CLIENT READ (only after routing established as far as evidence allows)

Evidence preference: direct parser instruction > caller/callee data-flow > target-structure store > downstream reads > bounded static correlation > naming/numerical coincidence. Decompiler text alone is INSUFFICIENT — every claimed instruction must be byte-pinned.

Record where established: READ_FUNCTION, READ_INSTRUCTION_VA, READ_INSTRUCTION_RVA, READ_INSTRUCTION_FILE_OFFSET, READ_INSTRUCTION_BYTES, SOURCE_CURSOR_OR_BASE, SOURCE_DISPLACEMENT, WIDTH, DEST_REGISTER, DEST_OBJECT_OR_STRUCTURE, DEST_FIELD_OFFSET, STORE_INSTRUCTION_VA, STORE_INSTRUCTION_BYTES.

For every load-bearing instruction preserve IMAGE_BASE, VA, RVA, FILE_OFFSET, ORIGINAL_BYTES (read from the PINNED physical EXE; machine-verifiable: bytes at FILE_OFFSET must equal the recorded ORIGINAL_BYTES).

## §10 DESTINATION FIELD + BOUNDED CONSUMER CENSUS

If a destination field is identified, perform a bounded consumer census sufficient to answer the research question. Record: STATIC_WRITE_SEARCH_SCOPE, STATIC_READ_SEARCH_SCOPE, STATIC_WRITE_SITES_FOUND, STATIC_READ_SITES_FOUND, UNRESOLVED_ALIASES, UNRESOLVED_INDIRECT_CALLS, UNINSPECTED_PATHS.

Do NOT call a bounded census exhaustive for the entire client unless exhaustiveness itself is demonstrated. Consumer-exhaustiveness wording (V2-012): use ONE_DIRECT_CALLER_FOUND / ONLY_DIRECT_CALLER_AFTER_EXHAUSTIVE_CENSUS / ONLY_CALLER_GLOBAL / ONLY_NAMED_CONSUMER_IN_CURRENT_EVIDENCE exactly as evidenced; any un-inspected reference class (direct refs, address-taken/data refs, callbacks, vtables, function pointers, thunks, tail calls, computed dispatch, jump tables) makes global exhaustiveness UNVERIFIED.

Classify material consumers only when evidenced, from the authorization's open list: comparison; switch/branch; array index; map lookup; resource lookup; object lookup; function argument; virtual dispatch input; arithmetic; coordinate transformation; flag/mask; opaque propagation. Do NOT force a category when evidence does not support one.

## §11 FOLLOW THE VALUE, NOT THE NAME

For every claimed edge preserve SOURCE -> INSTRUCTION -> DESTINATION. If the value enters a map/registry/lookup, establish separately: KEY_ROLE, LOOKUP_CONTAINER, RESULT_TYPE, RESULT_CONSUMER. A map lookup does not by itself establish the semantic identity of the key. If a returned object is later used for resource/model loading, prove that subsequent edge independently.

## §12 HONEST BOUNDARIES + TERMINAL TAXONOMY

Do not expand scope merely because the result is interesting. RUN_STATUS terminal values (exactly these):

CONSUMER_REACHED_SEMANTIC_CONFIRMED | CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED | CONSUMER_REACHED_ROLE_PLAUSIBLE | AMBIGUOUS | CONSUMER_UNREACHED | BLOCKED_SOURCE_NOT_ESTABLISHED | BLOCKED_INPUT_IDENTITY_MISMATCH.

AMBIGUOUS and CONSUMER_UNREACHED are VALID scientific outcomes when supported by bounded evidence.

Report separately: FIELD_IDENTITY = <status>; OBSERVED_OPERATION = <status>; FINAL_SEMANTIC_ROLE = <bounded wording> + <status> — using only CONFIRMED|STRONGLY_SUPPORTED|PLAUSIBLE|UNVERIFIED|REJECTED. Valid example: FIELD_IDENTITY=UNVERIFIED, OBSERVED_OPERATION=CONFIRMED, FINAL_SEMANTIC_ROLE=UNVERIFIED. Structural parse closure is not semantic closure.

## §13 NEGATIVE CONTROLS

When a mechanism or semantic interpretation is proposed, at least one meaningful negative control is MANDATORY (capable of falsifying the interpretation). Record for each: NEGATIVE_CONTROL, EXPECTED_FAILURE, ACTUAL_RESULT, FAILURE_CASE_DETECTED.

Minimum feasible set for this run (execute all that are technically feasible; mark infeasible ones with the reason):

- NC-FRAMING (mandatory): an in-memory corrupted/truncated record variant (e.g. size field beyond EOF; wrong base/shifted start) must make the parser FAIL (bounds/EOF violation detected) — proves the framing is falsifiable, not a self-confirming walk.
- NC-ANCHOR-ADJ (mandatory once the client read is claimed): adjacent displacement control — the payload+0x2C (or +0x34) field of the anchored record, extracted/decoded by the same rule, must NOT land in the same destination structure field as +0x30 (verify at the instruction level: distinct source displacement => distinct destination store/field, or the destination claim is downgraded).
- NC-RECORD (mandatory): a second record (different +0x30 value, e.g. ANCHOR_ZERO) passes through the SAME parser path — establishes the mechanism is field-driven, not record-specific (record the shared/differing evidence).
- NC-VALUE (mandatory IF a lookup/comparison mechanism is claimed): a value not satisfying the claimed role (e.g. 0 from ANCHOR_ZERO, or an out-of-domain value) must behave differently in the traced mechanism (e.g. lookup miss / not-found path / different branch), or the mechanism claim is downgraded.

If NO mechanism is reached: NEGATIVE_CONTROL_STATUS = NOT_APPLICABLE_NO_MECHANISM_REACHED with a measured bounded explanation; SEMANTIC_PASS = NO; still execute NC-FRAMING, NC-ANCHOR (feasible part), NC-RECORD and the routing-discrimination controls. Do NOT invent an interpretation solely to manufacture a negative control.

## §14 ANTI-CIRCULAR VALIDATION

For every significant PASS state record: MEASURED_QUANTITY, INDEPENDENT_SOURCE_OF_TRUTH, WHY_NON_CIRCULAR, FAILURE_CASE_DETECTED. Re-reading the same generated CSV is not independent validation. A second script that merely consumes the first script's generated interpretation is not automatically independent. Prefer original physical bytes + independently implemented recomputation. The executor's framing parse must be an in-run implementation (prior tools may be used only as cross-validation, labeled as such); the QC worker's re-parse must share NO code with the executor's implementation.

## §15 BLAST RADIUS VS PRIOR CLAIMS

If a semantic role is established or an earlier placement claim is contradicted, compare against prior claims and report: PRIOR_CLAIMS_CONFIRMED, PRIOR_CLAIMS_NARROWED, PRIOR_CLAIMS_REJECTED, PRIOR_CLAIMS_UNCHANGED. Do NOT rewrite historical reports; use explicit retraction/supersession edges where necessary (in-package). Relevant prior claims to check against if the trace touches them: the id2-domain membership observation (20002@48: 1,364/1,366 members, AMEND_R2_ID2_MEMBERSHIP_20002_48.json, semantic_reference=UNVERIFIED); the open instance->template edge for world statics (JOIN R1 UNRESOLVED §1); WORLD_INSTANCE_TO_MODEL_LINK=NOT_DEMONSTRATED; PLACEMENT_SOURCE=NOT_RECOVERED.

## §16 NO IMPLEMENTATION

This is a Rosetta/RE experiment. Even if the field participates in instance->resource / resource->model / placement / XYZ, do NOT implement the result in the renderer/runtime during this run. Implementation requires separate human authorization after independent post-audit.

## §17 OUTPUT PACKAGE (logical contents; exact filenames may differ when technically justified, but equivalent evidence must exist)

00_CONTROL\: RUN_CONTRACT.md; SOURCE_IDENTITY.md; PREFLIGHT.md (+ AUTHORIZATION_RECORD.md, PREFLIGHT_EXPECTED.md, CONTRACT_FREEZE.json from formalization)

01_RAW\: RECORD_FRAMING.* (full-file census: every record's frame/payload boundaries + the field census rows); FIELD_BYTE_ANCHOR.* (the anchored records' byte-level anchor evidence with bounds assertions); ROUTING_EVIDENCE.*; CLIENT_READ_BYTES.* (VA byte-pins: IMAGE_BASE/VA/RVA/FILE_OFFSET/ORIGINAL_BYTES per load-bearing instruction); RELEVANT_XREFS.*

02_ANALYSIS\: VFS_TO_PARSER_TRACE.md; FIELD_TO_DESTINATION_TRACE.md; DESTINATION_CONSUMER_CENSUS.*; CONSUMER_TRACE.md; NEGATIVE_CONTROLS.md; SEMANTIC_ASSESSMENT.md; BLAST_RADIUS.md

03_SCRIPTS\: analysis/recomputation scripts (executor's; each artifact states its generator + generator SHA — derived-number provenance)

04_QC\: reserved for the FRESH internal-QC worker (QC_REPORT.md + its independent countercheck artifacts + its own tools subfolder)

06_REPORT\: REPORT.md; HANDOFF.md; EVIDENCE_INDEX.md; MANIFEST_SHA256.csv (executor generates it covering executor outputs; known-stale until the final regeneration after QC + PE-MASTER verdict — document this note; manifest self-exclusion rule per the L12 precedent: a manifest cannot contain its own hash)

Original game payloads NEVER go into Git (trivially satisfied: no commit at all); evidence hex excerpts must be bounded, not whole-payload dumps.

## §18 FINAL REPORT FIELDS (REPORT.md must carry ALL of these, exact keys)

RUN_ID; BASE_HEAD; STATIC_ONLY=YES; RUNTIME_EXECUTION_PERFORMED=NO; EXE_IDENTITY_MATCH; VFS_IDENTITY_MATCH; SOURCE_SHA256; RECORD_ORDINAL_OR_PHYSICAL_ID; RECORD_FRAME_START; RECORD_PAYLOAD_START; RECORD_PAYLOAD_LENGTH; FIELD_FILE_OFFSET; PAYLOAD_PLUS_30_RAW_BYTES; PAYLOAD_PLUS_30_DECODED_VALUE; 20002_VFS_TO_PARSER_ROUTING (CONFIRMED|STRONGLY_SUPPORTED|PLAUSIBLE|UNVERIFIED|REJECTED); CLIENT_READ_IDENTIFIED (YES|NO); READ_FUNCTION; READ_INSTRUCTION_VA; READ_INSTRUCTION_RVA; READ_INSTRUCTION_FILE_OFFSET; DEST_FIELD_IDENTIFIED (YES|NO); DEST_STRUCTURE; DEST_FIELD_OFFSET; DOWNSTREAM_CONSUMER_IDENTIFIED (YES|NO); OBSERVED_OPERATION; STATIC_READ_SEARCH_SCOPE; STATIC_WRITE_SEARCH_SCOPE; UNRESOLVED_ALIASES; UNRESOLVED_INDIRECT_CALLS; UNINSPECTED_PATHS; FIELD_IDENTITY_STATUS (CONFIRMED|STRONGLY_SUPPORTED|PLAUSIBLE|UNVERIFIED|REJECTED); FINAL_SEMANTIC_ROLE (bounded wording); FINAL_SEMANTIC_STATUS (same taxonomy); WORLD_INSTANCE_TO_MODEL_EDGE (CONFIRMED|STRONGLY_SUPPORTED|PLAUSIBLE|UNVERIFIED|REJECTED|NOT_TESTED); PLACEMENT_XYZ_RECOVERED (YES|NO); NEGATIVE_CONTROL_STATUS; INDEPENDENT_QC (PASS|PASS_WITH_FINDINGS|FAIL — filled after the QC round; executor leaves it as QC_PENDING); RUN_STATUS (one of the §12 terminal values).

Also: Q1_STATUS_CHANGED=NO; PE_MASTER_QUALIFICATION_CHANGED=NO; GATE_B_CHANGED=NO; M1_CHANGED=NO; M2_CHANGED=NO; M3_CHANGED=NO; COMMIT=NO; PUSH=NO.

Every count states its denominator. Every claim carries its physical evidence pointer + taxonomy status (EVIDENCE_INDEX.md maps claim -> artifact -> status).

## §19 POST-RUN STATE + HARD STOP

PE_MASTER_ROLE = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE; INDEPENDENT_CHATGPT_DESKTOP_POST_AUDIT_REQUIRED = YES; AUTO_FOLLOWUP_RE = NO; NEXT_EXPERIMENT_AUTHORIZED = NO.

After internal QC and the final report: HARD_STOP = YES. No automatic continuation regardless of result. Do not start another placement experiment; do not implement the finding; do not launch the client; do not cross a milestone boundary; do not alter Q1 state.

## §A EXECUTABLE GATES (each gate = machine-checkable predicate; a gate whose predicate is weaker than its label is a finding even if its output is correct)

- S0_INPUT_IDENTITY (hard, fail-closed): ACTUAL_HEAD == 9203b6d1ad5025f4158d5165863594132aaac49f AND EXE size/SHA256 AND VFS size/SHA256 equal the pinned values. FAIL => RUN_STATUS=BLOCKED_INPUT_IDENTITY_MISMATCH; HARD_STOP.
- S1_RECORD_FRAMING (hard for every downstream claim): an in-run executor implementation walks 20002.vfs from byte 0 to EXACT EOF (documented exact-consumption invariant, e.g. sum of strides == file size AND next_offset == file_size); record count N recorded with the derivation; anchored records' FRAME_START/PAYLOAD_START/PAYLOAD_LENGTH recorded; NC-FRAMING executed and FAILS the corrupted variant. Any framing uncertainty => downstream claims stay conditional and the uncertainty is preserved (do not force).
- S2_FIELD_ANCHOR (hard for downstream): bounds assertions present and true for every analyzed record (machine-checkable in the artifact); RAW_BYTES/width/endianness/value recorded with provenance labels (HYPOTHESIS_DERIVED vs RAW per §7); census denominator == record count N (or documented bounds-violation subset).
- S3_ROUTING (classification gate): routing outputs per §8 present; the CLIENT_READ claim for THIS file's field is allowed ONLY if 20002_VFS_ROUTED_TO_GENERIC_PARSER >= PLAUSIBLE with explicit byte-level routing evidence (else CLIENT_READ_IDENTIFIED=NO with the bound recorded; a generic parser +0x30 hit is recorded as candidate context, NOT as a client-read claim).
- S4_CLIENT_READ (hard for the read claim): every claimed instruction byte-pinned (bytes at FILE_OFFSET in the pinned EXE == recorded ORIGINAL_BYTES — machine-verifiable); the full read chain fields per §9 present; decompiler text alone NEVER sufficient.
- S5_CONSUMER_CENSUS (bounded): scopes/counts/unresolved-lists per §10 present; exhaustiveness wording per V2-012.
- S6_MECHANISM_SEMANTICS (classification): KEY_ROLE/LOOKUP_CONTAINER/RESULT_TYPE/RESULT_CONSUMER if a lookup; FIELD_IDENTITY vs OBSERVED_OPERATION vs FINAL_SEMANTIC_ROLE separated; §13 negative control executed if any mechanism/semantic interpretation is proposed.
- S7_WORDING_HONESTY (hard for publication): the report/evidence must NOT apply any §2-forbidden label to the value without in-run byte-level proof; static conclusions labeled STATIC_ONLY; RUNTIME=NOT_TESTED; prior-evidence citations labeled PRIOR_EVIDENCE; if the id2-domain membership is re-measured it is CONTEXT ONLY (membership count, no significance language) and any new membership-style comparison must follow the AMEND-R2 Appendix A constraints (matched alternative domains with pre-frozen seeds, background measured from the controls themselves, offset controls with matched rules; the RETRACTED shuffled-set control is FORBIDDEN).
- S8_PACKAGE_COMPLIANCE (hard): all §17 artifacts exist (or documented equivalents); REPORT carries all §18 fields; git status delta at end == ONLY the new package dir (all 5 pre-existing untracked groups byte-identical); HEAD unchanged; ZERO commits; ZERO staged entries; no Entropia.exe process was launched (STATIC_ONLY); MANIFEST census documented.

## §B PRIOR-EVIDENCE LEADS (LEADS_TO_REVERIFY — NOT TRUTH; every load-bearing use must be re-verified from the pinned bytes in-run; these are entry points, not conclusions)

- VFS grammar (from JOIN R1 04_TOOLS/vfs_common.py + T1/T3): records framed by a 16-byte header {u32 id, u32 size, u16 ver, crc32}, payload follows, records aligned/strided to a per-file base (templates.vfs base=36); 20002.vfs: 1,366 records, ver=1, zeroed CRC fields (crc_gate_active=false in the permissive family walk), exact-EOF walk confirmed by prior strict+permissive readers. RE-DERIVE the header layout, base and stride for 20002.vfs from physical bytes in-run.
- The historical +48 observation (AMEND_R2_ID2_MEMBERSHIP_20002_48.json): "field_offset_in_payload": 48 (= 0x30) — 1,364/1,366 values members of the templates.vfs id2 domain; non-members = records 1014/1015 (zero-indexed), value 0 each; semantic_reference=UNVERIFIED. CONTEXT ONLY.
- Loader-chain VAs (JOIN R1 PE_MASTER_REVIEW claim 5, CONFIRMED there at code level): FUN_0070E810 builds "<classID>.vfs" from a numeric class ID; opens via FUN_00972DF0 (byte pin C7 44 24 1C 80 00 @0x70E841; ".vfs" string @0xA86820); record layout FUN_00959090 (prior hint: parsed 0x58-byte array element fields at offsets corresponding to payload +0x2C/+0x30-class cursor reads); array append FUN_0094D9B0 (ADD [EDX+4],0x58 @0x94D9F5 — 0x58-byte elements). Prior decompilations: JOIN R1 01_RAW\GHIDRA_OUT\ (read-only reference).
- Class-ID machinery (RECEIVER_PROVENANCE run): ArkObjectClassImpl<T, classID> registrations; mangling<->imm32 correlation rule (prior 36/36; examples: 20006=ArkParameterCommon $0EOCG@=0x4E26; Surgeon 20035; Container; RealWorldItem 20034); class ID 20002 = 0x4E22 — an imm32 census of 20002 in the EXE (LE bytes 22 4E 00 00 — verify the encoding yourself before scanning; the historical 296317-vs-296445 LE encoding trap is the recorded failure class) plus the mangling census are candidate routing evidence.
- templates.vfs registry (TEMPLATE_CONSUMER_TRACE run): id2-keyed std::map, singleton DAT_00ba1824; record parser FUN_00730c90; lookup FUN_0072f580; getter FUN_007ce1e0 (8B 41 08 C3) reads +8 of multiple receiver types (receiver-provenance trap — do NOT transfer field identity across receiver types).
- The 20xxx parameter-family channel resolves class->data-file (per JOIN R1); consumers of the parsed parameter arrays were NOT decoded as of JOIN R1 (UNRESOLVED §2) — this run's consumer census is exactly that gap for the +0x30 field.

## §C INTERNAL QC REQUIREMENTS (for the fresh QC worker; PE-MASTER dispatches it separately after the executor returns)

Fresh context; NO shared code with the executor's implementations. Minimum: (1) re-hash EXE+VFS+HEAD; (2) independent re-parse of 20002.vfs framing (own implementation lineage) — record count, anchored records' payload start/length, field offset/value agreement with the executor; (3) byte-verify EVERY load-bearing pinned VA (read bytes at the recorded FILE_OFFSET in the pinned EXE, compare to recorded ORIGINAL_BYTES); (4) verify each gate predicate asserts what its label claims (gate-strength audit); (5) EXECUTE at least one negative control independently crafted by the QC worker (not merely re-run by the executor's script); (6) forbidden-wording sweep over REPORT/evidence (§2 labels without in-run proof; significance language; exhaustiveness overclaims; runtime claims); (7) recompute denominators/counts from raw artifacts; (8) taxonomy/status-algebra check (FIELD_IDENTITY vs OBSERVED_OPERATION vs FINAL_SEMANTIC_ROLE not flattened; run verdict vs claim status separate); (9) EVIDENCE_INDEX claim->artifact census; (10) manifest spot re-hash. QC writes ONLY inside 04_QC\ (+ 04_QC\qc_tools\); verdict PASS|PASS_WITH_FINDINGS|FAIL with findings P0/P1/P2/P3 in 04_QC\QC_REPORT.md. QC does NOT alter executor evidence and does NOT perform new science beyond its counterchecks.

## §D DISPATCH METADATA (for the executor's final handoff)

FINAL_HANDOFF_SCHEMA (executor's final answer = delivery notice ONLY):

AUDIT_OUTPUT_ROOT = <the package root>
FINAL_REPORT_PATH = <root>\06_REPORT\REPORT.md
PRIMARY_EVIDENCE_PATHS = <root>\01_RAW\{RECORD_FRAMING.*, FIELD_BYTE_ANCHOR.*, ROUTING_EVIDENCE.*, CLIENT_READ_BYTES.*}; <root>\02_ANALYSIS\{...}
RUN_STATUS = <terminal value per §12>
HARD_STOP_REASON = <exact one-line reason>

Plus: ACTUAL_HEAD_end (must equal BASE_SHA), git-status-delta statement, no-commit/no-push/no-runtime confirmations, package file count.
