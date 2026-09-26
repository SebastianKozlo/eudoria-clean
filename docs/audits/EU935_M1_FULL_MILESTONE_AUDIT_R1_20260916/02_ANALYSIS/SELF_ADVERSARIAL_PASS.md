# SELF-ADVERSARIAL PASS - EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916

PE-MASTER's five most load-bearing claims, each with CLAIM | FALSIFIER |
COUNTERCHECK | RESULT | IMPACT. Persisted verbatim (formatted; no content
changes).

## 1. Height decode chain

- CLAIM: the height decode chain (TDF u16 -> engine decode -> heights) is
  era-labeled CONFIRMED.
- FALSIFIER: an engine decode mismatch on a sampled tile.
- COUNTERCHECK: 9216/9216 sample identity vs the frozen r169 oracle + 9/9
  byte-faithful vs an independent parser + the full-map SHA reproduction +
  PE-MASTER land recomputation 79.60605005374798% exact.
- RESULT: stands (CONFIRMED, era-labeled).
- IMPACT: row 1.

## 2. Foliage RNG / scale byte-locks

- CLAIM: the foliage RNG/scale arithmetic is byte-locked and bit-exact.
- FALSIFIER: a byte mismatch at _DAT_00a7d7a8 / _DAT_00a8c758 /
  _DAT_00a980d0 or the FSTP points.
- COUNTERCHECK: the bytes re-read (00 00 00 00 C0 FF DF 40 / E0 FF EF 40),
  463,141 platform samples, the exhaustive domain proofs, the PC24 sensitivity
  measured on both domains.
- RESULT: stands CONDITIONAL on the x87 CW (honestly labeled).
- IMPACT: rows 10-11.

## 3. Terrain_14 blend semantics

- CLAIM: the Terrain_14 blend model is the era-9.3.5 engine semantics.
- FALSIFIER: shader/model divergence from the shipped .fx/binary.
- COUNTERCHECK: the HLSL byte-extracted SHA-pinned, the producer decompile +
  disasm pin, the thresholds byte-match the palette alpha values (the double
  data-side confirmation), 13 fail-closed mutation controls.
- RESULT: stands (era 9.3.5; the 2003 divergent blend recorded).
- IMPACT: row 6.

## 4. World datum (+50.0, height field)

- CLAIM: the world datum (+50.0 slot, the height-field frame) is byte-locked.
- FALSIFIER: byte divergence at 0x00A81D20 / the 2 sites, or a datum
  misread.
- COUNTERCHECK: PE-MASTER byte-locks twice (run + review session) + this
  audit's EXE SHA re-hash E7785430 MATCH + the land reproduction + the
  filename-xy census.
- RESULT: stands at world-datum level (the PARTIAL verdict honest).
- IMPACT: rows 3/14.

## 5. Foliage historical placement (the overclaim trap)

- CLAIM: (negative check) no standing document overclaims historical
  placement.
- FALSIFIER: any doc claiming 1:1 historical placement.
- COUNTERCHECK: census of standing docs - the V4 rows carry
  RECONSTRUCTION-ONLY labels.
- RESULT: no overclaim found (the negative verified).
- IMPACT: row 10 + the downstream contract.

## ALSO RECORDED

- Era discipline verified (PCG/JUL/CD/EU_LATER labeled; the different-era
  Entropia.exe 8,445,952 documented against misuse).
- BLOCKED not waived (the x87/cellstream exhaustive negatives inspected).
- No retracted claim feeds the conclusions (the retraction ledger verified -
  01_RAW/RETRACTION_SUPERSESSION_LEDGER.csv).
- Implementation success not masquerading as semantics (the self-regression
  vs original-client parity distinction maintained).
- Witness/falsification executed by RUN-C/RUN-E with PE-MASTER re-execution
  (6/6; 5/6 predictions exact + F-1).
