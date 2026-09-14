# HANDOFF — PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914

- RUN_ID: PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914
- BASE_SHA: 3644e5ac9cbf7b5445861e7f5342fb8642741346
- OBSERVED_MASTER_SHA: 3644e5ac9cbf7b5445861e7f5342fb8642741346 (local master and live
  remote master observed equal to BASE_SHA; no drift)
- BRANCH: audit/pe935-ninode-slot17-gb-oracle-minicheck-r1 (isolated worktree
  D:\Eudoria_Reconstruction\worktrees\PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1)
- COMMIT_SHA: the single commit at the branch tip containing exactly this package
  (no other paths); its value and the verified remote branch SHA are reported in the
  executor's return message to PE-MASTER and are verifiable via
  `git rev-parse audit/pe935-ninode-slot17-gb-oracle-minicheck-r1` /
  `git ls-remote origin audit/pe935-ninode-slot17-gb-oracle-minicheck-r1`
- REPORT_PATH: docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/06_REPORT/REPORT.md
- EVIDENCE_PATH: docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/03_EVIDENCE/ (index: EVIDENCE_INDEX.csv)
- GATES_PATH: docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/06_REPORT/STAGE_ACCEPTANCE_GATES.csv
- FILES_CHANGED: exactly the package docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/ (35 files incl. this manifest: 00_CONTROL 6 [2 docs + 4 deterministic scripts], 01_RAW 3, 02_ANALYSIS 6, 03_EVIDENCE 15, 06_REPORT 5; census in MANIFEST_SHA256.csv); nothing else
- FINAL_FUNCTION_IDENTITY_STATUS: **B — STRONGLY_SUPPORTED_GETOBJECTBYNAME**
  (A withheld: Entropia's engine generation is not in the pinned oracle set; the
  slot-position alignment is a measured model anchored at slots 0/1/2/16/17/18/27,
  not an exact/era-exact ABI transfer)
- GAMEBRYO_112_SLOT17: NiNode::SetSelectiveUpdateFlags(bool&, bool, bool&)
  (GetObjectByName = slot 16, +0x40; compiled era VC71 evidence)
- GAMEBRYO_1226_SLOT17: NiNode::ApplyTransform(const NiMatrix3&, const NiPoint3&, bool)
  (GetObjectByName = slot 18, +0x48; compiled evidence)
- ENTROPIA_007B5390_OPERATION: recursive named-object lookup — self-name-check first
  (helper 0x7BF220, name at this+0x0C, inlined strcmp), then child-array iteration
  (+0xCC array / +0xD4 count), recursive virtual dispatch through the child's vtable
  slot +0x44 (its own slot), first-match-or-NULL, thiscall one const char* arg (ret 4)
- OFFSET90_RESULT: GB112 +0x90 = m_kWorld.m_Translate.x; GB12 +0x90 =
  m_kWorld.m_Translate.y; Entropia +0x90 = m_kWorld.m_Translate.x — PROVEN from
  Entropia bytes this run (slot 27 UpdateWorldData: m_kWorld@+0x6C, rep movsd x13;
  slot 16 anchors NiTransform translate@+0x24, scale@+0x30)
- TRANSFORM_TO_MODEL_STATUS: NOT_DEMONSTRATED (unchanged; model-bridge guard held —
  maximum architectural inference recorded: the SF+0x30 NiNode behaves as a
  scene-graph root/container from which named NiAVObjects can be queried, PLAUSIBLE)
- PUSH_STATUS: git push -u origin audit/pe935-ninode-slot17-gb-oracle-minicheck-r1;
  remote branch SHA independently verified after push (reported in the return message)
- HARD_STOP_REASON: none (all gates PASS; no blocker; HARD STOP observed after push)

## Scientific summary

Neither pinned Gamebryo oracle places GetObjectByName at NiNode vtable slot 17
(GB 1.1.2: SetSelectiveUpdateFlags@17 / GetObjectByName@16; GB 1.2.2.6:
ApplyTransform@17 / GetObjectByName@18; the +2 between them is the source-proven
GetGroup/SetGroup virtualization). Entropia 0x007B5390 was therefore identified
behaviorally: it is nearly instruction-identical to the era VC71 compiled
NiNode::GetObjectByName, and Entropia's vtable ABI prefix was measured this run
(slot 0 vector deleting dtor, slot 1 scalar deleting dtor thunk, slot 2 GetRTTI —
proven to be NiNode's via the in-binary NiRTTI static initializer naming "NiNode"
with base NiAVObject), giving a measured +1 slot shift vs both oracles that aligns
the decoded neighbors 16/17/18/27 with GB112's ApplyTransform/GetObjectByName/
SetSelectiveUpdateFlags/UpdateWorldData at 15/16/17/26. Verdict: B
(STRONGLY_SUPPORTED_GETOBJECTBYNAME). The +0x90 secondary question is closed for all
three sides from compiled bytes (world translate X / Y / X respectively).

## Caveats

- Entropia's actual engine generation remains unidentified (47-slot vtable, 2-slot
  dtor prefix, +0x14 class-tail delta; Gamebryo 2.6 materials on disk are outside the
  pinned oracle set and were not used).
- Entropia vtable slots 3..15 were not decoded; the alignment model is anchored at
  seven slots, not the full prefix.
- GB12 compiled evidence is from the project's VS2022 rebuild of a SHA-verified
  byte-identical src copy (era-VC71 evidence exists only for GB112).
- All findings are STATIC-ONLY; the client never ran.
- The SceneFeeder downstream consumer chain (returned_object+0x90 -> ...) was NOT
  decoded and stays as published INPUT.
