#!/usr/bin/env python3
"""The +50.0 semantic direction — the caller-of-caller byte analysis (read-only).
Known: the slot-fill callers at 0x9482E9 / 0x94839A / 0x949181 call the packer
FUN_00991a20 with {value(+50.0 via FADD qword [0x00A81D20]), format 50.0f @0x00A7AFA8}.
Goal: (1) find the FUNCTION containing each call site (scan back for the prologue);
(2) census the CALL sites into those functions; (3) decode the value source feeding
the FADD (where does the pre-+50.0 value come from?)."""
import json
import struct

EXE = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\sandbox\wd\Entropia.exe"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIGHT_AGGREGATE_20260905_160000\PLUS50_CALLER_ANALYSIS.json"

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
t = pe + 24 + opt
for i in range(nsec):
    name = d[t:t + 8].rstrip(b"\x00").decode()
    vsize, va, rsize, raw = struct.unpack_from("<IIII", d, t + 8)
    secs.append((name, va, vsize, raw, rsize))
    t += 40
TEXT = next(s for s in secs if s[0] == ".text")
TVA, TRAW, TSZ = TEXT[1], TEXT[3], min(TEXT[2], TEXT[4])


def va2off(va):
    rva = va - 0x400000
    for name, sva, vsz, raw, rsz in secs:
        if sva <= rva < sva + vsz:
            return raw + (rva - sva)
    return None


def off2va(off):
    for name, sva, vsz, raw, rsz in secs:
        if raw <= off < raw + rsz:
            return 0x400000 + sva + (off - raw)
    return None


def find_function_start(call_va):
    """Scan back from the call site for the CC padding + prologue boundary."""
    off = va2off(call_va)
    # walk back until we find CC CC followed by a prologue-ish sequence
    i = off
    while i > TRAW:
        if d[i - 1] == 0xCC and d[i] != 0xCC:
            # candidate function start at i (first byte after CC padding)
            cand = d[i:i + 6]
            if (cand[:3] in (b"\x55\x8b\xec", b"\x8b\xff\x55")) or \
               (cand[:1] in (b"\x53", b"\x56", b"\x57", b"\x83", b"\x81", b"\xa1", b"\x6a")) or \
               cand[:2] in (b"\x8b", b"\xe9", b"\xeb"):
                return off2va(i)
        i -= 1
    return None


sites = [0x009482E9, 0x0094839A, 0x00949181]
funcs = {}
for s in sites:
    fs = find_function_start(s)
    funcs[hex(s)] = hex(fs) if fs else None
    print(f"call site {s:#x} -> function start {fs and hex(fs)}")

# census: all CALL/E8 sites targeting each function start
all_calls = {}
for fs in {v for v in funcs.values() if v}:
    hits = []
    for i in range(TRAW, TRAW + TSZ - 5):
        if d[i] == 0xE8:
            rel = struct.unpack_from("<i", d, i + 1)[0]
            src = off2va(i)
            if src and src + 5 + rel == int(fs, 16):
                hits.append(src)
    all_calls[fs] = hits
    print(f"function {fs}: {len(hits)} call sites: " + " ".join(hex(h) for h in hits[:12]))

# decode the context around the FADD in each slot-fill caller region: which register/
# value feeds it — dump the 160 bytes BEFORE the first packer call site per function
ctx = {}
for s in sites[:1] + sites[1:2]:
    off = va2off(s)
    ctx[hex(s)] = d[off - 160:off + 5].hex()

out = {"functions": funcs, "inbound_calls": {k: [hex(h) for h in v] for k, v in all_calls.items()},
       "caller_context": ctx}
with open(OUT, "w") as f:
    json.dump(out, f, indent=2)
print("\nwritten:", OUT)
