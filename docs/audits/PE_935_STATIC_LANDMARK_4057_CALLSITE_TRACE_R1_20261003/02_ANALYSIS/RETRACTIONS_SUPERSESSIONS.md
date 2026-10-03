# RETRACTIONS / SUPERSESSIONS — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. STATIC_ONLY. No published canon file is modified;
all supersessions are current-meaning-only, recorded here.

## R-1 — s9 container-level sids census superseded by s10 entry-level parse

```text
SUPERSEDED (current meaning): 01_RAW/SIDS_REPINS.json's series census and the
interpreted fields IMMEDIATE_4057_IS_SIDS_RECORD_ID / IMMEDIATE_886_IS_SIDS_
RECORD_ID = False. That census tested CONTAINER record ids; sids.vfs holds ONE
container record (id=1), so the test was vacuous-by-construction. The string
ids live as PAYLOAD entries. SUPERSEDOR: 01_RAW/SIDS_ENTRY_PARSE.json (measured
layout from g6; exact-closure parse; 3,887 entries) — IMMEDIATE_4057_IS_SIDS_
ENTRY_ID = True, 0xFD9 -> 'S_REPAIR_UI_CLEAR_TOOLTIP'. The s9 walk's file
identity pin (129,040 B, D58EF1D2...) and container census remain valid.
Data nuance (R1 amend, record-only; QC-confirmed — 04_QC/TARGETED_QC_REPORT.md):
the first sids payload entry is an empty string with id 2021; the payload
still closes exactly under the documented layout with 3,887 entries.
```

## R-2 — FALSIFIER_REACH_CHECK.json artifact history corrected (R1 amend; finding F-P2-1)

```text
CORRECTED (R1 amend, finding F-P2-1): the FALSIFIER_REACH_CHECK.json shipped
with the original package was the s7_curate_g4.py version (stage S7; 13
functions = g1..g4 + the containing function; TOTAL_DIRECT_TEMPLATE_MACHINERY_
HITS = 0 over that subset only) — the s8_curate_g5.py g1..g5 regeneration
described by the original R-2 never landed in the package, and the g6 function
was never in the artifact at all. R1 regeneration: 03_SCRIPTS/s12_falsifier_
reach_check_v2.py rebuilt the artifact (schema-compatible) from the curated
g1..g6 raw JSONs over ALL 18 measured functions: total_functions_checked = 18;
TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS = 1 (the shared GENERIC mapfind
FUN_004D1430 called at 0x00823C57 inside FUN_00823C10 on the string-table
manager map @[mgr+4], singleton DAT_00BA12F4) classified NOT a template-registry
edge (different singleton than the registry tree DAT_00BA1824, referenced only
inside getter FUN_0043A550; composite key; string values; FUN_0072F580 not on
the path); TOTAL_TEMPLATE_REGISTRY_EDGES = 0. QC independently measured the
same single hit over all 18 windows (04_QC/TARGETED_QC_REPORT.md Q8). The
interpreted conclusion (0 template-registry edges on the 4057 path) is
unchanged by every version of the artifact.
```

## R-3 — working label correction: FUN_008DF3F0 / FUN_008DF310 are not ctors

```text
CORRECTED (this run's own working labels only): the g2 script labels
"D04_ctor_008df3f0" / "D05_ctor_008df310" were pre-dataflow guesses. The
measured bodies (g2) are guard+act helpers: `if (FUN_008df1e0() != 0) {
FUN_008e1f60()/FUN_008e2ab0(); return; }` — 19 B each, 554/392 call sites. No
construction claim is made from them anywhere in this package; the label in
the script filename is a historical label, the evidence files state the
measured behavior.
```

## R-4 — Jython signed-byte display artifact in the first g1 dump

```text
CORRECTED (instrument): the first g1 execution printed listing bytes via
Jython '%02X' % signed_byte (e.g. '-27' for 0xD9). Detected immediately (the
s2 physical pin showed 68 D9 0F 00 00); g1 was fixed to '(b & 0xFF)' and
re-run; the curated package contains only fixed-format listings. The s2
crosscheck parser defensively accepts both forms. No evidence file in the
package carries the artifact.
```

## R-5 — the deferred lead's candidate statuses (disposition, not a canon retraction)

```text
RESOLVED-NEGATIVE (for this call-site, per the run's falsifier): the deferred
lead recorded in PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003
(DEFERRED_PLACEMENT_LEADS.md) carried candidate statuses TO_BE_REPINNED. This
run re-pinned every pin: PUSH 4057 @0x0059AB12 CONFIRMED (byte-exact);
templates record 4057 {A=218757, B=218758} CONFIRMED (data side); 218757.nif /
218758.bvi index presence CONFIRMED; BUT the connecting claim
(IMMEDIATE_4057_IS_TEMPLATE_ID at this call-site) is REJECTED_FOR_THIS_CALLSITE
— the immediate is a sids.vfs string-table id (S_REPAIR_UI_CLEAR_TOOLTIP).
The templates data-side facts are NOT retracted; only the call-site linkage is
rejected. HUMAN_HISTORICAL_RECOLLECTION (218757 as a landmark probe) remains
untouched evidence-class HUMAN_HISTORICAL_RECOLLECTION (probe-selection only).
```

## R-6 — Prior canon explicitly NOT retracted

```text
UNCHANGED: record-bridge E1-E12, the desktop-correction dispositions
(F-D1..F-D4), CURRENT_CLAIM_STATE.md §7 invariants (MAIN_RECORD_REQUEST_INDEX_
CHAIN=SUPPORTED for record 4508; RESULT_LEVEL=B; RUNTIME_NIF_OPEN=NOT_CLOSED;
PLACEMENT_XYZ_RECOVERED=NO), and every prior package. This run measured a
DIFFERENT call-site (0x0059AB12) than the record-bridge family (4508 chains);
no prior result conflicts with this run's findings.
```
