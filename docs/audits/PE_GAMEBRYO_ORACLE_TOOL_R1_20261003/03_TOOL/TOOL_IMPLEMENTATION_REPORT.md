# TOOL_IMPLEMENTATION_REPORT — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (E2)

GAMEBRYO_ORACLE_TOOL_BUILT = YES (G-TOOL-1 PASS):
tools/gamebryo_oracle/ with ONE entrypoint oracle.py supporting inspect /
probe-version / compare / capabilities; schemas/oracle_result.schema.json +
comparison_result.schema.json (order s8 minimum + extensions: version_gate,
rtti_gate, tool_reports, object_count_check); adapters gb12/ (with registry.py
factory census), gb26/, gb112/, gb23/, compare/ -- ONLY our code, ZERO
proprietary source in the repo; README.md with usage + s22 local dependency
representation; tests/test_gb12.py (self + control battery).

- G-TOOL-2 DETERMINISM: PASS (byte-identical double runs for T1/T2/T4/T5;
  no wall-clock anywhere in the JSON bodies; sha256s in TEST_MATRIX.csv).
- G-TOOL-3 FAIL_CLOSED: PASS (all controls DETECTED, none silent).
- G-TOOL-4 ORACLE_LABELING: PASS (every JSON: ORACLE_MODE, era_category,
  oracle.gamebryo_version, loader_identity, loader_source_identity with
  file+sha256, tool_version; SOURCE_DERIVED output never phrased as original
  execution; full-decode extension flagged decode_continued_after_rtti_gate).
- T3 full-decode: honest PARTIAL (480s wall cap; ~298 not-implemented
  registered classes make the closure search combinatorial); the original
  verdict + header-level data for T3 are complete.
- Adapter semantics are pinned to the E1 source canon (gb12core.py header =
  full per-file citation block; NiStream.cpp sha E955C36E, NiObject.cpp
  B137FE42, per-class LoadBinary bodies extracted this run into the sandbox
  evidence pack phaseD_gb12_loadbinary_extracts*.txt).
- Executed original tools: gb112 SceneGraphPrinter BLOCKED_EVALUATION_
  TIMELOCK_EXPIRED (verbatim dialog text captured); gb12 SceneGraphPrinter
  exits 1 without observable output; gb12 SceneViewer_DX8 alive without
  observable load result; gb26 PhysXNifViewer runs but never reaches the NIF
  load in this environment (Settings -> missing EGB_SHADER_LIBRARY_PATH ->
  'Failed to load shader library!'). All attempts: ORIGINAL UNMODIFIED exes,
  sandbox-local runtimes, zero patching (s19); screenshots LOCAL_ONLY (s20).

- C1 note (2026-10-03, correction round): the five mutation-control
  outputs are now persisted as raw JSON in 04_EVIDENCE/controls/,
  re-executed on sandbox copies via 04_EVIDENCE/scripts/
  c1_control_persist.py + c1_followup.py + c1_complete.py (same control
  code paths as tests/test_gb12.py; per-payload verdicts + labels
  inside each JSON; all five controls have a DETECTED case; honest
  per-payload non-detections are recorded and explained inside
  each JSON). In E2 they were executed in-memory with only the batch
  stdout captured -- disclosed; no detector verdict changed by C1.

- C2 note (2026-10-03, correction round): capabilities all-adapters mode fixed
  -- oracle.py _get_adapter now loads each adapter under a unique module name
  (gb_oracle_adapter_<name>) via importlib.util; the Python module cache
  previously made every adapter after the first resolve to the FIRST adapter
  module (all four adapters reported gb12's capabilities; the compare default
  path was equally broken). compare() now initializes result["summary"] = {}
  immediately after items = result["items"] (prevents the latent KeyError in
  the both-failed early branch; exercised paths unchanged). gb112 adapter:
  import struct moved into the top import block (was at the very bottom).
  Doc corrections: NIF_LOAD_PIPELINE.md per-block LoadBinary sentence for
  4.1.0.12 (lower bound NOT met; GroupID NOT read; T4 decode EOF-exact),
  gb12core.py FACTORY REGISTRY comment (census list embedded in
  adapters/gb12/registry.py), HANDOFF.md GB_1_2 leading token now REJECTED,
  STAGE_ACCEPTANCE_GATES.csv "14 columns" wording. Regression: oracle inspect
  218757.nif --adapter gb12 --full-decode output sha256
  E86AAAB65CFF26FC11E07E81DF403C6E0C26922FC72BD001C3BC0FB0ABDF77B9 --
  unchanged; no decode behavior change.
