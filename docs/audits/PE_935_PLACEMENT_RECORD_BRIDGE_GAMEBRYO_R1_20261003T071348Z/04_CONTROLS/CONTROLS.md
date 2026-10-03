# CONTROLS — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

Contract §7: every load-bearing edge has two check methods, at least one
directly from PCG physical bytes. Ghidra export + its parser = one source line
(honored: Method A = Ghidra; Method B = this run's own raw-EXE/physical-file
readers). Byte checks verify instructions, not selection/object identity/
semantics (stated per control).

---

## CONTROL-1 — False candidate / false access (NEW_CONTROL_EXECUTED)

- TESTED CLAIM: "the 4-byte load [ECX+0x08] (FUN_007CE1E0) reads the template
  record's A (model id) field" — i.e. that displacement +0x08 in this context
  is specific, not a generic coincidence.
- EXPECTED DISCRIMINATOR: the same displacement (+0x08) on DIFFERENT object
  types in the same traced machinery must demonstrably mean something else;
  a displacement-value search must be shown to produce false positives so the
  context requirement is proven, not assumed.
- ACTUAL OBSERVATION:
  1. On an RB-tree node, +0x08 is the LEFT-child pointer: FUN_004D1430
     (mapfind, byte window L03) walks `iVar2 = *(int *)(iVar1 + 8)` for the
     left subtree while comparing the key at node+0x10 — same displacement,
     completely different meaning.
  2. FUN_007CE1E0 itself has **817 CALL callsites / 367 unique callers**
     (own census C2, T10) — it is a generic field-getter family member; e.g.
     in the VFS per-record reader FUN_00971AD0 (Z10) the same getter is called
     on a FILE object and its output is stored into the record's output slot
     — NOT a model id.
  3. In FUN_00726E70 (ArkObject ctor, D03) the getter is invoked on the
     TEMPLATE object (param_1) and its result goes to entity+0x28 — the
     object-provenance (ECX = lookup result of E2) is what makes it "A",
     not the displacement.
- SOURCE_IDENTITY: Entropia.exe E7785430... (pinned); windows L03/L05 +
  census C2 from this run's own instruments.
- STATUS: **PASS** — the A-read claim survives only with ECX-provenance
  (pinned in E2/E3: `MOV ECX, EDI` @0x006C3F6E between lookup and getter);
  bare displacement matching is demonstrably a false-positive generator.

## CONTROL-2 — Template/resource vs instance (NEW_CONTROL_EXECUTED)

- TESTED CLAIM (attempted falsification): "the runtime placement record built
  by FUN_00567170/FUN_005B5F90/FUN_00567770 is a WORLD instance of the
  templates.vfs record" (i.e. that the physical record maps to a world-
  instance identity).
- EXPECTED DISCRIMINATOR: any of the following would rescue the claim:
  (a) a construction driver that reads templates.vfs itself (the only reader
  is the registry loader); (b) the placement record carrying the template's
  own identity fields (id2) at its identity slot; (c) the placement record
  being a NiAVObject (m_kLocal/m_kWorld offsets).
- ACTUAL OBSERVATION:
  - FUN_0072FA30 (the ONLY templates.vfs reader; census T02: 1 caller) is the
    registry loader; NONE of the censused construction drivers reads any VFS
    file — their id2 inputs come from code immediates (E9a: PUSH 0x3ED3
    byte-pinned), the message dispatcher (E9b: FUN_004B18D0 switch), or
    runtime attributes (E9c: property tag 6).
  - The placement record's identity key (@+0) is set by the deserializer from
    the message cursor (FUN_007453D0 reads key u32 first — W08), not from the
    template; the template is only looked up where needed as a DEFINITION.
  - The placement record is NOT a NiAVObject: setters store at +0x08/+0x14/
    +0x20 (E6) vs the pinned NiAVObject m_kLocal @+0x38 / m_kWorld @+0x6C
    (C12/Mechanism-3).
- SOURCE_IDENTITY: Entropia.exe (pinned) + templates.vfs (pinned) + census
  C2/C4/C6/C8 + byte windows L03/L09/L10/L16.
- STATUS: **FAIL for the world-instance claim** → world-instance identity
  from a physical record = UNKNOWN (kept UNKNOWN, not passed). This control
  is the documented reason RESULT_LEVEL is not A.

## CONTROL-3 — Oracle transfer (NEW_CONTROL_EXECUTED; one historical reused)

- TESTED CLAIM: "the pending-attach thunks FUN_0077C0B0/F0 are Gamebryo
  NiNode::AttachChild" (the tempting name-based/slot-based match).
- EXPECTED DISCRIMINATOR: oracle AttachChild's distinctive operation set
  (NULL guard, IncRefCount/DecRefCount pair, AttachParent, children-array
  insertion).
- ACTUAL OBSERVATION: none of the four operations appear in the callee
  implementations FUN_00779D60/E20 (Z03/Z04) — they are a LOD/attachment
  state machine (fields +0x60 state, +0x90 partner). Full record in
  05_ORACLE/ORACLE_RECORDS.md Mechanism 2.
- SOURCE_IDENTITY: Gb12 source NiNode.cpp:52 (oracle, external code line) +
  Entropia bytes (pinned).
- STATUS: **PASS** (the false matcher is rejected).
- HISTORICAL_CONTROL_REUSED (labeled, not new): NINODE_SLOT17's NC2 — the
  slot-number matcher would label Entropia slot 17 as
  SetSelectiveUpdateFlags(GB112) or ApplyTransform(GB12); the behavioral
  identification as GetObjectByName-like was that run's. This run re-pinned
  its anchor (slot 17 = 0x007B5390, C12 MATCH) and did NOT re-litigate the
  identification.

## CONTROL-4 — Byte cross-check (method-pair enforcement; NEW_CONTROL_EXECUTED)

- TESTED CLAIM: every instruction cited from Ghidra in E1-E12 exists verbatim
  in the physical EXE.
- EXPECTED DISCRIMINATOR: any byte drift between listing and raw file.
- ACTUAL OBSERVATION: 962/962 instructions identical after signed-byte
  normalization; 113/113 CALL/imm32 targets recomputed from raw rel32 bytes
  match the listing targets (01_RAW/C10V2_BYTE_CROSSCHECK.json). The one
  transcription artifact of this run's first pin attempt (c10 v1, signed-hex
  misreading — my own error) was caught by exactly this cross-check and
  corrected by automation (c10v2), demonstrating the control's discriminating
  power.
- SOURCE_IDENTITY: Entropia.exe (pinned) + C9 listing JSON + c10v2 script.
- STATUS: **PASS**.

## CONTROL-5 — Payload record identity (physical-file side; NEW_CONTROL_EXECUTED)

- TESTED CLAIM: the record bytes attributed to templates.vfs record 4508 (and
  cross-records 11963 / 20002-rec0) are those of the pinned file, not of a
  different corpus or era.
- EXPECTED DISCRIMINATOR: SHA256 pins + independent container walk + EOF-
  exactness + CRC behavior.
- ACTUAL OBSERVATION: templates.vfs SHA256 BE57818C... (pinned at preflight
  AND re-hashed by C1 with a different implementation); 5,438/5,438 records,
  base=36, exact EOF, 0 CRC fail; record 4508 dump byte-exact vs the C1 dump;
  20002.vfs re-pinned (SHA C3899C3E...) with record 0 payload bytes matching
  the 20002_PAYLOAD30_CONSUMER canon (BB 2E 00 00 @payload+0x30).
- SOURCE_IDENTITY: physical corpus files (pinned).
- STATUS: **PASS**.

## Controls NOT established / not executed

- No control attempted to prove or disprove the semantic role of the slot
  objects in FUN_00848EA0 (their class is UNKNOWN) — CONTROL-2's conclusion
  does not extend to them either way.
- No runtime control of any kind (STATIC_ONLY run).
- The historical QC-R4 per_artifact.failed cosmetic issue was NOT repaired
  (contract: out of scope this run).
