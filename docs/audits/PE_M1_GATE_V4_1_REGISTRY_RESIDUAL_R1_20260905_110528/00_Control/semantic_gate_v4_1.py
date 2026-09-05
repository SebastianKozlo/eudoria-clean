#!/usr/bin/env python3
# -*- coding: ascii -*-
# semantic_gate_v4_1.py - W2 of PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528:
# THE EXTENDED SEMANTIC GATE (run-local; report -> 01_RAW\semantic_gate_report_v4_1.json).
# Extensions over the R2 gate:
#  (a) FULL-DOCUMENT WALK of the V4.1 JSON - ALL top-level keys (incl.
#      consolidation_basis, supersession, this_run_evidence, honest_limits_binding,
#      charter_five_labels, nine_fields_per_row, taxonomy) + the FULL manifest walk;
#      the typed-exempt rule UNCHANGED (records explicitly typed as
#      retraction/supersession - a dict whose record_type contains
#      SUPERSCRIPTION/RETRACTION - are the ONLY permitted carriers of the
#      retired wordings);
#  (b) NEW forbidden phrases in live fields: "reads 0.0 statically",
#      "missing: the exact RNG normalization divisor",
#      "missing: the u16->world position divisor" (+ the R2's seven, all
#      case-insensitive);
#  (c) NEW negative fixture N6 = the registry entries with the OLD missing/why
#      restored (the full pre-V4.1 state: matrix json + manifest echo + the MD
#      lines) -> FAIL; N1-N5 unchanged;
#  (d) re-execution of the WHOLE gate: clean PASS + N1-N6 ALL FAIL.
# MD-parity rule (NEW, stricter): each LIVE registry entry's missing/why fields
# are ALSO scanned as their MD-parity renderings ("missing: <value>" /
# "why: <value>") - the phrase "missing: the exact RNG normalization divisor" is
# the rendered form; typed records are exempt (the permitted carriers).
import copy
import hashlib
import json
import os
import re
import sys

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
MANIFEST = os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")
V3_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V3.json")
V3_SHA = "0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8"
OUT = os.path.join(RAW, "semantic_gate_report_v4_1.json")

FIVE = ["knowledge", "implementation", "validation", "historical_fidelity", "evidence_status"]
NINE = FIVE + ["era", "denominator", "limitations", "evidence"]
FORBIDDEN = ["32768.0 divisor", "divisor candidate", "u16/k", "rand*2.0",
             "2.0 divisor candidate", "463141+20000", "4,912,912",
             "reads 0.0 statically",                                   # NEW (V4.1)
             "missing: the exact rng normalization divisor",           # NEW (V4.1)
             "missing: the u16->world position divisor"]               # NEW (V4.1)
TYPED_EXEMPT_MARKERS = ["SUPERSESSION", "RETRACTION"]

# the pre-V4.1 registry state (the N6 fixture data - the old fields, inherited
# verbatim from the old matrix/V3; the historical open-item record now kept as
# the typed RETRACTION record in the composed entries)
OLD_ENTRIES = {
    "P-RNG-DIV": {"placeholder": "P-RNG-DIV (foliage_system)",
                  "missing": "the exact RNG normalization divisor",
                  "why": "_DAT_00a7d7a8 reads 0.0 statically (runtime-initialized)",
                  "resume_path": "runtime tracing (separate authorization)"},
    "P-POS-SCALE": {"placeholder": "P-POS-SCALE (foliage_system)",
                    "missing": "the u16->world position divisor",
                    "why": "_DAT_00a8c758 reads 0.0 statically (runtime-initialized)",
                    "resume_path": "runtime tracing"},
}
OLD_MD_LINES = {
    "P-RNG-DIV": "- **P-RNG-DIV (foliage_system)** - missing: the exact RNG normalization divisor | why: _DAT_00a7d7a8 reads 0.0 statically (runtime-initialized) | resume: runtime tracing (separate authorization)",
    "P-POS-SCALE": "- **P-POS-SCALE (foliage_system)** - missing: the u16->world position divisor | why: _DAT_00a8c758 reads 0.0 statically (runtime-initialized) | resume: runtime tracing",
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def is_typed_supersession(obj):
    rt = ""
    if isinstance(obj, dict):
        rt = str(obj.get("record_type", ""))
    return any(m in rt.upper() for m in TYPED_EXEMPT_MARKERS)


def flatten(obj):
    """the full text of a field value (string or nested record)."""
    if isinstance(obj, dict):
        return " ".join(flatten(v) for k, v in sorted(obj.items()))
    if isinstance(obj, list):
        return " ".join(flatten(v) for v in obj)
    return str(obj)


def walk_live(obj, path, exempt, hits, kind):
    """collect forbidden-phrase hits from all LIVE (non-exempt) string fields."""
    if isinstance(obj, dict):
        exempt_here = exempt or is_typed_supersession(obj)
        for k, v in obj.items():
            walk_live(v, "%s.%s" % (path, k), exempt_here, hits, kind)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_live(v, "%s[%d]" % (path, i), exempt, hits, kind)
    elif isinstance(obj, str):
        if not exempt:
            low = obj.lower()
            for p in FORBIDDEN:
                if p in low:
                    hits.append({"kind": kind, "where": path, "phrase": p,
                                 "excerpt": obj[max(0, low.find(p) - 40):low.find(p) + 60]})


def scan_matrix(matrix, tag):
    """the FULL-document scan (ALL top-level keys) + the structural + required-phrase checks."""
    hits, problems = [], []
    # (a) the full-document walk - EVERY top-level key, typed-exempt rule unchanged
    walk_live(matrix, tag, False, hits, "matrix")
    # the MD-parity rule: each LIVE registry entry's missing/why rendered as the MD does
    for i, e in enumerate(matrix.get("era_bounded_registry_v4", [])):
        if is_typed_supersession(e):
            continue  # the whole entry typed -> exempt (not the case in V4.1, but rule-complete)
        for field in ("missing", "why"):
            v = e.get(field)
            if isinstance(v, dict) and is_typed_supersession(v):
                continue  # the typed record = the permitted carrier
            rendering = "%s: %s" % (field, flatten(v))
            low = rendering.lower()
            for p in FORBIDDEN:
                if p in low:
                    hits.append({"kind": "matrix_md_parity", "where": "registry[%d].%s" % (i, field),
                                 "phrase": p, "excerpt": rendering[max(0, low.find(p) - 40):low.find(p) + 60]})
    # the P-RNG-DIV/P-POS-SCALE fields: "divisor candidate" explicitly forbidden there (flattened)
    for e in matrix.get("era_bounded_registry_v4", []):
        ph = e.get("placeholder", "")
        if ph.startswith("P-RNG-DIV") or ph.startswith("P-POS-SCALE"):
            for f in ("era_statement", "v4_status", "missing", "why", "resume_path"):
                if "divisor candidate" in flatten(e.get(f, "")).lower():
                    hits.append({"kind": "matrix", "where": "registry.%s.%s" % (ph, f),
                                 "phrase": "divisor candidate", "excerpt": flatten(e[f])[:100]})
    # structural: 19 rows x 9 fields non-vacuous
    rows = matrix.get("final_matrix_19_rows_v4", [])
    if len(rows) != 19:
        problems.append("matrix has %d rows (!= 19)" % len(rows))
    for r in rows:
        for f in NINE:
            v = r.get(f)
            if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v):
                problems.append("row %d field %s VACUOUS" % (r.get("row", "?"), f))
    # required phrases (the R2 rules, unchanged)
    by_row = {r["row"]: r for r in rows}
    if "65535.0" not in by_row[10]["knowledge"] or "float32(1/12800)" not in by_row[10]["knowledge"]:
        problems.append("ROW10 knowledge missing '65535.0' AND 'float32(1/12800)'")
    if "32767.0" not in by_row[11]["knowledge"]:
        problems.append("ROW11 knowledge missing '32767.0'")
    if "SUPERSEDED-LOCKED" not in by_row[11]["limitations"] or "32767.0" not in by_row[11]["limitations"]:
        problems.append("ROW11 limitations missing 'SUPERSEDED-LOCKED' + '32767.0'")
    lim8 = by_row[8]["limitations"]
    if "single-witness" not in lim8 or "457485" not in lim8:
        problems.append("ROW8 limitations missing 'single-witness' AND '457485'")
    reg = matrix.get("era_bounded_registry_v4", [])
    if len(reg) != 19:
        problems.append("registry has %d entries (!= 19)" % len(reg))
    for e in reg:
        if (e["placeholder"].startswith("P-RNG-DIV") or e["placeholder"].startswith("P-POS-SCALE")) \
                and "SUPERSEDED-LOCKED" not in e.get("v4_status", ""):
            problems.append("registry %s v4_status missing 'SUPERSEDED-LOCKED'" % e["placeholder"])
    # the V4.1 required composition (both entries, per the byte locks)
    rng = [e for e in reg if e["placeholder"].startswith("P-RNG-DIV")]
    pos = [e for e in reg if e["placeholder"].startswith("P-POS-SCALE")]
    for entries, const, addr in ((rng, "32767.0", "0x00a7d7a8"), (pos, "65535.0", "0x00a8c758")):
        for e in entries:
            phn = e["placeholder"].split(" ")[0]
            m = flatten(e.get("missing", "")).lower()
            if not ("composed in v4.1" in m and "none for the divisor" in m and const in m and addr in m
                    and "historical open-item record follows" in m):
                problems.append("registry %s missing: the V4.1 composed form absent (label/NONE-for-the-divisor/%s/%s/historical-record pointer)" % (phn, const, addr))
            rp = flatten(e.get("resume_path", "")).lower()
            if not ("composed in v4.1" in rp and "none for the divisor" in rp and "actual-cw" in rp):
                problems.append("registry %s resume_path: the V4.1 composed form absent" % phn)
            w = e.get("why")
            if not (isinstance(w, dict) and is_typed_supersession(w)):
                problems.append("registry %s why: NOT a typed supersession/retraction record (the retired hypothesis wording is permitted ONLY there)" % phn)
            else:
                st = flatten(w).lower()
                if not ("composed in v4.1" in st and "disproven" in st and "file-backed .rdata" in st
                        and "00 00 00 00 c0 ff df 40" in st and "00 00 00 00 e0 ff ef 40" in st):
                    problems.append("registry %s why.statement: the V4.1 disproof composition incomplete (label/DISPROVEN/file-backed .rdata/both byte patterns)" % phn)
                if "reads 0.0 statically" not in flatten(w.get("supersedes", "")).lower():
                    problems.append("registry %s why.supersedes: the retired why not carried by the typed record" % phn)
            h = e.get("historical_open_item_record")
            if not (isinstance(h, dict) and is_typed_supersession(h)):
                problems.append("registry %s historical_open_item_record: NOT a typed retraction record (the historical open-item record must follow as TYPED context, NOT live status)" % phn)
            else:
                exp = OLD_ENTRIES[phn]
                if h.get("missing") != exp["missing"] or h.get("why") != exp["why"] or h.get("resume_path") != exp["resume_path"]:
                    problems.append("registry %s historical_open_item_record: != the exact historical open-item triple" % phn)
    return hits, problems


def scan_md(md_text):
    hits, problems = [], []
    low = md_text.lower()
    for p in FORBIDDEN:
        idx = 0
        while True:
            i = low.find(p, idx)
            if i < 0:
                break
            hits.append({"kind": "md", "where": "offset %d" % i, "phrase": p,
                         "excerpt": md_text[max(0, i - 40):i + 60]})
            idx = i + 1
    # the five labels rendered per row, non-vacuous
    for m in re.finditer(r"### ROW (\d+) - ", md_text):
        row_no = int(m.group(1))
        start = m.end()
        nxt = md_text.find("### ROW ", start)
        section = md_text[start:nxt if nxt > 0 else len(md_text)]
        for label in ["KNOWLEDGE", "IMPLEMENTATION", "VALIDATION", "HISTORICAL_FIDELITY", "EVIDENCE_STATUS"]:
            mm = re.search(r"\*\*%s:?\*\*:?\s*(\S.*)" % label, section)
            if not mm or not mm.group(1).strip():
                problems.append("MD ROW %d: the %s label is missing or vacuous" % (row_no, label))
    # required phrases in the MD row sections (the R2 rules)
    def row_section(n):
        m = re.search(r"### ROW %d - " % n, md_text)
        start = m.end()
        nxt = md_text.find("### ROW ", start)
        return md_text[start:nxt if nxt > 0 else len(md_text)]
    if "65535.0" not in row_section(10) or "float32(1/12800)" not in row_section(10):
        problems.append("MD ROW10 missing the required phrases")
    if "32767.0" not in row_section(11) or "SUPERSEDED-LOCKED" not in row_section(11):
        problems.append("MD ROW11 missing the required phrases")
    lim8 = row_section(8)
    if "single-witness" not in lim8 or "457485" not in lim8:
        problems.append("MD ROW8 LIMITATIONS missing the required phrases")
    # the registry v4_status lines (the R2 rule)
    for e_label in ["P-RNG-DIV", "P-POS-SCALE"]:
        m = re.search(r"\*\*%s \(foliage_system\)\*\*.*?v4_status: (\S.*)" % e_label, md_text, re.S)
        if not m or "SUPERSEDED-LOCKED" not in m.group(1):
            problems.append("MD registry %s v4_status missing 'SUPERSEDED-LOCKED'" % e_label)
    # the V4.1 composed registry lines (the MD rendering of the composed fields)
    for e_label, const, addr in (("P-RNG-DIV", "32767.0", "@0x00A7D7A8"), ("P-POS-SCALE", "65535.0", "@0x00A8C758")):
        m = re.search(r"^- \*\*%s \(foliage_system\)\*\* - (.*)$" % e_label, md_text, re.M)
        if not m:
            problems.append("MD registry %s: the registry line missing" % e_label)
            continue
        line = m.group(1)
        for req in ("composed in V4.1", "NONE for the divisor", const, addr,
                    "the historical open-item record follows", "DISPROVEN", "file-backed .rdata",
                    "typed SUPERSESSION record", "typed RETRACTION record", "actual-CW"):
            if req not in line:
                problems.append("MD registry %s line missing the composed element %r" % (e_label, req))
    return hits, problems


def scan_manifest(manifest, matrix):
    hits, problems = [], []
    # (a) the FULL-document walk - every top-level key, typed-exempt rule unchanged
    walk_live(manifest, "manifest", False, hits, "manifest")
    # the MD-parity rule on the manifest's registry echo (identical rule to the matrix)
    for i, e in enumerate(manifest.get("era_bounded_registry_v4", [])):
        if is_typed_supersession(e):
            continue
        for field in ("missing", "why"):
            v = e.get(field)
            if isinstance(v, dict) and is_typed_supersession(v):
                continue
            rendering = "%s: %s" % (field, flatten(v))
            low = rendering.lower()
            for p in FORBIDDEN:
                if p in low:
                    hits.append({"kind": "manifest_md_parity", "where": "manifest.registry[%d].%s" % (i, field),
                                 "phrase": p, "excerpt": rendering[max(0, low.find(p) - 40):low.find(p) + 60]})
    # structural: 19 claims, the five charter fields non-vacuous
    claims = manifest.get("claims_19_rows", [])
    if len(claims) != 19:
        problems.append("manifest has %d claims (!= 19)" % len(claims))
    for c in claims:
        for f in FIVE:
            key = "evidence_status" if f == "evidence_status" else f
            if key not in c or not str(c[key]).strip():
                problems.append("manifest claim %s missing the %s field" % (c.get("claim_id"), f))
    # the V4.1 echo rule: the manifest registry echo == the matrix registry (built FROM the fields)
    if json.dumps(manifest.get("era_bounded_registry_v4"), sort_keys=True) != \
            json.dumps(matrix.get("era_bounded_registry_v4"), sort_keys=True):
        problems.append("manifest registry echo != the V4.1 matrix registry (the echo must be rebuilt from the V4.1 fields)")
    return hits, problems


def gate(matrix, md_text, manifest):
    m_hits, m_problems = scan_matrix(matrix, "matrix")
    d_hits, d_problems = scan_md(md_text)
    f_hits, f_problems = scan_manifest(manifest, matrix)
    all_hits = m_hits + d_hits + f_hits
    all_problems = m_problems + d_problems + f_problems
    verdict = "PASS" if (not all_hits and not all_problems) else "FAIL"
    return verdict, all_hits, all_problems


def restore_old(entries_list):
    """the N6 fixture: restore the OLD missing/why (the pre-V4.1 entry shape)."""
    out = []
    for e in entries_list:
        ph = e["placeholder"].split(" ")[0]
        if ph in OLD_ENTRIES:
            old = copy.deepcopy(OLD_ENTRIES[ph])
            old["era_statement"] = e["era_statement"]
            old["v4_status"] = e["v4_status"]
            out.append(old)
        else:
            out.append(copy.deepcopy(e))
    return out


def main():
    with open(V4_JSON, "r", encoding="ascii", newline="") as f:
        v4 = json.load(f)
    with open(V4_MD, "r", encoding="ascii", newline="") as f:
        md_text = f.read().replace("\r\n", "\n")
    with open(MANIFEST, "r", encoding="ascii", newline="") as f:
        manifest = json.load(f)
    v3_actual = sha256_file(V3_JSON)
    if v3_actual != V3_SHA:
        print("HARD STOP: the V3 JSON SHA mismatch (the N1 fixture source)")
        return 1
    with open(V3_JSON, "r", encoding="ascii", newline="") as f:
        v3 = json.load(f)

    # ---- the clean scan (N5)
    verdict, hits, problems = gate(v4, md_text, manifest)
    print("clean V4.1 scan: %s (hits=%d problems=%d)" % (verdict, len(hits), len(problems)))
    for h in hits:
        print("  HIT:", h)
    for p in problems:
        print("  PROBLEM:", p)

    # ---- N1: rows 8/10/11 fixture FROM THE V3 CARRIED FIELDS (unchanged from R2)
    n1 = copy.deepcopy(v4)
    v3_rows = {r["row"]: r for r in v3["final_matrix_19_rows_v3"]}
    for n in (8, 10, 11):
        n1["final_matrix_19_rows_v4"][n - 1]["knowledge"] = v3_rows[n]["carried_knowledge"]
        n1["final_matrix_19_rows_v4"][n - 1]["limitations"] = v3_rows[n]["honest_bounds"]
    n1_verdict, n1_hits, _ = gate(n1, md_text, manifest)
    print("N1 (the V3 carried fields for rows 8/10/11): %s (hits=%d)" % (n1_verdict, len(n1_hits)))
    for h in n1_hits[:6]:
        print("   ", h["where"], "->", h["phrase"])

    # ---- N2: a V4.1 copy with one section-13 field removed (unchanged from R2)
    n2 = copy.deepcopy(v4)
    del n2["final_matrix_19_rows_v4"][4]["historical_fidelity"]   # row 5
    n2_verdict, _, n2_problems = gate(n2, md_text, manifest)
    print("N2 (row 5 historical_fidelity removed): %s (problems=%d)" % (n2_verdict, len(n2_problems)))

    # ---- N3: the era_statement fixture (unchanged from R2)
    n3 = copy.deepcopy(v4)
    for e in n3["era_bounded_registry_v4"]:
        if e["placeholder"].startswith("P-RNG-DIV"):
            e["era_statement"] = "the 32768.0 divisor CANDIDATE - RNG identity confirmed, divisor labeled"
    n3_verdict, n3_hits, _ = gate(n3, md_text, manifest)
    print("N3 (the stale era_statement fixture): %s (hits=%d)" % (n3_verdict, len(n3_hits)))

    # ---- N4: a copy with a required phrase removed (unchanged from R2)
    n4 = copy.deepcopy(v4)
    n4["final_matrix_19_rows_v4"][9]["knowledge"] = \
        n4["final_matrix_19_rows_v4"][9]["knowledge"].replace("float32(1/12800)-widened", "the widened f64 constant")
    n4_verdict, _, n4_problems = gate(n4, md_text, manifest)
    print("N4 (ROW10 required phrase removed): %s (problems=%d)" % (n4_verdict, len(n4_problems)))

    # ---- N6 (NEW): the registry entries with the OLD missing/why restored - the FULL
    #      pre-V4.1 state (matrix json + manifest echo + the MD lines) -> must FAIL
    n6 = copy.deepcopy(v4)
    n6["era_bounded_registry_v4"] = restore_old(n6["era_bounded_registry_v4"])
    n6_manifest = copy.deepcopy(manifest)
    n6_manifest["era_bounded_registry_v4"] = restore_old(n6_manifest["era_bounded_registry_v4"])
    n6_md = md_text
    for label in ("P-RNG-DIV", "P-POS-SCALE"):
        n6_md = re.sub(r"^- \*\*%s \(foliage_system\)\*\* - .*$" % label,
                       lambda m, _old=OLD_MD_LINES[label]: _old, n6_md, flags=re.M)
    n6_verdict, n6_hits, n6_problems = gate(n6, n6_md, n6_manifest)
    print("N6 (the OLD missing/why restored - the full pre-V4.1 registry state): %s (hits=%d problems=%d)"
          % (n6_verdict, len(n6_hits), len(n6_problems)))
    for h in n6_hits[:12]:
        print("   ", h["kind"], h["where"], "->", h["phrase"])
    for p in n6_problems[:8]:
        print("    PROBLEM:", p)

    fixtures = {
        "N1_rows_8_10_11_from_the_V3_carried_fields": {"expected": "FAIL", "actual": n1_verdict, "hits": n1_hits[:10], "pass": n1_verdict == "FAIL"},
        "N2_one_section13_field_removed": {"expected": "FAIL", "actual": n2_verdict, "problems": n2_problems, "pass": n2_verdict == "FAIL"},
        "N3_stale_era_statement_fixture": {"expected": "FAIL", "actual": n3_verdict, "hits": n3_hits, "pass": n3_verdict == "FAIL"},
        "N4_required_phrase_removed": {"expected": "FAIL", "actual": n4_verdict, "problems": n4_problems, "pass": n4_verdict == "FAIL"},
        "N5_clean_v4_1_copy": {"expected": "PASS", "actual": verdict, "pass": verdict == "PASS"},
        "N6_old_missing_why_restored_full_pre_v4_1_state": {"expected": "FAIL", "actual": n6_verdict,
                                                            "hits": n6_hits[:16], "problems": n6_problems[:16],
                                                            "pass": n6_verdict == "FAIL"},
    }
    all_pass = verdict == "PASS" and all(f["pass"] for f in fixtures.values())
    report = {
        "run_id": "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528",
        "work_item": "W2 - the EXTENDED semantic gate (full-document walk + the new forbidden phrases + N6)",
        "scanned": {
            "v4_1_json": {"path": V4_JSON, "sha256": sha256_file(V4_JSON)},
            "v4_1_md": {"path": V4_MD, "sha256": sha256_file(V4_MD)},
            "manifest_v4_1": {"path": MANIFEST, "sha256": sha256_file(MANIFEST)},
            "v3_json_fixture_source": {"path": V3_JSON, "sha256": v3_actual},
        },
        "forbidden_phrases": FORBIDDEN,
        "forbidden_rule": ("forbidden in ALL live fields (the FULL-document walk of the V4.1 json [all top-level keys] "
                           "+ the full manifest walk + the full MD text; case-insensitive); permitted ONLY in records "
                           "explicitly typed as retraction/supersession (the registry why = the typed SUPERSESSION record; "
                           "the historical open-item record = the typed RETRACTION record; the manifest supersession_notes); "
                           "the MD-parity rule additionally scans each live registry missing/why as its MD rendering"),
        "required_rule": ("the R2 required phrases unchanged + the V4.1 composition requirements (both entries: the "
                          "'composed in V4.1' label, NONE-for-the-divisor, the byte-locked constant + address, the typed "
                          "SUPERSESSION why with the DISPROVEN/file-backed-.rdata statement + both byte patterns, the typed "
                          "RETRACTION historical open-item record with the exact old triple, the actual-CW resume_path)"),
        "clean_scan": {"verdict": verdict, "hits": hits, "problems": problems},
        "fixtures": fixtures,
        "verdict": "PASS" if all_pass else "FAIL (SEMANTIC_VIOLATION)",
        "script_sha256": sha256_file(os.path.abspath(__file__)),
    }
    with open(OUT, "w", encoding="ascii", newline="") as f:
        json.dump(report, f, indent=1)
        f.write("\n")
    print()
    print("SEMANTIC GATE (V4.1 extended):", report["verdict"])
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
