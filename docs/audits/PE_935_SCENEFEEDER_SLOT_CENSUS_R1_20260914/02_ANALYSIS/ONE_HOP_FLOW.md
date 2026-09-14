# ONE_HOP_FLOW.md — PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914

Minimal dataflow documentation for every slot with window-field (SF+0x30/+0x34/+0x38/+0x3C)
involvement, plus the one-hop checks performed (thunk resolution, function-start evidence).
Per the contract dataflow-stop rule, every flow below is documented ONLY up to the FIRST CALL;
no callee body was decoded beyond the explicitly allowed one-hop resolutions.

Layer labels used: [BYTES] original EXE bytes; [DISASM] own capstone 5.0.7 x86-32 listing
(01_RAW/SLOT_DISASSEMBLY.txt); [ADJ] executor adjudication; [HYP] hypothesis (explicitly
marked); engine execution layer: ABSENT (no runtime evidence claimed or implied).

---

## slot 3 — FUN_0050A050 (the only slot that reads the position VALUES)

Two-path function, `ret 8` (thiscall + 2 stack args: arg1 = out buffer, arg2 = optional
provider/query). Body 0x0050A050..0x0050A0AA.

### Path A (primary; taken when arg2 != NULL and the +0x30 link answers non-NULL)

```
0050A05B  mov ecx, [esi+0x30]     ; [DISASM] esi = this (0x50A057 mov esi,ecx)
                                  ; READ of SF+0x30 (the LINK field)
0050A05E  mov edx, [ecx]          ; link->vtable
0050A060  push eax               ; eax = arg2 (loaded 0x50A050)
0050A061  mov eax, [edx+0x44]     ; vtable slot 17 (0x44/4)
0050A064  call eax                ; FIRST CALL. STOP.
```

- Dataflow proven (up to the call only): SF+0x30 (link pointer) -> ecx -> receiver of the
  virtual call at 0x50A064; arg2 -> stack argument. **No position value (SF+0x34..0x3C) is
  read on this path at all.**
- Receiver: the SF+0x30 link object. Class/RTTI: **unknown in this run** — the vtable is read
  from the object at runtime; statically only the slot index (+0x44 = slot 17) is known. This
  is exactly the one-hop limit; identifying the link class is the proposed next test (see
  REPORT.md §NEXT_TEST), NOT performed here.
- Post-call shape (recorded for context only; flows STOP at the first call): the call result
  is tested, and if non-NULL, result+0x90 and arg1 are passed to 0x437F70, whose result feeds
  thiscall 0x82B5A0. Callees not decoded (stop rule).

### Path B (fallback; taken when arg2 == NULL via 0x50A059, or the Path-A virtual call
### returned NULL via 0x50A068 — on the first entry esi is still `this`)

```
0050A087  mov edx, [esi]          ; esi = this -> SceneFeederObject vtable 0x00A7D458
0050A089  mov eax, [edx+4]        ; vtable slot 1 -> physically 0x005090A0
                                  ;   (proven from the .rdata dump in
                                  ;    01_RAW/VTABLE_AND_SLOTS.txt: slot 1 = 0x5090A0)
0050A08C  mov ecx, esi            ; ecx = this
0050A08E  call eax                ; FIRST CALL (self-virtual slot 1). STOP.
                                  ;   target = FUN_005090A0 = lea eax,[ecx+0x34]; ret
                                  ;   => returns &this->pos (SF+0x34) in eax
0050A090  mov edx, [eax]          ; READ X = SF+0x34 (through returned pointer)
0050A092  mov ecx, [esp+8]        ; ecx = arg1 (caller out buffer)
0050A096  mov [ecx], edx          ; arg1[0] = X
0050A098  mov edx, [eax+4]        ; READ Y = SF+0x38
0050A09B  mov [ecx+4], edx        ; arg1[4] = Y
0050A09E  mov eax, [eax+8]        ; READ Z = SF+0x3C
0050A0A1  mov [ecx+8], eax        ; arg1[8] = Z
0050A0A4  mov eax, ecx            ; return arg1
0050A0A7  ret 8
```

- Position dataflow (complete, because NO further call occurs after 0x50A08E):
  SF+0x34/0x38/0x3C -> [eax]/[eax+4]/[eax+8] reads -> edx/eax registers -> stores into
  the CALLER's out buffer arg1. **The position values do NOT flow into any call.**
  `position_to_call = N`.
- The reads are indirect (through the pointer returned by the self-virtual slot-1 call).
  Provenance of that pointer is STATIC and in-run: vtable[1] of 0x00A7D458 = 0x5090A0, whose
  3-byte body is `lea eax,[ecx+0x34]; ret` [BYTES: 8D 41 34 C3]. Therefore [eax] = SF+0x34,
  [eax+4] = SF+0x38, [eax+8] = SF+0x3C for every instance whose vtable is 0x00A7D458.
- [HYP] bounded caveat (engine execution ABSENT): if a DERIVED class overrode slot 1, the
  returned pointer could differ; no override site exists within this vtable and no runtime
  check is possible in a STATIC-ONLY run. The claim is explicitly scoped to instances whose
  vtable == 0x00A7D458 (the RTTI-verified SceneFeederObject vtable).
- Second-entry subtlety (0x50A068 path): when Path A's virtual call returns NULL, esi has been
  reloaded to arg1 (0x50A06A), so the shared tail at 0x50A087 then dispatches on ARG1's
  vtable (caller-side object, unknown class, out of scope). The SF position reads occur on
  the arg2==NULL entry (esi = this, proven). This subtlety is recorded for honesty; it does
  not change the slot-3 census row.

### slot 3 verdict
- reads_sf30 = Y (Path A), reads_sf34/38/3c = Y (Path B), writes_sf34/38/3c = N (writes go to
  arg1, the caller's buffer — targets [ecx]/[ecx+4]/[ecx+8] with ecx = arg1, not SF fields),
- takes_position_address = N (the address is taken by the CALLEE slot 1, not in this body),
- position_to_call = N, classification = MIXED (link read + position value read; the position
  sub-behavior is READ-LOCAL: values copied to the caller's out buffer, never into a call).

---

## slot 1 — FUN_005090A0 (position-ADDRESS getter; no value read)

```
005090A0  lea eax, [ecx+0x34]     ; [BYTES: 8D 41 34] eax = &this->pos (SF+0x34)
005090A3  ret                     ; returns the ADDRESS to the virtual caller
```

- Address dataflow: this -> lea -> eax -> returned to the CALLER (the address leaves the
  function through the return value; it does not flow into a call FROM this function).
- No SF+0x34/0x38/0x3C value is read or written in this body; SF+0x30 is not touched.
- In-run consumer demonstration: slot 3's fallback (0x50A08E) calls this slot virtually and
  reads X/Y/Z through the returned pointer — proving the getter semantics from within the
  same vtable.
- Census disposition: takes_position_address = Y; classification NO_RELEVANT_ACCESS under the
  documented VALUE-dataflow convention (no value read/write, no call flow); the address
  exposure itself is a first-class finding, carried by the dedicated column and this note.

---

## slot 0 — FUN_0050A460 (scalar deleting destructor; no window-field access)

```
0050A463  call 0x50A240           ; ecx = this (thiscall) -> dtor body (NOT decoded)
0050A468  test byte [esp+8], 1    ; deleting-dtor flags argument
0050A470  call 0x95D42A           ; push this -> operator delete
```

- One-hop thunk resolution (allowed): 0x95D42A = `FF 25 5C 53 A7 00` -> IAT 0x00A7535C ->
  **MSVCR80.dll.??3@YAXPAX@Z (operator delete(void*))** — resolved by the executor's own
  import-table walk. This confirms the scalar-deleting-destructor reading.
- 0x50A240: SEH prologue (`6A FF 68 A3 AC 9B 00 ...`), exactly 1 direct E8 caller (0x50A463,
  this slot) -> the SceneFeederObject destructor body candidate. NOT decoded (stop rule);
  if PE-MASTER wants it, it is a separately dispatchable seam, but it is not
  position-relevant evidence for the census (the slot body itself reads none of
  +0x30..+0x3C).
- No NEXT_SEAM is claimed from slot 0 (final status is B, not A).

---

## slots 2 and 4 — FUN_005090B0 / FUN_005090C0 (address getters for OTHER fields)

`lea eax,[ecx+0x74]; ret` and `lea eax,[ecx+0x80]; ret` — address-of SF+0x74 / SF+0x80,
both outside the census window (0x30..0x3C). No window-field access. Negative results.

---

## slot 5 — FUN_00509580 (forwards arg1 with this->field18; no window-field access)

```
00509584  mov ecx, [ecx+0x18]      ; READ SF+0x18 (outside window)
00509589  call 0x4150F0           ; (this->field18, arg1) - receiver carries no window field
00509590  call 0x8B71D0           ; thiscall on result - no window field
```

- 0x18 is NOT in {0x30, 0x34, 0x38, 0x3C}: negative result for the census window.
- Callees not decoded (stop rule); neither receiver involves any window-field data.

---

## One-hop evidence used for body-end boundaries (no callee decode)

- 0x50A480 (follows slot 0's true end): own E8 callers 0x50B03A, 0x58EE19 -> separate
  function start; slot 0 body ends at 0x50A47E (ret 4 @0x50A47B + 2-byte cc pad completing
  to the 16-byte-aligned boundary 0x50A480).
- 0x50A0B0 (follows slot 3's end): E8 caller 0x44CC41 + 2 E9 jumpers -> separate function
  start; slot 3 body ends at 0x50A0AA (ret 8 @0x50A0A7 + 6-byte cc pad).
- 0x5095A0 (follows slot 5's end): E8 caller 0x442DF2 -> separate function start; slot 5 body
  ends at 0x509598 (ret 4 @0x509595 + 8-byte cc pad).
- Slots 1/2/4 end at their single `ret` with 11-12 byte cc pads; the next 16-aligned VA is
  the next vtable slot (next_known boundary, cross-checked both ways).

## NEXT_SEAM

NONE — final status class is B (no slot passes position values into a call; there is no
position-to-call seam to name). The single proposed next test is in REPORT.md §NEXT_TEST.
