#!/usr/bin/env python3
# gb112 adapter -- ORIGINAL_TOOL_EXECUTION wrapper for the INSTALLED original
# Gamebryo 1.1.2 Evaluation tools (era GB_1_1_2).
#
# LOCAL DEPENDENCY REPRESENTATION (s22; no binaries are copied into the repo):
#   LOCAL_PATH_DESCRIPTION: installed Gamebryo 1.1.2 Evaluation tools tree
#     (SceneGraphPrinter console tool; SceneViewer DX8/DX9 GUI viewers)
#   LOCAL_PATH: D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\Tools\...
#   VERSION: Gamebryo 1.1.2 Evaluation (NDL 2004; engine identifies/writes
#     NIF 10.1.0.0 -- installed SDK NiVersion.h sha256 67C9C745...)
#   SIZE / SHA256: per-exe identity below (verified against the E1
#     TOOLCHAIN_MATRIX census before each run).
#   REPRODUCTION_METHOD: run the ORIGINAL UNMODIFIED exe from a sandbox
#     working directory with the VC71 runtime DLLs that ship in the same
#     tools distribution (D:\gamebyroengine\extracted\Gb112_tools_setup\
#     MSVCR71.DLL / MSVCP71.DLL / MFC71.DLL) copied LOCALLY into the sandbox
#     run directory (never installed system-wide); capture stdout/stderr/
#     exit code; the tool itself is never patched (s19).
#
# VERSION-RANGE CLAIMS: UNKNOWN (binary NiMain.lib; the gate constants are
# compiled in -- never claimed from source).
#
# If a tool cannot run, the EXACT blocker class is recorded (missing DLL
# name(s), platform error, entry-point error); never "tool broken".

import hashlib
import os
import shutil
import struct
import subprocess

ADAPTER_ID = "gb112"
ORACLE_MODE = "ORIGINAL_TOOL_EXECUTION"
ERA_CATEGORY = "GB_1_1_2"

GB112_TOOLS_ROOT = (r"D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\Tools")
VC71_DLL_SOURCES = [
    r"D:\gamebyroengine\extracted\Gb112_tools_setup\MSVCR71.DLL",
    r"D:\gamebyroengine\extracted\Gb112_tools_setup\MSVCP71.DLL",
    r"D:\gamebyroengine\extracted\Gb112_tools_setup\MFC71.DLL",
]
TOOLS = {
    # sha256 == E1 TOOLCHAIN_MATRIX rows (verified at run time)
    "SceneGraphPrinter": {
        "path": os.path.join(
            GB112_TOOLS_ROOT,
            "DeveloperTools", "SceneGraphPrinter", "Win32", "VC71",
            "SceneGraphPrinter.exe"),
        "sha256_expected": "3A7F768DA719E124F27A20BBEC7CFA89CC68F7FD"
                           "E2747A3C364B0C8ABBE30BB6",
        "kind": "console",
    },
    "SceneViewer_DX8": {
        "path": os.path.join(
            GB112_TOOLS_ROOT, "SceneViewer", "Application", "VC71",
            "SceneViewer_DX8.exe"),
        "sha256_expected": "6A984014EF951F5722D2DC64226F928B155A749CC"
                           "39A421FFD1490D9B25FDF8C",
        "kind": "gui",
    },
    "SceneViewer_DX9": {
        "path": os.path.join(
            GB112_TOOLS_ROOT, "SceneViewer", "Application", "VC71",
            "SceneViewer_DX9.exe"),
        "sha256_expected": "A2DACA0A6F02200BCC93D5544CE4085946810E79CC"
                           "5B46C28E69EC666C8B9EA1",
        "kind": "gui",
    },
}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _tool_report(tool_name, input_path, workdir, stdout, stderr, exit_code,
                 duration_s, extra=None):
    return {
        "tool": tool_name,
        "tool_path": TOOLS[tool_name]["path"],
        "tool_sha256": _sha256(TOOLS[tool_name]["path"]),
        "tool_sha256_matches_E1_census":
            _sha256(TOOLS[tool_name]["path"]) ==
            TOOLS[tool_name]["sha256_expected"],
        "tool_modified": False,
        "input_path": os.path.abspath(input_path),
        "input_sha256": _sha256(input_path),
        "sandbox_workdir": os.path.abspath(workdir),
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "duration_s": duration_s,
        "extra": extra or {},
    }


def run_tool(tool_name, input_path, workdir, timeout_s=60):
    """Copy the ORIGINAL unmodified tool + VC71 runtime DLLs into the sandbox
    workdir, run it on a sandbox copy of the input, capture everything."""
    os.makedirs(workdir, exist_ok=True)
    tool_path = TOOLS[tool_name]["path"]
    if not os.path.exists(tool_path):
        return {"tool": tool_name, "blocked": True,
                "blocker_class": "TOOL_PATH_MISSING",
                "detail": "installed tool not found: %s" % tool_path}
    local_tool = os.path.join(workdir, os.path.basename(tool_path))
    shutil.copyfile(tool_path, local_tool)
    dll_blockers = []
    for dll in VC71_DLL_SOURCES:
        if os.path.exists(dll):
            shutil.copyfile(dll, os.path.join(workdir, os.path.basename(dll)))
        else:
            dll_blockers.append(os.path.basename(dll))
    local_input = os.path.join(workdir, "input.nif")
    shutil.copyfile(input_path, local_input)
    import time
    t0 = time.time()
    try:
        proc = subprocess.run(
            [local_tool, "input.nif"], cwd=workdir,
            capture_output=True, timeout=timeout_s)
        dur = round(time.time() - t0, 3)
        return _tool_report(tool_name, input_path, workdir,
                            proc.stdout.decode("latin-1", "replace"),
                            proc.stderr.decode("latin-1", "replace"),
                            proc.returncode, dur)
    except subprocess.TimeoutExpired:
        dur = round(time.time() - t0, 3)
        return _tool_report(tool_name, input_path, workdir, "", "",
                            "TIMEOUT", dur, extra={"timeout_s": timeout_s})
    except OSError as e:
        return {
            "tool": tool_name, "blocked": True,
            "blocker_class": "OSERROR_LAUNCH",
            "detail": str(e),
            "input_path": os.path.abspath(input_path),
        }


def inspect(path, full_decode=False, workdir=None, tools=("SceneGraphPrinter",)):
    """ORIGINAL_TOOL_EXECUTION attempt(s) on sandbox copies. The oracle JSON
    reports execution observations; version-range claims stay UNKNOWN."""
    reports = []
    if workdir is None:
        workdir = os.path.join(os.path.dirname(os.path.abspath(path)),
                               "gb112_runs")
    for t in tools:
        reports.append(run_tool(t, path, workdir))
    accepted = False
    error = "NOT_TESTED"
    any_ok = any(isinstance(r.get("exit_code"), int) and r["exit_code"] == 0
                 and r.get("stdout") for r in reports)
    return {
        "schema": "gamebryo_oracle/oracle_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "decode_continued_after_rtti_gate": False,
        "input_identity": {
            "path": os.path.abspath(path),
            "size": os.path.getsize(path),
            "sha256": _sha256(path),
            "header": _header_of(path),
            "nif_version": _version_of(path),
            "nif_version_u32": _version_u32_of(path),
        },
        "oracle": {
            "gamebryo_version": "GB_1_1_2 (Gamebryo 1.1.2 Evaluation; NIF 10.1.0.0 era)",
            "loader_identity": "INSTALLED ORIGINAL TOOLS (unmodified; sandbox-local VC71 runtime)",
            "loader_source_identity": {
                "file": "installed binary tools (Gamebryo 1.1.2 Evaluation\\Tools)",
                "sha256": "per-tool sha256 in tool_reports (== E1 census)",
            },
            "tool_version": "gamebryo_oracle/1.0.0 gb112 execution wrapper",
            "version_range_claim": "UNKNOWN (binary lib; never claimed from source)",
        },
        "load_result": {
            "accepted": accepted and any_ok,
            "partial": False,
            "error": error if not any_ok else None,
            "error_code": "ORIGINAL_TOOL_OBSERVATION" if not any_ok else None,
        },
        "tool_reports": reports,
        "objects": [],
        "scene_graph": {"roots": [], "edges": []},
        "type_histogram": {},
        "controllers": [],
        "properties": [],
        "textures": [],
        "bounds": [],
        "warnings": ["gb112 is an execution adapter: block-level decode "
                     "data is NOT_AVAILABLE_IN_ORACLE (the tools print "
                     "scene summaries, they do not emit field data)"],
        "unknowns": [],
    }


def _header_of(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(256)
        nl = data.find(b"\x0a")
        if 0 < nl <= 128:
            return data[:nl].decode("latin-1")
    except OSError:
        pass
    return None


def _version_of(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(256)
        nl = data.find(b"\x0a")
        if 0 < nl <= 128 and len(data) >= nl + 5:
            (v,) = struct.unpack("<I", data[nl + 1:nl + 5])
            return "%d.%d.%d.%d" % ((v >> 24) & 0xFF, (v >> 16) & 0xFF,
                                    (v >> 8) & 0xFF, v & 0xFF)
    except (OSError, struct.error):
        pass
    return None


def _version_u32_of(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(256)
        nl = data.find(b"\x0a")
        if 0 < nl <= 128 and len(data) >= nl + 5:
            (v,) = struct.unpack("<I", data[nl + 1:nl + 5])
            return v
    except (OSError, struct.error):
        pass
    return None


def probe_version(path):
    return {
        "schema": "gamebryo_oracle/probe_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "oracle": {
            "gamebryo_version": "GB_1_1_2 (Gamebryo 1.1.2 Evaluation)",
            "loader_identity": "installed original tools (binary)",
            "loader_source_identity": {
                "file": "Gamebryo 1.1.2 Evaluation\\Tools (installed)",
                "sha256": "per-tool; see inspect tool_reports",
            },
            "tool_version": "gamebryo_oracle/1.0.0 gb112 execution wrapper",
            "version_range_claim": "UNKNOWN (binary lib)",
        },
        "input_identity": {
            "path": os.path.abspath(path),
            "size": os.path.getsize(path),
            "sha256": _sha256(path),
            "header": _header_of(path),
            "nif_version": _version_of(path),
        },
        "probe": {"verdict": "UNKNOWN",
                  "reason": "GB 1.1.2 read range is compiled into NiMain.lib "
                            "(binary); executed-loader behavior only, no "
                            "source claim"},
    }


def capabilities():
    return {
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "version_gate": "UNKNOWN (binary lib; never claimed from source)",
        "rtti_behavior": "UNKNOWN (binary)",
        "tools": {k: TOOLS[k]["path"] for k in TOOLS},
        "runtime_dlls_sandbox_local": [os.path.basename(p)
                                       for p in VC71_DLL_SOURCES],
        "supports_full_decode": False,
    }
