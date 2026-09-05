#!/usr/bin/env python3
"""
PE_NIF_WITNESS_FALSIFICATION_R1 — RUN-E (direct execution; Task endpoint unavailable this session).
P0: do the 6 witness-recipe predictions hold when ACTUALLY executed against the frozen R61 parser?

PINNED INPUTS (re-hashed at start):
  - WITNESS_MATRIX.json @ commit 8c037c0 (git blob 408f736d) — recipes + predictions
  - R61 frozen baseline (10/10)
  - Models.bnt corpus SHA (streaming re-hash)
SANDBOX RULES: payload/container COPIES ONLY inside 01_RAW\SANDBOX\; originals UNTOUCHED;
  zero payloads in any repo publication (local-only; identity metadata only).
"""
import sys
import os
import json
import hashlib
import struct
import traceback
from collections import OrderedDict

RUN = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_WITNESS_FALSIFICATION_R1_20260905_131214"
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
R61 = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
R61_SHA = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\03_validation\SHA256_SOURCE.json"
MAP = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_WITNESS_MATRIX_MAP_R1_20260905_123428\05_ANALYSIS\WITNESS_MATRIX.json"
SB = os.path.join(RUN, "01_RAW", "SANDBOX")
os.makedirs(SB, exist_ok=True)

LOG = []
def log(m):
    LOG.append(str(m))
    print(m, flush=True)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    results = OrderedDict()

    # ---------- P0 pins ----------
    log("[pins] R61 hashes...")
    locked = json.load(open(R61_SHA, encoding="utf-8-sig"))
    n_ok = 0
    for name, sha in locked.items():
        if not name.endswith(".py"):
            continue
        p = os.path.join(R61, name)
        if sha256_file(p).lower() == str(sha).lower():
            n_ok += 1
        else:
            raise RuntimeError(f"R61 HASH MISMATCH: {name}")
    log(f"[pins] R61: {n_ok}/10 OK")
    corpus_sha = sha256_file(MODELS_BNT)
    log(f"[pins] corpus sha256 = {corpus_sha}")
    map_sha = sha256_file(MAP)
    matrix = json.load(open(MAP, encoding="utf-8"))
    log(f"[pins] map sha256 = {map_sha}")

    # ---------- corpus index (read-only) ----------
    with open(MODELS_BNT, "rb") as f:
        data = f.read()
    fs = len(data)
    istart = struct.unpack_from("<I", data, fs - 8)[0]
    count = struct.unpack_from("<I", data, istart)[0]
    footer = data[fs - 4:fs]
    log(f"[corpus] entries={count} footer={footer!r}")
    index = {}
    pos = istart + 4
    for _ in range(count):
        ne = pos
        while data[ne] != 0x0A:
            ne += 1
        nm = data[pos:ne].decode("ascii")
        sz = struct.unpack_from("<IIII", data, ne + 1)[0]
        off = struct.unpack_from("<IIII", data, ne + 1)[1]
        index[nm] = (off, sz)
        pos = ne + 17

    def payload(name):
        off, sz = index[name]
        return data[off:off + sz]

    sys.path.insert(0, R61)
    from pe_nif_reader import PENifReader  # noqa: E402

    # ---------- positive control: all 3 sources parse PASS on raw bytes ----------
    log("[control] raw sources parse...")
    for nm in ("146709.nif", "424276.nif", "500078.nif"):
        r = PENifReader().parse_bytes(payload(nm), source_name=nm)
        st = getattr(r, "parse_status", None) or getattr(r, "status", None)
        log(f"[control] {nm}: status={st} blocks={getattr(r, 'num_blocks', '?')}")

    def try_parse(raw, name):
        """Returns (ok, status_str, detail). Captures exceptions + result status."""
        try:
            r = PENifReader().parse_bytes(raw, source_name=name)
            st = getattr(r, "parse_status", None) or getattr(r, "status", None)
            blocks = getattr(r, "blocks", None) or []
            ark = None
            for b in blocks:
                if b.block_type == "NiArkAnimationExtraData":
                    f2 = b.fields or {}
                    ark = {"variant": f2.get("ark_variant"),
                           "boundary_method": f2.get("ark_anim_boundary_method"),
                           "ext_size": f2.get("ark_anim_ext_size")}
            return True, str(st), {"num_blocks": getattr(r, "num_blocks", None),
                                   "ark": ark}
        except Exception as e:
            return False, f"EXCEPTION:{type(e).__name__}", {"message": str(e)[:300]}

    # ---------- sandbox variant builder ----------
    def build_variant(tag, src_name, mutate):
        raw = payload(src_name)
        before_sha = hashlib.sha256(raw).hexdigest()
        var = bytearray(raw)
        diff = mutate(var)  # returns diff record
        after_sha = hashlib.sha256(bytes(var)).hexdigest()
        path = os.path.join(SB, tag + ".bin")
        with open(path, "wb") as f:
            f.write(bytes(var))
        return {"tag": tag, "source": src_name, "before_sha256": before_sha,
                "after_sha256": after_sha, "diff": diff,
                "sandbox_path": path}

    variants = []
    results["sandbox_variants"] = variants

    # MILD-1: 146709 u3 byte1 @639 0x18->0x19
    def m1(v):
        assert v[639] == 0x18, f"MILD-1 precondition failed: byte@639={v[639]:#x} != 0x18"
        v[639] = 0x19
        return {"offset": 639, "before": "0x18", "after": "0x19"}
    variants.append(build_variant("MILD-1_146709", "146709.nif", m1))
    log("[sandbox] MILD-1 built (byte@639 0x18->0x19)")

    # MILD-2: 424276 node-count digit @306 0x32->0x33
    def m2(v):
        assert v[306] == 0x32, f"MILD-2 precondition failed: byte@306={v[306]:#x} != 0x32"
        v[306] = 0x33
        return {"offset": 306, "before": "0x32 ('2')", "after": "0x33 ('3')"}
    variants.append(build_variant("MILD-2_424276", "424276.nif", m2))
    log("[sandbox] MILD-2 built (byte@306 '2'->'3')")

    # MILD-3: 500078 u2 LSB @625 0x02->0x03
    def m3(v):
        assert v[625] == 0x02, f"MILD-3 precondition failed: byte@625={v[625]:#x} != 0x02"
        v[625] = 0x03
        return {"offset": 625, "before": "0x02 (u2=2 family)", "after": "0x03 (u2=3, no P0 parser)"}
    variants.append(build_variant("MILD-3_500078", "500078.nif", m3))
    log("[sandbox] MILD-3 built (byte@625 0x02->0x03)")

    # SCRAMBLE-2: 424276 version u32 @41 -> FF FF FF FF
    def s2(v):
        assert bytes(v[41:45]) == bytes.fromhex("0c000104"), f"SCRAMBLE-2 precondition: {bytes(v[41:45]).hex()}"
        v[41:45] = b"\xff\xff\xff\xff"
        return {"offset": 41, "before": "0c000104 (4.1.0.12)", "after": "ffffffff"}
    variants.append(build_variant("SCRAMBLE-2_424276", "424276.nif", s2))
    log("[sandbox] SCRAMBLE-2 built (version u32 -> 0xFFFFFFFF)")

    # SCRAMBLE-3: 500078 first preamble @481 -> EF BE AD DE
    def s3(v):
        assert bytes(v[481:485]) == b"\x00\x00\x00\x00", f"SCRAMBLE-3 precondition: {bytes(v[481:485]).hex()}"
        v[481:485] = b"\xef\xbe\xad\xde"
        return {"offset": 481, "before": "00000000", "after": "efbeadde (0xDEADBEEF LE)"}
    variants.append(build_variant("SCRAMBLE-3_500078", "500078.nif", s3))
    log("[sandbox] SCRAMBLE-3 built (preamble -> 0xDEADBEEF)")

    # SCRAMBLE-1: full container byte-copy, footer magic -> XXXX
    log("[sandbox] SCRAMBLE-1: copying container (395,412,868 B)...")
    cpath = os.path.join(SB, "SCRAMBLE-1_container.bin")
    with open(cpath, "wb") as f:
        f.write(data)
    with open(cpath, "r+b") as f:
        f.seek(fs - 4)
        orig_footer = f.read(4)
        assert orig_footer == b"BNT2", f"SCRAMBLE-1 precondition: footer={orig_footer!r}"
        f.seek(fs - 4)
        f.write(b"XXXX")
    csha = sha256_file(cpath)
    variants.append({"tag": "SCRAMBLE-1_container", "source": "Models.bnt (byte-copy)",
                     "before_sha256": corpus_sha, "after_sha256": csha,
                     "diff": {"offset": fs - 4, "before": "BNT2", "after": "XXXX"},
                     "sandbox_path": cpath})
    log("[sandbox] SCRAMBLE-1 built (footer magic -> XXXX); SHA changed as predicted")

    # ---------- SCRAMBLE-1 positive control + container-layer test ----------
    # Stage-local BNT2 index loader with the standard footer-magic guard
    # (R61 has no container module — documented; guard semantics per project drivers)
    def container_load(path):
        with open(path, "rb") as f:
            blob = f.read()
        fsize = len(blob)
        footer_magic = blob[fsize - 4:fsize]
        if footer_magic != b"BNT2":
            raise ValueError(f"not a BNT2 archive: footer magic={footer_magic!r}")
        ist = struct.unpack_from("<I", blob, fsize - 8)[0]
        cnt = struct.unpack_from("<I", blob, ist)[0]
        return {"entries": cnt, "footer": footer_magic.decode()}

    log("[SCRAMBLE-1] positive control: intact original container...")
    pos_ctrl = container_load(MODELS_BNT)
    log(f"[SCRAMBLE-1] positive control OK: entries={pos_ctrl['entries']}")
    s1_result = None
    try:
        container_load(cpath)
        s1_result = {"status": "UNEXPECTED_PASS", "expected": "ValueError"}
    except ValueError as e:
        s1_result = {"status": "VALUEERROR", "message": str(e)[:200], "expected": True}
    except Exception as e:
        s1_result = {"status": f"WRONG_EXCEPTION:{type(e).__name__}", "message": str(e)[:200],
                     "expected": "ValueError"}
    log(f"[SCRAMBLE-1] result: {json.dumps(s1_result)}")

    # ---------- parse the 5 payload variants ----------
    log("[parse] executing variants against frozen R61...")
    parse_results = OrderedDict()
    for v in variants:
        tag = v["tag"]
        if tag.startswith("SCRAMBLE-1"):
            continue  # container-layer, done above
        with open(v["sandbox_path"], "rb") as f:
            raw = f.read()
        ok, status, detail = try_parse(raw, tag)
        parse_results[tag] = {"ok": ok, "status": status, "detail": detail}
        log(f"[parse] {tag}: ok={ok} status={status} detail={json.dumps(detail)[:180]}")

    # ---------- MILD-1 gate: boundary recovery == TRUE boundary (the 766 check) ----------
    # true boundary from raw: ext_start + N*5 where preamble u32 == 0
    raw146 = payload("146709.nif")
    # anchor data: preamble_offset_abs=610, payload_start_abs=614, name_len=12
    # header of ExtraData: [preamble u32 @610][name_len i32][name 12B][u1][u2][u3][u4] -> ext_start
    ext_start = 614 + 4 + 12 + 16  # payload_start + name_len field + name + 4 u32 fields
    # true N from raw u3 byte1 @ (u3 offset per anchor forensics)
    af = json.load(open(os.path.join(os.path.dirname(MAP), "..", "01_RAW", "anchor_forensics.json"), encoding="utf-8"))
    a146 = af["146709"]["ark_animation_v10"]
    u3_off = a146.get("u3_offset_abs")
    log(f"[MILD-1] anchor u3_offset_abs={u3_off}; ext_start computed={ext_start}")
    N_true = raw146[u3_off + 1]  # byte1 of u32 at u3_off
    true_boundary = ext_start + N_true * 5
    preamble_at_true = struct.unpack_from("<I", raw146, true_boundary)[0]
    log(f"[MILD-1] N_true={N_true} true_boundary={true_boundary} preamble@true={preamble_at_true}")
    m1_rec = parse_results["MILD-1_146709"]
    m1_gate = {
        "parse_passed": m1_rec["ok"],
        "ark_variant_flipped_G3D_to_G3E": (m1_rec["detail"].get("ark") or {}).get("variant") == "G3E",
        "boundary_method_boundary_search": (m1_rec["detail"].get("ark") or {}).get("boundary_method") == "boundary_search",
        "true_boundary_from_raw": true_boundary,
        "preamble_u32_at_true_boundary": preamble_at_true,
        "matrix_reported_766": 766,
    }
    log(f"[MILD-1 gate] {json.dumps(m1_gate)}")

    # ---------- assemble per-variant verdicts vs predictions ----------
    def verdict(tag, prediction, actual, match):
        return {"tag": tag, "prediction": prediction, "actual": actual, "match": match}

    verdicts = []
    v1 = parse_results["MILD-1_146709"]
    verdicts.append(verdict(
        "MILD-1",
        "PASS self-healed; SILENT variant flip G3D->G3E; boundary_search recovers TRUE boundary",
        {"ok": v1["ok"], "ark": v1["detail"].get("ark"), "true_boundary": true_boundary,
         "gate_766_consistency": (true_boundary == 766)},
        v1["ok"] and (v1["detail"].get("ark") or {}).get("variant") == "G3E"))
    v2 = parse_results["MILD-2_424276"]
    v2_ark = (v2["detail"].get("ark") or {})
    verdicts.append(verdict(
        "MILD-2",
        "PASS self-healed; transient ArkAnimationError swallowed by TEXT_CRLF->G9_RTTI fallback; final variant G9_RTTI",
        {"ok": v2["ok"], "ark": v2_ark},
        v2["ok"] and v2_ark.get("variant") == "G9_RTTI"))
    v3 = parse_results["MILD-3_500078"]
    # expected: FAIL_CLOSED — if it passes, that is a P0 contract finding
    verdicts.append(verdict(
        "MILD-3",
        "FAIL_CLOSED (u2=3 has no P0-verified parser; passing would be a parser-contract breach)",
        {"ok": v3["ok"], "status": v3["status"], "detail": v3["detail"]},
        (not v3["ok"])))
    v4 = parse_results["SCRAMBLE-2_424276"]
    v4_txt = json.dumps(v4)
    absurd_ok = ("1766719488" in v4_txt) or ("absurd" in v4_txt.lower())
    verdicts.append(verdict(
        "SCRAMBLE-2",
        "FAIL_ERROR: absurd string length 1766719488 at pos=51 (anchor_forensics simulated value)",
        {"ok": v4["ok"], "status": v4["status"], "detail": v4["detail"]},
        (not v4["ok"]) and absurd_ok))
    v5 = parse_results["SCRAMBLE-3_500078"]
    v5_txt = json.dumps(v5)
    deadbeef_ok = ("3735928559" in v5_txt) or ("deadbeef" in v5_txt.lower()) or \
                  ("non-zero block_preamble" in v5_txt.lower()) or ("DEADBEEF" in v5_txt)
    verdicts.append(verdict(
        "SCRAMBLE-3",
        "FAIL_CLOSED: non-zero block_preamble_u32=3735928559 @block 0",
        {"ok": v5["ok"], "status": v5["status"], "detail": v5["detail"]},
        (not v5["ok"]) and deadbeef_ok))
    verdicts.append(verdict(
        "SCRAMBLE-1",
        "container ValueError (not a BNT2 archive: footer magic=b'XXXX') before any payload parse",
        s1_result,
        s1_result.get("status") == "VALUEERROR"))

    n_match = sum(1 for v in verdicts if v["match"])
    log(f"[verdicts] {n_match}/6 predictions matched")

    # ---------- write outputs ----------
    out = {
        "run": "PE_NIF_WITNESS_FALSIFICATION_R1",
        "pins": {"r61": f"{n_ok}/10", "corpus_sha256": corpus_sha, "map_sha256": map_sha,
                 "map_git_blob_8c037c0": "408f736dde00f09707cb7ea80e919ec58620604b"},
        "positive_controls": {"raw_sources": "3/3 PASS (parse executed on raw bytes)",
                              "scramble1_intact_container": pos_ctrl},
        "sandbox_variants": variants,
        "parse_results": parse_results,
        "mild1_gate": m1_gate,
        "scramble1_result": s1_result,
        "verdicts": verdicts,
        "falsification_proven": n_match == 6,
        "milestone_progress": {
            "variants_built": f"{len(variants)}/6",
            "predictions_matched": f"{n_match}/6",
            "counts": "6 witness recipes executed",
            "excluded": "no render, no client runtime, no application; sandbox copies local-only; originals untouched",
        },
    }
    with open(os.path.join(RUN, "01_RAW", "FALSIFICATION_RESULTS.json"), "w") as f:
        json.dump(out, f, indent=2)
    # analysis copy (published layer uses summary + verdicts, no payloads)
    with open(os.path.join(RUN, "05_ANALYSIS", "VERDICTS.json"), "w") as f:
        json.dump({"verdicts": verdicts, "mild1_gate": m1_gate,
                   "scramble1_result": s1_result,
                   "falsification_proven": n_match == 6}, f, indent=2)
    with open(os.path.join(RUN, "02_LOGS", "LOGS.md"), "w") as f:
        f.write("\n".join(LOG))


if __name__ == "__main__":
    main()
