#!/usr/bin/env python3
# -*- coding: ascii -*-
# append_v4_1_marks.py - the append-only V4.1 supersession marks (GATE_INDEX.md +
# GATES\AMENDMENTS.md). Fail-loud: verifies the current pre-append SHAs == the
# pins; appends in BINARY mode (byte-extension); verifies the .pre copies ==
# the pins AND the appended files are byte-extensions of the .pre copies.
import hashlib
import os
import sys
from datetime import datetime, timezone

RUN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RUN_ROOT, "01_RAW")
REPO_GATE = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE"
GATE_INDEX = os.path.join(REPO_GATE, "GATE_INDEX.md")
AMENDMENTS = os.path.join(REPO_GATE, "GATES", "AMENDMENTS.md")
V4_JSON = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.json")
V4_MD = os.path.join(REPO_GATE, "GATES", "M1_GATE_DELIVERABLE_MATRIX_V4.md")
MANIFEST = os.path.join(REPO_GATE, "EVIDENCE_MANIFEST_V4.json")

PIN_GATE_INDEX = "FD68060A63184B94753493D87A04CFB33FBA9667C07DD91D4D5B47810F1CC558"
PIN_AMENDMENTS = "C8FF0ABE475E7D37CE790F89CFB941E0FA4A5A0BA23B27921534EFFC6D51D347"
RUN_ID = "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528"
BASE_SHA = "58ab627"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def append_section(path, section_text):
    """binary byte-extension append (CRLF section)."""
    with open(path, "ab") as f:
        f.write(section_text.encode("ascii"))


def main():
    gi_sha, am_sha = sha256_file(GATE_INDEX), sha256_file(AMENDMENTS)
    if gi_sha != PIN_GATE_INDEX:
        raise SystemExit("HARD STOP: GATE_INDEX.md pre-append SHA mismatch (%s)" % gi_sha)
    if am_sha != PIN_AMENDMENTS:
        raise SystemExit("HARD STOP: AMENDMENTS.md pre-append SHA mismatch (%s)" % am_sha)
    v4j, v4m, mv4 = sha256_file(V4_JSON), sha256_file(V4_MD), sha256_file(MANIFEST)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # ---- the GATE_INDEX.md append
    gi_section = (
        "\r\n\r\n---\r\n\r\n"
        "## THE V4.1 REGISTRY-RESIDUAL RECORD - " + RUN_ID + " (appended " + ts + ")\r\n"
        "\r\n"
        "The bounded V4.1 residual fix (ordered by the PE-MASTER post-audit of the V4 correction - verdict\r\n"
        "MASTER_PARTIAL_PASS, commit " + BASE_SHA + ") has executed. THIS section is APPENDED - nothing above was\r\n"
        "rewritten (the pre-append state is frozen at\r\n"
        "`99_Audits\\" + RUN_ID + "\\01_RAW\\GATE_INDEX.md.pre`,\r\n"
        "SHA256 " + PIN_GATE_INDEX + ", a byte-prefix of this file - proven by the run's consistency check).\r\n"
        "\r\n"
        "### The residual and its fix (the post-audit's F-1)\r\n"
        "\r\n"
        "- THE RESIDUAL: the registry entries P-RNG-DIV/P-POS-SCALE carried in their LIVE `missing`/`why`\r\n"
        "  fields the verbatim-inherited pre-iter035 hypothesis \"reads 0.0 statically (runtime-initialized)\"\r\n"
        "  - FACTUALLY FALSE vs the byte-locked operands (0x00A7D7A8 = 32767.0 f64, bytes 00 00 00 00 C0 FF\r\n"
        "  DF 40; 0x00A8C758 = 65535.0 f64, bytes 00 00 00 00 E0 FF EF 40 - iter035, CONSTANT_ADDRESS_LOCK,\r\n"
        "  re-read by PE-MASTER at the R2 post-audit) and internally contradictory with the entries' own\r\n"
        "  SUPERSEDED-LOCKED v4_status. A MANDATE gap (the R2 no-copy set named only era_statement), not an\r\n"
        "  executor deviation.\r\n"
        "- THE FIX (composed from the existing records; ZERO new forensics): both entries' missing/why/\r\n"
        "  resume_path composed per the byte locks, each labeled \"composed in V4.1\": missing = NONE for\r\n"
        "  the divisor (byte-locked 32767.0 f64 @0x00A7D7A8 / 65535.0 f64 @0x00A8C758, iter035; the\r\n"
        "  historical open-item record follows); why = the TYPED SUPERSESSION record carrying the disproof\r\n"
        "  statement verbatim (the retired hypothesis wording is permitted ONLY in typed records);\r\n"
        "  resume_path = NONE for the divisor; runtime tracing remains relevant only to the actual-CW\r\n"
        "  question. The historical open-item record (the old missing/why/resume) is kept ONLY as the TYPED\r\n"
        "  RETRACTION record in the V4.1 JSON (historical context, NOT live status).\r\n"
        "- The LIVE MD layer renders the composed fields WITHOUT the retired wording (the R2-established\r\n"
        "  architecture: retired wordings live ONLY in typed JSON records).\r\n"
        "\r\n"
        "### The new LIVE SHAs (the V4.1 edit; the V4.1 layer = the V4 files edited in place)\r\n"
        "\r\n"
        "- `GATES\\M1_GATE_DELIVERABLE_MATRIX_V4.json` (SHA256 " + v4j + ") - the two registry entries\r\n"
        "  composed (the typed records); the other 17 entries + every other top-level key verified IDENTICAL.\r\n"
        "- `GATES\\M1_GATE_DELIVERABLE_MATRIX_V4.md` (SHA256 " + v4m + ") - the two registry lines\r\n"
        "  re-rendered; exactly 2 lines differ, the line count unchanged.\r\n"
        "- `EVIDENCE_MANIFEST_V4.json` (SHA256 " + mv4 + ") - the registry echo rebuilt FROM THE V4.1\r\n"
        "  fields + the built_from SHAs updated (the V4 md/json new SHAs); every other key verified IDENTICAL.\r\n"
        "\r\n"
        "### The extended semantic gate (re-executed in full)\r\n"
        "\r\n"
        "- Extended per the mandate: the FULL-document walk (ALL top-level keys of the V4.1 JSON + the full\r\n"
        "  manifest walk + the full MD text), the NEW forbidden phrases (\"reads 0.0 statically\", \"missing:\r\n"
        "  the exact RNG normalization divisor\", \"missing: the u16->world position divisor\" - permitted ONLY\r\n"
        "  in typed retraction/supersession records), the MD-parity rule, and the NEW negative fixture N6.\r\n"
        "  The clean edited V4.1 PASSES (0 hits / 0 problems); N1-N4 FAIL exactly as in the R2; N6 (the OLD\r\n"
        "  missing/why restored - the full pre-V4.1 registry state across the matrix + the manifest echo +\r\n"
        "  the MD lines) FAILS with hits in every scanned document - see the run mirror\r\n"
        "  01_RAW\\semantic_gate_report_v4_1.json.\r\n"
        "\r\n"
        "### State after the V4.1 residual fix (binding)\r\n"
        "\r\n"
        "M1 remains **PARTIAL / HARD_STOPPED_AT_GATE**; M2 remains HARD-STOPPED. This V4.1 run closes NOTHING\r\n"
        "except its own residual; the package now awaits the PE-MASTER re-audit, then the external re-judgment\r\n"
        "(the human's relay decision alone). Provenance: built by pe-reconstruction from read-only records\r\n"
        "(BASE_SHA " + BASE_SHA + "; the commit scope is ONLY\r\n"
        "`docs\\audits\\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\\**` + the run mirror\r\n"
        "`docs\\audits\\" + RUN_ID + "\\**`; the run's control scripts + raw outputs live under\r\n"
        "`99_Audits\\" + RUN_ID + "\\`).\r\n"
    )

    # ---- the AMENDMENTS.md append
    am_section = (
        "\r\n\r\n## THE V4.1 REGISTRY-RESIDUAL CORRECTION (appended " + ts + " by " + RUN_ID + ")\r\n"
        "\r\n"
        "The V4 matrix above is now the V4.1-EDITED LIVE LAYER: its registry entries P-RNG-DIV/P-POS-SCALE\r\n"
        "carried the PE-MASTER post-audit's F-1 residual (the LIVE missing/why fields carried the\r\n"
        "verbatim-inherited pre-iter035 hypothesis \"reads 0.0 statically (runtime-initialized)\" - factually\r\n"
        "false vs the iter035 byte locks and contradictory with the entries' own SUPERSEDED-LOCKED\r\n"
        "v4_status). The bounded fix, composed from the existing records (ZERO new forensics):\r\n"
        "\r\n"
        "- both entries' missing = \"composed in V4.1: NONE for the divisor (byte-locked 32767.0 f64\r\n"
        "  @0x00A7D7A8 / 65535.0 f64 @0x00A8C758, iter035; the historical open-item record follows)\";\r\n"
        "- both entries' why = the TYPED SUPERSESSION record carrying the disproof statement verbatim (the\r\n"
        "  pre-iter035 hypothesis was DISPROVEN by the byte lock - the slot is file-backed .rdata with the\r\n"
        "  exact bytes); the retired hypothesis wording is permitted ONLY in that typed record;\r\n"
        "- both entries' resume_path = \"composed in V4.1: NONE for the divisor; runtime tracing remains\r\n"
        "  relevant only to the actual-CW question\";\r\n"
        "- the historical open-item record (the old missing/why/resume) is kept ONLY as the TYPED RETRACTION\r\n"
        "  record in the V4.1 JSON (historical context, NOT live status);\r\n"
        "- EVIDENCE_MANIFEST_V4.json: the registry echo rebuilt FROM THE V4.1 fields + the built_from SHAs\r\n"
        "  updated (the V4 md/json new SHAs);\r\n"
        "- the extended semantic gate: the clean V4.1 PASSES; N1-N6 ALL FAIL (N6 = the OLD missing/why\r\n"
        "  restored).\r\n"
        "\r\n"
        "The pre-append state of this file is frozen at\r\n"
        "`99_Audits\\" + RUN_ID + "\\01_RAW\\AMENDMENTS.md.pre` (SHA256\r\n"
        + PIN_AMENDMENTS + ", a byte-prefix of this file).\r\n"
        "\r\n"
        "Layering rule (unchanged): read the frozen matrix + the amendment records above for HISTORY; read\r\n"
        "the **V4 (V4.1-edited) matrix** for the LIVE verdicts; read `../EVIDENCE_MANIFEST_V4.json` for the\r\n"
        "per-claim evidence chain; the TYPED records in the registry entries are the ONLY carriers of the\r\n"
        "retired wordings.\r\n"
        "\r\n"
        "State: M1 remains PARTIAL / HARD_STOPPED_AT_GATE; nothing here authorizes M2.\r\n"
    )

    append_section(GATE_INDEX, gi_section)
    append_section(AMENDMENTS, am_section)

    # ---- the append-only proofs (fail-loud)
    ok = True
    for target, pre, pin in ((GATE_INDEX, os.path.join(RAW, "GATE_INDEX.md.pre"), PIN_GATE_INDEX),
                             (AMENDMENTS, os.path.join(RAW, "AMENDMENTS.md.pre"), PIN_AMENDMENTS)):
        pre_sha = sha256_file(pre)
        pre_b = open(pre, "rb").read()
        cur_b = open(target, "rb").read()
        prefix_ok = cur_b.startswith(pre_b)
        print("%s: pre_sha==pin %s | byte-prefix %s | new sha %s"
              % (os.path.basename(target), pre_sha == pin, prefix_ok, sha256_file(target)))
        if pre_sha != pin or not prefix_ok:
            ok = False
    if not ok:
        raise SystemExit("HARD STOP: the append-only proofs failed")
    print("append-only marks: OK (GATE_INDEX.md -> %s ; AMENDMENTS.md -> %s)"
          % (sha256_file(GATE_INDEX), sha256_file(AMENDMENTS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
