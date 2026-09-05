# SOURCE_QUOTES — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3

Verbatim quotes anchoring every R3 claim to its physical source. Every quote was
verified present in the named artifact (whitespace-normalized match) at emit
time; hashes are recomputed this run. Historical artifacts are READ-ONLY and
were NOT modified.

---

## Q1 — the two defective R2 Node helper declarations (defect evidence, R3C-01/02)

> Source: `D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\00_CONTROL\control_r2.cjs`
> SHA256: `666c378da43dd23b961252bdc091baf9b2c7df6b32268d002ed916b20018b59e` (hash-pin re-verified by R3G3a before extraction)

```js
function adler32(b) { let a = 1, s = 0; for (let i = 0; i < b.length; i++) { s = (s + b[i]) % 65521; a = (a + s) % 65521; } return ((a << 16) | s) >>> 0; }
function fnv1a(b) { let x = 0x811C9DC5; for (let i = 0; i < b.length; i++) x = ((x ^ b[i]) * 0x01000193) >>> 0; return x >>> 0; }
```

WHY: the byte-sum accumulator (`s`) starts at 0 and the accumulated sum (`a`) starts at 1 — the RFC 1950 roles/initials (s1=1, s2=0) are misassigned. The FNV multiply happens in float64 before `>>> 0`.

## Q2 — the R2 crc32 declaration + table (positive control, R3C-03)

> Source: same file, SHA256 as Q1.

```js
function crc32(b) { // standard CRC-32 (IEEE 802.3), matches zlib.crc32
  let c = 0xffffffff;
  for (let i = 0; i < b.length; i++) c = CRC_T[(c ^ b[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
const CRC_T = new Uint32Array(256);
for (let n = 0; n < 256; n++) { let v = n; for (let k = 0; k < 8; k++) v = (v & 1) ? ((v >>> 1) ^ 0xedb88320) : (v >>> 1); CRC_T[n] = v >>> 0; }
```

WHY: executed as a literal this table-driven crc32 equals zlib.crc32 on all 14 KAT vectors and 11,022/11,022 entries per crc32 input class — the defect census is bounded to adler32 + fnv1a.

## Q3 — the R2 Python fnv1a (the correct leg, R3C-08)

> Source: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\00_CONTROL\run_gates.py`
> SHA256: `7688732929b75e926f4fa2a5bf5ca362032d921d24f1d307f883d6e5355bcede`

```python
def fnv1a(b):
    x = 0x811C9DC5
    for byte in b: x = ((x ^ byte) * 0x01000193) & 0xFFFFFFFF
    return x
```

WHY: exact-integer arithmetic — this is why the R2 Python leg produced correct aggregates. The R2 Node leg (Q1) did not. Same formula, different arithmetic: isolates the float64 root cause (R3C-02).

## Q4 — the R2 gate serialization defect (F3, R3C-12)

> Source: same file, SHA256 as Q3.

```python
def gate(gid, name, gtype, measured, denominator, truth, noncirc, failure, fixtures, ok):
    GATES.append({'gate_id': gid, 'gate_name': name, 'gate_type': gtype,
        'measured_quantity': measured, 'denominator': denominator,
        'independent_source_of_truth': truth, 'why_non_circular': noncirc,
        'failure_case_detected': failure, 'fixtures': fixtures, 'pass': bool(ok)})
```

WHY: `'pass': bool(ok)` — HR-1..HR-4 were called with `ok=None` and serialized as `false` (JSON) / `FAIL` (CSV), misrepresenting pending human review as failed review. R2G13's own TEST_RESULTS record shows `"HR-1"... "pass": false`.

> Source: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\02_LOGS\TEST_RESULTS.json`
> SHA256: `a0d5c1249bfad39518999e86b713aae6a39fa6859899db28161fefb7cb9d1b53`

```json
{"gate_id": "HR-1", "gate_name": "Semantic adequacy of the corrected wordings (nine/ten, trailing values, measured-first, evidence-graded)", "gate_type": "HUMAN_REVIEWED", ..., "pass": false}
```

> Source: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\STAGE_ACCEPTANCE_GATES.csv`
> SHA256: `b8f8ca6dea55dd1407e84b5718b5fce4b9bcc090f03953707f94334d807c9f2f`

```csv
HR-1,...,HUMAN_REVIEWED,FAIL,...
```

## Q5 — R2G8's superseded independence assurance (R3C-08, S-04)

> Source: R2 TEST_RESULTS.json, SHA256 as Q4.

```json
"gate_name": "candidate recount: NINE exact-zero + payload-CRC nonzero (Python == Node == R36 historical)",
"why_non_circular": "three independent computations (Node, Python, R36 historical)",
```

WHY: the "Node" leg computed different functions whose zero-match aggregates coincidentally agreed (R3C-06/R3C-09). The physical counts stand (R3C-07); the assurance does not.

## Q6 — R2G13's stale tally label (R3C-13, S-10)

> Source: R2 TEST_RESULTS.json, SHA256 as Q4.

```json
"gate_name": "CLAIM_MATRIX validity: 24 rows, one taxonomy status per row, tally {CONFIRMED 17, REJECTED 7}, real source hashes"
```

WHY: the actual R2 CLAIM_MATRIX.csv rows tally CONFIRMED 16 / REJECTED 8 (recounted by R3G16 from the emitted CSV; SHA256 `6d1e09a38ad20ac57f8baec3aff8977837955ada66221e7867e55ecde9e9617d`).

## Q7 — R2 report method claim (S-05)

> Source: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\06_REPORT\00_FINAL_REPORT.md`
> SHA256: `2aee83b9858a5dffaef864324ec15d3b027433b12c64bc76390bcf159297effd`

```markdown
The TEN named candidates were PHYSICALLY recomputed over both full containers this
run (definitions read from the R36 driver source; Node hand-rolled CRC32/adler32/
FNV-1a cross-checked against Python zlib):
...
- Three-way agreement: R2 Node == R2 Python == R36 historical FIELD_D_TESTS.json
  (20/20 candidate-era pairs, R2G8).
```

WHY: the cross-check was aggregate-only; value-level cross-check fails for adler/fnv (11022/11022 and 11016/11022 per-entry mismatches, R3C-06). Superseded wording in PROPOSED_DOC_CORRECTIONS_R3.md P3R3.

## Q8 — R2 handoff wording (S-08)

> Source: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\HANDOFF.md`
> SHA256: `29f09c97e2be40028c2939ff3aca7ef078d91f1c06c5c542da40a6970bdb7559`

```markdown
2. Candidate wording FIXED: NINE exact-zero on both corpora; d==crc32(payload) =
   3,435/5,596 + 3,299/5,426 (not universal, not zero); three-way agreement
   (Node/Python/R36 historical); ten-exact-zero wording superseded.
```

## Q9 — R2 census aggregates + method note (R3C-07 agreement target, S-03)

> Source: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\01_RAW\RECOUNTS.json`
> SHA256: `19718c95d90d6d314bb2528e0928ffccf120b8f15f57bad15a40fe0cfa026b25`

```json
"method": "PHYSICAL RECOMPUTATION this run over both full containers (Node hand-rolled CRC32/adler32/FNV-1a; candidate definitions read from the R36 driver source field_d_r36.py L110-122,L502-533)",
"name_derived_candidate_matches": { "d == crc32(payload) [== c]": 3435, "d == adler32(payload)": 0, ... "d == fnv1a(name)": 0, "d == size": 0, "d == offset": 0 }
```

WHY: R3's corrected census agrees with these counts 20/20 (R3G11) — the physical result was never in question; only the method provenance is superseded.

## Q10 — R36 historical primitives + counts (the correct historical reference)

> Source: `D:\Eudoria_Reconstruction\99_Audits\PE_NIF_FIELD_D_R36_20260904_171903\01_source\field_d_r36.py`
> SHA256: `3f74804ab264949bd473c6dc33057c68c510f420265c5c71502ea9faf9f8a8a6`
> Results: `...\02_results\FIELD_D_TESTS.json` SHA256: `2af4cd39d36db96a2013a6de75983469aa6e2e7856a40061de6c86c6d54ee043`

```python
def crc32(b):  return zlib.crc32(b) & 0xFFFFFFFF
def adler32(b): return zlib.adler32(b) & 0xFFFFFFFF
def fnv1a(b):
    x = 0x811C9DC5
    for byte in b: x = ((x ^ byte) * 0x01000193) & 0xFFFFFFFF
    return x
```

WHY: the R36 historical leg was CORRECT (zlib + exact-int). Together with the correct R2 Python leg this means the R2 aggregate result was already confirmed by two correct implementations; the R2 Node defect was concealed by zero-match insensitivity.

## Q11 — R34 per-span counterexamples (F2, R3C-10)

> Source: `D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results\REAL_SPARSE_GRAMMAR.json`
> SHA256: `2c26ba86db44ad7a58322c136112fec36e23efab1db1fafea1c976311eba007e` (pin re-verified by R3G12pin)

```json
{"file": "592572.nif", "bi": 65, "si": 45, "has_real": true, "n_wp_inrange": 2, "g1_ok": 0, "g2_ok": 0, "mscan_ok_m": [30], "var_ok": 0, "var_recs": 1}
{"file": "579739.nif", "bi": 109, "si": 138, "has_real": true, "n_wp_inrange": 1, "g1_ok": 0, "g2_ok": 0, "mscan_ok_m": [4], "var_ok": 0}
{"file": "574751.nif", "bi": 80, "si": 4, "has_real": true, "n_wp_inrange": 1, "g1_ok": 0, "g2_ok": 1, "mscan_ok_m": [11], "var_ok": 0}
```

WHY: three concrete members of the 62-span class that have another recorded fit despite var_ok=0 — contradicting "334 real-record spans fit no tested grammar".

## Q12 — R35 claim table rows (F2b, R3C-11)

> Source: `D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CROSS_ERA_R35_20260904_170224\REPORT.md`
> SHA256: `8f7e36c3b0cb2fcdbe26209be99e232bb5bb91ff1755f41d80ca99bb37473aad`

```markdown
| C-MORPH-1 | Real sparse variable-k grammar `[u16 idx][k×f32 Σ=1][9×f32]` | 3,186/6,167 fit spans; rr 2,093/2,427 (86.2%) | **2,061/4,674 fit spans; rr 1,180/1,457 (81.0%)** | **ERA-STABLE** | CONFIRMED (STRONGLY_SUPPORTED per R34 basis) |
...
**Verdict counts: ERA-STABLE 19, EVOLVED 2, ABSENT-in-2003 0, falsification candidates 0.**
```

WHY: C-MORPH-1 is a partial-fit claim and 2 claims are EVOLVED — "all 21 claims at 100%" is not a valid summary of this table.

## Q13 — R2 P1R2-5 / P2R2-2 proposal wording (S-11/S-12 supersession targets)

> Source: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\06_REPORT\PROPOSED_DOC_CORRECTIONS_R2.md`
> SHA256: `90bd092140676519ff125521a952ca10e5338276546c44e7097d203de348902b`

```markdown
byte-exact on 2,093/2,427 classifier-real spans (86.2%; the 'real-record' class is a
hypothesis-aligned classifier) and 3,186/6,167 all fit spans; 334 real-record spans fit
no tested grammar; observed k ∈ {1,2,3,4} on 9.3.5 exact examples and k ∈ {1..5} on 2003.
...
eras), every byte-exact grammar reproduced at 100% and the rare-family and importer
pattern censuses were count-identical.
```

WHY: both statements are the supersession targets of P1R2-5-R3 / P2R2-2-R3 (PROPOSED_DOC_CORRECTIONS_R3.md). Neither R2 nor R3 proposal has been applied.

## Q14 — the external post-audit verdict (input authority for this run)

> Source: `D:\Eudoria_Reconstruction\99_Audits\PE_NIF_R2_POST_AUDIT_20260905_025627\06_REPORT\00_FINAL_REPORT.md`
> SHA256: `8681f754adb0f05f56074b22f7338e7f69a4648cc5241d34a759bfdd66376178`
> Reproducer: `...\00_CONTROL\verify.py` SHA256: `c0fa16fe81717158ffd6c563d7fb58998c136e75af4f7c6c3f55ed264aac1d62`
> Raw verification record: `...\01_RAW\verification.json` SHA256: `6617a8f68442664f3d70e96e7bdc330b2e3e3cc09943f9eaaa18ff202f39d41f`

```markdown
Date: 2026-09-05. Verdict: **REVALIDATION_REQUIRED**.
...
P0 = HASH_PRIMITIVE_VALUE_IDENTITY_BEFORE_AGGREGATE_ACCEPTANCE
...
**F1 — CONFIRMED implementation/validation defect.** R2 `00_CONTROL/control_r2.cjs`
definitions `adler32` and `fnv1a` do not implement their declared algorithms correctly.
...
Nine exact-zero candidate counts = independently CONFIRMED by correct reference.
Node implements the named algorithms correctly = REJECTED.
20/20 matching aggregate counts proves implementation identity = REJECTED.
```

WHY: the authority for this revalidation run. R3 tested its counterexamples against the actual executed bytes (R3G6b) rather than accepting them blindly — all five R2 values and all five corrected values reproduced exactly.

## Q15 — the execution prompt (run charter)

> Source: `D:\Eudoria_Reconstruction\99_Audits\PE_NIF_R2_POST_AUDIT_20260905_025627\00_CONTROL\OPENCODE_REVALIDATION_PROMPT.md`
> SHA256: `662d4c522a570d210549618bfee7d27acbc0253f39034c005c2678bde389d35c` (verified by R3G1)

```markdown
P0 = HASH_PRIMITIVE_VALUE_IDENTITY_BEFORE_AGGREGATE_ACCEPTANCE
...
5. Negative controls MUST fail: unchanged R2 helpers; a deliberately wrong-value
   implementation preserving aggregate zero-match counts; pending-as-false serialization.
...
HARD STOP after this corrected published package and handoff. Wait for independent
revalidation before proposals are applied. No next milestone or unbounded loop.
```

## Q16 — R39 final row raw bytes (F5, R3C-14)

> Sidecar: `...\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\05_ANALYSIS\NORMALIZED_MANIFESTS\PE_NIF_WIKI_AUDIT_R39_20260904_180213.artifact_index.lossless.csv`
> Original manifest: `D:\Eudoria_Reconstruction\99_Audits\PE_NIF_WIKI_AUDIT_R39_20260904_180213\artifact_index.csv`
> SHA256: `6a007dbb7d489a702258807babd3c758ecddbf87fe659160fd17579f0030ffa6`

```text
row 10 raw (hex): 61727469666163745f696e6465782e6373762c3c6e6f74206c69737465643a20612066696c652063616e6e6f7420636f6e7461696e20697473206f776e205348412d3235363e2c302c73656c662d6578636c7573696f6e20646f63756d656e746564202852333120707265636564656e74292c6e2f610d
decoded:         artifact_index.csv,<not listed: a file cannot contain its own SHA-256>,0,self-exclusion documented (R31 precedent),n/a\r
```

WHY: the final field ends with a bare CR (0x0d) INSIDE the row, followed by the recorded CRLF terminator. Under the custom physical-line contract computed_by = "n/a\r" (matches the sidecar mapping exactly); under standard CSV record semantics it parses as "n/a". Both preserve the original bytes — an interpretive difference, not byte loss (R3G14).
