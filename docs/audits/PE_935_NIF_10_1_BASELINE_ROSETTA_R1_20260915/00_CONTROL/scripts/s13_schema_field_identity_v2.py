#!/usr/bin/env python3
# s13_schema_field_identity_v2.py -- FIELD-IDENTITY-V2 schema census
# for PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (contract C2/C4).
#
# SUPERSEDES TOOLING BEHAVIOR of s06_world_slice_validator.py
# SchemaDecoder._fields_for (which deduplicated effective schema fields
# by bare FIELD NAME and thereby LOSED same-name occurrences, e.g.
# NiSourceTexture "File Name" x2). DOES NOT REWRITE HISTORICAL HOLDOUT
# evidence (s04/s06 bytes unchanged; s13 is new successor tooling).
#
# FIELD_IDENTITY_V2 (contract C4): a field occurrence is identified by
# (owner_type, field_name, occurrence_index, field_type, ver1, ver2,
# vercond, cond, template, schema_order). DISPLAY LABEL != SCHEMA
# FIELD IDENTITY. Never collapse occurrences by display name.
#
# What this script measures (C2):
# 1. Duplicate-name groups: every effective type (niobject chain AND
#    compound) whose version-effective field list contains >1 occurrence
#    of the same field name (NO dedup applied).
# 2. For each group: which occurrence the OLD s06 model kept
#    (first-wins unless strictly higher version-preference), which
#    occurrences it LOST, and whether the loss is LOAD-BEARING for NIF
#    10.1.0.0 (can change the applicable byte sequence for some value
#    vector / concrete type).
# 3. Classification buckets (contract C7 groups):
#    mutually-exclusive-cond / version-variants / different-owner /
#    different-template / simultaneously-active-possibility / other.
#
# Outputs:
#   01_RAW/DUPLICATE_FIELD_IDENTITY_CENSUS.csv
#   02_WORK (run-local): FIELD_IDENTITY_CENSUS_SUMMARY.json
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s04_nifxml_baseline import SchemaOracle, HIST  # noqa: E402

REPO_RAW = os.path.join(os.path.dirname(HERE), "..", "01_RAW")
WORK = (r"D:\Eudoria_Reconstruction\99_Audits"
        r"\PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916\02_WORK")

# Types physically observed in the PCG v10.1 census (from the packaged
# census CSV -- measurement columns only, provenance of the label column
# is AMEND-011 s11; we only read type_name + files here).
CENSUS_CSV = os.path.join(REPO_RAW, "ENTROPIA_NIF_10_1_TYPE_CENSUS.csv")


def load_observed():
    obs = {}
    with open(CENSUS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                files = int(row.get("files") or 0)
            except ValueError:
                files = 0
            obs[row["type_name"]] = files
    return obs


def eff_fields_v2(oracle, type_name, seen=None):
    """Occurrence-preserving effective field list (parent first).

    This is FIELD_IDENTITY_V2: NO dedup by name. Every <add>/<field>
    element in the inheritance chain appears exactly once, in schema
    order (s04.effective_fields already has this property; it is
    re-implemented here explicitly so the identity model is stated
    in the successor tool itself).
    """
    seen = seen or set()
    if type_name in seen:
        return []
    seen.add(type_name)
    o = oracle.objects.get(type_name)
    if o is None:
        return []
    fields = []
    if o["inherit"]:
        fields.extend(eff_fields_v2(oracle, o["inherit"], seen))
    for f in o["fields"]:
        fields.append((type_name, f))
    return fields


def pref(oracle, f):
    """s06 collapse preference: True(2) > None(1) > False(0)."""
    ok, _ = oracle.field_applies(f)
    return 2 if ok is True else (1 if ok is None else 0)


def old_model_survivor(oracle, occs):
    """Which occurrence would frozen s06 _fields_for keep?  Index of
    the survivor within occs, plus which indices are LOST."""
    # s06: first occurrence claims the name; a later replaces only on
    # STRICTLY higher pref.
    survivor = 0
    for i in range(1, len(occs)):
        if pref(oracle, occs[i][1]) > pref(oracle, occs[survivor][1]):
            survivor = i
    return survivor, [i for i in range(len(occs)) if i != survivor]


def classify_group(oracle, occs):
    """Classification buckets for one duplicate-name group."""
    names_owners = {o for o, _ in occs}
    types_ = {f["type"] for _, f in occs}
    conds = [f.get("cond") for _, f in occs]
    vers = [(f.get("ver1"), f.get("ver2")) for _, f in occs]
    verconds = [f.get("vercond") for _, f in occs]
    applicable = [pref(oracle, f) == 2 for _, f in occs]
    n_applicable = sum(applicable)

    buckets = []
    if len(names_owners) > 1:
        buckets.append("same name + different owner")
    if len(types_) > 1:
        buckets.append("same name + different field type")
    # version-variant bucket: occurrences that differ ONLY in version
    # gates such that at most one is applicable at 10.1
    if n_applicable <= 1 and len({(c) for c in conds if c}) <= 1 \
            and any(v != (None, None) for v in vers):
        buckets.append("same name + version variants")
    if n_applicable >= 2:
        distinct_conds = {c for c in conds if c}
        if distinct_conds and len(distinct_conds) >= 1 and \
                all(c is not None for c in conds) and len(distinct_conds) > 1:
            buckets.append("same name + mutually exclusive cond")
        else:
            buckets.append("same name + simultaneously active possibility")
    if not buckets:
        buckets.append("other")
    return buckets, n_applicable


def load_bearing(oracle, occs, survivor):
    """Is the old-model collapse load-bearing for NIF 10.1.0.0?

    Load-bearing iff >=2 occurrences are version-applicable at 10.1 AND
    the LOST occurrences can consume different bytes than the survivor
    for some value vector / concrete type: differing cond expressions,
    differing field types, differing templates, or differing array
    relations.
    """
    applicable = [(i, o, f) for i, (o, f) in enumerate(occs)
                  if pref(oracle, f) == 2]
    if len(applicable) < 2:
        return False, "at most one occurrence version-applicable at 10.1"
    lost_applicable = [i for i, _, _ in applicable if i != survivor]
    if not lost_applicable:
        return False, ("collapse keeps the only applicable occurrence"
                       " (survivor replaced an excluded twin)")
    surv_o, surv_f = occs[survivor]
    reasons = []
    for i in lost_applicable:
        o, f = occs[i]
        if f.get("cond") != surv_f.get("cond"):
            reasons.append("cond differs (%r vs %r)"
                          % (f.get("cond"), surv_f.get("cond")))
        if f["type"] != surv_f["type"]:
            reasons.append("type differs (%s vs %s)"
                           % (f["type"], surv_f["type"]))
        if (f.get("arr1") or None) != (surv_f.get("arr1") or None):
            reasons.append("array relation differs")
        if f.get("vercond") != surv_f.get("vercond"):
            reasons.append("vercond differs (%r vs %r)"
                          % (f.get("vercond"), surv_f.get("vercond")))
    if reasons:
        return True, "; ".join(sorted(set(reasons)))
    # same cond/type/arr but different template: label-level only
    templates = {f.get("template") for _, f in occs if pref(oracle, f) == 2}
    if len(templates) > 1:
        return True, "template differs among applicable occurrences"
    return False, "applicable occurrences byte-equivalent at 10.1"


def census():
    oracle = SchemaOracle(HIST, "NIFXML_HIST_0_7_1_1", "add")
    observed = load_observed()

    rows = []
    summary = {"groups": 0, "occurrences": 0, "types_with_dups": 0,
               "groups_load_bearing": 0, "load_bearing_types": [],
               "load_bearing_observed_types": [],
               "niobject_groups": 0, "compound_groups": 0}

    # census BOTH niobjects and compounds ("effective type" = both)
    all_names = set()
    for kind in ("niobject", "compound"):
        store = oracle.objects if kind == "niobject" else oracle.compounds
        for tname in store:
            all_names.add((kind, tname))

    for kind, tname in sorted(all_names):
        if kind == "niobject":
            occs = eff_fields_v2(oracle, tname)
        else:
            c = oracle.compounds.get(tname)
            if c is None:
                continue
            occs = [(tname, f) for f in c["fields"]]
        by_name = {}
        for idx, (owner, f) in enumerate(occs):
            by_name.setdefault(f["name"], []).append((idx, owner, f))
        for fname, lst in sorted(by_name.items()):
            if len(lst) < 2:
                continue
            summary["groups"] += 1
            summary["occurrences"] += len(lst)
            summary["types_with_dups"] += 1
            if kind == "niobject":
                summary["niobject_groups"] += 1
            else:
                summary["compound_groups"] += 1
            group_occs = [(o, f) for _, o, f in lst]
            survivor, lost = old_model_survivor(oracle, group_occs)
            buckets, n_app = classify_group(oracle, group_occs)
            lb, lb_reason = load_bearing(oracle, group_occs, survivor)
            if lb:
                summary["groups_load_bearing"] += 1
                summary["load_bearing_types"].append(
                    "%s:%s" % (kind, tname))
                if kind == "niobject" and tname in observed:
                    summary["load_bearing_observed_types"].append(tname)
            for occ_i, (schema_idx, owner, f) in enumerate(lst):
                ok, cond_eval = oracle.field_applies(f)
                rows.append({
                    "type_name": tname,
                    "type_kind": kind,
                    "owner_type": owner,
                    "field_name": fname,
                    "occurrence_index": occ_i,
                    "field_type": f["type"] or "",
                    "ver1": f.get("ver1") or "",
                    "ver2": f.get("ver2") or "",
                    "vercond": f.get("vercond") or "",
                    "cond": f.get("cond") or "",
                    "template": f.get("template") or "",
                    "arr1": f.get("arr1") or "",
                    "schema_order": schema_idx,
                    "version_applicable_at_10_1":
                        "TRUE" if ok is True else
                        ("UNRESOLVED" if ok is None else "FALSE"),
                    "currently_collapsed_by_s06":
                        ("SURVIVOR" if occ_i == survivor else "LOST"),
                    "group_classification": " | ".join(buckets),
                    "group_load_bearing_at_10_1":
                        "LOAD_BEARING" if lb else "NOT_LOAD_BEARING",
                    "load_bearing_reason": lb_reason if lb else "",
                    "physically_observed_in_pcg":
                        "TRUE" if (kind == "niobject"
                                   and tname in observed) else "FALSE",
                    "affected_file_count_if_known":
                        str(observed.get(tname, "")) if
                        (kind == "niobject" and tname in observed) else "",
                    "simultaneously_applicable_at_10_1":
                        "TRUE" if n_app >= 2 else "FALSE",
                })
    summary["types_with_dups"] = len({(r["type_kind"], r["type_name"])
                                      for r in rows})
    out = os.path.join(REPO_RAW, "DUPLICATE_FIELD_IDENTITY_CENSUS.csv")
    cols = ["type_name", "type_kind", "owner_type", "field_name",
            "occurrence_index", "field_type", "ver1", "ver2", "vercond",
            "cond", "template", "arr1", "schema_order",
            "version_applicable_at_10_1", "currently_collapsed_by_s06",
            "group_classification", "group_load_bearing_at_10_1",
            "load_bearing_reason", "physically_observed_in_pcg",
            "affected_file_count_if_known",
            "simultaneously_applicable_at_10_1"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    assert len(rows) == summary["occurrences"], (
        "row count != occurrence count: %d vs %d"
        % (len(rows), summary["occurrences"]))
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "FIELD_IDENTITY_CENSUS_SUMMARY.json"),
              "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))
    print("csv %s rows=%d" % (out, len(rows)))


if __name__ == "__main__":
    census()
