# FINAL_REPORT — PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006

RUN_CLASS: BOUNDED_STATIC_RE · Era: PCG 9.3.5 · MODE: STATIC-ONLY (the client NEVER
ran; byte reads and one Ghidra headless import of a hash-verified sandbox COPY only;
no runtime hooking, no network, no payload opening/decoding of VFS/BNT/NIF/ARK).
Executor: pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS).
BASE 3921dbe2a43a9181f8a50fa5242d8586c85896b6 (== origin/master == actual remote).
EXE E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 / 8,015,872 B
(re-verified at preflight, in every instrument, and at QC time).

---

## 1. The question and the answer

**QUESTION (contract §2):** Does a receiver-proven use of FUN_00414130's returned key
connect the SAME MovableObject/ClientMovableObject to a reusable
resource/template/model, or is the key used only for runtime identity/map operations
in the examined path?

**ANSWER:**

1. **FUN_00414130 is NOT a class-specific "get instance key" getter.** It is a shared
   4-byte offset reader `mov eax,[ecx+0x74]; ret` (bytes `8B 41 74 C3` @0x00414130,
   re-pinned from the physical EXE; Ghidra 11.2.1 independently confirms the function
   body [[0x00414130,0x00414133]]). Its **6 direct E8 callsites use at least three
   DIFFERENT receiver kinds**:
   - the ClientMovableObject instance (0x00528FD9, ctor; 0x008561AC, map insert — in
     the examined CREATE chain);
   - the **GameClient singleton** [0x00B9FE5C] (0x004569D3, 0x00456BEB, 0x0045723E —
     NEW callsites, not in any BASE published xref; receiver proven =
     FUN_00401360() → [0x00B9FE5C], 0x88 B, ctor FUN_004157B0, vtable 0x00A79F18 →
     RTTI `.?AVGameClient@@`);
   - a dereferenced pointer [x] via the generic `8B 01 C3` deref helper FUN_004123D0
     (0x0045A08B — receiver class UNRESOLVED within bounds).
   A same-offset read is therefore NOT evidence of the same field, class, or role
   (the contract's warning was confirmed by measurement).

2. **Within the examined path, the key is used for runtime identity/map operations
   only — and NO resource/template/model consumer was demonstrated.**
   - **Insert site (0x008561AC, FUN_00856190):** the key is the STLport hash_map
     identity key on mgr1+0x10 — pair{key=[value+0x74], value=the instance itself},
     find-or-create, duplicate → the value's vtable slot-0 deleting dtor. This map is
     an IDENTITY map (instance-key → the same instance object), byte-distinct from
     the templates.vfs RB-tree registry (root 0x00BA1824, FUN_0043A550/FUN_0072F580).
      Control CTRL_C proves the insert body contains ZERO DIRECT (E8) calls to the
      resource family (FUN_0072F580 / FUN_006C9700 / FUN_006CB6F0 / FUN_006CB020 / FUN_0043A550).
   - **Ctor branch (0x00528FD9 → FUN_005247C0 → FUN_00509330, the selected
     receiver-proven branch):** the key undergoes **NO lookup at all** —
     FUN_005247C0 (the SF factory wrapper, fully decoded this run) performs no map
     or resource operation; the key passes through unchanged into the SF constructor,
     is stored at **[SF+0x14]** (`8B 44 24 50` + `89 45 14` @0x00509372..7E), and is
     passed into the constructor of a 0x14-B object at the budget boundary
     (`E8 50 1D 14 00` @0x0050948B → FUN_0064B1E0) — the THIRD further call edge,
     where the contract's two-edge trace budget stopped the analysis.

3. **OUTCOME = `BOUND_REACHED`.** The receiver-proven trace stopped at the budget
   boundary with the key's next consumer (FUN_0064B1E0 / the key-carrying object)
   unresolved in-budget. No resource edge exists anywhere in the examined path;
   a MAP-identity use is PROVEN at the insert site; the ctor-branch key is
   identity-carrying data whose ultimate consumer was not examined.
   The candidate LEAD families (FUN_0072F580 / FUN_006C9700 / FUN_006CB6F0 /
   FUN_006CB020) were **not on the examined chain** — none is called anywhere in the
   two traced functions or the insert body.

## 2. Enumeration method, range, exclusions (contract §3.1)

- **Method:** linear byte scan of the raw file image of .text (0x00401000..0x00A75000,
  raw_size 0x674000, full section, no gaps skipped): every offset with byte 0xE8 is a
  candidate; target = va+5+signed32(next 4 bytes); hits = target == 0x00414130.
  No exclusions at the raw stage — every raw hit is recorded (E8_CENSUS.json). The
  same scan was run over the WHOLE file (0 hits outside .text), plus an E9
  JMP-thunk census (0 hits) and an absolute-dword census of 0x00414130 (0 hits — no
  address-takers). Published BASE xrefs (0x00528FD9, 0x008561AC) were re-verified by
  target recomputation (both MATCH).
- **Instruction starts:** each candidate verified PROVEN_EXACT by the independent
  tool (Ghidra 11.2.1 `getInstructionAt` — all six are CALL instructions at exact
  instruction starts; Ghidra's own reference graph shows exactly 6 references, all
  UNCONDITIONAL_CALL). The two BASE-published sites additionally sit inside
  BASE-canon function entries (FUN_00528E50 ctor, FUN_00856190 insert).
- **NOT claimed covered:** indirect calls (call reg / call [mem]), inlined reads of
  [x+0x74], alias forms other than E9, and code in sections other than .text. No
  claim about "all readers" is made.

## 3. Shortlist (max 3) and receiver provenance (contract §3.2)

| Site | Containing function | Receiver provenance | Basis |
|---|---|---|---|
| 0x00528FD9 | FUN_00528E50 (ctor) | **SAME_MOVABLE_OBJECT_PROVEN** | prologue `8B F1` MOV ESI,ECX @0x00528E76; ClientMovableObject vtable store `C7 06 B0 DC A7 00` @0x00528EA2 (RTTI `.?AVClientMovableObject@@` calibration PASS; Ghidra names the vftable); `8B CE` MOV ECX,ESI @0x00528FD2 immediately before the call (CTRL_B gate) |
| 0x008561AC | FUN_00856190 (insert) | **SAME_MOVABLE_OBJECT_PROVEN_IN_EXAMINED_CREATE_CHAIN** | receiver = EDI = the value argument (`8B CF` @0x008561AA); in the examined CREATE chain (FUN_004C46C0 → insert @0x004C47DA, BASE canon) the value is the new MovableObject |
| 0x0045A08B | FUN_00459fd0 | **UNRESOLVED** | receiver = [EBX] via FUN_004123D0 (`8B 01 C3`); EBX's class not resolvable within bounds; the read value is PUSHed as the last stack arg of FUN_00853d00(mgr1, 0, &l1, &l2, 2, value) — the strongest NEW resource lead (mgr1-family query), NOT decoded (function #8, out of budget) |

Census-classified, not shortlisted (the 3-site GameClient idiom): 0x004569D3,
0x00456BEB, 0x0045723E — **DIFFERENT_OBJECT** (receiver = the GameClient singleton
returned by FUN_00401360; [GameClient+0x74] then used as the RECEIVER of
FUN_004A9850 with a &param-set-pair stack arg; FUN_004A9850 not decoded).

## 4. The selected branch trace (≤2 further call edges — contract §3.3)

Callsite 0x00528FD9: key = [CMO+0x74] → PUSH @0x00528FDE → FUN_005247C0(this=EDI=holder, arg1=key, arg2=&string) @0x00528FE1 → result [this+0xC0] @0x00528FEA (the SceneFeederObject pointer — BASE canon re-verified in bytes).

- **Edge 1 — FUN_005247C0 (full own decode this run):** SEH prologue; `PUSH 0x98;
  CALL 0x0095D3C4` (operator new); alloc-fail skip; `8B 4C 24 28` (arg2=string) +
  `8B 54 24 24` (arg1=**key**) + `51 52 57` (push string, key, holder) + `8B C8`
  (ECX=new block) + `E8 1C 4B FE FF` @0x0052480F → FUN_00509330; then
  FUN_005094E0(this=SF, &holder+0xC0) (back-ptr) and FUN_006A8980(this=holder+0x24,
  2 stack ptrs) (list registration); `RET 8`. **The key is NOT used for any lookup
  in this function** — no map find, no registry call, no resource call. The key
  arrives purely as ctor data.
- **Edge 2 — FUN_00509330 (SF ctor, key-relevant full own decode):** vtable store
  `C7 45 00 58 D4 A7 00` (0x00A7D458 = SceneFeederObject, RTTI calibration PASS);
  `[SF+0x14] = arg2 = the KEY` (`8B 44 24 50` + `89 45 14` @0x00509372..7E);
  `[SF+0x8C] = arg1 = holder` (`89 8D 8C 00 00 00` @0x00509411); new(0x118) +
  FUN_007B6000 → `[SF+0x30]` = the refcounted NiNode + refcount++ @+4 (BASE canon
  chain re-verified in bytes); **tail:** `PUSH 0x14` + new + `8B 55 14`
  (EDX = [SF+0x14] = **the KEY**) + `PUSH EDX` + `8B C8` + `E8 50 1D 14 00`
  @0x0050948B → **FUN_0064B1E0** — the THIRD further call edge = the budget
  boundary → **STOP**; then `8B 4D 30` + `PUSH EAX` + `PUSH 0x00A7D444` +
  `E8 D9 D5 2A 00` @0x005094A2 → FUN_007B6A80 (registration into the NiNode — edge
  recorded, callee NOT decoded); `RET 0xC` (confirms the 3-stack-arg ABI:
  holder, key, string).

## 5. The boundary lead (NON-CANONICAL, disclosed over-budget probe)

At the budget boundary a bounded "head probe" was executed on FUN_0064B1E0 (intended
as an identity probe; the 0x30-byte dump covered the function's entire 27-byte body —
**an over-budget probe, disclosed**: FUNCTION_LEDGER row 7, QC_REPORT Q7). Probe
content (recorded as a NON-CANONICAL LEAD, NOT load-bearing): FUN_0064B1E0 constructs
a 0x14-B object with vtable 0x00A83274 → RTTI **`.?AVSceneFeederObjectExtraData@@`**,
stores the KEY at [obj+0x10] (`89 46 10` @0x0064B1EC), calls a base ctor FUN_007C8780,
`RET 4`; FUN_00509330 registers this object into the SF's NiNode (FUN_007B6A80 args:
[SF+0x30], obj, 0x00A7D444 — the third arg probed NOT-A-CLASS-VTABLE). **The consumers
of SceneFeederObjectExtraData+0x10 were NOT examined** — this is the NEXT_INPUT/EDGE
for any follow-up run. No resource/template/model consumer claim is made from it.

## 6. Budget accounting and the disclosed deviation

- COUNTED (6, the contract maximum): FUN_00414130 (getter), FUN_00528E50 (selected
  caller), FUN_005247C0 (edge 1), FUN_00509330 (edge 2), FUN_00856190 (map insert /
  key-to-map negative), FUN_00401360 (receiver classification).
- DISCLOSED probes beyond the 6: FUN_0064B1E0 (27-B body fully read by an unguarded
  boundary probe — over-budget deviation, disclosed, non-load-bearing, NOT repeated);
  FUN_004157B0 (0x30-B head read only: the vtable store, for the GameClient
  classification — bounded classification probe, disclosed).
- Sites examined in detail: 3 shortlisted (2 traced as branches); census-classified:
  3 more. Further call edges traced from the selected callsite: 2 (budget respected);
  the 3rd edge recorded and stopped at. No 4th shortlisted site, no second deep
  branch, no function-#8 analysis.

## 7. Status algebra (per material record; contract §5)

| Record | FUNCTION_IDENTITY | OBSERVED_OPERATION | FINAL_SEMANTIC_ROLE | HISTORICAL_INPUT_AVAILABILITY |
|---|---|---|---|---|
| FUN_00414130 | CONFIRMED (bytes + Ghidra + RET/CC boundary) | mov eax,[ecx+0x74]; ret | SHARED +0x74 OFFSET READER (not class-specific; 3 receiver kinds proven) | n/a (code) |
| FUN_00528E50 | CONFIRMED ClientMovableObject ctor (vtable/RTTI) | base ctor + derived vtable + SF-creation chain | THE selected receiver-proven caller | consumes a message-derived record (BASE canon); NO historical value recovered |
| FUN_005247C0 | CONFIRMED SF factory wrapper (RET 8) | new(0x98) + ctor delegation + back-ptr + list registration; NO lookup | create-and-register wrapper (key = pass-through ctor data) | n/a |
| FUN_00509330 | CONFIRMED SceneFeederObject ctor (vtable/RTTI, RET 0xC) | [SF+0x14]=key; [SF+0x8C]=holder; NiNode attach; key → FUN_0064B1E0 (boundary) | SF ctor carrying the instance key as identity data | n/a |
| FUN_00856190 | CONFIRMED mgr1 hash_map insert | key=[value+0x74]; pair{key,value}; find-or-create; duplicate→deleting dtor | RUNTIME IDENTITY MAP (NOT a resource join; CTRL_C) | value = the instance object (examined CREATE chain) |
| FUN_00401360 | CONFIRMED lazy singleton getter | return [0x00B9FE5C] (new(0x88)+FUN_004157B0 on miss) | GameClient-singleton getter (receiver classifier) | n/a |
| FUN_0064B1E0 (probe) | SceneFeederObjectExtraData ctor (RTTI probe) | [obj+0x10]=key; base ctor; RET 4 | NON-CANONICAL LEAD (identity-carrier; consumers unexamined) | n/a |

Two distinct records referencing one key (the ctor store + the map insert) do NOT
prove world instances — no such claim is made here.

## 8. Material PASS records (contract §5 requirement per important PASS)

- **Getter pin PASS**: MEASURED_QUANTITY = the 4 bytes at 0x00414130; INDEPENDENT
  SOURCE_OF_TRUTH = physical EXE + Ghidra instruction; WHY_NON_CIRCULAR = two
  independent readers (own walk + Ghidra) agree without sharing code;
  FAILURE_CASE_DETECTED = the +0x78 expectation mutation FAILS (CTRL_A);
  coverage limit = the 4-byte getter pin only.
- **All-6-instruction-starts PASS**: MEASURED = 6/6 PROVEN_EXACT by Ghidra;
  INDEPENDENT SOURCE = Ghidra's own flow analysis vs my raw byte scan;
  NON_CIRCULAR = different engines; FAILURE_CASE = a mid-instruction E8 (like the
  census patterns outside .text, all 0) would have no instruction at the VA and be
  caught; coverage = direct E8 calls in .text only.
- **Receiver-proven ctor branch PASS**: MEASURED = the 4-edge byte chain;
  INDEPENDENT SOURCE = physical EXE + RTTI calibration + Ghidra vftable naming;
  NON_CIRCULAR = RTTI name re-derived from EXE data, not from a label;
  FAILURE_CASE = removing edge E3 (CTRL_B) FAILS the claim; coverage = the ctor
  callsite receiver.
- **Map-identity PASS (resource-join negative)**: MEASURED = the insert body's byte
  pins + the zero-resource-family E8 census; INDEPENDENT SOURCE = physical body
  bytes + the BASE-canon resource-family address list (read as input);
  NON_CIRCULAR = the detector enumerates E8 targets directly; FAILURE_CASE = the
  injected fake E8→FUN_0072F580 is detected (CTRL_C falsifier); coverage = the
  decoded insert body only.

## 9. Untouched statuses and honesty block

- WORLD_XYZ_RECOVERED = NO; STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED;
  HISTORICAL_INSTANCE_DATA_RECOVERED = NO; PE_MASTER = PROVISIONAL_UNTIL_QUALIFIED;
  CANONICAL_GATE_EFFECT = NONE; NEXT_EXPERIMENT_AUTHORIZED = NO.
- Negative results concern the examined branch, not every PE path. No positive join
  was forced; no historical values are claimed.
- NEXT_INPUT/EDGE (at most one recommendation, DESIGNED_NOT_EXECUTED): decode the
  SceneFeederObjectExtraData chain — FUN_0064B1E0's base ctor FUN_007C8780, the
  semantics of FUN_007B6A80's registration, and the readers of ExtraData+0x10 — to
  determine whether the carried instance key ever reaches a resource/template/model
  consumer. (The UNRESOLVED shortlisted site 0x0045A08B — the FUN_00853d00 mgr1-family
  query — is the second-ranked lead, noted without recommendation weight.)
- Persistence per the human dispatch: commit/push NOT performed; AUDIT_ENTRYPOINT.md
  NOT edited (proposed row in HANDOFF.md); the manifest was computed WITHOUT the
  entrypoint row (see HANDOFF §persistence).
