# GAMEBRYO ORACLE RECORDS — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

ORACLE_MECHANISMS_MAX = 3 (contract §5). Mechanisms selected for the traced
path only; no Gamebryo inventory attempted.

## Oracle source identities (pinned at preflight and used here)

| Source | Version | Physical path | Size (B) | SHA256 |
|---|---|---|---|---|
| Gb12 source tree | Gamebryo 1.2.2.6 source | D:\gamebyroengine\extracted\Gb12_Source\ | (tree) | not hashed as a whole; per-file locators given below |
| NiMain.lib | Gamebryo 1.1.2 Evaluation, VC71 ReleaseLib | D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib | 3,073,590 | FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597 |
| Target binary | PCG/EU 9.3.5 | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 |

Oracle evidence below = source LOCATORS + hashes + short derived descriptions
(no source dumps committed).

---

## MECHANISM 1 — NiObjectNET::SetName / NiNode ctor (scene-root naming)

- ORACLE: Gb12 source `CoreLibs\NiMain\NiObjectNET.cpp` line 112
  (`void NiObjectNET::SetName(const char* pcName)`: `delete[] m_pcName; if
  (pcName) { m_pcName = new char[strlen(pcName)+1]; strcpy(...); } else
  m_pcName = 0;`) and `CoreLibs\NiMain\NiNode.cpp` line 34
  (`NiNode::NiNode(unsigned int uiNumChildren) : m_kChildren(uiNumChildren) {}`).
  NiMain.lib (1.1.2) vtable canon for NiNode exists from the
  NINODE_SLOT17 run (32 slots there vs Entropia's 47) — NOT re-derived here.
- HYPOTHESIS: the Entropia function that names the scene root
  ("NetImmerseScene::Root", reached from FUN_00933310) is a NiObjectNET::SetName
  counterpart writing m_pcName at object+0xC, and the object is a NiNode whose
  ctor initializes the children array.
- PCG935 MATCH: O02 decompile of FUN_007B67E0: `operator delete([this+0xC])`,
  inline strlen loop, `operator new(len+1)`, inline strcpy loop into
  `[this+0xC]`, else `[this+0xC]=0` — structurally identical operation sequence
  to the oracle source. O01 decompile of FUN_007B6000: writes
  NiNode::vftable (RTTI-labeled symbol present in the binary), inits the
  children array object (LEA ECX,[ESI+0xC8] -> FUN_00788480(param,1)) and the
  effects list (@+0xE0 vft NiTPointerList<NiDynamicEffect*>).
- TARGET_LOCAL PROOF: raw ctor bytes `... 8D 8E C8 00 00 00 ... C7 06 F4 CC
  A8 00 ...` (C12): the vtable immediate 0x00A8CCF4 is stored by `MOV
  dword ptr [ESI], imm32` at 0x007B6041; vtable slot 17 = 0x007B5390
  (historical GetObjectByName-like anchor, MATCH); slot count 47 dumped from
  raw bytes. SetName store target +0xC agrees with the NINODE_SLOT17 layout
  (name member @+0x0C).
- ALTERNATIVE MATCHES / VERSION CONFLICTS: GB12 moved the name member to
  +0x08 (per NINODE_SLOT17 cross-version table); Entropia uses +0xC — the
  operation matches the SOURCE ALGORITHM, the member offset matches the
  Entropia-local layout (1.1.2-era +0x0C), NOT GB12's +0x08. No offset was
  transferred from either oracle.
- SCOPED STATUS: **STRONGLY_SUPPORTED** — FUN_007B67E0 = NiObjectNET::SetName
  counterpart (behavioral identity, member-offset identity with the Entropia
  NiNode RTTI chain); FUN_007B6000 = NiNode ctor counterpart. Not
  CONFIRMED-as-identity because no binary symbol directly names either
  function and the era generation is unidentified (NINODE_SLOT17 canon).

## MECHANISM 2 — NiNode::AttachChild (used as a NEGATIVE matcher for E7)

- ORACLE: Gb12 source `CoreLibs\NiMain\NiNode.cpp` line 52
  (`AttachChild`: assert/NULL-guard; `pkChild->IncRefCount()`;
  `pkChild->AttachParent(this)`; `m_kChildren.AddFirstEmpty(pkChild)` or
  `m_kChildren.Add(pkChild)` depending on `bFirstAvail`; `DecRefCount()`).
- HYPOTHESIS (to falsify): the pending-attach thunks FUN_0077C0B0/F0/120
  (reached from the model pending-attach processor FUN_006CB3C0) are scene-
  graph AttachChild calls.
- PCG935 MATCH (falsified): the implementations FUN_00779D60/E20/F80/C80/E70
  (Z03-Z07) contain NONE of the oracle's distinguishing operations: no
  NULL-guarded child, no refcount increment/decrement pair, no
  AttachParent-equivalent, no children-array insertion. They implement a
  state machine (state @+0x60 in {0..4}, partner @+0x90, transition floats,
  a search over an array @+0x30 with count @+0x38 gated by fields @+0xAC /
  +0x5C / +0x38) over the Ark visual-manager object.
- TARGET_LOCAL PROOF: thunk bytes pinned (L13: `8B 4C 24 04 6A 01 E8 A5 DC
  FF FF` @0x0077C0B0 -> FUN_00779D60; `E8 27 DD FF FF` @0x0077C0F4 ->
  FUN_00779E20); all 962 window bytes verified against the raw EXE (c10v2).
- ALTERNATIVE MATCHES: a name-based ("attach") or slot-number-based match
  would label these as AttachChild — the behavioral comparison rejects it.
- SCOPED STATUS: **REJECTED (as AttachChild); CONFIRMED as an Ark LOD /
  attachment state machine.** This is CONTROL-3 (oracle transfer) executed.

## MECHANISM 3 — NiAVObject UpdateWorldData (transform propagation target)

- ORACLE: Gb12 source `CoreLibs\NiMain\NiAVObject.cpp` (UpdateWorldData /
  UpdateRgid machinery) + the NINODE_SLOT17 canon (historical, its own run's
  evidence): Entropia NiNode m_kLocal @+0x38, m_kWorld @+0x6C, world
  translate X @+0x90; slot 27 described as UpdateWorldData.
- HYPOTHESIS: the Entropia NiNode vtable slot 27 function propagates
  local->world transforms (m_kLocal @+0x38 multiplied with a parent's
  m_kWorld @+0x6C), giving the TARGET semantics for the transform edge: what
  a scene-inserted instance's transform would look like (versus the placement
  record's +0x08/+0x14 fields traced in E6).
- PCG935 MATCH: vtable located from raw ctor bytes (0x00A8CCF4); slot 27 =
  0x007E4820; its first instructions: `SUB ESP,0x34; PUSH EBX; MOV EBX,ECX;
  MOV EAX,[EBX+0x24]; TEST EAX,EAX; ... LEA ECX,[EBX+0x38]; ...
  LEA ECX,[EAX+0x6C]; CALL FUN_006EB380` — reads the object's +0x24 (parent
  pointer), +0x38 (m_kLocal) and parent's +0x6C (m_kWorld), then calls a
  transform-multiply helper. Shape matches UpdateWorldData.
- TARGET_LOCAL PROOF: raw vtable dump (C12) + slot bytes read directly from
  the EXE; offset constants +0x38/+0x6C match the historical canon pins.
- ALTERNATIVE MATCHES / DISCREPANCY: the historical description "writes
  m_kWorld at +0x6C via rep movsd x13" was NOT reproduced inside the first
  512 B of slot 27 (only 1 consecutive rep movsd found); the multiply-copy
  may live deeper in the function or in FUN_006EB380. This is recorded as a
  probe-window discrepancy, NOT as a contradiction of the historical run's
  own byte evidence (this run did not re-derive their window).
- SCOPED STATUS: **STRONGLY_SUPPORTED (UpdateWorldData-shaped; distinctive
  non-exact match per contract §5).** Used ONLY to state the target transform
  semantics; no offset/slot transfer beyond the Entropia-local re-pins.

---

## Transfer rules honored (contract §5)

- No offsets, slot numbers, layout constants, ABI, or semantics were
  transferred from GB12/GB112 to the target; every target-side constant was
  re-measured from Entropia bytes (C10v2/C12).
- Same NIF version does not imply same engine generation — no such claim made.
- Matching bytes confirm instructions only; function identity above is
  capped at STRONGLY_SUPPORTED except where the binary's own RTTI symbols
  (NiNode::vftable, NiControllerSequence::vftable) directly label the object
  class (object identity, not function identity).
- GB 2.3/2.6/3.2 oracles were NOT needed for the three mechanisms above;
  if a future trace needs era-exact AttachChild/NiStream bodies, that need is
  recorded in the handoff (NOT_CHECKED item).
