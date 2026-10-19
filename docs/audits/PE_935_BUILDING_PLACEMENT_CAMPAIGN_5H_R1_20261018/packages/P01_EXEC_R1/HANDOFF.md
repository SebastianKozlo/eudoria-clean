# P01 HANDOFF — to PE-MASTER

RUN_STATUS: **COMPLETED** (all contract section-12 minimum outputs materialized; Front A wall cap respected; no scope expansion; no forbidden access; no new regions beyond the two admissions)

## Scoped result (one paragraph for the controller)

**A1: The identity bridge is NOT in region 0x006B1C60-0x006B1E00.** The window contains only (a) factory class-bootstrap 006B1C60 (`[ECX]=0xA85454` vtable install, `[0x00BA7220]=1` flag — class identity, not registration of any resource) and (b) a type-directed worklist walker 006B1C80 (partial in window; type nodes 0xBA7218/0xBA7210, children via +CC/+D4). No key, no ID compare, no [elem+8] store, no receiver pointer. **Type66+ID A → 296445: NOT_ESTABLISHED, unaddressed by this region** — no keyed logic exists in either window. **A2: 006B1C80's explicit stores cannot reach the outslot or V** (the open `[EDI]=EAX` store is pinned to the local deque insert cursor; STRONGLY_SUPPORTED, premise-level countermodels preserved). **A2b: 007D27B0 is the NiStream teardown (vptr 0xA8EC24)** — it cannot write outslot/V via explicit stores or arguments, **but it frees the +0x148 holder** (the exact holder of the post-load V read), so Q-preservation premises must drop holder-liveness and track retain-dependence (STRONGLY_SUPPORTED refinement).

## Precise remaining edge (FIRST_MISSING_EDGE, scoped to P01)

WHERE the resource-ID→element→receiver binding is stored. Priority: (1) un-admitted tail of body 006B1C80 (0x006B1E00→~0x006B1F40; leaf path 006b1e2f, exits 006b1f28/006b1f34; est. ~90 rows, 1 body) — **REQUEST_*.json admission needed from parent**; (2) caller of 006B1C60 (who installs the factory object / reads flag 0xBA7220); (3) W1 cache/registry code outside this package.

Secondary open premise: retain-before-teardown ordering in 0082E750 (needs 0082E750 admission) — would close P01-C7's CONDITIONAL refinement into the Q0/Q1/VT preservation chain.

## Actual counters vs reservations

| Counter | Reserved | Actual |
|---|---|---|
| Bodies | 6 | 3 (006B1C60 complete, 006B1C80 partial-window, 007D27B0 complete; contract's 006B1D15/D49/DC6 were branch targets, not bodies) |
| Instruction rows | 236 | 236 (126 region1 lines 626420-626545 + 110 region2 lines 995327-995436, all analyzed) |
| CALL sites | 19 | 19 (6 unique direct targets + indirect/virtual sites enumerated in COUNTERS.json) |
| Candidates | 4 | 4 (all evaluated, none promoted as identity bridge) |

Front A caps: 3/16 bodies, 236/1800 rows, 19/64 CALL, 4/12 candidates. Package time: start 21:14:37Z, artifacts complete ~21:30Z — inside handoff target 21:49:25Z and wall cap 21:58:31Z.

## Package path census

D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018\packages\P01_EXEC_R1\
CONTRACT.json, RUN_STARTED.json, SOURCE_PINS.json, EXTRACT_REGION1_006B1C60_006B1E00.txt, EXTRACT_REGION2_007D27B0_007D291E.txt, ANALYSIS_NOTES.md, CLAIMS.json, MEMORY_AND_IDENTITY.json, COUNTERS.json, BARRIER_BACKLOG.json, REPORT.md, HANDOFF.md, GATES.json, artifact_index.csv, MANIFEST.json (written last, self-excluded).

## Notes for reviewer

- Verify: source SHA re-hash; extract SHAs (71B83F5C…, D783257F…); line-range bijection extracts↔source; store census against the verbatim extracts (the A1 absence claim is census-based); frame arithmetic for [ESP+0x70]=first stack arg (ANALYSIS_NOTES R2); the +0x148 free path rows 995394-995409.
- Countermodel spot-checks for A2/A2b: (a) allocator-alias countermodel for [EDI]=EAX — confirm we labeled it premise-excluded, not disproven; (b) this-relative-only store census of 007D27B0; (c) the "outslot inside [this..this+0x194]" countermodel — premise-excluded only.
- Independent counters: my "3 actual bodies" relies on in-window CFG (JZ targets prove 006B1D15/D49/DC6 are labels); recheck jumps at source lines 626463, 626483, 626510.

## Request to parent

1. Admission decision for region 0x006B1E00-0x006B1F40 (006B1C80 tail) — highest-value A1 continuation, fits Front A caps (would bring Front A to 4/16 bodies, ~326/1800 rows).
2. Optionally: admission for 0082E750 region (retain-before-teardown closure) — better routed as its own package given row cost.

This is a child-scope completion. The parent campaign continues; no milestone/gate/canonical state was touched (CANONICAL_GATE_EFFECT=NONE).
