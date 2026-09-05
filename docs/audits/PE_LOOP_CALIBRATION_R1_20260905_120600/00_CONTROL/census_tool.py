#!/usr/bin/env python3
"""census_tool.py - PE_LOOP_CALIBRATION_R1_20260905_120600 (RUN-4, loop-mechanics calibration).

The bounded, safe, mechanical census:
  (a) re-hash EVERY file of the LIVE M1 gate package recursively (path+size+SHA256);
  (b) re-hash the named index/report files of the five M1 run dirs (READ-ONLY,
      exact-name matches; a named file absent = NOT_FOUND recorded + continue);
  (c) CROSS-CHECK: every SHA the package's own records state vs the fresh hashes
      (the census is a detector): MATCH / SUPERSEDED_HISTORICAL (the package's own
      append-only layer model) / MISMATCH (LOUD finding) / EXTERNAL_REFERENCE
      (out of census scope, recorded not verified) / UNKNOWN_UNRESOLVED;
  (d) the counts per scope;
  (e) update the WRITE-AHEAD state file 00_CONTROL/PE_LOOP_CALIBRATION_STATE.json
      to CENSUS_DONE / AWAITING_ORCHESTRATOR_AUDIT.

DISCIPLINE: ZERO writes outside the calibration ROOT. The state file is physically
re-read at census start (the restart/resume proof) and re-read after the update.
Fail-closed: if the state file is not at RUNNING/CENSUS_DISPATCHED, ABORT.
"""

import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

RUN_ID = "PE_LOOP_CALIBRATION_R1_20260905_120600"
ROOT = Path(r"D:\Eudoria_Reconstruction\99_Audits") / RUN_ID
STATE_PATH = ROOT / "00_CONTROL" / "PE_LOOP_CALIBRATION_STATE.json"
PKG_ROOT = Path(r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits") / "PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
AUDITS_ROOT = Path(r"D:\Eudoria_Reconstruction\99_Audits")
RUN_DIRS = [
    "PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439",
    "PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816",
    "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327",
    "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528",
    "PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209",
]
NAMED_FILES = ["artifact_index.csv", "REPORT.md", "HANDOFF.md", "STAGE_ACCEPTANCE_GATES.csv"]
PKG_REPO_PREFIX = "docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/"
RUN_DIR_REL_PREFIXES = ("00_CONTROL/", "01_RAW/", "02_LOGS/", "03_STATIC/", "04_RUNTIME/", "05_ANALYSIS/", "06_REPORT/")
EXT_PREFIXES = ("src/", "terrain/", "pcg_install", "docs/audits/PE_M1")

HEX64_ALL = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])")
BACKTICK = re.compile(r"`([^`\n]{1,300})`")
TOK = re.compile(r"[A-Za-z]:[\\/][\w ./\\()\-]+|[\w .()\-]+[\\/][\w ./\\()\-]*|[\w.()\-]+\.[A-Za-z0-9]{2,4}")
PATH_KEYS = ("file", "local_path", "path", "repo_path", "run_path", "source", "relpath", "url", "manifest", "file_name")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def main():
    # 0. RESUME-READ of the WRITE-AHEAD state (the dispatch boundary)
    state_raw = STATE_PATH.read_text(encoding="utf-8")
    state_at_dispatch = json.loads(state_raw)
    state_sha_at_dispatch = hashlib.sha256(state_raw.encode("utf-8")).hexdigest().upper()
    if state_at_dispatch.get("status") != "RUNNING" or state_at_dispatch.get("phase") != "CENSUS_DISPATCHED":
        print("[ABORT] state file not at RUNNING/CENSUS_DISPATCHED - fail-closed, ZERO census writes")
        return 2
    print("[RESUME-READ] state physically re-read at census start: status=%s phase=%s dispatch=%s sha256=%s" % (
        state_at_dispatch["status"], state_at_dispatch["phase"], state_at_dispatch["dispatch"], state_sha_at_dispatch))

    # (a) SCOPE A: the gate package re-hash census
    pkg_files = []
    unreadable = []
    for f in sorted(p for p in PKG_ROOT.rglob("*") if p.is_file()):
        rel = f.relative_to(PKG_ROOT).as_posix()
        try:
            pkg_files.append({"path": rel, "size_bytes": f.stat().st_size, "sha256": sha256_file(f)})
        except OSError as e:
            unreadable.append({"path": rel, "error": str(e)})
    fresh = {r["path"]: {"size_bytes": r["size_bytes"], "sha256": r["sha256"]} for r in pkg_files}
    fresh_by_sha = defaultdict(list)
    for r in pkg_files:
        fresh_by_sha[r["sha256"]].append(r["path"])
    total_bytes_a = sum(r["size_bytes"] for r in pkg_files)
    print("[SCOPE-A] gate package: %d files hashed, %d bytes, unreadable=%d" % (len(pkg_files), total_bytes_a, len(unreadable)))

    # (b) SCOPE B: the named index/report files of the five run dirs
    per_run_dir = []
    found_b = 0
    not_found_b = 0
    for d in RUN_DIRS:
        rdir = AUDITS_ROOT / d
        slots = []
        for name in NAMED_FILES:
            hits = sorted(p for p in rdir.rglob(name) if p.is_file()) if rdir.is_dir() else []
            if hits:
                for p in hits:
                    slots.append({"named_file": name, "status": "FOUND",
                                  "path": p.relative_to(AUDITS_ROOT).as_posix(),
                                  "size_bytes": p.stat().st_size, "sha256": sha256_file(p)})
                found_b += len(hits)
            else:
                slots.append({"named_file": name, "status": "NOT_FOUND", "searched_run_dir": d,
                              "note": "exact-name match absent from the run dir tree (recorded + continue)"})
                not_found_b += 1
        per_run_dir.append({"run_dir": d, "slots": slots,
                            "found": sum(1 for s in slots if s["status"] == "FOUND"),
                            "not_found": sum(1 for s in slots if s["status"] == "NOT_FOUND")})
        print("[SCOPE-B] %s: found=%d not_found=%d" % (d, per_run_dir[-1]["found"], per_run_dir[-1]["not_found"]))
    print("[SCOPE-B] totals: slots=%d found_hashed=%d not_found=%d" % (len(RUN_DIRS) * len(NAMED_FILES), found_b, not_found_b))

    # (c) CROSS-CHECK: extract every SHA claim from the package's own records
    claims = []

    def classify_token(tok):
        t = tok.strip().strip("`\"').,;:()")
        t = t.replace("\\", "/")
        if not t:
            return None, None
        # usable-token rule (dispatch 3): ignore numeric/punct-only fragments and
        # extension-less version-like fragments so they never become candidates
        if re.search(r"[A-Za-z]", t) is None:
            return None, None
        if "/" not in t:
            m = re.search(r"\.([A-Za-z0-9]{2,4})$", t)
            if not m or not m.group(1).isalpha():
                return None, None
        if ("99_Audits" in t or re.search(r"[A-Za-z]:/", t)
                or t.startswith(RUN_DIR_REL_PREFIXES) or t.startswith(EXT_PREFIXES)
                or t in RUN_DIRS or any(t == "99_Audits/" + d for d in RUN_DIRS)):
            return "EXT", t
        t2 = t[len(PKG_REPO_PREFIX):] if t.startswith(PKG_REPO_PREFIX) else t
        if t2 in fresh:
            return "PKG", t2
        if "/" not in t2:
            hits = sorted(k for k in fresh if k.rsplit("/", 1)[-1] == t2)
            if len(hits) == 1:
                return "PKG", hits[0]
        # dispatch-3 broadening: a usable path-like token that is NOT a package file
        # is an out-of-census-scope reference (external artifact cited by bare name)
        return "EXT", t

    def add_claim(hexv, source_rel, locator, ctx_tokens):
        ctx_pkg, ctx_ext = [], []
        for tok in ctx_tokens:
            kind, val = classify_token(tok)
            if kind == "PKG":
                ctx_pkg.append(val)
            elif kind == "EXT":
                ctx_ext.append(val)
        claims.append({"sha256_recorded": hexv, "source_file": source_rel, "locator": locator,
                       "package_path_candidates": sorted(set(ctx_pkg)),
                       "external_context": sorted(set(ctx_ext))})

    def walk_json(node, source_rel, pointer, inherited_ctx):
        if isinstance(node, dict):
            own = [v for k, v in node.items() if isinstance(v, str) and k in PATH_KEYS]
            ctx = own + inherited_ctx
            for k, v in node.items():
                walk_json(v, source_rel, pointer + "." + k, ctx)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk_json(v, source_rel, pointer + "[" + str(i) + "]", inherited_ctx)
        elif isinstance(node, str):
            for m in HEX64_ALL.finditer(node):
                add_claim(m.group(0).upper(), source_rel, pointer, inherited_ctx)

    def walk_md(p, source_rel):
        # CLAIM ASSOCIATION (dispatch 3): each hex's PRIMARY context = the nearest
        # usable path-like token BEFORE it on the same line (this package's citation
        # grammar is "NAME (SHA256 HEX); NAME (SHA256 HEX); ..."); secondary context
        # = the previous line's tokens (for name-on-previous-line claims). Dispatch 2's
        # flat same-line+prev-line candidate set over-attributed the multi-artifact
        # EVIDENCE lines (matrix V4.md lines 96/144/156: 6-7 external artifact SHAs per
        # line each inheriting the single package filename on the line) - verified at
        # source; those claims are EXTERNAL references, not superseded layers of the
        # package file. Hex-first matching is unaffected: any recorded SHA equal to a
        # fresh package hash is a MATCH regardless of context.
        prev_toks = []
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as e:
            unreadable.append({"path": source_rel, "error": str(e)})
            return
        for i, line in enumerate(lines):
            toks = [(m.start(), m.group(0)) for m in BACKTICK.finditer(line)]
            toks += [(m.start(), m.group(0)) for m in TOK.finditer(line)]
            toks.sort()
            line_toks = [t for _, t in toks]
            for m in HEX64_ALL.finditer(line):
                before = [t for pos, t in toks if pos < m.start()]
                add_claim(m.group(0).upper(), source_rel, "line " + str(i + 1),
                          (before[-1:] + prev_toks) if before else prev_toks)
            prev_toks = line_toks

    for r in pkg_files:
        p = PKG_ROOT / r["path"]
        if p.suffix.lower() == ".json":
            try:
                walk_json(json.loads(p.read_text(encoding="utf-8")), r["path"], "$", [])
            except (OSError, ValueError) as e:
                unreadable.append({"path": r["path"], "error": "json parse: " + str(e)})
        elif p.suffix.lower() == ".md":
            walk_md(p, r["path"])
    print("[CROSS-CHECK] claims extracted: %d" % len(claims))

    # claim classification (hex-first; then per-candidate resolution)
    for c in claims:
        if c["sha256_recorded"] in fresh_by_sha:
            c["verdict"] = "MATCH"
            c["matched_files"] = sorted(fresh_by_sha[c["sha256_recorded"]])
        elif c["package_path_candidates"]:
            c["verdict"] = "PENDING_PKG"
        elif c["external_context"]:
            c["verdict"] = "EXTERNAL_REFERENCE"
        else:
            c["verdict"] = "UNKNOWN_UNRESOLVED"

    matching_files = set()
    for c in claims:
        if c["verdict"] == "MATCH":
            matching_files.update(c["matched_files"])

    mismatch_findings = {}  # file -> {recorded, sources}
    for c in claims:
        if c["verdict"] != "PENDING_PKG":
            continue
        dispo = {}
        loud = False
        for cand in c["package_path_candidates"]:
            if cand in matching_files:
                dispo[cand] = "SUPERSEDED_HISTORICAL"
            else:
                dispo[cand] = "MISMATCH"
                loud = True
                mf = mismatch_findings.setdefault(cand, {"recorded_sha256_claims": [], "claim_sources": []})
                mf["recorded_sha256_claims"].append(c["sha256_recorded"])
                mf["claim_sources"].append(c["source_file"] + " (" + c["locator"] + ")")
        if loud:
            c["verdict"] = "MISMATCH"
        elif dispo:
            c["verdict"] = "SUPERSEDED_HISTORICAL"
        else:
            c["verdict"] = "UNKNOWN_UNRESOLVED"
        c["candidate_dispositions"] = dispo
    for mf in mismatch_findings.values():
        mf["recorded_sha256_claims"] = sorted(set(mf["recorded_sha256_claims"]))
        mf["claim_sources"] = sorted(set(mf["claim_sources"]))

    counts = defaultdict(int)
    for c in claims:
        counts[c["verdict"]] += 1

    # per-package-file claim coverage
    coverage = []
    for r in pkg_files:
        fp = r["path"]
        matching = sum(1 for c in claims if c["verdict"] == "MATCH" and fp in c["matched_files"])
        superseded = sum(1 for c in claims if c["verdict"] == "SUPERSEDED_HISTORICAL" and fp in c.get("candidate_dispositions", {}))
        mismatched = sum(1 for c in claims if c["verdict"] == "MISMATCH" and fp in c.get("candidate_dispositions", {}))
        coverage.append({"path": fp, "matching_claims": matching, "superseded_claims": superseded,
                          "mismatch_claims": mismatched,
                          "recorded_sha_in_package_records": matching > 0})

    mismatch_list = []
    for fp in sorted(mismatch_findings):
        mismatch_list.append({"file": fp, "fresh_sha256": fresh[fp]["sha256"],
                              **mismatch_findings[fp],
                              "verdict": "LOUD FINDING - recorded SHA does not match the fresh hash and no superseding claim matches"})
    print("[CROSS-CHECK] verdicts: MATCH=%d SUPERSEDED_HISTORICAL=%d MISMATCH=%d EXTERNAL_REFERENCE=%d UNKNOWN_UNRESOLVED=%d" % (
        counts["MATCH"], counts["SUPERSEDED_HISTORICAL"], counts["MISMATCH"],
        counts["EXTERNAL_REFERENCE"], counts["UNKNOWN_UNRESOLVED"]))
    for mm in mismatch_list:
        print("[LOUD] MISMATCH %s fresh=%s recorded=%s sources=%s" % (
            mm["file"], mm["fresh_sha256"], mm["recorded_sha256_claims"], mm["claim_sources"]))

    # (d)+(e) write census outputs + update the state file
    generated_at = now_iso()
    ext_items = [{"sha256_recorded": c["sha256_recorded"], "source_file": c["source_file"],
                  "locator": c["locator"], "external_context": c["external_context"]}
                 for c in claims if c["verdict"] == "EXTERNAL_REFERENCE"]
    unknown_items = [{"sha256_recorded": c["sha256_recorded"], "source_file": c["source_file"],
                      "locator": c["locator"]} for c in claims if c["verdict"] == "UNKNOWN_UNRESOLVED"]
    superseded_items = [{"sha256_recorded": c["sha256_recorded"], "source_file": c["source_file"],
                         "locator": c["locator"], "candidate_dispositions": c.get("candidate_dispositions", {})}
                        for c in claims if c["verdict"] == "SUPERSEDED_HISTORICAL"]

    census_a = {
        "run_id": RUN_ID,
        "generated_at": generated_at,
        "census_class": "LOOP_CALIBRATION_R1 re-hash census: scope (a) gate package + cross-check (c) vs the package's own recorded SHAs",
        "state_file_resume_read": {
            "path": "00_CONTROL/PE_LOOP_CALIBRATION_STATE.json",
            "sha256_at_dispatch_read": state_sha_at_dispatch,
            "status_read": state_at_dispatch["status"],
            "phase_read": state_at_dispatch["phase"],
            "dispatch_read": state_at_dispatch["dispatch"],
            "note": "physically re-read from disk at census start (the restart/resume proof: the state survived the dispatch boundary)",
        },
        "scope_a_gate_package": {
            "root": PKG_ROOT.as_posix(),
            "rule": "every file recursively; identity metadata only (path+size+SHA256); READ-ONLY",
            "file_count": len(pkg_files),
            "total_bytes": total_bytes_a,
            "unreadable_files": unreadable,
            "files": pkg_files,
        },
        "cross_check_c": {
            "rule": "every SHA the package's own records state for a package file vs the fresh hashes; within-scope mismatch = LOUD finding; superseded-layer claims classified per the package's own append-only model; out-of-scope references recorded as external (not verified)",
            "claims_extracted": len(claims),
            "verdict_counts": dict(counts),
            "mismatch_findings": mismatch_list,
            "superseded_historical": superseded_items,
            "external_references": {"count": len(ext_items), "items": ext_items},
            "unknown_unresolved": unknown_items,
            "package_file_claim_coverage": coverage,
            "claims": claims,
        },
    }
    out_a = ROOT / "01_RAW" / "census_gate_package.json"
    out_a.write_text(json.dumps(census_a, indent=1, ensure_ascii=True), encoding="utf-8")

    census_b = {
        "run_id": RUN_ID,
        "generated_at": generated_at,
        "census_class": "LOOP_CALIBRATION_R1 re-hash census: scope (b) the named index/report files of the five M1 run dirs (READ-ONLY)",
        "scope_b_run_indexes": {
            "rule": "exact-name matches searched within each run dir tree (READ-ONLY; the full trees are NOT in scope); a named file absent = NOT_FOUND recorded + continue",
            "named_files": NAMED_FILES,
            "run_dirs": RUN_DIRS,
            "per_run_dir": per_run_dir,
            "totals": {"slots": len(RUN_DIRS) * len(NAMED_FILES), "found_hashed": found_b, "not_found": not_found_b},
        },
    }
    out_b = ROOT / "01_RAW" / "census_run_indexes.json"
    out_b.write_text(json.dumps(census_b, indent=1, ensure_ascii=True), encoding="utf-8")

    state = dict(state_at_dispatch)
    state["status"] = "CENSUS_DONE"
    state["phase"] = "AWAITING_ORCHESTRATOR_AUDIT"
    state["files_hashed"] = {
        "scope_a_gate_package": {"count": len(pkg_files), "total_bytes": total_bytes_a, "unreadable": len(unreadable)},
        "scope_b_run_indexes": {"slots": len(RUN_DIRS) * len(NAMED_FILES), "found_hashed": found_b, "not_found": not_found_b},
        "total_files_hashed": len(pkg_files) + found_b,
    }
    state["cross_check"] = {
        "claims_extracted": len(claims),
        "match": counts["MATCH"],
        "superseded_historical": counts["SUPERSEDED_HISTORICAL"],
        "mismatch": counts["MISMATCH"],
        "external_reference": counts["EXTERNAL_REFERENCE"],
        "unknown_unresolved": counts["UNKNOWN_UNRESOLVED"],
    }
    state["mismatch_findings"] = mismatch_list
    state["updated_at"] = generated_at
    state["updated_by"] = "pe-reconstruction (census_tool.py, dispatch 1 completed)"
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    state_after_raw = STATE_PATH.read_text(encoding="utf-8")
    state_sha_after = hashlib.sha256(state_after_raw.encode("utf-8")).hexdigest().upper()
    state_after = json.loads(state_after_raw)
    print("[STATE-UPDATE] status=%s phase=%s" % (state_after["status"], state_after["phase"]))
    print("[STATE-UPDATE] state file sha256 after update: %s" % state_sha_after)
    print("[COUNTS] scope_a=%d files / %d bytes; scope_b found_hashed=%d not_found=%d; claims=%d (MATCH=%d SUPERSEDED=%d MISMATCH=%d EXT=%d UNKNOWN=%d)" % (
        len(pkg_files), total_bytes_a, found_b, not_found_b, len(claims), counts["MATCH"],
        counts["SUPERSEDED_HISTORICAL"], counts["MISMATCH"], counts["EXTERNAL_REFERENCE"], counts["UNKNOWN_UNRESOLVED"]))
    print("[OUTPUTS] %s" % out_a.as_posix())
    print("[OUTPUTS] %s" % out_b.as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
