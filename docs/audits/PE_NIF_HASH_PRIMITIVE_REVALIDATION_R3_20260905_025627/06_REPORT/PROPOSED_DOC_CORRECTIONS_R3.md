# PROPOSED_DOC_CORRECTIONS_R3 — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3

STATUS: PROPOSALS ONLY. Nothing below has been applied. The repo, docs/nif, the
wiki, historical runs (R1/R2/R29-R40) and canon are UNCHANGED by this run. An
authorized applier (after the NEXT independent post-audit) must review, then
apply. These proposals SUPERSEDE the corresponding R2 items per
05_ANALYSIS/SUPERSESSION_MAP.csv (S-01..S-12); R2 items not listed here remain
as proposed in R2. R2 and all historical artifacts stay byte-unchanged.

Areas: PRIM = hash primitives / method provenance; F2 = morph-residual and
grammar-summary wording; F3 = three-state gate policy; F5 = sidecar bare-CR
policy.

## P1R2-5-R3 (supersedes R2 P1R2-5; claims R3C-10): morph residual wording

- OLD (R2 P1R2-5 proposed): "...334 real-record spans fit no tested grammar..."
- NEW: "[9 × f32 trailing values; grouping and semantic role UNVERIFIED — the
  tested variable-k model consumes 9 × f32 after the weight list; grouping them
  into three triples (e.g. 3 morph states × XYZ) is an OPEN HYPOTHESIS, not an
  established structure; divisibility of nine does not establish the grouping.
  Scope limits that MUST travel with this wording: the parser takes the
  SMALLEST k in 1..8 whose weight prefix sums ≈1.0 (first-match; segmentation
  uniqueness NOT proven); byte-exact on 2,093/2,427 classifier-real spans
  (86.2%; the 'real-record' class is a hypothesis-aligned classifier) and
  3,186/6,167 all fit spans; **334 classifier-real spans do not fit the tested
  VARIABLE-K model — of those 334, 62 have another recorded fit among the
  recorded alternatives (g1/g2/mscan; e.g. 592572.nif bi=65 si=45
  mscan_ok_m=[30]) and 272 have none among the recorded alternatives;
  alternative-model fits are recorded fits, NOT true segmentation and NOT
  semantic confirmation**; observed k ∈ {1,2,3,4} on 9.3.5 exact examples and
  k ∈ {1..5} on 2003.]"
- Basis: independent re-sum of the hash-pinned R34 per_span raw records
  (01_RAW/R34_RESUM.json; gate R3G12). NOT a new physical grammar execution.

## P2R2-2-R3 (supersedes R2 P2R2-2 summary sentence; claims R3C-11): 21-claim summary wording

- OLD (R2 P2R2-2 proposed): "...every byte-exact grammar reproduced at 100%
  and the rare-family and importer pattern censuses were count-identical..."
- NEW: "**Conclusion (CONFIRMED at the tested scope): in the 21 tested grammar
  claims on the 2003 and 9.3.5 Models.bnt corpora (5,426/5,426 + 5,596/5,596
  parse closure; note 5,208/5,422 shared files are byte-identical across
  eras), 19 claims are ERA-STABLE and 2 are EVOLVED (C-G3B-3 failure-profile
  delta; C-SHAD-2 vocabulary delta); every BYTE-EXACT VALIDATOR reproduced at
  100% WITHIN ITS TESTED POPULATION, and the rare-family and importer pattern
  censuses were count-identical. C-MORPH-1 is a PARTIAL-FIT claim (rr
  2,093/2,427 = 86.2% on 9.3.5; 1,180/1,457 = 81.0% on 2003), not a 100% fit.
  All drift observed in the tested claims was CONTENT; no grammar-level drift
  was found. No claim is made about untested claims, other archives, or other
  versions.**"
- Basis: verbatim transcription of the R35 21-claim table with exact claim IDs,
  denominators, verdicts and evidence statuses (01_RAW/R35_CLAIM_TABLE_PRESERVED.json;
  gate R3G13). "All 21 claims reproduced at 100%" must NOT be exported anywhere.

## P3R3 (ledger entries; claims R3C-01..R3C-09; supersedes R2 method-provenance wordings S-03..S-08)

Correction-ledger entries for the R2 texts that asserted the R2 Node hash
primitives as correct implementations (historical files are NOT edited):
- R2 06_REPORT/00_FINAL_REPORT.md Area B sentence "Node hand-rolled
  CRC32/adler32/FNV-1a cross-checked against Python zlib" → corrected: "the
  candidate census was recomputed with stage-local primitives validated by
  known-answer tests and per-entry oracle identity (R3); the R2 Node adler32
  and fnv1a helpers are CONFIRMED defective (value mismatches on 11,022/11,022
  name inputs, 11,022/11,022 payload inputs, and 11,016/11,022 name inputs
  respectively); the R2 crc32 helper and the size/offset candidates were
  correct; the aggregate counts were never affected because zero-match is
  insensitive to value errors".
- R2G8 wording "Python == Node == R36 historical" / "three independent
  computations" → corrected: "corrected primitives == R2 Python (zlib/exact-int)
  == R36 historical (zlib/exact-int); the R2 Node leg computed different
  functions whose zero-match aggregates coincidentally agreed".
- Standing rule (the P0): hash-primitive VALUE IDENTITY (known-answer tests +
  per-entry oracle agreement) must be established BEFORE aggregate acceptance,
  because aggregate zero-match counts are provably insensitive to value errors
  (demonstrated by the R3 wrong-value controls: KAT exit 1 with identical
  zero-match census, 02_LOGS/kat_wrong_value_controls.json + R3G7b).

## P4R3 (three-state gate policy; claims R3C-12/R3C-13; supersedes S-09/S-10)

- Human-review gate state MUST be serialized three-state: PASS / FAIL /
  PENDING (R2's `'pass': bool(ok)` turned pending into false/FAIL — R2 HR-1..4
  were PENDING, not FAIL; reproduced as a negative control with exit code 1).
- Gate tally labels MUST be derived from the actual emitted rows at emit time
  (R2G13's "{CONFIRMED 17, REJECTED 7}" label vs the actual 16/8 rows).
- OVERALL EXECUTABLE PASS must always be presented as distinct from human
  acceptance (explicit human_acceptance field: PENDING_HUMAN_REVIEW).

## P5R3 (sidecar bare-CR policy; claims R3C-14; documents R2 Area C acceptance)

- The accepted 12/12 byte-lossless sidecars (R2 Area C) are PRESERVED; no
  manifest migration is requested or authorized.
- Where semantic header normalization is restated, the policy line is explicit:
  semantic mapping follows the CUSTOM PHYSICAL-LINE CONTRACT (a bare CR inside
  a physical row is DATA; the R2 builder csvParse semantics). Under standard
  CSV record semantics exactly one row (R39 row 10) parses differently
  (computed_by "n/a\r" vs "n/a") — an INTERPRETIVE difference, NOT raw-byte
  loss; both layers reconstruct the original bytes exactly (R3G14:
  12/12 SHA-equal reconstruction + 0 field-mapping errors under the custom
  contract, R39 row 10 included).

## Not proposed (explicitly out of scope)

- No wholesale manifest migration; no wiki edits; no docs/nif edits (P1R2-5-R3
  and P2R2-2-R3 remain proposals exactly like their R2 predecessors); no
  change to any historical run; no new morph-boundary research; no promotion
  of alternative fits to true segmentation; no milestone advancement.
