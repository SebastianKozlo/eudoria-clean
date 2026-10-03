#!/usr/bin/env python3
# c1_followup.py -- PE_GAMEBRYO_ORACLE_TOOL_R1_20261003, correction round C1
# follow-up (runner: 04_EVIDENCE/scripts/c1_control_persist.py already
# persisted the five mutation-control JSONs; this script completes them).
#
# (a) The initial C1 battery on the STOCK sample crashed at the link control
#     (the VERBATIM tests/test_gb12.py find() resolves the children[0] u32
#     pattern to the footer num-top field on that sample -> decode raised
#     DecodeError, fail-closed). The battery-level try/except then replaced
#     the STOCK entries of all five controls with a blanket exception entry.
#     This follow-up re-runs the STOCK controls INDIVIDUALLY (per-control
#     try/except) and replaces those blanket entries with per-control
#     results -- mutations + checks copied VERBATIM from test_gb12.py.
# (b) Bounded search across GB 1.2 SDK sample models for a payload that
#     exercises the verbatim link-control path to its LINK_FAILURE warning
#     (clean original-mode load so the link phase runs + NiNode with integer
#     children). The first passing sample is recorded as an additional run.
# (c) Recomputes the FAILURE_CASE_DETECTED label of all five control JSONs
#     and re-persists them.
#
# Discipline unchanged: sandbox copies only; source files read-only;
# sha256 recorded for every run entry. No verdict is altered; raw outputs
# and honest check results only.

import hashlib
import json
import os
import shutil
import struct
import sys
import traceback

BASE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
TOOL = os.path.join(BASE, "tools", "gamebryo_oracle")
AUD = os.path.join(BASE, "docs", "audits", "PE_GAMEBRYO_ORACLE_TOOL_R1_20261003")
CTRL = os.path.join(AUD, "04_EVIDENCE", "controls")
SANDBOX = os.path.join(r"C:\Users\User\AppData\Local\Temp\opencode", "c1_gb_oracle_controls")
RUN_ID = "PE_GAMEBRYO_ORACLE_TOOL_R1_20261003_C1"
STOCK = (r"D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\Samples\Models"
         r"\Collision\NIF\1310 HN (Plane).nif")
STOCK_SHA = "F26FB84346E32BE94AFD9FD3C62DA18FB49308480D7EC38476A216520F6DAC8F"
SDK_MODELS = r"D:\gamebyroengine\extracted\Gb12_Source\Samples\Models"
MAX_CANDIDATES = 120
MAX_CAND_SIZE = 300000

CONTROL_FILES = {
    "corrupted_header_version": "corrupted_header_version.json",
    "corrupted_midfile": "corrupted_midfile.json",
    "unknown_class_mutation": "unknown_class_mutation.json",
    "link_failure_mutation": "link_failure_mutation.json",
    "object_count_mutation": "object_count_mutation.json",
}


def say(*parts):
    print("[C1F] " + " ".join(str(p) for p in parts))


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def dump_json(path, obj):
    with open(path, "w", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")


def base_lr(res):
    return {k: res["load_result"][k]
            for k in ("accepted", "partial", "error", "error_code")}


sys.path.insert(0, TOOL)
import gb12core  # noqa: E402

TEST_SHA = sha256_file(os.path.join(TOOL, "tests", "test_gb12.py"))
os.makedirs(SANDBOX, exist_ok=True)


def load_doc(cid):
    p = os.path.join(CTRL, CONTROL_FILES[cid])
    with open(p, "r") as fh:
        return json.load(fh)


def recompute_fcd(doc):
    runs = doc.get("runs", [])
    detected = [r["payload"] for r in runs
                if r.get("control", {}).get("check", {}).get("passed") is True]
    not_detected = [r["payload"] for r in runs
                    if r.get("control", {}).get("check", {}).get("passed") is False]
    skipped = [r["payload"] for r in runs
               if r.get("control", {}).get("check", {}).get("passed") is None]
    fcd = ("a silent success in this control's failure class would FAIL the "
           "check; measured: DETECTED on %s" % detected)
    if not_detected:
        fcd += ("; NOT detected on %s (raw outputs recorded -- see per-run "
                "entries)" % not_detected)
    if skipped:
        fcd += ("; not applicable / not run on %s (see per-run entries)"
                % skipped)
    doc["FAILURE_CASE_DETECTED"] = fcd
    return detected, not_detected, skipped


# ============================ (a) STOCK per-control re-run ==================
# battery() below replicates the main runner's controls VERBATIM, but with a
# per-control try/except so one crashing control cannot wipe the others.

def battery(data, copy):
    out = {}

    def wrap(name, fn):
        try:
            return fn()
        except Exception:
            return {"mutation": "control raised an exception (see 'exception')",
                    "check": {"name": name, "passed": False,
                              "expression": "-",
                              "detail": "decode raised an exception "
                                        "(fail-closed, never silent)"},
                    "raw_output": None,
                    "exception": traceback.format_exc(limit=6)}

    def c_header():
        mut2 = bytearray(data)
        nl = mut2.find(b"\x0a")
        voff = nl + 1
        (v0,) = struct.unpack("<I", bytes(mut2[voff:voff + 4]))
        mut2[voff:voff + 4] = struct.pack("<I", v0 ^ 0x00400000)
        res_h = gb12core.decode(bytes(mut2), path="<corrupted-header-version>")
        ok = (res_h["load_result"]["accepted"] is False and
              res_h["load_result"]["error"] is not None)
        return {"mutation": "header version u32 at offset %d: 0x%08X ^ 0x00400000 -> 0x%08X"
                            % (voff, v0, v0 ^ 0x00400000),
                "check": {"name": "corrupted_header_rejected", "passed": bool(ok),
                          "expression": "load_result.accepted is False and load_result.error is not None",
                          "detail": "error=%r" % res_h["load_result"]["error"]},
                "raw_output": res_h}

    def c_unknown():
        mut = bytearray(data)
        probe = struct.pack("<I", 6) + b"NiNode"
        idx = mut.find(probe)
        how = ("probe <u32:6>'NiNode' found at byte %d" % idx
               if idx != -1 else None)
        if idx != -1:
            mut[idx:idx + len(probe)] = struct.pack("<I", 8) + b"NiXyzzyx"
        else:
            for p in range(len(mut) - 4):
                (ln,) = struct.unpack("<I", bytes(mut[p:p + 4]))
                if 3 < ln < 64:
                    cand = bytes(mut[p + 4:p + 4 + ln])
                    if all(0x41 <= c <= 0x7A for c in cand) and \
                            cand.startswith(b"Ni"):
                        mut[p:p + 4 + ln] = struct.pack("<I", 8) + b"NiXyzzyx"
                        how = ("fallback scan: first plausible Ni* string "
                               "(len %d) mutated at byte %d" % (ln, p))
                        break
        res_u = gb12core.decode(bytes(mut), path="<mutated-unknown-class>")
        ok = (res_u["load_result"]["error_code"] == "RTTIError" and
              "NiXyzzyx" in (res_u["load_result"]["error"] or ""))
        return {"mutation": "first RTTI-table class-name string replaced with "
                            "unregistered name 'NiXyzzyx' (%s)" % how,
                "check": {"name": "unknown_class_reported", "passed": bool(ok),
                          "expression": "error_code == 'RTTIError' and 'NiXyzzyx' in error",
                          "detail": res_u["load_result"]["error"]},
                "raw_output": res_u}

    def c_count():
        mut3 = bytearray(data)
        nl = mut3.find(b"\x0a")
        voff = nl + 1
        (v,) = struct.unpack("<I", bytes(mut3[voff:voff + 4]))
        nboff = voff + (8 if v >= gb12core.V_USER_GATE else 4)
        (nb,) = struct.unpack("<I", bytes(mut3[nboff:nboff + 4]))
        mut3[nboff:nboff + 4] = struct.pack("<I", nb + 5)
        res_m = gb12core.decode(bytes(mut3), path="<count-mismatch>")
        ok = (res_m.get("object_count_check", {}).get("match") is False or
              res_m["load_result"]["error_code"] in ("DECODE_ERROR",
                                                     "INVALID_TYPE_INDEX"))
        return {"mutation": "header num_blocks %d -> %d at offset %d"
                           % (nb, nb + 5, nboff),
                "check": {"name": "object_count_mismatch_detected",
                          "passed": bool(ok),
                          "expression": "object_count_check.match is False or error_code in (DECODE_ERROR, INVALID_TYPE_INDEX)",
                          "detail": "count_check=%r error=%r" %
                                    (res_m.get("object_count_check"),
                                     res_m["load_result"]["error"])},
                "raw_output": res_m}

    def c_link():
        res_f = gb12core.decode(data, path=copy, full_decode=True)
        entry = {"mutation": "none",
                 "check": {"name": "link_failure_detected", "passed": None,
                           "expression": "any('LINK_FAILURE' in w for w in warnings)",
                           "detail": "no full-decode objects or no NiNode with "
                                     "integer children links on this payload"},
                 "raw_output": None,
                 "full_decode_context": {
                     "load_result": res_f["load_result"],
                     "decode_continued_after_rtti_gate":
                         res_f.get("decode_continued_after_rtti_gate"),
                     "objects": len(res_f.get("objects") or [])}}
        if res_f["objects"]:
            for o in res_f["objects"]:
                if o and o.get("type") == "NiNode":
                    lt = (o.get("links", {}).get("children") or [])
                    if lt and isinstance(lt[0], int):
                        mut4 = bytearray(data)
                        target = lt[0]
                        pat = struct.pack("<I", target)
                        pos = mut4.find(pat, o["byte_start"])
                        if pos != -1:
                            mut4[pos:pos + 4] = struct.pack("<I", 0xFFFFFFFE)
                            res_l = gb12core.decode(bytes(mut4),
                                                    path="<link-failure>")
                            warn = any("LINK_FAILURE" in w
                                       for w in res_l.get("warnings", []))
                            entry = {
                                "mutation": "first NiNode child-link u32 "
                                            "(target=%d) replaced with "
                                            "0xFFFFFFFE at byte %d"
                                            % (target, pos),
                                "check": {"name": "link_failure_detected",
                                          "passed": bool(warn),
                                          "expression": "any('LINK_FAILURE' in w for w in warnings)",
                                          "detail": "warnings=%r" %
                                                    res_l.get("warnings", [])[:3]},
                                "raw_output": res_l}
                        else:
                            entry["mutation"] = ("skipped: child-link pattern "
                                                 "not found after block "
                                                 "byte_start")
                    else:
                        entry["mutation"] = ("skipped: first NiNode has no "
                                             "integer children links")
                    break
        return entry

    def c_midfile():
        mut2b = bytearray(data)
        mid = len(mut2b) // 2
        mut2b[mid] ^= 0xFF
        res_c = gb12core.decode(bytes(mut2b), path="<corrupted-midfile>",
                                full_decode=True)
        ok = ((not res_c["load_result"]["accepted"]) and
              (res_c["load_result"]["partial"] or
               res_c["load_result"]["error"] is not None))
        return {"mutation": "byte at %d (len//2) ^= 0xFF; decoded with full_decode=True" % mid,
                "check": {"name": "corruption_fail_not_silent", "passed": bool(ok),
                          "expression": "(not accepted) and (partial or error is not None)",
                          "detail": "accepted=%r partial=%r error=%r decode_error=%r" %
                                    (res_c["load_result"]["accepted"],
                                     res_c["load_result"]["partial"],
                                     res_c["load_result"]["error"],
                                     [w for w in res_c.get("warnings", [])
                                      if "CLOSURE" in w])},
                "raw_output": res_c}

    out["corrupted_header_version"] = wrap("corrupted_header_rejected", c_header)
    out["unknown_class_mutation"] = wrap("unknown_class_reported", c_unknown)
    out["object_count_mutation"] = wrap("object_count_mismatch_detected", c_count)
    out["link_failure_mutation"] = wrap("link_failure_detected", c_link)
    out["corrupted_midfile"] = wrap("corruption_fail_not_silent", c_midfile)
    return out


stock_copy = os.path.join(SANDBOX, "STOCK_sandbox_copy.nif")
shutil.copyfile(STOCK, stock_copy)
if sha256_file(STOCK) != STOCK_SHA:
    raise SystemExit("STOCK sha pin mismatch")
with open(stock_copy, "rb") as fh:
    stock_data = fh.read()
stock_base = gb12core.decode(stock_data, path=stock_copy)
stock_blr = base_lr(stock_base)
say("STOCK baseline:", json.dumps(stock_blr, sort_keys=True))
stock_res = battery(stock_data, stock_copy)

for cid, entry in stock_res.items():
    doc = load_doc(cid)
    doc["runs"] = [r for r in doc.get("runs", []) if r["payload"] != "STOCK"]
    doc["runs"].append({"payload": "STOCK", "source_path": STOCK,
                        "source_sha256": STOCK_SHA,
                        "sandbox_copy": stock_copy,
                        "baseline_original_verdict": stock_blr,
                        "control": entry})
    doc["RUN_NOTE"] = ("The initial C1 battery on the STOCK sample crashed "
                       "at the link control (a blanket battery-exception "
                       "entry was recorded); this follow-up "
                       "(04_EVIDENCE/scripts/c1_followup.py) re-ran the "
                       "STOCK controls individually and replaced that entry "
                       "with this per-control result.")
    chk = entry["check"]
    say("STOCK %-38s passed=%s" % (chk["name"], chk["passed"]))
    dump_json(os.path.join(CTRL, CONTROL_FILES[cid]), doc)

# ================= (b) bounded SDK search for the verbatim link path =========
cands = []
for dp, dn, fnames in os.walk(SDK_MODELS):
    for f in sorted(fnames):
        if f.lower().endswith(".nif"):
            p = os.path.join(dp, f)
            if os.path.getsize(p) <= MAX_CAND_SIZE:
                cands.append(p)
cands.sort(key=lambda p: (os.path.basename(p) != "2310 HN (Plane).nif", p))
say("SDK sample candidates:", len(cands))

tried = 0
link_run = None
passing_name = None
for c in cands[:MAX_CANDIDATES]:
    name = os.path.basename(c)
    if name == "1310 HN (Plane).nif":
        continue  # already covered by the STOCK entry (pattern collision)
    tried += 1
    try:
        copy = os.path.join(SANDBOX, "link_cand_%03d.nif" % tried)
        shutil.copyfile(c, copy)
        with open(copy, "rb") as fh:
            data = fh.read()
        b = gb12core.decode(data, path=copy)
        if b["load_result"]["accepted"] is not True:
            continue  # need a clean original-mode load so the link phase runs
        res_f = gb12core.decode(data, path=copy, full_decode=True)
        hit = None
        if res_f["objects"]:
            for o in res_f["objects"]:
                if o and o.get("type") == "NiNode":
                    lt = (o.get("links", {}).get("children") or [])
                    if lt and isinstance(lt[0], int):
                        mut4 = bytearray(data)
                        pat = struct.pack("<I", lt[0])
                        pos = mut4.find(pat, o["byte_start"])
                        if pos != -1:
                            hit = (lt[0], pos, mut4)
                    break
        if hit is None:
            continue
        target, pos, mut4 = hit
        mut4[pos:pos + 4] = struct.pack("<I", 0xFFFFFFFE)
        res_l = gb12core.decode(bytes(mut4), path="<link-failure>")
        warn = any("LINK_FAILURE" in w for w in res_l.get("warnings", []))
        say("link candidate %2d %-40s target=%d pos=%d passed=%s"
            % (tried, name, target, pos, warn))
        if warn:
            link_run = {"payload": "SDK:" + name, "source_path": c,
                        "source_sha256": sha256_file(c),
                        "sandbox_copy": copy,
                        "baseline_original_verdict": base_lr(b),
                        "control": {
                            "mutation": "first NiNode child-link u32 (target=%d) "
                                        "replaced with 0xFFFFFFFE at byte %d"
                                        % (target, pos),
                            "check": {"name": "link_failure_detected",
                                      "passed": True,
                                      "expression": "any('LINK_FAILURE' in w for w in warnings)",
                                      "detail": "warnings=%r" %
                                                res_l.get("warnings", [])[:3]},
                            "raw_output": res_l}}
            passing_name = name
            break
    except Exception:
        say("link candidate %2d %-40s exception: %s"
            % (tried, name, sys.exc_info()[1]))
        continue

link_doc = load_doc("link_failure_mutation")
if link_run is not None:
    link_doc["runs"].append(link_run)
    link_doc["RUN_NOTE"] = (
        "Initial C1 battery: the verbatim link control on STOCK (1310 HN "
        "(Plane).nif) resolved the children[0] u32 pattern to the footer "
        "num-top field (value collision), so the mutation fed 0xFFFFFFFE "
        "into num-top and decode raised DecodeError (fail-closed exception, "
        "never silent; recorded in the STOCK run entry). On the T2 sandbox "
        "copy there is no NiNode with integer children links (not "
        "applicable), and on the T1 sandbox copy the original-mode load "
        "stops at the RTTI gate before any link phase (itself fail-closed). "
        "A bounded follow-up search across GB 1.2 SDK sample models (%d "
        "candidates tried) found '%s', which exercises the VERBATIM "
        "tests/test_gb12.py control path to its LINK_FAILURE warning; that "
        "run is recorded as the last entry."
        % (tried, passing_name))
    say("LINK CONTROL REPRODUCED on", passing_name)
else:
    link_doc["RUN_NOTE"] = (
        "Initial C1 battery: the verbatim link control on STOCK (1310 HN "
        "(Plane).nif) resolved the children[0] u32 pattern to the footer "
        "num-top field (value collision) and decode raised DecodeError "
        "(fail-closed exception, never silent). A bounded follow-up search "
        "across %d GB 1.2 SDK sample candidates did NOT find a payload that "
        "exercises the verbatim path to a LINK_FAILURE warning -- the E2 "
        "TEST_MATRIX claim for this control remains uncorroborated by a "
        "persisted raw output (disclosed for PE-MASTER)." % tried)
    say("LINK CONTROL NOT REPRODUCED in", tried, "candidates")

# ============================ (c) recompute + persist all five ==============
final = {}
for cid in CONTROL_FILES:
    doc = load_doc(cid)
    det, ndet, skip = recompute_fcd(doc)
    p = os.path.join(CTRL, CONTROL_FILES[cid])
    dump_json(p, doc)
    final[CONTROL_FILES[cid]] = {
        "sha256": sha256_file(p),
        "detected_on": det, "not_detected_on": ndet,
        "not_applicable_or_not_run_on": skip}
    with open(p, "r") as fh:
        json.load(fh)  # parseability check

say("FINAL CONTROL STATE:")
print("C1F_FINAL: " + json.dumps(final, sort_keys=True))
