# extract_expected_pins.py
# RUN: PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
# D2: persist the EXPECTED PIN REGISTRY (the separate expected roster of
# claim IDs, addresses, intended roles and pinned expect_ea/expect_imm/expect_
# bytes specs) extracted from the BASE-pinned c1_pin_ledger.py::PINS Git
# blob (ast literal evaluation - no historical code executed). The registry
# is a CHECKED artifact: gate Q2 (cqc_battery.py) re-derives the roster from
# the same BASE Git blob in-run and requires the on-disk registry to EQUAL
# it (registry tamper = FAIL). PINS is never edited to make a missing or
# relabelled record pass.
# Output: EXPECTED_PIN_REGISTRY.json (--out override).

import argparse
import json
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pin_roster  # noqa: E402

RUN = (r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits"
       r"\PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RUN, "EXPECTED_PIN_REGISTRY.json"))
    args = ap.parse_args()

    roster = pin_roster.expected_from_git()
    ident = pin_roster.roster_identity()
    tally = pin_roster.role_tally()
    ea_required = sum(1 for r in roster.values() if r["role"] == "mem")
    out = {
        "run": "PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005",
        "artifact": "EXPECTED_PIN_REGISTRY",
        "role": ("the separate EXPECTED pin universe for the D2-corrected "
                 "gate Q2: the multiset of claim IDs, their addresses and "
                 "their intended roles; the roster is checked against the "
                 "generated C1 JSON/CSV and against the pinned EXE, and is "
                 "itself re-derived from the BASE Git blob in-run by the "
                 "battery (never trusted from disk)"),
        "source": ident,
        "expected_total": len(roster),
        "expected_role_tally": tally,
        "expected_ea_required_count": ea_required,
        "uniqueness": ("each expected claim occurs EXACTLY ONCE "
                       "(machine-enforced at extraction: duplicate claim_id "
                       "in PINS aborts)"),
        "pins": [
            {"claim_id": r["claim_id"],
             "va": "0x%08X" % r["va"],
             "role": r["role"],
             "expect_bytes": r["expect_bytes"],
             "expect_ea": r["expect_ea"],
             "expect_imm": r["expect_imm"]}
            for r in sorted(roster.values(), key=lambda x: x["claim_id"])
        ],
    }
    with open(args.out, "w", newline="\n", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print("EXPECTED_PIN_REGISTRY written: %d claims, role_tally=%s, ea_required=%d"
          % (len(roster), json.dumps(tally), ea_required))


if __name__ == "__main__":
    main()
