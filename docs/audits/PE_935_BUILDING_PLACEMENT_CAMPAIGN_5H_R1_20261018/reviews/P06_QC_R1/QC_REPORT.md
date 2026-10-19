# QC REPORT — P06 (Front C) independent internal review
# RUN_ID: P06_QC_R1_20261018 | parent campaign: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018

- REVIEWER: pe-master-auditor, fresh child session dispatched directly by PE-MASTER (NO_NESTED_TASKS; no delegation; P05_QC_R1 predecessor marker untouched, unrelated to this pack)
- TARGET PACK: `packages\P06_EXEC_R1` (attribution: pe-reconstruction, bounded executor) — immutable, not modified by this review
- ADMISSION: A912213023006 (CONTROL/EVENTS/000008_ADMIT.json, 2026-10-18T22:20:52.721Z); this review opened NO new bodies (CONTRACT §12: re-checking the same extracts creates no new uncounted front)
- PINNED SOURCE: `GHIDRA_H5_VTABLE2.txt` — SHA256 `642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB` **recomputed by this reviewer** (50,780,146 B; 1,743,929 lines). Address search = navigation; semantic read confined to the two admitted subregions.
- QC VERDICT: **QC_PASS** (process verdict: **PASS_WITH_CORRECTIONS**) — all load-bearing claims independently re-derived and upheld; 1 P2 + 3 P3 corrections registered; no claim rejected; incident adjudicated compliant.

## 1. Mechanical integrity (all independently executed by this reviewer)

| Check | Result |
|---|---|
| MANIFEST re-hash (15 entries) | 15/15 SHA256 match, 15/15 size match |
| Manifest bijection | HOLDS (every disk file ↔ one manifest entry; only MANIFEST.json itself absent from its own list — self-excluded by design, not a defect) |
| Line parity vs pinned source | **92/92 rows byte-identical** (A: source lines 1282626-1282629; B: 1145803-1145890) |
| Window completeness | my scan of the pinned listing found exactly 4 rows in window A and 88 rows in window B — extracts complete, no missing/extra rows |
| Generator lineage | `tools/extract_p06_subregions.py` read to EOF: pin-verified (exit 2 on mismatch), read-only, VA-filtered with 9th-char space guard; no payload access; no circularity |
| Chronology vs CONTROL/EVENTS | ADMIT 22:20:52Z → CONTRACT 22:21:04Z → RUN_STARTED 22:21:29Z → extraction 22:21:54-56Z → analysis → correction pass 22:28:01-06Z (disclosed) → artifact_index + MANIFEST 22:28:12Z LAST — strictly ordered, no pre-admission read |

## 2. Instruction-level verification of the decisive derivations

**(a) The LEA/RET body (window A, 0x20 buffer content).** Independent VA-delta + encoding verification of all 4 in-window rows: `008bd720 LEA EAX,[ECX+0x18]` (8D 41 18, 3B) → `008bd723 RET` (C3, 1B) → body ends 008bd724; gap 008bd724-008bd72f contains NO listing rows (inter-body padding); the ONLY other in-window content is the unforeseen body `008bd730 MOV AL,[ECX+0x64]` (8A 41 64, 3B) → `008bd733 RET` (1B). **The worker's claims are upheld exactly**: 0x008BD720 is a 2-instruction, register-pure, side-effect-free leaf returning ECX+0x18; there is NO dispatch target VA; the "dispatches to" premise is REJECTED_WITH_EVIDENCE (CONFIRMED, listing-level, body fully in-window). Nothing else is in-window beyond the disclosed 0x008BD730 body.

**(b) The 0x00848EA0 call census.** Independent census of the 88 in-window rows: exactly **11 CALL instructions** (00848ed6, 00848ef8, 00848f0a, 00848f19, 00848f1f, 00848f26, 00848f39, 00848f40, 00848f74, 00848f8e, 00848fa6), **11 unique targets**, **0 indirect calls** — matches COUNTERS exactly. All 88 consecutive VA deltas fit standard x86 encodings (decisive cases independently recomputed: `MOV FS:[0x0],EAX` = 64 A3 moffs form (6B) — the only encoding consistent with the 00848ec1→00848ec7 delta; near JZ (0F 84) at 00848edf/00848eff because targets exceed rel8 range; short JZ (74, rel8=0x7B) at 00848f47; `FSTP [ESP]` = D9 1C 24 (3B); `MOV [ESP+0x78],imm32` = C7 44 24 78 + imm32 (8B)). Prologue arithmetic: [ESP+0x80] = first stack argument (3 SEH pushes + SUB 0x5C + 5 pushes + ret = 0x80) — CONFIRMED. Memory-read census independently reproduced: no slot-object field read in-window, no vtable dereference, class NOT_ESTABLISHED in-window — CONFIRMED. Produce chain CONFIRMED: `0x006C1F90(3 ptrs + 1 float)` with caller-cleanup ADD ESP,0x10 matching exactly 4 pushed dwords (incl. the `PUSH ECX;FSTP [ESP]` float slot), 12-byte triple copied to frame locals, JMP 0x00848FC6 outside window.

**(c) Navigation claims.** Independent single-pass address search of the pinned listing: pattern `8bd720` → **26 rows = 1 body + 22 direct CALL sites + 3 imm32 loads + 0 other**; the 22 call-site VAs and 3 imm32 VAs are **identical, entry by entry, to REPORT §9** (006b6d05/006c3fb0 `MOV EBX,0x8bd720`, 006d44e8 `MOV EDI,0x8bd720`). Pattern `848ea0` → **2 rows = 1 body + 1 CALL site (004e55f7) + 0 imm32**. All claims C1-C7 navigation facts CONFIRMED.

## 3. Accepted claims (with evidence_level adjudicated)

| Claim | Subject | Worker level | Reviewer adjudication |
|---|---|---|---|
| CLAIM-P06-C1 | 0x008BD720 = LEA EAX,[ECX+0x18]; RET; no dispatch target; premise REJECTED_WITH_EVIDENCE | CONFIRMED | **ACCEPTED — CONFIRMED** (re-derived instruction-level) |
| CLAIM-P06-C2 | pointer-returning leaf; continuation consumer-side; 22 CALL + 3 imm32 sites; NOT exclusively virtual (data-section caveat stated) | CONFIRMED (body semantics) / NOT_ESTABLISHED (which site) | **ACCEPTED — CONFIRMED / NOT_ESTABLISHED** (nav counts reproduced exactly; premise "no direct caller ≠ exclusively virtual" honored with evidence) |
| CLAIM-P06-C3 | flag-dispatch structure: 0x00745540(slot,1)→bool; TRUE falls through; flag-2 path ≥ 0x00848FEC outside window; AMEND-4/5 instruction-level confirmation | CONFIRMED (structure) / PLAUSIBLE (flag-2 attribution, inherited) | **ACCEPTED — CONFIRMED structure; PLAUSIBLE inherited attribution** (levels correctly separated) |
| CLAIM-P06-C4 | slot interface = {0x745540→bool, 0x745BF0→ptr null-checked, 0x745690→float}; no direct field read in-window; class NOT_ESTABLISHED; tag-6 hypothesis UNVERIFIED | CONFIRMED / STRONGLY_SUPPORTED / NOT_ESTABLISHED / UNVERIFIED | **ACCEPTED — all four levels upheld** (memory census independently reproduced) |
| CLAIM-P06-C5 | in-window dataflow: guarded lookup chain → 0x008E0110 → guard 0x0072FCE0 → 0x0072FE30 out-buffers → t=0x00745690 → R=0x006C1F90 → triple to frame locals; JMP epilogue outside; in-window writes frame-local only | CONFIRMED (structure) | **ACCEPTED — CONFIRMED structure, WITH CORRECTION QC-C2** (see §4: two of three out-buffers zero-initialized, not three; 6 stores not 7) |
| CLAIM-P06-C6 | NO VFS-record-fed channel visible in-window; scoped negative; merge NOT decidable in-window; gap edges (0x00745BF0 provenance, tag-6 writers, caller 0x004E55F7) | CONFIRMED (scoped) / NOT_ESTABLISHED (end-to-end) | **ACCEPTED — CONFIRMED scoped negative**; bounds kept (NOT an end-to-end absence claim); "definition registry ≠ instance source" preserved (not promoted) |
| CLAIM-P06-C7 | navigation facts (26/22/3; 2/1/0) | CONFIRMED (listing-level) | **ACCEPTED — CONFIRMED** (independently reproduced, lists identical) |

## 4. Corrections (registered; none rejects a claim)

- **QC-C2 (P2) — REPORT 4.1 row 9 + CLAIM-P06-C5 buffer wording.** "FLDZ + 7 FST/FSTP stores ... three 12-byte float3 frame buffers, zero-initialized in-window": actual census is **6** stores (00848f4f/f54/f5c/f61/f69/f70) = 24 B = **two** 12-byte buffers; the third out-arg pointer (LEA EDX,[ESP+0x24] @00848f65 → frame Q+0x1C) resolves to the region the earlier (c,c,c) const-vec group initialized (PUSH ESI + FST [ESP+0x20/0x24/0x28] at 00848eec-00848ef4). 6 stores cannot zero 3 buffers — internally inconsistent as worded. Correction: two zeroed + one (c,c,c)-filled in-window (under a non-callee-clean model, partially unwritten). Out-param idiom, produce chain and all other claims unaffected (callee overwrites the buffers). Required by the parent's re-derivation brief (the 0x0072FE30 payload group is a decisive derivation).
- **QC-C1 (P3) — same sentence, store count**: "7 zero-stores" → 6 (7 = instruction count including FLDZ).
- **QC-C3 (P3) — stale "honest bound" sentences** in COUNTERS.json/GATES.json ("final edit between 22:27:38.348Z and 22:27:52.985Z") vs corrected-file mtimes 22:28:01Z/22:28:03Z: the bound is true for the pre-correction content; the correction pass that embedded the sentence ran after the upper bound. REPORT §6.9 and MANIFEST disclose the correction pass, so the provenance chain stays honest — wording correction only.
- **QC-C4 (P3) — GATES G3 "extraction began 22:23Z"** vs extract mtimes 22:21:54-56Z (gate outcome unaffected: RUN_STARTED 22:21:29Z precedes extraction).
- **QC-C5 (P3, observation) — REPORT 4.1 row 11 VA range** "(00848f97-00848fbe)" overlaps row 12's range and omits ADD ESP,0x10 at 00848fbb — prose-range imprecision only; instruction descriptions correct.

## 5. Rejected overclaims

**None.** No load-bearing claim of P06 failed re-derivation. The two over-statements found (QC-C1/QC-C2) are sub-sentences inside an otherwise-confirmed claim and are registered as corrections with preserved valid layers.

## 6. INCIDENT-P06-I1 adjudication (explicit, per CONTRACT §6)

**Facts (verified):** window A [0x008BD720,0x008BD740) contained a second logical body 0x008BD730 (`MOV AL,[ECX+0x64]; RET`) not declared in body_entries; the VA region **was inside admission A912213023006** (the ADMIT event's combined span covers it); the worker (i) reported the incident (REPORT §5, GATES G10, CLAIMS incident block, HANDOFF, COUNTERS, MANIFEST), (ii) preserved the raw rows in the extract (verified present, lines 1282628-1282629), (iii) built **no claim** on it (verified: all 7 claims checked; occurrences are disclosure-level only; bodies_used_for_claims=2), (iv) kept rows 92≤98, CALL 11≤14, candidates 4≤4 within reserve, (v) opened no region beyond the admitted windows.

**Ruling: incident handling COMPLIANT with CONTRACT §6 in substance.** The contract's letter says "oznacz pakiet PARTIAL/NONCOMPLIANT stosownie do kontraktu"; the worker used the hybrid label **COMPLETED_WITH_PROCEDURAL_INCIDENT**, which preserves both facts (work completed; incident exists) and makes the non-clean status impossible to miss in every status surface (REPORT header, GATES gate_summary + run_status, MANIFEST run_status, COUNTERS budget_check, HANDOFF status block, CLAIMS incidents). I adjudicate the label variance as acceptable: the contract's intent (incident visible, no silent clean COMPLETED, no retroactive authorization, extract preserved, body unused) is fully satisfied, and the disposition is explicitly left to the parent. **Obligations for the parent:** (1) charge the +1 body (3 actual vs 2 reserved) to the shared campaign budget — it is an honest actual, not a retro-authorization; (2) record this adjudication in the campaign ledger. Package remains COMPLETED_WITH_PROCEDURAL_INCIDENT; no re-grade to PARTIAL is required by the evidence.

## 7. Premise preservation & scoped negatives

- update mechanism ≠ source: preserved (no promotion anywhere; C5 labels inherited and cited).
- vtable match ≠ receiver identity: preserved (C4: 0x745xxx family shape proves nothing about class; census-based).
- no direct caller ≠ exclusively virtual: applied **with evidence** (C2: 22 direct callers + 3 imm32; C6: 1 caller, and "exclusively direct" explicitly NOT claimed either — data-section caveat stated).
- definition registry ≠ instance source: preserved (C6; templates.vfs standing unchanged).
- Scoped negatives keep bounds: **verified** — C6's negative is explicitly in-window-only with three named gap edges; V3/V4 negatives exercised the actual predicates (window arithmetic, not absence-inference).

## 8. Precise remaining edge (confirmed as stated by the pack)

1. {0x66,A} continuation: which of the 3 imm32 registration sites (006B6D05/006C3FB0/006D44E8 — recorded-not-read, verified present in listing) stores 0x008BD720 into the scheduler queue, and what consumes &req+0x18.
2. id2/property provenance inside 0x00745BF0 (class-20006 tag-6 hypothesis UNVERIFIED — correctly not claimed).
3. Slot-object provenance at caller 0x004E55F7.
4. (Added by this review, minor) the initial content of the third 0x0072FE30 out-buffer ((c,c,c) region) — immaterial if the callee fully overwrites it, which the out-param contract implies but does not prove in-window.

## 9. NOT_CHECKED (explicit)

- Out-of-window regions: all 11 callees, 3 control targets (0x00848FEC/0x00848FC4/0x00848FC6), SEH handler 0x00A28300, data refs 0x00A7B25C/0x00B9D8D0, all 22+3 caller/registration sites, 0x004E55F7 — recorded-not-read (navigation only), per admission discipline; NOT semantically read by this reviewer either.
- Bridge context documents (DRAFT_FINAL_REPORT.md, AMEND_LOG_R1.md, bridge HANDOFF.md, PE_MASTER_REVIEW.md): cited by the pack, NOT re-derived here; their standing was accepted as inherited labels only, which is exactly how the pack uses them.
- Campaign-wide budget arithmetic beyond this package (parent's ledger); earlier packages P01-P04 (out of scope of this review).

## 10. FULL_READ_LOG

Pack P06_EXEC_R1 read to EOF: REPORT.md, CLAIMS.json, COUNTERS.json, GATES.json, HANDOFF.md, SOURCE_PINS.json, MEMORY_AND_IDENTITY.json, BARRIER_BACKLOG.json, CONTRACT.json, RUN_STARTED.json, EXTRACT_META.json, artifact_index.csv, MANIFEST.json, tools/extract_p06_subregions.py, both extracts. Parent control read: CONTROL/EVENTS/000008_ADMIT.json; authoring CONTRACT.md (§4/§6/§12). Pinned source: hashed, size+line-count verified; 92 admitted rows read and re-verified; two address-search navigation passes executed (no semantic out-of-window read).

**Verdict: QC_PASS / PASS_WITH_CORRECTIONS. Findings: 0×P0, 0×P1, 1×P2 (QC-C2), 4×P3 (QC-C1, QC-C3, QC-C4, QC-C5). Incident: compliant, adjudicated §6.**
