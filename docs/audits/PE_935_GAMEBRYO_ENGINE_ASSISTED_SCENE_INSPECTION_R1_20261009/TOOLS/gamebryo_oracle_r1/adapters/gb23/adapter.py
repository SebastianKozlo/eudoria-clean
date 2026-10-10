#!/usr/bin/env python3
# gb23 adapter -- HEADER-ONLY metadata adapter (era GB_2_3).
#
# The GB 2.3 Evaluation SDK is a BINARY SDK (Wise installer; 0 NI*.cpp core
# entries in its 4,642-entry file table -- E1 VERSION_SUPPORT.md section 4).
# Recovered NiVersion.h (sha256 DFCCD6ECA8D48B984B1931D0A983E758A37167CC
# CBCF742143B6555CBFB81D39, recovered from the SDK setup in E1) proves
# GAMEBRYO 2.3.0.0, build 24-04-2007, NIF write version 20.3.0.9.
# The NIF READ range is compiled into NIMAIN23VC71R.lib -> UNKNOWN.
#
# EXECUTION: NOT_TESTED, reason: its installer (GbEvaluationToolsSetup.exe
# inside GB_2.3.iso) was never installed and NOTHING is installed in this
# run. No GB 2.3 tool execution claim is made.

import hashlib
import os
import struct

ADAPTER_ID = "gb23"
ORACLE_MODE = "SOURCE_DERIVED_REIMPLEMENTATION"  # header-level metadata only
ERA_CATEGORY = "GB_2_3"

NOT_TESTED_REASON = ("GB 2.3 Evaluation tools were never installed; no "
                     "installation is performed in this run (execution "
                     "NOT_TESTED by design)")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _header_probe(path):
    with open(path, "rb") as fh:
        data = fh.read(256)
    out = {"path": os.path.abspath(path), "size": os.path.getsize(path),
           "sha256": _sha256(path)}
    nl = data.find(b"\x0a")
    if 0 < nl <= 128:
        out["header"] = data[:nl].decode("latin-1")
        if len(data) >= nl + 5:
            (v,) = struct.unpack("<I", data[nl + 1:nl + 5])
            out["nif_version"] = "%d.%d.%d.%d" % ((v >> 24) & 0xFF,
                                                  (v >> 16) & 0xFF,
                                                  (v >> 8) & 0xFF, v & 0xFF)
            out["nif_version_u32"] = v
    return out


def inspect(path, full_decode=False):
    ident = _header_probe(path)
    return {
        "schema": "gamebryo_oracle/oracle_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "decode_continued_after_rtti_gate": False,
        "input_identity": ident,
        "oracle": {
            "gamebryo_version": "GB_2_3 (Gamebryo 2.3.0 Evaluation; NIF write version 20.3.0.9)",
            "loader_identity": "header-only metadata adapter (binary SDK; no loader semantics claimed)",
            "loader_source_identity": {
                "file": "recovered GB 2.3 NiVersion.h (E1 extraction from "
                        "GbEvaluationSDKSetup.exe Wise table)",
                "sha256": "DFCCD6ECA8D48B984B1931D0A983E758A37167CCCBCF742"
                          "143B6555CBFB81D39",
            },
            "tool_version": "gamebryo_oracle/1.0.0 gb23 header-only adapter",
            "version_range_claim": "UNKNOWN (binary NIMAIN23VC71R.lib)",
        },
        "load_result": {
            "accepted": False,
            "partial": False,
            "error": "NOT_TESTED: " + NOT_TESTED_REASON,
            "error_code": "NOT_TESTED",
        },
        "version_gate": {"min": "UNKNOWN", "max": "UNKNOWN",
                         "verdict": "UNKNOWN"},
        "objects": [],
        "scene_graph": {"roots": [], "edges": []},
        "type_histogram": {},
        "controllers": [],
        "properties": [],
        "textures": [],
        "bounds": [],
        "warnings": ["execution NOT_TESTED: " + NOT_TESTED_REASON],
        "unknowns": [],
    }


def probe_version(path):
    ident = _header_probe(path)
    return {
        "schema": "gamebryo_oracle/probe_result@1.0",
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "oracle": {
            "gamebryo_version": "GB_2_3 (Gamebryo 2.3.0 Evaluation)",
            "loader_identity": "header-only metadata adapter",
            "loader_source_identity": {
                "file": "recovered GB 2.3 NiVersion.h",
                "sha256": "DFCCD6ECA8D48B984B1931D0A983E758A37167CCCBCF742"
                          "143B6555CBFB81D39",
            },
            "tool_version": "gamebryo_oracle/1.0.0 gb23 header-only adapter",
            "version_range_claim": "UNKNOWN (binary SDK)",
        },
        "input_identity": ident,
        "probe": {"verdict": "UNKNOWN",
                  "reason": "read range compiled into NIMAIN23VC71R.lib "
                            "(binary); execution NOT_TESTED: " +
                            NOT_TESTED_REASON},
    }


def capabilities():
    return {
        "adapter": ADAPTER_ID,
        "ORACLE_MODE": ORACLE_MODE,
        "era_category": ERA_CATEGORY,
        "version_gate": "UNKNOWN (binary SDK)",
        "rtti_behavior": "UNKNOWN (binary SDK)",
        "execution": "NOT_TESTED: " + NOT_TESTED_REASON,
        "supports_full_decode": False,
    }
