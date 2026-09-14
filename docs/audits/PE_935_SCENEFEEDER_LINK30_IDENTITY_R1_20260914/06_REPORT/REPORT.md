# REPORT.md — PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914

RUN_ID: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 · RUN_CLASS: LOAD_BEARING ·
Milestone: EU935-M1 World Surface Fidelity (SceneFeeder position chain, SF+0x30
link-identity seam) · Era: PCG_9_3_5 · MODE: STATIC-ONLY (the client NEVER ran; no
process of any game binary was launched; byte-reading scripts only; nothing here is
a runtime oracle result). Executor: pe-reconstruction (direct PE-MASTER dispatch,
NO_NESTED_TASKS). Publication is a separate later step (pe-master-auditor, after
PE-MASTER adjudication) — ZERO git mutations by this run.

---

## 1. Human-first decision block

**Co jest zapisywane do SceneFeederObject+0x30 i jaka jest klasa tego obiektu?**

**Answer (statically proven, era PCG_9_3_5):**

1. **What is written:** exactly TWO static instructions in the whole binary are
   proven writers of [SF+0x30]:
   - **0x005093C3** in the SF constructor FUN_00509330: `mov dword ptr [ebp+0x30], eax`
     (bytes `89 45 30`) — stores a freshly **operator-new(0x118)** heap block,
     initialized by FUN_007B6000(this=block, arg=0), then **refcount++ at block+4**
     (`add dword ptr [eax+4], 1` @ 0x005093C8).
   - **0x0050A2D1** in the SF destructor body FUN_0050A240: `mov dword ptr [esi+0x30], ebx`
     (bytes `89 5E 30`, ebx=0) — after the refcount release protocol
     (decref `add [ecx+4],-1`; at zero: destroy via vtable slot 1 `call edx`),
     the field is nulled.

2. **Class/type of the stored object:** the stored block's primary vtable is
   **0x00A8CCF4** (stored by the block ctor at 0x007B6041 `mov dword ptr [esi],0xa8ccf4`),
   and the byte-confirmed MSVC RTTI walk gives the verbatim name

   **RTTI_NAME = `.?AVNiNode@@`**

   — the Gamebryo/NetImmerse **NiNode** scene-graph node class. The object is
   reference-counted (count dword at block+4; SF ctor increments, SF dtor decrements
   and destroys through vtable slot 1 when zero). Supporting structure: the block
   embeds a member vtable 0x00A8CCE0 at block+0xE0 = `?$NiTPointerList@PAVNiDynamicEffect@@@@`
   (consistent with NiNode's dynamic-effect list).

**FINAL_STATUS: A — IDENTIFIED** (complete writer census with auditable denominator +
continuous creation/receipt provenance for both writers + RTTI/type identity with
calibrated walker). **NEXT_SEAM: SLOT17** (the NiNode vtable slot 17 dword at
[0x00A8CCF4+0x44] = 0x007B5390 — VALUE recorded, NOT decoded, per contract).

Scope guard honored: no MODEL_BRIDGE_CONFIRMED and no TRANSFORM_TO_MODEL claim is
made anywhere in this package; TRANSFORM_TO_MODEL remains NOT_DEMONSTRATED. The RTTI
name does not read like a "Model..." class; the maximum semantic label achieved is
**SF30_LINK_TYPE_IDENTIFIED**.

---

## 2. State before → after

- BEFORE (accepted PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914): SF+0x30 = an UNKNOWN
  "link" object, read by vtable slot 3 (FUN_0050A050) primary path at 0x0050A05B and
  dispatched through the link's vtable+0x44; no writer census existed; the link class
  was explicitly UNKNOWN. Canon completeness note: the accepted
  PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 had ALREADY established (own
  decode, its REPORT §4.1 FUN_00509330 line) that the SF ctor performs new(0x118) →
  FUN_007B6000 → stores at SF+0x30, with refcount at block+4, characterized as a
  "scene object" with NO class name.
- AFTER: SF+0x30 = a refcounted NiNode heap block; complete writer census performed
  (2 proven writers, denominator 3643); provenance chains byte-evidenced; class
  identity RTTI-confirmed `.?AVNiNode@@`; the field's proven lifecycle transitions
  (create in ctor / release+null in dtor) are byte-locked (mid-life writers bounded by
  the census residue, §3/§7). THIS run independently CONFIRMS that prior-run chain
  byte-level and adds: the complete writer census (incl. the dtor nulling), the
  calibrated RTTI class identity `.?AVNiNode@@` (newly published), the slot-17
  value, and the census bound. P1 provenance chain: byte-confirmed (consistent with
  the prior-run association; class identity NEW).

---

## 3. Claims → evidence (all VAs byte-locked from the physical EXE via own PE walk)

| # | claim | status | evidence |
|---|---|---|---|
| C1 | RTTI walker calibration reproduces the known answer | CONFIRMED | 01_RAW/SF30_RTTI_RAW.txt §A: [0x00A7D454]=0x00AA12B8 → COL(sig=0,off=0,ptd=0x00B78834) → TD name `.?AVSceneFeederObject@@` == expected. Asserted fail-closed before the link walk. |
| C2 | SF identity re-derived in-run (not inherited) | CONFIRMED | Raw §2.1: exactly TWO stores of imm32 0x00A7D458 in .text: 0x00509366 (ctor, `mov [ebp],0xa7d458`) and 0x0050A269 (dtor, `mov [esi],0xa7d458`); ctor E8 callers = {0x0047D043, 0x0052480F}; ZERO absolute dword refs of 0x00509330 in the file; both creation paths = operator new(0x98) (thunk 0x95D3C4 = MSVCR80.dll.??2@YAPAXI@Z, own IAT walk). |
| C3 | Complete writer census (Task A) | CONFIRMED | Enumeration rule (documented in raw header): linear capstone 5.0.7 sweep of FULL .text (0x00401000..0x00A75000, rsize 0x674000), bad-byte restart; 2,266,698 instructions decoded, 64 restarts; RAW CANDIDATES (any WRITE mem-operand disp==0x30: mov disp8/disp32, base+index+disp, imm stores, superset incl. x87) = **3643** = the denominator. Every candidate has a CSV row; counts recomputed from rows: PROVEN=2, REJECTED=3023, POSSIBLE=618, UNRESOLVED=0 (3643 total). (Counts historical at this run's publication; canonical after AMEND_LOG_R2 F1 branch (b): 619 POSSIBLE / 3022 REJECTED — census row 0x0040525B reclassified REJECTED_ALIAS -> POSSIBLE_ALIAS; the CSV rows unchanged.) |
| C4 | The two PROVEN writers + receiver provenance | CONFIRMED | 0x005093C3: ebp==SF (0x00509357 `mov ebp,ecx`; 0x00509366 vtable store) — CSV receiver_provenance carries the chain. 0x0050A2D1: esi==SF (0x0050A263 `mov esi,ecx`; 0x0050A269 vtable store; dtor body called from vtable slot 0 FUN_0050A460). |
| C5 | Source provenance to creation/receipt only (Task B) | CONFIRMED | 02_ANALYSIS/SF30_PROVENANCE.md: P1 hop table 0x00509376→0x005093C8 (new(0x118)→FUN_007B6000→stored→refcount++), STOP at receipt; P2 = constant 0 (0x0050A272 `xor ebx,ebx`) after the release protocol 0x0050A2BD..0x0050A2D1. SOURCE_PROVENANCE per writer: RESOLVED / RESOLVED (no UNRESOLVED edge needed). |
| C6 | Type identity (Task C) | CONFIRMED | Raw §B: block ctor 0x007B6041 stores vtable 0x00A8CCF4; [0x00A8CCF0]=0x00AAEEC8 (raw bytes `c8eeaa00`) → COL(sig=0,off=0,ptd=0x00B936C8) → TD name bytes `2e3f41564e694e6f64654040` = `.?AVNiNode@@`; vtable in .rdata, 47 code-pointer entries; ctor FUN_007B6000 is NOT a vtable entry (not virtual). Supporting: embedded vtable 0x00A8CCE0 @ block+0xE0 → `?$NiTPointerList@PAVNiDynamicEffect@@@@`. |
| C7 | Positive control (mandatory) | PASS | 01_RAW/POSITIVE_CONTROL_0050A050.txt: (a) 0x0050A057=`8B F1` (mov esi,ecx), 0x0050A05B=`8B 4E 30` (mov ecx,[esi+0x30]); (b) ECX NOT modified in 0x0050A05B..0x0050A064 (measured: only `mov edx,[ecx]`, `push eax`, `mov eax,[edx+0x44]`); (c) 0x0050A05E=`8B 11`, 0x0050A061=`8B 42 44`, 0x0050A064=`FF D0` (call eax) — receiver of the call = ECX = [ESI+0x30] = [SF+0x30]. Independently re-asserted at gate time (G1). |
| C8 | Coverage classes (i)–(iv) | SCANNED (all four) | Raw §05: (i) every register-based candidate classified; (ii) stack-slot SF holders traced ([esp+0x60] @ FUN_0047CCF0, [esp+0x2c] @ FUN_005247C0) — no additional proven writer; (iii) combined-disp forms {0x34,0x3C,0x40,0x44,0x48,0xF0} at the 5 proven container functions (7 store sites) → ZERO hits (see C10); (iv) bulk-init at SF ctor/init sites: only 2 `rep movsd` in the ctor — targets [esp+0x18] (stack) and [ebp+0x4C] (SF+0x4C..0x70) — NEITHER covers +0x30. |
| C9 | SF durable-pointer slots census | CONFIRMED | Complete E8 census of FUN_005247C0 = 7 callsites; after each, the returned SF is stored at container+{0x0C,0x10,0x14} (FUN_0044D590), +0xC0 (FUN_00528E50 — the prior-run "instance+0xC0" pointer re-derived and confirmed), +0x04 (FUN_0067B800, FUN_0067C7C0), +0x18 (FUN_006A3930). SF methods are re-received from those slots (e.g. load @0x0052901A `mov ecx,[esi+0xc0]`; call 0x5094c0 @0x00529020) — receiver proof for FUN_005094C0. |
| C10 | Combined-offset alias impossibility | CONFIRMED (negative) | The SF slot holds a POINTER (store `mov [container+field],eax`, eax=operator-new block), not an embedded SF — so a [container+field+0x30]-form write hits the container's own field, never SF+0x30. Scanned anyway per contract: zero hits of the combined forms at the proven container functions. |
| C11 | Scope held | CONFIRMED | G5 script census: zero claim-context occurrences of MODEL_BRIDGE_CONFIRMED / TRANSFORM_TO_MODEL in the package; zero slot-17 decode listings; zero candidates inside the forbidden function ranges (0x437F70, 0x82B5A0, 0x007B5390) — the positive-control window re-read (allowed) is the only touch of forbidden callees IN THE PACKAGE CONTENT; the gate machinery derived the forbidden functions' extents by in-memory boundary-only decode (no semantics extracted, nothing persisted). |

### The POSSIBLE_ALIAS bound (honest residue, by design of the taxonomy)

619 of 3643 candidates are classified **POSSIBLE_ALIAS** (canonical after
AMEND_LOG_R2 F1; historical row count 618): receiver provenance not
resolvable to SF or non-SF within this run's static bounds (base register e.g. esi/eax
in functions never proven to receive SF; whole-binary SF pointer-origin closure —
interprocedural dataflow — was out of scope). This residue is the documented static
bound of the census method, NOT unexamined code: every row carries its form, function,
and the structural rejection rules that did not apply. 3022 rows are REJECTED_ALIAS
(canonical after AMEND_LOG_R2 F1; historical row count 3023) with per-row reasons;
fired-reason census recomputed by script from the raw why-lines of the HISTORICAL
01_RAW/SF30_WRITER_RAW.txt (byte-identical): **R-ESP 2765 / R-STACK-PTR 129 /
R-CTOR-OTHER 104 / R-ZERO 18 / R-LEA-STACK 3 / R-EBP-INHERITED 2 / R-IMM-STATIC 1 /
R-CONT-FIELD 1 = 3023 (historical)**; **R-EBP-FRAME: rule present, never fired
(0 rows)**. (AMEND_LOG_R2 F1 supersession, BRANCH (b): the historical R-IMM-STATIC
label of census row 0x0040525B — raw why-line 'base==edx = fixed immediate address' —
is SUPERSEDED: the base register holds the VALUE loaded from the global pointer slot
0x00B6C3D8 (`mov edx, dword ptr [0xb6c3d8]` @0x00405250, bytes 8B 15 D8 C3 B6 00;
proof 01_RAW/F1_GLOBALPTR_PROOF_RAW.txt). The corrected rejection R-GLOBAL-PTR-NON-SF
was attempted and PROVED the direct-write channel closed (exactly ONE direct writer
0x00404C9D storing FUN_00409080's return = its `this` = 0x00B9FEC0, a static .data
address, non-polymorphic — no vtable store in its body; the slot at rest 0x00000000) —
but the address-taker channel is OPEN: the sole consumer of &global (FUN_00404B60,
arg verified at [esp+0x20]) stores the arg pointer into a linked list (`mov dword
ptr [ecx], edx` @0x00404BE9 with edx == &global), so a write-through-pointer channel
via the list is NOT excluded within the amendment's static bounds. The row is
therefore reclassified REJECTED_ALIAS -> POSSIBLE_ALIAS. Canonical counts: 3643 =
2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED. The historical CSV/RAW
artifacts stay byte-identical; the reclassification is recorded in AMEND_LOG_R2 and
02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md.)

---

## 4. Gates (06_REPORT/STAGE_ACCEPTANCE_GATES.csv; all recomputed by finalize.py)

| gate | verdict | raw evidence (summary) |
|---|---|---|
| G0-SOURCE-BASE | **PASS** | EXE sha E7785430...F31 == pin, size 8015872 == pin; HEAD==origin/master==ls-remote==1a490eed4ca2b295e78cd3cf851a08ac9c93930b; dirty = foreign untracked experiments/ + this run's own untracked package dir (by-design; git mutations forbidden). |
| G1-POSITIVE-CONTROL | **PASS** | bytes (a)(b)(c) measured exactly as specified; re-asserted from physical bytes at gate time. |
| G2-CENSUS-COMPLETENESS | **PASS** | enumeration rule + range + denominator (3643) documented in raw; 3643/3643 rows carry 4-class classification; raw==CSV==state-json counts (2/618/3023/0); coverage (i)–(iv) all scanned in raw. |
| G3-PROVENANCE | **PASS** | both PROVEN writers have creation/receipt-level hop tables with VA+bytes; no UNRESOLVED edge. |
| G4-TYPE-IDENTITY | **PASS** | calibration PASS first; link walk byte-confirmed to `.?AVNiNode@@`; re-walked independently at gate time; slot-17 VALUE recorded NOT decoded. |
| G5-SCOPE-HELD | **PASS** | zero forbidden RESULT claims; zero slot-17/0x437F70/0x82B5A0 analyses; zero denominator rows inside forbidden ranges. |

## 5. Negative controls (meaningful, run-internal)

1. **RTTI known-answer calibration** — the walker must first reproduce
   `.?AVSceneFeederObject@@` from 0x00A7D458 (fail-closed assert) — protects the
   `.?AVNiNode@@` result from walker bugs.
2. **Absolute-reference test** — dword 0x00509330 occurs ZERO times in the file →
   the ctor (and hence SF creation) census via E8 callsites is complete, no hidden
   indirect construction path.
3. **Combined-offset zero-hit scan** — the {+0x34,+0x3C,+0x40,+0x44,+0x48,+0xF0}
   forms at the proven container sites produce ZERO hits (and are provably
   non-aliasing because the SF slot is a pointer field, C10).
4. **Bulk-init non-coverage proof** — the ctor's two `rep movsd` are measured to
   target [esp+0x18] and [ebp+0x4C] (range +0x4C..+0x70) — bulk init provably does
   NOT cover +0x30 (class iv satisfied with byte evidence, not assumption).
5. **Classifier discipline** — the 3023 REJECTED rows (historical at this run's
   publication; canonical 3022 after AMEND_LOG_R2 F1) demonstrate the classifier
   does not rubber-stamp: structural rules (stack/frame/lea/null/other-class/
   container-field — plus the historical `imm` rule, whose single fired row proved
   a mislabel and is canonically POSSIBLE_ALIAS per AMEND_LOG_R2 F1/erratum E-2)
   fire with per-row reasons.
6. **Scope census** — zero claim-context forbidden labels; zero decodes of the
   forbidden callees; the slot-17 dword appears exactly once as a recorded VALUE.

## 6. Hard stops

None triggered. BASE and source identity verified exactly (no BASE_DRIFT, no
SOURCE_IDENTITY_FAIL); no blocker returned to PE-MASTER; run completed within its
contract.

## 7. NOT_CHECKED (explicit — what this run did NOT examine)

- **NiNode vtable slot 17 decode** ([0x00A8CCF4+0x44] = 0x007B5390): VALUE recorded,
  not decoded — the NEXT seam, per contract.
- **0x437F70, 0x82B5A0**: not analyzed (the positive-control window re-read of
  FUN_0050A050 bytes is the only touch, contract-allowed).
- The other 46 slots of the NiNode vtable; any method of the NiNode class.
- Callees inside the block ctor (0x7C02D0, 0x788480, 0x7DE000) — recorded at
  receipt level only, not analyzed (Task B stops at creation/receipt).
- The 618 POSSIBLE_ALIAS rows (historical at this run's publication; 619 canonical
   after AMEND_LOG_R2 F1) were not individually resolved to non-SF (requires
   whole-binary SF pointer-origin closure; declared bound of the method).
- The SF dtor's second release block (0x50A2D4..0x50A2EA, re-read of the now-null
  field) — semantics not analyzed beyond the measured write.
- SF+0x30's value LATER behavior (what the NiNode is used for after receipt;
  SceneFeeder→model direction) — TRANSFORM_TO_MODEL remains NOT_DEMONSTRATED.
- Callers/consumers of the SF vtable slots; GetPosition output consumers.
- 296445, template 4508, terrain, NIF, network, any runtime work — untouched.
- The second SF creation context's container fields beyond the SF slots proven here;
  other objects' +0x30 fields (only receiver-proven rows concern SF).

## 8. Untouched status (unchanged by this run)

- TRANSFORM_TO_SCENEFEEDER = PROVEN (accepted prior runs; re-derived here only as
  the creation chain feeding the census).
- **TRANSFORM_TO_MODEL = NOT_DEMONSTRATED** — nothing in this package upgrades,
  downgrades, or re-labels that status. Max label achieved: SF30_LINK_TYPE_IDENTIFIED
  (`.?AVNiNode@@`).

## 9. Handoff block (full delivery notice: 06_REPORT/HANDOFF.md)

RUN_STATUS: COMPLETE · FINAL_STATUS: A — IDENTIFIED · NEXT_SEAM: SLOT17
(0x007B5390 = [NiNode-vtable+0x44], recorded, undecoded). The one next test for the
next run: decode NiNode vtable slot 17 (0x007B5390) — the exact virtual invoked by
FUN_0050A050's primary path on the SF+0x30 link — down to its first call only, under
the standing scope guards (max label CANDIDATE_MODEL_BRIDGE or lower per that run's
own contract).
