# QC REPORT — P05 (Front B) independent internal review
# RUN_ID: P05_QC_R2_20261018 | parent campaign: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018

- REVIEWER: pe-master-auditor, fresh child session dispatched directly by PE-MASTER (NO_NESTED_TASKS; no delegation). Predecessor `P05_QC_R1` (marker-only, unavailable session) left untouched, per parent instruction.
- TARGET PACK: `packages\P05_EXEC_R1` — attribution **DIRECT_ANALYST_FALLBACK by the PE-MASTER parent** (CONTRACT §4) after two incomplete child executions (both markers preserved inside the pack). Full adversarial standard applied identically to any executor's pack; findings below apply to the parent's own fallback product and are reported as such.
- ADMISSION: A6929aee83fa4 (CONTROL/EVENTS/000007_ADMIT.json, 2026-10-18T22:04:24.594Z; reserve 6 bodies / 164 instructions / 12 edges / 4 candidates). This review opened NO new bodies (CONTRACT §12: re-checking the same extracts creates no new uncounted front).
- PINNED SOURCE: `GHIDRA_H5_VTABLE2.txt` — SHA256 `642CC29A...CC1D8DB` **recomputed by this reviewer** (50,780,146 B; 1,743,929 lines). Semantic read confined to the six admitted subregions; writer 0x005094C0 NOT read (not admitted); address searches = navigation only.
- QC VERDICT: **QC_PASS** (process verdict: **PASS_WITH_CORRECTIONS**) — all eight claims' core content independently re-derived and upheld; 2×P2 + 2×P3 findings registered; no science claim rejected.

## 1. Mechanical integrity (independently executed)

| Check | Result |
|---|---|
| MANIFEST re-hash (15 entries incl. 2 attempt markers) | 15/15 SHA256 match, 15/15 size match |
| Manifest bijection | HOLDS (only MANIFEST.json absent from its own list — self-excluded by design) |
| Line parity vs pinned source | **164/164 rows byte-identical** (R1: 145443-145450; R2: 1170926-1171004; R3: 1171005-1171021; R4: 1171022-1171044; R5: 1171144-1171172; R6: 1178571-1178578) |
| Window completeness | my scan of the pinned listing found exactly 8/79/17/23/29/8 rows in the six windows — extracts complete, zero missing, zero extra |
| Counters | 6 bodies / 164 rows (= reserve exactly) / 8 CALL (0+3+1+2+2+0; per-subregion split identical to COUNTERS breakdown) / 4 candidates — ALL MATCH |
| Chronology | ADMIT 22:04:24Z → CONTRACT 22:04:34Z → RUN_STARTED (child 1, empty return) 22:04:55Z → RETRY1 (child 2, empty return) 22:08:35Z → fallback extracts 22:12:28Z → reports 22:13:06Z → MANIFEST 22:13:09Z LAST — strictly ordered; no pre-admission action |
| Attribution honesty | fallback disclosed in REPORT header, MANIFEST.attribution, CLAIMS.attribution, COUNTERS.attribution, GATES.G6, HANDOFF; both child-attempt markers preserved (RETRY1's recorded hash of the first marker matches the manifest) — **UPHELD** (contract §4: "Ujawnij udział poszczególnych ról") |

## 2. Instruction-level verification of the decisive derivations (all six windows)

- **C1 (0x00509070)** — CONFIRMED: thiscall 3-DWORD setter, `arg1 → [ECX+0x80/+0x84/+0x88]` (8 rows verified; deltas exact: 4+2+6+3+6+3+6+3 bytes → RET 0x4 ends exactly at 0x00509091); **NOT an SF+30 link-setter** (no SF+30 access in window) — window-scoped negative upheld.
- **C2 (0x0085BFA0, the dominant producer)** — CONFIRMED: `[this+0x2C]` → vtable slot **+0x24** (index 9) indirect call with out-arg (`PUSH EDX` = frame ptr); **12 float loads from the returned EAX**; 21 FLD/FSTP shuffle pairs; `CALL 0x0096cb20`, `CALL 0x0096cf80`; **`REP MOVSD` ECX=9** copying 9 dwords from the 96cf80 output to arg1; `[out+0x24]/[out+0x28]/[out+0x2c]` written from stack; **`FLD1` → `FSTP [EAX+0x30]` = [out+0x30]=1.0**; `RET 0x4`. Every element of the parent-brief's decisive chain (FLD/FSTP shuffle + final store chain) verified verbatim against source lines 1170926-1171004. Nuance (F4 below): the net permutation of the 3×3 floats into the pre-96cb20 arg area is identity (column-major scatter with 0x10 stride + descending row-major regroup cancel); "transpose-like" is a code-pattern descriptor, not a proven net transpose.
- **C3 (0x0085C0C0)** — CONFIRMED: slot **+0x28** (index 10) pass-through with out-arg, 3 floats to arg1, returns record pointer (17 rows; ends exactly at 0x0085C0ED).
- **C4 (0x0085C0F0)** — CONFIRMED structure: calls **0x0085BFA0** (frame out-record), **REP MOVSD ECX=9 copies the 3×3 part to [ESP+0x8]** (verified disjoint from the saved-register slots — full stack arithmetic re-derived: saved ESI at E-0x5C, saved EDI at E-0x60, copy at E-0x58..E-0x34), **zeros {0,0,0} to arg1** (FLDZ + FST [ESI]/[ESI+4]/FSTP [ESI+8]), `CALL 0x0096cd10` with **ECX = the copied 3×3** ([ESP+0xc] at ESP=E-0x64 ≡ [ESP+0x8] at ESP=E-0x60) and record as stack arg, returns record. STRONGLY_SUPPORTED (96cd10 semantics un-admitted) — level appropriate.
- **C5 (0x0085C280)** — core structure CONFIRMED (gate byte `[this+0x24]`; slot **+0x160** called with 0x80, AL-gated; slot **+0xdc** with out-arg; 3 floats to arg1; RET 0x4) — **but with FINDING F1 (P2)** below on the un-taken branches.
- **C6 (0x00862850)** — CONFIRMED: **RAW FIELD COPY** `[this+0x3C]/[this+0x40]/[this+0x44] → arg1`, no calls, no computation (8 rows; ends exactly at 0x00862868); premises honestly keep field semantics unknown.
- **C7** — composition claim; **STRONGLY_SUPPORTED is the correct level** (writer 0x005094C0 link is inherited P04 standing — correctly NOT re-derived here since un-admitted; slots un-admitted; countermodel "slot +0x28 may return a raw stored local translation" honestly recorded). ACCEPTED.
- **C8** — window-scoped negative CONFIRMED: no admitted subregion reads/writes SF+30; 509070 rejected as THE link-setter; root-vs-internal node remains UNDETERMINED. ACCEPTED.

## 3. Findings

**P05-QC-F1 (P2) — 85C280's un-taken branches target 0x0085C2D1, OUTSIDE the admitted window; "none truncated" is contradicted; C5's disposition sub-claim is not provable in-window.**
Source: `extracts/R5_85C280_85C2D1.txt` rows 1171148 (`0085c28a JZ 0x0085c2d1`) and 1171155 (`0085c2a0 JNZ 0x0085c2d1`); window [0x0085C280, **0x0085C2D1**) end-exclusive. On both taken paths the frame is uncleaned (ESP=E-0x10, saved ESI still pushed), so 0x0085C2D1+ necessarily contains further instructions of the logical body (at minimum a shared cleanup/return) that were **not read**. Contradicted claims: (a) COUNTERS note "all six logical functions fully in-window, none truncated" — FALSE for R5 (R1/R2/R3/R4/R6 verified to end exactly at their window ends); (b) C5 sentence "Un-taken paths leave the record untouched" — NOT_ESTABLISHED in-window. Correction: downgrade that sub-claim to PLAUSIBLE; record gap VA **0x0085C2D1**; fix the counters note. Skutek: C7's dominant-route conclusion unaffected (the flag-1 path is fully in-window and ends RET 0x4), but the "stale-frame variant of P04 V3 remains live" argument must not cite the un-taken-path disposition as established. Revalidation: admit [0x0085C2D1, ~0x0085C2E0) and verify the shared tail writes nothing to arg1.

**P05-QC-F2 (P2, procedural — attributed to the parent's fallback execution) — pack does not meet CONTRACT §12 minimum artifact set / its own required_outputs.**
Missing: `MEMORY_AND_IDENTITY.json` (no memory/write-set/identity ledger for the six windows), dedicated `SOURCE_PINS.json` (pin only inside RUN_STARTED/MANIFEST), `artifact_index.csv` (explicitly required by the pack's own CONTRACT.required_outputs); extracts lack §6 per-extract headers (source SHA, admission ID). The DIRECT_ANALYST_FALLBACK authorization (§4) covers executing the science on the same contract/admission — it does not waive §12's artifact minimums. Science unaffected: this review independently verified all claims from the extracts + pinned source. Correction: parent corrigendum note (new R2/corrigendum; never edit the frozen pack).

**P05-QC-F3 (P3) — the "4 candidates" are never enumerated** (count matches reserve; reconstructible from CLAIMS; not traceable). Enumerate in the corrigendum.

**P05-QC-F4 (P3) — C2 "3x3 transpose-like shuffle" wording**: net permutation of the 9 matrix floats into the pre-96cb20 argument area is IDENTITY (re-derived from the 21 FLD/FSTP pairs' ESP-relative arithmetic); keep "reordered via strided scatter/regroup", do not cite a proven transpose. C2's load-bearing conclusion (computed, virtual-delegated, not raw) is unaffected.

## 4. Rejected overclaims

None at claim level. C1-C6, C8 CONFIRMED as scoped; C7 STRONGLY_SUPPORTED (correct level). The over-precision in C5's last sentence and the counters note is corrected (F1), not rejected wholesale — the valid layers of the claim are preserved.

## 5. Precise remaining edge (confirmed, plus reviewer addition)

As stated by the pack (HANDOFF/BARRIER_BACKLOG): (1) class/vtable identity of `[this+0x2C]` and slots +0x24/+0x28 (+0xdc/+0x160) targets; (2) 0x00862850 receiver class and +0x3C field semantics (006A36F0 arg1 provenance); (3) helper bodies 0096cb20/0096cf80/0096cd10; (4) SF+30 writer — 509070 rejected for this role. **Added by this review:** (5) the 0x0085C2D1 shared tail of 85C280 (un-admitted; bounds the un-taken-path disposition of C5/P04-V3 stale-frame variant).

## 6. Scoped negatives & premises

- Scoped negatives keep window bounds: verified — C8 and C1's SF+30 negatives are window-scoped only; C6's "raw bytes yes, semantic role UNVERIFIED" is honest.
- update mechanism ≠ source: preserved in C7's premises (computed route ≠ historical record restore; helper semantics un-admitted).
- vtable match ≠ receiver identity: preserved (receiver classes unknown throughout; REPORT "Remaining edge" reflects it).
- No direct caller ≠ exclusively virtual: not applicable to this pack's windows (no caller census was claimed); no violation.

## 7. NOT_CHECKED (explicit)

- Writer 0x005094C0 region, helper bodies 0096cb20/0096cf80/0096cd10, virtual slot targets (+0x24/+0x28/+0x160/+0xdc implementations), 0x0085C2D1+ shared tail, 0x006A36F0, data barriers (0x00A7AF80, 0xA7957B, slots 0x00A75A38/44/5C/40), P04 context docs (cited, not re-derived), VTABLE_INVENTORY.csv / GA3_VTABLE_ENTRIES.json (HANDOFF suggestions, unread), earlier packages P01-P04, campaign-wide budget ledger.
- No EXE/payload/runtime/config/repo actions performed; frozen pack and parent CONTROL untouched; no new bodies opened.

## 8. FULL_READ_LOG

Pack P05_EXEC_R1 read to EOF (all 15 files, incl. both attempt markers and all six extracts). Parent control read: CONTROL/EVENTS/000007_ADMIT.json; authoring CONTRACT.md §4/§6/§12. Pinned source: hash/size/line-count verified; 164 admitted rows read and byte-verified; window scans executed for all six windows; no out-of-window semantic read.

**Verdict: QC_PASS / PASS_WITH_CORRECTIONS. Findings: 0×P0, 0×P1, 2×P2 (F1, F2), 2×P3 (F3, F4). Attribution honest. Counters exact. Mechanical integrity perfect.**
