#!/usr/bin/env python3
# oracle.py -- GAMEBRYO_ORACLE_TOOL single entrypoint CLI.
#
# Usage:
#   python oracle.py inspect <nif> [--adapter gb12|gb26|gb112|gb23]
#        [--full-decode] [--out <file>]
#   python oracle.py probe-version <nif> [--adapter ...]
#   python oracle.py compare <nif> --our-parser <our_result.json>
#        [--oracle-result <oracle_result.json>] [--out <file>]
#   python oracle.py capabilities [--adapter ...]
#
# Exit codes: 0 = success; 2 = rejected/failed (JSON still emitted);
# 3 = usage/IO error. Output is deterministic (no wall-clock data).
#
# F2 CLI_SUCCESS_SEMANTICS (2026-10-03, applies to `inspect` ONLY): for
# adapters that report the F2 axis TOOL_VERDICT (gb12), inspect exits 0 ONLY
# on TOOL_VERDICT=PASS (ADAPTER_DECODE_COVERAGE=COMPLETE AND
# ADAPTER_INTEGRITY=PASS AND no source-predicted REJECTED); any
# REGISTERED_BUT_NOT_DECODED_BY_ADAPTER boundary-only block or
# LINK_FAILURE/out-of-range link => exit != 0. Adapters without the F2 axes
# keep their pre-F2 accepted-based exit semantics (unchanged).
# probe-version / compare / capabilities exit semantics are UNCHANGED.

import argparse
import importlib.util
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

ADAPTERS = ("gb12", "gb26", "gb112", "gb23")


def _get_adapter(name):
    mod_path = os.path.join(_HERE, "adapters", name, "adapter.py")
    spec = importlib.util.spec_from_file_location(
        "gb_oracle_adapter_" + name, mod_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _emit(obj, out_path):
    text = json.dumps(obj, indent=1, sort_keys=False, ensure_ascii=True)
    if out_path:
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text + "\n")
    else:
        sys.stdout.write(text + "\n")
    return text


def cmd_inspect(args):
    ad = _get_adapter(args.adapter)
    res = ad.inspect(args.nif, full_decode=args.full_decode)
    _emit(res, args.out)
    verdict = res.get("TOOL_VERDICT")
    if verdict is not None:
        # F2 (2026-10-03, inspect ONLY): exit 0 ONLY on TOOL_VERDICT=PASS
        # (coverage COMPLETE + integrity PASS + no source-predicted
        # REJECTED). A boundary-only REGISTERED_BUT_NOT_DECODED_BY_ADAPTER
        # block or a LINK_FAILURE/out-of-range link => exit 2. No
        # default-success fallback: an adapter that reports the F2 axes is
        # gated by TOOL_VERDICT alone.
        return 0 if verdict == "PASS" else 2
    lr = res.get("load_result", {})
    return 0 if lr.get("accepted") else 2


def cmd_probe(args):
    ad = _get_adapter(args.adapter)
    res = ad.probe_version(args.nif)
    _emit(res, args.out)
    probe = res.get("probe", {})
    return 0 if probe.get("verdict") == "ACCEPTED" else 2


def cmd_compare(args):
    cmp_mod = _get_adapter("compare")
    oracle_json = None
    if args.oracle_result:
        oracle_json = cmp_mod.load(args.oracle_result)
    else:
        oad = _get_adapter("gb12")
        oracle_json = oad.inspect(args.nif, full_decode=True)
    our_json = cmp_mod.load(args.our_parser)
    res = cmp_mod.compare(oracle_json, our_json)
    _emit(res, args.out)
    bad = res.get("summary", {}).get("counts", {}).get("MISMATCH", 0)
    return 0 if bad == 0 else 2


def cmd_capabilities(args):
    if args.adapter:
        ad = _get_adapter(args.adapter)
        res = ad.capabilities()
        _emit(res, args.out)
        return 0
    out = {"tool": "gamebryo_oracle", "version": "1.0.0",
           "adapters": {}}
    for name in ADAPTERS:
        ad = _get_adapter(name)
        out["adapters"][name] = ad.capabilities()
    _emit(out, args.out)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="oracle.py", description="GAMEBRYO_ORACLE_TOOL entrypoint")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("inspect", help="full oracle inspect of a NIF")
    sp.add_argument("nif")
    sp.add_argument("--adapter", default="gb12", choices=ADAPTERS)
    sp.add_argument("--full-decode", action="store_true")
    sp.add_argument("--out", default=None)
    sp.set_defaults(func=cmd_inspect)

    sp = sub.add_parser("probe-version", help="header + version gate probe")
    sp.add_argument("nif")
    sp.add_argument("--adapter", default="gb12", choices=ADAPTERS)
    sp.add_argument("--out", default=None)
    sp.set_defaults(func=cmd_probe)

    sp = sub.add_parser("compare", help="compare oracle vs our decoder output")
    sp.add_argument("nif")
    sp.add_argument("--our-parser", required=True,
                    help="our decoder result JSON")
    sp.add_argument("--oracle-result", default=None,
                    help="oracle result JSON (default: run gb12 full-decode)")
    sp.add_argument("--out", default=None)
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("capabilities", help="adapter capability report")
    sp.add_argument("--adapter", default=None, choices=ADAPTERS)
    sp.add_argument("--out", default=None)
    sp.set_defaults(func=cmd_capabilities)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as e:
        sys.stderr.write("IOERROR: %s\n" % e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
