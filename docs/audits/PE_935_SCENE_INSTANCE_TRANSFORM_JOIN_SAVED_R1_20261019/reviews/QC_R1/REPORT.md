# QC_R1 REPORT — independent internal QC of PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019

QC_RUN_ID: QC_R1 | RUN_ID: PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019
Author: pe-master-auditor (FRESH independent QC session; no authorship of any audited package)
Parent: PE-MASTER | Contract: AUTHORING_R1 CONTRACT.md section 10
Date: 2026-10-20 | Host: WINDEV2407EVAL
Target scope: P01_CALLER, P02_CONTINUATION, P03_DISPATCHER, P04_OWNERCTOR, P01..P11_EXTRACT, CONTROL (EVENTS/REQUESTS/PLANS), root checkpoint files. READ-ONLY: no package file modified.

## QC_VERDICT: PASS_WITH_FINDINGS

(2 findings P1, 7 findings P2, plus observations. All load-bearing mechanical recomputations — ESP/FPU balance, receiver/argument flows, budgets, event-chain integrity, source pins, bounded negatives — PASS. The P1 findings are claim-text factual errors in two fallback-authored claims that must be corrected before seal; they do not invalidate the mechanical discipline or the packages' UNKNOWN/conditional statuses.)

---

## 1. Mandatory recomputation results (per QC task items 1–7)

| item | scope | result |
|---|---|---|
| 1 | P01 ESP walk + ECX/arg/REP MOVSD | **PASS** (5/5 sub-checks) |
| 2 | P02 FPU/ESP + L1/L2 dataflow | **PASS 7/8** — FAIL on L1 OUT-slot mapping (**QC-F1**) |
| 3 | P03 receivers/S1/S1_2/guard-exit/census | **PASS** (7/7 asked sub-checks; census claims carry **QC-F2**) |
| 4 | P04/P05/P08/P10 saved-text claims (+P09 hex cross-check) | **PASS 8/9** — arg-index nit **QC-F8** |
| 5 | Budgets / ADMIT-vs-request / event chain / source pins | **PASS** (7/7) |
| 6 | Negative scope (FIRST_MISSING_EDGE labels) | **PASS** (2/2) |
| 7 | Alias/lifetime premise inventory | **PASS with gaps** (16 labeled groups correct; 5 unlabeled gaps → QC-F5/F6/F7/F9) |

Full recompute detail with row/line references: `RECHECKS.json`.

## 2. Findings

**[P1] QC-F1 — P02 L1 source-slot off-by-4: 0085C140 reads OUT+0x24, not OUT+0x20; the "non-contiguous, +0x24 skipped" claim is wrong.**
- Contradicted claim: P02 REPORT §1.2 ("L1 = [ESI+0x54/0x58/0x5C] + S1*(OUT[+0x20/+0x28/+0x2C] − ...)"), REPORT §2 ("the three OUT slots consumed here are +0x20, +0x28, +0x2C (non-contiguous: +0x24 skipped)"), FLOW.md step 2, STACK_MAP line 11 ("+0x20 (E-0x14) @0x0085C140"), CLAIMS P02-C03 (status CONFIRMED), GATES G06 (result PASS).
- Physical counter-evidence: `P02_EXTRACT` rows 1171051/1171054: the `FLD dword ptr [ESP+0x70]` at 0085C140 executes **before** `PUSH ECX` at 0085C14B, with ESP=E-0x80 (the 0085BFA0 out-arg push at 0085C138 was cleaned by 0085BFA0's RET 0x4 — pinned from the opened frozen body, R2 P04_EXTRACT row 1171004 `RET 0x4 @0x0085C0B4`, re-read by this QC). [E−0x80+0x70] = **[E−0x10] = OUT+0x24** (OUT=E−0x34). The package's P02-C03 premise ("frame offsets at ESP=E−0x84, arg pushed at 0x0085C14B still on stack") applies the post-push ESP to a pre-push instruction.
- Independent corroboration: (a) P03's own STACK_MAP line 10 computes the identical out-buffer trio of CALL 0085BFA0@00528870 at **+0x24/+0x28/+0x2C** (out=E−0x68; reads [E−0x44]/[E−0x40]/[E−0x3C]); (b) the frozen 0085BFA0 body explicitly stores the 3-component result trio to [EAX+0x24]/[EAX+0x28]/[EAX+0x2C] and 1.0f to [EAX+0x30] (R2 P04_EXTRACT rows 1170996/1170998/1171001) — under the frozen "9 rot + 3 trans + 1.0f" layout, +0x24/+0x28/+0x2C is the CONTIGUOUS translation trio; (c) the P03 caller reads the 0085C130 result at [EAX+0x24]/[+0x28]/[+0x2C] (rows 182010–182016).
- Failure mechanism: single ESP-state slip at one instruction; propagated consistently through all P02 documents and into the QC-question paraphrase itself.
- Affected: P02 REPORT/FLOW/STACK_MAP/CLAIMS-C03/GATES-G06; the semantic summary "owner fields blended toward three floats from the fresh 0085BFA0 output" survives (the three floats are the translation trio, which is now coherent rather than the bizarre rot[8]/trans[1]/trans[2] mix the +0x20 reading implied).
- Correction: restate L1 = [ESI+0x54/0x58/0x5C] + S1*(**OUT[+0x24]**/+0x28/+0x2C − field); delete "non-contiguous / +0x24 skipped" (the slot not read here is +0x20). Packages are unsealed — fix in place pre-seal, or add sibling CORRIGENDUM post-seal per contract §10.
- Revalidation predicate: recompute [ESP+0x70] at 0085C140 with ESP=E−0x80 (0085BFA0 RET 0x4 pinned) → E−0x10 = OUT+0x24; assert slots {0x24,0x28,0x2C} contiguous and +0x20 absent from the window.

**[P1] QC-F2 — P03-C13 receiver-attribution conflation: 0085B0A0/0085B0B0/0085ACB0 do NOT "receive ECX=[owner+0xC]"; they receive ECX=owner.**
- Contradicted claim: P03-C13 ("The receiver object [owner+0xC] has a method family at 0085B0A0/0085B0B0/0085ACB0/0085C130/0085C280/0085C310/0085C330/0085CDE0/0085BFA0 — **all receive ECX=[owner+0xC] in this window**", status "CONFIRMED (dispatch pattern)") and REPORT finding 7 ("The receiver [owner+0xC] has a 10-method family in the 0085B0A0..0085CDE0 range — this is the receiver's class cluster").
- Physical counter-evidence (P03_EXTRACT): row 181869 CALL 0085b0a0@0052882A with ECX = entry ECX = this (owner; no ECX write between MOV ESI,ECX@00528814 and the call); row 181873 CALL 0085b0b0@00528835 preceded by `MOV ECX,ESI`; row 181882 CALL 0085acb0@00528854 preceded by `MOV ECX,ESI`. Ten calls (B0A0×5, B0B0×3, ACB0×2) dispatch on the OWNER. The claim's own row_vas (0052882A/00528835/00528854) disprove its wording. P03's own census P03-C10 classifies these correctly as owner-methods — the package contradicts itself between C10 (correct) and C13 (wrong).
- Failure mechanism: summary claim conflated "methods located in the 0085B0A0–0085CDE0 address cluster" with "methods dispatched on the receiver"; also an unexplained count ("10-method" vs 9 distinct in-window targets listed).
- Affected: the next-edge decision "saved RTTI/ctor census for the receiver cluster 0085B0A0..0085CDE0" — if acted on as worded, the receiver-class search would wrongly include owner-class methods (wasted/incorrect admissions; the owner class is separately identified as the 0xA7DCB0/0xA91E4B0 family).
- Correction: restrict the [owner+0xC]-receiver set to {0085BFA0, 0085C130×2, 0085CDE0, 0085C280, 0085C310, 0085C330} (7 calls); classify 0085B0A0/0085B0B0/0085ACB0 as owner-methods (ECX=ESI); optionally re-word the address-cluster observation as a separate claim (both method families live in 0085B0A0–0085CDE0, which remains true and useful).
- Revalidation predicate: row-by-row ECX audit at all 29 CALLs (done here; see RECHECKS ITEM3) — assert receiver-set membership per call equals C10's classification and contains no owner-methods.

**[P2] QC-F3 — P03-C03 "identical roles" for the +0xE0/+0xE4/+0xE8 float trio is overstated.** P01's trio: E0:=0.0 and E4:=0.0 always, E8:=E4 conditionally (global-vs-field compare). P03's trio: E4+=f1, E0=min(E0+f1,E8), S1_2=E0/E8. Same offsets and float-trio family; different dataflow. The same-class conclusion (STRONGLY_SUPPORTED) rests correctly on +0xC/+0x10/member-shape + the P04 ctor field-set superset — restate the float-trio phrase as "same offsets, same float-trio family, different operations". Source: P01 rows 180904–180914 vs P03 rows 182026–182049.

**[P2] QC-F4 — P03-C01 "no ECX use" in helper 005287E0 is literally false.** Row 181845: `MOV ECX,dword ptr [ESP+0x8]` — ECX is the dword-count scratch counter. Correct wording: "ECX not used as this/receiver (scratch only)". The cdecl/3-stack-args/dword-copy/RET classification is otherwise correct and verified.

**[P2] QC-F5 — P03 premise-inventory gaps (ESP/FPU balance claims).** (a) 0043AE80 RET 0x4 cleanup premise (PUSH ECX@0052899D) missing from C11's list — required for epilogue balance; (b) 0041C740 and 0043AE80 float-return-in-ST0 premises missing (STACK_MAP line 22 names only 004B2A20/00861220/00734210/00861240; 0041C740's return is consumed by FMUL@00528977 and 0043AE80's by FSTP ST0@005289AA); (c) opaque-callee FPU-neutrality premise for C12's depth-0-at-RET claim not explicit. The balance itself recomputed PASS under the (now-enumerated) premise set.

**[P2] QC-F6 — P02 FPU documentation defects.** (a) opaque-callee FPU-neutrality (0096CD10×2, 0096D7C0) unlabeled for C11's depth-0 claim (0085BFA0's FPU balance is evidence-covered by the frozen body); (b) STACK_MAP §FPU's "full step list in REPORT.md" pointer dangles — no full step list exists in P02 REPORT.md; (c) the "exact peaks" list has garbled intermediates ("5 @0x0085C1EA" → 3 after-exec at 0085C1E8 per my trace; "5 @0x0085C216" → 5 at 0085C20C) while peak=6 and depth-0-at-RET (the load-bearing parts) are correct.

**[P2] QC-F7 — P02-C05/P02 finding 1 cross-package field-identity premise unlabeled.** "this+0x30 = the 13-dword transform field the P01 caller fills" presumes the owner-class match (P03-C03/P04-C04, STRONGLY_SUPPORTED, not CONFIRMED) and leaves instance-identity open; P01-C24 elsewhere (correctly) refuses offset-equality unification. Mechanical dataflow stands; label the premise or downgrade to class-conditional phrasing.

**[P2] QC-F8 — P04-C06 "CALL 0x401360(arg2)" argument index wrong.** Row 81: `MOV EDX,[esp+0x48]` at ESP=E−0x38 → [E+0x10] = the ctor's 4th stack arg (RET 0x10 = 4 args; A1–A3 forwarded to the base ctor). "arg2" matches no consistent numbering. Chain conclusion ([this+0xC0] = 005247C0 product) unaffected.

**[P2] QC-F9 — P03-C10 census: 007105F0 receiver classification rests on an unlabeled ECX-clobber premise.** ECX=ESI at CALL 007105F0@0052885B/@00528AF9 only if 0085ACB0 (called immediately before with ECX=ESI) preserves ECX — thiscall ECX is volatile and 0085ACB0's body is unopened. Classify as "ESI if 0085ACB0 preserves ECX (premise), else UNKNOWN" or move to a separate premise-labeled group.

**Observations (non-blocking):** P02/P03/P04 artifact_index "~" size placeholders (P01 has real sizes); P03 request/plan candidate-owner label "0x00528809" vs visible entry 00528810 (conservative navigation label; claims use 00528810 correctly); P02 G01/C10 "4 inner pushes" silently excludes the evidence-cleaned 0085C138 push (balance correct); P04 finding 3's flat "DIFFERENT object" for [this+0xC0] vs [this+0xC] is the loose version of the correctly-hedged answer-section text ("NOT identified with"); P04 REPORT finding 1 "exactly the field families" is the loose version of the precisely-worded P04-C03 "exact init-set superset" (substance verified).

**Positive notes:** (1) P04-C10's open premise "0085B1B0 0xC?" is resolvable from already-admitted evidence: P09_EXTRACT hex `C2 0C 00` at 0085B31D — 0085B1B0 is RET 0xC; upgrade to CONFIRMED. (2) All 11 source pins re-hashed OK (hash+size). (3) Event chain previous_sha256 linkage intact (12/12). (4) Budget sums exact (34/413/35/34/712), no incidents; ADMIT counts match extract reality row-for-row. (5) The P03 package's own +0x24/+0x28/+0x2C computation independently confirms QC-F1's correction. (6) Worker-fallback attribution (DISPATCH_LEDGER D01–D10) is coherent with package author fields; P01 (worker pe-reconstruction, D01 COMPLETE) is the only worker-authored package.

## 3. FULL_READ_LOG (files read to completion by this QC)

Contract (AUTHORING_R1/CONTRACT.md, 153 lines, full). Run root: CORRECTIONS_APPLIED.json, DISPATCH_LEDGER.json, SCIENCE_CHECKPOINT.json. CONTROL/EVENTS 000001–000012 (all, full), CONTROL/REQUESTS P01–P11 (programmatic equality vs ADMIT payloads; P03 plan spot-read full), CONTROL/PLANS P03 (full; existence of P01–P11 verified). Extracts P01–P11 (all 11, full reads; P03 read in full 279 lines). Packages: P01_CALLER (all 9 files full), P02_CONTINUATION (all 9 full), P03_DISPATCHER (all 9 full), P04_OWNERCTOR (all 8 full). Prior frozen run read-only: PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019/P04_EXTRACT (full, 137 lines — used to pin 0085BFA0 RET 0x4, EAX=out-arg, translation-trio store slots). Hashed (not semantically read): all 9 catalog source files (pin verification), H5 (50,780,146 B pin re-hash).

## 4. NOT_CHECKED

See RECHECKS.json `not_checked`: no script execution; no callee runtime behavior (all unopened callees remain premise-only); selected_lines_sha256 values (raw-line hashes) not recomputed — source-file pins (stronger) re-hashed instead; P05–P11 have no analysis packages (extracts only, consistent with mid-run state); root-level §12 closure artifacts not yet present (parent's pre-seal step); no git/publication in this QC scope.

## 5. Verdict rationale

The run's mechanical backbone is sound: my independent recomputations confirm every ESP/FPU balance, every receiver/argument flow, every budget figure, the event-chain integrity, all source pins, and the bounded negatives. The two P1 findings are claim-wording/derivation errors in PE-MASTER-fallback analysis (one effective-address slip, one receiver-attribution conflation) — both precisely correctable from evidence already in the admitted set, neither fabricated nor status-inflating beyond the affected claims. Verdict: **PASS_WITH_FINDINGS**; corrections QC-F1/QC-F2 (and the P2s) should be applied before the parent seals the packages (unsealed state permits in-place fix; otherwise sibling CORRIGENDUM per contract §10).
