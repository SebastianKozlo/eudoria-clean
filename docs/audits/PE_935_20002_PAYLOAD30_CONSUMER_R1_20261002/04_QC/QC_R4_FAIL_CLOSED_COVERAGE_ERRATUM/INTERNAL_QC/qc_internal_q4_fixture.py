#!/usr/bin/env python3
# FRESH INTERNAL QC (Q4) - fixture verification with MY OWN differ.
# Independent implementation: flatten-leaf-paths diff (not the executor's
# recursive walk), own byte-level diff, own census, own payload scan.
import sys
sys.dont_write_bytecode = True

import hashlib
import json
import os

PKG = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002"
REV = os.path.join(PKG, "04_QC", "QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM")
RAW = os.path.join(PKG, "01_RAW", "DESKTOP_CORRECTION_R1")
FIXTURE = os.path.join(REV, "FIXTURE_INVALID_VA")
IQ = os.path.join(REV, "INTERNAL_QC")
OUT = os.path.join(IQ, "Q4_FIXTURE_VERIFICATION_RESULT.json")

ARTIFACTS = ["BRANCH_SELECTION_TRACE.json", "FALLBACK_PATH_RECORD.json",
             "DESTINATION_PROOF_CORRECTION_R1.json", "CURSOR_PROOF_CORRECTION_R1.json"]
FREEZE_EXPECTED = {
    "BRANCH_SELECTION_TRACE.json": "D488D5346F27E37B3EDCA9818A5BF8FAB9420DA5DAFA416A3DF2226E0A6C7D04",
    "FALLBACK_PATH_RECORD.json": "67956FD18D4A1AD74A94B3FAB599CA324FC938888988663230A2761E775CFEE2",
    "DESTINATION_PROOF_CORRECTION_R1.json": "AF0E2657893B5A98F99D99821B275AA13EFEC86FEC5037A486EA1BDCAE8808A6",
    "CURSOR_PROOF_CORRECTION_R1.json": "2E0BEA3D80B47F9D2DA655FF8862122E6196A17E728D38F04A42F1F7C1A95DBB",
}
MUTATED_BST_EXPECTED = "F40AAA249A7D8C20B24F3E70839C3064AF16C3E7C6840A7917FAF5A5BA9F3B25"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def load(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def pstr(path):
    """Render a leaf path tuple like pins[74].va (my own renderer)."""
    out = ""
    for comp in path:
        if isinstance(comp, int):
            out += "[%d]" % comp
        else:
            out += ("." if out else "") + str(comp)
    return out


def flatten(obj, path=()):
    """My OWN flatten-to-leaf-paths differ basis. Leaves = scalars."""
    leaves = {}
    if isinstance(obj, dict):
        if not obj:
            leaves[path] = "{}"
        for k in obj:
            leaves.update(flatten(obj[k], path + (k,)))
    elif isinstance(obj, list):
        if not obj:
            leaves[path] = "[]"
        for i, v in enumerate(obj):
            leaves.update(flatten(v, path + (i,)))
    else:
        leaves[path] = obj
    return leaves


def my_leaf_diff(a, b):
    """Flatten both, compare leaf maps. Returns list of diffs with my own
    rendering: added/removed/changed leaves."""
    fa = flatten(a)
    fb = flatten(b)
    diffs = []
    for k in sorted(fa.keys() | fb.keys(), key=lambda t: (pstr(t),)):
        if k not in fb:
            diffs.append({"path": pstr(k), "change": "removed_in_fixture", "old": fa[k]})
        elif k not in fa:
            diffs.append({"path": pstr(k), "change": "added_in_fixture", "new": fb[k]})
        elif fa[k] != fb[k]:
            diffs.append({"path": pstr(k), "change": "value", "old": fa[k], "new": fb[k]})
    return diffs


def my_input_ids(inputs_dir):
    ids = []
    for art in ARTIFACTS:
        doc = load(os.path.join(inputs_dir, art))
        main = doc.get("pins")
        used = None
        if isinstance(main, list) and len(main) > 0:
            used = "pins"
        elif "entry_pins" in doc:
            main = doc.get("entry_pins")
            if isinstance(main, list):
                used = "entry_pins"
        if used is not None:
            for i in range(len(main)):
                ids.append("%s::%s[%d]" % (art, used, i))
        ws = doc.get("width_sources")
        if isinstance(ws, dict):
            for key in sorted(ws.keys()):
                wp = ws[key].get("width_pins") if isinstance(ws[key], dict) else None
                if isinstance(wp, list):
                    for i in range(len(wp)):
                        ids.append("%s::width_sources.%s.width_pins[%d]" % (art, key, i))
    return ids


def main():
    result = {"q": "Q4_fixture_verification", "hashes": {}, "checks": {}}

    # 1. hash matrix: canonical vs fixture vs freeze-expected
    for art in ARTIFACTS:
        cpath = os.path.join(RAW, art)
        fpath = os.path.join(FIXTURE, art)
        result["hashes"][art] = {
            "canonical_sha256": sha256_file(cpath),
            "fixture_sha256": sha256_file(fpath),
            "freeze_expected_sha256": FREEZE_EXPECTED[art],
            "canonical_size": os.path.getsize(cpath),
            "fixture_size": os.path.getsize(fpath),
        }
    h = result["hashes"]
    other_three_equal = all(h[a]["canonical_sha256"] == h[a]["fixture_sha256"] == FREEZE_EXPECTED[a]
                            for a in ARTIFACTS if a != "BRANCH_SELECTION_TRACE.json")
    result["checks"]["three_non_mutated_fixture_files_hash_equal_canonical"] = other_three_equal
    result["checks"]["fixture_BST_sha_matches_expected_mutated"] = (
        h["BRANCH_SELECTION_TRACE.json"]["fixture_sha256"] == MUTATED_BST_EXPECTED)
    result["checks"]["canonical_BST_sha_matches_freeze"] = (
        h["BRANCH_SELECTION_TRACE.json"]["canonical_sha256"] == FREEZE_EXPECTED["BRANCH_SELECTION_TRACE.json"])
    result["checks"]["same_byte_length"] = (
        h["BRANCH_SELECTION_TRACE.json"]["canonical_size"] == h["BRANCH_SELECTION_TRACE.json"]["fixture_size"])

    # 2. byte-level diff (my own)
    with open(os.path.join(RAW, "BRANCH_SELECTION_TRACE.json"), "rb") as f:
        rb = f.read()
    with open(os.path.join(FIXTURE, "BRANCH_SELECTION_TRACE.json"), "rb") as f:
        fb = f.read()
    positions = [i for i in range(min(len(rb), len(fb))) if rb[i] != fb[i]]
    result["byte_diff"] = {
        "canonical_len": len(rb), "fixture_len": len(fb),
        "same_length": len(rb) == len(fb),
        "changed_position_count": len(positions),
        "positions": positions,
        "contiguous": bool(positions) and positions == list(range(positions[0], positions[-1] + 1)),
    }
    # locate the single '"va": "0x00977807"' literal in the CANONICAL bytes
    lit_old = b'"va": "0x00977807"'
    lit_new = b'"va": "0xFFFFFFFF"'
    n_old = rb.count(lit_old)
    n_new = fb.count(lit_new)
    off_old = rb.find(lit_old)
    off_new = fb.find(lit_new)
    va_off = off_old + len(b'"va": "') if off_old >= 0 else None
    expected_positions = [va_off + i for i in range(10) if "0x00977807"[i] != "0xFFFFFFFF"[i]] if va_off is not None else None
    result["byte_diff"].update({
        "canonical_literal_count": n_old, "fixture_literal_count": n_new,
        "canonical_literal_offset": off_old, "fixture_literal_offset": off_new,
        "va_value_start_offset": va_off,
        "my_expected_changed_positions": expected_positions,
        "positions_exactly_the_va_value_diff_chars": positions == expected_positions,
    })

    # 3. recursive JSON leaf diff (my own flatten-based differ)
    can_doc = load(os.path.join(RAW, "BRANCH_SELECTION_TRACE.json"))
    fix_doc = load(os.path.join(FIXTURE, "BRANCH_SELECTION_TRACE.json"))
    leaf_diffs = my_leaf_diff(can_doc, fix_doc)
    result["json_leaf_diff"] = {
        "differ": "fresh-QC flatten-leaf-paths (independent implementation)",
        "changed_leaf_count": len(leaf_diffs),
        "changed_leaves": leaf_diffs,
        "exactly_one_changed_leaf": len(leaf_diffs) == 1,
        "the_leaf_is_pins74_va_old_to_new": (
            len(leaf_diffs) == 1 and leaf_diffs[0]["path"] == "pins[74].va"
            and leaf_diffs[0]["change"] == "value"
            and leaf_diffs[0]["old"] == "0x00977807"
            and leaf_diffs[0]["new"] == "0xFFFFFFFF"),
    }

    # 4. fixture pin census + identity identity with canonical (my own reader)
    raw_ids = my_input_ids(RAW)
    fix_ids = my_input_ids(FIXTURE)
    result["fixture_census"] = {
        "fixture_pin_count": len(fix_ids),
        "canonical_pin_count": len(raw_ids),
        "fixture_ids_unique": len(fix_ids) == len(set(fix_ids)),
        "identity_sets_identical": sorted(raw_ids) == sorted(fix_ids),
        "count_is_185": len(fix_ids) == 185,
    }

    # 5. payload scan: only the 4 JSON copies + FIXTURE_DIFF.json allowed
    allowed = set(ARTIFACTS) | {"FIXTURE_DIFF.json"}
    files = []
    for name in sorted(os.listdir(FIXTURE)):
        p = os.path.join(FIXTURE, name)
        if not os.path.isfile(p):
            result["payload_scan"] = {"error": "non-file entry in fixture dir", "name": name}
            break
        with open(p, "rb") as f:
            data = f.read()
        info = {
            "name": name, "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest().upper(),
            "first8_hex": data[:8].hex(),
            "nul_byte_count": data.count(b"\x00"),
            "starts_with_MZ": data[:2] == b"MZ",
            "is_allowed_name": name in allowed,
        }
        try:
            data.decode("utf-8")
            info["utf8_decodable"] = True
        except UnicodeDecodeError:
            info["utf8_decodable"] = False
        files.append(info)
    result["payload_scan"] = {
        "fixture_file_count": len(files),
        "exactly_five_files": len(files) == 5,
        "all_names_allowed": all(x["is_allowed_name"] for x in files),
        "any_MZ_header": any(x["starts_with_MZ"] for x in files),
        "any_nul_bytes": any(x["nul_byte_count"] > 0 for x in files),
        "all_utf8_text": all(x["utf8_decodable"] for x in files),
        "files": files,
        "no_exe_vfs_payload": (len(files) == 5 and all(x["is_allowed_name"] for x in files)
                              and not any(x["starts_with_MZ"] for x in files)
                              and all(x["utf8_decodable"] for x in files)
                              and all(x["size"] < 50000 for x in files)),
    }

    # 6. FIXTURE_DIFF.json executor claims vs my measurements
    fd = load(os.path.join(FIXTURE, "FIXTURE_DIFF.json"))
    result["executor_fixture_diff_claims_vs_mine"] = {
        "selector_matched_index": {"executor": fd["selector"]["matched_index"], "mine": 74},
        "byte_va_value_offset": {"executor": fd["byte_level"]["va_value_offset"], "mine": va_off},
        "byte_changed_positions": {"executor": fd["byte_level"]["changed_positions"], "mine": positions},
        "json_changed_leaf_count": {"executor": fd["json_recursive_diff"]["changed_leaf_count"],
                                    "mine": len(leaf_diffs)},
        "json_changed_leaf_path": {"executor": fd["json_recursive_diff"]["changed_leaves"][0]["path"],
                                   "mine": leaf_diffs[0]["path"] if leaf_diffs else None},
        "pre_mutation_sha_match_freeze": fd["pre_mutation_sha256"] == FREEZE_EXPECTED,
        "post_mutation_BST": {"executor": fd["post_mutation_sha256"]["BRANCH_SELECTION_TRACE.json"],
                              "mine": MUTATED_BST_EXPECTED},
        "fixture_census_per_artifact": {"executor": fd["fixture_pin_census"]["per_artifact"],
                                        "mine": {"BRANCH_SELECTION_TRACE.json": 96,
                                                 "FALLBACK_PATH_RECORD.json": 25,
                                                 "DESTINATION_PROOF_CORRECTION_R1.json": 23,
                                                 "CURSOR_PROOF_CORRECTION_R1.json": 41}},
    }

    ok = (other_three_equal
          and result["checks"]["fixture_BST_sha_matches_expected_mutated"]
          and result["checks"]["canonical_BST_sha_matches_freeze"]
          and result["checks"]["same_byte_length"]
          and result["byte_diff"]["positions_exactly_the_va_value_diff_chars"]
          and result["json_leaf_diff"]["the_leaf_is_pins74_va_old_to_new"]
          and result["fixture_census"]["identity_sets_identical"]
          and result["fixture_census"]["count_is_185"]
          and result["payload_scan"]["no_exe_vfs_payload"])
    result["overall_q4"] = ok

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
