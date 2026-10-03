# PE_MASTER_REVIEW — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

Issued by PE-MASTER (supervisory controller; independent deep audit; dispatched per the
human's run-specific authorization of 2026-10-03). Mode: ADVISORY_PRE_QUALIFICATION.
CANONICAL_GATE_EFFECT = NONE. RUN_CLASS = LOAD_BEARING (PE-MASTER declaration per POM
A1.1); RUN_TYPE = BOUNDED_STATIC_PLACEMENT_RE. Audited: BASE_SHA
743f9fac2dd5c9e94eaba074b46903b4d3686b46; the working-tree package (commit = the
publication commit that adds this package; discover via
`git log -1 -- docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z`).

## VERDICT

MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE).
RESULT_LEVEL = B (PARTIAL RESOURCE/SCENE CHAIN) — AGREED, honest (CONTROL-2 correctly
FAIL->UNKNOWN; the LEVEL-A edge was not established and was not forced).
Fresh-QC verdicts stand: QC_PASS_WITH_FINDINGS (P2-1/P3-1/P3-2 closed by the one
allowed repair round AMEND-1..5; RE_QC_PASS; P3-A/P3-B/P3-3 carried as errata).

## COVERAGE (PE-MASTER own audit)

FULL READ: all package documents (DRAFT_FINAL_REPORT, HANDOFF, AUTHORIZATION, PREFLIGHT,
RUN_PLAN, SELECTION, TRACE_EDGE_BLOCKS, NOT_CHECKED, RETRACTIONS_SUPERSESSIONS,
CLAIM_MATRIX 15 rows, CONTROLS, ORACLE_RECORDS, AMEND_LOG_R1, QC_AUDIT_R1, QC_RECHECK_R1),
the binding contract file (SHA AB192885... verified), and the load-bearing generator
sources c1_census.py, c2_caller_census.py, c9_listing_windows.py, c10v2_byte_crosscheck.py,
c12_ninode_vtable_repin.py. INDEPENDENT PHYSICAL COUNTER-CHECKS (PE-MASTER own instruments,
outside the project tree, 61 checks): EXE identity/ASLR/PE mapping; the load-bearing byte
pins of E1/E2/E3/E6/E8/E9 (lookup window, emitter chain incl. MOV ECX/EAX, CALL rel32
targets, pair stores, callback imm32 0x008BD720, getter 8B 41 08 C3, ctor vtable store
C7 06 F4 CC A8 00, PUSH 0x3ED3, strings); NiNode vtable slots 17/27; RTTI chains
(.?AVNiControllerSequence@@ / .?AVNiNode@@ / .?AVArkObject@@); own ArkVFS02 walks
(templates.vfs 5,438 records EOF-exact 0 CRC; 20002.vfs 1,366 EOF-exact; record 4508
bytes+CRC+A@96,516+D_f32 exact; record 11963 leg_BASE length-prefixed list; off48
membership 1,364/2=[0,0]); own BNT2 index walk (5,596 entries; anchors 296445.nif
@395,268,773, 551661.nif @395,323,507; absences 296446.nif/4508.nif/460563.nif confirmed
— the E3 falsifier has teeth); own raw .text census scans (reader FUN_0072FA30: 0 E8 /
exactly 1 E9 @0x00452497 / 0 imm32 + thunk decode CALL 0043A550+MOV ECX,EAX+JMP;
lookup 25 sites; ctor 55; pump 13 incl. 0x006CB7CF; driver 3; getter 808 raw);
slot-27 copy chain (LEA ESI,[EBX+0x38] @0x7E4844; LEA EDI,[EBX+0x6C] @0x7E4847;
MOV ECX,0xD; F3 A5 @0x7E484F); package counts (C9 20 windows/962 instructions;
C10V2 962/962 + 113/113; decompiles 88; C2 targets 19; T01 25/23; T02 1/1;
T10 817/367 Ghidra vs 808 raw — method delta confirmed); extension census (text only).
NOT CHECKED by PE-MASTER: sources of c3/c4/c5/c6/c7/c8/c10(v1)/c11 (same-pattern Ghidra
extractors; their outputs were double-verified: fresh-QC full read + PE-MASTER physical
re-derivations of the load-bearing outputs; c10v1 is protected superseded instrument
history); non-load-bearing decompile bodies; the 23/11/6 unique-caller derivations
(QC-verified; PE-MASTER verified the callsite counts); budget-usage counts (~14/~27/~10 —
not re-countable from artifacts; disclosed UNVERIFIED, hard limits independently
confirmed unexceeded); artifact_index row-by-row re-hash (performed twice by QC/re-QC
39/39; PE-MASTER verified the physical census); the untracked foreign package
PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928 (used as LEAD only; its observation
1,364/1,366 independently REPRODUCED by the run's C1 and by PE-MASTER's own walk);
full Models.bnt join re-run (bounded reuse per contract §2; the anchor re-pinned and
PE-MASTER-verified).

## CLAIM MATRIX (PE-MASTER verification of the run's load-bearing claims)

E1 record->parser->registry: CONFIRMED (PE-MASTER own file walk + record bytes + CRC +
reader census 1-caller thunk + QC store-order re-derivation).
E2 lookup id2->template: CONFIRMED (PE-MASTER byte reads B1-B5 + 25-site own scan).
E3 getter A -> pair {0x66,A} -> scheduler: CONFIRMED (PE-MASTER byte chain B6-B15 +
getter body; callback imm32 pinned; prose byte-string defect F-2 recorded, data correct).
E4 A=296445 -> "296445.nif" join anchor: CONFIRMED (PE-MASTER own BNT2 walk; full join
= bounded reuse of JOIN R1 3,618/3,618, correctly disclosed; runtime physical open stays
STRONGLY_SUPPORTED — provider bodies not decoded).
E5 instance path structure + NiControllerSequence identity: STRONGLY_SUPPORTED structure
(identity CONFIRMED by PE-MASTER RTTI walk; R-1 correction accepted; historical
"named instance" phrase carried no class identity — blast radius statement agreed).
E6 placement-record setters as runtime transport (record != NiAVObject): CONFIRMED
(offsets vs m_kLocal@+0x38/m_kWorld@+0x6C; position provenance runtime — the honest
chain-breaker).
E7 attach thunks != NiNode::AttachChild (Ark LOD/attachment state machine): CONFIRMED as
classification (oracle negative matcher; QC Z03-Z07 verification; CONTROL-3 PASS).
E8 scene root NiNode + SetName("NetImmerseScene::Root"): CONFIRMED (PE-MASTER vtable store
+ string + SetName prolog + RTTI).
E9 construction sources (hardcode/message/attribute; NONE reads templates.vfs): PARTIALLY
CONFIRMED / OPEN — agreed; census basis PE-MASTER-verified (1 reader via thunk; driver
sites); bounded to the censused machinery.
E10 template list2 payload vec3 -> slot-position lerp: CONFIRMED as payload-derived
transform data (slot class UNKNOWN — honest).
E12a slot 17 = 0x007B5390 re-pin: CONFIRMED (PE-MASTER vtable read).
E12b 20002 rec0 = 11963 re-pin + 1,364/1,366 membership: CONFIRMED (PE-MASTER own).
E12c slot 27 UpdateWorldData-shaped: STRONGLY_SUPPORTED — agreed and STRENGTHENED: the
full m_kLocal->m_kWorld copy chain is physically present in the probe window (see F-1).
X1/X2: CANDIDATE/UNVERIFIED + data facts CONFIRMED — agreed, not promoted.

## GATE PREDICATES

LEVEL A/B/C definitions: contract-frozen; B correctly assigned (A's requirements
unmet, honestly). CONTROL-1..5: all NEW_CONTROL_EXECUTED with tested claim / expected
discriminator / actual observation / source identity / status; CONTROL-2 FAIL->UNKNOWN
is the documented reason RESULT_LEVEL is not A — the control has teeth. CONTROL-3's
HISTORICAL_CONTROL_REUSED correctly labeled. Limits: 88/120 detailed, 3/3 records,
3/3 oracle mechanisms, shortlist 3, deep trace 1, repair rounds 1/1 — all verified.
GATE-DESIGN NOTE: CONTROL-4 verifies C9-vs-EXE (data) but no layer machine-diffs prose
byte-strings vs C9 — proven by two prose transcription defects (P3-1 caught by QC;
F-2 caught by PE-MASTER). Recorded as a design lesson; the load-bearing data layers are
unaffected (962/962 + 113/113).

## FINDINGS (PE-MASTER; all preserved; dispositions final)

F-1 [P2 CORRECTNESS — RESOLVED BY ADJUDICATION]: S-4 / E12(d) / ORACLE_RECORDS
Mechanism-3 / DRAFT_FINAL P1(b) state the historical NINODE_SLOT17 description
"rep movsd x13" was "NOT reproduced within this probe window (1 consecutive rep movsd
found)". REJECTED AS WORDED. The historical package's evidence says "rep movsd 13 dwords"
/ "mov ecx,0xD; rep movsd — 13 dwords = 52 bytes" — ONE instruction with ECX=13, not 13
consecutive instructions. PE-MASTER physically re-verified INSIDE the run's own 512-B
window: LEA ESI,[EBX+0x38] @0x7E4844; LEA EDI,[EBX+0x6C] @0x7E4847; MOV ECX,0xD
@0x7E484A; REP MOVSD @0x7E484F — the historical slot-27 observation is REPRODUCED
EXACTLY by this run's own probe window. Root cause (source-verified): the
c12_ninode_vtable_repin.py instrument counted consecutive rep movsd instructions
("x13 expected", predicate consec>=10) while its own docstring correctly described the
52-byte copy — the notation misreading was baked into the instrument, honestly disclosed
by the run as a "discrepancy" instead of a false retraction. DISPOSITION: the
"discrepancy" claim fragment is RETRACTED as worded; the historical claim stands
CONFIRMED (and this run's slot-27 STRONGLY_SUPPORTED status is unaffected/strengthened);
correction carried by this review + the FINAL_REPORT erratum (the one repair round was
consumed; contract §8: record without cosmetic reopening). No historical package
requires modification; no adjudication beyond this review is needed.
F-2 [P3 HYGIENE]: TRACE_EDGE_BLOCKS.md E3 prose byte string "E8 67 5E 10 00" — physical
bytes are "E8 67 A2 10 00" (rel32 target 0x007CE1E0 correct; 0xA2 signed-hex residue
-0x5E — the same class as P3-1). Caught by PE-MASTER; missed by both QC rounds. The
pinned data (C9/C10V2) is correct. Erratum.
P3-A (re-QC): AMEND_LOG_R1.md sweep-statement over-claims "no remaining '68 2D'"
(2 legitimate protected instrument-history occurrences exist). Erratum.
P3-B (re-QC): AMEND_LOG_R1.md "Repair UTC: 2026-10-03T09:04:00Z" does not reconcile
with physical mtimes (07:50:06Z..07:50:46Z window). Treat as declared-not-measured.
Erratum.
P3-3 (QC): T10 getter census 817 (Ghidra) vs 808 (raw) — method delta; PE-MASTER's own
raw scan = 808 (confirmed). Method note stands.
F-4 [P3 OBSERVATION]: E11 numbering gap (E1..E10, E12) — no dropped claim (TRACE and
CLAIM_MATRIX are consistent); non-contiguity only. No action.
F-5 [P3 OBSERVATION]: the shorthand "JOIN R1" names two different packages
(PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 — committed — for the 3,618/3,618 join;
PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928 — foreign untracked — for the
1,364/1,366 observation and the "AMEND-R2 F3" wording). Both attributions are factually
correct in context; the untracked package was used as a contract-permitted LEAD and its
observation was independently REPRODUCED (run C1 + PE-MASTER). Future runs should cite
full package names.

## CANON CONFLICTS / RETRACTIONS

One conflict, resolved: F-1 (above). The run's own retraction R-1 (NiControllerSequence)
is accepted; its blast-radius statement (no historical claim asserted the class identity)
is verified against the published record. Supersessions S-1/S-2/S-3 consistent (all
re-pins REPRODUCED by PE-MASTER); S-4 superseded by the F-1 adjudication (no discrepancy
exists). No retracted claim is cited as standing evidence anywhere in the package.

## AUDIT OF AUDITOR

Fresh QC (QC_AUDIT_R1): genuinely independent (own PE mapper / VFS walker / BNT2 parser /
call-site scanner / RTTI walker; instruments present in 07_QC/raw; PE-MASTER independently
reproduced the key re-derivations). Found 3 real defects (P2-1/P3-1/P3-2). Blind spots:
endorsed the S-4 "discrepancy" framing (same-engine notation misreading); missed the
second prose byte defect (F-2). Focused RE-QC (QC_RECHECK_R1): repairs verified true by
own measurements; integrity via content baselines + mtime corroboration; honest baseline
disclosure (no pre-repair hash list — mitigated); repeated the S-4 endorsement. Both QC
verdicts stand; the two blind spots are corrected by this review.

## STATUS ALGEBRA (kept separate)

CLAIM_KNOWLEDGE_STATUS: as per claim matrix above. FINDING_DISPOSITION: F-1
ACCEPTED+RESOLVED-BY-ADJUDICATION (retraction of the wording, not of the evidence);
F-2/P3-A/P3-B ACCEPTED (erratum); P3-3 ACCEPTED (method note); F-4/F-5 recorded
(observations). EXECUTABLE_GATE_STATE: controls/limits all verified PASS (CONTROL-2
honestly FAIL for the world-instance claim). HUMAN_REVIEW_STATE: PENDING (Desktop
post-audit of the exact pushed SHA is the contract's NEXT_ACTION; PE-MASTER remains
PROVISIONAL_UNTIL_QUALIFIED). PERSISTENCE_STATE: this publication commit.
APPLICATION_STATE: n/a (no doc proposals). MILESTONE_STATE: EU935-M1 unchanged — OPEN;
M1_CLOSED = NO; no gate effect.

## CHECKPOINT DELTA

NONE (no canonical checkpoint update; the entrypoint row + this package are the record).

## NEXT EXPERIMENT (DESIGNED, NOT EXECUTED, NOT AUTHORIZED)

The run's proposal is the sound P0 candidate: decode the scheduler callback
FUN_008BD720 + the type-0x66 provider chain down to the NIF load (closes the model-load
body; NiStream oracle comparison), and decode the class-20006 property-tag-6 WRITERS
(if ever file-fed, FAMILY-P/T merge into a real physical-record->placement channel).
NEXT_EXPERIMENT_AUTHORIZED = NO (human's decision). Do not run it.

## GOVERNANCE BLOCK (unchanged per contract §10)

PE_MASTER_STATUS = PROVISIONAL_UNTIL_QUALIFIED; Q1_STATUS = UNCHANGED;
GATE_B_CANONICAL_AUTHORITY = BLOCKED;
GATE_C_R3_HISTORICAL_STATUS = MILESTONE_POST_AUDIT_PASS_FOR_AUDITED_SHA;
GATE_C_HISTORICAL_AUDITED_SHA = 666a822e1109b3aa68be96fece932def3236424b;
M1_CLOSED = NO; M2_M3_AUTHORIZED = NO; CANONICAL_GATE_EFFECT = NONE;
NEXT_EXPERIMENT_AUTHORIZED = NO; NEXT_ACTION = DESKTOP_POST_AUDIT_OF_EXACT_PUSHED_SHA.
