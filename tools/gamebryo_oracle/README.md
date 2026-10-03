# GAMEBRYO_ORACLE_TOOL

Original-Gamebryo-as-oracle tool for Project Entropia / Entropia Universe
9.3.5 NIF forensics (run PE_GAMEBRYO_ORACLE_TOOL_R1_20261003, order s7-s23).

ERA CATEGORY: OUR_TOOL. The tool code here is 100% OUR code. ZERO proprietary
Gamebryo source, binaries, or NIF payloads live in this directory: the
adapters contain ONLY our code, build instructions, local path discovery,
invocation wrappers, output parsers and hash verification. Original payloads
and original tools are used READ-ONLY from their original locations or the
run sandbox; modified copies never leave the sandbox.

## Usage

```
python oracle.py inspect <nif> [--adapter gb12|gb26|gb112|gb23] [--full-decode] [--out file]
python oracle.py probe-version <nif> [--adapter ...]
python oracle.py compare <nif> --our-parser <our_result.json> [--oracle-result file]
python oracle.py capabilities [--adapter ...]
python tests/test_gb12.py --self            # pure-logic tests
python tests/test_gb12.py --sandbox-payload <file>   # control battery
```

Exit codes: 0 accepted, 2 rejected/failed (JSON still emitted), 3 IO error.
All JSON output is DETERMINISTIC: no wall-clock timestamps, no random data.

## Adapters

| adapter | ORACLE_MODE | era | semantics |
|---|---|---|---|
| gb12 | SOURCE_DERIVED_REIMPLEMENTATION | GB_1_2 | Gamebryo 1.2.2 NiStream load semantics re-implemented from the original source tree (`gb12core.py` header = full citation block with per-file SHA256): "File Format" header test; packed-u32 gate 3.3.0.11..10.2.0.0 with the original error strings; user-defined version iff file >= 10.0.1.8; RTTI string table + factory with the ORIGINAL fail-closed behavior (unregistered class -> RTTIError -> Load() false); per-block GroupID u32 iff 5.0.0.6 <= v < 10.1.0.114 (P2); LoadBinary/link/postlink phases; EOF-exact closure. |
| gb26 | SOURCE_DERIVED_REIMPLEMENTATION | GB_2_6 | version gate ONLY (min 10.1.0.114, NiStream.cpp sha 72781EEB...): the wrong-version negative control. In-range files report NOT_IMPLEMENTED_BEYOND_GATE (no fake GB 2.6 decode). |
| gb112 | ORIGINAL_TOOL_EXECUTION | GB_1_1_2 | runs the INSTALLED original Gamebryo 1.1.2 Evaluation tools (unmodified, sandbox-local VC71 runtime DLLs) on sandbox copies; parses stdout/exit; version-range claims stay UNKNOWN (binary lib). Exact blocker classes are recorded when a tool cannot run. |
| gb23 | SOURCE_DERIVED_REIMPLEMENTATION (header-only) | GB_2_3 | metadata-only: engine identity from the recovered NiVersion.h (sha DFCCD6EC...); read range UNKNOWN (binary); execution NOT_TESTED (installer never installed; nothing is installed by this tool). |
| compare | MIXED | OUR_TOOL | oracle vs our FIELD_IDENTITY_V2 decoder, the order-s11 19-item list, statuses {MATCH, MISMATCH, NOT_AVAILABLE_IN_ORACLE, NOT_AVAILABLE_IN_OUR_DECODER, SEMANTICALLY_UNRESOLVED}. |

### gb12 RTTI table validation (F1 fix, 2026-10-03)

`gb12core.py` validates the ENTIRE RTTI table in SOURCE TABLE ORDER
(NiStream.cpp LoadRTTI L421-433: name -> factory lookup -> next name),
including entries no object references. The FIRST unregistered table entry
is the fail-closed verdict (RTTIError -> Load() false) BEFORE any later
table name, any object type index (L436-444), the object groups or any body
byte. The JSON separates `rtti_table_validation` (the table-order factory
scan: `first_rtti_miss`, `first_miss_table_index`, `names_read`,
`full_table_read`, `unregistered_table_entries`,
`source_predicted_verdict`) from the OBJECT-side artifacts
`object_reference_histogram` + `object_reference_census` (one u16 type
index per header block; LoadRTTI L436-444). In ordinary fail-closed mode a
factory miss reports NOTHING past the miss (no indices, no histogram, no
census, no bodies). The legacy `< 5.0.0.1` inline-RTTI layout is NOT
migrated to this fix. The pre-F1 build validated by iterating object type
indices instead (Desktop post-audit finding F1): unused unregistered
entries were silently skipped and the first miss was reported in object
order.

### gb12 --full-decode (OUR extension; NEVER original behavior)

The ORIGINAL GB 1.2 verdict is always: first unregistered RTTI table entry
-> LoadRTTI RTTIError -> Load() returns false. With `--full-decode` the
adapter CONTINUES the stream decode past the miss (recording unknown blocks
with closure-derived boundaries) so known-class field data can be compared.
In that mode the JSON carries `load_result.accepted=false` +
`error=RTTIError(<first table miss>)` + `partial=true` +
`decode_continued_after_rtti_gate=true` and KEEPS
`rtti_table_validation.source_predicted_verdict=REJECTED` with
`first_rtti_miss` = the first miss in TABLE order; every continuation past
the miss is explicitly labeled (`extension_observation`). If the extension
itself hits a parser failure (truncated later table name, corrupt or
incomplete object indices), it halts with an `EXTENDED_*` warning and the
source-predicted verdict is never masked. The ORIGINAL verdict is reported
in `load_result` and never silently merged. SOURCE_DERIVED output is never
phrased as original execution (G-TOOL-4).

## Local dependency representation (s22)

| item | LOCAL_PATH_DESCRIPTION | VERSION | SIZE | SHA256 | REPRODUCTION_METHOD |
|---|---|---|---|---|---|
| GB 1.2.2 source tree (read-only semantics source) | `D:\gamebyroengine\extracted\Gb12_Source` | Gamebryo 1.2.2 (CoreLibs NiVersion.h 1.2.2.6, build 2006-06-19) | ~tree | per-cited-file SHA256s in `gb12core.py` header | read-only; the adapter re-implements the cited loader semantics |
| GB 2.6.0 flat source (gate source) | `D:\gamebyroengine\extracted\Gb26_src` | Gamebryo 2.6.0 (2008-10-20) | ~tree | NiStream.cpp 72781EEB... | read-only; gate constants re-implemented |
| GB 1.1.2 installed tools | `D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\Tools\...` | Gamebryo 1.1.2 Evaluation (NDL 2004) | per-exe | per-exe in `adapters/gb112/adapter.py` | ORIGINAL UNMODIFIED exes copied to the sandbox run dir + sandbox-local VC71 DLLs (`extracted\Gb112_tools_setup\MSVCR71.DLL/MSVCP71.DLL/MFC71.DLL`); stdout/stderr/exit captured |
| GB 2.6 viewer deployment reference | interrupted-run sandbox `...\PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003\sandbox\viewer` + `C:\Users\User\AppData\Local\Temp\opencode\gb_tools_inventory\*.cab` | GB 2.6 (2008) | per-file | recorded per attempt in 04_EVIDENCE | read-only reference; fresh copies extracted into THIS run's sandbox only |
| nifxml historical schema (our decoder) | `D:\Eudoria_Reconstruction\04_External_References\reference_only\nifxml_historical\nif.xml` | 0.7.1.1 | - | pinned by the ROSETTA run (s04 loader) | read-only input of the FIELD_IDENTITY_V2 decoder lineage |

## Factory registry provenance (adapters/gb12/registry.py)

`GB12_REGISTERED_CLASSES` is generated from the ORIGINAL GB 1.2.2 source tree:
every `NiRegisterStream(...)` / `NiStream::RegisterLoader("name", ...)` call
in the per-lib `*SDM.cpp` static data managers across `CoreLibs` (198 unique
class names; per-SDM sha256 in the file header). Zero `NiArk*` classes occur
anywhere in the registry, so the fail-closed RTTI verdict for MindArk NiArk*
blocks is invariant to which CoreLibs subset a prebuilt tool links.

## Tests

`tests/test_gb12.py` exercises: version packing; registry invariants; the
wrong-version controls (synthetic 99.0.0.0 -> LATER_VERSION, 1.0.0.0 ->
OLDER_VERSION); NOT_NIF_FILE; determinism; the F1 RTTI table-order battery
(registered-only baseline preserved; unused unregistered entry rejected;
first miss by TABLE order, not object order; factory miss before
incomplete object indices; factory miss before a truncated later table
name; --full-decode keeps SOURCE_PREDICTED_VERDICT=REJECTED with the
table-order FIRST_RTTI_MISS and labels the extension, whose own parser
failures never mask the source verdict); and (with `--sandbox-payload`)
the fail-closed battery on a sandbox copy of a real payload: RTTIError
reporting, unknown-class reporting (mutated RTTI name), corruption
fail-not-silent, object-count mismatch detection, partial-load
never-PASS, link-failure detection. Every control prints
MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR /
FAILURE_CASE_DETECTED (s18).

## Schemas

`schemas/oracle_result.schema.json` and `schemas/comparison_result.schema.json`
implement the order s8 minimum (`input_identity{size,sha256,header,
nif_version}`, `oracle{gamebryo_version,loader_identity,
loader_source_identity,tool_version}`, `load_result{accepted,partial,
error}`, `objects[]`, `scene_graph`, `type_histogram`, `controllers`,
`properties`, `textures`, `bounds`, `warnings`, `unknowns`) plus extensions
(`version_gate`, `rtti_gate` (deprecated compact alias), `rtti_table_validation`,
`object_reference_histogram`, `object_reference_census`, `tool_reports`,
`object_count_check`).
