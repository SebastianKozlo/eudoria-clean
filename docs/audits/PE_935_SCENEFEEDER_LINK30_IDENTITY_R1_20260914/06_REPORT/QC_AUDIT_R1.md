# QC_AUDIT_R1.md — PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (INTERNAL_QC, round 1)

- QC_RUN: fresh-context INTERNAL_QC by pe-master-auditor (independent of the execution;
  the formalizer was PE-MASTER relaying a human contract).
- AUDITED RUN: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (RUN_CLASS LOAD_BEARING,
  executor pe-reconstruction, STATIC-ONLY, era PCG_9_3_5, milestone EU935-M1).
- METHOD: NO re-execution of the executor's scripts. Own PE parser, own RTTI walker,
  own sweep implementation, own CSV/raw parsers, own byte reads at every cited VA.
  Only the capstone 5.0.7 decoder library (same install path) is shared — my probe
  code is independent. Probe scripts + outputs: `00_CONTROL/qc_probe/` (established
  convention; listed with SHA256 at the end of this report).
- QC date: 2026-09-14. ZERO git mutations by QC (verified before and after).

---

## 1. S0 — source/base fail-closed (own measurement)

| item | result |
|---|---|
| HEAD | `1a490eed4ca2b295e78cd3cf851a08ac9c93930b` == BASE_SHA pin |
| origin/master (local ref) | `1a490eed…` == pin |
| `git ls-remote origin master` | `1a490eed…` == pin (remote equality verified against the actual remote) |
| git status | only `?? docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/` (this run's own untracked package, by-design per the disclosed G0 dirty-path note) + foreign `?? experiments/` (untouched by QC) |
| git diff vs HEAD | empty — no tracked file modified; executor made ZERO git mutations (claim CONFIRMED) |
| Entropia.exe SHA256 | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` == pin |
| Entropia.exe size | 8015872 == pin |
| PE facts (own header walk) | machine 0x014C, opt_magic 0x010B, image_base 0x00400000, DLLCHARACTERISTICS 0x0000 (no DYNAMIC_BASE) |

**S0 = PASS.**

## 2. Administrative correction verification (contract line 40)

Own measurements of the previous run PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914:
27 package files (counted), 26 manifest data rows + manifest self-exclusion (counted),
and its publication commit `1a490ee` (== this run's BASE_SHA) contains exactly 28 paths
= 27 package paths + root `AUDIT_ENTRYPOINT.md` (git show --name-only, counted).
The correction is STATED in RUN_CONTRACT.md:40 and SOURCE_IDENTITIES.json:43 and is
factually correct. The old wrong figures ("26 package files / 25 manifest rows") occur
in the new package ONLY inside the correction statements themselves (contract:40,
identities:43, finalize.py:245) — never used as facts. CONFIRMED.

## 3. Claim matrix — independent verification (C1–C12)

**C1 census.** My own re-implementation of the documented enumeration rule (linear
capstone 5.0.7 sweep of full .text 0x00401000..0x00A75000, candidate = any decoded
insn with a WRITE mem-operand disp==0x30, bad-byte restart at last_end+1) reproduces
the sweep **exactly**: 2,266,698 instructions decoded, 64 restarts, **3643 candidates**
(qc3). My own CSV parse: 3643 rows, PROVEN 2 / POSSIBLE_ALIAS 618 / REJECTED_ALIAS 3023 /
UNRESOLVED 0; unique writer_va, no duplicates. Raw file contains exactly 3643 unique
`###` per-candidate blocks, 1:1 and in the same order as the CSV rows. Every one of the
3643 CSV instruction strings equals my own decode of the physical bytes (0 mismatches);
the CSV candidate set == my candidate set (0 missing / 0 extra). Base-register
distribution reproduced exactly (eax=80, ebp=25, ebx=24, ecx=30, edi=76, edx=6, esi=637,
esp=2765; sum 3643). The 2,266,698 figure is the documented sweep's decoded-insn count —
now independently derived. **CONFIRMED.**

**C2 writer#1 @0x005093C3 (SF ctor FUN_00509330).** Own byte reads at every cited VA:
0x00509357 `8B E9 mov ebp,ecx`; 0x00509366 `C7 45 00 58 D4 A7 00 mov [ebp],0xa7d458`
(SF vtable store → ebp==SF-this); 0x00509376 `68 18 01 00 00 push 0x118`;
0x005093A0 `E8 1F 40 45 00 call 0x95d3c4` (own IAT walk → `MSVCR80.dll.??2@YAPAXI@Z`
operator new); 0x005093B6 `8B C8 mov ecx,eax`; 0x005093B8 `E8 43 CC 2A 00 call 0x7b6000`;
**0x005093C3 `89 45 30 mov [ebp+0x30],eax`**; 0x005093C8 `83 40 04 01 add [eax+4],1`
(refcount++ at block+4). Receiver-register soundness re-derived: ebp has exactly ONE
definition in the ctor stream up to the write (the entry `mov ebp,ecx`) — the PROVEN
classification cannot rest on a stale register. Block ctor FUN_007B6000 window verified
aligned: 0x007B6023 `8B F1 mov esi,ecx`; 0x007B6029 `E8 A2 A2 00 00 call 0x7c02d0`;
**0x007B6041 `C7 06 F4 CC A8 00 mov [esi],0xa8ccf4`** (primary vtable at block+0);
0x007B605E `C7 86 E0 00 00 00 E0 CC A8 00 mov [esi+0xE0],0xa8cce0` (secondary vtable at
block+0xE0); 0x007B609F `8B C6 mov eax,esi`. **CONFIRMED.**

**C3 writer#2 @0x0050A2D1 (SF dtor body FUN_0050A240).** Own bytes: 0x0050A263 `8B F1
mov esi,ecx`; 0x0050A269 `C7 06 58 D4 A7 00 mov [esi],0xa7d458`; release protocol
0x0050A2BD `8B 4E 30`, 0x0050A2C0 `3B CB`, 0x0050A2C4 `83 41 04 FF` (refcount--),
0x0050A2C8 `75 07`, 0x0050A2CA `8B 01`, 0x0050A2CC `8B 50 04` (vtable slot 1),
0x0050A2CF `FF D2 call edx`; **0x0050A2D1 `89 5E 30 mov [esi+0x30],ebx`** (ebx=0 from
`xor ebx,ebx` @0x0050A272); 0x0050A2D4 `8B 4E 30` re-read. esi has exactly ONE
definition in the dtor body up to the write. Dtor-body call from vtable slot 0 verified:
0x0050A463 `E8 D8 FD FF FF call 0x50a240` inside FUN_0050A460 (slot 0). SF vtable slot
dwords verified: [0x00A7D458..0x00A7D46C] = 0x50A460/0x5090A0/0x5090B0/0x50A050/
0x5090C0/0x509580. **CONFIRMED.**

**C4 RTTI walk (own walker, every dword from physical bytes).**
Calibration: [0x00A7D454]=0x00AA12B8 (raw `b812aa00`); COL 0x00AA12B8
sig=0 off=0 cd=0 ptd=0x00B78834 pchd=0x00AA12CC; TD 0x00B78834 vfptr=0x00A98110
spare=0; name = `.?AVSceneFeederObject@@` — calibration reproduces the known answer.
Link: [0x00A8CCF0]=0x00AAEEC8 (raw `c8eeaa00`); COL 0x00AAEEC8 sig=0 off=0 cd=0
ptd=0x00B936C8 pchd=0x00AAEEDC; TD name bytes `2e3f41564e694e6f64654040` =
**`.?AVNiNode@@`**. Secondary: [0x00A8CCDC]=0x00AAEE78 → ptd 0x00B93694 →
`.?AV?$NiTPointerList@PAVNiDynamicEffect@@@@`. All three walks byte-confirmed.
NiNode vtable extent from 0x00A8CCF4: **47** code-pointer entries (own count);
0x007B6000 is NOT among the entries (own check). ONE LABEL DEFECT: the name is at
**TD+0x08** (correct MSVC TypeDescriptor layout; the executor's walker code reads +8
and the calibration PASS proves it), but the raw/report label says "TD+0x0C" — see
finding P2-2 (bytes correct, label wrong; the label originates in the contract itself,
RUN_CONTRACT.md:59). **Claim CONFIRMED (label defect separately reported).**

**C5 positive control.** Own bytes: 0x0050A057 `8B F1`, 0x0050A05B `8B 4E 30`,
0x0050A05E `8B 11`, 0x0050A061 `8B 42 44`, 0x0050A064 `FF D0`; ECX clobber scan of
0x50A05E..0x50A064 (own decode: `mov edx,[ecx]`, `push eax`, `mov eax,[edx+0x44]`)
finds no ECX definition → receiver of CALL [vtable+0x44] == ECX == [ESI+0x30] ==
[SF+0x30]. The window naturally contains the `call 0x437f70` instruction @0x50A075
(window re-read, contract-allowed; no callee analysis anywhere in the package).
**CONFIRMED (PASS).**

**C6 NEXT_SEAM value + no-decode.** Own read: [0x00A8CCF4+0x44]=[0x00A8CD38] =
**0x007B5390** (in .text). My full-package census of every occurrence of 0x007B5390 /
0x437F70 / 0x82B5A0: all occurrences are (a) the contract text, (b) the recorded slot-17
VALUE (RTTI raw:27, WRITER_RAW:142, census_state.json, HANDOFF, REPORT next-seam
mentions), (c) finalize.py's own gate-machinery scan strings, and (d) the positive-control
window's `call 0x437f70` instruction line. Zero disassembly listings, zero analysis of
any forbidden callee. Additionally verified with my own function-extent derivation
(boundary-only): **0 census rows fall inside** my extents of 0x00437F70 (len 0x77),
0x0082B5A0 (len 0x47), 0x007B5390 (len 0x51) — the nearest census row is +852 past
0x7B5390's entry, far outside any plausible extent. **CONFIRMED.**

**C7 scope census (independent).** My own census of all 17 package files: every
occurrence of MODEL_BRIDGE_CONFIRMED / TRANSFORM_TO_MODEL (14 lines) is negative /
forbidden-context; **zero claim-context occurrences**. No "MODEL_BRIDGE" or
"TRANSFORM_TO_MODEL" result claim exists. NOT_DEMONSTRATED statements present and
required (REPORT:48,149,159; HANDOFF:39). Era label PCG_9_3_5 present in REPORT,
HANDOFF, SOURCE_IDENTITIES, README; STATIC-ONLY stated everywhere; RUN_ID in the raw
census/RTTI files. (Era-label gaps in the remaining evidence artifacts: finding P3-5.)
**CONFIRMED** (with P3 hygiene notes).

**C8 the 618 POSSIBLE_ALIAS bound (THE CRITICAL ONE)** — see §5 assessment below and
the sampling evidence here: 618 rows across 562 distinct non-SF-proven functions;
**zero POSSIBLE rows inside the 19 F_SF functions** (inside F_SF: exactly 2 PROVEN +
7 REJECTED, all receiver-verified by me — 6 esp-stack writes and 1 container-field
write 0x0044D5F0 `mov [esi+0x30],edx` where esi is the container this, SF slot at
+0xC). 12-row sample across 12 distinct functions: every sampled row's raw `why`
matches the class definition (base register of unknown provenance in a function not
proven to ever receive SF; two FPO-ebp-repurposed variants). My own window decodes of
the samples agree (e.g. 0x006E1A57/0x007894B6: `mov esi,ecx` thiscall-this copies in
unknown-class functions — the exact unbounded pattern). REJECTED sampling: my own
reason census over all 3023 raw `why:` lines sums exactly to 3023 with distribution
R-ESP 2765 / R-STACK-PTR 129 / R-CTOR-OTHER 104 / R-ZERO 18 / R-LEA-STACK 3 /
R-EBP-INHERITED 2 / R-IMM-STATIC 1 / R-CONT-FIELD 1; sampled rows verified against
their windows (e.g. R-ZERO 0x007A929C preceded by `xor eax,eax` @0x007A9296 — own
decode; R-IMM-STATIC 0x0040525B base=edx from fixed immediate). Adversarial deep-check
of 4 R-CTOR-OTHER rows (full-body, own decode): in each, the claimed other-class
vtable store via the base register exists before the candidate (e.g. fn 0x00402E90
stores 0x00A7973C `.?AVArkReleaseClientApplication@@` via esi) and the base has
exactly ONE definition in the whole body (the entry `mov esi,ecx`) → the rejection is
sound for the samples; the rule's documented assumption (SF never passed as this to
another class's ctor) has no counter-evidence in any SF-context function. **The bound
is structurally sound and honestly documented; what it does NOT cover is the
interprocedural channel — see §5.**

**C9 gates G0–G5.** All six PREDICATE lines read and checked against the executed
mechanism (census.py + finalize.py, both read to EOF). G0: exact identity + dirty-path
set as disclosed (the package dir is an expected untracked path because the executor
is forbidden git mutations while required to create the package — the deviation from
the contract's literal "only experiments/" is disclosed in RUN_CONTRACT:122-127;
sensible). G1: byte re-asserted at gate time (finalize.py:57-60) + text check.
G2: vocab/enum/counts/coverage checks match my own recount. G3: hop-table presence
+ RESOLVED strings. G4: text checks + independent re-walk at gate time
(finalize.py:105-108). G5: mechanism findings P2-3/P3-7 below (detector permissive;
extent computation decodes forbidden bodies in memory) — but the **asserted results
are independently TRUE** (my own census: 0 claim-context, 0 slot-17 listings,
0 rows inside forbidden ranges). Negative controls all actually ran and are
independently reproduced: RTTI calibration (assert-first, fail-closed — census.py:81-83),
absolute-reference test (0 occurrences — my own scan agrees), combined-offset scan
(0 hits — my own rescan at the 5 container functions agrees), bulk-init non-coverage
(own decode: rep movsd #1 target `lea edi,[esp+0x18]` @0x5093E0 + `mov esi,0xb93c80`
+ `mov ecx,9` @0x509458; rep movsd #2 `lea edi,[ebp+0x4c]` @0x509462 + `mov ecx,9`
@0x509465 → SF+0x4C..0x70; NEITHER covers +0x30), classifier discipline (3023 per-row
reasons), scope census. **All six PASS verdicts stand.**

**C10 COUNTER_ARITHMETIC.** Every printed count re-derived by my own tools: census
counts (2/618/3023/0, total 3643 — CSV parse), raw block count (3643 — regex census),
base-register distribution (exact match), manifest rows 16 == 17 executor files minus
manifest self (L12 precedent, self-exclusion held — verified), script SHA table (all 4
rows match my re-hash), state-json == CSV == raw-header counts (all 3643 / same dict),
sweep stats (2,266,698 / 64 — exact reproduction), prior-run reference hashes (3/3
match my re-hash), administrative 27/26/28 figures (own counts). **CONFIRMED.**

**C11 manifest.** Re-hashed every executor package file (17): all 16 manifest rows
match; no executor file missing from the manifest; no manifest row pointing at a
non-existent file; the manifest itself correctly self-excluded (documented).
SCRIPT_SHA256.csv covers all 3 scripts + census_state.json, all matching.
**CONFIRMED.**

**C12 REPORT/HANDOFF vs the 20-point contract.** REPORT.md carries: human-first
decision block (Polish question first), RUN_ID/RUN_CLASS/milestone EU935-M1 header,
state before→after, claims→evidence table with taxonomy statuses (CONFIRMED/PASS/
SCANNED/NOT_DEMONSTRATED — no "%"-style claims), denominators, gates summary, negative
controls, hard stops ("None triggered" — consistent with S0), NOT_CHECKED (honest,
includes the 618 residue and the slot-17 seam), untouched-status section
(TRANSFORM_TO_MODEL remains NOT_DEMONSTRATED; max label SF30_LINK_TYPE_IDENTIFIED),
handoff block. HANDOFF implements the FINAL_HANDOFF_SCHEMA completely (all 16 fields
verified). REPORT does not claim beyond its taxonomy statuses, with one wording
caveat (P3-9). FINAL_STATUS A adjudication: §5 below.

## 4. Findings (P0: 0 · P1: 0 · P2: 3 · P3: 6)

> No finding invalidates a load-bearing claim of the run. All core science
> (writers, provenance, RTTI identity, census counts, gates results) is
> independently reproduced to the byte. The findings below are citation-precision,
> label-precision, gate-mechanism and hygiene defects.

**P2-1. Receiver-site citations attach the `mov` to the CALL's VA (semantic claim
correct, VA citation imprecise).** Locations: 06_REPORT/REPORT.md:79 (C9 row);
01_RAW/SF30_WRITER_RAW.txt:62 (§2.6); 00_CONTROL/census.py:196;
00_CONTROL/census_state.json:72. Claim: "0x00529020 `mov ecx,[esi+0xc0]; call
0x5094c0`" and "0x0067B8E8 mov ecx,[esi+4]". Counter-evidence (own decode): the load
is at **0x0052901A** (`8B 8E C0 00 00 00`) and the call at 0x00529020; the loads for
the other sites are at 0x0067B8E4 / 0x0067C8A4 / 0x006A3A29 with calls at
0x0067B8E8 / 0x0067C8A8 / 0x006A3A2D. Skutek/impact: the semantic content (FUN_005094C0
called with ecx loaded from a proven SF slot) is byte-proven by me at all four sites,
and no census classification depends on it (zero census candidates inside
FUN_005094C0), so nothing is invalidated — but a future run citing the raw pointer
would re-derive anyway (contract-mandated), and the current text mislabels the VA.
Correction (narrow): reword to "load @0x0052901A `mov ecx,[esi+0xc0]`; call
0x5094c0 @0x00529020" (and analogues for the 3 other sites). Revalidation predicate:
decode 0x0052901A/0x00529020 and the three pairs and confirm the load/call split.

**P2-2. RTTI name-offset label "TD+0x0C" is wrong; the actual name offset is TD+0x08
(bytes correct).** Locations: 01_RAW/SF30_RTTI_RAW.txt:10 and :19; 06_REPORT/REPORT.md
evidence row C6 ("TD+0x0C name bytes"); the label originates in the contract itself
(RUN_CONTRACT.md:59 "TD+0x0C name string"). Counter-evidence (own reads): TD+0x08 =
`2e3f4156…` = ".?AVSceneFeederObject@@" / ".?AVNiNode@@" (the recorded bytes — so the
walker read +8); TD+0x0C = "SceneFeederObject@@" / "NiNode@@" (the name WITHOUT the
".?AV" prefix — proving the label and the recorded bytes disagree). The executor's
walker code (sf30_core.py:322, `td_raw[8:]`) is the correct MSVC TypeDescriptor layout
and the calibration PASS supports it. Impact: a re-derivation following the label would
read the wrong offset and get a name without the ".?AV" prefix; the identity conclusion
is unaffected (bytes as recorded are the true names). Correction (narrow): relabel to
"TD+0x08 name bytes" in future regenerations; note the contract's own label as the
origin of the error (fix the contract template too). Revalidation predicate: read
8 bytes at TD+0x08 vs TD+0x0C and compare to the recorded hex.

**P2-3. G5 negative-context detector is substring-permissive (gate mechanism weaker
than the claimed fail-closed).** Location: 00_CONTROL/finalize.py:127-129. Mechanism:
any line containing MODEL_BRIDGE_CONFIRMED/TRANSFORM_TO_MODEL passes the gate if the
line merely also contains one of "NOT_DEMONSTRATED" / "not made" / "no " / "NOT " /
"remains" / "zero" — e.g. a hypothetical claim line "MODEL_BRIDGE_CONFIRMED (no
further doubt)" would pass. Impact: the G5 **verdict is nonetheless TRUE** — my own
independent census of all 17 package files found 14 label occurrences, all in
negative/forbidden context, 0 claim-context (and zero slot-17/forbidden-callee
listings). The defect is in the reusable gate mechanism, not in this run's result.
Correction (narrow, for future gate templates): fail on ANY occurrence unless the line
matches an explicit whitelist of sanctioned negative statements, and record the
census (file, line, context) in the gates row. Revalidation predicate: inject a
synthetic claim line into a copy of the package and assert the gate FAILS.

**P3-4. REPORT's REJECTED-reason enumeration lists R-EBP-FRAME, which fired 0 times.**
Location: 06_REPORT/REPORT.md:92-93 (§3 bound section: "R-ESP stack slots; R-EBP-FRAME
/ R-EBP-INHERITED frames; …"). Counter-evidence: my raw-wide census of all 3023
`why:` lines finds R-EBP-FRAME 0 times; the fired reasons are R-ESP 2765, R-STACK-PTR
129, R-CTOR-OTHER 104, R-ZERO 18, R-LEA-STACK 3, R-EBP-INHERITED 2, R-IMM-STATIC 1,
R-CONT-FIELD 1 (=3023 exactly). Correction: enumerate only fired reasons (with counts)
or state "R-EBP-FRAME (0 rows; rule present, never fired)". Revalidation: recount the
reason families from the raw why-lines.

**P3-5. Era/RUN_ID header labels missing from four evidence artifacts.** Locations:
01_RAW/POSITIVE_CONTROL_0050A050.txt (no PCG_9_3_5, no RUN_ID),
01_RAW/SF30_RTTI_RAW.txt and 01_RAW/SF30_WRITER_RAW.txt (no PCG_9_3_5; RUN_ID present),
02_ANALYSIS/SF30_PROVENANCE.md (no PCG_9_3_5, no RUN_ID). STATIC-ONLY is present in
all four. The quality bar ("era label PCG_9_3_5 everywhere") is met in the four
identity/report documents but not in every evidence artifact. Correction: add the era
+ RUN_ID header lines in future regenerations. No science impact.

**P3-6. Raw §2.1/§03 "hit -> store insn" renderings are misaligned decodes and omit
the hit VA.** Locations: 01_RAW/SF30_WRITER_RAW.txt:19 ("hit -> store insn: 00509368
`0058d4 add byte ptr [eax - 0x2c], bl`" — a misaligned decode of the imm32 bytes; the
true store is at 0x00509366, correctly stated on the "classified:" lines :23-24) and
:83-87 (renders at 0x00509001 / 0x008B92F8 / 0x008B9518 similarly misaligned for the
0x00A7D42C pattern scan). Root cause: census.py:103 (`C.hexdump(pe, h, 0) and …`
evaluates falsy → the hit VA is never printed) and the 1..8-byte-back disasm can land
on a covering misaligned decode. The authoritative classified lines are correct and
asserted (census.py:106). Correction: print the hit VA explicitly and render the
containing instruction from its true start. Cosmetic/provenance noise only.

**P3-7. Gate machinery computed forbidden-function extents by decoding their bodies
in memory (unpersisted boundary touch).** Location: 00_CONTROL/finalize.py:147
(`fn_range(0x00437F70), fn_range(0x0082B5A0), fn_range(0x007B5390)` → `derive_body`
linearly decodes those bodies to find their ends; only the row-membership count 0 was
used, nothing persisted). The full-.text census sweep itself also necessarily decodes
through those bytes (contract-mandated), so this is a boundary/extent computation
within that regime — but REPORT.md:81/107's "the positive-control window re-read
(allowed) is the only touch" is accurate for the PACKAGE CONTENTS, not for the run's
in-memory machinery. Correction (future runs): document the extent-touch in the G5
gates row, or derive extents without semantic decode. My own QC extent-derivation did
the same boundary-only touch (disclosed; no semantics extracted, no listings).

**P3-8. PROVENANCE hop notation "ecx=[block+0xC8]" is a dereference notation for an
address-of instruction.** Location: 02_ANALYSIS/SF30_PROVENANCE.md:41 ("call 0x788480
with ecx=[block+0xC8]"). Measured (own decode): `lea ecx,[esi+0xc8]` @0x007B6037
(address-of block+0xC8) preceding `call 0x788480` @0x007B6047. Correction: "ecx =
&block[+0xC8] (lea @0x007B6037)". Receipt-level recording is otherwise byte-correct.

**P3-9. Two wording imprecisions in REPORT.** (a) REPORT.md:63 §2: "the field's whole
lifecycle … is byte-locked" — the proven transitions (create in ctor / release+null in
dtor) ARE byte-locked, but "whole" implicitly leans on the census bound (the 618
residue); the bound is prominently disclosed in §3/§7, so suggest "the field's proven
lifecycle transitions (create/release/null) are byte-locked". (b) REPORT.md:78 C8(iii)
"at the 7 proven container callsites" — the scan actually covered the 5 proven
container FUNCTION bodies (a superset of the 7 store sites; my own rescan agrees with
0 hits); suggest "at the 5 proven container functions (7 store sites)". No claim
direction changes in either case.

## 5. The 618-POSSIBLE_ALIAS completeness question (mandatory assessment)

The census denominator is provably complete: my own re-implementation of the
documented enumeration rule reproduces the sweep to the exact instruction (2,266,698
decoded, 64 restarts) and the exact candidate set (3643), every CSV row byte-matches
my own decode, and the raw file contains a windowed block for every candidate. The
618-row residue is bounded at two levels. Per ROW it is evidence-backed: each row
carries its instruction form, its containing function (562 distinct functions), its
base register and the honest result that the receiver's provenance could not be
statically resolved to SF or non-SF within the run's bounds; my 12-row sampling
across 12 different functions found exactly the documented pattern (unknown-provenance
bases in functions never proven to receive SF, e.g. thiscall-this copies in
unproven classes) with zero misclassifications, and my adversarial deep-checks of the
rejection families (R-CTOR-OTHER full-body, R-ZERO, R-IMM-STATIC, R-CONT-FIELD) found
them sound as applied. Per CLASS the bound is function-level, not
reachability- or vtable-anchored: what the census proves is that inside all 19
SF-proven-context functions every write-form candidate is resolved — exactly the 2
PROVEN writers (each anchored by the vtable store of 0x00A7D458 into [this+0] with
single-definition receiver registers, both re-verified by me) and 7 REJECTED
(stack/container receivers) — plus a complete enumeration of the SF creation and
containment surface (2 E8 ctor callers, 0 absolute references, 7 durable pointer
slots with byte-verified stores). What the census does NOT prove — and honestly says
so in REPORT §3, §7 and HANDOFF — is that none of the 618 could write SF+0x30: an SF
pointer could in principle reach a non-F_SF function's register through an unmodeled
interprocedural channel (argument passing, stack/heap intermediates, globals), and
whole-binary SF pointer-origin closure was explicitly out of scope. So "exactly two"
is proven exactly as the package words it — "exactly two PROVEN writers" — and the
completeness of the census is enumeration-completeness (auditable denominator, full
4-class classification, disclosed residue), not resolution-completeness of all 3643
receivers. FINAL_STATUS A is therefore SUPPORTED under the contract's own taxonomy
(Task A defines the census deliverable as the auditable denominator with a 4-class
classification; POSSIBLE_ALIAS is a contract-designed class and G2–G4, the contract's
own A-tier predicates, all pass), with the explicit caveat for PE-MASTER that under a
stricter ad-hoc reading of "complete writer census" (every receiver resolved) the
honest ceiling would be below A — but that reading would make the contract's own
POSSIBLE_ALIAS class meaningless, and the package already carries the stricter
reading's disclosure at every level (REPORT §1 "proven writers", §3 bound section,
§7 NOT_CHECKED, HANDOFF residue line). I adjudicate A as defensible and honestly
documented; no downgrade is required by the evidence.

## 6. FINAL_STATUS adjudication

**FINAL_STATUS: A — IDENTIFIED: SUPPORTED (QC).** Complete auditable writer census
(denominator independently reproduced to the exact instruction and row), continuous
creation/receipt-level provenance for both proven writers (every hop byte-verified by
me), RTTI/type identity via a calibrated, byte-confirmed walker (`.?AVNiNode@@`,
secondary `?$NiTPointerList@PAVNiDynamicEffect@@@@`), scope held (no model-bridge
claim, no slot-17 consumption), with the 618-row static bound disclosed as
required. NEXT_SEAM SLOT17 (0x007B5390, recorded VALUE only) is the correct,
contract-mandated next seam.

## 7. FULL_READ_LOG (executor package, read to EOF unless noted)

RUN_CONTRACT.md (128 lines, full) · SOURCE_IDENTITIES.json (full) · SCRIPT_SHA256.csv
(full) · census_state.json (full) · sf30_core.py (346 lines, full) · census.py (1087
lines, full) · finalize.py (286 lines, full) · POSITIVE_CONTROL_0050A050.txt (full) ·
SF30_RTTI_RAW.txt (full) · SF30_PROVENANCE.md (full) · REPORT.md (full) · HANDOFF.md
(full) · MANIFEST_SHA256.csv (full) · STAGE_ACCEPTANCE_GATES.csv (full) ·
SF30_WRITER_RAW.txt (header §01–§05 + RTTI §07 read in full; the 3643 per-candidate
blocks were FULLY parsed programmatically — class/why/reason extracted for every row,
12+ blocks read line-by-line — not a linear human read of all 2.4 MB) ·
SF30_WRITER_CENSUS.csv (all 3643 rows parsed programmatically and every row's
instruction cross-checked against my own byte decode). Prior-run artifacts touched
read-only for the administrative verification (SLOT_CENSUS file/manifest counts,
commit file list, 3 reference-file hashes).

## 8. NOT_CHECKED (by this QC round)

- No runtime/dynamic verification of any claim (STATIC-ONLY contract; no game binary
  process launched by QC either).
- 606 of the 618 POSSIBLE_ALIAS rows were not individually hand-traced (12 sampled
  across 12 functions + all 618 parsed for form/function/why; the class-level bound
  assessed structurally).
- 100 of the 104 R-CTOR-OTHER rows not deep-checked beyond the claimed
  vtable/RTTI-string presence (4 deep-checked full-body).
- The 64 sweep restart points were reproduced numerically but not individually
  inspected for boundary validity.
- 0x437F70 / 0x82B5A0 / 0x007B5390 bodies NOT analyzed by QC (extent-derivation only,
  boundary semantics-free, consistent with the run's scope).
- The executor's own census.py/finalize.py were NOT re-executed (independence
  requirement); all checks are my own re-implementations.
- Prior-run packages re-verified only for the administrative figures and the 3
  reference hashes; their science was not re-audited here.

## 9. QC probe inventory (QC additions, outside the executor's manifest by convention)

00_CONTROL/qc_probe/: qc1_counters.py · qc2_bytes.py · qc3_sweep.py ·
qc4_sample_scope.py · qc4b_scope_bytes.py · qc5_final.py · out_qc1_counters.txt ·
out_qc2_bytes.txt · out_qc3_sweep.txt · out_qc4_sample_scope.txt ·
out_qc4b_scope_bytes.txt · out_qc5_final.txt. SHA256 (uppercase):
qc1_counters.py BB7FF3AD8B19A635A79C843797A3E20781AE9F3A9D5D37397BFFF5EC9338AA65 ·
qc2_bytes.py DCE9091AB93877B78E39309E7B2AFD244C630BA7D31F32E5FB591C7EC6E6C98B ·
qc3_sweep.py 9AF5B188D3A21FB7A6BDAB4E2D2FD21ACFA69548FD14A8BEEC8F96F6B8601E8D ·
qc4_sample_scope.py 22E9AC4CF76625026FA7B2D5E8EA200BCC041B8A20FC15B07634A29D49B3D942 ·
qc4b_scope_bytes.py 430B80CE6AB7B52D2B4F456B15B86552FD0C7D11B3FAEDE5BBB4C16270DD8959 ·
qc5_final.py 2DDAD0CB40384D3D040F568E0039BE04B5752FF19AD141B56957DF5FFA56E1B0 ·
out_qc1_counters.txt DFE4B37D71CDBAADDC28DBD0C422207F359C1FA1881ECFE2B0BEADAE4001E0B4 ·
out_qc2_bytes.txt DB3BC4CF5C79181A4EAC01DA5FBFF5FF57598F96A9A33300A14796A3FA5D0BBE ·
out_qc3_sweep.txt 05509B777DBB9CCCE3C945B816951C487C0FC7E8D3A1E343A8E18035F3DAAA46 ·
out_qc4_sample_scope.txt 6786160F8597510EAE019B930372865980ECAC40A857AA54B37A0AC612A2F466 ·
out_qc4b_scope_bytes.txt 741CFF6084A5D7A8BC52AFA9B2AEC3663C96F34D9CC8CD4E0542E909F020B5A3 ·
out_qc5_final.txt 71B99BC7403497FA9F7F63544FD4F8F99EFC8ED5905320481EAFB2C6A0128AC0.
(Note: out_qc* file hashes above were taken before QC_AUDIT_R1.md was written; the
qc_probe outputs do not cover this file.)

## 10. Verdict

- **QC_VERDICT: QC_PASS** — the load-bearing claims of
  PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 are independently reproduced to the
  byte (writers, provenance chains, RTTI identity, census counts, sweep denominator,
  gates results, manifests, administrative correction); scope held; no overclaim found.
- Findings: **P0: 0, P1: 0, P2: 3, P3: 6** (P2-1 receiver-site citation VAs; P2-2
  "TD+0x0C" vs actual +0x08 label; P2-3 G5 detector permissiveness; P3-4 R-EBP-FRAME
  0-count enumeration; P3-5 era/RUN_ID label gaps; P3-6 misaligned "store insn"
  renders; P3-7 gate extent-touch disclosure; P3-8 "ecx=[block+0xC8]" notation; P3-9
  two REPORT wordings). Each with exact location, counter-evidence, narrow correction
  and revalidation predicate in §4. None blocks adjudication or publication; the P2
  items should be carried as amendments/notes in any NEXT regeneration and the G5
  detector fix into the next gate template.
- FINAL_STATUS A: SUPPORTED with the 618-bound adjudication in §5–§6.
- No executor evidence file was modified by QC. ZERO git mutations (HEAD ==
  BASE_SHA == origin/master == remote, verified before and after; only the untracked
  package dir + foreign experiments/ remain).

— pe-master-auditor, INTERNAL_QC round 1, 2026-09-14.
