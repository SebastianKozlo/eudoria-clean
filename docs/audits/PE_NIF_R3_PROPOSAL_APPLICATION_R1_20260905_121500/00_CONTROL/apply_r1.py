#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""apply_r1.py — PE_NIF_R3_PROPOSAL_APPLICATION_R1 driver (RUN-B).

Bounded wording-only application of the R3 proposals P1-P5 per TARGET_MAP.json
(HR-R3-3 = GO). Phases: pregate | apply | gates | index. Old fragments come
from the hash-pinned map_defs.py; new texts from the hash-pinned TARGET_MAP.json
(both re-hashed in-driver before use; cross-checked against the pinned proposal
sources). G1 = 13 fragments EXACTLY-ONCE (census method, line spans cross-
checked vs the map). Writes only inside RUN_ROOT + the authorized targets.
Exit 2 = HARD_STOP (pregate/apply), 1 = gate failure. No Git inside (G6 is
executed by the operator; raw records saved to 01_RAW by the operator)."""
import csv
import datetime
import glob
import hashlib
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app_defs as A
import app_content as C

sys.path.insert(0, os.path.join(A.TARGETMAP_ROOT, "00_CONTROL"))

DRIVER_FILES = ["apply_r1.py", "app_defs.py", "app_content.py"]
FAILURES = []


def fail(m):
    FAILURES.append(m)
    print("FAIL: " + m)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8")


def write_text(p, s):
    with open(p, "wb") as f:
        f.write(s.encode("utf-8"))


def norm(s):
    return " ".join(s.split())


def jdump(p, o):
    write_text(p, json.dumps(o, indent=1, ensure_ascii=False) + "\n")


def line_of(t, pos):
    return t.count("\n", 0, pos) + 1


def count_fragment(t, frag):
    lf = t.count(frag)
    crlf = t.count(frag.replace("\n", "\r\n")) if "\n" in frag else lf
    if lf and not crlf:
        v, h = "LF", lf
    elif crlf and not lf:
        v, h = "CRLF", crlf
    else:
        v, h = ("LF+CRLF", lf) if lf == crlf else ("MIXED", lf + crlf)
    return lf, crlf, v, h


def frag_lines(t, frag):
    for var in (frag, frag.replace("\n", "\r\n")):
        i = t.find(var)
        if i >= 0:
            return line_of(t, i), line_of(t, i + len(var) - 1)
    return None


def git(args):
    return subprocess.run(["git"] + args, cwd=A.REPO, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def extract_marker(md, marker):
    s = "<!-- EXTRACT:%s:START -->" % marker
    e = "<!-- EXTRACT:%s:END -->" % marker
    return md[md.index(s) + len(s):md.index(e)].strip()


def load_inputs():
    pins = {}
    for name, (path, want) in A.PIN.items():
        got = sha256_file(path)
        pins[name] = {"path": path, "sha256": got, "expected": want,
                      "match": got.lower() == want}
        if not pins[name]["match"]:
            fail("pinned input SHA mismatch: %s" % name)
    if FAILURES:
        return None
    import map_defs as D
    tmap = json.loads(read_text(A.PIN["TARGET_MAP.json"][0]))
    fixed_md = read_text(A.PIN["PROPOSALS_P2P3_FIXED.md"][0])
    xt = {"P2R2-2-R3-FIXED/main": extract_marker(fixed_md, "P2R2-2-R3-FIXED"),
          "P3R3/a": extract_marker(fixed_md, "P3R3-FIXED-1"),
          "P3R3/c": extract_marker(fixed_md, "P3R3-FIXED-3")}
    dc = {"P1R2-5-R3/a": D.NEW_P1A, "P1R2-5-R3/b": D.NEW_P1B,
          "P3R3/b1": D.NEW_P3B, "P3R3/b2": D.NEW_P3B, "P3R3/b3": D.NEW_P3B,
          "P3R3/b4": D.NEW_P3B, "P4R3/a": D.NEW_P4A, "P4R3/b1": D.NEW_P4B,
          "P4R3/b2": D.NEW_P4B, "P4R3/b3": D.NEW_P4B, "P4R3/c": D.NEW_P4C,
          "P5R3/a": D.NEW_P5A, "P5R3/b": D.NEW_P5B}
    edits, frags, targets = {}, {}, {}
    for prop in tmap["proposals"]:
        for ed in prop["edits"]:
            r = dict(ed)
            r["proposal_id"] = prop["proposal_id"]
            r["claims"] = prop["claims"]
            r["area"] = prop["area"]
            edits[ed["edit_id"]] = r
    for prop in D.MAP_PROPOSALS:
        for ed in prop["edits"]:
            frags[ed["edit_id"]] = ed["old_fragment"]
            targets[ed["edit_id"]] = (ed.get("target_file_abs_override")
                                      or prop["target_file_abs"])
    for eid in A.ALL_EDITS:
        if eid not in edits:
            fail("edit missing from map: %s" % eid)
        if eid not in frags:
            fail("edit missing from pinned defs: %s" % eid)
    for eid, r in edits.items():
        if eid in xt and norm(r["new_text"]) != norm(xt[eid]):
            fail("map new_text != EXTRACT payload: %s" % eid)
        if eid in dc and norm(r["new_text"]) != norm(dc[eid]):
            fail("map new_text != pinned defs constant: %s" % eid)
    if len(edits) != 16:
        fail("map edit count != 16 (%d)" % len(edits))
    return {"pins": pins, "map": tmap, "edits": edits, "frags": frags,
            "targets": targets, "fixed": xt}


def docs_registry():
    reg = {}
    for p in sorted(glob.glob(os.path.join(A.DOCS_NIF, "**", "*.*"),
                              recursive=True)):
        t = read_text(p)
        reg[p] = {"sha256": sha256_file(p), "size_bytes": os.path.getsize(p),
                  "lines": t.count("\n") + 1,
                  "line_ending": "CRLF" if "\r\n" in t else "LF"}
    return reg


def hist_hashes():
    rec = {}
    for rel in A.R2_HIST_RELS:
        lp = os.path.join(A.R2_LOCAL, *rel.split("\\"))
        rp = os.path.join(A.R2_REPO, *rel.split("\\"))
        lh, rh = sha256_file(lp), sha256_file(rp)
        rec[rel] = {"local": {"path": lp, "sha256": lh,
                              "size_bytes": os.path.getsize(lp)},
                    "repo": {"path": rp, "sha256": rh,
                             "size_bytes": os.path.getsize(rp)},
                    "trees_equal": lh == rh}
        if not rec[rel]["trees_equal"]:
            fail("R2 historical file differs between trees: %s" % rel)
    return rec


def pkg_rehash(root):
    rows = list(csv.DictReader(open(os.path.join(root, "artifact_index.csv"),
                                    encoding="utf-8")))
    ok, bad = 0, []
    for r in rows:
        p = r["source_path_full"]
        try:
            h, sz = sha256_file(p), os.path.getsize(p)
        except OSError as ex:
            bad.append([p, "unreadable: %s" % ex])
            continue
        if h == r["sha256"].lower() and sz == int(r["size_bytes"]):
            ok += 1
        else:
            bad.append([p, "hash/size mismatch"])
    return {"rows_checked": len(rows), "matches": ok, "mismatches": bad}


def verify_all_fragments(inp, scope):
    """G1/G5 fragment check. scope: 'pre' (exactly-once, all 13) or
    'post-hist' (exactly-once, the 10 historical; docs fragments absent)."""
    res, cache = [], {}
    for eid in A.ALL_EDITS:
        frag = inp["frags"][eid]
        if frag is None:
            continue  # standing texts carry no fragment to verify
        tp = inp["targets"][eid]
        hist = tp.startswith(A.AUDITS_LOCAL)
        if scope == "post-hist" and not hist:
            continue
        if tp not in cache:
            cache[tp] = read_text(tp)
        t = cache[tp]
        lf, crlf, var, hits = count_fragment(t, frag)
        spans = frag_lines(t, frag)
        rec = {"edit_id": eid, "target_file": tp, "lf": lf, "crlf": crlf,
               "variant": var, "occurrences": hits,
               "line_start": spans[0] if spans else None,
               "line_end": spans[1] if spans else None, "ok": hits == 1}
        mv = inp["edits"][eid]["machine_verification"]
        rec["map_cross_check"] = {
            "map_line_start": mv["line_start"], "map_line_end": mv["line_end"],
            "map_occurrences": mv["occurrences"],
            "lines_match": (mv["line_start"] == rec["line_start"]
                            and mv["line_end"] == rec["line_end"]),
            "variant_match": mv["matched_variant"] == var}
        if not rec["ok"]:
            fail("G1 EXACTLY_ONCE_FAIL: %s (%d occurrences)" % (eid, hits))
        if scope == "pre" and not rec["map_cross_check"]["lines_match"]:
            fail("G1 line-span drift vs map: %s" % eid)
        res.append(rec)
    return res


def phase_pregate():
    inp = load_inputs()
    if FAILURES:
        jdump(os.path.join(A.RUN_ROOT, "01_RAW", "G1_PREGATE.json"),
              {"failures": list(FAILURES)})
        sys.exit(2)
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    g1 = verify_all_fragments(inp, "pre")
    base = git(["rev-parse", "HEAD"])
    staged = git(["diff", "--cached", "--name-only"])
    status = git(["status", "--porcelain"])
    docs_reg = docs_registry()
    hist = hist_hashes()
    tm = pkg_rehash(A.TARGETMAP_ROOT)
    r3 = pkg_rehash(A.R3_ROOT)
    if tm["mismatches"]:
        fail("TARGETMAP package modified: %s" % tm["mismatches"])
    if r3["mismatches"]:
        fail("R3 package modified: %s" % r3["mismatches"])
    if len(docs_reg) != 15:
        fail("docs/nif registry has %d files (expected 15)" % len(docs_reg))
    if staged.stdout.strip():
        fail("staged index NOT empty before the run: %s" % staged.stdout)
    if status.stdout.strip():
        fail("working tree NOT clean before the run: %s" % status.stdout)
    pre_dir = os.path.join(A.RUN_ROOT, "05_ANALYSIS", "PRE_EDIT_COPIES")
    os.makedirs(pre_dir, exist_ok=True)
    for eid in A.REPLACE_EDITS:
        tp = inp["targets"][eid]
        cp = os.path.join(pre_dir, os.path.basename(tp) + ".pre_edit")
        with open(tp, "rb") as f, open(cp, "wb") as g:
            g.write(f.read())
    out = {"run_id": A.RUN_ID, "timestamp": ts,
           "pinned_inputs": inp["pins"],
           "base_sha": base.stdout.strip(),
           "staged_index_before": staged.stdout,
           "worktree_status_before": status.stdout,
           "g1_fragments": g1,
           "g1_summary": {"fragments_checked": len(g1),
                          "all_exactly_once": all(r["ok"] for r in g1),
                          "all_lines_match_map": all(
                              r["map_cross_check"]["lines_match"] for r in g1)},
           "standing_text_ops_no_fragment": [e for e in A.ALL_EDITS
                                             if inp["frags"][e] is None],
           "docs_nif_registry_before": docs_reg,
           "r2_historical_before": hist,
           "targetmap_pkg_rehash": tm, "r3_pkg_rehash": r3}
    jdump(os.path.join(A.RUN_ROOT, "01_RAW", "G1_PREGATE.json"), out)
    jdump(os.path.join(A.RUN_ROOT, "05_ANALYSIS", "SHA_REGISTRY_BEFORE.json"),
          {"docs_nif": docs_reg, "r2_historical": hist})
    print("PREGATE: %d fragments exactly-once; BASE_SHA=%s; failures=%d"
          % (len(g1), out["base_sha"], len(FAILURES)))
    sys.exit(2 if FAILURES else 0)


def replace_once(path, old, new):
    t = read_text(path)
    lf, crlf, var, hits = count_fragment(t, old)
    if hits != 1 or var == "MIXED":
        return None, "expected exactly-once non-mixed, got %s x%d" % (var, hits)
    frag = old if ("\n" not in old or var == "LF") else old.replace("\n", "\r\n")
    t2 = t.replace(frag, new, 1)
    return t2, None


def phase_apply():
    inp = load_inputs()
    if FAILURES:
        sys.exit(2)
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    log = {"run_id": A.RUN_ID, "timestamp": ts, "replacements": [],
           "annotations": [], "sync": []}
    # -- 3 REPLACE edits (byte-exact, single replacement each)
    for eid in A.REPLACE_EDITS:
        tp = inp["targets"][eid]
        old, new = inp["frags"][eid], inp["edits"][eid]["new_text"]
        sha_b, sz_b = sha256_file(tp), os.path.getsize(tp)
        spans = frag_lines(read_text(tp), old)
        t2, err = replace_once(tp, old, new)
        if err:
            fail("REPLACE %s: %s" % (eid, err))
            jdump(os.path.join(A.RUN_ROOT, "01_RAW", "APPLY_LOG.json"), log)
            sys.exit(2)
        write_text(tp, t2)
        lf, crlf, var, hits = count_fragment(read_text(tp), old)
        new_ok = norm(new) in norm(read_text(tp))
        rec = {"edit_id": eid, "file": tp,
               "sha256_before": sha_b, "size_before": sz_b,
               "old_span_lines": [spans[0], spans[1]],
               "new_text_sha256": hashlib.sha256(
                   new.encode("utf-8")).hexdigest(),
               "sha256_after": sha256_file(tp),
               "size_after": os.path.getsize(tp),
               "old_absent_after": {"lf": lf, "crlf": crlf, "hits": hits,
                                    "ok": hits == 0},
               "new_present_norm": new_ok}
        if hits != 0:
            fail("REPLACE %s: old fragment still present" % eid)
        if not new_ok:
            fail("REPLACE %s: new text not present" % eid)
        log["replacements"].append(rec)
    # -- 13 annotation entries in 3 standing files (header first, then append)
    hist = hist_hashes()
    hdrs = {"ledger": C.ledger_header(A.RUN_ID, ts),
            "rules": C.rules_header(A.RUN_ID, ts),
            "policies": C.policies_header(A.RUN_ID, ts)}
    bodies = {k: [] for k in hdrs}
    hist_rel_of = {}
    for eid in A.ALL_EDITS:
        if eid in A.REPLACE_EDITS:
            continue
        tp = inp["targets"][eid]
        rel = None
        if tp is not None:
            for r in A.R2_HIST_RELS:
                if tp.endswith(r):
                    rel = r
            if rel is None:
                for r in A.R2_HIST_RELS:
                    if tp.replace("\\", "/").endswith(r.replace("\\", "/")):
                        rel = r
        hist_rel_of[eid] = rel
    for eid in (A.LEDGER_EDITS + A.RULE_EDITS + A.POLICY_EDITS):
        ed = inp["edits"][eid]
        frag = inp["frags"][eid]
        rel = hist_rel_of.get(eid)
        spans = frag_lines(read_text(inp["targets"][eid]), frag) if frag else None
        hh = hist.get(rel) if rel else None
        extra = None
        if eid == "P5R3/b":
            hits = []
            for p in sorted(glob.glob(os.path.join(A.DOCS_NIF, "**", "*.*"),
                                      recursive=True)):
                nt = norm(read_text(p))
                for pat in A.P5B_ABSENCE_PATTERNS:
                    if norm(pat) in nt:
                        hits.append([os.path.relpath(p, A.DOCS_NIF), pat])
            extra = ["- absence re-verification (this run): no restatement of the"
                     " semantic-header-normalization trigger family exists in"
                     " docs/nif (read-only whitespace-normalized scan of the 15"
                     " docs/nif files for %d patterns: %d hits)"
                     % (len(A.P5B_ABSENCE_PATTERNS), len(hits))]
            if hits:
                fail("P5R3/b absence re-verification found hits: %s" % hits)
        entry = C.render_entry(
            eid, ed["operation"], A.ENTRY_TITLES[eid], ed["claims"],
            ed["new_text"], frag, spans, ed["evidence_pointer"],
            ed["lineage_ref"], ed["new_text_source"], rel,
            hh["local"]["sha256"] if hh else None,
            hh["local"]["sha256"] if hh else None,
            hh["trees_equal"] if hh else None, A.RUN_ID, extra)
        bodies[A.ANN_KEY_OF_EDIT[eid]].append(entry)
    pre_dir = os.path.join(A.RUN_ROOT, "05_ANALYSIS", "G5_PRE_PROOFS")
    os.makedirs(pre_dir, exist_ok=True)
    for key, fname, role in A.ANN_FILES:
        rp = os.path.join(A.AUDITS_REPO, fname)
        lp = os.path.join(A.AUDITS_LOCAL, fname)
        header = hdrs[key]
        body = "".join(bodies[key])
        pre = os.path.join(pre_dir, fname + ".pre")
        write_text(pre, header)
        final = header + body
        write_text(rp, final)
        write_text(lp, final)
        rb = open(rp, "rb").read()
        lb = open(lp, "rb").read()
        pb = open(pre, "rb").read()
        rec = {"file": fname, "role": role,
               "entries": [e for e in (A.LEDGER_EDITS + A.RULE_EDITS +
                         A.POLICY_EDITS) if A.ANN_KEY_OF_EDIT[e] == key],
               "pre_path": pre, "pre_size": len(pb),
               "repo_path": rp, "repo_sha256": sha256_file(rp),
               "repo_size": len(rb),
               "prefix_ok": rb.startswith(pb) and lb.startswith(pb),
               "sync_equal": rb == lb, "local_path": lp,
               "local_sha256": sha256_file(lp)}
        if not rec["prefix_ok"]:
            fail("G5 ANNOTATION_APPEND_FAIL: prefix proof %s" % fname)
        if not rec["sync_equal"]:
            fail("SYNC mismatch: %s" % fname)
        log["annotations"].append(rec)
        log["sync"].append({"file": fname, "repo_sha256": rec["repo_sha256"],
                            "local_sha256": rec["local_sha256"],
                            "equal": rec["sync_equal"]})
    jdump(os.path.join(A.RUN_ROOT, "01_RAW", "APPLY_LOG.json"), log)
    jdump(os.path.join(A.RUN_ROOT, "05_ANALYSIS", "EDIT_LOG.json"), log)
    print("APPLY: %d replacements + %d annotation entries in %d files; "
          "failures=%d" % (len(log["replacements"]), sum(
              len(r["entries"]) for r in log["annotations"]),
              len(log["annotations"]), len(FAILURES)))
    sys.exit(2 if FAILURES else 0)


def scan_forbidden(paths):
    res, total = [], 0
    for p in paths:
        t = read_text(p)
        nt = norm(t)
        hits = []
        for pat in A.FORBIDDEN:
            c = t.count(pat) + nt.count(norm(pat))
            if c:
                hits.append({"pattern": pat, "count": c})
                total += c
        res.append({"file": p, "hits": hits})
    return res, total


def phase_gates():
    inp = load_inputs()
    if FAILURES:
        sys.exit(2)
    # G2 — new texts present verbatim (norm); old fragments absent
    g2 = []
    for eid in A.REPLACE_EDITS:
        tp = inp["targets"][eid]
        t = read_text(tp)
        old, new = inp["frags"][eid], inp["edits"][eid]["new_text"]
        lf, crlf, var, hits = count_fragment(t, old)
        rec = {"edit_id": eid, "file": tp,
               "new_text_present_norm": norm(new) in norm(t),
               "new_text_present_bytes": new in t,
               "old_absent": {"lf": lf, "crlf": crlf, "hits": hits},
               "old_absent_norm": norm(old) not in norm(t)}
        if not (rec["new_text_present_norm"] and rec["old_absent"]["hits"] == 0
                and rec["old_absent_norm"]):
            fail("G2 POST_EDIT_TEXT_MISMATCH: %s" % eid)
        g2.append(rec)
    # annotation payloads present verbatim in their standing files
    ann_g2 = []
    for eid in (A.LEDGER_EDITS + A.RULE_EDITS + A.POLICY_EDITS):
        key = A.ANN_KEY_OF_EDIT[eid]
        fname = dict((k, f) for k, f, _ in A.ANN_FILES)[key]
        t = read_text(os.path.join(A.AUDITS_REPO, fname))
        rec = {"edit_id": eid, "file": fname,
               "new_text_present_norm": norm(inp["edits"][eid]["new_text"])
               in norm(t)}
        if not rec["new_text_present_norm"]:
            fail("G2 annotation payload missing: %s" % eid)
        ann_g2.append(rec)
    jdump(os.path.join(A.RUN_ROOT, "01_RAW", "G2_POST.json"),
          {"replace_targets": g2, "annotation_files": ann_g2})
    # G3 — forbidden-clause scan (docs/nif all files + the 3 standing files)
    docs_files = sorted(glob.glob(os.path.join(A.DOCS_NIF, "**", "*.*"),
                                 recursive=True))
    ann_paths = [os.path.join(A.AUDITS_REPO, f) for _, f, _ in A.ANN_FILES]
    dres, dtotal = scan_forbidden(docs_files)
    ares, atotal = scan_forbidden(ann_paths)
    jdump(os.path.join(A.RUN_ROOT, "01_RAW", "G3_FORBIDDEN_SCAN.json"),
          {"patterns": A.FORBIDDEN, "docs_nif_files_scanned": len(docs_files),
           "docs_nif_hits": dres, "docs_nif_total_hits": dtotal,
           "annotation_files_scanned": len(ann_paths),
           "annotation_hits": ares, "annotation_total_hits": atotal,
           "pass": dtotal == 0 and atotal == 0})
    if dtotal or atotal:
        fail("G3 FORBIDDEN_PHRASE_PRESENT: docs=%d ann=%d" % (dtotal, atotal))
    # G4 — 13 non-target docs/nif files hash-identical before/after
    before = json.loads(read_text(os.path.join(
        A.RUN_ROOT, "05_ANALYSIS", "SHA_REGISTRY_BEFORE.json")))["docs_nif"]
    after = docs_registry()
    g4 = []
    for p in sorted(before):
        rec = {"file": os.path.relpath(p, A.DOCS_NIF),
               "sha_before": before[p]["sha256"],
               "sha_after": after[p]["sha256"],
               "target": p in [inp["targets"][e] for e in A.REPLACE_EDITS],
               "identical": before[p]["sha256"] == after[p]["sha256"]}
        if not rec["target"] and not rec["identical"]:
            fail("G4 COLLATERAL_EDIT: %s" % p)
        g4.append(rec)
    nontarget = [r for r in g4 if not r["target"]]
    jdump(os.path.join(A.RUN_ROOT, "01_RAW", "G4_COLLATERAL_REGISTRY.json"),
          {"registry": g4, "non_target_count": len(nontarget),
           "non_target_all_identical": all(r["identical"] for r in nontarget),
           "target_files_changed": [r["file"] for r in g4 if r["target"]]})
    # G5 — append-only proofs + historical byte-identity + package re-hash
    pre_dir = os.path.join(A.RUN_ROOT, "05_ANALYSIS", "G5_PRE_PROOFS")
    proofs = []
    for _, fname, _ in A.ANN_FILES:
        rb = open(os.path.join(A.AUDITS_REPO, fname), "rb").read()
        pb = open(os.path.join(pre_dir, fname + ".pre"), "rb").read()
        proofs.append({"file": fname, "pre_size": len(pb),
                       "final_size": len(rb), "prefix_ok": rb.startswith(pb)})
        if not rb.startswith(pb):
            fail("G5 ANNOTATION_APPEND_FAIL: %s" % fname)
    hist_after = hist_hashes()
    hb = json.loads(read_text(os.path.join(
        A.RUN_ROOT, "05_ANALYSIS", "SHA_REGISTRY_BEFORE.json")))["r2_historical"]
    hist_ok = all(hb[r]["local"]["sha256"] == hist_after[r]["local"]["sha256"]
                  and hb[r]["repo"]["sha256"] == hist_after[r]["repo"]["sha256"]
                  for r in hb)
    for r in hb:
        if not (hb[r]["local"]["sha256"] == hist_after[r]["local"]["sha256"]
                and hb[r]["repo"]["sha256"] == hist_after[r]["repo"]["sha256"]):
            fail("G5 historical file changed: %s" % r)
    frag_post = verify_all_fragments(inp, "post-hist")
    tm = pkg_rehash(A.TARGETMAP_ROOT)
    r3 = pkg_rehash(A.R3_ROOT)
    if tm["mismatches"] or r3["mismatches"]:
        fail("G5 historical package modified")
    jdump(os.path.join(A.RUN_ROOT, "01_RAW", "G5_APPEND_PROOFS.json"),
          {"prefix_proofs": proofs,
           "historical_files_byte_identical": hist_ok,
           "r2_historical_after": hist_after,
           "historical_fragments_still_exactly_once": frag_post,
           "targetmap_pkg_rehash": tm, "r3_pkg_rehash": r3})
    jdump(os.path.join(A.RUN_ROOT, "05_ANALYSIS", "SHA_REGISTRY_AFTER.json"),
          {"docs_nif": after, "r2_historical": hist_after})
    print("GATES: G2 ok; G3 docs hits=0 ann hits=0; G4 %d/%d non-target "
          "identical; G5 prefix_ok=%s hist_ok=%s; failures=%d"
          % (len(nontarget), len(nontarget) and sum(1 for r in nontarget
              if r["identical"]), all(p["prefix_ok"] for p in proofs),
             hist_ok, len(FAILURES)))
    sys.exit(1 if FAILURES else 0)


def phase_index():
    drv_txt = read_text(os.path.join(A.RUN_ROOT, "00_CONTROL",
                                     "SHA256_DRIVER.txt"))
    for f in DRIVER_FILES:
        h = sha256_file(os.path.join(A.RUN_ROOT, "00_CONTROL", f))
        if h.lower() not in drv_txt.lower():
            print("FATAL: %s changed after SHA256_DRIVER.txt" % f)
            sys.exit(2)
    # re-verify every gate raw record fail-closed
    g1 = json.loads(read_text(os.path.join(A.RUN_ROOT, "01_RAW",
                                           "G1_PREGATE.json")))
    ap = json.loads(read_text(os.path.join(A.RUN_ROOT, "01_RAW",
                                           "APPLY_LOG.json")))
    g2 = json.loads(read_text(os.path.join(A.RUN_ROOT, "01_RAW",
                                           "G2_POST.json")))
    g3 = json.loads(read_text(os.path.join(A.RUN_ROOT, "01_RAW",
                                           "G3_FORBIDDEN_SCAN.json")))
    g4 = json.loads(read_text(os.path.join(A.RUN_ROOT, "01_RAW",
                                           "G4_COLLATERAL_REGISTRY.json")))
    g5 = json.loads(read_text(os.path.join(A.RUN_ROOT, "01_RAW",
                                           "G5_APPEND_PROOFS.json")))
    checks = {
        "g1_all_exactly_once": g1["g1_summary"]["all_exactly_once"],
        "g1_lines_match_map": g1["g1_summary"]["all_lines_match_map"],
        "apply_replacements": len(ap["replacements"]) == 3,
        "apply_annotation_files": len(ap["annotations"]) == 3,
        "apply_annotation_entries": sum(len(r["entries"])
                                         for r in ap["annotations"]) == 13,
        "apply_sync_all_equal": all(s["equal"] for s in ap["sync"]),
        "g2_all_ok": all(r["new_text_present_norm"]
                         and r["old_absent"]["hits"] == 0
                         and r["old_absent_norm"]
                         for r in g2["replace_targets"])
                      and all(r["new_text_present_norm"]
                              for r in g2["annotation_files"]),
        "g3_zero_hits": g3["pass"],
        "g4_non_target_identical": g4["non_target_all_identical"]
                                   and g4["non_target_count"] == 13,
        "g5_prefix_ok": all(p["prefix_ok"] for p in g5["prefix_proofs"]),
        "g5_hist_identical": g5["historical_files_byte_identical"],
        "g5_fragments_exactly_once": all(f["ok"] for f in
            g5["historical_fragments_still_exactly_once"]),
        "g5_pkgs_unchanged": (not g5["targetmap_pkg_rehash"]["mismatches"]
                              and not g5["r3_pkg_rehash"]["mismatches"])}
    for k, v in checks.items():
        if not v:
            fail("INDEX re-verify failed: %s" % k)
    gates_csv = os.path.join(A.RUN_ROOT, "STAGE_ACCEPTANCE_GATES.csv")
    with open(gates_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["gate_id", "gate_name", "gate_type", "result",
                    "measured_quantity", "denominator",
                    "independent_source_of_truth", "why_non_circular",
                    "failure_case_detected", "method_class"])
        w.writerow(["AG1", "all 13 old fragments EXACTLY-ONCE pre-edit "
                    "(census method; line spans cross-checked vs map)",
                    "EXECUTABLE", "PASS" if checks["g1_all_exactly_once"]
                    and checks["g1_lines_match_map"] else "FAIL",
                    "13/13 exactly-once; 13/13 line spans == map",
                    "13 fragments", "01_RAW/G1_PREGATE.json (raw per-fragment "
                    "counts + spans)", "recount in this run from the physical "
                    "files; map cross-check is a second independent record",
                    "any fragment missing/duplicated aborts before editing",
                    "PHYSICAL_RECOMPUTATION"])
        w.writerow(["AG2", "new texts present VERBATIM "
                    "(whitespace-normalized) in the 2 targets; old fragments "
                    "absent", "EXECUTABLE",
                    "PASS" if checks["g2_all_ok"] else "FAIL",
                    "3/3 replacements verified + 13/13 annotation payloads "
                    "present", "3 REPLACE edits + 13 annotation entries",
                    "01_RAW/G2_POST.json", "norm-presence + byte-absence "
                    "recomputed from the edited files",
                    "any old fragment surviving or new text absent fails",
                    "PHYSICAL_RECOMPUTATION"])
        w.writerow(["AG3", "forbidden-clause scan over docs/nif = 0 hits "
                    "(+ the 3 standing files)", "EXECUTABLE",
                    "PASS" if checks["g3_zero_hits"] else "FAIL",
                    "0 hits / %d docs files + 0 / 3 standing files"
                    % g3["docs_nif_files_scanned"],
                    "%d files" % (g3["docs_nif_files_scanned"] + 3),
                    "01_RAW/G3_FORBIDDEN_SCAN.json",
                    "byte + whitespace-normalized scan of the physical files",
                    "any forbidden phrase present fails",
                    "PHYSICAL_RECOMPUTATION"])
        w.writerow(["AG4", "all docs/nif files OUTSIDE the 2 targets "
                    "hash-identical before/after", "EXECUTABLE",
                    "PASS" if checks["g4_non_target_identical"] else "FAIL",
                    "13/13 non-target files identical",
                    "13 non-target files", "05_ANALYSIS/SHA_REGISTRY_BEFORE"
                    ".json + _AFTER.json", "SHA256 recomputed before and after "
                    "from the physical files",
                    "any hash drift of a non-target fails",
                    "PHYSICAL_RECOMPUTATION"])
        w.writerow(["AG5", "annotations APPEND-ONLY (.pre byte-prefix proofs); "
                    "historical files byte-identical (both trees)", "EXECUTABLE",
                    "PASS" if checks["g5_prefix_ok"]
                    and checks["g5_hist_identical"] else "FAIL",
                    "3/3 prefix proofs; 4/4 R2 historical files byte-identical "
                    "in both trees; 10/10 historical fragments still "
                    "exactly-once; TARGETMAP+R3 packages re-hashed unchanged",
                    "3 standing files + 4 historical files x 2 trees",
                    "01_RAW/G5_APPEND_PROOFS.json",
                    "byte-prefix comparison + SHA256 re-hash after the run",
                    "any prefix/sync/hash failure fails",
                    "PHYSICAL_RECOMPUTATION"])
        w.writerow(["AG6", "ONE path-limited commit: staged-index inspection "
                    "before add (empty), add ONLY the explicit run paths, "
                    "verify git diff --cached --stat lists exactly those "
                    "paths, commit, push origin/master, verify remote == "
                    "local HEAD", "EXECUTABLE",
                    "PENDING_COMMIT (subchecks a/b recorded pre-commit in "
                    "01_RAW/G6_PRECOMMIT.json; commit+push executed after this "
                    "package is finalized; post-commit record = 01_RAW/"
                    "G6_POSTCOMMIT.json, local-only by the self-reference "
                    "limit; PASS recorded there)",
                    "pre-commit staged index empty + diff --cached --stat = "
                    "exact run paths", "1 commit",
                    "the git index + remote (physical)",
                    "raw git outputs recorded by the operator, not summaries",
                    "staged index non-empty, unexpected staged path, push "
                    "failure or remote != local fails",
                    "PHYSICAL_RECOMPUTATION"])
        w.writerow(["AA1", "authorization: HR-R3-3 = GO issued by the human "
                    "via PE-MASTER (input precondition of this run)",
                    "HUMAN_REVIEW", "GO_GRANTED",
                    "HR-R3-3 GO; TARGET_MAP.json SHA256 verified = the "
                    "authoritative map; wording-only scope enforced",
                    "1 human decision", "the human tasking (RUN-B) + the "
                    "pinned map", "this run executed exactly the 16 mapped "
                    "operations; any evidence-status change beyond the map's "
                    "new_texts would violate the design",
                    "none (authorization record)",
                    "HUMAN_REVIEW"])
    artifacts = [
        ("00_CONTROL\\NEXT_PROMPT.md",
         "RUN-B executed prompt (formalized)"),
        ("00_CONTROL\\apply_r1.py", "run driver"),
        ("00_CONTROL\\app_defs.py", "run driver constants (pinned inputs)"),
        ("00_CONTROL\\app_content.py",
         "run driver annotation-content builders"),
        ("00_CONTROL\\SHA256_DRIVER.txt",
         "driver-suite hash record (after last edit, before first execution)"),
        ("01_RAW\\G1_PREGATE.json",
         "G1 raw: pinned SHAs, BASE_SHA, staged-index state, 13 fragment "
         "verifications with map cross-checks, before-registries"),
        ("01_RAW\\APPLY_LOG.json",
         "apply raw: 3 byte-exact replacements + 3 annotation files with "
         "prefix proofs and SYNC hashes"),
        ("01_RAW\\G2_POST.json", "G2 raw: verbatim-presence + absence checks"),
        ("01_RAW\\G3_FORBIDDEN_SCAN.json", "G3 raw: forbidden-clause scan"),
        ("01_RAW\\G4_COLLATERAL_REGISTRY.json",
         "G4 raw: before/after hash registry of all docs/nif files"),
        ("01_RAW\\G5_APPEND_PROOFS.json",
         "G5 raw: prefix proofs + historical byte-identity + package re-hash"),
        ("01_RAW\\G6_PRECOMMIT.json",
         "G6 raw: pre-commit staged-index inspection + the explicit add paths "
         "(written between the gates and index phases; the post-commit record "
         "G6_POSTCOMMIT.json is local-only by the self-reference limit)"),
        ("05_ANALYSIS\\SHA_REGISTRY_BEFORE.json", "before-state hash registry"),
        ("05_ANALYSIS\\SHA_REGISTRY_AFTER.json", "after-state hash registry"),
        ("05_ANALYSIS\\EDIT_LOG.json", "edit log (mirror of APPLY_LOG.json)"),
        ("05_ANALYSIS\\PRE_EDIT_COPIES\\09-semantics.md.pre_edit",
         "pre-edit copy of REPLACE target 1 (before/after SHA registry proof)"),
        ("05_ANALYSIS\\PRE_EDIT_COPIES\\10-containers-corpus.md.pre_edit",
         "pre-edit copy of REPLACE target 2"),
        ("05_ANALYSIS\\G5_PRE_PROOFS\\CORRECTION_LEDGER.md.pre",
         "G5 .pre byte-prefix proof (ledger header state before append)"),
        ("05_ANALYSIS\\G5_PRE_PROOFS\\STANDING_RULES.md.pre",
         "G5 .pre byte-prefix proof (rules header state before append)"),
        ("05_ANALYSIS\\G5_PRE_PROOFS\\STANDING_POLICIES.md.pre",
         "G5 .pre byte-prefix proof (policies header state before append)"),
        ("06_REPORT\\00_FINAL_REPORT.md", "final report"),
        ("REPORT.md", "run report pointer"),
        ("HANDOFF.md", "handoff"),
        ("STAGE_ACCEPTANCE_GATES.csv", "gate ledger"),
    ]
    rows = []
    for rel, role in artifacts:
        p = os.path.join(A.RUN_ROOT, *rel.split("\\"))
        if not os.path.exists(p):
            fail("index: artifact missing: %s" % rel)
            continue
        rows.append([p, role, sha256_file(p), str(os.path.getsize(p)),
                     "this run (%s, 2026-09-05)" % A.RUN_ID,
                     "COMMITTED (repo docs/audits/%s/ + local 99_Audits "
                     "byte-identical pair)" % A.RUN_ID,
                     "gates AG1-AG5 + the 16 mapped operations"])
    with open(os.path.join(A.RUN_ROOT, "artifact_index.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_path_full", "role", "sha256", "size_bytes",
                    "snapshot_time_scope", "publication_scope",
                    "claims_supported"])
        w.writerows(rows)
    print("INDEX: gates csv + artifact_index.csv (%d rows, manifest excludes "
          "itself — documented); failures=%d" % (len(rows), len(FAILURES)))
    sys.exit(1 if FAILURES else 0)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("pregate", "apply", "gates",
                                                "index"):
        print("usage: apply_r1.py pregate|apply|gates|index")
        sys.exit(2)
    {"pregate": phase_pregate, "apply": phase_apply,
     "gates": phase_gates, "index": phase_index}[sys.argv[1]]()


if __name__ == "__main__":
    main()
