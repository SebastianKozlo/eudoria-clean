# P04 HANDOFF — to PE-MASTER (parent campaign continues)

RUN_STATUS: COMPLETED (all contract outputs materialized; package scope closed within deadline)
Package: P04 (Front B1) | Worker: pe-reconstruction | Admission: A0af4119f1ccf (respected exactly)
RUN_STARTED 2026-10-18T21:49:38Z; materialization finished before 2026-10-18T22:25:00Z hard stop.

## Scoped result (one sentence)

The SF position writer 0x005094C0 is a thiscall copy-setter of a pointer-supplied 12-byte triple; in the four admitted callers the record is transform-shaped data with NO ID/parent/rotation channel, produced by getter callees OUTSIDE this admission (dominant: 0x0085BFA0 out-buffer tail at +0x24, witness R4; R5: 0x0085C0C0 return), so the exact data-route gap is the getters' read semantics — NOT yet the historical source.

## Exact next admissions requested (priority order)

1. **0x0085BFA0** (record producer, R2/R3/R4; R4 = discriminating witness) — closes V1/V2/V3: what it reads on its receiver and how many bytes it writes at out. Highest value per cost.
2. **0x0085C0C0 + 0x0085C0F0** (R5 paired position/rotation getters, 0x30 apart, both on arg1 with out=&local) — closes V4 and identifies the R5 source-object fields.
3. **0x00509070** (SF method receiving getter-returned pointer in R2/R3/R4) — candidate SF+30/NiNode-link setter; the node-role (root vs internal NIF node) identity edge.
4. **0x00509510** (rotation setter) — confirms the paired rotation field layout; cheap.
5. Optional: **0x0067C7C0 continuation** (from 0x0067C921/JMP 0x0067C923 + epilogue) and **0x006C0D50** (0x130-record ctor with lookup result) — the R5 spawn/copy path's instance-record construction; plus callers-of-0x0067C7C0 navigation.
6. Un-admitted writer callsites (parent already flagged 0x004B31E0, 0x005F61F0; newly inventoried: 0x00527BA8+0x00527BF0, 0x00528317, 0x00529020, and the two extra in-family callsites 0x0067B8E8, 0x006A3A2D) — any of these may pass an ID-bearing record; the admitted four do not.

## Precise remaining edge

The record's byte producer (85BFA0/85C0C0 family) is identified but unread; the receiver-of-record identity chain (509070 → SF+30? → which NiNode) is identified but unread; the R2 (85C280 vs 85BFA0) and R3 (862850 vs 85BFA0) ambiguity is structural (both geometries fit exactly: 4x4 translation row at &F+0xC+0x30 vs 4x3 tail at &F+0x18+0x24) and resolvable only by reading 85BFA0's extent.

## Barriers (data, not admission)

- qword [0x00A7AF80] value, constant 0xA7957B, function-pointer slots [0x00A75A38]/[0x00A75A44]/[0x00A75A5C]/[0x00A75A40]: DATA addresses; the pinned listing is code-only. Resolving requires a corpus document containing them; otherwise remains a barrier (EXE forbidden).

## Counters (actual; reserved in parentheses)

- bodies 5 (5) — R5 window truncated at admission boundary; epilogue un-admitted
- instruction rows 291 (291) exact
- CALL sites 47 (47) exact; 28 unique targets (24 direct + 4 indirect)
- candidates 4 (4) exact
- semantic reads outside admission: 0; navigation greps only (12 writer callsites inventoried, 8 un-admitted NOT read)

## Files

- CONTRACT.json, RUN_STARTED.json, SOURCE_PINS.json, CLAIMS.json (C1–C10 with premises/countermodels/evidence levels), MEMORY_AND_IDENTITY.json, COUNTERS.json, BARRIER_BACKLOG.json, REPORT.md, HANDOFF.md, GATES.json, artifact_index.csv, MANIFEST.json (LAST, self-excluded), extracts/R1–R5 (+ SHAs in SOURCE_PINS/artifact_index), tools/extract_subregions.ps1.

## Standing labels (unchanged, per parent contract)

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. No promotion performed or implied.
