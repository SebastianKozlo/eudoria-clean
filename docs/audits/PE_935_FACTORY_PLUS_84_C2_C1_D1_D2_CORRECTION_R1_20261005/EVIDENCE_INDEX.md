# EVIDENCE INDEX — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005

Every raw artifact of this package, what it is, how it was produced, and
where its anti-circularity comes from. Machine evidence under 01_RAW;
documents and matrices at package root; instruments under 03_SCRIPTS.

## Raw machine evidence (01_RAW)

| Artifact | What it is / how produced | Independent source of truth |
|---|---|---|
| `D1_INDEPENDENT_ORACLE_RECORDS.json` | The independent-oracle records: GNU objdump (GNU Binutils for Debian) 2.44 via WSL; per fixture: bytes, role, expected boundaries, FULL command line (`wsl -e sh -c "objdump -D -b binary -m i386 -M intel <fixture>"`), verbatim raw stdout/stderr, returncode. 80 synthetic fixtures: the 71 carried fixtures recaptured (NEW-G, NEW-F, A1/A2/B/C/D/E, the complete H1 rm table, the H2 controls, the P2-2 unit vectors - role texts annotated REPRODUCED_THIS_RUN) + 9 D1 fixtures (the `0F 73 /4` negatives `0F 73 E0 02` / `66 0F 73 E0 02`, the six contract legal controls, the downstream falsifier stream). | GNU objdump - an ISA oracle INDEPENDENT of the production decoder; this run's D1 expected verdicts were locked from the D1 contract + the ISA reference BEFORE the corrected decoder's D1 behaviour was evaluated (never the reverse). The objdump recovery disassembly after (bad) in the falsifier stream is NOT treated as execution evidence. |
| `BASE_COMMIT_MESSAGE_VERBATIM.txt` | The verbatim BASE (THREE-P2) commit message at 9d31a82 (immutable history; 4,918 B). Referenced by supersession record S-CM-01; history is never edited. | Q14 machine-checks this file equals `git log -1 --format=%B 9d31a82...` (commit_message_verbatim_fidelity). |
| `C1_PIN_EVIDENCE.json` | Regenerated pin evidence: 133 pins re-measured against the pinned EXE with the D1-corrected decoder + carried corrected boundary machinery; per-pin opcode_bytes/length/boundary fields + the effective_address object for the 46 mem pins + censuses. Identical to BASE after excluding the declared `run` label (measured by REGRESSION_DIFF.json). | The pinned EXE (static byte reads); gate Q2 re-derives every covered field independently, now ALSO bound to the BASE-pinned PINS roster. |
| `C2_CENSUS.json` | Regenerated census summary: measured quantities + closure statements + the AF3 note + known stores + the 0x0075138F ArkEstate lead re-verification. All 13 quantities identical to BASE (measured). | The pinned EXE; counts re-summed from the emitted CSV by gate Q9. |
| `C3_OBJECT_SCOPE.json` | Regenerated object-scope facts: ctor extent decode (RET_REACHED, 93 instructions), the 3 effective-displacement-0 stores (2 FS:[0] SEH stores + the [EDI] cursor store), DIRECT_VPTR status, known callsites, ctor call-site census, allocation-size facts. Values identical to BASE (fresh regeneration, measured). | The pinned EXE; gate Q8 re-derives the collection. |
| `CQC_DECODER_UNIT_TESTS.json` | The decoder unit battery: 72 entries measured from the generated artifact (64 carried + 8 D1 entries; 6 new distinct byte patterns - two D1 entries duplicate the carried 0F 73 /2 and /6 patterns with D1 notes) + census re-decode of all 2612 rows + coverage windows. | Expected values locked from the independent objdump oracle; the census re-decode is against the pinned EXE. |
| `CQC_BOUNDARY_COUNTEREXAMPLES.json` | The boundary-test matrix evidence: A1, A2, B, C, D, E, NEW-F (ANCHORS, both stream boundary lists, cached+uncached crosscheck, the order-permutation proofs), NEW-G, the NEW D1_0F73_4_DOWNSTREAM_FALSIFIER case (corrected outcome + the in-run BASE reproduction with module identities + the .text pattern census), 2x REAL-REFUTE, 3x REAL positive controls, the non-E8 control, the census discipline sweep and the anchor registry. 14 cases. | The pinned EXE for real cases; the synthetic fixtures' expected boundaries from the objdump oracle; the BASE defect reproduction is MEASURED through the committed BASE modules (READ-ONLY import; identities recorded). |
| `CQC_MUTATION_RESULTS.json` | The 7 RETAINED causal mutations (M1, M2, M3, M4, AF3/Q8 compound, M5, M6) with exact BEFORE/AFTER values and the exact failing predicates; each routed through the SAME production gate on a TEMPORARY COPY of the ACTUAL regenerated artifact (temp tree OUTSIDE the repo, deleted after). | Same-gate causality; the mutation targets are the actual artifacts, never fixtures. |
| `D2_MUTATION_RESULTS.json` | The 8 NEW D2 causal controls (D2-M1..M8: compound kind+EA removals x2, whole-pin deletions x2, duplicate claim, extra claim JSON, extra claim CSV, synchronized JSON+CSV omission with adjusted totals) with per-case SEMANTIC_DELTA, BEFORE/AFTER artifact hashes, per-case INPUT_HASH_CENSUS (unrelated inputs byte-identical to the production package), exact failing predicates and the substitute-failure check. | The production gate_q2's OWN predicates against the pinned EXE + the BASE-pinned roster (no manifest/Git-baseline/other-gate failure can substitute). |
| `D1_BOUNDARY_FALSIFIER.json` | The mandatory D1 downstream falsifier record: synthetic `0F 73 E0 02 E8 05 00 00 00 C3`, synthetic strong entry at +0; corrected machinery: UNRESOLVED / NOT_VERIFIED / no promotion; BASE (THREE-P2) modules measured: CONFIRMED / PASS / target 0x00A0000E; the .text occurrence census of the affected pattern (zero, both forms); the synthetic-fixture scope note. | Both decoder versions' outcomes measured in-run through the same production boundary machinery; module file identities recorded; no VA/fixture special-casing. |

## Root machine artifacts

| Artifact | What it is |
|---|---|
| `EXPECTED_PIN_REGISTRY.json` | The D2 expected roster: 133 claims with va/role/expect_bytes/expect_ea/expect_imm; extracted from the BASE-pinned `03_SCRIPTS/c1_pin_ledger.py::PINS` Git blob (blob 5a7b642f...) by AST literal evaluation (no historical code executed); source identity recorded; gate Q2 re-derives it in-run from the same blob and requires the file to EQUAL the re-derivation (registry tamper = FAIL). |
| `CORRECTED_PIN_LEDGER.csv` | The regenerated same-VA pin ledger (133 records, 0 failures; identical statuses to BASE) - BYTE-IDENTICAL to the committed BASE file (measured by REGRESSION_DIFF.json). |
| `CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv` | The regenerated census (2612 rows) - BYTE-IDENTICAL to the committed BASE census (measured). |
| `AF3_PROVENANCE_LEDGER.csv` | The regenerated AF3 ledger (5 rows) - BYTE-IDENTICAL to BASE (measured). |
| `AF1_MUTATION_MATRIX.csv` | The 15-row mutation matrix (7 retained controls + 8 D2 controls) incl. MUTATION_CLASS, BEFORE/AFTER values and failing-predicate counts. |
| `AF2_BOUNDARY_TEST_MATRIX.csv` | The 14-case boundary matrix incl. the D1_0F73_4_DOWNSTREAM_FALSIFIER case. |
| `REGRESSION_DIFF.json` | The complete regression vs the exact BASE package: byte-identity per artifact, declared-metadata-only changes (the run labels), every content change (all expected D1/D2 additions), census/pin/AF3/quantity comparisons (0 row/field changes). |

## Documents

INPUT_IDENTITIES.md, GENERATION_RECORD.md, FINAL_REPORT.md, QC_REPORT.md,
EVIDENCE_INDEX.md, HANDOFF.md, SUPERSESSION_LEDGER.md (9 records),
PE_MASTER_REVIEW.md (explicit placeholder: the review is the PE-MASTER
persistence phase; PE_MASTER_REVIEW_PERFORMED_BY_THIS_RUN = NO).

## Instruments (03_SCRIPTS; all sys.dont_write_bytecode = True, --out/--csv/--pkg-root overrides)

| Script | Role |
|---|---|
| `x86dec.py` | The D1-corrected fail-closed decoder: THREE-P2 lineage + the per-opcode 0F 71/72/73 legal-reg tables (0F 73 /4 rejected in both prefix classes; /4 legal for 71/72; 66 0F 73 /3,/7 legal; mod=3/memory/F2-F3/0F BA behaviour unchanged). |
| `pebnd.py` | Carried boundary machinery (sorted extents, anchor-conflict policy, call promotion rules) - unchanged; the D1 decoder change is measured through it. |
| `c1_pin_ledger.py` | Pin JSON+CSV generator (PINS carried verbatim; the D2 expected roster). |
| `c2_census.py` | Census generator (run label only). |
| `c3_object_scope.py` | C3 generator (run label only). |
| `cqc_battery.py` | The D1/D2-corrected QC battery: Q1-Q14 + the retained 7-mutation harness + the NEW run_d2_mutations harness + the D1 falsifier case with in-run BASE reproduction. |
| `capture_independent_evidence.py` | Oracle capture (80 fixtures) + the BASE commit-message verbatim capture. |
| `pin_roster.py` | NEW: the expected-roster extraction from the BASE Git blob (ast literal evaluation; in-process cache; identity recording). |
| `extract_expected_pins.py` | NEW: EXPECTED_PIN_REGISTRY.json generator. |
| `diff_vs_base.py` | NEW: the regression vs the exact BASE package (byte identity vs declared-metadata-excluded identity). |
| `make_manifest.py` | Manifest generator (LAST; self-excluded; entrypoint covered at its CURRENT BASE state). |

## Oracle record example (verbatim, D1 negative)

Command line (persisted per fixture):
`wsl -e sh -c "objdump -D -b binary -m i386 -M intel /mnt/c/Users/User/AppData/Local/Temp/opencode/d1d2_oracle/D1_NEG_73_4_E0.bin"`

Raw output (verbatim in 01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json):

```
   0:	0f 73                	(bad)
```

(The committed BASE decoder decoded these 4 bytes as a valid 4-byte
immediate-shift instruction and certified a later E8 through that stream -
see 01_RAW/D1_BOUNDARY_FALSIFIER.json; the corrected decoder REJECTs the
form and the stream stops.)
