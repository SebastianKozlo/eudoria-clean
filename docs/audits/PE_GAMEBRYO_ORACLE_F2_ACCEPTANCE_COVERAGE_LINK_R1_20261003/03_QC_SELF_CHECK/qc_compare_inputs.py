#!/usr/bin/env python3
# qc_compare_inputs.py -- OUR OWN synthetic our-parser JSON for the F2 QC
# compare-command semantics preservation check (pre/post fix, both sides
# pinned). Derived by hand from the pinned fx_VALID_positive.nif layout
# (one NiNode "root", identity local transform, no children/effects, 1
# root). OUR data; zero proprietary content.

import hashlib
import json
import os
import sys

SB = (r"C:\Users\User\AppData\Local\Temp\opencode"
      r"\PE_GAMEBRYO_ORACLE_F2_20261003\sandbox\01_FIXTURES")
NIF = os.path.join(SB, "fx_VALID_positive.nif")


def main():
    with open(NIF, "rb") as fh:
        data = fh.read()
    our = {
        "decoder_identity": {
            "decoder": "F2_QC_SYNTHETIC_OUR_PARSER",
            "note": "hand-built minimal our-parser record for the F2 QC "
                    "compare-semantics preservation check; OUR data",
        },
        "input_identity": {"sha256": hashlib.sha256(data).hexdigest().upper()},
        "num_blocks": 1,
        "parse": {"accepted": True, "error": None},
        "blocks": [{
            "index": 0,
            "type": "NiNode",
            "name": "root",
            "status": "decoded",
            "local_transform": {
                "translate": [0.0, 0.0, 0.0],
                "rotate": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0]],
                "scale": 1.0,
            },
            "links": {},
        }],
        "scene_graph": {"edges": []},
    }
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        SB, "qc_our_parser_fx_VALID.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(our, fh, indent=1, sort_keys=False, ensure_ascii=True)
        fh.write("\n")
    print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
