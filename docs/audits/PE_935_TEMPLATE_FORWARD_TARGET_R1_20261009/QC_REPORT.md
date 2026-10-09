# QC_REPORT — Internal QC of PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009

- **QC_RUN_ID**: PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009_QC_R1_20261009
- **Auditor**: pe-master-auditor, fresh context, dispatched by PE-MASTER (NO_NESTED_TASKS).
  Internal QC inside PE-MASTER — not an independent Desktop post-audit, not executor
  self-review. Executor artifacts were **read, never modified**; no commit/push;
  AUDIT_ENTRYPOINT.md untouched; no MANIFEST created.
- **Audited package**: `docs\audits\PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009\`
- **Method**: every load-bearing value re-measured by the auditor's own PE parser,
  byte-exact extraction, and a **third independent x86-32 decoder** written for this QC
  (`SCRATCH\QC_FRESH\`, labeled AUDITOR_RECHECK). Negative controls executed.
- **VERDICT: QC_PASS_WITH_FINDINGS** (zero P0/P1; 1×P2, 5×P3; no load-bearing
  conclusion invalidated; no rework dispatch required).

---

## 1. Per-duty results

| Duty | Result | Basis (auditor's own re-measurement) |
|---|---|---|
| D1 IDENTITY | **PASS** | EXE re-hashed: 8,015,872 B / SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (match). Ghidra sandbox EXE re-hashed = physical (match). Predecessor package: **all 26 manifest data rows re-hashed (25 package + AUDIT_ENTRYPOINT.md) — all byte-identical**. Git: HEAD == origin/master == live ls-remote == BASE `cea10e9…`; tracked diff empty; foreign untracked (5 packages + experiments/) untouched; **zero .pyc** in package+scratch (recursive, incl. this QC's own work). |
| D2 SUBJECT PINS | **PASS** | **72/72 byte pins MATCH** (64 main + 8 follow-up; every pin read from the EXE via my own PE section mapping, no executor listing involved). All **14/14 rel32 call targets recomputed** from opcode bytes: `0x511259→0x7CE1E0`, `0x6C3F74→0x7CE1E0`, `0x6C3FB5→0x40B070` + 11 anchors — all match. Sentinel `0x00BA5800`: my PE parse confirms `.data` raw ends at VA `0x00BA0000` < `0x00BA5800` < virtual end `0x00BA96E4`, vsize>rsize ⇒ **zero-initialized tail ⇒ static zero**; immediate-scan of all six bodies: `0xBA5800` appears ONLY in the lookup's not-found load (`B8 00 58 BA 00` @`0x72F5A5`) — **callers never test it**. FUN_0043A550 (119 B, 35 insns re-decoded): the incoming key sits at `[ESP+0x18]` post-prologue and is **never read** (only `[ESP+8]` SEH restores + local writes) — getter-never-reads-stack-arg **CONFIRMED**. |
| D3 DATAFLOW | **PASS** | My decoder reproduces **339/54/2/2/19/35 = 451 body instructions** with **VA boundaries identical** to the executor's OWN_DECODER output on all six bodies (and their raw bytes match the physical EXE everywhere; objdump W_B listing parsed: 54/54 identical). E1: single ECX writer `MOV ECX,EAX` @`0x511257`, 0 intervening calls. E2: single ECX writer `MOV ECX,EDI` @`0x6C3F6E`; EDI's only body writer `MOV EDI,EAX` @`0x6C3F67`; 0 intervening calls. E3: EDI capture is the only in-window EDI write; final ECX writer `MOV ECX,EDI` @`0x6C3FAE` on both converged paths; growth path crosses `CALL 0x6C2E00` (body CLOSED) — the **ABI condition is exactly as recorded**. No missed template-relevant writes/aliases: no EAX writer between the `0x40B070` call and reads `0x6C3FBE/C1`; `0x6C3FBA` reads a frame local, writes only ECX. `[P+8]` forwarding re-verified end-to-end: save `89 44 24 10` @`0x6C3F83`; pair stores `89 19`/`89 41 04` @`0x6C3F8D/F` (EAX still `[P+8]` there — censused); FUN_006C3640 arg order re-derived from the 6 pushes (arg6 `[P+8]`, arg5 `0x8BD720`, arg4 param_2, arg3 `[P+0x18]`, arg2 `[P+0x14]`, arg1 `&[ESP+0x30]`, this = same, cdecl +`ADD ESP,0x18`); FUN_00414670 3-arg/5-arg arg mappings verified; EDI=0 path-conditionality verified (only EDI writer between `XOR EDI,EDI` @`0x5110DF` and the capture is the XOR); liveness end @`0x51133F`. **FUN_00567170-family: absent** — my complete call-target census of W_A/W_B (46 distinct targets) contains no `0x567170`. Post-body context re-pinned (`E8 4F FF FF FF` @`0x6C3FFC`→`0x6C3F50`, `ADD ESP,8` @`0x6C4004`). |
| D4 FALSIFIERS | **PASS** | 8/8 designed AND executed (each record carries MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED). Load-bearing ones re-executed by me: F1 writer censuses reproduced; F2 sentinel facts re-measured; F3 struct-copy provenance re-traced (`0x50CAF0` call @`0x5112AC`, `0x50D8C0` call @`0x511307`, destinations `MOV ECX,ESP` @`0x5112B6/@0x511311` = stack; second `0x7CE1E0` use receiver = `0x41B3A0` result); F4 **zero FPU/SSE re-measured over my own decode of all six bodies** (no D8-DF/9B, no SSE-like 0F forms, no F2/F3/66+0F); F5 save/reload pair re-pinned; F6 re-verified — FUN_0040B070 takes **no stack argument**, `0x8BD720` (BB 20 D7 8B 00 @`0x6C3FB0`) is arg5 prep for FUN_006C3640, `.text`-range, never called in-window; F7 getter stack-arg claim re-verified + Ghidra export properly quarantined (`GHIDRA_HYPOTHESIS_ONLY`); F8 **independently replicated** — my third decoder agrees 451/451 with theirs and objdump (0 boundary, 0 call-target disagreements), and the disclosed repair loop is evidenced (`f8_boundary_crosscheck.json`: 135 initial disagreements → `DEFECTS_TO_FIX` → fixed → final 0). My negative controls: corrupted expectations correctly detected as MISMATCH (method not vacuous); my own decoder bugs produced loud failures fixed before any conclusion. |
| D5 GATES+RECORDS | **PASS_WITH_FINDINGS** | Gates: G1 PASS (72 pins + 14 rel32), G2 PASS (3/3 edges re-derived), G3 PASS **with P2-1/P3-1** (all 4 direct template rows + 7 forward rows exact and complete; my full audit of **135 memory-form operands** in the six bodies found **no missed template-derived access**), G4 PASS (INTERIOR_POINTER_SAME_OBJECT byte-proven; TRANSFORM_SEMANTICS=UNVERIFIED), G5 PASS (8/8), G6 PASS (identities re-verified), G7 PASS (promotion grep: every coordinate-term occurrence in the package is prohibitive/negative; claim limits verbatim). PREREG-before-science: consistent (mtime 10:31:15 precedes all decode artifacts 10:35+; windows/caps/falsifiers match execution; mtime caveat recorded). SELF_CHECK: credible — all its 46 byte re-checks re-verified by me. EVIDENCE_INDEX: 22/22 package hashes + 35/35 unique scratch hashes match; zero unindexed files. HANDOFF/FINAL_REPORT counts consistent with my re-measurements (451 insns; 126 = modrm-form memory operands — see P3-1; 23 files). NOT_CHECKED list honest — no forbidden body appears in any decoded artifact (window census verified). Intervention ledger: **HONEST** (Ghidra reuse pre-declared in PREREG §6 + sandbox hash verified; decoder repair loop disclosed and evidenced; objdump slices = genuine EXE bytes — I compared all 7 `.bin` slices against the EXE; no runtime/network; no installs; no commits; python -B, zero .pyc). |

## 2. Findings ledger

**P2-1 — Census machine-classifier provenance over-broad (7 W_A `[EAX]`-based operands mislabeled).**
`selfcheck.py` classifies ALL W_A `[EAX…]` operands under the "0x50CAF0/0x50D8C0 result
struct" class, and the census text states that class as the two struct-copy ranges. I
traced the true bases: `0x005111A5` reads the **CALL 0x843DD0** result; `0x005113DC/DE/E5`
and `0x00511455/5A/5D` are **stack writes through EAX=ESP** (`MOV EAX,ESP` @`0x005113D5` /
@`0x00511453` after `SUB ESP,0xC`). All 7 are genuinely non-template — **no template
access is missing; every conclusion stands** — but the "unclassified=[]" completeness
demonstration rests on a class rule whose label is wrong for 7 members.
**Correction (records pass via PE-MASTER; executor artifacts immutable for QC):** split
the class text/classifier into (a) struct-copy sources (2 ranges), (b) `0x843DD0`-result
read, (c) ESP-based stack-write regions. **Revalidation:** classifier over all 135
memory-form operands yields unclassified=[] with correct per-operand provenance
(reference: `QC_FRESH\QC_D6_FINAL_PINS.json`).

**P3-1 — SELF_CHECK "126 memory operands" excludes 9 A0–A3 moffs-form accesses.**
x86probe's moffs branch (A0–A3) never appends to `mem_ops`, so the machine count is
modrm-form only. The 9 (3× W_A: FS:[0] ×2 + cookie; 6× W_E2: FS:[0], cookie, singleton
read, singleton store, NULL store, FS:[0] write) ARE textually enumerated in census
classes, so completeness substantively holds; true all-forms count = **135** (incl. 42
LEA address computations). Correction: document the denominator definition or extend the
classifier to moffs.

**P3-2 — E3 chain census omits the byte-proven-safe crossing CALL 0x006C3F74.** The E3
chain is anchored "from template capture `0x6C3F67`", which lies before the E2 subject
CALL `0x6C3F74` (on both paths). EDI survival across it is **byte-provable** (the callee's
open 4-byte body never writes EDI), so the only ABI-assumption crossing remains
`0x6C2E00` exactly as recorded — the `CONFIRMED_CONDITIONAL` classification is correct
and non-weakened. Correction: add the crossing with its verification mode (byte-proven
vs ABI-assumption) in a records pass.

**P3-3 — SELF_CHECK "files: 22" vs HANDOFF "23 physical files"** (SELF_CHECK ran before
EVIDENCE_INDEX.md was written). Both honest for their moment; auditor's fresh hygiene
census: 23 files, 0 violations. Optional note only.

**P3-4 — CALL_EDGE_PROVENANCE has 13 entries while SELF_CHECK says "checked: 14"** (the
14th, `0x511154→0x41B3A0`, exists only in selfcheck.py). All 14 recomputed by me: MATCH.
Optional: add the edge row or a scope note.

**P3-5 — (informational) W_A body-end analysis marks the next function's `6A FF 68…`
SEH prologue as `is_next_prologue: false`** — the 4×CC padding rule still terminates the
body correctly (1212 B re-derived by me), so no defect; recorded for the pattern library.

## 3. Auditor toolchain disclosure (L1/L2 discipline)

Third decoder written fresh for this QC. Defects found during bring-up — ALU lo=2/3
boundary bug, missing 0x90–0x97 XCHG (both produced loud decode errors/count mismatches),
plus mnemonic-only defects (group1 /4-/5 AND↔SUB label, CMP in regs_w, raw-field
truncation on prefix bytes — none affect lengths, writes-sets, pins or conclusions) —
were fixed **before** any QC conclusion; the final three-way agreement was computed only
after fixes. Negative controls: corrupted getter bytes / wrong disp / wrong rel32 byte all
detected as MISMATCH.

## 4. Claim-status re-check (contract adjudication)

| Claim | Auditor status |
|---|---|
| FUN_007CE1E0 = 4-byte getter `8B 41 08 C3`, dereferences `[P+8]` | **CONFIRMED** (byte-verified) |
| FUN_0040B070 = 4-byte interior-pointer thunk `8D 41 14 C3`, no dereference | **CONFIRMED** (byte-verified) |
| Reads `0x6C3FBE`=`[P+0x18]` / `0x6C3FC1`=`[P+0x14]` | **CONFIRMED** (base provenance censused) |
| DERIVED_OBJECT_IDENTITY = INTERIOR_POINTER_SAME_OBJECT | **CONFIRMED** |
| TRANSFORM_SEMANTICS = UNVERIFIED (zero FPU/SSE in six bodies) | **CONFIRMED** (my own census) |
| POINTER_IDENTITY: E1/E2 CONFIRMED, E3 CONFIRMED_CONDITIONAL (0x6C2E00 ABI condition) | **CONFIRMED** (re-derived) |
| Sentinel `0x00BA5800` = static-zero .data tail, never tested by callers | **CONFIRMED** (PE parse + scan) |
| Lookup returns mapfind_result+0x14 (`83 C0 14` @`0x72F59E`) | **CONFIRMED** |
| Getter never reads its stack arg (Ghidra signature artifact, F7) | **CONFIRMED** |
| FUN_00567170-family not involved | **CONFIRMED** (call-target census) |
| Runtime identity NOT_ESTABLISHED; claim limits verbatim; WORLD_XYZ_RECOVERED = NO | **PRESERVED** (no promotion anywhere) |

## 5. NOT_CHECKED by the auditor (honesty list)

objdump listings other than W_B not re-parsed line-by-line (covered by the executor's
crosscheck + my own full decode of the same bytes); remaining SCRATCH generator scripts
beyond key sections (outputs hash-verified and independently re-measured); historical
before/after moments of the executor's checks (current state verified and consistent);
Ghidra project internal state (disclosure accepted); PREREGISTRATION first-write time
(mtime is last-write evidence — L14 caveat recorded).

## 6. Disposition for PE-MASTER

The executor run is **scientifically sound**: every contract claim reproduced from
physical bytes by an independent third decoder; the honest-outcome discipline
(UNKNOWN semantics, no promotion, E3 condition recorded, sentinel/NULL conditions kept)
is genuine. Findings are documentation/bookkeeping precision (P2-1 + P3-1..P3-5) —
suitable for a bounded records-correction dispatch or acceptance with the ledger noted;
**no pe-reconstruction rework is required**. Persistence/publication decisions remain
PE-MASTER's.

*QC artifacts: `QC_RESULTS.json` (this directory) + `QC_REPORT.md` (this file);
auditor evidence under `D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009\SCRATCH\QC_FRESH\`
(17 files, local-only). Git unchanged: HEAD = BASE = `cea10e9cfcaa2e814f5cfe4269fd2a6a409d54da`;
nothing committed or pushed by this QC.*
