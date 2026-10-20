# PREMISES_AND_COUNTERMODELS

## Labeled premises (standing, not facts)
1. Callee-cleanup conventions: 0096CD10 RET4, 0096D7C0 RET8, 0085CDE0 RET8, 0085C280 RET4, 0085BFA0 cleans its 1 out-arg (observed: no ADD ESP after calls; ESP balance collapses otherwise). 0085B1B0 RET 0xC now CONFIRMED from raw bytes.
2. 0096CD10 WRITE-BEHAVIOR of its out-trios is OPAQUE; L2 = v + S1*(u-v) content is CONDITIONAL on it (if no write, u=v=0 => w=0).
3. Float-return ST0 premises for 004B2A20, 00861220/00861320/00861240, 00734210; FPU-neutrality of opaque callees on the normal path.
4. Decompileer label provenance: "MovableObject::vftable" is an RTTI-derived decompiler symbol from a prior frozen run's saved decompilation; vtable VALUES (0xA91E4C, 0xA7DCB0) are confirmed from raw bytes in this run.
5. [receiver+0x30] content identity in P02 rests on the P01 caller dataflow write (one VISIBLE writer; earlier writers unknown — alias/lifetime to the 0085C130 read not proven).
6. 007105F0 ECX receiver premise (ECX-clobber assumption); no load-bearing claim depends on it.
7. Region-window function boundaries in P03/P06/P09 are RET-navigated candidates, not full CFG proofs.

## Countermodeled / rejected overclaims (this run)
1. "0085BFA0 receiver is SceneFeeder" — REJECTED as unproved (profile-only; no vptr/RTTI for the receiver in admitted corpus).
2. "ctor writes receiver +0x2C" — REJECTED: the only +0x2C writes found are bit0 flags on [owner+0xC0] (different object) and construction zero-stores; the data-address writer remains UNKNOWN.
3. "out-trio slots non-contiguous (+0x20 with +0x24 skipped)" — REJECTED by QC F1 (push-shift error); corrected to continuous +0x24/+0x28/+0x2C.
4. "0085B0A0 family all dispatched on [owner+0xC]" — REJECTED by QC F2; split receiver sets.
5. "whole-range remove-zero / first-chronological-use / 004D1430-constructor" — NOT REVIVED (standing corrections from prior postaudit; unchanged here).
6. "child local NIF transform = historical placement" — NOT ASSERTED; no placement claim made anywhere in this run.

## Distinctions kept
- model resource identity UNKNOWN; receiver identity UNKNOWN (class), CONFIRMED (mechanics);
- node/resource root vs world instance root: NOT_ESTABLISHED;
- NIF-local transform vs placement transform: no historical placement claimed;
- static class proof (owner class) vs runtime selection premise (which instance) kept separate;
- values (none recovered) vs historical 9.3.5 positions: NONE claimed.
