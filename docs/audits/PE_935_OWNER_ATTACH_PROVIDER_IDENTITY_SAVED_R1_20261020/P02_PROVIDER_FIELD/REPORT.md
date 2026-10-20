# P02 PROVIDER FIELD — store+2C @ 0085BE70, region [0085BD80,0085BEE0)

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P02_PROVIDER_FIELD)
Source: P02_EXTRACT.txt, admission A48f4c758c48c, 125 listing rows. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts executed.
AUTHORSHIP: PARENT_DIRECT_FALLBACK (both worker attempts stalled empty; see RUN_STARTED.json).

## 1. Question

Per contract §7: qualify the navigational store+2C candidate at 0085BE70 — function entry, this-adjustment,
constructor-or-update, stored value provenance, and whether it concerns R of 0085BFA0, its member,
provider P (=M32[R+0x2C]), or another object.

## 2. Function frame (entry 0085BD80)

- ABI: thiscall-style — EDI := ECX at 0085BD9D (**no this-adjustment**; receiver register copied unmodified),
  one stack arg ARG1 = ESI (loaded at 0085BD94 from [ESP+0x28] pre-push base), epilogue POP EDI/ESI/EBP/EBX,
  ADD ESP,0x18, **RET 0x4**. Frame: SUB ESP,0x18 + 4 saved regs. ESP balanced on both exit paths seen
  (0085BEDB RET / 0085BEDE FLDZ tail beyond window end at 0085BEE0).
- Symbols: **OBJ** = EDI = this (ECX at entry). **RD** = ESI = ARG1, a stream-reader-like object:
  [RD]=buffer base, [RD+0x8]=size/limit, [RD+0xC]=position, byte [RD+0x11]=active flag; helper 0040DE60
  (ECX=RD, arg 1 or 4) advances the position — reader semantics supported, not proven class identity.

## 3. Verdict on the candidate store+2C @ 0085BE70

- Effective destination: **ECX-relative field store into this-object: MOV [EDI+0x2C],ECX-reg** where
  the stored value comes from **global memory [0x00BA9220]**. It is part of a contiguous 3-dword copy:
  [EDI+0x28] := [0x00BA921C] (0085BE67), **[EDI+0x2C] := [0x00BA9220] (0085BE70)**,
  [EDI+0x30] := [0x00BA9224] (0085BE79). No vptr is written anywhere in this body; this is **not**
  a constructor-with-vtable and the stored value is **not** a call result, not a provider object pointer
  from a factory, and not stream data — it is a **static 3-dword global constant** (float-like trio
  layout: three consecutive dwords from three consecutive global addresses).
- It executes only on the path where the reader flag byte BL (stream-derived, with bit tests 0x20/0x40/
  sign/0x10 at 0085BE13-0085BE3C) has **bit 0x10 clear** (JZ 0085BE62). On the bit-0x10-set path the
  same trio region is written via CALL 0085BC10 (ECX=EDI+0x28, stack args: pointer to local float
  from [0x00A7B128]-derived local, ESI=RD) — an alternative update from the reader path.
- Value provenance chain (bit-0x10-clear path): global 0x00BA921C..0x00BA9224 → registers → fields
  +0x28/+0x2C/+0x30 of OBJ. One load level, no aliasing in-window, no call between load and store.
- The function is structurally a **stream-deserialization / update method**: bits of the reader flag byte
  conditionally negate (FCHS) fields +0x1C (via EBP=EDI+0x1C), +0x20, +0x24; +0x38 and +0x3C receive
  floats read from the RD buffer (0085BE90-0085BE99, 0085BEB8-0085BECC); byte [RD+0x11] is cleared at
  end. Fields +0x1C/+0x20/+0x24 behave as float components; +0x28/+0x2C/+0x30 as a 3-float trio.

## 4. Relation to B / R / P

- **NOT_ESTABLISHED that OBJ == R** (R = M32[B+0xC], receiver of 0085BFA0). No caller census of
  0085BD80 is in evidence; address adjacency with 0085BFA0 is not a join. OBJ and R remain separate values.
- **Material layout observation (conditional, not an identity claim)**: in this body +0x2C is written
  as the middle dword of a 3-dword float-like constant copy. If OBJ were R, then M32[R+0x2C] (read as
  provider pointer P in 0085BFA0 @0085BFA6, frozen prior R2 P04) would on this path be a float-cast
  value, not an object pointer — a structural tension, NOT a proof of inequality (different object, or
  different lifetime stage, remain open). Both facts stand separately; no pointer-equality or
  inequality is claimed.
- No edge in this window writes or reads any vtable slot; SLOT24/SLOT28 untouched here.

## 5. Countermodels examined

- REJECTED for this body: "store+2C writes provider pointer P" (value is a global constant dword).
- REJECTED: "0085BD80 is a constructor writing R+0x2C" (no vptr store; update/deserialization shape).
- REJECTED: OBJ == R by address adjacency or similar region (no join evidence).
- PRESERVED as open: OBJ == R from a later caller join; 0085BC10 path writing the trio from reader data.

## 6. Next concrete edges (frontier)

1. Caller census of 0085BD80 (who constructs/updates OBJ) — binds OBJ to B/R chain or rejects.
2. Body of 0085BC10 (bit-0x10 path writer of the +0x28/+0x2C/+0x30 trio) and 0085BD20 (used 3x on
   EAX of 00864360) — both small, both directly downstream of the candidate store.
3. 00864360 (reads/writes locals + &OBJ+0x24/&OBJ+0x20/ARG stack) — producer of the +0x20/+0x24 floats.

Budget (this package): 4 body / 4 candidate reservations charged at P02 admission; 125 rows; 8 CALL
sites visible (00864360, 0085BD20 x3, 0040DE60 x2, 0085BC10 — 0085BD20 counted once per unique VA:
00864360, 0085BD20, 0040DE60, 0085BC10 = 4 unique); 0 incident debits.
