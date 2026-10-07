# INPUT_IDENTITIES — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

Written BEFORE any input is treated as evidence (contract §1). All SHA256 values
were measured by this executor from the physical files (Get-FileHash / Python
hashlib) at preflight time 2026-10-06T22:4x–22:5x-07:00, except the BASE-pinned
package files whose identity is given by (BASE_SHA, repo_path) — those were read
via `git show 24f45e0...` from the exact BASE commit, never from the working
tree. Machine-readable mirror: INPUT_IDENTITIES.json.

## 1. Primary binaries

| input | size_bytes | SHA256 | role |
|---|---|---|---|
| D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | THE pinned static analysis target (read-only byte source for every decode; re-verified at preflight) |

Ghidra: NO Ghidra project is used by this run. GHIDRA_PROJECT_USED = NONE.
Reason: establishing a trusted program-identity chain for an existing project
was not performed within this run's bounds, and labels/pseudocode do not
substitute for bytes (contract §1). All analysis is byte-level: own PE mapper +
capstone 5.0.7 decode + own arithmetic recomputation (the established Method B
of the prior published runs). No program database is created or published.

## 2. Contract and authorization inputs (pinned at dispatch)

| input | size_bytes | SHA256 |
|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_JOIN_PROMPT_REVIEW_20261006\OPENCODE_MODEL_CHILD_JOIN_REVIEWED.md | 15,348 | F929D2C03B1D078BD69BDD206B0CF51DE5F393A0CE6D39618ED87819D043F3C8 |
| C:\Users\User\Documents\ChatGPT\PE\PE_SCENEFEEDER_MODEL_JOIN_COMPARISON_RESEARCH_R2_20261006\HANDOFF_NOTES.md | 1,641 | D531B56AB0C1FD180A31DABC5DACAAE289372CA7B8FD8EC8BAAC565FAB0E4355 |

## 3. Private research reports (pinned sources; NOT canonical authority)

Each re-verified by this executor at preflight BEFORE use (contract §2). All
three matched their dispatch-pinned hashes, therefore all three ARE used as
declared pinned inputs. Supersession statuses preserved per contract.

| input | size_bytes | SHA256 (re-verified) | status |
|---|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_SCENEFEEDER_ENGINE_COMPARISON_RESEARCH_20261006\REPORT.md | 17,914 | 26CBF3AB57CEB99DB90760AB503E58AF5D42DCE5E2AB6DA428578DBD4DCD64C1 | pinned private research; architectural/fingerprint input only |
| C:\Users\User\Documents\ChatGPT\PE\PE_935_NIRTTI_CLASS_IDENTITY_DESKTOP_RESEARCH_R1_20261004\REPORT.md | 13,385 | D6B81792BC1AA99124C772EF05C6690A94BFF97DD11B09CCECC3B226C852547A | pinned private research; RTTI/class-identity input only |
| C:\Users\User\Documents\ChatGPT\PE\PE_935_PLACEMENT_BRIDGE_DESKTOP_POST_AUDIT_20261003\REPORT.md | 15,300 | 598DA71AC3DC1F6577EA2AF9E25ED8CF9C53A2603899D08B8AA3307A8CC35396 | pinned private research; independent Desktop post-audit of the bridge run |

## 4. BASE prior packages used as evidence candidates (read via git show from BASE_SHA 24f45e0108b922c26ff584fee9ef7749de0390b6)

Identity of each item = (BASE_SHA, path). The supersession status of each prior
package is carried explicitly in PRE_REGISTERED_ANCHORS.md and CLAIM_MATRIX.csv;
the old whole-package MASTER_ACCEPTED of the source run of the instance-key
family is SUPERSEDED by the published POST_AUDIT_CORRECTION package.

- docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/
  — FINAL_REPORT.md (SF island: SF ctor chain, SF+0x30 NiNode creation,
  ExtraData registration, DEFERRED_LEAD FUN_007B68B0 boundary).
- docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006/
  — FINAL_REPORT.md, SUPERSESSION.md (records-level correction of the above;
  RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH preserved).
- docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
  — 06_REPORT/DRAFT_FINAL_REPORT.md (authoritative science),
    06_REPORT/FINAL_REPORT.md (publication record),
    02_ANALYSIS/TRACE_EDGE_BLOCKS.md (E1–E12 with VAs: emitter FUN_006C3F50
    request {0x66,A}, scheduler entry FUN_006C3640 with callback FUN_008BD720,
    instance creator FUN_006CB6F0, named-instance FUN_006CB020, pending-attach
    FUN_006CB3C0, attach thunks, E7 negative).
- docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/REPORT.md
  (SF+0x30 = refcounted NiNode; writer census 2 PROVEN writers; slot 17
  positive control 0x0050A05B/0x0050A064).
- docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/06_REPORT/REPORT.md
  (SF vtable 6 slots; slot 3 = FUN_0050A050 GetPosition(out, name); primary
  path reads the +0x30 link and dispatches vtable+0x44).
- docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/06_REPORT/REPORT.md
  (slot 17 = 0x007B5390 = GetObjectByName-like, STRONGLY_SUPPORTED (status B);
  NiNode children array +0xCC / count +0xD4; m_kWorld +0x6C; translate +0x90).
- docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/06_REPORT/REPORT.md
  (slot 3 primary path = named lookup on SF+0x30 root; +0x90 = world translate;
  conversion pair FUN_00437F70 / FUN_0082B5A0).

## 5. Oracle source files (the single allowed oracle mechanism location set)

Used ONLY if/when the ONE oracle mechanism (NiNode::AttachChild /
NiAVObject::AttachParent fingerprint) is applied. Identities re-measured at use
time and compared against the earlier research's SOURCE_IDENTITIES.json
(expected values below from PE_SCENEFEEDER_ENGINE_COMPARISON_RESEARCH_20261006):

| file | expected size | expected SHA256 |
|---|---|---|
| D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiNode.cpp | 33,897 | 38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016 |
| D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiAVObject.cpp | 33,215 | 72E0837149B03CCDA171BDF5E68E1E1F8C2712B2F10E7957AC3EC26344CA5EA7 |

Role: NON_EXACT_PCG_SOURCE_ORACLE (architectural fingerprint only; no ABI/
offset/semantic transfer to PCG; no copying of source text into the repo).

## 6. Private scratch (outside the repo; registered; not published)

SCRATCH_DIR = C:\Users\User\AppData\Local\Temp\opencode\PE_935_MODEL_CHILD_JOIN_R1_20261006
Contains this run's private analysis tooling (PE byte reader, capstone decode
helpers, census scripts) and intermediate outputs. Will be inventoried at the
end of the run; not part of the package or the manifest.

## 7. Preflight verification record (measured)

- git fetch origin: performed 2026-10-06T22:49:05-07:00 (local); LOCAL_HEAD =
  24f45e0108b922c26ff584fee9ef7749de0390b6 == origin/master == actual remote
  (git ls-remote) == EXPECTED_BASE_SHA. MATCH.
- Relevant tracked changes: NONE (git status --porcelain: no modified/staged
  tracked paths; only untracked).
- Foreign untracked inventoried (6 roots, untouched by this run):
  docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.
  NOTE: PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and
  PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/ are foreign untracked
  (NOT in BASE) and are therefore NOT used as evidence inputs by this run
  (contract §2 restricts prior anchors to BASE packages + the pinned private
  reports). They are listed here only as inventory.
- OUTPUT_ROOT absent before run (collision check PASS); created by this run.
