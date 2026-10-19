# PE_935_BUILDING_PLACEMENT_5H_PUBLIC_SUMMARY_Q_R1_20261018 — Corrected Public Summary of the CAND4 "Q" Run

- SUMMARY_ID: PE_935_BUILDING_PLACEMENT_5H_PUBLIC_SUMMARY_Q_R1_20261018
- AUTHORED_BY: pe-master-auditor publication worker, under PE-MASTER dispatch (human authorization of 2026-10-18, contract §14)
- WHAT THIS IS: a sanitized public summary of the local frozen run
  PE_935_CAND4_Q_CTOR_ARGUMENT_SAVED_R1_20261018 ("the Q run") AS CORRECTED by
  the deep postaudit PE_935_CAND4_Q_DEEP_POSTAUDIT_R1_20261018 (published in this
  repository at `docs/audits/PE_935_CAND4_Q_DEEP_POSTAUDIT_R1_20261018/`).
- WHAT THIS IS NOT: the Q package itself. The frozen Q package (including its
  01_RAW listing extracts and 01_TOOLS) stays LOCAL-ONLY and is NOT published.
  No raw listing rows, no game payload bytes, no VFS/BNT/NIF literals are
  reproduced here; short address/mnemonic/offset quotes are analytic citations
  only (contract §14 rule).
- METHOD: this summary restates only what the sealed Q report, its provenance
  files and the published postaudit support, with the postaudit's material
  corrections applied. It does not re-derive the science and adds no new
  evidence.

## 1. Provenance of the local frozen sources (cited by identity, not content)

- Sealed Q run root (local-only): `99_Audits\PE_935_CAND4_Q_CTOR_ARGUMENT_SAVED_R1_20261018`
  (inside `D:\Eudoria_Reconstruction`, not part of this repository).
- Q run REPORT.md: 11,405 B, SHA256 2FE8D9DBA72083E2BE9A1A7E16A6EADA53A81129C75B8F6BA09B6B86CC0B2810.
- Q run Q_ARGUMENT_PROVENANCE.json: 8,708 B, SHA256 21E066368FEFE8FD8EFB9D7099296CA36617850698B2E234BC027AD150E0FC7E.
- Q run S_PRODUCER_BINDING.json: 2,803 B, SHA256 73CA2F92CB3FC947275B576E069456248EE3D286F1787ED9B8DDD597205E7620.
- Q run MANIFEST_SHA256.csv (self-excluded, LAST): 3,212 B, SHA256 B7D19291E1C680AAB7407674FAC10444AAD4E1E9CEEE2CA816F29F906A863DD0.
  (All four identities re-hashed from disk on the publication date by this worker.)
- Published postaudit (this commit): `docs/audits/PE_935_CAND4_Q_DEEP_POSTAUDIT_R1_20261018/`
  — REPORT.md, artifact_index.csv, MANIFEST_SHA256.csv.
- Related sealed campaign (this commit, sanitized projection):
  `docs/audits/PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018/`.

## 2. The mechanism the Q run established (postaudit-consistent wording)

Scope: static, saved-evidence only (a pinned 50,780,146-byte saved Ghidra listing,
SHA256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB, plus pinned
saved dumps; EXE never opened, client never run, 0 runtime actions).

1. **ArkNiStreamer helper identity.** 0x0082E580 (3 instructions, this run) installs
   vptr 0x00A91994; saved RTTI links that address to `.?AVArkNiStreamer@@` (VTABLE_INVENTORY
   L1038, prior evidence, cited with pins). The helper object is an Ark-side wrapper of
   Gamebryo streams; the magic tag cells 0xA91998 (first 4 bytes "Game" — read from a saved
   non-code dump; consistent with the "Gamebryo File Format" header family of the PE 9.3.5
   era; remaining bytes unreadable without the EXE) and 0xA919A4 lie immediately past that
   one-slot vtable. Postaudit boundary: the tag-vtable neighborhood is CONTEXT for the
   class-constant reading, not proof of it. 0x0082E750 and 0x0082E5C0 are methods of this
   class. (Postaudit verdict: the mechanism narrative is retained.)
2. **The acquire path 0x0082E750 and the Q argument.** 006B1FD0 constructs the local
   helper via 0082E580, calls 0082E750 with an out-slot, checks the first value, and on
   the success path allocates 0x14 bytes, passing a later read of that slot to 006C9540.
   In 0082E750 the visible flow: prefix guards (tag4 @0xA919A4 or tag8 @0xA91998), a
   local NiStream object (vptr 0x00A8EC24; ctor 007D3540 zeroes, among others, +0x148),
   and CALL 007D0E60 over (data,len); 007D0E60 is a wrapper that builds a stream over the
   (data,len) buffer (via 007EEB80) and calls the VIRTUAL slot 1 of NiStream — the actual
   NIF parser. On success (AL): **V = M32[M32[obj1+0x148]]** — the root pointer read from
   the loaded-stream holder field. Post-load processing (recursive child walker 0082E5C0
   over children base +0xCC / count +0xD4; 007BF500 virtual dispatch; retain *out=V,
   [V+4]+=1) precedes the final store *out=V.
3. **Classification of V.** V = the root of a NIF loaded from a string-buffered
   serialized blob — STRONGLY_SUPPORTED by the saved static context. Postaudit
   corrections that bind here (mandatory):
   - NiStream is a LOCAL stack object of the producer; its storage must not be confused
     with the root, and it was not itself claimed to be malloc-allocated.
   - The description "the object extracted from the loaded NIF stream, a candidate root
     of a resource" is strongly supported by static context; **"the unique root of the
     concrete building model 296445" is NOT_ESTABLISHED** — the role of field +0x148 and
     the number of roots require separate proof, and the buffer content is identified
     only by context, not fully.
4. **Factory table binding — CONFIRMED_IN_SAVED_TABLE.** The saved GA3 census binds
   vtable 0x00A85454 (`.?AVArkModelResourceItemFactory@@`) slot 1 to 006B1FD0; it is the
   ONLY inventoried vtable containing 006b1fd0. The call shape matches E2/W2 exactly:
   `[elem+8]->slot1(A, &string)` — arg1 (A) is unused in the 006B1FD0 body, arg2 is the
   address of the {data,len} string. The returned S receives SetKeys (00826840):
   [S+4]=0x66, [S+8]=A, then node registration and AddRef. S layout (0x14B):
   vptr@0 (0x00A91670 -> 0x00A85A2C), type@4 (0x66), id@8 (A), refcount@0xC,
   root@0x10 (V). Every ArkModelResourceItem in the saved listing was created via
   CALL 006B2073 — the only direct call of the constructor; the ctor appears in no
   inventoried vtable. Postaudit corrections that bind here (mandatory):
   - **No-direct-caller does NOT prove exclusively-virtual use**: one exact direct CALL
     of the ctor and zero direct CALLs of the factory do not prove all constructions go
     through that path; indirect calls, other sources or other entry styles remain
     possible. A one-listing census must not be generalized to the whole runtime.
   - Without the concrete factory registration in [elem+8] at runtime, the binding is a
     strong candidate, not actualS; W1 remains a separate (possibly cache) path.
5. **Base-ctor preservation.** 00826730 (7 instructions) writes only [this..this+0xC]
   (base vptr 0x00A91670 + zero fields), no stack writes, no calls. Postaudit
   refinement: "no ESP stores" alone would not prove stack-slot safety — a this=slot-4
   alias would zero it via [this+4]; the correct premise is a FRESH heap allocation
   disjoint from the active stack (conditional on allocator/memory state), which the
   postaudit requires to be named as such. The Q0 store [S+0x10]=V @006C9554 therefore
   has write-level origin from the argument passed by the caller.
6. **Preservation bounds (honest scope).** The mechanical census of MOV [reg+0x10]
   stores in the class cluster [006C9400,006C9A00) found real writes only at the ctor
   (@006C9554) and the dtor zeroing (@006C96BA); other hits were false positives. S
   vtable slots 008E0110 and 00434321 were NOT opened — potential writers are not
   excluded; a global +0x10 census is meaningless and was not performed. Postaudit
   additions: the walker 007BF500 contains virtual calls, so its full write-set cannot
   be assigned from its explicit MOVs alone; explicit-store coverage in 0082E750 was
   accepted, but opaque calls (007D27B0, 0095D3CA) follow some stores, so final-value
   guarantees beyond the explicit store census are conditional; the success path
   dereferences the holder and calls methods on V before the final TEST — "fail-closed"
   is not "null/fault-safe".
7. **V_first / V_reload / Q0 / Q1 / VT distinctions (postaudit, mandatory).** The first
   read of V @006B201A and the constructor-argument reload @006B206C read the SAME cell,
   but 006B1C80 and the allocator sit between them; equality of the ctor-time value to
   the first-read value requires preservation, not identity-by-address. The correct
   chain is: nonzero at ctor = nonzero-at-first-read PLUS preservation through the
   intervening code (bounded as in point 6). No claim may equate V_first, V_reload, Q0
   (the stored [S+0x10]), Q1 (any later read of the field) or VT (dispatch-time value)
   without a preservation proof. 006B1C80 is partially open and already contains
   [EDI]=EAX where EDI comes from a local container — a frame-local-only reading of
   that store is NOT a guarantee without EDI provenance.
8. **NiStream+4 static cell 0x00A8EC28 (the FIRST_MISSING_EDGE, correctly framed).**
   NiStream vtable slot 1 is the value stored at [0x00A8EC28] (vtable base +4). The
   barrier is the ABSENCE of that saved DWORD in the checked sources — a static-table
   address, which does not by definition require runtime capture. Other saved exports
   may contain the cell; availability must be checked in the allowed catalog, then a
   pivot performed. Postaudit bound: even reading the target would not close actualS/Q
   or determine the class of the object produced from the stream content. The
   alternative edge, runtime [Q] @0x007B79FD, is likewise outside the saved sources.
   A runtime [Q] for one execution would not prove the global historical-buildings
   mechanism.
9. **NiTArray addressing levels (postaudit correction of the Q report wording).** There
   is NO C8-versus-CC conflict: the NiTArray object starts at +C8, its data pointer is
   +CC, its count is +D4. The Q report sentence "NiTArray starts at +CC" is wrong; the
   walker's reads (base +0xCC, count +0xD4) are the field addresses, not the object
   start.
10. **Slot3 target set (unchanged).** The dispatch-time target of V's vtable slot 3
    remains a CONDITIONAL_SET from the saved GA3 evidence ({bare NiObjectNET/NiAVObject
    identity 0x00864230; NiNode clone-root 0x007B6240; NiTriShape 0x007C73C0; NiCamera
    0x007BE170; open set of other Ni classes}) plus an UNPROVEN structural hint toward
    the NiNode family (children-array layout in the walker). Q_VPTR_AT_DISPATCH remains
    RUNTIME_CONDITIONAL_SET; VT11 @007B7A11 is a separate read (prior canon, unchanged).

## 3. Statuses (Q report §5 as corrected; postaudit verdict applied)

- Q_ARGUMENT_ORIGIN = RESOLVED_SAVED_EVIDENCE (V = out-slot of ArkNiStreamer::acquire =
  root of a NIF loaded from a serialized blob; base-ctor write-level preservation proven
  as bounded above).
- S_INSTANCE_BINDING = STRONGLY_SUPPORTED_CONDITIONAL (unique saved-table vtable binding
  + exact call-shape; runtime receiver premise retained).
- Q_FIELD_PRESERVATION = CONDITIONAL_BOUNDED_NO_OTHER_WRITER_FOUND (cluster closed for
  the MOV [reg+0x10] pattern only; slots 008E0110/00434321 unopened; virtual-call
  write-sets not assignable from explicit MOVs).
- Q_VPTR_AT_DISPATCH = RUNTIME_CONDITIONAL_SET (+ NiNode-family structural hint, not
  proof). SLOT3_TARGET = CONDITIONAL_SET as in point 10.
- MODEL_ROOT_RELATION = CANDIDATE (V = resource-model root candidate; world-instance
  identity NOT established; unique-root-296445 NOT_ESTABLISHED).
- Postaudit verdict on the Q run: **PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS**
  (integrity and numeric limits PASS; the main model-loader path is a valuable new
  result; the final RESOLVED/PROVEN wordings were too broad in the points corrected
  above; canonical gate effect NONE).
- Time metadata defect of the source run (postaudit, disclosed): RUN_START.utc
  20:23:26Z vs RUN_START mtime 20:23:38Z, manifest mtime 20:43:46Z — roughly 20 minutes
  of wall time between the declared start and the seal, not the 65-70 minutes of active
  work claimed; update_science.py wrote a literal found_utc 21:18:00Z after an earlier
  closure; other artifact stamps (20:52, 21:10) postdate the seal. These timestamps are
  metadata and cannot be accepted as a reliable chronology or as a measure of reasoning
  time. The scientific identities were re-hashed and verified unchanged after audit.
- Standing labels (unchanged): WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT =
  NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM = UNKNOWN; CANONICAL_GATE_EFFECT = NONE.
- QC_ORIGIN of the Q run = SELF_CHECK; the independent deep postaudit of the new science
  is PE_935_CAND4_Q_DEEP_POSTAUDIT_R1_20261018 (published here); the final independent
  Desktop post-audit of the whole 5h campaign remains PENDING.

## 4. Where to read more (all in this repository)

- Campaign sanitized projection: `docs/audits/PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018/`
  (REPORT.md — fronts A-D synthesis; per-package analytic documents; per-package QC
  packs; publication controls in `00_PUBLICATION/`).
- Deep postaudit: `docs/audits/PE_935_CAND4_Q_DEEP_POSTAUDIT_R1_20261018/`.
- Entry point: `AUDIT_ENTRYPOINT.md` (repository root).

This summary carries no canonical gate effect and no milestone claim; publication is
not scientific acceptance.
