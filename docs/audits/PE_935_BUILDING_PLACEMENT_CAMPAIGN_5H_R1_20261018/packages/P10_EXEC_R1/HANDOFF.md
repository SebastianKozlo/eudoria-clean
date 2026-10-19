# P10 HANDOFF — to PE-MASTER

RUN_ID = PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | PACKAGE = P10 (Front C) | run_status = COMPLIANT (gates overall PASS, see GATES.json)

## 1. Out-of-window targets — exact VAs, NOT read in P10 (do not silently open)

| VA | What it is | Why out of window | Next use |
|---|---|---|---|
| 0x00745BF0 | caller wrapper (key builder + result interpreter; P07's admitted window) | outside P10 region 0x00745A70–0x00745B00 | B1/B3/B4: re-admission needed for NEW semantic analysis; OR reviewer may re-check P07's existing extract under reviewer rules (parent contract §12: re-checking the same extract does not create a new uncounted front) |
| 0x00745C28 | callsite `CALL 0x00745a70` inside 745BF0 (seen as address-search navigation hit, line 809950; mnemonic only) | inside 745BF0 body | included in any B1 admission |
| 0x00745C40 | P07-cited fail-path exit target of 745BF0 | outside both windows | only after B1 |
| 0x00745B00 | body immediately following 745A70's RET (identity unknown — address only) | region end-exclusive | unclaimed; no question currently requires it |
| UNKNOWN | populator/writer of the scanned array (stores to the [this+4]/[this+8]-bounded range and/or S4-based memory) | no VA visible in P10 window (0 calls, 0 global refs) | B2: needs a discovery anchor from saved listings; this is the FAMILY-P/T merge decision point |
| UNKNOWN | consumer of entry payload bytes 1..7 | unread in P10 window | covered by B1 (post-call) or B2 (writer) |
| 0x007B6C4B | Front-A backlog continuation | DENIED by helper (FRONT_A_TIME_CAP, events 000011/000012) | stays in backlog; do NOT admit under Front A cap |

## 2. Merge discriminator verdict (what the parent needs for FAMILY-P/T)

1. 745A70 = **byte-tag linear scan** (8-byte entries, byte-0 discriminator, match byte = slot S6 low byte, return = entry position or end value S2). **Not** a hash/tree/RTTI/serializer structure; **no** VFS/parser/record-feeding operation in-window.
2. The caller's **4-DWORD key is not consumed as a composite match key** by this callee (only S6 can match, S4 is an address term, S3/S5 are dead). id2/class-20006/tag-6 as a composite-key property lookup is **REJECTED at the callee level**; the surviving caller-side variant (caller picks the tag byte; payload carries identity fields) is **NOT_ESTABLISHED**.
3. FAMILY-P/T merge question **NOT_DECIDABLE at this level** — displaced to two edges: **B1** (key-DWORD→S6 mapping at 0x00745C28; also settles cursor duality B4 and payload reading B3) and **B2** (array populator identity). Recommended next package: B1 (cheapest, single already-listed body, directly answers "can the tag byte be 6 or 4 at this callsite"); B2 needs a new anchor and likely costs more.

## 3. Handoff facts for the next package

- If B1 is admitted: ask specifically for the caller's stack writes/pushes mapped to callee slots S1..S6 (P10's slot arithmetic is in CLAIMS.json P10-2 — reuse it, do not re-derive). P07's saved extract of 745BF0 already exists in P07_EXEC_R1; the parent decides reviewer-recheck vs fresh admission.
- Falsifiable implication already in hand (from P10): **if S6 at 0x00745C28 is ever >255 (e.g. 20006), the lookup always fails and returns S2** — a caller-side arithmetic fact that constrains any tag-6/tag-4 reading.
- Premises to keep enforcing: identical shapes ≠ common semantics (do not canonize "PropertyMap::find" naming); definition registry ≠ instance source; scoped negatives keep window bounds (no-VFS-in-window ≠ not-VFS-fed); no direct caller ≠ exclusively virtual.

## 4. Package contents (all under packages\P10_EXEC_R1)

CONTRACT.json, RUN_STARTED.json, SOURCE_PINS.json, EXTRACT_745A70_745B00.txt, CLAIMS.json, MEMORY_AND_IDENTITY.json, COUNTERS.json, BARRIER_BACKLOG.json, REPORT.md, HANDOFF.md, GATES.json, artifact_index.csv, MANIFEST.json (written last, self-excluded). Exact hashes in artifact_index.csv / MANIFEST.json.

Standing unchanged: WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN, CANONICAL_GATE_EFFECT=NONE. QC_ORIGIN=SELF_CHECK; independent QC pending at parent.
