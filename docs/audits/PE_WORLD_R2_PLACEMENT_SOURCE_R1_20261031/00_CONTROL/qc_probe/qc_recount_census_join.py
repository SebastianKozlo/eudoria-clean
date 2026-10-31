#!/usr/bin/env python3
"""QC recount script — pe-master-auditor INTERNAL_QC of
PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031 (2026-10-31).

INDEPENDENT re-derivation of the run's load-bearing counters directly from
Volumes.bnt / Models.bnt bytes. Not derived from the executor's tools; written
from the BNT2 trailer convention independently. Read-only on pcg_install.
Outputs summarized in QC_RECOUNT_OUTPUT.txt.
"""
import struct, hashlib

BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
MODELS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"


def bnt2_index(path):
    data = open(path, "rb").read()
    n = len(data)
    assert data[-4:] == b"BNT2"
    idx = struct.unpack_from("<I", data, n - 8)[0]
    pos = idx
    cnt = struct.unpack_from("<I", data, pos)[0]
    pos += 4
    entries = []
    for _ in range(cnt):
        nl = data.index(b"\x0a", pos)
        name = data[pos:nl].decode("ascii")
        pos = nl + 1
        packed, off, c, d = struct.unpack_from("<IIII", data, pos)
        pos += 16
        entries.append((name, packed, off))
    assert pos == n - 8, "roundtrip failed"
    return data, entries


vdata, vent = bnt2_index(BNT)
print("Volumes size", len(vdata), "sha", hashlib.sha256(vdata).hexdigest())
print("count", len(vent), "all_bvi", all(e[0].endswith(".bvi") for e in vent),
      "distinct", len(set(e[0] for e in vent)))

t0 = t0ok = t1 = t1ok = other = recs = 0
for name, packed, off in vent:
    h = vdata[off:off + 4]
    if h[0] == 0 and h[1] == 0:
        k = struct.unpack_from("<H", vdata, off + 2)[0]
        t0 += 1
        recs += k
        if 4 + k * 36 == packed:
            t0ok += 1
    elif h == b"\x01\x00\x00\x00":
        t1 += 1
        if packed >= 12:
            vc = struct.unpack_from("<I", vdata, off + 8)[0]
            if 12 + vc * 12 + 4 <= packed:
                t1ok += 1
    else:
        other += 1
print("census type0", t0, "ok", t0ok, "| type1", t1, "ok", t1ok,
      "| other", other, "| records", recs)

mdata, ment = bnt2_index(MODELS)
print("models entries", len(ment), "dups", len(ment) - len(set(e[0] for e in ment)))
nif = set()
for nm, _, _ in ment:
    if nm.endswith(".nif"):
        try:
            nif.add(int(nm[:-4]))
        except ValueError:
            pass
print("nif ids", len(nif))

ex = m1 = p1 = nj = both = 0
for name, _, _ in vent:
    i = int(name[:-4])
    a = i in nif
    b = (i - 1) in nif
    c = (i + 1) in nif
    if b and c:
        both += 1
    if a:
        ex += 1
    elif b:
        m1 += 1
    elif c:
        p1 += 1
    else:
        nj += 1
print("join exact", ex, "minus1", m1, "plus1", p1, "not_joined", nj,
      "sum", ex + m1 + p1 + nj, "overlap(-1&+1)", both)

# field-level join on the 3 type0 samples
tot = u32h = u16h = 0
hits = []
for s in ["506044.bvi", "105624.bvi", "506237.bvi"]:
    d = {e[0]: (e[1], e[2]) for e in vent}
    packed, off = d[s]
    p = vdata[off:off + packed]
    k = struct.unpack_from("<H", p, 2)[0]
    for i in range(k):
        vals = struct.unpack_from("<9f", p, 4 + i * 36)
        for fi, v in enumerate(vals):
            tot += 1
            b = struct.pack("<f", v)
            u32 = struct.unpack("<I", b)[0]
            u16a, u16b = struct.unpack("<HH", b)
            if u32 in nif:
                u32h += 1
                hits.append(("u32", s, i, fi, u32))
            for u16 in (u16a, u16b):
                if u16 in nif:
                    u16h += 1
                    hits.append(("u16", s, i, fi, u16))
print("fields", tot, "u32 hits", u32h, "u16 hits", u16h, hits)

# full-corpus f1-f6 span measurement (world-frame clustering check)
spans = []
for name, packed, off in vent:
    h = vdata[off:off + 4]
    if h[0] == 0 and h[1] == 0:
        k = struct.unpack_from("<H", vdata, off + 2)[0]
        if k == 0 or 4 + k * 36 != packed:
            continue
        vs = []
        for i in range(k):
            f = struct.unpack_from("<9f", vdata, off + 4 + i * 36)
            vs.extend(f[0:6])
        spans.append((name, min(vs), max(vs), max(vs) - min(vs)))
spans.sort(key=lambda x: -x[3])
print("span files", len(spans), "widest", spans[0], "narrowest", spans[-1])
print("span>524287:", sum(1 for s in spans if s[3] > 524287))
