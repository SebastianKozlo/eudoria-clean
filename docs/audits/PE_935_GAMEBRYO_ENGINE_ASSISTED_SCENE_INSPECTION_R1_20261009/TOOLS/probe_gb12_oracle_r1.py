#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""probe_gb12_oracle_r1.py â€” QUALIFY and use the ONE optional native helper
(Work Package C, contract section 11) for RUN_ID
PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009.

HELPER: the EXISTING custom gb12_oracle.exe (NOT the unmodified vendor
printer; NOT newly built this run):
  PATH D:\gamebyroengine\extracted\gb12_build\bin\gb12_oracle.exe
  594944 B, SHA256 DD7112A41D83557395C5D31F72C89BFEA3D7906AB28EF4DD3C4BD8E398EB046C
  (identity re-verified here against the contract pin).

WHY THIS HELPER (the required distinction the stock printer cannot expose):
contract section 9 requires separating an OBSERVED native error from a
SOURCE-PREDICTED first missing factory. The stock binary prints only the
generic "Error loading stream." (Package B C11 specificity FAIL) â€” it cannot
identify the failing class. gb12_oracle loads through the SAME stock GB 1.2.2
NiStream + stock factory registry (zero NiArk loaders, zero dummy factories)
and additionally prints NiStream::GetLastError()/GetLastErrorMessage() â€”
turning the specific failing class into an OBSERVED native fact.

PROVENANCE INSPECTED BEFORE INVOCATION (this phase):
  - source: D:\gamebyroengine\extracted\gb12_build\oracle\oracle.cpp
    (771 lines; SHA256 AD1F5DED06FA17AE77D9A5077CE2704404451FA0A751FA59F76EF9A24A9E591A
    re-measured this phase). Header: "CLI NIF loader-oracle built from full
    Gamebryo 1.2.2 source (legal use of possessed NDL-licensed sources; the
    compiled 1.1.2 evaluation tools are timelocked and must NOT be patched â€”
    this oracle is the sanctioned path)". Build tag: EU935_GB12_ORACLE_BUILD_R1.
  - interface (oracle.cpp main, L500-541): gb12_oracle.exe <file.nif>
    [--dump blocks|tree|keyframes|skin] [--json out.json]; exit 0 = load OK,
    1 = load FAIL (explicit engine error), 2 = usage.
  - load verdict JSON fields (L562-580): "load": OK|FAIL, "lastError": enum,
    "lastErrorMessage": string, "nifVersion", "numBlocks", "numTopObjects".
  - binary imports: NO MSVCP71/MSVCR71 import strings (unlike the stock
    printer) â€” the child-PATH DLL exposure class is kept for uniformity but
    has no effect on this executable (recorded honestly).

DISCLOSED BEHAVIOR DIFFERENCES FROM THE UNMODIFIED STOCK PRINTER:
  1. Different executable (custom source build; the vendor binary stays
     untouched and remains the mandatory printer).
  2. OracleStream derives from NiStream and snapshots the full object list
     during load via the PUBLIC static NiStream::RegisterPostProcessFunction
     (runs inside LoadStream before FreeLoadData) â€” ZERO engine changes, but
     an added observation hook the stock printer does not have.
  3. Prints NiStream::GetLastError()/GetLastErrorMessage() â€” the SPECIFIC load
     error (the stock printer never calls it; measured C11 FAIL).
  4. Tree dump calls Update(0.0f, false) â€” controllers SKIPPED (rest pose,
     oracle.cpp L404-405/L754); the stock printer's Update(0.0f) runs
     controllers (bUpdateControllers defaults true). The helper's printed
     local transforms are REST-POSE, the stock printer's are POST-Update(0).
  5. Output is JSON (stock: text traversal); --dump modes blocks|tree|
     keyframes|skin.
  6. Same stock factory registry (source-built NiMain/NiAnimation/NiParticle
     registrations incl. compat aliases); a rejected load FAILS the same way.

QUALIFICATION CONTROLS (run BEFORE the PE inputs; preregistered expectations):
  QC1 SDK positive: OBJECT.NIF (10.0.1.18, 60 blocks) -> expect exit 0,
      load OK, numBlocks 60, numTopObjects 2.
  QC2 missing-factory negative: SYNTH_UNKNOWN_CLASS.nif (Package B LOCAL_ONLY
      fixture, QzNode in the type table) -> expect exit 1, load FAIL,
      lastErrorMessage contains "QzNode: cannot find create function.".
  QC3 empty scene: SYNTH_EMPTY_SCENE.nif -> expect exit 0, load OK,
      numBlocks 0, numTopObjects 0.
PE expectations: all four selected payloads -> load FAIL (missing NiArk
factory); the observed lastErrorMessage is compared against the
SOURCE_PREDICTED first missing factory (table order) â€” SEPARATE namespaces.

No SDK install, no compiler, no original-tree modification, no binary
patching, no guessed NiArk loaders, no dummy-factory registration.
"""
import ctypes
import hashlib
import json
import os
import subprocess
import sys

RUN_ID = "PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009"
HELPER = (r"D:\gamebyroengine\extracted\gb12_build\bin\gb12_oracle.exe")
HELPER_SHA = "DD7112A41D83557395C5D31F72C89BFEA3D7906AB28EF4DD3C4BD8E398EB046C"
HELPER_SIZE = 594944
HELPER_SRC = (r"D:\gamebyroengine\extracted\gb12_build\oracle\oracle.cpp")
HELPER_SRC_SHA = ("AD1F5DED06FA17AE77D9A5077CE27044"
                  "04451FA0A751FA59F76EF9A24A9E591A")
RUNTIME = r"D:\gamebyroengine\extracted\Gb112_tools_setup"
OUT_ROOT = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
            r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PE_OUT = os.path.join(OUT_ROOT, "02_PE")
RAW = os.path.join(PE_OUT, "raw")
LOCAL_ROOT = (r"D:\Eudoria_Reconstruction\99_Audits"
              r"\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009")
PAYLOAD_DIR = os.path.join(LOCAL_ROOT, "02_PE_payloads")
FIXTURES = os.path.join(LOCAL_ROOT, "01_SDK_fixtures")
SDK_OBJECT = (r"D:\gamebyroengine\extracted\Gb12_Source\Samples\Tutorials"
              r"\Data\Win32\OBJECT.NIF")
TIMEOUT_S = 60

CASES = [
    # (case, kind, input, expected)
    ("QC1_SDK_POSITIVE_OBJECT", "CONTROL", SDK_OBJECT,
     {"exit": 0, "load": "OK", "numBlocks": 60, "numTopObjects": 2}),
    ("QC2_MISSING_FACTORY_QZNODE", "CONTROL",
     os.path.join(FIXTURES, "SYNTH_UNKNOWN_CLASS.nif"),
     {"exit": 1, "load": "FAIL",
      "lastErrorMessage_contains": "QzNode: cannot find create function."}),
    ("QC3_EMPTY_SCENE", "CONTROL",
     os.path.join(FIXTURES, "SYNTH_EMPTY_SCENE.nif"),
     {"exit": 0, "load": "OK", "numBlocks": 0, "numTopObjects": 0}),
    ("PE_218757_HELPER", "PE", os.path.join(PAYLOAD_DIR, "218757.nif"), None),
    ("PE_496633_HELPER", "PE", os.path.join(PAYLOAD_DIR, "496633.nif"), None),
    ("PE_512126_HELPER", "PE", os.path.join(PAYLOAD_DIR, "512126.nif"), None),
    ("PE_423020_HELPER", "PE", os.path.join(PAYLOAD_DIR, "423020.nif"), None),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def run_case(name, kind, path, expected):
    out_path = os.path.join(RAW, name + ".oracle.json")
    err_path = os.path.join(RAW, name + ".oracle.stderr.txt")
    command = [HELPER, path, "--json", out_path]
    env = os.environ.copy()
    env["PATH"] = RUNTIME + ";" + env.get("PATH", "")
    rec = {
        "case": name, "kind": kind, "input": path,
        "input_identity": {"path": path,
                           "size_bytes": os.path.getsize(path)
                           if os.path.exists(path) else None,
                           "sha256": sha256_file(path)
                           if os.path.exists(path) else None},
        "command": command,
        "cwd": PAYLOAD_DIR if kind == "PE" else FIXTURES,
        "child_env_delta": {"PATH": "+" + RUNTIME + ";<inherited PATH>"},
        "child_env_delta_class": "CHILD_PROCESS_PATH_DLL_EXPOSURE "
                                 "(no effect on this exe: no VC71 DLL imports)",
        "timeout_s": TIMEOUT_S,
        "oracle_json_path": out_path, "stderr_path": err_path,
    }
    old_mode = ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
    try:
        with open(err_path, "wb") as ef:
            try:
                proc = subprocess.run(command, cwd=rec["cwd"], env=env,
                                      stdout=ef, stderr=ef,
                                      timeout=TIMEOUT_S,
                                      creationflags=subprocess.CREATE_NO_WINDOW,
                                      check=False)
                # stdout redirected into the --json file by the tool; stderr
                # captured separately is not possible with a single stream â€”
                # reopen: the tool writes usage/errors to stderr. We captured
                # both into ef (stdout was also ef â€” the tool with --json
                # writes the JSON to the file, so stdout gets nothing).
                rec["exit_code"] = proc.returncode
                rec["timeout"] = False
            except subprocess.TimeoutExpired:
                rec["exit_code"] = None
                rec["timeout"] = True
    finally:
        ctypes.windll.kernel32.SetErrorMode(old_mode)
    rec["stderr_text"] = (open(err_path, "rb").read()
                          .decode("cp1252", errors="replace"))
    parsed = None
    if os.path.exists(out_path):
        try:
            with open(out_path, encoding="utf-8", errors="replace") as f:
                parsed = json.load(f)
        except json.JSONDecodeError as ex:
            rec["json_parse_error"] = str(ex)
            with open(out_path, encoding="utf-8", errors="replace") as f:
                parsed = {"raw_text_head": f.read(2000)}
    rec["oracle_json"] = parsed
    if expected:
        ok = True
        detail = {}
        if "exit" in expected:
            detail["exit_match"] = rec.get("exit_code") == expected["exit"]
        if "load" in expected and parsed:
            detail["load_match"] = parsed.get("load") == expected["load"]
        if "numBlocks" in expected and parsed:
            detail["numblocks_match"] = parsed.get("numBlocks") == \
                expected["numBlocks"]
        if "numTopObjects" in expected and parsed:
            detail["numtop_match"] = parsed.get("numTopObjects") == \
                expected["numTopObjects"]
        if "lastErrorMessage_contains" in expected and parsed:
            detail["specific_error_match"] = \
                expected["lastErrorMessage_contains"] in \
                str(parsed.get("lastErrorMessage", ""))
        ok = all(detail.values()) and detail
        rec["control"] = {"expected": expected, "checks": detail,
                          "control_pass": bool(ok)}
    return rec


def main():
    os.makedirs(RAW, exist_ok=True)
    helper_sha = sha256_file(HELPER)
    helper_size = os.path.getsize(HELPER)
    src_sha = sha256_file(HELPER_SRC)
    identity = {
        "helper_identity": {
            "path": HELPER, "size_bytes": helper_size, "sha256": helper_sha,
            "contract_pin_match": (helper_sha == HELPER_SHA
                                   and helper_size == HELPER_SIZE)},
        "helper_source_identity": {
            "path": HELPER_SRC, "sha256": src_sha,
            "reverified_match": src_sha == HELPER_SRC_SHA,
            "lines": sum(1 for _ in open(HELPER_SRC, encoding="latin-1"))},
    }
    if not identity["helper_identity"]["contract_pin_match"]:
        raise SystemExit("E_HELPER_IDENTITY: gb12_oracle.exe != contract pin")
    if not identity["helper_source_identity"]["reverified_match"]:
        raise SystemExit("E_HELPER_SOURCE: oracle.cpp hash changed")

    results = []
    for name, kind, path, expected in CASES:
        rec = run_case(name, kind, path, expected)
        results.append(rec)
    controls_ok = all(r.get("control", {}).get("control_pass")
                      for r in results if r["kind"] == "CONTROL")
    if not controls_ok:
        # contract section 11: a helper that fails its controls is not
        # qualified; PE results are still recorded but flagged.
        print("WARNING: helper qualification controls FAILED; "
              "PE results are flagged UNQUALIFIED_HELPER")
    summary = {
        "run_id": RUN_ID,
        "stage": "S14_optional_native_helper_qualification_and_use",
        "helper": "gb12_oracle.exe (EXISTING custom SDK-source build; NOT "
                  "newly built; NOT the unmodified vendor printer)",
        **identity,
        "why_this_helper": ("the stock printer cannot expose the specific "
                            "failing class (C11 specificity FAIL); this "
                            "helper prints NiStream::GetLastErrorMessage() "
                            "through the SAME stock factory registry (zero "
                            "NiArk loaders, zero dummy factories) â€” "
                            "contract section 11 single-helper rule"),
        "disclosed_behavior_differences_vs_stock_printer": [
            "custom executable built from the possessed GB 1.2.2 source "
            "(EU935_GB12_ORACLE_BUILD_R1); vendor binary untouched",
            "OracleStream NiStream-subclass snapshot hook via the PUBLIC "
            "RegisterPostProcessFunction (zero engine changes; added "
            "observation capability the stock printer lacks)",
            "prints the SPECIFIC NiStream last error (stock printer never "
            "calls GetLastErrorMessage)",
            "tree dump uses Update(0.0f, false): controllers SKIPPED (rest "
            "pose); the stock printer runs controllers (Update(0.0f))",
            "JSON output (stock: text); --dump blocks|tree|keyframes|skin",
            "NO MSVCP71/MSVCR71 imports (child-PATH DLL exposure class kept "
            "for uniformity; no effect on this exe)",
        ],
        "qualification_controls": [r for r in results if r["kind"] == "CONTROL"],
        "controls_all_pass": controls_ok,
        "pe_results": [r for r in results if r["kind"] == "PE"],
        "client_executed": False,
        "no_engine_changes": True,
        "no_dummy_factories": True,
        "no_guessed_niark_loaders": True,
    }
    out = os.path.join(PE_OUT, "NATIVE_HELPER_RESULTS.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps({
        "helper_pin_match": identity["helper_identity"]["contract_pin_match"],
        "controls": [(r["case"], r.get("control", {}).get("control_pass"),
                     r.get("exit_code"),
                     (r.get("oracle_json") or {}).get("lastErrorMessage"))
                    for r in results if r["kind"] == "CONTROL"],
        "controls_all_pass": controls_ok,
        "pe": [(r["case"], r.get("exit_code"),
                (r.get("oracle_json") or {}).get("load"),
                (r.get("oracle_json") or {}).get("lastErrorMessage"))
               for r in results if r["kind"] == "PE"],
    }, indent=2))


if __name__ == "__main__":
    main()
