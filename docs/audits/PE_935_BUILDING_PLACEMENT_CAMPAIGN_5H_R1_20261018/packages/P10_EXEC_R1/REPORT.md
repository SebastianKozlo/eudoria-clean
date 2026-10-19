# P10 REPORT — Front C merge discriminator: the map read behind 745BF0 (body 0x00745A70)

RUN_ID = PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | PACKAGE = P10 (Front C) | Worker = pe-reconstruction (child, no delegation)
Admission ID = A6b8526417348 (ADMIT granted by parent before dispatch) | Region = 0x00745A70–0x00745B00 (end-exclusive), 57 rows, 0 calls.
Source = saved listing GHIDRA_H5_VTABLE2.txt (SHA256 642CC29A…CC1D8DB, 50,780,146 B, pin verified before any semantic read). Extract = EXTRACT_745A70_745B00.txt (source lines 809770–809826, SHA256 1E7091F73667448A622C10D0E99E0C6EAFDC352842DBBE97565E8E7340D76645).

## 1. What 0x00745A70 actually is (machine-level, from the 57 rows)

`0x00745A70` is a single self-contained **first-match linear scan** over an array of **8-byte entries**, bounded by two stack-supplied values, with a **one-byte** match criterion:

- **Consumed stack slots** (S_n = [ESP_entry + n*4]; entry-frame arithmetic incl. push-shift correction):
  - S1 → EAX = scan **start cursor** (MOV EAX,[ESP+0x4] @745A70)
  - S2 → EDI = scan **end** (MOV EDI,[ESP+0x14-0xC] @745A7F, 3 pushes corrected); **EDI is never written again** (the `MOV EDI,EDI` @745A8E is a self-move no-op)
  - S4 → ESI = **additive address base term** (MOV ESI,[ESP+0x18-0x8] @745A7A, 2 pushes corrected)
  - S6 → EDX = **match value** (MOV EDX,[ESP+0x18] @745A74)
  - **S3 and S5 are never read** — dead slots in this callee.
- **Main scan**: ECX = (S2−S1) `SAR 5` → count of 0x20-byte blocks; JLE skips if empty. Per block: 4 checks (unrolled), each `MOVZX`-loading the **first byte** of the entry at `[ESI + cursor]` and `CMP` against S6; cursor += 8 per entry; loop-back `JG @745A90`. 4-unroll + SAR 5 ⇒ **entry size 8 is a compile-time constant**.
- **Residual dispatch** (@745AC6): ECX = ((S2−cursor)>>3)−1; ==1 → single check @745AF2; ==2 → checks @745AE7+745AF2; ==3 → checks @745ADC+745AE7+745AF2; ==0 (and ≥4, unreachable for 8-aligned ranges) → fail @745AFA.
- **Return contract (std::find-shaped)**: on match, EAX = **cursor value of the START of the matching entry** (verified on all 7 match sites — the `ADD EAX,0x8` always precedes the compare for checks 2–4); on no match, EAX = **S2 (the end value)** via `MOV EAX,EDI` @745AFA. Caller distinguishes success by comparing to S2.
- **ABI**: no EBP frame; EBX/ESI/EDI preserved (3 push / 3 pop, balanced); `RET` **without immediate** (callee does not clean args); EAX/ECX/EDX clobbered.

## 2. Answers to the package question

**Q1 — What key does it match?** A **single byte**. The only comparison in the window is `MOVZX`-byte vs S6 as a full DWORD. Usable key space = S6's low byte (0–255); **S6 > 255 can never match anything** (zero-extended bytes are ≤255), i.e. a callsite feeding e.g. 20006 into S6 produces a **guaranteed always-fail** that returns S2 — a falsifiable caller-side implication. The caller's 4-DWORD key (P07-cited, incl. constant 4) is **not** consumed here as a composite: at most the DWORD landing in S6 acts as the match value, the one landing in S4 acts as an address base, and any landing in S3/S5 are dead (CLAIM P10-2/P10-4/P10-5).

**Q2 — What entry structure does it walk/return?** A flat (non-hashed, non-tree) array of **8-byte entries** in [S1,S2), byte-addressed as `[S4 + cursor]`, cursor ∈ {S1, S1+8, …}. **Byte 0 of each entry is the compared discriminator; bytes 1–7 are never read in-window** (their meaning — id2? class? pointer? padding? — is not established by this window). Returns the matching entry's position, or the end value on failure. Cursor duality (absolute pointer if S4=0 at the callsite, offset if S4≠0) is **not decidable in-window** (P10-8); P07's cited caller behavior "success returns *[EAX]" is consistent with S4=0 but cannot be cross-checked without the caller window.

**Q3 — Does the id2/class-20006-tag-6 property hypothesis survive?** **Not at the 0x00745A70 level — REJECTED_WITH_EVIDENCE (scoped).** The window contains a 1-byte match only; no immediate 20006 (0x4E26), 6, or 2 appears anywhere (immediate census: 0x1,0x3,0x4,0x5,0x8,0x14,0x18); a class-20006 value fed as S6 would be degenerate always-fail (Q1). What survives is only the **weaker caller-side variant**: the caller (745BF0 window) may select which byte tag to search and may interpret the entry payload as id2/class/tag data — that variant is **NOT_ESTABLISHED** here and moves to the caller edge (B1/B3, HANDOFF).

**Q4 — Any VFS-record-fed source visible in-window (FAMILY-P/T merge)?** **No — scoped negative with window bounds.** 0 CALL instructions; no absolute/global data address in any operand (all memory operands are [ESP+imm] and [ESI+EAX(+0x8)]); no I/O. The origin of the scanned array is **invisible in this window**; the FAMILY-P/T merge question is **NOT_DECIDABLE at this level**. The deciding evidence is the **writer/populator of the [this+4]/[this+8]-bounded array** (unknown VA, out of window). Per premise: absence in-window ≠ absence in the program.

## 3. Position in the campaign

P07 said "callee 745A70 performs the actual read" and moved the id2/tag-6 question here. P10 closes that move: the callee is a pure in-memory byte-tag scan; **the composite-key property reading is rejected at this level**, and the merge question is cleanly displaced onto two precise caller-side edges: (B1) the key-DWORD→slot mapping at the 0x00745C28 callsite, and (B2) the array populator. No VFS/parser/record semantics were found or claimed. Front C's first missing edge is therefore now sharper than before P10: it is no longer "what does the map read do" (answered: byte-tag linear scan) but "who feeds the array and which key byte is selected".

## 4. Counters (actual vs reserved)

- Reserved (contract): 1 body / 57 rows / edges 4 / 2 candidates. (Prompt paraphrase said "4 CALL"; contract file is authoritative — see COUNTERS.json disclosure. Actual CALL sites = 0 under either reading.)
- Actual: **1 body opened (0x00745A70), 57/57 rows exact (no overshoot), 0 CALL sites, 12 conditional branches, 0 unconditional jumps, 1 RET, 2 follow-up candidates identified.** No unforeseen bodies (0 calls ⇒ vacuous incident gate). Campaign contribution: 1 body / 57 rows / 0 CALL / 2 candidates.

## 5. Process and discipline

Window discipline: region located by address search (navigation); two navigation events disclosed — the search surfaced line 809950 (`CALL 0x00745a70` inside 745BF0, P07's window; address+mnemonic only, body not read) and the boundary line 809827 (0x00745B00, address-only scan). Content at/after 0x00745B00 not read. The DENIED Front-A item (007B6C4B continuation, FRONT_A_TIME_CAP, events 000011/000012) was not touched. All 4 contract premises preserved and applied (MEMORY_AND_IDENTITY.json). Real clock only. Gates: 13 PASS + 1 PASS_WITH_DISCLOSURE (RUN_STARTED preceded only by mechanical CONTRACT.json copy), 0 FAIL — overall PASS, run_status COMPLIANT.

## 6. Standing (unchanged by P10)

WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN, CANONICAL_GATE_EFFECT=NONE.

QC_ORIGIN=SELF_CHECK (this report's counters and gates are the worker's own self-check, labeled as such; independent QC belongs to the parent's reviewer per §12).
