# EVIDENCE_INDEX — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

Index of every evidence file of the package with its role, plus the measured identity of the
cited external sources. Sizes and SHA256 values of in-package files are recorded in
`MANIFEST_SHA256.csv` (generated LAST, self-excluded); this index records ROLE and LINEAGE.

## 1. Physical re-pins (raw evidence of the measured bytes) — `01_RAW/`

| File | Role |
|---|---|
| `01_RAW/SELECTED_WRITE_BYTES.txt` | The physical re-pin of the selected store: raw bytes at the store window, the instruction decode (VA 0x0085B281, `89 4E 44`, mov dword [esi+0x44], ecx; 3 B; 32-bit), physical file offset 4567681 (0x45B281), the FUN_0085B1B0 boundary proof (C3 + 3×CC @0x0085B1AC-AF), the copy triple @0x0085B281/87/8D and the zero-init fst triple @0x0085B1E4/E7/EC. |
| `01_RAW/RECEIVER_LINEAGE.txt` | The receiver/base provenance chain: ESI = FUN_0085B1B0 ctor this = the MovableObject-under-construction (base vtable 0x00A91E4C = `.?AVMovableObject@@` stamped @0x0085B1C1, C7 06 4C 1E A9 00) which FUN_00528E50 stamps 0x00A7DCB0 = `.?AVClientMovableObject@@` on the same memory after return (C7 06 B0 DC A7 00 @0x00528EA2); the temporal nuance (NOT a finished CMO at store time) stated at the claim site. |
| `01_RAW/VALUE_PRODUCER_LINEAGE.txt` | The immediate value chain: mov edi,[esp+0x14] @0x0085B1DA → mov ecx,edi @0x0085B24B → call rel32 @0x0085B27A → FUN_00746560 (lea eax,[ecx+8]; ret — 8D 41 08 C3) → mov ecx,[eax] @0x0085B27F (8B 08) → the store @0x0085B281; clobber-scan evidence; VALUE_PRODUCER_VA = 0x0085B27F; COPY_FROM_MEMORY. |

## 2. Claims — machine-readable ledgers

| File | Role |
|---|---|
| `WRITE_PROVENANCE_LEDGER.csv` | The 12 load-bearing claim hops (H01–H12: 6 receiver pins + 4 value pins + the selected store + the accessor body) with VA/bytes/independent-evidence columns. |
| `CLAIM_MATRIX.csv` | The full claim matrix per contract §11 (claim_id, claim_text, build, original_source_sha, VA, physical_offset, original_bytes, function/receiver/value/semantic statuses, independent evidence, falsifier, limitation, active standing, supersession reference). |
| `FUNCTION_AND_EDGE_BUDGET.csv` | The budget ledger (store 1/1; body 1/1 re-pin; edges 0/0; callee bodies 0/0; xref 0; promotions 0; windows read). **ERRATA note (F-QC-1, applied in FINAL_REPORT.md §6 — this frozen executor file is NOT edited in place): the declared "TOTAL EXE BYTES READ = 381 B" is off by one; the correct total is 382 B (RTTI 0x00A7DCB0 chain = 4+20+26 = 50 B, not 49). Non-material to any predicate or limit.** |

## 3. Census, preregistration and identity

| File | Role |
|---|---|
| `ANCHOR_SELECTION.md` | The committed-evidence-only anchor census INCLUDING the negative search boundary: 6 qualifying stores in FUN_0085B1B0 + 10 reclassified/excluded records (each exclusion pin byte-verified by QC, incl. the FUN_00509510 rep-movsd → SF+0x4C reclassification — NOT a CMO store); the pre-registered selection rule (copy family over zero-init bulk idiom) and the disclosed-and-rejected lowest-VA alternative (fst @0x0085B1E4, CONSTANT). Documented errata notes (frozen file NOT edited): F-QC-2 — census row C-L "fstp" should read "fst" (D9 55 44, reg=2 → FST); F-QC-3 — census row C-K's region claim @0x00855260 is QC-byte-verified beyond the cited committed file's end (0x008551DF); see FINAL_REPORT.md §10. |
| `PREREGISTRATION.md` | The question, exact budget, candidate priority rule and falsifiers fixed BEFORE new science (contract §11). |
| `INPUT_IDENTITIES.md` | The measured identity of every required input (contract, EXE, the 7 pinned source-pair files, the further historical-context files, governance inputs) with PASS/FAIL status; PROJECT_STATE.json recorded absent (N/A). |

## 4. Controls and scripts

| File | Role |
|---|---|
| `CONTROL_RESULTS.json` | The measured results of the M1–M6 synthetic mutation controls (all CONTROL_PASS) and the M7/M8 token gates (PASS), with measured quantities, independent sources of truth, non-circularity notes, expected failure modes and observed results. |
| `03_SCRIPTS/repin_write_provenance.py` | The executor re-pin script (python -B; read-only bounded PE access through the Source-B range-safe reader; no residue). |
| `03_SCRIPTS/token_gates.py` | The executor M7/M8 token-gate script (scanned 10/12 package file suffixes — see F-QC-4). |
| `03_SCRIPTS/qc_remeasure.py` | The fresh-QC re-measurement script (own PE parser, own x86-32 decoder, own RTTI walk, own mutants; EXE read-only, mutations in-memory only; python -B). |

## 5. Fresh internal QC

| File | Role |
|---|---|
| `QC_RESULTS.json` | Machine-readable per-duty measured values and verdicts of the fresh-context internal QC (9/9 duties PASS; all pins re-measured independently; W1 232 B byte-identical; findings F-QC-1..4). |
| `QC_REPORT.md` | The QC report: origin (pe-master-auditor fresh-context internal QC — internal to PE-MASTER; NOT an independent Desktop post-audit, NOT MASTER_ACCEPTED, NOT milestone closure), method and independence, all nine duties, the findings F-QC-1 (P2, required errata), F-QC-2 (P2, optional), F-QC-3 (P3, optional), F-QC-4 (P3, observation), coverage and NOT_CHECKED. |

## 6. Persistence-phase files (this phase; PE-MASTER-supplied verdict + finalization)

| File | Role |
|---|---|
| `PE_MASTER_REVIEW.md` | The PE-MASTER MASTER_AUDIT verdict persisted VERBATIM as supplied (MASTER_ACCEPTED, advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE; preflight, claim matrix, gate predicates, findings, coverage, terminal standing). |
| `FINAL_REPORT.md` | The final report: run/contract identity, preflight, census + selection, the A-outcome table, the value chain, the budget WITH the F-QC-1 ERRATA section (declared 381 → correct 382, non-material), controls summary, the active J3 standing carried verbatim, PLUS4 standing unchanged, QC origin + verdict + findings (errata applied there), the PE-MASTER advisory review, the three coverage classes, open items, terminal governance. |
| `EVIDENCE_INDEX.md` | This index. |
| `HANDOFF.md` | The contract §15 terminal handoff fields with actual measured values. |
| `MANIFEST_SHA256.csv` | The manifest generated LAST over every physical package file EXCEPT itself PLUS `AUDIT_ENTRYPOINT.md`; repo-relative paths; self-exclusion documented. |

## 7. Cited external sources (measured identity at use; all verified MATCH by executor, QC and PE-MASTER)

| Source | Path (repo-relative) | Size / SHA256 |
|---|---|---|
| Source A anchor preregistration | `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/PRE_REGISTERED_ANCHORS.md` | 10650 / `ABC21A0D9C36C564F2328648AF1997D93810813B44D337C55A027B1B24F3A695` |
| Source A continuation decode | `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/01_RAW/FUN_00528E50_CONTINUATION.txt` | 5471 / `BAB06CEB76C33AB47B69A9A27E7D18F1AAA81481EB8F5AA1D9DD3EE5AF16DBD1` |
| Source A SF methods decode | `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/01_RAW/FUN_509x_SF_METHODS.txt` | 6078 / `3A011632A3D96050FDB1DA81D3231C28BECDE3E8517F3820E57E495C8B9FEC85` |
| Source A final report | `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/FINAL_REPORT.md` | 13663 / `E62B7581564A2A6B6946EDFDA29D5077D333C485647A9E2F5969E5732AD8C75B` |
| Source B bounded PE reader | `docs/audits/PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008/03_SCRIPTS/checker_plus4_successor_v2.py` | 38568 / `80EBEE27883AA61173737590FB822B3503B4658CDA511B4B690F8E75B6B64E62` |
| J3 ACTIVE supersession | `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md` | 8339 / `DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845` |
| J3 corrected status algebra | `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/CORRECTED_STATUS_ALGEBRA.md` | 8987 / `00D09B0F72F1F6859C9DAF8A73C592659F251B596588DA304D9BC6912A40FA9F` |

### 7.1 Further required historical context (read-only; measured identity re-verified at persistence — matches INPUT_IDENTITIES.md)

| Path (repo-relative) | Size / SHA256 (measured) |
|---|---|
| `docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/FINAL_REPORT.md` | 14656 / `39DA4D869400D43F3675280EA38B6314618EAD10F3FD1DB1E839DE5989BEEA7A` |
| `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/CLAIM_MATRIX.csv` | 5232 / `32F81A962262ACB5DAF668A425B57775F2F6BD2C117D702B26EBF23763C75DDF` |
| `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/01_RAW/REPIN_ANCHOR_WINDOWS.txt` | 18633 / `5BE0AC8A5BE0F46BD9FE1E200173E86174CF795D3D5A000E028C5C8032D370F3` |

### 7.2 Target corpus (LOCAL-ONLY; never committed)

`Entropia.exe` (PCG_9_3_5) — 8015872 B, SHA256
`E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — rehashed before/after
the run (executor) and independently by QC; unchanged. Represented in the package ONLY by
size, SHA256, build, the reproducible read method (Source-B range-safe PE API) and short
bounded instruction bytes; no proprietary payload in the repo.

## 8. Lineage rule

`REPORT CLAIM → SOURCE IDENTITY → PHYSICAL / RAW EVIDENCE → INDEPENDENT CHECK → STATUS`:
every load-bearing claim of this package traces to `01_RAW/` re-pins of the physical EXE
through `WRITE_PROVENANCE_LEDGER.csv` / `CLAIM_MATRIX.csv`, was independently re-measured by
the fresh QC (`QC_RESULTS.json` / `QC_REPORT.md`) and by PE-MASTER (`PE_MASTER_REVIEW.md`).
No generated file substitutes for the physical bytes; no report is treated as source-of-truth.
