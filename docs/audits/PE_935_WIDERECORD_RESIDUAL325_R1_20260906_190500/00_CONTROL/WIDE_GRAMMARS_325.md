# WIDE_GRAMMARS_325.md - VERBATIM W1/W3 grammar freeze (PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500)

The W1/W3 definitions are copied VERBATIM from RUN C PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 (its CONTRACT.md sha256 404f73687913a5ee934ce123b6bd9588bc2427dfd7b73b2f217f1b21f6ff5f3e and its driver widerecord_driver_r1.py sha256 b4fa818a7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714 pinned first; both verified in-driver). The frozen grammar blocks below are the PINNED K2 driver `00_CONTROL/morph_residual_deepdive_r1.py` of PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209, SHA256 b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a (re-hashed at freeze time; the K2 manifest is DEFECTIVE and was NOT used as a hash source - every K2 artifact was re-hashed directly from bytes).

Line ranges are 1-based inclusive ranges into that exact file. The driver byte-verifies each block against the pinned source BEFORE any test execution and imports the pinned module for execution, so the executed grammars ARE these frozen definitions. The driver also byte-verifies the W1/W3 definition lines and invocation-semantics items against RUN C's pinned WIDE_GRAMMARS.md (sha256 3079ecabee7b95721668e24e4ff3845c11d76835d651379d81ac7ad2c0b8557e). NO post-hoc variants; any additional probe must be labeled POST-HOC NON-COVERAGE and excluded from all coverage numbers. W2 (RUN C) is NOT part of this run's pre-registered set (this contract tests W1/W3 only); no W2 execution, no W2 claims.

Standing sentence: no semantic claims; the +65 (RUN A) = RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with the family-concentration bounds; the H7 join-mechanism = UNVALIDATED (RUN A) - NO H7-based claims; the residual-325 remains the heterogeneous bucket this run only PROBES. Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

## The pre-registered wide-record grammars (RUN C CONTRACT.md Section 3, VERBATIM; W1 and W3 only this run)

- W1 = the fixed-m mscan unit [u16 idx][32 x f32] (m=32) with the head weight pair, consuming the span from the walk start.
- W3 = W1 with a Wm mis-estimate window (Wm-64..Wm+64, step 4).

## Frozen invocation semantics (RUN C operationalization, VERBATIM; items 1, 3, 4; the 325-specific item 5 replaces RUN C's 269-specific item 5)

1. Walk start u = Wm - 2 (the K2/R34 census convention; dp = s[2:], Wm = the block's most-common span length). W1 executes K2.parse_fixed(dp, u, N, 32) VERBATIM (m = 32 = MSCAN_MAX; the head weight pair fl0+fl1~1.0 within WP_TOL is the parse_fixed head-pair semantics, counted as wp by the frozen unit; the fit predicate is the frozen unit's own: ok and recs > 0 - no additional constraint, no parameter change, no improvement).
3. W3 executes K2.parse_fixed(dp, u + d, N, 32) VERBATIM over the frozen Wm mis-estimate window d in {-64, -60, ..., 0, ..., +60, +64} (Wm' = Wm + d, start u' = Wm' - 2; step 4; 33 positions INCLUDING d=0, so W3 is a superset of W1; scan order ascending from d=-64; the FIRST hitting offset is recorded; no per-span free parameter outside the frozen window). Fit = any window position yields ok and recs > 0.
4. Negative controls (NC_PROCEDURES_325.md): per-span wrong-start trials at u+2 and u-2 (2 trials per span, explicit denominators), the SAME grammar executed at the wrong start; rate-vs-rate comparisons only.
5. The 325 population: the 325 R21-unknown residual 9.3.5 morph keys (the census-verified unknown-325 population: fail greedy walk + r19 + backtrack + shift-scan; 333 R21-unknown MINUS 8 shift-only = 325 EXACT; 56 files; 551564.nif x84) (POPULATION_325.json); 333 - 8 = 325 asserted EXACTLY.

## B1_constants (lines 79-83)

```python
WP_TOL = 1e-4
VAR_MAX_K = 8
VAR_NDELTA = 9
MSCAN_MAX = 32
MSCAN_EXT = 64
```

## B2_H4_WIN (lines 86-86)

```python
H4_WIN = 64
```

## B3_clean (lines 100-103)

```python
def clean(v):
    if v != v or abs(v) >= 1e6:
        return False
    return v == 0.0 or abs(v) >= 2.0 ** -126
```

## B4_parse_fixed (lines 251-285)

```python
def parse_fixed(dp, u, N, m):
    end = len(dp)
    rl = 2 + 4 * m
    if (end - u) % rl != 0 or u < 0:
        return (False, 0, [], 0)
    p = u
    recs = 0
    wp = 0
    idxs = []
    uf = struct.unpack_from
    while p < end:
        idx = uf("<H", dp, p)[0]
        if idx >= N:
            return (False, recs, idxs, wp)
        okfl = True
        fl0 = fl1 = 0.0
        for k in range(m):
            v = uf("<f", dp, p + 2 + 4 * k)[0]
            if not clean(v):
                okfl = False
                break
            if k == 0:
                fl0 = v
            elif k == 1:
                fl1 = v
        if not okfl:
            return (False, recs, idxs, wp)
        if m >= 2 and abs((fl0 + fl1) - 1.0) <= WP_TOL:
            wp += 1
        idxs.append(idx)
        recs += 1
        p += rl
    if p == end:
        return (True, recs, idxs, wp)
    return (False, recs, idxs, wp)
```

## B5_parse_variable (lines 288-320)

```python
def parse_variable(dp, u, N, kmax=VAR_MAX_K, ndelta=VAR_NDELTA, tol=WP_TOL,
                   idx_limit=None):
    p = u
    end = len(dp)
    recs = 0
    k_hist = Counter()
    idxs = []
    uf = struct.unpack_from
    while p < end:
        if p + 2 > end:
            return (False, recs, k_hist, idxs)
        idx = uf("<H", dp, p)[0]
        lim = N if idx_limit is None else idx_limit
        if idx >= lim:
            return (False, recs, k_hist, idxs)
        found = False
        for k in range(1, kmax + 1):
            need = 2 + 4 * (k + ndelta)
            if p + need > end:
                break
            fls = [uf("<f", dp, p + 2 + 4 * q)[0] for q in range(k + ndelta)]
            if not all(clean(v) for v in fls):
                continue
            if abs(sum(fls[:k]) - 1.0) <= tol:
                found = True
                k_hist[k] += 1
                idxs.append(idx)
                recs += 1
                p += need
                break
        if not found:
            return (False, recs, k_hist, idxs)
    return (p == end, recs, k_hist, idxs)
```

## B6_nc2 (lines 871-882)

```python
    def nc2(parsefn):
        """negative control at u+2 and u-2; parsefn(r, u2) -> (ok, recs,...)"""
        hits = []
        for r in NF:
            for d in (2, -2):
                u2 = r["u"] + d
                if u2 < 0:
                    continue
                out = parsefn(r, u2)
                if out[0] and out[1] > 0:
                    hits.append((span_key(r), d))
        return hits
```

