#!/usr/bin/env python3
# gb26 adapter -- SOURCE_DERIVED version-gate ONLY (negative-control adapter).
#
# Source: GB 2.6.0 NiStream.cpp (Gb26_src\NiStream.cpp), SHA256
# 72781EEB0E22D42152E04FADD498EA30292D1807E5C60378F08BFD8563693BA2, L48-52:
#   ms_uiNifMinVersion = GetVersion(10, 1, 0, 114);
#   ms_uiNifMaxVersion = NIF_* (20.6.0.0)
# LoadHeader L395-407: identical integer range test; below min ->
# OLDER_VERSION "NIF version is too old."; above max -> LATER_VERSION
# "Unknown NIF version."
#
# T-corpus files (NIF 10.1.0.0 and 4.1.0.12) are all BELOW the GB 2.6 floor
# -> explicit REJECTED. This adapter implements the gate ONLY; decode beyond
# the gate is NOT_IMPLEMENTED_BEYOND_GATE (scope honesty: no GB 2.6 block
# reimplementation is claimed).

import hashlib
import os

import struct

ADAPTER_ID = "gb26"
ORACLE_MODE = "SOURCE_DERIVED_REIMPLEMENTATION"
ERA_CATEGORY = "GB_2_6"

GB26_MIN = (10, 1, 0, 114)
GB26_MAX = (20, 6, 0, 0)


def _ver_u32(maj, minr, patch, internal):
    return ((maj & 0xFF) << 24) | ((minr & 0xFF) << 16) | \
           ((patch & 0xFF) << 8) | (internal & 0xFF)


V_MIN = _ver_u32(*GB26_MIN)
V_MAX = _ver_u32(*GB26_MAX)


def _u32_to_ver(v):
    return "%d.%d.%d.%d" % ((v >> 24) & 0xFF, (v >> 16) & 0xFF,
                            (v >> 8) & 0xFF, v & 0xFF)


def _common(path):
    with open(path, "rb") as fh:
        data = fh.read()
    out = {
        "schema": "gamebryo_oracle/oracle_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "decode_continued_after_rtti_gate": False,
        "input_identity": {
            "path": os.path.abspath(path),
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest().upper(),
        },
        "oracle": {
            "gamebryo_version": "GB_2_6 (Gamebryo 2.6.0, NIF write version 20.6.0.0)",
            "loader_identity": "NiStream::LoadHeader version gate only (GB 2.6.0 NiStream.cpp L48-52, L395-407)",
            "loader_source_identity": {
                "file": "D:\\gamebyroengine\\extracted\\Gb26_src\\NiStream.cpp",
                "sha256": "72781EEB0E22D42152E04FADD498EA30292D1807E5C60378F08BFD8563693BA2",
            },
            "tool_version": "gamebryo_oracle/1.0.0 gb26 gate adapter",
        },
        "version_gate": {"min": _u32_to_ver(V_MIN), "max": _u32_to_ver(V_MAX)},
        "load_result": {"accepted": False, "partial": False, "error": None,
                        "error_code": None},
        "objects": [],
        "scene_graph": {"roots": [], "edges": []},
        "type_histogram": {},
        "controllers": [],
        "properties": [],
        "textures": [],
        "bounds": [],
        "warnings": [],
        "unknowns": [],
    }
    nl = data.find(b"\x0a")
    if nl == -1 or nl > 128:
        out["load_result"].update(error="NOT_NIF_FILE",
                                   error_code="NOT_NIF_FILE")
        return out, data
    line = data[:nl].decode("latin-1")
    out["input_identity"]["header"] = line
    if "File Format" not in line:
        out["load_result"].update(error="NOT_NIF_FILE: 'File Format' absent",
                                  error_code="NOT_NIF_FILE")
        return out, data
    if len(data) < nl + 5:
        out["load_result"].update(error="NOT_NIF_FILE: truncated header",
                                  error_code="NOT_NIF_FILE")
        return out, data
    (ver,) = struct.unpack("<I", data[nl + 1:nl + 5])
    out["input_identity"]["nif_version"] = _u32_to_ver(ver)
    out["input_identity"]["nif_version_u32"] = ver
    if ver < V_MIN:
        out["load_result"].update(
            accepted=False,
            error="OLDER_VERSION: NIF version is too old.",
            error_code="OLDER_VERSION")
        out["version_gate"]["verdict"] = "REJECTED"
    elif ver > V_MAX:
        out["load_result"].update(
            accepted=False,
            error="LATER_VERSION: Unknown NIF version.",
            error_code="LATER_VERSION")
        out["version_gate"]["verdict"] = "REJECTED"
    else:
        out["load_result"].update(
            accepted=False, partial=False,
            error="NOT_IMPLEMENTED_BEYOND_GATE: gb26 adapter implements the "
                  "source-derived version gate only; no GB 2.6 block decode "
                  "is claimed (scope honesty)",
            error_code="NOT_IMPLEMENTED")
        out["version_gate"]["verdict"] = "ACCEPTED"
    return out, data


def inspect(path, full_decode=False):
    out, _data = _common(path)
    if full_decode:
        out["warnings"].append("--full-decode has no effect on the gb26 "
                               "gate-only adapter (NOT_IMPLEMENTED_BEYOND_GATE)")
    return out


def probe_version(path):
    out, _ = _common(path)
    probe = {
        "schema": "gamebryo_oracle/probe_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "oracle": out["oracle"],
        "input_identity": out["input_identity"],
        "version_gate": out["version_gate"],
        "probe": {"verdict": "REJECTED" if out["load_result"]["error_code"] ==
                   "OLDER_VERSION" else
                   (out["load_result"]["error_code"] or "ACCEPTED"),
                  "reason": out["load_result"]["error"]},
    }
    return probe


def capabilities():
    return {
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "version_gate": "10.1.0.114 .. 20.6.0.0 (source: NiStream.cpp L48-52)",
        "rtti_behavior": "NOT_IMPLEMENTED_BEYOND_GATE",
        "supports_full_decode": False,
        "note": "wrong-version negative-control adapter; T-corpus files "
                "(10.1.0.0 / 4.1.0.12) are below the floor -> REJECTED",
    }
