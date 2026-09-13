#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
QC probe B (PE-MASTER-AUDITOR, INTERNAL_QC) for PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912.

1. OWN full walk of templates.vfs per the claimed stride rule
   stride = ceil((16+size)/base)*base, base = u32@0x08; own CRC-32 implementation
   (own 0xEDB88320 table, NOT zlib) — full census recompute vs S2_TRUE_WALK_RESULT.json.
2. Target records 4508/4752/2249 field verification (id/A/B/C/PARAM@+0x20 vs contract).
3. PROMPT_DELTA_1 (PARAM@+0x20 not +0x24; counters pair @+0x24) and
   PROMPT_DELTA_2 (sibling starts 97,288/93,976) byte measurement.
4. Negative control: 1-byte payload flip -> CRC discriminator.
5. Data-binding byte scans: Models.bnt / Volumes.bnt name existence + negatives.

READ-ONLY on all inputs. Writes: 00_CONTROL\qc_probe\qc_B_walk_databinding_result.json
"""
import hashlib
import json
import struct
import sys

VFS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs"
MODELS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
VOLUMES = r"D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt"
OUT = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\00_CONTROL\qc_probe\qc_B_walk_databinding_result.json"
S2_JSON = r"D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\01_RAW\S2_TRUE_WALK_RESULT.json"

res = {"probe": "qc_B_walk_databinding", "errors": []}

# ------------------------------------------------------------------ own CRC-32
def make_table():
    tbl = []
    for i in range(256):
        c = i
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if c & 1 else c >> 1
        tbl.append(c)
    return tbl


TBL = make_table()


def crc32_own(data):
    crc = 0xFFFFFFFF
    for b in data:
        crc = (crc >> 8) ^ TBL[(crc ^ b) & 0xFF]
    return crc ^ 0xFFFFFFFF


# self-test of the implementation against known values
assert crc32_own(b"123456789") == 0xCBF43926, "CRC-32 self-test failed"
res["crc32_selftest"] = "PASS (123456789 -> CBF43926)"

with open(VFS, "rb") as f:
    vfs = f.read()
res["vfs_size"] = len(vfs)
res["vfs_sha256"] = hashlib.sha256(vfs).hexdigest().upper()
res["vfs_magic"] = vfs[:8].decode("ascii", "replace")
u32_08, u32_0c = struct.unpack_from("<II", vfs, 8)
res["hdr_u32_08_base"] = u32_08
res["hdr_u32_0c"] = u32_0c
assert vfs[:8] == b"ArkVFS02", "magic"
assert u32_08 == 36, "base=36"

# ------------------------------------------------------------------ own walk
base = u32_08
pos = 16
n = 0
records = []
crc_fail = []
size_census = {}
d_nonzero = e_nonzero = de_both = f_nonzero = id_ne_id2 = tail_nonzero = 0
stop_reason = None
while pos + 16 <= len(vfs):
    bid, bsize, bver, bcrc = struct.unpack_from("<IIII", vfs, pos)
    if bver != 1:
        stop_reason = "ver!=1 at %d" % pos
        break
    if pos + 16 + bsize > len(vfs):
        stop_reason = "truncated at %d" % pos
        break
    payload = vfs[pos + 16: pos + 16 + bsize]
    calc = crc32_own(payload)
    ok = (calc == bcrc)
    if not ok:
        crc_fail.append({"offset": pos, "id": bid, "field": "%08X" % bcrc, "calc": "%08X" % calc})
    stride = -(-(16 + bsize) // base) * base  # ceil
    rec = {"i": n, "off": pos, "id": bid, "size": bsize, "ver": bver,
           "crcf": "%08X" % bcrc, "ok": ok, "stride": stride}
    if bsize >= 28:
        id2, A, B, C = struct.unpack_from("<IIII", vfs, pos + 16)
        Df = struct.unpack_from("<f", vfs, pos + 0x20)[0]
        Ef = struct.unpack_from("<f", vfs, pos + 0x24)[0]
        Fv = struct.unpack_from("<I", vfs, pos + 0x28)[0]
        rec.update({"id2": id2, "A": A, "B": B, "C": C, "D": Df, "E": Ef, "F": Fv})
        if id2 != bid:
            id_ne_id2 += 1
        if Df != 0.0:
            d_nonzero += 1
        if Ef != 0.0:
            e_nonzero += 1
        if Df != 0.0 and Ef != 0.0:
            de_both += 1
        if Fv != 0:
            f_nonzero += 1
    size_census[bsize] = size_census.get(bsize, 0) + 1
    tail = vfs[pos + 16 + bsize: pos + stride]
    if any(t != 0 for t in tail):
        tail_nonzero += 1
    records.append(rec)
    pos += stride
    n += 1
if stop_reason is None:
    stop_reason = "EOF"

res["walk"] = {
    "record_count": len(records), "stop_reason": stop_reason, "stop_offset": pos,
    "crc_fail_count": len(crc_fail), "crc_fail_first5": crc_fail[:5],
    "D_nonzero": d_nonzero, "E_nonzero": e_nonzero, "DE_both": de_both,
    "F_nonzero": f_nonzero, "id_ne_id2": id_ne_id2, "tail_nonzero": tail_nonzero,
    "last_record_end": records[-1]["off"] + records[-1]["stride"] if records else None,
    "undocumented_bytes": len(vfs) - (records[-1]["off"] + records[-1]["stride"]) if records else None,
    "size_census": {str(k): v for k, v in sorted(size_census.items())},
}
print("[B] own walk: %d records, stop=%s, crc_fail=%d, last_end=%s, undocumented=%s"
      % (len(records), stop_reason, len(crc_fail), res["walk"]["last_record_end"], res["walk"]["undocumented_bytes"]))

# ------------------------------------------------------------------ targets
def find_target(rid):
    for r in records:
        if r["id"] == rid and r["size"] >= 28:
            return r
    return None


targets = {}
for rid in (4508, 4752, 2249):
    r = find_target(rid)
    if r is None:
        res["errors"].append("target %d not found in own walk" % rid)
        continue
    targets[str(rid)] = {
        "file_offset": r["off"], "index": r["i"], "size": r["size"], "ver": r["ver"],
        "crc32_field": r["crcf"], "crc_ok": r["ok"],
        "id2": r["id2"], "A": r["A"], "B": r["B"], "C": r["C"],
        "D_f32_0x20": r["D"], "E_f32_0x24": r["E"], "F_u32_0x28": r["F"],
    }
    print("[B] target %d @%d: A=%s B=%s crc=%s(%s) D=%.6f E=%.6f"
          % (rid, r["off"], r["A"], r["B"], r["crcf"], "OK" if r["ok"] else "FAIL", r["D"], r["E"]))
res["targets"] = targets

# exact byte checks for record 4752 (PROMPT_DELTA_2) and 4508 (PROMPT_DELTA_1)
r4752 = targets.get("4752")
if r4752:
    off = r4752["file_offset"]
    raw16 = vfs[off:off + 16]
    got_id, got_size, got_ver, got_crc = struct.unpack("<IIII", raw16)
    A_raw = struct.unpack_from("<I", vfs, off + 0x14)[0]
    B_raw = struct.unpack_from("<I", vfs, off + 0x18)[0]
    D_raw = struct.unpack_from("<f", vfs, off + 0x20)[0]
    cnt_pair = struct.unpack_from("<HH", vfs, off + 0x24)
    res["prompt_delta_2_4752"] = {
        "offset_measured": off,
        "claim": 97288,
        "id": got_id, "id_expect": 4752,
        "size": got_size, "ver": got_ver, "crc_field": "%08X" % got_crc,
        "A@+0x14": A_raw, "A_expect": 126740,
        "B@+0x18": B_raw, "B_expect": 126741,
        "PARAM_f32@+0x20": D_raw, "PARAM_expect": 111.80599975585938,
        "counters_pair@+0x24": {"u16_str": cnt_pair[0], "u16_u32": cnt_pair[1]},
        "result": "PASS" if (off == 97288 and got_id == 4752 and A_raw == 126740 and B_raw == 126741
                             and abs(D_raw - 111.80599975585938) < 1e-4) else "FAIL",
    }
    if res["prompt_delta_2_4752"]["result"] != "PASS":
        res["errors"].append("PROMPT_DELTA_2 record 4752 mismatch: %r" % res["prompt_delta_2_4752"])
    print("[B] PROMPT_DELTA_2 (4752): offset=%d id=%d A=%d B=%d PARAM=%.6f counters=%r -> %s"
          % (off, got_id, A_raw, B_raw, D_raw, cnt_pair, res["prompt_delta_2_4752"]["result"]))

r2249 = targets.get("2249")
if r2249:
    res["prompt_delta_2_2249"] = {"offset_measured": r2249["file_offset"], "claim": 93976,
                                  "result": "PASS" if r2249["file_offset"] == 93976 else "FAIL"}
    if res["prompt_delta_2_2249"]["result"] != "PASS":
        res["errors"].append("2249 offset mismatch: %d" % r2249["file_offset"])
    print("[B] PROMPT_DELTA_2 (2249): offset=%d -> %s"
          % (r2249["file_offset"], res["prompt_delta_2_2249"]["result"]))

# PROMPT_DELTA_1 for 4508: PARAM bytes at +0x20 vs +0x24
r4508 = targets.get("4508")
if r4508:
    off = r4508["file_offset"]
    d_bytes = vfs[off + 0x20: off + 0x24].hex()
    e_bytes = vfs[off + 0x24: off + 0x28].hex()
    res["prompt_delta_1_4508"] = {
        "offset": off, "D@+0x20_bytes": d_bytes, "D_expect_cb_e1_f9_42": True if d_bytes == "cbe1f942" else False,
        "D_value": struct.unpack_from("<f", vfs, off + 0x20)[0],
        "E@+0x24_bytes": e_bytes, "E_value": struct.unpack_from("<f", vfs, off + 0x24)[0],
        "A@+0x14": struct.unpack_from("<I", vfs, off + 0x14)[0],
        "B@+0x18": struct.unpack_from("<I", vfs, off + 0x18)[0],
        "id@+0x00": struct.unpack_from("<I", vfs, off)[0],
        "size@+0x04": struct.unpack_from("<I", vfs, off + 4)[0],
        "ver@+0x08": struct.unpack_from("<I", vfs, off + 8)[0],
        "crc@+0x0C": "%08X" % struct.unpack_from("<I", vfs, off + 12)[0],
        "id2@+0x10": struct.unpack_from("<I", vfs, off + 16)[0],
        "C@+0x1C": struct.unpack_from("<I", vfs, off + 0x1C)[0],
    }
    pd1 = res["prompt_delta_1_4508"]
    pd1["result"] = "PASS" if (pd1["D@+0x20_bytes"] == "cbe1f942" and pd1["D_value"] == 124.94100189208984
                               and pd1["A@+0x14"] == 296445 and pd1["B@+0x18"] == 296446
                               and pd1["id@+0x00"] == 4508 and pd1["size@+0x04"] == 28
                               and pd1["ver@+0x08"] == 1 and pd1["crc@+0x0C"] == "AFF5797C"
                               and pd1["id2@+0x10"] == 4508 and pd1["C@+0x1C"] == 0) else "FAIL"
    if pd1["result"] != "PASS":
        res["errors"].append("PROMPT_DELTA_1 record 4508 mismatch: %r" % pd1)
    print("[B] PROMPT_DELTA_1 (4508): D@+0x20=%s(%.6f) E@+0x24=%s -> %s"
          % (d_bytes, pd1["D_value"], e_bytes, pd1["result"]))

# ------------------------------------------------------------------ negative control
r4508rec = find_target(4508)
if r4508rec:
    payload = bytearray(vfs[r4508rec["off"] + 16: r4508rec["off"] + 16 + r4508rec["size"]])
    orig = crc32_own(bytes(payload))
    payload[0] ^= 0xFF
    bad = crc32_own(bytes(payload))
    res["negative_control_crc"] = {
        "original": "%08X" % orig, "flipped": "%08X" % bad,
        "claim_original": "AFF5797C", "claim_flipped": "3C32D977",
        "gate_discriminates": bad != orig,
        "matches_claim": (orig == 0xAFF5797C and bad == 0x3C32D977),
    }
    if not res["negative_control_crc"]["matches_claim"]:
        res["errors"].append("negative control mismatch: orig=%08X flipped=%08X" % (orig, bad))
    print("[B] negative control: orig=%08X flipped=%08X (claim AFF5797C -> 3C32D977)"
          % (orig, bad))

# ------------------------------------------------------------------ compare census with S2
with open(S2_JSON, "r", encoding="utf-8") as f:
    s2 = json.load(f)
s2_census = s2["measured"]["true_size_census"]
my_census = res["walk"]["size_census"]
census_equal = {str(k): v for k, v in my_census.items()} if isinstance(my_census, dict) else my_census
res["census_compare"] = {
    "s2_keys": len(s2_census), "qc_keys": len(census_equal),
    "equal": census_equal == s2_census,
    "diffs": {k: [s2_census.get(k), census_equal.get(k)] for k in set(s2_census) | set(census_equal)
              if s2_census.get(k) != census_equal.get(k)},
    "walk_count_s2": s2["measured"]["walk_record_count"], "walk_count_qc": len(records),
    "crc_fail_s2": s2["measured"]["walk_crc_fail_count"], "crc_fail_qc": len(crc_fail),
    "D_s2": s2["measured"]["D_f32_0x20_nonzero"], "D_qc": d_nonzero,
    "E_s2": s2["measured"]["E_f32_0x24_nonzero"], "E_qc": e_nonzero,
    "DE_s2": s2["measured"]["DE_both_nonzero"], "DE_qc": de_both,
    "F_s2": s2["measured"]["F_u32_0x28_nonzero"], "F_qc": f_nonzero,
    "idne_s2": s2["measured"]["id_ne_id2_count"], "idne_qc": id_ne_id2,
    "tail_s2": s2["measured"]["tail_nonzero_count"], "tail_qc": tail_nonzero,
}
print("[B] census compare: equal=%s (s2=%d qc=%d records; crc_fail s2=%s qc=%s; D %s/%s E %s/%s DE %s/%s F %s/%s)"
      % (res["census_compare"]["equal"], res["census_compare"]["walk_count_s2"], len(records),
         res["census_compare"]["crc_fail_s2"], len(crc_fail),
         res["census_compare"]["D_s2"], d_nonzero, res["census_compare"]["E_s2"], e_nonzero,
         res["census_compare"]["DE_s2"], de_both, res["census_compare"]["F_s2"], f_nonzero))
if res["census_compare"]["diffs"]:
    print("[B] census diffs: %r" % res["census_compare"]["diffs"])

# ------------------------------------------------------------------ data binding scans
def scan_file(path, needles):
    out = {}
    with open(path, "rb") as f:
        data = f.read()
    for nd in needles:
        hits = []
        start = 0
        while True:
            i = data.find(nd, start)
            if i < 0:
                break
            hits.append(i)
            start = i + 1
            if len(hits) >= 5:
                break
        out[nd.decode()] = {"count_first5cap": len(hits), "offsets": hits}
    return out


print("[B] scanning Models.bnt (395,412,868 B)...")
res["models_scan"] = scan_file(MODELS, [b"296445.nif", b"126740.nif", b"278453.nif",
                                        b"999999999.nif", b"296446.nif"])
print("[B] Models.bnt: %r" % {k: v["offsets"] for k, v in res["models_scan"].items()})
print("[B] scanning Volumes.bnt (3,746,375 B)...")
res["volumes_scan"] = scan_file(VOLUMES, [b"296446.bvi", b"126741.bvi", b"278454.bvi",
                                          b"999999999.bvi", b"296445.bvi"])
print("[B] Volumes.bnt: %r" % {k: v["offsets"] for k, v in res["volumes_scan"].items()})

# claim verification
res["data_binding_verdict"] = {
    "296445.nif_exists@395268773": 395268773 in res["models_scan"]["296445.nif"]["offsets"],
    "126740.nif_exists@395268719": 395268719 in res["models_scan"]["126740.nif"]["offsets"],
    "278453.nif_exists@395268746": 395268746 in res["models_scan"]["278453.nif"]["offsets"],
    "negative_999999999.nif_absent": len(res["models_scan"]["999999999.nif"]["offsets"]) == 0,
    "296446.bvi_exists@3701937": 3701937 in res["volumes_scan"]["296446.bvi"]["offsets"],
    "126741.bvi_exists@3701883": 3701883 in res["volumes_scan"]["126741.bvi"]["offsets"],
    "278454.bvi_exists@3701910": 3701910 in res["volumes_scan"]["278454.bvi"]["offsets"],
    "negative_999999999.bvi_absent": len(res["volumes_scan"]["999999999.bvi"]["offsets"]) == 0,
}
verdict = res["data_binding_verdict"]
all_ok = all(verdict.values())
if not all_ok:
    res["errors"].append("data binding verdict not all true: %r" % verdict)
print("[B] data-binding verdict: %r -> %s" % (verdict, "ALL PASS" if all_ok else "FAIL"))

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2)
print("\n== B SUMMARY: errors=%d ==" % len(res["errors"]))
for e in res["errors"]:
    print("ERROR: " + e)
sys.exit(1 if res["errors"] else 0)
