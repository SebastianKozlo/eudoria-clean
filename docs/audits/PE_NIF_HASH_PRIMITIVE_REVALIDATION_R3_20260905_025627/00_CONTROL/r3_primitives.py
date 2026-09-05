"""r3_primitives.py — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3 stage-local primitives.

Definitions (explicit, per the R3 prompt items 2-3):

  Adler-32 (RFC 1950 section 2.2):
      s1 = 1, s2 = 0                     (initialization)
      for each byte b:  s1 = (s1 + b) mod 65521 ; s2 = (s2 + s1) mod 65521
      result = (s2 << 16) | s1            (32-bit)
    Independent oracle: zlib.adler32 (C library), plus a closed-form arithmetic
    formulation (numpy, when available) and the corrected Node implementation
    (probe_r2_helpers.cjs, plain Number arithmetic — exact here because every
    intermediate is < 2^53).

  FNV-1a-32 (RFC 9923 / draft-eastlake-fnv):
      h = 0x811C9DC5                      (32-bit offset basis)
      for each byte b:  h = (h XOR b) * 0x01000193 mod 2^32
    The multiply MUST be exact integer arithmetic. Ordinary JavaScript Number
    (float64) multiplication loses integer precision above 2^53 BEFORE the
    32-bit reduction; that is the R2 defect being revalidated. Python int is
    exact; the Node oracle uses BigInt with mod 2^32.

  CRC-32 (IEEE 802.3, = zlib.crc32):
      reflected table-driven, poly 0xEDB88320, init/final 0xFFFFFFFF.
    Independent oracle: zlib.crc32.

Negative-control primitives (R3 prompt item 5) — deliberately WRONG-VALUE
implementations chosen so that the aggregate zero-match property is preserved
(they still never equal d), demonstrating that match-count aggregates alone
cannot detect value errors; only per-value known-answer/oracle identity can:

  adler32_wrong_xor : correct adler XOR 0x5A5A5A5A  (wrong for every input incl. empty)
  fnv1a_wrong_basis : FNV-1a with offset basis 0x811C9DC6 (one byte off)

R2 literal-semantics reimplementations (Python-exact transcription of the two
R2 Node helper declarations, for cross-check only — the ACTUAL hash-pinned R2
source bytes are executed by 00_CONTROL/probe_r2_helpers.cjs; the equivalence
Python-reimplementation == Node-literal-execution is asserted on all KAT
vectors AND on all 11,022 corpus name inputs):

  adler32_r2_literal : let a=1, s=0; per byte: s=(s+b)%65521; a=(a+s)%65521;
                       return (a<<16)|s   — starts the byte sum at 0 and the
                       accumulated sum at 1: roles/initials misassigned vs RFC1950.
  fnv1a_r2_literal   : x=0x811C9DC5; per byte: x=((x^b)*0x01000193)>>>0 — in
                       Node this multiplies in float64 (precision loss above
                       2^53). The Python transcription below uses exact ints
                       and therefore does NOT reproduce the float defect; it is
                       used only to cross-check the Node execution on inputs
                       where the float product happens to stay exact.

Three-state gate serialization (R3 prompt item 7):
  three_state(ok) : None -> PENDING, True -> PASS, False -> FAIL
  bool_coerce(ok) : R2 run_gates.py behavior — bool(ok) — None -> False (FAIL)

NO shared tools, NO R2 files, NO historical scripts are modified by this
module. It is one-time 00_CONTROL code for this run only.
"""
from __future__ import annotations

import zlib

MOD_ADLER = 65521
FNV_OFFSET_32 = 0x811C9DC5
FNV_PRIME_32 = 0x01000193
MASK_32 = 0xFFFFFFFF


# --------------------------------------------------------------------------
# corrected primitives (spec implementations)
# --------------------------------------------------------------------------
def adler32_rfc1950(data: bytes) -> int:
    """Adler-32 per RFC 1950 section 2.2: s1=1, s2=0, mod 65521, (s2<<16)|s1."""
    s1 = 1
    s2 = 0
    for b in data:
        s1 = (s1 + b) % MOD_ADLER
        s2 = (s2 + s1) % MOD_ADLER
    return (s2 << 16) | s1


def adler32_rfc1950_carry(data: bytes, carry: int) -> int:
    """Streaming form: continue a previous adler value (s2<<16|s1) over data."""
    s2 = carry >> 16
    s1 = carry & 0xFFFF
    for b in data:
        s1 = (s1 + b) % MOD_ADLER
        s2 = (s2 + s1) % MOD_ADLER
    return (s2 << 16) | s1


def adler32_closed_form(data) -> int:
    """Closed-form (numpy int64, chunked) — independent arithmetic formulation.

    Per chunk of m bytes with carry-in (s1, s2):
        S      = sum(B_j)
        s1'    = (s1 + S) mod 65521
        s2'    = (s2 + m*s1 + sum_j (m-j+1)*B_j) mod 65521
    (derivation: s2 accumulates s1_after each byte). Chunks of 1e6 bytes keep
    every int64 product far below 2^63 (max weighted sum ~1.3e14 per chunk).
    Exact for payloads of any size.
    """
    import numpy as np

    mv = memoryview(data)
    total = mv.nbytes
    s1 = 1
    s2 = 0
    off = 0
    CHUNK = 1_000_000
    while off < total:
        a = np.frombuffer(mv[off:off + CHUNK], dtype=np.uint8).astype(np.int64)
        m = a.size
        if m == 0:
            break
        s = int(a.sum())
        weights = np.arange(m, 0, -1, dtype=np.int64)  # (m-j+1) for j = 1..m
        s2 = (s2 + m * s1 + int((a * weights).sum())) % MOD_ADLER
        s1 = (s1 + s) % MOD_ADLER
        off += CHUNK
    return (s2 << 16) | s1


def fnv1a_rfc9923(data: bytes) -> int:
    """FNV-1a-32 per RFC 9923: exact-integer multiply mod 2^32."""
    h = FNV_OFFSET_32
    for b in data:
        h = ((h ^ b) * FNV_PRIME_32) & MASK_32
    return h


def fnv1a_rfc9923_carry(data: bytes, carry: int) -> int:
    h = carry
    for b in data:
        h = ((h ^ b) * FNV_PRIME_32) & MASK_32
    return h


def _crc_table():
    tbl = []
    for n in range(256):
        v = n
        for _ in range(8):
            v = (v >> 1) ^ 0xEDB88320 if v & 1 else v >> 1
        tbl.append(v)
    return tbl


_CRC_T = _crc_table()


def crc32_ieee(data: bytes) -> int:
    """Own table-driven CRC-32 (independent of zlib). Matches zlib.crc32."""
    c = 0xFFFFFFFF
    for b in data:
        c = _CRC_T[(c ^ b) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFF


def crc32_ieee_carry(data: bytes, carry: int) -> int:
    c = carry ^ 0xFFFFFFFF
    for b in data:
        c = _CRC_T[(c ^ b) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFF


# --------------------------------------------------------------------------
# R2 literal-semantics transcription (cross-check only; see module docstring)
# --------------------------------------------------------------------------
def adler32_r2_literal(data: bytes) -> int:
    """Exact-int transcription of R2 control_r2.cjs L37 semantics (see docstring)."""
    a = 1
    s = 0
    for b in data:
        s = (s + b) % MOD_ADLER
        a = (a + s) % MOD_ADLER
    return ((a << 16) | s) & MASK_32


def fnv1a_r2_literal_exact(data: bytes) -> int:
    """Exact-int transcription of R2 control_r2.cjs L38 WITHOUT the float defect.

    Only equals the executed Node literal when every float product stayed
    exact (short/aligned inputs). Used to characterize, not to substitute.
    """
    x = 0x811C9DC5
    for b in data:
        x = ((x ^ b) * 0x01000193) & MASK_32
    return x


# --------------------------------------------------------------------------
# deliberately wrong-value negative controls (aggregate-preserving)
# --------------------------------------------------------------------------
def adler32_wrong_xor(data: bytes) -> int:
    """Wrong for every input (empty -> 0x5A5A5A5B != 1); preserves zero-match."""
    return adler32_rfc1950(data) ^ 0x5A5A5A5A


def fnv1a_wrong_basis(data: bytes) -> int:
    """FNV-1a with a one-off offset basis: wrong values, zero-match preserved."""
    h = 0x811C9DC6
    for b in data:
        h = ((h ^ b) * FNV_PRIME_32) & MASK_32
    return h


# --------------------------------------------------------------------------
# three-state gate serialization vs R2 bool coercion
# --------------------------------------------------------------------------
def three_state(ok) -> str:
    if ok is None:
        return 'PENDING'
    return 'PASS' if ok else 'FAIL'


def bool_coerce(ok) -> str:
    """R2 run_gates.py L50 behavior: stores bool(ok) — None becomes False/FAIL."""
    return 'PASS' if bool(ok) else 'FAIL'


# --------------------------------------------------------------------------
# known-answer test vectors (executable BEFORE corpus aggregation)
# expected_* : published constants where PROVENANCE says so; else None and the
# oracle identity (zlib / cross-implementation agreement) is the assertion.
# --------------------------------------------------------------------------
def _h(s: str) -> bytes:
    return bytes.fromhex(s) if s else b''


KAT_VECTORS = [
    # (id, hex, expected_adler, expected_fnv, expected_crc32, provenance)
    ('V01_empty', '', 0x00000001, 0x811C9DC5, 0x00000000,
     'PUBLISHED: adler init=1 (RFC1950 s2.2); fnv offset basis (RFC9923); crc32("")=0 (IEEE)'),
    ('V02_a', '61', 0x00620062, 0xE40C292C, 0xE8B7BE43,
     'PUBLISHED: fnv1a-32("a")=0xE40C292C (RFC9923/draft-eastlake-fnv test vectors); adler/crc via oracle'),
    ('V03_hello', '68656c6c6f', 0x062C0215, 0x4F9F2CAB, 0x3610A686,
     'PUBLISHED: fnv1a-32("hello")=0x4F9F2CAB (R3 prompt + external post-audit counterexample, independently verified here)'),
    ('V04_foobar', '666f6f626172', None, 0xBF9CF968, None,
     'PUBLISHED: fnv1a-32("foobar")=0xBF9CF968 (draft-eastlake-fnv appendix vectors)'),
    ('V05_wikipedia', '57696b697065646961', 0x11E60398, None, None,
     'PUBLISHED: adler32("Wikipedia")=0x11E60398 (published worked example; asserts the zlib oracle itself)'),
    ('V06_123456789', '313233343536373839', 0x091E01DE, 0xBB86B11C, 0xCBF43926,
     'PUBLISHED: crc32("123456789")=0xCBF43926 (canonical IEEE check value; asserts the zlib oracle); adler/fnv cross-implementation'),
    ('V07_name_548296', '3534383239362e6e6966', 0x0CAC02AE, 0x4E2B6736, None,
     'R2-era corpus name vector (external post-audit KAT; values re-derived independently here)'),
    ('V08_zero_byte', '00', None, None, None,
     'binary single zero byte'),
    ('V09_ff_byte', 'ff', None, None, None,
     'binary single high byte'),
    ('V10_range256', ''.join('%02x' % i for i in range(256)), 0xADF67F81, 0x90A458C5, None,
     'binary sweep incl. zero/high bytes (external post-audit KAT; re-derived here)'),
    ('V11_ff4096', 'ff' * 4096, None, None, None,
     'overflow-sensitive: repeated high bytes stress FNV multiply mod 2^32 and adler mod 65521'),
    ('V12_zero4096', '00' * 4096, None, None, None,
     'overflow-sensitive: zero bytes keep FNV XOR-state, forcing pure multiply-chain mod 2^32; adler s2 grows by 1/byte'),
    ('V13_a10', '61' * 10, None, None, None,
     'repeated input: chaining check vs incremental carry-in form'),
    ('V14_incremental_split', '68656c6c6f', None, None, None,
     'incremental: "he"+"llo" two-stage carry must equal one-shot (adler/fnv/crc all streaming)'),
]


def kat_vector_bytes():
    out = []
    for vid, hx, ea, ef, ec, prov in KAT_VECTORS:
        out.append((vid, _h(hx), ea, ef, ec, prov))
    return out


def oracle_values(data: bytes):
    """Independent oracle values: zlib (C) + own table CRC."""
    return {
        'adler_zlib': zlib.adler32(data) & MASK_32,
        'crc32_zlib': zlib.crc32(data) & MASK_32,
        'crc32_own_table': crc32_ieee(data),
    }


def check_published_constants() -> list:
    """Verify the ORACLES' own published vectors (non-circular oracle validation)."""
    results = []
    checks = [
        ('zlib.adler32(b"") == 1 (RFC1950 init)', zlib.adler32(b'') & MASK_32, 0x00000001),
        ('zlib.adler32(b"Wikipedia") == 0x11E60398 (published example)',
         zlib.adler32(b'Wikipedia') & MASK_32, 0x11E60398),
        ('zlib.crc32(b"123456789") == 0xCBF43926 (canonical check value)',
         zlib.crc32(b'123456789') & MASK_32, 0xCBF43926),
        ('zlib.crc32(b"a") == 0xE8B7BE43 (published CRC-32("a"))',
         zlib.crc32(b'a') & MASK_32, 0xE8B7BE43),
        ('fnv exact-int ("" ) == 0x811C9DC5 (RFC9923 offset basis)',
         fnv1a_rfc9923(b''), 0x811C9DC5),
        ('fnv exact-int ("a") == 0xE40C292C (RFC9923 vector)', fnv1a_rfc9923(b'a'), 0xE40C292C),
        ('fnv exact-int ("foobar") == 0xBF9CF968 (draft-eastlake vector)',
         fnv1a_rfc9923(b'foobar'), 0xBF9CF968),
        ('fnv exact-int ("hello") == 0x4F9F2CAB (R3 prompt counterexample)',
         fnv1a_rfc9923(b'hello'), 0x4F9F2CAB),
    ]
    for label, actual, expected in checks:
        results.append({'check': label, 'actual': '%08x' % actual,
                        'expected': '%08x' % expected, 'pass': actual == expected})
    return results


def run_kat(primitive_set: str = 'corrected') -> dict:
    """Executable known-answer suite. primitive_set selects the value source.

    Returns per-vector records; 'all_pass' is False iff any asserted predicate
    fails. Callers translate all_pass into the process exit code (nonzero on
    failure) — see run_kats.py / revalidate_r3.py.
    """
    pick = {
        'corrected': lambda d: (adler32_rfc1950(d), fnv1a_rfc9923(d), crc32_ieee(d)),
        'r2_literal_python': lambda d: (adler32_r2_literal(d), fnv1a_r2_literal_exact(d), crc32_ieee(d)),
        'wrong_value_controls': lambda d: (adler32_wrong_xor(d), fnv1a_wrong_basis(d), crc32_ieee(d)),
    }[primitive_set]

    records = []
    all_pass = True
    for vid, data, ea, ef, ec, prov in kat_vector_bytes():
        mine_a, mine_f, mine_c = pick(data)
        orc = oracle_values(data)
        rec = {
            'vector_id': vid, 'input_len': len(data), 'provenance': prov,
            'adler': {'impl': '%08x' % mine_a, 'zlib_oracle': '%08x' % orc['adler_zlib'],
                      'published': '%08x' % ea if ea is not None else None},
            'fnv': {'impl': '%08x' % mine_f,
                    'published': '%08x' % ef if ef is not None else None},
            'crc32': {'impl': '%08x' % mine_c, 'zlib_oracle': '%08x' % orc['crc32_zlib'],
                      'own_table_oracle': '%08x' % orc['crc32_own_table'],
                      'published': '%08x' % ec if ec is not None else None},
        }
        # asserted predicates (deterministic; any false => all_pass False)
        fails = []
        if primitive_set == 'corrected':
            if mine_a != orc['adler_zlib']:
                fails.append('adler_impl!=zlib')
            if mine_c != orc['crc32_zlib'] or mine_c != orc['crc32_own_table']:
                fails.append('crc_impl!=oracle')
            if ea is not None and mine_a != ea:
                fails.append('adler!=published')
            if ef is not None and mine_f != ef:
                fails.append('fnv!=published')
            if ec is not None and mine_c != ec:
                fails.append('crc!=published')
        else:
            # For control sets the SAME corrected-oracle predicates must be
            # evaluated: a wrong-value implementation must FAIL them.
            if mine_a != orc['adler_zlib']:
                fails.append('adler_impl!=zlib')
            if ea is not None and mine_a != ea:
                fails.append('adler!=published')
            if ef is not None and mine_f != ef:
                fails.append('fnv!=published')
        rec['failed_predicates'] = fails
        if fails:
            all_pass = False
        records.append(rec)

    # incremental/streaming identity (corrected set only)
    incremental = None
    if primitive_set == 'corrected':
        d1, d2 = b'he', b'llo'
        whole = d1 + d2
        inc = {
            'adler_two_stage_vs_oneshot':
                adler32_rfc1950_carry(d2, adler32_rfc1950(d1)) == adler32_rfc1950(whole),
            'adler_zlib_carry_vs_oneshot':
                (zlib.adler32(d2, zlib.adler32(d1)) & MASK_32) == adler32_rfc1950(whole),
            'fnv_two_stage_vs_oneshot':
                fnv1a_rfc9923_carry(d2, fnv1a_rfc9923(d1)) == fnv1a_rfc9923(whole),
            'crc_two_stage_vs_oneshot':
                crc32_ieee_carry(d2, crc32_ieee(d1)) == crc32_ieee(whole),
        }
        incremental = inc
        if not all(inc.values()):
            all_pass = False

    return {'primitive_set': primitive_set, 'all_pass': all_pass,
            'vector_count': len(records), 'vectors': records,
            'incremental_identity': incremental}
