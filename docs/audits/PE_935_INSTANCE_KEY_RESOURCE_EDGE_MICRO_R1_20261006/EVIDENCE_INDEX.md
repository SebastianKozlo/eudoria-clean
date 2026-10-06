# EVIDENCE_INDEX — PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006

All evidence lives under `docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/`.
Every claim in FINAL_REPORT/QC_REPORT cites at least one artifact below. No original
game payload is included; no EXE copy is committed (the Ghidra sandbox lives outside
the repo at `C:\Users\User\AppData\Local\Temp\opencode\PE935K_GHIDRA\`, deleted-or-
retained per temp policy; its identity metadata is recorded here).

## 01_RAW/ (measurements — all generated from the pinned EXE)

| Artifact | Content | Produced by |
|---|---|---|
| GovernanceWriteTime.txt | GOVERNANCE_DECISION.md write-time independent re-measurement (2026-10-05 23:54:05.874, size, SHA256) | PowerShell re-measure (KROK 0) |
| GETTER_PIN.txt / GETTER_PIN.json | FUN_00414130 byte pin: VA→offset 0x14130, bytes `8B 41 74 C3`, boundary window, PE header spot checks, full section map | 03_SCRIPTS/pin_getter.py |
| E8_CENSUS.json | the 6 E8 hits (each with VA/rel32/bytes), whole-file scan (0 outside .text), E9 census (0), absolute-dword census (0), published-xref recompute (2/2 MATCH), method + exclusions statement | 03_SCRIPTS/e8_census.py |
| BYTE_WINDOWS.txt | raw hex dumps, 10 windows, all script-generated from the pinned EXE: FUN_00401360, FUN_005247C0, FUN_00509330 (body), FUN_00856190, ctor prologue, base-ctor key-store window, FUN_00459fd0 callsite window, plus the three windows cited by EDGE_LEDGER (E-E2-EXTRADATA/E-E2-REG/E-XD/E-GB2) and FUNCTION_LEDGER (rows 4/7/8): SF_ctor_tail 0x00509470..0x005094BF, F0064B1E0_head 0x0064B1E0..0x0064B20F, F004157B0_head 0x004157B0..0x004157DF. The three cited windows were ABSENT from the artifact at run time (internal QC finding F2) and are NOW PERSISTED by the record-repair (byte_windows.py WINDOWS extended; BYTE_WINDOWS.txt regenerated append-only, first 7 windows byte-identical; content verified against the ledger claims and the QC's own M6 dumps). The earlier description advertised an unpersisted "boundary probe" output — that concept is superseded: its content is now the SF_ctor_tail and F0064B1E0_head windows | 03_SCRIPTS/byte_windows.py |
| RTTI_PROBES.json | calibration (3/3 BASE-canon vtables reproduced, fail-closed) + probes: 0x00A79F18=`.?AVGameClient@@`, 0x00A83274=`.?AVSceneFeederObjectExtraData@@`, 0x00A7D444=NOT-A-CLASS-VTABLE | 03_SCRIPTS/rtti_probes.py |
| GHIDRA_VERIFY.json | independent-tool verification: getter function identity, 6/6 candidates PROVEN_EXACT (instruction starts, CALL flow targets, containing functions), exactly-6 references to 0x00414130 (all UNCONDITIONAL_CALL) | Ghidra 11.2.1 headless + 03_SCRIPTS/ghidra_post.py |
| GHIDRA_DISASM_WINDOWS.txt | Ghidra disassembly listings: getter window, the 4 new-candidate windows, ctor window, insert window | Ghidra postscript |
| GHIDRA_DECOMPILES.txt | Ghidra decompilations of the 5 budgeted functions (getter, ctor, FUN_005247C0, FUN_00509330, FUN_00856190) — cross-check layer for the own byte decodes | Ghidra postscript |
| QC_CONTROLS.json | the three controls (a)/(b)/(c) with clean/mutated runs, EXE identity at QC time, census recount (6), getter boundary re-read | 03_SCRIPTS/qc_controls.py |

## 03_SCRIPTS/ (actual measurement/QC scripts — all run-local)

| Script | Role |
|---|---|
| pe935k_core.py | run-local PE walk (headers, sections, VA↔offset, byte reads); fail-closed size/PE asserts |
| pin_getter.py | getter pin + boundary dump |
| e8_census.py | E8/E9/dword census with method/range/exclusions |
| byte_windows.py | raw byte window dumps (own evidence); WINDOWS list extended by the record-repair (internal QC finding F2) with SF_ctor_tail / F0064B1E0_head / F004157B0_head (byte read from the pinned EXE, EXE identity re-verified before the read) |
| rtti_probes.py | MSVC RTTI chains; calibration-first, fail-closed |
| ghidra_post.py | Ghidra headless postscript (candidates verification, references, decompiles, disasm windows); SHA256 after final edit `38FBCFBE2ADB79F0E11C66B9254B8BBE5E116BF170D7FC4AD2CBD401348E4800` (hashed 2026-10-05 23:57:33, BEFORE launch) |
| qc_controls.py | targeted QC controls (a)/(b)/(c) + identity/recount/boundary re-reads |

## Package documents

GOVERNANCE_DECISION.md (KROK 0, verbatim human instruction + DA1 present-adjudication),
INPUT_IDENTITIES.md, FINAL_REPORT.md, QC_REPORT.md, HANDOFF.md (with the proposed
AUDIT_ENTRYPOINT.md row), FUNCTION_LEDGER.csv, EDGE_LEDGER.csv,
CALLSITE_SHORTLIST.csv, EVIDENCE_INDEX.md (this file),
COMMITTED_PACKAGE_MANIFEST_SHA256.csv (generated LAST; scope = every physical file
under this package minus the manifest itself; per the human dispatch the
AUDIT_ENTRYPOINT.md row is NOT part of this phase's manifest and the file was NOT
edited — the persistence phase will regenerate the manifest with it).

## NOT_CHECKED (explicit)

Ghidra sandbox project internals (outside the repo); any VFS/BNT/NIF/ARK payload;
all runtime behavior; FUN_0064B1E0 consumers; FUN_007C8780; FUN_007B6A80;
FUN_004A9850; FUN_00853D00; FUN_009789C0; the 4 new containing-function bodies;
indirect/inlined +0x74 readers anywhere; Desktop post-audit (NOT_PERFORMED).
