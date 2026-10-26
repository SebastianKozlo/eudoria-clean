# LIVE_FRONTIER_QUEUE — R8 FINAL (refreshed at closure; supersedes wave-1 table)

| edgeID | question | pin/range | predecessor | result | gap closed (addendum) | next action | budget status |
|--------|----------|-----------|-------------|--------|----------------------|-------------|---------------|
| F-A07 | A07 decodes analysis (ingest head 0x505C00 + PFIX/SPTR 0x506190) | decodes ON DISK (jobs/A07/attempt_1) | A06 | unanalyzed future input (INC-R8-008) | presence->execution completion | one bounded analysis child | ready |
| F-A08 | CODE-ingest body 0x508290 | 0x508290-0x5083C0 (~80 rows) | A06 | pending | CODE->interpreter wiring | DECODE ADMIT | ready |
| F-A09 | interpreter head 0x50A340 | 0x50A340-0x50A3ED (~60 rows) | A06 | pending | VM loop tie to ingest class | DECODE ADMIT | ready |
| F-A10 | decrypt-site hunt upstream of 0x505C00 | xref + decode | A07-analysis | pending | stream provenance (resource-open vs other) | after F-A07 | ready |
| F-M11 | copier true entry + src getter | M11 sweep hits on disk + fresh 0x4020C0 decode | M09/M10/M11 | OPEN (INC-R8-006/007) | model-resource->E->X join | narrow child redo | ready |
| F-M12 | slot 0x2c tail 0x5CC7D6 + 0x4FFBD0 + 0x506760 + 0x5A2830 | small decodes | M10 | R=root NEGATIVE-leaning (slot 0x2c partial) | R identity | low priority | ready |
| F-Q2X | Q2 open list (M09 sweep copier callers; R identity) | see Q2 QC_RESULT | Q2 | open | input->model-node | low priority | ready |
| F-EXT1 | 5.1.0.0 own Scripts.ark/Models.ark (PE_PCG.ark / FullDat) | external | A05 | BLOCKED: CONTRACT §2 separate human scope | in-build definitions availability | human decision | blocked |
| F-EXT2 | instance placement values | external | A04 | BLOCKED: network-fed per canon | historical XYZ | out of static scope | blocked |
| F-EXT3 | IAT import resolution | external | A06 | BLOCKED: packed exe flat dump IAT 0x0 | decrypt/import chain | needs unpacked import table scope | blocked |

Wave verdicts (root-adjudicated, all children): M01 ACCEPTED; T01 ACCEPTED; M02 ACCEPTED (thunk); T02-a1 partial->T02-a2 ACCEPTED; Q1 QC_PASS; M03-a1 artifacts->M03-a2 ACCEPTED (E=FETCH); T03 ACCEPTED; T04 ACCEPTED (P=E+F8 storage-level, Q2-confirmed 14 sites); M04 ACCEPTED (E polymorphic); T05-a1/a2 FAILED (INC-R8-004)->T05B ACCEPTED (receiver/arg2 UNBOUND-in-window); M05 ACCEPTED; M06 ACCEPTED (0x66 family != E); M07 ACCEPTED (5813C0 refuted; 5CAEF0 factory); A01 ACCEPTED (anchors era-labelled; ISO negative); M08 ACCEPTED (0x18 != E; root-R candidate); A02 ACCEPTED (records 4508/4057 verified; grammar; superset); Q2 QC_PASS; A03 ACCEPTED (templates.vfs NEGATIVE-BOUNDED); M09 ACCEPTED (triple-copy confirmed; R!=root leaning); A04 ACCEPTED (definition->resource VERIFIED; Jan-2003 era); M10 ACCEPTED (head deeper; slot 0x2c string mechanics; 0x5077c0 keyed query); A05 ACCEPTED (machinery EVIDENCED); M11 partial (INC-R8-006); A06 ACCEPTED (PARTIAL presence->execution); M11B FAILED (INC-R8-007); A07 decodes-only (INC-R8-008); Q3 QC_PASS CLOSURE_ELIGIBLE.
