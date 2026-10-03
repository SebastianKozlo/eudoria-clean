# NEGATIVE CONTROLS — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. STATIC_ONLY. Contract §20 requires at least the
five controls below; each is executed and evidence-cited.

## CONTROL-1 — numeric coincidence ("does 4057 really reach the template consumer?")

```text
EXECUTED: reach-check over all 18 measured functions against the fixed canon
template-machinery VA set (01_RAW/FALSIFIER_REACH_CHECK.json; TEMPLATE_ROLE_TEST.md §4).
RESULT: FAIL — 4057 does NOT reach FUN_0072F580 or any proven template-id consumer.
Structural supplement: the anchored immediate is one of six consecutive values
(0xFD4..0xFD9) consumed identically; only 0xFD6 and 0xFD9 numerically overlap
templates.vfs id2 (4054, 4057) while ALL SIX are sids.vfs string ids
(S_REPAIR_UI_*_TOOLTIP) — the overlap is coincidence between two id spaces
(01_RAW/SIDS_ENTRY_PARSE.json, SIDS_REPINS.json templates_series_census).
LEAD DISPOSITION: rejected for this call-site; per contract §31 no alternative
rescue was attempted.
```

## CONTROL-2 — unrelated-immediate control (same-class numbers treated as plain constants)

```text
EXECUTED: full immediate census of the containing function FUN_00599D30
(01_RAW/CALLSITE_DATAFLOW_WINDOWS.json immediate_census_function_wide):
62 unique PUSH immediate values (NOT an imm32-only census: the decoded
PUSH-immediate set includes imm8/0x6A-form pushes such as the small integers
0..0x16 and 0x3C; QC's independent imm32-only/0x68-form byte census found 49
unique imm32 values — 04_QC/TARGETED_QC_REPORT.md F-P3-4b) — small integers
(0..0x16), UI ids (0xFF, 0x1DF,
0x376=886, 0xFA7..0xFD9), sizes/counts (0x3C, 0x1050, 0x186A0, 0x26B2, 0x26B3),
string/VA immediates (0x886B6, 0x8559D, 0x597680, 0x5976C0, 0x597A10,
0x9D2626), and a 12-entry consecutive table-pointer series (0xB7DD48..0xB7DDB8)
plus 0xBA342C. The same code treats the ENTIRE class identically (PUSH ->
thiscall argument); nothing about 4057's mechanics is special. The sibling
series (0xFAB, 0xFAE..0xFB2, 0x376) and every series member were resolved to
sids.vfs string ids, demonstrating the value class is UI string ids, not
template ids. No special semantics were granted to 4057 because it matches
templates.vfs.
```

## CONTROL-3 — identity continuity (same runtime object through to transform)

```text
EXECUTED AS VACUOUS-NEGATIVE: the falsifier fired before any
template/resource/transform path existed; there is NO transform path to test
continuity on. The identity chain that WAS measured (4057 -> composite key ->
string -> ArkUI::Component store) is continuity-verified per step
(CALLSITE_DATAFLOW.md §3, every step VA+bytes+src/dst). No world-instance
bridge is claimed, so no cross-object identity shortcut exists.
```

## CONTROL-4 — spatial semantics (three-float falsification)

```text
EXECUTED AS VACUOUS-NEGATIVE: NO three-float operation exists anywhere on the
measured 18-function path (integer ids, pointers, strings only —
TRANSFORM_PROVENANCE.md §3). No "position" was named and no alternative
(color/scale/direction) needed testing; nothing was promoted from data shape.
```

## CONTROL-5 — scene insertion (generic machinery is not proof)

```text
EXECUTED: the terminal store FUN_008DFB70 constructs an ArkUI::Component temp
(vtable 0x00A7A948 @0x008DFBD0) — a UI component container. No NiNode ctor,
no SetName, no UpdateWorldData-shaped propagation, no AttachChild shape, no
scene root edge appears in any measured function; INSTANCE_TO_SCENE_EDGE is
NOT_ESTABLISHED and NOT CLAIMED (TRANSFORM_PROVENANCE.md §4; the record-bridge
E7 negative-control family applies by shape, and none of those shapes occur).
```

## Supplementary honesty controls (self-applied)

```text
- Ghidra-vs-physical byte identity: 951/951 instructions of the containing
  function byte-identical to the EXE via the OWN PE mapper (no Ghidra involved
  on the verification side) — 01_RAW/RAW_BYTE_PINS.json g1_byte_crosscheck.
- Mapper calibrations: two independent canon anchors reproduced before any
  callsite byte was trusted (RAW_BYTE_PINS.json).
- VFS walker calibrations: templates walk must reproduce 5,438 records /
  0 CRC-fail / exact EOF / record 4508 @96,496 A=296445 before the 4057 record
  was trusted (TEMPLATE_4057_PHYSICAL_RECORD.json); BNT2 parsers must reproduce
  index_start 395,262,727 / count 5,596 / anchor 296445.nif @395,268,773 and the
  Volumes.bnt calibration name before the 218757/218758 lookups were trusted.
- sids.vfs layout: derived from the client's own parser (g6) and validated by
  exact payload closure + count match (3,887/3,887) — two independent sides
  (SIDS_ENTRY_PARSE.json).
- Jython signed-byte display artifact ("-27" = 0xD9) detected, documented, and
  eliminated in the curated listings; the crosscheck parser handles both forms
  (RETRACTIONS_SUPERSESSIONS.md).
```
