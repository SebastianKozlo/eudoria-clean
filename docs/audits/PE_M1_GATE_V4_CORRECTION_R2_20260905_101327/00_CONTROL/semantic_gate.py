#!/usr/bin/env python3
# -*- coding: ascii -*-
# semantic_gate.py - W8: THE SEMANTIC GATE (run-local; report in 01_RAW).
# Scans ALL live fields of the V4 JSON (9 fields x 19 rows; registry: v4_status
# + era_statement + missing/why/resume_path; known_open) + the V4 MD + the V4
# manifest. FORBIDDEN phrases (permitted ONLY in records explicitly typed as
# retraction/supersession): "32768.0 divisor", "divisor candidate" (in the
# P-RNG-DIV/P-POS-SCALE fields - additionally forbidden in ALL live fields,
# the strictest reading), "u16/K", "rand*2.0", "2.0 divisor CANDIDATE",
# "463141+20000", "4,912,912". REQUIRED phrases: ROW10 -> "65535.0" AND
# "float32(1/12800)"; ROW11 -> "32767.0" AND "SUPERSEDED-LOCKED"; ROW8
# LIMITATIONS -> "single-witness" AND "457485"; registry P-RNG-DIV/P-POS-SCALE
# v4_status -> "SUPERSEDED-LOCKED"; the five section-13 fields non-vacuous
# x 19 rows in BOTH formats. NEGATIVE FIXTURES (fail-closed proof): N1 the
# rows-8/10/11 fixture FROM THE V3 CARRIED FIELDS -> FAIL; N2 a V4 copy with
# one section-13 field removed -> FAIL; N3 the era_statement fixture
# "the 32768.0 divisor CANDIDATE" -> FAIL; N4 a copy with a required phrase
# removed -> FAIL; N5 the clean V4 copy -> PASS. NON-PASS = SEMANTIC_VIOLATION
# with every hit printed.
import copy
import hashlib
import json
import os
import sys

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
MANIFEST = os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")
V3_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V3.json")
V3_SHA = "0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8"
OUT = os.path.join(RUN_ROOT, "01_RAW", "semantic_gate_report.json")

FIVE = ["knowledge", "implementation", "validation", "historical_fidelity", "evidence_status"]
NINE = FIVE + ["era", "denominator", "limitations", "evidence"]
FORBIDDEN = ["32768.0 divisor", "divisor candidate", "u16/k", "rand*2.0",
             "2.0 divisor candidate", "463141+20000", "4,912,912"]
TYPED_EXEMPT_MARKERS = ["SUPERSESSION", "RETRACTION"]


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


def walk_live(obj, path, exempt, hits, phrases, kind):
    """collect forbidden-phrase hits from all LIVE (non-exempt) string fields."""
    if isinstance(obj, dict):
        exempt_here = exempt or is_typed_supersession(obj)
        for k, v in obj.items():
            walk_live(v, "%s.%s" % (path, k), exempt_here, hits, phrases, kind)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_live(v, "%s[%d]" % (path, i), exempt, hits, phrases, kind)
    elif isinstance(obj, str):
        if not exempt:
            low = obj.lower()
            for p in phrases:
                if p in low:
                    hits.append({"kind": kind, "where": path, "phrase": p,
                                 "excerpt": obj[max(0, low.find(p) - 40):low.find(p) + 60]})


def scan_matrix(matrix, tag):
    hits = []
    problems = []
    # forbidden phrases in ALL live fields of the matrix (the matrix has NO typed records)
    walk_live(matrix.get("final_matrix_19_rows_v4", []), "rows", False, hits, FORBIDDEN, "matrix")
    walk_live(matrix.get("era_bounded_registry_v4", []), "registry", False, hits, FORBIDDEN, "matrix")
    walk_live(matrix.get("known_open_list_v4", []), "known_open", False, hits, FORBIDDEN, "matrix")
    for k in ("deliverable", "milestone", "created_by", "scope_statement", "corrections_applied_this_run"):
        if k in matrix:
            walk_live(matrix[k], k, False, hits, FORBIDDEN, "matrix")
    # the P-RNG-DIV/P-POS-SCALE registry fields: "divisor candidate" explicitly forbidden there
    for e in matrix.get("era_bounded_registry_v4", []):
        ph = e["placeholder"]
        if ph.startswith("P-RNG-DIV") or ph.startswith("P-POS-SCALE"):
            for f in ("era_statement", "v4_status", "missing", "why", "resume_path"):
                if "divisor candidate" in e.get(f, "").lower():
                    hits.append({"kind": "matrix", "where": "registry.%s.%s" % (ph, f), "phrase": "divisor candidate", "excerpt": e[f][:100]})
    # structural: 19 rows x 9 fields non-vacuous
    rows = matrix.get("final_matrix_19_rows_v4", [])
    if len(rows) != 19:
        problems.append("matrix has %d rows (!= 19)" % len(rows))
    for r in rows:
        for f in NINE:
            v = r.get(f)
            if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v):
                problems.append("row %d field %s VACUOUS" % (r.get("row", "?"), f))
    # required phrases
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
    for e in matrix.get("era_bounded_registry_v4", []):
        if (e["placeholder"].startswith("P-RNG-DIV") or e["placeholder"].startswith("P-POS-SCALE")) \
                and "SUPERSEDED-LOCKED" not in e["v4_status"]:
            problems.append("registry %s v4_status missing 'SUPERSEDED-LOCKED'" % e["placeholder"])
    return hits, problems


def scan_md(md_text):
    hits = []
    problems = []
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
    import re
    for m in re.finditer(r"### ROW (\d+) - ", md_text):
        row_no = int(m.group(1))
        start = m.end()
        nxt = md_text.find("### ROW ", start)
        section = md_text[start:nxt if nxt > 0 else len(md_text)]
        for label in ["KNOWLEDGE", "IMPLEMENTATION", "VALIDATION", "HISTORICAL_FIDELITY", "EVIDENCE_STATUS"]:
            pat = r"\*\*%s:?\*\*:?\s*(\S.*)" % label
            mm = re.search(pat, section)
            if not mm or not mm.group(1).strip():
                problems.append("MD ROW %d: the %s label is missing or vacuous" % (row_no, label))
    # required phrases in the MD row sections
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
    for e_label in ["P-RNG-DIV", "P-POS-SCALE"]:
        m = re.search(r"\*\*%s \(foliage_system\)\*\*.*?v4_status: (\S.*)" % e_label, md_text, re.S)
        if not m or "SUPERSEDED-LOCKED" not in m.group(1):
            problems.append("MD registry %s v4_status missing 'SUPERSEDED-LOCKED'" % e_label)
    return hits, problems


def scan_manifest(manifest):
    hits = []
    problems = []
    # everything EXCEPT the explicitly-typed supersession records is live
    live = {k: v for k, v in manifest.items() if k not in ("supersession_notes", "supersession")}
    walk_live(live, "manifest", False, hits, FORBIDDEN, "manifest")
    walk_live(manifest.get("supersession", {}), "manifest.supersession", False, hits, FORBIDDEN, "manifest")
    # the supersession_notes records ARE typed -> exempt (the only permitted
    # carriers); their carried phrases are collected informationally below
    claims = manifest.get("claims_19_rows", [])
    if len(claims) != 19:
        problems.append("manifest has %d claims (!= 19)" % len(claims))
    for c in claims:
        for f in FIVE:
            key = "evidence_status" if f == "evidence_status" else f
            if key not in c or not str(c[key]).strip():
                problems.append("manifest claim %s missing the %s field" % (c.get("claim_id"), f))
    # informational: the forbidden phrases legitimately carried by the TYPED
    # supersession records (the ONLY permitted carriers)
    permitted = []
    def _collect(obj, path):
        if isinstance(obj, dict):
            if is_typed_supersession(obj):
                walk_strings(obj, path, permitted)
                return
            for k, v in obj.items():
                _collect(v, "%s.%s" % (path, k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _collect(v, "%s[%d]" % (path, i))
    def walk_strings(obj, path, sink):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk_strings(v, "%s.%s" % (path, k), sink)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk_strings(v, "%s[%d]" % (path, i), sink)
        elif isinstance(obj, str):
            low = obj.lower()
            for p in FORBIDDEN:
                if p in low:
                    sink.append({"where": path, "phrase": p})
    _collect(manifest.get("supersession_notes", []), "manifest.supersession_notes")
    return hits, problems, permitted


def gate(matrix, md_text, manifest):
    m_hits, m_problems = scan_matrix(matrix, "matrix")
    d_hits, d_problems = scan_md(md_text)
    f_hits, f_problems, exempt = scan_manifest(manifest)
    all_hits = m_hits + d_hits + f_hits
    all_problems = m_problems + d_problems + f_problems
    verdict = "PASS" if (not all_hits and not all_problems) else "FAIL"
    return verdict, all_hits, all_problems, exempt


def main():
    with open(V4_JSON, "r", encoding="ascii") as f:
        v4 = json.load(f)
    with open(V4_MD, "r", encoding="ascii") as f:
        md_text = f.read()
    with open(MANIFEST, "r", encoding="ascii") as f:
        manifest = json.load(f)
    v3_actual = sha256_file(V3_JSON)
    if v3_actual != V3_SHA:
        print("HARD STOP: the V3 JSON SHA mismatch (the N1 fixture source)")
        return 1
    with open(V3_JSON, "r", encoding="ascii") as f:
        v3 = json.load(f)

    # ---- the clean scan (N5)
    verdict, hits, problems, exempt = gate(v4, md_text, manifest)
    print("clean V4 scan: %s (hits=%d problems=%d; typed-exempt carriers=%d)"
          % (verdict, len(hits), len(problems), len(exempt)))
    for h in hits:
        print("  HIT:", h)
    for p in problems:
        print("  PROBLEM:", p)

    # ---- N1: rows 8/10/11 fixture FROM THE V3 CARRIED FIELDS
    n1 = copy.deepcopy(v4)
    v3_rows = {r["row"]: r for r in v3["final_matrix_19_rows_v3"]}
    for n in (8, 10, 11):
        n1["final_matrix_19_rows_v4"][n - 1]["knowledge"] = v3_rows[n]["carried_knowledge"]
        n1["final_matrix_19_rows_v4"][n - 1]["limitations"] = v3_rows[n]["honest_bounds"]
    n1_verdict, n1_hits, n1_problems, _ = gate(n1, md_text, manifest)
    print("N1 (the V3 carried fields for rows 8/10/11): %s (hits=%d)" % (n1_verdict, len(n1_hits)))
    for h in n1_hits[:6]:
        print("   ", h["where"], "->", h["phrase"])

    # ---- N2: a V4 copy with one section-13 field removed
    n2 = copy.deepcopy(v4)
    del n2["final_matrix_19_rows_v4"][4]["historical_fidelity"]   # row 5
    n2_verdict, n2_hits, n2_problems, _ = gate(n2, md_text, manifest)
    print("N2 (row 5 historical_fidelity removed): %s (problems=%d)" % (n2_verdict, len(n2_problems)))

    # ---- N3: the era_statement fixture
    n3 = copy.deepcopy(v4)
    for e in n3["era_bounded_registry_v4"]:
        if e["placeholder"].startswith("P-RNG-DIV"):
            e["era_statement"] = "the 32768.0 divisor CANDIDATE - RNG identity confirmed, divisor labeled"
    n3_verdict, n3_hits, _, _ = gate(n3, md_text, manifest)
    print("N3 (the stale era_statement fixture): %s (hits=%d)" % (n3_verdict, len(n3_hits)))

    # ---- N4: a copy with a required phrase removed
    n4 = copy.deepcopy(v4)
    n4["final_matrix_19_rows_v4"][9]["knowledge"] = \
        n4["final_matrix_19_rows_v4"][9]["knowledge"].replace("float32(1/12800)-widened", "the widened f64 constant")
    n4_verdict, n4_hits, n4_problems, _ = gate(n4, md_text, manifest)
    print("N4 (ROW10 required phrase removed): %s (problems=%d)" % (n4_verdict, len(n4_problems)))

    fixtures = {
        "N1_rows_8_10_11_from_the_V3_carried_fields": {"expected": "FAIL", "actual": n1_verdict, "hits": n1_hits[:10], "pass": n1_verdict == "FAIL"},
        "N2_one_section13_field_removed": {"expected": "FAIL", "actual": n2_verdict, "problems": n2_problems, "pass": n2_verdict == "FAIL"},
        "N3_stale_era_statement_fixture": {"expected": "FAIL", "actual": n3_verdict, "hits": n3_hits, "pass": n3_verdict == "FAIL"},
        "N4_required_phrase_removed": {"expected": "FAIL", "actual": n4_verdict, "problems": n4_problems, "pass": n4_verdict == "FAIL"},
        "N5_clean_v4_copy": {"expected": "PASS", "actual": verdict, "pass": verdict == "PASS"},
    }
    all_pass = verdict == "PASS" and all(f["pass"] for f in fixtures.values())
    report = {
        "run_id": "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327",
        "work_item": "W8 - the semantic gate",
        "scanned": {
            "v4_json": {"path": V4_JSON, "sha256": sha256_file(V4_JSON)},
            "v4_md": {"path": V4_MD, "sha256": sha256_file(V4_MD)},
            "manifest_v4": {"path": MANIFEST, "sha256": sha256_file(MANIFEST)},
            "v3_json_fixture_source": {"path": V3_JSON, "sha256": v3_actual},
        },
        "forbidden_phrases": FORBIDDEN,
        "forbidden_rule": "forbidden in ALL live fields; permitted ONLY in records explicitly typed as retraction/supersession (the manifest's supersession_notes records; the matrix + MD carry none)",
        "typed_exempt_carriers_observed": exempt,
        "clean_scan": {"verdict": verdict, "hits": hits, "problems": problems},
        "fixtures": fixtures,
        "verdict": "PASS" if all_pass else "FAIL (SEMANTIC_VIOLATION)",
        "script_sha256": sha256_file(os.path.abspath(__file__)),
    }
    with open(OUT, "w", encoding="ascii") as f:
        json.dump(report, f, indent=1)
        f.write("\n")
    print()
    print("SEMANTIC GATE:", report["verdict"])
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
