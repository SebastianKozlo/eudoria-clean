# AMEND_LOG.md — PE_CITY_ASSET_MAP_R1_20261010 — persistence-phase amendments

RUN_ID = PE_CITY_ASSET_MAP_R1_20261010
PHASE = PERSISTENCE_PUBLISH (contract §8)
PERFORMED_BY = pe-master-auditor persistence session (2026-10-10)
SCOPE = the four REQUIRED FIXES from the fresh internal QC REVIEW.md findings (QC verdict
PASS_WITH_FINDINGS: 0 P0 / 0 P1 / 1 P2 / 3 P3; PE-MASTER-confirmed before persistence).

This is the FIRST amend log of this run: the fresh internal QC performed NO repairs (its one
authorized targeted repair round was unused), so no earlier amend log exists. Historical phase
artifacts are preserved; no raw evidence was modified to agree with a report; the two report-package
amendments below are machine-readability corrections mandated by the QC findings, with revalidation
gates executed after each fix.

## Fix 1 — P2-1: TEXTURE_LINK_DISPOSITIONS.csv RFC4180 quoting (report package)

- TARGET: `docs/audits/PE_CITY_ASSET_MAP_R1_20261010/TEXTURE_LINK_DISPOSITIONS.csv`
- DEFECT (QC REVIEW.md §2 P2-1): the 1,545 PCG_9_3_5 aggregated rows carried the literal
  `Textures.bnt (8,381 entries)` unquoted in `container_entry`; the thousands-separator comma tore
  every such row into 8 fields against the 7-field schema (QC2 histogram {7:42, 8:1545}).
- ACTION: quote exactly the `container_entry` occurrences containing the comma:
  `,Textures.bnt (8,381 entries),` → `,"Textures.bnt (8,381 entries)",` — 1,545 replacements
  (pattern occurrences in the file: exactly 1,545; no other `Textures.bnt` reference existed).
  NO disposition value, model_id, era, edge, slot or texture_name altered. CRLF line endings,
  trailing newline and header preserved; file stays UTF-8 without BOM.
- PRE: 584,206 B / SHA256 0465C736FADB2C44653C9EFB23DF90886902DD73247A840547D0E0CB3CB929B4
- POST: 587,296 B / SHA256 268F5531BE447A78C8B607830B55BCDE6A9A26892D1C7578E39DE5365982A6DA
  (delta +3,090 B = 1,545 × 2 quote bytes — no other change class).
- REVALIDATION (independent strict RFC4180 parser, fresh code path, not qc2): header exact match;
  1,587 data rows; field-count histogram {7: 1587} — ALL rows exactly 7 fields; bare-LF/CR rejected
  (none found); CD_2003 rows 42; PCG_9_3_5 rows 1,545; distinct PCG models with ≥1 edge 1,545
  (edge-less 6 = batch 1,551 − 1,545, confirmed from PCG935_NAME_BATCH_SUMMARY.json: modelsProcessed
  1,551 / edges 4,151); NAME_NOT_FOUND sum 3,357; MATERIAL_REFERENCE_CONFIRMED sum 794; edges total
  4,151; CD-side edges 19 material + 19 texture-chain + 4 state. RESULT = PASS.
- SUM CHECK vs QC REVIEW revalidation gate: 3,357 / 794 / 4,151 / 1,545 / 19+19+4 — UNCHANGED, PASS.

## Fix 2 — P3-1: INTERVENTION_LEDGER.md F12 data-row count correction (append-only)

- TARGET: `docs/audits/PE_CITY_ASSET_MAP_R1_20261010/INTERVENTION_LEDGER.md`
- DEFECT (QC REVIEW.md §2 P3-1): the historical F12 row records "1,588 data rows" for
  TEXTURE_LINK_DISPOSITIONS.csv; the actual count is 1,587 (42 + 1,545; header excluded); the row
  also calls the file ASCII-only while it is UTF-8 (19 em-dashes in the phase-4 material rows).
- ACTION: APPEND-ONLY correction section "PERSISTENCE-PHASE CORRECTIONS AND INTERVENTIONS" with
  correction row C1 (the exact correction text required by the QC finding) plus informational rows
  C2–C4 recording the other persistence amendments of this log. The historical F12 row is preserved
  byte-identically (verified: POST file's first 21,836 bytes == PRE file).
- PRE: 21,836 B / SHA256 89C59FE849FA5128D272C0F35F1B4EDCE77CDC61AA146EEE77E958D7255C9ABE
- POST: 24,243 B / SHA256 0F7A1A988A5135849634BA081F981A734FBA6C6C6C701EB24AF088CDAFE804BFB3
- REVALIDATION: historical prefix byte-identity check PASS; correction row present at EOF; recounted
  data rows 1,587 (see Fix 1 revalidation). RESULT = PASS.

## Fix 3 — P3-2: skill chapter overlap example replaced (allowlist skill file)

- TARGET: `.opencode/skills/pe-gamebryo-rosetta/references/catalog-era-identity.md`
- DEFECT (QC REVIEW.md §2 P3-2): §1 used "656865.nif" as an example of a name present in BOTH era
  model containers; that name exists in NEITHER (QC14/QC15; no near-miss 6568* names).
- ACTION: replace the example with the verified overlap example `266865.nif` (kept `65678.nif`),
  adding the verification clause. One passage edited; no other content changed.
- PRE: 9,509 B / SHA256 DCC15FD7E8185233FB67FBA9F447AA4F587EB8F1E6728EAAEBD9F598F5EE359B
- POST: 9,563 B / SHA256 478AD41B6A945797081662BB603F5E675969D6C5DE9F06070333C9606CCF6D28
- REVALIDATION (independent, performed BEFORE the edit, against both phase-2 model catalogs from
  PRIVATE_OUTPUT/PHASE2_CATALOGS): `656865.nif` NOT_FOUND in CD2003_MODELS_ARK_ENTRIES.csv (2,492
  entries) and NOT_FOUND in PCG935_MODELS_BNT_ENTRIES.csv (5,596 entries); `266865.nif` FOUND ×1 in
  each; `65678.nif` FOUND ×1 in each. After the edit: `656865` occurrences in the file = 0;
  `266865.nif` and `65678.nif` present in the fixed passage. RESULT = PASS.

## Fix 4 — P3-3: PRIVATE_OUTPUT run_records.json UTF-8 BOM stripped (private artifact)

- TARGET: `D:\Eudoria_Reconstruction\99_Audits\PE_CITY_ASSET_MAP_R1_20261010\PHASE3_NativeControl\run_records.json`
  (PRIVATE_OUTPUT — never inside the repo; private path+SHA reference only).
- DEFECT (QC REVIEW.md §2 P3-3): file started with EF BB BF; strict JSON.parse failed (the only
  BOM-bearing JSON of 21 private JSON artifacts censused by QC5).
- ACTION (choice made: strip the BOM, preserving content): removed the leading 3 bytes; every
  remaining byte identical by construction (byte-range copy of bytes 3..end). No record content
  altered. This is a private-side mechanical encoding fix, not a repo change and not raw-evidence
  tampering: the four native-control records' content (argv/cwd/env-delta/exe SHA/exit/stdout/stderr)
  is byte-identical after the strip.
- PRE: 3,500 B / SHA256 2FD4A81FB68250262D678BD9A875D4C500C327880E7F163099D81D1B166C6C51 (BOM EF BB BF)
- POST: 3,497 B / SHA256 A65AEDD8F01FAC9AE84936919A696D29E6AA3667DBC169DF038345AA73EEEC15 (starts `[\r\n`)
- REVALIDATION: strict `JSON.parse(readFileSync(...,'utf8'))` on the fixed artifact SUCCEEDS;
  4 records; first record outcome `EXITED` (native-control semantics intact). RESULT = PASS.
- DISCLOSURE: the same limitation note (BOM class observed on private PowerShell-written artifacts)
  is recorded in LIMITATIONS.md so the QC observation stays visible even though this file is fixed.

## Post-fix state

- All four QC-mandated fixes applied and revalidated: PASS.
- No other file was modified by this phase before the report-package writes below
  (REPORT.md / CLAIM_MATRIX.csv / LIMITATIONS.md / PE_MASTER_REVIEW.md / HANDOFF.md /
  EVIDENCE_INDEX.md / MANIFEST_SHA256.csv — all NEW files; the only pre-existing files touched by
  the persistence phase are the two amended above).
- AMEND_LOG itself is report-package evidence and is covered by the final MANIFEST_SHA256.csv
  (manifest LAST, self-excluded).
