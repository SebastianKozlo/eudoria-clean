# HANDOFF — PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1

RUN_ID = PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203
EXECUTED BY = pe-reconstruction (single bounded governance round; no nested
agents; no repo writes)
DATE = 2026-09-05
INPUT = 00_CONTROL\NEXT_PROMPT.md (SHA256
c9ccb5bb56fa8dd8f140f4c3126adc8aa9beddc4cb14d50fb9d0b7c0329276a2, verified
before execution) + the R3 proposal file 06_REPORT\PROPOSED_DOC_CORRECTIONS_R3.md
of PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627 (SHA256
84b3d05db719ab09a6ceece8300bbee059655b5443f6b5cfc1090b4c8b7ec8e6 — matches the
tasking pin AND the R3 manifest row; re-verified in-driver).

## What this run did (scope: items 3-5 of the prompt; items 1-2 were the
## master-auditor's, item 6 is the master's)

1. ITEM 3 — 06_REPORT\GATE_WEAKNESS_ADDENDUM.md. The three gate weaknesses from
   the follow-up review were each CODE-CONFIRMED by reading the actual R3
   source (revalidate_r3.py, hash-verified against the R3 manifest):
   - R3G6c (lines 291-292): `if vec[1]` skips the empty-payload KAT vector —
     13/14 compared, label claims "all 14".
   - R3G10 (lines 508-512): the PASS predicate forces adler32(name) + five
     crc32 classes only; adler32(payload) and fnv1a(name) are emitted (lines
     513-517) but not enforced.
   - Implementation-count overstatement (line 474 claim): actual per-entry
     counts = FNV 2, adler32(name) 3, adler32(payload) 3 full + iterative
     sample leg (6,335/11,022 entries, 247,004,079 B); 6 occurrences of the
     claim located in the R3 package.
   PLUS the minor STAGE_ACCEPTANCE_GATES.csv omission from the R3
   artifact_index.csv (33 rows, no gates row) — confirmed. The addendum
   assesses materiality for each (LOW; no R3 conclusion invalidated) and
   records gate-design guidance. THE COMPLETED R3 PACKAGE IS UNMODIFIED —
   re-hashed 33/33 rows twice (verify + index phases).

2. ITEM 4 — 05_ANALYSIS\TARGET_MAP.json. Full map for P1R2-5-R3 /
   P2R2-2-R3 (as FIXED) / P3R3 / P4R3 / P5R3: proposal_id -> target file ->
   EXACT old fragment (verbatim, with CURRENT line numbers) -> operation
   (REPLACE / LEDGER-ENTRY / STANDING-RULE / STANDING-POLICY) -> proposed new
   text (verbatim from the hash-pinned proposal; the P2/P3 fixes applied) ->
   evidence pointer. MACHINE-VERIFIED: all 13 old fragments occur EXACTLY ONCE
   in their target files (newline-aware, CRLF-adapted; counts recorded per
   entry). docs/nif targets: 09-semantics.md:180 + 191-192 (P1R2-5-R3),
   10-containers-corpus.md:121-125 (P2R2-2-R3-FIXED). R2 historical targets
   (ledger entries, NOT edited): 00_FINAL_REPORT.md:101-102 + 129-132,
   run_gates.py:50/:249/:366, TEST_RESULTS.json:127/:207,
   STAGE_ACCEPTANCE_GATES.csv:9 (x2) /:14. The P1R2-5-R3 new text is carried
   as two segments whose join EQUALS the full proposal NEW (machine-checked);
   every verbatim-marked text is a whitespace-normalized substring of the
   hash-pinned proposal file.

3. ITEM 5 — 06_REPORT\PROPOSALS_P2P3_FIXED.md. P2R2-2-R3-FIXED removes the
   categorical "every BYTE-EXACT VALIDATOR ... 100%" clause and scopes to the
   measured claim population (per-claim R35 table results; C-MORPH-1 partial
   fit 86.2%/81.0% with ASCII-only changed-payload morph family presence 3
   files/29 occurrences; C-MORPH-2 signature-not-validator; C-G3B-3/C-SHAD-2
   EVOLVED). P3R3-FIXED replaces the general "zero-match is insensitive to
   value errors" / "provably insensitive" with the evidence-bounded statement:
   insensitivity PROVEN for the specific R3 wrong-value controls
   (adler32_wrong_xor, fnv1a_wrong_basis) and the two R2 hash defects on the
   2003 and 9.3.5 Models.bnt corpora — NOT a general property. Machine
   checks: forbidden clauses absent, unchanged heads verbatim in the proposal,
   fixed texts extracted from EXTRACT markers (the map embeds the same
   extraction — no divergence possible).

4. CENSUS — 05_ANALYSIS\CONTRADICTION_CENSUS.json. READ-ONLY census of
   docs/nif (13 md files, hashed before/after — identical; this run modified
   nothing). Review citations verified at CURRENT lines (no shift):
   09-semantics.md:180, 08-ark-proprietary.md:196, 10-containers-corpus.md:121.
   9 FLAGGED occurrences total (position deltas 09-sem:180; delta triples
   09-sem:191 + 08-ark:196-197; true structure 08-ark:196; cross-era 100%
   family 10-cont:105, 121-125, corpus/README.md:30) — INCLUDING 2 uncited
   occurrences the census added (corpus/README.md:30 and 10-containers-
   corpus.md:105). 3 already-hedged "9-float triple grouping" occurrences
   (08-ark:206, 11-open-problems.md:36, README.md:92); 3 ITER-21-residual
   interaction items (09-semantics.md:195-196, 08-ark-proprietary.md:215) —
   these coexist with (not contradicted by) the R3 P1R2-5-R3 334/62/272
   wording; 4 ABSENCE checks all zero (no R3-superseded method-provenance
   wording stands in docs/nif); 3 OUT-OF-SCOPE wordings recorded for
   completeness only (R1/R2-PENDING proposal targets, NOT R3-superseded):
   d==c biconditional 09-semantics.md:208 + 10-containers-corpus.md:23;
   README.md:3 "complete, evidence-based".

## Gates

STAGE_ACCEPTANCE_GATES.csv = 13 EXECUTABLE PASS + 2 HUMAN_REVIEW PENDING
(HR-R1-1 addendum/fixed-texts adequacy for the master commit; HR-R1-2 target
map suitability for the future application run). Driver + data hashes
recorded in 00_CONTROL\SHA256_DRIVER.txt AFTER the last edit, BEFORE first
execution; the verify/index phases re-verify them (any change aborts).

## Package / manifest

artifact_index.csv = 11 rows, REAL SHA-256 computed in-driver at index time
(after all artifacts were final). THE MANIFEST EXCLUDES ITSELF (a manifest
cannot contain its own hash; documented precedent — recorded in REPORT.md,
here and in the driver docstring).

## What this run did NOT do

No docs/nif application (the two REPLACE edits remain proposals pending
HR-R3-3); no wiki edits (HOLD unchanged); no M2; no morph research; no
modification of the completed R3 package or ANY historical run (R3 re-hashed
33/33 unmodified, twice; R1/R2 sources read-only); no repo commits — the
master-auditor performs the final PATH-LIMITED commit (item 6) with full
staged-index control; no BDR/Hermes/PE-Vault writes.

## Next steps (master + human)

1. MASTER (item 6): path-limited commit of THIS run dir only, full staged-index
   control, per the standard discipline.
2. HUMAN: HR-R3-3 (proposal application decision) and the wiki HOLD remain
   unchanged by this run. If HR-R3-3 is later granted, the application run
   must consume 06_REPORT\PROPOSALS_P2P3_FIXED.md texts (NOT the uncorrected
   R3 P2/P3 clauses) + 05_ANALYSIS\TARGET_MAP.json (old fragments + exact
   lines already machine-verified; re-verify at application time) + the census
   for the interaction items (the 09-semantics.md:195-196 / 08-ark:215 ITER-21
   residual sentences are NOT contradicted by R3 and were NOT mapped as edits).
3. Gate-design guidance from the addendum (labels state the executed
   population; predicates enforce what is emitted; per-class implementation
   counts; every published artifact indexed) applies to FUTURE run suites —
   the R3 package itself stays frozen.
