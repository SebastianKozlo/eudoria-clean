#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s13_selection_extraction_r1.py — Mechanical PE selection + fresh extraction
(Work Package C, contract section 8) for RUN_ID
PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009.

MECHANICAL SELECTION ONLY — frozen rules from 02_PE/PREREGISTRATION_PE_PHASE.md
(written BEFORE any native/deep inspection). No candidate replacement if a
selection later fails. Historical values are CALIBRATION cross-checks only.

Rules:
  (a) mandatory 218757.nif (byte identity with the pin REQUIRED).
  (b) stock-only candidate: pool = NIF 10.1.0.0 entries, version u32 inside the
      SDK gate [0x0330000B .. 0x0A020000] (=3.3.0.11..10.2.0.0), user version 0,
      whose COMPLETE declared type table is contained in the measured stock
      registry (COPY of tools/gamebryo_oracle/adapters/gb12/registry.py,
      GB12_REGISTERED_CLASSES, 198 names, zero NiArk*). 4.1.0.12/4.0.0.2 entries
      are EXCLUDED from this pool (their class tables are inline per block =
      not header-readable; no NiArk removal to manufacture a candidate).
      Rank: smallest payload, then lexicographically smallest name.
  (c) compound-scene candidates: pool = NIF 10.1.0.0 entries with >= 4 NiNode
      OBJECT references AND >= 2 NiTriShape OBJECT references (object counts
      from the header type-index histogram; NEVER type-table entry counts).
      Rank: NiNode count desc, NiTriShape count desc, payload size desc,
      name asc. Top 3. LABEL: ranks compound STRUCTURE, not proven world
      scenes.
  Dedup: 218757 excluded from pools (b)/(c); a payload is never selected twice.
  HARD MAX 5 distinct PE NIFs.

Extraction: index-proven offset/size from the pinned Models.bnt (identity
re-verified here); payloads written ONLY to this run's LOCAL_ONLY_ROOT
(02_PE_payloads/); every payload SHA256 must equal the census SHA256; 218757
must additionally equal the contract pin 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ORACLE_COPY = os.path.join(HERE, "gamebryo_oracle_r1")
sys.path.insert(0, ORACLE_COPY)
from adapters.gb12 import registry as gb12_registry  # noqa: E402

RUN_ID = "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009"
ARCHIVE = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
OUT_ROOT = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PE_OUT = os.path.join(OUT_ROOT, "02_PE")
LOCAL_ROOT = (r"D:\Eudoria_Reconstruction\99_Audits"
              r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
LOCAL_WORK = os.path.join(LOCAL_ROOT, "02_PE_work")
PAYLOAD_DIR = os.path.join(LOCAL_ROOT, "02_PE_payloads")

PIN_218757 = "3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36"
MODELS_SHA = "C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0"
V_MIN, V_MAX = 0x0330000B, 0x0A020000  # SDK gate 3.3.0.11 .. 10.2.0.0


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    os.makedirs(PAYLOAD_DIR, exist_ok=True)
    # ---- basis identities
    models_sha = sha256_file(ARCHIVE)
    if models_sha != MODELS_SHA:
        raise SystemExit("E_INPUT_HASH: Models.bnt changed vs pin")
    full_path = os.path.join(LOCAL_WORK, "per_entry_full.json")
    with open(full_path, encoding="utf-8") as f:
        histos = json.load(f)
    reg_path = os.path.join(ORACLE_COPY, "adapters", "gb12", "registry.py")
    reg_sha = sha256_file(reg_path)
    reg = set(gb12_registry.GB12_REGISTERED_CLASSES)
    if len(reg) != 198:
        raise SystemExit("E_REGISTRY_COUNT: %d" % len(reg))

    # ---- pool assembly (from the fresh census histograms)
    files_101 = [h for h in histos.values()
                 if h.get("version") == "0x0A010000"]
    user_ver_nonzero = [h for h in files_101 if h.get("user_version") != 0]
    if user_ver_nonzero:
        raise SystemExit("E_USER_VERSION: nonzero user version in 10.1 files: %d"
                         % len(user_ver_nonzero))
    histos_781 = None
    for h in histos.values():
        if h.get("entry_index") == 781:
            histos_781 = h
            break

    # name lookup map (index -> name)
    idx2name = {h["entry_index"]: n for n, h in histos.items()}

    # (b) stock-only pool
    pool_b = []
    for h in files_101:
        ver = int(h["version"], 16)
        if not (V_MIN <= ver <= V_MAX):
            continue
        unregistered = [t for t in h["block_types"] if t not in reg]
        if not unregistered:
            pool_b.append({"name": idx2name[h["entry_index"]],
                           "entry_index": h["entry_index"],
                           "size": h["size"], "offset": h["offset"],
                           "sha256_stored": h["sha256_stored"],
                           "num_blocks": h["num_blocks"],
                           "block_types": h["block_types"]})
    pool_b_4x_excluded = [h for h in histos.values()
                          if h.get("version") in ("0x0401000C", "0x04000002")]
    excluded_b_4x = len(pool_b_4x_excluded)
    # pool (b) evidence: quantify WHY the pool is empty (or not) — corpus-level
    # unregistered-type census over the complete declared tables.
    fully_registered = 0
    from collections import Counter as _C
    unreg_files_census = _C()
    for h in files_101:
        unreg = sorted(set(t for t in h["block_types"] if t not in reg))
        if not unreg:
            fully_registered += 1
        for t in unreg:
            unreg_files_census[t] += 1

    # (c) compound pool (object-reference counts, NOT table entries)
    pool_c = []
    for n, h in histos.items():
        if h.get("version") != "0x0A010000":
            continue
        tc = h.get("type_counts") or {}
        nn = tc.get("NiNode", 0)
        ts = tc.get("NiTriShape", 0)
        if nn >= 4 and ts >= 2:
            pool_c.append({"name": n, "entry_index": h["entry_index"],
                           "size": h["size"], "offset": h["offset"],
                           "sha256_stored": h["sha256_stored"],
                           "num_blocks": h["num_blocks"],
                           "NiNode_objects": nn, "NiTriShape_objects": ts})

    # ---- ranking (frozen rules)
    MANDATORY = "218757.nif"
    pool_b_sorted = sorted(pool_b, key=lambda e: (e["size"], e["name"]))
    pool_c_sorted = sorted(pool_c,
                           key=lambda e: (-e["NiNode_objects"],
                                          -e["NiTriShape_objects"],
                                          -e["size"], e["name"]))
    # dedup vs mandatory + across categories
    selected_b = None
    for e in pool_b_sorted:
        if e["name"] != MANDATORY:
            selected_b = e
            break
    already = {MANDATORY}
    if selected_b:
        already.add(selected_b["name"])
    selected_c = []
    for e in pool_c_sorted:
        if len(selected_c) >= 3:
            break
        if e["name"] in already:
            continue
        selected_c.append(e)
        already.add(e["name"])

    # ---- fresh extraction (index-proven ranges)
    def extract(name, h):
        with open(ARCHIVE, "rb") as f:
            f.seek(h["offset"])
            raw = f.read(h["size"])
        if len(raw) != h["size"]:
            raise SystemExit("E_READ: short read %s" % name)
        sha = hashlib.sha256(raw).hexdigest().upper()
        if sha != h["sha256_stored"]:
            raise SystemExit("E_SHA: %s census mismatch" % name)
        out_path = os.path.join(PAYLOAD_DIR, name)
        with open(out_path, "wb") as f:
            f.write(raw)
        return {"payload_local_only_path": out_path,
                "payload_size_bytes": len(raw), "payload_sha256": sha,
                "byte_identity_vs_census": sha == h["sha256_stored"]}

    # mandatory 218757
    h218757 = histos.get("218757.nif")
    if h218757 is None:
        raise SystemExit("E_MISSING_218757")
    ext_a = extract("218757.nif", h218757)
    ext_a["byte_identity_vs_contract_pin"] = (
        ext_a["payload_sha256"] == PIN_218757)
    if not ext_a["byte_identity_vs_contract_pin"]:
        raise SystemExit("E_PIN: 218757 fresh extraction != contract pin")

    sel_b = None
    if selected_b:
        hb = histos[selected_b["name"]]
        sel_b = dict(selected_b)
        sel_b.update(extract(selected_b["name"], hb))
        if not sel_b:
            raise SystemExit("E_B")
    sel_c = []
    for e in selected_c:
        hc = histos[e["name"]]
        s = dict(e)
        s.update(extract(e["name"], hc))
        sel_c.append(s)

    result = {
        "run_id": RUN_ID,
        "stage": "S13_selection_and_extraction",
        "selection_frozen_before_native_or_deep_inspection": True,
        "rules_source": "02_PE/PREREGISTRATION_PE_PHASE.md sections 3 (written "
                        "before this script ran)",
        "basis": {
            "models_bnt": {"path": ARCHIVE, "sha256_reverified": models_sha,
                           "pin_match": models_sha == MODELS_SHA},
            "census": {"csv": "02_PE/CORPUS_METADATA_CENSUS.csv",
                       "full_histograms_local_only":
                           os.path.join(LOCAL_WORK, "per_entry_full.json")},
            "stock_registry": {
                "identity": "COPY of tools/gamebryo_oracle/adapters/gb12/"
                            "registry.py (canonical READ_ONLY); copy path "
                            "TOOLS/gamebryo_oracle_r1/adapters/gb12/registry.py",
                "copy_sha256": reg_sha,
                "registered_class_count": len(reg),
                "niark_present": sorted(t for t in reg if "Ark" in t)},
        },
        "pools": {
            "mandatory": {"name": MANDATORY, "entry_index": 781,
                          "size": h218757["size"],
                          "offset": h218757["offset"],
                          "sha256_stored": h218757["sha256_stored"]},
            "stock_only_pool": {
                "definition": "NIF 10.1.0.0, SDK version gate "
                              "[3.3.0.11..10.2.0.0], user version 0, COMPLETE "
                              "declared type table subset of "
                              "GB12_REGISTERED_CLASSES",
                "pool_size": len(pool_b),
                "fully_registered_tables_in_10_1_corpus": fully_registered,
                "unregistered_type_census_10_1_corpus": {
                    "note": "files declaring each unregistered type name at "
                            "least once in their COMPLETE declared table",
                    "types": [{"name": t, "declared_by_files": c}
                              for t, c in sorted(unreg_files_census.items(),
                                                key=lambda kv: -kv[1])]},
                "excluded_4x_entries_no_header_readable_table": excluded_b_4x,
                "ranked_shortlist_top10": [
                    {"name": e["name"], "entry_index": e["entry_index"],
                     "size": e["size"], "num_blocks": e["num_blocks"],
                     "block_types": e["block_types"]}
                    for e in pool_b_sorted[:10]],
            },
            "compound_pool": {
                "definition": "NIF 10.1.0.0, NiNode objects >= 4 AND "
                              "NiTriShape objects >= 2 (type-index histogram "
                              "object counts; type-table entries NEVER used "
                              "as object counts)",
                "pool_size": len(pool_c),
                "label": "ranks compound STRUCTURE, not proven world scenes",
                "ranked_shortlist_full": [
                    {"rank": i + 1, "name": e["name"],
                     "entry_index": e["entry_index"], "size": e["size"],
                     "num_blocks": e["num_blocks"],
                     "NiNode_objects": e["NiNode_objects"],
                     "NiTriShape_objects": e["NiTriShape_objects"]}
                    for i, e in enumerate(pool_c_sorted[:40])],
            },
        },
        "selection": {
            "a_mandatory_218757": {
                "name": "218757.nif", "entry_index": 781,
                "container": ARCHIVE,
                "index_range": {"offset": h218757["offset"],
                                "size": h218757["size"]},
                **ext_a},
            "b_stock_only_candidate": (
                {"name": sel_b["name"], "entry_index": sel_b["entry_index"],
                 "container": ARCHIVE,
                 "index_range": {"offset": histos[sel_b["name"]]["offset"],
                                 "size": histos[sel_b["name"]]["size"]},
                 "declared_block_types": sel_b["block_types"],
                 "all_types_registered_in_stock_registry": True,
                 "payload_size_bytes": sel_b["payload_size_bytes"],
                 "payload_sha256": sel_b["payload_sha256"],
                 "payload_local_only_path": sel_b["payload_local_only_path"],
                 "byte_identity_vs_census": sel_b["byte_identity_vs_census"]}
                if sel_b else "NO_STOCK_ONLY_CANDIDATE"),
            "c_compound_candidates": [
                {"name": s["name"], "entry_index": s["entry_index"],
                 "container": ARCHIVE,
                 "index_range": {"offset": histos[s["name"]]["offset"],
                                 "size": histos[s["name"]]["size"]},
                 "NiNode_objects": s["NiNode_objects"],
                 "NiTriShape_objects": s["NiTriShape_objects"],
                 "num_blocks": s["num_blocks"],
                 "payload_size_bytes": s["payload_size_bytes"],
                 "payload_sha256": s["payload_sha256"],
                 "payload_local_only_path": s["payload_local_only_path"],
                 "byte_identity_vs_census": s["byte_identity_vs_census"],
                 "classification_label": "compound-scene STRUCTURE candidate "
                                        "(not a proven world scene)"}
                for s in sel_c],
            "hard_max_distinct_nifs": 5,
            "distinct_selected": 1 + (1 if sel_b else 0) + len(sel_c),
            "deduplication_applied": sorted(already),
        },
        "provenance_discipline": ("All extracted payload bytes are LOCAL_ONLY "
                                 "(never committed); each carries "
                                 "container/index/range/size/SHA256 "
                                 "provenance."),
    }
    out = os.path.join(PE_OUT, "SELECTION_AND_EXTRACTION_PROVENANCE.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({
        "stock_only_pool_size": len(pool_b),
        "compound_pool_size": len(pool_c),
        "selected_b": (sel_b["name"] if sel_b else "NO_STOCK_ONLY_CANDIDATE"),
        "selected_c": [(s["name"], s["NiNode_objects"], s["NiTriShape_objects"])
                        for s in sel_c],
        "distinct_selected": result["selection"]["distinct_selected"],
        "218757_pin_identity": ext_a["byte_identity_vs_contract_pin"],
    }, indent=2))


if __name__ == "__main__":
    main()
