# SF30_PROVENANCE - value-source chains for PROVEN_SF30_WRITER rows
RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · Era: PCG_9_3_5 · STATIC-ONLY

All VAs and bytes below are MEASURED from the physical EXE (own PE walk,
capstone 5.0.7 x86-32). STATIC-ONLY. Chains stop at creation/receipt of the
written value; the value's later behavior is NOT followed (contract).

## P1. writer 0x005093C3 (SF ctor FUN_00509330): [SF+0x30] = new(0x118) block

Receiver proof: 0x00509357 `mov ebp,ecx` (SF-this from thiscall ecx);
0x00509366 `mov dword ptr [ebp],0xa7d458` (SF vtable store at [this+0]);
hence [ebp+0x30] == SF+0x30.

| hop | VA | bytes | instruction | evidence |
|---|---|---|---|---|
| 00509376 | 6818010000 | `push 0x118` | alloc size 0x118 pushed |
| 005093A0 | e81f404500 | `call 0x95d3c4` | operator new (thunk 0x95D3C4 = MSVCR80.dll.??2@YAPAXI@Z) |
| 005093A5 | 83c404 | `add esp, 4` | cdecl cleanup of the new() arg |
| 005093AC | 3bc3 | `cmp eax, ebx` | null test of the new block |
| 005093B5 | 53 | `push ebx` | ctor arg = 0 (ebx) |
| 005093B6 | 8bc8 | `mov ecx, eax` | ecx = new block (this for 0x7B6000) |
| 005093B8 | e843cc2a00 | `call 0x7b6000` | block initializer FUN_007B6000(this=block, 0) |
| 005093BD | eb02 | `jmp 0x5093c1` | skip-null path join |
| 005093BF | 33c0 | `xor eax, eax` | alloc-fail path: eax = 0 |
| 005093C1 | 3bc3 | `cmp eax, ebx` | null test of initialized block (ctor return) |
| 005093C3 | 894530 | `mov dword ptr [ebp + 0x30], eax` | WRITE: SF+0x30 = block pointer |
| 005093C6 | 7404 | `je 0x5093cc` | if null skip refcount |
| 005093C8 | 83400401 | `add dword ptr [eax + 4], 1` | refcount++ at block+4 |

Source chain (creation/receipt level): operator new(0x118) -> initialized by
FUN_007B6000 (thiscall this=block, arg=0) -> returned block pointer stored at
SF+0x30 -> refcount dword at block+4 incremented. STOP (later behavior not
followed).

Block initializer identity evidence (only what Task C needs; NO method of
the link vtable is decoded anywhere in this run; callees inside the block ctor
are recorded at receipt level only and are NOT analyzed):

- 007B6023 `mov esi, ecx` mov esi,ecx - this = block
- 007B6029 `call 0x7c02d0` call 0x7C02D0 with this=block (callee NOT analyzed - receipt-level only)
- 007B6041 `mov dword ptr [esi], 0xa8ccf4` VTABLE STORE: [this] = 0x00A8CCF4
- 007B6047 `call 0x788480` call 0x788480 with ecx = &block[+0xC8] (lea ecx,[esi+0xC8] @0x007B6037 — address-of, not dereference) (callee NOT analyzed)
- 007B609F `mov eax, esi` mov eax,esi - ctor returns this

Check: FUN_007B6000 (the block ctor, not a vtable method) is NOT an entry of
vtable 0x00A8CCF4 (verified in RTTI raw: no slot value equals 0x007B6000).

## P2. writer 0x0050A2D1 (SF dtor body FUN_0050A240): [SF+0x30] = 0

Receiver proof: 0x0050A263 `mov esi,ecx` (thiscall SF-this); 0x0050A269
`mov dword ptr [esi],0xa7d458` (SF vtable store at [this+0]); the function is
the dtor body called from vtable slot 0 (FUN_0050A460). Hence [esi+0x30] ==
SF+0x30.

| hop | VA | bytes | instruction | evidence |
|---|---|---|---|---|
| 0050A2BD | 8b4e30 | `mov ecx, dword ptr [esi + 0x30]` | load link = [SF+0x30] |
| 0050A2C0 | 3bcb | `cmp ecx, ebx` | null test |
| 0050A2C4 | 834104ff | `add dword ptr [ecx + 4], -1` | refcount-- at link+4 |
| 0050A2C8 | 7507 | `jne 0x50a2d1` | if nonzero, keep link |
| 0050A2CA | 8b01 | `mov eax, dword ptr [ecx]` | if zero: vtable = [link] |
| 0050A2CC | 8b5004 | `mov edx, dword ptr [eax + 4]` | deleter = vtable slot 1 |
| 0050A2CF | ffd2 | `call edx` | dispatch deleter (destroy link) |
| 0050A2D1 | 895e30 | `mov dword ptr [esi + 0x30], ebx` | WRITE: SF+0x30 = 0 (ebx) |
| 0050A2D4 | 8b4e30 | `mov ecx, dword ptr [esi + 0x30]` | re-read of the now-null field (defensive duplicate) |

Source chain (creation/receipt level): the written value is the constant 0 in
ebx (`xor ebx,ebx` at 0x0050A272); the write happens after the refcount release
protocol. STOP.

SOURCE_PROVENANCE per PROVEN writer: P1 = RESOLVED (allocation->ctor->stored);
P2 = RESOLVED (constant zero after release protocol).
