# J01b EXECUTOR SEMANTICS — DAT_A / DAT_B submit-path executors (static, 2003 PE binary)

RUN_ID=PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 | JOB=J01b | lineage=J01-split-b
Binary: PE2_unpacked_out.exe SHA256 56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650. All bytes below read from the file with an independent python decoder and cross-checked against Ghidra 11.2.1 (own project J01bProj).

## DAT_A = FUN_005c27a0 — EMPTY NO-OP
- Raw bytes @0x5c27a0: `c3` (RET) followed by NOP padding. The function does literally nothing.
- Called at 0x506b1e `ff 15 44 e8 61 00` as FUN_005c27a0(record_buffer_0x14, 2) from FUN_005068f0 — a semantically inert call.
- Also passed as the element-destructor argument to the typed-array builder FUN_0053955a (pushed `68 a0 27 5c 00` at 0x506a70 and 0x506baa) — i.e. "records have trivial destructor".
- Installed in TWO table slots: T1[5]=0x61E840 via FUN_005543b0(1,0) and DAT_A=T1[6]=0x61E844 via FUN_00561a30(1,1) (J01a canon).
- 1193 static references from ~1100 distinct functions (Ghidra REF census): a default do-nothing callback shared image-wide. As COMMON as a function can be.

## DAT_B = FUN_00561ee0 — pure forwarder to FUN_005541e0 (quaternion record normalizer)
- Raw bytes @0x561ee0: `8b 44 24 08  8b 4c 24 04  50 51  e8 f1 22 ff ff  83` = MOV EAX,[ESP+8]; MOV ECX,[ESP+4]; PUSH EAX; PUSH ECX; CALL FUN_005541e0 — 13-byte argument-preserving thunk.
- Called at 0x506c58 `ff 15 58 e8 61 00` as FUN_00561ee0(record_buffer_0x18, 2) from FUN_005068f0.
- FUN_005541e0(buf, count) operates in-place on the 0x18-byte records ({target, 0x18, quat[4] at +8..+0x14}):
  1. **Pass 1 (adjacent pairs):** dot = q[i]·q[i+1] (4-float dot product); if dot < 0.0f (const @0x5e2cf4 = 0.0) → all 4 components of q[i+1] are replaced by their negation via FUN_00544720 (`-q`). This is the classic **shortest-path quaternion sign flip**.
  2. **Pass 2:** record+8 (first quat component) is clamped into [-1.0f (0x5e2cf0), +1.0f (0x5e2b24)], writing 0xbf800000 / 0x3f800000 on out-of-range.
- Sharing census (REF): FUN_005541e0 is ALSO installed in table slot T1[0] by installer FUN_00553f00 (DATA ref 0x553f38) and called directly by FUN_0055ddf0 (@0x555de0a), FUN_00561ee0 (@0x561eea), FUN_00568630 (@0x568642). FUN_00561ee0 has an additional direct caller @0x56211e in an unnamed sibling 0x18-record producer region (0x562040–0x56212f, no Ghidra function object — found by REF scan + raw disasm, honoring NO_DIRECT_XREF ≠ dead code).

## Mechanism (producer → normalizer → consumer)
- Producer: FUN_005068f0 builds the 2-record arrays; record[0] target dwords are bit-exact copies of owner+0x6C / owner+0x70 (FLD/FSTP d9 40 6c / d9 40 70), payload x,y,z from node+0x50/0x54/0x58, quat from node+0x2C; emission gated by owner+0x74 byte and component flags (FUN_005120b0/e0/110).
- Executor: DAT_A inert; DAT_B normalizes the quaternion records in place (the 0x14 position records need no normalization).
- Consumer: FUN_00555470 (0x14 path) / FUN_005553f0 (0x18 path), thiscall this = the 0x50-byte channel-holder; lazily create the channel object at this+0x44 (FUN_00554bb0), store the buffer (FUN_00554c80/FUN_00554c50), clear this+0x3C/+0x38; then FUN_00556d70 registers a channel id by name on the 0xFC transform-stream object and FUN_00556ea0 stores the channel-holder at that id; FUN_00506e10 finalizes the stream. Downstream drain remains R1's T3-d2 OPEN edge (not followed; static scope ends here).

## COMMON vs PER-MODEL: **COMMON**
- No model/def id (4508/4057/296445/218757) occurs in any of the 8 chain regions (byte-scanned); 296445/218757/4057 have ZERO file-wide LE32 occurrences; 4508 occurs exactly once file-wide (VA 0x5bcfe5, outside the chain).
- The chain carries per-INSTANCE identity (pair id at +8, node pointer), never per-MODEL ids.
- Executor sharing census above. No common class was promoted by offset similarity; vtable identities used: pair 0x5E7534, instance P 0x5E799C, X 0x5EBC1C.
