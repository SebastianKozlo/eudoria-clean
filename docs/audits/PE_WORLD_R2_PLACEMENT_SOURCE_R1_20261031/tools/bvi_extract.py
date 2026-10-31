#!/usr/bin/env python3
"""RUN Stage C — extract sample .bvi payloads from Volumes.bnt (read-only source).

Writes 01_RAW/samples/<name>.bin (small, local-only) + <name>.hexdump.txt.
Uses the same self-validated index parse as volume_pin.py (re-parsed here).
"""
import os, struct, hashlib

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
SAMPLES = ["506044.bvi", "105624.bvi", "506237.bvi", "584781.bvi"]
OUTDIR = os.path.join(RUN, "01_RAW", "samples")
os.makedirs(OUTDIR, exist_ok=True)

data = open(BNT, "rb").read()
size = len(data)
assert data[-4:] == b"BNT2"
index_start = struct.unpack_from("<I", data, size - 8)[0]
pos = index_start
count = struct.unpack_from("<I", data, pos)[0]
pos += 4
index = {}
for _ in range(count):
    nl = data.index(b"\x0a", pos)
    name = data[pos:nl].decode("ascii")
    pos = nl + 1
    packed, off, c, d = struct.unpack_from("<IIII", data, pos)
    pos += 16
    index[name] = (packed, off, c, d)

manifest = []
for s in SAMPLES:
    packed, off, c, d = index[s]
    payload = data[off:off + packed]
    assert len(payload) == packed
    hexpath = os.path.join(OUTDIR, s + ".hexdump.txt")
    binpath = os.path.join(OUTDIR, s + ".bin")
    with open(binpath, "wb") as fh:
        fh.write(payload)
    with open(hexpath, "w", encoding="utf-8") as fh:
        fh.write(f"# {s} packed={packed} offset={off} index_c={c} index_d={d} "
                 f"sha256={hashlib.sha256(payload).hexdigest()}\n")
        for i in range(0, len(payload), 16):
            chunk = payload[i:i + 16]
            hexs = " ".join(f"{b:02x}" for b in chunk)
            asci = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            fh.write(f"{i:08x}  {hexs:<47}  {asci}\n")
    manifest.append({"name": s, "packed": packed, "offset": off,
                     "c": c, "d": d,
                     "sha256": hashlib.sha256(payload).hexdigest()})
print(manifest)
with open(os.path.join(OUTDIR, "SAMPLE_MANIFEST.json"), "w") as fh:
    import json
    json.dump(manifest, fh, indent=2)
