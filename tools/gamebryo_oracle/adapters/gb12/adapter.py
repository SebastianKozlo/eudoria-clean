#!/usr/bin/env python3
# gb12 adapter -- SOURCE_DERIVED_REIMPLEMENTATION of Gamebryo 1.2.2 loader
# semantics (see ../../gb12core.py header for the full source canon).
#
# The original GB 1.2 semantics are: LoadHeader "File Format" test; packed-u32
# version gate 3.3.0.11..10.2.0.0 (OLDER_VERSION "NIF version is too old." /
# LATER_VERSION "Unknown NIF version."); user-defined version iff file version
# >= 10.0.1.8; RTTI string table + factory lookup with the ORIGINAL
# fail-closed behavior (unregistered class -> RTTIError -> Load() false);
# per-block GroupID u32 iff 5.0.0.6 <= v < 10.1.0.114 (P2).
#
# --full-decode is OUR extension (continues past the RTTI gate, recording the
# offending classes as unknowns): in that mode the JSON carries
# load_result.accepted=false + error=RTTIError(<class>) + partial=true +
# unknowns=[...] + decode_continued_after_rtti_gate=true. The ORIGINAL verdict
# is always reported; SOURCE_DERIVED output is never phrased as original
# execution.

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import gb12core  # noqa: E402

ADAPTER_ID = "gb12"
ORACLE_MODE = "SOURCE_DERIVED_REIMPLEMENTATION"
ERA_CATEGORY = "GB_1_2"


def inspect(path, full_decode=False):
    """Full GB 1.2 oracle inspect of a NIF file (original verdict + optional
    OUR full-decode extension past the RTTI gate)."""
    with open(path, "rb") as fh:
        data = fh.read()
    res = gb12core.decode(data, path=os.path.abspath(path),
                          full_decode=full_decode)
    return res


def probe_version(path):
    """Header + version-gate probe only (no block decode)."""
    with open(path, "rb") as fh:
        data = fh.read()
    r = gb12core.Reader(data)
    out = {
        "schema": "gamebryo_oracle/probe_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "oracle": {
            "gamebryo_version": "GB_1_2 (Gamebryo 1.2.2)",
            "loader_identity": "NiStream::LoadHeader (GB 1.2.2 CoreLibs NiMain)",
            "loader_source_identity": {
                "file": "D:\\gamebyroengine\\extracted\\Gb12_Source\\"
                        "CoreLibs\\NiMain\\NiStream.cpp",
                "sha256": "E955C36EBBB442029E00BE8A154726741B8454A6"
                          "07F2DC043F1FD542B009DC25",
            },
            "tool_version": "%s/%s" % (gb12core.TOOL_NAME,
                                       gb12core.TOOL_VERSION),
        },
        "input_identity": {
            "path": os.path.abspath(path),
            "size": len(data),
            "sha256": gb12core.sha256_file(path),
        },
        "version_gate": {"min": "3.3.0.11", "max": "10.2.0.0"},
    }
    try:
        line = r.line()
    except gb12core.DecodeError:
        out["probe"] = {"verdict": "NOT_NIF_FILE",
                        "reason": "header line unreadable"}
        return out
    out["input_identity"]["header"] = line
    if "File Format" not in line:
        out["probe"] = {"verdict": "NOT_NIF_FILE",
                        "reason": "Not a NIF file"}
        return out
    ver = r.u32()
    out["input_identity"]["nif_version"] = gb12core.u32_to_ver(ver)
    out["input_identity"]["nif_version_u32"] = ver
    if ver < gb12core.V_MIN:
        out["probe"] = {"verdict": "REJECTED",
                        "reason": "OLDER_VERSION: NIF version is too old."}
    elif ver > gb12core.V_MAX:
        out["probe"] = {"verdict": "REJECTED",
                        "reason": "LATER_VERSION: Unknown NIF version."}
    else:
        out["probe"] = {"verdict": "ACCEPTED",
                        "reason": "version within [3.3.0.11, 10.2.0.0]"}
    return out


def capabilities():
    return {
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "version_gate": "3.3.0.11 .. 10.2.0.0 (source: NiStream.cpp L42-46)",
        "rtti_behavior": "fail-closed RTTIError on unregistered class "
                         "(NiStream.cpp L427-433)",
        "full_decode_extension": "continue past the RTTI gate, closure-search "
                                 "boundaries for unknown blocks (OUR "
                                 "extension, never original behavior)",
        "decoded_classes": sorted(gb12core.LOADERS.keys()),
        "registered_classes_count": 198,
        "registered_registry": "adapters/gb12/registry.py "
                               "(SDM census; NiArk* absent)",
        "supports_full_decode": True,
    }
