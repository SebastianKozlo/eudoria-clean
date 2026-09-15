# QC_AUDIT.md — G13 FRESH-CONTEXT INDEPENDENT QC — PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915

- QC session: fresh independent pe-master-auditor session (did NOT formalize or execute the run)
- Date: 2026-09-15 | Mode: INTERNAL_QC (G13) | STATIC-ONLY (binary never executed)
- Target re-measured fail-closed by the QC itself: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
  SIZE=8015872 (own measurement == pin), SHA256=E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  (own measurement == pin), PE32 i386 (machine 0x014C, opt-magic 0x010B, ImageBase 0x00400000 — own PE parse),
  5 sections (own header parse matches SOURCE_IDENTITIES.json exactly).
- Environment: `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (3.12.7) + capstone 5.0.7 (verified live).
- QC tooling: the QC's own scripts live OUTSIDE the package
  (`C:\Users\User\AppData\Local\Temp\opencode\pe_qc_holder_r1\`, files qc1..qc8; AUDITOR COUNTERCHECK,
  NOT project evidence). Every load-bearing re-derivation below was made from the pinned bytes with the
  QC's own decoders/censuses; the run's generators were NOT trusted for any load-bearing item.
- Git: ZERO mutations by the QC session. Read-only observations: HEAD == origin/master ==
  895bbc8baa2d002c562b7e5b43212e38c2abb16f (== contract BASE_SHA, unchanged since the run's end
  observation); untracked set = {NINODE_SLOT17 dir (pre-existing), this run dir, experiments/} — matches
  AT_RUN_END_GIT_OBSERVATION.md exactly. The only file written inside the package by this QC session is
  this QC_AUDIT.md (it is intentionally NOT added to MANIFEST_SHA256.csv, which the QC session must not
  mutate).

## QC VERDICT: **QC_FAIL**

One P0 load-bearing defect: the run's primary answer — "[ArkAnimation-family +0x14] is NULL at every
statically-bounded construction; no writer binds ANY object" — is **falsified by the bytes**: at all
eight param-chained factory call sites (+ one additional alias chain), the `xor esi,esi` that the run's
slices read as the universal held-value source sits on a *conditional error path*, and the *normal*
path bypasses it via an incoming `jmp <block_start>+2` after constructing a child-animation object.
On those paths the base ctor binds a **non-NULL, RTTI-identified child object** into [this+0x14].
Everything else the run measured — the thunk decode, the five-class membership, the census arithmetic,
the four-channel caller census, the negative controls, the package hygiene — was independently
re-derived by this QC and is **correct**. The defect is confined to the Phase C(iv)/(v) value-chain
slices and every conclusion built on them (HELD_OBJECT_IDENTITY, the recorded H2/H3 bases,
TOP_NEW_DISCOVERY "unexercised stub layer", SUCCESS B's stated mechanism).

## 1. Claim-by-claim verdict (EVIDENCE_INDEX C1..C16, each re-derived by the QC from bytes)

| claim | run status | QC verdict | QC evidence (own) |
|---|---|---|---|
| C1 EXE identity == pins | CONFIRMED | **CONFIRMED** | own size/SHA256/PE-header re-measure (QC-1) |
| C2 FUN_006FAB80 = slot-3 forwarder, 10/10 checks | CONFIRMED | **CONFIRMED** | own decode 0x006FAB80..0x006FAB97 + 6x CC pad + ret 8; all 10 pin byte-rows match (QC-2) |
| C3 arg1 x87 roundtrip; pointer-vs-float ambiguity | CONFIRMED | **CONFIRMED** (measurement CONFIRMED; bit-preservation classes are analytic and remain so labeled) | own decode `fld [esp+4]`/`fstp [esp]` (QC-2) |
| C4 exactly 5 classes contain the thunk at slot 2 | CONFIRMED | **CONFIRMED** | own imm32 census: exactly 5 whole-file occurrences, all 5 at the claimed slot dwords (QC-5/6); own vtable extent walk: 8/8/9/9/9 slots, slot2==thunk in all five, stop dwords 0xAA7804/0xAA7934/0x40C90FDB/0x3727C5AC/0xAA7C28 (QC-33) |
| C5 shared base = Predefined; base ctor 0x006FABA0 | CONFIRMED | **CONFIRMED** | own COL/CHD/BCD walks (QC-30b: all 10 classes' lineages); own decode of ctor vtable store @0x006FABA8 |
| C6 family closure = 10 classes (Predefined lineage) | CONFIRMED | **CONFIRMED** | own lineage walk: exactly the 10 Predefined-derived classes; Scale/Intensity/Alpha/Color/Translation/Transform/Rotation/FloatValue derive from **ArkAnimationFloatValue** (separate root) (QC-30b) |
| C7 census denominator 10,711; 1898/8811/2/0; 0 attribution failures | CONFIRMED | **CONFIRMED** | own CSV recount: 10,711 rows; STACK_FRAME=8811, REG_INDIRECT=1898, SIB=2, no ABS/UNKNOWN (QC-36) |
| C8 exactly 3 family +0x14 writers, all values NULL | CONFIRMED | **PARTIALLY REJECTED** — "exactly 3 family writers" CONFIRMED (own recount + own family-function scan QC-39: only 0x006FABB5/0x006FAC25/0x006FAC75 write [reg+0x14] in family functions); "all values NULL" **FALSIFIED** (P0-1: the ctor's arg2 is non-NULL on bypass paths) |
| C9 ctor ABI: ret 0xC; held=arg2=[esp+0xC]; NULL-guarded refcount | CONFIRMED | **CONFIRMED** | own full decode 0x006FABA0..0x006FABF5: `89 48 14`, `BA 01 00 00 00`, `01 51 04`, `85 c9/74 03` guard, `ret 0xC` (QC-3) |
| C10 held param NULL at all 6 ctor sites | CONFIRMED | **FALSIFIED** (P0-1) | sites 1/2/3/5 (`push 0` @0x006FAFC0/0x006FB089/0x006FB402/0x006FE9E1 — own decode) CONFIRMED NULL; sites 4/6 param chains are **not** constant-NULL (P0-1) |
| C11 release path: refcount@held+4; held->vt[0](1); field zeroed | CONFIRMED | **CONFIRMED** | own decode of 0x006FAC00/0x006FAC50 (and 0x006FB740/0x006FD2E0 wrappers) |
| C12 no thunk caller (4 channels) | CONFIRMED | **CONFIRMED** | own raw-byte censuses: E8/E9/EB denominators 156,829/40,668/17,961 → 0 hits; imm32 = 5 (own slots only); own CSV recount 1,438 → 0 PROVEN / 5 REJECTED / 1,433 INSUFFICIENT (QC-6/37) |
| C13 SF infrastructure validated | CONFIRMED | **CONFIRMED** | own reads: SF vtable 6 slots [0x50A460/0x5090A0/0x5090B0/0x50A050/0x5090C0/0x509580], stop dword @0x00A7D470 = "dPVS" ASCII, COL → .?AVSceneFeederObject@@; own decode FUN_0050A050 chunk 2 [0x0050A087..0x0050A0AA) incl. `ret 8` @0x0050A0A7 and the slot-1 float3 out-copy; own decode of container 0x0044D5D8.. with 3 calls to 0x005247C0 (args 0xF0000000/1/2) storing at +0x0C/+0x10/+0x14 |
| C14 negative control: selectivity 1/803; PIN-NC anchors | CONFIRMED | **CONFIRMED** | own recount of the inventory: 1,393 COL-backed vtables, 803 valid slot-3, exactly 1 == 0x0050A050; own dword reads: 0x007AC2F0 @ slot 14 of vt 0x00A8C2EC (.?AVNiD3DPixelShader@@) and 0x00A8C59C (.?AVNiD3DHLSLPixelShader@@); 0x007F1D70 @ slot 1 of vt 0x00A90304 (.?AVNiBoundingVolume@@) (QC-42/46) |
| C15 arg2 provenance/value NOT_DEMONSTRATED; role UNVERIFIED | CONFIRMED | **CONFIRMED with one wording correction** — the statuses stand on the empty-thunk-caller-set basis (re-verified); but [E5]'s "no arg2 can ever reach a live receiver" is falsified by P0-1 (live receivers DO exist; the arg1/arg2 pointer-vs-float discriminator remains unresolvable only because the thunk has no proven caller) |
| C16 G1 git state clean; zero mutations | CONFIRMED | **CONFIRMED** (post-hoc) | QC's own read-only git observation: HEAD/origin == BASE_SHA; untracked set exact |

## 2. FINDING P0-1 (QC) — the NULL-everywhere headline is falsified by branch-bypass edges

**Severity: P0. The primary answer of the run is wrong in static reach.**

**Contradicted claims (exact locations):**
- REPORT.md §1 ("Every statically-reachable construction of the entire 10-class ArkAnimation family ...
  binds the held param (ctor arg2) to NULL"; "the binding edge does not exist"),
- REPORT.md §2 (HELD_OBJECT_IDENTITY: NULL CONFIRMED; TOP_NEW_DISCOVERY "unexercised stub layer"),
- REPORT.md §3 P0-1 and P1-5 ("All construct with held=NULL"),
- REPORT.md §0 H2 disposition text ("NO writer binds ANY object") and H3 disposition ("all values are
  constant NULL; the receiver set is empty"),
- REPORT.md §5 SUCCESS B text ("the receiver is not another class — it is NULL"),
- HANDOFF.md headline outcomes ("HELD_OBJECT_IDENTITY: NULL ... ladder terminates at LEVEL 0; no class
  ever bound"; "TOP_NEW_DISCOVERY: ... unexercised stub layer"),
- SCIENCE_STATUS_DELTA rows 6/7/13/15/16, RECEIVER_IDENTITY.md ladder table, HOLDER14_PROVENANCE.md
  §C(iv) RESULT ("the held param is NULL at EVERY statically-reachable construction site"),
  HOLDER14_WRITER_RAW.txt [IV-1..6] slice verdicts ("ZERO: xor esi,esi" for the Deriv/Cyclic chains).

**Physical counter-evidence (all byte addresses + bytes from the QC's own decode of the pinned EXE):**

The 0x006D1xxx–0x006D2xxx "factory sites" are blocks of ONE large name-dispatch construct (entry
function 0x006D0ED0, which the QC measured to have exactly 3 direct E8 callers: 0x0058EFD6, 0x0058F19F,
0x006D2B1C — i.e., family construction is statically reachable). Each factory block is a B.5
pseudo-function whose first instruction `xor esi,esi` is a **conditional error-path leaf**, not the
universal esi definition. Canonical chain (Derivatives factory A; every byte below decoded by the QC):

```
0x006D2042  6a0c             push 0xC                     ; CHILD allocation (ArkAnimationScale size 0xC)
0x006D2044  e87bb32800       call 0x95D3C4                ; ??2 operator new
0x006D2049  83c404           add esp, 4
0x006D204C  89442414         mov [esp+0x14], eax
0x006D2050  85c0             test eax, eax
0x006D2052  c68424c00000001f mov byte [esp+0xC0], 0x1F
0x006D205A  7410             je 0x6D206C                  ; alloc FAILED -> xor esi,esi (NULL held)
0x006D205C  8b4c241c         mov ecx, [esp+0x1C]
0x006D2060  51               push ecx
0x006D2061  8bc8             mov ecx, eax
0x006D2063  e8989c0200       call 0x6FBD00                ; alloc SUCCEEDED -> construct the CHILD
0x006D2068  8bf0             mov esi, eax                 ; esi = child object (ctor returns this)
0x006D206A  eb02             jmp 0x6D206E                  ; <-- BYPASSES the xor at 0x6D206C
0x006D206C  33f6             xor esi, esi                  ; (only the je/alloc-fail path executes this)
0x006D206E  6a6c             push 0x6C                     ; Derivatives allocation
...
0x006D20C7  56               push esi                      ; ARG2 of the Derivatives ctor call
...
0x006D20DA  e8b1940200       call 0x6FB590                 ; ArkAnimationDerivatives ctor(arg2 = esi)
```

`0x006FBD00` (QC's own decode) is a constructor: `mov esi,ecx; call 0x6FFEE0; mov [esi],0xA865E0;
mov eax,esi; ret 4` — it stores vtable 0x00A865E0 (QC's own RTTI walk: COL 0x00AA7A50 →
**.?AVArkAnimationScale@@**) and returns `this` in EAX, which on this path is a **non-NULL** fresh
allocation (the je at 0x006D205A already tested it). The chain then flows (QC-verified end-to-end,
including the QC's own frame arithmetic for the Derivatives ctor: `mov eax,[esp+0x28]` at esp-delta
0x1C ⇒ entry [esp+0xC] = its arg2; and the push-tail at the call: last-3 pushes = arg0/arg1/arg2 with
esi 3rd-from-top): factory esi → Deriv ctor arg2 → base ctor arg2 (`mov ecx,[esp+0xC]` @0x006FABA2) →
`mov [eax+0x14], ecx` @0x006FABB5. **[this+0x14] receives the ArkAnimationScale object.**

The QC byte-verified the same bypass shape (`je → block start` / `call <child_ctor>; mov esi,eax;
jmp <block start>+2`) at **all eight** param-chained factory blocks, plus one additional alias chain:

| block start | bypass child ctor | child class (own RTTI) | child vtable | child alloc | family ctor call fed (arg2) |
|---|---|---|---|---|---|
| 0x006D206C (Deriv-A) | 0x006FBD00 | .?AVArkAnimationScale@@ | 0x00A865E0 | 0x0C | 0x006D20DA → 0x6FB590 (Derivatives) |
| 0x006D228B (Deriv-B) | 0x006FC450 | .?AVArkAnimationColor@@ | 0x00A8661C | — | 0x006D22F7 → 0x6FB590 |
| 0x006D23EB (Deriv-C) | 0x006FBF90 | .?AVArkAnimationIntensity@@ | 0x00A86608 | — | 0x006D2457 → 0x6FB590 |
| 0x006D16DB (Sin-1) | 0x006FD420 | .?AVArkAnimationTranslation@@ | 0x00A86678 | — | 0x006D1736 → 0x6FD270 (CyclicSin) |
| 0x006D17C8 (Sin-2) | 0x006FCD00 | .?AVArkAnimationAlpha@@ | 0x00A8663C | — | 0x006D1828 → 0x6FD270 |
| 0x006D1A93 (Sin-3) | 0x006FBF90 | .?AVArkAnimationIntensity@@ | 0x00A86608 | — | 0x006D1AF3 → 0x6FD270 |
| 0x006D1C58 (Sin-4) | 0x006FBD00 | .?AVArkAnimationScale@@ | 0x00A865E0 | — | 0x006D1CB3 → 0x6FD270 |
| 0x006D1D60 (Linear) | 0x006FD420 | .?AVArkAnimationTranslation@@ | 0x00A86678 | 0x24 | 0x006D1DC6 → 0x6FBAB0 (CyclicLinear) |
| 0x006D1FB1/0x006D1FB3 (alias into Deriv-C's shared tail via `jmp 0x6D2441`) | 0x006FD420 | .?AVArkAnimationTranslation@@ | 0x00A86678 | 0x24 | 0x006D2457 → 0x6FB590 (shared tail) |

Every child ctor is a real constructor (each stores its class vtable — QC-decoded) and four of the
five were byte-verified to return `this` (`mov eax,esi`-shape: 0x006FBD13 Scale, 0x006FC03A Intensity,
0x006FC6CD Color, 0x006FD4F4 Translation — non-NULL on the path that reaches them, because the
allocation was just tested non-NULL). For the fifth (Alpha, ctor 0x006FCD00 — a multi-chunk function;
see the run's own P2-3) the QC verified the bypass edge and the vtable store but did not individually
re-derive its return instruction; the P0 does not depend on it — the falsified claim is that esi is
**constant zero** (it is `ret(0x006FCD00)`, a value the run never traced), not that it is any
particular pointer. The QC verified with its own clobber scans that ESI has **no**
redefinition between each block entry and the `push esi`, so the child pointer arrives intact at the
ctor call. Sin/Cyclic chains inherit the same values (the Cyclic ctor is called only by the
Linear/Sin ctors — QC's own E8 census — which forward their own arg2; QC-verified at the Linear
0x006FBAB8 (`mov edx,[esp+0xC]` at entry) and Sin 0x006FD278 sites).

**Resulting corrected value table (within static reach):**
- TimeController, NodeUpdate, AnimatedTexture, ParticleSystemPredefined, ParticleSystemPredefinedMod:
  held = **NULL always** (their ctors pass immediate `push 0` to the base ctor — QC-verified bytes
  0x006FAFC0/0x006FB089/0x006FB402/0x006FE9E1; PSPMod chains via the PSP ctor's `push 0`).
- ArkAnimationDerivatives, ArkAnimationCyclicLinear, ArkAnimationCyclicSin, ArkAnimationCyclic:
  held = **NULL on the allocation-failure paths**, and = **a live child-animation object**
  (Scale/Intensity/Alpha/Color/Translation — RTTI-identified, vtable-stored, refcount-compatible
  layout: the dtor's `refcount@held+4` and `held->vt[0](1)` release protocol is consistent with these
  children being genuinely held) on the normal (name-match + alloc-success) paths.

The child classes belong to a separate hierarchy root (QC's own lineage walk):
ArkAnimationFloatValue ← {Transform ← (Scale, Rotation, Translation); Color ← Intensity; Alpha} —
none of them derives from ArkAnimationPredefined, so the run's 10-class family closure (P1-5 scope
part) remains CORRECT; the correction concerns the FIELD's value, not the family's definition.

**Why the run missed it (mechanism):** Phase C(iv)'s clobber-aware slice walked back from `push esi`
within the B.5 pseudo-function [0x006D206C..0x006D20E4), found `xor esi,esi` at the pseudo-function's
first instruction, and — because the pseudo-function has no E8 callers (its entries are a `je` to the
start and a `jmp` to start+2 from the preceding block of the same construct) — terminated with
"ZERO at function start" without examining incoming branch edges. The B.5 tight-boundary map
dissected the dispatcher construct into pseudo-functions; the slice engine's function-entry assumption
(registers fresh at entry; caller-cross = E8 callers) is invalid for branch-target pseudo-entries.
The declared bound (4 levels x 384 B, multi-start, caller-cross) would have contained the bypass edges
(they lie 0x1E–0x2A bytes before the pseudo-function start), but the engine's edge model did not
include intra-construct je/jmp edges or skip-offset entries. AMEND_LOG A3/A4 fixed other slice defects
but not this one. The QC notes the run's census could never surface this either: all 40 census rows in
the dispatcher region are esp-based (STACK_FRAME, excluded) and the child pointers flow only through
registers.

**Blast radius (RUNS/CLAIMS/CODE):** confined to this run package (untracked, uncommitted; no prior
run depends on its outputs — it is R1 of this seam). Affected claims: REPORT §0 H2/H3 recorded bases,
§1 primary answer, §2 HELD_OBJECT_IDENTITY/TOP_NEW_DISCOVERY/TOP_OPEN_BLOCKER(i) premise, §3 P0-1 and
P1-5 value part, §5 SUCCESS B mechanism; HANDOFF.md headline outcome line "held param is NULL at ALL
6 ctor sites (4x immediate push 0; param chains to `xor esi,esi` at 8 factory sites)";
HOLDER14_PROVENANCE/RECEIVER_IDENTITY/ARG2_UPSTREAM_ANALYSIS disposition texts;
SCIENCE_STATUS_DELTA rows 6/7/13/15/16; HOLDER14_WRITER_RAW [IV-1..6] slice verdicts.
**Unaffected (QC-re-verified independently):** H1/FORWARDER_OPERATION (CONFIRMED stands), the
writer census counts and the 3-writer set, Phase D four-channel thunk-caller census (0 callers
stands — QC's own byte censuses agree exactly), five-class membership + P1-2 (0x00AA7958) — QC
re-derived: dword @0x00AA7958 = 0x00AA7964 (Cyclic CHD's pBCD field), no 0x006FAB80 dword anywhere in
0x00AA7930..0x00AA79A4 — P1-2 CONFIRMED, G7 negative control, census arithmetic, package hygiene,
G1 git discipline.

**Narrow correction (for pe-reconstruction; the QC does not implement it):**
1. Re-run the Phase C(iv)/(v) arg2 slices at the six base-ctor sites with incoming-branch-edge
   awareness: for every B.5 pseudo-function start, enumerate incoming je/jcc/E9/EB edges AND edges
   landing at start+N (N>0); for the dispatcher construct [0x006D0ED0..0x006D265F], either merge the
   pseudo-functions or run the slice over the full construct extent.
2. Re-derive the held-value disposition per the table above; identify each child ctor's class via its
   vtable store + RTTI (Scale/Color/Intensity/Alpha/Translation), and measure each child vtable's
   slot-ordinal-3 target (QC measurements to confirm: Scale/Translation slot-3 = 0x006FFF00;
   Intensity/Alpha/Color slot-3 = 0x9154A0 — none equals 0x0050A050).
3. Re-dispose the status algebra: HELD_OBJECT_IDENTITY = NOT-NULL-CHILD-OBJECT at bounded constructions
   of 4 classes (ladder L2 reachable: RTTI class family identified) + NULL for the other 6 classes and
   on the error paths; H2 outcome (REJECTED — not SceneFeeder) STANDS but via its own specified
   falsifier (writers bind OTHER RTTI classes, none SceneFeederObject, slot-3 ≠ 0x0050A050), no longer
   via "no writer binds any object"; H3 flips (receiver identity IS provable — CONFIRMED-shaped);
   SCENEFEEDER_LINK = REJECTED re-based; TOP_NEW_DISCOVERY = the held field is a live
   composite/child-animation binding mechanism (the Rosetta edge ArkAnimation → [this+0x14] exists;
   its receivers are FloatValue-hierarchy channel animations, so the SceneFeeder/NiNode-name-lookup
   edge remains falsified at the receiver-identity link — SUCCESS B proper, not "the binding edge
   does not exist"); the crash-consistency sentence must be retracted (a slot-2 dispatch on a live
   composite would NOT fault — it would forward to the child's slot-3).
4. Correct REPORT.md/HANDOFF.md/02_ANALYSIS texts accordingly; regenerate the defective slice sections
   of HOLDER14_WRITER_RAW.txt by the protocol (deterministic regeneration + AMEND_LOG entry; never
   hand-edit completed raws).
5. Re-examine whether the 1,433 INSUFFICIENT_PROOF dispatch candidates and the 68/814 residue rows
   need re-review under the corrected receiver-set reality (bounded: the family now has PROVABLE
   non-NULL held at bounded sites, which changes the "all family objects carry held=NULL so a dispatch
   would fault" rejection shortcut — the census numbers themselves stand).

**Revalidation predicate (post-correction):** from bytes, at each of the 9 chains above (plus any
newly discovered under the upgraded edge-aware bound): (a) both entry paths of every factory block are
enumerated (xor-path + bypass-path); (b) the per-class held-value table matches the QC's table;
(c) each child class's RTTI name, vtable VA and slot-3 dword are re-measured and != 0x0050A050;
(d) no package text claims universal NULL; (e) the H2/H3/HELD_OBJECT_IDENTITY/SCENEFEEDER_LINK/
TOP_NEW_DISCOVERY fields carry the corrected bases.

## 3. Other findings

**P2-1 (QC) — unqualified "no caller" wording (V2R-001/V2R-004 class).**
REPORT §2 TOP_NEW_DISCOVERY: "the slot-2 forwarder has no caller"; HANDOFF.md: "slot-2 forwarder has
no caller". The measured result is "0 PROVEN / 5 REJECTED / 1,433 INSUFFICIENT_PROOF / 0 direct E8-E9-EB
/ 5 imm32 (own slots)" — the correct bounded wording (used correctly elsewhere: REPORT §1, §2 census
outcome, P0-2 "zero statically-identifiable callers") is "no statically-identifiable caller". Fix:
qualify both spots. (Independent of P0-1.)

**P2-2 (QC) — leaf-census arithmetic does not sum to its denominator.**
HOLDER14_PROVENANCE.md §C(ii): leaf verdicts THIS_ENTRY=814, BOUND_EXHAUSTED=485, LEA_ADDR=244,
OTHER_WRITE=224, ZERO=21, CALL_RETURN=36, PARAM=68 sum to **1,892**, not the declared 1,895 non-family
rows (3 rows unaccounted in the printed breakdown). The per-row CSV classification (1,895) is correct
(QC recount); the printed leaf census is internally inconsistent. Fix: regenerate the breakdown from
the rows or correct the numbers.

**P3-1 (QC) — [N7] mini read-census undercounted ("exactly 10" is wrong).**
NEGCTL_RECEIVER_RAW.txt [N7] claims "[reg+0x14] operand references in family functions: 10". The QC's
own scan over the full family-function set (all slots of the 10 family vtables + all ctors/dtors — 57
functions) finds **28** refs, including: the PSP/PSPMod vtable slot-7 delegation stub 0x006FE890
(`mov edx,[eax+0x14]` @0x006FE899 — another vtable-slot-5 read like 0x006FAB66, missed by [N7]);
PSP-ctor source-array reads `fld [eax+0x14]`/`fld [ecx+0x14]` @0x006FEA46/0x006FEA4C; esp-based refs
in the AT ctor (0x006FB3EA/0x006FB4EE), Derivatives slot 6 (0x006FB9D4), Linear/Sin ctors
(0x006FBAB4/0x006FBAC2/0x006FD274/0x006FD282), PSPMod ctor (0x006FEB55), Predefined slot-3 function
(0x008267C7/0x008267DA). [N7] does not declare its family-function set bound. Auxiliary raw; not
load-bearing (the writer census is the load-bearing artifact and is correct). Fix: bound the claim or
regenerate over the full family set.

**P3-2 (QC) — HOLDER14_CENSUS_SUMMARY [C4] is a partial list presented as "FAMILY-CTOR CALLER
FUNCTIONS (one level up)".** It lists 7 caller functions (PSP/AT/NU/TC + Deriv×3) but omits the Linear
factory and the four Sin factories (QC's E8 census of the derived ctors: TC=1 @0x006D2656, NU=1
@0x006D258B, AT=1 @0x006D253A, Deriv=3 @0x006D20DA/0x006D22F7/0x006D2457, PSP=1 external @0x006D1578
(+1 family-internal: PSPMod ctor @0x006FEB4B), Linear=1 @0x006D1DC6, Sin=4
@0x006D1736/0x006D1828/0x006D1AF3/0x006D1CB3; Cyclic=2 family-internal @0x006FBAD9/0x006FD299).
Labeled "context only"; misleading as a census. Fix: complete or relabel.

**P3-3 (QC) — ARG2_VALUE_FLOW_RAW [E3] misprints the ArkVegetationObservable slot-2 value.** [E3]:
"its vtable 0x00A9D294 slot-2 = 0x00000000". The actual dword @0x00A9D29C = **0x566B7241** (ASCII
"ArkV" string fragment — the vtable has fewer than 3 slots). The REJECTED classification is correct
(no slot-2 entry ⇒ cannot dispatch the thunk; QC re-read the other four: MaPanel* slot-2 =
0x0083FA60 ≠ thunk ✓). Fix: print the real dword or "no slot-2 entry".

**P3-4 (QC) — IDENTITY_VERIFICATION [5] PIN-NN measured-address typo.** "measured dword @0x00A8D138 =
0x007B5390 MATCH=True": 0x00A8CCF4+0x44 = **0x00A8CD38** (QC own read: 0x007B5390 — MATCH ✓); the
dword at the printed 0x00A8D138 is 0x00000000. Value/pin correct; printed address wrong (D138 vs CD38).
Not load-bearing (pins-table revalidation only; G12 NOT_APPLICABLE). Fix: correct the printed address.

**P3-5 (QC) — AT_RUN_END_GIT_OBSERVATION.md local-timestamp inconsistency.** "2026-09-15T07:06:59Z
(executor-local 2026-09-14 22:06:59 Pacific Standard Time)": 07:06:59Z = 2026-09-15 00:06:59 PDT; the
AT_RUN_START pair is internally consistent. Metadata-only. Fix: correct the local line.

**P3-6 (QC) — AT_RUN_START_GIT_OBSERVATION.md dangling pointer.** References
"01_RAW/GIT_OBSERVATION_COMMANDS.txt" (not in the package; content moved to AMEND_LOG A8). Fix: point
to AMEND_LOG A8.

**P3-7 (QC) — HOLDER14_WRITER_RAW [IV-0d] is incomplete for its stated scope.** "operator-new sites
feeding family ctor calls" lists 11 sites (the 6 base-ctor-calling derived ctors) but omits the
PSPredefined and PSPredefinedMod new-sites (PSP factory block's `call 0x95D3C4` @0x006D1530 with the
size pushed before block entry; PSPMod ctor called from 6 dispatcher sites @0x006D12A3/0x006D1329/
0x006D13AF/0x006D142C/0x006D14A9/0x006D1526 — QC's own E8 census). Fix: complete or bound the title.

**P3-8 (QC) — P1-2's RTTI-region wording is imprecise (claim itself CONFIRMED).** FORWARDER_ANALYSIS:
"0x00AA7958 ... is CyclicLinear's base-class descriptor array area". Precisely (QC reads): 0x00AA7958
is the **pBCD-array pointer field of the Cyclic CHD @0x00AA7948** (value 0x00AA7964 → Cyclic's own BCD
array at 0x00AA7964; CyclicLinear's BCD array begins at 0x00AA79A4). The load-bearing claim (RTTI
data, not a vtable; no thunk dword — QC: no 0x006FAB80 dword in 0x00AA7930..0x00AA79A4) is CONFIRMED.
Fix: correct the wording.

## 4. Counterexample hunts (mandate items 1–6) — methods and outcomes

1. **BULK-COPY HOLE — bounded-empty within the family code region; channel declared.** QC census:
   636 rep movs/stos sites in .text; 4 in the ArkAnimation code region: 0x006FBDD7/0x006FBDE8 (inside
    the **ArkAnimationRotation** ctor [0x006FBDB0..0x006FBE23) — copies template data to [ebx+0x34]/
    [ebx+0x58], a child-class object, not a family object, offsets do not cover +0x14), 0x006FBF30
   (child-class helper, destination [edi+0x38]-range), 0x006FEE22 (func [0x006FEDA0..0x006FEE47),
   destination [ebx+0x48]-range — does not touch +0x14). All family ctors/dtors initialize
   field-by-field (QC decodes) — no copy-ctor/assignment-copy construction path for family objects
   found in the family region. **NOT CHECKED (declared):** .text-wide destination-provenance tracing
   of the remaining 632 rep-movs sites (would require the run-scale slice engine; a family-object
   pointer would have to flow out and back, and the QC's family-function scan shows no such handoff
   inside family code). Note: the run never censused this
   channel either (the census's write-form coverage is disp==0x14 write instructions) — under P0-1's
   correction this channel should be declared in the corrected report's bounds.
2. **NON-E8 CHANNELS TO THE BASE CTOR AND DERIVED CTORS — empty.** QC own censuses: E9→0x006FABA0: 0;
   EB→0x006FABA0: 0; imm32 0x006FABA0 whole-file: 0 (no function-pointer channel); E8→base ctor:
   exactly 6 (byte-identical to the run's list). Per derived ctor: E8 callers TC=1, NU=1, AT=1, Deriv=3,
   PSP=2 (1 external + 1 family-internal PSPMod ctor), Cyclic=2 (family-internal Linear+Sin), Linear=1,
   Sin=4; E9/EB per ctor: 0; imm32 per ctor VA: 0. No virtual/function-pointer construction channel
   exists; the caller enumeration of every family ctor is complete. (The P0 enters through the
   enumerated E8 channel itself — the VALUE chains, not missing callers.)
3. **THE 68/814 RESIDUE — sampled, no family hit found.** QC sampled 15 PARAM-leaf and 15
   THIS_ENTRY-leaf census rows (all 30 byte-identical to the physical bytes — row integrity ✓);
   containing functions are non-family; no non-family census row's OP_STR references any family
   vtable value (QC fingerprint scan over all 1,895 rows). The residue therefore remains honestly
   labeled unproven in the run. (P0-1 does not enter through this residue — it enters through the
   run's own PROVEN slice paths, which is why it invalidates the headline rather than just widening
   the residual uncertainty.)
4. **THE 1,433 INSUFFICIENT_PROOF CANDIDATES — sampled 18, all genuine slot-2 dispatch patterns with
   unproven receivers; none claimed PROVEN; the report (in its census fields) does not claim the thunk
   is never called.** The unqualified "has no caller" spots are reported as P2-1. Note under P0-1: the
   corrected report must also drop the "a dispatch would fault at [NULL]" shortcut (see P0-1 §5).
5. **CRASH-CONSISTENCY WORDING — correct as wording, broken as premise.** REPORT §1 words it as a
   hypothetical ("A hypothetical dispatch on a live family instance would fault at [NULL]") — good.
   But P0-1 breaks the premise: live family instances with non-NULL held exist on bounded paths, so
   the hypothetical dispatch would NOT fault; that consistency argument must be retracted, not just
   re-qualified.
6. **FACTORY IDENTITY/LIVENESS — the construction layer is STATICALLY REACHABLE, which further
   undermines the "unexercised" reading.** The dispatcher construct entry 0x006D0ED0 has 3 direct E8
   callers (0x0058EFD6, 0x0058F19F, 0x006D2B1C — QC census); the name-compare chain uses inline
   string compares against .rdata names (no jump tables — QC imm32 census of all block starts: 0
   hits); the PSPMod ctor has 6 dispatcher call sites. Under the corrected reading, the family's
   held-object feature is a **live composite-animation binding mechanism** on the normal dispatch
   paths — only the slot-2 forwarder remains without a statically-identifiable caller.

## 5. Independent re-derivations (mandate a–j) — summary of QC evidence

(a) EXE identity: own measure — all pins MATCH (QC-1). (b) FUN_006FAB80: own decode — extent
0x006FAB80..0x006FAB9A (ret 8, 6x CC pad, next start 0x006FABA0), thiscall ECX, arg1 [esp+4] via
`fld/fstp` x87 roundtrip (slot-allocation push semantics confirmed: the pushed ECX cell is overwritten
by the fstp), arg2 [esp+8] verbatim via EDX, slot-3 byte evidence `8B 40 0C`, single basic block, one
call — FORWARDER_OPERATION_STATUS=CONFIRMED re-derived. (c) Base ctor 0x006FABA0: own decode — ret
0xC (3 stack args), arg2=held @ [esp+0xC] (`8B 4C 24 0C`), write `89 48 14` @0x006FABB5, refcount
`BA 01 00 00 00`/`01 51 04` NULL-guarded by `85 C9`+`74 03`; E8 census to 0x006FABA0: exactly 6 sites
(0x006FAFC7/0x006FB092/0x006FB409/0x006FB5CD/0x006FE9E8/0x006FFA87). (d) Per-site arg2 chains:
sites 1/2/3/5 = immediate `push 0` (byte-verified); sites 4/6 param chains re-derived — including
the QC's own esp-delta frame arithmetic for the Derivatives ctor (0x28−0x1C=0xC=arg2) and the
push-tail arg-slot verification at the factory calls — **with the P0-1 discovery that the chains are
NOT constant-NULL** (bypass edges). (e) Five-class membership: own COL/TD/CHD/BCD walks — names,
vtables, extents (8/8/9/9/9 slots; stop dwords re-read), slot ordinal 2 == thunk in all five; imm32
census = 5 own-slot dwords; 0x00AA7958 = Cyclic CHD pBCD field (0x00AA7964), no thunk dword in the
region — P1-2 CONFIRMED. (f) Writer census arithmetic: own recount 10,711 / 1,898 / 8,811 / 2 / 0 /
0; FAMILY_CONTEXT_PROVEN=3 (a=3, b=0); NON_FAMILY=1,895; 30 residue rows byte-verified. (g) Caller
census: own byte censuses 156,829/40,668/17,961 → 0; imm32=5; own recount 1,438 → 0/5/1,433; the 5
REJECTED receivers re-read (4x slot-2=0x0083FA60; ArkVegetationObservable has no slot-2 — see P3-3).
(h) Negative control: own recount 1,393/803/1 + own PIN-NC dword reads (all MATCH). (i) Status algebra
+ wording: statuses correctly separated in the matrix; the bounded-static wording holds in the census
fields; the two unqualified "no caller" spots (P2-1) and the P0-1-affected fields listed above.
(j) Package hygiene: MANIFEST_SHA256.csv 40/40 hashes+sizes verified (QC re-hash), self-exclusion
correct (only MANIFEST_SHA256.csv itself outside the manifest; QC_AUDIT.md is a post-manifest QC
addition per contract §13); SCRIPT_SHA256.csv 10/10 verified and consistent with every raw header's
GENERATOR line; no __pycache__/.pyc anywhere in the package; STAGE_ACCEPTANCE_GATES.csv complete with
G13/G14/G15 PENDING; EVIDENCE_INDEX.csv 16/16 rows carry MEASURED_QUANTITY /
INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED (some FAILURE_CASE_DETECTED
cells are "N/A" — acceptable for pure re-measure rows; the material gates carry explicit YES).

## 6. What the QC verified as CORRECT (for adjudication context)

Phase A (thunk decode, 10/10 pin rows), Phase B (five-class membership, extents, ordinals, hierarchy,
vtable-store census, 0x00AA7958 falsification), the base-ctor ABI correction P1-1 (including the
NULL-guard the pin missed), the full census arithmetic (both CSVs), the Phase D four-channel census
(0 thunk callers — QC byte censuses agree exactly, including all three raw-byte denominators), G7
(1/803 selectivity + both PIN-NC anchors + the 5 REJECTED candidates), the SF infrastructure
revalidation (P1-3 chunk-2 ret-8 site; P1-4 container correction — 3 factory calls with args
0xF0000000/1/2 storing at +0x0C/+0x10/+0x14, QC byte-verified), the 6-site E8 list, the honest
NOT_DEMONSTRATED/UNVERIFIED statuses, the AMEND_LOG correction discipline (A4's arg0→arg2 fix was
properly recorded), the L12 manifest self-exclusion, and G1's git discipline (QC post-hoc check:
HEAD/origin == BASE_SHA, untracked set exact, zero mutations).

## 7. QC coverage and NOT_CHECKED

Covered: every headline claim (9/9 items of the QC mandate) re-derived from bytes with the QC's own
tooling; both census CSVs fully recounted; 30 residue rows + 18 dispatch candidates + 5 REJECTED
receivers + 3 PIN-NC anchors byte-verified; all 10 classes' RTTI lineages walked; the child-class
hierarchy identified; package hygiene fully verified; git state verified read-only.

NOT CHECKED (explicit):
- Full independent re-derivation of the B.5 function map (105,492 functions) — the QC used the run's
  B5_FUNCTION_MAP.csv only as a lookup index; every load-bearing address was independently decoded.
- .text-wide destination-provenance tracing of the 632 out-of-region rep-movs sites (bulk-copy
  channel declared in §4.1).
- Deep caller-cross re-derivation of the remaining 1,433 dispatch candidates and the 68 PARAM rows
  beyond the QC samples (run-scale slice engine required).
- Runtime behavior of anything (STATIC-ONLY QC; the client was never executed).
- The dispatcher's name-table semantics (which animation names select which block) — not needed for
  any verdict.
- imm32 census of the five child-ctor VAs as potential function-pointer channels (the P0 is
  established via the direct dispatcher calls; additional channels could only widen it).
- The run's G10/G11 dispositions beyond their dependence on the empty-caller set (they stand).

## 8. Adjudication inputs for PE-MASTER (G14)

- QC_VERDICT: **QC_FAIL** — one P0 (P0-1 above); the run's primary answer is falsified in static
  reach; the repair is bounded (re-slice with branch-edge awareness at the 6 sites / 9 chains,
  re-dispose 5 status rows, correct the affected texts, regenerate the defective raw sections via
  AMEND_LOG).
- A large body of the run's measurements is independently confirmed and should be PRESERVED (§6);
  the correction should not trigger a wholesale re-run.
- The corrected science result (QC-measured): the seam "ArkAnimation → [this+0x14]" is a REAL
  composite-animation binding edge; its bounded receivers are the ArkAnimationFloatValue-hierarchy
  channel classes (Scale/Intensity/Alpha/Color/Translation; slot-3 targets 0x006FFF00/0x9154A0 —
  QC-measured, none == 0x0050A050); the SceneFeeder Rosetta edge is falsified at the
  receiver-identity link (SUCCESS B proper) — NOT at "the binding edge does not exist". HELD =
  NULL for 6 of 10 classes and on all allocation-failure paths; non-NULL child objects otherwise.
- QC session performed ZERO git mutations; the only file created inside the package is this
  QC_AUDIT.md. QC counter-check scripts and outputs are outside the package at
  `C:\Users\User\AppData\Local\Temp\opencode\pe_qc_holder_r1\` (AUDITOR COUNTERCHECK, NOT project
  evidence).
