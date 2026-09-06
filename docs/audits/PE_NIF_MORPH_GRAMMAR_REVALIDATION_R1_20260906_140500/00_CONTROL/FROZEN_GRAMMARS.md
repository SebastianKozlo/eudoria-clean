# FROZEN_GRAMMARS.md — VERBATIM grammar freeze (PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500)

Source of every block below: the PINNED K2 driver `00_CONTROL/morph_residual_deepdive_r1.py` of PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209, SHA256 b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a (re-hashed at extraction time).

Line ranges are 1-based inclusive ranges into that exact file. The revalidation driver byte-verifies each block against the pinned source BEFORE any test execution and imports the pinned module for execution, so the executed grammars ARE these frozen definitions.

Standing sentence (applies to this and every artifact of this run): no semantic claims; class -256/field1 MEANING remains unknown; the -256=>zero-entry association remains ONE-WAY. Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / ERA_TRANSFER_DIAGNOSTIC / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

## B1_constants (lines 79-82)

Grammar constants (verbatim; used by every parser below).

```python
WP_TOL = 1e-4
VAR_MAX_K = 8
VAR_NDELTA = 9
MSCAN_MAX = 32
```

## B2_sane (lines 96-97)

sane() — float sanity predicate used by greedy_r18 (H7 join walk).

```python
def sane(v):
    return v == v and (v == 0 or 1e-45 < abs(v) < 1e6)
```

## B3_clean (lines 100-103)

clean() — float cleanliness predicate used by the variable-k parsers.

```python
def clean(v):
    if v != v or abs(v) >= 1e6:
        return False
    return v == 0.0 or abs(v) >= 2.0 ** -126
```

## B4_greedy_r18 (lines 121-144)

greedy_r18(dp, Wm) — the frozen H7 adjacency-join walk predicate (R18 greedy walk, VERBATIM incl. the 2-byte 00 00 tail acceptance).

```python
def greedy_r18(dp, Wm):
    i2 = Wm - 2
    ent = 0
    while i2 < len(dp):
        took = False
        if i2 + 18 <= len(dp):
            idv = struct.unpack_from("<H", dp, i2)[0]
            if idv < 0x8000:
                fl = [struct.unpack_from("<f", dp, i2 + 2 + 4 * k)[0] for k in range(4)]
                if all(sane(v) for v in fl):
                    ent += 1
                    i2 += 18
                    took = True
        if not took and i2 + 4 <= len(dp):
            v = struct.unpack_from("<f", dp, i2)[0]
            if sane(v):
                i2 += 4
                took = True
        if not took:
            if ent > 0 and len(dp) - i2 == 2 and dp[i2:i2 + 2] == b"\x00\x00":
                i2 = len(dp)
                break
            return False
    return ent > 0 and i2 == len(dp)
```

## B5_parse_variable (lines 288-320)

parse_variable(dp, u, N, kmax, ndelta, tol, idx_limit) — the frozen variable-k grammar; H5c2 = this function with idx_limit=0x8000 (H5c idx-relaxed). VERBATIM, no parameter changes.

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

## B6_parse_variable_trunctail (lines 357-396)

parse_variable_trunctail(dp, u, N, kmax, ndelta, tol, max_leftover) — the frozen H5a truncated-tail grammar. VERBATIM, no parameter changes.

```python
def parse_variable_trunctail(dp, u, N, kmax=VAR_MAX_K, ndelta=VAR_NDELTA,
                             tol=WP_TOL, max_leftover=41):
    p = u
    end = len(dp)
    recs = 0
    k_hist = Counter()
    idxs = []
    uf = struct.unpack_from
    while p < end:
        rem = end - p
        if rem < 2:
            if rem <= max_leftover:
                return (True, recs, k_hist, idxs, rem)
            return (False, recs, k_hist, idxs, -1)
        idx = uf("<H", dp, p)[0]
        if idx >= N:
            if rem <= max_leftover:
                return (True, recs, k_hist, idxs, rem)
            return (False, recs, k_hist, idxs, -1)
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
            rem = end - p
            if rem <= max_leftover:
                return (True, recs, k_hist, idxs, rem)
            return (False, recs, k_hist, idxs, -1)
    return (True, recs, k_hist, idxs, 0)
```

## B7_H5a_invocation (lines 1003-1016)

H5a test invocation in K2 (fit condition ok and recs>0 and left>0; negative control nc2 at u+2/u-2). VERBATIM.

```python
    # ---- H5a ----
    h5a_fits = []
    h5a_hist = Counter()
    for r in NF:
        ok, recs, kh, idxs, left = parse_variable_trunctail(r["dp"], r["u"], r["N"])
        if ok and recs > 0 and left > 0:
            h5a_fits.append((span_key(r), left))
            h5a_hist[left] += 1
    h5a_nc = nc2(lambda r, u2: parse_variable_trunctail(r["dp"], u2, r["N"])[:4])
    results["H5a"] = {"fits": [[list(k), l] for k, l in h5a_fits],
                      "leftover_histogram": {str(k): v for k, v in sorted(h5a_hist.items())},
                      "n_fits": len(h5a_fits), "nc": [[list(k), d] for k, d in h5a_nc]}
    log("[r1] H5a: fits=%d hist=%s nc=%d"
        % (len(h5a_fits), dict(h5a_hist), len(h5a_nc)))
```

## B8_H5c_invocation (lines 1035-1052)

H5c test invocation in K2 (H5c2 = idx_limit 0x8000; fit condition ok and recs>0; negative control nc2). VERBATIM.

```python
    # ---- H5c ----
    h5c = {}
    for vid, limmode in (("H5c1_idx_lt_2N", "2N"), ("H5c2_idx_lt_0x8000", "raw")):
        fits_v = []
        for r in NF:
            lim = 2 * r["N"] if limmode == "2N" else 0x8000
            ok, recs, kh, idxs = parse_variable(r["dp"], r["u"], r["N"],
                                                idx_limit=lim)
            if ok and recs > 0:
                fits_v.append((span_key(r), max(idxs) if idxs else 0))
        def _pf(r, u2, limmode=limmode):
            lim = 2 * r["N"] if limmode == "2N" else 0x8000
            return parse_variable(r["dp"], u2, r["N"], idx_limit=lim)
        ncv = nc2(_pf)
        h5c[vid] = {"fits": [[list(k), mx] for k, mx in fits_v], "n_fits": len(fits_v),
                    "n_nc": len(ncv)}
        log("[r1] %s: fits=%d nc=%d" % (vid, len(fits_v), len(ncv)))
    results["H5c"] = h5c
```

## B9_H7_invocation (lines 1152-1171)

H7 prev/next adjacency-join procedure in K2 (H7a: prev dp + current span incl. leading tag; H7b: current dp + next span incl. leading tag; both tested with greedy_r18(dpj, Wm)). VERBATIM.

```python
    # ---- H7 ----
    h7a = []
    h7b = []
    h7c_blocks = []
    h7c_skipped = []
    for r in RU:
        ctx = blocks_ctx.get((r["file"], r["bi"]))
        if ctx is None:
            continue
        spans = ctx["spans"]
        Wm = ctx["Wm"]
        si = r["si"]
        if si > 0:
            dpj = spans[si - 1][2:] + r["s"]
            if greedy_r18(dpj, Wm):
                h7a.append(span_key(r))
        if si + 1 < len(spans):
            dpj = r["dp"] + spans[si + 1]
            if greedy_r18(dpj, Wm):
                h7b.append(span_key(r))
```

## B10_nc2 (lines 871-882)

nc2() — K2 negative-control procedure at pinned wrong starts u+2 and u-2 (the H5a/H5c NC basis of this run). VERBATIM.

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
