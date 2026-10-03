#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 - Batch E1 phase_selection.py
Test-corpus selection (G-SEL-1/G-SEL-2). STATIC / READ-ONLY on originals.

Fail-closed chain:
  1. re-hash Models.bnt (pin C950A8C2... 395412868 B) - HARD STOP on mismatch
  2. re-hash manifest pcg953_nif_manifest.csv (pin 2BE0DEFC... 2827906 B)
  3. parse manifest with python csv (real parser; embedded newlines)
  4. own BNT2 trailer-index walk (calibrated on 296445.nif anchor), layout
     auto-detected vs the pinned UNVERIFIED_REFERENCE T1 values, validated
     across all entries (offset+size <= index_start)
  5. mechanical selection T2-T5 per SELECTION.md section 1 (+tie-breaks),
     candidates cross-checked against the Models.bnt index
  6. FRESH extraction of T1-T5 payloads into THIS run's sandbox
  7. NIF version re-read from each EXTRACTED file's own header
  8. EXTRACT_PROVENANCE.json -> package 04_EVIDENCE; selection_report.json
"""
import csv, hashlib, json, os, re, struct, sys

RUN = "PE_GAMEBRYO_ORACLE_TOOL_R1_20261003"
PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003"
SBX = r"D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox"
MODELS = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MANIFEST = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\nif\corpus\pcg953_nif_manifest.csv"
PAYDIR = os.path.join(SBX, "payloads")
os.makedirs(PAYDIR, exist_ok=True)

PIN_MODELS_SHA = "C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0"
PIN_MODELS_SIZE = 395412868
PIN_MANIFEST_SHA = "2BE0DEFC9C09FF26371528A4601C10216AC3013717A244EB0652169123989B59"
PIN_MANIFEST_SIZE = 2827906
# UNVERIFIED_REFERENCE cross-check values (interrupted run; not trusted inputs)
REF = {"t1_offset": 116223520, "t1_size": 57316,
       "t1_sha": "3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36",
       "anchor_296445_nameoff": 395268773,
       "t1_entry_index": 781, "t1_name_file_offset": 395283797,
       "t1_header": "Gamebryo File Format, Version 10.1.0.0", "t1_num_blocks": 66,
       "models_index_start": 395262727, "models_index_count": 5596}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()

def hardstop(reason):
    print("HARD_STOP: " + reason)
    sys.exit(3)

# ---------- 1-2. fail-closed re-hash ----------
m_size = os.path.getsize(MODELS)
m_sha = sha256_file(MODELS)
print("Models.bnt size=%d sha256=%s" % (m_size, m_sha))
if m_size != PIN_MODELS_SIZE or m_sha != PIN_MODELS_SHA:
    hardstop("Models.bnt pin mismatch (size %d vs %d, sha %s)" % (m_size, PIN_MODELS_SIZE, m_sha))
mf_size = os.path.getsize(MANIFEST)
mf_sha = sha256_file(MANIFEST)
print("manifest size=%d sha256=%s" % (mf_size, mf_sha))
if mf_size != PIN_MANIFEST_SIZE or mf_sha != PIN_MANIFEST_SHA:
    hardstop("manifest pin mismatch (size %d vs %d, sha %s)" % (mf_size, PIN_MANIFEST_SIZE, mf_sha))

# ---------- 3. manifest parse (real CSV parser) ----------
with open(MANIFEST, "r", encoding="utf-8-sig", newline="") as f:
    rdr = csv.DictReader(f)
    cols = rdr.fieldnames
    rows = list(rdr)
print("manifest columns: %s" % cols)
print("manifest logical rows: %d" % len(rows))
if len(rows) != 5596:
    hardstop("manifest row count %d != 5596" % len(rows))
lowcols = {c.lower(): c for c in cols}
def col(name):
    return lowcols.get(name)
C_NAME, C_SIZE, C_SHA = col("name"), col("size"), col("sha256")
C_VER, C_BLOCKS = col("version"), col("num_blocks")
if not all([C_NAME, C_SIZE, C_VER]):
    hardstop("manifest missing required columns")
def get_blocks(r):
    v = (r.get(C_BLOCKS) or "0").strip()
    try:
        return int(v)
    except ValueError:
        return 0
vers = {}
for r in rows:
    vers[r[C_VER]] = vers.get(r[C_VER], 0) + 1
print("version distribution: %s" % vers)

# ---------- 4. own BNT2 index walk ----------
size = os.path.getsize(MODELS)
with open(MODELS, "rb") as f:
    f.seek(size - 8)
    tail = f.read(8)
index_start, = struct.unpack("<I", tail[:4])
if tail[4:] != b"BNT2":
    hardstop("Models.bnt footer is %r not BNT2" % tail[4:])
with open(MODELS, "rb") as f:
    f.seek(index_start)
    blob = f.read()
count, = struct.unpack_from("<I", blob, 0)
print("index_start=%d count=%d" % (index_start, count))
if count != 5596:
    hardstop("index count %d != 5596" % count)
entries = []
pos = 4
for i in range(count):
    nl = blob.find(b"\x0a", pos)
    if nl < 0:
        hardstop("0x0A not found at entry %d" % i)
    name = blob[pos:nl].decode("latin-1")
    meta = blob[nl + 1:nl + 17]
    entries.append({"entry_index": i, "name": name,
                    "name_file_offset": index_start + pos,
                    "meta_hex": meta.hex(), "meta": meta})
    pos = nl + 17
idx_by_name = {}
for e in entries:
    idx_by_name.setdefault(e["name"], []).append(e)
dups = {k: len(v) for k, v in idx_by_name.items() if len(v) > 1}
print("duplicate index names: %d" % len(dups))
# anchor calibration
anchor = idx_by_name.get("296445.nif", [None])[0]
print("anchor 296445.nif name_file_offset=%d (ref %d) MATCH=%s" %
      (anchor["name_file_offset"], REF["anchor_296445_nameoff"],
       anchor["name_file_offset"] == REF["anchor_296445_nameoff"]))
if anchor["name_file_offset"] != REF["anchor_296445_nameoff"]:
    hardstop("anchor 296445.nif name_file_offset mismatch - index walk desynced")
# metadata layout auto-detect on T1
t1e = idx_by_name.get("218757.nif", [None])[0]
if t1e is None:
    hardstop("218757.nif absent from Models.bnt index")
off_pos = size_pos = None
for k in range(0, 13, 4):
    if struct.unpack_from("<I", t1e["meta"], k)[0] == REF["t1_offset"]:
        off_pos = k
    if struct.unpack_from("<I", t1e["meta"], k)[0] == REF["t1_size"]:
        size_pos = k
print("metadata layout: offset@%s size@%s (16B meta=%s)" % (off_pos, size_pos, t1e["meta_hex"]))
if off_pos is None or size_pos is None:
    hardstop("could not detect index metadata layout vs pinned T1 values")
bad_bounds = 0
for e in entries:
    e["payload_offset"] = struct.unpack_from("<I", e["meta"], off_pos)[0]
    e["payload_size"] = struct.unpack_from("<I", e["meta"], size_pos)[0]
    if e["payload_offset"] + e["payload_size"] > index_start:
        bad_bounds += 1
print("entries with offset+size beyond index_start: %d" % bad_bounds)
if bad_bounds:
    hardstop("%d index entries violate bounds" % bad_bounds)
print("T1 index: entry_index=%d (ref %d) name_off=%d (ref %d) offset=%d size=%d" %
      (t1e["entry_index"], REF["t1_entry_index"], t1e["name_file_offset"],
       REF["t1_name_file_offset"], t1e["payload_offset"], t1e["payload_size"]))
t1_ref_ok = (t1e["entry_index"] == REF["t1_entry_index"]
             and t1e["name_file_offset"] == REF["t1_name_file_offset"]
             and t1e["payload_offset"] == REF["t1_offset"]
             and t1e["payload_size"] == REF["t1_size"])
print("T1 reference cross-check ALL MATCH = %s" % t1_ref_ok)

# ---------- 5. mechanical selection ----------
exclusions = []
def index_crosscheck(name, manifest_size):
    e = idx_by_name.get(name, [None])[0]
    if e is None:
        return None, "absent from Models.bnt index"
    if e["payload_size"] != manifest_size:
        return None, "size mismatch manifest %d vs index %d" % (manifest_size, e["payload_size"])
    return e, None

def pick(pool, key, label):
    srt = sorted(pool, key=key)
    for cand in srt:
        e, err = index_crosscheck(cand["name"], int(cand[C_SIZE]))
        if err:
            exclusions.append({"candidate": cand["name"], "rule": label, "reason": err})
            continue
        return cand, e
    hardstop("no valid candidate for %s" % label)

rows_101 = [r for r in rows if r[C_VER] == "10.1.0.0"]
rows_412 = [r for r in rows if r[C_VER] == "4.1.0.0" or r[C_VER] == "4.1.0.12"]
rows_412 = [r for r in rows_412 if r[C_VER] == "4.1.0.12"]
t1_row = next(r for r in rows if r[C_NAME] == "218757.nif")
t2_row, t2_e = pick(rows_101, lambda r: (int(r[C_SIZE]), get_blocks(r), r[C_NAME]), "T2")
t3_row, t3_e = pick(rows_101, lambda r: (-get_blocks(r), -int(r[C_SIZE]), r[C_NAME]), "T3")
t4_row, t4_e = pick(rows_412, lambda r: (int(r[C_SIZE]), get_blocks(r), r[C_NAME]), "T4")
excl_names = {"218757.nif", t2_row[C_NAME], t4_row[C_NAME]}
rows_t5 = [r for r in rows if r[C_NAME] not in excl_names]
t5_row, t5_e = pick(rows_t5, lambda r: (int(r[C_SIZE]), get_blocks(r), r[C_NAME]), "T5")
print("pools: 10.1.0.0=%d 4.1.0.12=%d all=%d T5pool=%d" %
      (len(rows_101), len(rows_412), len(rows), len(rows_t5)))
print("T2=%s size=%s blocks=%s" % (t2_row[C_NAME], t2_row[C_SIZE], get_blocks(t2_row)))
print("T3=%s size=%s blocks=%s" % (t3_row[C_NAME], t3_row[C_SIZE], get_blocks(t3_row)))
print("T4=%s size=%s blocks=%s" % (t4_row[C_NAME], t4_row[C_SIZE], get_blocks(t4_row)))
print("T5=%s size=%s blocks=%s" % (t5_row[C_NAME], t5_row[C_SIZE], get_blocks(t5_row)))
print("exclusions: %s" % exclusions)

# ---------- 6-7. fresh extraction + header re-read ----------
def read_nif_header(data):
    nl = data.find(b"\n")
    if nl < 0:
        return None
    header_line = data[:nl].decode("latin-1")
    ver, = struct.unpack_from("<I", data, nl + 1)
    p = nl + 5
    ud = None
    def pack(a, b, c, d):
        return (a << 24) | (b << 16) | (c << 8) | d
    if ver >= pack(10, 0, 1, 8):
        ud, = struct.unpack_from("<I", data, p)
        p += 4
    nb, = struct.unpack_from("<I", data, p)
    return {"header_line": header_line, "version_u32": ver,
            "version_decoded": "%d.%d.%d.%d" % ((ver >> 24) & 255, (ver >> 16) & 255, (ver >> 8) & 255, ver & 255),
            "user_defined_u32": ud, "num_blocks_from_header": nb}

sel = {"T1": (t1_row, t1e), "T2": (t2_row, t2_e), "T3": (t3_row, t3_e),
       "T4": (t4_row, t4_e), "T5": (t5_row, t5_e)}
prov = {"run_id": RUN, "stage": "T_corpus_selection_and_extraction",
        "container": {"path": MODELS, "size": m_size, "sha256": m_sha,
                      "pin_sha256": PIN_MODELS_SHA, "pin_match": True},
        "manifest": {"path": MANIFEST, "size": mf_size, "sha256": mf_sha,
                     "pin_sha256": PIN_MANIFEST_SHA, "pin_match": True,
                     "logical_rows": len(rows), "version_distribution": vers},
        "bnt2_index": {"index_start": index_start, "entry_count": count,
                       "anchor_296445_nameoff": anchor["name_file_offset"],
                       "anchor_match": True,
                       "meta_layout": {"offset_byte_pos": off_pos, "size_byte_pos": size_pos},
                       "walk": "own trailer-index parser: last8={u32 index_start,'BNT2'}; blob=count u32; entries=name until 0x0A + 16B metadata"},
        "selection": {}, "payloads": {}}
for t, (r, e) in sel.items():
    with open(MODELS, "rb") as f:
        f.seek(e["payload_offset"])
        raw = f.read(e["payload_size"])
    sha = hashlib.sha256(raw).hexdigest().upper()
    method = "raw slice [offset, offset+size)"
    man_sha = (r.get(C_SHA) or "").strip().upper()
    sha_matches_manifest = (sha == man_sha)
    if not sha_matches_manifest:
        import zlib
        try:
            dec = zlib.decompress(raw)
            sha2 = hashlib.sha256(dec).hexdigest().upper()
            if sha2 == man_sha:
                raw, sha, method = dec, sha2, "zlib-decompressed slice"
        except Exception:
            pass
    outp = os.path.join(PAYDIR, r[C_NAME])
    open(outp, "wb").write(raw)
    hdr = read_nif_header(raw)
    rec = {"T": t, "asset": r[C_NAME],
           "index_entry": {"entry_index": e["entry_index"], "name_file_offset": e["name_file_offset"],
                           "payload_offset": e["payload_offset"], "payload_size": e["payload_size"],
                           "meta_hex": e["meta_hex"]},
           "manifest_row": {"version": r[C_VER], "size": int(r[C_SIZE]), "num_blocks": get_blocks(r),
                            "sha256": man_sha},
           "extracted": {"path": outp, "size_bytes": len(raw), "sha256": sha, "method": method,
                         "sha_matches_manifest": sha_matches_manifest},
           "header": hdr}
    if t == "T1":
        rec["T1_reference_crosscheck"] = {
            "offset_match": e["payload_offset"] == REF["t1_offset"],
            "size_match": e["payload_size"] == REF["t1_size"],
            "sha_match_vs_interrupted_run": sha == REF["t1_sha"],
            "header_match": hdr and hdr["header_line"] == REF["t1_header"],
            "num_blocks_match": hdr and hdr["num_blocks_from_header"] == REF["t1_num_blocks"]}
    prov["payloads"][t] = rec
    print("T%s %s off=%d size=%d sha=%s header=%r ver=%s blocks=%d" %
          (t, r[C_NAME], e["payload_offset"], e["payload_size"], sha[:16],
           hdr["header_line"] if hdr else None,
           hdr["version_decoded"] if hdr else None,
           hdr["num_blocks_from_header"] if hdr else -1))

prov["selection"] = {
    "rules": "SELECTION.md section 1 (fixed T1; T2 min-size 10.1.0.0; T3 max num_blocks 10.1.0.0; T4 min-size 4.1.0.12; T5 overall min-size excluding T1/T2/T4; tie-breaks: size-min smaller num_blocks then lex name; max-blocks larger size then lex name)",
    "candidate_pools": {"10.1.0.0": len(rows_101), "4.1.0.12": len(rows_412),
                        "total": len(rows), "t5_pool": len(rows_t5)},
    "exclusions": exclusions,
    "selected": {t: {"name": r[C_NAME], "version": r[C_VER],
                     "size": int(r[C_SIZE]), "num_blocks_manifest": get_blocks(r)}
                 for t, (r, e) in sel.items()},
    "mechanical": "computed from manifest + Models.bnt index ONLY, before any oracle run"}

with open(os.path.join(PKG, "04_EVIDENCE", "EXTRACT_PROVENANCE.json"), "w", encoding="utf-8") as f:
    json.dump(prov, f, indent=1)
with open(os.path.join(SBX, "phaseBC", "selection_report.json"), "w", encoding="utf-8") as f:
    json.dump(prov, f, indent=1)
print("EXTRACT_PROVENANCE.json + selection_report.json written")
print("SELECTION_DATA_OK")
