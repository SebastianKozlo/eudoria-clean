# 00_CONTROL — PLAN (PE-NIF-CLAIM-EVIDENCE-LOCK-R1)

## Mandate
Execute the bounded reconciliation round PE-NIF-CLAIM-EVIDENCE-LOCK-R1 per
NEXT_OPENCODE_PROMPT.md (SHA256 BFDB1D23E42904FB29CBDB5995D072B8C793AB5D4E241E28BF7F3EFA8EEBA562,
verified before execution). P0 = CLAIM–EVIDENCE SCOPE LOCK. Verify the
auditor's allegations from raw evidence; do NOT copy them unverified; produce
claim/denominator/counterexample reconciliation + doc-correction PROPOSALS.

## Execution plan (as executed)
1. Mandatory reading: AGENTS.md; PE_CURRENT_CHECKPOINT / PE_WORKFLOW_RULES /
   PE_MASTER_CONTEXT / PE_CANONICAL_STATE / PE_CONTEXT_SOURCES /
   PE_SESSION_HANDOFF; the external-audit final report; probe.json;
   probe.cjs; all 12 referenced run dirs (REPORT, gates, artifact_index,
   raw result JSONs per F1-F6).
2. docs/nif reference state: record HEAD (8cd0bc3), working-tree cleanliness,
   diff vs 077b8a4 (empty), current SHA256 of both wiki targets.
3. Writer-conflict check: ACTIVE_WRITER.lock scope vs this run's writes
   (no overlap; read-only on writer paths; no lock takeover).
4. Six controls, each grounded in RAW evidence:
   - C1 (R32): independent re-sum of ANIM_FRAME_CHECK.json (985/142/30 check;
     frame==slot; ANIM16-31 recount vs the report's "10 of 45").
   - C2 (R33/R34): meta re-read of REAL_SPARSE_GRAMMAR.json (6167/2427/3186/
     2093); k=1 counterexamples (574845.nif bi=69 si=14/27); parse_variable
     driver-source inspection (first-match vs uniqueness); classifier
     definition read verbatim.
   - C3+4 (R35/R36): direct BNT2 index parse of BOTH original containers;
     era join (identical/changed/unique separation); c==CRC32 all; d==c;
     the 3 same-payload-different-d names; changed-payload family-witness
     scan (block-name scan + coarse diff-region intersection, labeled
     approximate); FIELD_D_TESTS formula range; writer-evidence absence.
   - C5 (R29/R37/R38): spot re-reads of PATTERNS.json (14/10/834),
     CLASS_SEQUENCES.json (348/348 root-last), MODE_ANALYSIS.json (mode
     census + 41076 twin pair + verdict block).
   - C6 (R39/R40): proposal counts; exact re-application of the 9 R40
     proposals onto git 077b8a4^ (byte-exact apply proof); numstat (+236);
     manifest validation (11 strict errors / 8 manifests) + 12 normalized
     sidecars; wiki overclaim site inventory.
5. Outputs: 00_CONTROL (this plan + hash-lock + one-time scripts);
   01_RAW (CONTROL_R1_RESULTS.json); 02_LOGS; 03_STATIC (SOURCE_QUOTES.md);
   04_RUNTIME (NOT_RUN.md); 05_ANALYSIS (CLAIM_MATRIX.csv 43x14,
   ALLEGATION_DISPOSITIONS.csv 23, DENOMINATORS.json, COUNTEREXAMPLES.json,
   NORMALIZED_MANIFESTS 12x CSV); 06_REPORT (00_FINAL_REPORT.md +
   PROPOSED_DOC_CORRECTIONS.md); REPORT.md; STAGE_ACCEPTANCE_GATES.csv;
   artifact_index.csv (real hashes; self-exclusion documented); HANDOFF.md.
6. HARD STOP after report + handoff; no wiki/canon/loop writes; no commit;
   no old drivers; no game; no new discoveries.

## Hash-lock discipline
- Prompt SHA verified pre-execution (see above).
- control_r1.cjs: hash-after-last-edit, executed twice (exec-1 trailing-blank
  parser artifact fixed; both hashes in SHA256_CONTROL.txt, recorded BEFORE
  each execution).
- generate_claim_matrix.cjs / generate_artifact_index.cjs: run-dir analysis
  instrumentation; their outputs validated (strict CSV, 0 bad rows).
- artifact_index.csv excludes itself (self-hash impossibility — documented
  exclusion row inside the manifest).

## Deviations from plan
None material. The only mid-run corrections (both documented in 02_LOGS):
control_r1.cjs exec-1->exec-2 (trim standard), CLAIM_MATRIX emitter hygiene
(quoted fields; single-status-per-atomic-claim split of compound rows).
