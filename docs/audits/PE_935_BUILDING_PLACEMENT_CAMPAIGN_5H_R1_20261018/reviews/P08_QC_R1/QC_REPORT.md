# QC REPORT — P08 (Front D1, saved-evidence document-assimilation) independent internal review
# RUN_ID: PE_935_PLACEMENT_P08_QC_R1_20261018 | parent campaign: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018

- REVIEWER: pe-master-auditor, fresh child session dispatched directly by PE-MASTER (NO_NESTED_TASKS; no delegation; no Task tool invoked; no EXE/payload/runtime/config/repo actions)
- TARGET PACK: `packages\P08_EXEC_R1` — immutable, not modified by this review; this review wrote only to `reviews\P08_QC_R1`
- PACKAGE CLASS: Front D document assimilation; admitted_regions = []; NO body admission (contract-mandated)
- WORKER VERDICT UNDER REVIEW: **SCOPED_NEGATIVE_WITH_BOUNDS** — no historical world-instance placement values in the assimilated saved-evidence corpus
- QC VERDICT: **QC_PASS** — process verdict: **PASS** (1×P3 cosmetic correction registered; zero rejected claims; zero counter-evidence found)

## 0. Adjudication summary

The worker's scoped negative is **upheld in full**. Every load-bearing claim was re-anchored to catalog-pinned primary documents (fresh SHA256 5/5 == catalog pins, independently recomputed); every quoted standing value was located verbatim at the cited lines; the classification table was re-verified against the full CSV census and the source runs' own texts; the four negative bounds and the precise remaining edge are present and correctly sourced. Counters 0 bodies / 0 rows / 0 CALL are real — no admission event for P08 exists, and the pack contains no binary/listing artifacts. The premises were applied, not merely recited.

## 1. Mechanical integrity (all independently executed by this reviewer)

| Check | Result |
|---|---|
| MANIFEST re-hash (11 entries) | 11/11 SHA256 match, 11/11 size match |
| Manifest bijection | HOLDS (disk = 11 entries + MANIFEST.json self-excluded; zero unmanifested files) |
| Package CONTRACT.json identity | SHA256 `12092315…ABF4A` == `CONTROL\CONTRACTS\P08.json` (byte-identical copy) == RUN_STARTED/MANIFEST pins |
| Source pins (5 documents) | Fresh disk SHA256 == SAVED_TEXT_CATALOG pin == worker-recorded value, **5/5** (catalog scope CLOSED_SAVED_TEXT_ONLY; file_count 967 recounted) |
| Census over-reading check | PASS — catalog files of the same runs NOT read (bridge FINAL_REPORT.md/HANDOFF.md; errata 03_REPORT/HANDOFF.md); only the 5 contract-named documents |
| No body read | PASS — EVENTS 000001–000010 enumerate ADMITs for P01,P01,P02,P03,P04,P05,P06,P07,P09; **no P08 admission**; zero binary artifacts in pack; forbidden counters all zero |
| Event chain integrity | previous_event_sha256 links verified CHAIN_OK across all 10 events (no retro-insertion) |
| Chronology | contract now_utc 23:02:13Z → RUN_STARTED 23:02:25Z → MANIFEST 23:05:54Z (LAST) — strictly ordered; hard stop 2026-10-19T00:00:00Z respected |
| Attribution honesty | SELF_CHECK block explicitly labeled "executor's own — NOT independent PE-MASTER audit"; HANDOFF QC_ORIGIN = SELF_CHECK only; no self-QC promoted to independent audit |

## 2. Checked-sources census adjudication (the "3 named sources (+2 more)" question)

The contract's main_question enumerates **five documents across three runs**: (1) bridge `06_REPORT/DRAFT_FINAL_REPORT.md`; (2) scene-inspection `HANDOFF.md` **+ `FINAL_REPORT.md` sections** on WORLD_XYZ/PE_WORLD_ROOT_IDENTITY; (3) errata `TRANSFORM_TABLE_CORRECTED.csv` **+ `00_RAPORT_CORRECTED.md`**. The worker's census contains **exactly these five** (S1, S2a, S2b, S3a, S3b) — no more, no less.

Adjudication of the "+2 more": under the strict three-file reading (one primary file per named run), the two additional census entries are **S2b `FINAL_REPORT.md`** and **S3b `00_RAPORT_CORRECTED.md`** — both are **explicitly contract-named** ("+ FINAL_REPORT.md sections…", "+ 00_RAPORT_CORRECTED.md"), so these are not worker-invented additions; under the three-run reading, the census is a 1:1 expansion of the three runs into their five named files. Either way: **all census entries are contract-covered, catalog-pinned (verified 5/5 by fresh hash), and correctly classified** with per-source role and read-mode. The read-mode split (4 full + 1 relevant-sections) follows the contract's own wording ("FINAL_REPORT.md sections…"), and the disclosed section ranges were verified against the document's actual section anchors (§4.6 at L295–333, §4.7 at L335–354, §5 at L356–369, final block within L420–456).

## 3. Accepted claims (with evidence_level adjudicated)

| Claim | Subject (condensed) | Pack level | Reviewer adjudication |
|---|---|---|---|
| P08-CL1 | Standing negatives of the three runs (PLACEMENT_XYZ_RECOVERED=NO; WORLD_XYZ_RECOVERED=NO + PE_WORLD_ROOT_IDENTITY=NOT_ESTABLISHED + MODEL_GEOMETRY_MATCHES=0; NOT_FOUND_IN_SEARCHED_SCOPE) | CONFIRMED | **ACCEPTED — CONFIRMED** (each quote located verbatim: S1 L108–110; S2a L52–54; S2b L359–363; S3b L21/L22; statuses re-quoted, not re-derived, and the claim says exactly that) |
| P08-CL2 | Every transform-like value in the assimilated documents falls into 9 classes; none passes the 4-part D1 test (instance identity + model identity + byte provenance + frame) | CONFIRMED | **ACCEPTED — CONFIRMED (for the assimilated document set)** — all 9 classes re-anchored to primary text/CSV; full independent CSV census (30 rows; 14 changed; 16 zero-rows; local_S all 1.0; examples byte-exact) found **no counter-example**; the strongest candidates (296445 world_T column; 218757 (0,−1030,820); PARAM 124.941) each fail at identity or frame exactly as stated |
| P08-CL3 | TRANSFORM_TABLE_CORRECTED.csv provenance: own-parser byte data (155/155 block map) mechanically recomputed by errata analyze_tree_v2.py under world[i]=parent_world∘local_i; G1 gate with 16/30 unchanged rows as negative control; 14/30 changed exactly | CONFIRMED | **ACCEPTED — CONFIRMED** (S3b L13/L160/L302–304 verbatim; CSV changed_vs_r1 recount = exactly the 14 mesh_idx listed; not an SDK parse; stock GB 1.2 native load of these assets corpus-proven impossible) |
| P08-CL4 | The three runs are separate instruments sharing underlying sources — corroboration, not three independent confirmations; independent lines are the errata G2 reproductions, bridge CONTROL-4, scene-inspection 5/5 cross-check | CONFIRMED | **ACCEPTED — CONFIRMED** (shared identities verified: Models.bnt C950A8C2… pinned in S1 L15, S2b L71 (re-verified before/after), S3b L33; 296445 payload 656795d8… byte-identical across eras S3b L44–46) |
| P08-CL5 | Bounded remaining edge: values server-delivered per PE2/2003 canon (era-scoped to PE2_unpacked_out.exe), session records absent (FIRST_PEINST 0/6, no cache, servers unreachable), 9.3.5 mechanism UNVERIFIED, corpus searches clean; unsearched classes = Strings/*.bnt (blob-448, decoder-as-lead), .prt, media | STRONGLY_SUPPORTED | **ACCEPTED — STRONGLY_SUPPORTED** (every bound quote verified: S3b L21/L24/L260/L276, S1 L102–105; the honest level fits a claim about where values could still exist; falsifiers listed and none known) |
| P08-CL6 | Standing statuses preserved unchanged; no candidate promotion | CONFIRMED | **ACCEPTED — CONFIRMED** (no counter-value found anywhere in the assimilated set; no promotion language in the pack) |

**Scoped negative bounds (explicit, verified present):** (1) searched-and-clean scope enumerated with denominators (u32LE full corpus + u32BE full Data with 0 BE hits; decompressed terrain; 1,936 decoded scripts — 296445/296446 only in 4508.obj.dec as VM immediates = definition linkage; VFS both eras at field level; 23×29×5 encoding census PASS-NEGATIVE; no spawn table in 2,712-position scripts); (2) unsearched value-carrier classes named with reasons (Strings/*.bnt encrypted blob-448 location-class — decoder exists as a lead, not used; .prt undecoded; media pattern-only; none a known placement carrier for 296445); (3) values-provenance bound (server-delivered; session records absent; 9.3.5 mechanism UNVERIFIED [E-A1]); (4) frame bound (PE_WORLD_ROOT_IDENTITY=NOT_ESTABLISHED; PE_AXES_AND_UNITS=UNVERIFIED — a value candidate could not be interpreted without a frame). The negative is scoped to the **assimilated corpus**, not claimed as a corpus-wide or world-wide absence — correctly bounded.

## 4. Premises application (all four verified as APPLIED, not recited)

1. *Three documents copying one source ≠ three independent confirmations* → P08-CL4 with documented shared identities.
2. *SDK-controlled parse values are saved evidence only in their scope* → applied to I-SYNTHETIC-CONTROL, plus the stronger verified fact that the 296445/218757 tables are not even SDK parses (own-parser bytes + stated arithmetic convention; native load corpus-proven impossible).
3. *Movable rec+38/rot+44 channel is not static-building evidence* → applied inside R-MECHANISM-NO-VALUES; not counted as static-building placement evidence.
4. *Transform values without instance identity + frame/origin/scale are not historical placement* → the operative test applied to every class; each class's failure point (identity or frame) is stated.

## 5. Corrections (registered; none invalidates a claim)

- **QC-P08-1 (P3, cosmetic) — REPORT.md §1 census table, S2b row formatting.** The Size column cell contains "—" while the size (51,369 B) is given inside the adjacent Source cell. Zero effect on any claim, hash, or counter (size and SHA both correct). Fix for the ledger/synthesis: none required; if the table is ever reproduced, place 51,369 in the Size column.

No P0/P1/P2 findings. No data defect, no coverage gap, no premise violation, no admission violation, no chronology violation, no attribution violation.

## 6. Rejected overclaims

**None.** All six claims survive independent re-anchoring at their stated levels. No status was promoted (WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN, CANONICAL_GATE_EFFECT=NONE all preserved); the PE2/2003 mechanism is kept era-scoped (its binary only) with 9.3.5 explicitly UNVERIFIED — exactly matching the source runs' own qualifiers.

## 7. Precise remaining edge (adjudicated, confirmed well-formed)

Within the closed corpus, D1 is closed as a scoped negative: historical placement VALUES for the studied objects are not recoverable because the 2003-canon delivery channel is server-session-based (byte-evidenced in PE2_unpacked_out.exe only), session records do not exist in the corpus (FIRST_PEINST 0/6; no cache; servers unreachable), and the frame for interpreting any candidate is itself not established. Recovery would require (a) an external archived session record (none known), (b) an independent external source (out of corpus), or (c) runtime capture (forbidden in this campaign). The 9.3.5 consumer MECHANISM (PE_935_TEMPLATE_CONSUMER_TRACE_R1 design, [E-V2R007], S3b §9) remains the designed P0 experiment — it would close Front B/C mechanism knowledge but cannot produce historical values. Unsearched value-carrier classes (Strings/*.bnt, .prt, media interiors) remain explicit data barriers (P08-B2), not known carriers.

## 8. Coverage and NOT_CHECKED (L11 discipline)

- FULL_READ: all 12 P08 package files (11 + MANIFEST), to EOF.
- FULL_READ (primary): TRANSFORM_TABLE_CORRECTED.csv (30 data rows re-censused in full); SAVED_TEXT_CATALOG.json structural fields (scope, file_count, per-source pins).
- BOUNDED_INSPECTION: S1/S2a/S3b (claim-anchored line-range reads + full-document pattern sweeps covering every load-bearing topic); S2b inside the worker's disclosed section ranges plus section-anchor checks.
- NOT_CHECKED (this review): full-text re-read of S2b outside the disclosed section ranges (51,369 B document; the contract itself mandates sections-only); campaign-wide corpus search for placement values (out of P08 scope — P08 is document assimilation; the corpus-wide searches are the assimilated runs' own measured results, quoted with provenance); the physical EXE/VFS/BNT payloads (forbidden; not needed — no claim in P08 rests on this reviewer touching payloads).
- Denominator algebra: census = 5 documents read = 5 contract-named = 5 catalog-pinned (0 missing, 0 extra, 0 unverified). Package = 12 files = 11 manifest + 1 self-excluded manifest. Classification = 9 classes over the assimilated set (exhaustive for those documents; the claim is scoped accordingly).

## 9. Process verdict

**PASS.** Contract SHA verified; RUN_STARTED first; 5/5 source pins independently reproduced; zero body admission verified at the event, artifact and counter level; forbidden lists untouched; premises applied; scoped negative carries its bounds and a precise remaining edge; standing statuses unchanged; real clock, hard stop respected; honest attribution. The single registered item is cosmetic (QC-P08-1, P3).
