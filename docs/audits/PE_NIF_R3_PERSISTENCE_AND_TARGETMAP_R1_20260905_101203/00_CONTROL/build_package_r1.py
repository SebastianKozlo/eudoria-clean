#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_package_r1.py — PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1 driver.

Phases (argv[1]): hash | verify | index
  hash   — compute SHA256 of THIS driver + map_defs.py, write
           00_CONTROL/SHA256_DRIVER.txt (run once after the LAST edit of both
           files; verify/index re-verify the hashes before doing anything).
  verify — machine-verify the TARGET_MAP old fragments (each must occur EXACTLY
           ONCE in its target file, newline-aware with CRLF adaptation), the
           new-text verbatim checks (whitespace-normalized substrings of the
           hash-pinned R3 proposal), the P1R2-5-R3 two-segment join check, the
           P2/P3 fixed-text extraction + forbidden-clause checks, the docs/nif
           contradiction census (every occurrence, current line numbers), the
           review-citation line verification, the R3-package unmodified re-hash
           (all rows of the R3 artifact_index.csv), and the docs/nif state
           snapshot. Writes 05_ANALYSIS/TARGET_MAP.json +
           05_ANALYSIS/CONTRADICTION_CENSUS.json. Exit 1 on any failure.
  index  — re-verify driver+defs hashes vs SHA256_DRIVER.txt, re-verify docs/nif
           unchanged (vs the census snapshot) and the R3 package unchanged,
           then compute REAL SHA-256 of every package artifact and write
           artifact_index.csv. THE MANIFEST EXCLUDES ITSELF (documented
           precedent; the exclusion is recorded in REPORT.md/HANDOFF.md).
           Exit 1 on any failure.

GOVERNANCE: reads the R3/R2 historical runs and docs/nif READ-ONLY. Writes ONLY
inside RUN_ROOT. No docs/nif application, no wiki writes, no repo writes, no
modification of any historical run.
"""
import csv
import datetime
import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_defs as D  # noqa: E402

RUN_ROOT = D.RUN_ROOT
PROMPT_MD = os.path.join(RUN_ROOT, "00_CONTROL", "NEXT_PROMPT.md")
DRIVER_PY = os.path.join(RUN_ROOT, "00_CONTROL", "build_package_r1.py")
DEFS_PY = os.path.join(RUN_ROOT, "00_CONTROL", "map_defs.py")
DRIVER_TXT = os.path.join(RUN_ROOT, "00_CONTROL", "SHA256_DRIVER.txt")
PROPOSAL_MD = os.path.join(D.R3_ROOT, "06_REPORT", "PROPOSED_DOC_CORRECTIONS_R3.md")
PROPOSAL_FIXED_MD = os.path.join(RUN_ROOT, "06_REPORT", "PROPOSALS_P2P3_FIXED.md")
TARGET_MAP_JSON = os.path.join(RUN_ROOT, "05_ANALYSIS", "TARGET_MAP.json")
CENSUS_JSON = os.path.join(RUN_ROOT, "05_ANALYSIS", "CONTRADICTION_CENSUS.json")
ARTIFACT_INDEX_CSV = os.path.join(RUN_ROOT, "artifact_index.csv")

FAILURES = []


def fail(msg):
    FAILURES.append(msg)
    print("FAIL: " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8")


def write_text(path, s):
    with open(path, "wb") as f:
        f.write(s.encode("utf-8"))


def norm(s):
    return " ".join(s.split())


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def count_fragment(text, frag):
    """Newline-aware count. Returns (lf, crlf, variant, hits)."""
    lf = text.count(frag)
    crlf = text.count(frag.replace("\n", "\r\n")) if "\n" in frag else lf
    if lf and not crlf:
        v, h = "LF", lf
    elif crlf and not lf:
        v, h = "CRLF", crlf
    else:
        v, h = ("LF+CRLF", lf) if lf == crlf else ("MIXED", lf + crlf)
    return lf, crlf, v, h


def frag_lines(text, frag):
    for variant in (frag, frag.replace("\n", "\r\n")):
        i = text.find(variant)
        if i >= 0:
            return line_of(text, i), line_of(text, i + len(variant) - 1)
    return None


def census_build(text):
    out, idx = [], []
    i, n = 0, len(text)
    while i < n:
        if text[i].isspace():
            j = i
            while j < n and text[j].isspace():
                j += 1
            out.append(" ")
            idx.append(i)
            i = j
        else:
            out.append(text[i])
            idx.append(i)
            i += 1
    return "".join(out), idx


def census_find(ntext, idx, orig, pattern):
    hits, start = [], 0
    pn = norm(pattern)
    while True:
        m = ntext.find(pn, start)
        if m < 0:
            break
        o_s, o_e = idx[m], idx[m + len(pn) - 1]
        ls, le = line_of(orig, o_s), line_of(orig, o_e)
        raw = orig[o_s:o_e + 1].replace("\r\n", " ").replace("\n", " ")
        hits.append({"line_start": ls, "line_end": le,
                     "excerpt": (raw[:240] + "...") if len(raw) > 240 else raw})
        start = m + len(pn)
    return hits


def extract_marker(md_text, marker):
    s = "<!-- EXTRACT:%s:START -->" % marker
    e = "<!-- EXTRACT:%s:END -->" % marker
    i = md_text.index(s) + len(s)
    j = md_text.index(e)
    return md_text[i:j].strip()


def extract_p1_new(proposal_text):
    lines = proposal_text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("## P1R2-5-R3"))
    buf, in_new = [], False
    for l in lines[start + 1:]:
        if not in_new:
            if l.startswith("- NEW: \""):
                buf.append(l[len('- NEW: "'):])
                in_new = True
        else:
            if l.rstrip().endswith("\""):
                buf.append(l.rstrip()[:-1])
                break
            buf.append(l)
    return "\n".join(buf)


def r3_rehash():
    """Re-hash every artifact listed in the R3 manifest; return stats."""
    rows = list(csv.DictReader(open(os.path.join(D.R3_ROOT, "artifact_index.csv"),
                                    encoding="utf-8")))
    ok = 0
    bad = []
    for r in rows:
        p = r["source_path_full"]
        try:
            h = sha256_file(p)
            sz = os.path.getsize(p)
        except OSError as ex:
            bad.append((p, "unreadable: %s" % ex))
            continue
        if h == r["sha256"].lower() and sz == int(r["size_bytes"]):
            ok += 1
        else:
            bad.append((p, "hash/size mismatch"))
    return {"rows_checked": len(rows), "matches": ok, "mismatches": bad}


def docs_state():
    files = sorted(glob.glob(os.path.join(D.DOCS_NIF, "**", "*.md"), recursive=True))
    state = {}
    for p in files:
        t = read_text(p)
        state[p] = {"sha256": sha256_file(p), "size_bytes": os.path.getsize(p),
                    "lines": t.count("\n") + 1,
                    "line_ending": "CRLF" if "\r\n" in t else "LF"}
    return state


# --------------------------------------------------------------------------- hash
def phase_hash():
    h_drv, h_defs = sha256_file(DRIVER_PY), sha256_file(DEFS_PY)
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    txt = (
        "SHA256_DRIVER — %s\r\n"
        "policy: both scripts hashed AFTER THEIR LAST EDIT, BEFORE FIRST EXECUTION;\r\n"
        "the verify and index phases re-verify these hashes and abort on change.\r\n"
        "recorded (UTC-local): %s\r\n"
        "00_CONTROL\\build_package_r1.py  SHA256 = %s\r\n"
        "00_CONTROL\\map_defs.py         SHA256 = %s\r\n"
    ) % (D.RUN_ID, ts, h_drv, h_defs)
    write_text(DRIVER_TXT, txt)
    print("SHA256_DRIVER.txt written. driver=%s defs=%s" % (h_drv, h_defs))


# ------------------------------------------------------------------------- verify
def phase_verify():
    results = {"gates": {}, "failures": list(FAILURES)}
    p_sha = sha256_file(PROMPT_MD)
    results["gates"]["prompt_sha256"] = p_sha
    if p_sha != D.EXPECTED_PROMPT_SHA256:
        fail("prompt SHA mismatch: %s" % p_sha)
    pr_sha = sha256_file(PROPOSAL_MD)
    results["gates"]["proposal_sha256"] = pr_sha
    if pr_sha != D.EXPECTED_PROPOSAL_SHA256:
        fail("proposal SHA mismatch: %s" % pr_sha)

    drv_txt = read_text(DRIVER_TXT)
    results["gates"]["driver_sha256"] = sha256_file(DRIVER_PY)
    results["gates"]["map_defs_sha256"] = sha256_file(DEFS_PY)
    if sha256_file(DRIVER_PY) not in drv_txt or sha256_file(DEFS_PY) not in drv_txt:
        fail("driver/defs hash not recorded in SHA256_DRIVER.txt (run hash phase first)")

    proposal = read_text(PROPOSAL_MD)
    proposal_n = norm(proposal)
    fixed_md = read_text(PROPOSAL_FIXED_MD)
    fixed_p2 = extract_marker(fixed_md, "P2R2-2-R3-FIXED")
    fixed_p3_1 = extract_marker(fixed_md, "P3R3-FIXED-1")
    fixed_p3_3 = extract_marker(fixed_md, "P3R3-FIXED-3")

    # --- fixed-text checks ----------------------------------------------------
    fx = {}
    fx["p2_removed_clause_absent"] = D.P2_REMOVED_CLAUSE not in norm(fixed_p2)
    fx["p2_contains_partial_fit"] = "C-MORPH-1 is a PARTIAL-FIT claim" in norm(fixed_p2)
    fx["p2_contains_ascii_presence"] = "3 files / 29 occurrences" in norm(fixed_p2)
    fx["p2_contains_no_untested"] = "No claim is made about untested claims" in norm(fixed_p2)
    fx["p3fix1_head_in_proposal"] = norm(D.P3FIX1_HEAD) in proposal_n
    fx["p3fix1_removed_absent"] = (D.P3_REMOVED_CLAUSE not in norm(fixed_p3_1)
                                   and D.P3_REMOVED_CLAUSE2 not in norm(fixed_p3_1))
    fx["p3fix1_contains_demonstrated"] = "DEMONSTRATED insensitive" in norm(fixed_p3_1)
    fx["p3fix3_head_in_proposal"] = norm(D.P3FIX3_HEAD) in proposal_n
    fx["p3fix3_removed_absent"] = (D.P3_REMOVED_CLAUSE not in norm(fixed_p3_3)
                                   and D.P3_REMOVED_CLAUSE2 not in norm(fixed_p3_3))
    fx["p3fix3_contains_demonstrated"] = "DEMONSTRATED insensitive" in norm(fixed_p3_3)
    for k, v in fx.items():
        if not v:
            fail("fixed-text check failed: %s" % k)
    results["fixed_text_checks"] = fx

    # --- verbatim new-text checks --------------------------------------------
    vt = {}
    vt["NEW_P1A_in_proposal"] = norm(D.NEW_P1A).rstrip("]") in proposal_n
    vt["NEW_P1B_in_proposal"] = norm(D.NEW_P1B).lstrip("[") in proposal_n
    for name in ("NEW_P3B", "NEW_P4A", "NEW_P4B", "NEW_P4C", "NEW_P5A", "NEW_P5B"):
        vt[name + "_in_proposal"] = norm(getattr(D, name)) in proposal_n
    p1_full = norm(extract_p1_new(proposal))
    join = norm(D.NEW_P1A).rstrip("]") + " " + norm(D.NEW_P1B).lstrip("[")
    vt["P1_segment_join_equals_full_NEW"] = (join == p1_full and p1_full.endswith("]")
                                            and p1_full.startswith("["))
    for k, v in vt.items():
        if not v:
            fail("verbatim check failed: %s" % k)
    results["verbatim_checks"] = vt

    # --- old-fragment exactly-once checks ------------------------------------
    target_cache = {}
    frag_stats = []
    proposals_out = []
    for prop in D.MAP_PROPOSALS:
        prop_out = {k: v for k, v in prop.items() if k != "edits"}
        edits_out = []
        for ed in prop["edits"]:
            eo = {k: v for k, v in ed.items() if k != "old_fragment"}
            if ed["old_fragment"] is None:
                eo["machine_verification"] = {
                    "kind": "no-fragment (standing text)", "occurrences": None,
                    "ok": True}
            else:
                tpath = ed.get("target_file_abs_override") or prop["target_file_abs"]
                if tpath not in target_cache:
                    target_cache[tpath] = read_text(tpath)
                t = target_cache[tpath]
                lf, crlf, variant, hits = count_fragment(t, ed["old_fragment"])
                spans = frag_lines(t, ed["old_fragment"])
                ok = (hits == 1)
                if not ok:
                    fail("fragment %s: %d occurrences (expected exactly 1) in %s"
                         % (ed["edit_id"], hits, tpath))
                eo["machine_verification"] = {
                    "kind": "old-fragment exactly-once", "target_file": tpath,
                    "lf_variant_count": lf, "crlf_variant_count": crlf,
                    "matched_variant": variant, "occurrences": hits,
                    "line_start": spans[0] if spans else None,
                    "line_end": spans[1] if spans else None, "ok": ok}
                frag_stats.append({"edit_id": ed["edit_id"], "target": tpath,
                                   "occurrences": hits, "ok": ok})
            # resolve placeholder new_texts
            if ed["new_text"].startswith("@EXTRACT:"):
                marker = ed["new_text"][len("@EXTRACT:"):]
                eo["new_text"] = {"P2R2-2-R3-FIXED": fixed_p2,
                                  "P3R3-FIXED-1": fixed_p3_1,
                                  "P3R3-FIXED-3": fixed_p3_3}[marker]
            else:
                eo["new_text"] = ed["new_text"]
            edits_out.append(eo)
        prop_out["edits"] = edits_out
        proposals_out.append(prop_out)

    # discovery scan (informational, not gated)
    disc = {}
    for name, path in (("Python == Node == R36 historical", D.R2_GATES_PY),
                       ("Python == Node == R36 historical", D.R2_TR_JSON)):
        t = target_cache.get(path) or read_text(path)
        disc["%s @ %s" % (name, os.path.basename(path))] = t.count(name)

    results["fragment_stats"] = frag_stats
    results["discovery_scan"] = disc

    # --- census ---------------------------------------------------------------
    state = docs_state()
    census_files = {}
    for p, meta in state.items():
        t = read_text(p)
        ntext, idx = census_build(t)
        census_files[p] = {"text": t, "ntext": ntext, "idx": idx}
    occurrences = {}
    for cat_key, pattern, category, why in D.CENSUS_PATTERNS:
        hits = []
        for p, cf in census_files.items():
            for h in census_find(cf["ntext"], cf["idx"], cf["text"], pattern):
                h["file"] = os.path.relpath(p, D.DOCS_NIF).replace("\\", "/")
                h["why_flagged"] = why
                hits.append(h)
        occurrences[cat_key] = {"pattern": pattern, "category": category,
                                 "count": len(hits), "matches": hits}
    # absence checks must be zero
    for k, occ in occurrences.items():
        if occ["category"] == "ABSENCE" and occ["count"] != 0:
            fail("absence check failed: %s found %d occurrences" % (k, occ["count"]))

    # review citations
    rc = []
    for cit in D.REVIEW_CITATIONS:
        p = os.path.join(D.DOCS_NIF, cit["file"])
        cf = census_files[p]
        found = [h for h in census_find(cf["ntext"], cf["idx"], cf["text"], cit["pattern"])]
        at_line = any(h["line_start"] == cit["claimed_line"] for h in found)
        if not at_line:
            fail("review citation drifted: %s:%d expected %r" %
                 (cit["file"], cit["claimed_line"], cit["pattern"]))
        rc.append({"file": cit["file"], "claimed_line": cit["claimed_line"],
                   "pattern": cit["pattern"], "citation_for": cit["citation_for"],
                   "verified_at_claimed_line": at_line,
                   "actual_line_spans": [[h["line_start"], h["line_end"]] for h in found]})
    results["review_citations"] = rc

    # --- R3 unmodified ---------------------------------------------------------
    r3r = r3_rehash()
    results["r3_package_rehash"] = r3r
    if r3r["mismatches"]:
        fail("R3 package modified: %s" % r3r["mismatches"])

    # --- write outputs ---------------------------------------------------------
    os.makedirs(os.path.dirname(TARGET_MAP_JSON), exist_ok=True)
    n_frags = len(frag_stats)
    map_obj = {
        "run_id": D.RUN_ID,
        "purpose": ("Full P1-P5 proposal -> target map with machine-verified old "
                    "fragments (each occurs EXACTLY ONCE in its target file) and "
                    "verbatim proposed new texts (P2/P3 fixes applied per "
                    "PROPOSALS_P2P3_FIXED.md). MAP ONLY — nothing is applied; "
                    "docs/nif and all historical runs stay byte-identical."),
        "source_proposal": {"path": PROPOSAL_MD,
                            "sha256": pr_sha,
                            "sha256_matches_expected_pin": pr_sha == D.EXPECTED_PROPOSAL_SHA256},
        "fixed_texts_source": {"path": PROPOSAL_FIXED_MD,
                               "sha256": sha256_file(PROPOSAL_FIXED_MD)},
        "prompt": {"path": PROMPT_MD, "sha256": p_sha},
        "driver_hashes": {"build_package_r1.py": results["gates"]["driver_sha256"],
                          "map_defs.py": results["gates"]["map_defs_sha256"]},
        "operations_legend": {
            "REPLACE": "future docs/nif application edit (NOT this run)",
            "LEDGER-ENTRY": "historical file preserved byte-identical; entry records superseded wording",
            "STANDING-RULE": "new standing text; no superseded file wording",
            "STANDING-POLICY": "acceptance/policy guard; anchor fragment verifies the referenced historical wording"},
        "proposals": proposals_out,
        "map_stats": {
            "proposals_mapped": len(D.MAP_PROPOSALS),
            "total_edits": sum(len(p["edits"]) for p in D.MAP_PROPOSALS),
            "old_fragments_machine_verified": n_frags,
            "fragments_exactly_once": sum(1 for s in frag_stats if s["ok"]),
            "fragment_verification_all_ok": all(s["ok"] for s in frag_stats),
            "verbatim_checks_all_ok": all(vt.values()),
            "fixed_text_checks_all_ok": all(fx.values()),
            "r3_package_unchanged": not r3r["mismatches"],
            "discovery_scan": disc},
    }
    jdump(TARGET_MAP_JSON, map_obj)

    census_obj = {
        "run_id": D.RUN_ID,
        "scope": ("READ-ONLY census of docs/nif — no edits performed. The docs_state "
                  "hashes are re-verified by the index phase to prove this run did "
                  "not modify docs/nif."),
        "censused_files": {os.path.relpath(p, D.DOCS_NIF).replace("\\", "/"): m
                           for p, m in state.items()},
        "review_citations": rc,
        "occurrences": occurrences,
        "totals": {
            "flagged_occurrences": sum(o["count"] for o in occurrences.values()
                                       if o["category"].startswith("FLAGGED")),
            "adjacent_interaction_occurrences": sum(o["count"] for o in occurrences.values()
                                                     if o["category"] == "ADJACENT-INTERACTION"),
            "adjacent_hedged_occurrences": sum(o["count"] for o in occurrences.values()
                                                if o["category"] == "ADJACENT-HEDGED"),
            "absence_checks_all_zero": all(o["count"] == 0 for o in occurrences.values()
                                           if o["category"] == "ABSENCE"),
            "out_of_scope_occurrences": sum(o["count"] for o in occurrences.values()
                                            if o["category"] == "OUT-OF-SCOPE")},
    }
    jdump(CENSUS_JSON, census_obj)

    print("VERIFY phase complete.")
    print("  proposals mapped: %d; edits: %d; fragments exactly-once: %d/%d"
          % (map_obj["map_stats"]["proposals_mapped"], map_obj["map_stats"]["total_edits"],
             map_obj["map_stats"]["fragments_exactly_once"], n_frags))
    print("  flagged occurrences: %d; adjacent: %d/%d; absence all-zero: %s; OOS: %d"
          % (census_obj["totals"]["flagged_occurrences"],
             census_obj["totals"]["adjacent_interaction_occurrences"],
             census_obj["totals"]["adjacent_hedged_occurrences"],
             census_obj["totals"]["absence_checks_all_zero"],
             census_obj["totals"]["out_of_scope_occurrences"]))
    print("  R3 re-hash: %d/%d rows match" % (r3r["matches"], r3r["rows_checked"]))
    print("  failures: %d" % len(FAILURES))
    sys.exit(1 if FAILURES else 0)


# -------------------------------------------------------------------------- index
def phase_index():
    drv_txt = read_text(DRIVER_TXT)
    for path in (DRIVER_PY, DEFS_PY):
        h = sha256_file(path)
        if h not in drv_txt:
            print("FATAL: %s changed after SHA256_DRIVER.txt was written" % path)
            sys.exit(2)
    cen = json.loads(read_text(CENSUS_JSON))
    cur = docs_state()
    for p, meta in cen["censused_files"].items():
        ap = os.path.join(D.DOCS_NIF, *p.split("/"))
        if sha256_file(ap) != meta["sha256"]:
            print("FATAL: docs/nif file changed since census: %s" % p)
            sys.exit(2)
    r3r = r3_rehash()
    if r3r["mismatches"]:
        print("FATAL: R3 package modified: %s" % r3r["mismatches"])
        sys.exit(2)

    artifacts = [
        ("00_CONTROL\\NEXT_PROMPT.md", "R1 run artifact (00_CONTROL/NEXT_PROMPT.md — the executed prompt)", "gate R1G1"),
        ("00_CONTROL\\build_package_r1.py", "R1 run driver (00_CONTROL/build_package_r1.py)", "gates R1G7/R1G8/R1G9/R1G10/R1G12/R1G13"),
        ("00_CONTROL\\map_defs.py", "R1 run driver data (00_CONTROL/map_defs.py)", "gates R1G7/R1G8/R1G9/R1G10/R1G12/R1G13"),
        ("00_CONTROL\\SHA256_DRIVER.txt", "R1 driver hash record (hashed after last edit, before first execution)", "driver integrity"),
        ("05_ANALYSIS\\TARGET_MAP.json", "item 4 target map (machine-verified old fragments, verbatim new texts)", "item 4; gates R1G7/R1G8"),
        ("05_ANALYSIS\\CONTRADICTION_CENSUS.json", "docs/nif read-only contradiction census (current lines)", "census; gates R1G9/R1G10/R1G12"),
        ("06_REPORT\\GATE_WEAKNESS_ADDENDUM.md", "item 3 gate-weakness addendum (R3G6c/R3G10/impl-count + manifest omission)", "item 3; gates R1G3/R1G4/R1G5/R1G6"),
        ("06_REPORT\\PROPOSALS_P2P3_FIXED.md", "item 5 corrected P2/P3 proposal texts (extraction-marked)", "item 5; P2/P3 fixes"),
        ("REPORT.md", "R1 run report (pointer + final handoff block)", "run report"),
        ("HANDOFF.md", "R1 handoff (master path-limited commit pending; HR decisions unchanged)", "handoff"),
        ("STAGE_ACCEPTANCE_GATES.csv", "R1 gate ledger (EXECUTABLE + HUMAN_REVIEW rows)", "gates R1G1..R1G13 + HR-R1-1/2"),
    ]
    rows = []
    for rel, role, claims in artifacts:
        p = os.path.join(RUN_ROOT, *rel.split("\\"))
        rows.append([os.path.join(RUN_ROOT, rel), role, sha256_file(p),
                     str(os.path.getsize(p)),
                     "this run (%s, 2026-09-05)" % D.RUN_ID.replace("PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_", "PE-NIF-R3-PERSISTENCE-AND-TARGETMAP-R1, "),
                     "RUN PACKAGE (no repo write by this run; master path-limited commit pending)",
                     claims])
    with open(ARTIFACT_INDEX_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_path_full", "role", "sha256", "size_bytes",
                    "snapshot_time_scope", "publication_scope", "claims_supported"])
        w.writerows(rows)
    print("INDEX phase complete: artifact_index.csv written with %d rows "
          "(the manifest excludes itself — documented)." % len(rows))
    print("  docs/nif unchanged since census: %d files OK"
          % len(cen["censused_files"]))
    print("  R3 re-hash: %d/%d rows match" % (r3r["matches"], r3r["rows_checked"]))


def jdump(path, obj):
    write_text(path, json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("hash", "verify", "index"):
        print("usage: build_package_r1.py hash|verify|index")
        sys.exit(2)
    {"hash": phase_hash, "verify": phase_verify, "index": phase_index}[sys.argv[1]]()
