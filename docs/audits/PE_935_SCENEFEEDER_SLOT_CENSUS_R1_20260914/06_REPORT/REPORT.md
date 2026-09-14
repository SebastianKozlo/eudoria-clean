# REPORT.md — PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914

RUN_ID: PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 · RUN_CLASS: MATERIAL · MODE: STATIC-ONLY
Executor: pe-reconstruction (direct PE-MASTER dispatch, NO_NESTED_TASKS). Engine-execution
layer ABSENT (the client never ran; nothing here is an "oracle" result). Publication is a
separate step (pe-master-auditor, after PE-MASTER adjudication).

Source identity (own fail-closed S0): `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`,
SHA256 e7785430e81dffe648ce8f5312414b17bc9fce61389689a22f753765d5280f31 == pin, size 8015872
== pin, machine 0x014C (i386), opt_magic 0x010B (PE32), image_base 0x00400000. BASE_SHA
verified: repo `12_WebGame\eudoria-clean` HEAD == origin/master == ls-remote ==
6465019298e66856a2fe9fa9750c047d057c97dd (zero git mutations by the executor; the only
dirty path is the foreign untracked `experiments/`, untouched).

---

## 1. The research question

> Which slots of the SceneFeederObject vtable DIRECTLY read the corrected position stored at
> SF+0x34..0x3C, and what do they do with those values immediately after the read?

## 2. Vtable identity and slot map (derived from the physical EXE, not from any prior report)

Own RTTI walk: [0x00A7D454] = 0x00AA12B8 -> COL (signature=0, offset=0, cd_offset=0,
pTypeDescriptor=0x00B78834, pClassHierarchy=0x00AA12CC) -> TD name
`.?AVSceneFeederObject@@` — PASS. Vtable 0x00A7D458 is in `.rdata` and has EXACTLY 6 slots;
the six contract functions ARE the complete vtable:

| slot | function | body (own derivation) | size |
|---|---|---|---|
| 0 | FUN_0050A460 | 0x0050A460..0x0050A47E | 30 B |
| 1 | FUN_005090A0 | 0x005090A0..0x005090A4 | 4 B |
| 2 | FUN_005090B0 | 0x005090B0..0x005090B4 | 4 B |
| 3 | FUN_0050A050 | 0x0050A050..0x0050A0AA | 90 B |
| 4 | FUN_005090C0 | 0x005090C0..0x005090C7 | 7 B |
| 5 | FUN_00509580 | 0x00509580..0x00509598 | 24 B |

Every body end is evidence-derived (terminal RET + inter-function padding completing to the
16-byte-aligned boundary + independent function-start evidence for the adjacent functions:
0x50A480 has its own 2 E8 callers; 0x50A0B0 has 1 E8 caller + 2 E9 jumpers; 0x5095A0 has 1
E8 caller). Slot 0's sweep initially overran a 2-byte CC pad into the adjacent function
0x50A480; the rule was fixed to alignment-completing CC runs and the decode re-run — the
published listing is the corrected one. Vtable extent ends at slot 5: the next dword
(0x53565064) is ASCII `dPVS` .rdata data, not a code pointer.

## 3. The 6-slot census (full table: 02_ANALYSIS/SCENEFEEDER_SLOT_CENSUS.csv)

| slot | classification | disposition |
|---|---|---|
| 0 · FUN_0050A460 | NO_RELEVANT_ACCESS | Scalar deleting destructor: calls 0x50A240 (dtor body; SEH prologue; sole E8 caller = this slot; NOT decoded — stop rule), then if flags&1 calls 0x95D42A = **MSVCR80.dll.??3@YAXPAX@Z operator delete** (one-hop import-thunk resolve, own IAT walk), returns this. Zero window-field (SF+0x30..0x3C) access. |
| 1 · FUN_005090A0 | NO_RELEVANT_ACCESS (see taxonomy note) | **Position-ADDRESS getter**: `lea eax,[ecx+0x34]; ret` (bytes 8D 41 34 C3). Takes &SF+0x34 and returns it to the virtual caller; reads/writes NO position value. |
| 2 · FUN_005090B0 | NO_RELEVANT_ACCESS | `lea eax,[ecx+0x74]; ret` — address-of SF+0x74, outside the census window. |
| 3 · FUN_0050A050 | **MIXED** | **The one slot that reads the position VALUES.** `GetPosition(out arg1, query arg2)`, ret 8. PRIMARY path (arg2!=NULL): reads the **+0x30 LINK** (0x50A05B), virtual call on the link object (0x50A064, vtable slot 17 [+0x44], dynamic target — class unknown in this run); result+0x90 + arg1 feed 0x437F70 then 0x82B5A0 (not decoded — stop rule). FALLBACK path (arg2==NULL): self-virtual call of **vtable slot 1** (0x50A08E — physically the slot-1 getter above) returns &SF+0x34, then **reads X/Y/Z** at 0x50A090/0x50A098/0x50A09E and **copies the triple into the caller's out buffer** arg1 (0x50A096/0x50A09B/0x50A0A1), returning arg1. **No position value flows into any call.** |
| 4 · FUN_005090C0 | NO_RELEVANT_ACCESS | `lea eax,[ecx+0x80]; ret` — address-of SF+0x80, outside the census window. |
| 5 · FUN_00509580 | NO_RELEVANT_ACCESS | Reads SF+0x18 (outside window), forwards (this->field18, arg1) to 0x4150F0, result to thiscall 0x8B71D0. No window-field access. |

Taxonomy note (documented convention): the classification column carries the position-VALUE
dataflow (read/write/call-flow of SF+0x34..0x3C values). Slot 1 exposes the position BY
ADDRESS without reading values, so its classification is NO_RELEVANT_ACCESS while the
dedicated `takes_position_address=Y` column and this note carry the address-exposure finding.
Slot 3 is MIXED because it reads BOTH the +0x30 link (primary path) and the position values
(fallback path); its position sub-behavior is exactly READ-LOCAL (values copied to the
caller's buffer, never into a call). Both readings are fully supported by
01_RAW/SLOT_DISASSEMBLY.txt and 02_ANALYSIS/ONE_HOP_FLOW.md.

Semantic bonus (in-run consistency proof): slot 3's fallback consumes slot 1's returned
pointer to read X/Y/Z — the getter semantics of slot 1 are demonstrated from within the same
vtable, and the field identity SF+0x34/+0x38/+0x3C = the position triple is cross-confirmed
against the FUN_005094C0 writer window (§5).

## 4. Gates (full detail: 06_REPORT/STAGE_ACCEPTANCE_GATES.csv)

- **G1-SOURCE: PASS** — SHA+size+PE32 all measured equal (fail-closed asserts ran first in
  every script).
- **G2-VTABLE: PASS** — identity confirmed by own walk; vtable physical; six entries derived
  from .rdata (each slot value == function start VA exactly; first-bytes dumped; listings
  decode cleanly from those VAs).
- **G3-COMPLETE-SLOT-CENSUS: PASS** — 6/6 rows, every column filled, allowed vocabulary only.
- **G4-POSITION-ACCESS: PASS** — slot 3's value reads carry raw instruction evidence plus the
  in-run pointer-provenance chain; slot 1 carries the raw `lea` bytes; the negative slots
  carry full-listing evidence of absence.
- **G5-ONE-HOP-FLOW: PASS (vacuous)** — no slot passes position values into a CALL. No
  MODEL / NiAVObject / ArkModelResourceInstanceRef / TRANSFORM_TO_MODEL /
  CANDIDATE_MODEL_BRIDGE claim is made anywhere in this package. The only window-field call
  flow is the +0x30 LINK dispatch (receiver = the link object; class unknown, no claim).

## 5. Positive control

FUN_005094C0 window (01_RAW/POSITIVE_CONTROL_005094C0.txt): measured bytes
`8B 44 24 04 8B 10 89 51 34 8B 50 04 89 51 38 8B 40 08 89 41 3C C6 41 28 01 C2 04 00` —
BYTE-EXACT match to the contract-expected pattern, and 9/9 semantic checks PASS: the
caller-supplied triple pointer [esp+4] is read at +0/+4/+8 and copied into
this+0x34/+0x38/+0x3C, flag this+0x28=1, ret 4. Layer note: the window proves
arg-triple -> SF+0x34..0x3C; the prior-run caller-side identity (arg == instance+0x44) was
not re-derived and is not needed for control validation. **POSITIVE_CONTROL = PASS** (a
failure would have made this run RUN_INVALID).

## 6. Final status

**B** — a slot (FUN_0050A050, slot 3) READS the position (X/Y/Z at SF+0x34/0x38/0x3C, on the
arg2==NULL fallback path) and does NOT send it to a CALL: the values are copied into the
caller's out buffer and returned. Slot 1 additionally exposes &pos by address without
reading. **NEXT_SEAM = NONE** (no position-to-call exists; that concept applies to status A).

### THE ONE NEXT TEST (status B requires exactly one)

**SF+0x30 LINK IDENTITY + SLOT-17 DECODE.** (a) Static writer-scan of SceneFeederObject+0x30
(all stores to [SF-this+0x30] in .text, provenance-checked against SceneFeederObject
constructor sites known from the accepted prior run); (b) RTTI-walk the vtable of the object
type stored at SF+0x30; (c) decode that class's vtable slot 17 ([vtable+0x44] — the exact
virtual target invoked at 0x0050A064 by slot 3's primary path) down to its FIRST call only.
Rationale: slot 3's primary path makes the +0x30 link the PRIMARY position provider
(link->slot17(arg2) result, +0x90 offset, feeds the out buffer via 0x437F70/0x82B5A0), with
the SF+0x34 triple as the NULL-fallback cache; identifying the link and its slot-17 answer
is the shortest static route to the model-bridge direction question (provider-is-model vs
provider-is-other). Scope guards: decode stops at the first call inside slot 17; the maximum
outcome label is CANDIDATE_MODEL_BRIDGE; no runtime work.

## 7. NOT_CHECKED (explicit)

- All callee bodies beyond the allowed one-hop: 0x50A240 (dtor body), 0x437F70, 0x82B5A0,
  0x4150F0, 0x8B71D0, and the dynamic link->vtable[+0x44] target (class unknown).
- The SF+0x30 link object's class/RTTI (requires the writer-scan = the proposed next test).
- Callers of slots 1/3 (who consumes &pos / GetPosition output) — caller-side provenance, out
  of scope; including the shared-tail polymorphism of slot 3's second entry (arg1's vtable,
  caller-side object).
- The `instance+0x44` arg identity of FUN_005094C0's caller (prior-run knowledge, not
  re-derived here).
- Fields outside the census window: SF+0x18 (slot 5), SF+0x74 (slot 2), SF+0x80 (slot 4),
  SF+0x28 (control-window flag), the +0x40..0x48 triple visible after 0x5094D9.
- Runtime override analysis of virtual slots (engine execution ABSENT; all claims scoped to
  instances whose vtable == 0x00A7D458).
- 296445 recovery, template 4508, SceneFeeder→model proof, terrain cells, network/ring/
  executor, placement history — untouched by contract.

## 8. Untouched status (unchanged by this run)

- TRANSFORM_TO_SCENEFEEDER = PROVEN (accepted prior run; positive control re-validated the
  writer window).
- **TRANSFORM_TO_MODEL = NOT_DEMONSTRATED** — this run found NO slot that passes the
  position into any call; nothing here upgrades, downgrades, or re-labels that status.
