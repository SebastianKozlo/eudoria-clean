# RUN_CONTRACT.md — PE_935_SF_ARG2_PROVENANCE_R1_20260914

Formalized by pe-master-auditor under PE-MASTER loop `2ed038db-5d2e-4e7e-b679-2d29bf57501a`
(EU935-M1, 4h auto loop, Phase 2 science). The Phase-1 cleanup
PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 is ACCEPTED and published — the loop may do
science. Executor: pe-reconstruction (direct PE-MASTER dispatch, NO_NESTED_TASKS).
Publication is a separate later step (pe-master-auditor, after PE-MASTER adjudication) —
ZERO git mutations by the executor.

**THIS FILE IS THE EXECUTOR'S ONLY BINDING SPECIFICATION.** The executor works from this
contract plus the two sibling pin records `00_CONTROL/SOURCE_IDENTITIES.json` and
`00_CONTROL/GIT_OBSERVATIONS_AT_FORMALIZE.md` (both IMMUTABLE INPUTS — do not edit, do
not append to them; your outputs go elsewhere in the package). Where this contract and any
memory, skill, summary or stale copy disagree, THIS CONTRACT wins. Where this contract's
expected pins and the physical pinned bytes disagree, THE BYTES win: record the
discrepancy as a PIN_MISMATCH finding, continue with the MEASURED truth, and fail the
affected gate — NEVER silently adapt a claim to a pin (rule L22).

---

## A. IDENTITY

| Field | Value |
|---|---|
| RUN_ID | PE_935_SF_ARG2_PROVENANCE_R1_20260914 |
| RUN_CLASS | MATERIAL — upward reclassification to LOAD_BEARING allowed later on evidence per governance A1.1: if the arg2 semantic role becomes a foundation for later runs, a fresh deep QC is owed |
| RUN_TYPE | STATIC_SEAM_PROBE (Rosetta edge: SceneFeeder → named-object lookup) |
| MILESTONE | EU935-M1 |
| ERA | PCG_9_3_5 |
| MODE | STATIC-ONLY |
| EXECUTOR | pe-reconstruction (direct PE-MASTER dispatch, NO_NESTED_TASKS) |
| PUBLICATION | separate later step by pe-master-auditor after PE-MASTER adjudication; ZERO git mutations by the executor |
| PARENT_LOOP_ID | 2ed038db-5d2e-4e7e-b679-2d29bf57501a (Phase 2) |

**MODE = STATIC-ONLY means:** the client NEVER runs in this run — no process launch of any
game binary, no debugger/tracer/injector attached to any binary, no oracle execution. Own
byte reads + own capstone disassembly of the pinned EXE ONLY. Every script MUST fail
closed on SHA256+SIZE of the pinned EXE BEFORE reading a single byte (see G0 and H).

**Package root** (skeleton `00_CONTROL` already created by the formalizer; the executor
creates the remaining dirs 01_RAW, 02_ANALYSIS, 03_EVIDENCE, 06_REPORT as needed):

```
D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_ARG2_PROVENANCE_R1_20260914\
```

**Repo BASE_SHA** (`12_WebGame\eudoria-clean`, branch `master`):
`f239eb85cd0f56ae10cee52d57833a49f225965c` — measured at formalize time: HEAD ==
origin/master (local cached ref) == live `git ls-remote origin refs/heads/master` ==
BASE_SHA (see GIT_OBSERVATIONS_AT_FORMALIZE.md). The executor RE-MEASURES all four at run
start (the AT_RUN_START git observation, see W6); any other value = HARD_STOP BASE_DRIFT
(no reset, no reconcile, report only).

**Physical source (the ONLY binary this run may read):**
`D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` — PINNED SIZE 8015872 bytes, PINNED
SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (measured by
the formalizer 2026-09-14; full identity record in SOURCE_IDENTITIES.json, including the
dispatching-prompt SHA-string discrepancy note). The executor re-verifies with its own
fail-closed S0 (SHA256 + size; plus PE32 sanity: machine 0x014C, image_base 0x00400000);
mismatch = HARD_STOP SOURCE_IDENTITY_FAIL, no downstream.

**Dirty/untracked inventory expected at run start** (re-verify in the AT_RUN_START
observation): exactly `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`
(untracked; PARKED historical package — IMMUTABLE, see G7), `experiments/` (untracked,
foreign — untouched), and this run's own package dir (by design). Nothing else. Any staged
path anywhere = HARD_STOP FOREIGN_STAGED_PATH (do not unstage, do not absorb; report and
stop).

**HARD_STOPS (armed):**
- SOURCE_IDENTITY_FAIL — EXE hash/size/PE32 mismatch → stop, no downstream.
- BASE_DRIFT — run-start HEAD/origin/ls-remote ≠ BASE_SHA → stop, no reset/reconcile, report only.
- FOREIGN_STAGED_PATH — any staged path in `git status --short` → stop; never unstage or absorb.
- PIN_MISMATCH is NOT a hard stop: it is a recorded finding (see the L22 rule above).

---

## B. STANDING FACTS (INPUT ONLY)

These are INPUT pins, not conclusions of this run. Re-verify each IN-RUN from physical
bytes as fail-closed pins where marked; NEVER upgrade any of them by citation. Their
published sources are pinned in SOURCE_IDENTITIES.json.

### B.1 SceneFeederObject slot 3 (re-verify in W1; source: PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914, published)

SceneFeederObject (SF) primary vtable **0x00A7D458** (RTTI `.?AVSceneFeederObject@@`,
6-slot vtable: slots 0..5 = 0x50A460/0x5090A0/0x5090B0/0x50A050/0x5090C0/0x509580);
its slot 3 (+0x0C) = **FUN_0050A050 = GetPosition(out arg1, query arg2)**:

- **Primary path (arg2 != NULL):** reads [SF+0x30] (the NiNode link), virtually calls the
  link-vtable slot +0x44 (target 0x007B5390) at 0x0050A064, passing the name argument;
  the returned object's +0x90 flows 0x437F70 -> 0x82B5A0 to fill arg1 (published flow —
  REFERENCE ONLY this run, do NOT re-analyze; G6).
- **Fallback path (arg2 == NULL):** self-vcall of vtable slot 1 (the +0x34 address
  getter), then copies X/Y/Z from SF+0x34/0x38/0x3C to the caller's out buffer.

Dispatch-window pins (fail-closed; VERIFY the bytes in W1):

| VA | bytes | instruction |
|---|---|---|
| 0x0050A057 | 8B F1 | mov esi, ecx (esi = this = SF) |
| 0x0050A05B | 8B 4E 30 | mov ecx, [esi+0x30] (the link) |
| 0x0050A05E | 8B 11 | mov edx, [ecx] (link vtable) |
| 0x0050A060 | (VERIFY) | push eax (the dispatch push — the arg2 name argument; W1 re-derives the eax def chain) |
| 0x0050A061 | 8B 42 44 | mov eax, [edx+0x44] (slot 17 of the link vtable) |
| 0x0050A064 | FF D0 | call eax |

Fallback-path pins (fail-closed; VERIFY in W1): self-vtable load + slot-1 vcall at
0x0050A087 (`mov edx,[esi]`) / 0x0050A089 (`mov eax,[edx+4]`) / 0x0050A08E (`call eax`);
X/Y/Z reads at 0x0050A090 / 0x50A098 / 0x50A09E (from SF+0x34/0x38/0x3C via the returned
&SF+0x34); out-buffer copies at 0x50A096 / 0x50A09B / 0x50A0A1. Published measured ABI:
**ret 8** (two stack args) — MEASURE every ret site yourself, do not assume. Published
function extent: 0x0050A050..0x0050A0AA (90 B) — re-derive by the B.5 rule. Published
prior-run NOT_CHECKED note relayed as input: the SLOT_CENSUS run flagged an unexamined
"shared-tail polymorphism of slot 3's second entry (arg1's vtable, caller-side object)" —
your own boundary + decode decides what the tail actually contains; record it.

### B.2 The SF+0x30 link and its slot-17 function (standing; do NOT re-identify — G6; sources: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 + PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914, both published)

SF+0x30 = a refcounted **NiNode** (primary vtable 0x00A8CCF4, RTTI `.?AVNiNode@@`,
refcount at block+4). **0x007B5390 = the NiNode vtable slot-17 function** = a recursive
named-object lookup (OBSERVED_OPERATION CONFIRMED; FUNCTION_IDENTITY =
NiNode::GetObjectByName STRONGLY_SUPPORTED — **the locked B->A criterion; do NOT raise
it, do NOT re-derive it, do NOT re-identify slot 17**). Its published signature (standing
input): thiscall, one `const char*` stack argument (ret 4), EAX = object pointer or NULL;
self-name check first (name @ this+0x0C, helper 0x007BF220), then children (array @
this+0xCC, count @ this+0xD4), recursive same-slot virtual dispatch, first-match-or-NULL.
Published +0x90 fact (reference only): +0x90 = m_kWorld.m_Translate.x. A fail-closed VALUE
check you MAY do (a value read, NOT a decode): dword [0x00A8CCF4+0x44] == 0x007B5390.

### B.3 SF durable-pointer holder slots (the W2 starting points; verify the slot reads exist as pinned; source: LINK30 REPORT C9)

Receivers that may hold SF pointers: container+0x0C/+0x10/+0x14 (writer FUN_0044D590),
container+0xC0 (writer FUN_00528E50 — the "instance+0xC0" slot), container+0x04
(FUN_0067B800, FUN_0067C7C0), container+0x18 (FUN_006A3930). SF methods are re-received
from those slots (e.g. the load at 0x0052901A `mov ecx,[esi+0xc0]`, then call 0x5094c0 at
0x00529020 — the published receiver proof for FUN_005094C0). Additional published
creation-side pins usable for SF-proven values: SF ctor FUN_00509330, E8 callers =
{0x0047D043, 0x0052480F}; SF vtable imm32 stores = 0x00509366 (ctor) and 0x0050A269
(dtor); the two proven writers of [SF+0x30] = 0x005093C3 (ctor) and 0x0050A2D1 (dtor body
FUN_0050A240). NONE of these is adopted as this run's evidence without in-run
re-verification from bytes.

### B.4 The census canonical layer (context; source: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914 supersession, carried by the LINK30 R3 sidecar)

Canonical writer-census counts: **3643 = 2 PROVEN / 620 POSSIBLE / 3021 REJECTED / 0
UNRESOLVED** (the 2026-09-14 cleanup R1 supersession). The historical CSV/RAW artifacts
(LINK30 package) are IMMUTABLE (G7) — read-only if consulted; never edited, never adopted
as this run's evidence.

### B.5 The KNOWN function-attribution defect class (MANDATORY METHOD; source: cleanup R1, P2-1)

For ANY function-level analysis in THIS run, do NOT trust any inherited function boundary
(the P2-1 defect class: historical census function attributions were proven wrong for
non-function VAs with zero references). Derive every function extent yourself from the
bytes. **Your mandatory boundary-derivation rule (record per function in the raw
evidence):**

1. Decode from the entry VA (capstone, CS_ARCH_X86, CS_MODE_32, detail=True) to the
   first terminal control-flow end (RET / RET imm16 / unconditional JMP out of the
   window).
2. Padding evidence = a RUN of 0xCC (or 0x90) bytes AFTER a terminal end that COMPLETES to
   the next 16-byte-aligned VA. **FNMAP lesson: a single 0x90/0xCC byte before a
   16-aligned VA is NOT padding evidence — it can be an operand/disp byte of a preceding
   instruction.** The decoder must not consume padding bytes as instructions (the
   SLOT_CENSUS overrun lesson: a sweep once overran a 2-byte CC pad into the adjacent
   function; the fixed rule is alignment-completing runs + re-decode).
3. E8-target lattice: every E8/E9 (and EB/imm32) target is a function-start datum; a
   boundary is corroborated when the adjacent function start has its own
   E8/E9/EB/imm32/vtable references.
4. Zero-reference disproof: a candidate function start with ZERO E8/E9/EB/imm32
   references, not a vtable entry and not the PE entry point, is SUSPECT — record it,
   never build a claim on it silently.
5. This rule applies to EVERY function this run analyzes (including FUN_0050A050 itself).

---

## C. THE ONE PRIMARY QUESTION

> **WHO supplies FUN_0050A050's arg2 (the name argument of the SF slot-3 primary-path
> virtual dispatch to the NiNode named-object lookup), WHAT VALUES does it take, and WHAT
> is its semantic role?**

Output as FOUR INDEPENDENT statuses, each on its own evidence, each from the vocabulary
CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED:

1. **ARG2_ABI** — the calling convention and argument path: which register/stack slot
   carries arg2 at FUN_0050A050's entry, how it reaches the dispatch push, and the ret-N
   cleanup.
2. **ARG2_PROVENANCE** — who supplies it: the call sites of the slot-3 channel and their
   arg2 producers.
3. **ARG2_VALUE_CLASS** — what the values are (string literal / buffer / field / unknown),
   classified per value with evidence.
4. **ARG2_FINAL_SEMANTIC_ROLE** — what the argument MEANS. Hypotheses (node name / bone /
   socket / marker / other NiAVObject name / config key) are HYPOTHESES ONLY: do NOT
   infer char* → bone or name → socket (human order §32). This status may only rise above
   UNVERIFIED with DIRECT evidence (a string value matching a known runtime-consumed name
   is NOT enough; a direct producer→semantic link is).

The four statuses are INDEPENDENT: e.g. ARG2_ABI CONFIRMED with ARG2_FINAL_SEMANTIC_ROLE
UNVERIFIED is a perfectly valid outcome. An exhausted bound is an honest recorded
outcome — the affected status stays at its evidence level; it is NOT a failure.

---

## D. WORK ITEMS

### W1. ABI re-derivation (fail-closed)

Decode FUN_0050A050 fully (0x0050A050 entry to its extent end by your own B.5 boundary
rule; record the extent). Derive the arg2 register/stack path from the caller's pushes to
the dispatch push at 0x0050A060 (`push eax` — where does eax hold arg2? re-derive: entry
this=ECX, the arg1/arg2 stack layout, the exact eax def chain; record VA+bytes for every
instruction in the chain). Confirm the thiscall ret-4-vs-ret-8 cleanup: how many bytes
does FUN_0050A050 pop at EVERY ret site — it has 2 stack args → expect `ret 8` (C2 08 00);
MEASURE, do not assume. Confirm the fallback (arg2==NULL) branch site and its reads.
Expected pins to re-derive (fail-closed, B.1): the dispatch-window bytes; the fallback
reads at 0x0050A090/0x50A098/0x50A09E (X/Y/Z from SF+0x34/0x38/0x3C — VERIFY); the
out-buffer copies at 0x50A096/0x50A09B/0x50A0A1 (VERIFY). Every pin check records the
measured bytes; mismatch = PIN_MISMATCH finding + G1 disposition.

### W2. CALLER CENSUS of the slot-3 channel

FUN_0050A050 is vtable slot 3 of SF — the call channel is VIRTUAL
(`mov eax,[ecx]` + `call [eax+0xC]` or equivalent) on SF receivers. Three censuses, each
with its rule + denominators recorded:

- **(a) E8 census:** full-.text census of direct calls (E8 rel32; record E9 jmp targets
  too) targeting 0x0050A050. Expect 0 or few — MEASURE. Record: .text range, scan rule,
  total E8 count, match count, match VAs.
- **(b) imm32 census:** whole-file (all sections) little-endian dword 0x0050A050 census —
  the address-taken count. Expect exactly 1, at the vtable (the dword at 0x00A7D464 =
  [0x00A7D458+0x0C]) — MEASURE; record every hit's VA+section; any additional hit is an
  address-taken datum to disposition in (c).
- **(c) VIRTUAL CALL-SITE census:** find every call site that loads a vtable and calls
  slot +0x0C whose RECEIVER is provably an SF pointer. Bounded method (DECLARE the bound
  in the report; default bound: TWO levels of register/dataflow tracing):
  1. **Holder-slot route:** start from the KNOWN SF holder slots (B.3) — enumerate reads
     of those holder slots (e.g. `mov reg,[container+0xC0]` etc.) and check which flow
     into a slot-3 virtual call.
  2. **Pattern route (if feasible):** a bounded .text pattern census of `FF 50 0C` /
     `FF 90 0C 00 00 00` / `8B 40/41/... 0C` + `FF D0`-style sequences — but ALWAYS with
     receiver proof (below).
  3. **Receiver proof (mandatory for every candidate):** the receiver register must trace
     to an SF holder slot or an SF-proven value within the declared bound. An SF-proven
     value is one traceable to (i) a read of a known SF holder slot, (ii) an SF creation
     chain (the ctor FUN_00509330 call sites 0x0047D043/0x0052480F per B.3, re-verified
     in-run), or (iii) another receiver-proven SF value within the bound. A candidate
     without proof is recorded **INSUFFICIENT_PROOF** — honestly, never silently dropped
     and never promoted.
  4. Every candidate call site gets: VA+bytes, receiver proof (or INSUFFICIENT_PROOF),
     and the arg2 construction analysis (W3).

### W3. ARG2 PRODUCER ANALYSIS per call site

Trace back the pushed arg2 register/stack slot at each verified slot-3 call site to its
producer: an immediate string VA (read the .rdata/.data literal — record the string bytes
and VA), a buffer parameter, a call's return value, a field of an object, etc. — up to a
DECLARED bound (default: two levels or the producer instruction, whichever comes first).
Record each producer with VA+bytes. **If the producer is a string literal: record the
literal's content VERBATIM (strings are facts, not payloads).**

### W4. STRING/VALUE CLASSIFICATION

For each identified arg2 value: classify ARG2_VALUE_CLASS (e.g. `.rdata string literal
X` / runtime buffer / member field / unknown) with evidence. Aggregate: how many distinct
values, how many call sites, any patterns. HYPOTHESES (node name / bone / socket / marker
/ other NiAVObject name / config key) are HYPOTHESES ONLY — do NOT infer char* → bone or
name → socket (human order §32). ARG2_FINAL_SEMANTIC_ROLE may only rise above UNVERIFIED
with direct evidence (see C.4).

### W5. STATUS SYNTHESIS

The four statuses (ARG2_ABI / ARG2_PROVENANCE / ARG2_VALUE_CLASS / ARG2_FINAL_SEMANTIC_ROLE),
each with its own evidence trail; plus the **Rosetta-edge delta statement** — what this
run changed vs the standing matrix (the standing matrix is
`docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/02_ANALYSIS/SCIENCE_STATUS_MATRIX.csv`;
its arg2 rows: "arg2 ABI" = `partially observed revalidate-pending`, "arg2 provenance" =
`UNVERIFIED`, "arg2 semantic role" = `UNVERIFIED`). Write
`02_ANALYSIS/SCIENCE_STATUS_DELTA.csv` in the standing schema
(`era,item,status_before,status_after,evidence_pointer`) with ONLY the rows this run
touches; a new item this run establishes (e.g. an "arg2 value class" row) is added marked
`NEW` in status_before. Example delta wording: arg2 ABI `partially observed
revalidate-pending` → now `measured` (your own status); arg2 provenance `UNVERIFIED` →
now `measured-or-bounded`; etc. — use the measured truth, never the aspiration.

### W6. PACKAGE

- **01_RAW/** — all disassembly + census raws, including: the full FUN_0050A050
  disassembly; the three census raws (E8 / imm32 / virtual call sites with per-candidate
  rows); the timestamped git observation AT_RUN_START (HEAD/branch/origin/master local +
  ls-remote/status --short/worktree list); the identity verification records (the
  fail-closed S0 outputs). Suggested names (equivalents allowed if mapped in
  EVIDENCE_INDEX.csv): `FUN_0050A050_DISASM.txt`, `CENSUS_E8_DIRECT.txt`,
  `CENSUS_IMM32_0050A050.txt`, `VIRTUAL_CALLSITE_CENSUS.csv`,
  `AT_RUN_START_GIT_OBSERVATION.md`, `IDENTITY_VERIFICATION.txt`.
- **02_ANALYSIS/** — `ARG2_ANALYSIS.md` (the consolidated analysis: per-call-site
  receiver proofs + arg2 producer chains + value classifications; the four statuses with
  evidence; the delta statement) and `SCIENCE_STATUS_DELTA.csv` (only the rows this run
  touches).
- **03_EVIDENCE/** — `README.md` + `EVIDENCE_INDEX.csv` with generator + generator
  SHA256 per artifact (and per artifact: source path, executed command, environment,
  exact counts, independent truth source, negative controls, limitations).
- **06_REPORT/** — drafts: `REPORT.md`, `HANDOFF.md` (schema in G),
  `STAGE_ACCEPTANCE_GATES.csv` (G0-G8 self-assessed + the two standing rows
  `G14_FRESH_QC` = PENDING — owned by the fresh independent QC session, NOT the executor
  — and `G15_PERSISTENCE` = PENDING — owned by pe-master-auditor after PE-MASTER
  adjudication), and `MANIFEST_SHA256.csv` (family convention: every package file,
  SHA256, no self-row, zero missing, zero duplicate paths). Scripts live in 00_CONTROL/
  with `SCRIPT_SHA256.csv` (same convention).
- Derived artifacts carry: source path, generator path+SHA256, executed command,
  environment, exact counts, independent truth source, negative controls, limitations,
  dependency links (per-artifact in EVIDENCE_INDEX.csv).

**Calibrations and negative controls (mandatory, meaningful):**

- **CAL-1 (imm32 scanner known-answer):** your whole-file LE-dword scanner, pointed at
  0x00A7D458, must reproduce the published known-answer stores 0x00509366 and 0x0050A269
  (B.3). Tooling calibration ONLY — never adopted as this run's evidence.
- **CAL-2 (E8 census known-answer):** your E8 census machinery, pointed at FUN_005247C0,
  must find 7 call sites (published LINK30 C9). Tooling calibration ONLY.
- **NC-1 (ABI known-answer):** the B.1 dispatch-window + fallback pins must match
  byte-for-byte (this doubles as the decoder known-answer; mismatch = PIN_MISMATCH
  finding + G1 disposition — the MEASURED bytes win).
- **NC-2 (receiver disproof):** the virtual-call-site census must demonstrably REJECT at
  least one slot-3-style call site whose receiver is provably NOT SF (e.g. a +0x0C vcall
  on an RTTI-identified non-SF class) — proving the receiver-proof rule discriminates. A
  census that would accept every `FF 50 0C` pattern fails G2.
- **NC-3 (string verbatim read-back):** every .rdata/.data literal identified as an arg2
  producer gets its raw bytes re-read at the literal VA and recorded VERBATIM in the raw
  evidence (proves the pointer→content chain; no interpretation).
- **NC-4 (vtable-entry pin):** the imm32 census must find the vtable entry — the dword at
  0x00A7D464 == 0x0050A050; record the measured dword.

---

## E. GATES

The executor self-assesses; the fresh QC verifies; PE-MASTER adjudicates. Gate CSV
schema (06_REPORT/STAGE_ACCEPTANCE_GATES.csv, family convention):
`GATE,MEASURED_QUANTITY,INDEPENDENT_SOURCE_OF_TRUTH,WHY_NON_CIRCULAR,FAILURE_CASE_DETECTED,STATUS`.

- **G0_SOURCE_IDENTITY** — PASS only if: own script-measured SHA256 == pin AND size ==
  8015872 AND PE32 sanity (machine 0x014C, image_base 0x00400000) AND the AT_RUN_START
  git observation shows HEAD == BASE_SHA == origin/master == live ls-remote AND the
  untracked set == exactly {FIRSTCALL pkg, experiments/, this package} AND zero staged
  paths. MEASURED_QUANTITY: hash/size/git values. INDEPENDENT_SOURCE_OF_TRUTH: own
  hashlib + own git reads vs the 00_CONTROL pins. WHY_NON_CIRCULAR: the pins were
  recorded by a different worker (the formalizer) at a different time; the executor
  re-measures independently. FAILURE_CASE_DETECTED: any mismatch = the armed HARD_STOPs
  (SOURCE_IDENTITY_FAIL / BASE_DRIFT / FOREIGN_STAGED_PATH) with no downstream.
- **G1_ABI_REDERIVED** — PASS only if: FUN_0050A050 fully decoded entry→extent end by the
  B.5 rule; the arg2 path derived from entry (this=ECX; the arg1/arg2 stack layout; the
  exact eax def chain to the dispatch push at 0x0050A060) with VA+bytes recorded; the
  ret-N cleanup MEASURED at every ret site; the dispatch + fallback pins re-verified
  (B.1/W1) with measured bytes. A pin mismatch = PIN_MISMATCH finding; G1 FAILS if the
  arg2 path or ret-N could not be measured.
- **G2_CALLER_CENSUS_COMPLETENESS** — PASS only if: all three censuses executed with
  documented rules + denominators (E8 count, imm32 count, virtual-call-site candidates
  examined, receiver-proof outcomes per candidate, the bound declared, exhaustion states
  recorded). A hit-list without rule/denominator = FAIL. NC-2 must show the census
  discriminates (rejects a non-SF receiver).
- **G3_ARG2_PRODUCERS** — PASS only if: every verified call site's arg2 producer recorded
  with VA+bytes up to the declared bound; exhausted bounds recorded honestly; string
  literals recorded VERBATIM with VA (NC-3).
- **G4_VALUE_CLASS** — PASS only if: every identified arg2 value classified with
  evidence; distinct-value count + per-site mapping recorded; the aggregate complete
  (no unexplained verified sites).
- **G5_HYPOTHESIS_DISCIPLINE** — PASS only if: zero semantic-role promotions without
  direct evidence; the four statuses independent (each with its own evidence trail);
  hypotheses labeled as hypotheses everywhere (REPORT + ANALYSIS).
- **G6_SCOPE_HELD** — PASS only if: no downstream consumer analysis beyond the
  already-published +0x90 flow reference; no model/NIF corpus work; no P2/P3/P4 items;
  no slot-17 re-identification (0x007B5390's FUNCTION_IDENTITY stays STRONGLY_SUPPORTED —
  the locked B->A criterion; the value check [0x00A8CCF4+0x44] is allowed, decoding slot
  17 is not); TRANSFORM_TO_MODEL / MODEL_BRIDGE untouched = NOT_DEMONSTRATED.
- **G7_IMMUTABILITY** — PASS only if: the FIRSTCALL package (7 file hashes + 3 empty
  dirs, pinned in SOURCE_IDENTITIES.json) unchanged; experiments/ untouched; historical
  packages untouched; the census CSV/RAW (LINK30 SF30_WRITER_CENSUS.csv +
  SF30_WRITER_RAW.txt) untouched; zero git mutations (end-of-run git re-observation:
  HEAD == BASE_SHA, no staged entries, no commits, same untracked set + this package).
- **G8_PACKAGE_HYGIENE** — PASS only if: deterministic scripts (sorted output; no
  wall-clock inside reproducible artifacts except the mandated timestamped observation
  files); `-B` everywhere (no `__pycache__`, no `.pyc` in the package); no payloads
  (string literals from .rdata are FACTS and are allowed; NO binary dumps); interpreter +
  capstone measured provenance per the established convention (every script header
  records the python version+path and capstone `__version__` + `__file__`; the 5.0.9
  dist-info label is a known false label — trust the measured `__version__`; explicit
  `sys.path.insert` if the capstone_lib copy is needed); EVIDENCE_INDEX.csv complete
  (generator + generator SHA256 per artifact); MANIFEST_SHA256.csv complete.

**NON-PASS CLASSES:** `PASS` / `FAIL` / `NOT_APPLICABLE(reason)` / `PENDING(G14/G15)`.
**Outcome:** `PROPOSAL_READY` or `DEFECTS_FOUND` (honest list). **TIMEBOX:** soft 45
minutes. If a work item exceeds its bound: stop it, record the bound, continue the rest.
An exhausted bound is an honest recorded outcome (the affected status stays at its
evidence level), NOT a failure. **INCOMPLETE is never PASS.**

---

## F. FORBIDDEN (hard)

- No client/oracle binary execution (no process launch, no debugger, no tracer, no
  injection, no VM) — STATIC-ONLY.
- No FIRSTCALL / experiments / historical-package modification (read + hash only).
- No AUDIT_ENTRYPOINT edits.
- No wiki/canonical state changes.
- No milestone actions (no M2, no promotion, no closure, no gate-grade claims).
- Zero git mutations (no add/commit/push/stash/checkout/reset/branch; read-only git
  measurements only).
- No proprietary payloads (string literals from .rdata are FACTS and are allowed; no
  binary dumps; no .bnt/.ark/.nif corpus extraction).
- No pycache (run with -B; no .pyc in the package).
- No new milestone.
- No human prompts (the executor returns to PE-MASTER; never wakes or asks the human; no
  launcher files telling anyone to paste anything anywhere).

---

## G. FINAL_HANDOFF_SCHEMA

`06_REPORT/HANDOFF.md` must contain exactly these fields:

- RUN_ID
- BASE_SHA
- OBSERVED_HEAD_SHA
- git mutations (expected NONE)
- W1-W6 statuses
- ARG2_ABI / ARG2_PROVENANCE / ARG2_VALUE_CLASS / ARG2_FINAL_SEMANTIC_ROLE — the four
  statuses + one-line evidence each
- the caller-census denominators (E8 count; imm32 count; virtual-call-site candidates
  examined; receiver-proof outcomes)
- the distinct arg2 values found (list)
- the falsifier observed (if any)
- gates G0-G8 self-assessed
- P0/P1/P2/P3 findings
- REPORT_PATH
- HANDOFF_PATH
- EVIDENCE_PATHS
- RUN_STATUS
- HARD_STOP_REASON (expected NONE)

---

## H. PROCESS RULES

- **L22:** expected values (including every pin in B) are fail-closed pins — re-derive
  everything from the pinned EXE; a pin mismatch is a recorded finding, never silently
  adapted.
- **Script-computed hashes only** — never hand-copied hash strings as evidence; hashes
  come from in-script hashlib/Get-FileHash at measurement time.
- **-B always**; canonical interpreter
  `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (Python 3.12.7 measured at
  formalize time; re-measure and record in every script header).
- **Capstone measured provenance** in every script header: `capstone.__version__` +
  `capstone.__file__` (the 5.0.9 dist-info label is a known false label; the measured
  value at formalize time was 5.0.7 at
  `D:\Eudoria_Reconstruction\10_Scripts\python_env\Lib\site-packages\capstone\__init__.py`
  — re-measure; explicit `sys.path.insert` if the capstone_lib copy is needed).
- **The B.5 function-boundary rule applies to EVERY function this run analyzes.**
- **If interrupted:** save `00_CONTROL/RESUME_POINT.md` (what is done, what is next, the
  exact resume point, NOT_CHECKED) and return to PE-MASTER — a context boundary is a
  return to the parent, not the end of the timebox; do not claim a new session starts
  itself.
- **Claim status vs finding disposition vs gate result stay separate**; evidence status
  vocabulary: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.
  UNAVAILABLE is not NO; NOT_OBSERVED_IN_CAPTURE is not REJECTED.
- **Order of execution:** G0 identity first (S0 fail-closed in every script), then W1 →
  W2 → W3 → W4 → W5 → W6 (W2's arg2 tracing depends on W1's ABI derivation; record the
  dependency).

*Contract formalized 2026-09-14 (timestamp in GIT_OBSERVATIONS_AT_FORMALIZE.md); the
contract's own SHA256 is recorded in the formalizer's delivery notice to PE-MASTER. This
file is an IMMUTABLE INPUT for the executor.*
