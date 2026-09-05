# GATE_WEAKNESS_ADDENDUM — PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1

RUN_ID = PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203
STATUS = ADDENDUM ONLY (governance record). The completed R3 package
(PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627) is UNMODIFIED by this
run; nothing below edits, rewrites or re-opens any R3 artifact. This addendum
lives in THIS run dir only, per the human-relayed MASTER_PARTIAL_PASS follow-up
review, and records the three gate weaknesses + one minor evidence-hygiene
omission that the follow-up review flagged. Each weakness was re-confirmed in
this run by reading the ACTUAL R3 source code (00_CONTROL\revalidate_r3.py,
SHA256 0998547944a1d729e304947b730162af921921795c7f3eab3240740ccc66d80d per the
R3 artifact_index.csv row for revalidate_r3.py — re-hashed this run, MATCH).

---

## W-1 — R3G6c: empty-CRC-vector coverage label overstates the executed comparison

CODE CONFIRMATION = CONFIRMED (revalidate_r3.py lines 291-298, read this run):

```python
ok_r2crc = all(v['r2_crc32'] == (zlib.crc32(bytes.fromhex(vec[1])) & 0xFFFFFFFF)
               for vec, v in zip(rp.KAT_VECTORS, probe['kat_vectors']) if vec[1])
gate('R3G6c', 'positive control: the R2 crc32 literal is NOT defective (defect census bounded)',
     'R2 crc32 == zlib.crc32 on all %d KAT vectors' % len(probe['kat_vectors']),
     '%d KAT vectors' % len(probe['kat_vectors']), 'zlib.crc32 (C oracle)',
     ...)
```

The predicate `if vec[1]` skips every KAT vector whose payload-hex field is the
empty string. r3_primitives.py KAT_VECTORS has 14 vectors (V01_empty .. V14);
V01_empty carries hex `''`, so the executed comparison covers 13/14 vectors —
while the gate MEASURED label renders "on all %d KAT vectors" %
len(probe['kat_vectors']) = **14**. The label says all-14; the comparison
tested 13.

MATERIALITY = LOW, conclusion NOT invalidated:
- The empty-input R2-crc32 OUTPUT is still recorded (probe_r2_helpers.cjs
  executes the R2 crc32 literal on all 14 vectors including V01_empty and
  writes r2_crc32 per vector into 01_RAW\R2_HELPER_PROBE.json kat_vectors);
  only the R3G6c RE-DERIVATION (literal value vs zlib.crc32 recomputation)
  skips it.
- The per-entry census covers the crc classes on 11,022 non-empty corpus
  inputs (0 mismatches on all five crc32 classes, R3G9/R3G10).
- The PE_MASTER review independently executed the R2-crc32 literal vs zlib on
  the KAT set and reported 0/14 mismatches (PE_MASTER_REVIEW.md claim 3).
- crc32("") == 0 is the trivial IEEE value; a defect expressible only on the
  empty input would not affect any corpus aggregate (all names/payloads are
  non-empty).
CORRECT COVERAGE LABEL (for any future restatement): "R2 crc32 == zlib.crc32
on 13/14 KAT vectors (the empty-payload vector V01_empty is skipped by the
`if vec[1]` predicate; its R2-literal output is recorded in
R2_HELPER_PROBE.json but not re-derived in this gate)".

---

## W-2 — R3G10: the PASS predicate enforces less than the gate emits

CODE CONFIRMATION = CONFIRMED (revalidate_r3.py lines 508-522, read this run):

```python
ok_census = (r2_vs['adler32(name)']['mismatches'] == DEN
             and r2_vs['adler32(name)']['r2_node_matches_corrected'] == 0
             and all(r2_vs[c]['mismatches'] == 0 for c in
                     ['crc32(name)', 'crc32(name+0x0A)', 'crc32(name+u32size_le)',
                      'crc32(u32size_le+name)', 'crc32(payload)']))
gate('R3G10', 'R2-vs-corrected per-entry value comparison recorded (complete mismatch census)',
     'adler32(name) %d/%d mismatches; adler32(payload) %d/%d; fnv1a(name) %d/%d mismatches '
     '(%d coincidences); all five crc32 candidates 0 mismatches (R2 crc32 correct)'
     % (...), ..., 'PHYSICAL_RECOMPUTATION', ok_census)
```

The gate EMITS the full mismatch census — adler32(name) 11,022/11,022,
adler32(payload) 11,022/11,022, fnv1a(name) 11,016/11,022 with exactly 6
coincidences, five crc32 classes 0 — but the PASS predicate `ok_census` forces
only: (a) adler32(name) full-mismatch with 0 matches, and (b) the five crc32
classes at 0 mismatches. The adler32(payload) and fnv1a(name) numbers are NOT
in the predicate: a hypothetical run in which the R2 adler-payload or FNV
helper happened to be correct (0 mismatches) would still PASS R3G10 while the
emitted measured text displayed the anomaly.

MATERIALITY = LOW for the R3 conclusions, REAL for gate design:
- The values are recorded per entry in 01_RAW\PRIMITIVE_VALUE_COMPARISON.json
  (r2_vs_corrected block) and were independently re-derived at census level by
  the PE_MASTER review (claim 6: 11022/11022/11016 + exactly 6 coincidences).
- The defects are independently established by R3G6b (KAT counterexample
  reproduction, exit-forcing) and R3G11; R3G10 is a RECORDING gate, and its
  name ("...recorded") is technically accurate — but the emitted full numbers
  alongside a weaker predicate read as enforcement the predicate does not
  deliver.
GATE-DESIGN NOTE for future runs: either extend the predicate
(adler32(payload) mismatches == DEN; fnv1a(name) mismatches == expected with
expected coincidences) or label the gate explicitly as record-only.

---

## W-3 — "four independent implementations per defect-affected class": implementation-count overstatement

CODE CONFIRMATION = CONFIRMED (revalidate_r3.py lines 431-476 + r3_primitives.py
lines 70-203 + probe_r2_helpers.cjs lines 71-84, read this run).

The R3G9 independence_method field asserts: "four independent implementations
per defect-affected input class; none shares code with another". The ACTUAL
per-class implementation counts in the per-entry identity pass
(revalidate_r3.py:436-448) are:

| defect-affected class | full-corpus implementations (per entry, 11,022) | sample-only leg |
|---|---|---|
| fnv1a(name) | **2**: own exact-int fnv1a_rfc9923 == Node BigInt fnvCorrected | — |
| adler32(name) | **3**: zlib C == own adler32_rfc1950 (iterative) == Node adlerCorrected | — |
| adler32(payload) | **3**: zlib C == numpy closed-form adler32_closed_form == Node adlerCorrected | + iterative-spec adler32_rfc1950 leg on the bounded sample (6,335 entries / 247,004,079 B; sizes <= 32 KiB + top-50 + every 97th) |
| crc32 classes (NOT defect-affected) | 2-3: zlib == own table (name) / zlib == R2 Node literal | + own-table payload sample leg |

NO defect-affected class has four full per-entry implementations; full FNV has
2, full Adler has 3, plus the iterative payload leg on a sample. The claim is
overstated as a count. (A defensible reading — 3 full + 1 sample leg = 4 LEGS
for adler32(payload) only — still fails for fnv1a(name) and adler32(name).)

OCCURRENCES OF THE CLAIM IN THE R3 PACKAGE (census, this run — 6 sites, two
phrasings):
1. 00_CONTROL\revalidate_r3.py:474 — "four independent implementations per
   defect-affected input class; none shares code with another"
2. 02_LOGS\TEST_RESULTS.json:217 — same phrasing (R3G9 why_non_circular)
3. STAGE_ACCEPTANCE_GATES.csv:16 (R3G9 row) — same phrasing
4. 00_CONTROL\emit_r3_analysis.py:113 — "four independent implementations per
   defect-affected class (zlib C, numpy closed form, Node Number/BigInt, own
   table/iterative)"
5. 05_ANALYSIS\CLAIM_MATRIX.csv:6 (R3C-05) — same parenthesized phrasing
6. HANDOFF.md:64 — "(four independent implementations per input class)"

MATERIALITY = LOW — the R3G9 IDENTITY RESULT (11,022/11,022 per class) is NOT
invalidated: every class has >= 2 independent implementations with no shared
code, the defect classes (adler) have 3 full implementations, and FNV's
2-implementation per-entry agreement is additionally anchored by four
published RFC/draft vectors at KAT level (V01/V02/V03/V04 expected_fnv) plus
the wrong-basis negative control. The overstatement is in the independence
LABEL, not in the measurement or the per-class evidence.
CORRECTED WORDING (for any future restatement): "per-class independent
implementations: fnv1a(name) 2 (exact-int, Node BigInt) + published vectors at
KAT level; adler32(name) 3 (zlib, own iterative, Node); adler32(payload) 3
full (zlib, numpy closed form, Node) + an iterative-spec sample leg
(6,335/11,022 entries); crc32: zlib + own table (+ R2 literal as the
defect-census bound); none shares code with another."

---

## W-4 (minor, evidence hygiene) — STAGE_ACCEPTANCE_GATES.csv omitted from the R3 artifact_index.csv

CONFIRMED this run by manifest read + row count: the R3 artifact_index.csv
carries 33 artifact rows (32 published + 1 LOCAL_ONLY census-full) and does
NOT list the run root's STAGE_ACCEPTANCE_GATES.csv (29 lines incl. header — a
PUBLISHED gate ledger, per the R3 REPORT and HANDOFF). The manifest's own
self-exclusion (artifact_index.csv is not a row in itself) is documented
precedent; the gates CSV is a different case: it is a published artifact and
should have been indexed. First flagged by the PE_MASTER review
(PE_MASTER_REVIEW.md CODE_FINDINGS [MINOR/EVIDENCE-HYGIENE]); no material
effect — the gates were independently verified against TEST_RESULTS.json
(zgodne). This run's own artifact_index.csv indexes its STAGE_ACCEPTANCE_GATES.csv.

---

## Aggregate assessment

- None of W-1..W-4 invalidates an R3 technical conclusion: each affected
  number was independently re-derived (PE_MASTER review claims 3/5/6) or is a
  label/predicate weakness with the underlying values recorded and verified.
  The R3 verdict (technical package ACCEPTED) stands.
- All four are GATE-DESIGN / LABEL-FIDELITY findings. Future gate suites
  should: (1) make coverage labels state the exact executed population
  (W-1); (2) make PASS predicates enforce everything the measured text emits
  (W-2); (3) state per-class implementation counts, not a single minimum
  inflated to a uniform claim (W-3); (4) index every published artifact in
  the manifest, excluding only the manifest itself, with the exclusion
  documented (W-4 — this run's manifest follows that rule).
- HARD BOUNDARY honored: the R3 package (and every historical run) is
  byte-unmodified; this addendum is the only record of these findings in this
  run dir.
