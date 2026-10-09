# EVIDENCE_INDEX — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

Index of every evidence file of this package with its role. Executor + QC evidence is
FROZEN (11 physical files: executor 8 + QC 3; unmodified by this persistence phase —
their SIZE/SHA256 below were re-measured at persistence start and match the freeze).
The four persistence-phase documents (PE_MASTER_REVIEW.md, FINAL_REPORT.md,
EVIDENCE_INDEX.md, HANDOFF.md) and MANIFEST_SHA256.csv were written by the
pe-master-auditor persistence phase; their final SIZE/SHA256 are recorded in
MANIFEST_SHA256.csv (generated LAST; self-exclusion documented there — a manifest
cannot contain its own SHA256).

## 1. Frozen executor evidence (8 files)

| File | Size (B) | SHA256 | Role |
|---|---:|---|---|
| `PREREGISTRATION.md` | 16899 | `4E80397805468725B3712CF46A4DB1A2005EF6F1D40859415E1A5350D6BC35ED` | Pre-registration written BEFORE any disassembly/extraction: the question, window pins, budget, symbolic-stack plan, expected decode, the six expected control results, falsifiers F1–F6, path scope / ABI assumptions, standing §8 carried verbatim; executor phase boundary (§11) |
| `INPUT_IDENTITIES.md` | 10228 | `D321648CD86582F8E7E8E0711BCD8ABF1EAEC4C941EBB5BF63DD5B998A3D30F2` | Measured input identities: frozen contract (18964 B / 9BAF558E… MATCH), git triple + clean tree + OUTPUT_ROOT absent, EXE identity, the four contract §2 repo inputs (bytes+SHA+blob equality), governance read, tool identities, temp directory plan, preflight verdict PASS; also the honest stray-temp-path disclosure |
| `01_EVIDENCE/WINDOW_IDENTITY.json` | 2314 | `3CEBCD04CB0D5921585635EF720CF0E8C15CC70F027491FED6F6703FABEB7ECF` | The physical re-pin, machine-readable: EXE identity before/after, PE mapping (ImageBase 0x400000; RVA 0x128E76; .text; computed file offset 1216118 == pin), window bytes/SHA == contract pin, DOC-1 note (W3 first two bytes not read/decoded), callsite rel32 recompute → 0x0085B1B0, tool identity |
| `01_EVIDENCE/CALLSITE_DISASSEMBLY.txt` | 1696 | `5A588C865472E108C54FED00981669E92E1BEDEE98115429F1C2BCBFD80915D8` | Verbatim raw GNU objdump 2.44 output of the single baseline invocation (command + fixture identity + unmodified stdout): 10 instructions ending exactly at the CALL — the decode evidence for the ledger |
| `STACK_LEDGER.csv` | 1904 | `016859E4FE5BEA988FD2252708D1F760086834255CAE69E9F6EC8AC99F8005D0` | The instruction-by-instruction ledger: VA/bytes/objdump text/ESP delta/ESP after/kind/dst/src/source-slot address per row + the summary block (ESP_BEFORE_CALL S-0xC; ESP_AT_CALLEE_ENTRY S-0x10; ARG1_ENTRY_SLOT S-0xC; ARG1 chain; reaching definition; receiver; recomputed target); machine-parsed by the QC — exact match |
| `ARG1_PROVENANCE.json` | 10071 | `29FF09675BEC2A4604524CBD202E6542AA850FD54A6ABBAEFF0395BF6813F85E` | The machine-readable result: callsite, the arg1 determination (push VA/register/value expression/producer VA/source operand/source slot/entry slot/reaching definition/upstream boundary/path scope), receiver separation, arg2/arg3 with declared_semantics NONE, callee entry conventions (prior pinned evidence, body not re-opened), aliasing checks, ABI assumptions, budget, standing §8, not_performed, controls summary, science outcome |
| `CONTROLS_RESULTS.json` | 147192 | `A8C470DFB73A5559BB4D2E7C1F27BA7A7D0C38D7F58200FEB9014D4AA469BDE7` | The six fixtures + outcomes + raw objdump outputs + repairs disclosure: per-case objdump invocations (rc/stderr/command), fixture identities (size/SHA/byte deltas/diff offsets), measured facts per case, expected-vs-measured checks per case (BASELINE_QUALIFIED + 5× CONTROL_PASS), `objdump_raw_output_by_case` (all six), control methodology, EXE identity after, temp cleanup record; `executor_implementation_notes` = the honest R1+R2 repairs disclosure |
| `03_SCRIPTS/run_stack_controls.py` | 63771 | `7091C33E2A12D48593235DCEEA8CDA0CB7853669EAB0A54CEE354058CC485A99` | The executor replay runner (pure stdlib, `python -B`): reads the window from the EXE, builds fixtures in the OS temp dir (outside Git), invokes objdump per fixture, parses the raw output, performs the symbolic replay and the fail-closed contiguity/unsupported guards, writes STACK_LEDGER.csv / ARG1_PROVENANCE.json / CONTROLS_RESULTS.json |

## 2. Frozen fresh-QC evidence (3 files)

| File | Size (B) | SHA256 | Role |
|---|---:|---|---|
| `03_SCRIPTS/qc_stack_replay.py` | 41419 | `B7624687511B0B2BA2F56850EF86704C061AB69D8C3B0A3F21A350367091DD75` | The QC independent replay (own implementation; no executor-code import; own parser with per-instruction byte-column cross-validation; own fixtures; own expectations from contract §4/§5/§6; fail-closed; produces the QC's ledger/case signatures and its NC1/NC2 negative controls) |
| `QC_RESULTS.json` | 46947 | `BB674940F3C56F9AD5B8B8D2A207A5839B0321CC20049E4445F618563F80388A` | The fresh QC, machine-readable: origin + QC_PASS + verdict scope; input identities re-verified (contract/EXE/git/4 repo inputs/entrypoint blob); tool provenance + 8 invocations; independence dimensions (same-disassembler honestly stated as NOT cross-implementation QC); duties 1–7 with MEASURED_QUANTITY/SOURCE_OF_TRUTH/WHY_NON_CIRCULAR/FAILURE_CASE_DETECTED per meaningful PASS; six QC case outcomes + agreement with executor; fixture SHA convergence; NC1/NC2; findings F-QC-1/F-QC-2; coverage + NOT_CHECKED + count algebra |
| `QC_REPORT.md` | 16243 | `C290023F7515DD013B3FEA8C0712CA89ED4DD4287CDC39B3CE243A78907501F5` | The fresh QC, human-readable: method, per-duty results (window re-pin, ledger agreement, 6/6 outcomes, PASS records, executor-claims verification incl. preregistration-before-science CONSISTENT-documentary + repairs R1+R2 ADJUDICATED HONEST, symbolic-provenance discipline, scope compliance), QC negative controls, findings, coverage, verdict |

## 3. Persistence-phase documents (this phase; identities in MANIFEST_SHA256.csv)

| File | Role |
|---|---|
| `PE_MASTER_REVIEW.md` | PE-MASTER's master audit persisted VERBATIM (internal advisory MASTER_AUDIT; MASTER_ACCEPTED advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE; own window re-pin + manual ledger verification ALL MATCH) |
| `FINAL_REPORT.md` | This run's final report: identities, preflight, window, tool provenance, ledger, arg1 determination (field-by-field with ARG1_PROVENANCE.json), six controls with 12-outcome accounting, QC results + honest independence statement, disclosed process items, scope, standing §8 verbatim, terminal governance |
| `EVIDENCE_INDEX.md` | This file |
| `HANDOFF.md` | Contract §10 terminal fields with the ACTUAL measured values + value provenance + persistence facts |
| `MANIFEST_SHA256.csv` | Generated LAST: every physical file under OUTPUT_ROOT except itself PLUS the updated AUDIT_ENTRYPOINT.md (repo-relative; size_bytes; sha256; measured census + bijection self-check; self-exclusion documented) |

## 4. Required repository inputs (contract §2; cited with SIZE/SHA; read-only, blob-verified at BASE)

| Path | Bytes | SHA256 | Role in this run |
|---|---:|---|---|
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/CONTROL_RESULTS.json` | 18509 | `9545D0D78881C29BC805EA3A05C8AA936D364256671D31A1AE907677A63DE2F8` | Prior pinned evidence: the W3 record (0x00528E74, len 52, raw offset 1216116 — this window is the sub-range beginning two bytes in) and the callee entry conventions (W1 decode: entry `mov eax,[esp+0x8]` = arg2; `mov edi,[esp+0x14]` @0x0085B1DA after four pushes = [entry+4] = arg1) |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/FINAL_REPORT.md` | 15589 | `FF5FDBD2F54F20E3026B5992F7BCC411B0572ADA249F157BA11CB441E1AC83E0` | Prior committed context of the source run (provenance narrative standing) |
| `docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/SUPERSESSION_AND_STANDING.md` | 6848 | `0AB2CDECE09CB2FF1419C48E9A1169832A0A061C618A7F94F290089C75F49921` | Standing/supersession state: DOC-1..DOC-4 backlog, J3 standing carried verbatim, the phase-boundary (delegation) precedent |
| `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md` | 8339 | `DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845` | The J3 supersession set (S-1..S-5) and the `ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL` standing preserved by this run |

Other cited inputs: the frozen contract itself (18964 B /
`9BAF558EA21751B59FA00C41EF532CA20D829AA6082804387DD4BDB71BBF4939`);
`AUDIT_ENTRYPOINT.md` at BASE (271684 B /
`53528A82695C710FCF68ACD60BAF9B9442CD649B89F4C82E35F81ED86660E5BB`, == HEAD blob —
governance read; this persistence phase adds ONE newest-first LATEST RUNS row for this
run and modifies no other row); the target binary `Entropia.exe` (8015872 B /
`E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — read-only within
the authorized window; never committed; no proprietary payload in this package).

## 5. Package census

Physical package files after this persistence phase: **16** = 11 frozen executor/QC
files (executor 8 + QC 3) + PE_MASTER_REVIEW.md + FINAL_REPORT.md + EVIDENCE_INDEX.md +
HANDOFF.md + MANIFEST_SHA256.csv. Manifest rows: 15 package rows (16 minus the
self-excluded manifest) + 1 entrypoint row = **16 rows**. Bijection verified at
generation (missing=0, extra=0, duplicate=0, size=0, SHA=0).
