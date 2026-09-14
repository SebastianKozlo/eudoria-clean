# SF30_WRITER_CENSUS supersession (AMEND_R2) — census row 0x0040525B

RUN: PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 · Era: PCG_9_3_5 · MODE: STATIC-ONLY
(the client NEVER ran; no process of any game binary was launched; byte-reading
scripts only). RUN_CLASS: MATERIAL (post-audit amendment). BRANCH: **(b)** — the F1-P
proof FAILED its address-taker closure predicate, so the row's CANONICAL
classification changes REJECTED_ALIAS -> POSSIBLE_ALIAS (see 06_REPORT/AMEND_LOG_R2.md
§1). This sidecar is an ANNOTATION of the historical census artifacts — it does not
modify them.

## The superseded row (CSV row 18, quoted verbatim from 02_ANALYSIS/SF30_WRITER_CENSUS.csv)

`0x0040525B,0x00405150,"mov dword ptr [edx + 0x30], ebx",ebx,static data address,REJECTED_ALIAS`

## The superseded raw why-line (01_RAW/SF30_WRITER_RAW.txt line 320, verbatim)

`    why: R-IMM-STATIC: base==edx = fixed immediate address (edx, dword ptr [0xb6c3d8] @ 00405250); SF proven always-heap (both creation paths operator new; no static/placement creation exists)`

## Canonical supersession statement (BRANCH (b))

The historical rejection reason R-IMM-STATIC ("base==edx = fixed immediate address") is
SUPERSEDED. The base register edx holds the VALUE loaded from the global pointer slot
0x00B6C3D8 (`mov edx, dword ptr [0xb6c3d8]` @0x00405250, bytes 8B 15 D8 C3 B6 00; no
edx definition in the open interval (0x00405250, 0x0040525B) — the only intervening
instruction is `push 0x404c30` @0x00405256; proven in
01_RAW/F1_GLOBALPTR_PROOF_RAW.txt of this amendment run).

The amendment attempted the corrected rejection R-GLOBAL-PTR-NON-SF ("the global's
value space excludes any heap-only SceneFeederObject pointer") and PROVED, from
physical bytes:

- **the direct-write channel closed**: a full-.text census of absolute [0x00B6C3D8]
  operands found 179 occurrences — 178 READs + EXACTLY ONE WRITE @0x00404C9D
  (`mov dword ptr [0xb6c3d8], eax`, bytes A3 D8 C3 B6 00), storing FUN_00409080's
  return value;
- **the value chain**: the return value == FUN_00409080's `this` == 0x00B9FEC0 (entry
  `mov ecx, 0xb9fec0` @0x00404C86 immediately before the sole `call 0x00409080`
  @0x00404C8B; inside FUN_00409080 the last eax definition is `mov eax, esi`
  @0x00409142 — esi captured once from ecx @0x004090A5 (8B F1) and not redefined
  before the eax capture — followed only by epilogue and `ret 4` @0x00409155;
  no vtable store into [esi]/[esi+0] exists in the body: non-polymorphic);
  0x00B9FEC0 is a static .data address whose at-rest image [0x00B9FEC0..0x00B9FF20]
  is all zero, and [0x00B6C3D8] at rest is 0x00000000;
- **the sole address-taker** of 0x00B6C3D8 in .text is `push 0xb6c3d8` @0x00404C90,
  whose consumer is FUN_00404B60 (the arg verified at [esp+0x20] by the measured
  stack arithmetic 4 + 0 + 28 == 0x20);
- **SF is always-heap** (both creation paths operator new(0x98): `push 0x98`
  @0x005247E7 + the operator-new thunk call @0x005247EC in the FUN_005247C0 window;
  SF ctor E8 callers exactly {0x0047D043, 0x0052480F}).

BUT the **address-taker channel is OPEN**: FUN_00404B60 stores the arg pointer — i.e.
&global — into a linked list (`mov dword ptr [ecx], edx` @0x00404BE9, bytes 89 11,
with edx == &global — no edx redefinition between the arg load `mov edx, dword ptr
[esp + 0x20]` @0x00404BC5 and the store), while its other arg uses are read [arg+8]
(`cmp esi, dword ptr [edx + 8]` @0x404BD3) and write [arg+0xc] (`mov dword ptr
[edx + 0xc], eax` @0x404BE6) only. The pointer to the global slot therefore escapes
into a list structure, and a write through that list-derived pointer (some other code
writing the node's +0 field — the +0 field IS the global slot) is NOT excludable
within this amendment's static decode bounds. The value space {0x00000000,
0x00B9FEC0} is therefore proven ONLY for the direct channel; the indirect channel
remains unbounded. A REJECTED row's reason must be structurally self-contained
(AMEND_LOG_R2 erratum E-2); the row is therefore reclassified
**REJECTED_ALIAS -> POSSIBLE_ALIAS** (canonical; BRANCH (b) of the amendment contract).
The corrected label R-GLOBAL-PTR-NON-SF does NOT stand — it would rest on the
unverified assumption that no list-derived write ever reaches the global slot.

## Historical artifact status (byte-identical; NOT regenerated)

- 02_ANALYSIS/SF30_WRITER_CENSUS.csv — SHA256
  71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0 (re-hashed and
  asserted by this amendment BEFORE this sidecar was written; the file was not
  modified by this amendment).
- 01_RAW/SF30_WRITER_RAW.txt — SHA256
  64402A73013B52943E10AE17BB115F466A0D3BEF98AA3835915CF3C1CD572248 (re-hashed and
  asserted; the file was not modified by this amendment).

Both are HISTORICAL artifacts of the accepted run
PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (publication state, amendment R1).
REGENERATION PROHIBITION: they must NOT be regenerated without a determinism proof;
the canonical superseded state is carried by this sidecar and by
06_REPORT/AMEND_LOG_R2.md.

## Counts

- Historical (the unchanged CSV rows, recomputed by this amendment's proof script,
  P9 PASS): 3643 = 2 PROVEN_SF30_WRITER / 618 POSSIBLE_ALIAS / 3023 REJECTED_ALIAS /
  0 UNRESOLVED.
- **CANONICAL** (after this amendment, BRANCH (b)): 3643 = 2 PROVEN_SF30_WRITER /
  **619 POSSIBLE_ALIAS** / **3022 REJECTED_ALIAS** / 0 UNRESOLVED — exactly one row
  (0x0040525B) moves REJECTED -> POSSIBLE; every other row's classification is
  unchanged.
- The historical fired-reason census (recomputed from the unchanged raw why-lines)
  remains: R-ESP 2765 / R-STACK-PTR 129 / R-CTOR-OTHER 104 / R-ZERO 18 / R-LEA-STACK 3
  / R-EBP-INHERITED 2 / R-IMM-STATIC 1 / R-CONT-FIELD 1 = 3023 REJECTED (historical);
  canonically the single R-IMM-STATIC row is no longer REJECTED: 3022.
