#!/usr/bin/env python3
# -*- coding: ascii -*-
# append_v4_marks.py - W1: the append-only V4 supersession marks.
# Saves the .pre copies (append-only prefix proofs, like the completion run
# did) into THIS run's 01_RAW, then APPENDS the V4 correction record to
# GATE_INDEX.md and the V4 consolidation note to GATES\AMENDMENTS.md.
# Nothing above the appended section is touched; the .pre files are verified
# byte-prefixes of the post-append files by the consistency check.
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
GATE_INDEX = os.path.join(REPO_GATE, "GATE_INDEX.md")
AMENDMENTS = os.path.join(REPO_GATE, "GATES", "AMENDMENTS.md")
RAW = os.path.join(RUN_ROOT, "01_RAW")
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
MANIFEST_V4 = os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")
PC24 = os.path.join(RUN_ROOT, "01_RAW", "pc24_synthetic_measurement.json")

BASE_SHA = "faf215b4b5da80d30b895997c58f0a292d33fd08"
PIN_GATE_INDEX = "B8FD886BEF3575C048AA1978DE5908D6E0F8068A91EFC172EEB6456391A8A04B"
PIN_AMENDMENTS = "5403B19613CD9B6E39C134A9029F92506907B61289BC522523C1C370B4F57125"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    # fail-closed: the pre-append files must match the pinned SHAs
    gi_sha = sha256_file(GATE_INDEX)
    am_sha = sha256_file(AMENDMENTS)
    if gi_sha != PIN_GATE_INDEX or am_sha != PIN_AMENDMENTS:
        print("HARD STOP: pre-append file SHA mismatch.")
        print("  GATE_INDEX.md pinned=%s actual=%s" % (PIN_GATE_INDEX, gi_sha))
        print("  AMENDMENTS.md pinned=%s actual=%s" % (PIN_AMENDMENTS, am_sha))
        return 1
    # save the .pre copies (append-only prefix proofs)
    shutil.copyfile(GATE_INDEX, os.path.join(RAW, "GATE_INDEX.md.pre"))
    shutil.copyfile(AMENDMENTS, os.path.join(RAW, "AMENDMENTS.md.pre"))
    v4j = sha256_file(V4_JSON)
    v4m = sha256_file(V4_MD)
    mv4 = sha256_file(MANIFEST_V4)
    pc24_sha = sha256_file(PC24)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    gi_append = """

---

## THE V4 CORRECTION RECORD - PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 (appended %s)

The V4 correction (the corrected re-launch of the R1 mandate; R1 hard-stopped correctly on a
single-nibble pin transcription error and its evidence is preserved untouched at
`99_Audits\\PE_M1_GATE_V4_CORRECTION_R1_20260905_100405\\`) has executed, per the PE-MASTER-refined
12-point mandate. THIS section is APPENDED - nothing above was rewritten (the pre-append state is
frozen at `99_Audits\\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\\01_RAW\\GATE_INDEX.md.pre`,
SHA256 %s, a byte-prefix of this file - proven by the run's consistency check).

### The new LIVE files (the V4 layer)

- `GATES\\M1_GATE_DELIVERABLE_MATRIX_V4.md` (SHA256 %s) + `GATES\\M1_GATE_DELIVERABLE_MATRIX_V4.json`
  (SHA256 %s) - the corrected, semantically clean matrix: ALL 19 rows carry 9 FIELDS
  (KNOWLEDGE / IMPLEMENTATION / VALIDATION / HISTORICAL_FIDELITY / EVIDENCE_STATUS / ERA /
  DENOMINATOR / LIMITATIONS / EVIDENCE) in BOTH formats, with the five charter section-13 labels
  rendered per row (the V3 MD's verdict-only rendering - defect F1 - is not repeated).
- `EVIDENCE_MANIFEST_V4.json` (SHA256 %s) - the per-claim manifest built FROM THE V4 FIELDS (never
  from the old matrix's carried fields), every cited evidence SHA re-hashed at build time, the
  corrected oracle counter split (443,141 platform + 20,000 f80-exactness = 463,141 TOTAL), and
  the PC24 re-measurement record.

### The supersessions of record (append-only; every superseded file is FROZEN, untouched)

- the V3 matrix copies -> **FROZEN HISTORY, SUPERSEDED-BY-V4** (this is the mark; the files stay).
- `EVIDENCE_MANIFEST.json` -> **SUPERSEDED by EVIDENCE_MANIFEST_V4.json** (the file untouched;
  its stale carried fields - the rows-10/11 retracted arithmetic, the row-8 unbounded 'queued'
  line - are the superseded content).
- the repair-run STAGE_ACCEPTANCE_GATES.csv line-4 counter phrasing -> superseded by the corrected
  split (the frozen CSV NOT edited; the typed supersession record lives in EVIDENCE_MANIFEST_V4.json).

### The corrections applied (the 12-point mandate)

1. the six old-matrix field gaps composed + labeled (ROW2 historical_fidelity; ROW13/15/16/17
   implementation; ROW19 knowledge/implementation split).
2. the NO-COPY set recomposed from CURRENT evidence (rows 6/8/10/11/19 + the registry
   era_statements for P-RNG-DIV/P-POS-SCALE - the fourth stale carrier).
3. ROW10 = ONLY the iter035 arithmetic (nodeX/Y = f32(u16/65535.0 f64) node-local fractions [0,1];
   nodeScale = f32(|value * 0.00007812499825377017|) = float32(1/12800)-widened = 10737418/2^37;
   the retracted arithmetic wordings REMOVED).
4. ROW11 = the SUPERSEDED-LOCKED constants (_DAT_00a7d7a8 = 32767.0 f64; _DAT_00a8c758 = 65535.0
   f64) with the OPEN items kept ([P-RNG-P3]; the view-band p2 provenance; the actual-x87-CW
   conditionality - PC=24 breaks 14,104/229,376 = 6.15%% of the REAL lerp domain and
   103,073/1,245,184 of the synthetic domain).
5. ROW8 = the SINGLE ORIGINAL-DIRECT WITNESS (Models.bnt 457485 -> NIF v10.1.0.0 -> NiTriShape ->
   NiArkTextureExtraData 457490 -> TGA2; 16/16 strict) separated from the STILL-OPEN full
   clean-NIF path + the witness matrix + the scrambled-texture falsification.
6. the PC24 SYNTHETIC RE-MEASUREMENT (a measurement without an artifact is not evidence):
   38 frozen pairs x 32,768 = 1,245,184 comparisons; measured **103,073** - the citation is
   **CONFIRMED** (double measurement: PE-MASTER auditor-side + THIS run-side, independent
   implementations, exact agreement; the real-domain anchor 14,104 and the shared-pair
   self-consistency checks all PASS; the frozen domain_reproof.json untouched - HYG-1).
7. the semantic gate (the forbidden/required phrase lists + the negative fixtures N1-N4 + the
   clean-copy PASS) - see the run mirror 01_RAW\\semantic_gate_report.json.
8. the fail-closed consistency check (every pinned input re-hashed; the V3/old-matrix/old-manifest
   files untouched; the .pre prefix proofs; the payload scan) - 01_RAW\\consistency_report_v4.json.

### State after the V4 correction (binding)

M1 remains **PARTIAL / HARD_STOPPED_AT_GATE**; M2 remains HARD-STOPPED. This V4 correction closes
NOTHING beyond its own package; the open items live in `UNRESOLVED.md` + the V4 known-open set.
Provenance: built by pe-reconstruction from read-only records (BASE_SHA %s; the commit scope is
ONLY `docs\\audits\\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\\**` + the run mirror
`docs\\audits\\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\\**`; the run's control scripts + raw
outputs live under `99_Audits\\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\\`).
""" % (ts, gi_sha, v4m, v4j, mv4, BASE_SHA)

    am_append = """

---

## THE V4 CORRECTION (appended %s by PE_M1_GATE_V4_CORRECTION_R2_20260905_101327)

The V3 copies above are now **FROZEN HISTORY, SUPERSEDED-BY-V4**: the corrected, semantically
clean matrix is `M1_GATE_DELIVERABLE_MATRIX_V4.md` + `.json` in THIS directory (NEW physical
files; the V3 was never edited). The pre-append state of this file is frozen at
`99_Audits\\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\\01_RAW\\AMENDMENTS.md.pre` (SHA256 %s,
a byte-prefix of this file).

What the V4 changes relative to the V3 (per the V4 files' own consolidation statements):

- ALL 19 rows carry 9 FIELDS in BOTH formats and the MD renders the five charter section-13
  labels per row (the V3 MD's verdict-only rendering - the external post-audit's defect F1 - is
  not repeated);
- the six old-matrix field gaps are COMPOSED + LABELED ('composed in V4 from <source>'):
  ROW2 historical_fidelity, ROW13/15/16/17 implementation, ROW19 knowledge/implementation split;
- the NO-COPY set is recomposed from CURRENT evidence (never carried from ITER_048): rows 6, 8,
  10, 11, 19 + the registry era_statements for P-RNG-DIV/P-POS-SCALE (the fourth stale carrier -
  the V3 registry's era_statements contradicted their own SUPERSEDED-LOCKED v3_status);
- ROW10 KNOWLEDGE = ONLY the iter035 arithmetic (the V3 carried_knowledge carried the REJECTED
  arithmetic wordings - not carried into V4);
- ROW11 = the SUPERSEDED-LOCKED constants + the OPEN items kept (the V3 honest_bounds carried the
  retired candidate wording - not carried into V4);
- ROW8 = the SINGLE ORIGINAL-DIRECT WITNESS separated from the STILL-OPEN full clean-NIF path
  (the V3 honest_bounds' unbounded 'queued' line - not carried into V4);
- the corrected oracle counter split is carried (443,141 platform + 20,000 f80 = 463,141 TOTAL;
  the repair-run STAGE_ACCEPTANCE_GATES.csv line-4 phrasing superseded by a typed record in
  EVIDENCE_MANIFEST_V4.json - the frozen CSV NOT edited);
- the PC24 synthetic sensitivity is RE-MEASURED run-side: **103,073/1,245,184 CONFIRMED**
  (the double measurement; 01_RAW\\pc24_synthetic_measurement.json; the frozen domain_reproof.json
  untouched - its synthetic lerp_pc24_mismatches=0 is a DEFAULT COUNTER, HYG-1);
- the HYG-5 citation-label defect is NOT carried: iter033_manifest.json cites its own SHA
  (DD598152...); F299C622... is attached to assets/foliage_glb/MANIFEST.json.

Layering rule (now the standing form): read the frozen matrix + the amendment records above for
HISTORY; read the V3 copies for the validator-repair-era verdicts (frozen); read the
**V4 matrix** for the LIVE verdicts; read `../EVIDENCE_MANIFEST_V4.json` for the per-claim
evidence chain (source/generator/SHA/denominator/independent truth/why_non_circular/failure
case/dependencies/limitations); read `../CORRECTION_NOTES.md` for the hygiene corrections.

State: M1 remains PARTIAL / HARD_STOPPED_AT_GATE; nothing here authorizes M2.
""" % (ts, am_sha)

    with open(GATE_INDEX, "a", encoding="ascii", newline="") as f:
        f.write(gi_append)
    with open(AMENDMENTS, "a", encoding="ascii", newline="") as f:
        f.write(am_append)

    # verify the .pre files are byte-prefixes (fail-loud)
    for target, pre in ((GATE_INDEX, os.path.join(RAW, "GATE_INDEX.md.pre")),
                        (AMENDMENTS, os.path.join(RAW, "AMENDMENTS.md.pre"))):
        pre_bytes = open(pre, "rb").read()
        post_bytes = open(target, "rb").read()
        if not post_bytes.startswith(pre_bytes):
            print("HARD STOP: %s is not a byte-prefix of %s" % (pre, target))
            return 1
    print("append OK: GATE_INDEX.md (%s -> %s)" % (gi_sha[:12], sha256_file(GATE_INDEX)[:12]))
    print("append OK: AMENDMENTS.md (%s -> %s)" % (am_sha[:12], sha256_file(AMENDMENTS)[:12]))
    print("  .pre byte-prefix proofs: VERIFIED for both")
    return 0


if __name__ == "__main__":
    sys.exit(main())
