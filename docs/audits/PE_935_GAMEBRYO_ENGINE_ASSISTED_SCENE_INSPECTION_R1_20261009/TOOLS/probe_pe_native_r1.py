#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_pe_native_r1.py — Native stock-printer execution on the SELECTED PE
payloads (Work Package C, contract section 9) for RUN_ID
PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009.

LINEAGE DISCLOSURE — REUSED CODE (adapted copy of THIS RUN's own
TOOLS/probe_sdk_tools_r1.py, which is itself an adapted copy of the Desktop
probe_tools.py; lineage chain in 01_SDK/SOURCE_AND_BUILD_IDENTITIES.json):
- same run harness (subprocess + CREATE_NO_WINDOW + SetErrorMode + per-process
  30 s timeout + CHILD_PROCESS_PATH_DLL_EXPOSURE);
- same stdout visit parser (BOTH PrintID forms) and populated-scene rule;
- same per-run provenance fields (argv, cwd, env delta, input SHA, exe SHA,
  exit, raw stdout/stderr paths, timeout).

PE-specific additions:
- inputs are this run's fresh LOCAL_ONLY extractions (never the original
  container directly; container identity re-verified here);
- per-input SOURCE_PREDICTED first missing factory from the serialized class
  table (table order) vs the measured stock registry — labeled SEPARATELY from
  the observed native report (contract section 9);
- populated-scene rule enforced: exit 0 alone is NEVER sufficient.

No PE client execution. No GUI. No original/container/SDK modification.
"""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ORACLE_COPY = os.path.join(HERE, "gamebryo_oracle_r1")
sys.path.insert(0, ORACLE_COPY)
from adapters.gb12 import registry as gb12_registry  # noqa: E402

RUN_ID = "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009"
TOOL = Path(r"D:\gamebyroengine\extracted\Gb12_Source\Tools\DeveloperTools"
            r"\SceneGraphPrinter\Win32\VC71\SceneGraphPrinter.exe")
RUNTIME = Path(r"D:\gamebyroengine\extracted\Gb112_tools_setup")
OUT_ROOT = Path(r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
                r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PE_OUT = OUT_ROOT / "02_PE"
RAW = PE_OUT / "raw"
LOCAL_ROOT = Path(r"D:\Eudoria_Reconstruction\99_Audits"
                  r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PAYLOAD_DIR = LOCAL_ROOT / "02_PE_payloads"
ARCHIVE = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
MODELS_SHA = "C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0"
TIMEOUT_S = 30
FLAGS = ["-trans", "-extra", "-prop", "-geom", "-bs", "-mem"]

SELECTED = ["218757.nif", "496633.nif", "512126.nif", "423020.nif"]


def ident(p):
    b = p.read_bytes()
    return {"path": str(p), "size_bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest()}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


VISIT_RE = re.compile(
    r"^\s*(\d+) - ([A-Za-z0-9_]+)(?::<([^>]*)>)?(?:\s+<0x([0-9A-Fa-f]+)>)?\s*$")
ANY_NUMBERED_RE = re.compile(r"^\s*\d+ - ")


def parse_stdout(text):
    rows = []
    for line in text.splitlines():
        m = VISIT_RE.match(line)
        if m:
            rows.append({"depth": int(m.group(1)), "class": m.group(2),
                         "name": m.group(3), "address": m.group(4)})
    numbered_lines = [ln for ln in text.splitlines()
                      if ANY_NUMBERED_RE.match(ln)]
    unaccounted = [ln for ln in numbered_lines if not VISIT_RE.match(ln)]
    summary = re.search(r"Total Object Count: (\d+), Tree Depth: (\d+)", text)
    uniq_addr = len({r["address"] for r in rows if r["address"]})
    visits_with_addr = sum(1 for r in rows if r["address"])
    return {
        "numbered_visit_rows_parsed": len(rows),
        "numbered_lines_in_raw": len(numbered_lines),
        "numbered_lines_unaccounted": len(unaccounted),
        "unaccounted_examples": unaccounted[:5],
        "unique_printed_addresses": uniq_addr,
        "visits_without_address_token": len(rows) - visits_with_addr,
        "reported_summary": ([int(summary.group(1)), int(summary.group(2))]
                             if summary else None),
        "class_histogram": dict(__import__("collections").Counter(
            r["class"] for r in rows)),
        "depth_histogram": dict(sorted(
            __import__("collections").Counter(r["depth"] for r in rows).items())),
        "first_rows": rows[:10],
    }


def predicted_first_missing_factory(path, reg):
    """SOURCE_PREDICTED (not observed): the original GB 1.2 LoadRTTI scans the
    complete RTTI table in SOURCE TABLE ORDER; the FIRST unregistered name is
    the deterministic source-predicted rejection point. Reads the serialized
    type table from the payload bytes (documented 10.1 header layout)."""
    data = Path(path).read_bytes()
    nl = data.index(b"\x0A")
    r = nl + 1
    ver, = struct.unpack_from("<I", data, r)
    r += 4
    if ver != 0x0A010000:
        return {"version_hex": "0x%08X" % ver,
                "note": "non-10.1 file: table-order prediction not derived"}
    uv, = struct.unpack_from("<I", data, r)
    r += 4
    nb, = struct.unpack_from("<I", data, r)
    r += 4
    nbt, = struct.unpack_from("<H", data, r)
    r += 2
    names = []
    for i in range(nbt):
        ln, = struct.unpack_from("<I", data, r)
        r += 4
        names.append(data[r:r + ln].decode("ascii"))
        r += ln
    for i, nm in enumerate(names):
        if nm not in reg:
            return {"version_hex": "0x%08X" % ver, "user_version": uv,
                    "num_blocks": nb, "num_block_types": nbt,
                    "first_unregistered_table_name": nm,
                    "first_miss_table_index": i,
                    "unregistered_table_names": [x for x in names
                                                  if x not in reg]}
    return {"version_hex": "0x%08X" % ver, "user_version": uv,
            "num_blocks": nb, "num_block_types": nbt,
            "first_unregistered_table_name": None,
            "note": "all table names registered"}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    models_sha = sha256_file(ARCHIVE)
    if models_sha != MODELS_SHA:
        raise SystemExit("E_INPUT_HASH: Models.bnt changed vs pin")
    reg = set(gb12_registry.GB12_REGISTERED_CLASSES)
    tool_before = ident(TOOL)
    dll_identities = [ident(RUNTIME / n) for n in ("MSVCP71.DLL", "MSVCR71.DLL")]
    payload_identities = {n: ident(PAYLOAD_DIR / n) for n in SELECTED}

    env = os.environ.copy()
    env["PATH"] = str(RUNTIME) + ";" + env.get("PATH", "")
    old_error_mode = ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
    results = []
    try:
        for name in SELECTED:
            p = PAYLOAD_DIR / name
            case = "PE_" + name.rsplit(".", 1)[0]
            command = [str(TOOL), "-in", str(p)] + FLAGS
            out = RAW / (case + ".stdout.txt")
            err = RAW / (case + ".stderr.txt")
            r = {
                "case": case, "kind": "PE_SELECTED_PAYLOAD",
                "input": str(p),
                "input_identity": ident(p),
                "command": command,
                "cwd": str(PAYLOAD_DIR),
                "child_env_delta": {"PATH": "+" + str(RUNTIME)
                                    + ";<inherited PATH>"},
                "child_env_delta_class": "CHILD_PROCESS_PATH_DLL_EXPOSURE",
                "timeout_s": TIMEOUT_S,
                "stdout_raw_path": str(out), "stderr_raw_path": str(err),
            }
            with out.open("wb") as of, err.open("wb") as ef:
                try:
                    proc = subprocess.run(command, cwd=str(PAYLOAD_DIR),
                                          env=env, stdout=of, stderr=ef,
                                          timeout=TIMEOUT_S,
                                          creationflags=subprocess.CREATE_NO_WINDOW,
                                          check=False)
                    r["exit_code"] = proc.returncode
                    r["timeout"] = False
                except subprocess.TimeoutExpired:
                    r["exit_code"] = None
                    r["timeout"] = True
                except OSError as ex:
                    r["exit_code"] = None
                    r["timeout"] = False
                    r["launch_error"] = str(ex)
            text = out.read_bytes().decode("cp1252", errors="replace")
            errtext = err.read_bytes().decode("cp1252", errors="replace")
            parsed = parse_stdout(text)
            r.update(stderr_text=errtext,
                     stdout_size=out.stat().st_size,
                     stderr_size=err.stat().st_size,
                     parsed_summary=parsed,
                     executable_identity_at_run=tool_before,
                     scope="PE_ORIGINAL_INPUT_UNCHANGED_COPY")
            # populated-scene rule (preregistered; exit 0 alone insufficient)
            rep = parsed["reported_summary"] or [0, 0]
            r["populated_scene_check"] = {
                "exit_zero": r.get("exit_code") == 0,
                "numbered_visits": parsed["numbered_visit_rows_parsed"],
                "reported_total_object_count": rep[0],
                "POPULATED_SCENE_INSPECTION": (
                    r.get("exit_code") == 0
                    and parsed["numbered_visit_rows_parsed"] >= 1
                    and rep[0] > 0),
            }
            if (r.get("exit_code") == 1
                    and errtext.strip() == "Error loading stream."
                    and parsed["numbered_visit_rows_parsed"] == 0):
                r["native_outcome_class"] = "NATIVE_LOAD_REJECTED"
                r["native_error_specificity"] = (
                    "GENERIC — the stock binary prints the identical message "
                    "for every load failure (Package B C11 specificity FAIL); "
                    "the binary alone does NOT identify the failing class")
            elif r.get("exit_code") == 0 and not \
                    r["populated_scene_check"]["POPULATED_SCENE_INSPECTION"]:
                r["native_outcome_class"] = (
                    "EXIT_ZERO_NOT_POPULATED (preregistered rule: empty "
                    "output + exit 0 is NOT a populated scene inspection)")
            elif r.get("timeout"):
                r["native_outcome_class"] = "TIMEOUT (measured result)"
            else:
                r["native_outcome_class"] = "MEASURED (see parsed summary)"
            # SOURCE-PREDICTED first missing factory (SEPARATE namespace)
            r["source_predicted_first_missing_factory"] = predicted_first_missing_factory(p, reg)
            r["source_predicted_label"] = (
                "SOURCE_PREDICTED_FROM_PINNED_SDK_REGISTRY_AND_SERIALIZED_TABLE "
                "— NOT an observed native report")
            results.append(r)
    finally:
        ctypes.windll.kernel32.SetErrorMode(old_error_mode)

    tool_after = ident(TOOL)
    unchanged = {
        "tool_unchanged": tool_after == tool_before,
        "tool_after": tool_after,
        "dlls_unchanged": all(ident(RUNTIME / n["path"].split("\\")[-1]) == n
                              for n in dll_identities),
        "payloads_unchanged": all(ident(PAYLOAD_DIR / n) == v
                                  for n, v in payload_identities.items()),
    }
    result = {
        "run_id": RUN_ID,
        "phase": "02_PE native execution (Work Package C, contract section 9)",
        "tool_identity": tool_before,
        "dll_identities": dll_identities,
        "container_identity_reverified": {
            "path": ARCHIVE, "sha256": models_sha,
            "pin_match": models_sha == MODELS_SHA},
        "payload_identities": payload_identities,
        "execution_environment": {
            "dll_exposure_class": "CHILD_PROCESS_PATH_DLL_EXPOSURE",
            "path_prepend": str(RUNTIME),
            "per_process_timeout_s": TIMEOUT_S,
            "launcher_error_mode": "SetErrorMode(SEM_FAILCRITICALERRORS|"
                                   "SEM_NOOPENFILEERRORBOX|SEM_NOGPFAULTERRORBOX)",
            "flags": FLAGS,
            "cwd": str(PAYLOAD_DIR),
            "populated_scene_rule": "exit 0 AND >=1 numbered visit AND "
                                    "nonzero Total Object Count (Package B "
                                    "preregistered rule; exit 0 alone never "
                                    "sufficient)",
        },
        "cases": results,
        "originals_unchanged_after_runs": unchanged,
        "client_executed": False,
        "gui_executed": False,
        "global_environment_changed": False,
        "note": ("native pointer values (-mem), if any, are SDK-process "
                 "addresses, NOT PCG pointers/block IDs/asset IDs; -trans is "
                 "LOCAL post-Update state; -bs is a WORLD BOUND, not a "
                 "pivot/position."),
    }
    (PE_OUT / "NATIVE_EXECUTION_RESULTS.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "tool_unchanged": unchanged["tool_unchanged"],
        "payloads_unchanged": unchanged["payloads_unchanged"],
        "cases": [{"case": r["case"], "exit_code": r.get("exit_code"),
                   "timeout": r.get("timeout"),
                   "stderr": r["stderr_text"][:60],
                   "outcome": r["native_outcome_class"],
                   "populated": r["populated_scene_check"]["POPULATED_SCENE_INSPECTION"],
                   "predicted_first_miss": (r["source_predicted_first_missing_factory"]
                                            .get("first_unregistered_table_name"))}
                  for r in results],
    }, indent=2))


if __name__ == "__main__":
    main()
