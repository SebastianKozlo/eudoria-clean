#!/usr/bin/env python3
# c1_control_persist.py -- PE_GAMEBRYO_ORACLE_TOOL_R1_20261003, correction round C1.
#
# FIX-1: re-executes the five mutation-control code paths of
#   tools/gamebryo_oracle/tests/test_gb12.py (payload_controls battery;
#   mutation + check logic copied VERBATIM below, marked as such) on SANDBOX
#   COPIES of pinned payloads and persists the raw outputs as JSON in
#   04_EVIDENCE/controls/, each labeled MEASURED_QUANTITY /
#   INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED.
# FIX-3: converts 04_EVIDENCE/gui_attempts_log.txt and gui_attempts_log2.txt
#   from UTF-16LE+BOM to plain UTF-8 verbatim, with a one-line conversion
#   header (same pattern as the E3 sgp_T1_dialog.txt fix).
# FIX-4: deletes the transient __pycache__/*.pyc build artifacts under
#   tools/gamebryo_oracle (BEFORE any import; run with python -B so no new
#   .pyc files are written) and creates tools/gamebryo_oracle/.gitignore
#   (__pycache__/ + *.pyc).
#
# Discipline: pinned payloads are opened READ-ONLY and their sha256 pins are
# verified first; every mutation is applied to an in-memory bytearray loaded
# from a sandbox copy in the OS temp sandbox. No verdict is altered here;
# raw outputs and honest check results only.

import hashlib
import json
import os
import shutil
import struct
import sys
import time
import traceback

BASE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
TOOL = os.path.join(BASE, "tools", "gamebryo_oracle")
AUD = os.path.join(BASE, "docs", "audits", "PE_GAMEBRYO_ORACLE_TOOL_R1_20261003")
CTRL_DIR = os.path.join(AUD, "04_EVIDENCE", "controls")
LOG1 = os.path.join(AUD, "04_EVIDENCE", "gui_attempts_log.txt")
LOG2 = os.path.join(AUD, "04_EVIDENCE", "gui_attempts_log2.txt")
SANDBOX = os.path.join(r"C:\Users\User\AppData\Local\Temp\opencode", "c1_gb_oracle_controls")
RUN_ID = "PE_GAMEBRYO_ORACLE_TOOL_R1_20261003_C1"
MIDFILE_WALL_RISK = ("not run in C1 on this payload: a full-decode closure "
                     "search on a corrupted 66-block NiArk body has unbounded "
                     "wall risk (E3 measured the same S_B candidate-phase cost "
                     "class on T3); the control is exercised on the T2 and "
                     "STOCK sandbox copies (T2 = payload parity with the "
                     "independent QC control set)")

T0 = time.time()
SUMMARY = {"run_id": RUN_ID, "pyc_removed": [], "gui_logs": [], "controls": {}}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest().upper()


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


def say(*parts):
    print("[C1] " + " ".join(str(p) for p in parts))


# ------------------------------------------------------------------ FIX-4 --
removed_pyc = []
for root, dirs, files in os.walk(TOOL):
    for d in sorted(list(dirs)):
        if d == "__pycache__":
            p = os.path.join(root, d)
            for f in sorted(os.listdir(p)):
                removed_pyc.append(os.path.relpath(
                    os.path.join(p, f), TOOL).replace("\\", "/"))
            shutil.rmtree(p, ignore_errors=True)
            dirs.remove(d)
gitignore_path = os.path.join(TOOL, ".gitignore")
with open(gitignore_path, "w", newline="\n") as fh:
    fh.write("__pycache__/\n*.pyc\n")
SUMMARY["pyc_removed"] = removed_pyc
say("FIX-4 removed %d .pyc files; .gitignore sha256=%s" %
    (len(removed_pyc), sha256_file(gitignore_path)))
for f in removed_pyc:
    say("  removed:", f)

# ------------------------------------------------------------------ FIX-3 --
def convert_utf16_log(path, label):
    with open(path, "rb") as fh:
        b = fh.read()
    if b[:2] != b"\xff\xfe":
        say("FIX-3", label, "SKIP: no UTF-16LE BOM (first bytes %s)" %
            b[:2].hex().upper())
        return {"label": label, "converted": False, "reason": "no UTF-16LE BOM"}
    body16 = b[2:]
    text = body16.decode("utf-16-le")
    if text.encode("utf-16-le") != body16:
        raise SystemExit("FIX-3 round-trip verification FAILED for " + label)
    sep = "\r\n" if "\r\n" in text[:2000] else "\n"
    header = ("(C1 encoding fix: this evidence file was originally captured as "
              "UTF-16LE with BOM by a PowerShell 5.1 redirect; converted "
              "verbatim to plain UTF-8 on 2026-10-03 -- log wording "
              "byte-preserved, no content change.)")
    out = header.encode("ascii") + sep.encode("ascii") + text.encode("utf-8")
    old_sha = sha256_bytes(b)
    with open(path, "wb") as fh:
        fh.write(out)
    rec = {"label": label, "converted": True, "old_sha256_utf16le": old_sha,
           "new_sha256_utf8": sha256_file(path),
           "old_bytes": len(b), "new_bytes": len(out),
           "verbatim_verified": True, "bom_before": "FF FE",
           "bom_after": "none (plain UTF-8)"}
    SUMMARY["gui_logs"].append(rec)
    say("FIX-3", label, "converted verbatim:", json.dumps(rec, sort_keys=True))


convert_utf16_log(LOG1, "gui_attempts_log.txt")
convert_utf16_log(LOG2, "gui_attempts_log2.txt")

# ----------------------------------------------------------------- imports --
sys.path.insert(0, TOOL)
import gb12core  # noqa: E402  (caches purged above; -B prevents .pyc writes)

TEST_SHA = sha256_file(os.path.join(TOOL, "tests", "test_gb12.py"))
say("test_gb12.py sha256 =", TEST_SHA)

# ------------------------------------------------------------ payload prep --
# argv entries: LABEL=path[|PIN] where PIN is a sha256 pin or "size=N".
payloads = []
for a in sys.argv[1:]:
    label, rest = a.split("=", 1)
    path, pin = (rest.split("|", 1) + [None])[:2]
    if not os.path.isfile(path):
        say("payload MISSING", label, path)
        continue
    sha = sha256_file(path)
    if pin and pin.startswith("size="):
        want = int(pin[5:])
        ok = os.path.getsize(path) == want
        pin_desc = "size=%d" % want
    elif pin:
        ok = sha == pin.upper()
        pin_desc = "sha256 pin"
    else:
        ok = True
        pin_desc = "no pin supplied"
    say("payload", label, "sha256=%s pin(%s) match=%s" % (sha, pin_desc, ok))
    if not ok:
        say("payload", label, "PIN MISMATCH -- excluded (fail-closed)")
        continue
    if os.path.isdir(SANDBOX):
        shutil.rmtree(SANDBOX)
    os.makedirs(SANDBOX)
    copy = os.path.join(SANDBOX, label + "_sandbox_copy.nif")
    shutil.copyfile(path, copy)
    if sha256_file(copy) != sha:
        raise SystemExit("sandbox copy hash mismatch for " + label)
    with open(copy, "rb") as fh:
        data = fh.read()
    payloads.append({"label": label, "source": path, "sha": sha,
                     "copy": copy, "data": data})

# ============================ control battery ===============================
# Mutation + check logic below is copied VERBATIM from
# tools/gamebryo_oracle/tests/test_gb12.py payload_controls(); only the
# capture differs (results recorded instead of printed via check()).


def battery(pl):
    """Run the five mutation controls on ONE payload's sandbox-copy bytes."""
    data = pl["data"]
    out = {}

    # baseline: unmutated original-mode decode (verbatim first battery step)
    base = gb12core.decode(data, path=pl["copy"])
    base_lr = {k: base["load_result"][k]
               for k in ("accepted", "partial", "error", "error_code")}

    # --- control: corrupted header version (verbatim) ---
    mut2 = bytearray(data)
    nl = mut2.find(b"\x0a")
    voff = nl + 1
    (v0,) = struct.unpack("<I", bytes(mut2[voff:voff + 4]))
    mut2[voff:voff + 4] = struct.pack("<I", v0 ^ 0x00400000)
    res_h = gb12core.decode(bytes(mut2), path="<corrupted-header-version>")
    ok = (res_h["load_result"]["accepted"] is False and
          res_h["load_result"]["error"] is not None)
    out["corrupted_header_version"] = {
        "mutation": "header version u32 at offset %d: 0x%08X ^ 0x00400000 -> 0x%08X"
                    % (voff, v0, v0 ^ 0x00400000),
        "check": {"name": "corrupted_header_rejected", "passed": bool(ok),
                  "expression": "load_result.accepted is False and load_result.error is not None",
                  "detail": "error=%r" % res_h["load_result"]["error"]},
        "raw_output": res_h}

    # --- control: unknown-class substitution (verbatim; NiXyzzyx per the test
    #     file -- QC's independent variant of this control used NiQCxo) ---
    mut = bytearray(data)
    probe = struct.pack("<I", 6) + b"NiNode"
    idx = mut.find(probe)
    how = "probe <u32:6>'NiNode' found at byte %d" % idx if idx != -1 else None
    if idx != -1:
        mut[idx:idx + len(probe)] = struct.pack("<I", 8) + b"NiXyzzyx"
    else:
        first_len = None
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
    out["unknown_class_mutation"] = {
        "mutation": "first RTTI-table class-name string replaced with "
                    "unregistered name 'NiXyzzyx' (%s)" % how,
        "check": {"name": "unknown_class_reported", "passed": bool(ok),
                  "expression": "error_code == 'RTTIError' and 'NiXyzzyx' in error",
                  "detail": res_u["load_result"]["error"]},
        "raw_output": res_u}

    # --- control: object-count +5 (verbatim) ---
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
    out["object_count_mutation"] = {
        "mutation": "header num_blocks %d -> %d at offset %d" % (nb, nb + 5, nboff),
        "check": {"name": "object_count_mismatch_detected", "passed": bool(ok),
                  "expression": "object_count_check.match is False or error_code in (DECODE_ERROR, INVALID_TYPE_INDEX)",
                  "detail": "count_check=%r error=%r" %
                            (res_m.get("object_count_check"),
                             res_m["load_result"]["error"])},
        "raw_output": res_m}

    # --- control: link field 0xFFFFFFFE (verbatim) ---
    res_f = gb12core.decode(data, path=pl["copy"], full_decode=True)
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
                            "mutation": "first NiNode child-link u32 (target=%d) "
                                        "replaced with 0xFFFFFFFE at byte %d"
                                        % (target, pos),
                            "check": {"name": "link_failure_detected",
                                      "passed": bool(warn),
                                      "expression": "any('LINK_FAILURE' in w for w in warnings)",
                                      "detail": "warnings=%r" %
                                                res_l.get("warnings", [])[:3]},
                            "raw_output": res_l}
                    else:
                        entry["mutation"] = ("skipped: child-link pattern not "
                                             "found after block byte_start")
                else:
                    entry["mutation"] = ("skipped: first NiNode has no integer "
                                         "children links")
                break
    out["link_failure_mutation"] = entry

    # --- control: corrupted mid-file (verbatim; full_decode=True) ---
    if pl["label"] == "T1":
        out["corrupted_midfile"] = {
            "mutation": "none (mid-file flip NOT applied in C1 on T1)",
            "check": {"name": "corruption_fail_not_silent", "passed": None,
                      "expression": "(not accepted) and (partial or error is not None)",
                      "detail": MIDFILE_WALL_RISK},
            "raw_output": None}
    else:
        mut2b = bytearray(data)
        mid = len(mut2b) // 2
        mut2b[mid] ^= 0xFF
        res_c = gb12core.decode(bytes(mut2b), path="<corrupted-midfile>",
                                full_decode=True)
        ok = ((not res_c["load_result"]["accepted"]) and
              (res_c["load_result"]["partial"] or
               res_c["load_result"]["error"] is not None))
        out["corrupted_midfile"] = {
            "mutation": "byte at %d (len//2) ^= 0xFF; decoded with full_decode=True" % mid,
            "check": {"name": "corruption_fail_not_silent", "passed": bool(ok),
                      "expression": "(not accepted) and (partial or error is not None)",
                      "detail": "accepted=%r partial=%r error=%r decode_error=%r" %
                                (res_c["load_result"]["accepted"],
                                 res_c["load_result"]["partial"],
                                 res_c["load_result"]["error"],
                                 [w for w in res_c.get("warnings", [])
                                  if "CLOSURE" in w])},
            "raw_output": res_c}

    return out, base_lr


CONTROL_LABELS = {
    "corrupted_header_version": {
        "MEASURED_QUANTITY":
            "gb12 adapter decode verdict (load_result.accepted / .error / "
            ".error_code) on a sandbox copy whose header version u32 was "
            "mutated (v XOR 0x00400000); the raw decode JSON of every run is "
            "embedded under 'runs'",
        "INDEPENDENT_SOURCE_OF_TRUTH":
            "GB 1.2 NiStream version-gate semantics (NiStream.cpp sha256 "
            "E955C36E..., E1 source canon): a header version outside the "
            "supported window must be explicitly rejected, never silently "
            "accepted",
        "WHY_NON_CIRCULAR":
            "the mutation is applied to payload bytes BEFORE decode; the "
            "verdict comes from the decoder under test while the expectation "
            "comes from the source-derived version gate, not from the "
            "decoder's own output",
    },
    "corrupted_midfile": {
        "MEASURED_QUANTITY":
            "gb12 adapter FULL-DECODE verdict (load_result.accepted / "
            ".partial / .error + warnings) on a sandbox copy with one "
            "mid-file byte flipped (data[len//2] XOR 0xFF)",
        "INDEPENDENT_SOURCE_OF_TRUTH":
            "no valid NIF decode exists for a corrupted body: the E1 "
            "source-derived LoadBinary semantics must surface the failure "
            "(error/partial + warnings), never accepted=true",
        "WHY_NON_CIRCULAR":
            "the byte flip precedes decode; the full-decode path is the tool "
            "under test; the control asserts only fail-closed behavior (never "
            "silent success), independent of any expected content",
    },
    "unknown_class_mutation": {
        "MEASURED_QUANTITY":
            "gb12 adapter decode verdict on a sandbox copy whose first "
            "RTTI-table class-name string was substituted with the "
            "unregistered name NiXyzzyx (verbatim per tests/test_gb12.py; the "
            "independent QC variant of this control used NiQCxo)",
        "INDEPENDENT_SOURCE_OF_TRUTH":
            "GB 1.2 factory registry census (Gb12_Source CoreLibs *SDM.cpp "
            "NiRegisterStream, 198 registered classes, zero NiArk*): the "
            "substituted name is absent, so the original loader must fail "
            "with RTTIError(<name>)",
        "WHY_NON_CIRCULAR":
            "the registry census is derived from the independent source tree, "
            "not from our decoder; the mutation precedes decode; a decoder "
            "that silently skipped or accepted an unknown class would be "
            "caught by this control",
    },
    "link_failure_mutation": {
        "MEASURED_QUANTITY":
            "gb12 adapter decode warnings on a sandbox copy whose first "
            "NiNode child-link u32 was replaced with the out-of-range value "
            "0xFFFFFFFE",
        "INDEPENDENT_SOURCE_OF_TRUTH":
            "GB 1.2 link semantics: linkIDs must reference existing objects; "
            "an out-of-range linkID must be flagged with a LINK_FAILURE "
            "warning per block/field, never silently ignored",
        "WHY_NON_CIRCULAR":
            "the link target is taken from the decoded object table of the "
            "same copy, but the mutation is applied to the file bytes before "
            "a fresh decode; the expectation (warning, not silence) comes "
            "from source-derived link semantics, not from the decoder",
    },
    "object_count_mutation": {
        "MEASURED_QUANTITY":
            "gb12 adapter decode verdict on a sandbox copy whose header "
            "num_blocks was mutated +5 (object_count_check.match and/or "
            "error_code DECODE_ERROR / INVALID_TYPE_INDEX)",
        "INDEPENDENT_SOURCE_OF_TRUTH":
            "GB 1.2 source invariant: header num_blocks vs decoded count "
            "(assert usRTTI < usRTTICount per source L440); a count mismatch "
            "must be detected, never silently accepted",
        "WHY_NON_CIRCULAR":
            "the count mutation precedes decode; the expectation comes from "
            "the source-derived invariant, not from the decoder; the "
            "decoder's object_count_check is the measured quantity",
    },
}

CONTROL_FILES = {
    "corrupted_header_version": "corrupted_header_version.json",
    "corrupted_midfile": "corrupted_midfile.json",
    "unknown_class_mutation": "unknown_class_mutation.json",
    "link_failure_mutation": "link_failure_mutation.json",
    "object_count_mutation": "object_count_mutation.json",
}

os.makedirs(CTRL_DIR, exist_ok=True)
acc = {cid: [] for cid in CONTROL_FILES}

for pl in payloads:
    say("battery start", pl["label"], "elapsed=%.1fs" % (time.time() - T0))
    try:
        res, base_lr = battery(pl)
    except Exception:
        say("battery EXCEPTION on", pl["label"], ":", traceback.format_exc())
        for cid in acc:
            acc[cid].append({
                "payload": pl["label"], "source_path": pl["source"],
                "source_sha256": pl["sha"], "sandbox_copy": pl["copy"],
                "error": "battery exception, see runner transcript: " +
                         traceback.format_exc(limit=3)})
        continue
    for cid, entry in res.items():
        acc[cid].append({
            "payload": pl["label"], "source_path": pl["source"],
            "source_sha256": pl["sha"], "sandbox_copy": pl["copy"],
            "baseline_original_verdict": base_lr,
            "control": entry})
        chk = entry["check"]
        say("  [%s] %s payload=%s passed=%s" %
            ("PASS" if chk["passed"] else ("SKIP" if chk["passed"] is None else "FAIL"),
             chk["name"], pl["label"], chk["passed"]))
    # incremental persistence after each payload battery
    for cid, runs in acc.items():
        detected = [r["payload"] for r in runs
                    if r.get("control", {}).get("check", {}).get("passed") is True]
        not_detected = [r["payload"] for r in runs
                        if r.get("control", {}).get("check", {}).get("passed") is False]
        skipped = [r["payload"] for r in runs
                   if r.get("control", {}).get("check", {}).get("passed") is None]
        fcd = ("a silent success in this control's failure class would FAIL "
               "the check; measured: DETECTED on %s" % detected +
               ("; NOT detected on %s (raw outputs recorded -- see per-run "
                "entries)" % not_detected if not_detected else "") +
               ("; not applicable / not run on %s (see per-run entries)" % skipped
                if skipped else ""))
        doc = {"CONTROL_ID": cid, "RUN_ID": RUN_ID,
               "EXECUTED": "2026-10-03 (correction round C1)",
               "CODE_PATH": {
                   "test_file": "tools/gamebryo_oracle/tests/test_gb12.py",
                   "test_file_sha256": TEST_SHA,
                   "mutation_logic": "copied verbatim from payload_controls()",
                   "runner": "04_EVIDENCE/scripts/c1_control_persist.py"},
               "SANDBOX_DISCIPLINE":
                   "mutations applied to in-memory bytearrays loaded from "
                   "sandbox copies in the OS temp sandbox; pinned payloads "
                   "read-only; sha256/size pins verified before use",
               "MEASURED_QUANTITY": CONTROL_LABELS[cid]["MEASURED_QUANTITY"],
               "INDEPENDENT_SOURCE_OF_TRUTH":
                   CONTROL_LABELS[cid]["INDEPENDENT_SOURCE_OF_TRUTH"],
               "WHY_NON_CIRCULAR": CONTROL_LABELS[cid]["WHY_NON_CIRCULAR"],
               "FAILURE_CASE_DETECTED": fcd,
               "runs": runs}
        p = os.path.join(CTRL_DIR, CONTROL_FILES[cid])
        dump_json(p, doc)
        SUMMARY["controls"][CONTROL_FILES[cid]] = sha256_file(p)

# ------------------------------------------------------------- final checks --
pycache_left = []
for root, dirs, files in os.walk(TOOL):
    for d in dirs:
        if d == "__pycache__":
            for f in os.listdir(os.path.join(root, d)):
                pycache_left.append(os.path.relpath(
                    os.path.join(root, d, f), TOOL))
    for f in files:
        if f.endswith(".pyc"):
            pycache_left.append(os.path.relpath(os.path.join(root, f), TOOL))
SUMMARY["pyc_remaining_after_run"] = pycache_left

for fn, sha in sorted(SUMMARY["controls"].items()):
    p = os.path.join(CTRL_DIR, fn)
    with open(p, "r") as fh:
        json.load(fh)  # parseability check
    say("control JSON ok:", fn, sha)

say("pyc remaining after run:", pycache_left)
say("total elapsed %.1fs" % (time.time() - T0))
print("C1_RUN_SUMMARY: " + json.dumps(SUMMARY, sort_keys=True))
