#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
QC probe D (PE-MASTER-AUDITOR, INTERNAL_QC):
1. GATE-NC claim "no 296445/4508 constants anywhere in the chain" — scan all
   chain functions for imm32 296445 (0x0004877D), 4508 (0x0000119C), 296446,
   126740, 278453.
2. Manifest re-hash of 10 random artifacts + full-path spot check.
3. E.3 sentinel bss cross-check (VA 0x00BA5800 vs .data raw/virtual end).

READ-ONLY. Writes: 00_CONTROL\qc_probe\qc_D_nc_manifest_result.json
"""
import hashlib
import json
import random
import struct
import sys

EXE = r"D:\Eudoria_Reconstruction\pcg_install\Entropia.exe"
RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912"
IDX = RUN + r"\06_REPORT\artifact_index.csv"
OUT = RUN + r"\00_CONTROL\qc_probe\qc_D_nc_manifest_result.json"

res = {"probe": "qc_D_nc_manifest", "errors": []}

with open(EXE, "rb") as f:
    blob = f.read()
e_lfanew = struct.unpack_from("<I", blob, 0x3C)[0]
coff = e_lfanew + 4
size_opt = struct.unpack_from("<H", blob, coff + 16)[0]
opt = coff + 20
image_base = struct.unpack_from("<I", blob, opt + 28)[0]
sections = []
for i in range(struct.unpack_from("<H", blob, coff + 2)[0]):
    off = opt + size_opt + 40 * i
    name = blob[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", blob, off + 8)
    sections.append((name, vsize, vaddr, rsize, rptr))


def va2off(va):
    rva = va - image_base
    for (n, vs, vd, rs, rp) in sections:
        if vd <= rva < vd + vs and (rva - vd) < rs:
            return rp + (rva - vd)
    return None


# --- 1. constants scan over the chain functions ---
CHAIN = {
    "loader_0072fa30": 0x0072FA30, "vfs_open_00972df0": 0x00972DF0, "indexwalk_00972ad0": 0x00972AD0,
    "stride_00979d00": 0x00979D00, "recread_00971ad0": 0x00971AD0, "crc_004063d0": 0x004063D0,
    "parser_00730c90": 0x00730C90, "ctor_00730700": 0x00730700, "sub1_00730b70": 0x00730B70,
    "sub2_00730970": 0x00730970, "copy_005670a0": 0x005670A0, "insert_0072f8d0": 0x0072F8D0,
    "keyget_004123d0": 0x004123D0, "singleton_0043a550": 0x0043A550, "lookup_0072f580": 0x0072F580,
    "valid_0072fce0": 0x0072FCE0, "getterA_007ce1e0": 0x007CE1E0, "getterB_00746550": 0x00746550,
    "getterC_006b22d0": 0x006B22D0, "pump_006c9700": 0x006C9700, "arm_single_00415670": 0x00415670,
    "dispatcher_00823c10": 0x00823C10, "consumer_006b4c50": 0x006B4C50, "avatarvar_0043eae0": 0x0043EAE0,
    "pairinsert_0043c700": 0x0043C700, "objcreate_006c0d50": 0x006C0D50, "cache_00799930": 0x00799930,
    "bnt2_00967d00": 0x00967D00, "rm_init_0041dae0": 0x0041DAE0,
}
SPAN = 0x2000  # generous per-function window
CONSTS = {296445: "A_4508", 4508: "id_4508", 296446: "B_4508", 126740: "A_4752", 278453: "A_2249"}
scan = {}
for cval, cname in CONSTS.items():
    tb = struct.pack("<I", cval)
    hits = []
    for fname, fva in CHAIN.items():
        off = va2off(fva)
        if off is None:
            continue
        body = blob[off:off + SPAN]
        i = body.find(tb)
        if i >= 0:
            hits.append("%s@%08X" % (fname, fva + i))
    scan["%d(%s)" % (cval, cname)] = hits
res["chain_constants_scan"] = scan
res["chain_constants_verdict"] = {
    "claim": "no 296445/4508-specific constants anywhere in the chain",
    "all_empty": all(len(v) == 0 for v in scan.values()),
}
print("[D] chain constants scan: %r -> all_empty=%s"
      % (scan, res["chain_constants_verdict"]["all_empty"]))
if not res["chain_constants_verdict"]["all_empty"]:
    res["errors"].append("template-specific constants found in chain: %r" % scan)

# --- 2. sentinel bss cross-check (independent recompute) ---
data_sec = [s for s in sections if s[0] == ".data"][0]
raw_end_va = image_base + data_sec[2] + data_sec[4 - 1]  # vaddr + rsize
raw_end_va = image_base + data_sec[2] + data_sec[3]
virt_end_va = image_base + data_sec[2] + data_sec[1]
res["sentinel_bss"] = {
    "data_raw_end_va": "%08X" % raw_end_va, "data_virtual_end_va": "%08X" % virt_end_va,
    "sentinel_0xBA5800_in_bss": raw_end_va <= 0x00BA5800 < virt_end_va,
    "raw_size": data_sec[3], "virtual_size": data_sec[1],
}
print("[D] sentinel bss: raw_end=%08X virt_end=%08X in_bss=%s"
      % (raw_end_va, virt_end_va, res["sentinel_bss"]["sentinel_0xBA5800_in_bss"]))

# --- 3. manifest re-hash of 10 random artifacts ---
with open(IDX, "r", encoding="utf-8") as f:
    lines = [ln.strip() for ln in f if ln.strip()]
header = lines[0]
rows = [ln.split(",") for ln in lines[1:]]
random.seed(20260913)
sample = random.sample(rows, 10)
results = []
for rel, size_s, sha in sample:
    p = RUN + "\\" + rel
    try:
        with open(p, "rb") as fh:
            data = fh.read()
        got_sha = hashlib.sha256(data).hexdigest().upper()
        ok = (got_sha == sha) and (str(len(data)) == size_s)
        results.append({"path": rel, "claim_size": size_s, "actual_size": len(data),
                        "claim_sha": sha, "actual_sha": got_sha, "match": ok})
        print("[%s] %-58s size %s/%s" % ("PASS" if ok else "FAIL", rel, size_s, len(data)))
    except OSError as e:
        results.append({"path": rel, "error": str(e), "match": False})
        print("[FAIL] %-58s ERROR %s" % (rel, e))
res["manifest_rehash"] = results
n_bad = sum(1 for r in results if not r.get("match"))
if n_bad:
    res["errors"].append("%d/10 sampled manifest rows mismatch" % n_bad)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print("\n== D SUMMARY: errors=%d ==" % len(res["errors"]))
for e in res["errors"]:
    print("ERROR: " + e)
sys.exit(1 if res["errors"] else 0)
