# TRACE EDGE BLOCKS — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

FAMILY-T (templates.vfs registry-template family) — SELECTED (see 02_ANALYSIS/SELECTION.md).
All code claims: PCG/EU 9.3.5 client Entropia.exe, SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, 8,015,872 B,
image base 0x00400000, ASLR OFF (re-pinned at preflight).
Method A = Ghidra 11.2.1 decompilation/listing (run-local project copy of
PE935_DISPLAY_ENUM_R1; original project untouched; LOCAL-ONLY outside repo).
Method B = raw byte reads from the physical EXE with this run's own PE mapper +
manual x86 decode (scripts c10v2/c12; no Ghidra involved).
Cross-check: 962/962 listing instructions byte-identical to raw EXE bytes;
113/113 CALL/imm32 targets recomputed from raw bytes match the listing
(01_RAW/C10V2_BYTE_CROSSCHECK.json).

---

## E1 — Physical record → parser → registry insert

```text
CLAIM_ID: E1-READ-PARSE-INSERT / STATUS: CONFIRMED
SOURCE_IDENTITY: templates.vfs — D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs
  560,788 B, SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77,
  magic ArkVFS02, base=36, 5,438 records walked to exact EOF, 0 CRC fail
  (01_RAW/C1_CENSUS.json).
RECORD_IDENTITY: record id2=4508 (header id 4508), file_offset 96,496 (0x17930),
  header {id=4508, size=28, ver=1, crc32=AFF5797C}, payload 28 B:
  9c 11 00 00 | fd 85 04 00 | fe 85 04 00 | 00 00 00 00 | cb e1 f9 42 | 00 00 | 00 00 | 00 00 00 00
  = {id2=4508, A=296445, B=296446, C=0, D_f32=124.94100189208984,
     list1_count=0, list2_count=0, f11=0}
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION:
  - FUN_0072FA30 (reader): builds path from .rdata string
    "Parameters\templates.vfs" @VA 0x00A86D30 (raw search: 1 hit, .rdata,
    file_offset 6,843,696 — 01_RAW/C10V2_BYTE_CROSSCHECK.json)
  - per-record read FUN_00971AD0: SetFilePointer(handle@+0x18) seek
    (01_RAW/C9_LISTING_WINDOWS.json L05; decompiled Z10) then ReadFile into the
    0x80 raw buffer; cursor fields set (+0xC offset=0, +0x11 flag=1)
  - parse FUN_00730C90 (Z01/X01, byte window L06): reads u32 fields in order
    f0, f2, f1, f3, f4 -> template object fields +0x00, +0x08, +0x04, +0x0C, +0x10
    (i.e. f0=id2, f2=A, f1=B, f3=C, f4=D_f32), then list1 parser FUN_00730B70
    (u16 count + count x strings -> vector<basic_string> @+0x14), then list2
    parser FUN_00730970 (u16 count + count x u32 -> vector<u32> @+0x20),
    then f11 -> +0x2C.
  - registry insert FUN_0072F8D0 (X03, window L18): STL Rb_tree insert unique,
    KEY at node+0x10 compared against *key param; new node from FUN_0072F7F0;
    rebalance + count++.
INPUT_VALUE_OR_POINTER_PROVENANCE: file payload bytes of record 4508 (physical
  source above), read by FUN_00971AD0 into the raw record buffer, parsed by
  FUN_00730C90 into the 12-u32 template object {id2, B, A, C, D_f32, list1,
  list2, f11}.
OUTPUT_VALUE_OR_POINTER_PROVENANCE: template object inserted in RB-tree with
  root DAT_00BA1824 (lazy singleton init in FUN_0043A550 — X11: if
  DAT_00BA1824==0 -> new(0x18) -> FUN_0052A260).
SELECTED_PATH_AND_REACHABILITY_PROOF: FUN_0072FA30 iterates ALL records of the
  file (do-loop over the record id list; 5,438/5,438 walked to EOF by the
  independent C1 walk which uses the file's own stride math, not the binary).
OBJECT_IDENTITY / BASE_POINTER / FIELD_OFFSET: template object = registry RB-tree
  node + 0x14; key = node+0x10 = id2; A = template+0x08.
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = Ghidra decompilation of reader/
  per-record/parse/insert; B = C1 own walk of the physical file (independent
  decoder of the container format) + raw EXE byte windows (L04/L05/L06/L18
  cross-checked by c10v2). The C1 walk does not use the client binary at all;
  the binary-side parse order is byte-pinned.
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: if the parse order were different
  (e.g. A at payload+0 as f0), the emitter's getter [template+0x08] would read
  4508's id2 instead of 296445 and the model join would break (296445.nif hit
  vs 4508.nif). Actual: A=296445 lands at template+0x08 (parse writes payload[1]
  to +0x08), and 296445.nif exists in Models.bnt while the alternative would
  have needed to be re-derived. RESULT: PASS.
```

## E2 — Registry lookup: id2 → template object

```text
CLAIM_ID: E2-LOOKUP / STATUS: CONFIRMED
SOURCE_IDENTITY: Entropia.exe (pinned above).
RECORD_IDENTITY: lookup key = id2 (runtime u32; for the anchored trace = 4508 or
  the hardcoded/driver-supplied ids; see E9).
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: FUN_0072F580
  (01_RAW/C9_LISTING_WINDOWS.json L02):
  0x0072F590  E8 9B 1E DA FF     CALL FUN_004D1430 (mapfind)
  0x0072F59E  83 C0 14            ADD EAX, 0x14            (node -> template)
  0x0072F5A2  C2 04 00            RET 4
  0x0072F5A5  B8 00 58 BA 00      MOV EAX, 0x00BA5800      (default on miss)
  mapfind FUN_004D1430: RB-tree walk, key at node+0x10, left node+8, right
  node+0xC; returns last node with key >= searched (window L03).
INPUT_VALUE_OR_POINTER_PROVENANCE: key = id2 in ECX (thiscall, ECX set by every
  caller — pinned for the emitter at 0x006C3F60 `MOV ECX,EAX` before the call).
OUTPUT_VALUE_OR_POINTER_PROVENANCE: EAX = node+0x14 = template object, or
  DAT_00BA5800 sentinel on miss.
SELECTED_PATH_AND_REACHABILITY_PROOF: 25 CALL callsites / 23 unique callers
  (own census C2, T01) — the lookup is the single template-entry mechanism of
  the censused machinery.
OBJECT_IDENTITY / BASE_POINTER / FIELD_OFFSET: template object at node+0x14
  (value); key id2 at node+0x10 (byte-confirmed in mapfind and insert).
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = Ghidra listing/decompilation;
  B = raw EXE bytes (c10v2: 962/962 identical incl. this window) and the
  independently measured C1 registry walk (5,438 unique id2 — matches the
  registry the code builds).
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: if node+0x14 were not the value, the
  emitter's subsequent [ECX+0x08] getter would read node internals (e.g. left
  pointer at +0x08) instead of A — the {0x66, A} pair would then carry a
  pointer fragment, and the Models.bnt name join would fail. Actual: getter
  reads 296445 (A) and 296445.nif exists at the pinned index offset. RESULT: PASS.
```

## E3 — Template → getter A → model request pair {0x66=MODEL, A}

```text
CLAIM_ID: E3-GETTER-A-PAIR / STATUS: CONFIRMED
SOURCE_IDENTITY: Entropia.exe (pinned).
RECORD_IDENTITY: A value for the record under trace = 296445 (from E1 payload
  bytes fd 85 04 00 @file 96,516).
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: FUN_006C3F50 (emitter;
  window L01, c10v2 byte-verified):
  0x006C3F5B  E8 ...               CALL FUN_0043A550 (registry lazy-init)
  0x006C3F60  8B C8                MOV ECX, EAX            (ECX = id2)
  0x006C3F62  E8 19 B6 06 00       CALL FUN_0072F580       (lookup; raw rel32
                                    target 0x0072F580 recomputed by c10v2)
  0x006C3F67  8B F8                MOV EDI, EAX            (EDI = template)
  0x006C3F69  BB 66 00 00 00       MOV EBX, 0x66           (MODEL type)
  0x006C3F6E  8B CF                MOV ECX, EDI            (ECX = template)
  0x006C3F74  E8 67 5E 10 00       CALL FUN_007CE1E0       (getter A)
  0x006C3F8D  89 19                MOV [ECX], EBX          (store 0x66)
  0x006C3F8F  89 41 04             MOV [ECX+4], EAX        (store A)
  then FUN_006C3640(queue, ..., callback 0x008BD720, A) — scheduler entry.
INPUT_VALUE_OR_POINTER_PROVENANCE: id2 param -> lookup -> template (E2); A =
  [template+0x08] via FUN_007CE1E0 (same getter byte-pinned by
  PE_935_20002_PAYLOAD30_CONSUMER for the ArkObject ctor; re-pinned here for
  the emitter path).
OUTPUT_VALUE_OR_POINTER_PROVENANCE: 8-byte pair {type=0x66, id=A=296445} stored
  in the caller-provided queue vector (+0x4/+0x8 header), then handed to the
  request scheduler with callback FUN_008BD720.
SELECTED_PATH_AND_REACHABILITY_PROOF: the pair store and the scheduler call are
  straight-line in the function (no branch between lookup and store except the
  queue-grow path which writes the same pair).
OBJECT_IDENTITY / BASE_POINTER / FIELD_OFFSET: A = template+0x08; the queue is
  caller-owned (param_2).
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = Ghidra decompilation (R04) +
  listing; B = raw byte windows cross-checked 962/962; the A value itself
  (296445) is measured from the physical templates.vfs record (C1), not from
  the binary — so the payload->object->request chain is not self-confirmed.
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: if ECX at the getter call were NOT
  the lookup result (e.g. the id2), A would be 4508/16082/etc. and the nif
  join would miss. Actual: [template+0x08]=296445 for record 4508 and
  296445.nif exists (E5). RESULT: PASS.
```

## E4 — Model resource join A → <A>.nif (data side, re-pinned)

```text
CLAIM_ID: E4-MODEL-JOIN / STATUS: CONFIRMED (data join; runtime physical open
  remains STRONGLY_SUPPORTED per prior canon — provider virtual bodies not
  re-decoded this run)
SOURCE_IDENTITY: Models.bnt — D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt
  395,412,868 B, SHA256 C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0
  (index metadata only; NO payload extraction).
RECORD_IDENTITY: index name "296445.nif" @name_file_offset 395,268,773
  (historical anchor E.7 re-measured this run: C1) — 5,596 entries, index_start
  395,262,727; "551661.nif" @395,323,507 (for the FAMILY-P cross-check record
  id2=11963); "296446.nif" ABSENT (B goes to Volumes.bnt as .bvi — consistent
  with the 1,666/1,666 B-join of JOIN R1); "460563.nif" ABSENT (historical
  negative).
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: data-level join (no new
  instruction window; the request side is E3; the pump FUN_006C9700 has 13
  CALL sites / 11 callers — own census T05).
INPUT/OUTPUT PROVENANCE: A=296445 from E3 -> index name "296445.nif".
SELECTED_PATH_AND_REACHABILITY_PROOF: full-corpus join CONFIRMED by JOIN R1
  (3,618/3,618 unique nonzero A, 0 misses, own decoders) — this run re-pins the
  anchor (296445.nif @395,268,773) with its own parser (C1) and does NOT
  re-run the full join (bounded reuse, recorded).
OBJECT_IDENTITY: nif resource name in BNT2 index.
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = JOIN R1 full join (prior, with own
  decoders); B = this run's own index parse of the anchor (independent
  implementation of the trailer-index format).
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: absent or duplicate name would break
  the join. Actual: anchor offset matches prior canon exactly. RESULT: PASS.
```

## E5 — Model instance creation path (request → instance → named registration)

```text
CLAIM_ID: E5-INSTANCE-PATH / STATUS: STRONGLY_SUPPORTED (structure CONFIRMED at
  byte level; identity of the named 0x110 object CORRECTED to
  NiControllerSequence — see RETRACTIONS)
SOURCE_IDENTITY: Entropia.exe (pinned).
RECORD_IDENTITY: A=296445 request -> FUN_006CB6F0 (cache-lookup by id in
  [store map]; miss -> FUN_006C9700 pump (request) -> operator new(0xC) ->
  FUN_006FA8B0 ctor (vft 0x00A864B8, refcount@+4, item@+8 — prior canon,
  inherited, NOT re-decompiled this run) -> FUN_006CB020 named-instance builder
  -> FUN_006F33A0 registration).
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION:
  - FUN_006CB6F0 (R11; window L20): cache lookup FUN_00971780, pump call, new,
  ctor, named-instance call, registration call — all in straight-line decompile.
  - FUN_006CB020 (R12): builds stringstream "<id>__<name>", operator new(0x110),
    FUN_007796D0(name,...) — decompiled O03 this run: the 0x110 object's ctor
    writes NiControllerSequence::vftable (RTTI symbol in the binary). The
    "ArkAnimation" class-check string gates this path (R12).
  - pending-attach processor FUN_006CB3C0 (R13): descriptor {type@+0x5C,
    A@+0x64}; type 1/2/3 branches; attach ops FUN_0077C0B0/F0/120 (see E7).
INPUT/OUTPUT PROVENANCE: A (from E3/E4 chain) as request id; named instance
  keyed by "<A>__<name>".
SELECTED_PATH_AND_REACHABILITY_PROOF: pump FUN_006C9700 called by the instance
  creator itself (census T05: FUN_006CB6F0 site 0x006CB7CF); FUN_006CB3C0
  called from FUN_006CB4C0 (vector walk over descriptors, gate *(item+0x5C)!=0)
  and FUN_006CD850 (LOD update — census T09/T06 callers).
OBJECT_IDENTITY / BASE_POINTER / FIELD_OFFSET: descriptor type@+0x5C, id@+0x64;
  named instance = NiControllerSequence (0x110 B).
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = Ghidra decompilations R11/R12/R13
  (this run); B = census caller counts (own C2/C4) + byte windows L20
  (c10v2-verified). The identity correction (NiControllerSequence) comes from
  the binary's own RTTI symbol in the decompilation, not from an external guess.
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: if FUN_006CB020 built a
  world-object instance rather than an animation-sequence holder, its ctor
  would not write NiControllerSequence::vftable. Actual: it does (O03).
  RESULT: PASS (as corrected).
```

## E6 — Placement-record transform setters (runtime placement record)

```text
CLAIM_ID: E6-PLACEMENT-SETTERS / STATUS: CONFIRMED (as RUNTIME transform
  transport; NOT a physical-record -> instance edge — see E9/E10)
SOURCE_IDENTITY: Entropia.exe (pinned).
RECORD_IDENTITY: runtime placement record {key@+0, X2@+4, position vec3
  @+0x08..0x10, rotation vec3 @+0x14..0x1C, param pair @+0x20/+0x24, variant
  u16@+0x34} — inherited layout (JOIN R1/INSTANCE_TRACE) re-pinned this run at
  instruction level.
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: (window L09/L10, c10v2-verified)
  FUN_00730F90 (position setter): MOV [ECX+0x08],EDX / [ECX+0xC],EDX /
    [ECX+0x10],EAX  (bytes 89 51 08 / 89 51 0C / 89 41 10) — RET 4
  FUN_00730FB0 (rotation setter): stores to [ECX+0x14/0x18/0x1C]
  FUN_00730FD0 (pair setter): stores to [ECX+0x20/0x24]
  FUN_00730F60 (init): zero 11 u32 (44 B record prefix)
INPUT_VALUE_OR_POINTER_PROVENANCE: setters receive vec3 pointers from their
  callers; for the construction path FUN_00567170 the position comes from
  FUN_00566100 (Y01: position read from a runtime movable object at
  +0x44..+0x4C, or +0x68 for the self case, with scale/offset arithmetic);
  for FUN_00567770 the position comes from the attribute tree
  (FUN_00846840 — W06) — i.e. RUNTIME sources, not file payloads.
OUTPUT_VALUE_OR_POINTER_PROVENANCE: placement record fields; the record is then
  registered by name (FUN_00457930) — W06 decompile — and handed to the visual
  path (FUN_006D0990 etc.).
SELECTED_PATH_AND_REACHABILITY_PROOF: setters byte-pinned; init+set+register
  sequence appears in both construction drivers (R05/R06 decompiles).
OBJECT_IDENTITY / BASE_POINTER / FIELD_OFFSET: thiscall ECX = placement record;
  fields as listed.
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = Ghidra decompiles of the drivers;
  B = raw byte pins (89 51 08 etc. — c10v2 962/962). The position PROVENANCE
  is stated as runtime (Y01/W06), which is what BREAKS the physical-record
  chain — documented rather than assumed.
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: if the setters wrote into a
  NiAVObject m_kLocal (translate @+0x5C per NINODE_SLOT17 canon), we would see
  +0x5C stores. Actual: stores at +0x08/+0x14/+0x20 — a DIFFERENT structure
  (the placement record), so the placement record is NOT a NiAVObject.
  RESULT: PASS (record -> NiAVObject transform edge NOT established — open).
```

## E7 — Attach edge: pending-attach thunks are NOT NiNode::AttachChild

```text
CLAIM_ID: E7-ATTACH-CLASSIFICATION / STATUS: REJECTED-AS-ATTACHCHILD /
  CONFIRMED-AS-LOD-STATE-MACHINE
SOURCE_IDENTITY: Entropia.exe (pinned) + Gb12 oracle source (see 05_ORACLE).
RECORD_IDENTITY: attach operations invoked from the pending-attach processor
  FUN_006CB3C0: FUN_0077C0B0 (type 1/2 path), FUN_0077C0F0 (type 2), and the
  LOD-update path FUN_0077C090/C0/100 (R15).
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: (window L13, c10v2-verified)
  0x0077C0B0  8B 4C 24 04         MOV ECX,[ESP+4]
  0x0077C0B4  6A 01               PUSH 1
  0x0077C0B6  E8 A5 DC FF FF       CALL FUN_00779D60
  0x0077C0BB  ...                 MOV AL,1; RET 4
  0x0077C0F4  E8 27 DD FF FF       CALL FUN_00779E20 (thunk f)
  0x0077C0E0  E8 AB EC FF FF       CALL FUN_0077AD90 (thunk c0 -> another impl)
  Implementations (Z03-Z07): FUN_00779D60/E20/F80/C80/E70 operate on a state
  field @+0x60 (values 0..4), partner pointer @+0x90, transition floats
  @+0x64/+0x68/+0x6C, an index/flag pair @+0x98/+0x9C, and an array @+0x30 with
  count @+0x38 — a LOD/attachment STATE MACHINE over the visual manager object,
  NOT a scene-graph child-array insertion.
INPUT/OUTPUT PROVENANCE: object = the model's runtime visual wrapper (reached
  in R13 as *(*(resource lookup)+8)+8 style chains), not a NiNode.
SELECTED_PATH_AND_REACHABILITY_PROOF: decompiles Z03-Z07 (this run) compared
  against Gb12 NiNode::AttachChild source (NiNode.cpp:52): AttachChild does
  NULL-guard + IncRefCount + AttachParent + children-array add + DecRefCount.
  NONE of these operations appear in Z03-Z07 (no refcount pair, no children
  array add, no parent set on a child object).
OBJECT_IDENTITY: FUN_00779D60-family operate on the Ark visual-manager object
  (0x130-class area), NOT on NiNode (whose vtable 0x00A8CCF4 — C12 — has
  slot 17 = 0x007B5390, the GetObjectByName-like function, none of which are
  these).
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = Ghidra decompiles; B = raw byte
  pins (L13/L14/L15 — 962/962); oracle = independent Gb12 source (external
  code line, not derived from the binary).
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: name-based matching ("attach") would
  mislabel these as AttachChild. The behavioral comparison falsifies that.
  RESULT: PASS (negative control — see CONTROL-3).
```

## E8 — Scene graph root and NiNode naming (oracle mechanism 1 site)

```text
CLAIM_ID: E8-SCENE-ROOT / STATUS: CONFIRMED (operations); scene insertion of
  model instances NOT traced further this run
SOURCE_IDENTITY: Entropia.exe (pinned).
RECORD_IDENTITY: scene root NiNode: new(0x118) -> ctor FUN_007B6000 (O01:
  writes NiNode::vftable @MOV [ESI],0x00A8CCF4 — C12 raw pin; children array
  init via FUN_00788480 with LEA ECX,[ESI+0xC8]; effects list vft @+0xE0)
  -> FUN_007B67E0("NetImmerseScene::Root") (O02 = NiObjectNET::SetName-shaped:
  delete [this+0xC]; strlen; new(len+1); strcpy -> [this+0xC]; else 0).
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: ctor vtable store
  C7 06 F4 CC A8 00 @0x007B6041 (raw bytes C12); name store per O02.
INPUT/OUTPUT PROVENANCE: literal "NetImmerseScene::Root" (string in binary);
  R17 decompile + raw string pin (C1/c12-era raw searches).
SELECTED_PATH_AND_REACHABILITY_PROOF: R17 (FUN_00933310) — new(0x118), ctor,
  SetName("NetImmerseScene::Root"), NiZBufferProperty new(0x28) + attach.
OBJECT_IDENTITY: NiNode (RTTI symbol NiNode::vftable in binary; 47-slot vtable
  @0x00A8CCF4; name member @+0xC per SetName store and NINODE_SLOT17 canon).
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = Ghidra decompile O01/O02/R17;
  B = raw vtable imm32 pin (C12) + Gb12 oracle source comparison
  (NiNode.cpp:34, NiObjectNET.cpp:112).
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: SetName writing at +0xC matches both
  the Gb12 oracle source (m_pcName) and the historical NINODE_SLOT17 layout
  (name @+0x0C). RESULT: PASS.
```

## E9 — Who drives construction: id2/position sources (the BROKEN EDGE)

```text
CLAIM_ID: E9-CONSTRUCTION-SOURCES / STATUS: PARTIALLY CONFIRMED / OPEN as the
  level-A blocker
SOURCE_IDENTITY: Entropia.exe (pinned).
RECORD_IDENTITY (the inputs to the placement-construction path):
  (a) HARDCODED id2 immediates in code:
      - FUN_005B6597: 68 D3 3E 00 00  PUSH 0x3ED3 (16083) -> CALL FUN_005B5F90
        (window L16; also 0x3ED2=16082 variants) — movable-relative construction.
      - FUN_00567170 selects id2 from {0x3BD9=15321, 0x3BDA=15322, 0x3BDB=15323,
        0x3A47=14919} by attribute flags (R05 decompile).
      - emitter-array callers FUN_006C3FE0/FUN_006C4020 iterate id2 arrays
        (Z08/Z09) from FUN_006C4060.
  (b) MESSAGE-CHANNEL drivers: FUN_004B18D0 (Q02) dispatches message types
      {0xA2..0xC7 incl. 0xB0 -> FUN_004574F0 -> deserB FUN_004C47F0;
      0xB9 -> FUN_005B72C0; 0xC6 -> FUN_004B0AB0; 199/0xC7 -> FUN_004B1670} —
      the placement record deserialization (FUN_007453D0/Z11: key u32, X2,
      variant u16@+0x34, three u32, u8) and the construction drivers are
      REACHED FROM MESSAGE DISPATCH.
  (c) ATTRIBUTE path: FUN_00848EA0 (R08) reads per-slot {u16@+0xC, float@+0x10}
      under flag 2, and for flag-1 slots: id2 from property machinery (Q05: class 20006
      instance, property tag 6 via FUN_007376A0 / FUN_0070C180(6)) -> lookup ->
      FUN_0072FE30 (template list2 -> 3 x vec3) -> FUN_006C1F90 lerp
      (default, template_vec, attr_float) -> slot position @+0x00 (slot stride
      0x18 — Q04).
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: PUSH 0x3ED3 @0x005B6597
  (byte-pinned, L16/c10v2); dispatcher switch decompiled (Q02); lerp call site
  0x00848FA6 (window L12).
INPUT/OUTPUT PROVENANCE: id2 values from code immediates / message payload /
  runtime attribute — NONE of these three channels is a file record of
  templates.vfs; templates.vfs only supplies the DEFINITION looked up by id2.
SELECTED_PATH_AND_REACHABILITY_PROOF: census chains: FUN_004B18D0 <- {FUN_004B1B70,
  FUN_004B2950} (P04); FUN_005B72C0 <- FUN_004B18D0 case 0xB9; FUN_00567C50 <- {
  FUN_00514EF0 (0 callers — virtual), FUN_0058DB50 <- FUN_00468910 (P03, 9
  callers), FUN_005B72C0}; FUN_006A34A0 (dynamic factory, 2x spawn) <-
  {FUN_0067B4F0, FUN_0067C560} (preview-UI area).
OBJECT_IDENTITY / BASE_POINTER / FIELD_OFFSET: as per E6 record + message
  cursor objects.
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = decompiles R05/R06/R08/X06/X08/Q02/
  W06/Z08/Z09; B = raw byte pins (L16, L12; 962/962) + own census counts.
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: if a caller fed a templates.vfs
  record's own id2+position from the FILE into these constructors, we would
  see a VFS record read in these chains. None of the censused construction
  callers reads templates.vfs (the only file reader is FUN_0072FA30, census
  T02: exactly 1 caller = the registry loader). RESULT: the physical-record ->
  world-instance identity edge is NOT ESTABLISHED in the censused machinery —
  the broken edge for LEVEL A.
```

## E10 — Template payload list2 (positions) — the payload-derived transform data

```text
CLAIM_ID: E10-PAYLOAD-VEC3 / STATUS: CONFIRMED as payload data + CONFIRMED use
  in one runtime slot-position computation (identity-preserving from the FILE
  to a computed position, but the SLOT object is not established as a world
  instance)
SOURCE_IDENTITY: templates.vfs (pinned) + Entropia.exe (pinned).
RECORD_IDENTITY: template object list2 = vector<u32> at template+0x20, parsed
  from the physical payload by FUN_00730970 (u16 count + count x u32). When
  (end-begin)&~3 == 0x24 (36 B = 9 u32), FUN_0072FE30 (W04) copies out three
  vec3s (offsets 0x0/0xC/0x18 of the vector data) and returns 1.
  Record 4508: list2 EMPTY (28-B payload; both u16 counts = 0).
  Record id2=11963 (payload 382 B): list1_count=16 strings (first string
  "leg_BASE" — C1 raw bytes) — the 20002/P-family cross-record.
VA / FILE_OFFSET / INSTRUCTION_BYTES / FUNCTION: FUN_0072FE30 (decompiled W04,
  byte window in C9 set), lerp FUN_006C1F90 (W03: out[i] = a[i] + t*(b[i]-a[i])),
  consumer chain FUN_00848EA0 (R08) -> slot position store (Q04 slot stride
  0x18).
INPUT/OUTPUT PROVENANCE: template list2 values from the physical file payload;
  lerp parameter = runtime attribute float (FUN_00745690 — Q06); default = code
  constant _DAT_00a7b25c; output = slot vec3 @+0x00 of the 0x18-stride slot
  object.
SELECTED_PATH_AND_REACHABILITY_PROOF: R08 loop over 3 slots (uVar10 0..2);
  flag-1 branch executes lookup -> FUN_0072FE30 -> lerp -> store.
OBJECT_IDENTITY: slot object = FUN_007333E0(index) of the caller object;
  semantic class of that object NOT established this run.
METHOD_A / METHOD_B / WHY_NON_CIRCULAR: A = decompiles; B = C1 own file parse
  (payload bytes incl. record 11963 list1 string) + raw byte windows.
FALSIFIER / ACTUAL_COUNTERCHECK / RESULT: if list2 were parsed differently,
  the 0x24 size gate would fail. Actual: gate structure confirmed; the file
  side (u16 count + u32 elements) confirmed by the C1 walk + payload dumps.
  RESULT: PASS (bounded: payload vec3 -> runtime position computation
  established; world-instance semantics of the slot object NOT established).
```

## E12 — Historical anchors re-pinned

```text
CLAIM_ID: E12-HISTORICAL-ANCHORS / STATUS: see per-anchor
(a) NINODE_SLOT17 slot 17 anchor: NiNode vtable @0x00A8CCF4 (raw pin from ctor
    MOV [ESI],imm32), slot 17 (+0x44) = 0x007B5390 — MATCHES the historical
    anchor (C12). CONFIRMED re-pin.
(b) 20002.vfs record 0 anchor: payload+0x30 = BB 2E 00 00 = 11963 — re-pinned
    from own bytes (C1), matches 20002_PAYLOAD30_CONSUMER canon. CONFIRMED.
(c) Models.bnt anchor 296445.nif @395,268,773 — re-pinned (C1/E4). CONFIRMED.
(d) NiNode UpdateWorldData (historical slot 27): slot 27 = 0x007E4820; the
    function is UpdateWorldData-shaped (LEA ECX,[EBX+0x38] = m_kLocal,
    LEA ECX,[EAX+0x6C] = parent m_kWorld, transform-multiply call FUN_006EB380,
    rep movsd present but only 1 consecutive in the first 512 B — the
    historical "rep movsd x13" description was NOT reproduced within this
    probe window; documented as a discrepancy, NOT as a retraction of the
    historical run's own evidence). STRONGLY_SUPPORTED (distinctive,
    non-exact).
```

---

## Separately-reported axes (contract §6)

- FUNCTION_IDENTITY: reader FUN_0072FA30 CONFIRMED (string+parse+insert chain);
  lookup FUN_0072F580 CONFIRMED; getter FUN_007CE1E0 CONFIRMED as [ECX+0x08]
  load; emitter FUN_006C3F50 CONFIRMED; FUN_007B67E0 = NiObjectNET::SetName
  STRONGLY_SUPPORTED (behavioral identity + RTTI-consistent layout; no symbol
  in binary names it directly); FUN_007B6000 = NiNode ctor STRONGLY_SUPPORTED;
  0x007B5390 = GetObjectByName-like (historical B, re-pinned, not re-litigated);
  FUN_00779D60-family = LOD/attachment state machine (NOT AttachChild).
- OBSERVED_OPERATION: file record -> parse -> registry -> keyed lookup ->
  {0x66=MODEL, A} request pair; placement records get runtime position/rotation
  via setters from message/attribute/hardcoded drivers.
- FINAL_SEMANTIC_ROLE (bounded): templates.vfs = the static template registry
  {id2 -> A (model nif id), B (collision bvi id), C, D_f32, name lists, u32
  list} consumed by the model machinery and by placement construction as a
  DEFINITION source; its records are not shown to carry instance identity or
  instance transforms for world placement.
- MODEL_RESOURCE_EDGE: CONFIRMED for record 4508 (A=296445 -> 296445.nif).
- INSTANCE_IDENTITY: named model-side instance = NiControllerSequence
  "<A>__<name>" (corrected); world-instance identity from a file record
  NOT ESTABLISHED.
- TRANSFORM_EDGE: placement-record setters CONFIRMED as runtime transport
  (record is not a NiAVObject — +0x08/+0x14 vs m_kLocal@+0x38/+0x5C); template
  payload list2 -> slot position lerp CONFIRMED (payload-derived transform
  data); physical-record -> world-instance transform NOT ESTABLISHED.
- SCENE_GRAPH_EDGE: scene root NiNode + SetName CONFIRMED; model -> scene
  insertion NOT traced past the LOD/attach state machine (E7).
- PERSISTENT_PLACEMENT_EDGE: NOT ESTABLISHED (drivers are message/attr/hardcode).
- MODEL_ID_RECOVERED: YES — A=296445 (296445.nif) for record 4508 (and
  A=551661 for the cross-record id2=11963).
- PLACEMENT_XYZ_RECOVERED: NO — no placement XYZ recovered for any world
  instance from a physical record this run; the only payload-derived vec3
  (list2) feeds a slot-position computation whose object class is unknown.
