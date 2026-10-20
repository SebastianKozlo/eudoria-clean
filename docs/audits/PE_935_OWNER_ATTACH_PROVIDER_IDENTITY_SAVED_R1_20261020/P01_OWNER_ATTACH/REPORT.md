# P01 OWNER ATTACH — store+C @ 0085ACE9, region [0085ACD0,0085AD10)

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P01_OWNER_ATTACH)
Source: P01_EXTRACT.txt, admission A954d84cd8720, 26 listing rows. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts executed.

## 1. Question

Per contract §6: qualify the navigational store+C candidate at 0085ACE9 — actual destination
(ESP-relative vs ECX-relative, PUSH effects), stored value, ABI, and whether it is a B→R
attach or a stack local.

## 2. Function frame (entry 0085ACD0)

- `SUB ESP,0x8` reserves an 8-byte local frame (L0 at ESP0-8, L1 at ESP0-4).
- `PUSH ESI` (0085ACDD) → ESP = ESP0-0xC.
- `MOV ESI,[ESP+0x10]` (0085ACDE) → `[ESP0-0xC+0x10] = [ESP0+4]` = the single stack argument. `RET 0x4` (0085AD0F) confirms exactly one dword argument. ESI = ARG1.
- ECX at entry is the receiver (`this`-style): all field reads are ECX-relative (+0x44, +0x5c, +0x74, +0x78, +0x88).
- `CMP [ECX+0x88],0` + `JNZ 0085AD12` (0085ACDB/0085ACE2): the zeroing + call block executes only when `[ECX+0x88] == 0` (lazy/guarded path). The fall-through at 0085AD12 is outside this window.

## 3. The store at 0085ACE9 — destination and value

EDX = 0 (`XOR EDX,EDX` 0085ACD9; no redefinition until 0085ACF2).

PUSH state at the store: after `SUB ESP,8` and `PUSH ESI`, ESP = ESP0-0xC; `PUSH EDX` at 0085ACE4 makes ESP = ESP0-0x10. Therefore at 0085ACE5/0085ACE9:

- `MOV [ESP+0x8],EDX` → `[ESP0-0x10+8] = [ESP0-8]` = **L0** = 0
- `MOV [ESP+0xC],EDX` (0085ACE9) → `[ESP0-0x10+0xC] = [ESP0-4]` = **L1** = 0

**Conclusion: 0085ACE9 stores ZERO to stack local L1 (ESP-relative), the high dword of the 8-byte
local pair [ESP0-8, ESP0-4].** It is NOT ECX-relative, NOT an object field, NOT a return-address
slot (the push accounting is explicit and balanced), and NOT a B→R attach.

`LEA EAX,[ESP+0x8]` (0085ACED) takes &L0; the 8-byte zeroed pair is passed **by address** as an
argument to CALL 00730F00 — i.e. an out-buffer / caller-supplied local, not heap/obj storage.

## 4. CALL 00730F00 — ABI (from caller side only; callee body not opened)

Pushes after `PUSH ESI`, in order (deepest = last arg):

| push VA | value | becomes |
|---|---|---|
| 0085ACE4 | 0 (EDX) | arg6 = 0 |
| 0085ACF1 | &L0 (out buffer) | arg5 |
| 0085ACF5 | ECX+0x5c (embedded address) | arg4 |
| 0085ACFC | ECX+0x44 (embedded address) | arg3 |
| 0085AD00 | [ECX+0x78] (field value) | arg2 |
| 0085AD01 | [ECX+0x74] (field value) | arg1 |

`MOV ECX,ESI` (0085AD02) sets ECX = ARG1 = the callee's thiscall receiver. At CALL, ESP = ESP0-0x24.
Post-call the caller performs no `ADD ESP,0x18`; the epilogue (`POP ESI; ADD ESP,8; RET 0x4`) balances
only if the callee cleans its 6 dword args → **caller expects stdcall-like RET 0x18 in 00730F00**
(inferred from caller ESP balance; callee body unopened). Return of this function: `MOV EAX,ESI`
(0085AD09) — the function returns its own ARG1 (the receiver object passed in).

## 5. Answer to the contract questions

- Actual destination of 0085ACE9: **stack local L1 at ESP0-4, ESP-relative after one PUSH; not ECX-relative.**
- Stored value: **0 (zero-init), not a pointer, not a field value, not a copy member.**
- ABI of 0085ACD0: thiscall-entry (ECX receiver), 1 stack arg, `RET 0x4`; callee 00730F00 invoked
  thiscall with ECX=ARG1 and 6 stack args incl. the zeroed 8-byte out-buffer.
- B→R attach at 0085ACE9? **NO. It is a stack-local zeroing.** No B+field, R, P, VT, F or T symbol
  appears in this window; B and R (per contract §3 bindings) are not touched by this body.

## 6. Candidate verdict

The navigational store+C candidate at 0085ACE9 is **rejected for this body** (negative result,
scoped to this body only — not a claim that no B→R attach writer exists). The next concrete source
pointer per contract §6/§7 should be the Stage B candidate store+2C @ 0085BE70
(region [0085BD80,0085BEE0), REQUEST_PROVIDER_FIELD), which is a store inside an object, unlike
this stack local.

## 7. Budget ledger (this package)

- Body reservations: 1 (this region) / candidate reservations: 1 (store+C @ ACE9) — both consumed.
- Listing rows: 26 (charged = given extract). CALL charges: 1 (CALL 00730F00, listing-only,
  callee body NOT opened). Document lines: this package.
- Union: 1 body owner (0085ACD0), 1 CALL VA (00730F00).

## 8. Premises / countermodels tested

- CM1 "store hits the return-address slot": refuted — explicit push sequence gives [ESP+0xC]=ESP0-4
  (local), not ESP0.
- CM2 "stored value is a pointer/field": refuted — EDX=0 from XOR at 0085ACD9, no intervening write.
- CM3 "store is B+C or R+field": refuted — destination is ESP-relative; ECX-relative accesses in
  this body are reads/LEA only (+0x44/+0x5c/+0x74/+0x78/+0x88); no memory write targets [ECX+...].
- CM4 "callee is cdecl": caller-side ESP balance contradicts it; callee body unopened → status
  STRONGLY_SUPPORTED, not CONFIRMED.
- Not tested (out of scope): whether ARG1 (ESI) equals B, R, or any other instance — requires
  caller provenance (00527AB0 thread), not available in this window.
