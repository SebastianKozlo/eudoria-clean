# OBJECT_IDENTITY.md — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004

PHASE D. What EXACT value/object is written at factory+0x84.

## The assigned value

The setter's store `MOV [ESI+0x84],EAX` @0x0070C71E writes EAX where:

- **Success path** (allocation succeeded): EAX = the object returned by
  `CALL FUN_00972380` @0x0070C715 — the constructor of a freshly allocated
  **0xA4-byte heap object** (`PUSH 0xA4` @0x0070C6F9; `MOV ECX,new` @0x0070C713).
  The constructor returns `this` (`MOV EAX,ESI; ... RET` @0x009724C5-...-D9).
- **Allocation-failure path**: EAX = 0 (`XOR EAX,EAX` @0x0070C71C) — the same
  store instruction writes NULL.

ASSIGNED_VALUE_REPRESENTATION = **OBJECT_POINTER** (a heap object pointer; NULL only
on the allocation-failure branch of the same store).

## The assigned object (immediate structural identity — STOP point per contract)

| Field | Measured value |
|---|---|
| ASSIGNED_OBJECT_CONSTRUCTOR | **FUN_00972380** (extent 0x00972380..0x009724D9, ~0x15C bytes; first CC pair at 0x009724DA) |
| ASSIGNED_OBJECT_VTABLE | **NONE — the object is NON-POLYMORPHIC**: no vtable store exists anywhere in the ctor extent (searched C7 06/89 06/89 07/C7 07-style [this] stores of .rdata pointers); all its methods are invoked by DIRECT rel32 calls, not virtual dispatch |
| Allocation size | 0xA4 bytes (280) |
| Reader-family methods (direct-called on this object) | FUN_00971AD0 (the per-record reader — the SAME function the consumer invokes on [factory+0x84], prior canon), FUN_00971650 (advance/verify, consumer-invoked), 0x00972DF0 (the post-attach method called by the setter itself @0x0070C742, body NOT decoded) |

### Measured structure (from the ctor's own stores)

- `MOV [ESI+0x18],-1` @0x009723D3 (a -1 sentinel member).
- An **embedded 0x14-byte cursor-like object at +0x3C**: `LEA EDI,[ESI+0x3C]`
  @0x00972427; `PUSH 1` / `PUSH 0x80` (init args); `[EDI+4] = 0x80` (SIZE = 0x80)
  @0x00972443; `CALL new(0x80)` → `[EDI] = buffer` @0x00972452; `[EDI+0x11] = 1`
  (flag) @0x00972454 — **an embedded 0x80-byte record buffer**.
- Tail pairs: `[+0x88]=1`, `[+0x8C]=0x80`, `[+0x90]=0`, `[+0x94]=1`,
  `[+0x98]=0x80`, `[+0x9C]=0` (@0x00972499..0x009724C4) — two
  {flag=1, size=0x80} pairs.

### Corroboration (NOT a bridge claim)

The 0x80-byte embedded record buffer + the {1, 0x80} pairs match the consumer's
record-read discipline (FUN_0070DCF0 reads ONE record of ≤0x80 bytes + 8-byte
framing into a 0x80-byte buffer with cursor init (0x80, 1) — prior canon), and the
setter's post-attach call passes the driver locals that included {0x80, 8}. The
object is structurally A RECORD STREAM of 0x80-byte records with 8-byte framing
configuration. This is structural corroboration between the attached object and the
consumer's read path — it does NOT assert that any particular runtime read succeeds.

**LEAD (recorded, NOT used)**: the same ctor FUN_00972380 is called at 0x0072FA76
inside the templates.vfs reader-chain region (FUN_0072FA30 reader → per-record
FUN_00971AD0 → parse — R1 canon), i.e. the attached-object class is the SAME CLASS
as the one used when reading templates.vfs. This is a reader-family class
coincidence and a STRONG LEAD for the next experiment; per the anti-numeric-
coincidence discipline and the contract's out-of-scope list, NO physical-record /
file-bridge claim is made here.

## The NULL-only vs non-null discipline (dispatch clarification 2)

This run found a genuine NONNULL_ASSIGNMENT (the 0xA4 stream object), so the
NULL-only field states do NOT apply:
ASSIGNED_OBJECT_IDENTITY for NULL stores = NOT_APPLICABLE_FOR_NULL applies only to
the 0x0070D013 initialization row (INITIALIZATION_NULL; EBX=0).

## Terminal Phase D fields

```text
ASSIGNED_VALUE_REPRESENTATION = OBJECT_POINTER
ASSIGNED_OBJECT_IDENTITY       = 0xA4-BYTE NON-POLYMORPHIC RECORD-STREAM OBJECT
                                 (ctor FUN_00972380; embedded 0x80-B record cursor
                                 at +0x3C; {1,0x80} pairs; direct-call methods
                                 FUN_00971AD0 / FUN_00971650 / 0x00972DF0)
ASSIGNED_OBJECT_VTABLE         = NONE (non-polymorphic; no vtable store in the ctor)
ASSIGNED_OBJECT_CONSTRUCTOR    = FUN_00972380
ULTIMATE_VALUE_SOURCE          = UNKNOWN  (STOP at object identity per contract;
                                 the driver's "Cache\" / "Parameters\" string
                                 constants are bounded context, NOT a provenance
                                 classification)
FILE_DERIVED_VALUE_EXCLUDED    = NO
RECORD_A_RELATION              = NOT_ESTABLISHED
```

HARD STOP here per the contract: no templates.vfs opening, no RECORD_A, no
backing-source resolution, no file/network/cache classification beyond the bounded
observations above.
