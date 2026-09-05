# -*- coding: utf-8 -*-
"""app_defs.py — constants for the PE_NIF_R3_PROPOSAL_APPLICATION_R1 driver.

Pinned inputs are re-hashed by apply_r1.py before use. Old fragments come from
the hash-pinned map_defs.py of PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203
(SHA256 aaa61d970503fde8cc7a2b4e399c5c1f7ba3ba5b03a074e36e4c26fd85515b49);
new texts come from the hash-pinned TARGET_MAP.json
(D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628).
"""
import os

RUN_ID = "PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500"
RUN_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500"
REPO = r"D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean"
DOCS_NIF = os.path.join(REPO, "docs", "nif")
AUDITS_LOCAL = r"D:\Eudoria_Reconstruction\99_Audits"
AUDITS_REPO = os.path.join(REPO, "docs", "audits")
TARGETMAP_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203"
R3_ROOT = r"D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627"
R2_LOCAL = os.path.join(AUDITS_LOCAL, "PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054")
R2_REPO = os.path.join(AUDITS_REPO, "PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054")

PIN = {
    "TARGET_MAP.json": (
        os.path.join(TARGETMAP_ROOT, "05_ANALYSIS", "TARGET_MAP.json"),
        "d3f043f2167c1bd0edbc9c4f7957d5fd31af37c8296848deeb9350dda7699628"),
    "PROPOSED_DOC_CORRECTIONS_R3.md": (
        os.path.join(R3_ROOT, "06_REPORT", "PROPOSED_DOC_CORRECTIONS_R3.md"),
        "84b3d05db719ab09a6ceece8300bbee059655b5443f6b5cfc1090b4c8b7ec8e6"),
    "PROPOSALS_P2P3_FIXED.md": (
        os.path.join(TARGETMAP_ROOT, "06_REPORT", "PROPOSALS_P2P3_FIXED.md"),
        "65dc552806c2c2a1e27a7abdb227b4ccf09a8c2a473bc6a9628655298a88de27"),
    "map_defs.py": (
        os.path.join(TARGETMAP_ROOT, "00_CONTROL", "map_defs.py"),
        "aaa61d970503fde8cc7a2b4e399c5c1f7ba3ba5b03a074e36e4c26fd85515b49"),
    "build_package_r1.py": (
        os.path.join(TARGETMAP_ROOT, "00_CONTROL", "build_package_r1.py"),
        "ed5fc01693ec6ffd739b64a25ad69e0c3df923fa996da043ae20c248aba31b38"),
    "TARGETMAP_NEXT_PROMPT.md": (
        os.path.join(TARGETMAP_ROOT, "00_CONTROL", "NEXT_PROMPT.md"),
        "c9ccb5bb56fa8dd8f140f4c3126adc8aa9beddc4cb14d50fb9d0b7c0329276a2"),
}

REPLACE_EDITS = ["P1R2-5-R3/a", "P1R2-5-R3/b", "P2R2-2-R3-FIXED/main"]
LEDGER_EDITS = ["P3R3/a", "P3R3/b1", "P3R3/b2", "P3R3/b3", "P3R3/b4",
                "P4R3/a", "P4R3/b1", "P4R3/b2", "P4R3/b3"]
RULE_EDITS = ["P3R3/c", "P4R3/c"]
POLICY_EDITS = ["P5R3/a", "P5R3/b"]
ALL_EDITS = REPLACE_EDITS + LEDGER_EDITS + RULE_EDITS + POLICY_EDITS

# annotation standing files: key -> (filename, short role)
ANN_FILES = [
    ("ledger", "CORRECTION_LEDGER.md",
     "correction-ledger supersession record (LEDGER-ENTRY operations)"),
    ("rules", "STANDING_RULES.md",
     "standing rules (STANDING-RULE operations)"),
    ("policies", "STANDING_POLICIES.md",
     "standing policies (STANDING-POLICY operations)"),
]
ANN_KEY_OF_EDIT = {}
for _e in LEDGER_EDITS:
    ANN_KEY_OF_EDIT[_e] = "ledger"
for _e in RULE_EDITS:
    ANN_KEY_OF_EDIT[_e] = "rules"
for _e in POLICY_EDITS:
    ANN_KEY_OF_EDIT[_e] = "policies"

# forbidden clauses (PROPOSALS_P2P3_FIXED.md forbidden exports + the P2/P3
# removed clauses from its driver's forbidden list)
FORBIDDEN = [
    "All 21 claims reproduced at 100%",
    "every BYTE-EXACT VALIDATOR reproduced at 100%",
    "every BYTE-EXACT VALIDATOR reproduced at 100",
    "zero-match is insensitive to value errors",
    "provably insensitive to value errors",
]

# P5R3/b absence re-verification patterns (the restatement trigger family)
P5B_ABSENCE_PATTERNS = [
    "semantic header normalization",
    "CUSTOM PHYSICAL-LINE CONTRACT",
    "physical-line contract",
    "bare CR inside a physical row",
]

R2_HIST_RELS = [
    "06_REPORT\\00_FINAL_REPORT.md",
    "00_CONTROL\\run_gates.py",
    "02_LOGS\\TEST_RESULTS.json",
    "STAGE_ACCEPTANCE_GATES.csv",
]

# short human titles for the 13 annotation entries
ENTRY_TITLES = {
    "P3R3/a": "R2 06_REPORT/00_FINAL_REPORT.md, Area B sentence (R2 Node hash-primitive method provenance)",
    "P3R3/b1": "R2 00_CONTROL/run_gates.py, R2G8 independence wording (three-computations claim)",
    "P3R3/b2": "R2 02_LOGS/TEST_RESULTS.json, R2G8 why_non_circular wording (three-computations claim)",
    "P3R3/b3": "R2 STAGE_ACCEPTANCE_GATES.csv row R2G8, independence wording (three-computations claim)",
    "P3R3/b4": "R2 STAGE_ACCEPTANCE_GATES.csv row R2G8, gate label phrase (Python==Node==R36)",
    "P4R3/a": "R2 00_CONTROL/run_gates.py L50 bool coercion (human-review gate state serialization)",
    "P4R3/b1": "R2 00_CONTROL/run_gates.py R2G13 gate label (stale tally wording)",
    "P4R3/b2": "R2 02_LOGS/TEST_RESULTS.json R2G13 gate_name (stale tally wording)",
    "P4R3/b3": "R2 STAGE_ACCEPTANCE_GATES.csv row R2G13 (stale tally wording)",
    "P3R3/c": "hash-primitive value identity before aggregate acceptance (the P0)",
    "P4R3/c": "overall executable pass distinct from human acceptance",
    "P5R3/a": "R2 Area C sidecar acceptance preserved; no manifest migration",
    "P5R3/b": "sidecar bare-CR semantic mapping policy (future-restatement guard)",
}
