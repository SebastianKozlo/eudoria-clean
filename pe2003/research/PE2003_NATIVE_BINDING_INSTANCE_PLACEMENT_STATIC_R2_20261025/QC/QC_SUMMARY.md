# QC_SUMMARY — INTERNAL_QC of RUN PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025

QC_RUN_ID: QC_PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025_F1
QC worker: fresh pe-master-auditor (procedurally independent; no job of this run executed by this session).
Started/finished (tool-measured): 2026-10-25T11:08:34Z .. 2026-10-25T11:20:00Z (python datetime UTC; Get-Date not used — this is a Windows-PowerShell host session; all timestamps below are tool-measured python/clock values recorded in QC outputs).
Read-only except this QC dir (created exclusive-OK). No nested Task. No runtime. No frozen artifact touched.

## VERDICT: QC_PARTIAL

Rationale: all independently re-derived claims TRUE (37 verification items, QC_VERIFIED_CLAIMS.csv); corrections handled honestly (immutability + hash pins + downstream supersession + ledger records all verified); no forbidden overclaim wording found; WORLD_XYZ_RECOVERED=NO and FAMILY-LEVEL join limits maintained everywhere. QC_PARTIAL, not QC_PASS, because of P1-1 (budget ledger cannot support cap compliance — SP-A09: SEMANTIC_BUDGET_COMPLIANCE=UNVERIFIED), P2-1 (B01 admission-trail loss), P2-2 (P01 LOC cap deviation unresolved), and explicit NOT_CHECKED load-bearing components (below) which forbid QC_PASS under control 15 / L11 coverage algebra.

## Per-area verdicts

1. STRUCTURE — PASS (all 11 SCIENCE_ROOT JSONs strict-parse, 0 duplicate keys; all 16 CSVs full-field-count parse; report-vs-data row counts confirmed: J02 30, J04 69(69 TRUE), B02a 10+8=18 bijection, P01_NIF_BLOCK_MAP 155+62=217, J03 100/3403; B01 owner CSV = 6 data rows/7 total — P3-4 count-convention nit).
2. CORRECTIONS — PASS with P2-3 disclosure requirement: (i) J01a 0xF0->0xF000 correction independently CONFIRMED from my own PE header parse (.data SR=0xF000); correction block present in J01a_WRITER_CENSUS.json; j01a_emit.py re-hash matches seq=9 ADMIN_APPENDIX pin and line 206 carries 0xF000. (ii) J01b premise supersessions (X=0x28B, X+0x14 no static writer, node+0x2C quat) are documented ONLY in downstream artifacts (P01 premise_correction/node_2c correction; J04 x14_writer_correction_to_J01b) — acceptable, but the final report must carry a supersession map (P2-3). (iii) B02a f1/f2 transposition adjudicated from raw DYN bytes: J02's correction is CORRECT; B02a original left unmodified with the defect visible (hash pin OK). (iv) J02 seq=14 incident: all 11 B02a/data files re-hashed against HANDOFF pins — ZERO drift confirmed.
3. OVERCLAIMS — PASS: no NETWORK_ONLY, no branches_exhausted, no unbounded impossibility/cannot-exist, no placement/world-position recovery claim; P01 maintains LOCAL_PART_TRANSFORM vs WORLD explicitly; instance-level join kept STILL_AMBIGUOUS in J03/J04 and AMBIGUOUS in P02 (family-level only, pinned by two byte-identical vt installs I re-verified). "impossible" appears only as coverage-scoped statements inside the frozen, superseded J01b original.
4. LEDGERS/BUDGET — PARTIAL: ADMISSION_EVENTS seq 1..23 contiguous, no gaps/dups, every job except B01 has its own admissions; ROLE_LEDGER records root modelID=glm-5-3 (not high) per SP-A06 requirement — but BUDGET_LEDGER covers only 4 early units and cannot support the 96/A6/B30/J24/P18/Q18 accounting (P1-1). P01 LOC 878>800 disclosed as KNOWN DEVIATION (P2-2 — process deviation, must not be silently treated as compliant).

## Independent re-derivation vs read-only

Independently re-derived with own tools (not job tools): EXE SHA pin; PE section table (incl. .data SR 0xF000); 16 byte-claims at VA via my own VA->offset mapping; the P01 push-0x28 creation sites (6a 28 @0x521b78/@0x5b7256, both calls target FUN_005b5110 — RESOLVES root's open finding, premise byte-supported); Scripts.ark SHA + 3 member AK local-header parses (CRC+SHA, STORED); 4508/4057 DYN records and model-id STOREI bytes (adjudicating the B02a transposition); NIF file pins; all strict-JSON/CSV/hash-pin/row-count checks; 5 sampled J04 byte-verify rows re-derived from raw EXE.

Read-only (trust but verify at hash level): WORK evidence files, ledgers, contracts, job HANDOFFs, the governing POSTAUDIT REPORT.md (SP-A01..09 dispositions checked against this run: SP-A01/02/05 wording violations absent; SP-A07 CSV hygiene PASS this run; SP-A08 chronology not re-audited; SP-A09 violated by ledger omission — P1-1).

## FULL_READ_LOG

Fully read to EOF: all 11 SCIENCE_ROOT JSONs; B01_OWNER_CLASSIFICATION.csv, J01a_TABLE_MAP.csv, J01b_EXECUTOR_SEMANTICS.md, P01_NIF_BLOCK_MAP.csv (row counts; per-row contents spot-checked); ledgers (3); B01 HANDOFF; POSTAUDIT REPORT.md (108 lines); J01a emit line 206 region.
Partially read (head/sample): B02a_DECODE_ANNOTATED.txt (existence/format check only); J04/J02/B02a data CSVs (full machine-parse of every row, semantic content sampled).
Not read: WORK/jobs/*/tools/out/ decompile dumps (60+ per job); jobs/B02 dead-attempt dirs; P01_RAW_CENSUS.json (752KB); Ghidra scan logs.

## NOT_CHECKED (explicit)

- Ghidra decompilation/disassembly correctness for all jobs (raw bytes verified independently at claim sites; decompile texts trusted only as job-internal cross-checks).
- J03 3403 register-site census and 100 unique pairs: row COUNT verified only, sites not independently re-derived from binary.
- J02 1936-file corpus literal scan and EXE literal scan: not re-run (the 4 model-id instructions + DYN records in 4508/4057 re-derived; 1796/2202 EXTN hash matches accepted from B02a re-derivation claims).
- B01 Ghidra xref census (88 fns) and image-wide LE-ref scans: not re-executed; the load-bearing ark/EXE bytes were independently verified instead.
- opencode.db modelID census (SP-A06): NOT independently re-verified (read-only DB not opened by this QC); ROLE_LEDGER claim accepted as declared with its own recorded evidence pointer.
- NIF block-map content semantics (155/62 block parses): row counts only; not re-parsed from the NIF files.
- Runtime anything (contract is 100% static).
- HOSTCALL_BINDING.json / PLACEMENT_MESSAGE_SCHEMA.json / VM tables / R1 fixup map pins: not re-hashed by this QC (admission gates recorded by the jobs).

## FINDINGS (ordered by severity)

P1-1 Budget ledger incomplete (see QC_FINDINGS.json P1-1) — required correction before seal: additive ledger completion or explicit UNVERIFIED carry.
P2-1 B01 admission-trail loss (disclosed; require final-report disclosure).
P2-2 P01 tool-LOC 878>800 hard-cap deviation (disclosed; require root acceptance decision).
P2-3 J01b superseded claims lack in-file supersession marker; supersession lives in P01/J04 artifacts — final report MUST include the supersession map.
P3-1 P01 LEA VA off-by-one (0x5b3ca9 actual; bytes exact).
P3-2 P01 push-0x28 VAs (cited VAs are ctor CALL sites; pushes at 0x521b78/0x5b7256) — root finding resolved, premise CONFIRMED.
P3-3 J02 file_off = operand dword location, instruction starts -4.
P3-4 owner_rows count convention (6 data rows vs "7").
P3-5 seq=14 "12 files" vs 11 actual (all hashes match).
P3-6 ADMISSION_EVENTS.jsonl is a JSON object, not JSONL.

## CORRECTIONS THE ROOT MUST ORDER BEFORE SEAL/PUBLICATION

1. Append a BUDGET_LEDGER completion block enumerating all dispatches incl. dead attempts with family attribution and explicit spend-vs-cap statement (or an explicit SEMANTIC_BUDGET_COMPLIANCE=UNVERIFIED declaration in the final report). (P1-1)
2. Final report must state: B01 admission-trail loss (P2-1); the J01b->P01/J04 supersession map (P2-3); the P01 LOC deviation acceptance decision (P2-2); the precision errata (P3-1/2/3) including exact push VAs 0x521b78/0x5b7256 and LEA VA 0x5b3ca9; the count-convention notes (P3-4/5/6).
No scientific artifact needs content correction: every defect found is administrative/precision-level; all load-bearing science claims sampled re-derived TRUE.

Artifacts: QC_FINDINGS.json, QC_VERIFIED_CLAIMS.csv (37 items), QC_STRUCTURE_CHECK.json, qc_bytecheck.py, qc_structure.py, qc_bytecheck_raw.json — all in this QC dir.
