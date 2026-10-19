# P01_QC_R1 — Independent Internal QC Report (RETRY 1 of 1)

RUN_ID: PE_935_P01_QC_R1_20261018 | PARENT LOOP: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | TARGET: packages\P01_EXEC_R1 (immutable, 15 artifacts)
Reviewer: pe-master-auditor (fresh session; no delegation; NO_NESTED_TASKS) | Started 2026-10-18T21:25:22Z | Review type: INTERNAL_QC (worker pack carried qc_origin=SELF_CHECK; this is the independent pass)
Scope: Front A, priorities A1+A2/A2b, the two admitted windows only (0x006B1C60-0x006B1E00 @Adc52ad119303; 0x007D27B0-0x007D291E @Ab6ebb24f3a07). No EXE/payload/runtime/config actions; no repo/CONTROL/canonical mutation; no bodies beyond the two admitted regions.

## 1. Verdict summary

- **QC_VERDICT: QC_PASS** (scientific content) — every load-bearing worker claim was independently re-derived from the pinned saved listing and confirmed; no claim contradicted by physical evidence; no gate invalidated.
- **PROCESS_VERDICT: PASS_WITH_CORRECTIONS** — 2 P2 factual/consistency corrections and 2 P2 premise-completeness additions are required in a future corrigendum (the sealed package stays immutable per contract §12/§13); 3 P3 cosmetic notes. None of the corrections changes any total, gate result, or scientific conclusion.

## 2. Physical integrity (re-hash / bijection)

- Pinned source re-hash: GHIDRA_H5_VTABLE2.txt SHA256 = 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB, 50,780,146 B — **matches contract pin** (recomputed at review).
- Worker manifest re-hash: **all 14 listed artifact SHA256s recomputed and match exactly** (CONTRACT.json 42ee114c…, RUN_STARTED aca68afe…, SOURCE_PINS 00d58bdc…, EXTRACT_REGION1 71b83f5c…, EXTRACT_REGION2 d783257f…, ANALYSIS_NOTES f63d8bc0…, CLAIMS ab410ce2…, MEMORY_AND_IDENTITY 695a8313…, COUNTERS f4066741…, BARRIER_BACKLOG b4719086…, REPORT a5e0e85e…, HANDOFF d83099c8…, GATES 06a48d6e…, artifact_index 8336d39c…). MANIFEST.json self-excluded; reviewer-computed hash a1d114e590e37d60bc099224fa09b916417b1a9d225abf1c208adbfd9c02940a (7143 B) — SOURCE_FILE_UNCHANGED and MANIFEST_IDENTITY_CORRECT both hold.
- Bijection: 14 listed + 1 self-excluded = 15 disk files; **no duplicate rows, no case-alias collisions, no unlisted strays**. CONTRACT.json is a byte-identical copy of CONTROL\CONTRACTS\P01.json (hash equality verified).

## 3. Independent re-derivation (what I did myself)

I re-read the pinned listing directly (not the worker's extracts): lines 626419-626546 and 995326-995437. The two boundary lines on each side were used ONLY for VA/boundary-integrity (end-exclusive cut) checks — the worker's own SOURCE_PINS boundary_note discloses the same boundary lines and their handling, which my check confirms was honest. Full line-numbered rederivations: RECHECK_NOTES.json. Highlights:

- **Line parity: PASS.** Both worker extracts are byte-identical to the source listing row-for-row (126 rows @626420-626545; 110 rows @995327-995436). Window cuts are exact: line 626546 starts at VA 006b1e00 (= end-exclusive end; the extract correctly stops before it), line 995437 starts at 007d2920 (next body after RET 007d291d).
- **Region 1 store census (all 126 rows): PASS.** I enumerated every memory-writing instruction myself. Non-frame stores in the window: only `[EAX]=0xa85454` (006b1c62; EAX=ECX=this of the 4-row stub), `[0x00BA7220]=1` (006b1c68, global flag) and `[EDI]=EAX` (006b1d0a). All other explicit writes are the walker's own frame/SEH/container slots. **No [elem+8] store — the only +8 accesses are READS** (006b1d89 `MOV EDX,[EAX+8]`, 006b1da4 `MOV EAX,[EDX+8]`, both vtable-slot loads feeding virtual calls). No receiver-pointer store, no resource-ID compare, no keyed lookup.
- **[EDI]=[ESP+0x2c] pinning: PASS (recomputed instruction-by-instruction).** Frame arithmetic independently reproduced: prologue consumes 0x6C below entry ESP (3 pushes 0xC + SUB 0x4c + 4 pushes 0x10 + cookie push 0x4; the PUSH EBP at 006b1cb4 is the 0-argument to CALL 0043ba10, callee-popped — the only reading consistent with all later [ESP+off] references), so **[ESP+0x70] = entryESP+4 = the single by-value stack argument**. Chain verified: `LEA ECX,[ESP+0x20]` (frame-local 10-dword container header, zero-init 006b1cbe-006b1ce2) → CALL 0043ba10 → `MOV EDI,[ESP+0x2c]` (006b1cef, insert-cursor field) → `MOV EAX,[ESP+0x70]` (006b1cf3, ARG1) → **`MOV [EDI],EAX` (006b1d0a)** writes the caller-supplied root value into the walker's own worklist storage; cursor advance `[ESP+0x2c]=EDI+4` (006b1d0f). The postaudit's open EDI-origin point is genuinely closed at the explicit-store level, with the worker's premise-level countermodels (allocator aliasing, member-internal aliases via the two ECX=elem virtuals, indirect [0x00A759FC] free) preserved, not silently dropped.
- **Region 2: PASS with one wording correction.** vptr install `MOV [ESI],0xa8ec24` @007d27d9 = **instruction-fact**; complete write-set census (my own) = this-relative stores ([this], [this+4], [this+12C], [this+144], [this+194], member+4 refcount) + frame/SEH only; only argument is ECX=this (prologue PUSH ECX is a slot reused as the this-save; epilogue `ADD ESP,0x10` balances the pushes exactly → no caller stack args; plain RET). **The [this+0x148] free is an instruction-fact** (007d288a `MOV EAX,[ESI+0x148]`; TEST; JZ skip; free path 007d28a6-007d28c0 via 0095dd6c(0x79fc70,[ptr-4],4,ptr) then 0095db40([ptr-4])) — null-guarded, and the +0x148 field itself is never nulled in the window. Its identification as the holder of the post-load V read is correctly labeled inference via the cited postaudit premise (citation verified: postaudit REPORT.md L9 contains exactly "V=M32[M32[obj+148h]] … store *out=V i retain" and "obiekt NiStream z vptr 00A8EC24"; L19 contains the open [EDI]=EAX/EDU-origin point as cited).

## 4. Accepted claims (with statuses I assign after re-derivation)

| Claim | My re-derivation result | Status accepted |
|---|---|---|
| P01-C1 (no identity bridge in window; full 126-row census) | Census reproduced; only non-frame stores are vtable install, global flag, deque insert; +8 only read | **ACCEPT CONFIRMED** (scoped to window; countermodel preserved) |
| P01-C2 (region = factory vtable/flag stub + type-directed walker; mechanics) | All mechanics reproduced: ARG1 seeding, deque insert/pop/advance, 0x80 chunk free via [0x00A759FC](chunk,0x80), vtable+8 virtuals with ECX=elem, [result+4] parent chains, node matches 0xBA7218→branch / 0xBA7210→leaf, children [EBX+0xCC]/[EBX+0xD4] with 4-byte stride | **ACCEPT CONFIRMED (mechanics)**; "scene-graph walker" naming stays STRONGLY_SUPPORTED (not promoted) |
| P01-C3 (type66+ID A join unaddressed; no keyed logic in windows) | Immediate census over all 236 rows: no 0x42/66, no 296445/0x4861D, no ID compares, no keyed table access | **ACCEPT CONFIRMED (absence in windows)**; global join stays NOT_ESTABLISHED |
| P01-C4 (006B1C80 explicit stores cannot reach outslot/V; [EDI] pinned) | Frame arithmetic + pinning chain independently reproduced; opaque residuals correctly preserved | **ACCEPT STRONGLY_SUPPORTED** (explicit-store scope, premise-level countermodels preserved) |
| P01-C5 (007D27B0 = NiStream teardown mechanics) | All mechanics reproduced; ONE wording correction (see 5.1) | **ACCEPT mechanics CONFIRMED** with correction; dtor-class naming stays STRONGLY_SUPPORTED/CONDITIONAL (dtor vs Close) |
| P01-C6 (007D27B0 cannot write outslot/V via explicit stores/arguments) | Write-set + argument census reproduced exactly | **ACCEPT STRONGLY_SUPPORTED** (premise-level countermodels preserved) |
| P01-C7 (frees +0x148 holder → Q premises must drop holder-liveness, track retain) | Free path instruction-fact verified; premise chain verified at citation level; see 5.3 premise additions | **ACCEPT STRONGLY_SUPPORTED** (free CONFIRMED in-window; V/Q bearing conditional on cited premises) |
| P01-C8 (body-entry map correction) | JZ targets at source lines 626463/626483/626510 verified — all three are in-window branch targets of 006B1C80 | **ACCEPT CONFIRMED** (factual correction of the contract's body-entry map) |

Preserved-distinction compliance: verified. No equality assumed across V_first/V_reload/Q0/Q1/VT (no such claim made); "no direct caller ≠ exclusively virtual" not misused; vtable matches kept as class/type identity only; explicit-store ≠ final-value-after-opaque-calls kept (both A2/A2b conclusions are explicit-store-scoped with residuals enumerated); heap/stack disjointness labeled premise; NiTArray +CC/+D4 cross-confirmed on branch elements. Scoped negatives keep their bounds — none of the absence claims was promoted to a global negative.

## 5. Corrections required (corrigendum items; sealed package stays immutable)

**5.1 [P2] Pass-attribution error for the +0x194 null store (CLAIMS P01-C5, ANALYSIS_NOTES R3).**
- Evidence: source lines 995359-995368 — the `MOV [ESI+0x194],0x0` @007d282b executes in the FIRST +0x194 pass (merge point after first decrement/conditional-destroy, BEFORE the +0x128 release); the second pass (007d2847-007d2860, lines 995376-995384) contains NO null store.
- Skutek: wording contradicts the instruction order. No impact on C5 mechanics, the C6 write-set census (the store exists either way), C7, counters, or gates. Note the corrected reading adds a small honest nuance: after the first pass nulls the field, the second pass re-tests it and can only act if the intervening +0x128 release re-populated the field (opaque channel — consistent with the worker's residual enumeration).
- Correction: "(twice; the FIRST pass also nulls the field after decrement/conditional-destroy; the second pass re-tests it)".
- Revalidation: re-read lines 995368 and 995376-995384 — confirm no store to [ESI+0x194] after the second destroy call.

**5.2 [P2] CALL-breakdown arithmetic errors in two summary fields.**
- REPORT.md line 43: "6 virtual releases/destroys … 6× 0095db40" — actual 5 and 5 (breakdown sums to 16 vs the true 14; contradicts the report's own correct totals 19 and COUNTERS' correct 14-entry detail list). COUNTERS.json indirect_sites: "EDX x4 (region2 virtuals)" — actual EDX x5.
- Skutek: none on totals/gates/conclusions; the authoritative detail lists are correct.
- Correction: "5 virtual releases/destroys … 5× 0095db40"; "EDX x5 (region2 virtuals)".
- Revalidation: recount CALL rows at source lines 995349-995428 (my census in COUNTERS_RECHECK.json is the reference).

**5.3 [P2] Premise-completeness additions (record, do not soften, any conclusion).**
- P01-C7 must add the **same-instance premise**: the vptr 0xA8EC24 match proves same CLASS, not that the 007D27B0 call on the 0082E750 path receives the same object whose +0x148 was read (the preserved "vtable match ≠ runtime receiver identity" distinction applies at instance level too). Without it, "the V-holder is dangling after this call" is conditional on instance identity at the call site.
- P01-C7 should state explicitly that the free is **null-guarded** (TEST EAX,EAX / JZ skip) — on the postaudit's success path the holder was non-null, so the conditional is satisfied there, but the guard belongs in the claim body.
- P01-C4's window-wide sentence ("no explicit store in the window reaches the caller's outslot or V cell") implicitly covers the stub's stores; add the (postaudit-consistent) premise that the outslot/V cell is not the fixed global 0x00BA7220 and does not lie within the stub's this-object. 
- Skutek: without these, the premise ledgers are incomplete even though every conclusion currently drawn remains valid under the postaudit's frame-local placement of the outslot and the same-instance call context.
- Revalidation: presence-check of the added premise strings in the corrigendum; no new region read required.

**P3 cosmetic notes (no action required for science):** G6/HANDOFF "~21:31Z/~21:30Z" vs actual final mtime 21:21:16Z (conservative direction); MANIFEST manifest_written 21:21:01Z vs final write 21:21:16Z (disclosed refresh; content verified correct); CONTRACT.json copy written 24 s before RUN_STARTED.json (benign input-receipt ordering — the worker's own run outputs still start with RUN_STARTED as the contract's output list requires).

## 6. Rejected overclaims

None. I found no claim that outruns its evidence: the worker did not promote window-scoped absences to global negatives (C3 stays NOT_ESTABLISHED globally), did not equate V/Q variants, did not claim receiver identity from vtable matches, and labeled dtor/deque/scene-graph namings as hedged semantics rather than RTTI facts. The two breakdown/wording defects in 5.1-5.2 are factual errors inside otherwise-correct summaries, not overclaims of evidence level.

## 7. Precise remaining edge (confirmed as the correct next target)

FIRST_MISSING_EDGE stands as the worker scoped it: **WHERE the resource-ID→element→receiver binding is stored** — no keyed logic exists in either admitted window; the top-priority un-admitted location is the tail of 006B1C80 (0x006B1E00-0x006B1F40, incl. leaf path 006b1e2f and exits 006b1f28/006b1f34, est. ~90 rows, 1 body; would bring Front A to 4/16 bodies, ~326/1800 rows — inside caps), then the caller of 006B1C60, then W1/cache code. My boundary check incidentally confirms the deque-insert store pattern continues at 006b1e00 (the first out-of-window row) — the worker never claimed otherwise and its honest-limits statement matches. Secondary: retain-before-teardown ordering in 0082E750 (P01-B3) to convert C7's CONDITIONAL refinement into a closed premise.

## 8. Counters and chronology (recheck verdicts)

- Bodies 3/6, rows 236/236, CALL 19/19, candidates 4/4 — all recomputed and correct (COUNTERS_RECHECK.json); Front A caps 3/16, 236/1800, 19/64, 4/12 — correct.
- Chronology: ADMIT 000002 (21:14:13Z, Adc52ad119303, reserve 5/126/5/2) and ADMIT 000003 (21:14:15Z, Ab6ebb24f3a07, reserve 1/110/14/2) both match the contract regions/reserves exactly and precede RUN_STARTED (21:14:37Z) and the extract mtimes (21:18:12Z). All artifacts sealed by 21:21:16Z, inside the 21:49:25Z handoff target and 21:58:31Z wall cap. No retroactive authorization; no scope creep.
- Worker gates G1-G10: independently confirmed where checkable (G1 contract hash, G2 source hash, G3 scope/boundary handling, G4 extract integrity+line parity, G5 budget, G6 time, G8 honest negatives, G9 premises, G10 outputs/bijection). G7 (no forbidden access) accepted at pack level: no artifact, path, or mtime suggests EXE/payload/runtime/Ghidra/old-script/frozen-root/config/repo access; this review performed none either.

## 9. Review limits (NOT_CHECKED)

- No region beyond the two admitted windows was semantically read by this review (006B1C80 tail, 0082E750, 006B1FD0, helpers 0043ba10/0043ca60/007d1d70/007d16b0/0095db40/0095dd6c, [0x00A759FC] target) — they remain premise-level opaque exactly as the worker scoped them; my acceptance preserves that level.
- Worker session-log tool outputs were not replayed; underlying facts were verified directly instead. campaign_control.py was not re-run (read-only QC; parent owns the clock).
- Context docs (CAND4 postaudit REPORT.md, SCIENCE_CHECKPOINT.json) were verified at citation level only (cited premises confirmed to exist verbatim; postaudit SHA256 at review: c4288e8386d68802bb46a3a651b5abb47d9b0e91d6cf9eeccf9516d30e3f3e3c) — not re-derived from 0082E750/0082E580 bytes.
- Full read log: all 15 worker artifacts read to EOF; pinned source read at lines 626419-626546, 995326-995437 (boundary rows VA-check only); parent P01.json, CONTRACT.md (sections 1-16, incl. required 5/6/12), CONTROL EVENTS 000001-000003 listed and 000002/000003 read in full.

## 10. Handoff to PE-MASTER

- Independent re-derivation **was** performed (no honest-inability declaration needed).
- Next parent action: decide on the worker's REQUEST for region 0x006B1E00-0x006B1F40 (006B1C80 tail) — my QC supports it as the correct A1 continuation; optionally route P01-B3 (0082E750 retain ordering) as its own package. Materialize the 5.1-5.3 corrections as a corrigendum/R2 or fold them into the campaign synthesis (frozen P01_EXEC_R1 must not be edited in place).
- This QC is internal; it does not close Front A, does not promote any standing, and leaves QC_ORIGIN for the package as now independently reviewed at the campaign level.
