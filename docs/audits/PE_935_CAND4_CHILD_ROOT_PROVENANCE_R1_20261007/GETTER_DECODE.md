# GETTER_DECODE — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

The contract §4 deliverable: the complete bounded body of FUN_006C66D0 (the CAND-4
child getter), its operation class, the measured field offset, and the bounded
producer trace of that field's value on the examined path variant.

Decoder identity: capstone 5.0.7 (cs_version (5,0,1280); package + native engine
SHA256 in INPUT_IDENTITIES.md §4); all bytes read through the fail-closed pinned
EXE reader; every rel32 target independently recomputed by this run's own
arithmetic (call_va + 5 + int32(rel32)); the two implementations agree.

## 1. THE GETTER BODY (complete bounded body; raw window 01_RAW/FUN_006C66D0_GETTER_FULL.txt)

```asm
0x006C66D0  8B 41 68    mov eax, dword ptr [ecx + 0x68]
0x006C66D3  C3          ret
```

- Entry 0x006C66D0 (byte-exact: all three examined callers reach it by verified
  rel32 — 0x0050A3AF, 0x0050A39D, 0x0050A34B, each recomputed to 0x006C66D0).
- Extent 0x006C66D0..0x006C66D4 — RESOLVED. Provenance of the extent claim (a
  CC/RET heuristic alone is NOT proof): the terminal ret C3 @0x006C66D3 is
  followed by 12 consecutive int3 alignment bytes 0x006C66D4..0x006C66DF and the
  aligned entry of a distinct next body at 0x006C66E0 (push esi; standard
  prologue) — the function is exactly 4 bytes.
- Branches: NONE. NULL handling: NONE (raw field value returned).
- Return convention: EAX = [this+0x68]; thiscall, no stack cleanup.

```text
GETTER_OPERATION = DIRECT_FIELD_GETTER
ARKMODELMANAGER_CHILD_FIELD_OFFSET = 0x68 (measured: 8B 41 68)
```

## 2. WHAT THE FIELD HOLDS (the §2 answer, measured)

The class of the receiver is CONFIRMED by RTTI measured from the vtable chains:
vtable 0x00A855D0 -> .?AVArkModelManagerMain@@ (derived; written by the derived
ctor @0x006C0D9B); base vtable 0x00A85A08 -> .?AVArkModelManager@@ (written by
the base ctor @0x006C8FAB). The +0x68 field lies in the BASE-class region.

The child value is a REFCOUNTED OBJECT POINTER:
- the writer stores it with incref [value+4] (01 5F 04 @0x006C67E7) and
  decrefs/zero-destroys the previous value via its vtable slot 1
  (@0x006C67D4/0x006C67DE) — the NiObject-family refcount protocol
  (consistent with the prior join-operation canon's refcount fingerprint);
- after the write, the object is used as a NAMED-LOOKUP ROOT: two conditional
  lookups via FUN_007B6C30 run ON the stored child, with measured name
  constants 'ArkTexture' (0x00A859F8) and 'ArkAnimation' (0x00A8547C).

## 3. BOUNDED PRODUCER TRACE (writer census within the declared scope)

Examined-path chain (the only manager-receiver calls between the allocation
0x006A3A4D and the getter call 0x0050A3AF):

| step | function | role | measured facts |
|---|---|---|---|
| 1 | FUN_006C0D50 (derived ctor; called @0x006A3A77) | construction | delegates to base ctor @0x006C0D64 (args 4, param, FUN_00733340-result); zeroes derived region +0x110..+0x12A; vtable 0xA855D0 @0x006C0D9B |
| 2 | FUN_006C8F80 (base ctor) | **WRITER W1: NULL reset** | `mov [esi+0x68], ebx` @0x006C8FD3 (89 5E 68); also [+0x6C]=0 @0x006C8FE3, flag [+0xEC]=0 @0x006C9014; inits the +0x70 template holder (FUN_005670A0 @0x006C8FE6) and the +0xA0 sub-object (FUN_0043A330 @0x006C9005) |
| 3 | FUN_006C8B20 (lazy init; called @0x006A3A8D) | trigger | if flag [+0xEC]==0 and [+0x68]==0 -> call FUN_006C6F60 @0x006C8B3A; on success set [+0xEC]=1, register callbacks (FUN_006C7740 with constants FUN_006C66E0/FUN_006C6CE0), dispatch vtable slot 3 (0x006C19B0, not opened) |
| 4 | FUN_006C6F60 (producer) | instance creation | guard [+0x6C]==0; validity check of the [+0x70] holder (FUN_0072FCE0 @0x006C6F97); two import-mediated lookups with the EMPTY-STRING key 0x00A7957B; A = FUN_007CE1E0([this+0x70]) @0x006C6FF6 (the prior-canon getter A); instance = FUN_006C9700(A, &local, &local, 0) @0x006C6FFC (cdecl; the prior-canon instance-creator pump); `mov [esi+0x6C], eax` @0x006C7008; on success call FUN_006C6780 @0x006C7049 + dispatch vtable slot 2 (0x006C0FD0, not opened) |
| 5 | FUN_006C6780 (installer) | **WRITER W2: the value producer** | guards [+0x68]==0 and [+0x6C]!=0; `mov edi, [eax+4]` @0x006C67BE (eax = the instance); `mov [esi+0x68], edi` @0x006C67E2 (89 7E 68) with the refcount swap; then the two named lookups ('ArkTexture'/'ArkAnimation'). PARTIAL body: the 200-byte window ends at 0x006C6848 mid-body — extent UNRESOLVED past the window; no continuation is claimed (contract §4). |

```text
CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
```

Why not CONFIRMED_MODEL_DERIVED (contract §4 bar — multiple unresolved elements):
1. The semantic identity of [instance+4] is UNRESOLVED (GAP-1): the creation
   chain (FUN_006C9700) was not opened; the prior-canon wrapper class
   (.?AVArkModelResourceInstanceRef@@, vtable 0x00A864B8, prior field map
   refcount@+4/item@+8) CONTRADICTS the [instance+4]-as-pointer use if the pump
   returns that wrapper.
2. FUN_006C8BB0 (the second on-path manager method, called @0x006A3A94) is
   NOT_CHECKED (GAP-2) — an alternative/overwriting producer cannot be excluded.
3. The model-typing of A on this path stands on prior canon only (the
   {0x66=MODEL, A} family; no payload/type emission was examined here).

## 4. Getter callsites on the examined path (context)

- @0x0050A34B — old-manager detach path (the old child = the OLD manager's
  [+0x68]; pushed for the NiNode slot-42 detach; prior canon V02).
- @0x0050A39D — install gate: `je 0x50A453` bails the whole install if the
  new manager's [+0x68] is NULL — the examined variant REQUIRES a non-NULL
  child, i.e. the lazy producer chain MUST have run successfully.
- @0x0050A3AF — THE child getter: result EAX -> EDI @0x0050A3B7 -> push EDI
  @0x0050A3F6 -> NiNode slot-41 join call @0x0050A3F7 (see §7 records:
  01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt).

## 5. Raw records of this deliverable

- 01_RAW/FUN_006C66D0_GETTER_FULL.txt (the getter + extent provenance)
- 01_RAW/FUN_006C0D50_CTOR_DECODE.txt (body #2)
- 01_RAW/FUN_006C8F80_BASECTOR_DECODE.txt (body #3)
- 01_RAW/FUN_006C8B20_LAZYINIT_DECODE.txt (body #4)
- 01_RAW/FUN_006C6F60_PRODUCER_DECODE.txt (body #5)
- 01_RAW/FUN_006C6780_INSTALLER_PARTIAL.txt (body #6, partial, extent UNRESOLVED)
- 01_RAW/PINS_AND_REL32.txt (56 byte pins + 23 rel32 recomputes)
- 01_RAW/VTABLE_RTTI_STRINGS.txt (vtable/RTTI/string data evidence)
