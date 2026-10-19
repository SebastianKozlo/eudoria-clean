# QC REPORT — P07 (Front C) independent internal review
# RUN_ID: P07_QC_R1_20261018 | parent campaign: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018

- REVIEWER: pe-master-auditor, fresh child session dispatched directly by PE-MASTER (NO_NESTED_TASKS; no delegation; no Task tool invoked)
- TARGET PACK: `packages\P07_EXEC_R1` (attribution: **DIRECT_ANALYST_FALLBACK of the PE-MASTER parent**, CONTRACT.md §4, after two incomplete child executions; attempt-1 artifacts preserved and reused) — immutable, not modified by this review
- ADMISSION: A0c76e3cc1494 (CONTROL/EVENTS/000009_ADMIT.json, 2026-10-18T22:42:27.505Z); this review opened NO new bodies (CONTRACT §12; re-checking the same extracts creates no new uncounted front)
- PINNED SOURCE: `GHIDRA_H5_VTABLE2.txt` — SHA256 `642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB` **recomputed by this reviewer** (50,780,146 B). Semantic read confined to the four admitted subregions; address search = navigation; out-of-window targets recorded-not-read.
- QC VERDICT: **QC_PASS** (process verdict: **PASS_WITH_CORRECTIONS**) — all five claims independently re-derived and upheld, zero rejections; 2×P1 + 2×P2 + 2×P3 corrections registered (counter-data and documentation class; none invalidates a claim).

## 1. Mechanical integrity (all independently executed by this reviewer)

| Check | Result |
|---|---|
| MANIFEST re-hash (15 entries) | 15/15 SHA256 match, 15/15 size match |
| Manifest bijection | HOLDS (disk = 15 entries + MANIFEST.json self-excluded; zero unmanifested files) |
| Package CONTRACT.json identity | SHA256 = CONTROL/CONTRACTS/P07.json (byte-identical copy) |
| Line parity vs pinned source | **148/148 rows byte-identical** (SR1: 809928-809959; SR2: 632981-633034; SR3: 650187-650215; SR4: 671404-671436) — full parity, exceeds the pack's "spot checks" |
| Window bounds | All 148 rows inside the four admitted windows; SR1 closes exactly at 0x00745C40 (RET 0x4), SR2 at 0x006B6D3E (JMP tail), SR3 at 0x006C3FDC (RET), SR4 at 0x006D450E (JMP tail) — **zero out-of-admission rows** |
| Encoding/tiling (independent) | All consecutive-VA deltas fit standard x86 encodings; decisive forms recomputed: `MOV [ESP+0x24],0x66` = C7 44 24 24 imm32 (8B, 006b6cf3→006b6cfb), `MOV EBX/EDI,0x8bd720` = BB/BF imm32 (5B) at 006b6d05/006c3fb0/006d44e8, `MOV [ESP+0xe8],0x1` = C7 84 24 disp32 imm32 (11B, 006d44b9→006d44c4), short JZ/JMP targets recomputed EXACT (745c40, 6b6d3e, 6b6d39, 6b6cc5, 6d4510, 6d450e, 6d44e0). No undefined-byte gaps — extract completeness follows |
| Generator lineage | `tools/extract_p07_subregions.py` read to EOF: pin-refusing (exit 2 on mismatch), read-only, VA-filtered end-exclusive; extracts regenerated NOT by re-running it but by direct source reads (148/148) — independence preserved |
| Chronology vs CONTROL/EVENTS | ADMIT 22:42:27.505Z → CONTRACT 22:42:32 → RUN_STARTED 22:43:02 → tool 22:43:27 → extracts 22:43:29 → analysis docs 22:51:18 → MANIFEST 22:51:18 LAST — strictly ordered, no pre-admission read |
| Attribution honesty | DIRECT_ANALYST_FALLBACK present in ALL package docs (REPORT title+§2, CLAIMS, COUNTERS, GATES, HANDOFF, MEMORY_AND_IDENTITY, SOURCE_PINS note, BARRIER_BACKLOG, MANIFEST); RUN_STARTED honestly shows attempt-1 worker pe-reconstruction |

## 2. Instruction-level verification of the decisive chains (dispatch-required)

1. **The 0x66 store** — source line 633010 @006b6cf3 `MOV dword ptr [ESP + 0x24],0x66`, encoding-verified (8B imm32 form). Stack arithmetic re-simulated: after the two LEA/PUSH pairs the store lands at frame slot E0+0x1c, adjacent to the A-value at E0+0x20 (stored @006b6ce3) — the 8-byte {0x66, A} frame pair that 0x0043C700 is invoked on (args &E0+0x24, &E0+0x1c; ECX=ESI). Claim C3's row-level statements are exact.
2. **The 0x8bd720 immediates** — all three sites verified verbatim + encoding-verified: `MOV EBX,0x8bd720` @006b6d05 (SR2), `MOV EBX,0x8bd720` @006c3fb0 (SR3), `MOV EDI,0x8bd720` @006d44e8 (SR4); identical, entry-by-entry, to P06 REPORT §9's recorded-not-read navigation list (coherent campaign continuation).
3. **The call census** — independent recount: **13 CALL rows** (SR1:1, SR2:6, SR3:3, SR4:3), **10 unique targets** (745a70, 6b4120, 72fce0, 7ce1e0, 43c700, 40b070, 43e5b0, 6c2e00, 6c3640, 733650). Published total `call_sites: 10` is CORRECT under the CONTRACT §6 "unikalne CALL sites" metric; the published per-window breakdown is DEFECTIVE (finding QC-P07-1).
4. **SR1 keyed-lookup mechanics** — 4-DWORD tuple writes verified ([EAX]=EBX, [EAX+4]=4 (MOV EAX,0x4; MOV EDI,EAX), [EAX+8]=ECX, [EAX+0xc]=arg1); callee 745A70 receives [this+4], [this+8], &arg1 and the key by value (ADD ESP,0x1c cleans exactly key(4)+3 pushes — stack arithmetic CONFIRMED); sentinel `CMP EAX,[ESI+8]` + `JZ 0x00745c40` (= first byte outside window, recomputed exact); success `MOV EAX,[EAX]` returns *[EAX].
5. **SR2/SR4 loop mechanics** — back-edges `JMP 0x006b6cc5` / `JMP 0x006d44e0` and exits `JZ 0x006b6d3e` / `JZ 0x006d450e`(+`JZ 0x006d4510`) recomputed exact; boolean gate `CALL 0x0072fce0; TEST AL,AL; JZ skip` verified; A-read `CALL 0x007ce1e0` → `[ESP+0x20]` verified.

## 3. Accepted claims (with evidence_level adjudicated)

| Claim | Subject (condensed) | Pack level | Reviewer adjudication |
|---|---|---|---|
| P07-C1 | 0x00745BF0 keyed map-lookup helper, not a property getter: 4-DWORD key (const 4 at +0x4), CALL 745A70 with [this+4]/[this+8]+key, sentinel CMP [this+8], success *[EAX], fail JZ→0x00745C40 (window end); id2/tag-6 NOT confirmed in-window | STRONGLY_SUPPORTED | **ACCEPTED — STRONGLY_SUPPORTED** (re-derived instruction-level; callee un-admitted, map semantics = hypothesis per countermodel; key[0]/key[2] in-window provenance unestablished — consistent with the level) |
| P07-C2 | No VFS/record-fed source visible in the 745BF0 window (scoped negative; merge question → 745A70) | CONFIRMED | **ACCEPTED — CONFIRMED scoped negative** (full 32-row census reproduced; bounds kept; not an end-to-end absence claim) |
| P07-C3 | 0x006B6C9D {0x66,A}-forming registration pump: worklist loop; 72FCE0 valid check; 7CE1E0 A-read getter (bridge-CONFIRMED, cited); 0x66 pair build via 43C700; callback 8BD720 via 40B070; enqueue via 43E5B0 | CONFIRMED | **ACCEPTED — CONFIRMED for the in-window structure** (loop, stores, immediates, calls all re-derived); functional labels of un-admitted callees (43C700 pair-build, 40B070 register, 43E5B0 enqueue) are the claim's OWN premise-flagged arg-shape inferences — wording note QC-P07-4 |
| P07-C4 | 006C3F98 and 006D44A4 (loop) pass the SAME callback 0x008BD720 via 40B070 + 6C3640 (second enqueue path) | CONFIRMED | **ACCEPTED — CONFIRMED for the pattern identity** (same immediate + identical call/deref/enqueue shape at both sites, re-derived); "register" is arg-shape wording, premise-disclosed (QC-P07-4) |
| P07-C5 | Consumer chain bounded; exact gap = bodies 0040B070/0043E5B0/006C3640 + callback invocation census | STRONGLY_SUPPORTED | **ACCEPTED — STRONGLY_SUPPORTED** (composition of P06 + P07-C3/C4; gap claim independently cross-checked against ALL campaign CONTRACTS/REQUESTS/EVENTS: no admission anywhere covers those bodies or an invocation census; 8BD720 body itself was P06's) |

**Citation verification (premises: inherited bridge claims cited, not re-derived):** 7CE1E0 = `MOV EAX,[ECX+0x08]; RET` (8b 41 08 c3) — byte-locked in the saved corpus (ATTRIBUTE_ORIGIN_SEAM GH1_DECOMP_CENSUS; CONSUMER_TRACE Z1_CLAIMS_MATRIX; CAND4_CHILD_ROOT_PROVENANCE CL-06 "prior-canon getter A [template+0x08], bridge CH1/X23") — **citation ACCURATE**; 72FCE0 = validity check — CONFIRMED standing in CAND4_CHILD_ROOT_PROVENANCE CL-05 (measured bytes) — **citation ACCURATE**; 8BD720 = leaf returning ECX+0x18, no dispatch target — P06 REPORT §3 + P06 QC §2(a), CONFIRMED and re-derived there — **citation ACCURATE**. Nuance registered under QC-P07-4: the getter is +8-GENERIC (RECEIVER_PROVENANCE_CORRECTIONS F1) — the A-role at this callsite is canon-inherited; element/receiver type un-admitted in P07.

## 4. Corrections (registered; none rejects a claim)

- **QC-P07-1 (P1) — COUNTERS.json `call_breakdown` is defective data.** Published `{SR1:1, SR2:8, SR3:3, SR4:2}`: SR2:8 and SR4:2 match neither CALL rows (6/3) nor per-window unique targets (6/3); the breakdown sums to **14, contradicting its own published total `call_sites:10`**; no consistent counting rule reproduces it from the frozen extracts. Correct values: CALL rows 1/6/3/3 (total 13); unique-target union 10 (per-window first-seen contributions 1/6/2/1). The headline total (10 unique CALL sites) is CORRECT and equals the reserve. Effect: any downstream consumer reading `call_breakdown` gets wrong data; the campaign ledger must use the recomputed values. Fix (parent ledger / corrigendum path; frozen pack immutable): state the counting rule and replace the breakdown.
- **QC-P07-2 (P1) — `artifact_index.csv` missing.** Required output per P07.json `required_outputs` and parent CONTRACT.md §12 ("Minimum worker pack: … gates, artifact index i manifest LAST"). The file is absent from the package and unlisted in MANIFEST.json. MANIFEST.json (15 entries, bijection verified) functionally covers the index role for this pack, but the contract-named artifact is not satisfied. Procedural/mechanical non-compliance, no scientific impact (all indexed data is recoverable from the verified manifest). Fix: record the deviation in the campaign ledger; do NOT retro-write the frozen pack; if a corrected index is needed it must be an explicit corrigendum.
- **QC-P07-3 (P2) — overshoot wording is physically wrong as written.** COUNTERS note + REPORT §Counters say SR2 "includes the loop tail beyond the function-map window 0x006B6D3E". Physically the extract's last row is VA 0x006b6d3c (JMP, 2B) ending exactly at 0x006B6D3E — **nothing is beyond the window end**. The +15 is actual-vs-RESERVE row accounting (148 vs 133; implied SR2 reserve 39), covering loop-tail rows INSIDE the admitted window. No admission violation occurred (see §6); the wording must not be read as an out-of-admission read. Correction: "SR2 actual 54 rows vs 39 reserved (function-map-predicted count); all 54 rows inside the admitted window ending 0x006B6D3E end-exclusive".
- **QC-P07-4 (P2) — two wording nuances on CONFIRMED claims.** (a) C3/C4/REPORT say the sites "register the SAME callback": the in-window CONFIRMED fact is the same imm32 value flowing through the identical 40B070→deref→6C3640/43E5B0 pattern; "registration" semantics is arg-shape (the claims' own premises disclose this — keep the premise flag attached wherever used as a working dependency). (b) C3's "A-read getter": 7CE1E0 reads +8 of MULTIPLE receiver types (corpus F1 correction); the A-role here is canon-inherited, and the element/receiver type is un-admitted — the claim should carry this receiver-type caveat when reused.
- **QC-P07-5 (P3) — body/fragment and metric-definition nuances.** Only SR1 is a complete body (prologue+epilogue in-window). SR2/SR4 are head-fragments (exits out-of-window); SR3 is a tail-fragment (epilogue POP EDI/ESI/EBX + ADD ESP,8 + RET with no in-window matching prologue); SR2/SR3 read stack slots above any entry-relative arg area ([ESP+0x38]/[ESP+0x50]) — entry ABI of 006B6C9D/006C3F98 is NOT established in-window (premise "worklist source un-admitted" honestly covers it). "bodies: 4" counts the contract's declared body_entries (consistent with reserve); no claim depends on entry ABI. Also: the "candidates" metric is undefined in package docs (inferred = the four admitted body candidates; numerically consistent).
- **QC-P07-6 (P3) — REPORT "10 CALL" ambiguity.** States the unique-target metric without saying so (CALL rows are 13). Recommend "10 unique CALL targets (13 CALL rows)" wherever the terminal-facing counters are quoted.

## 5. Rejected overclaims

**None.** All five claims survive independent re-derivation at their stated levels. The registered defects are counter-data/documentation class (QC-P07-1..6), not claim failures.

## 6. Overshoot adjudication (explicit, per CONTRACT §6)

**Facts (verified):** SR2 extract = 54 rows, VAs 006b6c9d–006b6d3c, **all inside the admitted subregion [0x006B6C9D, 0x006B6D3E)**; the last instruction (JMP back-edge, 2B) ends exactly at 0x006B6D3E end-exclusive. The window contains exactly ONE body fragment (0x006B6C9D) — its loop back-edge (006b6d3c→006b6cc5) and skip (006b6cda→006b6d39) stay in-window; its exit (JZ→0x006B6D3E) targets the excluded continuation. Package rows 148 vs 133 reserved = +15, entirely SR2, entirely in-admission.

**Ruling: NO admission violation; NO retroactive authorization needed.** The region was admitted (EVENT 000009_ADMIT, 22:42:27.505Z) before extraction (22:43:29Z); no out-of-admission row was extracted or read; no unforeseen in-window body was opened. The event the parent disclosed is a **reserve-accounting overshoot** (148 actual vs 133 booked), honestly disclosed (COUNTERS note, REPORT §Counters, GATES G3). The pack's "no refund" phrasing is directionally moot — actual EXCEEDS reserve.

**Obligations for the parent:** (1) charge ACTUAL 148 instruction rows (not 133) to the campaign ledger totals; (2) record this adjudication; (3) apply correction QC-P07-3 to any future quotation of the overshoot wording.

## 7. Premise preservation & scoped negatives

- identical names/shapes ≠ common semantics: preserved (C4 premise: the three contexts may serve different request classes sharing the callback);
- definition registry ≠ instance source: preserved (no VFS-registry promotion; C2 carries P06's standing);
- no direct caller ≠ exclusively virtual: not counter-violated (no caller-census claim in P07; 8BD720 standing cited from P06 with its 22-CALL + 3-imm32 evidence);
- scoped negatives keep window bounds: **verified** (C2 window-scoped only with the merge question explicitly moved to un-admitted 745A70; C1's id2/tag-6 negative bounded to in-window).

## 8. Precise remaining edge (confirmed, consistent with HANDOFF/BACKLOG)

1. Consumer/transport bodies **0040B070, 0043E5B0, 006C3640** (request transport; none admitted anywhere in the campaign — verified against all CONTRACTS/REQUESTS/EVENTS).
2. **745A70** body — id2/class-20006-tag-6 property provenance + VFS→slot merge discriminator.
3. Upstream worklist/caller-frame provenance of **006B6C9D** (and the entry-ABI nuance, QC-P07-5).
4. Callback invocation census for **8BD720** — who invokes it and who consumes the returned &req+0x18 (P06 QC edge #1, now sharpened by P07-C3/C4: the three imm32 sites all pass 8BD720 through 40B070; the scheduler-side invoker remains unknown).

## 9. NOT_CHECKED (explicit)

- All out-of-window targets: bodies 745A70, 6B4120, 72FCE0, 7CE1E0, 43C700, 40B070, 43E5B0, 6C2E00, 733650, 6C3640, 8BD720 (P06's, inherited); fail path 745C40+; SR2 exit 6B6D3E+; SR4 exits 6D450E/6D4510+ — recorded-not-read (navigation only), per admission discipline; NOT semantically read by this reviewer either.
- Bridge context documents beyond citation-level verification (accepted as inherited labels exactly as the pack uses them).
- P01–P05 science (out of scope; P06 QC already adjudicated P06); campaign-wide budget arithmetic beyond this package (parent ledger); "attempt 2 added nothing" is a disclosed non-event with no disk artifacts (consistent, not independently provable).

## 10. FULL_READ_LOG

Pack P07_EXEC_R1 read to EOF: REPORT.md, CLAIMS.json, COUNTERS.json, GATES.json, HANDOFF.md, MEMORY_AND_IDENTITY.json, SOURCE_PINS.json, BARRIER_BACKLOG.json, CONTRACT.json, RUN_STARTED.json, MANIFEST.json, tools/extract_p07_subregions.py, all 4 extracts. Parent control: CONTRACTS/P07.json, REQUESTS/REQUEST_P07.json, EVENTS/000001_START.json, EVENTS/000009_ADMIT.json; authoring CONTRACT.md (§1–16, focus 5/6/9/12). Context: P06_EXEC_R1/REPORT.md (full), P06_QC_R1/QC_REPORT.md (full), P06_QC_R1/RUN_STARTED.json. Pinned source: rehashed; 148 admitted rows read directly; no semantic out-of-window read; citation-level corpus greps (7CE1E0/72FCE0/8BD720) and two CONTROL searches (case-sensitive + case-insensitive). Load-bearing unchecked components: NONE.

---

**Verdict: QC_PASS / PASS_WITH_CORRECTIONS. Findings: 0×P0, 2×P1 (QC-P07-1 counter breakdown data, QC-P07-2 missing artifact_index.csv), 2×P2 (QC-P07-3 overshoot wording, QC-P07-4 wording/citation nuances), 2×P3 (QC-P07-5 fragment/metric nuances, QC-P07-6 CALL-count ambiguity). Claims accepted 5/5 at adjudicated levels; rejected overclaims: none. Overshoot adjudicated: no admission violation, no retroactive authorization; parent must book actual 148 rows.**
