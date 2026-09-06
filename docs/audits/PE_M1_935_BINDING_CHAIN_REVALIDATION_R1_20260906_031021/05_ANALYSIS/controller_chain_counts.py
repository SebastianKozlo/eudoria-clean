#!/usr/bin/env python3
"""05_ANALYSIS: controller-chain-inclusive edge count (era PCG_9_3_5).

The canon V2 controller-edge definition is DIRECT: (NiTexturingProperty,
NiFlipController) via fields['controller']. The 8 unattached flip controllers
found by the main driver are CHAINED controllers (property.controller ->
NiFlipController#1 -> next_controller -> NiFlipController#2, same target
property). This script counts the chain-inclusive attachment pairs
(property, controller) by traversing next_controller chains from
property.controller while the chain target property stays the same.
Read-only; frozen R61; same corpus pin as the main driver.
"""
import sys, os, json, struct
sys.dont_write_bytecode = True
RUN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN_DIR, "05_ANALYSIS", "CONTROLLER_CHAIN_COUNTS.json")
MODELS_BNT = r"D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
R61_SOURCE_DIR = r"D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source"
sys.path.insert(0, R61_SOURCE_DIR)
from pe_nif_reader import PENifReader  # noqa: E402

with open(MODELS_BNT, "rb") as f:
    data = f.read()
fs = len(data)
istart = struct.unpack_from("<I", data, fs - 8)[0]
count = struct.unpack_from("<I", data, istart)[0]
pos = istart + 4
entries = []
for _ in range(count):
    ne = pos
    while data[ne] != 0x0A:
        ne += 1
    name = data[pos:ne].decode("ascii", "replace")
    size, off = struct.unpack_from("<II", data, ne + 1)
    entries.append((name, size, off))
    pos = ne + 17

reader = PENifReader()
direct_edges = set()
chain_edges = set()          # (nif, prop_block, ctrl_block) reached via chains
flip_blocks = 0
chain_len_hist = {}
for name, size, off in entries:
    res = reader.parse_bytes(data[off:off + size], source_name=name)
    if res.parse_status != "PASS":
        continue
    bidx = {b.block_index: b for b in res.blocks}
    for b in res.blocks:
        if b.block_type == "NiFlipController":
            flip_blocks += 1
    for b in res.blocks:
        if b.block_type != "NiTexturingProperty":
            continue
        first = (b.fields or {}).get("controller", -1)
        if first == -1:
            continue
        fb = bidx.get(first)
        if fb is None or fb.block_type != "NiFlipController":
            continue
        direct_edges.add((name, b.block_index, first))
        # walk the controller chain
        cur = fb
        seen = set()
        chain = 0
        while cur is not None and cur.block_index not in seen:
            seen.add(cur.block_index)
            nxt = (cur.fields or {}).get("next_controller", -1)
            if nxt == -1 or nxt not in bidx:
                break
            nb = bidx[nxt]
            if nb.block_type == "NiFlipController":
                chain += 1
                chain_edges.add((name, b.block_index, nxt))
            cur = nb
        if chain:
            chain_len_hist[chain] = chain_len_hist.get(chain, 0) + 1

out = {
    "era": "PCG_9_3_5",
    "flip_controller_blocks": flip_blocks,
    "direct_controller_edges_canon_v2_definition": len(direct_edges),
    "chained_controller_edges_reached_via_next_controller": len(chain_edges),
    "chain_inclusive_total": len(direct_edges) + len(chain_edges),
    "properties_with_chains_histogram": chain_len_hist,
    "note": ("DIRECT = canon M3-4.5 V2 definition (NiTexturingProperty.controller "
             "-> NiFlipController). CHAIN-EXTRA = additional NiFlipController blocks "
             "reached by following next_controller chains from the directly attached "
             "controller (each chained controller's target is the SAME "
             "NiTexturingProperty). 2003 V2 reported 148 edges from 125 "
             "controllers; the exact 2003 traversal code is not extant, so both "
             "9.3.5 counts are reported under explicit semantics."),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
