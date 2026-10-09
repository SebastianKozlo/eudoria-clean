#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""token_gates.py — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

Contract section 9 controls M7 (J3-standing token gate) and M8 (semantic-
promotion gate): mechanical scans over THIS RUN'S OWN output package. The
gates detect (a) restoration of the J3-superseded transform conclusion as an
ACTIVE claim, (b) WORLD_XYZ_RECOVERED=YES style assertions, (c) object
conflation (CMO+0x4C == SF+0x4C / NiNode+0x5C / m_kLocal / m_kWorld), and
(d) this-run semantic promotion of +0x44/+0x48/+0x4C to position/XYZ/world-
coordinate claims. python -B; stdlib only; read-only over the package files.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)

SCANNED_SUFFIXES = (".md", ".txt", ".csv", ".json")
SUPERSESSION_MARKERS = ("supersede", "supersession", "superseded",
                       "j3 s-5", "historical", "not qualified",
                       "not_qualified", "measured_incidental",
                       "contract section 3", "preregistration section 3")
FORBIDDEN_EQUALITIES = [
    re.compile(r"cmo\+0x4c\s*(==|is|=)\s*sf\+0x4c", re.I),
    re.compile(r"cmo\+0x4c\s*(==|is|=)\s*ninode\+0x5c", re.I),
    re.compile(r"cmo\+0x4c\s*(==|is|=)\s*m_klocal", re.I),
    re.compile(r"cmo\+0x4c\s*(==|is|=)\s*m_kworld", re.I),
]
FORBIDDEN_ACTIVE = [
    re.compile(r"WORLD_XYZ_RECOVERED\s*=\s*YES", re.I),
    re.compile(r"GLOBAL_COORDINATE_FRAME\s*=\s*(ESTABLISHED|YES)", re.I),
    re.compile(r"HISTORICAL_PLACEMENT_RECORD\s*=\s*(ESTABLISHED|YES|RECOVERED)", re.I),
    re.compile(r"INSTANCE_MODEL_JOIN\s*=\s*(ESTABLISHED|YES|CONFIRMED)", re.I),
    re.compile(r"STORES?\s+THE\s+(WORLD|GLOBAL|HISTORICAL)\s+(POSITION|XYZ|COORDINATE)", re.I),
    re.compile(r"\+0x44\s+IS\s+THE\s+(POSITION|X|Y|Z)\b", re.I),
]
TRANSFORM_ACTIVE = re.compile(
    r"SAME_INSTANCE_TRANSFORM_RELATION\s*=\s*CONFIRMED_STATIC", re.I)


def main():
    hits = {"files_scanned": [], "forbidden_active": [], "equality_conflation": [],
            "transform_active_without_supersession": [],
            "promotion_pattern_hits": []}
    for root, _dirs, files in os.walk(PKG):
        for fn in files:
            if not fn.endswith(SCANNED_SUFFIXES):
                continue
            if fn == "token_gates.py":
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, PKG)
            hits["files_scanned"].append(rel)
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                prev_lines = []  # 2-line look-back context for wrapped text
                for lineno, line in enumerate(f, 1):
                    for rx in FORBIDDEN_ACTIVE:
                        if rx.search(line):
                            hits["forbidden_active"].append(
                                {"file": rel, "line": lineno, "text": line.strip()[:160]})
                    for rx in FORBIDDEN_EQUALITIES:
                        if rx.search(line):
                            hits["equality_conflation"].append(
                                {"file": rel, "line": lineno, "text": line.strip()[:160]})
                    if TRANSFORM_ACTIVE.search(line):
                        low = line.lower()
                        if not any(m in low for m in SUPERSESSION_MARKERS):
                            hits["transform_active_without_supersession"].append(
                                {"file": rel, "line": lineno, "text": line.strip()[:160]})
                    # promotion probe: the word "position" attached to
                    # +0x44/instance/store on a line lacking any historical-
                    # context marker or explicit UNVERIFIED ceiling.
                    # Prohibition/falsifier/gate DESCRIPTIONS (e.g. the
                    # pre-registered falsifier F5 text) legitimately name
                    # the forbidden thing; they carry explicit prohibition
                    # markers and are not active claims. The probe uses a
                    # 2-line look-back context so hard-wrapped markdown
                    # cannot split a prohibition sentence from its marker
                    # (the hard gates above remain strictly single-line).
                    if re.search(r"\+0x4[48c].{0,80}position|position.{0,80}\+0x4[48c]", line, re.I):
                        context = " ".join(prev_lines[-2:] + [line]).lower()
                        markers = ("historical", "superseded", "prior", "unverified",
                                   "not promoted", "ceiling", "label", "context",
                                   "pozcja", "must not", "no promotion", "forbidden",
                                   "if this run", "falsifier", "process control",
                                   "would fail", "gate")
                        if not any(m in context for m in markers):
                            hits["promotion_pattern_hits"].append(
                                {"file": rel, "line": lineno, "text": line.strip()[:160]})
                    prev_lines.append(line)
                    if len(prev_lines) > 2:
                        prev_lines.pop(0)

    gates = {
        "M7_j3_standing_token_gate": {
            "transform_active_without_supersession_hits":
                hits["transform_active_without_supersession"],
            "PASS": len(hits["transform_active_without_supersession"]) == 0,
            "expected": "0 hits (any restoration of the superseded transform "
                        "conclusion as an ACTIVE claim would fail the gate)"},
        "M7_world_xyz_gate": {
            "forbidden_active_hits": hits["forbidden_active"],
            "PASS": len(hits["forbidden_active"]) == 0,
            "expected": "0 hits"},
        "M8_object_conflation_gate": {
            "equality_conflation_hits": hits["equality_conflation"],
            "PASS": len(hits["equality_conflation"]) == 0,
            "expected": "0 hits (CMO+0x4C must not be equated with SF+0x4C, "
                        "NiNode+0x5C, m_kLocal or m_kWorld)"},
        "M8_semantic_promotion_probe": {
            "promotion_pattern_hits": hits["promotion_pattern_hits"],
            "PASS": len(hits["promotion_pattern_hits"]) == 0,
            "expected": "0 unqualified 'position'-attached-to-+0x44/48/4C "
                        "lines (historical-context-marked mentions pass)"},
        "files_scanned_count": len(hits["files_scanned"]),
        "files_scanned": sorted(hits["files_scanned"]),
    }

    with open(os.path.join(PKG, "CONTROL_RESULTS.json"), "r",
              encoding="utf-8") as f:
        doc = json.load(f)
    doc["token_gates"] = gates
    with open(os.path.join(PKG, "CONTROL_RESULTS.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=1, sort_keys=False)

    for name, g in gates.items():
        if isinstance(g, dict):
            print(name, "PASS" if g.get("PASS") else "FAIL", g)
        else:
            print(name, g)
    all_pass = all(g.get("PASS") for g in gates.values()
                   if isinstance(g, dict))
    print("TOKEN_GATES_ALL_PASS =", all_pass)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
