#!/usr/bin/env python3
"""
PE_NIF_WITNESS_MATRIX_MAP_R1 (RUN-C) -- driver.

P0 question: which files serve as the WITNESS SET for future falsification
testing of the R61 frozen parser and the documented NIF grammars -- and for
each witness: machine-verified SHA256, predicted parse outcome (PASS/FAIL +
WHY, citing grammar/evidence), and falsification prediction?

MAP ONLY contract (THIS RUN):
  - ZERO renders, ZERO game code, ZERO corrupted-variant builds.
  - The frozen R61 parser is run READ-ONLY on the RAW known-good witnesses
    only (offline parse confirmation -- explicitly permitted).
  - NO corrupted variant is built or parsed. Recipes + predictions only.
  - NO payload bytes are written to the run dir (identity metadata only).
  - Corpus sources (Models.bnt, 2003 extraction dir, R61 source, manifests)
    are READ-ONLY. All outputs go ONLY to this run dir.
  - No bare except. Every exception typed + logged.

Stages (idempotent, sequential):
  s1 r61        - verify R61 frozen baseline 10/10 hashes (READ-ONLY)
  s2 corpus     - Models.bnt identity (sha256, size, BNT2 index meta)
  s3 witnesses  - extract witness payloads IN MEMORY from Models.bnt by BNT2
                  index offset; SHA256 personally; cross-check vs BOTH corpus
                  manifests + prior R61 result CSVs (read-only lookups);
                  hash 2003-era files from the extraction dir (shared names)
  s4 parse      - READ-ONLY R61 parse of the 8 raw witness files (5 primary +
                  3 character/clothing alternates) -> current PASS status
  s5 anchors    - byte-level anchor forensics on the raw payloads (in-memory):
                  locate every named offset the recipes need; verify each
                  prediction's preconditions from raw bytes (G3E boundary
                  recovery scan, G9 RTTI fallback scan, formula-boundary
                  preamble, SCRAMBLE-2 absurd-length simulation arithmetic)
  s6 emit       - 01_RAW jsons + 05_ANALYSIS/WITNESS_MATRIX.json
"""
import sys
import os
import csv
import json
import struct
import hashlib
import traceback

sys.dont_write_bytecode = True  # never touch R01 source __pycache__ (READ-ONLY)

RUN_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_WITNESS_MATRIX_MAP_R1_20260905_123428"
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA_JSON = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json"
CORPUS_2003_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1B3_REAL_PE_NIF_COMPATIBILITY_LAB_V1_20260819_010815\02_extraction\nif"
MANIFEST_935 = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\nif\corpus\pcg953_nif_manifest.csv"
MANIFEST_2003 = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\nif\corpus\manifest_2003.csv"
R61_RESULTS_2003 = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\02_results\FULL_5426_RESULTS_R61.csv"
R61_RESULTS_935 = r"D:\Eudoria_Reconstruction\99_Audits\PE_PCG935_NIF_CORPUS_AUDIT_R1_20260904_113907\02_results\FULL_PARSE_RESULTS_R61_PCG935.csv"
BNT2_INDEX_PCG935 = r"D:\Eudoria_Reconstruction\99_Audits\PE_PCG935_NIF_CORPUS_AUDIT_R1_20260904_113907\02_results\BNT2_INDEX_ENTRIES.csv"

RAW_DIR = os.path.join(RUN_DIR, "01_RAW")
ANA_DIR = os.path.join(RUN_DIR, "05_ANALYSIS")

# Witness sets (names without .nif)
PRIMARY = ["424276", "426763", "500078", "146709", "592572"]
ALTERNATES = ["137260", "574703", "574845"]  # character/clothing extras
ALL_WITNESSES = PRIMARY + ALTERNATES


def log(msg):
    print(msg, flush=True)


def json_default(o):
    """Bytes->hex, frozenset->sorted list, sets->sorted list (identity metadata only)."""
    if isinstance(o, (bytes, bytearray)):
        return {"_bytes_hex": o.hex(), "_len": len(o)}
    if isinstance(o, (set, frozenset)):
        return {"_set": sorted(o)}
    return {"_unserializable": str(type(o))}


def dump_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=json_default)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str, chunk=1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_csv_index(path):
    """Load a manifest CSV into {name: row}."""
    idx = {}
    with open(path, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            idx[row["name"]] = row
    return idx


def load_bnt2(path):
    """BNT2 footer index loader (same contract as audit_pcg935_nif_r1.py)."""
    with open(path, "rb") as f:
        data = f.read()
    file_size = len(data)
    if data[-4:] != b"BNT2":
        raise ValueError(f"not a BNT2 archive: footer magic={data[-4:]!r}")
    index_start = struct.unpack_from("<I", data, file_size - 8)[0]
    if index_start >= file_size:
        raise ValueError(f"index_start {index_start} >= file_size {file_size}")
    count = struct.unpack_from("<I", data, index_start)[0]
    index_end = file_size - 8
    entries = []
    pos = index_start + 4
    for i in range(count):
        if pos >= index_end:
            raise ValueError(f"index truncated at entry {i}")
        name_end = pos
        while name_end < index_end and data[name_end] != 0x0A:
            name_end += 1
        if name_end >= index_end:
            raise ValueError(f"entry {i}: unterminated name")
        name = data[pos:name_end].decode("ascii", errors="replace")
        field_start = name_end + 1
        f_a, f_b, f_c, f_d = struct.unpack_from("<IIII", data, field_start)
        entries.append({"index": i, "name": name, "packed_size": f_a,
                        "offset": f_b, "field_c": f_c, "field_d": f_d})
        pos = field_start + 16
    meta = {"file_size": file_size, "index_start": index_start,
            "declared_count": count, "parsed_count": len(entries)}
    return data, entries, meta


# ============================================================
# Stage s1: R61 frozen baseline verification (READ-ONLY)
# ============================================================
def stage_r61():
    locked = load_json(R61_SHA_JSON)
    files = locked.get("files", locked)
    results = {}
    mismatches = []
    for name, sha in sorted(files.items()):
        path = os.path.join(R61_SOURCE_DIR, name)
        if not os.path.exists(path):
            results[name] = {"status": "MISSING"}
            mismatches.append(f"MISSING {name}")
            continue
        actual = sha256_file(path)
        ok = actual.lower() == str(sha).lower()
        results[name] = {"locked_sha256": str(sha).lower(), "actual_sha256": actual,
                         "status": "MATCH" if ok else "MISMATCH"}
        if not ok:
            mismatches.append(f"MISMATCH {name}")
    out = {"checked": len(results), "match": sum(1 for r in results.values() if r["status"] == "MATCH"),
           "mismatches": mismatches, "files": results,
           "contract": "R61 source used AS-IS, READ-ONLY, from its locked directory"}
    dump_json(out, os.path.join(RAW_DIR, "r61_baseline_verification.json"))
    log(f"[s1 r61] {out['match']}/{out['checked']} MATCH, mismatches={len(mismatches)}")
    if mismatches:
        raise RuntimeError(f"R61 hash verification FAILED: {mismatches}")
    return out


# ============================================================
# Stage s2+s3: corpus identity + witness hashing
# ============================================================
def stage_witnesses():
    # corpus identity
    log("[s2] hashing Models.bnt (395 MB) ...")
    bnt_sha = sha256_file(MODELS_BNT)
    data, entries, meta = load_bnt2(MODELS_BNT)
    entry_by_name = {e["name"]: e for e in entries}
    log(f"[s2] Models.bnt sha256={bnt_sha} entries={meta['parsed_count']}")

    # cross-check BNT2 offsets vs the PCG935 audit's recorded index (read-only)
    pcg_idx = {}
    with open(BNT2_INDEX_PCG935, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pcg_idx[row["name"]] = row

    man935 = load_csv_index(MANIFEST_935)
    man2003 = load_csv_index(MANIFEST_2003)

    # prior R61 result rows (read-only lookups)
    r61_2003_rows = {}
    with open(R61_RESULTS_2003, "r", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            r61_2003_rows[row["filename"]] = row
    r61_935_rows = {}
    with open(R61_RESULTS_935, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r61_935_rows[row["filename"]] = row

    witnesses = {}
    for base in ALL_WITNESSES:
        name = base + ".nif"
        rec = {"name": name}
        # --- 9.3.5 provenance: extract payload IN MEMORY by BNT2 offset ---
        if name not in entry_by_name:
            raise KeyError(f"{name} not in Models.bnt BNT2 index")
        e = entry_by_name[name]
        payload = data[e["offset"]:e["offset"] + e["packed_size"]]
        if len(payload) != e["packed_size"]:
            raise ValueError(f"{name}: short payload slice")
        sha935 = sha256_bytes(payload)
        rec["pcg953_935"] = {
            "source": MODELS_BNT,
            "bnt2_index": e["index"],
            "bnt2_offset": e["offset"],
            "packed_size": e["packed_size"],
            "sha256_computed": sha935,
            "pcg935_audit_offset_crosscheck": (
                int(pcg_idx[name]["offset"]) if name in pcg_idx else None),
            "offset_agrees_with_pcg935_audit": (
                int(pcg_idx[name]["offset"]) == e["offset"]) if name in pcg_idx else None,
            "manifest_sha256": man935[name]["sha256"] if name in man935 else None,
            "manifest_match": (man935[name]["sha256"].lower()
                               == sha935) if name in man935 else None,
        }
        rec["version"] = man935[name]["version"] if name in man935 else None
        rec["variant_family"] = man935[name]["ark_anim_variant"] if name in man935 else None
        rec["manifest_row_935"] = {
            "parse_status": man935[name]["parse_status"],
            "num_blocks": man935[name]["num_blocks"],
            "skinned_meshes": man935[name]["skinned_meshes"],
            "max_bones": man935[name]["max_bones"],
            "morph_blocks": man935[name]["morph_blocks"],
            "keyframe_controllers": man935[name]["keyframe_controllers"],
            "num_text_keys": man935[name]["num_text_keys"],
        } if name in man935 else None
        rec["prior_r61_result_935"] = {
            "parse_status": r61_935_rows[name]["parse_status"],
            "blocks_parsed": r61_935_rows[name]["blocks_parsed"],
        } if name in r61_935_rows else None

        # --- 2003 provenance: hash the extracted corpus file ---
        p2003 = os.path.join(CORPUS_2003_DIR, name)
        if os.path.exists(p2003):
            sha03 = sha256_file(p2003)
            rec["corpus_2003"] = {
                "source": p2003,
                "size": os.path.getsize(p2003),
                "sha256_computed": sha03,
                "manifest_sha256": man2003[name]["sha256"] if name in man2003 else None,
                "manifest_match": (man2003[name]["sha256"].lower() == sha03) if name in man2003 else None,
                "byte_identical_to_935": sha03 == rec["pcg953_935"]["sha256_computed"],
            }
            rec["prior_r61_result_2003"] = {
                "parse_status": r61_2003_rows[name]["parse_status"],
                "blocks_parsed": r61_2003_rows[name]["blocks_parsed"],
            } if name in r61_2003_rows else None
        else:
            rec["corpus_2003"] = "NOT_PRESENT_IN_2003_CORPUS"
            rec["prior_r61_result_2003"] = None
        rec["_payload"] = payload  # in-memory only; NEVER written
        witnesses[base] = rec

    corpus_identity = {
        "models_bnt": {"path": MODELS_BNT, "size": meta["file_size"],
                       "sha256_computed": bnt_sha,
                       "bnt2_index_start": meta["index_start"],
                       "bnt2_declared_count": meta["declared_count"],
                       "bnt2_parsed_count": meta["parsed_count"]},
        "corpus_2003_dir": {"path": CORPUS_2003_DIR,
                            "nif_file_count": len([f for f in os.listdir(CORPUS_2003_DIR)
                                                   if f.endswith(".nif")])},
        "note": "Models.bnt read FULLY in memory; payloads sliced by BNT2 offset; "
                "no corpus file modified; payload bytes never written to run dir",
    }
    dump_json(corpus_identity, os.path.join(RAW_DIR, "corpus_identity.json"))

    # witness hashes (without in-memory payloads)
    wh = {k: {kk: vv for kk, vv in v.items() if kk != "_payload"} for k, v in witnesses.items()}
    dump_json(wh, os.path.join(RAW_DIR, "witness_hashes.json"))

    log(f"[s3] hashed {len(witnesses)} witnesses "
        f"(9.3.5: {len(witnesses)}; 2003-shared: "
        f"{sum(1 for v in witnesses.values() if v['corpus_2003'] != 'NOT_PRESENT_IN_2003_CORPUS')})")
    for base, v in witnesses.items():
        m9 = v["pcg953_935"]["manifest_match"]
        c2 = v["corpus_2003"]
        m2 = c2["manifest_match"] if isinstance(c2, dict) else None
        log(f"      {base}.nif 935_manifest_match={m9} 2003_manifest_match={m2}")
    return witnesses, corpus_identity


# ============================================================
# Stage s4: READ-ONLY parse confirmation
# ============================================================
def stage_parse(witnesses):
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402
    reader = PENifReader()
    confirmations = {}
    for base in ALL_WITNESSES:
        payload = witnesses[base]["_payload"]
        result = reader.parse_bytes(payload, source_name=base + ".nif")
        hist = {}
        for b in result.blocks:
            hist[b.block_type] = hist.get(b.block_type, 0) + 1
        conf = {
            "source": "RAW known-good payload (in-memory BNT2 slice; 9.3.5 provenance)",
            "parse_status": result.parse_status,
            "version_string": result.version_string,
            "version_raw_hex": hex(result.version_raw) if result.version_raw else None,
            "user_version": result.user_version,
            "num_blocks_header": result.num_blocks,
            "num_blocks_parsed": len(result.blocks),
            "blocks_match_header": len(result.blocks) == result.num_blocks,
            "fail_reason": result.fail_reason,
            "block_histogram": dict(sorted(hist.items(), key=lambda kv: -kv[1])),
        }
        confirmations[base] = conf
        log(f"[s4] {base}.nif -> {result.parse_status} blocks={len(result.blocks)}/{result.num_blocks}")
        dump_json(confirmations, os.path.join(RAW_DIR, "parse_confirmations.json"))
    return confirmations


# ============================================================
# Stage s5: anchor forensics (read-only raw byte reads)
# ============================================================
def find_block(result, block_type):
    for b in result.blocks:
        if b.block_type == block_type:
            return b
    return None


def stage_anchors(witnesses, confirmations):
    sys.path.insert(0, R61_SOURCE_DIR)
    from pe_nif_reader import PENifReader  # noqa: E402
    from pe_header import parse_header  # noqa: E402
    from pe_stream import PEStream  # noqa: E402
    import pe_niark_animation as ark  # noqa: E402

    reader = PENifReader()
    A = {}  # anchor forensics per witness

    # helper: v10 NiArkAnimationExtraData field offsets
    def v10_ark_offsets(payload, meta):
        ps = meta.payload_start_abs
        name_len = struct.unpack_from("<i", payload, ps)[0]
        name = payload[ps + 4:ps + 4 + name_len].decode("ascii", errors="replace")
        return {
            "block_index": meta.block_index,
            "preamble_offset_abs": meta.block_start_abs,
            "payload_start_abs": ps,
            "extra_data_name": name,
            "name_len": name_len,
            "u1_offset_abs": ps + 4 + name_len,
            "u2_offset_abs": ps + 4 + name_len + 4,
            "u3_offset_abs": ps + 4 + name_len + 8,
            "u4_offset_abs": ps + 4 + name_len + 12,
            "ext_start_abs": ps + 4 + name_len + 16,
            "u1": struct.unpack_from("<i", payload, ps + 4 + name_len)[0],
            "u2": struct.unpack_from("<I", payload, ps + 4 + name_len + 4)[0],
            "u3": struct.unpack_from("<I", payload, ps + 4 + name_len + 8)[0],
            "u4": struct.unpack_from("<I", payload, ps + 4 + name_len + 12)[0],
        }

    def v4_ark_offsets(payload, meta):
        bs = meta.block_start_abs  # v4: payload start AFTER inline RTTI string consumed
        return {
            "block_index": meta.block_index,
            "block_start_abs": bs,
            "link_offset_abs": bs,
            "u1_offset_abs": bs + 4, "u2_offset_abs": bs + 8,
            "u3_offset_abs": bs + 12, "u4_offset_abs": bs + 16,
            "ext_start_abs": bs + 20,
            "link": struct.unpack_from("<i", payload, bs)[0],
            "u1": struct.unpack_from("<i", payload, bs + 4)[0],
            "u2": struct.unpack_from("<I", payload, bs + 8)[0],
            "u3": struct.unpack_from("<I", payload, bs + 12)[0],
            "u4": struct.unpack_from("<I", payload, bs + 16)[0],
        }

    # ---------------- 424276 (v4 TEXT_CRLF) ----------------
    p = witnesses["424276"]["_payload"]
    res = reader.parse_bytes(p, source_name="424276.nif")
    nl = p.find(b"\n")
    ver_off = nl + 1
    ver_bytes = p[ver_off:ver_off + 4]
    num_blocks = struct.unpack_from("<I", p, nl + 5)[0]
    arkmeta = find_block(res, "NiArkAnimationExtraData")
    v4o = v4_ark_offsets(p, arkmeta)
    ext_start = v4o["ext_start_abs"]
    # TEXT grammar anchors
    crlf1 = p.find(b"\r\n", ext_start, min(ext_start + 5000, len(p)))
    digits_start = crlf1 + 2
    digits_end = digits_start
    while digits_end < len(p) and p[digits_end:digits_end + 2] != b"\r\n":
        digits_end += 1
    digits_bytes = p[digits_start:digits_end]
    # skip stray non-digits as the parser does (only 0x30-0x39 collected)
    digit_chars = bytes(b for b in digits_bytes if 0x30 <= b <= 0x39)
    node_count = int(digit_chars.decode("ascii")) if digit_chars else 0
    # G9 fallback verification: first known-RTTI sized-string candidate >= ext_start
    KNOWN = ark._KNOWN_NIF_TYPES
    g9_first = None
    scan_pos = ext_start
    limit = min(ext_start + 10000, len(p))
    while scan_pos + 4 <= limit:
        slen = struct.unpack_from("<i", p, scan_pos)[0]
        if 5 <= slen <= 50 and scan_pos + 4 + slen <= len(p):
            if p[scan_pos + 4:scan_pos + 4 + slen] in KNOWN:
                g9_first = scan_pos
                break
        scan_pos += 1
    # the true next-block RTTI string start (v4 block after ark anim)
    next_blk = res.blocks[arkmeta.block_index + 1] if arkmeta.block_index + 1 < len(res.blocks) else None
    next_type = next_blk.block_type if next_blk else None
    next_rtti_start = (next_blk.block_start_abs - 4 - len(next_blk.block_type)
                       if next_blk else None)
    # SCRAMBLE-2 simulation arithmetic (corrupted version u32 = 0xFFFFFFFF):
    nbt = struct.unpack_from("<H", p, nl + 9)[0]           # num_block_types u16
    first_ss_len = struct.unpack_from("<i", p, nl + 11)[0]  # first sized_string i32
    A["424276"] = {
        "era": "v4.1.0.12", "variant": "TEXT_CRLF",
        "header": {"header_text": p[:nl].decode("ascii", errors="replace"),
                   "newline_pos": nl, "version_offset_abs": ver_off,
                   "version_bytes_hex": ver_bytes.hex(),
                   "version_u32": struct.unpack_from("<I", p, ver_off)[0],
                   "num_blocks_u32": num_blocks},
        "ark_animation_v4": v4o,
        "ark_parser_fields": {k: v for k, v in arkmeta.fields.items()
                               if k in ("ark_variant", "ark_node_count",
                                        "ark_line_ending", "ark_trailer_family",
                                        "ark_trailer_len")},
        "text_grammar": {
            "first_crlf_abs": crlf1,
            "node_count_digits_start_abs": digits_start,
            "node_count_digits_raw_hex": digits_bytes.hex(),
            "node_count_ascii_digits": digit_chars.decode("ascii", errors="replace"),
            "node_count_value": node_count,
            "node_count_last_digit_abs": digits_start + len(digits_bytes) - 1,
            "node_count_last_digit_hex": hex(p[digits_start + len(digits_bytes) - 1]),
        },
        "next_block_after_ark": {"block_index": arkmeta.block_index + 1,
                                 "block_type": next_type,
                                 "true_rtti_sized_string_start_abs": next_rtti_start},
        "g9_fallback_verification": {
            "first_known_rtti_candidate_abs": g9_first,
            "candidate_is_true_next_block_boundary": g9_first == next_rtti_start,
            "note": "replicates pe_niark_animation._parse_v4_rtti_boundary scan "
                    "(lines 403-410) on the RAW payload; equal values mean the "
                    "MILD-2 corrupted parse recovers the TRUE boundary via G9",
        },
        "scramble2_prediction_inputs": {
            "corrupted_version": "0xFFFFFFFF",
            "sim_num_block_types_u16_at_nl_plus_9": nbt,
            "sim_first_sized_string_len_at_nl_plus_11": first_ss_len,
            "sim_absurd_length_error": (f"absurd string length {first_ss_len} "
                                        f"at pos={nl + 11}") if first_ss_len > 1_000_000
            or first_ss_len < 0 else f"(no absurd length; value {first_ss_len} in range)",
        },
    }

    # ---------------- 426763 (v4 SHORT28) ----------------
    p = witnesses["426763"]["_payload"]
    res = reader.parse_bytes(p, source_name="426763.nif")
    arkmeta = find_block(res, "NiArkAnimationExtraData")
    v4o = v4_ark_offsets(p, arkmeta)
    ext = p[v4o["ext_start_abs"]:v4o["ext_start_abs"] + 8]
    A["426763"] = {
        "era": "v4.1.0.12", "variant": "SHORT28",
        "ark_animation_v4": v4o,
        "ark_parser_fields": {k: v for k, v in arkmeta.fields.items()
                              if k in ("ark_variant", "ark_extension")},
        "short28_verification": {
            "ext_first_8_bytes_hex": ext.hex(),
            "all_zero_8B": ext == b"\x00" * 8,
            "peek7": ext[7],
            "selector_note": "u3==0xFFFFFFFF && u2>=4 && peek[7]==0x00 -> SHORT28 "
                             "(pe_niark_animation.py lines 117-121); docs/nif/08 "
                             "L291: fixed 8B = 8x00, verified 35/35 (ITER-31)",
            "alternate_recipe_note": "single byte peek[7] 0x00->0x01 flips variant "
                                     "to FIXED_B_61 (41B read): +33B over-consume -> "
                                     "v4 inline-RTTI desync -> predicted FAIL "
                                     "(recorded as RECIPE-ALTERNATE, not executed)",
        },
    }

    # ---------------- 500078 (v10 G3B + Bip01) ----------------
    p = witnesses["500078"]["_payload"]
    stream = PEStream(p, source_name="500078.nif")
    header = parse_header(stream, source_name="500078.nif")
    res = reader.parse_bytes(p, source_name="500078.nif")
    arkmeta = find_block(res, "NiArkAnimationExtraData")
    v10o = v10_ark_offsets(p, arkmeta)
    ext_start = v10o["ext_start_abs"]
    g3b_size = struct.unpack_from("<I", p, ext_start)[0]
    g3b_marker = p[ext_start + 4]
    g3b_flag = p[ext_start + 5]
    tk = find_block(res, "NiTextKeyExtraData")
    n_kfc = sum(1 for b in res.blocks if b.block_type == "NiKeyframeController")
    A["500078"] = {
        "era": "v10.1.0.0", "variant": "G3B",
        "header": {"data_start_offset_abs": header.data_start_offset,
                   "first_block_type": header.block_types[header.block_type_index[0]]
                   if header.block_types else None,
                   "num_blocks": header.num_blocks,
                   "num_block_types": len(header.block_types),
                   "user_version": header.user_version},
        "first_preamble_verification": {
            "preamble_offset_abs": header.data_start_offset,
            "raw_u32_hex": struct.unpack_from("<I", p, header.data_start_offset)[0]
                           .to_bytes(4, "little").hex(),
            "is_zero": struct.unpack_from("<I", p, header.data_start_offset)[0] == 0,
        },
        "ark_animation_v10": v10o,
        "ark_parser_fields": {k: v for k, v in arkmeta.fields.items()
                              if k in ("ark_variant", "ark_anim_count", "ark_anim_flag",
                                       "ark_anim_ext_size", "ark_anim_boundary_method")},
        "g3b_record_anchors": {
            "ext_start_abs": ext_start,
            "record_size_u32": g3b_size,
            "record_total_bytes": g3b_size + 4,
            "marker_byte": hex(g3b_marker),
            "flag_byte": hex(g3b_flag),
            "docs_note": "docs/nif/08-ark-proprietary.md L457-464 record grammar "
                         "(ITER-30, byte-exact 1682/1682); L497: 500078 392B "
                         "record with 13 event strings (DUNGMASTER set)",
        },
        "skeleton_and_textkeys": {
            "NiTextKeyExtraData_block_index": tk.block_index if tk else None,
            "NiKeyframeController_count": n_kfc,
            "manifest_num_text_keys": 25,
            "prior_run_ref": "PE_KEYFRAME_FORMAT_R1_20260905_220000 keyframe_inventory.csv: "
                             "ANIMATION_SKELETON, Bip01* bone names (Bip01 Pelvis/Spine*/"
                             "Neck*/Head/Ponytail*/Clavicle/UpperArm/Forearm...)",
        },
    }

    # ---------------- 146709 (v10 G3D class-01) ----------------
    p = witnesses["146709"]["_payload"]
    stream = PEStream(p, source_name="146709.nif")
    header = parse_header(stream, source_name="146709.nif")
    res = reader.parse_bytes(p, source_name="146709.nif")
    arkmeta = find_block(res, "NiArkAnimationExtraData")
    v10o = v10_ark_offsets(p, arkmeta)
    ext_start = v10o["ext_start_abs"]
    u3 = v10o["u3"]
    n_count = (u3 >> 8) & 0xFF
    true_boundary = ext_start + n_count * 5
    tb_u32 = struct.unpack_from("<I", p, true_boundary)[0]
    formula_end_corrupt = ext_start + (n_count + 1) * 5
    fe_u32 = struct.unpack_from("<I", p, formula_end_corrupt)[0]
    # G3E recovery verification: frozen boundary search on RAW from ext_start
    g3e_found = ark._find_v10_block_boundary(p, ext_start, len(p))
    next_blk = res.blocks[arkmeta.block_index + 1] if arkmeta.block_index + 1 < len(res.blocks) else None
    A["146709"] = {
        "era": "v10.1.0.0", "variant": "G3D",
        "ark_animation_v10": v10o,
        "ark_parser_fields": {k: v for k, v in arkmeta.fields.items()
                              if k in ("ark_variant", "ark_anim_ext_size",
                                       "ark_anim_boundary_method")},
        "g3d_formula_anchors": {
            "u3_u32": u3, "u3_byte0": hex(u3 & 0xFF), "u3_byte1_N": n_count,
            "u3_byte1_abs_offset": v10o["u3_offset_abs"] + 1,
            "formula_ext_size_Nx5": n_count * 5,
            "ext_start_abs": ext_start,
            "true_boundary_abs": true_boundary,
            "true_boundary_u32": tb_u32,
            "true_boundary_is_preamble_zero": tb_u32 == 0,
            "corrupted_formula_end_abs": formula_end_corrupt,
            "corrupted_formula_end_u32": fe_u32,
            "corrupted_formula_end_is_nonzero": fe_u32 != 0,
            "g3e_recovery_search_from_ext_start": g3e_found,
            "g3e_recovers_true_boundary": g3e_found == true_boundary,
            "next_block_type": next_blk.block_type if next_blk else None,
            "docs_note": "docs/nif/08 L316: G3D node-reference list, 5-byte records "
                         "[00][class 01|02|03][u16 block_index][00], 348/348 CONFIRMED",
        },
        "skin_rig": {
            "NiSkinInstance": sum(1 for b in res.blocks if b.block_type == "NiSkinInstance"),
            "NiSkinData": sum(1 for b in res.blocks if b.block_type == "NiSkinData"),
            "NiSkinPartition": sum(1 for b in res.blocks if b.block_type == "NiSkinPartition"),
            "max_bones_manifest": 18,
        },
    }

    # ---------------- 592572 (v10 G3D morph) ----------------
    p = witnesses["592572"]["_payload"]
    res = reader.parse_bytes(p, source_name="592572.nif")
    arkmeta = find_block(res, "NiArkAnimationExtraData")
    v10o = v10_ark_offsets(p, arkmeta)
    vm = find_block(res, "NiVertexMorphExtraData")
    vm_info = None
    if vm:
        vs = vm.payload_start_abs
        vname_len = struct.unpack_from("<i", p, vs)[0]
        vname = p[vs + 4:vs + 4 + vname_len].decode("ascii", errors="replace")
        dstart = vs + 4 + vname_len
        vm_info = {
            "block_index": vm.block_index,
            "payload_start_abs": vs,
            "extra_data_name": vname,
            "data_start_abs": dstart,
            "first_byte_const_0x01": hex(p[dstart]),
            "u32_vertex_count": struct.unpack_from("<I", p, dstart + 1)[0],
            "u16_tag": struct.unpack_from("<H", p, dstart + 5)[0],
            "vertex_count_matches_docs_1294": struct.unpack_from("<I", p, dstart + 1)[0] == 1294,
            "boundary_method": vm.fields.get("boundary_method"),
            "docs_note": "docs/nif/08 L146: NiVertexMorphExtraData decoded record model "
                         "(ITER-4): 0x01 const + u32 N (592572: 1294 == 1294 CONFIRMED) "
                         "+ u16 tag + per-vertex records; parser = C24 boundary-search, "
                         "PARTIALLY_KNOWN, boundary EXACT",
        }
    A["592572"] = {
        "era": "v10.1.0.0", "variant": "G3D",
        "ark_animation_v10": v10o,
        "ark_parser_fields": {k: v for k, v in arkmeta.fields.items()
                              if k in ("ark_variant", "ark_anim_ext_size",
                                       "ark_anim_boundary_method")},
        "vertex_morph_block": vm_info,
        "era_drift_note": "present in 9.3.5 corpus (Models.bnt) but NOT in the 2003 "
                          "corpus (manifest_2003 has no 592572.nif) -- the only primary "
                          "witness with single-corpus provenance (era-drift datum)",
    }

    dump_json(A, os.path.join(RAW_DIR, "anchor_forensics.json"))
    log("[s5] anchor forensics: "
        + json.dumps({k: "OK" for k in A}))
    # sanity assertions (loud if any precondition of a prediction is violated)
    assert A["424276"]["g9_fallback_verification"]["candidate_is_true_next_block_boundary"], \
        "MILD-2 precondition violated: G9 first candidate != true boundary"
    assert A["146709"]["g3d_formula_anchors"]["g3e_recovers_true_boundary"], \
        "MILD-1 precondition violated: G3E search does not recover true boundary"
    assert A["146709"]["g3d_formula_anchors"]["true_boundary_is_preamble_zero"], \
        "MILD-1 precondition violated: true boundary preamble not zero"
    assert A["500078"]["first_preamble_verification"]["is_zero"], \
        "SCRAMBLE-3 precondition violated: first preamble not zero"
    log("[s5] all recipe preconditions VERIFIED from raw bytes")
    return A


def main():
    try:
        os.makedirs(RAW_DIR, exist_ok=True)
        os.makedirs(ANA_DIR, exist_ok=True)
        r61 = stage_r61()
        witnesses, corpus_identity = stage_witnesses()
        confirmations = stage_parse(witnesses)
        anchors = stage_anchors(witnesses, confirmations)
        # emit the WITNESS_MATRIX.json (stage s6) in a second pass via a separate
        # emitter call so the matrix assembly is traceable
        emit_matrix(r61, witnesses, corpus_identity, confirmations, anchors)
        log("[DONE] MAP complete; no corrupted variant built or parsed")
    except Exception as ex:
        log(f"[FATAL] {type(ex).__name__}: {ex}")
        log(traceback.format_exc())
        sys.exit(1)


def emit_matrix(r61, witnesses, corpus_identity, confirmations, anchors):
    """Assemble 05_ANALYSIS/WITNESS_MATRIX.json -- the MAP deliverable."""
    C = {
        "run_id": "PE_NIF_WITNESS_MATRIX_MAP_R1_20260905_123428",
        "run_class": "RUN-C WITNESS-MATRIX MAP (offline analysis; ZERO renders; MAP ONLY)",
        "p0_question": "Which files should serve as the WITNESS SET for future "
                       "falsification testing of the R61 frozen parser and the "
                       "documented grammars -- and per witness: machine-verified "
                       "SHA256, predicted parse outcome (PASS/FAIL + WHY), and "
                       "falsification prediction (severely-scrambled MUST fail loudly)?",
        "context": {
            "documentation_loop": "EU935-M2 contribution; wiki HOLD semantics released "
                                  "for THIS map only; NO M2 advancement",
            "r61_baseline": "parse closure 5,596/5,596 (9.3.5 Models.bnt) + "
                            "5,426/5,426 (2003 corpus); frozen 20260828",
            "map_only_contract": "frozen parser run READ-ONLY on RAW known-good files "
                                 "only; NO corrupted variant built or parsed; recipes "
                                 "+ predictions only; no payload bytes in outputs",
        },
        "r61_baseline_verification": {"checked": r61["checked"], "match": r61["match"],
                                      "mismatches": r61["mismatches"],
                                      "contract": "10/10 hashes verified personally "
                                                  "from physical bytes before any use"},
        "corpus_identity": corpus_identity,
    }

    def provenance(base):
        w = witnesses[base]
        p9 = dict(w["pcg953_935"])
        p9.pop("manifest_sha256", None)
        c2 = w["corpus_2003"]
        return {"pcg953_935_payload": p9,
                "corpus_2003": (dict(c2) if isinstance(c2, dict) else c2),
                "era_version": w["version"],
                "variant_family": w["variant_family"],
                "prior_r61_results": {"r61_2003_run": w.get("prior_r61_result_2003"),
                                       "r61_935_run": w.get("prior_r61_result_935")},
                "read_only_confirmation": confirmations[base]}

    kg = []
    kg.append({
        "witness_id": "KG-1", "name": "424276.nif", "era_version": "4.1.0.12",
        "era": "v4", "variant_family": "TEXT_CRLF", "size": 28794,
        "roles": ["TEXT-records witness (NiArkAnimationExtraData TEXT_CRLF self-terminating grammar)",
                  "v4-era representative",
                  "viewport-bearing (NiArkViewportInfoExtraData) + NiFlipController/NiStringExtraData"],
        "prior_run_crossrefs": [
            "pcg953_nif_manifest.csv row 424276.nif (PASS)",
            "manifest_2003.csv row 424276.nif (PASS; byte-identical across eras)",
            "docs/nif/08-ark-proprietary.md L293 (TEXT_CRLF self-terminating grammar; "
            "M1C-era 183 catch-all corrected by R31 G9_RTTI separation)"],
        "provenance": provenance("424276"),
        "predicted_parse_result": {
            "status": "PASS",
            "why": "v4 header grammar (pe_header.py v4 layout: header text -> version "
                   "0x0401000C -> NumBlocks -> inline RTTI blocks); NiArkAnimationExtraData "
                   "v4 selector routes u3!=0xFFFFFFFF + non-zero-prefix to TEXT_CRLF "
                   "(pe_niark_animation.py lines 95-155); TEXT grammar: CRLF -> ASCII "
                   "node_count -> N x NodeDataStart records -> trailer 6B/35B/39B by "
                   "byte[5] (lines 162-264; GTEXT_RAW_GRAMMAR_SPEC 31/31 CONFIRMED); "
                   "R61 closure includes this file (prior 2003 R61 + 9.3.5 R61 rows both PASS)",
            "citations": ["pe_header.py (v4 layout docstring + parse_header)",
                         "pe_niark_animation.py L95-155 (v4 selector), L162-264 (_parse_text_extension)",
                         "docs/nif/08-ark-proprietary.md L293"]},
        "falsification_prediction": {
            "mildly_wrong": "MILD-2 (node_count last ASCII digit +1): ArkAnimationError "
                            "'NodeDataStart not found for node <M>' -> G9_RTTI fallback "
                            "-> PREDICTED PASS with ark_variant flipped TEXT_CRLF->G9_RTTI "
                            "(PARTIALLY_KNOWN, v4_rtti_search). PRECONDITION VERIFIED from "
                            "raw bytes: first known-RTTI candidate == true next-block boundary.",
            "severely_scrambled": "SCRAMBLE-2 (version u32 -> 0xFFFFFFFF): MUST_FAIL_LOUDLY "
                                  "as FAIL_ERROR 'header parse error: absurd string length "
                                  "<computed> at pos=<computed>' (precondition + exact value "
                                  "computed in anchor_forensics.json)."},
    })
    kg.append({
        "witness_id": "KG-2", "name": "426763.nif", "era_version": "4.1.0.12",
        "era": "v4", "variant_family": "SHORT28", "size": 10351,
        "roles": ["v4 FIXED-family (SHORT28) representative",
                  "second v4 variant family for era diversity",
                  "minimal FIXED-family falsification anchor (8B all-zero extension)"],
        "prior_run_crossrefs": [
            "pcg953_nif_manifest.csv row 426763.nif (PASS)",
            "manifest_2003.csv row 426763.nif (PASS; byte-identical across eras)",
            "docs/nif/08-ark-proprietary.md L291 (SHORT28: fixed 8B = 8x00, verified 35/35 ITER-31)"],
        "provenance": provenance("426763"),
        "predicted_parse_result": {
            "status": "PASS",
            "why": "v4 header grammar; NiArkAnimationExtraData v4 selector: u3==0xFFFFFFFF "
                   "&& u2>=4 && peek[7]==0x00 -> SHORT28 fixed 8B extension "
                   "(pe_niark_animation.py lines 117-121); docs L291 'fixed 8 B = 8x00, "
                   "verified 35/35 (ITER-31)'; raw bytes re-verified: ext first 8 bytes "
                   "all zero (anchor_forensics.json)",
            "citations": ["pe_niark_animation.py L117-121",
                         "docs/nif/08-ark-proprietary.md L291"]},
        "falsification_prediction": {
            "mildly_wrong": "RECIPE-ALTERNATE (peek[7] 0x00->0x01 single byte at "
                            "ext_start+7): selector flips SHORT28->FIXED_B_61, reads 41B "
                            "instead of 8B -> +33B over-consume -> v4 inline-RTTI "
                            "desync -> predicted FAIL (unknown block type or StreamError). "
                            "Recorded as alternate; NOT built, NOT parsed this run.",
            "severely_scrambled": "SCRAMBLE-2 pattern also applies (version u32 anchor) "
                                  "-- same MUST_FAIL_LOUDLY class as KG-1."},
    })
    kg.append({
        "witness_id": "KG-3", "name": "500078.nif", "era_version": "10.1.0.0",
        "era": "v10", "variant_family": "G3B", "size": 57642,
        "roles": ["G3B-bearing witness (binary ArkAnimation record grammar)",
                  "character witness: ANIMATION_SKELETON, full Bip01 rig (DUNGMASTER)",
                  "event-block TEXT-records carrier: the documented 392 B record "
                  "(13 event strings, NiTextKeyExtraData 25 keys)",
                  "v10-era representative"],
        "prior_run_crossrefs": [
            "PE_KEYFRAME_FORMAT_R1_20260905_220000 keyframe_inventory.csv: 500078 = "
            "ANIMATION_SKELETON, 38 kf controllers, Bip01* bone names",
            "docs/nif/08-ark-proprietary.md L497 (500078 392 B record: end, morph: 1, "
            "11x start -name <anim> -loop; DUNGMASTER set) + L457-464 (G3B record "
            "grammar, ITER-30, byte-exact 1682/1682)",
            "pcg953_nif_manifest.csv + manifest_2003.csv rows 500078.nif (PASS, identical SHA)"],
        "provenance": provenance("500078"),
        "predicted_parse_result": {
            "status": "PASS",
            "why": "v10 header grammar (pe_header.py v10 layout: text -> version "
                   "0x0A010000 -> user_version -> NumBlocks -> NumBlockTypes u16 + "
                   "type table + BlockTypeIndex u16[] + NumGroups); every block framed "
                   "by 4-byte preamble u32=0 (pe_block_reader.py L269-282); "
                   "NiArkAnimationExtraData v10 u2=2 family -> u3=0 + binary first bytes "
                   "-> G3B boundary search (pe_niark_animation.py L782-810); the G3B ext "
                   "is ONE record [u32 size][u8 02][u8 flag][u32 X][u8 Y][5xf32][u8 class]"
                   "[u8 count][strings] (docs L457-464); NiTextKeyExtraData v10 (C11-B); "
                   "NiKeyframeController/NiKeyframeData (C12-B); prior R61 rows PASS both eras",
            "citations": ["pe_header.py (v10 layout)",
                         "pe_block_reader.py L269-282 (preamble contract)",
                         "pe_niark_animation.py L782-810 (G3B route)",
                         "docs/nif/08-ark-proprietary.md L457-464, L497"]},
        "falsification_prediction": {
            "mildly_wrong": "MILD-3 (u2 LSB 0x02->0x03): MUST FAIL LOUDLY as FAIL_CLOSED "
                            "'variant parse error: v10 NiArkAnimationExtraData "
                            "u2=0x00000003 has no P0-verified parser. FAIL CLOSED.' -- "
                            "the variant-closed failsafe contract.",
            "severely_scrambled": "SCRAMBLE-3 (first v10 block preamble u32 -> 0xDEADBEEF): "
                                  "MUST_FAIL_LOUDLY as FAIL_CLOSED 'non-zero "
                                  "block_preamble_u32=3735928559' at block 0."},
    })
    kg.append({
        "witness_id": "KG-4", "name": "146709.nif", "era_version": "10.1.0.0",
        "era": "v10", "variant_family": "G3D", "size": 41473,
        "roles": ["G3D-bearing witness (formula byte[1]*5 node-reference list)",
                  "character witness: class-01 non-biped mob rig (skinned, 18 bones)",
                  "MILD-1 self-heal recipe carrier (G3D->G3E boundary-search fallback)"],
        "prior_run_crossrefs": [
            "PE_NIF_G3D_CLASS_ROLE_R37_20260904_173625 REPORT.md L75-77: Class-01 files "
            "(7/7): 137260, 146709, 205850, 353140, 459889, 501549, 546608; "
            "L86: 'class-01 = core-bone flag on small non-biped mob rigs'",
            "PE_NIF_G3D_CLASS_R15_COR_20260904_142037 (class census)",
            "docs/nif/08-ark-proprietary.md L316 (G3D: node-reference list, 5-byte "
            "records [00][class 01|02|03][u16 block_index][00]; 348/348 CONFIRMED)"],
        "provenance": provenance("146709"),
        "predicted_parse_result": {
            "status": "PASS",
            "why": "v10 header + preamble grammar; NiArkAnimationExtraData v10 u2=2 "
                   "family -> u3!=0 with byte0=0x01 -> G3D formula ext_size = byte[1]*5 "
                   "(pe_niark_animation.py L817-849); ext = N 5-byte node-reference "
                   "records; formula boundary validated against next-block preamble "
                   "(is_valid_boundary); NiSkinInstance/NiSkinData (C19/C20) + "
                   "NiSkinPartition (C21) parse the 18-bone rig; prior R61 rows PASS",
            "citations": ["pe_niark_animation.py L817-849 (G3D formula)",
                         "docs/nif/08-ark-proprietary.md L316",
                         "pe_standard_blocks.py (parse_niskin_instance / parse_niskin_data / parse_niskin_partition)"]},
        "falsification_prediction": {
            "mildly_wrong": "MILD-1 (u3 byte1 N->N+1): formula boundary misses the next-block "
                            "preamble -> G3E boundary-search fallback -> PREDICTED PASS "
                            "with ark_variant flipped G3D->G3E (boundary_method formula->"
                            "boundary_search). PRECONDITION VERIFIED from raw bytes: "
                            "_find_v10_block_boundary(raw, ext_start) == true boundary "
                            "(anchor_forensics.json).",
            "severely_scrambled": "SCRAMBLE-3 pattern applies (preamble anchor)."},
    })
    kg.append({
        "witness_id": "KG-5", "name": "592572.nif", "era_version": "10.1.0.0",
        "era": "v10", "variant_family": "G3D", "size": 159622,
        "roles": ["morph-bearing witness (NiVertexMorphExtraData, N=1294 documented pairing)",
                  "clothing witness: torso_xtra BASE/BUMP avatar body-part mesh",
                  "era-drift datum: 9.3.5-only (NOT in the 2003 corpus)"],
        "prior_run_crossrefs": [
            "docs/nif/08-ark-proprietary.md L146 (NiVertexMorphExtraData record model "
            "DECODED, ITER-4: 'vertex count N ... CONFIRMED when the correct mesh is "
            "paired: 592572.nif 1294 == 1294')",
            "docs/nif/09-semantics.md L191 area (morph span scope limits; 592572 bi=65 "
            "si=45 mscan_ok_m=[30]; the 334-unfit-residual caveat lineage)",
            "PE_NIF_G3D_CLASS_R15_COR / G3D_CLASS_SEM_R22 / CLASS_SEQUENCES_R37 census files"],
        "provenance": provenance("592572"),
        "predicted_parse_result": {
            "status": "PASS",
            "why": "v10 grammar + G3D formula ext (as KG-4) + NiVertexMorphExtraData "
                   "parsed by the C24 boundary-search parser (PARTIALLY_KNOWN semantics, "
                   "EXACT boundary; pe_standard_blocks.py parse_nivertexmorph_extra_data); "
                   "the documented decoded record model (docs L146) is the WIKI layer "
                   "on top of the parser's boundary: 0x01 const + u32 N + u16 tag + "
                   "per-vertex [u16 tag][W x f32] records; prior R61 row PASS (9.3.5)",
            "citations": ["pe_standard_blocks.py (parse_nivertexmorph_extra_data, C24)",
                         "docs/nif/08-ark-proprietary.md L146-158",
                         "docs/nif/09-semantics.md (morph span scope limits)"]},
        "falsification_prediction": {
            "mildly_wrong": "MILD-1 pattern applies to its G3D ext (same code path as KG-4).",
            "severely_scrambled": "SCRAMBLE-3 pattern applies (preamble anchor). "
                                  "Morph-specific: any future morph-grammar change MUST "
                                  "preserve the 1294 vertex-count pairing (docs L146) "
                                  "and the block boundary EXACT status -- a witness "
                                  "against silent morph-parser regressions."},
    })

    mildly_wrong = [
        {
            "recipe_id": "MILD-1",
            "class": "mildly_wrong_single_byte",
            "source_witness": "146709.nif (KG-4; applies byte-identical to both corpus provenances)",
            "structural_anchor": "NiArkAnimationExtraData u3 byte1 = G3D formula count N "
                                  "(ext_size = N*5)",
            "exact_corruption": {
                "byte_offset_abs_in_payload": anchors["146709"]["g3d_formula_anchors"]["u3_byte1_abs_offset"],
                "before_hex": hex(anchors["146709"]["g3d_formula_anchors"]["u3_byte1_N"]),
                "after_hex": hex(anchors["146709"]["g3d_formula_anchors"]["u3_byte1_N"] + 1),
                "before_value": anchors["146709"]["g3d_formula_anchors"]["u3_byte1_N"],
                "after_value": anchors["146709"]["g3d_formula_anchors"]["u3_byte1_N"] + 1,
                "semantics": "G3D node-reference count N -> N+1 (formula ext "
                             "(N+1)*5 overshoots the true next-block preamble by 5 bytes)"},
            "predicted_outcome": {
                "status": "PASS (self-healed)",
                "failure_mode": "none loud; SILENT variant flip",
                "mechanism": "u3 byte0 stays 0x01 -> G3D branch; formula_ext_size=(N+1)*5; "
                             "is_valid_boundary check at ext_start+(N+1)*5 fails "
                             "(u32 != 0 there -- verified from raw bytes); code falls to "
                             "the G3E else-branch: _find_v10_block_boundary(data, ext_start) "
                             "recovers the TRUE boundary (verified: == ext_start+N*5 with "
                             "preamble u32==0); parse completes",
                "expected_field_changes": {"ark_variant": "G3D -> G3E",
                                           "ark_anim_boundary_method": "formula -> boundary_search",
                                           "semantic_status": "PARTIALLY_KNOWN (already was)"},
                "falsification_value": "if a future parser version hard-fails on formula "
                                       "misalignment or changes the fallback, this witness "
                                       "flips from PASS to FAIL -- detects silent changes "
                                       "to the documented self-heal path"},
            "why_the_parser_should_still_handle_it": "the G3D branch does not trust the "
                                                     "formula blindly: it validates the "
                                                     "computed end against the next v10 "
                                                     "block preamble and falls back to the "
                                                     "shared boundary search (the same "
                                                     "search that handles G3B/G3E)",
            "code_path_citations": ["pe_niark_animation.py L817-849 (G3D formula + "
                                   "is_valid_boundary check), L850-862 (else -> G3E "
                                   "boundary search), L516-589 (_find_v10_block_boundary)"],
            "precondition_verification": anchors["146709"]["g3d_formula_anchors"],
        },
        {
            "recipe_id": "MILD-2",
            "class": "mildly_wrong_single_byte",
            "source_witness": "424276.nif (KG-1; applies byte-identical to both corpus provenances)",
            "structural_anchor": "TEXT_CRLF node_count line: last ASCII digit",
            "exact_corruption": {
                "byte_offset_abs_in_payload": anchors["424276"]["text_grammar"]["node_count_last_digit_abs"],
                "before_hex": anchors["424276"]["text_grammar"]["node_count_last_digit_hex"],
                "after_hex": hex(int(anchors["424276"]["text_grammar"]["node_count_last_digit_hex"], 16) + 1),
                "before_value": anchors["424276"]["text_grammar"]["node_count_ascii_digits"],
                "after_value": str(int(anchors["424276"]["text_grammar"]["node_count_ascii_digits"]) + 1),
                "semantics": "declared node count M -> M+1 (one more NodeDataStart record "
                             "is demanded than exists)",
                "precondition": "last digit must be < '9' for the +1 recipe; otherwise use "
                                "the -1 variant (recorded; NOT the case for this file -- "
                                "actual digits recorded in anchor_forensics.json)"},
            "predicted_outcome": {
                "status": "PASS (self-healed)",
                "failure_mode": "transient ArkAnimationError swallowed by the "
                                "TEXT_CRLF->G9_RTTI fallback; final result SILENT variant flip",
                "mechanism": "_parse_text_extension raises ArkAnimationError('TEXT: "
                             "NodeDataStart not found for node <M>') at the extra node "
                             "iteration (marker find happens first in every loop "
                             "iteration); _parse_v4_variant catches ArkAnimationError and "
                             "falls back to _parse_v4_rtti_boundary; the scan finds the "
                             "TRUE next-block RTTI sized-string (verified from raw bytes: "
                             "first known-type candidate == true boundary) -> boundary "
                             "recovered -> parse completes",
                "expected_field_changes": {"ark_variant": "TEXT_CRLF -> G9_RTTI",
                                           "ark_anim_boundary_method": "-> v4_rtti_search",
                                           "semantic_status": "PARTIALLY_KNOWN"},
                "falsification_value": "documents the tolerance boundary of the TEXT "
                                       "grammar + the G9 catch-all; a future strict "
                                       "grammar (reject instead of fallback) flips this "
                                       "witness to FAIL_CLOSED -- the exact loudness "
                                       "evolution is itself worth falsifying"},
            "why_the_parser_should_still_handle_it": "the v4 selector treats TEXT_CRLF as "
                                                     "try-first with G9 boundary-search "
                                                     "fallback (pe_niark_animation.py "
                                                     "L146-155); the fallback is the "
                                                     "P0-verified route for 10 G9_RTTI files",
            "code_path_citations": ["pe_niark_animation.py L219-222 (marker find + raise), "
                                    "L146-155 (TEXT_CRLF try / G9 fallback), "
                                    "L389-424 (_parse_v4_rtti_boundary scan)"],
            "precondition_verification": anchors["424276"]["g9_fallback_verification"],
        },
        {
            "recipe_id": "MILD-3",
            "class": "mildly_wrong_single_byte_must_reject",
            "source_witness": "500078.nif (KG-3; applies byte-identical to both corpus provenances)",
            "structural_anchor": "NiArkAnimationExtraData u2 LSB = v10 variant family "
                                 "selector (0x00000002 = u2=2 family)",
            "exact_corruption": {
                "byte_offset_abs_in_payload": anchors["500078"]["ark_animation_v10"]["u2_offset_abs"],
                "before_hex": "0x02",
                "after_hex": "0x03",
                "before_value": "u2 = 0x00000002 (G3B family)",
                "after_value": "u2 = 0x00000003 (no P0-verified parser)",
                "semantics": "family selector corruption: u2 is the FIRST dispatch "
                             "decision of the v10 ArkAnimation grammar",
            },
            "predicted_outcome": {
                "status": "FAIL_CLOSED",
                "failure_mode": "ArkAnimationError -> FailClosedError -> parse_status="
                                "FAIL_CLOSED, fail_block_index=<ark block>, "
                                "fail_block_type=NiArkAnimationExtraData, boundary UNSAFE",
                "predicted_fail_reason_exact": "FAIL CLOSED: block_type=NiArkAnimationExtraData "
                                               "offset=<payload_start_abs> reason=variant "
                                               "parse error: v10 NiArkAnimationExtraData "
                                               "u2=0x00000003 has no P0-verified parser. "
                                               "FAIL CLOSED.",
                "mechanism": "_parse_v10_variant: u2u != 0xFFFFFFFF and u2u != 0x00000002 "
                             "-> raise ArkAnimationError (V10_UNKNOWN_U2 branch); "
                             "dispatch_block's generic except converts it to FailClosedError "
                             "('variant parse error: ...'); the reader records FAIL_CLOSED "
                             "and stops",
                "falsification_value": "the R61 grammar is VARIANT-CLOSED by design: only "
                                       "u2=0xFFFFFFFF (Mode1/Mode2) and u2=2 (G3A-G3E) have "
                                       "P0-verified layouts. If this witness ever parses as "
                                       "PASS, the failsafe contract has been broken."},
            "why_the_parser_must_reject": "per the frozen failsafe contract, unknown "
                                          "variant families FAIL CLOSED rather than "
                                          "guessing a layout (R61 closure property: "
                                          "5,596/5,596 with zero guessed layouts)",
            "code_path_citations": ["pe_niark_animation.py L647-653 (V10_UNKNOWN_U2 "
                                    "ArkAnimationError), L44-46 (ArkAnimationError class)",
                                    "pe_block_reader.py L356-362 (variant parse error -> "
                                    "FailClosedError)",
                                    "pe_nif_reader.py L88-106 (FailClosedError -> "
                                    "FAIL_CLOSED recording)"],
            "precondition_verification": {
                "ark_u2_computed": anchors["500078"]["ark_animation_v10"]["u2"],
                "ark_u2_is_2": anchors["500078"]["ark_animation_v10"]["u2"] == 2,
                "ark_variant_from_parse": anchors["500078"]["ark_parser_fields"]},
        },
    ]

    severely_scrambled = [
        {
            "recipe_id": "SCRAMBLE-1",
            "class": "severely_scrambled_container",
            "source": "byte-copy of pcg_install Models.bnt (395,412,868 B; SHA256 recorded "
                      "in corpus_identity.json). NEVER the original -- the recipe is "
                      "defined for a sandbox copy (source-tree safety rule).",
            "structural_anchor_destroyed": "BNT2 footer magic (last 4 bytes of the archive)",
            "exact_corruption": {
                "byte_offset_in_container_copy": "file_size-4 (absolute)",
                "before_hex": "42 4E 54 32 ('BNT2')",
                "after_hex": "58 58 58 58 ('XXXX')",
                "determinism": "fixed 4-byte overwrite; no other byte touched"},
            "falsification_prediction": "MUST_FAIL_LOUDLY: the BNT2 index loader raises "
                                        "ValueError(\"not a BNT2 archive: footer magic=b'XXXX'\") "
                                        "BEFORE any NIF parsing -- all 5,596 payloads become "
                                        "unreachable; the container SHA256 also changes "
                                        "(detectable pre-parse).",
            "why_the_parse_must_fail_loudly": "the footer magic is the outermost structural "
                                              "anchor of the 9.3.5 corpus: without it the "
                                              "index_start pointer is uninterpretable and "
                                              "NO payload can be located",
            "code_path_citations": ["audit_pcg935_nif_r1.py L83-84 (container gate in "
                                    "load_bnt2, the R61-era extraction contract)",
                                    "BNT2 format: marker + footer index (pe-bnt-tdf skill)"],
        },
        {
            "recipe_id": "SCRAMBLE-2",
            "class": "severely_scrambled_header_version",
            "source_witness": "424276.nif payload copy (KG-1; v4.1.0.12)",
            "structural_anchor_destroyed": "NIF version selector field (the u32 that "
                                           "routes ALL downstream grammar mode flags)",
            "exact_corruption": {
                "byte_offset_abs_in_payload": anchors["424276"]["header"]["version_offset_abs"],
                "before_hex": anchors["424276"]["header"]["version_bytes_hex"],
                "after_hex": "ff ff ff ff",
                "before_value": "0x0401000C (4.1.0.12)",
                "after_value": "0xFFFFFFFF (major=255)",
                "determinism": "fixed 4-byte overwrite at the machine-verified version offset"},
            "falsification_prediction": "MUST_FAIL_LOUDLY as FAIL_ERROR 'header parse "
                                        "error: absurd string length <computed> at "
                                        "pos=<computed>' -- exact simulated values "
                                        "recorded in anchor_forensics.json "
                                        "(scramble2_prediction_inputs); the failure occurs "
                                        "in parse_header BEFORE any block is dispatched.",
            "why_the_parse_must_fail_loudly": "parse_version(0xFFFFFFFF) sets type_table=True "
                                              "(raw >= 0x05000001 boundary) while is_v10 stays "
                                              "False -- the header reader then consumes the "
                                              "v4 block area as a v10 type table; the first "
                                              "sized-string length is block data (computed "
                                              "garbage > 1,000,000) and pe_stream's "
                                              "absurd-length guard aborts deterministically",
            "code_path_citations": ["pe_version.py L57-58 (type_table boundary), L46-93 "
                                    "(mode flags)",
                                    "pe_header.py L75-80 (NumBlockTypes + block_types loop)",
                                    "pe_stream.py L121-127 (sized_string absurd-length guard)",
                                    "pe_nif_reader.py L55-60 (header error -> FAIL_ERROR)"],
            "precondition_verification": anchors["424276"]["scramble2_prediction_inputs"],
        },
        {
            "recipe_id": "SCRAMBLE-3",
            "class": "severely_scrambled_block_framing",
            "source_witness": "500078.nif payload copy (KG-3; v10)",
            "structural_anchor_destroyed": "the v10 4-byte block record separator "
                                           "(preamble u32=0) that frames EVERY block",
            "exact_corruption": {
                "byte_offset_abs_in_payload": anchors["500078"]["header"]["data_start_offset_abs"],
                "before_hex": "00 00 00 00",
                "after_hex": "ef be ad de (0xDEADBEEF)",
                "determinism": "fixed 4-byte overwrite at the machine-verified "
                               "first-block preamble offset"},
            "falsification_prediction": "MUST_FAIL_LOUDLY as FAIL_CLOSED 'FAIL CLOSED: "
                                        "block_type=<first block type> offset=<data_start_offset> "
                                        "reason=non-zero block_preamble_u32=3735928559' -- "
                                        "fail_block_index=0, boundary UNSAFE; the reader "
                                        "records the failed block and stops.",
            "why_the_parse_must_fail_loudly": "for 10.0.0.0 <= v < 10.2.0.0 every block is "
                                              "framed by a 4-byte u32=0 separator; "
                                              "dispatch_block treats ANY non-zero preamble "
                                              "as parser desynchronization and fails closed "
                                              "immediately -- this is the single loudest "
                                              "in-file anchor in the v10 grammar",
            "code_path_citations": ["pe_version.py L76 (has_block_preamble)",
                                    "pe_block_reader.py L269-282 (preamble read + "
                                    "non-zero -> FailClosedError)",
                                    "pe_nif_reader.py L88-106 (FAIL_CLOSED recording)"],
            "precondition_verification": anchors["500078"]["first_preamble_verification"],
        },
    ]

    character_clothing = {
        "identifiability_note": "the corpus manifests carry no explicit character/clothing "
                                "type column; identification was made via prior run data "
                                "(keyframe inventory + G3D class-role census) + manifest "
                                "texture/skinning columns, per the RUN-C instruction "
                                "('use prior run data where named')",
        "character_witnesses": [
            {"name": "500078.nif", "status": "PRIMARY WITNESS (KG-3)",
             "identification": "ANIMATION_SKELETON, full Bip01 rig (Bip01, Pelvis, Spine*, "
                                "Neck*, Head, HeadNub, Ponytail*, Clavicle, UpperArm, "
                                "Forearm...), 38 NiKeyframeControllers, DUNGMASTER anim set",
             "source": "PE_KEYFRAME_FORMAT_R1_20260905_220000\\03_EVIDENCE\\keyframe_inventory.csv"},
            {"name": "146709.nif", "status": "PRIMARY WITNESS (KG-4)",
             "identification": "class-01 G3D file (7/7 list: 137260, 146709, 205850, "
                                "353140, 459889, 501549, 546608) -- core-bone flag on "
                                "small NON-BIPED mob rig; skinned_meshes=1, max_bones=18",
             "source": "PE_NIF_G3D_CLASS_ROLE_R37_20260904_173625 REPORT.md L75-86"},
            {"name": "137260.nif", "status": "ALTERNATE (character)",
             "identification": "class-01 G3D mob rig (same 7/7 list); skinned_meshes=1, "
                                "max_bones=49; byte-identical in both corpora (re-hashed "
                                "personally this run)",
             "source": "PE_NIF_G3D_CLASS_ROLE_R37_20260904_173625 REPORT.md L75-77",
             "provenance": provenance("137260")},
        ],
        "clothing_witnesses": [
            {"name": "592572.nif", "status": "PRIMARY WITNESS (KG-5)",
             "identification": "avatar body-part/clothing mesh: torso_xtra BASE + BUMP "
                                "textures; morph-bearing (NiVertexMorphExtraData N=1294); "
                                "9.3.5-only (era drift)",
             "source": "pcg953_nif_manifest.csv textures column + docs/nif/08 L146"},
            {"name": "574703.nif", "status": "ALTERNATE (clothing)",
             "identification": "avatar body-part set: calf/foot/forearm/glasses/hand/"
                                "head_up/leg/torso/upperarm BASE+BUMP (9 skinned morph "
                                "parts, max_bones=24)",
             "source": "pcg953_nif_manifest.csv (morph=9, skinned=9, bones=24)",
             "provenance": provenance("574703")},
            {"name": "574845.nif", "status": "ALTERNATE (clothing)",
             "identification": "avatar body-part set: calf/face/foot/forearm/hand/leg/"
                                "torso/upperarm BASE+BUMP (8 skinned morph parts, "
                                "max_bones=24)",
             "source": "pcg953_nif_manifest.csv (morph=8, skinned=8, bones=24)",
             "provenance": provenance("574845")},
        ],
        "not_identifiable_record": "NONE required -- all witness files above were "
                                    "identified via prior run data; no "
                                    "NOT_IDENTIFIABLE_FROM_MANIFEST entry was needed "
                                    "(the manifest alone would NOT have sufficed: no type "
                                    "column -- this is the exact reason prior-run "
                                    "cross-referencing was mandated)",
    }

    matrix = dict(C)
    matrix["witness_classes"] = {
        "known_good_witnesses": kg,
        "mildly_wrong_recipes": mildly_wrong,
        "severely_scrambled_recipes": severely_scrambled,
        "character_clothing_witnesses": character_clothing,
    }
    matrix["counts"] = {
        "known_good_witnesses": len(kg),
        "mildly_wrong_recipes": len(mildly_wrong),
        "severely_scrambled_recipes": len(severely_scrambled),
        "character_witnesses": 2,
        "clothing_witnesses": 1,
        "alternate_witnesses_rehashed": 3,
        "era_mix": {"v4_era_known_good": 2, "v10_era_known_good": 3,
                    "corpus_era_mix": "4/5 primary witnesses byte-identical across "
                                      "2003 + 9.3.5 corpora (dual provenance hashed "
                                      "personally); 1 witness 9.3.5-only"},
    }
    matrix["milestone_progress"] = {
        "M1": "PARTIAL â€” P0-1 x87 CW experiment DESIGN READY (awaiting review+GO); "
              "witness matrix + scrambled falsification MAP = THIS RUN (delivered); "
              "next queue: georef/P-DATUM, then P-CELLSTREAM/P-CLIMATE",
        "M2": "NOT_ADVANCED â€” EU935-M2 contribution only (wiki HOLD semantics "
              "released for THIS map); zero M2 advancement claims",
        "documentation_loop": "NIF doc loop RUN-C contribution complete; the "
                              "falsification EXECUTION run (building+testing the 6 "
                              "recipe variants in a sandbox) is the proposed NEXT "
                              "run, GATED on explicit authorization",
        "map_only": "no corrupted variant built or parsed; frozen parser used "
                    "READ-ONLY on raw known-good files only",
    }
    dump_json(matrix, os.path.join(ANA_DIR, "WITNESS_MATRIX.json"))
    log(f"[s6] WITNESS_MATRIX.json emitted: "
        f"{len(kg)} known-good, {len(mildly_wrong)} mildly-wrong, "
        f"{len(severely_scrambled)} severely-scrambled")


if __name__ == "__main__":
    main()

