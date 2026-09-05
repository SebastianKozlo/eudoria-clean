#!/usr/bin/env python3
"""validate_cw_capture.py — the FAIL-CLOSED JSONL validator for the KROK B ingest
of PE_M1_X87CW_EXECUTION_R1_20260905_125139 (the x87 CW capture).
Per design W3.4.13 (the line schema), W3.4.12 (the N-hit policy), W3.4.14 (the
cross-site agreement), W4.5 (the ambiguity classes), W5 (the decode + the verdict
strings). Every line must independently parse (profile §14 rule 6).
Usage: python validate_cw_capture.py [path-to-cw_capture.jsonl]
Exit 0 = PASS (the measurement verdict printed); non-zero = the failure list.
"""
import json
import sys
from datetime import datetime, timezone

DEFAULT = r"D:\Eudoria_Reconstruction\99_Audits\PE_M1_X87CW_EXECUTION_R1_20260905_125139\04_RUNTIME\cw_capture.jsonl"

REQUIRED_FIELDS = ["hit_index", "attempt", "site", "bp_va", "eip", "pid",
                   "cw_hex", "pc_bits", "pc_decoded", "rc_bits", "rc_decoded",
                   "exception_masks_bits", "cw_full_binary", "capture_method",
                   "screenshot", "timestamp"]
SITES = {"FDIV_0x0098CE5A": "0x0098CE5A", "FLD_0x0095B2BC": "0x0095B2BC",
         "SPAWN_ENTRY_0x0095B180": "0x0095B180", "GRID_ENTRY_0x0098FE00": "0x0098FE00",
         "PROCESS_ENTRY": "aux"}
PC_DECODE = {"00": "24-bit single", "01": "reserved", "10": "53-bit double", "11": "64-bit extended"}
RC_DECODE = {"00": "nearest-even", "01": "down", "10": "up", "11": "truncate"}
N_REQUIRED = 10


def decode_cw(cw):
    """cw = int; returns (pc_bits, rc_bits, masks_bits, full_binary)."""
    full = format(cw, "016b")
    return full[6:8], full[4:6], full[10:16], full


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    problems, lines = [], []
    try:
        raw = open(path, "r", encoding="utf-8").read().splitlines()
    except OSError as e:
        print(json.dumps({"verdict": "OPEN-INGEST_FAILURE", "problems": [str(e)]}))
        sys.exit(3)

    for i, ln in enumerate(raw, 1):
        if not ln.strip():
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError as e:
            problems.append(f"L{i}: JSON parse failure: {e}")
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in obj or obj[f] in (None, "")]
        if missing:
            problems.append(f"L{i}: missing/vacuous fields: {missing}")
            continue
        # EIP must equal the bp VA for site breakpoints (the W3.4.11 self-check)
        if obj["site"] in SITES and SITES[obj["site"]] not in ("aux",) \
                and obj["eip"].lower() != SITES[obj["site"]].lower():
            problems.append(f"L{i}: eip {obj['eip']} != bp_va {SITES[obj['site']]}")
        # The mechanical decode check (the JSONL records raw + decoded; the
        # validator re-derives and requires agreement — no trust, recompute)
        try:
            cw = int(obj["cw_hex"], 16)
            pc_bits, rc_bits, masks, full = decode_cw(cw)
            if obj["pc_bits"] != pc_bits:
                problems.append(f"L{i}: pc_bits {obj['pc_bits']} != recomputed {pc_bits}")
            if obj["rc_bits"] != rc_bits:
                problems.append(f"L{i}: rc_bits {obj['rc_bits']} != recomputed {rc_bits}")
            if obj["exception_masks_bits"] != masks:
                problems.append(f"L{i}: masks {obj['exception_masks_bits']} != recomputed {masks}")
            if obj["cw_full_binary"] != full:
                problems.append(f"L{i}: cw_full_binary != recomputed {full}")
            if obj["pc_decoded"] != PC_DECODE.get(pc_bits, "reserved"):
                problems.append(f"L{i}: pc_decoded '{obj['pc_decoded']}' != table '{PC_DECODE.get(pc_bits)}'")
            if obj["rc_decoded"] != RC_DECODE.get(rc_bits, "?"):
                problems.append(f"L{i}: rc_decoded '{obj['rc_decoded']}' != table '{RC_DECODE.get(rc_bits)}'")
        except (ValueError, KeyError) as e:
            problems.append(f"L{i}: cw decode failure: {e}")
        lines.append(obj)

    # The N-hit completeness per site (the primary sites only; the fallback sites
    # also require N when the fallback ladder was used)
    by_site = {}
    for o in lines:
        by_site.setdefault(o["site"], []).append(o)
    n_problems = [f"site {s}: {len(v)} hits < N={N_REQUIRED}" for s, v in by_site.items()
                  if len(v) < N_REQUIRED and s != "PROCESS_ENTRY"]

    # The cross-site agreement (the primary pair, if both captured)
    prim = [s for s in ("FDIV_0x0098CE5A", "FLD_0x0095B2BC") if s in by_site]
    series_problems = []
    verdict_series = {}
    for s, v in by_site.items():
        if s == "PROCESS_ENTRY":
            continue
        pcs = sorted({o["pc_bits"] for o in v})
        rcs = sorted({o["rc_bits"] for o in v})
        verdict_series[s] = {"pc_values": pcs, "rc_values": rcs,
                             "stable": len(pcs) == 1 and len(rcs) == 1,
                             "transition_observed": len(pcs) > 1 or len(rcs) > 1}
        if len(pcs) > 1:
            series_problems.append(f"site {s}: PC series UNSTABLE across hits: {pcs} -> CW_READ_AMBIGUITY (W4.5a)")
    if len(prim) == 2:
        pc1 = {o["pc_bits"] for o in by_site[prim[0]]}
        pc2 = {o["pc_bits"] for o in by_site[prim[1]]}
        if pc1 != pc2:
            series_problems.append(f"cross-site PC disagreement {prim[0]}={pc1} vs {prim[1]}={pc2} -> CW_READ_AMBIGUITY (W4.5d)")

    all_problems = problems + n_problems + series_problems
    # The verdict determination (W5): only from STABLE, COMPLETE primary series
    verdict = None
    if not all_problems and prim:
        pc = by_site[prim[0]][0]["pc_bits"]
        rc = by_site[prim[0]][0]["rc_bits"]
        if pc == "10":
            verdict = "MEASURED-PC53"
        elif pc == "11":
            verdict = "MEASURED-PC64"
        elif pc == "00":
            verdict = "MEASURED-PC24-DEFECT"
        elif pc == "01":
            verdict = "OPEN-CW_RESERVED_FIELD"
        if verdict in ("MEASURED-PC53", "MEASURED-PC64") and rc != "00":
            verdict += "+RC_NOT_NEAREST_EVEN (the RC sub-item stays OPEN per W5.1 - NO silent pass)"
    elif problems or series_problems:
        verdict = "OPEN-CW_READ_AMBIGUITY"
    elif n_problems:
        verdict = "OPEN-INCOMPLETE_SERIES"
    elif not prim:
        verdict = "OPEN-NO_PRIMARY_CAPTURE"

    out = {
        "run_id": "PE_M1_X87CW_EXECUTION_R1_20260905_125139",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "lines_read": len(lines),
        "verdict": verdict,
        "problems": all_problems,
        "series": verdict_series,
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if verdict and verdict.startswith("MEASURED") and not all_problems else 1)


if __name__ == "__main__":
    main()
