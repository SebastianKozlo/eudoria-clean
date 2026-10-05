# EVIDENCE INDEX — PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005

Every raw artifact of this package, what it is, how it was produced, and
where its anti-circularity comes from. Machine evidence under 01_RAW;
documents and matrices at package root; instruments under 03_SCRIPTS.

## Raw machine evidence (01_RAW)

| Artifact | What it is / how produced | Independent source of truth |
|---|---|---|
| `ORACLE_INDEPENDENT_RECORDS.json` | The independent-oracle records: GNU objdump (GNU Binutils for Debian) 2.44 via WSL; per fixture: bytes, role, expected boundaries, FULL command line (`wsl -e sh -c "objdump -D -b binary -m i386 -M intel <fixture>"`), verbatim raw stdout/stderr, returncode. 71 synthetic fixtures: NEW-G (P2-2 falsifier), NEW-F (P2-1 falsifier), A1/A2/B/C/D/E, the complete H1 16-bit-addressing rm table (mod 0/1/2), the H2 grouped-opcode positive/negative controls (incl. the legal `66 0F 73 /3` PSRLDQ and `/7` PSLLDQ register forms and the invalid memory forms), and the P2-2 decoder unit vectors. | GNU objdump - an ISA oracle INDEPENDENT of the production decoder; expected boundaries were locked from objdump BEFORE the corrected decoder was written (never the reverse). |
| `C2_COMMIT_MESSAGE_VERBATIM.txt` | The verbatim C2 commit message (immutable history). Referenced by supersession record S-P2-03; history is never edited. | Q14 machine-checks this file equals `git log -1 --format=%B c4cb60f...` (commit_message_verbatim_fidelity). |
| `C1_PIN_EVIDENCE.json` | Regenerated pin evidence: 133 preserved pins re-measured against the pinned EXE with the corrected decoder + corrected (order-independent) boundary machinery; per-pin opcode_bytes/length/boundary fields + the effective_address object for the 46 mem pins + censuses. | The pinned EXE (static byte reads); boundary fields re-derived by the corrected machinery; Q2/Q3 re-derive every covered field independently in the battery. |
| `C2_CENSUS.json` | Regenerated census summary: measured quantities + closure statements + the AF3 note + known stores + the 0x0075138F ArkEstate lead re-verification. | The pinned EXE; counts re-summed from the emitted CSV by gate Q9. |
| `C3_OBJECT_SCOPE.json` | Regenerated object-scope facts with the corrected instruments: ctor extent decode (RET_REACHED, 93 instructions), the 3 effective-displacement-0 stores with segment semantics (2 FS:[0] SEH stores + the [EDI] cursor store), DIRECT_VPTR_STORE_IN_EXAMINED_CTOR, known callsites, ctor call-site census, allocation-size facts. Values measured UNCHANGED vs C2 (fresh regeneration, not a copy - see the diff evidence). | The pinned EXE; gate Q8 re-derives the collection. |
| `CQC_DECODER_UNIT_TESTS.json` | The decoder unit battery: 64 vectors measured from the generated artifact (count never hard-coded) - the inherited C2 vectors + P2-2 (0F 84 rel32 = 6; 66 0F 84 / 66 0F 8F rel16 = 5; 67 0F 84 REJECT) + H1 (rm=7 [BX] vs rm=6 [BP+disp] vs rm=6 mod=0 [disp16], register names spot-checked) + H2 (legal 0F BA /4-/7 incl. memory forms; legal MMX/SSE2 imm-shift register forms incl. PSRLDQ/PSLLDQ; reserved 0F BA /0-/3; reserved/invalid 0F 71/72/73 reg+mod+prefix combinations; F2/F3 forms) + census re-decode of all 2612 rows. | Expected values locked from the independent objdump oracle; the census re-decode is against the pinned EXE. |
| `CQC_BOUNDARY_COUNTEREXAMPLES.json` | The boundary-test matrix evidence: A1, A2, B, C, D, E, NEW-F (with ANCHORS, both stream boundary lists, cached+uncached crosscheck, and the ORDER_PERMUTATION_PROOFS: 56 synthetic permutations + 50 randomized orders of the real 0x004B0980 production stream, every result invariant), NEW-G (with INTERNAL_E8_PROMOTED=NO and the oracle record reference), REAL-REFUTE (the two real driver pins re-derived REFUTED_MID_INSTRUCTION refuted_by=0x004B0980), REAL (the three real-EXE positive CALL controls), the non-E8 control, the census discipline sweep, and the anchor registry. | The pinned EXE for real cases; the synthetic fixtures' expected boundaries from the objdump oracle; the permutation proofs falsify insertion-order dependence. |
| `CQC_MUTATION_RESULTS.json` | The 7 causal mutations with exact BEFORE/AFTER values and the EXACT failing predicates measured on each mutated run: M1 (JSON ctor opcode_bytes -> Q2), M2 (CSV callback measured_operand -> Q3), M3 (C3 store collection removed -> Q8), M4 (census containing_function -> Q6), AF3/Q8 (COMPOUND: manager row IDENTITY_EDGE + IDENTIFIED_OBJECT + IDENTITY_EVIDENCE + ADDRESS_PROVENANCE_STATUS removed -> Q7, 5 failing predicates), M5 (JSON EA base_register ESI->EAX -> Q2), M6 (JSON EA provenance -> fake known-function provenance -> Q2). | Each mutation is applied to a TEMPORARY COPY of the ACTUAL final artifact in a temp tree OUTSIDE the repo (deleted after; never persisted); UNMUTATED=PASS -> MUTATED=FAIL through the SAME gate function object. |
| `CQC_FINAL.json` | The fresh QC record: 13 data-mode gates Q1-Q13 (all PASS), the 7/7 mutation summary, the docs-mode Q14 record (run last), qc_scope=SELF_CHECK (executor self-QC; author/origin explicit). | Every gate status derived from measured inputs on disk. |
| `CHANGED_FIELDS_VS_C2.json` | The full regression change table vs the committed C2 artifacts (READ-ONLY comparison): every changed field of the pin JSON/CSV, all 2612 census rows, the C2_CENSUS measured quantities, the C3 key fields, the AF3 ledger rows, and the boundary-case set: 16 pin boundary-field changes (the two declassified driver pins x {boundary_status, boundary_source, boundary_start, boundary_refuted_by} x {JSON, CSV}), 7 new boundary cases, ZERO census row changes, ZERO quantity changes, ZERO C3/AF3 changes. | Both sides read from disk; the census CSV and AF3 ledger additionally verified BYTE-IDENTICAL to the committed C2 files (fresh regeneration measured unchanged, not copied). |

## Root matrices

| Artifact | What it is |
|---|---|
| `CORRECTED_PIN_LEDGER.csv` | The regenerated same-VA pin ledger (133 records, 0 failures; identical statuses to C2; the two driver pins' boundary fields updated per S-P2-05/S-P2-06). |
| `CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv` | The regenerated census (2612 rows) - byte-identical to the committed C2 census (measured). |
| `AF3_PROVENANCE_LEDGER.csv` | The regenerated AF3 ledger (5 rows: the manager PROVEN row + the 4 downgraded layout controls) - byte-identical to C2 (measured). |
| `AF1_MUTATION_MATRIX.csv` | The 7-row mutation matrix incl. BEFORE_VALUE/AFTER_VALUE and failing-predicate counts. |
| `AF2_BOUNDARY_TEST_MATRIX.csv` | The boundary-test matrix: 13 cases, each row persisting BYTES, ANCHORS, EXPECTED_DECODE, MEASURED_BOUNDARIES, ACTUAL_DECODE, EXPECTED/ACTUAL_CALL_PROMOTION, BOUNDARY_SOURCE/STATUS, CALL_VALIDATION, REFUTED_BY, FAILURE_CONDITION_DETECTED, and the historical defect note. |
| `CHANGED_BOUNDARY_FIELDS_VS_C2.csv` | The change table (artifact / row_or_pin / field / old / new) - 23 rows. |

## Instruments (03_SCRIPTS; all sys.dont_write_bytecode = True, --out/--csv/--pkg-root overrides)

| Script | Role |
|---|---|
| `x86dec.py` | Corrected fail-closed decoder: C2 lineage + P2-2 BRANCH A (66 0F 8x rel16) + H1 (rm=7 = [BX]) + H2 (grouped-opcode validity by opcode+reg+mod+prefix). |
| `pebnd.py` | Corrected boundary machinery: C2 lineage + P2-1 (sorted, order-independent extents coverage; module-level `covers_mid_instruction` sorts its input; anchor-conflict policy unchanged). |
| `c1_pin_ledger.py` | Pin JSON+CSV generator (this run's defaults). |
| `c2_census.py` | Census generator (this run's defaults). |
| `c3_object_scope.py` | C3 generator (this run's defaults). |
| `cqc_battery.py` | The corrected QC battery (Q1-Q14 + the 7-mutation harness + NEW-F/NEW-G/REAL-REFUTE + permutation proofs). |
| `capture_independent_evidence.py` | Oracle capture (71 fixtures) + the C2 commit-message verbatim capture. |
| `diff_vs_c2.py` | The regression change table vs the committed C2 artifacts. |
| `make_manifest.py` | Manifest generator (this run's defaults). **NOT RUN in phase 1** - the manifest is generated LAST in phase 2 only. |

## Oracle record example (verbatim, NEW-G)

Command line (persisted per fixture):
`wsl -e sh -c "objdump -D -b binary -m i386 -M intel /mnt/c/Users/User/AppData/Local/Temp/opencode/p2fix_oracle/NEW_G_66_0F_84_je_rel16.bin"`

Raw output (verbatim in 01_RAW/ORACLE_INDEPENDENT_RECORDS.json):

```
   0:	66 0f 84 00 00       	je     0x5
   5:	b8 00 e8 01 00       	mov    eax,0x1e800
   a:	00 00                	add    BYTE PTR [eax],al
   c:	c3                   	ret
```

(The C2 decoder measured the first instruction as 7 bytes and its anchor
stream landed on the E8 at +7 - interior to the MOV immediate - fabricating
a CALL edge; the corrected decoder measures 5 and the candidate is
REFUTED_MID_INSTRUCTION with INTERNAL_E8_PROMOTED = NO.)
