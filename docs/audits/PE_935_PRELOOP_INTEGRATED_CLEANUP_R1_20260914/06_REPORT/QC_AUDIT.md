# QC_AUDIT — G14 FRESH INDEPENDENT QC — PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914

- QC_RUN_CLASS: INTERNAL_QC (G14 fresh-context QC; independent re-verification from disk)
- QC_VERIFIER: pe-master-auditor (fresh session; NOT the formalizer of this run; did NOT
  participate in execution)
- PARENT_LOOP: 2ed038db-5d2e-4e7e-b679-2d29bf57501a · MILESTONE: EU935-M1
- QC_DATE: 2026-09-14 (local) · TIMEBOX HONESTY: the 25-minute soft timebox was EXCEEDED
  (~50 min) — cause: the 11 mandatory QC checks each required own byte-level
  counter-verification of load-bearing claims (E1/E2 chains, censuses, counts, RTTI,
  NiRTTI probe, classifier re-run, hashes, git chronology). All 11 checks were COMPLETED;
  nothing was abandoned. Recorded honestly per contract.
- METHOD: independent counter-checks by the QC's own scripts (fail-closed SHA256+SIZE
  first, own PE parse, own capstone 5.0.7 — measured `__version__`/`__file__`, canonical
  interpreter `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` 3.12.7), run
  with `-B` from `C:\Users\User\AppData\Local\Temp\opencode\qc_cleanup_r1\`
  (AUDITOR_COUNTERCHECK namespace; ZERO writes outside this QC_AUDIT.md and the temp dir).
  ZERO git mutations by the QC. The client binary was NEVER executed (STATIC-ONLY held).

---

## G14 VERDICT: **QC_PASS_WITH_FINDINGS**

Every load-bearing claim of the executor REPRODUCED under the QC's own independent
measurements (full detail below). No contradiction between any disposition's evidence and
its claim. The findings register contains: ONE confirmed P2 (the historical LINK30
function-attribution layer defect — reported by the executor, now CONFIRMED and
rule-level scoped by the QC; it is an input-layer defect of the historical census, not a
defect of this cleanup run) and P3 cosmetics. None of the findings invalidates a gate.

---

## 1. G0/G1/G2 re-verification (QC's own measurements)

| Item | QC measured | Pin | Verdict |
|---|---|---|---|
| Entropia.exe SHA256 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (Get-FileHash, own assert) | same | MATCH |
| Entropia.exe SIZE | 8015872 | 8015872 | MATCH |
| HEAD | a7a6c756bc35a5b28220236e9ac649131206aeb3 | BASE_SHA | MATCH |
| branch | master | master | MATCH |
| origin/master (local ref) | a7a6c756... | BASE_SHA | MATCH |
| ls-remote origin master (live) | a7a6c756... | BASE_SHA | MATCH |
| SLOT17 branch tip (rev-parse) | 5290e79e0dc469c70605f35c125d7b727f9f7a6b | pinned tip | MATCH |
| ls-remote origin (branch, live) | 5290e79e... | pinned tip | MATCH |
| 5290e79^ (parent) | 3644e5ac9cbf7b5445861e7f5342fb8642741346 | pinned parent | MATCH |
| git status --short | exactly 3 untracked entries (FIRSTCALL pkg, cleanup pkg, experiments/), 0 modified, 0 staged | expected 3 | MATCH |
| AUDIT_ENTRYPOINT.md | NOT in status output → untouched by the executor | required | MATCH |
| SLOT17 worktree | porcelain 0 entries; HEAD == tip | clean | MATCH |
| worktree list | main repo @a7a6c75 [master]; SLOT17 worktree @5290e79 [branch] | — | consistent |
| Cleanup package file count | 28 files: 00_CONTROL 7 (3 formalizer inputs + 4 executor scripts), 01_RAW 10, 02_ANALYSIS 6, 03_EVIDENCE 2, 06_REPORT 3 | W9 claim 28 | MATCH |
| Executor's AT_CLEANUP_START git observation | present (01_RAW/GIT_OBSERVATIONS_AT_CLEANUP_START.md), timestamped 2026-09-14 15:55:38 -07:00, all components match the QC's own re-measurements | required | MATCH |

G0/G1/G2 components independently CONFIRMED.

## 2. E1 evidence chain (QC own byte reads; fail-closed SHA first)

- Bytes @0x007EAC00 (QC dump): `00 00 00 89 84 24 BC 00 00 00` — lead `00 00` (mid-stream
  `add byte ptr [eax], al` decode). REPRODUCED.
- QC conservative raw-scan ref census for 0x007EAC00 (every E8/E9 rel32 and EB rel8
  occurrence in .text whose target is the VA, PLUS whole-file imm32): **E8=0, E9=0, EB=0,
  imm32=0**. The executor's zero-reference claim REPRODUCED (raw scan over-counts relative
  to true instruction streams, so 0 in the scan is a fortiori 0 in any decode).
- Real function 0x007EA740: QC pad dump `46 10 01 5E 5D 5B C2 04 00 CC CC CC CC CC CC CC`
  (ret + CC padding = real boundary); prologue decodes as MSVC SEH frame
  (`push -1; push 0xa2128c; mov eax,fs:[0]; push eax; sub esp,0x174; push ebx/ebp/esi/edi;
  security cookie; fs:[0]=...`). REPRODUCED — this is what proves it an ENTRY.
- Bytes @0x007EA76D (QC): `8B AC 24 A0 01 00 00` = `mov ebp, dword ptr [esp + 0x1a0]`.
  REPRODUCED. ARG3 arithmetic independently re-derived: 8 pushes (0x20) + 0x174 sub =>
  esp = entry_esp − 0x194 at that point; [esp+0x1a0] = [entry_esp+0x0C] = ARG3. CORRECT.
- QC EBP-write scan (linear, entry→writer): exactly ONE EBP-writing instruction
  (0x007EA76D). No other EBP redefinition before the writer. REPRODUCED.
- Bytes @0x007EB1B3 (QC): `89 75 30` = `mov dword ptr [ebp+0x30], esi`. REPRODUCED.
- QC E8 census of 0x007EA740: exactly ONE call site 0x007EB284; E9/EB/imm32 = 0. REPRODUCED
  (the executor's "sole E8 caller, zero indirect channels" is complete — no
  address-taken/jump-table channel exists per the QC's own whole-file imm32 scan).
- QC E8 census of the caller wrapper 0x007EB210: exactly THREE call sites
  (0x007C198F, 0x007EB2FF, 0x007EB410); E9/EB/imm32 = 0. REPRODUCED (level-1 closure
  complete within the declared two-level bound).
- Level-2 arg3 provenance: the QC re-derived the push order at each call site from the
  executor's census decodes (consistent with the QC's own wrapper decode: caller A pushes
  its EBP (set `mov ebp, ecx` @0x7C1977 — an ECX-this); caller B pushes
  edx = [esp+0x14] (incoming stack-arg VALUE); caller C pushes its EBP register (frame
  state not established within the bound)). NONE of the three proves arg3 a stack address
  on every writer-reaching path; equally, non-SF-ness of arg3 is NOT proven.
- **Completeness judgment**: the executor's E1 census IS complete within its declared
  two-level bound — it enumerates ALL direct callers of 0x007EA740 (exactly 1, QC-verified)
  and ALL entry channels of the wrapper (exactly 3 E8, zero indirect, QC-verified), with
  the bound declared in the file header. What was proven: EBP = ARG3 = wrapper's EBP =
  wrapper's arg3 (an object pointer). What was NOT proven: the class/heap-ness of arg3 on
  the three level-2 paths. Under RULE V2 that is exactly NONE_PROVEN → the conservative
  default **POSSIBLE_ALIAS is CORRECT** (REJECTED was never proven; no claim that the
  write IS SF+0x30).
- **E1_FINAL_CLASS = POSSIBLE_ALIAS (case NONE_PROVEN): SOUND.**

## 3. E2 evidence chain (QC own byte reads)

- Bytes @0x0082DAC0 (QC): `00 00 00 8B 85 90 00 00 00` — lead `00 00`, mid-stream.
  QC ref census: E8/E9/EB/imm32 = **0**. Historical attribution DISPROVEN — REPRODUCED.
- Real function 0x0082DA80: pad dump `5D 5E 5B 59 C2 04 00 CC CC CC...` (ret+CC boundary);
  entry `53 55 8B E9 8B 85 90 00...` = `push ebx; push ebp; mov ebp, ecx` @0x0082DA82.
  REPRODUCED. QC EBP-write scan entry→writer: exactly ONE (0x0082DA82).
- Bytes @0x0082DB61 (QC): `66 89 4D 30` = `mov word ptr [ebp+0x30], cx`. REPRODUCED
  (16-bit width note in the reconciliation is correct — the base register is what matters).
- QC E8 census of 0x0082DA80: exactly ONE call site 0x0082E057; E9/EB/imm32 = 0.
  QC E8 census of the caller FUN_0082DFF0: exactly TWO call sites (0x006B0C63, 0x006B0F38);
  E9/EB/imm32 = 0. REPRODUCED ("sole caller, two entry sites, zero indirect channels").
- QC aligned disasm at BOTH 0x82DFF0 call sites: `lea ecx, [esp + 0x9c]; call 0x82d920`
  (ctor) then, after exactly 4 pushes (0x10), `lea ecx, [esp + 0xac]; call 0x82dff0` —
  the SAME stack slot (0x9c + 0x10 = 0xac). The reader is constructed IN PLACE as a STACK
  LOCAL on BOTH entry paths. QC disasm of FUN_0082DFF0 head: `mov esi, ecx` @0x0082E017
  (reader this -> ESI); at the call site `mov ecx, esi; call 0x82da80`. REPRODUCED.
- QC E8 census of ctor 0x0082D920: exactly TWO call sites (0x6B0C41, 0x6B0F16) — the two
  above; ctor decode: `mov dword ptr [esi], 0xa9189c` (vtable store) — REPRODUCED.
- QC independent RTTI walk of vtable 0x00A9189C: vtable-4 -> COL 0x00AB25E8 ->
  TypeDescriptor 0x00B96D3C -> name `.?AVArkNiTGAReader@@` (byte-read from .data).
  REPRODUCED.
- **Judgment**: case B is PROVEN by the QC's own decode — EBP at the writer = ECX at the
  sole call site = ESI = FUN_0082DFF0's this = the `[esp+0x9c]` stack local on BOTH entry
  paths; every writer-reaching path therefore has EBP = a stack address, which can never
  alias always-heap SF+0x30; ADDITIONALLY the object is an ArkNiTGAReader (class distinct
  from SceneFeederObject, QC-verified RTTI). **E2 REJECTED_ALIAS (case B + class
  corroboration): SOUND.**

## 4. Classifier (G8) — QC re-run

QC copied `00_Control/ebp_alias_classifier.py` byte-identically to the temp namespace
(self-SHA at run: AC63A2CB3C2CC9970031E6F69E65937A98F21A90BE3D15C9FAE85BF89C18C0AA —
identical to the package pin and the recorded raw output's generator line) and executed it
with the canonical interpreter `-B`:

- TEST 1 negative (SYNTHETIC_FIXTURE `53 56 8B D9 89 75 30`, unknown live-in EBP, no EBP
  redefinition, write [ebp+0x30],esi): output **POSSIBLE_ALIAS / NONE_PROVEN** — matches
  the package-recorded raw output. REQUIRED class returned.
- TEST 2 positive control (`55 8B EC 89 45 30`): output **REJECTED_ALIAS / case A** —
  matches. Exit code 0; "BOTH TESTS PASS".
- Fixture labelling: SYNTHETIC_FIXTURE explicitly labelled in the script, the raw output
  and the evidence index. CONFIRMED (the fixture bytes are inline synthetic; the script
  reads no game binary).
- QC source review of the checker (read to EOF): `writes_ebp` correctly excludes `push ebp`
  (reads, not writes); frame construction = adjacent `push ebp; mov ebp,esp` pair; EBP
  redefined from non-ESP => REJECTED only with caller-closure proofs, else POSSIBLE_ALIAS;
  untouched EBP => REJECTED only with frame-construction-on-all-paths proof, else
  POSSIBLE_ALIAS. Implements RULE V2 correctly. G8 CONFIRMED PASS.

## 5. P2 BLAST RADIUS — the historical LINK30 attribution defect (rule-level QC answer)

**Attribution method (census.py, read by the QC):** `function_va` = `map_lookup(va)` over
FNMAP (a lattice of 16-aligned entries "preceded by a CC/90 pad byte" whose forward
misaligned decode happens to cover the VA), falling back to
`pe.find_function_start(va, max_back=0x4000)` — the SAME backward heuristic. **Defect
mechanism (QC byte-verified):** a `0x90`/`0xCC` byte immediately before a 16-aligned VA is
NOT padding evidence — it can be an operand/disp byte of a mid-function instruction. E1:
the byte at 0x007EABFF is the 0x90 of `D9 84 24 90 00 00 00`-class stream; E2: the byte at
0x0082DABF is the 0x90 displacement byte of `... B5 90 00 00 00` (`add [ebp+0x90],esi`).
Both 16-aligned => both entered FNMAP as false entries; the wrong window then EXCLUDED
the real prologue (0x7EA740 / 0x82DA80), so "ebp untouched" was evaluated over a sub-range
of the real function — the exact failure mechanism of R-EBP-INHERITED for E1/E2.

**Rule-level classification (census.py classification logic, read by the QC):**

| Fired rule | Rows | Consumes function window? | Class |
|---|---|---|---|
| R-ESP (`stack slot (esp+0x30)`) | 2765 | NO — base==esp read from the WRITER's own operand | **FORM_ONLY** (attribution-independent) |
| R-STACK-PTR (`stack`) | 129 | YES — backward register trace inside the attributed window | ATTRIBUTION_DEPENDENT |
| R-CTOR-OTHER (`other-class this (vtable ...)`) | 104 | YES — `fn_vtable_store_class(derive_body(fs))` over the attributed body | ATTRIBUTION_DEPENDENT |
| R-ZERO (`null base`) | 18 | YES — backward trace in window | ATTRIBUTION_DEPENDENT |
| R-LEA-STACK (`stack object`) | 3 | YES — backward trace in window | ATTRIBUTION_DEPENDENT |
| R-EBP-INHERITED (`caller stack (inherited ebp)`) | 2 | YES — EBP-redefinition scan in window | ATTRIBUTION_DEPENDENT — **both rows DISPROVEN (E1/E2)** |
| R-IMM-STATIC (`static data address`) | 1 | YES — backward trace | ATTRIBUTION_DEPENDENT — already superseded by AMEND_R2 (moot) |
| R-CONT-FIELD (`container+0x30`) | 1 | YES — SF_SLOTS_BY_FN built via find_function_start + trace | ATTRIBUTION_DEPENDENT |

Histogram QC-recomputed from the CSV `receiver_provenance` column: 2765/129/104/18/3/2/1/1
— exactly the historical fired census (the QC independently reproduced R-CTOR-OTHER = 3023
− 2919 = 104). The 618 POSSIBLE rows (`unknown` 596 + `unknown (ebp repurposed)` 22) are
the conservative default class — a wrong window there can only have made rows MORE
conservative or left the class unchanged; the 2 PROVEN rows are anchor-based (the
find_function_start docstring itself notes classification never rests on it alone for
PROVEN rows).

**Exposure statement (for PE-MASTER adjudication):** up to **257 REJECTED rows**
(129+104+18+3+2+1) whose rejection reasons performed window analysis at an
attribution-derived function start are the exposure class of this defect; the 2765 R-ESP
rejections are form-only and attribution-independent (SAFE). Failure modes in the exposed
class: a window that starts INSIDE the real function can MISS the true last register
definition (stale-definition REJECTED, or conservative fall-through to POSSIBLE — the
latter harmless).

**QC spot-check (declared SAMPLE, not a census; deterministic stride):** 10 rows sampled
from the attribution-dependent REJECTED pool + 5 from the R-ESP pool. QC disassembled each
row's `function_va` lead bytes and preceding bytes: **15/15 point at PLAUSIBLE function
starts** (16-aligned, preceded by CC/ret+CC padding, decoding to real prologues — SEH
frames, `sub esp/push`, etc.); **0 mid-instruction/padding-only attributions** in the
sample. The E1/E2 defect did NOT appear in the QC sample. Honest conclusion: the defect
class is REAL (mechanism byte-proven, 2/2 occurrences in R-EBP-INHERITED) but its
frequency on other rows is NOT demonstrated by N=15; the executor's "exposure UNKNOWN;
recommend census-wide attribution re-derivation" stands, now with the rule-level scoping
above.

## 6. Counts arithmetic (G9) — QC recompute from the CSV

QC parse of the READ-ONLY `SF30_WRITER_CENSUS.csv`: 3643 rows, unique writer_va;
classification self-count **2 PROVEN_SF30_WRITER / 618 POSSIBLE_ALIAS / 3023 REJECTED_ALIAS
/ 0 UNRESOLVED** (executor's CSV self-derivation reproduced). Deltas: AMEND_R2
(0x0040525B REJECTED->POSSIBLE: 2/619/3022/0) + this run E1 (0x007EB1B3
REJECTED->POSSIBLE) + E2 unchanged => **2/620/3021/0; 2+620+3021+0 == 3643** ASSERTED
OK. CSV row spot-verified verbatim for 0x007EB1B3 (function_va 0x007EAC00, REJECTED_ALIAS)
and 0x0082DB61 and 0x0040525B. LINK30 hashes: QC-measured NOW
CSV 71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0 (352206 B) /
RAW 64402A73013B52943E10AE17BB115F466A0D3BEF98AA3835915CF3C1CD572248 (2492537 B) ==
pins == the executor's AT_START and AT_END records — **before == after == now**.
The derived counts are NOT hard-coded (per-row derivation in
02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md is consistent with the QC-verified byte
evidence). G9 CONFIRMED.

## 7. SLOT17 AUD-F1..F7 verifications (QC own evidence)

- **F1/F7 (chronology)**: QC `git log --format` — a7a6c756 authored/committed
  2026-09-14 14:40:54 -0700; 5290e79 at 15:11:43 -0700; QC `git reflog master` — a7a6c756
  @14:40:54, 3644e5ac @10:12:52. CONFIRMED: local master was already a7a6c756 at SLOT17
  publication; RUN_START (14:31) master==3644e5ac TRUE; the temporal-scope erratum
  (ACCEPTED) is CORRECT; REMOTE_HEAD_CHRONOLOGY = UNRESOLVED is the honest reading (local
  reflog cannot date the remote ref change). Branch parent pin 3644e5ac QC-verified.
- **F2 (census)**: QC `git ls-tree -r 5290e79` per-directory count of the SLOT17 package
  paths: **00_CONTROL 6, 01_RAW 3, 02_ANALYSIS 6, 03_EVIDENCE 16, 06_REPORT 4, TOTAL 35**
  — exactly the pin; the SLOT17 HANDOFF's "03_EVIDENCE 15, 06_REPORT 5" is the confirmed
  erratum. ACCEPTED disposition CORRECT.
- **F3 (mtimes)**: QC Get-Item LastWriteTime of the five pin files:
  entropia_rtti_probe.py 14:11:34, parse_coff_vtable.py 14:12:14,
  entropia_disasm_7b5390.py 14:18:25, coff_disasm_symbol.py 14:24:07,
  GB12_SOURCE_LOCATORS.md 14:26:37 — ALL < 14:31 (carried); spot-check of a regenerated
  file (GB12_NINODE_OBJ_VTABLE_DUMP.json 14:53:20 >= 14:39). MATCHES the executor's
  35-file mtime table and the expected pin. PARTIALLY_ACCEPTED disposition CORRECT (the
  REPORT's unqualified "All evidence was regenerated" is the overstatement; mtime is
  corroboration; content stands on re-measurements).
- **F4 (PE header)**: QC own struct reads after fail-closed SHA: e_lfanew 0x120, opt start
  0x138, magic 0x10B, ImageBase@opt+0x1C = 0x00400000, SectionAlignment@opt+0x20 = 0x1000,
  DllCharacteristics@opt+0x46 = 0x0000; section table parsed (.text/.rdata/.data/.tls/
  .rsrc). The standard IMAGE_OPTIONAL_HEADER32 layout holds EXACTLY; the "+4 shifted"
  docstring claim is factually wrong. REJECTED_WITH_EVIDENCE CORRECT.
- **F5 (oracle identity)**: QC Get-FileHash NiMain.lib = FF4519AFD2475D9A6E71A35E5DB6B0F5
  A0B7E9E86EC3662C6A340DA19BA06597, size 3073590 == pins; QC census of
  `D:\gamebyroengine\extracted\Gb112_eval\`: Documentation ONLY, containing HTML/,
  GbEvaluationDocumentationSetup.dat (1224), GbEvaluationUninstaller.exe (124886),
  license.txt (286), Unwise32.exe (164864) — == the AT_FORMALIZE census. "Gb112_eval =
  full same content" is FALSE on disk. REJECTED_WITH_EVIDENCE CORRECT.
- **F6**: record-only disposition of chat-only wording; no verbatim reconstruction;
  corrected temporal scoping recorded. Consistent with the F1 evidence; nothing to
  contradict. ACCEPTED disposition APPROPRIATE.

## 8. GB12 / NiRTTI (G4/G5)

- QC re-parsed `03_EVIDENCE/GB12_NINODE_OBJ_VTABLE_DUMP.json` (SLOT17 package, read-only)
  with its own script: NiNode vtable slot_count 34; **slot 13 GetGroup, 14 SetGroup,
  15 UpdateControllers, 16 UpdateNodeBound, 17 ApplyTransform, 18 GetObjectByName,
  19 SetSelectiveUpdateFlags** (mangled symbols verbatim in the QC output) — the expected
  sequence REPRODUCED from the raw JSON; the prose-table erratum (duplicated
  UpdateControllers@13&15 / UpdateNodeBound@14&16 in CLASS_HIERARCHY_AND_VTABLE_MAP.md) is
  thereby confirmed as claimed; headline 17/18/19 unchanged.
- QC re-ran the bounded probe logic with its own byte scan: the pattern `B9 70 72 BA 00`
  has EXACTLY ONE whole-file occurrence @ file 0x66C33A = VA 0x00A6C33A (.text). QC
  capstone decode of the context: `0x00A6C330 push 0xba7224; 0x00A6C335 push 0xa8d8bc;
  0x00A6C33A mov ecx, 0xba7270; 0x00A6C33F call 0x7199e0; 0x00A6C344 ret` — int3-padded
  standalone thunk. QC read the literal at 0x00A8D8BC in .rdata: **"NiAVObject"**.
  QC ALSO decoded the NiNode initializer at 0x00A6C200: `push 0xba7270; push 0xa8ce00
  ('NiNode' — QC-verified literal); mov ecx, 0xba7218; call 0x7199e0; ret` — the SAME ctor,
  and the NiNode initializer's BASE push is exactly 0x00BA7270, i.e. the two initializers
  mutually corroborate the class hierarchy (NiNode's base = the NiAVObject NiRTTI).
- **QC judgment on the upgrade**: `*(NiRTTI*)0x00BA7270 = NiRTTI("NiAVObject", base
  0x00BA7224)` is proven DIRECTLY from the static-initializer call-site bytes — the SAME
  evidence class that made 0x00BA7218 = NiNode NiRTTI CONFIRMED (identical thunk shape,
  identical ctor 0x7199E0, name literal in .rdata, second static use of 0xBA7218 in the E1
  wrapper `cmp eax, 0xba7218` @0x007EB260 as additional corroboration). The contract's
  W6.4 explicitly authorized this upgrade; the bound was respected (one pattern + one
  context window). **CONFIRMED is JUSTIFIED**, with the stated evidence class: proven from
  initializer call-site bytes; the object STORAGE at 0xBA7270 lies in the .data
  virtual-only tail (runtime-constructed, not in file bytes) — the same caveat as the
  NiNode case, correctly disclosed in the errata and the report.

## 9. F5 disposition (G10) — QC re-verification

- QC re-hashed ALL 7 FIRSTCALL files: 7/7 == the SOURCE_IDENTITIES.json pins (RUN_CONTRACT
  9E000603..., SOURCE_IDENTITIES 088A4EE4..., run_state D7F74288..., slot17_core 02D58F8B...,
  slot17_run C4802B2A..., .pyc FF83444B..., SLOT17_BODY_RAW 2EABC45F...) — BEFORE==AFTER==NOW
  from the QC's own measurements; 3 empty directories confirmed by the executor's records
  (directory structure itself QC-observed via the file walk).
- QC read FIRSTCALL `01_RAW/SLOT17_BODY_RAW.txt` (read-only) and independently verified
  the supersession facts against SLOT17's re-measurements AND its own bytes: (2) NiNode
  RTTI .?AVNiNode@@ vtable 0x00A8CCF4 — consistent with SLOT17 fingerprint; (3) slot17
  dword = 0x007B5390 — consistent; (5) the 0x7B5390 instruction sequence (push ebx;
  mov ebx,[esp+8]; push edi; push ebx; mov edi,ecx; call 0x7bf220 @0x7B5399) — IDENTICAL
  in the SLOT17 fingerprint; (6) helper 0x7BF220 NULL-guards + byte-pair strcmp + ret 4 —
  consistent; (4) the 6 dispatch pins — QC read the bytes @0x50A057 itself:
  `8B F1 74 2C 8B 4E 30 8B 11 50 8B 42 44 FF D0` — all six pinned sequences present
  byte-exact (the `74 2C` between is an unpinned branch, consistent with both listings);
  (1) the SF calibration chain is re-derivable by the same RTTI method family (SLOT17's
  chain probe). **6/6 consistent, 6/6 strictly subsumed: CONFIRMED.**
  F5_SCIENCE_STATUS = SUPERSEDED_SCIENTIFICALLY_BY SLOT17 R1 (5290e79) — appropriately
  derived; F5_PROCESS_STATUS = PARKED_UNAUTHORIZED_ATTEMPT recorded verbatim-faithful.

## 10. Package hygiene (W9)

- 28 files QC-counted (7/10/6/2/3). EVIDENCE_INDEX.csv covers every executor artifact
  (10 raw + 6 analysis + 4 scripts + 3 report drafts + README + index) with generator +
  generator SHA256; the 3 formalizer control inputs are contract inputs (not executor
  artifacts) — defensible scope.
- NO `__pycache__`, NO `.pyc` anywhere in the cleanup package (QC recursive scan).
- No proprietary payloads: all 01_RAW files are text listings/records (max 45.8 KB
  disasm listing); no binary dumps. STATIC-ONLY held (no game/oracle binary executed by
  anyone in this chain; NiMain.lib never executed).
- REPORT/HANDOFF/STAGE_ACCEPTANCE_GATES internally consistent: counts 2/620/3021/0 sum
  3643 everywhere; gates G0-G13 self-assessed PASS WITH measured quantities and
  independent sources declared; G14/G15 correctly PENDING. SCIENCE_STATUS_MATRIX: all 15
  standing statuses preserved EXACTLY (GetObjectByName stays STRONGLY_SUPPORTED — the
  locked B->A criterion held; +0x90 stays CONFIRMED STRUCTURAL); the ONLY upgrade is the
  NiRTTI 0x00BA7270 semantic identity per the authorized bounded probe; new rows (E1/E2,
  0xBA7218 second-use, canonical counts) all cite evidence pointers. NO unauthorized
  upgrades.

## 11. Historical immutability (G11) — QC summary

- FIRSTCALL 7/7 hashes == pins (QC) — untouched.
- LINK30 CSV/RAW == pins (QC) — untouched (before==after==now).
- SLOT17 branch tip local == remote == 5290e79; parent == 3644e5ac (QC) — untouched.
- SLOT17 worktree clean, HEAD == tip; QC spot-hash of 4 package files
  (GB12_NINODE_OBJ_VTABLE_DUMP.json, CLASS_HIERARCHY_AND_VTABLE_MAP.md, HANDOFF.md,
  ENTROPIA_NIRTTI_STATIC_INIT.txt) — all present in the worktree package's
  06_REPORT/MANIFEST_SHA256.csv — untouched.
- `experiments/` still untracked, no changes (QC git status).
- AUDIT_ENTRYPOINT.md NOT modified (not in git status; no modification recorded).
- ZERO git mutations by the executor (QC git status/refs identical to AT_FORMALIZE pins).

---

## FINDINGS REGISTER

**P2-1 (CONFIRMED, input-layer — for PE-MASTER adjudication; matches the executor's own
P2): historical LINK30 function-attribution layer can attribute writers to non-function
VAs.** Evidence: E1 (0x007EB1B3 -> 0x007EAC00) and E2 (0x0082DB61 -> 0x0082DAC0) both
mid-stream (QC byte-proof; zero E8/E9/EB/imm32 references). Mechanism: 16-aligned +
preceded-by-0x90/0xCC byte is treated as entry evidence, but 0x90/0xCC can be operand/disp
bytes (QC byte-proof at both sites). Blast radius (rule-level): 2765 R-ESP rejections are
FORM_ONLY (safe); up to **257 REJECTED rows** are ATTRIBUTION_DEPENDENT (R-STACK-PTR 129,
R-CTOR-OTHER 104, R-ZERO 18, R-LEA-STACK 3, R-EBP-INHERITED 2, R-CONT-FIELD 1; R-IMM-STATIC
1 already superseded); 618 POSSIBLE rows are conservative-class. QC sample N=15 (10
attribution-dependent + 5 form-only): **15/15 plausible function starts, 0 defects found in
the sample** — SAMPLE, not a census; the exposure on other rows remains UNKNOWN. Skutek:
any of the 257 exposed REJECTED rows could in principle be a stale-definition rejection
(conservative failures fall to POSSIBLE, which is safe). Poprawka (proposed, NOT executed):
a future authorized census-wide attribution re-derivation with a padded-boundary-verified
FNMAP (align + full pad-run + call-target lattice cross-check) — as the executor already
recommended. Revalidation predicate: re-derive function_va for the 257 exposed rows from a
verified boundary map; any row whose rejection reason does not survive re-derivation at
the TRUE function start moves REJECTED->POSSIBLE via an append-only sidecar.

**P3-1: HANDOFF.md raw-file count slip.** "01_RAW/ (9 raw files)" — the directory holds
10 (QC count; EVIDENCE_INDEX.csv correctly lists all 10). Cosmetic; the index is
authoritative and correct.

**P3-2: IDENTITY_VERIFICATION_AT_END.txt section-3 header says "byte-identity (BEFORE)"**
inside the END record — a copy-paste label slip; the content is the END re-measurement
(timestamp 2026-09-14T16:09:10; values == pins == QC's own now-measurements). No
evidentiary ambiguity in practice.

**P3-3: cross-reference drift in SLOT17_AUDIT_FINDINGS_DISPOSITION.md.** It cites errata
as "SLOT17_ERRATA.md §E1/§E2/§E3" while the errata file's actual sections are §4
(AUD-F1/F7), §5 (AUD-F2), §3 (AUD-F4). Content findable; labels drifted.

**P3-4: mojibake em-dashes in ebp_alias_classifier.py string literals** (and hence in the
raw test output's decorative lines): the source contains double-encoded UTF-8 sequences
from an editing artifact. The QC verified the OUTPUT file decodes as valid UTF-8 and that
every load-bearing line (fixture hex, CLASSIFIER OUTPUT, CASE, REQUIRED, G8 verdict) is
pure ASCII and matches the QC's own re-run exactly. Classification logic unaffected.

**P3-5 (disclosed by the executor, QC-checked): timebox overrun** — the executor reported
~70 min vs the 40-min soft timebox (honest disclosure in REPORT §0/§9); the QC's own
25-minute soft timebox was also exceeded (~50 min, disclosed in this header). No work
item was truncated by either.

**P3-6 (disclosed by the executor, QC-checked): START-record generator provenance** —
01_RAW/IDENTITY_VERIFICATION_AT_START.txt was generated by script revision 83B392E3...,
the END record by 1E28AF12...; disclosed in REPORT §9 and EVIDENCE_INDEX; measurements
identical (QC re-measured everything independently — see §6/§9/§11 above).

## COVERAGE HONESTY — what the QC verified PERSONALLY vs accepted

PERSONALLY VERIFIED (own bytes/scripts/commands): Entropia SHA+SIZE; PE optional header +
section table; E1/E2 byte chains INCLUDING all four cited VAs' bytes, both disproof
censuses (E8/E9/EB/imm32), both real-entry boundaries, both EBP-redefinition sites, both
writer byte sequences, EBP-write scans entry->writer, the 0x7EA740/0x7EB210/0x82DA80/
0x82DFF0/0x82D920 call-target lattices (1/3/1/2/2 sites, all matching), both stack-local
ctor constructions, the ArkNiTGAReader RTTI walk; the classifier re-run (both fixtures);
the CSV parse/counts/provenance histogram; the 15-row function_va spot-check; GB12 JSON
slots 13-19; the NiRTTI bounded probe re-run (sole hit, thunk decode, both name literals);
the 6 dispatch pins @0x50A057; FIRSTCALL 7/7 + NiMain.lib + Gb112_eval hashes/censuses;
LINK30 CSV/RAW hashes; all git identities incl. live ls-remote, reflog chronology, ls-tree
per-directory census, worktree cleanliness, untracked set; AUD-F3 mtimes; SLOT17 4-file
spot-hash vs its MANIFEST; package 28-file census; pycache/payload scan; the science
status matrix vs the standing pins.

ACCEPTED FROM EXECUTOR ARTIFACTS (not independently re-executed, but consistency-checked
and non-load-bearing or independently corroborated): the full E1/E2 disasm listing files
to EOF (load-bearing content re-derived by the QC's own decode; listings spot-consistent);
generator sources `e_ebp_reval.py`, `cleanup_verify_identities.py`,
`nirtti_bounded_probe.py` were NOT read to EOF — instead, ALL their load-bearing outputs
were independently re-measured (the strongest counter-check); the executor's AT_START/AT_END
identity records (values independently re-measured now); the SLOT17 HANDOFF/REPORT verbatim
claim quotes inside the disposition doc (the load-bearing refutations are the QC's own
measurements); SLOT17 fingerprint facts beyond the supersession spot-checks;
GIT_OBSERVATIONS_AT_FORMALIZE.md (formalizer input, not executor work); the F6 chat-text
record (not on disk by definition; nothing to contradict).

NOT_CHECKED: GB12_CHAIN_OBJ_VTABLE_DUMP.json contents in depth (QC confirms it exists,
is BOM-prefixed valid JSON, and is NOT claim-bearing for any cleanup statement — the
slot-sequence claims rest on GB12_NINODE_OBJ_VTABLE_DUMP.json, QC-verified); the 10-raw
listings' full EOF read as above; remote-side git history beyond ls-remote head
comparisons (REMOTE_HEAD_CHRONOLOGY stays UNRESOLVED, honestly recorded).

## G14 CLOSURE

**G14 = QC_PASS_WITH_FINDINGS.** The E1/E2 byte chains reproduce; the classifier tests
reproduce; the counts sum and match the pins; no historical artifact changed; no
disposition's evidence contradicts its claim. The P2 is a confirmed INPUT-LAYER defect of
the historical LINK30 census (reported by the executor, scoped rule-level by the QC,
sampled N=15 with zero additional occurrences) — it does not invalidate this cleanup's
derivation (which re-derived the two affected rows from physical bytes) but MUST be
adjudicated by PE-MASTER together with the derived canonical counts (3643 = 2/620/3021/0)
and the proposed future census-wide attribution re-derivation. G15 (persistence) remains
PENDING for the persistence worker after adjudication.

— pe-master-auditor (G14 fresh QC), 2026-09-14
