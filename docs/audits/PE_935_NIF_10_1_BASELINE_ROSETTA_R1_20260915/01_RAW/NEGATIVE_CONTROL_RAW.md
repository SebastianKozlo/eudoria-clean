# NEGATIVE_CONTROL_RAW — PE_935_NIF_10_1_BASELINE_ROSETTA_R1 (§19/L19)

Every negative control below was EXECUTED (not merely designed). A control
passes when the validator REALLY FAILS on the corrupted input (proving the
validator is driven by bytes, not by priors or parser outputs).

## NC-SET-A — BNT2 walker fail-closed controls (s01_bnt2_walk.py)

Synthetic BNT2 built from SYNTHETIC payloads (no proprietary bytes):

| Control | Manipulation | Expected | Actual | Verdict |
|---|---|---|---|---|
| NC_BASE | none | walk PASS | PASS | control-of-control OK |
| NC_TRUNCATE | file cut to 50% | FAIL | FAIL(E_MAGIC) | PASS |
| NC_CORRUPT_COUNT | NumEntries declared n+1 | FAIL | FAIL(E_NAME_EOF) | PASS |
| NC_WRONG_ENDIAN | walker forced big-endian footer | FAIL | FAIL(E_DIR_OFFSET) | PASS |

Real-archive invariants (all PASS on Models.bnt): E_EOF_EXACT (index ends
exactly at filesize-8), entry bounds [0, DirOffset), zero overlaps, zero
duplicate names, 100% payload coverage (coverage_bytes == dir_offset; 0
interior gaps).

## NC-SET-B — parser-output echo controls (s05_crosscheck_parser_manifest.py)

Prove the census scanner is NOT echoing pcg953_nif_manifest.csv (R61 output):

| Control | Manipulation | Expected | Actual | Verdict |
|---|---|---|---|---|
| NC_ECHO_VERSION_CORRUPT | version u32 @39 → 0xDEADBEEF | scan FAIL | SCAN_FAILED(E_NOT_10_1) | PASS |
| NC_ECHO_NUMBLOCKTYPES_CORRUPT | u16 @51 → 0xFFFF | scan FAIL | SCAN_FAILED(E_NUMBLOCKTYPES_SANITY) | PASS |
| NC_ECHO_NUMBLOCKS_CORRUPT | u32 @47 → 0x7FFFFFFF | scan FAIL | SCAN_FAILED(E_NUMBLOCKS_SANITY) | PASS |
| NC_ECHO_TRUNCATE_HEADER | payload cut at byte 60 | scan FAIL | SCAN_FAILED(E_SHORT_TYPE) | PASS |

Post-hoc comparison (sanctioned AFTER census): independent census vs R61
manifest = MATCH 4838/4838 files (type histograms + num_blocks identical);
0 misclassifications; type totals identical. This is mutual validation, not
echo (the corrupted-input controls prove byte-dependence).

## NC-SET-C — closure-decoder dependency controls (s06/s07)

The closure decoder's decisions come from bytes via closure constraint:

| Control | Mechanism | Result |
|---|---|---|
| NC_CLOSURE_EXACTNESS | every accepted file must consume ALL bytes + EOF-exact + TopObjects | 2,343 PASS / 20 PARSE_BLOCKED (0 silent accepts) |
| NC_GROUPID_INVARIANT | per-block GroupID must be 0 (PE) | any nonzero → backtrack/fail; 0 violations accepted |
| NC_REF_RANGE | all refs must be -1 or [0, num_blocks) | 0 out-of-range accepted in 2,343 closed files; 24 ArkTexture OOR refs were recorded as anomalies at the time [F-14/AMEND-009: all 24 were fake entries of the 24 mis-parsed blocks (the next block's GroupID/"ArkViewportInfo" name bytes consumed as entry fields) — retracted; 0 OOR refs remain in the re-derived true parse] |
| NC_FLOAT_SANITY | NaN/Inf → fail | enforced; no NaN/Inf accepted |
| NC_BOUNDARY_SEARCH_EXHAUSTION | wrong Ark candidates must fail downstream | search-exhausted files recorded as FAIL (never guessed) |
| NC_HYPOTHESIS_FREEZE | decoder changed between TRAIN and HOLDOUT? | NO — hypothesis_sha identical (6DB2F1E3...); holdout run 467/473 reproduced deterministically in the ALL-pass |

## NC-SET-D — anti-circularity of the baseline

- Census (s03) reads ONLY header/type-table bytes via own walker; the type
  census CSV existed before any manifest comparison (file timestamps in
  02_WORK and git-untracked package order).
- The field-decode (s06) is driven by the pinned SCHEMA (nif.xml HIST) +
  engine framing — never by wiki text or parser code; the wiki claims are
  compared POST-HOC (FINDINGS_LOG + LIVE_DOC_IMPACT_MATRIX).
- Where this run's byte-derived findings CONTRADICT prior claims
  (importer tail 41 vs 38; ref role; 24-block count variant [F-14/
  AMEND-009: this CONTRADICTION is RETRACTED — the byte re-derivation
  supports the prior formula claim in-slice; the "variant family" was
  this run's own decoder artifact]), the byte evidence wins and the
  contradiction is recorded — the validator did not inherit its outputs.

## Residual honesty notes

- The greedy candidate ORDER (schema-first, footer-preferring) could in
  principle accept a byte-compatible but semantically mislabeled split
  (width-identical ambiguities are disclosed as such — ApplyMode 2xu16 vs
  u32; VertexColor split; importer 38+3 vs 41 attribution). Where two
  parses consume identical bytes, closure cannot arbitrate SEMANTICS —
  these are explicitly NOT claimed as resolved. [CONFIRMED post-freeze:
  exactly this artifact class materialized in the ArkTexture count
  decisions — F-14/AMEND-009.]
- [F-14/AMEND-009 RETRACTION] The formerly recorded "24 ArkTexture
  anomaly entries and 3 NiNode-target refs" were NOT in-file garbage:
  they were fake entries produced by this run's own count-candidate
  ordering on 24 mis-parsed blocks (18 zero-count + 6 true-count-1/2;
  the next block's GroupID/"ArkViewportInfo" name bytes consumed as
  entry fields). The true parse has 0 OOR / 0 NiNode refs. Per-block
  evidence: 01_RAW/ARKTEXTURE_ZERO_COUNT_REDERIVATION.csv +
  ARKTEXTURE_FAKE_ENTRIES_RETRACTED.csv.
